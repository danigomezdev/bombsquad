package bsremote.less.network

import bsremote.less.Protocol
import bsremote.less.model.RemoteState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import kotlinx.coroutines.Job
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlin.time.TimeSource

enum class ConnectionStatus {
    DISCONNECTED, CONNECTING, CONNECTED, ERROR
}

data class ConnectionInfo(
    val status: ConnectionStatus = ConnectionStatus.DISCONNECTED,
    val playerId: Int = -1,
    val protocolV2: Boolean = false,
    val lagMs: Long = 0,
    val errorMessage: String = ""
)

class Connection {
    private val _info = MutableStateFlow(ConnectionInfo())
    val info: StateFlow<ConnectionInfo> = _info.asStateFlow()

    private val _state = MutableStateFlow(RemoteState())

    private var socket: UdpSocket? = null
    private var serverAddress = ""
    private var serverPort = 0
    private var job: Job? = null

    // Circular state buffers indexed 0-255
    private val statesV1 = ShortArray(Protocol.STATE_HISTORY_SIZE)
    private val statesV2 = IntArray(Protocol.STATE_HISTORY_SIZE)
    private val stateBirthTimes = LongArray(Protocol.STATE_HISTORY_SIZE)

    private var nextState = 0
    private var requestedState = 0
    private var lastSentValue = Int.MIN_VALUE
    private var lastStateTime = 0L

    private var playerId = -1
    private var protocolV2 = false
    private var requestId = 0

    private val packetChannel = Channel<ReceivedPacket>(capacity = 32)

    private val startMark = TimeSource.Monotonic.markNow()
    private fun nowMs(): Long = startMark.elapsedNow().inWholeMilliseconds

    fun setState(state: RemoteState) {
        _state.value = state
    }

    fun connect(address: String, port: Int, playerName: String, uniqueId: Int, scope: CoroutineScope) {
        val s = UdpSocket()
        socket = s
        serverAddress = address
        serverPort = port
        requestId = (nowMs() % 10000).toInt()
        playerId = -1
        protocolV2 = false
        nextState = 0
        requestedState = 0
        lastSentValue = Int.MIN_VALUE
        lastStateTime = 0L
        _state.value = RemoteState()

        val now = nowMs()
        for (i in 0 until Protocol.STATE_HISTORY_SIZE) {
            stateBirthTimes[i] = now
        }

        _info.value = ConnectionInfo(status = ConnectionStatus.CONNECTING)

        println("[Connection] connecting to $address:$port as '$playerName'")

        job = scope.launch {
            val receiveJob = launch(Dispatchers.IO) {
                s.setTimeout(2000)
                println("[Connection] receive loop started")
                while (isActive) {
                    try {
                        val packet = s.receive(16) ?: continue
                        println("[Connection] packet received type=${packet.data[0].toInt() and 0xFF} len=${packet.length}")
                        packetChannel.trySend(packet)
                    } catch (e: Exception) {
                        if (!isActive) break
                        println("[Connection] receive error: ${e.message}")
                    }
                }
            }

            // Must use Dispatchers.IO — process() calls socket.send() which is blocking IO
            val processJob = launch(Dispatchers.IO) {
                println("[Connection] process loop started")
                while (isActive) {
                    drainPackets()
                    process(playerName, uniqueId)
                    delay(Protocol.PROCESS_INTERVAL_MS)
                }
            }

            receiveJob.join()
            processJob.join()
        }
    }

    fun disconnect() {
        val s = socket ?: return
        val id = playerId
        if (id != -1) {
            try {
                s.send(byteArrayOf(Protocol.MSG_DISCONNECT, id.toByte()), serverAddress, serverPort)
            } catch (e: Exception) { }
        }
        _info.value = ConnectionInfo(status = ConnectionStatus.DISCONNECTED)
        job?.cancel()
        s.close()
        socket = null
        playerId = -1
    }

    private fun drainPackets() {
        while (true) {
            val packet = packetChannel.tryReceive().getOrNull() ?: break
            handlePacket(packet)
        }
    }

    private fun handlePacket(packet: ReceivedPacket) {
        if (packet.length < 1) return
        val buf = packet.data

        when (buf[0]) {
            Protocol.MSG_ID_RESPONSE -> {
                println("[Connection] MSG_ID_RESPONSE len=${packet.length} status=${_info.value.status}")
                if (packet.length == 3 && _info.value.status == ConnectionStatus.CONNECTING) {
                    playerId = buf[1].toInt() and 0xFF
                    protocolV2 = (buf[2].toInt() and 0xFF) == Protocol.RESPONSE_PROTOCOL_V2
                    nextState = 0
                    println("[Connection] connected! playerId=$playerId protocolV2=$protocolV2")
                    _info.value = _info.value.copy(
                        status = ConnectionStatus.CONNECTED,
                        playerId = playerId,
                        protocolV2 = protocolV2
                    )
                }
            }
            Protocol.MSG_STATE_ACK -> {
                if (packet.length == 2) {
                    val ackIndex = buf[1].toInt() and 0xFF
                    val diff = (ackIndex - requestedState) and 0xFF
                    if (diff in 1..127) {
                        val lastAcked = (ackIndex - 1) and 0xFF
                        val lag = nowMs() - stateBirthTimes[lastAcked]
                        requestedState = ackIndex
                        _info.value = _info.value.copy(lagMs = lag)
                    }
                }
            }
            Protocol.MSG_DISCONNECT_ACK -> {
                if (packet.length == 1) {
                    _info.value = ConnectionInfo(status = ConnectionStatus.DISCONNECTED)
                    job?.cancel()
                }
            }
            Protocol.MSG_DISCONNECT -> {
                if (packet.length == 2) {
                    val msg = when (buf[1].toInt() and 0xFF) {
                        Protocol.DISCONNECT_VERSION_MISMATCH -> "Version mismatch"
                        Protocol.DISCONNECT_GAME_SHUTTING_DOWN -> "Game is shutting down"
                        Protocol.DISCONNECT_NOT_ACCEPTING -> "Game is full"
                        else -> "Disconnected"
                    }
                    _info.value = ConnectionInfo(
                        status = ConnectionStatus.ERROR,
                        errorMessage = msg
                    )
                    job?.cancel()
                }
            }
        }
    }

