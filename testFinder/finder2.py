# Copyright 2025 - Solely by BrotherBoard
# Intended for personal use only
# Bug? Feedback? Telegram >> @BroBordd

"""
Finder v2.0 - Find anyone

Experimental. Feedback is appreciated.
Useful if you are looking for someone, or just messing around.

Features:
- One click to do everything
- Targets all reachable public servers just like gather window
- Sniffs around roster from servers without joining them

Combine with Power plugin for better control.
"""

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

class Finder:
    VER = '2.0'
    COL1 = (0,0.3,0.3)
    COL2 = (0,0.55,0.55)
    COL3 = (0,0.7,0.7)
    COL4 = (0,1,1)
    COL5 = (1,1,0)
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
        s.thr = []
        s.ikids = []
        s.pro = []
        s.sust = None
        s.s1 = s.snd('powerup01')
        c = s.__class__
        # parent
        z = (460,400)
        c.P = cw(
            scale_origin_stack_offset=src.get_screen_space_center(),
            size=z,
            oac=s.bye
        )[0]
        # footing
        sw(
            parent=c.P,
            size=z,
            border_opacity=0
        )
        # fetch
        tw(
            parent=c.P,
            text='Fetch all servers',
            color=s.COL4,
            position=(19,359)
        )
        bw(
            parent=c.P,
            position=(360,343),
            size=(80,39),
            label='Fetch',
            color=s.COL2,
            textcolor=s.COL4,
            oac=s.fresh
        )
        tw(
            parent=c.P,
            text='Sniff out players without joining',
            color=s.COL3,
            scale=0.8,
            position=(15,330),
            maxwidth=320
        )
        # separator
        iw(
            parent=c.P,
            size=(429,1),
            position=(17,330),
            texture=gt('white'),
            color=s.COL2
        )
        # cube art
        c.ARTT = tw(
            parent=c.P,
            text='' if c.ART else f'Finder v{c.VER}\n{CH(lmao())}',
            maxwidth=430,
            max_height=125,
            h_align='center',
            v_align='top',
            color=s.COL4,
            position=(205,295),
        )
        # separator
        iw(
            parent=c.P,
            size=(429,1),
            position=(17,200),
            texture=gt('white'),
            color=s.COL2
        )
        # filter
        c.FT = tw(
            parent=c.P,
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
            parent=c.P,
            position=(26,153),
            text='Search',
            color=s.COL3
        )
        # players
        p1 = sw(
            parent=c.P,
            position=(20,18),
            size=(205,122),
            border_opacity=0.4,
            color=s.COL4
        )
        c.P2 = ocw(
            parent=p1,
            size=(205,1),
            background=False
        )
        s.pltip = tw(
            parent=c.P,
            position=(90,100),
            text='Sniff some servers\nto collect players\nResults vary by\ntime and connection',
            color=s.COL4,
            maxwidth=175,
            h_align='center'
        )
        # info
        iw(
            parent=c.P,
            position=(235,18),
            size=(205,172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'),
            opacity=0.4
        )
        s.tip = 'Select something to\nview server info'
        c.TIP = tw(
            parent=c.P,
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
        tw(s.ft2,text=['Search',''][bool(ct)])
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
                parent=c.P,
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

        s.ikids.append(bw(
            parent=c.P,
            position=(253,65),
            size=(166,30),
            label=p,
            color=s.COL2,
            textcolor=s.COL4,
            oac=Call(s.oke,'\n'.join([' | '.join([str(j) for j in _.values()]) for _ in pz]) or 'Nothing')
        ))
        s.ikids.append(bw(
            parent=c.P,
            position=(253,30),
            size=(166,30),
            label='Connect',
            color=s.COL2,
            textcolor=s.COL4,
            oac=Call(CON,i['a'],i['p'],False)
        ))
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
        ocw(c.P,transition='out_scale')
        l = s.snd('laser')
        f = lambda: teck(0.01,f) if c.P else l.stop()
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
        TIP('Scanning servers!\nThis should take a few seconds!\nYou can close this window.')
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
        tw(c.ARTT,text=('\n'.join(''.join(c.ART[i:i+40]) for i in range(0,len(s.ART),40))))
        s.up()
    def up(s):
        c = s.__class__
        [_.delete() for _ in c.KIDS]
        c.KIDS.clear()
        pl = s.plys()
        s.pltip.delete() if pl else 0
        sy = max(len(pl)*30,90)
        ocw(c.P2,size=(205,sy))
        dun = 0
        for _,g in enumerate(pl):
            p,a = g
            tt = tw(
                parent=c.P2,
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
            if not dun and p == c.SL: ocw(c.P2,visible_child=tt); dun = 1
            c.KIDS.append(tt)
    def done(s):
        s.ding(0,1)
        [_.join() for _ in s.thr]
        s.thr.clear()
        c = s.__class__
        tt = time() - c.ST
        ln = len(s.MEM)
        ab = int(ln/tt)
        TIP(f'Finished!\nScanned {ln} servers in {round(tt,2)} seconds!\nAbout {ab} server{["s",""][ab<2]}/sec')
        s.__class__.BUSY = False

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

# ba_meta require api 9
# ba_meta export babase.Plugin
class byBordd(Plugin):
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
            label='Finder',
            color=Finder.COL1,
            textcolor=Finder.COL3,
            size=sz,
            oac=lambda:Finder(s.b)
        )
