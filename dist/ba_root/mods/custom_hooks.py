# ba_meta require api 9
"""Custom hooks to pull of the in-game functions."""

from __future__ import annotations

import _thread
import importlib
import logging
import os
import time
from datetime import datetime

import _babase
from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
import _bascenev1
from baclassic._appmode import ClassicAppMode
import bauiv1 as bui
import setting
from baclassic._servermode import ServerController
from bascenev1._activitytypes import ScoreScreenActivity
from bascenev1._map import Map
from bascenev1._session import Session
from bascenev1lib.activity import dualteamscore, multiteamscore, drawscore
from bascenev1lib.activity.coopscore import CoopScoreScreen
from bascenev1lib.actor import playerspaz
#from spazmod import modifyspaz
from tools import (
    servercontroller
)
from chathandle import handlechat


if TYPE_CHECKING:
    from typing import Any

settings = setting.get_settings_data()
org_end = bs._activity.Activity.end

def new_end(self, results: Any = None,
            delay: float = 0.0, force: bool = False):
    """Runs when game is ended."""
    activity = bs.get_foreground_host_activity()

    if isinstance(activity, CoopScoreScreen):
        #team_balancer.checkToExitCoop()
        pass
    org_end(self, results, delay, force)


bs._activity.Activity.end = new_end
org_player_join = bs._activity.Activity.on_player_join


def night_mode() -> None:
    """Checks the time and enables night mode."""

    if settings['autoNightMode']['enable']:

        start = datetime.strptime(
            settings['autoNightMode']['startTime'], "%H:%M")
        end = datetime.strptime(settings['autoNightMode']['endTime'], "%H:%M")
        now = datetime.now()

        if now.time() > start.time() or now.time() < end.time():
            activity = bs.get_foreground_host_activity()

            activity.globalsnode.tint = (0.5, 0.7, 1.0)

            if settings['autoNightMode']['fireflies']:
                try:
                    activity.fireflies_generator(
                        20, settings['autoNightMode']["fireflies_random_color"])
                except:
                    pass


def kick_vote_started(started_by: str, started_to: str) -> None:
    """Logs the kick vote."""
    #logger.log(f"{started_by} started kick vote for {started_to}.")


def on_kicked(account_id: str) -> None:
    """Runs when someone is kicked by kickvote."""
    #logger.log(f"{account_id} kicked by kickvotes.")


def on_kick_vote_end():
    """Runs when kickvote is ended."""
    #logger.log("Kick vote End")

def shutdown(func) -> None:
    """Set the app to quit either now or at the next clean opportunity."""

    def wrapper(*args, **kwargs):
        # add screen text and tell players we are going to restart soon.
        bs.chatmessage(
            "El servidor se reiniciará en la próxima oportunidad. (fin de la serie)")
        _babase.restart_scheduled = True
        bs.get_foreground_host_activity().restart_msg = bs.newnode(
            'text',
            attrs={
                'text': "El servidor se reiniciará después de esta serie.",
                'flatness': 1.0,
                'h_align': 'right',
                'v_attach': 'bottom',
                'h_attach': 'right',
                'scale': 0.5,
                'position': (
                    -25,
                    54),
                'color': (
                    1,
                    0.5,
                    0.7)
            })
        func(*args, **kwargs)

    return wrapper


ServerController.shutdown = shutdown(ServerController.shutdown)

#def playerspaz_init(playerspaz: bs.Player, node: bs.Node, player: bs.Player):
#    """Runs when player is spawned on map."""
#    modifyspaz.main(playerspaz, node, player)


def on_access_check_response(self, data):
    if data is not None:
        addr = data['address']
        port = data['port']
        if settings["ballistica_web"]["enable"]:
            bs.set_public_party_stats_url(
                f'https://discord.gg/q5GdnP85Ky')

    servercontroller._access_check_response(self, data)


ServerController._access_check_response = on_access_check_response

def filter_chat_message(msg: str, client_id: int) -> str | None:
    """Returns all in game messages or None (ignore's message)."""
    print("Activando chat..")
    print(f"[DEBUG] Mensaje recibido: {msg} de {client_id}")
    return handlechat.filter_chat_message(msg, client_id)

# ba_meta export babase.Plugin
class modSetup(babase.Plugin):
    def on_app_running(self):
        """Runs when app is launched."""
        print("Server is running , lets save cache")
        pass

    # it works sometimes , but it blocks shutdown so server raise runtime
    # exception,   also dump server logs
    def on_app_shutdown(self):
        print("Server shutting down , lets save cache")