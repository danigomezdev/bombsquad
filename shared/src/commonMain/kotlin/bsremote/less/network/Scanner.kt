package bsremote.less.network

import bsremote.less.Protocol
import bsremote.less.model.Party
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlin.time.TimeSource

class Scanner {
    private val _parties = MutableStateFlow<List<Party>>(emptyList())
    val parties: StateFlow<List<Party>> = _parties.asStateFlow()

    private var socket: UdpSocket? = null
    private val entries = mutableMapOf<String, Party>()
    private val mutex = Mutex()
    private var job: Job? = null
    private val startMark = TimeSource.Monotonic.markNow()

    private fun nowMs(): Long = startMark.elapsedNow().inWholeMilliseconds

    fun start(scope: CoroutineScope) {
        val s = UdpSocket()
        socket = s
        s.setBroadcast(true)
        s.setTimeout(Protocol.SOCKET_TIMEOUT_MS)

        println("[Scanner] starting, socket ready")

        job = scope.launch {
            // IO: blocking receive loop
            val receiveJob = launch(Dispatchers.IO) {
                println("[Scanner] receive loop started")
                while (isActive) {
                    try {
                        val packet = s.receive(256) ?: continue
                        if (packet.length > 1 && packet.data[0] == Protocol.PACKET_GAME_RESPONSE) {
                            val name = packet.data.decodeToString(1, packet.length)
                            println("[Scanner] found server: $name @ ${packet.senderAddress}:${packet.senderPort}")
                            val party = Party(name, packet.senderAddress, packet.senderPort, nowMs())
                            mutex.withLock {
                                entries[name] = party
                                _parties.value = entries.values.toList()
                            }
                        }
                    } catch (e: Exception) {
                        if (!isActive) break
                        println("[Scanner] receive error: ${e.message}")
                    }
                }
                println("[Scanner] receive loop stopped")
            }

            // IO: broadcast + prune loop (send must not run on Main)
            val broadcastJob = launch(Dispatchers.IO) {
                println("[Scanner] broadcast loop started")
                while (isActive) {
                    trySendBroadcast(s)
                    delay(1000)
                    pruneOld()
                }
            }

            receiveJob.join()
            broadcastJob.join()
        }
    }

    fun stop() {
        println("[Scanner] stopping")
        job?.cancel()
        socket?.close()
        socket = null
        entries.clear()
        _parties.value = emptyList()
    }

    private fun trySendBroadcast(s: UdpSocket) {
        try {
            s.sendBroadcast(byteArrayOf(Protocol.PACKET_GAME_QUERY), Protocol.DISCOVERY_PORT)
            println("[Scanner] broadcast sent")
        } catch (e: Exception) {
            println("[Scanner] broadcast error: ${e.message}")
        }
    }

    private suspend fun pruneOld() {
        val now = nowMs()
        mutex.withLock {
            val stale = entries.filter { now - it.value.lastSeenMs > Protocol.SERVER_TIMEOUT_MS }
            if (stale.isNotEmpty()) {
                println("[Scanner] pruning ${stale.size} stale server(s)")
                stale.keys.forEach { entries.remove(it) }
                _parties.value = entries.values.toList()
            }
        }
    }
}
