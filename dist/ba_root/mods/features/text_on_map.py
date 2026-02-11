import random
import _babase
import setting
from stats import mystats
import babase
import bascenev1 as bs

setti = setting.get_settings_data()

class textonmap:

    def __init__(self):
        data = setti['textonmap']
        left = data['bottom left watermark']
        top = data['top watermark']
        nextMap = ""

        try:
            nextMap = bs.get_foreground_host_session().get_next_game_description()
            nextMapText = nextMap.evaluate(lang='Spanish')
            #print(nextMapText)
        except Exception:
            pass
        try:
            top = top.replace("@IP", _babase.our_ip).replace("@PORT", str(_babase.our_port))
        except Exception:
            pass

        self.index = 0
        self.highlights = data['center highlights'].get("msg", [])

        self.show_team_score()
        self.left_watermark(left)
        self.nextGame(nextMap)
        self.top_message(top)
        self.restart_msg()

        if setti["leaderboard"]["enable"]:
            self.leaderBoard()

        # Only start the timer if there are messages
        if self.highlights:
            self.timer = bs.timer(8, babase.Call(self.highlights_), repeat=True)

    def highlights_(self):
        if not self.highlights:
            return  # No messages, show nothing

        if setti["textonmap"]['center highlights']["randomColor"]:
            color = (random.random(), random.random(), random.random())
        else:
            color = tuple(setti["textonmap"]["center highlights"]["color"])

        node = bs.newnode(
            'text',
            attrs={
                'text': self.highlights[self.index],
                'flatness': 1.0,
                'h_align': 'center',
                'v_attach': 'bottom',
                'scale': 1,
                'position': (0, 138),
                'color': color,
            },
        )

        self.delt = bs.timer(7, node.delete)

        # Make sure you don't go over the range
        self.index = (self.index + 1) % len(self.highlights)

    def show_team_score(self):
        """Display team scores (e.g., Azul: 0   Rojo: 0) centered at the top."""
        try:
            session = bs.get_foreground_host_session()
            teams = session.sessionteams

            if len(teams) < 2:
                return  # Only show if there are at least 2 teams

            team1 = teams[0]
            team2 = teams[1]

            # Try to evaluate localized team names in Spanish
            try:
                name1 = team1.name.evaluate(lang='Spanish')
            except Exception:
                try:
                    name1 = team1.name.evaluate()
                except Exception:
                    name1 = str(team1.name)

            try:
                name2 = team2.name.evaluate(lang='Spanish')
            except Exception:
                try:
                    name2 = team2.name.evaluate()
                except Exception:
                    name2 = str(team2.name)

            score1 = team1.customdata.get('score', 0)
            score2 = team2.customdata.get('score', 0)

            #print(f"[TEAM SCORE] {name1}: {score1} | {name2}: {score2}")

            # First team name + score (left)
            bs.newnode('text', attrs={
                'text': f"{name1}: {score1}",
                'flatness': 1.0,
                'h_align': 'right',
                'v_attach': 'top',
                'scale': 1.0,
                'position': (-40, -80),
                'color': team1.color if hasattr(team1, "color") else (0.5, 0.5, 0.5),
            })

            # Second team name + score (right)
            bs.newnode('text', attrs={
                'text': f"{name2}: {score2}",
                'flatness': 1.0,
                'h_align': 'left',
                'v_attach': 'top',
                'scale': 1.0,
                'position': (40, -80),
                'color': team2.color if hasattr(team2, "color") else (0.5, 0.5, 0.5),
            })

        except Exception as e:
            print("Error showing team score:", e)

    def left_watermark(self, text: str):
        bs.newnode('text', attrs={
            'text': text,
            'flatness': 1.0,
            'h_align': 'left',
            'v_attach': 'bottom',
            'h_attach': 'left',
            'scale': 0.8,
            'position': (15, 60),
            'color': (1, 1, 1)
        })

        base_x = 120
        top_y = 90
        bottom_y = 55

        divider_top = bs.newnode('image', attrs={
            'texture': bs.gettexture('white'),
            'color': (1, 1, 0),
            'position': (base_x, top_y),
            'attach': 'bottomLeft',
            'scale': (220, 4),
            'opacity': 0.9
        })

        divider_bottom = bs.newnode('image', attrs={
            'texture': bs.gettexture('white'),
            'color': (1, 1, 0),
            'position': (base_x, bottom_y),
            'attach': 'bottomLeft',
            'scale': (220, 4),
            'opacity': 0.9
        })

        rainbow_keys = {
            0.0: (1, 0, 0),
            0.2: (1, 1, 0),
            0.4: (0, 1, 0),
            0.6: (0, 1, 1),
            0.8: (0, 0, 1),
            1.0: (1, 0, 1),
        }

        bs.animate_array(node=divider_top, attr='color', size=3, keys=rainbow_keys, loop=True)
        bs.animate_array(node=divider_bottom, attr='color', size=3, keys=rainbow_keys, loop=True)

    def nextGame(self, text):
        try:
            session = bs.get_foreground_host_session()
            game_number = session.get_game_number() + 1 if hasattr(session, "get_game_number") else 1
        except Exception:
            game_number = 1

        bs.newnode('text', attrs={
            'text': bs.Lstr(
                value='${A} ${B}',
                subs=[
                    (
                        '${A}',
                        bs.Lstr(
                            resource='upNextText',
                            subs=[('${COUNT}', str(game_number))]
                        ),
                    ),
                    ('${B}', text)
                ]
            ),
            'flatness': 1.0,
            'h_align': 'right',
            'v_attach': 'bottom',
            'h_attach': 'right',
            'scale': 0.7,
            'position': (-25, 16),
            'color': (0.5, 0.5, 0.5),
        })


    def season_reset(self, text):
        bs.newnode('text', attrs={
            'text': "Season ends in: " + str(text) + " days",
            'flatness': 1.0,
            'h_align': 'right',
            'v_attach': 'bottom',
            'h_attach': 'right',
            'scale': 0.5,
            'position': (-25, 34),
            'color': (0.6, 0.5, 0.7),
        })

    def restart_msg(self):
        if hasattr(_babase, 'restart_scheduled'):
            activity = bs.get_foreground_host_activity()
            if not hasattr(activity, "restart_msg_node"):
                activity.restart_msg_node = bs.newnode(
                    'text',
                    attrs={
                        'text': "El servidor se reiniciará después de esta serie.",
                        'flatness': 1.0,
                        'h_align': 'right',
                        'v_attach': 'bottom',
                        'h_attach': 'right',
                        'scale': 0.5,
                        'position': (-25, 54),
                        'color': (1, 0.5, 0.7),
                    }
                )

    def top_message(self, text):
        bs.newnode('text', attrs={
            'text': text,
            'flatness': 1.0,
            'h_align': 'center',
            'v_attach': 'top',
            'scale': 0.7,
            'position': (0, -70),
            'color': (1, 1, 1),
        })

    def leaderBoard(self):
        # Get all stats
        stats = mystats.get_all_stats()

        # Sort by scores (descending)
        ordered = sorted(
            stats.values(),
            key=lambda x: x.get("scores", 0),
            reverse=True
        )

        # Extract up to 5 real names
        player_names = [p.get("name", "Unknown") for p in ordered[:5]]

        # Configured slots (design)
        leaderboard_slots = [
            {
                "default_name": "PlayerOne",
                "color": (1.0, 0.0, 0.0),   # Red
                "texture": "penguinColorMask",
                "y": -80
            },
            {
                "default_name": "PlayerTwo",
                "color": (0.0, 0.5, 1.0),   # Blue
                "texture": "explosion",
                "y": -115
            },
            {
                "default_name": "PlayerThree",
                "color": (1.0, 1.0, 0.0),   # Yellow
                "texture": "bunnyColor",
                "y": -150
            },
            {
                "default_name": "PlayerFour",
                "color": (1.0, 0.4, 0.7),   # Pink
                "texture": "uiAtlas2",
                "y": -185
            },
            {
                "default_name": "PlayerFive",
                "color": (0.6, 0.0, 1.0),   # Violet
                "texture": "uiAtlas2",
                "y": -220
            }
        ]

        # Fill with defaults if missing
        names = list(player_names)
        while len(names) < 5:
            names.append(leaderboard_slots[len(names)]["default_name"])

        #print("[DEBUG] Leaderboard Names ->", names)

        # Create nodes for each location
        for i, slot in enumerate(leaderboard_slots):
            text_color = slot["color"]
            bg_color = tuple(c * 0.5 for c in text_color)  # more opaque
            pos_y = slot["y"]

            # Background
            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture(slot["texture"]),
                'position': (0, pos_y),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_color
            })

            # Text
            name = names[i]
            text_display = name[:10] + ("..." if len(name) > 10 else "")
            bs.newnode('text', attrs={
                'text': f"#{i+1} {text_display}",
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, pos_y),
                'scale': 0.7, 'color': text_color
            })

    def debug_print_all_stats(self):
        """
        Prints the entire contents of mystats to the console (full stats, top players, and total players).
        """
        stats = mystats.get_all_stats()

        print("\n" + "="*40)
        print("[DEBUG] --- ESTADO DE MYSTATS ---")

        # Total
        print(f"[DEBUG] Total jugadores en stats.json: {len(stats)}")

        # Each player
        for aid, data in stats.items():
            print(f"  - {aid}: {data}")

        # Top 5 
        ordered = sorted(
            stats.items(), 
            key=lambda x: x[1].get("score", 0),
            reverse=True
        )
        top5 = [name for name, _ in ordered[:5]]
        print("\n[DEBUG] Top 5 Names:", top5 if top5 else "(vacío)")

        print("[DEBUG] --- FIN DEBUG MYSTATS ---")
        print("="*40 + "\n")
