# ba_meta require api 9
# ba_meta name Auto Respond
# ba_meta description A mod that allows you to have automatic replies to specific messages
# ba_meta version 2.8

from babase import (
    clipboard_is_supported as CIS,
    clipboard_get_text as CGT,
    clipboard_has_text as CHT,
    Plugin
)
from bauiv1 import (
    get_special_widget as gsw,
    containerwidget as cw,
    screenmessage as push,
    checkboxwidget as chk,
    scrollwidget as sw,
    buttonwidget as bw,
    SpecialChar as sc,
    textwidget as tw,
    checkboxwidget as cb,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    UIScale as uis,
    charstr as cs,
    app as APP,
    Call,
    CallStrict,
    CallPartial
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM
)
from _babase import get_string_width as strw
from datetime import datetime as DT
from bauiv1lib import party

class Add:
    """Add a response"""
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(300,295),
            ps=AR.UIS()*0.8
        )
        a = []
        for i in range(2):
            j = ['If found','Respond with'][i]
            tw(
                parent=w,
                text=j+':',
                position=(30,250-70*i)
            )
            t = tw(
                parent=w,
                maxwidth=230,
                size=(230,30),
                editable=True,
                v_align='center',
                color=(0.75,0.75,0.75),
                position=(30,218-70*i),
                allow_clear_button=False
            )
            a.append(t)
            AR.bw(
                parent=w,
                size=(20,30),
                iconscale=1.3,
                icon=gt('file'),
                position=(265,218-70*i),
                on_activate_call=CallStrict(s.paste,a[i])
            )
        for i in range(2):
            tw(
                parent=w,
                text=['After','seconds'][i],
                position=(30+160*i,105)
            )
        s.t = tw(
            parent=w,
            size=(90,30),
            editable=True,
            text=var('time'),
            h_align='center',
            position=(95,105),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        s.cbv = False
        s.cb = cb(
            parent=w,
            size=(250,30),
            position=(27.5,65),
            text='Search in message',
            value=s.cbv,
            on_value_change_call=CallPartial(setattr,s,'cbv'),
            color=(0.75,0.75,0.75),
            textcolor=(1,1,1),
        )
        tw(
            parent=w,
            scale=0.6,
            position=(20,37.5),
            text=f'%m: Your v2 name ({byBordd.me()})\n%s: Sender name\n%t: Time (HH:MM:SS)',
            maxwidth=190,
            color=(0.65,0.65,0.65)
        )
        AR.bw(
            parent=w,
            label='Add',
            size=(50,35),
            position=(230,25),
            on_activate_call=CallStrict(s._add,a)
        )
        AR.swish()
    def _add(s,a):
        """Actually add"""
        z = tw(query=s.t)
        try: z = float(z)
        except: AR.err('Invalid time. Fix your input!'); return
        var('time',str(z))
        i,j = [tw(query=t).strip().replace('\n',' ') for t in a]
        if not i or not j: AR.err('Write something!'); return
        l = var('l') or {}
        lc = var('lc') or {}
        ic = i.lower()
        if ic in lc: AR.err('Trigger already exists!'); return
        l.update({i:(j,z,s.cbv)})
        lc.update({ic:(j,z,s.cbv)})
        var('l',l)
        var('lc',lc)
        [tw(t,text='') for t in a]
        AR.ok()
    def paste(s,t):
        """Paste"""
        if not CIS(): AR.err('Unsupported!'); return
        if not CHT(): AR.err('Your clipboard is empty!'); return
        tw(t,text=CGT().replace('\n',' '),color=(0,1,0))
        gs('gunCocking').play()
        teck(0.3,Call(tw,t,color=(1,1,1)))
        push('Pasted!',color=(0,1,0))

class Nuke:
    """Nuke a response"""
    def __init__(s,t):
        i = len(var('l'))
        if not i: AR.err('Add some triggers first!'); return
        w = AR.cw(
            source=t,
            size=(260,350),
            ps=AR.UIS()*0.5
        )
        a = sw(
            parent=w,
            size=(220,290),
            position=(20,40)
        )
        s.c = cw(
            parent=a,
            size=(220,i*30),
            background=False
        )
        AR.bw(
            parent=w,
            label='Nuke',
            size=(60,25),
            position=(180,10),
            on_activate_call=CallStrict(s._nuke)
        )
        s.kids = []
        s.sl = None
        s.fresh()
        AR.swish()
    def _nuke(s):
        """Actually nuke"""
        if s.sl is None: AR.err('Select something!'); return
        l = var('l')
        lc = var('lc')
        l.pop(list(l)[s.sl])
        lc.pop(list(lc)[s.sl])
        var('l',l)
        var('lc',lc)
        s.sl = None
        s.fresh()
        AR.bye()
    def fresh(s):
        """Refresh"""
        [k.delete() for k in s.kids]
        s.kids.clear()
        l = var('l'); k = list(l); j = len(l)
        [s.kids.append(tw(
            text=k[i],
            parent=s.c,
            size=(220,30),
            selectable=True,
            click_activate=True,
            position=(0,(30*j)-30*(i+1)),
            on_activate_call=CallStrict(s.hl,i),
        )) for i in range(j)]
        cw(s.c,size=(220,j*30))
    def hl(s,i):
        """Highlight"""
        [tw(t,color=(1,1,1)) for t in s.kids]
        tw(s.kids[i],color=(0,1,0))
        s.sl = i

class Tune:
    """The settings"""
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,190),
            ps=AR.UIS()*0.8
        )
        AR.swish()
        for i in range(4):
            j = [
                'Notify upon responding',
                'Ding upon responding',
                'Respond to '+byBordd.me(),
                'Case sensitive'
            ][i]
            c = f'tune{i}'
            chk(
                text=j,
                parent=w,
                size=(290,30),
                textcolor=(1,1,1),
                value=var(c),
                position=(30,20+40*i),
                color=(0.13,0.13,0.13),
                on_value_change_call=CallPartial(var,c)
            )

