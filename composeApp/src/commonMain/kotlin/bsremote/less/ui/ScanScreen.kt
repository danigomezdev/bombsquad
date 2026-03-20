package bsremote.less.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import bsremote.less.Language
import bsremote.less.LocalLanguage
import bsremote.less.Str
import bsremote.less.model.Party

private val BgColor       = Color(0xFF1A1A2E)
private val CardColor     = Color(0xFF16213E)
private val AccentColor   = Color(0xFF4CC9F0)
private val TextPrimary   = Color(0xFFEEEEEE)
private val TextSecondary = Color(0xFF888899)

@Composable
fun ScanScreen(
    parties: List<Party>,
    playerName: String,
    onPlayerNameChange: (String) -> Unit,
    onPartySelected: (Party) -> Unit,
    onManualConnect: (String, Int) -> Unit,
    onLanguageToggle: () -> Unit
) {
    val lang = LocalLanguage.current
    var showManualDialog by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(BgColor)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = Str.appTitle(lang),
                    color = AccentColor,
                    fontSize = 22.sp,
                    style = MaterialTheme.typography.headlineMedium,
                    modifier = Modifier.weight(1f)
                )
                // Language toggle button
                Button(
                    onClick = onLanguageToggle,
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2A2A4A)),
                    modifier = Modifier.padding(start = 8.dp)
                ) {
                    Text(
                        text = if (lang == Language.EN) "ES" else "EN",
                        color = AccentColor,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = playerName,
                onValueChange = { if (it.length <= 20) onPlayerNameChange(it) },
                label = { Text(Str.playerName(lang), color = TextSecondary) },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(onDone = {}),
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(20.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = Str.availableGames(lang),
                    color = TextPrimary,
                    fontSize = 16.sp,
                    modifier = Modifier.weight(1f)
                )
                if (parties.isEmpty()) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        color = AccentColor,
                        strokeWidth = 2.dp
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (parties.isEmpty()) {
                Text(
                    text = Str.searching(lang),
                    color = TextSecondary,
                    fontSize = 14.sp,
                    modifier = Modifier.padding(vertical = 8.dp)
                )
            }

            LazyColumn(modifier = Modifier.weight(1f)) {
                items(parties, key = { it.name }) { party ->
                    PartyItem(party = party, onClick = { onPartySelected(party) })
                    HorizontalDivider(color = Color(0xFF2A2A4A), thickness = 0.5.dp)
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Button(
                onClick = { showManualDialog = true },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(Str.connectByIp(lang))
            }
        }

        if (showManualDialog) {
            ManualConnectDialog(
                onConnect = { address, port ->
                    showManualDialog = false
                    onManualConnect(address, port)
                },
                onDismiss = { showManualDialog = false }
            )
        }
    }
}

@Composable
private fun PartyItem(party: Party, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .clickable(onClick = onClick)
            .background(CardColor)
            .padding(horizontal = 16.dp, vertical = 14.dp)
    ) {
        Column {
            Text(
                text = party.name,
                color = TextPrimary,
                fontSize = 16.sp,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = "${party.address}:${party.port}",
                color = TextSecondary,
                fontSize = 12.sp
            )
        }
    }
    Spacer(modifier = Modifier.height(4.dp))
}

@Composable
private fun ManualConnectDialog(
    onConnect: (String, Int) -> Unit,
    onDismiss: () -> Unit
) {
    val lang = LocalLanguage.current
    var address by remember { mutableStateOf("") }
    var port    by remember { mutableStateOf("43210") }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black.copy(alpha = 0.6f))
            .clickable(onClick = onDismiss),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth(0.85f)
                .clip(RoundedCornerShape(12.dp))
                .background(CardColor)
                .clickable(onClick = {})  // absorb clicks so they don't dismiss
                .padding(20.dp)
        ) {
            Text(Str.connectByIp(lang), color = TextPrimary, fontSize = 18.sp)
            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = address,
                onValueChange = { address = it },
                label = { Text(Str.ipAddress(lang), color = TextSecondary) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = port,
                onValueChange = { port = it },
                label = { Text(Str.port(lang), color = TextSecondary) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))

            Row {
                Button(onClick = onDismiss, modifier = Modifier.weight(1f)) {
                    Text(Str.cancel(lang))
                }
                Spacer(modifier = Modifier.size(8.dp))
                Button(
                    onClick = {
                        val portNum = port.toIntOrNull() ?: 43210
                        if (address.isNotBlank()) onConnect(address.trim(), portNum)
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Text(Str.connect(lang))
                }
            }
        }
    }
}
