# ba_meta require api 9

from __future__ import annotations
import os
import time
import socket
from threading import Thread
from random import randint, uniform as uf
from json import load, loads, dump, JSONDecodeError, dumps
import babase
from babase import app, Plugin
import _babase
from bascenev1 import (
    connect_to_party as CON,
    protocol_version as PT,
    app as app
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
    apptime as apptime,
    apptimer as teck,
    AppTimer as tuck,
    getsound as gs,
    getmesh as gm,
    charstr as cs,
    Call,
    CallStrict,
    widget as ow,
    pushcall as pushcall,
    open_url as open_url,
    app as APP
)
from bauiv1lib.popup import PopupMenuWindow
from bauiv1lib import colorpicker
from typing import TYPE_CHECKING, Sequence, Optional, Dict, Any
import _bauiv1
import re

import urllib
import urllib.request
import urllib.error
import json
from threading import Thread

if TYPE_CHECKING:
    from typing import Dict, Optional, Any, Sequence

from babase._general import Call
import bauiv1lib.party as party
from bauiv1lib.confirm import ConfirmWindow
import bauiv1 as bui
import bascenev1 as bs

# I know you're looking at this code for a reason.
# Congrats, you found it — but yeah, I made it easy.
# Still, welcome.
BASE_URL = "https://www.bombsquadapi.lat"
V2_LOGO = "\ue063"
CREATOR = "\ue043Less"

# Constants and file paths
MY_DIRECTORY = _babase.env()['python_directory_user'] + "/LessFinder"
CONFIGS_FILE = os.path.join(MY_DIRECTORY, "configs.json")
FRIENDS_FILE = os.path.join(MY_DIRECTORY, "friends.json")

DEFAULT_LANGUAGES_DICT = {
    "es": {"name": "Español", "pc_compatible": True},
    "en": {"name": "English", "pc_compatible": True},
    "pt": {"name": "Português", "pc_compatible": True},
    "ru": {"name": "Русский", "pc_compatible": True},
    "hi": {"name": "हिन्दी", "pc_compatible": False},
    "ml": {"name": "മലയാളം", "pc_compatible": False},
    "id": {"name": "Bahasa Indonesia", "pc_compatible": False}
}

# Utility functions to get language names and IDs
def get_language_name(lang_id: str) -> str:
    """Get the display name for a language ID."""
    return DEFAULT_LANGUAGES_DICT.get(lang_id, {}).get("name", "English")

def get_language_names_dict() -> dict:
    """Get a simple dict of lang_id: name for compatibility with existing code."""
    return {lang_id: info["name"] for lang_id, info in DEFAULT_LANGUAGES_DICT.items()}

INVALID_KEY_TEXT = '[{0}]'
DEFAULT_AVAILABLE_LANG_LIST = [info["name"] for info in DEFAULT_LANGUAGES_DICT.values()]
DEFAULT_AVAILABLE_LANG_ID_LIST = list(DEFAULT_LANGUAGES_DICT.keys())
CFG_NAME_PREFFERED_LANG = 'Less Finder Language'
CFG_NAME_FILTER_ACCOUNT = 'Acounts Filter'
CFG_NAME_COLOR_BACKGROUND = 'COLOR BACKGROUND'
CFG_NAME_COLOR_SECONDARY = 'COLOR SECONDARY'
CFG_NAME_COLOR_TERTIARY = 'COLOR TERTIARY'
CFG_NAME_COLOR_PRIMARY = 'COLOR PRIMARY'
CFG_NAME_COLOR_ACCENT = 'COLOR ACCENT'
JSONS_DEFAULT_INDENT_FILE       = 1

COLOR_SCREENCMD_NORMAL  = (1.0, 0.65, 0.8)
COLOR_SCREENCMD_ERROR   = (1.0, 0.20, 0.0)

default_finder_config: Dict[str, Any] = {
    CFG_NAME_PREFFERED_LANG: '',
    CFG_NAME_FILTER_ACCOUNT: 'all',
    CFG_NAME_COLOR_BACKGROUND: (0.1, 0.1, 0.1),
    CFG_NAME_COLOR_SECONDARY: (0.2, 0.2, 0.2),
    CFG_NAME_COLOR_TERTIARY: (0.6, 0.6, 0.6),
    CFG_NAME_COLOR_PRIMARY: (1.0, 1.0, 1.0),
    CFG_NAME_COLOR_ACCENT: (1.0, 1.0, 1.0)
}

Translate_Texts: Dict[str, dict[str, str]] = {
    'Global.search': {
        'en': 'Search',
        'es': 'Buscar',
        'pt': 'Buscar',
        'ru': 'Поиск',
        'hi': 'खोजें',
        'ml': 'തിരയുക',
        'id': 'Cari'
    },
    'Global.delete': {
        'en': 'Delete',
        'es': 'Eliminar',
        'pt': 'Excluir',
        'ru': 'Удалить',
        'hi': 'हटाएं',
        'ml': 'ഇല്ലാതാക്കുക',
        'id': 'Hapus'
    },
    'Global.filter': {
        'en': 'Filter',
        'es': 'Filtrar',
        'pt': 'Filtrar',
        'ru': 'Фильтр',
        'hi': 'फ़िल्टर',
        'ml': 'ഫിൽട്ടർ',
        'id': 'Saring'
    },
    'Global.connect': {
        'en': 'Connect',
        'es': 'Conectar',
        'pt': 'Conectar',
        'ru': 'Подключить',
        'hi': 'कनेक्ट',
        'ml': 'കണക്റ്റ്',
        'id': 'Sambungkan'
    },
    'Global.online': {
        'en': 'Online',
        'es': 'En línea',
        'pt': 'Online',
        'ru': 'Онлайн',
        'hi': 'ऑनलाइन',
        'ml': 'ഓൺലൈൻ',
        'id': 'Online'
    },
    'Global.fieldEmpty': {
        'en': 'The field is empty, cannot add',
        'es': 'El campo está vacío, no se puede agregar',
        'pt': 'O campo está vazio, não é possível adicionar',
        'ru': 'Поле пустое, нельзя добавить',
        'hi': 'फ़ील्ड खाली है, जोड़ नहीं सकते',
        'ml': 'ഫീൽഡ് ശൂന്യമാണ്, ചേർക്കാൻ സാധിക്കില്ല',
        'id': 'Kolom kosong, tidak dapat menambahkan'
    },
    'Global.results': {
        'en': 'Results',
        'es': 'Resultados',
        'pt': 'Resultados',
        'ru': 'Результаты',
        'hi': 'परिणाम',
        'ml': 'ഫലങ്ങൾ',
        'id': 'Hasil'
    },
    'Global.credits': {
        'en': 'Credits',
        'es': 'Créditos',
        'pt': 'Créditos',
        'ru': 'Благодарности',
        'hi': 'श्रेय',
        'ml': 'ക്രെഡിറ്റുകൾ',
        'id': 'Kredit'
    },
    'Global.deletedSuccessfully': {
        'en': 'Deleted successfully',
        'es': 'Eliminado correctamente',
        'pt': 'Excluído com sucesso',
        'ru': 'Успешно удалено',
        'hi': 'सफलतापूर्वक हटाया गया',
        'ml': 'വിജയകരമായി നീക്കം ചെയ്തു',
        'id': 'Berhasil dihapus'
    },
    'Global.addedSuccessfully': {
        'en': 'Added successfully',
        'es': 'Agregado correctamente',
        'pt': 'Adicionado com sucesso',
        'ru': 'Успешно добавлено',
        'hi': 'सफलतापूर्वक जोड़ा गया',
        'ml': 'വിജയകരമായി ചേർത്തു',
        'id': 'Berhasil ditambahkan'
    },
    'Global.addedToFriendsList': {
        'en': 'Added to friends list!',
        'es': '¡Agregado a la lista de amigos!',
        'pt': 'Adicionado à lista de amigos!',
        'ru': 'Добавлено в список друзей!',
        'hi': 'दोस्तों की सूची में जोड़ा गया!',
        'ml': 'സുഹൃത്തുകളുടെ പട്ടികയിൽ ചേർത്തു!',
        'id': 'Ditambahkan ke daftar teman!'
    },
    'Global.alreadyInList': {
        'en': 'Already in list',
        'es': 'Ya está en la lista',
        'pt': 'Já está na lista',
        'ru': 'Уже в списке',
        'hi': 'पहले से सूची में है',
        'ml': 'ഇതിനകം പട്ടികയിൽ ഉണ്ട്',
        'id': 'Sudah ada dalam daftar'
    },
    'Global.alreadyInFriendsList': {
        'en': 'Already in friends list',
        'es': 'Ya está en la lista de amigos',
        'pt': 'Já está na lista de amigos',
        'ru': 'Уже в списке друзей',
        'hi': 'पहले से दोस्तों की सूची में है',
        'ml': 'ഇതിനകം സുഹൃത്തുകളുടെ പട്ടികയിൽ ഉണ്ട്',
        'id': 'Sudah ada dalam daftar teman'
    },
    'Global.copiedToClipboard': {
        'en': 'Copied to clipboard!',
        'es': '¡Copiado al portapapeles!',
        'pt': 'Copiado para a área de transferência!',
        'ru': 'Скопировано в буфер обмена!',
        'hi': 'क्लिपबोर्ड में कॉपी किया गया!',
        'ml': 'ക്ലിപ്പ്ബോർഡിലേക്ക് പകർത്തി!',
        'id': 'Disalin ke papan klip!'
    },
    'ProfileSearchWindow.profileSearch': {
        'en': 'Profile Search',
        'es': 'Búsqueda de Perfil',
        'pt': 'Busca de Perfil',
        'ru': 'Поиск профиля',
        'hi': 'प्रोफ़ाइल खोज',
        'ml': 'പ്രൊഫൈൽ തിരയൽ',
        'id': 'Pencarian Profil'
    },
    'ProfileSearchWindow.loadingProfileData': {
        'en': 'Loading profile data...',
        'es': 'Cargando datos del perfil...',
        'pt': 'Carregando dados do perfil...',
        'ru': 'Загрузка данных профиля...',
        'hi': 'प्रोफ़ाइल डेटा लोड हो रहा है...',
        'ml': 'പ്രൊഫൈൽ ഡാറ്റ ലോഡ് ചെയ്യുന്നു...',
        'id': 'Memuat data profil...'
    },
    'ProfileSearchWindow.name': {
        'en': 'Name',
        'es': 'Nombre',
        'pt': 'Nome',
        'ru': 'Имя',
        'hi': 'नाम',
        'ml': 'പേര്',
        'id': 'Nama'
    },
    'ProfileSearchWindow.character': {
        'en': 'Character',
        'es': 'Personaje',
        'pt': 'Personagem',
        'ru': 'Персонаж',
        'hi': 'चरित्र',
        'ml': 'കഥാപാത്രം',
        'id': 'Karakter'
    },
    'ProfileSearchWindow.accounts': {
        'en': 'Accounts',
        'es': 'Cuentas',
        'pt': 'Contas',
        'ru': 'Аккаунты',
        'hi': 'खाते',
        'ml': 'അക്കൗണ്ടുകൾ',
        'id': 'Akun'
    },
    'ProfileSearchWindow.rankInfo': {
        'en': 'Rank Info',
        'es': 'Información de Rango',
        'pt': 'Informações de Classificação',
        'ru': 'Информация о ранге',
        'hi': 'रैंक जानकारी',
        'ml': 'റാങ്ക് വിവരങ്ങൾ',
        'id': 'Info Peringkat'
    },
    'ProfileSearchWindow.current': {
        'en': 'Current',
        'es': 'Actual',
        'pt': 'Atual',
        'ru': 'Текущий',
        'hi': 'वर्तमान',
        'ml': 'നിലവിലെ',
        'id': 'Saat Ini'
    },
    'ProfileSearchWindow.previousRanks': {
        'en': 'Previous Ranks',
        'es': 'Rangos Anteriores',
        'pt': 'Classificações Anteriores',
        'ru': 'Предыдущие ранги',
        'hi': 'पिछले रैंक',
        'ml': 'മുൻ റാങ്കുകൾ',
        'id': 'Peringkat Sebelumnya'
    },
    'ProfileSearchWindow.season': {
        'en': 'Season',
        'es': 'Temporada',
        'pt': 'Temporada',
        'ru': 'Сезон',
        'hi': 'सीज़न',
        'ml': 'സീസൺ',
        'id': 'Musim'
    },
    'ProfileSearchWindow.achievements': {
        'en': 'Achievements',
        'es': 'Logros',
        'pt': 'Conquistas',
        'ru': 'Достижения',
        'hi': 'उपलब्धियाँ',
        'ml': 'നേട്ടങ്ങൾ',
        'id': 'Pencapaian'
    },
    'ProfileSearchWindow.trophies': {
        'en': 'Trophies',
        'es': 'Trofeos',
        'pt': 'Troféus',
        'ru': 'Трофеи',
        'hi': 'ट्रॉफी',
        'ml': 'ട്രോഫികൾ',
        'id': 'Trofi'
    },
    'ProfileSearchWindow.moreInfo': {
        'en': 'More Info',
        'es': 'Más Información',
        'pt': 'Mais Informações',
        'ru': 'Подробнее',
        'hi': 'अधिक जानकारी',
        'ml': 'കൂടുതൽ വിവരങ്ങൾ',
        'id': 'Info Lebih Lanjut'
    },
    'ProfileSearchWindow.accountType': {
        'en': 'Account Type',
        'es': 'Tipo de Cuenta',
        'pt': 'Tipo de Conta',
        'ru': 'Тип аккаунта',
        'hi': 'खाते का प्रकार',
        'ml': 'അക്കൗണ്ട് തരം',
        'id': 'Jenis Akun'
    },
    'ProfileSearchWindow.activeDays': {
        'en': 'Active Days',
        'es': 'Días Activos',
        'pt': 'Dias Ativos',
        'ru': 'Активные дни',
        'hi': 'सक्रिय दिन',
        'ml': 'സജീവ ദിവസങ്ങൾ',
        'id': 'Hari Aktif'
    },
    'ProfileSearchWindow.created': {
        'en': 'Created',
        'es': 'Creado',
        'pt': 'Criado',
        'ru': 'Создан',
        'hi': 'बनाया गया',
        'ml': 'സൃഷ്ടിച്ചത്',
        'id': 'Dibuat'
    },
    'ProfileSearchWindow.lastActive': {
        'en': 'Last Active',
        'es': 'Última Actividad',
        'pt': 'Última Atividade',
        'ru': 'Последняя активность',
        'hi': 'आखिरी बार सक्रिय',
        'ml': 'അവസാനമായി സജീവമായ',
        'id': 'Terakhir Aktif'
    },
    'ProfileSearchWindow.accountExistence': {
        'en': 'Account Existence',
        'es': 'Existencia de la Cuenta',
        'pt': 'Existência da Conta',
        'ru': 'Существование учетной записи',
        'hi': 'खाता अस्तित्व',
        'ml': 'അക്കൗണ്ട് നിലവിലുണ്ട്',
        'id': 'Keberadaan Akun'
    },
    'ProfileSearchWindow.Error.searchingAccount': {
        'en': 'Oops, an error occurred while searching for this account',
        'es': 'Ups, ocurrió un error al buscar esta cuenta',
        'pt': 'Ops, ocorreu um erro ao buscar esta conta',
        'ru': 'Упс, произошла ошибка при поиске этой учетной записи',
        'hi': 'ओह, इस खाते को खोजते समय एक त्रुटि हुई',
        'ml': 'അയ്യോ, ഈ അക്കൗണ്ട് തിരയുന്നതിനിടെ ഒരു പിശക് സംഭവിച്ചു',
        'id': 'Ups, terjadi kesalahan saat mencari akun ini'
    },
    'ProfileSearchWindow.Error.networkShort': {
        'en': 'Network error:',
        'es': 'Error de red:',
        'pt': 'Erro de rede:',
        'ru': 'Ошибка сети:',
        'hi': 'नेटवर्क त्रुटि:',
        'ml': 'നെറ്റ്‌വർക്ക് പിശക്:',
        'id': 'Kesalahan jaringan:'
    },
    'ProfileSearchWindow.Error.accountNotFound': {
        'en': 'Account not found',
        'es': 'Cuenta no encontrada',
        'pt': 'Conta não encontrada',
        'ru': 'Учетная запись не найдена',
        'hi': 'खाता नहीं मिला',
        'ml': 'അക്കൗണ്ട് കണ്ടെത്തിയില്ല',
        'id': 'Akun tidak ditemukan'
    },
    'ProfileSearchWindow.Error.noValidParameter': {
        'en': 'No valid parameter provided',
        'es': 'No se proporcionó un parámetro válido',
        'pt': 'Nenhum parâmetro válido fornecido',
        'ru': 'Не указан действительный параметр',
        'hi': 'कोई मान्य पैरामीटर प्रदान नहीं किया गया',
        'ml': 'സാധുവായ ഒരു പാരാമീറ്ററും നൽകിയിട്ടില്ല',
        'id': 'Tidak ada parameter valid yang diberikan'
    },
    'ProfileSearch.profileSearch': {
        'en': 'Profile Search',
        'es': 'Búsqueda de Perfil',
        'pt': 'Busca de Perfil',
        'ru': 'Поиск профиля',
        'hi': 'प्रोफ़ाइल खोज',
        'ml': 'പ്രൊഫൈൽ തിരയൽ',
        'id': 'Pencarian Profil'
    },
    'ProfileSearch.enterNameAndPressSearch': {
        'en': 'Enter a name and press Search',
        'es': 'Ingresa un nombre y presiona Buscar',
        'pt': 'Digite um nome e pressione Buscar',
        'ru': 'Введите имя и нажмите "Поиск"',
        'hi': 'एक नाम दर्ज करें और खोज दबाएँ',
        'ml': 'ഒരു പേര് നൽകുക, തിരയൽ അമർത്തുക',
        'id': 'Masukkan nama dan tekan Cari'
    },
    'ProfileSearch.searching': {
        'en': 'Searching...',
        'es': 'Buscando...',
        'pt': 'Buscando...',
        'ru': 'Поиск...',
        'hi': 'खोज रहा है...',
        'ml': 'തിരയുന്നു...',
        'id': 'Mencari...'
    },
    'ProfileSearch.Error.noAccountFound': {
        'en': 'No account found with Public ID:',
        'es': 'No se encontró ninguna cuenta con el ID público:',
        'pt': 'Nenhuma conta encontrada com ID Público:',
        'ru': 'Не найдена учетная запись с публичным ID:',
        'hi': 'इस सार्वजनिक आईडी के साथ कोई खाता नहीं मिला:',
        'ml': 'പബ്ലിക് ഐഡിയോടൊപ്പം യാതൊരു അക്കൗണ്ടും കണ്ടെത്തിയില്ല:',
        'id': 'Tidak ditemukan akun dengan ID Publik:'
    },
    'ProfileSearch.Error.network': {
        'en': 'Network error. Please check your connection and try again.',
        'es': 'Error de red. Por favor revisa tu conexión e inténtalo de nuevo.',
        'pt': 'Erro de rede. Por favor, verifique sua conexão e tente novamente.',
        'ru': 'Ошибка сети. Пожалуйста, проверьте подключение и попробуйте снова.',
        'hi': 'नेटवर्क त्रुटि। कृपया अपना कनेक्शन जांचें और पुनः प्रयास करें।',
        'ml': 'നെറ്റ്‌വർക്ക് പിശക്. ദയവായി നിങ്ങളുടെ കണക്ഷൻ പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Kesalahan jaringan. Silakan periksa koneksi Anda dan coba lagi.'
    },
    'ProfileSearch.Error.serviceUnavailable': {
        'en': 'Search service is currently unavailable. Please try again later.',
        'es': 'El servicio de búsqueda no está disponible actualmente. Por favor inténtalo más tarde.',
        'pt': 'O serviço de busca está indisponível no momento. Por favor, tente novamente mais tarde.',
        'ru': 'Служба поиска в настоящее время недоступна. Пожалуйста, попробуйте позже.',
        'hi': 'खोज सेवा वर्तमान में उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।',
        'ml': 'തിരച്ചിൽ സേവനം നിലവിൽ ലഭ്യമല്ല. ദയവായി പിന്നീട് വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Layanan pencarian saat ini tidak tersedia. Silakan coba lagi nanti.'
    },
    'ProfileSearch.Error.searchFailed': {
        'en': 'Oops, an error occurred while searching. Please try again.',
        'es': 'Ups, ocurrió un error al realizar la búsqueda. Por favor inténtalo de nuevo.',
        'pt': 'Ops, ocorreu um erro durante a busca. Por favor, tente novamente.',
        'ru': 'Упс, произошла ошибка при поиске. Пожалуйста, попробуйте снова.',
        'hi': 'ओह, खोज करते समय एक त्रुटि हुई। कृपया पुनः प्रयास करें।',
        'ml': 'അയ്യോ, തിരച്ചിൽ നടത്തുന്നതിനിടെ ഒരു പിശക് സംഭവിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Ups, terjadi kesalahan saat melakukan pencarian. Silakan coba lagi.'
    },
    'ProfileSearch.Error.invalidResponse': {
        'en': 'Invalid response from server. Please try again.',
        'es': 'Respuesta inválida del servidor. Por favor inténtalo de nuevo.',
        'pt': 'Resposta inválida do servidor. Por favor, tente novamente.',
        'ru': 'Неверный ответ от сервера. Пожалуйста, попробуйте снова.',
        'hi': 'सर्वर से अमान्य प्रतिक्रिया मिली। कृपया पुनः प्रयास करें।',
        'ml': 'സെർവറിൽ നിന്ന് അസാധുവായ പ്രതികരണം ലഭിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Respons tidak valid dari server. Silakan coba lagi.'
    },
    'ProfileSearch.Error.unexpected': {
        'en': 'Oops, an unexpected error occurred. Please try again.',
        'es': 'Ups, ocurrió un error inesperado. Por favor inténtalo de nuevo.',
        'pt': 'Ops, ocorreu um erro inesperado. Por favor, tente novamente.',
        'ru': 'Упс, произошла непредвиденная ошибка. Пожалуйста, попробуйте снова.',
        'hi': 'ओह, एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।',
        'ml': 'അയ്യോ, പ്രതീക്ഷിക്കാത്ത ഒരു പിശക് സംഭവിച്ചു. ദയവായി വീണ്ടും ശ്രമിക്കുക.',
        'id': 'Ups, terjadi kesalahan tak terduga. Silakan coba lagi.'
    },
    'ProfileSearch.Error.noExactMatch': {
        'en': 'No exact match found for',
        'es': 'No se encontró una coincidencia exacta para',
        'pt': 'Nenhuma correspondência exata encontrada para',
        'ru': 'Точное совпадение не найдено для',
        'hi': 'इसके लिए कोई सटीक मेल नहीं मिला',
        'ml': 'ഇതിനായി കൃത്യമായ പൊരുത്തം കണ്ടെത്തിയില്ല',
        'id': 'Tidak ditemukan kecocokan yang tepat untuk'
    },
    'ProfileSearch.Error.noAccountFoundWithId': {
        'en': 'No account found with ID:',
        'es': 'No se encontró ninguna cuenta con el ID:',
        'pt': 'Nenhuma conta encontrada com ID:',
        'ru': 'Не найдена учетная запись с ID:',
        'hi': 'इस आईडी के साथ कोई खाता नहीं मिला:',
        'ml': 'ഐഡിയോടൊപ്പം യാതൊരു അക്കൗണ്ടും കണ്ടെത്തിയില്ല:',
        'id': 'Tidak ditemukan akun dengan ID:'
    },
    'FriendsWindow.allFriends': {
        'en': 'All Your Friends',
        'es': 'Todos tus Amigos',
        'pt': 'Todos os Seus Amigos',
        'ru': 'Все ваши друзья',
        'hi': 'आपके सभी दोस्त',
        'ml': 'നിങ്ങളുടെ എല്ലാ സുഹൃത്തുക്കളും',
        'id': 'Semua Teman Anda'
    },
    'FriendsWindow.addManually': {
        'en': 'Add\nManually',
        'es': 'Agregar\nManualmente',
        'pt': 'Adicionar\nManualmente',
        'ru': 'Добавить\nВручную',
        'hi': 'मैन्युअली\nजोड़ें',
        'ml': 'മാനുവൽ\nചേർക്കുക',
        'id': 'Tambah\nManual'
    },
    'FriendsWindow.selectFriendToView': {
        'en': 'Select a friend\nto see where they are',
        'es': 'Selecciona un amigo\npara ver donde está',
        'pt': 'Selecione um amigo\npara ver onde ele está',
        'ru': 'Выберите друга,\nчтобы увидеть его местоположение',
        'hi': 'किसी दोस्त को चुनें\nयह देखने के लिए कि वह कहाँ है',
        'ml': 'ഒരു സുഹൃത്തിനെ തിരഞ്ഞെടുക്കുക\nഅവൻ എവിടെയെന്ന് കാണാൻ',
        'id': 'Pilih seorang teman\nuntuk melihat di mana ia berada'
    },
    'FriendsWindow.noFriendsOnline': {
        'en': 'Uh, it seems\nthere are no friends\nonline, try\nsearching servers',
        'es': 'Uh, parece que\nno hay amigos\nen línea, prueba\nbuscando servidores',
        'pt': 'Uh, parece que\nnão há amigos\nonline, tente\nbuscar servidores',
        'ru': 'Кажется, что\nнет друзей\nв сети, попробуйте\nпоискать серверы',
        'hi': 'अरे, लगता है कि\nकोई दोस्त ऑनलाइन\nनहीं है, सर्वर\nखोजकर देखें',
        'ml': 'ഉഫ്, ഓൺലൈൻ\nസുഹൃത്തുക്കൾ ഇല്ലെന്ന്\nതോന്നുന്നു, സർവർ\nതിരഞ്ഞ് നോക്കൂ',
        'id': 'Uh, sepertinya\nbelum ada teman\nyang online,\ncoba cari server'
    },
    'FriendsWindow.viewProfile': {
        'en': 'View Profile',
        'es': 'Ver Perfil',
        'pt': 'Ver Perfil',
        'ru': 'Просмотреть профиль',
        'hi': 'प्रोफ़ाइल देखें',
        'ml': 'പ്രൊഫൈൽ കാണുക',
        'id': 'Lihat Profil'
    },
    'FriendsWindow.deleteFriend': {
        'en': 'Delete Friend',
        'es': 'Eliminar Amigo',
        'pt': 'Excluir Amigo',
        'ru': 'Удалить друга',
        'hi': 'दोस्त\nहटाएँ',
        'ml': 'സുഹൃത്ത് ഇല്ലാതാക്കുക',
        'id': 'Hapus Teman'
    },
    'FriendsWindow.addFriend': {
        'en': 'Add\nTo Friends',
        'es': 'Agregar\nAmigo',
        'pt': 'Adicionar\nAmigo',
        'ru': 'Добавить\nв друзья',
        'hi': 'दोस्त\nजोड़ें',
        'ml': 'സുഹൃത്ത്\nചേർക്കുക',
        'id': 'Tambah\nTeman'
    },
    'FinderWindow.searchServers': {
        'en': 'Search All Servers',
        'es': 'Buscar todos los servidores',
        'pt': 'Buscar Todos os Servidores',
        'ru': 'Искать все серверы',
        'hi': 'सभी सर्वर खोजें',
        'ml': 'എല്ലാ സര്‍വറുകളും അന്വേഷിക്കുക',
        'id': 'Cari Semua Server'
    },
    'FinderWindow.searchPlayers': {
        'en': 'Search players without having to join a match',
        'es': 'Busca jugadores sin tener que unirse a partida',
        'pt': 'Busque jogadores sem precisar entrar em uma partida',
        'ru': 'Искать игроков без необходимости присоединяться к матчу',
        'hi': 'खिलाड़‍ियों को खोजें बिना मैच में जुड़ने की ज़रूरत',
        'ml': 'മത്സരത്തിൽ ചേരേണ്ടതില്ലാതെ കളിക്കാരെ തിരയുക',
        'id': 'Cari pemain tanpa harus bergabung ke pertandingan'
    },
    'FinderWindow.pressSearch': {
        'en': 'Press search and\nI\'ll handle the rest!',
        'es': '¡Pulsa buscar y yo me\nencargo del resto!',
        'pt': 'Pressione buscar e\nEu cuido do resto!',
        'ru': 'Нажмите поиск, и\nя позабочусь об остальном!',
        'hi': 'सर्च दबाएँ और\nबाकी मैं संभाल लूँगा!',
        'ml': 'സെർച്ച് അമർത്തൂ,\nമറ്റെല്ലാം ഞാൻ നോക്കാം!',
        'id': 'Tekan cari dan\nbiar aku urus sisanya!'
    },
    'FinderWindow.filterDescription': {
        'en': 'Filter by player/server names or by specific characters',
        'es': 'Filtra por el nombre de los jugadores/servidores o por caracteres específicos',
        'pt': 'Filtre por nomes de jogadores/servidores ou por caracteres específicos',
        'ru': 'Фильтруйте по именам игроков/серверов или по определённым символам',
        'hi': 'खिलाड़ियों/सर्वरों के नाम या विशिष्ट अक्षरों के अनुसार फ़िल्टर करें',
        'ml': 'കളിക്കാരുടെ/സെർവറുകളുടെ പേരുകളോ പ്രത്യേക അക്ഷരങ്ങളോ അടിസ്ഥാനമാക്കി ഫിൽട്ടർ ചെയ്യുക',
        'id': 'Saring berdasarkan nama pemain/server atau karakter tertentu'
    },
    'FinderWindow.searchServersForPlayers': {
        'en': 'Search some servers\nto find players\nresults may vary\nby time and connection',
        'es': 'Busca en algunos servidores\npara encontrar jugadores\nLos resultados pueden variar\nsegún la hora y la conexión',
        'pt': 'Pesquise alguns servidores\npara encontrar jogadores\nos resultados podem variar\npor horário e conexão',
        'ru': 'Ищите на некоторых серверах,\nчтобы найти игроков\nрезультаты могут различаться\nв зависимости от времени и подключения',
        'hi': 'कुछ सर्वरों में खोजें\nखिलाड़ी खोजने के लिए\nपरिणाम बदल सकते हैं\nसमय और कनेक्शन के अनुसार',
        'ml': 'ചില സര്‍വറുകളില്‍ തിരയുക\nകളിക്കാരെ കണ്ടെത്താൻ\nഫലങ്ങൾ മാറാം\nസമയം മറ്റും കണക്ഷൻ അനുസരിച്ച്',
        'id': 'Cari di beberapa server\nuntuk menemukan pemain\nhasil dapat berbeda\nsesuai waktu dan koneksi'
    },
    'FinderWindow.selectToViewInfo': {
        'en': 'Select something to\nview server info',
        'es': 'Selecciona algo para\nver la info del servidor',
        'pt': 'Selecione algo para\nver informações do servidor',
        'ru': 'Выберите что-нибудь,\nчтобы просмотреть информацию о сервере',
        'hi': 'कुछ चुनें ताकि आप\nसर्वर की जानकारी देखें',
        'ml': 'ഏതെങ്കിലും തിരഞ്ഞെടുക്കുക\nസർവർ വിവരങ്ങൾ കാണാൻ',
        'id': 'Pilih sesuatu untuk\nmelihat info server'
    },
    'FinderWindow.scanningServers': {
        'en': 'Scanning servers!\nThis should take a few seconds.\nYou can close this window.',
        'es': '¡Escaneando servidores!\nEsto debería tardar unos segundos.\nPuedes cerrar esta ventana.',
        'pt': 'Escaneando servidores!\nIsso deve levar alguns segundos.\nVocê pode fechar esta janela.',
        'ru': 'Сканирование серверов!\nЭто займет несколько секунд.\nВы можете закрыть это окно.',
        'hi': 'सर्वर स्कैन हो रहे हैं!\nइसमें कुछ सेकंड लगेंगे।\nआप यह विंडो बंद कर सकते हैं।',
        'ml': 'സര്‍വറുകൾ സ്കാന്‍ ചെയ്യുന്നു!\nഇതിന് കുറച്ച് സെക്കൻഡ് മാത്രം എടുക്കും.\nഈ ജാലകം നിങ്ങൾക്ക് അടയ്ക്കാം.',
        'id': 'Sedang memindai server!\nIni seharusnya hanya\nmembutuhkan beberapa detik.\nAnda bisa menutup jendela ini.'
    },
    'FinderWindow.stillBusy': {
        'en': '¡Still busy!',
        'es': '¡Sigo ocupado!',
        'pt': 'Ainda ocupado!',
        'ru': 'Все еще занят!',
        'hi': 'मैं अभी भी व्यस्त हूँ!',
        'ml': 'ഞാൻ ഇതുവരെ തിരക്കിലാണ്!',
        'id': 'Masih sibuk!'
    },
    'FinderWindow.searchProfiles': {
        'en': 'Search Profiles',
        'es': 'Buscar Perfiles',
        'pt': 'Buscar Perfis',
        'ru': 'Поиск профилей',
        'hi': 'प्रोफ़ाइल खोजें',
        'ml': 'പ്രൊഫൈലുകൾ തിരയുക',
        'id': 'Cari Profil'
    },
    'FinderWindow.changeColors': {
        'en': 'Change Colors',
        'es': 'Cambiar colores',
        'pt': 'Mudar Cores',
        'ru': 'Изменить цвета',
        'hi': 'रंग बदलें',
        'ml': 'നിറങ്ങൾ മാറ്റുക',
        'id': 'Ubah Warna'
    },
    'FinderWindow.changeLanguage': {
        'en': 'Change Language',
        'es': 'Cambiar idioma',
        'pt': 'Mudar Idioma',
        'ru': 'Изменить язык',
        'hi': 'भाषा बदलें',
        'ml': 'ഭാഷ മാറ്റുക',
        'id': 'Ubah Bahasa'
    },
    'Scan.finished': {
        'en': 'Finished!',
        'es': '¡Terminado!',
        'pt': 'Terminado!',
        'ru': 'Завершено!',
        'hi': 'समाप्त!',
        'ml': 'പൂർത്തിയായി!',
        'id': 'Selesai!'
    },
    'Scan.scanned': {
        'en': 'Scanned',
        'es': 'Escaneados',
        'pt': 'Escaneado',
        'ru': 'Отсканировано',
        'hi': 'स्कैन किए',
        'ml': 'സ്കാൻ ചെയ്തു',
        'id': 'Dipindai'
    },
    'Scan.servers': {
        'en': 'servers',
        'es': 'servidores',
        'po': 'servidores',
        'ru': 'серверы',
        'hi': 'सर्वर',
        'ml': 'സർവർ',
        'id': 'server'
    },
    'Scan.in': {
        'en': 'in',
        'es': 'en',
        'po': 'em',
        'ru': 'в',
        'hi': 'में',
        'ml': 'ഇൽ',
        'id': 'dalam'
    },
    'Scan.seconds': {
        'en': 'seconds!',
        'es': 'segundos!',
        'po': 'segundos!',
        'ru': 'секунд!',
        'hi': 'सेकंड!',
        'ml': 'സെക്കൻഡുകൾ!',
        'id': 'detik!'
    },
    'Scan.approximately': {
        'en': 'Approximately',
        'es': 'Aproximadamente',
        'po': 'Aproximadamente',
        'ru': 'Приблизительно',
        'hi': 'लगभग',
        'ml': 'ഏകദേശം',
        'id': 'Sekitar'
    },
    'Scan.server': {
        'en': 'servers',
        'es': 'servidores',
        'po': 'servidores',
        'ru': 'серверы',
        'hi': 'सर्वर',
        'ml': 'സർവർ',
        'id': 'servers'
    },
    'Scan.perSecond': {
        'en': '/sec',
        'es': '/seg',
        'po': '/seg',
        'ru': '/сек',
        'hi': '/सेक',
        'ml': '/സെക്',
        'id': '/detik'
    },
    'PartyWindow.addFriend': {
        'en': 'Add friend',
        'es': 'Agregar amigo',
        'po': 'Adicionar amigo',
        'ru': 'Добавить друга',
        'hi': 'दोस्त जोड़ें',
        'ml': 'സുഹൃത്ത് ചേർക്കുക',
        'id': 'Tambah teman'
    },
    'PartyWindow.areYouSureToKick': {
        'en': 'Are you sure to kick',
        'es': '¿Estás seguro de expulsar?',
        'po': 'Tem certeza de que quer expulsar',
        'ru': 'Вы уверены, что хотите кикнуть',
        'hi': 'क्या आप वाकई निकालना चाहते हैं',
        'ml': 'നിങ്ങൾ പുറത്താക്കാൻ ഉറപ്പാണോ',
        'id': 'Apakah Anda yakin untuk mengeluarkan'
    },
    'PartyWindow.voteToKick': {
        'en': 'Vote to kick',
        'es': 'Votar para expulsar',
        'po': 'Votar para expulsar',
        'ru': 'Голосовать за кик',
        'hi': 'निकालने के लिए मतदान',
        'ml': 'പുറത്താക്കാൻ വോട്ട് ചെയ്യുക',
        'id': 'Pemungutan suara untuk mengeluarkan'
    },
    'PartyWindow.viewAccount': {
        'en': 'View account',
        'es': 'Ver cuenta',
        'po': 'Ver conta',
        'ru': 'Просмотреть аккаунт',
        'hi': 'खाता देखें',
        'ml': 'അക്കൗണ്ട് കാണുക',
        'id': 'Lihat akun'
    },
    'CreditsWindow.developer': {
        'en': 'Developer',
        'es': 'Desarrollador',
        'po': 'Desenvolvedor',
        'ru': 'Разработчик',
        'hi': 'डेवलपर',
        'ml': 'ഡെവലപ്പർ',
        'id': 'Pengembang'
    },
    'CreditsWindow.motivation': {
        'en': 'Motivation',
        'es': 'Motivación',
        'po': 'Motivação',
        'ru': 'Мотивация',
        'hi': 'प्रेरणा',
        'ml': 'പ്രേരണം',
        'id': 'Motivasi'
    },
    'CreditsWindow.motivationDescription': {
        'en': 'My motivation to create this was trying to make a friends system so you can easily find your friends and play some parties, also to see a player’s level by viewing their profile and time spent playing BombSquad',
        'es': 'Mi motivación para crear esto fue intentar hacer un sistema de amigos para poder encontrar fácilmente a tus amigos y jugar algunas fiestas, también mirar el nivel de un jugador viendo su perfil y tiempo jugando BombSquad',
        'po': 'Minha motivação para criar isso foi tentar fazer um sistema de amigos para que você possa encontrar facilmente seus amigos e jogar algumas festas, também para ver o nível de um jogador visualizando seu perfil e tempo gasto jogando BombSquad',
        'ru': 'Моей мотивацией для создания этого была попытка сделать систему друзей, чтобы вы могли легко находить своих друзей и играть в некоторые вечеринки, а также видеть уровень игрока, просматривая его профиль и время, проведенное за игрой в BombSquad',
        'hi': 'इसे बनाने की मेरी प्रेरणा एक मित्र प्रणाली बनाने की कोशिश थी ताकि आप अपने दोस्तों को आसानी से ढूंढ सकें और कुछ पार्टियाँ खेल सकें, साथ ही उनके प्रोफ़ाइल और BombSquad खेलने में बिताए गए समय को देखकर किसी खिलाड़ी का स्तर भी देख सकें',
        'ml': 'ഇത് സൃഷ്ടിക്കാൻ എനിക്ക് പ്രചോദനമായത് നിങ്ങളുടെ സുഹൃത്തുകളെ എളുപ്പത്തിൽ കണ്ടെത്താനും ചില പാർട്ടികൾ കളിക്കാനും കഴിയുന്ന ഒരു സുഹൃത്ത് സംവിധാനം ഉണ്ടാക്കുക, കൂടാതെ അവരുടെ പ്രൊഫൈലും BombSquad കളിച്ച സമയവും देखकर ഒരു കളിക്കാരന്റെ ലെവൽ കാണുക എന്നതുമായിരുന്നു',
        'id': 'Motivasi saya untuk membuat ini adalah mencoba membuat sistem teman agar dapat dengan mudah menemukan teman Anda dan bermain beberapa pesta, juga melihat level seorang pemain dengan melihat profil mereka dan waktu bermain BombSquad'
    },
    'CreditsWindow.inspiration': {
        'en': 'Inspiration',
        'es': 'Inspiración',
        'po': 'Inspiração',
        'ru': 'Вдохновение',
        'hi': 'प्रेरणा',
        'ml': 'പ്രചോദനം',
        'id': 'Inspirasi'
    },
    'CreditsWindow.inspirationDescription': {
        'en': 'This is my first official mod, I took inspiration from features of some mods I saw within the community, I hope they do not mind, in the same way I will list them below',
        'es': 'Este es mi primer mod oficial, tomé como inspiración funcionalidades de algunos mods que vi dentro de la comunidad, espero no se molesten, de igual forma los pondré aquí abajo',
        'po': 'Este é meu primeiro mod oficial, me inspirei em recursos de alguns mods que vi na comunidade, espero que não se importem, da mesma forma os listarei abaixo',
        'ru': 'Это мой первый официальный мод, я черпал вдохновение из функций некоторых модов, которые я видел в сообществе, надеюсь, они не против, точно так же я перечислю их ниже',
        'hi': 'यह मेरा पहला आधिकारिक मॉड है, मैंने समुदाय के भीतर देखे गए कुछ मॉड्स की विशेषताओं से प्रेरणा ली है, आशा है कि उन्हें आपत्ति नहीं होगी, इसी तरह मैं उन्हें नीचे सूचीबद्ध करूँगा',
        'ml': 'ഇത് എന്റെ ആദ്യ ഔദ്യോഗിക മോഡാണ്, കമ്മ്യൂണിറ്റിക്കുള്ളിൽ ഞാൻ കണ്ട ചില മോഡുകളുടെ സവിശേഷതകളിൽ നിന്ന് ഞാൻ പ്രചോദനം നേടി, അവർക്ക് അതിൽ പ്രശ്നമില്ലെന്ന് ഞാൻ പ്രതീക്ഷിക്കുന്നു, അതുപോലെ അവയെ ഞാൻ താഴെ ചേർക്കും',
        'id': 'Ini adalah mod resmi pertama saya, saya mengambil inspirasi dari fitur beberapa mod yang saya lihat di dalam komunitas, saya harap mereka tidak keberatan, dengan cara yang sama saya akan mencantumkannya di bawah'
    },
    'CreditsWindow.thanksMessage': {
        'en': f'Thank you {V2_LOGO}VanyOne for trying this and making the preview video, and to the people who helped with their opinions and support. I may add new features in the future. I know it is not perfect and that there are several bugs, but that is all for now. I will gradually fix the existing issues. I hope you enjoy it, with love - {CREATOR}',      
        'es': f'Gracias {V2_LOGO}VanyOne por probar esto y hacer el video preview, y a las personas que ayudaron con sus opiniones y apoyo. Puede que añada nuevas funcionalidades en un futuro. Sé que no es perfecto y que hay varios errores, pero es todo por el momento. Igual solucionaré gradualmente los errores que existen. Espero lo disfruten, con cariño - {CREATOR}',     
        'po': f'Obrigado {V2_LOGO}VanyOne por testar isso e fazer o vídeo de prévia, e às pessoas que ajudaram com suas opiniões e apoio. Posso adicionar novas funcionalidades no futuro. Sei que não é perfeito e que há vários erros, mas por enquanto é só isso. Também corrigirei gradualmente os erros existentes. Espero que você goste, com carinho - {CREATOR}',       
        'ru': f'Спасибо {V2_LOGO}VanyOne за то, что попробовали это и сделали видео-превью, а также людям, которые помогли своими мнениями и поддержкой. Возможно, я добавлю новые функции в будущем. Я знаю, что это не идеально и что есть несколько ошибок, но на данный момент это всё. Я буду постепенно исправлять существующие ошибки. Надеюсь, вам понравится, с любовью - {CREATOR}',      
        'hi': f'{V2_LOGO}VanyOne को इसे आज़माने और प्रीव्यू वीडियो बनाने के लिए धन्यवाद, साथ ही उन लोगों को भी जिन्होंने अपनी राय और समर्थन से मदद की। मैं भविष्य में नई सुविधाएँ जोड़ सकता हूँ। मुझे पता है कि यह परफेक्ट नहीं है और इसमें कई त्रुटियाँ हैं, लेकिन फिलहाल इतना ही है। मैं मौजूदा समस्याओं को धीरे-धीरे ठीक करता रहूँगा। आशा है कि आप इसका आनंद लेंगे, स्नेह सहित - {CREATOR}',      
        'ml': f'{V2_LOGO}VanyOne ഇത് പരീക്ഷിക്കുകയും പ്രിവ്യൂ വീഡിയോ തയ്യാറാക്കുകയും ചെയ്തതിന് നന്ദി, അവരുടെ അഭിപ്രായങ്ങളും പിന്തുണയും നൽകിയ എല്ലാവർക്കും നന്ദി. ഭാവിയിൽ ഞാൻ പുതിയ ഫീച്ചറുകൾ ചേർക്കാൻ സാധ്യതയുണ്ട്. ഇത് പൂർണ്ണമായതല്ലെന്നും പല പിശകുകളും ഉണ്ടെന്നും എനിക്ക് അറിയാം, പക്ഷേ ഇപ്പോൾ ഇത്രയേ ഉള്ളൂ. നിലവിലുള്ള പ്രശ്നങ്ങൾ ഞാൻ ക്രമേണ പരിഹരിക്കും. നിങ്ങൾ ഇത് ആസ്വദിക്കുമെന്ന് ഞാൻ പ്രതീക്ഷിക്കുന്നു, സ്നേഹത്തോടെ - {CREATOR}',        
        'id': f'Terima kasih {V2_LOGO}VanyOne telah mencoba ini dan membuat video pratinjau, serta kepada orang-orang yang membantu dengan pendapat dan dukungan mereka. Saya mungkin akan menambahkan fitur baru di masa depan. Saya tahu ini belum sempurna dan masih ada beberapa kesalahan, tetapi untuk saat ini hanya itu. Saya akan memperbaiki masalah yang ada secara bertahap. Semoga kalian menikmatinya, dengan penuh kasih - {CREATOR}'
    }
}

