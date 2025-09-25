# ba_meta require api 9

from __future__ import annotations
from typing import TYPE_CHECKING

import babase
import bauiv1 as bui
import bascenev1 as bs
import _babase
import random
from bascenev1lib.actor.spaz import Spaz

if TYPE_CHECKING:
    from typing import Any, Type, Optional, Tuple, List, Dict

# ba_meta export babase.Plugin
class UwUuser(babase.Plugin):
    Spaz._old_init = Spaz.__init__
    def _new_init(self,
                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 source_player: bs.Player = None,
                 start_invincible: bool = True,
                 can_accept_powerups: bool = True,
                 powerups_expire: bool = False,
                 demo_mode: bool = True):
        self._old_init(color,highlight,character,source_player,
                       start_invincible,can_accept_powerups,
                       powerups_expire,demo_mode)

        def emit() -> None:
            bs.emitfx(position=self.node.position,
                      velocity=self.node.velocity,
                      count=10,
                      scale=2,
                      spread=0.10,
                      chunk_type="spark")
        bs.timer(0.3, emit, repeat=True)
    Spaz.__init__ = _new_init
