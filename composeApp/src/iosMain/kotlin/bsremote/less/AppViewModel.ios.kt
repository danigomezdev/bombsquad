package bsremote.less

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import bsremote.less.model.Party
import bsremote.less.model.RemoteState
import bsremote.less.network.Connection
import bsremote.less.network.ConnectionInfo
import bsremote.less.network.Scanner
import kotlinx.coroutines.flow.StateFlow
import kotlin.random.Random

@Suppress("EXPECT_ACTUAL_CLASSIFIERS_ARE_IN_BETA_WARNING")
actual class AppViewModel : ViewModel() {
    private val scanner    = Scanner()
    private val connection = Connection()

    actual val parties: StateFlow<List<Party>>           = scanner.parties
    actual val connectionInfo: StateFlow<ConnectionInfo> = connection.info

    actual var playerName: String = "Player"
    private val uniqueId: Int = Random.nextInt(1, 65535)

    init {
        scanner.start(viewModelScope)
    }

    actual fun connectTo(party: Party) {
        scanner.stop()
        connection.connect(party.address, party.port, playerName, uniqueId, viewModelScope)
    }

    actual fun connectToAddress(address: String, port: Int) {
        scanner.stop()
        connection.connect(address, port, playerName, uniqueId, viewModelScope)
    }

    actual fun disconnect() {
        connection.disconnect()
        scanner.start(viewModelScope)
    }

    actual fun setRemoteState(state: RemoteState) {
        connection.setState(state)
    }

    override fun onCleared() {
        scanner.stop()
        connection.disconnect()
    }
}
