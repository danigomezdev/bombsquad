# ba_meta require api 9
# ba_meta name Discord Rich Presence
# ba_meta description A mod that allows you to update your gaming activity on Discord specifically for BombSquad
# ba_meta version 1.1.4

#!"Made to you by @brostos, @Dliwk & Less"

from __future__ import annotations
from urllib.request import Request, urlopen, urlretrieve
from pathlib import Path
from os import getcwd, remove
from os.path import abspath
from bauiv1lib.popup import PopupWindow

import asyncio
import sys
import http.client
import ast
import uuid
import json
import socket
import time
import threading
import shutil
import hashlib
import logging
import select
from time import mktime
import babase
import _babase
import bascenev1 as bs
import bauiv1 as bui
from baenv import TARGET_BALLISTICA_BUILD as build_number

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Tuple


MAPNAME_ID = {
    "bombsquadicon": "963448129900908595",
    "zigzagpreview": "963448133130522624",
    "tiptoppreview": "963448133168279582",
    "towerdpreview": "963448135886200912",
    "thepadpreview": "963448137916248084",
    "steprightuppreview": "963448141728862248",
    "roundaboutpreview": "963448143997972550",
    "rampagepreview": "963448146422296676",
    "monkeyfacepreview": "963448151182831626",
    "footballstadiumpreview": "963448158719983646",
    "doomshroompreview": "963448160993292368",
    "cragcastlepreview": "963448163048513536",
    "courtyardpreview": "963448166127120504",
    "bridgitpreview": "963448169180565654",
    "biggpreview": "963448172905127996",
    "alwayslandpreview": "963448174163423252",
    "bigg": "1013013392455376977",
    "bridgit": "1013013400139333632",
    "courtyard": "1013013410776096788",
    "cragcastle": "1013013423132528700",
    "doomshroom": "1013013438223622224",
    "footballstadium": "1013013452517810226",
    "hockeystadium": "1013013464060547112",
    "monkeyface": "1013013477721383023",
    "rampage": "1013013484830728273",
    "roundabout": "1013013508323037264",
    "steprightup": "1013013567768907826",
    "thepad": "1013013577197699163",
    "tiptop": "1013013593089904721",
    "towerd": "1013013604531970131",
    "zigzag": "1013013618188619816",
    "bombsquadlogo2": "1013016083701190726",
    "windows": "1084050785488338984",
    "linux": "1084078945944739920",
    "lobby": "1084180821973418226",
    "ranking": "1084224689272004719",
    "rampagelevelcolor": "1086989941541703741",
    "landmine": "1087000404866371766",
    "rgbstripes": "1087000416492990474",
    "shrapnel1color": "1087151233225195590",
    "bonescolor": "1087151164077899928",
    "bridgitlevelcolor": "1087151178674094182",
    "crossout": "1087151197963681902",
    "naturebackgroundcolor": "1087151209896476782",
    "zigzaglevelcolor": "1087151253206876241",
    "zoeicon": "1087151266989363240",
    "bg": "1087564057890000906",
    "alwayslandlevelcolor": "1087564765406167080",
    "hockeystadiumpreview": "1087574349285961768",
    "mac": "1087584375287336992",
    "flyer": "1087584543147561051",
    "replay": "1087592122393301102",
    "coop": "1097697042891018311",
    "ffa": "1097697050214269008",
    "lobbysmall": "1097697055926923335",
    "replaysmall": "1097697062746853386",
    "teams": "1097697068727935036",
    "bacongreece": "1097700754623565894",
    "basketballstadium": "1097700771501441167",
    "flapland": "1097700783622979664",
    "alwaysland": "1097700794213613610",
    "hoveringwood": "1097700802321199224",
    "jrmponslaught": "1097700810479124520",
    "jrmprunaround": "1097700817194205286",
    "lakefrigid": "1097700828023898203",
    "mushfeud": "1097700836920000594",
    "pillar_bases": "1097700846340407427",
    "powerup_factory": "1097700854422851656",
    "snowballpit": "1097700869673341009",
    "stoneishfort": "1097700887826272308",
    "toiletdonut": "1097700898584666193",
    "whereeaglesdare": "1097700904972587109",
    "android": "1097728392280932453",
}
ANDROID = babase.app.classic.platform == "android"
APP_VERSION = (
    _babase.app.version
    if build_number < 21282
    else (
        _babase.app.env.engine_version
        if build_number > 21823
        else _babase.app.env.version
    )
)

