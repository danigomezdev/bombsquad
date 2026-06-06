from __future__ import annotations

from typing import override

import bauiv1 as bui


class V3AccountWindow(bui.MainWindow):

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        app = bui.app
        assert app.classic is not None

        uiscale = app.ui_v1.uiscale
        self._width = 750 if uiscale is bui.UIScale.SMALL else 520
        self._height = 550 if uiscale is bui.UIScale.SMALL else 400

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                toolbar_visibility='menu_full',
                scale=(
                    1.6 if uiscale is bui.UIScale.SMALL
                    else 1.1 if uiscale is bui.UIScale.MEDIUM else 0.9
                ),
            ),
            transition=transition,
            origin_widget=origin_widget,
        )

        self._build_ui()

    def _build_ui(self) -> None:
        v3_user = bui.app.config.get('V3 Username', '')

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 50),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='V3 Account',
            color=bui.app.ui_v1.title_color,
            scale=1.2,
            maxwidth=self._width * 0.8,
        )

        y = self._height - 95
        row_h = 35

        info: list[tuple[str, str]] = [
            ('Username', v3_user),
            ('Tickets', '...'),
            ('Tokens', '...'),
        ]
        for label, value in info:
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.25, y),
                size=(0, 0),
                text=label,
                h_align='right',
                v_align='center',
                color=(0.6, 0.6, 0.6),
                scale=0.7,
                flatness=1.0,
                shadow=0.0,
                maxwidth=self._width * 0.3,
            )
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.28, y),
                size=(0, 0),
                text=value,
                h_align='left',
                v_align='center',
                color=(1, 1, 1),
                scale=0.7,
                flatness=1.0,
                shadow=0.0,
                maxwidth=self._width * 0.5,
            )
            y -= row_h

        y -= 20
        btn_w = 220
        buttons: list[tuple[str, str]] = [
            ('Manage Characters', 'characterIconMask'),
            ('Manage Profiles', 'inventoryIcon'),
            ('Change Password', 'lockIcon'),
        ]
        for label, icon in buttons:
            bui.buttonwidget(
                parent=self._root_widget,
                position=((self._width - btn_w) * 0.5, y),
                size=(btn_w, 45),
                label=label,
                icon=bui.gettexture(icon),
                iconscale=0.8,
                color=(0.4, 0.45, 0.55),
                autoselect=True,
                on_activate_call=bui.CallStrict(
                    self._placeholder, label
                ),
            )
            y -= 55

        y -= 15
        bui.buttonwidget(
            parent=self._root_widget,
            position=((self._width - btn_w) * 0.5, y),
            size=(btn_w, 45),
            label='Sign Out',
            icon=bui.gettexture('cancelIcon'),
            iconscale=0.8,
            color=(0.5, 0.2, 0.2),
            autoselect=True,
            on_activate_call=self._sign_out,
        )

    def _placeholder(self, label: str) -> None:
        bui.screenmessage(f'{label} coming soon', color=(0.5, 0.5, 1))

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

    def _sign_out(self) -> None:
        import _babase
        cfg = bui.app.config
        cfg['V3 Token'] = ''
        cfg['V3 Username'] = ''
        cfg.commit()
        _babase.set_account_sign_in_state(False)
        bui.screenmessage('Signed out', color=(1, 0.5, 0))
        self.main_window_back()
