# ba_meta require api 9
from baenv import TARGET_BALLISTICA_BUILD as build_number
import os
import json
import math
import weakref
import time
import babase
import bauiv1 as bui
import bascenev1 as bs
import _babase
from bauiv1lib.popup import PopupMenuWindow, PopupWindow, PopupMenu
from bauiv1lib.confirm import ConfirmWindow
from bauiv1lib.colorpicker import ColorPickerExact
from bauiv1lib.mainmenu import MainMenuWindow
from typing import List, Tuple, Sequence, Optional, Dict, Any, Union, TYPE_CHECKING, cast
import bauiv1lib.party
import urllib.request, pickle
from time import sleep
from threading import Thread
import random
import datetime
import logging

_ip = '127.0.0.1'
_port = 43210
_ping = '-'
url = 'http://bombsquadprivatechat.ml'
last_msg = None

my_directory = _babase.env()['python_directory_user'] + '/UltraPartyWindowFiles/'
quick_msg_file = my_directory +  'QuickMessages.txt'
cookies_file = my_directory + 'cookies.txt'
blacklist_file = my_directory + 'BlackList.txt'
love_file = my_directory + 'Love.txt'
saved_ids_file = my_directory + 'saved_ids.json'

def initialize():
    config_defaults = {
        'Party Chat Muted':False,
        'Chat Muted': False,
        'ping button': True,
        'IP button': True,
        'copy button': True,
        'Direct Send': False,
        'Colorful Chat': True,
        'Custom Commands': [],
        'Message Notification': 'bottom',
        'Self Status': 'online'
    }
    
    config = babase.app.config
    for key in config_defaults:
        if key not in config:
            config[key] = config_defaults[key]

    if not os.path.exists(my_directory):
        os.makedirs(my_directory)
    if not os.path.exists(cookies_file):
        with open(cookies_file, 'wb') as f:
            pickle.dump({}, f)
    if not os.path.exists(saved_ids_file):
        with open(saved_ids_file, 'w') as f:
            data = {}
            json.dump(data, f)

def display_error(msg=None):
    if msg:
        bui.screenmessage(msg, (1,0,0))
    else:
        bui.screenmessage('Failed!', (1,0,0))
    bui.getsound('error').play()

def display_success(msg=None):
    if msg:
        bui.screenmessage(msg, (0,1,0))
    else:
        bui.screenmessage('Successful!', (0,1,0))


class ColorTracker:
    def __init__(self):
        self.saved = {}
    def _get_safe_color(self, sender):
        while True:
            color = (random.random(), random.random(), random.random())
            s = 0
            background = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
            for i,j in zip(color, background):
                s += (i - j) ** 2
            if s > 0.1:
                self.saved[sender] = color
                if len(self.saved) > 20:
                    self.saved.pop(list(self.saved.keys())[0])
                break
            time.sleep(0.1)
    def _get_sender_color(self, sender):
        if sender not in self.saved:
            self.thread = Thread(target=self._get_safe_color, args=(sender,))
            self.thread.start()
            return (1,1,1)
        else:
            return self.saved[sender]


class PrivateChatHandler:
    def __init__(self):
        self.pvt_msgs = {}
        self.login_id = None
        self.last_msg_id = None
        self.logged_in = False
        self.cookieProcessor = urllib.request.HTTPCookieProcessor()
        self.opener = urllib.request.build_opener(self.cookieProcessor)
        self.filter = 'all'
        self.pending_messages = []
        self.friends_status = {}
        self._ping()

    def _load_ids(self):
        with open(saved_ids_file, 'r') as f:
            saved = json.load(f)
            if self.myid in saved:
                self.saved_ids = saved[self.myid]
            else:
                self.saved_ids = {'all': '<all>'}

    def _dump_ids(self):
        with open(saved_ids_file, 'r') as f:
            saved = json.load(f)
        with open(saved_ids_file, 'w') as f:
            saved[self.myid] = self.saved_ids
            json.dump(saved, f)

    def _ping(self):
        self.server_online = False
        response = self._send_request(url = f'{url}')
        if not response:
            self.error = 'Server offline'
        elif response in ['v1.0', 'v2.0']:
            self.server_online = True
        else:
            self.error = 'Update party window'

    def _signup(self, registration_key):
        data = dict(pb_id = self.myid, registration_key = registration_key)
        response = self._send_request(url = f'{url}/signup', data=data)
        if response:
            if response == 'successful':
                display_success('Account Created Successfully')
                self._login(registration_key = registration_key)
                return True
            display_error(response)

    def _save_cookie(self):
        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)
        with open(cookies_file, 'wb') as f:
            for c in self.cookieProcessor.cookiejar:
                cookie = pickle.dumps(c)
                break
            cookies[self.myid] = cookie
            pickle.dump(cookies, f)

    def _cookie_login(self):
        self.myid = _babase.get_v1_account_misc_read_val_2('resolvedAccountID', '')
        try:
            with open(cookies_file, 'rb') as f:
                cookies = pickle.load(f)
        except:
            return False
        if self.myid in cookies:
            cookie = pickle.loads(cookies[self.myid])
            self.cookieProcessor.cookiejar.set_cookie(cookie)
            self.opener = urllib.request.build_opener(self.cookieProcessor)
            response = self._send_request(url=f'{url}/login')
            if response.startswith('logged in as'):
                self.logged_in = True
                self._load_ids()
                display_success(response)
                return True

    def _login(self, registration_key):
        self.myid = _babase.get_v1_account_misc_read_val_2('resolvedAccountID', '')
        data = dict(pb_id = self.myid, registration_key = registration_key)
        print(f"[_login]: Test {url}/login")
        response = self._send_request(url = f'{url}/login', data=data)
        if response == 'successful':
            self.logged_in = True
            self._load_ids()
            self._save_cookie()
            display_success('Account Logged in Successfully')
            return True
        else:
            display_error(response)

    def _query(self, pb_id=None):
        if not pb_id:
            pb_id = self.myid
        print(f"[_query]: Test {url}/query/{pb_id}")
        response = self._send_request(url = f'{url}/query/{pb_id}')
        if response == 'exists':
            return True
        return False

    def _send_request(self, url, data=None):
        try:
            if not data:
                response = self.opener.open(url)
            else:
                response = self.opener.open(url, data=json.dumps(data).encode())
            if response.getcode() != 200:
                display_error(response.read().decode())
                return None
            else:
                return response.read().decode()
        except:
            return None

    def _save_id(self, account_id, nickname='<default>', verify=True):
        #display_success(f'Saving {account_id}. Please wait...')
        if verify:
            url = 'http://bombsquadgame.com/accountquery?id=' + account_id
            response = json.loads(urllib.request.urlopen(url).read().decode())
            if 'error' in response:
                display_error('Enter valid account id')
                return False
            self.saved_ids[account_id] = {}
            name = None
            if nickname == '<default>':
                name_html = response['name_html']
                name = name_html.split('>')[1]
            nick = name if name else nickname
        else:
            nick = nickname
        self.saved_ids[account_id] = nick
        self._dump_ids()
        display_success(f'Account added: {nick}({account_id})')
        return True

    def _remove_id(self, account_id):
        removed = self.saved_ids.pop(account_id)
        self._dump_ids()
        bui.screenmessage(f'Removed successfully: {removed}({account_id})', (0,1,0))
        bui.getsound('shieldDown').play()

    def _format_message(self, msg):
        filter = msg['filter']
        if filter in self.saved_ids:
            if self.filter == 'all':
                message = '[' + self.saved_ids[filter] + ']' + msg['message']
            else:
                message = msg['message']
        else:
            message = '[' + msg['filter'] + ']: ' + 'Message from unsaved id. Save id to view message.'
        return message

    def _get_status(self, id, type='status'):
        info = self.friends_status.get(id, {})
        if not info:
            return '-'
        if type == 'status':
            return info['status']
        else:
            last_seen = info["last_seen"]
            last_seen = _get_local_time(last_seen)
            bui.screenmessage(f'Last seen on: {last_seen}')


def _get_local_time(utctime):
    d = datetime.datetime.strptime(utctime, '%d-%m-%Y %H:%M:%S')
    d = d.replace(tzinfo=datetime.timezone.utc)
    d = d.astimezone()
    return d.strftime('%B %d,\t\t%H:%M:%S')

def _creat_Lstr_list(string_list: list = []) -> list:
    return ([babase.Lstr(resource="??Unknown??", fallback_value=item) for item in string_list])

def update_status():
    if messenger.logged_in:
        if babase.app.config['Self Status'] == 'online':
            host = bs.get_connection_to_host_info().get('name', '')
            if host:
                my_status = f'Playing in {host}'
            else:
                my_status = 'in Lobby'
            ids_to_check = [i for i in messenger.saved_ids if i != 'all']
            response = messenger._send_request(url = f'{url}/updatestatus', data = dict(self_status = my_status, ids = ids_to_check))
            if response:
                messenger.friends_status = json.loads(response)
        else:
            messenger.friends_status = {}

def messenger_thread():
    counter = 0
    while True:
        counter += 1
        time.sleep(0.6)
        check_new_message()
        if counter > 5:
            counter = 0
            update_status()

def check_new_message():
    if messenger.logged_in:
        if messenger.login_id != messenger.myid:
            response = messenger._send_request(f'{url}/first')
            if response:
                messenger.pvt_msgs = json.loads(response)
                if messenger.pvt_msgs['all']:
                    messenger.last_msg_id = messenger.pvt_msgs['all'][-1]['id']
                    messenger.login_id = messenger.myid
        else:
            response = messenger._send_request(f'{url}/new/{messenger.last_msg_id}')
            if response:
                new_msgs = json.loads(response)
                if new_msgs:
                    for msg in new_msgs['messages']:
                        if msg['id'] > messenger.last_msg_id:
                            messenger.last_msg_id = msg['id']
                            messenger.pvt_msgs['all'].append(dict(id=msg['id'], filter=msg['filter'], message=msg['message'], sent=msg['sent']))
                            if len(messenger.pvt_msgs['all']) > 40:
                                messenger.pvt_msgs['all'].pop(0)
                            if msg['filter'] not in messenger.pvt_msgs:
                                messenger.pvt_msgs[msg['filter']] = [dict(id=msg['id'], filter=msg['filter'], message=msg['message'], sent=msg['sent'])]
                            else:
                                messenger.pvt_msgs[msg['filter']].append(dict(id=msg['id'], filter=msg['filter'], message=msg['message'], sent=msg['sent']))
                                if len(messenger.pvt_msgs[msg['filter']]) > 20:
                                    messenger.pvt_msgs[msg['filter']].pop(0)
                            messenger.pending_messages.append((messenger._format_message(msg), msg['filter'], msg['sent']))

def display_message(msg, msg_type, filter=None, sent=None):
    flag = None
    notification = babase.app.config['Message Notification']
    if bui.app.ui_v1.party_window:
      if bui.app.ui_v1.party_window():
        if bui.app.ui_v1.party_window()._private_chat:
            flag = 1
            if msg_type == 'private':
                if messenger.filter == filter or messenger.filter == 'all':
                    bui.app.ui_v1.party_window().on_chat_message(msg, sent)
                else:
                    if notification == 'top':
                        bui.screenmessage(msg, (1, 1, 0), True, bui.gettexture('coin'))
                    else:
                        bui.screenmessage(msg, (1, 1, 0), False)
            else:
                bui.screenmessage(msg, (0.2, 1.0, 1.0), True, bui.gettexture('circleShadow'))
        else:
            flag = 1
            if msg_type == 'private':
                if notification == 'top':
                    bui.screenmessage(msg, (1, 1, 0), True, bui.gettexture('coin'))
                else:
                    bui.screenmessage(msg, (1, 1, 0), False)
    if not flag:
        if msg_type == 'private':
            if notification == 'top':
                bui.screenmessage(msg, (1, 1, 0), True, bui.gettexture('coin'))
            else:
                bui.screenmessage(msg, (1, 1, 0), False)
        else:
            bui.screenmessage(msg, (0.2, 1.0, 1.0), True, bui.gettexture('circleShadow'))

def msg_displayer():
    for msg in messenger.pending_messages:
        display_message(msg[0], 'private', msg[1], msg[2])
        messenger.pending_messages.remove(msg)
    if babase.app.config['Chat Muted'] and not babase.app.config['Party Chat Muted']:
        global last_msg
        last = bs.get_chat_messages()
        lm = last[-1] if last else None
        if lm != last_msg:
            last_msg = lm
            display_message(lm, 'public')


