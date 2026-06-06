from __future__ import annotations

import json
from threading import Thread
from typing import override

import bauiv1 as bui
import bascenev1 as bs
from bascenev1lib.actor.spazappearance import get_appearances


class V3StoreWindow(bui.Window):

    def __init__(self, origin_widget: bui.Widget):
        sw, sh = bui.get_virtual_screen_size()
        self._width = min(900, sw * 0.9)
        self._height = min(650, sh * 0.9)
        self._chars: list[dict] = []
        self._loaded = False
        self._busy = False

        assert bui.app.classic is not None
        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                toolbar_visibility='menu_full',
                scale=(
                    1.9 if uiscale is bui.UIScale.SMALL
                    else 1.3 if uiscale is bui.UIScale.MEDIUM else 1.0
                ),
                scale_origin_stack_offset=(
                    origin_widget.get_screen_space_center()
                ),
            )
        )

        self._appearances = get_appearances(include_locked=True)
        self._app_map: dict[str, object] = {}
        assert bui.app.classic is not None
        for name in self._appearances:
            app = bui.app.classic.spaz_appearances.get(name)
            if app:
                self._app_map[app.name.lower().replace(' ', '')] = app

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 45),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='V3 Store',
            color=(1, 1, 1),
            scale=1.2,
        )

        self._status = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            text='Loading...',
            h_align='center',
            v_align='center',
        )
        self._spinner = bui.spinnerwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 25, self._height * 0.5 + 30),
            size=40,
            style='bomb',
        )

        token = bui.app.config.get('V3 Token', '')
        if not token:
            bui.textwidget(edit=self._status, text='Not signed in', color=(1, 0.3, 0.3))
            bui.spinnerwidget(edit=self._spinner, visible=False)
            return

        V3StoreFetcher(
            self._on_loaded
        ).start()

    def _on_loaded(self, ok: bool, data: list[dict] | str) -> None:
        self._loaded = True
        bui.spinnerwidget(edit=self._spinner, visible=False)
        if not ok:
            msg = str(data)[:200]
            bui.textwidget(edit=self._status, text=msg, color=(1, 0.3, 0.3))
            bui.screenmessage(f'Store error: {msg[:80]}', color=(1, 0, 0))
            return
        bui.textwidget(edit=self._status, text='')
        self._chars = data
        try:
            self._build_grid()
        except Exception as e:
            bui.textwidget(edit=self._status, text=str(e), color=(1, 0.3, 0.3))

    def _build_grid(self) -> None:
        cols = 4
        icon_size = 100
        cell_w = (self._width - 60) / cols
        cell_h = icon_size + 60

        scroll_w = self._width - 40
        scroll_h = self._height - 90
        rows = (len(self._chars) + cols - 1) // cols
        content_h = max(rows * cell_h + 30, scroll_h)

        scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(20, 25),
            size=(scroll_w, scroll_h),
            background=False,
            capture_arrows=True,
            simple_culling_v=cell_h * 2,
        )
        container = bui.containerwidget(
            parent=scroll,
            size=(scroll_w - 10, content_h),
            background=False,
            selection_loops_to_parent=True,
        )

        for i, ch in enumerate(self._chars):
            col = i % cols
            row = i // cols
            cx = col * cell_w + 10
            cy = content_h - (row + 1) * cell_h

            char_id = ch.get('id', '')
            name = ch.get('name', '?')
            owned = ch.get('owned', False)
            active = ch.get('is_active', False)
            price_t = ch.get('price_tickets', 0)
            price_k = ch.get('price_tokens', 0)

            bx = cx + (cell_w - icon_size) / 2 - 10
            by = cy + 20

            app = self._app_map.get(char_id)
            icon_tex = app.icon_texture if app else 'white'
            icon_mask = app.icon_mask_texture if app else 'white'

            btn_color = (0.3, 0.7, 0.3) if active else (0.3, 0.4, 0.5)
            if owned:
                label = 'Active' if active else 'Equip'
                action = bui.CallStrict(self._equip, char_id)
            elif price_t > 0:
                label = f'{price_t}T'
                action = bui.CallStrict(self._buy, char_id, 'tickets')
                btn_color = (0.6, 0.5, 0.2)
            else:
                label = ''
                action = bui.CallStrict(self._equip, char_id)
                btn_color = (0.3, 0.5, 0.4)

            btn = bui.buttonwidget(
                parent=container,
                size=(icon_size, icon_size),
                position=(bx, by),
                button_type='square',
                color=btn_color,
                autoselect=True,
                on_activate_call=action,
            )

            if icon_tex != 'white':
                bui.imagewidget(
                    parent=container,
                    draw_controller=btn,
                    size=(icon_size, icon_size),
                    position=(bx, by),
                    texture=bui.gettexture(icon_tex),
                    tint_texture=bui.gettexture(icon_mask),
                    mask_texture=bui.gettexture('characterIconMask'),
                    tint_color=(1, 1, 1),
                    tint2_color=(1, 1, 1),
                )

            bui.textwidget(
                parent=container,
                draw_controller=btn,
                text=name,
                position=(cx + cell_w / 2 - 10, by - 2),
                size=(0, 0),
                h_align='center',
                v_align='top',
                maxwidth=cell_w - 20,
                scale=0.5,
                color=(0, 1, 0) if owned else (1, 1, 1),
                flatness=1.0,
                shadow=0.3,
            )

            if label:
                bui.textwidget(
                    parent=container,
                    draw_controller=btn,
                    text=label,
                    position=(cx + cell_w / 2 - 10, by + icon_size + 5),
                    size=(0, 0),
                    h_align='center',
                    v_align='center',
                    scale=0.5,
                    color=(1, 1, 1),
                    flatness=1.0,
                    shadow=0.3,
                )

    def _equip(self, char_id: str) -> None:
        if self._busy:
            return
        self._busy = True
        V3StoreAPI(
            'PATCH',
            _api_url('/api/v3/account'),
            {'active_character': char_id},
            lambda ok, data: self._on_result(ok, data, f'Equipped {char_id}'),
        ).start()

    def _buy(self, char_id: str, currency: str) -> None:
        if self._busy:
            return
        self._busy = True
        V3StoreAPI(
            'POST',
            _api_url(f'/api/v3/characters/{char_id}/purchase'),
            {'currency': currency},
            lambda ok, data: self._on_result(ok, data, f'Bought {char_id}!'),
        ).start()

    def _on_result(self, ok: bool, data, msg: str) -> None:
        self._busy = False
        if ok:
            bui.screenmessage(msg, color=(0, 1, 0))
            self._refresh()
        else:
            bui.screenmessage(str(data), color=(1, 0.3, 0.3))

    def _refresh(self) -> None:
        self._spinner = bui.spinnerwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 25, self._height * 0.5 + 30),
            size=40,
            style='bomb',
            visible=True,
        )
        V3StoreFetcher(
            self._on_loaded
        ).start()