class List:
    """List responses"""
    def __init__(s,t):
        i = len(var('l'))
        if not i: AR.err('Add some triggers first!'); return
        w = AR.cw(
            source=t,
            size=(450,300),
            ps=AR.UIS()*0.8
        )
        a = sw(
            parent=w,
            size=(150,260),
            position=(30,20)
        )
        s.c = cw(
            parent=a,
            size=(220,i*30),
            background=False,
        )
        s.txt = []
        for i in range(3):
            j = ['Trigger','Response','Parsed'][i]
            k = [(0,1,1),(1,1,0),(1,0,1)][i]
            tw(
                color=k,
                parent=w,
                text=j+':',
                position=(190,240-80*i)
            )
            t = tw(
                parent=w,
                maxwidth=250,
                max_height=60,
                v_align='top',
                position=(190,215-80*i)
            )
            s.txt.append(t)
        bw(
            parent=w,
            position=(390,240),
            size=(40,40),
            label='',
            texture=gt('achievementEmpty'),
            on_activate_call=s.info,
            color=(1,1,1),
            enable_sound=False
        )
        s.kids = []
        s.sl = None
        s.fresh()
        AR.swish()
    """Show info"""
    def info(s):
        i = s.sl
        if i is None: AR.err('Select a trigger first!'); return
        a,b,c = list(var('l').items())[i][1]
        push(f'Trigger order: {i+1}\nResponds after: {b} seconds\nWildcard: {c}')
        gs('tap').play()
    """Refesh"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        l = var('l'); k = list(l); j = len(l)
        [s.kids.append(tw(
            text=k[i],
            parent=s.c,
            size=(150,30),
            selectable=True,
            click_activate=True,
            position=(0,(30*j)-30*(i+1)),
            on_activate_call=CallStrict(s.hl,i),
        )) for i in range(j)]
        cw(s.c,size=(220,j*30))
    """Highlight"""
    def hl(s,i):
        [tw(t,color=(1,1,1)) for t in s.kids]
        tw(s.kids[i],color=(0,1,0))
        s.sl = i
        l = var('l')
        v = list(l)[i]
        r = l[v][0]
        p = AR.parse(t=r)
        [tw(s.txt[i],text=sn([v,r,p][i])) for i in range(3)]

"""The AutoRespond base"""
class AR:
    @classmethod
    def UIS(c=0):
        i = APP.ui_v1.uiscale
        return [1.5,1.1,0.8][0 if i == uis.SMALL else 1 if i == uis.MEDIUM else 2]
    @classmethod
    def parse(c=0,t=0,s=None):
        me = byBordd.me()
        return t.replace('%t',DT.now().strftime("%H:%M:%S")).replace('%s',s or byBordd.v2+'BroBordd').replace('%m',me)
    @classmethod
    def bw(c,**k):
        return bw(
            **k,
            textcolor=(1,1,1),
            enable_sound=False,
            button_type='square',
            color=(0.18,0.18,0.18)
        )
    @classmethod
    def cw(c,source,ps=0,**k):
        o = source.get_screen_space_center() if source else None
        r = cw(
            **k,
            scale=c.UIS()+ps,
            transition='in_scale',
            color=(0.18,0.18,0.18),
            parent=gsw('overlay_stack'),
            scale_origin_stack_offset=o
        )
        cw(r,on_outside_click_call=CallStrict(c.swish,t=r))
        return r
    swish = lambda c=0,t=0: (gs('swish').play(),cw(t,transition='out_scale') if t else t)
    err = lambda t: (gs('block').play(),push(t,color=(1,1,0)))
    ok = lambda: (gs('dingSmallHigh').play(),push('Okay!',color=(0,1,0)))
    bye = lambda: (gs('laser').play(),push('Bye!',color=(0,1,0)))
    def __init__(s, source: bw = None) -> None:
        w = s.w = s.cw(
            source=source,
            size=(260,370),
        )
        [tw(
            scale=2,
            parent=w,
            text='Auto',
            h_align='center',
            position=(65-i*3,325-i*3),
            color=[(1,1,1),(0.6,0.6,0.6)][i]
        ) for i in [1,0]]
        mem = globals()
        for i in range(4):
            j = ['Add','Nuke','Tune','List'][i]
            k = ['O','A','U','Y'][i]
            b = s.bw(
                label=j,
                parent=w,
                size=(200,65),
                position=(30,230-70*i),
                icon=gt(f'ouya{k}Button')
            )
            bw(b,on_activate_call=CallStrict(mem[j],b))
        s.b = bw(
            parent=w,
            size=(60,40),
            position=(155,315),
            enable_sound=False,
            button_type='square',
            on_activate_call=s.but
        )
        s.but(1)
        s.swish()
    def but(s,dry=0):
        v = var('state')
        if not dry:
            v = [1,0][v]
            var('state',v)
            gs('deek').play()
        bw(
            s.b,
            label=['OFF','ON'][v],
            color=[(0.35,0,0),(0,0.45,0)][v],
            textcolor=[(0.5,0,0),(0,0.6,0)][v]
        )

# Config
pr = 'ar3_'
def var(s,v=None):
    c = APP.config
    s = pr+s
    if v is None: return c.get(s,v)
    c[s] = v
    c.commit()
def reset_conf(): cfg = APP.config; [(cfg.pop(c) if c.startswith(pr) else None) for c in cfg.copy()]; cfg.commit()

# Default
for i in range(4): j = f'tune{i}'; v = var(j); var(j,i<3) if v is None else v
None if var('state') else var('state',1)
None if var('time') else var('time','0.5')
None if var('l') else var('l',{})
None if var('lc') else var('lc',{})

# Mini tools
SW = lambda s: strw(s,suppress_warning=True)
def sn(s):
    out = ''
    w = 0.0
    for c in s:
        ch_w = SW(c)
        if w + ch_w > 520:
            out += '\n'
            w = 0.0
        out += c
        w += ch_w
    return out

# ba_meta export babase.Plugin
class byBordd(Plugin):
    me = lambda c=0: APP.plus.get_v1_account_name() if APP.plus.get_v1_account_state() == 'signed_in' else '???'
    v2 = cs(sc.V2_LOGO)
    B = '​'
    def __init__(s):
        o = party.PartyWindow.__init__
        def e(s,*a,**k):
            r = o(s,*a,**k)
            b = AR.bw(
                icon=gt('achievementOutline'),
                position=(s._width-15,s._height-45),
                parent=s._root_widget,
                iconscale=0.7,
                size=(90,30),
                label='Auto'
            )
            bw(b,on_activate_call=CallStrict(AR,source=b))
            return r
        party.PartyWindow.__init__ = e
        s.z = []
        teck(5,s.ear)
    def ear(s):
        z = GCM()
        teck(0.3,s.ear)
        if z == s.z: return
        s.z = z;
        v = z[-1]
        if v.endswith(s.B): return
        f,m = v.split(': ',1)
        k = s.me()
        if f in [k,s.v2+k] and not var('tune2'): return
        if var('tune3'): l = var('l')
        else: # any
            m = m.lower()
            l = var('lc')
        h = l.get(m,None)
        if h is not None: # equal
            a,b,_ = h
            s.S(b,a,f,0)
        else: # wild
            re = [y for y,_ in sorted([(y,m.find(y)) for y in l if y in m],key=lambda x: x[1])]
            for r in re:
                a,b,c = l.get(r,[0,0,0])
                if not r or not c: continue # unwild :c
                s.S(b,a,f,1)
    def S(s,b,a,f,j):
        if not var('state'): return # ignore
        p = AR.parse(t=a,s=f)
        teck(b,Call(CM,p+s.B))
        push(f"{['Equals','Contains'][j]}!\nReplying to: {f}\nWith text: {p}\nAfter {b} seconds!",color=(0,0.8,0.8)) if var('tune0') else None
        gs('dingSmallHigh').play() if var('tune1') else None