    private fun process(playerName: String, uniqueId: Int) {
        when (_info.value.status) {
            ConnectionStatus.CONNECTING -> sendIdRequest(playerName, uniqueId)
            ConnectionStatus.CONNECTED -> {
                val now = nowMs()
                val force = (now - lastStateTime) >= Protocol.KEEPALIVE_INTERVAL_MS
                doStateChange(force)
                if (protocolV2) shipStatesV2() else shipStatesV1()
            }
            else -> {}
        }
    }

    private fun sendIdRequest(playerName: String, uniqueId: Int) {
        println("[Connection] sending ID request to $serverAddress:$serverPort")
        val cleanName = playerName.replace("#", "")
        val deviceName = "$cleanName#$uniqueId"
        val nameBytes = deviceName.encodeToByteArray()
        val dLen = minOf(nameBytes.size, 99)

        val data = ByteArray(128)
        data[0] = Protocol.MSG_ID_REQUEST
        data[1] = 121 // old protocol compat byte
        data[2] = (requestId and 0xFF).toByte()
        data[3] = (requestId shr 8).toByte()
        data[4] = Protocol.REQUEST_PROTOCOL_VERSION.toByte()
        for (i in 0 until dLen) data[5 + i] = nameBytes[i]

        try {
            socket?.send(data.copyOf(5 + dLen), serverAddress, serverPort)
        } catch (e: Exception) { }
    }

    private fun doStateChange(force: Boolean) {
        if (playerId == -1) return
        if (protocolV2) doStateChangeV2(force) else doStateChangeV1(force)
    }

    private fun doStateChangeV2(force: Boolean) {
        val encoded = _state.value.encodeV2()
        if (encoded == lastSentValue && !force) return

        stateBirthTimes[nextState] = nowMs()
        statesV2[nextState] = encoded
        nextState = (nextState + 1) and 0xFF
        lastSentValue = encoded
        lastStateTime = nowMs()
    }

    private fun doStateChangeV1(force: Boolean) {
        val encoded = _state.value.encodeV1()
        if (encoded.toInt() == lastSentValue && !force) return

        stateBirthTimes[nextState] = nowMs()
        statesV1[nextState] = encoded
        nextState = (nextState + 1) and 0xFF
        lastSentValue = encoded.toInt()
        lastStateTime = nowMs()
    }

    private fun shipStatesV2() {
        val id = playerId
        if (id == -1) return
        var count = (nextState - requestedState) and 0xFF
        if (count > Protocol.MAX_STATES_PER_PACKET) count = Protocol.MAX_STATES_PER_PACKET
        if (count < 1) return

        val data = ByteArray(4 + 3 * count)
        data[0] = Protocol.MSG_STATE2
        data[1] = id.toByte()
        data[2] = count.toByte()
        var s = (nextState - count) and 0xFF
        data[3] = s.toByte()

        var idx = 4
        repeat(count) {
            data[idx++] = (statesV2[s] and 0xFF).toByte()
            data[idx++] = ((statesV2[s] shr 8) and 0xFF).toByte()
            data[idx++] = ((statesV2[s] shr 16) and 0xFF).toByte()
            s = (s + 1) and 0xFF
        }

        try {
            socket?.send(data, serverAddress, serverPort)
        } catch (e: Exception) {
            _info.value = _info.value.copy(
                status = ConnectionStatus.ERROR,
                errorMessage = "Game shut down"
            )
        }
    }

    private fun shipStatesV1() {
        val id = playerId
        if (id == -1) return
        var count = (nextState - requestedState) and 0xFF
        if (count > Protocol.MAX_STATES_PER_PACKET) count = Protocol.MAX_STATES_PER_PACKET
        if (count < 1) return

        val data = ByteArray(4 + 2 * count)
        data[0] = Protocol.MSG_STATE
        data[1] = id.toByte()
        data[2] = count.toByte()
        var s = (nextState - count) and 0xFF
        data[3] = s.toByte()

        var idx = 4
        repeat(count) {
            data[idx++] = (statesV1[s].toInt() and 0xFF).toByte()
            data[idx++] = (statesV1[s].toInt() shr 8).toByte()
            s = (s + 1) and 0xFF
        }

        try {
            socket?.send(data, serverAddress, serverPort)
        } catch (e: Exception) {
            _info.value = _info.value.copy(
                status = ConnectionStatus.ERROR,
                errorMessage = "Game shut down"
            )
        }
    }
}
