package bsremote.less.model

import android.content.Context

private const val PREFS_NAME = "BSRemotePrefs"

data class GamepadPrefs(
    val buttonScale: Float   = 1.0f,
    val buttonOffsetX: Float = 0f,
    val buttonOffsetY: Float = 0f,
    val dPadFixed: Boolean   = false,
    val dPadOffsetX: Float   = 0f,
    val dPadOffsetY: Float   = 0f
)

fun Context.loadGamepadPrefs(): GamepadPrefs {
    val p = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    return GamepadPrefs(
        buttonScale   = p.getFloat("buttonScale",   1.0f),
        buttonOffsetX = p.getFloat("buttonOffsetX", 0f),
        buttonOffsetY = p.getFloat("buttonOffsetY", 0f),
        dPadFixed     = p.getBoolean("dPadFixed",   false),
        dPadOffsetX   = p.getFloat("dPadOffsetX",   0f),
        dPadOffsetY   = p.getFloat("dPadOffsetY",   0f)
    )
}

fun Context.saveGamepadPrefs(prefs: GamepadPrefs) {
    getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE).edit()
        .putFloat("buttonScale",   prefs.buttonScale)
        .putFloat("buttonOffsetX", prefs.buttonOffsetX)
        .putFloat("buttonOffsetY", prefs.buttonOffsetY)
        .putBoolean("dPadFixed",   prefs.dPadFixed)
        .putFloat("dPadOffsetX",   prefs.dPadOffsetX)
        .putFloat("dPadOffsetY",   prefs.dPadOffsetY)
        .apply()
}