class SortQuickMessages:
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
        self._width = 750 if uiscale is babase.UIScale.SMALL else 600
        self._height = (300 if uiscale is babase.UIScale.SMALL else
                        325 if uiscale is babase.UIScale.MEDIUM else 350)
        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            on_outside_click_call=self._save,
            color=bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.3 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -16) if uiscale is babase.UIScale.SMALL else (0,0)
        )
        
        bui.textwidget(parent=self._root_widget,
            position=(-10, self._height - 50),
            size=(self._width, 25),
            text='Sort Quick Messages',
            color=bui.app.ui_v1.title_color,
            scale=1.05,
            h_align='center',
            v_align='center',
            maxwidth=270
        )
        
        b_textcolor = (0.4, 0.75, 0.5)
        up_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10, 170),
            size=(75, 75),
            on_activate_call=self._move_up,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True
        )

        down_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10,75),
            size=(75, 75),
            on_activate_call=self._move_down,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True
        )

        self._scroll_width = self._width - 150
        self._scroll_height = self._height - 110
        
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._scroll_height),
            color=bg_color,
            position=(100,40)
        )
        
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0
        )
        
        with open(quick_msg_file, 'r') as f:
            self.msgs = f.read().split('\n')
        
        self._msg_selected = None
        self._refresh()
        
        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._save
        )

    def _refresh(self):
        for child in self._columnwidget.get_children():
            child.delete()
        for msg in enumerate(self.msgs):
            txt = bui.textwidget(
                parent = self._columnwidget,
                size=(self._scroll_width - 10, 30),
                selectable=True,
                always_highlight=True,
                on_select_call=babase.Call(self._on_msg_select, msg),
                text=msg[1],
                h_align='left',
                v_align='center',
                maxwidth=self._scroll_width)
            if msg == self._msg_selected:
                bui.columnwidget(edit=self._columnwidget,
                    selected_child=txt,
                    visible_child=txt)

    def _on_msg_select(self, msg):
        self._msg_selected = msg

    def _move_up(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index:
            self.msgs.insert((index - 1), self.msgs.pop(index))
            self._msg_selected = (index-1, msg)
            self._refresh()

    def _move_down(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index + 1 < len(self.msgs):
            self.msgs.insert((index + 1), self.msgs.pop(index))
            self._msg_selected = (index+1, msg)
            self._refresh()

    def _save(self) -> None:
        try:
            with open(quick_msg_file, 'w') as f:
                f.write('\n'.join(self.msgs))
        except:
            logging.exception()
            bui.screenmessage('Error!', (1,0,0))
        bui.containerwidget(
            edit=self._root_widget,
            transition='out_right')
        

class SortBlacklistUsers:
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
        self._width = 750 if uiscale is babase.UIScale.SMALL else 600
        self._height = (300 if uiscale is babase.UIScale.SMALL else
                        325 if uiscale is babase.UIScale.MEDIUM else 350)
        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            on_outside_click_call=self._save,
            color=bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.3 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -16) if uiscale is babase.UIScale.SMALL else (0,0)
        )
        
        bui.textwidget(parent=self._root_widget,
            position=(-10, self._height - 50),
            size=(self._width, 25),
            text='Sort Quick Messages',
            color=bui.app.ui_v1.title_color,
            scale=1.05,
            h_align='center',
            v_align='center',
            maxwidth=270
        )
        
        b_textcolor = (0.4, 0.75, 0.5)
        up_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10, 170),
            size=(75, 75),
            on_activate_call=self._move_up,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True
        )

        down_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10,75),
            size=(75, 75),
            on_activate_call=self._move_down,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True
        )

        self._scroll_width = self._width - 150
        self._scroll_height = self._height - 110
        
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._scroll_height),
            color=bg_color,
            position=(100,40)
        )
        
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0
        )
        
        with open(blacklist_file, 'r') as f:
            self.msgs = f.read().split('\n')
        
        self._msg_selected = None
        self._refresh()
        
        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._save
        )

    def _refresh(self):
        for child in self._columnwidget.get_children():
            child.delete()
        for msg in enumerate(self.msgs):
            txt = bui.textwidget(
                parent = self._columnwidget,
                size=(self._scroll_width - 10, 30),
                selectable=True,
                always_highlight=True,
                on_select_call=babase.Call(self._on_msg_select, msg),
                text=msg[1],
                h_align='left',
                v_align='center',
                maxwidth=self._scroll_width)
            if msg == self._msg_selected:
                bui.columnwidget(edit=self._columnwidget,
                    selected_child=txt,
                    visible_child=txt)

    def _on_msg_select(self, msg):
        self._msg_selected = msg

    def _move_up(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index:
            self.msgs.insert((index - 1), self.msgs.pop(index))
            self._msg_selected = (index-1, msg)
            self._refresh()

    def _move_down(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index + 1 < len(self.msgs):
            self.msgs.insert((index + 1), self.msgs.pop(index))
            self._msg_selected = (index+1, msg)
            self._refresh()

    def _save(self) -> None:
        try:
            with open(blacklist_file, 'w') as f:
                f.write('\n'.join(self.msgs))
        except:
            logging.exception()
            bui.screenmessage('Error!', (1,0,0))
        bui.containerwidget(
            edit=self._root_widget,
            transition='out_right')
        

class BlacklistManager:
    def __init__(self, blacklist_file, bui):
        self.blacklist_file = blacklist_file
        self.bui = bui

    def search_blacklist_users(self):
        try:
            # Get the list of connected players from the host's roster
            try:
                self.roster = bs.get_game_roster()
            except Exception as e:
                self.roster = []
                logging.exception("No se pudo obtener el roster de jugadores")

            # Build the list of names from the roster
            users = []
            for player in self.roster:
                display_name = player.get('display_string', '')
                if display_name:
                    users.append(display_name)
                for p in player.get('players', []):
                    name = p.get('name_full')
                    if name:
                        users.append(name)

            # Clean up rare and duplicate characters
            cleaned_namelist = list(set(name.replace('', '').strip() for name in users if name))

            # Read the blacklist
            if os.path.exists(self.blacklist_file):
                with open(self.blacklist_file, 'r') as f:
                    blacklist = set(line.strip().replace('', '') for line in f if line.strip())
            else:
                blacklist = set()

            # Show both lists
            #print("\nLista proporcionada:")
            #for name in cleaned_namelist:
            #    print(f"- {name}")

            #print("\nBlacklist actual:")
            #for name in blacklist:
            #    print(f"- {name}")

            # Comparation
            intersection = set(cleaned_namelist) & blacklist
            if intersection:
                #print("\nUsuarios en ambas listas:")
                self.bui.screenmessage(f'Saliendo de partida, se encontraron usarios bloquados, cuidate ;)', (1, 1, 0))
                
                for user in intersection:
                    self.bui.screenmessage(f'Usuario detectado: {user}', (1, 1, 0))
                self._end_game()
            #else:
                #print("\n❌ No hay usuarios en ambas listas")

        except Exception:
            logging.exception("Error comparando listas con la blacklist")
            self.bui.screenmessage('Error comparando listas con la blacklist!', (1, 0, 0))

    def send_user_to_black_list(self, namelist):
        try:
            accountv2name = namelist[0]

            if os.path.exists(self.blacklist_file):
                with open(self.blacklist_file, 'r') as f:
                    blacklist = set(line.strip() for line in f if line.strip())
            else:
                blacklist = set()

            if accountv2name not in blacklist:
                blacklist.add(accountv2name)
                with open(self.blacklist_file, 'w') as f:
                    f.write('\n'.join(sorted(blacklist)))

                self.bui.screenmessage(f'Usuario {accountv2name} guardado en la blackList. Saliendo de la partida...', (0, 1, 0))
                self.bui.getsound('dingSmallHigh').play()
            else:
                self.bui.screenmessage(f'El usuario {accountv2name} ya está en la blackList', (1, 1, 0))
        except Exception:
            logging.exception("Error guardando usuario en la blacklist")
            self.bui.screenmessage('Error guardando este usuario en la blacklist!', (1, 0, 0))
            self.bui.getsound('error').play()
        finally:
            self._end_game()

#    def _end_game(self) -> None:
#        assert bui.app.classic is not None
#
#        # no-op if our underlying widget is dead or on its way out.
#        if not self._root_widget or self._root_widget.transitioning_out:
#            return
#
#        bui.containerwidget(edit=self._root_widget, transition='out_left')
#        bui.app.classic.return_to_main_menu_session_gracefully(reset_ui=False)

    def _end_game(self) -> None:
        assert bui.app.classic is not None

        # If you have UI open, close it
        if hasattr(self, '_root_widget') and self._root_widget and not self._root_widget.transitioning_out:
            bui.containerwidget(edit=self._root_widget, transition='out_left')

        # Always exit to menu
        bui.app.classic.return_to_main_menu_session_gracefully(reset_ui=False)

    #def start_blacklist_monitor(self):
    #    def monitor():
    #        while True:
    #            if os.path.exists(self.blacklist_file):
    #                with open(self.blacklist_file, 'r') as f:
    #                    users = [line.strip() for line in f if line.strip()]
    #                    for user in users:
    #                        print(f'[BlackList] Usuario: {user}')
    #                        # self.bui.screenmessage(f'[BlackList] Usuario: {user}', (1, 1, 1))
    #            time.sleep(2)
    #
    #    t = Thread(target=monitor, daemon=True)
    #    t.start()


class SettingsWindow:
    """Window for answering simple yes/no questions."""

    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        height = (300 if uiscale is babase.UIScale.SMALL else
                   350 if uiscale is babase.UIScale.MEDIUM else 400)
        width = (500 if uiscale is babase.UIScale.SMALL else
                   600 if uiscale is babase.UIScale.MEDIUM else 650)
        scroll_h = (200 if uiscale is babase.UIScale.SMALL else
                   250 if uiscale is babase.UIScale.MEDIUM else 270)
        scroll_w = (450 if uiscale is babase.UIScale.SMALL else
                   550 if uiscale is babase.UIScale.MEDIUM else 600)
        self._transition_out: Optional[str]
        scale_origin: Optional[Tuple[float, float]]
        self._transition_out = 'out_scale'
        scale_origin = 10
        transition = 'in_scale'
        scale_origin = None
        cancel_is_selected = False
        cfg = babase.app.config
        bg_color = cfg.get('PartyWindow Main Color', (0.5,0.5,0.5))

        self.root_widget = bui.containerwidget(
            size=(width, height),
            color = bg_color,
            transition=transition,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=scale_origin)
        
        bui.textwidget(
            parent=self.root_widget,
            position=(width * 0.5, height - 45),
            size=(20, 20),
            h_align='center',
            v_align='center',
            text="Custom Settings",
            scale=0.9,
            color=(5,5,5)
        )
        
        cbtn = btn = bui.buttonwidget(
            parent=self.root_widget,
            autoselect=True,
            position=(30, height - 60),
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._cancel
        )

        scroll_position = (30 if uiscale is babase.UIScale.SMALL else
                           40 if uiscale is babase.UIScale.MEDIUM else 50)
        self._scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            position=(30, scroll_position),
            simple_culling_v=20.0,
            highlight=False,
            size=(scroll_w, scroll_h),
            selection_loops_to_parent=True
        )

        bui.widget(edit=self._scrollwidget, right_widget=self._scrollwidget)
        self._subcontainer = bui.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)
        ip_button = bui.checkboxwidget(
            parent=self._subcontainer,
            size=(300, 30),
            maxwidth=300,
            textcolor = ((0,1,0) if cfg['IP button'] else (0.95,0.65,0)),
            scale=1,
            value=cfg['IP button'],
            autoselect=True,
            #text="IP Button",
            text="Botón de IP",
            on_value_change_call=self.ip_button
        )

        ping_button = bui.checkboxwidget(
            parent=self._subcontainer,
            size=(300, 30),
            maxwidth=300,
            textcolor = ((0,1,0) if cfg['ping button'] else (0.95,0.65,0)),
            scale=1,
            value=cfg['ping button'],
            autoselect=True,
            #text="Ping Button",
            text="Botón de Ping",
            on_value_change_call=self.ping_button
        )

        copy_button = bui.checkboxwidget(
            parent=self._subcontainer,
            size=(300, 30),
            maxwidth=300,
            textcolor = ((0,1,0) if cfg['copy button'] else (0.95,0.65,0)),
            scale=1,
            value=cfg['copy button'],
            autoselect=True,
            text="Botón de Copiar texto",
            on_value_change_call=self.copy_button
        )

        direct_send = bui.checkboxwidget(
            parent=self._subcontainer,
            size=(300, 30),
            maxwidth=300,
            textcolor = ((0,1,0) if cfg['Direct Send'] else (0.95,0.65,0)),
            scale=1,
            value=cfg['Direct Send'],
            autoselect=True,
            #text="Directly Send Custom Commands",
            text="Enviar comandos personalizados directamente",
            on_value_change_call=self.direct_send
        )

        colorfulchat = bui.checkboxwidget(
            parent=self._subcontainer,
            size=(300, 30),
            maxwidth=300,
            textcolor = ((0,1,0) if cfg['Colorful Chat'] else (0.95,0.65,0)),
            scale=1,
            value=cfg['Colorful Chat'],
            autoselect=True,
            text="Chat colorido",
            on_value_change_call=self.colorful_chat
        )

        msg_notification_text = bui.textwidget(
            parent=self._subcontainer,
            scale=0.8,
            color=(1, 1, 1),
            text='Notificación de mensaje:',
            size=(100, 30),
            h_align='left',
            v_align='center'
        )

        msg_notification_widget = PopupMenu(
            parent=self._subcontainer,
            position=(100, height - 1200),
            width=200,
            scale=(2.8 if uiscale is babase.UIScale.SMALL else
                  1.8 if uiscale is babase.UIScale.MEDIUM else 1.2),
            choices=['top', 'bottom'],
            current_choice=babase.app.config['Message Notification'],
            button_size=(80,25),
            on_value_change_call=self._change_notification
        )

        self_status_text = bui.textwidget(
            parent=self._subcontainer,
            scale=0.8,
            color=(1, 1, 1),
            text='Self Status:',
            size=(100, 30),
            h_align='left',
            v_align='center'
        )

        self_status_widget = PopupMenu(
            parent=self._subcontainer,
            position=(50, height - 1000),
            width=200,
            scale=(2.8 if uiscale is babase.UIScale.SMALL else
                  1.8 if uiscale is babase.UIScale.MEDIUM else 1.2),
            choices=['online', 'offline'],
            current_choice=babase.app.config['Self Status'],
            button_size=(80,25),
            on_value_change_call=self._change_status
        )
        
        bui.containerwidget(edit=self.root_widget, cancel_button=btn)
        bui.containerwidget(
            edit=self.root_widget,
            selected_child=(
                cbtn if cbtn is not None and cancel_is_selected else None),
                start_button=None
        )

    def ip_button(self, value: bool):
        cfg = babase.app.config
        cfg['IP button'] = value
        cfg.apply_and_commit()
        if cfg['IP button']:
            bui.screenmessage("IP Button is now enabled", color = (0,1,0))
        else:
            bui.screenmessage("IP Button is now disabled", color = (1,0.7,0))

    def ping_button(self, value: bool):
        cfg = babase.app.config
        cfg['ping button'] = value
        cfg.apply_and_commit()
        if cfg['ping button']:
            bui.screenmessage("Ping Button is now enabled", color = (0,1,0))
        else:
            bui.screenmessage("Ping Button is now disabled", color = (1,0.7,0)) 

    def copy_button(self, value: bool):
        cfg = babase.app.config
        cfg['copy button'] = value
        cfg.apply_and_commit()
        if cfg['copy button']:
            bui.screenmessage("Copy Text Button is now enabled", color = (0,1,0))
        else:
            bui.screenmessage("Copy Text Button is now disabled", color = (1,0.7,0))

    def direct_send(self, value: bool):
        cfg = babase.app.config
        cfg['Direct Send'] = value
        cfg.apply_and_commit()

    def colorful_chat(self, value: bool):
        cfg = babase.app.config
        cfg['Colorful Chat'] = value
        cfg.apply_and_commit()

    def _change_notification(self, choice):
        cfg = babase.app.config
        cfg['Message Notification'] = choice
        cfg.apply_and_commit()

    def _change_status(self, choice):
        cfg = babase. app.config
        cfg['Self Status'] = choice
        cfg.apply_and_commit()

    def _cancel(self) -> None:
        bui.containerwidget(
            edit=self.root_widget,
            transition=('out_right' if self._transition_out is None else
                        self._transition_out))


