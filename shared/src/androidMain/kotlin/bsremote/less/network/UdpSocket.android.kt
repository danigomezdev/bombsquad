package bsremote.less.network

import android.util.Log
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.NetworkInterface
import java.net.SocketTimeoutException

private const val TAG = "BSRemote.UdpSocket"

actual class UdpSocket {
    private val socket = DatagramSocket()

    init {
        Log.d(TAG, "socket created on port ${socket.localPort}")
    }

    actual fun setBroadcast(enabled: Boolean) {
        socket.broadcast = enabled
        Log.d(TAG, "broadcast=$enabled")
    }

    actual fun setTimeout(ms: Int) {
        socket.soTimeout = ms
    }

    actual fun send(data: ByteArray, address: String, port: Int) {
        val addr = InetAddress.getByName(address)
        socket.send(DatagramPacket(data, data.size, addr, port))
    }

    actual fun sendBroadcast(data: ByteArray, port: Int) {
        var sentCount = 0
        try {
            val interfaces = NetworkInterface.getNetworkInterfaces() ?: run {
                Log.w(TAG, "sendBroadcast: no network interfaces found")
                return
            }
            for (iface in interfaces.asSequence()) {
                if (!iface.isUp || iface.isLoopback) continue
                for (ifAddr in iface.interfaceAddresses) {
                    val broadcast = ifAddr.broadcast ?: continue
                    try {
                        socket.send(DatagramPacket(data, data.size, broadcast, port))
                        Log.d(TAG, "sent broadcast to $broadcast via ${iface.name}")
                        sentCount++
                    } catch (e: Exception) {
                        Log.w(TAG, "broadcast failed on ${iface.name}: ${e.message}")
                    }
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "sendBroadcast error: ${e.message}", e)
        }
        if (sentCount == 0) {
            Log.w(TAG, "sendBroadcast: no interface accepted the packet")
        }
    }

    actual fun receive(bufferSize: Int): ReceivedPacket? {
        return try {
            val buf = ByteArray(bufferSize)
            val packet = DatagramPacket(buf, buf.size)
            socket.receive(packet)
            Log.v(TAG, "received ${packet.length} bytes from ${packet.address}:${packet.port}")
            ReceivedPacket(
                data = packet.data,
                length = packet.length,
                senderAddress = packet.address?.hostAddress ?: "",
                senderPort = packet.port
            )
        } catch (e: SocketTimeoutException) {
            null
        }
    }

    actual fun close() {
        Log.d(TAG, "closing socket")
        socket.close()
    }
}
