# ba_meta require api 9

from __future__ import annotations

import random
import json
import os
import threading
import urllib.error
import urllib.request
import _babase
import babase
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

VERSION = "1.9"
UPDATE_URL = "https://raw.githubusercontent.com/danigomezdev/bombsquad/refs/heads/main/CheapDisco/CheapDisco.json"

_E = _babase.env()
_H = {"User-Agent": _E["legacy_user_agent_string"]}


def _fj():
    req = urllib.request.Request(UPDATE_URL, headers=_H)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _cv():
    try:
        d = _fj()
        rv = d.get("metadata", {}).get("version", "")
        ru = d.get("metadata", {}).get("url_raw_mod", "")
        return {"update_available": str(rv) != VERSION, "remote_version": str(rv), "url_raw_mod": ru}
    except Exception:
        return {"update_available": False, "remote_version": None, "url_raw_mod": ""}


def _sut(w, t, c):
    if w and w.exists():
        bui.textwidget(w, text=t, color=c)


class UpdateWindow(bui.Window):
    def __init__(s, start_check=True):
        w, h = 455, 180
        us = bui.app.ui_v1.uiscale
        sc = 1.8 if us is babase.UIScale.SMALL else 1.3 if us is babase.UIScale.MEDIUM else 0.9
        super().__init__(
            root_widget=bui.containerwidget(parent=bui.get_special_widget("overlay_stack"),
                size=(w, h), scale=sc, color=(0.4, 0.37, 0.49),
                stack_offset=(0, 0), on_outside_click_call=s.close),
            prevent_main_window_auto_recreate=False)
        s._updating = False
        lpm_installed = os.path.exists(os.path.join(_E["python_directory_user"], "LessPluginManager.py"))
        bui.textwidget(parent=s._root_widget, position=(w/2, h-26), size=(0,0),
            text="Updates", scale=0.85, color=(0.9,0.9,0.9), h_align="center", v_align="center", maxwidth=w-130 if not lpm_installed else w-40)
        bui.buttonwidget(parent=s._root_widget, position=(27, h-42), size=(36,36),
            label=babase.charstr(babase.SpecialChar.BACK), button_type="backSmall",
            color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s.close)
        if not lpm_installed:
            bui.buttonwidget(parent=s._root_widget, position=(w-161, h-38), size=(140,30),
                label="LessPluginManager", autoselect=True,
                color=(0.55, 0.35, 0.75), textcolor=(0.9, 0.85, 1.0),
                on_activate_call=s._show_lpm)
        bui.textwidget(parent=s._root_widget, position=(w/2, h-70), size=(0,0),
            text=f"Current: v{VERSION}", scale=0.72, color=(0.9,0.9,0.9),
            h_align="center", v_align="center", maxwidth=w-40)
        s._st = bui.textwidget(parent=s._root_widget, position=(w/2, h-100), size=(0,0),
            text="Checking...", scale=0.65, color=(0.5,0.5,0.5), h_align="center", v_align="center", maxwidth=w-40)
        s._ab = bui.buttonwidget(parent=s._root_widget, position=(w/2-50, 30), size=(100,34),
            label="Check", color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s._sc)
        if start_check: s._sc()

    def _show_lpm(s):
        w2, h2 = 360, 180
        sc2 = 1.3 if bui.app.ui_v1.uiscale is babase.UIScale.MEDIUM else 0.9
        r = bui.containerwidget(
            parent=bui.get_special_widget("overlay_stack"),
            size=(w2, h2), scale=sc2, color=(0.4, 0.37, 0.49),
            stack_offset=(0, 0),
            on_outside_click_call=lambda: r.delete(),
        )
        bui.textwidget(parent=r, position=(w2/2, h2-27), size=(0,0),
            text="LessPluginManager", scale=0.8, color=(0.9,0.9,0.9),
            h_align="center", v_align="center", maxwidth=w2-40)
        bui.buttonwidget(parent=r, position=(27, h2-43), size=(36,36),
            label=babase.charstr(babase.SpecialChar.BACK), button_type="backSmall",
            color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9),
            on_activate_call=lambda: r.delete())
        bui.textwidget(parent=r, position=(w2/2, h2-78), size=(0,0),
            text="Enhanced plugin manager with\nupdate buttons, mod downloads\nand category filters.",
            scale=0.55, color=(0.8,0.8,0.8),
            h_align="center", v_align="center", maxwidth=w2-30)
        s._lpm_st = bui.textwidget(parent=r, position=(w2/2, 65), size=(0,0),
            text="", scale=0.5, color=(0.5,0.5,0.5),
            h_align="center", v_align="center")
        bui.buttonwidget(parent=r, position=(w2/2-68, 18), size=(136, 40),
            label="Download v1.0", color=(0.25, 0.45, 0.75), textcolor=(1,1,1),
            on_activate_call=s._download_lpm)

    def _download_lpm(s):
        bui.textwidget(s._lpm_st, text="Downloading...", color=(0.5,0.5,1))
        threading.Thread(target=s._dl_lpm_thread, daemon=True).start()

    def _dl_lpm_thread(s):
        try:
            req = urllib.request.Request(
                "https://github.com/danigomezdev/bombsquad/raw/main/LessPluginManager/LessPluginManager.py",
                headers=_H)
            with urllib.request.urlopen(req, timeout=60) as resp: c = resp.read()
            mp = os.path.join(_E["python_directory_user"], "LessPluginManager.py")
            with open(mp, "wb") as f: f.write(c)
            s._lpm_done("Downloaded! Restart BombSquad.", (0,1,0))
        except Exception as e:
            s._lpm_done(f"Error: {e}", (1,0.5,0.5))

    def _lpm_done(s, t, c):
        babase.pushcall(lambda: _sut(s._lpm_st, t, c), from_other_thread=True)

    def close(s):
        if s._root_widget.exists(): s._root_widget.delete()
    def _sc(s):
        if s._updating: return
        bui.textwidget(s._st, text="Checking...", color=(0.5,0.5,0.5))
        bui.buttonwidget(s._ab, label="...", color=(0.4,0.4,0.4))
        threading.Thread(target=s._rc, daemon=True).start()
    def _rc(s):
        info = _cv(); r = info.get("remote_version")
        if info.get("update_available") and r:
            s._info = info
            babase.pushcall(s._sua, from_other_thread=True)
        elif r: babase.pushcall(s._su2d, from_other_thread=True)
        else: babase.pushcall(s._ser, from_other_thread=True)
    def _sua(s):
        rv = s._info.get("remote_version", "?")
        bui.textwidget(s._st, text=f"Latest: v{rv}", color=(0.3,0.9,0.3))
        bui.buttonwidget(s._ab, label="Update", color=(0.2,0.6,0.2), textcolor=(1,1,1), on_activate_call=s._du)
    def _su2d(s):
        bui.textwidget(s._st, text="You have the latest version.", color=(0.3,0.9,0.3))
        bui.buttonwidget(s._ab, label="OK", color=(0.2,0.6,0.2), textcolor=(1,1,1))
    def _ser(s):
        bui.textwidget(s._st, text="Could not check for updates.", color=(1,0.5,0.5))
        bui.buttonwidget(s._ab, label="Retry", color=(0.5,0.4,0.6), textcolor=(1,1,1))
    def _du(s):
        if s._updating: return
        s._updating = True
        bui.textwidget(s._st, text="Downloading...", color=(0.5,0.5,1))
        bui.buttonwidget(s._ab, label="...", color=(0.4,0.4,0.4))
        threading.Thread(target=s._rd, args=(s._info,), daemon=True).start()
    def _rd(s, info):
        url = info.get("url_raw_mod", "")
        if not url: return s._ss("No download URL.", (1,0.5,0.5))
        try:
            req = urllib.request.Request(url, headers=_H)
            with urllib.request.urlopen(req, timeout=60) as resp: c = resp.read()
            with open(os.path.join(_E["python_directory_user"], "CheapDisco.py"), "wb") as f: f.write(c)
            s._ss("Updated! Restart BombSquad.", (0,1,0))
        except Exception as e: s._ss(f"Error: {e}", (1,0.5,0.5))
    def _ss(s, t, c):
        babase.pushcall(lambda: _sut(s._st, t, c), from_other_thread=True)


# ba_meta export babase.Plugin
class byLess(bs.Plugin):
    def on_app_running(self) -> None: pass

    def has_settings_ui(self):
        return True

    def show_settings_ui(self, source_widget):
        DiscoSettingsWindow(source_widget)
