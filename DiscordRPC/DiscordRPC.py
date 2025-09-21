# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING
from baenv import TARGET_BALLISTICA_BUILD as build_number
import babase
import bauiv1 as bui
import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional
import weakref
import os
import json
import time
from time import mktime
from abc import ABCMeta, abstractmethod
import socket
import sys
import struct
import uuid

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2
OP_PING = 3
OP_PONG = 4


class DiscordIpcError(Exception):
    pass


class DiscordIpcClient(metaclass=ABCMeta):
    def __init__(self, client_id):
        self.client_id = client_id
        self._connect()
        self._do_handshake()
        #print(f"[DiscordRP] Conectado vía ID {client_id}")

    @classmethod
    def for_platform(cls, client_id, platform=sys.platform):
        if platform == 'win32':
            return WinDiscordIpcClient(client_id)
        else:
            return UnixDiscordIpcClient(client_id)

    @abstractmethod
    def _connect(self):
        pass

    def _do_handshake(self):
        ret_op, ret_data = self.send_recv({'v': 1, 'client_id': self.client_id}, op=OP_HANDSHAKE)
        if ret_op == OP_FRAME and ret_data['cmd'] == 'DISPATCH' and ret_data['evt'] == 'READY':
            return
        else:
            if ret_op == OP_CLOSE:
                self.close()
            raise RuntimeError(ret_data)

    @abstractmethod
    def _write(self, data: bytes):
        pass

    @abstractmethod
    def _recv(self, size: int) -> bytes:
        pass

    def _recv_header(self) -> (int, int):
        header = self._recv_exactly(8)
        return struct.unpack("<II", header)

    def _recv_exactly(self, size) -> bytes:
        buf = b""
        size_remaining = size
        while size_remaining:
            chunk = self._recv(size_remaining)
            buf += chunk
            size_remaining -= len(chunk)
        return buf

    def close(self):
        print("[DiscordRP] Cerrando conexión")
        try:
            self.send({}, op=OP_CLOSE)
        finally:
            self._close()

    @abstractmethod
    def _close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def send_recv(self, data, op=OP_FRAME):
        self.send(data, op)
        return self.recv()

    def send(self, data, op=OP_FRAME):
        #print(f"[DiscordRP] Enviando {data}")
        data_str = json.dumps(data, separators=(',', ':'))
        data_bytes = data_str.encode('utf-8')
        header = struct.pack("<II", op, len(data_bytes))
        self._write(header)
        self._write(data_bytes)

    def recv(self) -> (int, "JSON"):
        op, length = self._recv_header()
        payload = self._recv_exactly(length)
        data = json.loads(payload.decode('utf-8'))
        #print(f"[DiscordRP] Recibido {data}")
        return op, data

    def set_activity(self, act):
        data = {
            'cmd': 'SET_ACTIVITY',
            'args': {'pid': os.getpid(),
                     'activity': act},
            'nonce': str(uuid.uuid4())
        }
        #print(f"[DiscordRP] Actualizando actividad: {act}")
        self.send(data)


class WinDiscordIpcClient(DiscordIpcClient):
    _pipe_pattern = R'\\?\pipe\discord-ipc-{}'

    def _connect(self):
        for i in range(10):
            path = self._pipe_pattern.format(i)
            try:
                self._f = open(path, "w+b")
            except OSError:
                pass
            else:
                break
        else:
            return DiscordIpcError("No se pudo conectar al pipe de Discord")
        self.path = path
        print(f"[DiscordRP] Conectado a pipe {path}")

    def _write(self, data: bytes):
        try:
            self._f.write(data)
            self._f.flush()
        except:
            pass

    def _recv(self, size: int) -> bytes:
        try:
            return self._f.read(size)
        except:
            return b"0"

    def _close(self):
        self._f.close()