class AndroidPresencebyLess():
    def __init__(self):

        self.details = "Menú principal"
        self.state = "AFK"
        self.laststatus = "offline"
        self.starttime = mktime(time.localtime())

        self._http_port = 26000
        self._http_running = False
        self._http_thread = None
        self._http_sock = None
        self._last_status = {}

        # Start the timer 1s after loading
        babase.apptimer(1.0, self.start_timer)

        # Start HTTP server
        try:
            self.start_http_server(host="127.0.0.1", port=self._http_port)
        except Exception as e:
            #print("[SERVER][HTTP] Could not start HTTP server:", e)
            pass

    def start_timer(self):
        # Run every 0.9 seconds
        self._timer = babase.AppTimer(0.9, self.main, repeat=True)

    def main(self):
        try:
            self.getstatus()
        except Exception as e:
            import traceback
            #print("[SERVER][ERROR]", e)
            traceback.print_exc()

    def getstatus(self):
        host_info = bs.get_connection_to_host_info_2()
    
        if host_info is None:
            name = "server not found"
            ip = "ip not found"
            port = "port not found"
            players_str = "0/0"
        else:
            current_players = len(bs.get_game_roster()) - 1
            if current_players <= 6:
                max_players = "6"
            else:
                max_players = str(current_players)
            players_str = f"{current_players}/{max_players}"
    
            name = host_info.name
            ip = host_info.address
            port = host_info.port
    
        # --- Print in console ---
        #print(f"[SERVER] Name: {name}")
        #print(f"[SERVER] IP: {ip}")
        #print(f"[SERVER] Port: {port}")
        #print(f"[SERVER] Players: {players_str}")
    
        # --- Create new snapshot ---
        new_status = {
            "server_name": name,
            "ip": ip,
            "port": port,
            "players": players_str,
            "timestamp": int(time.time()),
        }
    
        # --- Update only if changes ---
        changed = False
        for key, value in new_status.items():
            if self._last_status.get(key) != value:
                self._last_status[key] = value
                changed = True
    
        if changed:
            #print("[SERVER][DEBUG] Status updated in _last_status")
            pass
    
        self.state = name
        self.details = f"Online ({players_str})"


    def build_status_payload(self):
        return self._last_status

    # ---- Mini HTTP server ----
    def start_http_server(self, host="127.0.0.1", port=43210):
        if self._http_running:
            return
        self._http_running = True
        self._http_thread = threading.Thread(
            target=self._http_server_loop, args=(host, port), daemon=True
        )
        self._http_thread.start()
        #print(f"[SERVER][HTTP] Server started at http://{host}:{port}")

    def stop_http_server(self):
        self._http_running = False
        try:
            if self._http_sock:
                try:
                    self._http_sock.close()
                except:
                    pass
                self._http_sock = None
            if self._http_thread:
                self._http_thread.join(timeout=0.2)
        except Exception as e:
            #print("[SERVER][HTTP] Error stopping server:", e)
            pass

    def _http_server_loop(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(5)
            sock.setblocking(False)
            self._http_sock = sock
        except Exception as e:
            #print("[SERVER][HTTP] Could not bind socket:", e)
            self._http_running = False
            return

        while self._http_running:
            try:
                rlist, _, _ = select.select([sock], [], [], 1.0)
                if not rlist:
                    continue
                conn, addr = sock.accept()
                threading.Thread(
                    target=self._handle_http_client, args=(conn, addr), daemon=True
                ).start()
            except Exception:
                pass

        try:
            sock.close()
        except:
            pass
        self._http_sock = None
        #print("[SERVER][HTTP] Server stopped")

    def _handle_http_client(self, conn, addr):
        try:
            conn.settimeout(2.0)
            data = b""
            try:
                data = conn.recv(4096)
            except socket.timeout:
                pass
            if not data:
                conn.close()
                return

            try:
                text = data.decode("utf-8", errors="ignore")
                first_line = text.splitlines()[0] if text.splitlines() else ""
            except:
                first_line = ""

            method, path = "", "/"
            parts = first_line.split()
            if len(parts) >= 2:
                method, path = parts[0], parts[1]

            if method == "GET" and path in ("/", "/status", "/status.json"):
                payload = self.build_status_payload()
                body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                headers = [
                    b"HTTP/1.1 200 OK",
                    b"Content-Type: application/json; charset=utf-8",
                    b"Content-Length: " + str(len(body)).encode("ascii"),
                    b"Access-Control-Allow-Origin: *",
                    b"",
                    b"",
                ]
                resp = b"\r\n".join(headers) + body
                conn.sendall(resp)
            else:
                body = b'{"error":"not found"}'
                headers = [
                    b"HTTP/1.1 404 Not Found",
                    b"Content-Type: application/json; charset=utf-8",
                    b"Content-Length: " + str(len(body)).encode("ascii"),
                    b"",
                    b"",
                ]
                conn.sendall(b"\r\n".join(headers) + body)
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except:
                pass

    def __del__(self):
        try:
            self.stop_http_server()
        except:
            pass


if ANDROID:  
    AndroidPresencebyLess()

if not ANDROID:
    # installing pypresence
    def get_module():

        install_path = Path(abspath(bs.app.env.python_directory_app))
        path = Path(f"{install_path}/pypresence.tar.gz")
        file_path = Path(f"{install_path}/pypresence")
        source_dir = Path(f"{install_path}/pypresence-4.3.0/pypresence")
        if not file_path.exists():
            url = "https://files.pythonhosted.org/packages/f4/2e/d110f862720b5e3ba1b0b719657385fc4151929befa2c6981f48360aa480/pypresence-4.3.0.tar.gz"
            try:
                filename, headers = urlretrieve(url, filename=path)
                with open(filename, "rb") as f:
                    content = f.read()
                    assert (
                        hashlib.md5(content).hexdigest()
                        == "f7c163cdd001af2456c09e241b90bad7"
                    )
                shutil.unpack_archive(filename, install_path, format="gztar")
                shutil.copytree(source_dir, file_path)
                shutil.rmtree(Path(f"{install_path}/pypresence-4.3.0"))
                remove(path)
            except:
                pass

    get_module()

    from pypresence import PipeClosed, DiscordError, DiscordNotFound
    from pypresence.utils import get_event_loop
    import pypresence

    DEBUG = True

    def print_error(err: str, include_exception: bool = False) -> None:
        if DEBUG:
            if include_exception:
                logging.exception(err)
            else:
                logging.error(err)
        else:
            print(f"ERROR in discordrp.py: {err}")

    def log(msg: str) -> None:
        if DEBUG:
            print(f"LOG in discordrp.py: {msg}")

    def _run_overrides() -> None:
        old_init = bs.Activity.__init__

        def new_init(self, *args: Any, **kwargs: Any) -> None:  # type: ignore
            old_init(self, *args, **kwargs)
            self._discordrp_start_time = time.mktime(time.localtime())

        bs.Activity.__init__ = new_init  # type: ignore

        old_connect = bs.connect_to_party

        def new_connect(*args, **kwargs) -> None:  # type: ignore
            global _last_server_addr
            global _last_server_port
            old_connect(*args, **kwargs)
            _last_server_addr = kwargs.get("address") or args[0]
            # ! Joining a game on same device as host NB check what happens if host is port forwarded you join it and check joining a server port forwarded or not
            _last_server_port = (
                kwargs.get("port") or args[1] if len(args) > 1 else 43210
            )

        bs.connect_to_party = new_connect

    start_time = time.time()

    class RpcThread(threading.Thread):
        def __init__(self):
            super().__init__(name="RpcThread")
            self.rpc = pypresence.Presence(963434684669382696)
            self.state: str | None = "In Game"
            self.details: str | None = "Main Menu"
            self.start_timestamp = time.mktime(time.localtime())
            self.large_image_key: str | None = "bombsquadicon"
            self.large_image_text: str | None = "BombSquad Icon"
            self.small_image_key: str | None = None
            self.small_image_text: str | None = None
            self.party_id: str = str(uuid.uuid4())
            self.party_size = 1
            self.party_max = 8
            self.join_secret: str | None = None
            self._last_update_time: float = 0
            self._last_secret_update_time: float = 0
            self._last_connect_time: float = 0
            self.should_close = False
            self.connection_to_host_info = None

        @staticmethod
        def is_discord_running():
            for i in range(6463, 6473):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.01)
                try:
                    conn = s.connect_ex(("localhost", i))
                    s.close()
                    if conn == 0:
                        s.close()
                        return True
                except:
                    s.close()
                    return False

        def _generate_join_secret(self):
            # resp = requests.get('https://legacy.ballistica.net/bsAccessCheck').text
            try:
                connection_info = self.connection_to_host_info
                if connection_info:
                    addr = _last_server_addr
                    port = _last_server_port
                else:
                    with urlopen("https://legacy.ballistica.net/bsAccessCheck") as resp:
                        resp = resp.read().decode()
                    resp = ast.literal_eval(resp)
                    addr = resp["address"]
                    port = resp["port"]
                    addr, port = addr, port
                secret_dict = {
                    "format_version": 1,
                    "hostname": addr,
                    "port": port,
                }

                self.join_secret = json.dumps(secret_dict)
            except Exception as _:
                pass

        def _update_secret(self):
            #! use in game thread
            threading.Thread(target=self._generate_join_secret, daemon=True).start()
            self._last_secret_update_time = time.time()

        def run(self) -> None:
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            asyncio.set_event_loop(get_event_loop())

            while not self.should_close:
                if time.time() - self._last_update_time > 0.1:
                    self._do_update_presence()
                if time.time() - self._last_secret_update_time > 15:
                    self._update_secret()
                time.sleep(0.03)

        def _subscribe(self, event: str, **args):
            self.rpc.send_data(
                1,
                {
                    "nonce": f"{time.time():.20f}",
                    "cmd": "SUBSCRIBE",
                    "evt": event,
                    "args": args,
                },
            )
            data = self.rpc.loop.run_until_complete(self.rpc.read_output())
            self.handle_event(data)

        def _subscribe_events(self):
            self._subscribe("ACTIVITY_JOIN")
            self._subscribe("ACTIVITY_JOIN_REQUEST")

        # def _update_presence(self) -> None:
        #     self._last_update_time = time.time()
        #     try:
        #         self._do_update_presence()
        #     except (AttributeError, AssertionError):
        #         try:
        #             self._reconnect()
        #         except Exception:
        #             print_error("failed to update presence", include_exception= True)

        def _reconnect(self) -> None:
            self.rpc.connect()
            self._subscribe_events()
            self._do_update_presence()
            self._last_connect_time = time.time()

        def _do_update_presence(self) -> None:
            if RpcThread.is_discord_running():
                self._last_update_time = time.time()
                try:
                    data = self.rpc.update(
                        state=self.state or "  ",
                        details=self.details,
                        start=start_time,
                        large_image=self.large_image_key,
                        large_text=self.large_image_text,
                        small_image=self.small_image_key,
                        small_text=self.small_image_text,
                        party_id=self.party_id,
                        party_size=[self.party_size, self.party_max],
                        join=self.join_secret,
                    )
                    self.handle_event(data)
                except (PipeClosed, DiscordError, AssertionError, AttributeError):
                    try:
                        self._reconnect()
                    except (DiscordNotFound, DiscordError):
                        pass

        def handle_event(self, data):
            evt = data["evt"]
            if evt is None:
                return

            data = data.get("data", {})

            if evt == "ACTIVITY_JOIN":
                secret = data.get("secret")
                try:
                    server = json.loads(secret)
                    format_version = server["format_version"]
                except Exception:
                    logging.exception("discordrp: unknown activity join format")
                else:
                    try:
                        if format_version == 1:
                            hostname = server["hostname"]
                            port = server["port"]
                            self._connect_to_party(hostname, port)
                    except Exception:
                        logging.exception(
                            f"discordrp: incorrect activity join data, {format_version=}"
                        )

            elif evt == "ACTIVITY_JOIN_REQUEST":
                user = data.get("user", {})
                uid = user.get("id")
                username = user.get("username")
                avatar = user.get("avatar")
                self.on_join_request(username, uid, avatar)

        def _connect_to_party(self, hostname, port) -> None:
            babase.pushcall(
                babase.Call(bs.connect_to_party, hostname, port), from_other_thread=True
            )

        def on_join_request(self, username, uid, avatar) -> None:
            del uid  # unused
            del avatar  # unused
            babase.pushcall(
                babase.Call(
                    bui.screenmessage,
                    "Discord: {} wants to join!".format(username),
                    color=(0.0, 1.0, 0.0),
                ),
                from_other_thread=True,
            )
            #! check this function for sound creation error
            babase.pushcall(
                lambda: bui.getsound("bellMed").play(), from_other_thread=True
            )


