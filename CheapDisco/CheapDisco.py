# ba_meta require api 9
# ba_meta name Cheap Disco
# ba_meta description A mod that changes the background color of the Bombsquad MainMenu, using random dark colors
# ba_meta version 1.0.1

from __future__ import annotations

import random
import babase as ba
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib.popup import PopupWindow
from bauiv1lib.config import ConfigNumberEdit
from bascenev1lib.mainmenu import MainMenuActivity

def disco():
    activity = bs.get_foreground_host_activity()

    if (isinstance(activity, MainMenuActivity) and
        ba.app.config.get('Disco Settings', {}).get('Mainmenu', True)) or (
        isinstance(activity, bs.GameActivity) and 
        ba.app.config.get('Disco Settings', {}).get('In-Game', True)):

        R = random.uniform(0.0, 0.5)
        G = random.uniform(0.0, 0.5)
        B = random.uniform(0.0, 0.5)

        bs.get_foreground_host_activity().globalsnode.tint = (R, G, B)


class ConfigNumberEditDup(ConfigNumberEdit):
    def _up(self) -> None:
        self._value = min(self._maxval, self._value + self._increment)
        global abc
        abc = ba.AppTimer(self._value, disco, repeat=True)
        self._changed()

    def _down(self) -> None:
        self._value = max(self._minval, self._value - self._increment)
        global abc
        abc = ba.AppTimer(self._value, disco, repeat=True)
        self._changed()


class DiscoSettingsWindow(PopupWindow):
    def __init__(self, origin_widget):
        self.scale_origin = origin_widget.get_screen_space_center()
        bui.getsound('swish').play()
        _uiscale = bui.app.ui_v1.uiscale
        s = 1.65 if _uiscale is ba.UIScale.SMALL else 1.39 if _uiscale is ba.UIScale.MEDIUM else 1.67
        width = 400 * s
        height = width * 0.5
        text_scale = 0.7 * s
        self._transition_out = 'out_scale'
        transition = 'in_scale'

        self._root_widget = bui.containerwidget(
            size=(width, height),
            on_outside_click_call=self._back,
            transition=transition,
            scale=(1.5 if _uiscale is ba.UIScale.SMALL else 1.5
                    if _uiscale is ba.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin)

        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, height * 0.87),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=(
                'Rave Settings' if bui.app.config.get('Lang', None) == 'Gibberish'
                else 'Disco Settings'
            ),
            scale=text_scale * 1.25,
            color=bui.app.ui_v1.title_color,
            maxwidth=width * 0.9)

        back_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width * 0.1, height * 0.8),
            size=(60, 60),
            scale=0.8,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)

        bui.containerwidget(edit=self._root_widget, cancel_button=back_button)

        self._mainmenu_checkbox = bui.checkboxwidget(
            parent=self._root_widget,
            position=(width * 0.25, height * 0.6),
            size=(100, 30),
            autoselect=True,
            maxwidth=430,
            textcolor=(0.8, 0.8, 0.8),
            scale=text_scale,
            value=ba.app.config.get('Disco Settings', {}).get('Mainmenu', True),
            text=bui.Lstr(value=(
                'Mainmenu Rave' if bui.app.config.get('Lang', None) == 'Gibberish' else
                'Disco in Mainmenu'
            )),
            on_value_change_call=bui.WeakCall(
                self._on_disco_mainmenu_value_change
            ),
        )
        self._ingame_checkbox = bui.checkboxwidget(
            parent=self._root_widget,
            position=(width * 0.25, height * 0.4),
            size=(100, 30),
            autoselect=True,
            maxwidth=430,
            textcolor=(0.8, 0.8, 0.8),
            scale=text_scale,
            value=ba.app.config.get('Disco Settings', {}).get('In-Game', True),
            text=bui.Lstr(value=(
                'GamePlay Rave' if bui.app.config.get('Lang', None) == 'Gibberish' else
                'Disco in GamePlay'
            )),
            on_value_change_call=bui.WeakCall(
                self._on_disco_ingame_value_change
            ),
        )

        self._disco_timer = ConfigNumberEditDup(
            parent=self._root_widget,
            position=(
                width * (0.25 if _uiscale is ba.UIScale.MEDIUM else 0.28),
                height * 0.2
            ),
            configkey='Disco Color Time',
            displayname=bui.Lstr(value=''),
            minval=0.1,
            maxval=60.0,
            increment=0.1,
            fallback_value=1.0,
            textscale=text_scale
        )
        self._disco_timer.nametext = bui.textwidget(
            parent=self._root_widget,
            position=(
                width * (0.20 if _uiscale is ba.UIScale.MEDIUM else 0.26),
                height * 0.2
            ),
            size=(100, 30),
            text=bui.Lstr(value=(
                'Rave Timer:' if bui.app.config.get('Lang', None) == 'Gibberish' else
                'Disco Color Time:'
            )),
            color=(0.8, 0.8, 0.8, 1.0),
            h_align='center',
            v_align='center',
            scale=text_scale,
        )
        bui.textwidget(
            edit=self._disco_timer.valuetext,
            position=(
                width * (
                    0.20 if _uiscale is ba.UIScale.MEDIUM else 0.26
                ) + 155,
                height * 0.2
            )
        )
        bui.buttonwidget(
            edit=self._disco_timer.minusbutton,
            position=(
                width * (
                    0.20 if _uiscale is ba.UIScale.MEDIUM else 0.26
                ) + 230,
                height * 0.2
            )
        )
        bui.buttonwidget(
            edit=self._disco_timer.plusbutton,
            position=(
                width * (
                    0.20 if _uiscale is ba.UIScale.MEDIUM else 0.26
                ) + 280,
                height * 0.2
            )
        )


    def _on_disco_mainmenu_value_change(self, val: bool) -> None:
        cfg = bui.app.config
        if cfg.get('Disco Settings', {}) == {}:
            cfg['Disco Settings'] = {}
        cfg['Disco Settings']['Mainmenu'] = val
        cfg.apply_and_commit()
        if not val and isinstance(bs.get_foreground_host_activity(), MainMenuActivity):
            bs.get_foreground_host_activity().globalsnode.tint = (1, 1, 1)

    def _on_disco_ingame_value_change(self, val: bool) -> None:
        cfg = bui.app.config
        if cfg.get('Disco Settings', {}) == {}:
            cfg['Disco Settings'] = {}
        cfg['Disco Settings']['In-Game'] = val
        cfg.apply_and_commit()
        if not val and isinstance(bs.get_foreground_host_activity(), bs.GameActivity):
            bs.get_foreground_host_activity().globalsnode.tint = (1, 1, 1)

    def _back(self) -> None:
        bui.getsound('swish').play()
        bui.containerwidget(edit=self._root_widget, transition='out_scale')


abc = ba.AppTimer(ba.app.config.get('Disco Color Time', 1.0), disco, repeat=True)

# ba_meta export babase.Plugin
class byLess(bs.Plugin):
    def on_app_running(self) -> None: pass

    def has_settings_ui(self):
        return True

    def show_settings_ui(self, source_widget):
        DiscoSettingsWindow(source_widget)
