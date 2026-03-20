package bsremote.less.network

data class ReceivedPacket(
    val data: ByteArray,
    val length: Int,
    val senderAddress: String,
    val senderPort: Int
)

expect class UdpSocket() {
    fun setBroadcast(enabled: Boolean)
    fun setTimeout(ms: Int)
    fun send(data: ByteArray, address: String, port: Int)
    fun sendBroadcast(data: ByteArray, port: Int)

    // Returns null on timeout, throws on socket closed or fatal error
    fun receive(bufferSize: Int): ReceivedPacket?

    fun close()
}
