package bsremote.less

import android.app.Application
import android.content.Context
import android.net.wifi.WifiManager
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import bsremote.less.model.Party
import bsremote.less.model.RemoteState
import bsremote.less.network.Connection
import bsremote.less.network.ConnectionInfo
import bsremote.less.network.ConnectionStatus
import bsremote.less.network.Scanner
import kotlinx.coroutines.flow.StateFlow
import kotlin.random.Random

private const val TAG = "BSRemote.ViewModel"

class AppViewModel(application: Application) : AndroidViewModel(application) {
    private val scanner = Scanner()
    private val connection = Connection()

    val parties: StateFlow<List<Party>> = scanner.parties
    val connectionInfo: StateFlow<ConnectionInfo> = connection.info

    var playerName: String = "Player"
    private val uniqueId: Int = Random.nextInt(1, 65535)

    // Needed to receive UDP broadcast packets on WiFi on Android
    private val wifiManager =
        application.getSystemService(Context.WIFI_SERVICE) as WifiManager
    private val multicastLock =
        wifiManager.createMulticastLock("BSRemote").apply {
            setReferenceCounted(true)
        }

    init {
        acquireMulticastLock()
        scanner.start(viewModelScope)
    }

    private fun acquireMulticastLock() {
        try {
            if (!multicastLock.isHeld) {
                multicastLock.acquire()
                Log.d(TAG, "multicast lock acquired")
            }
        } catch (e: Exception) {
            Log.e(TAG, "failed to acquire multicast lock: ${e.message}")
        }
    }

    private fun releaseMulticastLock() {
        try {
            if (multicastLock.isHeld) {
                multicastLock.release()
                Log.d(TAG, "multicast lock released")
            }
        } catch (e: Exception) {
            Log.e(TAG, "failed to release multicast lock: ${e.message}")
        }
    }

    fun connectTo(party: Party) {
        Log.d(TAG, "connecting to ${party.name} @ ${party.address}:${party.port}")
        scanner.stop()
        connection.connect(party.address, party.port, playerName, uniqueId, viewModelScope)
    }

    fun connectToAddress(address: String, port: Int) {
        Log.d(TAG, "connecting to $address:$port")
        scanner.stop()
        connection.connect(address, port, playerName, uniqueId, viewModelScope)
    }

    fun disconnect() {
        Log.d(TAG, "disconnecting")
        connection.disconnect()
        acquireMulticastLock()
        scanner.start(viewModelScope)
    }

    fun setRemoteState(state: RemoteState) {
        connection.setState(state)
    }

    fun isConnected(): Boolean =
        connectionInfo.value.status == ConnectionStatus.CONNECTED

    override fun onCleared() {
        scanner.stop()
        connection.disconnect()
        releaseMulticastLock()
    }
}
