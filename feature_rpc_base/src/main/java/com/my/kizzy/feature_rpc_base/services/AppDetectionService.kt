/*
 *
 *  ******************************************************************
 *  *  * Copyright (C) 2022
 *  *  * AppDetectionService.kt is part of Kizzy
 *  *  *  and can not be copied and/or distributed without the express
 *  *  * permission of yzziK(Vaibhav)
 *  *  *****************************************************************
 *
 *
 */

@file:Suppress("DEPRECATION")

package com.my.kizzy.feature_rpc_base.services

import android.app.Notification
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.app.usage.UsageStats
import android.app.usage.UsageStatsManager
import android.content.Intent
import android.os.IBinder
import com.blankj.utilcode.util.AppUtils
import com.my.kizzy.data.rpc.KizzyRPC
import com.my.kizzy.data.rpc.RpcImage
import com.my.kizzy.domain.model.rpc.RpcButtons
import com.my.kizzy.feature_rpc_base.Constants
import com.my.kizzy.feature_rpc_base.setLargeIcon
import com.my.kizzy.preference.Prefs
import com.my.kizzy.resources.R
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import java.util.SortedMap
import java.util.TreeMap
import javax.inject.Inject

import io.ktor.client.call.*
import io.ktor.client.request.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import org.json.JSONObject

data class BombsquadDataRaw(
    val serverName: String,
    val ip: String,
    val port: String,
    val players: String,
    val timestamp: Long
)

@AndroidEntryPoint
class AppDetectionService : Service() {

    @Inject
    lateinit var kizzyRPC: KizzyRPC

    @Inject
    lateinit var scope: CoroutineScope

    @Inject
    lateinit var notificationBuilder: Notification.Builder

    @Inject
    lateinit var notificationManager: NotificationManager

    private lateinit var pendingIntent: PendingIntent

    private lateinit var restartPendingIntent: PendingIntent

