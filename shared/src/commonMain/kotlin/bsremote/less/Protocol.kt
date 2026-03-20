package bsremote.less

object Protocol {
    const val DISCOVERY_PORT = 43210

    const val PACKET_GAME_QUERY: Byte = 8
    const val PACKET_GAME_RESPONSE: Byte = 9

    const val MSG_ID_REQUEST: Byte = 2
    const val MSG_ID_RESPONSE: Byte = 3
    const val MSG_DISCONNECT: Byte = 4
    const val MSG_STATE: Byte = 5
    const val MSG_STATE_ACK: Byte = 6
    const val MSG_DISCONNECT_ACK: Byte = 7
    const val MSG_STATE2: Byte = 10

    // Sent in byte[4] of ID request to indicate V2 support
    const val REQUEST_PROTOCOL_VERSION = 50

    // Server responds with 100 in byte[2] when it supports V2
    const val RESPONSE_PROTOCOL_V2 = 100

    const val DISCONNECT_VERSION_MISMATCH = 0
    const val DISCONNECT_GAME_SHUTTING_DOWN = 1
    const val DISCONNECT_NOT_ACCEPTING = 2

    const val STATE_HISTORY_SIZE = 256
    const val MAX_STATES_PER_PACKET = 11

    const val KEEPALIVE_INTERVAL_MS = 3000L
    const val PROCESS_INTERVAL_MS = 100L
    const val SERVER_TIMEOUT_MS = 5000L
    const val SOCKET_TIMEOUT_MS = 500
}
