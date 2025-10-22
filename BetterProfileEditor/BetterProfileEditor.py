# ba_meta require api 9
# ba_meta name Better Profile Editor
# ba_meta version 1.5
# ba_meta description Advanced viewer of your Bombsquad profiles, with a live character that updates based on your profile choices

from __future__ import annotations

from typing import override, Any

import random
import functools

import babase
import bauiv1 as bui
import bascenev1 as bs

from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.mainmenu import MainMenuActivity, MainMenuSession

from bauiv1lib.profile.edit import EditProfileWindow
import bauiv1lib.profile.browser as ProfileBrowserFile
from bauiv1lib.profile.browser import ProfileBrowserWindow


INVOKE_MM_UI = True
OLD_INVOKE_MM_UI_FUNC = bs.app.classic.invoke_main_menu_ui


def invoke_main_menu_ui():
    global INVOKE_MM_UI, OLD_INVOKE_MM_UI_FUNC
    if INVOKE_MM_UI:
        OLD_INVOKE_MM_UI_FUNC()
    INVOKE_MM_UI = True


class ProfileSpaz(Spaz):
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.OutOfBoundsMessage):
            activity = bs.get_foreground_host_activity()
            with activity.context:
                activity.set_character(activity.character)
                activity.set_color(activity.color)
                activity.set_highlight(activity.highlight)
        return super().handlemessage(msg)


class BetterProfileActivity(bs.Activity[bs.Player, bs.Team]):
    """Activity showing the rotating main menu bg stuff."""

    _stdassets = bs.Dependency(bs.AssetPackage, 'stdassets@1')

    def __init__(self, settings: dict):
        super().__init__(settings)

        self.spaz: ProfileSpaz | None = None
        self.character: str = 'Spaz'
        self.color: tuple[float, float, float] = (1.0, 1.0, 1.0)
        self.highlight: tuple[float, float, float] = (0.5, 0.5, 0.5)

    @override
    def on_transition_in(self) -> None:
        super().on_transition_in()

        # DARK BACKGROUND - Dark solid color
        self.bgterrain = bs.NodeActor(
            bs.newnode(
                'terrain',
                attrs={
                    'mesh': bs.getmesh('thePadBG'),
                    'color': (0.1, 0.05, 0.1),  # Dark color
                    'lighting': False,
                    'background': True,
                },
            )
        )

        bs.set_map_bounds((-99, -99, -99, 99, 99, 99))

        shared = SharedObjects.get()
        self._pmat = bs.Material()
        self._rmat = bs.Material()
        self._pmat.add_actions(('modify_part_collision', 'collide', False))
        self._rmat.add_actions(
            conditions=('they_dont_have_material', shared.player_material),
            actions=('modify_part_collision', 'collide', False)
        )
        self._rmat.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', True)
            )
        )

        # COLLISION REGION
        bs.newnode(
            'region',
            attrs={
                'position': (0, 16, 16),
                'scale': (2, 1.3, 2),
                'type': 'box',
                'materials': (shared.footing_material, self._rmat)
            },
        )

        self.platform = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'box',
                'position': (0, 16, 16),
                'mesh': bs.getmesh("cylinder"),
                'color_texture': bs.gettexture('shield'),
                'gravity_scale': 0.0,
                'materials': (self._pmat,)
            },
        )

        bs.setmusic(bs.MusicType.GRAND_ROMP)

        # Create initial spaz immediately
        with self.context:
            self.set_character(self.character)

    def set_character(self, name: str) -> None:
        # Remove previous spaz if it exists
        if self.spaz is not None:
            self.spaz.handlemessage(bs.DieMessage(immediate=True))
            if hasattr(self.spaz, 'node') and self.spaz.node:
                self.spaz.node.delete()
        
        self.character = name
        # Create new spaz - same as in the original mod
        self.spaz = ProfileSpaz(character=name, start_invincible=False).autoretain()
        self.spaz.node.is_area_of_interest = False
        
        # Exact position as in the original mod - works perfectly
        self.spaz.handlemessage(bs.StandMessage(position=(0, 16, 16.5), angle=0))

    def set_color(self, color: tuple[float, float, float]) -> None:
        self.color = color
        if self.spaz is not None and hasattr(self.spaz, 'node'):
            self.spaz.node.color = color

    def set_highlight(self, color: tuple[float, float, float]) -> None:
        self.highlight = color
        if self.spaz is not None and hasattr(self.spaz, 'node'):
            self.spaz.node.highlight = color