class UnixDiscordIpcClient(DiscordIpcClient):
    def _connect(self):
        self._sock = socket.socket(socket.AF_UNIX)
        pipe_pattern = self._get_pipe_pattern()

        for i in range(10):
            path = pipe_pattern.format(i)
            if not os.path.exists(path):
                continue
            try:
                self._sock.connect(path)
            except OSError:
                pass
            else:
                break
        else:
            return DiscordIpcError("No se pudo conectar al socket de Discord")
        #print(f"[DiscordRP] Conectado a socket {path}")

    @staticmethod
    def _get_pipe_pattern():
        env_keys = ('XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP')
        for env_key in env_keys:
            dir_path = os.environ.get(env_key)
            if dir_path:
                break
        else:
            dir_path = '/tmp'
        return os.path.join(dir_path, 'discord-ipc-{}')

    def _write(self, data: bytes):
        self._sock.sendall(data)

    def _recv(self, size: int) -> bytes:
        return self._sock.recv(size)

    def _close(self):
        self._sock.close()


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def __init__(self):
        self.details = "Menú principal"
        self.state = "AFK"
        self.laststatus = "offline"
        self.starttime = mktime(time.localtime())
        self.dcLastState = False
        self.client_id = '806052133761450024'

        self._pipe_pattern = R'\\?\pipe\discord-ipc-{}'
        self.x = 0

        if self.discordrunning():
            self.rpc_obj = DiscordIpcClient.for_platform(self.client_id)
            self.dcLastState = True

        # Start the timer 1s after loading
        babase.apptimer(1.0, self.start_timer)

    def start_timer(self):
        self._timer = babase.AppTimer(0.9, self.main, repeat=True)
        #print("[DiscordRP][DEBUG] Timer iniciado correctamente")

    def discordrunning(self):
        if sys.platform == "win32":
            for i in range(10):
                path = self._pipe_pattern.format(i)
                try:
                    self._f = open(path, "w+b")
                except:
                    self.x += 1
                else:
                    self._f.close()
                    print(f"[DiscordRP] Detectado Discord en {path}")
                    return True
            print("[DiscordRP] No se encontró Discord en Windows")
            return False
        else:
            pipe_pattern = UnixDiscordIpcClient._get_pipe_pattern()
            for i in range(10):
                path = pipe_pattern.format(i)
                if os.path.exists(path):
                   # print(f"[DiscordRP] Detectado Discord en {path}")
                    return True
            print("[DiscordRP] No se encontró Discord en Linux/Mac")
            return False

    def main(self):
        try:
            if self.discordrunning():
                if not self.dcLastState:
                    print("[DiscordRP] Reconectando a Discord...")
                    self.rpc_obj = DiscordIpcClient.for_platform(self.client_id)
                    self.dcLastState = True
            else:
                if self.dcLastState:
                    print("[DiscordRP] Discord cerrado, deteniendo RPC")
                self.dcLastState = False

            # Execute the main logic
            self.getstatus()

            activity = {
                "state": self.state,
                "details": self.details,
                "timestamps": {
                    "start": self.starttime
                },
                "assets": {
                    "small_text": "bslogo",
                    "small_image": "bslogo",
                    "large_text": "large",
                    "large_image": "large"
                }
            }
            if self.dcLastState:
                self.rpc_obj.set_activity(activity)

        except Exception as e:
            import traceback
            print("[DiscordRP][ERROR]", e)
            traceback.print_exc()

    def getstatus(self):
        # --- REMOTE HOST INFO (if applicable) ---
        host_info = bs.get_connection_to_host_info_2()

        if host_info is None:
            #print("[SERVER] No conectado a ningún host remoto.")
            return

        # Current number of players
        current_players = len(bs.get_game_roster()) - 1

        # Max players calculation
        if current_players <= 6:
            max_players = "6"
            players_str = f"{current_players}/{max_players}"
        else:
            max_players = str(current_players)
            players_str = f"{current_players}/{max_players}"

        # Print only clean summary
        #print(f"[SERVER] Nombre: {host_info.name}")
        #print(f"[SERVER] IP: {host_info.address}")
        #print(f"[SERVER] Puerto: {host_info.port}")
        #print(f"[SERVER] Jugadores: {players_str}")

        # Update Rich Presence as well
        self.state = host_info.name
        self.details = f"Online ({players_str})"
