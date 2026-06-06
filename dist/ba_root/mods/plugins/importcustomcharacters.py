# ba_meta require api 9

from __future__ import annotations

import json
import os

import _babase
from typing import TYPE_CHECKING
from efro.terminal import Clr

from bascenev1lib.actor.spazappearance import Appearance

if TYPE_CHECKING:
    pass

def register_character_json(name, character):
    appearance = Appearance(name)
    appearance.color_texture = character['color_texture']
    appearance.color_mask_texture = character['color_mask']
    appearance.default_color = (0.6, 0.6, 0.6)
    appearance.default_highlight = (0, 1, 0)
    appearance.icon_texture = character['icon_texture']
    appearance.icon_mask_texture = character['icon_mask_texture']
    appearance.head_mesh = character['head']
    appearance.torso_mesh = character['torso']
    appearance.pelvis_mesh = character['pelvis']
    appearance.upper_arm_mesh = character['upper_arm']
    appearance.forearm_mesh = character['forearm']
    appearance.hand_mesh = character['hand']
    appearance.upper_leg_mesh = character['upper_leg']
    appearance.lower_leg_mesh = character['lower_leg']
    appearance.toes_mesh = character['toes_mesh']
    appearance.jump_sounds = character['jump_sounds']
    appearance.attack_sounds = character['attack_sounds']
    appearance.impact_sounds = character['impact_sounds']
    appearance.death_sounds = character['death_sounds']
    appearance.pickup_sounds = character['pickup_sounds']
    appearance.fall_sounds = character['fall_sounds']
    appearance.style = character['style']


def enable() -> None:
    characters_dir = os.path.join(_babase.env()["python_directory_user"],
                        "characters" + os.sep)
    
    json_files = [f for f in os.listdir(characters_dir) if f.endswith(".json")]

    if not json_files:
        #print("No se encontraron personajes disponibles.")
        return

    success = True
    for json_file in json_files:
        character_name = os.path.splitext(json_file)[0]
        json_path = os.path.join(characters_dir, json_file)

        try:
            with open(json_path, "r") as f:
                character_data = json.load(f)
            register_character_json(character_name, character_data)
        except Exception as e:
            success = False
            break

    #if success:
    #    print(
    #        f'{Clr.BBLK}{Clr.WHT}\nTodos los personajes fueron importados correctamente.{Clr.BBLK}',
    #    flush=True)
    #else:
    #    print(
    #        f'{Clr.RED}{Clr.WHT}\nOcurrió un error al importar los personajes.{Clr.RED}',
    #    flush=True)