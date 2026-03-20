package bsremote.less.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Fill
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.input.pointer.PointerInputChange
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import bsremote.composeapp.generated.resources.Res
import bsremote.composeapp.generated.resources.button_bomb
import bsremote.composeapp.generated.resources.button_bomb_pressed
import bsremote.composeapp.generated.resources.button_jump
import bsremote.composeapp.generated.resources.button_jump_pressed
import bsremote.composeapp.generated.resources.button_leave
import bsremote.composeapp.generated.resources.button_punch
import bsremote.composeapp.generated.resources.button_punch_pressed
import bsremote.composeapp.generated.resources.button_start
import bsremote.composeapp.generated.resources.button_throw
import bsremote.composeapp.generated.resources.button_throw_pressed
import bsremote.composeapp.generated.resources.center
import bsremote.composeapp.generated.resources.thumb
import bsremote.composeapp.generated.resources.thumb_pressed
import bsremote.less.LocalLanguage
import bsremote.less.Str
import bsremote.less.model.GamepadPrefs
import bsremote.less.model.RemoteState
import bsremote.less.model.loadGamepadPrefs
import bsremote.less.model.saveGamepadPrefs

import org.jetbrains.compose.resources.painterResource
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

private const val BTN_JUMP  = 0
private const val BTN_PUNCH = 1
private const val BTN_BOMB  = 2
private const val BTN_THROW = 3
private const val BTN_MENU  = 4
private const val BTN_LEAVE = 5

private val GameBg     = Color(0xFF0D0D1A)
private val DialogCard = Color(0xFF1E1E32)
private val LabelColor = Color(0xFF888899)
private val IconColor  = Color(0x99FFFFFF)

private val PointerInputChange.isPress:   Boolean get() =  pressed && !previousPressed
private val PointerInputChange.isMove:    Boolean get() =  pressed &&  previousPressed
private val PointerInputChange.isRelease: Boolean get() = !pressed &&  previousPressed