    private var runningPackage = ""
    override fun onBind(intent: Intent): IBinder? = null
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == Constants.ACTION_STOP_SERVICE) {
            stopSelf()
        } else if (intent?.action == Constants.ACTION_RESTART_SERVICE) {
            stopSelf()
            startService(Intent(this, AppDetectionService::class.java))
        } else {
            handleAppDetection()
        }
        return super.onStartCommand(intent, flags, startId)
    }

    override fun onDestroy() {
        scope.cancel()
        kizzyRPC.closeRPC()
        super.onDestroy()
    }

    private fun handleAppDetection() {
        val enabledPackages = getEnabledPackages()

        val stopIntent = createStopIntent()
        pendingIntent = createPendingIntent(stopIntent)

        val restartIntent = createRestartIntent()
        restartPendingIntent = PendingIntent.getService(
            this,
            0, restartIntent, PendingIntent.FLAG_IMMUTABLE
        )
        // Adding action to notification builder here to avoid having multiple Exit buttons
        // https://github.com/dead8309/Kizzy/issues/197
        notificationBuilder
            .setSmallIcon(R.drawable.ic_apps)
            .addAction(R.drawable.ic_apps, getString(R.string.restart), restartPendingIntent)
            .addAction(R.drawable.ic_apps, getString(R.string.exit), pendingIntent)


        startForeground(Constants.NOTIFICATION_ID, createDefaultNotification())

        val rpcButtons = getRpcButtons()

        scope.launch {
            while (isActive) {
                val queryUsageStats = getUsageStats()

                if (queryUsageStats != null && queryUsageStats.size > 1) {
                    val packageName = getLatestPackageName(queryUsageStats)
                    if (packageName != null && packageName !in EXCLUDED_APPS) {
                        handleValidPackage(packageName, enabledPackages, rpcButtons)
                    }
                }
                delay(5000)
            }
        }
    }

    private fun getEnabledPackages(): List<String> {
        val apps = Prefs[Prefs.ENABLED_APPS, "[]"]
        return Json.decodeFromString(apps)
    }

    private fun getRpcButtons(): RpcButtons {
        val rpcButtonsString = Prefs[Prefs.RPC_BUTTONS_DATA, "{}"]
        return Json.decodeFromString(rpcButtonsString)
    }

    private fun getUsageStats(): List<UsageStats>? {
        val usageStatsManager = getSystemService(USAGE_STATS_SERVICE) as UsageStatsManager
        val currentTimeMillis = System.currentTimeMillis()
        return usageStatsManager.queryUsageStats(
            UsageStatsManager.INTERVAL_DAILY,
            currentTimeMillis - 10000,
            currentTimeMillis
        )
    }

    private fun getLatestPackageName(usageStats: List<UsageStats>): String? {
        val treeMap: SortedMap<Long, UsageStats> = TreeMap()
        for (usageStatsItem in usageStats) {
            treeMap[usageStatsItem.lastTimeUsed] = usageStatsItem
        }
        return treeMap.lastKey()?.let { treeMap[it]?.packageName }
    }

    private suspend fun handleValidPackage(
        packageName: String,
        enabledPackages: List<String>,
        rpcButtons: RpcButtons,
    ) {
        if (packageName in enabledPackages && packageName != runningPackage) {
            handleEnabledPackage(packageName, rpcButtons)
            runningPackage = packageName
        } else if (packageName != runningPackage) {
            handleDisabledPackage()
            runningPackage = ""
        }
    }

    private suspend fun handleEnabledPackage(packageName: String, rpcButtons: RpcButtons) {
        val bombsquadPackage: String = "net.froemling.bombsquad"

        if (!kizzyRPC.isRpcRunning()) {
            kizzyRPC.apply {
                setName(AppUtils.getAppName(packageName))

                //if (packageName == bombsquadPackage) {
                //    setDetails("Teams @ US Tests 1")
                //    setPartySize(2,8)
                //}

                if (packageName == bombsquadPackage) {

                    scope.launch {
                        getBombsquadDataFlow().collect { data ->
                            //println("Respuesta BombSquad -> $data")

                            val players = data.players.split("/")
                            val current = players.getOrNull(0)?.toIntOrNull() ?: 0
                            val max = players.getOrNull(1)?.toIntOrNull() ?: 0

                            kizzyRPC.apply {
                                val details = if (data.serverName == "server not found") {
                                    "Menú principal"
                                } else {
                                    data.serverName
                                }
                                setDetails(details)
                                setPartySize(current, max)
                                build()
                            }
                        }
                    }

                }

                setStartTimestamps(System.currentTimeMillis())
                setStatus(Prefs[Prefs.CUSTOM_ACTIVITY_STATUS, "dnd"])
                setLargeImage(RpcImage.ApplicationIcon(packageName, this@AppDetectionService))
                if (Prefs[Prefs.USE_RPC_BUTTONS, false]) {
                    with(rpcButtons) {
                        setButton1(button1.takeIf { it.isNotEmpty() })
                        setButton1URL(button1Url.takeIf { it.isNotEmpty() })
                        setButton2(button2.takeIf { it.isNotEmpty() })
                        setButton2URL(button2Url.takeIf { it.isNotEmpty() })
                    }
                }
                build()
            }
        }
        notificationManager.notify(
            Constants.NOTIFICATION_ID, notificationBuilder
                .setContentText(
                    if (packageName == bombsquadPackage)
                        "Detección BombSquad: ${packageName}"
                    else
                        packageName
                )

                .setLargeIcon(
                    rpcImage = RpcImage.ApplicationIcon(packageName, this@AppDetectionService),
                    context = this@AppDetectionService
                )
                .build()
        )
    }

    fun getBombsquadDataFlow(): Flow<BombsquadDataRaw> = flow {
        while (true) {
            try {
                val rawJson: String = NetworkClient.httpClient
                    .get("http://127.0.0.1:26000/")
                    .body()

                val json = JSONObject(rawJson)

                val data = BombsquadDataRaw(
                    serverName = json.optString("server_name", "unknown"),
                    ip = json.optString("ip", "unknown"),
                    port = json.opt("port").toString(),
                    players = json.optString("players", "0/0"),
                    timestamp = json.optLong("timestamp", 0)
                )

                emit(data) // we send the object
            } catch (e: Exception) {
                println("❌ Error BombSquad: ${e.message}")
            }

            delay(3000) // wait 3 seconds
        }
    }

    private fun handleDisabledPackage() {
        if (kizzyRPC.isRpcRunning()) {
            kizzyRPC.closeRPC()
        }
        notificationManager.notify(Constants.NOTIFICATION_ID, createDefaultNotification())
    }

    private fun createDefaultNotification(): Notification {
        return Notification.Builder(this, Constants.CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_apps)
            .setContentTitle(getString(R.string.service_enabled))
            .addAction(R.drawable.ic_apps, getString(R.string.exit), pendingIntent)
            .addAction(R.drawable.ic_apps, getString(R.string.restart), restartPendingIntent)
            .build()
    }

    private fun createStopIntent(): Intent {
        val stopIntent = Intent(this, AppDetectionService::class.java)
        stopIntent.action = Constants.ACTION_STOP_SERVICE
        return stopIntent
    }

    private fun createRestartIntent(): Intent {
        val restartIntent = Intent(this, AppDetectionService::class.java)
        restartIntent.action = Constants.ACTION_RESTART_SERVICE
        return restartIntent
    }

    private fun createPendingIntent(stopIntent: Intent): PendingIntent {
        return PendingIntent.getService(this, 0, stopIntent, PendingIntent.FLAG_IMMUTABLE)
    }

    companion object {
        val EXCLUDED_APPS = listOf("com.my.kizzy", "com.discord")
    }
}