####### FINDER MAIN SETTINGS #######
finder_config: Dict[str, Any] = {}
"""Global Less Finder Settings,

Usages: `finder_config.get(config_key)` OR `finder_config[config_key]`"""

def load_finder_config(is_from_backup: bool=False, read_only: bool=False) -> Dict[str, Any]:
    """Load the party configuration from the file if it exists, else create it with default values"""
    global finder_config
    try:
        if os.path.exists(CONFIGS_FILE):
            # Load the config from the file
            updated = False
            with open(CONFIGS_FILE, 'r') as file:
                finder_config = load(file)

            # Validate config
            if not read_only:
                keys_to_remove = []
                for key in finder_config:
                    if key not in default_finder_config:
                        keys_to_remove.append(key)

                for key in keys_to_remove:
                    TIP(f"{get_lang_text('partyConfigLoadRemoveKey')}: {key}", color=COLOR_SCREENCMD_ERROR)
                    del finder_config[key]
                    if not updated: updated = True

                # Ensure all default configs are present, if not, add them
                for default_key, default_value in default_finder_config.items():
                    if default_key not in finder_config:
                        TIP(f"{get_lang_text('partyConfigLoadAddKey')}: {default_key}", color=COLOR_SCREENCMD_NORMAL)
                        finder_config[default_key] = default_value
                        if not updated: updated = True

                if updated:
                    save_finder_config(finder_config)
                # Save the updated configuration with valid keys
            return finder_config
        else:
            # If the file doesn't exist, create it with default values
            if not os.path.exists(MY_DIRECTORY):
                os.makedirs(MY_DIRECTORY)
            save_finder_config(default_finder_config, first_boot=True)
            finder_config = default_finder_config
            return default_finder_config
    except Exception as e:
        TIP(f"Error loading config: {e}", color=COLOR_SCREENCMD_ERROR)
        print(e)
        try:
            if os.path.exists(CONFIGS_FILE):
                if os.path.isfile(CONFIGS_FILE):
                    os.remove(CONFIGS_FILE)
                    if not is_from_backup: load_finder_config(is_from_backup=True)
        except Exception as e: print(e)
    finder_config = default_finder_config
    return default_finder_config

def save_finder_config(config: dict[str, Any], first_boot: bool = False, force:bool=False):
    """Save the current PartyWindow configuration to a file"""
    global finder_config
    try:
        if (not force and (not first_boot and load_finder_config(read_only=True) == config)) or not config:
            return
        with open(CONFIGS_FILE, 'w', encoding='utf-8') as file:
            dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
            finder_config = config
    except FileNotFoundError:
        with open(CONFIGS_FILE, 'w', encoding='utf-8') as file:
            dump(config, file, indent=JSONS_DEFAULT_INDENT_FILE)
    except Exception as e:
        print(e)

def update_finder_config(key: str, value: Any):
    """Update a specific key in the configuration file"""
    global finder_config
    if not finder_config: load_finder_config()
    if finder_config and key in finder_config:
        finder_config[key] = value
        save_finder_config(finder_config)
        load_finder_config()

### FRIENDS STORAGE ####
friends_list: list[dict[str, Any]] = []
"""
    Friends list storage.

    Each friend dict contains:
    {
      "name": str,
      "id": str,
      "accounts": list[str] | None,
      "account_pb": str | None,
      "account_id": str | None
    }
"""

def load_friends(is_from_backup: bool = False) -> list[dict[str, Any]]:
    """Load the friends list from disk, or create an empty one."""
    global friends_list
    try:
        if os.path.exists(FRIENDS_FILE):
            with open(FRIENDS_FILE, "r", encoding="utf-8") as file:
                friends_list = load(file)

            changed = False
            for friend in friends_list:
                if "name" not in friend or "id" not in friend:
                    friends_list.remove(friend)
                    changed = True
                    continue

                # Ensure all fields exist
                for key in ("accounts", "account_pb", "account_id"):
                    if key not in friend:
                        friend[key] = None
                        changed = True

            if changed:
                save_friends(friends_list)

            return friends_list

        # If file does not exist
        if not os.path.exists(MY_DIRECTORY):
            os.makedirs(MY_DIRECTORY)

        friends_list = []
        save_friends(friends_list, first_boot=True)
        return friends_list

    except Exception as e:
        TIP(f"Error loading friends: {e}", color=COLOR_SCREENCMD_ERROR)
        print(e)

        try:
            if os.path.exists(FRIENDS_FILE):
                os.remove(FRIENDS_FILE)
                if not is_from_backup:
                    return load_friends(is_from_backup=True)
        except Exception as e:
            print(e)

    friends_list = []
    return friends_list

def save_friends(data: list[dict[str, Any]],
                 first_boot: bool = False,
                 force: bool = False):
    """Persist the friends list to disk."""
    global friends_list
    try:
        if not force and not first_boot and load_friends() == data:
            return

        with open(FRIENDS_FILE, "w", encoding="utf-8") as file:
            dump(data, file, indent=JSONS_DEFAULT_INDENT_FILE)
            friends_list = data

    except Exception as e:
        print(e)

