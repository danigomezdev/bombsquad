# ba_meta require api 9

from socket import socket, SOCK_DGRAM
from random import uniform as uf
from babase import Plugin, app
from threading import Thread
from time import time, sleep
from bauiv1 import (
    get_ip_address_type as IPT,
    clipboard_set_text as COPY,
    get_special_widget as zw,
    containerwidget as ocw,
    screenmessage as push,
    buttonwidget as obw,
    scrollwidget as sw,
    imagewidget as iw,
    textwidget as tw,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    getmesh as gm,
    Call
)
from bauiv1lib.popup import PopupMenuWindow

import _babase
import os

from bascenev1 import (
    disconnect_from_host as BYE,
    connect_to_party as CON,
    protocol_version as PT,
    get_game_roster as GGR
)

my_directory = _babase.env()['python_directory_user'] 
best_friends_file = os.path.join(my_directory, "BestFriends.txt")

class Finder:
    
    COL1 = (0.1, 0.1, 0.1)     
    COL2 = (0.2, 0.2, 0.2)      
    COL3 = (0.6, 0.2, 0.4)     
    COL4 = (1, 0.08, 0.58)      
    COL5 = (1, 0.3, 0.6)        

    MAX = 0.3
    TOP = 25
    VER = '1.1'
    MEM = []
    BST = []
    SL = None

    def __init__(s,src):

        s.friends_open = False  
        s.thr = []
        s.ikids = []
        s.ibfriends = []
        s.busy = False
        s.s1 = s.snd('powerup01')
        c = s.__class__
        # parent
        s.sizeWindow = (800,435)
        s.p = cw(
            scale_origin_stack_offset=src.get_screen_space_center(),
            size=s.sizeWindow,
            oac=s.bye
        )[0]

        s._popup_target = None

        # footing
        sw(
            parent=s.p,
            size=s.sizeWindow,
            border_opacity=0
        )

        # fetch
        tw(
            parent=s.p,
            text='Buscar Servidores',
            color=s.COL4,
            position=(19,359)
        )

        bw(
            parent=s.p,
            position=(360,343),
            size=(80,39),
            label='Buscar',
            color=s.COL2,
            textcolor=s.COL4,
            oac=s.fresh
        )

        tw(
            parent=s.p,
            text='Hace ping y ordena servidores públicos.',
            color=s.COL3,
            scale=0.8,
            position=(15,330),
            maxwidth=320
        )

        # separator
        iw(
            parent=s.p,
            size=(429,1),
            position=(17,330),
            texture=gt('white'),
            color=s.COL2
        )

        # cycle
        tw(
            parent=s.p,
            text='Servidores de Ciclo',
            color=s.COL4,
            position=(19,294)
        )

        bw(
            parent=s.p,
            position=(360,278),
            size=(80,39),
            label='Ciclar',
            color=s.COL2,
            textcolor=s.COL4,
            oac=s.find
        )

        tw(
            parent=s.p,
            text='Recorre los mejores servidores y guarda a sus jugadores.',
            color=s.COL3,
            scale=0.8,
            position=(15,265),
            maxwidth=320,
            v_align='center'
        )

        # separator
        iw(
            parent=s.p,
            size=(429,1),
            position=(17,265),
            texture=gt('white'),
            color=s.COL2
        )

        # top
        tw(
            parent=s.p,
            text='Límite de Servidores',
            color=s.COL4,
            position=(19,230)
        )

        s.top = tw(
            parent=s.p,
            position=(398,228),
            size=(80,50),
            text=str(c.TOP),
            color=s.COL4,
            editable=True,
            h_align='center',
            v_align='center',
            corner_scale=0.1,
            scale=10,
            allow_clear_button=False,
            shadow=0,
            flatness=1,
        )

        tw(
            parent=s.p,
            text='Número máximo de servidores a ciclar.',
            color=s.COL3,
            scale=0.8,
            position=(15,201),
            maxwidth=320
        )

        # separator
        iw(
            parent=s.p,
            size=(429,1),
            position=(17,200),
            texture=gt('white'),
            color=s.COL2
        )

        # players
        pl = s.plys()

        sy = max(len(pl)*30,140)
        
        p1 = sw(
            parent=s.p,
            position=(20,18),
            size=(205,172),
            border_opacity=0.4
        )
        
        p2 = ocw(
            parent=p1,
            size=(205,sy),
            background=False
        )
        
        0 if pl else tw(
            parent=s.p,
            position=(90,100),
            text='Recorre algunos servidores \npara recolectar jugadores',
            color=s.COL4,
            maxwidth=175,
            h_align='center'
        )

        # Refresh all best friends 
        s._refreshBestFriendsConnectedUI(pl)

        s.kids = []
        s.kids_bf = []
        for _,g in enumerate(pl):
            p,a = g
            s.kids.append(tw(
                parent=p2,
                size=(200,30),
                selectable=True,
                click_activate=True,
                color=s.COL3,
                text=p,
                position=(0,sy-30-30*_),
                maxwidth=175,
                on_activate_call=Call(s._hl,_,p),
                v_align='center'
            ))
        
        # info
        iw(
            parent=s.p,
            position=(235,18),
            size=(205,172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'),
            opacity=0.4
        )
        
        s.tip = tw(
            parent=s.p,
            position=(310,98),
            text='Seleccione algo para \nver la información del \nservidor',
            color=s.COL4,
            maxwidth=170,
            h_align='center'
        ) if c.SL is None else 0

        iw(
            parent=s.p,
            size=(2, 435),
            position=(455, 0),
            texture=gt('white'),
            color=s.COL2
        )

        tw(
            parent=s.p,
            text='Todos tus Amigos',
            color=s.COL4,
            position=(540, 400)
        )

        #bw(
        #    parent=s.p,
        #    size=(40, 40),
        #    scale=0.5,
        #    button_type='square',
        #    autoselect=True,
        #    color=s.COL2,
        #    position=(760, 375),
        #    on_activate_call =s._on_setting_button_press,
        #    icon=gt('settingsIcon'),
        #    iconscale=1.2
        #)


        #bw(
        #    parent=s.p,
        #    size=(40, 40),
        #    scale=0.8,
        #    button_type='square',
        #    autoselect=True,
        #    color=s.COL1,
        #    position=(410, 390),
        #    #on_activate_call =s._on_setting_button_press,
        #    icon=gt('usersButton'),
        #    iconscale=1.2
        #)

        #friends_connected_btn = bw(
        #    parent=s.p,
        #    size=(45, 45),
        #    scale=0.8,
        #    button_type='square',
        #    autoselect=True,
        #    color=s.COL1,
        #    position=(410, 390),
        #    icon=gt('usersButton'),
        #    iconscale=1.2
        #)

        friends_connected_btn = bw(
            parent=s.p,
            position=(400, 390),
            size=(45, 38),
            autoselect=True,
            button_type='square',
            label='',  # sin texto
            color=s.COL1,  # invisible
            oac=lambda: (
                s.toggle_friends()
            )
        )
        
        iw(
            parent=s.p,
            size=(45, 45),
            position=(400, 390),
            draw_controller=friends_connected_btn,
            texture=gt('usersButton'),
        )
        
        # Número encima controlado por el mismo botón
        s._users_count_text = tw(
            parent=s.p,
            text="7",
            size=(0, 0),
            position=(400 + 21, 390 + 16),
            h_align="center",
            v_align="center",
            scale=0.6,
            color=(0,1,0,1),  # verde
            draw_controller=friends_connected_btn  # ojo: lo ligamos al botón, no a la imagen
        )



        s.text_input = tw(
            parent=s.p,
            position=(695,320),
            size=(120,50),
            text="",
            color=s.COL4,
            editable=True,
            h_align='center',
            v_align='center',
            corner_scale=0.1,
            scale=10,
            allow_clear_button=False,
            shadow=0,
            flatness=1,
        )

        bw(
            parent=s.p,
            position=(640, 250),
            size=(120, 39),
            label='Agregar \nManualmente',
            color=s.COL2,
            textcolor=s.COL4,
            oac=lambda: (
                (lambda friend: (
                    s.add_friend(friend),
                    tw(edit=s.text_input, text=""),
                    s._refreshBestFriendsUI()
                ))(tw(query=s.text_input))
            )
        )

        # separator
        iw(
            parent=s.p,
            size=(320,1),
            position=(470,235),
            texture=gt('white'),
            color=s.COL2
        )
        
        # top
        tw(
            parent=s.p,
            text='En linea \ue019',
            color=s.COL4,
            position=(465,195)
        )
        
        tw(
            parent=s.p,
            text='*Recuerda que solo aparecerán tus \namigos si están jugando en un servidor \n publico, con cupo y después de ciclarlos*',
            color=s.COL4,
            position=(585,210),
            scale=0.44
        )

        # Best friends list
        s.p3 = sw(
            parent=s.p,
            position=(465, 240),
            size=(140, 130),
            border_opacity=0.4
        )
        s.p4 = None  # Init empty
        s._refreshBestFriendsUI()

        # Best friends(Connected) list
        s.p4 = sw(
            parent=s.p,
            position=(465, 17),
            size=(140, 170),
            border_opacity=0.4
        )

        s.p5 = None  # Init empty

        s.p6 = sw(
            parent=s.p,
            position=(615, 17),
            size=(175, 170),
            border_opacity=0.4
        )

        s.tip_bf = tw(
            parent=s.p6,
            size=(150, 155),  
            position=(0, 0),
            text='Seleccione un amigo \npara ver la información \ndel servidor',
            color=s.COL4,
            maxwidth=150,
            h_align='center',
            v_align='center'
        )


    def toggle_friends(s):
        # Cambiamos el valor con "not"
        s.friends_open = not s.friends_open

        if s.friends_open:
            print("Abrir toggle de amigos")
            #s.sizeWindow = (600,435)
        else:
            print("Cerrar toggle de amigos")

    def _refreshBestFriendsUI(s):
        if hasattr(s, "p4_friends") and s.p4_friends and s.p4_friends.exists():
            s.p4_friends.delete()

        friends_connected_list = s.get_all_friends()
        sy2 = max(len(friends_connected_list) * 30, 140)

        s.p4_friends = ocw(
            parent=s.p3,
            size=(190, sy2),
            background=False
        )

        # if there are no friends
        if not friends_connected_list:
            tw(
                parent=s.p3,
                position=(42, 70),
                text='Sin amigos \nconectados',
                color=s.COL3,
                maxwidth=135,
                h_align='center',
                v_align='center'
            )
            return

        for i, friend in enumerate(friends_connected_list):
            display_name = friend if len(friend) <= 7 else friend[:7] + "..."
            pos_y = sy2 - 30 - 30 * i

            tw(
                parent=s.p4_friends,
                size=(170, 30),
                color=s.COL3,
                text=display_name,
                position=(0, pos_y),
                maxwidth=160,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=Call(s._showFriendPopup, friend, (200, pos_y))
            )


    def _refreshBestFriendsConnectedUI(s, p):
        if hasattr(s, "p4_best") and s.p4_best and s.p4_best.exists():
            s.p4_best.delete()
            s.p4_best = None
            s.p5_best = None

        # List of best friends online
        best_friends_connected_list = s.get_all_best_friends(p)
        sy3 = max(len(best_friends_connected_list) * 30, 140)

        # Main scrollable container
        if not hasattr(s, "p4_best") or not (s.p4_best and s.p4_best.exists()):
            s.p4_best = sw(
                parent=s.p,
                position=(465, 17),
                size=(140, 170),
                border_opacity=0.4
            )

        # New container with best friends list
        s.p5_best = ocw(
            parent=s.p4_best,
            size=(190, sy3),
            background=False
        )

        # If there are no connected
        if not best_friends_connected_list:
            tw(
                parent=s.p5_best,
                position=(42, 50),
                text='Sin mejores \namigos \nconectados',
                color=s.COL3,
                maxwidth=125,
                h_align='center',
                v_align='center'
            )
            return

        # Fill UI with connected names
        for i, friend in enumerate(best_friends_connected_list):
            # If the name exceeds 7 characters, fill in with "..."
            display_name = friend if len(friend) <= 7 else friend[:7] + "..."
            pos_y = sy3 - 30 - 30 * i

            tw(
                parent=s.p5_best,
                size=(170, 30),
                color=s.COL3,
                text=display_name,
                position=(0, pos_y),
                maxwidth=160,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=Call(s._infoBestFriends, friend),
            )

    def _showFriendPopup(s, friend: str, pos: tuple[float, float]):
        
        popup = PopupMenuWindow(
            position=pos,
            choices=["Eliminar"],
            current_choice="",
            delegate=s,
            width=1,
        )

        bw(
            parent=popup.root_widget,
            position=(0, 2),
            size=(140, 54),
            label='Eliminar',
            color=s.COL2,
            textcolor=s.COL4,
            oac=lambda: (
                s.remove_friend(friend),
                s._refreshBestFriendsUI(),
                s._refreshBestFriendsConnectedUI(s.plys())
            )
        )
        s._popup_target = friend  

    def popup_menu_closing(s, popup_window) -> None:
        s._popup_target = None

    def _hl(s,_,p):
        [tw(t,color=s.COL3) for t in s.kids]
        tw(s.kids[_],color=s.COL4)
        s._infoPlayer(p)
    
    def _infoPlayer(s,p):

        [_.delete() for _ in s.ikids]
        s.ikids.clear()
        s.tip and s.tip.delete()
        bst = s.__class__.BST
        for _ in bst:
            for r in _['roster']:
                if r['display_string'] == p:
                    i = _
                    break
        for _ in range(3):
            t = str(i['nap'[_]])
            s.ikids.append(tw(
                parent=s.p,
                position=(250,155-40*_),
                h_align='center',
                v_align='center',
                maxwidth=175,
                text=t,
                color=s.COL4,
                size=(175,30),
                selectable=True,
                click_activate=True,
                on_activate_call=Call(s.copy,t)
            ))

        if p.startswith("\ue063"):
            # v2: Show both buttons side by side
            s.ikids.append(bw(
                parent=s.p,
                position=(250, 30),
                size=(80, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))

            s.ikids.append(bw(
                parent=s.p,
                position=(340, 30),
                size=(90, 30),
                label='Agregar Amigo',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(lambda: (
                    s.add_friend(p[1:]),  # remove the "\ue063" and add it
                    s._refreshBestFriendsUI(),
                    s._refreshBestFriendsConnectedUI(s.plys())
                ))
            ))

        else:
            
            s.ikids.append(bw(
                parent=s.p,
                position=(253, 30),
                size=(166, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))

    def _infoBestFriends(s, p):
        
        # Clean Ui
        [_.delete() for _ in s.ibfriends]
        s.ibfriends.clear()
        s.tip_bf and s.tip_bf.delete()

        bst = s.__class__.BST
        i = None
        for entry in bst:
            for r in entry['roster']:
                if r['display_string'] == p:
                    i = entry
                    break
            if i:
                break

        if i is None:
            return

        # Main data
        server_name = i.get("n", "Desconocido")
        server_ip = i.get("a", "N/A")
        server_port = i.get("p", "N/A")

        s.ibfriends.append(tw(
                parent=s.p6,
                position=(0, 0),
                h_align='center',
                maxwidth=160,
                text=f"{server_name}\n{server_ip}\n{server_port}",
                color=s.COL4,
                size=(160,40)
        ))

        if p.startswith("\ue063"):
            # v2: Show both buttons side by side
            s.ibfriends.append(bw(
                parent=s.p6,
                position=(14, 30),
                size=(60, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))

            s.ibfriends.append(bw(
                parent=s.p6,
                position=(84, 30),
                size=(75, 30),
                label='Eliminar \nAmigo',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(lambda: (
                    s.remove_friend(p),  # remove the "\ue063" and add it
                    s._refreshBestFriendsUI(),
                    s._refreshBestFriendsConnectedUI(s.plys()),
                    [_.delete() for _ in s.ibfriends]
                ))
            ))

        else:
            
            s.ibfriends.append(bw(
                parent=s.p6,
                position=(0, 30),
                size=(156, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))
    
    def copy(s,t):
        s.ding(1,1)
        TIP('Copiado en el portapapeles!')
        COPY(t)
    
    def plys(s):
        z = []
        me = app.plus.get_v1_account_name()
        me = [me, '\ue063' + me]
        for _ in s.__class__.BST:
            a = _['a']
            if (r := _.get('roster', {})):
                for p in r:
                    ds = p['display_string']
                    if ds not in me:
                        z.append((ds, a))

        result = sorted(z, key=lambda _: _[0].startswith('\ue030Server'))

        return result

    def snd(s,t):
        l = gs(t)
        l.play()
        teck(uf(0.14,0.18),l.stop)
        return l
    
    def bye(s):
        s.s1.stop()
        ocw(s.p,transition='out_scale')
        l = s.snd('laser')
        f = lambda: teck(0.01,f) if s.p else l.stop()
        f()
    
    def ding(s,i,j):
        a = ['Small','']
        x,y = a[i],a[j]
        s.snd('ding'+x)
        teck(0.1,gs('ding'+y).play)
    
    def fresh(s):
        if s.busy: BTW("Still busy!"); return
        TIP('Buscando Servidores...')
        s.ding(1,0)
        s.busy = True
        p = app.plus
        p.add_v1_account_transaction(
            {
                'type': 'PUBLIC_PARTY_QUERY',
                'proto': PT(),
                'lang': 'English'
            },
            callback=s.kang,
        )
        p.run_v1_account_transactions()

    def get_all_friends(s) -> list[str]:
        if not os.path.exists(best_friends_file):
            return []

        with open(best_friends_file, "r", encoding="utf-8") as f:
            friends = [line.strip() for line in f.readlines() if line.strip()]

        return friends
    
    def get_all_best_friends(s, pl: list[tuple[str, str]] | None = None) -> list[str]:
        best_friends = s.get_all_friends()
        connected_best_friends = []

        # If no pl is passed or is empty, returns empty list
        if not pl:
            return []

        for p, a in pl:
            if p in best_friends:
                connected_best_friends.append(p)

        return connected_best_friends


    def add_friend(s, friend: str):
        if s.busy:
            BTW("Todavía Ocupado!")
            return

        # Validate that it is not empty
        if not friend or friend.strip() == "":
            push('El campo está vacío, no se puede agregar', (1,0,0))
            gs('error').play()
            return

        # Ensure the file exists
        if not os.path.exists(best_friends_file):
            with open(best_friends_file, "w", encoding="utf-8") as f:
                f.write("")

        prefixed_friend = f"\ue063{friend.strip()}"

        # Read what already exists
        with open(best_friends_file, "r", encoding="utf-8") as f:
            existing = [line.strip() for line in f.readlines()]

        # Check for duplicates
        if prefixed_friend not in existing:
            with open(best_friends_file, "a", encoding="utf-8") as f:
                f.write(prefixed_friend + "\n")

            s.ding(1, 0)
            TIP(f"{prefixed_friend} agregado con éxito")
        else:
            TIP(f"{prefixed_friend} ya está en la lista")

    def remove_friend(s, friend: str):
        if s.busy:
            BTW("Todavía Ocupado!")
            return

        # Validate that it is not empty
        if not friend or friend.strip() == "":
            push('El campo está vacío, no se puede eliminar', (1, 0, 0))
            gs('error').play()
            return

        if not os.path.exists(best_friends_file):
            push('No hay lista de amigos para eliminar', (1, 0, 0))
            gs('error').play()
            return

        prefixed_friend = f"{friend.strip()}"

        # Read all existing friends
        with open(best_friends_file, "r", encoding="utf-8") as f:
            existing = [line.strip() for line in f.readlines()]

        if prefixed_friend in existing:
            # Re-write file excluding the removed friend
            with open(best_friends_file, "w", encoding="utf-8") as f:
                for line in existing:
                    if line != prefixed_friend:
                        f.write(line + "\n")

            s.ding(0, 1)  # diferente sonido que add (por ejemplo)
            TIP(f"{prefixed_friend} eliminado con éxito")
        else:
            TIP(f"{prefixed_friend} no se encuentra en la lista")

    def kang(s,r):
        c = s.__class__
        c.MEM = r['l']
        s.thr = []
        for _ in s.__class__.MEM:
            t = Thread(target=Call(s.ping,_))
            s.thr.append(t)
            t.start()
        teck(s.MAX*4,s.join)
    
    def join(s):
        c = s.__class__
        [t.join() for t in s.thr]
        far = s.MAX*3000
        c.MEM = [_ for _ in c.MEM if _['ping']]
        c.MEM.sort(key=lambda _: _['ping'])
        s.thr.clear()
        TIP(f'Cargado {len(c.MEM)} servidores!')
        s.ding(0,1)
        s.busy = False
    
    def find(s):
        if s.busy: BTW("Still busy!"); return
        c = s.__class__
        if not c.MEM:
            BTW('Primero, busque algunos servidores!')
            return
        t = tw(query=s.top)
        if not t.isdigit():
            BTW('Invalid cycle limit!')
            return
        top = int(t)
        if not (0 < top < len(c.MEM)):
            BTW('Cycle count is too '+['big','small'][top<=0]+'!')
            return
        c.TOP = top
        s.ding(1,0)
        TIP('Empezando Ciclado...')
        s.busy = True
        s.ci = s.lr = 0
        c.BST = c.MEM[:top]
        s.cycle()

    def cycle(s):
        _ = s.__class__.BST[s.ci]
        s.ca = _['a']
        CON(s.ca,_['p'],False)
        s.wait()

    def wait(s,i=5):
        r = GGR()
        if (r != s.lr) and r: s.__class__.BST[s.ci]['roster'] = s.lr = r; return s.next()
        if not i: s.__class__.BST[s.ci]['roster'] = []; return s.next()
        teck(0.1,Call(s.wait,i-1))

    def next(s):
        s.ci += 1
        if s.ci >= len(s.__class__.BST):
            BYE()
            teck(0.5,s.yay)
            return
        s.cycle()

    def yay(s):
        TIP('Ciclado Terminado!')
        s.ding(0,1)
        s.busy = False
        zw('squad_button').activate()
        teck(0.3,byLess.up)

    def ping(s,_):
        sock = ping = None
        a,p = _['a'],_['p']
        sock = socket(IPT(a),SOCK_DGRAM)
        try: sock.connect((a,p))
        except: ping = None
        else:
            st = time()
            sock.settimeout(s.MAX)
            yes = False
            for _i in range(3):
                try:
                    sock.send(b'\x0b')
                    r = sock.recv(10)
                except: r = None
                if r == b'\x0c':
                    yes = True
                    break
                sleep(s.MAX)
            ping = (time()-st)*1000 if yes else None
        finally:
            _['ping'] = ping
            sock.close()

# Patches
bw = lambda *,oac=None,**k: obw(
    texture=gt('white'),
    on_activate_call=oac,
    enable_sound=False,
    **k
)

cw = lambda *,size=None,oac=None,**k: (p:=ocw(
    parent=zw('overlay_stack'),
    background=False,
    transition='in_scale',
    size=size,
    on_outside_click_call=oac,
    **k
)) and (p,iw(
    parent=p,
    texture=gt('softRect'),
    size=(size[0]*1.2,size[1]*1.2),
    position=(-size[0]*0.1,-size[1]*0.1),
    opacity=0.55,
    color=(0,0,0)
),iw(
    parent=p,
    size=size,
    texture=gt('white'),
    color=Finder.COL1
))

# Global
BTW = lambda t: (push(t,color=(1,1,0)),gs('block').play())
TIP = lambda t: push(t,Finder.COL3)

# ba_meta export babase.Plugin
class byLess(Plugin):
    
    BTN = None
    @classmethod
    def up(c):
        c.BTN.activate() if c.BTN.exists() else None
    
    def __init__(s):
        from bauiv1lib import party
        p = party.PartyWindow
        a = '__init__'
        o = getattr(p,a)
        setattr(p,a,lambda z,*a,**k:(o(z,*a,**k),s.make(z))[0])
    
    def make(s,z):
        sz = (80,30)
        p = z._root_widget
        x,y = (-60,z._height-45)
        iw(
            parent=p,
            size=(sz[0]*1.34,sz[1]*1.4),
            position=(x-sz[0]*0.14,y-sz[1]*0.20),
            texture=gt('softRect'),
            opacity=0.2,
            color=(0,0,0)
        )
        s.b = s.__class__.BTN = bw(
            parent=p,
            position=(x,y),
            #position=(-120,200),
            label='Buscar',
            color=Finder.COL1,
            textcolor=Finder.COL3,
            size=sz,
            oac=lambda:Finder(s.b)
        )
