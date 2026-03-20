package bsremote.less

import android.content.Context
import androidx.compose.runtime.compositionLocalOf

enum class Language { EN, ES }

val LocalLanguage = compositionLocalOf { Language.EN }

fun Context.loadLanguage(): Language {
    val code = getSharedPreferences("BSRemotePrefs", Context.MODE_PRIVATE)
        .getString("language", "EN") ?: "EN"
    return if (code == "ES") Language.ES else Language.EN
}

fun Context.saveLanguage(lang: Language) {
    getSharedPreferences("BSRemotePrefs", Context.MODE_PRIVATE).edit()
        .putString("language", lang.name)
        .apply()
}

object Str {
    fun appTitle(l: Language)        = if (l == Language.ES) "BombSquad Remoto"          else "BombSquad Remote"
    fun playerName(l: Language)      = if (l == Language.ES) "Nombre de jugador"          else "Player name"
    fun availableGames(l: Language)  = if (l == Language.ES) "Juegos disponibles"         else "Available games"
    fun searching(l: Language)       = if (l == Language.ES) "Buscando en la red local\u2026" else "Searching on local network\u2026"
    fun connectByIp(l: Language)     = if (l == Language.ES) "Conectar por IP"            else "Connect by IP"
    fun ipAddress(l: Language)       = if (l == Language.ES) "Direcci\u00f3n IP"          else "IP address"
    fun port(l: Language)            = if (l == Language.ES) "Puerto"                     else "Port"
    fun cancel(l: Language)          = if (l == Language.ES) "Cancelar"                   else "Cancel"
    fun connect(l: Language)         = if (l == Language.ES) "Conectar"                   else "Connect"
    fun connecting(l: Language)      = if (l == Language.ES) "conectando\u2026"           else "connecting\u2026"
    fun lagMs(l: Language, ms: Long) = if (l == Language.ES) "retraso ${ms}ms"            else "lag ${ms}ms"
    fun settings(l: Language)        = if (l == Language.ES) "Ajustes"                    else "Settings"
    fun buttonSize(l: Language)      = if (l == Language.ES) "Tama\u00f1o botones"        else "Button size"
    fun buttonsLR(l: Language)       = if (l == Language.ES) "Botones izq / der"          else "Buttons left / right"
    fun buttonsUD(l: Language)       = if (l == Language.ES) "Botones arriba / abajo"     else "Buttons up / down"
    fun joystickLR(l: Language)      = if (l == Language.ES) "Joystick izq / der"         else "Joystick left / right"
    fun joystickUD(l: Language)      = if (l == Language.ES) "Joystick arriba / abajo"    else "Joystick up / down"
    fun joystickLabel(l: Language)   = if (l == Language.ES) "Joystick:"                  else "Joystick:"
    fun floating(l: Language)        = if (l == Language.ES) "Flotante"                   else "Floating"
    fun fixed(l: Language)           = if (l == Language.ES) "Fijo"                       else "Fixed"
    fun close(l: Language)           = if (l == Language.ES) "Cerrar"                     else "Close"
}
