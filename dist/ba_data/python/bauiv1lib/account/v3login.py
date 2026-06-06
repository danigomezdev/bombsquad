from __future__ import annotations

import json
import time
from threading import Thread
from typing import override

import bauiv1 as bui
import bascenev1 as bs

import os as _os
import _babase
_API_ENV = _os.environ.get('BA_API_URL', '')
if _API_ENV:
    API_BASE = _API_ENV
elif bs.app.env.debug_build:
    API_BASE = 'http://localhost:3333'
else:
    API_BASE = 'https://api.bombsquad.lat'


class V3SignInWindow(bui.Window):

    def __init__(self, origin_widget: bui.Widget):
        self._width = 550
        self._height = 450
        self._idprefix = bui.app.ui_v1.new_id_prefix('v3signin')
        self._username = ''
        self._password = ''
        self._status_text: bui.Widget | None = None
        self._busy = False

        assert bui.app.classic is not None
        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                scale_origin_stack_offset=(
                    origin_widget.get_screen_space_center()
                ),
                scale=(
                    1.16
                    if uiscale is bui.UIScale.SMALL
                    else 1.0 if uiscale is bui.UIScale.MEDIUM else 0.9
                ),
            )
        )

        self._cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(30, self._height - 65),
            size=(130, 50),
            scale=0.8,
            label=bui.Lstr(resource='cancelText'),
            on_activate_call=self._close,
            autoselect=True,
        )
        bui.containerwidget(
            edit=self._root_widget, cancel_button=self._cancel_button
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 60),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=bui.Lstr(value='Login'),
            color=bui.app.ui_v1.title_color,
            scale=1.2,
            maxwidth=self._width * 0.8,
        )

        self._build_login_form()

    def _build_login_form(self) -> None:
        cy = self._height * 0.5 + 40

        bui.textwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|userlabel',
            position=(self._width * 0.5 - 200, cy + 10),
            size=(80, 30),
            text='Username',
            h_align='right',
            v_align='center',
            scale=0.8,
            color=(0.6, 0.6, 0.6),
            flatness=1.0,
            shadow=0.0,
        )
        self._user_field = bui.textwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|user',
            position=(self._width * 0.5 - 110, cy),
            size=(310, 45),
            editable=True,
            h_align='left',
            v_align='center',
            text='',
            max_chars=32,
            description='Username',
            autoselect=True,
        )

        cy -= 60
        bui.textwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|passlabel',
            position=(self._width * 0.5 - 200, cy + 10),
            size=(80, 30),
            text='Password',
            h_align='right',
            v_align='center',
            scale=0.8,
            color=(0.6, 0.6, 0.6),
            flatness=1.0,
            shadow=0.0,
        )
        self._pass_field = bui.textwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|pass',
            position=(self._width * 0.5 - 110, cy),
            size=(310, 45),
            editable=True,
            h_align='left',
            v_align='center',
            text='',
            max_chars=64,
            description='Password',
        )
        bui.widget(edit=self._pass_field, up_widget=self._user_field)

        cy -= 80
        self._login_btn = bui.buttonwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|login',
            position=(self._width * 0.5 - 120, cy),
            size=(240, 50),
            label='Sign In',
            on_activate_call=self._do_login,
            autoselect=True,
        )
        bui.widget(edit=self._login_btn, up_widget=self._pass_field)

        self._status_text = bui.textwidget(
            parent=self._root_widget,
            id=f'{self._idprefix}|status',
            position=(self._width * 0.5, cy - 20),
            size=(0, 0),
            text='',
            h_align='center',
            v_align='center',
            scale=0.75,
            color=(1, 0.3, 0.3),
            flatness=1.0,
            shadow=0.0,
        )

        self._spinner = bui.spinnerwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 25, cy - 25),
            size=40,
            style='bomb',
            visible=False,
        )

    def _show_register(self) -> None:
        self._close()
        V3RegisterWindow()

    def _do_login(self) -> None:
        if self._busy:
            return
        username = bui.textwidget(query=self._user_field).strip()
        password = bui.textwidget(query=self._pass_field)
        if not username or not password:
            self._status('Username and password required', (1, 0.3, 0.3))
            return
        self._busy = True
        self._status('Signing in...', (0.6, 0.6, 0.6))
        bui.spinnerwidget(edit=self._spinner, visible=True)
        V3AuthThread(
            'POST',
            f'{API_BASE}/auth/login',
            {'name': username, 'password': password},
            self._on_login_result,
        ).start()

    def _on_login_result(self, ok: bool, data: dict | str) -> None:
        bui.spinnerwidget(edit=self._spinner, visible=False)
        self._busy = False
        if not ok:
            self._status(str(data), (1, 0.3, 0.3))
            return
        token = data.get('accessToken', '')
        if not token:
            self._status('No token received', (1, 0.3, 0.3))
            return
        bui.pushcall(
            bui.CallStrict(
                lambda: self._on_signed_in(token, data.get('user', {})),
            )
        )

    def _on_signed_in(self, token: str, user: dict) -> None:

        cfg = bui.app.config
        cfg['V3 Token'] = token
        cfg['V3 Username'] = user.get('name', '')
        cfg.commit()

        _babase.set_account_sign_in_state(
            True, user.get('name', '')
        )

        V3AccountFetcher().start()

        bui.screenmessage(
            f'Signed in as {user.get("name", "")}',
            color=(0, 1, 0),
        )
        self._close()

    def _status(self, text: str, color: tuple[float, float, float]) -> None:
        if self._status_text:
            bui.textwidget(edit=self._status_text, text=text, color=color)

    def _close(self) -> None:
        if self._root_widget and not self._root_widget.transitioning_out:
            bui.containerwidget(
                edit=self._root_widget, transition='out_scale'
            )


