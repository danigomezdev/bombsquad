# ba_meta require api 9
# ba_meta name Ice Man
# ba_meta description A mod that provides your character with ice abilities, special effects, and more
# ba_meta version 1.1.2

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bauiv1
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spaz import Spaz, PunchHitMessage
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.actor.spazbot import SpazBot
from bascenev1lib.actor.bomb import BombFactory
from bauiv1lib import popup
import bascenev1

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