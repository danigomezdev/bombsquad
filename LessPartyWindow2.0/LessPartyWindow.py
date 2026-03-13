# ba_meta require api 9
# Released under the MIT License. See LICENSE for details.

from __future__ import annotations

import builtins as _builtins
import copy
from datetime import datetime, timezone, timedelta
from enum import Enum
import http.client
import json
from json import load, dump, loads, dumps, JSONDecodeError
import logging
import math
import os
import random
from random import randint, uniform as uf
import re
import shutil
import socket
import threading
from threading import Thread, Thread as _Thread
import time
import traceback
from typing import (
    TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Set, Union
)
import urllib.error
import urllib.parse
import urllib.parse as _up
import urllib.request
import urllib.request as _ur
import weakref as _weakref

import _babase
import _bauiv1
import babase
from babase import SpecialChar
import bascenev1 as bs
from bascenev1 import connect_to_party as CON, protocol_version as PT
import bauiv1 as bui
from bauiv1 import (
    containerwidget as ocw,
    buttonwidget as obw,
    scrollwidget as sw,
    imagewidget as iw,
    textwidget as tw,
    gettexture as gt,
    getmesh as gm,
    getsound as gs,
    screenmessage as push,
    get_special_widget as zw,
    apptime,
    apptimer as teck,
    AppTimer as tuck,
    AppTimer,
    charstr as cs,
    SpecialChar as sc,
    CallStrict,
    app as APP,
    get_ip_address_type as IPT,
    clipboard_set_text as COPY,
    screenmessage,
)
from bauiv1lib import colorpicker
from bauiv1lib.confirm import ConfirmWindow
from bauiv1lib.gather._gather import GatherWindow
from bauiv1lib.gather.publictab import PublicGatherTab, UIRow
import bauiv1lib.party as party
from bauiv1lib.popup import PopupMenu, PopupMenuWindow, PopupWindow
from bauiv1lib.tabs import TabRow



BASE_URL = "https://api.bombsquad.lat" # http://localhost:3333
V2_LOGO = "\ue063"
CREATOR = "\ue043Less"

# Directory paths
MY_DIRECTORY = _babase.env()['python_directory_user'] + "/LessPartyWindow"
PLAYERS_DIRECTORY = os.path.join(MY_DIRECTORY, "players")
USERS_DIRECTORY = os.path.join(MY_DIRECTORY, "users")
REMOTE_DIRECTORY = os.path.join(USERS_DIRECTORY, "remote")
CONFIGS_FILE = os.path.join(MY_DIRECTORY, "configs.json")
CAMERA_FILE = os.path.join(MY_DIRECTORY, "camera.json")
LAST_SERVERS_FILE = os.path.join(MY_DIRECTORY, "lastservers.json")
FRIENDS_FILE = os.path.join(PLAYERS_DIRECTORY, "friends.json")
PLAYERINFO_FILE = os.path.join(PLAYERS_DIRECTORY, "playerinfo.json")
CHATS_DIRECTORY = os.path.join(MY_DIRECTORY, "chats")
CHATS_JSON_FILE = os.path.join(CHATS_DIRECTORY, "chats.json")
DM_MSGS_FILE = os.path.join(REMOTE_DIRECTORY, "msgs.json")
QUICK_RESPONDS_FILE = os.path.join(MY_DIRECTORY, "quick_responds.txt")

# Config key names
CFG_NAME_PREFFERED_LANG = 'Less Finder Language'
CFG_NAME_FILTER_ACCOUNT = 'Acounts Filter'
CFG_NAME_COLOR_BACKGROUND = 'COLOR BACKGROUND'
CFG_NAME_COLOR_SECONDARY = 'COLOR SECONDARY'
CFG_NAME_COLOR_TERTIARY = 'COLOR TERTIARY'
CFG_NAME_COLOR_PRIMARY = 'COLOR PRIMARY'
CFG_NAME_COLOR_ACCENT = 'COLOR ACCENT'
CFG_NAME_COLOR_BUTTON = 'COLOR BUTTON'
CFG_NAME_USE_THEME = 'USE THEME'
CFG_NAME_UI_SCALE = 'UI Scale'

# Chat viewer config key names
CFG_NAME_CHAT_VIEWER_TYPE = 'Chats Name Viewer'
CFG_NAME_CHAT_VIEWER_SHOW_CID = 'Show Client ID'
CFG_NAME_GLOBAL_GATHER = 'Global Gather Modified'
CFG_NAME_CAMERA_AUTO_RESTORE = 'Camera Auto Restore'
CFG_NAME_CAMERA_LAST_USED = 'Camera Last Used'
CFG_NAME_MAX_RECENT_SERVERS = 'Max Recent Servers'
CFG_NAME_TINT_COLOR = 'Map Tint Color'
CFG_NAME_TINT_DISCO = 'Map Tint Disco'
CFG_NAME_TINT_DISCO_SPEED = 'Map Tint Disco Speed'
CFG_NAME_PING_MSG_FORMAT = 'Ping Message Format'
CFG_NAME_MAX_CHAT_LOGS = 'Max Chat Logs'
CFG_NAME_MAX_PLAYERINFO = 'Max Player Info'
CFG_NAME_CHAT_COLOR_INTENSITY = 'Chat Color Intensity'

CHAT_VIEW_TYPE_PROFILE = 'profile'
CHAT_VIEW_TYPE_ACCOUNT = 'account'
CHAT_VIEW_TYPE_MULTI = 'multi'
CHAT_VIEW_TYPE_MULTI_V2 = 'multi_v2'

# Translation config key names
CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD = 'Translate TextField Source'
CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD = 'Translate TextField Destination'
CFG_NAME_TRANSLATE_SOURCE_OTHER = 'Translate Other Text Source'
CFG_NAME_TRANSLATE_DESTINATION_OTHER = 'Translate Other Text Destination'
CFG_NAME_TRANSLATE_PREFERRED_MACHINE = 'Preffered Translate Machine'

JSONS_DEFAULT_INDENT_FILE = 1

# Screen message colors
COLOR_SCREENCMD_NORMAL = (1.0, 0.65, 0.8)
COLOR_SCREENCMD_ERROR = (1.0, 0.20, 0.0)

default_finder_config: Dict[str, Any] = {
    CFG_NAME_PREFFERED_LANG: '',
    CFG_NAME_FILTER_ACCOUNT: 'all',
    CFG_NAME_COLOR_BACKGROUND: (0.9, 1.0, 1.0),
    CFG_NAME_COLOR_SECONDARY: (0.962, 1.0, 1.0),
    CFG_NAME_COLOR_TERTIARY: (0.942, 1.0, 1.0),
    CFG_NAME_COLOR_PRIMARY: (0.988, 1.0, 1.0),
    CFG_NAME_COLOR_ACCENT: (0.95, 1.0, 1.0),
    CFG_NAME_COLOR_BUTTON: (0.98, 1.0, 1.0),
    CFG_NAME_USE_THEME: True,
    CFG_NAME_UI_SCALE: '',
    CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD: 'auto',
    CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD: 'en',
    CFG_NAME_TRANSLATE_SOURCE_OTHER: 'auto',
    CFG_NAME_TRANSLATE_DESTINATION_OTHER: 'en',
    CFG_NAME_TRANSLATE_PREFERRED_MACHINE: 'api',
    CFG_NAME_CHAT_VIEWER_TYPE: False,
    CFG_NAME_CHAT_VIEWER_SHOW_CID: False,
    CFG_NAME_GLOBAL_GATHER: False,
    CFG_NAME_CAMERA_AUTO_RESTORE: True,
    CFG_NAME_CAMERA_LAST_USED: None,
    CFG_NAME_MAX_RECENT_SERVERS: 5,
    CFG_NAME_TINT_COLOR: (1.0, 1.0, 1.0),
    CFG_NAME_TINT_DISCO: False,
    CFG_NAME_TINT_DISCO_SPEED: 1.0,
    CFG_NAME_PING_MSG_FORMAT: 'My Ping {}ms',
    CFG_NAME_MAX_CHAT_LOGS: 100,
    CFG_NAME_MAX_PLAYERINFO: 1000,
    CFG_NAME_CHAT_COLOR_INTENSITY: 'strong',
}


INVALID_KEY_TEXT = '[{0}]'

DEFAULT_LANGUAGES_DICT: Dict[str, dict] = {
    'es': {'name': 'Español', 'pc_compatible': True},
    'en': {'name': 'English', 'pc_compatible': True},
    'pt': {'name': 'Português', 'pc_compatible': True},
    'ru': {'name': 'Русский', 'pc_compatible': True},
    'hi': {'name': 'हिन्दी', 'pc_compatible': False},
    'ml': {'name': 'മലയാളം', 'pc_compatible': False},
    'id': {'name': 'Bahasa Indonesia', 'pc_compatible': False},
}

DEFAULT_AVAILABLE_LANG_LIST = [
    info['name'] for info in DEFAULT_LANGUAGES_DICT.values()
]
DEFAULT_AVAILABLE_LANG_ID_LIST = list(DEFAULT_LANGUAGES_DICT.keys())


def get_language_name(lang_id: str) -> str:
    return DEFAULT_LANGUAGES_DICT.get(lang_id, {}).get('name', 'English')


def get_language_names_dict() -> dict:
    return {
        lang_id: info['name']
        for lang_id, info in DEFAULT_LANGUAGES_DICT.items()
    }


Translate_Texts: Dict[str, Dict[str, str]] = {
    'Global.search': {
        'en': 'Search',
        'es': 'Buscar',
        'pt': 'Buscar',
        'ru': 'Поиск',
        'hi': 'खोजें',
        'ml': 'തിരയുക',
        'id': 'Cari',
    },
    'Global.delete': {
        'en': 'Delete',
        'es': 'Eliminar',
        'pt': 'Excluir',
        'ru': 'Удалить',
        'hi': 'हटाएं',
        'ml': 'ഇല്ലാതാക്കുക',
        'id': 'Hapus',
    },
    'Global.filter': {
        'en': 'Filter',
        'es': 'Filtrar',
        'pt': 'Filtrar',
        'ru': 'Фильтр',
        'hi': 'फ़िल्टर',
        'ml': 'ഫിൽട്ടർ',
        'id': 'Saring',
    },
    'Global.connect': {
        'en': 'Connect',
        'es': 'Conectar',
        'pt': 'Conectar',
        'ru': 'Подключить',
        'hi': 'कनेक्ट',
        'ml': 'കണക്റ്റ്',
        'id': 'Sambungkan',
    },
    'Global.online': {
        'en': 'Online',
        'es': 'En línea',
        'pt': 'Online',
        'ru': 'Онлайн',
        'hi': 'ऑनलाइन',
        'ml': 'ഓൺലൈൻ',
        'id': 'Online',
    },
    'Global.fieldEmpty': {
        'en': 'The field is empty, cannot add',
        'es': 'El campo está vacío, no se puede agregar',
        'pt': 'O campo está vazio, não é possível adicionar',
        'ru': 'Поле пустое, нельзя добавить',
        'hi': 'फ़ील्ड खाली है, जोड़ नहीं सकते',
        'ml': 'ഫീൽഡ് ശൂന്യമാണ്, ചേർക്കാൻ സാധിക്കില്ല',
        'id': 'Kolom kosong, tidak dapat menambahkan',
    },
    'Global.results': {
        'en': 'Results',
        'es': 'Resultados',
        'pt': 'Resultados',
        'ru': 'Результаты',
        'hi': 'परिणाम',
        'ml': 'ഫലങ്ങൾ',
        'id': 'Hasil',
    },
    'Global.credits': {
        'en': 'Credits',
        'es': 'Créditos',
        'pt': 'Créditos',
        'ru': 'Благодарности',
        'hi': 'श्रेय',
        'ml': 'ക്രെഡിറ്റുകൾ',
        'id': 'Kredit',
    },
    'Global.deletedSuccessfully': {
        'en': 'Deleted successfully',
        'es': 'Eliminado correctamente',
        'pt': 'Excluído com sucesso',
        'ru': 'Успешно удалено',
        'hi': 'सफलतापूर्वक हटाया गया',
        'ml': 'വിജയകരമായി നീക്കം ചെയ്തു',
        'id': 'Berhasil dihapus',
    },
    'Global.removedSuccessfully': {
        'en': 'Removed successfully',
        'es': 'Eliminado correctamente',
        'pt': 'Removido com sucesso',
        'ru': 'Успешно удалено',
        'hi': 'सफलतापूर्वक हटाया गया',
        'ml': 'വിജയകരമായി നീക്കി',
        'id': 'Berhasil dihapus',
    },
    'Global.addedSuccessfully': {
        'en': 'Added successfully',
        'es': 'Agregado correctamente',
        'pt': 'Adicionado com sucesso',
        'ru': 'Успешно добавлено',
        'hi': 'सफलतापूर्वक जोड़ा गया',
        'ml': 'വിജയകരമായി ചേർത്തു',
        'id': 'Berhasil ditambahkan',
    },
    'Global.addedToFriendsList': {
        'en': 'Added to friends list!',
        'es': '¡Agregado a la lista de amigos!',
        'pt': 'Adicionado à lista de amigos!',
        'ru': 'Добавлено в список друзей!',
        'hi': 'दोस्तों की सूची में जोड़ा गया!',
        'ml': 'സുഹൃത്തുകളുടെ പട്ടികയിൽ ചേർത്തു!',
        'id': 'Ditambahkan ke daftar teman!',
    },
    'Global.alreadyInList': {
        'en': 'Already in list',
        'es': 'Ya está en la lista',
        'pt': 'Já está na lista',
        'ru': 'Уже в списке',
        'hi': 'पहले से सूची में है',
        'ml': 'ഇതിനകം പട്ടികയിൽ ഉണ്ട്',
        'id': 'Sudah ada dalam daftar',
    },
    'Global.alreadyInFriendsList': {
        'en': 'Already in friends list',
        'es': 'Ya está en la lista de amigos',
        'pt': 'Já está na lista de amigos',
        'ru': 'Уже в списке друзей',
        'hi': 'पहले से दोस्तों की सूची में है',
        'ml': 'ഇതിനകം സുഹൃത്തുകളുടെ പട്ടികയിൽ ഉണ്ട്',
        'id': 'Sudah ada dalam daftar teman',
    },
    'Global.copiedToClipboard': {
        'en': 'Copied to clipboard!',
        'es': '¡Copiado al portapapeles!',
        'pt': 'Copiado para a área de transferência!',
        'ru': 'Скопировано в буфер обмена!',
        'hi': 'क्लिपबोर्ड में कॉपी किया गया!',
        'ml': 'ക്ലിപ്പ്ബോർഡിലേക്ക് പകർത്തി!',
        'id': 'Disalin ke papan klip!',
    },
    'ProfileSearchWindow.profileSearch': {
        'en': 'Profile Search',
        'es': 'Búsqueda de Perfil',
        'pt': 'Busca de Perfil',
        'ru': 'Поиск профиля',
        'hi': 'प्रोफ़ाइल खोज',
        'ml': 'പ്രൊഫൈൽ തിരയൽ',
        'id': 'Pencarian Profil',
    },
    'ProfileSearchWindow.loadingProfileData': {
        'en': 'Loading profile data...',
        'es': 'Cargando datos del perfil...',
        'pt': 'Carregando dados do perfil...',
        'ru': 'Загрузка данных профиля...',
        'hi': 'प्रोफ़ाइल डेटा लोड हो रहा है...',
        'ml': 'പ്രൊഫൈൽ ഡാറ്റ ലോഡ് ചെയ്യുന്നു...',
        'id': 'Memuat data profil...',
    },
    'Global.uid': {
        'en': 'UID',
        'es': 'UID',
        'pt': 'UID',
        'ru': 'UID',
        'hi': 'UID',
        'ml': 'UID',
        'id': 'UID',
    },
    'ProfileSearchWindow.name': {
        'en': 'Name',
        'es': 'Nombre',
        'pt': 'Nome',
        'ru': 'Имя',
        'hi': 'नाम',
        'ml': 'പേര്',
        'id': 'Nama',
    },
    'ProfileSearchWindow.character': {
        'en': 'Character',
        'es': 'Personaje',
        'pt': 'Personagem',
        'ru': 'Персонаж',
        'hi': 'चरित्र',
        'ml': 'കഥാപാത്രം',
        'id': 'Karakter',
    },
    'ProfileSearchWindow.accounts': {
        'en': 'Accounts',
        'es': 'Cuentas',
        'pt': 'Contas',
        'ru': 'Аккаунты',
        'hi': 'खाते',
        'ml': 'അക്കൗണ്ടുകൾ',
        'id': 'Akun',
    },
    'ProfileSearchWindow.rankInfo': {
        'en': 'Rank Info',
        'es': 'Información de Rango',
        'pt': 'Informações de Classificação',
        'ru': 'Информация о ранге',
        'hi': 'रैंक जानकारी',
        'ml': 'റാങ്ക് വിവരങ്ങൾ',
        'id': 'Info Peringkat',
    },
    'ProfileSearchWindow.current': {
        'en': 'Current',
        'es': 'Actual',
        'pt': 'Atual',
        'ru': 'Текущий',
        'hi': 'वर्तमान',
        'ml': 'നിലവിലെ',
        'id': 'Saat Ini',
    },
    'ProfileSearchWindow.previousRanks': {
        'en': 'Previous Ranks',
        'es': 'Rangos Anteriores',
        'pt': 'Classificações Anteriores',
        'ru': 'Предыдущие ранги',
        'hi': 'पिछले रैंक',
        'ml': 'മുൻ റാങ്കുകൾ',
        'id': 'Peringkat Sebelumnya',
    },
    'ProfileSearchWindow.season': {
        'en': 'Season',
        'es': 'Temporada',
        'pt': 'Temporada',
        'ru': 'Сезон',
        'hi': 'सीज़न',
        'ml': 'സീസൺ',
        'id': 'Musim',
    },
    'ProfileSearchWindow.achievements': {
        'en': 'Achievements',
        'es': 'Logros',
        'pt': 'Conquistas',
        'ru': 'Достижения',
        'hi': 'उपलब्धियाँ',
        'ml': 'നേട്ടങ്ങൾ',
        'id': 'Pencapaian',
    },
    'ProfileSearchWindow.trophies': {
        'en': 'Trophies',
        'es': 'Trofeos',
        'pt': 'Troféus',
        'ru': 'Трофеи',
        'hi': 'ट्रॉफी',
        'ml': 'ട്രോഫികൾ',
        'id': 'Trofi',
    },
    'ProfileSearchWindow.moreInfo': {
        'en': 'More Info',
        'es': 'Más Información',
        'pt': 'Mais Informações',
        'ru': 'Подробнее',
        'hi': 'अधिक जानकारी',
        'ml': 'കൂടുതൽ വിവരങ്ങൾ',
        'id': 'Info Lebih Lanjut',
    },
    'ProfileSearchWindow.accountType': {
        'en': 'Account Type',
        'es': 'Tipo de Cuenta',
        'pt': 'Tipo de Conta',
        'ru': 'Тип аккаунта',
        'hi': 'खाते का प्रकार',
        'ml': 'അക്കൗണ്ട് തരം',
        'id': 'Jenis Akun',
    },
    'ProfileSearchWindow.activeDays': {
        'en': 'Active Days',
        'es': 'Días Activos',
        'pt': 'Dias Ativos',
        'ru': 'Активные дни',
        'hi': 'सक्रिय दिन',
        'ml': 'സജീവ ദിവസങ്ങൾ',
        'id': 'Hari Aktif',
    },
    'ProfileSearchWindow.created': {
        'en': 'Created',
        'es': 'Creado',
        'pt': 'Criado',
        'ru': 'Создан',
        'hi': 'बनाया गया',
        'ml': 'സൃഷ്ടിച്ചത്',
        'id': 'Dibuat',
    },
    'ProfileSearchWindow.lastActive': {
        'en': 'Last Active',
        'es': 'Última Actividad',
        'pt': 'Última Atividade',
        'ru': 'Последняя активность',
        'hi': 'आखिरी बार सक्रिय',
        'ml': 'അവസാനമായി സജീവമായ',
        'id': 'Terakhir Aktif',
    },
    'ProfileSearchWindow.accountExistence': {
        'en': 'Account Creation Date',
        'es': 'Fecha de Creación de la Cuenta',
        'pt': 'Data de Criação da Conta',
        'ru': 'Дата создания аккаунта',
        'hi': 'खाता निर्माण तिथि',
        'ml': 'അക്കൗണ്ട് സൃഷ്ടിച്ച തീയതി',
        'id': 'Tanggal Pembuatan Akun',
    },
    'ProfileSearchWindow.ago': {
        'en': 'ago',
        'es': 'hace',
        'pt': 'há',
        'ru': 'назад',
        'hi': 'पहले',
        'ml': 'മുമ്പ്',
        'id': 'yang lalu',
    },
    'ProfileSearchWindow.years': {
        'en': 'years',
        'es': 'años',
        'pt': 'anos',
        'ru': 'лет',
        'hi': 'साल',
        'ml': 'വർഷം',
        'id': 'tahun',
    },
    'ProfileSearchWindow.months': {
        'en': 'months',
        'es': 'meses',
        'pt': 'meses',
        'ru': 'месяцев',
        'hi': 'महीने',
        'ml': 'മാസം',
        'id': 'bulan',
    },
    'ProfileSearchWindow.days': {
        'en': 'days',
        'es': 'días',
        'pt': 'dias',
        'ru': 'дней',
        'hi': 'दिन',
        'ml': 'ദിവസം',
        'id': 'hari',
    },
    'ProfileSearchWindow.Error.searchingAccount': {
        'en': 'Oops, an error occurred while searching for this account',
        'es': 'Ups, ocurrió un error al buscar esta cuenta',
        'pt': 'Ops, ocorreu um erro ao buscar esta conta',
        'ru': 'Упс, произошла ошибка при поиске этой учетной записи',
        'hi': 'ओह, इस खाते को खोजते समय एक त्रुटि हुई',
        'ml': 'അയ്യോ, ഈ അക്കൗണ്ട് തിരയുന്നതിനിടെ ഒരു പിശക് സംഭവിച്ചു',
        'id': 'Ups, terjadi kesalahan saat mencari akun ini',
    },
    'ProfileSearchWindow.Error.networkShort': {
        'en': 'Network error:',
        'es': 'Error de red:',
        'pt': 'Erro de rede:',
        'ru': 'Ошибка сети:',
        'hi': 'नेटवर्क त्रुटि:',
        'ml': 'നെറ്റ്‌വർക്ക് പിശക്:',
        'id': 'Kesalahan jaringan:',
    },
    'ProfileSearchWindow.Error.accountNotFound': {
        'en': 'Account not found',
        'es': 'Cuenta no encontrada',
        'pt': 'Conta não encontrada',
        'ru': 'Учетная запись не найдена',
        'hi': 'खाता नहीं मिला',
        'ml': 'അക്കൗണ്ട് കണ്ടെത്തിയില്ല',
        'id': 'Akun tidak ditemukan',
    },
    'ProfileSearchWindow.Error.noValidParameter': {
        'en': 'No valid parameter provided',
        'es': 'No se proporcionó un parámetro válido',
        'pt': 'Nenhum parâmetro válido fornecido',
        'ru': 'Не указан действительный параметр',
        'hi': 'कोई मान्य पैरामीटर प्रदान नहीं किया गया',
        'ml': 'സാധുവായ ഒരു പാരാമീറ്ററും നൽകിയിട്ടില്ല',
        'id': 'Tidak ada parameter valid yang diberikan',
    },
    'ProfileSearch.profileSearch': {
        'en': 'Profile Search',
        'es': 'Búsqueda de Perfil',
        'pt': 'Busca de Perfil',
        'ru': 'Поиск профиля',
        'hi': 'प्रोफ़ाइल खोज',
        'ml': 'പ്രൊഫൈൽ തിരയൽ',
        'id': 'Pencarian Profil',
    },
    'ProfileSearch.enterNameAndPressSearch': {
        'en': 'Enter a name and press Search',
        'es': 'Ingresa un nombre y presiona Buscar',
        'pt': 'Digite um nome e pressione Buscar',
        'ru': 'Введите имя и нажмите "Поиск"',
        'hi': 'एक नाम दर्ज करें और खोज दबाएँ',
        'ml': 'ഒരു പേര് നൽകുക, തിരയൽ അമർത്തുക',
        'id': 'Masukkan nama dan tekan Cari',
    },
    'ProfileSearch.searching': {
        'en': 'Searching...',
        'es': 'Buscando...',
        'pt': 'Buscando...',
        'ru': 'Поиск...',
        'hi': 'खोज रहा है...',
        'ml': 'തിരയുന്നു...',
        'id': 'Mencari...',
    },
    'ProfileSearch.Error.noAccountFound': {
        'en': 'No account found with Public ID:',
        'es': 'No se encontró ninguna cuenta con el ID público:',
        'pt': 'Nenhuma conta encontrada com ID Público:',
        'ru': 'Не найдена учетная запись с публичным ID:',
        'hi': 'इस सार्वजनिक आईडी के साथ कोई खाता नहीं मिला:',
        'ml': 'പബ്ലിക് ഐഡിയോടൊപ്പം യാതൊരു അക്കൗണ്ടും കണ്ടെത്തിയില്ല:',
        'id': 'Tidak ditemukan akun dengan ID Publik:',
    },
    'ProfileSearch.Error.network': {
        'en': 'Network error. Please check your connection and try again.',
        'es': 'Error de red. Por favor revisa tu conexión e inténtalo de nuevo.',
        'pt': 'Erro de rede. Por favor, verifique sua conexão e tente novamente.',
        'ru': 'Ошибка сети. Пожалуйста, проверьте подключение и попробуйте снова.',
        'hi': 'नेटवर्क त्रुटि। कृपया अपना कनेक्शन जांचें और पुनः प्रयास करें।',
        'ml': 'നെറ്റ്‌വർക്ക് പിശക്. ദയവായി നിങ്ങളുടെ കണക്ഷൻ പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Kesalahan jaringan. Silakan periksa koneksi Anda dan coba lagi.',
    },
    'ProfileSearch.Error.serviceUnavailable': {
        'en': 'Search service is currently unavailable. Please try again later.',
        'es': 'El servicio de búsqueda no está disponible actualmente. Por favor inténtalo más tarde.',
        'pt': 'O serviço de busca está indisponível no momento. Por favor, tente novamente mais tarde.',
        'ru': 'Служба поиска в настоящее время недоступна. Пожалуйста, попробуйте позже.',
        'hi': 'खोज सेवा वर्तमान में उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।',
        'ml': 'തിരച്ചിൽ സേവനം നിലവിൽ ലഭ്യമല്ല. ദയവായി പിന്നീട് വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Layanan pencarian saat ini tidak tersedia. Silakan coba lagi nanti.',
    },
    'ProfileSearch.Error.searchFailed': {
        'en': 'Oops, an error occurred while searching. Please try again.',
        'es': 'Ups, ocurrió un error al realizar la búsqueda. Por favor inténtalo de nuevo.',
        'pt': 'Ops, ocorreu um erro durante a busca. Por favor, tente novamente.',
        'ru': 'Упс, произошла ошибка при поиске. Пожалуйста, попробуйте снова.',
        'hi': 'ओह, खोज करते समय एक त्रुटि हुई। कृपया पुनः प्रयास करें।',
        'ml': 'അയ്യോ, തിരച്ചിൽ നടത്തുന്നതിനിടെ ഒരു പിശക് സംഭവിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Ups, terjadi kesalahan saat melakukan pencarian. Silakan coba lagi.',
    },
    'ProfileSearch.Error.invalidResponse': {
        'en': 'Invalid response from server. Please try again.',
        'es': 'Respuesta inválida del servidor. Por favor inténtalo de nuevo.',
        'pt': 'Resposta inválida do servidor. Por favor, tente novamente.',
        'ru': 'Неверный ответ от сервера. Пожалуйста, попробуйте снова.',
        'hi': 'सर्वर से अमान्य प्रतिक्रिया मिली। कृपया पुनः प्रयास करें।',
        'ml': 'സെർവറിൽ നിന്ന് അസാധുവായ പ്രതികരണം ലഭിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Respons tidak valid dari server. Silakan coba lagi.',
    },
    'ProfileSearch.Error.unexpected': {
        'en': 'Oops, an unexpected error occurred. Please try again.',
        'es': 'Ups, ocurrió un error inesperado. Por favor inténtalo de nuevo.',
        'pt': 'Ops, ocorreu um erro inesperado. Por favor, tente novamente.',
        'ru': 'Упс, произошла непредвиденная ошибка. Пожалуйста, попробуйте снова.',
        'hi': 'ओह, एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।',
        'ml': 'അയ്യോ, പ്രതീക്ഷിക്കാത്ത ഒരു പിശക് സംഭവിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Ups, terjadi kesalahan tak terduga. Silakan coba lagi.',
    },
    'ProfileSearch.Error.noExactMatch': {
        'en': 'No exact match found for',
        'es': 'No se encontró una coincidencia exacta para',
        'pt': 'Nenhuma correspondência exata encontrada para',
        'ru': 'Точное совпадение не найдено для',
        'hi': 'इसके लिए कोई सटीक मेल नहीं मिला',
        'ml': 'ഇതിനായി കൃത്യമായ പൊരുത്തം കണ്ടെത്തിയില്ല',
        'id': 'Tidak ditemukan kecocokan yang tepat untuk',
    },
    'ProfileSearch.Error.noAccountFoundWithId': {
        'en': 'No account found with ID:',
        'es': 'No se encontró ninguna cuenta con el ID:',
        'pt': 'Nenhuma conta encontrada com ID:',
        'ru': 'Не найдена учетная запись с ID:',
        'hi': 'इस आईडी के साथ कोई खाता नहीं मिला:',
        'ml': 'ഐഡിയോടൊപ്പം യാതൊരു അക്കൗണ്ടും കണ്ടെത്തിയില്ല:',
        'id': 'Tidak ditemukan akun dengan ID:',
    },
    'FriendsWindow.allFriends': {
        'en': 'All Your Friends',
        'es': 'Todos tus Amigos',
        'pt': 'Todos os Seus Amigos',
        'ru': 'Все ваши друзья',
        'hi': 'आपके सभी दोस्त',
        'ml': 'നിങ്ങളുടെ എല്ലാ സുഹൃത്തുക്കളും',
        'id': 'Semua Teman Anda',
    },
    'FriendsWindow.addManually': {
        'en': 'Add\nManually',
        'es': 'Agregar\nManualmente',
        'pt': 'Adicionar\nManualmente',
        'ru': 'Добавить\nВручную',
        'hi': 'मैन्युअली\nजोड़ें',
        'ml': 'മാനുവൽ\nചേർക്കുക',
        'id': 'Tambah\nManual',
    },
    'FriendsWindow.selectFriendToView': {
        'en': 'Select a friend\nto see where they are',
        'es': 'Selecciona un amigo\npara ver donde está',
        'pt': 'Selecione um amigo\npara ver onde ele está',
        'ru': 'Выберите друга,\nчтобы увидеть его местоположение',
        'hi': 'किसी दोस्त को चुनें\nयह देखने के लिए कि वह कहाँ है',
        'ml': 'ഒരു സുഹൃത്തിനെ തിരഞ്ഞെടുക്കുക\nഅവൻ എവിടെയെന്ന് കാണാൻ',
        'id': 'Pilih seorang teman\nuntuk melihat di mana ia berada',
    },
    'FriendsWindow.noFriendsOnline': {
        'en': 'Uh, it seems\nthere are no friends\nonline, try\nsearching servers',
        'es': 'Uh, parece que\nno hay amigos\nen línea, prueba\nbuscando servidores',
        'pt': 'Uh, parece que\nnão há amigos\nonline, tente\nbuscar servidores',
        'ru': 'Кажется, что\nнет друзей\nв сети, попробуйте\nпоискать серверы',
        'hi': 'अरे, लगता है कि\nकोई दोस्त ऑनलाइन\nनहीं है, सर्वर\nखोजकर देखें',
        'ml': 'ഉഫ്, ഓൺലൈൻ\nസുഹൃത്തുക്കൾ ഇല്ലെന്ന്\nതോന്നുന്നു, സർവർ\nതിരഞ്ഞ് നോക്കൂ',
        'id': 'Uh, sepertinya\nbelum ada teman\nyang online,\ncoba cari server',
    },
    'FriendsWindow.viewProfile': {
        'en': 'View Profile',
        'es': 'Ver Perfil',
        'pt': 'Ver Perfil',
        'ru': 'Просмотреть профиль',
        'hi': 'प्रोफ़ाइल देखें',
        'ml': 'പ്രൊഫൈൽ കാണുക',
        'id': 'Lihat Profil',
    },
    'FriendsWindow.deleteFriend': {
        'en': 'Delete Friend',
        'es': 'Eliminar Amigo',
        'pt': 'Excluir Amigo',
        'ru': 'Удалить друга',
        'hi': 'दोस्त\nहटाएँ',
        'ml': 'സുഹൃത്ത് ഇല്ലാതാക്കുക',
        'id': 'Hapus Teman',
    },
    'FriendsWindow.addFriend': {
        'en': 'Add\nTo Friends',
        'es': 'Agregar\nAmigo',
        'pt': 'Adicionar\nAmigo',
        'ru': 'Добавить\nв друзья',
        'hi': 'दोस्त\nजोड़ें',
        'ml': 'സുഹൃത്ത്\nചേർക്കുക',
        'id': 'Tambah\nTeman',
    },
    'FinderWindow.searchServers': {
        'en': 'Search All Servers',
        'es': 'Buscar todos los servidores',
        'pt': 'Buscar Todos os Servidores',
        'ru': 'Искать все серверы',
        'hi': 'सभी सर्वर खोजें',
        'ml': 'എല്ലാ സര്‍വറുകളും അന്വേഷിക്കുക',
        'id': 'Cari Semua Server',
    },
    'FinderWindow.searchPlayers': {
        'en': 'Search players without having to join a match',
        'es': 'Busca jugadores sin tener que unirse a partida',
        'pt': 'Busque jogadores sem precisar entrar em uma partida',
        'ru': 'Искать игроков без необходимости присоединяться к матчу',
        'hi': 'खिलाड़‍ियों को खोजें बिना मैच में जुड़ने की ज़रूरत',
        'ml': 'മത്സരത്തിൽ ചേരേണ്ടതില്ലാതെ കളിക്കാരെ തിരയുക',
        'id': 'Cari pemain tanpa harus bergabung ke pertandingan',
    },
    'FinderWindow.pressSearch': {
        'en': "Press search and\nI'll handle the rest!",
        'es': '¡Pulsa buscar y yo me\nencargo del resto!',
        'pt': 'Pressione buscar e\nEu cuido do resto!',
        'ru': 'Нажмите поиск, и\nя позабочусь об остальном!',
        'hi': 'सर्च दबाएँ और\nबाकी मैं संभाल लूँगा!',
        'ml': 'സെർച്ച് അമർത്തൂ,\nമറ്റെല്ലാം ഞാൻ നോക്കാം!',
        'id': 'Tekan cari dan\nbiar aku urus sisanya!',
    },
    'FinderWindow.filterDescription': {
        'en': 'Filter by player/server names or by specific characters',
        'es': 'Filtra por el nombre de los jugadores/servidores o por caracteres específicos',
        'pt': 'Filtre por nomes de jogadores/servidores ou por caracteres específicos',
        'ru': 'Фильтруйте по именам игроков/серверов или по определённым символам',
        'hi': 'खिलाड़ियों/सर्वरों के नाम या विशिष्ट अक्षरों के अनुसार फ़िल्टर करें',
        'ml': 'കളിക്കാരുടെ/സെർവറുകളുടെ പേരുകളോ പ്രത്യേക അക്ഷരങ്ങളോ അടിസ്ഥാനമാക്കി ഫിൽട്ടർ ചെയ്യുക',
        'id': 'Saring berdasarkan nama pemain/server atau karakter tertentu',
    },
    'FinderWindow.searchServersForPlayers': {
        'en': 'Search some servers\nto find players\nresults may vary\nby time and connection',
        'es': 'Busca en algunos servidores\npara encontrar jugadores\nLos resultados pueden variar\nsegún la hora y la conexión',
        'pt': 'Pesquise alguns servidores\npara encontrar jogadores\nos resultados podem variar\npor horário e conexão',
        'ru': 'Ищите на некоторых серверах,\nчтобы найти игроков\nрезультаты могут различаться\nв зависимости от времени и подключения',
        'hi': 'कुछ सर्वरों में खोजें\nखिलाड़ी खोजने के लिए\nपरिणाम बदल सकते हैं\nसमय और कनेक्शन के अनुसार',
        'ml': 'ചില സര്‍വറുകളില്‍ തിരയുക\nകളിക്കാരെ കണ്ടെത്താൻ\nഫലങ്ങൾ മാറാം\nസമയം മറ്റും കണക്ഷൻ അനുസരിച്ച്',
        'id': 'Cari di beberapa server\nuntuk menemukan pemain\nhasil dapat berbeda\nsesuai waktu dan koneksi',
    },
    'FinderWindow.selectToViewInfo': {
        'en': 'Select something to\nview server info',
        'es': 'Selecciona algo para\nver la info del servidor',
        'pt': 'Selecione algo para\nver informações do servidor',
        'ru': 'Выберите что-нибудь,\nчтобы просмотреть информацию о сервере',
        'hi': 'कुछ चुनें ताकि आप\nसर्वर की जानकारी देखें',
        'ml': 'ഏതെങ്കിലും തിരഞ്ഞെടുക്കുക\nസർവർ വിവരങ്ങൾ കാണാൻ',
        'id': 'Pilih sesuatu untuk\nmelihat info server',
    },
    'FinderWindow.scanningServers': {
        'en': 'Scanning servers!\nThis should take a few seconds.\nYou can close this window.',
        'es': '¡Escaneando servidores!\nEsto debería tardar unos segundos.\nPuedes cerrar esta ventana.',
        'pt': 'Escaneando servidores!\nIsso deve levar alguns segundos.\nVocê pode fechar esta janela.',
        'ru': 'Сканирование серверов!\nЭто займет несколько секунд.\nВы можете закрыть это окно.',
        'hi': 'सर्वर स्कैन हो रहे हैं!\nइसमें कुछ सेकंड लगेंगे।\nआप यह विंडो बंद कर सकते हैं।',
        'ml': 'സര്‍വറുകൾ സ്കാന്‍ ചെയ്യുന്നു!\nഇതിന് കുറച്ച് സെക്കൻഡ് മാത്രം എടുക്കും.\nഈ ജാലകം നിങ്ങൾക്ക് അടയ്ക്കാം.',
        'id': 'Sedang memindai server!\nIni seharusnya hanya\nmembutuhkan beberapa detik.\nAnda bisa menutup jendela ini.',
    },
    'FinderWindow.stillBusy': {
        'en': 'Still busy!',
        'es': '¡Sigo ocupado!',
        'pt': 'Ainda ocupado!',
        'ru': 'Все еще занят!',
        'hi': 'मैं अभी भी व्यस्त हूँ!',
        'ml': 'ഞാൻ ഇതുവരെ തിരക്കിലാണ്!',
        'id': 'Masih sibuk!',
    },
    'FinderWindow.searchProfiles': {
        'en': 'Search Profiles',
        'es': 'Buscar Perfiles',
        'pt': 'Buscar Perfis',
        'ru': 'Поиск профилей',
        'hi': 'प्रोफ़ाइल खोजें',
        'ml': 'പ്രൊഫൈലുകൾ തിരയുക',
        'id': 'Cari Profil',
    },
    'FinderWindow.changeColors': {
        'en': 'Change Colors',
        'es': 'Cambiar colores',
        'pt': 'Mudar Cores',
        'ru': 'Изменить цвета',
        'hi': 'रंग बदलें',
        'ml': 'നിറങ്ങൾ മാറ്റുക',
        'id': 'Ubah Warna',
    },
    'FinderWindow.changeLanguage': {
        'en': 'Change Language',
        'es': 'Cambiar idioma',
        'pt': 'Mudar Idioma',
        'ru': 'Изменить язык',
        'hi': 'भाषा बदलें',
        'ml': 'ഭാഷ മാറ്റുക',
        'id': 'Ubah Bahasa',
    },
    'Scan.finished': {
        'en': 'Finished!',
        'es': '¡Terminado!',
        'pt': 'Terminado!',
        'ru': 'Завершено!',
        'hi': 'समाप्त!',
        'ml': 'പൂർത്തിയായി!',
        'id': 'Selesai!',
    },
    'Scan.scanned': {
        'en': 'Scanned',
        'es': 'Escaneados',
        'pt': 'Escaneado',
        'ru': 'Отсканировано',
        'hi': 'स्कैन किए',
        'ml': 'സ്കാൻ ചെയ്തു',
        'id': 'Dipindai',
    },
    'Scan.servers': {
        'en': 'servers',
        'es': 'servidores',
        'pt': 'servidores',
        'ru': 'серверы',
        'hi': 'सर्वर',
        'ml': 'സർവർ',
        'id': 'server',
    },
    'Scan.in': {
        'en': 'in',
        'es': 'en',
        'pt': 'em',
        'ru': 'в',
        'hi': 'में',
        'ml': 'ഇൽ',
        'id': 'dalam',
    },
    'Scan.seconds': {
        'en': 'seconds!',
        'es': 'segundos!',
        'pt': 'segundos!',
        'ru': 'секунд!',
        'hi': 'सेकंड!',
        'ml': 'സെക്കൻഡുകൾ!',
        'id': 'detik!',
    },
    'Scan.approximately': {
        'en': 'Approximately',
        'es': 'Aproximadamente',
        'pt': 'Aproximadamente',
        'ru': 'Приблизительно',
        'hi': 'लगभग',
        'ml': 'ഏകദേശം',
        'id': 'Sekitar',
    },
    'Scan.server': {
        'en': 'servers',
        'es': 'servidores',
        'pt': 'servidores',
        'ru': 'серверы',
        'hi': 'सर्वर',
        'ml': 'സർവർ',
        'id': 'servers',
    },
    'Scan.perSecond': {
        'en': '/sec',
        'es': '/seg',
        'pt': '/seg',
        'ru': '/сек',
        'hi': '/सेक',
        'ml': '/സെക്',
        'id': '/detik',
    },
    'PartyWindow.host': {
        'en': 'host',
        'es': 'anfitrión',
        'pt': 'anfitrião',
        'ru': 'хост',
        'hi': 'होस्ट',
        'ml': 'ഹോസ്റ്റ്',
        'id': 'host',
    },
    'PartyWindow.addFriend': {
        'en': 'Add friend',
        'es': 'Agregar amigo',
        'pt': 'Adicionar amigo',
        'ru': 'Добавить друга',
        'hi': 'दोस्त जोड़ें',
        'ml': 'സുഹൃത്ത് ചേർക്കുക',
        'id': 'Tambah teman',
    },
    'PartyWindow.removeFriend': {
        'en': 'Remove friend',
        'es': 'Eliminar amigo',
        'pt': 'Remover amigo',
        'ru': 'Удалить друга',
        'hi': 'दोस्त हटाएं',
        'ml': 'സുഹൃത്തിനെ നീക്കുക',
        'id': 'Hapus teman',
    },
    'PartyWindow.areYouSureToKick': {
        'en': 'Are you sure to kick',
        'es': '¿Estás seguro de expulsar?',
        'pt': 'Tem certeza de que quer expulsar',
        'ru': 'Вы уверены, что хотите кикнуть',
        'hi': 'क्या आप वाकई निकालना चाहते हैं',
        'ml': 'നിങ്ങൾ പുറത്താക്കാൻ ഉറപ്പാണോ',
        'id': 'Apakah Anda yakin untuk mengeluarkan',
    },
    'PartyWindow.voteToKick': {
        'en': 'Vote to kick',
        'es': 'Votar para expulsar',
        'pt': 'Votar para expulsar',
        'ru': 'Голосовать за кик',
        'hi': 'निकालने के लिए मतदान',
        'ml': 'പുറത്താക്കാൻ വോട്ട് ചെയ്യുക',
        'id': 'Pemungutan suara untuk mengeluarkan',
    },
    'PartyWindow.viewAccount': {
        'en': 'View account',
        'es': 'Ver cuenta',
        'pt': 'Ver conta',
        'ru': 'Просмотреть аккаунт',
        'hi': 'खाता देखें',
        'ml': 'അക്കൗണ്ട് കാണുക',
        'id': 'Lihat akun',
    },
    'PartyWindow.mention': {
        'en': 'Mention',
        'es': 'Mencionar',
        'pt': 'Mencionar',
        'ru': 'Упомянуть',
        'hi': 'उल्लेख करें',
        'ml': 'പരാമർശിക്കുക',
        'id': 'Sebut',
    },
    'PartyWindow.kickById': {
        'en': 'Kick (ID: {})',
        'es': 'Expulsar (ID: {})',
        'pt': 'Expulsar (ID: {})',
        'ru': 'Кикнуть (ID: {})',
        'hi': 'निकालें (ID: {})',
        'ml': 'പുറത്താക്കുക (ID: {})',
        'id': 'Keluarkan (ID: {})',
    },
    'PartyWindow.addBlacklist': {
        'en': 'Blacklist',
        'es': 'Bloquear',
        'pt': 'Bloquear',
        'ru': 'Заблокировать',
        'hi': 'ब्लैकलिस्ट',
        'ml': 'ബ്ലോക്ക് ചെയ്യുക',
        'id': 'Blokir',
    },
    'PartyWindow.unblockUser': {
        'en': 'Unblock',
        'es': 'Desbloquear',
        'pt': 'Desbloquear',
        'ru': 'Разблокировать',
        'hi': 'अनब्लॉक करें',
        'ml': 'അൺബ്ലോക്ക് ചെയ്യുക',
        'id': 'Buka blokir',
    },
    'CreditsWindow.developer': {
        'en': 'Developer',
        'es': 'Desarrollador',
        'pt': 'Desenvolvedor',
        'ru': 'Разработчик',
        'hi': 'डेवलपर',
        'ml': 'ഡെവലപ്പർ',
        'id': 'Pengembang',
    },
    'CreditsWindow.motivation': {
        'en': 'Motivation',
        'es': 'Motivación',
        'pt': 'Motivação',
        'ru': 'Мотивация',
        'hi': 'प्रेरणा',
        'ml': 'പ്രേരണം',
        'id': 'Motivasi',
    },
    'CreditsWindow.motivationDescription': {
        'en': (
            "My motivation to create this was trying to make a friends system "
            "so you can easily find your friends and play some parties, also to "
            "see a player's level by viewing their profile and time spent playing BombSquad"
        ),
        'es': (
            'Mi motivación para crear esto fue intentar hacer un sistema de amigos '
            'para poder encontrar fácilmente a tus amigos y jugar algunas fiestas, '
            'también mirar el nivel de un jugador viendo su perfil y tiempo jugando BombSquad'
        ),
        'pt': (
            'Minha motivação para criar isso foi tentar fazer um sistema de amigos '
            'para que você possa encontrar facilmente seus amigos e jogar algumas festas, '
            'também para ver o nível de um jogador visualizando seu perfil e tempo gasto jogando BombSquad'
        ),
        'ru': (
            'Моей мотивацией для создания этого была попытка сделать систему друзей, '
            'чтобы вы могли легко находить своих друзей и играть в некоторые вечеринки, '
            'а также видеть уровень игрока, просматривая его профиль и время, '
            'проведенное за игрой в BombSquad'
        ),
        'hi': (
            'इसे बनाने की मेरी प्रेरणा एक मित्र प्रणाली बनाने की कोशिश थी ताकि आप अपने '
            'दोस्तों को आसानी से ढूंढ सकें और कुछ पार्टियाँ खेल सकें, साथ ही उनके प्रोफ़ाइल '
            'और BombSquad खेलने में बिताए गए समय को देखकर किसी खिलाड़ी का स्तर भी देख सकें'
        ),
        'ml': (
            'ഇത് സൃഷ്ടിക്കാൻ എനിക്ക് പ്രചോദനമായത് നിങ്ങളുടെ സുഹൃത്തുകളെ എളുപ്പത്തിൽ '
            'കണ്ടെത്താനും ചില പാർട്ടികൾ കളിക്കാനും കഴിയുന്ന ഒരു സുഹൃത്ത് സംവിധാനം ഉണ്ടാക്കുക'
        ),
        'id': (
            'Motivasi saya untuk membuat ini adalah mencoba membuat sistem teman agar dapat '
            'dengan mudah menemukan teman Anda dan bermain beberapa pesta, juga melihat level '
            'seorang pemain dengan melihat profil mereka dan waktu bermain BombSquad'
        ),
    },
    'CreditsWindow.inspiration': {
        'en': 'Inspiration',
        'es': 'Inspiración',
        'pt': 'Inspiração',
        'ru': 'Вдохновение',
        'hi': 'प्रेरणा',
        'ml': 'പ്രചോദനം',
        'id': 'Inspirasi',
    },
    'CreditsWindow.inspirationDescription': {
        'en': (
            'This is my first official mod, I took inspiration from features of some mods '
            'I saw within the community, I hope they do not mind, in the same way I will list them below'
        ),
        'es': (
            'Este es mi primer mod oficial, tomé como inspiración funcionalidades de algunos mods '
            'que vi dentro de la comunidad, espero no se molesten, de igual forma los pondré aquí abajo'
        ),
        'pt': (
            'Este é meu primeiro mod oficial, me inspirei em recursos de alguns mods que vi na '
            'comunidade, espero que não se importem, da mesma forma os listarei abaixo'
        ),
        'ru': (
            'Это мой первый официальный мод, я черпал вдохновение из функций некоторых модов, '
            'которые я видел в сообществе, надеюсь, они не против, точно так же я перечислю их ниже'
        ),
        'hi': (
            'यह मेरा पहला आधिकारिक मॉड है, मैंने समुदाय के भीतर देखे गए कुछ मॉड्स की '
            'विशेषताओं से प्रेरणा ली है, आशा है कि उन्हें आपत्ति नहीं होगी, '
            'इसी तरह मैं उन्हें नीचे सूचीबद्ध करूँगा'
        ),
        'ml': (
            'ഇത് എന്റെ ആദ്യ ഔദ്യോഗിക മോഡാണ്, കമ്മ്യൂണിറ്റിക്കുള്ളിൽ ഞാൻ കണ്ട ചില '
            'മോഡുകളുടെ സവിശേഷതകളിൽ നിന്ന് ഞാൻ പ്രചോദനം നേടി, അവർക്ക് അതിൽ '
            'പ്രശ്നമില്ലെന്ന് ഞാൻ പ്രതീക്ഷിക്കുന്നു, അതുപോലെ അവയെ ഞാൻ താഴെ ചേർക്കും'
        ),
        'id': (
            'Ini adalah mod resmi pertama saya, saya mengambil inspirasi dari fitur beberapa mod '
            'yang saya lihat di dalam komunitas, saya harap mereka tidak keberatan, '
            'dengan cara yang sama saya akan mencantumkannya di bawah'
        ),
    },
    'CreditsWindow.thanksMessage': {
        'en': (
            'Thank you \ue063VanyOne for trying this and making the preview video, '
            'and to the people who helped with their opinions and support. '
            'I may add new features in the future. I know it is not perfect and that '
            'there are several bugs, but that is all for now. '
            'I will gradually fix the existing issues. I hope you enjoy it, with love - \ue043Less'
        ),
        'es': (
            'Gracias \ue063VanyOne por probar esto y hacer el video preview, '
            'y a las personas que ayudaron con sus opiniones y apoyo. '
            'Puede que añada nuevas funcionalidades en un futuro. '
            'Sé que no es perfecto y que hay varios errores, pero es todo por el momento. '
            'Igual solucionaré gradualmente los errores que existen. '
            'Espero lo disfruten, con cariño - \ue043Less'
        ),
        'pt': (
            'Obrigado \ue063VanyOne por testar isso e fazer o vídeo de prévia, '
            'e às pessoas que ajudaram com suas opiniões e apoio. '
            'Posso adicionar novas funcionalidades no futuro. '
            'Sei que não é perfeito e que há vários erros, mas por enquanto é só isso. '
            'Também corrigirei gradualmente os erros existentes. '
            'Espero que você goste, com carinho - \ue043Less'
        ),
        'ru': (
            'Спасибо \ue063VanyOne за то, что попробовали это и сделали видео-превью, '
            'а также людям, которые помогли своими мнениями и поддержкой. '
            'Возможно, я добавлю новые функции в будущем. '
            'Я знаю, что это не идеально и что есть несколько ошибок, но на данный момент это всё. '
            'Я буду постепенно исправлять существующие ошибки. '
            'Надеюсь, вам понравится, с любовью - \ue043Less'
        ),
        'hi': (
            '\ue063VanyOne को इसे आज़माने और प्रीव्यू वीडियो बनाने के लिए धन्यवाद, '
            'साथ ही उन लोगों को भी जिन्होंने अपनी राय और समर्थन से मदद की। '
            'मैं भविष्य में नई सुविधाएँ जोड़ सकता हूँ। '
            'मुझे पता है कि यह परफेक्ट नहीं है और इसमें कई त्रुटियाँ हैं, लेकिन फिलहाल इतना ही है। '
            'मैं मौजूदा समस्याओं को धीरे-धीरे ठीक करता रहूँगा। '
            'आशा है कि आप इसका आनंद लेंगे, स्नेह सहित - \ue043Less'
        ),
        'ml': (
            '\ue063VanyOne ഇത് പരീക്ഷിക്കുകയും പ്രിവ്യൂ വീഡിയോ തയ്യാറാക്കുകയും ചെയ്തതിന് നന്ദി, '
            'അവരുടെ അഭിപ്രായങ്ങളും പിന്തുണയും നൽകിയ എല്ലാവർക്കും നന്ദി. '
            'ഭാവിയിൽ ഞാൻ പുതിയ ഫീച്ചറുകൾ ചേർക്കാൻ സാധ്യതയുണ്ട്. '
            'ഇത് പൂർണ്ണമായതല്ലെന്നും പല പിശകുകളും ഉണ്ടെന്നും എനിക്ക് അറിയാം, '
            'പക്ഷേ ഇപ്പോൾ ഇത്രയേ ഉള്ളൂ. '
            'നിലവിലുള്ള പ്രശ്നങ്ങൾ ഞാൻ ക്രമേണ പരിഹരിക്കും. '
            'നിങ്ങൾ ഇത് ആസ്വദിക്കുമെന്ന് ഞാൻ പ്രതീക്ഷിക്കുന്നു, സ്നേഹത്തോടെ - \ue043Less'
        ),
        'id': (
            'Terima kasih \ue063VanyOne telah mencoba ini dan membuat video pratinjau, '
            'serta kepada orang-orang yang membantu dengan pendapat dan dukungan mereka. '
            'Saya mungkin akan menambahkan fitur baru di masa depan. '
            'Saya tahu ini belum sempurna dan masih ada beberapa kesalahan, tetapi untuk saat ini hanya itu. '
            'Saya akan memperbaiki masalah yang ada secara bertahap. '
            'Semoga kalian menikmatinya, dengan penuh kasih - \ue043Less'
        ),
    },
    'chatViewProfile': {
        'en': 'Players Full Profile',
        'es': 'Perfil Completo del Jugador',
        'pt': 'Perfil Completo do Jogador',
        'ru': 'Полный профиль игрока',
        'hi': 'Players ka Pura Profile',
        'ml': 'Playersinte Purna Profile',
        'id': 'Profil Pemain Lengkap',
    },
    'chatViewAccount': {
        'en': 'Players Account Name',
        'es': 'Nombre de Cuenta del Jugador',
        'pt': 'Nome da Conta do Jogador',
        'ru': 'Имя аккаунта игрока',
        'hi': 'Players ka Account Naam',
        'ml': 'Playersinte Account Peru',
        'id': 'Nama Akun Pemain',
    },
    'chatViewMulti': {
        'en': 'Players Account & Profile',
        'es': 'Cuenta y Perfil del Jugador',
        'pt': 'Conta e Perfil do Jogador',
        'ru': 'Аккаунт и профиль игрока',
        'hi': 'Players ka Account aur Profile',
        'ml': 'Playersinte Accountum Profileum',
        'id': 'Akun & Profil Pemain',
    },
    'chatViewMultiV2': {
        'en': 'Players Account & Profile V.2',
        'es': 'Cuenta y Perfil del Jugador V.2',
        'pt': 'Conta e Perfil do Jogador V.2',
        'ru': 'Аккаунт и профиль игрока V.2',
        'hi': 'Players ka Account aur Profile V.2',
        'ml': 'Playersinte Accountum Profileum V.2',
        'id': 'Akun & Profil Pemain V.2',
    },
    'chatShowCid': {
        'en': "View Players' ClientID",
        'es': 'Ver ClientID del Jugador',
        'pt': 'Ver ClientID do Jogador',
        'ru': 'Просмотреть ClientID игрока',
        'hi': 'Players ka ClientID Dekhein',
        'ml': 'Playersinte ClientID Kaanuka',
        'id': 'Tampilkan ClientID Pemain',
    },
    'chatHideCid': {
        'en': "Hide Players' ClientID",
        'es': 'Ocultar ClientID del Jugador',
        'pt': 'Ocultar ClientID do Jogador',
        'ru': 'Скрыть ClientID игрока',
        'hi': 'Players ka ClientID Chhupao',
        'ml': 'Playersinte ClientID Marachuka',
        'id': 'Sembunyikan ClientID Pemain',
    },
    'chatViewOff': {
        'en': 'Turn Off Chat Name Viewer',
        'es': 'Apagar Visor de Nombres del Chat',
        'pt': 'Desligar Visualizador de Nomes do Chat',
        'ru': 'Выключить просмотр имен в чате',
        'hi': 'Chat Name Viewer Band Karo',
        'ml': 'Chat Name Viewer Off Akkuka',
        'id': 'Matikan Penampil Nama Chat',
    },
    'translateSettingsTitle': {
        'en': 'Translation Settings',
        'es': 'Configuración de Traducción',
        'pt': 'Configurações de Tradução',
        'ru': 'Настройки перевода',
        'hi': 'Anuvaad Settings',
        'ml': 'Mozhi Mattal Settings',
        'id': 'Pengaturan Terjemahan',
    },
    'translateSettingsTextfield': {
        'en': 'TextField Texts',
        'es': 'Textos de Campo de Texto',
        'pt': 'Textos do Campo de Texto',
        'ru': 'Тексты текстовых полей',
        'hi': 'TextField Texts',
        'ml': 'TextField Texts',
        'id': 'Kolom Teks',
    },
    'translateSettingsOther': {
        'en': 'Other Texts',
        'es': 'Otros Textos',
        'pt': 'Outros Textos',
        'ru': 'Другие тексты',
        'hi': 'Anya Texts',
        'ml': 'Mattulla Texts',
        'id': 'Teks Lainnya',
    },
    'translateMethod': {
        'en': 'Translate Method',
        'es': 'Método de Traducción',
        'pt': 'Método de Tradução',
        'ru': 'Метод перевода',
        'hi': 'Anuvaad Prakriya',
        'ml': 'Mozhi Mattal Padhathi',
        'id': 'Metode Penerjemahan',
    },
    'translateMethodAPI': {
        'en': 'API',
        'es': 'API',
        'pt': 'API',
        'ru': 'API',
        'hi': 'API',
        'ml': 'API',
        'id': 'API',
    },
    'translateMethodLINK': {
        'en': 'Link',
        'es': 'Enlace',
        'pt': 'Link',
        'ru': 'Ссылка',
        'hi': 'Link',
        'ml': 'Link',
        'id': 'Tautan',
    },
    'ChatPopup.translateText': {
        'en': 'Translate Text',
        'es': 'Traducir Texto',
        'pt': 'Traduzir Texto',
        'ru': 'Перевести текст',
        'hi': 'टेक्स्ट अनुवाद करें',
        'ml': 'ടെക്സ്റ്റ് വിവർത്തനം ചെയ്യുക',
        'id': 'Terjemahkan Teks',
    },
    'ChatPopup.copyText': {
        'en': 'Copy Text',
        'es': 'Copiar Texto',
        'pt': 'Copiar Texto',
        'ru': 'Копировать текст',
        'hi': 'टेक्स्ट कॉपी करें',
        'ml': 'ടെക്സ്റ്റ് പകർത്തുക',
        'id': 'Salin Teks',
    },
    'ChatPopup.copyMessage': {
        'en': 'Copy Message',
        'es': 'Copiar Mensaje',
        'pt': 'Copiar Mensagem',
        'ru': 'Копировать сообщение',
        'hi': 'संदेश कॉपी करें',
        'ml': 'സന്ദേശം പകർത്തുക',
        'id': 'Salin Pesan',
    },
    'ChatPopup.insertText': {
        'en': 'Insert Text',
        'es': 'Insertar Texto',
        'pt': 'Inserir Texto',
        'ru': 'Вставить текст',
        'hi': 'टेक्स्ट डालें',
        'ml': 'ടെക്സ്റ്റ് തിരുകുക',
        'id': 'Sisipkan Teks',
    },
    'ChatPopup.playerOption': {
        'en': 'Player Options',
        'es': 'Opciones de Jugador',
        'pt': 'Opções de Jogador',
        'ru': 'Опции игрока',
        'hi': 'खिलाड़ी विकल्प',
        'ml': 'കളിക്കാരന്റെ ഓപ്ഷനുകൾ',
        'id': 'Opsi Pemain',
    },
    'ChatPopup.playerNotFound': {
        'en': 'Player not found in records',
        'es': 'Jugador no encontrado en registros',
        'pt': 'Jogador não encontrado nos registros',
        'ru': 'Игрок не найден в записях',
        'hi': 'खिलाड़ी रिकॉर्ड में नहीं मिला',
        'ml': 'കളിക്കാരൻ രേഖകളിൽ കണ്ടെത്തിയില്ല',
        'id': 'Pemain tidak ditemukan di catatan',
    },
    'Menu.muteChatsOption': {
        'en': 'Mute Chats Option',
        'es': 'Opción de Silenciar Chats',
        'pt': 'Opção de Silenciar Chats',
        'ru': 'Опция отключения чатов',
        'hi': 'Chat Bisu Vikalp',
        'ml': 'Chats Mute Option',
        'id': 'Opsi Bisu Pesan',
    },
    'Menu.muteChat': {
        'en': 'Mute Chat',
        'es': 'Silenciar Chat',
        'pt': 'Silenciar Chat',
        'ru': 'Отключить чат',
        'hi': 'Chat Mute Karein',
        'ml': 'Chat Mute Cheyyuka',
        'id': 'Bisukan Chat',
    },
    'Menu.unmuteChat': {
        'en': 'Unmute Chat',
        'es': 'Activar Chat',
        'pt': 'Ativar Chat',
        'ru': 'Включить чат',
        'hi': 'Chat Unmute Karein',
        'ml': 'Chat Unmute Cheyyuka',
        'id': 'Aktifkan Chat',
    },
    'Menu.muteUsers': {
        'en': 'Mute Users',
        'es': 'Silenciar Usuarios',
        'pt': 'Silenciar Usuários',
        'ru': 'Заглушить пользователей',
        'hi': 'Users Mute Karein',
        'ml': 'Users Mute Cheyyuka',
        'id': 'Bisukan Pengguna',
    },
    'Menu.modifyColor': {
        'en': 'Modify PartyWindow Color',
        'es': 'Modificar Color de PartyWindow',
        'pt': 'Modificar Cor da PartyWindow',
        'ru': 'Изменить цвет окна группы',
        'hi': 'PartyWindow Rang Badlo',
        'ml': 'PartyWindow Color Modify Cheyyuka',
        'id': 'Ubah Warna PartyWindow',
    },
    'Menu.saveReplay': {
        'en': 'Save Last Game Replay',
        'es': 'Guardar Repetición del Último Juego',
        'pt': 'Salvar Replay do Último Jogo',
        'ru': 'Сохранить повтор последней игры',
        'hi': 'Aakhri Khel Replay Ko Save Karein',
        'ml': 'Last Game Replay Save Cheyyuka',
        'id': 'Simpan Game Replay Terakhir',
    },
    'Menu.replaySaved': {
        'en': 'Replay saved!',
        'es': '¡Repetición guardada!',
        'pt': 'Replay salvo!',
        'ru': 'Повтор сохранён!',
        'hi': 'Replay save ho gaya!',
        'ml': 'Replay save aayi!',
        'id': 'Replay tersimpan!',
    },
    'Menu.replayNoLastReplay': {
        'en': 'No last game replay found',
        'es': 'No se encontró repetición del último juego',
        'pt': 'Nenhum replay do último jogo encontrado',
        'ru': 'Последний повтор игры не найден',
        'hi': 'Koi last replay nahi mila',
        'ml': 'Last replay kittiyilla',
        'id': 'Tidak ada replay terakhir ditemukan',
    },
    'Menu.replaySaveFailed': {
        'en': 'Failed to save replay',
        'es': 'Error al guardar la repetición',
        'pt': 'Falha ao salvar o replay',
        'ru': 'Не удалось сохранить повтор',
        'hi': 'Replay save karne mein galti',
        'ml': 'Replay save cheyyaan kazhiyilla',
        'id': 'Gagal menyimpan replay',
    },
    'MuteUsersWindow.title': {
        'en': 'Mute Users',
        'es': 'Silenciar Usuarios',
        'pt': 'Silenciar Usuários',
        'ru': 'Заглушить пользователей',
        'hi': 'Users Mute Karein',
        'ml': 'Users Mute Cheyyuka',
        'id': 'Bisukan Pengguna',
    },
    'MuteUsersWindow.noPlayers': {
        'en': 'No players in party',
        'es': 'No hay jugadores en la sala',
        'pt': 'Não há jogadores na sala',
        'ru': 'Нет игроков в группе',
        'hi': 'Party mein koi player nahi',
        'ml': 'Party-il players illaa',
        'id': 'Tidak ada pemain di pesta',
    },
    'saveReplayTitle': {
        'en': 'Save Replay',
        'es': 'Guardar Repetición',
        'pt': 'Salvar Replay',
        'ru': 'Сохранить повтор',
        'hi': 'Replay Save Karein',
        'ml': 'Replay Save Cheyyuka',
        'id': 'Simpan Replay',
    },
    'saveReplayEnter': {
        'en': 'Save',
        'es': 'Guardar',
        'pt': 'Salvar',
        'ru': 'Сохранить',
        'hi': 'Save Karein',
        'ml': 'Save Cheyyuka',
        'id': 'Simpan',
    },
    'saveReplayInfoDate': {
        'en': 'Click to insert {} → replaced with current date',
        'es': 'Haz clic para insertar {} → se reemplaza con la fecha actual',
        'pt': 'Clique para inserir {} → substituído pela data atual',
        'ru': 'Нажмите, чтобы вставить {} → заменяется текущей датой',
        'hi': '{} insert karne ke liye click karein → current date se badla jaega',
        'ml': '{} insert cheyyaan click cheyyuka → current date aakum',
        'id': 'Klik untuk menyisipkan {} → diganti dengan tanggal saat ini',
    },
    'saveReplayInfoTime': {
        'en': 'Click to insert {} → replaced with current time',
        'es': 'Haz clic para insertar {} → se reemplaza con la hora actual',
        'pt': 'Clique para inserir {} → substituído pela hora atual',
        'ru': 'Нажмите, чтобы вставить {} → заменяется текущим временем',
        'hi': '{} insert karne ke liye click karein → current time se badla jaega',
        'ml': '{} insert cheyyaan click cheyyuka → current time aakum',
        'id': 'Klik untuk menyisipkan {} → diganti dengan waktu saat ini',
    },
    'saveReplayConfirmReplaceDefault': {
        'en': 'Replace current text with the default name',
        'es': 'Reemplazar el texto actual con el nombre por defecto',
        'pt': 'Substituir o texto atual pelo nome padrão',
        'ru': 'Заменить текущий текст именем по умолчанию',
        'hi': 'Current text ko default naam se replace karein',
        'ml': 'Current text default name kondu replace cheyyuka',
        'id': 'Ganti teks saat ini dengan nama default',
    },
    'saveReplayEmptyName': {
        'en': 'Name cannot be empty',
        'es': 'El nombre no puede estar vacío',
        'pt': 'O nome não pode estar vazio',
        'ru': 'Имя не может быть пустым',
        'hi': 'Naam khali nahi ho sakta',
        'ml': 'Naam kaali aakaan patilla',
        'id': 'Nama tidak boleh kosong',
    },
    'saveReplayOverwriteConfirm': {
        'en': 'A replay with this name already exists. Overwrite it',
        'es': 'Ya existe una repetición con este nombre. ¿Sobrescribirla',
        'pt': 'Já existe um replay com este nome. Sobrescrever',
        'ru': 'Повтор с таким именем уже существует. Перезаписать',
        'hi': 'Is naam ka replay pehle se hai. Overwrite karein',
        'ml': 'Ee perinte replay undaayirunnu. Overwrite cheyyuka',
        'id': 'Replay dengan nama ini sudah ada. Timpa',
    },
    'DMWindow.title': {
        'en': 'Direct Messages',
        'es': 'Mensajes Directos',
        'pt': 'Mensagens Diretas',
        'ru': 'Личные сообщения',
        'hi': 'Direct Messages',
        'ml': 'Direct Messages',
        'id': 'Pesan Langsung',
    },
    'Settings.title': {
        'en': 'Settings',
        'es': 'Ajustes',
        'pt': 'Configurações',
        'ru': 'Настройки',
        'hi': 'Settings',
        'ml': 'Settings',
        'id': 'Pengaturan',
    },
    'Settings.sectionInterface': {
        'en': 'Interface',
        'es': 'Interfaz',
        'pt': 'Interface',
        'ru': 'Интерфейс',
        'hi': 'Interface',
        'ml': 'Interface',
        'id': 'Antarmuka',
    },
    'Settings.sectionOptions': {
        'en': 'Options',
        'es': 'Opciones',
        'pt': 'Opções',
        'ru': 'Настройки',
        'hi': 'Options',
        'ml': 'Options',
        'id': 'Opsi',
    },
    'Settings.sectionTheme': {
        'en': 'Theme',
        'es': 'Tema',
        'pt': 'Tema',
        'ru': 'Тема',
        'hi': 'Theme',
        'ml': 'Theme',
        'id': 'Tema',
    },
    'Settings.language': {
        'en': 'Language',
        'es': 'Idioma',
        'pt': 'Idioma',
        'ru': 'Язык',
        'hi': 'भाषा',
        'ml': 'ഭാഷ',
        'id': 'Bahasa',
    },
    'Settings.dmNotifications': {
        'en': 'Show screen notifications for direct messages',
        'es': 'Mostrar notificaciones en pantalla de mensajes directos',
        'pt': 'Mostrar notificações de mensagens diretas na tela',
        'ru': 'Показывать уведомления для личных сообщений',
        'hi': 'Show screen notifications for direct messages',
        'ml': 'Show screen notifications for direct messages',
        'id': 'Tampilkan notifikasi layar untuk pesan langsung',
    },
    'Settings.chatViewerType': {
        'en': 'Chat name style',
        'es': 'Estilo de nombres en el chat',
        'pt': 'Estilo de nome no chat',
        'ru': 'Стиль имён в чате',
        'hi': 'Chat name style',
        'ml': 'Chat name style',
        'id': 'Gaya nama chat',
    },
    'Settings.chatViewerDisabled': {
        'en': 'Disabled',
        'es': 'Desactivado',
        'pt': 'Desativado',
        'ru': 'Отключено',
        'hi': 'Disabled',
        'ml': 'Disabled',
        'id': 'Dinonaktifkan',
    },
    'Settings.chatViewerProfile': {
        'en': 'Profile',
        'es': 'Perfil',
        'pt': 'Perfil',
        'ru': 'Профиль',
        'hi': 'Profile',
        'ml': 'Profile',
        'id': 'Profil',
    },
    'Settings.chatViewerAccount': {
        'en': 'Account',
        'es': 'Cuenta',
        'pt': 'Conta',
        'ru': 'Аккаунт',
        'hi': 'Account',
        'ml': 'Account',
        'id': 'Akun',
    },
    'Settings.chatViewerMulti': {
        'en': 'Multi',
        'es': 'Multi',
        'pt': 'Multi',
        'ru': 'Мульти',
        'hi': 'Multi',
        'ml': 'Multi',
        'id': 'Multi',
    },
    'Settings.chatViewerMultiV2': {
        'en': 'Multi V2',
        'es': 'Multi V2',
        'pt': 'Multi V2',
        'ru': 'Мульти V2',
        'hi': 'Multi V2',
        'ml': 'Multi V2',
        'id': 'Multi V2',
    },
    'Settings.showClientId': {
        'en': 'Show client ID',
        'es': 'Mostrar ID de cliente',
        'pt': 'Mostrar ID do cliente',
        'ru': 'Показывать ID клиента',
        'hi': 'Client ID dikhayein',
        'ml': 'Client ID kaanikkuka',
        'id': 'Tampilkan ID klien',
    },
    'Settings.sectionReset': {
        'en': 'Reset',
        'es': 'Restablecer',
        'pt': 'Redefinir',
        'ru': 'Сброс',
        'hi': 'Reset',
        'ml': 'Reset',
        'id': 'Reset',
    },
    'Settings.resetConfig': {
        'en': 'Reset all settings',
        'es': 'Restablecer configuración',
        'pt': 'Redefinir configurações',
        'ru': 'Сбросить настройки',
        'hi': 'Reset all settings',
        'ml': 'Reset all settings',
        'id': 'Reset semua pengaturan',
    },
    'Settings.resetConfigConfirm': {
        'en': 'Reset all settings to default?',
        'es': '¿Restablecer toda la configuración?',
        'pt': 'Redefinir todas as configurações?',
        'ru': 'Сбросить все настройки?',
        'hi': 'Reset all settings to default?',
        'ml': 'Reset all settings to default?',
        'id': 'Reset semua pengaturan ke default?',
    },
    'Settings.translationSettings': {
        'en': 'Translation settings',
        'es': 'Ajustes de traducción',
        'pt': 'Configurações de tradução',
        'ru': 'Настройки перевода',
        'hi': 'Translation settings',
        'ml': 'Translation settings',
        'id': 'Pengaturan terjemahan',
    },
    'Settings.changeThemeColor': {
        'en': 'Change theme color',
        'es': 'Cambiar color del tema',
        'pt': 'Alterar cor do tema',
        'ru': 'Изменить цвет темы',
        'hi': 'Theme color badlein',
        'ml': 'Theme color maattuka',
        'id': 'Ubah warna tema',
    },
    'Settings.colorsUpdated': {
        'en': 'Colors updated',
        'es': 'Colores actualizados',
        'pt': 'Cores atualizadas',
        'ru': 'Цвета обновлены',
        'hi': 'Colors update ho gaye',
        'ml': 'Colors update cheythu',
        'id': 'Warna diperbarui',
    },
    'Settings.useTheme': {
        'en': 'Auto theme',
        'es': 'Tema automático',
        'pt': 'Tema automático',
        'ru': 'Авто тема',
        'hi': 'Auto theme',
        'ml': 'Auto theme',
        'id': 'Tema otomatis',
    },
    'Settings.colorBackground': {
        'en': 'Primary Background',
        'es': 'Fondo primario',
        'pt': 'Fundo primário',
        'ru': 'Основной фон',
        'hi': 'Primary Background',
        'ml': 'Primary Background',
        'id': 'Latar utama',
    },
    'Settings.colorButton': {
        'en': 'Secondary Background',
        'es': 'Fondo secundario',
        'pt': 'Fundo secundário',
        'ru': 'Вторичный фон',
        'hi': 'Secondary Background',
        'ml': 'Secondary Background',
        'id': 'Latar sekunder',
    },
    'Settings.colorPrimary': {
        'en': 'Primary Color',
        'es': 'Color primario',
        'pt': 'Cor primária',
        'ru': 'Основной цвет',
        'hi': 'Primary Color',
        'ml': 'Primary Color',
        'id': 'Warna utama',
    },
    'Settings.colorSecondary': {
        'en': 'Secondary Color',
        'es': 'Color secundario',
        'pt': 'Cor secundária',
        'ru': 'Вторичный цвет',
        'hi': 'Secondary Color',
        'ml': 'Secondary Color',
        'id': 'Warna sekunder',
    },
    'Settings.colorTertiary': {
        'en': 'Tertiary Color',
        'es': 'Color terciario',
        'pt': 'Cor terciária',
        'ru': 'Третичный цвет',
        'hi': 'Tertiary Color',
        'ml': 'Tertiary Color',
        'id': 'Warna tersier',
    },
    'Settings.colorAccent': {
        'en': 'Accent',
        'es': 'Acento',
        'pt': 'Acento',
        'ru': 'Акцент',
        'hi': 'Accent',
        'ml': 'Accent',
        'id': 'Aksen',
    },
    'Settings.uiScale': {
        'en': 'UI Scale',
        'es': 'Escala de interfaz',
        'pt': 'Escala da interface',
        'ru': 'Масштаб интерфейса',
        'hi': 'UI Scale',
        'ml': 'UI Scale',
        'id': 'Skala antarmuka',
    },
    'Settings.uiScaleSmall': {
        'en': 'Small',
        'es': 'Pequeño',
        'pt': 'Pequeno',
        'ru': 'Маленький',
        'hi': 'Small',
        'ml': 'Small',
        'id': 'Kecil',
    },
    'Settings.uiScaleMedium': {
        'en': 'Medium',
        'es': 'Mediano',
        'pt': 'Médio',
        'ru': 'Средний',
        'hi': 'Medium',
        'ml': 'Medium',
        'id': 'Sedang',
    },
    'Settings.uiScaleLarge': {
        'en': 'Large',
        'es': 'Grande',
        'pt': 'Grande',
        'ru': 'Большой',
        'hi': 'Large',
        'ml': 'Large',
        'id': 'Besar',
    },
    'PartyWindow.title': {
        'en': 'Your Party',
        'es': 'Tu Fiesta',
        'pt': 'Sua Festa',
        'ru': 'Ваша Вечеринка',
        'hi': 'आपकी पार्टी',
        'ml': 'നിങ്ങളുടെ പാർട്ടി',
        'id': 'Pesta Anda',
    },
    'PartyWindow.emptyStr': {
        'en': 'Your party is empty.',
        'es': 'Tu fiesta está vacía.',
        'pt': 'Sua festa está vazia.',
        'ru': 'Ваша вечеринка пуста.',
        'hi': 'आपकी पार्टी खाली है।',
        'ml': 'നിങ്ങളുടെ പാർട്ടി ശൂന്യമാണ്.',
        'id': 'Pesta Anda kosong.',
    },
    'PartyWindow.emptyStr2': {
        'en': 'Use the gather window to assemble the party.',
        'es': 'Usa la ventana de reunión para armar una fiesta.',
        'pt': 'Use a janela de reunião para montar uma festa.',
        'ru': 'Используйте окно сбора, чтобы собрать вечеринку.',
        'hi': 'पार्टी बनाने के लिए गेदर विंडो का उपयोग करें।',
        'ml': 'പാർട്ടി ഒരുക്കാൻ ഗ്യാതർ വിൻഡോ ഉപയോഗിക്കുക.',
        'id': 'Gunakan jendela kumpul untuk membentuk sebuah pesta.',
    },
    'PartyWindow.chatMuted': {
        'en': 'Chat Muted',
        'es': 'Chat Silenciado',
        'pt': 'Chat Silenciado',
        'ru': 'Чат отключён',
        'hi': 'चैट म्यूट है',
        'ml': 'ചാറ്റ് മ്യൂട്ടാണ്',
        'id': 'Obrolan Dimatikan',
    },
    'FriendAction.inviteToParty': {
        'en': 'Invite to Party',
        'es': 'Invitar a la Fiesta',
        'pt': 'Convidar para a Festa',
        'ru': 'Пригласить на вечеринку',
        'hi': 'पार्टी में आमंत्रित करें',
        'ml': 'പാർട്ടിയിലേക്ക് ക്ഷണിക്കുക',
        'id': 'Undang ke Pesta',
    },
    'FriendAction.sendMessage': {
        'en': 'Send Message',
        'es': 'Enviar Mensaje',
        'pt': 'Enviar Mensagem',
        'ru': 'Отправить сообщение',
        'hi': 'संदेश भेजें',
        'ml': 'സന്ദേശം അയക്കുക',
        'id': 'Kirim Pesan',
    },
    'FriendAction.viewAccount': {
        'en': 'View Account',
        'es': 'Ver Cuenta',
        'pt': 'Ver Conta',
        'ru': 'Посмотреть аккаунт',
        'hi': 'अकाउंट देखें',
        'ml': 'അക്കൗണ്ട് കാണുക',
        'id': 'Lihat Akun',
    },
    'DM.requests': {
        'en': 'Friend Requests',
        'es': 'Solicitudes de Amistad',
        'pt': 'Pedidos de Amizade',
        'ru': 'Запросы в друзья',
        'hi': 'मित्र अनुरोध',
        'ml': 'സ്നേഹിത അഭ്യർത്ഥനകൾ',
        'id': 'Permintaan Teman',
    },
    'DM.requestsReceived': {
        'en': 'Received',
        'es': 'Recibidas',
        'pt': 'Recebidas',
        'ru': 'Полученные',
        'hi': 'प्राप्त',
        'ml': 'ലഭിച്ചത്',
        'id': 'Diterima',
    },
    'DM.requestsSent': {
        'en': 'Sent',
        'es': 'Enviadas',
        'pt': 'Enviadas',
        'ru': 'Отправленные',
        'hi': 'भेजे गए',
        'ml': 'അയച്ചത്',
        'id': 'Terkirim',
    },
    'DM.noRequests': {
        'en': 'No pending requests',
        'es': 'Sin solicitudes',
        'pt': 'Sem pedidos',
        'ru': 'Нет запросов',
        'hi': 'कोई अनुरोध नहीं',
        'ml': 'അഭ്യർത്ഥനകൾ ഇല്ല',
        'id': 'Tidak ada permintaan',
    },
    'DM.noSentRequests': {
        'en': 'No sent requests',
        'es': 'Sin solicitudes enviadas',
        'pt': 'Sem pedidos enviados',
        'ru': 'Нет отправленных',
        'hi': 'कोई भेजा नहीं',
        'ml': 'ഒന്നും അയച്ചിട്ടില്ല',
        'id': 'Tidak ada yang terkirim',
    },
    'DM.friends': {
        'en': 'Friends',
        'es': 'Amigos',
        'pt': 'Amigos',
        'ru': 'Друзья',
        'hi': 'मित्र',
        'ml': 'സ്നേഹിതർ',
        'id': 'Teman',
    },
    'DM.noDescription': {
        'en': 'No description',
        'es': 'Sin descripción',
        'pt': 'Sem descrição',
        'ru': 'Нет описания',
        'hi': 'कोई विवरण नहीं',
        'ml': 'വിവരണം ഇല്ല',
        'id': 'Tidak ada deskripsi',
    },
    'DM.globalChat': {
        'en': 'Global Chat',
        'es': 'Chat Global',
        'pt': 'Chat Global',
        'ru': 'Общий чат',
        'hi': 'ग्लोबल चैट',
        'ml': 'ഗ്ലോബൽ ചാറ്റ്',
        'id': 'Obrolan Global',
    },
    'DM.add': {
        'en': '+ Add',
        'es': '+ Agregar',
        'pt': '+ Adicionar',
        'ru': '+ Добавить',
        'hi': '+ जोड़ें',
        'ml': '+ ചേർക്കുക',
        'id': '+ Tambah',
    },
    'DM.backToGlobalChat': {
        'en': '< Global Chat',
        'es': '< Chat Global',
        'pt': '< Chat Global',
        'ru': '< Общий чат',
        'hi': '< ग्लोबल चैट',
        'ml': '< ഗ്ലോബൽ ചാറ്റ്',
        'id': '< Obrolan Global',
    },
    'DM.manageAccount': {
        'en': 'Manage Account',
        'es': 'Administrar Cuenta',
        'pt': 'Gerenciar Conta',
        'ru': 'Управление аккаунтом',
        'hi': 'Manage Account',
        'ml': 'Manage Account',
        'id': 'Kelola Akun',
    },
    'DM.logOut': {
        'en': 'Log Out',
        'es': 'Cerrar Sesión',
        'pt': 'Sair',
        'ru': 'Выйти',
        'hi': 'Log Out',
        'ml': 'Log Out',
        'id': 'Keluar',
    },
    'DM.logoutConfirm': {
        'en': 'Are you sure you want to log out?',
        'es': '¿Seguro que quieres cerrar sesión?',
        'pt': 'Tem certeza que deseja sair?',
        'ru': 'Вы уверены, что хотите выйти?',
        'hi': 'क्या आप लॉग आउट करना चाहते हैं?',
        'ml': 'ലോഗ് ഔട്ട് ചെയ്യണോ?',
        'id': 'Yakin ingin keluar?',
    },
    'ManageAccount.title': {
        'en': 'Manage Account',
        'es': 'Administrar Cuenta',
        'pt': 'Gerenciar Conta',
        'ru': 'Управление аккаунтом',
        'hi': 'Manage Account',
        'ml': 'Manage Account',
        'id': 'Kelola Akun',
    },
    'ManageAccount.nickname': {
        'en': 'Nickname',
        'es': 'Apodo',
        'pt': 'Apelido',
        'ru': 'Никнейм',
        'hi': 'Nickname',
        'ml': 'Nickname',
        'id': 'Nama panggilan',
    },
    'ManageAccount.description': {
        'en': 'Description',
        'es': 'Descripción',
        'pt': 'Descrição',
        'ru': 'Описание',
        'hi': 'Description',
        'ml': 'Description',
        'id': 'Deskripsi',
    },
    'ManageAccount.changePassword': {
        'en': 'Change Password',
        'es': 'Cambiar Contraseña',
        'pt': 'Alterar Senha',
        'ru': 'Изменить пароль',
        'hi': 'Change Password',
        'ml': 'Change Password',
        'id': 'Ubah Kata Sandi',
    },
    'ManageAccount.currentPassword': {
        'en': 'Current Password',
        'es': 'Contraseña Actual',
        'pt': 'Senha Atual',
        'ru': 'Текущий пароль',
        'hi': 'Current Password',
        'ml': 'Current Password',
        'id': 'Kata Sandi Saat Ini',
    },
    'ManageAccount.newPassword': {
        'en': 'New Password',
        'es': 'Nueva Contraseña',
        'pt': 'Nova Senha',
        'ru': 'Новый пароль',
        'hi': 'New Password',
        'ml': 'New Password',
        'id': 'Kata Sandi Baru',
    },
    'ManageAccount.save': {
        'en': 'Save',
        'es': 'Guardar',
        'pt': 'Salvar',
        'ru': 'Сохранить',
        'hi': 'Save',
        'ml': 'Save',
        'id': 'Simpan',
    },
    'ManageAccount.name': {
        'en': 'Name',
        'es': 'Nombre',
        'pt': 'Nome',
        'ru': 'Имя',
        'hi': 'नाम',
        'ml': 'പേര്',
        'id': 'Nama',
    },
    'ManageAccount.nameTaken': {
        'en': 'Name already taken.',
        'es': 'Ese nombre ya está en uso.',
        'pt': 'Nome já em uso.',
        'ru': 'Имя уже занято.',
        'hi': 'नाम पहले से लिया गया है।',
        'ml': 'പേര് ഇതിനകം ഉപയോഗിക്കുന്നു.',
        'id': 'Nama sudah digunakan.',
    },
    'ManageAccount.accountDeleted': {
        'en': 'Account "{name}" deleted.',
        'es': 'Cuenta "{name}" eliminada.',
        'pt': 'Conta "{name}" excluída.',
        'ru': 'Аккаунт "{name}" удалён.',
        'hi': '"{name}" खाता हटाया गया।',
        'ml': '"{name}" അക്കൗണ്ട് ഇല്ലാതാക്കി.',
        'id': 'Akun "{name}" dihapus.',
    },
    'ManageAccount.deleteAccount': {
        'en': 'Delete Account',
        'es': 'Eliminar cuenta',
        'pt': 'Excluir conta',
        'ru': 'Удалить аккаунт',
        'hi': 'खाता हटाएं',
        'ml': 'അക്കൗണ്ട് ഇല്ലാതാക്കുക',
        'id': 'Hapus Akun',
    },
    'ManageAccount.deleteConfirm': {
        'en': 'Are you sure? This cannot be undone.',
        'es': '¿Estás seguro? Esto no se puede deshacer.',
        'pt': 'Tem certeza? Isso não pode ser desfeito.',
        'ru': 'Вы уверены? Это нельзя отменить.',
        'hi': 'क्या आप सुनिश्चित हैं? इसे पूर्ववत नहीं किया जा सकता।',
        'ml': 'തീർച്ചയാണോ? ഇത് പഴയപടിയാക്കാൻ കഴിയില്ല.',
        'id': 'Yakin? Ini tidak bisa dibatalkan.',
    },
    'ManageAccount.maxV2': {
        'en': 'Max accounts reached for this game account.',
        'es': 'Se alcanzó el límite de cuentas para esta cuenta del juego.',
        'pt': 'Limite de contas atingido para esta conta do jogo.',
        'ru': 'Достигнут лимит аккаунтов для этой игровой учётной записи.',
        'hi': 'Max accounts reached for this game account.',
        'ml': 'Max accounts reached for this game account.',
        'id': 'Batas akun tercapai untuk akun game ini.',
    },
    'Settings.globalGather': {
        'en': 'Use Enhanced Gather by default',
        'es': 'Usar Gather mejorado por defecto',
        'pt': 'Usar Gather aprimorado por padrão',
        'ru': 'Использовать улучшенный Gather по умолчанию',
        'hi': 'Default mein Enhanced Gather use karein',
        'ml': 'Default Enhanced Gather upayogikku',
        'id': 'Gunakan Gather yang ditingkatkan secara default',
    },
    'gatherFilterBtn': {
        'en': 'Filters',
        'es': 'Filtros',
        'pt': 'Filtros',
        'ru': 'Фильтры',
        'hi': 'Filters',
        'ml': 'Filters',
        'id': 'Filter',
    },
    'gatherFilterTitle': {
        'en': 'Server Filters',
        'es': 'Filtros de Servidores',
        'pt': 'Filtros de Servidores',
        'ru': 'Фильтры серверов',
        'hi': 'Server Filters',
        'ml': 'Server Filters',
        'id': 'Filter Server',
    },
    'gatherFilterFreeze': {
        'en': 'Freeze List',
        'es': 'Congelar Lista',
        'pt': 'Congelar Lista',
        'ru': 'Заморозить список',
        'hi': 'List Freeze karein',
        'ml': 'List Freeze cheyyuka',
        'id': 'Bekukan Daftar',
    },
    'gatherFilterHideFull': {
        'en': 'Hide Full Servers',
        'es': 'Ocultar Servidores Llenos',
        'pt': 'Ocultar Servidores Cheios',
        'ru': 'Скрыть заполненные серверы',
        'hi': 'Full Servers chupaayein',
        'ml': 'Full Servers marakku',
        'id': 'Sembunyikan Server Penuh',
    },
    'gatherFilterHideEmpty': {
        'en': 'Hide Empty Servers',
        'es': 'Ocultar Servidores Vacíos',
        'pt': 'Ocultar Servidores Vazios',
        'ru': 'Скрыть пустые серверы',
        'hi': 'Khaali Servers chupaayein',
        'ml': 'Kaali Servers marakku',
        'id': 'Sembunyikan Server Kosong',
    },
    'gatherFilterOnlyEmpty': {
        'en': 'Only Empty Servers',
        'es': 'Solo Servidores Vacíos',
        'pt': 'Apenas Servidores Vazios',
        'ru': 'Только пустые серверы',
        'hi': 'Sirf Khaali Servers',
        'ml': 'Kaali Servers maathram',
        'id': 'Hanya Server Kosong',
    },
    'Button.chats': {
        'en': 'Chats',
        'es': 'Chats',
        'pt': 'Chats',
        'ru': 'Чаты',
        'hi': 'Chats',
        'ml': 'Chats',
        'id': 'Obrolan',
    },
    'Button.friends': {
        'en': 'Friends',
        'es': 'Amigos',
        'pt': 'Amigos',
        'ru': 'Друзья',
        'hi': 'Friends',
        'ml': 'Friends',
        'id': 'Teman',
    },
    'Button.trans': {
        'en': 'Trans',
        'es': 'Trad.',
        'pt': 'Trad.',
        'ru': 'Пер.',
        'hi': 'Trans',
        'ml': 'Trans',
        'id': 'Terj.',
    },
    'Camera.button': {
        'en': 'Camera',
        'es': 'Cámara',
        'pt': 'Câmera',
        'ru': 'Камера',
        'hi': 'कैमरा',
        'ml': 'ക്യാമറ',
        'id': 'Kamera',
    },
    'Camera.setCamera': {
        'en': 'Set Camera',
        'es': 'Controlar Cámara',
        'pt': 'Controlar Câmera',
        'ru': 'Управление камерой',
        'hi': 'Camera Set Karein',
        'ml': 'Camera Set Cheyyuka',
        'id': 'Atur Kamera',
    },
    'Camera.getCamera': {
        'en': 'Get Camera',
        'es': 'Ver Posiciones',
        'pt': 'Ver Posições',
        'ru': 'Позиции камеры',
        'hi': 'Camera Positions',
        'ml': 'Camera Positions',
        'id': 'Posisi Kamera',
    },
    'Camera.positions.title': {
        'en': 'Camera Positions',
        'es': 'Posiciones de Cámara',
        'pt': 'Posições da Câmera',
        'ru': 'Позиции камеры',
        'hi': 'Camera Positions',
        'ml': 'Camera Positions',
        'id': 'Posisi Kamera',
    },
    'Camera.positions.noPositions': {
        'en': 'No saved positions',
        'es': 'Sin posiciones guardadas',
        'pt': 'Sem posições salvas',
        'ru': 'Нет сохранённых позиций',
        'hi': 'Koi position save nahi',
        'ml': 'Saved positions onnumilla',
        'id': 'Tidak ada posisi tersimpan',
    },
    'Camera.positions.saveCurrent': {
        'en': 'Save Current',
        'es': 'Guardar Actual',
        'pt': 'Salvar Atual',
        'ru': 'Сохранить текущую',
        'hi': 'Current Save Karein',
        'ml': 'Current Save Cheyyuka',
        'id': 'Simpan Saat Ini',
    },
    'Camera.positions.saved': {
        'en': 'Position saved',
        'es': 'Posición guardada',
        'pt': 'Posição salva',
        'ru': 'Позиция сохранена',
        'hi': 'Position save ho gaya',
        'ml': 'Position save aayi',
        'id': 'Posisi tersimpan',
    },
    'Camera.positions.applied': {
        'en': 'Camera position applied',
        'es': 'Posición de cámara aplicada',
        'pt': 'Posição da câmera aplicada',
        'ru': 'Позиция камеры применена',
        'hi': 'Camera position apply ho gaya',
        'ml': 'Camera position apply aayi',
        'id': 'Posisi kamera diterapkan',
    },
    'Camera.positions.enterName': {
        'en': 'Enter name...',
        'es': 'Escribe un nombre...',
        'pt': 'Digite um nome...',
        'ru': 'Введите название...',
        'hi': 'Naam likho...',
        'ml': 'Peru ezhuthuka...',
        'id': 'Masukkan nama...',
    },
    'Camera.positions.apply': {
        'en': 'Apply',
        'es': 'Aplicar',
        'pt': 'Aplicar',
        'ru': 'Применить',
        'hi': 'Apply Karein',
        'ml': 'Apply Cheyyuka',
        'id': 'Terapkan',
    },
    'Camera.positions.delete': {
        'en': 'Del',
        'es': 'Borrar',
        'pt': 'Excluir',
        'ru': 'Удалить',
        'hi': 'Delete',
        'ml': 'Delete',
        'id': 'Hapus',
    },
    'Camera.positions.deleteConfirm': {
        'en': "Delete position '{name}'?",
        'es': "¿Borrar la posición '{name}'?",
        'pt': "Excluir posição '{name}'?",
        'ru': "Удалить позицию '{name}'?",
        'hi': "Delete position '{name}'?",
        'ml': "Delete position '{name}'?",
        'id': "Hapus posisi '{name}'?",
    },
    'Camera.overlay.position': {
        'en': 'Cam Position',
        'es': 'Posición Cámara',
        'pt': 'Posição Câmera',
        'ru': 'Позиция камеры',
        'hi': 'Cam Position',
        'ml': 'Cam Position',
        'id': 'Posisi Kamera',
    },
    'Camera.overlay.angle': {
        'en': 'Cam Angle',
        'es': 'Ángulo Cámara',
        'pt': 'Ângulo Câmera',
        'ru': 'Угол камеры',
        'hi': 'Cam Angle',
        'ml': 'Cam Angle',
        'id': 'Sudut Kamera',
    },
    'Camera.overlay.zoomIn': {
        'en': 'Zoom +',
        'es': 'Zoom +',
        'pt': 'Zoom +',
        'ru': 'Зум +',
        'hi': 'Zoom +',
        'ml': 'Zoom +',
        'id': 'Zoom +',
    },
    'Camera.overlay.zoomOut': {
        'en': 'Zoom -',
        'es': 'Zoom -',
        'pt': 'Zoom -',
        'ru': 'Зум -',
        'hi': 'Zoom -',
        'ml': 'Zoom -',
        'id': 'Zoom -',
    },
    'Camera.overlay.nameCam': {
        'en': 'Name Camera',
        'es': 'Nombre Cámara',
        'pt': 'Nome Câmera',
        'ru': 'Название камеры',
        'hi': 'Camera Name',
        'ml': 'Camera Name',
        'id': 'Nama Kamera',
    },
    'Camera.overlay.save': {
        'en': 'Save',
        'es': 'Guardar',
        'pt': 'Salvar',
        'ru': 'Сохранить',
        'hi': 'Save',
        'ml': 'Save',
        'id': 'Simpan',
    },
    'Camera.overlay.reset': {
        'en': 'Reset',
        'es': 'Resetear',
        'pt': 'Resetar',
        'ru': 'Сбросить',
        'hi': 'Reset',
        'ml': 'Reset',
        'id': 'Reset',
    },
    'Camera.overlay.done': {
        'en': 'Done',
        'es': 'Listo',
        'pt': 'Pronto',
        'ru': 'Готово',
        'hi': 'Done',
        'ml': 'Done',
        'id': 'Selesai',
    },
    'Menu.recentServers': {
        'en': 'Recent servers',
        'es': 'Servidores recientes',
        'pt': 'Servidores recentes',
        'ru': 'Недавние серверы',
        'hi': 'Recent servers',
        'ml': 'Recent servers',
        'id': 'Server terbaru',
    },
    'RecentServers.justNow': {
        'en': 'just now',
        'es': 'ahora mismo',
        'pt': 'agora mesmo',
        'ru': 'только что',
        'hi': 'अभी',
        'ml': 'ഇപ്പോൾ',
        'id': 'baru saja',
    },
    'RecentServers.minutesAgo': {
        'en': '{n} min ago',
        'es': 'hace {n} min',
        'pt': 'há {n} min',
        'ru': '{n} мин назад',
        'hi': '{n} मिनट पहले',
        'ml': '{n} മിനിറ്റ് മുൻപ്',
        'id': '{n} mnt lalu',
    },
    'RecentServers.hoursAgo': {
        'en': '{n} hr ago',
        'es': 'hace {n} h',
        'pt': 'há {n} h',
        'ru': '{n} ч назад',
        'hi': '{n} घंटे पहले',
        'ml': '{n} മണിക്കൂർ മുൻപ്',
        'id': '{n} jam lalu',
    },
    'RecentServers.daysAgo': {
        'en': '{n} days ago',
        'es': 'hace {n} días',
        'pt': 'há {n} dias',
        'ru': '{n} дн назад',
        'hi': '{n} दिन पहले',
        'ml': '{n} ദിവസം മുൻപ്',
        'id': '{n} hari lalu',
    },
    'RecentServers.title': {
        'en': 'Recent servers',
        'es': 'Servidores recientes',
        'pt': 'Servidores recentes',
        'ru': 'Недавние серверы',
        'hi': 'Recent servers',
        'ml': 'Recent servers',
        'id': 'Server terbaru',
    },
    'RecentServers.noServers': {
        'en': 'No recent servers',
        'es': 'Sin servidores recientes',
        'pt': 'Sem servidores recentes',
        'ru': 'Нет недавних серверов',
        'hi': 'No recent servers',
        'ml': 'No recent servers',
        'id': 'Tidak ada server terbaru',
    },
    'RecentServers.peek': {
        'en': 'Players',
        'es': 'Jugadores',
        'pt': 'Jogadores',
        'ru': 'Игроки',
        'hi': 'Players',
        'ml': 'Players',
        'id': 'Pemain',
    },
    'RecentServers.join': {
        'en': 'Join',
        'es': 'Unirse',
        'pt': 'Entrar',
        'ru': 'Войти',
        'hi': 'Join',
        'ml': 'Join',
        'id': 'Bergabung',
    },
    'RecentServers.joinFailed': {
        'en': 'Could not connect to server',
        'es': 'No se pudo conectar al servidor',
        'pt': 'Não foi possível conectar ao servidor',
        'ru': 'Не удалось подключиться к серверу',
        'hi': 'Could not connect to server',
        'ml': 'Could not connect to server',
        'id': 'Tidak dapat terhubung ke server',
    },
    'RecentServers.scanning': {
        'en': 'Scanning...',
        'es': 'Escaneando...',
        'pt': 'Verificando...',
        'ru': 'Сканирование...',
        'hi': 'Scanning...',
        'ml': 'Scanning...',
        'id': 'Memindai...',
    },
    'RecentServers.noResponse': {
        'en': 'No response',
        'es': 'Sin respuesta',
        'pt': 'Sem resposta',
        'ru': 'Нет ответа',
        'hi': 'No response',
        'ml': 'No response',
        'id': 'Tidak ada respons',
    },
    'RecentServers.noPlayers': {
        'en': 'No players found',
        'es': 'Sin jugadores',
        'pt': 'Nenhum jogador encontrado',
        'ru': 'Игроки не найдены',
        'hi': 'No players found',
        'ml': 'No players found',
        'id': 'Tidak ada pemain',
    },
    'Settings.maxRecentServers': {
        'en': 'Max recent servers',
        'es': 'Máx. servidores recientes',
        'pt': 'Máx. servidores recentes',
        'ru': 'Макс. недавних серверов',
        'hi': 'Max recent servers',
        'ml': 'Max recent servers',
        'id': 'Maks. server terbaru',
    },
    'Menu.tint': {
        'en': 'Map Tint',
        'es': 'Tinte de mapa',
        'pt': 'Tinte do mapa',
        'ru': 'Тинт карты',
        'hi': 'Map Tint',
        'ml': 'Map Tint',
        'id': 'Pewarnaan peta',
    },
    'Tint.title': {
        'en': 'Map Tint',
        'es': 'Tinte de mapa',
        'pt': 'Tinte do mapa',
        'ru': 'Тинт карты',
        'hi': 'Map Tint',
        'ml': 'Map Tint',
        'id': 'Pewarnaan peta',
    },
    'Tint.colorLabel': {
        'en': 'Tint color',
        'es': 'Color de tinte',
        'pt': 'Cor do tinte',
        'ru': 'Цвет тинта',
        'hi': 'Tint color',
        'ml': 'Tint color',
        'id': 'Warna tint',
    },
    'Tint.disco': {
        'en': 'Disco mode',
        'es': 'Modo disco',
        'pt': 'Modo disco',
        'ru': 'Режим диско',
        'hi': 'Disco mode',
        'ml': 'Disco mode',
        'id': 'Mode disko',
    },
    'Tint.discoSpeed': {
        'en': 'Speed (seconds)',
        'es': 'Velocidad (segundos)',
        'pt': 'Velocidade (segundos)',
        'ru': 'Скорость (секунды)',
        'hi': 'Speed (seconds)',
        'ml': 'Speed (seconds)',
        'id': 'Kecepatan (detik)',
    },
    'Tint.reset': {
        'en': 'Reset',
        'es': 'Restablecer',
        'pt': 'Redefinir',
        'ru': 'Сброс',
        'hi': 'Reset',
        'ml': 'Reset',
        'id': 'Reset',
    },
    'Tint.apply': {
        'en': 'Apply',
        'es': 'Aplicar',
        'pt': 'Aplicar',
        'ru': 'Применить',
        'hi': 'Apply',
        'ml': 'Apply',
        'id': 'Terapkan',
    },
    'Settings.cameraAutoRestore': {
        'en': 'Auto-restore last camera on game start',
        'es': 'Restaurar última cámara al iniciar partida',
        'pt': 'Restaurar câmera ao iniciar partida',
        'ru': 'Авто-восстановление камеры при старте игры',
        'hi': 'Auto-restore last camera on game start',
        'ml': 'Auto-restore last camera on game start',
        'id': 'Pulihkan kamera terakhir saat mulai permainan',
    },
    'Menu.recentPlayers': {
        'en': 'Recent Players',
        'es': 'Jugadores recientes',
        'pt': 'Jogadores recentes',
        'ru': 'Недавние игроки',
        'hi': 'Recent Players',
        'ml': 'Recent Players',
        'id': 'Pemain terbaru',
    },
    'RecentPlayers.title': {
        'en': 'Recent Players',
        'es': 'Jugadores recientes',
        'pt': 'Jogadores recentes',
        'ru': 'Недавние игроки',
        'hi': 'Recent Players',
        'ml': 'Recent Players',
        'id': 'Pemain terbaru',
    },
    'RecentPlayers.noPlayers': {
        'en': 'No players recorded yet',
        'es': 'Aún no hay jugadores guardados',
        'pt': 'Nenhum jogador registrado ainda',
        'ru': 'Игроки ещё не записаны',
        'hi': 'No players recorded yet',
        'ml': 'No players recorded yet',
        'id': 'Belum ada pemain yang tercatat',
    },
    'RecentPlayers.justNow': {
        'en': 'just now',
        'es': 'ahora mismo',
        'pt': 'agora mesmo',
        'ru': 'только что',
        'hi': 'just now',
        'ml': 'just now',
        'id': 'baru saja',
    },
    'RecentPlayers.minutesAgo': {
        'en': '{n}m ago',
        'es': 'hace {n}m',
        'pt': 'há {n}m',
        'ru': '{n}м назад',
        'hi': '{n}m ago',
        'ml': '{n}m ago',
        'id': '{n}m lalu',
    },
    'RecentPlayers.hoursAgo': {
        'en': '{n}h ago',
        'es': 'hace {n}h',
        'pt': 'há {n}h',
        'ru': '{n}ч назад',
        'hi': '{n}h ago',
        'ml': '{n}h ago',
        'id': '{n}j lalu',
    },
    'RecentPlayers.daysAgo': {
        'en': '{n}d ago',
        'es': 'hace {n}d',
        'pt': 'há {n}d',
        'ru': '{n}д назад',
        'hi': '{n}d ago',
        'ml': '{n}d ago',
        'id': '{n}h lalu',
    },
    'RecentPlayers.infoTitle': {
        'en': 'Player Info',
        'es': 'Info del jugador',
        'pt': 'Info do jogador',
        'ru': 'Инфо игрока',
        'hi': 'Player Info',
        'ml': 'Player Info',
        'id': 'Info pemain',
    },
    'RecentPlayers.messagesSent': {
        'en': 'Messages:',
        'es': 'Mensajes:',
        'pt': 'Mensagens:',
        'ru': 'Сообщений:',
        'hi': 'Messages:',
        'ml': 'Messages:',
        'id': 'Pesan:',
    },
    'RecentPlayers.servers': {
        'en': 'Servers:',
        'es': 'Servidores:',
        'pt': 'Servidores:',
        'ru': 'Серверы:',
        'hi': 'Servers:',
        'ml': 'Servers:',
        'id': 'Server:',
    },
    'RecentPlayers.nicknameSaved': {
        'en': 'Nickname saved',
        'es': 'Apodo guardado',
        'pt': 'Apelido salvo',
        'ru': 'Никнейм сохранён',
        'hi': 'Nickname saved',
        'ml': 'Nickname saved',
        'id': 'Nama panggilan disimpan',
    },
    'RecentPlayers.labelName': {
        'en': 'Name:', 'es': 'Nombre:', 'pt': 'Nome:', 'ru': 'Имя:',
        'hi': 'Name:', 'ml': 'Name:', 'id': 'Nama:',
    },
    'RecentPlayers.labelProfile': {
        'en': 'Profile:', 'es': 'Perfil:', 'pt': 'Perfil:', 'ru': 'Профиль:',
        'hi': 'Profile:', 'ml': 'Profile:', 'id': 'Profil:',
    },
    'RecentPlayers.labelNickname': {
        'en': 'Nickname:', 'es': 'Apodo:', 'pt': 'Apelido:', 'ru': 'Ник:',
        'hi': 'Nickname:', 'ml': 'Nickname:', 'id': 'Nama Panggilan:',
    },
    'RecentPlayers.labelClientId': {
        'en': 'Client ID:', 'es': 'ID Cliente:', 'pt': 'ID Cliente:', 'ru': 'ID Клиента:',
        'hi': 'Client ID:', 'ml': 'Client ID:', 'id': 'ID Klien:',
    },
    'RecentPlayers.labelPbId': {
        'en': 'PB-ID:', 'es': 'PB-ID:', 'pt': 'PB-ID:', 'ru': 'PB-ID:',
        'hi': 'PB-ID:', 'ml': 'PB-ID:', 'id': 'PB-ID:',
    },
    'RecentPlayers.labelLastMet': {
        'en': 'Last Met:', 'es': 'Último Encuentro:', 'pt': 'Último Encontro:', 'ru': 'Последняя встреча:',
        'hi': 'Last Met:', 'ml': 'Last Met:', 'id': 'Terakhir Bertemu:',
    },
    'playerInfo.newPlayer': {
        'en': '[NEW] {name} | Profile: {profile} | CID: {cid}',
        'es': '[NUEVO] {name} | Perfil: {profile} | CID: {cid}',
        'pt': '[NOVO] {name} | Perfil: {profile} | CID: {cid}',
        'ru': '[НОВЫЙ] {name} | Профиль: {profile} | CID: {cid}',
        'hi': '[NEW] {name} | Profile: {profile} | CID: {cid}',
        'ml': '[NEW] {name} | Profile: {profile} | CID: {cid}',
        'id': '[BARU] {name} | Profil: {profile} | CID: {cid}',
    },
    'playerInfo.newPlayerNoProfile': {
        'en': '[NEW] {name} | No Profile | CID: {cid}',
        'es': '[NUEVO] {name} | Sin perfil | CID: {cid}',
        'pt': '[NOVO] {name} | Sem perfil | CID: {cid}',
        'ru': '[НОВЫЙ] {name} | Нет профиля | CID: {cid}',
        'hi': '[NEW] {name} | No Profile | CID: {cid}',
        'ml': '[NEW] {name} | No Profile | CID: {cid}',
        'id': '[BARU] {name} | Tidak ada profil | CID: {cid}',
    },
    'playerInfo.joinBlacklist': {
        'en': '[BLACKLIST] {name}',
        'es': '[BLACKLIST] {name}',
        'pt': '[BLACKLIST] {name}',
        'ru': '[BLACKLIST] {name}',
        'hi': '[BLACKLIST] {name}',
        'ml': '[BLACKLIST] {name}',
        'id': '[BLACKLIST] {name}',
    },
    'playerInfo.joinFriend': {
        'en': '[FRIEND] {name}',
        'es': '[AMIGO] {name}',
        'pt': '[AMIGO] {name}',
        'ru': '[ДРУГ] {name}',
        'hi': '[FRIEND] {name}',
        'ml': '[FRIEND] {name}',
        'id': '[TEMAN] {name}',
    },
    'playerInfo.joinNickname': {
        'en': '[APODO] {name} #{nickname}',
        'es': '[APODO] {name} #{nickname}',
        'pt': '[APELIDO] {name} #{nickname}',
        'ru': '[APODO] {name} #{nickname}',
        'hi': '[APODO] {name} #{nickname}',
        'ml': '[APODO] {name} #{nickname}',
        'id': '[APODO] {name} #{nickname}',
    },
    'playerInfo.updateClientId': {
        'en': '[CID] {name}: {old} -> {new}',
        'es': '[CID] {name}: {old} -> {new}',
        'pt': '[CID] {name}: {old} -> {new}',
        'ru': '[CID] {name}: {old} -> {new}',
        'hi': '[CID] {name}: {old} -> {new}',
        'ml': '[CID] {name}: {old} -> {new}',
        'id': '[CID] {name}: {old} -> {new}',
    },
    'playerInfo.updateProfileName': {
        'en': '[PROFILE UPDATE] {name} -> {profile} | CID: {cid}',
        'es': '[ACTUALIZAR PERFIL] {name} -> {profile} | CID: {cid}',
        'pt': '[ATUALIZAR PERFIL] {name} -> {profile} | CID: {cid}',
        'ru': '[ОБНОВЛЕНИЕ ПРОФИЛЯ] {name} -> {profile} | CID: {cid}',
        'hi': '[PROFILE UPDATE] {name} -> {profile} | CID: {cid}',
        'ml': '[PROFILE UPDATE] {name} -> {profile} | CID: {cid}',
        'id': '[PERBARUI PROFIL] {name} -> {profile} | CID: {cid}',
    },
    'playerInfo.refreshProfileName': {
        'en': '[REFRESH] {name} kept last profile: {profile} | CID: {cid}',
        'es': '[REFRESH] {name} conserva último perfil: {profile} | CID: {cid}',
        'pt': '[REFRESH] {name} mantém último perfil: {profile} | CID: {cid}',
        'ru': '[ОБНОВЛ.] {name} сохранён последний профиль: {profile} | CID: {cid}',
        'hi': '[REFRESH] {name} kept last profile: {profile} | CID: {cid}',
        'ml': '[REFRESH] {name} kept last profile: {profile} | CID: {cid}',
        'id': '[REFRESH] {name} tetap profil terakhir: {profile} | CID: {cid}',
    },
    'playerInfo.addProfileName': {
        'en': '[JOIN] {name} first profile: {profile} | CID: {cid}',
        'es': '[UNIÓN] {name} primer perfil: {profile} | CID: {cid}',
        'pt': '[ENTRADA] {name} primeiro perfil: {profile} | CID: {cid}',
        'ru': '[ВХОД] {name} первый профиль: {profile} | CID: {cid}',
        'hi': '[JOIN] {name} first profile: {profile} | CID: {cid}',
        'ml': '[JOIN] {name} first profile: {profile} | CID: {cid}',
        'id': '[GABUNG] {name} profil pertama: {profile} | CID: {cid}',
    },
    'playerInfo.mutualServerAdded': {
        'en': '[SERVER] {name} new server: {server}',
        'es': '[SERVIDOR] {name} nuevo servidor: {server}',
        'pt': '[SERVIDOR] {name} novo servidor: {server}',
        'ru': '[СЕРВЕР] {name} новый сервер: {server}',
        'hi': '[SERVER] {name} new server: {server}',
        'ml': '[SERVER] {name} new server: {server}',
        'id': '[SERVER] {name} server baru: {server}',
    },
    'playerInfo.mutualServerFirst': {
        'en': '[SERVER] {name} first server: {server}',
        'es': '[SERVIDOR] {name} primer servidor: {server}',
        'pt': '[SERVIDOR] {name} primeiro servidor: {server}',
        'ru': '[СЕРВЕР] {name} первый сервер: {server}',
        'hi': '[SERVER] {name} first server: {server}',
        'ml': '[SERVER] {name} first server: {server}',
        'id': '[SERVER] {name} server pertama: {server}',
    },
    'chatLog.created': {
        'en': '[Chat Log] Created for: {server}',
        'es': '[Chat Log] Creado para: {server}',
        'pt': '[Chat Log] Criado para: {server}',
        'ru': '[Chat Log] Создан для: {server}',
        'hi': '[Chat Log] Created for: {server}',
        'ml': '[Chat Log] Created for: {server}',
        'id': '[Chat Log] Dibuat untuk: {server}',
    },
    'Settings.pingMsgFormat': {
        'en': 'Ping',
        'es': 'Ping',
        'pt': 'Ping',
        'ru': 'Ping',
        'hi': 'Ping',
        'ml': 'Ping',
        'id': 'Ping',
    },
    'Settings.pingMsgFormatDefault': {
        'en': 'My Ping {}ms',
        'es': 'Mi Ping {}ms',
        'pt': 'Meu Ping {}ms',
        'ru': 'Мой Пинг {}ms',
        'hi': 'My Ping {}ms',
        'ml': 'My Ping {}ms',
        'id': 'Ping Saya {}ms',
    },
    'Settings.pingMsgFormatHint': {
        'en': 'Use {} where the ping value goes',
        'es': 'Usa {} donde va el valor del ping',
        'pt': 'Use {} onde o valor do ping aparece',
        'ru': 'Используй {} там, где должно быть значение пинга',
        'hi': 'Use {} where the ping value goes',
        'ml': 'Use {} where the ping value goes',
        'id': 'Gunakan {} untuk nilai ping',
    },
    'Settings.pingMsgFormatError': {
        'en': 'Message must contain {}',
        'es': 'El mensaje debe contener {}',
        'pt': 'A mensagem deve conter {}',
        'ru': 'Сообщение должно содержать {}',
        'hi': 'Message must contain {}',
        'ml': 'Message must contain {}',
        'id': 'Pesan harus mengandung {}',
    },
    'Settings.pingMsgFormatErrorMultiple': {
        'en': 'Only one {} is allowed',
        'es': 'Solo se permite un {} en el mensaje',
        'pt': 'Apenas um {} é permitido',
        'ru': 'Допускается только один {}',
        'hi': 'Only one {} is allowed',
        'ml': 'Only one {} is allowed',
        'id': 'Hanya satu {} yang diizinkan',
    },
    'Settings.pingMsgFormatErrorLength': {
        'en': 'Message is too long (max 20 characters)',
        'es': 'El mensaje es demasiado largo (máx. 20 caracteres)',
        'pt': 'A mensagem é muito longa (máx. 20 caracteres)',
        'ru': 'Сообщение слишком длинное (макс. 20 символов)',
        'hi': 'Message is too long (max 20 characters)',
        'ml': 'Message is too long (max 20 characters)',
        'id': 'Pesan terlalu panjang (maks. 20 karakter)',
    },
    'Settings.sectionStorage': {
        'en': 'Storage',
        'es': 'Almacenamiento',
        'pt': 'Armazenamento',
        'ru': 'Хранилище',
        'hi': 'Storage',
        'ml': 'Storage',
        'id': 'Penyimpanan',
    },
    'Settings.maxChatLogs': {
        'en': 'Max server chat logs',
        'es': 'Máx. chat logs por servidor',
        'pt': 'Máx. logs de chat por servidor',
        'ru': 'Макс. логов чата серверов',
        'hi': 'Max server chat logs',
        'ml': 'Max server chat logs',
        'id': 'Maks log chat server',
    },
    'Settings.storageCounter': {
        'en': 'Used: {used}/{limit}',
        'es': 'Usado: {used}/{limit}',
        'pt': 'Usado: {used}/{limit}',
        'ru': 'Занято: {used}/{limit}',
        'hi': 'Used: {used}/{limit}',
        'ml': 'Used: {used}/{limit}',
        'id': 'Digunakan: {used}/{limit}',
    },
    'Settings.storagePathMsg': {
        'en': 'Location: {path}',
        'es': 'Ubicación: {path}',
        'pt': 'Localização: {path}',
        'ru': 'Расположение: {path}',
        'hi': 'Location: {path}',
        'ml': 'Location: {path}',
        'id': 'Lokasi: {path}',
    },
    'Settings.chatColorIntensity': {
        'en': 'Chat color per player',
        'es': 'Color de chat por jugador',
        'pt': 'Cor de chat por jogador',
        'ru': 'Цвет чата по игроку',
        'hi': 'Chat color per player',
        'ml': 'Chat color per player',
        'id': 'Warna chat per pemain',
    },
    'Settings.chatColorOff': {
        'en': 'Off',
        'es': 'Desactivado',
        'pt': 'Desativado',
        'ru': 'Выкл',
        'hi': 'बंद',
        'ml': 'ഓഫ്',
        'id': 'Nonaktif',
    },
    'Settings.chatColorSoft': {
        'en': 'Soft',
        'es': 'Suave',
        'pt': 'Suave',
        'ru': 'Мягкий',
        'hi': 'हल्का',
        'ml': 'മൃദു',
        'id': 'Lembut',
    },
    'Settings.chatColorStrong': {
        'en': 'Strong',
        'es': 'Fuerte',
        'pt': 'Forte',
        'ru': 'Яркий',
        'hi': 'तेज़',
        'ml': 'ശക്തമായ',
        'id': 'Kuat',
    },
    'Settings.maxPlayerInfo': {
        'en': 'Max stored players (player info)',
        'es': 'Máx. jugadores guardados (player info)',
        'pt': 'Máx. jogadores salvos (player info)',
        'ru': 'Макс. сохранённых игроков (player info)',
        'hi': 'Max stored players (player info)',
        'ml': 'Max stored players (player info)',
        'id': 'Maks pemain tersimpan (player info)',
    },
    'AccountsPopup.title': {
        'en': 'Accounts',
        'es': 'Cuentas',
        'pt': 'Contas',
        'ru': 'Аккаунты',
        'hi': 'खाते',
        'ml': 'അക്കൗണ്ടുകൾ',
        'id': 'Akun',
    },
    'AccountsPopup.signIn': {
        'en': 'Sign In',
        'es': 'Iniciar sesión',
        'pt': 'Entrar',
        'ru': 'Войти',
        'hi': 'साइन इन करें',
        'ml': 'സൈൻ ഇൻ',
        'id': 'Masuk',
    },
    'AccountsPopup.addAccount': {
        'en': '+ Add Account',
        'es': '+ Agregar cuenta',
        'pt': '+ Adicionar conta',
        'ru': '+ Добавить аккаунт',
        'hi': '+ खाता जोड़ें',
        'ml': '+ അക്കൗണ്ട് ചേർക്കുക',
        'id': '+ Tambah Akun',
    },
    'AccountsPopup.logout': {
        'en': 'Logout',
        'es': 'Cerrar sesión',
        'pt': 'Sair',
        'ru': 'Выйти',
        'hi': 'लॉग आउट',
        'ml': 'ലോഗ് ഔട്ട്',
        'id': 'Keluar',
    },
    'LoginWindow.title': {
        'en': 'Login',
        'es': 'Iniciar sesión',
        'pt': 'Entrar',
        'ru': 'Войти',
        'hi': 'लॉगिन',
        'ml': 'ലോഗിൻ',
        'id': 'Masuk',
    },
    'LoginWindow.name': {
        'en': 'Name',
        'es': 'Nombre',
        'pt': 'Nome',
        'ru': 'Имя',
        'hi': 'नाम',
        'ml': 'പേര്',
        'id': 'Nama',
    },
    'LoginWindow.password': {
        'en': 'Password',
        'es': 'Contraseña',
        'pt': 'Senha',
        'ru': 'Пароль',
        'hi': 'पासवर्ड',
        'ml': 'പാസ്‌വേഡ്',
        'id': 'Kata sandi',
    },
    'LoginWindow.login': {
        'en': 'Login',
        'es': 'Iniciar sesión',
        'pt': 'Entrar',
        'ru': 'Войти',
        'hi': 'लॉगिन करें',
        'ml': 'ലോഗിൻ ചെയ്യുക',
        'id': 'Masuk',
    },
    'LoginWindow.loggingIn': {
        'en': 'Logging in...',
        'es': 'Iniciando sesión...',
        'pt': 'Entrando...',
        'ru': 'Вход...',
        'hi': 'लॉगिन हो रहा है...',
        'ml': 'ലോഗിൻ ചെയ്യുന്നു...',
        'id': 'Masuk...',
    },
    'LoginWindow.createAccount': {
        'en': 'Create Account',
        'es': 'Crear cuenta',
        'pt': 'Criar conta',
        'ru': 'Создать аккаунт',
        'hi': 'खाता बनाएं',
        'ml': 'അക്കൗണ്ട് ഉണ്ടാക്കുക',
        'id': 'Buat Akun',
    },
    'CreateAccountWindow.title': {
        'en': 'Create Account',
        'es': 'Crear cuenta',
        'pt': 'Criar conta',
        'ru': 'Создать аккаунт',
        'hi': 'खाता बनाएं',
        'ml': 'അക്കൗണ്ട് ഉണ്ടാക്കുക',
        'id': 'Buat Akun',
    },
    'CreateAccountWindow.name': {
        'en': 'Name',
        'es': 'Nombre',
        'pt': 'Nome',
        'ru': 'Имя',
        'hi': 'नाम',
        'ml': 'പേര്',
        'id': 'Nama',
    },
    'CreateAccountWindow.nickname': {
        'en': 'Nickname',
        'es': 'Apodo',
        'pt': 'Apelido',
        'ru': 'Псевдоним',
        'hi': 'उपनाम',
        'ml': 'വിളിപ്പേര്',
        'id': 'Nama panggilan',
    },
    'CreateAccountWindow.password': {
        'en': 'Password',
        'es': 'Contraseña',
        'pt': 'Senha',
        'ru': 'Пароль',
        'hi': 'पासवर्ड',
        'ml': 'പാസ്‌വേഡ്',
        'id': 'Kata sandi',
    },
    'CreateAccountWindow.create': {
        'en': 'Create',
        'es': 'Crear',
        'pt': 'Criar',
        'ru': 'Создать',
        'hi': 'बनाएं',
        'ml': 'ഉണ്ടാക്കുക',
        'id': 'Buat',
    },
    'AddFriend.title': {
        'en': 'Add Friend',
        'es': 'Agregar amigo',
        'pt': 'Adicionar amigo',
        'ru': 'Добавить друга',
        'hi': 'मित्र जोड़ें',
        'ml': 'സുഹൃത്തിനെ ചേർക്കുക',
        'id': 'Tambah Teman',
    },
    'AddFriend.fieldLabel': {
        'en': 'Name or UID',
        'es': 'Nombre o UID',
        'pt': 'Nome ou UID',
        'ru': 'Имя или UID',
        'hi': 'नाम या UID',
        'ml': 'പേര് അല്ലെങ്കിൽ UID',
        'id': 'Nama atau UID',
    },
    'AddFriend.sendRequest': {
        'en': 'Send Request',
        'es': 'Enviar solicitud',
        'pt': 'Enviar pedido',
        'ru': 'Отправить заявку',
        'hi': 'अनुरोध भेजें',
        'ml': 'അഭ്യർത്ഥന അയയ്ക്കുക',
        'id': 'Kirim Permintaan',
    },
    'AddFriend.sending': {
        'en': 'Sending...',
        'es': 'Enviando...',
        'pt': 'Enviando...',
        'ru': 'Отправка...',
        'hi': 'भेज रहा है...',
        'ml': 'അയയ്ക്കുന്നു...',
        'id': 'Mengirim...',
    },
    'AddFriend.enterField': {
        'en': 'Enter a nickname or UID.',
        'es': 'Ingresa un apodo o UID.',
        'pt': 'Digite um apelido ou UID.',
        'ru': 'Введите псевдоним или UID.',
        'hi': 'उपनाम या UID दर्ज करें।',
        'ml': 'ഒരു വിളിപ്പേര് അല്ലെങ്കിൽ UID നൽകുക.',
        'id': 'Masukkan nama panggilan atau UID.',
    },
    'FriendRequest.accept': {
        'en': 'Accept',
        'es': 'Aceptar',
        'pt': 'Aceitar',
        'ru': 'Принять',
        'hi': 'स्वीकार करें',
        'ml': 'സ്വീകരിക്കുക',
        'id': 'Terima',
    },
    'FriendRequest.reject': {
        'en': 'Reject',
        'es': 'Rechazar',
        'pt': 'Rejeitar',
        'ru': 'Отклонить',
        'hi': 'अस्वीकार करें',
        'ml': 'നിരസിക്കുക',
        'id': 'Tolak',
    },
    'FriendRequest.cancel': {
        'en': 'Cancel',
        'es': 'Cancelar',
        'pt': 'Cancelar',
        'ru': 'Отменить',
        'hi': 'रद्द करें',
        'ml': 'റദ്ദാക്കുക',
        'id': 'Batalkan',
    },
    'FriendRequest.accepted': {
        'en': 'Now friends with {nick}!',
        'es': '¡Ahora son amigos con {nick}!',
        'pt': 'Agora são amigos com {nick}!',
        'ru': 'Теперь вы друзья с {nick}!',
        'hi': 'अब {nick} के साथ मित्र हैं!',
        'ml': 'ഇപ്പോൾ {nick}-ന്റെ സുഹൃത്താണ്!',
        'id': 'Sekarang berteman dengan {nick}!',
    },
    'FriendRequest.rejected': {
        'en': 'Request from {nick} rejected.',
        'es': 'Solicitud de {nick} rechazada.',
        'pt': 'Pedido de {nick} rejeitado.',
        'ru': 'Заявка от {nick} отклонена.',
        'hi': '{nick} का अनुरोध अस्वीकार किया।',
        'ml': '{nick}-ന്റെ അഭ്യർത്ഥന നിരസിച്ചു.',
        'id': 'Permintaan dari {nick} ditolak.',
    },
    'FriendRequest.cancelled': {
        'en': 'Request to {nick} cancelled.',
        'es': 'Solicitud a {nick} cancelada.',
        'pt': 'Pedido para {nick} cancelado.',
        'ru': 'Заявка {nick} отменена.',
        'hi': '{nick} को अनुरोध रद्द किया।',
        'ml': '{nick}-ന് അഭ്യർത്ഥന റദ്ദാക്കി.',
        'id': 'Permintaan ke {nick} dibatalkan.',
    },
    'DM.noFriendsYet': {
        'en': 'No friends yet',
        'es': 'Sin amigos aún',
        'pt': 'Sem amigos ainda',
        'ru': 'Пока нет друзей',
        'hi': 'अभी कोई मित्र नहीं',
        'ml': 'ഇതുവരെ സുഹൃത്തുക്കൾ ഇല്ല',
        'id': 'Belum ada teman',
    },
    'FriendMenu.inviteToGame': {
        'en': 'Invite to Game',
        'es': 'Invitar al juego',
        'pt': 'Convidar para o jogo',
        'ru': 'Пригласить в игру',
        'hi': 'खेल में आमंत्रित करें',
        'ml': 'ഗെയിമിലേക്ക് ക്ഷണിക്കുക',
        'id': 'Undang ke Game',
    },
    'FriendMenu.viewAccount': {
        'en': 'View Account',
        'es': 'Ver cuenta',
        'pt': 'Ver conta',
        'ru': 'Просмотр аккаунта',
        'hi': 'खाता देखें',
        'ml': 'അക്കൗണ്ട് കാണുക',
        'id': 'Lihat Akun',
    },
    'FriendMenu.removeFriend': {
        'en': 'Remove Friend',
        'es': 'Eliminar amigo',
        'pt': 'Remover amigo',
        'ru': 'Удалить из друзей',
        'hi': 'मित्र हटाएं',
        'ml': 'സുഹൃത്തിനെ നീക്കുക',
        'id': 'Hapus Teman',
    },
    'FriendMenu.removeConfirm': {
        'en': 'Remove {nick} from friends?',
        'es': '¿Eliminar a {nick} de tus amigos?',
        'pt': 'Remover {nick} dos amigos?',
        'ru': 'Удалить {nick} из друзей?',
        'hi': '{nick} को मित्रों से हटाएं?',
        'ml': '{nick} നെ സുഹൃത്തുക്കളിൽ നിന്ന് നീക്കണോ?',
        'id': 'Hapus {nick} dari teman?',
    },
    'FriendMenu.removed': {
        'en': '{nick} removed from friends.',
        'es': '{nick} eliminado de amigos.',
        'pt': '{nick} removido dos amigos.',
        'ru': '{nick} удалён из друзей.',
        'hi': '{nick} को मित्रों से हटाया गया।',
        'ml': '{nick} സുഹൃത്തുക്കളിൽ നിന്ന് നീക്കി.',
        'id': '{nick} dihapus dari teman.',
    },
    'GlobalChat.copy': {
        'en': 'Copy',
        'es': 'Copiar',
        'pt': 'Copiar',
        'ru': 'Копировать',
        'hi': 'कॉपी',
        'ml': 'കോപ്പി',
        'id': 'Salin',
    },
    'GlobalChat.translate': {
        'en': 'Translate',
        'es': 'Traducir',
        'pt': 'Traduzir',
        'ru': 'Перевести',
        'hi': 'अनुवाद',
        'ml': 'വിവർത്തനം',
        'id': 'Terjemahkan',
    },
    'GlobalChat.viewAccount': {
        'en': 'View Account',
        'es': 'Ver cuenta',
        'pt': 'Ver conta',
        'ru': 'Просмотр аккаунта',
        'hi': 'खाता देखें',
        'ml': 'അക്കൗണ്ട് കാണുക',
        'id': 'Lihat Akun',
    },
    'GlobalChat.loading': {
        'en': 'Loading...',
        'es': 'Cargando...',
        'pt': 'Carregando...',
        'ru': 'Загрузка...',
        'hi': 'लोड हो रहा है...',
        'ml': 'ലോഡ് ചെയ്യുന്നു...',
        'id': 'Memuat...',
    },
    'GlobalChat.loadError': {
        'en': 'Could not load profile.',
        'es': 'No se pudo cargar el perfil.',
        'pt': 'Não foi possível carregar o perfil.',
        'ru': 'Не удалось загрузить профиль.',
        'hi': 'प्रोफ़ाइल लोड नहीं हो सकी।',
        'ml': 'പ്രൊഫൈൽ ലോഡ് ചെയ്യാനായില്ല.',
        'id': 'Gagal memuat profil.',
    },
    'GlobalChat.sendFriendRequest': {
        'en': 'Send Friend Request',
        'es': 'Enviar solicitud de amistad',
        'pt': 'Enviar pedido de amizade',
        'ru': 'Отправить заявку в друзья',
        'hi': 'मित्र अनुरोध भेजें',
        'ml': 'സൗഹൃദ അഭ്യർത്ഥന അയയ്ക്കുക',
        'id': 'Kirim Permintaan Pertemanan',
    },
    'GlobalChat.requestPending': {
        'en': 'Request Pending...',
        'es': 'Solicitud pendiente...',
        'pt': 'Pedido pendente...',
        'ru': 'Заявка ожидает...',
        'hi': 'अनुरोध प्रतीक्षित...',
        'ml': 'അഭ്യർത്ഥന കാത്തിരിക്കുന്നു...',
        'id': 'Permintaan tertunda...',
    },
    'GlobalChat.sending': {
        'en': 'Sending...',
        'es': 'Enviando...',
        'pt': 'Enviando...',
        'ru': 'Отправка...',
        'hi': 'भेज रहा है...',
        'ml': 'അയയ്ക്കുന്നു...',
        'id': 'Mengirim...',
    },
    'GlobalChat.requestSent': {
        'en': 'Request sent to {nick}!',
        'es': '¡Solicitud enviada a {nick}!',
        'pt': 'Pedido enviado para {nick}!',
        'ru': 'Заявка отправлена {nick}!',
        'hi': '{nick} को अनुरोध भेजा!',
        'ml': '{nick}-ന് അഭ്യർത്ഥന അയച്ചു!',
        'id': 'Permintaan dikirim ke {nick}!',
    },
    'GlobalChat.alreadyFriends': {
        'en': 'Already friends or pending.',
        'es': 'Ya son amigos o está pendiente.',
        'pt': 'Já são amigos ou pendente.',
        'ru': 'Уже друзья или заявка ожидает.',
        'hi': 'पहले से मित्र हैं या अनुरोध लंबित है।',
        'ml': 'ഇതിനകം സുഹൃത്തുക്കൾ അല്ലെങ്കിൽ കാത്തിരിക്കുന്നു.',
        'id': 'Sudah berteman atau tertunda.',
    },
    'GlobalChat.userNotFound': {
        'en': 'User not found.',
        'es': 'Usuario no encontrado.',
        'pt': 'Usuário não encontrado.',
        'ru': 'Пользователь не найден.',
        'hi': 'उपयोगकर्ता नहीं मिला।',
        'ml': 'ഉപയോക്താവ് കണ്ടെത്തിയില്ല.',
        'id': 'Pengguna tidak ditemukan.',
    },
    'CreateAccountWindow.creating': {
        'en': 'Creating...',
        'es': 'Creando...',
        'pt': 'Criando...',
        'ru': 'Создание...',
        'hi': 'बना रहा है...',
        'ml': 'ഉണ്ടാക്കുന്നു...',
        'id': 'Membuat...',
    },
    'InviteBlock.statusMins': {
        'en': 'Invites blocked: {mins}m {secs}s left',
        'es': 'Invitaciones bloqueadas: {mins}m {secs}s restantes',
        'pt': 'Convites bloqueados: {mins}m {secs}s restantes',
        'ru': 'Приглашения заблокированы: {mins}м {secs}с осталось',
        'hi': 'आमंत्रण ब्लॉक: {mins}मि {secs}से शेष',
        'ml': 'ക്ഷണങ്ങൾ തടഞ്ഞു: {mins}മി {secs}സെ ശേഷിക്കുന്നു',
        'id': 'Undangan diblokir: sisa {mins}m {secs}d',
    },
    'InviteBlock.statusSecs': {
        'en': 'Invites blocked: {secs}s left',
        'es': 'Invitaciones bloqueadas: {secs}s restantes',
        'pt': 'Convites bloqueados: {secs}s restantes',
        'ru': 'Приглашения заблокированы: {secs}с осталось',
        'hi': 'आमंत्रण ब्लॉक: {secs}से शेष',
        'ml': 'ക്ഷണങ്ങൾ തടഞ്ഞു: {secs}സെ ശേഷിക്കുന്നു',
        'id': 'Undangan diblokir: sisa {secs}d',
    },
    'InviteBlock.removeBlock': {
        'en': 'Remove block',
        'es': 'Quitar bloqueo',
        'pt': 'Remover bloqueio',
        'ru': 'Снять блокировку',
        'hi': 'ब्लॉक हटाएं',
        'ml': 'ബ്ലോക്ക് നീക്കുക',
        'id': 'Hapus blokir',
    },
    'InviteBlock.blockedFor': {
        'en': 'Blocked for {min} min.',
        'es': 'Bloqueado por {min} min.',
        'pt': 'Bloqueado por {min} min.',
        'ru': 'Заблокировано на {min} мин.',
        'hi': '{min} मिनट के लिए ब्लॉक किया।',
        'ml': '{min} മി. ബ്ലോക്ക് ചെയ്തു.',
        'id': 'Diblokir selama {min} mnt.',
    },
    'InviteBlock.blockRemoved': {
        'en': 'Block removed.',
        'es': 'Bloqueo eliminado.',
        'pt': 'Bloqueio removido.',
        'ru': 'Блокировка снята.',
        'hi': 'ब्लॉक हटाया गया।',
        'ml': 'ബ്ലോക്ക് നീക്കി.',
        'id': 'Blokir dihapus.',
    },
    'InviteBlock.confirmRemove': {
        'en': 'Remove block on invites from {nick}?',
        'es': '¿Quitar bloqueo de invitaciones de {nick}?',
        'pt': 'Remover bloqueio de convites de {nick}?',
        'ru': 'Снять блокировку приглашений от {nick}?',
        'hi': '{nick} के निमंत्रण का ब्लॉक हटाएं?',
        'ml': '{nick}-ൽ നിന്ന് ക്ഷണ ബ്ലോക്ക് നീക്കണോ?',
        'id': 'Hapus blokir undangan dari {nick}?',
    },
    'InviteBlock.blockBtn': {
        'en': 'Block',
        'es': 'Bloquear',
        'pt': 'Bloquear',
        'ru': 'Блокировать',
        'hi': 'ब्लॉक',
        'ml': 'ബ്ലോക്ക്',
        'id': 'Blokir',
    },
    'InviteBlock.confirmBlock': {
        'en': 'Block game invites from {nick} for {min} min?',
        'es': '¿Bloquear invitaciones de {nick} por {min} min?',
        'pt': 'Bloquear convites de {nick} por {min} min?',
        'ru': 'Блокировать приглашения от {nick} на {min} мин?',
        'hi': '{nick} से {min} मिनट के लिए निमंत्रण ब्लॉक करें?',
        'ml': '{nick}-ൽ നിന്ന് {min} മിനിറ്റ് ക്ഷണം ബ്ലോക്ക് ചെയ്യണോ?',
        'id': 'Blokir undangan dari {nick} selama {min} menit?',
    },
    'InviteWindow.invitedBy': {
        'en': 'Invited by {sender}',
        'es': 'Invitado por {sender}',
        'pt': 'Convidado por {sender}',
        'ru': 'Приглашён от {sender}',
        'hi': '{sender} द्वारा आमंत्रित',
        'ml': '{sender} ക്ഷണിച്ചു',
        'id': 'Diundang oleh {sender}',
    },
    'InviteWindow.dontShow': {
        'en': 'Don\'t show from {sender} ({min} min)',
        'es': 'No mostrar de {sender} ({min} min)',
        'pt': 'Não mostrar de {sender} ({min} min)',
        'ru': 'Не показывать от {sender} ({min} мин)',
        'hi': '{sender} से न दिखाएं ({min} मिनट)',
        'ml': '{sender}-ൽ നിന്ന് കാണിക്കരുത് ({min} മി)',
        'id': 'Jangan tampilkan dari {sender} ({min} mnt)',
    },
    'QuickRespond.editOrder': {
        'en': 'Edit Order',
        'es': 'Editar orden',
        'pt': 'Editar ordem',
        'ru': 'Редактировать порядок',
        'hi': 'क्रम संपादित करें',
        'ml': 'ക്രമം എഡിറ്റ് ചെയ്യുക',
        'id': 'Edit Urutan',
    },
    'QuickRespond.label': {
        'en': 'Quick Respond',
        'es': 'Respuesta rápida',
        'pt': 'Resposta rápida',
        'ru': 'Быстрый ответ',
        'hi': 'त्वरित जवाब',
        'ml': 'ദ്രുത മറുപടി',
        'id': 'Balas Cepat',
    },
    'Admin.title': {
        'en': 'Users',
        'es': 'Usuarios',
        'pt': 'Usuários',
        'ru': 'Пользователи',
        'hi': 'उपयोगकर्ता',
        'ml': 'ഉപയോക്താക്കൾ',
        'id': 'Pengguna',
    },
    'Admin.banUser': {
        'en': 'Ban User',
        'es': 'Banear usuario',
        'pt': 'Banir usuário',
        'ru': 'Заблокировать',
        'hi': 'बैन करें',
        'ml': 'ബാൻ ചെയ്യുക',
        'id': 'Ban Pengguna',
    },
    'Admin.changeRole': {
        'en': 'Change Role',
        'es': 'Cambiar rol',
        'pt': 'Mudar papel',
        'ru': 'Изменить роль',
        'hi': 'भूमिका बदलें',
        'ml': 'റോൾ മാറ്റുക',
        'id': 'Ubah Peran',
    },
    'Admin.ban': {
        'en': 'Ban',
        'es': 'Banear',
        'pt': 'Banir',
        'ru': 'Бан',
        'hi': 'बैन',
        'ml': 'ബാൻ',
        'id': 'Ban',
    },
    'Admin.reason': {
        'en': 'Reason (optional)',
        'es': 'Razón (opcional)',
        'pt': 'Motivo (opcional)',
        'ru': 'Причина (необяз.)',
        'hi': 'कारण (वैकल्पिक)',
        'ml': 'കാരണം (ഐഛിക)',
        'id': 'Alasan (opsional)',
    },
    'Admin.hours': {
        'en': 'Hours',
        'es': 'Horas',
        'pt': 'Horas',
        'ru': 'Часы',
        'hi': 'घंटे',
        'ml': 'മണിക്കൂർ',
        'id': 'Jam',
    },
    'Admin.days': {
        'en': 'Days',
        'es': 'Días',
        'pt': 'Dias',
        'ru': 'Дни',
        'hi': 'दिन',
        'ml': 'ദിവസം',
        'id': 'Hari',
    },
    'Admin.permanent': {
        'en': 'Permanent',
        'es': 'Permanente',
        'pt': 'Permanente',
        'ru': 'Навсегда',
        'hi': 'स्थायी',
        'ml': 'സ്ഥിരം',
        'id': 'Permanen',
    },
    'Chat.bannedFor': {
        'en': 'Banned | {time}',
        'es': 'Baneado | {time}',
        'pt': 'Banido | {time}',
        'ru': 'Заблокирован | {time}',
        'hi': 'प्रतिबंधित | {time}',
        'ml': 'ബാൻ | {time}',
        'id': 'Dibanned | {time}',
    },
    'Chat.banReason': {
        'en': 'Reason: {reason}',
        'es': 'Motivo: {reason}',
        'pt': 'Motivo: {reason}',
        'ru': 'Причина: {reason}',
        'hi': 'कारण: {reason}',
        'ml': 'കാരണം: {reason}',
        'id': 'Alasan: {reason}',
    },
    'Admin.banned': {
        'en': '{nick} banned',
        'es': '{nick} baneado',
        'pt': '{nick} banido',
        'ru': '{nick} заблокирован',
        'hi': '{nick} बैन हो गया',
        'ml': '{nick} ബാൻ ചെയ്തു',
        'id': '{nick} dibanned',
    },
    'Admin.unbanned': {
        'en': '{nick} unbanned',
        'es': '{nick} desbaneado',
        'pt': '{nick} desbanido',
        'ru': '{nick} разблокирован',
        'hi': '{nick} अनबैन हो गया',
        'ml': '{nick} ബാൻ നീക്കി',
        'id': '{nick} di-unban',
    },
    'Admin.roleChanged': {
        'en': 'Role updated',
        'es': 'Rol actualizado',
        'pt': 'Papel atualizado',
        'ru': 'Роль обновлена',
        'hi': 'भूमिका अपडेट हुई',
        'ml': 'റോൾ അപ്ഡേറ്റ് ചെയ്തു',
        'id': 'Peran diperbarui',
    },
    'Admin.roleAlreadySet': {
        'en': '{nick} already has role {role}.',
        'es': '{nick} ya tiene el rol {role}.',
        'pt': '{nick} já tem o papel {role}.',
        'ru': '{nick} уже имеет роль {role}.',
        'hi': '{nick} के पास पहले से {role} रोल है।',
        'ml': '{nick}-ന് ഇതിനകം {role} റോൾ ഉണ്ട്.',
        'id': '{nick} sudah memiliki peran {role}.',
    },
    'Admin.roleConfirm': {
        'en': 'Change {nick}\'s role to {role}?',
        'es': '¿Cambiar el rol de {nick} a {role}?',
        'pt': 'Mudar o papel de {nick} para {role}?',
        'ru': 'Изменить роль {nick} на {role}?',
        'hi': '{nick} की भूमिका {role} करें?',
        'ml': '{nick}-ന്റെ റോൾ {role} ആക്കണോ?',
        'id': 'Ubah peran {nick} menjadi {role}?',
    },
    'Admin.viewAllUsers': {
        'en': 'Users',
        'es': 'Usuarios',
        'pt': 'Usuários',
        'ru': 'Пользователи',
        'hi': 'उपयोगकर्ता',
        'ml': 'ഉപയോക്താക്കൾ',
        'id': 'Pengguna',
    },
    'Admin.noUsers': {
        'en': 'No users found',
        'es': 'Sin usuarios',
        'pt': 'Nenhum usuário',
        'ru': 'Нет пользователей',
        'hi': 'कोई उपयोगकर्ता नहीं',
        'ml': 'ഉപയോക്താക്കൾ ഇല്ല',
        'id': 'Tidak ada pengguna',
    },
    'Admin.confirmBan': {
        'en': 'Ban {nick}?',
        'es': '¿Banear a {nick}?',
        'pt': 'Banir {nick}?',
        'ru': 'Заблокировать {nick}?',
        'hi': '{nick} को बैन करें?',
        'ml': '{nick}-നെ ബാൻ ചെയ്യണോ?',
        'id': 'Ban {nick}?',
    },
    'Admin.selectBanType': {
        'en': 'Ban type',
        'es': 'Tipo de ban',
        'pt': 'Tipo de ban',
        'ru': 'Тип бана',
        'hi': 'बैन प्रकार',
        'ml': 'ബാൻ തരം',
        'id': 'Tipe ban',
    },
    'Admin.duration': {
        'en': 'Duration',
        'es': 'Duración',
        'pt': 'Duração',
        'ru': 'Длительность',
        'hi': 'अवधि',
        'ml': 'ദൈർഘ്യം',
        'id': 'Durasi',
    },
    'Admin.confirm': {
        'en': 'Confirm',
        'es': 'Confirmar',
        'pt': 'Confirmar',
        'ru': 'Подтвердить',
        'hi': 'पुष्टि करें',
        'ml': 'സ്ഥിരീകരിക്കുക',
        'id': 'Konfirmasi',
    },
    'Admin.editProfile': {
        'en': 'Edit Account',
        'es': 'Editar cuenta',
        'pt': 'Editar conta',
        'ru': 'Редактировать аккаунт',
        'hi': 'खाता संपादित करें',
        'ml': 'അക്കൗണ്ട് എഡിറ്റ് ചെയ്യുക',
        'id': 'Edit Akun',
    },
    'Admin.profileSaved': {
        'en': 'Data changed successfully',
        'es': 'Datos cambiados correctamente',
        'pt': 'Dados alterados com sucesso',
        'ru': 'Данные успешно изменены',
        'hi': 'डेटा सफलतापूर्वक बदला गया',
        'ml': 'ഡാറ്റ വിജയകരമായി മാറ്റി',
        'id': 'Data berhasil diubah',
    },
    'Admin.noChanges': {
        'en': 'No changes.',
        'es': 'Sin cambios.',
        'pt': 'Sem alterações.',
        'ru': 'Нет изменений.',
        'hi': 'कोई बदलाव नहीं।',
        'ml': 'മാറ്റങ്ങളൊന്നുമില്ല.',
        'id': 'Tidak ada perubahan.',
    },
    'Admin.thisWillChange': {
        'en': 'This will change:',
        'es': 'Esto cambiará:',
        'pt': 'Isso mudará:',
        'ru': 'Это изменит:',
        'hi': 'यह बदलेगा:',
        'ml': 'ഇത് മാറ്റും:',
        'id': 'Ini akan mengubah:',
    },
    'Admin.deleteAccount': {
        'en': 'Delete account',
        'es': 'Eliminar cuenta',
        'pt': 'Excluir conta',
        'ru': 'Удалить аккаунт',
        'hi': 'खाता हटाएं',
        'ml': 'അക്കൗണ്ട് ഇല്ലാതാക്കുക',
        'id': 'Hapus akun',
    },
    'Admin.deleteAccountConfirm': {
        'en': "Delete {nick}'s account? This cannot be undone.",
        'es': '¿Eliminar la cuenta de {nick}? Esto no se puede deshacer.',
        'pt': 'Excluir a conta de {nick}? Isso não pode ser desfeito.',
        'ru': 'Удалить аккаунт {nick}? Это нельзя отменить.',
        'hi': '{nick} का खाता हटाएं? यह पूर्ववत नहीं किया जा सकता।',
        'ml': '{nick}-ന്റെ അക്കൗണ്ട് ഇല്ലാതാക്കണോ? ഇത് പഴയപടിയാക്കാൻ കഴിയില്ല.',
        'id': 'Hapus akun {nick}? Ini tidak dapat dibatalkan.',
    },
    'Admin.accountDeleted': {
        'en': "{nick}'s account deleted.",
        'es': 'Cuenta de {nick} eliminada.',
        'pt': 'Conta de {nick} excluída.',
        'ru': 'Аккаунт {nick} удалён.',
        'hi': '{nick} का खाता हटाया गया।',
        'ml': '{nick}-ന്റെ അക്കൗണ്ട് ഇല്ലാതാക്കി.',
        'id': 'Akun {nick} dihapus.',
    },
}




BLACKLIST_FILE = os.path.join(PLAYERS_DIRECTORY, 'blacklist.json')

_blacklist: Set[str] = set()


def load_blacklist() -> Set[str]:
    global _blacklist
    try:
        with open(BLACKLIST_FILE, encoding='utf-8') as f:
            data = json.load(f)
        _blacklist = set(data.get('blocked', []))
    except FileNotFoundError:
        _blacklist = set()
    except Exception:
        _blacklist = set()
    return _blacklist


def init_blacklist() -> None:
    """Create blacklist.json with empty data if it doesn't exist."""
    if not os.path.exists(BLACKLIST_FILE):
        save_blacklist()


def save_blacklist() -> None:
    try:
        os.makedirs(PLAYERS_DIRECTORY, exist_ok=True)
        with open(BLACKLIST_FILE, 'w', encoding='utf-8') as f:
            json.dump({'blocked': sorted(_blacklist)}, f, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception:
        import babase
        babase.print_exception()


def is_blocked(account: str) -> bool:
    return account in _blacklist


def set_blocked(account: str, blocked: bool) -> None:
    if blocked:
        _blacklist.add(account)
    else:
        _blacklist.discard(account)
    save_blacklist()


# Keyed by player's real name
playerinfo: Dict[str, Dict[str, Any]] = {}

# Default values for a player record
default_player_record: Dict[str, Any] = {
    'profile_name': [],
    'nickname': '',
    'client_id': '?',
    'pb_id': None,
    'last_met_ts': None,
    'mutual_server': [],
    'searched_bcs': None,
    '_id': None,
}


def _ensure_dir() -> None:
    if not os.path.exists(PLAYERS_DIRECTORY):
        os.makedirs(PLAYERS_DIRECTORY)


def _migrate_record(name: str, record: Dict[str, Any]) -> bool:
    """Add missing default keys to an existing record. Returns True if changed."""
    changed = False
    for key, default_val in default_player_record.items():
        if key not in record:
            record[key] = default_val
            changed = True

    # Drop legacy fields
    for legacy in ('last_met', 'messages', 'messages_sent'):
        if legacy in record:
            del record[legacy]
            changed = True

    # Normalize profile_name to list
    profile = record.get('profile_name')
    if isinstance(profile, str):
        record['profile_name'] = [profile] if profile else []
        changed = True
    elif profile is None:
        record['profile_name'] = []
        changed = True

    # Normalize mutual_server to list
    mutual = record.get('mutual_server')
    if mutual and not isinstance(mutual, list):
        record['mutual_server'] = [mutual]
        changed = True

    return changed


def load_playerinfo(is_from_backup: bool = False) -> Dict[str, Dict[str, Any]]:
    """Load player info from disk, creating an empty file if absent."""
    global playerinfo
    try:
        if os.path.exists(PLAYERINFO_FILE):
            with open(PLAYERINFO_FILE, 'r', encoding='utf-8') as f:
                data: Dict[str, Dict[str, Any]] = load(f)

            changed = False
            for name, record in data.items():
                if _migrate_record(name, record):
                    changed = True

            playerinfo = data
            if changed:
                save_playerinfo(playerinfo, force=True)
            return playerinfo

        _ensure_dir()
        playerinfo = {}
        save_playerinfo(playerinfo, first_boot=True)
        return playerinfo

    except Exception as e:
        print(f'[playerinfo] load error: {e}')
        try:
            if os.path.exists(PLAYERINFO_FILE):
                os.remove(PLAYERINFO_FILE)
                if not is_from_backup:
                    return load_playerinfo(is_from_backup=True)
        except Exception as e2:
            print(f'[playerinfo] backup recovery error: {e2}')

    playerinfo = {}
    return playerinfo


def _trim_playerinfo(data: Dict[str, Dict[str, Any]], max_entries: int) -> bool:
    """Remove oldest players (by last_met_ts) if over limit. Returns True if trimmed."""
    if len(data) <= max_entries:
        return False
    sorted_names = sorted(
        data.keys(),
        key=lambda n: data[n].get('last_met_ts') or 0,
    )
    to_remove = len(data) - max_entries
    for name in sorted_names[:to_remove]:
        del data[name]
    return True


def save_playerinfo(
    data: Dict[str, Dict[str, Any]],
    first_boot: bool = False,
    force: bool = False,
) -> None:
    """Persist player info to disk, skipping if unchanged."""
    global playerinfo
    try:
        _ensure_dir()
        max_entries = int(finder_config.get(CFG_NAME_MAX_PLAYERINFO, 1000))
        _trim_playerinfo(data, max_entries)

        if not force and not first_boot:
            try:
                with open(PLAYERINFO_FILE, 'r', encoding='utf-8') as f:
                    on_disk = load(f)
                if on_disk == data:
                    return
            except Exception:
                pass
        with open(PLAYERINFO_FILE, 'w', encoding='utf-8') as f:
            dump(data, f, indent=JSONS_DEFAULT_INDENT_FILE, ensure_ascii=False)
        playerinfo = data
    except Exception as e:
        print(f'[playerinfo] save error: {e}')


def get_player(name: str) -> Dict[str, Any]:
    """Return player record, creating a default one if not present."""
    if not playerinfo:
        load_playerinfo()
    if name not in playerinfo:
        playerinfo[name] = dict(default_player_record)
    return playerinfo[name]


def update_player(name: str, key: str, value: Any) -> None:
    """Update a single field for a player and persist."""
    record = get_player(name)
    record[key] = value
    save_playerinfo(playerinfo, force=True)


def upsert_player(name: str, data: Dict[str, Any]) -> None:
    """Merge data into an existing player record (or create one) and persist."""
    record = get_player(name)
    record.update(data)
    save_playerinfo(playerinfo, force=True)


def add_profile_name(name: str, profile: str) -> None:
    """Add a profile name to the player's list if not already present."""
    record = get_player(name)
    profiles: List[str] = record.setdefault('profile_name', [])
    if profile and profile not in profiles:
        profiles.append(profile)
        save_playerinfo(playerinfo, force=True)


def add_mutual_server(name: str, server: str) -> None:
    """Add a mutual server to the player's list if not already present."""
    record = get_player(name)
    servers: List[str] = record.setdefault('mutual_server', [])
    if server and server not in servers:
        servers.append(server)
        save_playerinfo(playerinfo, force=True)


def remove_player(name: str) -> None:
    """Delete a player record and persist."""
    if name in playerinfo:
        del playerinfo[name]
        save_playerinfo(playerinfo, force=True)


def get_all_players() -> Dict[str, Dict[str, Any]]:
    """Return all stored player records."""
    if not playerinfo:
        load_playerinfo()
    return playerinfo


def sync_from_roster(
    roster: list,
    server_name: str,
    cmdprint: bool = False,
    logmsg: bool = False,
    new_display_strings: frozenset = frozenset(),
) -> None:
    """Process a BombSquad game roster and persist player data.

    Mirrors the logic from _start_get_player_info in LessPartyWindow.
    Call this from a background thread — it does file I/O.
    """
    import time
    import babase
    from babase import SpecialChar
    from bauiv1 import screenmessage

    def _msg(text: str) -> None:
        if logmsg:
            babase.pushcall(
                lambda t=text: screenmessage(t, color=COLOR_SCREENCMD_NORMAL),
                from_other_thread=True,
            )

    if not roster:
        return

    if not playerinfo:
        load_playerinfo()

    now_ts = time.time()
    v2_logo = babase.charstr(SpecialChar.V2_LOGO)
    special_chars = [babase.charstr(c) for c in SpecialChar]
    changed = False

    # Get local user's account name to skip it
    local_name: Optional[str] = None
    try:
        plus = babase.app.plus
        if plus is not None:
            raw_local = plus.get_v1_account_display_string()
            if raw_local:
                local_name = (
                    raw_local if raw_local[0] in special_chars
                    else v2_logo + raw_local
                )
    except Exception:
        pass

    for entry in roster:
        raw_name: str = entry.get('display_string', '')
        players_list: list = entry.get('players', [])
        client_id = entry.get('client_id', '?')

        if not raw_name:
            continue

        # Skip hidden server-side names
        if raw_name.startswith('<HIDDEN>'):
            continue

        # Skip the host
        if client_id == -1:
            continue

        # Prefix V2 logo
        if raw_name[0] in special_chars:
            real_name = raw_name
        else:
            real_name = v2_logo + raw_name

        # Skip the local user
        if local_name and real_name == local_name:
            continue

        full_names: List[str] = [p['name_full'] for p in players_list if 'name_full' in p]
        profile_names = full_names

        profile_joint = ', '.join(profile_names) if profile_names else ''
        existing: Optional[Dict[str, Any]] = playerinfo.get(real_name)

        if existing is None:
            playerinfo[real_name] = dict(default_player_record)
            playerinfo[real_name].update({
                'profile_name': profile_names,
                'client_id': client_id,
                'last_met_ts': now_ts,
                'mutual_server': [server_name] if server_name else [],
            })
            changed = True
            if profile_names:
                _msg(get_lang_text('playerInfo.newPlayer').format(
                    name=real_name, profile=profile_joint, cid=client_id))
                if cmdprint:
                    print(get_lang_text('playerInfo.newPlayer').format(
                        name=real_name, profile=profile_joint, cid=client_id))
            else:
                _msg(get_lang_text('playerInfo.newPlayerNoProfile').format(
                    name=real_name, cid=client_id))
                if cmdprint:
                    print(get_lang_text('playerInfo.newPlayerNoProfile').format(
                        name=real_name, cid=client_id))
        else:
            # Update client_id
            if existing.get('client_id') != client_id:
                _msg(get_lang_text('playerInfo.updateClientId').format(
                    name=real_name,
                    old=existing.get('client_id', '?'),
                    new=client_id,
                ))
                if cmdprint:
                    print(get_lang_text('playerInfo.updateClientId').format(
                        name=real_name,
                        old=existing.get('client_id', '?'),
                        new=client_id,
                    ))
                existing['client_id'] = client_id
                changed = True

            # Update profile_name
            last_profiles: List[str] = existing.get('profile_name') or []
            if profile_names and last_profiles != profile_names:
                if last_profiles:
                    _msg(get_lang_text('playerInfo.updateProfileName').format(
                        name=real_name, profile=profile_joint, cid=client_id))
                    if cmdprint:
                        print(get_lang_text('playerInfo.updateProfileName').format(
                            name=real_name, profile=profile_joint, cid=client_id))
                    existing['profile_name'] = profile_names
                else:
                    _msg(get_lang_text('playerInfo.addProfileName').format(
                        name=real_name, profile=profile_joint, cid=client_id))
                    if cmdprint:
                        print(get_lang_text('playerInfo.addProfileName').format(
                            name=real_name, profile=profile_joint, cid=client_id))
                    existing['profile_name'] = profile_names
                changed = True
            elif not profile_names and last_profiles:
                if cmdprint:
                    print(get_lang_text('playerInfo.refreshProfileName').format(
                        name=real_name,
                        profile=', '.join(last_profiles),
                        cid=client_id,
                    ))

            # Update mutual_server
            mutual: List[str] = existing.get('mutual_server') or []
            if isinstance(mutual, str):
                mutual = [mutual]
                existing['mutual_server'] = mutual
            if server_name and server_name not in mutual:
                if not mutual:
                    _msg(get_lang_text('playerInfo.mutualServerFirst').format(
                        name=real_name, server=server_name))
                    if cmdprint:
                        print(get_lang_text('playerInfo.mutualServerFirst').format(
                            name=real_name, server=server_name))
                else:
                    _msg(get_lang_text('playerInfo.mutualServerAdded').format(
                        name=real_name, server=server_name))
                    if cmdprint:
                        print(get_lang_text('playerInfo.mutualServerAdded').format(
                            name=real_name, server=server_name))
                mutual.append(server_name)
                existing['mutual_server'] = mutual
                changed = True

            existing['last_met_ts'] = now_ts

    if changed:
        save_playerinfo(playerinfo, force=True)


_uiscale_subscribers: list[Callable[[babase.UIScale], None]] = []
_uiscale_last_scale: babase.UIScale | None = None
_uiscale_monitor_started: bool = False


def get_uiscale() -> babase.UIScale:
    return bui.app.ui_v1.uiscale


def get_uiscale_name() -> str:
    scale = get_uiscale()
    if scale is babase.UIScale.SMALL:
        return 'SMALL'
    if scale is babase.UIScale.MEDIUM:
        return 'MEDIUM'
    return 'LARGE'


def log_uiscale(tag: str = '') -> None:
    pass


def _uiscale_subscribe(callback: Callable[[babase.UIScale], None]) -> None:
    if callback not in _uiscale_subscribers:
        _uiscale_subscribers.append(callback)


def _uiscale_unsubscribe(callback: Callable[[babase.UIScale], None]) -> None:
    if callback in _uiscale_subscribers:
        _uiscale_subscribers.remove(callback)


def _uiscale_poll() -> None:
    global _uiscale_last_scale
    current = get_uiscale()
    if current is not _uiscale_last_scale:
        _uiscale_last_scale = current
        log_uiscale('scale_changed')
        for cb in list(_uiscale_subscribers):
            try:
                cb(current)
            except Exception:
                babase.print_exception()
    babase.apptimer(1.0, _uiscale_poll)


def _uiscale_start_monitor() -> None:
    """Start polling for UIScale changes."""
    global _uiscale_last_scale, _uiscale_monitor_started
    if _uiscale_monitor_started:
        return
    _uiscale_monitor_started = True
    _uiscale_last_scale = get_uiscale()
    log_uiscale('monitor_start')
    babase.apptimer(1.0, _uiscale_poll)





def _safe_dirname(name: str) -> str:
    """Strip filesystem-unsafe characters from a server name."""
    unsafe = set('<>:"/\\|?*')
    result = ''.join(c for c in name if c not in unsafe and ord(c) >= 32)
    return result.strip() or 'Unknown'


def log_message(
    real_name: str,
    profile: str,
    text: str,
    server_name: str,
) -> None:
    """Write a chat message to chats.json and the server's ChatLog.txt."""
    os.makedirs(CHATS_DIRECTORY, exist_ok=True)
    _write_chats_json(real_name, profile, text)
    _write_server_log(real_name, profile, text, server_name)


def _write_chats_json(real_name: str, profile: str, text: str) -> None:
    try:
        data: dict = {}
        if os.path.exists(CHATS_JSON_FILE):
            with open(CHATS_JSON_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        data.setdefault(real_name, []).append(f'{profile} >> {text}')
        with open(CHATS_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=JSONS_DEFAULT_INDENT_FILE, ensure_ascii=False)
    except Exception as e:
        print(f'[chat_logger] chats.json error: {e}')


def _trim_server_logs(max_logs: int) -> None:
    """Remove oldest server log directories if count exceeds max_logs."""
    try:
        entries = [
            e for e in os.scandir(CHATS_DIRECTORY)
            if e.is_dir()
        ]
        if len(entries) <= max_logs:
            return
        entries.sort(key=lambda e: e.stat().st_mtime)
        import shutil
        for entry in entries[:len(entries) - max_logs]:
            shutil.rmtree(entry.path, ignore_errors=True)
    except Exception as e:
        print(f'[chat_logger] trim error: {e}')


def _write_server_log(
    real_name: str,
    profile: str,
    text: str,
    server_name: str,
) -> None:
    if not server_name:
        return

    safe_name = _safe_dirname(server_name)
    server_dir = os.path.join(CHATS_DIRECTORY, safe_name)
    log_file = os.path.join(server_dir, 'ChatLog.txt')

    first_time = not os.path.exists(server_dir)
    if first_time:
        max_logs = int(finder_config.get(CFG_NAME_MAX_CHAT_LOGS, 100))
        _trim_server_logs(max_logs)
        os.makedirs(server_dir, exist_ok=True)
        _notify_created(server_name)

    now = datetime.now().strftime('%d-%m-%Y | %H:%M:%S')
    # Show [v2 | profile] when profile differs from v2, else just [v2]
    if profile and profile != real_name:
        sender_part = f'[{real_name} | {profile}]'
    else:
        sender_part = f'[{real_name}]'

    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f'[{now}] {sender_part} >> {text}\n')
    except Exception as e:
        print(f'[chat_logger] ChatLog.txt error: {e}')


def _notify_created(server_name: str) -> None:
    import babase
    from bauiv1 import screenmessage
    babase.pushcall(
        lambda: screenmessage(
            get_lang_text('chatLog.created').format(server=server_name),
            color=(1.0, 0.6, 0.2),
        ),
        from_other_thread=True,
    )




_chat_last_count: int = 0
_chat_monitor_started: bool = False


def _chat_poll() -> None:
    global _chat_last_count
    try:
        msgs = bs.get_chat_messages()
        count = len(msgs)
        if count < _chat_last_count:
            _chat_last_count = count
        elif count > _chat_last_count:
            new_msgs = list(msgs[_chat_last_count:])
            _chat_last_count = count
            roster = list(bs.get_game_roster() or [])
            if new_msgs and roster:
                server_info = bs.get_connection_to_host_info_2()
                server_name = (
                    server_info.name
                    if server_info and server_info.name
                    else 'Party'
                )
                Thread(
                    target=_process_messages,
                    args=(new_msgs, roster, server_name),
                    daemon=True,
                ).start()
    except Exception:
        babase.print_exception()
    babase.apptimer(1.0, _chat_poll)


def _find_v2_for_sender(
    sender: str,
    roster: list,
    special_chars: list,
    v2_logo: str,
) -> tuple[str | None, str]:
    """Return (v2_real_name, profile_name) matching the chat sender."""
    for entry in roster:
        if entry.get('client_id') == -1:
            continue  # skip host
        for player in entry.get('players', []):
            name = player.get('name', '')
            name_full = player.get('name_full', '')
            if sender in (name, name_full) or name in sender or name_full in sender:
                raw = entry.get('display_string', '')
                if not raw:
                    break
                real_name = raw if raw[0] in special_chars else v2_logo + raw
                return real_name, name_full or name or sender
    return None, sender


def _process_messages(msgs: list[str], roster: list, server_name: str) -> None:
    from babase import SpecialChar

    special_chars = [babase.charstr(c) for c in SpecialChar]
    v2_logo = babase.charstr(SpecialChar.V2_LOGO)

    # Get local user to optionally skip own messages
    local_name: str | None = None
    try:
        plus = babase.app.plus
        if plus is not None:
            raw_local = plus.get_v1_account_display_string()
            if raw_local:
                local_name = (
                    raw_local if raw_local[0] in special_chars
                    else v2_logo + raw_local
                )
    except Exception:
        pass

    for msg in msgs:
        if ': ' not in msg:
            continue
        sender, _, body = msg.partition(': ')
        body = body.strip()
        if not body:
            continue

        real_name, profile = _find_v2_for_sender(
            sender, roster, special_chars, v2_logo
        )
        if real_name is None:
            continue
        if local_name and real_name == local_name:
            continue

        log_message(real_name, profile, body, server_name)


def _chat_start_monitor() -> None:
    """Start polling chat for new messages. Call once at module load."""
    global _chat_monitor_started
    if _chat_monitor_started:
        return
    _chat_monitor_started = True
    babase.apptimer(2.0, _chat_poll)




_roster_last_roster: list = []
_roster_monitor_started: bool = False


def _notify_joins(roster: list, new_display_strings: frozenset) -> None:
    """Show colored screenmessages for blacklisted/friend/nicknamed players joining."""
    if not new_display_strings:
        return
    try:
        from bauiv1 import screenmessage

        v2_logo = babase.charstr(babase.SpecialChar.V2_LOGO)
        special_chars = [babase.charstr(c) for c in babase.SpecialChar]

        def _normalize(name: str) -> str:
            if name and name[0] in special_chars:
                return name
            return v2_logo + name if name else name

        friends = load_friends()
        friend_names: set[str] = set()
        for f in friends:
            n = f['name']
            friend_names.add(n)
            friend_names.add(n.replace(v2_logo, ''))
            friend_names.add(f'{v2_logo}{n}')

        all_players = get_all_players()

        for entry in roster:
            raw_name: str = entry.get('display_string', '')
            if not raw_name or raw_name.startswith('<HIDDEN>'):
                continue
            if entry.get('client_id') == -1:
                continue
            if raw_name not in new_display_strings:
                continue

            real_name = _normalize(raw_name)
            player_data = all_players.get(real_name) or all_players.get(raw_name)
            nickname = (player_data.get('nickname') or '').strip() if player_data else ''

            if is_blocked(real_name) or is_blocked(raw_name):
                msg = get_lang_text('playerInfo.joinBlacklist').format(name=real_name)
                screenmessage(msg, color=(1.0, 0.3, 0.3))
            elif real_name in friend_names or raw_name in friend_names:
                nick_suffix = f' #{nickname[:12]}' if nickname else ''
                msg = get_lang_text('playerInfo.joinFriend').format(name=real_name) + nick_suffix
                screenmessage(msg, color=(0.3, 1.0, 0.4))
            elif nickname:
                msg = get_lang_text('playerInfo.joinNickname').format(
                    name=real_name, nickname=nickname[:12])
                screenmessage(msg, color=(1.0, 0.6, 0.2))
    except Exception:
        babase.print_exception()


def _roster_poll() -> None:
    global _roster_last_roster
    try:
        roster = bs.get_game_roster()
        roster_key = frozenset(p.get('display_string', '') for p in roster)
        last_key = frozenset(p.get('display_string', '') for p in _roster_last_roster)

        if roster_key != last_key:
            new_display_strings = roster_key - last_key
            _roster_last_roster = list(roster)
            if roster:
                server_info = bs.get_connection_to_host_info_2()
                server_name = (
                    server_info.name
                    if server_info and server_info.name
                    else 'Party'
                )
                _notify_joins(roster, new_display_strings)
                _roster_copy = list(roster)
                Thread(
                    target=_run_sync,
                    args=(_roster_copy, server_name, new_display_strings),
                    daemon=True,
                ).start()
    except Exception:
        babase.print_exception()
    babase.apptimer(1.0, _roster_poll)


def _run_sync(roster: list, server_name: str, new_display_strings: frozenset = frozenset()) -> None:
    sync_from_roster(roster, server_name, logmsg=True, new_display_strings=new_display_strings)


def _roster_start_monitor() -> None:
    """Start polling for roster changes. Call once at module load."""
    global _roster_monitor_started
    if _roster_monitor_started:
        return
    _roster_monitor_started = True
    babase.apptimer(1.0, _roster_poll)


# Global state
finder_config: Dict[str, Any] = {}
friends_list: List[Dict[str, Any]] = []


def load_finder_config(is_from_backup: bool = False,
                       read_only: bool = False) -> Dict[str, Any]:
    """Load config from file, creating it with defaults if absent."""
    global finder_config
    try:
        if os.path.exists(CONFIGS_FILE):
            updated = False
            with open(CONFIGS_FILE, 'r') as file:
                loaded = load(file)

            if read_only:
                return loaded

            finder_config = loaded

            if not read_only:
                keys_to_remove = [k for k in finder_config
                                   if k not in default_finder_config]
                for key in keys_to_remove:
                    TIP(f"{get_lang_text('partyConfigLoadRemoveKey')}: {key}",
                        color=COLOR_SCREENCMD_ERROR)
                    del finder_config[key]
                    if not updated:
                        updated = True

                for default_key, default_value in default_finder_config.items():
                    if default_key not in finder_config:
                        TIP(f"{get_lang_text('partyConfigLoadAddKey')}: {default_key}",
                            color=COLOR_SCREENCMD_NORMAL)
                        finder_config[default_key] = default_value
                        if not updated:
                            updated = True

                if updated:
                    save_finder_config(finder_config)
            return finder_config
        else:
            if not os.path.exists(MY_DIRECTORY):
                os.makedirs(MY_DIRECTORY)
            save_finder_config(default_finder_config, first_boot=True)
            finder_config = default_finder_config
            return default_finder_config
    except Exception as e:
        TIP(f"Error loading config: {e}", color=COLOR_SCREENCMD_ERROR)
        print(e)
        try:
            if os.path.exists(CONFIGS_FILE) and os.path.isfile(CONFIGS_FILE):
                os.remove(CONFIGS_FILE)
                if not is_from_backup:
                    load_finder_config(is_from_backup=True)
        except Exception as e2:
            print(e2)
    finder_config = default_finder_config
    return default_finder_config


def save_finder_config(config: Dict[str, Any],
                       first_boot: bool = False,
                       force: bool = False) -> None:
    """Persist config to disk, skipping if unchanged."""
    global finder_config
    try:
        if not config:
            return
        on_disk = load_finder_config(read_only=True)
        if not force and not first_boot and on_disk == config:
            return
        with open(CONFIGS_FILE, 'w', encoding='utf-8') as file:
            dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
            finder_config = config
    except FileNotFoundError:
        with open(CONFIGS_FILE, 'w', encoding='utf-8') as file:
            dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print(f'[save_finder_config] error: {e}')


def update_finder_config(key: str, value: Any) -> None:
    """Update a single key in the config and persist."""
    global finder_config
    if not finder_config:
        load_finder_config()
    if finder_config and key in finder_config:
        finder_config[key] = value
        save_finder_config(finder_config)
        load_finder_config()


def load_friends(is_from_backup: bool = False) -> List[Dict[str, Any]]:
    """Load friends list from disk, creating an empty one if absent."""
    global friends_list
    try:
        if os.path.exists(FRIENDS_FILE):
            with open(FRIENDS_FILE, 'r', encoding='utf-8') as file:
                friends_list = load(file)

            changed = False
            for friend in friends_list:
                if 'name' not in friend or 'id' not in friend:
                    friends_list.remove(friend)
                    changed = True
                    continue
                for key in ('accounts', 'account_pb', 'account_id'):
                    if key not in friend:
                        friend[key] = None
                        changed = True

            if changed:
                save_friends(friends_list)
            return friends_list

        if not os.path.exists(PLAYERS_DIRECTORY):
            os.makedirs(PLAYERS_DIRECTORY)
        friends_list = []
        save_friends(friends_list, first_boot=True)
        init_blacklist()
        return friends_list

    except Exception as e:
        TIP(f"Error loading friends: {e}", color=COLOR_SCREENCMD_ERROR)
        print(e)
        try:
            if os.path.exists(FRIENDS_FILE):
                os.remove(FRIENDS_FILE)
                if not is_from_backup:
                    return load_friends(is_from_backup=True)
        except Exception as e2:
            print(e2)
    friends_list = []
    return friends_list


def save_friends(data: List[Dict[str, Any]],
                 first_boot: bool = False,
                 force: bool = False) -> None:
    """Persist friends list to disk."""
    global friends_list
    try:
        if not force and not first_boot and load_friends() == data:
            return
        with open(FRIENDS_FILE, 'w', encoding='utf-8') as file:
            dump(data, file, indent=JSONS_DEFAULT_INDENT_FILE)
            friends_list = data
    except Exception as e:
        print(e)


def add_friend(name: str, friend_id: str,
               accounts: List[str] | None = None,
               account_pb: str | None = None,
               account_id: str | None = None) -> None:
    """Add a new friend, skipping duplicates by id."""
    load_friends()
    for f in friends_list:
        if f['id'] == friend_id:
            TIP('Friend ID already exists.', color=COLOR_SCREENCMD_ERROR)
            return
    friends_list.append({
        'name': name,
        'id': friend_id,
        'accounts': accounts or [],
        'account_pb': account_pb,
        'account_id': account_id,
    })
    save_friends(friends_list)


def remove_friend(friend_id: str) -> None:
    """Delete a friend by id."""
    load_friends()
    friends_list[:] = [f for f in friends_list if f['id'] != friend_id]
    save_friends(friends_list)


def update_friend(friend_id: str, key: str, value: Any) -> None:
    """Update a single field for a friend."""
    load_friends()
    for f in friends_list:
        if f['id'] == friend_id:
            f[key] = value
            save_friends(friends_list)
            return


def add_account(friend_id: str, account_name: str) -> None:
    """Append an account name to a friend's account list."""
    load_friends()
    for f in friends_list:
        if f['id'] == friend_id:
            if f['accounts'] is None:
                f['accounts'] = []
            if account_name not in f['accounts']:
                f['accounts'].append(account_name)
            save_friends(friends_list)
            return


def remove_account(friend_id: str, account_name: str) -> None:
    """Remove an account name from a friend's account list."""
    load_friends()
    for f in friends_list:
        if f['id'] == friend_id and f['accounts']:
            if account_name in f['accounts']:
                f['accounts'].remove(account_name)
                save_friends(friends_list)
            return


def get_app_lang_as_id() -> str:
    """Return the active language ID (e.g. 'en', 'es')."""
    if not finder_config:
        load_finder_config()

    party_lang = finder_config.get(CFG_NAME_PREFFERED_LANG)
    if party_lang:
        return party_lang

    app_lang = babase.app.lang.language
    lang_id = 'en'
    for lang_code, lang_info in DEFAULT_LANGUAGES_DICT.items():
        if app_lang == lang_info['name']:
            lang_id = lang_code
            break

    update_finder_config(CFG_NAME_PREFFERED_LANG, lang_id)
    return lang_id


def get_languages_for_current_platform() -> Dict[str, str]:
    """Return language ids/names filtered for the current platform."""
    if babase.app.classic.platform != 'android':
        return {
            lang_id: lang_info['name']
            for lang_id, lang_info in DEFAULT_LANGUAGES_DICT.items()
            if lang_info['pc_compatible']
        }
    return get_language_names_dict()


def get_lang_text(key: str, lang_id: Optional[str] = None) -> str:
    """Return translated text for key. Falls back to 'en' if unavailable."""
    invalid_text = INVALID_KEY_TEXT.format(key)
    lang = (lang_id if lang_id in DEFAULT_AVAILABLE_LANG_ID_LIST
            else get_app_lang_as_id())

    text = Translate_Texts.get(key, {}).get(lang, '')
    if not text:
        en_text = Translate_Texts.get(key, {}).get('en', '')
        if en_text:
            return f'*{en_text}'

    return text if text else f'**{invalid_text}'


def bw(*, oac=None, **k) -> _bauiv1.Widget:
    """Create a styled button widget with white texture."""
    return obw(
        texture=gt('white'),
        on_activate_call=oac,
        enable_sound=False,
        **k
    )


def cw(*, size=None, oac=None, **k):
    """Create a full-screen overlay container with a dim background."""
    p = ocw(
        parent=zw('overlay_stack'),
        background=False,
        transition='in_scale',
        size=size,
        on_outside_click_call=oac,
        **k
    )
    x, y = babase.get_virtual_screen_size()
    iw(
        parent=p,
        texture=gt('white'),
        size=(x * 2, y * 2),
        position=(-x * 0.5, 0 - 200),
        opacity=0.55,
        color=(0, 0, 0)
    )
    iw(parent=p, size=size)
    return (p,)


def TIP(text: str, color: tuple | None = None) -> None:
    """Display a screen message. Uses theme COLOR_TERTIARY if no color given."""
    if color is None:
        try:
            color = ReactiveTheme().get_color('COLOR_TERTIARY')
        except Exception:
            color = (1.0, 1.0, 1.0)
    push(text, color)
    bui.getsound('ding').play()


# Spinner animation state keyed by widget id
_spinner_states: Dict[int, Any] = {}


def spinner(
    *,
    edit: _bauiv1.Widget | None = None,
    parent: _bauiv1.Widget | None = None,
    size: Optional[Sequence[float]] = None,
    position: Optional[Sequence[float]] = None,
    color: Optional[Sequence[float]] = None,
    opacity: float | None = None,
    style: str = 'bomb',
    fade: bool = True,
    visible: bool = True
) -> _bauiv1.Widget:
    """Create or edit an animated spinner image widget."""
    if size is None:
        size = (50, 50)
    if color is None:
        color = (1, 1, 1)

    if edit is not None:
        widget_id = id(edit)
        if widget_id in _spinner_states:
            _spinner_states[widget_id]['visible'] = visible
        return edit

    image_widget = iw(
        parent=parent,
        size=size,
        position=position,
        color=color,
        opacity=1.0 if visible else 0.0,
        texture=gt('spinner0'),
        has_alpha_channel=True
    )
    main_widget = image_widget
    widget_id = id(main_widget)
    _spinner_states[widget_id] = {
        'style': style,
        'fade': fade,
        'visible': visible,
        'presence': 1.0 if visible else 0.0,
        'current_frame': 0,
        'last_update': apptime(),
        'image_widget': image_widget,
    }

    def update_spinner() -> None:
        if not main_widget.exists():
            _spinner_states.pop(widget_id, None)
            return
        if widget_id not in _spinner_states:
            return
        state = _spinner_states[widget_id]
        current_time = apptime()
        elapsed = current_time - state['last_update']

        if state['visible']:
            state['presence'] = (min(1.0, state['presence'] + elapsed * 1.0)
                                 if state['fade'] else 1.0)
        else:
            state['presence'] = (max(0.0, state['presence'] - elapsed * 2.0)
                                 if state['fade'] else 0.0)

        alpha = max(0.0, min(1.0, state['presence'] * 2.0 - 1.0))
        frame = int(current_time * 24) % 12
        state['current_frame'] = frame

        if state['image_widget'].exists():
            iw(edit=state['image_widget'],
               texture=gt(f'spinner{frame}'),
               opacity=alpha)

        state['last_update'] = current_time
        if state['visible'] or state['presence'] > 0:
            teck(0.016, update_spinner)

    teck(0.016, update_spinner)
    return main_widget


def spinner_set_visible(spinner_widget: _bauiv1.Widget, visible: bool) -> None:
    """Set spinner visibility (triggers fade if fade=True)."""
    widget_id = id(spinner_widget)
    if widget_id in _spinner_states:
        _spinner_states[widget_id]['visible'] = visible


def spinner_set_fade(spinner_widget: _bauiv1.Widget, fade: bool) -> None:
    """Toggle fade-in/out for a spinner."""
    widget_id = id(spinner_widget)
    if widget_id in _spinner_states:
        _spinner_states[widget_id]['fade'] = fade


# Error display animation state keyed by widget id
_error_states: Dict[int, Any] = {}


def error_display(
    *,
    edit: _bauiv1.Widget | None = None,
    parent: _bauiv1.Widget | None = None,
    size: Optional[Sequence[float]] = None,
    position: Optional[Sequence[float]] = None,
    color: Optional[Sequence[float]] = None,
    opacity: float | None = None,
    error_text: str = '',
    text_color: Optional[Sequence[float]] = None,
    text_scale: float = 1.2,
    text_maxwidth: float = 600,
    icon_texture: str = 'cuteSpaz',
    fade: bool = True,
    visible: bool = True
) -> _bauiv1.Widget:
    """Create or edit an error display widget (icon + text) with fade."""
    if size is None:
        size = (180, 200)
    if color is None:
        color = (1, 1, 1)
    if text_color is None:
        try:
            text_color = ReactiveTheme().get_color('COLOR_PRIMARY')
        except Exception:
            text_color = (1, 1, 1)

    if edit is not None:
        widget_id = id(edit)
        if widget_id in _error_states:
            state = _error_states[widget_id]
            state['visible'] = visible
            state['error_text'] = error_text
            if state['text_widget'] and state['text_widget'].exists():
                tw(edit=state['text_widget'], text=error_text)
        return edit

    container = ocw(parent=parent, size=size, position=position,
                    background=False)
    icon_size = (size[0], size[1] * 0.7)
    text_height = size[1] * 0.3

    try:
        icon_widget = iw(
            parent=container,
            size=icon_size,
            position=(0, text_height),
            color=color,
            opacity=1.0 if visible else 0.0,
            texture=gt(icon_texture),
            has_alpha_channel=True
        )
    except Exception as e:
        print(f'Error creating error icon: {e}')
        try:
            icon_widget = iw(
                parent=container,
                size=(size[0] * 0.55, size[1] * 0.55),
                position=(size[0] * 0.225, text_height + size[1] * 0.15),
                color=color,
                opacity=1.0 if visible else 0.0,
                texture=gt('neoSpazIcon'),
                has_alpha_channel=True
            )
        except Exception as e2:
            print(f'Fallback also failed: {e2}')
            icon_widget = iw(
                parent=container, size=(1, 1), position=(0, 0),
                texture=gt('white'), opacity=0.0
            )

    text_widget = tw(
        parent=container,
        text=error_text,
        color=text_color,
        position=(size[0] * 0.2 - 30, text_height * 0.2 - 20),
        h_align='center',
        v_align='center',
        scale=text_scale,
        maxwidth=text_maxwidth,
        size=(size[0], text_height)
    )

    widget_id = id(container)
    _error_states[widget_id] = {
        'fade': fade,
        'visible': visible,
        'presence': 1.0 if visible else 0.0,
        'icon_widget': icon_widget,
        'text_widget': text_widget,
        'container': container,
        'error_text': error_text,
        'last_update': apptime(),
    }

    def update_error_display() -> None:
        if not container.exists():
            _error_states.pop(widget_id, None)
            return
        if widget_id not in _error_states:
            return
        state = _error_states[widget_id]
        current_time = apptime()
        elapsed = current_time - state['last_update']

        if state['visible']:
            state['presence'] = (min(1.0, state['presence'] + elapsed * 2.0)
                                 if state['fade'] else 1.0)
        else:
            state['presence'] = (max(0.0, state['presence'] - elapsed * 3.0)
                                 if state['fade'] else 0.0)

        alpha = max(0.0, min(1.0, state['presence']))

        if state['icon_widget'] and state['icon_widget'].exists():
            iw(edit=state['icon_widget'], opacity=alpha)

        if state['text_widget'] and state['text_widget'].exists():
            r, g, b = text_color[:3]
            tw(edit=state['text_widget'], color=(r, g, b, alpha))

        state['last_update'] = current_time
        if state['visible'] or state['presence'] > 0:
            teck(0.016, update_error_display)

    teck(0.016, update_error_display)
    return container


def error_display_set_visible(error_widget: _bauiv1.Widget,
                               visible: bool) -> None:
    """Set visibility for an error display (triggers fade)."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        _error_states[widget_id]['visible'] = visible


def error_display_set_fade(error_widget: _bauiv1.Widget, fade: bool) -> None:
    """Toggle fade-in/out for an error display."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        _error_states[widget_id]['fade'] = fade


def error_display_set_text(error_widget: _bauiv1.Widget, text: str) -> None:
    """Update the error message text."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        state = _error_states[widget_id]
        state['error_text'] = text
        if state['text_widget'] and state['text_widget'].exists():
            tw(edit=state['text_widget'], text=text)


def error_display_get_text(error_widget: _bauiv1.Widget) -> str:
    """Return the current error message text."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        return _error_states[widget_id].get('error_text', '')
    return ''


def error_display_set_icon(error_widget: _bauiv1.Widget,
                            icon_texture: str) -> None:
    """Change the icon texture of an error display."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        state = _error_states[widget_id]
        if state['icon_widget'] and state['icon_widget'].exists():
            try:
                iw(edit=state['icon_widget'], texture=gt(icon_texture))
            except Exception:
                print(f"Error: Texture '{icon_texture}' not found")


def wrap_text(text: str, max_line_length: int = 80) -> List[str]:
    """Wrap text at word boundaries to the given line length."""
    words = text.split()
    broken_words: List[str] = []
    for word in words:
        if len(word) > max_line_length:
            for i in range(0, len(word), max_line_length):
                broken_words.append(word[i:i + max_line_length])
        else:
            broken_words.append(word)

    lines: List[str] = []
    current_line: List[str] = []
    current_length = 0

    for word in broken_words:
        new_length = (current_length + 1 + len(word)
                      if current_line else len(word))
        if new_length <= max_line_length:
            current_line.append(word)
            current_length = new_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(' '.join(current_line))
    return lines


def _get_popup_window_scale() -> float:
    """Return scale factor for popup windows based on UI scale."""
    uiscale = bui.app.ui_v1.uiscale
    if uiscale is babase.UIScale.SMALL:
        return 2.3
    elif uiscale is babase.UIScale.MEDIUM:
        return 1.65
    return 1.23


def _creat_Lstr_list(string_list: List[str]) -> List[babase.Lstr]:
    """Convert a list of strings to Lstr objects."""
    return [babase.Lstr(value=s) for s in string_list]


_DEFAULT_QUICK_RESPONDS: List[str] = [
    'Good Game!',
    'Nice one!',
    'Let\'s go!',
]


def load_quick_responds() -> List[str]:
    """Load quick respond messages from file."""
    try:
        if os.path.exists(QUICK_RESPONDS_FILE):
            with open(QUICK_RESPONDS_FILE, 'r') as f:
                lines = [l for l in f.read().splitlines() if l.strip()]
                return lines if lines else list(_DEFAULT_QUICK_RESPONDS)
        save_quick_responds(_DEFAULT_QUICK_RESPONDS)
        return list(_DEFAULT_QUICK_RESPONDS)
    except Exception:
        return list(_DEFAULT_QUICK_RESPONDS)


def save_quick_responds(data: List[str]) -> None:
    """Save quick respond messages to file."""
    try:
        os.makedirs(os.path.dirname(QUICK_RESPONDS_FILE), exist_ok=True)
        with open(QUICK_RESPONDS_FILE, 'w') as f:
            f.write('\n'.join(data))
    except Exception:
        pass



class BorderWindow:
    """Computes border sizes and positions for a window rectangle."""

    class BorderInfo:
        def __init__(self, size: tuple, position: tuple) -> None:
            self.size = size
            self.position = position

    def __init__(self, window_size: tuple,
                 border_thickness: int = 4,
                 top_extra: int = 4) -> None:
        self.window_width, self.window_height = window_size
        self.border_thickness = border_thickness
        self.top_extra = top_extra

        self.border_left = self._make_border(
            size=(border_thickness, self.window_height),
            position=(0, 0)
        )
        self.border_top = self._make_border(
            size=(self.window_width + top_extra, border_thickness),
            position=(0, self.window_height)
        )
        self.border_right = self._make_border(
            size=(border_thickness, self.window_height),
            position=(self.window_width, 0)
        )
        self.border_bottom = self._make_border(
            size=(self.window_width, border_thickness),
            position=(0, 0)
        )

    def _make_border(self, size: tuple, position: tuple) -> BorderInfo:
        return BorderWindow.BorderInfo(size=size, position=position)




class ReactiveTheme:
    """Manages theme colors and notifies subscribers on color change."""

    def __init__(self) -> None:
        self._callbacks: dict = {}
        self._colors: dict = {}
        self._load_initial_colors()

    def _load_initial_colors(self) -> None:
        if not finder_config:
            load_finder_config()
        cfg = finder_config
        self._colors = {
            'COLOR_BACKGROUND': tuple(cfg.get(CFG_NAME_COLOR_BACKGROUND, (0.1, 0.1, 0.1))),
            'COLOR_SECONDARY': tuple(cfg.get(CFG_NAME_COLOR_SECONDARY, (0.2, 0.2, 0.2))),
            'COLOR_TERTIARY': tuple(cfg.get(CFG_NAME_COLOR_TERTIARY, (0.6, 0.6, 0.6))),
            'COLOR_PRIMARY': tuple(cfg.get(CFG_NAME_COLOR_PRIMARY, (1.0, 1.0, 1.0))),
            'COLOR_ACCENT': tuple(cfg.get(CFG_NAME_COLOR_ACCENT, (1.0, 1.0, 1.0))),
            'COLOR_BUTTON': tuple(cfg.get(CFG_NAME_COLOR_BUTTON, (0.25, 0.25, 0.3))),
        }

    def get_color(self, color_name: str) -> tuple:
        """Return the current color tuple for the given name."""
        return self._colors.get(color_name, (1.0, 1.0, 1.0))

    def get_color_lambda(self, color_name: str):
        """Return a lambda that always returns the current color."""
        return lambda: self._colors.get(color_name)

    def subscribe(self, color_name: str, callback) -> None:
        """Register callback to fire when the color changes."""
        if color_name not in self._callbacks:
            self._callbacks[color_name] = []
        self._callbacks[color_name].append(callback)

    def unsubscribe(self, color_name: str, callback) -> None:
        """Remove a previously registered callback."""
        if color_name in self._callbacks and callback in self._callbacks[color_name]:
            self._callbacks[color_name].remove(callback)

    def update_colors(self, colors_dict: dict) -> None:
        """Update multiple colors and notify subscribers of changes."""
        changed = []
        for color_name, new_color in colors_dict.items():
            if color_name in self._colors and self._colors[color_name] != new_color:
                self._colors[color_name] = new_color
                changed.append(color_name)

        for color_name in changed:
            if color_name in self._callbacks:
                for callback in self._callbacks[color_name][:]:
                    try:
                        callback(self._colors[color_name])
                    except Exception as e:
                        print(f'Error in callback of {color_name}: {e}')

    def refresh_from_config(self) -> None:
        """Reload colors from config and notify subscribers of changes."""
        old_colors = self._colors.copy()
        self._load_initial_colors()

        changed = [name for name, color in self._colors.items()
                   if old_colors.get(name) != color]

        for color_name in changed:
            if color_name in self._callbacks:
                for callback in self._callbacks[color_name][:]:
                    try:
                        callback(self._colors[color_name])
                    except Exception as e:
                        print(f'Error in callback of {color_name}: {e}')




class ReactiveLanguage:
    """Manages translated texts and notifies subscribers on language change."""

    def __init__(self) -> None:
        self._callbacks: dict = {}
        self._texts: dict = {}
        self._current_lang = 'en'
        self._load_initial_texts()

    def _load_initial_texts(self) -> None:
        if not finder_config:
            load_finder_config()
        self._current_lang = get_app_lang_as_id()
        self._load_language_texts(self._current_lang)

    def _load_language_texts(self, lang_id: str) -> None:
        self._texts = {}
        for text_key, translations in Translate_Texts.items():
            text = translations.get(lang_id, translations.get('en', f'[{text_key}]'))
            self._texts[text_key] = text

    def get_text(self, text_key: str, default: str | None = None) -> str:
        """Return current text for key."""
        return self._texts.get(text_key, default or f'[{text_key}]')

    def get_text_lambda(self, text_key: str, default: str | None = None):
        """Return a lambda that always returns the current text."""
        return lambda: self._texts.get(text_key, default or f'[{text_key}]')

    def subscribe(self, text_key: str, callback) -> None:
        """Register callback to fire when the text for text_key changes."""
        if text_key not in self._callbacks:
            self._callbacks[text_key] = []
        self._callbacks[text_key].append(callback)

    def unsubscribe(self, text_key: str, callback) -> None:
        """Remove a previously registered callback."""
        if text_key in self._callbacks and callback in self._callbacks[text_key]:
            self._callbacks[text_key].remove(callback)

    def update_language(self, lang_id: str) -> None:
        """Switch language and notify subscribers of changed texts."""
        if lang_id == self._current_lang:
            return
        old_texts = self._texts.copy()
        self._current_lang = lang_id
        self._load_language_texts(lang_id)

        for text_key, callback_list in self._callbacks.items():
            old_text = old_texts.get(text_key)
            new_text = self._texts.get(text_key)
            if old_text != new_text:
                for callback in callback_list[:]:
                    try:
                        callback(new_text)
                    except Exception as e:
                        print(f'Error in callback of {text_key}: {e}')

    def refresh_from_config(self) -> None:
        """Reload language from config and notify if it changed."""
        old_lang = self._current_lang
        self._load_initial_texts()
        if old_lang != self._current_lang:
            for text_key, callback_list in self._callbacks.items():
                for callback in callback_list[:]:
                    try:
                        callback(self._texts.get(text_key, text_key))
                    except Exception as e:
                        print(f'Error in callback of {text_key}: {e}')

language: ReactiveLanguage = ReactiveLanguage()
theme: ReactiveTheme = ReactiveTheme()
_global_language = language
_global_theme = theme
_language = language
_theme = theme





_SESSION_START = datetime.now(timezone.utc)
_dm_window_open = False
_SCREENMSG_CFG_KEY = 'dm_screenmsg_enabled'
_server_online: bool | None = None
_online_friend_ids: set = set()
_online_status_listeners: list = []
_pending_request_count: int = 0
_pending_request_listeners: list = []
_active_dm_chat_friend_id: Optional[int] = None
_unread_dm_listeners: list = []


def set_server_online(val: bool) -> None:
    global _server_online
    _server_online = val


def is_server_online() -> bool | None:
    """Returns True/False once ping completes, None if still pending."""
    return _server_online


def get_online_friend_ids() -> frozenset:
    """Returns the set of currently online friend user IDs."""
    return frozenset(_online_friend_ids)


def add_online_status_listener(cb) -> None:
    if cb not in _online_status_listeners:
        _online_status_listeners.append(cb)


def remove_online_status_listener(cb) -> None:
    try:
        _online_status_listeners.remove(cb)
    except ValueError:
        pass


def _notify_online_status_listeners() -> None:
    for cb in list(_online_status_listeners):
        try:
            cb()
        except Exception:
            pass


def get_pending_request_count() -> int:
    return _pending_request_count


def set_pending_request_count(count: int) -> None:
    global _pending_request_count
    _pending_request_count = count
    _notify_pending_request_listeners()


def add_pending_request_listener(cb) -> None:
    if cb not in _pending_request_listeners:
        _pending_request_listeners.append(cb)


def remove_pending_request_listener(cb) -> None:
    try:
        _pending_request_listeners.remove(cb)
    except ValueError:
        pass


def _notify_pending_request_listeners() -> None:
    for cb in list(_pending_request_listeners):
        try:
            cb()
        except Exception:
            pass


def set_active_dm_chat(friend_id: Optional[int]) -> None:
    global _active_dm_chat_friend_id
    _active_dm_chat_friend_id = friend_id


def get_active_dm_chat() -> Optional[int]:
    return _active_dm_chat_friend_id


def add_unread_dm_listener(cb) -> None:
    if cb not in _unread_dm_listeners:
        _unread_dm_listeners.append(cb)


def remove_unread_dm_listener(cb) -> None:
    try:
        _unread_dm_listeners.remove(cb)
    except ValueError:
        pass


def _notify_unread_dm_listeners() -> None:
    for cb in list(_unread_dm_listeners):
        try:
            cb()
        except Exception:
            pass


def get_unread_dm_count(friend_id: int) -> int:
    """Return unread message count for a conversation."""
    return load_dm_msgs().get(str(friend_id), {}).get('unread', 0)


def get_all_unread_dm_counts() -> dict:
    """Return {str(friend_id): count} for all conversations with unread > 0."""
    return {
        fid: data['unread']
        for fid, data in load_dm_msgs().items()
        if data.get('unread', 0) > 0
    }


def clear_unread_dm_count(friend_id: int) -> None:
    """Reset unread count to 0 for a conversation."""
    data = load_dm_msgs()
    key = str(friend_id)
    if data.get(key, {}).get('unread', 0) > 0:
        data[key]['unread'] = 0
        _save_dm_msgs(data)
        _notify_unread_dm_listeners()


def increment_unread_dm_count(friend_id: int) -> None:
    """Increment unread count by 1 for a conversation."""
    data = load_dm_msgs()
    key = str(friend_id)
    if key not in data:
        data[key] = {'nickname': '?', 'messages': [], 'unread': 0}
    data[key]['unread'] = data[key].get('unread', 0) + 1
    _save_dm_msgs(data)
    _notify_unread_dm_listeners()


def _on_friend_request_received(sender_nick: str) -> None:
    global _pending_request_count
    _pending_request_count += 1
    _notify_pending_request_listeners()
    try:
        import bauiv1 as bui
        bui.screenmessage(f'{sender_nick} sent you a friend request!', color=(1.0, 0.65, 0.0))
        bui.getsound('shieldUp').play()
    except Exception as e:
        print(f'[DM] screenmessage error: {e}')


def get_session_start() -> datetime:
    return _SESSION_START


def set_dm_window_open(val: bool) -> None:
    global _dm_window_open
    _dm_window_open = val


def is_dm_window_open() -> bool:
    return _dm_window_open


def get_screenmsg_enabled() -> bool:
    return bool(babase.app.config.get(_SCREENMSG_CFG_KEY, True))


def set_screenmsg_enabled(val: bool) -> None:
    babase.app.config[_SCREENMSG_CFG_KEY] = val
    babase.app.config.apply_and_commit()

_CFG_KEY = 'dm_auth'
_ACCOUNTS_KEY = 'dm_accounts'
_DM_TARGET_KEY = 'dm_chat_target'
_INVITE_BLOCK_KEY = 'dm_invite_block'
_INVITE_BLOCK_DEFAULT_MINUTES = 5
_INVITE_BLOCK_MAX_MINUTES = 300
_lock = threading.Lock()
_refresh_timer: Optional[threading.Timer] = None
_REFRESH_INTERVAL = 14 * 60  # access token lasts 15 min, refresh every 14

_refresh_lock = threading.Lock()
_last_refresh_time: float = 0.0
_MIN_REFRESH_GAP = 5 * 60  # max one token rotation per 5 minutes


def get_session() -> dict:
    return babase.app.config.get(_CFG_KEY, {})


def get_dm_chat_target() -> Optional[dict]:
    """Return the last DM chat target for the active account, or None."""
    uid = _get_my_user_id()
    if uid is None:
        return None
    return babase.app.config.get(_DM_TARGET_KEY, {}).get(uid)


def set_dm_chat_target(target: Optional[dict]) -> None:
    """Save the DM chat target for the active account."""
    uid = _get_my_user_id()
    if uid is None:
        return
    targets = dict(babase.app.config.get(_DM_TARGET_KEY, {}))
    if target is None:
        targets.pop(uid, None)
    else:
        targets[uid] = target
    babase.app.config[_DM_TARGET_KEY] = targets
    babase.app.config.apply_and_commit()


def get_invite_block(nickname: str) -> Optional[dict]:
    """Return active block info for nickname, or None if not blocked/expired."""
    blocks = babase.app.config.get(_INVITE_BLOCK_KEY, {})
    block = blocks.get(nickname)
    if not block:
        return None
    try:
        until = datetime.fromisoformat(block['until'])
        if datetime.now(timezone.utc) < until:
            return block
        # expired: clean up
        new_blocks = {k: v for k, v in blocks.items() if k != nickname}
        babase.app.config[_INVITE_BLOCK_KEY] = new_blocks
        babase.app.config.apply_and_commit()
        return None
    except Exception:
        return None


def set_invite_block(nickname: str, minutes: int) -> None:
    """Block invites from nickname for the given number of minutes."""
    from datetime import timedelta
    minutes = max(1, min(minutes, _INVITE_BLOCK_MAX_MINUTES))
    blocks = dict(babase.app.config.get(_INVITE_BLOCK_KEY, {}))
    until = (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat()
    blocks[nickname] = {'until': until, 'minutes': minutes}
    babase.app.config[_INVITE_BLOCK_KEY] = blocks
    babase.app.config.apply_and_commit()


def clear_invite_block(nickname: str) -> None:
    """Remove invite block for nickname."""
    blocks = dict(babase.app.config.get(_INVITE_BLOCK_KEY, {}))
    if nickname in blocks:
        del blocks[nickname]
        babase.app.config[_INVITE_BLOCK_KEY] = blocks
        babase.app.config.apply_and_commit()


def is_invite_blocked(nickname: str) -> bool:
    """Return True if invites from nickname are currently blocked."""
    return get_invite_block(nickname) is not None


def get_access_token() -> Optional[str]:
    return get_session().get('accessToken')


def get_refresh_token() -> Optional[str]:
    return get_session().get('refreshToken')


def is_logged_in() -> bool:
    return bool(get_access_token())


def get_accounts_list() -> list:
    """Returns list of locally saved accounts [{user, refreshToken}]."""
    return list(babase.app.config.get(_ACCOUNTS_KEY, []))


def _save_accounts_list(accounts: list) -> None:
    babase.app.config[_ACCOUNTS_KEY] = accounts
    babase.app.config.apply_and_commit()


def remove_account_from_list(user_id: int) -> None:
    """Remove account from local list. If it's the active account, also logs out."""
    accounts = [a for a in get_accounts_list() if a.get('user', {}).get('id') != user_id]
    _save_accounts_list(accounts)
    if get_session().get('user', {}).get('id') == user_id:
        full_logout()


def _apply_session_to_config(data: dict) -> None:
    """Write session and accounts to config in-memory (no disk commit)."""
    config = babase.app.config
    user = data.get('user', get_session().get('user', {}))
    rt = data.get('refreshToken', '')
    config[_CFG_KEY] = {
        'accessToken': data.get('accessToken', ''),
        'refreshToken': rt,
        'user': user,
    }
    if user.get('id') and rt:
        uid = user.get('id')
        accounts = list(config.get(_ACCOUNTS_KEY, []))
        for i, acc in enumerate(accounts):
            if acc.get('user', {}).get('id') == uid:
                accounts[i] = {'user': user, 'refreshToken': rt}
                break
        else:
            accounts.append({'user': user, 'refreshToken': rt})
        config[_ACCOUNTS_KEY] = accounts


def save_session(data: dict) -> None:
    _apply_session_to_config(data)
    babase.app.config.apply_and_commit()


def patch_session_user(fields: dict) -> None:
    """Update specific fields of the current session user in-memory and on disk."""
    session = get_session()
    user = {**session.get('user', {}), **fields}
    save_session({**session, 'user': user})


def clear_session() -> None:
    config = babase.app.config
    config.pop(_CFG_KEY, None)
    config.apply_and_commit()


_UA = 'Mozilla/5.0 (compatible)'


def _raw_request(
    method: str,
    path: str,
    body: Optional[dict] = None,
    extra_headers: Optional[dict] = None,
) -> tuple[Union[dict, list], int]:
    """Make an HTTP request"""
    url = f'{BASE_URL}{path}'
    data = json.dumps(body).encode('utf-8') if body is not None else None
    headers: dict = {'User-Agent': _UA}
    if data is not None:
        headers['Content-Type'] = 'application/json'
    token = get_access_token()
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if extra_headers:
        headers.update(extra_headers)

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode('utf-8')
            return (json.loads(raw) if raw.strip() else {}), resp.status
    except urllib.error.HTTPError as e:
        err_body: dict = {}
        try:
            err_body = json.loads(e.read().decode('utf-8'))
        except Exception:
            pass
        return err_body, e.code
    except Exception as exc:
        return {'error': str(exc)}, 0


def _do_refresh_request(rt: str) -> tuple[dict, int]:
    """Raw HTTP call to /auth/refresh. Returns (body, status)."""
    data = json.dumps({'refreshToken': rt}).encode('utf-8')
    req = urllib.request.Request(
        f'{BASE_URL}/auth/refresh',
        data=data,
        headers={'Content-Type': 'application/json', 'User-Agent': _UA},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8')), resp.status
    except urllib.error.HTTPError as e:
        return {}, e.code
    except Exception:
        return {}, 0


def full_logout() -> None:
    """Stop all sessions and clear stored tokens. Keeps accounts list intact."""
    global _friends_session, _global_session, _last_refresh_time
    _online_friend_ids.clear()
    global _pending_request_count
    _pending_request_count = 0
    stop_keep_alive()
    _last_refresh_time = 0.0
    fs, gs = _friends_session, _global_session
    _friends_session = None
    _global_session = None
    if fs is not None:
        fs.stop()
    if gs is not None:
        gs.stop()
    clear_session()


def _on_session_expired() -> None:
    """Refresh token is invalid. Clear tokens in-memory immediately, then push full cleanup to main thread."""
    # Wipe tokens from memory now so retry attempts in bg threads abort
    babase.app.config.pop(_CFG_KEY, None)

    def _cleanup() -> None:
        full_logout()
        try:
            import bauiv1 as bui
            bui.screenmessage('DM: session expired, please log in again.', color=(1.0, 0.4, 0.2))
        except Exception:
            pass

    babase.pushcall(_cleanup, from_other_thread=True)


def _try_refresh_sync(force: bool = False) -> bool:
    """Refresh the access token. Returns True if token is/was valid.

    Uses a lock to prevent concurrent token rotation races.
    Throttled to once per _MIN_REFRESH_GAP unless force=True.
    On 401 from server, calls _on_session_expired to clean up.
    """
    global _last_refresh_time
    with _refresh_lock:
        if not force and time.time() - _last_refresh_time < _MIN_REFRESH_GAP:
            return bool(get_access_token())
        rt = get_refresh_token()
        if not rt:
            return False
        body, status = _do_refresh_request(rt)
        if status == 200:
            # Write tokens to memory now; persist to disk on main thread
            _apply_session_to_config(body)
            babase.pushcall(babase.app.config.apply_and_commit, from_other_thread=True)
            _last_refresh_time = time.time()
            return True
        elif status == 401:
            _on_session_expired()
            return False
        else:
            return False


def _with_refresh(
    method: str,
    path: str,
    body: Optional[dict] = None,
) -> tuple[Union[dict, list], int]:
    """Make a request and retry once after refreshing if 401 is returned."""
    resp, status = _raw_request(method, path, body)
    if status == 401:
        if _try_refresh_sync():
            resp, status = _raw_request(method, path, body)
    return resp, status


def authenticated_get(path: str) -> tuple[Union[dict, list], int]:
    return _with_refresh('GET', path)


def authenticated_post(path: str, body: Optional[dict] = None) -> tuple[Union[dict, list], int]:
    return _with_refresh('POST', path, body)


def authenticated_put(path: str, body: Optional[dict] = None) -> tuple[Union[dict, list], int]:
    return _with_refresh('PUT', path, body)


def authenticated_delete(path: str, payload: Optional[dict] = None) -> tuple[Union[dict, list], int]:
    return _with_refresh('DELETE', path, payload)


def sync_my_role() -> None:
    """Fetch /auth/me and update session role if it changed. Call from a background thread."""
    body, status = authenticated_get('/auth/me')
    if status != 200 or not isinstance(body, dict):
        return
    new_role = body.get('role')
    if not new_role:
        return
    current_role = get_session().get('user', {}).get('role')
    if new_role != current_role:
        babase.pushcall(
            lambda: patch_session_user({'role': new_role}),
            from_other_thread=True,
        )


def _keep_alive_tick() -> None:
    if get_refresh_token():
        _try_refresh_sync()
    if get_refresh_token():
        _schedule_keep_alive()


def _schedule_keep_alive() -> None:
    global _refresh_timer
    with _lock:
        if _refresh_timer is not None:
            _refresh_timer.cancel()
        t = threading.Timer(_REFRESH_INTERVAL, _keep_alive_tick)
        t.daemon = True
        t.start()
        _refresh_timer = t


def start_keep_alive() -> None:
    """Start periodic token refresh. Call after successful login."""
    _schedule_keep_alive()


def stop_keep_alive() -> None:
    global _refresh_timer
    with _lock:
        if _refresh_timer is not None:
            _refresh_timer.cancel()
            _refresh_timer = None


def switch_to_account(
    account: dict,
    on_success=None,
    on_failure=None,
) -> None:
    """Switch active session to a different saved account. Runs in background thread."""
    global _friends_session, _global_session, _last_refresh_time
    rt = account.get('refreshToken', '')
    user = account.get('user', {})

    # Stop current sessions without touching accounts list
    stop_keep_alive()
    fs, gs = _friends_session, _global_session
    _friends_session = None
    _global_session = None
    if fs is not None:
        fs.stop()
    if gs is not None:
        gs.stop()
    clear_session()

    def _run() -> None:
        body, status = _do_refresh_request(rt)
        if status == 200:
            body.setdefault('user', user)

            def _apply() -> None:
                global _last_refresh_time
                save_session(body)
                _last_refresh_time = time.time()
                start_keep_alive()
                ensure_friends_session()
                if on_success:
                    on_success()

            babase.pushcall(_apply, from_other_thread=True)
        elif status == 401:
            def _expired() -> None:
                remove_account_from_list(user.get('id'))
                if on_failure:
                    on_failure('expired')

            babase.pushcall(_expired, from_other_thread=True)
        else:
            if on_failure:
                babase.pushcall(lambda: on_failure('network'), from_other_thread=True)

    threading.Thread(target=_run, daemon=True).start()


def _sio_poll_get(base: str, qs: str, timeout: float = 10.0) -> str:
    req = urllib.request.Request(
        f'{base}/socket.io/?{qs}',
        headers={'User-Agent': _UA},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8')


def _sio_poll_post(base: str, qs: str, body: str) -> None:
    data = body.encode('utf-8')
    req = urllib.request.Request(
        f'{base}/socket.io/?{qs}',
        data=data,
        headers={'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': _UA},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        r.read()


class GlobalChatSession:
    """Singleton Socket.IO session for global chat with persistent cache."""

    def __init__(self) -> None:
        self._sid: Optional[str] = None
        self._active = False
        self._ping_interval = 25.0
        self._cache: list[dict] = []
        self._listeners: list = []

    def start(self) -> None:
        self._active = True
        threading.Thread(target=self._load_then_run, daemon=True).start()

    def stop(self) -> None:
        self._active = False

    def send(self, content: str) -> bool:
        if not self._sid:
            return False
        try:
            qs = f'EIO=4&transport=polling&sid={self._sid}'
            payload = json.dumps(['global:send', {'content': content}])
            _sio_poll_post(BASE_URL, qs, f'42/global,{payload}')
            return True
        except Exception:
            return False

    def get_cache(self) -> list[dict]:
        return list(self._cache)

    def add_listener(self, cb) -> None:
        if cb not in self._listeners:
            self._listeners.append(cb)

    def remove_listener(self, cb) -> None:
        try:
            self._listeners.remove(cb)
        except ValueError:
            pass

    def _load_then_run(self) -> None:
        # Use _with_refresh so an expired token gets renewed before connecting
        body, status = _with_refresh('GET', '/global-chat?limit=50')
        if status == 200 and isinstance(body, list):
            for msg in body:
                ts_str = msg.get('created_at', '')
                try:
                    fixed = ts_str.replace('Z', '+00:00').replace(' ', 'T')
                    if fixed and fixed[-3] in ('+', '-') and fixed[-2:].isdigit():
                        fixed += ':00'
                    ts = datetime.fromisoformat(fixed)
                    if ts < _SESSION_START:
                        continue
                except Exception:
                    pass
                self._cache.append(msg)
            cache_snapshot = list(self._cache)

            def _notify_initial() -> None:
                for cb in list(self._listeners):
                    try:
                        for m in cache_snapshot:
                            cb(m)
                    except Exception:
                        pass

            babase.pushcall(_notify_initial, from_other_thread=True)

        self._run_socket()

    def _run_socket(self) -> None:
        import time
        while self._active:
            try:
                self._connect_and_poll()
            except Exception:
                if self._active:
                    time.sleep(3)

    def _connect_and_poll(self) -> None:
        # Refresh token before connecting to avoid immediate 44 Unauthorized
        _try_refresh_sync()
        token = get_access_token()
        if not token:
            return

        raw = _sio_poll_get(BASE_URL, 'EIO=4&transport=polling')
        handshake = json.loads(raw[1:] if raw and raw[0] == '0' else raw)
        self._sid = handshake['sid']
        self._ping_interval = handshake.get('pingInterval', 25000) / 1000
        qs = f'EIO=4&transport=polling&sid={self._sid}'

        auth = json.dumps({'token': f'Bearer {token}'})
        _sio_poll_post(BASE_URL, qs, f'40/global,{auth}')

        poll_timeout = self._ping_interval + 20
        while self._active:
            raw = _sio_poll_get(BASE_URL, qs, timeout=poll_timeout)
            self._handle_packets(raw)

    def _handle_packets(self, raw: str) -> None:
        for pkt in raw.split('\x1e'):
            if not pkt:
                continue
            if pkt[0] == '1':
                raise RuntimeError('Server closed connection')
            if pkt[0] == '2':
                try:
                    qs = f'EIO=4&transport=polling&sid={self._sid}'
                    _sio_poll_post(BASE_URL, qs, '3')
                except Exception:
                    pass
            elif pkt.startswith('44/global,'):
                print(f'[DM] Auth error: {pkt}')
                refreshed = _try_refresh_sync(force=True)
                if refreshed or get_access_token():
                    raise RuntimeError('Token refreshed, reconnecting')
                return  # _on_session_expired already cleaned up and notified
            elif pkt.startswith('42/global,'):
                try:
                    data = json.loads(pkt[len('42/global,'):])
                    if isinstance(data, list) and data[0] == 'global:receive':
                        msg = data[1]
                        self._cache.append(msg)
                        if len(self._cache) > 200:
                            self._cache.pop(0)

                        def _dispatch(m=msg) -> None:
                            for cb in list(self._listeners):
                                try:
                                    cb(m)
                                except Exception:
                                    pass
                            if not _dm_window_open and get_screenmsg_enabled():
                                try:
                                    import bauiv1 as bui
                                    bui.screenmessage(
                                        f'{m.get("nickname","?")}: {m.get("content","")}',
                                        color=(0.4, 0.7, 1.0),
                                    )
                                except Exception:
                                    pass

                        babase.pushcall(_dispatch, from_other_thread=True)
                except Exception as e:
                    print(f'[DM] Packet parse error: {e}')


_global_session: Optional[GlobalChatSession] = None


def ensure_global_session() -> GlobalChatSession:
    """Return the singleton chat session, starting it if needed."""
    global _global_session
    if _global_session is None:
        _global_session = GlobalChatSession()
        _global_session.start()
    return _global_session


class FriendsSession:
    """Socket.IO session for the /friends namespace (DMs, presence)."""

    def __init__(self) -> None:
        self._sid: Optional[str] = None
        self._active = False
        self._ping_interval = 25.0
        self._dm_listeners: dict = {}
        self._all_dm_listeners: list = []
        self._server_invite_listeners: list = []
        self._heartbeat_timer: Optional[threading.Timer] = None

    def start(self) -> None:
        self._active = True
        threading.Thread(target=self._run_socket, daemon=True).start()

    def stop(self) -> None:
        self._active = False
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()

    def send_server_invite(self, receiver_id: int, server_name: str, ip: str, port: str) -> bool:
        if not self._sid:
            return False
        try:
            qs = f'EIO=4&transport=polling&sid={self._sid}'
            payload = json.dumps(['server:info', {
                'receiverId': receiver_id,
                'serverName': server_name,
                'serverIp': ip,
                'serverPort': port,
            }])
            packet = f'42/friends,{payload}'
            _sio_poll_post(BASE_URL, qs, packet)
            return True
        except Exception as e:
            print(f'[DM] send_server_invite error: {e}')
            return False

    def send_dm(self, receiver_id: int, content: str, msg_id: str) -> bool:
        if not self._sid:
            return False
        try:
            qs = f'EIO=4&transport=polling&sid={self._sid}'
            payload = json.dumps(['chat:send', {
                'receiverId': receiver_id,
                'content': content,
                'messageId': msg_id,
            }])
            _sio_poll_post(BASE_URL, qs, f'42/friends,{payload}')
            return True
        except Exception as e:
            print(f'[DM] send_dm error: {e}')
            return False

    def add_dm_listener(self, friend_id: int, cb) -> None:
        listeners = self._dm_listeners.setdefault(friend_id, [])
        if cb not in listeners:
            listeners.append(cb)

    def remove_dm_listener(self, friend_id: int, cb) -> None:
        try:
            self._dm_listeners.get(friend_id, []).remove(cb)
        except ValueError:
            pass

    def add_all_dm_listener(self, cb) -> None:
        if cb not in self._all_dm_listeners:
            self._all_dm_listeners.append(cb)

    def remove_all_dm_listener(self, cb) -> None:
        try:
            self._all_dm_listeners.remove(cb)
        except ValueError:
            pass

    def add_server_invite_listener(self, cb) -> None:
        if cb not in self._server_invite_listeners:
            self._server_invite_listeners.append(cb)

    def remove_server_invite_listener(self, cb) -> None:
        try:
            self._server_invite_listeners.remove(cb)
        except ValueError:
            pass

    def _send_heartbeat(self) -> None:
        if self._sid and self._active:
            try:
                qs = f'EIO=4&transport=polling&sid={self._sid}'
                _sio_poll_post(BASE_URL, qs, '42/friends,["heartbeat"]')
            except Exception:
                pass
        self._schedule_heartbeat()

    def _schedule_heartbeat(self) -> None:
        if not self._active:
            return
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()
        t = threading.Timer(30.0, self._send_heartbeat)
        t.daemon = True
        t.start()
        self._heartbeat_timer = t

    def _run_socket(self) -> None:
        import time
        while self._active:
            try:
                self._connect_and_poll()
            except Exception:
                if self._active:
                    time.sleep(3)

    def _connect_and_poll(self) -> None:
        import time
        _try_refresh_sync()
        token = get_access_token()
        if not token:
            time.sleep(5)
            return

        raw = _sio_poll_get(BASE_URL, 'EIO=4&transport=polling')
        handshake = json.loads(raw[1:] if raw and raw[0] == '0' else raw)
        self._sid = handshake['sid']
        self._ping_interval = handshake.get('pingInterval', 25000) / 1000
        qs = f'EIO=4&transport=polling&sid={self._sid}'

        auth = json.dumps({'token': f'Bearer {token}'})
        _sio_poll_post(BASE_URL, qs, f'40/friends,{auth}')
        self._schedule_heartbeat()
        # Request initial list of online friends (ack ID 1)
        _sio_poll_post(BASE_URL, qs, '42/friends,1["getOnlineFriends"]')

        poll_timeout = self._ping_interval + 20
        while self._active:
            raw = _sio_poll_get(BASE_URL, qs, timeout=poll_timeout)
            self._handle_packets(raw)

    def _handle_packets(self, raw: str) -> None:
        for pkt in raw.split('\x1e'):
            if not pkt:
                continue
            if pkt[0] == '1':
                raise RuntimeError('Server closed connection')
            if pkt[0] == '2':
                try:
                    qs = f'EIO=4&transport=polling&sid={self._sid}'
                    _sio_poll_post(BASE_URL, qs, '3')
                except Exception:
                    pass
            elif pkt.startswith('44/friends,'):
                print(f'[DM] Friends auth error: {pkt}')
                if self._heartbeat_timer:
                    self._heartbeat_timer.cancel()
                    self._heartbeat_timer = None
                refreshed = _try_refresh_sync(force=True)
                if refreshed or get_access_token():
                    raise RuntimeError('Token refreshed, reconnecting /friends')
                return 
            elif pkt.startswith('43/friends,'):
                # Currently only used for getOnlineFriends
                try:
                    after_ns = pkt[len('43/friends,'):]
                    i = 0
                    while i < len(after_ns) and after_ns[i].isdigit():
                        i += 1
                    ack_payload = json.loads(after_ns[i:])
                    result = ack_payload[0] if isinstance(ack_payload, list) else ack_payload
                    if isinstance(result, dict) and 'onlineFriends' in result:
                        ids = {int(x) for x in result['onlineFriends']}
                        _online_friend_ids.clear()
                        _online_friend_ids.update(ids)
                        babase.pushcall(_notify_online_status_listeners, from_other_thread=True)
                except Exception as e:
                    print(f'[DM] ACK parse error: {e}')
            elif pkt.startswith('42/friends,'):
                try:
                    data = json.loads(pkt[len('42/friends,'):])
                    if isinstance(data, list) and data[0] == 'chat:delivered':
                        pass
                    elif isinstance(data, list) and data[0] == 'chat:receive':
                        msg = data[1]
                        sender_id = msg.get('senderId')

                        def _dispatch(m=msg, sid=sender_id) -> None:
                            for cb in list(self._all_dm_listeners):
                                try:
                                    cb(m)
                                except Exception as e:
                                    print(f'[DM] all_dm_listener error: {e}')
                            for cb in list(self._dm_listeners.get(sid, [])):
                                try:
                                    cb(m)
                                except Exception:
                                    pass

                        babase.pushcall(_dispatch, from_other_thread=True)
                    elif isinstance(data, list) and data[0] == 'server:info':
                        invite = data[1]

                        def _dispatch_invite(inv=invite) -> None:
                            for cb in list(self._server_invite_listeners):
                                try:
                                    cb(inv)
                                except Exception as e:
                                    print(f'[DM] server invite cb error: {e}')

                        babase.pushcall(_dispatch_invite, from_other_thread=True)
                    elif isinstance(data, list) and data[0] == 'friendRequest':
                        req_info = data[1] if len(data) > 1 else {}
                        sender_nick = req_info.get('senderNickname', '?')
                        babase.pushcall(
                            lambda n=sender_nick: _on_friend_request_received(n),
                            from_other_thread=True,
                        )
                    elif isinstance(data, list) and data[0] == 'friendOnlineStatus':
                        status_info = data[1] if len(data) > 1 else {}
                        uid = status_info.get('userId')
                        is_online = status_info.get('isOnline')
                        if uid is not None and is_online is not None:
                            if is_online:
                                _online_friend_ids.add(int(uid))
                            else:
                                _online_friend_ids.discard(int(uid))
                            babase.pushcall(_notify_online_status_listeners, from_other_thread=True)
                except Exception as e:
                    print(f'[DM] Friends packet parse error: {e}')


_friends_session: Optional[FriendsSession] = None


def _on_global_dm_receive(msg: dict) -> None:
    """Saves every incoming DM and shows screenmessage when DM window is closed."""
    sender_id = msg.get('senderId')
    sender_name = msg.get('senderName') or msg.get('senderNickname', '?')
    sender_nick = msg.get('senderNickname', '?')
    content = msg.get('content', '')

    if sender_id is not None:
        try:
            append_dm_message(sender_id, sender_nick, sender_id, sender_nick, content)
        except Exception as e:
            print(f'[DM] global dm save error: {e}')
        # Only count as unread if the user is not currently viewing this chat
        chat_is_open = _dm_window_open and _active_dm_chat_friend_id == sender_id
        if not chat_is_open:
            try:
                increment_unread_dm_count(sender_id)
            except Exception as e:
                print(f'[DM] unread increment error: {e}')

    if not chat_is_open:
        try:
            babase.screenmessage(f'{sender_name}: {content}', color=(0.5, 0.8, 1.0))
        except Exception as e:
            print(f'[DM] global dm screenmessage error: {e}')


def _on_global_server_invite(invite: dict) -> None:
    """Show ServerInvitePopup over the overlay stack regardless of DM window state."""
    sender = invite.get('senderNickname', '?')
    if is_invite_blocked(sender):
        return
    try:
        import bauiv1 as bui
        ServerInvitePopup(invite=invite)
    except Exception as e:
        print(f'[DM] Could not show server invite popup: {e}')


def ensure_friends_session() -> FriendsSession:
    """Return the singleton friends session, starting it if needed."""
    global _friends_session
    if _friends_session is None:
        _friends_session = FriendsSession()
        _friends_session.start()
        _friends_session.add_all_dm_listener(_on_global_dm_receive)
        _friends_session.add_server_invite_listener(_on_global_server_invite)
    return _friends_session


def _ensure_remote_dir() -> None:
    if not os.path.exists(REMOTE_DIRECTORY):
        os.makedirs(REMOTE_DIRECTORY)


def _get_my_user_id() -> Optional[str]:
    """Returns the active account's user ID as string, or None if not logged in."""
    uid = get_session().get('user', {}).get('id')
    return str(uid) if uid is not None else None


def _load_all_dm_msgs() -> dict:
    """Load the full msgs file. Migrates old single-user format automatically."""
    try:
        _ensure_remote_dir()
        if not os.path.exists(DM_MSGS_FILE):
            return {}
        with open(DM_MSGS_FILE, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        if not raw:
            return {}
        first = next(iter(raw.values()))
        if isinstance(first, dict) and 'messages' in first:
            accounts = get_accounts_list()
            if len(accounts) == 1:
                uid = str(accounts[0].get('user', {}).get('id', ''))
                if uid:
                    migrated = {uid: raw}
                    with open(DM_MSGS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(migrated, f, indent=1, ensure_ascii=False)
                    return migrated
            return {}
        return raw
    except Exception as e:
        print(f'[DM] _load_all_dm_msgs error: {e}')
    return {}


def load_dm_msgs() -> dict:
    """Return DM conversations for the active account, keyed by friend_id (str)."""
    uid = _get_my_user_id()
    if uid is None:
        return {}
    return _load_all_dm_msgs().get(uid, {})


def _save_dm_msgs(data: dict) -> None:
    uid = _get_my_user_id()
    if uid is None:
        return
    try:
        _ensure_remote_dir()
        all_data = _load_all_dm_msgs()
        all_data[uid] = data
        with open(DM_MSGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=1, ensure_ascii=False)
    except Exception as e:
        print(f'[DM] _save_dm_msgs error: {e}')


def get_conversation_msgs(friend_id: int) -> list:
    """Return stored messages with a friend for the active account."""
    return load_dm_msgs().get(str(friend_id), {}).get('messages', [])


def append_dm_message(friend_id: int, friend_nickname: str,
                      sender_id: int, sender_nick: str, content: str) -> None:
    """Append a message to the active account's conversation with friend_id."""
    data = load_dm_msgs()
    key = str(friend_id)
    if key not in data:
        data[key] = {'nickname': friend_nickname, 'messages': []}
    else:
        data[key]['nickname'] = friend_nickname
    data[key]['messages'].append({
        'sender_id': sender_id,
        'nickname': sender_nick,
        'content': content,
        'ts': datetime.now(timezone.utc).isoformat(),
    })
    _save_dm_msgs(data)


def try_auto_login() -> None:
    """Try to restore session using stored refresh token. Runs in a background thread."""
    if not get_refresh_token():
        return

    def _run() -> None:
        ok = _try_refresh_sync()
        if ok:
            start_keep_alive()
            ensure_friends_session()
            nick = get_session().get('user', {}).get('nickname', '')

            def _notify() -> None:
                try:
                    import bauiv1 as bui
                    if nick:
                        bui.screenmessage(f'Welcome back, {nick}!', color=(0, 0.8, 0.5))
                except Exception:
                    pass

            babase.pushcall(_notify, from_other_thread=True)

    threading.Thread(target=_run, daemon=True).start()


# Log
log_uiscale('party_module_load')
_uiscale_start_monitor()
_roster_start_monitor()
_chat_start_monitor()
try_auto_login()


class _ChatColorTracker:
    """Assigns a consistent random color to each chat sender."""

    def __init__(self) -> None:
        self._saved: dict[str, tuple[float, float, float]] = {}

    def _generate(self, sender: str) -> None:
        while True:
            color = (random.random(), random.random(), random.random())
            # Ensure enough contrast
            if sum(c * c for c in color) > 0.15:
                self._saved[sender] = color
                if len(self._saved) > 30:
                    self._saved.pop(next(iter(self._saved)))
                break

    def get(self, sender: str) -> tuple[float, float, float] | None:
        if sender not in self._saved:
            Thread(target=self._generate, args=(sender,), daemon=True).start()
            return None
        return self._saved[sender]


_chat_color_tracker = _ChatColorTracker()

# Weak reference to the active party window
_active_party_window_ref: '_weakref.ref[LPartyWindow] | None' = None


def get_active_party_window() -> 'LPartyWindow | None':
    return _active_party_window_ref() if _active_party_window_ref is not None else None


def insert_into_chat_field(text: str) -> None:
    """Insert text into the party window chat field if it's open."""
    w = _active_party_window_ref() if _active_party_window_ref is not None else None
    if w is None:
        return
    try:
        if w._text_field and w._text_field.exists():
            bui.textwidget(edit=w._text_field, text=text)
    except Exception:
        pass


def _log_active_accounts() -> None:
    plus = babase.app.plus
    game_name = ''
    if plus is not None:
        try:
            game_name = plus.get_v1_account_display_string()
        except Exception:
            pass
    api_nick = get_session().get('user', {}).get('nickname', '') if is_server_online() else ''

    if not game_name and not api_nick:
        return

    if api_nick and game_name:
        msg = f'Logged in as {api_nick}! Welcome back, {game_name}!'
    elif api_nick:
        msg = f'Welcome back! Logged in as {api_nick}!'
    else:
        msg = f'Welcome back, {game_name}!'

    babase.screenmessage(msg, color=(0.5, 1.0, 0.7))


def _ping_and_log() -> None:
    import threading
    import urllib.request
    import urllib.error

    def _run() -> None:
        online = False
        try:
            with urllib.request.urlopen(f'{BASE_URL}/health', timeout=5) as resp:
                online = True
        except urllib.error.HTTPError as e:
            online = True
        except urllib.error.URLError:
            pass
        except Exception as e:
            pass

        set_server_online(online)
        babase.pushcall(_log_active_accounts, from_other_thread=True)

    threading.Thread(target=_run, daemon=True).start()


babase.apptimer(1.5, _ping_and_log)

# Icon prefixes
_SPECIAL_CHARS = [babase.charstr(i) for i in bui.SpecialChar]

_NICKNAME_MAX_LEN = 12


def _fmt_nickname(nick: str) -> str:
    """Return #Nickname, truncated with ... if over _NICKNAME_MAX_LEN."""
    if len(nick) > _NICKNAME_MAX_LEN:
        nick = nick[:_NICKNAME_MAX_LEN] + '...'
    return f'#{nick}'


def _normalize_account_name(name: str) -> str:
    if name and name[0] in _SPECIAL_CHARS:
        return name
    return V2_LOGO + name if name else name


def _ping_color(ms: float) -> tuple[float, float, float]:
    if ms < 100:
        return (0.0, 1.0, 0.0)
    if ms < 900:
        return (1.0, 1.0, 0.0)
    return (1.0, 0.0, 0.0)


class _ThemedPopupMenu(PopupMenuWindow):
    """PopupMenuWindow with custom bg and text colors."""

    def __init__(
        self,
        *args,
        bg_color: tuple,
        text_color: tuple,
        scroll_color: tuple | None = None,
        scroll_threshold: int | None = None,
        scroll_height_offset: int = 0,
        **kwargs,
    ):
        import builtins as _builtins

        _orig_tw = bui.textwidget
        _text_widgets: list[bui.Widget] = []

        def _intercept_tw(*a, **kw):
            result = _orig_tw(*a, **kw)
            if kw.get('parent') is not None and 'size' in kw:
                _text_widgets.append(result)
            return result

        # Temporarily patch len to force scroll when choices exceed scroll_threshold
        _orig_len = None
        _choices_ref = kwargs.get('choices') or (args[1] if len(args) > 1 else None)
        if scroll_threshold is not None and _choices_ref is not None and _builtins.len(_choices_ref) > scroll_threshold:
            _orig_len = _builtins.len
            def _patched_len(x: object) -> int:
                if x is _choices_ref:
                    return 9  # exceeds the internal threshold of 8
                return _orig_len(x)  # type: ignore[misc]
            _builtins.len = _patched_len  # type: ignore[assignment]

        try:
            bui.textwidget = _intercept_tw
            super().__init__(*args, **kwargs)
            bui.textwidget = _orig_tw
        finally:
            if _orig_len is not None:
                _builtins.len = _orig_len

        bui.containerwidget(edit=self.root_widget, color=bg_color)
        for w in _text_widgets:
            if w.exists():
                bui.textwidget(edit=w, color=text_color)

        if hasattr(self, '_scrollwidget') and self._scrollwidget.exists():
            sw_kw: dict = {}
            if scroll_color:
                sw_kw['color'] = scroll_color
            if scroll_height_offset:
                sw_kw['size'] = (self._width - 40, self._height - 40 - scroll_height_offset)
            if sw_kw:
                bui.scrollwidget(edit=self._scrollwidget, **sw_kw)


_CFG_ROSTER_HIDDEN = 'lparty.roster_hidden'
_CFG_CHAT_MUTED = 'lparty.chat_muted'


class LPartyWindow(party.PartyWindow):

    def __init__(self, origin: Sequence[float] = (0, 0)) -> None:
        log_uiscale('party_window_open')
        self._roster_show_account: bool = False
        self._chat_raw_msgs: list[str] = []
        self._chat_senders: list[str | None] = []
        self._in_game: bool = False
        self._roster_hidden: bool = False
        _bg = _global_theme.get_color('COLOR_BACKGROUND')
        _orig_bw = bui.buttonwidget
        _orig_cw = bui.containerwidget
        _send_ref: list[bui.Widget] = []
        _menu_ref: list[bui.Widget] = []
        _root_created = [False]

        def _intercept_bw(*args, **kwargs):
            result = _orig_bw(*args, **kwargs)
            widget_id = str(kwargs.get('id', ''))
            if widget_id.endswith('|send'):
                _send_ref.append(result)
            elif widget_id.endswith('|menu'):
                _menu_ref.append(result)
            return result

        def _intercept_cw(*args, **kwargs):
            # inject lparty bg color
            if not _root_created[0] and 'edit' not in kwargs:
                _root_created[0] = True
                kwargs['color'] = _bg
            return _orig_cw(*args, **kwargs)

        bui.buttonwidget = _intercept_bw
        bui.containerwidget = _intercept_cw
        super().__init__(origin)
        bui.buttonwidget = _orig_bw
        bui.containerwidget = _orig_cw

        global _active_party_window_ref
        _active_party_window_ref = _weakref.ref(self)

        load_finder_config()
        load_friends()
        load_blacklist()
        load_playerinfo()

        theme = _global_theme
        self.bg_color = theme.get_color('COLOR_SECONDARY')
        self.title_color = theme.get_color('COLOR_PRIMARY')
        self.subtitle_color = theme.get_color('COLOR_SECONDARY')
        self.text_color = theme.get_color('COLOR_TERTIARY')
        color_background = theme.get_color('COLOR_BACKGROUND')
        self.background_color = color_background
        self.button_color = theme.get_color('COLOR_BUTTON')
        bui.scrollwidget(edit=self._scrollwidget, color=theme.get_color('COLOR_ACCENT'))
        language = _global_language
        is_small = bui.app.ui_v1.uiscale is bui.UIScale.SMALL
        send_size = (40, 40)

        if _send_ref:
            self._send_button = _send_ref[0]
            bui.buttonwidget(
                edit=self._send_button,
                label='',
                texture=bui.gettexture('rightButton'),
                size=(send_size),
                color=(1, 1, 1),
                position=(self._width - 80, 35),
            )

        if _menu_ref:
            self._menu_button = _menu_ref[0]
            bui.buttonwidget(edit=self._menu_button, color=self.button_color,
                             textcolor=self.title_color)

        bui.buttonwidget(edit=self._cancel_button, color=self.button_color,
                         textcolor=self.title_color)

        bui.textwidget(
            edit=self._title_text,
            color=self.title_color,
            text=language.get_text('PartyWindow.title'),
        )
        # keep stock _muted_text
        bui.textwidget(edit=self._muted_text, color=(0, 0, 0, 0))

        is_muted = babase.app.config.get(_CFG_CHAT_MUTED, False)
        self._lparty_muted_text = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            color=theme.get_color('COLOR_SECONDARY') if is_muted else (0, 0, 0, 0),
            text=language.get_text('PartyWindow.chatMuted'),
        )
        bui.textwidget(
            edit=self._empty_str,
            color=self.subtitle_color,
            text=language.get_text('PartyWindow.emptyStr'),
        )
        bui.textwidget(
            edit=self._empty_str_2,
            color=self.text_color,
            text=language.get_text('PartyWindow.emptyStr2'),
        )

        if is_small:
            bui.buttonwidget(edit=self._cancel_button, scale=0.55,
                             position=(30, self._height - 25))
            bui.buttonwidget(edit=self._menu_button, scale=0.55,
                             position=(self._width - 40, self._height - 25))
            bui.textwidget(edit=self._title_text, scale=0.75,
                           position=(self._width * 0.5, self._height - 11))
            bui.textwidget(edit=self._empty_str,
                           position=(self._width * 0.5, self._height - 35))
            bui.textwidget(edit=self._empty_str_2,
                           position=(self._width * 0.5, self._height - 53))
        else:
            bui.buttonwidget(edit=self._menu_button,
                             position=(self._width - 45, self._height - 47))
            bui.textwidget(edit=self._title_text, scale=1.05,
                           position=(self._width * 0.5, self._height - 24))
            bui.textwidget(edit=self._empty_str,
                           position=(self._width * 0.5, self._height - 52))
            bui.textwidget(edit=self._empty_str_2,
                           position=(self._width * 0.5, self._height - 70))

        assert bui.app.classic is not None
        self.uiscale = bui.app.ui_v1.uiscale

        bui.containerwidget(
            edit=self._root_widget,
            scale=(
                1.8 if self.uiscale is bui.UIScale.SMALL else
                1.3 if self.uiscale is bui.UIScale.MEDIUM else 1.0
            ),
            stack_offset=(
                (0.0, -12.5) if self.uiscale is bui.UIScale.SMALL else
                (210, -7.5) if self.uiscale is bui.UIScale.MEDIUM else
                (295, -10)
            ),
        )

        _uiscale_subscribe(self._on_uiscale_change)

        is_small = self.uiscale is bui.UIScale.SMALL
        is_medium = self.uiscale is bui.UIScale.MEDIUM
        btn_scale = 0.65 if is_small else (0.84 if is_medium else 1.2)
        btn_spacing = 25 if is_small else (32 if is_medium else 45)
        btn_x_offset = 8 if is_small else 10
        settings_scale = 0.55 if is_small else (0.6 if is_medium else 0.7)
        icon_btn_size = (30, 30)
        trans_scale = 1.0 if is_small else btn_scale
        trans_x = self._width - 35
        trans_y = 38 if is_small else 35

        button_start_y = self._height // 2 + btn_spacing * 2

        self._chat_view_button = bui.buttonwidget(
            parent=self._root_widget,
            size=icon_btn_size,
            scale=btn_scale,
            label='',
            button_type='square',
            color=self.button_color,
            position=(self._width - btn_x_offset + 2, button_start_y + btn_spacing),
            icon=bui.gettexture('usersButton'),
            iconscale=1.2,
            on_activate_call=self._on_chat_view_button_press,
        )

        self.finder_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 30),
            scale=btn_scale,
            label=language.get_text('Global.search'),
            button_type='square',
            color=self.button_color,
            textcolor=self.text_color,
            position=(self._width - btn_x_offset, button_start_y),
            on_activate_call=lambda: FinderWindow(self.finder_button, party_window=self)
        )

        self.button2 = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 30),
            scale=btn_scale,
            label=get_lang_text('Button.chats'),
            button_type='square',
            color=self.button_color,
            textcolor=self.text_color,
            position=(self._width - btn_x_offset, button_start_y - btn_spacing),
            on_activate_call=lambda: DMWindow()
        )

        _btn2_x = self._width - btn_x_offset
        _btn2_y = button_start_y - btn_spacing
        _is_small = self.uiscale is babase.UIScale.SMALL
        _is_medium = self.uiscale is babase.UIScale.MEDIUM
        _dm_badge_size = int(24 * 0.5) if _is_small else (int(24 * 0.7) if _is_medium else 24)
        _dm_badge_cx = (_btn2_x + 65 - 30) if _is_small else ((_btn2_x + 65 - 13) if _is_medium else (_btn2_x + 65))
        _dm_badge_cy = (_btn2_y + 35 + 10 - 27) if _is_small else ((_btn2_y + 35 - 10) if _is_medium else (_btn2_y + 35))
        self._dm_badge_img = bui.imagewidget(
            parent=self._root_widget,
            position=(_dm_badge_cx - _dm_badge_size // 2, _dm_badge_cy - _dm_badge_size // 2),
            size=(_dm_badge_size, _dm_badge_size),
            texture=bui.gettexture('circle'),
            color=(0.9, 0.1, 0.1),
            opacity=0.0,
        )
        self._dm_badge_num = bui.textwidget(
            parent=self._root_widget,
            position=(_dm_badge_cx, _dm_badge_cy),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='',
            scale=0.55 * 0.5 if _is_small else (0.55 * 0.7 if _is_medium else 0.55),
            color=(1.0, 1.0, 1.0),
        )
        add_unread_dm_listener(self._update_dm_badge)
        self._update_dm_badge()

        self.button3 = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 30),
            scale=btn_scale,
            label=get_lang_text('Button.friends'),
            button_type='square',
            color=self.button_color,
            textcolor=self.text_color,
            position=(self._width - btn_x_offset, button_start_y - btn_spacing * 2),
            on_activate_call=self._show_friends_popup,
        )

        _btn3_x = self._width - btn_x_offset
        _btn3_y = button_start_y - btn_spacing * 2
        _online_badge_size = int(24 * 0.5) if _is_small else (int(24 * 0.7) if _is_medium else 24)
        _online_badge_cx = (_btn3_x + 65 - 30) if _is_small else ((_btn3_x + 65 - 13) if _is_medium else (_btn3_x + 65))
        _online_badge_cy = (_btn3_y + 35 + 10 - 27) if _is_small else ((_btn3_y + 35 - 10) if _is_medium else (_btn3_y + 35))
        self._online_badge_img = bui.imagewidget(
            parent=self._root_widget,
            position=(_online_badge_cx - _online_badge_size // 2, _online_badge_cy - _online_badge_size // 2),
            size=(_online_badge_size, _online_badge_size),
            texture=bui.gettexture('circle'),
            color=(0.08, 0.75, 0.2),
            opacity=0.0,
        )
        self._online_badge_num = bui.textwidget(
            parent=self._root_widget,
            position=(_online_badge_cx, _online_badge_cy),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='',
            scale=0.55 * 0.5 if _is_small else (0.55 * 0.7 if _is_medium else 0.55),
            color=(1.0, 1.0, 1.0),
        )
        add_online_status_listener(self._update_online_badge)
        self._update_online_badge()

        self.button4 = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 30),
            scale=btn_scale,
            label=get_lang_text('Camera.button'),
            button_type='square',
            color=self.button_color,
            textcolor=self.text_color,
            position=(self._width - btn_x_offset, button_start_y - btn_spacing * 3),
            on_activate_call=self._show_camera_popup
        )

        self._icons_button = bui.buttonwidget(
            parent=self._root_widget,
            size=icon_btn_size,
            scale=btn_scale,
            label='',
            button_type='square',
            color=self.button_color,
            position=(self._width - btn_x_offset, button_start_y - btn_spacing * 4),
            icon=bui.gettexture('achievementsIcon'),
            iconscale=1.2,
            on_activate_call=self._show_icons_popup
        )

        self._translate_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(60, 30),
            scale=trans_scale,
            label=get_lang_text('Button.trans'),
            button_type='square',
            color=self.button_color,
            textcolor=self.text_color,
            position=(trans_x, trans_y),
            on_activate_call=self._on_translate_button_press
        )
        self._translate_button_armed: bool = False
        self._refreshing_chat: bool = False
        self._nav_idx: int = -1
        self._nav_prev_idx: int = -1
        self._nav_prev_widget: bui.Widget | None = None

        self._settings_button = bui.buttonwidget(
            parent=self._root_widget,
            size=(50, 50),
            scale=settings_scale,
            label='',
            button_type='square',
            autoselect=True,
            color=self.button_color,
            textcolor=self.title_color,
            position=(self._width - 10 if is_small else self._width - 10, self._height - 55 if is_small else (self._height - 81 if is_medium else self._height - 85)),
            icon=bui.gettexture('settingsIcon'),
            iconscale=1.2,
            on_activate_call=lambda: SettingsWindow(),
        )

        chat_nav_x = -11 if is_small else -7
        self._next_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(chat_nav_x, 16),
            size=(28, 28),
            label=babase.charstr(bui.SpecialChar.DOWN_ARROW),
            button_type='square',
            autoselect=False,
            repeat=True,
            color=self.button_color,
            textcolor=self.title_color,
            scale=1.0,
            on_activate_call=bui.CallStrict(self._next_message),
        )

        previous_btn_y = (
            self._height * 0.0425 * 3 + 8 if is_small else
            self._height * 0.0425 * 2.275 + 8 if is_medium else
            self._height * 0.0425 * 1.85 + 8
        )
        self._previous_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(chat_nav_x, previous_btn_y),
            size=(28, 28),
            label=babase.charstr(bui.SpecialChar.UP_ARROW),
            button_type='square',
            autoselect=False,
            repeat=True,
            color=self.button_color,
            textcolor=self.title_color,
            scale=1.0,
            on_activate_call=bui.CallStrict(self._previous_message),
        )

        nav_clear_y = (
            self._height * 0.075 + 8.5 if is_small else
            self._height * 0.0575 + 8.5 if is_medium else
            self._height * 0.055 + 8.5
        )
        self._nav_clear_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(chat_nav_x - 45, nav_clear_y),
            size=(28, 28),
            scale=1.0,
            label='',
            color=self.button_color,
            textcolor=self.title_color,
            on_activate_call=bui.CallStrict(self._on_nav_clear),
            autoselect=False,
            icon=bui.gettexture('replayIcon'),
            iconscale=1.1,
        )

        self._ping_button: bui.Widget | None = None
        self._icon_button: bui.Widget | None = None
        self._gather_button: bui.Widget | None = None
        self._ip_button: bui.Widget | None = None
        self._ping_ms: float = 0.0
        self._ping_running: bool = False
        self._window_open: bool = True
        self._last_recorded_server: str = ''

        self._party_check_timer = bui.AppTimer(
            1.0, bui.WeakCallStrict(self._check_party_state), repeat=True
        )
        self._check_party_state()

        self._subscribe_to_theme_changes(theme)
        self._subscribe_to_language_changes(language)

    def _check_party_state(self) -> None:
        roster = bs.get_game_roster()
        in_game = bool(roster)

        if in_game:
            server_info = bs.get_connection_to_host_info_2()
            game_name = (server_info.name if server_info and server_info.name else 'Party')
            if server_info and server_info.address:
                key = f'{server_info.address}:{server_info.port}'
                if key != self._last_recorded_server:
                    self._last_recorded_server = key
                    record_server(server_info.name or '', server_info.address, server_info.port)
                    # Restore or reset roster-hidden state for this server
                    cfg = bui.app.config.get(_CFG_ROSTER_HIDDEN, {})
                    self._roster_hidden = (
                        cfg.get('hidden', False) if cfg.get('server') == key else False
                    )

            title_txt = getattr(self, '_title_text', None)
            empty_str = getattr(self, '_empty_str', None)
            empty_str_2 = getattr(self, '_empty_str_2', None)
            if title_txt and title_txt.exists():
                bui.textwidget(edit=title_txt, text=game_name)
            if not self._in_game:
                if empty_str and empty_str.exists():
                    bui.textwidget(edit=empty_str, text='')
                if empty_str_2 and empty_str_2.exists():
                    bui.textwidget(edit=empty_str_2, text='')
                # Give title an actual size so it has a click area, and make it selectable
                if title_txt and title_txt.exists():
                    is_small = bui.app.ui_v1.uiscale is bui.UIScale.SMALL
                    _t_mw = self._scroll_width - 120
                    _t_cx = self._scroll_width * 0.5 + 35
                    _t_cy = self._height - 16 if is_small else self._height - 29
                    bui.textwidget(
                        edit=title_txt,
                        size=(_t_mw, 22),
                        position=(_t_cx - _t_mw * 0.5, _t_cy - 11),
                        maxwidth=_t_mw,
                        h_align='center',
                        selectable=True,
                        click_activate=True,
                        on_activate_call=bui.WeakCallStrict(self._on_title_click),
                    )
            self._in_game = True

            uiscale = bui.app.ui_v1.uiscale
            if uiscale is babase.UIScale.SMALL:
                _bs, _bsz, _gap, _bx, _by = 0.7, (37, 37), 31, -5, 60
            elif uiscale is babase.UIScale.MEDIUM:
                _bs, _bsz, _gap, _bx, _by = 0.8, (39, 39), 37, -15, 90
            else:
                _bs, _bsz, _gap, _bx, _by = 1.0, (45, 45), 53, -30, 105

            if self._ping_button is None or not self._ping_button.exists():
                self._ping_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(_bx, self._height - _by),
                    size=_bsz,
                    label='?',
                    scale=_bs,
                    button_type='square',
                    autoselect=False,
                    color=self.button_color,
                    text_scale=1.4,
                    enable_sound=False,
                    on_activate_call=self._send_ping_chat
                )

            self._do_ping()

            if self._icon_button is None or not self._icon_button.exists():
                self._icon_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(_bx, self._height - _by - _gap),
                    size=_bsz,
                    label='',
                    scale=_bs,
                    button_type='square',
                    autoselect=False,
                    color=self.button_color,
                    icon=bui.gettexture('achievementSharingIsCaring'),
                    enable_sound=False,
                    iconscale=1.2,
                    on_activate_call=self._toggle_name_display
                )

            if self._ip_button is None or not self._ip_button.exists():
                self._ip_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(_bx, self._height - _by - _gap * 2),
                    size=_bsz,
                    label='IP',
                    scale=_bs,
                    button_type='square',
                    autoselect=False,
                    color=self.button_color,
                    text_scale=1.2,
                    on_activate_call=self._ip_port_msg
                )

            if self._gather_button is None or not self._gather_button.exists():
                self._gather_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(_bx, self._height - _by - _gap * 3),
                    size=_bsz,
                    label='',
                    scale=_bs,
                    button_type='square',
                    autoselect=False,
                    color=self.button_color,
                    icon=bui.gettexture('controllerIcon'),
                    iconscale=1.2,
                    on_activate_call=self._open_gather
                )
        else:
            if self._ping_button is not None and self._ping_button.exists():
                self._ping_button.delete()
            self._ping_button = None

            if self._icon_button is not None and self._icon_button.exists():
                self._icon_button.delete()
            self._icon_button = None

            if self._ip_button is not None and self._ip_button.exists():
                self._ip_button.delete()
            self._ip_button = None

            if self._gather_button is not None and self._gather_button.exists():
                self._gather_button.delete()
            self._gather_button = None

            self._roster_show_account = False

            if self._in_game:
                language = _global_language
                title_txt = getattr(self, '_title_text', None)
                empty_str = getattr(self, '_empty_str', None)
                empty_str_2 = getattr(self, '_empty_str_2', None)
                _small = bui.app.ui_v1.uiscale is bui.UIScale.SMALL
                if title_txt and title_txt.exists():
                    bui.textwidget(
                        edit=title_txt,
                        text=language.get_text('PartyWindow.title'),
                        scale=0.75 if _small else 1.05,
                        size=(0, 0),
                        position=(
                            (self._width * 0.5, self._height - 11) if _small
                            else (self._width * 0.5, self._height - 24)
                        ),
                    )
                if empty_str and empty_str.exists():
                    bui.textwidget(
                        edit=empty_str,
                        text=language.get_text('PartyWindow.emptyStr'),
                        position=(
                            (self._width * 0.5, self._height - 35) if _small
                            else (self._width * 0.5, self._height - 52)
                        ),
                    )
                if empty_str_2 and empty_str_2.exists():
                    bui.textwidget(
                        edit=empty_str_2,
                        text=language.get_text('PartyWindow.emptyStr2'),
                        position=(
                            (self._width * 0.5, self._height - 53) if _small
                            else (self._width * 0.5, self._height - 70)
                        ),
                    )
            self._in_game = False

    def _update(self) -> None:
        if not self._root_widget or not self._root_widget.exists():
            return
        is_muted = babase.app.config.get(_CFG_CHAT_MUTED, False)
        # prevent stock from loading old messages when we're muted
        if is_muted:
            self._display_old_msgs = False
        _orig_sm = babase.screenmessage
        _sm_patched = False

        def _colored_sm(msg: str, *args, **kwargs) -> None:
            if not args and 'color' not in kwargs and ': ' in msg:
                sender, _, _ = msg.partition(': ')
                base = _chat_color_tracker.get(sender)
                if base is not None:
                    _intensity = finder_config.get(CFG_NAME_CHAT_COLOR_INTENSITY, 'strong')
                    if _intensity == 'strong':
                        kwargs['color'] = tuple(min(1.0, c + 0.3) for c in base)
                    elif _intensity == 'soft':
                        kwargs['color'] = tuple((c + 1.0) / 2.0 for c in base)
            _orig_sm(msg, *args, **kwargs)

        try:
            babase.screenmessage = _colored_sm
            _sm_patched = True
        except (AttributeError, TypeError):
            pass

        try:
            super()._update()
        finally:
            if _sm_patched:
                try:
                    babase.screenmessage = _orig_sm
                except (AttributeError, TypeError):
                    pass
        # always hide the stock muted text; we use our own
        if self._muted_text.exists():
            bui.textwidget(edit=self._muted_text, color=(0, 0, 0, 0))
        if is_muted:
            for w in list(self._chat_texts):
                if w.exists():
                    w.delete()
            self._chat_texts.clear()
            self._chat_senders.clear()
        w = getattr(self, '_lparty_muted_text', None)
        if w and w.exists():
            bui.textwidget(
                edit=w,
                color=_global_theme.get_color('COLOR_SECONDARY') if is_muted else (0, 0, 0, 0),
            )
        send_btn = getattr(self, '_send_button', None)
        if send_btn and send_btn.exists():
            bui.buttonwidget(
                edit=send_btn,
                color=(0.4, 0.4, 0.4) if is_muted else (1, 1, 1),
            )
        if self._roster and len(self._name_widgets) > len(self._roster):
            # bauiv1lib inserts the host text widget right after the host name (index 1)
            w = self._name_widgets[1]
            if w.exists():
                w.delete()
            self._name_widgets.pop(1)
        if self._name_widgets and self._name_widgets[0].exists():
            bui.textwidget(
                edit=self._name_widgets[0],
                color=_global_theme.get_color('COLOR_ACCENT'),
            )
        if self._roster and not self._roster_hidden:
            try:
                plus = babase.app.plus
                if plus is not None:
                    raw = plus.get_v1_account_display_string()
                    if raw:
                        local_display = _normalize_account_name(raw).strip()
                        accent = _global_theme.get_color('COLOR_ACCENT')
                        for idx, entry in enumerate(self._roster):
                            if entry.get('display_string', '').strip() == local_display:
                                if idx < len(self._name_widgets) and self._name_widgets[idx].exists():
                                    bui.textwidget(edit=self._name_widgets[idx], color=accent)
                                break
            except Exception:
                pass
        if self._roster and self._name_widgets and not self._roster_hidden:
            friends = load_friends()
            friend_names: set[str] = set()
            for f in friends:
                n = f['name']
                friend_names.add(n)
                friend_names.add(n.replace(V2_LOGO, ''))
                friend_names.add(f'{V2_LOGO}{n}')
            show_nickname = not self._roster_show_account
            if show_nickname:
                _all_players = get_all_players()
            for idx, entry in enumerate(self._roster):
                if idx >= len(self._name_widgets):
                    break
                if entry.get('client_id') == -1:
                    continue
                acc = entry.get('display_string', '')
                w = self._name_widgets[idx]
                if not w.exists():
                    continue
                nickname = ''
                if show_nickname and acc:
                    players_list = entry.get('players', [])
                    if any(p.get('name_full') for p in players_list):
                        real_name = _normalize_account_name(acc)
                        player_data = _all_players.get(real_name) or _all_players.get(acc)
                        if player_data:
                            nickname = (player_data.get('nickname') or '').strip()
                if acc and is_blocked(acc):
                    edits: dict = {'color': (1.0, 0.3, 0.3)}
                    if nickname:
                        edits['text'] = _fmt_nickname(nickname)
                    bui.textwidget(edit=w, **edits)
                elif acc and (acc in friend_names or acc.replace(V2_LOGO, '') in friend_names):
                    edits = {'color': (0.3, 1.0, 0.4)}
                    if nickname:
                        edits['text'] = _fmt_nickname(nickname)
                    bui.textwidget(edit=w, **edits)
                elif nickname:
                    bui.textwidget(edit=w, text=_fmt_nickname(nickname), color=(1.0, 0.6, 0.2))

        if bs.get_game_roster() and getattr(self, '_roster_show_account', False):
            self._apply_account_names()
        if self._roster_hidden:
            for w in self._name_widgets:
                if w.exists():
                    bui.textwidget(edit=w, text='')
            # Expand scroll to fill the space freed by hiding the user list
            is_small = bui.app.ui_v1.uiscale is bui.UIScale.SMALL
            scroll_h = max(100, self._height - (115 if is_small else 139))
            bui.scrollwidget(
                edit=self._scrollwidget,
                size=(self._scroll_width, scroll_h),
            )
        if bui.app.ui_v1.uiscale is bui.UIScale.SMALL and not self._roster_hidden:
            if self._name_widgets and self._roster:
                roster = self._roster
                columns = (
                    1 if len(roster) == 1 else
                    2 if len(roster) == 2 else 3
                )
                c_width = (self._width * 0.9) / max(3, columns)
                c_width_total = c_width * columns
                c_height = 24
                rows = int(math.ceil(len(roster) / columns))
                c_height_total = c_height * rows
                # Shrink scroll same way as parent but for SMALL height
                bui.scrollwidget(
                    edit=self._scrollwidget,
                    size=(self._scroll_width,
                          max(100, self._height - 110 - c_height_total)),
                )
                # Shift names up and reduce scale
                wi = 0
                for yr in range(rows):
                    for xr in range(columns):
                        idx = yr * columns + xr
                        if idx >= len(roster):
                            break
                        px = (self._width * 0.53
                              - c_width_total * 0.5
                              + c_width * xr - 23)
                        py = self._height - 65 - c_height * yr - 15 + 20
                        if wi < len(self._name_widgets):
                            bui.textwidget(
                                edit=self._name_widgets[wi],
                                position=(px, py),
                                scale=0.55,
                            )
                            wi += 1
                        pass
            else:
                bui.scrollwidget(
                    edit=self._scrollwidget,
                    size=(self._scroll_width, self._height - 150),
                )

    def _do_ping(self) -> None:
        if not self._window_open or self._ping_running:
            return
        info = bs.get_connection_to_host_info_2()
        if info is None or not info.address or not info.port:
            return
        self._ping_running = True
        Thread(
            target=self._ping_thread,
            args=(info.address, info.port),
            daemon=True
        ).start()

    def _ping_thread(self, address: str, port: int) -> None:
        try:
            family = socket.AF_INET6 if ':' in address else socket.AF_INET
            with socket.socket(family, socket.SOCK_DGRAM) as sock:
                sock.settimeout(5.0)
                start = time.monotonic()
                sock.sendto(b'\x0b', (address, port))
                try:
                    data = sock.recv(10)
                    if data == b'\x0c':
                        self._ping_ms = (time.monotonic() - start) * 1000
                except socket.timeout:
                    pass
        except Exception:
            pass
        finally:
            self._ping_running = False
            if self._window_open:
                babase.pushcall(self._update_ping_button, from_other_thread=True)

    def _update_ping_button(self) -> None:
        if self._ping_button is None or not self._ping_button.exists():
            return
        bui.buttonwidget(
            edit=self._ping_button,
            label=f'{round(self._ping_ms)}',
            textcolor=_ping_color(self._ping_ms)
        )

    def _send_ping_chat(self) -> None:
        fmt = str(finder_config.get(CFG_NAME_PING_MSG_FORMAT, get_lang_text('Settings.pingMsgFormatDefault')))
        if '{}' in fmt:
            bs.chatmessage(fmt.format(round(self._ping_ms)))

    def _add_msg(self, msg: str) -> None:
        # Format sender
        sender = None
        if ': ' in msg:
            sender, _, body = msg.partition(': ')
            if self._is_sender_blocked(sender):
                return
            display_msg = self._format_chat_sender(sender) + ': ' + body
        else:
            display_msg = msg

        intensity = finder_config.get(CFG_NAME_CHAT_COLOR_INTENSITY, 'strong')

        msg_color: tuple[float, float, float] = (1.0, 1.0, 1.0)
        if intensity != 'off' and sender:
            base = _chat_color_tracker.get(sender)
            if base is not None:
                if intensity == 'strong':
                    msg_color = tuple(min(1.0, c + 0.3) for c in base)  # type: ignore[assignment]
                else:  # soft
                    msg_color = tuple((c + 1.0) / 2.0 for c in base)  # type: ignore[assignment]

        txt = bui.textwidget(
            parent=self._columnwidget,
            h_align='left',
            v_align='center',
            scale=0.55,
            size=(900, 13),
            text=display_msg,
            color=msg_color,
            autoselect=True,
            always_highlight=True,
            maxwidth=self._scroll_width * 0.94,
            shadow=0.3,
            flatness=1.0,
            on_activate_call=bui.CallStrict(self._copy_msg, msg),
            selectable=True,
        )
        # Single click
        bui.textwidget(
            edit=txt,
            on_select_call=bui.CallStrict(self._on_chat_msg_press, msg, txt),
        )
        self._chat_texts.append(txt)
        self._chat_raw_msgs.append(display_msg)
        self._chat_senders.append(sender)
        while len(self._chat_texts) > 40:
            self._chat_texts.pop(0).delete()
            self._chat_raw_msgs.pop(0)
            if self._chat_senders:
                self._chat_senders.pop(0)
        bui.containerwidget(edit=self._columnwidget, visible_child=txt)

    def _on_chat_msg_press(self, msg: str, widget: bui.Widget | None) -> None:
        # Ignore if triggered
        if self._refreshing_chat:
            return
        self._pressed_chat_msg = msg
        self._pressed_chat_widget = widget
        sender, _, _ = msg.partition(': ')
        self._pressed_chat_sender = sender.strip()
        language = _global_language

        # Resolve sender's account from roster for mention/block
        self._popup_account = ''
        self._popup_chat_roster_entry = None
        for entry in bs.get_game_roster() or []:
            for player in entry.get('players', []):
                n = player.get('name', '')
                nf = player.get('name_full', '')
                if self._pressed_chat_sender in (n, nf) or n in self._pressed_chat_sender or nf in self._pressed_chat_sender:
                    self._popup_account = entry.get('display_string', '')
                    self._popup_chat_roster_entry = entry
                    break
            if self._popup_chat_roster_entry:
                break

        blocked = is_blocked(self._popup_account) if self._popup_account else False
        block_choice = 'remove_blacklist' if blocked else 'add_blacklist'
        block_label = get_lang_text('PartyWindow.unblockUser' if blocked else 'PartyWindow.addBlacklist')

        _entry = self._popup_chat_roster_entry
        _is_host_entry = _entry is not None and _entry.get('client_id') == -1
        _is_self_entry = False
        try:
            plus = babase.app.plus
            if plus is not None:
                raw_local = plus.get_v1_account_display_string()
                if raw_local:
                    local_acc = _normalize_account_name(raw_local).strip()
                    if self._popup_account:
                        _is_self_entry = local_acc == self._popup_account.strip()
                    if not _is_self_entry:
                        sender_str = self._pressed_chat_sender.strip()
                        _is_self_entry = sender_str in (local_acc, raw_local.strip())
        except Exception:
            pass
        _restrict = _is_host_entry or _is_self_entry

        choices = ['chat_translate', 'chat_copy', 'chat_insert']
        choices_display = _creat_Lstr_list([
            language.get_text('ChatPopup.translateText'),
            language.get_text('ChatPopup.copyText'),
            language.get_text('ChatPopup.insertText'),
        ])
        if not _restrict:
            choices.append('chat_player')
            choices_display.append(babase.Lstr(value=language.get_text('ChatPopup.playerOption')))

        if _entry and not _restrict:
            choices += ['chat_mention', block_choice]
            choices_display += [
                babase.Lstr(value=language.get_text('PartyWindow.mention')),
                babase.Lstr(value=block_label),
            ]

        pos = (
            widget.get_screen_space_center()
            if widget and widget.exists()
            else (400.0, 300.0)
        )
        pos = (pos[0] * 1.1, pos[1])

        self._popup_type = 'chat_msg'
        _ThemedPopupMenu(
            position=pos,
            scale=_get_popup_window_scale(),
            choices=choices,
            choices_display=choices_display,
            current_choice=choices[0],
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )

    def _toggle_name_display(self) -> None:
        if self._icon_button is None or not self._icon_button.exists():
            return
        if not bs.get_game_roster():
            return

        if self._roster_hidden:
            self._on_title_single_click()
            return

        self._roster_show_account = not self._roster_show_account

        if self._roster_show_account:
            bui.buttonwidget(
                edit=self._icon_button,
                icon=bui.gettexture('achievementTeamPlayer')
            )
            self._apply_account_names()
        else:
            bui.buttonwidget(
                edit=self._icon_button,
                icon=bui.gettexture('achievementSharingIsCaring')
            )
            # Resetting _roster
            self._roster = []
            self._update()

        bui.getsound('gunCocking').play()

    def _apply_account_names(self) -> None:
        """Overwrites party list name widgets with V2 account names, skipping host."""
        roster: list = getattr(self, '_roster', [])
        name_widgets: list = getattr(self, '_name_widgets', [])
        if not roster or not name_widgets:
            return

        # Skip index 0
        widget_idx = 1
        for entry in roster:
            is_host = entry.get('client_id') == -1
            if is_host:
                continue
            if widget_idx >= len(name_widgets):
                break
            widget = name_widgets[widget_idx]
            if widget.exists():
                client_id = entry.get('client_id', '')
                name = _normalize_account_name(entry['display_string'])
                bui.textwidget(
                    edit=widget,
                    text=f'{name} ({client_id})' if client_id != '' else name,
                )
            widget_idx += 1

    def _on_title_click(self) -> None:
        self._roster_hidden = not self._roster_hidden
        bui.app.config[_CFG_ROSTER_HIDDEN] = {
            'server': self._last_recorded_server,
            'hidden': self._roster_hidden,
        }
        bui.app.config.commit()
        if self._roster_hidden:
            for w in self._name_widgets:
                if w.exists():
                    bui.textwidget(edit=w, text='')
        else:
            self._roster = []
            self._update()
        bui.getsound('click01').play()

    def _on_menu_button_press(self) -> None:
        choices = ['opsiBisu', 'recentServers', 'recentPlayers']
        choices_display = [
            babase.Lstr(value=get_lang_text('Menu.muteChatsOption')),
            babase.Lstr(value=get_lang_text('Menu.recentServers')),
            babase.Lstr(value=get_lang_text('Menu.recentPlayers')),
        ]

        if bs.get_connection_to_host_info_2() is None:
            choices.append('tint')
            choices_display.append(babase.Lstr(value=get_lang_text('Menu.tint')))

        choices.append('saveLastGameReplay')
        choices_display.append(babase.Lstr(value=get_lang_text('Menu.saveReplay')))

        _ThemedPopupMenu(
            position=self._menu_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            width=170.0,
            choices=choices,
            choices_display=choices_display,
            current_choice=choices[0],
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )
        self._popup_type = 'menu'

    def _subscribe_to_theme_changes(self, theme: ReactiveTheme) -> None:
        theme.subscribe('COLOR_BUTTON', self._update_buttons_background_color)
        theme.subscribe('COLOR_PRIMARY', self._update_title_color)
        theme.subscribe('COLOR_SECONDARY', self._update_button_text_color)
        theme.subscribe('COLOR_TERTIARY', self._update_subtitle_color)
        theme.subscribe('COLOR_BACKGROUND', self._update_background_color)
        theme.subscribe('COLOR_ACCENT', self._update_scroll_color)
        self._theme = theme
        self._color_subscriptions = [
            ('COLOR_BUTTON', self._update_buttons_background_color),
            ('COLOR_PRIMARY', self._update_title_color),
            ('COLOR_SECONDARY', self._update_button_text_color),
            ('COLOR_TERTIARY', self._update_subtitle_color),
            ('COLOR_BACKGROUND', self._update_background_color),
            ('COLOR_ACCENT', self._update_scroll_color),
        ]

    def _subscribe_to_language_changes(self, language: ReactiveLanguage) -> None:
        language.subscribe('Global.search', self._update_button_text)
        language.subscribe('PartyWindow.title', self._update_title_text)
        language.subscribe('PartyWindow.emptyStr', self._update_empty_str)
        language.subscribe('PartyWindow.emptyStr2', self._update_empty_str2)
        language.subscribe('Camera.button', self._update_camera_button_label)
        language.subscribe('Button.chats', self._update_chats_button_label)
        language.subscribe('Button.friends', self._update_friends_button_label)
        language.subscribe('Button.trans', self._update_trans_button_label)
        language.subscribe('PartyWindow.chatMuted', self._update_chat_muted_text)
        self._language = language
        self._language_subscriptions = [
            ('Global.search', self._update_button_text),
            ('PartyWindow.title', self._update_title_text),
            ('PartyWindow.emptyStr', self._update_empty_str),
            ('PartyWindow.emptyStr2', self._update_empty_str2),
            ('Camera.button', self._update_camera_button_label),
            ('Button.chats', self._update_chats_button_label),
            ('Button.friends', self._update_friends_button_label),
            ('Button.trans', self._update_trans_button_label),
            ('PartyWindow.chatMuted', self._update_chat_muted_text),
        ]

    def _on_chat_view_button_press(self) -> None:
        show_cid = finder_config.get(CFG_NAME_CHAT_VIEWER_SHOW_CID, False)
        cid_text = get_lang_text('chatHideCid' if show_cid else 'chatShowCid')

        view_type = finder_config.get(CFG_NAME_CHAT_VIEWER_TYPE, False)
        current = {
            CHAT_VIEW_TYPE_PROFILE:  'chatViewProfile',
            CHAT_VIEW_TYPE_ACCOUNT:  'chatViewAccount',
            CHAT_VIEW_TYPE_MULTI:    'chatViewMulti',
            CHAT_VIEW_TYPE_MULTI_V2: 'chatViewMultiV2',
        }.get(view_type, 'chatViewOff')

        choices = [
            'chatShowOrHideCid',
            'chatViewProfile',
            'chatViewAccount',
            'chatViewMulti',
            'chatViewMultiV2',
            'chatViewOff',
        ]
        choices_display = _creat_Lstr_list([
            cid_text,
            get_lang_text('chatViewProfile'),
            get_lang_text('chatViewAccount'),
            get_lang_text('chatViewMulti'),
            get_lang_text('chatViewMultiV2'),
            get_lang_text('chatViewOff'),
        ])
        self._popup_type = 'chat_view'
        _ThemedPopupMenu(
            position=self._chat_view_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            width=170,
            choices=choices,
            choices_display=choices_display,
            current_choice=current,
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )

    def _format_chat_sender(self, sender: str) -> str:
        """Return the sender name reformatted according to the chat viewer setting."""
        view_type = finder_config.get(CFG_NAME_CHAT_VIEWER_TYPE, False)
        show_cid = finder_config.get(CFG_NAME_CHAT_VIEWER_SHOW_CID, False)

        if not view_type:
            return sender

        roster = bs.get_game_roster() or []
        match = None
        for entry in roster:
            for player in entry.get('players', []):
                name = player.get('name', '')
                name_full = player.get('name_full', '')
                if sender in (name, name_full) or name in sender or name_full in sender:
                    match = entry
                    break
            if match:
                break

        if not match:
            # No roster match: try to prefix with icon from the sender itself
            if sender and sender[0] in _SPECIAL_CHARS:
                return sender
            return sender

        account = match.get('display_string', sender)
        # Use name_full to preserve profile icons (color chars, special prefix, etc.)
        profiles_full = [p.get('name_full', '') or p.get('name', '')
                         for p in match.get('players', [])
                         if p.get('name_full') or p.get('name')]
        profile_joint = ', '.join(profiles_full) if profiles_full else sender
        client_id = match.get('client_id', -1)
        cid_prefix = f'[{client_id}] ' if show_cid and client_id != -1 else ''

        # If player has a nickname and is using a profile
        if profiles_full:
            real_name = _normalize_account_name(account)
            _pdata = _gap().get(real_name) or _gap().get(account)
            if _pdata:
                _nick = (_pdata.get('nickname') or '').strip()
                if _nick:
                    return cid_prefix + _fmt_nickname(_nick)

        # Icon from display_string
        account_icon = account[0] if account and account[0] in _SPECIAL_CHARS else ''

        if view_type == CHAT_VIEW_TYPE_PROFILE:
            return cid_prefix + (profile_joint if profiles_full else sender)
        if view_type == CHAT_VIEW_TYPE_ACCOUNT:
            return cid_prefix + account
        if view_type in (CHAT_VIEW_TYPE_MULTI, CHAT_VIEW_TYPE_MULTI_V2):
            if account != profile_joint:
                return cid_prefix + account + ' | ' + profile_joint
            return cid_prefix + account
        if account_icon and not sender.startswith(account_icon):
            return account_icon + sender
        return sender

    def _refresh_chat(self) -> None:
        self._refreshing_chat = True
        self._nav_idx = -1
        self._nav_prev_idx = -1
        self._nav_prev_widget = None
        self._chat_raw_msgs.clear()
        self._chat_senders.clear()
        while self._chat_texts:
            self._chat_texts.pop(0).delete()
        for msg in bs.get_chat_messages():
            self._add_msg(msg)
        babase.apptimer(0.1, bui.WeakCall(self._end_chat_refresh))

    def _end_chat_refresh(self) -> None:
        self._refreshing_chat = False

    def refresh_after_nickname_change(self) -> None:
        """Refresh chat messages and roster display after a nickname is saved or cleared."""
        self._refresh_chat()
        self._roster = []
        self._update()

    def refresh_chat_colors(self) -> None:
        """Recolor existing chat widgets based on current intensity setting."""
        intensity = finder_config.get(CFG_NAME_CHAT_COLOR_INTENSITY, 'strong')
        for i, widget in enumerate(self._chat_texts):
            if not widget.exists():
                continue
            sender = self._chat_senders[i] if i < len(self._chat_senders) else None
            color: tuple[float, float, float] = (1.0, 1.0, 1.0)
            if intensity != 'off' and sender:
                base = _chat_color_tracker.get(sender)
                if base is not None:
                    if intensity == 'strong':
                        color = tuple(min(1.0, c + 0.3) for c in base)  # type: ignore[assignment]
                    else:
                        color = tuple((c + 1.0) / 2.0 for c in base)  # type: ignore[assignment]
            bui.textwidget(edit=widget, color=color)

    def _translate_chat_widget(self, msg: str, widget: bui.Widget | None) -> None:
        text = msg.strip()
        if not text or not any(c.isalpha() for c in text):
            bui.getsound('error').play()
            return

        src = finder_config.get(CFG_NAME_TRANSLATE_SOURCE_OTHER, 'auto')
        dst = finder_config.get(CFG_NAME_TRANSLATE_DESTINATION_OTHER, 'en')
        method = finder_config.get(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, 'api')

        babase.screenmessage('Translating...', color=(0.6, 0.6, 1.0))

        def _apply(translated: str) -> None:
            if translated.lower() == text.lower():
                return
            if widget and widget.exists():
                bui.textwidget(edit=widget, text=translated)

        def _run() -> None:
            try:
                if method == 'link':
                    import urllib.parse as _up, urllib.request as _ur, re
                    params = _up.urlencode({'sl': src, 'tl': dst, 'text': text})
                    with _ur.urlopen(f'https://translate.google.com/m?{params}', timeout=8) as resp:
                        match = re.search(r'class="result-container">(.*?)<', resp.read().decode())
                        translated = match.group(1) if match else text
                else:
                    params = urllib.parse.urlencode({
                        'client': 'gtx', 'sl': src, 'tl': dst, 'dt': 't', 'q': text
                    })
                    url = f'https://translate.googleapis.com/translate_a/single?{params}'
                    with urllib.request.urlopen(url, timeout=8) as resp:
                        translated = json.loads(resp.read().decode())[0][0][0]
                babase.pushcall(lambda: _apply(translated), from_other_thread=True)
            except Exception:
                babase.pushcall(
                    lambda: babase.screenmessage('Translation failed', color=(1.0, 0.3, 0.3)),
                    from_other_thread=True,
                )

        Thread(target=_run, daemon=True).start()

    def _on_translate_button_press(self) -> None:
        if not self._translate_button_armed:
            self._translate_button_armed = True
            babase.apptimer(0.3, self._translate_text_field)
        else:
            self._translate_button_armed = False
            TranslationSettings()

    def _translate_text_field(self) -> None:
        if not self._translate_button_armed:
            return
        self._translate_button_armed = False

        msg: str = bui.textwidget(query=self._text_field)
        text = msg.strip()
        if not text or not any(c.isalpha() for c in text):
            bui.getsound('error').play()
            return

        src = finder_config.get(CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD, 'auto')
        dst = finder_config.get(CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD, 'en')
        method = finder_config.get(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, 'api')

        babase.screenmessage('Translating...', color=(0.6, 0.6, 1.0))

        def _apply(translated: str) -> None:
            if self._text_field.exists():
                bui.textwidget(edit=self._text_field, text=translated)

        def _run() -> None:
            try:
                if method == 'link':
                    import urllib.parse as _up
                    params = _up.urlencode({'sl': src, 'tl': dst, 'text': text})
                    url = f'https://translate.google.com/m?{params}'
                    import urllib.request as _ur
                    with _ur.urlopen(url, timeout=8) as resp:
                        import re
                        html = resp.read().decode()
                        match = re.search(r'class="result-container">(.*?)<', html)
                        translated = match.group(1) if match else text
                else:
                    params = urllib.parse.urlencode({
                        'client': 'gtx', 'sl': src, 'tl': dst, 'dt': 't', 'q': text
                    })
                    url = f'https://translate.googleapis.com/translate_a/single?{params}'
                    with urllib.request.urlopen(url, timeout=8) as resp:
                        data = json.loads(resp.read().decode())
                        translated = data[0][0][0]
                babase.pushcall(lambda: _apply(translated), from_other_thread=True)
            except Exception:
                babase.pushcall(
                    lambda: babase.screenmessage('Translation failed', color=(1.0, 0.3, 0.3)),
                    from_other_thread=True,
                )

        Thread(target=_run, daemon=True).start()

    def _send_chat_message(self) -> None:
        if babase.app.config.get(_CFG_CHAT_MUTED, False):
            bui.getsound('error').play()
            return
        text = str(bui.textwidget(query=self._text_field)).strip()
        if not text:
            self._show_quick_respond_window()
            return
        chunks: list[str] = []
        while len(text) > 64:
            chunks.append(text[:63] + '-')
            text = text[63:]
        chunks.append(text)
        for chunk in chunks:
            bs.chatmessage(chunk)
        bui.textwidget(edit=self._text_field, text='')

    def _show_quick_respond_window(self) -> None:
        choices = load_quick_responds()
        edit_order_text = f'*** {get_lang_text("QuickRespond.editOrder")} ***'
        choices.insert(0, edit_order_text)
        send_btn = getattr(self, '_send_button', None)
        if send_btn is None or not send_btn.exists():
            return
        self._popup_type = 'quickRespond'
        _ThemedPopupMenu(
            position=send_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            current_choice=choices[-1],
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
            scroll_color=_global_theme.get_color('COLOR_ACCENT'),
            scroll_threshold=4,
        )

    def _show_icons_popup(self) -> None:
        self._popup_type = 'icons'
        _ThemedPopupMenu(
            position=self._icons_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=_SPECIAL_CHARS,
            current_choice='',
            width=80.0,
            maxwidth=80.0,
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )

    def _append_to_chat(self, text: str) -> None:
        if not hasattr(self, '_text_field') or not self._text_field.exists():
            return
        current = bui.textwidget(query=self._text_field)
        bui.textwidget(edit=self._text_field, text=current + text)

    _NAV_MARK = '>> '

    def _nav_restore_prev(self) -> None:
        if self._nav_prev_widget and self._nav_prev_widget.exists():
            raw = (
                self._chat_raw_msgs[self._nav_prev_idx]
                if 0 <= self._nav_prev_idx < len(self._chat_raw_msgs)
                else ''
            )
            bui.textwidget(
                edit=self._nav_prev_widget,
                text=raw,
                color=(1, 1, 1),
            )
        self._nav_prev_widget = None
        self._nav_prev_idx = -1

    def _nav_apply_highlight(self, widget: bui.Widget, idx: int) -> None:
        raw = self._chat_raw_msgs[idx] if 0 <= idx < len(self._chat_raw_msgs) else ''
        highlighted = self._NAV_MARK + raw
        color = _global_theme.get_color('COLOR_SECONDARY')
        bui.textwidget(
            edit=widget,
            text=highlighted,
            color=color,
        )
        queried = str(bui.textwidget(query=widget))
        self._nav_prev_widget = widget
        self._nav_prev_idx = idx

    def _previous_message(self) -> None:
        if not self._chat_texts:
            return
        if self._nav_idx == -1:
            self._nav_idx = len(self._chat_texts) - 1
        else:
            self._nav_idx -= 1
            if self._nav_idx < 0:
                self._nav_idx = -1
                self._nav_restore_prev()
                bui.textwidget(edit=self._text_field, text='')
                return
        raw = self._chat_raw_msgs[self._nav_idx] if self._nav_idx < len(self._chat_raw_msgs) else ''
        body = raw.partition(': ')[2] if ': ' in raw else raw
        widget = self._chat_texts[self._nav_idx]
        bui.containerwidget(edit=self._columnwidget, visible_child=widget)
        self._nav_restore_prev()
        self._nav_apply_highlight(widget, self._nav_idx)
        bui.textwidget(edit=self._text_field, text=body)

    def _next_message(self) -> None:
        if not self._chat_texts:
            return
        if self._nav_idx == -1:
            self._nav_idx = 0
        else:
            self._nav_idx += 1
            if self._nav_idx >= len(self._chat_texts):
                self._nav_idx = -1
                self._nav_restore_prev()
                bui.textwidget(edit=self._text_field, text='')
                return
        raw = self._chat_raw_msgs[self._nav_idx] if self._nav_idx < len(self._chat_raw_msgs) else ''
        body = raw.partition(': ')[2] if ': ' in raw else raw
        widget = self._chat_texts[self._nav_idx]
        bui.containerwidget(edit=self._columnwidget, visible_child=widget)
        self._nav_restore_prev()
        self._nav_apply_highlight(widget, self._nav_idx)
        bui.textwidget(edit=self._text_field, text=body)

    def _on_nav_clear(self) -> None:
        self._nav_idx = -1
        self._nav_restore_prev()
        bui.textwidget(edit=self._text_field, text='')

    def _ip_port_msg(self) -> None:
        info = bs.get_connection_to_host_info_2()
        if info and info.address and info.port:
            bui.textwidget(edit=self._text_field, text=f'{info.address}:{info.port}')
        else:
            bui.getsound('error').play()

    def _open_gather(self) -> None:
        self._window_open = False
        self._party_check_timer = None
        self._unsubscribe_all_changes()
        if self._root_widget.exists():
            bui.containerwidget(edit=self._root_widget, transition='out_left')
            root = self._root_widget
            babase.apptimer(0.5, root.delete)
        # Temporarily register GatherModified in the nav system so that
        # if it auto-recreates gather, it uses the right class.
        from _bampui.lparty import set_global_gather_modified
        set_global_gather_modified(True)
        GatherModified(transition='in_left', from_party=True)

    def _update_background_color(self, new_color: tuple) -> None:
        self.background_color = new_color
        if self._root_widget and self._root_widget.exists():
            from _bampui.theme import o_container
            o_container(edit=self._root_widget, color=new_color)

    def _update_scroll_color(self, new_color: tuple) -> None:
        if self._scrollwidget and self._scrollwidget.exists():
            bui.scrollwidget(edit=self._scrollwidget, color=new_color)

    def _update_buttons_background_color(self, new_color: tuple) -> None:
        self.button_color = new_color
        for btn in [
            getattr(self, '_cancel_button', None),
            getattr(self, '_chat_view_button', None),
            getattr(self, 'finder_button', None),
            getattr(self, 'button2', None),
            getattr(self, 'button3', None),
            getattr(self, 'button4', None),
            getattr(self, '_icons_button', None),
            getattr(self, '_translate_button', None),
            getattr(self, '_menu_button', None),
            getattr(self, '_settings_button', None),
            getattr(self, '_ping_button', None),
            getattr(self, '_icon_button', None),
            getattr(self, '_ip_button', None),
            getattr(self, '_gather_button', None),
            getattr(self, '_next_button', None),
            getattr(self, '_previous_button', None),
            getattr(self, '_nav_clear_button', None),
        ]:
            if btn and btn.exists():
                bui.buttonwidget(edit=btn, color=new_color)

    def _update_title_color(self, new_color: tuple) -> None:
        self.title_color = new_color
        txt = getattr(self, '_title_text', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, color=new_color)

    def _update_button_text_color(self, new_color: tuple) -> None:
        self.subtitle_color = new_color
        for btn in [
            getattr(self, 'finder_button', None),
            getattr(self, 'button2', None),
            getattr(self, 'button3', None),
            getattr(self, 'button4', None),
            getattr(self, '_translate_button', None),
        ]:
            if btn and btn.exists():
                bui.buttonwidget(edit=btn, textcolor=new_color)
        self.bg_color = new_color
        txt = getattr(self, '_empty_str', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, color=new_color)

    def _update_subtitle_color(self, new_color: tuple) -> None:
        self.text_color = new_color
        txt = getattr(self, '_empty_str_2', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, color=new_color)

    def _update_button_text(self, new_text: str) -> None:
        if self.finder_button and self.finder_button.exists():
            bui.buttonwidget(edit=self.finder_button, label=new_text)

    def _update_title_text(self, new_text: str) -> None:
        txt = getattr(self, '_title_text', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, text=new_text)

    def _update_empty_str(self, new_text: str) -> None:
        if bs.get_game_roster():
            return
        txt = getattr(self, '_empty_str', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, text=new_text)

    def _update_empty_str2(self, new_text: str) -> None:
        if bs.get_game_roster():
            return
        txt = getattr(self, '_empty_str_2', None)
        if txt and txt.exists():
            bui.textwidget(edit=txt, text=new_text)

    def _update_camera_button_label(self, new_text: str) -> None:
        btn = getattr(self, 'button4', None)
        if btn and btn.exists():
            bui.buttonwidget(edit=btn, label=new_text)

    def _update_chats_button_label(self, new_text: str) -> None:
        btn = getattr(self, 'button2', None)
        if btn and btn.exists():
            bui.buttonwidget(edit=btn, label=new_text)

    def _update_friends_button_label(self, new_text: str) -> None:
        btn = getattr(self, 'button3', None)
        if btn and btn.exists():
            bui.buttonwidget(edit=btn, label=new_text)

    def _update_chat_muted_text(self, new_text: str) -> None:
        w = getattr(self, '_lparty_muted_text', None)
        if w and w.exists():
            bui.textwidget(edit=w, text=new_text)

    def _update_trans_button_label(self, new_text: str) -> None:
        btn = getattr(self, '_translate_button', None)
        if btn and btn.exists():
            bui.buttonwidget(edit=btn, label=new_text)

    def _show_camera_popup(self) -> None:
        self._popup_type = 'camera'
        _ThemedPopupMenu(
            position=self.button4.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            width=160.0,
            choices=['cameraSet', 'cameraGet'],
            choices_display=_creat_Lstr_list([
                get_lang_text('Camera.setCamera'),
                get_lang_text('Camera.getCamera'),
            ]),
            current_choice='cameraSet',
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )

    def _unsubscribe_theme_changes(self) -> None:
        if hasattr(self, '_color_subscriptions') and hasattr(self, '_theme'):
            for color_name, callback in self._color_subscriptions:
                self._theme.unsubscribe(color_name, callback)
            self._color_subscriptions.clear()

    def _unsubscribe_language_changes(self) -> None:
        if hasattr(self, '_language_subscriptions') and hasattr(self, '_language'):
            for text_key, callback in self._language_subscriptions:
                self._language.unsubscribe(text_key, callback)
            self._language_subscriptions.clear()

    def _on_uiscale_change(self, _: babase.UIScale) -> None:
        if not self._window_open:
            return
        _uiscale_unsubscribe(self._on_uiscale_change)
        self._window_open = False
        self._party_check_timer = None
        self._unsubscribe_theme_changes()
        self._unsubscribe_language_changes()
        remove_unread_dm_listener(self._update_dm_badge)
        remove_online_status_listener(self._update_online_badge)
        if self._root_widget.exists():
            bui.containerwidget(edit=self._root_widget, transition='out_scale')
        babase.apptimer(0.25, LPartyWindow)

    def _unsubscribe_all_changes(self) -> None:
        self._unsubscribe_theme_changes()
        self._unsubscribe_language_changes()
        _uiscale_unsubscribe(self._on_uiscale_change)
        remove_unread_dm_listener(self._update_dm_badge)
        remove_online_status_listener(self._update_online_badge)

    def _update_dm_badge(self) -> None:
        if not (self._root_widget.exists() and hasattr(self, '_dm_badge_img')):
            return
        count = len(get_all_unread_dm_counts())
        visible = count > 0
        bui.imagewidget(edit=self._dm_badge_img, opacity=1.0 if visible else 0.0)
        bui.textwidget(edit=self._dm_badge_num, text=str(count) if visible else '')

    def _update_online_badge(self) -> None:
        if not (self._root_widget.exists() and hasattr(self, '_online_badge_img')):
            return
        count = len(get_online_friend_ids())
        visible = count > 0
        bui.imagewidget(edit=self._online_badge_img, opacity=1.0 if visible else 0.0)
        bui.textwidget(edit=self._online_badge_num, text=str(count) if visible else '')

    def _on_party_member_press(self, client_id: int, is_host: bool,
                               widget: bui.Widget) -> None:
        entry = next(
            (e for e in (self._roster or []) if e.get('client_id') == client_id),
            None
        )

        language = _global_language
        kick_label = get_lang_text('PartyWindow.kickById').format(client_id)

        # Determine dynamic labels for block/friend based on current state
        acc = entry.get('display_string', '') if entry else ''
        blocked = is_blocked(acc)
        friends = load_friends()
        friend_entry = next(
            (f for f in friends if f['name'] in (acc, f'{V2_LOGO}{acc}', acc.replace(V2_LOGO, ''))),
            None
        )
        is_friend = friend_entry is not None
        self._popup_account = acc
        self._popup_friend_entry = friend_entry

        block_choice = 'remove_blacklist' if blocked else 'add_blacklist'
        block_label = get_lang_text('PartyWindow.unblockUser' if blocked else 'PartyWindow.addBlacklist')
        friend_choice = 'remove_friend_local' if is_friend else 'add_friend'
        friend_label = get_lang_text('PartyWindow.removeFriend' if is_friend else 'PartyWindow.addFriend')

        is_self = False
        try:
            plus = babase.app.plus
            if plus is not None:
                raw_local = plus.get_v1_account_display_string()
                if raw_local and acc:
                    is_self = _normalize_account_name(raw_local).strip() == acc.strip()
        except Exception:
            pass

        items = [
            ('mention', babase.Lstr(value=language.get_text('PartyWindow.mention'))),
        ]
        if not is_host:
            items.append(('info', babase.Lstr(value=get_lang_text('PartyWindow.viewAccount'))))
        if not is_host and not is_self:
            items += [
                ('kick', babase.Lstr(value=get_lang_text('PartyWindow.voteToKick'))),
                ('kick_by_id', babase.Lstr(value=kick_label)),
                ('player_info', babase.Lstr(value=get_lang_text('ChatPopup.playerOption'))),
                (friend_choice, babase.Lstr(value=friend_label)),
                (block_choice, babase.Lstr(value=block_label)),
            ]
        choices = [i[0] for i in items]
        choices_display = [i[1] for i in items]

        self._popup_party_member_client_id = client_id
        self._popup_party_member_is_host = is_host
        self._popup_type = 'partyMemberPress'

        _ThemedPopupMenu(
            position=widget.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            width=170.0,
            choices=choices,
            choices_display=choices_display,
            current_choice='kick',
            delegate=self,
            bg_color=self.background_color,
            text_color=self.title_color,
        )

    def _getObjectByID(self, type: str = 'playerName',
                       ID: int | None = None) -> object:
        """Lookup roster data by client ID. Defaults to the last pressed member."""
        if ID is None:
            ID = self._popup_party_member_client_id
        type = type.lower()
        output = []

        if not self._roster:
            return None

        for entry in self._roster:
            if type.startswith('all'):
                if type in ('roster', 'fullrecord'):
                    output.append(entry)
                elif 'player' in type and entry['players']:
                    if 'namefull' in type:
                        output += [p['name_full'] for p in entry['players']]
                    elif 'name' in type:
                        output += [p['name'] for p in entry['players']]
                    elif 'playerid' in type:
                        output += [p['id'] for p in entry['players']]
                elif type in ('account', 'displaystring'):
                    output.append(entry['display_string'])
            elif entry['client_id'] == ID:
                try:
                    if type in ('roster', 'fullrecord'):
                        return entry
                    elif 'player' in type and entry['players']:
                        single = len(entry['players']) == 1 or 'singleplayer' in type
                        if single:
                            if 'namefull' in type:
                                return entry['players'][0]['name_full']
                            elif 'name' in type:
                                return entry['players'][0]['name']
                            elif 'playerid' in type:
                                return entry['players'][0]['id']
                        else:
                            if 'namefull' in type:
                                return [p['name_full'] for p in entry['players']]
                            elif 'name' in type:
                                return [p['name'] for p in entry['players']]
                            elif 'playerid' in type:
                                return [p['id'] for p in entry['players']]
                    elif type in ('account', 'displaystring'):
                        return entry['display_string']
                except Exception:
                    babase.print_exception()

        return None if not output else output

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        if self._popup_type == 'mentionSelect':
            current = str(bui.textwidget(query=self._text_field))
            bui.textwidget(edit=self._text_field, text=current + f'@{choice} ')
            return

        if self._popup_type == 'icons':
            self._append_to_chat(choice)
            return

        if self._popup_type == 'quickRespond':
            edit_order_text = f'*** {get_lang_text("QuickRespond.editOrder")} ***'
            if choice == edit_order_text:
                SortMessagesList(
                    data=load_quick_responds(),
                    write_data_func=save_quick_responds,
                    label=get_lang_text('QuickRespond.label'),
                )
            else:
                self._append_to_chat(choice)
            return

        if self._popup_type == 'chat_msg':
            msg = getattr(self, '_pressed_chat_msg', '')
            widget = getattr(self, '_pressed_chat_widget', None)
            if choice == 'chat_translate':
                self._translate_chat_widget(msg, widget)
            elif choice == 'chat_copy':
                if bui.clipboard_is_supported():
                    bui.clipboard_set_text(msg)
                    babase.screenmessage(get_lang_text('Global.copiedToClipboard'))
            elif choice == 'chat_insert':
                self._append_to_chat(msg)
            elif choice == 'chat_player':
                sender = getattr(self, '_pressed_chat_sender', '')
                # match against roster to get the V2 display_string (playerinfo key)
                roster = bs.get_game_roster() or []
                v2_name = None
                for entry in roster:
                    for player in entry.get('players', []):
                        pname = player.get('name', '')
                        pname_full = player.get('name_full', '')
                        if sender in (pname, pname_full) or pname in sender or pname_full in sender:
                            v2_name = entry.get('display_string')
                            break
                    if v2_name:
                        break
                players = get_all_players()
                real_name = v2_name if v2_name and v2_name in players else None
                if real_name:
                    babase.apptimer(0.15, lambda n=real_name: PlayerInfoPopup(n))
                else:
                    babase.screenmessage(get_lang_text('ChatPopup.playerNotFound'),
                                        color=(1, 0.5, 0.5))
            elif choice == 'chat_mention':
                entry = getattr(self, '_popup_chat_roster_entry', None)
                if not entry:
                    return
                account = entry.get('display_string', '')
                player_names = [
                    p.get('name_full') or p.get('name', '')
                    for p in entry.get('players', [])
                    if p.get('name_full') or p.get('name')
                ]
                names: list[str] = []
                if account:
                    names.append(account.strip())
                for n in player_names:
                    n_clean = n.strip()
                    if n_clean and n_clean not in names:
                        names.append(n_clean)
                if not names:
                    return
                self._popup_type = 'mentionSelect'
                _ThemedPopupMenu(
                    position=popup_window.root_widget.get_screen_space_center(),
                    scale=_get_popup_window_scale(),
                    width=170.0,
                    choices=names,
                    choices_display=_creat_Lstr_list(names),
                    current_choice=names[0],
                    delegate=self,
                    bg_color=self.background_color,
                    text_color=self.title_color,
                )
            elif choice == 'add_blacklist':
                acc = getattr(self, '_popup_account', '')
                if acc:
                    set_blocked(acc, True)
                    TIP(f'{acc} {get_lang_text("Global.addedSuccessfully")}')
                    self._refresh_chat()
                    self._roster = None
            elif choice == 'remove_blacklist':
                acc = getattr(self, '_popup_account', '')
                if acc:
                    set_blocked(acc, False)
                    TIP(f'{acc} {get_lang_text("Global.removedSuccessfully")}')
                    self._refresh_chat()
                    self._roster = None
            return

        if self._popup_type == 'chat_view':
            if choice == 'chatShowOrHideCid':
                finder_config[CFG_NAME_CHAT_VIEWER_SHOW_CID] = not finder_config.get(
                    CFG_NAME_CHAT_VIEWER_SHOW_CID, False)
            elif choice == 'chatViewProfile':
                finder_config[CFG_NAME_CHAT_VIEWER_TYPE] = CHAT_VIEW_TYPE_PROFILE
            elif choice == 'chatViewAccount':
                finder_config[CFG_NAME_CHAT_VIEWER_TYPE] = CHAT_VIEW_TYPE_ACCOUNT
            elif choice == 'chatViewMulti':
                finder_config[CFG_NAME_CHAT_VIEWER_TYPE] = CHAT_VIEW_TYPE_MULTI
            elif choice == 'chatViewMultiV2':
                finder_config[CFG_NAME_CHAT_VIEWER_TYPE] = CHAT_VIEW_TYPE_MULTI_V2
            elif choice == 'chatViewOff':
                finder_config[CFG_NAME_CHAT_VIEWER_TYPE] = False
            save_finder_config(finder_config)
            self._refresh_chat()
            return

        if self._popup_type == 'menu':
            if choice == 'opsiBisu':
                is_muted = babase.app.config.get(_CFG_CHAT_MUTED, False)
                mute_key = 'unmuteChat' if is_muted else 'muteChat'
                mute_text = 'Menu.unmuteChat' if is_muted else 'Menu.muteChat'
                self._popup_type = 'mute'
                _ThemedPopupMenu(
                    position=self._menu_button.get_screen_space_center(),
                    scale=_get_popup_window_scale(),
                    width=170,
                    choices=[mute_key, 'muteUsers'],
                    choices_display=_creat_Lstr_list([
                        get_lang_text(mute_text),
                        get_lang_text('Menu.muteUsers'),
                    ]),
                    current_choice=mute_key,
                    delegate=self,
                    bg_color=self.background_color,
                    text_color=self.title_color,
                )
            elif choice == 'recentServers':
                LastServersWindow(party_window=self)
            elif choice == 'recentPlayers':
                RecentPlayersWindow()
            elif choice == 'saveLastGameReplay':
                self._save_last_game_replay()
            elif choice == 'tint':
                TintWindow()
            return

        if self._popup_type == 'mute':
            if choice in ('muteChat', 'unmuteChat'):
                muting = (choice == 'muteChat')
                babase.app.config[_CFG_CHAT_MUTED] = muting
                babase.app.config.commit()
                if muting:
                    for w in list(self._chat_texts):
                        if w.exists():
                            w.delete()
                    self._chat_texts.clear()
                    self._chat_senders.clear()
                else:
                    self._display_old_msgs = True
                    self._update()
            elif choice == 'muteUsers':
                MuteUsersWindow(self.get_root_widget())
            return

        if self._popup_type == 'camera':
            if choice == 'cameraGet':
                CameraPositionsWindow()
            elif choice == 'cameraSet':
                self.close()
                CameraOverlay()
            return

        if self._popup_type == 'banTimePress':
            result = bs.disconnect_client(
                self._popup_party_member_client_id, ban_time=int(choice))
            if not result:
                bui.getsound('error').play()
                bs.broadcastmessage(
                    babase.Lstr(resource='getTicketsWindow.unavailableText'),
                    color=(1, 0, 0))
            return

        if self._popup_type == 'partyMemberPress':
            if choice == 'kick':
                areYouSureToKickText = get_lang_text('PartyWindow.areYouSureToKick')
                ConfirmWindow(
                    text=f'{areYouSureToKickText} {self._getObjectByID("account")}?',
                    action=self._kick_selected_player,
                    cancel_button=True,
                    cancel_is_selected=True,
                    color=(1, 1, 1),
                    text_scale=1.0,
                    origin_widget=self.get_root_widget()
                )
            elif choice == 'info':
                account = self._getObjectByID('account')
                clean_name = account.replace(V2_LOGO, '')
                ProfileSearchWindow(self.get_root_widget(), v2=clean_name)
            elif choice == 'player_info':
                account = self._getObjectByID('account')
                players = get_all_players()
                if account and account in players:
                    babase.apptimer(0.15, lambda n=account: PlayerInfoPopup(n))
                else:
                    babase.screenmessage(get_lang_text('ChatPopup.playerNotFound'),
                                        color=(1, 0.5, 0.5))
            elif choice == 'add_friend':
                account = self._getObjectByID('account')
                clean_name = account.replace(V2_LOGO, '')
                self._add_friend(clean_name)
            elif choice == 'mention':
                account = self._getObjectByID('account')
                player_names = self._getObjectByID('playerNameFull') or []
                if isinstance(player_names, str):
                    player_names = [player_names]
                names: list[str] = []
                if account:
                    names.append(str(account).strip())
                for n in player_names:
                    n_clean = str(n).strip()
                    if n_clean and n_clean not in names:
                        names.append(n_clean)
                if not names:
                    return
                self._popup_type = 'mentionSelect'
                _ThemedPopupMenu(
                    position=popup_window.root_widget.get_screen_space_center(),
                    scale=_get_popup_window_scale(),
                    width=170.0,
                    choices=names,
                    choices_display=_creat_Lstr_list(names),
                    current_choice=names[0],
                    delegate=self,
                    bg_color=self.background_color,
                    text_color=self.title_color,
                )
            elif choice == 'kick_by_id':
                self._kick_selected_player()
            elif choice == 'add_blacklist':
                acc = getattr(self, '_popup_account', '') or self._getObjectByID('account') or ''
                if acc:
                    set_blocked(acc, True)
                    TIP(f'{acc} {get_lang_text("Global.addedSuccessfully")}')
                    self._refresh_chat()
                    self._roster = None
            elif choice == 'remove_blacklist':
                acc = getattr(self, '_popup_account', '') or self._getObjectByID('account') or ''
                if acc:
                    set_blocked(acc, False)
                    TIP(f'{acc} {get_lang_text("Global.removedSuccessfully")}')
                    self._refresh_chat()
                    self._roster = None
            elif choice == 'remove_friend_local':
                fe = getattr(self, '_popup_friend_entry', None)
                if fe:
                    remove_friend(fe['id'])
                    TIP(f'{fe["name"]} {get_lang_text("Global.removedSuccessfully")}')
                    self._roster = None

    def _add_friend(self, friend: str) -> None:
        if not friend or not friend.strip():
            TIP(get_lang_text('Global.fieldEmpty'), (1, 0, 0))
            bui.getsound('error').play()
            return

        prefixed_friend = f'{V2_LOGO}{friend.strip()}'
        friends = load_friends()

        for f in friends:
            if f['name'] == prefixed_friend:
                TIP(f'{prefixed_friend} {get_lang_text("Global.alreadyInList")}')
                return

        existing_ids = [int(f['id']) for f in friends if f['id'].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

        add_friend(
            name=prefixed_friend,
            friend_id=new_id,
            accounts=[],
            account_pb=None,
            account_id=None
        )
        TIP(f'{prefixed_friend} {get_lang_text("Global.addedSuccessfully")}')
        self._roster = None  # force color refresh on next tick

    def _kick_selected_player(self) -> None:
        if self._popup_party_member_client_id != -1:
            if bs.get_foreground_host_session() is not None:
                self._popup_type = 'banTimePress'
                choices = [0, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 99999999]
                PopupMenuWindow(
                    position=self.get_root_widget().get_screen_space_center(),
                    scale=_get_popup_window_scale(),
                    choices=[str(c) for c in choices],
                    choices_display=_creat_Lstr_list(
                        [f'Ban for {c} second(s).' for c in choices]),
                    current_choice='0',
                    delegate=self
                )
            else:
                info = bs.get_connection_to_host_info_2()
                if bool(info) and info.build_number < 14248:
                    bui.getsound('error').play()
                    bs.broadcastmessage(
                        babase.Lstr(resource='getTicketsWindow.unavailableText'),
                        color=(1, 0, 0))
                else:
                    result = bs.disconnect_client(
                        self._popup_party_member_client_id, ban_time=5 * 60)
                    if not result:
                        bui.getsound('error').play()
                        bs.broadcastmessage(
                            babase.Lstr(resource='getTicketsWindow.unavailableText'),
                            color=(1, 0, 0))
        else:
            bui.getsound('error').play()
            bs.broadcastmessage(
                babase.Lstr(resource='internal.cantKickHostError'),
                color=(1, 0, 0))

    def _is_sender_blocked(self, sender: str) -> bool:
        for entry in bs.get_game_roster() or []:
            for player in entry.get('players', []):
                n = player.get('name', '')
                nf = player.get('name_full', '')
                if sender in (n, nf) or n in sender or nf in sender:
                    account = entry.get('display_string', '')
                    return bool(account and is_blocked(account))
        return False

    def _save_last_game_replay(self) -> None:
        ReplayNameSavingPopup()

    def color_picker_selected_color(self, picker: object, color: tuple) -> None:
        """Called on every color change for live preview."""
        tag = picker.get_tag()  # type: ignore[attr-defined]
        if tag == 'COLOR_BACKGROUND':
            finder_config[CFG_NAME_COLOR_BACKGROUND] = color
            _global_theme.update_colors({'COLOR_BACKGROUND': color})

    def color_picker_closing(self, _: object) -> None:
        """Called when the color picker closes — persist the selection."""
        save_finder_config(finder_config)

    def _show_friends_popup(self) -> None:
        import threading
        self._update_online_badge()
        if not is_logged_in():
            bui.screenmessage('You need to log in first.', color=(1, 0.5, 0))
            return

        def _run() -> None:
            body, status = authenticated_get('/friends/')
            friends = body if status == 200 and isinstance(body, list) else []
            babase.pushcall(lambda: _show(friends), from_other_thread=True)

        def _show(friends: list) -> None:
            if not self._root_widget.exists():
                return
            if not friends:
                bui.screenmessage('No friends yet.', color=(0.7, 0.7, 0.7))
                return
            pos = self.button3.get_screen_space_center()
            _FriendPickerWindow(
                friends=friends,
                position=pos,
                on_select=lambda f: _FriendActionWindow(
                    friend=f,
                    position=pos,
                    is_online=f.get('friend_id') in get_online_friend_ids(),
                    on_invite=lambda: self._invite_friend_to_party(f),
                    on_message=lambda: self._message_friend(f),
                    on_account=lambda: self._view_friend_account(f),
                ),
            )

        threading.Thread(target=_run, daemon=True).start()

    def _invite_friend_to_party(self, friend: dict) -> None:
        import threading
        info = bs.get_connection_to_host_info_2()
        if info is None or not info.address:
            bui.screenmessage('Not connected to any server.', color=(1, 0.6, 0.2))
            return
        receiver_id = friend.get('friend_id')
        name = friend.get('friend_nickname', '?')
        ip = info.address
        port = str(info.port)

        def _run() -> None:
            ok = ensure_friends_session().send_server_invite(receiver_id, name, ip, port)

            def _apply() -> None:
                if ok:
                    bui.screenmessage(f'Invited {name}!', color=(0, 1, 0.5))
                    bui.getsound('cashRegister').play()
                else:
                    bui.screenmessage('Failed to send invite.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _message_friend(self, friend: dict) -> None:
        fid = friend.get('friend_id')
        nick = friend.get('friend_nickname', '?')
        set_dm_chat_target({'type': 'friend', 'friend_id': fid, 'friend_nickname': nick})
        DMWindow()

    def _view_friend_account(self, friend: dict) -> None:
        FriendAccountPopup(friend=friend)

    def close(self) -> None:
        self._window_open = False
        self._party_check_timer = None
        self._unsubscribe_all_changes()
        super().close()

    def close_with_sound(self) -> None:
        self._window_open = False
        self._party_check_timer = None
        self._unsubscribe_all_changes()
        super().close_with_sound()


class _FriendPickerWindow(PopupWindow):
    """Scrollable friend list popup anchored to button3."""

    def __init__(self, friends: list, position: tuple, on_select) -> None:
        self._on_select = on_select
        bg = _global_theme.get_color('COLOR_BUTTON')
        txt_color = _global_theme.get_color('COLOR_PRIMARY')

        row_h = 26
        icon_size = 18
        width = 130
        pad = 4
        max_visible = 6
        visible = min(len(friends), max_visible)
        height = visible * row_h + pad * 2 + 10

        super().__init__(
            position=position,
            size=(width, height),
            bg_color=bg,
            scale=_get_popup_window_scale(),
        )

        scroll = bui.scrollwidget(
            parent=self.root_widget,
            position=(pad, pad),
            size=(width - pad * 2, height - pad * 2),
            border_opacity=0.0,
            color=_global_theme.get_color('COLOR_ACCENT'),
        )

        container_h = len(friends) * row_h
        container = bui.containerwidget(
            parent=scroll,
            size=(width - pad * 2 - 20, container_h),
            background=False,
        )

        y = container_h - row_h - 2
        txt_w = width - pad * 2 - 20 - icon_size - 6
        online_ids = get_online_friend_ids()
        local_user_id = get_session().get('user', {}).get('id')
        accent_color = _global_theme.get_color('COLOR_ACCENT')
        for friend in friends:
            nick = friend.get('friend_nickname', '?')
            display = nick[:5] + '...' if len(nick) > 5 else nick
            is_online = friend.get('friend_id') in online_ids
            is_me = local_user_id is not None and friend.get('friend_id') == local_user_id

            bui.imagewidget(
                parent=container,
                position=(2, y + (row_h - icon_size) // 2),
                size=(icon_size, icon_size),
                texture=bui.gettexture('cuteSpaz'),
            )

            _dot_size = 10
            _dot_cx = 2 + icon_size - 4
            _dot_cy = y + (row_h - icon_size) // 2 + 4
            bui.imagewidget(
                parent=container,
                position=(_dot_cx - _dot_size // 2, _dot_cy - _dot_size // 2),
                size=(_dot_size, _dot_size),
                texture=bui.gettexture('circle'),
                color=(0.2, 0.85, 0.2) if is_online else (0.35, 0.35, 0.35),
            )

            bui.textwidget(
                parent=container,
                position=(icon_size, y + row_h / 2 - 13),
                size=(txt_w, row_h),
                text=display,
                scale=0.85,
                maxwidth=txt_w,
                color=accent_color if is_me else txt_color,
                h_align='left',
                v_align='center',
                selectable=True,
                click_activate=True,
                autoselect=True,
                on_activate_call=lambda f=friend: self._select(f),
            )
            y -= row_h

    def _select(self, friend: dict) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        self._on_select(friend)

    def on_popup_cancel(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')


class _FriendActionWindow(PopupWindow):
    """Action menu for a selected friend."""

    def __init__(self, friend: dict, position: tuple,
                 is_online: bool, on_invite, on_message, on_account) -> None:
        bg = _global_theme.get_color('COLOR_SECONDARY')
        txt_color = _global_theme.get_color('COLOR_PRIMARY')
        disabled_color = (0.38, 0.38, 0.38)

        row_h = 26
        width = 160

        actions = [
            (get_lang_text('FriendAction.inviteToParty'), on_invite, True),
            (get_lang_text('FriendAction.sendMessage'), on_message, True),
            (get_lang_text('FriendAction.viewAccount'), on_account, False),
        ]
        height = len(actions) * row_h + 8

        super().__init__(
            position=position,
            size=(width, height),
            bg_color=bg,
            scale=_get_popup_window_scale(),
        )

        y = height - row_h - 8
        for label, cb, needs_online in actions:
            enabled = not needs_online or is_online
            kw: dict = {}
            if enabled:
                kw = {
                    'selectable': True,
                    'click_activate': True,
                    'autoselect': True,
                    'on_activate_call': lambda c=cb: self._act(c),
                }
            bui.textwidget(
                parent=self.root_widget,
                position=(-4, y + row_h / 2 - 4),
                size=(width - 8, row_h),
                text=label,
                scale=0.8,
                maxwidth=width - 20,
                color=txt_color if enabled else disabled_color,
                h_align='left',
                v_align='center',
                **kw,
            )
            y -= row_h

    def _act(self, callback) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        callback()

    def on_popup_cancel(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')


class GatherModified(GatherWindow):
    """GatherWindow opened from the party window buttons."""

    _patched: bool = False
    _filter_frozen: bool = False
    _filter_hide_full: bool = False
    _filter_hide_empty: bool = False
    _filter_only_empty: bool = False

    # Saved originals so we can unpatch if needed
    _orig_clear: object = None
    _orig_update: object = None
    _orig_build_join: object = None
    _orig_update_lists: object = None

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
        from_party: bool = False,
    ) -> None:
        if not GatherModified._patched:
            GatherModified._patched = True
            self._patch_public_tab()

        super().__init__(transition=transition, origin_widget=origin_widget)

        if from_party:
            uiscale = bui.app.ui_v1.uiscale
            if uiscale is bui.UIScale.SMALL:
                bui.containerwidget(
                    edit=self._root_widget,
                    on_cancel_call=self._on_back,
                )
            elif self._back_button is not None and self._back_button.exists():
                bui.buttonwidget(
                    edit=self._back_button,
                    on_activate_call=self._on_back,
                )

    @staticmethod
    def _patch_public_tab() -> None:
        """PublicGatherTab and UIRow once at first open."""
        from bauiv1lib.gather.publictab import PublicGatherTab, UIRow

        _orig_clear = UIRow._clear
        _orig_update = UIRow.update
        GatherModified._orig_clear = _orig_clear
        GatherModified._orig_update = _orig_update

        def _peek_open(address: str, port: int, name: str, btn: bui.Widget) -> None:
            if btn.exists():
                ServerViewOverlay(
                    address=address, port=port,
                    source_widget=btn, name=name,
                )

        def _truncate(text: str) -> str:
            uiscale = bui.app.ui_v1.uiscale
            if uiscale is bui.UIScale.SMALL:
                limit = 22
            elif uiscale is bui.UIScale.MEDIUM:
                limit = 26
            else:
                limit = 30
            return text if len(text) <= limit else text[:limit] + '...'

        def patched_clear(self_row: UIRow) -> None:
            _orig_clear(self_row)
            w = getattr(self_row, '_peek_button', None)
            if w is not None and w.exists():
                w.delete()
            self_row._peek_button = None

        def patched_update(
            self_row: UIRow,
            index: int,
            party,
            sub_scroll_width: float,
            sub_scroll_height: float,
            lineheight: float,
            columnwidget: bui.Widget,
            join_text: bui.Widget,
            filter_text: bui.Widget,
            existing_selection,
            tab: PublicGatherTab,
        ) -> None:
            needs_update = party.clean_display_index != index
            # Truncate name before passing to original renderer
            original_name = party.name
            party.name = _truncate(original_name)
            _orig_update(
                self_row, index, party, sub_scroll_width, sub_scroll_height,
                lineheight, columnwidget, join_text, filter_text,
                existing_selection, tab,
            )
            party.name = original_name
            if not needs_update:
                return

            vpos = sub_scroll_height - lineheight * index - 50

            peek_btn = bui.buttonwidget(
                color=(0.5, 0.4, 0.93),
                textcolor=(1.0, 1.0, 1.0),
                label=get_lang_text('RecentServers.peek'),
                parent=columnwidget,
                autoselect=True,
                size=(90, 40),
                position=(sub_scroll_width - 375.0, 1 + vpos),
                scale=0.9,
            )
            bui.buttonwidget(
                edit=peek_btn,
                on_activate_call=bui.CallStrict(
                    _peek_open, party.address, party.port, party.name, peek_btn
                ),
            )
            bui.widget(edit=peek_btn, allow_preserve_selection=False)
            self_row._peek_button = peek_btn

        UIRow._clear = patched_clear
        UIRow.update = patched_update

        _orig_build_join = PublicGatherTab._build_join_tab
        GatherModified._orig_build_join = _orig_build_join

        def patched_build_join_tab(
            self_tab: PublicGatherTab,
            region_width: float,
            region_height: float,
        ) -> None:
            _orig_build_join(self_tab, region_width, region_height)
            c_height = region_height - 20
            v = c_height - 95
            bui.buttonwidget(
                parent=self_tab._container,
                label=get_lang_text('gatherFilterBtn'),
                size=(110, 40),
                position=(region_width * 0.5 + 210, v - 10),
                on_activate_call=lambda: FilterWindow(self_tab),
                autoselect=True,
                color=(0.5, 0.35, 0.8),
                textcolor=(1.0, 1.0, 1.0),
                text_scale=0.75,
            )

        PublicGatherTab._build_join_tab = patched_build_join_tab

        _orig_update_lists = PublicGatherTab._update_party_lists
        GatherModified._orig_update_lists = _orig_update_lists

        def patched_update_lists(self_tab: PublicGatherTab) -> None:
            if GatherModified._filter_frozen:
                return
            _orig_update_lists(self_tab)
            if GatherModified._filter_hide_full:
                self_tab._parties_displayed = {
                    k: v for k, v in self_tab._parties_displayed.items()
                    if v.size < v.size_max
                }
            if GatherModified._filter_hide_empty:
                self_tab._parties_displayed = {
                    k: v for k, v in self_tab._parties_displayed.items()
                    if v.size > 0
                }
            if GatherModified._filter_only_empty:
                self_tab._parties_displayed = {
                    k: v for k, v in self_tab._parties_displayed.items()
                    if v.size == 0
                }

        PublicGatherTab._update_party_lists = patched_update_lists

    @staticmethod
    def _unpatch_public_tab() -> None:
        """Restore original PublicGatherTab and UIRow methods."""
        if not GatherModified._patched:
            return
        from bauiv1lib.gather.publictab import PublicGatherTab, UIRow
        if GatherModified._orig_clear is not None:
            UIRow._clear = GatherModified._orig_clear
        if GatherModified._orig_update is not None:
            UIRow.update = GatherModified._orig_update
        if GatherModified._orig_build_join is not None:
            PublicGatherTab._build_join_tab = GatherModified._orig_build_join
        if GatherModified._orig_update_lists is not None:
            PublicGatherTab._update_party_lists = GatherModified._orig_update_lists
        GatherModified._patched = False

    def _on_back(self) -> None:
        # Restore original GatherWindow and patches if the user hasn't enabled it globally.
        from _bampui.lparty import set_global_gather_modified
        if not finder_config.get(CFG_NAME_GLOBAL_GATHER, False):
            set_global_gather_modified(False)
            GatherModified._unpatch_public_tab()
        self._save_state()
        try:
            bui.containerwidget(
                edit=self._root_widget,
                transition=self._main_window_transition_out,
            )
            root = self.get_root_widget()
            if root is not None:
                babase.apptimer(0.5, root.delete)
        except Exception:
            try:
                self.main_window_back()
            except Exception:
                pass


class FilterWindow:
    """Popup to filter the public server list."""

    def __init__(self, tab: object) -> None:
        from bauiv1lib.gather.publictab import PublicGatherTab
        self._tab: PublicGatherTab = tab  # type: ignore[assignment]

        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.8 if uiscale is bui.UIScale.SMALL else
            1.3 if uiscale is bui.UIScale.MEDIUM else 1.0
        )

        w, h = 300, 260
        self._root = bui.containerwidget(
            size=(w, h),
            scale=scale,
            transition='in_scale',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
        )

        bui.textwidget(
            parent=self._root,
            position=(w * 0.5, h - 24),
            size=(0, 0),
            text=get_lang_text('gatherFilterTitle'),
            scale=0.9,
            color=(1.0, 1.0, 0.8),
            h_align='center',
            v_align='center',
            maxwidth=w - 20,
        )

        x = w * 0.08
        v = h - 80
        step = 46

        chk_maxwidth = w * 0.78

        self._freeze_chk = bui.checkboxwidget(
            parent=self._root,
            text=get_lang_text('gatherFilterFreeze'),
            position=(x, v),
            size=(w * 0.85, 32),
            autoselect=True,
            color=(0.6, 0.6, 0.6),
            textcolor=(0.9, 0.9, 0.9),
            maxwidth=chk_maxwidth,
            value=GatherModified._filter_frozen,
            on_value_change_call=self._toggle_freeze,
        )
        v -= step

        self._full_chk = bui.checkboxwidget(
            parent=self._root,
            text=get_lang_text('gatherFilterHideFull'),
            position=(x, v),
            size=(w * 0.85, 32),
            autoselect=True,
            color=(0.6, 0.6, 0.6),
            textcolor=(0.9, 0.9, 0.9),
            maxwidth=chk_maxwidth,
            value=GatherModified._filter_hide_full,
            on_value_change_call=self._toggle_hide_full,
        )
        v -= step

        self._empty_chk = bui.checkboxwidget(
            parent=self._root,
            text=get_lang_text('gatherFilterHideEmpty'),
            position=(x, v),
            size=(w * 0.85, 32),
            autoselect=True,
            color=(0.6, 0.6, 0.6),
            textcolor=(0.9, 0.9, 0.9),
            maxwidth=chk_maxwidth,
            value=GatherModified._filter_hide_empty,
            on_value_change_call=self._toggle_hide_empty,
        )
        v -= step

        self._only_empty_chk = bui.checkboxwidget(
            parent=self._root,
            text=get_lang_text('gatherFilterOnlyEmpty'),
            position=(x, v),
            size=(w * 0.85, 32),
            autoselect=True,
            color=(0.6, 0.6, 0.6),
            textcolor=(0.9, 0.9, 0.9),
            maxwidth=chk_maxwidth,
            value=GatherModified._filter_only_empty,
            on_value_change_call=self._toggle_only_empty,
        )

    def _toggle_freeze(self, val: bool) -> None:
        GatherModified._filter_frozen = val

    def _toggle_hide_full(self, val: bool) -> None:
        GatherModified._filter_hide_full = val
        self._tab._party_lists_dirty = True

    def _toggle_hide_empty(self, val: bool) -> None:
        GatherModified._filter_hide_empty = val
        if val:
            GatherModified._filter_only_empty = False
            bui.checkboxwidget(edit=self._only_empty_chk, value=False)
        self._tab._party_lists_dirty = True

    def _toggle_only_empty(self, val: bool) -> None:
        GatherModified._filter_only_empty = val
        if val:
            GatherModified._filter_hide_empty = False
            bui.checkboxwidget(edit=self._empty_chk, value=False)
        self._tab._party_lists_dirty = True

    def _close(self) -> None:
        if self._root.exists():
            bui.containerwidget(edit=self._root, transition='out_scale')


class ServerViewOverlay:
    """Popup overlay to peek at a server's player list before joining."""

    def __init__(
        self,
        address: str,
        port: int,
        source_widget: bui.Widget,
        name: str = '',
    ) -> None:
        self._address = address
        self._port = port
        self._scanning = False
        self._row_widgets: list[bui.Widget] = []

        bg = _global_theme.get_color('COLOR_BACKGROUND')
        btn_color = _global_theme.get_color('COLOR_BUTTON')
        text_color = _global_theme.get_color('COLOR_PRIMARY')
        secondary_color = _global_theme.get_color('COLOR_SECONDARY')

        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.3 if uiscale is bui.UIScale.SMALL else
            1.0 if uiscale is bui.UIScale.MEDIUM else 0.85
        )

        self._w, self._h = 360, 290

        self._root = bui.containerwidget(
            size=(self._w, self._h),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=scale,
            color=bg,
            scale_origin_stack_offset=source_widget.get_screen_space_center(),
        )

        # Server name title
        bui.textwidget(
            parent=self._root,
            position=(self._w * 0.5, self._h - 20),
            size=(0, 0),
            text=name or address,
            scale=1.0,
            color=text_color,
            h_align='center',
            v_align='center',
            maxwidth=self._w - 16,
        )

        # IP:port subtitle
        bui.textwidget(
            parent=self._root,
            position=(self._w * 0.5, self._h - 44),
            size=(0, 0),
            text=f'{address}:{port}',
            scale=0.7,
            color=secondary_color,
            h_align='center',
            v_align='center',
        )

        # Status
        self._status_txt = bui.textwidget(
            parent=self._root,
            position=(self._w * 0.5, self._h - 66),
            size=(0, 0),
            text=get_lang_text('RecentServers.scanning'),
            scale=0.72,
            color=secondary_color,
            h_align='center',
            v_align='center',
            maxwidth=self._w - 16,
        )

        # Player list scroll
        scroll_h = self._h - 130
        self._scroll = bui.scrollwidget(
            parent=self._root,
            position=(5, 42),
            size=(self._w - 10, scroll_h),
            border_opacity=0.3,
        )
        self._container = bui.containerwidget(
            parent=self._scroll,
            size=(self._w - 30, 10),
            background=False,
        )

        # Connect button
        self._connect_btn = bui.buttonwidget(
            parent=self._root,
            position=(self._w * 0.5 - 70, 6),
            size=(140, 32),
            label=get_lang_text('RecentServers.join'),
            text_scale=0.75,
            autoselect=True,
            color=btn_color,
            textcolor=text_color,
            on_activate_call=self._do_connect,
        )

        self._start_scan()

    def _start_scan(self) -> None:
        if self._scanning:
            return
        self._scanning = True
        self._clear_rows()
        Thread(
            target=self._scan_thread,
            args=(self._address, self._port),
            daemon=True,
        ).start()

    def _scan_thread(self, addr: str, port: int) -> None:
        ping, roster = ping_and_get_roster(addr, port)
        babase.pushcall(
            lambda: self._on_scan_done(ping, roster),
            from_other_thread=True,
        )

    def _on_scan_done(self, ping: float | int, roster: list) -> None:
        if not self._root.exists():
            return
        self._scanning = False
        if ping == 999 or ping is None:
            bui.textwidget(
                edit=self._status_txt,
                text=get_lang_text('RecentServers.noResponse'),
                color=(1.0, 0.4, 0.4),
            )
            return
        players = [
            self._parse_spec_name(e.get('spec', ''))
            for e in roster
        ]
        players = [n for n in players if n and n not in ('Finder', 'Server')]
        count = len(players)
        bui.textwidget(
            edit=self._status_txt,
            text=f'{round(ping)}ms  ·  {count} player{"s" if count != 1 else ""}',
            color=(0.4, 1.0, 0.5),
        )
        self._build_rows(players)

    def _build_rows(self, players: list[str]) -> None:
        self._clear_rows()
        if not players:
            scroll_h = self._h - 130
            w = bui.textwidget(
                parent=self._root,
                position=(self._w * 0.5, 42 + scroll_h * 0.4),
                size=(0, 0),
                text=get_lang_text('RecentServers.noPlayers'),
                scale=0.85,
                color=(1.0, 0.8, 0.3),
                h_align='center',
                v_align='center',
            )
            self._row_widgets.append(w)
            return
        row_h = 38
        icon_size = 26
        ctn_h = max(len(players) * row_h + 10, 10)
        bui.containerwidget(edit=self._container, size=(self._w - 30, ctn_h))
        y = ctn_h - row_h - 4
        for name in players:
            icon = bui.imagewidget(
                parent=self._container,
                position=(28, y + (row_h - icon_size) / 2 + 5),
                size=(icon_size, icon_size),
                texture=bui.gettexture('cuteSpaz'),
            )
            self._row_widgets.append(icon)
            txt = bui.textwidget(
                parent=self._container,
                position=(15, y + row_h / 2 - 14),
                size=(self._w - 50, row_h),
                text=name,
                maxwidth=self._w - 60,
                scale=0.75,
                h_align='left',
                v_align='center',
                color=(0.95, 0.95, 0.95),
            )
            self._row_widgets.append(txt)
            y -= row_h

    def _parse_spec_name(self, spec_str: str) -> str:
        import re
        from json import loads, JSONDecodeError
        if not spec_str:
            return ''
        try:
            return loads(spec_str).get('n', '')
        except (JSONDecodeError, Exception):
            m = re.search(r'"n"\s*:\s*"([^"]*)"', spec_str)
            return m.group(1) if m else ''

    def _do_connect(self) -> None:
        from bascenev1 import connect_to_party
        connect_to_party(self._address, self._port, False)
        self._close()

    def _clear_rows(self) -> None:
        for w in self._row_widgets:
            if w.exists():
                w.delete()
        self._row_widgets.clear()
        bui.containerwidget(edit=self._container, size=(self._w - 30, 10))

    def _close(self) -> None:
        if self._root.exists():
            bui.containerwidget(edit=self._root, transition='out_scale')


def ping_and_get_roster(
    address: str,
    port: int,
    ping_wait: float = 0.3,
    timeout: float = 3.5,
    pro: list | None = None,
    dex=None,
) -> tuple:
    """Ping a server via UDP and retrieve its player roster.

    Returns (ping_ms, roster_list). Returns (999, []) on failure.
    """
    if pro is None:
        pro = []

    ping_result = None
    roster_result = None
    sock = None

    try:
        sock = socket.socket(IPT(address), socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        ping_start = time.time()
        ping_ok = False
        for _ in range(3):
            try:
                sock.sendto(b'\x0b', (address, port))
                data, addr = sock.recvfrom(10)
                if data == b'\x0c' and addr[0] == address:
                    ping_ok = True
                    break
            except Exception:
                break
            time.sleep(ping_wait)

        if not ping_ok:
            pro.append((dex, 999))
            return (999, [])

        ping_result = (time.time() - ping_start) * 1000

        json_enc = lambda h: dumps(h).encode('utf-8')
        hex_bytes = lambda h: bytes.fromhex(h.replace(' ', ''))
        send = lambda h, e=b'': sock.sendto(hex_bytes(h) + e, (address, port))
        recv = lambda b: sock.recvfrom(b)[0]

        my_hs = f'{(71 + randint(0, 150)):02x}'
        send(f'18 21 00 {my_hs}', _babase.app_instance_uuid().encode())
        srv_hs = f'{recv(3)[1]:02x}'
        recv(1024)

        send(f'24 {srv_hs} 10 21 00', json_enc(FinderWindow.SPEC))
        send(f'24 {srv_hs} 11 f0 ff f0 ff 00 12', json_enc(FinderWindow.AUTH))
        send(f'24 {srv_hs} 11 f1 ff f0 ff 00 15', json_enc({}))
        send(f'24 {srv_hs} 11 f2 ff f0 ff 00 03')

        recv(1024)
        recv(9)

        SRM = 0x25
        BSP = 0x11
        MMP = 0x0d
        MME = 0x0e
        MPR = 0x09

        parts = bytearray()
        collecting = False
        listen_start = time.time()

        while time.time() - listen_start < timeout / 2:
            pkt = recv(2048)
            if not pkt or len(pkt) < 9:
                continue
            if pkt[0] == SRM and pkt[2] == BSP:
                ptype = pkt[8]
                pdata = pkt[9:]
                if ptype == MPR:
                    roster_result = loads(pdata.rstrip(b'\x00').decode('utf-8'))
                    break
                elif ptype == MMP:
                    if pdata and pdata[0] == MPR:
                        collecting = True
                        parts = bytearray(pdata[1:])
                    elif collecting:
                        parts.extend(pdata)
                elif ptype == MME and collecting:
                    parts.extend(pdata)
                    roster_result = loads(parts.rstrip(b'\x00').decode('utf-8'))
                    break

        send(f'20 {srv_hs}')

    except Exception:
        pass
    finally:
        if sock is not None:
            sock.close()

    pro.append((dex, ping_result))
    return (ping_result, roster_result or [])


class FinderWindow:
    """Less Finder - server scanner and player finder."""

    SPEC = {'s': '{"n":"Finder","a":"","sn":""}', 'd': '69' * 20}
    AUTH = {'b': APP.env.engine_build_number, 'tk': '', 'ph': ''}

    MAX_PING = 0.3
    TOP_SERVERS = 1
    SERVER_MEMORY: list = []
    ART_DISPLAY: list = []
    BEST_SERVERS: list = []
    IS_SCANNING = False
    SERVER_LIST_ELEMENTS: list = []
    PLAYERS_LIST: list = []
    ART_DISPLAY_WIDGET = None
    SCROLL_WIDGET = None
    TIP_WIDGET = None
    FILTER_TEXT = ''
    FILTER_TEXT_WIDGET = None
    FILTER_UPDATER = None
    SHOWING_SERVER_ART = False
    SHOWING_SERVER_INFO = False
    _instances: list = []

    def __init__(self, source, party_window=None) -> None:
        self._party_window = party_window
        self.language = language
        self.theme = theme
        self.theme.refresh_from_config()
        self._current_selected_player = None
        self._current_displayed_player = None
        self.scan_threads: list = []
        self.info_elements: list = []
        self.progress_trackers: list = []
        self.status_updater = None
        self.background_sound = self._play_sound('powerup01')
        self.default_tip_text = ''
        self._popup_type: str | None = None

        # Friends panel state
        self.best_friends_connected = 0
        self._current_displayed_best_friend = None
        self._popup_target = None
        self.friends_parent = None
        self.friends_separator = None
        self.all_friends_text = None
        self.friend_input = None
        self.add_manual_button = None
        self.friends_separator2 = None
        self.online_friends_text = None
        self._friends_scroll_container = None
        self._friends_list_container = None
        self._connected_friends_scroll_container = None
        self._connected_friends_list_container = None
        self._friend_info_container = None
        self.friend_info_tip = None
        self.no_friends_online_text = None
        self.best_friends_elements: list = []
        self._friend_text_widgets: list = []
        self._connected_friend_text_widgets: list = []

        FinderWindow._instances.append(self)

        cls = self.__class__
        window_size = (815, 485)

        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.3 if uiscale is babase.UIScale.SMALL else
            1.0 if uiscale is babase.UIScale.MEDIUM else 0.9
        )
        cls.root = bui.containerwidget(
            size=window_size,
            color=self.theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=zw('overlay_stack'),
            on_outside_click_call=self.close_interface,
            scale=scale,
            scale_origin_stack_offset=source.get_screen_space_center(),
        )

        cls.MainParent = ocw(
            position=(0, 0), parent=cls.root,
            size=(460, 485), background=False
        )

        self._create_friends_panel(cls.root)

        obw(
            parent=cls.root,
            position=(19, 410),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self.close_interface,
        )

        obw(
            parent=cls.MainParent,
            label=self.language.get_text('FinderWindow.searchProfiles'),
            icon=gt('cuteSpaz'),
            iconscale=0.9,
            size=(135, 38), position=(53, 405),
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            text_scale=0.75,
            on_activate_call=self._search_profiles,
        )

        self.search_servers_text = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.searchServers'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(19, 374), maxwidth=320, max_height=28,
        )

        self.search_button = obw(
            parent=cls.MainParent, position=(360, 358),
            size=(80, 39), text_scale=0.7,
            label=self.language.get_text('Global.search'),
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self.start_server_scan
        )

        self.search_players_text = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.searchPlayers'),
            color=self.theme.get_color('COLOR_TERTIARY'),
            scale=0.8, position=(15, 345), maxwidth=320, max_height=28,
        )

        iw(
            parent=cls.MainParent, size=(429, 1), position=(17, 345),
            texture=gt('white'), color=self.theme.get_color('COLOR_SECONDARY')
        )

        cls.ART_DISPLAY_WIDGET = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.pressSearch'),
            maxwidth=430, max_height=125,
            h_align='center', v_align='top',
            color=self.theme.get_color('COLOR_PRIMARY'), position=(205, 275),
        )

        iw(
            parent=cls.MainParent, size=(429, 1), position=(17, 215),
            texture=gt('white'), color=self.theme.get_color('COLOR_SECONDARY')
        )

        cls.FILTER_TEXT_WIDGET = tw(
            parent=cls.MainParent, position=(23, 165),
            size=(201, 35), text=cls.FILTER_TEXT,
            editable=True, glow_type='uniform', allow_clear_button=False,
            v_align='center', color=self.theme.get_color('COLOR_PRIMARY'),
            description=get_lang_text('FinderWindow.filterDescription')
        )

        self.filter_placeholder = tw(
            parent=cls.MainParent, position=(26, 168),
            text=get_lang_text('Global.search'),
            maxwidth=80, max_height=25,
            color=self.theme.get_color('COLOR_TERTIARY')
        )

        self.players_parent = sw(
            parent=cls.MainParent, position=(20, 33),
            size=(205, 122), border_opacity=0.4,
            color=self.theme.get_color('COLOR_ACCENT')
        )

        cls.MainParent2 = ocw(
            parent=self.players_parent, size=(205, 1), background=False
        )

        self.players_tip = tw(
            parent=cls.MainParent, position=(90, 115),
            text=self.language.get_text('FinderWindow.searchServersForPlayers'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=175, max_height=100, h_align='center'
        )

        iw(
            parent=cls.MainParent, position=(235, 33),
            size=(205, 172), texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'), opacity=0.4
        )

        cls.TIP_WIDGET = tw(
            parent=cls.MainParent, position=(310, 113),
            text=self.language.get_text('FinderWindow.selectToViewInfo'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=170, max_height=100, h_align='center'
        )

        if cls.ART_DISPLAY:
            self._draw_art()
        self._update_players_list()
        if cls.SCROLL_WIDGET:
            self._display_server_info(cls.SCROLL_WIDGET)
        cls.FILTER_UPDATER = tuck(0.1, self._update_filter, repeat=True)

    @classmethod
    def refresh_friends_lists(cls) -> None:
        """Refresh friends UI in all active FinderWindow instances."""
        active = [
            inst for inst in cls._instances
            if (hasattr(inst, 'friends_parent') and
                inst.friends_parent and
                inst.friends_parent.exists())
        ]
        for inst in active:
            try:
                inst.refresh_best_friends_ui()
                try:
                    players = [V2_LOGO + p.strip()
                               for p, _ in inst._get_filtered_players()]
                except Exception as e:
                    print(f'[FinderWindow] Could not get players list: {e}')
                    players = []
                inst.refresh_best_friends_connected_ui(players)
            except Exception as e:
                print(f'[FinderWindow] Error refreshing friends: {e}')

    def _update_filter(self) -> None:
        cls = self.__class__
        if not self.filter_placeholder.exists():
            cls.FILTER_UPDATER = None
            return
        current = tw(query=cls.FILTER_TEXT_WIDGET)
        search = get_lang_text('Global.search')
        tw(self.filter_placeholder, text=('' if current else search))
        if current != cls.FILTER_TEXT:
            cls.FILTER_TEXT = current
            self._update_players_list()

    def _on_server_select(self, index: int, player_name: str) -> None:
        cls = self.__class__
        cls.SCROLL_WIDGET = player_name
        self._current_selected_player = player_name
        for i, el in enumerate(cls.SERVER_LIST_ELEMENTS):
            if el and el.exists():
                color = (self.theme.get_color('COLOR_PRIMARY') if i == index
                         else self.theme.get_color('COLOR_TERTIARY'))
                tw(edit=el, color=color)
        self._display_server_info(player_name)

    def _display_server_info(self, player_name: str) -> None:
        for el in self.info_elements:
            el.delete()
        self.info_elements.clear()
        cls = self.__class__
        tw(cls.TIP_WIDGET, text='')
        cls.SHOWING_SERVER_INFO = True
        self._current_displayed_player = player_name

        server_info = player_data = None
        for server in cls.SERVER_MEMORY:
            for entry in server.get('roster', []):
                spec = self._safe_load_spec(entry.get('spec', ''))
                if spec and spec.get('n') == player_name:
                    server_info = server
                    player_data = entry['p']
                    break
            if server_info:
                break

        if server_info is None:
            cls.SCROLL_WIDGET = None
            cls.SHOWING_SERVER_INFO = False
            tw(cls.TIP_WIDGET, text=self.default_tip_text)
            self._current_displayed_player = None
            return

        for i, key in enumerate(['n', 'a', 'p']):
            field_text = str(server_info[key])
            pos_x = [250, 245, 375][i]
            pos_y = [170, 130][bool(i)]
            size_x = [175, 115, 55][i]
            w = tw(
                parent=cls.MainParent,
                position=(pos_x, pos_y),
                h_align='center', v_align='center',
                maxwidth=size_x, text=field_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(size_x, 30), selectable=True,
                click_activate=True, glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, field_text)
            )
            self.info_elements.append(w)

        account_v2 = [str(list(p.values())[1]) for p in player_data]

        account_btn = obw(
            parent=cls.MainParent, position=(253, 80),
            size=(170, 30),
            label=(str(account_v2[0]) if account_v2 and account_v2[0] != []
                   else player_name),
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=CallStrict(self._show_notification,
                           '\n'.join([' | '.join([str(j) for j in p.values()])
                                      for p in player_data]) or 'Nothing')
        )
        self.info_elements.append(account_btn)

        connect = get_lang_text('Global.connect')
        if account_v2 and str(account_v2[0]).startswith(V2_LOGO):
            c_btn = obw(
                parent=cls.MainParent, position=(250, 45),
                size=(80, 30), label=connect,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                on_activate_call=CallStrict(self._connect, server_info['a'], server_info['p'], server_info.get('n', ''))
            )
            self.info_elements.append(c_btn)

            af_btn = obw(
                parent=cls.MainParent, position=(340, 45),
                size=(87, 30), label=get_lang_text('FriendsWindow.addFriend'),
                text_scale=0.5,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                on_activate_call=CallStrict(lambda: (
                    self._add_friend(player_name),
                    self._update_friends_panel()
                ))
            )
            self.info_elements.append(af_btn)
        else:
            c_btn = obw(
                parent=cls.MainParent, position=(253, 45),
                size=(170, 30), label=connect,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                on_activate_call=CallStrict(self._connect, server_info['a'], server_info['p'], server_info.get('n', ''))
            )
            self.info_elements.append(c_btn)

    def _update_friends_panel(self) -> None:
        self.refresh_best_friends_ui()
        players = [V2_LOGO + p.strip() for p, _ in self._get_filtered_players()]
        self.refresh_best_friends_connected_ui(players)
        pass

    def _show_options_popup(self, source_button) -> None:
        self._popup_type = 'options'
        PopupMenuWindow(
            position=source_button.get_screen_space_center(),
            choices=['search_profiles', 'credits'],
            choices_display=[
                babase.Lstr(value=get_lang_text('FinderWindow.searchProfiles')),
                babase.Lstr(value=get_lang_text('Global.credits')),
            ],
            current_choice='search_profiles',
            delegate=self,
        )

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        if self._popup_type == 'friend':
            friend = self._popup_target
            if choice == 'view_profile':
                self._open_profile(friend)
            elif choice == 'delete_friend':
                self._delete_friend(friend)
                self.refresh_best_friends_ui()
                self.refresh_best_friends_connected_ui()
                self._show_friend_info_tip()
            return
        if self._popup_type != 'options':
            return
        if choice == 'search_profiles':
            self._search_profiles()
        elif choice == 'credits':
            self._credits()

    def _search_profiles(self) -> None:
        cls = self.__class__
        source = (cls.root if hasattr(cls, 'root') and cls.root.exists()
                  else zw('overlay_stack'))
        ProfileSearch(source)

    def _credits(self) -> None:
        cls = self.__class__
        source = (cls.root if hasattr(cls, 'root') and cls.root.exists()
                  else zw('overlay_stack'))
        CreditsWindow(source)

    def _generate_theme_from_color(self, base_color: tuple) -> dict:
        def adj(c, f):
            return tuple(max(0.0, min(1.0, x * f)) for x in c)
        b = tuple(base_color)
        return {
            CFG_NAME_COLOR_BACKGROUND: (0.1, 0.1, 0.1),
            CFG_NAME_COLOR_SECONDARY: (0.2, 0.2, 0.2),
            CFG_NAME_COLOR_TERTIARY: adj(b, 0.6),
            CFG_NAME_COLOR_PRIMARY: b,
            CFG_NAME_COLOR_ACCENT: adj(b, 1.2),
        }

    def _create_color_picker(self, position, initial_color, call) -> None:
        self._initial_picker_color = initial_color
        self._color_changed = False
        return colorpicker.ColorPicker(
            parent=self.root, position=position,
            initial_color=initial_color, delegate=self, tag=call,
        )

    def _save_colors_to_config(self, colors: dict) -> None:
        for k, v in colors.items():
            finder_config[k] = tuple(v)
        save_finder_config(finder_config)
        self.theme.update_colors({
            'COLOR_BACKGROUND': tuple(finder_config.get(CFG_NAME_COLOR_BACKGROUND)),
            'COLOR_SECONDARY': tuple(finder_config.get(CFG_NAME_COLOR_SECONDARY)),
            'COLOR_TERTIARY': tuple(finder_config.get(CFG_NAME_COLOR_TERTIARY)),
            'COLOR_PRIMARY': tuple(finder_config.get(CFG_NAME_COLOR_PRIMARY)),
            'COLOR_ACCENT': tuple(finder_config.get(CFG_NAME_COLOR_ACCENT)),
        })

    def color_picker_selected_color(self, picker, color) -> None:
        if color != self._initial_picker_color:
            self._color_changed = True
            self._save_colors_to_config(self._generate_theme_from_color(color))

    def color_picker_closing(self, picker) -> None:
        if self._color_changed:
            push('Colors updated successfully!', self.theme.get_color('COLOR_TERTIARY'))

    def popup_menu_closing(self, popup_window) -> None:
        self._popup_target = None

    def on_popup_cancel(self) -> None:
        pass

    def _show_notification(self, text: str) -> None:
        push(text, self.theme.get_color('COLOR_TERTIARY'))
        self._play_ding_sound(1, 1)

    def _copy_to_clipboard(self, text: str) -> None:
        self._play_ding_sound(1, 1)
        push(get_lang_text('Global.copiedToClipboard'), self.theme.get_color('COLOR_TERTIARY'))
        COPY(text)

    def _get_filtered_players(self) -> list:
        player_list = []
        cls = self.__class__
        for server in cls.SERVER_MEMORY:
            roster = server.get('roster', {})
            if not roster:
                continue
            for player in roster:
                spec = self._safe_extract_player_spec(player)
                if not spec:
                    continue
                if (spec == 'Finder' or
                        (cls.FILTER_TEXT and
                         not self._check_server_against_filter(roster))):
                    continue
                player_list.append((spec, server['a']))
        return sorted(player_list, key=lambda x: x[0].startswith('Server'))

    def _safe_extract_player_spec(self, player_data: dict):
        try:
            spec_str = player_data.get('spec', '')
            if not spec_str:
                return None
            try:
                return loads(spec_str).get('n', '')
            except JSONDecodeError:
                m = re.search(r'"n"\s*:\s*"([^"]*)"', spec_str)
                if m:
                    return m.group(1)
                m = re.search(r'"name"\s*:\s*"([^"]*)"', spec_str)
                return m.group(1) if m else None
        except Exception as e:
            print(f'Safe error extracting player spec: {e}')
            return None

    def _check_server_against_filter(self, roster: list) -> bool:
        ft = self.__class__.FILTER_TEXT.lower()
        for player in roster:
            name = self._safe_extract_player_spec(player)
            if name and name != 'Finder' and ft in name.lower():
                return True
            for profile in player.get('p', []):
                if ft in profile.get('nf', '').lower():
                    return True
        return False

    def _safe_load_spec(self, spec_str: str) -> dict | None:
        if not spec_str:
            return None
        try:
            return loads(spec_str)
        except JSONDecodeError:
            try:
                cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', spec_str)
                return loads(cleaned)
            except Exception:
                return None
        except Exception:
            return None

    def _play_sound(self, sound_type: str):
        sound = gs(sound_type)
        sound.play()
        teck(uf(0.14, 0.18), sound.stop)
        return sound

    def _connect(self, address: str, port: int, name: str = '', *_) -> None:
        party_window = self._party_window
        self.close_interface()
        if party_window is not None:
            party_window.close()
        CON(address, port, False)

    def close_interface(self) -> None:
        self.background_sound.stop()
        self.status_updater = None
        self._party_window = None
        cls = self.__class__
        if self in cls._instances:
            cls._instances.remove(self)
        ocw(cls.root, transition='out_scale')
        laser = self._play_sound('laser')

        def stop_check() -> None:
            if cls.root:
                teck(0.01, stop_check)
            else:
                laser.stop()
        stop_check()

    def _play_ding_sound(self, *sound_sequence) -> None:
        sizes = ['Small', '']
        for i, idx in enumerate(sound_sequence):
            name = 'ding' + sizes[idx]
            if i < len(sound_sequence) - 1:
                teck(i / 10, CallStrict(self._play_sound, name))
            else:
                gs(name).play()

    def start_server_scan(self) -> None:
        cls = self.__class__
        if cls.IS_SCANNING:
            push(get_lang_text('FinderWindow.stillBusy'), self.theme.get_color('COLOR_TERTIARY'))
            self._play_ding_sound(0, 0)
            return

        cls.SHOWING_SERVER_ART = False
        cls.SHOWING_SERVER_INFO = False
        push(get_lang_text('FinderWindow.scanningServers'), self.theme.get_color('COLOR_TERTIARY'))
        cls.SCAN_START_TIME = time.time()
        self._play_ding_sound(1, 0)
        cls.IS_SCANNING = True

        plus = APP.plus
        plus.add_v1_account_transaction(
            {'type': 'PUBLIC_PARTY_QUERY', 'proto': PT(), 'lang': 'English'},
            callback=self._on_server_query_response,
        )
        plus.run_v1_account_transactions()

    def get_all_friends(self) -> list:
        """Return friend names from storage (excluding the default 'less')."""
        try:
            return [f['name'] for f in load_friends() if f['name'] != 'less']
        except Exception as e:
            print(f'Error loading friends: {e}')
            return []

    def _add_friend(self, friend: str) -> None:
        if not friend or not friend.strip():
            push(get_lang_text('Global.fieldEmpty'), (1, 0, 0))
            gs('error').play()
            return

        prefixed = f'{V2_LOGO}{friend.strip()}'
        friends = load_friends()

        for f in friends:
            if f['name'] == prefixed:
                push(f'{prefixed} {get_lang_text("Global.alreadyInList")}', self.theme.get_color('COLOR_TERTIARY'))
                return

        existing_ids = [int(f['id']) for f in friends if f['id'].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

        add_friend(name=prefixed, friend_id=new_id,
                   accounts=[], account_pb=None, account_id=None)
        self._play_ding_sound(1, 0)

        self.refresh_best_friends_ui()
        players = [V2_LOGO + p.strip() for p, _ in self._get_filtered_players()]
        self.refresh_best_friends_connected_ui(players)
        pass

        push(f'{prefixed} {get_lang_text("Global.addedSuccessfully")}', self.theme.get_color('COLOR_TERTIARY'))

    def _delete_friend(self, friend: str) -> None:
        if not friend or not friend.strip():
            push(get_lang_text('Global.fieldEmpty'), (1, 0, 0))
            gs('error').play()
            return

        prefixed = friend.strip()
        friends = load_friends()
        target = next((f for f in friends if f['name'] == prefixed), None)

        if not target:
            push(f'{prefixed} not found in list', self.theme.get_color('COLOR_TERTIARY'))
            return

        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('FriendMenu.removeConfirm').format(nick=prefixed),
            action=CallStrict(self._do_delete_friend, prefixed, target['id']),
            ok_text=get_lang_text('FriendMenu.removeFriend'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1, 0.7, 0.7),
        )
        bui.containerwidget(edit=confirm.root_widget, color=self.theme.get_color('COLOR_BACKGROUND'))

    def _do_delete_friend(self, prefixed: str, friend_id: str) -> None:
        remove_friend(friend_id)
        self._play_ding_sound(0, 1)
        push(f'{prefixed} {get_lang_text("Global.deletedSuccessfully")}', self.theme.get_color('COLOR_TERTIARY'))
        self._update_friends_panel()
        self.refresh_best_friends_ui()
        self.refresh_best_friends_connected_ui()
        self._show_friend_info_tip()

    def _on_server_query_response(self, response: dict) -> None:
        cls = self.__class__
        cls.SERVER_MEMORY = response['l']
        cls.ART_DISPLAY = [cs(sc.OUYA_BUTTON_U)] * len(cls.SERVER_MEMORY)
        self.scan_threads = []

        for i, server in enumerate(cls.SERVER_MEMORY):
            t = Thread(target=CallStrict(self._ping_server, server, i))
            self.scan_threads.append(t)
            t.start()

        self.status_updater = tuck(0.01, self._update_ping_status, repeat=True)

    def _ping_server(self, server: dict, index: int) -> None:
        address = server.get('a')
        port = server.get('p')
        if not address or not port:
            self.progress_trackers.append((index, 999))
            return
        server['ping'], server['roster'] = ping_and_get_roster(
            address, port,
            pro=self.progress_trackers, dex=index
        )

    def _update_ping_status(self) -> None:
        if not self.progress_trackers:
            return
        index, ping = self.progress_trackers.pop()
        cls = self.__class__

        if ping == 999:
            cls.ART_DISPLAY[index] = cs(sc.OUYA_BUTTON_A)
        elif ping is not None and ping < 100:
            cls.ART_DISPLAY[index] = cs(sc.OUYA_BUTTON_O)
        else:
            cls.ART_DISPLAY[index] = cs(sc.OUYA_BUTTON_Y)

        if cls.ART_DISPLAY_WIDGET.exists():
            self._draw_art()

        if cs(sc.OUYA_BUTTON_U) not in cls.ART_DISPLAY:
            self.status_updater = None
            self._on_scan_complete()

    def _draw_art(self) -> None:
        cls = self.__class__
        art = '\n'.join(''.join(cls.ART_DISPLAY[i:i + 40])
                        for i in range(0, len(cls.ART_DISPLAY), 40))
        cls.SHOWING_SERVER_ART = True
        if (hasattr(cls, 'ART_DISPLAY_WIDGET') and
                cls.ART_DISPLAY_WIDGET and cls.ART_DISPLAY_WIDGET.exists()):
            tw(cls.ART_DISPLAY_WIDGET, text=art, position=(205, 310))
        self._update_players_list()

    def _update_players_list(self) -> None:
        cls = self.__class__
        for el in cls.SERVER_LIST_ELEMENTS:
            el.delete()
        cls.SERVER_LIST_ELEMENTS.clear()

        players = self._get_filtered_players()
        if players and hasattr(self, 'players_tip') and self.players_tip.exists():
            self.players_tip.delete()

        container_h = max(len(players) * 30, 90)
        ocw(cls.MainParent2, size=(205, container_h))

        found_selected = False
        for i, (player_name, address) in enumerate(players):
            is_selected = (player_name == cls.SCROLL_WIDGET and not found_selected)
            color = (self.theme.get_color('COLOR_PRIMARY') if is_selected
                     else self.theme.get_color('COLOR_TERTIARY'))

            w = tw(
                parent=cls.MainParent2, size=(200, 30),
                selectable=True, click_activate=True,
                glow_type='uniform', color=color, text=player_name,
                position=(0, container_h - 30 - 30 * i),
                maxwidth=175, v_align='center',
                on_activate_call=CallStrict(self._on_server_select, i, player_name),
            )

            if is_selected and not found_selected:
                ocw(cls.MainParent2, visible_child=w)
                found_selected = True

            cls.SERVER_LIST_ELEMENTS.append(w)

        self._current_selected_player = cls.SCROLL_WIDGET

    def _on_scan_complete(self) -> None:
        cls = self.__class__
        if not cls.root or not cls.root.exists():
            cls.IS_SCANNING = False
            return
        self._play_ding_sound(0, 1)
        for t in self.scan_threads:
            t.join()
        self.scan_threads.clear()

        scan_time = time.time() - cls.SCAN_START_TIME
        n = len(cls.SERVER_MEMORY)
        sps = int(n / scan_time) if scan_time else 0

        push(
            f'{get_lang_text("Scan.finished")}\n'
            f'{get_lang_text("Scan.scanned")} {n} {get_lang_text("Scan.servers")} '
            f'{get_lang_text("Scan.in")} {round(scan_time, 2)} {get_lang_text("Scan.seconds")}\n'
            f'{get_lang_text("Scan.approximately")} {sps} '
            f'{get_lang_text("Scan.server")}{get_lang_text("Scan.perSecond")}',
            self.theme.get_color('COLOR_TERTIARY'),
        )

        cls.IS_SCANNING = False
        self._update_friends_panel()

    def _create_friends_panel(self, parent_widget) -> None:
        panel_size = (355, 485)
        self.friends_parent = ocw(
            parent=parent_widget, size=panel_size,
            position=(460, 0), background=False,
        )

        self.friends_separator = iw(
            parent=self.friends_parent, size=(3, 485), position=(0, 0),
            texture=gt('white'), color=self.theme.get_color('COLOR_ACCENT')
        )

        self.all_friends_text = tw(
            parent=self.friends_parent,
            text=self.language.get_text('FriendsWindow.allFriends'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=250, max_height=35, position=(540 - 450, 415)
        )

        self.friend_input = tw(
            parent=self.friends_parent,
            position=(695 - 450, 335), size=(120, 50), text='',
            color=self.theme.get_color('COLOR_PRIMARY'),
            editable=True, h_align='center', v_align='center',
            corner_scale=0.1, scale=10, allow_clear_button=False,
            shadow=0, flatness=1,
        )

        self.add_manual_button = obw(
            parent=self.friends_parent,
            position=(640 - 450, 265), size=(120, 39), text_scale=0.6,
            label=self.language.get_text('FriendsWindow.addManually'),
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=lambda: (
                (lambda friend: (
                    self._add_friend(friend),
                    tw(edit=self.friend_input, text=''),
                    self.refresh_best_friends_ui(),
                    self.refresh_best_friends_connected_ui()
                ))(tw(query=self.friend_input))
            )
        )

        self.friends_separator2 = iw(
            parent=self.friends_parent,
            size=(320, 1), position=(470 - 450, 250),
            texture=gt('white'), color=self.theme.get_color('COLOR_SECONDARY')
        )

        self.online_friends_text = tw(
            parent=self.friends_parent,
            text=self.language.get_text('Global.online') + '\ue019',
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(465 - 450, 210), maxwidth=180, max_height=40,
        )

        self._friends_scroll_container = sw(
            parent=self.friends_parent,
            position=(465 - 450, 255), size=(140, 130),
            border_opacity=0.4, color=self.theme.get_color('COLOR_ACCENT')
        )

        self._friends_list_container = None
        self.refresh_best_friends_ui()

        self._connected_friends_scroll_container = sw(
            parent=self.friends_parent,
            position=(465 - 450, 32), size=(140, 170),
            border_opacity=0.4, color=self.theme.get_color('COLOR_ACCENT')
        )

        self._connected_friends_list_container = None

        self._friend_info_container = ocw(
            parent=self.friends_parent,
            position=(615 - 450, 32), size=(175, 170), background=False
        )

        iw(
            parent=self.friends_parent,
            position=(160, 32), size=(180, 172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'), opacity=0.4
        )

        self.friend_info_tip = tw(
            parent=self._friend_info_container,
            size=(165, 170), position=(0, 0),
            text=self.language.get_text('FriendsWindow.selectFriendToView'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=160, h_align='center', v_align='center'
        )

        self.refresh_best_friends_ui()
        self.refresh_best_friends_connected_ui()

    def refresh_best_friends_ui(self) -> None:
        """Rebuild the all-friends scrollable list."""
        if (hasattr(self, '_friends_list_container') and
                self._friends_list_container and
                self._friends_list_container.exists()):
            self._friends_list_container.delete()

        friends = self.get_all_friends()

        if not friends:
            self._friends_list_container = ocw(
                parent=self._friends_scroll_container,
                size=(190, 140), background=False
            )
            default = tw(
                parent=self._friends_list_container,
                size=(170, 30), color=self.theme.get_color('COLOR_TERTIARY'),
                text=f'{V2_LOGO}less', position=(0, 110),
                maxwidth=160, selectable=True, click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(
                    self._show_friend_popup, (200, 100), delete_user=False
                )
            )
            self._friend_text_widgets = [default]
            return

        container_h = max(len(friends) * 30, 140)
        self._friends_list_container = ocw(
            parent=self._friends_scroll_container,
            size=(190, container_h), background=False
        )
        self._friend_text_widgets = []

        for i, friend in enumerate(friends):
            display = friend if len(friend) <= 7 else friend[:7] + '...'
            w = tw(
                parent=self._friends_list_container,
                size=(170, 30), color=self.theme.get_color('COLOR_TERTIARY'),
                text=display, position=(0, container_h - 30 - 30 * i),
                maxwidth=100, selectable=True, click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(self._show_friend_popup, (200, 100), friend)
            )
            self._friend_text_widgets.append(w)

    def refresh_best_friends_connected_ui(self,
                                           players_list: list | None = None) -> None:
        """Rebuild the online-friends section."""
        if not (self.friends_parent and self.friends_parent.exists()):
            return

        if (hasattr(self, 'no_friends_online_text') and
                self.no_friends_online_text and
                self.no_friends_online_text.exists()):
            self.no_friends_online_text.delete()
            self.no_friends_online_text = None

        if (hasattr(self, '_connected_friends_list_container') and
                self._connected_friends_list_container and
                self._connected_friends_list_container.exists()):
            self._connected_friends_list_container.delete()
            self._connected_friends_list_container = None

        self._connected_friend_text_widgets = []

        if players_list is None:
            players_list = [V2_LOGO + p.strip()
                            for p, _ in self._get_filtered_players()]

        real_friends = self.get_all_friends()
        connected = self._get_connected_best_friends(players_list)
        self.best_friends_connected = len(connected)

        if not connected or not real_friends:
            self.no_friends_online_text = tw(
                parent=self.friends_parent,
                position=(60, 105),
                text=self.language.get_text('FriendsWindow.noFriendsOnline'),
                color=self.theme.get_color('COLOR_TERTIARY'),
                maxwidth=120, max_height=90, h_align='center', v_align='center'
            )
            return

        self._connected_friends_list_container = sw(
            parent=self.friends_parent,
            position=(465 - 450, 32), size=(140, 170),
            border_opacity=0.4, color=self.theme.get_color('COLOR_ACCENT')
        )

        container_h = max(len(connected) * 30, 170)
        inner = ocw(
            parent=self._connected_friends_list_container,
            size=(140, container_h), background=False
        )

        for i, friend in enumerate(connected):
            display = friend if len(friend) <= 7 else friend[:7] + '...'
            w = tw(
                parent=inner, size=(130, 30),
                color=self.theme.get_color('COLOR_TERTIARY'),
                text=display, position=(5, container_h - 30 - 30 * i),
                maxwidth=100, selectable=True, click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(self._display_best_friend_info, friend)
            )
            self._connected_friend_text_widgets.append(w)

    def _get_connected_best_friends(self, players_list: list | None = None) -> list:
        """Return friends that appear in the current players list."""
        try:
            friends_set = set(self.get_all_friends())
            if not players_list:
                return []
            seen: set = set()
            result: list = []
            for player in players_list:
                if player in friends_set and player not in seen:
                    result.append(player)
                    seen.add(player)
                clean = player.lstrip(V2_LOGO)
                if clean in friends_set and player not in seen:
                    result.append(player)
                    seen.add(player)
            return result
        except Exception as e:
            print(f'Error getting connected best friends: {e}')
            return []

    def _show_friend_popup(self, position: tuple, friend: str | None = None,
                            delete_user: bool = True) -> None:
        view_text = self.language.get_text('FriendsWindow.viewProfile')
        delete_text = self.language.get_text('FriendsWindow.deleteFriend')

        choices = ['view_profile']
        choices_display = [babase.Lstr(value=view_text)]
        if friend is not None and delete_user:
            choices.append('delete_friend')
            choices_display.append(babase.Lstr(value=delete_text))

        self._popup_type = 'friend'
        self._popup_target = friend
        popup = PopupMenuWindow(
            position=position,
            choices=choices,
            choices_display=choices_display,
            current_choice='view_profile',
            delegate=self,
        )
        bui.containerwidget(
            edit=popup.root_widget,
            color=self.theme.get_color('COLOR_BUTTON'),
        )

    def _open_profile(self, friend: str | None) -> None:
        ProfileSearchWindow(
            self.friends_parent,
            v2=friend.replace(V2_LOGO, '') if friend else None
        )

    def _show_friend_info_tip(self) -> None:
        for el in self.best_friends_elements:
            el.delete()
        self.best_friends_elements.clear()
        if self._friend_info_container and self._friend_info_container.exists():
            self.friend_info_tip = tw(
                parent=self._friend_info_container,
                size=(165, 170), position=(0, 0),
                text=self.language.get_text('FriendsWindow.selectFriendToView'),
                color=self.theme.get_color('COLOR_PRIMARY'),
                maxwidth=160, h_align='center', v_align='center'
            )
        self._current_displayed_best_friend = None

    def _display_best_friend_info(self, player_name: str) -> None:
        clean = player_name.lstrip(V2_LOGO)

        for el in self.best_friends_elements:
            el.delete()
        self.best_friends_elements.clear()
        if self.friend_info_tip and self.friend_info_tip.exists():
            self.friend_info_tip.delete()

        self._current_displayed_best_friend = player_name
        server_info = server_address = server_port = None

        try:
            for srv in FinderWindow.SERVER_MEMORY:
                for entry in srv.get('roster', []):
                    spec = self._safe_load_spec(entry.get('spec', ''))
                    if spec and spec.get('n') in (clean, player_name):
                        server_info = srv
                        server_address = srv['a']
                        server_port = srv['p']
                        break
                if server_info:
                    break
        except Exception:
            pass

        def add(w) -> None:
            self.best_friends_elements.append(w)

        add(tw(
            parent=self._friend_info_container,
            position=(10, 140), h_align='left', v_align='center',
            maxwidth=90, text=f'{V2_LOGO}{clean}',
            color=self.theme.get_color('COLOR_PRIMARY'),
            size=(155, 25), selectable=True, click_activate=True,
            glow_type='uniform',
            on_activate_call=CallStrict(self._copy_to_clipboard, clean)
        ))

        info_btn = obw(
            parent=self._friend_info_container, label='',
            size=(25, 25), position=(135, 140),
            texture=gt('cuteSpaz'), selectable=False, color=(1, 1, 1),
            enable_sound=False,
            on_activate_call=lambda: self._open_profile(clean)
        )
        add(info_btn)

        add(iw(
            parent=self._friend_info_container,
            size=(155, 2), position=(10, 135),
            texture=gt('white'), color=self.theme.get_color('COLOR_SECONDARY')
        ))

        server_name = server_info['n'] if server_info else 'N/A'
        add(tw(
            parent=self._friend_info_container,
            position=(10, 95), h_align='left', v_align='center',
            maxwidth=155, text=server_name,
            color=self.theme.get_color('COLOR_PRIMARY'),
            size=(155, 25), selectable=True, click_activate=True,
            glow_type='uniform',
            on_activate_call=CallStrict(self._copy_to_clipboard, server_name)
        ))

        if server_address and server_port:
            add(tw(
                parent=self._friend_info_container,
                position=(10, 70), h_align='left', v_align='center',
                maxwidth=100, text=server_address,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(100, 25), selectable=True, click_activate=True,
                glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, server_address)
            ))
            add(tw(
                parent=self._friend_info_container,
                position=(112, 70), text=':',
                color=self.theme.get_color('COLOR_PRIMARY'), scale=1.0
            ))
            add(tw(
                parent=self._friend_info_container,
                position=(120, 70), h_align='left', v_align='center',
                maxwidth=45, text=str(server_port),
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(45, 25), selectable=True, click_activate=True,
                glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, str(server_port))
            ))
        else:
            add(tw(
                parent=self._friend_info_container,
                position=(10, 70), h_align='left', v_align='center',
                maxwidth=155, text='N/A',
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(155, 25), selectable=False
            ))

        connect_text = self.language.get_text('Global.connect')
        delete_text = self.language.get_text('FriendsWindow.deleteFriend')

        add(iw(
            parent=self._friend_info_container,
            size=(165, 1), position=(10, 65),
            texture=gt('white'), color=self.theme.get_color('COLOR_SECONDARY')
        ))

        if server_info and server_address and server_port:
            add(obw(
                parent=self._friend_info_container,
                position=(10, 35), size=(150, 25), label=connect_text,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                on_activate_call=CallStrict(
                    self._connect, server_address, int(server_port), server_name
                )
            ))

        add(obw(
            parent=self._friend_info_container,
            position=(10, 5 if server_info else 35), size=(150, 25),
            label=delete_text,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=CallStrict(self._delete_friend, player_name)
        ))

    def get_connected_count(self) -> int:
        return self.best_friends_connected

    def update_connected_count_display(self, count_widget) -> None:
        if count_widget and count_widget.exists():
            tw(edit=count_widget, text=str(self.best_friends_connected))


_NAME_RE = re.compile(r'^[a-z0-9_]{3,50}$')
_AUTH_REGISTER = f'{BASE_URL}/auth/register'
_AUTH_LOGIN = f'{BASE_URL}/auth/login'


def _post_json(url: str, payload: dict) -> tuple[dict, int]:
    """Send a POST request with JSON body. Returns (parsed_body, status_code)."""
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible)',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8')), resp.status
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode('utf-8'))
        except Exception:
            pass
        return body, e.code
    except urllib.error.URLError:
        return {'error': 'Could not connect to server.'}, 0


class CreateAccountWindow:
    """Window for creating a new DM account."""

    def __init__(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        self._width = 360
        self._height = 335

        bg_color = _theme.get_color('COLOR_BACKGROUND')
        color_primary = _theme.get_color('COLOR_PRIMARY')

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=bg_color,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 28),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('CreateAccountWindow.title'),
            scale=1.0,
            color=(1, 1, 1),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(15, self._height - 52),
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._back,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        field_x = 20
        field_w = self._width - 40
        label_scale = 0.72

        # Name
        bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 265),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('CreateAccountWindow.name'),
            scale=label_scale,
            color=color_primary,
        )
        self._name_field = bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 215),
            size=(field_w, 38),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=25,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Login name (lowercase, letters, digits, _)',
        )

        # Nickname
        bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 205),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('CreateAccountWindow.nickname'),
            scale=label_scale,
            color=color_primary,
        )
        self._nick_field = bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 155),
            size=(field_w, 38),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=30,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Unique nickname',
        )

        # Password
        bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 145),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('CreateAccountWindow.password'),
            scale=label_scale,
            color=color_primary,
        )
        self._pass_field = bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 95),
            size=(field_w, 38),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=50,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Password (min 8 characters)',
        )

        self._create_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(field_x, 16),
            size=(field_w, 68),
            label=get_lang_text('CreateAccountWindow.create'),
            color=(0.2, 0.6, 0.2),
            textcolor=(1, 1, 1),
            on_activate_call=self._on_create,
        )

    @staticmethod
    def _get_v2_account() -> str | None:
        try:
            plus = babase.app.plus
            if plus is None:
                return None
            raw = plus.get_v1_account_display_string()
            if not raw:
                return None
            v2_logo = babase.charstr(babase.SpecialChar.V2_LOGO) if hasattr(babase.SpecialChar, 'V2_LOGO') else '\ue063'
            cleaned = raw.lstrip(v2_logo).strip()
            return cleaned if cleaned else None
        except Exception:
            return None

    def _on_create(self) -> None:
        name = bui.textwidget(query=self._name_field)
        nick = bui.textwidget(query=self._nick_field)
        password = bui.textwidget(query=self._pass_field)

        if not name or not nick or not password:
            bui.screenmessage('Please fill in all fields.', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        if not _NAME_RE.match(name):
            bui.screenmessage('Name: 3-50 chars, lowercase letters, digits or _', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        if len(password) < 8:
            bui.screenmessage('Password must be at least 8 characters.', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        v2 = self._get_v2_account()
        bui.buttonwidget(edit=self._create_btn, label=get_lang_text('CreateAccountWindow.creating'), color=(0.3, 0.3, 0.3))

        def _run() -> None:
            payload: dict = {'name': name, 'nickname': nick, 'password': password}
            if v2:
                payload['v2'] = v2
            body, status = _post_json(_AUTH_REGISTER, payload)

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(
                    edit=self._create_btn,
                    label=get_lang_text('CreateAccountWindow.create'),
                    color=(0.2, 0.6, 0.2),
                )
                if status == 201:
                    save_session(body)
                    start_keep_alive()
                    ensure_friends_session()
                    user = body.get('user', {})
                    bui.screenmessage(
                        f'Welcome, {user.get("nickname", nick)}!',
                        color=(0, 1, 0),
                    )
                    bui.getsound('cashRegister').play()
                    self._close()
                    DMWindow()
                elif status == 409:
                    error = body.get('error', '')
                    if 'V2' in error or 'v2' in error:
                        bui.screenmessage('Max accounts for this game account reached (5).', color=(1, 0.3, 0.3))
                    elif 'Name' in error or 'name' in error:
                        bui.screenmessage('That name is already taken.', color=(1, 0.3, 0.3))
                    else:
                        bui.screenmessage(error or 'Account already exists.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                elif status == 400:
                    error = body.get('error', 'Invalid data.')
                    bui.screenmessage(error, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                elif status == 0:
                    bui.screenmessage('Could not connect to server.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Server error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        Thread(target=_run, daemon=True).start()

    def _back(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()
        LoginWindow()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class LoginWindow:
    """Login window for the DM feature."""

    def __init__(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        self._width = 360
        self._height = 285

        bg_color = _theme.get_color('COLOR_BACKGROUND')
        color_primary = _theme.get_color('COLOR_PRIMARY')

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=bg_color,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 28),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('LoginWindow.title'),
            scale=1.0,
            color=(1, 1, 1),
        )

        close_btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(15, self._height - 50),
            size=(30, 30),
            label='X',
            button_type='square',
            color=(0.6, 0.1, 0.1),
            textcolor=(1, 1, 1),
            enable_sound=False,
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=close_btn)

        field_x = 20
        field_w = self._width - 40
        label_scale = 0.72

        # Name (login field)
        bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 218),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('LoginWindow.name'),
            scale=label_scale,
            color=color_primary,
        )
        self._nick_field = bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 168),
            size=(field_w, 38),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=25,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Name (login)',
        )

        # Password
        bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 158),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('LoginWindow.password'),
            scale=label_scale,
            color=color_primary,
        )
        self._pass_field = bui.textwidget(
            parent=self._root_widget,
            position=(field_x, 108),
            size=(field_w, 38),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=50,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Password',
        )

        self._login_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(field_x, 60),
            size=(field_w, 40),
            label=get_lang_text('LoginWindow.login'),
            color=(0.2, 0.5, 0.8),
            textcolor=(1, 1, 1),
            on_activate_call=self._on_login,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(field_x, 16),
            size=(field_w, 38),
            label=get_lang_text('LoginWindow.createAccount'),
            color=(0.25, 0.25, 0.25),
            textcolor=(0.8, 0.8, 0.8),
            on_activate_call=self._open_create_account,
        )

    def _on_login(self) -> None:
        nick = bui.textwidget(query=self._nick_field)
        password = bui.textwidget(query=self._pass_field)

        if not nick or not password:
            bui.screenmessage('Please fill in all fields.', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        bui.buttonwidget(edit=self._login_btn, label=get_lang_text('LoginWindow.loggingIn'), color=(0.3, 0.3, 0.3))

        def _run() -> None:
            body, status = _post_json(_AUTH_LOGIN, {
                'name': nick,
                'password': password,
            })

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(
                    edit=self._login_btn,
                    label=get_lang_text('LoginWindow.login'),
                    color=(0.2, 0.5, 0.8),
                )
                if status == 200:
                    save_session(body)
                    start_keep_alive()
                    ensure_friends_session()
                    user = body.get('user', {})
                    bui.screenmessage(
                        f'Logged in as {user.get("nickname", nick)}',
                        color=(0, 1, 0.5),
                    )
                    bui.getsound('cashRegister').play()
                    self._close()
                    DMWindow()
                elif status == 401:
                    bui.screenmessage('Invalid name or password.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                elif status == 400:
                    error = body.get('error', 'Missing fields.')
                    bui.screenmessage(error, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                elif status == 0:
                    bui.screenmessage('Could not connect to server.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Server error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        Thread(target=_run, daemon=True).start()

    def _open_create_account(self) -> None:
        self._close()
        CreateAccountWindow()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()







def _fmt_ban_msg(ban: dict) -> str:
    """Format a ban dict into a human-readable screenmessage string."""
    from datetime import datetime, timezone
    ban_type = ban.get('ban_type', '')
    reason = (ban.get('reason') or '').strip()
    if ban_type == 'permanent':
        time_str = get_lang_text('Admin.permanent')
    else:
        expires = ban.get('expires_at')
        time_str = '?'
        if expires:
            try:
                exp = datetime.fromisoformat(str(expires).replace('Z', '+00:00'))
                remaining = max(0, int((exp - datetime.now(timezone.utc)).total_seconds()))
                h, rem = divmod(remaining, 3600)
                m, s = divmod(rem, 60)
                if h > 0:
                    time_str = f'{h}h {m}m {s}s'
                elif m > 0:
                    time_str = f'{m}m {s}s'
                else:
                    time_str = f'{s}s'
            except Exception:
                pass
    msg = get_lang_text('Chat.bannedFor').format(time=time_str)
    if reason:
        msg += f' | {get_lang_text("Chat.banReason").format(reason=reason)}'
    return msg


class DMWindow:
    """Main DM window with friends list on the left and global chat on the right."""

    def __init__(self) -> None:
        import urllib.request
        import urllib.error

        uiscale = bui.app.ui_v1.uiscale
        self._width = 700
        self._height = 435 if uiscale is babase.UIScale.SMALL else 480
        self._friends: list[dict] = []
        self._chat_texts: list = []
        self._selected_msg = ''
        self._chat_friend: Optional[dict] = None
        self._msg_select_seq = 0
        self._target_restored = False

        scale = (
            1.44 if uiscale is babase.UIScale.SMALL else
            1.1 if uiscale is babase.UIScale.MEDIUM else 1.1
        )

        _dm_bg = _theme.get_color('COLOR_BACKGROUND')

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_dm_bg,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=scale,
        )

        # title always visible while checking
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 16),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('DMWindow.title'),
            scale=1.0,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        close_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(30, self._height - 54),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            enable_sound=False,
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=close_btn)

        self._checking_txt = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='Checking connection...',
            scale=0.7,
            color=(0.5, 0.5, 0.5),
        )

        def _ping() -> None:
            online = False
            try:
                with urllib.request.urlopen(f'{BASE_URL}/health', timeout=5) as resp:
                    online = bool(resp.status)
            except urllib.error.HTTPError:
                online = True
            except urllib.error.URLError:
                pass
            except Exception:
                pass

            set_server_online(online)
            babase.pushcall(
                lambda: self._on_ping_result(online),
                from_other_thread=True,
            )

        threading.Thread(target=_ping, daemon=True).start()

    def _on_ping_result(self, online: bool) -> None:
        if not self._root_widget.exists():
            return

        self._checking_txt.delete()

        if not online:
            self._build_offline_ui()
            return

        if not is_logged_in():
            bui.containerwidget(edit=self._root_widget, transition='out_scale')
            if get_accounts_list():
                AccountsPopup(on_logout=LoginWindow)
            else:
                LoginWindow()
            return

        set_dm_window_open(True)
        self._build_ui()
        self._load_friends()

        session = ensure_global_session()
        for msg in session.get_cache():
            self._add_chat_message(msg)
        session.add_listener(self._on_realtime_message)

        ensure_friends_session().add_server_invite_listener(self._on_server_invite)
        add_online_status_listener(self._on_online_status_change)
        add_pending_request_listener(self._update_pending_badge)
        add_unread_dm_listener(self._update_unread_badges)
        threading.Thread(target=self._fetch_initial_pending, daemon=True).start()
        threading.Thread(target=sync_my_role, daemon=True).start()

    def _build_offline_ui(self) -> None:
        w, h = self._width, self._height
        error_display(
            parent=self._root_widget,
            position=(w * 0.5 - 90, h * 0.5 - 60),
            size=(180, 200),
            error_text='Connection error.\nTry again later.',
            icon_texture='cuteSpaz',
            text_color=(1.0, 0.4, 0.4),
        )

    def _build_ui(self) -> None:
        user = get_session().get('user', {})
        nick = user.get('nickname', '')
        role = user.get('role', 'USER')

        self._acct_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(50, 22),
            size=(80, 25),
            label=f'\ue019 {nick}',
            button_type='square',
            color=(0.2, 0.35, 0.2),
            textcolor=(0.6, 0.95, 0.6),
            enable_sound=True,
            on_activate_call=lambda: AccountPopup(
                on_logout=self._close,
                on_switch=self._close,
                on_profile_updated=self._on_profile_updated,
            ),
        )

        if role == 'ADMIN':
            bui.buttonwidget(
                parent=self._root_widget,
                position=(138, 22),
                size=(82, 25),
                label=get_lang_text('Admin.viewAllUsers'),
                button_type='square',
                color=(0.35, 0.15, 0.15),
                textcolor=(1.0, 0.5, 0.5),
                text_scale=0.62,
                enable_sound=True,
                on_activate_call=self._open_admin_users,
            )

        if role in ('ADMIN', 'MANAGER'):
            role_color = (1.0, 0.35, 0.35) if role == 'ADMIN' else (0.95, 0.75, 0.2)
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width - 39, self._height - 37),
                size=(0, 0),
                h_align='right',
                v_align='top',
                text=f'[ {role} ]',
                scale=0.62,
                color=role_color,
            )

        self._build_friends_panel()
        self._build_chat_panel()

    def _on_profile_updated(self, fields: dict) -> None:
        if not self._root_widget.exists() or not self._acct_btn.exists():
            return
        if 'nickname' in fields:
            bui.buttonwidget(edit=self._acct_btn, label=f'\ue019 {fields["nickname"]}')

        self._build_friends_panel()
        self._build_chat_panel()

    def _build_friends_panel(self) -> None:
        _, h = self._width, self._height
        px, pw = 10, 243

        bui.textwidget(
            parent=self._root_widget,
            position=(px + pw / 2, h - 48),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('DM.friends'),
            scale=0.74,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(px + 20+ 20, 60),
            size=(80, 30),
            label=get_lang_text('DM.add'),
            color=(0.2, 0.5, 0.2),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._open_add_friend,
        )

        self._requests_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(px + 20 + 80 +45, 60),
            size=(80, 30),
            label=get_lang_text('DM.requests'),
            color=(0.5, 0.3, 0.1),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._open_pending,
        )

        badge_size = 24
        badge_cx = px + 20 + 80 + 45 + 80
        badge_cy = 75
        self._pending_badge_img = bui.imagewidget(
            parent=self._root_widget,
            position=(badge_cx - badge_size // 2, badge_cy - badge_size // 2),
            size=(badge_size, badge_size),
            texture=bui.gettexture('circle'),
            color=(0.9, 0.1, 0.1),
            opacity=0.0,
        )
        self._pending_badge_num = bui.textwidget(
            parent=self._root_widget,
            position=(badge_cx, badge_cy),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='',
            scale=0.55,
            color=(1.0, 1.0, 1.0),
        )

        self._friends_scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(px + 20, 60 + 40), 
            size=(pw -20, h - 160),
            background=False,
            highlight=False,
            capture_arrows=True,
            color=_theme.get_color('COLOR_ACCENT'),
        )

        self._friends_container = bui.containerwidget(
            parent=self._friends_scroll,
            size=(pw - 20 - 20, 20),
            background=False,
            selection_loops_to_parent=True,
        )

    def _build_chat_panel(self) -> None:
        w, h = self._width, self._height
        cx = 264
        cw = w - cx - 8

        self._chat_back_btn: bui.Widget | None = None

        self._chat_title_widget = bui.textwidget(
            parent=self._root_widget,
            position=(cx + cw * 0.45, h - 48),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('DM.globalChat'),
            scale=0.74,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        send_w = 40
        tf_w = cw - send_w - 21

        self._chat_input = bui.textwidget(
            parent=self._root_widget,
            position=(cx, 10),
            size=(tf_w, 40),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=500,
            maxwidth=tf_w - 8,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description='Message...',
            on_return_press_call=self._send_message,
        )

        self._send_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(cx + tf_w + 5, 12),
            size=(send_w, send_w),
            label='',
            texture=bui.gettexture('rightButton'),
            color=(1, 1, 1),
            enable_sound=False,
            on_activate_call=self._send_message,
        )

        self._chat_scroll_width = cw
        self._chat_scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(cx, 56),
            size=(cw - 30 , h - 114),
            background=False,
            highlight=False,
            capture_arrows=True,
            color=_theme.get_color('COLOR_ACCENT'),
        )

        self._chat_column = bui.columnwidget(
            parent=self._chat_scroll,
            border=2,
            left_border=-160,
            margin=0,
        )

    def _rebuild_friends(self) -> None:
        if not self._root_widget.exists():
            return

        pw = 243
        row_h = 36
        total_h = max(len(self._friends) * row_h + 8, 20)
        container_w = pw - 20

        self._friends_container.delete()
        self._friends_container = bui.containerwidget(
            parent=self._friends_scroll,
            size=(container_w, total_h),
            background=False,
            selection_loops_to_parent=True,
        )

        if not self._friends:
            bui.textwidget(
                parent=self._friends_container,
                position=(container_w / 2, total_h / 2),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=get_lang_text('DM.noFriendsYet'),
                scale=0.7,
                color=(0.5, 0.5, 0.5),
            )
            return

        row_x = 2
        row_w = container_w - 24
        menu_btn_w = 26
        btn_color = _theme.get_color('COLOR_BUTTON')
        online_ids = get_online_friend_ids()

        all_unread = get_all_unread_dm_counts()

        y = total_h - row_h
        for friend in self._friends:
            raw = friend.get('friend_name') or friend.get('friend_nickname', '?')
            display = raw[:8] + '...' if len(raw) > 8 else raw
            fid = friend.get('friend_id')
            is_online = fid in online_ids
            unread = all_unread.get(str(fid), 0) if fid is not None else 0

            # row button spans full width; menu button overlaps on top at right edge
            row_btn = bui.buttonwidget(
                parent=self._friends_container,
                position=(row_x, y),
                size=(row_w, row_h),
                label='',
                color=btn_color,
                enable_sound=True,
                on_activate_call=lambda f=friend: self._switch_to_friend(f),
            )

            icon_size = 34
            icon_x = 5
            icon_y = y + (row_h - icon_size) // 2 - 1

            bui.imagewidget(
                parent=self._friends_container,
                position=(row_x + icon_x, icon_y),
                size=(icon_size, icon_size),
                texture=bui.gettexture('cuteSpaz'),
                draw_controller=row_btn,
            )

            # online status dot (bottom-right corner of icon)
            dot_size = 10
            dot_cx = row_x + icon_x + icon_size - 7
            dot_cy = icon_y + 8
            bui.imagewidget(
                parent=self._friends_container,
                position=(dot_cx - dot_size // 2, dot_cy - dot_size // 2),
                size=(dot_size, dot_size),
                texture=bui.gettexture('circle'),
                color=(0.2, 0.85, 0.2) if is_online else (0.35, 0.35, 0.35),
                draw_controller=row_btn,
            )

            bui.textwidget(
                parent=self._friends_container,
                position=(row_x + icon_x + icon_size + 5, y + row_h / 2),
                size=(0, 0),
                h_align='left',
                v_align='center',
                text=display,
                scale=0.75,
                color=(0.85, 0.85, 0.9),
                maxwidth=row_w - (icon_x + icon_size + 9) - menu_btn_w - 10,
                draw_controller=row_btn,
            )

            # unread messages badge
            if unread > 0:
                badge_size = 22
                badge_cx = row_x + row_w - menu_btn_w + 20
                badge_cy = y + row_h / 2 - 10
                bui.imagewidget(
                    parent=self._friends_container,
                    position=(badge_cx - badge_size // 2, badge_cy - badge_size // 2),
                    size=(badge_size, badge_size),
                    texture=bui.gettexture('circle'),
                    color=(0.9, 0.1, 0.1),
                    draw_controller=row_btn,
                )
                bui.textwidget(
                    parent=self._friends_container,
                    position=(badge_cx, badge_cy),
                    size=(0, 0),
                    h_align='center',
                    v_align='center',
                    text=str(unread) if unread < 100 else '99+',
                    scale=0.55,
                    color=(1.0, 1.0, 1.0),
                    draw_controller=row_btn,
                )

            # menu icon a bit to the left of the right edge
            bui.buttonwidget(
                parent=self._friends_container,
                position=(row_x + row_w - menu_btn_w - 16, y + (row_h - menu_btn_w) // 2),
                size=(menu_btn_w, menu_btn_w),
                label='',
                texture=bui.gettexture('menuIcon'),
                color=_theme.get_color('COLOR_PRIMARY'),
                icon_color=_theme.get_color('COLOR_PRIMARY'),
                enable_sound=True,
                on_activate_call=lambda f=friend: self._open_friend_menu(f),
            )

            y -= row_h

        if not self._target_restored:
            self._target_restored = True
            self._restore_chat_target()

    def _restore_chat_target(self) -> None:
        target = get_dm_chat_target()
        if target is None or target.get('type') == 'global':
            return
        if target.get('type') == 'friend':
            fid = target.get('friend_id')
            for f in self._friends:
                if f.get('friend_id') == fid:
                    self._switch_to_friend(f)
                    return

    def _add_chat_message(self, msg: dict) -> None:
        if not self._root_widget.exists():
            return

        display_name = msg.get('nickname') or msg.get('name', '?')
        content = msg.get('content', '')
        role = msg.get('role', 'USER')
        row_w = int(self._chat_scroll_width * 0.94 - 20)

        if role == 'ADMIN':
            text = f'\u2022 {display_name}: {content}'
            color = (1.0, 0.35, 0.35)
        elif role == 'MANAGER':
            text = f'\u2022 {display_name}: {content}'
            color = (1.0, 0.65, 0.1)
        else:
            text = f'{display_name}: {content}'
            color = (1.0, 1.0, 1.0)

        txt = bui.textwidget(
            parent=self._chat_column,
            h_align='left',
            v_align='center',
            scale=0.65,
            size=(900, 14),
            text=text,
            color=color,
            maxwidth=row_w,
            shadow=0.3,
            flatness=1.0,
            selectable=True,
        )
        bui.textwidget(
            edit=txt,
            on_select_call=bui.CallPartial(self._on_msg_select, text, txt, msg),
        )
        track = txt

        self._chat_texts.append(track)
        if len(self._chat_texts) > 60:
            self._chat_texts.pop(0).delete()

        bui.containerwidget(edit=self._chat_column, visible_child=track)

    def _on_msg_select(self, text: str, widget: bui.Widget, msg: dict) -> None:
        self._selected_msg = text
        self._selected_msg_data = msg
        self._msg_select_seq += 1
        seq = self._msg_select_seq

        try:
            pos = widget.get_screen_space_center() if widget.exists() else (400.0, 300.0)
        except Exception:
            pos = (400.0, 300.0)

        session_user = get_session().get('user', {})
        my_id = session_user.get('id')
        caller_role = session_user.get('role', 'USER')
        sender_id = msg.get('user_id') or msg.get('senderId')
        is_other = (
            self._chat_friend is None
            and sender_id is not None
            and sender_id != my_id
        )
        choices = ['copy', 'translate']
        labels = [
            get_lang_text('GlobalChat.copy'),
            get_lang_text('GlobalChat.translate'),
        ]
        if is_other:
            choices.append('profile')
            labels.append(get_lang_text('GlobalChat.viewAccount'))
            if caller_role in ('ADMIN', 'MANAGER'):
                sender_role = msg.get('role', 'USER')
                can_ban = sender_role not in ('ADMIN',) and not (
                    caller_role == 'MANAGER' and sender_role == 'MANAGER'
                )
                if can_ban:
                    choices.append('ban')
                    labels.append(get_lang_text('Admin.banUser'))
                if caller_role == 'ADMIN':
                    choices.append('changeRole')
                    labels.append(get_lang_text('Admin.changeRole'))

        def _open_popup() -> None:
            if seq != self._msg_select_seq:
                return
            if not self._root_widget.exists():
                return
            self._msg_popup = _ThemedPopupMenu(
                position=(pos[0] * 1.05, pos[1]),
                scale=_get_popup_window_scale(),
                choices=choices,
                choices_display=_creat_Lstr_list(labels),
                current_choice='copy',
                delegate=self,
                bg_color=_theme.get_color('COLOR_BACKGROUND'),
                text_color=_theme.get_color('COLOR_PRIMARY'),
            )

        babase.apptimer(0.15, _open_popup)

    def popup_menu_selected_choice(self, _: PopupMenuWindow, choice: str) -> None:
        if choice == 'copy':
            try:
                bui.clipboard_set_text(self._selected_msg)
                bui.screenmessage('Copied!', color=(0.5, 1, 0.5))
            except Exception:
                bui.screenmessage(self._selected_msg, color=(0.8, 0.8, 0.8))
        elif choice == 'translate':
            bui.screenmessage('Translate coming soon.', color=(0.8, 0.8, 0.5))
        elif choice == 'profile':
            msg = getattr(self, '_selected_msg_data', {})
            db_id = msg.get('user_id') or msg.get('senderId')
            uid_str = msg.get('uid', '')
            display = msg.get('nickname') or msg.get('name', '?')
            if db_id is not None:
                is_friend = db_id in {f.get('friend_id') for f in self._friends}
                on_pending = self._open_pending

                def _check_and_open(db_id=db_id, uid_str=uid_str, display=display, is_friend=is_friend):
                    if is_friend:
                        pending_status = 'none'
                    else:
                        check_body, check_http = authenticated_get(f'/friends/check/{db_id}')
                        pending_status = (
                            check_body.get('status', 'none')
                            if check_http == 200 and isinstance(check_body, dict) else 'none'
                        )
                    friend_dict = {'friend_id': db_id, 'friend_nickname': display}
                    babase.pushcall(
                        lambda: FriendAccountPopup(
                            friend=friend_dict,
                            is_friend=is_friend,
                            uid_str=uid_str,
                            pending_status=pending_status,
                            on_pending_click=on_pending,
                        ),
                        from_other_thread=True,
                    )

                threading.Thread(target=_check_and_open, daemon=True).start()
        elif choice == 'ban':
            msg = getattr(self, '_selected_msg_data', {})
            db_id = msg.get('user_id') or msg.get('senderId')
            display = msg.get('nickname') or msg.get('name', '?')
            if db_id is not None:
                AdminBanPopup(friend={'friend_id': db_id, 'friend_nickname': display})
        elif choice == 'changeRole':
            msg = getattr(self, '_selected_msg_data', {})
            db_id = msg.get('user_id') or msg.get('senderId')
            display = msg.get('nickname') or msg.get('name', '?')
            if db_id is not None:
                AdminChangeRolePopup(friend={'friend_id': db_id, 'friend_nickname': display})

    def popup_menu_closing(self, _: PopupMenuWindow) -> None:
        pass

    def _load_friends(self) -> None:
        def _run() -> None:
            body, status = authenticated_get('/friends/')

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                if status == 200 and isinstance(body, list):
                    self._friends = body
                    self._rebuild_friends()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _on_realtime_message(self, msg: dict) -> None:
        if self._root_widget.exists():
            self._add_chat_message(msg)

    def _split_message(self, text: str) -> list[str]:
        chunks: list[str] = []
        while len(text) > 64:
            chunks.append(text[:63] + '-')
            text = text[63:]
        chunks.append(text)
        return chunks

    def _send_message(self) -> None:
        import time
        content = bui.textwidget(query=self._chat_input)
        if not content or not content.strip():
            return

        if self._chat_friend is not None:
            if self._chat_friend.get('friend_id') not in get_online_friend_ids():
                bui.screenmessage('Friend is offline.', color=(0.6, 0.6, 0.6))
                bui.getsound('error').play()
                return

        bui.textwidget(edit=self._chat_input, text='')
        bui.buttonwidget(edit=self._send_btn, color=(0.5, 0.5, 0.5))

        chunks = self._split_message(content.strip())
        friend = self._chat_friend

        if friend is None:
            def _run_global() -> None:
                try:
                    ban_body, ban_status = authenticated_get('/auth/me/ban')
                    print(f'[ban-check] status={ban_status} body={ban_body}')
                except Exception as e:
                    print(f'[ban-check] exception: {e}')
                    ban_body, ban_status = None, 0

                if ban_status == 200 and isinstance(ban_body, dict) and ban_body.get('banned'):
                    ban = ban_body.get('ban') or {}
                    msg = _fmt_ban_msg(ban)
                    print(f'[ban-check] user is banned, msg={msg}')

                    def _show_ban() -> None:
                        if not self._root_widget.exists():
                            print('[ban-check] root_widget gone, skipping show_ban')
                            return
                        bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1))
                        bui.textwidget(edit=self._chat_input, text=content)
                        bui.screenmessage(msg, color=(1, 0.15, 0.15))
                        bui.getsound('error').play()

                    babase.pushcall(_show_ban, from_other_thread=True)
                    return

                print(f'[ban-check] not banned, sending...')
                ok = all(ensure_global_session().send(chunk) for chunk in chunks)
                print(f'[ban-check] send result ok={ok}')

                def _apply() -> None:
                    if not self._root_widget.exists():
                        return
                    bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1))
                    if not ok:
                        bui.screenmessage('Failed to send message.', color=(1, 0.3, 0.3))

                babase.pushcall(_apply, from_other_thread=True)

            threading.Thread(target=_run_global, daemon=True).start()
        else:
            receiver_id = friend.get('friend_id')
            user = get_session().get('user', {})
            my_name = user.get('name') or user.get('nickname', '?')
            my_nick = user.get('nickname', '?')
            my_id = user.get('id', 0)
            fnick = friend.get('friend_nickname', '?')

            def _run_dm() -> None:
                ok = True
                for i, chunk in enumerate(chunks):
                    msg_id = f'dm_{int(time.time() * 1000)}_{i}'
                    if not ensure_friends_session().send_dm(receiver_id, chunk, msg_id):
                        ok = False
                        break
                    append_dm_message(receiver_id, fnick, my_id, my_nick, chunk)

                def _apply() -> None:
                    if not self._root_widget.exists():
                        return
                    bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1))
                    if ok:
                        for chunk in chunks:
                            self._add_chat_message({'name': my_name, 'content': chunk})
                    else:
                        bui.screenmessage('Failed to send message.', color=(1, 0.3, 0.3))

                babase.pushcall(_apply, from_other_thread=True)

            threading.Thread(target=_run_dm, daemon=True).start()

    def _switch_to_friend(self, friend: dict) -> None:
        self._chat_friend = friend
        nick = friend.get('friend_nickname', '?')
        fid = friend.get('friend_id')
        set_dm_chat_target({'type': 'friend', 'friend_id': fid, 'friend_nickname': nick})
        set_active_dm_chat(fid)
        if fid is not None:
            clear_unread_dm_count(fid)

        is_online = fid in get_online_friend_ids()
        bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1) if is_online else (0.4, 0.4, 0.4))
        bui.textwidget(edit=self._chat_title_widget, text=nick)
        if self._chat_back_btn is None or not self._chat_back_btn.exists():
            self._chat_back_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(268, self._height - 60),
                size=(95, 24),
                label=get_lang_text('DM.backToGlobalChat'),
                button_type='square',
                color=_theme.get_color('COLOR_BACKGROUND'),
                textcolor=_theme.get_color('COLOR_PRIMARY'),
                text_scale=0.6,
                enable_sound=True,
                on_activate_call=self._switch_to_global,
            )

        for txt in self._chat_texts:
            txt.delete()
        self._chat_texts.clear()

        if fid is not None:
            for msg in get_conversation_msgs(fid):
                self._add_chat_message({
                    'nickname': msg.get('nickname', '?'),
                    'content': msg.get('content', ''),
                })

        def _cancel_load_popup() -> None:
            self._msg_select_seq += 1
        babase.apptimer(0.05, _cancel_load_popup)

        ensure_global_session().remove_listener(self._on_realtime_message)
        if fid is not None:
            ensure_friends_session().add_dm_listener(fid, self._on_dm_message)

    def _switch_to_global(self) -> None:
        set_dm_chat_target({'type': 'global'})
        set_active_dm_chat(None)
        if self._chat_friend is not None:
            fid = self._chat_friend.get('friend_id')
            if fid is not None:
                ensure_friends_session().remove_dm_listener(fid, self._on_dm_message)
            self._chat_friend = None

        bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1))
        bui.textwidget(edit=self._chat_title_widget, text=get_lang_text('DM.globalChat'))
        if self._chat_back_btn is not None and self._chat_back_btn.exists():
            self._chat_back_btn.delete()
            self._chat_back_btn = None

        for txt in self._chat_texts:
            txt.delete()
        self._chat_texts.clear()

        session = ensure_global_session()
        session.add_listener(self._on_realtime_message)
        for msg in session.get_cache():
            self._add_chat_message(msg)

        def _cancel_load_popup() -> None:
            self._msg_select_seq += 1
        babase.apptimer(0.05, _cancel_load_popup)

    def _on_server_invite(self, invite: dict) -> None:
        if self._root_widget.exists():
            if not is_invite_blocked(invite.get('senderNickname', '?')):
                ServerInvitePopup(invite=invite)

    def _on_dm_message(self, msg: dict) -> None:
        # saving is handled by the global listener; here we only update the chat display
        if self._root_widget.exists():
            self._add_chat_message({
                'name': msg.get('senderName') or msg.get('senderNickname', '?'),
                'content': msg.get('content', ''),
            })

    def _open_add_friend(self) -> None:
        AddFriendPopup(on_done=self._load_friends)

    def _open_pending(self, initial_tab: str = 'received') -> None:
        PendingRequestsPopup(on_done=self._load_friends, initial_tab=initial_tab)

    def _open_friend_menu(self, friend: dict) -> None:
        FriendMenuPopup(
            friend=friend,
            on_done=self._load_friends,
        )

    def _fetch_initial_pending(self) -> None:
        body, status = authenticated_get('/friends/pending')
        count = len(body) if status == 200 and isinstance(body, list) else 0
        set_pending_request_count(count)
        babase.pushcall(self._update_pending_badge, from_other_thread=True)

    def _update_pending_badge(self) -> None:
        if not (self._root_widget.exists() and hasattr(self, '_pending_badge_img')):
            return
        count = get_pending_request_count()
        visible = count > 0
        bui.imagewidget(edit=self._pending_badge_img, opacity=1.0 if visible else 0.0)
        bui.textwidget(edit=self._pending_badge_num, text=str(count) if visible else '')

    def _update_unread_badges(self) -> None:
        if not self._root_widget.exists():
            return
        self._rebuild_friends()

    def _on_online_status_change(self) -> None:
        if not (self._root_widget.exists() and hasattr(self, '_friends_scroll')):
            return
        self._rebuild_friends()
        if self._chat_friend is not None and hasattr(self, '_send_btn'):
            fid = self._chat_friend.get('friend_id')
            is_online = fid in get_online_friend_ids()
            bui.buttonwidget(edit=self._send_btn, color=(1, 1, 1) if is_online else (0.4, 0.4, 0.4))

    def _open_admin_users(self) -> None:
        AdminUsersWindow()

    def _close(self) -> None:
        set_dm_window_open(False)
        set_active_dm_chat(None)
        remove_online_status_listener(self._on_online_status_change)
        remove_pending_request_listener(self._update_pending_badge)
        remove_unread_dm_listener(self._update_unread_badges)
        if is_server_online() is not False:
            try:
                ensure_global_session().remove_listener(self._on_realtime_message)
                ensure_friends_session().remove_server_invite_listener(self._on_server_invite)
                if self._chat_friend is not None:
                    fid = self._chat_friend.get('friend_id')
                    if fid is not None:
                        ensure_friends_session().remove_dm_listener(fid, self._on_dm_message)
            except Exception:
                pass
        if self._root_widget.exists():
            bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AddFriendPopup:
    """Popup to send a friend request by nickname."""

    def __init__(self, on_done=None) -> None:
        self._on_done = on_done
        uiscale = bui.app.ui_v1.uiscale
        self._width = 320
        self._height = 215

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('AddFriend.title'),
            scale=0.9,
            color=(1, 1, 1),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(13, self._height - 39),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        bui.textwidget(
            parent=self._root_widget,
            position=(14, 155),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('AddFriend.fieldLabel'),
            scale=0.7,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        self._field = bui.textwidget(
            parent=self._root_widget,
            position=(14, 105),
            size=(self._width - 28, 36),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=50,
            maxwidth=self._width - 38,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=4,
            description="Nickname or 10-digit UID",
            on_return_press_call=self._send,
        )

        self._btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(14, 16),
            size=(self._width - 28, 52),
            label=get_lang_text('AddFriend.sendRequest'),
            color=(0.2, 0.5, 0.2),
            textcolor=(1, 1, 1),
            on_activate_call=self._send,
        )

    def _send(self) -> None:
        query = bui.textwidget(query=self._field)
        if not query:
            bui.screenmessage(get_lang_text('AddFriend.enterField'), color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        bui.buttonwidget(edit=self._btn, label=get_lang_text('AddFriend.sending'), color=(0.3, 0.3, 0.3))

        def _run() -> None:
            if query.isdigit() and len(query) == 10:
                payload = {'uid': query}
            else:
                payload = {'name': query}
            body, status = authenticated_post('/friends/', payload)

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(edit=self._btn, label=get_lang_text('AddFriend.sendRequest'), color=(0.2, 0.5, 0.2))
                if status == 201:
                    nick = isinstance(body, dict) and body.get('friend_nickname') or query
                    bui.screenmessage(get_lang_text('GlobalChat.requestSent').format(nick=nick), color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                    self._close()
                elif status == 409:
                    bui.screenmessage(get_lang_text('GlobalChat.alreadyFriends'), color=(1, 0.5, 0))
                    bui.getsound('error').play()
                elif status == 404:
                    bui.screenmessage(get_lang_text('GlobalChat.userNotFound'), color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                elif status == 400:
                    bui.screenmessage(body.get('error', 'Invalid request.'), color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()
        if self._on_done:
            self._on_done()


class PendingRequestsPopup:
    """Popup with tabs for received and sent friend requests."""

    from enum import Enum

    class _Tab(Enum):
        RECEIVED = 'received'
        SENT = 'sent'

    def __init__(self, on_done=None, initial_tab: str = 'received') -> None:
        from bauiv1lib.tabs import TabRow

        self._on_done = on_done
        self._received: list[dict] = []
        self._sent: list[dict] = []
        self._current_tab = self._Tab.SENT if initial_tab == 'sent' else self._Tab.RECEIVED
        uiscale = bui.app.ui_v1.uiscale
        self._width = 360
        _base_h = int(430 * 0.9)
        self._height = int(_base_h * 0.8) if uiscale is babase.UIScale.SMALL else _base_h

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 22),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('DM.requests'),
            scale=0.9,
            color=(1, 1, 1),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(13, self._height - 44),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        tabdefs = [
            (self._Tab.RECEIVED, bui.Lstr(value=get_lang_text('DM.requestsReceived'))),
            (self._Tab.SENT, bui.Lstr(value=get_lang_text('DM.requestsSent'))),
        ]
        self._tab_row = TabRow(
            self._root_widget,
            tabdefs,
            idprefix='pending_requests',
            size=(self._width - 20, 36),
            pos=(10, self._height - 102),
            on_select_call=self._set_tab,
        )
        self._tab_row.update_appearance(self._current_tab)

        _accent = _theme.get_color('COLOR_ACCENT')
        _primary = _theme.get_color('COLOR_PRIMARY')
        for tab in self._tab_row.tabs.values():
            bui.buttonwidget(edit=tab.button, color=_accent, textcolor=_primary)

        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(10, 26),
            size=(self._width - 20, self._height - 124),
            background=False,
            highlight=False,
        )

        self._container = bui.containerwidget(
            parent=self._scroll,
            size=(self._width - 40, 20),
            background=False,
        )

        self._load()

    def _set_tab(self, tab_id: str) -> None:
        self._current_tab = tab_id
        self._tab_row.update_appearance(tab_id)
        _accent = _theme.get_color('COLOR_ACCENT')
        _primary = _theme.get_color('COLOR_PRIMARY')
        for tab in self._tab_row.tabs.values():
            bui.buttonwidget(edit=tab.button, color=_accent, textcolor=_primary)
        self._rebuild()

    def _load(self) -> None:
        def _run() -> None:
            recv_body, recv_st = authenticated_get('/friends/pending')
            sent_body, sent_st = authenticated_get('/friends/sent')
            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                self._received = recv_body if recv_st == 200 and isinstance(recv_body, list) else []
                self._sent = sent_body if sent_st == 200 and isinstance(sent_body, list) else []
                self._rebuild()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _rebuild(self) -> None:
        if not self._root_widget.exists():
            return
        if self._current_tab == self._Tab.RECEIVED:
            self._rebuild_list(self._received, sent=False)
        else:
            self._rebuild_list(self._sent, sent=True)

    def _rebuild_list(self, items: list[dict], sent: bool) -> None:
        inner_w = self._width - 40
        row_h = 48
        total_h = max(len(items) * row_h + 8, 40)

        self._container.delete()
        self._container = bui.containerwidget(
            parent=self._scroll,
            size=(inner_w, total_h),
            background=False,
        )

        if not items:
            empty_key = 'DM.noSentRequests' if sent else 'DM.noRequests'
            bui.textwidget(
                parent=self._container,
                position=(inner_w * 0.5, total_h * 0.5),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=get_lang_text(empty_key),
                scale=0.75,
                color=(0.5, 0.5, 0.5),
            )
            return

        y = total_h - row_h
        for req in items:
            nick = req.get('friend_nickname', '?')
            uid = req.get('user_id', 0) if not sent else req.get('friend_id', 0)

            bui.textwidget(
                parent=self._container,
                position=(6, y + row_h / 2),
                size=(0, 0),
                h_align='left',
                v_align='center',
                text=nick,
                scale=0.8,
                color=(0.9, 0.9, 0.9),
                maxwidth=inner_w - 150,
            )

            if sent:
                bui.buttonwidget(
                    parent=self._container,
                    position=(inner_w - 80, y + 8),
                    size=(72, 32),
                    label=get_lang_text('FriendRequest.cancel'),
                    color=(0.5, 0.2, 0.1),
                    textcolor=(1, 1, 1),
                    enable_sound=True,
                    on_activate_call=lambda u=uid, n=nick: self._cancel(u, n),
                )
            else:
                bui.buttonwidget(
                    parent=self._container,
                    position=(inner_w - 148, y + 8),
                    size=(62, 32),
                    label=get_lang_text('FriendRequest.accept'),
                    color=(0.2, 0.6, 0.2),
                    textcolor=(1, 1, 1),
                    enable_sound=True,
                    on_activate_call=lambda u=uid, n=nick: self._accept(u, n),
                )
                bui.buttonwidget(
                    parent=self._container,
                    position=(inner_w - 70, y + 8),
                    size=(62, 32),
                    label=get_lang_text('FriendRequest.reject'),
                    color=(0.6, 0.2, 0.2),
                    textcolor=(1, 1, 1),
                    enable_sound=True,
                    on_activate_call=lambda u=uid, n=nick: self._reject(u, n),
                )

            y -= row_h

    def _accept(self, uid: int, nick: str) -> None:
        def _run() -> None:
            _, status = authenticated_post(f'/friends/requests/{uid}/accept')

            def _apply() -> None:
                if status == 200:
                    bui.screenmessage(get_lang_text('FriendRequest.accepted').format(nick=nick), color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                    set_pending_request_count(max(0, get_pending_request_count() - 1))
                    self._load()
                else:
                    bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _reject(self, uid: int, nick: str) -> None:
        def _run() -> None:
            _, status = authenticated_post(f'/friends/requests/{uid}/reject')

            def _apply() -> None:
                if status in (200, 204):
                    bui.screenmessage(get_lang_text('FriendRequest.rejected').format(nick=nick), color=(0.7, 0.7, 0.7))
                    bui.getsound('swish').play()
                    set_pending_request_count(max(0, get_pending_request_count() - 1))
                    self._load()
                else:
                    bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _cancel(self, friend_id: int, nick: str) -> None:
        def _run() -> None:
            _, status = authenticated_delete(f'/friends/{friend_id}')

            def _apply() -> None:
                if status in (200, 204):
                    bui.screenmessage(get_lang_text('FriendRequest.cancelled').format(nick=nick), color=(0.7, 0.7, 0.7))
                    bui.getsound('swish').play()
                    self._load()
                else:
                    bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()
        if self._on_done:
            self._on_done()


class FriendMenuPopup:
    """Small popup menu for actions on a friend."""

    def __init__(self, friend: dict, on_done=None) -> None:
        self._friend = friend
        self._on_done = on_done
        uiscale = bui.app.ui_v1.uiscale
        self._width = 260

        caller_role = get_session().get('user', {}).get('role', 'USER')
        is_admin_or_manager = caller_role in ('ADMIN', 'MANAGER')
        self._height = 320 if is_admin_or_manager else 220

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        nick = friend.get('friend_nickname', '?')

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 35),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=nick,
            scale=1.2,
            color=(1, 1, 1),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(13, self._height - 48),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        fx = 14
        fw = self._width - 28
        is_online = friend.get('friend_id') in get_online_friend_ids()

        # admin/manager actions at the top
        if is_admin_or_manager:
            bui.buttonwidget(
                parent=self._root_widget,
                position=(fx, 216),
                size=(fw, 38),
                label=get_lang_text('Admin.banUser'),
                color=(0.55, 0.1, 0.1),
                textcolor=(1, 1, 1),
                enable_sound=True,
                on_activate_call=self._open_ban,
            )
            bui.buttonwidget(
                parent=self._root_widget,
                position=(fx, 166),
                size=(fw, 38),
                label=get_lang_text('Admin.changeRole'),
                color=(0.2, 0.28, 0.45),
                textcolor=(0.6, 0.7, 1.0),
                enable_sound=True,
                on_activate_call=self._open_change_role,
            )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(fx, 116),
            size=(fw, 38),
            label=get_lang_text('FriendMenu.inviteToGame'),
            color=(0.45, 0.3, 0.15) if is_online else (0.28, 0.28, 0.28),
            textcolor=(1.0, 0.85, 0.5) if is_online else (0.45, 0.45, 0.45),
            enable_sound=True,
            on_activate_call=self._invite_to_game if is_online else self._friend_offline,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(fx, 66),
            size=(fw, 38),
            label=get_lang_text('FriendMenu.viewAccount'),
            color=(0.25, 0.3, 0.45),
            textcolor=(0.6, 0.6, 0.9),
            enable_sound=True,
            on_activate_call=lambda: FriendAccountPopup(friend=friend),
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(fx, 16),
            size=(fw, 38),
            label=get_lang_text('FriendMenu.removeFriend'),
            color=(0.55, 0.15, 0.15),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._remove,
        )

    def _friend_offline(self) -> None:
        bui.screenmessage('Friend is offline.', color=(0.6, 0.6, 0.6))
        bui.getsound('error').play()

    def _remove(self) -> None:
        nick = self._friend.get('friend_nickname', '?')
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('FriendMenu.removeConfirm').format(nick=nick),
            action=self._do_remove,
            ok_text=get_lang_text('FriendMenu.removeFriend'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1, 0.7, 0.7),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_remove(self) -> None:
        fid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')

        def _run() -> None:
            _, status = authenticated_delete(f'/friends/{fid}')

            def _apply() -> None:
                if status in (200, 204):
                    bui.screenmessage(get_lang_text('FriendMenu.removed').format(nick=nick), color=(0.8, 0.5, 0.5))
                    bui.getsound('shieldDown').play()
                    self._close()
                else:
                    bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _invite_to_game(self) -> None:
        import bascenev1 as bs
        info = bs.get_connection_to_host_info_2()
        if info is None or not info.address:
            bui.screenmessage('Not connected to any server.', color=(1, 0.6, 0.2))
            bui.getsound('error').play()
            return

        receiver_id = self._friend.get('friend_id')
        name = info.name or 'BombSquad Server'
        ip = info.address
        port = str(info.port)

        def _run() -> None:
            ok = ensure_friends_session().send_server_invite(receiver_id, name, ip, port)

            def _apply() -> None:
                if ok:
                    nick = self._friend.get('friend_nickname', '?')
                    bui.screenmessage(f'Invitation sent to {nick}!', color=(0.5, 1.0, 0.5))
                    bui.getsound('cashRegister').play()
                else:
                    bui.screenmessage('Failed to send invitation.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _open_ban(self) -> None:
        AdminBanPopup(friend=self._friend)

    def _open_change_role(self) -> None:
        AdminChangeRolePopup(friend=self._friend)

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()
        if self._on_done:
            self._on_done()


class ServerInvitePopup:
    """Popup shown when a friend sends a game server invitation."""

    def __init__(self, invite: dict) -> None:
        self._invite = invite
        self._block_checked = False
        uiscale = bui.app.ui_v1.uiscale
        self._width = 300
        self._height = 185

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        server_name = invite.get('serverName', 'Unknown Server')
        ip = invite.get('serverIp', '')
        port = invite.get('serverPort', '')
        sender = invite.get('senderNickname', '?')
        self._sender_nick = sender

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 22),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=server_name,
            scale=0.9,
            color=(1, 1, 1),
            maxwidth=self._width - 20,
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 46),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('InviteWindow.invitedBy').format(sender=sender),
            scale=0.62,
            color=(0.6, 0.6, 0.6),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 72),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=f'{ip}:{port}',
            scale=0.7,
            color=(0.5, 0.85, 0.65),
        )

        chk = bui.checkboxwidget(
            parent=self._root_widget,
            position=(14, 76),
            size=(self._width - 28, 26),
            text=get_lang_text('InviteWindow.dontShow').format(sender=sender, min=_INVITE_BLOCK_DEFAULT_MINUTES),
            scale=0.65,
            value=False,
            textcolor=(0.75, 0.75, 0.5),
            maxwidth=self._width - 55,
        )
        bui.checkboxwidget(
            edit=chk,
            on_value_change_call=lambda v: setattr(self, '_block_checked', bool(v)),
        )

        half = (self._width - 28) * 0.5 - 4
        bui.buttonwidget(
            parent=self._root_widget,
            position=(14, 16),
            size=(half, 50),
            label=get_lang_text('FriendRequest.accept'),
            color=(0.2, 0.6, 0.2),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._accept,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(14 + half + 8, 16),
            size=(half, 50),
            label=get_lang_text('FriendRequest.reject'),
            color=(0.55, 0.15, 0.15),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._close,
        )

    def _apply_block_if_checked(self) -> None:
        if self._block_checked:
            set_invite_block(self._sender_nick, _INVITE_BLOCK_DEFAULT_MINUTES)

    def _accept(self) -> None:
        self._apply_block_if_checked()
        ip = self._invite.get('serverIp', '')
        port = self._invite.get('serverPort', '0')
        try:
            from bascenev1 import connect_to_party
            connect_to_party(ip, int(port), False)
        except Exception as e:
            bui.screenmessage(f'Could not connect: {e}', color=(1, 0.3, 0.3))
        self._close_widget()

    def _close(self) -> None:
        self._apply_block_if_checked()
        self._close_widget()

    def _close_widget(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class FriendAccountPopup:
    """Shows basic account info of a friend."""

    def __init__(
        self,
        friend: dict,
        is_friend: bool = True,
        uid_str: str = '',
        pending_status: str = 'none',
        on_pending_click=None,
    ) -> None:
        from datetime import datetime, timezone
        uiscale = bui.app.ui_v1.uiscale
        self._width = 280
        nick = friend.get('friend_nickname', '?')
        self._nick = nick
        self._is_friend = is_friend
        self._uid_str = uid_str
        self._pending_status = pending_status
        self._on_pending_click = on_pending_click
        self._nickname_loaded: str | None = None

        block = get_invite_block(nick) if is_friend else None
        block_h = 78 if block else 0
        btn_h = 48
        bottom_h = (btn_h + 12) if not is_friend else block_h
        self._height = (195 if block else 193) + bottom_h
        self._block_timer: bui.AppTimer | None = None
        self._v2_account: str | None = None

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(18, self._height - 38),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        self._v2_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 112, self._height - 38),
            size=(98, 28),
            label='...',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.6,
            enable_sound=True,
            opacity=0.0,
            on_activate_call=self._open_v2_profile,
        )
        self._back_btn = back_btn
        self._popup_type = 'block'
        self._rendered_height = self._height
        self._desc_lift = 0

        if is_friend and not block:
            self._block_invite_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(54, self._height - 48),
                size=(58, 28),
                label=get_lang_text('InviteBlock.blockBtn'),
                color=(0.55, 0.1, 0.1),
                textcolor=_theme.get_color('COLOR_PRIMARY'),
                text_scale=0.55,
                enable_sound=True,
                on_activate_call=self._show_block_new_popup,
            )

        # spaz icon
        icon_size = 64
        icon_x = 14
        icon_y = self._height - 125
        self._icon_widget = bui.imagewidget(
            parent=self._root_widget,
            position=(icon_x, icon_y),
            size=(icon_size, icon_size),
            texture=bui.gettexture('neoSpazIcon'),
            tint_texture=bui.gettexture('neoSpazIconColorMask'),
            mask_texture=bui.gettexture('characterIconMask'),
            tint_color=_theme.get_color('COLOR_PRIMARY'),
            tint2_color=_theme.get_color('COLOR_SECONDARY'),
        )

        # info rows
        info_x = icon_x + icon_size - 35
        cont_w = self._width - info_x - 8
        self._info_container = info_container = bui.containerwidget(
            parent=self._root_widget,
            size=(cont_w, 75),
            position=(info_x, icon_y - 8),
            background=False,
        )
        label_w = 58
        row_gap = 20
        items = [
            (f'{get_lang_text("ManageAccount.nickname")}:', nick or '...'),
            (f'{get_lang_text("ProfileSearchWindow.name")}:', '...'),
            (f'{get_lang_text("Global.uid")}:', f'#{uid_str}' if uid_str else '...'),
        ]
        self._name_row_idx = 1
        self._uid_row_idx = 2
        self._info_rows: list[bui.Widget] = []
        for i, (lbl, val) in enumerate(items):
            y = 60 - i * row_gap - (8 if i == 0 else 7)
            raw = val.lstrip('@#')
            bui.textwidget(
                parent=info_container,
                text=lbl,
                color=_theme.get_color('COLOR_PRIMARY'),
                position=(32, y),
                size=(label_w, 20),
                h_align='left', v_align='top',
                scale=0.62, maxwidth=label_w, max_height=18,
            )
            vw = bui.textwidget(
                parent=info_container,
                text=val,
                color=_theme.get_color('COLOR_SECONDARY'),
                position=(label_w + 17, y),
                size=(cont_w - label_w, 20),
                h_align='left', v_align='top',
                scale=0.62, maxwidth=cont_w - label_w, max_height=18,
                selectable=True, click_activate=True, glow_type='uniform',
                on_activate_call=lambda v=raw: (
                    bui.clipboard_set_text(v),
                    bui.screenmessage(
                        get_lang_text('Global.copiedToClipboard'),
                        color=(0.6, 1.0, 0.6),
                    ),
                    bui.getsound('dingSmall').play(),
                ),
            )
            self._info_rows.append(vw)

        # horizontal divider
        self._divider_widget = bui.imagewidget(
            parent=self._root_widget,
            position=(14, icon_y - 8),
            size=(self._width - 28, 1),
            texture=bui.gettexture('white'),
            color=_theme.get_color('COLOR_ACCENT'),
        )

        # description
        fw_desc = self._width - 28
        self._desc_widget = bui.textwidget(
            parent=self._root_widget,
            position=((self._width - fw_desc) / 2, icon_y - 78),
            size=(fw_desc, 55),
            h_align='center', v_align='top',
            text='',
            scale=0.58,
            color=_theme.get_color('COLOR_SECONDARY'),
            maxwidth=fw_desc,
        )

        # block section
        if block:
            try:
                until = datetime.fromisoformat(block['until'])
                self._block_until = until
                remaining_s = max(0, int((until - datetime.now(timezone.utc)).total_seconds()))
            except Exception:
                self._block_until = datetime.now(timezone.utc)
                remaining_s = 0

            mins, secs = divmod(remaining_s, 60)
            timer_text = (
                get_lang_text('InviteBlock.statusMins').format(mins=mins, secs=secs)
                if mins > 0
                else get_lang_text('InviteBlock.statusSecs').format(secs=secs)
            )
            self._block_label = bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.5, block_h - 5),
                size=(0, 0),
                h_align='center', v_align='center',
                text=timer_text, scale=0.62,
                color=(1.0, 0.7, 0.3),
                maxwidth=self._width - 20,
            )
            row_y = block_h - 45
            _half = (self._width - 28) // 2 - 4
            self._block_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(14, row_y), size=(_half, 26),
                label=f'{max(1, (remaining_s + 59) // 60)} min',
                color=_theme.get_color('COLOR_BUTTON'),
                textcolor=_theme.get_color('COLOR_PRIMARY'),
                enable_sound=True,
                on_activate_call=self._show_block_minutes_popup,
            )
            self._remove_block_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(14 + _half + 8, row_y), size=(_half, 26),
                label=get_lang_text('InviteBlock.removeBlock'),
                color=(0.5, 0.15, 0.15), textcolor=(1, 1, 1),
                enable_sound=True, on_activate_call=self._remove_block,
            )
            if remaining_s > 0:
                self._block_timer = bui.AppTimer(1.0, self._update_block_timer, repeat=True)

        # action button for non-friends
        if not is_friend:
            is_pending = pending_status in ('pending_sent', 'pending_received')
            if is_pending:
                self._add_btn = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(14, 12), size=(self._width - 28, btn_h),
                    label=get_lang_text('GlobalChat.requestPending'),
                    color=(0.6, 0.35, 0.0), textcolor=(1, 1, 1),
                    enable_sound=True, on_activate_call=self._open_pending,
                )
            else:
                self._add_btn = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(14, 12), size=(self._width - 28, btn_h),
                    label=get_lang_text('GlobalChat.sendFriendRequest'),
                    color=(0.2, 0.5, 0.2), textcolor=(1, 1, 1),
                    enable_sound=True, on_activate_call=self._add_friend,
                )

        self._load(friend)

    def _open_pending(self) -> None:
        self._close()
        if self._on_pending_click:
            tab = 'sent' if self._pending_status == 'pending_sent' else 'received'
            self._on_pending_click(tab)

    def _add_friend(self) -> None:
        uid = self._uid_str or (self._nickname_loaded or '')
        if not uid:
            bui.screenmessage(get_lang_text('GlobalChat.loadError'), color=(1, 0.5, 0))
            bui.getsound('error').play()
            return
        nick = self._nickname_loaded or uid
        bui.buttonwidget(edit=self._add_btn, label=get_lang_text('GlobalChat.sending'), color=(0.3, 0.3, 0.3))
        payload = {'uid': self._uid_str} if self._uid_str else {'friendNickname': nick}

        def _run() -> None:
            _, status = authenticated_post('/friends/', payload)

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                if status == 201:
                    bui.screenmessage(
                        get_lang_text('GlobalChat.requestSent').format(nick=nick),
                        color=(0, 1, 0),
                    )
                    bui.getsound('cashRegister').play()
                    bui.buttonwidget(
                        edit=self._add_btn,
                        label=get_lang_text('GlobalChat.requestPending'),
                        color=(0.6, 0.35, 0.0),
                        on_activate_call=self._open_pending,
                    )
                else:
                    bui.buttonwidget(
                        edit=self._add_btn,
                        label=get_lang_text('GlobalChat.sendFriendRequest'),
                        color=(0.2, 0.5, 0.2),
                    )
                    if status == 409:
                        bui.screenmessage(get_lang_text('GlobalChat.alreadyFriends'), color=(1, 0.5, 0))
                        bui.getsound('error').play()
                    elif status == 404:
                        bui.screenmessage(get_lang_text('GlobalChat.userNotFound'), color=(1, 0.3, 0.3))
                        bui.getsound('error').play()
                    else:
                        bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                        bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _show_block_minutes_popup(self) -> None:
        choices = ['5', '10', '20', '30', '45', '60', '120', '300']
        _ThemedPopupMenu(
            position=self._block_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            current_choice=choices[0],
            delegate=self,
            width=190.0,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        )

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        from datetime import datetime, timezone, timedelta
        minutes = max(1, min(int(choice), _INVITE_BLOCK_MAX_MINUTES))
        if self._popup_type == 'blockNew':
            from bauiv1lib.confirm import ConfirmWindow
            confirm = ConfirmWindow(
                text=get_lang_text('InviteBlock.confirmBlock').format(nick=self._nick, min=minutes),
                action=babase.Call(self._apply_new_block, minutes),
                ok_text=get_lang_text('InviteBlock.blockBtn'),
                cancel_text=bui.Lstr(resource='cancelText'),
            )
            bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))
            return
        set_invite_block(self._nick, minutes)
        self._block_until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        remaining_s = minutes * 60
        mins, secs = divmod(remaining_s, 60)
        timer_text = (
            get_lang_text('InviteBlock.statusMins').format(mins=mins, secs=secs) if mins > 0
            else get_lang_text('InviteBlock.statusSecs').format(secs=secs)
        )
        if self._block_label.exists():
            bui.textwidget(edit=self._block_label, text=timer_text)
        if self._block_btn.exists():
            bui.buttonwidget(edit=self._block_btn, label=f'{mins}m' if mins > 0 else f'{secs}s')
        if not self._block_timer:
            self._block_timer = bui.AppTimer(1.0, self._update_block_timer, repeat=True)
        bui.screenmessage(get_lang_text('InviteBlock.blockedFor').format(min=minutes), color=(1.0, 0.7, 0.3))
        bui.getsound('ding').play()

    def _show_block_new_popup(self) -> None:
        choices = ['5', '10', '20', '30', '45', '60', '120', '300']
        self._popup_type = 'blockNew'
        _ThemedPopupMenu(
            position=self._block_invite_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            current_choice=choices[0],
            delegate=self,
            width=190.0,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        )

    def _apply_new_block(self, minutes: int) -> None:
        from datetime import datetime, timezone, timedelta
        if not self._root_widget.exists():
            return
        set_invite_block(self._nick, minutes)
        self._popup_type = 'block'
        if hasattr(self, '_block_invite_btn') and self._block_invite_btn.exists():
            self._block_invite_btn.delete()

        # grow container
        _block_h = 80
        _cur_h = self._rendered_height
        _new_h = _cur_h + _block_h
        _iy = _new_h - 125
        _fw = self._width - 28
        bui.containerwidget(edit=self._root_widget, size=(self._width, _new_h))
        bui.buttonwidget(edit=self._back_btn, position=(18, _new_h - 48))
        bui.buttonwidget(edit=self._v2_btn, position=(self._width - 112, _new_h - 48))
        bui.imagewidget(edit=self._icon_widget, position=(14, _iy))
        bui.containerwidget(edit=self._info_container, position=(43, _iy - 8))
        bui.imagewidget(edit=self._divider_widget, position=(14, _iy - 8))
        bui.textwidget(edit=self._desc_widget, position=(14, _iy - 78 + self._desc_lift))
        self._rendered_height = _new_h

        # create block section at the bottom
        remaining_s = minutes * 60
        mins, secs = divmod(remaining_s, 60)
        timer_text = (
            get_lang_text('InviteBlock.statusMins').format(mins=mins, secs=secs) if mins > 0
            else get_lang_text('InviteBlock.statusSecs').format(secs=secs)
        )
        self._block_until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        self._block_label = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, _block_h - 5),
            size=(0, 0),
            h_align='center', v_align='center',
            text=timer_text, scale=0.62,
            color=(1.0, 0.7, 0.3),
            maxwidth=self._width - 20,
        )
        _row_y = _block_h - 45
        _half = (self._width - 28) // 2 - 4
        self._block_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(14, _row_y), size=(_half, 26),
            label=f'{mins}m' if mins > 0 else f'{secs}s',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            enable_sound=True,
            on_activate_call=self._show_block_minutes_popup,
        )
        self._remove_block_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(14 + _half + 8, _row_y), size=(_half, 26),
            label=get_lang_text('InviteBlock.removeBlock'),
            color=(0.5, 0.15, 0.15), textcolor=(1, 1, 1),
            enable_sound=True, on_activate_call=self._remove_block,
        )
        if remaining_s > 0:
            self._block_timer = bui.AppTimer(1.0, self._update_block_timer, repeat=True)
        bui.screenmessage(get_lang_text('InviteBlock.blockedFor').format(min=minutes), color=(1.0, 0.7, 0.3))
        bui.getsound('ding').play()

    def popup_menu_closing(self, popup_window: PopupMenuWindow) -> None:
        pass

    def _remove_block(self) -> None:
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('InviteBlock.confirmRemove').format(nick=self._nick),
            action=self._do_remove_block,
            ok_text=get_lang_text('InviteBlock.removeBlock'),
            cancel_text=bui.Lstr(resource='cancelText'),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_remove_block(self) -> None:
        clear_invite_block(self._nick)
        self._block_timer = None
        for _w in ('_block_label', '_block_btn', '_remove_block_btn'):
            _widget = getattr(self, _w, None)
            if _widget and _widget.exists():
                _widget.delete()
        _new_h = self._rendered_height - 80
        _iy = _new_h - 125
        bui.containerwidget(edit=self._root_widget, size=(self._width, _new_h))
        bui.buttonwidget(edit=self._back_btn, position=(18, _new_h - 48))
        bui.buttonwidget(edit=self._v2_btn, position=(self._width - 112, _new_h - 48))
        bui.imagewidget(edit=self._icon_widget, position=(14, _iy))
        bui.containerwidget(edit=self._info_container, position=(43, _iy - 8))
        bui.imagewidget(edit=self._divider_widget, position=(14, _iy - 8))
        bui.textwidget(edit=self._desc_widget, position=(14, _iy - 78 + self._desc_lift))
        self._rendered_height = _new_h
        self._popup_type = 'block'
        self._block_invite_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(54, _new_h - 48),
            size=(58, 28),
            label=get_lang_text('InviteBlock.blockBtn'),
            color=(0.55, 0.1, 0.1),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.55,
            enable_sound=True,
            on_activate_call=self._show_block_new_popup,
        )
        bui.screenmessage(get_lang_text('InviteBlock.blockRemoved'), color=(0.5, 1.0, 0.5))
        bui.getsound('shieldDown').play()

    def _open_v2_profile(self) -> None:
        if not self._v2_account:
            return
        ProfileSearchWindow(source_widget=self._root_widget, v2=self._v2_account)

    def _load(self, friend: dict) -> None:
        fid = friend.get('friend_id')

        def _run() -> None:
            body, status = authenticated_get(f'/users/{fid}')

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                import textwrap as _tw
                if status == 200 and isinstance(body, dict):
                    v2 = body.get('v2') or ''
                    self._v2_account = v2 if v2 else None
                    self._nickname_loaded = body.get('nickname', '') or None
                    name = body.get('name', '').strip()
                    uid = body.get('uid', self._uid_str)
                    description = (body.get('description') or '').strip()
                    if len(description) > 150:
                        description = description[:147] + '...'
                    # update name row
                    if len(self._info_rows) > self._name_row_idx:
                        name_w = self._info_rows[self._name_row_idx]
                        if name_w.exists():
                            bui.textwidget(edit=name_w, text=f'@{name}' if name else '')
                    # update uid row
                    if len(self._info_rows) > self._uid_row_idx:
                        uid_w = self._info_rows[self._uid_row_idx]
                        if uid_w.exists():
                            bui.textwidget(edit=uid_w, text=f'#{uid}' if uid else '')
                    _line_count = 1
                    if description:
                        _lines, _words, _cur = [], description.split(), ''
                        for _w in _words:
                            while len(_w) > 0:
                                _space = ' ' if _cur else ''
                                _avail = 37 - len(_cur) - len(_space)
                                if len(_w) <= _avail:
                                    _cur += _space + _w
                                    _w = ''
                                elif _avail >= 2:
                                    _lines.append(_cur + _space + _w[:_avail - 1] + '-')
                                    _cur, _w = '', _w[_avail - 1:]
                                else:
                                    _lines.append(_cur)
                                    _cur = ''
                        if _cur:
                            _lines.append(_cur)
                        _line_count = len(_lines)
                        desc_txt = '\n'.join(_lines)
                    else:
                        desc_txt = get_lang_text('DM.noDescription')
                    if _line_count <= 1:
                        _extra_h = -7
                        _desc_lift = 25
                    elif _line_count == 2:
                        _extra_h = 0
                        _desc_lift = 20
                    elif _line_count == 3:
                        _extra_h = 10
                        _desc_lift = 8
                    elif _line_count == 5:
                        _extra_h = 10 + (_line_count - 3) * 14
                        _desc_lift = -10
                    else:
                        _extra_h = 10 + (_line_count - 3) * 14
                        _desc_lift = 0
                    _fw = self._width - 28
                    if _extra_h != 0 and self._root_widget.exists():
                        _new_h = self._height + _extra_h
                        self._rendered_height = _new_h
                        _iy = _new_h - 125
                        bui.containerwidget(edit=self._root_widget, size=(self._width, _new_h))
                        bui.buttonwidget(edit=self._back_btn, position=(18, _new_h - 48))
                        bui.buttonwidget(edit=self._v2_btn, position=(self._width - 112, _new_h - 48))
                        if hasattr(self, '_block_invite_btn') and self._block_invite_btn.exists():
                            bui.buttonwidget(edit=self._block_invite_btn, position=(54, _new_h - 48))
                        bui.imagewidget(edit=self._icon_widget, position=(14, _iy))
                        bui.containerwidget(edit=self._info_container, position=(43, _iy - 8))
                        bui.imagewidget(edit=self._divider_widget, position=(14, _iy - 8))
                        self._desc_lift = _desc_lift
                        bui.textwidget(edit=self._desc_widget, position=(14, _iy - 78 + _desc_lift), size=(_fw, max(20, 55 + _extra_h)))
                    elif _desc_lift != 0 and self._desc_widget.exists():
                        _iy = self._height - 125
                        self._desc_lift = _desc_lift
                        bui.textwidget(edit=self._desc_widget, position=(14, _iy - 78 + _desc_lift))
                    if v2 and self._v2_btn.exists():
                        bui.buttonwidget(edit=self._v2_btn, label=f'{V2_LOGO} {v2}', opacity=1.0)
                else:
                    desc_txt = get_lang_text('GlobalChat.loadError')
                if self._desc_widget.exists():
                    bui.textwidget(edit=self._desc_widget, text=desc_txt)

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _update_block_timer(self) -> None:
        from datetime import datetime, timezone
        if not self._root_widget.exists():
            self._block_timer = None
            return
        remaining_s = max(0, int((self._block_until - datetime.now(timezone.utc)).total_seconds()))
        if remaining_s <= 0:
            bui.textwidget(edit=self._block_label, text=get_lang_text('InviteBlock.blockRemoved'))
            self._block_timer = None
            return
        mins, secs = divmod(remaining_s, 60)
        text = (
            get_lang_text('InviteBlock.statusMins').format(mins=mins, secs=secs) if mins > 0
            else get_lang_text('InviteBlock.statusSecs').format(secs=secs)
        )
        bui.textwidget(edit=self._block_label, text=text)
        if self._block_btn.exists():
            bui.buttonwidget(edit=self._block_btn, label=f'{mins}m' if mins > 0 else f'{secs}s')

    def _close(self) -> None:
        self._block_timer = None
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class GlobalSenderPopup:
    """Shows the profile of a global chat sender and allows adding them as friend."""

    def __init__(
        self,
        user_id: int,
        display_name: str,
        uid_str: str = '',
        is_friend: bool = False,
        pending_status: str = 'none',
        on_pending_click=None,
    ) -> None:
        self._user_id = user_id
        self._uid_str = uid_str
        self._is_friend = is_friend
        self._nickname: str | None = None
        self._on_pending_click = on_pending_click
        self._pending_status = pending_status
        uiscale = bui.app.ui_v1.uiscale
        self._width = 280
        is_pending = pending_status in ('pending_sent', 'pending_received')
        self._height = 220 if is_friend else 240

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=display_name,
            scale=0.95,
            color=(0.6, 0.95, 0.6),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(8, self._height - 39),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        bui.imagewidget(
            parent=self._root_widget,
            position=(self._width * 0.5 - 28, self._height - 115),
            size=(56, 56),
            texture=bui.gettexture('cuteSpaz'),
        )

        info_y = 80 if not is_friend else 90
        self._info_text = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, info_y),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('GlobalChat.loading'),
            scale=0.7,
            color=(0.7, 0.7, 0.7),
        )

        if not is_friend:
            if is_pending:
                self._add_btn = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(14, 16),
                    size=(self._width - 28, 42),
                    label=get_lang_text('GlobalChat.requestPending'),
                    color=(0.6, 0.35, 0.0),
                    textcolor=(1, 1, 1),
                    enable_sound=True,
                    on_activate_call=self._open_pending,
                )
            else:
                self._add_btn = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(14, 16),
                    size=(self._width - 28, 42),
                    label=get_lang_text('GlobalChat.sendFriendRequest'),
                    color=(0.2, 0.5, 0.2),
                    textcolor=(1, 1, 1),
                    enable_sound=True,
                    on_activate_call=self._add_friend,
                )

        self._load()

    def _load(self) -> None:
        def _run() -> None:
            body, status = authenticated_get(f'/users/{self._user_id}')

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                if status == 200 and isinstance(body, dict):
                    self._nickname = body.get('nickname', '')
                    uid = body.get('uid', self._uid_str)
                    lines = []
                    nick = body.get('nickname', '').strip()
                    if nick:
                        lines.append(f'@{nick}')
                    if uid:
                        lines.append(f'#{uid}')
                    v2 = body.get('v2') or ''
                    if v2:
                        lines.append(f'{V2_LOGO} {v2}')
                    info = '\n'.join(lines) if lines else ''
                else:
                    info = get_lang_text('GlobalChat.loadError')
                bui.textwidget(edit=self._info_text, text=info)

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _open_pending(self) -> None:
        self._close()
        if self._on_pending_click:
            tab = 'sent' if self._pending_status == 'pending_sent' else 'received'
            self._on_pending_click(tab)

    def _add_friend(self) -> None:
        uid = self._uid_str or (self._nickname or '')
        if not uid:
            bui.screenmessage(get_lang_text('GlobalChat.loadError'), color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        nick = self._nickname or uid
        bui.buttonwidget(edit=self._add_btn, label=get_lang_text('GlobalChat.sending'), color=(0.3, 0.3, 0.3))

        payload = {'uid': self._uid_str} if self._uid_str else {'friendNickname': nick}

        def _run() -> None:
            _, status = authenticated_post('/friends/', payload)

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                if status == 201:
                    bui.screenmessage(
                        get_lang_text('GlobalChat.requestSent').format(nick=nick),
                        color=(0, 1, 0),
                    )
                    bui.getsound('cashRegister').play()
                    bui.buttonwidget(
                        edit=self._add_btn,
                        label=get_lang_text('GlobalChat.requestPending'),
                        color=(0.6, 0.35, 0.0),
                        on_activate_call=self._open_pending,
                    )
                else:
                    bui.buttonwidget(
                        edit=self._add_btn,
                        label=get_lang_text('GlobalChat.sendFriendRequest'),
                        color=(0.2, 0.5, 0.2),
                    )
                    if status == 409:
                        bui.screenmessage(get_lang_text('GlobalChat.alreadyFriends'), color=(1, 0.5, 0))
                        bui.getsound('error').play()
                    elif status == 404:
                        bui.screenmessage(get_lang_text('GlobalChat.userNotFound'), color=(1, 0.3, 0.3))
                        bui.getsound('error').play()
                    else:
                        bui.screenmessage(f'Error ({status}).', color=(1, 0.3, 0.3))
                        bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AccountsPopup:
    """Account switcher popup shown when multiple accounts are saved locally."""

    _ROW_H = 54
    _HEADER_H = 44
    _FOOTER_H = 52

    def __init__(self, on_logout=None, on_switch=None) -> None:
        self._on_logout = on_logout
        self._on_switch = on_switch
        accounts = get_accounts_list()
        active_id = get_session().get('user', {}).get('id')

        uiscale = bui.app.ui_v1.uiscale
        self._width = 320
        self._height = self._HEADER_H + len(accounts) * self._ROW_H + self._FOOTER_H

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 22),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('AccountsPopup.title'),
            scale=0.9,
            color=(1, 1, 1),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(8, self._height - 38),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        y = self._FOOTER_H
        for acc in accounts:
            uid = acc.get('user', {}).get('id')
            self._build_row(acc, y, is_active=(uid == active_id))
            y += self._ROW_H

        _btn_w = int((self._width - 28) * 0.7)
        _btn_h = int(34 * 0.7)
        bui.buttonwidget(
            parent=self._root_widget,
            position=((self._width - _btn_w) / 2, 9),
            size=(_btn_w, _btn_h),
            label=get_lang_text('AccountsPopup.addAccount'),
            color=(0.15, 0.25, 0.15),
            textcolor=(0.55, 0.85, 0.55),
            on_activate_call=self._add_account,
        )

    def _build_row(self, acc: dict, y: int, is_active: bool) -> None:
        nick_raw = acc.get('user', {}).get('nickname', '?')
        nick = nick_raw[:15] + '...' if len(nick_raw) > 15 else nick_raw

        # nickname
        bui.textwidget(
            parent=self._root_widget,
            position=(12, y + 27),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=nick,
            scale=0.82,
            color=(0.5, 0.95, 0.5) if is_active else (0.78, 0.78, 0.78),
            maxwidth=138,
        )

        # action button — centered in the right half
        if is_active:
            bui.buttonwidget(
                parent=self._root_widget,
                position=(165, y + 12),
                size=(88, 34),
                label=get_lang_text('AccountsPopup.logout'),
                color=(0.5, 0.15, 0.15),
                textcolor=(1.0, 0.75, 0.75),
                on_activate_call=self._logout,
            )
        else:
            bui.buttonwidget(
                parent=self._root_widget,
                position=(165, y + 12),
                size=(88, 34),
                label=get_lang_text('AccountsPopup.signIn'),
                color=(0.15, 0.3, 0.45),
                textcolor=(0.6, 0.85, 1.0),
                on_activate_call=lambda a=acc: self._switch(a),
            )

        # remove button
        bui.buttonwidget(
            parent=self._root_widget,
            position=(269, y + 14),
            size=(24, 26),
            label='x',
            button_type='square',
            color=(0.3, 0.1, 0.1),
            textcolor=(0.85, 0.45, 0.45),
            on_activate_call=lambda a=acc: self._remove(a),
        )

    def _switch(self, account: dict) -> None:
        nick = account.get('user', {}).get('nickname', '?')
        on_switch = self._on_switch
        bui.screenmessage(f'Signing in as {nick}...', color=(0.5, 0.8, 1.0))
        self._close()

        def _ok() -> None:
            bui.screenmessage(f'Signed in as {nick}!', color=(0.0, 1.0, 0.5))
            bui.getsound('cashRegister').play()
            if on_switch:
                on_switch()
            DMWindow()

        def _fail(reason: str) -> None:
            if reason == 'expired':
                bui.screenmessage(
                    f'Session expired for {nick}. Please log in again.',
                    color=(1.0, 0.4, 0.2),
                )
            else:
                bui.screenmessage('Could not connect. Try again.', color=(1.0, 0.5, 0.0))

        switch_to_account(account, on_success=_ok, on_failure=_fail)

    def _remove(self, account: dict) -> None:
        uid = account.get('user', {}).get('id')
        if uid:
            remove_account_from_list(uid)
        bui.getsound('swish').play()
        self._close()
        remaining = get_accounts_list()
        if remaining:
            AccountsPopup(on_logout=self._on_logout)
        elif self._on_logout:
            self._on_logout()

    def _logout(self) -> None:
        full_logout()
        bui.screenmessage('Logged out.', color=(0.8, 0.8, 0.8))
        bui.getsound('swish').play()
        self._close()
        # Reopen so the user can sign into another saved account
        remaining = get_accounts_list()
        if remaining:
            AccountsPopup(on_logout=self._on_logout)
        elif self._on_logout:
            self._on_logout()

    def _add_account(self) -> None:
        self._close()
        LoginWindow()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AccountPopup:
    """Popup to manage account or log out."""

    def __init__(self, on_logout=None, on_switch=None, on_profile_updated=None) -> None:
        self._on_logout = on_logout
        self._on_switch = on_switch
        self._on_profile_updated_cb = on_profile_updated
        uiscale = bui.app.ui_v1.uiscale
        self._width = 280
        self._height = 320

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        user = get_session().get('user', {})
        nick = user.get('nickname', '?')
        name = user.get('name', '')
        uid_str = user.get('uid', '')
        description = user.get('description', '')
        self._v2_account: str = ''

        # header
        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(18, self._height - 38),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        self._v2_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 112, self._height - 38),
            size=(98, 28),
            label='...',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.6,
            enable_sound=True,
            opacity=0.0,
            on_activate_call=self._open_v2_profile,
        )

        if len(get_accounts_list()) > 1:
            bui.buttonwidget(
                parent=self._root_widget,
                position=(self._width - 112 - 34, self._height - 38),
                size=(28, 28),
                label='',
                texture=bui.gettexture('cuteSpaz'),
                color=(1, 1, 1),
                enable_sound=True,
                on_activate_call=self._open_accounts,
            )

        # spaz icon
        icon_size = 64
        icon_x = 14
        icon_y = self._height - 125
        self._char_widget = bui.imagewidget(
            parent=self._root_widget,
            position=(icon_x, icon_y + 7),
            size=(icon_size, icon_size),
            texture=bui.gettexture('neoSpazIcon'),
            tint_texture=bui.gettexture('neoSpazIconColorMask'),
            mask_texture=bui.gettexture('characterIconMask'),
            tint_color=_theme.get_color('COLOR_PRIMARY'),
            tint2_color=_theme.get_color('COLOR_SECONDARY'),
        )

        info_x = icon_x + icon_size - 35

        cont_w = self._width - info_x - 8
        self._info_cont_w = cont_w
        info_container = bui.containerwidget(
            parent=self._root_widget,
            size=(cont_w, 75),
            position=(info_x, icon_y - 8),
            background=False,
        )

        items = [
            (f'{get_lang_text("ManageAccount.nickname")}:', nick or '...'),
            (f'{get_lang_text("ProfileSearchWindow.name")}:', f'@{name}'),
            (f'{get_lang_text("Global.uid")}:', f'#{uid_str}'),
        ]
        row_gap = 20
        label_w = 58
        self._nick_value_widget = None
        self._name_value_widget = None
        self._ban_widget: Optional[bui.Widget] = None
        self._ban_reason: str = ''
        self._ban_timer: Optional[babase.AppTimer] = None
        self._ban_data: Optional[dict] = None
        self._ban_info_container = info_container
        self._info_item_widgets: list = []
        for i, (label, value) in enumerate(items):
            y = 60 - i * row_gap - (8 if i == 0 else 7)
            raw_value = value.lstrip('@#')
            lw = bui.textwidget(
                parent=info_container,
                text=label,
                color=_theme.get_color('COLOR_PRIMARY'),
                position=(32, y),
                size=(label_w, 20),
                h_align='left',
                v_align='top',
                scale=0.62,
                maxwidth=label_w,
                max_height=18,
            )
            val_widget = bui.textwidget(
                parent=info_container,
                text=value,
                color=_theme.get_color('COLOR_SECONDARY'),
                position=(label_w + 17, y),
                size=(cont_w - label_w, 20),
                h_align='left',
                v_align='top',
                scale=0.62,
                maxwidth=cont_w - label_w,
                max_height=18,
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=lambda v=raw_value: (
                    bui.clipboard_set_text(v),
                    bui.screenmessage(get_lang_text('Global.copiedToClipboard'), color=(0.6, 1.0, 0.6)),
                    bui.getsound('dingSmall').play(),
                ),
            )
            self._info_item_widgets.append((lw, val_widget))
            if i == 0:
                self._nick_value_widget = val_widget
            elif i == 1:
                self._name_value_widget = val_widget
        bui.imagewidget(
            parent=self._root_widget,
            position=(14, icon_y - 8),
            size=(self._width - 28, 1),
            texture=bui.gettexture('white'),
            color=_theme.get_color('COLOR_ACCENT'),
        )

        import textwrap
        fw_desc = self._width - 28
        self._desc_widget = bui.textwidget(
            parent=self._root_widget,
            position=((self._width - fw_desc) / 2, icon_y - 58),
            size=(fw_desc, 55),
            h_align='center',
            v_align='top',
            text='\n'.join(textwrap.wrap(description, width=50)) if description else get_lang_text('DM.noDescription'),
            scale=0.58,
            color=_theme.get_color('COLOR_SECONDARY'),
            maxwidth=fw_desc,
        )

        # buttons
        fx, fw = 14, self._width - 28
        btn_h = 48

        bui.buttonwidget(
            parent=self._root_widget,
            position=(fx, 66),
            size=(fw, btn_h),
            label=get_lang_text('DM.manageAccount'),
            color=(0.25, 0.3, 0.45),
            textcolor=(0.6, 0.6, 0.8),
            enable_sound=True,
            on_activate_call=lambda: ManageAccountPopup(on_updated=self._on_updated, on_delete=self._on_deleted),
        )
        bui.buttonwidget(
            parent=self._root_widget,
            position=(fx, 12),
            size=(fw, btn_h),
            label=get_lang_text('DM.logOut'),
            color=(0.55, 0.15, 0.15),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._logout,
        )

        uid = user.get('id')
        if uid:
            threading.Thread(target=self._load_v2, args=(uid,), daemon=True).start()
            threading.Thread(target=self._load_ban, daemon=True).start()

    def _load_ban(self) -> None:
        body, status = authenticated_get('/auth/me/ban')

        def _apply() -> None:
            if not self._root_widget.exists():
                return
            if status != 200 or not isinstance(body, dict) or not body.get('banned'):
                return
            ban = body.get('ban') or {}
            self._ban_data = ban
            self._ban_reason = (ban.get('reason') or '').strip()
            ban_type = ban.get('ban_type', '')
            label_w = 58

            # expand popup and info container to fit ban row
            bui.containerwidget(
                edit=self._root_widget,
                size=(self._width, self._height + 15),
            )
            bui.containerwidget(
                edit=self._ban_info_container,
                size=(self._info_cont_w, 95),
            )
            row_gap = 20
            for idx, (lbl_w, val_w) in enumerate(self._info_item_widgets):
                new_y = 80 - idx * row_gap - (8 if idx == 0 else 7)
                bui.textwidget(edit=lbl_w, position=(32, new_y))
                bui.textwidget(edit=val_w, position=(label_w + 17, new_y))

            def _on_ban_click() -> None:
                if self._ban_reason:
                    bui.screenmessage(
                        get_lang_text('Chat.banReason').format(reason=self._ban_reason),
                        color=(1, 0.15, 0.15),
                    )
                    bui.getsound('error').play()

            self._ban_widget = bui.textwidget(
                parent=self._ban_info_container,
                text='Ban: ...',
                color=(1.0, 0.2, 0.2),
                position=(label_w + 17, 13),
                size=(self._width - label_w - 8, 20),
                h_align='left',
                v_align='top',
                scale=0.62,
                maxwidth=self._width - label_w - 20,
                max_height=18,
                selectable=bool(self._ban_reason),
                click_activate=bool(self._ban_reason),
                glow_type='uniform',
                on_activate_call=_on_ban_click,
            )
            bui.textwidget(
                parent=self._ban_info_container,
                text='Ban:',
                color=(1.0, 0.35, 0.35),
                position=(32, 13),
                size=(label_w, 20),
                h_align='left',
                v_align='top',
                scale=0.62,
                maxwidth=label_w,
                max_height=18,
            )
            self._update_ban_countdown()
            if ban_type != 'permanent':
                self._ban_timer = babase.AppTimer(
                    1.0, babase.Call(self._update_ban_countdown), repeat=True,
                )

        babase.pushcall(_apply, from_other_thread=True)

    def _update_ban_countdown(self) -> None:
        if not (self._root_widget.exists() and self._ban_widget and self._ban_widget.exists()):
            self._ban_timer = None
            return
        ban = self._ban_data or {}
        ban_type = ban.get('ban_type', '')
        if ban_type == 'permanent':
            time_str = get_lang_text('Admin.permanent')
        else:
            from datetime import datetime, timezone
            expires = ban.get('expires_at')
            time_str = '?'
            if expires:
                try:
                    exp = datetime.fromisoformat(str(expires).replace('Z', '+00:00'))
                    remaining = max(0, int((exp - datetime.now(timezone.utc)).total_seconds()))
                    h, rem = divmod(remaining, 3600)
                    m, s = divmod(rem, 60)
                    if h > 0:
                        time_str = f'{h}h {m}m {s}s'
                    elif m > 0:
                        time_str = f'{m}m {s}s'
                    else:
                        time_str = f'{s}s'
                except Exception:
                    pass
        bui.textwidget(edit=self._ban_widget, text=time_str)

    def _load_v2(self, uid: int) -> None:
        body, status = authenticated_get(f'/users/{uid}')

        def _apply() -> None:
            if not self._root_widget.exists():
                return
            if status == 200 and isinstance(body, dict):
                v2 = body.get('v2', '') or ''
                if v2:
                    self._v2_account = v2
                    bui.buttonwidget(
                        edit=self._v2_btn,
                        label=f'{V2_LOGO} {v2}',
                        opacity=1.0,
                    )
                import textwrap
                desc = body.get('description', '') or ''
                bui.textwidget(
                    edit=self._desc_widget,
                    text='\n'.join(textwrap.wrap(desc, width=50)) if desc else get_lang_text('DM.noDescription'),
                )

        babase.pushcall(_apply, from_other_thread=True)

    def _open_accounts(self) -> None:
        def _on_done():
            self._close()
            if self._on_switch:
                self._on_switch()
        AccountsPopup(on_logout=self._on_logout, on_switch=_on_done)

    def _open_v2_profile(self) -> None:
        if not self._v2_account:
            return
        ProfileSearchWindow(source_widget=self._root_widget, v2=self._v2_account)

    def _logout(self) -> None:
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('DM.logoutConfirm'),
            action=self._do_logout,
            ok_text=get_lang_text('DM.logOut'),
            cancel_text=bui.Lstr(resource='cancelText'),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_logout(self) -> None:
        full_logout()
        bui.screenmessage('Logged out.', color=(0.8, 0.8, 0.8))
        bui.getsound('swish').play()
        self._close()
        if self._on_logout:
            self._on_logout()

    def _on_deleted(self) -> None:
        try:
            self._close()
        except Exception:
            pass
        if self._on_logout:
            self._on_logout()

    def _on_updated(self, fields: dict) -> None:
        """Refresh info/desc widgets and propagate to parent."""
        if self._root_widget.exists():
            if 'nickname' in fields and self._nick_value_widget and self._nick_value_widget.exists():
                bui.textwidget(edit=self._nick_value_widget, text=fields['nickname'])
            if 'name' in fields and self._name_value_widget and self._name_value_widget.exists():
                bui.textwidget(edit=self._name_value_widget, text=f'@{fields["name"]}')
            if 'description' in fields and self._desc_widget and self._desc_widget.exists():
                import textwrap
                desc = fields['description']
                bui.textwidget(
                    edit=self._desc_widget,
                    text='\n'.join(textwrap.wrap(desc, width=50)) if desc else get_lang_text('DM.noDescription'),
                )
        if self._on_profile_updated_cb:
            self._on_profile_updated_cb(fields)

    def _close(self) -> None:
        self._ban_timer = None
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class ManageAccountPopup:
    """Popup to edit nickname, description and password."""

    def __init__(self, on_updated=None, on_delete=None) -> None:
        self._on_updated = on_updated
        self._on_delete = on_delete
        uiscale = bui.app.ui_v1.uiscale
        self._width = 340
        self._height = int(420 * 0.75) if uiscale is babase.UIScale.SMALL else 420

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        user = get_session().get('user', {})

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 24),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('ManageAccount.title'),
            scale=0.9,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(18, self._height - 40),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        scroll_w = self._width - 35
        scroll_h = self._height - 47
        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(17, 0),
            size=(scroll_w, scroll_h),
            background=False,
            highlight=False,
            color=_theme.get_color('COLOR_ACCENT'),
        )

        col_w = scroll_w - 24
        col_pad = 10
        self._col = bui.columnwidget(
            parent=self._scroll,
            border=2,
            margin=0,
        )

        field_h = 34
        btn_h = 36
        clr_label = _theme.get_color('COLOR_SECONDARY')
        clr_field = (0.9, 0.9, 0.9, 1.0)
        clr_btn = _theme.get_color('COLOR_BUTTON')
        clr_btn_txt = _theme.get_color('COLOR_PRIMARY')

        def _spacer(h: int = 8) -> None:
            bui.textwidget(parent=self._col, text='', size=(col_w, h))

        def _section_title(text: str) -> None:
            bui.textwidget(
                parent=self._col,
                size=(col_w, 26),
                text=text,
                h_align='center',
                v_align='center',
                scale=0.85,
                color=clr_label,
            )

        def _section_label(text: str, padding: int = col_pad, x_offset: int = 0) -> None:
            if x_offset:
                _row = bui.containerwidget(parent=self._col, size=(col_w, 22), background=False)
                bui.textwidget(
                    parent=_row,
                    position=(x_offset, 0),
                    size=(col_w, 22),
                    text=text,
                    h_align='left',
                    v_align='center',
                    scale=0.72,
                    color=clr_label,
                    padding=padding,
                )
            else:
                bui.textwidget(
                    parent=self._col,
                    size=(col_w, 22),
                    text=text,
                    h_align='left',
                    v_align='center',
                    scale=0.72,
                    color=clr_label,
                    padding=padding,
                )

        def _divider() -> None:
            bui.textwidget(parent=self._col, text='', size=(col_w, 6))
            bui.imagewidget(
                parent=self._col,
                size=(col_w - 10, 1),
                texture=bui.gettexture('white'),
                color=_theme.get_color('COLOR_ACCENT'),
            )

        # Nickname section
        _spacer(6)
        _section_title(get_lang_text('ManageAccount.nickname'))
        self._nick_field = bui.textwidget(
            parent=self._col,
            size=(col_w, field_h + 3),
            text=user.get('nickname', ''),
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=50,
            maxwidth=col_w - 20,
            color=clr_field,
            padding=col_pad,
        )
        _spacer(4)
        self._nick_btn = bui.buttonwidget(
            parent=self._col,
            size=(col_w, btn_h),
            label=get_lang_text('ManageAccount.save'),
            color=clr_btn,
            textcolor=clr_btn_txt,
            enable_sound=True,
            on_activate_call=self._save_nickname,
        )

        # Name section
        _spacer(5)
        _divider()
        _section_title(get_lang_text('ManageAccount.name'))
        self._name_field = bui.textwidget(
            parent=self._col,
            size=(col_w, field_h + 3),
            text=user.get('name', ''),
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=25,
            maxwidth=col_w - 20,
            color=clr_field,
            padding=col_pad,
        )
        _spacer(4)
        self._name_btn = bui.buttonwidget(
            parent=self._col,
            size=(col_w, btn_h),
            label=get_lang_text('ManageAccount.save'),
            color=clr_btn,
            textcolor=clr_btn_txt,
            enable_sound=True,
            on_activate_call=self._save_name,
        )

        # Description section
        _spacer(5)
        _divider()
        _section_title(get_lang_text('ManageAccount.description'))
        self._desc_field = bui.textwidget(
            parent=self._col,
            size=(col_w, field_h + 30),
            text=user.get('description', ''),
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=150,
            maxwidth=col_w - 20,
            color=clr_field,
            padding=col_pad,
        )
        _counter_row = bui.containerwidget(
            parent=self._col,
            size=(col_w, 16),
            background=False,
        )
        self._desc_counter = bui.textwidget(
            parent=_counter_row,
            position=(-55, 0),
            size=(col_w, 16),
            text=f'{len(user.get("description", ""))}/150',
            h_align='left',
            v_align='center',
            scale=0.55,
            color=(0.5, 0.5, 0.5),
        )
        from bauiv1 import AppTimer
        self._desc_timer = AppTimer(
            0.15,
            lambda: self._update_desc_counter(),
            repeat=True,
        )
        _spacer(4)
        self._desc_btn = bui.buttonwidget(
            parent=self._col,
            size=(col_w, btn_h),
            label=get_lang_text('ManageAccount.save'),
            color=clr_btn,
            textcolor=clr_btn_txt,
            enable_sound=True,
            on_activate_call=self._save_description,
        )

        # Change password section
        _spacer(5)
        _divider()
        _section_title(get_lang_text('ManageAccount.changePassword'))
        _spacer(2)
        _section_label(get_lang_text('ManageAccount.currentPassword'), padding=0, x_offset=-35)
        self._cur_pwd_field = bui.textwidget(
            parent=self._col,
            size=(col_w, field_h + 4),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=128,
            maxwidth=col_w - 20,
            color=clr_field,
            padding=col_pad,
        )
        _spacer(4)
        _spacer(2)
        _section_label(get_lang_text('ManageAccount.newPassword'), padding=0, x_offset=-35)
        self._new_pwd_field = bui.textwidget(
            parent=self._col,
            size=(col_w, field_h + 4),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=128,
            maxwidth=col_w - 20,
            color=clr_field,
            padding=col_pad,
            on_return_press_call=self._save_password,
        )
        _spacer(4)
        self._pwd_btn = bui.buttonwidget(
            parent=self._col,
            size=(col_w, btn_h),
            label=get_lang_text('ManageAccount.changePassword'),
            color=clr_btn,
            textcolor=clr_btn_txt,
            enable_sound=True,
            on_activate_call=self._save_password,
        )
        # Delete account section
        _spacer(5)
        _divider()
        _spacer(4)
        self._delete_btn = bui.buttonwidget(
            parent=self._col,
            size=(col_w, btn_h),
            label=get_lang_text('ManageAccount.deleteAccount'),
            color=(0.6, 0.1, 0.1),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._confirm_delete,
        )
        _spacer(10)

        threading.Thread(target=self._fetch_me, daemon=True).start()

    def _update_desc_counter(self) -> None:
        if not self._desc_counter.exists():
            self._desc_timer = None
            return
        text = bui.textwidget(query=self._desc_field) or ''
        bui.textwidget(edit=self._desc_counter, text=f'{len(text)}/150')

    def _fetch_me(self) -> None:
        body, status = authenticated_get('/users/me')

        def _apply() -> None:
            if not self._root_widget.exists():
                return
            if status == 200 and isinstance(body, dict):
                bui.textwidget(edit=self._nick_field, text=body.get('nickname', ''))
                bui.textwidget(edit=self._name_field, text=body.get('name', ''))
                bui.textwidget(edit=self._desc_field, text=body.get('description', ''))
        babase.pushcall(_apply, from_other_thread=True)

    def _save_nickname(self) -> None:
        nick = bui.textwidget(query=self._nick_field)
        if not nick or not nick.strip():
            bui.screenmessage('Nickname cannot be empty.', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return
        bui.buttonwidget(edit=self._nick_btn, color=(0.3, 0.3, 0.3))

        def _run() -> None:
            body, status = authenticated_put('/users/me/nickname', {'nickname': nick.strip()})

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(
                    edit=self._nick_btn,
                    color=_theme.get_color('COLOR_BUTTON'),
                )
                if status == 200:
                    patch_session_user({'nickname': nick.strip()})
                    if self._on_updated:
                        self._on_updated({'nickname': nick.strip()})
                    bui.screenmessage(get_lang_text('ManageAccount.save') + ' OK', color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                else:
                    err = body.get('error', f'Error ({status})') if isinstance(body, dict) else f'Error ({status})'
                    bui.screenmessage(err, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _save_name(self) -> None:
        name = bui.textwidget(query=self._name_field)
        if not name or not name.strip():
            bui.screenmessage(get_lang_text('ManageAccount.name') + '?', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return
        bui.buttonwidget(edit=self._name_btn, color=(0.3, 0.3, 0.3))

        def _run() -> None:
            body, status = authenticated_put('/users/me/name', {'name': name.strip()})

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(edit=self._name_btn, color=_theme.get_color('COLOR_BUTTON'))
                if status == 200:
                    patch_session_user({'name': name.strip()})
                    if self._on_updated:
                        self._on_updated({'name': name.strip()})
                    bui.screenmessage(get_lang_text('ManageAccount.save') + ' OK', color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                elif status == 409:
                    bui.screenmessage(get_lang_text('ManageAccount.nameTaken'), color=(1, 0.5, 0))
                    bui.getsound('error').play()
                else:
                    err = body.get('error', f'Error ({status})') if isinstance(body, dict) else f'Error ({status})'
                    bui.screenmessage(err, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _save_description(self) -> None:
        desc = bui.textwidget(query=self._desc_field)
        bui.buttonwidget(edit=self._desc_btn, color=(0.3, 0.3, 0.3))

        def _run() -> None:
            body, status = authenticated_put('/users/me/description', {'description': desc})

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(
                    edit=self._desc_btn,
                    color=_theme.get_color('COLOR_BUTTON'),
                )
                if status == 200:
                    patch_session_user({'description': desc})
                    if self._on_updated:
                        self._on_updated({'description': desc})
                    bui.screenmessage(get_lang_text('ManageAccount.save') + ' OK', color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                else:
                    err = body.get('error', f'Error ({status})') if isinstance(body, dict) else f'Error ({status})'
                    bui.screenmessage(err, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _save_password(self) -> None:
        cur = bui.textwidget(query=self._cur_pwd_field)
        new = bui.textwidget(query=self._new_pwd_field)

        if not cur:
            bui.screenmessage(get_lang_text('ManageAccount.currentPassword') + '?', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return
        if not new or len(new) < 8:
            bui.screenmessage('Min 8 characters.', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        bui.buttonwidget(edit=self._pwd_btn, color=(0.3, 0.3, 0.3))

        def _run() -> None:
            body, status = authenticated_put(
                '/users/me/password',
                {'currentPassword': cur, 'newPassword': new},
            )

            def _apply() -> None:
                if not self._root_widget.exists():
                    return
                bui.buttonwidget(
                    edit=self._pwd_btn,
                    color=_theme.get_color('COLOR_BUTTON'),
                )
                if status == 200:
                    bui.screenmessage(get_lang_text('ManageAccount.changePassword') + ' OK', color=(0, 1, 0))
                    bui.getsound('cashRegister').play()
                    self._close()
                elif status == 401:
                    bui.screenmessage('Incorrect current password.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    err = body.get('error', f'Error ({status})') if isinstance(body, dict) else f'Error ({status})'
                    bui.screenmessage(err, color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _confirm_delete(self) -> None:
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('ManageAccount.deleteConfirm'),
            action=self._ask_delete_password,
            ok_text=get_lang_text('ManageAccount.deleteAccount'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1, 0.5, 0.5),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _ask_delete_password(self) -> None:
        """Show a small popup with a password field to confirm deletion."""
        uiscale = bui.app.ui_v1.uiscale
        w, h = 320, 160
        self._del_root = bui.containerwidget(
            size=(w, h),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=lambda: bui.containerwidget(edit=self._del_root, transition='out_scale'),
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )
        bui.textwidget(
            parent=self._del_root,
            position=(w * 0.5, h - 28),
            size=(0, 0), h_align='center', v_align='center',
            text=get_lang_text('ManageAccount.currentPassword'),
            scale=0.85, color=_theme.get_color('COLOR_PRIMARY'),
        )
        self._del_pwd_field = bui.textwidget(
            parent=self._del_root,
            position=(14, h - 90),
            size=(w - 28, 38),
            text='', h_align='left', v_align='center',
            editable=True, max_chars=128,
            maxwidth=w - 48,
            color=(0.9, 0.9, 0.9, 1.0), padding=4,
            description=get_lang_text('ManageAccount.currentPassword'),
            on_return_press_call=self._execute_delete,
        )
        btn_y = 10
        bui.buttonwidget(
            parent=self._del_root,
            position=(14, btn_y), size=((w - 34) // 2, 36),
            label=bui.Lstr(resource='cancelText'),
            color=(0.3, 0.3, 0.3), textcolor=(0.8, 0.8, 0.8),
            on_activate_call=lambda: bui.containerwidget(edit=self._del_root, transition='out_scale'),
        )
        self._del_confirm_btn = bui.buttonwidget(
            parent=self._del_root,
            position=(18 + (w - 34) // 2, btn_y), size=((w - 34) // 2, 36),
            label=get_lang_text('ManageAccount.deleteAccount'),
            color=(0.6, 0.1, 0.1), textcolor=(1, 1, 1),
            on_activate_call=self._execute_delete,
        )

    def _execute_delete(self) -> None:
        if not self._del_root.exists():
            return
        password = bui.textwidget(query=self._del_pwd_field)
        if not password:
            bui.screenmessage(get_lang_text('ManageAccount.currentPassword') + '?', color=(1, 0.5, 0))
            bui.getsound('error').play()
            return
        account_name = get_session().get('user', {}).get('name', '?')
        bui.buttonwidget(edit=self._del_confirm_btn, color=(0.3, 0.1, 0.1))

        def _run() -> None:
            _, status = authenticated_delete('/users/me', payload={'password': password})

            def _apply() -> None:
                if self._del_root.exists():
                    bui.containerwidget(edit=self._del_root, transition='out_scale')
                if status == 204:
                    bui.screenmessage(
                        get_lang_text('ManageAccount.accountDeleted').format(name=account_name),
                        color=(1, 0.5, 0.5),
                    )
                    bui.getsound('shieldDown').play()
                    if self._on_delete:
                        self._on_delete()
                    self._close()
                    full_logout()
                elif status == 401:
                    bui.screenmessage('Incorrect password.', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


_DEFAULT_PAGE_SIZE = 10


def _caller_role() -> str:
    return get_session().get('user', {}).get('role', 'USER')


def _caller_id() -> Optional[int]:
    return get_session().get('user', {}).get('id')


def _ban_remaining_text(ban: dict) -> str:
    """Returns a short human-readable string for ban expiry including seconds."""
    if ban.get('ban_type') == 'permanent':
        return get_lang_text('Admin.permanent')
    expires = ban.get('expires_at')
    if not expires:
        return ''
    try:
        from datetime import datetime, timezone
        exp = datetime.fromisoformat(expires.replace('Z', '+00:00'))
        remaining = max(0, int((exp - datetime.now(timezone.utc)).total_seconds()))
        h, rem = divmod(remaining, 3600)
        m, s = divmod(rem, 60)
        if h > 0:
            return f'{h}h {m}m {s}s'
        if m > 0:
            return f'{m}m {s}s'
        return f'{s}s'
    except Exception:
        return ''


class AdminUsersWindow:
    """Scrollable list of all registered users with search and pagination. ADMIN only."""

    def __init__(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        self._width = 420
        self._height = 445
        self._all_users: list[dict] = []
        self._bans_map: dict[int, dict] = {}
        self._filtered: list[dict] = []
        self._current_page = 0
        self._page_size = _DEFAULT_PAGE_SIZE
        self._countdown_widgets: list[tuple[bui.Widget, dict]] = []
        self._countdown_timer: Optional[babase.AppTimer] = None
        self._role_filter: str = 'ALL'

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                1.44 if uiscale is babase.UIScale.SMALL else
                1.3 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 26),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('Admin.title'),
            scale=1.0,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        scroll_w = self._width - 30
        field_y = self._height - 78
        field_h = 32
        btn_h = 28

        # back button aligned vertically with search field
        bui.buttonwidget(
            parent=self._root_widget,
            position=(15, field_y - 5),
            size=(30, btn_h),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )

        filter_btn_w = 56
        filter_gap = 6
        field_w = scroll_w - 50 - 8 - 52 - 15 - filter_gap - filter_btn_w - 5
        self._search_field = bui.textwidget(
            parent=self._root_widget,
            position=(53, field_y - 13),
            size=(field_w, field_h + 7),
            text='',
            h_align='left',
            v_align='center',
            editable=True,
            max_chars=40,
            maxwidth=field_w - 10,
            color=(0.9, 0.9, 0.9, 1.0),
            padding=5,
            description=get_lang_text('Global.search'),
            on_return_press_call=self._on_search,
        )
        search_btn_x = 35 + field_w + 8 + 5 + 15 + 4
        bui.buttonwidget(
            parent=self._root_widget,
            position=(search_btn_x, field_y - 5),
            size=(50, btn_h),
            label=get_lang_text('Global.search'),
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.68,
            enable_sound=True,
            on_activate_call=self._on_search,
        )
        self._filter_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(search_btn_x + 50 + filter_gap + 10, field_y - 5),
            size=(filter_btn_w, btn_h),
            label=self._role_filter,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.65,
            enable_sound=True,
            on_activate_call=self._show_role_filter_popup,
        )

        self._scroll_h = self._height - 78 - 6 - 44 - 10
        self._scroll: Optional[bui.Widget] = None

        self._pagination_widget = bui.containerwidget(
            parent=self._root_widget,
            size=(self._width - 20, 34),
            position=(10, 5),
            background=False,
        )
        self._list_container: Optional[bui.Widget] = None

        self._loading_spinner: Optional[bui.Widget] = None
        try:
            self._loading_spinner = spinner(
                parent=self._root_widget,
                position=(self._width * 0.5 - 25, self._height * 0.5 - 25),
                size=(50, 50),
                color=(1, 1, 1),
                visible=True,
            )
        except Exception as e:
            print(f'Error creating spinner: {e}')

        threading.Thread(target=self._fetch_users, daemon=True).start()

    def _fetch_users(self) -> None:
        (users_body, users_status), (bans_body, bans_status) = (
            authenticated_get('/admin/users'),
            authenticated_get('/admin/bans'),
        )

        def _apply() -> None:
            if not self._root_widget.exists():
                return
            if self._loading_spinner and self._loading_spinner.exists():
                self._loading_spinner.delete()

            if users_status != 200 or not isinstance(users_body, dict):
                bui.textwidget(
                    parent=self._root_widget,
                    position=(self._width * 0.5, self._height * 0.5),
                    size=(0, 0),
                    h_align='center',
                    v_align='center',
                    text=get_lang_text('Admin.noUsers'),
                    scale=0.85,
                    color=(0.7, 0.4, 0.4),
                )
                return

            users_list = users_body.get('users', [])
            self._page_size = int(users_body.get('pageSize', _DEFAULT_PAGE_SIZE))

            if bans_status == 200 and isinstance(bans_body, list):
                self._bans_map = {b['user_id']: b for b in bans_body if 'user_id' in b}

            self._all_users = users_list
            self._filtered = users_list
            self._current_page = 0
            self._show_page(0)

        babase.pushcall(_apply, from_other_thread=True)

    def _reload(self) -> None:
        """Re-fetches users and bans after a ban/unban action."""
        threading.Thread(target=self._fetch_users, daemon=True).start()

    def _on_search(self) -> None:
        self._apply_filters()

    def _apply_filters(self) -> None:
        query = (bui.textwidget(query=self._search_field) or '').strip().lower()
        result = self._all_users
        if self._role_filter != 'ALL':
            result = [u for u in result if u.get('role', 'USER') == self._role_filter]
        if query:
            result = [
                u for u in result
                if query in str(u.get('id', '')).lower()
                or query in (u.get('name', '') or '').lower()
                or query in (u.get('nickname', '') or '').lower()
            ]
        self._filtered = result
        self._show_page(0)

    def _show_role_filter_popup(self) -> None:
        choices = ['ALL', 'USER', 'ADMIN', 'MANAGER']
        _ThemedPopupMenu(
            position=self._filter_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            choices_display=[bui.Lstr(value=c) for c in choices],
            current_choice=self._role_filter,
            delegate=self,
            width=150.0,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        )

    def popup_menu_selected_choice(self, _: 'PopupMenuWindow', choice: str) -> None:
        self._role_filter = choice
        bui.buttonwidget(edit=self._filter_btn, label=choice)
        self._apply_filters()

    def popup_menu_closing(self, _: 'PopupMenuWindow') -> None:
        pass

    def _show_page(self, page: int) -> None:
        if not self._root_widget.exists():
            return
        self._current_page = page

        # stop previous countdown timer
        if self._countdown_timer is not None:
            self._countdown_timer = None
        self._countdown_widgets = []

        if self._list_container and self._list_container.exists():
            self._list_container.delete()

        scroll_w = self._width - 30
        if self._scroll and self._scroll.exists():
            self._scroll.delete()

        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(15, 44),
            size=(scroll_w, self._scroll_h),
            simple_culling_v=50,
            color=_theme.get_color('COLOR_ACCENT'),
        )

        start = page * self._page_size
        page_users = self._filtered[start:start + self._page_size]

        row_h = 46
        content_h = max(row_h, len(page_users) * row_h + 6)
        self._list_container = bui.containerwidget(
            parent=self._scroll,
            size=(scroll_w - 10, content_h),
            background=False,
        )

        if not page_users:
            bui.textwidget(
                parent=self._list_container,
                position=((scroll_w - 10) * 0.5, content_h * 0.5),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=get_lang_text('Admin.noUsers'),
                scale=0.78,
                color=(0.5, 0.5, 0.5),
            )
        else:
            my_id = _caller_id()
            caller_role = _caller_role()
            role_colors = {
                'ADMIN': (1.0, 0.3, 0.3),
                'MANAGER': (0.9, 0.7, 0.2),
                'USER': (0.6, 0.6, 0.6),
            }
            total = len(page_users)
            for i, user in enumerate(page_users):
                y = (total - 1 - i) * row_h + 3
                uid = user.get('id')
                raw_nick = user.get('nickname', '?')
                nick = raw_nick[:12] + '...' if len(raw_nick) > 12 else raw_nick
                name = user.get('name', '?')
                role = user.get('role', 'USER')
                role_color = role_colors.get(role, (0.6, 0.6, 0.6))
                ban = self._bans_map.get(uid) if uid is not None else None
                is_self = uid == my_id

                row = bui.containerwidget(
                    parent=self._list_container,
                    size=(scroll_w - 14, row_h - 4),
                    position=(0, y),
                    background=False,
                )
                rw = scroll_w - 14

                nick_color = (1.0, 0.35, 0.35) if ban else (0.9, 0.9, 0.9)
                bui.textwidget(
                    parent=row,
                    position=(4, (row_h - 4) * 0.5 + 5),
                    size=(0, 0),
                    h_align='left',
                    v_align='center',
                    text=nick,
                    scale=0.76,
                    color=nick_color,
                    maxwidth=140,
                )

                sub_y = (row_h - 4) * 0.5 - 9
                if ban:
                    countdown_widget = bui.textwidget(
                        parent=row,
                        position=(4, sub_y),
                        size=(0, 0),
                        h_align='left',
                        v_align='center',
                        text=_ban_remaining_text(ban),
                        scale=0.55,
                        color=(1.0, 0.45, 0.45),
                        maxwidth=140,
                    )
                    if ban.get('ban_type') != 'permanent':
                        self._countdown_widgets.append((countdown_widget, ban))
                else:
                    bui.textwidget(
                        parent=row,
                        position=(4, sub_y),
                        size=(0, 0),
                        h_align='left',
                        v_align='center',
                        text=f'@{name}',
                        scale=0.58,
                        color=(0.5, 0.5, 0.5),
                        maxwidth=130,
                    )

                bui.textwidget(
                    parent=row,
                    position=(rw * 0.5 - 7, (row_h - 4) * 0.5 + 1),
                    size=(0, 0),
                    h_align='center',
                    v_align='center',
                    text=role,
                    scale=0.63,
                    color=role_color,
                )

                can_act = (
                    not is_self
                    and (caller_role == 'ADMIN' or (caller_role == 'MANAGER' and role != 'ADMIN'))
                )
                if can_act and uid is not None:
                    friend_dict = {
                        'friend_id': uid,
                        'friend_nickname': nick,
                        'friend_name': name,
                        'friend_v2': user.get('v2') or '',
                        'friend_description': user.get('description') or '',
                        'role': user.get('role', 'USER'),
                    }
                    bui.buttonwidget(
                        parent=row,
                        position=(rw - 80, (row_h - 4) * 0.5 - 13),
                        size=(50, 24),
                        label='...',
                        color=_theme.get_color('COLOR_BUTTON'),
                        textcolor=_theme.get_color('COLOR_PRIMARY'),
                        text_scale=0.7,
                        enable_sound=True,
                        on_activate_call=babase.Call(
                            self._open_actions, friend_dict, ban,
                        ),
                    )

        # start real-time countdown if there are banned users in this page
        if self._countdown_widgets:
            self._countdown_timer = babase.AppTimer(
                1.0, babase.Call(self._update_countdowns), repeat=True,
            )

        self._build_pagination()

    def _update_countdowns(self) -> None:
        if not self._root_widget.exists():
            self._countdown_timer = None
            return
        for widget, ban in self._countdown_widgets:
            if widget.exists():
                bui.textwidget(edit=widget, text=_ban_remaining_text(ban))

    def _build_pagination(self) -> None:
        if self._pagination_widget and self._pagination_widget.exists():
            self._pagination_widget.delete()

        total_pages = max(1, (len(self._filtered) + self._page_size - 1) // self._page_size)
        pw = self._width - 20
        self._pagination_widget = bui.containerwidget(
            parent=self._root_widget,
            size=(pw, 34),
            position=(10, 10),
            background=False,
        )

        nav_w = 32
        gap = 8
        label_w = 60
        total_w = nav_w + gap + label_w + gap + nav_w
        cx = (pw - total_w) / 2

        prev_page = max(0, self._current_page - 1)
        next_page = min(total_pages - 1, self._current_page + 1)

        bui.buttonwidget(
            parent=self._pagination_widget,
            position=(cx, 4), size=(nav_w, 26),
            label='<',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            autoselect=True, scale=0.85,
            on_activate_call=babase.Call(self._show_page, prev_page),
        )

        bui.textwidget(
            parent=self._pagination_widget,
            position=(cx + nav_w + gap + label_w * 0.5, 17),
            size=(0, 0),
            h_align='center', v_align='center',
            text=f'({self._current_page + 1}/{total_pages})',
            scale=0.72,
            color=_theme.get_color('COLOR_SECONDARY'),
        )

        bui.buttonwidget(
            parent=self._pagination_widget,
            position=(cx + nav_w + gap + label_w + gap, 4), size=(nav_w, 26),
            label='>',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            autoselect=True, scale=0.85,
            on_activate_call=babase.Call(self._show_page, next_page),
        )

    def _open_actions(self, friend: dict, ban: Optional[dict]) -> None:
        AdminActionsPopup(friend=friend, ban=ban, on_done=self._reload)

    def _close(self) -> None:
        self._countdown_timer = None
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AdminActionsPopup:
    """Popup with view/edit/role/ban options for a user."""

    def __init__(
        self,
        friend: dict,
        ban: Optional[dict] = None,
        on_done: Optional[Callable] = None,
    ) -> None:
        self._friend = friend
        self._ban = ban
        self._on_done = on_done
        uiscale = bui.app.ui_v1.uiscale
        self._width = 240
        caller_role = _caller_role()
        is_banned = ban is not None
        rows = 4 

        if caller_role == 'ADMIN':
            rows = 5
        self._height = int((60 + rows * 46) * 1.15)

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        nick = friend.get('friend_nickname', '?')
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 31),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=nick,
            scale=0.9,
            color=(1, 1, 1),
            maxwidth=self._width * 0.4,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(15, self._height - 44),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        fw = self._width - 28
        y = self._height - 105
        self._unban_btn: Optional[bui.Widget] = None
        self._unban_timer: Optional[babase.AppTimer] = None

        bui.buttonwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(fw, 36),
            label=get_lang_text('FriendMenu.viewAccount'),
            color=(0.2, 0.28, 0.4),
            textcolor=(0.6, 0.7, 1.0),
            enable_sound=True,
            on_activate_call=self._view_account,
        )
        y -= 46

        if caller_role == 'ADMIN':
            bui.buttonwidget(
                parent=self._root_widget,
                position=(14, y),
                size=(fw, 36),
                label=get_lang_text('Admin.editProfile'),
                color=(0.25, 0.25, 0.4),
                textcolor=(0.7, 0.7, 1.0),
                enable_sound=True,
                on_activate_call=lambda: AdminEditProfilePopup(friend=friend, on_done=on_done),
            )
            y -= 46

        bui.buttonwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(fw, 36),
            label=get_lang_text('Admin.changeRole'),
            color=(0.25, 0.35, 0.5),
            textcolor=(0.6, 0.7, 1.0),
            enable_sound=True,
            on_activate_call=lambda: AdminChangeRolePopup(friend=friend, on_done=on_done),
        )
        y -= 46

        if is_banned:
            ban_txt = _ban_remaining_text(ban)
            label = f'Unban ({ban_txt})' if ban_txt else 'Unban'
            self._unban_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(14, y),
                size=(fw, 36),
                label=label,
                color=(0.2, 0.5, 0.2),
                textcolor=(0.7, 1.0, 0.7),
                enable_sound=True,
                on_activate_call=self._confirm_unban,
            )
            if ban.get('ban_type') != 'permanent':
                self._unban_timer = babase.AppTimer(
                    1.0, babase.Call(self._update_unban_label), repeat=True,
                )
        else:
            bui.buttonwidget(
                parent=self._root_widget,
                position=(14, y),
                size=(fw, 36),
                label=get_lang_text('Admin.banUser'),
                color=(0.55, 0.15, 0.15),
                textcolor=(1, 1, 1),
                enable_sound=True,
                on_activate_call=lambda: AdminBanPopup(friend=friend, on_done=on_done),
            )
        y -= 46

        if caller_role == 'ADMIN':
            bui.buttonwidget(
                parent=self._root_widget,
                position=(14, y),
                size=(fw, 36),
                label=get_lang_text('Admin.deleteAccount'),
                color=(0.5, 0.1, 0.1),
                textcolor=(1, 0.6, 0.6),
                enable_sound=True,
                on_activate_call=self._confirm_delete,
            )

    def _update_unban_label(self) -> None:
        if self._unban_btn is None or not self._unban_btn.exists():
            self._unban_timer = None
            return
        ban_txt = _ban_remaining_text(self._ban)
        label = f'Unban ({ban_txt})' if ban_txt else 'Unban'
        bui.buttonwidget(edit=self._unban_btn, label=label)

    def _view_account(self) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        FriendAccountPopup(friend={'friend_id': uid, 'friend_nickname': nick}, is_friend=False)

    def _confirm_unban(self) -> None:
        nick = self._friend.get('friend_nickname', '?')
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=f'Unban {nick}?',
            action=self._do_unban,
            ok_text='Unban',
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(0.7, 1.0, 0.7),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_unban(self) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        if uid is None:
            return
        on_done = self._on_done

        def _run() -> None:
            _, status = authenticated_delete(f'/admin/bans/{uid}')

            def _apply() -> None:
                if status in (200, 204):
                    bui.screenmessage(
                        get_lang_text('Admin.unbanned').format(nick=nick),
                        color=(0.5, 1, 0.5),
                    )
                    bui.getsound('cashRegister').play()
                    if on_done:
                        on_done()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()
        self._close()

    def _confirm_delete(self) -> None:
        nick = self._friend.get('friend_nickname', '?')
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('Admin.deleteAccountConfirm').format(nick=nick),
            action=self._do_delete,
            ok_text=get_lang_text('Admin.deleteAccount'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1.0, 0.5, 0.5),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_delete(self) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        if uid is None:
            return
        on_done = self._on_done

        def _run() -> None:
            _, status = authenticated_delete(f'/admin/users/{uid}')

            def _apply() -> None:
                if status in (200, 204):
                    bui.screenmessage(
                        get_lang_text('Admin.accountDeleted').format(nick=nick),
                        color=(1, 0.5, 0.5),
                    )
                    bui.getsound('shieldDown').play()
                    if on_done:
                        on_done()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()
        self._close()

    def _close(self) -> None:
        self._unban_timer = None
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AdminBanPopup:
    """Popup to ban a user with configurable duration and reason."""

    _CFG_BAN_TYPE = '_bampui_admin_ban_type'
    _CFG_BAN_DURATION = '_bampui_admin_ban_duration'
    _DURATION_CHOICES = ['5', '10', '20', '30', '45', '60', '120', '300']
    _TYPE_CHOICES = ['hours', 'days', 'permanent']

    def __init__(self, friend: dict, on_done: Optional[Callable] = None) -> None:
        self._friend = friend
        self._on_done = on_done
        self._active_popup: str = ''

        cfg = babase.app.config
        self._ban_type: str = cfg.get(self._CFG_BAN_TYPE, 'hours')
        self._ban_duration: str = cfg.get(self._CFG_BAN_DURATION, '24')

        uiscale = bui.app.ui_v1.uiscale
        self._width = 360
        self._height = 348

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        nick = friend.get('friend_nickname', '?')
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 29),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('Admin.confirmBan').format(nick=nick),
            scale=0.88,
            color=_theme.get_color('COLOR_PRIMARY'),
            maxwidth=self._width * 0.65,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(15, self._height - 44),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        clr_label = _theme.get_color('COLOR_SECONDARY')
        fw = self._width - 28
        btn_w = int(self._width * 0.4)
        y = self._height - 62 - 17

        # ban type selector
        bui.textwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(0, 0),
            h_align='left', v_align='center',
            text=get_lang_text('Admin.selectBanType'),
            scale=0.68, color=clr_label,
        )
        y -= 32 + 10
        self._type_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(btn_w, 30),
            label=self._type_label(self._ban_type),
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.72,
            enable_sound=True,
            on_activate_call=self._open_type_popup,
        )
        y -= 38 - 7

        # duration selector
        bui.textwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(0, 0),
            h_align='left', v_align='center',
            text=get_lang_text('Admin.duration'),
            scale=0.68, color=clr_label,
        )
        y -= 32 + 10
        self._duration_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(btn_w, 30),
            label=self._ban_duration,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            text_scale=0.72,
            enable_sound=True,
            on_activate_call=self._open_duration_popup,
        )
        if self._ban_type == 'permanent':
            bui.buttonwidget(edit=self._duration_btn, color=(0.2, 0.2, 0.2),
                             textcolor=(0.4, 0.4, 0.4))
        y -= 38 - 7

        # reason field
        bui.textwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(0, 0),
            h_align='left', v_align='center',
            text=get_lang_text('Admin.reason'),
            scale=0.68, color=clr_label,
        )
        y -= 7 + 35 + 10
        self._reason_field = bui.textwidget(
            parent=self._root_widget,
            position=(14, y),
            size=(fw, 42),
            text='',
            h_align='left', v_align='center',
            editable=True, max_chars=100,
            maxwidth=fw - 10,
            color=(0.9, 0.9, 0.9, 1.0), padding=6,
        )

        ban_btn_w = int(self._width * 0.85)
        bui.buttonwidget(
            parent=self._root_widget,
            position=((self._width - ban_btn_w) // 2, 12),
            size=(ban_btn_w, 38),
            label=get_lang_text('Admin.ban'),
            color=(0.65, 0.1, 0.1),
            textcolor=(1, 1, 1),
            enable_sound=True,
            on_activate_call=self._confirm_ban,
        )

    def _type_label(self, ban_type: str) -> str:
        return {
            'hours': get_lang_text('Admin.hours'),
            'days': get_lang_text('Admin.days'),
            'permanent': get_lang_text('Admin.permanent'),
        }.get(ban_type, ban_type)

    def _open_type_popup(self) -> None:
        self._active_popup = 'type'
        _ThemedPopupMenu(
            position=self._type_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=self._TYPE_CHOICES,
            choices_display=bui.Lstr(value='') if False else [
                bui.Lstr(value=self._type_label(c)) for c in self._TYPE_CHOICES
            ],
            current_choice=self._ban_type,
            delegate=self,
            width=190.0,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        )

    def _open_duration_popup(self) -> None:
        if self._ban_type == 'permanent':
            return
        self._active_popup = 'duration'
        _ThemedPopupMenu(
            position=self._duration_btn.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=self._DURATION_CHOICES,
            current_choice=self._ban_duration if self._ban_duration in self._DURATION_CHOICES else self._DURATION_CHOICES[0],
            delegate=self,
            width=190.0,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        )

    def popup_menu_selected_choice(self, _: 'PopupMenuWindow', choice: str) -> None:
        if self._active_popup == 'type':
            self._ban_type = choice
            babase.app.config[self._CFG_BAN_TYPE] = choice
            babase.app.config.apply_and_commit()
            bui.buttonwidget(edit=self._type_btn, label=self._type_label(choice))
            is_perm = choice == 'permanent'
            bui.buttonwidget(
                edit=self._duration_btn,
                color=(0.2, 0.2, 0.2) if is_perm else _theme.get_color('COLOR_BUTTON'),
                textcolor=(0.4, 0.4, 0.4) if is_perm else _theme.get_color('COLOR_PRIMARY'),
            )
        elif self._active_popup == 'duration':
            self._ban_duration = choice
            babase.app.config[self._CFG_BAN_DURATION] = choice
            babase.app.config.apply_and_commit()
            bui.buttonwidget(edit=self._duration_btn, label=choice)

    def popup_menu_closing(self, _: 'PopupMenuWindow') -> None:
        self._active_popup = ''

    def _confirm_ban(self) -> None:
        nick = self._friend.get('friend_nickname', '?')
        if self._ban_type == 'permanent':
            duration_str = get_lang_text('Admin.permanent')
        else:
            duration_str = f'{self._ban_duration} {self._type_label(self._ban_type)}'
        text = get_lang_text('Admin.confirmBan').format(nick=nick) + f'\n{duration_str}'
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=text,
            action=self._do_ban,
            ok_text=get_lang_text('Admin.ban'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1.0, 0.6, 0.6),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_ban(self) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        if uid is None:
            return
        on_done = self._on_done

        ban_type = self._ban_type
        reason = bui.textwidget(query=self._reason_field) or ''
        payload: dict = {'userId': uid, 'banType': ban_type, 'reason': reason or 'Banned by admin'}

        if ban_type != 'permanent':
            try:
                duration = max(1, int(self._ban_duration))
            except ValueError:
                duration = 24
            payload['duration'] = duration

        def _run() -> None:
            _, status = authenticated_post('/admin/bans', payload)

            def _apply() -> None:
                if status == 201:
                    bui.screenmessage(
                        get_lang_text('Admin.banned').format(nick=nick),
                        color=(1, 0.4, 0.4),
                    )
                    bui.getsound('shieldDown').play()
                    if on_done:
                        on_done()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()
        self._close()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AdminChangeRolePopup:
    """Popup to change a user's role."""

    def __init__(self, friend: dict, on_done: Optional[Callable] = None) -> None:
        self._friend = friend
        self._on_done = on_done
        uiscale = bui.app.ui_v1.uiscale
        self._width = 240
        caller_role = _caller_role()

        roles = ['USER', 'MANAGER']
        if caller_role == 'ADMIN':
            roles.append('ADMIN')

        self._height = int((60 + len(roles) * 46) * 1.2)

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                2.1 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        nick = friend.get('friend_nickname', '?')
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 29),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=f'{get_lang_text("Admin.changeRole")}: {nick}',
            scale=0.78,
            color=_theme.get_color('COLOR_PRIMARY'),
            maxwidth=self._width * 0.5,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(10, self._height - 44),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        fw = self._width - 28
        y = self._height - 74 - 30
        role_colors = {
            'USER': ((0.25, 0.3, 0.25), (0.7, 1.0, 0.7)),
            'MANAGER': ((0.3, 0.3, 0.15), (1.0, 0.9, 0.4)),
            'ADMIN': ((0.4, 0.15, 0.15), (1.0, 0.5, 0.5)),
        }
        for role in roles:
            bg, txt = role_colors.get(role, ((0.25, 0.25, 0.25), (0.8, 0.8, 0.8)))
            bui.buttonwidget(
                parent=self._root_widget,
                position=(14, y),
                size=(fw, 36),
                label=role,
                color=bg,
                textcolor=txt,
                enable_sound=True,
                on_activate_call=babase.Call(self._set_role, role),
            )
            y -= 46

    def _set_role(self, role: str) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        current_role = self._friend.get('role', 'USER')
        if uid is None:
            return

        if role == current_role:
            bui.screenmessage(
                get_lang_text('Admin.roleAlreadySet').format(nick=nick, role=role),
                color=(1, 0.8, 0.3),
            )
            bui.getsound('error').play()
            return

        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=get_lang_text('Admin.roleConfirm').format(nick=nick, role=role),
            action=babase.Call(self._do_set_role, role),
            ok_text=get_lang_text('Admin.confirm'),
            cancel_text=bui.Lstr(resource='cancelText'),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_set_role(self, role: str) -> None:
        uid = self._friend.get('friend_id')
        nick = self._friend.get('friend_nickname', '?')
        if uid is None:
            return
        on_done = self._on_done

        def _run() -> None:
            _, status = authenticated_post(f'/admin/users/{uid}/role', {'role': role})

            def _apply() -> None:
                if status == 200:
                    bui.screenmessage(
                        f'{nick}: {get_lang_text("Admin.roleChanged")} → {role}',
                        color=(0.5, 0.9, 1.0),
                    )
                    bui.getsound('cashRegister').play()
                    self._close()
                    if on_done:
                        on_done()
                elif status == 403:
                    bui.screenmessage('Forbidden', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class AdminEditProfilePopup:
    """Popup for ADMIN to change name, nickname, password, description or v2 of another user."""

    def __init__(self, friend: dict, on_done: Optional[Callable] = None) -> None:
        self._friend = friend
        self._on_done = on_done
        uiscale = bui.app.ui_v1.uiscale
        self._width = 500
        field_h = 51
        lbl_gap = 62
        field_gap = 7
        n_fields = 5
        self._height = 68 + n_fields * (lbl_gap + field_gap) + field_h + 56 - 40

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                1.0 if uiscale is babase.UIScale.SMALL else
                0.85 if uiscale is babase.UIScale.MEDIUM else 0.75
            ),
        )

        nick = friend.get('friend_nickname', '?')
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 24),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=f'{get_lang_text("Admin.editProfile")}: {nick}',
            scale=0.78,
            color=_theme.get_color('COLOR_PRIMARY'),
            maxwidth=self._width * 0.8,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(32, self._height - 44),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        clr_label = _theme.get_color('COLOR_SECONDARY')
        clr_field = (0.9, 0.9, 0.9, 1.0)
        fw = int(self._width * 0.9)
        fx = (self._width - fw) // 2
        y = self._height - 68

        def _label(text: str) -> None:
            nonlocal y
            bui.textwidget(
                parent=self._root_widget,
                position=(fx, y), size=(0, 0),
                h_align='left', v_align='center',
                text=text, scale=0.78, color=clr_label,
            )
            y -= lbl_gap

        def _field(
            max_chars: int,
            initial: str = '',
            on_return: Optional[Callable] = None,
        ) -> bui.Widget:
            nonlocal y
            w = bui.textwidget(
                parent=self._root_widget,
                position=(fx, y), size=(fw, field_h),
                text=initial, h_align='left', v_align='center',
                editable=True, max_chars=max_chars,
                maxwidth=fw - 10, color=clr_field, padding=6,
                on_return_press_call=on_return,
            )
            y -= field_gap
            return w

        _label(get_lang_text('ProfileSearchWindow.name'))
        self._name_field = _field(25, initial=friend.get('friend_name', ''))

        _label(get_lang_text('ManageAccount.nickname'))
        self._nick_field = _field(35, initial=friend.get('friend_nickname', ''))

        _label('v2 account')
        self._v2_field = _field(25, initial=friend.get('friend_v2', ''))

        _label(get_lang_text('ManageAccount.description'))
        self._desc_field = _field(150, initial=friend.get('friend_description', ''))

        _label(get_lang_text('ManageAccount.newPassword'))
        self._pwd_field = _field(128, on_return=self._save)

        save_w = int(self._width * 0.6)
        bui.buttonwidget(
            parent=self._root_widget,
            position=((self._width - save_w) // 2, 12), size=(save_w, 36),
            label=get_lang_text('Admin.confirm'),
            color=(0.25, 0.4, 0.25),
            textcolor=(0.7, 1.0, 0.7),
            enable_sound=True,
            on_activate_call=self._save,
        )

    def _save(self) -> None:
        uid = self._friend.get('friend_id')
        if uid is None:
            return

        nick = (bui.textwidget(query=self._nick_field) or '').strip()
        name = (bui.textwidget(query=self._name_field) or '').strip()
        pwd = (bui.textwidget(query=self._pwd_field) or '').strip()
        desc = (bui.textwidget(query=self._desc_field) or '').strip()
        v2 = (bui.textwidget(query=self._v2_field) or '').strip()

        old_nick = self._friend.get('friend_nickname') or ''
        old_name = self._friend.get('friend_name') or ''
        old_desc = self._friend.get('friend_description') or ''
        old_v2 = self._friend.get('friend_v2') or ''

        changes: list[str] = []
        payload: dict = {}

        if name and name != old_name:
            changes.append(f'name: {old_name} -> {name}')
            payload['name'] = name
        if nick and nick != old_nick:
            changes.append(f'nickname: {old_nick} -> {nick}')
            payload['nickname'] = nick
        if v2 and v2 != old_v2:
            changes.append(f'v2: {old_v2} -> {v2}')
            payload['v2'] = v2
        if desc and desc != old_desc:
            changes.append(f'description: {old_desc} -> {desc}')
            payload['description'] = desc
        if pwd:
            changes.append('password: *** -> [changed]')
            payload['password'] = pwd

        if not changes:
            bui.screenmessage(get_lang_text('Admin.noChanges'), color=(1, 0.8, 0.3))
            bui.getsound('error').play()
            return

        self._pending_payload = payload
        confirm_text = get_lang_text('Admin.thisWillChange') + '\n' + '\n'.join(changes)
        from bauiv1lib.confirm import ConfirmWindow
        confirm = ConfirmWindow(
            text=confirm_text,
            action=self._do_save,
            ok_text=get_lang_text('Admin.confirm'),
            cancel_text=bui.Lstr(resource='cancelText'),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_save(self) -> None:
        uid = self._friend.get('friend_id')
        payload = getattr(self, '_pending_payload', {})
        if uid is None or not payload:
            return
        on_done = self._on_done

        def _run() -> None:
            body, status = authenticated_put(f'/admin/users/{uid}/profile', payload)

            def _apply() -> None:
                if status == 200:
                    bui.screenmessage(
                        get_lang_text('Admin.profileSaved'),
                        color=(0.5, 1, 0.5),
                    )
                    bui.getsound('cashRegister').play()
                    # update friend dict so fields stay current if popup stays open
                    if isinstance(body, dict):
                        if 'name' in body:
                            self._friend['friend_name'] = body['name']
                        if 'nickname' in body:
                            self._friend['friend_nickname'] = body['nickname']
                        if 'v2' in body:
                            self._friend['friend_v2'] = body.get('v2') or ''
                        if 'description' in body:
                            self._friend['friend_description'] = body.get('description') or ''
                    if on_done:
                        on_done()
                elif status in (400, 409):
                    bui.screenmessage(
                        get_lang_text('ManageAccount.nameTaken') if status == 409 else 'Validation error',
                        color=(1, 0.5, 0),
                    )
                    bui.getsound('error').play()
                else:
                    bui.screenmessage(f'Error ({status})', color=(1, 0.3, 0.3))
                    bui.getsound('error').play()

            babase.pushcall(_apply, from_other_thread=True)

        threading.Thread(target=_run, daemon=True).start()

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()


class ProfileSearchWindow:
    """Window for viewing a single profile fetched from the API."""

    CHARACTER_MAP = {
        'Frosty': 'frosty', 'Taobao Mascot': 'ali', 'Kronk': 'kronk',
        'Zoe': 'zoe', 'Bernard': 'bear', 'Wizard': 'wizard',
        'Snake Shadow': 'ninja', 'Bones': 'bones', 'Cyborg': 'cyborg',
        'Penguin': 'penguin', 'Pixie': 'pixie', 'B-9000': 'cyborg',
        'Santa Claus': 'santa', 'Spaz': 'neoSpaz', 'Grumbledorf': 'wizard',
        'Pascal': 'jack', 'Jack Morgan': 'jack', 'Easter Bunny': 'bunny',
        'Agent Johnson': 'agent', 'Mel': 'mel', 'Pixel': 'pixie',
    }

    def __init__(self, source_widget, search=None, v2=None,
                 pb=None, id=None) -> None:
        self.theme = _theme
        self.language = _language

        self.passed_param: Optional[str] = None
        self.passed_value: Optional[str] = None
        self.profile_data = None
        self.loading = True
        self.error = None
        self.account_not_found = False

        params = []
        if search is not None:
            params.append(('search', search))
        if v2 is not None:
            params.append(('v2', v2))
        if pb is not None:
            params.append(('pb', pb))
        if id is not None:
            params.append(('id', id))

        if len(params) == 1:
            self.passed_param, self.passed_value = params[0]
        elif not params:
            self.passed_param, self.passed_value = 'v2', 'less'
        else:
            self.passed_param, self.passed_value = params[0]

        self._create_ui(source_widget)
        self._fetch_profile_data()

    def _create_ui(self, source_widget) -> None:
        import babase
        uiscale = bui.app.ui_v1.uiscale
        is_small = uiscale is babase.UIScale.SMALL
        is_medium = uiscale is babase.UIScale.MEDIUM
        w = 440 if is_small else 550
        h = 510 if is_small else (600 if is_medium else 650)
        self._w = w
        self._h = h
        self._is_small = is_small
        self._is_medium = is_medium
        scale = (
            1.32 if uiscale is babase.UIScale.SMALL else
            1.1 if uiscale is babase.UIScale.MEDIUM else 1.0
        )

        self.root = bui.containerwidget(
            size=(w, h),
            color=self.theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self.close,
            scale=scale,
            scale_origin_stack_offset=source_widget.get_screen_space_center(),
        )

        back_btn = bui.buttonwidget(
            parent=self.root,
            position=(45 if is_small else 40, h - 58),
            size=(28, 38),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            enable_sound=False,
            on_activate_call=self.close,
        )
        bui.containerwidget(edit=self.root, cancel_button=back_btn)

        self.title_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearchWindow.profileSearch'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(w * 0.45, h - (46 if is_small else 56)),
            h_align='center', v_align='center',
            scale=0.9,
            maxwidth=300, max_height=40,
        )

        self.status_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearchWindow.loadingProfileData'),
            color=self.theme.get_color('COLOR_TERTIARY'),
            position=(w * 0.45, h * 0.45),
            h_align='center', v_align='center',
            scale=1.0, maxwidth=w - 50
        )

        self.loading_spinner = None
        try:
            self.loading_spinner = spinner(
                parent=self.root,
                position=(w * 0.45 - 25, h * 0.45 - 75),
                size=(50, 50), color=(1, 1, 1), visible=True
            )
        except Exception as e:
            print(f'Error creating spinner: {e}')

        self.header_container = None
        self.main_scroll = None
        self.basic_info_widgets = []
        self.info_text_widgets = []
        self.error_display_widget = None
        self.add_friend_button = None

    def _create_profile_content(self) -> None:
        import babase
        is_small = bui.app.ui_v1.uiscale is babase.UIScale.SMALL
        w, h = self._w, self._h

        self.header_container = ocw(
            parent=self.root, size=(w - 50, 120),
            position=(25, h - 180), background=False
        )

        char_size = (81, 85) if is_small else (100, 105)
        char_x_end = char_size[0] + 20
        self.character_widget = iw(
            parent=self.header_container, size=char_size, position=(10, 30 if is_small else 10),
            texture=gt('white'), color=(1, 1, 1), opacity=0
        )

        self._create_friend_button()

        self.basic_info_container = ocw(
            parent=self.header_container, size=(w - char_x_end - 50, 110),
            position=(char_x_end, -5), background=False
        )

        scroll_w = int(500 * 0.75) if is_small else 500
        scroll_h = (int(390 * 0.75) + 5 if is_small else
                    385 if self._is_medium else 431)
        self.main_scroll = sw(
            parent=self.root, size=(scroll_w, scroll_h), position=(25, 45 if is_small else 35),
            border_opacity=0.3, color=self.theme.get_color('COLOR_ACCENT')
        )

        self.scroll_content = ocw(
            parent=self.main_scroll, size=(scroll_w, 600), background=False
        )

    def _create_friend_button(self) -> None:
        if self.add_friend_button and self.add_friend_button.exists():
            self.add_friend_button.delete()

        is_friend = self._check_if_friend()

        if is_friend:
            try:
                texture = gt('cuteSpaz')
            except Exception:
                try:
                    texture = gt('achievementStayinAlive')
                except Exception:
                    texture = gt('star')
            on_activate = lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
        else:
            try:
                texture = gt('achievementStayinAlive')
            except Exception:
                try:
                    texture = gt('cuteSpaz')
                except Exception:
                    texture = gt('star')
            on_activate = self._add_friend_from_profile

        btn_y = self._h - 58
        self.add_friend_button = obw(
            parent=self.root, label='',
            size=(39, 39), position=(self._w - 44 - 52, btn_y),
            texture=texture, color=(1, 1, 1),
            enable_sound=True, on_activate_call=on_activate
        )

    def _check_if_friend(self) -> bool:
        if not self.profile_data:
            return False
        profile_name = self.profile_data.get('name', 'Unknown')
        if profile_name == 'Unknown':
            return False
        prefixed = (profile_name if profile_name.startswith(V2_LOGO)
                    else f'{V2_LOGO}{profile_name}')
        return any(f['name'] == prefixed for f in load_friends())

    def _add_friend_from_profile(self) -> None:
        if not self.profile_data:
            TIP('No profile data available')
            return
        try:
            profile_name = self.profile_data.get('name', 'Unknown')
            account_id = self.profile_data.get('account_id')
            account_pb = self.profile_data.get('account_pb')
            accounts = self.profile_data.get('accounts', [])

            friends = load_friends()
            for f in friends:
                if f['name'] == profile_name:
                    TIP(f'{profile_name} {get_lang_text("Global.alreadyInFriendsList")}')
                    self._update_friend_button_state()
                    return

            existing_ids = [int(f['id']) for f in friends if f['id'].isdigit()]
            new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

            add_friend(name=profile_name, friend_id=new_id,
                       accounts=accounts, account_pb=account_pb,
                       account_id=account_id)

            TIP(f'{profile_name} {get_lang_text("Global.addedToFriendsList")}')
            gs('ding').play()
            self._update_friend_button_state(is_friend=True)
            self._try_refresh_friends_panel()
        except Exception as e:
            print(f'Error adding friend: {e}')
            TIP('Error adding friend')

    def _update_friend_button_state(self, is_friend: bool = False) -> None:
        if not (hasattr(self, 'add_friend_button') and
                self.add_friend_button and
                self.add_friend_button.exists()):
            return
        current_is_friend = is_friend or self._check_if_friend()
        if current_is_friend:
            try:
                obw(edit=self.add_friend_button, texture=gt('cuteSpaz'),
                    on_activate_call=lambda: TIP(get_lang_text('Global.alreadyInFriendsList')))
            except Exception:
                try:
                    obw(edit=self.add_friend_button, texture=gt('achievementStayinAlive'),
                        on_activate_call=lambda: TIP(get_lang_text('Global.alreadyInFriendsList')))
                except Exception:
                    pass
        else:
            try:
                obw(edit=self.add_friend_button, texture=gt('achievementStayinAlive'),
                    on_activate_call=self._add_friend_from_profile)
            except Exception:
                try:
                    obw(edit=self.add_friend_button, texture=gt('cuteSpaz'),
                        on_activate_call=self._add_friend_from_profile)
                except Exception:
                    pass

    def _try_refresh_friends_panel(self) -> None:
        try:
            FinderWindow.refresh_friends_lists()
        except Exception as e:
            print(f'Error refreshing friends panel: {e}')

    def _display_error(self, error_message: Optional[str] = None) -> None:
        if not self.root.exists():
            return
        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None

        error_text = (get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                      if error_message is None
                      else error_message)

        tw(edit=self.status_widget, text='')
        display_text = '\n'.join(wrap_text(error_text, 30))

        cx = self._w // 2 - 90
        cy = self._h // 2 - 100
        try:
            self.error_display_widget = error_display(
                parent=self.root, size=(180, 200), position=(cx, cy),
                error_text=display_text,
                text_color=self.theme.get_color('COLOR_PRIMARY'),
                text_scale=1.2, text_maxwidth=400,
                icon_texture='cuteSpaz', fade=True, visible=True
            )
        except Exception:
            try:
                self.error_display_widget = error_display(
                    parent=self.root, size=(100, 150), position=(cx + 40, cy),
                    error_text=display_text,
                    text_color=self.theme.get_color('COLOR_PRIMARY'),
                    text_scale=1.2, text_maxwidth=400,
                    icon_texture='neoSpazIcon', fade=True, visible=True
                )
            except Exception:
                tw(edit=self.status_widget, text=error_text)

    def _extract_value_from_text(self, text: str) -> str:
        idx = text.find(':')
        return text[idx + 1:].strip() if idx != -1 else text

    def _copy_data_to_clipboard(self, text: str) -> None:
        try:
            COPY(self._extract_value_from_text(text))
            TIP(get_lang_text('Global.copiedToClipboard'))
            gs('dingSmall').play()
        except Exception as e:
            print(f'Error copying to clipboard: {e}')
            TIP('Failed to copy to clipboard')
            gs('error').play()

    def _fetch_profile_data(self) -> None:
        def fetch_thread() -> None:
            try:
                base_url = f'{BASE_URL}/accounts'
                if self.passed_param == 'v2':
                    url = f'{base_url}?v2={self.passed_value}'
                elif self.passed_param == 'pb':
                    url = f'{base_url}?pb={self.passed_value}'
                elif self.passed_param == 'id':
                    url = f'{base_url}?id={self.passed_value}'
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.noValidParameter')
                    self.loading = False
                    pushcall(self._update_ui, from_other_thread=True)
                    return

                req = urllib.request.Request(url, headers={'User-Agent': 'BombSquad Mod'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    parsed_data = json.loads(response.read().decode())

                if parsed_data.get('result'):
                    self.profile_data = parsed_data['result']
                    self.loading = False
                    self.error = None
                    self.account_not_found = False
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                    self.loading = False
                    self.account_not_found = True

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self.error = get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                    self.account_not_found = True
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
                    self.account_not_found = False
                self.loading = False
            except urllib.error.URLError as e:
                self.error = f'{get_lang_text("ProfileSearchWindow.Error.networkShort")} {e}'
                self.loading = False
            except Exception as e:
                self.error = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
                self.loading = False
                import traceback
                print(f'[ProfileSearchWindow] {traceback.format_exc()}')

            pushcall(self._update_ui, from_other_thread=True)

        t = Thread(target=fetch_thread, daemon=True)
        t.start()

    def _update_ui(self) -> None:
        if not self.root.exists():
            return

        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()

        if self.loading:
            tw(edit=self.status_widget,
               text=self.language.get_text('ProfileSearchWindow.loadingProfileData'))
            return

        if self.error:
            error_msg = (get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                         if self.account_not_found
                         else get_lang_text('ProfileSearchWindow.Error.searchingAccount'))
            self._display_error(error_msg)
            return

        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None

        tw(edit=self.status_widget, text='')

        if self.profile_data and not self.header_container:
            self._create_profile_content()

        self._update_friend_button_state()
        self._display_character()
        self._display_basic_info()
        self._display_profile_info()

    def _display_character(self) -> None:
        if not self.profile_data or not self.character_widget.exists():
            return
        ext = self.profile_data.get('external_info', {})
        bs = ext.get('bsAccountInfo', {})
        prof = bs.get('profile', {})
        char_name = prof.get('character', 'Spaz')
        color = tuple(prof.get('color', [1, 1, 1])[:3])
        highlight = tuple(prof.get('highlight', [1, 1, 1])[:3])
        char_key = self.CHARACTER_MAP.get(char_name, 'neoSpaz')
        try:
            iw(edit=self.character_widget,
               texture=gt(f'{char_key}Icon'),
               tint_texture=gt(f'{char_key}IconColorMask'),
               mask_texture=gt('characterIconMask'),
               tint_color=color, tint2_color=highlight, opacity=1)
        except Exception as e:
            print(f'Error loading character textures: {e}')
            try:
                iw(edit=self.character_widget,
                   texture=gt('neoSpazIcon'),
                   tint_texture=gt('neoSpazIconColorMask'),
                   mask_texture=gt('characterIconMask'),
                   tint_color=color, tint2_color=highlight, opacity=1)
            except Exception as e2:
                print(f'Fallback also failed: {e2}')

    def _display_basic_info(self) -> None:
        if not self.profile_data or not self.basic_info_container.exists():
            return
        for w in self.basic_info_widgets:
            if w.exists():
                w.delete()
        self.basic_info_widgets = []

        ext = self.profile_data.get('external_info', {})
        bs = ext.get('bsAccountInfo', {})
        base = ext.get('baseInfo', {})
        prof = bs.get('profile', {})

        items = [
            (f'{self.language.get_text("ProfileSearchWindow.name")}:',
             base.get('name', self.profile_data.get('name'))),
            ('Account ID:', self.profile_data.get('account_id', 'Unknown')),
            ('Account PB:', self.profile_data.get('account_pb', 'Unknown')),
            (f'{self.language.get_text("ProfileSearchWindow.character")}:',
             prof.get('character', 'Unknown')),
        ]

        txt_scale = 0.58 if self._is_small else 0.8
        row_gap = 20 if self._is_small else 25
        for i, (label, value) in enumerate(items):
            full_text = f'{label} {value}'
            w = tw(
                parent=self.basic_info_container, text=full_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(390, 35), position=(-70 if self._is_small else -30, 90 - (i * row_gap)),
                h_align='left', v_align='top', scale=txt_scale,
                maxwidth=390, max_height=25,
                selectable=True, click_activate=True, glow_type='uniform',
                on_activate_call=lambda t=full_text: self._copy_data_to_clipboard(t)
            )
            self.basic_info_widgets.append(w)

    def _display_profile_info(self) -> None:
        if not self.profile_data or not self.scroll_content.exists():
            return
        for w in self.info_text_widgets:
            if w.exists():
                w.delete()
        self.info_text_widgets = []

        ext = self.profile_data.get('external_info', {})
        bs = ext.get('bsAccountInfo', {})
        base = ext.get('baseInfo', {})
        ballistica = ext.get('ballisticaAccountInfo') or {}
        prof = bs.get('profile', {})

        current_y = 550
        line_h = 25
        sec_sp = 15

        def add_info(text: str, color_key: str, scale: float = 0.8,
                     pos_x: int = 10, **kwargs):
            nonlocal current_y
            w = tw(
                parent=self.scroll_content, text=text,
                color=self.theme.get_color(color_key),
                position=(pos_x, current_y),
                h_align='left', v_align='top',
                scale=scale, maxwidth=480, glow_type='uniform',
                **kwargs
            )
            self.info_text_widgets.append(w)

        # Accounts
        accounts = self.profile_data.get('accounts', [])
        if accounts:
            add_info(f'{self.language.get_text("ProfileSearchWindow.accounts")}:',
                     'COLOR_PRIMARY')
            current_y -= line_h
            for acc in accounts:
                w = tw(
                    parent=self.scroll_content, text=f'• {acc}',
                    color=self.theme.get_color('COLOR_TERTIARY'),
                    size=(600, 30), position=(-50, current_y),
                    h_align='left', v_align='top', scale=0.7, maxwidth=460,
                    selectable=True, click_activate=True, glow_type='uniform',
                    on_activate_call=lambda t=f'• {acc}': self._copy_data_to_clipboard(t)
                )
                self.info_text_widgets.append(w)
                current_y -= line_h
            current_y -= sec_sp

        # Rank
        rank = bs.get('rank', [])
        prev_ranks = bs.get('prevRanks', [])
        if rank or prev_ranks:
            add_info(f'{self.language.get_text("ProfileSearchWindow.rankInfo")}:',
                     'COLOR_PRIMARY')
            current_y -= line_h
            if rank and len(rank) >= 3:
                rank_label = f'  {self.language.get_text("ProfileSearchWindow.current")}:'
                rank_value = f' {rank[0]} {rank[1]} #{rank[2]}'
                rank_text = rank_label + rank_value
                label_w = tw(
                    parent=self.scroll_content, text=rank_label,
                    color=self.theme.get_color('COLOR_PRIMARY'),
                    size=(600, 30), position=(-50, current_y),
                    h_align='left', v_align='top', scale=0.7, maxwidth=120,
                )
                self.info_text_widgets.append(label_w)
                value_w = tw(
                    parent=self.scroll_content, text=rank_value,
                    color=self.theme.get_color('COLOR_SECONDARY'),
                    size=(600, 30), position=(20, current_y),
                    h_align='left', v_align='top', scale=0.7, maxwidth=340,
                    selectable=True, click_activate=True, glow_type='uniform',
                    on_activate_call=lambda t=rank_text: self._copy_data_to_clipboard(t)
                )
                self.info_text_widgets.append(value_w)
                current_y -= line_h
            if prev_ranks:
                add_info(f'  {self.language.get_text("ProfileSearchWindow.previousRanks")}:',
                         'COLOR_PRIMARY', pos_x=34)
                current_y -= line_h
                for pr in prev_ranks:
                    if len(pr) >= 4:
                        season, rank_name, points, position = pr
                        pr_label = f'• {self.language.get_text("ProfileSearchWindow.season")} {season}:'
                        pr_value = f' #{position} {rank_name} {points}'
                        pr_full = pr_label + pr_value
                        lw = tw(
                            parent=self.scroll_content, text=pr_label,
                            color=self.theme.get_color('COLOR_PRIMARY'),
                            size=(600, 30), position=(-30, current_y),
                            h_align='left', v_align='top', scale=0.65, maxwidth=130,
                        )
                        self.info_text_widgets.append(lw)
                        vw = tw(
                            parent=self.scroll_content, text=pr_value,
                            color=self.theme.get_color('COLOR_SECONDARY'),
                            size=(600, 30), position=(100, current_y),
                            h_align='left', v_align='top', scale=0.65, maxwidth=310,
                            selectable=True, click_activate=True, glow_type='uniform',
                            on_activate_call=lambda t=pr_full: self._copy_data_to_clipboard(t)
                        )
                        self.info_text_widgets.append(vw)
                        current_y -= line_h
                current_y -= sec_sp

        # Achievements
        ach_count = len(APP.classic.ach.achievements)
        ach_text = f'{self.language.get_text("ProfileSearchWindow.achievements")}: {bs.get("achievementsCompleted", 0)}/{ach_count}'
        add_info(ach_text, 'COLOR_PRIMARY')
        current_y -= line_h + sec_sp

        # Trophies
        trophies_text = bs.get('trophies', '')
        if trophies_text:
            final_str = ''
            cur_char = None
            cur_count = 0
            for ch in trophies_text:
                if ch == cur_char:
                    cur_count += 1
                else:
                    if cur_char is not None:
                        final_str += (f'{cur_char}×{cur_count} ' if cur_count > 1
                                      else f'{cur_char} ')
                    cur_char = ch
                    cur_count = 1
            if cur_char:
                final_str += (f'{cur_char}×{cur_count}' if cur_count > 1 else cur_char)

            add_info(f'{self.language.get_text("ProfileSearchWindow.trophies")}:',
                     'COLOR_PRIMARY')
            current_y -= line_h
            w = tw(
                parent=self.scroll_content, text=final_str,
                color=self.theme.get_color('COLOR_ACCENT'),
                size=(570, 30), position=(-50, current_y - 5),
                h_align='left', v_align='top', scale=0.8, maxwidth=460,
                selectable=True, click_activate=True, glow_type='uniform',
                on_activate_call=lambda t=final_str: self._copy_data_to_clipboard(t)
            )
            self.info_text_widgets.append(w)
            current_y -= line_h + sec_sp

        # More Info
        add_info(f'{self.language.get_text("ProfileSearchWindow.moreInfo")}:',
                 'COLOR_PRIMARY')
        current_y -= line_h

        from datetime import datetime, timezone
        raw_date = base.get('created', 'Unknown')
        formatted = 'Unknown'
        age_str = ''
        if raw_date != 'Unknown':
            try:
                dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
                formatted = dt.strftime('%d/%m/%Y %H:%M')
                total_days = (datetime.now(timezone.utc) - dt).days
                y = total_days // 365
                m = (total_days % 365) // 30
                d = (total_days % 365) % 30
                lbl_y = self.language.get_text('ProfileSearchWindow.years')
                lbl_m = self.language.get_text('ProfileSearchWindow.months')
                lbl_d = self.language.get_text('ProfileSearchWindow.days')
                lbl_ago = self.language.get_text('ProfileSearchWindow.ago')
                age_str = f'({lbl_ago}: {y} {lbl_y}, {m} {lbl_m}, {d} {lbl_d})'
            except Exception:
                formatted = raw_date

        more_data = [
            (f'{self.language.get_text("ProfileSearchWindow.accountType")}:',
             ballistica.get('accountType', 'Unknown')),
            (f'{self.language.get_text("ProfileSearchWindow.activeDays")}:',
             ballistica.get('totalActiveDays', 'Unknown')),
            (f'{self.language.get_text("ProfileSearchWindow.created")}:',
             ballistica.get('created', 'Unknown')),
            (f'{self.language.get_text("ProfileSearchWindow.lastActive")}:',
             ballistica.get('lastActive', 'Unknown')),
            (f'{self.language.get_text("ProfileSearchWindow.accountExistence")}:',
             formatted),
        ]
        for label, value in more_data:
            ft = f'{label} {value}'
            lw = tw(
                parent=self.scroll_content, text=label,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(600, 30), position=(-50, current_y),
                h_align='left', v_align='top', scale=0.7, maxwidth=200,
            )
            self.info_text_widgets.append(lw)
            vw = tw(
                parent=self.scroll_content, text=str(value),
                color=self.theme.get_color('COLOR_SECONDARY'),
                size=(600, 30), position=(155, current_y),
                h_align='left', v_align='top', scale=0.7, maxwidth=280,
                selectable=True, click_activate=True, glow_type='uniform',
                on_activate_call=lambda t=ft: self._copy_data_to_clipboard(t)
            )
            self.info_text_widgets.append(vw)
            current_y -= line_h

        if age_str:
            w = tw(
                parent=self.scroll_content, text=age_str,
                color=self.theme.get_color('COLOR_SECONDARY'),
                size=(600, 30), position=(-50, current_y),
                h_align='left', v_align='top', scale=0.7, maxwidth=480,
                selectable=True, click_activate=True, glow_type='uniform',
                on_activate_call=lambda t=age_str: self._copy_data_to_clipboard(t)
            )
            self.info_text_widgets.append(w)
            current_y -= line_h

        ocw(edit=self.scroll_content, size=(500, 585))

    def close(self) -> None:
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')


class AccountCard:
    """UI card widget showing a player's name and linked accounts."""

    def __init__(self, name: str, accounts: list, call=None,
                 parent=None, position: tuple = (0.0, 0.0)) -> None:
        self._name = name
        self._accounts = accounts
        self._call = call

        card_width = 650 - 3
        card_height = 112
        x, y = position

        self._container = obw(
            parent=parent, label='', size=(card_width, card_height),
            position=(x, y),
            color=_theme.get_color('COLOR_BACKGROUND'),
            on_activate_call=lambda: call() if call else None,
            enable_sound=False,
        )

        char_size = (70, 70)
        char_x = x + 10
        char_y = y + (card_height - char_size[1]) / 2

        self.character_widget = iw(
            parent=parent, draw_controller=self._container,
            size=char_size, position=(char_x, char_y),
            texture=gt('cuteSpaz'),
        )

        content_x = char_x + char_size[0] + 15
        content_width = card_width - content_x - 10
        centered = self._should_center_title(name, accounts)

        if centered:
            self.title_widget = tw(
                parent=parent, draw_controller=self._container,
                position=(content_x, y + card_height / 2 - 15),
                text=name, color=(0.95, 0.95, 0.95),
                scale=1.1, h_align='left', v_align='center',
                maxwidth=content_width
            )
            self.accounts_widget = None
        else:
            self.title_widget = tw(
                parent=parent, draw_controller=self._container,
                position=(content_x, y + card_height - 43),
                text=name, color=(0.95, 0.95, 0.95),
                scale=1.1, h_align='left', v_align='center',
                maxwidth=content_width
            )
            self.accounts_widget = tw(
                parent=parent, draw_controller=self._container,
                position=(content_x - 14, y + 22),
                text=self._format_accounts(accounts),
                color=(0.7, 0.7, 0.7),
                scale=0.8, h_align='left', v_align='center',
                maxwidth=content_width
            )

    def _should_center_title(self, name: str, accounts: list) -> bool:
        if not accounts:
            return True
        return len(accounts) == 1 and accounts[0] == name

    def _format_accounts(self, accounts: list) -> str:
        if not accounts:
            return 'No accounts'
        display = accounts[:5]
        has_more = len(accounts) > 5
        parts = []
        for i, acc in enumerate(display, 1):
            parts.append(acc)
            if i % 3 == 0 and i < len(display):
                parts.append('\n')
            elif i < len(display):
                parts.append(', ')
        if has_more:
            parts.append('\n...' if len(display) % 3 == 0 else ', ...')
        return ''.join(parts)

    def get_button(self):
        return self._container


class ProfileSearch:
    """Window for searching profiles by name."""

    def __init__(self, source_widget, search_term: str = '') -> None:
        self.source_widget = source_widget
        self.search_term = search_term
        self.loading = bool(search_term)
        self.error = None
        self.results = []
        self.current_page = 0
        self.total_pages = 0
        self.total_results = 0
        self.page_size = 0

        self.theme = _theme
        self.language = _language

        if not finder_config:
            load_finder_config()
        self.current_filter = finder_config.get(CFG_NAME_FILTER_ACCOUNT, 'all')
        self._popup_target: str | None = None

        self._create_ui()
        if self.search_term:
            self._fetch_search_results()

    def _create_ui(self) -> None:
        import babase
        from bauiv1 import AppTimer as tuck

        w, h = 700, 550
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.19 if uiscale is babase.UIScale.SMALL else
            1.05 if uiscale is babase.UIScale.MEDIUM else 0.95
        )
        self.root = bui.containerwidget(
            size=(w, h),
            color=self.theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self.close,
            scale=scale,
            scale_origin_stack_offset=self.source_widget.get_screen_space_center(),
        )

        back_btn = obw(
            parent=self.root, position=(35, h - 73),
            size=(28, 38),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self.close,
        )
        bui.containerwidget(edit=self.root, cancel_button=back_btn)

        self.title_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearch.profileSearch'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(w * 0.45, h - 26),
            h_align='center', v_align='center',
            scale=1.0, maxwidth=400, max_height=32,
        )

        self.search_input = tw(
            parent=self.root, position=(81, h - 75),
            size=(290, 40), text=self.search_term, editable=True,
            description='Enter player name to search',
            maxwidth=285, h_align='left', v_align='center',
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.search_placeholder = tw(
            parent=self.root, position=(119, h - 78),
            text='', color=self.theme.get_color('COLOR_TERTIARY')
        )

        self.search_button = obw(
            parent=self.root, position=(390, h - 73), size=(120, 40),
            label=self.language.get_text('Global.search'),
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._on_search_pressed
        )

        self.filter_button = obw(
            parent=self.root, position=(520, h - 73), size=(140, 40),
            label=f'{self.language.get_text("Global.filter")}: {self.current_filter.upper()}',
            color=self.theme.get_color('COLOR_BUTTON'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._show_filter_popup
        )

        status_text = (self.language.get_text('ProfileSearch.enterNameAndPressSearch')
                       if not self.search_term
                       else self.language.get_text('ProfileSearch.searching'))
        self.status_widget = tw(
            parent=self.root, text=status_text,
            color=self.theme.get_color('COLOR_TERTIARY'),
            position=(w * 0.47, h * 0.5),
            h_align='center', v_align='center',
            scale=1.3, maxwidth=w - 50
        )

        self.loading_spinner = None
        if self.search_term:
            try:
                self.loading_spinner = spinner(
                    parent=self.root,
                    position=(w * 0.45 - 25, h * 0.45 - 75),
                    size=(50, 50), style='simple', color=(1, 1, 1), visible=True
                )
            except Exception as e:
                print(f'Error creating spinner: {e}')

        self.scroll_widget = sw(
            parent=self.root, size=(650, 379), position=(25, 91),
            color=self.theme.get_color('COLOR_ACCENT')
        )

        self.container_widget = ocw(
            parent=self.scroll_widget, size=(650, 0), background=False
        )

        self.pagination_widget = ocw(
            parent=self.root, size=(650, 28), position=(25, 44),
            background=False,
        )
        self._page_indicator = None

        self.error_display_widget = None
        self._update_search_placeholder()
        self.filter_updater = tuck(0.1, self._update_search_placeholder, repeat=True)

    def _update_search_placeholder(self) -> None:
        if not self.search_placeholder.exists():
            self.filter_updater = None
            return
        current_text = tw(query=self.search_input)
        tw(edit=self.search_placeholder, text='' if current_text else '')

    def _show_filter_popup(self) -> None:
        import babase
        filters = ['all', 'v2', 'id', 'pb']
        self._popup_target = 'filter_accounts'
        popup = PopupMenuWindow(
            position=self.filter_button.get_screen_space_center(),
            choices=filters,
            choices_display=[babase.Lstr(value=f.upper()) for f in filters],
            current_choice=self.current_filter,
            width=92,
            delegate=self,
        )
        bui.containerwidget(
            edit=popup.root_widget,
            color=self.theme.get_color('COLOR_BUTTON'),
        )

    def popup_menu_closing(self, popup_window) -> None:
        self._popup_target = None

    def _on_filter_selected(self, filter_type: str, popup) -> None:
        self.current_filter = filter_type
        popup.root_widget.delete()
        update_finder_config(CFG_NAME_FILTER_ACCOUNT, filter_type)
        obw(edit=self.filter_button,
            label=f'{self.language.get_text("Global.filter")}: {filter_type.upper()}')
        placeholders = {
            'all': 'Enter player name (shows all matches)',
            'v2': 'Enter exact player name (finds specific account)',
            'id': 'Enter account ID (e.g., a-g45489)',
            'pb': 'Enter public ID (e.g., pb-IF4JU08_Jg==)',
        }
        tw(edit=self.search_input, description=placeholders.get(filter_type, 'Enter search term'))

    def _clear_error_display(self) -> None:
        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None
        tw(edit=self.status_widget, text='')

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        if self._popup_target != 'filter_accounts':
            return
        self.current_filter = choice
        update_finder_config(CFG_NAME_FILTER_ACCOUNT, choice)
        if self.filter_button.exists():
            obw(edit=self.filter_button,
                label=f'{self.language.get_text("Global.filter")}: {choice.upper()}')

    def popup_menu_closing(self, popup_window: PopupMenuWindow) -> None:
        self._popup_target = None

    def _on_search_pressed(self) -> None:
        search_term = tw(query=self.search_input)
        if not search_term:
            return
        self._clear_error_display()
        self.search_term = search_term
        self.loading = True
        self.error = None
        self.results = []
        self.current_page = 1
        self.total_pages = 0

        tw(edit=self.status_widget, text=self.language.get_text('ProfileSearch.searching'))
        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()
        try:
            self.loading_spinner = spinner(
                parent=self.root,
                position=(350 - 25, 250 - 50),
                size=(50, 50), style='simple', color=(1, 1, 1), visible=True
            )
        except Exception as e:
            print(f'Error creating spinner: {e}')

        if self.container_widget.exists():
            self.container_widget.delete()
        self.container_widget = ocw(
            parent=self.scroll_widget, size=(650, 0), background=False
        )
        self._fetch_search_results()

    def _fetch_search_results(self, page: int = 1) -> None:
        import math
        self.current_page = page

        def fetch_thread() -> None:
            try:
                if self.current_filter == 'all':
                    url = (f'{BASE_URL}/accounts?search={self.search_term}'
                           f'&page={page}&pageSize=10')
                    req = urllib.request.Request(url, headers={'User-Agent': 'BombSquad Mod'})
                    with urllib.request.urlopen(req, timeout=10) as response:
                        parsed_data = json.loads(response.read().decode())

                    results = parsed_data.get('results', [])
                    if not results:
                        self.error = 'No results found'
                        self.loading = False
                        pushcall(self._update_ui, from_other_thread=True)
                        return

                    self.results = results
                    self.total_results = parsed_data.get('totalResults', len(results))
                    self.page_size = parsed_data.get('pageSize', 10)
                    self.total_pages = math.ceil(self.total_results / self.page_size) if self.page_size else 1
                    self.loading = False
                    self.error = None

                else:
                    url = f'{BASE_URL}/accounts?search={self.search_term}&max=all'
                    req = urllib.request.Request(url, headers={'User-Agent': 'BombSquad Mod'})
                    with urllib.request.urlopen(req, timeout=10) as response:
                        parsed_data = json.loads(response.read().decode())

                    if 'results' not in parsed_data or not parsed_data['results']:
                        self.error = 'No results found'
                        self.loading = False
                        pushcall(self._update_ui, from_other_thread=True)
                        return

                    results = parsed_data['results']

                if self.current_filter == 'v2':
                    exact = next(
                        (r for r in results
                         if r.get('name', '').replace(V2_LOGO, '').lower() == self.search_term.lower()),
                        None
                    )
                    if not exact:
                        req_all = urllib.request.Request(
                            f'{BASE_URL}/accounts?search={self.search_term}&max=all',
                            headers={'User-Agent': 'BombSquad Mod'}
                        )
                        with urllib.request.urlopen(req_all, timeout=15) as r:
                            all_data = json.loads(r.read().decode())
                        exact = next(
                            (r for r in all_data.get('results', [])
                             if r.get('name', '').replace(V2_LOGO, '').lower() == self.search_term.lower()),
                            None
                        )
                    if exact:
                        self.results = [exact]
                        self.total_results = self.page_size = self.total_pages = 1
                        self.loading = False
                        self.error = None
                    else:
                        self.error = f'{get_lang_text("ProfileSearch.Error.noExactMatch")} \'{self.search_term}\''
                        self.loading = False

                elif self.current_filter == 'id':
                    exact = next(
                        (r for r in results
                         if str(r.get('account_id', '')).lower() == self.search_term.lower()),
                        None
                    )
                    if exact:
                        self.results = [exact]
                        self.total_results = self.page_size = self.total_pages = 1
                        self.loading = False
                        self.error = None
                    else:
                        self.error = f'{get_lang_text("ProfileSearch.Error.noAccountFoundWithId")} {self.search_term}'
                        self.loading = False

                elif self.current_filter == 'pb':
                    exact = next(
                        (r for r in results
                         if str(r.get('account_pb', '')).lower() == self.search_term.lower()),
                        None
                    )
                    if exact:
                        self.results = [exact]
                        self.total_results = self.page_size = self.total_pages = 1
                        self.loading = False
                        self.error = None
                    else:
                        self.error = f'{get_lang_text("ProfileSearch.Error.noAccountFound")} {self.search_term}'
                        self.loading = False

            except urllib.error.HTTPError as e:
                self.error = (get_lang_text('ProfileSearch.Error.serviceUnavailable')
                              if e.code == 404
                              else get_lang_text('ProfileSearch.Error.searchFailed'))
                self.loading = False
            except urllib.error.URLError:
                self.error = get_lang_text('ProfileSearch.Error.network')
                self.loading = False
            except json.JSONDecodeError:
                self.error = get_lang_text('ProfileSearch.Error.invalidResponse')
                self.loading = False
            except Exception:
                self.error = get_lang_text('ProfileSearch.Error.unexpected')
                self.loading = False

            pushcall(self._update_ui, from_other_thread=True)

        Thread(target=fetch_thread, daemon=True).start()

    def _update_ui(self) -> None:
        if not self.root.exists():
            return
        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()
        if self.loading:
            tw(edit=self.status_widget, text=self.language.get_text('ProfileSearch.searching'))
            return
        if self.error:
            self._display_error(self.error)
            return

        self._clear_error_display()
        title = f'{self.language.get_text("Global.search")}: {self.search_term} ({self.page_size} {self.language.get_text("Global.results")})'
        tw(edit=self.title_widget, text=title)

        if not self.results:
            self._display_error('No results found')
            return

        card_h = 100
        spacing = 2
        total_h = len(self.results) * (card_h + spacing)
        ocw(edit=self.container_widget, size=(650, total_h))

        current_y = total_h - card_h - 5
        for result in self.results:
            AccountCard(
                name=result.get('name', 'Unknown'),
                accounts=result.get('accounts', []),
                call=lambda r=result: self._on_result_pressed(r),
                parent=self.container_widget,
                position=(-13, current_y)
            )
            current_y -= card_h + spacing

        self._render_pagination()

    def _render_pagination(self) -> None:
        if not self.pagination_widget.exists():
            return
        self.pagination_widget.delete()
        if self._page_indicator and self._page_indicator.exists():
            self._page_indicator.delete()
        self._page_indicator = None

        MAX_VISIBLE = 10
        btn_w = 24
        btn_h = 22
        gap = 9
        nav_w = 28
        container_w = 650
        pages = min(self.total_pages, 20)

        self.pagination_widget = ocw(
            parent=self.root, size=(container_w, 34), position=(25, 49),
            background=False,
        )
        if pages <= 1:
            return

        if pages <= MAX_VISIBLE:
            total_btn_w = pages * (btn_w + gap)
            start_x = max(0, (container_w - total_btn_w) / 2)
            for p in range(1, pages + 1):
                x = start_x + (p - 1) * (btn_w + gap)
                obw(
                    parent=self.pagination_widget,
                    position=(x, 6), size=(btn_w, btn_h),
                    label=str(p),
                    color=(self.theme.get_color('COLOR_ACCENT') if p == self.current_page
                           else self.theme.get_color('COLOR_BUTTON')),
                    textcolor=self.theme.get_color('COLOR_PRIMARY'),
                    autoselect=True,
                    scale=0.81,
                    on_activate_call=CallStrict(self._go_to_page, p),
                )
        else:
            group = (self.current_page - 1) // MAX_VISIBLE
            group_start = group * MAX_VISIBLE + 1
            group_end = min(pages, group_start + MAX_VISIBLE - 1)
            visible = group_end - group_start + 1
            total_btn_w = nav_w + gap + visible * (btn_w + gap) + nav_w + gap
            start_x = max(0, (container_w - total_btn_w) / 2)
            x = start_x

            # back button
            obw(
                parent=self.pagination_widget,
                position=(x, 6), size=(nav_w, btn_h),
                label='<', color=self.theme.get_color('COLOR_BUTTON'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                autoselect=True, scale=0.85,
                on_activate_call=CallStrict(
                    self._go_to_page, max(1, group_start - MAX_VISIBLE)),
            )
            x += nav_w + gap

            for p in range(group_start, group_end + 1):
                obw(
                    parent=self.pagination_widget,
                    position=(x, 6), size=(btn_w, btn_h),
                    label=str(p),
                    color=(self.theme.get_color('COLOR_ACCENT') if p == self.current_page
                           else self.theme.get_color('COLOR_BUTTON')),
                    textcolor=self.theme.get_color('COLOR_PRIMARY'),
                    autoselect=True, scale=0.81,
                    on_activate_call=CallStrict(self._go_to_page, p),
                )
                x += btn_w + gap

            # next button
            obw(
                parent=self.pagination_widget,
                position=(x, 6), size=(nav_w, btn_h),
                label='>', color=self.theme.get_color('COLOR_BUTTON'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                autoselect=True, scale=0.85,
                on_activate_call=CallStrict(
                    self._go_to_page, min(pages, group_end + 1)),
            )

            # page indicator centered below buttons
            self._page_indicator = tw(
                parent=self.root,
                position=(700 / 2, 32),
                size=(0, 0),
                text=f'({self.current_page}/{pages})',
                scale=0.7,
                h_align='center',
                v_align='center',
                color=self.theme.get_color('COLOR_SECONDARY'),
            )

    def _go_to_page(self, page: int) -> None:
        if not self.root.exists():
            return
        self.loading = True
        self.error = None
        self.results = []
        tw(edit=self.status_widget, text=self.language.get_text('ProfileSearch.searching'))
        if self.container_widget.exists():
            self.container_widget.delete()
        self.container_widget = ocw(
            parent=self.scroll_widget, size=(650, 0), background=False
        )
        self._fetch_search_results(page=page)

    def _display_error(self, error_message: str) -> None:
        if not self.root.exists():
            return
        self._clear_error_display()
        display_text = '\n'.join(wrap_text(error_message, 30))
        try:
            self.error_display_widget = error_display(
                parent=self.root, size=(180, 200), position=(260, 200),
                error_text=display_text,
                text_color=self.theme.get_color('COLOR_PRIMARY'),
                text_scale=1.2, text_maxwidth=600,
                icon_texture='cuteSpaz', fade=True, visible=True
            )
        except Exception:
            tw(edit=self.status_widget, text=error_message)

    def _on_result_pressed(self, result: dict) -> None:
        account_pb = result.get('account_pb')
        if account_pb:
            ProfileSearchWindow(self.source_widget, pb=account_pb)
        else:
            self._display_error('Error: No account PB found in the selected profile')

    def close(self) -> None:
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')





class CreditsWindow:
    """Window for displaying credits."""

    def __init__(self, source_widget) -> None:
        self.source_widget = source_widget
        self.theme = _theme
        self.language = _language
        self._create_ui()
        self._build_content()

    def _format_inspiration(self) -> str:
        inspiration_data = {
            'BrotherBoard': ['finder'],
            'FluffyPal': ['FluffyPartyWindow'],
            'Mr.Smoothy': ['adv'],
        }
        return '\n'.join(
            f'{author} -> mods: {", ".join(mods)}'
            for author, mods in inspiration_data.items()
        )

    def _create_ui(self) -> None:
        window_size = (600, 550)
        borders = BorderWindow(window_size)

        self.root = cw(
            scale_origin_stack_offset=self.source_widget.get_screen_space_center(),
            size=window_size,
            oac=self.close,
        )[0]

        iw(
            parent=self.root,
            size=window_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )

        for border in (borders.border_left, borders.border_top,
                       borders.border_right, borders.border_bottom):
            iw(
                parent=self.root,
                size=border.size,
                position=border.position,
                texture=gt('white'),
                color=self.theme.get_color('COLOR_PRIMARY')
            )

        tw(
            parent=self.root,
            text=self.language.get_text('Global.credits'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(window_size[0] * 0.45, window_size[1] - 50),
            h_align='center',
            v_align='center',
            scale=1.2,
            maxwidth=400
        )

        self.main_scroll = sw(
            parent=self.root,
            size=(550, 440),
            position=(25, 40),
            border_opacity=0.3,
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        self.scroll_content = ocw(
            parent=self.main_scroll,
            size=(550, 1000),
            background=False
        )

    def _build_content(self) -> None:
        current_y = 680
        section_spacing = 40
        line_spacing = 5
        line_height = 25
        self.text_widgets = []

        def add_text(text: str, color_key: str, scale: float = 1.0,
                     maxwidth: int = 500) -> None:
            nonlocal current_y
            w = tw(
                parent=self.scroll_content,
                text=text,
                color=self.theme.get_color(color_key),
                position=(240, current_y),
                h_align='center',
                v_align='center',
                scale=scale,
                maxwidth=maxwidth
            )
            self.text_widgets.append(w)

        def add_wrapped(text: str, color_key: str, scale: float,
                        max_len: int = 60) -> int:
            nonlocal current_y
            lines = wrap_text(text, max_len)
            for i, line in enumerate(lines):
                w = tw(
                    parent=self.scroll_content,
                    text=line,
                    color=self.theme.get_color(color_key),
                    position=(240, current_y - (i * (line_height + line_spacing))),
                    h_align='center',
                    v_align='center',
                    scale=scale,
                    maxwidth=500
                )
                self.text_widgets.append(w)
            return len(lines)

        # Developer
        add_text(self.language.get_text('CreditsWindow.developer'), 'COLOR_PRIMARY')
        current_y -= line_height + 10
        add_text(CREATOR, 'COLOR_TERTIARY', scale=1.1)
        current_y -= section_spacing

        # Motivation
        add_text(self.language.get_text('CreditsWindow.motivation'), 'COLOR_PRIMARY')
        current_y -= line_height + 10
        n = add_wrapped(self.language.get_text('CreditsWindow.motivationDescription'),
                        'COLOR_TERTIARY', 0.8)
        current_y -= n * (line_height + line_spacing) + section_spacing

        # Inspiration
        add_text(self.language.get_text('CreditsWindow.inspiration'), 'COLOR_PRIMARY')
        current_y -= line_height
        n = add_wrapped(self.language.get_text('CreditsWindow.inspirationDescription'),
                        'COLOR_TERTIARY', 0.8)
        current_y -= n * (line_height + line_spacing) + 20

        inspiration_lines = self._format_inspiration().split('\n')
        for i, line in enumerate(inspiration_lines):
            w = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_TERTIARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.9,
                maxwidth=500
            )
            self.text_widgets.append(w)
        current_y -= len(inspiration_lines) * (line_height + line_spacing) + section_spacing

        # Thanks message
        thanks_lines = wrap_text(self.language.get_text('CreditsWindow.thanksMessage'), 80)
        for i, line in enumerate(thanks_lines):
            w = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_PRIMARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.9,
                maxwidth=500
            )
            self.text_widgets.append(w)

        ocw(edit=self.scroll_content, size=(550, 720))

    def close(self) -> None:
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')





class MuteUsersWindow:
    def __init__(self, origin_widget: bui.Widget) -> None:
        load_blacklist()

        uiscale = bui.app.ui_v1.uiscale
        roster = bs.get_game_roster() or []

        plus = babase.app.plus
        own_display = (
            plus.get_v1_account_display_string()
            if plus is not None and plus.get_v1_account_state() == 'signed_in'
            else None
        )

        # Collect roster entries (skip host / own account).
        entries: list[dict] = []
        seen: set[str] = set()
        for entry in roster:
            if entry.get('client_id') == -1:
                continue
            acc = entry.get('display_string', '')
            if not acc or acc in seen:
                continue
            if own_display and acc == own_display:
                continue
            profiles = [
                p.get('name_full') or p.get('name', '')
                for p in entry.get('players', [])
                if p.get('name_full') or p.get('name')
            ]
            entries.append({
                'account': acc,
                'client_id': entry.get('client_id', '?'),
                'profiles': profiles,
            })
            seen.add(acc)

        n = len(entries)
        row_h = 52
        self._width = 400
        self._height = min(90 + n * row_h, 460) if n else 130

        bg_color = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        primary_color = _theme.get_color('COLOR_PRIMARY')

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=bg_color,
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                1.68 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 27),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('MuteUsersWindow.title'),
            scale=1.0,
            color=primary_color,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(15, self._height - 50),
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=btn_color,
            textcolor=primary_color,
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        if not entries:
            bui.textwidget(
                parent=self._root_widget,
                position=(self._width * 0.5, self._height * 0.5 - 10),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text=get_lang_text('MuteUsersWindow.noPlayers'),
                scale=0.85,
                color=(0.7, 0.7, 0.7),
            )
            return

        scroll_w = self._width - 35
        scroll_h = self._height - 65 - 30
        scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=((self._width - scroll_w) / 2, 25),
            size=(scroll_w, scroll_h),
            simple_culling_v=50,
            color=_theme.get_color('COLOR_ACCENT'),
        )
        sub_h = max(n * row_h, scroll_h)
        sub = bui.containerwidget(
            parent=scroll,
            size=(scroll_w - 10, sub_h),
            background=False,
        )

        y = sub_h - row_h
        for entry in entries:
            account = entry['account']
            client_id = entry['client_id']
            profiles = entry['profiles']
            profile_str = profiles[0] if profiles else ''
            blocked = is_blocked(account)
            name_color = (1.0, 0.3, 0.3) if blocked else (0.9, 0.9, 0.9)

            label = f'{client_id}) {account}'
            if profile_str:
                label += f' | {profile_str}'

            w = bui.checkboxwidget(
                parent=sub,
                size=(scroll_w - 30, row_h - 8),
                maxwidth=scroll_w - 40,
                text=babase.Lstr(value=label),
                scale=0.72,
                position=(0, y + 4),
                value=blocked,
                textcolor=name_color,
            )
            bui.checkboxwidget(
                edit=w,
                on_value_change_call=bui.CallPartial(self._on_toggle, account, w),
            )

            y -= row_h

    def _on_toggle(self, account: str, widget: bui.Widget, value: bool) -> None:
        set_blocked(account, value)
        bui.checkboxwidget(
            edit=widget,
            textcolor=(1.0, 0.3, 0.3) if value else (0.9, 0.9, 0.9),
        )
        pw = get_active_party_window()
        if pw is not None:
            pw._roster = None

    def _close(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()





class ReplayNameSavingPopup(PopupWindow):
    def __init__(self) -> None:
        width = 600
        height = 250
        uiscale = bui.app.ui_v1.uiscale
        bg = tuple(finder_config.get(CFG_NAME_COLOR_SECONDARY, (0.2, 0.2, 0.2)))
        color_primary = tuple(finder_config.get(CFG_NAME_COLOR_PRIMARY, (1.0, 1.0, 1.0)))
        color_secondary = tuple(finder_config.get(CFG_NAME_COLOR_SECONDARY, (0.2, 0.2, 0.2)))

        super().__init__(
            position=(0.0, 0.0),
            size=(width, height),
            scale=(
                1.8 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
            bg_color=bg,
        )

        cancel_btn = bui.buttonwidget(
            parent=self.root_widget,
            position=(40, height - 48),
            size=(30, 30),
            label='X',
            button_type='square',
            color=(0.6, 0.1, 0.1),
            textcolor=(1, 1, 1),
            enable_sound=False,
            on_activate_call=self._on_cancel_press,
        )

        # Title
        bui.textwidget(
            parent=self.root_widget,
            text=get_lang_text('saveReplayTitle'),
            position=(width * 0.5, height - 45),
            maxwidth=width * 0.85,
            color=color_primary,
            scale=0.8,
            size=(0, 0),
            h_align='center',
            v_align='center',
            selectable=True,
            click_activate=True,
            on_activate_call=self._insert_default_name,
        )

        enter_text = get_lang_text('saveReplayEnter')
        b_width = min(len(enter_text) * 13.5, 300)
        enter_btn = bui.buttonwidget(
            parent=self.root_widget,
            position=(width * 0.5 - b_width * 0.5, 20),
            size=(b_width, 60),
            scale=1.0,
            label=enter_text,
            on_activate_call=self._do_enter,
            enable_sound=False,
        )

        tf_y = height - 121
        self._text_field = bui.textwidget(
            parent=self.root_widget,
            position=(width * 0.025, tf_y),
            size=(width * 0.95, 46),
            text='',
            h_align='left',
            v_align='center',
            max_chars=100,
            maxwidth=width * 0.9,
            color=(0.9, 0.9, 0.9, 1.0),
            editable=True,
            padding=4,
            on_return_press_call=enter_btn.activate,
        )
        bui.widget(edit=cancel_btn, down_widget=self._text_field)
        bui.containerwidget(
            edit=self.root_widget,
            cancel_button=cancel_btn,
            start_button=enter_btn,
            selected_child=self._text_field,
        )

        info_items = [
            ('$date', get_lang_text('saveReplayInfoDate').format('$date')),
            ('$time', get_lang_text('saveReplayInfoTime').format('$time')),
        ]
        info_y = tf_y - 22.5
        for placeholder, text in info_items:
            bui.textwidget(
                parent=self.root_widget,
                text=text,
                position=(-60, info_y),
                color=color_secondary,
                size=(width * 0.9, 30),
                scale=0.75,
                h_align='left',
                v_align='center',
                selectable=True,
                click_activate=True,
                on_activate_call=bui.CallStrict(self._append_placeholder, placeholder),
            )
            info_y -= 22.5

    def _append_placeholder(self, placeholder: str) -> None:
        current = bui.textwidget(query=self._text_field)
        if placeholder not in current:
            bui.textwidget(edit=self._text_field, text=current + placeholder)

    def _insert_default_name(self) -> None:
        current = bui.textwidget(query=self._text_field)
        default = 'My Replay $date $time'
        if not current or not current.strip():
            bui.textwidget(edit=self._text_field, text=default)
        else:
            text = get_lang_text('saveReplayConfirmReplaceDefault')
            tf = self._text_field

            def _do_replace() -> None:
                bui.textwidget(edit=tf, text=default)

            ConfirmWindow(
                origin_widget=self.root_widget,
                text=f'{text}?',
                width=min(len(text) * 13.5, 600),
                height=125,
                action=_do_replace,
                cancel_is_selected=True,
            )

    def on_popup_cancel(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def _on_cancel_press(self) -> None:
        bui.containerwidget(edit=self.root_widget, transition='out_scale')
        bui.getsound('swish').play()

    def _do_enter(self) -> None:
        name = bui.textwidget(query=self._text_field)
        if not name or not name.strip():
            babase.screenmessage(
                get_lang_text('saveReplayEmptyName'), color=(1.0, 0.3, 0.3))
            bui.getsound('error').play()
            bui.containerwidget(
                edit=self.root_widget, selected_child=self._text_field)
            return
        self._save_replay(name.strip())

    def _save_replay(self, custom_name: str) -> None:
        import os as _os
        import _babase
        from datetime import datetime

        try:
            replay_dir = _babase.get_replays_dir()
            name = custom_name.replace(
                '$date', datetime.now().strftime('%Y-%m-%d')
            ).replace(
                '$time', datetime.now().strftime('%H-%M-%S')
            )
            dest = _os.path.join(replay_dir, f'{name}.brp')

            if _os.path.exists(dest):
                text = get_lang_text('saveReplayOverwriteConfirm')
                ConfirmWindow(
                    text=f'{text}?',
                    width=min(len(text) * 13.5, 600),
                    height=120,
                    action=bui.CallStrict(self._do_save, dest),
                    cancel_is_selected=True,
                    origin_widget=self.root_widget,
                )
            else:
                self._do_save(dest)
        except Exception:
            babase.print_exception()
            babase.screenmessage(
                get_lang_text('Menu.replaySaveFailed'), color=(1.0, 0.3, 0.3))

    def _do_save(self, dest: str) -> None:
        import os as _os
        import shutil
        import _babase

        try:
            src = _os.path.join(_babase.get_replays_dir(), '__lastReplay.brp')
            if not _os.path.exists(src):
                babase.screenmessage(
                    get_lang_text('Menu.replayNoLastReplay'), color=(1.0, 0.3, 0.3))
                bui.getsound('error').play()
                return
            shutil.copy2(src, dest)
            babase.screenmessage(
                get_lang_text('Menu.replaySaved'), color=(0.0, 1.0, 0.5))
            bui.getsound('gunCocking').play()
        except Exception:
            babase.print_exception()
            babase.screenmessage(
                get_lang_text('Menu.replaySaveFailed'), color=(1.0, 0.3, 0.3))

        bui.containerwidget(edit=self.root_widget, transition='out_scale')


class _SettingsPopupMenuWindow(PopupMenuWindow):
    """PopupMenuWindow with theme bg and text colors."""

    def __init__(self, *args, bg_color: tuple, text_color: tuple, **kwargs):
        _orig_tw = bui.textwidget
        _text_widgets: list[bui.Widget] = []

        def _intercept(*a, **kw):
            result = _orig_tw(*a, **kw)
            if kw.get('parent') is not None and 'size' in kw:
                _text_widgets.append(result)
            return result

        bui.textwidget = _intercept
        super().__init__(*args, **kwargs)
        bui.textwidget = _orig_tw

        bui.containerwidget(edit=self.root_widget, color=bg_color)
        for w in _text_widgets:
            if w.exists():
                bui.textwidget(edit=w, color=text_color)


class _SettingsPopupMenu(PopupMenu):
    """PopupMenu that opens a themed popup window."""

    def _make_popup(self) -> None:
        if not self._button:
            return
        if self._opening_call:
            self._opening_call()
        self._window_widget = _SettingsPopupMenuWindow(
            position=self._button.get_screen_space_center(),
            delegate=self,
            width=self._width,
            maxwidth=self._maxwidth,
            scale=self._scale,
            choices=self._choices,
            current_choice=self._current_choice,
            choices_disabled=self._choices_disabled,
            choices_display=self._choices_display,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        ).root_widget


class SettingsWindow:
    """Modpack settings: language, chat, and notification options."""

    def __init__(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        self._width = 420
        self._height = 400
        scroll_w = self._width - 40
        self._col_w = scroll_w - 20

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._close,
            scale=(
                1.68 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        self._title_widget = bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 22),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('Settings.title'),
            scale=0.95,
            color=_theme.get_color('COLOR_SECONDARY'),
        )

        _theme.subscribe('COLOR_BACKGROUND', self._on_bg_color_change)
        _theme.subscribe('COLOR_SECONDARY', self._on_secondary_color_change)
        _theme.subscribe('COLOR_ACCENT', self._on_accent_color_change)
        _theme.subscribe('COLOR_ACCENT', self._on_secondary_color_change)
        _theme.subscribe('COLOR_BUTTON', self._on_secondary_color_change)
        _theme.subscribe('COLOR_BUTTON', self._on_back_btn_color_change)
        _theme.subscribe('COLOR_PRIMARY', self._on_back_btn_color_change)
        self._theme_subscriptions = [
            ('COLOR_BACKGROUND', self._on_bg_color_change),
            ('COLOR_SECONDARY', self._on_secondary_color_change),
            ('COLOR_ACCENT', self._on_accent_color_change),
            ('COLOR_ACCENT', self._on_secondary_color_change),
            ('COLOR_BUTTON', self._on_secondary_color_change),
            ('COLOR_BUTTON', self._on_back_btn_color_change),
            ('COLOR_PRIMARY', self._on_back_btn_color_change),
        ]

        self._back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(23, self._height - 38),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=self._back_btn)

        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(20, 20),
            size=(scroll_w, self._height - 80),
            selection_loops_to_parent=True,
            color=_theme.get_color('COLOR_ACCENT'),
        )
        self._col = bui.columnwidget(
            parent=self._scroll,
            selection_loops_to_parent=True,
        )

        self._build_content()

    def _build_content(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        popup_scale = (
            2.8 if uiscale is babase.UIScale.SMALL else
            1.8 if uiscale is babase.UIScale.MEDIUM else 1.2
        )

        self._add_section(get_lang_text('Settings.sectionInterface'), divider=False)

        self._add_label(get_lang_text('Settings.language'))
        langs = get_languages_for_current_platform()
        ids = list(langs.keys())
        names = list(langs.values())
        current_lang = get_app_lang_as_id()
        if current_lang not in ids:
            current_lang = ids[0]
        self._add_popup(
            width=200,
            scale=popup_scale,
            current_choice=current_lang,
            choices=ids,
            choices_display=[babase.Lstr(value=n) for n in names],
            on_value_change_call=self._on_lang_change,
        )
        self._add_spacer()

        self._add_label(get_lang_text('Settings.uiScale'))
        uiscale_choices = ['2', '1', '0']
        uiscale_labels = [
            get_lang_text('Settings.uiScaleSmall'),
            get_lang_text('Settings.uiScaleMedium'),
            get_lang_text('Settings.uiScaleLarge'),
        ]
        current_uiscale = str(finder_config.get(CFG_NAME_UI_SCALE) or babase.app.config.get('UIScale', 2))
        if current_uiscale not in uiscale_choices:
            current_uiscale = '2'
        self._add_popup(
            width=200,
            scale=popup_scale,
            current_choice=current_uiscale,
            choices=uiscale_choices,
            choices_display=[babase.Lstr(value=l) for l in uiscale_labels],
            on_value_change_call=self._on_uiscale_change,
        )
        self._add_spacer()

        self._add_label(get_lang_text('Settings.chatColorIntensity'))
        intensity_choices = ['off', 'soft', 'strong']
        intensity_labels = [
            get_lang_text('Settings.chatColorOff'),
            get_lang_text('Settings.chatColorSoft'),
            get_lang_text('Settings.chatColorStrong'),
        ]
        current_intensity = str(finder_config.get(CFG_NAME_CHAT_COLOR_INTENSITY, 'strong'))
        if current_intensity not in intensity_choices:
            current_intensity = 'strong'
        self._add_popup(
            width=150,
            scale=popup_scale,
            current_choice=current_intensity,
            choices=intensity_choices,
            choices_display=[babase.Lstr(value=l) for l in intensity_labels],
            on_value_change_call=self._on_chat_color_intensity_change,
        )

        self._add_section(get_lang_text('Settings.sectionTheme'))

        use_theme = bool(finder_config.get(CFG_NAME_USE_THEME, True))
        self._add_checkbox(
            get_lang_text('Settings.useTheme'),
            use_theme,
            self._on_use_theme_change,
        )
        self._add_spacer()

        if use_theme:
            color_label = get_lang_text('Settings.changeThemeColor')
            bui.buttonwidget(
                parent=self._col,
                position=(0, 0),
                size=(min(self._col_w, max(180, len(color_label) * 10)), 40),
                label=color_label,
                autoselect=True,
                color=_theme.get_color('COLOR_BUTTON'),
                textcolor=_theme.get_color('COLOR_SECONDARY'),
                on_activate_call=self._open_color_picker,
            )
        else:
            color_slots = [
                (CFG_NAME_COLOR_BACKGROUND, 'Settings.colorBackground'),
                (CFG_NAME_COLOR_BUTTON, 'Settings.colorButton'),
                (CFG_NAME_COLOR_PRIMARY, 'Settings.colorPrimary'),
                (CFG_NAME_COLOR_SECONDARY, 'Settings.colorSecondary'),
                (CFG_NAME_COLOR_TERTIARY, 'Settings.colorTertiary'),
                (CFG_NAME_COLOR_ACCENT, 'Settings.colorAccent'),
            ]
            for cfg_key, lang_key in color_slots:
                label = get_lang_text(lang_key)
                bui.buttonwidget(
                    parent=self._col,
                    position=(0, 0),
                    size=(min(self._col_w, max(140, len(label) * 10)), 36),
                    label=label,
                    autoselect=True,
                    color=_theme.get_color('COLOR_BUTTON'),
                    textcolor=_theme.get_color('COLOR_SECONDARY'),
                    on_activate_call=lambda _k=cfg_key: self._open_manual_picker(_k),
                )
                self._add_spacer()

        self._add_section(get_lang_text('Settings.sectionOptions'))

        self._add_checkbox(
            get_lang_text('Settings.dmNotifications'),
            get_screenmsg_enabled(),
            self._on_notifications_change,
        )
        self._add_spacer()

        self._add_checkbox(
            get_lang_text('Settings.globalGather'),
            bool(finder_config.get(CFG_NAME_GLOBAL_GATHER, False)),
            self._on_global_gather_change,
        )
        self._add_spacer()

        self._add_checkbox(
            get_lang_text('Settings.cameraAutoRestore'),
            bool(finder_config.get(CFG_NAME_CAMERA_AUTO_RESTORE, True)),
            self._on_camera_auto_restore_change,
        )
        self._add_spacer()

        bui.textwidget(
            parent=self._col,
            size=(self._col_w, 30),
            maxwidth=self._col_w,
            text=get_lang_text('Settings.pingMsgFormat'),
            scale=1.0,
            color=_theme.get_color('COLOR_PRIMARY'),
            h_align='left',
            v_align='center',
        )
        self._add_label(get_lang_text('Settings.pingMsgFormatHint'))
        current_fmt = str(
            finder_config.get(
                CFG_NAME_PING_MSG_FORMAT, get_lang_text('Settings.pingMsgFormatDefault')
            )
        )
        bui.textwidget(parent=self._col, text='', size=(self._col_w, 3))
        self._ping_fmt_field = bui.textwidget(
            parent=self._col,
            size=(self._col_w * 0.7 + 20, 40),
            text=current_fmt,
            editable=True,
            color=_theme.get_color('COLOR_PRIMARY'),
            maxwidth=int(self._col_w * 0.7) + 10,
            max_chars=20,
            padding=4,
        )
        bui.buttonwidget(
            parent=self._col,
            position=(0, 0),
            size=(80, 36),
            label='OK',
            autoselect=True,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_SECONDARY'),
            on_activate_call=self._on_ping_fmt_save,
        )
        self._add_spacer()

        self._add_section(get_lang_text('Settings.sectionStorage'))

        self._add_label(get_lang_text('Settings.maxRecentServers'))
        max_choices = ['3', '5', '10', '20']
        current_max = str(finder_config.get(CFG_NAME_MAX_RECENT_SERVERS, 5))
        if current_max not in max_choices:
            current_max = '5'
        self._add_popup(
            width=100,
            scale=popup_scale,
            current_choice=current_max,
            choices=max_choices,
            choices_display=[babase.Lstr(value=c) for c in max_choices],
            on_value_change_call=self._on_max_recent_servers_change,
        )
        rs_used = self._count_recent_servers()
        self._rs_counter_widget, _ = self._add_counter_row(
            used=rs_used,
            limit=int(current_max),
            on_path_press=self._on_recent_servers_path_press,
        )
        self._add_spacer()

        self._add_label(get_lang_text('Settings.maxChatLogs'))
        max_chat_choices = ['50', '100', '200', '500', '1000']
        current_max_chat = str(finder_config.get(CFG_NAME_MAX_CHAT_LOGS, 100))
        if current_max_chat not in max_chat_choices:
            current_max_chat = '100'
        self._add_popup(
            width=120,
            scale=popup_scale,
            current_choice=current_max_chat,
            choices=max_chat_choices,
            choices_display=[babase.Lstr(value=c) for c in max_chat_choices],
            on_value_change_call=self._on_max_chat_logs_change,
        )
        chat_used = self._count_chat_logs()
        self._chat_counter_widget, _ = self._add_counter_row(
            used=chat_used,
            limit=int(current_max_chat),
            on_path_press=self._on_chat_logs_path_press,
        )
        self._add_spacer()

        self._add_label(get_lang_text('Settings.maxPlayerInfo'))
        max_pi_choices = ['100', '500', '1000', '2000', '5000']
        current_max_pi = str(finder_config.get(CFG_NAME_MAX_PLAYERINFO, 1000))
        if current_max_pi not in max_pi_choices:
            current_max_pi = '1000'
        self._add_popup(
            width=120,
            scale=popup_scale,
            current_choice=current_max_pi,
            choices=max_pi_choices,
            choices_display=[babase.Lstr(value=c) for c in max_pi_choices],
            on_value_change_call=self._on_max_playerinfo_change,
        )
        pi_used = self._count_playerinfo()
        self._pi_counter_widget, _ = self._add_counter_row(
            used=pi_used,
            limit=int(current_max_pi),
            on_path_press=self._on_playerinfo_path_press,
        )
        self._add_spacer()

        btn_label = get_lang_text('Settings.translationSettings')
        bui.buttonwidget(
            parent=self._col,
            position=(0, 0),
            size=(min(self._col_w, max(180, len(btn_label) * 10)), 40),
            label=btn_label,
            autoselect=True,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_SECONDARY'),
            on_activate_call=TranslationSettings,
        )

        self._add_section(get_lang_text('Settings.sectionReset'))

        reset_label = get_lang_text('Settings.resetConfig')
        bui.buttonwidget(
            parent=self._col,
            position=(0, 0),
            size=(min(self._col_w, max(180, len(reset_label) * 10)), 40),
            label=reset_label,
            autoselect=True,
            color=(0.6, 0.1, 0.1),
            textcolor=(1.0, 1.0, 1.0),
            on_activate_call=self._on_reset_config_press,
        )

    def _rebuild_content(self) -> None:
        if self._col and self._col.exists():
            self._col.delete()
        self._col = bui.columnwidget(
            parent=self._scroll,
            selection_loops_to_parent=True,
        )
        bui.textwidget(
            edit=self._title_widget,
            text=get_lang_text('Settings.title'),
            color=_theme.get_color('COLOR_SECONDARY'),
        )
        self._build_content()

    def _on_bg_color_change(self, new_color: tuple) -> None:
        if self._root_widget and self._root_widget.exists():
            from _bampui.theme import o_container
            o_container(edit=self._root_widget, color=new_color)

    def _on_secondary_color_change(self, _: tuple) -> None:
        if self._root_widget and self._root_widget.exists():
            self._rebuild_content()

    def _on_accent_color_change(self, new_color: tuple) -> None:
        if self._scroll and self._scroll.exists():
            bui.scrollwidget(edit=self._scroll, color=new_color)

    def _on_back_btn_color_change(self, _: tuple) -> None:
        if self._back_btn and self._back_btn.exists():
            bui.buttonwidget(
                edit=self._back_btn,
                color=_theme.get_color('COLOR_BUTTON'),
                textcolor=_theme.get_color('COLOR_PRIMARY'),
            )

    def _add_popup(self, **kwargs) -> _SettingsPopupMenu:
        pm = _SettingsPopupMenu(parent=self._col, position=(0, 0), **kwargs)
        btn = pm.get_button()
        if btn and btn.exists():
            bui.buttonwidget(
                edit=btn,
                color=_theme.get_color('COLOR_BUTTON'),
                textcolor=_theme.get_color('COLOR_SECONDARY'),
            )
        return pm

    def _add_label(self, text: str) -> None:
        bui.textwidget(
            parent=self._col,
            size=(self._col_w, 30),
            maxwidth=self._col_w,
            text=text,
            editable=False,
            color=_theme.get_color('COLOR_SECONDARY'),
        )

    def _add_checkbox(self, text: str, value: bool, callback) -> None:
        w = bui.checkboxwidget(
            parent=self._col,
            size=(self._col_w, 32),
            maxwidth=self._col_w * 0.9,
            text=text,
            scale=0.85,
            value=value,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_SECONDARY'),
        )
        bui.checkboxwidget(
            edit=w,
            on_value_change_call=lambda v, _w=w: callback(v, _w),
        )

    def _add_spacer(self) -> None:
        bui.textwidget(parent=self._col, text='', size=(self._col_w, 12))

    def _add_section(self, label: str, divider: bool = True) -> None:
        if divider:
            bui.textwidget(parent=self._col, text='', size=(self._col_w, 6))
            bui.imagewidget(
                parent=self._col,
                size=(self._col_w - 30, 1),
                texture=bui.gettexture('white'),
                color=_theme.get_color('COLOR_ACCENT'),
            )
        bui.textwidget(
            parent=self._col,
            size=(self._col_w, 28),
            maxwidth=self._col_w,
            text=label,
            scale=0.95,
            color=_theme.get_color('COLOR_PRIMARY'),
            h_align='center',
            v_align='center',
        )

    def _on_uiscale_change(self, val: str) -> None:
        import _babase
        from babase._mgen.enums import UIScale
        uiscale_map = {
            '0': UIScale.LARGE,
            '1': UIScale.MEDIUM,
            '2': UIScale.SMALL,
        }
        scale = uiscale_map.get(val)
        if scale is None:
            return
        finder_config[CFG_NAME_UI_SCALE] = val
        save_finder_config(finder_config)
        self._unsubscribe()
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        _babase.app.set_ui_scale(scale)

    def _on_lang_change(self, lang_id: str) -> None:
        update_finder_config(CFG_NAME_PREFFERED_LANG, lang_id)
        _language.update_language(lang_id)
        self._rebuild_content()

    def _on_notifications_change(self, val: bool, widget: bui.Widget) -> None:
        set_screenmsg_enabled(val)
        bui.checkboxwidget(edit=widget, textcolor=(0, 1, 0) if val else (0.95, 0.65, 0))

    def _on_max_recent_servers_change(self, val: str) -> None:
        finder_config[CFG_NAME_MAX_RECENT_SERVERS] = int(val)
        save_finder_config(finder_config)
        if hasattr(self, '_rs_counter_widget') and self._rs_counter_widget.exists():
            used = self._count_recent_servers()
            limit = int(val)
            bui.textwidget(
                edit=self._rs_counter_widget,
                text=get_lang_text('Settings.storageCounter').format(
                    used=used, limit=limit
                ),
                color=self._usage_color(used, limit),
            )

    def _on_camera_auto_restore_change(self, val: bool, widget: bui.Widget) -> None:
        finder_config[CFG_NAME_CAMERA_AUTO_RESTORE] = val
        save_finder_config(finder_config)
        bui.checkboxwidget(edit=widget, textcolor=(0, 1, 0) if val else (0.95, 0.65, 0))

    def _on_reset_config_press(self) -> None:
        from bauiv1lib.confirm import ConfirmWindow
        ConfirmWindow(
            get_lang_text('Settings.resetConfigConfirm'),
            self._do_reset_config,
            cancel_is_selected=True,
        )

    def _do_reset_config(self) -> None:
        import copy
        finder_config.clear()
        finder_config.update(copy.deepcopy(default_finder_config))
        save_finder_config(finder_config)
        _theme.update_colors({
            'COLOR_BACKGROUND': tuple(finder_config[CFG_NAME_COLOR_BACKGROUND]),
            'COLOR_BUTTON': tuple(finder_config[CFG_NAME_COLOR_BUTTON]),
            'COLOR_PRIMARY': tuple(finder_config[CFG_NAME_COLOR_PRIMARY]),
            'COLOR_SECONDARY': tuple(finder_config[CFG_NAME_COLOR_SECONDARY]),
            'COLOR_TERTIARY': tuple(finder_config[CFG_NAME_COLOR_TERTIARY]),
            'COLOR_ACCENT': tuple(finder_config[CFG_NAME_COLOR_ACCENT]),
        })
        self._rebuild_content()

    def _on_chat_color_intensity_change(self, val: str) -> None:
        finder_config[CFG_NAME_CHAT_COLOR_INTENSITY] = val
        save_finder_config(finder_config)
        label_key = {
            'off': 'Settings.chatColorOff',
            'soft': 'Settings.chatColorSoft',
            'strong': 'Settings.chatColorStrong',
        }.get(val, val)
        babase.screenmessage(
            f"{get_lang_text('Settings.chatColorIntensity')}: {get_lang_text(label_key)}",
            color=_theme.get_color('COLOR_ACCENT'),
        )
        w = get_active_party_window()
        if w is not None:
            w.refresh_chat_colors()

    @staticmethod
    def _count_recent_servers() -> int:
        import json
        try:
            if os.path.exists(LAST_SERVERS_FILE):
                with open(LAST_SERVERS_FILE, 'r', encoding='utf-8') as f:
                    return len(json.load(f))
        except Exception:
            pass
        return 0

    @staticmethod
    def _on_recent_servers_path_press() -> None:
        babase.screenmessage(
            get_lang_text('Settings.storagePathMsg').format(path=LAST_SERVERS_FILE),
            color=(0.6, 0.9, 1.0),
        )

    @staticmethod
    def _count_chat_logs() -> int:
        try:
            return sum(1 for e in os.scandir(CHATS_DIRECTORY) if e.is_dir())
        except Exception:
            return 0

    @staticmethod
    def _count_playerinfo() -> int:
        return len(playerinfo)

    @staticmethod
    def _usage_color(used: int, limit: int) -> tuple:
        if limit <= 0:
            return (1.0, 1.0, 1.0)
        ratio = used / limit
        if ratio < 0.5:
            return (0.3, 1.0, 0.3)
        if ratio < 0.75:
            return (1.0, 1.0, 0.0)
        if ratio < 0.9:
            return (1.0, 0.6, 0.0)
        return (1.0, 0.2, 0.2)

    def _add_counter_row(
        self, used: int, limit: int, on_path_press
    ) -> tuple[bui.Widget, bui.Widget]:
        """Row with a left-aligned usage counter and a path button 5px to its right."""
        row_h = 28
        txt_scale = 0.75
        label = get_lang_text('Settings.storageCounter').format(
            used=used, limit=limit
        )
        btn_x = int(bui.get_string_width(label, suppress_warning=True) * txt_scale) + 9
        row = bui.containerwidget(
            parent=self._col,
            size=(self._col_w, row_h),
            background=False,
        )
        txt = bui.textwidget(
            parent=row,
            position=(0, 0),
            size=(0, row_h),
            text=label,
            scale=txt_scale,
            color=self._usage_color(used, limit),
            h_align='left',
            v_align='center',
        )
        btn = bui.buttonwidget(
            parent=row,
            position=(btn_x, (row_h - 22) // 2),
            size=(22, 22),
            label=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
            button_type='square',
            autoselect=True,
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_SECONDARY'),
            enable_sound=True,
            on_activate_call=on_path_press,
        )
        return txt, btn

    @staticmethod
    def _on_chat_logs_path_press() -> None:
        babase.screenmessage(
            get_lang_text('Settings.storagePathMsg').format(path=CHATS_DIRECTORY),
            color=(0.6, 0.9, 1.0),
        )

    @staticmethod
    def _on_playerinfo_path_press() -> None:
        babase.screenmessage(
            get_lang_text('Settings.storagePathMsg').format(path=PLAYERINFO_FILE),
            color=(0.6, 0.9, 1.0),
        )

    def _on_max_chat_logs_change(self, val: str) -> None:
        finder_config[CFG_NAME_MAX_CHAT_LOGS] = int(val)
        save_finder_config(finder_config)
        if hasattr(self, '_chat_counter_widget') and self._chat_counter_widget.exists():
            used = self._count_chat_logs()
            limit = int(val)
            bui.textwidget(
                edit=self._chat_counter_widget,
                text=get_lang_text('Settings.storageCounter').format(
                    used=used, limit=limit
                ),
                color=self._usage_color(used, limit),
            )

    def _on_max_playerinfo_change(self, val: str) -> None:
        finder_config[CFG_NAME_MAX_PLAYERINFO] = int(val)
        save_finder_config(finder_config)
        if hasattr(self, '_pi_counter_widget') and self._pi_counter_widget.exists():
            used = self._count_playerinfo()
            limit = int(val)
            bui.textwidget(
                edit=self._pi_counter_widget,
                text=get_lang_text('Settings.storageCounter').format(
                    used=used, limit=limit
                ),
                color=self._usage_color(used, limit),
            )

    def _on_ping_fmt_save(self) -> None:
        if not hasattr(self, '_ping_fmt_field') or not self._ping_fmt_field.exists():
            return
        val = str(bui.textwidget(query=self._ping_fmt_field)).strip()
        if len(val) > 20:
            bui.screenmessage(
                get_lang_text('Settings.pingMsgFormatErrorLength'),
                color=(1.0, 0.3, 0.3),
            )
            bui.getsound('error').play()
            return
        if '{}' not in val:
            bui.screenmessage(
                get_lang_text('Settings.pingMsgFormatError'),
                color=(1.0, 0.3, 0.3),
            )
            bui.getsound('error').play()
            return
        if val.count('{}') > 1:
            bui.screenmessage(
                get_lang_text('Settings.pingMsgFormatErrorMultiple'),
                color=(1.0, 0.3, 0.3),
            )
            bui.getsound('error').play()
            return
        finder_config[CFG_NAME_PING_MSG_FORMAT] = val
        save_finder_config(finder_config)
        bui.getsound('gunCocking').play()

    def _on_global_gather_change(self, val: bool, widget: bui.Widget) -> None:
        finder_config[CFG_NAME_GLOBAL_GATHER] = val
        save_finder_config(finder_config)
        set_global_gather_modified(val)
        bui.checkboxwidget(edit=widget, textcolor=(0, 1, 0) if val else (0.95, 0.65, 0))

    def _on_use_theme_change(self, val: bool, widget: bui.Widget) -> None:
        finder_config[CFG_NAME_USE_THEME] = val
        save_finder_config(finder_config)
        bui.checkboxwidget(edit=widget, textcolor=(0, 1, 0) if val else (0.95, 0.65, 0))
        self._rebuild_content()

    def _open_manual_picker(self, cfg_key: str) -> None:
        self._color_changed = False
        self._is_manual_picker = True
        self._picker_cfg_key = cfg_key
        defaults = {
            CFG_NAME_COLOR_BACKGROUND: (0.9, 1.0, 1.0),
            CFG_NAME_COLOR_BUTTON: (0.98, 1.0, 1.0),
            CFG_NAME_COLOR_SECONDARY: (0.962, 1.0, 1.0),
            CFG_NAME_COLOR_TERTIARY: (0.942, 1.0, 1.0),
            CFG_NAME_COLOR_PRIMARY: (0.988, 1.0, 1.0),
            CFG_NAME_COLOR_ACCENT: (0.95, 1.0, 1.0),
        }
        self._initial_picker_color = tuple(
            finder_config.get(cfg_key, defaults.get(cfg_key, (1.0, 1.0, 1.0)))
        )
        colorpicker.ColorPicker(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            initial_color=self._initial_picker_color,
            delegate=self,
            tag='manual',
        )

    def _open_color_picker(self) -> None:
        self._color_changed = False
        self._is_manual_picker = False
        self._picker_cfg_key = None
        self._initial_picker_color = _theme.get_color('COLOR_BACKGROUND')
        colorpicker.ColorPicker(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            initial_color=self._initial_picker_color,
            delegate=self,
            tag='accent',
        )

    def _generate_theme_from_color(self, base_color: tuple) -> dict:
        """Derive all theme colors from a base background color."""
        def clamp(v): return max(0.0, min(1.0, v))
        def to_white(c, t): return tuple(clamp(c[i] + (1.0 - c[i]) * t) for i in range(3))
        def shift(c, d): return tuple(clamp(x + d) for x in c)

        b = tuple(base_color)
        avg = sum(b) / 3
        # Amplify color deviation from grey to create a vivid accent
        accent = tuple(clamp(avg + (x - avg) * 4.0 + 0.25) for x in b)

        return {
            CFG_NAME_COLOR_BACKGROUND: b,
            CFG_NAME_COLOR_BUTTON: shift(b, 0.08),
            CFG_NAME_COLOR_PRIMARY: to_white(b, 0.88),
            CFG_NAME_COLOR_SECONDARY: to_white(b, 0.62),
            CFG_NAME_COLOR_TERTIARY: to_white(b, 0.42),
            CFG_NAME_COLOR_ACCENT: accent,
        }

    def _save_colors_to_config(self, colors: dict) -> None:
        for k, v in colors.items():
            finder_config[k] = tuple(v)
        save_finder_config(finder_config)
        _theme.update_colors({
            'COLOR_BACKGROUND': tuple(finder_config[CFG_NAME_COLOR_BACKGROUND]),
            'COLOR_BUTTON': tuple(finder_config[CFG_NAME_COLOR_BUTTON]),
            'COLOR_PRIMARY': tuple(finder_config[CFG_NAME_COLOR_PRIMARY]),
            'COLOR_SECONDARY': tuple(finder_config[CFG_NAME_COLOR_SECONDARY]),
            'COLOR_TERTIARY': tuple(finder_config[CFG_NAME_COLOR_TERTIARY]),
            'COLOR_ACCENT': tuple(finder_config[CFG_NAME_COLOR_ACCENT]),
        })

    def color_picker_selected_color(self, picker, color) -> None:
        if color == self._initial_picker_color:
            return
        self._color_changed = True
        if getattr(self, '_is_manual_picker', False):
            new_color = tuple(color)
            finder_config[self._picker_cfg_key] = new_color
            save_finder_config(finder_config)
            cfg_to_theme = {
                CFG_NAME_COLOR_BACKGROUND: 'COLOR_BACKGROUND',
                CFG_NAME_COLOR_BUTTON: 'COLOR_BUTTON',
                CFG_NAME_COLOR_SECONDARY: 'COLOR_SECONDARY',
                CFG_NAME_COLOR_TERTIARY: 'COLOR_TERTIARY',
                CFG_NAME_COLOR_PRIMARY: 'COLOR_PRIMARY',
                CFG_NAME_COLOR_ACCENT: 'COLOR_ACCENT',
            }
            theme_key = cfg_to_theme.get(self._picker_cfg_key)
            if theme_key:
                _theme.update_colors({theme_key: new_color})
        else:
            self._save_colors_to_config(self._generate_theme_from_color(color))

    def color_picker_closing(self, picker) -> None:
        if self._color_changed:
            bui.screenmessage(
                get_lang_text('Settings.colorsUpdated'),
                color=_theme.get_color('COLOR_TERTIARY'),
            )

    def _unsubscribe(self) -> None:
        for color_name, callback in getattr(self, '_theme_subscriptions', []):
            _theme.unsubscribe(color_name, callback)
        self._theme_subscriptions = []

    def _close(self) -> None:
        self._unsubscribe()
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()




class _TranslationPopupMenuWindow(PopupMenuWindow):
    """PopupMenuWindow with theme bg, text, and scroll colors."""

    def __init__(self, *args, bg_color: tuple, text_color: tuple, **kwargs):
        _orig_tw = bui.textwidget
        _orig_sw = bui.scrollwidget
        _text_widgets: list[bui.Widget] = []
        _scroll_widgets: list[bui.Widget] = []

        def _intercept_tw(*a, **kw):
            result = _orig_tw(*a, **kw)
            if kw.get('parent') is not None and 'size' in kw:
                _text_widgets.append(result)
            return result

        def _intercept_sw(*a, **kw):
            result = _orig_sw(*a, **kw)
            _scroll_widgets.append(result)
            return result

        bui.textwidget = _intercept_tw
        bui.scrollwidget = _intercept_sw
        super().__init__(*args, **kwargs)
        bui.textwidget = _orig_tw
        bui.scrollwidget = _orig_sw

        bui.containerwidget(edit=self.root_widget, color=bg_color)
        for w in _text_widgets:
            if w.exists():
                bui.textwidget(edit=w, color=text_color)
        for w in _scroll_widgets:
            if w.exists():
                bui.scrollwidget(edit=w, color=_theme.get_color('COLOR_ACCENT'))


class _TranslationPopupMenu(PopupMenu):
    """PopupMenu that opens a themed popup window."""

    def _make_popup(self) -> None:
        if not self._button:
            return
        if self._opening_call:
            self._opening_call()
        self._window_widget = _TranslationPopupMenuWindow(
            position=self._button.get_screen_space_center(),
            delegate=self,
            width=self._width,
            maxwidth=self._maxwidth,
            scale=self._scale,
            choices=self._choices,
            current_choice=self._current_choice,
            choices_disabled=self._choices_disabled,
            choices_display=self._choices_display,
            bg_color=_theme.get_color('COLOR_BACKGROUND'),
            text_color=_theme.get_color('COLOR_PRIMARY'),
        ).root_widget


# All languages supported by Google Translate, sorted alphabetically.
LANGUAGES: dict[str, str] = {'auto': 'Auto-detect', **dict(sorted({
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
    'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
    'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo',
    'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
    'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao',
    'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
    'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'or': 'Odia',
    'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese',
    'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
    'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona',
    'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
    'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh',
    'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu',
}.items(), key=lambda item: item[1]))}


class TranslationSettings:
    def __init__(self) -> None:
        uiscale = bui.app.ui_v1.uiscale
        self._cfg = finder_config

        settings = self._get_settings()
        base_height = 225
        self._height = base_height + 40 * len(settings)
        self._width = 500

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            color=_theme.get_color('COLOR_BACKGROUND'),
            transition='in_scale',
            toolbar_visibility='menu_minimal_no_back',
            parent=bui.get_special_widget('overlay_stack'),
            on_outside_click_call=self._cancel,
            scale=(
                1.68 if uiscale is babase.UIScale.SMALL else
                1.5 if uiscale is babase.UIScale.MEDIUM else 1.0
            ),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height - 20),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('translateSettingsTitle'),
            scale=1.0,
            color=_theme.get_color('COLOR_PRIMARY'),
        )

        btn = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(30, self._height - 60),
            size=(30, 30),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=_theme.get_color('COLOR_BUTTON'),
            textcolor=_theme.get_color('COLOR_PRIMARY'),
            on_activate_call=self._cancel,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=btn)

        x_offset = self._width * 0.45
        y_pos = self._height - 115

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, y_pos + 20),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('translateSettingsTextfield'),
            scale=1.0,
            color=_theme.get_color('COLOR_SECONDARY'),
        )
        self._create_lang_menu(settings['tf_src'], y_pos - 30, 0)
        self._create_lang_menu(settings['tf_dst'], y_pos - 30, x_offset)
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, y_pos - 12),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
            scale=1.2,
            color=_theme.get_color('COLOR_SECONDARY'),
        )

        y_pos -= 80

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, y_pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=get_lang_text('translateSettingsOther'),
            scale=1.0,
            color=_theme.get_color('COLOR_SECONDARY'),
        )
        self._create_lang_menu(settings['other_src'], y_pos - 50, 0)
        self._create_lang_menu(settings['other_dst'], y_pos - 50, x_offset)
        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, y_pos - 32),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
            scale=1.2,
            color=_theme.get_color('COLOR_SECONDARY'),
        )

        y_pos -= 100

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.1, y_pos),
            size=(0, 0),
            h_align='left',
            v_align='center',
            text=get_lang_text('translateMethod'),
            scale=1.0,
            color=_theme.get_color('COLOR_SECONDARY'),
        )
        self._create_method_menu(x_offset, y_pos)

    def _get_settings(self) -> dict:
        lang_keys = list(LANGUAGES.keys())
        dst_keys = lang_keys[1:]  # exclude 'auto' for destination
        return {
            'tf_src':    {'config': CFG_NAME_TRANSLATE_SOURCE_TEXT_FIELD,      'choices': lang_keys},
            'tf_dst':    {'config': CFG_NAME_TRANSLATE_DESTINATION_TEXT_FIELD,  'choices': dst_keys},
            'other_src': {'config': CFG_NAME_TRANSLATE_SOURCE_OTHER,            'choices': lang_keys},
            'other_dst': {'config': CFG_NAME_TRANSLATE_DESTINATION_OTHER,       'choices': dst_keys},
        }

    def _styled_popup(self, pm: PopupMenu) -> None:
        btn = pm.get_button()
        if btn and btn.exists():
            bui.buttonwidget(
                edit=btn,
                color=_theme.get_color('COLOR_BUTTON'),
                textcolor=_theme.get_color('COLOR_SECONDARY'),
            )

    def _create_lang_menu(self, setting: dict, y_pos: float, x_offset: float) -> None:
        uiscale = bui.app.ui_v1.uiscale
        choices = setting['choices']
        cfg_key = setting['config']
        current = self._cfg.get(cfg_key, choices[0])
        if current not in choices:
            current = choices[0]
        pm = _TranslationPopupMenu(
            parent=self._root_widget,
            position=(self._width * 0.0875 + x_offset + x_offset * 0.25, y_pos),
            width=200,
            scale=(
                2.24 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else 1.2
            ),
            current_choice=current,
            choices=choices,
            choices_display=[babase.Lstr(value=LANGUAGES[l]) for l in choices],
            button_size=(130, 35),
            on_value_change_call=lambda v: self._save(cfg_key, v),
        )
        self._styled_popup(pm)

    def _create_method_menu(self, x_offset: float, y_pos: float) -> None:
        uiscale = bui.app.ui_v1.uiscale
        pm = _TranslationPopupMenu(
            parent=self._root_widget,
            position=(self._width * 0.0875 + x_offset + x_offset * 0.25, y_pos - 20),
            width=200,
            scale=(
                2.24 if uiscale is babase.UIScale.SMALL else
                1.8 if uiscale is babase.UIScale.MEDIUM else 1.2
            ),
            current_choice=self._cfg.get(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, 'api'),
            choices=['api', 'link'],
            choices_display=[
                babase.Lstr(value=get_lang_text('translateMethodAPI')),
                babase.Lstr(value=get_lang_text('translateMethodLINK')),
            ],
            button_size=(130, 35),
            on_value_change_call=lambda v: self._save(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, v),
        )
        self._styled_popup(pm)

    def _save(self, key: str, value: str) -> None:
        finder_config[key] = value

    def _cancel(self) -> None:
        save_finder_config(finder_config)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
        bui.getsound('swish').play()

_LOG = logging.getLogger(__name__)

def _load_camera_positions() -> list[dict[str, Any]]:
    try:
        if os.path.exists(CAMERA_FILE):
            with open(CAMERA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as exc:
        _LOG.exception('[camera] load failed: %s', exc)
    return []


def _save_camera_positions(positions: list[dict[str, Any]]) -> None:
    try:
        if not os.path.exists(MY_DIRECTORY):
            os.makedirs(MY_DIRECTORY)
        with open(CAMERA_FILE, 'w', encoding='utf-8') as f:
            json.dump(positions, f, indent=JSONS_DEFAULT_INDENT_FILE)
        _LOG.debug('[camera] saved %d positions', len(positions))
    except Exception as exc:
        _LOG.exception('[camera] save failed: %s', exc)


class CameraPositionsWindow(bui.Window):
    """Lists saved camera positions, allows applying and deleting them."""

    def close(self) -> None:
        if self._root_widget.exists():
            self._root_widget.delete()

    def __init__(self) -> None:
        width, height = 380, 420
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.35 if uiscale is babase.UIScale.SMALL else
            1.3 if uiscale is babase.UIScale.MEDIUM else 0.9
        )

        bg = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        text_color = _theme.get_color('COLOR_PRIMARY')

        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(width, height),
                scale=scale,
                color=bg,
                stack_offset=(0, 0),
                on_outside_click_call=self.close,
            ),
            prevent_main_window_auto_recreate=False,
        )

        self._width = width
        self._height = height
        self._btn_color = btn_color
        self._text_color = text_color
        self._positions: list[dict[str, Any]] = _load_camera_positions()

        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.45, height - 28),
            size=(0, 0),
            text=get_lang_text('Camera.positions.title'),
            scale=0.85,
            color=text_color,
            h_align='center',
            v_align='center',
            maxwidth=width * 0.4,
        )

        back_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(25, height - 45),
            size=(28, 28),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=btn_color,
            textcolor=text_color,
            enable_sound=False,
            on_activate_call=self.close,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=back_btn)

        bui.buttonwidget(
            parent=self._root_widget,
            position=(width - 38 - 60, height - 46),
            size=(60, 32),
            label=get_lang_text('Camera.overlay.reset'),
            button_type='square',
            color=btn_color,
            textcolor=text_color,
            autoselect=True,
            on_activate_call=self._reset,
        )

        scroll_height = height - 55
        scroll_w = int((width - 20) * 0.9)
        scroll_h = int(scroll_height * 0.88)
        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=((width - scroll_w) // 2, height - 50 - scroll_h),
            size=(scroll_w, scroll_h),
            capture_arrows=True,
        )
        self._list_container = bui.containerwidget(
            parent=self._scroll,
            size=(width - 36, max(60, len(self._positions) * 46 + 10)),
            background=False,
        )

        self._build_list()

    def _build_list(self) -> None:
        for child in self._list_container.get_children():
            child.delete()

        if not self._positions:
            bui.textwidget(
                parent=self._list_container,
                position=((self._width - 36) / 2, 30),
                size=(0, 0),
                text=get_lang_text('Camera.positions.noPositions'),
                scale=0.7,
                color=(0.5, 0.5, 0.5),
                h_align='center',
                v_align='center',
            )
            return

        row_h = 40
        gap = 6
        for i, entry in enumerate(reversed(self._positions)):
            idx = len(self._positions) - 1 - i
            y = (len(self._positions) - 1 - i) * (row_h + gap) + 6

            bui.textwidget(
                parent=self._list_container,
                position=(10, y + row_h / 2),
                size=(0, 0),
                text=entry.get('name', '?'),
                scale=0.72,
                color=self._text_color,
                h_align='left',
                v_align='center',
                maxwidth=self._width - 196,
            )
            bui.buttonwidget(
                parent=self._list_container,
                size=(52, row_h - 4),
                position=(self._width - 200, y + 2),
                label=get_lang_text('Camera.positions.apply'),
                button_type='square',
                color=(0.2, 0.6, 0.2),
                textcolor=(1.0, 1.0, 1.0),
                autoselect=True,
                on_activate_call=lambda e=entry: self._apply(e),
            )
            bui.buttonwidget(
                parent=self._list_container,
                size=(52, row_h - 4),
                position=(self._width - 132, y + 2),
                label=get_lang_text('Camera.positions.delete'),
                button_type='square',
                color=(0.6, 0.15, 0.15),
                textcolor=(1.0, 1.0, 1.0),
                autoselect=True,
                on_activate_call=lambda ix=idx: self._delete(ix),
            )

    def _reset(self) -> None:
        try:
            _babase.set_camera_manual(False)
            _LOG.debug('[camera] reset: manual mode off')
        except Exception as exc:
            _LOG.exception('[camera] _reset failed: %s', exc)

    def _apply(self, entry: dict[str, Any]) -> None:
        try:
            _babase.set_camera_manual(True)
            _babase.set_camera_position(*entry['pos'])
            _babase.set_camera_target(*entry['target'])
            _LOG.debug('[camera] applied "%s"', entry.get('name'))
            babase.screenmessage(
                f"{get_lang_text('Camera.positions.applied')}: {entry.get('name', '')}",
                color=(0.5, 0.8, 1.0),
            )
            finder_config[CFG_NAME_CAMERA_LAST_USED] = {
                'name': entry.get('name', ''),
                'pos': entry['pos'],
                'target': entry['target'],
            }
            save_finder_config(finder_config)
        except Exception as exc:
            _LOG.exception('[camera] apply failed: %s', exc)

    def _delete(self, idx: int) -> None:
        from bauiv1lib.confirm import ConfirmWindow
        entry = self._positions[idx] if 0 <= idx < len(self._positions) else None
        if entry is None:
            return
        name = entry.get('name', '?')
        confirm = ConfirmWindow(
            text=get_lang_text('Camera.positions.deleteConfirm').format(name=name),
            action=lambda: self._do_delete(idx),
            ok_text=get_lang_text('Camera.positions.delete'),
            cancel_text=bui.Lstr(resource='cancelText'),
            color=(1, 0.7, 0.7),
        )
        bui.containerwidget(edit=confirm.root_widget, color=_theme.get_color('COLOR_BACKGROUND'))

    def _do_delete(self, idx: int) -> None:
        if 0 <= idx < len(self._positions):
            removed = self._positions.pop(idx)
            _save_camera_positions(self._positions)
            _LOG.debug('[camera] deleted "%s"', removed.get('name'))
            new_h = max(60, len(self._positions) * 46 + 10)
            bui.containerwidget(edit=self._list_container, size=(self._width - 36, new_h))
            self._build_list()


class CameraOverlay(bui.Window):
    """Camera control overlay - layout matching the manual camera mod."""

    def close(self) -> None:
        if self._root_widget.exists():
            self._root_widget.delete()

    def __init__(self) -> None:
        btn_color = _theme.get_color('COLOR_BUTTON')
        text_color = _theme.get_color('COLOR_PRIMARY')

        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(0, 0),
                on_outside_click_call=self.close,
            ),
            prevent_main_window_auto_recreate=False,
        )

        self._btn_color = btn_color
        self._text_color = text_color
        arrow_sz = (50, 50)

        # position group (right side)
        bui.textwidget(
            parent=self._root_widget,
            position=(500, 185), size=(0, 0),
            text=get_lang_text('Camera.overlay.position'),
            scale=0.65, color=text_color,
            h_align='center', v_align='center',
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.LEFT_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(429, 60),
            on_activate_call=lambda: self._move_pos('x', -1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(538, 60),
            on_activate_call=lambda: self._move_pos('x', 1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(482, 120),
            on_activate_call=lambda: self._move_pos('y', 1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(482, 2),
            on_activate_call=lambda: self._move_pos('y', -1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=(100, 30),
            label=get_lang_text('Camera.overlay.zoomIn'),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-550, -60),
            on_activate_call=lambda: self._move_pos('z', -1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=(100, 30),
            label=get_lang_text('Camera.overlay.zoomOut'),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-550, -100),
            on_activate_call=lambda: self._move_pos('z', 1),
        )

        # target group (left side)
        bui.textwidget(
            parent=self._root_widget,
            position=(-462, 185), size=(0, 0),
            text=get_lang_text('Camera.overlay.angle'),
            scale=0.65, color=text_color,
            h_align='center', v_align='center',
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.LEFT_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-538, 60),
            on_activate_call=lambda: self._move_target('x', -1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.RIGHT_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-429, 60),
            on_activate_call=lambda: self._move_target('x', 1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-482, 120),
            on_activate_call=lambda: self._move_target('y', 1),
        )
        bui.buttonwidget(
            parent=self._root_widget, size=arrow_sz,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            repeat=True, button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(-482, 2),
            on_activate_call=lambda: self._move_target('y', -1),
        )

        # name field label aligned to field start
        bui.textwidget(
            parent=self._root_widget, position=(370, -30), size=(0, 0),
            text=get_lang_text('Camera.overlay.nameCam'),
            scale=0.75, color=text_color,
            h_align='left', v_align='center',
        )
        self._name_field = bui.textwidget(
            parent=self._root_widget, editable=True,
            size=(150, 40), position=(370, -80),
            text='', maxwidth=145, flatness=1.0,
            autoselect=True, v_align='center', corner_scale=0.7,
        )

        # action buttons
        bui.buttonwidget(
            parent=self._root_widget, size=(60, 30),
            label=get_lang_text('Camera.overlay.save'),
            button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(370, -120), on_activate_call=self._save,
        )
        bui.buttonwidget(
            parent=self._root_widget, size=(60, 30),
            label=get_lang_text('Camera.overlay.reset'),
            button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(440, -120), on_activate_call=self._reset,
        )
        bui.buttonwidget(
            parent=self._root_widget, size=(60, 30),
            label=get_lang_text('Camera.overlay.done'),
            button_type='square', autoselect=True,
            color=btn_color, textcolor=text_color,
            position=(510, -120), on_activate_call=self.close,
        )

    def _move_pos(self, axis: str, sign: int) -> None:
        try:
            x, y, z = _babase.get_camera_position()
            _LOG.debug('[camera] pos before: (%s, %s, %s)', x, y, z)
            d = float(sign)
            if axis == 'x':
                x += d
            elif axis == 'y':
                y += d
            elif axis == 'z':
                z += d
            _babase.set_camera_manual(True)
            _babase.set_camera_position(x, y, z)
            _LOG.debug('[camera] pos after: (%s, %s, %s)', x, y, z)
        except Exception as exc:
            _LOG.exception('[camera] _move_pos failed: %s', exc)

    def _move_target(self, axis: str, sign: int) -> None:
        try:
            x, y, z = _babase.get_camera_target()
            _LOG.debug('[camera] target before: (%s, %s, %s)', x, y, z)
            d = float(sign)
            if axis == 'x':
                x += d
            elif axis == 'y':
                y += d
            _babase.set_camera_manual(True)
            _babase.set_camera_target(x, y, z)
            _LOG.debug('[camera] target after: (%s, %s, %s)', x, y, z)
        except Exception as exc:
            _LOG.exception('[camera] _move_target failed: %s', exc)

    def _save(self) -> None:
        name = str(bui.textwidget(query=self._name_field)).strip()
        if not name:
            name = f'Cam {len(_load_camera_positions()) + 1}'
        try:
            pos = list(_babase.get_camera_position())
            tgt = list(_babase.get_camera_target())
        except Exception as exc:
            _LOG.exception('[camera] get position failed: %s', exc)
            return
        positions = _load_camera_positions()
        positions.append({'name': name, 'pos': pos, 'target': tgt})
        _save_camera_positions(positions)
        bui.textwidget(edit=self._name_field, text='')
        babase.screenmessage(
            f"{get_lang_text('Camera.positions.saved')}: {name}",
            color=(0.5, 1.0, 0.5),
        )
        _LOG.debug('[camera] saved "%s" pos=%s tgt=%s', name, pos, tgt)

    def _reset(self) -> None:
        try:
            _babase.set_camera_manual(False)
            _LOG.debug('[camera] reset: manual mode off')
        except Exception as exc:
            _LOG.exception('[camera] _reset failed: %s', exc)




_LOG = logging.getLogger(__name__)

_disco_timer: babase.AppTimer | None = None


def _apply_tint(color: tuple) -> None:
    try:
        activity = bs.get_foreground_host_activity()
        if activity is not None:
            activity.globalsnode.tint = color
    except Exception as exc:
        _LOG.debug('[tint] apply failed: %s', exc)


def _disco_tick() -> None:
    color = (
        random.uniform(0.0, 0.6),
        random.uniform(0.0, 0.6),
        random.uniform(0.0, 0.6),
    )
    _apply_tint(color)


def _start_disco(speed: float) -> None:
    global _disco_timer
    _stop_disco()
    _disco_timer = babase.AppTimer(max(0.1, speed), _disco_tick, repeat=True)


def _stop_disco() -> None:
    global _disco_timer
    _disco_timer = None


def apply_saved_tint() -> None:
    """Apply persisted tint color on startup if disco is off."""
    if finder_config.get(CFG_NAME_TINT_DISCO, False):
        speed = float(finder_config.get(CFG_NAME_TINT_DISCO_SPEED, 1.0))
        _start_disco(speed)
    else:
        color = finder_config.get(CFG_NAME_TINT_COLOR, (1.0, 1.0, 1.0))
        if tuple(color) != (1.0, 1.0, 1.0):
            _apply_tint(tuple(color))


class TintWindow(bui.Window):
    """Map tint control: solid color or disco mode."""

    def close(self) -> None:
        if self._root_widget.exists():
            self._root_widget.delete()

    def __init__(self) -> None:
        width, height = 360, 320
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.8 if uiscale is babase.UIScale.SMALL else
            1.3 if uiscale is babase.UIScale.MEDIUM else 0.9
        )

        bg = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        text_color = _theme.get_color('COLOR_PRIMARY')

        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(width, height),
                scale=scale,
                color=bg,
                stack_offset=(0, 0),
                on_outside_click_call=self.close,
            ),
            prevent_main_window_auto_recreate=False,
        )

        self._width = width
        self._height = height
        self._btn_color = btn_color
        self._text_color = text_color
        self._color_changed = False
        self._current_color = tuple(
            finder_config.get(CFG_NAME_TINT_COLOR, (1.0, 1.0, 1.0))
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(width / 2, height - 26),
            size=(0, 0),
            text=get_lang_text('Tint.title'),
            scale=0.85,
            color=text_color,
            h_align='center',
            v_align='center',
            maxwidth=width - 40,
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(width - 46, height - 42),
            size=(36, 36),
            label=babase.charstr(babase.SpecialChar.CLOSE),
            button_type='square',
            color=btn_color,
            textcolor=text_color,
            scale=0.8,
            on_activate_call=self.close,
        )

        y = height - 80

        # Color label
        bui.textwidget(
            parent=self._root_widget,
            position=(20, y),
            size=(0, 0),
            text=get_lang_text('Tint.colorLabel'),
            scale=0.75,
            color=text_color,
            h_align='left',
            v_align='center',
        )
        self._color_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - 120, y - 16),
            size=(90, 32),
            label='',
            button_type='square',
            color=self._current_color,
            autoselect=True,
            on_activate_call=self._open_color_picker,
        )

        y -= 60

        # Disco checkbox
        disco_val = bool(finder_config.get(CFG_NAME_TINT_DISCO, False))
        self._disco_val = disco_val
        self._disco_checkbox = bui.checkboxwidget(
            parent=self._root_widget,
            position=(20, y),
            size=(width - 40, 32),
            maxwidth=(width - 40) * 0.9,
            text=get_lang_text('Tint.disco'),
            scale=0.82,
            value=disco_val,
            textcolor=(0, 1, 0) if disco_val else (0.95, 0.65, 0),
        )
        bui.checkboxwidget(
            edit=self._disco_checkbox,
            on_value_change_call=self._on_disco_change,
        )

        y -= 52

        # Disco speed
        bui.textwidget(
            parent=self._root_widget,
            position=(20, y),
            size=(0, 0),
            text=get_lang_text('Tint.discoSpeed'),
            scale=0.75,
            color=text_color,
            h_align='left',
            v_align='center',
        )
        speed_val = finder_config.get(CFG_NAME_TINT_DISCO_SPEED, 1.0)
        self._speed_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(80, 32),
            position=(width - 110, y - 14),
            text=str(round(float(speed_val), 2)),
            maxwidth=75,
            flatness=1.0,
            autoselect=True,
            v_align='center',
            corner_scale=0.7,
            description='0.1-60',
        )

        y -= 60

        # Apply / Reset buttons
        bui.buttonwidget(
            parent=self._root_widget,
            position=(20, y),
            size=(90, 36),
            label=get_lang_text('Tint.apply'),
            button_type='square',
            color=(0.2, 0.5, 0.2),
            textcolor=(1, 1, 1),
            autoselect=True,
            on_activate_call=self._apply,
        )
        bui.buttonwidget(
            parent=self._root_widget,
            position=(125, y),
            size=(90, 36),
            label=get_lang_text('Tint.reset'),
            button_type='square',
            color=btn_color,
            textcolor=text_color,
            autoselect=True,
            on_activate_call=self._reset,
        )

    def _open_color_picker(self) -> None:
        colorpicker.ColorPicker(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            initial_color=self._current_color,
            delegate=self,
            tag='tint',
        )

    def color_picker_selected_color(self, picker: Any, color: tuple) -> None:
        self._current_color = tuple(color)
        bui.buttonwidget(edit=self._color_btn, color=self._current_color)
        self._color_changed = True

    def color_picker_closing(self, picker: Any) -> None:
        pass

    def _on_disco_change(self, val: bool) -> None:
        self._disco_val = val
        bui.checkboxwidget(
            edit=self._disco_checkbox,
            textcolor=(0, 1, 0) if val else (0.95, 0.65, 0),
        )

    def _apply(self) -> None:
        disco = self._disco_val
        finder_config[CFG_NAME_TINT_DISCO] = disco

        try:
            speed = float(str(bui.textwidget(query=self._speed_field)).strip())
            speed = max(0.1, min(60.0, speed))
        except (ValueError, TypeError):
            speed = 1.0
        finder_config[CFG_NAME_TINT_DISCO_SPEED] = speed

        if disco:
            _start_disco(speed)
        else:
            _stop_disco()
            finder_config[CFG_NAME_TINT_COLOR] = list(self._current_color)
            _apply_tint(self._current_color)

        save_finder_config(finder_config)
        self.close()

    def _reset(self) -> None:
        _stop_disco()
        finder_config[CFG_NAME_TINT_DISCO] = False
        finder_config[CFG_NAME_TINT_COLOR] = [1.0, 1.0, 1.0]
        save_finder_config(finder_config)
        _apply_tint((1.0, 1.0, 1.0))
        self.close()





_LOG = logging.getLogger(__name__)


def _load() -> list[dict[str, Any]]:
    try:
        if os.path.exists(LAST_SERVERS_FILE):
            with open(LAST_SERVERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as exc:
        _LOG.exception('[lastservers] load failed: %s', exc)
    return []


def _save(servers: list[dict[str, Any]]) -> None:
    try:
        if not os.path.exists(MY_DIRECTORY):
            os.makedirs(MY_DIRECTORY)
        with open(LAST_SERVERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(servers, f, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as exc:
        _LOG.exception('[lastservers] save failed: %s', exc)


def record_server(name: str, address: str, port: int) -> None:
    """Record a server entry, replacing the oldest if at capacity."""
    if not address:
        return
    max_count = int(finder_config.get(CFG_NAME_MAX_RECENT_SERVERS, 5))
    servers = _load()
    now = time.time()

    # If already exists, move it to the top with updated timestamp
    for i, entry in enumerate(servers):
        if entry.get('address') == address and entry.get('port') == port:
            servers.pop(i)
            servers.insert(0, {
                'name': name or entry.get('name', ''),
                'address': address,
                'port': port,
                'timestamp': now,
            })
            _save(servers)
            return

    if len(servers) >= max_count:
        oldest_idx = min(range(len(servers)), key=lambda i: servers[i].get('timestamp', 0))
        servers.pop(oldest_idx)

    servers.insert(0, {'name': name, 'address': address, 'port': port, 'timestamp': now})

    _save(servers)
    _LOG.debug('[lastservers] recorded "%s" %s:%d', name, address, port)


class LastServersWindow(bui.Window):
    """Popup listing recently visited servers with a join button."""

    def close(self) -> None:
        if self._root_widget.exists():
            self._root_widget.delete()

    def __init__(self, party_window: bui.Window | None = None) -> None:
        self._party_window = party_window
        width, height = 400, 380
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.8 if uiscale is babase.UIScale.SMALL else
            1.3 if uiscale is babase.UIScale.MEDIUM else 0.9
        )

        bg = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        text_color = _theme.get_color('COLOR_PRIMARY')
        accent_color = _theme.get_color('COLOR_ACCENT')

        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(width, height),
                scale=scale,
                color=bg,
                stack_offset=(0, 0),
                on_outside_click_call=self.close,
            ),
            prevent_main_window_auto_recreate=False,
        )

        self._width = width
        self._height = height
        self._btn_color = btn_color
        self._text_color = text_color

        bui.textwidget(
            parent=self._root_widget,
            position=(width / 2, height - 26),
            size=(0, 0),
            text=get_lang_text('RecentServers.title'),
            scale=0.85,
            color=text_color,
            h_align='center',
            v_align='center',
            maxwidth=width - 80,
        )
        bui.buttonwidget(
            parent=self._root_widget,
            position=(17, height - 42),
            size=(36, 36),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=btn_color,
            textcolor=text_color,
            on_activate_call=self.close,
        )

        scroll_width = width - 45
        scroll_height = height - 73
        scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=((width - scroll_width) / 2, 20),
            size=(scroll_width, scroll_height),
            color=accent_color,
            capture_arrows=True,
        )
        servers = sorted(_load(), key=lambda e: e.get('timestamp', 0), reverse=True)
        content_h = max(60, len(servers) * 56 + 10)
        self._container = bui.containerwidget(
            parent=scroll,
            size=(width - 51, content_h),
            background=False,
        )
        self._build_list(servers)

    def _relative_time(self, ts: float) -> str:
        elapsed = time.time() - ts
        if elapsed < 60:
            return get_lang_text('RecentServers.justNow')
        minutes = int(elapsed / 60)
        if minutes < 60:
            return get_lang_text('RecentServers.minutesAgo').replace('{n}', str(minutes))
        hours = int(elapsed / 3600)
        if hours < 24:
            return get_lang_text('RecentServers.hoursAgo').replace('{n}', str(hours))
        days = int(elapsed / 86400)
        return get_lang_text('RecentServers.daysAgo').replace('{n}', str(days))

    def _build_list(self, servers: list[dict[str, Any]]) -> None:
        if not servers:
            bui.textwidget(
                parent=self._container,
                position=((self._width - 36) / 2, 30),
                size=(0, 0),
                text=get_lang_text('RecentServers.noServers'),
                scale=0.72,
                color=(0.5, 0.5, 0.5),
                h_align='center',
                v_align='center',
            )
            return

        row_h = 50
        gap = 6
        total = len(servers)
        for i, entry in enumerate(servers):
            y = (total - 1 - i) * (row_h + gap) + 6
            name = entry.get('name') or entry.get('address', '?')
            addr = entry.get('address', '')
            port = entry.get('port', 0)
            ts = entry.get('timestamp', 0)
            date_str = self._relative_time(ts) if ts else ''

            bui.textwidget(
                parent=self._container,
                position=(10, y + row_h * 0.65),
                size=(0, 0),
                text=name,
                scale=0.68,
                color=self._text_color,
                h_align='left',
                v_align='center',
                maxwidth=180,
            )
            bui.textwidget(
                parent=self._container,
                position=(10, y + row_h * 0.28),
                size=(0, 0),
                text=date_str,
                scale=0.58,
                color=(0.55, 0.55, 0.55),
                h_align='left',
                v_align='center',
                maxwidth=self._width - 170,
            )

            # Peek button
            peek_btn = bui.buttonwidget(
                parent=self._container,
                size=(65, row_h - 8),
                position=(self._width - 190, y + 4),
                label=get_lang_text('RecentServers.peek'),
                button_type='square',
                color=(0.5, 0.4, 0.93),
                textcolor=(1.0, 1.0, 1.0),
                autoselect=True,
                scale=0.85,
            )
            bui.buttonwidget(
                edit=peek_btn,
                on_activate_call=lambda a=addr, p=port, n=name, b=peek_btn: self._peek(a, p, n, b),
            )

            # Join button
            bui.buttonwidget(
                parent=self._container,
                size=(58, row_h - 8),
                position=(self._width - 122, y + 4),
                label=get_lang_text('RecentServers.join'),
                button_type='square',
                color=(0.2, 0.5, 0.2),
                textcolor=(1.0, 1.0, 1.0),
                autoselect=True,
                scale=0.85,
                on_activate_call=lambda a=addr, p=port: self._join(a, p),
            )

    def _peek(self, address: str, port: int, name: str, btn: bui.Widget) -> None:
        if btn.exists():
            ServerViewOverlay(address=address, port=port, source_widget=btn, name=name)

    def _join(self, address: str, port: int) -> None:
        try:
            from bascenev1 import connect_to_party
            self.close()
            if self._party_window is not None:
                self._party_window.close()
            connect_to_party(address, int(port), False)
        except Exception as exc:
            _LOG.exception('[lastservers] join failed: %s', exc)
            babase.screenmessage(
                get_lang_text('RecentServers.joinFailed'),
                color=(1.0, 0.3, 0.3),
            )

class SortMessagesList:
    """Window for reordering, adding, editing and deleting a list of strings."""

    def __init__(
        self,
        data: List[str],
        write_data_func: Callable[[List[str]], None],
        label: str,
    ) -> None:
        uiscale = bui.app.ui_v1.uiscale
        bg_color = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        title_color = _theme.get_color('COLOR_PRIMARY')
        accent_color = _theme.get_color('COLOR_ACCENT')

        self._width = (600 if uiscale is babase.UIScale.SMALL else
                       750 if uiscale is babase.UIScale.MEDIUM else 825)
        self._height = (325 if uiscale is babase.UIScale.SMALL else
                        375 if uiscale is babase.UIScale.MEDIUM else 425)

        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            on_outside_click_call=self._save,
            color=bg_color,
            parent=bui.get_special_widget('overlay_stack'),
            scale=(2.0 if uiscale is babase.UIScale.SMALL else
                   1.3 if uiscale is babase.UIScale.MEDIUM else 1.0),
            stack_offset=(0, -16) if uiscale is babase.UIScale.SMALL else (0, 0),
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.25, self._height - 50),
            size=(self._width * 0.5, 25),
            text=label,
            color=title_color,
            scale=1.05,
            h_align='center',
            v_align='center',
            maxwidth=270,
        )

        _btn_sz = int(75 * 0.7)
        _gap = 8
        _scroll_cy = 65 + (self._height - 130) // 2
        _down_y = _scroll_cy - (_btn_sz * 2 + _gap) // 2
        _up_y = _down_y + _btn_sz + _gap

        bui.buttonwidget(
            parent=self._root_widget,
            position=(10, _up_y),
            size=(_btn_sz, _btn_sz),
            on_activate_call=self._move_up,
            label=babase.charstr(babase.SpecialChar.UP_ARROW),
            button_type='square',
            color=btn_color,
            textcolor=title_color,
            autoselect=True,
            repeat=True,
        )
        bui.buttonwidget(
            parent=self._root_widget,
            position=(10, _down_y),
            size=(_btn_sz, _btn_sz),
            on_activate_call=self._move_down,
            label=babase.charstr(babase.SpecialChar.DOWN_ARROW),
            button_type='square',
            color=btn_color,
            textcolor=title_color,
            autoselect=True,
            repeat=True,
        )
        _is_small = uiscale is babase.UIScale.SMALL
        _back_sz = 40 if _is_small else 50
        _back_x = self._width * 0.0025 + (18 if _is_small else 13)
        bui.buttonwidget(
            parent=self._root_widget,
            position=(_back_x, self._height * 0.825 + 5),
            size=(_back_sz, _back_sz),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._save,
            color=btn_color,
            textcolor=title_color,
            iconscale=1.2,
        )

        self._scroll_width = self._width - 200
        self._scroll_height = self._height - 145
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._scroll_height),
            color=accent_color,
            position=(83, 75),
        )
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0,
        )

        _tf_y = self._height * 0.055 + 7
        self._attribute_text_field = bui.textwidget(
            parent=self._root_widget,
            editable=True,
            size=(self._scroll_width - 60, 33),
            position=(93, _tf_y),
            text='',
            maxwidth=300,
            shadow=0.3,
            flatness=1.0,
            description='Enter message here',
            autoselect=True,
            v_align='center',
        )

        _rbtn_x = self._width * 0.9375 - 40 - (15 if _is_small else 0)
        _rbtn_gap = 10
        _rbtn_cy = self._height // 2
        _rbtn_add_y = _rbtn_cy - (50 * 3 + _rbtn_gap * 2) // 2
        _rbtn_reload_y = _rbtn_add_y + 50 + _rbtn_gap
        _rbtn_delete_y = _rbtn_reload_y + 50 + _rbtn_gap

        delete_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(_rbtn_x, _rbtn_delete_y),
            size=(50, 50),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2,
            on_activate_call=self._delete_attribute,
            button_type='square',
            color=btn_color,
            textcolor=(1, 0.3, 0.3),
            enable_sound=False,
            autoselect=True,
        )
        _ = delete_btn

        bui.buttonwidget(
            parent=self._root_widget,
            position=(_rbtn_x, _rbtn_reload_y),
            size=(50, 50),
            icon=bui.gettexture('replayIcon'),
            iconscale=1.25,
            button_type='square',
            color=btn_color,
            textcolor=title_color,
            enable_sound=False,
            on_activate_call=self._edit_attribute,
            autoselect=True,
        )

        add_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(_rbtn_x, _rbtn_add_y),
            size=(50, 50),
            icon=bui.gettexture('powerupHealth'),
            iconscale=1.25,
            button_type='square',
            color=btn_color,
            textcolor=accent_color,
            enable_sound=False,
            on_activate_call=self._add_attribute,
            autoselect=True,
        )
        bui.textwidget(edit=self._attribute_text_field, on_return_press_call=add_btn.activate)

        bui.buttonwidget(
            parent=self._root_widget,
            position=(97 + self._scroll_width - 60 + 12, _tf_y + (33 - 25) // 2),
            size=(25, 25),
            label='©',
            button_type='backSmall',
            color=btn_color,
            textcolor=accent_color,
            on_activate_call=self._copy_text,
            autoselect=True,
        )

        self.msgs = data
        self.original_msgs = list(data)
        self.save = write_data_func
        self._msg_selected: tuple = ()
        self.text_widgets_dict: dict[str, bui.Widget] = {}

        self._refresh()
        bui.containerwidget(edit=self._root_widget, on_cancel_call=self._save)

    def _refresh(self) -> None:
        for child in self._columnwidget.get_children():
            child.delete()
        self.text_widgets_dict.clear()
        for msg in enumerate(self.msgs):
            txt = bui.textwidget(
                parent=self._columnwidget,
                size=(self._scroll_width - 10, 30),
                selectable=True,
                always_highlight=True,
                on_select_call=babase.Call(self._on_msg_select, msg),
                text=msg[1],
                h_align='left',
                v_align='center',
                maxwidth=self._scroll_width,
                color=_theme.get_color('COLOR_PRIMARY'),
            )
            self.text_widgets_dict[msg[1]] = txt
            if msg == self._msg_selected:
                bui.columnwidget(edit=self._columnwidget, selected_child=txt, visible_child=txt)

    def _on_msg_select(self, msg: tuple) -> None:
        self._msg_selected = msg
        index = msg[0]
        if 0 <= index < len(self.msgs):
            bui.textwidget(edit=self._attribute_text_field, text=self.msgs[index])
        else:
            self._refresh()
            self._msg_selected = ()
            bui.textwidget(edit=self._attribute_text_field, text='')

    def _move_up(self) -> None:
        if not self._msg_selected:
            return
        index, msg = self._msg_selected[0], self._msg_selected[1]
        if index > 0:
            self.msgs.insert(index - 1, self.msgs.pop(index))
            self._msg_selected = (index - 1, msg)
            self._refresh()

    def _move_down(self) -> None:
        if not self._msg_selected:
            return
        index, msg = self._msg_selected[0], self._msg_selected[1]
        if index + 1 < len(self.msgs):
            self.msgs.insert(index + 1, self.msgs.pop(index))
            self._msg_selected = (index + 1, msg)
            self._refresh()

    def _add_attribute(self) -> None:
        text: str = bui.textwidget(query=self._attribute_text_field)
        text = text.strip()
        if not text:
            bui.screenmessage(get_lang_text('Global.fieldEmpty'), (1, 0, 0))
            bui.getsound('error').play()
            return
        if text in self.msgs:
            bui.screenmessage(get_lang_text('Global.fieldEmpty'), (1, 0.5, 0))
            bui.getsound('error').play()
            return
        self.msgs.append(text)
        bui.textwidget(edit=self._attribute_text_field, text='')
        self._refresh()
        bui.getsound('shieldUp').play()

    def _edit_attribute(self) -> None:
        if not self._msg_selected:
            return
        new_text: str = bui.textwidget(query=self._attribute_text_field)
        new_text = new_text.strip()
        if not new_text:
            bui.getsound('error').play()
            return
        index = self._msg_selected[0]
        old_msg = self._msg_selected[1]
        if new_text == old_msg:
            return
        self.msgs[index] = new_text
        widget = self.text_widgets_dict.get(old_msg)
        if widget and widget.exists():
            bui.textwidget(edit=widget, text=new_text)
            self.text_widgets_dict[new_text] = widget
            del self.text_widgets_dict[old_msg]
        else:
            self._refresh()
        self._msg_selected = (index, new_text)
        bui.getsound('shieldUp').play()

    def _delete_attribute(self) -> None:
        if not self._msg_selected or not self.msgs:
            bui.getsound('error').play()
            return
        index = self._msg_selected[0]
        msg = self.msgs.pop(index)
        widget = self.text_widgets_dict.pop(msg, None)
        if widget and widget.exists():
            widget.delete()
        if index > 0:
            self._msg_selected = (index - 1, self.msgs[index - 1])
        else:
            self._msg_selected = ()
        bui.getsound('shieldDown').play()

    def _copy_text(self) -> None:
        text = bui.textwidget(query=self._attribute_text_field)
        if text and bui.clipboard_is_supported():
            bui.clipboard_set_text(text)
            bui.screenmessage(get_lang_text('Global.copiedToClipboard'), color=(0.6, 1.0, 0.6))

    def _save(self) -> None:
        try:
            self.save(self.msgs)
        except Exception:
            pass
        if self.original_msgs != self.msgs:
            bui.getsound('gunCocking').play()
        bui.containerwidget(edit=self._root_widget, transition='out_right')
        bui.getsound('swish').play()


_PAGE_SIZE = 10


def _relative_time(ts: float | None, fallback: str | None = None) -> str:
    if ts is not None:
        elapsed = time.time() - ts
        if elapsed < 60:
            return get_lang_text('RecentPlayers.justNow')
        minutes = int(elapsed / 60)
        if minutes < 60:
            return get_lang_text('RecentPlayers.minutesAgo').replace('{n}', str(minutes))
        hours = int(elapsed / 3600)
        if hours < 24:
            return get_lang_text('RecentPlayers.hoursAgo').replace('{n}', str(hours))
        days = int(elapsed / 86400)
        return get_lang_text('RecentPlayers.daysAgo').replace('{n}', str(days))
    return fallback or ''


class RecentPlayersWindow(bui.Window):
    """Lists recently seen players with search and pagination."""

    def close(self) -> None:
        if self._root_widget.exists():
            self._root_widget.delete()

    def __init__(self) -> None:
        width, height = 570, 520
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            1.225 if uiscale is babase.UIScale.SMALL else
            1.25 if uiscale is babase.UIScale.MEDIUM else 0.9
        )

        bg = _theme.get_color('COLOR_BACKGROUND')
        btn_color = _theme.get_color('COLOR_BUTTON')
        text_color = _theme.get_color('COLOR_PRIMARY')

        super().__init__(
            root_widget=bui.containerwidget(
                parent=bui.get_special_widget('overlay_stack'),
                size=(width, height),
                scale=scale,
                color=bg,
                stack_offset=(0, 0),
                on_outside_click_call=self.close,
            ),
            prevent_main_window_auto_recreate=False,
        )

        self._width = width
        self._height = height
        self._btn_color = btn_color
        self._text_color = text_color
        self._current_page = 0
        self._all_players: list[tuple[str, dict[str, Any]]] = []
        self._filtered: list[tuple[str, dict[str, Any]]] = []

        # Title
        bui.textwidget(
            parent=self._root_widget,
            position=(width / 2, height - 26),
            size=(0, 0),
            text=get_lang_text('RecentPlayers.title'),
            scale=0.85,
            color=text_color,
            h_align='center',
            v_align='center',
            maxwidth=width - 80,
        )

        # Search row
        row_h = 34
        back_w = 36
        search_btn_w = 68
        row_gap = 6
        search_y = height - 76
        cursor_x = 29

        bui.buttonwidget(
            parent=self._root_widget,
            position=(cursor_x, search_y - 6),
            size=(back_w, row_h),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=btn_color,
            textcolor=text_color,
            enable_sound=False,
            on_activate_call=self.close,
        )
        cursor_x += back_w + row_gap + 2 

        field_w = width - cursor_x - row_gap - search_btn_w - 15 - 14

        self._search_input = bui.textwidget(
            parent=self._root_widget,
            position=(cursor_x + 4, search_y - 8),
            size=(field_w, row_h),
            text='',
            editable=True,
            description=get_lang_text('Global.search'),
            maxwidth=field_w - 8,
            h_align='left',
            v_align='center',
            color=text_color,
            on_return_press_call=bui.WeakCallStrict(self._on_search),
        )
        cursor_x += field_w + row_gap

        bui.buttonwidget(
            parent=self._root_widget,
            position=(width - search_btn_w - 20, search_y - 6),
            size=(search_btn_w, row_h),
            label=get_lang_text('Global.search'),
            color=btn_color,
            textcolor=text_color,
            on_activate_call=bui.WeakCallStrict(self._on_search),
        )

        scroll_top = search_y - row_gap
        # Scroll
        self._scroll = bui.scrollwidget(
            parent=self._root_widget,
            position=(25, 55),
            size=(width - 35, scroll_top - 55 - 10),
            capture_arrows=True,
            color=_theme.get_color('COLOR_ACCENT'),
        )

        # Pagination container
        self._pagination_widget = bui.containerwidget(
            parent=self._root_widget,
            size=(width - 20, 34),
            position=(10, 5),
            background=False,
        )

        self._list_container: bui.Widget | None = None
        self._page_indicator: bui.Widget | None = None

        # Load and show
        players = get_all_players()
        self._all_players = sorted(
            players.items(),
            key=lambda kv: kv[1].get('last_met_ts') or 0,
            reverse=True,
        )
        self._filtered = list(self._all_players)
        self._show_page(0)

    def _refresh(self) -> None:
        players = get_all_players()
        self._all_players = sorted(
            players.items(),
            key=lambda kv: kv[1].get('last_met_ts') or 0,
            reverse=True,
        )
        query = bui.textwidget(query=self._search_input).strip().lower()
        if query:
            self._filtered = [
                (n, d) for n, d in self._all_players
                if query in n.lower()
                or query in (d.get('nickname') or '').lower()
                or any(query in p.lower() for p in (d.get('profile_name') or []))
            ]
        else:
            self._filtered = list(self._all_players)
        self._show_page(self._current_page)

    def _on_search(self) -> None:
        query = bui.textwidget(query=self._search_input).strip().lower()
        if query:
            self._filtered = [
                (name, data) for name, data in self._all_players
                if query in name.lower()
                or query in (data.get('nickname') or '').lower()
                or any(query in p.lower() for p in (data.get('profile_name') or []))
            ]
        else:
            self._filtered = list(self._all_players)
        self._show_page(0)

    def _show_page(self, page: int) -> None:
        self._current_page = page

        if self._list_container and self._list_container.exists():
            self._list_container.delete()

        start = page * _PAGE_SIZE
        page_items = self._filtered[start:start + _PAGE_SIZE]

        row_h, gap = 64, 4
        content_h = max(60, len(page_items) * (row_h + gap) + 10)
        self._list_container = bui.containerwidget(
            parent=self._scroll,
            size=(self._width - 36, content_h),
            background=False,
        )

        if not page_items:
            bui.textwidget(
                parent=self._list_container,
                position=((self._width - 36) / 2, 30),
                size=(0, 0),
                text=get_lang_text('RecentPlayers.noPlayers'),
                scale=0.72,
                color=(0.5, 0.5, 0.5),
                h_align='center',
                v_align='center',
            )
        else:
            total = len(page_items)
            for i, (name, data) in enumerate(page_items):
                y = (total - 1 - i) * (row_h + gap) + 6
                self._build_row(name, data, y, row_h)

        self._build_pagination()

    def _build_row(
        self,
        name: str,
        data: dict[str, Any],
        y: float,
        row_h: float,
    ) -> None:
        profiles: list[str] = data.get('profile_name') or []
        profile_str = profiles[0] if profiles else ''
        nickname = data.get('nickname') or ''
        ts = data.get('last_met_ts')
        time_str = _relative_time(ts)

        display_name = f'{name} ({nickname})' if nickname else name
        card_w = self._width - 42

        card = bui.buttonwidget(
            parent=self._list_container,
            position=(-7, y),
            size=(card_w, row_h),
            label='',
            color=self._btn_color,
            enable_sound=True,
            autoselect=True,
            on_activate_call=lambda n=name: PlayerInfoPopup(
                n, on_close=bui.WeakCallStrict(self._refresh)
            ),
        )

        icon_size = 52
        icon_x = 10
        icon_y = y + (row_h - icon_size) / 2
        bui.imagewidget(
            parent=self._list_container,
            draw_controller=card,
            position=(icon_x, icon_y),
            size=(icon_size, icon_size),
            texture=bui.gettexture('cuteSpaz'),
        )

        text_x = icon_x + icon_size + 12

        # Name
        bui.textwidget(
            parent=self._list_container,
            draw_controller=card,
            position=(text_x, y + row_h * 0.72),
            size=(0, 0),
            text=babase.Lstr(value=display_name),
            scale=0.78,
            color=self._text_color,
            h_align='left',
            v_align='center',
            maxwidth=card_w * 0.52,
        )
        # Profile name
        if profile_str:
            bui.textwidget(
                parent=self._list_container,
                draw_controller=card,
                position=(text_x, y + row_h * 0.40),
                size=(0, 0),
                text=babase.Lstr(value=profile_str),
                scale=0.60,
                color=(0.6, 0.7, 0.9),
                h_align='left',
                v_align='center',
                maxwidth=card_w * 0.48,
            )
        # Time
        if time_str:
            bui.textwidget(
                parent=self._list_container,
                draw_controller=card,
                position=(card_w - 40, y + row_h * 0.5),
                size=(0, 0),
                text=babase.Lstr(value=time_str),
                scale=0.78,
                color=self._text_color,
                h_align='right',
                v_align='center',
                maxwidth=card_w * 0.32,
            )

    def _build_pagination(self) -> None:
        if self._pagination_widget.exists():
            self._pagination_widget.delete()
        if self._page_indicator and self._page_indicator.exists():
            self._page_indicator.delete()
        self._page_indicator = None

        total_pages = max(1, (len(self._filtered) + _PAGE_SIZE - 1) // _PAGE_SIZE)
        self._pagination_widget = bui.containerwidget(
            parent=self._root_widget,
            size=(self._width - 20, 34),
            position=(10, 5),
            background=False,
        )

        if total_pages <= 1:
            return

        MAX_VISIBLE = 10
        btn_w = 27
        gap = 9
        nav_w = 28

        if total_pages <= MAX_VISIBLE:
            total_btn_w = total_pages * (btn_w + gap)
            start_x = max(0, (self._width - 20 - total_btn_w) / 2) + 8
            for p in range(total_pages):
                x = start_x + p * (btn_w + gap)
                bui.buttonwidget(
                    parent=self._pagination_widget,
                    position=(x, 16),
                    size=(btn_w, 28),
                    label=str(p + 1),
                    color=(_theme.get_color('COLOR_ACCENT') if p == self._current_page
                           else self._btn_color),
                    textcolor=self._text_color,
                    autoselect=True,
                    scale=0.81,
                    on_activate_call=bui.WeakCallStrict(self._show_page, p),
                )
        else:
            group = self._current_page // MAX_VISIBLE
            group_start = group * MAX_VISIBLE
            group_end = min(total_pages, group_start + MAX_VISIBLE)
            visible = group_end - group_start
            total_btn_w = nav_w + gap + visible * (btn_w + gap) + nav_w + gap
            start_x = max(0, (self._width - 20 - total_btn_w) / 2) + 8
            x = start_x

            # back button
            bui.buttonwidget(
                parent=self._pagination_widget,
                position=(x, 16), size=(nav_w, 28),
                label='<', color=self._btn_color, textcolor=self._text_color,
                autoselect=True, scale=0.85,
                on_activate_call=bui.WeakCallStrict(
                    self._show_page, max(0, group_start - MAX_VISIBLE)),
            )
            x += nav_w + gap

            for p in range(group_start, group_end):
                bui.buttonwidget(
                    parent=self._pagination_widget,
                    position=(x, 16), size=(btn_w, 28),
                    label=str(p + 1),
                    color=(_theme.get_color('COLOR_ACCENT') if p == self._current_page
                           else self._btn_color),
                    textcolor=self._text_color,
                    autoselect=True, scale=0.81,
                    on_activate_call=bui.WeakCallStrict(self._show_page, p),
                )
                x += btn_w + gap

            # next button
            bui.buttonwidget(
                parent=self._pagination_widget,
                position=(x, 16), size=(nav_w, 28),
                label='>',color=self._btn_color, textcolor=self._text_color,
                autoselect=True, scale=0.85,
                on_activate_call=bui.WeakCallStrict(
                    self._show_page, min(total_pages - 1, group_end)),
            )
            x += nav_w + gap

            # page indicator centered below buttons
            self._page_indicator = bui.textwidget(
                parent=self._root_widget,
                position=(self._width / 2, 3),
                size=(0, 0),
                text=f'({self._current_page + 1}/{total_pages})',
                scale=0.7,
                h_align='center',
                v_align='center',
                color=_theme.get_color('COLOR_SECONDARY'),
            )


_MSGS_PER_PAGE = 25


def _load_player_chat_messages(real_name: str) -> list[str]:
    """Return the list of chat messages for a player from chats.json."""
    import json as _json
    try:
        import os
        if not os.path.exists(CHATS_JSON_FILE):
            return []
        with open(CHATS_JSON_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            data: dict = _json.loads(content) if content else {}
        return list(data.get(real_name) or [])
    except Exception:
        return []


class PlayerInfoPopup(PopupWindow):
    """Shows detailed info for a player from playerinfo storage."""

    def __init__(self, real_name: str, on_close: Any = None) -> None:
        self.real_name = real_name
        self._data: dict[str, Any] = get_all_players().get(real_name, {})
        self._transitioning_out = False
        self._on_close = on_close

        self._messages: list[str] = _load_player_chat_messages(real_name)
        has_msgs = bool(self._messages)
        self._msgs_per_page = _MSGS_PER_PAGE
        self._total_msg_pages = max(1, (len(self._messages) + _MSGS_PER_PAGE - 1) // _MSGS_PER_PAGE)
        self._msg_page = 0

        if has_msgs:
            self._width = 950
            self._height = 625
            self._start_gap = 370.0
            self._spacing = 32.5
        else:
            self._width = 750
            self._height = 380
            self._start_gap = 75.0
            self._spacing = 35.0
        self._info_scale = 1.0

        bg_color = _theme.get_color('COLOR_BACKGROUND')
        self._btn_color = _theme.get_color('COLOR_BUTTON')
        self._text_color = _theme.get_color('COLOR_PRIMARY')

        uiscale = bui.app.ui_v1.uiscale
        if has_msgs:
            scale = (
                1.35 if uiscale is babase.UIScale.SMALL else
                1.4 if uiscale is babase.UIScale.MEDIUM else 1.0
            )
        else:
            scale = (
                1.5 if uiscale is babase.UIScale.SMALL else
                1.4 if uiscale is babase.UIScale.MEDIUM else 1.0
            )

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=scale,
            bg_color=bg_color,
        )

        # Title
        bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 25),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.5,
            color=bui.app.ui_v1.title_color,
            text=get_lang_text('RecentPlayers.infoTitle'),
        )

        # Back button
        bui.buttonwidget(
            parent=self.root_widget,
            position=(40, self._height - 58),
            size=(28, 38),
            label=babase.charstr(babase.SpecialChar.BACK),
            button_type='backSmall',
            color=self._btn_color,
            textcolor=self._text_color,
            enable_sound=False,
            on_activate_call=bui.WeakCallStrict(self._on_cancel_press),
        )

        # Mutual servers button
        mutual = self._data.get('mutual_server') or []
        if isinstance(mutual, str):
            mutual = [mutual]
        nav_anchor_x = self._width * 0.78 - 30
        nav_anchor_y = self._height * 0.025 + 35
        if mutual:
            bui.buttonwidget(
                parent=self.root_widget,
                position=(nav_anchor_x - 34, nav_anchor_y),
                size=(40, 40),
                label='',
                on_activate_call=bui.WeakCallStrict(self._show_mutual_servers),
                color=self._btn_color,
                autoselect=False,
                icon=bui.gettexture('achievementFreeLoader'),
                iconscale=1.2,
            )

        label_x = self._width * 0.1 - 45
        value_x = self._width * 0.38 - 45

        profiles: list[str] = self._data.get('profile_name') or []
        profile_str = ', '.join(profiles) if profiles else 'N/A'
        nickname_val = self._data.get('nickname') or ''
        client_id = str(self._data.get('client_id', 'N/A'))
        pb_id = str(self._data.get('pb_id') or 'N/A')
        ts = self._data.get('last_met_ts')
        last_met_str = _relative_time(ts) or 'N/A'

        rows = [
            (get_lang_text('RecentPlayers.labelName'), real_name, False),
            (get_lang_text('RecentPlayers.labelProfile'), profile_str, False),
            (get_lang_text('RecentPlayers.labelNickname'), nickname_val if nickname_val else 'N/A', True),
            (get_lang_text('RecentPlayers.labelClientId'), client_id, False),
            (get_lang_text('RecentPlayers.labelPbId'), pb_id, False),
            (get_lang_text('RecentPlayers.labelLastMet'), last_met_str, False),
        ]

        for idx, (label, value, editable) in enumerate(rows):
            pos_y = self._height - self._start_gap - self._spacing * (idx + 1)
            self._create_row(label, value, pos_y, label_x, value_x, editable)

        self._page_label: bui.Widget | None = None
        if has_msgs:
            self._scroll_widget: bui.Widget | None = None
            self._col_widget: bui.Widget | None = None
            if self._total_msg_pages > 1:
                nav_x = nav_anchor_x + 40 + 8
                bui.buttonwidget(
                    parent=self.root_widget,
                    position=(nav_x - 23, nav_anchor_y + 4),
                    size=(32, 32),
                    label='<',
                    color=self._btn_color,
                    textcolor=self._text_color,
                    autoselect=True,
                    on_activate_call=bui.WeakCallStrict(self._prev_msg_page),
                )
                bui.buttonwidget(
                    parent=self.root_widget,
                    position=(nav_x + 27, nav_anchor_y + 4),
                    size=(32, 32),
                    label='>',
                    color=self._btn_color,
                    textcolor=self._text_color,
                    autoselect=True,
                    on_activate_call=bui.WeakCallStrict(self._next_msg_page),
                )
                self._page_label = bui.textwidget(
                    parent=self.root_widget,
                    position=(nav_x + 70, nav_anchor_y + 20),
                    size=(0, 0),
                    h_align='left',
                    v_align='center',
                    scale=0.75,
                    color=self._text_color,
                    text=f'(1/{self._total_msg_pages})',
                )
            self._setup_msg_scroll()

    def _setup_msg_scroll(self, focus_last: bool = False) -> None:
        if self._scroll_widget and self._scroll_widget.exists():
            self._scroll_widget.delete()

        scroll_w = self._width - 70
        scroll_h = self._height - 300
        scroll_x = int((self._width - scroll_w) / 2)
        scroll_y = self._height - 64 - scroll_h
        self._scroll_widget = bui.scrollwidget(
            parent=self.root_widget,
            position=(scroll_x, scroll_y),
            size=(scroll_w, scroll_h),
            capture_arrows=True,
            color=_theme.get_color('COLOR_ACCENT'),
        )
        self._col_widget = bui.columnwidget(
            parent=self._scroll_widget,
            border=2,
            left_border=-130,
            margin=0,
        )

        start = self._msg_page * self._msgs_per_page
        page_msgs = self._messages[start:start + self._msgs_per_page]

        last_widget = None
        for entry in page_msgs:
            if ' >> ' in entry:
                profile, _, text = entry.partition(' >> ')
            else:
                profile, text = '', entry
            full_text = f'{profile}: {text}'
            w = bui.textwidget(
                parent=self._col_widget,
                position=(0, 0),
                size=(scroll_w + 40, 22),
                text=full_text,
                maxwidth=scroll_w * 0.97,
                scale=0.72,
                h_align='left',
                v_align='center',
                color=self._text_color,
                selectable=True,
                always_highlight=True,
                autoselect=False,
            )
            bui.textwidget(
                edit=w,
                on_select_call=bui.WeakCallStrict(
                    self._on_msg_press, full_text, text, w
                ),
            )
            last_widget = w

        if focus_last and last_widget and last_widget.exists():
            bui.containerwidget(
                edit=self._scroll_widget,
                visible_child=last_widget,
            )

        if self._page_label and self._page_label.exists():
            bui.textwidget(
                edit=self._page_label,
                text=f'({self._msg_page + 1}/{self._total_msg_pages})',
            )

    def _prev_msg_page(self) -> None:
        if self._msg_page > 0:
            self._msg_page -= 1
            self._setup_msg_scroll()

    def _next_msg_page(self) -> None:
        if self._msg_page < self._total_msg_pages - 1:
            self._msg_page += 1
            self._setup_msg_scroll()

    def _create_row(
        self,
        label: str,
        value: str,
        pos_y: float,
        label_x: float,
        value_x: float,
        editable: bool = False,
    ) -> None:
        bui.textwidget(
            parent=self.root_widget,
            position=(label_x, pos_y),
            size=(0, 0),
            scale=self._info_scale,
            h_align='left',
            v_align='center',
            text=label,
            color=_theme.get_color('COLOR_PRIMARY'),
        )
        if editable:
            self._nickname_widget = bui.textwidget(
                parent=self.root_widget,
                position=(value_x + 4, pos_y - 15),
                size=(150, 35),
                maxwidth=150,
                scale=self._info_scale,
                h_align='left',
                v_align='center',
                text=value if value != 'N/A' else '',
                selectable=True,
                editable=True,
                autoselect=True,
                max_chars=25,
                on_return_press_call=bui.WeakCallStrict(self._save_nickname),
                color=bui.app.ui_v1.title_color,
                description='nickname',
            )
            bui.buttonwidget(
                parent=self.root_widget,
                position=(value_x + 4 + 150 + 10, pos_y - 12),
                size=(75, 35),
                label='OK',
                scale=0.8,
                on_activate_call=bui.WeakCallStrict(self._save_nickname),
                color=self._btn_color,
                autoselect=False,
            )
        else:
            bui.textwidget(
                parent=self.root_widget,
                position=(value_x, pos_y),
                size=(0, 0),
                scale=self._info_scale,
                h_align='left',
                v_align='center',
                text=value,
                selectable=True,
                autoselect=False,
                click_activate=True,
                on_activate_call=lambda v=value: self._copy(v),
                color=bui.app.ui_v1.title_color,
            )

    def _save_nickname(self) -> None:
        text = bui.textwidget(query=self._nickname_widget)
        nickname = text.strip() if text else ''
        update_player(self.real_name, 'nickname', nickname)
        bui.screenmessage(
            get_lang_text('RecentPlayers.nicknameSaved'),
            color=(0, 1, 0),
        )
        bui.getsound('ding').play()
        bui.containerwidget(edit=self.root_widget, selected_child=None)
        pw = get_active_party_window()
        if pw is not None:
            pw.refresh_after_nickname_change()

    def _copy(self, value: str) -> None:
        if value and value != 'N/A':
            babase.clipboard_set_text(value)
            bui.screenmessage(
                get_lang_text('Global.copiedToClipboard'),
                color=(0, 1, 0),
            )

    def _show_mutual_servers(self) -> None:
        mutual = self._data.get('mutual_server') or []
        if isinstance(mutual, str):
            mutual = [mutual]
        bui.screenmessage(
            get_lang_text('RecentPlayers.servers') + ' ' + ', '.join(mutual),
        )

    def _on_msg_press(
        self, full_text: str, msg_only: str, widget: bui.Widget | None
    ) -> None:
        self._pressed_msg_full = full_text
        self._pressed_msg_only = msg_only
        self._pressed_msg_widget = widget

        pos = (
            widget.get_screen_space_center()
            if widget and widget.exists()
            else (400.0, 300.0)
        )
        uiscale = bui.app.ui_v1.uiscale
        scale = (
            2.0 if uiscale is babase.UIScale.SMALL else
            1.5 if uiscale is babase.UIScale.MEDIUM else 1.2
        )
        choices = ['msg_copy', 'msg_copy_text', 'msg_insert', 'msg_translate']
        choices_display = [
            babase.Lstr(value=get_lang_text('ChatPopup.copyText')),
            babase.Lstr(value=get_lang_text('ChatPopup.copyMessage')),
            babase.Lstr(value=get_lang_text('ChatPopup.insertText')),
            babase.Lstr(value=get_lang_text('ChatPopup.translateText')),
        ]
        bg = _theme.get_color('COLOR_BACKGROUND')
        txt = _theme.get_color('COLOR_PRIMARY')
        _ThemedPopupMenu(
            position=pos,
            scale=scale,
            choices=choices,
            choices_display=choices_display,
            current_choice=choices[0],
            delegate=self,
            bg_color=bg,
            text_color=txt,
        )

    def popup_menu_selected_choice(
        self, popup_window: Any, choice: str
    ) -> None:
        if choice == 'msg_copy':
            self._copy(self._pressed_msg_full)
        elif choice == 'msg_copy_text':
            self._copy(self._pressed_msg_only)
        elif choice == 'msg_insert':
            insert_into_chat_field(self._pressed_msg_full)
        elif choice == 'msg_translate':
            full = getattr(self, '_pressed_msg_full', '')
            only = self._pressed_msg_only
            prefix = full[: len(full) - len(only)] if only and full.endswith(only) else ''
            self._translate_message(
                only,
                getattr(self, '_pressed_msg_widget', None),
                prefix=prefix,
            )

    def popup_menu_closing(self, popup_window: Any) -> None:
        pass

    def _translate_message(self, text: str, widget: bui.Widget | None, prefix: str = '') -> None:
        import urllib.parse
        import urllib.request
        import json as _json
        from threading import Thread as _Thread

        text = text.strip()
        if not text or not any(c.isalpha() for c in text):
            bui.getsound('error').play()
            return

        src = finder_config.get(CFG_NAME_TRANSLATE_SOURCE_OTHER, 'auto')
        dst = finder_config.get(CFG_NAME_TRANSLATE_DESTINATION_OTHER, 'en')
        method = finder_config.get(CFG_NAME_TRANSLATE_PREFERRED_MACHINE, 'api')

        babase.screenmessage('Translating...', color=(0.6, 0.6, 1.0))

        def _apply(translated: str) -> None:
            if translated.lower() == text.lower():
                return
            if widget and widget.exists():
                bui.textwidget(edit=widget, text=prefix + translated)

        def _run() -> None:
            try:
                if method == 'link':
                    import re
                    params = urllib.parse.urlencode({'sl': src, 'tl': dst, 'text': text})
                    with urllib.request.urlopen(
                        f'https://translate.google.com/m?{params}', timeout=8
                    ) as resp:
                        match = re.search(
                            r'class="result-container">(.*?)<', resp.read().decode()
                        )
                        translated = match.group(1) if match else text
                else:
                    params = urllib.parse.urlencode({
                        'client': 'gtx', 'sl': src, 'tl': dst, 'dt': 't', 'q': text
                    })
                    url = f'https://translate.googleapis.com/translate_a/single?{params}'
                    with urllib.request.urlopen(url, timeout=8) as resp:
                        translated = _json.loads(resp.read().decode())[0][0][0]
                babase.pushcall(lambda: _apply(translated), from_other_thread=True)
            except Exception:
                babase.pushcall(
                    lambda: babase.screenmessage('Translation failed', color=(1.0, 0.3, 0.3)),
                    from_other_thread=True,
                )

        _Thread(target=_run, daemon=True).start()

    def _on_cancel_press(self) -> None:
        if self._transitioning_out:
            return
        self._transitioning_out = True
        bui.getsound('swish').play()
        if self.root_widget.exists():
            self.root_widget.delete()
        if self._on_close is not None:
            try:
                self._on_close()
            except Exception:
                pass

    def on_popup_cancel(self) -> None:
        self._on_cancel_press()



party.PartyWindow = LPartyWindow

# dev_console_add_text fails with RuntimeError if the dev console is not
# active (debug build only, happens when UI scale changes mid-refresh).
# Patch DevConsoleTab.text so the error doesn't propagate back to C++.
try:
    from babase._devconsole import DevConsoleTab
    _orig_dc_text = DevConsoleTab.text

    def _safe_dc_text(self, text, *args, **kwargs):
        try:
            return _orig_dc_text(self, text, *args, **kwargs)
        except RuntimeError:
            pass

    DevConsoleTab.text = _safe_dc_text
except Exception:
    pass


def _apply_saved_uiscale() -> None:
    saved = finder_config.get(CFG_NAME_UI_SCALE)
    if not saved:
        return
    import _babase
    from babase._mgen.enums import UIScale
    uiscale_map = {'0': UIScale.LARGE, '1': UIScale.MEDIUM, '2': UIScale.SMALL}
    scale = uiscale_map.get(str(saved))
    if scale is not None:
        _babase.app.set_ui_scale(scale)


babase.apptimer(0.5, _apply_saved_uiscale)

_orig_gather_window = None


def set_global_gather_modified(enabled: bool) -> None:
    """Replace or restore bauiv1lib.gather.GatherWindow globally."""
    global _orig_gather_window
    import bauiv1lib.gather as _gather_mod

    if enabled:
        if _orig_gather_window is None:
            _orig_gather_window = _gather_mod.GatherWindow
        _gather_mod.GatherWindow = GatherModified
    else:
        if _orig_gather_window is not None:
            _gather_mod.GatherWindow = _orig_gather_window
        GatherModified._unpatch_public_tab()


def _apply_global_gather() -> None:
    if finder_config.get(CFG_NAME_GLOBAL_GATHER, False):
        set_global_gather_modified(True)


babase.apptimer(0.6, _apply_global_gather)


def _setup_camera_auto_restore() -> None:
    try:
        import bascenev1 as bs
        import _babase

        _orig_on_begin = bs.Activity.on_begin

        def _patched_on_begin(self) -> None:
            _orig_on_begin(self)
            if not finder_config.get(CFG_NAME_CAMERA_AUTO_RESTORE, True):
                return
            if not isinstance(self, bs.GameActivity):
                return
            last = finder_config.get(CFG_NAME_CAMERA_LAST_USED)
            if not last:
                return

            def _restore() -> None:
                try:
                    _babase.set_camera_manual(True)
                    _babase.set_camera_position(*last['pos'])
                    _babase.set_camera_target(*last['target'])
                except Exception:
                    pass

            bs.timer(0.5, _restore)

        bs.Activity.on_begin = _patched_on_begin
    except Exception:
        pass


babase.apptimer(0.7, _setup_camera_auto_restore)


def _apply_saved_tint() -> None:
    apply_saved_tint()


babase.apptimer(0.8, _apply_saved_tint)

# ba_meta export babase.Plugin
class byLess(babase.Plugin):

    def on_app_running(self) -> None:
        pass