class NewEditProfileWindow(EditProfileWindow):
    def __init__(
        self,
        existing_profile: str | None,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        assert bui.app.classic is not None
        plus = bui.app.plus
        assert plus is not None

        self._existing_profile = existing_profile
        self._r = 'editProfileWindow'
        self._spazzes: list[str] = []
        self._icon_textures: list[bui.Texture] = []
        self._icon_tint_textures: list[bui.Texture] = []
        (
            self._color,
            self._highlight,
        ) = bui.app.classic.get_player_profile_colors(existing_profile)

        self.session = bs.get_foreground_host_session()
        self.activity = bs.get_foreground_host_activity()
        
        uiscale = bui.app.ui_v1.uiscale
        self._width = width = (400.0
            if uiscale is bui.UIScale.SMALL else 600.0
            if uiscale is bui.UIScale.MEDIUM else  680.0)
        self._height = height = (
            200.0
            if uiscale is bui.UIScale.SMALL
            else 350.0 if uiscale is bui.UIScale.MEDIUM else 450.0
        )
        self._base_scale = (
            2.0
            if uiscale is bui.UIScale.SMALL
            else 1.35 if uiscale is bui.UIScale.MEDIUM else 1.0
        )
        super(EditProfileWindow, self).__init__(
            root_widget=bui.containerwidget(
                size=(0, 0),
                scale=self._base_scale,
                stack_offset=(0, 0),
                toolbar_visibility=None,
            ),
            transition='in_scale',
            origin_widget=origin_widget,
        )
        cancel_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(-width/2 - (100 if uiscale is bui.UIScale.SMALL else 20), height/2),
            size=(155, 60),
            scale=0.8,
            autoselect=True,
            label=bui.Lstr(resource='cancelText'),
            on_activate_call=self._cancel,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=btn)
        save_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(width/2 - (25 if uiscale is bui.UIScale.SMALL else 70), height/2),
            size=(155, 60),
            autoselect=True,
            scale=0.8,
            label=bui.Lstr(resource='saveText'),
        )
        bui.containerwidget(edit=self._root_widget, start_button=btn)
        bui.textwidget(
            parent=self._root_widget,
            position=(0, height/1.5 + (25 if uiscale is bui.UIScale.SMALL else 0)),
            size=(0, 0),
            text=(
                bui.Lstr(resource=f'{self._r}.titleNewText')
                if existing_profile is None
                else bui.Lstr(resource=f'{self._r}.titleEditText')
            ),
            color=(0, 0, 0),
            maxwidth=290,
            scale=1.0,
            h_align='center',
            v_align='center',
        )

        self.refresh_characters()
        profile = bui.app.config.get('Player Profiles', {}).get(
            self._existing_profile, {}
        )

        try:
            self.character = profile['character']
        except:
            self.character = 'Spaz'

       # Initialize the character in the activity
        if self.activity is not None and hasattr(self.activity, 'set_character'):
            with self.activity.context:
                self.activity.set_character(self.character)
                self.activity.set_color(self._color)
                self.activity.set_highlight(self._highlight)

        if 'global' in profile:
            self._global = profile['global']
        else:
            self._global = False

        if 'icon' in profile:
            self._icon = profile['icon']
        else:
            self._icon = bui.charstr(bui.SpecialChar.LOGO)

        assigned_random_char = False
        try:
            icon_index = self._spazzes.index(profile['character'])
        except Exception:
            random.seed()
            icon_index = random.randrange(len(self._spazzes))
            assigned_random_char = True
        self._icon_index = icon_index
        bui.buttonwidget(edit=save_button, on_activate_call=self.save)

        self._name = (
            '' if self._existing_profile is None else self._existing_profile
        )
        self._is_account_profile = self._name == '__account__'

        if assigned_random_char:
            assert bui.app.classic is not None
            clr = bui.app.classic.spaz_appearances[
                self._spazzes[icon_index]
            ].default_color
            if clr is not None:
                self._color = clr
            highlight = bui.app.classic.spaz_appearances[
                self._spazzes[icon_index]
            ].default_highlight
            if highlight is not None:
                self._highlight = highlight

        if self._name == '':
            names = bs.get_random_names()
            self._name = names[random.randrange(len(names))]

        self._clipped_name_text = bui.textwidget(
            parent=self._root_widget,
            text='',
            position=(185, height/2.2),
            flatness=1.0,
            shadow=0.0,
            scale=0.55,
            size=(0, 0),
            maxwidth=100,
            h_align='center',
            v_align='center',
            color=(0, 0, 0),
        )

        info_b_size = (10 if uiscale is bui.UIScale.SMALL else 15)

        self._upgrade_button = None
        if self._is_account_profile:
            if plus.get_v1_account_state() == 'signed_in':
                sval = plus.get_v1_account_display_string()
            else:
                sval = '??'
            bui.textwidget(
                parent=self._root_widget,
                position=(0, height/2 + 20),
                size=(0, 0),
                scale=1.2,
                text=sval,
                maxwidth=270,
                h_align='center',
                v_align='center',
            )
            txtl = bui.Lstr(
                resource='editProfileWindow.accountProfileText'
            ).evaluate()
            bui.textwidget(
                parent=self._root_widget,
                position=(-14, height/2 - 7),
                size=(0, 0),
                scale=(0.5 if uiscale is bui.UIScale.SMALL else 0.6),
                color=(0, 0, 0),
                text=txtl,
                maxwidth=270,
                h_align='center',
                v_align='center',
            )
            self._account_type_info_button = bui.buttonwidget(
                parent=self._root_widget,
                label='?',
                size=(info_b_size, info_b_size),
                text_scale=0.6,
                position=(
                    50 - (10 if uiscale is bui.UIScale.SMALL else 0),
                    height/2 - (10 if uiscale is bui.UIScale.SMALL else 15)
                ),
                button_type='square',
                color=(0.6, 0.5, 0.65),
                autoselect=True,
                on_activate_call=self.show_account_profile_info,
            )
        elif self._global:
            b_size = 40 if uiscale is bui.UIScale.SMALL else 60
            self._icon_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                position=(-width/3, height/3),
                size=(b_size, b_size),
                color=(0.6, 0.5, 0.6),
                label='',
                button_type='square',
                text_scale=1.2,
                on_activate_call=self._on_icon_press,
            )
            self._icon_button_label = bui.textwidget(
                parent=self._root_widget,
                position=(-width/3 + b_size/2, height/3 + b_size/4),
                draw_controller=btn,
                h_align='center',
                v_align='center',
                size=(0, 0),
                color=(1, 1, 1),
                text='',
                scale=2.0,
            )

            bui.textwidget(
                parent=self._root_widget,
                h_align='center',
                v_align='center',
                position=(-width/3 + b_size/2, height/3 - 15),
                size=(0, 0),
                draw_controller=btn,
                text=bui.Lstr(resource=f'{self._r}.iconText'),
                scale=0.7,
                color=(0, 0, 0),
                maxwidth=120,
            )

            self._update_icon()

            bui.textwidget(
                parent=self._root_widget,
                position=(0, height/2 + 20),
                size=(0, 0),
                scale=1.2,
                text=self._name,
                maxwidth=240,
                h_align='center',
                v_align='center',
            )
            txtl = bui.Lstr(
                resource='editProfileWindow.globalProfileText'
            ).evaluate()
            bui.textwidget(
                parent=self._root_widget,
                position=(-14, height/2 - 7),
                size=(0, 0),
                scale=(0.5 if uiscale is bui.UIScale.SMALL else 0.6),
                color=(0, 0, 0),
                text=txtl,
                maxwidth=240,
                h_align='center',
                v_align='center',
            )
            self._account_type_info_button = bui.buttonwidget(
                parent=self._root_widget,
                label='?',
                size=(info_b_size, info_b_size),
                text_scale=0.6,
                position=(
                    50 - (10 if uiscale is bui.UIScale.SMALL else 0),
                    height/2 - (10 if uiscale is bui.UIScale.SMALL else 15)
                ),
                button_type='square',
                color=(0.6, 0.5, 0.65),
                autoselect=True,
                on_activate_call=self.show_global_profile_info,
            )
        else:
            bui.textwidget(
                parent=self._root_widget,
                text=bui.Lstr(resource=f'{self._r}.nameText'),
                position=(
                    -140 + (25 if uiscale is bui.UIScale.SMALL else 0),
                    height/2 + (22.5 if uiscale is bui.UIScale.SMALL else 20)
                ),
                size=(0, 0),
                h_align='right',
                v_align='center',
                color=(0, 0, 0),
                scale=(0.7 if uiscale is bui.UIScale.SMALL else 0.9),
            )

            self._text_field = bui.textwidget(
                parent=self._root_widget,
                position=(-132.5, height/2),
                size=(265, 40),
                text=self._name,
                h_align='center',
                v_align='center',
                max_chars=16,
                description=bui.Lstr(resource=f'{self._r}.nameDescriptionText'),
                autoselect=True,
                editable=True,
                padding=4,
                color=(0.9, 0.9, 0.9, 1.0),
                scale=(0.8 if uiscale is bui.UIScale.SMALL else 1),
                on_return_press_call=bui.Call(save_button.activate),
            )

            txtl = bui.Lstr(
                resource='editProfileWindow.localProfileText'
            ).evaluate()
            bui.textwidget(
                parent=self._root_widget,
                position=(
                    -70 if uiscale is bui.UIScale.SMALL else -80,
                    height/2 - (5 if uiscale is bui.UIScale.SMALL else 10)
                ),
                size=(0, 0),
                scale=(0.5 if uiscale is bui.UIScale.SMALL else 0.6),
                color=(0, 0, 0),
                text=txtl,
                maxwidth=270,
                h_align='center',
                v_align='center',
            )
            self._account_type_info_button = bui.buttonwidget(
                parent=self._root_widget,
                label='?',
                size=(info_b_size, info_b_size),
                text_scale=0.6,
                position=(-20, height/2 - (10 if uiscale is bui.UIScale.SMALL else 20)),
                button_type='square',
                color=(0.6, 0.5, 0.65),
                autoselect=True,
                on_activate_call=self.show_local_profile_info,
            )
            self._upgrade_button = bui.buttonwidget(
                parent=self._root_widget,
                label=bui.Lstr(resource='upgradeText'),
                size=(40, 17),
                text_scale=1.0,
                button_type='square',
                position=(
                    60 if uiscale is bui.UIScale.SMALL else 80,
                    height/2 - (15 if uiscale is bui.UIScale.SMALL else 20)
                ),
                color=(0.6, 0.5, 0.65),
                autoselect=True,
                on_activate_call=self.upgrade_profile,
            )
            self._random_name_button = bui.buttonwidget(
                parent=self._root_widget,
                label=bui.Lstr(resource='randomText'),
                size=(30, 20),
                position=(
                    152 - (37.5 if uiscale is bui.UIScale.SMALL else 0),
                    height/2 + (12.5 if uiscale is bui.UIScale.SMALL else 10)
                ),
                button_type='square',
                color=(0.6, 0.5, 0.65),
                autoselect=True,
                on_activate_call=self.assign_random_name,
            )

        self._update_clipped_name()
        self._clipped_name_timer = bui.AppTimer(
            0.333, bui.WeakCall(self._update_clipped_name), repeat=True
        )

        if not self._is_account_profile and not self._global:
            bui.containerwidget(
                edit=self._root_widget, selected_child=self._text_field
            )

        b_size = 80
        b_size_2 = 100
        self._color_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(
                -self._width/2 - (15 if uiscale is bui.UIScale.SMALL else 0),
                (-35 if uiscale is bui.UIScale.SMALL else 0)
            ),
            size=(b_size, b_size),
            color=self._color,
            label='',
            scale=(0.8 if uiscale is bui.UIScale.SMALL else 1),
            button_type='square',
        )
        origin = self._color_button.get_screen_space_center()
        bui.buttonwidget(
            edit=self._color_button,
            on_activate_call=bui.WeakCall(self._make_picker, 'color', origin),
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align='center',
            v_align='center',
            position=(
                -(self._width - b_size)/2 - (22.5 if uiscale is bui.UIScale.SMALL else 0),
                -b_size/3 - (20 if uiscale is bui.UIScale.SMALL else 0)
            ),
            size=(0, 0),
            draw_controller=btn,
            text=bui.Lstr(resource=f'{self._r}.colorText'),
            scale=0.7,
            color=(0, 0, 0),
            maxwidth=120,
        )

        self._highlight_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(
                (self._width - b_size)/2,
                (-35 if uiscale is bui.UIScale.SMALL else 0)
            ),
            up_widget=(
                self._upgrade_button
                if self._upgrade_button is not None
                else self._account_type_info_button
            ),
            size=(b_size, b_size),
            color=self._highlight,
            label='',
            scale=(0.8 if uiscale is bui.UIScale.SMALL else 1),
            button_type='square',
        )

        origin = self._highlight_button.get_screen_space_center()
        bui.buttonwidget(
            edit=self._highlight_button,
            on_activate_call=bui.WeakCall(
                self._make_picker, 'highlight', origin
            ),
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align='center',
            v_align='center',
            position=(
                (self._width)/2 - (7.5 if uiscale is bui.UIScale.SMALL else 0),
                -b_size/3 - (20 if uiscale is bui.UIScale.SMALL else 0)
            ),
            size=(0, 0),
            draw_controller=btn,
            text=bui.Lstr(resource=f'{self._r}.highlightText'),
            scale=0.7,
            color=(0, 0, 0),
            maxwidth=120,
        )

        self._characters_shown = []
        for i in range(0, 3):
            d = 100 if uiscale is bui.UIScale.SMALL else 140
            m = 10 if (uiscale is bui.UIScale.SMALL and i == 1) else 0
            self._characters_shown.append([
                bui.buttonwidget(
                    parent=self._root_widget,
                    autoselect=True,
                    position=(
                        -b_size_2/2 * (
                            0.8 if uiscale is bui.UIScale.SMALL else 1
                        ) + (i - 1) * d + abs(i - 1) * (b_size_2 - 30)/4 + m,
                        -(height + b_size_2)/2 + abs(i - 1) * (b_size_2 - 30)/4
                    ),
                    up_widget=self._account_type_info_button,
                    on_activate_call=functools.partial(self._on_character_press, i-1),
                    size=(b_size_2 - abs(i - 1) * 30, b_size_2 - abs(i - 1) * 30),
                    label='',
                    color=(1, 1, 1),
                    scale=0.65 if uiscale is bui.UIScale.SMALL else 1,
                    mask_texture=bui.gettexture('characterIconMask'),
                ),
                bui.textwidget(
                    parent=self._root_widget,
                    h_align='center',
                    v_align='center',
                    position=((i - 1) * d, -(height + b_size_2)/2 - (20 if i==1 else 0) + m/2),
                    size=(0, 0),
                    draw_controller=btn,
                    text='',
                    scale=(0.5 if uiscale is bui.UIScale.SMALL else 0.7),
                    color=(0, 0, 0),
                    maxwidth=130,
                )
            ])

        bui.widget(edit=cancel_button, down_widget=self._color_button)
        bui.widget(edit=save_button, down_widget=self._highlight_button)
        bui.widget(
            edit=self._color_button,
            up_widget=cancel_button,
            down_widget=self._characters_shown[0][0],
            left_widget=None,
            right_widget=self._highlight_button,
        )
        bui.widget(
            edit=self._highlight_button,
            up_widget=save_button,
            down_widget=self._characters_shown[2][0],
            left_widget=self._color_button,
            right_widget=None,
        )
        bui.widget(
            edit=self._characters_shown[0][0],
            up_widget=self._color_button,
            down_widget=None,
            left_widget=None,
            right_widget=self._characters_shown[1][0],
        )
        bui.widget(
            edit=self._characters_shown[1][0],
            up_widget=self._color_button,
            down_widget=None,
            left_widget=self._characters_shown[0][0],
            right_widget=self._characters_shown[2][0],
        )
        bui.widget(
            edit=self._characters_shown[2][0],
            up_widget=self._highlight_button,
            down_widget=None,
            left_widget=self._characters_shown[1][0],
            right_widget=None,
        )
        if self._is_account_profile:
            bui.widget(edit=cancel_button, right_widget=self._account_type_info_button)
            bui.widget(edit=save_button, left_widget=self._account_type_info_button)
            bui.widget(
                edit=self._account_type_info_button,
                up_widget=None,
                down_widget=self._characters_shown[1][0],
                left_widget=cancel_button,
                right_widget=save_button,
            )
        if not self._is_account_profile and not self._global:
            bui.widget(edit=cancel_button, right_widget=self._text_field)
            bui.widget(edit=save_button, left_widget=self._random_name_button)
            bui.widget(edit=self._account_type_info_button, right_widget=self._upgrade_button)

        self._update_character()

    def reload_window(self) -> None:
        """Transitions out and recreates ourself."""

        # no-op if we're not in control.
        if not self.main_window_has_control():
            return

        # Replace ourself with ourself, but keep the same back location.
        assert self.main_window_back_state is not None

        session = bs.get_foreground_host_session()
        self.main_window_replace(
            (
                NewEditProfileWindow(self.getname())
                if isinstance(session, MainMenuSession) else
                EditProfileWindow(self.getname())
            ),
            back_state=self.main_window_back_state,
        )

    def _on_character_press(self, num: int = 0) -> None:
        if num < 0:
            self._update_character(len(self._spazzes) + num)
        else:
            self._update_character(num)

    def _update_character(self, change: int = 0) -> None:
        length = len(self._spazzes)
        self._icon_index = index = (self._icon_index + change) % length
        for i, character in enumerate(self._characters_shown):
            character_button, character_text = character
            ind = length-1 if (index==0 and i==0) else (index + (i - 1))%length
            if character_button:
                bui.buttonwidget(
                    edit=character_button,
                    texture=self._icon_textures[ind],
                    tint_texture=self._icon_tint_textures[ind],
                    tint_color=self._color,
                    tint2_color=self._highlight,
                )
            if character_text:
                bui.textwidget(
                    edit=character_text,
                    text=self._spazzes[ind],
                )
        
        # Update the character in the activity with secure checks
        if self.activity is not None and hasattr(self.activity, 'set_character'):
            with self.activity.context:
                new_character = self._spazzes[self._icon_index]
                if hasattr(self.activity, 'character') and self.activity.character != new_character:
                    self.activity.set_character(name=new_character)
                    self.activity.character = new_character
                
                if hasattr(self.activity, 'set_color'):
                    self.activity.set_color(self._color)
                if hasattr(self.activity, 'set_highlight'):
                    self.activity.set_highlight(self._highlight)

    def _cancel(self) -> None:
        self.main_window_back()
        global INVOKE_MM_UI
        with self.session.context:
            INVOKE_MM_UI = False
            self.session.setactivity(bs.newactivity(MainMenuActivity))

    def save(self, transition_out: bool = True) -> bool:
        value = super().save(transition_out)
        global INVOKE_MM_UI
        with self.session.context:
            if transition_out:
                INVOKE_MM_UI = False
                self.session.setactivity(bs.newactivity(MainMenuActivity))
        return value


