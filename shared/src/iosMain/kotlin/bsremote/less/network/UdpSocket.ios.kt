package bsremote.less.network

import kotlinx.cinterop.ExperimentalForeignApi
import kotlinx.cinterop.IntVar
import kotlinx.cinterop.alloc
import kotlinx.cinterop.convert
import kotlinx.cinterop.memScoped
import kotlinx.cinterop.ptr
import kotlinx.cinterop.reinterpret
import kotlinx.cinterop.sizeOf
import kotlinx.cinterop.toKString
import kotlinx.cinterop.usePinned
import platform.posix.AF_INET
import platform.posix.IPPROTO_UDP
import platform.posix.SO_BROADCAST
import platform.posix.SO_RCVTIMEO
import platform.posix.SOCK_DGRAM
import platform.posix.SOL_SOCKET
import platform.posix.close
import platform.posix.htonl
import platform.posix.htons
import platform.posix.inet_addr
import platform.posix.inet_ntoa
import platform.posix.ntohs
import platform.posix.recvfrom
import platform.posix.sendto
import platform.posix.setsockopt
import platform.posix.sockaddr_in
import platform.posix.socklen_tVar
import platform.posix.socket
import platform.posix.timeval
import platform.posix.memset

@OptIn(ExperimentalForeignApi::class)
actual class UdpSocket {
    private val fd: Int = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

    actual fun setBroadcast(enabled: Boolean) = memScoped {
        val opt = alloc<IntVar>()
        opt.value = if (enabled) 1 else 0
        setsockopt(fd, SOL_SOCKET, SO_BROADCAST, opt.ptr, sizeOf<IntVar>().convert())
    }

    actual fun setTimeout(ms: Int) = memScoped {
        val tv = alloc<timeval>()
        tv.tv_sec = (ms / 1000).convert()
        tv.tv_usec = ((ms % 1000) * 1000).convert()
        setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, tv.ptr, sizeOf<timeval>().convert())
    }

    actual fun send(data: ByteArray, address: String, port: Int) = memScoped {
        val addr = alloc<sockaddr_in>()
        memset(addr.ptr, 0, sizeOf<sockaddr_in>().convert())
        addr.sin_family = AF_INET.convert()
        addr.sin_port = htons(port.toUShort())
        addr.sin_addr.s_addr = inet_addr(address)
        data.usePinned { pinned ->
            sendto(fd, pinned.addressOf(0), data.size.convert(), 0,
                addr.ptr.reinterpret(), sizeOf<sockaddr_in>().convert())
        }
    }

    actual fun sendBroadcast(data: ByteArray, port: Int) {
        send(data, "255.255.255.255", port)
    }

    actual fun receive(bufferSize: Int): ReceivedPacket? {
        val buf = ByteArray(bufferSize)
        return memScoped {
            val fromAddr = alloc<sockaddr_in>()
            val fromLen = alloc<socklen_tVar>()
            fromLen.value = sizeOf<sockaddr_in>().convert()

            val received = buf.usePinned { pinned ->
                recvfrom(fd, pinned.addressOf(0), bufferSize.convert(), 0,
                    fromAddr.ptr.reinterpret(), fromLen.ptr)
            }

            if (received < 0) null
            else {
                val senderIp = inet_ntoa(fromAddr.sin_addr)?.toKString() ?: ""
                val senderPort = ntohs(fromAddr.sin_port).toInt()
                ReceivedPacket(buf, received.toInt(), senderIp, senderPort)
            }
        }
    }

    actual fun close() {
        platform.posix.close(fd)
    }
}