def _api_url(path: str) -> str:
    import os
    base = os.environ.get('BA_API_URL', '')
    if not base:
        base = 'http://localhost:3333' if bs.app.env.debug_build else 'https://api.bombsquad.lat'
    return f'{base}{path}'


class V3StoreFetcher(Thread):

    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    @override
    def run(self) -> None:
        try:
            token = bui.app.config.get('V3 Token', '')
            import urllib.request
            import sys

            sys.stderr.write(f'STORE_DEBUG: fetching account. token_len={len(token)}\n')
            sys.stderr.flush()

            _req(_api_url('/api/v3/account'), token)

            sys.stderr.write(f'STORE_DEBUG: fetching characters\n')
            sys.stderr.flush()

            data = _req(_api_url('/api/v3/characters'), token)
            items = data.get('characters', [])

            sys.stderr.write(f'STORE_DEBUG: got {len(items)} chars\n')
            sys.stderr.flush()

            bui.pushcall(
                lambda cb=self._callback, ok=True, d=items: cb(ok, d),
                from_other_thread=True,
            )
        except Exception as exc:
            import traceback
            msg = f'{exc}'
            sys.stderr.write(f'STORE_DEBUG: ERROR {msg}\n{traceback.format_exc()}\n')
            sys.stderr.flush()
            bui.pushcall(
                lambda cb=self._callback, e=msg: cb(False, e),
                from_other_thread=True,
            )


def _req(url: str, token: str) -> dict:
    import urllib.request
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {token}'},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read().decode())


class V3StoreAPI(Thread):

    def __init__(self, method: str, url: str, body: dict, callback):
        super().__init__()
        self._method = method
        self._url = url
        self._body = body
        self._callback = callback

    @override
    def run(self) -> None:
        try:
            token = bui.app.config.get('V3 Token', '')
            import urllib.request
            data = json.dumps(self._body).encode()
            req = urllib.request.Request(
                self._url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}',
                },
                method=self._method,
            )
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read().decode())
            bui.pushcall(
                bui.CallStrict(self._callback, True, result),
                from_other_thread=True,
            )
        except Exception as exc:
            bui.pushcall(
                bui.CallStrict(self._callback, False, str(exc)),
                from_other_thread=True,
            )