# -----------------------------------------------------
# CRUD FUNCTIONS
# -----------------------------------------------------
def add_friend(name: str, friend_id: str,
               accounts: list[str] | None = None,
               account_pb: str | None = None,
               account_id: str | None = None):
    """Add a new friend."""
    load_friends()

    # Prevent duplicates by id
    for f in friends_list:
        if f["id"] == friend_id:
            TIP("Friend ID already exists.", color=COLOR_SCREENCMD_ERROR)
            return

    new_friend = {
        "name": name,
        "id": friend_id,
        "accounts": accounts or [],
        "account_pb": account_pb,
        "account_id": account_id
    }

    friends_list.append(new_friend)
    save_friends(friends_list)


def remove_friend(friend_id: str):
    """Delete a friend by ID."""
    load_friends()

    friends_list[:] = [f for f in friends_list if f["id"] != friend_id]
    save_friends(friends_list)


def update_friend(friend_id: str, key: str, value: Any):
    """Update a single field for a friend."""
    load_friends()

    for f in friends_list:
        if f["id"] == friend_id:
            f[key] = value
            save_friends(friends_list)
            return


def add_account(friend_id: str, account_name: str):
    """Add an account name to a friend."""
    load_friends()

    for f in friends_list:
        if f["id"] == friend_id:
            if f["accounts"] is None:
                f["accounts"] = []

            if account_name not in f["accounts"]:
                f["accounts"].append(account_name)

            save_friends(friends_list)
            return


def remove_account(friend_id: str, account_name: str):
    """Remove an account from a friend."""
    load_friends()

    for f in friends_list:
        if f["id"] == friend_id and f["accounts"]:
            if account_name in f["accounts"]:
                f["accounts"].remove(account_name)
                save_friends(friends_list)
            return

def get_app_lang_as_id() -> str:
    """
    Returns The Language `ID`.
    Such as: `id`, `en`, `hi`, `...`
    """

    if not finder_config:
        load_finder_config()
    
    party_lang = finder_config.get(CFG_NAME_PREFFERED_LANG)
    if party_lang:
        return party_lang
    
    # Fallback to the app's language
    App_Lang = app.lang.language
    lang_id = 'en'
    
    # Search for matching language name
    for lang_code, lang_info in DEFAULT_LANGUAGES_DICT.items():
        if App_Lang == lang_info["name"]:
            lang_id = lang_code
            break
    
    # Save the detected language as preferred
    update_finder_config(CFG_NAME_PREFFERED_LANG, lang_id)
    return lang_id


def get_languages_for_current_platform() -> dict:
    """
    Returns language IDs and names filtered for the current platform.
    On non-Android platforms, only shows alphabet-compatible languages.
    """
    
    if babase.app.classic.platform != 'android':
        # Only show PC-compatible languages
        return {
            lang_id: lang_info["name"]
            for lang_id, lang_info in DEFAULT_LANGUAGES_DICT.items()
            if lang_info["pc_compatible"]
        }
    else:
        # Android: show all languages
        return get_language_names_dict()

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

# UI helper functions
def bw(*, oac=None, **k):
    """Create a custom button widget."""
    return obw(
        texture=gt('white'),
        on_activate_call=oac,
        enable_sound=False,
        **k
    )

def cw(*, size=None, oac=None, **k):
    """Create the main window with overlay."""
    p = ocw(
        parent=zw('overlay_stack'),
        background=False,
        transition='in_scale',
        size=size,
        on_outside_click_call=oac,
        **k
    )
    x,y = babase.get_virtual_screen_size()
    iw(
        parent=p,
        texture=gt('white'),
        size=(x*2, y*2),
        position=(-x*0.5, 0-200),
        opacity=0.55,
        color=(0, 0, 0)
    )
    iw(parent=p, size=size)
    return (p,)

def TIP(text, color=None):
    """Show a tooltip message."""
    theme = ReactiveTheme()
    final_color = color if color is not None else theme.get_color('COLOR_TERTIARY')
    push(text, final_color)

_spinner_states = {}

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
    """
    Create or edit a spinner widget.
    """
    
    # Default size if not provided
    if size is None:
        size = (50, 50)
    
    # Default color if not provided
    if color is None:
        color = (1, 1, 1)
    
    if edit is not None:
        widget_id = id(edit)
        if widget_id in _spinner_states:
            state = _spinner_states[widget_id]
            state['visible'] = visible
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

    # Store animation state
    widget_id = id(main_widget)
    _spinner_states[widget_id] = {
        'style': style,
        'fade': fade,
        'visible': visible,
        'presence': 1.0 if visible else 0.0,
        'current_frame': 0,
        'last_update': apptime(),
        'image_widget': image_widget
    }
    
    # Set up update timer for animation
    def update_spinner():
        if not main_widget.exists():
            if widget_id in _spinner_states:
                del _spinner_states[widget_id]
            return
        
        if widget_id not in _spinner_states:
            return
            
        state = _spinner_states[widget_id]
        current_time = apptime()
        elapsed = current_time - state['last_update']
        
        # Update visibility and presence
        if state['visible']:
            if state['fade']:
                state['presence'] = min(1.0, state['presence'] + elapsed * 1.0)
            else:
                state['presence'] = 1.0
        else:
            if state['fade']:
                state['presence'] = max(0.0, state['presence'] - elapsed * 2.0)
            else:
                state['presence'] = 0.0
        
        # Calculate alpha based on presence
        alpha = max(0.0, min(1.0, state['presence'] * 2.0 - 1.0))
        
        # Advance through frames at 24fps
        frame = int(current_time * 24) % 12
        texture_name = f'spinner{frame}'
        state['current_frame'] = frame
        
        if state['image_widget'].exists():
            iw(
                edit=state['image_widget'],
                texture=gt(texture_name),
                opacity=alpha
            )
        
        state['last_update'] = current_time
        
        # Continue animation if visible and present
        if state['visible'] or state['presence'] > 0:
            teck(0.016, update_spinner)
    
    # Start the animation
    teck(0.016, update_spinner)
    
    return main_widget

def spinner_set_visible(spinner_widget: _bauiv1.Widget, visible: bool):
    """Set the visibility of a spinner widget."""
    widget_id = id(spinner_widget)
    if widget_id in _spinner_states:
        _spinner_states[widget_id]['visible'] = visible

def spinner_set_fade(spinner_widget: _bauiv1.Widget, fade: bool):
    """Set whether the spinner fades in/out."""
    widget_id = id(spinner_widget)
    if widget_id in _spinner_states:
        _spinner_states[widget_id]['fade'] = fade


_error_states = {}

def error_display(
    *,
    edit: _bauiv1.Widget | None = None,
    parent: _bauiv1.Widget | None = None,
    size: Optional[Sequence[float]] = None,
    position: Optional[Sequence[float]] = None,
    color: Optional[Sequence[float]] = None,
    opacity: float | None = None,
    error_text: str = "",
    text_color: Optional[Sequence[float]] = None,
    text_scale: float = 1.2,
    text_maxwidth: float = 600,
    icon_texture: str = 'cuteSpaz',
    fade: bool = True,
    visible: bool = True
) -> _bauiv1.Widget:
    """
    Create or edit an error display widget with icon and text.
    
    Args:
        edit: Widget to edit (if None, creates new)
        parent: Parent widget
        size: Size of the icon (default: (180, 200))
        position: Position of the container (default: (0, 0))
        color: Color of the icon (default: (1, 1, 1))
        opacity: Opacity of the icon (default: 1.0)
        error_text: Error message to display
        text_color: Color of the error text (default: theme COLOR_PRIMARY)
        text_scale: Scale of the error text
        text_maxwidth: Maximum width for text wrapping
        icon_texture: Texture for the error icon (default: 'cuteSpaz')
        fade: Whether to fade in/out
        visible: Initial visibility
    
    Returns:
        Container widget containing icon and text
    """
    
    # Default size if not provided
    if size is None:
        size = (180, 200)
    
    # Default color if not provided
    if color is None:
        color = (1, 1, 1)
    
    # Default text color if not provided
    if text_color is None:
        try:
            theme = ReactiveTheme()
            text_color = theme.get_color('COLOR_PRIMARY')
        except:
            text_color = (1, 1, 1)
    
    if edit is not None:
        widget_id = id(edit)
        if widget_id in _error_states:
            state = _error_states[widget_id]
            state['visible'] = visible
            state['error_text'] = error_text
            
            # Update text widget if exists
            if state['text_widget'] and state['text_widget'].exists():
                tw(
                    edit=state['text_widget'],
                    text=error_text
                )
        return edit

    # Create container for icon and text
    container = ocw(
        parent=parent,
        size=size,
        position=position,
        background=False
    )
    
    # Calculate positions for icon and text
    icon_size = (size[0], size[1] * 0.7) 
    text_height = size[1] * 0.3
    
    # Create icon widget
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
        # Fallback to neoSpazIcon if cuteSpaz not available
        print(f"Error creating error icon: {e}")
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
            print(f"Fallback also failed: {e2}")
            # Create empty widget as fallback
            icon_widget = iw(
                parent=container,
                size=(1, 1),
                position=(0, 0),
                texture=gt('white'),
                opacity=0.0
            )
    
    # Create text widget
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
    
    # Store animation state
    widget_id = id(container)
    _error_states[widget_id] = {
        'fade': fade,
        'visible': visible,
        'presence': 1.0 if visible else 0.0,
        'icon_widget': icon_widget,
        'text_widget': text_widget,
        'container': container,
        'error_text': error_text,
        'last_update': apptime()
    }
    
    # Set up update timer for fade animation
    def update_error_display():
        if not container.exists():
            if widget_id in _error_states:
                del _error_states[widget_id]
            return
        
        if widget_id not in _error_states:
            return
            
        state = _error_states[widget_id]
        current_time = apptime()
        elapsed = current_time - state['last_update']
        
        # Update visibility and presence
        if state['visible']:
            if state['fade']:
                state['presence'] = min(1.0, state['presence'] + elapsed * 2.0)
            else:
                state['presence'] = 1.0
        else:
            if state['fade']:
                state['presence'] = max(0.0, state['presence'] - elapsed * 3.0)
            else:
                state['presence'] = 0.0
        
        # Calculate alpha based on presence
        alpha = max(0.0, min(1.0, state['presence']))
        
        # Update icon opacity
        if state['icon_widget'] and state['icon_widget'].exists():
            iw(
                edit=state['icon_widget'],
                opacity=alpha
            )
        
        # Update text opacity
        if state['text_widget'] and state['text_widget'].exists():
            text_r, text_g, text_b = text_color
            tw(
                edit=state['text_widget'],
                color=(text_r, text_g, text_b, alpha)
            )
        
        state['last_update'] = current_time
        
        # Continue animation if visible or fading out
        if state['visible'] or state['presence'] > 0:
            teck(0.016, update_error_display)
    
    # Start the animation
    teck(0.016, update_error_display)
    
    return container

def error_display_set_visible(error_widget: _bauiv1.Widget, visible: bool):
    """Set the visibility of an error display widget."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        _error_states[widget_id]['visible'] = visible

def error_display_set_fade(error_widget: _bauiv1.Widget, fade: bool):
    """Set whether the error display fades in/out."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        _error_states[widget_id]['fade'] = fade

def error_display_set_text(error_widget: _bauiv1.Widget, text: str):
    """Update the error text of an error display widget."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        state = _error_states[widget_id]
        state['error_text'] = text
        if state['text_widget'] and state['text_widget'].exists():
            tw(
                edit=state['text_widget'],
                text=text
            )

def error_display_get_text(error_widget: _bauiv1.Widget) -> str:
    """Get the current error text of an error display widget."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        return _error_states[widget_id].get('error_text', '')
    return ''

def error_display_set_icon(error_widget: _bauiv1.Widget, icon_texture: str):
    """Change the icon texture of an error display widget."""
    widget_id = id(error_widget)
    if widget_id in _error_states:
        state = _error_states[widget_id]
        if state['icon_widget'] and state['icon_widget'].exists():
            try:
                iw(
                    edit=state['icon_widget'],
                    texture=gt(icon_texture)
                )
            except:
                print(f"Error: Texture '{icon_texture}' not found")

def wrap_text(text, max_line_length=80):
    """Wrap text to specified line length with word boundaries.
    
    Args:
        text: The text to wrap.
        max_line_length: Maximum line length in characters.
    
    Returns:
        A list of lines.
    """
    # Split text into words
    words = text.split()
    
    # Break words that are too long
    broken_words = []
    for word in words:
        if len(word) > max_line_length:
            # Break the word into chunks
            for i in range(0, len(word), max_line_length):
                broken_words.append(word[i:i+max_line_length])
        else:
            broken_words.append(word)
    
    # Build lines
    lines = []
    current_line = []
    current_length = 0
    
    for word in broken_words:
        # Check if we can add this word to the current line
        if current_line:
            # Account for a space
            new_length = current_length + 1 + len(word)
        else:
            new_length = len(word)
        
        if new_length <= max_line_length:
            current_line.append(word)
            current_length = new_length
        else:
            # Start a new line
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

class ReactiveLanguage:
    """Class for handling texts reactively."""
    
    def __init__(self):
        self._callbacks = {}
        self._texts = {}
        self._current_lang = 'en'
        self._load_initial_texts()
    
    def _load_initial_texts(self):
        """Load initial texts from the settings."""
        if not finder_config:
            load_finder_config()
        
        self._current_lang = get_app_lang_as_id()
        self._load_language_texts(self._current_lang)
    
    def _load_language_texts(self, lang_id):
        """Load all texts for a specific language."""
        self._texts = {}
        for text_key, translations in Translate_Texts.items():
            text = translations.get(lang_id, translations.get('en', f'[{text_key}]'))
            self._texts[text_key] = text
    
    def get_text(self, text_key, default=None):
        """Get current text by key."""
        return self._texts.get(text_key, default or f'[{text_key}]')
    
    def get_text_lambda(self, text_key, default=None):
        """Return a lambda that always returns the current text."""
        return lambda: self._texts.get(text_key, default or f'[{text_key}]')
    
    def subscribe(self, text_key, callback):
        """Subscribe to a callback function for when a text changes."""
        if text_key not in self._callbacks:
            self._callbacks[text_key] = []
        self._callbacks[text_key].append(callback)
    
    def unsubscribe(self, text_key, callback):
        """Cancel subscription."""
        if text_key in self._callbacks and callback in self._callbacks[text_key]:
            self._callbacks[text_key].remove(callback)
    
    def update_language(self, lang_id):
        """Change language and notify subscribers."""
        if lang_id == self._current_lang:
            return
        
        old_texts = self._texts.copy()
        self._current_lang = lang_id
        self._load_language_texts(lang_id)
        
        # Notify all text subscribers that changed
        for text_key, callback_list in self._callbacks.items():
            old_text = old_texts.get(text_key)
            new_text = self._texts.get(text_key)
            if old_text != new_text:
                for callback in callback_list[:]:
                    try:
                        callback(new_text)
                    except Exception as e:
                        print(f"Error in callback of {text_key}: {e}")
    
    def refresh_from_config(self):
        """Refresh language from settings."""
        old_lang = self._current_lang
        self._load_initial_texts()
        
        # If the language has changed, notify everyone
        if old_lang != self._current_lang:
            for text_key, callback_list in self._callbacks.items():
                for callback in callback_list[:]:
                    try:
                        callback(self._texts.get(text_key, text_key))
                    except Exception as e:
                        print(f"Error in callback of {text_key}: {e}")

class ReactiveTheme:
    """Class for handling colors reactively."""
    
    def __init__(self):
        self._callbacks = {}
        self._colors = {}
        self._load_initial_colors()
    
    def _load_initial_colors(self):
        """Load initial colors from finder_config."""
        if not finder_config:
            load_finder_config()
        
        self._colors = {
            'COLOR_BACKGROUND': tuple(finder_config.get(CFG_NAME_COLOR_BACKGROUND, (0.1, 0.1, 0.1))),
            'COLOR_SECONDARY': tuple(finder_config.get(CFG_NAME_COLOR_SECONDARY, (0.2, 0.2, 0.2))),
            'COLOR_TERTIARY': tuple(finder_config.get(CFG_NAME_COLOR_TERTIARY, (0.6, 0.6, 0.6))),
            'COLOR_PRIMARY': tuple(finder_config.get(CFG_NAME_COLOR_PRIMARY, (1.0, 1.0, 1.0))),
            'COLOR_ACCENT': tuple(finder_config.get(CFG_NAME_COLOR_ACCENT, (1.0, 1.0, 1.0)))
        }
    
    def get_color(self, color_name):
        """Get current color."""
        return self._colors.get(color_name)
    
    def get_color_lambda(self, color_name):
        """Return a lambda that always returns the current color."""
        return lambda: self._colors.get(color_name)
    
    def subscribe(self, color_name, callback):
        """Subscribe to a callback function to activate when a color changes."""
        if color_name not in self._callbacks:
            self._callbacks[color_name] = []
        self._callbacks[color_name].append(callback)
    
    def unsubscribe(self, color_name, callback):
        """Cancel subscription."""
        if color_name in self._callbacks and callback in self._callbacks[color_name]:
            self._callbacks[color_name].remove(callback)
    
    def update_colors(self, colors_dict):
        """Update colors and notify subscribers."""
        changed_colors = []
        
        for color_name, new_color in colors_dict.items():
            if color_name in self._colors and self._colors[color_name] != new_color:
                self._colors[color_name] = new_color
                changed_colors.append(color_name)
        
        # Notify subscribers of the color changes
        for color_name in changed_colors:
            if color_name in self._callbacks:
                for callback in self._callbacks[color_name][:]:
                    try:
                        callback(self._colors[color_name])
                    except Exception as e:
                        print(f"Error in callback of {color_name}: {e}")
    
    def refresh_from_config(self):
        """Refresh colors from settings."""
        old_colors = self._colors.copy()
        self._load_initial_colors()
        
        # Check which colors changed
        changed_colors = []
        for color_name, new_color in self._colors.items():
            if color_name in old_colors and old_colors[color_name] != new_color:
                changed_colors.append(color_name)
        
        # Report changes
        for color_name in changed_colors:
            if color_name in self._callbacks:
                for callback in self._callbacks[color_name][:]:
                    try:
                        callback(self._colors[color_name])
                    except Exception as e:
                        print(f"Error in callback of {color_name}: {e}")

class BorderWindow:
    def __init__(self, window_size, border_thickness=4, top_extra=4):
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

    class BorderInfo:
        def __init__(self, size, position):
            self.size = size
            self.position = position

    def _make_border(self, size, position):
        return BorderWindow.BorderInfo(size=size, position=position)

class CreditsWindow:
    """Window for displaying credits."""
    
    def __init__(self, source_widget):
        self.source_widget = source_widget
        
        self.theme = ReactiveTheme()
        self.language = ReactiveLanguage()
        
        self._create_ui()
        self._build_content()
    
    def _format_inspiration(self):
        """Format the inspiration dictionary into readable text."""
        inspiration_data = {
            'BrotherBoard': ['finder'],
            'FluffyPal': ['FluffyPartyWindow'],
            'Mr.Smoothy': ['adv']
        }
        
        formatted = []
        for author, mods in inspiration_data.items():
            mods_str = ', '.join(mods)
            formatted.append(f"{author} -> mods: {mods_str}")
        
        return '\n'.join(formatted)
    
    def _create_ui(self):
        window_size = (600, 550)
        borders = BorderWindow(window_size)
        
        self.root = cw(
            scale_origin_stack_offset=self.source_widget.get_screen_space_center(),
            size=window_size,
            oac=self.close,
        )[0]
        
        # Window background
        iw(
            parent=self.root,
            size=window_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )
        
        # Borders
        iw(
            parent=self.root,
            size=borders.border_left.size,
            position=borders.border_left.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )
        
        iw(
            parent=self.root,
            size=borders.border_top.size,
            position=borders.border_top.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )
        
        iw(
            parent=self.root,
            size=borders.border_right.size,
            position=borders.border_right.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )
        
        iw(
            parent=self.root,
            size=borders.border_bottom.size,
            position=borders.border_bottom.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )
        
        # Window title
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
        
        # Scroll widget for content
        self.main_scroll = sw(
            parent=self.root,
            size=(550, 440),
            position=(25, 40),
            border_opacity=0.3,
            color=self.theme.get_color('COLOR_SECONDARY')
        )
        
        # Container for scroll
        self.scroll_content = ocw(
            parent=self.main_scroll,
            size=(550, 1000),
            background=False
        )
    
    def _build_content(self):
        """Build all content sections within the scroll container."""
        current_y = 680
        section_spacing = 40
        line_spacing = 5
        line_height = 25
        self.text_widgets = []
        
        # Developer section
        dev_title = tw(
            parent=self.scroll_content,
            text=self.language.get_text('CreditsWindow.developer'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(240, current_y),
            h_align='center',
            v_align='center',
            scale=1.0,
            maxwidth=500
        )
        self.text_widgets.append(dev_title)
        current_y -= line_height + 10
        
        dev_name = tw(
            parent=self.scroll_content,
            text=CREATOR,
            color=self.theme.get_color('COLOR_TERTIARY'),
            position=(240, current_y),
            h_align='center',
            v_align='center',
            scale=1.1,
            maxwidth=500
        )
        self.text_widgets.append(dev_name)
        current_y -= section_spacing
        
        # Motivation section
        motivation_title = tw(
            parent=self.scroll_content,
            text=self.language.get_text('CreditsWindow.motivation'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(240, current_y),
            h_align='center',
            v_align='center',
            scale=1.0,
            maxwidth=500
        )
        self.text_widgets.append(motivation_title)
        current_y -= line_height + 10
        
        # Get and wrap motivation description
        motivation_text = self.language.get_text('CreditsWindow.motivationDescription')
        wrapped_motivation = wrap_text(motivation_text, 60)
        
        for i, line in enumerate(wrapped_motivation):
            widget = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_TERTIARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.8,
                maxwidth=500
            )
            self.text_widgets.append(widget)
        
        current_y -= (len(wrapped_motivation) * (line_height + line_spacing)) + section_spacing
        
        # Inspiration section
        inspiration_title = tw(
            parent=self.scroll_content,
            text=self.language.get_text('CreditsWindow.inspiration'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(240, current_y),
            h_align='center',
            v_align='center',
            scale=1.0,
            maxwidth=500
        )
        self.text_widgets.append(inspiration_title)
        current_y -= line_height
        
        inspiration_desc = self.language.get_text('CreditsWindow.inspirationDescription')
        wrapped_inspiration = wrap_text(inspiration_desc, 60)
        
        for i, line in enumerate(wrapped_inspiration):
            widget = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_TERTIARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.8,
                maxwidth=500
            )
            self.text_widgets.append(widget)
        
        current_y -= (len(wrapped_inspiration) * (line_height + line_spacing)) + 20
        
        # Format and display inspiration data
        inspiration_data = self._format_inspiration()
        inspiration_lines = inspiration_data.split('\n')
        
        for i, line in enumerate(inspiration_lines):
            widget = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_TERTIARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.9,
                maxwidth=500
            )
            self.text_widgets.append(widget)
        
        current_y -= (len(inspiration_lines) * (line_height + line_spacing)) + section_spacing
        
        # Thanks message section
        thanks_text = self.language.get_text('CreditsWindow.thanksMessage')
        wrapped_thanks = wrap_text(thanks_text, 80)
        
        for i, line in enumerate(wrapped_thanks):
            widget = tw(
                parent=self.scroll_content,
                text=line,
                color=self.theme.get_color('COLOR_PRIMARY'),
                position=(240, current_y - (i * (line_height + line_spacing))),
                h_align='center',
                v_align='center',
                scale=0.9,
                maxwidth=500
            )
            self.text_widgets.append(widget)
        
        # Calculate the bottom position
        last_line_bottom = current_y - (len(wrapped_thanks) * (line_height + line_spacing))
        total_height_needed = 720  
        
        ocw(
            edit=self.scroll_content,
            size=(550, total_height_needed)
        )
    
    def close(self):
        """Close the window."""
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')

