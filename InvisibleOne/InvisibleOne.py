# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bauiv1 as bui
import bascenev1 as bs
from bascenev1lib.actor.flag import Flag
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Optional, Sequence, Union


class Player(bs.Player['Team']):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.chosen_light: Optional[bs.NodeActor] = None


class Team(bs.Team[Player]):
    """Our team type for this game."""

    def __init__(self, time_remaining: int) -> None:
        self.time_remaining = time_remaining


# ba_meta export bascenev1.GameActivity
class InvicibleOneGame(bs.TeamGameActivity[Player, Team]):
    """
    Game involving trying to remain the one 'invisible one'
    for a set length of time while everyone else tries to
    kill you and become the invisible one themselves.
    """

    name = 'Invisible One'
    description = ('Be the invisible one for a length of time to win.\n'
                   'Kill the invisible one to become it.')
    available_settings = [
        bs.IntSetting(
            'Invicible One Time',
            min_value=10,
            default=30,
            increment=10,
        ),
        bs.BoolSetting('Invicible one is lazy', default=True),
        bs.BoolSetting('Night mode', default=False),
        bs.IntChoiceSetting(
            'Time Limit',
            choices=[
                ('None', 0),
                ('1 Minute', 60),
                ('2 Minutes', 120),
                ('5 Minutes', 300),
                ('10 Minutes', 600),
                ('20 Minutes', 1200),
            ],
            default=0,
        ),
        bs.FloatChoiceSetting(
            'Respawn Times',
            choices=[
                ('Shorter', 0.25),
                ('Short', 0.5),
                ('Normal', 1.0),
                ('Long', 2.0),
                ('Longer', 4.0),
            ],
            default=1.0,
        ),
        bs.BoolSetting('Epic Mode', default=False),
    ]
    scoreconfig = bs.ScoreConfig(label='Time Held')

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        return bs.app.classic.getmaps('keep_away')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._invicible_one_player: Optional[Player] = None
        self._swipsound = bui.getsound('swip')
        self._countdownsounds: Dict[int, babase.Sound] = {
            10: bui.getsound('announceTen'),
            9: bui.getsound('announceNine'),
            8: bui.getsound('announceEight'),
            7: bui.getsound('announceSeven'),
            6: bui.getsound('announceSix'),
            5: bui.getsound('announceFive'),
            4: bui.getsound('announceFour'),
            3: bui.getsound('announceThree'),
            2: bui.getsound('announceTwo'),
            1: bui.getsound('announceOne')
        }
        self._flag_spawn_pos: Optional[Sequence[float]] = None
        self._reset_region_material: Optional[bs.Material] = None
        self._flag: Optional[Flag] = None
        self._reset_region: Optional[bs.Node] = None
        self._epic_mode = bool(settings['Epic Mode'])
        self._invicible_one_time = int(settings['Invicible One Time'])
        self._time_limit = float(settings['Time Limit'])
        self._invicible_one_is_lazy = bool(settings['Invicible one is lazy'])
        self._night_mode = bool(settings['Night mode'])

        # Base class overrides
        self.slow_motion = self._epic_mode
        self.default_music = (bs.MusicType.EPIC
                              if self._epic_mode else bs.MusicType.CHOSEN_ONE)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Show your invisibility powers.'

    def create_team(self, sessionteam: bs.SessionTeam) -> Team:
        return Team(time_remaining=self._invicible_one_time)

    def on_team_join(self, team: Team) -> None:
        self._update_scoreboard()

    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        if self._get_invicible_one_player() is player:
            self._set_invicible_one_player(None)

    def on_begin(self) -> None:
        super().on_begin()
        print("[Game] on_begin() called. Starting game initialization...")

        shared = SharedObjects.get()
        print("[Game] SharedObjects loaded.")

        self.setup_standard_time_limit(self._time_limit)
        print(f"[Game] Time limit set to {self._time_limit} seconds.")

        self.setup_standard_powerup_drops()
        print("[Game] Standard powerup drops enabled.")

        self._flag_spawn_pos = self.map.get_flag_position(None)
        print(f"[Game] Flag spawn position: {self._flag_spawn_pos}")

        Flag.project_stand(self._flag_spawn_pos)
        print("[Game] Flag stand projected at spawn position.")

        self._set_invicible_one_player(None)
        print("[Game] No invincible player at start. Flag will be available.")

        if self._night_mode:
            gnode = bs.getactivity().globalsnode
            gnode.tint = (0.4, 0.4, 0.4)
            print("[Game] Night mode enabled. Tint applied to globalsnode.")

        pos = self._flag_spawn_pos
        bs.timer(1.0, call=self._tick, repeat=True)
        print("[Game] Tick timer started (interval = 1s).")

        mat = self._reset_region_material = bs.Material()
        mat.add_actions(
            conditions=(
                'they_have_material',
                shared.player_material,
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect',
                 bs.WeakCall(self._handle_reset_collide)),
            ),
        )
        print("[Game] Reset region material created with collision actions.")

        self._reset_region = bs.newnode('region',
                                        attrs={
                                            'position': (pos[0], pos[1] + 0.75,
                                                         pos[2]),
                                            'scale': (0.5, 0.5, 0.5),
                                            'type': 'sphere',
                                            'materials': [mat]
                                        })
        print(f"[Game] Reset region created at {pos}.")


    def _get_invicible_one_player(self) -> Optional[Player]:
        # Should never return invalid references; return None in that case.
        if self._invicible_one_player:
            print(f"[Check] Current invincible player: {self._invicible_one_player}")
            return self._invicible_one_player
        print("[Check] No invincible player set.")
        return None

    def _handle_reset_collide(self) -> None:
        print("[Collision] A player collided with the reset region.")

        # If we have a chosen one, ignore these.
        if self._get_invicible_one_player() is not None:
            print("[Collision] Ignored: there is already an invincible player.")
            return

        # Attempt to get a Player controlling a Spaz that we hit.
        try:
            player = bs.getcollision().opposingnode.getdelegate(
                PlayerSpaz, True).getplayer(Player, True)
            print(f"[Collision] Player found: {player}")
        except bs.NotFoundError:
            print("[Collision] No valid player found on collision.")
            return

        if player.is_alive():
            print(f"[Collision] Player {player} is alive. Assigning as invincible one.")
            self._set_invicible_one_player(player)
        else:
            print(f"[Collision] Player {player} is dead. Ignoring.")


    def _flash_flag_spawn(self) -> None:
        print("[Visual] Flashing flag spawn position.")
        light = bs.newnode('light',
                           attrs={
                               'position': self._flag_spawn_pos,
                               'color': (1, 1, 1),
                               'radius': 0.3,
                               'height_attenuated': False
                           })
        bs.animate(light, 'intensity', {0: 0, 0.25: 0.5, 0.5: 0}, loop=True)
        bs.timer(1.0, light.delete)
        print("[Visual] Flash created and will auto-delete after 1s.")

    def _tick(self) -> None:
        print("[Tick] Running tick...")

        # Give the chosen one points.
        player = self._get_invicible_one_player()
        if player is not None:
            print(f"[Tick] Invincible player found: {player}")

            # This shouldn't happen, but just in case.
            if not player.is_alive():
                babase.print_error("[Tick] ERROR: Invincible player is dead. Resetting...")
                self._set_invicible_one_player(None)
            else:
                scoring_team = player.team
                assert self.stats
                self.stats.player_scored(player,
                                         3,
                                         screenmessage=False,
                                         display=False)
                print(f"[Tick] Player {player} scored +3 points.")

                scoring_team.time_remaining = max(
                    0, scoring_team.time_remaining - 1)
                print(f"[Tick] Team {scoring_team} time remaining: {scoring_team.time_remaining}s")

                self._update_scoreboard()
                print("[Tick] Scoreboard updated.")

                # announce numbers we have sounds for
                if scoring_team.time_remaining in self._countdownsounds:
                    print(f"[Tick] Countdown sound triggered: {scoring_team.time_remaining}")
                    bs.playsound(
                        self._countdownsounds[scoring_team.time_remaining])

                # Winner!
                if scoring_team.time_remaining <= 0:
                    print(f"[Game] Team {scoring_team} reached 0s. Ending game...")
                    self.end_game()

        else:
            print("[Tick] No invincible player at the moment.")
            # (player is None)
            # This shouldn't happen, but just in case.
            if self._invicible_one_player is not None:
                babase.print_error("[Tick] ERROR: Nonexistent player reference found. Resetting...")
                self._set_invicible_one_player(None)

    def end_game(self) -> None:
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team,
                                   self._invicible_one_time - team.time_remaining)
        self.end(results=results, announce_delay=0)

    def _set_invicible_one_player(self, player: Optional[Player]) -> None:
        existing = self._get_invicible_one_player()
        if existing:
            existing.chosen_light = None
        self._swipsound.play()
        if not player:
            assert self._flag_spawn_pos is not None
            self._flag = Flag(color=(1, 0.9, 0.2),
                              position=self._flag_spawn_pos,
                              touchable=False)
            self._invicible_one_player = None

            # Create a light to highlight the flag;
            # this will go away when the flag dies.
            bs.newnode('light',
                       owner=self._flag.node,
                       attrs={
                           'position': self._flag_spawn_pos,
                           'intensity': 0.6,
                           'height_attenuated': False,
                           'volume_intensity_scale': 0.1,
                           'radius': 0.1,
                           'color': (1.2, 1.2, 0.4)
                       })

            # Also an extra momentary flash.
            self._flash_flag_spawn()
        else:
            if player.actor:
                self._flag = None
                self._invicible_one_player = player

                if self._invicible_one_is_lazy:
                    player.actor.connect_controls_to_player(enable_punch = False, enable_pickup = False, enable_bomb = False)
                if player.actor.node.torso_mesh != None:
                    player.actor.node.color_mask_texture = None
                    player.actor.node.color_texture = None
                    player.actor.node.head_mesh = None
                    player.actor.node.torso_mesh = None
                    player.actor.node.upper_arm_mesh = None
                    player.actor.node.forearm_mesh = None
                    player.actor.node.pelvis_mesh = None
                    player.actor.node.toes_mesh = None
                    player.actor.node.upper_leg_mesh = None
                    player.actor.node.lower_leg_mesh = None
                    player.actor.node.hand_mesh = None
                    player.actor.node.style = 'cyborg'
                    invi_sound = []
                    player.actor.node.jump_sounds = invi_sound
                    player.actor.attack_sounds = invi_sound
                    player.actor.impact_sounds = invi_sound
                    player.actor.pickup_sounds = invi_sound
                    player.actor.death_sounds = invi_sound
                    player.actor.fall_sounds = invi_sound
        
                player.actor.node.name = ''


    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            # Augment standard behavior.
            super().handlemessage(msg)
            player = msg.getplayer(Player)
            if player is self._get_invicible_one_player():
                killerplayer = msg.getkillerplayer(Player)
                self._set_invicible_one_player(None if (
                    killerplayer is None or killerplayer is player
                    or not killerplayer.is_alive()) else killerplayer)
            self.respawn_player(player)
        else:
            super().handlemessage(msg)

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team,
                                            team.time_remaining,
                                            self._invicible_one_time,
                                            countdown=True)