class PartyWindow(bui.Window):
    """Party list/chat window."""

    def __del__(self) -> None:
        bui.set_party_window_open(False)

    def __init__(self, origin: Sequence[float] = (0, 0)):

        self._private_chat = False
        self._firstcall = True
        self.ping_server()
        bui.set_party_window_open(True)
        self._r = 'partyWindow'
        self._popup_type: Optional[str] = None
        self._popup_party_member_client_id: Optional[int] = None
        self._popup_party_member_is_host: Optional[bool] = None
        self._width = 500
        
        uiscale = bui.app.ui_v1.uiscale
        self._height = (365 if uiscale is babase.UIScale.SMALL else
                        480 if uiscale is babase.UIScale.MEDIUM else 600)
        self.bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))

        self._last_msg_clicked: str = None
        self._last_time_pressed_msg: float = 0.0
        self._last_time_pressed_translate: float = 0.0
        self._double_press_interval: float = 0.3
        #self.ping_timer = bs.Timer(5, bs.WeakCall(self.ping_server), repeat=True)

        bui.Window.__init__(self, root_widget=bui.containerwidget(
            size=(self._width, self._height),
            transition='in_scale',
            color=self.bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self.close_with_sound,
            scale_origin_stack_offset=origin,
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.35 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -10) if uiscale is babase.UIScale.SMALL else (
                240, 0) if uiscale is babase.UIScale.MEDIUM else (330, 20)))

        self._cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(30, self._height - 47),
            size=(50, 50),
            label='',
            on_activate_call=self.close,
            autoselect=True,
            color=self.bg_color,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        bui.containerwidget(
            edit=self._root_widget,
            cancel_button=self._cancel_button
        )

        self._menu_button = bui.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(self._width - 80, self._height - 47),
            size=(50, 50),
            label='...',
            autoselect=True,
            button_type='square',
            on_activate_call=bs.WeakCall(self._on_menu_button_press),
            color=self.bg_color,
            iconscale=1.2)

        info = bs.get_connection_to_host_info()
        #print("[PartyWindow]: Abriste el chat")

        blacklist_manager = BlacklistManager(blacklist_file, bui)
        if info.get('name', '') != '':
            blacklist_manager.search_blacklist_users()
        #else:
        #    print("No party")

        if info.get('name', '') != '':
            self.title = babase.Lstr(value=info['name'])
        else:
            self.title = babase.Lstr(resource=self._r + '.titleText')

        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.9,
            color=(0.5, 0.7, 0.5),
            text=self.title,
            size=(0, 0),
            position=(self._width * 0.47, self._height - 29),
            maxwidth=self._width * 0.6,
            h_align='center',
            v_align='center'
        )

        self._empty_str = bui.textwidget(
            parent=self._root_widget,
            scale=0.75,
            size=(0, 0),
            position=(self._width * 0.5, self._height - 65),
            maxwidth=self._width * 0.85,
            h_align='center',
            v_align='center'
        )

        self._scroll_width = self._width - 50
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._height - 200),
            position=(30, 80),
            color=self.bg_color
        )
        
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0
        )

        bui.widget(edit=self._menu_button, down_widget=self._columnwidget)

        self._muted_text = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=babase.Lstr(resource='chatMutedText'))

        self._text_field = txt = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(530-140, 40),
            position=(44+100, 39),
            text='',
            maxwidth=494,
            shadow=0.3,
            flatness=1.0,
            description=babase.Lstr(resource=self._r + '.chatMessageText'),
            autoselect=True,
            v_align='center',
            corner_scale=0.7)

        bui.widget(
            edit=self._scrollwidget,
            autoselect=True,
            left_widget=self._cancel_button,
            up_widget=self._cancel_button,
            down_widget=self._text_field
        )

        bui.widget(
            edit=self._columnwidget,
            autoselect=True,
            up_widget=self._cancel_button,
            down_widget=self._text_field
        )
        
        bui.containerwidget(edit=self._root_widget, selected_child=txt)
        self._send_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 35),
            label=babase.Lstr(resource=self._r + '.sendText'),
            button_type='square',
            autoselect=True,
            color=self.bg_color,
            position=(self._width - 70, 35),
            on_activate_call=self._send_chat_message
        )

        def _times_button_on_click():
            Quickreply = self._get_quick_responds()
            if len(Quickreply) > 0:
                PopupMenuWindow(
                    position=self._times_button.get_screen_space_center(),
                    scale=self._get_popup_window_scale(),
                    color=self.bg_color,
                    choices=Quickreply,
                    choices_display=_creat_Lstr_list(Quickreply),
                    current_choice=Quickreply[0],
                    delegate=self
                )
                self._popup_type = "QuickMessageSelect"
                
        bui.textwidget(edit=txt, on_return_press_call=btn.activate)
        self._previous_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            button_type='square',
            autoselect=True,
            position=(38, 57),
            color=self.bg_color,
            scale=0.75,
            on_activate_call=self._previous_message
        )
        
        self._next_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            button_type='square',
            autoselect=True,
            color=self.bg_color,
            scale=0.75,
            position=(38, 28),
            on_activate_call=self._next_message
        )
        
        self._times_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 35),
            label="Mensaje \n Rápido",
            color=self.bg_color,
            button_type='square',
            autoselect=True,
            position=(70, 35),
            on_activate_call=_times_button_on_click
        )
        
        if babase.app.config['copy button']:
            self._copy_button = bui.buttonwidget(
                parent=self._root_widget,
                size=(15, 15),
                label='©',
                button_type='backSmall',
                autoselect=True,
                color=self.bg_color,
                position=(self._width - 40, 80),
                on_activate_call=self._copy_to_clipboard
            )

        self._ping_button = None
        if info.get('name', '') != '':
            if babase.app.config['ping button']:
                self._ping_button = bui.buttonwidget(
                    parent=self._root_widget,
                    scale=0.7,
                    position=(self._width - 542, self._height - 57),
                    size=(75, 75),
                    autoselect=True,
                    button_type='square',
                    label=f'{_ping}', 
                    on_activate_call=self._send_ping,
                    color=self.bg_color,
                    text_scale=2.3,
                    iconscale=1.2
                )

            if babase.app.config['IP button']:
                self._ip_port_button = bui.buttonwidget(
                    parent=self._root_widget,
                    size=(70, 40),
                    label='Mostrar\nIP',
                    button_type='square',
                    autoselect=True,
                    color=self.bg_color,
                    position=(self._width - 550, self._height - 105),
                    on_activate_call=self._ip_port_msg
                )

        self._settings_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 50),
            scale=0.5,
            button_type='square',
            autoselect=True,
            color=self.bg_color,
            position=(self._width - 40, self._height - 47),
            on_activate_call =self._on_setting_button_press,
            icon=bui.gettexture('settingsIcon'),
            iconscale=1.2
        )
        
        self._privatechat_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 50),
            scale=0.5,
            button_type='square',
            autoselect=True,
            color=self.bg_color,
            position=(self._width - 40, self._height - 80),
            on_activate_call =self._on_privatechat_button_press,
            icon=bui.gettexture('ouyaOButton'),
            iconscale=1.2
        )
        
        self._name_widgets: List[bui.Widget] = []
        self._roster: Optional[List[Dict[str, Any]]] = None
        #self._update_timer = bs.Timer(1.0,
        #                              bs.WeakCall(self._update),
        #                              repeat=True)
        self._update()
        #self._show_love_window()

    def on_chat_message(self, msg: str, sent=None) -> None:
        """Called when a new chat message comes through."""
        if babase.app.config['Party Chat Muted'] and not bui.app.ui_v1.party_window()._private_chat:
            return
        if sent:
            self._add_msg(msg, sent)
        else:
            self._add_msg(msg)

    def _copy_msg(self, msg: str) -> None:
        """Copiar texto al portapapeles y mostrar un mensaje visual."""
        bui.clipboard_set_text(msg)
        bui.screenmessage("Mensaje copiado", color=(0, 1, 0))

    def _on_message_click(self, msg: str) -> None:
        now = babase.apptime()
        #print(f"[CLICK] Mensaje: '{msg}' | Tiempo actual: {now:.3f}")
        #print(f"[CLICK] Último mensaje clickeado: '{self._last_msg_clicked}'")
        #print(f"[CLICK] Tiempo desde el último clic: {(now - self._last_time_pressed_msg):.3f}")

        if (now - self._last_time_pressed_msg < self._double_press_interval) and (self._last_msg_clicked == msg):
            #print("[DOUBLE CLICK DETECTADO] Copiando mensaje al portapapeles...")
            self._copy_msg(msg)
            self._last_time_pressed_msg = 0.0
            self._last_msg_clicked = None
        else:
            #print("[CLICK SIMPLE] Guardando este clic como referencia.")
            self._last_msg_clicked = msg
            self._last_time_pressed_msg = now

    def _add_msg(self, msg: str, sent=None) -> None:
        if babase.app.config['Colorful Chat']:
            sender = msg.split(': ')[0]
            color = color_tracker._get_sender_color(sender) if sender else (1, 1, 1)
        else:
            color = (1, 1, 1)
        maxwidth = self._scroll_width * 0.94
        
        txt = bui.textwidget(
            parent=self._columnwidget,
            text=msg,
            h_align='left',
            v_align='center',
            size=(40, 13),         
            scale=0.55,
            color=color,
            maxwidth=maxwidth,        
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            selectable=True,
            click_activate=True,
            on_activate_call=bui.Call(self._on_message_click, msg)
        )

        bui.textwidget(
            edit=txt,
            selectable=True,
            click_activate=True,
            on_activate_call=babase.Call(self._on_message_click, msg)
        )

        self._chat_texts.append(txt)
        if len(self._chat_texts) > 40:
            first = self._chat_texts.pop(0)
            first.delete()
        bui.containerwidget(edit=self._columnwidget, visible_child=txt)

    def _display_love_message(self, probability: int, duration: float):
        if random.randint(1, probability) == 1:
            print(f"Executed with time {duration}")

            origin_widget = self.get_root_widget()  # capturado ahora

            def delayed_message():
                try:
                    bui.containerwidget(edit=origin_widget)  # testea si sigue vivo
                    LoveWindow(origin_widget=origin_widget)
                    print("Executed again as the last time.")
                except Exception as e:
                    print(f"Widget destroyed before reuse: {e}")

            babase.apptimer(duration, delayed_message)
        else:
            print("Not executed")


    def _show_love_window(self) -> None:
        if not os.path.exists(love_file) or os.path.getsize(love_file) == 0:
            with open(love_file, 'w') as f:
                f.write('show_love_message: True')
        # Read the contents of the file
        with open(love_file, 'r') as f:
            content = f.read().strip()
        # Check and act on the status
        if content == 'show_love_message: True':
            try:
                # Open the server information window
                self._display_love_message(15, 5) # 25 Seconds
                #LoveWindow(origin_widget=self.get_root_widget())
            except Exception as e:
                logging.exception("Error displaying information:")
                bs.broadcastmessage(f"Error: {str(e)}", color=(1, 0, 0))
                bui.getsound('error').play()
        else:
            print("Esta ventana ya se abrió.")

    def _show_rcp_activity(self) -> None:
        try:
            # Open the server information window
            ServerInfoWindow(origin_widget=self.get_root_widget())
        except Exception as e:
            logging.exception("Error displaying information:")
            bs.broadcastmessage(f"Error: {str(e)}", color=(1, 0, 0))
            bui.getsound('error').play()
        
    

    def _show_love_message(self) -> None:
        try:
            # Open the server information window
            LoveWindow(origin_widget=self.get_root_widget())
            bui.getsound('aww').play()

        except Exception as e:
            logging.exception("Error displaying window:")
            bs.broadcastmessage(f"Error: {str(e)}", color=(1, 0, 0))
            bui.getsound('error').play()

    def _on_menu_button_press(self) -> None:
        is_muted = babase.app.config['Party Chat Muted']
        uiscale = bui.app.ui_v1.uiscale
        
        choices = [
            'muteOption',
            'modifyColor',
            'addQuickReply',
            'removeQuickReply',
            #'credits'
            'removeBlackListUser',
            #'discordrpc'
        ]

        #choices_display = ['Mute Option', 'Modify Main Color', 'Add as Quick Reply', 'Remove a Quick Reply', 'Credits']
        
        choices_display = [
            'Opción de Silencio',
            'Modificar Color Principal',
            'Agregar como Respuesta Rápida',
            'Eliminar una Respuesta Rápida',
            'Eliminar un usuario de la BlackList',
            #'Discord RPC'
            #'Créditos'
        ]

        if hasattr(bs.get_foreground_host_activity(), '_map'):
            choices.append('manualCamera')
            choices_display.append('Manual Camera')
            
        PopupMenuWindow(
            position=self._menu_button.get_screen_space_center(),
            color=self.bg_color,
            scale=(2.3 if uiscale is babase.UIScale.SMALL else
                   1.65 if uiscale is babase.UIScale.MEDIUM else 1.23),
            choices=choices,
            choices_display= self._create_baLstr_list(choices_display),
            current_choice='muteOption',
            delegate=self)
        self._popup_type = 'menu'

    def _update(self) -> None:
      if not self._private_chat:
        bui.set_party_window_open(True)
        bui.textwidget(edit=self._title_text, text=self.title)
        if self._firstcall:
            if hasattr(self, '_status_text'):
                self._status_text.delete()
            self._roster = []
            self._firstcall = False
            self._chat_texts: List[bui.Widget] = []
            if not babase.app.config['Party Chat Muted']:
                msgs = bs.get_chat_messages()
                for msg in msgs:
                    self._add_msg(msg)
        # update muted state
        if babase.app.config['Party Chat Muted']:
            bui.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.3))
            # clear any chat texts we're showing
            if self._chat_texts:
                while self._chat_texts:
                    first = self._chat_texts.pop()
                    first.delete()
        else:
            bui.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.0))
        if self._ping_button:
            bui.buttonwidget(edit=self._ping_button,
                              label=f'{_ping}',
                              textcolor=self._get_ping_color())

        # update roster section
        roster = bs.get_game_roster()
        if roster != self._roster or self._firstcall:

            self._roster = roster

            # clear out old
            for widget in self._name_widgets:
                widget.delete()
            self._name_widgets = []
            if not self._roster:
                top_section_height = 60
                bui.textwidget(edit=self._empty_str,
                              text=babase.Lstr(resource=self._r + '.emptyText'))
                bui.scrollwidget(edit=self._scrollwidget,
                                size=(self._width - 50,
                                      self._height - top_section_height - 110),
                                position=(30, 80))
            else:
                columns = 1 if len(
                    self._roster) == 1 else 2 if len(self._roster) == 2 else 3
                rows = int(math.ceil(float(len(self._roster)) / columns))
                c_width = (self._width * 0.9) / max(3, columns)
                c_width_total = c_width * columns
                c_height = 24
                c_height_total = c_height * rows
                for y in range(rows):
                    for x in range(columns):
                        index = y * columns + x
                        if index < len(self._roster):
                            t_scale = 0.65
                            pos = (self._width * 0.53 - c_width_total * 0.5 +
                                   c_width * x - 23,
                                   self._height - 65 - c_height * y - 15)

                            # if there are players present for this client, use
                            # their names as a display string instead of the
                            # client spec-string
                            try:
                                if self._roster[index]['players']:
                                    # if there's just one, use the full name;
                                    # otherwise combine short names
                                    if len(self._roster[index]
                                           ['players']) == 1:
                                        p_str = self._roster[index]['players'][
                                            0]['name_full']
                                    else:
                                        p_str = ('/'.join([
                                            entry['name'] for entry in
                                            self._roster[index]['players']
                                        ]))
                                        if len(p_str) > 25:
                                            p_str = p_str[:25] + '...'
                                else:
                                    p_str = self._roster[index][
                                        'display_string']
                            except Exception:
                                logging.exception(
                                    'Error calcing client name str.')
                                p_str = '???'
                            widget = bui.textwidget(
                                parent=self._root_widget,
                                position=(pos[0], pos[1]),
                                scale=t_scale,
                                size=(c_width * 0.85, 30),
                                maxwidth=c_width * 0.85,
                                color=(1, 1, 1) if index == 0 else (1, 1, 1),
                                selectable=True,
                                autoselect=True,
                                click_activate=True,
                                text=babase.Lstr(value=p_str),
                                h_align='left',
                                v_align='center'
                            )
                            
                            self._name_widgets.append(widget)

                            # in newer versions client_id will be present and
                            # we can use that to determine who the host is.
                            # in older versions we assume the first client is
                            # host
                            if self._roster[index]['client_id'] is not None:
                                is_host = self._roster[index][
                                    'client_id'] == -1
                            else:
                                is_host = (index == 0)

                            # FIXME: Should pass client_id to these sort of
                            #  calls; not spec-string (perhaps should wait till
                            #  client_id is more readily available though).
                            bui.textwidget(
                                edit=widget,
                                on_activate_call=babase.Call(
                                self._on_party_member_press,
                                self._roster[index]['client_id'],
                                is_host, widget)
                            )
                            
                            pos = (self._width * 0.53 - c_width_total * 0.5 +
                                   c_width * x,
                                   self._height - 65 - c_height * y)

                            # Make the assumption that the first roster
                            # entry is the server.
                            # FIXME: Shouldn't do this.
                            if is_host:
                                twd = min(
                                    c_width * 0.85,
                                    _babase.get_string_width(
                                        p_str, suppress_warning=True) *
                                    t_scale)
                                self._name_widgets.append(
                                    bui.textwidget(
                                        parent=self._root_widget,
                                        position=(pos[0] + twd + 1,
                                                  pos[1] - 0.5),
                                        size=(0, 0),
                                        h_align='left',
                                        v_align='center',
                                        maxwidth=c_width * 0.96 - twd,
                                        color=(0.1, 1, 0.1, 0.5),
                                        text=babase.Lstr(resource=self._r +
                                                     '.hostText'),
                                        scale=0.4,
                                        shadow=0.1,
                                        flatness=1.0))
                bui.textwidget(edit=self._empty_str, text='')
                bui.scrollwidget(
                    edit=self._scrollwidget,
                    size=(self._width - 50, max(100, self._height - 139 - c_height_total)),
                    position=(30, 80)
                )
      else:
        bui.set_party_window_open(False)
        for widget in self._name_widgets:
            widget.delete()
        self._name_widgets = []
        bui.textwidget(edit=self._title_text, text='Private Chat')
        bui.textwidget(edit=self._empty_str, text='')
        if self._firstcall:
            self._firstcall = False
            if hasattr(self, '_status_text'):
                self._status_text.delete()
            try:
                msgs = messenger.pvt_msgs[messenger.filter]
            except:
                msgs = []
            if self._chat_texts:
                while self._chat_texts:
                    first = self._chat_texts.pop()
                    first.delete()
            uiscale = bui.app.ui_v1.uiscale
            scroll_height = (165 if uiscale is babase.UIScale.SMALL else
                            280 if uiscale is babase.UIScale.MEDIUM else 400)
            bui.scrollwidget(edit=self._scrollwidget,
                            size=(self._width - 50, scroll_height))
            for msg in msgs:
                message = messenger._format_message(msg)
                self._add_msg(message, msg['sent'])

            self._filter_text = bui.textwidget(
                parent=self._root_widget,
                scale=0.6,
                color=(0.9, 1.0, 0.9),
                text='Filter: ',
                size=(0, 0),
                position=(self._width * 0.3, self._height - 70),
                h_align='center',
                v_align='center'
            )

            choices = [i for i in messenger.saved_ids]
            choices_display = [babase.Lstr(value=messenger.saved_ids[i]) for i in messenger.saved_ids]
            choices.append('add')
            choices_display.append(babase.Lstr(value='***Add New***'))
            
            filter_widget = PopupMenu(
                parent=self._root_widget,
                position=(self._width * 0.4, self._height - 80),
                width=200,
                scale=(2.8 if uiscale is babase.UIScale.SMALL else
                        1.8 if uiscale is babase.UIScale.MEDIUM else 1.2),
                choices=choices,
                choices_display=choices_display,
                current_choice=messenger.filter,
                button_size=(120,30),
                on_value_change_call=self._change_filter
            )
            
            self._popup_button = filter_widget.get_button()
            
            if messenger.filter != 'all':
                user_status = messenger._get_status(messenger.filter)
                if user_status == 'Offline':
                    color = (1,0,0)
                elif user_status.startswith(('Playing in', 'in Lobby')):
                    color = (0,1,0)
                else:
                    color = (0.9, 1.0, 0.9)
                self._status_text = bui.textwidget(
                    parent=self._root_widget,
                    scale=0.5,
                    color=color,
                    text=f'Status:\t{user_status}',
                    size=(200, 30),
                    position=(self._width * 0.3, self._height - 110),
                    h_align='center',
                    v_align='center',
                    autoselect=True,
                    selectable=True,
                    click_activate=True
                )
                
                bui.textwidget(edit=self._status_text, on_activate_call=babase.Call(messenger._get_status, messenger.filter, 'last_seen'))

    def _change_filter(self, choice):
        if choice == 'add':
            self.close()
            AddNewIdWindow()
        else:
            messenger.filter = choice
            self._firstcall = True
            self._filter_text.delete()
            self._popup_button.delete()
            if self._chat_texts:
                while self._chat_texts:
                    first = self._chat_texts.pop()
                    first.delete()
            self._update()

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        """Called when a choice is selected in the popup."""
        if self._popup_type == 'partyMemberPress':
            playerinfo = self._get_player_info(self._popup_party_member_client_id)
            
            if choice == 'kick':
                name = playerinfo['ds']
                ConfirmWindow(
                    text=f'Estas seguro de iniciar una votación \n para expulsar a {name}?',
                    action = self._vote_kick_player,
                    cancel_button=True,
                    cancel_is_selected=True,
                    color=self.bg_color,
                    text_scale=1.0,
                    origin_widget=self.get_root_widget()
                )

            elif choice == 'mention':
                players = playerinfo['players']
                choices = []
                namelist = [playerinfo['ds']]
                for player in players:
                    name = player['name_full']
                    if name not in namelist:
                        namelist.append(name)
                choices_display = self._create_baLstr_list(namelist)
                for i in namelist:
                    i = i.replace('"', '\"')
                    i = i.replace("'", "\'")
                    choices.append(f'self._edit_text_msg_box("{i}")')
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color,
                    scale=self._get_popup_window_scale(),
                    choices=choices,
                    choices_display=choices_display,
                    current_choice=choices[0],
                    delegate=self
                )
                
                self._popup_type = "executeChoice"
            
            elif choice == 'adminkick':
                name = playerinfo['ds']
                ConfirmWindow(
                    text=f'Estás seguro de usar el comando admin\n para expulsar a {name}',
                    action=self._send_admin_kick_command,
                    cancel_button=True,
                    cancel_is_selected=True,
                    color=self.bg_color,
                    text_scale=1.0,
                    origin_widget=self.get_root_widget()
                )

            elif choice == 'customCommands':
                choices = []
                choices_display = []
                playerinfo = self._get_player_info(self._popup_party_member_client_id)
                account = playerinfo['ds']
                try:
                    name = playerinfo['players'][0]['name_full']
                except:
                    name = account
                for i in babase.app.config.get('Custom Commands'):
                    i = i.replace('$c', str(self._popup_party_member_client_id))
                    i = i.replace('$a', str(account))
                    i = i.replace('$n', str(name))
                    if babase.app.config['Direct Send']:
                        choices.append(f'bs.chatmessage("{i}")')
                    else:
                        choices.append(f'self._edit_text_msg_box("{i}")')
                    choices_display.append(babase.Lstr(value=i))
                
                choices.append('AddNewChoiceWindow()')
                choices_display.append(babase.Lstr(value='***Add New***'))
                
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color,
                    scale=self._get_popup_window_scale(),
                    choices=choices,
                    choices_display=choices_display,
                    current_choice=choices[0],
                    delegate=self
                )

                self._popup_type = 'executeChoice'

            elif choice == 'blockplayer':
                name = playerinfo['ds']
                ConfirmWindow(
                    text=f'Estás seguro de bloquear a este jugador, \n al hacer esto te sacará de la partida \n cuando esta persona entre {name}',
                    action=self._send_user_to_black_list,
                    cancel_button=True,
                    cancel_is_selected=True,
                    color=self.bg_color,
                    text_scale=1.0,
                    origin_widget=self.get_root_widget()
                )

            elif choice == 'addNew':
                AddNewChoiceWindow()

        elif self._popup_type == 'menu':
            if choice == 'muteOption':
                current_choice = self._get_current_mute_type()
                PopupMenuWindow(
                    position = (self._width - 60, self._height - 47),
                    color=self.bg_color,
                    scale=self._get_popup_window_scale(),
                    
                    choices=[
                        'muteInGameOnly',
                        'mutePartyWindowOnly',
                        'muteAll',
                        'unmuteAll'
                    ],
                    
                    choices_display=self._create_baLstr_list(
                         [
                            'Silenciar solo mensajes del juego',
                            'Silenciar solo mensajes de la sala',
                            'Silenciar todo',
                            'Activar todos los sonidos'
                        ]
                    ),
                    current_choice=current_choice,
                    delegate=self
                )
                
                self._popup_type = 'muteType'
            
            elif choice == 'modifyColor':
                ColorPickerExact(
                    parent=self.get_root_widget(),
                    position=self.get_root_widget().get_screen_space_center(),
                    initial_color=self.bg_color,
                    delegate=self, tag=''
                )

            elif choice == 'addQuickReply':
                try:
                    newReply = bui.textwidget(query=self._text_field)
                    oldReplies = self._get_quick_responds()
                    oldReplies.append(newReply)
                    self._write_quick_responds(oldReplies)
                    bui.screenmessage(f'"{newReply}" is added.', (0,1,0))
                    bui.getsound('dingSmallHigh').play()
                except:
                    logging.exception()
            
            elif choice == 'removeQuickReply':
                quick_reply = self._get_quick_responds()
                
                PopupMenuWindow(
                    position=self._send_button.get_screen_space_center(),
                    color=(self.bg_color),
                    scale=self._get_popup_window_scale(),
                    choices=quick_reply,
                    choices_display=self._create_baLstr_list(quick_reply),
                    current_choice=quick_reply[0],
                    delegate=self
                )
                self._popup_type = 'removeQuickReplySelect'
            
            elif choice == 'credits':
                ConfirmWindow(
                    text=u'\ue043Ultra Pro Maxx ++ Party Window\ue043\nBy Droopy\n\nThanks To Karishma Who Helped Me In Coding This \nWonderfull Party Window With Manual Camera\nFor Now Manual Camera Will Work Only With Offline Mode\n\nDiscord - Droopy#1111',
                    action = self.join_discord,
                    width=420,
                    height=230,
                    color=self.bg_color,
                    text_scale=1.0,
                    ok_text="Join Discord",
                    origin_widget=self.get_root_widget()
                )

            elif choice == 'discordrpc':
                try:
                    ConfirmWindow(text=
                        u'Mostrar Actividad de juego en Discord\n\n'
                        'Al confirmar, está dando acceso para que en su Discord aparezca\n'
                        'como actividad datos de el servidor:\n\n'
                        f'{bs.get_connection_to_host_info()["name"]}\n',
                        action = self._show_rcp_activity,
                        #action = self._show_love_message,
                        width=420,
                        height=230,
                        color=(255, 255, 255),
                        text_scale=1.5,
                        origin_widget=self.get_root_widget()
                    )  
                except:
                    bui.screenmessage('¡Parece que no estás en ninguna partida!', (1,0,0))
                    bui.getsound('error').play()

            elif choice == 'removeBlackListUser':
                try:
                    quick_reply = self._get_blacklist_users()
                    
                    PopupMenuWindow(
                        position=self._send_button.get_screen_space_center(),
                        color=(self.bg_color),
                        scale=self._get_popup_window_scale(),
                        choices=quick_reply,
                        choices_display=self._create_baLstr_list(quick_reply),
                        current_choice=quick_reply[0],
                        delegate=self
                    )
                    self._popup_type = 'removeBlackListUserSelect'
                except:
                    bui.screenmessage('¡Parece que no estás en ninguna partida!', (1,0,0))
                    bui.getsound('error').play()
                
            elif choice == 'manualCamera':
                bui.containerwidget(edit=self._root_widget, transition='out_scale')
                Manual_camera_window()

        elif self._popup_type == 'muteType':
            self._change_mute_type(choice)

        elif self._popup_type == 'executeChoice':
            exec(choice)

        elif self._popup_type == 'quickMessage':
            if choice == '*** EDIT ORDER ***':
                SortQuickMessages()
            else:
                self._edit_text_msg_box(choice)

        elif self._popup_type == "QuickMessageSelect":
            # bui.textwidget(edit=self._text_field,text=self._get_quick_responds()[index])
            self._edit_text_msg_box(choice, "add")

        elif self._popup_type == 'removeQuickReplySelect':
            data = self._get_quick_responds()
            data.remove(choice)
            self._write_quick_responds(data)
            bui.screenmessage(f'"{choice}" se eliminó de las respuestas rápidas.', (1,0,0))
            bui.getsound('shieldDown').play()

        elif self._popup_type == 'removeBlackListUserSelect':
            data = self._get_blacklist_users()
            data.remove(choice)
            self._write_blacklist_responds(data)
            bui.screenmessage(f'"{choice}" se eliminó de la blacklist.', (1,0,0))
            bui.getsound('shieldDown').play()

        else:
            print(f'unhandled popup type: {self._popup_type}')
        del popup_window  # unused

    def _vote_kick_player(self):
            if self._popup_party_member_is_host:
                bui.getsound('error').play()
                bui.screenmessage(
                    babase.Lstr(resource='internal.cantKickHostError'),
                    color=(1, 0, 0))
            else:
                assert self._popup_party_member_client_id is not None

                # Ban for 5 minutes.
                result = bs.disconnect_client(
                    self._popup_party_member_client_id, ban_time=5 * 60)
                if not result:
                    bui.getsound('error').play()
                    bui.screenmessage(
                        babase.Lstr(resource='getTicketsWindow.unavailableText'),
                        color=(1, 0, 0))

    def _send_admin_kick_command(self):
        bs.chatmessage('/kick ' + str(self._popup_party_member_client_id))

    def _end_game(self) -> None:
        assert bui.app.classic is not None

        # no-op if our underlying widget is dead or on its way out.
        if not self._root_widget or self._root_widget.transitioning_out:
            return

        bui.containerwidget(edit=self._root_widget, transition='out_left')
        bui.app.classic.return_to_main_menu_session_gracefully(reset_ui=False)

    def _send_user_to_black_list(self):
        # 1. Obtener el namelist usando lógica existente
        playerinfo = self._get_player_info(self._popup_party_member_client_id)
        players = playerinfo['players']
        namelist = [playerinfo['ds']]

        for player in players:
            name = player['name_full']
            if name not in namelist:
                namelist.append(name)

        # 2. Instanciar y usar BlacklistManager
        blacklist_manager = BlacklistManager(blacklist_file, bui)
        blacklist_manager._root_widget = self._root_widget  # necesario para _end_game
        blacklist_manager.send_user_to_black_list(namelist)


    def _copy_to_clipboard(self):
        msg = bui.textwidget(query=self._text_field)
        if msg == '':
            bui.screenmessage('Nothing to copy.', (1,0,0))
            bui.getsound('error').play()
        else:
            babase.clipboard_set_text(msg)
            bui.screenmessage(f'"{msg}" is copied to clipboard.', (0,1,0))
            bui.getsound('dingSmallHigh').play()

    def _get_current_mute_type(self):
        cfg = babase.app.config
        if cfg['Chat Muted'] == True:
            if cfg['Party Chat Muted'] == True:
                return 'muteAll'
            else:
                return 'muteInGameOnly'
        else:
            if cfg['Party Chat Muted'] == True:
                return 'mutePartyWindowOnly'
            else:
                return 'unmuteAll'

    def _change_mute_type(self, choice):
        cfg = babase.app.config
        if choice == 'muteInGameOnly':
            cfg['Chat Muted'] = True
            cfg['Party Chat Muted'] = False
        elif choice == 'mutePartyWindowOnly':
            cfg['Chat Muted'] = False
            cfg['Party Chat Muted'] = True
        elif choice == 'muteAll':
            cfg['Chat Muted'] = True
            cfg['Party Chat Muted'] = True
        else:
            cfg['Chat Muted'] = False
            cfg['Party Chat Muted'] = False
        cfg.apply_and_commit()
        self._update()

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _on_party_member_press(self, client_id: int, is_host: bool,
                               widget: bui.Widget) -> None:
        # if we're the host, pop up 'kick' options for all non-host members
        if bs.get_foreground_host_session() is not None:
            kick_str = babase.Lstr(resource='kickText')
        else:
            # kick-votes appeared in build 14248
            if (bs.get_connection_to_host_info().get('build_number', 0) <
                    14248):
                return
            kick_str = babase.Lstr(resource='kickVoteText')
        uiscale = bui.app.ui_v1.uiscale
        choices = ['kick', 'mention', 'adminkick']
        choices_display = [kick_str] + list(self._create_baLstr_list(['Menciona a este jugador', f'Kick ID: {client_id}']))
        choices.append('customCommands')
        choices_display.append(babase.Lstr(value='Comandos personalizados'))
        choices.append('blockplayer')
        choices_display.append(babase.Lstr(value='Enviar Jugador a Blacklist'))
        PopupMenuWindow(
            position=widget.get_screen_space_center(),
            color=self.bg_color,
            scale=(2.3 if uiscale is babase.UIScale.SMALL else
                   1.65 if uiscale is babase.UIScale.MEDIUM else 1.23),
            choices=choices,
            choices_display=choices_display,
            current_choice='mention',
            delegate=self)
        self._popup_type = 'partyMemberPress'
        self._popup_party_member_client_id = client_id
        self._popup_party_member_is_host = is_host

    def _send_chat_message(self) -> None:
        msg = bui.textwidget(query=self._text_field)
        if '\\' in msg:
            msg = msg.replace('\\d', ('\ue048'))
            msg = msg.replace('\\c', ('\ue043'))
            msg = msg.replace('\\h', ('\ue049'))
            msg = msg.replace('\\s', ('\ue046'))
            msg = msg.replace('\\n', ('\ue04b'))
            msg = msg.replace('\\f', ('\ue04f'))
            msg = msg.replace('\\g', ('\ue027'))
            msg = msg.replace('\\i', ('\ue03a'))
            msg = msg.replace('\\m', ('\ue04d'))
            msg = msg.replace('\\t', ('\ue01f'))
            msg = msg.replace('\\bs', ('\ue01e'))
            msg = msg.replace('\\j', ('\ue010'))
            msg = msg.replace('\\e', ('\ue045'))
            msg = msg.replace('\\l', ('\ue047'))
            msg = msg.replace('\\a', ('\ue020'))
            msg = msg.replace('\\b', ('\ue00c'))
        if not msg:
            choices = self._get_quick_responds()
            choices.append('*** EDIT ORDER ***')

            PopupMenuWindow(
                position=self._send_button.get_screen_space_center(),
                scale=self._get_popup_window_scale(),
                color=self.bg_color,
                choices=choices,
                current_choice=choices[0],
                delegate=self
            )
            self._popup_type = 'quickMessage'
            return
        
        elif msg.startswith('/info '):
            account = msg.replace('/info ', '')
            if account:
                from bauiv1lib.account import viewer
                viewer.AccountViewerWindow(
                        account_id=account)
                bui.textwidget(edit=self._text_field, text='')
                return
        if not self._private_chat:
            if msg == '/id':
                myid = _babase.get_v1_account_misc_read_val_2('resolvedAccountID', '')
                bs.chatmessage(f"My Unique ID : {myid}")
            elif msg == '/save':
              info = bs.get_connection_to_host_info()
              config = babase.app.config
              if info.get('name', '') != '':
                title = info['name']
                if not isinstance(config.get('Saved Servers'), dict):
                    config['Saved Servers'] = {}
                config['Saved Servers'][f'{_ip}@{_port}'] = {
                    'addr': _ip,
                    'port': _port,
                    'name': title
                }
                config.commit()
                bui.screenmessage("Server Added To Manual", color=(0,1,0), transient=True)
                bui.getsound('gunCocking').play()
            
            elif msg != '':
                bs.chatmessage(cast(str, msg))
        else:
            receiver = messenger.filter
            name = _babase.get_v1_account_display_string()
            
            if not receiver:
                display_error('Choose a valid receiver id')
                return
            
            data = {'receiver': receiver, 'message': f'{name}: {msg}'}
            
            if msg.startswith('/rename '):
                if messenger.filter != 'all':
                    nickname = msg.replace('/rename ', '')
                    messenger._save_id(messenger.filter, nickname, verify=False)
                    self._change_filter(messenger.filter)
            elif msg == '/remove':
                if messenger.filter != 'all':
                    messenger._remove_id(messenger.filter)
                    self._change_filter('all')
                else:
                    display_error('Cant delete this')
                bui.textwidget(edit=self._text_field, text='')
                return
            babase.Call(messenger._send_request, url, data)
            babase.Call(check_new_message)
            Thread(target = messenger._send_request, args = (url, data)).start()
            Thread(target = check_new_message).start()
            #messenger._send_request(url=url, data=data)
            #check_new_message()
        bui.textwidget(edit=self._text_field, text='')

    def _write_quick_responds(self, data):
        try:
            with open(quick_msg_file, 'w') as f:
                f.write('\n'.join(data))
        except:
            logging.exception()
            bui.screenmessage('Error!', (1,0,0))
            bui.getsound('error').play()

    def _write_blacklist_responds(self, data):
        try:
            with open(blacklist_file, 'w') as f:
                f.write('\n'.join(data))
        except:
            logging.exception()
            bui.screenmessage('Error!', (1,0,0))
            bui.getsound('error').play()

    def _get_quick_responds(self):
        if os.path.exists(quick_msg_file):
            with open(quick_msg_file, 'r') as f:
                return f.read().split('\n')
        else:
            default_replies = ['What the hell?', 'Dude that\'s amazing!']
            self._write_quick_responds(default_replies)
            return default_replies
        
    def _get_blacklist_users(self):
        if os.path.exists(blacklist_file):
            with open(blacklist_file, 'r') as f:
                return f.read().split('\n')
        else:
            default_replies = ['What the hell?', 'Dude that\'s amazing!']
            self._write_quick_responds(default_replies)
            return default_replies

    def color_picker_selected_color(self, picker, color) -> None:
        bui.containerwidget(edit=self._root_widget, color=color)
        color = tuple(round(i,2) for i in color)
        self.bg_color = color
        babase.app.config['PartyWindow Main Color'] = color

    def color_picker_closing(self, picker) -> None:
        babase.app.config.apply_and_commit()

    def _remove_sender_from_message(self, msg=''):
        msg_start = msg.find(": ") + 2
        return msg[msg_start:]
        
    def _previous_message(self):
        msgs = self._chat_texts
        if not hasattr(self, 'msg_index'):
            self.msg_index = len(msgs) - 1 
        else:
            if self.msg_index > 0:
                self.msg_index -= 1
            else:
                del self.msg_index
        try:
            msg_widget = msgs[self.msg_index]
            msg = bui.textwidget(query=msg_widget)
            msg = self._remove_sender_from_message(msg)
            if msg in ('', '   '):
                self._previous_message()
                return
        except:
            msg = ''
        self._edit_text_msg_box(msg, 'replace')

    def _next_message(self):
        msgs = self._chat_texts
        if not hasattr(self, 'msg_index'):
            self.msg_index = 0
        else:
            if self.msg_index < len(msgs)-1:
                self.msg_index += 1
            else:
                del self.msg_index
        try:
            msg_widget = msgs[self.msg_index]
            msg = bui.textwidget(query=msg_widget)
            msg = self._remove_sender_from_message(msg)
            if msg in ('', '   '):
                self._next_message()
                return
        except:
            msg = ''
        self._edit_text_msg_box(msg, 'replace')
        
    def _ip_port_msg(self):
        try:
            msg = f'IP : {_ip}     PORT : {_port}'
        except:
            msg = ''
        self._edit_text_msg_box(msg, 'replace')

    def ping_server(self):
        info = bs.get_connection_to_host_info()
        if info.get('name', '') != '':
            self.pingThread = PingThread(_ip, _port)
            self.pingThread.start()

    def _get_ping_color(self):
        try:
            if _ping < 100:
                return (0,1,0)
            elif _ping < 500:
                return (1,1,0)
            else:
                return (1,0,0)
        except:
            return (0.1,0.1,0.1)

    def _send_ping(self):
        if isinstance(_ping, int):
            bs.chatmessage(f'My ping = {_ping}ms')

    def close(self) -> None:
        """Close the window."""
        bui.containerwidget(edit=self._root_widget, transition='out_scale')

    def close_with_sound(self) -> None:
        """Close the window and make a lovely sound."""
        bui.getsound('swish').play()
        self.close()

    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return(2.4 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0)

    def _create_baLstr_list(self, list1):
        return (babase.Lstr(value=i) for i in list1)

    def _get_player_info(self, clientID):
        info = {}
        for i in bs.get_game_roster():
            if i['client_id'] == clientID:
                info['ds'] = i['display_string']
                info['players'] = i['players']
                info['aid'] = i['account_id']
                break
        return info

    def _edit_text_msg_box(self, text, action='add'):
        if isinstance(text, str):
            if action == 'add':
                bui.textwidget(edit=self._text_field, text=bui.textwidget(query=self._text_field)+text)
            elif action =='replace':
                bui.textwidget(edit=self._text_field, text=text)

    def _on_setting_button_press(self):
        try:
            SettingsWindow()
        except Exception as e:
            logging.exception()
            pass 

    def _on_privatechat_button_press(self):
        try:
            if messenger.logged_in:
                self._firstcall = True
                if self._chat_texts:
                    while self._chat_texts:
                        first = self._chat_texts.pop()
                        first.delete()
                if not self._private_chat:
                    self._private_chat = True
                else:
                    self._filter_text.delete()
                    self._popup_button.delete()
                    self._private_chat = False
                self._update()
            else:
                if messenger.server_online:
                    if not messenger._cookie_login():
                        if messenger._query():
                            LoginWindow(wtype = 'login')
                        else:
                            LoginWindow(wtype = 'signup')
                else:
                    display_error(messenger.error)
        except Exception as e:
            logging.exception()
            pass 

    def join_discord(self):
        bui.open_url("https://discord.gg/AnqRvKQkmV")