class Discordlogin(PopupWindow):

    def __init__(self):
        # pylint: disable=too-many-locals
        _uiscale = bui.app.ui_v1.uiscale
        self._transitioning_out = False
        s = (
            1.25
            if _uiscale is babase.UIScale.SMALL
            else 1.27 if _uiscale is babase.UIScale.MEDIUM else 1.3
        )
        self._width = 380 * s
        self._height = 150 + 150 * s
        bg_color = (0.5, 0.4, 0.6)
        log_btn_colour = (
            (0.10, 0.95, 0.10)
            if not babase.app.config.get("encrypted_tokey")
            else (1.00, 0.15, 0.15)
        )
        log_txt = (
            "LOG IN" if not babase.app.config.get("encrypted_tokey") else "LOG OUT"
        )
        self.code = False
        self.resp = "Placeholder"
        # Plucked  from https://gist.github.com/brostosjoined/3bb7b96c1f6397d389427f46e104005f
        import base64

        X_Super_Properties = {
            "os": "Android",
            "browser": "Android Chrome",
            # ! Find the devices original (Linux; Android 10; K)
            "browser_user_agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
        }
        self.headers = {
            "User-Agent": X_Super_Properties["browser_user_agent"],
            "Content-Type": "application/json",
            "X-Super-Properties": base64.b64encode(
                json.dumps(X_Super_Properties).encode()
            ).decode(),
        }

        # creates our _root_widget
        PopupWindow.__init__(
            self,
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=(
                2.1
                if _uiscale is babase.UIScale.SMALL
                else 1.5 if _uiscale is babase.UIScale.MEDIUM else 1.0
            ),
            bg_color=bg_color,
        )

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(25, self._height - 40),
            size=(50, 50),
            scale=0.58,
            label="",
            color=bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture("crossOut"),
            iconscale=1.2,
        )

        bui.imagewidget(
            parent=self.root_widget,
            position=(180, self._height - 55),
            size=(32 * s, 32 * s),
            texture=bui.gettexture("discordLogo"),
            color=(10 - 0.32, 10 - 0.39, 10 - 0.96),
        )

        self.email_widget = bui.textwidget(
            parent=self.root_widget,
            text="Email/Phone Number",
            size=(400, 70),
            position=(50, 180),
            h_align="left",
            v_align="center",
            editable=True,
            scale=0.8,
            autoselect=True,
            maxwidth=220,
        )

        self.password_widget = bui.textwidget(
            parent=self.root_widget,
            text="Password",
            size=(400, 70),
            position=(50, 120),
            h_align="left",
            v_align="center",
            editable=True,
            scale=0.8,
            autoselect=True,
            maxwidth=220,
        )

        bui.containerwidget(edit=self.root_widget, cancel_button=self._cancel_button)

        bui.textwidget(
            parent=self.root_widget,
            position=(265, self._height - 37),
            size=(0, 0),
            h_align="center",
            v_align="center",
            scale=1.0,
            text="Discord",
            maxwidth=200,
            color=(0.80, 0.80, 0.80),
        )

        bui.textwidget(
            parent=self.root_widget,
            position=(265, self._height - 78),
            size=(0, 0),
            h_align="center",
            v_align="center",
            scale=1.0,
            text="??Use at your own risk??\n ??discord account might get terminated??",
            maxwidth=200,
            color=(1.00, 0.15, 0.15),
        )

        self._login_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(120, 65),
            size=(400, 80),
            scale=0.58,
            label=log_txt,
            color=log_btn_colour,
            on_activate_call=self.login,
            autoselect=True,
        )

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition="out_scale")

    def on_bascenev1libup_cancel(self) -> None:
        bui.getsound("swish").play()
        self._transition_out()

    def backup_2fa_code(self, ticket):
        if babase.do_once():
            self.email_widget.delete()
            self.password_widget.delete()

            self.backup_2fa_widget = bui.textwidget(
                parent=self.root_widget,
                text="2FA/Discord Backup code",
                size=(400, 70),
                position=(50, 120),
                h_align="left",
                v_align="center",
                editable=True,
                scale=0.8,
                autoselect=True,
                maxwidth=220,
            )

        mfa_json = {
            "code": bui.textwidget(query=self.backup_2fa_widget),
            "ticket": ticket,
            "login_source": None,
            "gift_code_sku_id": None
        }
        code = mfa_json["code"]
        if len(code) == 6 and code.isdigit():  # len the backup code and check if it number for 2fa
            try:
                payload_2FA = json.dumps(mfa_json, separators=(',', ':'))
                conn_2FA = http.client.HTTPSConnection("discord.com")
                conn_2FA.request(
                    "POST", "/api/v9/auth/mfa/totp", payload_2FA, self.headers
                )
                res_2FA = conn_2FA.getresponse().read()
                token = json.loads(res_2FA)["token"]
                PresenceUpdate.brosCrypt(token)
                bui.screenmessage("Successfully logged in", (0.21, 1.0, 0.20))
                bui.getsound("shieldUp").play()
                self.on_bascenev1libup_cancel()
                PresenceUpdate().start()
            except:
                self.code = True
                bui.screenmessage("Incorrect code", (1.00, 0.15, 0.15))
                bui.getsound("error").play()

    def login(self):
        if not babase.app.config.get("encrypted_tokey") and self.code == False:
            try:

                login_json = {
                    "login": bui.textwidget(query=self.email_widget),
                    "password": bui.textwidget(query=self.password_widget),
                    "undelete": False,
                    "login_source": None,
                    "gift_code_sku_id": None,
                }

                conn = http.client.HTTPSConnection("discord.com")

                login_payload = json.dumps(login_json, separators=(",", ":"))
                conn.request("POST", "/api/v9/auth/login", login_payload, self.headers)
                login_res = conn.getresponse().read()

                try:
                    token = json.loads(login_res)["token"]
                    PresenceUpdate.brosCrypt(token)
                    bui.screenmessage("Successfully logged in", (0.21, 1.0, 0.20))
                    bui.getsound("shieldUp").play()
                    self.on_bascenev1libup_cancel()
                    PresenceUpdate().start()
                except KeyError:
                    try:
                        ticket = json.loads(login_res)["ticket"]
                        bui.screenmessage(
                            "Input your 2FA or Discord Backup code", (0.21, 1.0, 0.20)
                        )
                        bui.getsound("error").play()
                        self.resp = ticket
                        self.backup_2fa_code(ticket=ticket)
                        self.code = True
                    except KeyError:
                        bui.screenmessage("Incorrect credentials", (1.00, 0.15, 0.15))
                        bui.getsound("error").play()

            except:
                bui.screenmessage("Connect to the internet", (1.00, 0.15, 0.15))
                bui.getsound("error").play()

            conn.close()
        elif self.code == True:
            self.backup_2fa_code(ticket=self.resp)

        else:
            self.email_widget.delete()
            self.password_widget.delete()
            del babase.app.config["encrypted_tokey"]
            babase.app.config.commit()
            bui.getsound("shieldDown").play()
            bui.screenmessage("Account successfully removed!!", (0.10, 0.10, 1.00))
            self.on_bascenev1libup_cancel()
            PresenceUpdate().close()


