# ba_meta require api 9

from typing import List, Dict, Any

import babase
import bauiv1 as bui

original_get_store_layout = bui.app.classic.store.get_store_layout

def add_special_characters(layout:
                           Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    special_characters = [
        'characters.bunny',
        'characters.taobaomascot',
        'characters.santa'
    ]
    for character in special_characters:
        if character not in layout['characters'][0]['items']:
            layout['characters'][0]['items'].append(character)


def add_special_minigames(layout:
                          Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    special_minigames = [
        'games.easter_egg_hunt',
    ]
    for minigame in special_minigames:
        if minigame not in layout['minigames'][0]['items']:
            layout['minigames'][0]['items'].append(minigame)


def modified_get_store_layout() -> Dict[str, List[Dict[str, Any]]]:
    layout = original_get_store_layout()
    add_special_characters(layout)
    add_special_minigames(layout)
    return layout


# ba_meta export babase.Plugin
class Main(babase.Plugin):
    def on_app_running(self) -> None:
        bui.app.classic.store.get_store_layout = modified_get_store_layout