class LovePartyWindow:
    def __init__(self):
        self._initialize()
        
    def _initialize(self):
        """Inicializa el sistema de LoveWindow"""
        #print("Initializing LovePartyWindow system...")
        
        # Create file if it doesn't exist
        if not os.path.exists(love_file):
            with open(love_file, 'w') as f:
                f.write('show_love_message: True')
            #print("Created love_file with default settings")
        
        # Check if the message has already been displayed
        with open(love_file, 'r') as f:
            content = f.read().strip()
            
        self._should_show = (content == 'show_love_message: True')
        #print(f"LoveWindow should show: {self._should_show}")
        
    def show_love_window(self, origin_widget=None):
        """Muestra la ventana de amor si está habilitada"""
        try:
            if not self._should_show:
                #print("LoveWindow already shown previously")
                return
                
            #print("Attempting to show LoveWindow...")
            
            self._display_love_message(15, 5, origin_widget)
            
        except Exception as e:
            logging.exception("Error showing LoveWindow:")
            bui.screenmessage("Error showing love message", color=(1, 0, 0))
            bui.getsound('error').play()

    def _display_love_message(self, probability: int, delay: float, origin_widget=None):
        if random.randint(1, probability) == 1:
            #print(f"Scheduling LoveWindow to show in {delay} seconds")
            
            def delayed_message():
                try:
                    if origin_widget and not origin_widget():
                        #logging.warning("Origin widget no longer exists, aborting LoveWindow")
                        return
                        
                    #print("Now showing LoveWindow")
                    LoveWindow(origin_widget=origin_widget)
                    bui.getsound('aww').play()
                    
                    # Mark as shown
                    #with open(love_file, 'w') as f:
                    #    f.write('show_love_message: False')
                    self._should_show = False
                    #print("LoveWindow shown and status saved")
                    
                except Exception as e:
                    #logging.exception("Error in delayed LoveWindow display:")
                    bui.screenmessage("Error showing love", color=(1, 0, 0))

            babase.apptimer(delay, delayed_message)