def get_class():
    if ANDROID:
        return PresenceUpdate()
    elif not ANDROID:
        return RpcThread()


# ba_meta export babase.Plugin
class DiscordRP(babase.Plugin):
    def __init__(self) -> None:
        self.update_timer: bs.Timer | None = None
        self.rpc_thread = get_class()
        self._last_server_info: str | None = None

        if not ANDROID:
            _run_overrides()

    def on_app_running(self) -> None:
        if not ANDROID:
            threading.Thread(
                target=self.rpc_thread.start, daemon=True, name="start_rpc"
            ).start()

            self.update_timer = bs.AppTimer(
                1, bs.WeakCall(self.update_status), repeat=True
            )
        if ANDROID:
            self.rpc_thread.start()
            self.update_timer = bs.AppTimer(
                4, bs.WeakCall(self.update_status), repeat=True
            )

    def has_settings_ui(self):
        if ANDROID:
            return True
        else:
            return False

    def show_settings_ui(self, button):
        Discordlogin()

    def on_app_shutdown(self) -> None:
        if not ANDROID and self.rpc_thread.is_discord_running():
            self.rpc_thread.rpc.close()
            self.rpc_thread.should_close = True

    def on_app_pause(self) -> None:
        self.rpc_thread.close()

    def on_app_resume(self) -> None:
        global start_time
        start_time = time.time()
        self.rpc_thread.start()

    def _get_current_activity_name(self) -> str | None:
        act = bs.get_foreground_host_activity()
        if isinstance(act, bs.GameActivity):
            return act.name

        this = "Lobby"
        name: str | None = (
            act.__class__.__name__.replace("Activity", "")
            .replace("ScoreScreen", "Ranking")
            .replace("Coop", "")
            .replace("MultiTeam", "")
            .replace("Victory", "")
            .replace("EndSession", "")
            .replace("Transition", "")
            .replace("Draw", "")
            .replace("FreeForAll", "")
            .replace("Join", this)
            .replace("Team", "")
            .replace("Series", "")
            .replace("CustomSession", "Custom Session(mod)")
        )

        if name == "MainMenu":
            name = "Main Menu"
        if name == this:
            self.rpc_thread.large_image_key = "lobby"
            self.rpc_thread.large_image_text = "Bombing up"
            self.rpc_thread.small_image_key = "lobbysmall"
        if name == "Ranking":
            self.rpc_thread.large_image_key = "ranking"
            self.rpc_thread.large_image_text = "Viewing Results"
        return name

    def _get_current_map_name(self) -> Tuple[str | None, str | None]:
        act = bs.get_foreground_host_activity()
        if isinstance(act, bs.GameActivity):
            texname = act.map.get_preview_texture_name()
            if texname:
                return act.map.name, texname.lower().removesuffix("preview")
        return None, None

    def update_status(self) -> None:
        roster = bs.get_game_roster()
        try:
            connection_info = (
                bs.get_connection_to_host_info()
                if build_number < 21727
                else bs.get_connection_to_host_info_2()
            )
            self.rpc_thread.connection_to_host_info = connection_info
        except (RuntimeError, TypeError):
            pass

        self.rpc_thread.large_image_key = "bombsquadicon"
        self.rpc_thread.large_image_text = "BombSquad"
        self.rpc_thread.small_image_key = _babase.app.classic.platform
        self.rpc_thread.small_image_text = (
            f"{_babase.app.classic.platform.capitalize()}({APP_VERSION})"
        )
        try:
            if not ANDROID:
                svinfo = str(connection_info)
                if self._last_server_info != svinfo:
                    self._last_server_info = svinfo
                    self.rpc_thread.party_id = str(uuid.uuid4())
                    self.rpc_thread._update_secret()

            if connection_info:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)

                if bs.get_connection_to_host_info_2().address == local_ip:
                    self.rpc_thread.details = "Local Server"
                else:
                    self.rpc_thread.details = "Online"

                servername = connection_info.name
                self.rpc_thread.party_size = max(
                    1, sum(len(client["players"]) for client in roster)
                )
                self.rpc_thread.party_max = max(8, self.rpc_thread.party_size)
                if len(servername) == 19 and "Private Party" in servername:
                    self.rpc_thread.state = "Private Party"
                elif servername == "":  # A local game joinable from the internet
                    try:
                        offlinename = json.loads(
                            bs.get_game_roster()[0]["spec_string"]
                        )["n"]
                        if len(offlinename) > 19:  # Thanks Rikko
                            self.rpc_thread.state = offlinename[slice(19)] + "..."
                        else:
                            self.rpc_thread.state = offlinename
                    except IndexError:
                        pass
                else:
                    if len(servername) > 19:
                        self.rpc_thread.state = servername[slice(19)] + ".."
                    else:
                        self.rpc_thread.state = servername[slice(19)]

            if not connection_info:
                self.rpc_thread.details = (
                    "Local"  # ! replace with something like ballistica github cause
                )
                self.rpc_thread.state = self._get_current_activity_name()
                self.rpc_thread.party_size = max(1, len(roster))
                self.rpc_thread.party_max = max(1, bs.get_public_party_max_size())

                if (
                    bs.get_foreground_host_session() is not None
                    and self.rpc_thread.details == "Local"
                ):
                    session = (
                        bs.get_foreground_host_session()
                        .__class__.__name__.replace("MainMenuSession", "")
                        .replace("EndSession", "")
                        .replace("FreeForAllSession", ": FFA")
                        .replace("DualTeamSession", ": Teams")
                        .replace("CoopSession", ": Coop")
                    )
                    if len(session) > 1:
                        self.rpc_thread.small_image_key = session.replace(
                            ": ", ""
                        ).lower()
                        self.rpc_thread.small_image_text = session.replace(": ", "")
                    self.rpc_thread.details = self.rpc_thread.details
                if (
                    self.rpc_thread.state == "NoneType"
                ):  # sometimes the game just breaks which means its not really watching replay FIXME
                    self.rpc_thread.state = "Watching Replay"
                    self.rpc_thread.large_image_key = "replay"
                    self.rpc_thread.large_image_text = "Viewing Awesomeness"
                    self.rpc_thread.small_image_key = "replaysmall"
        except UnboundLocalError:
            pass

        act = bs.get_foreground_host_activity()
        session = bs.get_foreground_host_session()
        if act:
            from bascenev1lib.game.elimination import EliminationGame
            from bascenev1lib.game.thelaststand import TheLastStandGame
            from bascenev1lib.game.meteorshower import MeteorShowerGame
            from bascenev1lib.game.football import FootballCoopGame
            from bascenev1lib.game.easteregghunt import EasterEggHuntGame

            # noinspection PyUnresolvedReferences,PyProtectedMember
            try:
                self.rpc_thread.start_timestamp = act._discordrp_start_time  # type: ignore
            except AttributeError:
                # This can be the case if plugin launched AFTER activity
                # has been created; in that case let's assume it was
                # created just now.
                self.rpc_thread.start_timestamp = act._discordrp_start_time = time.mktime(  # type: ignore
                    time.localtime()
                )
            if isinstance(act, EliminationGame):
                alive_count = len([p for p in act.players if p.lives > 0])
                self.rpc_thread.details += f" ({alive_count} players left)"
            elif isinstance(act, TheLastStandGame):
                # noinspection PyProtectedMember
                points = act._score
                self.rpc_thread.details += f" ({points} points)"
            elif isinstance(act, MeteorShowerGame):
                with act.context:
                    sec = bs.time() - act._timer.getstarttime()
                secfmt = ""
                if sec < 60:
                    secfmt = f"{sec:.2f}"
                else:
                    secfmt = f"{int(sec) // 60:02}:{sec:.2f}"
                self.rpc_thread.details += f" ({secfmt})"
            # elif isinstance(act, OnslaughtGame):
            #     score = act._score
            #     level = act._wavenum
            #     # self.
            elif isinstance(act, FootballCoopGame):
                # try:
                #     score = f"{act.teams[0].score} : {act.teams[1].score}"
                # except IndexError:
                score = f"{act.teams[0].score} : {act._bot_team.score}"
                self.rpc_thread.details = score
            # elif isinstance(act, RunaroundGame)
            #     score = act._score
            #     level = act._wavenum
            #     lives = act._lives
            elif isinstance(act, EasterEggHuntGame):
                eggs_collected = len(act._eggs) - 1
                self.rpc_thread.details = f"{eggs_collected} eggs collected"
            # elif isinstance(act, TargetPracticeGame):
            #     #for FFA
            #     scoere = bs.get_foreground_host_activity().players[0].score

            # if isinstance(session, ba.DualTeamSession):
            #     scores = ':'.join([
            #         str(t.customdata['score'])
            #         for t in session.sessionteams
            #     ])
            #     self.rpc_thread.details += f' ({scores})'

        mapname, short_map_name = self._get_current_map_name()
        if mapname:
            asset_keys = MAPNAME_ID.keys()
            if short_map_name in asset_keys:
                self.rpc_thread.large_image_text = mapname
                self.rpc_thread.large_image_key = short_map_name
                # self.rpc_thread.small_image_key = 'bombsquadlogo2'
                # self.rpc_thread.small_image_text = 'BombSquad'

        if _babase.get_idle_time() / (1000 * 60) % 60 >= 0.4:
            self.rpc_thread.details = f"AFK in {self.rpc_thread.details}"
            if not ANDROID:
                self.rpc_thread.large_image_key = (
                    "https://media.tenor.com/uAqNn6fv7x4AAAAM/bombsquad-spaz.gif"
                )
        if babase.app.config.get("encrypted_tokey") and ANDROID:
            #! This function might cause some errors
            try:
                self.rpc_thread.presence()
            except Exception as e:
                # raise (e)
                pass