@Composable
fun GamepadScreen(
    lagMs: Long,
    isV2: Boolean,
    onStateChanged: (RemoteState) -> Unit,
    onDisconnect: () -> Unit
) {
    val lang = LocalLanguage.current

    var prefs        by remember { mutableStateOf(loadGamepadPrefs()) }
    var showSettings by remember { mutableStateOf(false) }

    LaunchedEffect(prefs) { saveGamepadPrefs(prefs) }

    var joystickPointerId  by remember { mutableStateOf<Long?>(null) }
    var joystickCenter     by remember { mutableStateOf(Offset.Zero) }
    var joystickOffset     by remember { mutableStateOf(Offset.Zero) }
    var joyH               by remember { mutableStateOf(0f) }
    var joyV               by remember { mutableStateOf(0f) }
    var joystickCanvasSize by remember { mutableStateOf(Size.Zero) }

    val pointerButtons = remember { mutableStateMapOf<Long, Int>() }

    fun emitState() {
        val active = pointerButtons.values.toSet()
        onStateChanged(
            RemoteState(
                jump       = BTN_JUMP  in active,
                punch      = BTN_PUNCH in active,
                bomb       = BTN_BOMB  in active,
                pickUp     = BTN_THROW in active,
                menu       = BTN_MENU  in active,
                horizontal = joyH,
                vertical   = joyV
            )
        )
    }

    val density = LocalDensity.current

    val maxJoyRadiusPx = with(density) { 65.dp.toPx() }
    val basePx         = with(density) { 140.dp.toPx() }
    val knobPx         = with(density) { 70.dp.toPx() }
    val btnSpacingPx   = with(density) { 62.dp.toPx() }
    val btnSizePx      = with(density) { 130.dp.toPx() }
    val cornerBtnPx    = with(density) { 48.dp.toPx() }
    val clusterOffsetY = with(density) { 40.dp.toPx() }

    val effectiveBtnSpacing = btnSpacingPx * prefs.buttonScale
    val effectiveBtnSize    = btnSizePx    * prefs.buttonScale
    val btnOffsetXPx        = with(density) { prefs.buttonOffsetX.dp.toPx() }
    val btnOffsetYPx        = with(density) { prefs.buttonOffsetY.dp.toPx() }
    val dPadOffsetXPx       = with(density) { prefs.dPadOffsetX.dp.toPx() }
    val dPadOffsetYPx       = with(density) { prefs.dPadOffsetY.dp.toPx() }

    val pCenter = painterResource(Res.drawable.center)
    val pThumb  = painterResource(Res.drawable.thumb)
    val pThumbP = painterResource(Res.drawable.thumb_pressed)
    val pJump   = painterResource(Res.drawable.button_jump)
    val pJumpP  = painterResource(Res.drawable.button_jump_pressed)
    val pPunch  = painterResource(Res.drawable.button_punch)
    val pPunchP = painterResource(Res.drawable.button_punch_pressed)
    val pBomb   = painterResource(Res.drawable.button_bomb)
    val pBombP  = painterResource(Res.drawable.button_bomb_pressed)
    val pThrow  = painterResource(Res.drawable.button_throw)
    val pThrowP = painterResource(Res.drawable.button_throw_pressed)
    val pMenu   = painterResource(Res.drawable.button_start)
    val pLeave  = painterResource(Res.drawable.button_leave)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(GameBg)
    ) {
        Row(modifier = Modifier.fillMaxSize()) {

            // Left panel: joystick
            Canvas(
                modifier = Modifier
                    .weight(0.45f)
                    .fillMaxHeight()
                    .pointerInput(maxJoyRadiusPx, prefs.dPadFixed, dPadOffsetXPx, dPadOffsetYPx, showSettings) {
                        if (showSettings) return@pointerInput
                        awaitPointerEventScope {
                            while (true) {
                                val event = awaitPointerEvent()
                                for (ch in event.changes) {
                                    val pid = ch.id.value
                                    when {
                                        ch.isPress -> {
                                            if (joystickPointerId == null) {
                                                joystickPointerId = pid
                                                joystickCenter = if (prefs.dPadFixed) {
                                                    Offset(
                                                        joystickCanvasSize.width  / 2f + dPadOffsetXPx,
                                                        joystickCanvasSize.height * 0.6f + dPadOffsetYPx
                                                    )
                                                } else {
                                                    ch.position
                                                }
                                                joystickOffset = Offset.Zero
                                                joyH = 0f; joyV = 0f
                                                emitState()
                                            }
                                            ch.consume()
                                        }
                                        ch.isMove && pid == joystickPointerId -> {
                                            val d = ch.position - joystickCenter
                                            var xVal = d.x / maxJoyRadiusPx
                                            var yVal = d.y / maxJoyRadiusPx
                                            if      (xVal >  1f) { val m =  1f / xVal; xVal =  1f; yVal *= m }
                                            else if (xVal < -1f) { val m = -1f / xVal; xVal = -1f; yVal *= m }
                                            if      (yVal >  1f) { val m =  1f / yVal; xVal *= m; yVal =  1f }
                                            else if (yVal < -1f) { val m = -1f / yVal; xVal *= m; yVal = -1f }
                                            joystickOffset = Offset(xVal * maxJoyRadiusPx, yVal * maxJoyRadiusPx)
                                            joyH = xVal
                                            joyV = yVal
                                            emitState()
                                            ch.consume()
                                        }
                                        ch.isRelease && pid == joystickPointerId -> {
                                            joystickPointerId = null
                                            joystickOffset = Offset.Zero
                                            joyH = 0f; joyV = 0f
                                            emitState()
                                            ch.consume()
                                        }
                                    }
                                }
                            }
                        }
                    }
            ) {
                joystickCanvasSize = size

                val isActive      = joystickPointerId != null
                val defaultCenter = Offset(size.width / 2f + dPadOffsetXPx, size.height * 0.6f + dPadOffsetYPx)
                val baseCenter    = if (isActive) joystickCenter else defaultCenter

                translate(baseCenter.x - basePx / 2, baseCenter.y - basePx / 2) {
                    with(pCenter) { draw(Size(basePx, basePx)) }
                }
                val knobCenter = baseCenter + joystickOffset
                translate(knobCenter.x - knobPx / 2, knobCenter.y - knobPx / 2) {
                    with(if (isActive) pThumbP else pThumb) { draw(Size(knobPx, knobPx)) }
                }
            }

            // Right panel: action buttons
            Canvas(
                modifier = Modifier
                    .weight(0.55f)
                    .fillMaxHeight()
                    .pointerInput(effectiveBtnSpacing, effectiveBtnSize, cornerBtnPx, clusterOffsetY, btnOffsetXPx, btnOffsetYPx, showSettings) {
                        if (showSettings) return@pointerInput
                        awaitPointerEventScope {
                            while (true) {
                                val event = awaitPointerEvent()
                                for (ch in event.changes) {
                                    val pid = ch.id.value
                                    when {
                                        ch.isPress || ch.isMove -> {
                                            val btn = hitTest(
                                                ch.position,
                                                size.width.toFloat(), size.height.toFloat(),
                                                effectiveBtnSpacing, effectiveBtnSize, cornerBtnPx,
                                                clusterOffsetY, btnOffsetXPx, btnOffsetYPx
                                            )
                                            if (btn == BTN_LEAVE && ch.isPress) {
                                                onDisconnect()
                                            } else {
                                                pointerButtons[pid] = btn
                                            }
                                            ch.consume()
                                        }
                                        ch.isRelease -> {
                                            pointerButtons.remove(pid)
                                            ch.consume()
                                        }
                                    }
                                }
                                emitState()
                            }
                        }
                    }
            ) {
                val active = pointerButtons.values.toSet()
                val cx = size.width  / 2f + btnOffsetXPx
                val cy = size.height / 2f + clusterOffsetY + btnOffsetYPx

                fun drawBtn(
                    idx: Int, c: Offset,
                    normal:  androidx.compose.ui.graphics.painter.Painter,
                    pressed: androidx.compose.ui.graphics.painter.Painter
                ) {
                    translate(c.x - effectiveBtnSize / 2, c.y - effectiveBtnSize / 2) {
                        with(if (idx in active) pressed else normal) { draw(Size(effectiveBtnSize, effectiveBtnSize)) }
                    }
                }

                drawBtn(BTN_THROW, Offset(cx,                      cy - effectiveBtnSpacing), pThrow, pThrowP)
                drawBtn(BTN_PUNCH, Offset(cx - effectiveBtnSpacing, cy),                       pPunch, pPunchP)
                drawBtn(BTN_BOMB,  Offset(cx + effectiveBtnSpacing, cy),                       pBomb,  pBombP)
                drawBtn(BTN_JUMP,  Offset(cx,                      cy + effectiveBtnSpacing), pJump,  pJumpP)

                val menuX = size.width  - cornerBtnPx * 0.9f
                val menuY = size.height - cornerBtnPx * 0.9f
                translate(menuX - cornerBtnPx / 2, menuY - cornerBtnPx / 2) {
                    with(pMenu) { draw(Size(cornerBtnPx, cornerBtnPx)) }
                }
                translate(10f, 10f) {
                    with(pLeave) { draw(Size(cornerBtnPx, cornerBtnPx)) }
                }
            }
        }

        // Lag indicator
        if (lagMs >= 0) {
            val lagColor = when {
                lagMs == 0L -> Color(0xFF66FF88)
                lagMs < 80  -> Color(0xFF66FF88)
                lagMs < 200 -> Color(0xFFFFE066)
                lagMs < 400 -> Color(0xFFFF9933)
                else        -> Color(0xFFFF4444)
            }
            Text(
                text = if (lagMs == 0L) Str.connecting(lang) else Str.lagMs(lang, lagMs),
                color = lagColor,
                fontSize = 11.sp,
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(bottom = 6.dp)
            )
        }

        // Settings gear icon — bottom-left of joystick area
        Canvas(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(start = 8.dp, bottom = 8.dp)
                .size(34.dp)
                .clickable(
                    indication = null,
                    interactionSource = remember { MutableInteractionSource() }
                ) { showSettings = true }
        ) {
            drawGearIcon(Offset(size.width / 2, size.height / 2), size.width * 0.9f, IconColor)
        }

        // Settings overlay
        if (showSettings) {
            SettingsDialog(
                prefs = prefs,
                onPrefsChanged = { prefs = it },
                onDismiss = { showSettings = false }
            )
        }
    }
}

