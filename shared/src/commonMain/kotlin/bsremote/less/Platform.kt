package bsremote.less

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform