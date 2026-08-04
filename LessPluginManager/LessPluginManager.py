# ba_meta require api 9

from __future__ import annotations
from typing import override, TYPE_CHECKING

import importlib
import json
import os
import threading
import urllib.error
import urllib.request

import _babase
import babase
import bauiv1 as bui
from bauiv1lib.settings.plugins import PluginWindow, Category
from bauiv1lib import popup

if TYPE_CHECKING:
    from typing import Any

_MODS_API_URL = "https://api.luxkit.net/mods"
_env = _babase.env()
_HEADERS = {"User-Agent": _env["legacy_user_agent_string"]}
_plugin_has_update_cache: dict[str, bool] = {}
_mods_api_cache: list[dict] | None = None


def _plugin_has_update(class_path: str) -> bool:
    module_name = class_path.split('.')[0]
    if module_name in _plugin_has_update_cache:
        return _plugin_has_update_cache[module_name]

    try:
        module = importlib.import_module(module_name)
        has_update = hasattr(module, 'UpdateWindow')
    except Exception:
        has_update = False

    _plugin_has_update_cache[module_name] = has_update
    return has_update


def _fetch_mods_blocking() -> list[dict]:
    global _mods_api_cache
    try:
        req = urllib.request.Request(_MODS_API_URL, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            _mods_api_cache = data
            return data
    except Exception:
        return _mods_api_cache or []


class LessPluginWindow(PluginWindow):

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        self._mode = 'plugins'
        self._download_category = 'all'
        super().__init__(transition=transition, origin_widget=origin_widget)

        uiscale = bui.app.ui_v1.uiscale
        screensize = bui.get_virtual_screen_size()
        scale = (
            1.7 if uiscale is babase.UIScale.SMALL else
            1.4 if uiscale is babase.UIScale.MEDIUM else 1.0
        )
        target_width = min(self._width - 80, screensize[0] / scale)
        target_height = min(self._height - 80, screensize[1] / scale)
        yoffs = 0.5 * self._height + 0.5 * target_height + 20.0

        settings_button_x = (
            self._width * 0.5 + self._scroll_width * 0.5 - 40
        )
        if uiscale is babase.UIScale.SMALL:
            if bui.in_main_menu():
                settings_button_x -= 65
            else:
                settings_button_x -= 115

        button_row_yoffs = yoffs + (
            -2 if uiscale is babase.UIScale.SMALL else 10
        )

        self._downloads_button = bui.buttonwidget(
            parent=self._root_widget,
            id=f'{self.main_window_id_prefix}|downloads',
            position=(120, button_row_yoffs - 58),
            size=(100, 40),
            label='Downloads',
            autoselect=True,
            color=(0.25, 0.45, 0.75),
            textcolor=(0.7, 0.85, 1.0),
            on_activate_call=self._toggle_downloads,
        )

    def _toggle_downloads(self) -> None:
        if self._mode == 'downloads':
            self._mode = 'plugins'
            self._clear_scroll_widget()
            self._show_plugins()
            bui.buttonwidget(
                edit=self._downloads_button,
                label='Downloads',
                color=(0.25, 0.45, 0.75),
            )
            bui.buttonwidget(
                edit=self._category_button,
                label=bui.Lstr(resource=self._category.resource),
                color=(0.55, 0.73, 0.25),
            )
        else:
            self._mode = 'downloads'
            self._download_category = 'all'
            self._clear_scroll_widget()
            self._show_downloads_loading()
            bui.buttonwidget(
                edit=self._downloads_button,
                label='Installed',
                color=(0.25, 0.45, 0.75),
            )
            bui.buttonwidget(
                edit=self._category_button,
                label='All',
                color=(0.55, 0.73, 0.25),
            )
            threading.Thread(
                target=self._fetch_and_populate, daemon=True
            ).start()

    def _show_category_options(self) -> None:
        if self._mode == 'downloads':
            uiscale = bui.app.ui_v1.uiscale
            popup.PopupMenuWindow(
                position=(
                    self._category_button.get_screen_space_center()
                ),
                scale=(
                    2.3 if uiscale is babase.UIScale.SMALL
                    else 1.65 if uiscale is babase.UIScale.MEDIUM
                    else 1.23
                ),
                choices=['all', 'minigame', 'mod'],
                choices_display=[
                    bui.Lstr(value='All'),
                    bui.Lstr(value='Minigames'),
                    bui.Lstr(value='Mods'),
                ],
                current_choice=self._download_category,
                delegate=self,
            )
        else:
            super()._show_category_options()

    def popup_menu_selected_choice(
        self, popup_window: popup.PopupMenuWindow, choice: str
    ) -> None:
        if self._mode == 'downloads':
            del popup_window
            self._download_category = choice
            bui.buttonwidget(
                edit=self._category_button,
                label={
                    'all': 'All', 'minigame': 'Minigames', 'mod': 'Mods'
                }.get(choice, choice),
            )
            self._clear_scroll_widget()
            self._show_downloads_loading()
            threading.Thread(
                target=self._fetch_and_populate, daemon=True
            ).start()
        else:
            super().popup_menu_selected_choice(popup_window, choice)

    def popup_menu_closing(self, popup_window: popup.PopupWindow) -> None:
        pass

    def _show_downloads_loading(self) -> None:
        plug_line_height = 50
        sub_width = self._scroll_width
        sub_height = 80
        bui.containerwidget(
            edit=self._subcontainer,
            size=(self._scroll_width, sub_height),
        )
        bui.textwidget(
            parent=self._subcontainer,
            position=(sub_width * 0.5, sub_height * 0.5),
            size=(0, 0),
            text='Loading mods...',
            scale=0.8,
            color=(0.5, 0.5, 0.5),
            h_align='center',
            v_align='center',
        )
        bui.textwidget(
            edit=self._num_plugins_text,
            text='',
        )

    def _fetch_and_populate(self) -> None:
        mods = _fetch_mods_blocking()
        babase.pushcall(
            lambda: self._populate_downloads(mods),
            from_other_thread=True,
        )

    def _populate_downloads(self, mods: list[dict]) -> None:
        self._clear_scroll_widget()

        if self._download_category != 'all':
            mods = [
                m for m in mods
                if m.get('category', '') == self._download_category
            ]

        plug_line_height = 50
        sub_width = self._scroll_width
        sub_height = max(len(mods) * plug_line_height, 80)
        sub_height = max(len(mods) * plug_line_height, 80)
        bui.containerwidget(
            edit=self._subcontainer,
            size=(self._scroll_width, sub_height),
        )

        if not mods:
            bui.textwidget(
                parent=self._subcontainer,
                position=(sub_width * 0.5, sub_height * 0.5),
                size=(0, 0),
                text='Could not fetch mods list.',
                scale=0.8,
                color=(1, 0.5, 0.5),
                h_align='center',
                v_align='center',
            )
            return

        mods_dir = _env["python_directory_user"]

        for i, mod in enumerate(mods):
            item_y = sub_height - (i + 1) * plug_line_height
            name = mod.get("name", "Unknown")
            version = mod.get("version", "")
            file_name = mod.get("file_name", "")
            installed = os.path.exists(os.path.join(mods_dir, file_name))

            label = f"{name}  v{version}"
            if installed:
                label += "  [installed]"

            bui.textwidget(
                parent=self._subcontainer,
                position=(15, item_y + 10),
                size=(0, 0),
                text=label,
                scale=0.7,
                color=(0, 1, 0) if installed else (0.8, 0.8, 0.8),
                h_align='left',
                v_align='center',
                maxwidth=sub_width - 160,
            )

            btn_label = 'Installed' if installed else 'Download'
            btn_color = (0.3, 0.5, 0.3) if installed else (0.25, 0.45, 0.75)
            dl_btn = bui.buttonwidget(
                parent=self._subcontainer,
                label=btn_label,
                autoselect=True,
                size=(100, 40),
                position=(sub_width - 130, item_y + 6),
                color=btn_color,
                textcolor=(1, 1, 1),
            )
            if installed:
                bui.buttonwidget(
                    edit=dl_btn, color=(0.3, 0.5, 0.3)
                )
            else:
                bui.buttonwidget(
                    edit=dl_btn,
                    on_activate_call=bui.CallStrict(
                        self._download_mod, mod, i
                    ),
                )

        bui.textwidget(
            edit=self._num_plugins_text,
            text=str(len(mods)),
        )

    def _download_mod(self, mod: dict, index: int) -> None:
        file_name = mod.get("file_name", "")
        url = mod.get("url_raw_mod", "")
        if not url or not file_name:
            bui.screenmessage('No download URL.', color=(1, 0.5, 0.5))
            bui.getsound('error').play()
            return

        threading.Thread(
            target=self._download_mod_thread,
            args=(url, file_name),
            daemon=True,
        ).start()

    def _download_mod_thread(self, url: str, file_name: str) -> None:
        try:
            req = urllib.request.Request(url, headers=_HEADERS)
            with urllib.request.urlopen(req, timeout=120) as resp:
                content = resp.read()
            mod_path = os.path.join(
                _env["python_directory_user"], file_name
            )
            with open(mod_path, "wb") as f:
                f.write(content)
            self._show_download_status(
                f'Downloaded {file_name}. Restart BombSquad.',
                (0, 1, 0),
            )
        except Exception as e:
            self._show_download_status(
                f'Error: {e}', (1, 0.5, 0.5)
            )

    def _show_download_status(self, text: str, color: tuple) -> None:
        def _apply():
            bui.screenmessage(text, color=color)
            bui.getsound('dingSmallHigh' if color[1] > 0.5 else 'error').play()
        babase.pushcall(_apply, from_other_thread=True)

    @override
    def _show_plugins(self) -> None:
        if self._mode != 'plugins':
            return
        plugspecs = bui.app.plugins.plugin_specs
        plugstates: dict[str, dict] = bui.app.config.setdefault(
            'Plugins', {}
        )
        assert isinstance(plugstates, dict)

        plug_line_height = 50
        sub_width = self._scroll_width
        num_enabled = 0
        num_disabled = 0

        plugspecs_sorted = sorted(plugspecs.items())

        bui.textwidget(edit=self._no_plugins_installed_text, text='')

        for _classpath, plugspec in plugspecs_sorted:
            if plugspec.enabled:
                num_enabled += 1
            else:
                num_disabled += 1

        if self._category is Category.ALL:
            sub_height = len(plugspecs) * plug_line_height
        elif self._category is Category.ENABLED:
            sub_height = num_enabled * plug_line_height
        elif self._category is Category.DISABLED:
            sub_height = num_disabled * plug_line_height
        else:
            from typing import assert_never
            assert_never(self._category)

        bui.containerwidget(
            edit=self._subcontainer,
            size=(self._scroll_width, sub_height),
        )

        num_shown = 0
        for classpath, plugspec in plugspecs_sorted:
            plugin = plugspec.plugin
            enabled = plugspec.enabled

            if self._category is Category.ALL:
                show = True
            elif self._category is Category.ENABLED:
                show = enabled
            elif self._category is Category.DISABLED:
                show = not enabled
            else:
                from typing import assert_never
                assert_never(self._category)

            if not show:
                continue

            has_settings = (
                plugin is not None and plugin.has_settings_ui()
            )
            has_update = _plugin_has_update(classpath)

            if has_settings and has_update:
                maxwidth_offset = 300
            elif has_settings or has_update:
                maxwidth_offset = 200
            else:
                maxwidth_offset = 80

            item_y = sub_height - (num_shown + 1) * plug_line_height
            check = bui.checkboxwidget(
                parent=self._subcontainer,
                id=f'{self.main_window_id_prefix}|enabled.{classpath}',
                text=bui.Lstr(value=classpath),
                autoselect=True,
                value=enabled,
                maxwidth=self._scroll_width - maxwidth_offset,
                position=(10, item_y),
                size=(self._scroll_width - 40, 50),
                on_value_change_call=bui.CallPartial(
                    self._check_value_changed, plugspec
                ),
                textcolor=(
                    (0.8, 0.3, 0.3)
                    if (plugspec.attempted_load and plugspec.plugin is None)
                    else (
                        (0.6, 0.6, 0.6)
                        if plugspec.plugin is None
                        else (0, 1, 0)
                    )
                ),
            )

            settings_button = None
            update_button = None

            if has_settings:
                settings_button = bui.buttonwidget(
                    parent=self._subcontainer,
                    id=(
                        f'{self.main_window_id_prefix}'
                        f'|settings.{classpath}'
                    ),
                    label=bui.Lstr(resource='mainMenu.settingsText'),
                    autoselect=True,
                    size=(100, 40),
                    position=(sub_width - 130, item_y + 6),
                )
                bui.buttonwidget(
                    edit=settings_button,
                    on_activate_call=bui.CallStrict(
                        plugin.show_settings_ui, settings_button
                    ),
                )

            if has_update:
                btn_size = 75 if has_settings else 100
                update_x = sub_width - (224 if has_settings else 130)
                update_button = bui.buttonwidget(
                    parent=self._subcontainer,
                    id=(
                        f'{self.main_window_id_prefix}'
                        f'|update.{classpath}'
                    ),
                    label='Update',
                    autoselect=True,
                    size=(btn_size, 40),
                    position=(update_x, item_y + 6),
                )
                bui.buttonwidget(
                    edit=update_button,
                    on_activate_call=bui.CallStrict(
                        self._show_update, classpath, update_button
                    ),
                )

            right_widget = None
            if update_button is not None:
                right_widget = update_button
            elif settings_button is not None:
                right_widget = settings_button

            if num_shown == 0:
                bui.widget(
                    edit=check,
                    up_widget=self._back_button,
                    left_widget=self._back_button,
                    right_widget=(
                        self._settings_button
                        if right_widget is None
                        else right_widget
                    ),
                )
                if settings_button is not None:
                    bui.widget(
                        edit=settings_button,
                        up_widget=self._back_button,
                    )
                if update_button is not None:
                    bui.widget(
                        edit=update_button,
                        up_widget=self._back_button,
                    )

            bui.widget(
                edit=check, show_buffer_top=40, show_buffer_bottom=40
            )
            num_shown += 1

        bui.textwidget(
            edit=self._num_plugins_text,
            text=str(num_shown),
        )

        if num_shown == 0:
            bui.textwidget(
                edit=self._no_plugins_installed_text,
                text=bui.Lstr(resource='noPluginsInstalledText'),
            )

    def _show_update(
        self, classpath: str, source_widget: bui.Widget
    ) -> None:
        module_name = classpath.split('.')[0]
        try:
            module = importlib.import_module(module_name)
            module.UpdateWindow(start_check=True)
        except Exception:
            bui.screenmessage(
                'Update check failed.', color=(1, 0, 0)
            )
            bui.getsound('error').play()


_pending_updates: list[str] = []


def _check_mod_version(class_path: str) -> dict | None:
    module_name = class_path.split('.')[0]
    try:
        module = importlib.import_module(module_name)
        for fn_name in ('_cv', 'check_version_blocking', 'check_version'):
            func = getattr(module, fn_name, None)
            if func is not None:
                return func()
    except Exception:
        pass
    return None


def _check_all_updates_background() -> None:
    global _pending_updates
    _pending_updates = []
    plugspecs = bui.app.plugins.plugin_specs
    for classpath, plugspec in plugspecs.items():
        if not plugspec.enabled or not _plugin_has_update(classpath):
            continue
        info = _check_mod_version(classpath)
        if info and info.get('update_available'):
            _pending_updates.append(
                f"{classpath} (v{info.get('current_version')} → "
                f"v{info.get('remote_version')})"
            )
    if _pending_updates:
        babase.pushcall(_show_updates_notification,
                        from_other_thread=True)


def _show_updates_notification() -> None:
    bui.getsound('dingSmallHigh').play()
    for update in _pending_updates:
        bui.screenmessage(
            f'Update available: {update}',
            color=(0.0, 1.0, 0.5),
        )


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def __init__(self):
        import bauiv1lib.settings.plugins as plugins_mod
        plugins_mod.PluginWindow = LessPluginWindow

    def on_app_running(self) -> None:
        threading.Thread(
            target=_check_all_updates_background, daemon=True
        ).start()