class V3RegisterWindow(bui.Window):

    def __init__(self):
        self._width = 550
        self._height = 450
        self._idprefix = bui.app.ui_v1.new_id_prefix('v3register')
        self._busy = False
        self._status_text: bui.Widget | None = None

        assert bui.app.classic is not None
        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                scale=(
                    1.16
                    if uiscale is bui.UIScale.SMALL
                    else 1.0 if uiscale is bui.UIScale.MEDIUM else 0.9
                ),
            )
        )

        self._cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(30, self._height - 65),
            size=(130, 50),
            scale=0.8,
            label=bui.Lstr(resource='cancelText'),
            on_activate_call=self._close,
            autoselect=True,
        )
        bui.containerwidget(
            edit=self._root_widget, cancel_button=self._cancel_button
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 60),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=bui.Lstr(value='Create Account'),
            color=bui.app.ui_v1.title_color,
            scale=1.15,
            maxwidth=self._width * 0.8,
        )

        cy = self._height * 0.5 + 70
        fields = [
            ('username', 'Username'),
            ('password', 'Password'),
        ]
        self._fields: dict[str, bui.Widget] = {}
        for key, label in fields:
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.5 - 200, cy + 10),
                size=(80, 30),
                text=label,
                h_align='right',
                v_align='center',
                scale=0.8,
                color=(0.6, 0.6, 0.6),
                flatness=1.0,
                shadow=0.0,
            )
            self._fields[key] = bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.5 - 110, cy),
                size=(310, 45),
                editable=True,
                h_align='left',
                v_align='center',
                text='',
                max_chars=key == 'username' and 25 or 64,
                description=label,
                autoselect=key == 'username',
            )
            cy -= 65

        bui.widget(edit=self._fields['password'], up_widget=self._fields['username'])

        self._register_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 120, cy),
            size=(240, 50),
            label='Create Account',
            on_activate_call=self._do_register,
            autoselect=True,
        )
        bui.widget(edit=self._register_btn, up_widget=self._fields['password'])

        self._status_text = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, cy - 30),
            size=(0, 0),
            text='',
            h_align='center',
            v_align='center',
            scale=0.75,
            color=(1, 0.3, 0.3),
            flatness=1.0,
            shadow=0.0,
        )

        self._spinner = bui.spinnerwidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 25, cy - 35),
            size=40,
            style='bomb',
            visible=False,
        )

    def _do_register(self) -> None:
        if self._busy:
            return
        username = bui.textwidget(query=self._fields['username']).strip()
        password = bui.textwidget(query=self._fields['password'])
        if not username or not password:
            self._status('Username and password required', (1, 0.3, 0.3))
            return
        if len(password) < 8:
            self._status('Password must be 8+ chars', (1, 0.3, 0.3))
            return
        self._busy = True
        self._status('Creating account...', (0.6, 0.6, 0.6))
        bui.spinnerwidget(edit=self._spinner, visible=True)
        V3AuthThread(
            'POST',
            f'{API_BASE}/auth/register',
            {'name': username, 'password': password},
            self._on_register_result,
        ).start()

    def _on_register_result(self, ok: bool, data: dict | str) -> None:
        bui.spinnerwidget(edit=self._spinner, visible=False)
        self._busy = False
        if not ok:
            self._status(str(data), (1, 0.3, 0.3))
            return
        token = data.get('accessToken', '')
        if not token:
            self._status('No token received', (1, 0.3, 0.3))
            return
        bui.pushcall(
            bui.CallStrict(
                lambda: self._on_registered(token, data.get('user', {})),
            )
        )

    def _on_registered(self, token: str, user: dict) -> None:

        cfg = bui.app.config
        cfg['V3 Token'] = token
        cfg['V3 Username'] = user.get('name', '')
        cfg.commit()

        _babase.set_account_sign_in_state(
            True, user.get('name', '')
        )

        bui.screenmessage(
            f'Account created: {user.get("name", "")}',
            color=(0, 1, 0),
        )
        self._close()

    def _status(self, text: str, color: tuple[float, float, float]) -> None:
        if self._status_text:
            bui.textwidget(edit=self._status_text, text=text, color=color)

    def _close(self) -> None:
        if self._root_widget and not self._root_widget.transitioning_out:
            bui.containerwidget(
                edit=self._root_widget, transition='out_scale'
            )


