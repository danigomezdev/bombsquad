# ba_meta require api 9

from __future__ import annotations

import bascenev1 as bs
import _baplus
import _babase
import babase
from bauiv1lib.fileselector import FileSelectorWindow
#from bauiv1lib.promocode import PromoCodeWindow
from bauiv1lib.confirm import ConfirmWindow
import bauiv1 as bui
import os
import urllib.request
from threading import Thread
import logging
from babase._general import Call
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, Sequence

app = _babase.app
            
MODS_DIR = _babase.env()['python_directory_user'] 
SAVED_REPLAYS = MODS_DIR + '/REPLAYS/'

#print("antes dir")
#print(dir(babase.app))
REPLAYS_DIR =  bui.get_replays_dir()
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/octet-stream',
    'User-Agent': 'BombSquad Client'
}

class ExportConfirmation(ConfirmWindow):
    def __init__(
        self,
        file_path = "",
        status = "init",
        text: str | bui.Lstr = 'Are you sure?',
        ok_text = "",
        action: Callable[[], Any] | None = None,
        origin_widget: bui.Widget | None = None,
        
    ):
        super().__init__(text=text, action=action, origin_widget=origin_widget, ok_text=ok_text)
        self.status = status
        self.file_path = file_path

    def _ok(self) -> None:
        if self.status == "init":
            self._cancel()
            #ExportConfirmation("", "uploading", text = "Uploading file wait !", ok_text= "Wait")
            self._upload_file()
            
        elif self.status == "uploading":
             bui.screenmessage("uploading in progress")
        elif self.status == "uploaded":
            pass

    def _upload_file(self):
        self.status = "uploading"
        print(self.root_widget)
        thread = Thread(target = handle_export, args = (self.file_path, self.uploaded, self.root_widget,))
        thread.start()

    def uploaded(self, url, root_widget):
        self.status = "uploaded"
        #from bauiv1lib.url import ShowURLWindow
        #ShowURLWindow(url)

class ImportConfirmation(ConfirmWindow):
    def __init__(
        self,
        file_path = "",
        status = "init",
        text: str | bui.Lstr = 'Are you sure?',
        ok_text = "",
        action: Callable[[], Any] | None = None,
        origin_widget: bui.Widget | None = None,
        
    ):
        super().__init__(text=text, action=action, origin_widget=origin_widget, ok_text=ok_text)
        self.status = status
        self.file_path = file_path

    def _ok(self) -> None:
        if self.status == "init":
            self._cancel()
            #ExportConfirmation("", "uploading", text = "Uploading file wait !", ok_text= "Wait")
            self._upload_file()
            
        elif self.status == "uploading":
             bui.screenmessage("uploading in progress")
        elif self.status == "uploaded":
            pass

    def _upload_file(self):
        self.status = "uploading"
        print(self.root_widget)
        thread = Thread(target = handle_import, args = (self.file_path, self.uploaded, self.root_widget,))
        thread.start()

    def uploaded(self, url, root_widget):
        self.status = "uploaded"
        #from bauiv1lib.url import ShowURLWindow
        #ShowURLWindow(url)

class ImportFilesWindow:
    def __init__(self, origin_widget: bui.Widget | None = None, path=None):
        self._path = path

        # Create and display file chooser pointing to SAVED_REPLAYS
        FileSelectorWindow(
            path=SAVED_REPLAYS,
            callback=self._file_chosen,
            show_base_path=False,
            valid_file_extensions=["brp",
                                    #"py", "txt", "json"
                                    ],
            allow_folders=False,
        ).get_root_widget()

    def _file_chosen(self, path: str | None):
        if path is not None:
            #bui.screenmessage(f"Archivo seleccionado: {os.path.basename(path)}")
            #print(f"[INFO] Archivo seleccionado: {path}")

            ImportConfirmation(
                path,
                "init",
                text= "Quieres importar el archivo " +
                path.split("/")[-1],
                ok_text= "Importar"
            )

