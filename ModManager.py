# ba_meta require api 9
# ba_meta description A mod that allows you to easily install, update and delete multiple mods in the remote repository
# ba_meta version 1.1.3
# ba_meta nomod

import urllib.request
import http.client
import socket
import json
import ssl
import re
import os
import sys
import copy
import asyncio
import hashlib
import contextlib
from typing import override
from datetime import datetime
import logging

import babase
import _babase
import bauiv1 as bui
from bauiv1lib import popup, confirm
from bauiv1lib.settings.allsettings import AllSettingsWindow


MOD_MANAGER_VERSION = "1.1.3"
MOD_MANAGER_MOD = "https://raw.githubusercontent.com/danigomezdev/bombsquad/refs/heads/modmanager/ModManager.py"
REPOSITORY_URL = "https://github.com/danigomezdev/bombsquad/tree/modmanager"
MODS_DATA_URL = "https://raw.githubusercontent.com/danigomezdev/bombsquad/refs/heads/modmanager/data.json"
CURRENT_TAG = "modmanager"

_env = _babase.env()
_app_api_version = babase.app.env.api_version

HEADERS = {
    "User-Agent": _env["legacy_user_agent_string"],
}
PLUGIN_DIRECTORY = _env["python_directory_user"]
loop = babase._asyncio._asyncio_event_loop

open_popups = []
MAIN_COLOR = (0.23, 0.23, 0.23)

def _add_popup(popup): open_popups.append(popup)

def _remove_popup(popup):
    try:
        open_popups.remove(popup)
    except ValueError:
        pass

def _uiscale(): return bui.app.ui_v1.uiscale

DISCORD_URL = "https://discord.gg/q5GdnP85Ky"
_CACHE = {}

class MD5CheckSumFailed(Exception):
    pass


class PluginNotInstalled(Exception):
    pass


class CategoryDoesNotExist(Exception):
    pass


class NoCompatibleVersion(Exception):
    pass


class PluginSourceNetworkError(Exception):
    pass


class CategoryMetadataParseError(Exception):
    pass


def send_network_request(request):
    return urllib.request.urlopen(request)


async def async_send_network_request(request):
    response = await loop.run_in_executor(None, send_network_request, request)
    return response


def stream_network_response_to_file(request, file, md5sum=None, retries=3):
    response = urllib.request.urlopen(request)
    chunk_size = 16 * 1024
    content = b""
    with open(file, "wb") as fout:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            fout.write(chunk)
            content += chunk
    if md5sum and hashlib.md5(content).hexdigest() != md5sum:
        if retries <= 0:
            raise MD5CheckSumFailed("MD5 checksum match failed.")
        return stream_network_response_to_file(
            request,
            file,
            md5sum=md5sum,
            retries=retries-1,
        )
    return content


async def async_stream_network_response_to_file(request, file, md5sum=None, retries=3):

    content = await loop.run_in_executor(
        None,
        stream_network_response_to_file,
        request,
        file,
        md5sum,
        retries,
    )
    return content

async def check_for_update():
    """
    Checks if a new version of the Mod Manager is available.
    Returns a dictionary with information about the update.
    """
    try:
        #print("DEBUG: Checking for update...")
        
        # Create request for the mod manager file
        request = urllib.request.Request(
            MOD_MANAGER_MOD,
            headers=HEADERS,
        )
        
        # Download the contents of the remote file
        response = await async_send_network_request(request)
        remote_content = response.read().decode('utf-8')
        
        # Find version in content using regex
        version_pattern = r'#\s*ba_meta\s+version\s+([\d.]+)'
        version_match = re.search(version_pattern, remote_content)
        
        if not version_match:
            #print("DEBUG: Version not found in remote file")
            return {
                'update_available': False,
                'current_version': MOD_MANAGER_VERSION,
                'remote_version': None
            }
            
        remote_version = version_match.group(1)
        current_version = MOD_MANAGER_VERSION
        
        #print(f"DEBUG: Local version: {current_version}, Remote version: {remote_version}")
        
        # Compare versions
        if remote_version != current_version:
            #print(f"DEBUG: New version available: {remote_version}")
            return {
                'update_available': True,
                'current_version': current_version,
                'remote_version': remote_version
            }
        else:
            #print("DEBUG: The Mod Manager is updated")
            return {
                'update_available': False,
                'current_version': current_version,
                'remote_version': remote_version
            }
            
    except Exception as e:
        #print(f"DEBUG: Error checking for update: {e}")
        return {
            'update_available': False,
            'current_version': MOD_MANAGER_VERSION,
            'remote_version': None
        }

async def update_mod_manager(current_version, remote_version):
    """
    Download and update Mod Manager to the latest version.
    Display messages to the user during the process.
    """
    global MOD_MANAGER_VERSION  
    
    try:
        # Show startup message
        bui.screenmessage(f"Actualizando Mod Manager a v{remote_version}", color=(0, 1, 0))
        
        # Download the remote file
        request = urllib.request.Request(
            MOD_MANAGER_MOD,
            headers=HEADERS,
        )
        
        response = await async_send_network_request(request)
        remote_content = response.read().decode('utf-8')
        
        # Get the current mod manager file path
        current_file_path = sys.modules[__name__].__file__
        
        # Write the new content
        with open(current_file_path, 'w', encoding='utf-8') as f:
            f.write(remote_content)
        
        # Success message
        bui.screenmessage("¡Mod Manager actualizado! Reinicia el juego.", color=(0, 1, 0))
        bui.getsound('shieldUp').play()
        #print(f"DEBUG: Mod Manager updated from {current_version} to {remote_version}")
        MOD_MANAGER_VERSION = str(remote_version)
        return True
        
    except Exception as e:
        # Error message
        #print(f"DEBUG: Error during update: {e}")
        bui.screenmessage("Error al actualizar Mod Manager", color=(1, 0, 0))
        bui.getsound('error').play()
        return False

async def auto_update_mod_manager():
    """
    Automatically checks if a new version of Mod Manager is available
    and updates it if necessary.
    """
    
    if not babase.app.config["Mod Manager"]["Settings"]["Actualizar automáticamente Mod Manager"]:
        return
    
    # Check if an update is available
    update_info = await check_for_update()
    
    #print(f"Current version: {update_info['current_version']}")
    #if update_info['remote_version']:
    #    print(f"Remote version: {update_info['remote_version']}")
    
    if not update_info['update_available']:
        return
    
    await update_mod_manager(update_info['current_version'], update_info['remote_version'])

def partial_format(string_template, **kwargs):
    for key, value in kwargs.items():
        string_template = string_template.replace("{" + key + "}", value)
    return string_template


class DNSBlockWorkaround:
    """
    Some ISPs put a DNS block on domains that are needed for plugin manager to
    work properly. This class stores methods to workaround such blocks by adding
    dns.google as a fallback.

    Such as Jio, a pretty popular ISP in India has a DNS block on
    raw.githubusercontent.com (sigh..).

    References:
      * https://github.com/orgs/community/discussions/42655

    Usage:
    -----
    >>> import urllib.request
    >>> import http.client
    >>> import socket
    >>> import ssl
    >>> import json
    >>> DNSBlockWorkaround.apply()
    >>> response = urllib.request.urlopen("https://dnsblockeddomain.com/path/to/resource/")
    """

    _google_dns_cache = {}

    def apply():
        opener = urllib.request.build_opener(
            DNSBlockWorkaround._HTTPHandler,
            DNSBlockWorkaround._HTTPSHandler,
        )
        urllib.request.install_opener(opener)

    def _resolve_using_google_dns(hostname):
        response = urllib.request.urlopen(f"https://dns.google/resolve?name={hostname}")
        response = response.read()
        response = json.loads(response)
        resolved_host = response["Answer"][0]["data"]
        return resolved_host

    def _resolve_using_system_dns(hostname):
        resolved_host = socket.gethostbyname(hostname)
        return resolved_host

    def _resolve_with_workaround(hostname):
        resolved_host_from_cache = DNSBlockWorkaround._google_dns_cache.get(hostname)
        if resolved_host_from_cache:
            return resolved_host_from_cache

        resolved_host_by_system_dns = DNSBlockWorkaround._resolve_using_system_dns(hostname)

        if DNSBlockWorkaround._is_blocked(hostname, resolved_host_by_system_dns):
            resolved_host = DNSBlockWorkaround._resolve_using_google_dns(hostname)
            DNSBlockWorkaround._google_dns_cache[hostname] = resolved_host
        else:
            resolved_host = resolved_host_by_system_dns

        return resolved_host

    def _is_blocked(hostname, address):
        is_blocked = False
        if hostname == "raw.githubusercontent.com":
            # Jio's DNS server may be blocking it.
            is_blocked = address.startswith("49.44.")

        return is_blocked

    class _HTTPConnection(http.client.HTTPConnection):
        def connect(self):
            host = DNSBlockWorkaround._resolve_with_workaround(self.host)
            self.sock = socket.create_connection(
                (host, self.port),
                self.timeout,
            )

    class _HTTPSConnection(http.client.HTTPSConnection):
        def connect(self):
            host = DNSBlockWorkaround._resolve_with_workaround(self.host)
            sock = socket.create_connection(
                (host, self.port),
                self.timeout,
            )
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
            sock = context.wrap_socket(sock, server_hostname=self.host)
            self.sock = sock

    class _HTTPHandler(urllib.request.HTTPHandler):
        def http_open(self, req):
            return self.do_open(DNSBlockWorkaround._HTTPConnection, req)

    class _HTTPSHandler(urllib.request.HTTPSHandler):
        def https_open(self, req):
            return self.do_open(DNSBlockWorkaround._HTTPSConnection, req)


