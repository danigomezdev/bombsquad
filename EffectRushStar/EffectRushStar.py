# ba_meta require api 9
# ba_meta name Effect Rush Star
# ba_meta description A mod that creates a flashy star that floats around the map

from __future__ import annotations
from typing import TYPE_CHECKING, cast

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

# ba_meta export babase.Plugin
class byLess(babase.Plugin):
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