from __future__ import annotations

import copy
import os
import time
import urllib.request
import json
from threading import Thread
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast, override

from bauiv1lib.gather import GatherTab
from bauiv1lib.gather.publictab import UIRow, PingThread, AddrFetchThread, Selection, SelectionComponent, PartyEntry
import bauiv1 as bui
import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any
    from bauiv1lib.gather import GatherWindow

API_BASE = os.environ.get('BA_API_URL', 'https://api.bombsquad.lat')

DEBUG_PROCESSING = False


@dataclass
class State:
    sub_tab: str = 'join'
    parties: list[tuple[str, PartyEntry]] | None = None
    next_entry_index: int = 0
    filter_value: str = ''
    have_server_list_response: bool = False
    have_valid_server_list: bool = False


class PublicLessGatherTab(GatherTab):
    def __init__(self, window: GatherWindow) -> None:
        super().__init__(window)
        self._idprefix = f'{window.main_window_id_prefix}|publicless'
        self._container: bui.Widget | None = None
        self._join_text: bui.Widget | None = None
        self._join_list_column: bui.Widget | None = None
        self._join_status_text: bui.Widget | None = None
        self._join_status_spinner: bui.Widget | None = None
        self._no_servers_found_text: bui.Widget | None = None
        self._not_signed_in_text: bui.Widget | None = None
        self._join_sub_scroll_width: float | None = None
        self._filter_text: bui.Widget | None = None
        self._host_scrollwidget: bui.Widget | None = None
        self._selection: Selection | None = None
        self._refreshing_list = False
        self._update_timer: bui.AppTimer | None = None
        self._last_server_list_query_time: float | None = None
        self._local_address: str | None = None
        self._last_connect_attempt_time: float | None = None
        self._ui_rows: list[UIRow] = []
        self._refresh_ui_row = 0
        self._have_user_selected_row = False
        self._first_valid_server_list_time: float | None = None
        self._parties: dict[str, PartyEntry] = {}
        self._parties_sorted: list[tuple[str, PartyEntry]] = []
        self._party_lists_dirty = True
        self._parties_displayed: dict[str, PartyEntry] = {}
        self._next_entry_index = 0
        self._have_server_list_response = False
        self._have_valid_server_list = False
        self._filter_value = ''
        self._pending_party_infos: list[dict[str, Any]] = []
        self._last_sub_scroll_height = 0.0

    @override
    def on_activate(
        self,
        parent_widget: bui.Widget,
        tab_button: bui.Widget,
        region_width: float,
        region_height: float,
        region_left: float,
        region_bottom: float,
    ) -> bui.Widget:
        c_width = region_width
        c_height = region_height - 20
        self._container = bui.containerwidget(
            parent=parent_widget,
            position=(region_left, region_bottom + (region_height - c_height) * 0.5),
            size=(c_width, c_height),
            background=False,
            selection_loops_to_parent=True,
        )
        v = c_height - 30
        self._join_text = bui.textwidget(
            parent=self._container,
            id=f'{self._idprefix}|jointab',
            position=(c_width * 0.5, v),
            color=(0.6, 1.0, 0.6),
            scale=1.3,
            size=(0, 0),
            maxwidth=c_width * 0.9,
            h_align='center',
            v_align='center',
            click_activate=True,
            selectable=True,
            autoselect=True,
            on_activate_call=lambda: None,
            text='Join a public party(less)',
            glow_type='uniform',
        )
        bui.widget(edit=self._join_text, up_widget=tab_button)

        if self._local_address is None:
            AddrFetchThread(
                bui.WeakCallPartial(self._fetch_local_addr_cb)
            ).start()

        self._build_join_tab(region_width, region_height)
        self._update_timer = bui.AppTimer(
            0.1, bui.WeakCallStrict(self._update), repeat=True
        )
        return self._container

    @override
    def on_deactivate(self) -> None:
        self._update_timer = None

    @override
    def save_state(self) -> None:
        assert bui.app.classic is not None
        bui.app.ui_v1.window_states[type(self)] = State(
            parties=[(i, copy.copy(p)) for i, p in self._parties_sorted[:40]],
            next_entry_index=self._next_entry_index,
            filter_value=self._filter_value,
            have_server_list_response=self._have_server_list_response,
            have_valid_server_list=self._have_valid_server_list,
        )

    @override
    def restore_state(self) -> None:
        assert bui.app.classic is not None
        state = bui.app.ui_v1.window_states.get(type(self))
        if state is None:
            state = State()
        assert isinstance(state, State)
        if state.parties:
            self._parties = {key: copy.copy(party) for key, party in state.parties}
            self._parties_sorted = list(self._parties.items())
            self._party_lists_dirty = True
            self._next_entry_index = state.next_entry_index
            self._have_server_list_response = state.have_server_list_response
            self._have_valid_server_list = state.have_valid_server_list
        self._filter_value = state.filter_value

    def _build_join_tab(self, region_width: float, region_height: float) -> None:
        c_width = region_width
        c_height = region_height - 20
        sub_scroll_height = c_height - 125
        self._join_sub_scroll_width = sub_scroll_width = min(1200, region_width - 80)
        v = c_height - 35
        v -= 60
        filter_txt = bui.Lstr(resource='filterText')
        self._filter_text = bui.textwidget(
            parent=self._container,
            id=f'{self._idprefix}|filter',
            text=self._filter_value,
            size=(350, 45),
            position=(c_width * 0.5 - 150, v - 10),
            h_align='left',
            v_align='center',
            editable=True,
            maxwidth=310,
            description=filter_txt,
        )
        bui.widget(edit=self._filter_text, up_widget=self._join_text)
        bui.textwidget(
            text=filter_txt,
            parent=self._container,
            size=(0, 0),
            position=(c_width * 0.5 - 170, v + 13),
            maxwidth=150,
            scale=0.8,
            color=(0.5, 0.46, 0.5),
            flatness=1.0,
            h_align='right',
            v_align='center',
        )
        bui.textwidget(
            text=bui.Lstr(resource='nameText'),
            parent=self._container,
            size=(0, 0),
            position=((c_width - sub_scroll_width) * 0.5 + 50, v - 8),
            maxwidth=60,
            scale=0.6,
            color=(0.5, 0.46, 0.5),
            flatness=1.0,
            h_align='center',
            v_align='center',
        )
        bui.textwidget(
            text=bui.Lstr(resource='gatherWindow.partySizeText'),
            parent=self._container,
            size=(0, 0),
            position=(c_width * 0.5 + sub_scroll_width * 0.5 - 110, v - 8),
            maxwidth=60,
            scale=0.6,
            color=(0.5, 0.46, 0.5),
            flatness=1.0,
            h_align='center',
            v_align='center',
        )
        bui.textwidget(
            text=bui.Lstr(resource='gatherWindow.pingText'),
            parent=self._container,
            size=(0, 0),
            position=(c_width * 0.5 + sub_scroll_width * 0.5 - 30, v - 8),
            maxwidth=60,
            scale=0.6,
            color=(0.5, 0.46, 0.5),
            flatness=1.0,
            h_align='center',
            v_align='center',
        )
        v -= sub_scroll_height + 23
        self._host_scrollwidget = scrollw = bui.scrollwidget(
            parent=self._container,
            simple_culling_v=10,
            position=((c_width - sub_scroll_width) * 0.5, v),
            size=(sub_scroll_width, sub_scroll_height),
            claims_up_down=False,
            claims_left_right=True,
            autoselect=True,
        )
        self._join_list_column = bui.containerwidget(
            parent=scrollw,
            id=f'{self._idprefix}|joinlistcolumn',
            background=False,
            size=(400, 400),
            claims_left_right=True,
        )
        self._join_status_text = bui.textwidget(
            parent=self._container,
            text='',
            size=(0, 0),
            scale=0.9,
            flatness=1.0,
            shadow=0.0,
            h_align='center',
            v_align='top',
            maxwidth=c_width,
            color=(0.6, 0.6, 0.6),
            position=(c_width * 0.5, c_height * 0.5),
        )
        self._join_status_spinner = bui.spinnerwidget(
            parent=self._container,
            position=(c_width * 0.5, c_height * 0.5),
            style='bomb',
            size=64,
        )
        self._no_servers_found_text = bui.textwidget(
            parent=self._container,
            text='',
            size=(0, 0),
            scale=0.9,
            flatness=1.0,
            shadow=0.0,
            h_align='center',
            v_align='top',
            color=(0.6, 0.6, 0.6),
            position=(c_width * 0.5, c_height * 0.5),
        )
        self._not_signed_in_text = bui.textwidget(
            parent=self._container,
            text='Not Signed In',
            size=(0, 0),
            scale=1.0,
            flatness=1.0,
            shadow=0.0,
            h_align='center',
            v_align='center',
            color=(1.0, 0.4, 0.4),
            position=(c_width * 0.5, c_height * 0.5),
        )

    def _update(self) -> None:
        text = self._filter_text
        if text:
            filter_value = cast(str, bui.textwidget(query=text))
            if filter_value != self._filter_value:
                self._filter_value = filter_value
                self._party_lists_dirty = True
                for party in self._parties.values():
                    party.clean_display_index = None

        self._query_party_list_periodically()
        self._ping_parties_periodically()
        self._process_pending_party_infos()
        self._update_party_lists()

        if self._not_signed_in_text:
            v3_token = bui.app.config.get('V3 Token', '')
            bui.textwidget(
                edit=self._not_signed_in_text,
                text='' if v3_token else 'Not Signed In',
            )

        if self._join_status_text:
            assert self._join_status_spinner
            if self._have_valid_server_list:
                bui.textwidget(edit=self._join_status_text, text='')
                bui.spinnerwidget(edit=self._join_status_spinner, visible=False)
            elif self._have_server_list_response:
                bui.textwidget(edit=self._join_status_text, text='')
                bui.spinnerwidget(edit=self._join_status_spinner, visible=False)
            else:
                bui.textwidget(edit=self._join_status_text, text='')
                bui.spinnerwidget(edit=self._join_status_spinner, visible=True)

        self._update_party_rows()

    def _query_party_list_periodically(self) -> None:
        now = bui.apptime()
        if self._last_server_list_query_time is None or now - self._last_server_list_query_time > 10.0:
            self._last_server_list_query_time = now
            ServerListFetchThread(
                bui.WeakCallPartial(self._on_server_list_result)
            ).start()

    def _on_server_list_result(self, result: dict[str, Any] | None) -> None:
        self._have_server_list_response = True
        if result is None:
            v3_token = bui.app.config.get('V3 Token', '')
            self._have_valid_server_list = bool(v3_token)
            return

        if not self._have_valid_server_list:
            self._first_valid_server_list_time = time.time()
        self._have_valid_server_list = True

        servers = result.get('servers', [])
        self._pending_party_infos += servers

        for partyval in list(self._parties.values()):
            partyval.claimed = False
        for server in servers:
            addr = server.get('address', '')
            port = server.get('port', -1)
            party_key = f'{addr}_{port}'
            party = self._parties.get(party_key)
            if party is not None:
                party.claimed = True
        self._parties = {
            key: val for key, val in list(self._parties.items()) if val.claimed
        }
        self._parties_sorted = [p for p in self._parties_sorted if p[1].claimed]
        self._party_lists_dirty = True

        if DEBUG_PROCESSING:
            print(f'Handled server list results: {len(servers)} servers')

    def _process_pending_party_infos(self) -> None:
        chunksize = 30
        parties_in = self._pending_party_infos[:chunksize]
        self._pending_party_infos = self._pending_party_infos[chunksize:]
        for server in parties_in:
            addr = server.get('address', '')
            assert isinstance(addr, str)
            port = server.get('port', -1)
            assert isinstance(port, int)
            party_key = f'{addr}_{port}'
            party = self._parties.get(party_key)
            if party is None:
                party = PartyEntry(
                    address=addr,
                    next_ping_time=bui.apptime() + 5.0,
                    index=self._next_entry_index,
                )
                self._parties[party_key] = party
                self._parties_sorted.append((party_key, party))
                self._party_lists_dirty = True
                self._next_entry_index += 1
            party.port = port
            party.name = server.get('name', server.get('host_name', ''))
            assert isinstance(party.name, str)
            party.size = server.get('player_count', 0)
            assert isinstance(party.size, int)
            party.size_max = server.get('max_players', 0)
            assert isinstance(party.size_max, int)
            party.ping_interval = 10.0
            party.clean_display_index = None

            if DEBUG_PROCESSING and parties_in:
                print(f'Processed server: {party.name} at {addr}:{port}')

    def _update_party_lists(self) -> None:
        if not self._party_lists_dirty:
            return
        self._parties_sorted.sort(
            key=lambda p: (
                p[1].ping if p[1].ping is not None else 999999.0,
                p[1].index,
            )
        )
        if not self._have_valid_server_list:
            self._parties_displayed = {}
        else:
            if self._filter_value:
                filterval = self._filter_value.lower()
                self._parties_displayed = {
                    k: v
                    for k, v in self._parties_sorted
                    if filterval in v.name.lower()
                }
            else:
                self._parties_displayed = dict(self._parties_sorted)
        if self._selection is not None and self._selection.entry_key not in self._parties_displayed:
            self._have_user_selected_row = False
        if not self._have_user_selected_row and self._parties_displayed:
            firstpartykey = next(iter(self._parties_displayed))
            self._selection = Selection(firstpartykey, SelectionComponent.NAME)
        self._party_lists_dirty = False

    def _update_party_rows(self) -> None:
        columnwidget = self._join_list_column
        if not columnwidget:
            return
        assert self._join_text
        assert self._filter_text
        assert self._host_scrollwidget
        bui.containerwidget(
            edit=self._host_scrollwidget,
            claims_up_down=(len(self._parties_displayed) > 0),
        )
        bui.textwidget(edit=self._no_servers_found_text, text='')
        clipcount = len(self._ui_rows) - len(self._parties_displayed)
        if clipcount > 0:
            clipcount = max(clipcount, 50)
            self._ui_rows = self._ui_rows[:-clipcount]
        if self._have_valid_server_list and not self._parties_displayed:
            v3_token = bui.app.config.get('V3 Token', '')
            if v3_token:
                bui.textwidget(
                    edit=self._no_servers_found_text,
                    text='No parties found',
                )
            return
        assert self._join_sub_scroll_width is not None
        sub_scroll_width = self._join_sub_scroll_width
        lineheight = 42
        sub_scroll_height = lineheight * len(self._parties_displayed) + 50
        bui.containerwidget(
            edit=columnwidget, size=(sub_scroll_width, sub_scroll_height)
        )
        if sub_scroll_height != self._last_sub_scroll_height:
            self._refresh_ui_row = 0
            self._last_sub_scroll_height = sub_scroll_height
            for party in self._parties.values():
                party.clean_display_index = None

        def refresh_on() -> None:
            self._refreshing_list = True
        bui.pushcall(refresh_on)
        rowcount = min(12, len(self._parties_displayed))
        party_vals_displayed = list(self._parties_displayed.values())
        while rowcount > 0:
            refresh_row = self._refresh_ui_row % len(self._parties_displayed)
            if refresh_row >= len(self._ui_rows):
                self._ui_rows.append(UIRow())
                refresh_row = len(self._ui_rows) - 1
            if self._first_valid_server_list_time is not None:
                if time.time() - self._first_valid_server_list_time < 4.0:
                    if refresh_row > 40:
                        refresh_row = 0
            self._ui_rows[refresh_row].update(
                refresh_row,
                party_vals_displayed[refresh_row],
                sub_scroll_width=sub_scroll_width,
                sub_scroll_height=sub_scroll_height,
                lineheight=lineheight,
                columnwidget=columnwidget,
                join_text=self._join_text,
                existing_selection=self._selection,
                filter_text=self._filter_text,
                tab=self,
            )
            self._refresh_ui_row = refresh_row + 1
            rowcount -= 1

        def refresh_off() -> None:
            self._refreshing_list = False
        bui.pushcall(refresh_off)

    def _ping_parties_periodically(self) -> None:
        assert bui.app.classic is not None
        now = bui.apptime()
        for party in list(self._parties.values()):
            if party.next_ping_time <= now and bui.app.classic.ping_thread_count < 15:
                mult = 1
                if party.ping_responses == 0:
                    if party.ping_attempts > 4:
                        mult = 10
                    elif party.ping_attempts > 2:
                        mult = 5
                if party.ping is not None:
                    mult = 10 if party.ping > 300 else 5 if party.ping > 150 else 2
                interval = party.ping_interval * mult
                party.next_ping_time = now + party.ping_interval * mult
                party.ping_attempts += 1
                PingThread(
                    party.address,
                    party.port,
                    bui.WeakCallPartial(self._ping_callback),
                ).start()

    def _ping_callback(self, address: str, port: int | None, result: float | None) -> None:
        party_key = f'{address}_{port}'
        party = self._parties.get(party_key)
        if party is not None:
            if result is not None:
                party.ping_responses += 1
            current_ping = party.ping
            if current_ping is not None and result is not None and result < 150:
                smoothing = 0.7
                party.ping = smoothing * current_ping + (1.0 - smoothing) * result
            else:
                party.ping = result
            party.clean_display_index = None
            self._party_lists_dirty = True

    def _fetch_local_addr_cb(self, val: str) -> None:
        self._local_address = str(val)

    def on_public_party_activate(self, party: PartyEntry) -> None:
        self.save_state()
        address = party.address
        port = party.port
        if bs.app.classic is not None:
            bs.app.classic.save_ui_state()
        now = time.time()
        last_connect_time = self._last_connect_attempt_time
        if last_connect_time is None or now - last_connect_time > 2.0:
            bs.connect_to_party(address, port=port)
            self._last_connect_attempt_time = now

    def set_public_party_selection(self, sel: Selection) -> None:
        if self._refreshing_list:
            return
        self._selection = sel
        self._have_user_selected_row = True


class ServerListFetchThread(Thread):
    def __init__(self, call):
        super().__init__()
        self._call = call

    @override
    def run(self) -> None:
        try:
            req = urllib.request.Request(f'{API_BASE}/api/servers')
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read().decode())
            bui.pushcall(
                bui.CallStrict(self._call, data), from_other_thread=True
            )
        except Exception:
            bui.pushcall(
                bui.CallStrict(self._call, None), from_other_thread=True
            )
