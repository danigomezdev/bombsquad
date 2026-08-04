# ba_meta require api 9

from __future__ import annotations
from typing import TYPE_CHECKING, cast

import json, os, threading
import urllib.error, urllib.request
import _babase
import bauiv1 as bui
import babase
import bascenev1 as bs
import random
from bascenev1._map import Map
from bascenev1lib.mainmenu import MainMenuSession

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable, List, Dict, Tuple, Optional, Union

# Text settings
TEXT_CONTENT = "\ue00cLess\ue00c"  
TEXT_SIZE = 0.01             
TEXT_COLOR = (1, 1, 1)   

VERSION = "1.1.2"
UPDATE_URL = "https://raw.githubusercontent.com/danigomezdev/bombsquad/refs/heads/main/EffectRushStar/EffectRushStar.json"

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
        w, h = 400, 230
        us = bui.app.ui_v1.uiscale
        sc = 1.8 if us is babase.UIScale.SMALL else 1.3 if us is babase.UIScale.MEDIUM else 0.9
        super().__init__(
            root_widget=bui.containerwidget(parent=bui.get_special_widget("overlay_stack"),
                size=(w, h), scale=sc, color=(0.4, 0.37, 0.49),
                stack_offset=(0, 0), on_outside_click_call=s.close),
            prevent_main_window_auto_recreate=False)
        s._updating = False
        bui.textwidget(parent=s._root_widget, position=(w/2, h-26), size=(0,0),
            text="Updates", scale=0.85, color=(0.9,0.9,0.9), h_align="center", v_align="center", maxwidth=w-40)
        bui.buttonwidget(parent=s._root_widget, position=(17, h-42), size=(36,36),
            label=babase.charstr(babase.SpecialChar.BACK), button_type="backSmall",
            color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s.close)
        bui.textwidget(parent=s._root_widget, position=(w/2, h-70), size=(0,0),
            text=f"Current: v{VERSION}", scale=0.72, color=(0.9,0.9,0.9),
            h_align="center", v_align="center", maxwidth=w-40)
        s._st = bui.textwidget(parent=s._root_widget, position=(w/2, h-100), size=(0,0),
            text="Checking...", scale=0.65, color=(0.5,0.5,0.5), h_align="center", v_align="center", maxwidth=w-40)
        s._ab = bui.buttonwidget(parent=s._root_widget, position=(w/2-50, 40), size=(100,34),
            label="Check", color=(0.5,0.4,0.6), textcolor=(0.9,0.9,0.9), on_activate_call=s._sc)
        if start_check: s._sc()
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
            with open(os.path.join(_E["python_directory_user"], "EffectRushStar.py"), "wb") as f: f.write(c)
            s._ss("Updated! Restart BombSquad.", (0,1,0))
        except Exception as e: s._ss(f"Error: {e}", (1,0.5,0.5))
    def _ss(s, t, c):
        babase.pushcall(lambda: _sut(s._st, t, c), from_other_thread=True)


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def has_settings_ui(s): return True
    def show_settings_ui(s, w): UpdateWindow()  #only_updates

    Map._old_init = Map.__init__

    def _new_init(self, vr_overlay_offset: Optional[Sequence[float]] = None) -> None:
        self._old_init(vr_overlay_offset)   
        in_game = not isinstance(bs.get_foreground_host_session(), MainMenuSession)
        if not in_game: 
            return

        def path():

            shield1 = bs.newnode("shield", attrs={
                'color': (1, 1, 1), 
                'position': (-5.750, 4.3515026107, 2.0), 
                'radius': 1.4
            })


            bs.animate_array(shield1, 'color', 3, {
                0: (random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                    random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                    random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])),
                0.2: (2, 0, 2), 
                0.4: (2, 2, 0), 
                0.6: (0, 2, 0), 
                0.8: (0, 2, 2)
            }, loop=True)


            flash1 = bs.newnode("flash", attrs={
                'position': (0, 0, 0), 
                'size': 0.6, 
                'color': (1, 1, 1)
            })
            shield1.connectattr('position', flash1, 'position')


            text_node1 = bs.newnode('text',
                attrs={
                    'text': TEXT_CONTENT,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'color': TEXT_COLOR,
                    'scale': TEXT_SIZE,
                    'h_align': 'center'
                }
            )


            text_math1 = bs.newnode('math',
                attrs={
                    'input1': (0, 1.2, 0),  
                    'operation': 'add'
                }
            )
            shield1.connectattr('position', text_math1, 'input2')
            text_math1.connectattr('output', text_node1, 'position')

            bs.animate_array(text_node1, 'color', 3, {
                0: (1, 0, 0), # red
                0.2: (1, 1, 0), # yellow
                0.4: (0, 1, 0), # green
                0.6: (0, 1, 1), # light blue
                0.8: (1, 0, 1), # purple
            }, loop=True)

            bs.animate_array(shield1, 'position', 3, {
                0: (-10, 3, -5),
                5: (10, 6, -5),
                10: (-10, 3, 5),
                15: (10, 6, 5),
                20: (-10, 3, -5)
            }, loop=True)

            shield2 = bs.newnode("shield", attrs={
                'color': (1, 1, 1), 
                'position': (5.750, 4.3515026107, -2.0), 
                'radius': 1.4
            })

            bs.animate_array(shield2, 'color', 3, {
                0: (random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                    random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                    random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])),
                0.2: (0, 2, 2), 
                0.4: (2, 0, 2), 
                0.6: (2, 2, 0), 
                0.8: (0, 2, 0)
            }, loop=True)

            flash2 = bs.newnode("flash", attrs={
                'position': (0, 0, 0), 
                'size': 0.6, 
                'color': (1, 1, 1)
            })
            shield2.connectattr('position', flash2, 'position')

            text_node2 = bs.newnode('text',
                attrs={
                    'text': TEXT_CONTENT,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'color': TEXT_COLOR,
                    'scale': TEXT_SIZE,
                    'h_align': 'center'
                }
            )

            text_math2 = bs.newnode('math',
                attrs={
                    'input1': (0, 1.2, 0),  
                    'operation': 'add'
                }
            )
            shield2.connectattr('position', text_math2, 'input2')
            text_math2.connectattr('output', text_node2, 'position')

            bs.animate_array(text_node2, 'color', 3, {
                0: (1, 0, 1),   # purple
                0.2: (0, 1, 1), # light blue
                0.4: (0, 1, 0), # green
                0.6: (1, 1, 0), # yellow
                0.8: (1, 0, 0), # red
            }, loop=True)

            bs.animate_array(shield2, 'position', 3, {
                0: (10, 6, 5),
                5: (-10, 3, 5),
                10: (10, 6, -5),
                15: (-10, 3, -5),
                20: (10, 6, 5)
            }, loop=True)

        bs.timer(0.1, path)

    Map.__init__ = _new_init