class NewProfileBrowserWindow(ProfileBrowserWindow):
    def _new_profile(self) -> None:
        session = bs.get_foreground_host_session()
        with session.context:
            if isinstance(session, MainMenuSession):
                session.setactivity(bs.newactivity(BetterProfileActivity))

        if not self.main_window_has_control():
            return
        assert self._profiles is not None
        if len(self._profiles) > 100:
            bui.screenmessage(bui.Lstr(translate=(
                'serverResponses', 'Max number of profiles reached.',
                )),
                color=(1, 0, 0),
            )
            bui.getsound('error').play()
            return

        if isinstance(session, MainMenuSession):
            self.main_window_replace(NewEditProfileWindow(existing_profile=None))
        else:
            self.main_window_replace(EditProfileWindow(existing_profile=None))

    def _edit_profile(self) -> None:
        session = bs.get_foreground_host_session()
        with session.context:
            if isinstance(session, MainMenuSession):
                session.setactivity(bs.newactivity(BetterProfileActivity))

        if not self.main_window_has_control():
            return
        if self._selected_profile is None:
            bui.getsound('error').play()
            bui.screenmessage(
                bui.Lstr(resource='nothingIsSelectedErrorText'), color=(1, 0, 0)
            )
            return

        if isinstance(session, MainMenuSession):
            self.main_window_replace(NewEditProfileWindow(self._selected_profile))
        else:
            self.main_window_replace(EditProfileWindow(self._selected_profile))


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def __init__(self):
        ProfileBrowserFile.ProfileBrowserWindow = NewProfileBrowserWindow
        bs.app.classic.invoke_main_menu_ui = invoke_main_menu_ui