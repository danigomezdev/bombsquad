# ba_meta require api 9
# ba_meta name Less Party Window
# ba_meta description A mod that makes scaled modifications to the PartyWindow, giving multiple options for use in-game
# ba_meta version 1.1.4

from __future__ import annotations
import re
import os
import sys
import json
import time
import math
import glob
import shutil
import socket
import random
import base64
import string
import weakref
import traceback
import http.client
import urllib.request, urllib.error, urllib.parse
#from html.parser import HTMLParser
from datetime import datetime
from threading import Thread
import logging
import babase
import bauiv1 as bui
import bascenev1 as bs
from babase._general import Call, CallPartial, CallStrict
from babase._mgen.enums import SpecialChar, UIScale

import _babase # type: ignore

import bauiv1lib.party # Our Party Window Package
from bauiv1lib.confirm import ConfirmWindow
from bauiv1lib.colorpicker import ColorPickerExact
from bauiv1lib.account.viewer import AccountViewerWindow
import bauiv1lib.popup as popup
from bauiv1lib.popup import PopupMenuWindow, PopupWindow, PopupMenu


from json import (
    dumps,
    loads,
    dump,
    JSONDecodeError,
    load
)
from threading import Thread
import time
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

import _babase
import os

from bauiv1lib.tabs import TabRow
from enum import Enum

from baenv import TARGET_BALLISTICA_BUILD as build_number
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from typing import Any, Sequence, List, Optional, Dict, Tuple, Callable, Literal
    from bauiv1lib.play import PlaylistSelectContex

get_ip_address_type = babase.get_ip_address_type
disconnect_from_host = bs.disconnect_from_host # bs.disconnect_from_host()

is_muted = babase.app.config.resolve('Chat Muted')


# Global Access Variable
#==============# IDENTITY #==============#
# Add your account name if not exist later
MY_MASTER = [ # Use Correct Icons
    
]

# Your nicknames, what others calls you with that nick
# How to? ["my nick1", "my nick2"]
default_nick_names = [

]
#==============# IDENTITY #==============#

#======================= Constant =======================#
# Global max warns, applies to party window manual warns
# If warns equal to this, they'll be kicked
MAX_WARNS = 4

KICK_CMD   = '/kick'
REMOVE_CMD = '/remove'

### Anti Abuse(Bad Words) Replies ###
balas_indonesian = 'Bahasanya Tolong Dijaga'
balas_indonesian_chill = 'Santai oi..'

balas_english = 'Dont Saying Badwords Please'

balas_indian = 'Dont Swearing/Using Badwords Please'
balas_indian_chill = 'Chill Na..?'

balas_bad_emojis = 'Dont Use That Emoji Please'
###-------------------------------###
# Anti abuse language
anti_abuse_language_indonesia = True
anti_abuse_language_english = True
anti_abuse_language_hindi = True

### Manual Add Warns Text ###
# Use {name} for player name, {warn} for their warings
add_warn_msg_use_profile_name = False # Put True If You Want It Mention Their Profile Instead Acc Name
add_warn_msg_betraying = "Don\'t Betraying {name}. Warn {warn}!"
add_warn_msg_abusing = "Don\'t Abusing, {name}. Warn {warn}!"
add_warn_msg_kick_vote = "Don\'t Start Unnecessary Kick Votes, {name}. Warn {warn}!"
add_warn_msg_teaming = "Don\'t Teaming, {name}. Warn {warn}!"
# When the max reached and add baibai msg
warn_msg_max_reached = "Enough Warnings, Goodbye👋"

## Kick vote analyzer ##
# Be specific while using it, e.g:
# {voter}* vote mesage *{voted}
kick_vote_start_texts = [
    ' started a kick vote for '
]
vote_kicking_started_reply_message = "Provide the vote kicking reason `{name}` 👀"
vote_kicking_started_reply_message_noname =  "Provide the vote kicking reason 👀"

vote_kicking_started_master_reply = "Why kik me `{name}`"
vote_kicking_started_master_reply_noname = "Why kik me"

# Server Questions & Answers
# Usages:- "Question": "Answer", ...
sync_kunci_jawaban_default_with_file = True # Not Used
kunci_jawaban_default: Dict[str, str] = {
    "the owners": "VoRtEx AnD HoNoR", # >> OwnerShip
    "the owner": "VoRtEx",
    "the 1st owner": "VoRtEx",
    "the first owner": "VoRtEx",
    "the 2nd owner": "VoRtEx",
    "the second owner": "VoRtEx",
    "master": "VoRtEx",
    "edited": "VoRtEx",
    "editor": "VoRtEx",
    "the owner": "VoRtEx",
    "modded the server": "VoRtEx",
    "modded this server": "VoRtEx",
    "who is the server host": "PiKa",
    "largest planet": "JuPiTeR", # >> Quiz
    "biggest planet": "JuPiTeR",
    "smallest planet": "MeRcUrY",
    "eiffel": "PaRiS",
    "effiel tower is located in which city": "PaRiS",
    "sky": "IDK",
    "bear": "B",
    "open a single lock": "PiAnO",
    "hard to get out": "TrOuBlE",
    "playstation": "PlAyStAtIoN",
    "keep me": "PrOmiSe",
    "entra duro, seco y sale mojado": "IDK",
    "con \"c\" y termina con \"o\"": "CoDo",
    "bombsquad run on": "PyThOn", # >> About this Game
    "name of this game": "BoMbSqUaD",
    "who made this game": "Eric Froemling",
    "which currency": "TiCkEtS",
    "joined the discord": "YeS", # >> Discord
    "joined discord": "YeS",
    "joined our discord server": "YeS",
    "enjoy": "yEs",
    "country corona": "ChInA", # >> Bing Chiling ¯\_(ツ)_/¯
    "wear during corona": "MaSk",
    "wash": "YeS",
    "safe inside home": "YeS",
    "sanitize": "YeS",
    "sanitizing": "YeS",
}

# Party Window Scale
PARTY_WINDOW_SCALE_SMALL  = 0.745
PARTY_WINDOW_SCALE_MEDIUM = 0.445
PARTY_WINDOW_SCALE_LARGE  = 0.225

DEFAULT_LANGUAGES_DICT          = {
    "hi": "Hindi",
    "en": "English",
    "es": "Spanish",
    "ml": "Malayalam",
    "id": "Indonesian"
}
DEFAULT_AVAILABLE_LANG_LIST     = list(DEFAULT_LANGUAGES_DICT.values())
DEFAULT_AVAILABLE_LANG_ID_LIST  = list(DEFAULT_LANGUAGES_DICT.keys())

NEW_AVAILABLE_LANG_LIST         : list[str] = []
NEW_AVAILABLE_LANG_ID_LIST      : list[str] = []

P_NAME_STR_MAX_WIDTH            = 25 # Partywindow Player Names
MAX_MSG_LENGTH                  = 70 # Max: 80

PNAME_AND_MSG_SPLITTER          = ': '
INVALID_KEY_TEXT                = '[{0}]'

MAX_ERRORS                      = 10  # Maximum number of errors to keep in the log

CHOSEN_ICON_TO_SHOW             = '' # Icon to show when opening icon list

TEXTWIDGET_DEFAULT_COLOR        = (1, 1, 1)
CHOSEN_TEXT_HIGHLIGHT_MARK      = '>> '
TEXTWIDGET_SELECTED_COLOR       = (1, 0, 0, 1) # R, G, B, Alpha
TEXTWIDGET_CHANGE_COLOR_RANGE   = 0.3

PNAME_AND_MSG_SPLITTER_MODIFIED = ' >> ' # Dont Change If You Already Using This Plugin

MUTED_LOGS_MARK                 = "*[Muted]"

MAX_CHAT_LOGS_FILE_SIZE         = 200 # KB

JSONS_DEFAULT_INDENT_FILE       = 1

PING_MESSAGE                    = [ # Add more as you like
'Ping-pong🏓 {}ms',
'JumPing {}ms 🐇'
]

_default_server_ip = '8.8.8.8'
_default_server_port = 43210

_server_ip = _default_server_ip
_server_port = _default_server_port

_server_ping: float = 0
"""Server Ping, when available, Use `round` for rounding or use `int` to cuts the float nums"""

# Max Players To Be Shown Each Pages On Player List Popup
players_per_page_on_all_namelist = 150
players_per_page_on_current_session_namelist = 25

# Maximum of players saved data for each file, kindly dont change after your players data-
# already reached the max data, might cause multiple same players data on separated files
max_players_on_all_names_file = 3000

### BombSquad default max chat ###
# Kindly Don't Change If You Don't Know What Is This.
# Incorrect input will ruin/destroy chats data and slow down devices(Hardwares)
maximum_bombsquad_chat_messages = 40

### Partywindow default max chat ###
# Maximum party window chats to be shown when opening partywindow.
# Might inaccurate, and more means lag, dont put more unless you have a beefy device
maximum_party_window_chats = maximum_bombsquad_chat_messages + 60

### Max Individual Player's Saved Chats ###
# I don't put it more, because the size will increased everytime players chatting,
# and big size will slow down loads & saves
max_player_chat_data = maximum_bombsquad_chat_messages * 2

### Max Saved Expanded Chats ###
# Max Expanded Chats Data
# > Not 100% Accurate:
# Some Chats Can Be Dissappearing and Some Players Name Can Be Invalid(Mostly Shown as Dots "..." or Cutted)
max_internal_all_chats_data = maximum_bombsquad_chat_messages * 5

# Wheteher mention their account or profile name
use_their_profile_for_greet_friends = False

## Backups Days Delay ##
# A backup time delay by days
backup_interval = 2

sorry_delay = 5
thanks_delay = 5

SORRY_WORDS = ["Sryyy", "Sorryy", "Sry", "Sowwy", "Forgive me"] # %
SORRY_CONFESSION = ["My bad", "My fault", "My mistake", "My apologies", "Shouldn't have done that"] # $
# % = Sorry Word
# $ = Confession Word
SORRY_ARGUMENTS = [
    "%, It\'s on me",
    "Ah! %!",
    "Ah, I slipped, %...",
    "Ah, % about that!",
    "Ah, $, %!",
    "A- I did that, $!",
    "$! Wasn't my intention!",
    "$, Forgive the error...!",
    "$!",
    "%, didn't mean to mess up!",
    "%, Totally $!",
    "Didn't mean to trouble, %",
]

THANKS_WORDS = [
    "Thanks", "Thank you",
    "Thx", "Tysm", "Tqq",
    "Thanks a lot", "Much appreciated"
] # %
THANKS_ARGUMENTS = [
    "% for the help!",
    "%, you're the best!",
    "Couldn't have done it without you, %!",
    "%, You're Awesome!",
    "%, you're a lifesaver!",
    "Big thanks!",
    "%, You're Amazing!"
]

COLORS: Dict[str, tuple[float, float, float]] = {
    'black'     : (0.0, 0.0, 0.0),
    'white'     : (1.0, 1.0, 1.0),
    'red'       : (1.0, 0.0, 0.0),
    'orange'    : (1.0, 0.5, 0.0),
    'yellow'    : (1.0, 1.0, 0.0),
    'lime'      : (0.5, 1.0, 0.0),
    'green'     : (0.0, 1.0, 0.0),
    'cyan'      : (0.0, 1.0, 1.0),
    'blue'      : (0.0, 0.0, 1.0),
    'magenta'   : (1.0, 0.0, 1.0),
    'indigo'    : (0.3, 0.0, 0.5),
    'purple'    : (0.5, 0.0, 0.5),
    'pink'      : (1.0, 0.3, 0.5),
    'brown'     : (0.6, 0.4, 0.2),
    'gray'      : (0.5, 0.5, 0.5)
}
"""Get Color RGB Tuples By Color Name Using Str"""

BCSSERVER = 'mods.ballistica.workers.dev'

## CMD Logo ##
CMD_LOGO_CAUTION = "[!]"
CMD_LOGO_POSITIVE = "[+]"
CMD_LOGO_NEGATIVE = "[-]"
CMD_LOGO_POSITIVE_WARNING = "[+!]"
CMD_LOGO_NEGATIVE_WARNING = "[-!]"
CMD_LOGO_PERCENT = "[%]"
CMD_LOGO_SERVER = "[SERVER]"

####################### EMOJIS #######################
HAPPY_EMOJIS: List[str] = [
    "(◍/ω＼◍)", "( •̀ ω •́ )✧", '✧⁠◝⁠(⁠⁰⁠▿⁠⁰⁠)⁠◜⁠✧', "o(⋄°▽°⋄)o",
    "q(≧▽≦q)"
]
WTH_EMOJIS: List[str] = [
    '(⊙_◎)', '.______.', '눈_눈', '(￣﹏￣；)',
    '(•_•)', '！Σ(￣□￣;)'
]
SAD_EMOJIS: List[str] = [
    "(╥﹏╥)", "(TдT)", "ಥ‿ಥ", "(；′⌒`)",
    "(´。＿。｀)"
]
####################### EMOJIS #######################

SERVER_NAMES = [
    'Server', 'server', 'Server', 'server'
#   ,'BCS-', 'bcs-', 'BCS-', 'bcs-' 'BCS-', 'bcs-'
]

COLOR_SCREENCMD_NORMAL  = (1.0, 0.65, 0.8)
COLOR_SCREENCMD_ERROR   = (1.0, 0.20, 0.0)

CUSTOM_COMMANDS_PREFIX  = [
    '$acc',
    '$cid',
    '$name',
    '$sad',
    '$happy',
    '$unamused'
]

current_server_name = ""

list_kata_halo = [
    'hi', 'hi ', 'hif', 'hii', 'hey', 'hai', 'heya', 'hoi',
    'hlo', 'hei', 'hello', 'helo', 'halo', 'hallo', 'hemlo', 'hmlo', 'ello', 'hewwo', 'hewo',
    'greeting', 'yow', 'wsp', 'wsg', 'yo ', 'yoo', 'sup',
    'pagi', 'siang', 'sore', 'malam'
]

jawab_halo = ["Hoi", "Ello", "Hi There", "Heyy", "Hii", "Hello", "Yow", "Heya", 'Hiee', 'Hloo']


original_screenmessage  = bs.broadcastmessage
original_chatmessage    = bs.chatmessage


SystemEncode = sys.getfilesystemencoding()
if not isinstance(SystemEncode, str):
    SystemEncode = "utf-8"

def screenmessage(
	message: str,
	color: Optional[Sequence[float]] = None,
	top: bool = False,
	image: dict[str, Any] | None = None,
	log: bool = False,
	clients: Optional[Sequence[int]] = None,
	transient: bool = False
) -> None:
    original_screenmessage(message=message, color=color, top=top, image=image, log=log, clients=clients, transient=transient)

"""
bs.broadcastmessage = screenmessage
bsscreenmessage = screenmessage
bs.broadcastmessage = screenmessage
"""

def chatmessage(msg: str):
    original_chatmessage(msg)

_text_field: Optional[bui.Widget] = None

#~~~~~~~~~~~~~~~~~~~~~~~~# DIRECTORY #~~~~~~~~~~~~~~~~~~~~~~~~#
file_date = datetime.now().strftime("[%d-%m-%Y]")
#$$$$$$$$$$$$$$$$# PARTY WINDOW DATA #$$$$$$$$$$$$$$$$#
main_directory: str = _babase.env()['python_directory_user']
#main_directory = "A:/FILES/BS Party Window Data" # Custom Path For PCs (Usually). Dont ends with "/ or \"

party_window_folder_name = 'LessResponderPartyWindow'
party_window_directory: str = main_directory + f'/{party_window_folder_name}/'
#party_window_directory: str = __file__.split(__name__, 1)[0] + f'{party_window_folder_name}/'

party_window_backup_directory = main_directory + f"/{party_window_folder_name} Backup/"

## Main Data ##
quick_msg_file_name = 'QuickMessages'
quick_msg_file_path = party_window_directory + f'{quick_msg_file_name}.txt'

custom_command_file_name = 'Custom Commands'
custom_command_file_path = party_window_directory + f'{custom_command_file_name}.txt'

config_party_file_name = 'LessPartyWindowSettings'
config_party_file_path = party_window_directory + f'{config_party_file_name}.json'

internal_error_log_file_name = 'Error Logs'
internal_error_log_file_path = party_window_directory + f'{internal_error_log_file_name}.json'
## Main Data ##

cache_folder_name = 'cache'
cache_folder_path = party_window_directory + f"{cache_folder_name}/"

## Custom Translation ##
custom_translated_text_folder_name = 'translate_texts_custom_data'
custom_translated_text_folder_path = cache_folder_path + f"{custom_translated_text_folder_name}/"

custom_translated_text_file_name = '{lang_key}'
custom_translated_text_file_path = custom_translated_text_folder_path + f"{custom_translated_text_file_name}.json"
## Custom Translation ##

## New Translation ##
new_translated_text_folder_name = 'translate_texts_new_data'
new_translated_text_folder_path = cache_folder_path + f"{new_translated_text_folder_name}/"

new_translated_text_file_splitter = "-"
new_translated_text_file_name = '{lang_key}'+new_translated_text_file_splitter+'{lang}'
new_translated_text_file_path = new_translated_text_folder_path + f"{new_translated_text_file_name}.json"
## New Translation ##
#$$$$$$$$$$$$$$$$# PARTY WINDOW DATA #$$$$$$$$$$$$$$$$#

#@@@@@@@@@@@@@@@# AUTO RESPONDER DATA #@@@@@@@@@@@@@@@#
######## Chats Data ########
responder_folder_name = 'LessAutoResponder'
responder_directory: str = party_window_directory + f'{responder_folder_name}/'

chats_data_file_folder_name = 'Chats Data'
server_name_default = "Unknown Server"
chats_data_file_folder_path = responder_directory + f"{chats_data_file_folder_name}/{server_name_default}/"
internal_chats_data_file_folder_path = responder_directory + f"{chats_data_file_folder_name}/"

config_responder_file_name = 'LessResponderSettings'
config_responder_file_path = responder_directory + f'{config_responder_file_name}.json'

chats_data_file_name = 'Player Chats Data'
chats_data_file_path = chats_data_file_folder_path + f"{chats_data_file_name}.json"

internal_chats_data_file_name = 'Internal Chat Data'
internal_chats_data_file_path = internal_chats_data_file_folder_path + f"{internal_chats_data_file_name}.json"

internal_all_chats_data_file_name = 'Internal All Chat Data'
internal_all_chats_data_file_path = internal_chats_data_file_folder_path + f"{internal_all_chats_data_file_name}.json"

chats_log_file_name = 'Chats Log'
chats_log_file_path = chats_data_file_folder_path + f"{chats_log_file_name}.txt"
######## Chats Data ########

######## Other Data ########
nickname_file_name = 'My Nicknames'
nickname_file_path = responder_directory + f'{nickname_file_name}.json'

kunci_jawaban_file_name = 'QuestionsAndAnswers'
kunci_jawaban_file_path = responder_directory + f'{kunci_jawaban_file_name}.json'

custom_reply_file_name = 'Custom Replies'
custom_reply_file_path = responder_directory + f'{custom_reply_file_name}.json'
######## Other Data ########

####### Players Data #######
players_data_file_folder_name = 'Players Data'
players_data_file_folder_path = responder_directory + f"{players_data_file_folder_name}/"

all_players_data_folder_name = 'Saved All Names'
all_players_data_folder_path = players_data_file_folder_path + f"{all_players_data_folder_name}/"
all_players_data_backup_folder_path = players_data_file_folder_path + f"Backups/"
saved_names_file_name = 'SavedPlayersData'
saved_names_file_path = all_players_data_folder_path + f'{saved_names_file_name}.json'

warning_file_name = 'Player Warning Counts'
warning_file_path = players_data_file_folder_path + f'{warning_file_name}.json'

exception_for_player_names_file_name = 'Friends'
exception_for_player_names_file_path = players_data_file_folder_path + f'{exception_for_player_names_file_name}.json'

blacklist_file_name = 'Blacklisted Account Names'
blacklist_file_path = players_data_file_folder_path + f'{blacklist_file_name}.json'

muted_players_file_name = 'Muted Players'
muted_players_file_path = players_data_file_folder_path + f'{muted_players_file_name}.json'
####### Players Data #######

#-----------# Abuses Data #-----------#
id_lang = 'id'
en_lang = 'en'
hi_lang = 'hi'

abuses_languages = [id_lang, en_lang, hi_lang]

abuse_file_folder_name = 'Abuse Words List'
abuse_file_folder_path = responder_directory + f"{abuse_file_folder_name}/"
abuse_file_paths: Dict[str, str] = {
    id_lang : abuse_file_folder_path + 'Abuses-Indonesia.json',
    en_lang : abuse_file_folder_path + 'Abuses-English.json',
    hi_lang : abuse_file_folder_path + 'Abuses-Indian.json'
}
exception_for_anti_abuse_file_name = 'Words Exception'
exception_for_anti_abuse_file_path = abuse_file_folder_path + f'{exception_for_anti_abuse_file_name}.json'
#-----------# Abuses Data #-----------#

#~~~~~~~~~~~ Server Players Data ~~~~~~~~~~~#
players_server_data_name = "Server Players Data"
players_server_data_folder_path = responder_directory + f"{players_server_data_name}/"
#~~~~~~~~~~~ Server Players Data ~~~~~~~~~~~#

#@@@@@@@@@@@@@@@# AUTO RESPONDER DATA #@@@@@@@@@@@@@@@#
#~~~~~~~~~~~~~~~~~~~~~~~~# DIRECTORY #~~~~~~~~~~~~~~~~~~~~~~~~#


def get_random_happy_emoji() -> str:
    return random.choice(HAPPY_EMOJIS)
def get_random_unamused_emoji() -> str:
    return random.choice(WTH_EMOJIS)
def get_random_sad_emoji() -> str:
    return random.choice(SAD_EMOJIS)

def get_app_lang_as_id() -> str:
    """
    Returns The Language `ID`.
    Such as: `id`, `en`, `hi`, `...`
    """
    party_lang = party_config.get(CFG_NAME_PREFFERED_LANG)
    if party_lang:
        return party_lang
    App_Lang = bs.app.lang.language
    lang_id = 'en'
    if App_Lang in DEFAULT_AVAILABLE_LANG_LIST:
        if App_Lang == 'Indonesian':
            lang_id = 'id'
        elif App_Lang == 'Spanish':
            lang_id = 'es'
        elif App_Lang == 'Malayalam':
            lang_id = 'ml'
        elif App_Lang == 'Hindi': # Lol, no :(
            lang_id = 'hi'
        else:
            lang_id = 'en'
    party_config[CFG_NAME_PREFFERED_LANG] = lang_id
    return lang_id

def get_random_sorry_word() -> str:
    sorry = (random.choice(SORRY_ARGUMENTS).replace(
        '%', random.choice(SORRY_WORDS)).replace(
        '$', random.choice(SORRY_CONFESSION)))
    return sorry

def get_random_thanks_word() -> str:
    thanks = (random.choice(THANKS_ARGUMENTS).replace(
        '%',  random.choice(THANKS_WORDS)))
    return thanks

my_directory = _babase.env()['python_directory_user'] + "/UltraServerFinder"
best_friends_file = os.path.join(my_directory, "BestFriends.txt")
configs_file = os.path.join(my_directory, "configs.json")

def ensure_files_exist():
    """Ensure UltraServerFinder directory and required files exist."""
    # Create the folder if it doesn't exist
    os.makedirs(my_directory, exist_ok=True)

    # Create BestFriends.txt if it doesn't exist
    if not os.path.exists(best_friends_file):
        with open(best_friends_file, "w", encoding="utf-8") as f:
            f.write("")

    # Create configs.json if it doesn't exist
    if not os.path.exists(configs_file):
        with open(configs_file, "w", encoding="utf-8") as f:
            dump({}, f, indent=4, ensure_ascii=False)

def load_config():
    ensure_files_exist()
    with open(configs_file, "r", encoding="utf-8") as f:
        try:
            return load(f)
        except JSONDecodeError:
            return {}

class Finder:
    VER = '1.1'
    config = load_config()
    COL1 = tuple(config.get("COL1", (0.1, 0.1, 0.1)))
    COL2 = tuple(config.get("COL2", (0.2, 0.2, 0.2)))
    COL3 = tuple(config.get("COL3", (0.6, 0.2, 0.4)))
    COL4 = tuple(config.get("COL4", (1, 0.08, 0.58)))
    COL5 = tuple(config.get("COL5", (1, 0.3, 0.6)))
    
    MAX = 0.3
    TOP = 1
    MEM = []
    ART = []
    BST = []
    BUSY = False
    KIDS = []
    P2 = None
    ARTT = None
    SL = None
    TIP = None
    FLT = ''

    def __init__(s,src):
        config = load_config()
        #s.friends_open = config.get("friends_open", False)
        s.friends_open = True

        s.thr = []
        s.ikids = []
        s.ibfriends = []
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

        if s.friends_open:
            s._FriendsWindow()

        edit_color = bw(
            parent=c.MainParent,
            position=(350, 390),
            size=(45, 38),
            autoselect=True,
            button_type='square',
            label='',
            color=s.COL1,
            oac=lambda: s._make_color_picker(
                position=(s.root.get_screen_space_center()),
                initial_color=s.COL5,
                call='color',
            )
        )
        
        iw(
            parent=c.MainParent,
            size=(45, 45),
            position=(350, 390),
            draw_controller=edit_color,
            texture=gt('menuButton'),
        )

        _friends_connected_btn = bw(
            parent=c.MainParent,
            position=(400, 390),
            size=(45, 38),
            autoselect=True,
            button_type='square',
            label='',
            color=s.COL1,
            #oac=lambda:(
            #    s._toggleFriendsWindow()
            #)
        )
        
        iw(
            parent=c.MainParent,
            size=(45, 45),
            position=(400, 390),
            draw_controller=_friends_connected_btn,
            texture=gt('usersButton'),
        )

        s.bf_connected = len(s._getAllBestFriendsConnected(["\ue063" + player.strip() for player, _ in s.plys()]))
        s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()])

        s._users_connected_count = tw(
            parent=c.MainParent,
            text=str(s.bf_connected),
            size=(0, 0),
            position=(400 + 21, 390 + 16),
            h_align="center",
            v_align="center",
            scale=0.6,
            color=(0,1,0,1),
            draw_controller=_friends_connected_btn  
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
        _parent1 = sw(
            parent=c.MainParent,
            position=(20,18),
            size=(205,122),
            border_opacity=0.4,
            color=s.COL4
        )

        c.MainParent2 = ocw(
            parent=_parent1,
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
        c.SL and s._info(c.SL)
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
        s._info(p)

    def _info(s,p):
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
                label='Agregar \nAmigo',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(lambda: (
                    s._addFriend(p),
                    s._refreshBestFriendsUI(),
                    s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()])
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
                oac=CallStrict(CON, i['a'], i['p'], False)
            ))
    
    def _saveConfigs(s, config: dict):
        os.makedirs(my_directory, exist_ok=True)
        with open(configs_file, "w", encoding="utf-8") as f:
            dump(config, f, indent=4, ensure_ascii=False)

    def _FriendsWindow(s):

            sizeWindow = (355,435)
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

            # Best friends list
            s._parent3 = sw(
                parent=s.ParentFriends,
                position=(465-450, 240),
                size=(140, 130),
                border_opacity=0.4
            )
            s._parent4 = None  # Init empty
            s._refreshBestFriendsUI()

            # Best friends(Connected) list
            s._parent4 = sw(
                parent=s.ParentFriends,
                position=(465-450, 17),
                size=(140, 170),
                border_opacity=0.4
            )

            s._parent5 = None  # Init empty

            s._parent6 = sw(
                parent=s.ParentFriends,
                position=(615-450, 17),
                size=(175, 170),
                border_opacity=0.4
            )

            s.tip_bf = tw(
                parent=s._parent6,
                size=(150, 155),  
                position=(0, 0),
                text='Selecciona un amigo \npara ver donde está',
                color=s.COL4,
                maxwidth=150,
                h_align='center',
                v_align='center'
            )
            s._refreshBestFriendsUI()
            s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()])

    def _toggleFriendsWindow(s):
        s.friends_open = not getattr(s, "friends_open", False)

        config = load_config()
        config["friends_open"] = s.friends_open
        s._saveConfigs(config)
        
        if s.friends_open:
            s._FriendsWindow()

        else:
            if hasattr(s, "ParentFriends") and s.ParentFriends and s.ParentFriends.exists():
                s.ParentFriends.delete()
                s.ParentFriends = None

    def _updateCount(s):
        new_count = len(
            s._getAllBestFriendsConnected(
                ["\ue063" + player.strip() for player, _ in s.plys()]
            )
        )
    
        if getattr(s, "_users_connected_count", None) and s._users_connected_count.exists():
            tw(edit=s._users_connected_count, text=str(new_count))


    def _refreshBestFriendsUI(s):
        if hasattr(s, "_parent4_friends") and s._parent4_friends and s._parent4_friends.exists():
            s._parent4_friends.delete()

        friends_connected_list = s.get_all_friends()
        sy2 = max(len(friends_connected_list) * 30, 140)

        s._parent4_friends = ocw(
            parent=s._parent3,
            size=(190, sy2),
            background=False
        )

        # if there are no friends
        if not friends_connected_list:
            #tw(
            #    parent=s._parent3,
            #    position=(-1000, 10),
            #    text='Sin amigos \nconectados',
            #    color=s.COL3,
            #    size=(130, 100),
            #    h_align='center',
            #    v_align='center'
            #)
            #return
            friends_connected_list = ["\ue063spaz"]

        for i, friend in enumerate(friends_connected_list):
            display_name = friend if len(friend) <= 7 else friend[:7] + "..."
            pos_y = sy2 - 30 - 30 * i

            tw(
                parent=s._parent4_friends,
                size=(170, 30),
                color=s.COL3,
                text=display_name,
                position=(0, pos_y),
                maxwidth=160,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(s._showFriendPopup, friend, (200, 100))
            )


    def _refreshBestFriendsConnectedUI(s, p):
        if not (s.ParentFriends and s.ParentFriends.exists()):
            #print("[DEBUG]: BestFriends panel does not exist, aborting refresh.")
            return
        
        if hasattr(s, "_parent4_best") and s._parent4_best and s._parent4_best.exists():
            s._parent4_best.delete()
            s._parent4_best = None
            s._parent5_best = None

        # List of best friends online
        best_friends_connected_list = s._getAllBestFriendsConnected(p)
        sy3 = max(len(best_friends_connected_list) * 30, 140)

        # Main scrollable container
        if not hasattr(s, "_parent4_best") or not (s._parent4_best and s._parent4_best.exists()):
            s._parent4_best = sw(
                parent=s.ParentFriends,
                position=(465-450, 17),
                size=(140, 170),
                border_opacity=0.4
            )

        # New container with best friends list
        s._parent5_best = ocw(
            parent=s._parent4_best,
            size=(190, sy3),
            background=False
        )

        # If there are no connected
        if not best_friends_connected_list:
            tw(
                parent=s._parent5_best,
                position=(42, 50),
                text="Uh, parece que \nno hay amigos \nen línea, prueba \nbuscando servidores",
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
                parent=s._parent5_best,
                size=(170, 30),
                color=s.COL3,
                text=display_name,
                position=(0, pos_y),
                maxwidth=160,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(s._infoBestFriend, friend),
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
                s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()])
            )
        )
        s._popup_target = friend  

    def popup_menu_closing(s, popup_window) -> None:
        s._popup_target = None


    def _infoBestFriend(s, p):
        # Clean the player (remove the prefix if it exists)
        clean_p = p.lstrip("\ue063")

        # Clean Ui
        [_.delete() for _ in s.ibfriends]
        s.ibfriends.clear()
        s.tip_bf and s.tip_bf.delete()
        
        c = s.__class__
        i = None

        for idx, _ in enumerate(c.MEM):
            for r in _.get('roster', []):
                spec = loads(r['spec'])
                if spec['n'] == clean_p:
                    i = _
                    pz = r['p']
                    break
            if i is not None:
                break

        server_name = i.get("n", "Unknown")
        server_ip = i.get("a", "N/A")
        server_port = i.get("p", "N/A")

        s.ibfriends.append(tw(
            parent=s._parent6,
            position=(0, 0),
            h_align='center',
            maxwidth=160,
            text=f"{server_name}\n{server_ip}\n{server_port}",
            color=s.COL4,
            size=(160,40)
        ))

        if i is None:
            c.SL = None
            tw(c.TIP, text=s.tip)
            return

        account_v2 = [str(list(_.values())[1]) for _ in pz]

        s.ibfriends.append(bw(
            parent=s._parent6,
            position=(253, 65),
            size=(170, 30),
            label=str(account_v2[0]) if account_v2 and account_v2[0] != [] else clean_p,
            color=s.COL2,
            textcolor=s.COL4,
            oac=Call(s.oke, '\n'.join([' | '.join([str(j) for j in _.values()]) for _ in pz]) or 'Nothing')
        ))

        if p.startswith("\ue063"):
            # v2: Show both buttons side by side
            s.ibfriends.append(bw(
                parent=s._parent6,
                position=(14, 30),
                size=(60, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=CallStrict(CON, i['a'], i['p'], False)
            ))

            s.ibfriends.append(bw(
                parent=s._parent6,
                position=(84, 30),
                size=(75, 30),
                label='Eliminar \nAmigo',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(lambda: (
                    s._deleteFriend(p),
                    s._refreshBestFriendsUI(),
                    s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()]),
                    [_.delete() for _ in s.ibfriends]
                ))
            ))

        else:   
            s.ibfriends.append(bw(
                parent=s._parent6,
                position=(0, 30),
                size=(156, 30),
                label='Conectar',
                color=s.COL2,
                textcolor=s.COL4,
                oac=Call(CON, i['a'], i['p'], False)
            ))

    def make_theme_from_picker(s, base_color):
        def adjust(color, factor):
            return tuple(max(0.0, min(1.0, c * factor)) for c in color)

        # convert list to tuple if coming from picker
        base = tuple(base_color)

        return {
            "COL1": (0.1, 0.1, 0.1),      # dark fixed background
            "COL2": (0.2, 0.2, 0.2),      # secondary fund
            "COL3": adjust(base, 0.6),    # a little darker
            "COL4": base,                 # exact main color of the picker
            "COL5": adjust(base, 1.2),    # brighter
        }


    def _make_color_picker(s, position, initial_color, call):
        import bauiv1lib as bui

        return bui.colorpicker.ColorPicker(
            parent=s.root,
            position=position,
            initial_color=initial_color,
            delegate=s,
            tag=call,
        )
    
    def save_colors_to_config(s, colors: dict):
        """Save colors to the configuration file."""
        config = load_config()
        for k, v in colors.items():
            config[k] = tuple(v)
        s._saveConfigs(config)


    def load_colors_from_config(s):
        "Loads colors from config and applies them to Finder."
        config = load_config()
        for k in ["COL1", "COL2", "COL3", "COL4", "COL5"]:
            if k in config:
                setattr(Finder, k, tuple(config[k]))


    def color_picker_selected_color(s, picker, color):
        tag = picker.get_tag()
        tema = s.make_theme_from_picker(color)

        # Update the attributes of the Finder class
        for k, v in tema.items():
            setattr(Finder, k, tuple(v))

        # Save to config
        s.save_colors_to_config(tema)

        # Debug
        #print("[DEBUG] Variables Finder actualizadas:")
        for k in ["COL1", "COL2", "COL3", "COL4", "COL5"]:
            #print(f"  {k} = {getattr(Finder, k)}")
            pass

        #print(f"[DEBUG] Color seleccionado: {tuple(color)} para tag: {tag}")

        if tag == 'color':
            s._color = tuple(color)
            #print(f"[DEBUG] Color principal actualizado: {s._color}")

        elif tag == 'highlight':
            s._highlight = tuple(color)
            #print(f"[DEBUG] Highlight actualizado: {s._highlight}")


    def color_picker_closing(s, picker):
        s.bye()
        teck(0.25, byLess.up)
        

    def on_popup_cancel(s):
        pass
        #print("[DEBUG] Picker cancelado")

    def oke(s,t):
        TIP(t)
        s.ding(1,1)

    def copy(s,t):
        s.ding(1,1)
        TIP('¡Copiado en el portapapeles!')
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

    def open(s):
        c = s.__class__
        ocw(c.root, transition='in_scale')
    
    def ding(s,*z):
        a = ['Small','']
        for i,_ in enumerate(z):
            h = 'ding'+a[_]
            teck(i/10,CallStrict(s.snd,h) if i<(len(z)-1) else gs(h).play)
    
    def fresh(s):
        c = s.__class__
        if c.BUSY:
            TIP("Still busy!")
            s.ding(0,0)
            return
        TIP('¡Escaneando servidores!\nEsto debería tardar unos segundos.\nPuedes cerrar esta ventana.')
        c.ST = time.time()
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

    def _getAllBestFriendsConnected(s, pl: list[str] | None = None) -> list[str]:
        best_friends = s.get_all_friends()
        connected_best_friends = []

        # If no pl is passed or is empty, returns empty list
        if not pl:
            return []

        for p in pl:
            if p in best_friends:
                connected_best_friends.append(p)

        return connected_best_friends

    def _addFriend(s, friend: str):
        ensure_files_exist()

        if not friend or friend.strip() == "":
            push('El campo está vacío, no se puede agregar', (1,0,0))
            gs('error').play()
            return

        prefixed_friend = f"\ue063{friend.strip()}"

        with open(best_friends_file, "r", encoding="utf-8") as f:
            existing = [line.strip() for line in f.readlines()]

        if prefixed_friend not in existing:
            with open(best_friends_file, "a", encoding="utf-8") as f:
                f.write(prefixed_friend + "\n")

            s.ding(1, 0)
            s.bf_connected += 1
            s._updateCount()
            s._refreshBestFriendsUI()
            TIP(f"{prefixed_friend} agregado con éxito")
        else:
            TIP(f"{prefixed_friend} ya está en la lista")


    def _deleteFriend(s, friend: str):
        ensure_files_exist()

        if not friend or friend.strip() == "":
            push('El campo está vacío, no se puede eliminar', (1, 0, 0))
            gs('error').play()
            return

        prefixed_friend = f"{friend.strip()}"

        with open(best_friends_file, "r", encoding="utf-8") as f:
            existing = [line.strip() for line in f.readlines()]

        if prefixed_friend in existing:
            with open(best_friends_file, "w", encoding="utf-8") as f:
                for line in existing:
                    if line != prefixed_friend:
                        f.write(line + "\n")

            s.ding(0, 1)
            s.bf_connected -= 1
            TIP(f"{prefixed_friend} eliminado con éxito")
            s._updateCount()
            s._refreshBestFriendsUI()
        else:
            TIP(f"{prefixed_friend} no se encuentra en la lista")


    def kang(s,r):
        c = s.__class__
        c.MEM = r['l']
        c.ART = [cs(sc.OUYA_BUTTON_U)]*len(c.MEM)
        s.thr = []
        for i,_ in enumerate(c.MEM):
            t = Thread(target=CallStrict(s.ping,_,i))
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
            cs(sc.OUYA_BUTTON_O) if (p is not None and p < 100) else
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
                on_activate_call=CallStrict(s.hl,_,p),
                v_align='center'
            )
            if not dun and p == c.SL: ocw(c.MainParent2,visible_child=tt); dun = 1
            c.KIDS.append(tt)

    def done(s):
        s.ding(0,1)
        [_.join() for _ in s.thr]
        s.thr.clear()
        c = s.__class__
        tt = time.time() - c.ST
        ln = len(s.MEM)
        ab = int(ln/tt)
        TIP(f'¡Terminado!\nEscaneados {ln} servidores en {round(tt,2)} segundos!\nAproximadamente {ab} servidor{["es",""][ab<2]}/seg')
        s.__class__.BUSY = False
        s._refreshBestFriendsConnectedUI(["\ue063" + player.strip() for player, _ in s.plys()])
        s._updateCount()

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
    sock = socket.socket(IPT(address),socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        ping_start_time = time.time()
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
            time.sleep(ping_wait)
        if ping_success:
            ping_result = (time.time() - ping_start_time) * 1000
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
        roster_listen_start_time = time.time()
        while time.time() - roster_listen_start_time < (timeout / 2): # Use part of the total timeout
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
    size=size
))


#cw = lambda *,size=None,oac=None,**k: (p:=ocw(
#    parent=zw('overlay_stack'),
#    background=False,
#    transition='in_scale',
#    size=size,
#    on_outside_click_call=oac,
#    **k
#)) and (p,iw(
#    parent=p,
#    size=size
#))

# Global
BTW = lambda t: (push(t,color=(1,1,0)),gs('block').play())
TIP = lambda t: push(t,Finder.COL3)


button_delays_dict: Dict[str, dict[str, float]] = {}
class ButtonDelayHandler:
    global button_delays_dict
    def __init__(self):
        pass

    def start(
            self,
            button_widget: bui.Widget,
            delay_key: str, 
            message: Callable[[], str],
            delay_time: float):
        """
        Memulai delay untuk tombol.

        button_widget: Tombol (widget) yang akan diedit.
        delay_key: Nama kunci untuk menampilkan dan menyimpan delay (melanjutkan).
        message: Pesan khusus yang akan disampaikan.
        delay_time: Waktu delay maksimum (dalam detik).
        """

        if delay_key not in button_delays_dict:
            button_delays_dict[delay_key] = {}
            button_delays_dict[delay_key]["delay"] = delay_time
            button_delays_dict[delay_key]["current_delay"] = 0

        current_delay = button_delays_dict[delay_key]["current_delay"]
        button_delay = button_delays_dict[delay_key]["delay"]

        delay = button_delay - current_delay
        if delay < button_delay:
            screenmessage(message="Too fast!", color=COLOR_SCREENCMD_NORMAL)
            return

        chatmessage(message())

        button_delays_dict[delay_key]["current_delay"] = delay_time
        for i in range(int(delay_time * 10) + 1):
            babase.apptimer(i / 10, CallStrict(self._update_delay, button_widget, delay_key, i / 10))

    def update_button_label(self, button: bui.Widget, delay_name: str):
        current_delay = button_delays_dict[delay_name]["current_delay"]
        button_delay = button_delays_dict[delay_name]["delay"]

        delay = button_delay - current_delay
        if delay < button_delay:
            remaining_time = round(current_delay, 1)
            label = str(remaining_time)
        else:
            label = delay_name

        if button.exists():
            bui.buttonwidget(edit=button, label=label)

    def _update_delay(self, button: bui.Widget, delay_name: str, elapsed_time: float, is_continue: bool = False):
        if not is_continue:
            elapsed = button_delays_dict[delay_name]["delay"] - elapsed_time
            button_delays_dict[delay_name]["current_delay"] = round(elapsed, 1)
        self.update_button_label(button, delay_name)

    def continue_delay(self, button: bui.Widget, delay_name: str) -> str:
        if delay_name not in button_delays_dict: return ""

        current_delay = button_delays_dict[delay_name]["current_delay"]
        last_delay = round(sorry_delay - current_delay, 1)
        print(f'Continuing Button [{delay_name}] Delay From {last_delay}')
        if current_delay < sorry_delay:
            for i in range(int((last_delay) * 10) + 1):
                babase.apptimer(i / 10, Call(self._update_delay, button, delay_name, current_delay * 10 + i, True))
        return str(last_delay)

    def get_delay(self, delay_name: str) -> float | bool:
        if delay_name in button_delays_dict:
            delay = button_delays_dict[delay_name]["current_delay"]
            if delay > 0:
                return delay
        return False

Translate_Texts: Dict[str, dict[str, str]] = {
'opsiBisu': { # >> menuOption
    'id': 'Opsi Bisu Pesan',
    'en': 'Mute Chats Option',
    'hi': 'Chat Bisu Vikalp',
    'es': 'Opción de Silenciar Chats',
    'ml': 'Chats Mute Vikalp'
},
'modifWarnaParty': {
    'id': 'Ubah Warna PartyWindow',
    'en': 'Modify PartyWindow Color',
    'hi': 'PartyWindow Rang Badlo',
    'es': 'Modificar Color de PartyWindow',
    'ml': 'PartyWindow Color Modify Cheyyuka'
},
'tambahResponCepat': {
    'id': 'Tambah Respon Cepat',
    'en': 'Add A Quick Respond',
    'hi': 'Ek Tez Pratikriya Jodo',
    'es': 'Agregar una Respuesta Rápida',
    'ml': 'Oru Quick Respond Add Cheyyuka'
},
'tambahResponCepatTutorial': {
    'id': 'Isi TextBar Dengan Teks Respon Cepat Kamu\nUntuk Menambah Respon Cepat',
    'en': 'Fill The TextBar With Your Quick Respond Texts\nTo Add A Quick Respond',
    'hi': 'Apne Tez Pratikriya Lekh TextBar Mein Bharein\nEk Tez Pratikriya Jodne Ke Liye',
    'es': 'Llena la Barra de Texto con tus Textos de Respuesta Rápida\nPara Agregar una Respuesta Rápida',
    'ml': 'Ningalude Quick Respond Texts TextBaril Nirakkuka\nOru Quick Respond Add Cheyyan'
},
'hapusResponCepat': {
    'id': 'Hapus Respon Cepat',
    'en': 'Remove A Quick Respond',
    'hi': 'Ek Tez Pratikriya Hatayein',
    'es': 'Eliminar una Respuesta Rápida',
    'ml': 'Oru Quick Respond Remove Cheyyuka'
},
'muteInGameOnly': { # >> Mute Type
    'id': 'Nonaktifkan Dalam Game Saja',
    'en': 'Mute In Game Messages Only',
    'hi': 'Keval Khel Mein Sandesh Bisu Karein',
    'es': 'Silenciar Solo Mensajes en el Juego',
    'ml': 'Game Messages Matram Mute Cheyyuka'
},
'mutePartyWindowOnly': {
    'id': 'Nonaktifkan Pesan PartyWindow Saja',
    'en': 'Mute Party Window Messages Only',
    'hi': 'Keval PartyWindow Sandesh Bisu Karein',
    'es': 'Silenciar Solo Mensajes de PartyWindow',
    'ml': 'PartyWindow Messages Matram Mute Cheyyuka'
},
'muteAll': {
    'id': 'Nonaktifkan Semua',
    'en': 'Mute all',
    'hi': 'Sab Bisu Karein',
    'es': 'Silenciar Todo',
    'ml': 'Ellam Mute Cheyyuka'
},
'unmuteAll': {
    'id': 'Aktifkan Semua',
    'en': 'Unmute All',
    'hi': 'Sab Ko Unmute Karein',
    'es': 'Desactivar Silencio de Todo',
    'ml': 'Ellam Unmute Cheyyuka'
},
'hapusResponCepatPilihText': { # >> Quick Respond
    'id': 'Telah Dihapus Dari Respon Cepat',
    'en': 'Removed From Quick Respond',
    'hi': 'Tez Pratikriya Se Hataya Gaya',
    'es': 'Eliminado de Respuesta Rápida',
    'ml': 'Quick Respondil Ninnum Remove Cheythu'
},
'editResponCepat': {
    'id': 'Kustomisasi Respon Cepat',
    'en': 'Edit Quick Respond',
    'hi': 'Tez Pratikriya Ko Edit Karein',
    'es': 'Editar Respuesta Rápida',
    'ml': 'Quick Respond Edit Cheyyuka'
},
'saveLastGameReplay': {
    'id': 'Simpan Game Replay Terakhir',
    'en': 'Save Last Game Replay',
    'hi': 'Aakhri Khel Replay Ko Save Karein',
    'es': 'Guardar Repetición del Último Juego',
    'ml': 'Last Game Replay Save Cheyyuka'
},
'sortQuickRespond': {
    'id': 'SORTIR URUTAN',
    'en': 'EDIT ORDER',
    'hi': 'KRAM SANSODHAN',
    'es': 'EDITAR ORDEN',
    'ml': 'ORDER EDIT CHEYYUKA'
},
'voteKickConfirm': { # >> Kicking
    'id': 'Voting Untuk Menendang Pemain Ini?',
    'en': 'Vote Kick This Player?',
    'hi': 'Is Khiladi Ko Vote Kick Karein?',
    'es': '¿Votar para Expulsar a Este Jugador?',
    'ml': 'Ee Playerine Vote Kick Cheyyuka?'
},
'cantKickHost': {
    'id': 'Kamu Tidak Bisa Menendang Tuan Rumah',
    'en': 'You Can\'t Kick The Host',
    'hi': 'Aap Mezabaan Ko Laat Nhi Maar Sakate',
    'es': 'No Puedes Expulsar al Anfitrión',
    'ml': 'Nee Hostine Kick Cheyyan Kazhiyilla'
},
'cantKickMaster': {
    'id': 'Kamu Tidak Bisa Menendang Diri Sendiri',
    'en': 'You Can\'t Kick Yourself',
    'hi': 'Aap Khud Ko Kick Nahi Kar Sakte',
    'es': 'No Puedes Expulsarte A Ti Mismo',
    'ml': 'Nee Thanneye Kick Cheyyan Kazhiyilla'
},
'votekick': { # >> Party Member Press
    'id': 'Voting Keluar',
    'en': 'Vote Kick',
    'hi': 'Vote Kick',
    'es': 'Votar Expulsión',
    'ml': 'Vote Kick'
},
'mention': {
    'id': 'Tag Pemain Ini',
    'en': 'Mention This Player',
    'hi': 'Is Khiladi Ko Mention Karein',
    'es': 'Mencionar a Este Jugador',
    'ml': 'Ee Playerine Mention Cheyyuka'
},
'warnInfo': {
    'id': 'Peringatan: {}',
    'en': 'Warns: {}',
    'hi': 'Chitavani: {}',
    'es': 'Advertencias: {}',
    'ml': 'Warning: {}'
},
'partyPressWarnAdd': {
    'id': 'Beri Peringatan',
    'en': 'Give Warn',
    'hi': 'Chitavani De',
    'es': 'Dar Advertencia',
    'ml': 'Warning Kodukkuka'
},
'partyPressWarnDecrease': {
    'id': 'Kurangi Peringatan',
    'en': 'Decrease Warn',
    'hi': 'Chitavani Kam Karein',
    'es': 'Disminuir Advertencia',
    'ml': 'Warning Kurakkuka'
},
'addNewLangNoSplitter': {
    'id': 'Masukkan \"{}\" diantara id-bahasa dan Bahasa',
    'en': 'Put \"{}\" between lang-id and Lang',
    'hi': 'lang-id aur Lang ke beech \"{}\" rakhein',
    'es': 'Ponga \"{}\" entre lang-id y Lang',
    'ml': 'Lang-idum Langum itayil \"{}\" vechuka'
},
'addNewLangInvalid': {
    'id': 'Itu bukan format yang valid',
    'en': 'That is not a valid format',
    'hi': 'Yeh ek valid format nahi hai',
    'es': 'Ese no es un formato válido',
    'ml': 'Atu oru valid format alla'
},
'addNewLangExist': {
    'id': 'Bahasa itu sudah ada di kamus',
    'en': 'That language already exist in the dictionaries',
    'hi': 'Woh bhasha pehle se hi dictionaries mein maujood hai',
    'es': 'Ese idioma ya existe en los diccionarios',
    'ml': 'Aa bhasha dictionariesil itayil undu'
},
'playerInfo': {
    'id': 'Info Pemain',
    'en': 'Player Info',
    'hi': 'Khiladi Ki Jankari',
    'es': 'Información del Jugador',
    'ml': 'Player Info'
},
'playerInfoNotFound': {
    'id': 'Tidak Dapat Menemukan Info Pemain Ini',
    'en': 'Can\'t Find This Player Info',
    'hi': 'Is kheladi ki jankari nahi mili',
    'es': 'No se puede encontrar la información de este jugador',
    'ml': 'Ee playernte info kandilla'
},
'adminkick': {
    'id': 'ID Tendang: {0}',
    'en': 'Kick ID: {0}',
    'hi': 'Kick ID: {0}',
    'es': 'Expulsar ID: {0}',
    'ml': 'Kick ID: {0}'
},
'adminKickConfirm': {
    'id': 'Tendang Player Ini',
    'en': 'Kick This Player',
    'hi': 'Is Khiladi Ko Kick Karein',
    'es': '¿Expulsar a Este Jugador',
    'ml': 'Ee Playerine Kick Cheyyuka'
},
'adminremove': {
    'id': 'Singkirkan: {0}',
    'en': 'Remove: {0}',
    'hi': 'Hatayein: {0}',
    'es': 'Eliminar: {0}',
    'ml': 'Remove: {0}'
},
'adminRemoveConfirm': {
    'id': 'Singkirkan Player Ini',
    'en': 'Remove This Player',
    'hi': 'Is Khiladi Ko Hatayein',
    'es': '¿Eliminar a Este Jugador',
    'ml': 'Ee Playerine Remove Cheyyuka'
},
'addNewChoiceCmd': {
    'id': 'PERINTAH BARU',
    'en': 'NEW CMD',
    'hi': 'NAYA CMD',
    'es': 'NUEVO CMD',
    'ml': 'PUTHIYA CMD'
},
'sortChoiceCmd': {
    'id': 'SORTIR PERINTAH',
    'en': 'SORT CMD',
    'hi': 'CMD KO SORT KAREIN',
    'es': 'ORDENAR CMD',
    'ml': 'CMD SORT CHEYYUKA'
},
'customCommands': {
    'id': 'Perintah Kustom',
    'en': 'Custom Command',
    'hi': 'Custom Command',
    'es': 'Comando Personalizado',
    'ml': 'Custom Command'
},
'editCustomCommands': {
    'id': 'Kustomisasi Perintah Kustom',
    'en': 'Edit Custom Commands',
    'hi': 'Custom Commands Ko Edit Karein',
    'es': 'Editar Comandos Personalizados',
    'ml': 'Custom Commands Edit Cheyyuka'
},
'addCustomCommands': {
    'id': 'Tambah Perintah Kustom',
    'en': 'Add Custom Commands',
    'hi': 'Custom Commands Jodein',
    'es': 'Agregar Comandos Personalizados',
    'ml': 'Custom Commands Add Cheyyuka'
},
'customCommandsNoCmdPrefix': {
    'id': 'Gunakan Setidaknya Salah Satu Dari Ini: {0}',
    'en': 'Atleast Use One Of These: {0}',
    'hi': 'Kam Se Kam Inme Se Ek Ka Upyog Karein: {0}',
    'es': 'Al Menos Usa Uno de Estos: {0}',
    'ml': 'Ithil Oru Upayogikkuka: {0}'
},
'translateTextLabel': {
    'id': 'Kamus Teks Terjemahan',
    'en': 'Translated Text Dictionaries',
    'hi': 'Anudit Path Shabdakosh',
    'es': 'Diccionarios de Textos Traducidos',
    'ml': 'Translated Text Dictionaries'
},
'confirmNewLangID': {
    'id': 'Lanjutkan \"{}\" seabagai id bahasa yang tepat?',
    'en': 'Continue \"{}\" as a correct language id?',
    'hi': '\"{}\" Ko Sahi Bhasha ID Ke Roop Mein Jari Rakhein?',
    'es': '¿Continuar \"{}\" como un ID de idioma correcto?',
    'ml': '\"{}\" Sariyaya Bhasha ID Aayi Thudarunnu?'
},
'saveLangIsInPreview': {
    'id': 'Kamu tidak dapat menyimpan saat dalam mode pratinjau',
    'en': 'You can\'t saving while in preview mode',
    'hi': 'Aap Preview Mode Mein Hote Hue Save Nahi Kar Sakte',
    'es': 'No Puedes Guardar Mientras Estás en Modo Vista Previa',
    'ml': 'Nee Preview Modeil Save Cheyyan Kazhiyilla'
},
'addWarnBetraying': { # >> Add Betray Warn Type
    'id': 'Berkhianat',
    'en': 'Betraying',
    'hi': 'Dhokha Dena',
    'es': 'Traicionar',
    'ml': 'Betraying'
},
'addWarnAbusing': {
    'id': 'Bicara Kasar',
    'en': 'Abusing',
    'hi': 'Gali Dena',
    'es': 'Abusar',
    'ml': 'Abusing'
},
'addWarnUnnecessaryVotes': {
    'id': 'Voting Tidak Perlu',
    'en': 'Unnecessary Votes',
    'hi': 'Avashyak Vote',
    'es': 'Votos Innecesarios',
    'ml': 'Avashyamaya Votes'
},
'addWarnTeaming': {
    'id': 'Kerjasama',
    'en': 'Teaming',
    'hi': 'Mil Kar Khelna',
    'es': 'Formar Equipo',
    'ml': 'Teaming'
},
'addWarnIsMaster': {
    'id': 'Kamu tidak bisa memberikan peringatan pada dirimu sendiri',
    'en': 'You can\'t warn yourself',
    'hi': 'Aap apne aap ko warn nahi kar sakte',
    'es': 'No puedes advertirte a ti mismo',
    'ml': 'Nee tanne warn cheyyan kazhiyilla'
},
'addWarnNotInGame': {
    'id': 'Peringatan ditambah (Tidak dalam permainan)',
    'en': 'Warn increased (Not in-game)',
    'hi': 'Warn Badhaya (Khel Mein Nahi)',
    'es': 'Advertencia aumentada (No en el juego)',
    'ml': 'Warn Kooduthal (Gameil Illa)'
},
'popupPlayerListWindowOpened': {
    'id': 'Jendela daftar pemain dibuka',
    'en': 'Player List Window Opened',
    'hi': 'Khiladi Suchi Ki Khidki Khuli',
    'es': 'Ventana de Lista de Jugadores Abierta',
    'ml': 'Player List Window Thurannu'
},
'popupPlayerListWindowOpenedSearching': {
    'id': 'Jendela daftar pemain dibuka, (+Pencarian)...',
    'en': 'Player List Window Opened, (+Searching)...',
    'hi': 'Khiladi Suchi Ki Khidki Khuli, (+Khoj)...',
    'es': 'Ventana de Lista de Jugadores Abierta, (+Buscando)...',
    'ml': 'Player List Window Thurannu, (+Searching)...'
},
'popupPlayerListWindowSearchingNotFound': {
    'id': 'Tidak ada kecocokan yang ditemukan untuk \"{}\"',
    'en': 'No Match Found For \"{}\"',
    'hi': '\"{}\" Ke Liye Koi Milaan Nahi Mila',
    'es': 'No se Encontró Coincidencia para \"{}\"',
    'ml': '\"{}\" Kku Match Kittiyilla'
},
'partyWindow.emptyText': {
    'id': 'Acaramu Kosong',
    'en': 'Your Party Is Empty',
    'hi': 'Aapki Party Khali Hai',
    'es': 'Tu Fiesta Está Vacía',
    'ml': 'Ninte Party Khali Aan'
},
'partyWindow.chatMutedText': {
    'id': 'Pesan Dibisukan',
    'en': 'Chat Muted',
    'hi': 'Chat Bisu',
    'es': 'Chat Silenciado',
    'ml': 'Chat Mute Cheythu'
},
'partyWindow.titleText': {
    'id': 'Pwesta Kamw',
    'en': 'Your Pawri',
    'hi': 'Aapki Pawri',
    'es': 'Tu Fiesta',
    'ml': 'Ninte Pawri'
},
'partyWindow.hostText': {
    'id': 'Tuan',
    'en': 'Host',
    'hi': 'Mezabaan',
    'es': 'Anfitrión',
    'ml': 'Host'
},
'cantMatchInPlayerData': {
    'id': 'Tidak dapat menyocokkan \"{}\" di data pemain',
    'en': 'Can\'t match \"{}\" in player data',
    'hi': 'Khiladi Data Mein \"{}\" Ka Milaan Nahi Kar Sakte',
    'es': 'No se Puede Coincidir \"{}\" en los Datos del Jugador',
    'ml': 'Player Datail \"{}\" Match Cheyyan Kazhiyilla'
},
'cantFindInPlayerData': {
    'id': 'Tidak dapat mencari \"{}\" di data pemain',
    'en': 'Can\'t find \"{}\" in player data',
    'hi': 'Khiladi Data Mein \"{}\" Nahi Mil Sakte',
    'es': 'No se Puede Encontrar \"{}\" en los Datos del Jugador',
    'ml': 'Player Datail \"{}\" Kittiyilla'
},
'addSuccess': {
    'id': 'Berhasil Ditambah',
    'en': 'Succesfully Added',
    'hi': 'Safalta Se Joda Gaya',
    'es': 'Agregado Exitosamente',
    'ml': 'Vijayapoorvam Add Cheythu'
},
'editSuccess': {
    'id': 'Teks Berhasil Diedit',
    'en': 'Text Succesfully Edited',
    'hi': 'Path Safalta Se Edit Kiya Gaya',
    'es': 'Texto Editado Exitosamente',
    'ml': 'Text Vijayapoorvam Edit Cheythu'
},
'editExist': {
    'id': 'Teks Editan Sudah Ada',
    'en': 'Text Edited Already Exist',
    'hi': 'Path Edit Kiya Hua Pehle Se Maujood Hai',
    'es': 'El Texto Editado Ya Existe',
    'ml': 'Edit Cheytha Text Already Exist'
},
'removeSuccess': {
    'id': 'Teks Berhasil Dihapus',
    'en': 'Text Succesfully Removed',
    'hi': 'Path Safalta Se Hataya Gaya',
    'es': 'Texto Eliminado Exitosamente',
    'ml': 'Text Vijayapoorvam Remove Cheythu'
},
'save': {
    'id': 'Simpan',
    'en': 'Save',
    'hi': 'Save Karein',
    'es': 'Guardar',
    'ml': 'Save Cheyyuka'
},
'use': {
    'id': 'Gunakan',
    'en': 'Use',
    'hi': 'Upyog Karein',
    'es': 'Usar',
    'ml': 'Upayogikkuka'
},
'copy': {
    'id': 'Salin',
    'en': 'Copy',
    'hi': 'Copy Karein',
    'es': 'Copiar',
    'ml': 'Copy Cheyyuka'
},
'textCopied': {
    'id': '\"{}\" Disalin',
    'en': '\"{}\" Copied',
    'hi': '\"{}\" Copy Kiya Gaya',
    'es': '\"{}\" Copiado',
    'ml': '\"{}\" Copy Cheythu'
},
'get': {
    'id': 'Dapatkan',
    'en': 'Get',
    'hi': 'Prapt Karein',
    'es': 'Obtener',
    'ml': 'Kittuka'
},
'enabled': {
    'id': 'Dinyalakan',
    'en': 'Enabled',
    'hi': 'Sakriya',
    'es': 'Habilitado',
    'ml': 'Enabled'
},
'disabled': {
    'id': 'Dimatikan',
    'en': 'Disabled',
    'hi': 'Nishkriya',
    'es': 'Deshabilitado',
    'ml': 'Disabled'
},
'confirmCopy': {
    'id': 'Salin Teks Ini',
    'en': 'Copy This Text', 
    'hi': 'Is Path Ko Copy Karein',
    'es': 'Copiar Este Texto',
    'ml': 'Itha Text Copy Cheyyuka'
},
'chatViewProfile': {
    'id': 'Profil Pemain Lengkap',
    'en': 'Players Full Profile',
    'hi': 'Players ka Pura Profile',
    'es': 'Perfil Completo del Jugador',
    'ml': 'Playersinte Purna Profile'
},
'chatViewAccount': {
    'id': 'Nama Akun Pemain',
    'en': 'Players Account Name',
    'hi': 'Players ka Account Naam',
    'es': 'Nombre de Cuenta del Jugador',
    'ml': 'Playersinte Account Peru'
},
'chatViewMulti': {
    'id': 'Akun & Profil Pemain',
    'en': 'Players Account & Profile',
    'hi': 'Players ka Account aur Profile',
    'es': 'Cuenta y Perfil del Jugador',
    'ml': 'Playersinte Accountum Profileum'
},
'chatViewMultiV2': {
    'id': 'Akun & Profil Pemain V.2',
    'en': 'Players Account & Profile V.2',
    'hi': 'Players ka Account aur Profile V.2',
    'es': 'Cuenta y Perfil del Jugador V.2',
    'ml': 'Playersinte Accountum Profileum V.2'
},
'chatShowCid': {
    'id': 'Tampilkan ClientID Pemain',
    'en': 'View Players\' ClientID',
    'hi': 'Players ka ClientID Dekhein',
    'es': 'Ver ClientID del Jugador',
    'ml': 'Playersinte ClientID Kaanuka'
},
'chatHideCid': {
    'id': 'Sembunyikan ClientID Pemain',
    'en': 'Hide Players\' ClientID',
    'hi': 'Players ka ClientID Chhupao',
    'es': 'Ocultar ClientID del Jugador',
    'ml': 'Playersinte ClientID Marachuka'
},
'chatViewOff': {
    'id': 'Matikan Penampil Nama Chat',
    'en': 'Turn Off Chat Name Viewer',
    'hi': 'Chat Name Viewer Band Karo',
    'es': 'Apagar Visor de Nombres del Chat',
    'ml': 'Chat Name Viewer Off Akkuka'
},
'backupAllNamesStart': { ####
    'id': 'Memulai pencadangan semua data nama',
    'en': 'Backing up all names data',
    'hi': 'Saare naam ke data ka backup liya ja raha hai',
    'es': 'Haciendo copia de seguridad de todos los datos de nombres',
    'ml': 'Ella perukalude data backup edukkunnu'
},
'backupAllNamesSuccess': {
    'id': 'Semua data nama berhasil dicadangkan',
    'en': 'All names data backed up successfully',
    'hi': 'Saare naam ke data ka backup safal hua',
    'es': 'Todos los datos de nombres respaldados exitosamente',
    'ml': 'Ella perukalude data vijayathode backup cheythu'
},
'backupAllNamesFailed': {
    'id': 'Gagal mencadangkan semua data nama',
    'en': 'Error backing up all names data',
    'hi': 'saare naam ke data ka backup mein galti hui',
    'es': 'Error al hacer copia de seguridad de todos los datos de nombres',
    'ml': 'Ella perukalude data backup cheyyumbol thappu undayi'
},
'copyText': { ##################################################################
    'id': 'Salin teks',
    'en': 'Copy text',
    'hi': 'Text copy karein',
    'es': 'Copiar texto',
    'ml': 'Text copy cheyyu'
},
'translateText': {
    'id': 'Terjemahkan teks',
    'en': 'Translate text',
    'hi': 'Text translate karein',
    'es': 'Traducir texto',
    'ml': 'Text translate cheyyu'
},
'insertText': {
    'id': 'Masukkan teks',
    'en': 'Insert text',
    'hi': 'Text insert karein',
    'es': 'Insertar texto',
    'ml': 'Text insert cheyyu'
},
'playerMenuOptionFromText': {
    'id': 'Opsi player',
    'en': 'Player option',
    'hi': 'Player option',
    'es': 'Opción de jugador',
    'ml': 'Player option'
},
'editablePopUpInvalidDataType': {
    'id': 'Tipe data tidak valid',
    'en': 'Data type is not valid',
    'hi': 'Data ka prakar valid nahi hai',
    'es': 'El tipo de datos no es válido',
    'ml': 'Data type valid alla'
},
'editablePopUpInvalidSaveFuncList': { # >>
    'id': 'Oops, Fungsi Penyimpan List Tidak Valid',
    'en': 'Uh Oh, Invalid List Saving Function',
    'hi': 'Oops, List save function valid nahi hai',
    'es': 'Ups, Función de guardado de lista no válida',
    'ml': 'Oops, List save function valid alla'
},
'editablePopUpInvalidSaveFuncDict': {
    'id': 'Oops, Fungsi Penyimpan Dict Tidak Valid',
    'en': 'Uh Oh, Invalid Dict Saving Function',
    'hi': 'Oops, Dict save function valid nahi hai',
    'es': 'Ups, Función de guardado de diccionario no válida',
    'ml': 'Oops, Dict save function valid alla'
},
'bcsObtainedAccountIdentity': {
    'id': 'Identitas',
    'en': 'Identity',
    'hi': 'Identity',
    'es': 'Identidad',
    'ml': 'Identity'
},
'bcsObtainedOtherAcc': {
    'id': 'Akun Lain',
    'en': 'Other Accounts',
    'hi': 'Other Accounts',
    'es': 'Otras cuentas',
    'ml': 'Other Accounts'
},
'bcsObtainedUpgradedName': {
    'id': 'Nama Terupgrade',
    'en': 'Upgraded Name',
    'hi': 'Upgraded Name',
    'es': 'Nombre mejorado',
    'ml': 'Upgraded Name'
},
'bcsObtainedOtherUpgradedName': {
    'id': 'Nama Terupgrade Lain',
    'en': 'Other Upgraded Names',
    'hi': 'Other Upgraded Names',
    'es': 'Otros nombres mejorados',
    'ml': 'Other Upgraded Names'
},
'bcsObtainedAccountDatesKEY': {
    'id': 'Akun Dibuat Pada',
    'en': 'Account Dates',
    'hi': 'Account Dates',
    'es': 'Fechas de la cuenta',
    'ml': 'Account Dates'
},
'bcsObtainedCretedOn': {
    'id': 'Dibuat Pada',
    'en': 'Created On',
    'hi': 'Created On',
    'es': 'Creado el',
    'ml': 'Created On'
},
'bcsObtainedUpdatedOn': {
    'id': 'Diperbaharui Pada',
    'en': 'Updated On',
    'hi': 'Updated On',
    'es': 'Actualizado el',
    'ml': 'Updated On'
},
'bcsObtainedConnectedDiscordKEY': {
    'id': 'Akun Discord Terkoneksi Pada Pemain',
    'en': 'Player\'s Connected Discord',
    'hi': 'Player\'s Connected Discord',
    'es': 'Discord conectado del jugador',
    'ml': 'Player\'s Connected Discord'
},
'bcsObtainedConnectedDiscordId': { # Unused
    'id': 'ID-DC',
    'en': 'DC-ID',
    'hi': 'DC-ID',
    'es': 'ID-DC',
    'ml': 'DC-ID'
},
'bcsObtainedConnectedDiscordUsername': {
    'id': 'Nama pengguna',
    'en': 'Username',
    'hi': 'Yuzar naam',
    'es': 'Nombre de usuario',
    'ml': 'Yuzar peru'
},
'bcsObtainedConnectedDiscordUniqueId': {
    'id': 'ID Unik',
    'en': 'Unique ID',
    'hi': 'Anokha ID',
    'es': 'ID único',
    'ml': 'Vyakti ID'
},
'bcsObtainedSpaz': {
    'id': 'Spaz-nya Si Pemain',
    'en': 'Player\'s Spaz',
    'hi': 'Kheladi ka Spaz',
    'es': 'Spaz del jugador',
    'ml': 'Khelaadiyude Spaz'
},
'bcsObtainedMutualServer': {
    'id': 'Ketemuan Di Server',
    'en': 'Mutual Servers',
    'hi': 'Sajha server',
    'es': 'Servidores mutuos',
    'ml': 'Sahadharmi server'
},
'errorAfterGetDataFromBCS': {
    'id': 'Error \"Setelah\" Mendapatkan Data Pemain Dari BCS',
    'en': 'Error \"After\" Obtaining Player Data From BCS',
    'hi': 'BCS se kheladi data prapt karne ke baad error',
    'es': 'Error \"Después\" de obtener datos del jugador de BCS',
    'ml': 'BCS-il ninnu khelaadi data kittiyappol error'
},
'confirmChangesFromBCS': {
    'id': 'Apakah Anda Ingin Menyimpan Perubahan Untuk Pemain Ini?',
    'en': 'Do You Want To Save Changes For Player',
    'hi': 'Kya aap kheladi ke liye parivartan save karna chahte hain?',
    'es': '¿Quieres guardar los cambios para el jugador?',
    'ml': 'Khelaadiyude maatpravarttanangal save cheyyaamo?'
},
'errorWhileGetDataFromBCS': {
    'id': 'Error Saat Mendapatkan Data Pemain',
    'en': 'Error On Getting Player Data',
    'hi': 'Kheladi data prapt karne mein error',
    'es': 'Error al obtener datos del jugador',
    'ml': 'Khelaadi data kittiyappol error'
},
'bcsGettingPlayerData': { # >> Get Data From BCS
    'id': 'Mendapatkan Data Pemain {0} Dari BCS',
    'en': 'Getting Player {0}\'s Data From BCS',
    'hi': 'BCS se kheladi {0} ka data prapt kiya ja raha hai',
    'es': 'Obteniendo datos del jugador {0} de BCS',
    'ml': 'BCS-il ninnu khelaadi {0}\'nte data kittunnu'
},
'bcsFetchError': {
    'id': 'Error Mendapatkan Data {0} Dari Server BCS',
    'en': 'Error Getting {0}\'s Data From BCS Server',
    'hi': 'BCS server se {0} ka data prapt karne mein error',
    'es': 'Error al obtener datos de {0} del servidor BCS',
    'ml': 'BCS server-il ninnu {0}\'nte data kittiyappol error'
},
'bcsFetchStillFetching': {
    'id': 'Data pemain {0} sedang dicari, tunggu sebentar',
    'en': 'Player {0}\'s Data still searched, please wait',
    'hi': 'Kheladi {0} ka data abhi bhi khoja ja raha hai, kripya prateeksha karein',
    'es': 'Los datos del jugador {0} aún se están buscando, por favor espere',
    'ml': 'Khelaadi {0}\'nte data ippozhum shodhikkunnu, kshamikkuka'
},
'bcsFetchFailedConnect': {
    'id': 'Tidak Dapat Terhubung Ke Server BCS Untuk Pemain {0}',
    'en': 'Can\'t Connect To BCS Server For Player {0}',
    'hi': 'Kheladi {0} ke liye BCS server se jod nahi ho paya',
    'es': 'No se puede conectar al servidor BCS para el jugador {0}',
    'ml': 'Khelaadi {0}\'nte BCS server-ilekku connect cheyyan kazhiyunnilla'
},
'bcsFetchNotFound': {
    'id': 'Tidak Dapat Menemukan Data {0} Dari Server BCS',
    'en': 'Can\'t Find {0}\'s Data From BCS Server',
    'hi': 'BCS server se {0} ka data nahi mila',
    'es': 'No se pueden encontrar los datos de {0} del servidor BCS',
    'ml': 'BCS server-il ninnu {0}\'nte data kandilla'
},
'bcsOnSearchTryEmpty': {
    'id': 'PB-ID Tidak Tersedia...\nAmbil Data {} Dari BCS?\n(Mungkin Butuh Waktu)',
    'en': 'PB-ID Is Not Available...\nGet {}\'s Data From BCS?\n(Might Take A While)',
    'hi': 'PB-ID uplabdh nahi hai...\nBCS se {} ka data prapt karein?\n(samay lagega)',
    'es': 'PB-ID no está disponible...\n¿Obtener datos de {} de BCS?\n(Podría tomar un tiempo)',
    'ml': 'PB-ID kittunilla...\nBCS-il ninnu {}\'nte data edukkamo?\n(samayam edukkum)'
},
'bcsOnSearchTryOnlyPb': {
    'id': 'PB-ID Tersedia Dari Sumber Lain\nAmbil Data Lain {} Dari BCS?\n(Mungkin Butuh Waktu)',
    'en': 'PB-ID Is Available From Other Source\nGet {}\'s Other Data From BCS?\n(Might Take A While)',
    'hi': 'PB-ID anya srot se uplabdh hai\nBCS se {} ka anya data prapt karein?\n(samay lagega)',
    'es': 'PB-ID está disponible desde otra fuente\n¿Obtener otros datos de {} de BCS?\n(Podría tomar un tiempo)',
    'ml': 'PB-ID vere oru sthaanatthil ninnu kittiyirikkunnu\nBCS-il ninnu {}\'nte vere data edukkamo?\n(samayam edukkum)'
},
'bcsOnSearchTryNoPbNoBcs': {
    'id': 'PB-ID Tidak Tersedia...\nDan Data {} Tidak Ditemukan Di BCS\nApakah Anda Ingin Mencari Data Lagi?',
    'en': 'PB-ID Is Not Available...\nAnd {}\'s Data Not Found In BCS\nDo You Wanna Research The Data?',
    'hi': 'PB-ID uplabdh nahi hai...\nAur {} ka data BCS mein nahi mila\nkya aap data phir se khojna chahte hain?',
    'es': 'PB-ID no está disponible...\nY los datos de {} no se encontraron en BCS\n¿Quieres investigar los datos de nuevo?',
    'ml': 'PB-ID kittunilla...\nBCS-il {}\'nte data kandilla\ndata mattoru pravisham shodhikkamo?'
},
'bcsOnSearchTryNoBcs': {
    'id': 'PB-ID Tersedia: {pb_id}\nTapi Data {name} Tidak Ditemukan Di BCS\nApakah Anda Ingin Mencari Data Lagi?',
    'en': 'PB-ID Available: {pb_id}\nBut {name}\'s Data Not Found In BCS\nDo You Wanna Research The Data',
    'hi': 'PB-ID uplabdh: {pb_id}\nLekin {name} ka data BCS mein nahi mila\nkya aap data phir se khojna chahte hain?',
    'es': 'PB-ID disponible: {pb_id}\nPero los datos de {name} no se encontraron en BCS\n¿Quieres investigar los datos de nuevo?',
    'ml': 'PB-ID kittiyirikkunnu: {pb_id}\nPakshe BCS-il {name}\'nte data kandilla\ndata mattoru pravisham shodhikkamo?'
},
'bcsOnSearchTryFull': {
    'id': 'PB-ID Dan Data Dari BCS Sudah Diperoleh:\nPB-ID Sekarang: {pb_id}\nAmbil Data {name} Dari BCS Lagi',
    'en': 'PB-ID And Data From BCS Already Obtained:\nCurrent PB-ID: {pb_id}\nGet {name}\'s Data From BCS Again',
    'hi': 'PB-ID aur BCS se data pehle hi prapt ho chuka hai:\nvartamaan PB-ID: {pb_id}\nBCS se {name} ka data phir se prapt karein',
    'es': 'PB-ID y datos de BCS ya obtenidos:\nPB-ID actual: {pb_id}\nObtener datos de {name} de BCS nuevamente',
    'ml': 'PB-IDum BCS-il ninnulla datayum kitti:\nCurrent PB-ID: {pb_id}\nBCS-il ninnu {name}\'nte data mattoru pravisham edukkuka'
},
'bcsOnSearchTryUnknown': {
    'id': 'Format Teks Tidak Dikenal Untuk Data {name}\nStatus PB-ID: {pb_id}\nStatus Pencarian: {other}',
    'en': 'Unknown Text Format For {name}\'s Data\nPB-ID Status: {pb_id}\nSearched Status: {other}',
    'hi': '{name} ke data ke liye anjaan text format\nPB-ID status: {pb_id}\nSearch status: {other}',
    'es': 'Formato de texto desconocido para los datos de {name}\nEstado de PB-ID: {pb_id}\nEstado de búsqueda: {other}',
    'ml': '{name}\'nte datayude anjaan text format\nPB-ID status: {pb_id}\nSearch status: {other}'
},
'bcsPbPriority': {
    'id': 'Prioritaskan PB-ID BCS',
    'en': 'Prioritize BCS PB-ID',
    'hi': 'BCS PB-ID ko prathamikta do',
    'es': 'Priorizar PB-ID de BCS',
    'ml': 'BCS PB-IDkk priority kodukkuka'
},
'settingsWindow.accountText': {
    'id': 'Akun',
    'en': 'Account',
    'hi': 'Khaata',
    'es': 'Cuenta',
    'ml': 'Account'
},
'saveReplayTitle': {
    'id': 'Simpan Rekaman Permainan Terakhir',
    'en': 'Save Last Game Replay',
    'hi': 'Pichhla game replay save karo',
    'es': 'Guardar la última repetición del juego',
    'ml': 'Kazhinja game replay save cheyyuka'
},
'saveReplayConfirmReplaceWithDefault': {
    'id': 'Yakin menggunakan nama rekaman default',
    'en': 'Confirm to use default replay name',
    'hi': 'Default replay naam istemal karne ki pusti karein',
    'es': 'Confirmar usar el nombre de repetición predeterminado',
    'ml': 'Default replay peru upayogikkunnathinu sthirappikkuka'
},
'saveReplayEnter': {
    'id': 'Simpan Rekaman Game',
    'en': 'Save Game Replay',
    'hi': 'Game replay save karo',
    'es': 'Guardar repetición del juego',
    'ml': 'Game replay save cheyyuka'
},
'saveReplayEmptyName': {
    'id': 'Nama rekaman permainan tidak bisa kosong',
    'en': 'Game replay name can\'t be empty',
    'hi': 'Game replay ka naam khali nahi ho sakta',
    'es': 'El nombre de la repetición del juego no puede estar vacío',
    'ml': 'Game replaynte peru khaliyakkam pattilla'
},
'saveReplayNoLastReplay': {
    'id': 'Rekaman permainan terkahir tidak ditemukan',
    'en': 'Last game replay file not found',
    'hi': 'Pichhla game replay file nahi mili',
    'es': 'Archivo de la última repetición del juego no encontrado',
    'ml': 'Kazhinja game replay file kandilla'
},
'saveReplaySaved': {
    'id': 'Rekaman game \"{}\" berhasil disimpan',
    'en': 'Game replay \"{}\" succesfully saved',
    'hi': 'Game replay \"{}\\" safalta se save ho gaya',
    'es': 'Repetición del juego \"{}\" guardada con éxito',
    'ml': 'Game replay \"{}\" vijayathode save cheythu'
},
'saveReplayError': {
    'id': 'Gagal menyimpan rekaman permainan',
    'en': 'Failed to save game replay',
    'hi': 'Game replay save karne mein asafal',
    'es': 'Error al guardar la repetición del juego',
    'ml': 'Game replay save cheyyan kazhiyilla'
},
'saveReplayInfoDate': {
    'id': '{} = Tanggal sekarang',
    'en': '{} = Current date',
    'hi': '{} = Vartamaan taareekh',
    'es': '{} = Fecha actual',
    'ml': '{} = Current date'
},
'saveReplayInfoTime': {
    'id': '{} = Waktu sekarang',
    'en': '{} = Current time',
    'hi': '{} = Vartamaan samay',
    'es': '{} = Hora actual',
    'ml': '{} = Current time'
},
'saveReplayOverwriteConfirm': {
    'id': 'Rekaman dengan nama ini sudah ada, timpa?',
    'en': 'The replay with this name already exist, overwrite?',
    'hi': 'Is naam ka replay pehle se maujood hai, overwrite karein?',
    'es': 'La repetición con este nombre ya existe, ¿sobrescribir?',
    'ml': 'Itha perulla replay munp undu, overwrite cheyyamo?'
},
'saveReplayConfirmExit': {
    'id': 'Yakin keluar tanpa menyimpan?',
    'en': 'Are you sure exit without saving?',
    'hi': 'Kya aap save kiye bina bahar jaane ke liye pakka hain?',
    'es': '¿Estás seguro de salir sin guardar?',
    'ml': 'Save cheyyathe purathu pokan nishchayikkunnundo?'
},
'savePlayerDataHappyMsg1': {
    'id': 'Wow, Kamu Telah Mengumpulkan {} Nama Pemain! Teruskan xD',
    'en': 'Wow, You Have Collected {} Player Names! Keep it Up xD',
    'hi': 'Wow, aapne {} player ke naam ikatthe kiye hain! Jaari rakho xD',
    'es': '¡Guau, has recopilado {} nombres de jugadores! Sigue así xD',
    'ml': 'Wow, ningal {} playernte perukal collect cheythu! Thudarum xD'
},
'savePlayerDataHappyMsg2': {
    'id': 'Daymm, Kamu Mengumpulkan {} Nama Pemain! Less Senang xD',
    'en': 'Daymm, You Collected {} Player Names! Less is Happy xD',
    'hi': 'Daymm, aapne {} player ke naam ikatthe kiye hain! Less khush hai xD',
    'es': '¡Vaya, has recopilado {} nombres de jugadores! Less está feliz xD',
    'ml': 'Daymm, ningal {} playernte perukal collect cheythu! Less santhoshappettu xD'
},
'savePlayerDataHappyMsg3': {
    'id': 'Kamu Mengumpulkan {} Nama Pemain, Luar Biasa! Kamu Pasti OG🙀',
    'en': 'You Collected {} Player Names, Amazing! You Sure An OG🙀',
    'hi': 'Aapne {} player ke naam ikatthe kiye, shandaar! Aap pakka OG hain🙀',
    'es': '¡Has recopilado {} nombres de jugadores, increíble! Definitivamente eres un OG🙀',
    'ml': 'Ningal {} playernte perukal collect cheythu, adbhutam! Ningal sure an OG🙀'
},
'savePlayerDataHappyMsg4': {
    'id': '{} Nama Pemain? Sentuh Rumput Bruh😭',
    'en': '{} Player Names? Touch Some Grass Bruh😭',
    'hi': '{} Player ke naam? Thoda ghaas chho lo bhai😭',
    'es': '¿{} Nombres de jugadores? Toca un poco de hierba, hermano😭',
    'ml': '{} Playernte perukal? Kurachu pul thodukku da😭'
},
'translateFailed': {
    'id': 'Tidak Dapat Terhubung Ke Google Translate / Tidak Ada Koneksi Internet',
    'en': 'Can\'t Connect To Google Translate / No Internet Connection',
    'hi': 'Google Translate se jod nahi ho paya / Internet connection nahi hai',
    'es': 'No se puede conectar a Google Translate / Sin conexión a Internet',
    'ml': 'Google Translate-ilekku connect cheyyan kazhiyilla / Internet connection illa'
},
'serverDisconnected': {
    'id': 'Ujung jarak jauh menutup koneksi tanpa respons',
    'en': 'Remote end closed connection without response',
    'hi': 'Door ka anty bina jawab ke jod tod diya',
    'es': 'El extremo remoto cerró la conexión sin respuesta',
    'ml': 'Dooravarti mukham bina uttaram bandham murichu'
},
'translateSameSrcDest': {
    'id': 'Sumber ({}) dan Tujuan ({}) Bahasa Sama',
    'en': 'Same Source ({}) And Destination ({}) Lang',
    'hi': 'Sam strot ({}) aur lakshya ({}) bhasha',
    'es': 'Mismo Origen ({}) y Destino ({}) Idioma',
    'ml': 'Samam sthaanam ({}) athra lakshyam ({}) bhasha'
},
'translateEmptyText': {
    'id': 'Ngga ada teks buat diterjemah',
    'en': 'Nothing to translate',
    'hi': 'Anuvad ke liye kuch nahi',
    'es': 'Nada que traducir',
    'ml': 'Anuvadakkaayi onnumilla'
},
'translateSameResult': {
    'id': 'Hasil terjemahan sama',
    'en': 'Translation results are the same',
    'hi': 'Anuvad ke nateeje saman hain',
    'es': 'Los resultados de la traducción son iguales',
    'ml': 'Anuvadattinte parinamam samanamanu'
},
'noResponderData': {
    'id': 'Tidak Ada Data Untuk Diambil Saat Ini',
    'en': 'No Data To Get Right Now',
    'hi': 'Abhi lene ke liye koi data nahi',
    'es': 'No hay datos para obtener ahora mismo',
    'ml': 'Ippol edukkaan data illa'
},
'findPlayerCmdShortArgument': {
    'id': 'Berikan setidaknya {} karakter untuk mencari',
    'en': 'Please provide at least {} characters to search',
    'hi': 'Khojne ke liye kam se kam {} akshar dijiye',
    'es': 'Por favor proporcione al menos {} caracteres para buscar',
    'ml': 'Thediyaan kurachu {} aksharam kodukku'
},
'findPlayerCmdFailed': {
    'id': 'Gagal Mencari',
    'en': 'Failed Finding',
    'hi': 'Khojne mein asaphal',
    'es': 'Búsqueda fallida',
    'ml': 'Thediyaan thottilla'
},
'findPlayerCmdNotFound': {
    'id': 'Tidak Ada Kecocokan Untuk \"{}\"',
    'en': 'No Match Found For \"{}\"',
    'hi': '\"{}\" ke liye koi mil nahi',
    'es': 'No se encontró coincidencia para \"{}\"',
    'ml': '\"{}\" inu ottum kittiyilla'
},
'findPlayerIncludeProfileEnable': {
    'id': 'Sertakan Pencocokan Dengan Profil Diaktifkan',
    'en': 'Include Matching With Profile Enabled',
    'hi': 'sakriya profile ke saath milan shamil karein',
    'es': 'Incluir coincidencia con perfil habilitado',
    'ml': 'Nakriya profile-umayi ottu cherkkuka'
},
'findPlayerIncludeProfileDisable': {
    'id': 'Sertakan Pencocokan Dengan Profil Dinonaktifkan',
    'en': 'Include Matching With Profile Disabled',
    'hi': 'Nishkriya profile ke saath milan shamil karein',
    'es': 'Incluir coincidencia con perfil deshabilitado',
    'ml': 'Nishkriya profile-umayi ottu cherkkuka'
},
'nickAlreadyExist': {
    'id': 'Nickname Sudah Ada',
    'en': 'Nick already exists',
    'hi': 'Nick pehle se maujood hai',
    'es': 'El apodo ya existe',
    'ml': 'Nick munpu undayirunnu'
},
'nickAdded': {
    'id': 'Nickname Ditambahkan',
    'en': 'Nick added',
    'hi': 'Nick jod diya gaya',
    'es': 'Apodo añadido',
    'ml': 'Nick cherthu'
},
'nickRemoved': {
    'id': 'Nickname Dihapus',
    'en': 'Nick removed',
    'hi': 'Nick hata diya gaya',
    'es': 'Apodo eliminado',
    'ml': 'Nick maatti'
},
'nickNotFound': {
    'id': 'Nickname Tidak Ditemukan',
    'en': 'Nick not found',
    'hi': 'Nick nahi mila',
    'es': 'Apodo no encontrado',
    'ml': 'Nick kittiyilla'
},
'responderBlacklistInvalidName': {
    'id': 'Nama Blacklist Tidak Valid',
    'en': 'Invalid Blacklist Names',
    'hi': 'Amany blacklist naam',
    'es': 'Nombres de lista negra no válidos',
    'ml': 'Amanya blacklist perukal'
},
'responderBlacklistAdded': {
    'id': 'Akun Ditambahkan Ke Blacklist',
    'en': 'Acc(s) added to the blacklist',
    'hi': 'Khaate blacklist mein jod diye gaye',
    'es': 'Cuenta(s) añadida(s) a la lista negra',
    'ml': 'Blacklist-il account(s) cherthu'
},
'responderMutedInvalidName': {
    'id': 'Nama Mute Tidak Valid',
    'en': 'Invalid Muted Names',
    'hi': 'Amany mute naam',
    'es': 'Nombres silenciados no válidos',
    'ml': 'Amanya mute perukal'
},
'responderMutedAdded': {
    'id': 'Akun Ditambahkan Ke Daftar Mute',
    'en': 'Acc(s) added to the muted list',
    'hi': 'Khaate mute list mein jod diye gaye',
    'es': 'Cuenta(s) añadida(s) a la lista de silenciados',
    'ml': 'Mute list-il account(s) cherthu'
},
'quickRespondButton': {
    'id': 'Cepat',
    'en': 'Quick',
    'hi': 'Tez',
    'es': 'Rápido',
    'ml': 'Vegam'
},
'psNewUserOpenTranslatedDict': {
    'id': 'Plugin masih baru! Tunggu {} hari lagi untuk membuka ini',
    'en': 'Plugin is still new! Wait {} more day(s) to open this',
    'hi': 'Plugin abhi naya hai! ise kholne ke liye {} aur din intezar karein',
    'es': '¡El plugin aún es nuevo! Espera {} día(s) más para abrir esto',
    'ml': 'Plugin innum putiya aanu! ith thurakkan {} divasam koodi kathirikkuka'
},
'psNewUserOpenTranslatedDictInvalidDate': {
    'id': 'Format tanggal terakhir penggunaan tidak valid',
    'en': 'Last usage date format is invalid',
    'hi': 'Antim upyog ki tarikh ka format amanya hai',
    'es': 'El formato de la fecha del último uso no es válido',
    'ml': 'Kadha upayogicha divasamaya format amanya aanu'
},
'psMainLanguage': {
    'id': 'Bahasa Utama {}',
    'en': '{} Main Language',
    'hi': '{} mukhya bhasha',
    'es': '{} Idioma Principal',
    'ml': '{} mukhya bhasha'
},
'psMainLanguageChanged': {
    'id': 'Bahasa utama JendelaParty sekarang adalah {}',
    'en': 'Current PartyWindow main Language is now {}',
    'hi': 'PartyWindow ki mukhya Bhasha ab {} hai',
    'es': 'El idioma principal de PartyWindow ahora es {}',
    'ml': 'PartyWindow-in mukhya Bhasha ippol {} aanu'
},
'psMessageNotificationPosKey': {
    'id': 'Posisi Notifikasi Pesan',
    'en': 'Message Notification Position',
    'hi': 'Sandesh suchna sthaan',
    'es': 'Posición de Notificación de Mensaje',
    'ml': 'Sandhesha aavishkaar sthaanam'
},
'psMessageNotificationPosTOP': {
    'id': 'Atas',
    'en': 'Top',
    'hi': 'Upar',
    'es': 'Arriba',
    'ml': 'Mel'
},
'psMessageNotificationPosBOTTOM': {
    'id': 'Bawah',
    'en': 'Bottom',
    'hi': 'Neeche',
    'es': 'Abajo',
    'ml': 'Keezh'
},
'psBsUiScaleKey': {
    'id': 'Skala UI BombSquad',
    'en': 'BombSquad UI Scale',
    'hi': 'BombSquad UI praman',
    'es': 'Escala de UI de BombSquad',
    'ml': 'BombSquad UI pramaanam'
},
'psBsUiScaleSMALL': {
    'id': 'Kecil',
    'en': 'Small',
    'hi': 'Chhota',
    'es': 'Pequeño',
    'ml': 'Cheriya'
},
'psBsUiScaleMEDIUM': {
    'id': 'Sedang',
    'en': 'Medium',
    'hi': 'Madhyam',
    'es': 'Mediano',
    'ml': 'Madhyamam'
},
'psBsUiScaleLARGE': {
    'id': 'Besar',
    'en': 'Large',
    'hi': 'Bada',
    'es': 'Grande',
    'ml': 'Valiya'
},
'qnaRemoved': { # >> Server Questions
    'id': 'Pertanyaan dihapus',
    'en': 'Question removed',
    'hi': 'Sawal hata diya gaya',
    'es': 'Pregunta eliminada',
    'ml': 'Prashnam maatti'
},
'qnaNotFound': {
    'id': '\"{}\" tidak ada di data pertanyaan',
    'en': '\"{}\" not in questions list',
    'hi': '\"{}\" sawal ke list mein nahi hai',
    'es': '\"{}\" no está en la lista de preguntas',
    'ml': '\"{}\" prashna list-il illa'
},
'question': {
    'id': 'Pertanyaan',
    'en': 'Question',
    'hi': 'Sawal',
    'es': 'Pregunta',
    'ml': 'Prashnam'
},
'answer': {
    'id': 'Jawaban',
    'en': 'Answer',
    'hi': 'Uttar',
    'es': 'Respuesta',
    'ml': 'Uttaram'
},
'crAdded': { # >> Custom Replies
    'id': 'Trigger: [{}] Balasan: [{}] ditambahkan',
    'en': 'Trigger: [{}] Reply: [{}] added',
    'hi': 'Trigger: [{}] uttar: [{}] joda gaya',
    'es': 'Disparador: [{}] Respuesta: [{}] añadido',
    'ml': 'Trigger: [{}] uttaram: [{}] cherthu'
},
'crRemoved': {
    'id': 'Trigger dihapus',
    'en': 'Trigger removed',
    'hi': 'Trigger hata diya gaya',
    'es': 'Disparador eliminado',
    'ml': 'Trigger maatti'
},
'crNotFound': {
    'id': 'Trigger: \"{}\" tidak ditemukan di balasan kustom',
    'en': 'Trigger: \"{}\" not found in custom replies',
    'hi': 'Trigger: \"{}\" custom jawab mein nahi mila',
    'es': 'Disparador: \"{}\" no encontrado en respuestas personalizadas',
    'ml': 'Trigger: \"{}\" custom uttaram-il kandilla'
},
'invalidMaxMsgLen': {
    'id': 'MAX_MSG_LENGTH Tidak Valid: [{val}] | [{type}] >> Maks: 99 (integer)',
    'en': 'Invalid MAX_MSG_LENGTH: [{val}] | [{type}] >> Max: 99 (integer)',
    'hi': 'Galat MAX_MSG_LENGTH: [{val}] | [{type}] >> adhik se adhik: 99 (integer)',
    'es': 'MAX_MSG_LENGTH no válido: [{val}] | [{type}] >> Máx: 99 (entero)',
    'ml': 'Thavana MAX_MSG_LENGTH: [{val}] | [{type}] >> kooduthal: 99 (integer)'
},
'cfgBlockNaCmd': { # Config Text
    'id': '[{}] Tidak Ada Dalam Perintah',
    'en': '[{}] Is An Unknown Command Prefix',
    'hi': '[{}] anjaan command prefix hai',
    'es': '[{}] es un prefijo de comando desconocido',
    'ml': '[{}] anjaan command prefix aanu'
},
'playerOptionRemoveData': { # >> Player Info Option
    'id': 'Hapus Data {}',
    'en': 'Remove {} Data',
    'hi': '{} ka data hatao',
    'es': 'Eliminar datos de {}',
    'ml': '{}\'nte data maatti'
},
'playerOptionRemoveDataConfirm': {
    'id': 'Yakin hapus data {}',
    'en': 'Are you sure to delete {} Data',
    'hi': 'Kya aap {} ka data delete karna chahte hain',
    'es': '¿Estás seguro de eliminar los datos de {}?',
    'ml': '{}\'nte data maattan nishchayikkunnundo?'
},
'playerOptionRemoveDataInMasterList': {
    'id': 'Kamu tidak bisa menghapus data diri sendiri',
    'en': 'You can\'t delete your own data',
    'hi': 'Aap apna data delete nahi kar sakte',
    'es': 'No puedes eliminar tus propios datos',
    'ml': 'Ningalude data ningal maattan pattilla'
},
'playerOptionRemoveDataNotExist': {
    'id': 'Data pemain {} tidak ditemukan',
    'en': 'Player {} data not found',
    'hi': 'Kheladi {} ka data nahi mila',
    'es': 'Datos del jugador {} no encontrados',
    'ml': 'Khelaadi {}\'nte data kandilla'
},
'playerOptionRemoveFriend': {
    'id': 'Berhenti Berteman',
    'en': 'UnFriend',
    'hi': 'Dosti todna',
    'es': 'Dejar de ser amigos',
    'ml': 'Snehitam maatti'
},
'playerOptionRemoveFriendSuccess': {
    'id': 'Kalian Bukan Teman Lagi',
    'en': 'You Both Are No Longer Friends',
    'hi': 'Aap dono ab doston mein nahi hain',
    'es': 'Ya no son amigos',
    'ml': 'Ningal randu perum snehitamalla'
},
'playerOptionRemoveFriendInMasterList': {
    'id': 'Kamu Tidak Bisa Memutus Pertemanan Dengan Tuanku',
    'en': 'You Can\'t UnFriend My Master',
    'hi': 'Aap mere master se dosti nahi tod sakte',
    'es': 'No puedes dejar de ser amigo de mi maestro',
    'ml': 'Ningal enre master-ine snehitam maattan pattilla'
},
'playerOptionRemoveFriendNotExist': {
    'id': 'Teman Tidak Ada Di Data',
    'en': 'Friend Does Not Exist In Data',
    'hi': 'Dost data mein nahi hai',
    'es': 'El amigo no existe en los datos',
    'ml': 'Snehitan data-il illa'
},
'playerOptionAddFriend': { # >> playerOptionAddFriend
    'id': 'Berteman Dengan Pemain Ini',
    'en': 'BeFriend With This Player',
    'hi': 'Is kheladi se dosti karo',
    'es': 'Hazte amigo de este jugador',
    'ml': 'Ee khelaadiyude snehitam aakuka'
},
'playerOptionAddFriendSuccess': {
    'id': 'Kamu Berhasil Berteman Dengan Pemain Ini',
    'en': 'You Have Successfully Befriended This Player',
    'hi': 'Aapne is kheladi se safalta se dosti kar li',
    'es': 'Te has hecho amigo de este jugador con éxito',
    'ml': 'Ningal ee khelaadiyude snehitam vijayathode aakki'
},
'playerOptionAddFriendAlreadyExists': {
    'id': 'Pemain Ini Sudah Menjadi Teman Anda',
    'en': 'This Player Is Already Your Friend',
    'hi': 'Ye kheladi pehle se hi aapka dost hai',
    'es': 'Este jugador ya es tu amigo',
    'ml': 'Ee khelaadi ningalude snehitan thanne aanu'
},
'playerOptionRemoveBlacklist': { # >> playerOptionRemoveBlacklist
    'id': 'Hapus Pemain Ini Dari Daftar Hitam',
    'en': 'Remove This Player From Blacklist',
    'hi': 'Is kheladi ko blacklist se hatao',
    'es': 'Elimina a este jugador de la lista negra',
    'ml': 'Ee khelaadiye blacklist-il ninnu maatti'
},
'playerOptionRemoveBlacklistSuccess': {
    'id': 'Pemain Berhasil Dihapus Dari Daftar Hitam',
    'en': 'Player Successfully Removed From Blacklist',
    'hi': 'Kheladi ko safalta se blacklist se hata diya gaya',
    'es': 'Jugador eliminado con éxito de la lista negra',
    'ml': 'Khelaadi blacklist-il ninnu vijayathode maatti'
},
'playerOptionRemoveBlacklistNotExist': {
    'id': 'Pemain Ini Tidak Masuk Di Daftar Hitam',
    'en': 'This Player Is Not Blacklisted',
    'hi': 'Ye kheladi blacklist mein nahi hai',
    'es': 'Este jugador no está en la lista negra',
    'ml': 'Ee khelaadi blacklist-il illa'
},
'playerOptionAddBlacklist': { # >> playerOptionAddBlacklist
    'id': 'Masukkan Pemain Ini Di Daftar Hitam',
    'en': 'Blacklist This Player',
    'hi': 'Is kheladi ko blacklist mein daalo',
    'es': 'Pon a este jugador en la lista negra',
    'ml': 'Ee khelaadiye blacklist-il koottuka'
},
'playerOptionAddBlacklistSuccess': {
    'id': 'Pemain Berhasil Ditambahkan Ke Daftar Hitam',
    'en': 'Player Successfully Added To Blacklist',
    'hi': 'Kheladi ko safalta se blacklist mein joda gaya',
    'es': 'Jugador añadido con éxito a la lista negra',
    'ml': 'Khelaadi blacklist-il vijayathode kootti'
},
'playerOptionAddBlacklistInMasterList': {
    'id': 'Kamu Tidak Bisa Menambahkan Tuanku Ke Daftar Hitam',
    'en': 'You Can\'t Blacklist My Master',
    'hi': 'Aap mere master ko blacklist mein nahi daal sakte',
    'es': 'No puedes poner a mi maestro en la lista negra',
    'ml': 'Ningal enre master-ine blacklist-il koottan pattilla'
},
'playerOptionAddBlacklistAlreadyExists': {
    'id': 'Pemain Ini Sudah Ada Masuk Daftar Hitam',
    'en': 'This Player Already Blacklisted',
    'hi': 'Ye kheladi pehle se hi blacklist mein hai',
    'es': 'Este jugador ya está en la lista negra',
    'ml': 'Ee khelaadi blacklist-il mungam thanne aanu'
},
'playerOptionRemoveMuted': { # >> playerOptionRemoveMuted
    'id': 'Jangan Bisukan Pemain Ini',
    'en': 'Unmute This Player',
    'hi': 'Is kheladi ko unmute karo',
    'es': 'Desilencia a este jugador',
    'ml': 'Ee khelaadiye unmute cheyyuka'
},
'playerOptionRemoveMutedSuccess': {
    'id': 'Pemain Berhasil Dihapus Dari Daftar Bisu',
    'en': 'Player Successfully Removed From Muted List',
    'hi': 'Kheladi ko safalta se muted list se hata diya gaya',
    'es': 'Jugador eliminado con éxito de la lista de silenciados',
    'ml': 'Khelaadi muted list-il ninnu vijayathode maatti'
},
'playerOptionRemoveMutedNotExist': {
    'id': 'Pemain Ini Tidak diBisukan',
    'en': 'This Player Is Not Muted',
    'hi': 'Ye kheladi muted nahi hai',
    'es': 'Este jugador no está silenciado',
    'ml': 'Ee khelaadi mute cheythittilla'
},
'playerOptionAddMuted': { # >> playerOptionAddMuted
    'id': 'Bisukan Pemain Ini',
    'en': 'Mute This Player',
    'hi': 'Is kheladi ko mute karo',
    'es': 'Silencia a este jugador',
    'ml': 'Ee khelaadiye mute cheyyuka'
},
'playerOptionAddMutedSuccess': {
    'id': 'Pemain Berhasil Dibisukan',
    'en': 'Player Successfully Muted',
    'hi': 'Kheladi ko safalta se muted list mein joda gaya',
    'es': 'Jugador añadido con éxito a la lista de silenciados',
    'ml': 'Khelaadi muted list-il vijayathode kootti'
},
'playerOptionAddMutedInMasterList': {
    'id': 'Kamu Tidak Bisa Menambahkan Tuanku Ke Daftar Bisu',
    'en': 'You Can\'t Mute My Master',
    'hi': 'Aap mere master ko mute nahi kar sakte',
    'es': 'No puedes silenciar a mi maestro',
    'ml': 'Ningal enre master-ine mute cheyyan pattilla'
},
'playerOptionAddMutedAlreadyExists': {
    'id': 'Pemain Ini Sudah diBisukan',
    'en': 'This Player Already Muted',
    'hi': 'Ye kheladi pehle se hi mute hai',
    'es': 'Este jugador ya está silenciado',
    'ml': 'Ee khelaadi mute cheythittilla'
},
'dataPopupSelectedIndex': {
    'id': 'Indeks Terpilih:\n[{0}]',
    'en': 'Selected Index:\n[{0}]',
    'hi': 'Chuna gaya index:\n[{0}]',
    'es': 'Índice Seleccionado:\n[{0}]',
    'ml': 'Thazhe pattiya index:\n[{0}]'
},
'cantMatchInPlayerData': {
    'id': 'Tidak Dapat Mencocokkan \"{}\" di Data Pemain',
    'en': 'Can\'t match \"{}\" in player data',
    'hi': 'Kheladi data mein \"{}\" se match nahi kar sakte',
    'es': 'No se puede coincidir \"{}\" en los datos del jugador',
    'ml': 'Khelaadi data-yil \"{}\" match cheyyan pattilla'
},
'cantFindInPlayerData': {
    'id': 'Tidak Dapat Menemukan \"{}\" di Data Pemain',
    'en': 'Can\'t find \"{}\" in player data',
    'hi': 'Kheladi data mein \"{}\" nahi mila',
    'es': 'No se puede encontrar \"{}\" en los datos del jugador',
    'ml': 'Khelaadi data-yil \"{}\" kandilla'
},
'addSuccess': {
    'id': 'Berhasil Ditambah',
    'en': 'Succesfully Added',
    'hi': 'Safalta se joda gaya',
    'es': 'Añadido Exitosamente',
    'ml': 'Vijayathode kootti'
},
'editSuccess': {
    'id': 'Teks Berhasil Diedit',
    'en': 'Text Succesfully Edited',
    'hi': 'Text safalta se edit kiya gaya',
    'es': 'Texto Editado Exitosamente',
    'ml': 'Text vijayathode edit cheythu'
},
'editExist': {
    'id': 'Teks Editan Sudah Ada',
    'en': 'Text Edited Already Exist',
    'hi': 'Edited text pehle se hi maujood hai',
    'es': 'El Texto Editado Ya Existe',
    'ml': 'Edited text munpu thanne undu'
},
'removeSuccess': {
    'id': 'Teks Berhasil Dihapus',
    'en': 'Text Succesfully Removed',
    'hi': 'Text safalta se hata diya gaya',
    'es': 'Texto Eliminado Exitosamente',
    'ml': 'Text vijayathode maatti'
},
'playerInfo': {
    'id': 'Info Pemain',
    'en': 'Player Info',
    'hi': 'Kheladi ki jankari',
    'es': 'Información del Jugador',
    'ml': 'Khelaadi vivaram'
},
'save': {
    'id': 'Simpan',
    'en': 'Save',
    'hi': 'Save karo',
    'es': 'Guardar',
    'ml': 'Save cheyyu'
},
'use': {
    'id': 'Gunakan',
    'en': 'Use',
    'hi': 'Upayog karo',
    'es': 'Usar',
    'ml': 'Upayogikkuka'
},
'copy': {
    'id': 'Salin',
    'en': 'Copy',
    'hi': 'Copy karo',
    'es': 'Copiar',
    'ml': 'Copy cheyyu'
},
'textCopied': {
    'id': '\"{}\" Disalin',
    'en': '\"{}\" Copied',
    'hi': '\"{}\" Copy kiya gaya',
    'es': '\"{}\" Copiado',
    'ml': '\"{}\" Copy cheythu'
},
'get': {
    'id': 'Dapatkan',
    'en': 'Get',
    'hi': 'Prapth karo',
    'es': 'Obtener',
    'ml': 'Edukkan'
},
'enabled': {
    'id': 'Dinyalakan',
    'en': 'Enabled',
    'hi': 'Enable kiya gaya',
    'es': 'Habilitado',
    'ml': 'Enable cheythu'
},
'disabled': {
    'id': 'Dimatikan',
    'en': 'Disabled',
    'hi': 'Disable kiya gaya',
    'es': 'Deshabilitado',
    'ml': 'Disable cheythu'
},
'confirmCopy': {
    'id': 'Salin Teks Ini',
    'en': 'Copy This Text',
    'hi': 'Is text ko copy karo',
    'es': 'Copiar Este Texto',
    'ml': 'Ee text copy cheyyu'
},
'translating': {
    'id': 'Menerjemahkan',
    'en': 'Translating',
    'hi': 'Anuvad kar rahe hain',
    'es': 'Traduciendo',
    'ml': 'Anuvadikkunnu'
},
'page': {
    'id': 'Halaman',
    'en': 'Page',
    'hi': 'Panna',
    'es': 'Página',
    'ml': 'Padippu'
},
'yes': {
    'id': 'Ya',
    'en': 'Yes',
    'hi': 'Haan',
    'es': 'Sí',
    'ml': 'Sheri'
},
'sorry': {
    'id': 'Maaf',
    'en': 'Sorry',
    'hi': 'Sorry',
    'es': 'Sorry',
    'ml': 'Sorry'
},
'search': {
    'id': 'Cari', 
    'en': 'Finder',      
    'hi': 'खोजें',     
    'es': 'Buscar',    
    'ml': 'തിരയുക'       
},
'thanks': {
    'id': 'Makasih',
    'en': 'Thanks',
    'hi': 'Thanks',
    'es': 'Gracias',
    'ml': 'Nandi'
},
'cancel': {
    'id': 'Batal',
    'en': 'Cancel',
    'hi': 'Radd karo',
    'es': 'Cancelar',
    'ml': 'Mattu'
},
'delete': {
    'id': 'Hapus',
    'en': 'Delete',
    'hi': 'Mitao',
    'es': 'Eliminar',
    'ml': 'Nashippikkuka'
},
'pasteNotSupported': {
    'id': 'Menempel teks dari clipboard tidak didukung',
    'en': 'Pasting text from clipboard not supported',
    'hi': 'Clipboard se text paste karne ka samarthan nahi hai',
    'es': 'Pegar texto del portapapeles no es compatible',
    'ml': 'Clipboard-il ninnum text paste cheyyan pattunilla'
},
'pasteEmpty': {
    'id': 'Tidak ada teks untuk ditempel',
    'en': 'No text to paste',
    'hi': 'Paste karne ke liye koi text nahi hai',
    'es': 'No hay texto para pegar',
    'ml': 'Paste cheyyan text illa'
},
'pasteConfirm': {
    'id': 'Tempel teks dari clipboard',
    'en': 'Paste text from clipboard',
    'hi': 'Clipboard se text paste kare',
    'es': 'Pegar texto del portapapeles',
    'ml': 'Clipboard-il ninnum text paste cheyyu'
},
'copyEmpty': {
    'id': 'Ngga Ada Teks Untuk Di Salin',
    'en': 'No Text To Copy',
    'hi': 'Copy karne ke liye koi text nahi',
    'es': 'No hay texto para copiar',
    'ml': 'Copy cheyyan text illa'
},
'editAttributeAddEmpty': {
    'id': 'Ngga ada teks untuk ditambah',
    'en': 'No text to add',
    'hi': 'Jodne ke liye koi text nahi',
    'es': 'No hay texto para agregar',
    'ml': 'Kooduthal text illa'
},
'editAttributeEmpty': {
    'id': 'Ngga ada teks untuk di edit',
    'en': 'No text to edit',
    'hi': 'Sanshodhan ke liye koi text nahi',
    'es': 'No hay texto para editar',
    'ml': 'Sanshodhikkunna text illa'
},
'editAttributeExist': {
    'id': 'Teks sudah ada di attribut',
    'en': 'Text already exist in the attribute',
    'hi': 'Text pehle se hi attribute mein maujood hai',
    'es': 'El texto ya existe en el atributo',
    'ml': 'Text attribute-il mungam undu'
},
'editAttributeSame': {
    'id': 'Teks yang di edit sama',
    'en': 'The edited text is the same',
    'hi': 'Sanshodhit text vahi hai',
    'es': 'El texto editado es el mismo',
    'ml': 'Sanshodhicha text adheham thanne'
},
'editAttributeDeleteEmpty': {
    'id': 'Tidak ada teks untuk di hapus',
    'en': 'No text to delete',
    'hi': 'Mitane ke liye koi text nahi',
    'es': 'No hay texto para eliminar',
    'ml': 'Nashippikkunna text illa'
},
'addAttributePlayerNotInData': {
    'id': 'Pemain \"{}\" tidak ada di data',
    'en': 'Player \"{}\" not in data',
    'hi': 'Kheladi \"{}\" data mein nahi hai',
    'es': 'Jugador \"{}\" no está en los datos',
    'ml': 'Kalikaaran \"{}\" data-yil illa'
},
'addAttribteNoSplitter': {
    'id': 'Gunakan \"{}\" untuk memisahkan kunci dan nilai',
    'en': 'Use \"{}\" for separating key and value',
    'hi': 'Key aur value alag karne ke liye \"{}\" ka upyog karein',
    'es': 'Usa \"{}\" para separar clave y valor',
    'ml': 'Keyum valueum verupatthikkunna \"{}\" upayogikkuka'
},
'translatePopupWarning': {
    'id': 'Fitur ini tidak dilanjutkan/diuji oleh Less\nDapat menyebabkan error yang tak terduga\nGunakan dengan resiko mu sendiri',
    'en': 'This feature is not continued/tested by Less\nMay cause unexpected errors\nUse at your own risk',
    'hi': 'Ye feature Less dwara na to jari hai na hi test kiya gaya hai\nAnapekshit errors ka karan ban sakta hai\nApne risk par upyog karein',
    'es': 'Esta característica no es continuada/probada por Less\nPuede causar errores inesperados\nÚsalo bajo tu propio riesgo',
    'ml': 'Ee feature Less kooduthal test cheyyappetta onnumalla\nEttavum pratheekshikkatha errors undaakum\nSwantam riskil upayogikkuka'
},
'pswTitle': {
    'id': 'Pengaturan Kustom',
    'en': 'Custom Settings',
    'hi': 'Custom Settings',
    'es': 'Configuraciones Personalizadas',
    'ml': 'Custom Settings'
},
'pswButtonTranslatedTextsDict': {
    'id': 'Kamus Teks Terjemahan',
    'en': 'Translated Texts Dictionaries',
    'hi': 'Anuvadit texts dictionaries',
    'es': 'Diccionarios de Textos Traducidos',
    'ml': 'Anuvadithamaya texts dictionaries'
},
'pswButtonTranslateWindowSettings': {
    'id': 'Pengaturan Terjemahan',
    'en': 'Translate Settings',
    'hi': 'Anuvad Settings',
    'es': 'Configuraciones de Traducción',
    'ml': 'Anuvad Settings'
},
'pswButtonTranslateWindowSettingsTutorial': {
    'id': 'Ketuk dua kali tombol terjemahan untuk membuka Jendela Pengaturan Terjemahan',
    'en': 'Double-tap translate button to open Translate Settings Window',
    'hi': 'Translate settings window kholne ke liye translate button par do baar tap karein',
    'es': 'Toca dos veces el botón de traducción para abrir la Ventana de Configuración de Traducción',
    'ml': 'Translate settings window thurakkan translate button-il randu thavana thattuka'
},
'pswCheckboxAccuratePing': {
    'id': 'Ping Server Akurat',
    'en': 'Accurate Server Ping',
    'hi': 'Sahi Server Ping',
    'es': 'Ping Preciso del Servidor',
    'ml': 'Sariyaya Server Ping'
},
'pswCheckboxPing': {
    'id': 'Tombol Ping',
    'en': 'Ping Button',
    'hi': 'Ping ka button',
    'es': 'Botón de Ping',
    'ml': 'Ping button'
},
'pswCheckboxIP': {
    'id': 'Tombol IP',
    'en': 'IP Button',
    'hi': 'IP ka Button',
    'es': 'Botón de IP',
    'ml': 'IP Button'
},
'pswCheckboxCopyPaste': {
    'id': 'Tombol Salin & Tempel',
    'en': 'CoPas Button',
    'hi': 'Copy Aur Paste Ka Button',
    'es': 'Botón de Copiar y Pegar',
    'ml': 'Copyum Pasteum Cheyyunna Button'
},
'pswCheckboxQuickRespond': {
    'id': 'Respon Cepat di Tombol Kirim',
    'en': 'Quick Respond In Send Button',
    'hi': 'Send Button Mein Turant Jawab Dena',
    'es': 'Respuesta Rápida en Botón de Enviar',
    'ml': 'Send Button-il Vegathil Prathikarikkuka'
},
'pswCheckboxAutoGreet': {
    'id': 'Sapa Teman Secara Otomatis (Jika Belum)',
    'en': 'Auto Greet My Friends (If Haven\'t)',
    'hi': 'Mere Doston Ko Apne Aap Salaam Karna (Agar Nahi Kiya Hai To)',
    'es': 'Saludo Automático a Mis Amigos (Si No Lo He Hecho)',
    'ml': 'Ente Snehithare Swayam Sambodhikkuka (Cheythittillenkil)'
},
'pswCheckboxAutoGreetMaster': {
    'id': 'Sapa Otomatis Hanya Jika Master Bergabung',
    'en': 'Auto Greet Only If Master Joined',
    'hi': 'Sirf Tabhi Apne Aap Salaam Karna Jab Master Shamil Ho',
    'es': 'Saludo Automático Solo Si El Maestro Se Une',
    'ml': 'Master Koodiyal Mathrame Swayam Sambodhikkuka'
},
'pswCheckboxAutoGreetFriends': {
    'id': 'Sapa Otomatis Hanya Jika Teman Bergabung',
    'en': 'Auto Greet Only If My Friends Joined',
    'hi': 'Sirf Tabhi Apne Aap Salaam Karna Jab Mere Dost Shamil Hon',
    'es': 'Saludo Automático Solo Si Mis Amigos Se Unen',
    'ml': 'Ente Snehithar Koodiyal Mathrame Swayam Sambodhikkuka'
},
'pswCheckboxDirectCustomCmd': {
    'id': 'Kirim Langsung Perintah Kustom',
    'en': 'Directly Send Custom Commands',
    'hi': 'Custom Commands Seedhe Bhejna',
    'es': 'Enviar Comandos Personalizados Directamente',
    'ml': 'Custom Commands Nere Ayachu Thannuka'
},
'pswCheckboxBlockNACommand': {
    'id': 'Blokir Perintah Internal yang Salah/Tidak Dikenal',
    'en': 'Block Incorrect/Unknown Internal Commands',
    'hi': 'Galat/Anjana Antarik Commands Ko Block Karna',
    'es': 'Bloquear Comandos Internos Incorrectos/Desconocidos',
    'ml': 'Thappu/Ariyatha Internal Commands Block Cheyyuka'
},
'pswCheckboxAskGameReplayName': {
    'id': 'Minta Nama Untuk Menyimpan Replay Terakhir',
    'en': 'Ask Naming For Saving Last Replay',
    'hi': 'Akhri Replay Save Karne Ke Liye Naam Poochna',
    'es': 'Preguntar Nombre Para Guardar El Último Replay',
    'ml': 'Kadha Replay Save Cheyyan Peru Chodhikkuka'
},
'pswCheckboxColorfulChats': {
    'id': 'Obrolan Berwarna-warni',
    'en': 'Colorful Chats',
    'hi': 'Rang-birange Chats',
    'es': 'Chats Coloridos',
    'ml': 'Varnamaya Samvadangal'
},
'pswCheckboxFocusToLastMsg': {
    'id': 'Otomatis Fokus ke Pesan Terakhir yang Dikirim',
    'en': 'Auto Focus To Last Message Sent',
    'hi': 'Bheje Gaye Akhri Sandesh Par Swayam Focus Karna',
    'es': 'Enfocar Automáticamente El Último Mensaje Enviado',
    'ml': 'Ayachu Thanna Kadha Sandeshattil Swayam Focus Cheyyuka'
},
'pswCheckboxHighlightChosenText': {
    'id': 'Sorot Teks Obrolan yang Dipilih',
    'en': 'Highlight Chosen Chat Text',
    'hi': 'Chune Gaye Chat Text Ko Highlight Karna',
    'es': 'Resaltar El Texto Del Chat Seleccionado',
    'ml': 'Ethirtha Chat Text Highlight Cheyyuka'
},
'pswCheckboxIncludePnameOnChosenText': {
    'id': 'Sertakan Nama Pemain pada Teks Obrolan yang Dipilih',
    'en': 'Include Player Name On Chosen Chat Text',
    'hi': 'Chune Gaye Chat Text Mein Kheladi Ka Naam Shamil Karna',
    'es': 'Incluir El Nombre Del Jugador En El Texto Del Chat Seleccionado',
    'ml': 'Ethirtha Chat Text-il Playernte Peru Kooduthal'
},
'pswCheckboxIncludeCidInQcNameChanger': {
    'id': 'Sertakan ClientID pada Pengubah Nama Cepat',
    'en': 'Include ClientID in Quick Name Changer',
    'hi': 'Quick Name Changer Mein ClientID Shamil Karna',
    'es': 'Incluir ClientID en el Cambiador Rápido de Nombres',
    'ml': 'Quick Name Changer-il ClientID Kooduthal'
},
'pswCheckboxSaveLastTypedMsg': {
    'id': 'Simpan Pesan Terakhir yang Diketik di Kolom Teks',
    'en': 'Save Last Message Typed In Text Field',
    'hi': 'Text Field Mein Type Kiye Gaye Akhri Sandesh Ko Save Karna',
    'es': 'Guardar El Último Mensaje Escrito En El Campo De Texto',
    'ml': 'Text Field-il Type Cheytha Kadha Sandesham Save Cheyyuka'
},
'pswCheckboxCustomScreenmessage': {
    'id': 'Modifikasi Pesan Layar Chat',
    'en': 'Modified Chat Screenmessage',
    'hi': 'Badla hua Chat Screenmessage',
    'es': 'Mensaje de Pantalla de Chat Modificado',
    'ml': 'Maattappetta Chat Screenmessage'
},
'pswCheckboxColorfulScreenmessage': {
    'id': 'Pesan Layar Bewarna-warni',
    'en': 'Colorful Screenmessage',
    'hi': 'Rang-birange Screenmessage',
    'es': 'Mensaje de Pantalla Colorido',
    'ml': 'Varnamaya Screenmessage'
},
'pswCheckboxChatNameViewerInScrmsg': {
    'id': 'Penampil-nama Chat di Screenmessage',
    'en': 'Chat Name Viewer in Screenmessage',
    'hi': 'Screenmessage Mein Chat Naam Dikhana',
    'es': 'Visor de Nombre de Chat en Mensaje de Pantalla',
    'ml': 'Screenmessage-il Chat Peru Kanikkuka'
},
'pswGlobalVarMaxPartywindowChats': {
    'id': 'Maksimal Obrolan di Jendela Party',
    'en': 'Party Window Max Chats',
    'hi': 'Party Window Ke Maksimam Chats',
    'es': 'Máximo de Chats en la Ventana de Party',
    'ml': 'Party Windowile Chatukalude Ettavum Kooduthal'
},
'pswGlobalVarPingMessage': {
    'id': 'Pesan Ping',
    'en': 'Ping Messages',
    'hi': 'Ping Sandesh',
    'es': 'Mensaje de Ping',
    'ml': 'Ping Sandesham'
},
'pswGlobalVarMaxWarns': {
    'id': 'Peringatan Maksimal Pemain',
    'en': 'Max Player Warns',
    'hi': 'Kheladi ke Maksimam Chetavani',
    'es': 'Máximas Advertencias Para Jugadores',
    'ml': 'Kheladikalkku Etavum Kooduthal Chetavani'
},
'pswGlobalVarPartyScale': {
    'id': 'Skala Party Window (S, M, L)',
    'en': 'Party Window Scale (S, M, L)',
    'hi': 'Party Window Ka Scale (S, M, L)',
    'es': 'Escala de la Ventana de Party (S, M, L)',
    'ml': 'Party Window-nte Scale (S, M, L)'
},
'pswGlobalVarInvalidInput': {
    'id': 'Input tidak valid untuk variabel global: {}',
    'en': 'Invalid input for global variables: {}',
    'hi': 'Global variables ke liye galat input: {}',
    'es': 'Entrada no válida para variables globales: {}',
    'ml': 'Global variables-inte thettaya input: {}'
},
'partyChatMutedWarn': {
    'id': 'Kamu sedang membisukan obrolan PartyWindow',
    'en': 'You\'re currently muting PartyWindow chats',
    'hi': 'Aap abhi partywindow chats ko mute kar rahe hain',
    'es': 'Actualmente estás silenciando los chats de PartyWindow',
    'ml': 'Ningal ippol partywindow chatukal mute cheyyunnu'
},
'rswTitle': {
    'id': 'Pengaturan Responder Chat',
    'en': 'Chat Responder Settings',
    'hi': 'Chat Responder Settings',
    'es': 'Configuración del Respondedor de Chat',
    'ml': 'Chat Responder Settings'
},
'rswEnable': {
    'id': 'Nyalakan Auto Responder Pesan',
    'en': 'Turn On Chat Auto Responder Engine',
    'hi': 'Chat Auto Responder Chalu Karein',
    'es': 'Activar el Respondedor Automático de Chat',
    'ml': 'Chat auto responder on aakku'
},
'rswSoal': {
    'id': 'Jawab Otomatis Pertanyaan Server',
    'en': 'Auto Answer Server Questions',
    'hi': 'Server ke sawalo ka automatic jawab',
    'es': 'Respuesta Automática a Preguntas del Servidor',
    'ml': 'Server chodhyangalkku automatic aayi uttaram'
},
'rswAmongUs': {
    'id': 'Among Us',
    'en': 'Among Us',
    'hi': 'Among Us',
    'es': 'Among Us',
    'ml': 'Among Us'
},
'rswNoNoobWord': {
    'id': 'Anti Kata Noob',
    'en': 'No Noob Word',
    'hi': 'Noob Shabd Nhi',
    'es': 'Sin Palabra Noob',
    'ml': 'Noob Shabdam Illa'
},
'rswCustomReplies': {
    'id': 'Balasan Otomatis Kustom',
    'en': 'Custom Replies',
    'hi': 'Custom Uttar',
    'es': 'Respuestas Personalizadas',
    'ml': 'Custom Uttarangal'
},
'rswAutoGreet': {
    'id': 'Sapa Otomatis',
    'en': 'Auto Greet',
    'hi': 'Automatic abhinandan',
    'es': 'Saludo Automático',
    'ml': 'Automatic abhinandanam'
},
'rswBruhIfAmazing': {
    'id': 'Bruh Jika Luar Biasa',
    'en': 'Bruh If Amazing',
    'hi': 'Bruh agar amazing ho',
    'es': 'Bruh Si Es Increíble',
    'ml': 'Bruh amazing aayal'
},
'rswCurrentSessionListLog': {
    'id': 'Log Daftar Sesi Saat Ini',
    'en': 'Current Session List Log',
    'hi': 'Current session ki list ka log',
    'es': 'Registro de Lista de Sesión Actual',
    'ml': 'Current session listinte log'
},
'rswAllNamesListLog': {
    'id': 'Log Daftar Semua Nama',
    'en': 'All Names List Log',
    'hi': 'Sabhi namon ki list ka log',
    'es': 'Registro de Lista de Todos los Nombres',
    'ml': 'Ellaa perukalude listinte log'
},
'rswCmdLogForPC': {
    'id': 'Log CMD Untuk PC',
    'en': 'CMD Log For PC',
    'hi': 'PC ke liye CMD log',
    'es': 'Registro CMD Para PC',
    'ml': 'PC-ykk CMD log'
},
'rswAntiAbuseAutoWarn': {
    'id': 'Anti Kata Kasar (Peringatan Otomatis)',
    'en': 'Anti Abuse (Auto Warn)',
    'hi': 'Anti abuse (automatic chetavani)',
    'es': 'Anti Abuso (Advertencia Automática)',
    'ml': 'Anti abuse (automatic chetavani)'
},
'rswIncludeChillAbuse': {
    'id': 'Sertakan Kata Kasar Kasual',
    'en': 'Include Casual Abuse',
    'hi': 'Saamanya apashabda shaamil karen',
    'es': 'Incluir Abuso Casual',
    'ml': 'Saadhaarana apashabdam kooduthal'
},
'rswAutoKickOnMaxWarns': {
    'id': 'Tendang Otomatis Saat Peringatan Maksimal',
    'en': 'Auto Kick On Max Warns',
    'hi': 'Maksimam chetavani par automatic kick',
    'es': 'Expulsión Automática en Máximas Advertencias',
    'ml': 'Etavum kooduthal chetavaniyil automatic kick'
},
'rswRefreshPlayersProfile': {
    'id': 'Segarkan Profil Pemain',
    'en': 'Refresh Player\'s Profile',
    'hi': 'Kheladi ke profile ko refresh karen',
    'es': 'Actualizar Perfil del Jugador',
    'ml': 'Kheladinte profile refresh cheyyuka'
},
'rswOnlyUpdateAvailablePData': {
    'id': 'Hanya Perbarui P-Data yang Tersedia',
    'en': 'Only Update Available P-Data',
    'hi': 'Sirf uplabdh P-data ko update karen',
    'es': 'Solo Actualizar P-Datos Disponibles',
    'ml': 'Ullathil P-data matrame update cheyyuka'
},
'rswChatLogging': {
    'id': 'Pencatatan Obrolan',
    'en': 'Chat Logging',
    'hi': 'Chat log karna',
    'es': 'Registro de Chats',
    'ml': 'Chat log cheyyuka'
},
'rswAddDatesAsSeparatorOnChatDataFiles': {
    'id': 'Tambahkan Tanggal Sebagai Pemisah di File Data Obrolan',
    'en': 'Add Dates As Separator On Chat Data Files',
    'hi': 'Chat data files par dates ko separator ke roop mein jodhen',
    'es': 'Agregar Fechas Como Separador en Archivos de Datos de Chat',
    'ml': 'Chat data files-il dates separator aayi kooduthal'
},
'rswTranslateMachine': {
    'id': 'Mesin Terjemahan',
    'en': 'Translate Machine',
    'hi': 'Anuvad machine',
    'es': 'Máquina de Traducción',
    'ml': 'Anuvadana yanthram'
},
'rswResetPlayerWarnsEachBoot': {
    'id': 'Setel Ulang Peringatan Pemain Setiap Booting',
    'en': 'Reset Player Warns Each Boot',
    'hi': 'Har boot par kheladi ke chetavani ko reset karen',
    'es': 'Reiniciar Advertencias de Jugador en Cada Arranque',
    'ml': 'Ore bootilum kheladinte chetavani reset cheyyuka'
},
'rswPartialMatchAbuses': {
    'id': 'Pencocokan Sebagian Kata Kasar',
    'en': 'Partial Match Abuses',
    'hi': 'Partial match abuses',
    'es': 'Abusos de Coincidencia Parcial',
    'ml': 'Partial match abuses'
},
'rswBypassAutoAnswerBlocker': {
    'id': 'Terobos Pemblokir Jawaban Otomatis',
    'en': 'Bypass Auto Answer Blocker',
    'hi': 'Automatic jawab blocker ko bypass karen',
    'es': 'Evitar Bloqueador de Respuesta Automática',
    'ml': 'Automatic uttar blocker bypass cheyyuka'
},
'rswAddYourProfileToMainName': {
    'id': 'Tambahkan Profil Anda ke Nama Utama',
    'en': 'Add Your Profile To Main Name',
    'hi': 'Apna profile main name mein jodhen',
    'es': 'Agregar Tu Perfil al Nombre Principal',
    'ml': 'Ninre profile main name-il kooduthal'
},
'rswUseScreenmessageCmdPrompts': {
    'id': 'Gunakan Prompt CMD Screenmessage',
    'en': 'Use Screenmessage CMD Prompts',
    'hi': 'Screenmessage CMD prompts ka upyog karen',
    'es': 'Usar Indicaciones CMD de Mensaje en Pantalla',
    'ml': 'Screenmessage CMD prompts upayogikkuka'
},
'rswPrioritizePbIdFromBcs': {
    'id': 'Prioritaskan PB-ID dari BCS',
    'en': 'Prioritize PB-ID From BCS',
    'hi': 'BCS se PB-ID ko prathamikta den',
    'es': 'Priorizar PB-ID de BCS',
    'ml': 'BCS-il ninnum PB-ID-ykk prathamikta kodukkuka'
},
'rswSendMyPingIfPing': {
    'id': 'Kirim Ping Saya Jika Ping',
    'en': 'Send My Ping If Ping',
    'hi': 'Ping karen to mera ping bhejen',
    'es': 'Enviar Mi Ping Si Hay Ping',
    'ml': 'Ping cheyyumpol ente ping ayakkuka'
},
'rswKickVoterAnalyzer': {
    'id': 'Analisis Penendang',
    'en': 'Kick Voter Analyzer',
    'hi': 'Kick voter analyzer',
    'es': 'Analizador de Votantes de Expulsión',
    'ml': 'Kick voter analyzer'
},
'errorPopupTitle': {
    'id': 'Catatan Kesalahan Internal',
    'en': 'Internal Error Log',
    'hi': 'Antarik truti log',
    'es': 'Registro de Errores Internos',
    'ml': 'Aathya thappu log'
},
'errorPopupConfirmCopyError': {
    'id': 'Salin Kesalahan ke Clipboard',
    'en': 'Copy Error To Clipboard',
    'hi': 'Truti ko clipboard mein copy karen',
    'es': 'Copiar Error al Portapapeles',
    'ml': 'Thappu clipboard-il copy cheyyuka'
},
'errorPopupErrorCopied': {
    'id': 'Error Disalin',
    'en': 'Error Copied',
    'hi': 'Truti copy ho gaya',
    'es': 'Error Copiado',
    'ml': 'Thappu copy cheythu'
},
'errorPopupNoError': {
    'id': 'Tidak Ada Kesalahan Tercatat',
    'en': 'No Errors Logged',
    'hi': 'Koi truti log nahi hua',
    'es': 'No Hay Errores Registrados',
    'ml': 'Thappukal log cheythittilla'
},
'v1.4ServerTitle': {
    'id': 'Server Versi V1.4',
    'en': 'Server Is V1.4',
    'hi': 'Server V1.4 Hai',
    'es': 'El Servidor Es V1.4',
    'ml': 'Server V1.4 Aanu'
},
'v1.4ServerMsg': {
    'id': 'Anda Bermain Di Server V1.4',
    'en': 'You\'re Playing In V1.4 Server',
    'hi': 'Aap V1.4 Server Mein Khel Rahe Hain',
    'es': 'Estás Jugando En Un Servidor V1.4',
    'ml': 'Nee V1.4 Server-il Kalikkunnu'
},
'gatherWindowStillOpen': {
    'id': 'Jendela Gather masih terbuka',
    'en': 'Gather window still opened',
    'hi': 'Gather window abhi bhi khula hai',
    'es': 'La ventana de reunión sigue abierta',
    'ml': 'Gather window ini open aayi nilkkunnu'
},
'partyConfigLoadRemoveKey': {
    'id': 'Menghapus konfigurasi PartyWindow yang kedaluwarsa atau tidak valid',
    'en': 'Removing outdated or invalid partywindow config',
    'hi': 'Purana ya amanya partywindow config hata rahe hain',
    'es': 'Eliminando configuración obsoleta o inválida de PartyWindow',
    'ml': 'Kazhinja athava amanya partywindow config remove cheyyunnu'
},
'partyConfigLoadAddKey': {
    'id': 'Menambahkan konfigurasi default PartyWindow yang hilang',
    'en': 'Adding missing default partywindow config',
    'hi': 'Gumshuda default partywindow config jod rahe hain',
    'es': 'Agregando configuración predeterminada faltante de PartyWindow',
    'ml': 'Kazhiya default partywindow config kooduthal'
},
'partyConfigLoadError': {
    'id': 'Error Saat Memuat Konfigurasi Utama Party',
    'en': 'Error On Main Party Config Load',
    'hi': 'Main party config load mein truti',
    'es': 'Error al Cargar la Configuración Principal de Party',
    'ml': 'Main party config load-il thappu'
},
'responderConfigLoadRemoveKey': {
    'id': 'Menghapus konfigurasi Responder yang kedaluwarsa atau tidak valid',
    'en': 'Removing outdated or invalid responder config',
    'hi': 'Purana ya amanya responder config hata rahe hain',
    'es': 'Eliminando configuración obsoleta o inválida de Responder',
    'ml': 'Kazhinja athava amanya responder config remove cheyyunnu'
},
'responderConfigLoadAddKey': {
    'id': 'Menambahkan konfigurasi default Responder yang hilang',
    'en': 'Adding missing default responder config',
    'hi': 'Gumshuda default responder config jod rahe hain',
    'es': 'Agregando configuración predeterminada faltante de Responder',
    'ml': 'Kazhiya default responder config kooduthal'
},
'responderConfigLoadError': {
    'id': 'Error Saat Memuat Konfigurasi Utama Responder',
    'en': 'Error On Main Responder Config Load',
    'hi': 'Main responder config load mein truti',
    'es': 'Error al Cargar la Configuración Principal de Responder',
    'ml': 'Main responder config load-il thappu'
},
'translateSettingsTitle': {
    'id': 'Pengaturan Terjemahan',
    'en': 'Translation Settings',
    'hi': 'Anuvaad Settings',
    'es': 'Configuración de Traducción',
    'ml': 'Mozhi Mattal Settings'
},
'translateSettingsTextfield': {
    'id': 'Kolom Teks',
    'en': 'TextField Texts',
    'hi': 'TextField Texts',
    'es': 'Textos de Campo de Texto',
    'ml': 'TextField Texts'
},
'translateSettingsOther': {
    'id': 'Teks Lainnya',
    'en': 'Other Texts',
    'hi': 'Anya Texts',
    'es': 'Otros Textos',
    'ml': 'Mattulla Texts'
},
'translateMethod': {
    'id': 'Metode Penerjemahan',
    'en': 'Translate Method',
    'hi': 'Anuvaad Prakriya',
    'es': 'Método de Traducción',
    'ml': 'Mozhi Mattal Padhathi'
},
'translateMethodLINK': {
    'id': 'Tautan',
    'en': 'Link',
    'hi': 'Link',
    'es': 'Enlace',
    'ml': 'Link'
},
'translateMethodAPI': {
    'id': 'API',
    'en': 'API',
    'hi': 'API',
    'es': 'API',
    'ml': 'API'
},
'pingInvalidIPandPORT': {
    'id': 'IP dan PORT Tidak Valid',
    'en': 'Not A Valid IP And PORT',
    'hi': 'Sahi IP Aur PORT Nahin',
    'es': 'No Es Una IP Y Puerto Válidos',
    'ml': 'Sariyaya IP Um Port Illa'
},
'pingNotAvailable': {
    'id': 'Tidak Dapat Melakukan Ping Saat Ini',
    'en': 'Can\'t Do Ping Right Now',
    'hi': 'Abhi Ping Nahi Kar Sakte',
    'es': 'No Se Puede Hacer Ping Ahora',
    'ml': 'Ippol Ping Cheyyan Kazhiyilla'
},
'isPingingServer': {
    'id': 'Masih melakukan ping server',
    'en': 'Still pinging server',
    'hi': 'Abhi bhi server ping ho raha hai',
    'es': 'Todavía haciendo ping al servidor',
    'ml': 'Ippozhum server ping cheyyunnu'
},
'credit&help': {
    'id': 'Kredit dan Bantuan',
    'en': 'Credit and Help', 
    'hi': 'Shrey aur Sahayata',
    'es': 'Crédito y Ayuda',
    'ml': 'Kreeditum Sahayavum'
},
'': {
    'id': '',
    'en': '',
    'hi': '',
    'es': '',
    'ml': ''
},
'': {
    'id': '',
    'en': '',
    'hi': '',
    'es': '',
    'ml': ''
}}
"""Global Access Translated Text Keys"""

def get_lang_text(key: str, lang_id: Optional[str] = None) -> str:
    """
    Returns translated text based on given key.

    Args:
        key: Key to get value/text from `Translate_Texts`
        lang_id: `('id', 'en', ...)` for specific language

    Desc:
        1 Star  : Key exists but language is empty, using 'en' as fallback
        2 Stars : Key not found or text empty
    """
    invalid_text = INVALID_KEY_TEXT.format(key)
    lang = lang_id if lang_id in DEFAULT_AVAILABLE_LANG_ID_LIST else get_app_lang_as_id()

    text = Translate_Texts.get(key, {}).get(lang, '')

    if not text:
        en_text = Translate_Texts.get(key, {}).get('en', '')
        if en_text: return f"*{en_text}"

    return text if text else f"**{invalid_text}" 

## Choices Text Trans Key ##
POPUP_MENU_TYPE_MENU_PRESS = 'menu'
CHOICES_KEY_MENU = 'menuOption'
POPUP_MENU_TYPE_PARTY_MEMBER_PRESS = 'partyMemberPress'
POPUP_MENU_TYPE_WARN_SELECT = 'warnOptionSelect'
POPUP_MENU_TYPE_ADD_WARN_TYPE = 'addWarnOptionSelect'
POPUP_MENU_TYPE_CHAT_VIEWER_TYPE = 'chatViewerType'
POPUP_MENU_TYPE_CHAT_PRESS = 'chatPress'
POPUP_MENU_TYPE_PLAYER_OPTION = 'playerOption'

## PopupMenuWindow Choices Type ##
POPUP_MENU_TYPE_MUTE_TYPE = 'muteType'
POPUP_MENU_TYPE_RM_QCK_RESPND_SEL = 'hapusResponCepatPilih'
POPUP_MENU_TYPE_SORT_QCK_RESPND = 'quickMessage'
POPUP_MENU_TYPE_EXECUTE_CHOICE = 'executeChoice'
POPUP_MENU_TYPE_SHOW_ICONS = 'showAllIcons'

def get_choices_key_lang_text(choice_key: str) -> Tuple[list[str], list[str]]:
    """
    Retruns tuple of two lists: `Choices Keys`, and that `Choices Keys' Display` Texts.
    Used For PopupMenuWindow
    """
    # key: str key list
    Key_Choices: Dict[str, list[str]] = {
        CHOICES_KEY_MENU: [
            'opsiBisu', 'modifWarnaParty', 'editCustomCommands', 'editResponCepat', 'saveLastGameReplay'#,'hapusResponCepat', 'tambahResponCepat', 'credit'
        ],
        POPUP_MENU_TYPE_MUTE_TYPE: [
            'muteInGameOnly', 'mutePartyWindowOnly', 'muteAll', 'unmuteAll'
        ],
        POPUP_MENU_TYPE_PARTY_MEMBER_PRESS: [
            'votekick', 'mention', 'adminkick', 'adminremove', 'warnInfo', 'playerInfo'
        ],
        POPUP_MENU_TYPE_WARN_SELECT: [
            'partyPressWarnDecrease', 'partyPressWarnAdd' 
        ],
        POPUP_MENU_TYPE_ADD_WARN_TYPE: [ # Add more warning Type
            'addWarnBetraying', 'addWarnAbusing', 'addWarnUnnecessaryVotes', 'addWarnTeaming'
        ],
        POPUP_MENU_TYPE_CHAT_VIEWER_TYPE: [
            'chatViewProfile', 'chatViewAccount', 'chatViewMulti', 'chatViewMultiV2'
        ],
        POPUP_MENU_TYPE_CHAT_PRESS: [
            'translateText', 'copyText', 'insertText'
        ]
    }
    choices_key     : List[str] = Key_Choices.get(choice_key, [])
    choices_display : List[str] = [get_lang_text(text) for text in choices_key]

    return (choices_key, choices_display)

def _create_baLstr_list(str_list: List[str]) -> Sequence[babase.Lstr]:
    return tuple(babase.Lstr(value=i) for i in str_list)

def _copy_to_clipboard(text: str, close_widget_func: Optional[Callable[[], None]] = None):
    if text.strip():
        babase.clipboard_set_text(text)
        screenmessage(f'{get_lang_text("textCopied").format(text)}', color=COLOR_SCREENCMD_NORMAL)
        bui.getsound('gunCocking').play(1.75)
    else:
        bui.getsound('error').play(1.75)
        screenmessage(get_lang_text('copyEmpty'), COLOR_SCREENCMD_ERROR)
    if close_widget_func:
        try: close_widget_func()
        except Exception as e: print(str(e))

def _send_message_parted(msg: str):
    if not isinstance(MAX_MSG_LENGTH, int) or MAX_MSG_LENGTH > 99:
        screenmessage(f"{get_lang_text('invalidMaxMsgLen').format(val=str(MAX_MSG_LENGTH), type=str(type(MAX_MSG_LENGTH)))}", COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.75)
        return
    if len(msg) > MAX_MSG_LENGTH:
        if " " not in msg:
            # Handle case where there are no spaces and the message is too long
            lines = [msg[i:i+MAX_MSG_LENGTH] for i in range(0, len(msg), MAX_MSG_LENGTH)]
        else:
            words = msg.split()
            lines: list[str] = []
            current_line: str = ""

            for word in words:
                if len(current_line) + len(word) + 1 <= MAX_MSG_LENGTH:  # +1 for space
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())  # Add the last line

        send_delay = 0.175  # should be between 0.0 - 1.0
        print(lines)
        for i, line in enumerate(lines):
            delay = i + 1
            if not len(lines) == delay:
                line += "-"  # Continuous msg mark :)
            babase.apptimer(delay * send_delay, Call(chatmessage, line))
    else:
        chatmessage(msg)

####### INTERAL EXCEPTION LOG #######
def print_internal_exception(*args: Any, **keywds: Any) -> None:
    """Print info about an exception along with pertinent context state.

    Category: **General Utility Functions**

    Prints all arguments provided along with various info about the
    current context and the outstanding exception.
    Pass the keyword 'once' as True if you want the call to only happen
    one time from an exact calling location.
    """
    if keywds:
        allowed_keywds = ['once']
        if any(keywd not in allowed_keywds for keywd in keywds):
            raise TypeError('invalid keyword(s)')
    try:
        # If we're only printing once and already have, bail.
        if keywds.get('once', False):
            if not _babase.do_once():
                return

        print('FLUFFY EXCEPTION ERROR:')
        _babase.print_context()

        print('PRINTED-FROM:')
        # Basically the output of traceback.print_stack()
        stackstr = ''.join(traceback.format_stack())
        print(stackstr, end='')
        stack_str = f'ERROR: {stackstr}\n'

        print('EXCEPTION:')
        # Basically the output of traceback.print_exc()
        _excstr = traceback.format_exc()
        excstr = '\n'.join('  ' + l for l in _excstr.splitlines())
        print(excstr)
        exception_str = f'{excstr}'

        err_str = ' '.join([str(a) for a in args])
        error_str = f'ERROR: {err_str}'
        print(f'FLUFFY ERROR: {err_str}\n')

        log_internal_exception(stackstr, excstr, err_str)
    except Exception:
        # I suppose using print_exception here would be a bad idea.
        print('ERROR: exception in print_internal_exception():')
        traceback.print_exc()
    try:
        bui.getsound('error').play(1.5)
    except:
        pass

error_data: Dict[str, dict[str, str]] = {}
def _load_internal_exception() -> Dict[str, dict[str, str]]:
    global error_data
    log_file_path = internal_error_log_file_path  # Path to the log file
    try:
        if not os.path.exists(responder_directory):
            os.makedirs(responder_directory)
        # Load existing error log if it exists
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r', encoding='utf-8') as f:
                error_data = json.load(f)
        else:
            with open(log_file_path, 'w', encoding='utf-8') as file:
                json.dump(error_data, file, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print_internal_exception(e)
    return error_data


def generate_random_key(length: int = 8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def log_internal_exception(stackstr, excstr, err_str):
    """Log internal exceptions to a JSON file"""
    global error_data
    log_file_path = internal_error_log_file_path  # Path to the log file

    curr_data = _load_internal_exception()
    
    # Check if excstr already exists in error_data
    existing_key = None
    for key, value in error_data.items():
        if value.get("excstr") == excstr:
            existing_key = key
            break
            
    # If excstr exists, move it to the end
    if existing_key:
        # Remove existing entry
        existing_entry = error_data.pop(existing_key)
        # Generate new random key
        new_key = generate_random_key()
        # Add entry back with new key
        error_data[new_key] = existing_entry
    else:
        # If excstr is new, create new entry
        # Generate random key
        error_key = generate_random_key()
        
        # Create the new error entry
        error_entry = {
            "stackstr": stackstr,
            "excstr": excstr,
            "err_str": err_str
        }

        # Add the new error entry to the log
        error_data[error_key] = error_entry

        # If we've exceeded max errors, remove the oldest one
        while len(error_data) > MAX_ERRORS:
            oldest_key = next(iter(error_data))
            error_data.pop(oldest_key)

    print(f"[ERROR] Error Logged: {err_str}")
    try: 
        screenmessage('[ERROR] An Internal Error Logged', color=COLOR_SCREENCMD_ERROR, top=True)
    except: 
        pass

    # Check if the new data is the same as the old data
    try:
        if error_data.values() == curr_data.values():
            print("[ERROR] Error data is unchanged, skipping write.")
            return  # Skip writing if data is the same
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet
    except json.JSONDecodeError:
        print("[ERROR] Error decoding existing error log, overwriting.")
    except Exception as e:
        print(f"[ERROR] Error comparing data: {e}")

    # Save the updated error log back to the file
    with open(log_file_path, 'w', encoding='utf-8') as f:
        json.dump(error_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
####### INTERAL EXCEPTION LOG #######

################### Commands Prefix ###################
CMD_MAIN_PREFIX = '-'

open_settings_window = 'orws'
get_help = 'help'
show_error_log_cmd = 'errlog'

open_all_chats_window = 'acw'

update_pb_cmd = 'uppb'

set_config = 'setcfg'
set_config2 = 'cfg'

show_data_cmd = 'shdata'
###
show_data_attr_nickname = 'nick'
show_data_attr_kunci_jawaban = 'qna'
show_data_attr_custom_replies = 'cr'
show_data_attr_blacklist_player = 'pbl'
show_data_attr_player_exception = 'exname'
show_data_attr_muted_player = 'muted'
show_data_attr_exception_anti_abuse_words = 'exword'
show_data_attr_abuse_data = 'ab'
show_data_attrs: list[str] = [
    show_data_attr_nickname, show_data_attr_kunci_jawaban,
    show_data_attr_custom_replies, show_data_attr_blacklist_player,
    show_data_attr_player_exception, show_data_attr_muted_player,
    show_data_attr_exception_anti_abuse_words, show_data_attr_abuse_data
]

add_nick = 'addnick'
remove_nick = 'removenick'
remove_nick2 = 'rmnick'

add_question = 'addq'
remove_question = 'removeq'
remove_question2 = 'rmq'
qna_divider = ':'

add_custom_reply_cmd = 'addcr'
remove_custom_reply_cmd = 'rmcr'
custom_reply_divider = ':'

add_abuse_cmd = 'addab'
remove_abuse_cmd = 'rmab'
abuse_cmd_divider = ':'

add_blacklist = 'addbl'
remove_blacklist = 'rmbl'

add_abuse_exception = 'addexab'
remove_abuse_exception = 'rmexab'

add_name_exception = 'addexname'
remove_name_exception = 'rmexname'

add_warn_cmd = 'addwarn'
decrease_warn_cmd = 'decwarn'
reset_player_warning_cmd = 'resetwarn'
reset_all_player_warning_cmd = 'resetallwarn'

show_current_list_msg = 'pnl'
show_all_list_msg = 'sal'
show_all_list_window = 'wal'
show_session_list_window = 'wsl'
find_player_in_all_list = 'findall'
find_player_in_current_session = 'find'

info_player_in_all_list = 'infoall'
info_player_in_current_session = 'info'

translate_cmd = 'tl'
server_ping_cmd = 'ping'

### Dont Change This ###
translate_output = "[TL]"
message_and_pname_splitter = ": "

################### Commands Prefix ###################

config_name_enable_less_responder         = 'enable'
config_name_soal                            = 'soal'
config_name_add_profile_to_mainname         = 'addprofile'
config_name_smart_2nd_attempt_answer        = 'smartsoal'
config_name_custom_reply                    = 'customreply'
config_name_noob                            = 'noob'
config_name_sus                             = 'sus'
config_name_less                          = 'less'
config_name_bruh                            = 'bruh'
config_name_chat_logging                    = 'logchat'
config_name_logmsg                          = 'logmsg'
config_name_logmsg2                         = 'logmsg2'
config_name_cmdprint                        = 'cmdprint'
config_name_anti_abuse                      = 'antiabuse'
config_name_vote_kick_detect                = 'votekick'
config_name_anti_abuse_chill                = 'chillabuse'
config_name_autokick                        = 'autokick'
config_name_refresh_names                   = 'refreshname'
config_name_only_update_available_pdata     = 'existpdata'
config_name_use_dates_on_chatdata           = 'datechat'
config_name_translate_machine               = 'tl'
config_name_reset_player_warns              = 'resetwarns'
config_name_partial_match_abuses            = 'partialabmatch'
config_name_screenmessage_cmd               = 'screencmd'
config_name_prioritize_bcs_pb               = 'bcspb'
config_name_show_my_master_ping             = 'shping'

# Default Config State And Settings Sort
default_responder_config = {
    config_name_enable_less_responder: False,
    config_name_soal: True,
    config_name_smart_2nd_attempt_answer: False,
    config_name_custom_reply: True,
    config_name_noob: False,
    config_name_sus: False,
    config_name_less: True,
    config_name_bruh: False,
    config_name_chat_logging: True,
    #config_name_use_dates_on_chatdata: False,
    #config_name_logmsg: False,
    config_name_logmsg2: True,
    config_name_cmdprint: False,
    config_name_screenmessage_cmd: True,
    config_name_vote_kick_detect: False,
    config_name_anti_abuse: False,
    config_name_partial_match_abuses: True,
    config_name_anti_abuse_chill: False,
    config_name_autokick: False,
    config_name_reset_player_warns: True,
    #config_name_add_profile_to_mainname: True,
    config_name_refresh_names: False,
    #config_name_only_update_available_pdata: True,
    config_name_prioritize_bcs_pb: True,
    #config_name_translate_machine: True,
    config_name_show_my_master_ping: True
}
responder_config: Dict[str, bool] = {}
"""Global Less Responder Settings,

Usages: `responder_config.get(config_key)` OR `responder_config[config_key]`"""

def get_responder_config_translate_text() -> dict[str, str]:
    config_display_names = {
        config_name_enable_less_responder: get_lang_text('rswEnable'),
        config_name_soal: get_lang_text('rswSoal'),
        config_name_sus: get_lang_text('rswAmongUs'),
        config_name_noob: get_lang_text('rswNoNoobWord'),
        config_name_custom_reply: get_lang_text('rswCustomReplies'),
        config_name_less: get_lang_text('rswAutoGreet'),
        config_name_bruh: get_lang_text('rswBruhIfAmazing'),
        config_name_logmsg: get_lang_text('rswCurrentSessionListLog'),
        config_name_logmsg2: get_lang_text('rswAllNamesListLog'),
        config_name_cmdprint: get_lang_text('rswCmdLogForPC'),
        config_name_anti_abuse: get_lang_text('rswAntiAbuseAutoWarn'),
        config_name_anti_abuse_chill: get_lang_text('rswIncludeChillAbuse'),
        config_name_autokick: get_lang_text('rswAutoKickOnMaxWarns'),
        config_name_refresh_names: get_lang_text('rswRefreshPlayersProfile'),
        config_name_only_update_available_pdata: get_lang_text('rswOnlyUpdateAvailablePData'),
        config_name_chat_logging: get_lang_text('rswChatLogging'),
        config_name_use_dates_on_chatdata: get_lang_text('rswAddDatesAsSeparatorOnChatDataFiles'),
        config_name_translate_machine: get_lang_text('rswTranslateMachine'),
        config_name_reset_player_warns: get_lang_text('rswResetPlayerWarnsEachBoot'),
        config_name_partial_match_abuses: get_lang_text('rswPartialMatchAbuses'),
        config_name_smart_2nd_attempt_answer: get_lang_text('rswBypassAutoAnswerBlocker'),
        config_name_add_profile_to_mainname: get_lang_text('rswAddYourProfileToMainName'),
        config_name_screenmessage_cmd: get_lang_text('rswUseScreenmessageCmdPrompts'),
        config_name_prioritize_bcs_pb: get_lang_text('rswPrioritizePbIdFromBcs'),
        config_name_show_my_master_ping: get_lang_text('rswSendMyPingIfPing'),
        config_name_vote_kick_detect: get_lang_text('rswKickVoterAnalyzer')
    }
    return config_display_names

cmd_toggle_session_pdata_chat = CMD_MAIN_PREFIX + show_current_list_msg
cmd_toggle_all_list_chat = CMD_MAIN_PREFIX + show_all_list_msg
cmd_toggle_all_pdata_window = CMD_MAIN_PREFIX + show_all_list_window
cmd_toggle_findall_pdata = CMD_MAIN_PREFIX + find_player_in_all_list
cmd_toggle_find_pdata = CMD_MAIN_PREFIX + find_player_in_current_session
cmd_toggle_session_pdata_window = CMD_MAIN_PREFIX + show_session_list_window
cmd_toggle_update_pb = CMD_MAIN_PREFIX + update_pb_cmd
cmd_toggle_reset_player_warns = CMD_MAIN_PREFIX + reset_player_warning_cmd
cmd_toggle_reset_all_player_warns = CMD_MAIN_PREFIX + reset_all_player_warning_cmd
cmd_toggle_info_player_current_pdata = CMD_MAIN_PREFIX + info_player_in_current_session
cmd_toggle_info_player_all_pdata = CMD_MAIN_PREFIX + info_player_in_all_list
cmd_toggle_show_data = CMD_MAIN_PREFIX + show_data_cmd
cmd_toggle_ping_server = CMD_MAIN_PREFIX + server_ping_cmd
toggle_show_data = CMD_MAIN_PREFIX + show_data_cmd
toggle_ping_server = CMD_MAIN_PREFIX + server_ping_cmd

toggle_add_questions = CMD_MAIN_PREFIX + add_question
toggle_remove_question = CMD_MAIN_PREFIX + remove_question
toggle_add_nick = CMD_MAIN_PREFIX + add_nick
toggle_remove_nick = CMD_MAIN_PREFIX + remove_nick
toggle_add_custom_replies = CMD_MAIN_PREFIX + add_custom_reply_cmd
toggle_remove_custom_replies = CMD_MAIN_PREFIX + remove_custom_reply_cmd
toggle_add_responder_blacklist = CMD_MAIN_PREFIX + add_blacklist
toggle_remove_responder_blacklist = CMD_MAIN_PREFIX + remove_blacklist
toggle_add_player_anti_abuse_exception = CMD_MAIN_PREFIX + add_name_exception
toggle_remove_player_anti_abuse_exception = CMD_MAIN_PREFIX + remove_name_exception

toggle_reset_player_warns = CMD_MAIN_PREFIX + reset_player_warning_cmd
toggle_reset_all_player_warns = CMD_MAIN_PREFIX + reset_all_player_warning_cmd
toggle_info_player_current_pdata = CMD_MAIN_PREFIX + info_player_in_current_session
toggle_info_player_all_pdata = CMD_MAIN_PREFIX + info_player_in_all_list
toggle_show_data = CMD_MAIN_PREFIX + show_data_cmd
toggle_ping_server = CMD_MAIN_PREFIX + server_ping_cmd
toggle_responder_settings = CMD_MAIN_PREFIX + open_settings_window
toggle_internal_all_chats_window = CMD_MAIN_PREFIX + open_all_chats_window
toggle_show_error_log = CMD_MAIN_PREFIX + show_error_log_cmd
toggle_gethelp = CMD_MAIN_PREFIX + get_help

toggle_kick_player_cmd = CMD_MAIN_PREFIX + 'kick'
toggle_remove_player_cmd2 = CMD_MAIN_PREFIX + 'rm'
toggle_remove_player_cmd = CMD_MAIN_PREFIX + 'remove'

toggle_add_anti_abuse_exception_word = CMD_MAIN_PREFIX + add_abuse_exception
toggle_remove_anti_abuse_exception_word = CMD_MAIN_PREFIX + remove_abuse_exception
toggle_add_abuse = CMD_MAIN_PREFIX + add_abuse_cmd
toggle_remove_abuse = CMD_MAIN_PREFIX + remove_abuse_cmd

all_toggles: list[str] = [
    cmd_toggle_session_pdata_chat, cmd_toggle_all_list_chat, cmd_toggle_all_pdata_window, cmd_toggle_findall_pdata,
    cmd_toggle_find_pdata, cmd_toggle_session_pdata_window, cmd_toggle_update_pb, cmd_toggle_reset_player_warns,
    cmd_toggle_reset_all_player_warns, cmd_toggle_info_player_current_pdata, cmd_toggle_info_player_all_pdata,
    cmd_toggle_show_data, cmd_toggle_ping_server
]

info_msgs = [
    f'Atajo para abrir la ventana de configuración (en el chat): {CMD_MAIN_PREFIX}{open_settings_window}',
    f'El botón de "refresh" actúa como un reinicio de sesión, similar a reiniciar el juego, pero de forma más suave.',
    f'Puedes cambiar configuraciones usando {CMD_MAIN_PREFIX}{set_config} seguido del nombre del ajuste.',
    f'También puedes cambiar el prefijo principal a lo que quieras. Prefijo actual: {CMD_MAIN_PREFIX}',
    f'Hay una función de lista negra para bloquear a cualquier jugador de usar las funciones de este plugin.',
    f'Puedes agregar preguntas usando {CMD_MAIN_PREFIX}{add_question}',
    f'Configura un apodo para saludos automáticos cuando los jugadores te llamen con "ese apodo" usando {CMD_MAIN_PREFIX}{add_nick}',
    f'Existe una función para guardar los nombres y perfiles de los jugadores.',
    f'Usa {CMD_MAIN_PREFIX}{find_player_in_current_session} para buscar datos de jugadores desde que abriste BombSquad.',
    f'Usa {CMD_MAIN_PREFIX}{show_session_list_window} para abrir la lista de sesión en una ventana.',
    f'Usa {CMD_MAIN_PREFIX}{find_player_in_all_list} para buscar datos de jugadores desde que empezaste a usar este plugin.',
    f'Usa {CMD_MAIN_PREFIX}{show_all_list_window} para abrir la lista completa de nombres en una versión con ventana.',
    f'Usa {CMD_MAIN_PREFIX}{show_current_list_msg} para enviar la lista actual (del servidor) en el chat.',
    f'Usa {CMD_MAIN_PREFIX}{show_all_list_msg} para enviar la lista completa de nombres en el chat. Evita usarlo en un servidor.',
    f'Usa {CMD_MAIN_PREFIX}{add_abuse_cmd} y {CMD_MAIN_PREFIX}{remove_abuse_cmd} para agregar o eliminar abusos.',
    f'Usa {CMD_MAIN_PREFIX}{add_abuse_exception} para añadir palabras de excepción a los abusos.',
    f'Usa {CMD_MAIN_PREFIX}{add_name_exception} para añadir jugadores/cuentas de excepción a los abusos.',
    f'Otros comandos relacionados con anti-abuso: {CMD_MAIN_PREFIX}{add_warn_cmd}, {CMD_MAIN_PREFIX}{decrease_warn_cmd}, {CMD_MAIN_PREFIX}{reset_player_warning_cmd}, {CMD_MAIN_PREFIX}{reset_all_player_warning_cmd}',
    f'Las respuestas personalizadas ({CMD_MAIN_PREFIX}{add_custom_reply_cmd}) permiten personalizar el texto:',
    f'$name (perfil), $acc (nombre de cuenta), $cid (client id), y ($unamused & $happy) son emojis.',
    f'{CMD_MAIN_PREFIX}{translate_cmd} sirve para traducir, soporta hasta 4 casos.',
    f'Usa {CMD_MAIN_PREFIX}{update_pb_cmd} para fusionar todos los datos de la lista con la base de jugadores del servidor (si está disponible).',
    f'Ahora puedes buscar usando listas con ventana, similar a {CMD_MAIN_PREFIX}{find_player_in_current_session}.',
    f'Los comandos para agregar cosas relacionadas con nombres de cuenta admiten coincidencias parciales, así que usa letras más específicas,',
    f'y hazlo antes de cerrar BS, ya que los datos de jugador se pierden al cerrar el juego.',
    f'Hacer coincidir puede ser problemático, pero intentaré arreglarlo en futuras actualizaciones.',
    f'Al reiniciar se eliminan todos los archivos guardados (excepto {saved_names_file_name}) y se crean nuevos.',
    f'Muestra los mensajes recientes ampliados con {CMD_MAIN_PREFIX}{open_all_chats_window}',
    f'Usa {CMD_MAIN_PREFIX}{info_player_in_current_session} para obtener la ventana de información del jugador.',
    f'{config_name_partial_match_abuses} es para coincidencias parciales de abusos en lugar de coincidencias exactas.',
    f'La configuración \"{config_name_screenmessage_cmd}\" sirve para mostrar el resultado del comando como ScreenMessage en lugar de enviarlo al chat.',
    f'La configuración \"{config_name_show_my_master_ping}\" envía tu ping automáticamente si tú o alguien usa /ping.',
    f'Todos los datos se guardan en:',
    f'{str(responder_directory)}',
    f'No olvides cambiar el nombre del propietario para tener permiso de uso y actualizar tus apodos.',
    f'Si no usas PC, desactiva {config_name_cmdprint} para reducir el lag.',
    f'Descargo de responsabilidad: este plugin no puede hacer coincidencias de nombres de jugadores con 100% de precisión. Nombres complicados, nombres duplicados,',
    f'o con puntos pueden causar errores o imprecisiones y provocar que algunos atributos se vuelvan inútiles o inestables.',
    f'Revisa dos veces cualquier dato incorrecto o inexacto relacionado con nombres de jugadores.'
]

###### INTERNAL CHATS DATA ######
internal_player_chats_data: Dict[str, list[str]] = {}
internal_all_chats_data: List[str] = []
"""An expanded get_chat_messages"""
def load_internal_chats_data(read_only:bool = False) -> Dict[str, list[str]]:
    global internal_player_chats_data
    try:
        if os.path.exists(internal_chats_data_file_path):
            with open(internal_chats_data_file_path, 'r', encoding='utf-8') as file:
                if read_only: return json.load(file)
                internal_player_chats_data = json.load(file)
        else:
            if not os.path.exists(responder_directory):
                os.makedirs(responder_directory)
            internal_player_chats_data = {}  # Empty by default
            if not os.path.exists(internal_chats_data_file_folder_path):
                os.makedirs(internal_chats_data_file_folder_path)
            with open(internal_chats_data_file_path, 'w') as f:
                json.dump(internal_player_chats_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
            babase.pushcall(Call(screenmessage, "Created Internal Chat Data File", COLOR_SCREENCMD_ERROR), from_other_thread=True)
    except Exception as e:
     #   babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error On Internal Chat Data Load: {e}", color=COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print('ERROR ' + str(e))
    return internal_player_chats_data

def load_internal_all_chats_data(read_only:bool = False) -> List[str]:
    global internal_all_chats_data
    try:
        if os.path.exists(internal_all_chats_data_file_path):
            with open(internal_all_chats_data_file_path, 'r', encoding='utf-8') as file:
                if read_only: return json.load(file)
                internal_all_chats_data = json.load(file)
        else:
            if not os.path.exists(responder_directory):
                os.makedirs(responder_directory)
            internal_all_chats_data = []  # Empty by default
            if not os.path.exists(internal_chats_data_file_folder_path):
                os.makedirs(internal_chats_data_file_folder_path)
            with open(internal_all_chats_data_file_path, 'w') as f:
                json.dump(internal_all_chats_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
            babase.pushcall(Call(screenmessage, "Created Internal All Chat Data File", COLOR_SCREENCMD_ERROR), from_other_thread=True)
    except Exception as e:
     #   babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error On Internal All Chat Data Load: {e}", color=COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print('ERROR ' + str(e))
    return internal_all_chats_data

internal_data_saving_call = 0
internal_data_saving_ratio = 5
def save_internal_player_chats_data(force: bool = False):
    global internal_data_saving_call
    internal_data_saving_call += 1
    if not force and not internal_data_saving_call > internal_data_saving_ratio: return
    internal_data_saving_call = 0
    now_data = internal_player_chats_data
    if now_data and list(now_data) != list(load_internal_chats_data(read_only=True)):
        with open(internal_chats_data_file_path, 'w') as f:
            json.dump(internal_player_chats_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)

def save_internal_all_chats_data(force: bool = False) -> None:
    global internal_data_saving_call
    internal_data_saving_call += 1
    if not force and not internal_data_saving_call > internal_data_saving_ratio: return
    internal_data_saving_call = 0
    now_data = internal_all_chats_data
    if now_data and now_data != load_internal_all_chats_data(read_only=True):
        with open(internal_all_chats_data_file_path, 'w') as f:
            json.dump(internal_all_chats_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)

####### Log Chats #######
def load_json_chats_data() -> Dict[str, list[str]]:
    chat_data: Dict[str, list[str]] = {}
    if os.path.exists(chats_data_file_path):
        try:
            with open(chats_data_file_path, 'r') as f:
                chat_data = json.load(f)
        except Exception as e:
            print_internal_exception(e)
            #try:
                #os.remove(chats_data_file_path)
            #except Exception as e:
                #print_internal_exception(e)
    else:
        babase.pushcall(Call(screenmessage, "Created Chat Logger Files", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        chat_data = {}
    return chat_data
####### Log Chats #######

###### INTERNAL CHATS DATA ######

########################## ALL NAMES ##########################
all_names: Dict[str, dict[str, Any]] = {}
"""The Simplified List Of Saved Players Data Externally (From File).
Every Players Met `Since Using This Plugin` (As Long The File Not Deleted).

Needs `_get_player_info`

Format: `{"name": dict[str, Any]}`

Available Data:
`profile_name`, `client_id`, `last_met`, `mutual_server`

Other:
`pb_id`, `searched_bcs`, `_id`, `accounts`, `current_premium_profile`,
`createdOn`, `updatedOn`, `discord`, `spaz`
"""

current_session_namelist: Dict[str, dict[str, Any]] = {}
"""The Simplified List Of Saved Players Data.
Every Players Met `Since BS Opened`.
Usually used for adding `Other` player condition that is not necessary
to be saved to file.

Needs `_get_player_info`

Format: `{"name": dict[str, Any]}`

Available Data:
`profile_name`, `client_id`

Other:
`greeted`
"""

current_namelist: Dict[str, dict[str, Any]] = {}
"""The Simplified List Of Saved Players Data.
Players Met `In Server Only` (Resets Everytime).
Good for improving matching name accuracy.

Needs `_get_player_info`

Format: `{"name": dict[str, Any]}`

Available Data:
`profile_name`, `client_id`
"""

###### GETTING FILE SIZE ######
def get_file_size_bytes(file_path: str):
    """Mengembalikan ukuran file dalam bytes.

    Args:
        file_path: Jalur lengkap ke file.

    Returns:
        Ukuran file dalam bytes.
    """

    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        print("File tidak ditemukan.")
        return None

def get_file_size(file_path: str, use_mb: bool = False) -> float | None:
    """Mengembalikan ukuran file dalam format MB atau KB.

    Args:
        file_path: Jalur lengkap ke file.

    Returns:
        String yang berisi ukuran file dalam format yang mudah dibaca.
    """

    size_in_bytes = get_file_size_bytes(file_path)
    if size_in_bytes is not None:
        size = size_in_bytes

        if use_mb and size_in_bytes >= 1048576:
            size = size_in_bytes / 1048576
        else:
            size = size_in_bytes / 1024
        return size

    else:
        return None
###### GETTING FILE SIZE ######

def zip_files_with_extension(input_path: str, output_path: str, file_extension: str = ".json", file_format: str="zip", use_temp_folder: bool = False) -> None:
    """Zips files with a specific extension from a folder.

    Args:
        input_path: The path to the folder containing the files.
        output_path: The path to save the zipped file.
        file_extension: The extension of the files to zip (e.g., ".json").
        file_format: The format of the archive (e.g., "zip", "tar", "gztar", "bztar").
        use_temp_folder: Whether use temporary folder for zipping. (extension will be ignored if False)
    """
    try:
        if use_temp_folder:
            # Create a temporary directory to hold the files to be zipped
            temp_dir = os.path.join(cache_folder_path, "temp_zip")
            os.makedirs(temp_dir, exist_ok=True)
            os.makedirs(output_path, exist_ok=True)

            # Copy files with the specified extension to the temporary directory
            for filename in os.listdir(input_path):
                if filename.endswith(file_extension):
                    input_file = os.path.join(input_path, filename)
                    output_file = os.path.join(temp_dir, filename)
                    shutil.copy2(input_file, output_file)  # copy2 preserves metadata

            try:
                # Create the archive from the temporary directory
                shutil.make_archive(output_path, file_format, temp_dir)
            except OSError as e:
                if e.errno == 1:  # Operation not permitted
                    # If archive creation is not permitted, copy files directly to output path
                    for filename in os.listdir(temp_dir):
                        src_file = os.path.join(temp_dir, filename)
                        dst_file = os.path.join(output_path, filename)
                        shutil.move(src_file, dst_file)
                else:
                    raise e # Re-raise other OSError exceptions

            # Remove the temporary directory
            shutil.rmtree(temp_dir)
        else:
            # Directly create archive from input path
            os.makedirs(output_path, exist_ok=True)

            try:
                shutil.make_archive(output_path, file_format, input_path)
            except OSError as e:
                if e.errno == 1:
                    for filename in os.listdir(input_path):
                        src_file = os.path.join(input_path, filename)
                        dst_file = os.path.join(output_path, filename)
                        shutil.copy2(src_file, dst_file)
                else:
                    raise e

    except Exception as e:
        print_internal_exception(e)

def backup_all_names_data():
    """Backups all names data to a zip file based on a specified interval. Should be on another `Thread`"""
    global party_config

    # Define the backup interval in days

    last_backup_date_str = party_config.get(CFG_NAME_LAST_ALL_NAMES_BACKUP)
    
    if last_backup_date_str:
        try:
            last_backup_date = datetime.strptime(last_backup_date_str, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format in config. Resetting backup date.")
            last_backup_date = None
            party_config[CFG_NAME_LAST_ALL_NAMES_BACKUP] = datetime.now().strftime("%d-%m-%Y")
    else:
        last_backup_date = None
        party_config[CFG_NAME_LAST_ALL_NAMES_BACKUP] = datetime.now().strftime("%d-%m-%Y")
    
    current_date = datetime.now()

    if not last_backup_date or (current_date - last_backup_date).days >= backup_interval:
        print("Backing up all names data...")
        babase.pushcall(Call(screenmessage, get_lang_text('backupAllNamesStart'), COLOR_SCREENCMD_NORMAL), from_other_thread=True)
        if last_backup_date:
            days_since_last_backup = (current_date - last_backup_date).days
            print(f"Last backup {days_since_last_backup} day(s) ago")
        try:
            # Ensure the backup directory exists
            if not os.path.exists(all_players_data_backup_folder_path):
                os.makedirs(all_players_data_backup_folder_path)
                babase.pushcall(Call(screenmessage, f"Created backup directory: {all_players_data_backup_folder_path}", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                print(f"Created backup directory: {all_players_data_backup_folder_path}")

            # Zip the all players data folder
            zip_files_with_extension(all_players_data_folder_path, (os.path.join(all_players_data_backup_folder_path, f"AllNamesBackup")))

            # Update the last backup date in the config
            party_config[CFG_NAME_LAST_ALL_NAMES_BACKUP] = current_date.strftime("%d-%m-%Y")
            save_party_config(party_config)
            babase.pushcall(Call(screenmessage, get_lang_text('backupAllNamesSuccess'), COLOR_SCREENCMD_NORMAL), from_other_thread=True)
            print("All names data backed up successfully.")
        except Exception as e:
            babase.pushcall(Call(screenmessage, get_lang_text('backupAllNamesFailed'), COLOR_SCREENCMD_NORMAL), from_other_thread=True)
            print_internal_exception(f"Error backing up all names data: {e}")
    else:
        days_since_last_backup = (current_date - last_backup_date).days
        if responder_config.get(config_name_cmdprint):
            print(f"All names data already backed up within the last {backup_interval} day(s). ({days_since_last_backup} day(s) ago)")


saved_names_file_part_separator = " Part "
saved_player_data_is_error = False
identical_all_names = False
def load_all_names_data():
    """Load saved Players Data from File and store it to a `global` variable `all_names`"""
    global all_names, identical_all_names
    updated = False
    loaded_all_names: Dict[str, dict[str, Any]] = {}
    
    def update_player_data(name: str, data: dict[str, Any]) -> bool:
        """Helper function to update player data fields"""
        nonlocal updated
        profile = data.get('profile_name')
        if profile:
            if isinstance(profile, str) and ', ' in profile:
                loaded_all_names[name]['profile_name'] = profile.split(', ')
                updated = True
            elif not isinstance(profile, list):
                loaded_all_names[name]['profile_name'] = [str(profile)] if profile else []
                updated = True
        elif profile is None:
            loaded_all_names[name]['profile_name'] = []
            updated = True
            
        if not data.get('client_id'):
            loaded_all_names[name]['client_id'] = "?"
            updated = True
            
        if loaded_all_names[name].get('_id') and loaded_all_names[name].get('searched_bcs') is None:
            loaded_all_names[name]['searched_bcs'] = True
            updated = True
            
        mutual_server = loaded_all_names[name].get('mutual_server')
        if mutual_server and not isinstance(mutual_server, list):
            loaded_all_names[name]['mutual_server'] = [mutual_server]
            updated = True
            
        return updated

    def move_to_backup(file_path: str, file_name: str) -> None:
        """Helper function to move files to backup folder"""
        try:
            if not os.path.exists(all_players_data_backup_folder_path):
                os.makedirs(all_players_data_backup_folder_path)
                print(f"Created backup directory: {all_players_data_backup_folder_path}")

            backup_file_path = os.path.join(all_players_data_backup_folder_path, file_name)
            shutil.move(file_path, backup_file_path)
            print(f"Moved all names file to backup: {file_name} -> {backup_file_path}")
        except Exception as e:
            print_internal_exception(f"Error moving all names file to backup: {e}")

    try:
        os.makedirs(all_players_data_folder_path, exist_ok=True)
        files = [f for f in os.listdir(all_players_data_folder_path) 
                if os.path.isfile(os.path.join(all_players_data_folder_path, f)) 
                and f.startswith(saved_names_file_name) 
                and f.endswith(".json")]

        for file_name in files:
            file_path = os.path.join(all_players_data_folder_path, file_name)
            try:
                if saved_names_file_part_separator not in file_name:
                    if len(files) == 1:
                        print(f"Only one file found without separator, reading: {file_name}")
                        with open(file_path, 'r', encoding='utf-8') as file:
                            file_data: Dict[str, dict[str, Any]] = json.load(file)
                            for name, data in file_data.items():
                                if name not in loaded_all_names:
                                    loaded_all_names[name] = data
                                    update_player_data(name, data)
                        
                        start_save_all_names(updated_from_load=True, force=True).start()
                        move_to_backup(file_path, file_name)
                        continue
                    
                    if responder_config.get(config_name_cmdprint):
                        print(f"Skipping Non Separated All Names Data: {file_name}")
                    move_to_backup(file_path, file_name)
                    continue

                if responder_config.get(config_name_cmdprint):
                    print(f"Reading Saved All Names Data File: {file_name}")
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_data: Dict[str, dict[str, Any]] = json.load(file)
                    for name, data in file_data.items():
                        if name not in loaded_all_names:
                            loaded_all_names[name] = data
                            update_player_data(name, data)
            except Exception as e:
                print_internal_exception(e)
                print(f"Error loading all names data from {file_name}")

        if loaded_all_names:
            if len(loaded_all_names) < len(all_names):
                print("Loaded all names data has fewer entries than the current all_names. Forcing a save.")
                start_save_all_names(updated_from_load=True, force=True).start()
            else:
                if all_names != loaded_all_names:
                    all_names = loaded_all_names
                else:
                    print("Loaded all names data is identical to current all_names. No changes needed.")
                identical_all_names = True

        if updated:
            _save_names_to_file(updated_from_load=True)
    except Exception as e:
        global saved_player_data_is_error
        saved_player_data_is_error = True
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error On All Names Data Load: {e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print_internal_exception(e)

_special_msg_sent = False
class start_save_all_names:
    """Save Player Names"""
    def __init__(self, updated_from_load:bool=False, force:bool=False):
        super().__init__()
        self.updated_from_load = updated_from_load
        self.force = force
        self.threaded = False
        self._last_shown_messages: Dict[str, str] = {}

    def start_threaded(self):
        self.threaded = True
        Thread(target=self.start).start()

    def start(self):
        global all_names, _special_msg_sent, is_saving_all_names_data
        players_count = 0
        try:
            if is_saving_all_names_data:
                print("Saving All Names Func Called Again While Not Done Saving Data (Internal), Returning..")
                return
            if not self.force:
                # Load data from existing files
                all_names_loaded = {}
                for filename in glob.glob(all_players_data_folder_path + saved_names_file_name + saved_names_file_part_separator + "*.json"):
                    try:
                        with open(filename, 'r') as file:
                            file_data = json.load(file)
                            all_names_loaded.update(file_data)
                    except Exception as e:
                        print_internal_exception(e)
                        print(f"Error loading data from {filename}")

                if all_names_loaded == all_names:
                    pass
                    #print('Save All Names Data (Function) Called While There Are No Changes, Returning..')
                    return
                if not self.force and len(all_names) < len(all_names_loaded):
                    print(f"Uh oh, Shorter All Names data wants to be saved, reloading All Names data")
                    load_all_names_data()
                    return

            is_saving_all_names_data = True
            # Determine the appropriate file based on number of players
            players_count = len(all_names)
            start_index = 0

            # Get list of existing files
            existing_files = sorted(glob.glob(all_players_data_folder_path + saved_names_file_name + saved_names_file_part_separator + "*.json"))
            
            # Calculate total files needed based on max players per file
            total_files = (players_count + max_players_on_all_names_file - 1) // max_players_on_all_names_file

            # Check if file exists and load existing data
            existing_data = {}

            # Iterate through each file
            for file_index in range(total_files):
                # Calculate start and end indices for current file
                start_index = file_index * max_players_on_all_names_file
                end_index = min(start_index + max_players_on_all_names_file, players_count)

                # Generate correct file name and path
                correct_file_name = saved_names_file_name + f"{saved_names_file_part_separator}{file_index+1}.json"
                correct_file_path = all_players_data_folder_path + correct_file_name

                # Check if using existing file
                if file_index < len(existing_files):
                    existing_file_path = existing_files[file_index]
                    existing_file_name = os.path.basename(existing_file_path)

                    # If existing file has wrong index, rename it
                    if existing_file_name != correct_file_name:
                        try:
                            os.rename(existing_file_path, correct_file_path)
                            print(f"Renamed {existing_file_name} to {correct_file_name}")
                        except Exception as e:
                            print(f"Error renaming {existing_file_name} to {correct_file_name}: {e}")
                    file_path = correct_file_path
                else:
                    # Create new file with correct index
                    file_path = correct_file_path

                # Get slice of data for current file
                current_data = dict(list(all_names.items())[start_index:end_index])

                try:
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            existing_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error loading existing data from {correct_file_name}:\n{e}\n")

                # Only save if data has changed or if it's a new file
                if current_data != existing_data or not os.path.exists(file_path):
                    try:
                        # Ensure directory exists
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)

                        # Save data with proper encoding and formatting
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(current_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
                        print(f"Successfully saved {len(current_data)} players to {correct_file_name}")
                    except Exception as e:
                        print(f"Error saving data to {file_path}: {e}")
                else:
                    print(f"No changes detected in {correct_file_name}, skipping save")

            # Clean up any extra files if total_files decreased
            for extra_file in existing_files[total_files:]:
                try:
                    os.remove(extra_file)
                    print(f"Removed extra file: {os.path.basename(extra_file)}")
                except Exception as e:
                    print(f"Error removing extra file {extra_file}: {e}")
        except Exception as e:
            print_internal_exception(e)

        is_saving_all_names_data = False
        print("All Names Data Saved To File")
        #try:
        #except Exception as e:
            #print_internal_exception(e)

        try:
            screen_message_color = (1, 0.1, 0.35)
            _special_msg_sent = True

            msg_range = None
            if players_count >= 100 and players_count <= 120:
                msg_range = '100-120'
                msg = get_lang_text("savePlayerDataHappyMsg1").format(str(players_count))
            elif players_count >= 200 and players_count <= 220:
                msg_range = '200-220'
                msg = get_lang_text("savePlayerDataHappyMsg2").format(str(players_count))
            elif players_count >= 500 and players_count <= 520:
                msg_range = '500-520'
                msg = get_lang_text("savePlayerDataHappyMsg3").format(str(players_count))
            elif players_count >= 1000 and players_count <= 1020:
                msg_range = '1000-1020'
                msg = get_lang_text("savePlayerDataHappyMsg4").format(str(players_count))
            else:
                _special_msg_sent = False
                return

            if msg_range and self._last_shown_messages.get(msg_range) != msg:
                if self.threaded:
                    babase.pushcall(Call(screenmessage, msg, screen_message_color), from_other_thread=True)
                else:
                    screenmessage(msg, screen_message_color)

                self._last_shown_messages[msg_range] = msg
        except Exception as e:
            print_internal_exception(e)

is_saving_all_names_data = False
def _save_names_to_file(updated_from_load:bool=False):
    """Start Saving All Names Thread"""
    if is_saving_all_names_data:
        print("Saving All Names Func Called Again While Not Done Saving Data, Returning..")
        #_babase.print_context()
        return
    start_save_all_names(updated_from_load).start_threaded()
########################## ALL NAMES ##########################

####### PARTY WINDOW MAIN SETTINGS #######
CFG_NAME_CHAT_MUTED = 'Chat Muted' # Screenmessage Chat Texts
CFG_NAME_PARTY_CHAT_MUTED = 'Party Chat Muted' # PartyWindow Chat Texts

CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD = 'Translate TextField Source'
CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD = 'Translate TextField Destination'

CFG_NAME_TRANSLATE_SOURCE_OTHER = 'Translate Other Text Source'
CFG_NAME_TRANSLATE_DESTINATION_OTHER = 'Translate Other Text Destination'

CFG_NAME_TRANSLATE_PREFERRED_MACHINE = 'Preffered Translate Machine'

CFG_NAME_MAIN_COLOR = 'PartyWindow Main Color'
CFG_NAME_MESSAGE_NOTIFICATION_POS = 'Message Notification'

CFG_NAME_PREFFERED_LANG = 'Party Window Language'

##### CUSTOM #####
CFG_NAME_ACCURATE_SERVER_PING_SEND = 'Accurate Server Ping Send'

CFG_NAME_BUTTON_PING = 'Ping Button'
CFG_NAME_BUTTON_IP = 'IP Button'
CFG_NAME_BUTTON_COPY_PASTE = 'Copy Paste Button'
CFG_NAME_INSTANT_QUICK_RESPOND = 'Instant Quick Respond'

CFG_NAME_AUTO_GREET_FRIENDS = 'Auto Greet Friends'
CFG_NAME_AUTO_GREET_FRIENDS_IF_MASTER_JOINED = 'Auto Greet Friends If Master Joined'
CFG_NAME_AUTO_GREET_FRIENDS_IF_FRIENDS_JOINED = 'Auto Greet Friends If They Joined'

CFG_NAME_DIRECT_CUSTOM_CMD = 'Direct Custom CMD'
CFG_NAME_BLOCK_NA_CMD = 'Block Unknown Internal Commands'
CFG_NAME_ASK_GAME_REPLAY_NAME = 'Ask Game Replay Name'
CFG_NAME_COLORFUL_CHATS = 'Colorful Chats'
CFG_NAME_FOCUS_TO_LAST_MSG = 'Auto Focus To Last Message'

CFG_NAME_HIGHLIGHT_CHOSEN_TEXT = 'Highlight Chosen Text'
CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT = 'Include Player Name On Chosen Text'
CFG_NAME_INCLUDE_CID_IN_QC_NAME_CHANGER = 'Include Client ID On Quick Name Changer'
CFG_NAME_SAVE_LAST_TYPED_MSG = 'Save Last Message Typed'

CFG_NAME_MODIFIED_SCREENMESSAGE = 'Modified Chat Screenmessage'
CFG_NAME_CHAT_NAME_VIEWER_IN_SCRMSG = 'Chat Name Viewer In Screenmessage'
CFG_NAME_COLORFUL_SCRMSG = 'Colorful Screenmessage'

CFG_NAME_PLUGIN_FRESH_USAGE_TIME = "LessPartyWindow Fresh Usage Time"
CFG_NAME_LAST_ALL_NAMES_BACKUP = "Last All Names Data Backup"
##### CUSTOM #####

CFG_NAME_CHAT_VIEWER_SHOW_CID = 'Show Client ID'
CFG_NAME_CHAT_VIEWER_TYPE = 'Chats Name Viewer'

chat_view_type_profile_name = 'profile'
chat_view_type_account_name = 'account'
chat_view_type_multi = 'multi'
chat_view_type_multi_v2 = 'multi_v2'
# Default Config State And Sort
default_party_config: Dict[str, Any] = {
    CFG_NAME_DIRECT_CUSTOM_CMD: False,
    CFG_NAME_INSTANT_QUICK_RESPOND: True,
    CFG_NAME_HIGHLIGHT_CHOSEN_TEXT: True,
    CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT: False,
    CFG_NAME_SAVE_LAST_TYPED_MSG: True,
    CFG_NAME_INCLUDE_CID_IN_QC_NAME_CHANGER: True,
    CFG_NAME_FOCUS_TO_LAST_MSG: True,
    CFG_NAME_CHAT_MUTED: False,
    CFG_NAME_PARTY_CHAT_MUTED: False,
    CFG_NAME_COLORFUL_CHATS: True,
    CFG_NAME_MODIFIED_SCREENMESSAGE: True,
    CFG_NAME_CHAT_NAME_VIEWER_IN_SCRMSG: True,
    CFG_NAME_COLORFUL_SCRMSG: True,
    CFG_NAME_CHAT_VIEWER_SHOW_CID: False,
    CFG_NAME_CHAT_VIEWER_TYPE: False,
    CFG_NAME_ACCURATE_SERVER_PING_SEND: False,
    CFG_NAME_BUTTON_PING: True,
    CFG_NAME_BUTTON_IP: True,
    CFG_NAME_BUTTON_COPY_PASTE: True,
    CFG_NAME_AUTO_GREET_FRIENDS: True,
    CFG_NAME_AUTO_GREET_FRIENDS_IF_MASTER_JOINED: True,
    CFG_NAME_AUTO_GREET_FRIENDS_IF_FRIENDS_JOINED: True,
    CFG_NAME_BLOCK_NA_CMD: True,
    CFG_NAME_ASK_GAME_REPLAY_NAME: True,
    CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD: 'auto',
    CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD: 'en',
    CFG_NAME_TRANSLATE_SOURCE_OTHER:'auto',
    CFG_NAME_TRANSLATE_DESTINATION_OTHER:'en',
    CFG_NAME_TRANSLATE_PREFERRED_MACHINE: 'api',
    CFG_NAME_PREFFERED_LANG: '',
    CFG_NAME_MESSAGE_NOTIFICATION_POS: 'bottom',
    CFG_NAME_MAIN_COLOR: (0.15, 0.30, 0.45),
    CFG_NAME_PLUGIN_FRESH_USAGE_TIME: datetime.now().strftime("%d-%m-%Y"),
    CFG_NAME_LAST_ALL_NAMES_BACKUP: datetime.now().strftime("%d-%m-%Y")
    
}

party_config: Dict[str, Any] = {}
"""Global Less Party Window Main Settings,

Usages: `party_config.get(config_key)` OR `party_config[config_key]`"""

def load_party_config(is_from_backup: bool=False, read_only: bool=False) -> Dict[str, Any]:
    """Load the party configuration from the file if it exists, else create it with default values"""
    global party_config
    try:
        if os.path.exists(config_party_file_path):
            # Load the config from the file
            updated = False
            with open(config_party_file_path, 'r') as file:
                party_config = json.load(file)

            # Validate config: Remove any keys that are not in default_party_config
            if not read_only:
                keys_to_remove = []
                for key in party_config:
                    if key not in default_party_config:
                        keys_to_remove.append(key)

                for key in keys_to_remove:
                    screenmessage(f"{get_lang_text('partyConfigLoadRemoveKey')}: {key}", color=COLOR_SCREENCMD_ERROR)
                    del party_config[key]
                    if not updated: updated = True

                # Ensure all default configs are present, if not, add them
                for default_key, default_value in default_party_config.items():
                    if default_key not in party_config:
                        screenmessage(f"{get_lang_text('partyConfigLoadAddKey')}: {default_key}", color=COLOR_SCREENCMD_NORMAL)
                        party_config[default_key] = default_value
                        if not updated: updated = True

                if updated:
                    save_party_config(party_config)
                # Save the updated configuration with valid keys
            return party_config
        else:
            # If the file doesn't exist, create it with default values
            if not os.path.exists(party_window_directory):
                os.makedirs(party_window_directory)  # Create the main directory if it doesn't exist
            save_party_config(default_party_config, first_boot=True)  # Save the default config into a file
            party_config = default_party_config
            return default_party_config
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} {get_lang_text('partyConfigLoadError')}: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
        try:
            if os.path.exists(config_party_file_path):
                if os.path.isfile(config_party_file_path):
                    os.remove(config_party_file_path)
                    if not is_from_backup: load_party_config(is_from_backup=True)
        except Exception as e: print_internal_exception(e)
    party_config = default_party_config
    return default_party_config

def save_party_config(config: dict[str, Any], first_boot: bool = False, force:bool=False):
    """Save the current PartyWindow configuration to a file"""
    global party_config
    try:
        if (not force and (not first_boot and load_party_config(read_only=True) == config)) or not config:
            return
        with open(config_party_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
            party_config = config
    except FileNotFoundError:
        with open(config_party_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print_internal_exception(e)

def update_party_config(key: str, value: Any):
    """Update a specific key in the configuration file"""
    global party_config
    if not party_config: load_party_config()
    if party_config and key in party_config:
        party_config[key] = value
        save_party_config(party_config)
        load_party_config()
####### PARTY WINDOW MAIN SETTINGS #######

###################### RESPONDER SETTINGS ######################
def load_responder_config(is_from_backup: bool=False, read_only: bool=False):
    """Load the configuration from the file if it exists, else create it with default values"""
    global responder_config
    try:
        if os.path.exists(config_responder_file_path):
            # Load the config from the file
            updated = False
            with open(config_responder_file_path, 'r') as file:
                responder_config = json.load(file)

            # Validate config: Remove any keys that are not in default_responder_config
            if not read_only:
                keys_to_remove = []
                for key in responder_config:
                    if key not in default_responder_config:
                        keys_to_remove.append(key)

                for key in keys_to_remove:
                    screenmessage(f"{get_lang_text('responderConfigLoadRemoveKey')}: {key}", color=COLOR_SCREENCMD_ERROR)
                    del responder_config[key]
                    if not updated: updated = True

                # Ensure all default configs are present, if not, add them
                for default_key, default_value in default_responder_config.items():
                    if default_key not in responder_config:
                        screenmessage(f"{get_lang_text('responderConfigLoadAddKey')}: {default_key}", color=COLOR_SCREENCMD_ERROR)
                        responder_config[default_key] = default_value
                        if not updated: updated = True
                if updated:
                    save_responder_config(responder_config)
            # Save the updated configuration with valid keys
            return responder_config
        else:
            # If the file doesn't exist, create it with default values
            if not os.path.exists(responder_directory):
                os.makedirs(responder_directory)  # Create the main directory if it doesn't exist
            save_responder_config(default_responder_config, first_boot=True)  # Save the default config into a file
            responder_config = default_responder_config
            return default_responder_config
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} {get_lang_text('responderConfigLoadError')}: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
        try:
            if os.path.exists(config_responder_file_path):
                if os.path.isfile(config_responder_file_path):
                    os.remove(config_responder_file_path)
                    if not is_from_backup: load_responder_config(is_from_backup=True)
        except Exception as e: print_internal_exception(e)
    responder_config = default_responder_config
    return default_responder_config

def save_responder_config(config: Dict[str, bool], first_boot: bool = False, force:bool=False):
    """Save the current PartyWindow configuration to a file"""
    global responder_config
    try:
        if (not force and (not first_boot and load_responder_config(read_only=True) == config)) or not config:
            return
        with open(config_responder_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
            responder_config = config
    except FileNotFoundError:
        with open(config_responder_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print_internal_exception(e)

def update_responder_config(key: str, value: bool):
    """Update a specific key in the configuration file"""
    global responder_config
    if not responder_config: load_responder_config()
    if key in responder_config and isinstance(value, bool):
        responder_config[key] = value
        save_responder_config(responder_config)
        load_responder_config()
###################### RESPONDER SETTINGS ######################

#################### KUNCI JAWABAN DATA ####################
kunci_jawaban: Dict[str, str] = {}
def _load_saved_kunci_jawaban(cmd:bool=False):
    """Load or initialize kunci jawaban from a file"""
    global kunci_jawaban
    updated = False
    try:
        if os.path.exists(kunci_jawaban_file_path):
            with open(kunci_jawaban_file_path, 'r', encoding='utf-8') as file:
                kunci_jawaban = json.load(file)
                """if not sync_kunci_jawaban_default_with_file or cmd: return kunci_jawaban
                for soal, jawaban_default in kunci_jawaban_default.items():
                    if soal in kunci_jawaban:
                        if kunci_jawaban[soal] != jawaban_default:
                            kunci_jawaban[soal] = jawaban_default
                            if not updated: updated = True

                    elif not soal in kunci_jawaban:
                        kunci_jawaban[soal] = jawaban_default
                        if not updated: updated = True
                if updated:
                    _save_kunci_jawaban_to_file(kunci_jawaban)"""
                return kunci_jawaban
        else:
            if not os.path.exists(responder_directory):
                os.makedirs(responder_directory)
            kunci_jawaban = kunci_jawaban_default
            _save_kunci_jawaban_to_file(kunci_jawaban_default)
            screenmessage("Created Default Questions And Answers File", color=COLOR_SCREENCMD_NORMAL)
            if kunci_jawaban: return kunci_jawaban
            return kunci_jawaban_default
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Server QnA Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    if kunci_jawaban: return kunci_jawaban 
    return kunci_jawaban_default

def _save_kunci_jawaban_to_file(data: Dict[str, str]):
    global kunci_jawaban
    with open(kunci_jawaban_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    _load_saved_kunci_jawaban(cmd=True)  # Load the updated list immediately
#################### KUNCI JAWABAN DATA ####################

#################### NICK NAMES DATA ####################
my_nick_names: List[str] = []
def _load_nicknames() -> list[str]:
    """Load nicknames from the file or return the default list"""
    global my_nick_names
    try:
        updated = False
        if os.path.exists(nickname_file_path):
            with open(nickname_file_path, 'r', encoding='utf-8') as f:
                my_nick_names = json.load(f)
                for nick in default_nick_names:
                    if nick not in my_nick_names:
                        my_nick_names.append(nick)
                        updated = True
                if updated:
                    save_nicknames(my_nick_names)
                return my_nick_names
        else:
            my_nick_names = default_nick_names
            save_nicknames(my_nick_names)
            screenmessage('Created default nicknames file', color=COLOR_SCREENCMD_ERROR)
        
            return default_nick_names
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Nicknames Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return default_nick_names

def save_nicknames(nicknames: list, is_cmd = False) -> None:
    """Save the nicknames to the file"""
    with open(nickname_file_path, 'w', encoding='utf-8') as f:
        json.dump(nicknames, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    if is_cmd: _load_nicknames()
#################### NICK NAMES DATA ####################

#################### CUSTOM REPLIES DATA ####################
custom_replies = {}
def _load_saved_custom_replies() -> Dict[str, str]:
    global custom_replies
    try:
        if os.path.exists(custom_reply_file_path):
            with open(custom_reply_file_path, 'r', encoding='utf-8') as file:
                custom_replies = json.load(file)
        else:
            if not os.path.exists(responder_directory):
                os.makedirs(responder_directory)
            custom_replies = {}  # Empty by default
            _save_custom_replies_to_file(custom_replies)
            screenmessage("Created Default Custom Replies File", color=COLOR_SCREENCMD_ERROR)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Custom Replies Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return custom_replies

def _save_custom_replies_to_file(data, is_cmd=False):
    with open(custom_reply_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    if is_cmd: _load_saved_custom_replies()
#################### CUSTOM REPLIES DATA ####################

#################### BLACKLIST RESPONDER PLAYERS DATA ####################
player_blacklisted_list: List[str] = []
"""Blacklisted Player From Triggering `Auto Respond`"""
def load_responder_blacklist_names(first_boot: bool = False) -> List[str]:
    """Load blacklisted names from the file or return the default list"""
    global player_blacklisted_list
    updated = False
    try:
        new_blacklist_names = []
        if os.path.exists(blacklist_file_path):
            with open(blacklist_file_path, 'r', encoding='utf-8') as f:
                _blacklist_names = json.load(f)
                if first_boot:
                    for name in player_blacklisted_list:
                        if name not in _blacklist_names and len(name) > 2:
                            new_blacklist_names.append(name)
                            updated = True
                        elif len(name) <= 2:
                            screenmessage(f"{CMD_LOGO_CAUTION} {get_lang_text('responderBlacklistInvalidName')}: \"{name}\"", color=COLOR_SCREENCMD_ERROR)

                player_blacklisted_list = list(set(_blacklist_names + new_blacklist_names))

                if updated and new_blacklist_names:
                    new_blacklisted_names = ", ".join(new_blacklist_names)
                    screenmessage(f"{CMD_LOGO_POSITIVE_WARNING} {get_lang_text('responderBlacklistAdded')}: [{new_blacklisted_names}]", color=COLOR_SCREENCMD_NORMAL)
                    save_blacklist_names(player_blacklisted_list)
                return player_blacklisted_list
        else:
            if not os.path.exists(players_data_file_folder_path):
                os.makedirs(players_data_file_folder_path)
            player_blacklisted_list = []
            save_blacklist_names(player_blacklisted_list)
            screenmessage('Created default blacklist names file', color=COLOR_SCREENCMD_ERROR)
            return player_blacklisted_list
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Blacklist Names Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return player_blacklisted_list

def save_blacklist_names(blacklist: List[str]) -> None:
    """Save the blacklisted names to the file"""
    try:
        for name in MY_MASTER+[f"{babase.charstr(babase.SpecialChar.V2_LOGO)}LessPal"]:
            if name in blacklist:
                blacklist.remove(name)
                #screenmessage(f'{CMD_LOGO_NEGATIVE} MY_MASTER ({name}) removed from blacklist', color=COLOR_SCREENCMD_NORMAL)
    except Exception as e:
        #screenmessage(f'{CMD_LOGO_CAUTION} Error removing MY_MASTER from blacklist: {e}', color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

    with open(blacklist_file_path, 'w', encoding='utf-8') as f:
        json.dump(blacklist, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    load_responder_blacklist_names()
#################### BLACKLIST RESPONDER PLAYERS DATA ####################

#################### MUTED PLAYERS DATA ####################
player_muted_list: List[str] = []
"""Muted Players From Its Chat being Shown in PartyWindow (If Possible)"""
def load_muted_players() -> List[str]:
    """Load muted players from the file or return the default list"""
    global player_muted_list
    try:
        updated = False
        new_player_muted_list: List[str] = []
        if os.path.exists(muted_players_file_path):
            with open(muted_players_file_path, 'r', encoding='utf-8') as f:
                _player_muted_list = json.load(f)
                updated = False
                for name in player_muted_list:
                    if name not in _player_muted_list and len(name) > 2:
                        new_player_muted_list.append(name)
                        updated = True
                    elif len(name) <= 2:
                        screenmessage(f"{CMD_LOGO_CAUTION} {get_lang_text('responderMutedInvalidName')}: \"{name}\"", color=COLOR_SCREENCMD_ERROR)

                player_muted_list = list(set(_player_muted_list + player_muted_list))

                if updated and new_player_muted_list:
                    new_player_muted_list_str = ", ".join(new_player_muted_list)
                    screenmessage(f"{CMD_LOGO_POSITIVE_WARNING} {get_lang_text('responderMutedAdded')}: [{new_player_muted_list_str}]", color=COLOR_SCREENCMD_NORMAL)
                    save_muted_players(player_muted_list)
                return player_muted_list

        else:
            if not os.path.exists(players_data_file_folder_path):
                os.makedirs(players_data_file_folder_path)
            player_muted_list = []
            save_muted_players(player_muted_list)
            screenmessage('Created default muted players file', color=COLOR_SCREENCMD_ERROR)
        return player_muted_list
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Muted Players Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return player_muted_list

def save_muted_players(muted_players: List[str]) -> None:
    """Save the muted players to the file"""
    global player_muted_list
    for name in muted_players:
        if name in MY_MASTER+[f"{babase.charstr(babase.SpecialChar.V2_LOGO)}LessPal"]:
            muted_players.remove(name)
        if muted_players.count(name) > 1:
            muted_players.remove(name)
    try:
        player_muted_list = muted_players
        with open(muted_players_file_path, 'w', encoding='utf-8') as f:
            json.dump(muted_players, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error saving muted players: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
#################### MUTED PLAYERS DATA ####################


####################### ANTI ABUSE DATA #######################
indonesian_abuses_default = [
    "asu", "asw", "tolol", 'kontol', "konto", "goblok", "bego", "babi", "setan", "bajing",
    "ngent", 'ngentot', 'ngentod', "kent", "gblk", "ajg", "puki", "kimak", "anjing", "bokep",
    "lonte", "lacur", "coli", "ppk", "mmk", "pepek", "memek", "tlol", 'anjg',
    "tolol", "bacot", "tempik", "perkosa", "tai", "ngntd", "pantek",
    "bgst", "bangsat", "bjingan", "bangst"
]

english_abuses_default = [
    'fuck', "fuc", "fuk", "fck", "fker", "fkr", "uuuck", "fuxc", "fuxk", "fkin", "fack", "the fk", "fk y",
    "fk u", "fk m", "fa k", "fu-ck", "f*", "fu c", "f@", "f#", "anus", "@nus", "d0g", "sh!t", "shit",
    "sh-it", "sh1t", "idiot", "idi.ot", "idi ot", "idi0t", "slut",
    "slur", "sl ut", "sl ur", "dick", "di ck", "dck", "di ck", "dck", "d*ck", "d!ck", "di-ck",
    "di.ck", "co-ck", "co.ck", "pussy", "pu$$", "vagina", "va gi", "vag!na", "cunt", "bitc",
    "bich", "beetch", "btch", "mtherf", "motherf", "mthrf", "m.f", "retard", "ass",
    "a$$", "@ss", "as s ", "bo.ob", "boob", "b00b", "pig", "nigg", "niig", "nigs", "niger",
    " niga", "cock", "piss", "tits", "pee ", "pimp", "whore", "wh@re", "nipp", "niple", "arse", "testic",
    "cum ", "cu m", "cu.m", "bstrd", "bastard", "pubic", "pube", "prostitute", "penis", "pen1s", "pnis", "pe.nis",
    "feces", "faeces", "b*tt", "bu tt", "rape", "r*perap3", "r#p",
    "r@p", "ra pe", "ra.pe", "di_k", "butt", "fatherless", "bxtches", "sh it", "bicth", "hentai", "fu\"k", "dic k"
]

indian_abuses_default = [
    "lund", "lu nd", "la ud", "laura", "lora", "laund", "lound", "lulli", "l#nd", "l@n", "l0d", "l@d",
    "lod3", "lo.de", "lawda", "lauda", "lau da", "ch od", "chud", "ch ud", "chut", "ch ut", "ch00t", "choot",
    "babbe", "bab be", "m.c", "ch0d", "ch#t", "chu-t", "r@nd", "mdrchd", "madarchod", "chod", "bube",
    "bu r ", "b*r", "buur", "chooch", "chuchi", "cho.och", "ch00c", "ch#c", "dalaal", "dalle",
    "dal le", "gand", "g@nd", "ga nd", "kutta", "kutte", "haraam", "jhat", "jhaat",
    "kutia", "kutti", "landi ", "landy", "nunn", "mooth", "muth", "paji", "paaji", "pesab",
    "pesaab", "pes ab", "pe sab", "pkmkb", "porkistan", "raand", "ullu", "t@t", "tatte", " tati",
    "tat te", "tatt e", "tatti", "tat ti", "tatt i", "tatt!", "tatty", "bhosda", "bhosdi", "bhsda",
    "bhosde", "b.d.s.k", "bdsk", "b@@p", "bhosdi", "lawdu", "lowde", "randi", "lavdu", "bhosdu",
    "lodu", "bosda", "mdrchot", "madarchot", "mdrcht", "bcc", "gendu", "ch00d", "jh@@tu",
    "chitiye"
]

bad_emojis = [
    '🖕', '🖕🏻', '🖕🏻', '🖕🏼', '🖕🏽', '🖕🏾',
    '🐖', '🐷', '🐽', '👉👌', '👌👈',
    '🍆🍑','🍑🍆', '🍌🍑', '🍑🍌', '🍑👈'
]

# Kasual
indonesian_abuses_chill = [
    'anj ', 'bodo', 'sinting', 'gila', 'buset', 'mampus', 'geble', 'gevlek', 'buta ',
    'gaje', 'waras', 'anjir', 'bongok', 'tai', 'anjim'
]

english_abuses_chill = [
    'dum', 'stupid', 'stpd', 'useless', 'usls', 'uselss', 'usless', 'pathe', 'rott',
    'shi-', 'sht', 'boring', 'garbage', 'trash', 'freak', 'imbecile', 'loser', 'losser',
    'frick', 'oh fu', 'moron', 'blabbermouth', 'timid', 'fearful', 'balls', 'poop',
    'ugly', 'jerk', 'brainless', 'u suk', 'm suk', 'stfu', 'suck', 'bloody', 'bloddy',
    'fu-', 'daddyless', 'motherless', 'sheet', 'shiet', 'shieet', 'fool'
]

indian_abuses_chill = [
    'gadha', 'fattu', 'गू', 'gote', 'haram'
]

indonesian_abuses = []
english_abuses = []
indian_abuses = []

########################## Anti Abuses ##########################
# File names for different languages
default_abuses = {
    id_lang: indonesian_abuses_default,
    en_lang: english_abuses_default,
    hi_lang: indian_abuses_default
}

def load_abuses(language: str) -> List[str]:
    """Load abuses for a given language"""
    global indonesian_abuses, english_abuses, indian_abuses
    try:
        # Get the file path for the specified language
        file_path = abuse_file_paths.get(language)

        # If the file path is invalid, return an error message
        if not file_path:
            print(f"Unsupported language code: {language}")
            return []

        # Load abuses from file if it exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                abuses = json.load(f)
                """default_abuses_list = default_abuses.get(language, [])
                updated = False

                # Check if default abuses are missing in the file and add them
                for default_abuse in default_abuses_list:
                    if default_abuse not in abuses:
                        abuses.append(default_abuse)
                        updated = True

                if updated:
                    save_abuses(language, abuses)
                    screenmessage(f'Updated \"{language}\" abuses file from default list', color=COLOR_SCREENCMD_ERROR)"""

                if language == id_lang:
                    indonesian_abuses = abuses
                elif language == en_lang:
                    english_abuses = abuses
                elif language == hi_lang:
                    indian_abuses = abuses
                return abuses
        else:
            if not os.path.exists(abuse_file_folder_path):
                os.makedirs(abuse_file_folder_path)
            # If the file doesn't exist, create it with default abuses
            if language == id_lang:
                indonesian_abuses = default_abuses[language]
                save_abuses(language, indonesian_abuses)
                screenmessage(f'Created default Indonesian abuses file', color=COLOR_SCREENCMD_ERROR)
                return indonesian_abuses
            elif language == en_lang:
                english_abuses = default_abuses[language]
                save_abuses(language, english_abuses)
                screenmessage(f'Created default English abuses file', color=COLOR_SCREENCMD_ERROR)
                return english_abuses
            elif language == hi_lang:
                indian_abuses = default_abuses[language]
                save_abuses(language, indian_abuses)
                screenmessage(f'Created default Indian abuses file', color=COLOR_SCREENCMD_ERROR)
                return indian_abuses
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Abuses Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return []

def save_abuses(language: str, abuses: list) -> None:
    """Save the abuses for a specific language"""
    file_path = abuse_file_paths.get(language)
    if not file_path:
        screenmessage(f"Unsupported language code: {language}", COLOR_SCREENCMD_ERROR)
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(abuses, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
####################### ANTI ABUSE DATA #######################

#################### PLAYERS ANTI ABUSE EXCEPTION (WHITELIST) DATA ####################
players_anti_abuse_exception: list[str] = []
"""List Of Our Friend That being `Excluded` from `Anti Abuse`"""

def load_player_name_exceptions() -> list[str]:
    """Load player names exceptions from the file, or return the default list"""
    global players_anti_abuse_exception
    updated = False
    try:
        if os.path.exists(exception_for_player_names_file_path):
            with open(exception_for_player_names_file_path, 'r', encoding='utf-8') as f:
                players_anti_abuse_exception = json.load(f)
                if not any(name in "LessPal" for name in players_anti_abuse_exception):
                    players_anti_abuse_exception.append("LessPal")
                    updated = True
                for name in MY_MASTER:
                    if not name in players_anti_abuse_exception:
                        players_anti_abuse_exception.append(name)
                        updated = True
                if updated:
                    save_player_name_exceptions(players_anti_abuse_exception)
                return players_anti_abuse_exception
        else:
            if not os.path.exists(abuse_file_folder_path):
                os.makedirs(abuse_file_folder_path)
            # If file doesn't exist, save the default list and return it
            save_player_name_exceptions(MY_MASTER)
            screenmessage('Created default player name exception file', color=COLOR_SCREENCMD_ERROR)
            return MY_MASTER if any(name in "LessPal" for name in MY_MASTER) else MY_MASTER + ['LessPal']
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Player Name Exception Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return MY_MASTER if any(name in "LessPal" for name in MY_MASTER) else MY_MASTER + ['LessPal']

def save_player_name_exceptions(exception_names: list[str]) -> None:
    """Save the player name exceptions list to the file"""
    try:
        for name in MY_MASTER:
            if name not in exception_names:
                exception_names.append(name)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error adding MY_MASTER to exception list: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

    with open(exception_for_player_names_file_path, 'w', encoding='utf-8') as f:
        json.dump(exception_names, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    load_player_name_exceptions()
#################### PLAYERS ANTI ABUSE EXCEPTION (WHITELIST) DATA ####################

#################### ANTI ABUSE WORDS EXCEPTION DATA ####################
exception_for_anti_abuse_default = [
    'pass', 'bass', 'sassy', 'pleass', 'grass', 'butter', 'assemb',
    'santai', 'partai', 'bantai', 'pantai',
    'piglet', 'random', 'button'
    'uranus', 'mammoth',
    "pantai", "cumi", "tanjiro",
    "basura", "cockroach", "cockroc", "leshita",
    "assum", "embarass", "wassap", "wass", "shita", "captai",
    "tail", "basu", "mass", "badass", "masuk",
    "sirf", "cashto", "smooth",
    "pegasus"
]
exception_words_for_anti_abuse = []
def load_anti_abuse_exception_words() -> list[str]:
    """Load exception words from the file or return the default list"""
    global exception_words_for_anti_abuse
    updates = 0
    try:
        if os.path.exists(exception_for_anti_abuse_file_path):
            with open(exception_for_anti_abuse_file_path, 'r', encoding='utf-8') as f:
                exception_words_for_anti_abuse = json.load(f)
                for default_exception in exception_for_anti_abuse_default:
                    if default_exception not in exception_words_for_anti_abuse:
                        exception_words_for_anti_abuse.append(default_exception)
                        updates += 1
                if updates != 0:
                    save_exception_word(exception_words_for_anti_abuse)
                return exception_words_for_anti_abuse
        else:
            if not os.path.exists(abuse_file_folder_path):
                os.makedirs(abuse_file_folder_path)
            # If file doesn't exist, save the default list and return it
            save_exception_word(exception_for_anti_abuse_default)
            screenmessage('Created default anti-abuse exception file', color=COLOR_SCREENCMD_ERROR)
            return exception_for_anti_abuse_default
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Anti Abuse Word Exc Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return exception_for_anti_abuse_default

def save_exception_word(exception_words: list[str]) -> None:
    """Save the exception list to the file"""
    with open(exception_for_anti_abuse_file_path, 'w', encoding='utf-8') as f:
        json.dump(exception_words, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    load_anti_abuse_exception_words()
#################### ANTI ABUSE WORDS EXCEPTION DATA ####################

##################### PLAYER ABUSE DATA #####################
player_warnings: Dict[str, int] = {}
"""Our player warning counter"""
def load_player_warnings() -> dict[str, int]:
    """Load player warnings from the file or return an empty dictionary"""
    global player_warnings
    try:
        if os.path.exists(warning_file_path):
            with open(warning_file_path, 'r', encoding='utf-8') as f:
                player_warnings = json.load(f)
                return player_warnings
        else:
            if not os.path.exists(players_data_file_folder_path):
                os.makedirs(players_data_file_folder_path)
            save_player_warnings({})
            screenmessage('Created Player Warnings File', color=COLOR_SCREENCMD_ERROR)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Player Warns Load: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
    return player_warnings

def save_player_warnings(data: dict[str, int]) -> None:
    """Save the player warnings list to the file"""
    with open(warning_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    load_player_warnings()


def detect_and_warn(nama_pemain: str, word: str, language_abuses: list[str], language: str, balasan: str, is_heavy: bool=False):
    detected_abuse = auto_responder.find_abuse(word, language_abuses) if auto_responder else None
    if detected_abuse:
        abuse = detected_abuse[0]
        name = detected_abuse[1]
        if not is_heavy:
            if any(icon in nama_pemain for icon in SPECIAL_CHARS):
                babase.pushcall(Call(chatmessage, f"Not Chill Word `{sensor_kata(abuse)}`({language}) Is In Ur Chat `{name}`"), from_other_thread=True)
                babase.pushcall(Call(chatmessage, f"{balasan}"), from_other_thread=True)

        elif is_heavy:
            if any(icon in nama_pemain for icon in SPECIAL_CHARS):
                add_player_abuse_warning(name, balasan, abuse, language)

def add_player_abuse_warning(player_name: str, balasan: str, detected_abuse: str, language: str="", is_emoji: bool=False) -> None:
    """Add warnings to the player's warning count"""
    global player_warnings
#    player_name = player_name.replace('', '') # Remove V2 Icon

    is_available = True
    if player_name not in current_session_namelist:
        is_available = False

    if is_available:
        if player_name in player_warnings:
            if responder_config.get(config_name_autokick):
                player_warnings[player_name] += 1
        else:
            player_warnings[player_name] = 1   

    if not is_emoji:
        if is_available and player_warnings[player_name] > MAX_WARNS and responder_config.get(config_name_autokick):
            msg = f"Badword `{sensor_kata(detected_abuse)}`({language}) Is In Ur Chat `{player_name}`, Enough!"
        else:
            msg = f"Badword `{sensor_kata(detected_abuse)}`({language}) Is In Ur Chat `{player_name}`"
        babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
    else:
        if is_available and player_warnings[player_name] > MAX_WARNS and responder_config.get(config_name_autokick):
            msg = f"Bad Emoji `{sensor_kata(detected_abuse)}` Is In Your Chat, `{player_name}`, Enough!"
        else:
            msg = f"Bad Emoji `{sensor_kata(detected_abuse)}` Is In Your Chat, `{player_name}`"
        babase.pushcall(Call(chatmessage, msg), from_other_thread=True)

    if is_available and player_warnings[player_name] <= MAX_WARNS:
        if responder_config.get(config_name_autokick) and is_available:
            babase.pushcall(Call(chatmessage, f"{balasan}! `{player_name}` Warn {str(player_warnings[player_name])}"), from_other_thread=True)
        else:
            babase.pushcall(Call(chatmessage, f"{balasan}! `{player_name}`"), from_other_thread=True)
    else:
        try:
            if is_available:
                real_name_cid = all_names[player_name]['client_id']
                kick_msg = f'{KICK_CMD} {str(real_name_cid)}'
                babase.pushcall(Call(chatmessage, kick_msg), from_other_thread=True)
                player_warnings[player_name] = 0

        except Exception as e:
            print(f'Error On Doing Auto Kick Action: ({e})')
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Auto Kick Failed: {e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            print_internal_exception(e)
            player_warnings[player_name] = 0

    save_player_warnings(player_warnings)

def manual_add_warn(player_name: str, reason: str = '', manual: bool = False) -> None:
    """Manually add 1 warning for a player"""
    global player_warnings

    if player_name in player_warnings:
        player_warnings[player_name] += 1
        if not manual: chatmessage(f"{CMD_LOGO_POSITIVE_WARNING} '{player_name}' Warns increased to {str(player_warnings[player_name])}")
        else: screenmessage(f"{CMD_LOGO_POSITIVE_WARNING} '{player_name}' Warns increased to {str(player_warnings[player_name])}", COLOR_SCREENCMD_NORMAL)
        if player_warnings[player_name] > MAX_WARNS and responder_config.get(config_name_autokick):
            try:
                real_name_cid = all_names[player_name]['client_id']
                if not manual: chatmessage(f'{KICK_CMD} {str(real_name_cid)}')
                player_warnings[player_name] = 0
            except Exception as e:
                if not manual:
                    screenmessage(f"{CMD_LOGO_CAUTION} Auto Kick Error {e}", color=COLOR_SCREENCMD_ERROR)
                    print(f'Error on doing kick action')
                print_internal_exception(e)
    else:
        player_warnings[player_name] = 1
        if not manual: chatmessage(f"{CMD_LOGO_POSITIVE_WARNING} '{player_name}' Warn 1") # public msg use (en) english

    save_player_warnings(player_warnings)

def manual_add_warn_popup(account_name: str, client_id: int, message: str):
    if account_name in MY_MASTER:
        screenmessage(get_lang_text('addWarnIsMaster'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
        return
    global player_warnings
    is_auto_kick = responder_config.get(config_name_autokick)
    player_warns = player_warnings.get(account_name, 0)
    if player_warns <= 0 or is_auto_kick:
        player_warnings[account_name] = player_warns + 1
    is_kick = False

    if not current_namelist.get(account_name):
        screenmessage(get_lang_text('addWarnNotInGame'), COLOR_SCREENCMD_ERROR)
        return

    # Formatting
    name: str = account_name
    warn_count = f"{str(player_warnings[account_name])}/{str(MAX_WARNS)}"
    if player_warnings[account_name] >= MAX_WARNS:
        message += f' {warn_msg_max_reached}'
        is_kick = True

    if add_warn_msg_use_profile_name and current_session_namelist.get(name, {}).get('profile_name'):
        try:
            profiles: list[str] = current_session_namelist[name]['profile_name']
            name = ', '.join(profiles)
        except: pass
    _send_message_parted(message.format(name=name, warn=warn_count))

    if is_kick and is_auto_kick:
        chatmessage(f'{KICK_CMD} {client_id}')
        player_warnings[account_name] = 0 

    save_player_warnings(player_warnings)

def manual_decrease_warn(player_name: str, is_master: bool = False) -> None:
    """Manually decrease 1 warning for a player"""
    global player_warnings

    if player_name in player_warnings:
        if player_warnings[player_name] >= 1:
            player_warnings[player_name] -= 1
            screenmessage(f"{CMD_LOGO_NEGATIVE_WARNING} \'{player_name}\' Warns decreased to {str(player_warnings[player_name])}", COLOR_SCREENCMD_NORMAL)
        else:
            msg = f"{CMD_LOGO_CAUTION} \'{player_name}\' Warns already 0"
            if not responder_config.get(config_name_screenmessage_cmd) and not is_master:
                chatmessage(msg)
            else:
                screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
    else:
        msg = f"{CMD_LOGO_CAUTION} \'{player_name}\' haven't warned before"
        if not responder_config.get(config_name_screenmessage_cmd) and not is_master:
            chatmessage(msg)
        else:
            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)

    save_player_warnings(player_warnings)

def reset_player_warning(message: str) -> None:
    """Reset a specific player's warning count"""
    global player_warnings
    _, player_name = message.split(' ', 1)

    is_matched = _match_player_acc_name_exme(list(player_warnings.keys()), player_name, include_my_name=True)
    if isinstance(is_matched, str):
        if is_matched in player_warnings:
            if player_warnings[is_matched] == 0:
                msg = f"{CMD_LOGO_CAUTION} '{is_matched}' warns already reset"
                if not responder_config.get(config_name_screenmessage_cmd):
                    chatmessage(msg)
                else:
                    screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
                return
            player_warnings[is_matched] = 0
            save_player_warnings(player_warnings)
            msg = f"{CMD_LOGO_NEGATIVE} '{is_matched}' warning count reset"
            if not responder_config.get(config_name_screenmessage_cmd):
                chatmessage(msg)
            else:
                screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
        else:
            msg = f"{CMD_LOGO_CAUTION} '{is_matched}' has no warnings"
            if not responder_config.get(config_name_screenmessage_cmd):
                chatmessage(msg)
            else:
                screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)

    elif is_matched is None:
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('cantMatchInPlayerData').format(player_name)}"
        if not responder_config.get(config_name_screenmessage_cmd):
            chatmessage(msg)
        else:
            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)

    else: chatmessage(f"{CMD_LOGO_CAUTION} ???")

def reset_all_player_warnings(cmd: bool=False) -> None:
    """Reset all players warning counts"""
    global player_warnings
    player_warnings = load_player_warnings()
    resets = False
    try:
        if player_warnings:
            for player_name in player_warnings:
                if not player_warnings[player_name] == 0:
                    player_warnings[player_name] = 0
                    if responder_config.get(config_name_cmdprint): print(f"Player Warning Resets: {player_name}")
                    resets = True
            if resets:
                save_player_warnings(player_warnings)
                screenmessage(f"{CMD_LOGO_NEGATIVE} All players warning counts have been reset", color=COLOR_SCREENCMD_NORMAL)
                if cmd:
                    msg = 'Reset Successful'
                    if not responder_config.get(config_name_screenmessage_cmd):
                        chatmessage(msg)
                    else:
                        screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
            elif not resets and cmd:
                msg = 'All Player Warnings Already Resets'
                if not responder_config.get(config_name_screenmessage_cmd):
                    chatmessage(msg)
                else:
                    screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
        else:
            pass
           # babase.AppTimer(2.5, Call(screenmessage, f"{CMD_LOGO_CAUTION} No player warnings to reset"))
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error On Player Warns Reset: {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

def handle_reset_player_warns(message: str):
    try:
        data = player_warnings
        if not data:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('noResponderData')}..."
            if not responder_config.get(config_name_screenmessage_cmd):
                chatmessage(msg)
            else:
                screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
            return
        cmd, player_name = message.split(' ', 1)
        reset_player_warning(player_name)
    except ValueError:
        msg = f"{CMD_LOGO_CAUTION} Use {toggle_reset_player_warns} [account_name]"
        if not responder_config.get(config_name_screenmessage_cmd):
            chatmessage(msg)
        else:
            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error", color=COLOR_SCREENCMD_ERROR)
        screenmessage(f"{CMD_LOGO_CAUTION} {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)
##################### PLAYER ABUSE DATA #####################

############################ PLAYER SERVER DATA ############################
server_players_data: dict[str, dict[str, Any]] = {}
def load_players_server_data() -> dict[str, dict[str, Any]]:
    """
    Load all JSON files that start with `profiles` from the Server Players Data folder,
    handling potential errors or duplicate keys, and saving to a new file.
    UPDATE: Format Data Returned same as the Format of players data saving from this plugin.
    `e.g: {"name": dict[str, Any]}`
    """
    global server_players_data
    files_processed = 0

    if not os.path.exists(players_server_data_folder_path):
        os.makedirs(players_server_data_folder_path)
        print(f"\nServer Players Data Folder Created, Put Server Players Data In Here:\n{str(players_server_data_folder_path)}")
        babase.pushcall(Call(screenmessage, f"Server Players Data Folder Created, Put Server Players Data In Here:{str(players_server_data_folder_path)}", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
        babase.pushcall(Call(screenmessage, f"{str(players_server_data_folder_path)}", COLOR_SCREENCMD_NORMAL), from_other_thread=True)

    try:
        empty_msg = f"Server Players Data Is Empty (；′⌒`)"
        if not os.listdir(players_server_data_folder_path):
            #babase.pushcall(Call(screenmessage, empty_msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)
            return {}
        for file_name in os.listdir(players_server_data_folder_path):
            if file_name.startswith("profiles") and file_name.endswith(".json"):
                files_processed += 1
                file_path = os.path.join(players_server_data_folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data: dict[str, dict[str, Any]] = json.load(file)
                        for pb_id, player_data in data.items():
                            player_name = player_data.name
                            if player_name: # Check if player_name exists cuz we need it
                                if server_players_data.get(player_name):
                                    # Handle duplicate player_name with different pb_id
                                    old_pb = server_players_data[player_name].get('pb_id')
                                    if old_pb and old_pb != pb_id:
                                      #  print(f"[WARNING] Same player_name '{player_name}' found with different pb_id {old_pb} -> {pb_id}")
                                        server_players_data[player_name]['pb_id'] = pb_id # Update pb_id
                                else:
                                    server_players_data[player_name] = player_data # Add player data if not exists
                                    server_players_data[player_name]['pb_id'] = pb_id # Add player data if not exists
                    except json.JSONDecodeError:
                        babase.pushcall(Call(screenmessage, f'{CMD_LOGO_CAUTION} Error loading {file_name}: Invalid JSON format', COLOR_SCREENCMD_ERROR), from_other_thread=True)
                        print_internal_exception(f"Invalid JSON in {file_name}")
                    except Exception as e:
                        babase.pushcall(Call(screenmessage, f'{CMD_LOGO_CAUTION} Error loading pb_id JSON database: {e}', COLOR_SCREENCMD_ERROR), from_other_thread=True)
                        print_internal_exception(e)

    except Exception as e:
        #babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error On Server P-Data Load: {e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print_internal_exception(e)
        return {}  # Return empty dictionary if error occurs

    if files_processed <= 0:
        babase.pushcall(Call(screenmessage, empty_msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)
        return {}
    return server_players_data

def _all_names_pb_update():
    update_all_names_with_pb_id(load_players_server_data())

def update_all_names_with_pb_id(server_pdata: dict[str, dict[str, Any]]):
    """Update all_names with pb_id data if the name matches or add new if not present.

    Should be done in another `Thread`"""
    global all_names
    total_data = 0
    if server_pdata == {}:
        msg = "No Server Players Data To Scan :("
        if not responder_config.get(config_name_screenmessage_cmd):
            babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
        else:
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)
        return
    try:
        changed_data_names: list[str] = []
        for player_name, data in server_pdata.items():
            pb_id = data.get('pb_id')

            # Continue to the next iteration if no player name is found
            if not player_name or player_name in changed_data_names:
                continue

            # Check if the player name exists in all_names
            if all_names.get(player_name):
                # If pb_id is different, update it
                if all_names[player_name].get('pb_id') != pb_id:
                    old_pb_id = all_names[player_name].get('pb_id')
                    # Prioritize old PB-ID if exists and config is set
                    if old_pb_id and responder_config.get(config_name_prioritize_bcs_pb):
                        print(f"[PB-ID] Prioritizing old pb_id {old_pb_id} over new {pb_id} for player '{player_name}'")
                    else:
                        all_names[player_name]['pb_id'] = pb_id
                        print(f"[PB-ID] Updated pb_id for player {old_pb_id} -> {pb_id} >> '{player_name}'")
                        changed_data_names.append(player_name)
                        total_data += 1
            # If player name doesn't exist, add it with pb_id
            """elif not responder_config.get(config_name_only_update_available_pdata) and player_name not in all_names:
                all_names[player_name] = {
                    'profile_name': False,
                    'client_id': '?',
                    'pb_id': pb_id
                }
                print(f"[NEW] Added new player '{player_name}' with pb_id: {pb_id}")
                changed_data_names.append(player_name)
                total_data += 1"""

        # Save updated all_names to file
        if total_data != 0:
            msg = f'PB-IDs Updated: {str(total_data)}'
            if not responder_config.get(config_name_screenmessage_cmd):
                babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
            else:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)
            print(f'PB-IDs Updated: {str(total_data)}')
            print('Saving Updates From Server Players Data..')
            _save_names_to_file()
        else:
            msg = f'No PB-IDs To Update'
            if not responder_config.get(config_name_screenmessage_cmd):
                babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
            else:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)

    except KeyError as e:
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} KeyError: Missing key in data", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        logging.exception(e)#print_internal_exception(e)
    except json.JSONDecodeError as e:
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} JSONDecodeError -> Error reading player data", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        logging.exception(e)#print_internal_exception(e)
    except Exception as e:
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error On Updating Server P-Data", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        babase.pushcall(Call(screenmessage, f"{e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print_internal_exception(e)
############################ PLAYER SERVER DATA ############################


##################### PING DATA #####################
def do_manual_server_ping(is_cmd:bool=False):
    try:
        info = bs.get_connection_to_host_info_2()
        if not info and is_cmd:
            msg = f'{CMD_LOGO_CAUTION} Can\'t Get Server Name Right Now :('
            if not responder_config.get(config_name_screenmessage_cmd):
                chatmessage(msg)
            else:
                screenmessage(msg, color=COLOR_SCREENCMD_ERROR)
            return
        elif info:
            server_name = info.name if info and info.name else server_name_default
            server_data = _get_server_data_from_fav(server_name)

            if server_data is None and is_cmd:
                msg = f'{CMD_LOGO_CAUTION} You Don\'t Have Any Saved (Fav) Server Data :('
                if not responder_config.get(config_name_screenmessage_cmd):
                    chatmessage(msg)
                else:
                    screenmessage(msg, color=COLOR_SCREENCMD_ERROR)
            elif server_data is False and is_cmd:
                msg = f'{CMD_LOGO_CAUTION} Can\'t Match Current Server In Saved (Fav) Server Data :('
                if not responder_config.get(config_name_screenmessage_cmd):
                    chatmessage(msg)
                else:
                    screenmessage(msg, color=COLOR_SCREENCMD_ERROR)
            elif isinstance(server_data, list):
                ip = server_data[0]
                port = server_data[1]
                _refresh_server_ip_and_port()
                Thread(target=start_pinging_server, args=(ip, port, is_cmd)).start()
    except Exception as e:
        if is_cmd:
            screenmessage(f"{CMD_LOGO_CAUTION} Error On Pinging :(")
            screenmessage(f"{CMD_LOGO_CAUTION} {e}", color=COLOR_SCREENCMD_ERROR)
            print_internal_exception(e)

def _get_server_data_from_fav(server_name: str) -> list[str] | bool | None:
    """Get server data from favorites

    `List`: Data matched [ip, port]

    `False`: No Match

    `None`: No Data
    """
    config = babase.app.config
    saved_servers: dict = config.get('Saved Servers', {})
    if not saved_servers:
        return None
    ip = None
    port = None
    for ip_port, server_data in saved_servers.items():
        saved_server_name = server_data.get('name')
        if not saved_server_name: continue
        if server_name == saved_server_name or server_name in saved_server_name:
            ip = server_data.get('addr')
            port = server_data.get('port')
    if ip and port:
        return [ip, port]
    else:
        return False

def _ping_server(ip, port) -> float | None:
    """
    Pings a server and returns the round-trip time in milliseconds.

    Args:
        `ip`: The IP address of the server.
        `port`: The PORT number of the server.

    Returns:
        The round-trip time in milliseconds, or None if the server is unreachable.
    """

    try:
        socket_type = get_ip_address_type(ip)
        with socket.socket(socket_type, socket.SOCK_DGRAM) as sock:
            sock.settimeout(5)
            starttime = time.time()
            for _i in range(3):
                sock.sendto(b'\x0b', (ip, port))
                try:
                    result = sock.recv(10)
                    if result == b'\x0c':
                        break
                except socket.timeout:
                    pass
                time.sleep(0.2)
            endtime = time.time()
            ping = ((endtime - starttime) * 1000)
            return ping
    except Exception as e:
        print_internal_exception(e)
        return None

error_sound = bui.getsound('error')
is_accurate_pinging = False
def _ping_server_accurate(callback: Callable[[], None]):
    global is_accurate_pinging

    if is_accurate_pinging:
        screenmessage(get_lang_text('isPingingServer'), COLOR_SCREENCMD_NORMAL)
        error_sound.play(1.5)
        return

    def start_accurate_ping():
        global is_accurate_pinging, is_doing_jobs, _server_ping
        defname = _ping_server_accurate.__name__
        is_doing_jobs.append(defname)

        is_accurate_pinging = True
        ping = _ping_server(_server_ip, _server_port)
        if ping:
            _server_ping = ping
            babase.pushcall(callback, from_other_thread=True)
        else:
            babase.pushcall(Call(screenmessage, get_lang_text('pingNotAvailable'), COLOR_SCREENCMD_ERROR))
            babase.pushcall(Call(error_sound.play, 1.5), from_other_thread=True)
        is_accurate_pinging = False

        is_doing_jobs.remove(defname)
    Thread(target=start_accurate_ping).start()

def _refresh_server_ip_and_port():
    info = bs.get_connection_to_host_info_2()
    server_name = info.name if info and info.name else server_name_default

    if server_name == server_name_default:
        global _server_ip, _server_port
        if _server_ip != _default_server_ip:
            _server_ip = _default_server_ip
            _server_port = _default_server_port
            print('Server IP and PORT Set To Default')
        print('Player Not In A Server')

def start_pinging_server(ip, port, is_cmd=False):
    """Start Pinging Server IP and PORT to global Variable. Do on a different `Thread`"""
    if ip == _default_server_ip:
        first_msg = f'{CMD_LOGO_CAUTION} {get_lang_text("pingInvalidIPandPORT")} :('
        if not responder_config.get(config_name_screenmessage_cmd) and is_cmd:
            babase.pushcall(Call(chatmessage, first_msg), from_other_thread=True)
        elif is_cmd:
            babase.pushcall(Call(screenmessage, first_msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
        print(first_msg)
        return
    intro_msg = f'{CMD_LOGO_SERVER} Pinging IP: {ip} PORT: {port}'
    ping = _ping_server(ip, port)
    if ping is None and is_cmd:
        msg = f'{CMD_LOGO_CAUTION} {get_lang_text("pingNotAvailable")} :('
        if not responder_config.get(config_name_screenmessage_cmd):
            babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
        else:
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
    elif ping or isinstance(ping, float):
        ping_msg = random.choice(PING_MESSAGE).format(round(ping, 2))
        if ping > 110:
            ping_msg += f' {get_random_sad_emoji()}'
        babase.pushcall(Call(chatmessage, ping_msg), from_other_thread=True)

global original_connect_to_party
original_connect_to_party = bs.connect_to_party
def new_connect_to_party(address: str, port: int = _default_server_port, print_progress: bool = False) -> None:
    global _server_ip, _server_port
    _server_ip = address
    _server_port = port
    #print(f'IP: {_server_ip}     PORT: {_server_port}')
    original_connect_to_party(_server_ip, _server_port, print_progress)
    if auto_responder: auto_responder._get_player_info()

def modify_conncet_to_party():
    bs.connect_to_party = new_connect_to_party
    #print('Connect To Party Modified')
    pass

def re_modify_conncet_to_party():
    """Re Change Connect To Party Func Module"""
    bs.connect_to_party = original_connect_to_party if bs.connect_to_party == new_connect_to_party else new_connect_to_party
    print(f'Connect To Party Re-Modified (Is Original): {bs.connect_to_party == original_connect_to_party} -> {bs.connect_to_party.__name__}')
##################### PING DATA #####################

# Func to censor abuse word that will be mentioned by My Master
def sensor_kata(word: str) -> str:
    huruf_sensor = {
        'a': 'á',
        'i': 'í',
        'u': 'ú',
        'e': 'é',
        'o': 'ó',
        'f': 'F',
        'd': 'đ',
        's': 'š',
        'm': 'ɱ',
        'k': 'ĸ'
    }
    return ''.join(huruf_sensor.get(char, char) for char in word)

def show_player_info_window(message: str, player_data: dict[str, dict[str, str]]) -> None:
    try:
        if not player_data:
            msg = f'{CMD_LOGO_CAUTION} {get_lang_text("noResponderData")}'
            screenmessage(msg, COLOR_SCREENCMD_NORMAL)
            return

        _, name = message.split(' ', 1)
        matched_name = find_player(name, True, player_data)

        if not player_data.get(matched_name):
            screenmessage(get_lang_text('findPlayerCmdNotFound').format(name), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return

        # Directly show player info popup
        PlayerInfoPopup(matched_name)
        msg = f"Opened Player \"{matched_name}\" Info Window"
        if not responder_config.get(config_name_screenmessage_cmd):
            chatmessage(msg)
        else:
            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)

    except ValueError:
        if player_data == all_names:
            toggle_str = toggle_info_player_all_pdata
        elif player_data == current_session_namelist:
            toggle_str = toggle_info_player_current_pdata
        else:
            toggle_str = '???'

        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('use')} {toggle_str} [name]"
        if not responder_config.get(config_name_screenmessage_cmd):
            chatmessage(msg)
        else:
            screenmessage(msg, color=COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} Error", color=COLOR_SCREENCMD_ERROR)
        screenmessage(f"{CMD_LOGO_CAUTION} {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

def _group_matched_players(player_names: dict[str, dict[str, Any]], search_term: str, match_with_profile: bool = True) -> Dict[str, dict[str, Any]]:
    """Find Player In Windowed List"""
    search_query_lower = search_term.lower()
    matched_player_names = {}

    edit_search_term = search_term
    if edit_search_term and edit_search_term[0] not in SPECIAL_CHARS:
        edit_search_term = babase.charstr(SpecialChar.V2_LOGO) + edit_search_term
    if player_names.get(edit_search_term):
        matched_player_names[edit_search_term] = player_names[edit_search_term]

    for real_name, profile_info in player_names.items():
        client_id = profile_info.get('client_id')
        p_profile: list[str] | None = profile_info.get('profile_name', [])
        if client_id == -1:
            pass#continue

        # Check for exact match first
        if search_query_lower == sanitize_name(real_name.lower()):
            matched_player_names[real_name] = profile_info
            continue

        if match_with_profile and p_profile:
            is_match = False
            for profile_name in p_profile:
                if search_query_lower == sanitize_name(profile_name.lower()):
                    matched_player_names[real_name] = profile_info
                    is_match = True
                    break
            if is_match:
                continue

        if search_query_lower in sanitize_name(real_name.lower()) or (match_with_profile and p_profile and search_query_lower in (', '.join([sanitize_name(name.lower()) for name in p_profile])).lower()):
            # Add the matching entry to self.player_names
            if real_name not in matched_player_names: matched_player_names[real_name] = profile_info
    return matched_player_names

def popup_player_list(message: str, player_data: dict[str, dict[str, Any]]):
    min_arguments_length = 1
    msg_short_argument = get_lang_text("findPlayerCmdShortArgument").format(str(min_arguments_length))
    msg_no_data = get_lang_text('noResponderData')

    msg_opened_window = get_lang_text('popupPlayerListWindowOpened')
    msg_opened_window_searching = get_lang_text('popupPlayerListWindowOpenedSearching')
    #msg_no_match = get_lang_text('popupPlayerListWindowSearchingNotFound')
    try:
        if player_data:
            cmd, search_term = message.split(' ', 1)

            if len(search_term) >= min_arguments_length:
                search_query = search_term.lower()
                PlayerListPopup(player_data, search_query)
                if not responder_config.get(config_name_screenmessage_cmd):
                    bs.chatmessage(msg_opened_window_searching)
                else:
                    bs.broadcastmessage(msg_opened_window_searching, color=COLOR_SCREENCMD_NORMAL)
            else:
                if not responder_config.get(config_name_screenmessage_cmd):
                    bs.chatmessage(msg_short_argument)
                else:
                    bs.broadcastmessage(msg_short_argument, color=COLOR_SCREENCMD_NORMAL)
                return
        else:
            if not responder_config.get(config_name_screenmessage_cmd):
                bs.chatmessage(msg_no_data)
            else:
                bs.broadcastmessage(msg_no_data, color=COLOR_SCREENCMD_NORMAL)
    except ValueError:
        if player_data:
            PlayerListPopup(player_data)
            if not responder_config.get(config_name_screenmessage_cmd):
                bs.chatmessage(msg_opened_window)
            else:
                bs.broadcastmessage(msg_opened_window, color=COLOR_SCREENCMD_NORMAL)
        else:
            if not responder_config.get(config_name_screenmessage_cmd):
                bs.chatmessage(msg_no_data)
            else:
                bs.broadcastmessage(msg_no_data, color=COLOR_SCREENCMD_NORMAL)
    except Exception as e:
        bs.broadcastmessage(f"{CMD_LOGO_CAUTION} Error :(")
        bs.broadcastmessage(f"{CMD_LOGO_CAUTION} {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

def _match_player_acc_name_exme(player_names: dict[str, dict[str, Any]] | list[str], search_term: str, include_my_name: bool=True, skip_my_name: bool=False) -> str | bool | None:
    """
    Match list/dict of player account name with search term.

    Only accept `simplified player names`. If Dict

    `str` = Match Found

    `False` = Matched MY_MASTER

    `None` = No Match
    """
    search_query = search_term.lower().strip()
    
    # Remove icons from the search query
    search_query = sanitize_name(search_query)

    def should_skip_name(name):
        return any(main_name in name for main_name in MY_MASTER)

    matched_player_name = None

    if isinstance(player_names, dict):
        # Try to find an exact match first
        for real_name, profile_info in player_names.items():
            real_name_lower = real_name.lower()
            if profile_info.get('client_id') == -1:
                continue

            sanitized_real_name = sanitize_name(real_name_lower)
            p_profiles = getattr(profile_info, 'profile_name', []) if profile_info is not None else []
            sanitized_profile_names = [sanitize_name(profile) for profile in p_profiles] if p_profiles else None

            if search_query == sanitized_real_name or (sanitized_profile_names and any(search_query == sanitized_profile for sanitized_profile in sanitized_profile_names)):
                if should_skip_name(real_name):
                    if skip_my_name:
                        continue
                    if not include_my_name:
                        return False  # Matching found, but exclude my name

                return real_name  # Exact match found

        # Try partial match if no exact match was found
        for real_name, profile_info in player_names.items():
            if profile_info.get('client_id') == -1:
                continue

            if (search_query in real_name.lower() or 
                (profile_info.get('profile_name', []) and search_query in ', '.join(getattr(profile_info, 'profile_name', []) if profile_info is not None else []).lower())):

                if should_skip_name(real_name):
                    if skip_my_name:
                        continue
                    if not include_my_name:
                        return False

                return real_name  # Partial match found

    elif isinstance(player_names, list):
        # Exact match first, then partial match
        for name in player_names:
            name_lower = name.lower()
            sanitized_name = sanitize_name(name_lower)
            if search_query == sanitized_name:
                if should_skip_name(name):
                    if skip_my_name:
                        continue
                    if not include_my_name:
                        return False
                return name
            
        for name in player_names:
            name_lower = name.lower()
            if search_query in name.lower():
                if should_skip_name(name_lower):
                    if skip_my_name:
                        continue
                    if not include_my_name:
                        return False
                return name

    return matched_player_name

def get_player_info_with_cid(clientID: int | None) -> Dict[str, Any]:
    """
    Return Player's Internal Info (Roster) Using Their `ClientID`.
    Don't worry, the name not started with V2 is handled.

    `RETURNED DATA`

    `data['account']` >> `STR`: Account Name

    `data['pb_id']` >> `STR`: PB-ID

    `data['profile_name_joint']` >> `STR`: Joint Of Player's Full Profile Names

    `data['profile_name_short']` >> `LIST[STR]`: Short Profile Names

    `data['profile_name']` >> `LIST[STR]`: Full Profile Names

    `data['client_id']` >> `INT`: Client ID
    """

    if clientID is None: # Should pass if its None, not using `not` statement, cuz 0 will be passed
        return {}

    all_player_info: list[dict[str, Any]] = [
        {
            'acc': player['display_string'],    # Account name
            'ds': player['players'],            # List of players playing in Acc (Profiles)
            'cid': player['client_id'],         # Client ID
            'aid': player['account_id']         # pb_id (Not For Clients)
        } for player in bs.get_game_roster()
    ]

    # Iterate over the current roster
    for player in all_player_info:
        client_id: int = player['cid']   # Client ID
        if client_id != clientID: continue

        _current_real_name: str = player['acc']     # Player's real name
        players: dict = player['ds']                # Player Joined Name (display name)
        account_id: str = player['aid']             # pb_id (Its Only Shows Current User pb_id, Not Other Players pb_id)

        full_names: List[str] = [
            p['name_full'] for p in players         # Get Player's Full Names
        ]
        names_short: List[str] = [
            p['name'] for p in players              # Get Player's Shorten Names
        ]
        current_real_name: str = ''

        # Handle icons in the real name
        if _current_real_name and _current_real_name[0] in SPECIAL_CHARS:
            current_real_name = player['acc']  # Original Icons
        elif _current_real_name.startswith('<HIDDEN>'):
            continue # Sadge
        else:
            # If player name Startwith PC or Android, its not possible
            # Because old servers support Device Icon
            # Else if the PC Or Android acc ID upgraded to V2
            current_real_name = babase.charstr(SpecialChar.V2_LOGO) + _current_real_name  # Add V2 Icon
            global is_1_4_server
            is_1_4_server = True

        ### Player Data Format ###
        # If the player has profile names (Joined)
        if players:
            # If the player has more than one profile name, join them with commas
            profile_name = full_names
            profile_name_short = names_short
            profile_name_joint = ', '.join(profile_name)
        else:
            profile_name = []
            profile_name_short = []
            profile_name_joint = ''

        p_data: Dict[str, str | list[str] | int] = {}

        p_data['account']                 = current_real_name     # Str Account Name
        p_data['profile_name_short']      = profile_name_short    # List Players In Acc Short Name
        p_data['client_id']               = client_id             # Client ID
        p_data['pb_id']                   = account_id            # Str (PB-ID)
        p_data['profile_name']            = profile_name          # List of profile names if Exist else False
        p_data['profile_name_joint']      = profile_name_joint    # profile names str Joint if Exist else False
        return p_data
    return {}

def get_simplified_player_info_using_cid(clientID: int | None, player_data: Dict[str, dict[str, Any]]) -> Dict[str, Any]:
    """
    Return Simplified Player's Info Using Their `ClientID`.
    Uses the simplified player names data for matching.
    """

    if clientID is None:
        return {}

    for pname, pdata in player_data.items():
        client_id = pdata.get('client_id', 0)

        if client_id == clientID:
            p_data: Dict[str, str | list[str] | int] = {
                'account': pname,
                'client_id': client_id,
                'pb_id': pdata.get('pb_id', ''),
                'profile_name': pdata.get('profile_name', []),
                'profile_name_short': pdata.get('profile_name_short', []),
                'profile_name_joint': pdata.get('profile_name_joint', '')
            }
            return p_data

    return {}

SPECIAL_CHARS: List[str] = [babase.charstr(i) for i in SpecialChar]
"""BombSquad Special Chars STR (Icons, Etc)"""
def sanitize_name(name: str):
    """Accurate Player's `Icon` Remover, By LessPal"""
    if name and name[0] in SPECIAL_CHARS:  # Check if the first character is not an alphabet or number
        return name[1:]
    return name

########## RUNNING BREAKER ##########
"""if not MY_MASTER:
    msg = f'{__name__}{PNAME_AND_MSG_SPLITTER}My Master Can\'t Be Empty'
    screenmessage(msg, COLOR_SCREENCMD_ERROR)
    raise ValueError(msg.removeprefix(__name__+PNAME_AND_MSG_SPLITTER))

if not any(name[0] in SPECIAL_CHARS for name in MY_MASTER):
    msg = f'{__name__}{PNAME_AND_MSG_SPLITTER}Please Input BS Icons In The Beginning Of The My Master\'s Name'
    screenmessage(msg, COLOR_SCREENCMD_ERROR)
    raise NameError(msg.removeprefix(__name__+PNAME_AND_MSG_SPLITTER))

if not all(name and name[1:].isalnum() for name in MY_MASTER):
    msg = f'{__name__}{PNAME_AND_MSG_SPLITTER}My Master\'s Name Can\'t Contains Special Letters'
    screenmessage(msg, COLOR_SCREENCMD_ERROR)
    raise NameError(msg.removeprefix(__name__+PNAME_AND_MSG_SPLITTER))
"""
#if not 'less' in __name__.lower():
#    msg = f"{__name__}{PNAME_AND_MSG_SPLITTER}Hey, You Need To Add \"Less\" Word In Less\'s PartyWindow Plugin\'s Name, Kindly Support Me :)"
#    screenmessage(msg, COLOR_SCREENCMD_ERROR)
#    raise NameError(msg.removeprefix(__name__+PNAME_AND_MSG_SPLITTER))

is_hidden_names_by_server = False
original_party_window = bauiv1lib.party.PartyWindow
def my_master_not_in_game():
    msg = f"{__name__}{PNAME_AND_MSG_SPLITTER}Uh oh, Can\'t Find My Master In Game/Server :("
    screenmessage(msg, COLOR_SCREENCMD_ERROR)
    if not is_hidden_names_by_server:
        bauiv1lib.party.PartyWindow = original_party_window
        global auto_responder
        if auto_responder:
            auto_responder._stop_engine()
            auto_responder = None
        babase.app.config['Chat Muted'] = False
########## RUNNING BREAKER ##########

player_acc_returner: Dict[str, str] = {}
"""
Helper to `get` player acc faster if exact match logic exist
using `_match_player_name` 
"""
def _match_player_name(player_name: str, player_data: dict[str, dict[str, Any]]) -> str:
    """
    Match Player Names Machine and Returns `Player's Account Name` If Match else original ,
    Don't Do `Lowering STR`.

    Only Accept The `Simplified Player Data`
    """
    # Cache lookup first
    if player_name in player_acc_returner:
        return player_acc_returner[player_name]

    # Handle common cases quickly
    if player_data.get(player_name): 
        return player_name
    if player_data.get(babase.charstr(SpecialChar.V2_LOGO) + player_name): 
        return babase.charstr(SpecialChar.V2_LOGO) + player_name

    # Pre-process name
    name = player_name
    if name.endswith('...') and name not in ('...', '....', '.....'):
        name = name.split('...')[0]

    # Generate possible name variations
    possible_names = {sanitize_name(n) for n in name.split('/')}
    possible_names.add(name)

    # Check cached names first
    for possible_name in possible_names:
        if possible_name in player_acc_returner:
            return player_acc_returner[possible_name]

    # Optimized partial matching
    for _player_real_name, profile_info in player_data.items():
        if profile_info.get('client_id') == -1:
            continue  # Skip server names

        profile_names = set(getattr(profile_info, 'profile_name', []) if profile_info is not None else [])
        profile_names_short = set(getattr(profile_info, 'profile_name_short', []) if profile_info is not None else [])

        # Check all possible name variations against profile names
        for possible_name in possible_names:
            # Exact match check
            if possible_name == _player_real_name:
                return _player_real_name

            # Short profile name matching
            if any(player_name == sanitize_name(profile) for profile in profile_names_short) or \
               any(name == sanitize_name(profile) for profile in profile_names_short):
                return _player_real_name

            # Profile name matching
            if any(possible_name in sanitize_name(profile) for profile in profile_names):
                return _player_real_name

            # Partial match in real name
            if possible_name in _player_real_name:
                return _player_real_name

    # No match found, return original name
    return player_name
"""Data Section"""

####### QUICK MESSAGES #######
default_quick_responds: List[str] = [
    'Dude That\'s Amazing!',
    'Good Game! $happy'
]
quick_responds: List[str] = []
"""Our Quick Responds"""
def _load_quick_responds() -> List[str]:
    global quick_responds
    try:
        if os.path.exists(quick_msg_file_path):
            with open(quick_msg_file_path, 'r') as f:
                quick_responds = f.read().splitlines()
                return quick_responds
        else:
            quick_responds = default_quick_responds
            _save_quick_responds(default_quick_responds)
            return default_quick_responds
    except Exception as e:
        print_internal_exception(e)
    return default_quick_responds

def _save_quick_responds(data: List[str]):
    try:
        if os.path.exists(quick_msg_file_path):
            with open(quick_msg_file_path, 'r') as f:
                existing_data = f.read().splitlines()
            if existing_data != data:
                with open(quick_msg_file_path, 'w') as f:
                    f.write('\n'.join(data))
            else:
                #print('Same Quick Respond Data')
                pass
        else:
            with open(quick_msg_file_path, 'w') as f:
                f.write('\n'.join(data))

    except Exception as e:
        logging.exception()
        screenmessage(f'Error writing quick responds: {e}', (1, 0, 0))
        bui.getsound('error').play(1.5)
####### QUICK MESSAGES #######

#### CUSTOM COMMANDS ####
default_custom_commands: List[str] = [
    '/donate 500 $cid $happy',
    '/ban $cid',
    '/pme $cid',
    '/gp $cid',
    '/pb $cid'
]
custom_commands: List[str] = []
"""Custom commands allow to create shortcuts for frequently used commands.
These commands can include variables that will be replaced with actual values when used:
- $name: Player's profile name
- $acc: Player's account name
- $cid: Player's client ID
- $happy: Happy emoji
- $unamused: Unamused emoji

You can add/edit/remove custom commands through the party window menu"""

def _load_custom_commands() -> List[str]:
    global custom_commands
    try:
        if os.path.exists(custom_command_file_path):
            with open(custom_command_file_path, 'r') as f:
                custom_commands = f.read().splitlines()
                return custom_commands
        else:
            _save_custom_commands(default_custom_commands)
            custom_commands = default_custom_commands
            return default_custom_commands
    except Exception as e:
        print_internal_exception(e)
    return custom_commands

def _save_custom_commands(data: List[str]):
    try:
        if os.path.exists(custom_command_file_path):
            with open(custom_command_file_path, 'r') as f:
                existing_data = f.read().splitlines()
            if existing_data != data:
                with open(custom_command_file_path, 'w') as f:
                    f.write('\n'.join(data))
            else:
                print('Same Custom Command Data')
        else:
            with open(custom_command_file_path, 'w') as f:
                f.write('\n'.join(data))
    except Exception as e:
        print_internal_exception(e)
        screenmessage('Error on saving custom commands', COLOR_SCREENCMD_ERROR)
#### CUSTOM COMMANDS ####

def _get_current_mute_type() -> Literal['muteAll', 'muteInGameOnly', 'mutePartyWindowOnly', 'unmuteAll']:
    if party_config.get(CFG_NAME_CHAT_MUTED) == True:
        if party_config.get(CFG_NAME_PARTY_CHAT_MUTED) == True:
            return 'muteAll'
        else:
            return 'muteInGameOnly'
    else:
        if party_config.get(CFG_NAME_PARTY_CHAT_MUTED) == True:
            return 'mutePartyWindowOnly'
        else:
            return 'unmuteAll'


#+++++++++++++++++++++# COMMANDS SECTION #+++++++++++++++++++++#
def find_player(search_term: str, include_profile: bool, player_data: dict[str, dict[str, Any]]) -> str:
    """Helper function to find a player by real or profile name using simplified player data"""
    search_term = sanitize_name(search_term)
    for name, info in player_data.items():
        if info.get('client_id') == -1:
            continue

        if search_term in name.lower():
            return name

        if include_profile:
            profile = info.profile_name
            if profile:
                profile_names = ', '.join(profile).lower()
                if search_term in profile_names:
                    return name
    return ''

def find_player_cmd(message: str, toggle: str, data_type: dict[str, dict[str, Any]], is_master: bool = False) -> None:
    """Send Matched Player Names"""
    # Mapping data types to their string representations
    if data_type == current_session_namelist:
        data_type_str = 'Current Session'
    elif data_type == all_names:
        data_type_str = 'All Names'
    elif data_type == current_namelist:
        data_type_str = 'Server Players'
    else:
        data_type_str = '???'

    try:
        # Validate data type
        if not data_type:
            msg = f'{CMD_LOGO_CAUTION} {get_lang_text("noResponderData")}...'
            if is_master or responder_config.get(config_name_screenmessage_cmd):
                screenmessage(msg, COLOR_SCREENCMD_NORMAL)
            else:
                chatmessage(msg)
            return

        # Validate and parse arguments
        if ' ' not in message.strip(): raise ValueError
        _, arguments = message.split(' ', 1)
        arguments = arguments.strip()
        
        # Validate argument length
        MIN_ARG_LENGTH = 1
        if len(arguments) < MIN_ARG_LENGTH:
            msg = f'{CMD_LOGO_CAUTION} {get_lang_text("findPlayerCmdShortArgument", "en" if not is_master else None).format(str(MIN_ARG_LENGTH))}'
            if is_master or responder_config.get(config_name_screenmessage_cmd):
                screenmessage(msg, COLOR_SCREENCMD_NORMAL)
            else:
                chatmessage(msg)
            return

        # Search by real name
        found_real_name = find_player(arguments, True, data_type)
        real_name_cid = data_type[found_real_name].get('client_id') if found_real_name else None
        real_name_pb_id = all_names[found_real_name].get('pb_id') if found_real_name else None

        # Search by profile name and real name
        profile_data = next(((getattr(info, 'profile_name', []), name, all_names.get(name, {}).get('pb_id', ''), info.get('client_id'))
                           for name, info in data_type.items()
                           if info.get('client_id') != -1 and 
                           ((getattr(info, 'profile_name', []) and arguments in ', '.join(getattr(info, 'profile_name', [])).lower()) or
                            arguments in name.lower())),
                          (None, None, None, 0))
        found_profile_name, found_real_name_from_profile, found_pb_id_from_profile, profile_cid = profile_data

        # Handle found profile
        if found_profile_name or found_real_name_from_profile:
            if found_profile_name:
                profile_str = ', '.join(found_profile_name)
                _send_message_parted(f'CID: [{profile_cid}] Profile -> ({profile_str}) Acc: ({found_real_name_from_profile})')
                if found_pb_id_from_profile:
                    chatmessage(f'[{found_real_name_from_profile}] PB-ID: {found_pb_id_from_profile}')

            # Handle found real name
            try:
                if found_real_name and not (found_profile_name and found_real_name in found_real_name_from_profile): # type: ignore
                    p_profile = all_names[found_real_name].get('profile_name', [])
                    profile_str = f'Profile: ({", ".join(p_profile)})' if p_profile else '(No Profile)'
                    _send_message_parted(f'CID: [{real_name_cid}] Acc -> ({found_real_name}) {profile_str}')
                    if real_name_pb_id:
                        _send_message_parted(f'[{found_real_name}] PB-ID: {real_name_pb_id}')
            except KeyError:
                _send_message_parted(f'CID: [{real_name_cid}] Acc -> ({found_real_name}) (No Profile)')

        # Handle no matches
        elif not found_real_name and not found_profile_name:
            msg = (f'No Match Found For "{arguments}" In {data_type_str} List' if not is_master else
                  f"{CMD_LOGO_CAUTION} {get_lang_text('findPlayerCmdNotFound').format(arguments)} In {data_type_str} List")
            if is_master or responder_config.get(config_name_screenmessage_cmd):
                screenmessage(msg, COLOR_SCREENCMD_NORMAL)
            else:
                chatmessage(msg)

    except ValueError:
        msg = f'{CMD_LOGO_CAUTION} {get_lang_text("use")} {toggle} [name] To Search In {data_type_str} Data'
        if is_master or responder_config.get(config_name_screenmessage_cmd):
            screenmessage(msg, COLOR_SCREENCMD_NORMAL)
        else:
            chatmessage(msg)
    except Exception as e:
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('findPlayerCmdFailed', 'en' if not is_master else None)} :("
        screenmessage(f"{CMD_LOGO_CAUTION} {e}", COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

def show_responder_data_window(message: str):
    try:
        _, data_attr = message.split(' ', 1)

        data_attr = data_attr.strip()
        data_type = 'Unknown'

        if data_attr.startswith(show_data_attr_nickname):
            data_type = "My Nicknames"
            EditableDataPopup(load_func=_load_nicknames, save_func_list=save_nicknames, label=data_type)

        elif data_attr.startswith(show_data_attr_kunci_jawaban):
            data_type = "Server QnA"
            EditableDataPopup(load_func=_load_saved_kunci_jawaban, save_func_dict=_save_kunci_jawaban_to_file, label=data_type)

        elif data_attr.startswith(show_data_attr_custom_replies):
            data_type = "Custom Replies"
            EditableDataPopup(load_func=_load_saved_custom_replies, save_func_dict=_save_custom_replies_to_file, label=data_type)

        elif data_attr.startswith(show_data_attr_blacklist_player):
            data_type = "Blacklisted Player"
            EditableDataPopup(load_func=load_responder_blacklist_names, save_func_list=save_blacklist_names, is_player=True, label=data_type)

        elif data_attr.startswith(show_data_attr_player_exception):
            data_type = "Player Exceptions"
            EditableDataPopup(load_func=load_player_name_exceptions, save_func_list=save_player_name_exceptions, is_player=True, label=data_type)

        elif data_attr.startswith(show_data_attr_muted_player):
            data_type = "Muted Players"
            EditableDataPopup(load_func=load_muted_players, save_func_list=save_muted_players, is_player=True, label=data_type)

        elif data_attr.startswith(show_data_attr_exception_anti_abuse_words):
            data_type = "Exception Words"
            EditableDataPopup(load_func=load_anti_abuse_exception_words, save_func_list=save_exception_word, label=data_type)

        elif data_attr.startswith(show_data_attr_abuse_data):
            data_type = "Abuses Data"
            try:
                _, lang = data_attr.split(' ', 1)
                if lang.strip().lower().startswith('id'):
                    EditableDataPopup(load_func=lambda: load_abuses(id_lang), save_func_list=lambda x: save_abuses(id_lang, x), label="Indonesian Abuses")
                elif lang.strip().lower().startswith('en'):
                    EditableDataPopup(load_func=lambda: load_abuses(en_lang), save_func_list=lambda x: save_abuses(en_lang, x), label="English Abuses")
                elif lang.strip().lower().startswith('hi'):
                    EditableDataPopup(load_func=lambda: load_abuses(hi_lang), save_func_list=lambda x: save_abuses(hi_lang, x), label="Hindi Abuses")
                else:
                    screenmessage(f"Invalid language code: {lang.strip()} Use: [{', '.join(abuses_languages)}]", color=COLOR_SCREENCMD_ERROR)
                    return

            except ValueError:
                msg = f"{CMD_LOGO_CAUTION} {get_lang_text('use')} {toggle_show_data} {show_data_attr_abuse_data} [{', '.join(abuses_languages)}]"
                if not responder_config.get(config_name_screenmessage_cmd):
                    chatmessage(f'{msg}')
                else:
                    screenmessage(f'{msg}', color=COLOR_SCREENCMD_NORMAL)
                return

        else:
            raise ValueError

        msg = f'Internal Data Opened: {data_type}'
        screenmessage(f'{msg}', color=COLOR_SCREENCMD_NORMAL)

    except ValueError:
        data_types_joint = ', '.join(show_data_attrs)
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('use')} {toggle_show_data} [{data_types_joint}]"
        if not responder_config.get(config_name_screenmessage_cmd):
            chatmessage(f'{msg}')
        else:
            screenmessage(f'{msg}', color=COLOR_SCREENCMD_NORMAL)
    except Exception as e:
        screenmessage(f"{CMD_LOGO_CAUTION} {e}", color=COLOR_SCREENCMD_ERROR)
        print_internal_exception(e)

#+++++++++++++++++++++# COMMANDS SECTION #+++++++++++++++++++++#
def matched_name(text: str, widget: bui.Widget):
    babase.pushcall(CallStrict(bui.textwidget, edit=widget, text=text), from_other_thread=True) # type: ignore

def save_last_game_replay(custom_name: Optional[str] = None) -> None:
    """
    Saves the last game replay with a timestamped name.

    Args:
        custom_name: An optional custom name for the replay file.
    """
    try:
        replay_dir = _babase.get_replays_dir()

        current_file_path = os.path.join(replay_dir, "__lastReplay.brp").encode(SystemEncode)

        print(f"Game replay path: {current_file_path}")

        if not os.path.exists(current_file_path):
            screenmessage(get_lang_text('saveReplayNoLastReplay') + f" {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return

        if custom_name:
            new_file_name = f"{custom_name}.brp"
            if '$date' in new_file_name:
                new_file_name = new_file_name.replace('$date', datetime.now().strftime("%Y-%m-%d"))
            if '$time' in new_file_name:
                new_file_name = new_file_name.replace('$time', datetime.now().strftime("%H-%M-%S"))
        else:
            default_name = str(babase.Lstr(resource="replayNameDefaultText").evaluate())
            new_file_name = f"{default_name} (%s).brp" % (datetime.now().strftime("%Y-%m-%d %H-%M-%S"))

        new_file_path = os.path.join(replay_dir, new_file_name).encode(SystemEncode)

        shutil.copyfile(current_file_path, new_file_path)

        screenmessage(get_lang_text('saveReplaySaved').format(new_file_name) + f" {get_random_happy_emoji()}", COLOR_SCREENCMD_NORMAL)
        bui.getsound('gunCocking').play()
    except Exception as e:
        print_internal_exception(e)
        screenmessage(get_lang_text('saveReplayError'), COLOR_SCREENCMD_ERROR)
        screenmessage(str(e), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)

class ReplayNameSavingPopup(popup.PopupWindow):
    """Window for entering custom name before saving replay."""
    def __init__(self) -> None:
        """create a custom name saving window"""
        self._transition_out = 'out_scale'

        width = 600
        height = 250

        uiscale = bui.app.ui_v1.uiscale
        super().__init__(
            position=(0.0, 0.0),
            size=(width, height),
            scale=(
                1.8 if uiscale is bui.UIScale.SMALL else
                1.5 if uiscale is bui.UIScale.MEDIUM else
                1.0
            ),
            bg_color=party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color))

        self._title = bui.textwidget(
            parent=self.root_widget,
            text=get_lang_text('saveReplayTitle'),
            position=(width*0.05, height - 45),
            maxwidth=width*0.775,
            color=(0.8, 0.8, 0.8, 1.0),
            scale=0.8,
            size=(width*0.85, 25),
            h_align='center',
            v_align='center',
            selectable=True,
            click_activate=True,
            on_activate_call=self._add_auto
        )

        self._cancel = btn = bui.buttonwidget(
            parent=self.root_widget,
            scale=0.75,
            position=(25, height - 40),
            size=(60, 60),
            label='',
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            color=(0.55, 0.5, 0.6),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2,
        )

        enter_text = get_lang_text('saveReplayEnter')
        b_width = min(len(enter_text) * 13.5, 300)
        self._enter_button = btn2 = bui.buttonwidget(
            parent=self.root_widget,
            position=(width * 0.5 - b_width * 0.5, 20),
            size=(b_width, 60),
            scale=1.0,
            label=enter_text,
            on_activate_call=self._do_enter,
            enable_sound=False
        )

        text_field_y_pos = height - 121
        self._text_field = bui.textwidget(
            parent=self.root_widget,
            position=(width*0.025, text_field_y_pos),
            size=(width*0.95, 46),
            text='',
            h_align='left',
            v_align='center',
            max_chars=100,
            maxwidth=width*0.9,
            color=(0.9, 0.9, 0.9, 1.0),
            editable=True,
            padding=4,
            on_return_press_call=self._enter_button.activate,
        )
        bui.widget(edit=btn, down_widget=self._text_field)

        bui.containerwidget(
            edit=self.root_widget,
            cancel_button=btn,
            start_button=btn2,
            selected_child=self._text_field,
        )

        info_texts = [
            ('$date', get_lang_text('saveReplayInfoDate').format('$date')),
            ('$time', get_lang_text('saveReplayInfoTime').format('$time'))
        ]
        info_y_pos = text_field_y_pos - 22.5
        for info, text in info_texts:
            bui.textwidget(
                parent=self.root_widget,
                text=text,
                position=(-width*0.05, info_y_pos),
                color=(0.8, 0.8, 0.8, 0.7),
                size=(width*0.6, 30),
                scale=0.75,
                h_align='left',
                v_align='center',
                selectable=True,
                click_activate=True,
                on_activate_call=CallStrict(self._add_info, info)
            )
            info_y_pos -= 22.5

    def _add_info(self, info: str):
        current_text = bui.textwidget(query=self._text_field)
        if info not in current_text:
            _edit_text_field_global(info, 'add', widget=self._text_field)

    def _add_auto(self):
        current_text: str = bui.textwidget(query=self._text_field)
        new_text = "My Custom Replay $date $time"
        def do_replace():
            _edit_text_field_global(new_text, 'replace', widget=self._text_field)
        if not current_text or not current_text.strip():
            do_replace()
        elif new_text not in current_text:
            text = get_lang_text('saveReplayConfirmReplaceWithDefault')
            ConfirmWindow(
                origin_widget=self.root_widget,
                text= f"{text}?",
                width=min(len(text) * 13.5, 600),
                height=125,
                action=do_replace,
                cancel_is_selected=True,
                cancel_text=get_lang_text('cancel'),
                text_scale=1,
                ok_text=get_lang_text('yes')
            )

    def on_popup_cancel(self) -> None:
        name = bui.textwidget(query=self._text_field)
        if not name or not name.strip():
            self._do_back()
        else:
            self._confirm_exit()

    def _on_cancel_press(self):
        name = bui.textwidget(query=self._text_field)
        if not name or not name.strip():
            self._do_back()
        else:
            self._confirm_exit()

    def _confirm_exit(self):
        text = get_lang_text('saveReplayConfirmExit')
        ConfirmWindow(
            text=f"{text}",
            width=min(len(text) * 13.5, 600),
            height=120,
            action=self._do_back,
            cancel_button=True,
            cancel_is_selected=True,
            text_scale=1.0,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel'),
            origin_widget=self.root_widget)

    def _save_replay(self, custom_name: str) -> None:
        try:
            replay_dir = _babase.get_replays_dir()
            new_file_name = f"{custom_name}.brp"
            
            if '$date' in new_file_name:
                new_file_name = new_file_name.replace('$date', datetime.now().strftime("%Y-%m-%d"))
            if '$time' in new_file_name:
                new_file_name = new_file_name.replace('$time', datetime.now().strftime("%H-%M-%S"))

            new_file_path = os.path.join(replay_dir, new_file_name).encode(SystemEncode)

            if os.path.exists(new_file_path):
                text = get_lang_text('saveReplayOverwriteConfirm')
                ConfirmWindow(
                    text=f"{text}?",
                    width=min(len(text) * 13.5, 600),
                    height=120,
                    action=Call(self._do_save, new_file_path),
                    cancel_button=True,
                    cancel_is_selected=True,
                    text_scale=1.0,
                    ok_text=get_lang_text('yes'),
                    cancel_text=get_lang_text('cancel'),
                    origin_widget=self.root_widget
                )
            else:
                self._do_save(new_file_path)

        except Exception as e:
            print_internal_exception(e)
            screenmessage(get_lang_text('saveReplayError'), COLOR_SCREENCMD_ERROR)
            screenmessage(str(e), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

    def _do_save(self, file_path: bytes) -> None:
        try:
            current_file_path = os.path.join(_babase.get_replays_dir(), "__lastReplay.brp").encode(SystemEncode)
            if not os.path.exists(current_file_path):
                screenmessage(get_lang_text('saveReplayNoLastReplay') + f" {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return

            shutil.copyfile(current_file_path, file_path)
            screenmessage(get_lang_text('saveReplaySaved').format(os.path.basename(file_path)) + f" {get_random_happy_emoji()}", COLOR_SCREENCMD_NORMAL)
            bui.getsound('gunCocking').play(1.5)
        except Exception as e:
            print_internal_exception(e)
            screenmessage(get_lang_text('saveReplayError'), COLOR_SCREENCMD_ERROR)
            screenmessage(str(e), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        bui.containerwidget(
            edit=self.root_widget, transition=self._transition_out
        )

    def _do_enter(self) -> None:
        name = bui.textwidget(query=self._text_field)
        if not name or not name.strip():
            screenmessage(get_lang_text('saveReplayEmptyName'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            bui.containerwidget(
                edit=self.root_widget,
                selected_child=self._text_field
            )
            return
        self._save_replay(name)

    def _do_back(self) -> None:
        bui.containerwidget(
            edit=self.root_widget, transition=self._transition_out
        )

_ping_button: bui.Widget
def _get_ping_color() -> tuple[float, float, float]:
    try:
        if _server_ping < 75:
            return (0, 1, 0) # Green
        elif _server_ping < 100:
            return (0.5, 1, 0) # Light Green
        elif _server_ping < 300:
            return (1, 1, 0) # Yellow
        elif _server_ping < 500:
            return (1, 0.75, 0) # Orange
        elif _server_ping < 750:
            return (1, 0.5, 0) # Dark Orange
        elif _server_ping < 1000:
            return (1, 0.25, 0) # Very Dark Orange
        else:
            return (1, 0, 0) # Red
    except:
        return (0.1, 0.1, 0.1)

def _rejoin_server():
    if _server_ip != _default_server_ip or _server_port != _default_server_port:
        if bs.get_connection_to_host_info_2():
            bs.disconnect_from_host()
            babase.apptimer(0.1, Call(bs.connect_to_party, _server_ip, _server_port))
        else:
            bs.connect_to_party(_server_ip, _server_port)
    else:
        msg = f"{CMD_LOGO_CAUTION} Invalid IP and PORT: {_server_ip}:{_server_port}"
        bui.getsound('error').play(1.5)
        screenmessage(msg, color=COLOR_SCREENCMD_ERROR)


is_gather_window = None
def new_close_gather_func():
    global is_gather_window

    # Validate that the window still exists and has its root widget
    if (
        is_gather_window is None
        or not hasattr(is_gather_window, "_root_widget")
        or is_gather_window._root_widget is None
    ):
        print("[DEBUG] Warning: GatherWindow already destroyed or invalid.")
        is_gather_window = None
        return

    try:
        # Close with transition if it still exists
        bui.containerwidget(
            edit=is_gather_window._root_widget,
            transition=is_gather_window._main_window_transition_out
        )

        # Remove the root widget after a small delay
        root_widget = is_gather_window.get_root_widget()
        if root_widget is not None:
            babase.apptimer(1.0, root_widget.delete)

        # Save state if the method exists
        if hasattr(is_gather_window, "_save_state"):
            is_gather_window._save_state()

        print("[DEBUG] Delete GatherWindow Root Widget Called")

    except Exception as e:
        print(f"[DEBUG] Error while closing GatherWindow: {e}")

    # Clean up global reference to avoid memory leaks
    is_gather_window = None

class ModifiedGatherWindow(bui.MainWindow):
    """Window for joining/inviting friends - MODIFIED VERSION."""

    class TabID(Enum):
        """Our available tab types."""
        ABOUT = 'about'
        INTERNET = 'internet'
        PRIVATE = 'private'
        NEARBY = 'nearby'
        MANUAL = 'manual'

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from bauiv1lib.gather.abouttab import AboutGatherTab
        from bauiv1lib.gather.manualtab import ManualGatherTab
        from bauiv1lib.gather.privatetab import PrivateGatherTab
        from bauiv1lib.gather.publictab import PublicGatherTab
        from bauiv1lib.gather.nearbytab import NearbyGatherTab

        plus = bui.app.plus
        assert plus is not None

        bui.set_analytics_screen('Gather Window')
        uiscale = bui.app.ui_v1.uiscale
        self._width = (
            1640
            if uiscale is bui.UIScale.SMALL
            else 1100 if uiscale is bui.UIScale.MEDIUM else 1200
        )
        self._height = (
            1000
            if uiscale is bui.UIScale.SMALL
            else 730 if uiscale is bui.UIScale.MEDIUM else 900
        )
        self._current_tab: GatherWindow.TabID | None = None
        self._r = 'gatherWindow'

        # Do some fancy math to fill all available screen area up to the
        # size of our backing container. This lets us fit to the exact
        # screen shape at small ui scale.
        screensize = bui.get_virtual_screen_size()
        scale = (
            1.4
            if uiscale is bui.UIScale.SMALL
            else 0.88 if uiscale is bui.UIScale.MEDIUM else 0.66
        )
        # Calc screen size in our local container space and clamp to a
        # bit smaller than our container size.
        target_width = min(self._width - 130, screensize[0] / scale)
        target_height = min(self._height - 130, screensize[1] / scale)

        # To get top/left coords, go to the center of our window and
        # offset by half the width/height of our target area.
        yoffs = 0.5 * self._height + 0.5 * target_height + 30.0

        self._scroll_width = target_width
        self._scroll_height = target_height - 65
        self._scroll_bottom = yoffs - 93 - self._scroll_height
        self._scroll_left = (self._width - self._scroll_width) * 0.5

        # Llamar al constructor padre
        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height),
                toolbar_visibility=(
                    'menu_tokens'
                    if uiscale is bui.UIScale.SMALL
                    else 'menu_full'
                ),
                scale=scale,
            ),
            transition=transition,
            origin_widget=origin_widget,
            # We're affected by screen size only at small ui-scale.
            refresh_on_screen_size_changes=uiscale is bui.UIScale.SMALL,
        )

        self._back_button = None  # Clean original reference
        
        # Create our custom button
        custom_back_pos = (70, yoffs - 43)
        custom_back_size = (60, 60)
        
        self._custom_back_button = bui.buttonwidget(
            parent=self._root_widget,
            position=custom_back_pos,
            size=custom_back_size,
            scale=1.1,
            autoselect=True,
            label=bui.charstr(bui.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._custom_main_window_back,
            color=(1, 1, 1), 
            textcolor=(0, 0, 0)
        )
        
        # Set the custom button as a cancel button
        bui.containerwidget(edit=self._root_widget, cancel_button=self._custom_back_button)
        
        # For uiscale SMALL, also set on_cancel_call
        if uiscale is bui.UIScale.SMALL:
            bui.containerwidget(
                edit=self._root_widget, 
                on_cancel_call=self._custom_main_window_back
            )

        bui.textwidget(
            parent=self._root_widget,
            position=(
                (
                    self._width * 0.5
                    + (
                        (self._scroll_width * -0.5 + 170.0 - 70.0)
                        if uiscale is bui.UIScale.SMALL
                        else 0.0
                    )
                ),
                yoffs - (64 if uiscale is bui.UIScale.SMALL else 4),
            ),
            size=(0, 0),
            color=bui.app.ui_v1.title_color,
            scale=1.3 if uiscale is bui.UIScale.SMALL else 1.0,
            h_align='left' if uiscale is bui.UIScale.SMALL else 'center',
            v_align='center',
            text=(bui.Lstr(resource=f'{self._r}.titleText')),
            maxwidth=135 if uiscale is bui.UIScale.SMALL else 320,
        )

        # Build up the set of tabs we want.
        tabdefs: list[tuple[GatherWindow.TabID, bui.Lstr]] = [
            (self.TabID.ABOUT, bui.Lstr(resource=f'{self._r}.aboutText'))
        ]
        if plus.get_v1_account_misc_read_val('enablePublicParties', True):
            tabdefs.append(
                (
                    self.TabID.INTERNET,
                    bui.Lstr(resource=f'{self._r}.publicText'),
                )
            )
        tabdefs.append(
            (self.TabID.PRIVATE, bui.Lstr(resource=f'{self._r}.privateText'))
        )
        tabdefs.append(
            (self.TabID.NEARBY, bui.Lstr(resource=f'{self._r}.nearbyText'))
        )
        tabdefs.append(
            (self.TabID.MANUAL, bui.Lstr(resource=f'{self._r}.manualText'))
        )

        tab_inset = 250.0 if uiscale is bui.UIScale.SMALL else 100.0

        self._tab_row = TabRow(
            self._root_widget,
            tabdefs,
            size=(self._scroll_width - 2.0 * tab_inset, 50),
            pos=(
                self._scroll_left + tab_inset,
                self._scroll_bottom + self._scroll_height - 4.0,
            ),
            on_select_call=bui.WeakCallStrict(self._set_tab),
        )

        # Now instantiate handlers for these tabs.
        tabtypes: dict[GatherWindow.TabID, type[GatherTab]] = {
            self.TabID.ABOUT: AboutGatherTab,
            self.TabID.MANUAL: ManualGatherTab,
            self.TabID.PRIVATE: PrivateGatherTab,
            self.TabID.INTERNET: PublicGatherTab,
            self.TabID.NEARBY: NearbyGatherTab,
        }
        self._tabs: dict[GatherWindow.TabID, GatherTab] = {}
        for tab_id in self._tab_row.tabs:
            tabtype = tabtypes.get(tab_id)
            if tabtype is not None:
                self._tabs[tab_id] = tabtype(self)

        # Eww; tokens meter may or may not be here; should be smarter
        # about this.
        bui.widget(
            edit=self._tab_row.tabs[tabdefs[-1][0]].button,
            right_widget=bui.get_special_widget('tokens_meter'),
        )
        if uiscale is bui.UIScale.SMALL:
            bui.widget(
                edit=self._tab_row.tabs[tabdefs[0][0]].button,
                left_widget=bui.get_special_widget('back_button'),
                up_widget=bui.get_special_widget('back_button'),
            )

        # Not actually using a scroll widget anymore; just an image.
        bui.imagewidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._scroll_height),
            position=(
                self._width * 0.5 - self._scroll_width * 0.5,
                self._scroll_bottom,
            ),
            texture=bui.gettexture('scrollWidget'),
            mesh_transparent=bui.getmesh('softEdgeOutside'),
            opacity=0.4,
        )
        self._tab_container: bui.Widget | None = None

        self._restore_state()

    def _custom_main_window_back(self) -> None:
        "Our custom function to close the window."
        
        # Save state if necessary
        if hasattr(self, "_save_state"):
            self._save_state()
            
        # Close the window using the native transition
        try:
            bui.containerwidget(
                edit=self._root_widget,
                transition=self._main_window_transition_out
            )
            
            # Schedule widget removal after a while
            root_widget = self.get_root_widget()
            if root_widget is not None:
                bui.apptimer(0.5, root_widget.delete)
                
        except Exception as e:
            #print(f"[DEBUG] Error during close: {e}")
            # Fallback: try closing in another way
            try:
                self.main_window_back()
            except:
                pass

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

    @override
    def on_main_window_close(self) -> None:
        self._save_state()

    def playlist_select(
        self,
        origin_widget: bui.Widget,
        context: PlaylistSelectContext,
    ) -> None:
        """Called by the private-hosting tab to select a playlist."""
        from bauiv1lib.play import PlayWindow

        # Avoid redundant window spawns.
        if not self.main_window_has_control():
            return

        playwindow = PlayWindow(
            origin_widget=origin_widget, playlist_select_context=context
        )
        self.main_window_replace(playwindow)

        # Grab the newly-set main-window's back-state; that will lead us
        # back here once we're done going down our main-window
        # rabbit-hole for playlist selection.
        context.back_state = playwindow.main_window_back_state

    def _set_tab(self, tab_id: TabID) -> None:
        if self._current_tab is tab_id:
            return
        prev_tab_id = self._current_tab
        self._current_tab = tab_id

        # We wanna preserve our current tab between runs.
        cfg = bui.app.config
        cfg['Gather Tab'] = tab_id.value
        cfg.commit()

        # Update tab colors based on which is selected.
        self._tab_row.update_appearance(tab_id)

        if prev_tab_id is not None:
            prev_tab = self._tabs.get(prev_tab_id)
            if prev_tab is not None:
                prev_tab.on_deactivate()

        # Clear up prev container if it hasn't been done.
        if self._tab_container:
            self._tab_container.delete()

        tab = self._tabs.get(tab_id)
        if tab is not None:
            self._tab_container = tab.on_activate(
                self._root_widget,
                self._tab_row.tabs[tab_id].button,
                self._scroll_width,
                self._scroll_height,
                self._scroll_left,
                self._scroll_bottom,
            )
            return

    def _save_state(self) -> None:
        try:
            for tab in self._tabs.values():
                tab.save_state()

            sel = self._root_widget.get_selected_child()
            selected_tab_ids = [
                tab_id
                for tab_id, tab in self._tab_row.tabs.items()
                if sel == tab.button
            ]
            if sel == self._custom_back_button:
                sel_name = 'Back'
            elif selected_tab_ids:
                assert len(selected_tab_ids) == 1
                sel_name = f'Tab:{selected_tab_ids[0].value}'
            elif sel == self._tab_container:
                sel_name = 'TabContainer'
            else:
                raise ValueError(f'unrecognized selection: \'{sel}\'')
            assert bui.app.classic is not None
            bui.app.ui_v1.window_states[type(self)] = {
                'sel_name': sel_name,
            }
        except Exception:
            logging.exception('Error saving state for %s.', self)

    def _restore_state(self) -> None:
        try:
            for tab in self._tabs.values():
                tab.restore_state()

            sel: bui.Widget | None
            assert bui.app.classic is not None
            winstate = bui.app.ui_v1.window_states.get(type(self), {})
            sel_name = winstate.get('sel_name', None)
            assert isinstance(sel_name, (str, type(None)))
            current_tab = self.TabID.ABOUT
            gather_tab_val = bui.app.config.get('Gather Tab')
            try:
                stored_tab = self.TabID(gather_tab_val)
                if stored_tab in self._tab_row.tabs:
                    current_tab = stored_tab
            except ValueError:
                pass
            self._set_tab(current_tab)
            if sel_name == 'Back':
                sel = self._custom_back_button
            elif sel_name == 'TabContainer':
                sel = self._tab_container
            elif isinstance(sel_name, str) and sel_name.startswith('Tab:'):
                try:
                    sel_tab_id = self.TabID(sel_name.split(':')[-1])
                except ValueError:
                    sel_tab_id = self.TabID.ABOUT
                sel = self._tab_row.tabs[sel_tab_id].button
            else:
                sel = self._tab_row.tabs[current_tab].button
            bui.containerwidget(edit=self._root_widget, selected_child=sel)

        except Exception:
            logging.exception('Error restoring state for %s.', self)


def _open_gather_window(close_window_func: Optional[Callable[[], None]] = None):
    global is_gather_window

    # Avoid duplicates
    if is_gather_window and is_gather_window.get_root_widget():
        try:
            # If it already exists, close it first
            is_gather_window.main_window_back()
        except:
            pass
        is_gather_window = None

    # Create new modified window
    is_gather_window = ModifiedGatherWindow('in_left', None)

    # Close previous window if provided
    if close_window_func:
        close_window_func()

    bui.getsound('dingSmallHigh').play(1.5)

def _get_popup_window_scale() -> float:
    uiscale = bui.app.ui_v1.uiscale
    return (
        1.6 if uiscale is babase.UIScale.SMALL
        else 1.325 if uiscale is babase.UIScale.MEDIUM
        else 1.05
    )

ping_server_delay = 6
def ping_server_recall():
    global is_pinging
    if is_pinging: return
    info = bs.get_connection_to_host_info_2()
    if info is not None and info.name != '': #and self._ping_button:
        Thread(target=PingThread, args=(_server_ip, _server_port)).start()

def reset_global_vars():
    global is_1_4_server, ping_server_timer, is_hidden_names_by_server, is_muted_player
    ping_server_timer = None
    is_1_4_server = False
    is_hidden_names_by_server = False
    is_muted_player = False

roster_name_viewer = 0

_pending_msgs: List[str] = []
"""List of pending messages send from server"""

_last_text_field_msg: str = ""
_chat_texts: List[str] = []

def replace_msg_emoji_var_with_emojis(text: str):
    if '$sad' in text.lower(): text = text.replace('$sad', get_random_sad_emoji())
    if '$happy' in text.lower(): text = text.replace('$happy', get_random_happy_emoji())
    if '$unamused' in text.lower(): text = text.replace('$unamused', get_random_unamused_emoji())
    return text

class LessPartyWindow(bauiv1lib.party.PartyWindow):

    def __del__(self) -> None:
        self.ping_timer = None
        self._update_timer = None

    def __init__(self, origin: Sequence[float] = (0, 0)) -> None:
        self._uiopenstate = bui.UIOpenState('classicparty')
        self.uiscale : babase.UIScale = bui.app.ui_v1.uiscale
        self.bg_color: tuple[float, float, float] = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)

        self._size_radius = -100
        self._width  : int = (1250 if self.uiscale is babase.UIScale.SMALL else
                              1100 if self.uiscale is babase.UIScale.MEDIUM else
                              1000) # Lebar
        self._height : int = (825 if self.uiscale is babase.UIScale.SMALL else
                              1075 if self.uiscale is babase.UIScale.MEDIUM else
                              1250) # Tinggi

        bui.Window.__init__(self,
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(self._width, self._height),
                transition='in_scale',
                color=self.bg_color,
                on_outside_click_call=self.close_with_sound,
                scale_origin_stack_offset=origin,
                scale=(
                    PARTY_WINDOW_SCALE_SMALL  if self.uiscale is babase.UIScale.SMALL else
                    PARTY_WINDOW_SCALE_MEDIUM if self.uiscale is babase.UIScale.MEDIUM else
                    PARTY_WINDOW_SCALE_LARGE
                ),
                stack_offset=(
                    (0.0, -12.5) if self.uiscale is babase.UIScale.SMALL else
                    (210, -7.5) if self.uiscale is babase.UIScale.MEDIUM else
                    (295, -10)
                )
            )
        )

        self._text_color = (1, 1, 1)
        self._popup_party_member_client_id: Optional[int] = None
        self._popup_party_member_account: Optional[str] = None
        self._popup_party_member_is_host: Optional[bool] = None
        self._firstcall = True

        self._r = 'partyWindow'

        self._chat_texts: List[str] = [] # type: ignore
        self._chat_text_widgets: List[bui.Widget] = []
        self._roster: Optional[List[Dict[str, Any]]] = None
        self._name_widgets: List[bui.Widget] = []
        self._name_texts: List[str] = []
        """Player Names Text Widget"""

        self._pressed_textwidget_text: Optional[str] = ''
        self._pressed_textwidget: Optional[bui.Widget] = None

        self._current_chosen_text: str = ''
        self._current_chosen_text_widget: bui.Widget | None = None
        self._current_chosen_text_id: int = -1
        self._current_chosen_text_color: tuple[float, float, float] = (1, 1, 1)

        self._translate_button_pressed: bool | None = False

        self._popup_type: Optional[str] = None
        """To Define Popup Type When A PopupMenuWindow Triggered, and Run `popup_menu_selected_choice`"""

        ### TEXT ##
        # Muted Text
        self._muted_text = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            scale=1.7,
            h_align='center',
            v_align='center',
            text=get_lang_text('partyWindow.chatMutedText'))

        self._is_1_4_server_text = None
        reset_global_vars()

        self._empty_str = bui.textwidget(
            parent=self._root_widget,
            scale=1.1,
            size=(0, 0),
            position=(self._width * 0.5,
                        self._height - 65),
            maxwidth=self._width * 0.85,
            h_align='center',
            v_align='center')

        # Title Text
        host_info = bs.get_connection_to_host_info_2()
        if host_info and host_info.name: 
            self.title = babase.Lstr(value=host_info.name)
        else:
            self.title = f"{get_lang_text('partyWindow.titleText')}"
        title_text_y_pos = (self._height - 20 if self.uiscale is babase.UIScale.SMALL else
                            self._height - 20 if self.uiscale is babase.UIScale.MEDIUM else
                            self._height - 20)
        ### BUTTONS ###
        title_width = self._width * 0.4
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=1.8,
            color=(0.5, 0.7, 0.5),
            text=self.title,
            size=(title_width, 30),
            position=(self._width * 0.3, title_text_y_pos),
            maxwidth=title_width*1.35,
            h_align='center',
            selectable=True,
            autoselect=False,
            click_activate=True,
            on_activate_call=CallStrict(self._get_party_name),
            v_align='center')

        # Menu Button
        self._menu_button = bui.buttonwidget(
            parent=self._root_widget,
            scale=1.5,
            position=(self._width - 150, self._height - 47),
            size=(50, 50),
            label='...',
            autoselect=False,
            button_type='square',
            on_activate_call=bs.WeakCallStrict(self._on_menu_button_press),
            color=self.bg_color,
            iconscale=1.2)

        # Settings Button
        self._settings_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 50),
            scale=1.35,
            button_type='square',
            autoselect=True,
            color=self.bg_color,
            position=(self._width - 65, self._height - 110),
            on_activate_call=self._on_setting_button_press,
            icon=bui.gettexture('settingsIcon'),
            iconscale=1.25)

        # Chat View Type button
        self._chat_name_view_type_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width-25, self._height * 0.745 if self.uiscale is babase.UIScale.SMALL else self._height * 0.80),
            size=(30, 30),
            scale=2.15,
            label='',
            button_type='square',
            autoselect=False,
            icon=bui.gettexture('usersButton'),
            iconscale=1.2,
            color=self.bg_color)
        bui.buttonwidget(edit=self._chat_name_view_type_button, on_activate_call=self._on_chat_view_button_press)

        thanks_ds: str = f'{get_lang_text("thanks")}!'
        self._thanks_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(45, 30),
            scale=2.15,
            label=thanks_ds,
            button_type='square',
            color=self.bg_color,
            position=(self._width-25, self._height * 0.615 if not self.uiscale is babase.UIScale.SMALL else self._height * 0.55),
        )
        bui.buttonwidget(
            edit=self._thanks_button,
            on_activate_call=CallStrict(
                self._start_button_delay,
                self._thanks_button,
                thanks_ds,
                get_random_thanks_word,
                thanks_delay
            ),
            label=(
                thanks_ds if ButtonDelayHandler().get_delay(thanks_ds) is False else
                ButtonDelayHandler().continue_delay(self._thanks_button, thanks_ds)
            )
        )

        #sorry_ds: str = f'{get_lang_text("sorry")}!'
        #self._sorry_button = bui.buttonwidget(
        #    parent=self._root_widget,
        #    size=(45, 30),
        #    scale=2.15,
        #    label=sorry_ds,
        #    button_type='square',
        #    color=self.bg_color,
        #    position=(self._width-25, self._height * 0.4 if not self.uiscale is babase.UIScale.SMALL else self._height * 0.45),
        #)
        #bui.buttonwidget(
        #    edit=self._sorry_button,
        #    on_activate_call=Call(
        #        self._start_button_delay,
        #        self._sorry_button,
        #        sorry_ds,
        #        get_random_sorry_word,
        #        sorry_delay
        #    ),
        #    label=(
        #        sorry_ds if ButtonDelayHandler().get_delay(sorry_ds) is False else
        #        ButtonDelayHandler().continue_delay(self._sorry_button, sorry_ds)
        #    )
        #)

        # Responder settings button
        self._responder_settings_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(30, 35),
            scale=1.8,
            label='',
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            position=(self._width - 12.25, 290),
            on_activate_call=ResponderSettingsWindow,
            icon=bui.gettexture('levelIcon'),
            iconscale=1.2)

        self._show_icons_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(30, 35),
            scale=1.8,
            label='',
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            position=(self._width - 12.5, 202.5),
            on_activate_call=self._show_icons_popup_menu,
            icon=bui.gettexture('achievementsIcon'),
            iconscale=1.2)

        # Copy text button
        if party_config.get(CFG_NAME_BUTTON_COPY_PASTE):
            self._copy_button = bui.buttonwidget(
                parent=self._root_widget,
                size=(17.5, 17.5),
                scale=1.9,
                label='©',
                button_type='backSmall',
                autoselect=False,
                enable_sound=False,
                color=self.bg_color,
                position=(self._width - 22.5, 120),
                on_activate_call=self._copy_textfield)
            self._paste_button = bui.buttonwidget(
                parent=self._root_widget,
                size=(17.5, 17.5),
                scale=1.925,
                label='Ⓟ',
                button_type='square',
                autoselect=False,
                enable_sound=False,
                color=self.bg_color,
                position=(self._width + 32.5, 120),
                on_activate_call=self._confirm_paste_textfield)

        # Translate text
        self._translate_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 35),
            scale=1.85,
            label="Trans",
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            position=(self._width - 17.5, 35),
            on_activate_call=self._translate_text_field_delay)

        # Send Button
        self._send_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 35),
            scale=1.85,
            label='',
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            position=(self._width - 120, 35),
            on_activate_call=self._send_chat_message,
            icon=bui.gettexture('rightButton'),
            icon_color=(1, 1, 1),
            iconscale=1.2)

        self._quick_respond_button = None
        if not party_config.get(CFG_NAME_INSTANT_QUICK_RESPOND):
            # Quick Respond Button
            self._quick_respond_button = bui.buttonwidget(
                parent=self._root_widget,
                size=(50, 35),
                scale=1.85,
                label=get_lang_text('quickRespondButton'),
                button_type='square',
                autoselect=False,
                color=self.bg_color,
                position=(60, 35))
            bui.buttonwidget(
                edit=self._quick_respond_button,
                on_activate_call=Call(self._show_quick_respond_window, self._quick_respond_button)
            )

        # Next message button
        chat_navigator_button_scale = 32.5
        chat_navigator_x_pos = -20
        self._next_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(chat_navigator_x_pos, 20),
            size=(chat_navigator_button_scale, chat_navigator_button_scale + 3),
            label=babase.charstr(SpecialChar.DOWN_ARROW),
            button_type='square',
            autoselect=False,
            repeat=True,
            color=self.bg_color,
            scale=1.775,
            on_activate_call=CallStrict(self._next_message))

        # Previous message button
        previous_button_height = (
            self._height * 0.0425 + (self._height * 0.0425) * 2 if self.uiscale is babase.UIScale.SMALL else
            self._height * 0.0425 + (self._height * 0.0425) * 1.275 if self.uiscale is babase.UIScale.MEDIUM else
            self._height * 0.0425 + (self._height * 0.0425) * 0.85)
        self._previous_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(chat_navigator_x_pos, previous_button_height),
            size=(chat_navigator_button_scale, chat_navigator_button_scale + 3),
            label=babase.charstr(SpecialChar.UP_ARROW),
            button_type='square',
            autoselect=False,
            repeat=True,
            color=self.bg_color,
            scale=1.775,
            on_activate_call=CallStrict(self._previous_message))

        # Refresh Selected Msg Button
        refresh_button_pos = (
            (chat_navigator_x_pos-80, self._height * 0.075) if self.uiscale is babase.UIScale.SMALL else
            (chat_navigator_x_pos-80, self._height * 0.0575) if self.uiscale is babase.UIScale.MEDIUM else
            (chat_navigator_x_pos-80, self._height * 0.055))
        self._refresh_selected_msg_button = bui.buttonwidget(
            parent=self._root_widget,
            position=refresh_button_pos,
            size=(40, 45),
            scale=1.6,
            label='',
            color=self.bg_color,
            on_activate_call=CallStrict(self._on_refresh_press),
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.2)

        left_up_button_part_y_pos = self._height - 42.5
        # Cancel Button
        self._cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            scale=1.5,
            position=(50, left_up_button_part_y_pos),
            size=(50, 50),
            label='',
            on_activate_call=self.close,
            autoselect=False,
            color=self.bg_color,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)
        bui.containerwidget(edit=self._root_widget, cancel_button=self._cancel_button)

        self._ping_button = None
        self._ip_port_button = None
        ping_button_y_pos = left_up_button_part_y_pos - 80
        ip_button_y_pos = ping_button_y_pos - 85
        if host_info:
            if party_config.get(CFG_NAME_BUTTON_PING):
                global _ping_button
                # Ping button
                self._ping_button = bui.buttonwidget(
                    parent=self._root_widget,
                    scale=1.5,
                    position=(-85, ping_button_y_pos),
                    size=(75, 75),
                    autoselect=False,
                    button_type='square',
                    label=f'{round(_server_ping)}',
                    on_activate_call=self._send_ping,
                    color=self.bg_color,
                    textcolor=_get_ping_color(),
                    text_scale=2.3,
                    iconscale=1.2)
                _ping_button = self._ping_button

            # IP button
            if party_config.get(CFG_NAME_BUTTON_IP):
                self._ip_port_button = bui.buttonwidget(
                    parent=self._root_widget,
                    scale=1.98,
                    position=(-40, ip_button_y_pos),
                    size=(35, 35),
                    label='IP',
                    button_type='square',
                    autoselect=False,
                    color=self.bg_color,
                    on_activate_call=self._ip_port_msg)

        # Change name roster view button
        roster_name_toggle_button_y_pos = ip_button_y_pos - 110 + (100 if not host_info else 0)
        self._change_name_roster_view_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(-40, roster_name_toggle_button_y_pos),
            size=(40, 40),
            label='',
            scale=1.9,
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            icon=bui.gettexture('achievementSharingIsCaring' if not roster_name_viewer else 'achievementTeamPlayer'),
            enable_sound=False,
            iconscale=1.2,
            on_activate_call=self._change_name_roster_viewer)

        # Gather Window button
        gather_button_y_pos = roster_name_toggle_button_y_pos - 100
        if host_info:
            self._gather_button = bui.buttonwidget(
                parent=self._root_widget,
                position=(-40, gather_button_y_pos),
                size=(40, 40),
                label='',
                scale=1.9,
                button_type='square',
                autoselect=False,
                color=self.bg_color,
                icon=bui.gettexture('controllerIcon'),
                enable_sound=False,
                iconscale=1.2,
                on_activate_call=CallStrict(_open_gather_window, self.close) #Call(screenmessage, 'Unavailable, Sorry :(', COLOR_SCREENCMD_ERROR)
            )
        #try:
            #if is_gather_window:
                #is_gather_window.get_root_widget().delete()
        #except Exception as e:
            #screenmessage(f"Error Deleting GatherWindow! {e}", COLOR_SCREENCMD_ERROR)
            #bui.getsound('error').play(1.5)

        # Rejoin button
        rejoin_button_y_pos = gather_button_y_pos - 100 + (100 if not host_info else 0)
        self._rejoin_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(-40, rejoin_button_y_pos),
            size=(40, 40),
            label='',
            scale=1.9,
            button_type='square',
            autoselect=False,
            color=self.bg_color,
            icon=bui.gettexture('replayIcon'),
            enable_sound=False,
            iconscale=1.2,
            on_activate_call=_rejoin_server)

        """Our Text Field, Where We Express Our Attitude/Expression"""
        self._text_field = txt = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(self._width * 0.62, 45) if party_config.get(CFG_NAME_INSTANT_QUICK_RESPOND) else (self._width * 0.56, 45), # Size
            position=(self._width * 0.2695, 57.5) if party_config.get(CFG_NAME_INSTANT_QUICK_RESPOND) else (self._width * 0.32, 57.5), # Pos
            maxwidth=self._width * 1.075 if party_config.get(CFG_NAME_INSTANT_QUICK_RESPOND) else self._width * 0.985, # Maxwidth
            scale=1.8,
            text=_last_text_field_msg if party_config.get(CFG_NAME_SAVE_LAST_TYPED_MSG) and _last_text_field_msg else "",
            shadow=0.3,
            flatness=1.0,
            description=babase.Lstr(resource=self._r + '.chatMessageText'),
            autoselect=True,
            v_align='center',
            corner_scale=0.7
        )
        bui.textwidget(edit=txt, on_return_press_call=btn.activate)
        global _text_field
        _text_field = self._text_field

        ### TEXT SCROLLER ###
        self._scroll_width = self._width - 80
        self._scroll_size = (self._scroll_width, self._height - 240)
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=self._scroll_size,
            position=(50, 110),
            color=self.bg_color)
        self._columnwidget = bui.columnwidget(parent=self._scrollwidget, border=2, margin=0)
    #    bui.widget(edit=self._menu_button, down_widget=self._columnwidget)

        # Window Part
        bui.widget(
            edit=self._scrollwidget,
            autoselect=False,
            left_widget=self._cancel_button,
            up_widget=self._cancel_button,
            down_widget=self._text_field)
        bui.widget(
            edit=self._columnwidget,
            autoselect=False,
            up_widget=self._cancel_button,
            down_widget=self._text_field)
        bui.containerwidget(edit=self._root_widget, selected_child=txt, color=self.bg_color)

        ping_server_recall()
        self.ping_timer = babase.AppTimer(
            3,
            ping_server_recall,
            repeat=True)#,
            #timetype=babase.TimeType.REAL)
        self._update_timer = babase.AppTimer(
            1.25,
            bs.WeakCallStrict(self._update),
            repeat=True)#,
            #timetype=babase.TimeType.REAL)
        self._update()
        self._refresh_text()

    def _start_button_delay(self, button: bui.Widget, key: str, msg_func: Callable[[], str], delay: float):
        ButtonDelayHandler().start(
            button_widget=button,
            delay_key=key,
            message=msg_func,
            delay_time=delay
        )

    def _show_icons_popup_menu(self):
        choices = SPECIAL_CHARS

        specialchar = CHOSEN_ICON_TO_SHOW
        if specialchar not in SPECIAL_CHARS: current_choice: str = ''
        else: current_choice: str = specialchar
        self._focus_to_text_field()
        self._popup_type = POPUP_MENU_TYPE_SHOW_ICONS
        PopupMenuWindow(
            position=self._show_icons_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            color=self.bg_color, # type: ignore
            choices=choices,
            current_choice= current_choice, #choices[63], # Show Dragon
            delegate=self)

    def _on_chat_view_button_press(self):
        self._popup_type = POPUP_MENU_TYPE_CHAT_VIEWER_TYPE
        choices, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_CHAT_VIEWER_TYPE)

        choices.insert(0, 'chatShowOrHideCid')
        cfg = party_config
        if cfg[CFG_NAME_CHAT_VIEWER_SHOW_CID]:
            view_cid_text = 'chatHideCid'
        else:
            view_cid_text = 'chatShowCid'
        choices_display.insert(0, get_lang_text(view_cid_text))

        choices.append('chatViewOff')
        choices_display.append(get_lang_text('chatViewOff'))

        view_type = party_config.get(CFG_NAME_CHAT_VIEWER_TYPE)
        the_choice = ''
        if view_type == chat_view_type_profile_name:
            the_choice = 'chatViewProfile'

        if view_type == chat_view_type_account_name:
            the_choice = 'chatViewAccount'

        if view_type == chat_view_type_multi:
            the_choice = 'chatViewMulti'

        if view_type == chat_view_type_multi_v2:
            the_choice = 'chatViewMultiV2'

        current_choice = the_choice if view_type else choices[-1]

        PopupMenuWindow(
            position=self._chat_name_view_type_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            color=self.bg_color, # type: ignore
            choices=choices,
            current_choice=current_choice,
            choices_display=_create_baLstr_list(choices_display),
            delegate=self)

    def _on_refresh_press(self):
        if self._current_chosen_text_id != -1:
            if party_config[CFG_NAME_HIGHLIGHT_CHOSEN_TEXT]:
                # Reset previous widget text and color
                previous_widget = self._chat_text_widgets[self._current_chosen_text_id]
                _previous_text = bui.textwidget(query=self._chat_text_widgets[self._current_chosen_text_id])
                previous_text = _previous_text.split(CHOSEN_TEXT_HIGHLIGHT_MARK, 1)[1] if CHOSEN_TEXT_HIGHLIGHT_MARK and _previous_text.startswith(CHOSEN_TEXT_HIGHLIGHT_MARK) else _previous_text
                bui.textwidget(edit=previous_widget, text=previous_text, color=self._current_chosen_text_color)
            self._current_chosen_text_id = -1
        bui.textwidget(edit=self._text_field, text='')
        self._focus_to_text_field()

    def on_chat_message(self, msg: str) -> None:
        """
        Called when a new chat message comes through.
        Our Main Gate To Get Chats While Opening PartyWindow :)
        """
        if party_config[CFG_NAME_PARTY_CHAT_MUTED]: return
        if auto_responder:
            auto_responder.pesan = bs.get_chat_messages() # Ah, shouldn't do this
            auto_responder.master_chats(msg)
        self._add_msg(msg=msg, sent=True)
     #   screenmessage(msg)

    def _add_msg(self, msg: str, sent: bool = False) -> None:
        """Add Messages Into Scroller"""
        _name, message = msg.split(PNAME_AND_MSG_SPLITTER, 1)

        if party_config[CFG_NAME_COLORFUL_CHATS]:
            player_color = color_tracker._get_sender_color(_name)
            while player_color == TEXTWIDGET_DEFAULT_COLOR:
                player_color = color_tracker._get_sender_color(_name)
            color = player_color
        else:
            color = TEXTWIDGET_DEFAULT_COLOR
        color = (color[0] + TEXTWIDGET_CHANGE_COLOR_RANGE,
                 color[1] + TEXTWIDGET_CHANGE_COLOR_RANGE,
                 color[2] + TEXTWIDGET_CHANGE_COLOR_RANGE)

        #touchable_text_widget = False
        text_widget = bui.textwidget( # Our text widget for each line of messages
            parent=self._columnwidget,
            text=msg,
            h_align='left',
            v_align='center',
            size=(self._scroll_width-25, 27.5), #(maxwidth, 20) if touchable_text_widget else (55, 13.5),
            #position=(0, 0),
            scale=1, #0.545 if not touchable_text_widget else 1,
            color=color,
            maxwidth=self._scroll_width*0.975,
            shadow=1.65,
            autoselect=True,
            selectable=True,
            always_highlight=True,
            click_activate=True,
            flatness=1.65)

        bui.textwidget(
            edit=text_widget,
            on_activate_call=CallStrict(self._on_party_text_press, msg, text_widget))

        self._chat_text_widgets.append(text_widget)
        self._chat_texts.append(msg)
        if party_config.get(CFG_NAME_FOCUS_TO_LAST_MSG):
            if text_widget and text_widget.exists():
                bui.columnwidget(
                    edit=self._columnwidget, 
                    visible_child=text_widget)

        if (party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) or party_config.get(CFG_NAME_CHAT_VIEWER_SHOW_CID)) or is_muted_player:
            if not any(_name.startswith(server) for server in SERVER_NAMES):
                Thread(target=NameMatcher, args=(msg, self._roster, matched_name, text_widget, True)).start()

        #if len(_chat_texts) > maximum_party_window_chats: # Party Winodw max chats
            #widget = self._chat_text_widgets.pop(0)
            #widget.delete()
            #self._chat_texts.pop(0)
            #if self._current_chosen_text_id != -1:
                #self._current_chosen_text_id -= 1 # Make sure to keep select the selected msg because its tilted

        if sent:
            if not party_config.get(CFG_NAME_CHAT_MUTED) and babase.app.config.get('Chat Muted'): bui.getsound('tap').play()
            global _pending_msgs
            _pending_msgs.append(msg)
            if auto_responder:
                babase.apptimer(0.2, auto_responder.manual_log_chats)
                #auto_responder.manual_log_chats(_pending_msgs)


    def _refresh_text(self, data: Dict[str, Any] = {}):
        global _chat_texts
        if not party_config[CFG_NAME_PARTY_CHAT_MUTED]:
            if self._chat_text_widgets:
                while self._chat_text_widgets:
                    first = self._chat_text_widgets.pop()
                    first.delete()
            while len(_chat_texts) > maximum_party_window_chats and max(200, len(_chat_texts)) > maximum_bombsquad_chat_messages:
                _chat_texts.pop(0)
            bs_msg: list[str] = bs.get_chat_messages()

            # Prioritize bs_msg if it has 40 messages
            if len(bs_msg) >= maximum_bombsquad_chat_messages:
                # Handle duplicate messages if _chat_texts length exceeds bsmaxchats (40)
                if len(_chat_texts) > maximum_bombsquad_chat_messages:
                    # Cut the last 40 messages to prevent duplicates
                    cutted_chat_texts = _chat_texts[:len(_chat_texts)-len(bs_msg)-1]

                    combined_msgs = cutted_chat_texts + bs_msg

                    # Get the last messages based on maximum_party_window_chats
                    msgs = combined_msgs[-min(maximum_party_window_chats, len(combined_msgs)):]
                else:
                    msgs = bs_msg
            else:
                msgs = bs_msg
            msgs = msgs[-min(len(msgs), maximum_party_window_chats):]
            for msg in msgs:
                self._add_msg(msg) # Hope the procces wont slowdown devices, turns out it does

        if self._chat_text_widgets:
            bui.columnwidget(
                edit=self._columnwidget, 
                visible_child=self._chat_text_widgets[-1])

        self._update()

    def _on_party_text_press(self, text: str, widget: bui.Widget):
        name, message = text.split(PNAME_AND_MSG_SPLITTER, 1)
        self._pressed_textwidget_text = text # Make sure its pname and the msg not splitted yet
        self._pressed_textwidget = widget
        choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_CHAT_PRESS)

        # Using current session may cause less accurate current player
        chosen_player_data = current_namelist if current_namelist else current_session_namelist

        # Show on party member press
        player_acc = _match_player_name(player_name=name, player_data=chosen_player_data)
        is_player_data = chosen_player_data.get(player_acc)
        if is_player_data:
            choices_key.append('playerMenuOptionFromText')
            choices_display.append(get_lang_text('playerMenuOptionFromText'))
            self._popup_party_member_client_id = is_player_data.get(player_acc, {}).get('client_id')
            self._popup_party_member_account = player_acc
        else:
            pass #self._refresh_text()

        self._popup_type = POPUP_MENU_TYPE_CHAT_PRESS

        pos: Tuple[float, float] = widget.get_screen_space_center()
        pos = (pos[0] + (pos[0] * 100), pos[1]) if self.uiscale is UIScale.SMALL else (pos[0] + (pos[0] * 1.1), pos[1])
        #print(f"Popupmenu textwidget pos 2: {pos}")
        PopupMenuWindow(
            position=pos,
            color=self.bg_color, # type: ignore
            scale= _get_popup_window_scale(),
            choices=choices_key,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices_key[0],
            delegate=self)

    def _on_menu_button_press(self) -> None:
        choices_key, choices_display = get_choices_key_lang_text(CHOICES_KEY_MENU)

        #if not self._roster:
        #    choices_key.append('credit')
        #    choices_display.append(get_lang_text('credit&help'))

        self._focus_to_text_field()
        self._popup_type = POPUP_MENU_TYPE_MENU_PRESS
        PopupMenuWindow(
            position=self._menu_button.get_screen_space_center(),
            color=self.bg_color, # type: ignore
            scale= _get_popup_window_scale(),
            choices=choices_key,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices_key[0],
            delegate=self)

    def _update(self, force: bool = False) -> None:
        if self._firstcall:
            self._roster = []
            self._firstcall = False
       #     self._chat_text_widgets: List[bui.Widget] = []
            """if not party_config[CFG_NAME_PARTY_CHAT_MUTED]:
                msgs = bs.get_chat_messages()
                for msg in msgs:
                    self._add_msg(msg)"""

        if party_config.get(CFG_NAME_PARTY_CHAT_MUTED):
            bui.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.3))
            # clear any chat texts we're showing
            while self._chat_text_widgets:
                first = self._chat_text_widgets.pop()
                first.delete()
        else:
            if self._muted_text:
                bui.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.0))

        roster = bs.get_game_roster()
        if roster == self._roster and not force:
            return

        global is_1_4_server, is_muted_player
        self._roster = roster

        # Lets clear name widget to refresh player showing
        for name_widget in self._name_widgets:
            name_widget.delete()
        self._name_widgets.clear()
        self._name_texts.clear()

        if not self._roster:
            top_section_height = 60
            bui.textwidget(
                edit=self._empty_str,
                text=get_lang_text('partyWindow.emptyText'))
            if self._is_1_4_server_text:
                bui.textwidget(edit=self._is_1_4_server_text, text='')
                self._is_1_4_server_text.delete()
                self._is_1_4_server_text = None
                is_1_4_server = False
        else:
            if self._title_text and self._title_text.exists():
                bui.textwidget(edit=self._title_text, text=self.title)
            columns = 1 if len(self._roster) == 1 else 2 if len(self._roster) == 2 else 3
            rows = int(math.ceil(float(len(self._roster)) / columns))
            c_width = (self._width * 0.865) / max(3, columns)
            c_width_total = c_width * columns
            c_height = 45
            c_height_total = c_height * rows
            global players_anti_abuse_exception
            friend = players_anti_abuse_exception # Friend
            notfriend = player_blacklisted_list # Not Friend
            hated = player_muted_list
            master: str = ''
            p_str: str = ''
            p_acc: str = ''
            for y in range(rows):
                for x in range(columns):
                    index = y * columns + x
                    if index < len(self._roster):
                        t_scale = 1.275
                        pos: tuple[float, float] = (self._width * 0.545 - c_width_total * 0.5 + c_width * x - 25, self._height - 65 - c_height * y - 15)

                        # if there are players present for this client, use
                        # their names as a display string instead of the
                        # client spec-string
                        p_acc: str = self._roster[index]['display_string']
                        if p_acc and p_acc[0] not in SPECIAL_CHARS and not p_acc.startswith('<HIDDEN>'):
                            p_acc = babase.charstr(SpecialChar.V2_LOGO) + p_acc
                            is_1_4_server = True
                        elif p_acc.startswith('<HIDDEN>'):
                            global is_hidden_names_by_server
                            is_hidden_names_by_server = True
                        if p_acc in MY_MASTER:
                            master = p_acc
                        try:
                            if not roster_name_viewer:
                                if self._roster[index]['players']:
                                    # if there's just one, use the full name;
                                    # otherwise combine short names
                                    if len(self._roster[index]['players']) == 1:
                                        p_str = self._roster[index]['players'][0]['name_full']
                                    else:
                                        p_str = ('/'.join([entry['name'] for entry in self._roster[index]['players']]))
                                        if len(p_str) > P_NAME_STR_MAX_WIDTH:
                                            # Cut long player name str
                                            p_str = p_str[:P_NAME_STR_MAX_WIDTH] + '...'
                                else:
                                    p_str = self._roster[index]['display_string']
                                    if p_str and p_str[0] not in SPECIAL_CHARS and not p_str.startswith('<HIDDEN>'):
                                        p_str = babase.charstr(SpecialChar.V2_LOGO) + p_str
                                        is_1_4_server = True
                            else:
                                p_str = f"{p_acc} [{self._roster[index]['client_id']}]" if party_config.get(CFG_NAME_INCLUDE_CID_IN_QC_NAME_CHANGER) else p_acc
                        except Exception as e:
                            print(f'Error calcing client name str: {e}')
                            p_str = '???'

                        if '"' in p_str: p_str = p_str.replace('"', '\"')
                        if "'" in p_str: p_str = p_str.replace("'", "\'")

                        color: tuple[float, float, float] = (1, 1, 1)
                        if any(p_acc == name for name in MY_MASTER): # Its My Master
                            col_range = 0.5
                            color = (self.bg_color[0]+col_range, self.bg_color[1]+col_range, self.bg_color[2]+col_range)
                        elif p_acc in f"{babase.charstr(babase.SpecialChar.V2_LOGO)}LessPal":
                            color = COLORS.get('pink', color)
                        elif p_acc in friend:
                            if player_warnings.get(p_acc):
                                color = COLORS.get('lime', color)
                            elif p_acc in hated:
                                color = COLORS.get('blue', color)
                            else:
                                color = COLORS.get('cyan', color)
                        elif p_acc in notfriend:
                            if player_warnings.get(p_acc):
                                color = COLORS.get('orange', color)
                            else:
                                color = COLORS.get('brown', color)
                        elif p_acc in hated:
                            if player_warnings.get(p_acc):
                                color = COLORS.get('black', color)
                            else:
                                color = COLORS.get('red', color)
                        elif player_warnings.get(p_acc):
                            color = COLORS.get('yellow', color)
                        elif p_acc in friend and p_acc in notfriend:
                            color = COLORS.get('purple', color)

                        how_many_p_with_this_str = 0
                        if p_str in self._name_texts:
                            how_many_p_with_this_str = self._name_texts.count(p_str) + 1
                            that_same_name_widget_index = self._name_texts.index(p_str) + 1
                            bui.textwidget(edit=self._name_widgets[that_same_name_widget_index], text=f"{p_str} {how_many_p_with_this_str-1}")

                        widget = bui.textwidget(
                            parent=self._root_widget,
                            position=(pos[0], pos[1]),
                            scale=t_scale,
                            size=(c_width * 0.85, 30),
                            maxwidth=c_width * 0.85,
                            color=color,
                            selectable=True,
                            click_activate=True,
                            autoselect=True,
                            text=(p_str if not how_many_p_with_this_str else f"{p_str} {how_many_p_with_this_str}"),
                            h_align='left',
                            v_align='center')
                        self._name_widgets.append(widget)
                        self._name_texts.append(p_str)

                        # in newer versions client_id will be present and
                        # we can use that to determine who the host is.
                        # in older versions we assume the first client is
                        # host
                        if self._roster[index]['client_id'] is not None:
                            is_host = self._roster[index]['client_id'] == -1
                        else:
                            is_host = (index == 0)

                        # FIXME: Should pass client_id to these sort of
                        #  calls; not spec-string (perhaps should wait till
                        #  client_id is more readily available though).
                        bui.textwidget(edit=widget,
                            on_activate_call=CallStrict(
                                self._on_party_member_press, # Action 
                                self._roster[index]['client_id'],
                                is_host,
                                widget,
                                p_acc)
                            )

                        pos: tuple[float, float] = (self._width * 0.53 - c_width_total * 0.5 + c_width * x, self._height - 65 - c_height * y)

                        # Make the assumption that the first roster
                        # entry is the server.
                        # FIXME: Shouldn't do this.
                        if is_host:
                            twd = min(
                                c_width * 0.85,
                                _babase.get_string_width(p_str, suppress_warning=True) * t_scale)
                            self._name_widgets.append(
                                bui.textwidget(
                                    parent=self._root_widget,
                                    position=(pos[0] + twd + 1 - 42.5, pos[1] - 0.25),
                                    size=(0, 0),
                                    h_align='left',
                                    v_align='center',
                                    maxwidth=c_width * 0.9 - twd,
                                    color=(0.1, 1, 0.1, 0.5),
                                    text=f"({get_lang_text('partyWindow.hostText')})",
                                    scale=0.85,
                                    shadow=1.75,
                                    flatness=1.75))
                        if p_acc in hated:
                            is_muted_player = True
            bui.textwidget(edit=self._empty_str, text='')
            if not master:
                babase.AppTimer(1, Call(self._update, True))
                print(f"WARNING, Master Not Found On Force: {force}")
                if force:
                    my_master_not_in_game()

            if self._ping_button and self._ping_button.exists():
                bui.buttonwidget(
                    edit=self._ping_button,
                    label=f'{round(_server_ping)}',
                    textcolor=_get_ping_color())
            bui.scrollwidget(edit=self._scrollwidget, size=(self._scroll_width, max(200, self._height - 139 - c_height_total - 25)))
            if self._chat_text_widgets:
                bui.containerwidget(
                    edit=self._columnwidget, 
                    visible_child=self._chat_text_widgets[-1])

        if is_1_4_server and not self._is_1_4_server_text:
            v1_4_server_text = get_lang_text('v1.4ServerTitle')
            v1_4_server_text_send = get_lang_text('v1.4ServerMsg')
            is_1_4_server_x_size = (len(v1_4_server_text) * 12, 30)
            self._is_1_4_server_text = bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.425, 0),
                color=(1, 1, 1, 0.35),
                size=is_1_4_server_x_size,
                scale=1.5,
                h_align='center',
                v_align='center',
                selectable=True,
                autoselect=False,
                click_activate=True,
                on_activate_call=Call(screenmessage, v1_4_server_text_send, COLOR_SCREENCMD_NORMAL),
                text=v1_4_server_text)

    def _change_name_roster_viewer(self):
        global roster_name_viewer
        if roster_name_viewer:
            roster_name_viewer = 0 # Profile Name
            if self._change_name_roster_view_button and self._change_name_roster_view_button.exists():
                bui.buttonwidget(
                    edit=self._change_name_roster_view_button,
                    icon=bui.gettexture('achievementSharingIsCaring')
                )
        else:
            roster_name_viewer = 1 # Account Name
            if self._change_name_roster_view_button and self._change_name_roster_view_button.exists():
                bui.buttonwidget(
                    edit=self._change_name_roster_view_button,
                    icon=bui.gettexture('achievementTeamPlayer')
                )
        bui.getsound('click01').play(1.75)
        self._update(force=True)

    def _get_party_name(self):
        info = bs.get_connection_to_host_info_2()
        if info is not None and info.name != '':
            party_name = info.name
            _edit_text_field_global(party_name, 'replace')

    def _on_party_member_press(self, client_id: Optional[int], is_host: bool, widget: bui.Widget, player_name: str) -> None: # type: ignore
        # if we're the host, pop up 'kick' options for all non-host members
        # Oops, added player_name parameter
        if bs.get_foreground_host_session() is not None:
            pass
        else:
            # kick-votes appeared in build 14248
            host_info = bs.get_connection_to_host_info_2()
            if host_info is not None and host_info.build_number < 14248:
                return

        if client_id is None:
            self._update()
            self._refresh_text()

        uiscale = bui.app.ui_v1.uiscale
        choices, _choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_PARTY_MEMBER_PRESS)

        choices_display: list[str] = []
        for choice_display in _choices_display:
            if choice_display == get_lang_text('adminkick'):
                if client_id == -1:
                    choices.remove('adminkick')
                    continue
                choice_display = choice_display.format(client_id)

            if choice_display == get_lang_text('adminremove'):
                if client_id == -1:
                    choices.remove('adminremove')
                    continue
                choice_display = choice_display.format(client_id)

            elif choice_display == get_lang_text('warnInfo'):
                if client_id == -1:
                    choices.remove('warnInfo')
                    continue
                global player_warnings
                info = get_player_info_with_cid(clientID=client_id)
                if not info and not player_name:
                    screenmessage(get_lang_text('playerInfoNotFound'), COLOR_SCREENCMD_NORMAL)
                    choices.remove('warnInfo')
                    continue
                name = info['account'] if info else player_name
                if '"' in name: name = name.replace('"', '\\"')
                if "'" in name: name = name.replace("'", "\\'")
                player_warning = player_warnings.get(name, 0)
                choice_display = choice_display.format(player_warning)

            choices_display.append(choice_display)

        choices.append('customCommands')
        choices_display.append(get_lang_text('customCommands'))

        self._popup_type = POPUP_MENU_TYPE_PARTY_MEMBER_PRESS
        self._popup_party_member_client_id = client_id
        self._popup_party_member_account = player_name
        self._popup_party_member_is_host = is_host

        if widget.exists():
            PopupMenuWindow(
                position=widget.get_screen_space_center(),
                color=self.bg_color, # type: ignore
                scale=_get_popup_window_scale(),
                choices=choices,
                choices_display=_create_baLstr_list(choices_display),
                current_choice=choices[0],
                delegate=self)
        else:
            """"""

    def _replace_icon_key(self, msg: str) -> str:
        if '\\flhi' in msg: msg = msg.replace('\\flhi', babase.charstr(SpecialChar.FLAG_INDIA))  # india
        if '\\flus' in msg: msg = msg.replace('\\flus', babase.charstr(SpecialChar.FLAG_UNITED_STATES)) # United States
        if '\\flmx' in msg: msg = msg.replace('\\flmx', babase.charstr(SpecialChar.FLAG_MEXICO)) # Mexico
        if '\\flgm' in msg: msg = msg.replace('\\flgm', babase.charstr(SpecialChar.FLAG_GERMANY)) # Germany
        if '\\flbr' in msg: msg = msg.replace('\\flbr', babase.charstr(SpecialChar.FLAG_BRAZIL)) # Brazil
        if '\\flru' in msg: msg = msg.replace('\\flru', babase.charstr(SpecialChar.FLAG_RUSSIA)) # Russia
        if '\\flch' in msg: msg = msg.replace('\\flch', babase.charstr(SpecialChar.FLAG_CHINA)) # China
        if '\\fluk' in msg: msg = msg.replace('\\fluk', babase.charstr(SpecialChar.FLAG_UNITED_KINGDOM)) # United Kingdom
        if '\\flca' in msg: msg = msg.replace('\\flca', babase.charstr(SpecialChar.FLAG_CANADA)) # Canada
        if '\\fljp' in msg: msg = msg.replace('\\fljp', babase.charstr(SpecialChar.FLAG_JAPAN)) # Japan
        if '\\flfr' in msg: msg = msg.replace('\\flfr', babase.charstr(SpecialChar.FLAG_FRANCE)) # France
        if '\\flid' in msg: msg = msg.replace('\\flid', babase.charstr(SpecialChar.FLAG_INDONESIA)) # Indonesia
        if '\\flit' in msg: msg = msg.replace('\\flit', babase.charstr(SpecialChar.FLAG_ITALY)) # Italy
        if '\\flsk' in msg: msg = msg.replace('\\flsk', babase.charstr(SpecialChar.FLAG_SOUTH_KOREA)) # South Korea
        if '\\flnl' in msg: msg = msg.replace('\\flnl', babase.charstr(SpecialChar.FLAG_NETHERLANDS)) # Netherlands
        if '\\flae' in msg: msg = msg.replace('\\flae', babase.charstr(SpecialChar.FLAG_UNITED_ARAB_EMIRATES)) # United Arab Emirates
        if '\\flqt' in msg: msg = msg.replace('\\flqt', babase.charstr(SpecialChar.FLAG_QATAR)) # Qatar
        if '\\fleg' in msg: msg = msg.replace('\\fleg', babase.charstr(SpecialChar.FLAG_EGYPT)) # Egypt
        if '\\flkw' in msg: msg = msg.replace('\\flkw', babase.charstr(SpecialChar.FLAG_KUWAIT)) # Kuwait
        if '\\flag' in msg: msg = msg.replace('\\flag', babase.charstr(SpecialChar.FLAG_ALGERIA)) # Algeria
        if '\\flsa' in msg: msg = msg.replace('\\flsa', babase.charstr(SpecialChar.FLAG_SAUDI_ARABIA)) # Saudi Arabia
        if '\\flmy' in msg: msg = msg.replace('\\flmy', babase.charstr(SpecialChar.FLAG_MALAYSIA)) # Malaysia
        if '\\flcz' in msg: msg = msg.replace('\\flcz', babase.charstr(SpecialChar.FLAG_CZECH_REPUBLIC)) # Czech Republic
        if '\\flau' in msg: msg = msg.replace('\\flau', babase.charstr(SpecialChar.FLAG_AUSTRALIA)) # Australia
        if '\\flsg' in msg: msg = msg.replace('\\flsg', babase.charstr(SpecialChar.FLAG_SINGAPORE)) # Singapore
        if '\\flir' in msg: msg = msg.replace('\\flir', babase.charstr(SpecialChar.FLAG_IRAN)) # Iran
        if '\\flpl' in msg: msg = msg.replace('\\flpl', babase.charstr(SpecialChar.FLAG_POLAND)) # Poland
        if '\\flar' in msg: msg = msg.replace('\\flar', babase.charstr(SpecialChar.FLAG_ARGENTINA)) # Argentina
        if '\\flph' in msg: msg = msg.replace('\\flph', babase.charstr(SpecialChar.FLAG_PHILIPPINES)) # Philippines
        if '\\flcl' in msg: msg = msg.replace('\\flcl', babase.charstr(SpecialChar.FLAG_CHILE)) # Chile

        if '\\v2' in msg: msg = msg.replace('\\v2', babase.charstr(SpecialChar.V2_LOGO)) # V2
        if '\\fe' in msg: msg = msg.replace('\\fe', babase.charstr(SpecialChar.FEDORA)) # fedora
        if '\\ha' in msg: msg = msg.replace('\\ha', babase.charstr(SpecialChar.HAL)) # hal
        if '\\yy' in msg: msg = msg.replace('\\yy', babase.charstr(SpecialChar.YIN_YANG)) # yin yang
        if '\\mu' in msg: msg = msg.replace('\\mu', babase.charstr(SpecialChar.MUSHROOM)) # mushroom
        if '\\vh' in msg: msg = msg.replace('\\vh', babase.charstr(SpecialChar.VIKING_HELMET)) # viking helmet
        if '\\sp' in msg: msg = msg.replace('\\sp', babase.charstr(SpecialChar.SPIDER)) # spider
        if '\\pa' in msg: msg = msg.replace('\\pa', babase.charstr(SpecialChar.PARTY_ICON)) # party icon
        if '\\ta' in msg: msg = msg.replace('\\ta', babase.charstr(SpecialChar.TEST_ACCOUNT)) # test account
        if '\\tb' in msg: msg = msg.replace('\\tb', babase.charstr(SpecialChar.TICKET_BACKING)) # ticket backing
        if '\\tr1' in msg: msg = msg.replace('\\tr1', babase.charstr(SpecialChar.TROPHY1)) # trophy 1
        if '\\tr2' in msg: msg = msg.replace('\\tr2', babase.charstr(SpecialChar.TROPHY2)) # trophy 2
        if '\\tr3' in msg: msg = msg.replace('\\tr3', babase.charstr(SpecialChar.TROPHY3)) # trophy 3
        if '\\tr4' in msg: msg = msg.replace('\\tr0a', babase.charstr(SpecialChar.TROPHY0A)) # trophy 0a
        if '\\tr5' in msg: msg = msg.replace('\\tr0b', babase.charstr(SpecialChar.TROPHY0B)) # trophy 0b
        if '\\tr6' in msg: msg = msg.replace('\\tr4', babase.charstr(SpecialChar.TROPHY4)) # trophy 4
        if '\\la' in msg: msg = msg.replace('\\la', babase.charstr(SpecialChar.LOCAL_ACCOUNT)) # local account
        #if '\\al' in msg: msg = msg.replace('\\al', babase.charstr(SpecialChar.ALIBABA_LOGO)) # alibaba logo
        if '\\oc' in msg: msg = msg.replace('\\oc', babase.charstr(SpecialChar.OCULUS_LOGO)) # oculus logo
        if '\\st' in msg: msg = msg.replace('\\st', babase.charstr(SpecialChar.STEAM_LOGO)) # steam logo
        if '\\nv' in msg: msg = msg.replace('\\nv', babase.charstr(SpecialChar.NVIDIA_LOGO)) # nvidia logo
        if '\\mi' in msg: msg = msg.replace('\\mi', babase.charstr(SpecialChar.MIKIROG)) # mikirog
        if '\\gp' in msg: msg = msg.replace('\\gp', babase.charstr(SpecialChar.GOOGLE_PLAY_GAMES_LOGO)) # google play
        if '\\d' in msg: msg = msg.replace('\\d', babase.charstr(SpecialChar.DRAGON)) # dragon
        if '\\c' in msg: msg = msg.replace('\\c', babase.charstr(SpecialChar.CROWN)) # crown
        if '\\h' in msg: msg = msg.replace('\\h', babase.charstr(SpecialChar.HELMET)) # helmet
        if '\\s' in msg: msg = msg.replace('\\s', babase.charstr(SpecialChar.SKULL)) # skull
        if '\\n' in msg: msg = msg.replace('\\n', babase.charstr(SpecialChar.NINJA_STAR)) # ninja star
        if '\\f' in msg: msg = msg.replace('\\f', babase.charstr(SpecialChar.FIREBALL)) # fireball
        if '\\g' in msg: msg = msg.replace('\\g', babase.charstr(SpecialChar.GAME_CIRCLE_LOGO)) # gather
        if '\\m' in msg: msg = msg.replace('\\m', babase.charstr(SpecialChar.MOON)) # moon
        if '\\t' in msg: msg = msg.replace('\\t', babase.charstr(SpecialChar.TICKET)) # ticket
        if '\\bs' in msg: msg = msg.replace('\\bs', babase.charstr(SpecialChar.LOGO)) # logo real
        if '\\j' in msg: msg = msg.replace('\\j', babase.charstr(SpecialChar.DPAD_CENTER_BUTTON)) # joystick
        if '\\e' in msg: msg = msg.replace('\\e', babase.charstr(SpecialChar.EYE_BALL)) # eye ball
        if '\\l' in msg: msg = msg.replace('\\l', babase.charstr(SpecialChar.HEART)) # heart
        if '\\b' in msg: msg = msg.replace('\\b', babase.charstr(SpecialChar.LOGO_FLAT)) # bs logo (2d art)

        return msg


    def _send_chat_message(self) -> None:
        msg: str = bui.textwidget(query=self._text_field)
        bui.textwidget(edit=self._text_field, text='')

        msg = replace_msg_emoji_var_with_emojis(msg)

        if '\\' in msg:
            msg = self._replace_icon_key(msg)

        if not msg or msg == "":
            if party_config.get(CFG_NAME_INSTANT_QUICK_RESPOND):
                self._show_quick_respond_window(self._send_button)
        #        print("Showing Quick Replies Window")
            else:
                chatmessage('ㅤ')
                self._focus_to_text_field()
            return
        else:
            if msg.startswith(CMD_MAIN_PREFIX) and len(msg) > 1 and msg[1].isalpha(): 
                if msg.startswith(cmd_toggle_findall_pdata):
                    #if not identical_all_names:
                        #load_all_names_data()
                    find_player_cmd(message=msg, data_type=all_names, is_master=True, toggle=cmd_toggle_findall_pdata)
                elif msg.startswith(cmd_toggle_find_pdata):
                    #if not identical_all_names:
                        #load_all_names_data()
                    find_player_cmd(message=msg, data_type=current_session_namelist, is_master=True, toggle=cmd_toggle_find_pdata)

                elif msg.startswith(cmd_toggle_all_pdata_window):
                    popup_player_list(msg, all_names)
                elif msg.startswith(cmd_toggle_session_pdata_window):
                    popup_player_list(msg, current_session_namelist)

                elif msg.startswith(cmd_toggle_show_data):
                    show_responder_data_window(msg)

                elif msg.startswith(toggle_add_questions) or msg.startswith(toggle_remove_question):
                    EditableDataPopup(load_func=_load_saved_kunci_jawaban, save_func_dict=_save_kunci_jawaban_to_file, label="Server QnA")

                elif msg.startswith(toggle_add_nick) or msg.startswith(toggle_remove_nick):
                    EditableDataPopup(load_func=_load_nicknames, save_func_list=save_nicknames, label="My Nicknames")

                elif msg.startswith(toggle_add_custom_replies) or msg.startswith(toggle_remove_custom_replies):
                    EditableDataPopup(load_func=_load_saved_custom_replies, save_func_dict=_save_custom_replies_to_file, label="Custom Replies")

                elif msg.startswith(toggle_add_responder_blacklist) or msg.startswith(toggle_remove_responder_blacklist):
                    EditableDataPopup(load_func=load_responder_blacklist_names, save_func_list=save_blacklist_names, is_player=True, label="Blacklisted Player")

                elif msg.startswith(toggle_add_player_anti_abuse_exception) or msg.startswith(toggle_remove_player_anti_abuse_exception):
                    EditableDataPopup(load_func=load_player_name_exceptions, save_func_list=save_player_name_exceptions, label="Player Exceptions")

                elif msg.startswith(toggle_add_anti_abuse_exception_word) or msg.startswith(toggle_remove_anti_abuse_exception_word):
                    EditableDataPopup(load_func=load_anti_abuse_exception_words, save_func_list=save_exception_word, is_player=True, label="Exception Words")

                elif msg.startswith(toggle_info_player_all_pdata):
                    show_player_info_window(msg, all_names)
                elif msg.startswith(toggle_info_player_current_pdata):
                    show_player_info_window(msg, current_session_namelist)

                elif msg.startswith(cmd_toggle_update_pb):
                    load_all_names_data()
                    Thread(target=_all_names_pb_update).start()

                elif msg.startswith(toggle_reset_player_warns):
                    handle_reset_player_warns(msg)

                elif msg.startswith(toggle_reset_all_player_warns):
                    reset_all_player_warnings(cmd=True)

                elif msg.startswith(toggle_add_abuse) or msg.startswith(toggle_remove_abuse):
                    msg = f"{CMD_LOGO_CAUTION} {get_lang_text('use')} {toggle_show_data} {show_data_attr_abuse_data} [{', '.join(abuses_languages)}]"
                    screenmessage(msg, COLOR_SCREENCMD_NORMAL)

                elif msg.startswith(toggle_ping_server):
                    _refresh_server_ip_and_port()
                    try:
                        print('Doing Automatic Pinging')
                        Thread(target=start_pinging_server, args=(_server_ip, _server_port, True)).start()
                    except:
                        try:
                            print("Failed Doing Automatic Pinging: Falling Back To Manual Pinging")
                            do_manual_server_ping(is_cmd=True)
                        except:
                            pass

                ############# Responder Windows #############
                elif msg.startswith(toggle_responder_settings):
                    try:
                        ResponderSettingsWindow()
                        message = 'Responder Setting Window Opened'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
                    except Exception as e:
                        message = f'{CMD_LOGO_CAUTION} Failed Opening Responder Setting Window'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(msg, color=COLOR_SCREENCMD_NORMAL)
                        screenmessage(f'{CMD_LOGO_CAUTION} {e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
                        print_internal_exception(e)

                elif msg.startswith(toggle_internal_all_chats_window):
                    try:
                        message = 'Expanded Chats Window Opened'
                        if internal_all_chats_data:
                            save_internal_all_chats_data(force=True)
                            save_internal_player_chats_data(force=True)
                            InternalChatsPopup("Internal Chats Data")
                        else:
                            message = f'{CMD_LOGO_CAUTION} No Recent Chats Data'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(message, color=COLOR_SCREENCMD_NORMAL)
                    except Exception as e:
                        message = f'{CMD_LOGO_CAUTION} Failed Opening Expanded Chats Window'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(message, color=COLOR_SCREENCMD_NORMAL)
                        screenmessage(f'{CMD_LOGO_CAUTION} {e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
                        print_internal_exception(e)

                elif msg.startswith(toggle_show_error_log):
                    try:
                        data = _load_internal_exception()
                        if data: ErrorPopup()
                        else:
                            message = f"You Got No Internal Errors Log"
                            if not responder_config.get(config_name_screenmessage_cmd):
                                chatmessage(message)
                            else:
                                screenmessage(message, color=COLOR_SCREENCMD_NORMAL)
                            return
                        message = 'Error Log Window Opened'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(message, color=COLOR_SCREENCMD_NORMAL)
                    except Exception as e:
                        message = f'{CMD_LOGO_CAUTION} Failed Opening Error Log Window'
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(message)
                        else:
                            screenmessage(message, color=COLOR_SCREENCMD_NORMAL)
                        screenmessage(f'{CMD_LOGO_CAUTION} {e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
                        print_internal_exception(e)

                elif msg.startswith(toggle_kick_player_cmd):
                    self._handle_player_action_cmd(msg, 'kick')

                elif msg.startswith(toggle_remove_player_cmd) or msg.startswith(toggle_remove_player_cmd2):
                    self._handle_player_action_cmd(msg, 'remove')

                elif msg.startswith(toggle_gethelp):
                    help_window_opened_msg = 'Help Window Opened'
                    failed_opening_help_window_msg = f'{CMD_LOGO_CAUTION} Failed Opening Help Window'
                    try:
                        ListPopup(info_msgs, "Help")
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(help_window_opened_msg)
                        else:
                            screenmessage(help_window_opened_msg, color=COLOR_SCREENCMD_NORMAL)
                    except Exception as e:
                        if not responder_config.get(config_name_screenmessage_cmd):
                            chatmessage(failed_opening_help_window_msg)
                        else:
                            screenmessage(failed_opening_help_window_msg, color=COLOR_SCREENCMD_NORMAL)
                        screenmessage(f'{CMD_LOGO_CAUTION} {e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
                        print_internal_exception(e)
                ############# Responder Windows #############
                else:
                    if party_config.get(CFG_NAME_BLOCK_NA_CMD):
                        if ' ' in msg:
                            prefix = msg.split(' ', 1)[0]
                        else:
                            prefix = msg
                        screenmessage(get_lang_text('cfgBlockNaCmd').format(prefix), COLOR_SCREENCMD_ERROR)
                    else:
                        self._focus_to_text_field()
                        if party_config[CFG_NAME_PARTY_CHAT_MUTED]:
                            screenmessage(get_lang_text('partyChatMutedWarn'), COLOR_SCREENCMD_ERROR)
                            bui.getsound('error').play(1.5)
                            return
                        _send_message_parted(msg=msg)
            #    elif msg.startswith(toggle_): pass
            elif msg.startswith('?'):
                cmd = msg.split('?')[1]
                if cmd:
                    exec(cmd)
                else:
                    self._focus_to_text_field()
                    if party_config[CFG_NAME_PARTY_CHAT_MUTED]:
                        screenmessage(get_lang_text('partyChatMutedWarn'), COLOR_SCREENCMD_ERROR)
                        bui.getsound('error').play(1.5)
                        return
                    _send_message_parted(msg=msg)
            else:
                self._focus_to_text_field()
                if party_config[CFG_NAME_PARTY_CHAT_MUTED]:
                    screenmessage(get_lang_text('partyChatMutedWarn'), COLOR_SCREENCMD_ERROR)
                    bui.getsound('error').play(1.5)
                    return
                _send_message_parted(msg=msg)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        """Called when a choice is selected in the popup, By defining the Type And then The Choice Of The Type."""
        if self._popup_type == POPUP_MENU_TYPE_MENU_PRESS:
            """Tempat pilihan yang ada di opsi Menu"""
            if choice == 'opsiBisu':
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_MUTE_TYPE)
                current_choice = _get_current_mute_type()
                self._popup_type = POPUP_MENU_TYPE_MUTE_TYPE
                PopupMenuWindow(
                    position=(self._width - 60, self._height - 47),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=current_choice,
                    delegate=self
                )
            elif choice == 'modifWarnaParty':
                color = party_config[CFG_NAME_MAIN_COLOR]
                ColorPickerExact(
                    parent=self.get_root_widget(),
                    position=self.get_root_widget().get_screen_space_center(),
                    initial_color=color,
                    delegate=self,
                    tag='')
            elif choice == 'hapusResponCepat':
                quick_reply_data = _load_quick_responds()
                self._popup_type = POPUP_MENU_TYPE_RM_QCK_RESPND_SEL
                PopupMenuWindow(
                    position=self._send_button.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=quick_reply_data,
                    choices_display=_create_baLstr_list(quick_reply_data),
                    current_choice=quick_reply_data[0],
                    delegate=self)
            elif choice == 'tambahResponCepat':
                newReply: str = bui.textwidget(query=self._text_field)
                if newReply:
                    currentReplies = _load_quick_responds()
                    currentReplies.append(newReply)
                    _save_quick_responds(currentReplies)
                    bui.getsound('gunCocking').play()
                else:
                    vote_kick_confirm_text = get_lang_text('tambahResponCepatTutorial')
                    confirm_text_part = vote_kick_confirm_text.splitlines()
                    self._focus_to_text_field()
                    ConfirmWindow(
                        text=f'{vote_kick_confirm_text}',
                        width=min(len(confirm_text_part[0]) * 13.5, 600),
                        height=120,
                        action=None,
                        cancel_button=False,
                        cancel_is_selected=True,
                        text_scale=1.0,
                        ok_text=get_lang_text('yes'),
                        cancel_text=get_lang_text('cancel'),
                        origin_widget=self.get_root_widget())
            elif choice == 'editResponCepat':
                SortMessagesList(data=_load_quick_responds(), write_data_func=_save_quick_responds, label=get_lang_text('editResponCepat'))
            elif choice == 'editCustomCommands':
                SortMessagesList(data=_load_custom_commands(), write_data_func=_save_custom_commands, label=get_lang_text('editCustomCommands'), needs_commands_prefix=True)
            elif choice == 'saveLastGameReplay':
                if party_config.get(CFG_NAME_ASK_GAME_REPLAY_NAME):
                    ReplayNameSavingPopup()
                else:
                    save_last_game_replay()
            elif choice == 'credit':
                CreditPopup()

        elif self._popup_type == POPUP_MENU_TYPE_RM_QCK_RESPND_SEL:
            # Remove The Selected Quick Respond `choice` From Data
            data = _load_quick_responds()
            data.remove(choice)
            _save_quick_responds(data)
            removed_text = get_lang_text('hapusResponCepatPilihText')
            screenmessage(f'\"{choice}\" {removed_text}')
            bui.getsound('shieldDown').play()
            self._focus_to_text_field()

        elif self._popup_type == POPUP_MENU_TYPE_PARTY_MEMBER_PRESS:
            playerinfo = get_player_info_with_cid(self._popup_party_member_client_id)
            if not playerinfo:
                pname = ''
                # There is always A Way :') ig... actually, no
                # Manual searching player data from saved text widget text
                if self._pressed_textwidget_text:
                    pname, current_text = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER, 1)
                else:
                    if self._popup_party_member_account:
                        pdata = current_session_namelist.get(self._popup_party_member_account, {})
                        if pdata:
                            account_name: str   = self._popup_party_member_account
                            client_id: int      = pdata.get('client_id', 0)

                            profiles: list[str] = pdata.get('profile_name', [])
                            profiles_joint: str = ', '.join(profiles) if profiles else ''
                            pname = account_name
                        if not pdata: return
                    else: return
                current_textwidget_text = self._pressed_textwidget_text
                current_textwidget: bui.Widget = self._pressed_textwidget
                player_acc: str = _match_player_name(pname, current_session_namelist)
                pdata = current_session_namelist.get(player_acc, {})
                if pdata:
                    account_name: str   = player_acc
                    client_id: int      = pdata.get('client_id', 0)

                    profiles: list[str] = pdata.get('profile_name', [])
                    profiles_joint: str = ', '.join(profiles) if profiles else ''
                else: return
            else:
                account_name: str   = playerinfo['account']
                client_id: int      = playerinfo['client_id']

                profiles: list[str] = playerinfo['profile_name']
                profiles_joint: str = playerinfo['profile_name_joint']

            if choice == 'votekick':
                # kick-votes appeared in build 14248
                host_info = bs.get_connection_to_host_info_2()
                if host_info is not None and host_info.build_number < 14248:
                    return
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                vote_kick_confirm_text = get_lang_text('voteKickConfirm')
                confirm_text = f'{vote_kick_confirm_text}\n{name}?'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=len(vote_kick_confirm_text) * 10,
                    height=150,
                    action=self._vote_kick_player,
                    cancel_button=True,
                    cancel_is_selected=True,
                    ok_text=get_lang_text('yes'),
                    cancel_text=get_lang_text('cancel'),
                    text_scale=1.0,
                    origin_widget=self.get_root_widget())

            elif choice == 'mention':
                # Mention Player By Adding Its Chosen Name Into Text Field
                _names_list: List[str] = []

                _names_list.append(account_name)
                if profiles: _names_list += profiles

                choices: List[str] = []
                names_list: List[str] = []

                for name in _names_list:
                    names_list.append(name)
                    if '"' in name: name = name.replace('"', '\\"')
                    if "'" in name: name = name.replace("'", "\\'")

                    choices.append('_edit_text_field_global("{name}", "add")'.format(name=name))

                names_display = _create_baLstr_list(names_list)

                self._focus_to_text_field()
                self._popup_type = POPUP_MENU_TYPE_EXECUTE_CHOICE
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices,
                    choices_display=names_display,
                    current_choice=choices[0],
                    delegate=self)

            elif choice == 'adminkick':
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                admin_kick_confirm_text = get_lang_text('adminKickConfirm')
                confirm_text = f'{admin_kick_confirm_text}?\n{name}'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=min((len(admin_kick_confirm_text) * 13.5), 600),
                    height=120,
                    action=Call(chatmessage, f'{KICK_CMD} {client_id}'),
                    cancel_button=True,
                    cancel_is_selected=True,
                    ok_text=get_lang_text('yes'),
                    cancel_text=get_lang_text('cancel'),
                    text_scale=1.0,
                    origin_widget=self.get_root_widget())

            elif choice == 'adminremove':
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                admin_remove_confirm_text = get_lang_text('adminRemoveConfirm')
                confirm_text = f'{admin_remove_confirm_text}?\n{name}'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=min((len(admin_remove_confirm_text) * 13.5), 600),
                    height=120,
                    action=Call(chatmessage, f'{REMOVE_CMD} {client_id}'),
                    cancel_button=True,
                    cancel_is_selected=True,
                    ok_text=get_lang_text('yes'),
                    cancel_text=get_lang_text('cancel'),
                    text_scale=1.0,
                    origin_widget=self.get_root_widget())

            elif choice == 'customCommands':
                choices: list[str] = []
                choices_display: list[str] = []
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                cmds_prefix: List[str] = ['/', '?']
                for text in custom_commands:
                    if '$acc' in text.lower():
                        text = text.replace('$acc', account_name)
                    if '$cid' in text.lower():
                        text = text.replace('$cid', str(client_id))
                    if '$name' in text.lower():
                        profile = profiles_joint if profiles else account_name
                        text = text.replace('$name', profile)
                    text = replace_msg_emoji_var_with_emojis(text)

                    choices_display.append(text)

                    if '"' in text: text = text.replace('"', '\\"')
                    if "'" in text: text = text.replace("'", "\\'")

                    if any(text.startswith(cmd_prefix) for cmd_prefix in cmds_prefix):
                        if party_config.get(CFG_NAME_DIRECT_CUSTOM_CMD):
                            choices.append(f'chatmessage("{text}")')
                        else:
                            choices.append(f'_edit_text_field_global("{text}", "replace")')
                    else:
                        choices.append(f'_edit_text_field_global("{text}", "replace")')


                """add_new_text = get_lang_text('addNewChoiceCmd')
                choices.append('AddNewChoiceWindow()')
                choices_display.append(f'*** {add_new_text} ***')"""

                sort_text = get_lang_text('sortChoiceCmd')
                choices.insert(0, f'SortMessagesList(_load_custom_commands(), _save_custom_commands, "Sort/Edit Custom Commands" , True)')
                choices_display.insert(0, f'*** {sort_text} ***')

             #  print(choices)
             #  print('\n', choices_display)
                self._focus_to_text_field()
                self._popup_type = POPUP_MENU_TYPE_EXECUTE_CHOICE
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices[len(choices) - 2],
                    delegate=self)

            elif choice == 'addNew':
                AddNewChoiceWindow()

            elif choice == 'warnInfo':
                self._popup_type = POPUP_MENU_TYPE_WARN_SELECT
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_WARN_SELECT)
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices_key[0],
                    delegate=self)

            elif choice == 'playerInfo':
                if client_id == -1:
                    if profiles:
                        account_name = profiles[0]
                PlayerInfoPopup(account_name)

        elif self._popup_type == POPUP_MENU_TYPE_CHAT_PRESS:
            pname, current_text = '', ''
            player_acc = ''
            player_profiles = []
            cid: Optional[int] = None
            if self._pressed_textwidget_text:
                pname, current_text = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER, 1)
            current_textwidget_text = self._pressed_textwidget_text
            current_textwidget: bui.Widget = self._pressed_textwidget
            if self._pressed_textwidget_text:
                player_acc: str = _match_player_name(pname, current_session_namelist)
                if current_session_namelist.get(player_acc):
                    player_profiles: list[str] = current_session_namelist.get(player_acc, {}).get('profile_name', [])
                    cid: Optional[int] = current_session_namelist.get(player_acc, {}).get('client_id')

            if choice == 'copyText':
                if current_textwidget_text:

                    msg = (
                        current_text if not party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) or pname.strip() == '...' else
                        str('/'.join(player_profiles) if player_profiles else pname) + PNAME_AND_MSG_SPLITTER + current_text
                    )
                    _copy_to_clipboard(msg)

            elif choice == 'translateText':
                if not current_textwidget_text: return
                self._translate_textwidget(current_text, current_textwidget)

            elif choice == 'insertText':
                if current_textwidget_text:
                    msg = (
                        current_text if not party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) or pname.strip() == '...' else
                        str('/'.join(player_profiles) if player_profiles else pname) + PNAME_AND_MSG_SPLITTER + current_text
                    )
                    _edit_text_field_global(msg, 'add')
                    self._focus_to_text_field()

            elif choice == 'playerMenuOptionFromText':
                if self._popup_party_member_client_id is None and self._popup_party_member_account is None:
                    self._refresh_text()
                    pass
                if self._pressed_textwidget_text and not player_acc: return
                self._on_party_member_press(cid, (False if not cid == -1 else True), popup_window.root_widget, player_acc)

        elif self._popup_type == POPUP_MENU_TYPE_SHOW_ICONS:
            _edit_text_field_global(choice, 'add', False)

        elif self._popup_type == POPUP_MENU_TYPE_WARN_SELECT:

            if choice == 'partyPressWarnAdd':
                self._popup_type = POPUP_MENU_TYPE_ADD_WARN_TYPE
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_ADD_WARN_TYPE)
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices_key[0],
                    delegate=self)

            elif choice == 'partyPressWarnDecrease':
                playerinfo = get_player_info_with_cid(self._popup_party_member_client_id)
                if playerinfo:
                    account_name: str   = playerinfo['account']
                elif self._popup_party_member_account:
                    account_name: str   =  self._popup_party_member_account
                else: return
                manual_decrease_warn(account_name, True)

        elif self._popup_type == POPUP_MENU_TYPE_ADD_WARN_TYPE:
            playerinfo = get_player_info_with_cid(self._popup_party_member_client_id)
            if playerinfo:
                account_name: str   = playerinfo['account']
                profiles_joint: str = playerinfo['profile_name_joint']
                client_id: int      = playerinfo['client_id']
            elif self._popup_party_member_account and current_session_namelist.get(self._popup_party_member_account):
                account_name: str   = self._popup_party_member_account
                profiles_joint: str = current_session_namelist[self._popup_party_member_account]['profile_name'] if current_session_namelist[self._popup_party_member_account]['profile_name'] else ''
                client_id: int      = current_session_namelist[self._popup_party_member_account]['client_id']
            else: return

            if choice == 'addWarnBetraying':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_betraying)

            elif choice == 'addWarnAbusing':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_abusing)

            elif choice == 'addWarnUnnecessaryVotes':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_kick_vote)

            elif choice == 'addWarnTeaming':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_teaming)

            self._popup_party_member_client_id = None
            self._popup_party_member_account  = None

        elif self._popup_type == POPUP_MENU_TYPE_CHAT_VIEWER_TYPE:
            cfg = party_config
            if choice == 'chatViewProfile':
                cfg[CFG_NAME_CHAT_VIEWER_TYPE] = chat_view_type_profile_name
                self._refresh_text(cfg)

            if choice == 'chatViewAccount':
                cfg[CFG_NAME_CHAT_VIEWER_TYPE] = chat_view_type_account_name
                self._refresh_text(cfg)

            if choice == 'chatViewMulti':
                cfg[CFG_NAME_CHAT_VIEWER_TYPE] = chat_view_type_multi
                self._refresh_text(cfg)

            if choice == 'chatViewMultiV2':
                cfg[CFG_NAME_CHAT_VIEWER_TYPE] = chat_view_type_multi_v2
                self._refresh_text()

            if choice == 'chatShowOrHideCid':
                if cfg[CFG_NAME_CHAT_VIEWER_SHOW_CID]:
                    cfg[CFG_NAME_CHAT_VIEWER_SHOW_CID] = False
                else:
                    cfg[CFG_NAME_CHAT_VIEWER_SHOW_CID] = True
                self._refresh_text(cfg)

            if choice == 'chatViewOff':
                cfg[CFG_NAME_CHAT_VIEWER_TYPE] = False
        #        cfg[CFG_NAME_CHAT_VIEWER_SHOW_CID] = False
                self._refresh_text(cfg)

        elif self._popup_type == POPUP_MENU_TYPE_EXECUTE_CHOICE:
            exec(choice)

        elif self._popup_type == POPUP_MENU_TYPE_MUTE_TYPE:
            self._change_mute_type(choice)

        elif self._popup_type == POPUP_MENU_TYPE_SORT_QCK_RESPND:
            sort_text = get_lang_text('sortQuickRespond')
            if choice == f"*** {sort_text} ***":
                SortMessagesList(_load_quick_responds(), _save_quick_responds, 'Sort/Edit Quick Respond')
            else:
                _edit_text_field_global(choice, action='add')

        elif self._popup_type == '': pass

        else:
            print(f'unhandled popup type: {self._popup_type}')

        del popup_window

    """Utility Sections"""
    def _on_setting_button_press(self):
        self._focus_to_text_field()
        try:
            PartySettingsWindow()
        except Exception as e:
            logging.exception()
            pass

    def _show_quick_respond_window(self, button: bui.Widget):
        choices = _load_quick_responds()
        for i, _choice in enumerate(choices):
            choices[i] = replace_msg_emoji_var_with_emojis(choices[i])

        sort_text = get_lang_text('sortQuickRespond')
        choices.insert(0, f'*** {sort_text} ***')

        self._focus_to_text_field()
        self._popup_type = POPUP_MENU_TYPE_SORT_QCK_RESPND
        if button:
            PopupMenuWindow(
                position=button.get_screen_space_center(),
                scale=_get_popup_window_scale(),
                color=self.bg_color, # type: ignore
                choices=choices,
                current_choice=choices[-1],
                delegate=self)

    def _copy_textfield(self):
        text: str = bui.textwidget(query=self._text_field)
        self._focus_to_text_field()
        if not text:
            screenmessage(get_lang_text('copyEmpty'), (1, 0 ,0))
            bui.getsound('error').play(1.5)
            return
        _copy_to_clipboard(text)
        """max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 10
        else:
            width = len(text) * 10
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}\n{text_title}",
            width= width,
            height=135,
            action=Call(_copy_to_clipboard, text),
            cancel_is_selected=True,
            text_scale=1,
            ok_text=get_lang_text('copy')
        )"""

    def _confirm_paste_textfield(self):
        is_clipboard: bool = babase.clipboard_is_supported()
        if not is_clipboard:
            screenmessage(f"{get_lang_text('pasteNotSupported')} {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return
        is_text_in_clipboard: bool = babase.clipboard_has_text()
        if not is_text_in_clipboard:
            screenmessage(f"{get_lang_text('pasteEmpty')} {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return
        cp_text: str = babase.clipboard_get_text()
        self._focus_to_text_field()
        if not cp_text.strip():
            screenmessage(f"{get_lang_text('pasteEmpty')} {get_random_unamused_emoji()}", COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return

        max_cp_text_len = 100
        is_dots = len(cp_text) > max_cp_text_len
        text = f"{get_lang_text('pasteConfirm')}?\n{cp_text[:min(len(cp_text), max_cp_text_len)]}{'...' if is_dots else ''}"
        ConfirmWindow(
            text=text,
            width=min((len(text) * 13.5)/1.5, 600),
            height=min(120*text.count('\n'), 300),
            action=CallStrict(self._paste_textfield, cp_text),
            cancel_button=True,
            cancel_is_selected=True,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel'),
            text_scale=1.0,
            origin_widget=self.get_root_widget())

    def _paste_textfield(self, text: str):
        if '\n' in text:
            text = ' '.join(text.splitlines())

        _edit_text_field_global(text, 'add')
        bui.getsound('ding').play(1.5)

    ####### CHAT NAVIGATOR BY FLUFFYPAL #######
    def _previous_message(self):
        if not self._chat_text_widgets: return
        if self._current_chosen_text_id == -1:  # Default chosen text id
            self._current_chosen_text_id = len(self._chat_text_widgets) - 1
            chosen_msg: str = self._chat_texts[self._current_chosen_text_id]
            _player_name = chosen_msg.split(PNAME_AND_MSG_SPLITTER, 1)[0]
            if party_config[CFG_NAME_COLORFUL_CHATS]:
                color: tuple[float, float, float] = color_tracker._get_sender_color(_player_name) if _player_name else (1, 1, 1)
            else:
                color: tuple[float, float, float] = TEXTWIDGET_DEFAULT_COLOR if TEXTWIDGET_DEFAULT_COLOR else (1, 1, 1)
            color = (color[0] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[1] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[2] + TEXTWIDGET_CHANGE_COLOR_RANGE)
            self._current_chosen_text_color = color

        else:
            if party_config[CFG_NAME_HIGHLIGHT_CHOSEN_TEXT]:
                # Reset previous widget text and color
                previous_widget = self._chat_text_widgets[self._current_chosen_text_id]
                _previous_text = bui.textwidget(query=self._chat_text_widgets[self._current_chosen_text_id])
                previous_text = _previous_text.split(CHOSEN_TEXT_HIGHLIGHT_MARK, 1)[1] if CHOSEN_TEXT_HIGHLIGHT_MARK and _previous_text.startswith(CHOSEN_TEXT_HIGHLIGHT_MARK) else _previous_text
                bui.textwidget(edit=previous_widget, text=previous_text, color=self._current_chosen_text_color)

            self._current_chosen_text_id -= 1
            if self._current_chosen_text_id < 0:
                self._current_chosen_text_id = -1
                bui.textwidget(edit=self._text_field, text='')
                return

        chosen_msg_widget = self._chat_text_widgets[self._current_chosen_text_id]
        chosen_msg: str = self._chat_texts[self._current_chosen_text_id]

        bui.containerwidget(
            edit=self._columnwidget, 
            visible_child=chosen_msg_widget)

        _player_name, _message= chosen_msg.split(PNAME_AND_MSG_SPLITTER, 1)
        if party_config[CFG_NAME_HIGHLIGHT_CHOSEN_TEXT]:
            if self._current_chosen_text_widget:
                if party_config[CFG_NAME_COLORFUL_CHATS]:
                    color: tuple[float, float, float] = color_tracker._get_sender_color(_player_name) if _player_name else (1, 1, 1)
                else:
                    color: tuple[float, float, float] = TEXTWIDGET_DEFAULT_COLOR if TEXTWIDGET_DEFAULT_COLOR else (1, 1, 1)
                color = (color[0] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[1] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[2] + TEXTWIDGET_CHANGE_COLOR_RANGE)
                self._current_chosen_text_color = color  # Save the current color

            # Add '>> ' to the beginning of the message
            highlighted_msg = f'{CHOSEN_TEXT_HIGHLIGHT_MARK}{bui.textwidget(query=chosen_msg_widget)}'
            bui.textwidget(edit=chosen_msg_widget, text=highlighted_msg, color=TEXTWIDGET_SELECTED_COLOR)

        self._current_chosen_text_widget = chosen_msg_widget
        self._current_chosen_text = chosen_msg

        player_name: list[str] = current_session_namelist.get(_match_player_name(_player_name, current_session_namelist), {}).get('profile_name', [])
        msg = (
            _message if
            (not party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) or _player_name.strip() == '...') else
            ('/'.join(player_name)[0:min(len('/'.join(player_name)), 20)] if player_name else _player_name) + PNAME_AND_MSG_SPLITTER + _message
        )
        _edit_text_field_global(msg, 'replace')

    def _next_message(self):
        if not self._chat_text_widgets: return
        if self._current_chosen_text_id == -1:  # Default chosen text id
            self._current_chosen_text_id = 0
            chosen_msg: str = self._chat_texts[self._current_chosen_text_id]
            _player_name = chosen_msg.split(PNAME_AND_MSG_SPLITTER, 1)[0]
            if party_config[CFG_NAME_COLORFUL_CHATS]:
                color: tuple[float, float, float] = color_tracker._get_sender_color(_player_name) if _player_name else (1, 1, 1)
            else:
                color: tuple[float, float, float] = TEXTWIDGET_DEFAULT_COLOR if TEXTWIDGET_DEFAULT_COLOR else (1, 1, 1)
            color = (color[0] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[1] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[2] + TEXTWIDGET_CHANGE_COLOR_RANGE)
            self._current_chosen_text_color = color
        else:
            if party_config[CFG_NAME_HIGHLIGHT_CHOSEN_TEXT]:
                # Reset previous widget text and color
                previous_widget = self._chat_text_widgets[self._current_chosen_text_id]
                _previous_text = bui.textwidget(query=self._chat_text_widgets[self._current_chosen_text_id])
                previous_text = _previous_text.split(CHOSEN_TEXT_HIGHLIGHT_MARK, 1)[1] if CHOSEN_TEXT_HIGHLIGHT_MARK and _previous_text.startswith(CHOSEN_TEXT_HIGHLIGHT_MARK) else _previous_text
                bui.textwidget(edit=previous_widget, text=previous_text, color=self._current_chosen_text_color)

            self._current_chosen_text_id += 1
            if self._current_chosen_text_id > len(self._chat_text_widgets) - 1:
                self._current_chosen_text_id = -1
                bui.textwidget(edit=self._text_field, text='')
                return

        chosen_msg_widget = self._chat_text_widgets[self._current_chosen_text_id]
        chosen_msg: str = self._chat_texts[self._current_chosen_text_id]

        bui.containerwidget(
            edit=self._columnwidget, 
            visible_child=chosen_msg_widget)

        _player_name, _message= chosen_msg.split(PNAME_AND_MSG_SPLITTER, 1)
        if party_config[CFG_NAME_HIGHLIGHT_CHOSEN_TEXT]:
            if self._current_chosen_text_widget:
                if party_config[CFG_NAME_COLORFUL_CHATS]:
                    color: tuple[float, float, float] = color_tracker._get_sender_color(_player_name) if _player_name else (1, 1, 1)
                else:
                    color: tuple[float, float, float] = TEXTWIDGET_DEFAULT_COLOR if TEXTWIDGET_DEFAULT_COLOR else (1, 1, 1)
                color = (color[0] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[1] + TEXTWIDGET_CHANGE_COLOR_RANGE, color[2] + TEXTWIDGET_CHANGE_COLOR_RANGE)
                self._current_chosen_text_color = color  # Save the current color

            # Add '>> ' to the beginning of the message
            highlighted_msg = f'{CHOSEN_TEXT_HIGHLIGHT_MARK}{bui.textwidget(query=chosen_msg_widget)}'
            bui.textwidget(edit=chosen_msg_widget, text=highlighted_msg, color=TEXTWIDGET_SELECTED_COLOR)

        self._current_chosen_text_widget = chosen_msg_widget
        self._current_chosen_text = chosen_msg

        player_name: list[str] = current_session_namelist.get(_match_player_name(_player_name, current_session_namelist), {}).get('profile_name', [])
        msg = (
            _message if
            (not party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) or _player_name.strip() == '...') else
            ('/'.join(player_name)[0:min(len('/'.join(player_name)), 20)] if player_name else _player_name) + PNAME_AND_MSG_SPLITTER + _message
        )
        _edit_text_field_global(msg, 'replace')
    ####### CHAT NAVIGATOR BY FLUFFYPAL #######

    def _ip_port_msg(self):
        try:
            msg = f'IP : {_server_ip}     PORT : {_server_port}'
        except:
            msg = ''
        _edit_text_field_global(msg, 'replace')
        self._focus_to_text_field()

    def _send_ping(self):
        if party_config.get(CFG_NAME_ACCURATE_SERVER_PING_SEND):
            _refresh_server_ip_and_port()
            def callback_func():
                if self._ping_button:
                    bui.buttonwidget(
                        edit=self._ping_button,
                        label=f'{round(_server_ping)}',
                        textcolor=_get_ping_color()
                    )
                    chatmessage(random.choice(PING_MESSAGE).format(str(round(_server_ping, 2))))
            _ping_server_accurate(callback=callback_func)
        else:
            if isinstance(_server_ping, (int, float)):
                chatmessage(random.choice(PING_MESSAGE).format(str(round(_server_ping, 2))))

    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return (1.6 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else
                2.0)

    def _change_mute_type(self, choice: str):
        global party_config
        if choice == 'muteInGameOnly':
            party_config[CFG_NAME_CHAT_MUTED] = True
            party_config[CFG_NAME_PARTY_CHAT_MUTED] = False
        elif choice == 'mutePartyWindowOnly':
            party_config[CFG_NAME_CHAT_MUTED] = False
            party_config[CFG_NAME_PARTY_CHAT_MUTED] = True
        elif choice == 'muteAll':
            party_config[CFG_NAME_CHAT_MUTED] = True
            party_config[CFG_NAME_PARTY_CHAT_MUTED] = True
        else:
            party_config[CFG_NAME_CHAT_MUTED] = False
            party_config[CFG_NAME_PARTY_CHAT_MUTED] = False
        self._update()

    def _vote_kick_player(self):
        if self._popup_party_member_is_host:
            bui.getsound('error').play(1.5)
            cant_kick_host_text = get_lang_text('cantKickHost') + f' {get_random_sad_emoji()}'
            screenmessage(
                cant_kick_host_text,
                color=COLOR_SCREENCMD_ERROR)
        else:
            assert self._popup_party_member_client_id is not None
            pinfo = get_player_info_with_cid(self._popup_party_member_client_id)
            if pinfo and pinfo['account'] in MY_MASTER:
                screenmessage(f"{get_lang_text('cantKickMaster')} {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return

            # Ban for 5 minutes.
            result = bs.disconnect_client(
                self._popup_party_member_client_id, ban_time=5 * 60)
            self._popup_party_member_client_id = None
            self._popup_party_member_account = None
            if not result:
                bui.getsound('error').play(1.5)
                screenmessage(
                    (babase.Lstr(resource='getTicketsWindow.unavailableText').evaluate()),
                    color=COLOR_SCREENCMD_ERROR)

    def _translate_text_field_delay(self):
        if self._translate_button_pressed is False:
            self._translate_button_pressed = True
            babase.apptimer(0.3, self._translate_text_field)
        elif self._translate_button_pressed is True:
            TranslationSettings()
            self._translate_button_pressed = False

    def _translate_text_field(self):
        if not self._translate_button_pressed: return
        self._translate_button_pressed = False
        self._focus_to_text_field()
        msg: str = bui.textwidget(query=self._text_field)
        name = ''
        if party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) and PNAME_AND_MSG_SPLITTER in msg and self._current_chosen_text_id != -1:
            name, text = msg.split(PNAME_AND_MSG_SPLITTER, 1)
        else:
            text = msg
        cleaned_msg = ''.join(filter(str.isalpha, text))

        if not msg or not cleaned_msg or msg == '':
            screenmessage(f'{CMD_LOGO_CAUTION} ' + get_lang_text('translateEmptyText'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('translating'), COLOR_SCREENCMD_NORMAL)

            def _apply_translation(translated: str):
                if party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) and PNAME_AND_MSG_SPLITTER in msg and self._current_chosen_text_id != -1:
                    translate_text = name + PNAME_AND_MSG_SPLITTER + translated
                else:
                    translate_text = translated
                if self._text_field.exists():
                    bui.textwidget(edit=self._text_field, text=translate_text)
            Translate(text=text, callback=_apply_translation, src_lang=party_config.get(CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD, 'auto'), dst_lang=party_config.get(CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD, 'en'))
    
    def _translate_textwidget(self, text_widget_text: str, text_widget: bui.Widget):
        """Translate the Pressed textwidget"""
        msg: str = bui.textwidget(query=text_widget)
        cleaned_msg = ''.join(filter(str.isalpha, text_widget_text))

        if not msg or not cleaned_msg or msg == '':
            screenmessage(f'{CMD_LOGO_CAUTION} ' + get_lang_text('translateEmptyText'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('translating'), COLOR_SCREENCMD_NORMAL)
            name = ''
            if PNAME_AND_MSG_SPLITTER in msg:
                name, text = msg.split(PNAME_AND_MSG_SPLITTER, 1)
            else:
                text = msg

            def _apply_translation(translated: str) -> None:
                if PNAME_AND_MSG_SPLITTER in msg:
                    translate_text = name + PNAME_AND_MSG_SPLITTER + translated
                else:
                    translate_text = translated
                if text_widget.exists():
                    bui.textwidget(edit=text_widget, text=translate_text)
            Translate(text=text, callback=_apply_translation)

    def _handle_player_action_cmd(self, msg: str, action_type: str) -> None:
        """Handle player kick/remove actions with confirmation window"""
        try:
            if not current_namelist or not self._roster:
                screenmessage(get_lang_text('noResponderData'), COLOR_SCREENCMD_NORMAL)
                return

            _, _name = msg.split(' ', 1)
            name = find_player(_name, True, current_namelist)

            if not current_namelist.get(name):
                screenmessage(get_lang_text('findPlayerCmdNotFound').format(_name), COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return

            client_id: int = current_namelist[name]['client_id']
            profile: list[str] = current_namelist[name]['profile_name']
            p_str = f"{name} | {', '.join(profile)}" if profile else name
            self._popup_party_member_client_id = client_id

            if action_type.lower().startswith('kick'):
                action_text = get_lang_text('adminKickConfirm')
                action_callback = self._send_admin_kick_command
            else:
                action_text = get_lang_text('adminRemoveConfirm')
                action_callback = self._send_admin_remove_command

            ConfirmWindow(
                text=f'{action_text}?\n{p_str}',
                width=min(max(len(action_text), len(p_str)) * 13.5, 600),
                height=150,
                action=action_callback,
                cancel_button=True,
                cancel_is_selected=True,
                text_scale=1.0,
                ok_text=get_lang_text('yes'),
                cancel_text=get_lang_text('cancel'),
                origin_widget=self.get_root_widget())

        except ValueError:
            if action_type.lower().startswith('kick'):
                toggle = toggle_kick_player_cmd
            else:
                toggle = f"({toggle_remove_player_cmd}/{toggle_remove_player_cmd2})"
            screenmessage(f"{CMD_LOGO_CAUTION} {get_lang_text('use')} {toggle} [name]", COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        except Exception as e:
            print_internal_exception(e)

    def _send_admin_kick_command(self):
        chatmessage(f'{KICK_CMD} {self._popup_party_member_client_id}')
        self._popup_party_member_client_id = None
        self._popup_party_member_account = None

    def _send_admin_remove_command(self):
        chatmessage(f'{REMOVE_CMD} {self._popup_party_member_client_id}')
        self._popup_party_member_client_id = None
        self._popup_party_member_account = None

    def color_picker_selected_color(self, picker, color: tuple[float, float, float]) -> None:
        bui.containerwidget(edit=self._root_widget, color=color)
        self.bg_color = color

    def color_picker_closing(self, picker) -> None:
        update_party_config(CFG_NAME_MAIN_COLOR, self.bg_color)

    def close(self) -> None:
        """Close the window."""
        try:
            if party_config.get(CFG_NAME_SAVE_LAST_TYPED_MSG):
                global _last_text_field_msg
                _last_text_field_msg = bui.textwidget(query=self._text_field)
        except Exception as e:
            print_internal_exception(e)
        save_party_config(party_config)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        global _text_field, ping_server_timer
        _text_field = None
        ping_server_timer = babase.AppTimer(
            ping_server_delay,
            ping_server_recall,
            repeat=True
            #timetype=babase.TimeType.REAL
        )

        ping_server_recall()

    def _focus_to_text_field(self):
        bui.containerwidget(
            edit=self._root_widget,
            selected_child=self._text_field,
            color=self.bg_color
        )

class NameMatcher:
    def __init__(
            self,
            message: str,
            roster: List[Dict[str, Any]],
            callback: Callable[[str, bui.Widget], None],
            widget: bui.Widget,
            del_muted: bool=False
        ) -> None:

        self.message = message
        self._roster = roster
        self.widget = widget
        self.callback = callback
        self.del_muted = del_muted
        self.run()

    def run(self):
        _name, message = self.message.split(PNAME_AND_MSG_SPLITTER, 1)
        p_data = current_namelist if self._roster else current_session_namelist

        player_name = _match_player_name(player_name=_name, player_data=p_data)
        player_data = p_data.get(player_name, {})

        player_client_id = player_data.get('client_id')
        player_profile: list[str] = player_data.get('profile_name', [])
        player_profile_joint = ', '.join(player_profile) if player_profile else player_name

        player_name_final = ''

        if self.del_muted and player_muted_list: # and p_data == current_namelist:
            if player_name in player_muted_list:
                if self.widget and self.widget.exists():
                    self.widget.delete()
                return

        if player_data and player_client_id != -1:
            if party_config.get(CFG_NAME_CHAT_VIEWER_SHOW_CID):
                player_name_final += (f'[{str(player_client_id)}] ')

            # Name Viewer
            if party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_profile_name:
                if player_profile and len(player_profile) == 1:
                    player_name_final += player_profile[0]
                else:
                    if player_profile:
                        player_name_final += f"{player_profile_joint}"
                    else:
                        player_name_final += f"{player_name}"

            elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_account_name:
                player_name_final += player_name

            elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_multi:
                if player_profile and len(player_profile) == 1:
                    if sanitize_name(player_name) != sanitize_name(player_profile[-1]):
                        player_name_final += player_name + ' | ' + player_profile_joint
                    else:
                        player_name_final += f"{player_name}"
                else:
                    if player_name != player_profile_joint:
                        player_name_final += player_name + ' | ' + f"{player_profile_joint}"
                    else:
                        player_name_final += f"{player_name}"

            elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_multi_v2:
                if player_profile and len(player_profile) == 1:
                    if sanitize_name(player_name) != sanitize_name(player_profile[-1]):
                        player_name_final += player_name + ' | ' + player_profile_joint
                    else:
                        player_name_final += f"{player_name}"
                else:
                    if player_name != _name:
                        player_name_final += player_name + ' | ' + f"{_name}"
                    else:
                        player_name_final += f"{player_name}"

            else:
                player_name_final += _name
        #else:
            #pass
            #print(f"No Data Found For {_name}")

        # Return normal name text if player_name_final is empty (no match)
        if not player_name_final or player_name_final == '':
            player_name_final = _name

        text = player_name_final + PNAME_AND_MSG_SPLITTER + message
        self._result(text=text)

    def _result(self, text: str):
        self.callback(text, self.widget)
        #babase.pushcall(Call(self.callback, text, self.widget), from_other_thread=True)

##### Response Time Interval (Seconds) #####
master_chats_interval           = 0.05
update_player_info_interval     = 0.4

log_chats_interval          = 0.05
second_log_chats_interval   = 0.075

custom_reply_delay      = 0.475
auto_ping_delay         = 2
noob_respone_delay      = 1
sus_respone_delay       = 2
less_respone_delay    = 0.475
bruh_respone_delay      = 2
############################################
is_doing_jobs: List[str] = []
"""
Defining if a task is recently used

Usage:
    - defname = self.func.__name__ + "smth"
    - if defname in is_doing_jobs: return
    - refresh_job(delay, defname)
"""
def reset_job(job: str):
    """Reset Job With Func Name"""
    global is_doing_jobs
    if job in is_doing_jobs:
        is_doing_jobs.remove(job)
        #print(f"Job Removed: {job}")

def refresh_job(timer: float | int, job: str):
    global is_doing_jobs
    if job not in is_doing_jobs:
        is_doing_jobs.append(job)
        babase.apptimer(timer, Call(reset_job, job))
    #print(f"Job Started: {job}")


def cari_sapaan(list_sapaan: List[str], message: str):
    return next((word for word in list_sapaan if word in message), None)

def cari_nick(list_nick: List[str], message: str):
    return next((word for word in list_nick if word in message), None)


ding_small_high = bui.getsound('dingSmallHigh')
class LessAutoResponder:
    """A Lovely Auto Responder"""
    def __init__(self):
        self.is_sending_names = False

        self._max_chat_reached = False

        self.update_chats_and_name = None
        self._get_player_info_timer = None
        self.log_chats_timer = None


        self._last_player_greets_me = ""
        self._last_player_custom_reply = ""
        self._last_custom_reply = ""

        self._last_soal = ""
        self._last_jawaban = ""

        self.nama_pemain = ''
        self.jawab_lain = ''
        self.pesan_terakhir = ''

        self.pesan: List[str] = []
        self.saved_msg: List[str] = []
        self.main_saved_msg: List[str] = []
        self.current_conncetion_info: Dict[str, Any] = {}

        self.current_roster = [{}]
        self._players_to_be_greeted: List[str] = []

        # Old latest message and player name init
        self.jawab_lain_lower: str = ''
        self.second_last_msg: str = ""
        self.third_last_msg: str = ""
        self.forth_last_msg: str = ""

        self.second_last_nama_pemain = ""
        self.third_last_nama_pemain = ""
        self.forth_last_nama_pemain = ""

        self._saving_names_ratio = 20
        self._current_name_saving_ratio = 0

    def _stop_engine(self):
        #self.update_chats_and_name = None
        self._get_player_info_timer = None
        self.log_chats_timer = None

    def _start_engine(self) -> None:
        """Start Func Loops"""
        #self.update_chats_and_name = babase.AppTimer(master_chats_interval, self.master_chats, repeat=True) # Our Master
        self._get_player_info_timer = babase.AppTimer(update_player_info_interval, CallStrict(self._get_player_info), repeat=True)

        self.log_chats_timer = babase.AppTimer(log_chats_interval, CallStrict(self.log_chats), repeat=True)

    def master_chats(self, msg: Optional[str] = None):
        """Master Func To Get Chats And Toggle Responders"""
        if len(self.pesan) >= 4:
            self.forth_last_msg = self.third_last_msg
            self.forth_last_nama_pemain = self.third_last_nama_pemain
        if len(self.pesan) >= 3:
            self.third_last_msg = self.second_last_msg
            self.third_last_nama_pemain = self.second_last_nama_pemain
        if len(self.pesan) >= 2:
            self.second_last_msg = self.jawab_lain
            self.second_last_nama_pemain = self.nama_pemain

        if self.pesan:
            self.pesan_terakhir = (self.pesan[-1] if not msg else msg).replace('', '')
            if ':' in self.pesan_terakhir:
                nama_pemain, jawab_lain = self.pesan_terakhir.split(message_and_pname_splitter, 1)
                self.nama_pemain = _match_player_name(nama_pemain, current_namelist) # Match Player Name
                self.jawab_lain_lower = jawab_lain.lower()
                self.jawab_lain = jawab_lain
            else:
                self.jawab_lain_lower = self.pesan_terakhir.lower()

        #if self.pesan and (self.main_saved_msg == [] or self.jawab_lain != self.main_saved_msg[-1]):
            #self.main_saved_msg.append(self.jawab_lain)
            #print(f"Msg Saved: {self.jawab_lain}")

        """Let's Check Responders :)"""
        if not responder_config.get(config_name_enable_less_responder): return
        if responder_config.get(config_name_anti_abuse):
            Thread(target=self.anti_abuse).start()
        if responder_config.get(config_name_vote_kick_detect):
            Thread(target=self.vote_kick_analyzer).start()
        if self.nama_pemain not in player_muted_list:
            if responder_config.get(config_name_soal):
                Thread(target=self.soal).start()
            if responder_config.get(config_name_custom_reply):
                Thread(target=self.respond_to_custom_reply).start()
            if responder_config.get(config_name_noob):
                Thread(target=self.deteksi_noob).start()
            if responder_config.get(config_name_sus):
                Thread(target=self.deteksi_sus).start()
            if responder_config.get(config_name_less):
                Thread(target=self.less).start()
            if responder_config.get(config_name_bruh):
                Thread(target=self.bruh).start()
            if responder_config.get(config_name_show_my_master_ping):
                self._do_auto_ping()
        self._check_other_responder()
        ###=========================###

    def manual_log_chats(self):
        """Manually Logs Each Msgs With Delays, From Incoming Msgs From PartyWindow

        Calling master_chat is unnecessary, we already have it called in PartyWindow"""
        global _pending_msgs
        if not _pending_msgs:
            print('Uh oh, Manual Msgs Got Empty List')
            return
        global _chat_texts
        pendings_data: Dict[str, list[list[str | None]]] = {}
        self._match_log_file_path_with_server_name()
        for i, message in enumerate(_pending_msgs):
            # Match the log file with the server name and set up the correct folder

            # Log the last message
            if message in _pending_msgs:
                _pending_msgs.remove(message)
            self.saved_msg.append(message)

            name, pesan, pname, player_name, profile = self._get_chat_logs_attrs(message)

            _chat_texts.append(message+(f" {MUTED_LOGS_MARK}" if pname in player_muted_list else ""))

            if responder_config.get(config_name_chat_logging):
                if pendings_data:
                    pendings_data["pendings_json"].append([pname, profile, pesan])
                    pendings_data["pendings_txt"].append([player_name, pesan])
                else:
                    pendings_data["pendings_json"] = [[pname, profile, pesan]]
                    pendings_data["pendings_txt"] = [[player_name, pesan]]

            ### Showing msg logic ###
            #self._show_msg(name, pesan, message, pname)
            ### Showing msg logic ###

       #     self.master_chats(message)

            self.internal_save_chat_json(pname, pesan, profile)

            if responder_config.get(config_name_cmdprint):
                if pname in player_muted_list:
                    pesan += f" {MUTED_LOGS_MARK}"
                print(f"[!MSG LOG] {player_name}: {pesan}")

        save_internal_all_chats_data()
        save_internal_player_chats_data()
        if responder_config.get(config_name_chat_logging):
            if pendings_data:
                self.save_chats_data(pendings_data=pendings_data)
            else:
                print(f"Oh no, saving chats logs on manual is empty")

        while len(self.saved_msg) > maximum_bombsquad_chat_messages:
            self.saved_msg.pop(0)

        if _pending_msgs:
            self.manual_log_chats()

    def log_chats(self):
        """Fetch new chat messages and log them using both JSON and TXT methods"""
        if babase.app.classic.party_window(): # type: ignore
            return
        global _chat_texts, _pending_msgs

        # Fetch the current chat messages
        chats: List[str] = bs.get_chat_messages()

        if self.pesan == chats:
            return
        self.pesan: List[str] = chats

        if _pending_msgs:
            self.manual_log_chats()
            return

        # Check if there are any chats to log
        if not chats:
            return

        current_len = len(chats)

        saved_len = len(self.saved_msg)

        profile = None
        pendings_data: Dict[str, list[list[str | None]]] = {}

        if not chats: return

        # Match the log file with the server name and set up the correct folder
        self._match_log_file_path_with_server_name()

        # Iterate over the current chat list and compare with the saved messages
        # When chats exceed max_chats, switch to the old method (log based on last messages)
        if saved_len >= maximum_bombsquad_chat_messages:
            chats_range = 3
            for i, _chat in enumerate(chats[-chats_range:]):
                if _chat not in self.saved_msg[saved_len-chats_range-1:]: #chats[current_len-(chats_range+1+i)] != self.saved_msg[current_len-(chats_range+1+i)]:
                    if not self._max_chat_reached:
                        bs.broadcastmessage(f"Max Chat Reached: {str(current_len)} | Doing Plan B", color=COLOR_SCREENCMD_NORMAL)
                        print(f"\nMax Chat Reached: {str(current_len)}\nLog Chat Plan B Started\n")
                   #     self.update_chats_and_name = babase.AppTimer(master_chats_interval, self.master_chats, repeat=True) # Our Master
                  #      self.log_chats_timer = babase.AppTimer(second_log_chats_interval, self.log_chats, repeat=True)
                        self._max_chat_reached = True

                    if saved_len >= maximum_bombsquad_chat_messages:
                        self.saved_msg.pop(0)

                    if not babase.app.classic.party_window(): self.master_chats(_chat) # type: ignore

                    # Log the last message
                    self.saved_msg.append(_chat)

                    name, pesan, pname, player_name, profile = self._get_chat_logs_attrs(_chat)

                    _chat_texts.append(_chat+(f" {MUTED_LOGS_MARK}" if pname in player_muted_list else ""))

                    ### Showing msg logic ###
                    self._show_msg(name, pesan, _chat, pname)
                    ### Showing msg logic ###

                    if responder_config.get(config_name_chat_logging):
                        if pendings_data:
                            pendings_data["pendings_json"].append([pname, profile, pesan])
                            pendings_data["pendings_txt"].append([player_name, pesan])
                        else:
                            pendings_data["pendings_json"] = [[pname, profile, pesan]]
                            pendings_data["pendings_txt"] = [[player_name, pesan]]

                    pesan = pesan + f" {MUTED_LOGS_MARK}" if party_config.get(CFG_NAME_CHAT_MUTED) else pesan
                    self.internal_save_chat_json(pname, pesan, profile)
                    if chats_range == i+1:
                        save_internal_all_chats_data()
                        save_internal_player_chats_data()
                        if responder_config.get(config_name_chat_logging):
                            if pendings_data:
                                self.save_chats_data(pendings_data=pendings_data)

                    if responder_config.get(config_name_cmdprint):
                        if pname in player_muted_list:
                            pesan += f" {MUTED_LOGS_MARK}"
                        print(f"[&MSG LOG] {player_name}: {pesan}")

        elif saved_len < maximum_bombsquad_chat_messages:
            for i in range(current_len):
                # When chats are within max_chats, compare the entire list and log differences
                if i >= saved_len:
                    if not babase.app.classic.party_window(): self.master_chats(chats[i]) # type: ignore

                    # Split the message into player name and the message content
                    name, pesan, pname, player_name, profile = self._get_chat_logs_attrs(chats[i])

                    _chat_texts.append(chats[i]+(f" {MUTED_LOGS_MARK}" if pname in player_muted_list else ""))

                    # Log the message
                    self.saved_msg.append(chats[i])

                    ### Showing msg logic ###
                    self._show_msg(name, pesan, chats[i], pname)
                    ### Showing msg logic ###

                    self.internal_save_chat_json(pname, pesan, profile)
                    if responder_config.get(config_name_chat_logging):
                        if pendings_data:
                            pendings_data["pendings_json"].append([pname, profile, pesan])
                            pendings_data["pendings_txt"].append([player_name, pesan])
                        else:
                            pendings_data["pendings_json"] = [[pname, profile, pesan]]
                            pendings_data["pendings_txt"] = [[player_name, pesan]]
                    if i == saved_len:
                        save_internal_all_chats_data()
                        save_internal_player_chats_data()
                        if responder_config.get(config_name_chat_logging):
                            if pendings_data:
                                self.save_chats_data(pendings_data=pendings_data)

                    if responder_config.get(config_name_cmdprint):
                        if pname in player_muted_list:
                            pesan += f" {MUTED_LOGS_MARK}"
                        print(f"[MSG LOG {i+1}] {player_name}: {pesan}")
                    """
                    screenmessage(f"Saved MSG Len: {str(len(self.saved_msg))}")
                    screenmessage(f"Saved MSG: {self.saved_msg[-1]}")
                    screenmessage(f"Current MSG Len: {str(current_len)}")
                    screenmessage(f"Current MSG: {chats[-1]}")
                    """

    def _show_msg(self, name: str, pesan: str, _chat: str, pname: str):
        if party_config.get(CFG_NAME_CHAT_MUTED): return
        if not babase.app.config.get('Chat Muted') is True: return
        if pname in player_muted_list: return
        if babase.app.classic.party_window(): return # type: ignore

        player_name_final = ''
        if party_config.get(CFG_NAME_CHAT_NAME_VIEWER_IN_SCRMSG):
            if not any(name.startswith(server) for server in SERVER_NAMES) and current_namelist.get(pname, {}).get('client_id') != -1:
                player_name_final = self._get_player_name_view(name=name, pname=pname)
            else:
                player_name_final = name

        scrmsg = _chat if not party_config.get(CFG_NAME_CHAT_NAME_VIEWER_IN_SCRMSG) else f"{player_name_final}{PNAME_AND_MSG_SPLITTER}{pesan}"
        color = TEXTWIDGET_DEFAULT_COLOR
        if party_config.get(CFG_NAME_COLORFUL_SCRMSG):
            while color == TEXTWIDGET_DEFAULT_COLOR:
                color = color_tracker._get_sender_color(name)
                col_range = 0.2
                color = (color[0] + col_range,
                            color[1] + col_range,
                            color[2] + col_range)
        else:
            color = (0.3, 0.55, 0.35)
        is_top_pos: bool = True if party_config.get(CFG_NAME_MESSAGE_NOTIFICATION_POS) == 'top' else False
        screenmessage(message=scrmsg, color=color, top=is_top_pos)
        bui.getsound('tap').play(1.2)
        #print(f"Other screenmessage: {is_muted}, {babase.app.config.get('Chat Muted')}, {babase.app.classic.party_window()}")

    def _get_player_name_view(self, name: str, pname: str) -> str:
        player_client_id = current_namelist.get(pname, {}).get('client_id')
        player_profile: list[str] = current_namelist.get(pname, {}).get('profile_name', [])
        player_profile_joint = ', '.join(player_profile) if player_profile else pname
        player_name_final = ''
        if party_config.get(CFG_NAME_CHAT_VIEWER_SHOW_CID) and player_client_id:
            player_name_final += (f'[{str(player_client_id)}]' + ' ')

        # Name Viewer
        if party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_profile_name:
            if player_profile and len(player_profile) == 1:
                player_name_final += player_profile_joint
            else:
                if player_profile:
                    player_name_final = f"{player_name_final} [{player_profile_joint}]"
                else:
                    player_name_final = f"{player_name_final} {player_profile_joint}"

        elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_account_name:
            player_name_final += pname

        elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_multi:
            if player_profile and len(player_profile) == 1:
                if sanitize_name(pname) != sanitize_name(player_profile_joint):
                    player_name_final += pname + ' | ' + player_profile_joint
                else:
                    player_name_final += f"{pname}"
            else:
                if pname != player_profile_joint:
                    player_name_final += pname + ' | ' + f"[{player_profile_joint}]"
                else:
                    player_name_final += f"{pname}"

        elif party_config.get(CFG_NAME_CHAT_VIEWER_TYPE) == chat_view_type_multi_v2:
            if player_profile and len(player_profile) == 1:
                if sanitize_name(pname) != sanitize_name(player_profile[-1]):
                    player_name_final += pname + ' | ' + player_profile_joint
                else:
                    player_name_final += f"{pname}"
            else:
                if pname != name:
                    player_name_final += pname + ' | ' + f"{name}"
                else:
                    player_name_final += f"{pname}"

        else:
            player_name_final += name

        if not player_name_final or player_name_final == '':
            player_name_final = name

        return player_name_final

    def save_chats_data(self, pendings_data: Dict[str, list[list[str | None]]]):
        #self.save_chat_json(pendings_data)
        self.save_chat_txt(pendings_data)
        #print(pending_json)

    def internal_save_chat_json(self, pname: str, msg: str, profile=None):
        #### Internal Chat Data ####
        global internal_player_chats_data, internal_all_chats_data, current_server_name
        
        profile_or_pname = f"{pname} | {profile}" if profile and (not profile in pname or ', ' in profile) else pname
        profile_only = f"{profile}" if profile and (not profile in pname or ', ' in profile) else pname
        timestamp2 = datetime.now().strftime("[%H:%M:%S]") # Currently not used
        internal_chat_entry = f"{profile_or_pname}{PNAME_AND_MSG_SPLITTER_MODIFIED}{msg}" # pname Acc should be the 1st
        profile_only_entry = f"{profile_only}{PNAME_AND_MSG_SPLITTER_MODIFIED}{msg}"

        info = self.current_conncetion_info
        server_name = info.name if info and info.name else server_name_default
        #print(internal_chat_entry)

        if server_name == server_name_default:# or any(pname.startswith(name) for name in SERVER_NAMES):
            return
        server_name_entry = f"{CMD_LOGO_SERVER} {server_name}"

        """Append message to the player's chat history"""
        if pname in internal_player_chats_data:
            if len(internal_player_chats_data[pname]) >= max_player_chat_data:
                internal_player_chats_data[pname].pop(0)
            internal_player_chats_data[pname].append(profile_only_entry)
        else:
            internal_player_chats_data[pname] = [profile_only_entry]

        """Append message to the all chat history"""
        if current_server_name != server_name:
            if len(internal_all_chats_data) >= max_internal_all_chats_data:
                internal_all_chats_data.pop(0)
            internal_all_chats_data.append(server_name_entry)
        if len(internal_all_chats_data) >= max_internal_all_chats_data:
            internal_all_chats_data.pop(0)
        internal_all_chats_data.append(internal_chat_entry)
        current_server_name = server_name

    def save_chat_json(self, pendings: Dict[str, list[list[str]]]):
        """Save player chat to a JSON file, appending new messages"""
        global chats_data_file_path
        chats_data_file_path = chats_data_file_folder_path + f"{chats_data_file_name}.json"

        info = self.current_conncetion_info
        server_name = info.name if info and info.name else server_name_default

        if server_name == server_name_default:# or any(pname.startswith(name) for name in SERVER_NAMES):
            return

        # Load existing data if the file exists
        def save():
            chat_data = load_json_chats_data()

            timestamp = datetime.now().strftime("[%H:%M:%S]") if responder_config.get(config_name_use_dates_on_chatdata) else datetime.now().strftime("[%d-%m-%Y | %H:%M:%S]")

            chat_entry: list[str] = []
            lenght = len(pendings) - 1
            pjson = pendings["pendings_json"]
            for i in range(0, lenght):
                pname, profile, pesan = pjson[i]
                profile_only = f"{profile}" if profile and (not profile in pname or ', ' in profile) else pname

                # Append message to the player's chat history
                if pname in chat_data:
                    chat_data[pname].append(f"{timestamp} [{profile_only}]{PNAME_AND_MSG_SPLITTER_MODIFIED}{pesan}")
                else:
                    chat_data[pname] = chat_entry

        # Save the updated data back to the file
            try:
                chats_data_file_path = os.path.join(chats_data_file_folder_path, f"{chats_data_file_name}.json")
                os.makedirs(os.path.dirname(chats_data_file_path), exist_ok=True)
                if os.path.exists(chats_data_file_path):
                    current_data_size = get_file_size(chats_data_file_path)
                    if isinstance(current_data_size, (float, int)) and current_data_size > MAX_CHAT_LOGS_FILE_SIZE:
                        files = [f for f in os.listdir(chats_data_file_folder_path) if f.endswith('.txt')]
                        num_files = len(files)
                        new_file_name = f"{chats_data_file_name}-{num_files}.json"
                        new_file_path = os.path.join(chats_data_file_folder_path, new_file_name)
                        os.rename(chats_data_file_path, new_file_path)
                        chats_data_file_path = new_file_path
                with open(chats_data_file_path, 'w', encoding='utf-8') as f:
                    json.dump(chat_data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
            except Exception as e:
                print_internal_exception(e)

        Thread(target=save).start()

    def save_chat_txt(self, pendings: Dict[str, list[list[str | None]]]):
        """Save chat to a TXT log file, appending new messages"""
        global chats_log_file_path

        info = self.current_conncetion_info
        server_name = info.name if info and info.name else server_name_default

        def save():
            if server_name == server_name_default:# or any(player_name.startswith(name) for name in SERVER_NAMES):
                return

            chat_entry = ''
            timestamp = datetime.now().strftime("[%H:%M:%S]") if responder_config.get(config_name_use_dates_on_chatdata) else datetime.now().strftime("[%d-%m-%Y | %H:%M:%S]")
            lenght = len(pendings) - 1
            ptxt = pendings["pendings_txt"]
            for i in range(0, lenght):
                player_name, pesan = ptxt[i]
                chat_entry += f"{timestamp} [{player_name}]{PNAME_AND_MSG_SPLITTER_MODIFIED}{pesan}\n"

            #os.makedirs(chats_data_file_folder_path, exist_ok=True)

            # Append the new message to the log file
            if server_name != server_name_default:
                chats_log_file_path = chats_data_file_folder_path + f"{chats_log_file_name}.txt"
                current_data_size = get_file_size(chats_log_file_path)
                if isinstance(current_data_size, (float, int)) and current_data_size > MAX_CHAT_LOGS_FILE_SIZE:
                    files = [f for f in os.listdir(chats_data_file_folder_path) if f.endswith('.txt')]
                    num_files = len(files)
                    new_file_name = f"{chats_log_file_name}-{num_files}.txt"
                    new_file_path = os.path.join(chats_data_file_folder_path, new_file_name)
                    os.rename(chats_log_file_path, new_file_path)
                    chats_log_file_path = new_file_path   

                with open(chats_log_file_path, 'a', encoding='utf-8') as f:
                    f.write(chat_entry)
        Thread(target=save).start()

    def _get_chat_logs_attrs(self, _chat: str) -> tuple[str, str, str, str, str | None]:
        name, pesan = _chat.split(message_and_pname_splitter, 1)
        pesan = pesan.strip()

        # Match the player name with a profile name if available
        pname = _match_player_name(name, current_namelist)
        try:
            profile = ', '.join(current_session_namelist[pname]['profile_name']) if current_session_namelist[pname].get('profile_name') else None
        except Exception as e:
            profile = None

        player_name = f"{pname} | {profile}" if profile and (not profile in pname or ', ' in profile) else pname
        return (name, pesan, pname, player_name, profile)

    def _send_greet_player_msg(self) -> None:
        """Greet Our `Friends` :)"""
        if not self._players_to_be_greeted: return
        if party_config.get(CFG_NAME_AUTO_GREET_FRIENDS_IF_MASTER_JOINED):
            if not any(current_namelist.get(name, {}).get('profile_name') for name in MY_MASTER):
                return
        delays = [1.5, 1.75, 2]
        print('\n')
        for i, name in enumerate(self._players_to_be_greeted):
            if not current_session_namelist.get(name): continue
            if use_their_profile_for_greet_friends: name = current_session_namelist.get(name, {}).get('profile_name', name)
            halo: str = f"{random.choice(jawab_halo)} {name} {get_random_happy_emoji()}"
            babase.apptimer(i + random.choice(delays), Call(self.greet, name, halo))
        print('\n')
        self._players_to_be_greeted.clear()

    def greet(self, name: str, word: str):
        if current_session_namelist.get(name, {}).get('greeted'): return
        chatmessage(word)
        current_session_namelist[name]['greeted'] = True
        screenmessage(f"{name} Greeted", COLOR_SCREENCMD_NORMAL, True)
        print(f'Greeted {name}')
        ding_small_high.play()

    def _get_player_info(self):
        roster = bs.get_game_roster()
        if self.current_roster == roster:
            return
        self.current_roster = roster
        self.current_conncetion_info = bs.get_connection_to_host_info_2()
        babase.apptimer(1.5, self._send_greet_player_msg)
        if self._players_to_be_greeted and not current_namelist:
            self._players_to_be_greeted.clear() # Cancel master's greeting

        Thread(target=self._start_get_player_info).start()

    def _start_get_player_info(self):
        """Ultimate Player Info Get

        Might Slowdown Device, Use `Thread`"""
        global all_names, current_session_namelist, current_namelist, player_acc_returner, identical_all_names

        current_namelist = {}  # Reset The Current List
        identical_all_names = False
        last_met_timestamp = datetime.now().strftime("[%d-%m-%Y | %I:%M %p]")
        server_name = self.current_conncetion_info.name if self.current_conncetion_info is not None else "Unknown"
        profile_names_list: List[str] = []

        if not self.current_roster:
            if not is_getting_player_data:
                start_save_all_names().start_threaded()
            Thread(target=save_internal_player_chats_data, args=(True,)).start()
            return
        # Extract game roster and construct player info list
        info = [
            {
                'acc': player['display_string'],    # Account name
                'ds': player['players'],            # List of players playing in Acc (Profiles)
                'cid': player['client_id']          # Client ID
                #'aid': player['account_id']        # pb_id (Not For Clients)
            } for player in self.current_roster
        ]

        # Iterate over the current roster
        for player in info:
            _current_real_name = player['acc']  # Player's real name
            players = player['ds']              # Player Joined Name (display name)
            client_id = player['cid']           # Client ID
            #account_id = player['aid']         # pb_id (Its Only Shows Current User pb_id, Not Other Players pb_id)
            full_names = [p['name_full'] for p in players]  # Get Players Full Names
            names_short: List[str] = [p['name'] for p in players]   # Get Player's Shorten Names. Why the heck it shows Mr.Smoothy

            # Handle icons in the real name
            current_real_name: str
            if _current_real_name and _current_real_name[0] in SPECIAL_CHARS:
                current_real_name = player['acc']  # Original Icons
            elif _current_real_name.startswith('<HIDDEN>'):
                global is_hidden_names_by_server
                is_hidden_names_by_server = True
                continue # Don't Save Player Data That Are Hidden By Server
            else:
                # If player name Startwith PC or Android, its not possible
                # Because old servers support Device Icon, else 1.4 Servers
                # And if the PC Or Android acc ID upgraded to V2
                current_real_name = babase.charstr(SpecialChar.V2_LOGO) + _current_real_name  # Add V2 Icon
                global is_1_4_server
                is_1_4_server = True # Make 1.4 State To True

            ### Player Data Format ###
            # If the client is a server (client_id = -1), swap real_name and profile_name
            if client_id == -1:
                if players:
                    server_profile_name = full_names
                    server_real_name = current_real_name
                    current_real_name = server_profile_name[0]  # Use profile name as the real name
                    profile_names: List[str] = [server_real_name]  # Use real name as the profile name
                    profile_names_joint = ', '.join(profile_names)
                    profile_name_short = names_short
                else:
                    profile_names = []
                    profile_name_short = [] 
                    profile_names_joint = False
            else:
                # If the player has profile names (Joined)
                if players:
                    # If the player has more than one profile name, join them with commas
                    profile_names = full_names
                    profile_names_joint = ', '.join(profile_names)
                    profile_name_short = names_short
                else:
                    profile_names = []
                    profile_name_short = [] 
                    profile_names_joint = False
            ###====================###

            """Current Session"""
            if current_real_name not in current_session_namelist:
                current_session_namelist[current_real_name] = {
                    'profile_name': profile_names,
                    'client_id': client_id,
                    'profile_name_short': profile_name_short
                }

            if (current_session_namelist[current_real_name]['client_id'] != client_id and not current_namelist.get(current_real_name)):
                current_session_namelist[current_real_name]['client_id'] = client_id

            if current_session_namelist[current_real_name]['profile_name'] != profile_names:
                if not current_namelist.get(current_real_name) and profile_names:
                    current_session_namelist[current_real_name]['profile_name'] = profile_names
                elif profile_names:
                    current_profiles = current_session_namelist[current_real_name].get('profile_name', [])
                    current_session_namelist[current_real_name]['profile_name'] = list(set(current_profiles + profile_names))

            if current_session_namelist[current_real_name]['profile_name_short'] != profile_name_short:
                if not current_namelist.get(current_real_name) and profile_name_short:
                    current_session_namelist[current_real_name]['profile_name_short'] = profile_name_short
                elif profile_name_short:
                    current_profiles_short = current_session_namelist[current_real_name].get('profile_name_short', [])
                    current_session_namelist[current_real_name]['profile_name_short'] = list(set(current_profiles_short + profile_name_short))

            if current_real_name in players_anti_abuse_exception and current_real_name not in MY_MASTER:
                if party_config.get(CFG_NAME_AUTO_GREET_FRIENDS) and \
                current_session_namelist.get(current_real_name) and not \
                current_session_namelist[current_real_name].get('greeted'):
                    if current_real_name not in self._players_to_be_greeted:
                        if not party_config.get(CFG_NAME_AUTO_GREET_FRIENDS_IF_FRIENDS_JOINED):
                            self._players_to_be_greeted.append(current_real_name)
                        elif profile_names:
                            self._players_to_be_greeted.append(current_real_name)

            """Permanent List"""
            if current_real_name not in all_names:
                all_names[current_real_name] = {
                    'profile_name': profile_names,
                    'client_id': client_id,
                    'last_met': last_met_timestamp,
                    'mutual_server': [server_name]
                }
                if profile_names:
                    profile_str_joint = ', '.join(all_names[current_real_name]['profile_name'])
                    if responder_config.get(config_name_cmdprint):
                        print(f"[NEW NAME] [{current_real_name}] With Profile [{profile_str_joint}] Added! CID: ({client_id})")
                    if responder_config.get(config_name_logmsg2):    
                        babase.pushcall(CallPartial(screenmessage, f"[NEW NAME] [{current_real_name}] With Profile [{profile_str_joint}] Added! CID: ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                else:
                    if responder_config.get(config_name_cmdprint):
                        print(f"[NEW NAME] [{current_real_name}] (No Profile) Added! CID: ({client_id})")
                    if responder_config.get(config_name_logmsg2):    
                        babase.pushcall(CallPartial(screenmessage, f"[NEW NAME] [{current_real_name}] (No Profile) Added! CID: ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
            else:
                if not current_namelist.get(current_real_name):
                    if all_names[current_real_name]['client_id'] != client_id:
                        if responder_config.get(config_name_cmdprint):
                            if all_names[current_real_name]['profile_name']:
                                profile_str_joint = ', '.join(all_names[current_real_name]['profile_name'])
                                print(f"Updating [CLIENT ID]: [{current_real_name}] With Last Profile [{profile_str_joint}] -> From ({all_names[current_real_name]['client_id']}) To ({client_id})")
                            else:
                                print(f"Updating [CLIENT ID]: [{current_real_name}] With (No Last Profile) -> From ({all_names[current_real_name]['client_id']}) To ({client_id})")

                        if responder_config.get(config_name_logmsg2):    
                            if all_names[current_real_name]['profile_name']:
                                profile_str_joint = ', '.join(all_names[current_real_name]['profile_name'])
                                babase.pushcall(CallStrict(screenmessage, f"Updating [CLIENT ID]: [{current_real_name}] With Last Profile [{profile_str_joint}] -> From ({all_names[current_real_name]['client_id']}) To ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                            else:
                                babase.pushcall(CallStrict(screenmessage, f"Updating [CLIENT ID]: [{current_real_name}] With (No Last Profile) -> From ({all_names[current_real_name]['client_id']}) To ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)

                        all_names[current_real_name]['client_id'] = client_id

                if all_names[current_real_name]['profile_name'] != profile_names and not current_namelist.get(current_real_name):
                    last_profiles = all_names[current_real_name]['profile_name']

                    if isinstance(last_profiles, list) and not all(current_namelist.get(_match_player_name(profile, current_namelist)) for profile in last_profiles):
                        if last_profiles:
                            profile_str_joint = ', '.join(last_profiles)

                            if profile_names:
                                # Update profile name
                                if responder_config.get(config_name_cmdprint):
                                    print(f"Updating Profile Name [{current_real_name}]: From [{profile_str_joint}] To [{profile_names_joint}] CID: ({client_id})")
                                if responder_config.get(config_name_logmsg2):                
                                    babase.pushcall(CallStrict(screenmessage, f"[{current_real_name}] Profile Name Updated To [{profile_names_joint}] CID: ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                                all_names[current_real_name]['profile_name'] = profile_names
                            else:
                                # Refresh profile name
                                if responder_config.get(config_name_refresh_names):
                                    msg_print = f"[REFRESH] Profile Name [{current_real_name}]: Last Profile Name -> [{profile_str_joint}] CID: ({client_id})"
                                    if responder_config.get(config_name_cmdprint):
                                        print(msg_print)
                                    if responder_config.get(config_name_logmsg2):            
                                        babase.pushcall(CallStrict(screenmessage, msg_print, COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                                    all_names[current_real_name]['profile_name'] = profile_names
                        else:
                            # Add new profile name
                            if profile_names:
                                if responder_config.get(config_name_cmdprint):
                                    print(f"[JOIN] Adding [{current_real_name}] Profile Name -> Profile: [{profile_names_joint}] CID: ({client_id})")
                                if responder_config.get(config_name_logmsg2):        
                                    babase.pushcall(CallStrict(screenmessage, f"[JOIN] Adding [{current_real_name}] Profile Name -> Profile: [{profile_names_joint}] CID: ({client_id})", COLOR_SCREENCMD_NORMAL), from_other_thread=True)
                    else:
                        if profile_names:
                            current_profiles: list[str] = all_names[current_real_name].get('profile_name', [])
                            updated_profiles = list(set(current_profiles + profile_names))
                            all_names[current_real_name]['profile_name'] = updated_profiles

                if all_names[current_real_name].get('mutual_server') is None or all_names[current_real_name].get('mutual_server') != server_name:
                    if all_names[current_real_name].get('mutual_server') is None:
                        all_names[current_real_name]['mutual_server'] = [server_name]
                        if responder_config.get(config_name_cmdprint):
                            print(f'[SERVER] [{current_real_name}] Mutual Server Added For The First Time [{server_name}]')
                    else:
                        if server_name and server_name not in all_names[current_real_name]['mutual_server']:
                            if isinstance(all_names[current_real_name]['mutual_server'], list):
                                all_names[current_real_name]['mutual_server'].append(server_name)
                                if responder_config.get(config_name_cmdprint):
                                    print(f'[SERVER] [{current_real_name}] Mutual Server Added: [{server_name}]')
                            elif isinstance(all_names[current_real_name]['mutual_server'], str):
                                all_names[current_real_name]['mutual_server'] = [server_name]
                                if responder_config.get(config_name_cmdprint):
                                    print(f'[SERVER] [{current_real_name}] Mutual Server Added For The First Time [{server_name}]')
                            else:
                                print(f"[SERVER] Invalid mutual server Type: {type(all_names[current_real_name]['mutual_server'])}")

                """if all_names[current_real_name].get('profile_name_short', ['']) != profile_name_short:
                    if not current_namelist.get(current_real_name):
                        # Don't Update Their Profile Names To None, Save Their Last Profile Names
                        if profile_names:
                            all_names[current_real_name]['profile_name_short'] = profile_name_short
                        else:
                            if responder_config.get(config_name_refresh_names):
                                all_names[current_real_name]['profile_name_short'] = profile_name_short
                    else:
                        if profile_names:
                            current_profiles = all_names[current_real_name].get('profile_name_short', [])
                            updated_profiles = list(set(current_profiles + profile_name_short))
                            all_names[current_real_name]['profile_name_short'] = updated_profiles"""

                if not all_names[current_real_name].get('last_met') or all_names[current_real_name]['last_met'] != last_met_timestamp:
                    all_names[current_real_name]['last_met'] = last_met_timestamp

            if profile_names_joint: profile_names_list.append(profile_names_joint)

            # Lets Use Namelist To Make Sure Name Not Updating Other Data List Many Times
            # If There Are Two Same Account In One Server
            """Namelist"""
            if current_real_name not in current_namelist:
                current_namelist[current_real_name] = {
                    'profile_name': profile_names,
                    'client_id': client_id,
                    'profile_name_short': profile_name_short
                }
            else:
                current_namelist[current_real_name] = {
                    'profile_name': list(set(profile_names + current_namelist[current_real_name]['profile_name'])),
                    'client_id': client_id,
                    'profile_name_short': list(set(profile_name_short + current_namelist[current_real_name]['profile_name_short']))
                }

        try: 
            # Helper to get player acc faster
            player_acc_returner = {}
            how_many_dots_name = sum(1 for name in current_namelist.values() if name.get('profile_name_short') == '...')
            for _player_real_name, profile_info in current_namelist.items():
                # Handle profile names
                if profile_info.get('profile_name', []) and isinstance(profile_info.get('profile_name', []), list):
                    for profile in profile_info.get('profile_name', []):
                        if profile and profile_info.get('client_id') != -1:
                            sanitized_profile = sanitize_name(profile)
                            # Check if profile already exists and delete if same
                            if sanitized_profile in player_acc_returner:
                                if player_acc_returner[sanitized_profile] != _player_real_name:
                                    del player_acc_returner[sanitized_profile]
                            else:
                                player_acc_returner[sanitized_profile] = _player_real_name

                # Handle real names
                sanitized_real_name = sanitize_name(_player_real_name)
                # Check if real name already exists and delete if same
                if sanitized_real_name in player_acc_returner:
                    if player_acc_returner[sanitized_real_name] != _player_real_name:
                        del player_acc_returner[sanitized_real_name]
                else:
                    player_acc_returner[sanitized_real_name] = _player_real_name

                # Handle short profile names
                name_short: list[str] | None = profile_info.get('profile_name_short')
                if name_short:
                    for short_profile in name_short:
                        if short_profile == '...' and not how_many_dots_name <= 1:
                            continue
                        if short_profile and profile_info.get('client_id') != -1:
                            sanitized_short = sanitize_name(short_profile)
                            # Check if short profile already exists and delete if same
                            if sanitized_short in player_acc_returner:
                                if player_acc_returner[sanitized_short] != _player_real_name:
                                    del player_acc_returner[sanitized_short]
                            else:
                                player_acc_returner[sanitized_short] = _player_real_name
        except Exception as e:
            print_internal_exception(e)

        _automatic_get_player_info_from_bcs()
        self._current_name_saving_ratio += 1
        if self._current_name_saving_ratio >= self._saving_names_ratio:
            print(f"Calling Saving All Names From {self._get_player_info.__name__} | {self._current_name_saving_ratio}")
            _save_names_to_file()
            self._current_name_saving_ratio = 0

    ############################## Chat Logger ##############################
    def get_current_time(self): # Not Used
        """Returns the current time formatted as [YYYY-MM-DD][HH:MM:SS]"""
        return datetime.now().strftime("[%d-%m-%Y] [%H:%M:%S]")
        
    def _match_log_file_path_with_server_name(self):
        """Get server name and update the log file folder path based on server and date"""
        global chats_data_file_folder_path

        forbidden_symbols = ['/', '\\', ':', '*', '?', "'", '"', '<', '>', '|']

        # Get server information
        info = self.current_conncetion_info
        server_name = info.name if info and info.name else server_name_default  # Use a default if the server name is empty

        # Clean server name for display purposes (optional)
        server_name_clean_display = ''.join(c for c in server_name if c.isalnum() or c in (' ', '_')).strip()

        # Clean server name for filenames (replace forbidden symbols)
        server_name_clean_filename = server_name.translate(str.maketrans('', '', ''.join(forbidden_symbols)))

        # Generate the date for folder creation
        file_date = datetime.now().strftime("[%d-%m-%Y]")

        # Update the folder path (use server_name_clean_filename for filenames)
        chats_data_file_folder_name = 'Chats Data'
        if responder_config.get(config_name_use_dates_on_chatdata):
            chats_data_file_folder_path = responder_directory + f"{chats_data_file_folder_name}/{server_name_clean_filename}/{file_date}/"
        else:
            chats_data_file_folder_path = responder_directory + f"{chats_data_file_folder_name}/{server_name_clean_filename}/"
        
        main_chats_data_file_folder_path = responder_directory + f"{chats_data_file_folder_name}/{server_name_clean_filename}"
        # Create the directory if it doesn't exist
        if not os.path.exists(main_chats_data_file_folder_path):
            os.makedirs(main_chats_data_file_folder_path)
            bs.broadcastmessage("Created Chat Logger Folder", color=COLOR_SCREENCMD_ERROR)

    def soal(self):
        """The Famous Auto Answer Server Questions, Premium By Me :)"""
        kata_soal_blacklist = ['warn', '==', 'pb-', 'rules', 'error evaluating', 'ping', 'started a kick']

        if any(word.lower() in self.jawab_lain_lower for word in kata_soal_blacklist):
            return

        pesan = self.pesan_terakhir.lower()

        math_trigger = ['what is', '=', 'cuanto']
        if (any(trigger in self.jawab_lain_lower for trigger in math_trigger) or (
            any(char.isdigit() for char in self.jawab_lain_lower) and any(self.nama_pemain.startswith(name.lower()) for name in SERVER_NAMES))) and (any(
            self.nama_pemain.startswith(name) for name in SERVER_NAMES) or any(name == self.nama_pemain for name in MY_MASTER)):
            try:
                jawab_mtk = pesan.replace('x', '*').replace('=', '').replace('?', '').replace('=', '')[pesan.find(':'):]
                all_digits = [x.isdigit() for x in jawab_mtk]
                t = [i for i, x in enumerate(all_digits) if x]
                if t:
                    jawaban_mtk = eval(jawab_mtk[t[0]:t[-1] + 1])  # Evaluasi Soal MTK
                    babase.pushcall(Call(bs.chatmessage, str(jawaban_mtk)), from_other_thread=True)
                    babase.pushcall(Call(babase.apptimer, 2.25, Call(self.soal_smart_check, str(jawaban_mtk))), from_other_thread=True)
                    return
            except Exception as e:
         #       bs.chatmessage(f"{CMD_LOGO_CAUTION} Error Evaluating -> [{e}] :')")
                print(f"{CMD_LOGO_CAUTION} Error Evaluating -> [{e}] :')")

        if any(self.nama_pemain.startswith(name) for name in SERVER_NAMES):
            for pertanyaan, jawaban in kunci_jawaban.items():
                if pertanyaan.lower() in pesan.lower() and not any(name == self.nama_pemain for name in MY_MASTER):
                    babase.pushcall(Call(chatmessage, str(jawaban)), from_other_thread=True)
                    babase.pushcall(Call(babase.apptimer, 2.25, Call(self.soal_smart_check, jawaban)), from_other_thread=True)
                    break

    def soal_smart_check(self, answer):
        """Smart 2nd Attempt Answer"""
        congratulations = ["congrat", "you got", "you earn", "you won"]
        if responder_config.get(config_name_smart_2nd_attempt_answer):
            if (not any(
                name.lower() in self.jawab_lain_lower for name in MY_MASTER) or not any( # 1st Phase
                name.lower() in self.second_last_msg.lower() for name in MY_MASTER)) and (any( # Check If My Master Acc Mentioned In Chat
                name in self.nama_pemain for name in SERVER_NAMES) or any( # 2nd Phase
                name.lower() in self.second_last_nama_pemain.lower() for name in SERVER_NAMES)) and not any( # Check if the one mentioned My Master is Server
                name == self.nama_pemain for name in MY_MASTER) and (not any( # 3rd Phase - Check if the answer is not already asnwered by My Master
                word.lower() in self.jawab_lain_lower for word in congratulations) and any( # 4th Phase (Global)
                self.nama_pemain.startswith(name) for name in SERVER_NAMES)): # Check If there are Congratulations Words after Getting the answer and Server Saying it
                bs.chatmessage(answer)

    def _check_other_responder(self):
        commands_responder_delay = 1
        if self.nama_pemain not in player_blacklisted_list:
            if self.jawab_lain_lower.startswith(cmd_toggle_findall_pdata):
                defname = self._check_other_responder.__name__ + cmd_toggle_findall_pdata
                if defname in is_doing_jobs: return
                refresh_job(commands_responder_delay, defname)

                if not identical_all_names:
                    load_all_names_data()
                find_player_cmd(message=self.jawab_lain_lower, data_type=all_names, is_master=False, toggle=cmd_toggle_findall_pdata)
            elif self.jawab_lain_lower.startswith(cmd_toggle_find_pdata):
                defname = self._check_other_responder.__name__ + cmd_toggle_find_pdata
                if defname in is_doing_jobs: return
                refresh_job(commands_responder_delay, defname)

                if not identical_all_names:
                    load_all_names_data()
                find_player_cmd(message=self.jawab_lain_lower, data_type=current_session_namelist, is_master=False, toggle=cmd_toggle_find_pdata)

    def _do_auto_ping(self):
        defname = self._do_auto_ping.__name__
        if defname in is_doing_jobs: return

        pemicu_cmd = '/ping'
        pemicu = 'ping'

        if ((self.jawab_lain_lower.startswith(pemicu_cmd) or (
                any(nick in self.jawab_lain_lower for nick in my_nick_names) and pemicu in self.jawab_lain_lower)
            ) and not any(name == self.nama_pemain for name in player_blacklisted_list)) or (
            (self.second_last_msg.lower().startswith(pemicu_cmd) or (
                any(nick in self.second_last_msg.lower() for nick in my_nick_names) and pemicu in self.second_last_msg.lower())
            ) and not any(name == self.second_last_nama_pemain for name in player_blacklisted_list) and not any(name == self.nama_pemain for name in MY_MASTER)):
            _refresh_server_ip_and_port()
            refresh_job(auto_ping_delay, defname)
            print(f"Auto Ping Called: {self.jawab_lain_lower} | {self.second_last_msg}")
            try:
                print('Doing Automatic Pinging')
                Thread(target=start_pinging_server, args=(_server_ip, _server_port)).start()
            except:
                try:
                    print("Failed Doing Automatic Pinging: Falling Back To Manual Pinging")
                    do_manual_server_ping()
                except:
                    pass

    def respond_to_custom_reply(self):
        defname = self.respond_to_custom_reply.__name__
        if defname in is_doing_jobs: return

        prefix_add_reply = CMD_MAIN_PREFIX + add_custom_reply_cmd
        prefix_remove_reply = CMD_MAIN_PREFIX + remove_custom_reply_cmd

        cmd = [prefix_add_reply, prefix_remove_reply]
        if any(word in self.jawab_lain_lower for word in cmd) and any(name == self.nama_pemain for name in MY_MASTER):
            return

        if (self._last_custom_reply != "") and (
            self._last_custom_reply.lower() not in self.jawab_lain_lower and
            self._last_custom_reply.lower() not in self.second_last_msg.lower() and
            self._last_custom_reply.lower() not in self.third_last_msg.lower() and
            self._last_custom_reply.lower() not in self.forth_last_msg.lower()):
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Last Custom Reply Resets"), from_other_thread=True)
            self._last_player_custom_reply = ""
            self._last_custom_reply = ""
        """ 
            ### ▽ Strict Mode ▽ ###
        if (self._last_player_custom_reply != "" or self._last_custom_reply != "") and (
            (self._last_player_custom_reply != name or (self._last_player_custom_reply not in self.second_last_nama_pemain and self._last_player_custom_reply not in self.third_last_nama_pemain and self._last_player_custom_reply not in self.forth_last_nama_pemain)) and 
            (self._last_custom_reply != reply or (self._last_custom_reply not in self.second_last_msg and self._last_custom_reply not in self.third_last_msg and self._last_custom_reply not in self.forth_last_msg))):
            babase.pushcall(Call(screenmessage, f"{cmd_logo_caution} Last Custom Reply Resets"), from_other_thread=True)
            self._last_player_custom_reply = ""
            self._last_custom_reply = ""

        if (self._last_player_custom_reply != "" or self._last_custom_reply != "") and (
            reply in self._last_custom_reply or name in self._last_player_custom_reply):
            return
        """ # Just Simply Replace This To Change Custom Reply Strictness

        if self._last_custom_reply != "": # Block if custom reply haven't resets
            return

        # Iterate through the custom replies to find a trigger match
        for trigger, reply in custom_replies.items():
            if (trigger in self.jawab_lain_lower and not any(name == self.nama_pemain for name in MY_MASTER) and not any(name == self.nama_pemain for name in player_blacklisted_list)) or (
                trigger in self.second_last_msg.lower() and not any( # Reply if the trigger burried before My Master could respond to it
                name == self.nama_pemain for name in MY_MASTER) and not any( # Make sure My Master haven't respond to it
                name == self.second_last_nama_pemain for name in MY_MASTER) and not any( # Don't respond if its My Master
                #name in self.second_last_nama_pemain for name in SERVER_NAMES) and not any( # Don't respond if it's Server
                name == self.second_last_nama_pemain for name in player_blacklisted_list)):

                if trigger in self.second_last_msg.lower():
                    name = self.second_last_nama_pemain
                else:
                    name = self.nama_pemain

                self._last_player_custom_reply = name

                # Replace $acc with the player's account name
                if '$acc' in reply:
                    reply = reply.replace('$acc', name)
                # Replace $name with the player's profile name (or a fallback)
                if '$cid' in reply:
                    client_id = all_names.get(name, {}).get('client_id', '???')
                    reply = reply.replace('$cid', str(client_id))
                if '$name' in reply:
                    profile = all_names.get(name, {}).get('profile_name', name)
                    if isinstance(profile, list):
                        profile = ', '.join(profile)
                    reply = reply.replace('$name', profile)
                reply = replace_msg_emoji_var_with_emojis(reply)

                self._last_custom_reply = reply

                # Send the customized reply
                babase.pushcall(Call(bs.chatmessage, f"{reply}"), from_other_thread=True)
                babase.pushcall(Call(refresh_job, custom_reply_delay, defname), from_other_thread=True)
                break

    def deteksi_noob(self):
        defname = self.deteksi_noob.__name__
        if defname in is_doing_jobs: return

        if any(word in self.jawab_lain_lower for word in custom_replies.keys()):
            return

        kata_noob = ['noob', 'nub', 'nob', 'ooob', '000b', 'no ob', 'n00b', 'n0b', 'no0b', 'n0ob', '0o0b', 'o0ob']

        if not any(name in self.nama_pemain for name in SERVER_NAMES) and not any(name == self.nama_pemain for name in MY_MASTER):
            if any(word in self.jawab_lain_lower for word in kata_noob):
                babase.pushcall(Call(babase.apptimer, noob_respone_delay, Call(bs.chatmessage, 'N')), from_other_thread=True)
                babase.pushcall(Call(refresh_job, noob_respone_delay, defname), from_other_thread=True)

    def deteksi_sus(self):
        defname = self.deteksi_sus.__name__
        if defname in is_doing_jobs: return

        if any(name == self.nama_pemain for name in player_blacklisted_list):
            return

        if any(word in self.jawab_lain_lower for word in custom_replies.keys()):
            return

        sus = [
            'suspicious', 'among us', 'amogus', 'om agus', 'u sus', 'm sus', 'super sus', 'is sus', 'sus',
            'imposto', 'imposta', 'impasta', 'impstr', 'impastar', 'impostr', 'imposter'
        ]

        if any(name in self.nama_pemain for name in SERVER_NAMES): return

        if any(word in self.jawab_lain_lower for word in sus):
            babase.pushcall(Call(babase.apptimer, sus_respone_delay, Call(chatmessage, '𐐘 𐑀 ඞා')), from_other_thread=True)
            babase.pushcall(Call(refresh_job, sus_respone_delay, defname), from_other_thread=True)

    def less(self):
        defname = self.less.__name__
        if defname in is_doing_jobs: return

        # Reset last player greeting if not found in recent messages
        if self._last_player_greets_me and not any(self._last_player_greet_word in msg for msg in [
            self.second_last_msg, self.third_last_msg, self.forth_last_msg]
        ):
            babase.pushcall(Call(screenmessage, f"Last Player Greet Resets: {self._last_player_greets_me}", (1, .35, .5)), from_other_thread=True)
            self._last_player_greets_me = self._last_player_greet_word = ""

        if (any(word in self.jawab_lain_lower for word in list_kata_halo) and 
            any(nick in self.jawab_lain_lower for nick in my_nick_names) and 
            not any(self.nama_pemain.startswith(name) for name in (
                SERVER_NAMES + player_blacklisted_list + MY_MASTER)) and 
            not self.nama_pemain in self._last_player_greets_me):

            balas_sapaan, emoji = random.choice(jawab_halo), get_random_happy_emoji()
            sapaan, nick = cari_sapaan(list_kata_halo, self.jawab_lain_lower), cari_nick(my_nick_names, self.jawab_lain_lower)
            is_sapaan_my_master = bool(cari_sapaan(list_kata_halo, self.second_last_msg.lower()) and self.second_last_nama_pemain in MY_MASTER)

            self._last_player_greets_me, self._last_player_greet_word = self.nama_pemain, self.jawab_lain
            name = current_session_namelist.get(self.nama_pemain, {}).get('profile_name', self.nama_pemain) if use_their_profile_for_greet_friends else self.nama_pemain

            if sapaan and not is_sapaan_my_master:
                babase.pushcall(Call(chatmessage, f"{balas_sapaan}{f' `{name}`!' if current_session_namelist.get(self.nama_pemain) else ''} {emoji}"), from_other_thread=True)
                print(f"\n({self._last_player_greets_me}) Greets You With Word [{sapaan}] And Nick [{nick}], {emoji}\n")
                if current_session_namelist.get(self.nama_pemain):
                    current_session_namelist[self.nama_pemain]['greeted'] = True
                babase.pushcall(Call(refresh_job, less_respone_delay, defname), from_other_thread=True)
                babase.pushcall(Call(ding_small_high.play), from_other_thread=True)

    def bruh(self):
        defname = self.bruh.__name__
        if defname in is_doing_jobs: return

        baris_baris  = [
            ' █▄▄ █▀█ █░█ █░█',
            ' █▄█ █▀▄ █▄█ █▀█'
        ]

        pemicu = ['amazing', 'amazink', 'luar biasa', 'kerja bagus'] # pemicu/triger

        if not any(name in self.nama_pemain for name in SERVER_NAMES):
            if (any(word in self.jawab_lain_lower for word in pemicu) and not
                any(word in self.jawab_lain_lower for word in custom_replies.keys()) and not
                any(name == self.nama_pemain for name in player_blacklisted_list)):
                for i, baris in enumerate(baris_baris):
                    babase.pushcall(Call(babase.apptimer, i*0.2, Call(chatmessage, baris)), from_other_thread=True)
                babase.pushcall(Call(refresh_job, bruh_respone_delay, defname), from_other_thread=True)

    def vote_kick_analyzer(self):
        defname = self.vote_kick_analyzer.__name__
        if defname in is_doing_jobs: return

        for kick_vote_text in kick_vote_start_texts:
            vote_kick_pattern = f"(.+){kick_vote_text}(.+)"
            match = re.search(vote_kick_pattern, self.jawab_lain)

            if match and any(server_name in self.nama_pemain for server_name in SERVER_NAMES):
                player1 = match.group(1).strip()
                player2 = match.group(2).strip()
                voter_name = _match_player_name(player1, current_namelist)
                voted_name = _match_player_name(player2, current_namelist)
                print(f"Vote kick detected: [{player1} | {voter_name}] *{kick_vote_text}* [{player2} | {voted_name}]")
                if voter_name in MY_MASTER: return
                if voter_name in players_anti_abuse_exception:
                    msg = f'Your friend \"{voter_name}\" is doing a kick vote'
                    babase.pushcall(Call(screenmessage, msg, (0, 1, 1)), from_other_thread=True)
                    return
                if voted_name in MY_MASTER:
                    msg = vote_kicking_started_master_reply.format(name=voter_name) if current_session_namelist.get(voter_name) else vote_kicking_started_master_reply_noname
                    msg += f' {get_random_sad_emoji()}'
                else:
                    msg = vote_kicking_started_reply_message.format(name=voter_name) if current_session_namelist.get(voter_name) else vote_kicking_started_reply_message_noname
                babase.pushcall(Call(chatmessage, msg), from_other_thread=True)
                babase.pushcall(Call(refresh_job, 1, defname), from_other_thread=True)
                break

    def anti_abuse(self):
        if anti_abuse_language_english: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, english_abuses, 'English', balas_english, is_heavy=True)
        if anti_abuse_language_hindi: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, indian_abuses, 'Hindi', balas_indian, is_heavy=True)
        if anti_abuse_language_indonesia: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, indonesian_abuses, 'Indonesia', balas_english, is_heavy=True)

        if responder_config.get(config_name_anti_abuse_chill):
            if anti_abuse_language_english: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, english_abuses_chill, 'English', get_random_unamused_emoji())
            if anti_abuse_language_hindi: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, indian_abuses_chill, 'Hindi', balas_indian_chill)
            if anti_abuse_language_indonesia: detect_and_warn(self.nama_pemain, self.jawab_lain_lower, indonesian_abuses_chill, 'Indonesia', balas_indonesian_chill)

        # Detect inappropriate emojis
        detected_abuse = self.find_abuse(self.jawab_lain_lower, bad_emojis)
        if detected_abuse:
            abuse = detected_abuse[0]
            name = detected_abuse[1]
            if any(icon in self.nama_pemain for icon in SPECIAL_CHARS):
                add_player_abuse_warning(name, balas_bad_emojis, abuse, is_emoji=True)

    def find_abuse(self, sentence: str, abuses: List[str]) -> tuple[str, str] | None:
        """Find Abuse Machine"""
        found = next((abuse for abuse in abuses if abuse in sentence), None)
        if found and (not any(
            name == self.nama_pemain for name in MY_MASTER) and not any(
            name in self.nama_pemain for name in SERVER_NAMES) and not any(
            name == self.nama_pemain for name in players_anti_abuse_exception) and not any(
            cr in sentence for cr in custom_replies.keys())):
            # Check if the message is a sentence or a single word
            if ' ' in sentence:
                # Split message into words and check if abuse word exists independently
                words = sentence.split()
                for word in words:
                    if responder_config.get(config_name_partial_match_abuses):    
                        if (found.strip() in word and not any(ex in word for ex in exception_words_for_anti_abuse)) or found == word:
                            return (found, self.nama_pemain)
                    else:
                        if found == word:
                            return (found, self.nama_pemain)
            else:
                if responder_config.get(config_name_partial_match_abuses):
                    if (found.strip() in sentence and not any(ex in sentence for ex in exception_words_for_anti_abuse)) or found == sentence:
                        return (found, self.nama_pemain)
                else:
                    if found == sentence:
                        return (found, self.nama_pemain)
        return None

class Translate:
    """
    Translate `text` given into configured destination language

    Add callback func `Callable[[str], None]` on second `arg` to give the translated text.
    """
    def __init__(
            self,
            text: str,
            callback: Callable[[str], None] = chatmessage,
            src_lang: Optional[str] = None,
            dst_lang: Optional[str] = None
        ):
        self.text = text
        self._apply_translation = callback
        self.src_lang = src_lang if src_lang else party_config.get(CFG_NAME_TRANSLATE_SOURCE_OTHER, 'auto')
        self.dst_lang = dst_lang if dst_lang else party_config.get(CFG_NAME_TRANSLATE_DESTINATION_OTHER, 'en')
        self.translate_method: str = party_config.get(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, 'api')
        Thread(target=self.run).start()

    def run(self) -> None:
        text_to_translate = self.text
        source_lang: str = self.src_lang
        dest_lang: str = self.dst_lang

        translated_text = None
        if self.translate_method == 'api' and source_lang == 'auto':
            # Combined detection and translation in a single API call
            translated_text = self.translate_text(
                text=text_to_translate,
                src_lang='auto',  # Pass 'auto' to handle detection within the translation call
                dest_lang=dest_lang)
        else:
            translated_text = self.translate_text(
                text=text_to_translate,
                src_lang=source_lang,
                dest_lang=dest_lang)

        if translated_text:
            if str(translated_text).lower() == text_to_translate.lower():
                babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('translateSameResult')}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            else:
                babase.pushcall(Call(self._apply_translation, translated_text), from_other_thread=True)
            #print(f"{self.run.__name__} {text} -> {translated_text}")
        #else:
            #babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('translateFailed')}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            #babase.pushcall(Call(error_sound.play, 1.5), from_other_thread=True)

    def detect_language(self, text: str): # Unused
        """API Only"""
        return self.make_translate_request_api(text, 'auto', 'en', detect_only=True)

    def translate_text(self, text: str, src_lang: str, dest_lang: str) -> Optional[str]:
        if self.translate_method == 'api':
            #print('translating using api')
            translated_text = self.make_translate_request_api(text, src_lang, dest_lang)
        else:
            #print('translating using link')
            translated_text = self.make_translate_request_link(text, src_lang, dest_lang)

        if translated_text and str(translated_text).lower() == text.lower():
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('translateSameResult')}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            #print(f"{self.translate_text.__name__} {text} -> {translated_text}")
            return None
        return translated_text

    def make_translate_request_api(self, text: str, src_lang: str, dest_lang: str, detect_only=False):
        """Make a request to Google Translate API and return translated text or detected language"""
        if src_lang == dest_lang and not detect_only:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('translateSameSrcDest').format(src_lang, dest_lang)} :("
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
            return None

        base_url = 'https://translate.googleapis.com/translate_a/single'
        params = {
            'client': 'gtx',
            'sl': src_lang,
            'tl': dest_lang,
            'dt': 't',
            'q': text
        }
        url = base_url + '?' + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                if detect_only:
                    return data[2]  # Return detected language

                # Extract translated text and detected language
                translated_text = data[0][0][0]
                detected_lang = data[2]

                return translated_text
        except urllib.error.URLError as e:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('translateFailed')} :(", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            print(str(e))
        except http.client.RemoteDisconnected:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('serverDisconnected')} :(", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        except Exception as e:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error Translating: {e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            print_internal_exception(e)
        return None

    def make_translate_request_link(self, text: str, src_lang: str, dest_lang: str):
        """Make a request to Google Translate using direct link and return the result"""
        if src_lang == dest_lang:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('translateSameSrcDest').format(src_lang, dest_lang)} :("
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
            return

        text = urllib.parse.quote(text)
        url = f'https://translate.google.com/m?tl={dest_lang}&sl={src_lang}&q={text}'

        try:
            request = urllib.request.Request(url)
            data = urllib.request.urlopen(request).read().decode('utf-8')
            result = data[
                (data.find('"result-container">'))+len('"result-container">'):data.find('</div><div class="links-container">')
            ]
            replace_list = [('&#39;', '\''), ('&quot;', '"'), ('&amp;', '&')]
            for i in replace_list:
                result = result.replace(i[0], i[1])
            return result
        except urllib.error.URLError as e:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('translateFailed')} :(", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            print(str(e))
        except http.client.RemoteDisconnected:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('serverDisconnected')} :(", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        except Exception as e:
            babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} Error: {e}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
            print_internal_exception(e)
        return None

is_pinging = False
class PingThread:
    def __init__(self, address: str, port: int):
        """Thread for sending out game pings."""
        self._address = address
        self._port = port
        self.run()

    def run(self) -> None:
        sock: Optional[socket.socket] = None
        try:
            global is_pinging
            if is_pinging: return
            is_pinging = True

            socket_type = get_ip_address_type(self._address)
            with socket.socket(socket_type, socket.SOCK_DGRAM) as sock:
                sock.settimeout(7.5)
                starttime = time.time()
                for _i in range(3):
                    sock.sendto(b'\x0b', (self._address, self._port))
                    try:
                        result = sock.recv(10)
                        if result == b'\x0c':
                            break
                    except socket.timeout:
                        pass
                    time.sleep(0.2)  # Adjust delay as needed
                endtime = time.time()
                ping = ((endtime - starttime) * 1000)
            global _server_ping
            _server_ping = ping
            try:
                defname = _ping_server_accurate.__name__
                if defname in is_doing_jobs: return

                if babase.app.classic.party_window(): # type: ignore
                    #if _ping_button.exists():
                        babase.pushcall(CallStrict(bui.buttonwidget,
                            edit=_ping_button, # type: ignore
                            label=f'{str(round(_server_ping))}', # type: ignore
                            textcolor=_get_ping_color()), from_other_thread=True # type: ignore
                        )
            except Exception as e:
                print("Error Ping " + str(e))
        except Exception:
            logging.exception('Error on gather ping')
        finally:
            try:
                is_pinging = False
                if sock is not None:
                    sock.close()
            except Exception:
                logging.exception('Error on gather ping cleanup')

class AddNewChoiceWindow: # Unsued
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self._root_widget = bui.containerwidget(
            size=(500, 250),
            transition='in_right',
            on_outside_click_call=self._close,
            color=bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.3 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -16) if uiscale is babase.UIScale.SMALL else (0, 0))
        self._title_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.8,
            color=(1, 1, 1),
            text=get_lang_text('addCustomCommands'),
            size=(0, 0),
            position=(250, 200),
            h_align='center',
            v_align='center')
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
            corner_scale=0.7)
        self._help_text = bui.textwidget(
            parent=self._root_widget,
            scale=0.6,
            color=(0.8, 0.8, 0.8),
            text=', '.join(CUSTOM_COMMANDS_PREFIX),
            size=(0, 0),
            position=(70, 120),
            h_align='left',
            v_align='center')
        self._add = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 30),
            label='Add',
            button_type='square',
            autoselect=True,
            position=(150, 50),
            on_activate_call=self._add_choice)
        bui.textwidget(edit=self._text_field, on_return_press_call=self._add.activate)

        self._remove = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 30),
            label='Remove',
            button_type='square',
            autoselect=True,
            position=(350, 50),
            on_activate_call=self._remove_custom_command)
        bui.containerwidget(edit=self._root_widget, on_cancel_call=self._close)

    def _add_choice(self):
        newCommand = bui.textwidget(query=self._text_field)
        data = _load_custom_commands()
        if any(i in newCommand for i in CUSTOM_COMMANDS_PREFIX):
            data.append(newCommand)
            _save_custom_commands(data)
            screenmessage(get_lang_text('addSuccess'), (0, 1, 0))
            bui.getsound('dingSmallHigh').play()
            self._close()
        else:
            custom_cmd_prefix_joint: str = ', '.join(CUSTOM_COMMANDS_PREFIX)
            screenmessage(get_lang_text('customCommandsNoCmdPrefix').format(custom_cmd_prefix_joint), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

    def _remove_custom_command(self):
        uiscale = bui.app.ui_v1.uiscale
        commands = _load_custom_commands()
        PopupMenuWindow(
            position=self._remove.get_screen_space_center(),
            color=party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color), # type: ignore
            scale=(2.4 if uiscale is babase.UIScale.SMALL else
                    1.5 if uiscale is babase.UIScale.MEDIUM else
                    1.0),
            choices=commands,
            current_choice=commands[0],
            delegate=self)
        self._popup_type = 'removeCustomCommandSelect'

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        """Called when a choice is selected in the popup."""
        if self._popup_type == 'removeCustomCommandSelect':
            data = _load_custom_commands()
            data.remove(choice)
            _save_custom_commands(data)
            screenmessage(get_lang_text('removeSuccess'), (0, 1, 0))
            bui.getsound('shieldDown').play()

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _close(self):
        bui.containerwidget(edit=self._root_widget, transition=('out_scale'))
        bui.getsound('swish').play()


class SortMessagesList:
    def __init__(self, data: List[str], write_data_func: Callable[[List[str]], None], label: str, needs_commands_prefix: bool = False):
        """Sort List Data"""
        uiscale = bui.app.ui_v1.uiscale
        bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self._width = (600 if uiscale is babase.UIScale.SMALL else # Small
                       750 if uiscale is babase.UIScale.MEDIUM else # Medium
                       825) # Large
        self._height = (325 if uiscale is babase.UIScale.SMALL else # Small
                        375 if uiscale is babase.UIScale.MEDIUM else # Medium
                        425) # Large
        self.needs_commands_prefix = needs_commands_prefix
        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            on_outside_click_call=self._save,
            color=bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.3 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -16) if uiscale is babase.UIScale.SMALL else (0, 0))
        label_textwidget = bui.textwidget(parent=self._root_widget,
                      position=(self._width * 0.10, self._height - 50),
                      size=(self._width * 0.5, 25),
                      text=label,
                      color=bui.app.ui_v1.title_color,
                      scale=1.05,
                      h_align='center',
                      v_align='center',
                      maxwidth=270)
        b_textcolor = (0.4, 0.75, 0.5)
        up_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10, 185),
            size=(75, 75),
            on_activate_call=self._move_up,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True)
        down_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(10, 90),
            size=(75, 75),
            on_activate_call=self._move_down,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            autoselect=True,
            repeat=True)
        back_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.0025, self._height * 0.825),
            size=(50, 50),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._save,
            color=bg_color,
            iconscale=1.2)

        self._scroll_width = self._width - 150
        self._scroll_height = self._height - 130
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._scroll_height),
            color=bg_color,
            position=(100, 65))
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0)

        self._attribute_text_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(self._scroll_width, 30),
            position=(100, self._height * 0.055),
            text='',
            maxwidth=300,
            shadow=0.3,
            flatness=1.0,
            description='Enter attribute here',
            autoselect=True,
            v_align='center'
        )

        delete_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.9375, self._height * 0.675),
            size=(50, 50),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2,
            on_activate_call=self._delete_attribute,
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            enable_sound=False,
            autoselect=True,
            repeat=False)
        edit_attribute_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.9375, self._height * 0.475),
            size=(50, 50),
            icon=bui.gettexture('replayIcon'),
            iconscale=1.25,
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            enable_sound=False,
            on_activate_call=self._edit_attribute,
            autoselect=True
        )
        add_attribute_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.9375, self._height * 0.275),
            size=(50, 50),
            icon=bui.gettexture('powerupHealth'),
            iconscale=1.25,
            button_type='square',
            color=bg_color,
            textcolor=b_textcolor,
            enable_sound=False,
            on_activate_call=self._add_attribute,
            autoselect=True
        )
        bui.textwidget(edit=self._attribute_text_field, on_return_press_call=add_attribute_button.activate)

        copy_text_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width * 0.9375, self._height * 0.125),
            size=(25, 25),
            label='©',
            button_type='backSmall',
            color=bg_color,
            textcolor=b_textcolor,
            on_activate_call=self._copy_text,
            autoselect=True
        )

        self.msgs = data
        self.original_msgs = data # the not edited data
        self.save = write_data_func

        self._msg_selected = []
        self.text_widgets_dict: Dict[str, bui.Widget] = {}  # Dictionary to store text widgets
        """`Msg`: `TextWidget`"""
        self._refresh()
        bui.containerwidget(edit=self._root_widget, on_cancel_call=self._save)

    def _refresh(self):
        for child in self._columnwidget.get_children():
            child.delete()
        for msg in enumerate(self.msgs):
            txt = bui.textwidget(
                parent=self._columnwidget,
                size=(self._scroll_width - 10, 30),
                selectable=True,
                always_highlight=True,
                on_select_call=CallStrict(self._on_msg_select, msg),
                text=msg[1],
                h_align='left',
                v_align='center',
                maxwidth=self._scroll_width)
            self.text_widgets_dict[msg[1]] = txt
            if msg == self._msg_selected:
                bui.columnwidget(edit=self._columnwidget,
                                selected_child=txt,
                                visible_child=txt)

    def _on_msg_select(self, msg):
        self._msg_selected = msg
        index = self._msg_selected[0]
        if self._msg_selected:
            if index >= 0 and index < len(self.msgs):  # Check if index is valid
                msg = self.msgs[index]
                bui.textwidget(edit=self._attribute_text_field, text=msg)  # Show selected msg in attribute text field
            else:
                self._refresh()
                self._msg_selected = []  # Clear selection if the message does not exist
                bui.textwidget(edit=self._attribute_text_field, text='')  # Clear the text field if no message is selected

    def _move_up(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index:
            self.msgs.insert((index - 1), self.msgs.pop(index))
            self._msg_selected = (index - 1, msg)
            self._refresh()

    def _move_down(self):
        index = self._msg_selected[0]
        msg = self._msg_selected[1]
        if index + 1 < len(self.msgs):
            self.msgs.insert((index + 1), self.msgs.pop(index))
            self._msg_selected = (index + 1, msg)
            self._refresh()

    def _add_attribute(self):
        attribute: str = bui.textwidget(query=self._attribute_text_field)
        attribute = attribute.strip()
        if attribute:
            if attribute in self.msgs:  # Check if attribute already exists
                screenmessage(get_lang_text('editAttributeExist'), COLOR_SCREENCMD_ERROR)  # Show message
                bui.getsound('error').play(1.5)
            else:
                if self.needs_commands_prefix and not any(prefix in attribute for prefix in CUSTOM_COMMANDS_PREFIX):
                    screenmessage(get_lang_text('customCommandsNoCmdPrefix').format(', '.join(CUSTOM_COMMANDS_PREFIX)), COLOR_SCREENCMD_ERROR)
                    bui.getsound('error').play(1.5)
                    return
                self.msgs.append(attribute)
                bui.textwidget(edit=self._attribute_text_field, text='')  # Clear the text field
                self._refresh()
                bui.getsound('shieldUp').play(1.5)
        else:
            screenmessage(get_lang_text('editAttributeAddEmpty'), COLOR_SCREENCMD_ERROR)
            bui.textwidget(edit=self._attribute_text_field, text='')
            bui.getsound('error').play(1.5)

    def _edit_attribute(self):
        selected_msg: str | None = bui.textwidget(query=self.text_widgets_dict.get(self._msg_selected[1])) if self.text_widgets_dict.get(self._msg_selected[1]) else None
        new_text: str = bui.textwidget(query=self._attribute_text_field)
        new_text = new_text.strip()
        if selected_msg:
            if new_text:
                if selected_msg != new_text:
                    index: int = self._msg_selected[0]
                    msg: str = self._msg_selected[1]
                    textwidget = self.text_widgets_dict.get(msg)
                    self.msgs[index] = new_text
                    bui.getsound('shieldUp').play(1.5)
                    if textwidget:
                        bui.textwidget(edit=textwidget, text=new_text)
                    else:
                        self._refresh()
                else:
                    screenmessage(get_lang_text('editAttributeSame'), COLOR_SCREENCMD_ERROR)  # Show message
                    bui.getsound('error').play(1.5)
            else:
                screenmessage(get_lang_text('editAttributeEmpty'), COLOR_SCREENCMD_ERROR)
                bui.textwidget(edit=self._attribute_text_field, text='')
                bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('editAttributeEmpty'), COLOR_SCREENCMD_ERROR)
            bui.textwidget(edit=self._attribute_text_field, text='')
            bui.getsound('error').play(1.5)

    def _delete_attribute(self):
        if self._msg_selected:
            if self.msgs:
                index: int = self._msg_selected[0]
                msg = self.msgs.pop(index)
                self.text_widgets_dict[msg].delete() # Delete that text widget
                del self.text_widgets_dict[msg]
                if index > 0:  # Check if there is a message above
                    self._msg_selected = (index - 1, self.msgs[index - 1])  # Select the message above
                bui.getsound('shieldDown').play(1.5)
            else:
                screenmessage(get_lang_text('editAttributeDeleteEmpty'), COLOR_SCREENCMD_ERROR)
                bui.textwidget(edit=self._attribute_text_field, text='')
                bui.getsound('error').play(1.5)

    def _copy_text(self):
        msg_to_copy = bui.textwidget(query=self._attribute_text_field)
        _copy_to_clipboard(msg_to_copy)

    def _save(self) -> None:
        try:
            self.save(self.msgs)
        except:
            logging.exception()
            screenmessage('Error!', COLOR_SCREENCMD_ERROR)
        if self.original_msgs != self.msgs:
            bui.getsound('gunCocking').play()
        bui.containerwidget(
            edit=self._root_widget,
            transition='out_right')
        bui.getsound('swish').play()

class ColorTracker:
    def __init__(self):
        self.saved: Dict[str, tuple[float, float, float]] = {}

    def _get_safe_color(self, sender):
        while True:
            color = (random.random(), random.random(), random.random())
            s = 0
            background = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
            for i, j in zip(color, background):
                s += (i - j) ** 2
            if s > 0.1:
                self.saved[sender] = color
                if len(self.saved) > 20:
                    self.saved.pop(list(self.saved.keys())[0])
                break
            time.sleep(0.1)

    def _get_sender_color(self, sender: str):
        if sender not in self.saved:
            self.thread = Thread(target=self._get_safe_color, args=(sender,))
            self.thread.start()
            return TEXTWIDGET_DEFAULT_COLOR
        else:
            return self.saved[sender]

global color_tracker
color_tracker = ColorTracker()

LANGUAGES = {
    'auto': 'Auto-detect',
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'f': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'}
LANGUAGES = {'auto': 'Auto-detect', **dict(sorted(LANGUAGES.items(), key=lambda item: item[1]))}

translate_text_tutorial = False
class PartySettingsWindow:
    def __init__(self):
        self.uiscale = bui.app.ui_v1.uiscale
        size_map = {
            babase.UIScale.SMALL: (600, 350),
            babase.UIScale.MEDIUM: (700, 400),
            babase.UIScale.LARGE: (800, 450)
        }
        width, height = size_map.get(self.uiscale, (650, 400))

        scroll_w = width*0.9
        scroll_h = height*0.725

        self.max_width = scroll_w * 0.935
        self.barrier_space = 20

        self.root_widget = bui.containerwidget(
            size=(width, height),
            color=party_config.get(CFG_NAME_MAIN_COLOR, (0.5, 0.5, 0.5)),
            transition='in_scale',
            scale={babase.UIScale.SMALL: 1.8, babase.UIScale.MEDIUM: 1.5, babase.UIScale.LARGE: 1.3}.get(self.uiscale, 1.0),
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self.on_outside_press)

        self._title = bui.textwidget(parent=self.root_widget, position=(width * 0.5, height - 45),
                      size=(20, 20), h_align='center', v_align='center',
                      text=get_lang_text('pswTitle'), scale=0.9, color=(1, 1, 1, 0.75))

        self.cancel_button = bui.buttonwidget(parent=self.root_widget, position=(30, height - 55), size=(30, 30),
                        label=babase.charstr(babase.SpecialChar.BACK), button_type='backSmall',
                        on_activate_call=self._cancel)

        self._scrollwidget = bui.scrollwidget(parent=self.root_widget, position=(30, 40),
                                             size=(scroll_w, scroll_h), selection_loops_to_parent=True)
        self._subcontainer = bui.columnwidget(parent=self._scrollwidget, selection_loops_to_parent=True)

        bui.containerwidget(edit=self.root_widget, cancel_button=self.cancel_button)


        self._start_adding_childs()
        self.focus_to_child(self._bool_options_textwidgets.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT))

    def _start_adding_childs(self):
        self._bool_options_textwidgets: Dict[str, bui.Widget] = {}
        self.start_adding_checkboxes()

        self._popup_menus_popups: Dict[str, bui.Widget] = {}
        self.start_adding_popup_menus()

        self._global_variables_textwidgets: Dict[str, bui.Widget] = {}
        self.global_variables()

        self.translate_settings()
        self.translate_text_button()

        bui.textwidget(edit=self._title, text=get_lang_text('pswTitle'))

    def focus_to_child(self, button: bui.Widget | None):
        if button is None: return
        chosen_check_box = CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT
        bui.containerwidget(
            edit=self._subcontainer,
            visible_child=self._bool_options_textwidgets[chosen_check_box],
            selected_child=self._bool_options_textwidgets[chosen_check_box]
        )

    def global_variables(self):
        global maximum_party_window_chats, MAX_WARNS, PING_MESSAGE
        global PARTY_WINDOW_SCALE_SMALL, PARTY_WINDOW_SCALE_MEDIUM, PARTY_WINDOW_SCALE_LARGE

        global_var_options: List[tuple[str, Optional[str], float | int | str | list[str], bool]] = [
            ("max_pw_chats", get_lang_text('pswGlobalVarMaxPartywindowChats'), maximum_party_window_chats, True),
            ("ping_msg", get_lang_text('pswGlobalVarPingMessage'), PING_MESSAGE, True),
            ("max_warns", get_lang_text('pswGlobalVarMaxWarns'), MAX_WARNS, True),
            ("pw_scale_small", get_lang_text('pswGlobalVarPartyScale'), PARTY_WINDOW_SCALE_SMALL, False),
            ("pw_scale_medium", None, PARTY_WINDOW_SCALE_MEDIUM, False),
            ("pw_scale_large", None, PARTY_WINDOW_SCALE_LARGE, True)
        ]

        self.ping_message_textwidget = []
        for key, display, value, barrier in global_var_options:
            if display:
                bui.textwidget(
                    parent=self._subcontainer,
                    size=(self.max_width, 30),
                    maxwidth=self.max_width,
                    text=display,
                    editable=False,
                    autoselect=True
                )
            
            if isinstance(value, list):
                for msg in value:
                    textwidget = bui.textwidget(
                        parent=self._subcontainer,
                        size=(self.max_width, 30),
                        maxwidth=self.max_width,
                        text=msg,
                        editable=True,
                        autoselect=True
                    )
                    if key == "ping_msg":
                        self.ping_message_textwidget.append(textwidget)
                    self._global_variables_textwidgets[key] = textwidget
            else:
                textwidget = bui.textwidget(
                    parent=self._subcontainer,
                    size=(self.max_width, 30),
                    maxwidth=self.max_width,
                    text=str(value),
                    editable=True,
                    autoselect=True
                )
                self._global_variables_textwidgets[key] = textwidget

                if key == "max_pw_chats":
                    self.max_chats_textwidget = textwidget
                elif key == "max_warns":
                    self.max_warns_textwidget = textwidget
                elif key == "pw_scale_small":
                    self.pw_scale_small_textwidget = textwidget
                elif key == "pw_scale_medium":
                    self.pw_scale_medium_textwidget = textwidget
                elif key == "pw_scale_large":
                    self.pw_scale_large_textwidget = textwidget

            if barrier:
                bui.textwidget(parent=self._subcontainer, text='', size=(self.max_width, self.barrier_space))

    def update_global_var(self):
        global maximum_party_window_chats, MAX_WARNS, PING_MESSAGE
        global PARTY_WINDOW_SCALE_SMALL, PARTY_WINDOW_SCALE_MEDIUM, PARTY_WINDOW_SCALE_LARGE

        # Update global variables from textwidget values
        try:
            maximum_party_window_chats = int("".join([num for num in bui.textwidget(query=self.max_chats_textwidget) if num.isnumeric()]))
            if maximum_party_window_chats < 10:
                maximum_party_window_chats = 10
            elif not isinstance(maximum_party_window_chats, int):
                maximum_party_window_chats = maximum_bombsquad_chat_messages
        except ValueError as e:
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

        try:
            MAX_WARNS = int("".join([num for num in bui.textwidget(query=self.max_warns_textwidget) if num.isnumeric()]))
            if MAX_WARNS < 2:
                MAX_WARNS = 2
            elif not isinstance(MAX_WARNS, int):
                MAX_WARNS = 3
        except ValueError as e:
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

        try:
            if isinstance(self.ping_message_textwidget, list):
                PING_MESSAGE = []
                for widget in self.ping_message_textwidget:
                    if bui.textwidget(query=widget).strip():
                        messages = str(bui.textwidget(query=widget)).split('\\n')
                        PING_MESSAGE.extend([msg.strip() for msg in messages if msg.strip()])
            else:
                ping_msg = str(bui.textwidget(query=self.ping_message_textwidget))
                PING_MESSAGE = [ping_msg] if ping_msg.strip() else ['Ping-pong🏓 {}ms']
        except ValueError as e:
            if not PING_MESSAGE:
                ping_msg = str(bui.textwidget(query=self.ping_message_textwidget))
                PING_MESSAGE = [ping_msg] if ping_msg.strip() else ['Ping-pong🏓 {}ms']
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

        try:
            PARTY_WINDOW_SCALE_SMALL = float("".join([num for num in bui.textwidget(query=self.pw_scale_small_textwidget) if num.isnumeric() or num == '.']))
            if PARTY_WINDOW_SCALE_SMALL < 0.5:
                PARTY_WINDOW_SCALE_SMALL = 0.5
            elif PARTY_WINDOW_SCALE_SMALL > 1.5:
                PARTY_WINDOW_SCALE_SMALL = 1.0
        except ValueError as e:
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

        try:
            PARTY_WINDOW_SCALE_MEDIUM = float("".join([num for num in bui.textwidget(query=self.pw_scale_medium_textwidget) if num.isnumeric() or num == '.']))
            if PARTY_WINDOW_SCALE_MEDIUM < 0.5:
                PARTY_WINDOW_SCALE_MEDIUM = 0.5
            elif PARTY_WINDOW_SCALE_MEDIUM > 1.5:
                PARTY_WINDOW_SCALE_MEDIUM = 1.0
        except ValueError as e:
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)

        try:
            PARTY_WINDOW_SCALE_LARGE = float("".join([num for num in bui.textwidget(query=self.pw_scale_large_textwidget) if num.isnumeric() or num == '.']))
            if PARTY_WINDOW_SCALE_LARGE < 0.5:
                PARTY_WINDOW_SCALE_LARGE = 0.5
            elif PARTY_WINDOW_SCALE_LARGE > 1.5:
                PARTY_WINDOW_SCALE_LARGE = 1.0
        except ValueError as e:
            screenmessage(get_lang_text('pswGlobalVarInvalidInput').format(str(e)), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)


    def start_adding_checkboxes(self):
        ############################### CHECKBOXES ###############################
        bool_options: List[tuple[str, str, Callable[[str, str, bui.Widget, bool], None] | None, bool | None]] = [
            (CFG_NAME_ACCURATE_SERVER_PING_SEND, get_lang_text('pswCheckboxAccuratePing'), self._apply_config, True),
            (CFG_NAME_BUTTON_PING, get_lang_text('pswCheckboxPing'), self._apply_config, None),
            (CFG_NAME_BUTTON_IP, get_lang_text('pswCheckboxIP'), self._apply_config, None),
            (CFG_NAME_BUTTON_COPY_PASTE, get_lang_text('pswCheckboxCopyPaste'), self._apply_config, None),
            (CFG_NAME_INSTANT_QUICK_RESPOND, get_lang_text('pswCheckboxQuickRespond'), self._apply_config, True),
            (CFG_NAME_AUTO_GREET_FRIENDS, get_lang_text('pswCheckboxAutoGreet'), self._apply_config, None),
            (CFG_NAME_AUTO_GREET_FRIENDS_IF_MASTER_JOINED, get_lang_text('pswCheckboxAutoGreetMaster'), self._apply_config, None),
            (CFG_NAME_AUTO_GREET_FRIENDS_IF_FRIENDS_JOINED, get_lang_text('pswCheckboxAutoGreetFriends'), self._apply_config, True),
            (CFG_NAME_DIRECT_CUSTOM_CMD, get_lang_text('pswCheckboxDirectCustomCmd'), self._apply_config, None),
            (CFG_NAME_BLOCK_NA_CMD, get_lang_text('pswCheckboxBlockNACommand'), self._apply_config, None),
            (CFG_NAME_ASK_GAME_REPLAY_NAME, get_lang_text('pswCheckboxAskGameReplayName'), self._apply_config, None),
            (CFG_NAME_COLORFUL_CHATS, get_lang_text('pswCheckboxColorfulChats'), self._apply_config, None),
            (CFG_NAME_FOCUS_TO_LAST_MSG, get_lang_text('pswCheckboxFocusToLastMsg'), self._apply_config, True),
            (CFG_NAME_HIGHLIGHT_CHOSEN_TEXT, get_lang_text('pswCheckboxHighlightChosenText'), self._apply_config, None),
            (CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT, get_lang_text('pswCheckboxIncludePnameOnChosenText'), self._apply_config, None),
            (CFG_NAME_INCLUDE_CID_IN_QC_NAME_CHANGER, get_lang_text('pswCheckboxIncludeCidInQcNameChanger'), self._apply_config, True),
            (CFG_NAME_SAVE_LAST_TYPED_MSG, get_lang_text('pswCheckboxSaveLastTypedMsg'), self._apply_config, True),
            (CFG_NAME_MODIFIED_SCREENMESSAGE, get_lang_text('pswCheckboxCustomScreenmessage'), self._apply_config, None),
            (CFG_NAME_COLORFUL_SCRMSG, get_lang_text('pswCheckboxColorfulScreenmessage'), self._apply_config, None),
            (CFG_NAME_CHAT_NAME_VIEWER_IN_SCRMSG, get_lang_text('pswCheckboxChatNameViewerInScrmsg'), self._apply_config, None),
        ]

        y_pos = 0
        for data in bool_options:
            if len(data) >= 3:
                cfg_key = data[0]
                msg = data[1]
                callback = data[2]
                widget = bui.checkboxwidget(
                    parent=self._subcontainer,
                    size=(self.max_width+(self.max_width*0.4), 31),
                    maxwidth=self.max_width+(self.max_width*0.15),
                    text=msg,
                    scale=0.8,
                    position=(0, y_pos),
                    value=party_config[cfg_key],
                    textcolor=(0, 1, 0) if party_config[cfg_key] else (0.95, 0.65, 0)
                )
                bui.checkboxwidget(
                    edit=widget,
                    on_value_change_call=CallStrict(callback, cfg_key, msg, widget) if callback else None
                )
                self._bool_options_textwidgets[cfg_key] = widget
                y_pos -= 10

            if data[-1] == True:
                barrier = bui.textwidget(parent=self._subcontainer, text='', size=(self.max_width, self.barrier_space)) # Barrier
        ############################### CHECKBOXES ###############################

    def start_adding_button(self):
        ##################### BUTTON WIDGET #####################
        button_options: List = [
            
        ]
        for data in button_options:
            cfg_key = data[0]
            text = data[1]
            callback = data[2]
            bui.buttonwidget(
            parent=self._subcontainer,
            position=(0, 0),
            size=(min(300, len(text) * 13.5)),
            label=text,
            scale=1,
            on_activate_call=callback,
            autoselect=False
        )
        ##################### BUTTON WIDGET #####################

    def start_adding_popup_menus(self):
        ##################### POPUP MENUS #####################
        popup_menu_options: List[tuple[str, str, List[str], List[str] | None, Callable[[str], None], str]] = [
            (CFG_NAME_MESSAGE_NOTIFICATION_POS, 
                get_lang_text('psMessageNotificationPosKey'), 
                ['top', 'bottom'], 
                [get_lang_text('psMessageNotificationPosTOP'),
                    get_lang_text('psMessageNotificationPosBOTTOM')],
                self._change_notification,
                party_config[CFG_NAME_MESSAGE_NOTIFICATION_POS]),

            ("UIScale", 
                get_lang_text('psBsUiScaleKey'),
                ["2", "1", "0"],
                [get_lang_text('psBsUiScaleSMALL'),
                    get_lang_text('psBsUiScaleMEDIUM'),
                    get_lang_text('psBsUiScaleLARGE')],
                self._set_uiscale,
                str(babase.app.config['UIScale'])),

            (CFG_NAME_PREFFERED_LANG, 
                get_lang_text('psMainLanguage').format(__name__), 
                DEFAULT_AVAILABLE_LANG_ID_LIST, 
                DEFAULT_AVAILABLE_LANG_LIST, 
                self._change_lang, 
                party_config[CFG_NAME_PREFFERED_LANG])
        ]

        for cfg_key, label, choices, choices_display, callback, current_choice in popup_menu_options:
            bui.textwidget(parent=self._subcontainer, text=label, size=(self.max_width, 30), h_align='left', v_align='center', color=(1, 1, 1))
            popup = PopupMenu(
                parent=self._subcontainer,
                position=(0, 0),
                width=200,
                scale=(2.8 if self.uiscale is UIScale.SMALL else
                       2.2 if self.uiscale is UIScale.MEDIUM else
                       1.2),
                choices=choices,
                choices_display=list(babase.Lstr(value=i) for i in choices_display) if choices_display else None,
                current_choice=current_choice,
                on_value_change_call=callback
            )
            self._popup_menus_popups[cfg_key] = popup.get_window_widget()
            bui.textwidget(parent=self._subcontainer, text='', size=(self.max_width, self.barrier_space)) # Barrier
        ##################### POPUP MENUS #####################


    #################### CONFIG APPLY ####################
    def _apply_config(self, key: str, message: str, widget: bui.Widget, v: bool):
        global party_config
        party_config[key] = v
        #screenmessage(f"{message} {get_lang_text('enabled') if value else get_lang_text('disabled')}", color=(0, 1, 0) if value else (1, 0.7, 0))
        if widget and widget.exists():
            bui.checkboxwidget(
                edit=widget,
                textcolor=(0, 1, 0) if party_config[key] else (0.95, 0.65, 0)
            )
        if key == CFG_NAME_MODIFIED_SCREENMESSAGE:            
            try:
                global is_muted
                babase.app.config['Chat Muted'] = v
                babase.app.config.apply_and_commit()
                is_muted = babase.app.config.resolve('Chat Muted')
            except Exception as e:
                print_internal_exception(e)


    def _change_notification(self, choice: str):
        global party_config
        party_config[CFG_NAME_MESSAGE_NOTIFICATION_POS] = choice

    def _change_lang(self, lang_id: str):
        global party_config, warning_translate_text, translate_text_tutorial
        translate_text_tutorial = False
        warning_translate_text = False
        party_config[CFG_NAME_PREFFERED_LANG] = lang_id
        screenmessage(get_lang_text('psMainLanguageChanged').format(DEFAULT_AVAILABLE_LANG_LIST[DEFAULT_AVAILABLE_LANG_ID_LIST.index(lang_id)]), color=(0,1,0))
        if self._subcontainer and self._subcontainer.exists(): self._subcontainer.delete()
        self._subcontainer = bui.columnwidget(parent=self._scrollwidget, selection_loops_to_parent=True)
        self._start_adding_childs()

    def _set_uiscale(self, val: str) -> None:
        num = int(''.join(num for num in val if num.isnumeric()))
        cfg = babase.app.config
        cfg['UIScale'] = num
        cfg.apply_and_commit()
        self.update_uiscale()
    
    def update_uiscale(self) -> None:
        if babase.app.config['UIScale'] == 0:
            uiscale = UIScale.LARGE
        elif babase.app.config['UIScale'] == 1:
            uiscale = UIScale.MEDIUM
        else:
            uiscale = UIScale.SMALL
        bui.app.ui_v1._uiscale = uiscale

    def translate_text_button(self):
        text = get_lang_text('pswButtonTranslatedTextsDict')
        def open_window():
            last_usage_str = party_config.get(CFG_NAME_PLUGIN_FRESH_USAGE_TIME)
            app_date = babase.app.config.get(CFG_NAME_PLUGIN_FRESH_USAGE_TIME)
            if app_date:
                last_usage_str = app_date
            else:
                babase.app.config[CFG_NAME_PLUGIN_FRESH_USAGE_TIME] = datetime.now().strftime("%d-%m-%Y")
                babase.app.config.apply_and_commit()
                last_usage_str = babase.app.config[CFG_NAME_PLUGIN_FRESH_USAGE_TIME]
            if last_usage_str:
                try:
                    last_usage_date = datetime.strptime(last_usage_str, "%d-%m-%Y")
                    current_date = datetime.now()
                    days_since_last_usage = (current_date - last_usage_date).days

                    if days_since_last_usage < 3:
                        screenmessage(get_lang_text('psNewUserOpenTranslatedDict').format(str(3 - days_since_last_usage)), color=COLOR_SCREENCMD_ERROR)
                        bui.getsound('error').play(1.5)
                        return
                except ValueError:
                    screenmessage(get_lang_text('psNewUserOpenTranslatedDictInvalidDate'), COLOR_SCREENCMD_ERROR)
                    party_config[CFG_NAME_PLUGIN_FRESH_USAGE_TIME] = datetime.now().strftime("%d-%m-%Y")
                    bui.getsound('error').play(1.5)
                    return
            TranslateTextsPopup(Translate_Texts)
        bui.buttonwidget(
            parent=self._subcontainer,
            position=(0, 0),
            size=(min(400, len(text)*14), 50),
            label=text,
            scale=1,
            on_activate_call=open_window,
            autoselect=False
        )
        bui.textwidget(parent=self._subcontainer, text='', size=(self.max_width, self.barrier_space)) # Barrier

    def translate_settings(self):
        def open_window():
            global translate_text_tutorial
            if not translate_text_tutorial:
                screenmessage(get_lang_text('pswButtonTranslateWindowSettingsTutorial'), COLOR_SCREENCMD_NORMAL)
            translate_text_tutorial = True
            TranslationSettings()
        text = get_lang_text('pswButtonTranslateWindowSettings')
        bui.buttonwidget(
            parent=self._subcontainer,
            position=(0, 0),
            size=(min(400, len(text)*14), 50),
            label=text,
            scale=1,
            on_activate_call=open_window,
            autoselect=False
        )
        bui.textwidget(parent=self._subcontainer, text='', size=(self.max_width, self.barrier_space)) # Barrier

    #################### CONFIG APPLY ####################
    def on_outside_press(self):
        bui.getsound('swish').play()
        self._cancel()

    def _cancel(self) -> None:
        global party_config
        save_party_config(party_config)
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        self.update_global_var()

class TranslationSettings:
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        # Calculate height based on number of settings
        base_height = 225
        self.height = base_height + (40 * len(self._get_translation_settings()))  # Add 50px per setting
        self.width = 500

        self.cfg = party_config
        bg_color = self.cfg.get(CFG_NAME_MAIN_COLOR, (0.5, 0.5, 0.5))

        self.root_widget = bui.containerwidget(
            size=(self.width, self.height),
            color=bg_color,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(2.1 if uiscale is babase.UIScale.SMALL else
                   1.5 if uiscale is babase.UIScale.MEDIUM else 1.0))
        
        bui.textwidget(parent=self.root_widget,
                      position=(self.width * 0.5, self.height - 20),
                      size=(0, 0),
                      h_align='center',
                      v_align='center',
                      text=get_lang_text('translateSettingsTitle'),
                      scale=1,
                      shadow=1.5,
                      color=(5, 5, 5))
        
        btn = bui.buttonwidget(parent=self.root_widget,
                             autoselect=True,
                             position=(30, self.height - 60),
                             size=(30, 30),
                             label=babase.charstr(babase.SpecialChar.BACK),
                             button_type='backSmall',
                             on_activate_call=self._cancel)

        # Create translation settings with section titles
        y_pos = self.height - 80
        settings = self._get_translation_settings()
        
        # Add Text Field section title
        bui.textwidget(parent=self.root_widget,
                     position=(self.width*0.5, y_pos+20),
                     size=(0, 0),
                     h_align='center',
                     v_align='center',
                     text=get_lang_text('translateSettingsTextfield'),
                     scale=1.0,
                     color=(1, 1, 1))
        
        # Create Text Field settings
        x_offset = self.width*0.45
        master_settings = settings['text_field']
        self._create_setting_ui(master_settings['source'], y_pos - 30, 0)
        self._create_setting_ui(master_settings['destination'], y_pos - 30, x_offset)

        y_pos -= 80

        # Add Other section title
        bui.textwidget(parent=self.root_widget,
                     position=(self.width*0.5, y_pos),
                     size=(0, 0),
                     h_align='center',
                     v_align='center',
                     text=get_lang_text('translateSettingsOther'),
                     scale=1.0,
                     color=(1, 1, 1))

        # Create Other settings
        other_settings = settings['other']
        self._create_setting_ui(other_settings['source'], y_pos - 50, 0)
        self._create_setting_ui(other_settings['destination'], y_pos - 50, x_offset)

        bui.containerwidget(edit=self.root_widget, cancel_button=btn)

        y_pos -= 100
        
        # Add Translation Method section title
        bui.textwidget(parent=self.root_widget,
                    position=(self.width*0.1, y_pos),
                    size=(0, 0),
                    h_align='left',
                    v_align='center',
                    text=get_lang_text('translateMethod'),
                    scale=1.0,
                    color=(1, 1, 1))

        # Create PopupMenu for translation method
        PopupMenu(
            parent=self.root_widget,
            position=(self.width*0.0875 + x_offset+(x_offset*0.25), y_pos - 20),
            width=200,
            scale=(2.8 if bui.app.ui_v1.uiscale is babase.UIScale.SMALL else
                1.8 if bui.app.ui_v1.uiscale is babase.UIScale.MEDIUM else 1.2),
            current_choice=self.cfg[CFG_NAME_TRANSLATE_PREFERRED_MACHINE],
            choices=['api', 'link'],
            choices_display=[babase.Lstr(value=get_lang_text('translateMethodAPI')), babase.Lstr(value=get_lang_text('translateMethodLINK'))],
            button_size=(130, 35),
            on_value_change_call=CallStrict(self._change_setting, CFG_NAME_TRANSLATE_PREFERRED_MACHINE)
        )

    def _create_setting_ui(self, setting:Dict[str, Any], y_pos: float, x_offset: float):
        """Create UI elements for a single translation setting"""
        
        bui.textwidget(parent=self.root_widget,
                     position=(self.width*0.5, y_pos+15),
                     size=(0, 0),
                     h_align='center',
                     v_align='center',
                     text="",
                     scale=1.0,
                     color=(1, 1, 1))
        
        # Create menu
        PopupMenu(
            parent=self.root_widget,
            position=(self.width*0.0875 + x_offset+(x_offset*0.25), y_pos),
            width=200,
            scale=(2.8 if bui.app.ui_v1.uiscale is babase.UIScale.SMALL else
                   1.8 if bui.app.ui_v1.uiscale is babase.UIScale.MEDIUM else 1.2),
            current_choice=self.cfg[setting['config']],
            choices=setting['choices'],
            choices_display=list(babase.Lstr(value=i) for i in [LANGUAGES[l] for l in setting['choices']]),
            button_size=(130, 35),
            on_value_change_call=CallStrict(self._change_setting, setting['config'])
        )

    def _get_translation_settings(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Return list of translation settings to display"""
        return {
            "text_field": {
                "source": {
                    'config': CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD,
                    'choices': list(LANGUAGES.keys())
                },
                "destination": {
                    'config': CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD,
                    'choices': list(LANGUAGES.keys())[1:]
                }
            },
            "other": {
                "source": {
                    'config': CFG_NAME_TRANSLATE_SOURCE_OTHER,
                    'choices': list(LANGUAGES.keys())
                },
                "destination": {
                    'config': CFG_NAME_TRANSLATE_DESTINATION_OTHER,
                    'choices': list(LANGUAGES.keys())[1:]
                }
            }
        }

    def _change_setting(self, config_name: str, choice: str):
        """Handle change for any translation setting"""
        global party_config
        party_config[config_name] = choice

    def _cancel(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        bui.getsound('swish').play()
        global party_config
        save_party_config(party_config)

class ResponderSettingsWindow(popup.PopupWindow):
    """Responder Settings Window"""
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        self._is_refreshing = False
        self._width = 650
        self._height = 360
        self.bg_color = (0.35, 0.50, 0.70)
        self.colors = [color for color in COLORS.values()]

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(
                2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
            bg_color=self.bg_color)

        # Cancel Button
        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(34, self._height - 48),
            size=(50, 50),
            scale=0.7,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)
        
        # Refresh Button
        self._refresh_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.7, self._height * 0.05),
            size=(150, 50),
            scale=0.7,
            label='Refresh',
            color=self.bg_color,
            on_activate_call=CallStrict(self._on_refresh_press),
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.2)
        
        # Help Button
        self._info_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.15, self._height * 0.05),
            size=(125, 50),
            scale=0.7,
            label='Help',
            color=self.bg_color,
            on_activate_call=self._on_info_press,
            autoselect=False,
            icon=bui.gettexture('star'),
            iconscale=1.2)
            
        # Reset Button
        self._reset_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.8, self._height * 0.875),
            size=(125, 50),
            scale=0.7,
            label="Reset",
            color=self.bg_color,
            on_activate_call= CallStrict(self._on_reset_press),
            autoselect=False,
            icon=bui.gettexture('graphicsIcon'),
            iconscale=1.2)
            
        # Internal Error Log Button
        self._reset_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width / 2.35, self._height * 0.05),
            size=(125, 50),
            scale=0.7,
            label="ErrLog",
            color=self.bg_color,
            on_activate_call=self._on_err_log_button_press,
            autoselect=False,
            icon=bui.gettexture('textClearButton'),
            iconscale=1.2)

        bui.containerwidget(edit=self.root_widget,
                           cancel_button=self._cancel_button)

        # Title
        bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.49, self._height - 27 - 5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.0,
            text=get_lang_text('rswTitle'),
            maxwidth=self._width * 0.6,
            color=bui.app.ui_v1.title_color)

        # Scrollable Container
        scroll_size = (self._width - 40, self._height - 120)
        self._scroll_widget = bui.scrollwidget(
            parent=self.root_widget,
            size=scroll_size,
            position=(20, 62.5))

        self._column = bui.columnwidget(parent=self._scroll_widget)

        # Dynamic checkboxes based on config_defaults
        self._checkboxes = {}
        self._populate_checkboxes()

    def _populate_checkboxes(self):
        """Populate checkboxes dynamically based on config_defaults"""
        v = 0  # Vertical position increment
        load_responder_config()

        display_name = get_responder_config_translate_text()
        for config_key, display_value in default_responder_config.items():
            self._add_checkbox(config_key, display_name[config_key], v=v)
            v -= 20  # Decrement vertical position for the next checkbox

    def _add_checkbox(self, config_key: str, display_name: str, v: float) -> None:
        """Add a checkbox for a specific setting"""
        self._checkboxes[config_key] = bui.checkboxwidget(
            parent=self._column,
            size=(self._width * 0.95, 50),
            autoselect=True,
            maxwidth=self._width * 0.925,
            scale=0.9,
            textcolor=(0.8, 0.8, 0.8),
            value=responder_config.get(config_key),
            text=display_name,
            on_value_change_call=CallPartial(self._set_config, config_key, display_name),
        )

    def _colorful_new_setting(self):
        bui.checkboxwidget(
            edit=self._checkboxes[config_name_screenmessage_cmd],
            textcolor=random.choice(self.colors)
        )
    
    def _set_config(self, config_key: str, display_name: str, value: bool) -> None:
        """Update the setting when a checkbox is toggled"""
        global responder_config
        update_party_config(config_key, value)

        # Optionally, apply specific settings immediately (if needed)
        self._apply_setting(display_name, value)
        responder_config[config_key] = value
        # Apply and save the new configuration globally
          # Save using the global save function

    def _apply_setting(self, display_name: str, value: bool) -> None:
        """Apply a specific setting immediately without recalling LessAutoResponder"""
        screenmessage(f'{display_name}: {get_lang_text("enabled") if value else get_lang_text("disabled")}', color=COLOR_SCREENCMD_NORMAL)

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _on_info_press(self) -> None:
        try:
            ListPopup(info_msgs, "Help")
        except Exception as e:
            screenmessage(f'Failed Opening Help Window', color=COLOR_SCREENCMD_ERROR)
            screenmessage(f'{e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
            print_internal_exception(e)

    def _on_refresh_press(self) -> None:
        try:
            if self._is_refreshing:
                screenmessage(f'Whoa, Slowdown Pal {get_random_happy_emoji()}', color=COLOR_SCREENCMD_NORMAL)
                return
            self._is_refreshing = True
            babase.apptimer(3, Call(self._reset_refresh))
            self._column.delete()
            self._column = bui.columnwidget(parent=self._scroll_widget)
            self._checkboxes = {}
            screenmessage('Configs Reloaded', color=COLOR_SCREENCMD_NORMAL)
            self._populate_checkboxes()
        except Exception as e:
            screenmessage(f'Failed Refreshing Configs', color=COLOR_SCREENCMD_ERROR)
            screenmessage(f'{e}', color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))
            print_internal_exception(e)
        """
        bui.app.ui_v1.clear_main_menu_window()
        bs.new_host_session(MainMenuSession)
        ResponderSettingsWindow()
        """

    def _reset_refresh(self):
        self._is_refreshing = False

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            save_responder_config(responder_config)
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def _on_err_log_button_press(self):
        data = _load_internal_exception()
        if data: ErrorPopup()
        else: screenmessage(f"You Got No Internal Errors Log", color=COLOR_SCREENCMD_NORMAL)

    def _on_reset_press(self):
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=u'Are You Sure You Want To Reset\nResponder Settings?',
            action=self._do_reset,
            cancel_is_selected=True,
            text_scale=1,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel'))

    def _do_reset(self):
        radius = 5
        try:
            ### Files ###
            os.remove(config_party_file_path)
            os.remove(config_responder_file_path)
            if saved_player_data_is_error:
                for file_name in os.listdir(all_players_data_folder_path):
                    file_path = os.path.join(all_players_data_folder_path, file_name)
                    os.remove(file_path)
            os.remove(nickname_file_path)
            os.remove(kunci_jawaban_file_path)
            os.remove(custom_reply_file_path)
            os.remove(exception_for_player_names_file_path)
            os.remove(warning_file_path)
            os.remove(blacklist_file_path)
            os.remove(exception_for_anti_abuse_file_path)
            os.remove(internal_chats_data_file_path)
            os.remove(internal_all_chats_data_file_path)
            os.remove(muted_players_file_path)
            ### Dirs ###
            os.remove(abuse_file_paths[id_lang])
            os.remove(abuse_file_paths[en_lang])
            os.remove(abuse_file_paths[hi_lang])

            for file_name in os.listdir(players_server_data_folder_path):
                if file_name.startswith("profiles") and file_name.endswith(".json"):
                    file_path = os.path.join(players_server_data_folder_path, file_name)
                    os.remove(file_path)

            #### Load Main Config ####
            babase.AppTimer(0, Call(load_responder_config))
            babase.AppTimer(1/radius, Call(_load_nicknames))
            babase.AppTimer(2/radius, Call(_load_saved_kunci_jawaban))
            babase.AppTimer(3/radius, Call(_load_saved_custom_replies))

            #### Load Players Data ####
            babase.AppTimer(4/radius, Call(load_all_names_data))
            babase.AppTimer(5/radius, Call(load_responder_blacklist_names))
            babase.AppTimer(6/radius, Call(load_player_name_exceptions))
            babase.AppTimer(7/radius, Call(load_player_warnings))
            babase.AppTimer(8/radius, Call(load_muted_players))

            #### Load Abuses ####
            babase.AppTimer(9/radius, Call(load_abuses, id_lang))
            babase.AppTimer(10/radius, Call(load_abuses, en_lang))
            babase.AppTimer(11/radius, Call(load_abuses, hi_lang))
            babase.AppTimer(12/radius, Call(load_anti_abuse_exception_words))

            #### Server Players Data ####
            babase.AppTimer(13/radius, Call(load_players_server_data))
            babase.AppTimer(14/radius, Call(load_internal_chats_data))
            babase.AppTimer(15/radius, Call(load_internal_all_chats_data))

        except Exception as e:
            screenmessage(f"{CMD_LOGO_CAUTION} Error On Reset: {e}", color=COLOR_SCREENCMD_ERROR)
            chatmessage(f"{CMD_LOGO_CAUTION} Error On Reset: {e}")
            print_internal_exception(e)

        babase.AppTimer(16/radius, self._transition_out)

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()

class CreditPopup(popup.PopupWindow):
    def __init__(self):
        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        self._is_refreshing = False
        self._width = 1100
        self._height = 600
        self.bg_color = (0.5, 0.25, 0.6)
        self.colors = [color for color in COLORS.values()]

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(
                2.2 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
            bg_color=self.bg_color)

        # Main label
        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 35),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.8,
            color=bui.app.ui_v1.title_color,
            text=get_lang_text('credit&help')
        )


        # Cancel button
        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(5, self._height - 70),
            size=(55, 55),
            scale=1.1,
            label='',
            color=self.bg_color,
            on_activate_call=self.on_popup_cancel,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        ### SCROLLER ###
        self.scrollwidget_width = self._width*0.475
        self.scrollwidget_x_tilt = self._width*0.485
        self.scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            position=(self.scrollwidget_x_tilt, self._height * 0.075),
            size=(self.scrollwidget_width, self._height * 0.825),
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2), # Scroller color
            highlight=False
        )
        self.data_container = bui.columnwidget(
            parent=self.scrollwidget,
            border=2,
            margin=0
        )
        ### SCROLLER ###

        self._ascii = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.05, self._height - 100),
            maxwidth=self.scrollwidget_x_tilt*0.885,
            size=(0, 0),
            h_align='left',
            v_align='center',
            scale=1.8,
            color=COLORS.get('pink', COLOR_SCREENCMD_NORMAL),
            text='Unavailable Yet :\'('
        )

    def ascii(self):
        ascii_one: list[str] = [

        ]
        ascii_two: list[str] = [

        ]


    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()

def _edit_text_field_global(text: str, action='add', auto_space: bool = True, widget: Optional[bui.Widget] = None):
    """Whether `Add` or `Replace` Text Field From The Text Given"""
    action = action.lower()
    curr_widget = _text_field if not widget else widget
    if isinstance(text, str) and curr_widget:
        if action.startswith('rep'):
            bui.textwidget(edit=curr_widget, text=text)

        elif action.startswith('add'):
            current_text: str = bui.textwidget(query=curr_widget)
            end_synbols = [
                ' ',
                '(', '[', '{',
                '\'', '\"', '`',
                '/', '\\', '|'
            ]
            if auto_space and current_text and current_text[-1] not in end_synbols:
                current_text += ' ' # Automatically add Space :)
            bui.textwidget(edit=curr_widget, text=(current_text + text))

class PlayerInfoPopup(popup.PopupWindow):
    """Show Player Info Window Using Their Name, Including Their Chats(If Available)"""
    def __init__(self, real_name: str):
        self.chats = internal_player_chats_data.get(real_name, [])
        self.chats_per_page = maximum_bombsquad_chat_messages # Use the default maximum party window chats each pages
        self.current_page = (len(self.chats) - 1) // self.chats_per_page # Automatically show the last page
        global all_names
        self.player_data = all_names
        self.real_name = real_name
        self.total_pages = (len(self.chats) - 1) // self.chats_per_page + 1  # Calculate the total pages

        # Window dimensions based on whether chats are available
        if self.chats:
            self._width = 950
            self._height = 625
            self._start_gap = 425
            self._info_text_scale = 1.0
            self._spacing = 32.5
        else:
            self._width = 750
            self._height = 320
            self._start_gap = 75
            self._info_text_scale = 1.0
            self._spacing = 35

        self.bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self._transitioning_out = False
        uiscale = bui.app.ui_v1.uiscale

        self._popup_type = ''
        self._pressed_textwidget_text = ''
        self._pressed_textwidget: bui.Widget = ''
        self._popup_party_member_client_id = 0
        self.uiscale : babase.UIScale = uiscale

        # Set up the popup window
        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0),
            bg_color=self.bg_color
        )

        # Main label
        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.6,
            color=bui.app.ui_v1.title_color,
            text=get_lang_text('playerInfo')
        )

        # Cancel button
        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(55, self._height - 63),
            size=(55, 55),
            scale=.875,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        self._send_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.850, self._height * 0.025),
            size=(40, 40),
            label='',
            scale=1,
            on_activate_call=CallStrict(self.on_send_click, real_name, self.player_data[real_name].get('profile_name', None), self.player_data[real_name].get('client_id', '?'), self.player_data[real_name].get('pb_id', None)),
            color=self.bg_color,
            autoselect=False,
            icon=bui.gettexture('rightButton'),
            icon_color=self.bg_color,
            iconscale=1.2)

        # Search Player Data from BCS Database Manually
        self._search_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.775, self._height * 0.025),
            size=(40, 40),
            label='',
            scale=1,
            on_activate_call=self._on_search_button_press,
            color=self.bg_color,
            autoselect=False,
            icon=bui.gettexture('backIcon'),
            icon_color=self.bg_color,
            iconscale=1.2
        )

        # View Account Info Button
        # Let's determine the logic for on_activate_call and icon..
        self._view_account_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.7, self._height * 0.025),
            size=(40, 40),
            label='',
            scale=1,
            on_activate_call=self._on_view_account_button_press if all_names[self.real_name].get('pb_id') else self._on_search_button_press,
            color=self.bg_color,
            autoselect=False,
            icon=bui.gettexture('ouyaUButton') if all_names[self.real_name].get('_id') else bui.gettexture('ouyaYButton') if all_names[self.real_name].get('pb_id') else bui.gettexture('ouyaAButton'),
            iconscale=1.2
        )

        if all_names[self.real_name].get('mutual_server'):
            if not isinstance(all_names[self.real_name]['mutual_server'], list):
                all_names[self.real_name]['mutual_server'] = [all_names[self.real_name]['mutual_server']]
                _save_names_to_file()

            self._mutual_server_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.625, self._height * 0.025),
                size=(40, 40),
                label='',
                scale=1,
                on_activate_call=CallStrict(ListPopup, all_names[self.real_name]['mutual_server'], "Mutual Servers"),
                color=self.bg_color,
                autoselect=False,
                icon=bui.gettexture('achievementFreeLoader'),
                iconscale=1.2
            )

        self._other_option_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(((self._width * 0.625) if not all_names[self.real_name].get('mutual_server') else (self._width * 0.550)), self._height * 0.025),
            size=(40, 40),
            label='',
            scale=1,
            on_activate_call=CallStrict(self._on_other_option_pressed),
            color=self.bg_color,
            autoselect=False,
            icon=bui.gettexture('settingsIcon'),
            iconscale=1.2
        )

        self._prioritize_bcs_pb_checkbox = bui.checkboxwidget(
            parent=self.root_widget,
            position=(self._width * 0.135, self._height - 75) if self.chats else (self._width * 0.125, self._height * 0.025),
            size=(200, 30),
            text=get_lang_text('bcsPbPriority'),
            value=responder_config.get(config_name_prioritize_bcs_pb, default_responder_config.get(config_name_prioritize_bcs_pb, False)),
            on_value_change_call=lambda v: self._set_config(config_name_prioritize_bcs_pb, v)
        )

        # Player chat list and navigation buttons
        if self.chats:
            if len(self.chats) > self.chats_per_page:
                self._page_text = bui.textwidget(
                    parent=self.root_widget,
                    position=(self._width * 0.85, self._height - 62.5),
                    size=(0, 0),
                    h_align='center',
                    v_align='center',
                    text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}",
                    color=bui.app.ui_v1.title_color
                )
            self._setup_chat_scroll(focous_to_last=True)

        # Create info text widgets for player attributes
        self._create_info_text(
            label=("Name:" if self.player_data[real_name].get('client_id', 'N/A') != -1 else "Server Name:"),
            text=real_name,
            position=(self._width * 0.125, self._height - self._start_gap - self._spacing),
            maxwidth=self._width * 0.6
        )
        self._create_info_text(
            label=("Profile:" if self.player_data[real_name].get('client_id', 'N/A') != -1 else "Server Version:"),
            text=', '.join(self.player_data[real_name].get('profile_name', [])) if self.player_data[real_name].get('profile_name') else "N/A",
            position=(self._width * 0.125, self._height - self._start_gap - self._spacing*2),
            maxwidth=self._width * 0.85
        )
        self._create_info_text(
            label="Client ID:",
            text=str(self.player_data[real_name].get('client_id', 'N/A')),
            position=(self._width * 0.125, self._height - self._start_gap - self._spacing*3),
            maxwidth=self._width * 0.6
        )
        self._create_info_text(
            label="PB-ID:",
            text=str(self.player_data[real_name].get('pb_id', 'N/A')),
            position=(self._width * 0.125, self._height - self._start_gap - self._spacing*4),
            maxwidth=self._width * 0.85
        )
        self._create_info_text(
            label="Last Met:",
            text=self.player_data[real_name].get('last_met', 'N/A'),
            position=(self._width * 0.125, self._height - self._start_gap - self._spacing*5),
            maxwidth=self._width * 0.40
        )

    def _set_config(self, config_key: str, value: bool) -> None:
        """Update the setting when a checkbox is toggled"""
        global responder_config
        update_responder_config(config_key, value)
        #screenmessage(f'{display_name}: {"Enabled" if value else "Disabled"}', color=COLOR_SCREENCMD_NORMAL)
        # Apply and save the new configuration globally
        responder_config[config_key] = value

    def _on_search_button_press(self):
        is_searched = all_names[self.real_name].get('searched_bcs')
        p_pb = all_names[self.real_name].get('pb_id')
        if is_searched is None: # Means The Status Of Player's Searched Data From BCS is: Unknown
            if not p_pb:
                text_str = f"{get_lang_text('bcsOnSearchTryEmpty').format(self.real_name)}"
            else:
                text_str = f"{get_lang_text('bcsOnSearchTryOnlyPb').format(self.real_name)}"
        elif is_searched is False: # Means The Status Of Player's Searched Data From BCS is: Already Searched And No Data Found
            if not p_pb:
                text_str = f"{get_lang_text('bcsOnSearchTryNoPbNoBcs').format(self.real_name)}"
            else:
                text_str = f"{get_lang_text('bcsOnSearchTryNoBcs').format(pb_id=p_pb, name=self.real_name)}?"
        elif is_searched is True: # Means The Status Of Player's Searched Data From BCS is: Already Searched And The Data Obtained
            text_str = f"{get_lang_text('bcsOnSearchTryFull').format(pb_id=p_pb, name=self.real_name)}?"
        else:
            text_str = f"{get_lang_text('bcsOnSearchTryUnknown').format(name=self.real_name, pb_id=p_pb, other=str(is_searched))}"

        ConfirmWindow(
            origin_widget=self.root_widget,
            text=text_str,
            width=550,
            height=150,
            action=Call(self._get_pb_online),
            cancel_is_selected=True,
            text_scale=1,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel'))

    def _on_view_account_button_press(self):
        CustomAccountViewerWindow(self.real_name, self.player_data[self.real_name], self.player_data[self.real_name].get('pb_id', None))

    def _setup_chat_scroll(self, focous_to_last: bool=False):
        self.scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            size=(self._width, self._height - 275),
            position=(10, 200),
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2),
            highlight=False
        )
        self.chat_container = bui.columnwidget(
            parent=self.scrollwidget,
            border=2,
            margin=0
        )
        self._show_page(self.current_page, focous_to_last)  # Populate the first page of chats

        # Navigation buttons for paginated chat list
        if len(self.chats) > self.chats_per_page:
            self._prev_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.75, self._height - self._start_gap - self._spacing - 10),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._previous_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )
            self._next_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.875, self._height - self._start_gap - self._spacing - 10),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._next_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )

    def _show_page(self, page: int, focous_to_last: bool=False):
        """Populate the text container with the current page of texts"""
        self.chat_container.delete()

        self.scrollwidget.delete()
        self.scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            size=(self._width, self._height - 275),
            position=(10, 200),
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2),
            highlight=False)

        self.chat_container = bui.columnwidget(parent=self.scrollwidget,border=2,margin=0)

        start_index = page * self.chats_per_page
        end_index = start_index + self.chats_per_page
        widget = None
        for chat in self.chats[start_index:end_index]:
            widget = bui.textwidget(
                parent=self.chat_container,
                size=(self._width, 20),
                text=chat,
                maxwidth=self._width * 0.96,
                scale=1,
                h_align='left',
                v_align='center',
                autoselect=False,
                selectable=True,
                click_activate=True,
                always_highlight=True,
                color=(0.8, 0.8, 0.8)
            )
            bui.textwidget(edit=widget, on_activate_call=CallStrict(self._on_textwidget_pressed, chat, widget))
        if len(self.chats) > self.chats_per_page:
            bui.textwidget(edit=self._page_text, text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}")

    def _on_textwidget_pressed(self, text: str, widget: bui.Widget):
        self._popup_type = POPUP_MENU_TYPE_CHAT_PRESS
        self._pressed_textwidget_text = text # Make sure its pname and the msg not splitted yet
        self._pressed_textwidget = widget
        choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_CHAT_PRESS)

        #Using current session may cause less accurate current player
        #chosen_player_data = current_namelist if current_namelist else all_names

        # Show on party member press
        """player_acc = self.real_name
        if current_session_namelist.get(player_acc):
            choices_key.append('playerMenuOptionFromText')
            choices_display.append(get_lang_text('playerMenuOptionFromText'))
            self._popup_party_member_client_id = chosen_player_data.get(player_acc, {}).get('client_id')
        else:
            pass""" # On a second thought, you dont need it :moyai:

        self._popup_type = POPUP_MENU_TYPE_CHAT_PRESS
        pos: tuple[float, float] = widget.get_screen_space_center()
        pos = (pos[0]*25, pos[1])
        PopupMenuWindow(
            position=pos,
            color=self.bg_color, # type: ignore
            scale= _get_popup_window_scale(),
            choices=choices_key,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices_key[0],
            delegate=self)

    def _on_other_option_pressed(self):
        choices_key: List[str] = []
        choices_display: List[str] = []
        global players_anti_abuse_exception, player_blacklisted_list

        choice = 'playerOptionRemoveData'
        choices_key.append(choice)
        choices_display.append(get_lang_text(choice).format(self.real_name))

        if self.real_name in players_anti_abuse_exception:
            choice = 'playerOptionRemoveFriend'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))
        else:
            choice = 'playerOptionAddFriend'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))

        if self.real_name in player_blacklisted_list:
            choice = 'playerOptionRemoveBlacklist'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))
        else:
            choice = 'playerOptionAddBlacklist'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))

        if self.real_name in player_muted_list:
            choice = 'playerOptionRemoveMuted'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))
        else:
            choice = 'playerOptionAddMuted'
            choices_key.append(choice)
            choices_display.append(get_lang_text(choice))

        player_warning: int = player_warnings.get(self.real_name, 0)
        choice = 'warnInfo'
        choices_key.append(choice)
        choices_display.append(get_lang_text(choice).format(player_warning))

        self._popup_type = POPUP_MENU_TYPE_PLAYER_OPTION
        PopupMenuWindow(
            position=self._other_option_button.get_screen_space_center(),
            color=self.bg_color, # type: ignore
            scale=_get_popup_window_scale(),
            choices=choices_key,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices_key[-1],
            delegate=self)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        if self._popup_type == POPUP_MENU_TYPE_CHAT_PRESS:
            pname, current_text = '', ''
            if self._pressed_textwidget_text:
                pname, current_text = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                if ' ' in pname:
                    pname = pname.split(' ', 1)[0].strip()
            current_textwidget_text = self._pressed_textwidget_text
            current_textwidget: bui.Widget = self._pressed_textwidget
     #       current_text = self._pressed_textwidget_text
            if self._pressed_textwidget_text:
                player_data = all_names
                player_acc: str = self.real_name
                player_profiles: list[str] = player_data.get(player_acc, {}).get('profile_name', [])
                player_client_id: int = player_data.get(player_acc, {}).get('client_id', 0)
                self._popup_party_member_client_id = player_client_id
            else:
                player_acc = ''
                player_profiles = []

            if choice == 'copyText':
                _copy_to_clipboard(current_textwidget_text)

            elif choice == 'translateText':
                if not current_textwidget_text: return
                self._translate_textwidget(current_text, current_textwidget)

            elif choice == 'insertText':
                if current_textwidget_text:
                    msg = (
                        current_text if not party_config.get(CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT) or pname.strip() == '...' else
                        str('/'.join(player_profiles) if player_profiles else pname) + PNAME_AND_MSG_SPLITTER + current_text
                    )
                    _edit_text_field_global(msg, 'add')

        elif self._popup_type == POPUP_MENU_TYPE_PLAYER_OPTION:
            if choice == 'playerOptionRemoveFriend':
                if self.real_name in players_anti_abuse_exception:
                    if self.real_name not in MY_MASTER:
                        players_anti_abuse_exception.remove(self.real_name)
                        screenmessage(message=(get_lang_text('playerOptionRemoveFriendSuccess') + f' {get_random_sad_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                        bui.getsound('shieldDown').play()
                        save_player_name_exceptions(players_anti_abuse_exception)
                    else:
                        screenmessage(message=(get_lang_text('playerOptionRemoveFriendInMasterList') + f' {get_random_sad_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                        bui.getsound('error').play(1.5)
                else:
                    screenmessage(message=(get_lang_text('playerOptionRemoveFriendNotExist')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'playerOptionAddFriend':
                if self.real_name not in players_anti_abuse_exception:
                    players_anti_abuse_exception.append(self.real_name)
                    screenmessage(message=(get_lang_text('playerOptionAddFriendSuccess') + f' {get_random_happy_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('gunCocking').play()
                    save_player_name_exceptions(players_anti_abuse_exception)
                else:
                    screenmessage(message=(get_lang_text('playerOptionAddFriendAlreadyExists')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'playerOptionRemoveBlacklist':
                if self.real_name in player_blacklisted_list:
                    player_blacklisted_list.remove(self.real_name)
                    screenmessage(message=(get_lang_text('playerOptionRemoveBlacklistSuccess') + f' {get_random_happy_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('shieldDown').play()
                    save_blacklist_names(player_blacklisted_list)
                else:
                    screenmessage(message=(get_lang_text('playerOptionRemoveBlacklistNotExist')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'playerOptionAddBlacklist':
                if self.real_name not in player_blacklisted_list and self.real_name not in MY_MASTER:
                    player_blacklisted_list.append(self.real_name)
                    screenmessage(message=(get_lang_text('playerOptionAddBlacklistSuccess') + f' {get_random_sad_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('gunCocking').play()
                    save_blacklist_names(player_blacklisted_list)
                elif self.real_name in MY_MASTER:
                    screenmessage(message=(get_lang_text('playerOptionAddBlacklistInMasterList') + f' {get_random_unamused_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)
                else:
                    screenmessage(message=(get_lang_text('playerOptionAddBlacklistAlreadyExists')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'playerOptionRemoveMuted':
                if self.real_name in player_muted_list:
                    player_muted_list.remove(self.real_name)
                    screenmessage(message=(get_lang_text('playerOptionRemoveMutedSuccess') + f' {get_random_happy_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('shieldDown').play()
                    save_muted_players(player_muted_list)
                else:
                    screenmessage(message=(get_lang_text('playerOptionRemoveMutedNotExist')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'playerOptionAddMuted':
                if self.real_name not in player_muted_list and self.real_name not in MY_MASTER:
                    player_muted_list.append(self.real_name)
                    screenmessage(message=(get_lang_text('playerOptionAddMutedSuccess') + f' {get_random_sad_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('gunCocking').play()
                    save_muted_players(player_muted_list)
                elif self.real_name in MY_MASTER:
                    screenmessage(message=(get_lang_text('playerOptionAddMutedInMasterList') + f' {get_random_unamused_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)
                else:
                    screenmessage(message=(get_lang_text('playerOptionAddMutedAlreadyExists')), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)

            elif choice == 'warnInfo':
                self._popup_type = POPUP_MENU_TYPE_WARN_SELECT
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_WARN_SELECT)
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices_key[0],
                    delegate=self)

            elif choice == 'playerOptionRemoveData':
                if self.real_name in all_names and self.real_name not in MY_MASTER:
                    text = get_lang_text('playerOptionRemoveDataConfirm').format(self.real_name)
                    ConfirmWindow(
                        origin_widget=self.root_widget,
                        text= f"{text}?",
                        width=(len(text) * 13.5),
                        height=125,
                        action=self._delete_this_player_data,
                        cancel_is_selected=True,
                        cancel_text=get_lang_text('cancel'),
                        text_scale=1,
                        ok_text=get_lang_text('yes')
                    )

                elif self.real_name in MY_MASTER:
                    screenmessage(message=(get_lang_text('playerOptionRemoveDataInMasterList') + f' {get_random_unamused_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
                    bui.getsound('error').play(1.5)
                else:
                    screenmessage(message=(get_lang_text('playerOptionRemoveDataNotExist').format(self.real_name)), color=COLOR_SCREENCMD_ERROR)
                    bui.getsound('error').play(1.5)

        elif self._popup_type == POPUP_MENU_TYPE_WARN_SELECT:
            if choice == 'partyPressWarnAdd':
                manual_add_warn(player_name=self.real_name, manual=True)

            elif choice == 'partyPressWarnDecrease':
                manual_decrease_warn(player_name=self.real_name, is_master=True)

        del popup_window

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _delete_this_player_data(self):
        try:
            del all_names[self.real_name]
            screenmessage(message=(get_lang_text('playerOptionRemoveData').format(self.real_name) + f' {get_random_sad_emoji()}'), color=COLOR_SCREENCMD_NORMAL)
            bui.getsound('shieldDown').play()
            start_save_all_names(force=True).start()
            self._transition_out()
        except Exception as e:
            print_internal_exception(e)

        try:
            # Also remove from internal_chats if present
            if self.real_name in internal_player_chats_data:
                del internal_player_chats_data[self.real_name]
                save_internal_player_chats_data()
        except Exception as e:
            print_internal_exception(e)


    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return (1.6 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else
                2.0)

    def _translate_textwidget(self, text_widget_text: str, text_widget: bui.Widget):
        """Translate the Pressed textwidget"""
        msg: str = bui.textwidget(query=text_widget)
        cleaned_msg = ''.join(filter(str.isalpha, text_widget_text))

        if not msg or not cleaned_msg or msg == '':
            screenmessage(f'{CMD_LOGO_CAUTION} ' + get_lang_text('translateEmptyText'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('translating'), COLOR_SCREENCMD_NORMAL)
            name = ''
            if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                name, text = msg.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
            else:
                text = msg

            def _apply_translation(translated: str):
                if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                    translate_text = name + PNAME_AND_MSG_SPLITTER_MODIFIED + translated
                else:
                    translate_text = translated
                if text_widget.exists():
                    bui.textwidget(edit=text_widget, text=translate_text)
            Translate(text=text, callback=_apply_translation)

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._show_page(self.current_page)
        else:
            self.current_page = 0
            self._show_page(self.current_page)

    def _previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
        else:
            self.current_page = (len(self.chats) - 1) // self.chats_per_page
            self._show_page(self.current_page)

    def _create_info_text(self, label: str, text: str, position: tuple, maxwidth: float):
        """Creates a pressable text widget for player attributes"""
        full_text = f"{label} {text}"
        if label != "PB-ID:":
            bui.textwidget(
                parent=self.root_widget,
                position=position,
                size=(maxwidth, 20),
                maxwidth=self._width * 0.9,
                scale=self._info_text_scale,
                h_align='left',
                v_align='center',
                text=full_text,
                selectable=True,
                autoselect=False,
                click_activate=True,
                on_activate_call=CallStrict(self._confirm_copy, text),
                color=bui.app.ui_v1.title_color)
        else:
            self._pb_text_widget = bui.textwidget(
                parent=self.root_widget,
                position=position,
                size=(maxwidth, 20),
                maxwidth=self._width * 0.9,
                scale=self._info_text_scale,
                h_align='left',
                v_align='center',
                text=full_text,
                selectable=True,
                autoselect=False,
                click_activate=True,
                on_activate_call=CallStrict(self._confirm_copy, text, True),
                color=bui.app.ui_v1.title_color)

    def _confirm_copy_chat(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 10
        else:
            width = len(text) * 10
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}\n{text_title}",
            width= width,
            height=135,
            action=Call(_copy_to_clipboard, text),
            cancel_is_selected=True,
            text_scale=1,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel')
        )

    def _confirm_copy(self, text: str, is_pb: bool=False):
        """Opens a confirm window to copy the selected text"""
        if not is_pb:
            if text != "N/A":
                ConfirmWindow(
                    origin_widget=self.root_widget,
                    text=f"{get_lang_text('confirmCopy')}\n{text}",
                    width=max(200, len(text) * 10),
                    height=125,
                    action=CallStrict(_copy_to_clipboard, text),
                    cancel_is_selected=True,
                    text_scale=1,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('copy'))
            else:
                screenmessage(f"{text}", color=(.7, .35, .5))
        else:
            if text == "N/A":
                if self.player_data[self.real_name].get('client_id') == -1:
                    screenmessage(text, COLOR_SCREENCMD_NORMAL)
                    return
                is_searched = all_names[self.real_name].get('searched_bcs')
                p_pb = all_names[self.real_name].get('pb_id')
                if is_searched is None: # Means The Status Of Player's Searched Data From BCS is: Unknown
                    if not p_pb:
                        text_str = f"{get_lang_text('bcsOnSearchTryEmpty').format(self.real_name)}"
                    else:
                        text_str = f"{get_lang_text('bcsOnSearchTryOnlyPb').format(self.real_name)}"
                elif is_searched is False: # Means The Status Of Player's Searched Data From BCS is: Already Searched And No Data Found
                    if not p_pb:
                        text_str = f"{get_lang_text('bcsOnSearchTryNoPbNoBcs').format(self.real_name)}"
                    else:
                        text_str = f"{get_lang_text('bcsOnSearchTryNoBcs').format(pb_id=p_pb, name=self.real_name)}?"
                elif is_searched is True: # Means The Status Of Player's Searched Data From BCS is: Already Searched And The Data Obtained
                    text_str = f"{get_lang_text('bcsOnSearchTryFull').format(pb_id=p_pb, name=self.real_name)}?"
                else:
                    text_str = f"{get_lang_text('bcsOnSearchTryUnknown').format(self.real_name, p_pb, str(is_searched))}"

                ConfirmWindow(
                    origin_widget=self.root_widget,
                    text=text_str,
                    width=550,
                    height=150,
                    action=CallStrict(self._get_pb_online),
                    cancel_is_selected=True,
                    text_scale=1,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('get'))
            else:
                ConfirmWindow(
                    origin_widget=self.root_widget,
                    text=f"{get_lang_text('confirmCopy')}\n{text}",
                    width=min(len(text) * 13.5, 600),
                    height=125,
                    action=Call(_copy_to_clipboard, text),
                    cancel_is_selected=True,
                    text_scale=1,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('copy'))

    def _get_pb_online(self):
        screenmessage(f"{get_lang_text('bcsGettingPlayerData').format(self.real_name)}...", color=COLOR_SCREENCMD_NORMAL)
        Thread(target=fetch_data, args=(self.real_name, self)).start()

    def on_send_click(self, real_name, full_name, client_id, pb_id):
        display_name = f"[{client_id}] {real_name} | {(', '. join(full_name))}" if full_name else f"[{client_id}] {real_name} [In Lobby]"
        display_name_pb = display_name + (f'\n{pb_id}' if pb_id else '')
        babase.clipboard_set_text(display_name_pb)
        chatmessage(display_name)
        if pb_id:
            chatmessage(f'[{real_name}] PB-ID: {pb_id}')
        screenmessage(display_name + (f' | {pb_id}' if pb_id else ''), color=(.7, .35, .5))

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            bui.containerwidget(edit=self.root_widget, transition='out_scale')
            self._transitioning_out = True
            save_responder_config(responder_config)
            bui.getsound('swish').play()

    def on_popup_cancel(self) -> None:
        self._transition_out()

class ErrorPopup(popup.PopupWindow):
    """Popup Window For Displaying Errors"""
    def __init__(self):
        self.error_data = _load_internal_exception()  # Load error data from JSON
        self.current_page = (len(self.error_data) - 1)  # Track the current page
        self.total_pages = len(self.error_data)  # Total number of errors

        self._width = 1000
        self._height = 550
        self.bg_color: tuple[float, float, float] = (0.05, 0.05, 0.2) # party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self.error_message = ""
        self._transitioning_out = False
        uiscale = bui.app.ui_v1.uiscale

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0),
            bg_color=self.bg_color
        )

        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.5,
            color=bui.app.ui_v1.title_color,
            text=get_lang_text('errorPopupTitle')
        )

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(55, self._height - 63),
            size=(55, 55),
            scale=.875,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        if self.total_pages > 1:
            # Navigation buttons
            self._prev_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.650, self._height * 0.05),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._previous_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )

            self._next_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.775, self._height * 0.05),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._next_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )
        
        if self.total_pages > 0:
            self._copy_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.9, self._height * 0.05),
                size=(40, 40),
                scale=1,
                label="",
                on_activate_call=self._confirm_copy_error,
                autoselect=False,
                enable_sound=False,
                color=self.bg_color,
                icon=bui.gettexture('levelIcon'),
                iconscale=1.2
            )

        # Error Text
        self._error_text = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.025, self._height * 0.075),
            size=(self._width * 0.95, self._height * 0.95),
            maxwidth= self._width * 0.95,
            max_height= self._height * 0.95,
            h_align='left',
            v_align='center',
            scale=1.0,
            color=(0.8, 0.8, 0.8),
            text=""
        )

        self._page_text = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.8, self._height - 70),
            scale=1,
            h_align='center',
            v_align='center',
            text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}",
            color=COLOR_SCREENCMD_ERROR
        )

        # Scroller
        self.scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            size=(self._width * 0.95, self._height * 0.725),
            position=(self._width * 0.025, self._height * 0.135),
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2), # Scroller Color
            highlight=False
        )
        self.error_container = bui.columnwidget(
            parent=self.scrollwidget,
            border=2,
            margin=0
        )

        self._show_page(self.current_page)  # Show the first error

    def _confirm_copy_error(self):
        text = f"{get_lang_text('errorPopupConfirmCopyError')}?"
        ConfirmWindow(
            origin_widget=self.root_widget,
            text= text,
            width=(len(text) * 13.5),
            height=125,
            action=CallStrict(self._copy_error),
            cancel_is_selected=True,
            cancel_text=get_lang_text('cancel'),
            text_scale=1,
            ok_text=get_lang_text('copy')
        )

    def _copy_error(self):
        babase.clipboard_set_text(self.error_message)
        screenmessage(f'{get_lang_text("errorPopupErrorCopied")}', color=COLOR_SCREENCMD_NORMAL)
        bui.getsound('gunCocking').play()

    def _show_page(self, page: int):
        """Display the error of the current page"""
        # Clear previous error messages
        self.error_container.delete()
        self.error_container = bui.columnwidget(
            parent=self.scrollwidget,
            border=2,
            margin=0
        )

        if self.total_pages > 0:
            # Get the error keys and calculate start/end indices for current page
            error_keys = list(self.error_data.keys())
            errors_per_page = 1  # Show 1 error per page
            start_index = page * errors_per_page
            end_index = min(start_index + errors_per_page, len(error_keys))

            # Display only the error for current page
            for i in range(start_index, end_index):
                error_key = error_keys[i]
                error_entry = self.error_data[error_key]
                
                # Create a list of error messages to display
                error_lines =   f"PRINTED-FROM:\n{error_entry.get('stackstr', 'N/A')}\n" \
                                f"EXCEPTION:\n{error_entry.get('excstr', 'N/A')}\n" \
                                f"\n" \
                                f"ERROR: {error_entry.get('err_str', 'N/A')}"

                self.error_message = error_lines
                # Create a text widget for each line of the error message
                for line in error_lines.splitlines():
                    bui.textwidget(
                        parent=self.error_container,
                        size=(self._width, 20),
                        text=f"{line}",
                        maxwidth=self._width * 0.9225,
                        scale=1,
                        h_align='left',
                        v_align='center',
                        selectable=True if line.strip() else False,
                        autoselect=False,
                        click_activate=True,
                        on_activate_call=CallStrict(self._confirm_copy, line) if line.strip() else None,
                        color=(0.8, 0.8, 0.8)
                    )

            # Update page text
            bui.textwidget(edit=self._page_text, text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}")
        else:
            bui.textwidget(edit=self._error_text, text=get_lang_text('errorPopupNoError'))
    def _confirm_copy(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 13.5
        else:
            width = len(text) * 13.5
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}?\n{text_title}",
            width= width,
            height=135,
            action=Call(_copy_to_clipboard, text),
            cancel_is_selected=True,
            cancel_text=get_lang_text('cancel'),
            text_scale=1,
            ok_text=get_lang_text('copy')
        )

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._show_page(self.current_page)
        else:
            self.current_page = 0
            self._show_page(self.current_page)

    def _previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
        else:
            self.current_page = self.total_pages - 1
            self._show_page(self.current_page)

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()

is_getting_player_data: bool = False
time_out_asked_names_delay = 120 # Seconds
def _automatic_get_player_info_from_bcs():
    """Automatic `Search Players Data` from `BCS` (if haven't). Should be on another `Thread`"""
    global all_names, current_session_namelist, is_getting_player_data
    if not current_session_namelist: return
    global all_names
    if is_getting_player_data:
        #print('Oops, Automatic Get Player Data From BCS Called While Not Done')
        return
    is_getting_player_data = True
    updated = False
    try:
        updated = False
        for i, name in enumerate(list(current_session_namelist.keys())):
            if all_names.get(name, {}).get('searched_bcs') is not None: continue
            if all_names.get(name, {}).get('client_id') == -1: continue # Why
            if name in ["LessPal"]: continue
            if name in MY_MASTER: continue # No
            if name in names_asked_bcs: continue
            babase.pushcall(CallStrict(babase.apptimer, time_out_asked_names_delay, CallStrict(clear_timeout_asked_names, name)), from_other_thread=True)
            data = _get_bcs_player_info(name)
            if data and isinstance(data, dict):
                _bcs_player_info_obtained(account_name=name, account_data=data, no_confirmation=True, print_progress_only=True)
                updated = True
                msg = '\n'
            elif data is False:
                msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchError').format(name)}"
            elif data is None:
                msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchFailedConnect').format(name)}"
            else:
                msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchNotFound').format(name)}"
                try:
                    if all_names.get(name):
                        all_names[name]['searched_bcs'] = False
                    else:
                        all_names[name] = {}
                        all_names[name]['searched_bcs'] = False
                except Exception as e:
                    print_internal_exception(f"Error On Getting Automatic BCS Data")
                updated = True
            print(msg)
        #_save_names_to_file()
    except Exception as e:
        print_internal_exception(e)
    finally:
        is_getting_player_data = False
        if updated:
            Thread(target=_automatic_get_player_info_from_bcs).start()
        is_any_none_searched = any(data.get('searched_bcs') is None for data in current_session_namelist.values())
        if not is_any_none_searched:
            start_save_all_names().start_threaded()
        #else: start_save_all_names().start_threaded()

def clear_timeout_asked_names(name: str):
    global names_asked_bcs, is_getting_player_data
    if name in names_asked_bcs:
        names_asked_bcs.remove(name)
        print(f"Removed timeout name: {name}")
    if not names_asked_bcs and is_getting_player_data:
        is_getting_player_data = False

names_asked_bcs: List[str] = []
def fetch_data(player_name: str, widget=None, no_confirmation: bool = False, print_progress_only: bool = False):
    """First Func To Be Called For Starting Thread To Get Player's Data From BCS, Should be on another `Thread`"""
    global all_names
    all_names_updated = False
    data = _get_bcs_player_info(player_name)
    sad = get_random_unamused_emoji()
    if player_name in names_asked_bcs:
        babase.pushcall(Call(screenmessage, get_lang_text('bcsFetchStillFetching').format(player_name), COLOR_SCREENCMD_ERROR), from_other_thread=True)
        return
    if data and isinstance(data, dict):
        try:
            if widget:
                babase.pushcall(Call(widget._transition_out), from_other_thread=True)
         #   babase.pushcall(Call(PlayerInfoPopup, self.real_name), from_other_thread=True)
            #babase.pushcall(Call(bui.buttonwidget, edit=self._view_account_button, icon=bui.gettexture('ouyaUButton'), on_activate_call=self._on_view_account_button_press), from_other_thread=True)
        except Exception as e: logging.exception(e)
        _bcs_player_info_obtained(player_name, data, no_confirmation, print_progress_only)
        all_names[player_name]['searched_bcs'] = True
        all_names_updated = True
    elif data is False:
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchError').format(player_name)} {sad}"
        if not print_progress_only:
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
    elif data is None:
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchFailedConnect').format(player_name)} {sad}"
        if not print_progress_only:
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
    else:
        msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchNotFound').format(player_name)} {sad}"
        if not print_progress_only:
            babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
        all_names[player_name]['searched_bcs'] = False
        all_names_updated = True
        name = player_name
        if name.startswith(''): name = name.replace('', '')
        else:
            if all_names_updated: _save_names_to_file()
            return
        data2 = _get_bcs_player_info(name)
        if data2 and isinstance(data2, dict):
            try:
                if widget:
                    babase.pushcall(Call(widget._transition_out), from_other_thread=True)
               # babase.pushcall(Call(PlayerInfoPopup, self.real_name), from_other_thread=True)
                #babase.pushcall(Call(bui.buttonwidget, edit=self._view_account_button, icon=bui.gettexture('ouyaUButton'), on_activate_call=self._on_view_account_button_press), from_other_thread=True)
            except Exception as e: logging.exception(e)
            _bcs_player_info_obtained(player_name, data2, no_confirmation, print_progress_only)
            all_names[player_name]['searched_bcs'] = True
            all_names_updated = True
        elif data is False:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchError').format(name)} {sad}"
            if not print_progress_only:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
        elif data is None:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchFailedConnect').format(name)} {sad}"
            if not print_progress_only:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
        else:
            msg = f"{CMD_LOGO_CAUTION} {get_lang_text('bcsFetchNotFound').format(name)} {sad}"
            if not print_progress_only:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_ERROR), from_other_thread=True)
            all_names[player_name]['searched_bcs'] = False
            all_names_updated = True
            if all_names_updated: _save_names_to_file()

def _get_bcs_player_info(name: str):
    """Get Player Info From BCS Database. Should be on another `Thread`"""
    # Code Get From Sara, Edited By LessPal
    global names_asked_bcs
    if name not in names_asked_bcs: names_asked_bcs.append(name)
    pbid = ""
    all_account_data: List[Dict[str, Any]] = []
    try:
        print(f"Name Asked BCS: {str(name)}")
        url = f'https://{BCSSERVER}/player?key={base64.b64encode(name.encode("utf-8")).decode("utf-8")}&base64=true'
        bsbuild_number = _babase.env().get("build_number", 0)
        #print("Build Number:", str(bsbuild_number))
        req = urllib.request.Request(url, headers={"User-Agent": f'BS{str(bsbuild_number)}', "Accept-Language": "en-US,en;q=0.9"})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            all_account_data = json.loads(data.decode('utf-8'))

            if all_account_data : all_account_data_string = str(all_account_data[0])
            else                : all_account_data_string = "Empty"
            if responder_config.get(config_name_cmdprint): _show_bcs_url_stats(name=str(name), url=url, data=all_account_data_string)# babase.pushcall(Call(_show_bcs_url_stats, name=str(name), url=url, data=all_account_data_string), from_other_thread=True)

            if all_account_data:
                names_asked_bcs.remove(name)
                return all_account_data[0]
    except urllib.error.URLError as e:
        names_asked_bcs.remove(name)
        return None
    except Exception as e:
        print_internal_exception(e)
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('errorWhileGetDataFromBCS')} ({name}) {get_random_unamused_emoji()}", COLOR_SCREENCMD_ERROR), from_other_thread=True)
        names_asked_bcs.remove(name)
        return False
    names_asked_bcs.remove(name)
    return all_account_data

def _bcs_player_info_obtained(account_name: str, account_data: Dict[str, Any], no_confirmation: bool = False, print_progress_only: bool = False):
    """Actions After PLayer Data From BCS Database Successfully Obtained, Should be on another `Thread`"""
    try:
        pbid = None
        try:
            ### Data ###
            pbid = account_data.get("pbid")
            old_pbid = None
            try: old_pbid = all_names[account_name].get("pb_id")
            except Exception as e:
                print(f"Failed Getting {account_name}\'s PB-ID From All Names: {e}")
            player_id = account_data.get("_id")
            player_other_acc = account_data.get("accounts")
            player_premium_name = account_data.get('name')
            player_premium_names = account_data.get('names')
            player_acc_created_on = account_data.get('createdOn')
            player_acc_updated_on = account_data.get('updatedOn')
            player_discord = account_data.get('discord')
            player_v = account_data.get('__v')
            ### Appereance ###
            player_character = account_data.get('character')

            if player_other_acc and len(player_other_acc) != 0:
                player_other_acc_joint = ", ".join([str(x) for x in player_other_acc]) 
            else:
                player_other_acc_joint = "¯\\_(ツ)_/¯"

            if player_premium_names and len(player_premium_names) != 0:
                player_premium_names_joint = ", ".join([str(x) for x in player_premium_names])
            else:
                player_premium_names_joint = "¯\\_(ツ)_/¯"

            if player_discord and len(player_discord) != 0:
                player_discord_joint = ", ".join([str(x) for x in player_discord])
            else:
                player_discord_joint = "¯\\_(ツ)_/¯"

            ### Other Actions After Data Obtained ###
            #babase.pushcall(Call(chatmessage, f"{account_name}\'s PB-ID {str(pbid)}"), from_other_thread=True)
            msg = f"{CMD_LOGO_POSITIVE} Successfully Obtaining Player {account_name}\'s Data {get_random_happy_emoji()}"
            if not print_progress_only:
                babase.pushcall(Call(screenmessage, msg, COLOR_SCREENCMD_NORMAL), from_other_thread=True)

            new_player_all_names_data: Dict[str, dict[str, Any]] = {} # Prepare the Updated Data
            new_player_all_names_data[account_name] = {}
            if pbid: new_player_all_names_data[account_name]['pb_id'] = pbid
            if player_id: new_player_all_names_data[account_name]['_id'] = player_id
            if player_other_acc:
                acc_joint = ", ".join(player_other_acc)
            #    print(acc_joint)
                for other_acc in player_other_acc:
                    if other_acc == account_name:
                        player_other_acc.remove(other_acc)
                        print(f"{account_name}\'s Same Account: [{other_acc}] Removed")
                if player_other_acc:
                    new_player_all_names_data[account_name]['accounts'] = player_other_acc
                else:
                    new_player_all_names_data[account_name]['accounts'] = False
                    print(f"{account_name}\'s Account Value Turned Into: False")
            if player_premium_name: new_player_all_names_data[account_name]['current_premium_profile'] = player_premium_name
            else: new_player_all_names_data[account_name]['current_premium_profile'] = False
            if player_premium_name and player_premium_names:
                prem_joint = ", ".join(player_premium_names)
         #       print(prem_joint) 
                for prem_name in player_premium_names:
                    if prem_name == player_premium_name:
                        player_premium_names.remove(prem_name)
                        print(f"{account_name}\'s Same Premium Profile: [{prem_name}] Removed")
                    if prem_name in player_premium_names and prem_name == account_name:
                        player_premium_names.remove(prem_name)
                        print(f"{account_name}\'s Same Premium Profile: [{prem_name}] Removed")
                if player_premium_names:
                    new_player_all_names_data[account_name]['other_premium_profiles'] = player_premium_names
            if player_acc_created_on: new_player_all_names_data[account_name]['createdOn'] = player_acc_created_on
            if player_acc_updated_on: new_player_all_names_data[account_name]['updatedOn'] = player_acc_updated_on
            if player_discord: new_player_all_names_data[account_name]['discord'] = player_discord
            if player_character: new_player_all_names_data[account_name]['spaz'] = player_character

        except Exception as e:
            print_internal_exception(e)
            return
        if old_pbid:
            if pbid != old_pbid:
                pb_id_info_text = f"{old_pbid} (Local) -> {pbid} (BCS)"
            else:
                pb_id_info_text = f"{pbid} (Same)"
        else:
            pb_id_info_text = f"{pbid}"
        custom_info_text_list = (
            f'PB-ID: {pb_id_info_text}\n' +
            f'ID: {player_id}\n' +
            f'{get_lang_text("bcsObtainedOtherAcc")}: {player_other_acc_joint}\n' +
            f'{get_lang_text("bcsObtainedUpgradedName")}: {player_premium_name}\n' +
            f'{get_lang_text("bcsObtainedOtherUpgradedName")}: {player_premium_names_joint}\n' +
            f'{get_lang_text("bcsObtainedCretedOn")}: {player_acc_created_on}\n' +
            f'{get_lang_text("bcsObtainedUpdatedOn")}: {player_acc_updated_on}\n' +
            f'{get_lang_text("bcsObtainedConnectedDiscord")}: {player_discord_joint}\n' +
            f'{get_lang_text("bcsObtainedSpaz")}: {player_character}'
        )

        if no_confirmation:
            _overwrite_current_player_data_with_bcs_data(account_name, new_player_all_names_data)
        else:
            text = get_lang_text('confirmChangesFromBCS')
            babase.pushcall(Call(ConfirmWindow,
                origin_widget=None, # type: ignore
                text=f"{text}:\n{account_name}?", # type: ignore
                action= Call(_overwrite_current_player_data_with_bcs_data, account_name, new_player_all_names_data), # type: ignore
                cancel_is_selected=True, # type: ignore
                width= min(len(text)*13.5, 600), # type: ignore
                height= 150, # type: ignore
                text_scale=1, # type: ignore
                ok_text=get_lang_text('save'), # type: ignore
                cancel_text=get_lang_text('cancel') # type: ignore
            ), from_other_thread=True)
    except Exception as e:
        print_internal_exception(e)
        babase.pushcall(Call(screenmessage, f"{CMD_LOGO_CAUTION} {get_lang_text('errorAfterGetDataFromBCS')}: {account_name} {get_random_unamused_emoji()}", COLOR_SCREENCMD_ERROR), from_other_thread=True)

gun_cocking = bui.getsound('gunCocking')
def _overwrite_current_player_data_with_bcs_data(name: str, data: Dict[str, dict[str, Any]]):
    global all_names
    old_pb = all_names[name].get("pb_id")
    all_names[name].update(data[name])
    all_names[name]['searched_bcs'] = True
    if old_pb:
        # Use Their Old Pb
        # Can usually make make it unobtainable from BCS player account viewer
        if not responder_config.get(config_name_prioritize_bcs_pb):
            all_names[name]['pb_id'] = old_pb
    #_save_names_to_file()
    babase.pushcall(gun_cocking.play, from_other_thread=True)

def _show_bcs_url_stats(name: str, url: str, data: str):
    print("\n#==============================================#")
    print(f"Name Asked BCS: {str(name)}")
    print(f"URL Asked: {url}")
    print(f"Format {name}\'s Returned: {str(data)}")
    print("#==============================================#\n")

class PlayerListPopup(popup.PopupWindow):
    """Player List Window"""
    def _get_player_data_type(self, label: str, load_only: bool = False) -> Dict[str, Dict[str, Any]]:
        self._refresh_allowed = True
        if label == self._label_allnames:
            player_names = all_names
            if not load_only:
                self.players_per_page = players_per_page_on_all_namelist  # Maximum number of players per page
        elif label == self._label_currentsession:
            player_names = current_session_namelist
            if not load_only:
                self.players_per_page = players_per_page_on_current_session_namelist
        elif label == self._label_currentnamelist:
            player_names = current_namelist
            if not load_only:
                self.players_per_page = len(player_names)
        else:
            player_names = self._unmodified_pdata
            if not load_only:
                self.players_per_page = len(player_names)
                self._refresh_allowed = False
        return player_names

    def __init__(self, player_names: Dict[str, dict[str, Any]], search_term: str = ""):
        self._unmodified_pdata = player_names

        self._label = ""
        self._label_allnames = "All Namelist"
        self._label_currentsession = "Current Session"
        self._label_currentnamelist = "Namelist"

        ####### Determine Pdata Type #######
        if player_names == all_names:
            self.player_names = all_names
            self.players_per_page = players_per_page_on_all_namelist  # Maximum number of players per page
            self._label = self._label_allnames

        elif player_names == current_session_namelist:
            self.player_names = current_session_namelist
            self.players_per_page = players_per_page_on_current_session_namelist
            self._label = self._label_currentsession

        elif player_names == current_namelist:
            self.player_names = current_namelist
            self.players_per_page = len(player_names)
            self._label = self._label_currentnamelist

        else:
            self.player_names = player_names
            self.players_per_page = len(player_names)
            self._refresh_allowed = False
            self._label = '???'
        ####### Determine Pdata Type #######

        self._get_player_data_type(self._label)

        self._is_refreshing = False
        self.search_widget_visible = False
        self._is_searhing = False
        self._last_search_term = ""

        self.current_page = 0  # Track the current page
        self._buttons = []
        self.total_pages = (len(player_names) - 1) // self.players_per_page + 1  # Calculate the total pages
        uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        self._width = 900
        self._height = 500
        self.bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self.colors = [color for color in COLORS.values()]
        # Count the number of players
        servers_count = sum(1 for profile_info in self.player_names.values() if profile_info.get('client_id') == -1)
        players_count = sum(1 for profile_info in self.player_names.values() if profile_info.get('client_id') != -1)

     #   label = label + f" (Players: {players_count})"
        label = self._label + f" (Players: {players_count}, Servers: {servers_count})"

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0),
            bg_color=self.bg_color)

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(55, self._height - 63),
            size=(55, 55),
            scale=.875,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)

        self._label_textwidget = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.275, self._height - 55),
            size=(self._width * 0.5, 35),
            h_align='center',
            v_align='center',
            scale=1.45,
            text=f"{label}",
            autoselect=False,
            selectable=True,
            click_activate=True,
            on_activate_call=Call(bs.broadcastmessage, get_random_happy_emoji(), COLOR_SCREENCMD_NORMAL),
            color=bui.app.ui_v1.title_color)
        
        self._page_text = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 478),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.25,
            text=f"Total: {players_count + servers_count} | Page: {self.current_page + 1} / {self.total_pages}" if len(self.player_names) > self.players_per_page else f"Total: {len(self.player_names)}",
            maxwidth=self._width * 0.8,
            color=bui.app.ui_v1.title_color)

        # Scrollable widget for player list
        self.scroll_size = (self._width - 60, self._height - 115)
        self.scroller = bui.scrollwidget(
            parent=self.root_widget,
            position=(25, 45),
            size=self.scroll_size,
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))  # Scroller Line Color

        self.scroll = bui.columnwidget(parent=self.scroller)

        if len(self.player_names) > self.players_per_page:
            # Add Next and Previous Buttons
            self._previous_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.11, self._height - 495),
                size=(90, 40),
                label='',
                scale=1,
                on_activate_call=self._previous_page,
                color=self.bg_color,
                autoselect=False)

            self._next_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.79, self._height - 495),
                size=(90, 40),
                label='',
                scale=1,
                on_activate_call=self._next_page,
                color=self.bg_color,
                autoselect=False)

        # Show the first page
        self._show_page(self.current_page)

        # Add search toggle button
        self._toggle_search_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width - 90, self._height - 495),
            size=(90, 40),
            label='Search',
            on_activate_call=self._toggle_search_widget,
            color=self.bg_color)

        #if self._refresh_allowed:
        self._refresh_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.925, self._height * 0.875),
            size=(40, 40),
            label='',
            color=self.bg_color,
            on_activate_call=self._on_refresh_press,
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.2)

        self._search_widget: Optional[bui.Widget] = None
        self._search_button: Optional[bui.Widget] = None
        self._reset_search_button: Optional[bui.Widget] = None
        self._profile_match_checkbox: Optional[bui.Widget] = None

        if search_term and search_term != "":
            self._toggle_search_widget()
            if self._search_widget and self._search_widget.exists():
                bui.textwidget(edit=self._search_widget, text=search_term)
                self._start_search()

    def _toggle_search_widget(self):
        """Toggle visibility of the search widget."""
        self.search_widget_visible = not self.search_widget_visible
        self._match_with_profile = False
        if not self.search_widget_visible:
            if self._search_widget and self._search_widget.exists(): self._search_widget.delete()
            if self._search_button and self._search_button.exists(): self._search_button.delete()
            if self._reset_search_button and self._reset_search_button.exists(): self._reset_search_button.delete()
            if self._profile_match_checkbox and self._profile_match_checkbox.exists(): self._profile_match_checkbox.delete() 
        else:
            # Add search text widget (initially hidden)
            self._search_widget = bui.textwidget(
                parent=self.root_widget,
                position=(42.5, self._height - 120),
                size=(self._width - 250, 40),
                text='',
                v_align='center',
                h_align='left',
                editable=True
            )

            # Add search action buttons (search and reset)
            self._reset_search_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width - 200, self._height - 120),
                size=(40, 40),
                label='',
                on_activate_call=self._reset_search,
                color=self.bg_color,
                icon=bui.gettexture('replayIcon'),
                iconscale=1.2
            )
            self._search_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width - 150, self._height - 120),
                size=(90, 40),
                label='Start',
                on_activate_call=self._start_search,
                color=self.bg_color
            )
            if self._search_widget and self._search_button:
                bui.textwidget(edit=self._search_widget, on_return_press_call=self._search_button.activate)

            # Add a checkbox widget to configure profile matching
            self._profile_match_checkbox = bui.checkboxwidget(
                parent=self.root_widget,
                position=(self._width - 50, self._height - 120),
                size=(40, 40),
                text='',
                value=self._match_with_profile,
                on_value_change_call=self._toggle_profile_matching
            )

        self.scroll_size = (
            self._width - 60,
            self._height - (175 if self.search_widget_visible else 115),
        )
        bui.scrollwidget(edit=self.scroller, size=self.scroll_size)

    def _toggle_profile_matching(self, v: bool):
        self._match_with_profile = v
        screenmessage(
            message=(get_lang_text('findPlayerIncludeProfileEnable') if v else
                     get_lang_text('findPlayerIncludeProfileDisable')
            ),
            color=COLOR_SCREENCMD_NORMAL
        )

    def _start_search(self):
        """Start searching players based on the search term."""
        search_term: str = bui.textwidget(query=self._search_widget)
        min_argument_len = 1
        if len(search_term) < min_argument_len:
            screenmessage(message=get_lang_text('findPlayerCmdShortArgument').format(str(min_argument_len)), color=COLOR_SCREENCMD_ERROR)
            return

        if search_term == self._last_search_term:
            pass#return
        self._last_search_term = search_term

        matched_players = _group_matched_players(self._get_player_data_type(self._label), sanitize_name(search_term), self._match_with_profile)
        self.player_names = matched_players
        self.search_word = search_term
        self.current_page = 0
        self.total_pages = (len(self.player_names) - 1) // self.players_per_page + 1
        self._is_searhing = True
        self._show_page(self.current_page)

    def _reset_search(self):
        """Reset the search and show all players."""
        self.player_names = self._get_player_data_type(self._label)
        self.search_word = ""
        bui.textwidget(edit=self._search_widget, text="")
        self.current_page = 0
        self.total_pages = (len(self.player_names) - 1) // self.players_per_page + 1
        self._is_searhing = False
        self._show_page(self.current_page)

    def _on_refresh_press(self):
        try:
            if self._is_refreshing:
                bs.broadcastmessage(f'Cooldown A Bit Pal {get_random_happy_emoji()}', color=COLOR_SCREENCMD_NORMAL)
                return
            self._is_refreshing = True
            babase.apptimer(6, Call(self._reset_refresh))
            load_all_names_data()
            if not self._is_searhing:
                self.player_names = self._get_player_data_type(self._label, load_only=self._is_searhing)
            else:
                invalid_names: List[str] = []
                for name in self.player_names.keys():
                    if name not in all_names:
                        invalid_names.append(name)
                if invalid_names:
                    for name in invalid_names:
                        del self.player_names[name]

            self.scroll.delete()
            self.scroll = bui.columnwidget(parent=self.scroller)
            self._show_page(self.current_page, is_refresh=True)
            bs.broadcastmessage('Player List Refreshed', color=COLOR_SCREENCMD_NORMAL)
        except Exception as e:
            bs.broadcastmessage(f"{CMD_LOGO_CAUTION} Error Player List Refresh: {e}", color=COLOR_SCREENCMD_ERROR)
            bs.chatmessage(f"{CMD_LOGO_CAUTION} Error List Refresh: {e}")
            print_internal_exception(e)

    def _reset_refresh(self):
        self._is_refreshing = False

    def _show_page(self, page: int, is_refresh:bool=False):
        """Display the players of the current page"""
        if not is_refresh:
            self.scroll.delete()  # Clear previous content
            self.scroller.delete()

            self.scroller = bui.scrollwidget(
                parent=self.root_widget,
                position=(25, 45),
                size=self.scroll_size,
                color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2))  # Scroller Line Color
            self.scroll = bui.columnwidget(parent=self.scroller)
        """
        self.scroll.delete()
        self.scroll = bui.columnwidget(parent=self.scroller)
        if self._buttons != []:
            for _buttons in self._buttons:
                _buttons.delete()
        """
        start_index = page * self.players_per_page
        end_index = min(start_index + self.players_per_page, len(self.player_names))

        server_color_button = random.choice(self.colors)
        real_data = list(self._get_player_data_type(label=self._label, load_only=True).keys())
        #print(f"{self._show_page.__name__} is searhing: {self._is_searhing}")
        for i, (real_name, profile_info) in enumerate(list(self.player_names.items())[start_index:end_index]):
            row = bui.rowwidget(parent=self.scroll, size=(self.scroll_size[0], 40))
            full_name = profile_info.get('profile_name', [])
            client_id = profile_info.get('client_id')
            pb_id = all_names[real_name].get('pb_id')

            player_index = real_data.index(real_name) + 1
            display_name = f"[{player_index}] {real_name}"

            display_name += f" | {(', '.join(full_name))}" if full_name else f" | [In Lobby]" # Add profile
            if pb_id:
                display_name += f' | {pb_id}' # Add pb-id

            button = bui.buttonwidget(
                parent=row,
                label=display_name,
                position=(-10, 0),
                size=(self.scroll_size[0] - 20, 38.5),
                on_activate_call=Call(self.on_player_data_pressed, real_name),
                enable_sound=False,
                color=server_color_button if client_id == -1 else self.bg_color)

            #self._buttons.append(button)

        # Update button states and page text
        bui.textwidget(edit=self._page_text, text=(f"Total: {len(self.player_names)} | Page: {self.current_page + 1} / {self.total_pages}" if len(self.player_names) > self.players_per_page else f"Total: {len(self.player_names)}"))

    def on_player_data_pressed(self, name: str):
        if name not in all_names:
            screenmessage(get_lang_text('playerOptionRemoveDataNotExist').format(name), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return
        bui.getsound('swish').play()
        PlayerInfoPopup(name)

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._show_page(self.current_page)
        else:
            self.current_page = 0
            self._show_page(self.current_page)
        
    def _previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
        else:
            self.current_page = (len(self.player_names) - 1) // self.players_per_page
            self._show_page(self.current_page)
            
    def on_list_click(self, real_name, full_name, client_id, pb_id):
        display_name = f"[{client_id}] {real_name} | {full_name}" if full_name else f"[{client_id}] {real_name} [In Lobby]"
        display_name_pb = display_name + (f'\n{pb_id}' if pb_id else '')
        babase.clipboard_set_text(display_name_pb)
        bs.chatmessage(display_name)
        if pb_id:
            bs.chatmessage(f'[{real_name}] PB-ID: {pb_id}')
        if not babase.app.classic.party_window(): bs.broadcastmessage(display_name + (f' | {pb_id}' if pb_id else ''), color=(.7, .35, .5)) # type: ignore

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()

class ListPopup(popup.PopupWindow):
    def __init__(self, list_data: list[str] | dict[str, str], label: str = ""):
        """Simple List or Dict Popup Window. Also Add Label"""
        self._list_data = list_data
        self._func_list_data = None
        self._is_dict = False

        self._is_refreshing = False
        if isinstance(list_data, dict):
            self._is_dict = True

        self.chats_per_page = maximum_bombsquad_chat_messages # Use the default maximum party window chats each pages
        self.current_page = (len(self._list_data) - 1) // self.chats_per_page # Automatically show last page of the chats
        self.total_pages = (len(self._list_data) - 1) // self.chats_per_page + 1

        self._text_label = label
        self._popup_type = ''
        self._popup_party_member_client_id: Optional[int] = None
        self._popup_party_member_is_host: Optional[bool] = False

        self._width = 950
        self._height = 625
        self.bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self._transitioning_out = False
        self._text_widgets = []
        uiscale = bui.app.ui_v1.uiscale

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0),
            bg_color=self.bg_color
        )

        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.6,
            color=bui.app.ui_v1.title_color,
            text=self._text_label
        )

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(55, self._height - 63),
            size=(55, 55),
            scale=.875,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        if self._text_label != "Help" or self._list_data != info_msgs:
            self._refresh_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.9, self._height * 0.875),
                size=(40, 40),
                label='',
                color=self.bg_color,
                on_activate_call= Call(self._refresh, self._func_list_data),
                autoselect=False,
                icon=bui.gettexture('replayIcon'),
                iconscale=1.2)

        if len(self._list_data) > self.chats_per_page:
            self._page_text = bui.textwidget(
                parent=self.root_widget,
                position=(self._width * 0.815, self._height - 62.5),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}",
                color=bui.app.ui_v1.title_color
            )
            self._prev_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.75, self._height - 575),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._previous_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )
            self._next_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.875, self._height - 575),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._next_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )

        self._show_page(self.current_page)

    def _show_page(self, page, is_refresh:bool=False):
        height = self._height * 0.725
        width = self._width
        if not is_refresh:
            if hasattr(self, 'scrollwidget'): self.scrollwidget.delete()
            self.scrollwidget = bui.scrollwidget(
                parent=self.root_widget,
                size=(width, height),
                position=(10, 90),
                color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2),
                highlight=False)
            if hasattr(self, 'chat_container'): self.chat_container.delete()
            self.chat_container = bui.columnwidget(parent=self.scrollwidget, border=2, margin=0)
        else:
            self.chat_container.delete()
            self.chat_container = bui.columnwidget(parent=self.scrollwidget, border=2, margin=0)

        start_index = page * self.chats_per_page
        end_index = start_index + self.chats_per_page
        if isinstance(self._list_data, list):
            for i, text in enumerate(self._list_data[start_index:end_index]):
                self._create_text_widget(i, text)
        elif isinstance(self._list_data, dict):
            for i, (key, value) in enumerate(self._list_data.items()):
                self.key_and_value_splitter = f'{PNAME_AND_MSG_SPLITTER_MODIFIED}'
                text = f"{str(key)}{self.key_and_value_splitter}{str(value)}"
                self._create_text_widget(i, text)
        else:
            print(f'Unhandled ListPopup Type: {type(self._list_data)}')

    def _create_text_widget(self, i: int, text: str):
        if self._is_dict and self.key_and_value_splitter in text:
            key, value = text.split(self.key_and_value_splitter, 1)
        text_widget = bui.textwidget(
            parent=self.chat_container,
            size=(self._width, 22.5),
            text=text if (self._text_label != "Help" or self._list_data != info_msgs) else f"{str(i + 1)}. {text}",
            maxwidth=self._width * 0.975,
            scale=1,
            h_align='left',
            v_align='center',
            selectable=True,
            autoselect=False,
            click_activate=True,
            color=(0.8, 0.8, 0.8) if not text.startswith(CMD_LOGO_SERVER) else (self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2)
        )
        if len(self._list_data) > self.chats_per_page:
            bui.textwidget(edit=self._page_text, text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}")

        bui.textwidget(
            edit=text_widget,
            on_activate_call=CallStrict(self._confirm_copy, text))
        #    Call(ListPopupInternalDataConfirmation, text, self._list_data, self) if not self._is_dict else
        self._text_widgets.append(text_widget)

    def _translate_textwidget(self, text_widget_text: str, text_widget: bui.Widget):
        """Translate the Pressed textwidget"""
        msg: str = bui.textwidget(query=text_widget)
        cleaned_msg = ''.join(filter(str.isalpha, text_widget_text))

        if not msg or not cleaned_msg or msg == '':
            screenmessage(f'{CMD_LOGO_CAUTION} ' + get_lang_text('translateEmptyText'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('translating'), COLOR_SCREENCMD_NORMAL)
            name = ''
            if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                name, text = msg.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
            else:
                text = msg

            def _apply_translation(translated: str):
                if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                    translate_text = name + PNAME_AND_MSG_SPLITTER_MODIFIED + translated
                else:
                    translate_text = translated
                if text_widget.exists():
                    bui.textwidget(edit=text_widget, text=translate_text)
            Translate(text=text, callback=_apply_translation)


    def _refresh(self, data =None):
        if data is not None:
            try:
                if isinstance(data, (dict, list)):
                    self._list_data = data
                    self._show_page(self.current_page, is_refresh=True)
                else:
                    if self._is_refreshing:
                        screenmessage(f'Cooldown A Bit Pal {get_random_happy_emoji()}', color=COLOR_SCREENCMD_NORMAL)
                        return
                    self._is_refreshing = True
                    babase.apptimer(1.75, Call(self._reset_refresh))
                    self._list_data = data()
                    screenmessage('Data Refreshed', color=COLOR_SCREENCMD_NORMAL)
                    self._show_page(self.current_page, is_refresh=True)
            except Exception as e:
                print_internal_exception(e)

    def _reset_refresh(self):
        self._is_refreshing = False

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._show_page(self.current_page)
        else:
            self.current_page = 0
            self._show_page(self.current_page)

    def _previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
        else:
            self.current_page = (len(self._list_data) - 1) // self.chats_per_page
            self._show_page(self.current_page)

    def _confirm_copy(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 13.5
        else:
            width = len(text) * 13.5
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}?\n{text_title}",
            width= width,
            height=135,
            action=CallStrict(_copy_to_clipboard, text),
            cancel_is_selected=True,
            cancel_text=get_lang_text('cancel'),
            text_scale=1,
            ok_text=get_lang_text('copy')
        )

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()



def save_custom_translated_text(data: Dict[str, str], lang_key: str) -> bool:
    try:
        path = custom_translated_text_file_path.format(lang_key=lang_key)
        if not os.path.exists(custom_translated_text_folder_path):
            os.makedirs(custom_translated_text_folder_path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print_internal_exception(e)
        return False
    return True

def load_custom_translated_text(lang_key: str) -> Dict[str, str]:
    path = custom_translated_text_file_path.format(lang_key=lang_key)
    data: Dict[str, str] = {}
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except Exception as e:
        print_internal_exception(e)
    #print(f"{load_custom_translated_text.__name__}: {data}")
    return data

def load_and_get_lang_key_custom_tranlated_text() -> Dict[str, Dict[str, str]]:
    """
    Load and retrieve custom translated text data.

    This function reads translation files from a specified directory,
    extracts the language key from the file name,
    and loads the translation data from the file.
    The data is returned as a dictionary where each key is a translation key
    and the value is another dictionary containing the language key
    and its corresponding translation.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary containing translation keys and their corresponding language-specific translations.
    """
    data: Dict[str, Dict[str, str]] = {}
    try:
        if not os.path.exists(custom_translated_text_folder_path):
            os.makedirs(custom_translated_text_folder_path)

        files = os.listdir(custom_translated_text_folder_path)
        if not files:
            return data

        for file_name in files:
            file_path = os.path.join(custom_translated_text_folder_path, file_name)
            if os.path.isfile(file_path):
                lang_key = file_name
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_data: Dict[str, str] = json.load(file)
                        for key, val in file_data.items():
                            data[key] = {lang_key: val}
                except json.JSONDecodeError as json_error:
                    msg = f"Error decoding JSON from custom translation file [{file_name}]:\n{json_error}\n"
                    print(msg)
                    screenmessage(msg.replace("\n", ""), COLOR_SCREENCMD_ERROR)
    except Exception as e:
        print_internal_exception(e)
    return data


def save_new_translated_text(data: Dict[str, str], lang_key: str, lang: str) -> bool:
    try:
        path = new_translated_text_file_path.format(lang_key=lang_key, lang=lang)
        if not os.path.exists(new_translated_text_folder_path):
            os.makedirs(new_translated_text_folder_path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print_internal_exception(e)
        return False
    return True

def load_new_translated_text(lang_key: str, lang: str) -> Dict[str, str]:
    path = new_translated_text_file_path.format(lang_key=lang_key, lang=lang)
    data: Dict[str, str] = {}
    try:
        if not os.path.exists(new_translated_text_folder_path):
            os.makedirs(new_translated_text_folder_path)

        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
    except Exception as e:
        print_internal_exception(e)
    #print(f"{load_custom_translated_text.__name__}: {data}")
    return data


def load_and_get_lang_key_new_tranlated_text() -> List[str | Dict[str, str]]:
    """
    Load and retrieve new translated text data.

    This function reads translation files from a specified directory, extracts the language key and language name from the file name, 
    and loads the translation data from the file. The data is returned as a list where:
    - index 0 is the language key (lang_key)
    - index 1 is the language name (lang)
    - index 2 is the translation data (data)

    Returns:
        List[Union[str, str, Dict[str, str]]]: A list containing the language key, language name, and translation data.
    """
    data: List[str | Dict[str, str]] = []
    try:
        if not os.path.exists(new_translated_text_folder_path):
            os.makedirs(new_translated_text_folder_path)

        files = os.listdir(new_translated_text_folder_path)
        if not files: return data

        for file_name in files:
            file_path = os.path.join(new_translated_text_folder_path, file_name)
            if os.path.isfile(file_path):
                lang_id, lang = file_name.split(new_translated_text_file_splitter, 1)
                with open(file_path, 'r', encoding='utf-8') as file:
                    translation_data: Dict[str, str] = json.load(file)
                    format: List[str | Dict[str, str]] = [lang_id, lang, translation_data]
                    data.append(format) # type: ignore

    except Exception as e:
        print_internal_exception(e)
    return data


def warning_confirm_text(widget: Optional[bui.Widget] = None):
    text = get_lang_text('translatePopupWarning')
    lines = text.count('\n')
    ConfirmWindow(
        origin_widget=widget,
        text=f"{text}",
        width=min((len(text)*12)/lines, 600),
        height=text.count('\n')*80,
        cancel_button=False,
        text_scale=1,
    )

warning_translate_text: bool = False
class TranslateTextsPopup(popup.PopupWindow):
    """Popup for viewing and editing translated text dictionaries"""
    def __init__(self, translate_texts: Dict[str, Dict[str, str]]):
        self._translate_texts = translate_texts
        self._current_lang_id = party_config.get(CFG_NAME_PREFFERED_LANG, "en")
        self._current_new_language = ""

        self._width = 1200
        self._height = 700
        self.bg_color = (0, 0.5, 0.25)

        self._new_translate_texts: Dict[str, Dict[str, str]] = {}
        new_data = load_and_get_lang_key_new_tranlated_text()
        if new_data:
            for lang_data in new_data:
                lang_id, lang, trans_data = lang_data
                if isinstance(lang_id, str) and isinstance(lang, str) and isinstance(trans_data, dict):
                    self._new_translate_texts.update({key: {lang_id: val} for key, val in trans_data.items()})
            #print("New Translation Data Exist")
            #print(new_data)

        self._is_editing_new_lang = False
        self._is_data_modified = False  # Track if data has been modified
        self._preview_mode = False     # Track preview mode for new language editing

        self._uiscale = bui.app.ui_v1.uiscale

        self._translation_text_widgets: Dict[str, list[bui.Widget]] = {}
        """How to use:

        `text = "\n".join(bui.textwidget(query=widget) for widget in self._translation_text_widgets[key])`
        """

        #### PopupMenu ####
        self._popup_type = ""
        #### PopupMenu ####

        super().__init__(
            position=(0, 0),
            size=(self._width, self._height),
            scale=(2.06 if self._uiscale is babase.UIScale.SMALL else
                   1.40 if self._uiscale is babase.UIScale.MEDIUM else
                   1.00),
            bg_color=self.bg_color
        )

        global warning_translate_text
        if not warning_translate_text:
            warning_translate_text = True
            warning_confirm_text(self.root_widget)

        # Main label
        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 35),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.8,
            color=bui.app.ui_v1.title_color,
            text=get_lang_text('translateTextLabel')
        )

        # Cancel button
        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(5, self._height - 70),
            size=(55, 55),
            scale=1.1,
            label='',
            color=self.bg_color,
            on_activate_call=self.on_popup_cancel,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        self._lang_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width*0.75, 30),
            size=(150, 40),
            label='Select Language',
            autoselect=False,
            on_activate_call=self._show_language_menu
        )

        self._save_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width/2, 30),
            size=(100, 40),
            label='Save',
            autoselect=False,
            on_activate_call=self._save_translation
        )

        self._new_lang_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width*0.25, 30),
            size=(150, 40),
            label='New Language',
            autoselect=False,
            on_activate_call=self._toggle_new_lang
        )


        # Add a scroll widget to display all keys
        self.scrollwidget_width = self._width - 60
        self.scrollwidget_height = self._height - 150
        self.scroll_size = (self.scrollwidget_width, self.scrollwidget_height)

        self._scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            position=(30, 72.5),
            size=self.scroll_size,
            highlight=False
        )

        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0
        )

        self.barrier_space = 25

        self._show_data(self._translate_texts)

        # Add preview button (hidden by default)
        self._preview_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.1, 30),
            size=(100, 40),
            label='Preview',
            autoselect=False,
            on_activate_call=self._toggle_preview,
         #   visible=False
        )

        self._new_lang_is_visible = False
        self._new_lang_textwidget: Optional[bui.Widget] = None
        self._create_new_lang_button: Optional[bui.Widget] = None


    def _toggle_new_lang(self):
        self._new_lang_is_visible = not self._new_lang_is_visible
        if not self._new_lang_is_visible:
            if self._new_lang_textwidget and self._new_lang_textwidget.exists(): self._new_lang_textwidget.delete()
            if self._create_new_lang_button and self._create_new_lang_button.exists(): self._create_new_lang_button.delete()
        else:
            self._new_lang_textwidget = bui.textwidget(
                parent=self.root_widget,
                position=(50, self._height - 125),
                size=(self.scrollwidget_width - 100, 40),
                text='',
                v_align='center',
                h_align='left',
                editable=True
            )

            self._create_new_lang_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width - 100, self._height - 125),
                size=(50, 50),
                label='',
                on_activate_call=self._create_new_language,
                color=self.bg_color,
                scale=1.2,
                icon=bui.gettexture('rightButton'),
                iconscale=1.2
            )

        self.scroll_size = (
            self.scrollwidget_width,
            (self.scrollwidget_height - 50 if self._new_lang_is_visible else self.scrollwidget_height),
        )
        bui.scrollwidget(edit=self._scrollwidget, size=self.scroll_size)

    ####### GUI INFORM #######
    def _new_lang_no_splitter(self, spl: str):
        bui.getsound('error').play(1.5)
        screenmessage(get_lang_text("addNewLangNoSplitter").format(spl), color=COLOR_SCREENCMD_ERROR)

    def _new_lang_invalid(self):
        bui.getsound('error').play(1.5)
        screenmessage(get_lang_text("addNewLangInvalid"), color=COLOR_SCREENCMD_ERROR)

    def _new_lang_exist(self):
        bui.getsound('error').play(1.5)
        screenmessage(get_lang_text("addNewLangExist"), color=COLOR_SCREENCMD_ERROR)
    ####### GUI INFORM #######

    ############################# IS DATA MODIFIED #############################
    def _toggle_preview(self):
        self._preview_mode = not self._preview_mode
        if self._preview_mode:
            for key, widgets in self._translation_text_widgets.items():
                edited_text = "\n".join(bui.textwidget(query=widget) for widget in widgets)
                edited_text = edited_text.replace("\\n", "\n")
                if key not in self._new_translate_texts:
                    self._new_translate_texts[key] = {}
                self._new_translate_texts[key][self._current_lang_id] = edited_text

            self._last_preview_lang = self._current_lang_id
            self._current_lang_id = "en"
            self._show_data(self._translate_texts, preview=True)
        else:
            for key, widgets in self._translation_text_widgets.items():
                edited_text: str = "\n".join(bui.textwidget(query=widget) for widget in widgets)
                if not edited_text: continue
                if key not in self._new_translate_texts:
                    self._new_translate_texts[key] = {}
                self._new_translate_texts[key]["en"] = edited_text

            self._current_lang_id = self._last_preview_lang
            self._show_data(self._new_translate_texts, preview=False)


    def _confirm_exit_without_saving(self) -> None:
        text = 'Changes are not saved. Exit anyway?'
        ConfirmWindow(
            text=text,
            width=min(len(text) * 13.5, 600),
            height=150,
            action=Call(self._exit_without_save),
            cancel_button=True,
            cancel_is_selected=True,
            ok_text='Yes',
            cancel_text='Cancel',
            text_scale=1.0,
            origin_widget=self.root_widget
        )

    def _confirm_change_language(self, *args):
        if len(args) >= 3:
            text = 'Changes are not saved. Create new language anyway?'
            ConfirmWindow(
                text=text,
                width=min(len(text) * 13.5, 600),
                height=150,
                action=Call(args[0], args[1], [args[2]]),
                cancel_button=True,
                cancel_is_selected=True,
                ok_text=get_lang_text('yes'),
                cancel_text=get_lang_text('cancel'),
                text_scale=1.0,
                origin_widget=self.root_widget
            )

    def _confirm_change_data_view(self, *args):
        if len(args) >= 3:
            self._current_lang_id: str = args[2]
            text='Changes are not saved. Change language anyway?'
            ConfirmWindow(
                text=text,
                width=min(len(text) * 13.5, 600),
                height=150,
                action=Call(args[0], args[1]),
                cancel_button=True,
                cancel_is_selected=True,
                ok_text=get_lang_text('yes'),
                cancel_text=get_lang_text('cancel'),
                text_scale=1.0,
                origin_widget=self.root_widget
            )
        else:
            print(f"Not Enough Args On {self._confirm_change_data_view.__name__}\n{args}")
    ############################# IS DATA MODIFIED #############################

    def _create_new_language(self):
        key_and_lang_splitter = ":"
        new_lang_id: str = bui.textwidget(query=self._new_lang_textwidget)

        if key_and_lang_splitter not in new_lang_id:
            self._new_lang_no_splitter(key_and_lang_splitter)
            return

        lang_id, lang = new_lang_id.split(key_and_lang_splitter, 1)
        lang_id = lang_id.strip().lower() ; lang = lang.strip() # heh, just get to know this ; useage ＼（〇_ｏ）／
        if not lang_id or not lang_id.isalpha() or not lang:
            self._new_lang_invalid()
            return

        if lang_id.lower() in DEFAULT_AVAILABLE_LANG_ID_LIST or any(av_lang.lower() in lang.lower() for av_lang in DEFAULT_AVAILABLE_LANG_LIST):
            self._new_lang_exist()
            return

        if self._is_data_edited_on_textwidget(data=self._translate_texts if not self._is_editing_new_lang else self._new_translate_texts):
            self._confirm_change_language(self._start_add_new_lang, lang_id, lang)
            return

        if not lang_id in LANGUAGES:
            self._ask_confirm_new_lang(lang_id, lang)
        else:
            lang = LANGUAGES[lang_id]
            self._start_add_new_lang(lang_id, lang)


    def _start_add_new_lang(self, lang_id: str, lang: str):
        self._new_lang_is_visible = True

        self._is_editing_new_lang = True
        self._is_original_edited = False

        self._current_lang_id = lang_id
        self._current_new_language = lang

        if self._new_translate_texts: self._new_translate_texts = {}

        for key in self._translate_texts.keys():
            if not key or key == "": continue
            self._new_translate_texts[key] = {}
            self._new_translate_texts[key][self._current_lang_id] = ""

        self._show_data(self._new_translate_texts)
        self._toggle_new_lang()

    def _ask_confirm_new_lang(self, lang_id: str, lang: str):
        text = get_lang_text('confirmNewLangID').format(lang_id)
        ConfirmWindow(
            text=f'{text}',
            width=min(len(text) * 13.5, 600),
            height=150,
            action=Call(self._start_add_new_lang, lang_id, lang),
            cancel_button=True,
            cancel_is_selected=True,
            ok_text=get_lang_text('yes'),
            cancel_text=get_lang_text('cancel'),
            text_scale=1.0,
            origin_widget=self.root_widget)

    def _show_data(self, data: Dict[str, Dict[str, str]], preview: bool = False):
        # Add text widgets for each key
        if self._columnwidget:
            self._columnwidget.delete()
            self._columnwidget = bui.columnwidget(
                parent=self._scrollwidget,
                border=2,
                margin=0.25
            )
        self._translation_text_widgets = {}

        if self._current_lang_id in NEW_AVAILABLE_LANG_ID_LIST:
            self._is_editing_new_lang = True
            index = NEW_AVAILABLE_LANG_ID_LIST.index(self._current_lang_id)
            self._current_new_language = NEW_AVAILABLE_LANG_LIST[index].replace(".json", "")
        else:
            self._is_editing_new_lang = False

        if not preview:
            self._preview_mode = False

        ####### Start the loops for showing all data #######

        for i, (key, value) in enumerate(data.items()):
            if (not key or key == ""): continue

            bui.textwidget(
                parent=self._columnwidget,
                size=(self.scrollwidget_width-25, 30),
                maxwidth=self.scrollwidget_width - 80,
                position=(30, 0),
                text=f"{i+1}. {key}",
                editable=False,
                h_align='left',
                v_align='center',
                color=COLOR_SCREENCMD_NORMAL
           #     click_activate=True,
           #     on_activate_call=Call(self._select_key, key)
            )

            invalid_format = INVALID_KEY_TEXT.format(f"{self._current_lang_id} {key}") if not self._is_editing_new_lang else ""
            translated_lang = value.get(self._current_lang_id, invalid_format)
            if "\n" not in translated_lang:
                widget = bui.textwidget(
                    parent=self._columnwidget,
                    editable=not preview,
                    size=(self.scrollwidget_width-25, 40),
                    maxwidth=self.scrollwidget_width - 25,
                    text=translated_lang,
                    h_align='left',
                    v_align='center'
                )
                self._translation_text_widgets[key] = [widget]
                if preview:
                    bui.textwidget(
                        edit=widget,
                        selectable=True,
                        click_activate=True,
                        on_activate_call=Call(self._confirm_copy, translated_lang)
                    )
            else:
                separted_texts = translated_lang.splitlines()
                for text in separted_texts:
                    widget2 = bui.textwidget(
                        parent=self._columnwidget,
                        editable=not preview,
                        size=(self.scrollwidget_width-25, 40),
                        maxwidth=self.scrollwidget_width - 25,
                        text=f"{text}",
                        h_align='left',
                        v_align='center'
                    )
                    if preview:
                        bui.textwidget(
                            edit=widget2,
                            selectable=True,
                            click_activate=True,
                            on_activate_call=Call(self._confirm_copy, str(text))
                        )
                    if key in self._translation_text_widgets:
                        self._translation_text_widgets[key].append(widget2)
                    else:
                        self._translation_text_widgets[key] = [widget2]

            bui.textwidget(parent=self._columnwidget, text='', size=(0, self.barrier_space)) # Barrier

    def _confirm_copy(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 10
        else:
            width = len(text) * 10
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}?\n{text_title}",
            width= width,
            height=135,
            action=Call(_copy_to_clipboard, text),
            cancel_is_selected=True,
            cancel_text=get_lang_text('cancel'),
            ok_text=get_lang_text('copy'),
            text_scale=1
        )

    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return (1.6 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else
                2.0)


    def _show_language_menu(self):
        self._popup_type = "selectLangKeyID"
        PopupMenuWindow(
            position=self._lang_button.get_screen_space_center(),
            choices=DEFAULT_AVAILABLE_LANG_ID_LIST,
            current_choice=self._current_lang_id,
            choices_display=_create_baLstr_list(DEFAULT_AVAILABLE_LANG_LIST),
            color=self.bg_color, # type: ignore
            scale=_get_popup_window_scale(),
            delegate=self
        )

    ################### POPUP MENU SECTION ###################
    def popup_menu_selected_choice(self, popup_window: PopupWindow, choice: str):
        if self._popup_type == "selectLangKeyID":
            self._is_editing_new_lang = False
            self._current_new_language = ""
            if self._is_data_edited_on_textwidget(data=self._translate_texts if not self._is_editing_new_lang else self._new_translate_texts):
                self._confirm_change_data_view(self._show_data, self._translate_texts, choice)
                return
            self._current_lang_id = choice
            self._show_data(self._translate_texts)

        del popup_window

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""
        del popup_window
    ################### POPUP MENU SECTION ###################

    def _save_translation(self):
        """Saving translation Data to file"""
        if self._preview_mode:
            screenmessage(message=(get_lang_text("saveLangIsInPreview") + f" {get_random_sad_emoji()}"), color=COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
            return

        data = self._translate_texts if not self._is_editing_new_lang else self._new_translate_texts

        reformated_data: Dict[str, str] = {}
        for key, val in data.items():
            if not key or key == "":
                continue
            edited_text = "\n".join(bui.textwidget(query=widget) for widget in self._translation_text_widgets[key])
            if val.get(self._current_lang_id) is None:
                continue
            if edited_text != val[self._current_lang_id]:
                reformated_data[key] = edited_text

        if not self._is_editing_new_lang:
            file_data = load_custom_translated_text(self._current_lang_id) or {}
        else:
            file_data = load_new_translated_text(self._current_lang_id, self._current_new_language)

        for key, val in file_data.items():
            if key not in reformated_data:
                reformated_data[key] = val

        if not reformated_data:
            screenmessage('No Translation Data To Be Saved', COLOR_SCREENCMD_ERROR)
            print("No Translation Data To Be Saved")
            return

        if not self._data_different_from_file(file_data, reformated_data):
            screenmessage('Translation Data Not Changed', COLOR_SCREENCMD_ERROR)
            print("Translation Data Not Changed")
            return

        for key, val in reformated_data.items():
            self._translate_texts[key][self._current_lang_id] = val

        if not self._is_editing_new_lang:
            save_custom_translated_text(reformated_data, self._current_lang_id)
        else:
            for key, val in reformated_data.items():
                self._new_translate_texts[key][self._current_lang_id] = val
            save_new_translated_text(reformated_data, self._current_lang_id, self._current_new_language)


    def _save_original_data(self):
        reformated_data: Dict[str, str] = {}
        for key, val in self._translate_texts.items():
            if not key or key == "": continue
            the_lang_edited = "\n".join(bui.textwidget(query=widget) for widget in self._translation_text_widgets[key])
            if the_lang_edited != val[self._current_lang_id]:
                reformated_data[key] = the_lang_edited

        if reformated_data:
            data = load_custom_translated_text(self._current_lang_id)

            if data and not self._data_different_from_file(data, reformated_data):
                print(f"Original Customized Translated Text Data is Same")
                return

            if data:
                data.update(reformated_data)

            for key, val in reformated_data.items():
                self._translate_texts[key][self._current_lang_id] = val
            save_custom_translated_text(reformated_data, self._current_lang_id)
        else:
            print(f"Original Customized Translated Text Data is Same #2")

    def _data_different_from_file(self, data: Dict[str, str], reformated_data: Dict[str, str]) -> bool:
        """
        Periksa apakah ada perbedaan antara data dari file dengan data yang sedang diubah.

        :param data: Data asli dari file.
        :param reformated_data: Data baru yang sedang diedit.
        :return: `True` jika ada perubahan, `False` jika tidak.
        """
        if not data and not reformated_data:
            return False

        if list(data.items()) != list(reformated_data.items()):
            return True

        for key, val in data.items():
            if key in reformated_data and val != reformated_data[key]:
                return True
        return False


    def _is_data_edited_on_textwidget(self, data: Dict[str, dict[str, str]]) -> bool:
        """
        Checks if any of the translation text widgets have been edited.
        """
        if not data: return False
        for key, val in data.items():
            if key:
                edited_text = "\n".join(bui.textwidget(query=widget) for widget in self._translation_text_widgets[key])
                if val.get(self._current_lang_id) is None:
                    continue
                if edited_text != val[self._current_lang_id]:
                    return True
        return False

    def _exit_without_save(self):
        self._transition_out(False)

    def _transition_out(self, saving: bool = True) -> None:
        if saving:
            if self._is_editing_new_lang:
                is_changed = self._is_data_edited_on_textwidget(self._new_translate_texts)
                if is_changed:
                    self._confirm_exit_without_saving()
                    return
            else:
                is_changed = self._is_data_edited_on_textwidget(self._translate_texts)
                if is_changed:
                    self._confirm_exit_without_saving()
                    return

        bui.getsound('swish').play()
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        load_and_update_tranlataion_data()

    def on_popup_cancel(self) -> None:
        self._transition_out()

class EditableDataPopup(popup.PopupWindow):
    """
    Simple Dict/List Data Editor
    
    Formats Accepted (From Func Returns):

    `Dict[str, str]`

    `List[str]`
    """
    def __init__(
            self,
            load_func: Callable[[], List[str] | Dict[str, str]],
            save_func_list: Optional[Callable[[List[str]], None]] = None,
            save_func_dict: Optional[Callable[[Dict[str, str]], None]] = None,
            is_player: bool = False,
            label: str = ""):
        self._data: List[str] | Dict[str, str] = load_func()

        self._load_data = load_func
        self._save_list = save_func_list
        self._save_dict = save_func_dict

        self._is_player = is_player

        self._uiscale : babase.UIScale = bui.app.ui_v1.uiscale

        self._refresh_delay: float = 3
        self._is_refreshing: bool  = False

        ### Popup Types XD ###
        self._popup_type = ""
        ### Popup Types XD ###

        self.bg_color = (.25, .05, .35)
        self._width = 950
        self._height = 625
        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=1.0,
            bg_color=self.bg_color
        )

        if not self._data:
            self._transition_out()
            screenmessage(message=get_lang_text('editablePopUpInvalidDataType') + f" {self._data}", color=COLOR_SCREENCMD_ERROR)
            return

        elif isinstance(self._data, list):
            if not self._save_list or not callable(self._save_list):
                self._transition_out()
                screenmessage(message=get_lang_text('editablePopUpInvalidSaveFuncList'), color=COLOR_SCREENCMD_ERROR)
                return

        elif isinstance(self._data, dict):
            if not self._save_dict or not callable(self._save_dict):
                self._transition_out()
                screenmessage(message=get_lang_text('editablePopUpInvalidSaveFuncDict'), color=COLOR_SCREENCMD_ERROR)
                return

        self._text_label = label

        self._text_widgets: List[bui.Widget] = []
        self._pressed_textwidget: Optional[bui.Widget] = None
        self._pressed_textwidget_text: Optional[str] = None

        self._selected_index_text = get_lang_text('dataPopupSelectedIndex')

        self._data_counter_splitter = ". "
        self._dict_key_val_splitter_viewer = " >> "
        self._dict_key_val_splitter = ":"


        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.6,
            color=bui.app.ui_v1.title_color,
            text=label
        )

        self.scrollwidget_width = self._width*0.775
        self.scrollwidget_x_tilt = 75
        self._edit_text_widget = bui.textwidget(
            parent=self.root_widget,
            editable=True,
            size=(self.scrollwidget_width, 40),
            position=(self.scrollwidget_x_tilt, 37.5),
            text='',
            maxwidth=self.scrollwidget_width,
            shadow=0.3,
            flatness=1.0,
            autoselect=True,
            v_align='center'
        )

        b_textcolor = (0.4, 0.75, 0.5)

        self._add_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.885, self._height*0.3),
            size=(100, 100),
            label='',
            on_activate_call=self._add_to_data,
            button_type='square',
            color=self.bg_color,
            textcolor=b_textcolor,
            icon=bui.gettexture('powerupHealth'),
            iconscale=2.25,
            enable_sound=False,
            autoselect=False
        )
        bui.textwidget(edit=self._edit_text_widget, on_return_press_call=self._add_button.activate)

        self._edit_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.885, self._height*0.5),
            size=(100, 100),
            label='',
            icon=bui.gettexture('replayIcon'),
            iconscale=2.25,
            on_activate_call=self._edit_data,
            button_type='square',
            color=self.bg_color,
            textcolor=b_textcolor,
            enable_sound=False,
            autoselect=False
        )

        self._delete_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.885, self._height*0.7),
            size=(100, 100),
            label='',
            icon=bui.gettexture('crossOut'),
            iconscale=2.25,
            on_activate_call=self._delete_data,
            button_type='square',
            color=self.bg_color,
            textcolor=b_textcolor,
            enable_sound=False,
            autoselect=False
        )

        self._selected_index_textwidget = bui.textwidget(
            parent=self.root_widget,
            size=(len(self._selected_index_text.splitlines()[0]) * 10, 50),
            position=(self._width * 0.865, self._height*0.2),
            scale=0.825,
            text=self._selected_index_text.format('1'),
            editable=False,
            selectable=True,
            always_highlight=True,
            autoselect=True,
            click_activate=True, # Make sure to one click activates it ;-;
            on_activate_call=self._on_index_selected_press,
            h_align='center',
            v_align='center',
            maxwidth=self.scrollwidget_width,
        )

        self._copy_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.scrollwidget_width+self.scrollwidget_x_tilt+20, 52.5),
            size=(30, 30),
            label='©',
            button_type='backSmall',
            color=self.bg_color,
            textcolor=b_textcolor,
            on_activate_call=self._copy_text,
            autoselect=True,
            enable_sound=False
        )

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(27.5, self._height - 48),
            size=(50, 50),
            scale=1,
            label='',
            color=self.bg_color,
            on_activate_call=self._transition_out,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)

        self.scrollwidget: Optional[bui.Widget] = None
        self.data_container: Optional[bui.Widget] = None

        self._up_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(-20, self._height * 0.55),
            size=(90, 90),
            text_scale=1.2,
            label=babase.charstr(SpecialChar.UP_ARROW),
            on_activate_call=self._move_up,
            button_type='square',
            color=self.bg_color,
            textcolor=b_textcolor,
            enable_sound=True,
            autoselect=False,
            repeat=True
        )

        self._down_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(-20, self._height * 0.4),
            size=(90, 90),
            text_scale=1.2,
            label=babase.charstr(SpecialChar.DOWN_ARROW),
            on_activate_call=self._move_down,
            button_type='square',
            color=self.bg_color,
            textcolor=b_textcolor,
            enable_sound=True,
            autoselect=False,
            repeat=True
        )


        self.scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            size=(self.scrollwidget_width, self._height * 0.8),
            position=(self.scrollwidget_x_tilt, self._height * 0.125),
            color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2), # Scroller color
            highlight=False
        )

        self._refresh_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self.scrollwidget_width+self.scrollwidget_x_tilt+75, 52.5),
            size=(40, 40),
            label='',
            color=self.bg_color,
            on_activate_call= self._refresh_data,
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.2)

        if self._is_player:
            button_size = 55
            self._player_list_popup = bui.buttonwidget(
                parent=self.root_widget,
                position=(7.5, self._height * 0.2),
                size=(button_size, button_size),
                label='',
                color=self.bg_color,
                on_activate_call= self._open_player_list_popup,
                autoselect=False,
                icon=bui.gettexture('achievementSharingIsCaring'),
                iconscale=1.2
            )

            self._player_info_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(7.5, self._height * 0.1),
                size=(button_size, button_size),
                label='',
                on_activate_call=self._on_player_info_press,
                button_type='square',
                color=self.bg_color,
                textcolor=b_textcolor,
                enable_sound=True,
                autoselect=False,
                repeat=False,
                icon=bui.gettexture('cuteSpaz'),
                iconscale=1.2
            )

        bui.containerwidget(
            edit=self.root_widget,
            color=self.bg_color,
            cancel_button=self._cancel_button)
        self._refresh_view()

    def _refresh_data(self):
        if self._is_refreshing:
            screenmessage(f'Whoa, Slowdown Pal {get_random_happy_emoji()}', color=COLOR_SCREENCMD_NORMAL)
            return

        self._data = self._load_data()
        self._refresh_view()
        self._is_refreshing = True
        screenmessage(f"Data Reloaded {get_random_happy_emoji()}", color=COLOR_SCREENCMD_NORMAL)
        babase.apptimer(self._refresh_delay, self._reset_refreshing)

    def _reset_refreshing(self):
        self._is_refreshing = False

    def _refresh_view(self, selected_index: Optional[int] = None, selected_text: bool = False):
        if self.scrollwidget and self.data_container:
            self.data_container.delete()

        self.data_container = bui.columnwidget(
            parent=self.scrollwidget,
            border=2,
            margin=0
        )

        for widget in self._text_widgets:
            widget.delete()
        self._text_widgets.clear()

        if isinstance(self._data, list):
            for i, item in enumerate(self._data):
                self._create_text_widget(f"{str(i+1)}{self._data_counter_splitter}{item}")
        elif isinstance(self._data, dict):
            for i, (key, value) in enumerate(self._data.items()):
                self._create_text_widget(f"{str(i+1)}{self._data_counter_splitter}{key}{self._dict_key_val_splitter_viewer}{value}")

        if not self._data: selected_index=None
        if selected_index is not None:
            if selected_text:
                text: str = bui.textwidget(query=self._text_widgets[selected_index])
                self._pressed_textwidget = self._text_widgets[selected_index]
                self._pressed_textwidget_text = text.split(self._data_counter_splitter, 1)[1]

                text_view = text.replace(f"{self._dict_key_val_splitter_viewer}", self._dict_key_val_splitter).split(self._data_counter_splitter, 1)[1]
                bui.textwidget(edit=self._edit_text_widget, text=text_view)
            if selected_index > -1:
                bui.columnwidget(
                    edit=self.data_container,
                    selected_child=self._text_widgets[selected_index],
                    visible_child=self._text_widgets[selected_index]
                )
            bui.textwidget(edit=self._selected_index_textwidget, text=self._selected_index_text.format(str(selected_index+1)))
        else:
            if self._data:
                text: str = bui.textwidget(query=self._text_widgets[0])
                self._pressed_textwidget = self._text_widgets[0]
                self._pressed_textwidget_text = text.split(self._data_counter_splitter, 1)[1]

                text_view = text.replace(f"{self._dict_key_val_splitter_viewer}", self._dict_key_val_splitter).split(self._data_counter_splitter, 1)[1]
                bui.textwidget(edit=self._edit_text_widget, text=text_view)
            else:
                self._pressed_textwidget_text = None
                self._pressed_textwidget = None


    def _on_index_selected_press(self):
        if self._pressed_textwidget_text and self._pressed_textwidget:
            screenmessage(f"[{self._pressed_textwidget_text}]", COLOR_SCREENCMD_NORMAL)
            selected_index = self._text_widgets.index(self._pressed_textwidget)
            widget = self._text_widgets[selected_index]
            bui.columnwidget(
                edit=self.data_container,
                selected_child=widget,
                visible_child=widget
            )
            bui.containerwidget(
                edit=self.root_widget,
                color=self.bg_color,
                selected_child=widget,
                visible_child=widget)

    def _on_textwidget_pressed(self, text: str, widget: bui.Widget):
        self._pressed_textwidget = widget
        self._pressed_textwidget_text = text.split(self._data_counter_splitter, 1)[1]

        text_view = text.replace(f"{self._dict_key_val_splitter_viewer}", self._dict_key_val_splitter).split(self._data_counter_splitter, 1)[1]
        bui.textwidget(edit=self._edit_text_widget, text=text_view)

        selected_index = self._text_widgets.index(self._pressed_textwidget) + 1
        bui.textwidget(edit=self._selected_index_textwidget, text=self._selected_index_text.format(str(selected_index)))

    def _on_player_info_press(self):
        player_name: str = bui.textwidget(query=self._edit_text_widget)
        if player_name in all_names:
            PlayerInfoPopup(player_name)
        else:
            self._player_not_exist(player_name)

    def _open_player_list_popup(self):
        PlayerListPopup(all_names)

    ### GUI INFORM ###
    def _player_not_exist(self, name: str):
        screenmessage(get_lang_text('addAttributePlayerNotInData').format(name), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    ### GUI INFORM ###

    def _copy_text(self):
        msg_to_copy = bui.textwidget(query=self._edit_text_widget)
        _copy_to_clipboard(msg_to_copy)

    def _move_up(self):
        """Move the selected item up."""
        if self._pressed_textwidget and self._pressed_textwidget_text:
            if isinstance(self._data, list):
                index = self._data.index(self._pressed_textwidget_text)
                if index > 0:
                    self._data[index], self._data[index - 1] = self._data[index - 1], self._data[index]
                    self._refresh_view(selected_index=index - 1, selected_text=True)

            elif isinstance(self._data, dict):
                key = self._pressed_textwidget_text.split(self._dict_key_val_splitter_viewer, 1)[0]
                items = list(self._data.items())
                index = next((i for i, (k, v) in enumerate(items) if k == key), None)
                if index is not None and index > 0:
                    items[index], items[index - 1] = items[index - 1], items[index]
                    self._data = dict(items)
                    self._refresh_view(selected_index=index - 1, selected_text=True)

              #      selected_index = index
                  #  bui.textwidget(edit=self._selected_index_textwidget, text=self._selected_index_text.format(str(selected_index)))

    def _move_down(self):
        """Move the selected item down."""
        if self._pressed_textwidget and self._pressed_textwidget_text:
            if isinstance(self._data, list):
                index = self._data.index(self._pressed_textwidget_text)
                if index < len(self._data) - 1:
                    self._data[index], self._data[index + 1] = self._data[index + 1], self._data[index]
                    self._refresh_view(selected_index=index + 1, selected_text=True)

            elif isinstance(self._data, dict):
                key = self._pressed_textwidget_text.split(self._dict_key_val_splitter_viewer, 1)[0]
                items = list(self._data.items())
                index = next((i for i, (k, v) in enumerate(items) if k == key), None)
                if index is not None and index < len(items) - 1:
                    items[index], items[index + 1] = items[index + 1], items[index]
                    self._data = dict(items)
                    self._refresh_view(selected_index=index + 1, selected_text=True)

                   # selected_index = index + 2
                  #  bui.textwidget(edit=self._selected_index_textwidget, text=self._selected_index_text.format(str(selected_index)))


    def _create_text_widget(self, text: str):
        widget = bui.textwidget(
            parent=self.data_container,
            size=(self.scrollwidget_width, 30),
            text=text,
            editable=False,
            selectable=True,
            always_highlight=True,
            autoselect=True,
            click_activate=True, # Make sure to one click activates it ;-;
            h_align='left',
            v_align='center',
            maxwidth=self.scrollwidget_width,
        )
        bui.textwidget(
            edit=widget,
            on_activate_call=Call(self._on_textwidget_pressed, text, widget)
        )
        self._text_widgets.append(widget)

    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return (1.6 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else
                2.0)

    ###### POPUP RELATED THINGS ######
    def _show_player_names_list_popup(self, data: Dict[str, dict[str, Any]]):
        choices = list(data.keys())
        choices.insert(0, "Did You Means:")

        self._popup_type = "perhapsPlayers"
        PopupMenuWindow(
            position=self._add_button.get_screen_space_center(),
            color=self.bg_color, # type: ignore
            scale=_get_popup_window_scale(),
            choices=choices,
         #   choices_display=_create_baLstr_list(choices_display),
            current_choice=choices[1 if len(choices) >= 2 else -1],
            choices_disabled=[choices[0]],
            delegate=self)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        if self._popup_type == "perhapsPlayers":
            # The choice is the players list
            if self._edit_text_widget and self._edit_text_widget.exists():
                bui.textwidget(edit=self._edit_text_widget, text=choice)

        self._popup_type = ""
        del popup_window

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""
    ###### POPUP RELATED THINGS ######

    def _add_to_data(self):
        """Add A Data"""
        new_text: str = bui.textwidget(query=self._edit_text_widget)
        bui.containerwidget(
            edit=self.root_widget,
            color=self.bg_color,
            selected_child=self._edit_text_widget)

        if not new_text:
            self._add_empty()
            return

        selected_index: Optional[int] = None

        if self._is_player:
            if not (new_text in all_names and new_text.strip() in all_names):
                perhaps_players = _group_matched_players(all_names, sanitize_name(new_text), False)
                if perhaps_players:
                    self._show_player_names_list_popup(perhaps_players)
                else:
                    self._player_not_exist(new_text)
                return

        # For List Data
        if isinstance(self._data, list):
            if new_text not in self._data:
                if self._pressed_textwidget_text:
                    selected_index = self._data.index(self._pressed_textwidget_text)
                    self._data.insert(selected_index + 1, new_text)  # Insert below the selected item
                else:
                    selected_index = len(self._data) - 1
                    self._data.append(new_text)  # If nothing is selected, add to the end
                self._add_success()
                self._refresh_view(selected_index=selected_index + 1, selected_text=True)
            else:
                self._add_exists()

        # For Dictionary Data
        elif isinstance(self._data, dict):
            spl = self._dict_key_val_splitter
            if spl not in new_text:
                screenmessage(get_lang_text('addAttribteNoSplitter').format(spl), COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return

            new_key, new_value = map(str, new_text.split(spl, 1))
            new_key = new_key.strip()
            new_value = new_value.strip()

            if not new_value or not new_key:
                self._add_empty()
                return

            if any(old_key in new_key for old_key in list(self._data.keys())):
                self._add_exists()
                return

            if new_key not in self._data:
                data_list = list(self._data.items())
                index = None
                if self._pressed_textwidget_text:
                    current_key = self._pressed_textwidget_text.split(self._dict_key_val_splitter_viewer, 1)[0].strip()
                    index = next((i for i, (k, v) in enumerate(data_list) if k == current_key), None)
                    if index is not None:
                        data_list.insert(index + 1, (new_key, new_value))  # Insert below the selected item
                    else:
                        data_list.append((new_key, new_value))
                        index = len(data_list) - 2
                else:
                    data_list.append((new_key, new_value))  # Add to the end if nothing is selected
                    index = len(data_list) - 2
                self._data = dict(data_list)  # Reconstruct the dictionary
                self._add_success()
                self._refresh_view(selected_index=index + 1, selected_text=True)
            else:
                self._add_exists()

    ### GUI INFORM ###
    def _add_success(self):
     #   bui.textwidget(edit=self._edit_text_widget, text='')
        screenmessage(get_lang_text('addSuccess'), COLOR_SCREENCMD_NORMAL)
        bui.getsound('shieldUp').play(1.5)
    def _add_exists(self):
        screenmessage(get_lang_text('editAttributeExist'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    def _add_empty(self):
        screenmessage(get_lang_text('editAttributeAddEmpty'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    ### GUI INFORM ###


    def _edit_data(self):
        """Edit Selected Data"""
        selected_index: Optional[int] = None
        bui.containerwidget(
            edit=self.root_widget,
            color=self.bg_color,
            selected_child=self._edit_text_widget)
        if not self._pressed_textwidget or not self._pressed_textwidget_text:
            self._edit_empty()
            return
        updated_text: str = bui.textwidget(query=self._edit_text_widget)
        if updated_text == self._pressed_textwidget_text:
            self._edit_same()
            return
        if not updated_text:
            self._edit_empty()
            return

        if self._is_player:
            if not (updated_text in all_names and updated_text.strip() in all_names):
                perhaps_players = _group_matched_players(all_names, sanitize_name(updated_text), False)
                if perhaps_players:
                    self._show_player_names_list_popup(perhaps_players)
                else:
                    self._player_not_exist(updated_text)
                return

        if isinstance(self._data, list):
            index = self._data.index(self._pressed_textwidget_text)
            self._data[index] = updated_text # Main
            selected_index = index
            self._refresh_view(selected_index=selected_index, selected_text=True)
            self._edit_success()
        elif isinstance(self._data, dict):
            spl = self._dict_key_val_splitter
            #### Exit ####    
            if spl not in updated_text:
                screenmessage(get_lang_text('addAttribteNoSplitter').format(spl), COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return
            new_key, new_value = map(str, updated_text.split(spl, 1))
            if not new_value.strip() or not new_key.strip():
                self._edit_empty()
                return
            #### Exit ####

            old_key = self._pressed_textwidget_text.split(self._dict_key_val_splitter_viewer, 1)[0]
          #  print(f"{old_key} -> {key}")
            if old_key == new_key:
                if self._data[old_key] == new_value:
                    self._edit_exist()
                    return
                self._data[new_key] = new_value # Main
            else:
                data_list = list(self._data)
                if any(data_list[i] in new_key for i, k in enumerate(self._data)):
                    self._edit_exist()
                    return
                self._data = { # Main
                    k if k != old_key else new_key: v if k != old_key else new_value
                    for k, v in self._data.items()
                }
            index = self._text_widgets.index(self._pressed_textwidget)
            selected_index = index
            self._refresh_view(selected_index=selected_index, selected_text=True)
            self._edit_success()

    ### GUI INFORM ###
    def _edit_success(self):
        screenmessage(get_lang_text('editSuccess'), COLOR_SCREENCMD_NORMAL)
        bui.getsound('shieldUp').play(1.5)
    def _edit_exist(self):
        screenmessage(get_lang_text('editExist'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    def _edit_same(self):
        screenmessage(get_lang_text('editAttributeSame'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    def _edit_empty(self):
        screenmessage(get_lang_text('editAttributeEmpty'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    ### GUI INFORM ###


    def _delete_data(self):
        """Delete Selected Data"""
        selected_index: Optional[int] = None
        if self._pressed_textwidget and self._pressed_textwidget_text:
            if isinstance(self._data, list):
                self._data.remove(self._pressed_textwidget_text) # Main
            elif isinstance(self._data, dict):
                key = self._pressed_textwidget_text.split(self._dict_key_val_splitter_viewer, 1)[0]
                del self._data[key] # Main
            index = self._text_widgets.index(self._pressed_textwidget)
            selected_index = max(0, index - 1)
            self._refresh_view(selected_index=selected_index, selected_text=True)
            self._delete_success()
        else:
            self._delete_empty()

    ### GUI INFORM ###
    def _delete_success(self):
      #  screenmessage(get_lang_text('removeSuccess'), COLOR_SCREENCMD_NORMAL)
        bui.getsound('shieldDown').play(1.5)
    def _delete_empty(self):
        screenmessage(get_lang_text('editAttributeDeleteEmpty'), COLOR_SCREENCMD_ERROR)
        bui.getsound('error').play(1.5)
    ### GUI INFORM ###

    def _transition_out(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        data = self._load_data()

        if data is None or self._data is None:
            return

        if list(data) == list(self._data):
            print('Oops, No Changes Made To Data')
            return

        if isinstance(self._data, list):
            if self._save_list:
                self._save_list(self._data)
                print(f"List Data Saved: {self._save_list.__name__}")

        elif isinstance(self._data, dict):
            if self._save_dict:
                self._save_dict(self._data)
                print(f"Dict Data Saved: {self._save_dict.__name__}")

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()


class InternalChatsPopup(popup.PopupWindow):
    """Popup Window for Internal Chats Data with Popup"""
    def __init__(self, label: str = "???"):
        """Popup Window for Internal Chats Data with Popup"""
        self._list_data = load_internal_all_chats_data()
        self._list_data_func = load_internal_all_chats_data
        self._text_label = label
        self._popup_type = ''
        self._popup_party_member_client_id: Optional[int] = None
        self._popup_party_member_is_host: Optional[bool] = False
        self.chats_per_page = maximum_bombsquad_chat_messages

        self.chats_per_page = maximum_bombsquad_chat_messages # Use the default maximum party window chats each pages
        self.current_page = (len(self._list_data) - 1) // self.chats_per_page # Automatically show last page of the chats
        self.total_pages = (len(self._list_data) - 1) // self.chats_per_page + 1

        self._width = 950
        self._height = 625
        self.bg_color = party_config.get(CFG_NAME_MAIN_COLOR, bui.app.ui_v1.heading_color)
        self._transitioning_out = False
        self._text_widgets = []
        uiscale = bui.app.ui_v1.uiscale

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(2.06 if uiscale is babase.UIScale.SMALL else 1.4 if uiscale is babase.UIScale.MEDIUM else 1.0),
            bg_color=self.bg_color
        )

        self._label = bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.6,
            color=bui.app.ui_v1.title_color,
            text=self._text_label
        )

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(55, self._height - 63),
            size=(55, 55),
            scale=.875,
            label='',
            color=self.bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2
        )

        if len(self._list_data) > self.chats_per_page:
            self._page_text = bui.textwidget(
                parent=self.root_widget,
                position=(self._width * 0.785, self._height - 62.5),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}",
                color=bui.app.ui_v1.title_color
            )
            self._prev_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.75, self._height - 575),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._previous_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )
            self._next_button = bui.buttonwidget(
                parent=self.root_widget,
                position=(self._width * 0.875, self._height - 575),
                size=(100, 40),
                scale=1,
                label="",
                on_activate_call=self._next_page,
                autoselect=False,
                repeat=True,
                color=self.bg_color
            )

        self._is_refreshing = False
        self._refresh_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width * 0.9, self._height * 0.875),
            size=(40, 40),
            label='',
            color=self.bg_color,
            on_activate_call= Call(self._refresh, self._list_data_func),
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.2)

        self._show_page(self.current_page)

    def _refresh(self, data =None):
        if data is not None:
            try:
                if isinstance(data, (list)):
                    self._list_data = data
                    self._show_page(self.current_page, is_refresh=True)
                else:
                    if self._is_refreshing:
                        screenmessage(f'Cooldown A Bit Pal {get_random_happy_emoji()}', color=COLOR_SCREENCMD_NORMAL)
                        return
                    self._is_refreshing = True
                    babase.apptimer(1.75, Call(self._reset_refresh))
                    self._list_data = data()
                    screenmessage('Data Refreshed', color=COLOR_SCREENCMD_NORMAL)
                    self._show_page(self.current_page, is_refresh=True)
            except Exception as e:
                print_internal_exception(e)

    def _reset_refresh(self):
        self._is_refreshing = False

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._show_page(self.current_page)
        else:
            self.current_page = 0
            self._show_page(self.current_page)

    def _previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
        else:
            self.current_page = (len(self._list_data) - 1) // self.chats_per_page
            self._show_page(self.current_page)

    def _show_page(self, page, is_refresh:bool=False):
        height = self._height * 0.725
        width = self._width
        if not is_refresh:
            if hasattr(self, 'scrollwidget'): self.scrollwidget.delete()
            self.scrollwidget = bui.scrollwidget(
                parent=self.root_widget,
                size=(width, height),
                position=(10, 90),
                color=(self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2),
                highlight=False)
            if hasattr(self, 'chat_container'): self.chat_container.delete()
            self.chat_container = bui.columnwidget(parent=self.scrollwidget, border=2, margin=0)
        else:
            self.chat_container.delete()
            self.chat_container = bui.columnwidget(parent=self.scrollwidget, border=2, margin=0)

        start_index = page * self.chats_per_page
        end_index = start_index + self.chats_per_page
        if isinstance(self._list_data, list):
            for i, text in enumerate(self._list_data[start_index:end_index]):
                self._create_text_widget(i, text)
        else:
            print(f'Unhandled ListPopup Type: {type(self._list_data)}')

    def _create_text_widget(self, i: int, text: str):
        text_widget = bui.textwidget(
            parent=self.chat_container,
            size=(self._width, 22.5),
            text=text,
            maxwidth=self._width * 0.975,
            scale=1,
            h_align='left',
            v_align='center',
            selectable=True,
            autoselect=False,
            click_activate=True,
            always_highlight=True,
            color=(0.8, 0.8, 0.8) if not text.startswith(CMD_LOGO_SERVER) else (self.bg_color[0]+0.2, self.bg_color[1]+0.2, self.bg_color[2]+0.2)
        )
        if len(self._list_data) > self.chats_per_page:
            bui.textwidget(edit=self._page_text, text=f"{get_lang_text('page')}: {self.current_page + 1} / {self.total_pages}")

        bui.textwidget(
            edit=text_widget,
            on_activate_call=Call(self._on_internal_chats_data_pressed, text, text_widget) if not text.startswith('[SERVER]') else Call(self._confirm_copy, text))
        self._text_widgets.append(text_widget)

    def _confirm_copy(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 10
        else:
            width = len(text) * 10
            text_title = text
        ConfirmWindow(
            origin_widget=self.root_widget,
            text=f"{get_lang_text('confirmCopy')}?\n{text_title}",
            width= width,
            height=135,
            action=Call(_copy_to_clipboard, text),
            cancel_is_selected=True,
            cancel_text=get_lang_text('cancel'),
            text_scale=1,
            ok_text=get_lang_text('copy')
        )

    def _on_internal_chats_data_pressed(self, text: str, widget: bui.Widget = None):
        self._pressed_textwidget = widget
        self._pressed_textwidget_text = text

        name, message = bui.textwidget(query=widget).split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
        if ' ' in name:
            name: str = name.split(' ', 1)[0]
        choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_CHAT_PRESS)

        # Using current session may cause less accurate current player
        # current_namelist if bs.get_connection_to_host_info_2() else all_names

        # Show on party member press
        if name != "...":
            player_acc = _match_player_name(player_name=name, player_data=all_names)
            if all_names.get(player_acc):
                choices_key.append('playerMenuOptionFromText')
                choices_display.append(get_lang_text('playerMenuOptionFromText'))
                self._popup_party_member_client_id = all_names.get(player_acc, {}).get('client_id')
                if self._popup_party_member_client_id == -1:
                    self._popup_party_member_is_host = True
                else:
                    self._popup_party_member_is_host = False
            else:
                pass #self._refresh_text()

        self.uiscale : babase.UIScale = bui.app.ui_v1.uiscale
        self._popup_type = POPUP_MENU_TYPE_CHAT_PRESS
        pos: tuple[float, float] = widget.get_screen_space_center()
        pos = (pos[0]*25, pos[1])
        PopupMenuWindow(
            position=pos,
            color=self.bg_color, # type: ignore
            scale= _get_popup_window_scale(),
            choices=choices_key,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices_key[0],
            delegate=self)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        if self._popup_type == POPUP_MENU_TYPE_CHAT_PRESS:
            pname = ''
            current_text = ''
            player_acc = ''
            player_profiles = []
            player_client_id = 0
            current_textwidget_text = ''
            if not choice == 'copyText' and not choice == 'translateText':
                if self._pressed_textwidget_text:
                    pname, current_text = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                    if ' ' in pname:
                        pname = pname.split(' ', 1)[0].strip()
                current_textwidget_text = self._pressed_textwidget_text
                current_textwidget: bui.Widget = self._pressed_textwidget
        #       current_text = self._pressed_textwidget_text
                if self._pressed_textwidget_text:
                    player_data = all_names
                    player_acc: str = pname if player_data.get(pname) else _match_player_name(pname, player_data)
                    player_profiles: list[str] = player_data.get(player_acc, {}).get('profile_name', [])
                    player_client_id: int | None = player_data.get(player_acc, {}).get('client_id')
                    self._popup_party_member_client_id = player_client_id
                    if player_client_id == -1:
                        self._popup_party_member_is_host = True
                    else:
                        self._popup_party_member_is_host = False
                else:
                    player_acc = ''
                    player_profiles = []
            if choice == 'playerMenuOptionFromText':
                if player_client_id is None:
                    pass#return
                self._on_party_member_press(player_client_id, (False if not player_client_id == -1 else True), popup_window.root_widget, player_acc)

            elif choice == 'copyText':
                _copy_to_clipboard(self._pressed_textwidget_text)

            elif choice == 'translateText':
                pname, current_text = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                self._translate_textwidget(current_text, self._pressed_textwidget)

            elif choice == 'insertText':
                if current_textwidget_text:
                    msg = (
                        current_text if not party_config[CFG_NAME_INCLUDE_PNAME_ON_CHOSEN_TEXT] or pname.strip() == '...' else
                        str('/'.join(player_profiles) if player_profiles else pname) + PNAME_AND_MSG_SPLITTER + current_text
                    )
                    _edit_text_field_global(msg, 'add')

        elif self._popup_type == POPUP_MENU_TYPE_PARTY_MEMBER_PRESS:
            # Manual searching player data from saved text widget text
            if self._pressed_textwidget_text:
                pname, chats = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                if ' ' in pname:
                    pname = pname.split(' ', 1)[0].strip()
            else:
                return
            player_data = all_names
            current_textwidget_text = self._pressed_textwidget_text
            current_textwidget: bui.Widget = self._pressed_textwidget
            player_acc: str = pname if player_data.get(pname) else _match_player_name(pname, player_data)
            pdata = player_data.get(player_acc, {})
            if pdata:
                account_name: str   = player_acc
                client_id: int      = pdata.get('client_id', 0)

                profiles: list[str] = pdata.get('profile_name', [])
                profiles_joint: str = ', '.join(profiles) if profiles else ''
                self._popup_party_member_client_id = client_id
                if client_id == -1:
                    self._popup_party_member_is_host = True
                else:
                    self._popup_party_member_is_host = False
            else: return

            if choice == 'votekick':
                # kick-votes appeared in build 14248
                host_info = bs.get_connection_to_host_info_2()
                if host_info is not None and host_info.build_number < 14248:
                    return
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                vote_kick_confirm_text = get_lang_text('voteKickConfirm')
                confirm_text = f'{vote_kick_confirm_text}\n{name}?'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=len(vote_kick_confirm_text) * 10,
                    height=150,
                    action=self._vote_kick_player,
                    cancel_button=True,
                    cancel_is_selected=True,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('yes'),
                    text_scale=1.0,
                    origin_widget=self.root_widget)

            elif choice == 'mention':
                # Mention Player By Adding Its Chosen Name Into Text Field
                _names_list: List[str] = []

                _names_list.append(account_name)
                if profiles: _names_list += profiles

                choices: List[str] = []
                names_list: List[str] = []

                for name in _names_list:
                    names_list.append(name)
                    if '"' in name: name = name.replace('"', '\\"')
                    if "'" in name: name = name.replace("'", "\\'")

                    choices.append('_edit_text_field_global("{name}", "add")'.format(name=name))

                names_display = _create_baLstr_list(names_list)

                self._popup_type = POPUP_MENU_TYPE_EXECUTE_CHOICE
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices,
                    choices_display=names_display,
                    current_choice=choices[0],
                    delegate=self)

            elif choice == 'adminkick':
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                admin_kick_confirm_text = get_lang_text('adminKickConfirm')
                confirm_text = f'{admin_kick_confirm_text}?\n{name}'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=min((len(admin_kick_confirm_text) * 13.5), 600),
                    height=120,
                    action=Call(chatmessage, f'{KICK_CMD} {client_id}'),
                    cancel_button=True,
                    cancel_is_selected=True,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('yes'),
                    text_scale=1.0,
                    origin_widget=self.root_widget)

            elif choice == 'adminremove':
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                admin_remove_confirm_text = get_lang_text('adminRemoveConfirm')
                confirm_text = f'{admin_remove_confirm_text}?\n{name}'
                ConfirmWindow(
                    text=f'{confirm_text}',
                    width=min((len(admin_remove_confirm_text) * 13.5), 600),
                    height=120,
                    action=Call(chatmessage, f'{REMOVE_CMD} {client_id}'),
                    cancel_button=True,
                    cancel_is_selected=True,
                    cancel_text=get_lang_text('cancel'),
                    ok_text=get_lang_text('yes'),
                    text_scale=1.0,
                    origin_widget=self.root_widget)

            elif choice == 'customCommands':
                choices: list[str] = []
                choices_display: list[str] = []
                name = account_name
                if profiles:
                    name = f'{account_name} | {profiles_joint}'

                cmds_prefix: List[str] = ['/', '?']
                for text in custom_commands:
                    if '$acc' in text.lower():
                        text = text.replace('$acc', account_name)
                    if '$cid' in text.lower():
                        text = text.replace('$cid', str(client_id))
                    if '$name' in text.lower():
                        profile = profiles_joint if profiles else account_name
                        text = text.replace('$name', profile)
                    text = replace_msg_emoji_var_with_emojis(text)

                    choices_display.append(text)

                    if '"' in text: text = text.replace('"', '\\"')
                    if "'" in text: text = text.replace("'", "\\'")

                    if any(text.startswith(cmd_prefix) for cmd_prefix in cmds_prefix):
                        if party_config.get(CFG_NAME_DIRECT_CUSTOM_CMD):
                            choices.append(f'chatmessage("{text}")')
                        else:
                            choices.append(f'_edit_text_field_global("{text}", "replace")')
                    else:
                        choices.append(f'_edit_text_field_global("{text}", "replace")')


                sort_text = get_lang_text('sortChoiceCmd')
                choices.insert(0, 'SortMessagesList(_load_custom_commands(), _save_custom_commands, "Sort/Edit Custom Commands", True)')
                choices_display.insert(0, f'*** {sort_text} ***')

              #  print(choices)
              #  print('\n', choices_display)
                self._popup_type = POPUP_MENU_TYPE_EXECUTE_CHOICE
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices[len(choices) - 2],
                    delegate=self)

            elif choice == 'addNew':
                AddNewChoiceWindow()

            elif choice == 'warnInfo':
                self._popup_type = POPUP_MENU_TYPE_WARN_SELECT
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_WARN_SELECT)
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices_key[0],
                    delegate=self)

            elif choice == 'playerInfo':
                if client_id == -1:
                    if profiles:
                        account_name = profiles[0]
                PlayerInfoPopup(account_name)

        elif self._popup_type == POPUP_MENU_TYPE_WARN_SELECT:

            if choice == 'partyPressWarnAdd':
                self._popup_type = POPUP_MENU_TYPE_ADD_WARN_TYPE
                choices_key, choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_ADD_WARN_TYPE)
                PopupMenuWindow(
                    position=popup_window.root_widget.get_screen_space_center(),
                    color=self.bg_color, # type: ignore
                    scale=_get_popup_window_scale(),
                    choices=choices_key,
                    choices_display=_create_baLstr_list(choices_display),
                    current_choice=choices_key[0],
                    delegate=self)

            elif choice == 'partyPressWarnDecrease':
                if self._pressed_textwidget_text:
                    pname, chats = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                    if ' ' in pname:
                        pname = pname.split(' ', 1)[0].strip()
                else:
                    return
                player_data = all_names
                current_textwidget_text = self._pressed_textwidget_text
                current_textwidget: bui.Widget = self._pressed_textwidget
                player_acc: str = _match_player_name(pname, player_data)
                pdata = player_data.get(player_acc, {})
                if pdata:
                    account_name: str   = player_acc
                    client_id: int      = pdata.get('client_id', 0)

                    profiles: list[str] = pdata.get('profile_name', [])
                    profiles_joint: str = ', '.join(profiles) if profiles else ''
                    self._popup_party_member_client_id = client_id
                    if client_id == -1:
                        self._popup_party_member_is_host = True
                    else:
                        self._popup_party_member_is_host = False
                else: return
                manual_decrease_warn(account_name, True)

        elif self._popup_type == POPUP_MENU_TYPE_ADD_WARN_TYPE:
            if self._pressed_textwidget_text:
                pname, chats = self._pressed_textwidget_text.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
                if ' ' in pname:
                    pname = pname.split(' ', 1)[0].strip()
            else:
                return
            player_data = all_names
            current_textwidget_text = self._pressed_textwidget_text
            current_textwidget: bui.Widget = self._pressed_textwidget
            player_acc: str = _match_player_name(pname, player_data)
            pdata = player_data.get(player_acc, {})
            if pdata:
                account_name: str   = player_acc
                client_id: int      = pdata.get('client_id', 0)

                profiles: list[str] = pdata.get('profile_name', [])
                profiles_joint: str = ', '.join(profiles) if profiles else ''
                self._popup_party_member_client_id = client_id
                if client_id == -1:
                    self._popup_party_member_is_host = True
                else:
                    self._popup_party_member_is_host = False
            else: return

            if choice == 'addWarnBetraying':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_betraying)

            elif choice == 'addWarnAbusing':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_abusing)

            elif choice == 'addWarnUnnecessaryVotes':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_kick_vote)

            elif choice == 'addWarnTeaming':
                manual_add_warn_popup(account_name, client_id, add_warn_msg_teaming)

        elif self._popup_type == POPUP_MENU_TYPE_EXECUTE_CHOICE:
            exec(choice)

        del popup_window

    def _get_popup_window_scale(self) -> float:
        uiscale = bui.app.ui_v1.uiscale
        return (2.4 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0)

    def _vote_kick_player(self):
        if self._popup_party_member_is_host:
            bui.getsound('error').play(1.5)
            cant_kick_host_text = get_lang_text('cantKickHost')
            screenmessage(
                cant_kick_host_text,
                color=COLOR_SCREENCMD_ERROR)
        else:
            assert self._popup_party_member_client_id is not None
            pinfo = get_player_info_with_cid(self._popup_party_member_client_id)
            if pinfo and pinfo['account'] in MY_MASTER:
                screenmessage(f"{get_lang_text('cantKickMaster')} {get_random_sad_emoji()}", COLOR_SCREENCMD_ERROR)
                bui.getsound('error').play(1.5)
                return

            # Ban for 5 minutes.
            result = bs.disconnect_client(
                self._popup_party_member_client_id, ban_time=5 * 60)
            if not result:
                bui.getsound('error').play(1.5)
                screenmessage(
                    babase.Lstr(resource='getTicketsWindow.unavailableText').evaluate(),
                    color=COLOR_SCREENCMD_ERROR)

    def popup_menu_closing(self, popup_window: PopupWindow) -> None:
        """Called when the popup is closing."""

    def _on_party_member_press(self, client_id: Optional[int], is_host: bool, widget: bui.Widget, player_name: str = '') -> None:
        # if we're the host, pop up 'kick' options for all non-host members
        if bs.get_foreground_host_session() is not None:
            pass
        else:
            pass

        uiscale = bui.app.ui_v1.uiscale
        choices, _choices_display = get_choices_key_lang_text(POPUP_MENU_TYPE_PARTY_MEMBER_PRESS)

        if not player_name and not client_id:
            screenmessage(f'{get_lang_text("cantFindInPlayerData").format(str(player_name))} :(', COLOR_SCREENCMD_NORMAL)
            return

        choices_display: list[str] = []
        for i, choice_display in enumerate(_choices_display):
            if choice_display == get_lang_text('votekick'):
                if not current_namelist.get(player_name) or is_host:
                    choices.remove('votekick')
                    continue

            elif choice_display == get_lang_text('adminkick'):
                if not current_namelist.get(player_name) or is_host:
                    choices.remove('adminkick')
                    continue
                choice_display = choice_display.format(client_id)

            elif choice_display == get_lang_text('adminremove'):
                if not current_namelist.get(player_name) or is_host:
                    choices.remove('adminremove')
                    continue
                choice_display = choice_display.format(client_id)

            elif choice_display == get_lang_text('warnInfo'):
                if client_id == -1 or is_host:
                    choices.remove('warnInfo')
                    continue
                global player_warnings
                info = get_player_info_with_cid(clientID=client_id)
                if not info and not player_name:
                    choices.remove('warnInfo')
                    continue

                name = info['account'] if info else player_name
                if '"' in name: name = name.replace('"', '\\"')
                if "'" in name: name = name.replace("'", "\\'")
                player_warning = player_warnings.get(name, 0)
                choice_display = choice_display.format(player_warning)

            elif choice_display == get_lang_text('customCommands'):
                if not current_namelist.get(player_name) or is_host:
                    choices.remove('customCommands')
                    continue
                choice_display = choice_display

            choices_display.append(choice_display)

        self._popup_type = POPUP_MENU_TYPE_PARTY_MEMBER_PRESS
        PopupMenuWindow(
            position=widget.get_screen_space_center(),
            color=self.bg_color, # type: ignore
            scale=_get_popup_window_scale(),
            choices=choices,
            choices_display=_create_baLstr_list(choices_display),
            current_choice=choices[0],
            delegate=self)

    def _translate_textwidget(self, text_widget_text: str, text_widget: bui.Widget):
        """Translate the Pressed textwidget"""
        msg: str = bui.textwidget(query=text_widget)
        cleaned_msg = ''.join(filter(str.isalpha, text_widget_text))

        if not msg or not cleaned_msg or msg == '':
            screenmessage(f'{CMD_LOGO_CAUTION} ' + get_lang_text('translateEmptyText'), COLOR_SCREENCMD_ERROR)
            bui.getsound('error').play(1.5)
        else:
            screenmessage(get_lang_text('translating'), COLOR_SCREENCMD_NORMAL)
            name = ''
            if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                name, text = msg.split(PNAME_AND_MSG_SPLITTER_MODIFIED, 1)
            else:
                text = msg

            def _apply_translation(translated: str):
                if PNAME_AND_MSG_SPLITTER_MODIFIED in msg:
                    translate_text = name + PNAME_AND_MSG_SPLITTER_MODIFIED + translated
                else:
                    translate_text = translated
                if text_widget.exists():
                    bui.textwidget(edit=text_widget, text=translate_text)
            Translate(text=text, callback=_apply_translation)

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()


class CustomAccountViewerWindow(AccountViewerWindow):
    def __init__(self, account_name: str, account_data: Dict[str, Any], account_id: str = '') -> None:
        self._loading_spinner = None
        super().__init__(account_id=account_id)
        self.real_name = account_name
        self.custom_data = account_data
        self.pb_id = account_id
        self.shruggie = "¯\\_(ツ)_/¯"

    def _confirm_copy_text(self, text: str):
        max_width = 75
        if len(text) > max_width:
            text_title = '-\n'.join([text[i:i+max_width] for i in range(0, len(text), max_width)])
            width = max_width * 10
        else:
            width = len(text) * 10
            text_title = text
        if PNAME_AND_MSG_SPLITTER in text:
            text = text.split(PNAME_AND_MSG_SPLITTER, 1)[1]
            text_title = text_title.split(PNAME_AND_MSG_SPLITTER, 1)[1]
        if text_title != self.shruggie:
            ConfirmWindow(
                origin_widget=self.root_widget,
                text=f"{get_lang_text('confirmCopy')}?\n{text_title}",
                width= width,
                height=135,
                action=Call(_copy_to_clipboard, text),
                cancel_is_selected=True,
                text_scale=1,
                ok_text=get_lang_text('copy'),
                cancel_text=get_lang_text('cancel')
            )
        else:
            screenmessage(self.shruggie, COLOR_SCREENCMD_NORMAL)

    def _on_query_response(self, data):
        if data is None:
            bui.textwidget(
                edit=self._loading_text,
                text=babase.Lstr(resource='internal.unavailableNoConnectionText'),
            )
            if self._loading_spinner:
                babase.apptimer(0.5, self._loading_spinner.delete)
        else:
            try:
                self._loading_text.delete()
                trophystr = ''
                try:
                    trophystr = data['trophies']
                    num = 10
                    chunks = [
                        trophystr[i : i + num]
                        for i in range(0, len(trophystr), num)
                    ]
                    trophystr = '\n\n'.join(chunks)
                    if trophystr == '':
                        trophystr = '-'
                except Exception:
                    logging.exception('Error displaying trophies.')

                shruggie = self.shruggie
                # Menampilkan data dari custom_data
                if self.custom_data:
                    player_id: str | None = self.custom_data.get("_id")
                    player_other_acc: List[str] | None = self.custom_data.get("accounts")
                    player_premium_name: str = self.custom_data.get('current_premium_profile', [])
                    player_premium_names: List[str] = self.custom_data.get('current_premium_profiles', [])
                    player_acc_created_on: str | None = f"{self.custom_data['createdOn'][0:10]} | {self.custom_data['createdOn'][11:19]}" if self.custom_data.get('createdOn') else None
                    player_acc_updated_on: str | None = f"{self.custom_data['updatedOn'][0:10]} | {self.custom_data['updatedOn'][11:19]}" if self.custom_data.get('updatedOn') else None
                    player_discord: List[dict[str, str]] = self.custom_data.get('discord', [])
                    player_character: str | None = self.custom_data.get('spaz')
                    player_mutual_server: List[str] = self.custom_data.get('mutual_server', [])
                else:
                    self._on_cancel_press()
                    return
                if player_mutual_server and not isinstance(player_mutual_server, list):
                    player_mutual_server = [player_mutual_server]
                    global all_names
                    all_names[self.real_name]['mutual_server'] = player_mutual_server
                    _save_names_to_file()

                if player_other_acc and len(player_other_acc) != 0:
                    player_other_acc_joint = ", ".join([str(x) for x in player_other_acc]) 
                else:
                    player_other_acc_joint = shruggie

                if player_premium_names and len(player_premium_names) != 0:
                    player_premium_names_joint = ", ".join([str(x) for x in player_premium_names])
                else:
                    player_premium_names_joint = shruggie

                grouped_info = {
                    "IDs": [
                        f'PB-ID: {self.pb_id}',
                        f'ID: {player_id if player_id else shruggie}'
                    ],
                    get_lang_text("bcsObtainedAccountDatesKEY"): [
                        f'{get_lang_text("bcsObtainedCretedOn")}: {player_acc_created_on if player_acc_created_on else shruggie}',
                        f'{get_lang_text("bcsObtainedUpdatedOn")}: {player_acc_updated_on if player_acc_updated_on else shruggie}'
                    ],
                    get_lang_text("bcsObtainedAccountIdentity"): [
                        f'{get_lang_text("bcsObtainedOtherAcc")}: {player_other_acc_joint}',
                        f'{get_lang_text("bcsObtainedUpgradedName")}: {player_premium_name if player_premium_name else shruggie}',
                        f'{get_lang_text("bcsObtainedOtherUpgradedName")}: {player_premium_names_joint}'
                    ]
                }
                if player_discord:
                    for i, d in enumerate(player_discord):
                        grouped_info[get_lang_text("bcsObtainedConnectedDiscordKEY")+(f" {i+1}" if len(player_discord) > 1 else "")] = [
                            f'{get_lang_text("bcsObtainedConnectedDiscordUsername")}: {d.get("username")}',
                            f'DC-ID: {d.get("id")}',
                            f'{get_lang_text("bcsObtainedConnectedDiscordUniqueId")}: {d.get("_id")}'
                        ]
                else:
                    grouped_info[get_lang_text("bcsObtainedConnectedDiscordKEY")] = [
                        shruggie
                    ]

                account_name_spacing = 15
                tscale = 0.65
                ts_height = _babase.get_string_height(
                    trophystr, suppress_warning=True
                )
                sub_width = self._width - 80
                sub_height: float = (
                    300
                    + ts_height * tscale
                    + account_name_spacing * len(data['accountDisplayStrings'])
                    + sum(len(info) for info in grouped_info.values()) * 17.5
                    + (len(player_mutual_server) * 17.5 if player_mutual_server else 0)
                )
                self._subcontainer = bui.containerwidget(
                    parent=self._scrollwidget,
                    size=(sub_width, sub_height),
                    background=False,
                )
                v = sub_height - 20

                # Menampilkan custom_info
                v -= 30
                for title, info_list in grouped_info.items():
                    gap = 15.5
                    v = sub_height - gap
                    sub_height -= gap
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(0, 0),
                        position=(sub_width * 0.5, v),
                        flatness=1.0,
                        h_align='center',
                        v_align='center',
                        scale=0.37,
                        color=bui.app.ui_v1.infotextcolor,
                        text=title,
                        maxwidth=sub_width * 0.9,
                    )
                    gap = 23.5
                    v = sub_height - gap
                    sub_height -= gap
                    for i, info in enumerate(info_list):
                        if i > 0:
                            gap = 15.5
                            v = sub_height - gap
                            sub_height -= gap
                        bui.textwidget(
                            parent=self._subcontainer,
                            size=(750, 20),
                            position=(-sub_width * 0.65, v),
                            h_align='center',
                            v_align='center',
                            scale=0.55,
                            color=babase.safecolor((1, 1, 1), 0.7),
                            text=info,
                            maxwidth=sub_width * 0.9,
                            selectable=True,
                            click_activate=True,
                            on_activate_call=Call(self._confirm_copy_text, info)
                        )

                if player_mutual_server:
                    v -= 20
                    # Menampilkan mutual server
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(0, 0),
                        position=(sub_width * 0.5, v),
                        flatness=1.0,
                        h_align='center',
                        v_align='center',
                        scale=0.37,
                        color=bui.app.ui_v1.infotextcolor,
                        text=get_lang_text('bcsObtainedMutualServer'),
                        maxwidth=sub_width * 0.9,
                    )

                    v = sub_height - 30
                    sub_height -= 30
                    for i, mutual_server in enumerate(player_mutual_server):
                        gap = 15.5
                        v = sub_height - gap
                        sub_height -= gap
                        bui.textwidget(
                            parent=self._subcontainer,
                            size=(750, 20),
                            position=(-sub_width * 0.65, v),
                            h_align='center',
                            v_align='center',
                            scale=0.55,
                            color=babase.safecolor((1, 1, 1), 0.7),
                            text=f"{mutual_server}",
                            maxwidth=sub_width * 0.9,
                            selectable=True,
                            click_activate=True,
                            on_activate_call=Call(self._confirm_copy_text, f"{mutual_server}")
                        )

                title_scale = 0.37
                center = 0.3
                maxwidth_scale = 0.45
                showing_character = False
                if data['profileDisplayString'] is not None or player_character:
                    tint_color = COLOR_SCREENCMD_NORMAL
                    try:
                        if data['profile'] is not None or player_character:
                            profile = data['profile'] if data.get('profile') else self.custom_data['spaz']
                            if profile and data.get('profile'):
                                character = babase.app.classic.spaz_appearances.get( # type: ignore
                                    profile['character'], None
                                )
                            else:
                                character = babase.app.classic.spaz_appearances.get( # type: ignore
                                    self.custom_data['spaz'], None
                                )

                            if character is not None:
                                tint_color = (
                                    profile['color']
                                    if 'color' in profile
                                    else COLOR_SCREENCMD_NORMAL
                                )
                                tint2_color = (
                                    profile['highlight']
                                    if 'highlight' in profile
                                    else (1, 1, 1)
                                )
                                icon_tex = character.icon_texture
                                tint_tex = character.icon_mask_texture
                                mask_texture = bui.gettexture(
                                    'characterIconMask'
                                )
                                bui.imagewidget(
                                    parent=self._subcontainer,
                                    position=(sub_width * center - 40, v - 95),
                                    size=(80, 80),
                                    color=(1, 1, 1),
                                    mask_texture=mask_texture,
                                    texture=bui.gettexture(icon_tex),
                                    tint_texture=bui.gettexture(tint_tex),
                                    tint_color=tint_color,
                                    tint2_color=tint2_color,
                                )
                                v -= 105
                    except Exception:
                        logging.exception('Error displaying character.')
                    profile_text = babase.Lstr(value=data['profileDisplayString'] if data.get('profileDisplayString') else self.custom_data['spaz'])
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(0, 0),
                        position=(sub_width * center, v),
                        h_align='center',
                        v_align='center',
                        scale=0.9,
                        color=babase.safecolor(tint_color, 0.7),
                        shadow=1.0,
                        text=profile_text,
                        maxwidth=sub_width * maxwidth_scale * 0.75,
                    )
                    showing_character = True
                    v -= 33

                center = 0.75 if showing_character else 0.5
                maxwidth_scale = 0.45 if showing_character else 0.9

                v = sub_height - 20
                account_title = get_lang_text('settingsWindow.accountText')
                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    flatness=1.0,
                    h_align='center',
                    v_align='center',
                    scale=title_scale,
                    color=bui.app.ui_v1.infotextcolor,
                    text=account_title,
                    maxwidth=sub_width * maxwidth_scale,
                )
                draw_small = (
                    showing_character or len(data['accountDisplayStrings']) > 1
                )
                v -= 25 if draw_small else 30
                # Accounts
                for account_string in data['accountDisplayStrings']:
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(200, 20),
                        position=((sub_width * center * 0.575 if self.custom_data.get('spaz') else sub_width * center * 0.35), v),
                        h_align='center',
                        v_align='center',
                        scale=0.55 if draw_small else 0.8,
                        text=account_string,
                        maxwidth=sub_width * maxwidth_scale,
                        selectable=True,
                        click_activate=True,
                        on_activate_call=Call(self._confirm_copy_text, account_string)
                    )
                    v -= account_name_spacing

                v += account_name_spacing
                v -= 25 if showing_character else 29

                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    flatness=1.0,
                    h_align='center',
                    v_align='center',
                    scale=title_scale,
                    color=bui.app.ui_v1.infotextcolor,
                    text=babase.Lstr(resource='rankText'),
                    maxwidth=sub_width * maxwidth_scale,
                )
                v -= 14
                if data['rank'] is None:
                    rank_str = '-'
                    suffix_offset = None
                else:
                    str_raw = babase.Lstr(
                        resource='league.rankInLeagueText'
                    ).evaluate()
                    rank_str = babase.Lstr(
                        resource='league.rankInLeagueText',
                        subs=[
                            ('${RANK}', str(data['rank'][2])),
                            (
                                '${NAME}',
                                babase.Lstr(
                                    translate=('leagueNames', data['rank'][0])
                                ),
                            ),
                            ('${SUFFIX}', ''),
                        ],
                    ).evaluate()
                    rank_str_width = min(
                        sub_width * maxwidth_scale,
                        _babase.get_string_width(
                            rank_str, suppress_warning=True
                        )
                        * 0.55,
                    )

                    if (
                        str_raw.endswith('${SUFFIX}')
                        and data['rank'][0] != 'Diamond'
                    ):
                        suffix_offset = rank_str_width * 0.5 + 2
                    else:
                        suffix_offset = None

                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    h_align='center',
                    v_align='center',
                    scale=0.55,
                    text=rank_str,
                    maxwidth=sub_width * maxwidth_scale,
                )
                if suffix_offset is not None:
                    assert data['rank'] is not None
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(0, 0),
                        position=(sub_width * center + suffix_offset, v + 3),
                        h_align='left',
                        v_align='center',
                        scale=0.29,
                        flatness=1.0,
                        text='[' + str(data['rank'][1]) + ']',
                    )
                v -= 14

                str_raw = babase.Lstr(resource='league.rankInLeagueText').evaluate()
                old_offs = -50
                prev_ranks_shown = 0
                for prev_rank in data['prevRanks']:
                    rank_str = babase.Lstr(
                        value='${S}:    ${I}',
                        subs=[
                            ('${S}', babase.Lstr(
                                resource='league.seasonText',
                                subs=[('${NUMBER}', str(prev_rank[0]))],
                                )
                            ),
                            ('${I}', babase.Lstr(
                                resource='league.rankInLeagueText',
                                subs=[
                                    ('${RANK}', str(prev_rank[3])),
                                    ('${NAME}', babase.Lstr(translate=('leagueNames', prev_rank[1],)),),
                                    ('${SUFFIX}', ''),
                                ])
                            )
                        ],
                    ).evaluate()
                    rank_str_width = min(
                        sub_width * maxwidth_scale,
                        _babase.get_string_width(
                            rank_str, suppress_warning=True
                        )
                        * 0.3,
                    )

                    if (
                        str_raw.endswith('${SUFFIX}')
                        and prev_rank[1] != 'Diamond'
                    ):
                        suffix_offset = rank_str_width + 2
                    else:
                        suffix_offset = None
                    bui.textwidget(
                        parent=self._subcontainer,
                        size=(0, 0),
                        position=(sub_width * center + old_offs, v),
                        h_align='left',
                        v_align='center',
                        scale=0.3,
                        text=rank_str,
                        flatness=1.0,
                        maxwidth=sub_width * maxwidth_scale,
                    )
                    if suffix_offset is not None:
                        bui.textwidget(
                            parent=self._subcontainer,
                            size=(0, 0),
                            position=(
                                sub_width * center + old_offs + suffix_offset,
                                v + 1,
                            ),
                            h_align='left',
                            v_align='center',
                            scale=0.20,
                            flatness=1.0,
                            text='[' + str(prev_rank[2]) + ']',
                        )
                    prev_ranks_shown += 1
                    v -= 10

                v -= 13

                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    flatness=1.0,
                    h_align='center',
                    v_align='center',
                    scale=title_scale,
                    color=bui.app.ui_v1.infotextcolor,
                    text=babase.Lstr(resource='achievementsText'),
                    maxwidth=sub_width * maxwidth_scale,
                )
                v -= 14
                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    h_align='center',
                    v_align='center',
                    scale=0.55,
                    text=str(data['achievementsCompleted'])
                    + ' / '
                    + str(len(bui.app.classic.ach.achievements)), # type: ignore
                    maxwidth=sub_width * maxwidth_scale,
                )
                v -= 25

                if prev_ranks_shown == 0 and showing_character:
                    v -= 20
                elif prev_ranks_shown == 1 and showing_character:
                    v -= 10

                center = 0.5
                maxwidth_scale = 0.9

                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, 0),
                    position=(sub_width * center, v),
                    h_align='center',
                    v_align='center',
                    scale=title_scale,
                    color=bui.app.ui_v1.infotextcolor,
                    flatness=1.0,
                    text=babase.Lstr(
                        resource='trophiesThisSeasonText',
                        fallback_resource='trophiesText',
                    ),
                    maxwidth=sub_width * maxwidth_scale,
                )
                v -= 19
                bui.textwidget(
                    parent=self._subcontainer,
                    size=(0, ts_height),
                    position=(sub_width * 0.5, v - ts_height * tscale),
                    h_align='center',
                    v_align='top',
                    corner_scale=tscale,
                    text=trophystr,
                )

            except Exception:
                logging.exception('Error displaying account info.')
            if self._loading_spinner:
                babase.apptimer(0.5, self._loading_spinner.delete)

def __popup_menu_window_init__(
    self,
    position: Tuple[float, float],
    choices: Sequence[str],
    current_choice: str,
    delegate: Any = None,
    width: float = 230.0,
    maxwidth: float | None = None,
    scale: float = 1.0,
    choices_disabled: Sequence[str] | None = None,
    choices_display: Sequence[babase.Lstr] | None = None,
    color: Tuple[float, float, float] = (0.35, 0.55, 0.15)):
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
    self._donebuilding = False
    if not choices:
        raise TypeError('Must pass at least one choice')
    self._width = width
    self._scale = scale
    if len(choices) > 7:
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
                    _babase.get_string_width(choice_display_name, suppress_warning=True)) + 75)
        else:
            self._width = max(
                self._width,
                min(
                    maxwidth,
                    _babase.get_string_width(choice_display_name, suppress_warning=True)) + 60)

    # init parent class - this will rescale and reposition things as
    # needed and create our root widget
    PopupWindow.__init__(
        self,
        position,
        size=(self._width, self._height),
        bg_color=self._color,
        scale=self._scale)

    if self._use_scroll:
        self._scrollwidget = bui.scrollwidget(
            parent=self.root_widget,
            position=(10, 20),
            highlight=False,
            color=(0.35, 0.55, 0.15),
            size=(self._width - 40, self._height - 40))
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0)
    else:
        self._offset_widget = bui.containerwidget(
            parent=self.root_widget,
            position=(20, 15),
            size=(self._width - 40, self._height),
            background=False)
        self._columnwidget = bui.columnwidget(
            parent=self._offset_widget,
            border=2,
            margin=0)
    for index, choice in enumerate(choices):
        if len(choices_display_fin) == len(choices):
            choice_display_name = choices_display_fin[index]
        else:
            choice_display_name = choice
        inactive = (choice in self._choices_disabled)
        wdg = bui.textwidget(
            parent=self._columnwidget,
            size=(self._width - 40, 28),
            on_select_call=CallStrict(self._select, index),
            click_activate=True,
            color=(
                (0.5, 0.5, 0.5, 0.5) if inactive else
                (0.5, 1, 0.5, 1) if choice == self._current_choice else
                (0.8, 0.8, 0.8, 1.0)
            ),
            padding=0,
            maxwidth=maxwidth,
            text=choice_display_name,
            on_activate_call=self._activate,
            v_align='center',
            selectable=(not inactive))
        if choice == self._current_choice:
            bui.containerwidget(
                edit=self._columnwidget,
                selected_child=wdg,
                visible_child=wdg)

    # ok from now on our delegate can be called
    self._delegate = weakref.ref(delegate)
    self._done_building = True
    self._donebuilding = True

def _get_store_char_tex(self) -> str:
    try:
        from bauiv1 import set_party_icon_always_visible # type: ignore
        set_party_icon_always_visible(True)
    except Exception as e:
        logging.exception(e)
    return (
        'storeCharacterXmas' if bui.app.plus.get_v1_account_misc_read_val('xmas', False) else # type: ignore
        'storeCharacterEaster' if bui.app.plus.get_v1_account_misc_read_val('easter', False) else # type: ignore
        'storeCharacter')

###### INTERNAL DATA ######
def backup_all_names():
    Thread(target=backup_all_names_data).start()

def _load_all_internal_data():
    #### Load Main Config ####
    load_party_config() # Load configs first
    load_responder_config()
    _load_nicknames()
    _load_saved_kunci_jawaban()
    _load_saved_custom_replies()

    #### Load Party Other Data ####
    _load_quick_responds()
    _load_custom_commands()

    #### Load Players Data ####
    load_all_names_data()
    babase.apptimer(1, backup_all_names)
    load_responder_blacklist_names(first_boot=True)
    load_muted_players()
    load_player_name_exceptions()
    if responder_config.get(config_name_reset_player_warns):
        reset_all_player_warnings()
    else:
        global player_warnings
        player_warnings = load_player_warnings()
    load_internal_chats_data()
    load_internal_all_chats_data()

    #### Load Abuses ####
    load_abuses(id_lang)
    load_abuses(en_lang)
    load_abuses(hi_lang)
    load_anti_abuse_exception_words()

    #### Server Players Data ####
    Thread(target=load_players_server_data).start()

    #### Translation Data ####
    load_and_update_tranlataion_data()

def load_and_update_tranlataion_data():
    global DEFAULT_AVAILABLE_LANG_ID_LIST, DEFAULT_AVAILABLE_LANG_LIST, Translate_Texts
    global NEW_AVAILABLE_LANG_LIST, NEW_AVAILABLE_LANG_ID_LIST

    new_data = load_and_get_lang_key_new_tranlated_text()
    if new_data:
        for lang_data in new_data:
            lang_id, lang, trans_data = lang_data
            if isinstance(lang_id, str) and isinstance(lang, str) and isinstance(trans_data, dict):

                if lang_id not in DEFAULT_AVAILABLE_LANG_ID_LIST:
                    DEFAULT_AVAILABLE_LANG_ID_LIST.append(lang_id)
                if lang not in DEFAULT_AVAILABLE_LANG_LIST:
                    DEFAULT_AVAILABLE_LANG_LIST.append(lang)

                if lang_id not in NEW_AVAILABLE_LANG_ID_LIST:
                    NEW_AVAILABLE_LANG_ID_LIST.append(lang_id)
                if lang not in NEW_AVAILABLE_LANG_LIST:
                    NEW_AVAILABLE_LANG_LIST.append(lang)

                for key, val in trans_data.items():
                    if key in Translate_Texts:
                        Translate_Texts[key][lang_id] = val
                    else:
                        Translate_Texts[key] = {lang_id: val}
    else:
        #print("fNew trasnlation data is empty")
        pass

    custom_data = load_and_get_lang_key_custom_tranlated_text()
    if custom_data:
        for key, val in custom_data.items():
            if key in Translate_Texts:
                Translate_Texts[key].update(val)
            else:
                Translate_Texts[key] = val
    else:
        #print("Custom translation data is empty")
        pass

def _save_internal_data_force(auto_save:bool=False):
    start_save_all_names().start() if not auto_save else start_save_all_names().start_threaded()
    save_internal_player_chats_data(force=True)
    save_internal_all_chats_data(force=True)
    save_party_config(config=party_config, force=True)
    save_responder_config(config=responder_config, force=True)
    print(f"Force ALL Data Saving Called")

def _save_internal_data_normal():
    save_internal_player_chats_data()
    save_internal_all_chats_data()
    save_party_config(config=party_config)
    save_responder_config(config=responder_config)
    print(f"Normal ALL Data Saving Called")
###### INTERNAL DATA ######

########## OTHER UTILS ##########
def _app_party_window():
    babase.app.classic.party_window # type: ignore

auto_responder = None
def apply_packages():
    try:
        bauiv1lib.party.PartyWindow = LessPartyWindow
        PopupMenuWindow.__init__ = __popup_menu_window_init__

        babase.app.classic.party_window = _app_party_window # type: ignore

        global auto_responder
        auto_responder = LessAutoResponder()
        auto_responder._start_engine()

        babase.app.config['Chat Muted'] = True if party_config.get(CFG_NAME_MODIFIED_SCREENMESSAGE) else False
        babase.app.config.apply_and_commit()

        global is_muted
        is_muted = babase.app.config.resolve('Chat Muted')

        global MY_MASTER
        master_name = bui.app.plus.get_v1_account_display_string(full=True) # type: ignore
        if not master_name in MY_MASTER and master_name:
            MY_MASTER.append(master_name)

        try:
            from bauiv1lib.mainmenu import MainMenuWindow
            MainMenuWindow._get_store_char_tex = _get_store_char_tex # type: ignore
        except Exception as e:
            logging.exception(e)

        #chatmessage("Hey, This Message Should Be Small Enough")
        #bauiv1lib.party.PartyWindow()
        #CreditPopup()

        #EditableDataPopup(load_func=load_responder_blacklist_names, save_func_list=save_blacklist_names, is_player=True, label="Blacklisted Players")
        #TranslateTextsPopup(Translate_Texts)
        #PlayerInfoPopup(MY_MASTER[0])
    except Exception as e:
        print_internal_exception(e)

def setbs_uiscale():
    if not 'UIScale' in babase.app.config:
        if bui.app.ui_v1._uiscale is UIScale.LARGE:
            scale = 0
        if bui.app.ui_v1._uiscale is UIScale.MEDIUM:
            scale = 1
        else:
            scale = 2
        babase.app.config['UIScale'] = scale
        babase.app.config.apply_and_commit()

    if babase.app.config['UIScale'] == 0:
        uiscale = UIScale.LARGE
    elif babase.app.config['UIScale'] == 1:
        uiscale = UIScale.MEDIUM
    else:
        uiscale = UIScale.SMALL
    bui.app.ui_v1._uiscale = uiscale

auto_save_data_timer = None
auto_save_data_ratio = 300 # Seconds
########## OTHER UTILS ##########

# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def on_app_running(self) -> None:
        _load_all_internal_data()
        setbs_uiscale()
        babase.apptimer(1.5, apply_packages)
        babase.apptimer(1, modify_conncet_to_party)

        global auto_save_data_timer
        auto_save_data_timer = babase.AppTimer(
            auto_save_data_ratio,
            CallStrict(_save_internal_data_normal),
            repeat=True
        )

        try:
            from bauiv1 import set_party_icon_always_visible  # type: ignore
            set_party_icon_always_visible(True)
        except Exception:
            pass

    def on_app_shutdown(self) -> None:
        return

    def has_settings_ui(self) -> bool:
        return True

    def show_settings_ui(self, source_widget: Optional[bui.Window]) -> None:
        PartySettingsWindow()

    BTN = None

    @classmethod
    def up(c):
        c.BTN.activate() if c.BTN.exists() else None

    def __init__(self):
        p = LessPartyWindow
        a = '__init__'
        o = getattr(p, a)
        setattr(p, a, lambda z, *a, **k: (o(z, *a, **k), self.make(z))[0])

    @property
    def uiscale(self):
        return bui.app.ui_v1.uiscale

    def make(self, z):
        sz = (120, 70)
        p = z._root_widget

        scale_name = (
            "SMALL" if self.uiscale is babase.UIScale.SMALL else
            "MEDIUM" if self.uiscale is babase.UIScale.MEDIUM else
            "LARGE"
        )

        #print(f"[byLess] Current UI Scale: {scale_name}")
        #babase.screenmessage(f"UI Scale: {scale_name}", color=(0, 1, 1))

        x: int = (
            1220 if self.uiscale is babase.UIScale.SMALL else
            1065 if self.uiscale is babase.UIScale.MEDIUM else
            964
        )
        y: int = (
            530 if self.uiscale is babase.UIScale.SMALL else
            745 if self.uiscale is babase.UIScale.MEDIUM else
            850
        )

        iw(
            parent=p,
            size=(sz[0] * 1.34, sz[1] * 1.4),
            position=(x - sz[0] * 0.14, y - sz[1] * 0.20),
            texture=gt('softRect'),
            opacity=0.2,
            color=(0, 0, 0)
        )

        search_ds: str = f'{get_lang_text("search")}!'
        self.search_button = self.__class__.BTN = bui.buttonwidget(
            parent=p,
            position=(x, y),
            label=search_ds,
            color=Finder.COL1,
            textcolor=Finder.COL3,
            size=sz,
            on_activate_call=lambda: Finder(self.search_button)
        )

        #print(f"[byLess] Button position: ({x}, {y}) size={sz}")