class ProfileSearchWindow:
    """ Profile Search Window """

    # Character mapping to textures
    CHARACTER_MAP = {
        "Frosty": "frosty",
        "Taobao Mascot": "ali",
        "Kronk": "kronk",
        "Zoe": "zoe",
        "Bernard": "bear",
        "Wizard": "wizard",
        "Snake Shadow": "ninja",
        "Bones": "bones",
        "Cyborg": "cyborg",
        "Penguin": "penguin",
        "Pixie": "pixie",
        "B-9000": "cyborg",
        "Santa Claus": "santa",
        "Spaz": "neoSpaz",
        "Grumbledorf": "wizard",
        "Penguin": "penguin",
        "Pascal": "jack",
        "Jack Morgan": "jack",
        "Easter Bunny": "bunny",
        "Agent Johnson": "agent",
        "Mel": "mel",
        "Pixel": "pixie"
    }

    """Window for searching profiles with API."""    
    def __init__(self, source_widget, search=None, v2=None, pb=None, id=None):

        self.theme = ReactiveTheme()
        self.language = ReactiveLanguage() 

        # Determine which parameter was passed
        self.passed_param = None
        self.passed_value = None
        self.profile_data = None
        self.loading = True
        self.error = None
        self.account_not_found = False

        # Check which parameters
        params_provided = []
        if search is not None:
            params_provided.append(("search", search))
        if v2 is not None: 
            params_provided.append(("v2", v2))
        if pb is not None:
            params_provided.append(("pb", pb))
        if id is not None:
            params_provided.append(("id", id))

        if len(params_provided) == 1:
            self.passed_param, self.passed_value = params_provided[0]
        elif len(params_provided) == 0:
            # Default to v2="less"
            self.passed_param = "v2"
            self.passed_value = "less"
        else:
            self.passed_param, self.passed_value = params_provided[0]
            print(f"[ProfileSearchWindow] Multiple parameters provided, using first: {self.passed_param}={self.passed_value}")
            print(f"[ProfileSearchWindow] Ignored parameters: {params_provided[1:]}")

        self._create_ui(source_widget)
        self._fetch_profile_data()
    
    def _create_ui(self, source_widget):
        window_size = (550, 650)
        borders = BorderWindow(window_size)
        
        self.root = cw(
            scale_origin_stack_offset=source_widget.get_screen_space_center(),
            size=window_size,
            oac=self.close,
        )[0]

        self.footer = obw(
            parent=self.root,
            size=window_size,
            texture=gt('empty'),
            label='',
            enable_sound=False
        )
        
        # Window background
        iw(
            parent=self.root,
            size=window_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )

        self.border_left = iw(
            parent=self.root,
            size=borders.border_left.size,
            position=borders.border_left.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_top = iw(
            parent=self.root,
            size=borders.border_top.size,
            position=borders.border_top.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_right = iw(
            parent=self.root,
            size=borders.border_right.size,
            position=borders.border_right.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_bottom = iw(
            parent=self.root,
            size=borders.border_bottom.size,
            position=borders.border_bottom.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )
        
        # Window title
        self.title_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearchWindow.profileSearch'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(window_size[0] * 0.20, window_size[1] - 50),
            h_align='center',
            v_align='center',
            scale=1.5,
            maxwidth = 200,
            max_height=45,
        )
        
        # Loading/status text
        self.status_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearchWindow.loadingProfileData'),
            color=self.theme.get_color('COLOR_TERTIARY'),
            position=(window_size[0] * 0.5, window_size[1] * 0.5),
            h_align='center',
            v_align='center',
            scale=1.0,
            maxwidth=window_size[0] - 50
        )
        
        # Loading spinner
        self.loading_spinner = None
        try:
            self.loading_spinner = spinner(
                parent=self.root,
                position=(window_size[0] * 0.5 - 25, window_size[1] * 0.5 - 75),
                size=(50, 50),
                color=(1, 1, 1),
                visible=True
            )
        except Exception as e:
            print(f"Error creating spinner: {e}")

        self.header_container = None
        self.main_scroll = None
        self.basic_info_widgets = []
        self.info_text_widgets = []
        self.error_display_widget = None
        self.add_friend_button = None

    def _create_profile_content(self):
        """Create profile content after data is loaded."""
        window_size = (550, 650)
        
        # Header container
        self.header_container = ocw(
            parent=self.root,
            size=(500, 120),
            position=(25, window_size[1] - 180),
            background=False
        )
        
        # Character display
        self.character_widget = iw(
            parent=self.header_container,
            size=(100, 105),
            position=(10, 10),
            texture=gt('white'),
            color=(1, 1, 1),
            opacity=0
        )

        # Create friend button with initial state
        self._create_friend_button()
        
        # Basic info container
        self.basic_info_container = ocw(
            parent=self.header_container,
            size=(380, 110),
            position=(120, -5),
            background=False
        )
        
        # Main scroll container
        self.main_scroll = sw(
            parent=self.root,
            size=(500, 455),
            position=(25, 10),
            border_opacity=0.3,
            color=self.theme.get_color('COLOR_SECONDARY')
        )
        
        # Container for scroll content
        self.scroll_content = ocw(
            parent=self.main_scroll,
            size=(500, 600),
            background=False
        )

    def _create_friend_button(self):
        """Create or recreate the friend button based on current friend status."""
        # Remove existing button if any
        if self.add_friend_button and self.add_friend_button.exists():
            self.add_friend_button.delete()
        
        # Check friend status
        is_already_friend = self._check_if_friend()
        
        if is_already_friend:
            try:
                texture = gt('cuteSpaz')
                on_activate = lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
            except Exception as e:
                print(f"Error loading cuteSpaz texture: {e}")
                try:
                    texture = gt('achievementStayinAlive')
                    on_activate = lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
                except Exception as e2:
                    print(f"Error loading achievementStayinAlive texture: {e2}")
                    texture = gt('star')
                    color = (0, 1, 0)
                    on_activate = lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
        else:
            # Not friend
            try:
                texture = gt('achievementStayinAlive')
                on_activate = self._add_friend_from_profile
            except Exception as e:
                print(f"Error loading achievementStayinAlive texture: {e}")
                try:
                    texture = gt('cuteSpaz')
                    on_activate = self._add_friend_from_profile
                except Exception as e2:
                    print(f"Error loading cuteSpaz texture: {e2}")
                    texture = gt('star')
                    on_activate = self._add_friend_from_profile
        
        # Create the button
        self.add_friend_button = obw(
            parent=self.header_container,
            label='',
            size=(50, 50),
            position=(440, 110),
            texture=texture,
            color=(1,1,1),
            enable_sound=True,
            on_activate_call=on_activate
        )

    def _check_if_friend(self):
        """Check if current profile is already in friends list."""
        if not self.profile_data:
            return False

        profile_name = self.profile_data.get("name", "Unknown")
        if profile_name == "Unknown":
            return False

        # Check if name start
        if not profile_name.startswith(V2_LOGO):
            prefixed_name = f"{V2_LOGO}{profile_name}"
        else:
            prefixed_name = profile_name

        friends = load_friends()
        for friend in friends:
            if friend["name"] == prefixed_name:
                return True
        return False

    def _add_friend_from_profile(self):
        """Add the current profile to friends list."""
        if not self.profile_data:
            TIP("No profile data available")
            return

        try:
            # Get profile data
            profile_name = self.profile_data.get("name", "Unknown")
            account_id = self.profile_data.get("account_id", None)
            account_pb = self.profile_data.get("account_pb", None)
            accounts = self.profile_data.get("accounts", [])

            # Load existing friends to check for duplicates
            friends = load_friends()

            # Check if already exists by name
            for f in friends:
                if f["name"] == profile_name:
                    TIP(f"{profile_name} {get_lang_text('Global.alreadyInFriendsList')}")
                    # Update button state just in case
                    self._update_friend_button_state()
                    return

            # Generate a new ID
            existing_ids = [int(f["id"]) for f in friends if f["id"].isdigit()]
            new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

            # Add friend using the CRUD function
            add_friend(
                name=profile_name,
                friend_id=new_id,
                accounts=accounts,
                account_pb=account_pb,
                account_id=account_id
            )

            TIP(f"{profile_name} {get_lang_text('Global.addedToFriendsList')}")
            gs('ding').play()

            self._update_friend_button_state(is_friend=True)
            self._try_refresh_friends_panel()

        except Exception as e:
            print(f"Error adding friend: {e}")
            TIP("Error adding friend")

    def _update_friend_button_state(self, is_friend=False):
        """Update the friend button appearance based on friend status."""
        if not hasattr(self, 'add_friend_button') or not self.add_friend_button or not self.add_friend_button.exists():
            return

        # Current friend status
        current_is_friend = is_friend or self._check_if_friend()
        
        if current_is_friend:
            # Already friend
            try:
                obw(
                    edit=self.add_friend_button,
                    texture=gt('cuteSpaz'),
                    on_activate_call=lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
                )
            except Exception as e:
                print(f"Error updating to cuteSpaz: {e}")
                try:
                    obw(
                        edit=self.add_friend_button,
                        texture=gt('achievementStayinAlive'),
                        on_activate_call=lambda: TIP(get_lang_text('Global.alreadyInFriendsList'))
                    )
                except Exception as e2:
                    print(f"Error updating to achievementStayinAlive: {e2}")
        else:
            # Not friend
            try:
                obw(
                    edit=self.add_friend_button,
                    texture=gt('achievementStayinAlive'),
                    on_activate_call=self._add_friend_from_profile
                )
            except Exception as e:
                print(f"Error updating to achievementStayinAlive: {e}")
                try:
                    obw(
                        edit=self.add_friend_button,
                        texture=gt('cuteSpaz'),
                        on_activate_call=self._add_friend_from_profile
                    )
                except Exception as e2:
                    print(f"Error updating to cuteSpaz: {e2}")

    def _try_refresh_friends_panel(self):
        """Try to refresh the friends panel if it exists."""
        try:
            FriendsWindow.refresh_friends_lists()
        except Exception as e:
            print(f"Error refreshing friends panel: {e}")

    def _display_error(self, error_message=None):
        """Display error message with error_display component."""
        if not self.root.exists():
            return

        # Clear any existing error display
        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None

        # Use custom message or default
        if error_message is None:
            error_text = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
        else:
            error_text = error_message

        # Clear status
        tw(edit=self.status_widget, text="")
        wrapped_lines = wrap_text(error_text, 30)
        display_text = '\n'.join(wrapped_lines)

        # Display error with component
        try:
            self.error_display_widget = error_display(
                parent=self.root,
                size=(180, 200),
                position=(185, 250),
                error_text=display_text,
                text_color=self.theme.get_color('COLOR_PRIMARY'),
                text_scale=1.2,
                text_maxwidth=400,
                icon_texture='cuteSpaz',
                fade=True,
                visible=True
            )
        except Exception as e:
            try:
                self.error_display_widget = error_display(
                    parent=self.root,
                    size=(100, 150),
                    position=(225, 250),
                    error_text=display_text,
                    text_color=self.theme.get_color('COLOR_PRIMARY'),
                    text_scale=1.2,
                    text_maxwidth=400,
                    icon_texture='neoSpazIcon',
                    fade=True,
                    visible=True
                )
            except Exception as e2:
                tw(edit=self.status_widget, text=error_text)

    def _extract_value_from_text(self, text):
        """Extract the value part from text."""
        if ':' in text:
            colon_index = text.find(':')
            if colon_index != -1:
                value = text[colon_index + 1:].strip()
                return value
        # If no colon found
        return text

    def _copy_data_to_clipboard(self, text):
        """Copy extracted value to clipboard."""
        try:
            # Extract the value part
            value = self._extract_value_from_text(text)
            
            COPY(value)
            TIP(get_lang_text('Global.copiedToClipboard'))
            gs('dingSmall').play()
            
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            TIP("Failed to copy to clipboard")
            gs('error').play()

    def _open_discord_url(self, user_id):
        """Open Discord URL for the given user ID."""
        discord_url = f"https://discord.com/users/{user_id}"
        print(f"[ProfileSearchWindow] Opening Discord URL: {discord_url}")
        open_url(discord_url)

    def _fetch_profile_data(self):
        """Fetch profile data from API in a separate thread."""
        def fetch_thread():
            try:
                # Build API URL
                base_url = f"{BASE_URL}/api/account"
                if self.passed_param == "v2":
                    url = f"{base_url}?v2={self.passed_value}"
                elif self.passed_param == "pb":
                    url = f"{base_url}?pb={self.passed_value}"
                elif self.passed_param == "id":
                    url = f"{base_url}?id={self.passed_value}"
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.noValidParameter')
                    self.loading = False
                    pushcall(self._update_ui, from_other_thread=True)
                    return

                # Make API request
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'BombSquad Mod'}
                )

                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read().decode()
                    parsed_data = json.loads(data)

                if "result" in parsed_data and parsed_data["result"]:
                    self.profile_data = parsed_data["result"]
                    self.loading = False
                    self.error = None
                    self.account_not_found = False
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                    self.loading = False
                    self.account_not_found = True

            except urllib.error.URLError as e:
                self.error = f"{get_lang_text('ProfileSearchWindow.Error.networkShort')} {str(e)}"
                self.loading = False
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self.error = get_lang_text('ProfileSearchWindow.Error.accountNotFound')
                    self.account_not_found = True
                else:
                    self.error = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
                    self.account_not_found = False
            except json.JSONDecodeError as e:
                self.error = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
                self.loading = False
            except Exception as e:
                self.error = get_lang_text('ProfileSearchWindow.Error.searchingAccount')
                self.loading = False
                import traceback
                print(f"[ProfileSearchWindow] Traceback: {traceback.format_exc()}")

            # Update UI in main thread
            pushcall(self._update_ui, from_other_thread=True)

        # Start the API call in a separate thread
        thread = Thread(target=fetch_thread)
        thread.daemon = True
        thread.start()
    
    def _update_ui(self):
        """Update the UI with profile data or error message."""
        
        if not self.root.exists():
            return
            
        # Remove loading spinner
        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()
            
        if self.loading:
            tw(edit=self.status_widget, text=self.language.get_text('ProfileSearchWindow.loadingProfileData'))
            return
            
        if self.error:
            # Always show error with cuteSpaz icon
            error_message = get_lang_text('ProfileSearchWindow.Error.accountNotFound') if self.account_not_found else get_lang_text('ProfileSearchWindow.Error.searchingAccount')
            self._display_error(error_message)
            return
            
        # Clear error icon if exists
        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None
            
        # Clear status and create profile content
        tw(edit=self.status_widget, text="")
        
        # Create profile content only when we have data
        if self.profile_data and not self.header_container:
            self._create_profile_content()
        
        # Update friend button state
        self._update_friend_button_state()
        
        # Update title with profile name
        profile_name = self.profile_data.get("name", "Unknown")
        
        # Display
        self._display_character()
        self._display_basic_info()
        self._display_profile_info()
    
    def _display_character(self):
        """Display the character with proper colors and mask."""
        if not self.profile_data or not self.character_widget.exists():
            return
            
        # Get character and colors from profile
        external_info = self.profile_data.get("external_info", {})
        bs_info = external_info.get("bsAccountInfo", {})
        profile_info = bs_info.get("profile", {})
        
        character_name = profile_info.get("character", "Spaz")
        color = profile_info.get("color", [1, 1, 1])
        highlight = profile_info.get("highlight", [1, 1, 1])
        
        # Convert to tuples (RGB format)
        color_tuple = tuple(color[:3])
        highlight_tuple = tuple(highlight[:3])
        
        # Map character name to texture name
        char_key = self.CHARACTER_MAP.get(character_name, "neoSpaz")
        texture_name = f"{char_key}Icon"
        mask_texture_name = f"{char_key}IconColorMask"
        
        try:
            iw(
                edit=self.character_widget,
                texture=gt(texture_name),
                tint_texture=gt(mask_texture_name),
                mask_texture=gt("characterIconMask"),
                tint_color=color_tuple,
                tint2_color=highlight_tuple,
                opacity=1
            )
        except Exception as e:
            print(f"Error loading character textures: {e}")
            try:
                iw(
                    edit=self.character_widget,
                    texture=gt('neoSpazIcon'),
                    tint_texture=gt('neoSpazIconColorMask'),
                    mask_texture=gt("characterIconMask"),
                    tint_color=color_tuple,
                    tint2_color=highlight_tuple,
                    opacity=1
                )
            except Exception as e2:
                print(f"Fallback also failed: {e2}")

    def _display_basic_info(self):
        """Display basic profile information in the header."""
        if not self.profile_data or not self.basic_info_container.exists():
            return

        # Clear previous basic info widgets
        for widget in self.basic_info_widgets:
            if widget.exists():
                widget.delete()
        self.basic_info_widgets = []

        external_info = self.profile_data.get("external_info", {})
        bs_info = external_info.get("bsAccountInfo", {})
        base_info = external_info.get("baseInfo", {})
        profile_info = bs_info.get("profile", {})

        # Basic profile info lines
        basic_info_data = [
            (f"{self.language.get_text('ProfileSearchWindow.name')}:", base_info.get('name', self.profile_data.get('name'))),
            ("Account ID:", self.profile_data.get('account_id', 'Unknown')),
            ("Account PB:", self.profile_data.get('account_pb', 'Unknown')),
            (f"{self.language.get_text('ProfileSearchWindow.character')}:", profile_info.get('character', 'Unknown'))
        ]

        # Add basic info to header
        line_height = 25
        for i, (label, value) in enumerate(basic_info_data):
            full_text = f"{label} {value}"
            text_widget = tw(
                parent=self.basic_info_container,
                text=full_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(390, 35),
                position=(-30, 90 - (i * line_height)),
                h_align='left',
                v_align='top',
                scale=0.8,
                maxwidth=390,
                max_height=25,
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=lambda t=full_text: self._copy_data_to_clipboard(t)
            )
            self.basic_info_widgets.append(text_widget)
    
    def _display_profile_info(self):
        """Display the detailed profile information in the scroll container."""
        if not self.profile_data or not self.scroll_content.exists():
            return

        # Clear previous info widgets
        for widget in self.info_text_widgets:
            if widget.exists():
                widget.delete()
        self.info_text_widgets = []

        external_info = self.profile_data.get("external_info", {})
        bs_info = external_info.get("bsAccountInfo", {})
        base_info = external_info.get("baseInfo", {})
        ballistica_info = external_info.get("ballisticaAccountInfo", {})
        profile_info = bs_info.get("profile", {})

        # Start position
        current_y = 550
        line_height = 25
        section_spacing = 15

        # Accounts section
        accounts = self.profile_data.get("accounts", [])
        if accounts:
            accounts_title_text = f"{self.language.get_text('ProfileSearchWindow.accounts')}:"
            accounts_title = tw(
                parent=self.scroll_content,
                text=accounts_title_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                position=(10, current_y),
                h_align='left',
                v_align='top',
                scale=0.8,
                maxwidth=480,
                glow_type='uniform'
            )
            self.info_text_widgets.append(accounts_title)
            current_y -= line_height

            # Display accounts
            for account in accounts:
                account_text = f"• {account}"
                account_widget = tw(
                    parent=self.scroll_content,
                    text=account_text,
                    color=self.theme.get_color('COLOR_TERTIARY'),
                    size=(600, 30),
                    position=(-50, current_y),
                    h_align='left',
                    v_align='top',
                    scale=0.7,
                    maxwidth=460,
                    selectable=True,
                    click_activate=True,
                    glow_type='uniform',
                    on_activate_call=lambda t=account_text: self._copy_data_to_clipboard(t)
                )
                self.info_text_widgets.append(account_widget)
                current_y -= line_height

            current_y -= section_spacing

        # Rank Info section
        rank = bs_info.get("rank", [])
        prev_ranks = bs_info.get("prevRanks", [])

        if rank or prev_ranks:
            # Rank Info title
            rank_title_text = f"{self.language.get_text('ProfileSearchWindow.rankInfo')}:"
            rank_title = tw(
                parent=self.scroll_content,
                text=rank_title_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                position=(10, current_y),
                h_align='left',
                v_align='top',
                scale=0.8,
                maxwidth=480,
                glow_type='uniform',
            )
            self.info_text_widgets.append(rank_title)
            current_y -= line_height

            # Current rank
            if rank and len(rank) >= 3:
                rank_text = f"  {self.language.get_text('ProfileSearchWindow.current')}: {rank[0]} {rank[1]} #{rank[2]}"
                rank_widget = tw(
                    parent=self.scroll_content,
                    text=rank_text,
                    color=self.theme.get_color('COLOR_TERTIARY'),
                    size=(600, 30),
                    position=(-50, current_y),
                    h_align='left',
                    v_align='top',
                    scale=0.7,
                    maxwidth=460,
                    selectable=True,
                    click_activate=True,
                    glow_type='uniform',
                    on_activate_call=lambda t=rank_text: self._copy_data_to_clipboard(t)
                )
                self.info_text_widgets.append(rank_widget)
                current_y -= line_height

            # Previous ranks
            if prev_ranks:
                prev_title_text = f"  {self.language.get_text('ProfileSearchWindow.previousRanks')}:"
                prev_title = tw(
                    parent=self.scroll_content,
                    text=prev_title_text,
                    color=self.theme.get_color('COLOR_TERTIARY'),
                    position=(34, current_y),
                    h_align='left',
                    v_align='top',
                    scale=0.7,
                    maxwidth=460,
                    glow_type='uniform',
                )
                self.info_text_widgets.append(prev_title)
                current_y -= line_height

                for prev_rank in prev_ranks:
                    if len(prev_rank) >= 4:
                        season, rank_name, points, position = prev_rank
                        rank_line_text = f"{self.language.get_text('ProfileSearchWindow.season')} {season}: #{position} {rank_name} {points}"
                        rank_line = tw(
                            parent=self.scroll_content,
                            text=rank_line_text,
                            color=self.theme.get_color('COLOR_TERTIARY'),
                            size=(600, 30),
                            position=(-30, current_y),
                            h_align='left',
                            v_align='top',
                            scale=0.65,
                            maxwidth=440,
                            selectable=True,
                            click_activate=True,
                            glow_type='uniform',
                            on_activate_call=lambda t=rank_line_text: self._copy_data_to_clipboard(t)
                        )
                        self.info_text_widgets.append(rank_line)
                        current_y -= line_height

                current_y -= section_spacing

        # Achievements section
        achievements = APP.classic.ach.achievements
        achievements_text_str = f"{self.language.get_text('ProfileSearchWindow.achievements')}: {bs_info.get('achievementsCompleted', 0)}/{str(len(achievements))}"
        achievements_widget = tw(
            parent=self.scroll_content,
            text=achievements_text_str,
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(10, current_y),
            h_align='left',
            v_align='top',
            scale=0.8,
            maxwidth=480,
            glow_type='uniform',
        )
        self.info_text_widgets.append(achievements_widget)
        current_y -= line_height + section_spacing

        # Trophies section
        trophies_text = bs_info.get("trophies", "")
        if trophies_text:
            # Count unique trophy characters
            trophy_counts = {}
            for char in trophies_text:
                trophy_counts[char] = trophy_counts.get(char, 0) + 1

            # Create final trophy string grouping repeated characters
            final_trophy_string = ""
            current_char = None
            current_count = 0

            for char in trophies_text:
                if char == current_char:
                    current_count += 1
                else:
                    if current_char is not None:
                        if current_count > 1:
                            final_trophy_string += f"{current_char}×{current_count} "
                        else:
                            final_trophy_string += f"{current_char} "
                    current_char = char
                    current_count = 1

            # Add last group
            if current_char is not None:
                if current_count > 1:
                    final_trophy_string += f"{current_char}×{current_count}"
                else:
                    final_trophy_string += f"{current_char}"

            # Trophies title
            trophies_title_text = f"{self.language.get_text('ProfileSearchWindow.trophies')}:"
            trophies_title = tw(
                parent=self.scroll_content,
                text=trophies_title_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                position=(10, current_y),
                h_align='left',
                v_align='top',
                scale=0.8,
                maxwidth=480,
                glow_type='uniform',
            )
            self.info_text_widgets.append(trophies_title)
            current_y -= line_height

            # Trophies display
            trophy_display = tw(
                parent=self.scroll_content,
                text=final_trophy_string,
                color=self.theme.get_color('COLOR_ACCENT'),
                size=(570, 30),
                position=(-50, current_y-5),
                h_align='left',
                v_align='top',
                scale=0.8,
                maxwidth=460,
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=lambda t=final_trophy_string: self._copy_data_to_clipboard(t)
            )
            self.info_text_widgets.append(trophy_display)
            current_y -= line_height + section_spacing

        # More Info
        more_info_title_text = f"{self.language.get_text('ProfileSearchWindow.moreInfo')}:"
        more_info_title = tw(
            parent=self.scroll_content,
            text=more_info_title_text,
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(10, current_y),
            h_align='left',
            v_align='top',
            scale=0.8,
            maxwidth=480,
            glow_type='uniform',
        )
        self.info_text_widgets.append(more_info_title)
        current_y -= line_height

        from datetime import datetime
        raw_date = base_info.get('created', 'Unknown')

        if raw_date != 'Unknown':
            dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            formatted = dt.strftime("%d/%m/%Y %H:%M")
        else:
            formatted = 'Unknown'

        # More Data
        more_data = [
            (f"{self.language.get_text('ProfileSearchWindow.accountType')}:", ballistica_info.get('accountType', 'Unknown')),
            (f"{self.language.get_text('ProfileSearchWindow.activeDays')}:", ballistica_info.get('totalActiveDays', 'Unknown')),
            (f"{self.language.get_text('ProfileSearchWindow.created')}:", ballistica_info.get('created', 'Unknown')),
            (f"{self.language.get_text('ProfileSearchWindow.lastActive')}:", ballistica_info.get('lastActive', 'Unknown')),
            (f"{self.language.get_text('ProfileSearchWindow.accountExistence')}:", formatted)
        ]

        for label, value in more_data:
            full_text = f"{label} {value}"
            text_widget = tw(
                parent=self.scroll_content,
                text=full_text,
                color=self.theme.get_color('COLOR_TERTIARY'),
                size=(600, 30),
                position=(-50, current_y),
                h_align='left',
                v_align='top',
                scale=0.7,
                maxwidth=480,
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=lambda t=full_text: self._copy_data_to_clipboard(t)
            )
            self.info_text_widgets.append(text_widget)
            current_y -= line_height

        # Set fixed height for scroll container
        ocw(edit=self.scroll_content, size=(500, 585))

    def close(self):
        """Close the window."""
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')

