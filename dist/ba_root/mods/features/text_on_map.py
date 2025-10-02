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
            nextMap = bs.get_foreground_host_session().get_next_game_description().evaluate()
        except Exception:
            pass
        try:
            top = top.replace("@IP", _babase.our_ip).replace("@PORT", str(_babase.our_port))
        except Exception:
            pass

        self.index = 0
        self.highlights = data['center highlights'].get("msg", [])

        self.left_watermark(left)
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

        # Asegurarse de no pasarse del rango
        self.index = (self.index + 1) % len(self.highlights)

    def left_watermark(self, text):
        bs.newnode('text', attrs={
            'text': text,
            'flatness': 1.0,
            'h_align': 'left',
            'v_attach': 'bottom',
            'h_attach': 'left',
            'scale': 0.7,
            'position': (25, 67),
            'color': (0.7, 0.7, 0.7),
        })

    def nextGame(self, text):
        bs.newnode('text', attrs={
            'text': "Next : " + text,
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
            _babase.get_foreground_host_activity().restart_msg = bs.newnode(
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
                })

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