class StartupTasks:
    def __init__(self):
        self.plugin_manager = ModManager()

    def setup_config(self):
        # is_config_updated = False
        existing_plugin_manager_config = copy.deepcopy(
            babase.app.config.get("Mod Manager"))

        plugin_manager_config = babase.app.config.setdefault("Mod Manager", {})
        plugin_manager_config.setdefault("Custom Sources", [])
        installed_plugins = plugin_manager_config.setdefault("Installed Plugins", {})
        for plugin_name in tuple(installed_plugins.keys()):
            plugin = PluginLocal(plugin_name)
            if not plugin.is_installed:
                del installed_plugins[plugin_name]

        # This order is the options will show up in Settings window.
        current_settings = {
            "Actualizar automáticamente Mod Manager": True,
            "Actualizar automáticamente los mods": True,
            "Habilitar mods automáticamente después de la instalación": True,
            "Notificar nuevos mods": True
        }
                
        #current_settings = {
        #    "Auto Update Mod Manager": True,
        #    "Auto Update Plugins": True,
        #    "Auto Enable Plugins After Installation": True,
        #    "Notify New Plugins": True
        #}

        settings = plugin_manager_config.setdefault("Settings", {})

        for setting, value in settings.items():
            if setting in current_settings:
                current_settings[setting] = value

        plugin_manager_config["Settings"] = current_settings

        if plugin_manager_config != existing_plugin_manager_config:
            babase.app.config.commit()

    async def update_plugin_manager(self):
        if not babase.app.config["Mod Manager"]["Settings"]["Actualizar automáticamente Mod Manager"]:
            return
        update_details = await self.plugin_manager.get_update_details()
        if update_details:
            to_version, commit_sha = update_details
            bui.screenmessage(f"Mod Manager is being updated to v{to_version}")
            try:
                await self.plugin_manager.update(to_version, commit_sha)
            except MD5CheckSumFailed:
                bui.getsound('error').play()
            else:
                bui.screenmessage("Update successful. Restart game to reload changes.",
                                  color=(0, 1, 0))
                bui.getsound('shieldUp').play()

    async def update_plugins(self):
        if not babase.app.config["Mod Manager"]["Settings"]["Actualizar automáticamente los mods"]:
            return
        await self.plugin_manager.setup_index()
        all_plugins = await self.plugin_manager.categories["All"].get_plugins()
        plugins_to_update = []
        for plugin in all_plugins:
            if plugin.is_installed and await plugin.get_local().is_enabled() and plugin.has_update():
                plugins_to_update.append(plugin.update())
        await asyncio.gather(*plugins_to_update)

    @staticmethod
    def _is_new_supported_plugin(plugin):
        is_an_update = len(plugin.versions) > 1
        if is_an_update:
            return False
        try:
            plugin.latest_compatible_version
        except NoCompatibleVersion:
            return False
        else:
            return True

    async def notify_new_plugins(self):
        if not babase.app.config["Mod Manager"]["Settings"]["Notificar nuevos mods"]:
            return
        show_max_names = 2
        await self.plugin_manager.setup_index()
        new_num_of_plugins = len(await self.plugin_manager.categories["All"].get_plugins())
        try:
            existing_num_of_plugins = babase.app.config["Mod Manager"]["Existing Number of Plugins"]
        except KeyError:
            babase.app.config["Mod Manager"]["Existing Number of Plugins"] = new_num_of_plugins
            babase.app.config.commit()
            return

        def title_it(plug):
            plug = str(plug).replace('_', ' ').title()
            return plug
        if existing_num_of_plugins < new_num_of_plugins:
            new_plugin_count = new_num_of_plugins - existing_num_of_plugins
            all_plugins = await self.plugin_manager.categories["All"].get_plugins()
            new_supported_plugins = list(filter(self._is_new_supported_plugin, all_plugins))
            new_supported_plugins.sort(
                key=lambda plugin: plugin.latest_compatible_version.released_on_date,
                reverse=True,
            )
            new_supported_plugins = new_supported_plugins[:new_plugin_count]
            new_supported_plugins_count = len(new_supported_plugins)
            if new_supported_plugins_count > 0:
                new_supported_plugins = ", ".join(map(title_it, (new_supported_plugins
                                                                 if new_supported_plugins_count <= show_max_names else
                                                                 new_supported_plugins[0:show_max_names])
                                                      ))
                if new_supported_plugins_count == 1:
                    notification_text = f"{new_supported_plugins_count} new plugin ({new_supported_plugins}) is available!"
                else:
                    notification_text = new_supported_plugins + \
                        ('' if new_supported_plugins_count <= show_max_names else ' and +' +
                         str(new_supported_plugins_count-show_max_names)) + " new plugins are available"
                bui.screenmessage(notification_text, color=(0, 1, 0))

        if existing_num_of_plugins != new_num_of_plugins:
            babase.app.config["Mod Manager"]["Existing Number of Plugins"] = new_num_of_plugins
            babase.app.config.commit()

    async def execute(self):
        self.setup_config()
        try:
            await auto_update_mod_manager()

            await asyncio.gather(
                self.update_plugin_manager(),
                self.update_plugins(),
                self.notify_new_plugins(),
            )
        except urllib.error.URLError:
            pass


class Category:
    def __init__(self, meta_url, tag=CURRENT_TAG):
        self.meta_url = meta_url
        self.tag = tag
        self.request_headers = HEADERS
        self._metadata = _CACHE.get("categories", {}).get(meta_url, {}).get("metadata")
        self._plugins = _CACHE.get("categories", {}).get(meta_url, {}).get("plugins")

    async def fetch_metadata(self):
        if self._metadata is None:
            request = urllib.request.Request(
                self.meta_url,
                headers=self.request_headers,
            )
            response = await async_send_network_request(request)
            self._metadata = json.loads(response.read())
            self.set_category_global_cache("metadata", self._metadata)
        return self

    async def get_description(self):
        return "Less mods collection"
    
    async def get_plugins(self):
        if self._plugins is None:
            try:
                await self.fetch_metadata()
                self._plugins = []

                for mod_data in self._metadata:
                    try:
                        if not all(key in mod_data for key in ['name', 'description', 'url_raw_mod', 'api_version', 'file_name']):
                            print(f"ERROR Mod data incompleto: {mod_data.get('name', 'unknown')}")
                            continue
                        
                        #print(f"DEBUG: Processing mod: {mod_data['name']} -> {mod_data['file_name']}")
                        
                        plugin_info = (
                            mod_data["name"],
                            {
                                "description": mod_data["description"],
                                "authors": [{"name": mod_data.get("author", "Community")}],
                                "external_url": mod_data.get("url_mod", ""),
                                "readme_url": mod_data.get("url_readme", ""),
                                "versions": {
                                    mod_data.get("version", "1.0.0"): {
                                        "api_version": mod_data["api_version"],
                                        "released_on": mod_data.get("released_on", "01-01-2024"),
                                        "commit_sha": "unknown",
                                        "md5sum": mod_data.get("md5sum", "")
                                    }
                                }
                            }
                        )
                        plugin = Plugin(
                            plugin_info,
                            mod_data["url_raw_mod"],
                            file_name=mod_data["file_name"],
                            tag=self.tag,
                        )
                        self._plugins.append(plugin)
                    except Exception as e:
                        print(f"ERROR: Failed to load mod {mod_data.get('name', 'unknown')}: {e}")
                        continue

                self.set_category_global_cache("plugins", self._plugins)
                #print(f"DEBUG: Total plugins loaded: {len(self._plugins)}")

            except Exception as e:
                print(f"CRITICAL ERROR in get_plugins: {e}")
                self._plugins = []

        return self._plugins

    def set_category_global_cache(self, key, value):
        if "categories" not in _CACHE:
            _CACHE["categories"] = {}
        if self.meta_url not in _CACHE["categories"]:
            _CACHE["categories"][self.meta_url] = {}
        _CACHE["categories"][self.meta_url][key] = value

    def unset_category_global_cache(self):
        try:
            del _CACHE["categories"][self.meta_url]
        except KeyError:
            pass

    def cleanup(self):
        self._metadata = None
        self._plugins.clear()
        self.unset_category_global_cache()

    async def refresh(self):
        self.cleanup()
        await self.get_plugins()

    def save(self):
        babase.app.config["Mod Manager"]["Custom Sources"].append(self.meta_url)
        babase.app.config.commit()


class CategoryAll(Category):
    def __init__(self, plugins={}):
        super().__init__(meta_url=None)
        self._name = "All"
        self._description = "All plugins"
        self._plugins = plugins


class PluginLocal:
    def __init__(self, name, file_name=None):
        """
        Initialize a plugin locally installed on the device.
        """
        self.name = name
        if file_name is None:
            self.file_name = self._find_actual_filename(name)
        else:
            self.file_name = file_name
        
        # Get the module_name from the file_name (without .py)
        self.module_name = self.file_name.replace('.py', '')
        
        self.install_path = os.path.join(PLUGIN_DIRECTORY, self.file_name)
        self._entry_point_initials = f"{self.module_name}."
        self.cleanup()


    def _find_actual_filename(self, name):
        "Find the actual file in the filesystem"
        
        # First try with the direct name
        direct_path = os.path.join(PLUGIN_DIRECTORY, f"{name}.py")
        if os.path.isfile(direct_path):
            return f"{name}.py"
        
        # Search for files that may match
        for filename in os.listdir(PLUGIN_DIRECTORY):
            if filename.endswith('.py'):
                # Remove spaces and compare
                clean_name = name.replace(' ', '').replace('_', '').lower()
                clean_filename = filename.replace(' ', '').replace('_', '').replace('.py', '').lower()
                if clean_name == clean_filename:
                    return filename
        
        # If not found, use the original name
        return f"{name}.py"
    
    def cleanup(self):
        self._content = None
        self._api_version = None
        self._entry_points = []

    @property
    def is_installed(self):
        return os.path.isfile(self.install_path)

    @property
    def is_installed_via_plugin_manager(self):
        return self.name in babase.app.config["Mod Manager"]["Installed Plugins"]

    def initialize(self):
        if self.name not in babase.app.config["Mod Manager"]["Installed Plugins"]:
            babase.app.config["Mod Manager"]["Installed Plugins"][self.name] = {}
        return self

    async def uninstall(self):
        try:
            os.remove(self.install_path)
        except FileNotFoundError:
            pass
        try:
            del babase.app.config["Mod Manager"]["Installed Plugins"][self.name]
        except KeyError:
            pass
        else:
            self.save()

    @property
    def version(self):
        try:
            version = (babase.app.config["Mod Manager"]
                       ["Installed Plugins"][self.name]["version"])
        except KeyError:
            version = None
        return version

    def _get_content(self):
        with open(self.install_path, "rb") as fin:
            return fin.read()

    def _set_content(self, content):
        with open(self.install_path, "wb") as fout:
            fout.write(content)

    def has_settings(self):
        try:
            for plugin_entry_point, plugin_spec in bui.app.plugins.plugin_specs.items():
                if plugin_entry_point.startswith(self._entry_point_initials):

                    if plugin_spec is None:
                        #print(f"DEBUG: plugin_spec is None for {plugin_entry_point}")
                        continue

                    if plugin_spec.plugin is None:
                        #print(f"DEBUG: plugin_spec.plugin is None for{plugin_entry_point}")
                        continue
                    
                    # Verify that the plugin has the has_settings_ui method
                    if not hasattr(plugin_spec.plugin, 'has_settings_ui'):
                        #print(f"DEBUG: plugin has no method has_settings_ui for{plugin_entry_point}")
                        continue
                    
                    result = plugin_spec.plugin.has_settings_ui()
                    #print(f"DEBUG: has_settings_ui() returned: {result} for {plugin_entry_point}")
                    return result

            #print(f"DEBUG: No plugins found with settings for {self.name}")
            return False

        except Exception as e:
            #print(f"ERROR in has_settings for{self.name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def launch_settings(self, source_widget):
        
        try:
            for plugin_entry_point, plugin_spec in bui.app.plugins.plugin_specs.items():
                if plugin_entry_point.startswith(self._entry_point_initials):

                    if plugin_spec is None:
                        #print(f"DEBUG: plugin_spec is None for {plugin_entry_point}")
                        continue
                        
                    if plugin_spec.plugin is None:
                        #print(f"DEBUG: plugin_spec.plugin is None for {plugin_entry_point}")
                        continue
                    
                    # Verify that the plugin has the show_settings_ui method
                    if not hasattr(plugin_spec.plugin, 'show_settings_ui'):
                        #print(f"DEBUG: plugin has no show_settings_ui method for {plugin_entry_point}")
                        continue
                    
                    return plugin_spec.plugin.show_settings_ui(source_widget)
            
        except Exception as e:
            #print(f"ERROR in launch_settings for {self.name}: {e}")
            import traceback
            traceback.print_exc()

    async def get_content(self):
        if self._content is None:
            if not self.is_installed:
                raise PluginNotInstalled("Plugin is not available locally.")

            self._content = await loop.run_in_executor(None, self._get_content)
        return self._content

    async def detect_entry_points_deep_scan(self):
        """
        Scans the entire file for entry points, not just the beginning
        """
        if not self.is_installed:
            return []

        content = await self.get_content()
        content_str = content.decode('utf-8', errors='ignore')
        entry_points_found = []

        # Find all export patterns in the ENTIRE file
        export_patterns = [
            r'#\s*ba_meta\s+export\s+babase\.Plugin\s*class\s+(\w+)',
            r'#\s*ba_meta\s+export\s+plugin\s*class\s+(\w+)',
            r'#\s*ba_meta\s+export\s+babase\s*class\s+(\w+)',
            r'ba_meta\s+export\s+babase\.Plugin\s*class\s+(\w+)',
            r'ba_meta\s+export\s+plugin\s*class\s+(\w+)'
        ]

        for pattern in export_patterns:
            matches = re.findall(pattern, content_str, re.IGNORECASE | re.MULTILINE)
            if matches:
                for match in matches:
                    entry_point = f"{self.module_name}.{match}"
                    if entry_point not in entry_points_found:
                        entry_points_found.append(entry_point)

        # Also search for alternative format (on multiple lines)
        multi_line_patterns = [
            r'#\s*ba_meta\s+export\s+babase\.Plugin\s*(?:.*\n)*?\s*class\s+(\w+)',
            r'#\s*ba_meta\s+export\s+plugin\s*(?:.*\n)*?\s*class\s+(\w+)'
        ]

        for pattern in multi_line_patterns:
            matches = re.findall(pattern, content_str, re.IGNORECASE)
            if matches:
                for match in matches:
                    entry_point = f"{self.module_name}.{match}"
                    if entry_point not in entry_points_found:
                        entry_points_found.append(entry_point)

        # Find specific lines that contain "ba_meta export"
        lines = content_str.split('\n')
        export_lines = []
        for i, line in enumerate(lines):
            if 'ba_meta export' in line.lower():
                export_lines.append((i, line.strip()))
                #print(f"Line {i}: {line.strip()}")

                # Find the class in the next 10 lines
                for j in range(i+1, min(i+11, len(lines))):
                    if lines[j].strip().startswith('class '):
                        class_line = lines[j].strip()
                        class_match = re.search(r'class\s+(\w+)', class_line)
                        if class_match:
                            class_name = class_match.group(1)
                            entry_point = f"{self.module_name}.{class_name}"
                            if entry_point not in entry_points_found:
                                entry_points_found.append(entry_point)
                                #print(f"  → Class found online{j}: {class_name}")

        return entry_points_found

    async def get_entry_points(self):
        if not self._entry_points:
            # Use deep scanning instead of limited regex
            entry_points_list = await self.detect_entry_points_deep_scan()
            self._entry_points = tuple(entry_points_list)
            
            #print(f"DEBUG: Entry points end for {self.name}: {self._entry_points}")
        return self._entry_points

    async def has_plugins(self):
        entry_points = await self.get_entry_points()
        result = len(entry_points) > 0
        #print(f"DEBUG: PluginLocal.has_plugins for{self.name}: {result} (entry_points: {entry_points})")
        return result
    
    async def is_enabled(self):
        """
        Return True even if a single entry point is enabled or contains minigames.
        """
        if not await self.has_plugins():
            #print(f"DEBUG: PluginLocal.is_enabled for {self.name}: True (no plugins)")
            return True
            
        for entry_point, plugin_info in babase.app.config["Plugins"].items():
            if entry_point.startswith(self._entry_point_initials) and plugin_info["enabled"]:
                #print(f"DEBUG: PluginLocal.is_enabled for {self.name}: True (entry_point {entry_point} enabled)")
                return True
                
        return False

    async def enable(self):
        for entry_point in await self.get_entry_points():
            if entry_point not in babase.app.config["Plugins"]:
                babase.app.config["Plugins"][entry_point] = {}
            babase.app.config["Plugins"][entry_point]["enabled"] = True
            plugin_spec = bui.app.plugins.plugin_specs.get(entry_point)
            if plugin_spec not in bui.app.plugins.active_plugins:
                self.load_plugin(entry_point)
                bui.screenmessage(f"{entry_point} cargado")
        self.save()
        
    def load_plugin(self, entry_point):
        #print(f"DEBUG: Loading plugin: {entry_point}")
        plugin_class = babase._general.getclass(entry_point, babase.Plugin)
        loaded_plugin_instance = plugin_class()
        loaded_plugin_instance.on_app_running()

        plugin_spec = babase.PluginSpec(class_path=entry_point, loadable=True)
        plugin_spec.enabled = True
        plugin_spec.plugin = loaded_plugin_instance
        bui.app.plugins.plugin_specs[entry_point] = plugin_spec
        bui.app.plugins.active_plugins.append(plugin_spec.plugin)

    def disable(self):
        for entry_point, plugin_info in babase.app.config["Plugins"].items():
            if entry_point.startswith(self._entry_point_initials):
                plugin_info["enabled"] = False
        bui.screenmessage(f"{self.module_name} deshabilitado", color=(0.9, 1, 0))
        bui.getsound('shieldDown').play()
        self.save()

    def set_version(self, version):
        app = babase.app
        app.config["Mod Manager"]["Installed Plugins"][self.name]["version"] = version
        return self

    async def set_content(self, content):
        if not self._content:

            await loop.run_in_executor(None, self._set_content, content)
            self._content = content
        return self

    async def set_content_from_network_response(self, request, md5sum=None, retries=3):
        if not self._content:
            self._content = await async_stream_network_response_to_file(
                request,
                self.install_path,
                md5sum=md5sum,
                retries=retries,
            )
        return self._content

    def save(self):
        babase.app.config.commit()
        return self