class LoginWindow:
    def __init__(self, wtype):
        self.wtype = wtype
        if self.wtype == 'signup':
            title = 'Sign Up Window'
            label = 'Sign Up'
        else:
            title = 'Login Window'
            label = 'Log In'
        uiscale = bui.app.ui_v1.uiscale
        bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
        self._root_widget = bui.containerwidget(
            size=(500,250),
            transition='in_scale',
            color=bg_color,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(2.1 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -10) if uiscale is babase.UIScale.SMALL else (
            240, 0) if uiscale is babase.UIScale.MEDIUM else (330, 20)
        )
        
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.8,
            color=(1,1,1),
            text=title,
            size=(0, 0),
            position=(250, 200),
            h_align='center',
            v_align='center'
        )
        
        self._id = bui.textwidget(
            parent=self._root_widget,
            scale=0.5,
            color=(1,1,1),
            text=f'Account: ' + _babase.get_v1_account_misc_read_val_2('resolvedAccountID', ''),
            size=(0, 0),
            position=(220, 170),
            h_align='center',
            v_align='center'
        )
        
        self._registrationkey_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.5,
            color=(1,1,1),
            text=f'Registration Key:',
            size=(0, 0),
            position=(100, 140),
            h_align='center',
            v_align='center'
        )
        
        self._text_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(200, 40),
            position=(175, 130),
            text='',
            maxwidth=410,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7
        )
        
        self._connect_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(150,30),
            color=(0,1,0),
            label='Get Registration Key',
            button_type='square',
            autoselect=True,
            position=(150, 80),
            on_activate_call = self._connect
        )
        
        self._confirm_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50,30),
            label=label,
            button_type='square',
            autoselect=True,
            position=(200, 40),
            on_activate_call = self._confirmcall
        )
        
        bui.textwidget(edit=self._text_field, on_return_press_call=self._confirm_button.activate)
    
    def _close(self):
        bui.containerwidget(
            edit=self._root_widget,
            transition=('out_scale')
        )

    def _connect(self):
        try:
            host = url.split('http://')[1].split(':')[0]
            import socket
            address = socket.gethostbyname(host)
            bs.disconnect_from_host()
            bs.connect_to_party(address, port=11111)
        except Exception:
            display_error('Cant get ip from hostname')

    def _confirmcall(self):
        if self.wtype == 'signup':
            key = bui.textwidget(query=self._text_field)
            answer = messenger._signup(registration_key=key) if key else None
            if answer:
                self._close()
        else:
            if messenger._login(registration_key=bui.textwidget(query=self._text_field)):
                self._close()


