package bsremote.less

import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.viewmodel.compose.viewModel
import bsremote.less.network.ConnectionStatus
import bsremote.less.ui.GamepadScreen
import bsremote.less.ui.ScanScreen

@Composable
fun App(vm: AppViewModel = viewModel<AppViewModel>()) {
    var language by remember { mutableStateOf(loadLanguage()) }

    val parties    by vm.parties.collectAsState()
    val connInfo   by vm.connectionInfo.collectAsState()
    var playerName by remember { mutableStateOf(vm.playerName) }

    val onScreen = when (connInfo.status) {
        ConnectionStatus.CONNECTED, ConnectionStatus.CONNECTING -> Screen.GAMEPAD
        else -> Screen.SCAN
    }

    CompositionLocalProvider(LocalLanguage provides language) {
        when (onScreen) {
            Screen.SCAN -> ScanScreen(
                parties = parties,
                playerName = playerName,
                onPlayerNameChange = { playerName = it; vm.playerName = it },
                onPartySelected = { vm.connectTo(it) },
                onManualConnect = { address, port -> vm.connectToAddress(address, port) },
                onLanguageToggle = {
                    language = if (language == Language.EN) Language.ES else Language.EN
                    saveLanguage(language)
                }
            )
            Screen.GAMEPAD -> GamepadScreen(
                lagMs = connInfo.lagMs,
                isV2 = connInfo.protocolV2,
                onStateChanged = { vm.setRemoteState(it) },
                onDisconnect = { vm.disconnect() }
            )
        }
    }
}

private enum class Screen { SCAN, GAMEPAD }