def _v3_api_base() -> str:
    import os as _os_inner
    env_url = _os_inner.environ.get('BA_API_URL', '')
    if env_url:
        return env_url
    return 'http://localhost:3333' if bs.app.env.debug_build else 'https://api.bombsquad.lat'


class V3AccountFetcher(Thread):

    def __init__(self):
        super().__init__()

    @override
    def run(self) -> None:
        try:
            token = bui.app.config.get('V3 Token', '')
            import urllib.request
            req = urllib.request.Request(
                f'{_v3_api_base()}/api/v3/account',
                headers={
                    'Authorization': f'Bearer {token}',
                    'User-Agent': 'Ballistica/1.7.63',
                },
            )
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode())
            acct = data.get('account', {})
            tickets = acct.get('tickets', -1)
            tokens = acct.get('tokens', -1)
            gold_pass = acct.get('gold_pass', False)

            def apply() -> None:
                import _baclassic
                _baclassic.set_root_ui_account_values(
                    tickets=tickets,
                    tokens=tokens,
                    league_type='',
                    league_number=-1,
                    league_rank=-1,
                    achievements_percent_text='',
                    level_text=f'Level {acct.get("level", 1)}',
                    xp_text=f'{acct.get("xp", 0)}/{acct.get("xpmax", 100)}',
                    inbox_count=-1,
                    inbox_count_is_max=False,
                    inbox_announce_text='',
                    gold_pass=gold_pass,
                    chest_0_appearance='',
                    chest_1_appearance='',
                    chest_2_appearance='',
                    chest_3_appearance='',
                    chest_0_create_time=-1.0,
                    chest_1_create_time=-1.0,
                    chest_2_create_time=-1.0,
                    chest_3_create_time=-1.0,
                    chest_0_unlock_time=-1.0,
                    chest_1_unlock_time=-1.0,
                    chest_2_unlock_time=-1.0,
                    chest_3_unlock_time=-1.0,
                    chest_0_unlock_tokens=-1,
                    chest_1_unlock_tokens=-1,
                    chest_2_unlock_tokens=-1,
                    chest_3_unlock_tokens=-1,
                    chest_0_ad_allow_time=-1.0,
                    chest_1_ad_allow_time=-1.0,
                    chest_2_ad_allow_time=-1.0,
                    chest_3_ad_allow_time=-1.0,
                    store_style='',
                )
            bui.pushcall(apply, from_other_thread=True)
        except Exception:
            pass


class V3AuthThread(Thread):

    def __init__(self, method: str, url: str, body: dict, callback):
        super().__init__()
        self._method = method
        self._url = url
        self._body = body
        self._callback = callback

    @override
    def run(self) -> None:
        try:
            import urllib.request
            data = json.dumps(self._body).encode()
            req = urllib.request.Request(
                self._url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Ballistica/1.7.63',
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
            msg = str(exc)
            try:
                if hasattr(exc, 'read'):
                    body = exc.read().decode()
                    err = json.loads(body)
                    msg = err.get('error', msg)
            except Exception:
                pass
            bui.pushcall(
                bui.CallStrict(self._callback, False, msg),
                from_other_thread=True,
            )
