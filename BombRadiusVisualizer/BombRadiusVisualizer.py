# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

# Let's import everything we need and nothing more.
import babase
import bascenev1
import random
from bascenev1lib.actor.bomb import Bomb

if TYPE_CHECKING:
    pass

# Global list to store all pumps with display
bombs_with_visualization = []

def change_bomb_colors():
    """Function that changes the colors of all bombs every 0.5 seconds"""
    global bombs_with_visualization
    
    # Filter bombs that no longer exist
    bombs_with_visualization = [bomb for bomb in bombs_with_visualization 
                               if bomb.node and bomb.node.exists()]
    
    for bomb in bombs_with_visualization:
        if (hasattr(bomb, 'radius_visualizer') and 
            bomb.radius_visualizer and bomb.radius_visualizer.exists() and
            hasattr(bomb, 'radius_visualizer_circle') and 
            bomb.radius_visualizer_circle and bomb.radius_visualizer_circle.exists()):
            
            # Generate random RGB colors (similar to the first mod)
            R_fill = random.uniform(0.0, 1.0)
            G_fill = random.uniform(0.0, 1.0)
            B_fill = random.uniform(0.0, 1.0)
            
            R_outline = random.uniform(0.0, 1.0)
            G_outline = random.uniform(0.0, 1.0)
            B_outline = random.uniform(0.0, 1.0)
            
            # Apply new colors
            bomb.radius_visualizer.color = (R_fill, G_fill, B_fill)
            bomb.radius_visualizer_circle.color = (R_outline, G_outline, B_outline)

# Global timer to change colors every 0.5 seconds
color_timer = babase.AppTimer(0.5, change_bomb_colors, repeat=True)

# ba_meta export babase.Plugin
class byLess(babase.Plugin):

    def new_bomb_init(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

            args[0].radius_visualizer = bascenev1.newnode('locator',
                                                   owner=args[0].node,
                                                   attrs={
                                                       'shape': 'circle',
                                                       'color': (0, 0, 1),
                                                       'opacity': 0.05,
                                                       'draw_beauty': False,
                                                       'additive': False
                                                   })
            args[0].node.connectattr('position', args[0].radius_visualizer, 'position')

            bascenev1.animate_array(args[0].radius_visualizer, 'size', 1, {
                0.0: [0.0],
                0.2: [args[0].blast_radius * 2.2],
                0.25: [args[0].blast_radius * 2.0]
            })

            args[0].radius_visualizer_circle = bascenev1.newnode('locator',
                                                          owner=args[0].node,
                                                          attrs={
                                                              'shape': 'circleOutline',
                                                              'size': [args[0].blast_radius * 2.0],
                                                              'color': (1, 1, 1),
                                                              'draw_beauty': False,
                                                              'additive': True
                                                          })
            args[0].node.connectattr('position', args[0].radius_visualizer_circle, 'position')

            bascenev1.animate(
                args[0].radius_visualizer_circle, 'opacity', {
                    0: 0.0,
                    0.4: 0.1
                })
            
            # Add this pump to the global list for color changing
            bombs_with_visualization.append(args[0])
            
        return wrapper
    
    Bomb.__init__ = new_bomb_init(Bomb.__init__)