class AddNewIdWindow:
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
        self._root_widget = bui.containerwidget(
            size=(500,250),
            transition='in_scale',
            color=bg_color,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(2.1 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0)
        )
        
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.8,
            color=(1,1,1),
            text='Add New ID',
            size=(0, 0),
            position=(250, 200),
            h_align='center',
            v_align='center'
        )
        
        self._accountid_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.6,
            color=(1,1,1),
            text='pb-id: ',
            size=(0, 0),
            position=(50, 155),
            h_align='center',
            v_align='center'
        )
        
        self._accountid_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(250, 40),
            position=(100, 140),
            text='',
            maxwidth=410,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7
        )
        
        self._nickname_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.5,
            color=(1,1,1),
            text='Nickname: ',
            size=(0, 0),
            position=(50, 115),
            h_align='center',
            v_align='center'
        )
        
        self._nickname_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(250, 40),
            position=(100, 100),
            text='<default>',
            maxwidth=410,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7
        )
        
        self._help_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.4,
            color=(0.1,0.9,0.9),
            text='Help:\nEnter pb-id of account you\n    want to chat to\nEnter nickname of id to\n    recognize id easily\nLeave nickname <default>\n    to use their default name',
            size=(0, 0),
            position=(325, 120),
            h_align='left',
            v_align='center'
        )
        
        self._add = bui.buttonwidget(
            parent=self._root_widget,
            size=(50,30),
            label='Add',
            button_type='square',
            autoselect=True,
            position=(100, 50),
            on_activate_call=babase.Call(self._relay_function)
        )
        
        bui.textwidget(edit=self._accountid_field, on_return_press_call=self._add.activate)
        
        self._remove = bui.buttonwidget(
            parent=self._root_widget,
            size=(75,30),
            label='Remove',
            button_type='square',
            autoselect=True,
            position=(170, 50),
            on_activate_call=self._remove_id
        )
        
        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._close
        )

    def _relay_function(self):
        account_id = bui.textwidget(query=self._accountid_field)
        nickname = bui.textwidget(query=self._nickname_field)
        try:
            if messenger._save_id(account_id, nickname):
                self._close()
        except:
            display_error('Enter valid pb-id')

    def _remove_id(self):
        uiscale = bui.app.ui_v1.uiscale
        if len(messenger.saved_ids) > 1:
            choices = [i for i in messenger.saved_ids]
            choices.remove('all')
            choices_display = [babase.Lstr(value=messenger.saved_ids[i]) for i in choices]
            PopupMenuWindow(
                position=self._remove.get_screen_space_center(),
                color=babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5)),
                scale=(2.4 if uiscale is babase.UIScale.SMALL else
                       1.5 if uiscale is babase.UIScale.MEDIUM else 1.0),
                choices=choices,
                choices_display = choices_display,
                current_choice=choices[0],
                delegate=self
            )
            self._popup_type = 'removeSelectedID'

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        """Called when a choice is selected in the popup."""
        if self._popup_type == 'removeSelectedID':
            messenger._remove_id(choice)
            self._close()

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _close(self):
        bui.containerwidget(edit=self._root_widget,
                           transition=('out_scale'))


