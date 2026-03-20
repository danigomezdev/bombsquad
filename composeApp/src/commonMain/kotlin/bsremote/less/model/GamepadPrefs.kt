package bsremote.less.model

import bsremote.less.AppPrefs

data class GamepadPrefs(
    val buttonScale: Float   = 1.0f,
    val buttonOffsetX: Float = 0f,
    val buttonOffsetY: Float = 0f,
    val dPadFixed: Boolean   = false,
    val dPadOffsetX: Float   = 0f,
    val dPadOffsetY: Float   = 0f
)

fun loadGamepadPrefs(): GamepadPrefs = GamepadPrefs(
    buttonScale   = AppPrefs.getFloat("buttonScale",   1.0f),
    buttonOffsetX = AppPrefs.getFloat("buttonOffsetX", 0f),
    buttonOffsetY = AppPrefs.getFloat("buttonOffsetY", 0f),
    dPadFixed     = AppPrefs.getBoolean("dPadFixed",   false),
    dPadOffsetX   = AppPrefs.getFloat("dPadOffsetX",   0f),
    dPadOffsetY   = AppPrefs.getFloat("dPadOffsetY",   0f)
)

fun saveGamepadPrefs(prefs: GamepadPrefs) {
    AppPrefs.putFloat("buttonScale",   prefs.buttonScale)
    AppPrefs.putFloat("buttonOffsetX", prefs.buttonOffsetX)
    AppPrefs.putFloat("buttonOffsetY", prefs.buttonOffsetY)
    AppPrefs.putBoolean("dPadFixed",   prefs.dPadFixed)
    AppPrefs.putFloat("dPadOffsetX",   prefs.dPadOffsetX)
    AppPrefs.putFloat("dPadOffsetY",   prefs.dPadOffsetY)
}
