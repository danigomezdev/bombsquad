# ba_meta require api 9

from json import dumps, loads
from threading import Thread
from time import time, sleep
from bascenev1 import (
    connect_to_party as CON,
    protocol_version as PT
)
from bauiv1 import (
    get_ip_address_type as IPT,
    clipboard_set_text as COPY,
    get_special_widget as zw,
    containerwidget as ocw,
    screenmessage as push,
    buttonwidget as obw,
    scrollwidget as sw,
    imagewidget as iw,
    SpecialChar as sc,
    textwidget as tw,
    gettexture as gt,
    apptimer as teck,
    AppTimer as tuck,
    getsound as gs,
    getmesh as gm,
    charstr as cs,
    Call
)

from bauiv1lib.popup import PopupMenuWindow
from babase import (
    app_instance_uuid as U,
    Plugin,
    app
)
from random import (
    uniform as uf,
    choice as CH,
    randint
)
from socket import (
    SOCK_DGRAM,
    socket
)
import _babase
import os

my_directory = _babase.env()['python_directory_user'] 
best_friends_file = os.path.join(my_directory, "BestFriends.txt")

class Finder:
    VER = '2.0'
    COL1 = (0.1, 0.1, 0.1)     
    COL2 = (0.2, 0.2, 0.2)      
    COL3 = (0.6, 0.2, 0.4)     
    COL4 = (1, 0.08, 0.58)      
    COL5 = (1, 0.3, 0.6)    

    MAX = 0.3
    TOP = 1
    MEM = []
    ART = []
    BUSY = False
    KIDS = []
    P2 = None
    ARTT = None
    SL = None
    TIP = None
    FLT = ''
    def __init__(s,src):
        s.friends_open = False  
        s.thr = []
        s.ikids = []
        s.pro = []
        s.sust = None
        s.ParentFriends = None
        s.s1 = s.snd('powerup01')
        c = s.__class__
        # parent
        sizeWindow = (800,435)

        c.root = cw(
            scale_origin_stack_offset=src.get_screen_space_center(),
            size=sizeWindow,
            oac=s.bye,
        )[0]

        sizeWindow = (460,435)

        c.MainParent = ocw(
            position=(0, 0),
            parent=c.root,
            size=sizeWindow,
            background=False
        )

        iw(
            parent=c.MainParent,
            size=sizeWindow,
            texture=gt('white'),
            color=s.COL1
        )

        # footing
        sw(
            parent=c.MainParent,
            size=sizeWindow,
            border_opacity=0
        )

        friends_connected_btn = bw(
            parent=c.MainParent,
            position=(400, 390),
            size=(45, 38),
            autoselect=True,
            button_type='square',
            label='',
            color=s.COL1,
            oac=lambda:(
                s.toggle_friends()
            )
        )
        
        iw(
            parent=c.MainParent,
            size=(45, 45),
            position=(400, 390),
            draw_controller=friends_connected_btn,
            texture=gt('usersButton'),
        )

        pl = s.plys()
        s.bf_connected = len(s._getAllBestFriendsConnected(pl))

        s._users_count_text = tw(
            parent=c.MainParent,
            text=str(s.bf_connected),
            size=(0, 0),
            position=(400 + 21, 390 + 16),
            h_align="center",
            v_align="center",
            scale=0.6,
            color=(0,1,0,1),
            draw_controller=friends_connected_btn  
        )

        # fetch
        tw(
            parent=c.MainParent,
            text='Buscar todos los servidores',
            color=s.COL4,
            position=(19,359)
        )
        bw(
            parent=c.MainParent,
            position=(360,343),
            size=(80,39),
            label='Buscar',
            color=s.COL2,
            textcolor=s.COL4,
            oac=s.fresh
        )
        tw(
            parent=c.MainParent,
            text='Busca jugadores sin tener que unirse a partida',
            color=s.COL3,
            scale=0.8,
            position=(15,330),
            maxwidth=320
        )
        # separator
        iw(
            parent=c.MainParent,
            size=(429,1),
            position=(17,330),
            texture=gt('white'),
            color=s.COL2
        )

        
        # cube art
        c.ARTT = tw(
            parent=c.MainParent,
            text='¡Pulsa buscar y yo me \nencargo del resto!',
            maxwidth=430,
            max_height=125,
            h_align='center',
            v_align='top',
            color=s.COL4,
            position=(205,260),
        )
        # separator
        iw(
            parent=c.MainParent,
            size=(429,1),
            position=(17,200),
            texture=gt('white'),
            color=s.COL2
        )
        # filter
        c.FT = tw(
            parent=c.MainParent,
            position=(23,150),
            size=(201,35),
            text=c.FLT,
            editable=True,
            glow_type='uniform',
            allow_clear_button=False,
            v_align='center',
            color=s.COL4,
            description='Raw search - Matches wildcard to all strings in server\'s JSON, including player names, and server name. Enter'
        )
        s.ft2 = tw(
            parent=c.MainParent,
            position=(26,153),
            text='Buscar',
            color=s.COL3
        )
        # players
        p1 = sw(
            parent=c.MainParent,
            position=(20,18),
            size=(205,122),
            border_opacity=0.4,
            color=s.COL4
        )
        c.MainParent2 = ocw(
            parent=p1,
            size=(205,1),
            background=False
        )
        s.pltip = tw(
            parent=c.MainParent,
            position=(90,100),
            text='Busca en algunos servidores\npara encontrar jugadores\nLos resultados pueden variar\nsegún la hora y la conexión',
            color=s.COL4,
            maxwidth=175,
            h_align='center'
        )
        # info
        iw(
            parent=c.MainParent,
            position=(235,18),
            size=(205,172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'),
            opacity=0.4
        )
        s.tip = 'Selecciona algo para\nver la info del servidor'
        c.TIP = tw(
            parent=c.MainParent,
            position=(310,98),
            text=s.tip,
            color=s.COL4,
            maxwidth=170,
            h_align='center'
        )
        # finally
        s.draw() if c.ART else 0
        s.up()
        c.SL and s.info(c.SL)
        c.FL = tuck(0.1,s.flup,repeat=True)
    def flup(s):
        c = s.__class__
        if not s.ft2.exists():
            c.FL = None
            return
        ct = tw(query=c.FT)
        tw(s.ft2,text=['Buscar',''][bool(ct)])
        if ct != s.FLT:
            c.FLT = ct
            s.up()
    def hl(s,_,p):
        c = s.__class__
        c.SL = p
        [tw(t,color=s.COL3) for t in c.KIDS]
        tw(c.KIDS[_],color=s.COL4)
        s.info(p)
    def info(s,p):
        [_.delete() for _ in s.ikids]
        s.ikids.clear()
        c = s.__class__
        tw(c.TIP,text='')
        i = None
        for _ in c.MEM:
            for r in _.get('roster',[]):
                spec = loads(r['spec'])
                if spec['n'] == p:
                    i = _
                    pz = r['p']
                    break
        if i is None:
            c.SL = None
            tw(c.TIP,text=s.tip)
            return
        for _ in range(3):
            t = str(i['nap'[_]])
            px = [250,245,375][_]
            py = [155,115][bool(_)]
            sx = [175,115,55][_]
            s.ikids.append(tw(
                parent=c.MainParent,
                position=(px,py),
                h_align='center',
                v_align='center',
                maxwidth=sx,
                text=t,
                color=s.COL4,
                size=(sx,30),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=Call(s.copy,t)
            ))

        account_v2 = [str(list(_.values())[1]) for _ in pz]

        s.ikids.append(bw(
            parent=c.MainParent,
            position=(253,65),
            size=(170,30),
            label=str(account_v2[0]) if account_v2 and account_v2[0] != [] else p,
            color=s.COL2,
            textcolor=s.COL4,
            oac=Call(s.oke,'\n'.join([' | '.join([str(j) for j in _.values()]) for _ in pz]) or 'Nothing')
        ))

        if account_v2 and str(account_v2[0]).startswith("\ue063"):
            # v2: Show both buttons side by side
            s.ikids.append(bw(
                parent=c.MainParent,
                position=(250, 30),
                size=(80, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))

            s.ikids.append(bw(
                parent=c.MainParent,
                position=(340, 30),
                size=(87, 30),
                label='Agregar Amigo',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(lambda: (
                    s._addFriend(p),
                    s._refreshBestFriendsUI(),
                    s._refreshBestFriendsConnectedUI(s.plys())
                ))
            ))
        else:
            s.ikids.append(bw(
                parent=c.MainParent,
                position=(253, 30),
                size=(170, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))


    def toggle_friends(s):
        s.friends_open = not s.friends_open

        if s.friends_open:
            print("Abrir toggle de amigos")

            sizeWindow = (355,435)
            # Crear panel de amigos como hijo
            
            s.ParentFriends = ocw(
                parent=s.root,
                size=sizeWindow,
                position=(460, 0),
                background=False,
            )
            

            iw(
                parent=s.ParentFriends,
                size=sizeWindow,
                texture=gt('white'),
                color=s.COL1
            )

            # separator
            iw(
                parent=s.ParentFriends,
                size=(3,435),
                position=(0,0),
                texture=gt('white'),
                color=s.COL2
            )

            tw(
                parent=s.ParentFriends,
                text='Todos tus Amigos',
                color=s.COL4,
                position=(540-450, 400)
            )


            s.text_input = tw(
                parent=s.ParentFriends,
                position=(695-450,320),
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
                parent=s.ParentFriends,
                position=(640-450, 250),
                size=(120, 39),
                label='Agregar \nManualmente',
                color=s.COL2,
                textcolor=s.COL4,
                oac=lambda: (
                    (lambda friend: (
                        s._addFriend(friend),
                        tw(edit=s.text_input, text=""),
                        s._refreshBestFriendsUI()
                    ))(tw(query=s.text_input))
                )
            )

            # separator
            iw(
                parent=s.ParentFriends,
                size=(320,1),
                position=(470-450,235),
                texture=gt('white'),
                color=s.COL2
            )

            # top
            tw(
                parent=s.ParentFriends,
                text='En linea \ue019',
                color=s.COL4,
                position=(465-450,195)
            )

            tw(
                parent=s.ParentFriends,
                text='*Recuerda que solo aparecerán tus \namigos si están jugando en un servidor \n publico, con cupo y después de ciclarlos*',
                color=s.COL4,
                position=(585-450,210),
                scale=0.44
            )

            # Best friends list
            s.p3 = sw(
                parent=s.ParentFriends,
                position=(465-450, 240),
                size=(140, 130),
                border_opacity=0.4
            )
            s.p4 = None  # Init empty
            s._refreshBestFriendsUI()

            # Best friends(Connected) list
            s.p4 = sw(
                parent=s.ParentFriends,
                position=(465-450, 17),
                size=(140, 170),
                border_opacity=0.4
            )

            s.p5 = None  # Init empty

            s.p6 = sw(
                parent=s.ParentFriends,
                position=(615-450, 17),
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
            s._refreshBestFriendsUI()
            s._refreshBestFriendsConnectedUI(s.plys())

        else:
            print("Cerrar toggle de amigos")

            # Destruir panel si existe
            if hasattr(s, "ParentFriends") and s.ParentFriends and s.ParentFriends.exists():
                s.ParentFriends.delete()
                s.ParentFriends = None

    def _updateCount(s):
        new_count = len(s._getAllBestFriendsConnected(s.plys()))
        tw(edit=s._users_count_text, text=str(new_count))


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
                position=(42-450, 70),
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
        if not (s.ParentFriends and s.ParentFriends.exists()):
            print("⚠️ No existe el panel BestFriends, abortando refresh.")
            return

        if hasattr(s, "p4_best") and s.p4_best and s.p4_best.exists():
            s.p4_best.delete()
            s.p4_best = None
            s.p5_best = None

        # List of best friends online
        best_friends_connected_list = s._getAllBestFriendsConnected(p)
        sy3 = max(len(best_friends_connected_list) * 30, 140)

        # Main scrollable container
        if not hasattr(s, "p4_best") or not (s.p4_best and s.p4_best.exists()):
            s.p4_best = sw(
                parent=s.ParentFriends,
                position=(465-450, 17),
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
                s._deleteFriend(friend),
                s._refreshBestFriendsUI(),
                s._refreshBestFriendsConnectedUI(s.plys())
            )
        )
        s._popup_target = friend  

    def popup_menu_closing(s, popup_window) -> None:
        s._popup_target = None

    def oke(s,t):
        TIP(t)
        s.ding(1,1)
    def copy(s,t):
        s.ding(1,1)
        TIP('Copied to clipboard!')
        COPY(t)
    def plys(s):
        z = []
        c = s.__class__
        for _ in c.MEM:
            a = _['a']
            if (r:=_.get('roster',{})):
                for p in r:
                    ds = loads(p['spec'])['n']
                    0 if (
                        ds == 'Finder' or
                        (c.FLT and not s.chk(r))
                    ) else z.append((ds,a))
        return sorted(z,key=lambda _: _[0].startswith('Server'))
    def chk(s,r):
        t = s.__class__.FLT.lower()
        for _ in r:
            n = loads(_['spec'])['n']
            if n != 'Finder' and t in n.lower(): return True
            for p in _['p']:
                if t in p['nf'].lower(): return True
        return False
    def snd(s,t):
        l = gs(t)
        l.play()
        teck(uf(0.14,0.18),l.stop)
        return l
    def bye(s):
        s.s1.stop()
        c = s.__class__
        ocw(c.root,transition='out_scale')
        l = s.snd('laser')
        f = lambda: teck(0.01,f) if c.root else l.stop()
        f()
    def ding(s,*z):
        a = ['Small','']
        for i,_ in enumerate(z):
            h = 'ding'+a[_]
            teck(i/10,Call(s.snd,h) if i<(len(z)-1) else gs(h).play)
    def fresh(s):
        c = s.__class__
        if c.BUSY:
            TIP("Still busy!")
            s.ding(0,0)
            return
        TIP('¡Escaneando servidores!\nEsto debería tardar unos segundos.\nPuedes cerrar esta ventana.')
        c.ST = time()
        s.ding(1,0)
        c.BUSY = True
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
    
    def _getAllBestFriendsConnected(s, pl: list[tuple[str, str]] | None = None) -> list[str]:
        best_friends = s.get_all_friends()
        connected_best_friends = []

        # If no pl is passed or is empty, returns empty list
        if not pl:
            return []

        for p, a in pl:
            if p in best_friends:
                connected_best_friends.append(p)

        return connected_best_friends


    def _addFriend(s, friend: str):
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
            s.bf_connected+=1
            s._updateCount()
            TIP(f"{prefixed_friend} agregado con éxito")
        else:
            TIP(f"{prefixed_friend} ya está en la lista")

    def _deleteFriend(s, friend: str):
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
            s.bf_connected-=1
            TIP(f"{prefixed_friend} eliminado con éxito")
            s._updateCount()
        else:
            TIP(f"{prefixed_friend} no se encuentra en la lista")

    def kang(s,r):
        c = s.__class__
        c.MEM = r['l']
        c.ART = [cs(sc.OUYA_BUTTON_U)]*len(c.MEM)
        s.thr = []
        for i,_ in enumerate(c.MEM):
            t = Thread(target=Call(s.ping,_,i))
            s.thr.append(t)
            t.start()
        s.sust = tuck(0.01,s.sus,repeat=True)
    def ping(s,_,i):
        _['ping'],_['roster'] = ping_and_kang(_['a'],_['p'],pro=s.pro,dex=i)
    def sus(s):
        if not s.pro: return
        i,p = s.pro.pop()
        c = s.__class__
        c.ART[i] = (
            cs(sc.OUYA_BUTTON_A) if p==999 else
            cs(sc.OUYA_BUTTON_O) if p<100 else
            cs(sc.OUYA_BUTTON_Y)
        )
        s.draw() if c.ARTT.exists() else None
        if cs(sc.OUYA_BUTTON_U) not in c.ART:
            s.syst = None
            s.done()
    def draw(s):
        c = s.__class__
        tw(c.ARTT,text=('\n'.join(''.join(c.ART[i:i+40]) for i in range(0,len(s.ART),40))), position=(205,295))
        s.up()
    def up(s):
        c = s.__class__
        [_.delete() for _ in c.KIDS]
        c.KIDS.clear()
        pl = s.plys()
        s.pltip.delete() if pl else 0
        sy = max(len(pl)*30,90)
        ocw(c.MainParent2,size=(205,sy))
        dun = 0
        for _,g in enumerate(pl):
            p,a = g
            tt = tw(
                parent=c.MainParent2,
                size=(200,30),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                color=[s.COL3,s.COL4][p==c.SL and not dun],
                text=p,
                position=(0,sy-30-30*_),
                maxwidth=175,
                on_activate_call=Call(s.hl,_,p),
                v_align='center'
            )
            if not dun and p == c.SL: ocw(c.MainParent2,visible_child=tt); dun = 1
            c.KIDS.append(tt)
    def done(s):
        s.ding(0,1)
        [_.join() for _ in s.thr]
        s.thr.clear()
        c = s.__class__
        tt = time() - c.ST
        ln = len(s.MEM)
        ab = int(ln/tt)
        TIP(f'¡Terminado!\nEscaneados {ln} servidores en {round(tt,2)} segundos!\nAproximadamente {ab} servidor{["es",""][ab<2]}/seg')
        s.__class__.BUSY = False
        s._refreshBestFriendsConnectedUI(s.plys())


# Kang
SPEC = {"s":"{\"n\":\"Finder\",\"a\":\"\",\"sn\":\"\"}","d":"69"*20}
AUTH = {'b': app.env.engine_build_number, 'tk': '', 'ph': ''}

def ping_and_kang(
    address: str,
    port: int,
    ping_wait: float = 0.3,
    timeout: float = 3.5,
    pro = [],
    dex = None,
):
    """
    Pings a server and then grabs its roster using a single connection.

    Args:
        address (str): The server's IP address.
        port (int): The server's port.
        ping_wait (float): Time to wait between ping retries.
        timeout (float): Overall timeout for the entire operation.

    Returns:
        tuple[float | None, dict | None]: A tuple containing the ping in milliseconds
                                           and the parsed roster dictionary.
    """
    ping_result = None
    roster_result = None
    sock = socket(IPT(address),SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        ping_start_time = time()
        ping_success = False
        for _ in range(3):
            try:
                sock.sendto(b'\x0b', (address, port))
                data, addr = sock.recvfrom(10)
                # Ensure the response is correct and from the right server
                if data == b'\x0c' and addr[0] == address:
                    ping_success = True
                    break
            except: break
            sleep(ping_wait)
        if ping_success:
            ping_result = (time() - ping_start_time) * 1000
        else:
            pro.append((dex,999))
            return (999,[])

        j = lambda h: dumps(h).encode('utf-8')
        q = bytes.fromhex
        p = lambda h, e=b'': sock.sendto(q(h.replace(' ','')) + e, (address, port))
        g = lambda b: sock.recvfrom(b)[0]
        # --- Start Handshake ---
        my_handshake = f'{(71 + randint(0, 150)):02x}'
        p(f'18 21 00 {my_handshake}', U().encode())
        # The server's response contains its handshake byte at index 1
        server_handshake = f'{g(3)[1]:02x}'
        g(1024)  # Ack/Server-Info packet

        p(f'24 {server_handshake} 10 21 00', j(SPEC))
        p(f'24 {server_handshake} 11 f0 ff f0 ff 00 12', j(AUTH))
        p(f'24 {server_handshake} 11 f1 ff f0 ff 00 15', j({}))
        p(f'24 {server_handshake} 11 f2 ff f0 ff 00 03')

        g(1024)  # Ack
        g(9)     # Ack
        # --- End Handshake ---

        # --- Roster Grabbing Loop ---
        # Message type IDs
        SERVER_RELIABLE_MESSAGE = 0x25
        BA_SCENEPACKET_MESSAGE = 0x11
        BA_MESSAGE_MULTIPART = 0x0d
        BA_MESSAGE_MULTIPART_END = 0x0e
        BA_MESSAGE_PARTY_ROSTER = 0x09
        roster_parts = bytearray()
        collecting_roster = False
        roster_listen_start_time = time()
        while time() - roster_listen_start_time < (timeout / 2): # Use part of the total timeout
            packet = g(2048) # Increased buffer size for safety

            if not packet or len(packet) < 9: continue

            if packet[0] == SERVER_RELIABLE_MESSAGE and packet[2] == BA_SCENEPACKET_MESSAGE:
                payload_type = packet[8]
                payload_data = packet[9:]

                if payload_type == BA_MESSAGE_PARTY_ROSTER:
                    json_string = payload_data.rstrip(b'\x00').decode('utf-8')
                    roster_result = loads(json_string)
                    break

                elif payload_type == BA_MESSAGE_MULTIPART:
                    if payload_data and payload_data[0] == BA_MESSAGE_PARTY_ROSTER:
                        collecting_roster = True
                        roster_parts.clear()
                        roster_parts.extend(payload_data[1:])
                    elif collecting_roster:
                        roster_parts.extend(payload_data)

                elif payload_type == BA_MESSAGE_MULTIPART_END and collecting_roster:
                    roster_parts.extend(payload_data)
                    json_string = roster_parts.rstrip(b'\x00').decode('utf-8')
                    roster_result = loads(json_string)
                    break
        # --- Send Disconnect ---
        p(f'20 {server_handshake}')

    except: pass
    finally: sock.close()
    pro.append((dex,ping_result))
    return (ping_result, roster_result or [])

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
    #parent=p,
    #texture=gt('softRect'),
    #size=(size[0]*1.2,size[1]*1.2),
    #position=(-size[0]*0.1,-size[1]*0.1),
    #opacity=0.55,
    #color=(0,0,0)
),iw(
    parent=p,
    size=size
))

# Global
BTW = lambda t: (push(t,color=(1,1,0)),gs('block').play())
TIP = lambda t: push(t,Finder.COL3)
lmao = lambda: [
    'Who are we looking for this time?',
    'Press on Fetch, and I\'ll do the rest.',
    'Let\'s legally stalk all servers!',
    'Let\'s list them all!',
    'Relax. We can find them.',
    'Lost your friend? Let\'s find them!',
    'Looking for players? I can help!',
    'Cool art appears here. Fetch already!',
    'Let\'s hear some "How did u find me!?"',
    'Ready as ever. Press on Fetch!',
    'Let\'s sniff out some packets!',
    'Who\'s there? I\'ll see myself!',
    'They can\'t hide!! Muahahaha-',
    'Why did I put a random tip here?',
    'We\'re having rosters for dinner!'
]


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
            label='Buscar',
            color=Finder.COL1,
            textcolor=Finder.COL3,
            size=sz,
            oac=lambda:Finder(s.b)
        )
