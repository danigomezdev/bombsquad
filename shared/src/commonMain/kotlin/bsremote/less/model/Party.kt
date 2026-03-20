package bsremote.less.model

data class Party(
    val name: String,
    val address: String,
    val port: Int,
    val lastSeenMs: Long
)