class AddNewChoiceWindow:
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        bg_color = babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5))
        self._root_widget = bui.containerwidget(
            size=(500,250),
            transition='in_scale',
            color=bg_color,
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(2.1 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -10) if uiscale is babase.UIScale.SMALL else (
            240, 0) if uiscale is babase.UIScale.MEDIUM else (330, 20)
        )
        
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.8,
            color=(1,1,1),
            text='Add Custom Command',
            size=(0, 0),
            position=(250, 200),
            h_align='center',
            v_align='center'
        )
        
        self._text_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(500, 40),
            position=(75, 140),
            text='',
            maxwidth=410,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7
        )
        
        self._help_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.4,
            color=(0.2,0.2,0.2),
            text='Use\n$c = client id\n$a = account id\n$n = name',
            size=(0, 0),
            position=(70, 75),
            h_align='left',
            v_align='center'
        )
        
        self._add = bui.buttonwidget(
            parent=self._root_widget,
            size=(50,30),
            label='Add',
            button_type='square',
            autoselect=True,
            position=(150, 50),
            on_activate_call=self._add_choice
        )
        
        bui.textwidget(edit=self._text_field, on_return_press_call=self._add.activate)
        
        self._remove = bui.buttonwidget(
            parent=self._root_widget,
            size=(50,30),
            label='Remove',
            button_type='square',
            autoselect=True,
            position=(350, 50),
            on_activate_call=self._remove_custom_command
        )
        
        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._close
        )

    def _add_choice(self):
        newCommand = bui.textwidget(query=self._text_field)
        cfg = babase.app.config
        if any(i in newCommand for i in ('$c','$a','$n')):
            cfg['Custom Commands'].append(newCommand)
            cfg.apply_and_commit()
            bui.screenmessage('Added successfully', (0,1,0))
            bui.getsound('dingSmallHigh').play()
            self._close()
        else:
            bui.screenmessage('Use at least of these ($c, $a, $n)',(1,0,0))
            bui.getsound('error').play()
    def _remove_custom_command(self):
        uiscale = bui.app.ui_v1.uiscale
        commands = babase.app.config['Custom Commands']
        
        PopupMenuWindow(
            position=self._remove.get_screen_space_center(),
            color=babase.app.config.get('PartyWindow Main Color', (0.5,0.5,0.5)),
            scale=(2.4 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0),
            choices=commands,
            current_choice=commands[0],
            delegate=self
            )
        self._popup_type = 'removeCustomCommandSelect'
    
    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        """Called when a choice is selected in the popup."""
        if self._popup_type == 'removeCustomCommandSelect':
            config = babase.app.config
            config['Custom Commands'].remove(choice)
            config.apply_and_commit()
            bui.screenmessage('Removed successfully', (0,1,0))
            bui.getsound('shieldDown').play()
    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""
    def _close(self):
        bui.containerwidget(edit=self._root_widget,
                           transition=('out_scale'))


class Manual_camera_window:
    def __init__(self):
            self._root_widget = bui.containerwidget(
                on_outside_click_call=None,
                size=(0,0)
            )
            
            button_size = (30,30)
            
            self._title_text = bui.textwidget(
                parent=self._root_widget,
                scale=0.9,
                color=(1,1,1),
                text='Manual Camera Setup',
                size=(0, 0),
                position=(130, 153),
                h_align='center',
                v_align='center'
            )
            
            self._xminus = bui.buttonwidget(
                parent=self._root_widget,
                size=button_size,
                label=babase.charstr(babase.SpecialChar.LEFT_ARROW),
                button_type='square',
                autoselect=True,
                position=(1, 60),
                on_activate_call=babase.Call(self._change_camera_position, 'x-')
            )
            
            self._xplus = bui.buttonwidget(
                parent=self._root_widget,
                size=button_size,
                label=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
                button_type='square',
                autoselect=True,
                position=(60, 60),
                on_activate_call=babase.Call(self._change_camera_position, 'x')
            )
            
            self._yplus = bui.buttonwidget(
                parent=self._root_widget,
                size=button_size,
                label=babase.charstr(babase.SpecialChar.UP_ARROW),
                button_type='square',
                autoselect=True,
                position=(30, 100),
                on_activate_call=babase.Call(self._change_camera_position, 'y')
            )
            
            self._yminus = bui.buttonwidget(
                parent=self._root_widget,
                size=button_size,
                label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
                button_type='square',
                autoselect=True,
                position=(30, 20),
                on_activate_call=babase.Call(self._change_camera_position, 'y-')
            )
            
            self.inwards = bui.buttonwidget(
                parent=self._root_widget,
                size=(100,30),
                label='INWARDS',
                button_type='square',
                autoselect=True,
                position=(120, 90),
                on_activate_call=babase.Call(self._change_camera_position, 'z-')
            )
            
            self._outwards = bui.buttonwidget(
                parent=self._root_widget,
                size=(100,30),
                label='OUTWARDS',
                button_type='square',
                autoselect=True,
                position=(120, 50),
                on_activate_call=babase.Call(self._change_camera_position, 'z')
            )
            
            self._step_text = bui.textwidget(
                parent=self._root_widget,
                scale=0.5,
                color=(1,1,1),
                text='Step:',
                size=(0, 0),
                position=(1, -20),
                h_align='center',
                v_align='center'
            )
            
            self._text_field = bui.textwidget(
                parent=self._root_widget,
                editable=True,
                size=(100, 40),
                position=(26, -35),
                text='',
                maxwidth=120,
                flatness=1.0,
                autoselect=True,
                v_align='center',
                corner_scale=0.7
            )
            
            self._reset = bui.buttonwidget(
                parent=self._root_widget,
                size=(50,30),
                label='Reset',
                button_type='square',
                autoselect=True,
                position=(120, -35),
                on_activate_call=babase.Call(self._change_camera_position, 'reset')
            )
            
            self._done = bui.buttonwidget(
                parent=self._root_widget,
                size=(50,30),
                label='Done',
                button_type='square',
                autoselect=True,
                position=(180, -35),
                on_activate_call=self._close
            )

            bui.containerwidget(
                edit=self._root_widget,
                cancel_button=self._done
            )

    def _close(self):
        bui.containerwidget(
            edit=self._root_widget,
            transition=('out_scale')
        )

    def _change_camera_position(self, direction):
        activity = bs.get_foreground_host_activity()
        node = activity.globalsnode
        aoi = list(node.area_of_interest_bounds)
        center = [(aoi[0] + aoi[3]) / 2,
                  (aoi[1] + aoi[4]) / 2,
                  (aoi[2] + aoi[5]) / 2]
        size = (aoi[3] - aoi[0],
                aoi[4] - aoi[1],
                aoi[5] - aoi[2])

        try:
            increment = float(bui.textwidget(query=self._text_field))
        except:
            #logging.exception()
            increment = 1

        if direction == 'x':
            center[0] += increment
        elif direction == 'x-':
            center[0] -= increment
        elif direction == 'y':
            center[1] += increment
        elif direction == 'y-':
            center[1] -= increment
        elif direction == 'z':
            center[2] += increment
        elif direction == 'z-':
            center[2] -= increment
        elif direction == 'reset':
            node.area_of_interest_bounds = activity._map.get_def_bound_box('area_of_interest_bounds')
            return

        aoi = (center[0] - size[0] / 2,
               center[1] - size[1] / 2,
               center[2] - size[2] / 2,
               center[0] + size[0] / 2,
               center[1] + size[1] / 2,
               center[2] + size[2] / 2)
        node.area_of_interest_bounds = tuple(aoi)


