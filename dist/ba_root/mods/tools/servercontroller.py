import _babase
from typing import TYPE_CHECKING

import bascenev1 as bs
from efro.terminal import Clr
import bauiv1 as bui
import babase
if TYPE_CHECKING:
    pass

from bascenev1lib.actor.spazappearance import *
import json
import os

def _access_check_response(self, data) -> None:
    if data is None:
        print('Error en la comprobación de acceso al puerto UDP (¿Internet caído?)')
    else:
        addr = data['address']
        port = data['port']

        addrstr = f' {addr}'
        poststr = ''
        _babase.our_ip = addr
        _babase.our_port = port

        # Show Bombsquad logo art
        os.system("cat ../art.txt")
        
        print(
            f'\n{Clr.BGRN}{Clr.WHT} Servidor iniciado {addr}:{port} {Clr.RST}',
            flush=True)
        if data['accessible']:
            # _fetch_public_servers()
            _babase.queue_chcker_timer = bs.AppTimer(8, babase.Call(
                simple_queue_checker), repeat=True)
            print(
                f"{Clr.SBLU}Comprobación del acceso al servidor maestro "
                f"\033[4m{addrstr}{Clr.RST}{Clr.SBLU} "
                f"puerto udp \033[4m{port}{Clr.RST}{Clr.SBLU} tuvo éxito.\n"
                f"Parece que su servidor está Unible desde internet. {poststr}{Clr.RST}"
            )

            if self._config.party_is_public:
                print(
                    f"{Clr.SBLU}Tu fiesta "
                    f"{Clr.BGRN}{Clr.WHT}{self._config.party_name}{Clr.RST}"
                    f"{Clr.SBLU} visible en la lista de partidas públicas.{Clr.RST}",
                    flush=True
                )
                import_characters()
            else:
                print(
                    f'{Clr.SBLU}Tu fiesta privada {self._config.party_name}'
                    f'Se pueden unir mediante {addrstr} {port}.{Clr.RST}'
                )
        else:
            print(
                f'{Clr.SRED}Comprobación del acceso al servidor maestro{addrstr}'
                f' puerto udp  {port} falló.\n'
                f'Su servidor no parece estar'
                f' Se puede acceder desde internet. Verifique su firewall o grupo de seguridad de instancia.{
                    poststr}{Clr.RST}'
            )


def _fetch_public_servers():
    bui.app.plus.add_v1_account_transaction(
        {
            'type': 'PUBLIC_PARTY_QUERY',
            'proto': bui.app.protocol_version,
            'lang': bs.app.lang.language,
        },
        callback=bui.WeakCall(_on_public_party_response),
    )
    bui.app.plus.run_v1_account_transactions()

def import_characters():
    characters_dir = "/home/archblue1001/teams-test/dist/ba_root/mods/CHARACTERS"

    json_files = [f for f in os.listdir(characters_dir) if f.endswith(".json")]

    if not json_files:
        print("No se encontraron personajes disponibles.")
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

    if success:
        print(
            f'{Clr.BBLK}{Clr.WHT}\nTodos los personajes fueron importados correctamente.{Clr.BBLK}',
        flush=True)
    else:
        print(
            f'{Clr.RED}{Clr.WHT}\nOcurrió un error al importar los personajes.{Clr.RED}',
        flush=True)

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

def _on_public_party_response(result):
    if result is None:
        return
    parties_in = result['l']
    queue_id = None
    for party_in in parties_in:
        addr = party_in['a']
        assert isinstance(addr, str)
        port = party_in['p']
        assert isinstance(port, int)
        if addr == _babase.our_ip and str(port) == str(_babase.our_port):
            queue_id = party_in['q']
    #  aah sad , public party result dont include our own server
    if queue_id:
        _babase.our_queue_id = queue_id
        _babase.queue_chcker_timer = bs.timer(6, babase.Call(check_queue),
                                              repeat=True)
    else:
        print("Algo anda mal, ¿por qué nuestro servidor no está en la lista pública?")


def check_queue():
    bui.app.plus.add_v1_account_transaction(
        {'type': 'PARTY_QUEUE_QUERY', 'q': _babase.our_queue_id},
        callback=babase.Call(on_update_response),
    )
    bui.app.plus.run_v1_account_transactions()
    # lets dont spam our own queue
    bui.app.plus.add_v1_account_transaction(
        {'type': 'PARTY_QUEUE_REMOVE', 'q': _babase.our_queue_id}
    )
    bui.app.plus.run_v1_account_transactions()


def on_update_response(response):
    allowed_to_join = response["c"]
    players_in_queue = response["e"]
    max_allowed_in_server = babase.app.classic.server._config.max_party_size
    current_players = len(bs.get_game_roster())
    # print(allowed_to_join)
    if allowed_to_join:
        #  looks good , yipee
        bs.set_public_party_queue_enabled(True)
        return
    if not allowed_to_join and len(
            players_in_queue) > 1 and current_players < max_allowed_in_server:
        #  something is wrong , lets disable queue for some time
        bs.set_public_party_queue_enabled(False)


def simple_queue_checker():
    max_allowed_in_server = babase.app.classic.server._config.max_party_size
    current_players = len(bs.get_game_roster())

    if current_players < max_allowed_in_server:
        bs.set_public_party_queue_enabled(False)
    else:
        bs.set_public_party_queue_enabled(True)
