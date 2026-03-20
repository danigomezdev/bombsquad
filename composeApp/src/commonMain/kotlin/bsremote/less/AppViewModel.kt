package bsremote.less

import androidx.lifecycle.ViewModel
import bsremote.less.model.Party
import bsremote.less.model.RemoteState
import bsremote.less.network.ConnectionInfo
import kotlinx.coroutines.flow.StateFlow

@Suppress("EXPECT_ACTUAL_CLASSIFIERS_ARE_IN_BETA_WARNING")
expect class AppViewModel : ViewModel {
    val parties: StateFlow<List<Party>>
    val connectionInfo: StateFlow<ConnectionInfo>
    var playerName: String
    fun connectTo(party: Party)
    fun connectToAddress(address: String, port: Int)
    fun disconnect()
    fun setRemoteState(state: RemoteState)
}