class ServerInfoWindow(bui.Window):
    def __init__(self, origin_widget=None):
        # Basic window configuration
        self._width = 600
        self._height = 500
        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                scale=(1.3 if uiscale is babase.UIScale.SMALL else
                       1.1 if uiscale is babase.UIScale.MEDIUM else 0.9),
                stack_offset=(0, -25) if uiscale is babase.UIScale.SMALL else (0, 0)
            )
        )

        # Get data from the server
        try:
            server_info = bs.get_connection_to_host_info()
            self.server_name = server_info.get('name', 'Nombre desconocido')
            self.roster = bs.get_game_roster()
        except Exception as e:
            self.server_name = "Error obteniendo datos"
            self.roster = []
            logging.exception("Error al obtener información del servidor:")

        # Configure UI elements
        self._setup_ui()

    def _setup_ui(self):
        # Window title
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 40),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text="Información del Servidor",
            scale=1.2,
            color=bui.app.ui_v1.title_color
        )

        # Close button
        self._close_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(30, self._height - 60),
            size=(50, 50),
            label='',
            on_activate_call=self.close,
            autoselect=True,
            color=(0.45, 0.63, 0.15),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        # Scroll area for content
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._width - 60, self._height - 120),
            position=(30, 50),
            highlight=False
        )

        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._width - 60, self._height * 2),
            background=False
        )

        # Show information
        self._populate_content()

    def _populate_content(self):
        v = self._height * 2 - 80  # Initial vertical position
        spacing = 30

        # Server name
        bui.textwidget(
            parent=self._subcontainer,
            position=(10, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=1.1,
            color=(0.6, 0.8, 1.0),
            text=f"Servidor: {self.server_name}",
            maxwidth=self._width - 100
        )
        v -= spacing * 1.5

        total_players = sum(1 for p in self.roster if p.get('client_id', 0) != -1)
        session = bs.get_foreground_host_session()
    
        # Get maximum players (default 8 if not available)
        max_players = session.max_players if session else 8
        
        # List of players
        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"Jugadores conectados: ({total_players}/{max_players})", 
            maxwidth=self._width - 100
        )
        v -= spacing

        for index, player in enumerate(self.roster, 1):
            display_name = player.get('display_string', 'Sin nombre')
            client_id = player.get('client_id', 'N/A')
            players = player.get('players', [])
            is_host = player.get('client_id', 0) == -1
            host_tag = "" if is_host else ""

            if index == 1:
                v -= 100
            
            # Player card
            self._create_player_card(
                pos=(30, v),
                index=index,
                display_name=display_name,
                client_id=client_id,
                players=players,
                host_tag=host_tag
            )
            v -= 100  # Space between cards

        # Adjust container height
        bui.containerwidget(
            edit=self._subcontainer,
            #height=max(self._height * 2, abs(v) + 350)
        )

    def _create_player_card(self, pos, index, display_name, client_id, players, host_tag):
        card_width = self._width - 100
        card_height = 90
        x, y = pos

        # Card background
        bui.containerwidget(
            parent=self._subcontainer,
            position=(x, y),
            size=(card_width, card_height),
            background=True,
            color=(0.2, 0.2, 0.25)
        )

        # Player number
        bui.textwidget(
            parent=self._subcontainer,
            position=(x + 15, y + card_height - 25),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=1.2,
            color=(0.8, 0.8, 1.0),
            text=f"{index}{host_tag}"
        )

        # Main information
        bui.textwidget(
            parent=self._subcontainer,
            position=(x + 100, y + card_height - 25),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.9, 0.9, 0.9),
            text=f"ID: {client_id}\nCuenta: {display_name}",
            maxwidth=card_width - 150
        )

        # Names in play
        if players:
            player_names = [p.get('name_full', 'Sin nombre') for p in players]
            bui.textwidget(
                parent=self._subcontainer,
                position=(x + 100, y + 15),
                size=(0, 0),
                h_align='left',
                v_align='bottom',
                scale=0.7,
                color=(0.7, 0.7, 0.7),
                text="Personajes: " + ", ".join(player_names),
                maxwidth=card_width - 150
            )

    def close(self):
        bui.containerwidget(edit=self._root_widget, transition='out_scale')


class LoveWindow(bui.Window):
    def __init__(self, origin_widget=None):
        # Basic window configuration
        self._width = 600
        self._height = 500
        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                scale=(1.3 if uiscale is babase.UIScale.SMALL else
                       1.1 if uiscale is babase.UIScale.MEDIUM else 0.9),
                stack_offset=(0, -25) if uiscale is babase.UIScale.SMALL else (0, 0)
            )
        )

        # Get data from the server
        try:
            server_info = bs.get_connection_to_host_info()
            self.server_name = server_info.get('name', 'Nombre desconocido')
            self.roster = bs.get_game_roster()
        except Exception as e:
            self.server_name = "Error obteniendo datos"
            self.roster = []
            logging.exception("Error al obtener información del servidor:")

        # Configure UI elements
        self._setup_ui()

    def _setup_ui(self):
        # Window title
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 40),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text="Recordatorio Importante",
            scale=1.2,
            color=bui.app.ui_v1.title_color
        )

        # Close button
        self._close_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(30, self._height - 60),
            size=(50, 50),
            label='',
            on_activate_call=self.close,
            autoselect=True,
            color=(0.45, 0.63, 0.15),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        # Scroll area for content
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._width - 60, self._height - 120),
            position=(30, 50),
            highlight=False
        )

        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._width - 60, self._height * 2),
            background=False
        )

        # Show information
        self._populate_content()

    def _populate_content(self):
        v = self._height * 2 - 80  # Initial vertical position
        spacing = 30

        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"Perdón si interrumpí tu partida, este es un",
            maxwidth=self._width - 100
        )

        v -= spacing * 1.2

        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"recordatorio de que Less te quiere mucho, este",
            maxwidth=self._width - 100
        )

        v -= spacing * 1.2

        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"no es un mensaje que reciba cualquier persona, eso",
            maxwidth=self._width - 100
        )

        v -= spacing * 1.2

        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"quiere decir que eres muy importante para él.",
            maxwidth=self._width - 100
        )

        v -= spacing * 1.2

        bui.textwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=0.9,
            color=(0.8, 0.8, 0.8),
            text=f"Cuídate mucho y toma agua.",
            maxwidth=self._width - 100
        )
        
        v -= spacing * 2.3

        bui.buttonwidget(
            parent=self._subcontainer,
            position=(20, v),
            size=(50, 50),
            label='',
            on_activate_call=self.soundHeart,
            autoselect=False,
            color=(0.45, 0.63, 0.15),
            icon=bui.gettexture('heart'),
            iconscale=1.2
        )
    
        # Adjust container height
        bui.containerwidget(
            edit=self._subcontainer,
            # height=max(self._height * 2, abs(v) + 350)
        )

    def confirm_close(self):
        # Update the file to mark that it has already been displayed

        ConfirmWindow(
            text=f'¿Segura que quieres salir?\n\n Al confirmar este mensaje no se mostrará más,\n de lo contrario de vez en cuando lo hará.',
            action = self.close,
            width=420,
            height=230,
            color=(255, 192, 203),
            text_scale=1.0,
            origin_widget=self.get_root_widget()
        )

    def close(self):
        # Update the file to mark that it has already been displayed
        with open(love_file, 'w') as f:
            f.write('show_love_message: False')
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
    
    def soundHeart(seld):
        bui.getsound('spazOw').play()


def __popup_menu_window_init__(
        self,
        position: Tuple[float, float],
        choices: Sequence[str],
        current_choice: str,
        delegate: Any = None,
        width: float = 230.0,
        maxwidth: float = None,
        scale: float = 1.0,
        color: Tuple[float, float, float] = (0.35, 0.55, 0.15),
        choices_disabled: Sequence[str] = None,
        choices_display: Sequence[babase.Lstr] = None):
        # FIXME: Clean up a bit.
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        if choices_disabled is None:
            choices_disabled = []
        if choices_display is None:
            choices_display = []

        # FIXME: For the moment we base our width on these strings so
        #  we need to flatten them.
        choices_display_fin: List[str] = []
        for choice_display in choices_display:
            choices_display_fin.append(choice_display.evaluate())

        if maxwidth is None:
            maxwidth = width * 1.5

        self._transitioning_out = False
        self._choices = list(choices)
        self._choices_display = list(choices_display_fin)
        self._current_choice = current_choice
        self._color = color
        self._choices_disabled = list(choices_disabled)
        self._done_building = False
        if not choices:
            raise TypeError('Must pass at least one choice')
        self._width = width
        self._scale = scale
        if len(choices) > 8:
            self._height = 280
            self._use_scroll = True
        else:
            self._height = 20 + len(choices) * 33
            self._use_scroll = False
        self._delegate = None  # don't want this stuff called just yet..

        # extend width to fit our longest string (or our max-width)
        for index, choice in enumerate(choices):
            if len(choices_display_fin) == len(choices):
                choice_display_name = choices_display_fin[index]
            else:
                choice_display_name = choice
            if self._use_scroll:
                self._width = max(
                    self._width,
                    min(
                        maxwidth,
                        _babase.get_string_width(choice_display_name,
                                             suppress_warning=True)) + 75)
            else:
                self._width = max(
                    self._width,
                    min(
                        maxwidth,
                        _babase.get_string_width(choice_display_name,
                                             suppress_warning=True)) + 60)

        # init parent class - this will rescale and reposition things as
        # needed and create our root widget
        PopupWindow.__init__(
            self,
            position,
            size=(self._width, self._height),
            bg_color = self._color,
            scale=self._scale
        )

        if self._use_scroll:
            self._scrollwidget = bui.scrollwidget(
                parent=self.root_widget,
                position=(20, 20),
                highlight=False,
                color=(0.35, 0.55, 0.15),
                size=(self._width - 40,
                      self._height - 40)
            )
            self._columnwidget = bui.columnwidget(
                parent=self._scrollwidget,
                border=2,
                margin=0
            )

        else:
            self._offset_widget = bui.containerwidget(
                parent=self.root_widget,
                position=(30, 15),
                size=(self._width - 40,
                      self._height),
                background=False
            )
            
            self._columnwidget = bui.columnwidget(
                parent=self._offset_widget,
                border=2,
                margin=0
            )

        for index, choice in enumerate(choices):
            if len(choices_display_fin) == len(choices):
                choice_display_name = choices_display_fin[index]
            else:
                choice_display_name = choice
            inactive = (choice in self._choices_disabled)
            wdg = bui.textwidget(
                parent=self._columnwidget,
                size=(self._width - 40, 28),
                on_select_call=babase.Call(self._select, index),
                click_activate=True,
                color=(0.5, 0.5, 0.5, 0.5) if inactive else
                ((0.5, 1, 0.5,
                  1) if choice == self._current_choice else
                 (0.8, 0.8, 0.8, 1.0)),
                padding=0,
                maxwidth=maxwidth,
                text=choice_display_name,
                on_activate_call=self._activate,
                v_align='center',
                selectable=(not inactive)
            )

            if choice == self._current_choice:
                bui.containerwidget(
                    edit=self._columnwidget,
                    selected_child=wdg,
                    visible_child=wdg
                )

        # ok from now on our delegate can be called
        self._delegate = weakref.ref(delegate)
        self._done_building = True

original_connect_to_party = bs.connect_to_party
#original_sign_in = _babase.sign_in

def modify_connect_to_party(address:str, port:int = 43210, print_progress:bool=True) -> None:
    global _ip, _port
    _ip = address
    _port = port
    original_connect_to_party(_ip, _port, print_progress)

temptimer = None
def modify_sign_in(account_type: str) -> None:
    #original_sign_in(account_type)
    if messenger.server_online:
        messenger.logged_in = False
        global temptimer
        #temptimer = bs.Timer(2, messenger._cookie_login)


class PingThread(Thread):
    """Thread for sending out game pings."""

    def __init__(self, address: str, port: int):
        super().__init__()
        self._address = address
        self._port = port

    def run(self) -> None:
        sock: Optional[socket.socket] = None
        try:
            import socket
            from babase._net import get_ip_address_type
            socket_type = get_ip_address_type(self._address)
            sock = socket.socket(socket_type, socket.SOCK_DGRAM)
            sock.connect((self._address, self._port))

            starttime = time.time()

            # Send a few pings and wait a second for
            # a response.
            sock.settimeout(1)
            for _i in range(3):
                sock.send(b'\x0b')
                result: Optional[bytes]
                try:
                    # 11: BA_PACKET_SIMPLE_PING
                    result = sock.recv(10)
                except Exception:
                    result = None
                if result == b'\x0c':
                    # 12: BA_PACKET_SIMPLE_PONG
                    accessible = True
                    break
                time.sleep(1)
            global _ping
            _ping = int((time.time() - starttime) * 1000.0)
        except Exception:
            logging.exception('Error on gather ping')
        finally:
            try:
                if sock is not None:
                    sock.close()
            except Exception:
                logging.exception('Error on gather ping cleanup')

def _get_store_char_tex(self) -> str:
        _babase.set_party_icon_always_visible(True)
        return ('storeCharacterXmas' if _babase.get_v1_account_misc_read_val(
            'xmas', False) else
                'storeCharacterEaster' if _babase.get_v1_account_misc_read_val(
                    'easter', False) else 'storeCharacter')


# ba_meta export plugin
class byLess(babase.Plugin):
    def __init__(self):
        if _babase.env().get("build_number",0) >= 20124:
            global messenger, listener, displayer, color_tracker, love_party
            initialize()
            messenger = PrivateChatHandler()
            listener = Thread(target=messenger_thread)
            listener.start()
            color_tracker = ColorTracker()
            
            # Initialize LovePartyWindow
            love_party = LovePartyWindow()
            #print("[byLess] Init love party")
            #print("LovePartyWindow initialized successfully")
            
            # Overriding original classes
            bauiv1lib.party.PartyWindow = PartyWindow
            PopupMenuWindow.__init__ = __popup_menu_window_init__
            bs.connect_to_party = modify_connect_to_party
            MainMenuWindow._get_store_char_tex = _get_store_char_tex
            
            # Show love window after initializing everything
            love_party.show_love_window()
            
        else:
            display_error("This Party Window only runs with BombSquad version higher than 1.7.39.22")