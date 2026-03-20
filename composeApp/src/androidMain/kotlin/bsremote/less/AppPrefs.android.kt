package bsremote.less

import android.content.Context
import android.content.SharedPreferences

@Suppress("EXPECT_ACTUAL_CLASSIFIERS_ARE_IN_BETA_WARNING")
actual object AppPrefs {
    private lateinit var prefs: SharedPreferences

    fun init(context: Context) {
        prefs = context.getSharedPreferences("BSRemotePrefs", Context.MODE_PRIVATE)
    }

    actual fun getFloat(key: String, default: Float)      = prefs.getFloat(key, default)
    actual fun putFloat(key: String, value: Float)        { prefs.edit().putFloat(key, value).apply() }
    actual fun getBoolean(key: String, default: Boolean)  = prefs.getBoolean(key, default)
    actual fun putBoolean(key: String, value: Boolean)    { prefs.edit().putBoolean(key, value).apply() }
    actual fun getString(key: String, default: String)    = prefs.getString(key, default) ?: default
    actual fun putString(key: String, value: String)      { prefs.edit().putString(key, value).apply() }
}