@Composable
private fun SettingsDialog(
    prefs: GamepadPrefs,
    onPrefsChanged: (GamepadPrefs) -> Unit,
    onDismiss: () -> Unit
) {
    val lang = LocalLanguage.current

    // Two-layer approach: background handles click-outside, card absorbs its own clicks
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xCC000000))
            .clickable(
                indication = null,
                interactionSource = remember { MutableInteractionSource() }
            ) { onDismiss() },
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .width(420.dp)
                .background(DialogCard, RoundedCornerShape(14.dp))
                // absorb clicks so they don't propagate to the dismissing background
                .clickable(
                    indication = null,
                    interactionSource = remember { MutableInteractionSource() }
                ) {}
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp, vertical = 20.dp)
        ) {
            Text(Str.settings(lang), color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)

            Spacer(Modifier.height(16.dp))

            PrefSlider(
                label   = Str.buttonSize(lang),
                value   = prefs.buttonScale,
                min     = 0.5f, max = 2.0f,
                display = { "${(it * 100).toInt()}%" }
            ) { onPrefsChanged(prefs.copy(buttonScale = it)) }

            PrefSlider(
                label   = Str.buttonsLR(lang),
                value   = prefs.buttonOffsetX,
                min     = -150f, max = 150f,
                display = { "${it.toInt()} dp" }
            ) { onPrefsChanged(prefs.copy(buttonOffsetX = it)) }

            PrefSlider(
                label   = Str.buttonsUD(lang),
                value   = prefs.buttonOffsetY,
                min     = -150f, max = 150f,
                display = { "${it.toInt()} dp" }
            ) { onPrefsChanged(prefs.copy(buttonOffsetY = it)) }

            Spacer(Modifier.height(4.dp))

            PrefSlider(
                label   = Str.joystickLR(lang),
                value   = prefs.dPadOffsetX,
                min     = -150f, max = 150f,
                display = { "${it.toInt()} dp" }
            ) { onPrefsChanged(prefs.copy(dPadOffsetX = it)) }

            PrefSlider(
                label   = Str.joystickUD(lang),
                value   = prefs.dPadOffsetY,
                min     = -150f, max = 150f,
                display = { "${it.toInt()} dp" }
            ) { onPrefsChanged(prefs.copy(dPadOffsetY = it)) }

            Spacer(Modifier.height(8.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(Str.joystickLabel(lang), color = LabelColor, fontSize = 13.sp)
                Spacer(Modifier.width(8.dp))
                RadioButton(selected = !prefs.dPadFixed, onClick = { onPrefsChanged(prefs.copy(dPadFixed = false)) })
                Text(Str.floating(lang), color = Color.White, fontSize = 13.sp)
                Spacer(Modifier.width(12.dp))
                RadioButton(selected = prefs.dPadFixed, onClick = { onPrefsChanged(prefs.copy(dPadFixed = true)) })
                Text(Str.fixed(lang), color = Color.White, fontSize = 13.sp)
            }

            Spacer(Modifier.height(20.dp))

            Button(
                onClick = onDismiss,
                modifier = Modifier.align(Alignment.CenterHorizontally),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF3A3A5A))
            ) {
                Text(Str.close(lang), color = Color.White)
            }
        }
    }
}

