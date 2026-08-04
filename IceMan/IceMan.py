# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bauiv1
import bauiv1 as bui
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spaz import Spaz, PunchHitMessage
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.actor.spazbot import SpazBot
from bascenev1lib.actor.bomb import BombFactory
from bauiv1lib import popup
import bascenev1
import json, os, threading
import urllib.error, urllib.request
import _babase

if TYPE_CHECKING:
    from typing import Any, Sequence

class ModLang:
    lang = babase.app.lang.language
    if lang == 'Spanish':
        title = 'Opciones del Mod'
        enable = 'Habilitar Mod'
        ice_bomb = 'Bombas de Hielo'
        ice_punch = 'Golpes Congelantes'
        ice_effect = 'Efectos de Hielo'
        ice_inmunity = 'Inmunidad a la Congelación'
    elif lang == 'Chinese':
        title = '模组选项'
        enable = '启用模组'
        ice_bomb = '冰弹'
        ice_punch = '冰拳'
        ice_effect = '冰效果'
        ice_inmunity = '冻结免疫'
    else:
        title = 'Mod Settings'
        enable = 'Enable Mod'
        ice_bomb = 'Ice Bombs'
        ice_punch = 'Icy Punches'
        ice_effect = 'Ice Effects'
        ice_inmunity = 'Freeze Immunity'


class ModSettingsPopup(popup.PopupWindow):

    def __init__(self):
        uiscale = babase.UIScale
        self._transitioning_out = False
        self._width = 480
        self._height = 380
        bg_color = (0.4, 0.37, 0.49)

        # creates our _root_widget
        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(
                2.06
                if uiscale is babase.UIScale.SMALL
                else 1.4
                if uiscale is babase.UIScale.MEDIUM
                else 1.0
            ),
            bg_color=bg_color)

        self._cancel_button = bauiv1.buttonwidget(
            parent=self.root_widget,
            position=(34, self._height - 48),
            size=(50, 50),
            scale=0.7,
            label='',
            color=bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bauiv1.gettexture('crossOut'),
            iconscale=1.2)
        bauiv1.containerwidget(edit=self.root_widget,
                           cancel_button=self._cancel_button)

        title = bauiv1.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.49, self._height - 27 - 5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.0,
            text=ModLang.title,
            maxwidth=self._width * 0.6,
            color=(0, 1, 0))

        checkbox_size = (self._width * 0.7, 50)
        checkbox_maxwidth = 250
        checkbox_space = 56
        v = -186
        bauiv1.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.155, self._height * 0.2 - v),
            size=checkbox_size,
            autoselect=True,
            maxwidth=checkbox_maxwidth,
            scale=1.0,
            textcolor=(0.8, 0.8, 0.8),
            value=babase.app.config['Iceman']['enable mod'],
            text=ModLang.enable,
            on_value_change_call=self._set_enable,
        )
        v += checkbox_space
        bauiv1.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.155, self._height * 0.2 - v),
            size=checkbox_size,
            autoselect=True,
            maxwidth=checkbox_maxwidth,
            scale=1.0,
            textcolor=(0.8, 0.8, 0.8),
            value=babase.app.config['Iceman']['ice punch'],
            text=ModLang.ice_punch,
            on_value_change_call=self.ice_punch,
        )
        v += checkbox_space
        bauiv1.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.155, self._height * 0.2 - v),
            size=checkbox_size,
            autoselect=True,
            maxwidth=checkbox_maxwidth,
            scale=1.0,
            textcolor=(0.8, 0.8, 0.8),
            value=babase.app.config['Iceman']['ice effect'],
            text=ModLang.ice_effect,
            on_value_change_call=self.ice_effect,
        )
        v += checkbox_space
        bauiv1.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.155, self._height * 0.2 - v),
            size=checkbox_size,
            autoselect=True,
            maxwidth=checkbox_maxwidth,
            scale=1.0,
            textcolor=(0.8, 0.8, 0.8),
            value=babase.app.config['Iceman']['ice immunity'],
            text=ModLang.ice_inmunity,
            on_value_change_call=self.ice_inmunity,
        )
        v += checkbox_space
        bauiv1.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.155, self._height * 0.2 - v),
            size=checkbox_size,
            autoselect=True,
            maxwidth=checkbox_maxwidth,
            scale=1.0,
            textcolor=(0.8, 0.8, 0.8),
            value=babase.app.config['Iceman']['ice bomb'],
            text=ModLang.ice_bomb,
            on_value_change_call=self.ice_bomb,
        )

    def ice_bomb(self, val: bool) -> None:
        cfg = babase.app.config
        cfg['Iceman']['ice bomb'] = val
        cfg.apply_and_commit()

    def ice_punch(self, val: bool) -> None:
        cfg = babase.app.config
        cfg['Iceman']['ice punch'] = val
        cfg.apply_and_commit()

    def ice_effect(self, val: bool) -> None:
        cfg = babase.app.config
        cfg['Iceman']['ice effect'] = val
        cfg.apply_and_commit()

    def ice_inmunity(self, val: bool) -> None:
        cfg = babase.app.config
        cfg['Iceman']['ice immunity'] = val
        cfg.apply_and_commit()

    def _set_enable(self, val: bool) -> None:
        cfg = babase.app.config
        cfg['Iceman']['enable mod'] = val
        cfg.apply_and_commit()

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bauiv1.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bauiv1.getsound('swish').play()
        self._transition_out()


