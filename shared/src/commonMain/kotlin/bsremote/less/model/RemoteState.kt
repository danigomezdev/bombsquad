package bsremote.less.model

import kotlin.math.abs
import kotlin.math.min
import kotlin.math.roundToInt

data class RemoteState(
    val punch: Boolean = false,
    val jump: Boolean = false,
    val bomb: Boolean = false,
    val pickUp: Boolean = false,
    val menu: Boolean = false,
    val run: Boolean = false,
    val horizontal: Float = 0f,
    val vertical: Float = 0f
) {
    // V1 encodes as 16 bits: buttons (0-4), h-sign (5), h-mag (6-9), v-sign (10), v-mag (11-14)
    fun encodeV1(): Short {
        var s = 0
        if (punch) s = s or 1
        if (jump) s = s or (1 shl 1)
        if (pickUp) s = s or (1 shl 2)
        if (bomb) s = s or (1 shl 3)
        if (menu) s = s or (1 shl 4)

        val hAbs = min(1.0f, abs(horizontal))
        s = s or ((if (horizontal > 0f) 1 else 0) shl 5)
        s = s or ((hAbs * 15.0f).roundToInt() shl 6)

        val vAbs = min(1.0f, abs(vertical))
        s = s or ((if (vertical > 0f) 1 else 0) shl 10)
        s = s or ((vAbs * 15.0f).roundToInt() shl 11)

        return s.toShort()
    }

    // V2 encodes as 24 bits packed into an Int:
    // byte0 = buttons, byte1 = horizontal (0-255, 128=center), byte2 = vertical
    fun encodeV2(): Int {
        var buttons = 0
        if (menu) buttons = buttons or 1
        if (jump) buttons = buttons or (1 shl 1)
        if (punch) buttons = buttons or (1 shl 2)
        if (pickUp) buttons = buttons or (1 shl 3)
        if (bomb) buttons = buttons or (1 shl 4)
        if (run) buttons = buttons or (1 shl 5)

        val h = (256.0f * (0.5f + horizontal * 0.5f)).toInt().coerceIn(0, 255)
        val v = (256.0f * (0.5f + vertical * 0.5f)).toInt().coerceIn(0, 255)

        return buttons or (h shl 8) or (v shl 16)
    }
}