class PluginVersion:
    def __init__(self, plugin, version, tag=CURRENT_TAG):
        self.number, info = version
        self.plugin = plugin
        self.api_version = info["api_version"]
        self.released_on = info["released_on"]
        self.commit_sha = info["commit_sha"]
        self.md5sum = info["md5sum"]

        # Use the plugin's direct URL (raw_url)
        self.download_url = self.plugin.url
        # Use normal_url for display
        self.view_url = self.plugin.info.get("external_url", self.plugin.url)

    def __eq__(self, plugin_version):
        return (self.number, self.plugin.name) == (plugin_version.number,
                                                   plugin_version.plugin.name)

    def __repr__(self):
        return f"<PluginVersion({self.plugin.name} {self.number})>"

    @property
    def released_on_date(self):
        return datetime.strptime(self.released_on, "%d-%m-%Y")

    async def _download(self, retries=3):
        #print(f"DEBUG: _download started for: {self.plugin.name}")
        #print(f"DEBUG: - file_name: {self.plugin.file_name}")
        #print(f"DEBUG: - install_path: {self.plugin.install_path}")
        #print(f"DEBUG: - download_url: {self.download_url}")
        
        local_plugin = self.plugin.create_local()
        
        #print(f"DEBUG: Local plugin created:")
        #print(f"DEBUG: - name: {local_plugin.name}")
        #print(f"DEBUG: - file_name: {local_plugin.file_name}") 
        #print(f"DEBUG: - install_path: {local_plugin.install_path}")
        
        await local_plugin.set_content_from_network_response(
            self.download_url,
            md5sum=self.md5sum,
            retries=retries,
        )

        local_plugin.set_version(self.number)
        local_plugin.save()
        
        #print(f"DEBUG: _download completed for:{self.plugin.name}")
        return local_plugin

    async def install(self, suppress_screenmessage=False):
        #print(f"DEBUG: install started for: {self.plugin.name}")
        try:
            local_plugin = await self._download()
        except MD5CheckSumFailed:
            print(f"ERROR MD5 checksum failed para: {self.plugin.name}")
            if not suppress_screenmessage:
                bui.screenmessage(
                    f"{self.plugin.name} failed MD5 checksum during installation", color=(1, 0, 0))
            return False
        else:
            #print(f"DEBUG: install successful for: {self.plugin.name}")
            if not suppress_screenmessage:
                bui.screenmessage(f"{self.plugin.name} installed", color=(0, 1, 0))
            check = babase.app.config["Mod Manager"]["Settings"]
            if check["Habilitar mods automáticamente después de la instalación"]:
                await local_plugin.enable()
            else:
                pass
            return True

class Plugin:
    def __init__(self, plugin, url, file_name=None, tag=CURRENT_TAG):
        """
        Initialize a plugin from network repository.
        """
        self.name, self.info = plugin
        self.file_name = file_name or self.name
        self.install_path = os.path.join(PLUGIN_DIRECTORY, self.file_name)
        self.url = url
        self.tag = tag
        self._local_plugin = None

        self._versions = None
        self._latest_version = None
        self._latest_compatible_version = None
        
    def __repr__(self):
        return f"<Plugin({self.name})>"

    def __str__(self):
        return self.name

    @property
    def view_url(self):
        return self.info.get("external_url", self.url)

    @property
    def is_installed(self):
        return os.path.isfile(self.install_path)

    @property
    def versions(self):
        if self._versions is None:
            self._versions = [
                PluginVersion(
                    self,
                    version,
                    tag=self.tag,
                ) for version in self.info["versions"].items()
            ]
        return self._versions

    @property
    def latest_version(self):
        if self._latest_version is None:
            # Usar la versión del JSON
            version_number = list(self.info["versions"].keys())[0]
            self._latest_version = PluginVersion(
                self,
                (version_number, self.info["versions"][version_number]),
                tag=self.tag,
            )
        return self._latest_version

    @property
    def latest_compatible_version(self):
        if self._latest_compatible_version is None:
            # Buscar versión compatible
            for number, info in self.info["versions"].items():
                if info["api_version"] == _app_api_version:
                    self._latest_compatible_version = PluginVersion(
                        self,
                        (number, info),
                        tag=self.tag
                    )
                    break
        if self._latest_compatible_version is None:
            raise NoCompatibleVersion(
                f"{self.name} has no version compatible with API {_app_api_version}."
            )
        return self._latest_compatible_version

    def get_local(self):
        if not self.is_installed:
            raise PluginNotInstalled(
                f"{self.name} needs to be installed to get its local plugin.")
        if self._local_plugin is None:
            self._local_plugin = PluginLocal(self.name, self.file_name)
        return self._local_plugin
    
    def create_local(self):
        return (
            PluginLocal(self.name, self.file_name)
            .initialize()
        )

    async def uninstall(self):
        await self.get_local().uninstall()
        bui.screenmessage(f"{self.name} uninstalled", color=(0.9, 1, 0))

    def has_update(self):
        try:
            latest_compatible_version = self.latest_compatible_version
        except NoCompatibleVersion:
            return False
        else:
            return self.get_local().version != latest_compatible_version.number

    async def update(self):
        if await self.latest_compatible_version.install(suppress_screenmessage=True):
            bui.screenmessage(f"{self.name} updated to {self.latest_compatible_version.number}",
                              color=(0, 1, 0))
            bui.getsound('shieldUp').play()
        else:
            bui.screenmessage(f"{self.name} failed MD5 checksum while updating to "
                              f"{self.latest_compatible_version.number}",
                              color=(1, 0, 0))
            bui.getsound('error').play()


class ModManager:
    def __init__(self):
        self.request_headers = HEADERS
        self._index = _CACHE.get("index", {})
        self._changelog = _CACHE.get("changelog", {})
        self.categories = {}
        self.module_path = sys.modules[__name__].__file__
        self._index_setup_in_progress = False
        self._changelog_setup_in_progress = False

    async def get_index(self):
        if not self._index:
            # For the new format, we create a minimal index
            self._index = {
                "categories": [MODS_DATA_URL],
                "external_source_url": "",  # Empty for now
                "versions": {
                    MOD_MANAGER_VERSION: {
                        "api_version": _app_api_version,
                        "released_on": "01-01-2024",
                        "commit_sha": "unknown", 
                        "md5sum": ""
                    }
                }
            }
            self.set_index_global_cache(self._index)
        return self._index

    async def setup_index(self):
        while self._index_setup_in_progress:
            # Avoid making multiple network calls to the same resource in parallel.
            # Rather wait for the previous network call to complete.
            await asyncio.sleep(0.1)
        self._index_setup_in_progress = not bool(self._index)
        index = await self.get_index()
        await self.setup_plugin_categories(index)
        self._index_setup_in_progress = False

    async def setup_plugin_categories(self, plugin_index):
        try:
            # We only have one category now - "All"
            self.categories["All"] = None
    
            # Create parent category with data.json URL
            category = Category(MODS_DATA_URL)
            await category.fetch_metadata()
            
            all_plugins = await category.get_plugins()
            
            if not all_plugins:
                print("WARNING: Could not load plugins from URL")
                # Create an empty list to avoid errors
                all_plugins = []
                
            self.categories["All"] = CategoryAll(plugins=all_plugins)
            
        except Exception as e:
            print(f"ERROR in setup_plugin_categories: {e}")
            # Make sure there is at least one empty category
            self.categories["All"] = CategoryAll(plugins=[])

    def cleanup(self):
        for category in self.categories.values():
            if category is not None:
                category.cleanup()
        self.categories.clear()
        self._index.clear()
        self._changelog = None
        self.unset_index_global_cache()

    async def refresh(self):
        self.cleanup()
        await self.setup_index()

    def set_index_global_cache(self, index):
        _CACHE["index"] = index

    def set_changelog_global_cache(self, changelog):
        _CACHE["changelog"] = changelog

    def unset_index_global_cache(self):
        try:
            del _CACHE["index"]
            del _CACHE["changelog"]
        except KeyError:
            pass

    async def get_update_details(self):
        index = await self.get_index()
        for version, info in index["versions"].items():
            if info["api_version"] != _app_api_version:
                # No point checking a version of the API game doesn't support.
                continue
            if version == MOD_MANAGER_VERSION:
                # We're already on the latest version for the current API.
                return
            else:
                if next(iter(index["versions"])) == version:
                    # Version on the top is the latest, so no need to specify
                    # the commit SHA explicitly to GitHub to access the latest file.
                    commit_sha = None
                else:
                    commit_sha = info["commit_sha"]
                return version, commit_sha

    async def update(self, to_version=None, commit_sha=None):
        index = await self.get_index()
        if to_version is None:
            to_version, commit_sha = await self.get_update_details()
        to_version_info = index["versions"][to_version]
        tag = commit_sha or CURRENT_TAG
        download_url = index["plugin_manager_url"].format(
            content_type="raw",
            tag=tag,
        )
        response = await async_send_network_request(download_url)
        content = response.read()
        if hashlib.md5(content).hexdigest() != to_version_info["md5sum"]:
            raise MD5CheckSumFailed("MD5 checksum failed during plugin manager update.")
        with open(self.module_path, "wb") as fout:
            fout.write(content)
        return to_version_info

    async def soft_refresh(self):
        pass

class ModWindow(popup.PopupWindow):
    def __init__(
        self,
        plugin: Plugin,
        origin_widget,
        plugins_list,
        transition='in_scale',
        button_callback=lambda: None,
    ):
        self.plugin: Plugin = plugin
        self.transition = transition
        self.plugins_list = plugins_list
        self.button_callback = button_callback
        self.scale_origin = origin_widget.get_screen_space_center()

        loop.create_task(self.draw_ui())

    def get_description(self, minimum_character_offset=40):
        """
        Splits the long plugin description into multiple lines.
        """
        string = self.plugin.info["description"]
        string_length = len(string)

        partitioned_string = ""
        partitioned_string_length = len(partitioned_string)

        while partitioned_string_length != string_length:
            next_empty_space = string[partitioned_string_length +
                                      minimum_character_offset:].find(" ")
            next_word_end_position = partitioned_string_length + \
                minimum_character_offset + max(0, next_empty_space)
            partitioned_string += string[partitioned_string_length:next_word_end_position]
            if next_empty_space != -1:
                # Insert a line break here, there's still more partitioning to do.
                partitioned_string += "\n"
            partitioned_string_length = len(partitioned_string)

        return partitioned_string

    async def draw_ui(self):
        bui.getsound('swish').play()
        b_text_color = (0.75, 0.7, 0.8)
        s = 1.25 if _uiscale() is babase.UIScale.SMALL else 1.39 if babase.UIScale.MEDIUM else 1.67
        width = 450 * s
        height = 120 + 100 * s
        color = (1, 1, 1)
        text_scale = 0.7 * s

        self._root_widget = bui.containerwidget(
            size=(width, height),
            on_outside_click_call=self._cancel,
            transition=self.transition,
            scale=(2.1 if _uiscale() is babase.UIScale.SMALL else 1.5
                   if _uiscale() is babase.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin
        )

        _add_popup(self)

        i = self.plugins_list.index(self.plugin)
        self.p_n_plugins = [
            self.plugins_list[i-1] if (i-1 > -1) else None,
            self.plugins_list[i+1] if (i+1 < len(self.plugins_list)) else None
        ]

        if self.p_n_plugins is not None:
            if self.p_n_plugins[0] is not None:
                previous_plugin_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(-12.5*s + (4 if _uiscale() is babase.UIScale.SMALL else -5),
                              height/2 - 20*s),
                    label='<',
                    size=(25, 40),
                    color=(1, 0.5, 0.5),
                    scale=s,
                    on_activate_call=self.show_previous_plugin
                )

            if self.p_n_plugins[1] is not None:
                next_plugin_button = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(width - 12.5*s - (8 if _uiscale()
                              is babase.UIScale.SMALL else 0), height/2 - 20*s),
                    label='>',
                    size=(25, 40),
                    color=(1, 0.5, 0.5),
                    scale=s,
                    on_activate_call=self.show_next_plugin
                )

        pos = height * 0.8
        plug_name = self.plugin.name.replace('_', ' ').title()
        plugin_title = f"{plug_name} ({self.plugin.latest_compatible_version.number})"
        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=plugin_title,
            scale=text_scale * 1.25,
            color=color,
            maxwidth=width * 0.9
        )

        pos -= 25
        pos -= 60

        # Info
        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=self.get_description(),
            scale=text_scale * 0.6,
            color=color,
            maxwidth=width * 0.95
        )
        b1_color = None
        b2_color = (0.8, 0.15, 0.35)
        b3_color = (0.2, 0.8, 0.3)
        pos = height * 0.1
        button_size = (80 * s, 40 * s)

        to_draw_button1 = True
        to_draw_button4 = False
        has_update = False
        
        #print(f"DEBUG: ModWindow: Processing mod{self.plugin.name}")
        #print(f"  - Installing: {self.plugin.is_installed}")
        
        if self.plugin.is_installed:
            self.local_plugin = self.plugin.get_local()
            #print(f"  - It has plugins: {await self.local_plugin.has_plugins()}")
            #print(f"  - It is enabled: {await self.local_plugin.is_enabled()}")
            
            if not await self.local_plugin.has_plugins():
                to_draw_button1 = False
                #print(f"  - Don't draw button 1: has no plugins")
            else:
                if await self.local_plugin.is_enabled():
                    button1_label = "Disable"
                    b1_color = (0.6, 0.53, 0.63)
                    button1_action = self.disable
                    #print(f"  - Button 1: Disable")
                    if self.local_plugin.has_settings():
                        to_draw_button4 = True
                        #print(f"  - Has settings: Yes")
                else:
                    button1_label = "Enable"
                    button1_action = self.enable
                    #print(f"  - Button 1: Enable")
            
            button2_label = "Uninstall"
            button2_action = self.uninstall
            has_update = self.plugin.has_update()
            #print(f"  - Has update: {has_update}")
            
            if has_update:
                button3_label = "Update"
                button3_action = self.update
                #print(f"  - Button 3: Update")
        else:
            button1_label = "Install"
            button1_action = self.install
            #print(f"  - Button 1: Install")

        if to_draw_button1:
            selected_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(
                    width * (0.1 if self.plugin.is_installed and has_update else
                             0.25 if self.plugin.is_installed else 0.4), pos
                ),
                size=button_size,
                on_activate_call=button1_action,
                color=b1_color,
                textcolor=b_text_color,
                button_type='square',
                text_scale=1,
                label=button1_label
            )

        if self.plugin.is_installed:
            selected_btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(
                    width * (0.4 if has_update or not to_draw_button1 else 0.55), pos),
                size=button_size,
                on_activate_call=button2_action,
                color=b2_color,
                textcolor=b_text_color,
                button_type='square',
                text_scale=1,
                label=button2_label
            )

            if has_update:
                selected_btn = bui.buttonwidget(
                    parent=self._root_widget,
                    position=(width * 0.7, pos),
                    size=button_size,
                    on_activate_call=button3_action,
                    color=b3_color,
                    textcolor=b_text_color,
                    autoselect=True,
                    button_type='square',
                    text_scale=1,
                    label=button3_label
                )

        bui.containerwidget(
            edit=self._root_widget,
            on_cancel_call=self._cancel,
            selected_child=selected_btn
        )

        open_pos_x = (415 if _uiscale() is babase.UIScale.SMALL else
                      475 if _uiscale() is babase.UIScale.MEDIUM else 465)
        open_pos_y = (100 if _uiscale() is babase.UIScale.SMALL else
                      110 if _uiscale() is babase.UIScale.MEDIUM else 120)
        open_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(open_pos_x, open_pos_y),
            size=(30, 40),
            button_type="square",
            label="",
            color=(0.6, 0.53, 0.63),
            on_activate_call=lambda: bui.open_url(self.plugin.view_url)
        )
        bui.imagewidget(
            parent=self._root_widget,
            position=(open_pos_x, open_pos_y),
            size=(30, 40),
            color=(0.8, 0.95, 1),
            texture=bui.gettexture("file"),
            draw_controller=open_button
        )
        bui.textwidget(
            parent=self._root_widget,
            position=(open_pos_x-3, open_pos_y+12),
            text="Source",
            size=(10, 10),
            draw_controller=open_button,
            color=(1, 1, 1, 1),
            rotate=25,
            scale=0.45
        )

        # Below snippet handles the tutorial button in the plugin window
        tutorial_url = self.plugin.info.get("readme_url")
        if tutorial_url:
            
            def tutorial_confirm_window():
                bui.open_url(tutorial_url)
                #text = "This will take you to the mod's documentation\n\"" + tutorial_url + "\""
                #tutorial_confirm_window = confirm.ConfirmWindow(
                #    text=text,
                #    action=lambda: bui.open_url(tutorial_url),
                #)
            open_pos_x = (440 if _uiscale() is babase.UIScale.SMALL else
                          500 if _uiscale() is babase.UIScale.MEDIUM else 490)
            open_pos_y = (100 if _uiscale() is babase.UIScale.SMALL else
                          110 if _uiscale() is babase.UIScale.MEDIUM else 120)
            open_button = bui.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                position=(open_pos_x + 20, open_pos_y),
                size=(30, 40),
                button_type="square",
                label="",
                color=(0.6, 0.53, 0.63),
                on_activate_call=tutorial_confirm_window
            )

            bui.imagewidget(
                parent=self._root_widget,
                position=(open_pos_x + 20, open_pos_y),
                size=(30, 40),
                color=(0.8, 0.95, 1),
                texture=bui.gettexture("frameInset"),
                draw_controller=open_button
            )
            bui.textwidget(
                parent=self._root_widget,
                position=(open_pos_x + 13, open_pos_y + 12),
                text="Readme",
                size=(10, 10),
                draw_controller=open_button,
                color=(1, 1, 1, 1),
                rotate=25,
                scale=0.45
            )

        if to_draw_button4:
            settings_pos_x = (60 if _uiscale() is babase.UIScale.SMALL else
                              60 if _uiscale() is babase.UIScale.MEDIUM else 60)
            settings_pos_y = (100 if _uiscale() is babase.UIScale.SMALL else
                              110 if _uiscale() is babase.UIScale.MEDIUM else 120)
            settings_button = bui.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                position=(settings_pos_x, settings_pos_y),
                size=(30, 40),
                button_type="square",
                label="",
                color=(0, 0.75, 0.75),
            )
            bui.buttonwidget(
                edit=settings_button,
                on_activate_call=babase.Call(self.settings, settings_button)
            )
            bui.imagewidget(
                parent=self._root_widget,
                position=(settings_pos_x, settings_pos_y),
                size=(30, 40),
                color=(0.8, 0.95, 1),
                texture=bui.gettexture("settingsIcon"),
                draw_controller=settings_button
            )

    def _ok(self) -> None:
        _remove_popup(self)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')

    def _cancel(self) -> None:
        bui.getsound('swish').play()
        _remove_popup(self)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')

    def button(fn):
        async def asyncio_handler(fn, self, *args, **kwargs):
            await fn(self, *args, **kwargs)
            await self.button_callback()

        def wrapper(self, *args, **kwargs):
            self._ok()

            if asyncio.iscoroutinefunction(fn):
                loop.create_task(asyncio_handler(fn, self, *args, **kwargs))
            else:
                fn(self, *args, **kwargs)
                loop.create_task(self.button_callback())

        return wrapper

    def settings(self, source_widget):
        self.local_plugin.launch_settings(source_widget)

    def show_previous_plugin(self):
        bui.containerwidget(edit=self._root_widget, transition='out_right')
        _remove_popup(self)
        ModWindow(
            self.p_n_plugins[0],
            self._root_widget,
            transition='in_left',
            plugins_list=self.plugins_list,
            button_callback=lambda: None
        )

    def show_next_plugin(self):
        bui.containerwidget(edit=self._root_widget, transition='out_left')
        _remove_popup(self)
        ModWindow(
            self.p_n_plugins[1],
            self._root_widget,
            transition='in_right',
            plugins_list=self.plugins_list,
            button_callback=lambda: None
        )

    @button
    def disable(self) -> None:
        self.local_plugin.disable()

    @button
    async def enable(self) -> None:
        await self.local_plugin.enable()
        bui.getsound('gunCocking').play()

    @button
    async def install(self):
        await self.plugin.latest_compatible_version.install()
        bui.getsound('cashRegister2').play()

    @button
    async def uninstall(self):
        await self.plugin.uninstall()
        bui.getsound('shieldDown').play()

    @button
    async def update(self):
        await self.plugin.update()
        bui.getsound('shieldUp').play()


class PluginCustomSourcesWindow(popup.PopupWindow):
    def __init__(self, origin_widget):
        self.selected_source = None

        self.scale_origin = origin_widget.get_screen_space_center()

        b_textcolor = (0.75, 0.7, 0.8)
        self._transition_out = 'out_scale'
        transition = 'in_scale'
        self._root_widget = bui.containerwidget(
            size=(400, 340),
            on_outside_click_call=self._ok,
            transition=transition,
            scale=(2.1 if _uiscale() is babase.UIScale.SMALL else 1.5
                   if _uiscale() is babase.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin,
            on_cancel_call=self._ok
        )

        _add_popup(self)

        bui.textwidget(
            parent=self._root_widget,
            position=(155, 300),
            size=(100, 25),
            text="Custom Plugin Sources",
            color=bui.app.ui_v1.title_color,
            scale=0.8,
            h_align="center",
            v_align="center",
            maxwidth=270,
        )

        scroll_size_x = (290 if _uiscale() is babase.UIScale.SMALL else
                         300 if _uiscale() is babase.UIScale.MEDIUM else 290)
        scroll_size_y = (170 if _uiscale() is babase.UIScale.SMALL else
                         185 if _uiscale() is babase.UIScale.MEDIUM else 180)
        scroll_pos_x = (55 if _uiscale() is babase.UIScale.SMALL else
                        40 if _uiscale() is babase.UIScale.MEDIUM else 60)
        scroll_pos_y = 105

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(scroll_size_x, scroll_size_y),
            position=(scroll_pos_x, scroll_pos_y)
        )
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=1, margin=0
        )

        delete_source_button_position_pos_x = 360
        delete_source_button_position_pos_y = 110
        delete_source_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(
                delete_source_button_position_pos_x, delete_source_button_position_pos_y
            ),
            size=(25, 25),
            label="",
            on_activate_call=self.delete_selected_source,
            button_type="square",
            color=(0.6, 0, 0)
        )

        bui.imagewidget(
            parent=self._root_widget,
            position=(
                delete_source_button_position_pos_x + 2, delete_source_button_position_pos_y
            ),
            size=(25, 25),
            color=(5, 2, 2),
            texture=bui.gettexture("crossOut"),
            draw_controller=delete_source_button
        )

        warning_pos_x = (43 if _uiscale() is babase.UIScale.SMALL else
                         35 if _uiscale() is babase.UIScale.MEDIUM else
                         48)
        bui.textwidget(
            parent=self._root_widget,
            position=(warning_pos_x, 74),
            size=(50, 22),
            text=("Warning: 3rd party plugin sources are not moderated\n"
                  "               by the community and may be dangerous!"),
            color=(1, 0.23, 0.23),
            scale=0.5,
            h_align="left",
            v_align="center",
            maxwidth=400,
        )

        self._add_source_widget = bui.textwidget(
            parent=self._root_widget,
            size=(335, 50),
            position=(21, 22),
            h_align='left',
            v_align='center',
            editable=True,
            scale=0.75,
            maxwidth=215,
            description="Add Source"
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(330, 28),
            size=(37, 37),
            on_activate_call=lambda: loop.create_task(self.add_source()),
            label="",
            texture=bui.gettexture("startButton"),
            button_type="square",
            color=(0, 0.9, 0),
            textcolor=b_textcolor,
            text_scale=1
        )

        self.draw_sources()

    def draw_sources(self):
        for plugin in self._columnwidget.get_children():
            plugin.delete()

        color = (1, 1, 1)
        for custom_source in babase.app.config["Mod Manager"]["Custom Sources"]:
            bui.textwidget(
                parent=self._columnwidget,
                selectable=True,
                color=color,
                text=custom_source,
                on_select_call=lambda: self.select_source(custom_source),
                h_align='left',
                v_align='center',
                scale=0.75,
                maxwidth=260
            )

    def select_source(self, source):
        self.selected_source = source

    async def add_source(self):
        source = bui.textwidget(query=self._add_source_widget)
        # External source URIs can optionally suffix `@branchname`, for example:
        # `bombsquad-community/sample-plugin-source@experimental`
        source_splits = source.split("@", maxsplit=1)
        if len(source_splits) == 1:
            # Fallack to `main` if `@branchname` isn't specified in an external source URI.
            source_repo, source_tag = source_splits[0], "main"
        else:
            source_repo, source_tag = source_splits
        meta_url = partial_format(
            _CACHE["index"]["external_source_url"],
            repository=source_repo,
        )
        category = Category(meta_url, tag=source_tag)
        try:
            await category.validate()
        except (PluginSourceNetworkError, CategoryMetadataParseError) as e:
            bui.screenmessage(str(e), color=(1, 0, 0))
            bui.getsound('error').play()
            return
        if source in babase.app.config["Mod Manager"]["Custom Sources"]:
            bui.screenmessage("Plugin source already exists")
            bui.getsound('error').play()
            return
        babase.app.config["Mod Manager"]["Custom Sources"].append(source)
        babase.app.config.commit()
        bui.screenmessage("Plugin source added; Refresh plugin list to see changes",
                          color=(0, 1, 0))
        bui.getsound('cashRegister2').play()
        self.draw_sources()

    def delete_selected_source(self):
        if self.selected_source is None:
            return
        babase.app.config["Mod Manager"]["Custom Sources"].remove(self.selected_source)
        babase.app.config.commit()
        bui.screenmessage("Plugin source deleted; Refresh plugin list to see changes",
                          color=(0.9, 1, 0))
        bui.getsound('shieldDown').play()
        self.draw_sources()

    def _ok(self) -> None:
        bui.getsound('swish').play()
        _remove_popup(self)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')


class PluginCategoryWindow(popup.PopupMenuWindow):
    def __init__(self, choices, current_choice, origin_widget, asyncio_callback):
        choices = (*choices, "Installed")
        self._asyncio_callback = asyncio_callback
        self.scale_origin = origin_widget.get_screen_space_center()
        super().__init__(
            position=self.scale_origin,
            scale=(2.3 if _uiscale() is babase.UIScale.SMALL else
                   1.65 if _uiscale() is babase.UIScale.MEDIUM else 1.23),
            choices=choices,
            current_choice=current_choice,
            delegate=self
        )
        self._root_widget = self.root_widget
        bui.containerwidget(edit=self.root_widget, color=MAIN_COLOR)
        _add_popup(self)
        #self._update_custom_sources_widget()

    def _update_custom_sources_widget(self):
        bui.textwidget(
            edit=self._columnwidget.get_children()[-1],
            color=(0.5, 0.5, 0.5),
            on_activate_call=self.show_sources_window
        )

    def popup_menu_selected_choice(self, window, choice):

        loop.create_task(self._asyncio_callback(choice))

    def popup_menu_closing(self, window):
        pass

    def show_sources_window(self):
        self._ok()
        PluginCustomSourcesWindow(origin_widget=self.root_widget)

    def _ok(self) -> None:
        bui.getsound('swish').play()
        _remove_popup(self)
        bui.containerwidget(edit=self.root_widget, transition='out_scale')


class ModManagerWindow(bui.MainWindow):
    def __init__(
        self,
        transition: str = "in_right",
        origin_widget: bui.Widget = None
    ):
        self.plugin_manager = ModManager()
        self.category_selection_button = None
        self.selected_category = 'All'
        self.plugins_in_current_view = {}
        self.selected_alphabet_order = 'a_z'
        self.alphabet_order_selection_button = None
        global open_popups
        open_popups = []

        loop.create_task(self.draw_index())

        self._width = (700 if _uiscale() is babase.UIScale.SMALL
                       else 550 if _uiscale() is babase.UIScale.MEDIUM
                       else 570)
        self._height = (500 if _uiscale() is babase.UIScale.SMALL
                        else 422 if _uiscale() is babase.UIScale.MEDIUM
                        else 500)
        top_extra = 20 if _uiscale() is babase.UIScale.SMALL else 0

        if origin_widget:
            self._transition_out = "out_scale"
            self._scale_origin = origin_widget.get_screen_space_center()
            transition = "in_scale"

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height + top_extra),
                toolbar_visibility="menu_minimal",
                scale=(1.9 if _uiscale() is babase.UIScale.SMALL
                       else 1.5 if _uiscale() is babase.UIScale.MEDIUM
                       else 1.0),
                stack_offset=(0, -25) if _uiscale() is babase.UIScale.SMALL else (0, 0)
            ),
            transition=transition,
            origin_widget=origin_widget,
        )

        back_pos_x = 5 + (37 if _uiscale() is babase.UIScale.SMALL else
                          27 if _uiscale() is babase.UIScale.MEDIUM else 68)
        back_pos_y = self._height - (95 if _uiscale() is babase.UIScale.SMALL else
                                     65 if _uiscale() is babase.UIScale.MEDIUM else 50)

        if _uiscale() is bui.UIScale.SMALL:
            self._back_button = None
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self.main_window_back
            )
        else:
            self._back_button = back_button = bui.buttonwidget(
                parent=self._root_widget,
                position=(back_pos_x, back_pos_y),
                size=(60, 60),
                scale=0.8,
                label=babase.charstr(babase.SpecialChar.BACK),
                button_type='backSmall',
                on_activate_call=self.main_window_back
            )

            bui.containerwidget(edit=self._root_widget, cancel_button=back_button)

        title_pos = self._height - (83 if _uiscale() is babase.UIScale.SMALL else
                                    50 if _uiscale() is babase.UIScale.MEDIUM else 50)

        # Title text
        self._title = bui.textwidget(
            parent=self._root_widget,
            position=(-10, title_pos),
            size=(self._width, 25),
            text="Mod Manager",
            color=bui.app.ui_v1.title_color,
            scale=1.05,
            h_align="center",
            v_align="center",
            maxwidth=270,
        )

        # Divider line under the title
        self._divider = bui.imagewidget(
            parent=self._root_widget,
            size=(270, 2),
            position=((self._width - 270) / 2, title_pos - 8),
            texture=bui.gettexture("white"),
            color=(1, 0, 0),
        )

        # Rainbow color sequence
        self._rainbow_colors = [
            (1, 0, 0),
            (1, 0.5, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 1, 1),
            (0, 0, 1),
            (1, 0, 1),
        ]

        # Track the current color index
        self._divider_color_index = 0

        # Function to rotate both divider and title colors
        def _update_colors():
            if not self._divider.exists() or not self._title.exists():
                return

            # Get next rainbow color
            self._divider_color_index = (
                self._divider_color_index + 1
            ) % len(self._rainbow_colors)
            new_color = self._rainbow_colors[self._divider_color_index]

            # Apply color to divider
            bui.imagewidget(edit=self._divider, color=new_color)

            # Dimmed version for title (50% opacity)
            title_color = tuple(c * 0.5 for c in new_color)
            bui.textwidget(edit=self._title, color=title_color)

            # Schedule next update
            bui.apptimer(1.0, _update_colors)

        # Start color rotation
        bui.apptimer(1.0, _update_colors)

        loading_pos_y = self._height - (275 if _uiscale() is babase.UIScale.SMALL else
                                        235 if _uiscale() is babase.UIScale.MEDIUM else 270)

        self._plugin_manager_status_text = bui.textwidget(
            parent=self._root_widget,
            position=(-5, loading_pos_y),
            size=(self._width, 25),
            text="",
            color=bui.app.ui_v1.title_color,
            scale=0.7,
            h_align="center",
            v_align="center",
            maxwidth=400,
        )
        self._loading_spinner = bui.spinnerwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, loading_pos_y),
            style='bomb',
            size=48,
        )

    @override
    def get_main_window_state(self) -> bui.MainWindowState:
        # Support recreating our window for back/refresh purposes.
        global open_popups
        # Close all open popups if ui changes.
        # check pr #390 for more info.
        for popup in open_popups:
            try:
                bui.containerwidget(edit=popup._root_widget, transition='out_scale')
            except:
                pass
        cls = type(self)
        return bui.BasicMainWindowState(
            create_call=lambda transition, origin_widget: cls(
                transition=transition, origin_widget=origin_widget
            )
        )

    def spin(self, show=False):
        w = self._loading_spinner
        p = self._root_widget
        bui.spinnerwidget(w, visible=show) if w.exists(
        ) and p.exists() and not p.transitioning_out else None

    @contextlib.contextmanager
    def exception_handler(self):
        try:
            yield
        except urllib.error.URLError:
            self.spin()
            try:
                bui.textwidget(
                    edit=self._plugin_manager_status_text,
                    text="Make sure you are connected\n to the Internet and try again."
                )
            except:
                pass
            self.plugin_manager._index_setup_in_progress = False
        except RuntimeError:
            # User probably went back before a bui.Window could finish loading.
            pass
        except Exception as e:
            self.spin()
            try:
                bui.textwidget(edit=self._plugin_manager_status_text, text=str(e))
            except:
                pass
            raise

    async def draw_index(self):
        self.draw_search_bar()
        self.draw_plugins_scroll_bar()
        self.draw_category_selection_button(post_label="All")
        self.draw_refresh_icon()
        self.draw_settings_icon()
        with self.exception_handler():
            await self.plugin_manager.setup_index()
            self.spin()
            try:
                bui.textwidget(edit=self._plugin_manager_status_text, text="")
            except:
                pass
            await self.select_category("All")

    def draw_plugins_scroll_bar(self):
        scroll_size_x = (515 if _uiscale() is babase.UIScale.SMALL else
                         430 if _uiscale() is babase.UIScale.MEDIUM else 420)
        scroll_size_y = (245 if _uiscale() is babase.UIScale.SMALL else
                         265 if _uiscale() is babase.UIScale.MEDIUM else 335)
        scroll_pos_x = (70 if _uiscale() is babase.UIScale.SMALL else
                        50 if _uiscale() is babase.UIScale.MEDIUM else 70)
        scroll_pos_y = (100 if _uiscale() is babase.UIScale.SMALL else
                        35 if _uiscale() is babase.UIScale.MEDIUM else 40)
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            size=(scroll_size_x, scroll_size_y),
            position=(scroll_pos_x, scroll_pos_y)
        )
        self._columnwidget = bui.columnwidget(
            parent=self._scrollwidget,
            border=2,
            margin=0
        )

    def draw_category_selection_button(self, post_label):
        category_pos_x = (440 if _uiscale() is babase.UIScale.SMALL else
                          340 if _uiscale() is babase.UIScale.MEDIUM else 370)
        category_pos_y = self._height - (141 if _uiscale() is babase.UIScale.SMALL else
                                         110 if _uiscale() is babase.UIScale.MEDIUM else 110)
        b_size = (140, 30)
        b_textcolor = (0.8, 0.8, 0.85)

        if self.alphabet_order_selection_button is None:
            self.alphabet_order_selection_button = bui.buttonwidget(
                parent=self._root_widget,
                size=(30, 30),
                position=(category_pos_x - 47, category_pos_y),
                label='Z - A' if self.selected_alphabet_order == 'z_a' else 'A - Z',
                on_activate_call=lambda: loop.create_task(self._on_order_button_press()),
                button_type="square",
                textcolor=b_textcolor,
                text_scale=0.6,
                color=MAIN_COLOR
            )
        else:
            b = self.alphabet_order_selection_button
            bui.buttonwidget(
                edit=b,
                label=('Z - A' if self.selected_alphabet_order == 'z_a' else 'A - Z')
            ) if b.exists() else None

        label = f"Category: {post_label}"

        if self.category_selection_button is None:
            self.category_selection_button = b = bui.buttonwidget(
                parent=self._root_widget,
                position=(category_pos_x, category_pos_y),
                size=b_size,
                label=label,
                button_type="square",
                textcolor=b_textcolor,
                text_scale=0.6,
                color=MAIN_COLOR
            )
            bui.buttonwidget(
                edit=b, on_activate_call=lambda: self.show_categories_window(source=b)),
        else:
            b = self.category_selection_button
            bui.buttonwidget(
                edit=b,
                label=label
            ) if b.exists() else None

    async def _on_order_button_press(self) -> None:
        self.selected_alphabet_order = ('a_z' if self.selected_alphabet_order == 'z_a' else 'z_a')
        bui.buttonwidget(edit=self.alphabet_order_selection_button,
                         label=('Z - A' if self.selected_alphabet_order == 'z_a' else 'A - Z')
                         )
        filter_text = bui.textwidget(parent=self._root_widget, query=self._filter_widget)
        if self.plugin_manager.categories != {}:
            if self.plugin_manager.categories['All'] is not None:
                await self.draw_plugin_names(
                    self.selected_category, search_term=filter_text, refresh=True, order=self.selected_alphabet_order
                )

    def draw_search_bar(self):
        search_bar_pos_x = (85 if _uiscale() is babase.UIScale.SMALL else
                            68 if _uiscale() is babase.UIScale.MEDIUM else 75)
        search_bar_pos_y = self._height - (
            145 if _uiscale() is babase.UIScale.SMALL else
            110 if _uiscale() is babase.UIScale.MEDIUM else 116)

        search_bar_size_x = (320 if _uiscale() is babase.UIScale.SMALL else
                             230 if _uiscale() is babase.UIScale.MEDIUM else 260)
        search_bar_size_y = (
            35 if _uiscale() is babase.UIScale.SMALL else
            35 if _uiscale() is babase.UIScale.MEDIUM else 45)

        filter_txt_pos_x = (60 if _uiscale() is babase.UIScale.SMALL else
                            40 if _uiscale() is babase.UIScale.MEDIUM else 50)
        filter_txt_pos_y = search_bar_pos_y + (3 if _uiscale() is babase.UIScale.SMALL else
                                               4 if _uiscale() is babase.UIScale.MEDIUM else 8)

        bui.textwidget(parent=self._root_widget,
                       text="Filter",
                       position=(filter_txt_pos_x, filter_txt_pos_y),
                       selectable=False,
                       h_align='left',
                       v_align='center',
                       color=bui.app.ui_v1.title_color,
                       scale=0.5)

        filter_txt = babase.Lstr(resource='filterText')
        search_bar_maxwidth = search_bar_size_x - (95 if _uiscale() is babase.UIScale.SMALL else
                                                   77 if _uiscale() is babase.UIScale.MEDIUM else
                                                   85)
        self._filter_widget = bui.textwidget(
            parent=self._root_widget,
            text="",
            size=(search_bar_size_x, search_bar_size_y),
            position=(search_bar_pos_x, search_bar_pos_y),
            h_align='left',
            v_align='center',
            editable=True,
            scale=0.8,
            autoselect=True,
            maxwidth=search_bar_maxwidth,
            description=filter_txt
        )
        self._last_filter_text = ""
        self._last_filter_plugins = []

        loop.create_task(self.process_search_term())

    async def process_search_term(self):
        while True:
            await asyncio.sleep(0.2)
            if not self._filter_widget:
                # Search filter widget got destroyed. No point checking for filter text anymore.
                return
            filter_text = bui.textwidget(parent=self._root_widget, query=self._filter_widget)
            if self.selected_category is None:
                continue
            try:
                await self.draw_plugin_names(
                    self.selected_category, search_term=filter_text.lower(), order=self.selected_alphabet_order)
            except CategoryDoesNotExist:
                pass

    def draw_settings_icon(self):
        settings_pos_x = (610 if _uiscale() is babase.UIScale.SMALL else
                          500 if _uiscale() is babase.UIScale.MEDIUM else 510)
        settings_pos_y = (130 if _uiscale() is babase.UIScale.SMALL else
                          60 if _uiscale() is babase.UIScale.MEDIUM else 70)
        controller_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(settings_pos_x, settings_pos_y),
            size=(30, 30),
            button_type="square",
            label=""
        )
        bui.buttonwidget(
            controller_button,
            on_activate_call=babase.Call(
                ModManagerSettingsWindow,
                self.plugin_manager,
                controller_button,
            ),
            color=MAIN_COLOR
        )
        bui.imagewidget(
            parent=self._root_widget,
            position=(settings_pos_x, settings_pos_y),
            size=(30, 30),
            color=(0.8, 0.95, 1),
            texture=bui.gettexture("settingsIcon"),
            draw_controller=controller_button
        )

    def draw_refresh_icon(self):
        refresh_pos_x = (610 if _uiscale() is babase.UIScale.SMALL else
                         500 if _uiscale() is babase.UIScale.MEDIUM else 510)
        refresh_pos_y = (180 if _uiscale() is babase.UIScale.SMALL else
                         108 if _uiscale() is babase.UIScale.MEDIUM else 120)

        controller_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(refresh_pos_x, refresh_pos_y),
            size=(30, 30),
            button_type="square",
            label="",
            on_activate_call=lambda: loop.create_task(self.refresh()),
            color=MAIN_COLOR
        )
        bui.imagewidget(
            parent=self._root_widget,
            position=(refresh_pos_x, refresh_pos_y),
            size=(30, 30),
            color=(0.8, 0.95, 1),
            texture=bui.gettexture("replayIcon"),
            draw_controller=controller_button
        )

    def search_term_filterer(self, plugin, search_term):
        """
        Filter plugins based on the search term.
        Now search by name and description.
        """
        search_term = search_term.lower().strip()

        # Search in mod name (case insensitive)
        plugin_name_lower = plugin.name.lower()
        if search_term in plugin_name_lower:
            return True

        # Search in the mod description (case insensitive)
        plugin_description_lower = plugin.info["description"].lower()
        if search_term in plugin_description_lower:
            return True

        # Search for partial words in the name
        name_words = plugin_name_lower.replace('_', ' ').replace('-', ' ')
        if search_term in name_words:
            return True

        # Fuzzy search - if the term is a substring of the name
        # E.g., "ptfltr" might find "PartyFilter"
        if len(search_term) > 2:
            name_chars = plugin_name_lower.replace('_', '').replace('-', '').replace(' ', '')
            search_chars = search_term.replace(' ', '')

            # Check if the search characters appear in order in the name
            pos = 0
            for char in search_chars:
                pos = name_chars.find(char, pos)
                if pos == -1:
                    break
                pos += 1
            else:
                # All characters found in order
                return True

        return False


    async def draw_plugin_names(self, category, search_term="", refresh=False, order='a_z'):
        # Re-draw plugin list UI if either search term or category was switched.
        to_draw_plugin_names = (search_term, category) != (self._last_filter_text,
                                                           self.selected_category)
        if not (to_draw_plugin_names or refresh):
            return
    
        try:
            if self.plugin_manager.categories != {}:
                if self.plugin_manager.categories['All'] is not None:
                    category_plugins = await self.plugin_manager.categories[category if category != 'Installed' else 'All'].get_plugins()
                else:
                    return
            else:
                return
        except (KeyError, AttributeError):
            no_internet_text = "Make sure you are connected\n to the Internet and try again."
            if bui.textwidget(query=self._plugin_manager_status_text) != no_internet_text:
                raise CategoryDoesNotExist(f"{category} does not exist.")
            else:
                return
    
        if search_term:
            original_count = len(category_plugins)
            plugins = list(filter(
                lambda plugin: self.search_term_filterer(plugin, search_term),
                category_plugins,
            ))
            filtered_count = len(plugins)
    
            for plugin in plugins:
                #print(f"DEBUG: Found: {plugin.name}")
                pass
        else:
            plugins = category_plugins
    
        def return_name(val):
            return val.name
        plugins.sort(key=return_name, reverse=(True if order == 'z_a' else False))
    
        if plugins == self._last_filter_plugins and not refresh:
            # Plugins names to draw on UI are already drawn.
            return
    
        self._last_filter_text = search_term
        self._last_filter_plugins = plugins
    
        if not self._columnwidget.exists():
            return
    
        if category == 'Installed':
            plugin_names_to_draw = tuple(
                plugin for plugin in plugins if plugin.is_installed
            )
        else:
            plugin_names_to_draw = plugins
    
        # Clear previous widgets
        [plugin.delete() for plugin in self._columnwidget.get_children()]
    
        # Process compatible plugins
        plugin_names_ready_to_draw = []
        for plugin in plugin_names_to_draw:
            try:
                lcv = plugin.latest_compatible_version
                plugin_names_ready_to_draw.append(plugin)
            except NoCompatibleVersion:
                continue

        # Counters by category
        counters = {
            "green_updated": 0,
            "blue_update": 0, 
            "orange_disabled": 0,
            "red_manual": 0,
            "gray_not_installed": 0
        }
    
        # Lists for each category
        mods_green = []
        mods_blue = []
        mods_orange = []
        mods_red = []
        mods_gray = []
    
        for plugin in plugin_names_ready_to_draw:
            if plugin.is_installed:
                local_plugin = plugin.get_local()
                is_enabled = await local_plugin.is_enabled()
                has_update = plugin.has_update()
                
                if is_enabled:
                    if not local_plugin.is_installed_via_plugin_manager:
                        counters["red_manual"] += 1
                        mods_red.append(plugin.name)
                    elif has_update:
                        counters["blue_update"] += 1
                        mods_blue.append(plugin.name)
                    else:
                        counters["green_updated"] += 1
                        mods_green.append(plugin.name)
                else:
                    counters["orange_disabled"] += 1
                    mods_orange.append(plugin.name)
            else:
                counters["gray_not_installed"] += 1
                mods_gray.append(plugin.name)
    
        # Print summary
        #print(f"\n--- MOD SUMMARY ---")
        #print(f"🟢 GREEN (Updated and enabled): {counters['green_updated']}")
        #if mods_green:
        #    print(f"   Mods: {', '.join(mods_green)}")
        #
        #print(f"🔵 BLUE (Update available): {counters['blue_update']}")
        #if mods_blue:
        #    print(f"   Mods: {', '.join(mods_blue)}")
        #
        #print(f"🟠 ORANGE (Disabled): {counters['orange disabled']}")
        #if mods_orange:
        #    print(f"   Mods: {', '.join(mods_orange)}")
        #
        #print(f"🔴 RED (Manually installed): {counters['red_manual']}")
        #if mods_red:
        #    print(f"   Mods: {', '.join(mods_red)}")
        #
        #print(f"⚫ GRAY (Not installed): {counters['gray_not_installed']}")
        #if mods_gray:
        #    print(f"   Mods: {', '.join(mods_gray[:10])}{'...' if len(mods_gray) > 10 else ''}")
        #
        #print("=== END OF SUMMARY ===\n")
 
        # SHOW MESSAGE IF NO RESULTS
        if not plugin_names_ready_to_draw:
            no_results_text = f"No se encontraron mods que coincidan con '{search_term}'" if search_term else "No hay mods disponibles en esta categoría"
    
            bui.textwidget(
                parent=self._columnwidget,
                size=(410, 30),
                selectable=False,
                color=(0.7, 0.7, 0.7),
                text=no_results_text,
                h_align='center',
                v_align='center',
                maxwidth=420,
                scale=0.8
            )

            return
    
        # Draw the found plugins
        for i, plugin in enumerate(plugin_names_ready_to_draw):
            await self.draw_plugin_name(plugin, plugin_names_ready_to_draw)

    async def draw_plugin_name(self, plugin, plugins_list):
        # Get the local plugin if installed
        if plugin.is_installed:
            local_plugin = plugin.get_local()
            is_enabled = await local_plugin.is_enabled()
            has_update = plugin.has_update()

            #print(f"DEBUG: Mod status{plugin.name}:")
            #print(f"  - Installed: Yes")
            #print(f"  - Enabled: {is_enabled}")
            #print(f"  - Has update: {has_update}")
            #print(f"  - Installed via manager: {local_plugin.is_installed_via_plugin_manager}")

            if is_enabled:
                if not local_plugin.is_installed_via_plugin_manager:
                    color = (0.8, 0.2, 0.2)  # RED - Installed manually
                elif has_update:
                    color = (0.2, 0.5, 1.0)  # BLUE - Update available
                else:
                    color = (0, 0.95, 0.2)   # GREEN - Updated and enabled
            else:
                color = (1, 0.6, 0)          # ORANGE - Installed but disabled
        else:
            color = (0.5, 0.5, 0.5)          # GRAY - Not installed

        plugin_name_widget_to_update = self.plugins_in_current_view.get(plugin.name)
        if plugin_name_widget_to_update:
            bui.textwidget(
                edit=plugin_name_widget_to_update,
                color=color
            )
        else:
            text_widget = bui.textwidget(
                parent=self._columnwidget,
                size=(410, 30),
                selectable=True,
                always_highlight=True,
                color=color,
                text=plugin.name.replace('_', ' ').title(),
                click_activate=True,
                on_activate_call=lambda: self.show_plugin_window(plugin, plugins_list),
                h_align='left',
                v_align='center',
                maxwidth=420
            )
            self.plugins_in_current_view[plugin.name] = text_widget

    def show_plugin_window(self, plugin, plugins_list):
        ModWindow(
            plugin,
            self._root_widget,
            plugins_list=plugins_list,
            button_callback=lambda: self.draw_plugin_name(plugin, plugins_list)
        )

    def show_categories_window(self, source):
        PluginCategoryWindow(
            self.plugin_manager.categories.keys(),
            self.selected_category,
            source,
            self.select_category
        )

    async def select_category(self, category):
        internal_category = category

        self.plugins_in_current_view.clear()
        self.draw_category_selection_button(post_label=category) 
        await self.draw_plugin_names(
            internal_category, search_term=self._last_filter_text, refresh=True, order=self.selected_alphabet_order)
        self.selected_category = internal_category  # Save the internal name

    def cleanup(self):
        self.plugin_manager.cleanup()
        for plugin in self._columnwidget.get_children():
            plugin.delete()
        self.plugins_in_current_view.clear()
        self._last_filter_text = ""
        self._last_filter_plugins = []

    async def refresh(self):

        self.cleanup()
        self.spin(True)

        try:
            with self.exception_handler():
                # Force full cache clearing
                if "index" in _CACHE:
                    del _CACHE["index"]
                if "categories" in _CACHE:
                    del _CACHE["categories"] 

                await self.plugin_manager.refresh()
                await self.plugin_manager.setup_index()
                self.spin()

                try:
                    bui.textwidget(edit=self._plugin_manager_status_text, text="")
                except:
                    pass

                await self.select_category(self.selected_category)

        except Exception as e:
            self.spin()
            try:
                bui.textwidget(edit=self._plugin_manager_status_text, 
                             text=f"Error: {str(e)}")
            except:
                pass

    def soft_refresh(self):
        pass


class ModManagerSettingsWindow(popup.PopupWindow):
    def __init__(self, plugin_manager, origin_widget):
        self._plugin_manager = plugin_manager
        self.scale_origin = origin_widget.get_screen_space_center()
        self.settings = babase.app.config["Mod Manager"]["Settings"].copy()

        loop.create_task(self.draw_ui())


    async def perform_update(self, current_version, remote_version):
        # Call update_mod_manager which now handles all messages
        success = await update_mod_manager(current_version, remote_version)

        if success:
            # Refresh the interface after successful update
            bui.textwidget(
                edit=self._restart_to_reload_changes_text,
                text='¡Actualizado!\nReinicia el juego.'
            )
            # Hide the refresh button
            if hasattr(self, '_update_button') and self._update_button.exists():
                self._update_button.delete()

    async def draw_ui(self):
        b_text_color = (0.8, 0.8, 0.85)
        s = 1.25 if _uiscale() is babase.UIScale.SMALL else 1.27 if _uiscale() is babase.UIScale.MEDIUM else 1.3
        width = 380 * s
        height = 150 + 150 * s
        color = (0.9, 0.9, 0.9)

        # Subtracting the default bluish-purple color from the texture, so it's as close
        # as to white as possible.
        discord_fg_color = (10 - 0.32, 10 - 0.39, 10 - 0.96)
        discord_bg_color = (0.525, 0.595, 1.458)
        github_bg_color = (0.23, 0.23, 0.23)
        text_scale = 0.7 * s
        self._transition_out = 'out_scale'
        transition = 'in_scale'
        button_size = (32 * s, 32 * s)
        # index = await self._plugin_manager.get_index()
        self._root_widget = bui.containerwidget(
            size=(width, height),
            on_outside_click_call=self._ok,
            transition=transition,
            scale=(2.1 if _uiscale() is babase.UIScale.SMALL else 1.5
                   if _uiscale() is babase.UIScale.MEDIUM else 1.0),
            scale_origin_stack_offset=self.scale_origin,
            color=MAIN_COLOR
        )
        _add_popup(self)
        pos = height * 0.9
        setting_title = "Ajustes"
        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=setting_title,
            scale=text_scale,
            color=bui.app.ui_v1.title_color,
            maxwidth=width * 0.9
        )

        pos -= 20
        save_button_y = pos
        self._save_button = bui.buttonwidget(
            parent=self._root_widget,
            position=((width * 0.82) - button_size[0] / 2, save_button_y),
            size=(73, 35),
            on_activate_call=self.save_settings_button,
            textcolor=b_text_color,
            button_type='square',
            text_scale=1,
            scale=0,
            selectable=False,
            label="Guardar\n Cambios"
        )
        pos -= 40

        for setting, value in self.settings.items():
            bui.checkboxwidget(
                parent=self._root_widget,
                position=(width * 0.1, pos),
                size=(170, 30),
                text=setting,
                value=value,
                on_value_change_call=babase.Call(self.toggle_setting, setting),
                maxwidth=500,
                textcolor=(0.9, 0.9, 0.9),
                scale=text_scale * 0.8,
                color=MAIN_COLOR
            )
            pos -= 34 * text_scale

        pos = height - 180

        pos -= 75
        
        try:
            plugin_manager_update_available = await self._plugin_manager.get_update_details()
        except urllib.error.URLError:
            plugin_manager_update_available = False
        discord_width = (width * 0.20) if plugin_manager_update_available else (width * 0.31)
        
        self.discord_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(discord_width - button_size[0] / 2, pos),
            size=button_size,
            on_activate_call=lambda: bui.open_url(DISCORD_URL),
            textcolor=b_text_color,
            color=discord_bg_color,
            button_type='square',
            text_scale=1,
            label=""
        )

        bui.imagewidget(
            parent=self._root_widget,
            position=(discord_width+0.5 - button_size[0] / 2, pos),
            size=button_size,
            texture=bui.gettexture("discordLogo"),
            color=discord_fg_color,
            draw_controller=self.discord_button
        )

        github_width = (width * 0.49) if plugin_manager_update_available else (width * 0.65)
        self.github_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(github_width - button_size[0] / 2, pos),
            size=button_size,
            on_activate_call=lambda: bui.open_url(REPOSITORY_URL),
            textcolor=b_text_color,
            color=github_bg_color,
            button_type='square',
            text_scale=1,
            label=''
        )

        bui.imagewidget(
            parent=self._root_widget,
            position=(github_width + 0.5 - button_size[0] / 2, pos),
            size=button_size,
            texture=bui.gettexture("githubLogo"),
            color=(1, 1, 1),
            draw_controller=self.github_button
        )

        bui.containerwidget(edit=self._root_widget, on_cancel_call=self._ok)

        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos-20),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text='by: Less',
            scale=text_scale * 0.65,
            color=color,
            maxwidth=width * 0.95
        )

        # Divider line under the fork author
        bui.imagewidget(
            parent=self._root_widget,
            size=(90, 2),
            position=(width * 0.4, pos-30),
            texture=bui.gettexture("white"),
            color=(1, 1, 1)
        )

        try:
            # Verificar si hay actualización disponible usando nuestra función
            update_info = await check_for_update()
            plugin_manager_update_available = update_info['update_available']
            remote_version = update_info['remote_version']
        except urllib.error.URLError:
            plugin_manager_update_available = False
            remote_version = None

        if plugin_manager_update_available and remote_version:
            text_color = (0.75, 0.2, 0.2)
            button_size = (95 * s, 32 * s)
            update_button_label = f'Actualizar a v{remote_version}'
            self._update_button = bui.buttonwidget(
                parent=self._root_widget,
                position=((width * 0.2) - button_size[0] / 2, save_button_y),
                size=button_size,
                on_activate_call=lambda: loop.create_task(self.perform_update(update_info['current_version'], update_info['remote_version'])),
                textcolor=b_text_color,
                button_type='square',
                text_scale=1,
                color=(0, 0.7, 0),
                label=update_button_label
            )
            self._restart_to_reload_changes_text = bui.textwidget(
                parent=self._root_widget,
                position=((width * 0.4) - button_size[0] / 2, save_button_y+10),
                size=(0, 0),
                h_align='center',
                v_align='center',
                text='',
                scale=text_scale * 0.65,
                color=(0, 0.8, 0),
                maxwidth=width * 0.9
            )
        else:
            text_color = (0, 0.8, 0)
        
        pos -= 45
        
        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=f'Mod Manager v{MOD_MANAGER_VERSION}',
            scale=text_scale * 0.6,
            color=text_color,
            maxwidth=width * 0.95
        )
        
        pos -= 15
        
        bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.49, pos),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=f'API Version: {_app_api_version}',
            scale=text_scale * 0.5,
            color=(0.4, 0.8, 1),
            maxwidth=width * 0.95
        )

        pos = height * 0.1

    def toggle_setting(self, setting, set_value):
        self.settings[setting] = set_value
        check = self.settings == babase.app.config["Mod Manager"]["Settings"]
        bui.buttonwidget(
            edit=self._save_button,
            scale=0 if check else 1,
            selectable=(not check),
            color=MAIN_COLOR
        )

    def save_settings_button(self):
        babase.app.config["Mod Manager"]["Settings"] = self.settings.copy()
        babase.app.config.commit()
        self._ok()
        bui.getsound('gunCocking').play()

    def _ok(self) -> None:
        bui.getsound('swish').play()
        _remove_popup(self)
        bui.containerwidget(edit=self._root_widget, transition='out_scale')


class NewAllSettingsWindow(AllSettingsWindow):
    """Window for selecting a settings category."""

    def __init__(
        self,
        transition: str | None = 'in_right',
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        assert bui.app.classic is not None
        uiscale = bui.app.ui_v1.uiscale
        width = 1000 if uiscale is bui.UIScale.SMALL else 800
        x_inset = 125 if uiscale is bui.UIScale.SMALL else 105
        height = 490
        top_extra = 20 if uiscale is bui.UIScale.SMALL else 0
        self._plugman_button = None

        super().__init__(transition, origin_widget)

        for child in self._root_widget.get_children():
            child.delete()

        bui.containerwidget(
            edit=self._root_widget, size=(width, height + top_extra)
        )

        if uiscale is bui.UIScale.SMALL:
            self._back_button = None
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self.main_window_back
            )
        else:
            self._back_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                position=(x_inset - 20, height - 85),
                size=(130, 60),
                scale=0.8,
                text_scale=1.2,
                label=bui.Lstr(resource='backText'),
                button_type='back',
                on_activate_call=self.main_window_back,
            )
            bui.containerwidget(edit=self._root_widget, cancel_button=btn)

        bui.textwidget(
            parent=self._root_widget,
            position=(0, height - 80),
            size=(width, 25),
            text=bui.Lstr(resource=f'{self._r}.titleText'),
            color=bui.app.ui_v1.title_color,
            h_align='center',
            v_align='center',
            maxwidth=130,
        )

        if self._back_button is not None:
            bui.buttonwidget(
                edit=self._back_button,
                button_type='backSmall',
                size=(60, 60),
                label=bui.charstr(bui.SpecialChar.BACK),
            )

        v = height - 265
        basew = 280 if uiscale is bui.UIScale.SMALL else 230
        baseh = 170
        x_offs = (
            x_inset + (105 if uiscale is bui.UIScale.SMALL else 72) - basew
        )  # now unused
        x_dif = (basew - 7) / 2
        x_offs2 = x_offs + basew - 7
        x_offs3 = x_offs + 2 * (basew - 7)
        x_offs4 = x_offs + 3 * (basew - 7)
        x_offs5 = x_offs2
        x_offs6 = x_offs3
        x_offs2 -= x_dif
        x_offs3 -= x_dif
        x_offs4 -= x_dif

        def _b_title(
            x: float, y: float, button: bui.Widget, text: str | bui.Lstr
        ) -> None:
            bui.textwidget(
                parent=self._root_widget,
                text=text,
                position=(x + basew * 0.47, y + baseh * 0.22),
                maxwidth=basew * 0.7,
                size=(0, 0),
                h_align='center',
                v_align='center',
                draw_controller=button,
                color=(0.7, 0.9, 0.7, 1.0),
            )

        ctb = self._controllers_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(x_offs2, v),
            size=(basew, baseh),
            button_type='square',
            label='',
            on_activate_call=self._do_controllers,
        )
        if self._back_button is None:
            bbtn = bui.get_special_widget('back_button')
            bui.widget(edit=ctb, left_widget=bbtn)
        _b_title(
            x_offs2, v, ctb, bui.Lstr(resource=f'{self._r}.controllersText')
        )
        imgw = imgh = 130
        bui.imagewidget(
            parent=self._root_widget,
            position=(x_offs2 + basew * 0.49 - imgw * 0.5, v + 35),
            size=(imgw, imgh),
            texture=bui.gettexture('controllerIcon'),
            draw_controller=ctb,
        )

        gfxb = self._graphics_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(x_offs3, v),
            size=(basew, baseh),
            button_type='square',
            label='',
            on_activate_call=self._do_graphics,
        )
        pbtn = bui.get_special_widget('squad_button')
        bui.widget(edit=gfxb, up_widget=pbtn, right_widget=pbtn)
        _b_title(x_offs3, v, gfxb, bui.Lstr(resource=f'{self._r}.graphicsText'))
        imgw = imgh = 110
        bui.imagewidget(
            parent=self._root_widget,
            position=(x_offs3 + basew * 0.49 - imgw * 0.5, v + 42),
            size=(imgw, imgh),
            texture=bui.gettexture('graphicsIcon'),
            draw_controller=gfxb,
        )

        abtn = self._audio_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(x_offs4, v),
            size=(basew, baseh),
            button_type='square',
            label='',
            on_activate_call=self._do_audio,
        )
        _b_title(x_offs4, v, abtn, bui.Lstr(resource=f'{self._r}.audioText'))
        imgw = imgh = 120
        bui.imagewidget(
            parent=self._root_widget,
            position=(x_offs4 + basew * 0.49 - imgw * 0.5 + 5, v + 35),
            size=(imgw, imgh),
            color=(1, 1, 0),
            texture=bui.gettexture('audioIcon'),
            draw_controller=abtn,
        )

        v -= baseh - 5

        avb = self._advanced_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(x_offs5, v),
            size=(basew, baseh),
            button_type='square',
            label='',
            on_activate_call=self._do_advanced,
        )
        _b_title(x_offs5, v, avb, bui.Lstr(resource=f'{self._r}.advancedText'))
        imgw = imgh = 120
        bui.imagewidget(
            parent=self._root_widget,
            position=(x_offs5 + basew * 0.49 - imgw * 0.5 + 5, v + 35),
            size=(imgw, imgh),
            color=(0.8, 0.95, 1),
            texture=bui.gettexture('advancedIcon'),
            draw_controller=avb,
        )

        self._plugman_button = pmb = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(x_offs6, v),
            size=(basew, baseh),
            button_type='square',
            label='',
            on_activate_call=self._do_plugman,
        )
        _b_title(x_offs6, v, pmb, bui.Lstr(value="Mod Manager"))
        imgw = imgh = 120
        bui.imagewidget(
            parent=self._root_widget,
            position=(x_offs6 + basew * 0.49 - imgw * 0.5 + 5, v + 35),
            size=(imgw, imgh),
            color=(0.8, 0.95, 1),
            texture=bui.gettexture('storeIcon'),
            draw_controller=pmb,
        )
        self._restore_state()

    def _do_plugman(self) -> None:
        # no-op if we're not in control.
        if not self.main_window_has_control():
            return

        self.main_window_replace(
            ModManagerWindow(origin_widget=self._plugman_button)
        )

    def _save_state(self) -> None:
        try:
            sel = self._root_widget.get_selected_child()
            if sel == self._controllers_button:
                sel_name = 'Controllers'
            elif sel == self._graphics_button:
                sel_name = 'Graphics'
            elif sel == self._audio_button:
                sel_name = 'Audio'
            elif sel == self._advanced_button:
                sel_name = 'Advanced'
            elif sel == self._plugman_button:
                sel_name = 'PlugMan'
            elif sel == self._back_button:
                sel_name = 'Back'
            else:
                raise ValueError(f'unrecognized selection \'{sel}\'')
            assert bui.app.classic is not None
            bui.app.ui_v1.window_states[type(self)] = {'sel_name': sel_name}
        except Exception:
            logging.exception('Error saving state for %s.', self)

    def _restore_state(self) -> None:
        try:
            assert bui.app.classic is not None
            sel_name = bui.app.ui_v1.window_states.get(type(self), {}).get(
                'sel_name'
            )
            sel: bui.Widget | None
            if sel_name == 'Controllers':
                sel = self._controllers_button
            elif sel_name == 'Graphics':
                sel = self._graphics_button
            elif sel_name == 'Audio':
                sel = self._audio_button
            elif sel_name == 'Advanced':
                sel = self._advanced_button
            elif sel_name == "PlugMan":
                sel = self._plugman_button
            elif sel_name == 'Back':
                sel = self._back_button
            else:
                sel = self._controllers_button
            if sel is not None:
                bui.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            logging.exception('Error restoring state for %s.', self)


# ba_meta export babase.Plugin
class byLess(babase.Plugin):
    def on_app_running(self) -> None:
        """Called when the app is being launched."""
        from bauiv1lib.settings import allsettings
        allsettings.AllSettingsWindow = NewAllSettingsWindow
        DNSBlockWorkaround.apply()
        asyncio.set_event_loop(babase._asyncio._asyncio_event_loop)
        startup_tasks = StartupTasks()

        loop.create_task(startup_tasks.execute())
