# BombSquad Remote — Kotlin Multiplatform Port

This project is a Kotlin Multiplatform (KMP) port of the original BombSquad Remote app created by Eric Froemling, which was written in Java for Android only. The goal of this port is to bring the same remote controller experience to both Android and iOS from a single shared codebase, using modern Kotlin tooling and Compose Multiplatform.

---

## What It Does

BombSquad Remote connects to a running BombSquad game session over the local network via UDP. It displays a virtual gamepad (joystick and action buttons) and sends player input to the game in real time. The app supports both the original V1 protocol and the newer V2 protocol.

---

## Technology Stack

- **Kotlin Multiplatform (KMP)** — shared business logic and UI across Android and iOS
- **Compose Multiplatform** — single UI codebase rendered natively on both platforms
- **Kotlin Coroutines** — asynchronous UDP networking with `Dispatchers.IO`
- **StateFlow** — reactive state management from ViewModel to UI
- **AndroidX ViewModel** — lifecycle-aware state holder; `AndroidViewModel` on Android, plain `ViewModel` on iOS
- **Compose Resources** — shared image assets declared once in `commonMain`
- **SharedPreferences** (Android) / **NSUserDefaults** (iOS) — platform-specific settings storage, abstracted behind a common `AppPrefs` object

---

## Architecture

The project follows the `expect`/`actual` pattern from Kotlin Multiplatform to isolate platform-specific behavior while keeping all UI and business logic in `commonMain`.

### expect/actual classes

| Common (`expect`)   | Android (`actual`)                        | iOS (`actual`)                   |
|---------------------|-------------------------------------------|----------------------------------|
| `AppViewModel`      | `AndroidViewModel` + WifiMulticastLock    | plain `ViewModel`                |
| `AppPrefs`          | `SharedPreferences`                       | `NSUserDefaults`                 |
| `UdpSocket`         | Java `DatagramSocket`                     | POSIX sockets via Kotlin/Native  |

### Layers

- **Network layer** (`shared` module): `Scanner` discovers game sessions via UDP broadcast. `Connection` handles the persistent UDP connection, encodes `RemoteState` into the BombSquad wire protocol, and tracks latency.
- **ViewModel layer** (`composeApp`): `AppViewModel` owns `Scanner` and `Connection`, exposes `StateFlow`s to the UI, and manages the WifiMulticastLock on Android.
- **UI layer** (`composeApp`): Two screens — `ScanScreen` (party discovery, manual IP connect, player name, language toggle) and `GamepadScreen` (joystick + action buttons rendered on Canvas, settings overlay).

---

## Project Structure

```
bsremoteKMP/
  composeApp/
    src/
      commonMain/       # Shared UI and logic (Compose, ViewModel expect, AppPrefs expect)
        kotlin/
          bsremote/less/
            App.kt
            AppViewModel.kt       # expect class
            AppPrefs.kt           # expect object
            Language.kt
            model/
              GamepadPrefs.kt
            ui/
              ScanScreen.kt
              GamepadScreen.kt
        composeResources/
          drawable/               # Shared PNG assets (joystick, buttons)
      androidMain/      # Android-specific implementations
        kotlin/
          bsremote/less/
            AppViewModel.kt       # actual class (AndroidViewModel + WifiMulticastLock)
            AppPrefs.android.kt   # actual object (SharedPreferences)
            MainActivity.kt
      iosMain/          # iOS-specific implementations
        kotlin/
          bsremote/less/
            AppViewModel.ios.kt   # actual class (ViewModel)
            AppPrefs.ios.kt       # actual object (NSUserDefaults)
            MainViewController.kt # ComposeUIViewController entry point

  shared/
    src/
      commonMain/       # Network protocol, models, expect UdpSocket
        kotlin/
          bsremote/less/
            network/
              Scanner.kt
              Connection.kt
              UdpSocket.kt        # expect class
            model/
              Party.kt
              RemoteState.kt
            Protocol.kt
      androidMain/      # UdpSocket backed by DatagramSocket
      iosMain/          # UdpSocket backed by POSIX sockets

  iosApp/               # Xcode project — Swift entry point, Info.plist, app icon
```

---

## Network Protocol

BombSquad Remote communicates with the game using a custom UDP protocol over port 43210.

- **Discovery**: the app sends UDP broadcast packets on the local network and listens for responses from active game sessions.
- **V1 protocol**: 16-bit state encoding — joystick axes and button flags packed into two bytes.
- **V2 protocol**: 24-bit state encoding — adds an extra byte for additional button support.

The `Protocol.kt` file contains the encoding logic shared by both platforms.

---

## Building

### Android

```shell
./gradlew :composeApp:assembleDebug
```

### iOS

Open `iosApp/iosApp.xcodeproj` in Xcode. The build will automatically invoke Gradle to compile the `ComposeApp` framework via the `embedAndSignAppleFrameworkForXcode` task.

Requires Xcode 15+ and a Mac.

---

## Settings

The gamepad screen includes a settings overlay (gear icon, bottom-left) where the player can adjust:

- Action button scale
- Action button horizontal and vertical offset
- Joystick horizontal and vertical offset
- Joystick mode: floating (spawns under the finger) or fixed (stays centered)

Settings are persisted per-platform using `SharedPreferences` on Android and `NSUserDefaults` on iOS, accessed through the shared `AppPrefs` abstraction.

---

## Language

The app supports English and Spanish. The active language can be toggled from the scan screen and is persisted across sessions.