class FileSelectorExtended(FileSelectorWindow):
        
    def __init__(
        self,
        path: str,
        callback: Callable[[str | None], Any] | None = None,
        show_base_path: bool = True,
        valid_file_extensions: Sequence[str] | None = None,
        allow_folders: bool = False,
    ):
        super().__init__(path, callback = callback, show_base_path = show_base_path, valid_file_extensions = valid_file_extensions, allow_folders = allow_folders)
        
        self._create_folder_button = bui.buttonwidget(
            parent=self._root_widget,
            button_type='square',
            position=(self._folder_center + 120, self._height - 113),
            color=(0.6, 0.53, 0.63),
            textcolor=(0.75, 0.7, 0.8),
            enable_sound=False,
            size=(55, 35),
            label="Crear \n Carpeta",
            on_activate_call=self._create_folder_replays_menu,
        )

        self._import_button = bui.buttonwidget(
            parent=self._root_widget,
            button_type='square',
            position=(self._folder_center + 200, self._height - 113),
            color=(0.6, 0.53, 0.63),
            textcolor=(0.75, 0.7, 0.8),
            enable_sound=False,
            size=(55, 35),
            label="Importar",
            on_activate_call=self._open_import_menu,
        )
    def _open_import_menu(self):
        ImportFilesWindow(origin_widget=self._import_button, path = self._path)

    def _create_folder_replays_menu(self):
        try:
            if os.path.exists(SAVED_REPLAYS):
                bui.screenmessage('La carpeta REPLAYS ya existe.', (1, 1, 0))
                bui.getsound('error').play()
            else:
                os.makedirs(SAVED_REPLAYS)
                bui.screenmessage('Carpeta REPLAYS creada con éxito.', (0, 1, 0))
                bui.getsound('dingSmallHigh').play()
        except Exception as e:
            bui.screenmessage('Error al crear la carpeta REPLAYS.', (1, 0, 0))
            bui.getsound('error').play()
            print(f"[ERROR] No se pudo crear la carpeta REPLAYS: {e}")

    def _on_entry_activated(self, entry: str) -> None:
        # pylint: disable=too-many-branches
        new_path = None
        try:
            assert self._path is not None
            if entry == '..':
                chunks = self._path.split('/')
                if len(chunks) > 1:
                    new_path = '/'.join(chunks[:-1])
                    if new_path == '':
                        new_path = '/'
                else:
                    bui.getsound('error').play()
            else:
                if self._path == '/':
                    test_path = self._path + entry
                else:
                    test_path = self._path + '/' + entry
                #if test_path == "/bombsquad/mods":
                #    test_path = MODS_DIR
                if test_path == "/bombsquad/replays":
                    test_path = REPLAYS_DIR
                if os.path.isdir(test_path):
                    bui.getsound('swish').play()
                    new_path = test_path
                elif os.path.isfile(test_path):
                    if self._is_valid_file_path(test_path):
                        bui.getsound('swish').play()
                        if self._callback is not None:
                            self._callback(test_path)
                    else:
                        bui.getsound('error').play()
                else:
                    print(
                        (
                            'Error: FileSelectorWindow found non-file/dir:',
                            test_path,
                        )
                    )
        except Exception:
            logging.exception(
                'Error in FileSelectorWindow._on_entry_activated().'
            )

        if new_path is not None:
            self._set_path(new_path)

org_listdir = os.listdir     
def custom_listdir(path):
    if path == "/bombsquad":
        return [#"mods",
                "replays"]
    return org_listdir(path)
os.listdir = custom_listdir

