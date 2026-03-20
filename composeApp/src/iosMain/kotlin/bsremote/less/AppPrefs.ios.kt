package bsremote.less

import platform.Foundation.NSUserDefaults

@Suppress("EXPECT_ACTUAL_CLASSIFIERS_ARE_IN_BETA_WARNING")
actual object AppPrefs {
    private val defaults = NSUserDefaults.standardUserDefaults

    actual fun getFloat(key: String, default: Float): Float =
        if (defaults.objectForKey(key) != null) defaults.floatForKey(key) else default

    actual fun putFloat(key: String, value: Float) =
        defaults.setFloat(value, forKey = key)

    actual fun getBoolean(key: String, default: Boolean): Boolean =
        if (defaults.objectForKey(key) != null) defaults.boolForKey(key) else default

    actual fun putBoolean(key: String, value: Boolean) =
        defaults.setBool(value, forKey = key)

    actual fun getString(key: String, default: String): String =
        defaults.stringForKey(key) ?: default

    actual fun putString(key: String, value: String) =
        defaults.setObject(value, forKey = key)
}