class AccountCard():
    def __init__(
        self,
        name: str,
        accounts: list[str],
        call: callable = None,
        parent: str = None,
        position: tuple[float, float] = (0.0, 0.0),
    ) -> None:
        super().__init__()
        self._name = name
        self._accounts = accounts
        self._call = call

        # Card size
        card_width = 650 - 40
        card_height = 100
        
        x = position[0]
        y = position[1]

        def _on_click():
            if call:
                call()

        # Container
        self._container = obw(
            parent=parent,
            label='',
            size=(card_width, card_height),
            position=(x, y),
            texture=gt('white'),
            color=(0.15, 0.15, 0.15),
            on_activate_call=_on_click,
            enable_sound=False,
        )

        # Character on the left
        character_size = (70, 70)
        character_x = x + 10
        character_y = y + (card_height - character_size[1]) / 2

        self.character_widget = iw(
            parent=parent,
            draw_controller=self._container,
            size=character_size,
            position=(character_x, character_y),
            texture=gt('cuteSpaz'),
        )

        # Header information on the right
        content_x = character_x + character_size[0] + 15
        content_width = card_width - content_x - 10

        # Check if it should be vertically centered
        should_center = self._should_center_title(name, accounts)

        if should_center:
            # Vertically centered title
            self.title_widget = tw(
                parent=parent,
                draw_controller=self._container,
                position=(content_x, y + card_height / 2 - 15),
                text=name,
                color=(0.95, 0.95, 0.95),
                scale=1.1,
                h_align='left',
                v_align='center',
                maxwidth=content_width
            )
            # Do not show accounts when centered
            self.accounts_widget = None
        else:
            # Title at the top
            self.title_widget = tw(
                parent=parent,
                draw_controller=self._container,
                position=(content_x, y + card_height - 40),
                text=name,
                color=(0.95, 0.95, 0.95),
                scale=1.1,
                h_align='left',
                v_align='center',
                maxwidth=content_width
            )

            # Process the accounts to format them with line breaks
            accounts_text = self._format_accounts(accounts)
            
            # Account text at the bottom
            self.accounts_widget = tw(
                parent=parent,
                draw_controller=self._container,
                position=(content_x, y + 15),
                text=accounts_text,
                color=(0.7, 0.7, 0.7),
                scale=0.8,
                h_align='left',
                v_align='center',
                maxwidth=content_width
            )

    def _should_center_title(self, name: str, accounts: list[str]) -> bool:
        """Determine if the title should be vertically centered."""
        # If there is exactly one account and it matches the name, center
        if len(accounts) == 1 and accounts[0] == name:
            return True
        # If there are no accounts, also center
        if not accounts:
            return True
        return False

    def _format_accounts(self, accounts: list[str]) -> str:
        """ 
            Format the account list with a maximum of 5
            accounts and line breaks every 3 accounts.
        """
        if not accounts:
            return "No accounts"
        
        # Limit to a maximum of 5 accounts
        display_accounts = accounts[:5]
        has_more = len(accounts) > 5
        
        formatted = []
        for i, account in enumerate(display_accounts, 1):
            formatted.append(account)
            if i % 3 == 0 and i < len(display_accounts):
                formatted.append("\n")
            elif i < len(display_accounts):
                formatted.append(", ")
        
        # Add "..." if there are more accounts
        if has_more:
            if len(display_accounts) % 3 == 0:
                formatted.append("\n...")
            else:
                formatted.append(", ...")
        
        return "".join(formatted)

    def get_button(self):
        """Return the main button widget for external use"""
        return self._container
    
