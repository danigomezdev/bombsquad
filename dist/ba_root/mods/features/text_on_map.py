import random
import _babase
import setting
#from stats import mystats
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

        #if setti["leaderboard"]["enable"]:
        #    self.leaderBoard()

        self.leaderBoardTest()

        # Solo iniciar el timer si hay mensajes
        if self.highlights:
            self.timer = bs.timer(8, babase.Call(self.highlights_), repeat=True)

    def highlights_(self):
        if not self.highlights:
            return  # No hay mensajes, no mostrar nada

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

#    def leaderBoard(self):
#        if len(mystats.top3Name) > 2:
#            if setti["leaderboard"]["barsBehindName"]:
#                bs.newnode('image', attrs={'scale': (300, 30),
#                                           'texture': bs.gettexture('uiAtlas2'),
#                                           'position': (0, -80),
#                                           'attach': 'topRight',
#                                           'opacity': 0.5,
#                                           'color': (0.7, 0.1, 0)})
#                bs.newnode('image', attrs={'scale': (300, 30),
#                                           'texture': bs.gettexture('uiAtlas2'),
#                                           'position': (0, -115),
#                                           'attach': 'topRight',
#                                           'opacity': 0.5,
#                                           'color': (0.6, 0.6, 0.6)})
#                bs.newnode('image', attrs={'scale': (300, 30),
#                                           'texture': bs.gettexture('uiAtlas2'),
#                                           'position': (0, -150),
#                                           'attach': 'topRight',
#                                           'opacity': 0.5,
#                                           'color': (0.1, 0.3, 0.1)})
#
#            bs.newnode('text', attrs={
#                'text': "#1 " + mystats.top3Name[0][:10] + "...",
#                'flatness': 1.0, 'h_align': 'left', 'h_attach': 'right',
#                'v_attach': 'top', 'v_align': 'center', 'position': (-140, -80),
#                'scale': 0.7, 'color': (0.7, 0.4, 0.3)})
#
#            bs.newnode('text', attrs={
#                'text': "#2 " + mystats.top3Name[1][:10] + "...",
#                'flatness': 1.0, 'h_align': 'left', 'h_attach': 'right',
#                'v_attach': 'top', 'v_align': 'center', 'position': (-140, -115),
#                'scale': 0.7, 'color': (0.8, 0.8, 0.8)})
#
#            bs.newnode('text', attrs={
#                'text': "#3 " + mystats.top3Name[2][:10] + "...",
#                'flatness': 1.0, 'h_align': 'left', 'h_attach': 'right',
#                'v_attach': 'top', 'v_align': 'center', 'position': (-140, -150),
#                'scale': 0.7, 'color': (0.2, 0.6, 0.2)})
#



    def leaderBoardTest(self):
        # Top 5 players (ejemplo)
        self.top5Name = ["PlayerOne", "PlayerTwo", "PlayerThree", "PlayerFour", "PlayerFive"]

        # 🎨 Colores configurables (texto)
        color_first = (1.0, 1.0, 0.0)   # Amarillo
        color_second = (0.0, 0.5, 1.0)  # Azul
        color_third = (1.0, 0.0, 0.0)   # Rojo
        color_fourth = (1.0, 0.4, 0.7)  # Rosado
        color_fifth = (0.6, 0.0, 1.0)   # Violeta

        # 🎨 Colores para los fondos (más opacos, multiplicados por 0.5)
        bg_first = tuple(c * 0.5 for c in color_first)
        bg_second = tuple(c * 0.5 for c in color_second)
        bg_third = tuple(c * 0.5 for c in color_third)
        bg_fourth = tuple(c * 0.5 for c in color_fourth)
        bg_fifth = tuple(c * 0.5 for c in color_fifth)

        if len(self.top5Name) >= 5:
            # Fondos
            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture('bunnyIconColorMask'),
                'position': (0, -80),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_first})

            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture('explosion'),
                'position': (0, -115),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_second})

            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture('penguinColorMask'),
                'position': (0, -150),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_third})

            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture('rgbStripes'),
                'position': (0, -185),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_fourth})

            bs.newnode('image', attrs={
                'scale': (300, 30),
                'texture': bs.gettexture('bunnyColor'),
                'position': (0, -220),
                'attach': 'topRight',
                'opacity': 0.5,
                'color': bg_fifth})

            # Textos Top 5
            bs.newnode('text', attrs={
                'text': "#1 " + self.top5Name[0][:10] + ("..." if len(self.top5Name[0]) > 10 else ""),
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, -80),
                'scale': 0.7, 'color': color_first})

            bs.newnode('text', attrs={
                'text': "#2 " + self.top5Name[1][:10] + ("..." if len(self.top5Name[1]) > 10 else ""),
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, -115),
                'scale': 0.7, 'color': color_second})

            bs.newnode('text', attrs={
                'text': "#3 " + self.top5Name[2][:10] + ("..." if len(self.top5Name[2]) > 10 else ""),
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, -150),
                'scale': 0.7, 'color': color_third})

            bs.newnode('text', attrs={
                'text': "#4 " + self.top5Name[3][:10] + ("..." if len(self.top5Name[3]) > 10 else ""),
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, -185),
                'scale': 0.7, 'color': color_fourth})

            bs.newnode('text', attrs={
                'text': "#5 " + self.top5Name[4][:10] + ("..." if len(self.top5Name[4]) > 10 else ""),
                'flatness': 1.0, 'h_align': 'left',
                'h_attach': 'right', 'v_attach': 'top',
                'v_align': 'center', 'position': (-140, -220),
                'scale': 0.7, 'color': color_fifth})
        else:
            print("[LeaderBoardTest] No hay suficientes jugadores para mostrar el Top 5")
