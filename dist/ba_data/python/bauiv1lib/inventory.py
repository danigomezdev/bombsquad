# Released under the MIT License. See LICENSE for details.
#
"""Provides help related ui."""

from __future__ import annotations

from typing import override

import bauiv1 as bui


class InventoryWindow(bui.MainWindow):
    """Shows what you got."""

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
        auxiliary_style: bool = True,
    ):

        uiscale = bui.app.ui_v1.uiscale
        self._width = 1400 if uiscale is bui.UIScale.SMALL else 750
        self._height = (
            1200
            if uiscale is bui.UIScale.SMALL
            else 530 if uiscale is bui.UIScale.MEDIUM else 600
        )

        # Do some fancy math to fill all available screen area up to the
        # size of our backing container. This lets us fit to the exact
        # screen shape at small ui scale.
        screensize = bui.get_virtual_screen_size()
        scale = (
            1.55
            if uiscale is bui.UIScale.SMALL
            else 1.15 if uiscale is bui.UIScale.MEDIUM else 1.0
        )

        # Calc screen size in our local container space and clamp to a
        # bit smaller than our container size.
        target_height = min(self._height - 100, screensize[1] / scale)

        # To get top/left coords, go to the center of our window and
        # offset by half the width/height of our target area.
        yoffs = 0.5 * self._height + 0.5 * target_height + 30.0

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                toolbar_visibility=(
                    'menu_full' if uiscale is bui.UIScale.SMALL else 'menu_full'
                ),
                toolbar_cancel_button_style=(
                    'close' if auxiliary_style else 'back'
                ),
                scale=scale,
            ),
            transition=transition,
            origin_widget=origin_widget,
            # We're affected by screen size only at small ui-scale.
            refresh_on_screen_size_changes=uiscale is bui.UIScale.SMALL,
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(
                self._width * 0.5,
                yoffs - (50 if uiscale is bui.UIScale.SMALL else 30),
            ),
            size=(0, 0),
            text=bui.Lstr(resource='inventoryText'),
            color=bui.app.ui_v1.title_color,
            scale=0.9 if uiscale is bui.UIScale.SMALL else 1.0,
            maxwidth=(130 if uiscale is bui.UIScale.SMALL else 200),
            h_align='center',
            v_align='center',
        )

        if uiscale is bui.UIScale.SMALL:
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self.main_window_back
            )
        else:
            btn = bui.buttonwidget(
                parent=self._root_widget,
                scale=0.8,
                position=(50, yoffs - 50),
                size=(50, 50) if auxiliary_style else (60, 55),
                extra_touch_border_scale=2.0,
                button_type=None if auxiliary_style else 'backSmall',
                on_activate_call=self.main_window_back,
                autoselect=True,
                label=bui.charstr(
                    bui.SpecialChar.CLOSE
                    if auxiliary_style
                    else bui.SpecialChar.BACK
                ),
            )
            bui.containerwidget(edit=self._root_widget, cancel_button=btn)

        if bool(False):
            print('WOULD TEST NEW STUFF')
        else:
            button_width = 300
            self._player_profiles_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(self._width * 0.5 - button_width * 0.5, yoffs - 200),
                autoselect=True,
                size=(button_width, 60),
                label=bui.Lstr(resource='playerProfilesWindow.titleText'),
                color=(0.55, 0.5, 0.6),
                icon=bui.gettexture('cuteSpaz'),
                textcolor=(0.75, 0.7, 0.8),
                on_activate_call=self._player_profiles_press,
            )
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.5, yoffs - 250),
                size=(0, 0),
                text=bui.Lstr(resource='moreSoonText'),
                scale=0.7,
                maxwidth=self._width * 0.9,
                h_align='center',
                v_align='center',
            )

    def _player_profiles_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.profile.browser import ProfileBrowserWindow

        self.main_window_replace(
            lambda: ProfileBrowserWindow(
                origin_widget=self._player_profiles_button
            )
        )

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )
