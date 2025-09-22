# ba_meta require api 9
from __future__ import annotations

import threading
import select
import socket
import json
import babase
import bascenev1 as bs
import time
from time import mktime


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def __init__(self):
        #print("[SERVER][INIT] Plugin byLess inicializado")

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
        #print("[SERVER][DEBUG] Configurando timer...")
        babase.apptimer(1.0, self.start_timer)

        # Start HTTP server
        try:
            self.start_http_server(host="127.0.0.1", port=self._http_port)
        except Exception as e:
            print("[SERVER][HTTP] Could not start HTTP server:", e)

    def start_timer(self):
        #print("[SERVER][DEBUG] Timer iniciado (cada 0.9s)")
        # Run every 0.9 seconds
        self._timer = babase.AppTimer(0.9, self.main, repeat=True)

    def main(self):
        #print("[SERVER][DEBUG] Ejecutando main()")
        try:
            self.getstatus()
        except Exception as e:
            import traceback
            print("[SERVER][ERROR]", e)
            traceback.print_exc()

    def getstatus(self):
        #print("[SERVER][DEBUG] Ejecutando getstatus()")
    
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
        #print(f"[SERVER] Nombre: {name}")
        #print(f"[SERVER] IP: {ip}")
        #print(f"[SERVER] Puerto: {port}")
        #print(f"[SERVER] Jugadores: {players_str}")
    
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
            #print("[SERVER][DEBUG] Estado actualizado en _last_status")
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
            print("[SERVER][HTTP] Error stopping server:", e)

    def _http_server_loop(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(5)
            sock.setblocking(False)
            self._http_sock = sock
        except Exception as e:
            print("[SERVER][HTTP] Could not bind socket:", e)
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
        print("[SERVER][HTTP] Server stopped")

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