@Composable
private fun PrefSlider(
    label: String,
    value: Float,
    min: Float,
    max: Float,
    display: (Float) -> String,
    onChange: (Float) -> Unit
) {
    Column(modifier = Modifier.padding(bottom = 2.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(label, color = LabelColor, fontSize = 12.sp)
            Text(display(value), color = Color.White, fontSize = 12.sp)
        }
        Slider(value = value, onValueChange = onChange, valueRange = min..max, modifier = Modifier.fillMaxWidth())
    }
}

// Gear icon drawn with path operations
private fun DrawScope.drawGearIcon(center: Offset, size: Float, color: Color) {
    val numTeeth  = 8
    val outerR    = size * 0.50f
    val innerR    = size * 0.36f
    val holeR     = size * 0.18f
    val toothAngle = (PI / numTeeth * 0.55).toFloat()

    val path = Path()
    for (i in 0 until numTeeth * 2) {
        val angle = (i * PI / numTeeth).toFloat()
        val r     = if (i % 2 == 0) outerR else innerR
        val x     = center.x + cos(angle) * r
        val y     = center.y + sin(angle) * r
        if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
    }
    path.close()
    drawPath(path, color, style = Fill)

    // hollow center
    drawCircle(color = GameBg, radius = holeR, center = center)
}

private fun hitTest(
    pos: Offset,
    w: Float, h: Float,
    spacing: Float,
    btnSize: Float,
    cornerSize: Float,
    clusterOffsetY: Float,
    btnOffsetX: Float = 0f,
    btnOffsetY: Float = 0f
): Int {
    val cornerR = cornerSize * 0.9f
    if ((pos - Offset(w - cornerSize * 0.9f, h - cornerSize * 0.9f)).length() < cornerR) return BTN_MENU
    if ((pos - Offset(cornerSize / 2 + 10f,  cornerSize / 2 + 10f)).length()  < cornerR) return BTN_LEAVE

    val cx = w / 2f + btnOffsetX
    val cy = h / 2f + clusterOffsetY + btnOffsetY
    val actionButtons = listOf(
        BTN_THROW to Offset(cx,           cy - spacing),
        BTN_PUNCH to Offset(cx - spacing, cy),
        BTN_BOMB  to Offset(cx + spacing, cy),
        BTN_JUMP  to Offset(cx,           cy + spacing)
    )
    return actionButtons.minByOrNull { (_, c) -> (pos - c).length() }?.first ?: -1
}

private fun Offset.length(): Float = sqrt(x * x + y * y)