class ProfileSearch:
    """Window for searching profiles by name."""
    
    def __init__(self, source_widget, search_term: str = ""):
        self.source_widget = source_widget
        self.search_term = search_term
        self.loading = True if search_term else False
        self.error = None
        self.results = []
        self.current_page = 0
        self.total_pages = 0
        self.total_results = 0
        self.page_size = 0

        self.theme = ReactiveTheme()
        self.language = ReactiveLanguage() 

        if not finder_config:
            load_finder_config()
        self.current_filter = finder_config.get(CFG_NAME_FILTER_ACCOUNT, 'all') 

        self._create_ui()
        if self.search_term:
            self._fetch_search_results()

    def _create_ui(self):

        window_size = (700, 550)
        borders = BorderWindow(window_size)

        self.root = cw(
            scale_origin_stack_offset=self.source_widget.get_screen_space_center(),
            size=window_size,
            oac=self.close,
        )[0]

        # Footer
        self.footer = obw(
            parent=self.root,
            size=window_size,
            texture=gt('empty'),
            label='',
            enable_sound=False
        )

        # Window background
        iw(
            parent=self.root,
            size=window_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )

        # Borders
        self.border_left = iw(
            parent=self.root,
            size=borders.border_left.size,
            position=borders.border_left.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_top = iw(
            parent=self.root,
            size=borders.border_top.size,
            position=borders.border_top.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_right = iw(
            parent=self.root,
            size=borders.border_right.size,
            position=borders.border_right.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_bottom = iw(
            parent=self.root,
            size=borders.border_bottom.size,
            position=borders.border_bottom.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        # Window title
        self.title_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearch.profileSearch'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(window_size[0] * 0.5, window_size[1] - 50),
            h_align='center',
            v_align='center',
            scale=1.2,
            maxwidth = 400,
            max_height=32,
        )

        # Search input field
        self.search_input = tw(
            parent=self.root,
            position=(35, window_size[1] - 100),
            size=(330, 40),
            text=self.search_term,
            editable=True,
            description="Enter player name to search",
            maxwidth=350,
            h_align='left',
            v_align='center',
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        # Search placeholder
        self.search_placeholder = tw(
            parent=self.root,
            position=(75, window_size[1] - 103),
            text="",
            color=self.theme.get_color('COLOR_TERTIARY')
        )

        # Search button
        buttonSearchSize = (120, 40)
        buttonSearchPosition = (405, window_size[1] - 100)
        self.search_button = bw(
            parent=self.root,
            position=buttonSearchPosition,
            size=buttonSearchSize,
            label=self.language.get_text('Global.search'),
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=self._on_search_pressed
        )

        borders = BorderWindow(buttonSearchSize)
        
        # Search borders button
        self.search_border_left = iw(
            parent=self.root,
            size=(borders.border_left.size[0]-1, borders.border_left.size[1]+3.5),
            position=(buttonSearchPosition[0]-5, buttonSearchPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.search_border_top = iw(
            parent=self.root,
            size=(borders.border_top.size[0]+4, borders.border_top.size[1]-1),
            position=(buttonSearchPosition[0]-2, buttonSearchPosition[1]+buttonSearchSize[1]),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.search_border_right = iw(
            parent=self.root,
            size=(borders.border_right.size[0]-1, borders.border_right.size[1]+3.5),
            position=(buttonSearchPosition[0]+buttonSearchSize[0]+4, buttonSearchPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.search_border_bottom = iw(
            parent=self.root,
            size=(borders.border_bottom.size[0]+6.5, borders.border_bottom.size[1]-1),
            position=(buttonSearchPosition[0]-2, buttonSearchPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        # Filter button
        buttonFilterSize = (120, 40)
        buttonFilterPosition = (545, window_size[1] - 100)
        borders = BorderWindow(buttonFilterSize)

        self.filter_button = bw(
            parent=self.root,
            position=buttonFilterPosition,
            size=buttonFilterSize,
            label=f"{self.language.get_text('Global.filter')}: {self.current_filter.upper()}",
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=self._show_filter_popup
        )

        self.filter_border_left = iw(
            parent=self.root,
            size=(borders.border_left.size[0], borders.border_left.size[1]+3.5),
            position=(buttonFilterPosition[0]-5, buttonFilterPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.filter_border_top = iw(
            parent=self.root,
            size=(borders.border_top.size[0]+4, borders.border_top.size[1]-1),
            position=(buttonFilterPosition[0]-2, buttonFilterPosition[1]+buttonFilterSize[1]),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.filter_border_right = iw(
            parent=self.root,
            size=(borders.border_right.size[0]-1, borders.border_right.size[1]+3.5),
            position=(buttonFilterPosition[0]+buttonFilterSize[0]+4, buttonFilterPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.filter_border_bottom = iw(
            parent=self.root,
            size=(borders.border_bottom.size[0]+6.5, borders.border_bottom.size[1]-1),
            position=(buttonFilterPosition[0]-2, buttonFilterPosition[1]-1),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        # Loading/status text
        self.status_widget = tw(
            parent=self.root,
            text=self.language.get_text('ProfileSearch.enterNameAndPressSearch') if not self.search_term else self.language.get_text('ProfileSearch.searching'),
            color=self.theme.get_color('COLOR_TERTIARY'),
            position=(window_size[0] * 0.47, window_size[1] * 0.45),
            h_align='center',
            v_align='center',
            scale=1.3,
            maxwidth=window_size[0] - 50
        )

        # Loading spinner
        self.loading_spinner = None
        if self.search_term:
            try:
                self.loading_spinner = spinner(
                    parent=self.root,
                    position=(window_size[0] * 0.5 - 25, window_size[1] * 0.5 - 75),
                    size=(50, 50),
                    style='simple',
                    color=(1, 1, 1),
                    visible=True
                )
            except Exception as e:
                print(f"Error creating spinner: {e}")

            
        # Scroll widget for results
        self.scroll_widget = sw(
            parent=self.root,
            size=(650, 380),
            position=(25, 50),
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        # Container for content
        self.container_widget = ocw(
            parent=self.scroll_widget,
            size=(650, 0),
            background=False
        )

        # Error widgets
        self.error_display_widget = None

        # Set up filter updater
        self._update_search_placeholder()
        self.filter_updater = tuck(0.1, self._update_search_placeholder, repeat=True)
    
    def _update_search_placeholder(self):
        """Update the search placeholder visibility."""
        if not self.search_placeholder.exists():
            self.filter_updater = None
            return
            
        current_text = tw(query=self.search_input)
        tw(edit=self.search_placeholder, text="" if current_text else "")
    
    def _show_filter_popup(self):
        """Show filter options popup."""
        x, y = self.filter_button.get_screen_space_center()
        popup = PopupMenuWindow(
            position=(x, y - 70),
            choices=[""],
            current_choice=self.current_filter,
            delegate=self,
            width=1
        )
        
        # Filter option buttons
        for i, filter_type in enumerate(["all", "v2", "id", "pb"]):
            bw(
                parent=popup.root_widget,
                position=(-70, 55 - i * 55),
                size=(140, 50),
                label=filter_type.upper(),
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(self._on_filter_selected, filter_type, popup)
            )
            self._popup_target = "filter_accounts"
    
    def popup_menu_closing(self, popup_window) -> None:
        """Handle popup menu closing."""
        self._popup_target = None

    def _on_filter_selected(self, filter_type, popup):
        """Handle filter selection."""
        self.current_filter = filter_type
        popup.root_widget.delete()

        # UPDATE SETTINGS AND BUTTON
        update_finder_config(CFG_NAME_FILTER_ACCOUNT, filter_type)

        # Update filter button text
        obw(
            edit=self.filter_button,
            label=f"{self.language.get_text('Global.filter')}: {filter_type.upper()}"
        )

        # Update placeholder
        placeholder_text = {
            "all": "Enter player name (shows all matches)",
            "v2": "Enter exact player name (finds specific account)",
            "id": "Enter account ID (e.g., a-g45489)",
            "pb": "Enter public ID (e.g., pb-IF4JU08_Jg==)"
        }.get(filter_type, "Enter search term")

        tw(edit=self.search_input, description=placeholder_text)
    
    def _clear_error_display(self):
        """Clear any existing error display."""
        if self.error_display_widget and self.error_display_widget.exists():
            self.error_display_widget.delete()
            self.error_display_widget = None
        
        # Clear error text
        tw(edit=self.status_widget, text="")
    
    def _on_search_pressed(self):
        """Handle search button press."""
        search_term = tw(query=self.search_input)
        if not search_term:
            return

        # Clear previous error
        self._clear_error_display()

        self.search_term = search_term
        self.loading = True
        self.error = None
        self.results = []

        # Update UI for loading
        tw(edit=self.status_widget, text=self.language.get_text('ProfileSearch.searching'))
        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()
        try:
            self.loading_spinner = spinner(
                parent=self.root,
                position=(350 - 25, 250 - 50),
                size=(50, 50),
                style='simple',
                color=(1, 1, 1),
                visible=True
            )
        except Exception as e:
            print(f"Error creating spinner: {e}")
        
        # Clear previous results
        if self.container_widget.exists():
            self.container_widget.delete()
        
        self.container_widget = ocw(
            parent=self.scroll_widget,
            size=(650, 0),
            background=False
        )

        self._fetch_search_results()
    
    def _fetch_search_results(self):
        """Fetch search results from API in a separate thread."""
        def fetch_thread():
            try:
                # Always use the same search endpoint
                url = f"{BASE_URL}/api/account?search={self.search_term}&max=all"
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'BombSquad Mod'}
                )

                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read().decode()
                    parsed_data = json.loads(data)
                    #print(f"[ProfileSearch] JSON parsed successfully")

                # Check if we have results
                if "results" not in parsed_data or not parsed_data["results"]:
                    self.error = "No results found"
                    self.loading = False
                    pushcall(self._update_ui, from_other_thread=True)
                    return

                results = parsed_data["results"]

                # Filter results
                if self.current_filter == "all":
                    self.results = results
                    self.total_results = parsed_data.get("totalResults", len(results))
                    self.page_size = parsed_data.get("pageSize", len(results))
                    self.total_pages = parsed_data.get("totalPages", 1)
                    self.loading = False
                    self.error = None

                elif self.current_filter == "v2":
                    exact_match = None
                    for result in results:
                        name = result.get('name')
                        if name:
                            clean_name = name.replace(V2_LOGO, '')
                            if clean_name.lower() == self.search_term.lower():
                                exact_match = result
                                break

                    if exact_match:
                        self.results = [exact_match]
                        self.total_results = 1
                        self.page_size = 1
                        self.loading = False
                        self.error = None
                    else:
                        # Second search across all results
                        url_all = f"{BASE_URL}/api/account?search={self.search_term}&max=all"
                        req_all = urllib.request.Request(
                            url_all, 
                            headers={'User-Agent': 'BombSquad Mod'}
                        )

                        with urllib.request.urlopen(req_all, timeout=15) as response_all:
                            data_all = response_all.read().decode()
                            parsed_data_all = json.loads(data_all)
                            #print(f"[ProfileSearch] All accounts search completed")

                        # Search for an exact match across all results
                        exact_match_all = None
                        if "results" in parsed_data_all:
                            for result in parsed_data_all["results"]:
                                name = result.get('name')
                                if name:
                                    clean_name = name.replace(V2_LOGO, '')
                                    if clean_name.lower() == self.search_term.lower():
                                        exact_match_all = result
                                        break

                        if exact_match_all:
                            self.results = [exact_match_all]
                            self.total_results = 1
                            self.page_size = 1
                            self.loading = False
                            self.error = None
                            #print(f"[ProfileSearch] Found exact match in all results")
                        else:
                            self.error = f"{get_lang_text('ProfileSearch.Error.noExactMatch')} '{self.search_term}'"
                            self.loading = False
                            #print(f"[ProfileSearch] No exact match found")

                elif self.current_filter == "id":
                    # Search by exact account_id
                    exact_match = None
                    for result in results:
                        account_id = result.get('account_id')
                        if account_id and str(account_id).lower() == self.search_term.lower():
                            exact_match = result
                            break

                    if exact_match:
                        self.results = [exact_match]
                        self.total_results = 1
                        self.page_size = 1
                        self.loading = False
                        self.error = None
                        #print(f"[ProfileSearch] Found exact account_id match")
                    else:
                        self.error = f"{get_lang_text('ProfileSearch.Error.noAccountFoundWithId')} {self.search_term}"
                        self.loading = False

                elif self.current_filter == "pb":
                    # Search by account PB
                    exact_match = None
                    for result in results:
                        account_pb = result.get('account_pb')
                        if account_pb and str(account_pb).lower() == self.search_term.lower():
                            exact_match = result
                            break

                    if exact_match:
                        self.results = [exact_match]
                        self.total_results = 1
                        self.page_size = 1
                        self.loading = False
                        self.error = None
                    else:
                        self.error = f"{get_lang_text('ProfileSearch.Error.noAccountFound')} {self.search_term}"
                        self.loading = False

            except urllib.error.URLError as e:
                self.error = get_lang_text('ProfileSearch.Error.network')
                self.loading = False
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self.error = get_lang_text('ProfileSearch.Error.serviceUnavailable')
                else:
                    self.error = get_lang_text('ProfileSearch.Error.searchFailed')
                self.loading = False
            except json.JSONDecodeError as e:
                self.error = get_lang_text('ProfileSearch.Error.invalidResponse')
                self.loading = False
            except Exception as e:
                self.error = get_lang_text('ProfileSearch.Error.unexpected')
                self.loading = False
                import traceback
                #print(f"[ProfileSearch] Traceback: {traceback.format_exc()}")

            # Update UI in main thread
            pushcall(self._update_ui, from_other_thread=True)

        thread = Thread(target=fetch_thread)
        thread.daemon = True
        thread.start()

    def _update_ui(self):
        """Update the UI with search results or error message."""
        if not self.root.exists():
            return

        # Remove loading spinner
        if self.loading_spinner and self.loading_spinner.exists():
            self.loading_spinner.delete()

        if self.loading:
            tw(edit=self.status_widget, text=self.language.get_text('ProfileSearch.searching'))
            return

        if self.error:
            self._display_error(self.error)
            return

        # Clear any error display
        self._clear_error_display()

        title_text = f"{self.language.get_text('Global.search')}: {self.search_term} ({self.page_size} {self.language.get_text('Global.results')})"
        tw(edit=self.title_widget, text=title_text)

        # If there are no results, show message
        if not self.results:
            self._display_error("No results found")
            return

        card_height = 100
        spacing = 10
        total_height = len(self.results) * (card_height + spacing)
        
        ocw(
            edit=self.container_widget,
            size=(650, total_height)
        )

        # Calculate initial position
        current_y = total_height - card_height

        # Show results
        for i, result in enumerate(self.results):
            name = result.get('name', 'Unknown')
            accounts = result.get('accounts', [])

            # Create AccountCard
            account_card = AccountCard(
                name=name,
                accounts=accounts,
                call=lambda r=result: self._on_result_pressed(r),
                parent=self.container_widget,
                position=(20, current_y)
            )

            # Update position for the next card
            current_y -= (card_height + spacing)

    def _display_error(self, error_message):
        """Display error message with error_display component."""
        if not self.root.exists():
            return

        # Clear any existing error display first
        self._clear_error_display()

        wrapped_lines = wrap_text(error_message, 30)
        display_text = '\n'.join(wrapped_lines)
        
        # Create error display component
        try:
            self.error_display_widget = error_display(
                parent=self.root,
                size=(180, 200),
                position=(260, 200),
                error_text=display_text,
                text_color=self.theme.get_color('COLOR_PRIMARY'),
                text_scale=1.2,
                text_maxwidth=600,
                icon_texture='cuteSpaz',
                fade=True,
                visible=True
            )
        except Exception as e:
            tw(edit=self.status_widget, text=error_message)
    
    def _on_result_pressed(self, result):
        """
            Handle result button press 
                - open ProfileSearchWindow with 
                account PB.
        """
        account_pb = result.get('account_pb')
        name = result.get('name', 'Unknown')
        
        if account_pb:
            ProfileSearchWindow(self.source_widget, pb=account_pb)
        else:
            self._display_error("Error: No account PB found in the selected profile")
    
    def close(self):
        """Close the window."""
        if self.root.exists():
            ocw(edit=self.root, transition='out_scale')

class FriendsWindow:
    """Friends Panel."""

    # Class variable to store all active instances
    _active_instances = []

    def __init__(self, parent_widget, theme, language, get_filtered_players_callback,
                 add_friend_callback, delete_friend_callback, connect_callback):
        """
        Initialize the Friends Panel.
        
        Args:
            parent_widget: The parent widget to attach to
            theme: ReactiveTheme instance for color management
            language: ReactiveLanguage instance for text management
            get_filtered_players_callback: Callback to get current filtered players
            add_friend_callback: Callback to add a friend
            delete_friend_callback: Callback to delete a friend
            connect_callback: Callback to connect to a server
        """
        
        self.theme = theme
        self.language = language
        self._get_filtered_players = get_filtered_players_callback
        self._add_friend = add_friend_callback
        self._delete_friend = delete_friend_callback
        self._connect_to_server = connect_callback
        
        # State variables
        self.best_friends_connected = 0
        self._current_displayed_best_friend = None
        self._popup_target = None
        
        # Widget references
        self.friends_parent = None
        self.friends_background = None
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
        
        # Element lists
        self.best_friends_elements = []
        self._friend_text_widgets = []
        self._connected_friend_text_widgets = []
        
        # Subscriptions
        self._language_subscriptions = []
        self._color_subscriptions = []
        
        # Register this instance
        FriendsWindow._active_instances.append(self)
        
        # Create the panel
        self._create_friends_panel(parent_widget)
        self._setup_language_subscriptions()
        self._setup_color_subscriptions()

    @classmethod
    def refresh_friends_lists(cls):
        """
        Load current friends from storage and update both UI lists.
        This method can be called from anywhere to refresh the friends panel.
        """
        #print("[FriendsWindow] Refreshing friends lists")
        
        # Get all active instances
        active_instances = []
        for instance in cls._active_instances:
            try:
                if (hasattr(instance, 'friends_parent') and 
                    instance.friends_parent and 
                    instance.friends_parent.exists()):
                    active_instances.append(instance)
            except:
                # Skip invalid instances
                continue
        
        if not active_instances:
            #print("[FriendsWindow] No active instances found")
            return
            
        for instance in active_instances:
            try:
                # Load current friends from storage
                current_friends = instance.get_all_friends()
                #print(f"[FriendsWindow] Loaded {len(current_friends)} friends")
                
                # Update the all friends list
                instance.refresh_best_friends_ui()
                
                try:
                    players_list = [V2_LOGO + player.strip() for player, _ in instance._get_filtered_players()]
                except Exception as e:
                    print(f"[FriendsWindow] Could not get players list: {e}")
                    players_list = []
                    
                instance.refresh_best_friends_connected_ui(players_list)
                #print(f"[FriendsWindow] Successfully updated instance")
                
            except Exception as e:
                print(f"[FriendsWindow] Error updating instance: {e}")

    def _create_friends_panel(self, parent_widget):
        """Create the friends panel window."""
        panel_size = (355, 435)
        self.friends_parent = ocw(
            parent=parent_widget,
            size=panel_size,
            position=(460, 0),
            background=False,
        )

        self.friends_background = iw(
            parent=self.friends_parent,
            size=panel_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )

        # Separator
        self.friends_separator = iw(
            parent=self.friends_parent,
            size=(3, 435),
            position=(0, 0),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        self.all_friends_text = tw(
            parent=self.friends_parent,
            text=self.language.get_text('FriendsWindow.allFriends'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth = 250,
            max_height=35,
            position=(540-450, 400)
        )

        self.friend_input = tw(
            parent=self.friends_parent,
            position=(695-450, 320),
            size=(120, 50),
            text="",
            color=self.theme.get_color('COLOR_PRIMARY'),
            editable=True,
            h_align='center',
            v_align='center',
            corner_scale=0.1,
            scale=10,
            allow_clear_button=False,
            shadow=0,
            flatness=1,
        )

        self.add_manual_button = bw(
            parent=self.friends_parent,
            position=(640-450, 250),
            size=(120, 39),
            text_scale=0.6,
            label=self.language.get_text('FriendsWindow.addManually'),
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                (lambda friend: (
                    self._add_friend(friend),
                    tw(edit=self.friend_input, text=""),
                    self.refresh_best_friends_ui(),
                    self.refresh_best_friends_connected_ui()
                ))(tw(query=self.friend_input))
            )
        )

        # Separator
        self.friends_separator2 = iw(
            parent=self.friends_parent,
            size=(320, 1),
            position=(470-450, 235),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        # Online friends header
        online_friends_tr = self.language.get_text("Global.online") + "\ue019"
        self.online_friends_text = tw(
            parent=self.friends_parent,
            text=online_friends_tr,
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(465-450, 195),
            maxwidth = 180,
            max_height=40,
        )

        # Best friends list
        self._friends_scroll_container = sw(
            parent=self.friends_parent,
            position=(465-450, 240),
            size=(140, 130),
            border_opacity=0.4,
            color=self.theme.get_color('COLOR_SECONDARY')
        )
        
        self._friends_list_container = None
        self.refresh_best_friends_ui()

        # Connected friends list
        self._connected_friends_scroll_container = sw(
            parent=self.friends_parent,
            position=(465-450, 17),
            size=(140, 170),
            border_opacity=0.4,
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        self._connected_friends_list_container = None

        # Friend info container
        self._friend_info_container = ocw(
            parent=self.friends_parent,
            position=(615-450, 17),
            size=(175, 170),
            background=False
        )

        iw(
            parent=self.friends_parent,
            position=(160, 17),
            size=(180, 172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'),
            opacity=0.4
        )

        self.friend_info_tip = tw(
            parent=self._friend_info_container,
            size=(165, 170),
            position=(0, 0),
            text=self.language.get_text('FriendsWindow.selectFriendToView'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=160,
            h_align='center',
            v_align='center'
        )

        self.refresh_best_friends_ui()
        self.refresh_best_friends_connected_ui()

    def refresh_best_friends_ui(self):
        """Refresh the best friends list UI."""
        if hasattr(self, "_friends_list_container") and self._friends_list_container and self._friends_list_container.exists():
            self._friends_list_container.delete()

        friends_list = self.get_all_friends()

        if not friends_list:
            # Create a small container
            container_height = 140
            self._friends_list_container = ocw(
                parent=self._friends_scroll_container,
                size=(190, container_height),
                background=False
            )

            # Show default
            default_friend_widget = tw(
                parent=self._friends_list_container,
                size=(170, 30),
                color=self.theme.get_color('COLOR_TERTIARY'),
                text=f"{V2_LOGO}less",
                position=(0, container_height - 30),
                maxwidth=160,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(self._show_friend_popup, (200, 100), delete_user=False)
            )

            # Initialize or clear widget list
            if hasattr(self, '_friend_text_widgets'):
                self._friend_text_widgets.clear()
            else:
                self._friend_text_widgets = []

            # Store only
            self._friend_text_widgets.append(default_friend_widget)

            return

        # Continue with normal friends list
        container_height = max(len(friends_list) * 30, 140)

        self._friends_list_container = ocw(
            parent=self._friends_scroll_container,
            size=(190, container_height),
            background=False
        )

        if not hasattr(self, '_friend_text_widgets'):
            self._friend_text_widgets = []
        else:
            self._friend_text_widgets.clear()

        for i, friend in enumerate(friends_list):
            display_name = friend if len(friend) <= 7 else friend[:7] + "..."
            pos_y = container_height - 30 - 30 * i

            friend_widget = tw(
                parent=self._friends_list_container,
                size=(170, 30),
                color=self.theme.get_color('COLOR_TERTIARY'),
                text=display_name,
                position=(0, pos_y),
                maxwidth=100,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(
                    self._show_friend_popup,
                    (200, 100),
                    friend 
                )
            )

            # Save widget reference
            self._friend_text_widgets.append(friend_widget)

    def refresh_best_friends_connected_ui(self, players_list=None):
        """Refresh the connected best friends list UI."""
        if not (self.friends_parent and self.friends_parent.exists()):
            return

        # Clean up previous no friends online text
        if hasattr(self, 'no_friends_online_text') and self.no_friends_online_text and self.no_friends_online_text.exists():
            self.no_friends_online_text.delete()
            self.no_friends_online_text = None

        if hasattr(self, "_connected_friends_list_container") and self._connected_friends_list_container and self._connected_friends_list_container.exists():
            self._connected_friends_list_container.delete()
            self._connected_friends_list_container = None

        if hasattr(self, '_connected_friend_text_widgets'):
            self._connected_friend_text_widgets.clear()
        else:
            self._connected_friend_text_widgets = []

        # Get players list if not provided
        if players_list is None:
            players_list = [V2_LOGO + player.strip() for player, _ in self._get_filtered_players()]

        # List of best friends online
        real_friends = self.get_all_friends()
        connected_friends = self._get_connected_best_friends(players_list)
        self.best_friends_connected = len(connected_friends)

        # Display message
        if not connected_friends or not real_friends:
            self.no_friends_online_text = tw(
                parent=self.friends_parent,
                position=(60, 90),
                text=self.language.get_text('FriendsWindow.noFriendsOnline'),
                color=self.theme.get_color('COLOR_TERTIARY'),
                maxwidth=120,
                max_height=90,
                h_align='center',
                v_align='center'
            )
            return

        self._connected_friends_list_container = sw(
            parent=self.friends_parent,
            position=(465-450, 17),
            size=(140, 170),
            border_opacity=0.4,
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        container_height = max(len(connected_friends) * 30, 170)
        self._connected_friends_inner_container = ocw(
            parent=self._connected_friends_list_container,
            size=(140, container_height),
            background=False
        )

        # Fill UI with connected names
        for i, friend in enumerate(connected_friends):
            display_name = friend if len(friend) <= 7 else friend[:7] + "..."
            pos_y = container_height - 30 - 30 * i

            connected_widget = tw(
                parent=self._connected_friends_inner_container,
                size=(130, 30),
                color=self.theme.get_color('COLOR_TERTIARY'),
                text=display_name,
                position=(5, pos_y),
                maxwidth=100,
                selectable=True,
                click_activate=True,
                v_align='center',
                on_activate_call=CallStrict(self._display_best_friend_info, friend)
            )

            # Save widget reference
            self._connected_friend_text_widgets.append(connected_widget)

    def get_all_friends(self) -> list[str]:
        """Return the list of all real friend names from storage (excluding default 'less')."""
        try:
            friends = load_friends()
            # Filter out the default
            return [friend["name"] for friend in friends if friend["name"] != "less"]
        except Exception as e:
            print(f"Error loading friends: {e}")
            return []

    def _get_connected_best_friends(self, players_list: list[str] | None = None) -> list[str]:
        """Get list of best friends that are currently connected."""
        try:
            best_friends = self.get_all_friends()
            connected_best_friends = []

            if not players_list:
                return []

            # Create a set for efficient search
            best_friends_set = set(best_friends)
            
            for player in players_list:
                # Check if player is in friends list
                if player in best_friends_set:
                    connected_best_friends.append(player)
                    
                # Also check with prefix
                clean_player = player.lstrip(V2_LOGO)
                if clean_player in best_friends_set:
                    connected_best_friends.append(player)

            return list(set(connected_best_friends))
            
        except Exception as e:
            print(f"Error getting connected best friends: {e}")
            return []

    def _show_friend_popup(
        self,
        position: tuple[float, float],
        friend: str | None = None,
        delete_user: bool = True
    ):
        viewProfileText = self.language.get_text('FriendsWindow.viewProfile')
        deleteText = self.language.get_text('FriendsWindow.deleteFriend')

        choices = [viewProfileText]
        if friend is not None and delete_user:
            choices.append(deleteText)

        popup = PopupMenuWindow(
            position=position,
            choices=choices,
            current_choice="",
            delegate=self,
            width=1,
        )

        # View profile button
        bw(
            parent=popup.root_widget,
            position=(0, 60 if friend is not None and delete_user else 0),
            size=(140, 54),
            label=viewProfileText,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                popup.root_widget.delete(),
                ProfileSearchWindow(
                    self.friends_parent,
                    v2=friend.replace(V2_LOGO, '') if friend else None
                )
            )
        )

        # Delete friend button
        if friend is not None and delete_user:
            bw(
                parent=popup.root_widget,
                position=(0, 0),
                size=(140, 54),
                label=deleteText,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=lambda: (
                    popup.root_widget.delete(),
                    self._delete_friend(friend),
                    self.refresh_best_friends_ui(),
                    self.refresh_best_friends_connected_ui(),
                    self._show_friend_info_tip()
                )
            )

        self._popup_target = friend

    def _show_friend_info_tip(self):
        """Show the friend info tip message."""
        [element.delete() for element in self.best_friends_elements]
        self.best_friends_elements.clear()

        # Create or update the tip
        if self._friend_info_container and self._friend_info_container.exists():
            self.friend_info_tip = tw(
                parent=self._friend_info_container,
                size=(165, 170),
                position=(0, 0),
                text=self.language.get_text('FriendsWindow.selectFriendToView'),
                color=self.theme.get_color('COLOR_PRIMARY'),
                maxwidth=160,
                h_align='center',
                v_align='center'
            )

        # Reset the reference of the friend shown
        self._current_displayed_best_friend = None

    def _display_best_friend_info(self, player_name):
        """Display information about a best friend."""
        # Clean the player name
        clean_player_name = player_name.lstrip(V2_LOGO)

        # Clean UI
        [element.delete() for element in self.best_friends_elements]
        self.best_friends_elements.clear()
        if self.friend_info_tip and self.friend_info_tip.exists():
            self.friend_info_tip.delete()

        self._current_displayed_best_friend = player_name
        server_info = None
        server_address = None
        server_port = None

        # Search in current server memory if available
        try:
            cls = FinderWindow

            for server in cls.SERVER_MEMORY:
                for roster_entry in server.get('roster', []):
                    spec_data = self._safe_load_spec(roster_entry.get('spec', ''))
                    if not spec_data:
                        continue

                    if spec_data.get('n') == clean_player_name or spec_data.get('n') == player_name:
                        server_info = server
                        server_address = server['a']
                        server_port = server['p']
                        break
                if server_info:
                    break
        except:
            pass
        
        # HEADER
        friend_name_widget = tw(
            parent=self._friend_info_container,
            position=(10, 140),
            h_align='left',
            v_align='center',
            maxwidth=90,
            text=f"{V2_LOGO}{clean_player_name}",
            color=self.theme.get_color('COLOR_PRIMARY'),
            size=(155, 25),
            selectable=True,
            click_activate=True,
            glow_type='uniform',
            on_activate_call=CallStrict(self._copy_to_clipboard, clean_player_name)
        )
        self.best_friends_elements.append(friend_name_widget)

        more_info_account = obw(
            parent=self._friend_info_container,
            label='',
            size=(25, 25),
            position=(135, 140),
            texture=gt('cuteSpaz'),
            selectable=False,
            color=(1,1,1),
            enable_sound=False,
            on_activate_call=lambda: ProfileSearchWindow(more_info_account, v2=clean_player_name)
        )

        self.best_friends_elements.append(more_info_account)

        # Divider
        header_divider = iw(
            parent=self._friend_info_container,
            size=(155, 2),
            position=(10, 135), 
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )
        self.best_friends_elements.append(header_divider)

        # Server name
        server_name = server_info['n'] if server_info else 'N/A'
        server_name_widget = tw(
            parent=self._friend_info_container,
            position=(10, 115-20),
            h_align='left',
            v_align='center',
            maxwidth=155,
            text=server_name,
            color=self.theme.get_color('COLOR_PRIMARY'),
            size=(155, 25),
            selectable=True,
            click_activate=True,
            glow_type='uniform',
            on_activate_call=CallStrict(self._copy_to_clipboard, server_name)
        )
        self.best_friends_elements.append(server_name_widget)

        # IP and Port on the same line
        if server_address and server_port:
            # IP widget
            ip_widget = tw(
                parent=self._friend_info_container,
                position=(10, 90-20),
                h_align='left',
                v_align='center',
                maxwidth=100,
                text=server_address,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(100, 25),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, server_address)
            )
            self.best_friends_elements.append(ip_widget)

            # Separator between IP and port
            separator = tw(
                parent=self._friend_info_container,
                position=(112, 90-20),
                text=":",
                color=self.theme.get_color('COLOR_PRIMARY'),
                scale=1.0
            )
            self.best_friends_elements.append(separator)

            # Port widget
            port_widget = tw(
                parent=self._friend_info_container,
                position=(120, 90-20),
                h_align='left',
                v_align='center',
                maxwidth=45,
                text=str(server_port),
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(45, 25),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, str(server_port))
            )
            self.best_friends_elements.append(port_widget)
        else:
            # Show "N/A" for both if not available
            na_widget = tw(
                parent=self._friend_info_container,
                position=(10, 90-20),
                h_align='left',
                v_align='center',
                maxwidth=155,
                text="N/A",
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(155, 25),
                selectable=False
            )
            self.best_friends_elements.append(na_widget)

        connect_text = self.language.get_text('Global.connect')
        delete_text = self.language.get_text('FriendsWindow.deleteFriend')

        # Divider
        button_divider = iw(
            parent=self._friend_info_container,
            size=(165, 1),
            position=(10, 65),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )
        self.best_friends_elements.append(button_divider)

        if server_info and server_address and server_port:
            # Friend is online
            connect_button = bw(
                parent=self._friend_info_container,
                position=(10, 35),
                size=(150, 25),
                label=connect_text,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(self._connect_to_server, server_address, int(server_port), False)
            )
            self.best_friends_elements.append(connect_button)

            delete_button = bw(
                parent=self._friend_info_container,
                position=(10, 5),
                size=(150, 25),
                label=delete_text,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(lambda: (
                    self._delete_friend(player_name),
                    self.refresh_best_friends_ui(),
                    self.refresh_best_friends_connected_ui(),
                    self._show_friend_info_tip()
                ))
            )
            self.best_friends_elements.append(delete_button)
        else:
            # Friend is offline
            delete_button = bw(
                parent=self._friend_info_container,
                position=(12, 35),
                size=(150, 25),
                label=delete_text,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(lambda: (
                    self._delete_friend(player_name),
                    self.refresh_best_friends_ui(),
                    self.refresh_best_friends_connected_ui(),
                    self._show_friend_info_tip()
                ))
            )
            self.best_friends_elements.append(delete_button)

    def _safe_load_spec(self, spec_str):
        """Safely load spec dictionary from JSON string."""
        if not spec_str:
            return None

        try:
            from json import loads
            try:
                return loads(spec_str)
            except:
                cleaned_spec = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', spec_str)
                return loads(cleaned_spec)
        except Exception as e:
            return None

    def _copy_to_clipboard(self, text):
        """Copy text to clipboard and show confirmation."""
        try:
            COPY(text)
            TIP(get_lang_text('Global.copiedToClipboard'))
        except:
            pass

    def popup_menu_closing(self, popup_window) -> None:
        """Handle popup menu closing."""
        self._popup_target = None

    def get_connected_count(self):
        """Get the current count of connected friends."""
        return self.best_friends_connected

    def update_connected_count_display(self, count_widget):
        """Update the connected count display widget."""
        if count_widget and count_widget.exists():
            tw(edit=count_widget, text=str(self.best_friends_connected))

    def _subscribe_language(self, text_key, callback):
        """Subscribe to a text callback and save the reference."""
        self.language.subscribe(text_key, callback)
        self._language_subscriptions.append((text_key, callback))

    def _subscribe_color(self, color_name, callback):
        """Subscribe to a color callback and save the reference."""
        self.theme.subscribe(color_name, callback)
        self._color_subscriptions.append((color_name, callback))

    def _setup_language_subscriptions(self):
        """Configure all language subscriptions."""
        self._subscribe_language('Global.online', self._update_online_friends_text)
        self._subscribe_language('FriendsWindow.allFriends', self._update_all_friends_text)
        self._subscribe_language('FriendsWindow.addManually', self._update_add_manual_button_text)
        self._subscribe_language('FriendsWindow.selectFriendToView', self._update_friend_info_tip_text)
        self._subscribe_language('FriendsWindow.noFriendsOnline', self._update_no_friends_online_text)
        self._subscribe_language('FriendsWindow.noFriendsAdded', self._update_no_friends_added_text)

    def _setup_color_subscriptions(self):
        """Configure all color subscriptions."""
        self._subscribe_color('COLOR_BACKGROUND', self._update_friends_background_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_friends_separator_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_friends_separator2_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_all_friends_text_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_friend_input_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_online_friends_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_add_manual_button_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_add_manual_button_textcolor)
        self._subscribe_color('COLOR_SECONDARY', self._update_friends_scroll_container_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_connected_friends_scroll_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_friend_info_container_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_friend_info_tip_color)
        self._subscribe_color('COLOR_TERTIARY', self._update_no_friends_online_color)
        self._subscribe_color('COLOR_TERTIARY', self._update_friend_text_widgets_color)
        self._subscribe_color('COLOR_TERTIARY', self._update_connected_friend_text_widgets_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_best_friends_info_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_best_friends_info_button_color)

    # Language update methods
    def _update_online_friends_text(self, new_text):
        """Update online friends text."""
        if hasattr(self, 'online_friends_text') and self.online_friends_text and self.online_friends_text.exists():
            tw(edit=self.online_friends_text, text=new_text + "\ue019")

    def _update_all_friends_text(self, new_text):
        """Update 'All Friends' text."""
        if hasattr(self, 'all_friends_text') and self.all_friends_text and self.all_friends_text.exists():
            tw(edit=self.all_friends_text, text=new_text)

    def _update_add_manual_button_text(self, new_text):
        """Update the text of the 'Add Manually' button."""
        if hasattr(self, 'add_manual_button') and self.add_manual_button and self.add_manual_button.exists():
            obw(edit=self.add_manual_button, label=new_text)

    def _update_friend_info_tip_text(self, new_text):
        """Update friend information tip text."""
        if hasattr(self, 'friend_info_tip') and self.friend_info_tip and self.friend_info_tip.exists():
            tw(edit=self.friend_info_tip, text=new_text)

    def _update_no_friends_online_text(self, new_text):
        """Update 'No Friends Online' text."""
        if hasattr(self, 'no_friends_online_text') and self.no_friends_online_text and self.no_friends_online_text.exists():
            tw(edit=self.no_friends_online_text, text=new_text)

    def _update_no_friends_added_text(self, new_text):
        """Update 'No Friends Added' text."""
        # This updates the text in the friends list when empty
        # We need to find and update the text widget in _friends_list_container
        if hasattr(self, '_friends_list_container') and self._friends_list_container and self._friends_list_container.exists():
            # Find text widgets in the container
            children = self._friends_list_container.get_children()
            for child in children:
                if hasattr(child, 'get_text'):
                    current_text = child.get_text()
                    if current_text and ('noFriends' in current_text or 'No friends' in current_text):
                        tw(edit=child, text=new_text)

    # Color update methods
    def _update_friends_background_color(self, new_color):
        """Update the background color of the Friends panel."""
        if hasattr(self, 'friends_background') and self.friends_background and self.friends_background.exists():
            iw(edit=self.friends_background, color=new_color)

    def _update_friends_separator_color(self, new_color):
        """Update the color of the friends panel separator."""
        if hasattr(self, 'friends_separator') and self.friends_separator and self.friends_separator.exists():
            iw(edit=self.friends_separator, color=new_color)

    def _update_friends_separator2_color(self, new_color):
        """Update color of second separator."""
        if hasattr(self, 'friends_separator2') and self.friends_separator2 and self.friends_separator2.exists():
            iw(edit=self.friends_separator2, color=new_color)

    def _update_all_friends_text_color(self, new_color):
        """Update the color of the 'All Friends' text."""
        if hasattr(self, 'all_friends_text') and self.all_friends_text and self.all_friends_text.exists():
            tw(edit=self.all_friends_text, color=new_color)

    def _update_friend_input_color(self, new_color):
        """Update the color of the friends input."""
        if hasattr(self, 'friend_input') and self.friend_input and self.friend_input.exists():
            tw(edit=self.friend_input, color=new_color)

    def _update_online_friends_color(self, new_color):
        """Update the color of the 'Online Friends' text."""
        if hasattr(self, 'online_friends_text') and self.online_friends_text and self.online_friends_text.exists():
            tw(edit=self.online_friends_text, color=new_color)

    def _update_add_manual_button_color(self, new_color):
        """Update color of 'Add Manually' button."""
        if hasattr(self, 'add_manual_button') and self.add_manual_button and self.add_manual_button.exists():
            obw(edit=self.add_manual_button, color=new_color)

    def _update_add_manual_button_textcolor(self, new_color):
        """Update the text color of the 'Add Manually' button."""
        if hasattr(self, 'add_manual_button') and self.add_manual_button and self.add_manual_button.exists():
            obw(edit=self.add_manual_button, textcolor=new_color)

    def _update_friends_scroll_container_color(self, new_color):
        """Update the color of the friends scroll container."""
        if hasattr(self, '_friends_scroll_container') and self._friends_scroll_container and self._friends_scroll_container.exists():
            sw(edit=self._friends_scroll_container, color=new_color)

    def _update_connected_friends_scroll_color(self, new_color):
        """Update the color of the connected friends scroll container."""
        if hasattr(self, '_connected_friends_scroll_container') and self._connected_friends_scroll_container and self._connected_friends_scroll_container.exists():
            sw(edit=self._connected_friends_scroll_container, color=new_color)

    def _update_friend_info_container_color(self, new_color):
        """Update the color of the friends info container."""
        if hasattr(self, '_friend_info_container') and self._friend_info_container and self._friend_info_container.exists():
            sw(edit=self._friend_info_container, color=new_color)

    def _update_friend_info_tip_color(self, new_color):
        """Update friend info tip color."""
        if hasattr(self, 'friend_info_tip') and self.friend_info_tip and self.friend_info_tip.exists():
            tw(edit=self.friend_info_tip, color=new_color)

    def _update_no_friends_online_color(self, new_color):
        """Update the text color of 'No Friends Online'."""
        if hasattr(self, 'no_friends_online_text') and self.no_friends_online_text and self.no_friends_online_text.exists():
            tw(edit=self.no_friends_online_text, color=new_color)

    def _update_friend_text_widgets_color(self, new_color):
        """Update the text color in the friends list."""
        if hasattr(self, '_friend_text_widgets'):
            for widget in self._friend_text_widgets:
                if widget and widget.exists():
                    tw(edit=widget, color=new_color)

    def _update_connected_friend_text_widgets_color(self, new_color):
        """Update the color of the text in the online friends list."""
        if hasattr(self, '_connected_friend_text_widgets'):
            for widget in self._connected_friend_text_widgets:
                if widget and widget.exists():
                    tw(edit=widget, color=new_color)

    def _update_best_friends_info_color(self, new_color):
        """Update color of best friends info elements."""
        if hasattr(self, '_current_displayed_best_friend') and self._current_displayed_best_friend:
            self._display_best_friend_info(self._current_displayed_best_friend)

    def _update_best_friends_info_button_color(self, new_color):
        """Update background color of best friends buttons."""
        if hasattr(self, '_current_displayed_best_friend') and self._current_displayed_best_friend:
            self._display_best_friend_info(self._current_displayed_best_friend)

    def cleanup(self):
        """Clean up all subscriptions and references."""
        # Unsubscribe from language updates
        for text_key, callback in self._language_subscriptions:
            self.language.unsubscribe(text_key, callback)
        self._language_subscriptions.clear()

        # Unsubscribe from color updates
        for color_name, callback in self._color_subscriptions:
            self.theme.unsubscribe(color_name, callback)
        self._color_subscriptions.clear()

class FinderWindow:
    """Less Finder."""

    language = ReactiveLanguage() 
    theme = ReactiveTheme()

    # Server connection constants
    SPEC = {"s":"{\"n\":\"Finder\",\"a\":\"\",\"sn\":\"\"}","d":"69"*20}
    AUTH = {'b': app.env.engine_build_number, 'tk': '', 'ph': ''}

    # UI state variables
    MAX_PING = 0.3
    TOP_SERVERS = 1
    SERVER_MEMORY = []
    ART_DISPLAY = []
    BEST_SERVERS = []
    IS_SCANNING = False
    SERVER_LIST_ELEMENTS = []
    PLAYERS_LIST = []
    ART_DISPLAY_WIDGET = None
    SCROLL_WIDGET = None
    TIP_WIDGET = None
    FILTER_TEXT = ''
    FILTER_TEXT_WIDGET = None
    FILTER_UPDATER = None
    SHOWING_SERVER_ART = False 
    SHOWING_SERVER_INFO = False

    def __init__(self, source):
        """Initialize the Server Finder UI."""
        
        self.theme.refresh_from_config()
        self._current_selected_player = None
        self._current_displayed_player = None 
        self._language_subscriptions = []
        self._color_subscriptions = [] 
        self.scan_threads = []
        self.info_elements = []
        self.progress_trackers = []
        self.status_updater = None
        self.background_sound = self._play_sound('powerup01')
        
        cls = self.__class__
        
        # Create main window
        window_size = (800, 435)
        borders = BorderWindow(window_size)

        cls.root = cw(
            scale_origin_stack_offset=source.get_screen_space_center(),
            size=window_size,
            oac=self.close_interface,
        )[0]

        self.footer = obw(
            parent=cls.root,
            size=window_size,
            texture=gt('empty'),
            label='',
            enable_sound=False
        )

        # Create main content area
        content_size = (460, 435)
        cls.MainParent = ocw(
            position=(0, 0),
            parent=cls.root,
            size=content_size,
            background=False
        )

        # Background
        iw(
            parent=cls.MainParent,
            size=content_size,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_BACKGROUND')
        )

        # Window border
        sw(
            parent=cls.MainParent,
            size=content_size,
            border_opacity=0
        )

        # Create friends panel
        self.friends_panel = FriendsWindow(
            parent_widget=cls.root,
            theme=self.theme,
            language=self.language,
            get_filtered_players_callback=self._get_filtered_players,
            add_friend_callback=self._add_friend,
            delete_friend_callback=self._delete_friend,
            connect_callback=CON
        )

        options_button = obw(
            parent=cls.MainParent,
            label='',
            size=(45, 45),
            position=(350, 390),
            texture=gt('menuButton'),
            selectable=False,
            color=(1,1,1),
            enable_sound=False,
            on_activate_call=lambda: self._show_options_popup(options_button)
        )

        # Friends connected button
        friends_connected_btn = obw(
            parent=cls.MainParent,
            label='',
            size=(45, 45),
            position=(400, 390),
            texture=gt('usersButton'),
            selectable=False,
            color=(1,1,1),
            enable_sound=False
        )

        # Friends connected count
        connected_count = self.friends_panel.get_connected_count() if hasattr(self, 'friends_panel') else 0
        self.connected_users_count = tw(
            parent=cls.MainParent,
            text=str(connected_count),
            size=(0, 0),
            position=(400 + 21, 390 + 16),
            h_align="center",
            v_align="center",
            scale=0.6,
            color=(0, 1, 0, 1),
            draw_controller=friends_connected_btn  
        )

        # Search section header
        self.search_servers_text = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.searchServers'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(19, 359),
            maxwidth = 320,
            max_height=28,
        )

        # Search button
        self.search_button = bw(
            parent=cls.MainParent,
            position=(360, 343),
            size=(80, 39),
            text_scale=0.7,
            label=self.language.get_text('Global.search'),
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=self.start_server_scan
        )

        # Search description
        self.search_players_text = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.searchPlayers'),
            color=self.theme.get_color('COLOR_TERTIARY'),
            scale=0.8,
            position=(15, 330),
            maxwidth = 320,
            max_height=28,
        )
        
        # Separator
        iw(
            parent=cls.MainParent,
            size=(429, 1),
            position=(17, 330),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        # Art display area
        cls.ART_DISPLAY_WIDGET = tw(
            parent=cls.MainParent,
            text=self.language.get_text('FinderWindow.pressSearch'),
            maxwidth=430,
            max_height=125,
            h_align='center',
            v_align='top',
            color=self.theme.get_color('COLOR_PRIMARY'),
            position=(205, 260),
        )

        # Separator
        iw(
            parent=cls.MainParent,
            size=(429, 1),
            position=(17, 200),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_SECONDARY')
        )

        # Filter input
        cls.FILTER_TEXT_WIDGET = tw(
            parent=cls.MainParent,
            position=(23, 150),
            size=(201, 35),
            text=cls.FILTER_TEXT,
            editable=True,
            glow_type='uniform',
            allow_clear_button=False,
            v_align='center',
            color=self.theme.get_color('COLOR_PRIMARY'),
            description=get_lang_text('FinderWindow.filterDescription')
        )

        search = get_lang_text('Global.search')
        self.filter_placeholder = tw(
            parent=cls.MainParent,
            position=(26, 153),
            text=search,
            maxwidth = 80,
            max_height=25,
            color=self.theme.get_color('COLOR_TERTIARY')
        )
        
        # Players list container
        self.players_parent = sw(
            parent=cls.MainParent,
            position=(20, 18),
            size=(205, 122),
            border_opacity=0.4,
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        cls.MainParent2 = ocw(
            parent=self.players_parent,
            size=(205, 1),
            background=False
        )

        self.players_tip = tw(
            parent=cls.MainParent,
            position=(90, 100),
            text=self.language.get_text('FinderWindow.searchServersForPlayers'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth = 175,
            max_height=100,
            h_align='center'
        )

        # Info panel background
        iw(
            parent=cls.MainParent,
            position=(235, 18),
            size=(205, 172),
            texture=gt('scrollWidget'),
            mesh_transparent=gm('softEdgeOutside'),
            opacity=0.4
        )

        self.border_left = iw(
            parent=cls.root,
            size=borders.border_left.size,
            position=borders.border_left.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_top = iw(
            parent=cls.root,
            size = (borders.border_top.size[0] + 12, borders.border_top.size[1]),
            position=borders.border_top.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_right = iw(
            parent=cls.root,
            size=borders.border_right.size,
            position=(borders.border_right.position[0] + 12, borders.border_right.position[1]),
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        self.border_bottom = iw(
            parent=cls.root,
            size = (borders.border_bottom.size[0] + 15, borders.border_bottom.size[1]),
            position=borders.border_bottom.position,
            texture=gt('white'),
            color=self.theme.get_color('COLOR_PRIMARY')
        )

        cls.TIP_WIDGET = tw(
            parent=cls.MainParent,
            position=(310, 98),
            text=self.language.get_text('FinderWindow.selectToViewInfo'),
            color=self.theme.get_color('COLOR_PRIMARY'),
            maxwidth=170,
            max_height=100,
            h_align='center'
        )

        self._setup_language_subscriptions()
        self._setup_colors_subscriptions()

        # Final setup
        self._draw_art() if cls.ART_DISPLAY else None
        self._update_players_list()
        cls.SCROLL_WIDGET and self._display_server_info(cls.SCROLL_WIDGET)
        cls.FILTER_UPDATER = tuck(0.1, self._update_filter, repeat=True)

    def _subscribe_language(self, text_key, callback):
        """Subscribe to a text callback and save the reference."""
        self.language.subscribe(text_key, callback)
        self._language_subscriptions.append((text_key, callback))

    def _unsubscribe_all_languages(self):
        """Remove all language subscriptions on close."""
        for text_key, callback in self._language_subscriptions:
            self.language.unsubscribe(text_key, callback)
        self._language_subscriptions.clear()

    def _subscribe_color(self, color_name, callback):
        """Subscribe to a callback and save the reference."""
        self.theme.subscribe(color_name, callback)
        self._color_subscriptions.append((color_name, callback))

    def _unsubscribe_all(self):
        """Remove all subscriptions upon closing."""
        # Unsubscribe from colors
        for color_name, callback in self._color_subscriptions:
            self.theme.unsubscribe(color_name, callback)
        self._color_subscriptions.clear()
        
        # Unsubscribe from languages
        self._unsubscribe_all_languages()
        
        # Clean up friends panel if exists
        if hasattr(self, 'friends_panel'):
            self.friends_panel.cleanup()

    def _update_filter(self):
        """Update the filter text and refresh the display."""
        cls = self.__class__
        if not self.filter_placeholder.exists():
            cls.FILTER_UPDATER = None
            return
            
        current_text = tw(query=cls.FILTER_TEXT_WIDGET)
        search = get_lang_text('Global.search')
        tw(self.filter_placeholder, text=[search,''][bool(current_text)])
        
        if current_text != self.FILTER_TEXT:
            cls.FILTER_TEXT = current_text
            self._update_players_list()

    def _on_server_select(self, index, player_name):
        """Handle server selection in the list."""
        cls = self.__class__
        cls.SCROLL_WIDGET = player_name
        self._current_selected_player = player_name 

        # Update colors immediately
        for i, element in enumerate(cls.SERVER_LIST_ELEMENTS):
            if element and element.exists():
                color = self.theme.get_color('COLOR_PRIMARY') if i == index else self.theme.get_color('COLOR_TERTIARY')
                tw(edit=element, color=color)

        self._display_server_info(player_name)

    def _display_server_info(self, player_name):
        """Display detailed information about the selected server."""
        [element.delete() for element in self.info_elements]
        self.info_elements.clear()
        cls = self.__class__
        tw(cls.TIP_WIDGET, text='')

        cls.SHOWING_SERVER_INFO = True
        self._current_displayed_player = player_name

        server_info = None
        for server in cls.SERVER_MEMORY:
            for roster_entry in server.get('roster', []):
                spec_data = self._safe_load_spec(roster_entry.get('spec', ''))
                if not spec_data:
                    continue

                if spec_data.get('n') == player_name:
                    server_info = server
                    player_data = roster_entry['p']
                    break

        if server_info is None:
            cls.SCROLL_WIDGET = None
            cls.SHOWING_SERVER_INFO = False
            tw(cls.TIP_WIDGET, text=self.default_tip_text)
            self._current_displayed_player = None
            return

        # Display server info
        for i, key in enumerate(['n', 'a', 'p']):
            field_text = str(server_info[key])
            pos_x = [250, 245, 375][i]
            pos_y = [155, 115][bool(i)]
            size_x = [175, 115, 55][i]

            text_widget = tw(
                parent=cls.MainParent,
                position=(pos_x, pos_y),
                h_align='center',
                v_align='center',
                maxwidth=size_x,
                text=field_text,
                color=self.theme.get_color('COLOR_PRIMARY'),
                size=(size_x, 30),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                on_activate_call=CallStrict(self._copy_to_clipboard, field_text)
            )
            self.info_elements.append(text_widget)

        account_v2 = [str(list(player.values())[1]) for player in player_data]

        account_button = bw(
            parent=cls.MainParent,
            position=(253, 65),
            size=(170, 30),
            label=str(account_v2[0]) if account_v2 and account_v2[0] != [] else player_name,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=CallStrict(self._show_notification, '\n'.join([' | '.join([str(j) for j in player.values()]) for player in player_data]) or 'Nothing')
        )
        self.info_elements.append(account_button)

        connect = get_lang_text('Global.connect')
        if account_v2 and str(account_v2[0]).startswith(V2_LOGO):
            # Show both buttons side by side for v2 accounts
            connect_button = bw(
                parent=cls.MainParent,
                position=(250, 30),
                size=(80, 30),
                label=connect,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(CON, server_info['a'], server_info['p'], False)
            )
            self.info_elements.append(connect_button)

            addFriend = get_lang_text('FriendsWindow.addFriend')
            add_friend_button = bw(
                parent=cls.MainParent,
                position=(340, 30),
                size=(87, 30),
                label=addFriend,
                text_scale=0.5,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(lambda: (
                    self._add_friend(player_name),
                    self._update_friends_panel()
                ))
            )
            self.info_elements.append(add_friend_button)
        else:
            connect_button = bw(
                parent=cls.MainParent,
                position=(253, 30),
                size=(170, 30),
                label=connect,
                color=self.theme.get_color('COLOR_SECONDARY'),
                textcolor=self.theme.get_color('COLOR_PRIMARY'),
                oac=CallStrict(CON, server_info['a'], server_info['p'], False)
            )
            self.info_elements.append(connect_button)

    def _update_friends_panel(self):
        """Update the friends panel after changes."""
        if hasattr(self, 'friends_panel'):
            self.friends_panel.refresh_best_friends_ui()
            players_list = [V2_LOGO + player.strip() for player, _ in self._get_filtered_players()]
            self.friends_panel.refresh_best_friends_connected_ui(players_list)
            self.friends_panel.update_connected_count_display(self.connected_users_count)

    def _show_options_popup(self, source_button):
        """Show options popup with profile search and color picker."""
        searchProfiles = get_lang_text('FinderWindow.searchProfiles')
        changeColors = get_lang_text('FinderWindow.changeColors')
        changeLanguage = get_lang_text('FinderWindow.changeLanguage')
        creditsText = get_lang_text('Global.credits')
        
        x = source_button.get_screen_space_center()[0]
        y = source_button.get_screen_space_center()[1] - 70
        popup = PopupMenuWindow(
            position=(x, y),
            choices=[searchProfiles, changeColors, changeLanguage, creditsText],
            current_choice="",
            delegate=self,
            width=1,
        )

        # Search profiles button
        bw(
            parent=popup.root_widget,
            position=(-100, 55+50),
            size=(180, 50),
            label=searchProfiles,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                popup.root_widget.delete(),
                self._search_profiles() 
            )
        )

        # Change colors button
        bw(
            parent=popup.root_widget,
            position=(-100, 0+50),
            size=(180, 50),
            label=changeColors,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                popup.root_widget.delete(),
                self._create_color_picker(
                    position=(self.root.get_screen_space_center()),
                    initial_color=self.theme.get_color('COLOR_ACCENT'),
                    call='color',
                )
            )
        )

        # Change lang button
        bw(
            parent=popup.root_widget,
            position=(-100, -55+50),
            size=(180, 50),
            label=changeLanguage,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                popup.root_widget.delete(),
                self._translate_window()
            )
        )

        bw(
            parent=popup.root_widget,
            position=(-100, -110+50),
            size=(180, 50),
            label=creditsText,
            color=self.theme.get_color('COLOR_SECONDARY'),
            textcolor=self.theme.get_color('COLOR_PRIMARY'),
            oac=lambda: (
                popup.root_widget.delete(),
                self._credits()
            )
        )

        self._popup_target = "options"

    def _search_profiles(self):
        """Open the profile search window."""
        source_widget = self.__class__.root if hasattr(self.__class__, 'root') and self.__class__.root.exists() else zw('overlay_stack')
        ProfileSearch(source_widget)
    
    def _translate_window(self):
        """Create language selection popup."""
        popup_size = (250, 300)
        popup_window = ocw(
            parent=zw('overlay_stack'),
            size=popup_size,
            background=False,
            transition='in_scale',
            on_outside_click_call=lambda: popup_window.delete()
        )
    
        # Popup background
        iw(
            parent=popup_window,
            size=popup_size,
            texture=gt('softRect'),
            color=self.theme.get_color('COLOR_BACKGROUND'),
            opacity=0.95
        )
    
        languages_to_show = get_languages_for_current_platform()
        if (APP.classic.platform != 'android'):
            tw(
                parent=popup_window,
                text="",
                position=(popup_size[0]/2, popup_size[1]-20),
                h_align='center',
                scale=0.6,
                color=(0.7, 0.7, 0.7, 1)
            )

        scroll_container = sw(
            parent=popup_window,
            position=(25, 50),
            size=(200, 200),
            border_opacity=0.3,
            color=self.theme.get_color('COLOR_SECONDARY')
        )
    
        languages_container = ocw(
            parent=scroll_container,
            size=(180, len(languages_to_show) * 55),
            background=False
        )
    
        # Get current language from settings
        current_lang_id = get_app_lang_as_id()
        current_lang_name = get_language_name(current_lang_id)
    
        # Color for current language
        CURRENT_LANG_COLOR = self.theme.get_color('COLOR_TERTIARY')
        NORMAL_LANG_COLOR = self.theme.get_color('COLOR_SECONDARY')
    
        # Create buttons for each language
        for i, (lang_id, lang_name) in enumerate(languages_to_show.items()):
            y_position = (len(languages_to_show) - i - 1) * 55
    
            # Determine color based on whether it is the current language
            is_current = lang_id == current_lang_id
            button_color = CURRENT_LANG_COLOR if is_current else NORMAL_LANG_COLOR
            text_color = (0, 0, 0, 1) if is_current else self.theme.get_color('COLOR_PRIMARY')
    
            # Language button
            lang_button = bw(
                parent=languages_container,
                position=(10, y_position + 10),
                size=(160, 45),
                label=lang_name,
                color=button_color,
                textcolor=text_color,
                oac=lambda lid=lang_id, lname=lang_name: self._select_language(lid, lname, popup_window)
            )
    
            # Current language indicator
            if is_current:
                tw(
                    parent=languages_container,
                    text='✓',
                    position=(150, y_position + 25),
                    h_align='center',
                    scale=1.5,
                    color=(0, 0, 0, 1)
                )

            if (APP.classic.platform != 'android') and not DEFAULT_LANGUAGES_DICT[lang_id]["pc_compatible"]:
                tw(
                    parent=languages_container,
                    text='⚠',
                    position=(140, y_position + 25),
                    h_align='center',
                    scale=0.8,
                    color=(1, 0.5, 0, 1)
                )
    
    def _select_language(self, lang_id: str, lang_name: str, popup_window):
        """Handle language selection."""

        update_finder_config(CFG_NAME_PREFFERED_LANG, lang_id)
        self.language.update_language(lang_id)
    
        confirmation_texts = {
            'id': f'Bahasa diubah ke: {lang_name}',
            'en': f'Language changed to: {lang_name}',
            'hi': f'भाषा बदली गई: {lang_name}',
            'es': f'Idioma cambiado a: {lang_name}',
            'ml': f'ഭാഷ മാറ്റി: {lang_name}'
        }
    
        TIP(confirmation_texts.get(lang_id, confirmation_texts['en']))
        popup_window.delete()


    def _credits(self):
        """Open Creditr."""
        source_widget = self.__class__.root if hasattr(self.__class__, 'root') and self.__class__.root.exists() else zw('overlay_stack')
        CreditsWindow(source_widget)

    #def _reload_interface(self):
    #    """Reload the interface to apply language changes."""
    #    self.close_interface()
    #    def reload():
    #        load_finder_config()
    #        #teck(0.1, byLess.activate_button)
    #    teck(0.2, reload)

    def _generate_theme_from_color(self, base_color):
        """Generate a color theme based on a base color."""
        def adjust_color(color, factor):
            return tuple(max(0.0, min(1.0, c * factor)) for c in color)

        base = tuple(base_color)

        return {
            CFG_NAME_COLOR_BACKGROUND: (0.1, 0.1, 0.1),
            CFG_NAME_COLOR_SECONDARY: (0.2, 0.2, 0.2),
            CFG_NAME_COLOR_TERTIARY: adjust_color(base, 0.6),
            CFG_NAME_COLOR_PRIMARY: base,
            CFG_NAME_COLOR_ACCENT: adjust_color(base, 1.2),
        }

    def _create_color_picker(self, position, initial_color, call):
        """Create a color picker dialog."""
        self._initial_picker_color = initial_color
        self._color_changed = False
        return colorpicker.ColorPicker(
            parent=self.root,
            position=position,
            initial_color=initial_color,
            delegate=self,
            tag=call,
        )
    
    def _save_colors_to_config(self, colors: dict):
        """Save colors to the configuration using finder_config."""
        # Update finder_config with the new colors
        for color_key, color_value in colors.items():
            finder_config[color_key] = tuple(color_value)
        
        # Save the settings
        save_finder_config(finder_config)
        
        # Update the reactive theme
        self.theme.update_colors({
            'COLOR_BACKGROUND': tuple(finder_config.get(CFG_NAME_COLOR_BACKGROUND)),
            'COLOR_SECONDARY': tuple(finder_config.get(CFG_NAME_COLOR_SECONDARY)),
            'COLOR_TERTIARY': tuple(finder_config.get(CFG_NAME_COLOR_TERTIARY)),
            'COLOR_PRIMARY': tuple(finder_config.get(CFG_NAME_COLOR_PRIMARY)),
            'COLOR_ACCENT': tuple(finder_config.get(CFG_NAME_COLOR_ACCENT))
        })

    def color_picker_selected_color(self, picker, color):
        """Handle color selection from color picker."""
        tag = picker.get_tag()
        theme = self._generate_theme_from_color(color)

        # Check if the color actually changed
        if color != self._initial_picker_color:
            self._color_changed = True

            # Save to new configuration
            self._save_colors_to_config(theme)

            if tag == 'color':
                self._main_color = tuple(color)

    def color_picker_closing(self, picker):
        """Handle color picker closing."""
        if self._color_changed:
            TIP("Colors updated successfully!")

    def popup_menu_closing(self, popup_window) -> None:
        """Handle popup menu closing."""
        self._popup_target = None

    def on_popup_cancel(self):
        """Handle popup cancellation."""
        pass

    def _show_notification(self, text):
        """Show a notification message."""
        TIP(text)
        self._play_ding_sound(1, 1)

    def _copy_to_clipboard(self, text):
        """Copy text to clipboard and show confirmation."""
        self._play_ding_sound(1, 1)
        TIP(get_lang_text('Global.copiedToClipboard'))
        COPY(text)

    def _get_filtered_players(self):
        """Get list of filtered players from servers."""
        player_list = []
        cls = self.__class__

        for server in cls.SERVER_MEMORY:
            address = server['a']
            roster = server.get('roster', {})

            if roster:
                for player in roster:
                    player_spec = self._safe_extract_player_spec(player)
                    if not player_spec:
                        continue
                    
                    # Skip if player is Finder or doesn't match filter
                    if (player_spec == 'Finder' or
                        (cls.FILTER_TEXT and not self._check_server_against_filter(roster))):
                        continue
                    player_list.append((player_spec, address))

        return sorted(player_list, key=lambda x: x[0].startswith('Server'))

    def _safe_extract_player_spec(self, player_data):
        """Extract the player's name safely."""
        try:
            spec_str = player_data.get('spec', '')
            if not spec_str:
                return None

            try:
                spec_data = loads(spec_str)
                return spec_data.get('n', '')
            except JSONDecodeError:
                match = re.search(r'"n"\s*:\s*"([^"]*)"', spec_str)
                if match:
                    return match.group(1)

                match = re.search(r'"name"\s*:\s*"([^"]*)"', spec_str)
                if match:
                    return match.group(1)

                return None

        except Exception as e:
            print(f"Safe error extracting player spec: {e}")
            return None

    def _check_server_against_filter(self, roster):
        """Check if server matches current filter text."""
        filter_text = self.__class__.FILTER_TEXT.lower()
        
        for player in roster:
            player_name = self._safe_extract_player_spec(player)
            if player_name and player_name != 'Finder' and filter_text in player_name.lower():
                return True
                
            for profile in player['p']:
                if filter_text in profile['nf'].lower():
                    return True
                        
        return False

    def _safe_load_spec(self, spec_str):
        """Securely load the spec dictionary from a JSON string."""
        if not spec_str:
            return None

        try:
            try:
                return loads(spec_str)
            except JSONDecodeError:
                cleaned_spec = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', spec_str)
                return loads(cleaned_spec)
        except Exception as e:
            return None

    def _play_sound(self, sound_type):
        """Play a sound effect."""
        sound = gs(sound_type)
        sound.play()
        teck(uf(0.14, 0.18), sound.stop)
        return sound

    def close_interface(self):
        """Close the server finder interface."""
        self.background_sound.stop()
        cls = self.__class__
        ocw(cls.root, transition='out_scale')
        laser_sound = self._play_sound('laser')
        self._unsubscribe_all()
        
        def stop_sound_check():
            if cls.root:
                teck(0.01, stop_sound_check)
            else:
                laser_sound.stop()
                
        stop_sound_check()

    def open_interface(self):
        """Open the server finder interface."""
        cls = self.__class__
        ocw(cls.root, transition='in_scale')

    def _play_ding_sound(self, *sound_sequence):
        """Play sequence of ding sounds."""
        sound_sizes = ['Small', '']
        for i, sound_index in enumerate(sound_sequence):
            sound_name = 'ding' + sound_sizes[sound_index]
            if i < (len(sound_sequence) - 1):
                teck(i/10, CallStrict(self._play_sound, sound_name))
            else:
                gs(sound_name).play()

    def start_server_scan(self):
        """Start scanning for servers."""
        cls = self.__class__
        if cls.IS_SCANNING:
            stillBusy = get_lang_text('FinderWindow.stillBusy')
            TIP(stillBusy)
            self._play_ding_sound(0, 0)
            return

        # Reset the state of the art
        cls.SHOWING_SERVER_ART = False
        cls.SHOWING_SERVER_INFO = False 

        scanningServers = get_lang_text('FinderWindow.scanningServers')
        TIP(scanningServers)
        cls.SCAN_START_TIME = time.time()
        self._play_ding_sound(1, 0)
        cls.IS_SCANNING = True

        plus = app.plus
        plus.add_v1_account_transaction(
            {
                'type': 'PUBLIC_PARTY_QUERY',
                'proto': PT(),
                'lang': 'English'
            },
            callback=self._on_server_query_response,
        )
        plus.run_v1_account_transactions()

    def get_all_friends(self) -> list[str]:
        """Return the list of all friend names (new storage)."""
        friends = load_friends()
        return [f["name"] for f in friends]

    def _get_connected_best_friends(self, players_list: list[str] | None = None) -> list[str]:
        """Get list of best friends that are currently connected."""
        best_friends = self.get_all_friends()
        connected_best_friends = []

        if not players_list:
            return []

        for player in players_list:
            if player in best_friends:
                connected_best_friends.append(player)

        return connected_best_friends

    def _add_friend(self, friend: str):
        """Add a friend."""

        if not friend or friend.strip() == "":
            fieldEmpty = get_lang_text('Global.fieldEmpty')
            push(fieldEmpty, (1, 0, 0))
            gs('error').play()
            return

        prefixed_friend = f"{V2_LOGO}{friend.strip()}"

        # Load current friends
        friends = load_friends()

        # Check if already exists
        for f in friends:
            if f["name"] == prefixed_friend:
                TIP(f"{prefixed_friend} {get_lang_text('Global.alreadyInList')}")
                return

        # Generate new ID
        existing_ids = [int(f["id"]) for f in friends if f["id"].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

        # Add friend object
        add_friend(
            name=prefixed_friend,
            friend_id=new_id,
            accounts=[],
            account_pb=None,
            account_id=None
        )

        self._play_ding_sound(1, 0)

        if hasattr(self, 'friends_panel'):
            self.friends_panel.refresh_best_friends_ui()
            players_list = [V2_LOGO + player.strip() for player, _ in self._get_filtered_players()]
            self.friends_panel.refresh_best_friends_connected_ui(players_list)
            self.friends_panel.update_connected_count_display(self.connected_users_count)

        TIP(f"{prefixed_friend} {get_lang_text('Global.addedSuccessfully')}")

    def _delete_friend(self, friend: str):
        """Delete a friend from the friends list (new system)."""

        if not friend or friend.strip() == "":
            fieldEmpty = get_lang_text('Global.fieldEmpty')
            push(fieldEmpty, (1, 0, 0))
            gs('error').play()
            return

        prefixed_friend = friend.strip()

        friends = load_friends()

        # Find by name
        target = None
        for f in friends:
            if f["name"] == prefixed_friend:
                target = f
                break

        if not target:
            TIP(f"{prefixed_friend} not found in list")
            return

        remove_friend(target["id"])

        self._play_ding_sound(0, 1)
        TIP(f"{prefixed_friend} {get_lang_text('Global.deletedSuccessfully')}")

        # Update friends panel
        self._update_friends_panel()

    def _on_server_query_response(self, response):
        """Handle server query response."""
        cls = self.__class__
        cls.SERVER_MEMORY = response['l']
        cls.ART_DISPLAY = [cs(sc.OUYA_BUTTON_U)] * len(cls.SERVER_MEMORY)
        self.scan_threads = []
        
        for i, server in enumerate(cls.SERVER_MEMORY):
            thread = Thread(target=CallStrict(self._ping_server, server, i))
            self.scan_threads.append(thread)
            thread.start()
            
        self.status_updater = tuck(0.01, self._update_ping_status, repeat=True)

    def _ping_server(self, server, index):
        """Ping a server and retrieve its roster."""
        server['ping'], server['roster'] = ping_and_get_roster(
            server['a'], server['p'], pro=self.progress_trackers, dex=index
        )

    def _update_ping_status(self):
        """Update the ping status display."""
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

    def _draw_art(self):
        """Draw the art display showing server status."""
        cls = self.__class__
        art_text = '\n'.join(''.join(cls.ART_DISPLAY[i:i+40]) for i in range(0, len(self.ART_DISPLAY), 40))

        cls.SHOWING_SERVER_ART = True

        if hasattr(cls, 'ART_DISPLAY_WIDGET') and cls.ART_DISPLAY_WIDGET and cls.ART_DISPLAY_WIDGET.exists():
            tw(cls.ART_DISPLAY_WIDGET, text=art_text, position=(205, 295))

        self._update_players_list()

    def _update_players_list(self):
        """Update the players list display."""
        cls = self.__class__
        [element.delete() for element in cls.SERVER_LIST_ELEMENTS]
        cls.SERVER_LIST_ELEMENTS.clear()

        players = self._get_filtered_players()
        if players:
            self.players_tip.delete()

        container_height = max(len(players) * 30, 90)
        ocw(cls.MainParent2, size=(205, container_height))

        found_selected = False
        for i, player_data in enumerate(players):
            player_name, address = player_data

            # Determine color based on selection
            is_selected = player_name == cls.SCROLL_WIDGET and not found_selected
            color = self.theme.get_color('COLOR_PRIMARY') if is_selected else self.theme.get_color('COLOR_TERTIARY')

            text_widget = tw(
                parent=cls.MainParent2,
                size=(200, 30),
                selectable=True,
                click_activate=True,
                glow_type='uniform',
                color=color,
                text=player_name,
                position=(0, container_height - 30 - 30 * i),
                maxwidth=175,
                on_activate_call=CallStrict(self._on_server_select, i, player_name),
                v_align='center'
            )

            if not found_selected and is_selected:
                ocw(cls.MainParent2, visible_child=text_widget)
                found_selected = True

            cls.SERVER_LIST_ELEMENTS.append(text_widget)

        # Save current selection state for color updates
        self._current_selected_player = cls.SCROLL_WIDGET

    def _on_scan_complete(self):
        """Handle scan completion."""
        self._play_ding_sound(0, 1)
        [thread.join() for thread in self.scan_threads]
        self.scan_threads.clear()
        
        cls = self.__class__

        scan_time = time.time() - cls.SCAN_START_TIME
        servers_scanned = len(self.SERVER_MEMORY)
        servers_per_second = int(servers_scanned / scan_time)
        scan_finished = get_lang_text('Scan.finished')
        scan_scanned = get_lang_text('Scan.scanned')
        scan_servers = get_lang_text('Scan.servers')
        scan_in = get_lang_text('Scan.in')
        scan_seconds = get_lang_text('Scan.seconds')
        scan_approx = get_lang_text('Scan.approximately')
        scan_server = get_lang_text('Scan.server')
        scan_per_second = get_lang_text('Scan.perSecond')

        TIP(
            f'{scan_finished}\n'
            f'{scan_scanned} {servers_scanned} {scan_servers} {scan_in} {round(scan_time,2)} {scan_seconds}\n'
            f'{scan_approx} {servers_per_second} {scan_server}{scan_per_second}'
        )

        cls.IS_SCANNING = False
        
        # Update friends panel with new server data
        self._update_friends_panel()

    # Language subscription methods
    def _setup_language_subscriptions(self):
        """Configure all language subscriptions."""
        self._subscribe_language('Global.search', self._update_search_button_text)
        self._subscribe_language('FinderWindow.searchServers', self._update_search_servers_header)
        self._subscribe_language('FinderWindow.searchPlayers', self._update_search_players_text)
        self._subscribe_language('FinderWindow.searchServersForPlayers', self._update_players_tip_text)
        self._subscribe_language('FinderWindow.pressSearch', self._update_art_display_text)
        self._subscribe_language('FinderWindow.selectToViewInfo', self._update_tip_widget_text)

    def _update_search_button_text(self, new_text):
        """Update search button text."""
        if hasattr(self, 'search_button') and self.search_button and self.search_button.exists():
            obw(edit=self.search_button, label=new_text)

    def _update_search_servers_header(self, new_text):
        """Update server search header text."""
        if hasattr(self, 'search_servers_text') and self.search_servers_text and self.search_servers_text.exists():
            tw(edit=self.search_servers_text, text=new_text)

    def _update_search_players_text(self, new_text):
        """Update search description text."""
        if hasattr(self, 'search_players_text') and self.search_players_text and self.search_players_text.exists():
            tw(edit=self.search_players_text, text=new_text)

    def _update_players_tip_text(self, new_text):
        """Update player tip text."""
        if hasattr(self, 'players_tip') and self.players_tip and self.players_tip.exists():
            tw(edit=self.players_tip, text=new_text)

    def _update_art_display_text(self, new_text):
        """Update the display art text only if we are not displaying server-side art."""
        cls = self.__class__
        if not cls.SHOWING_SERVER_ART:
            if hasattr(cls, 'ART_DISPLAY_WIDGET') and cls.ART_DISPLAY_WIDGET and cls.ART_DISPLAY_WIDGET.exists():
                tw(edit=cls.ART_DISPLAY_WIDGET, text=new_text)

    def _update_tip_widget_text(self, new_text):
        """Update tip widget text only if we are not displaying server information."""
        cls = self.__class__
        if not cls.SHOWING_SERVER_INFO:
            if hasattr(cls, 'TIP_WIDGET') and cls.TIP_WIDGET and cls.TIP_WIDGET.exists():
                tw(edit=cls.TIP_WIDGET, text=new_text)
                self.default_tip_text = new_text

    # Color subscription methods
    def _setup_colors_subscriptions(self):
        """Configure all color subscriptions."""
        self._subscribe_color('COLOR_PRIMARY', self._update_art_display_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_filter_text_color)
        self._subscribe_color('COLOR_TERTIARY', self._update_search_description_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_search_servers_text_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_search_button_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_search_button_textcolor)
        self._subscribe_color('COLOR_TERTIARY', self._update_filter_placeholder_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_players_container_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_players_tip_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_tip_widget_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_info_elements_color)
        self._subscribe_color('COLOR_SECONDARY', self._update_info_elements_button_color)
        self._subscribe_color('COLOR_TERTIARY', self._update_server_list_elements_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_server_list_selected_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_border_left_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_border_top_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_border_right_color)
        self._subscribe_color('COLOR_PRIMARY', self._update_border_bottom_color)
    
    def _update_filter_text_color(self, new_color):
        """Update filter text color."""
        cls = self.__class__
        if hasattr(cls, 'FILTER_TEXT_WIDGET') and cls.FILTER_TEXT_WIDGET and cls.FILTER_TEXT_WIDGET.exists():
            tw(edit=cls.FILTER_TEXT_WIDGET, color=new_color)

    def _update_search_description_color(self, new_color):
        """Update search description color."""
        if hasattr(self, 'search_players_text') and self.search_players_text and self.search_players_text.exists():
            tw(edit=self.search_players_text, color=new_color)

    def _update_art_display_color(self, new_color):
        """Update the art display color."""
        cls = self.__class__
        if hasattr(cls, 'ART_DISPLAY_WIDGET') and cls.ART_DISPLAY_WIDGET and cls.ART_DISPLAY_WIDGET.exists():
            tw(edit=cls.ART_DISPLAY_WIDGET, color=new_color)

    def _update_search_servers_text_color(self, new_color):
        """Update the color of the 'Search Servers' text."""
        if hasattr(self, 'search_servers_text') and self.search_servers_text and self.search_servers_text.exists():
            tw(edit=self.search_servers_text, color=new_color)

    def _update_search_button_color(self, new_color):
        """Update search button color."""
        if hasattr(self, 'search_button') and self.search_button and self.search_button.exists():
            obw(edit=self.search_button, color=new_color)

    def _update_search_button_textcolor(self, new_color):
        """Update the text color of the search button."""
        if hasattr(self, 'search_button') and self.search_button and self.search_button.exists():
            obw(edit=self.search_button, textcolor=new_color)

    def _update_filter_placeholder_color(self, new_color):
        """Update filter placeholder color."""
        if hasattr(self, 'filter_placeholder') and self.filter_placeholder and self.filter_placeholder.exists():
            tw(edit=self.filter_placeholder, color=new_color)
    
    def _update_players_container_color(self, new_color):
        """Update player container color."""
        if hasattr(self, 'players_parent') and self.players_parent and self.players_parent.exists():
            sw(edit=self.players_parent, color=new_color)
    
    def _update_players_tip_color(self, new_color):
        """Update player tip color."""
        if hasattr(self, 'players_tip') and self.players_tip and self.players_tip.exists():
            tw(edit=self.players_tip, color=new_color)
    
    def _update_tip_widget_color(self, new_color):
        """Update tip widget color."""
        cls = self.__class__
        if hasattr(cls, 'TIP_WIDGET') and cls.TIP_WIDGET and cls.TIP_WIDGET.exists():
            tw(edit=cls.TIP_WIDGET, color=new_color)

    def _update_info_elements_color(self, new_color):
        """Update the color of dynamic information elements."""
        if hasattr(self, '_current_displayed_player') and self._current_displayed_player:
            self._display_server_info(self._current_displayed_player)

    def _update_info_elements_button_color(self, new_color):
        """Update background color of dynamic information buttons."""
        if hasattr(self, '_current_displayed_player') and self._current_displayed_player:
            self._display_server_info(self._current_displayed_player)

    def _update_server_list_elements_color(self, new_color):
        """Update the color of the items in the server lists."""
        cls = self.__class__
        if hasattr(cls, 'SERVER_LIST_ELEMENTS'):
            for element in cls.SERVER_LIST_ELEMENTS:
                if element and element.exists():
                    # Only update unselected items
                    current_text = tw(query=element)
                    if current_text != self._current_selected_player:
                        tw(edit=element, color=new_color)

    def _update_server_list_selected_color(self, new_color):
        """Update the color of the selected item in the server list."""
        cls = self.__class__
        if hasattr(cls, 'SERVER_LIST_ELEMENTS') and hasattr(self, '_current_selected_player'):
            for element in cls.SERVER_LIST_ELEMENTS:
                if element and element.exists():
                    current_text = tw(query=element)
                    if current_text == self._current_selected_player:
                        tw(edit=element, color=new_color)

    def _update_border_left_color(self, new_color):
        """Update left border color."""
        if hasattr(self, 'border_left') and self.border_left and self.border_left.exists():
            iw(edit=self.border_left, color=new_color)

    def _update_border_top_color(self, new_color):
        """Update top border color."""
        if hasattr(self, 'border_top') and self.border_top and self.border_top.exists():
            iw(edit=self.border_top, color=new_color)

    def _update_border_right_color(self, new_color):
        """Update right border color."""
        if hasattr(self, 'border_right') and self.border_right and self.border_right.exists():
            iw(edit=self.border_right, color=new_color)

    def _update_border_bottom_color(self, new_color):
        """Update bottom border color."""
        if hasattr(self, 'border_bottom') and self.border_bottom and self.border_bottom.exists():
            iw(edit=self.border_bottom, color=new_color)

def ping_and_get_roster(
    address: str,
    port: int,
    ping_wait: float = 0.3,
    timeout: float = 3.5,
    pro = [],
    dex = None,
):
    """
    Ping a server and retrieve its roster using a single connection.

    Args:
        address (str): The server's IP address.
        port (int): The server's port.
        ping_wait (float): Time to wait between ping retries.
        timeout (float): Overall timeout for the entire operation.
        progress_trackers (list): List to track progress.
        index (int): Index of the server being pinged.

    Returns:
        tuple[float | None, dict | None]: A tuple containing the ping in milliseconds
                                          and the parsed roster dictionary.
    """
    ping_result = None
    roster_result = None
    sock = socket.socket(IPT(address), socket.SOCK_DGRAM)
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
            except:
                break
            time.sleep(ping_wait)
            
        if ping_success:
            ping_result = (time.time() - ping_start_time) * 1000
        else:
            pro.append((dex, 999))
            return (999, [])

        json_dumps = lambda h: dumps(h).encode('utf-8')
        bytes_from_hex = lambda h: bytes.fromhex(h.replace(' ', ''))
        send_packet = lambda h, e=b'': sock.sendto(bytes_from_hex(h) + e, (address, port))
        receive_packet = lambda b: sock.recvfrom(b)[0]
        
        # Start Handshake
        my_handshake = f'{(71 + randint(0, 150)):02x}'
        send_packet(f'18 21 00 {my_handshake}', _babase.app_instance_uuid().encode())
        # The server's response contains its handshake byte at index 1
        server_handshake = f'{receive_packet(3)[1]:02x}'
        receive_packet(1024)  # Ack/Server-Info packet

        send_packet(f'24 {server_handshake} 10 21 00', json_dumps(FinderWindow.SPEC))
        send_packet(f'24 {server_handshake} 11 f0 ff f0 ff 00 12', json_dumps(FinderWindow.AUTH))
        send_packet(f'24 {server_handshake} 11 f1 ff f0 ff 00 15', json_dumps({}))
        send_packet(f'24 {server_handshake} 11 f2 ff f0 ff 00 03')

        receive_packet(1024)  # Ack
        receive_packet(9)     # Ack
        # End Handshake

        # Roster Retrieval Loop
        SERVER_RELIABLE_MESSAGE = 0x25
        BA_SCENEPACKET_MESSAGE = 0x11
        BA_MESSAGE_MULTIPART = 0x0d
        BA_MESSAGE_MULTIPART_END = 0x0e
        BA_MESSAGE_PARTY_ROSTER = 0x09
        
        roster_parts = bytearray()
        collecting_roster = False
        roster_listen_start_time = time.time()
        
        while time.time() - roster_listen_start_time < (timeout / 2):
            packet = receive_packet(2048)

            if not packet or len(packet) < 9:
                continue

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
                    
        # Send Disconnect
        send_packet(f'20 {server_handshake}')

    except:
        pass
    finally:
        sock.close()
        
    pro.append((dex, ping_result))
    return (ping_result, roster_result or [])

# Global helper functions
def BTW(text):
    """Show a blocking message with sound."""
    push(text, color=(1, 1, 0))
    gs('block').play()

def _get_popup_window_scale() -> float:
    uiscale = bui.app.ui_v1.uiscale
    return (2.3 if uiscale is babase.UIScale.SMALL else
            1.65 if uiscale is babase.UIScale.MEDIUM else 1.23)

def _creat_Lstr_list(string_list: list = []) -> list:
    return ([babase.Lstr(resource="??Unknown??", fallback_value=item) for item in string_list])

class LPartyWindow(party.PartyWindow):
    def __init__(self, origin: Sequence[float] = (0, 0)):
        super().__init__(origin)
        load_finder_config()
        load_friends()

        self._menu_button_original = self._menu_button
        self._popup_party_member_client_id = None
        self._popup_type = None
        self._roster = None
        button_size = (80, 30)
        x_position = -60 
        y_position = self._height - 45
        borders = BorderWindow(button_size)
        theme = FinderWindow.theme
        color_bg = theme.get_color('COLOR_SECONDARY')
        color_primary = theme.get_color('COLOR_PRIMARY')
        language = FinderWindow.language
        search_text = language.get_text('Global.search')
        
        # Save reference to background widget
        self._button_background_widget = iw(
            parent=self._root_widget,
            size=(button_size[0] * 1.34, button_size[1] * 1.4),
            position=(x_position - button_size[0] * 0.14, y_position - button_size[1] * 0.20),
            texture=gt('softRect'),
            opacity=0.2,
            color=theme.get_color('COLOR_BACKGROUND')
        )

        self.finder_button = bw(
            parent=self._root_widget,
            position=(x_position, y_position),
            label=search_text,
            color=color_bg,
            textcolor=color_primary,
            size=button_size,
            oac=lambda: FinderWindow(self.finder_button)
        )

        # Create border widgets
        self.border_left = iw(
            parent=self._root_widget,
            size=(borders.border_left.size[0]-1, borders.border_left.size[1]+4.5),
            position=(x_position-5, y_position-2),
            texture=gt('white'),
            color=color_primary
        )

        self.border_top = iw(
            parent=self._root_widget,
            size=(borders.border_top.size[0], borders.border_top.size[1]-1),
            position=(x_position-2, y_position+button_size[1]),
            texture=gt('white'),
            color=color_primary
        )

        self.border_right = iw(
            parent=self._root_widget,
            size=(borders.border_right.size[0]-1, borders.border_right.size[1]+4.5),
            position=(x_position+button_size[0]+2, y_position-2),
            texture=gt('white'),
            color=color_primary
        )

        self.border_bottom = iw(
            parent=self._root_widget,
            size=(borders.border_top.size[0]+1, borders.border_top.size[1]-1),
            position=(x_position-2, y_position-2),
            texture=gt('white'),
            color=color_primary
        )

        self._subscribe_to_theme_changes(theme)
        self._subscribe_to_language_changes(language)

    def _on_menu_button_press(self) -> None:
        """Handle the menu button (three dots)."""
        is_muted = babase.app.config.resolve('Chat Muted')
        
        choices = ['unmute' if is_muted else 'mute']
        choices_display = [
            babase.Lstr(resource='chatUnMuteText' if is_muted else 'chatMuteText')
        ]
        
        server_info = bs.get_connection_to_host_info_2()
        if server_info is not None and not server_info.name.startswith('Private Party '):
            choices.append('add_to_favorites')
            choices_display.append(babase.Lstr(resource='addToFavoritesText'))
        
        PopupMenuWindow(
            position=self._menu_button.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            choices_display=choices_display,
            current_choice='unmute' if is_muted else 'mute',
            delegate=self,
        )
        self._popup_type = 'menu'
    
    def _subscribe_to_theme_changes(self, theme):
        """Subscribe button to theme changes from FinderWindow."""
        
        theme.subscribe('COLOR_SECONDARY', self._update_button_background_color)
        theme.subscribe('COLOR_PRIMARY', self._update_button_text_color)
        theme.subscribe('COLOR_BACKGROUND', self._update_button_background_widget_color)
        theme.subscribe('COLOR_PRIMARY', self._update_border_left_color)
        theme.subscribe('COLOR_PRIMARY', self._update_border_top_color)
        theme.subscribe('COLOR_PRIMARY', self._update_border_right_color)
        theme.subscribe('COLOR_PRIMARY', self._update_border_bottom_color)
        
        # Save references and theme for unsubscription
        self._theme = theme
        self._color_subscriptions = [
            ('COLOR_SECONDARY', self._update_button_background_color),
            ('COLOR_PRIMARY', self._update_button_text_color),
            ('COLOR_BACKGROUND', self._update_button_background_widget_color),
            ('COLOR_PRIMARY', self._update_border_left_color),
            ('COLOR_PRIMARY', self._update_border_top_color),
            ('COLOR_PRIMARY', self._update_border_right_color),
            ('COLOR_PRIMARY', self._update_border_bottom_color)
        ]
    
    def _subscribe_to_language_changes(self, language):
        """Subscribe button to language changes from FinderWindow."""
        language.subscribe('Global.search', self._update_button_text)
        
        # Save references for unsubscription
        self._language = language
        self._language_subscriptions = [
            ('Global.search', self._update_button_text)
        ]
    
    def _update_button_background_color(self, new_color):
        """Update button background color."""
        if self.finder_button and self.finder_button.exists():
            obw(edit=self.finder_button, color=new_color)
    
    def _update_button_text_color(self, new_color):
        """Update button text color."""
        if self.finder_button and self.finder_button.exists():
            obw(edit=self.finder_button, textcolor=new_color)
    
    def _update_button_text(self, new_text):
        """Update button text when language changes."""
        if self.finder_button and self.finder_button.exists():
            obw(edit=self.finder_button, label=new_text)
    
    def _update_button_background_widget_color(self, new_color):
        """Update button background widget color."""
        if hasattr(self, '_button_background_widget') and self._button_background_widget and self._button_background_widget.exists():
            iw(edit=self._button_background_widget, color=new_color)
    
    def _update_border_left_color(self, new_color):
        """Update left border color."""
        if hasattr(self, 'border_left') and self.border_left and self.border_left.exists():
            iw(edit=self.border_left, color=new_color)
    
    def _update_border_top_color(self, new_color):
        """Update top border color."""
        if hasattr(self, 'border_top') and self.border_top and self.border_top.exists():
            iw(edit=self.border_top, color=new_color)
    
    def _update_border_right_color(self, new_color):
        """Update right border color."""
        if hasattr(self, 'border_right') and self.border_right and self.border_right.exists():
            iw(edit=self.border_right, color=new_color)
    
    def _update_border_bottom_color(self, new_color):
        """Update bottom border color."""
        if hasattr(self, 'border_bottom') and self.border_bottom and self.border_bottom.exists():
            iw(edit=self.border_bottom, color=new_color)
    
    def _unsubscribe_theme_changes(self):
        """Unsubscribe all theme subscriptions."""
        if hasattr(self, '_color_subscriptions') and hasattr(self, '_theme'):
            for color_name, callback in self._color_subscriptions:
                self._theme.unsubscribe(color_name, callback)
            self._color_subscriptions.clear()
    
    def _unsubscribe_language_changes(self):
        """Unsubscribe all language subscriptions."""
        if hasattr(self, '_language_subscriptions') and hasattr(self, '_language'):
            for text_key, callback in self._language_subscriptions:
                self._language.unsubscribe(text_key, callback)
            self._language_subscriptions.clear()
    
    def _unsubscribe_all_changes(self):
        """Unsubscribe all theme and language subscriptions."""
        self._unsubscribe_theme_changes()
        self._unsubscribe_language_changes()
        
    def _on_party_member_press(self, client_id: int, is_host: bool,
                               widget: bui.Widget) -> None:
        
        # Choices
        choices = [
            "kick",
            "info",
            "add_friend"
        ]

        voteToKickText = get_lang_text('PartyWindow.voteToKick')
        viewAccountText = get_lang_text('PartyWindow.viewAccount')
        addFriendText = get_lang_text('PartyWindow.addFriend')

        choices_display = [
            babase.Lstr(value=voteToKickText), 
            babase.Lstr(value=viewAccountText),
            babase.Lstr(value=addFriendText),
        ]

        PopupMenuWindow(
            position=widget.get_screen_space_center(),
            scale=_get_popup_window_scale(),
            choices=choices,
            choices_display=choices_display,
            current_choice="mention",
            delegate=self
        )
        
        self._popup_party_member_client_id = client_id
        self._popup_party_member_is_host = is_host
        self._popup_type = "partyMemberPress"

    def _getObjectByID(self, type="playerName", ID=None):
        if ID is None:
            ID = self._popup_party_member_client_id
        type = type.lower()
        output = []
        for roster in self._roster:
            if type.startswith("all"):
                if type in ("roster", "fullrecord"):
                    output += [roster]
                elif type.find("player") != -1 and roster["players"] != []:
                    if type.find("namefull") != -1:
                        output += [(i["name_full"]) for i in roster["players"]]
                    elif type.find("name") != -1:
                        output += [(i["name"]) for i in roster["players"]]
                    elif type.find("playerid") != -1:
                        output += [i["id"] for i in roster["players"]]
                elif type.lower() in ("account", "displaystring"):
                    output += [(roster["display_string"])]
            elif roster["client_id"] == ID and not type.startswith("all"):
                try:
                    if type in ("roster", "fullrecord"):
                        return (roster)
                    elif type.find("player") != -1 and roster["players"] != []:
                        if len(roster["players"]) == 1 or type.find("singleplayer") != -1:
                            if type.find("namefull") != -1:
                                return ((roster["players"][0]["name_full"]))
                            elif type.find("name") != -1:
                                return ((roster["players"][0]["name"]))
                            elif type.find("playerid") != -1:
                                return (roster["players"][0]["id"])
                        else:
                            if type.find("namefull") != -1:
                                return ([(i["name_full"]) for i in roster["players"]])
                            elif type.find("name") != -1:
                                return ([(i["name"]) for i in roster["players"]])
                            elif type.find("playerid") != -1:
                                return ([i["id"] for i in roster["players"]])
                    elif type.lower() in ("account", "displaystring"):
                        return ((roster["display_string"]))
                except:
                    babase.print_exception()

        return (None if len(output) == 0 else output)

    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow,
                                   choice: str) -> None:
        """Handle popup menu selection."""

        # Handle menu button press (mute/unmute, add to favorites)
        if self._popup_type == "menu":
            if choice in ('mute', 'unmute'):
                cfg = babase.app.config
                cfg['Chat Muted'] = (choice == 'mute')
                cfg.apply_and_commit()

                # Force chat refresh
                if hasattr(self, '_display_old_msgs'):
                    self._display_old_msgs = True
                self._update()

                # Show confirmation message
                if choice == 'mute':
                    bs.broadcastmessage("Chat muted", color=(1, 0, 0))
                else:
                    bs.broadcastmessage("Chat unmuted", color=(0, 1, 0))

            elif choice == 'add_to_favorites':
                # Delegate to parent class method
                server_info = bs.get_connection_to_host_info_2()
                if server_info is not None:
                    super().popup_menu_selected_choice(popup_window, choice)
                else:
                    bui.getsound('error').play()
                    bs.broadcastmessage(
                        babase.Lstr(resource='errorText'),
                        color=(1, 0, 0)
                    )
            return

        # Handle ban time selection
        elif self._popup_type == "banTimePress":
            result = bs.disconnect_client(
                self._popup_party_member_client_id, ban_time=int(choice))
            if not result:
                bui.getsound('error').play()
                bs.broadcastmessage(
                    babase.Lstr(resource='getTicketsWindow.unavailableText'),
                    color=(1, 0, 0))
            return

        # Handle party member press
        if self._popup_type == "partyMemberPress":
            if choice == "kick":
                areYouSureToKickText = get_lang_text('PartyWindow.areYouSureToKick')
                ConfirmWindow(
                    text=f"{areYouSureToKickText} {self._getObjectByID('account')}?",
                    action=self._kick_selected_player, cancel_button=True, cancel_is_selected=True,
                    color=(1, 1, 1), text_scale=1.0,
                    origin_widget=self.get_root_widget()
                )
            elif choice == "info":
                account = self._getObjectByID("account")
                clean_name = account.replace(V2_LOGO, '')
                ProfileSearchWindow(self.get_root_widget(), v2=clean_name)
            elif choice == "add_friend":
                account = self._getObjectByID("account")
                clean_name = account.replace(V2_LOGO, '')
                self._add_friend(clean_name)

    def _add_friend(self, friend: str):
        """Add a friend."""

        if not friend or friend.strip() == "":
            fieldEmpty = get_lang_text('Global.fieldEmpty')
            push(fieldEmpty, (1, 0, 0))
            gs('error').play()
            return

        prefixed_friend = f"{V2_LOGO}{friend.strip()}"

        # Load current friends
        friends = load_friends()

        # Check if already exists
        for f in friends:
            if f["name"] == prefixed_friend:
                TIP(f"{prefixed_friend} {get_lang_text('Global.alreadyInList')}")
                return

        # Generate new ID
        existing_ids = [int(f["id"]) for f in friends if f["id"].isdigit()]
        new_id = str(max(existing_ids) + 1 if existing_ids else 0).zfill(2)

        # Add friend object
        add_friend(
            name=prefixed_friend,
            friend_id=new_id,
            accounts=[],
            account_pb=None,
            account_id=None
        )

        TIP(f"{prefixed_friend} {get_lang_text('Global.addedSuccessfully')}")

    def _kick_selected_player(self):
        if self._popup_party_member_client_id != -1:
            if bs.get_foreground_host_session() is not None:
                self._popup_type = "banTimePress"
                choices = [0, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 99999999]
                PopupMenuWindow(
                    position=self.get_root_widget().get_screen_space_center(),
                    scale=_get_popup_window_scale(),
                    choices=[str(item) for item in choices],
                    choices_display=_creat_Lstr_list(
                        [f"Ban for {item} second(s)." for item in choices]),
                    current_choice="Share_Server_Info",
                    delegate=self
                )
            else:
                info = bs.get_connection_to_host_info_2()
                if bool(info) and (info.build_number < 14248):
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

    def close(self) -> None:
        if hasattr(self, '_update_timer') and self._update_timer is not None:
            self._update_timer = None

        self._unsubscribe_all_changes()

        super().close()

    def close_with_sound(self) -> None:
        if hasattr(self, '_update_timer') and self._update_timer is not None:
            self._update_timer = None

        self._unsubscribe_all_changes()
        super().close_with_sound()

# ba_meta export babase.Plugin
class byLess(Plugin):
    def __init__(self):
        party.PartyWindow = LPartyWindow