class IceFX(bascenev1.Actor):
    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        scorch = bascenev1.newnode(
            'scorch',
            attrs={
                'position': position,
                'big': True,
                'color': (0.5, 0.9, 1.0)
            },
        )
        bascenev1.animate(scorch, 'size', {0.0: 0.4, 1.5: 0})
        bascenev1.timer(1.5, scorch.delete)


class CustomMod:
    def __init__(self):
        # Save original methods
        Spaz.old_init = Spaz.__init__
        
        def new_init(self, *args, **kwargs):
            # Call original method with all arguments
            self.old_init(*args, **kwargs)
            
            if not self.source_player:
                return
            if not babase.app.config['Iceman']['enable mod']:
                return
            if babase.app.config['Iceman']['ice bomb']:
                self.bomb_type = 'ice'
            if babase.app.config['Iceman']['ice effect']:
                light = bascenev1.newnode(
                    'light',
                    owner=self.node,
                    attrs={
                        'radius': 0.1,
                        'intensity': 0.4,
                        'height_attenuated': False,
                        'color': (0.5, 0.9, 1.0)
                    },
                )
                self.node.connectattr('position', light, 'position')
                self.node.color = self.node.highlight = (0.5, 0.9, 1.0)
                
                def emit():
                    if not self.node:
                        return
                    if babase.app.config['Iceman']['ice effect']:
                        IceFX(position=self.node.position)
                bascenev1.timer(0.1, emit, repeat=True)
        
        Spaz.__init__ = new_init

        # Also fix the handlemessage method
        Spaz.old_handlemessage = Spaz.handlemessage
        
        def new_handlemessage(self, msg: Any) -> Any:
            if isinstance(msg, PunchHitMessage):
                if not self.node:
                    return None
                node = bascenev1.getcollision().opposingnode
                try:
                    if self.source_player:
                        bot = node.getdelegate(SpazBot, True)
                        if bot.is_alive():
                            if babase.app.config['Iceman']['ice punch']:
                                bauiv1.getsound("freeze").play()
                                bot.handlemessage(bascenev1.FreezeMessage())
                                bot.shatter(True)
                                bot.handlemessage(bascenev1.DieMessage())
                                return None  # Don't propagate original message
                except bascenev1.NotFoundError:
                    pass
                # If not a bot, or ice punch not enabled, handle message normally
                return self.old_handlemessage(msg)
            elif isinstance(msg, bascenev1.FreezeMessage):
                if not self.node:
                    return None
                if self.source_player:
                    if babase.app.config['Iceman']['enable mod']:
                        if babase.app.config['Iceman']['ice immunity']:
                            # Play block sound using the correct method
                            bauiv1.getsound("icebelleDeath").play()
                            return None  # Don't freeze if immune
                # If no immunity, propagate the message
                return self.old_handlemessage(msg)
            else:
                return self.old_handlemessage(msg)
        
        Spaz.handlemessage = new_handlemessage