import uuid
import io
import re
import json
import urllib.request
import mimetypes
class MultiPartForm:
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        # Use a large random byte string to separate
        # parts of the MIME data.
        self.boundary = uuid.uuid4().hex.encode('utf-8')
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary={}'.format(
            self.boundary.decode('utf-8'))

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))

    def add_file(self, fieldname, filename, fileHandle,
                 mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = (
                mimetypes.guess_type(filename)[0] or
                'application/octet-stream'
            )
        self.files.append((fieldname, filename, mimetype, body))
        return

    @staticmethod
    def _form_data(name):
        return ('Content-Disposition: form-data; '
                'name="{}"\r\n').format(name).encode('utf-8')

    @staticmethod
    def _attached_file(name, filename):
        return ('Content-Disposition: form-data; '
                'name="{}"; filename="{}"\r\n').format(
                    name, filename).encode('utf-8')

    @staticmethod
    def _content_type(ct):
        return 'Content-Type: {}\r\n'.format(ct).encode('utf-8')

    def __bytes__(self):
        """Return a byte-string representing the form data,
        including attached files.
        """
        buffer = io.BytesIO()
        boundary = b'--' + self.boundary + b'\r\n'

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self._form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode('utf-8'))
            buffer.write(b'\r\n')

        # Add the files to upload
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self._attached_file(f_name, filename))
            buffer.write(self._content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(b'--' + self.boundary + b'--\r\n')
        return buffer.getvalue()

def handle_export(file, callback, root_widget):
    import shutil

    try:
        file_name = os.path.basename(file)

        # Make sure the folder exists
        if not os.path.exists(SAVED_REPLAYS):
            os.makedirs(SAVED_REPLAYS)

        target_path = os.path.join(SAVED_REPLAYS, file_name)
        shutil.copy(file, target_path)

        bui.screenmessage(f"Archivo exportado con éxico en {target_path}")
        #print(f"[INFO] File saved to: {target_path}")

        _babase.pushcall(Call(callback, target_path, root_widget), from_other_thread=True)

    except Exception as e:
        bui.screenmessage("Error exportando archivo.")
        print(f"[ERROR] Failed to copy file: {e}")

def handle_import(file, callback, root_widget):
    import shutil

    try:
        file_name = os.path.basename(file)

        # Make sure the destination folder exists
        if not os.path.exists(REPLAYS_DIR):
            os.makedirs(REPLAYS_DIR)

        target_path = os.path.join(REPLAYS_DIR, file_name)
        shutil.copy(file, target_path)

        bui.screenmessage(f"Archivo importado con éxito a {target_path}")
        #print(f"[INFO] Archivo importado a: {target_path}")

        _babase.pushcall(Call(callback, target_path, root_widget), from_other_thread=True)

    except Exception as e:
        bui.screenmessage("Error importando archivo.")
        print(f"[ERROR] Fallo al copiar archivo: {e}")

def handle_download(url, path, callback):
    req = urllib.request.Request(url, headers={'accept': '*/*'}, method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                # Read the filename from the Content-Disposition header
                filename = None
                content_disposition = response.headers.get('Content-Disposition', '')
               
                match = re.search(r'filename\*?=(.+)', content_disposition)
          
                if match:
                    filename = urllib.parse.unquote(match.group(1), encoding='utf-8')
                    filename = filename.replace("UTF-8''", '')

                output_path = os.path.join(path, filename)

                with open(output_path, 'wb') as file:
                    file.write(response.read())
                _babase.pushcall(Call(callback, output_path),from_other_thread= True)
                print(f"File downloaded and saved to: {output_path}")
            else:
                print(f"Failed to download file. Status code: {response.getcode()}")
    except urllib.error.URLError as e:
        # bui.screenmessage(f'Error occured {e}')
        print(f"Error occurred: {e}")

# ba_meta export plugin
class byLess(babase.Plugin):
    def on_app_running(self):
        pass

    def has_settings_ui(self):
        return True

    def show_settings_ui(self, source_widget):
            app = _babase.app
            virtual_directory_path = '/bombsquad'
            FileSelectorExtended(
               virtual_directory_path,
                callback=self.fileSelected,
                show_base_path=False,
                valid_file_extensions=[
                    "txt","py","json","brp"
                ],
                allow_folders=False,
            ).get_root_widget()
    
    def fileSelected(self, path):
        if path:
            ExportConfirmation(
                path,
                "init",
                text= "Quieres exportar el archivo " +
                path.split("/")[-1],
                ok_text= "Exportar"
            )