VERSION = "1.1.2"
UPDATE_URL = (
    "https://raw.githubusercontent.com/danigomezdev/bombsquad/"
    "refs/heads/main/IceMan/IceMan.json"
)

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
        bauiv1.textwidget(w, text=t, color=c)


class UpdateWindow(bauiv1.Window):
    def __init__(s, start_check=True):
        w, h = 455, 180
        us = bauiv1.app.ui_v1.uiscale
        sc = 1.8 if us is babase.UIScale.SMALL else 1.3 if us is babase.UIScale.MEDIUM else 0.9
        super().__init__(
            root_widget=bauiv1.containerwidget(parent=bauiv1.get_special_widget("overlay_stack"),
                size=(w, h), scale=sc, color=(0.4, 0.37, 0.49),
                stack_offset=(0, 0), on_outside_click_call=s.close),
            prevent_main_window_auto_recreate=False)
        s._updating = False
        lpm_installed = os.path.exists(os.path.join(_E["python_directory_user"], "LessPluginManager.py"))
        bauiv1.textwidget(parent=s._root_widget, position=(w/2, h-26), size=(0,0),
            text="Updates", scale=0.85, color=(0.9,0.9,0.9), h_align="center", v_align="center", maxwidth=w-130 if not lpm_installed else w-40)
        bauiv1.buttonwidget(parent=s._root_widget, position=(27, h-42), size=(36,36),
            label=babase.charstr(babase.SpecialChar.BACK), button_type="backSmall",
            color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s.close)
        if not lpm_installed:
            bauiv1.buttonwidget(parent=s._root_widget, position=(w-161, h-38), size=(140,30),
                label="LessPluginManager", autoselect=True,
                color=(0.55, 0.35, 0.75), textcolor=(0.9, 0.85, 1.0),
                on_activate_call=s._show_lpm)
        bauiv1.textwidget(parent=s._root_widget, position=(w/2, h-70), size=(0,0),
            text=f"Current: v{VERSION}", scale=0.72, color=(0.9,0.9,0.9),
            h_align="center", v_align="center", maxwidth=w-40)
        s._st = bauiv1.textwidget(parent=s._root_widget, position=(w/2, h-100), size=(0,0),
            text="Checking...", scale=0.65, color=(0.5,0.5,0.5), h_align="center", v_align="center", maxwidth=w-40)
        s._ab = bauiv1.buttonwidget(parent=s._root_widget, position=(w/2-50, 30), size=(100,34),
            label="Check", color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s._sc)
        if start_check: s._sc()

    def _show_lpm(s):
        w2, h2 = 360, 180
        sc2 = 1.3 if bauiv1.app.ui_v1.uiscale is babase.UIScale.MEDIUM else 0.9
        r = bauiv1.containerwidget(
            parent=bauiv1.get_special_widget("overlay_stack"),
            size=(w2, h2), scale=sc2, color=(0.4, 0.37, 0.49),
            stack_offset=(0, 0),
            on_outside_click_call=lambda: r.delete(),
        )
        bauiv1.textwidget(parent=r, position=(w2/2, h2-27), size=(0,0),
            text="LessPluginManager", scale=0.8, color=(0.9,0.9,0.9),
            h_align="center", v_align="center", maxwidth=w2-40)
        bauiv1.buttonwidget(parent=r, position=(27, h2-43), size=(36,36),
            label=babase.charstr(babase.SpecialChar.BACK), button_type="backSmall",
            color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9),
            on_activate_call=lambda: r.delete())
        bauiv1.textwidget(parent=r, position=(w2/2, h2-78), size=(0,0),
            text="Enhanced plugin manager with\nupdate buttons, mod downloads\nand category filters.",
            scale=0.55, color=(0.8,0.8,0.8),
            h_align="center", v_align="center", maxwidth=w2-30)
        s._lpm_st = bauiv1.textwidget(parent=r, position=(w2/2, 65), size=(0,0),
            text="", scale=0.5, color=(0.5,0.5,0.5),
            h_align="center", v_align="center")
        bauiv1.buttonwidget(parent=r, position=(w2/2-68, 18), size=(136, 40),
            label="Download v1.0", color=(0.25, 0.45, 0.75), textcolor=(1,1,1),
            on_activate_call=s._download_lpm)

    def _download_lpm(s):
        bauiv1.textwidget(s._lpm_st, text="Downloading...", color=(0.5,0.5,1))
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
        bauiv1.textwidget(s._st, text="Checking...", color=(0.5,0.5,0.5))
        bauiv1.buttonwidget(s._ab, label="...", color=(0.4,0.4,0.4))
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
        bauiv1.textwidget(s._st, text=f"Latest: v{rv}", color=(0.3,0.9,0.3))
        bauiv1.buttonwidget(s._ab, label="Update", color=(0.2,0.6,0.2), textcolor=(1,1,1), on_activate_call=s._du)
    def _su2d(s):
        bauiv1.textwidget(s._st, text="You have the latest version.", color=(0.3,0.9,0.3))
        bauiv1.buttonwidget(s._ab, label="OK", color=(0.2,0.6,0.2), textcolor=(1,1,1))
    def _ser(s):
        bauiv1.textwidget(s._st, text="Could not check for updates.", color=(1,0.5,0.5))
        bauiv1.buttonwidget(s._ab, label="Retry", color=(0.5,0.4,0.6), textcolor=(1,1,1))
    def _du(s):
        if s._updating: return
        s._updating = True
        bauiv1.textwidget(s._st, text="Downloading...", color=(0.5,0.5,1))
        bauiv1.buttonwidget(s._ab, label="...", color=(0.4,0.4,0.4))
        threading.Thread(target=s._rd, args=(s._info,), daemon=True).start()
    def _rd(s, info):
        url = info.get("url_raw_mod", "")
        if not url: return s._ss("No download URL.", (1,0.5,0.5))
        try:
            req = urllib.request.Request(url, headers=_H)
            with urllib.request.urlopen(req, timeout=60) as resp: c = resp.read()
            with open(os.path.join(_E["python_directory_user"], "IceMan.py"), "wb") as f: f.write(c)
            s._ss("Updated! Restart BombSquad.", (0,1,0))
        except Exception as e: s._ss(f"Error: {e}", (1,0.5,0.5))
    def _ss(s, t, c):
        babase.pushcall(lambda: _sut(s._st, t, c), from_other_thread=True)


# ba_meta export babase.Plugin
class byLess(babase.Plugin):

    def on_app_running(self) -> None:
        self.setup_config()
        self.custom_plugin()

    def setup_config(self) -> None:
        cfgname = 'Iceman'
        if cfgname not in babase.app.config:
            mod_list = {
                'enable mod': True,
                'ice bomb': True,
                'ice punch': True,
                'ice effect': True,
                'ice immunity': True,
            }
            babase.app.config[cfgname] = mod_list
            babase.app.config.apply_and_commit()

    def custom_plugin(self) -> None:
        CustomMod()

    def has_settings_ui(self) -> bool:
        return True

    def show_settings_ui(self, source_widget: babase.Widget | None) -> None:
        ModSettingsPopup()