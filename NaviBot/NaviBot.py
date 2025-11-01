# ba_meta nomod

from bascenev1lib.actor.spaz import Spaz
from babase import (
    app
)
import bascenev1 as bs
from math import sqrt
import json
import os, glob
from typing import TYPE_CHECKING, Tuple
from bauiv1 import (
    app as APP
)

if TYPE_CHECKING:
    from typing import Any, Tuple

try:
    from bubble import Bubble
    HAS_BUBBLE = True
except ImportError:
    HAS_BUBBLE = False

from random import choice

DEBUG = False


def D(): d = APP.classic.spaz_appearances; [d.pop(i) for i in d.copy() if i != 'Pascal' and d[i].default_color == (0.3,0.5,0.8)]; return d
NAME = lambda: list(D())

def log(msg):
    if DEBUG:
        print(f"[NaviBot] {msg}")

class NavGraph:
    """Handles navigation mesh loading and pathfinding"""

    # ADJUSTABLE: How much to penalize steep climbs (higher = avoid steep paths more)
    CLIMB_PENALTY = 5.0  # Multiply edge cost by this when climbing

    def __init__(self, filename):
        self.nodes = []
        self.edges = {}
        self.loaded = False
        self._load(filename)

    def _load(self, filename):
        try:
            filepath = os.path.join(app.env.python_directory_user, 'Paths', filename)

            if not os.path.exists(filepath):
                print(f"[NavGraph] File not found: {filepath}")
                return

            with open(filepath, 'r') as f:
                data = json.load(f)

            self.nodes = data.get('nodes', [])

            # Build adjacency list from node neighbors
            self.edges = {}
            for node in self.nodes:
                node_id = node['id']
                self.edges[node_id] = []

                pos = node['position']
                for neighbor_id in node.get('neighbors', []):
                    if neighbor_id < len(self.nodes):
                        neighbor_pos = self.nodes[neighbor_id]['position']
                        dist = self._distance(pos, neighbor_pos)

                        # PENALIZE UPHILL EDGES
                        height_diff = neighbor_pos[1] - pos[1]
                        if height_diff > 0:
                            dist *= self.CLIMB_PENALTY  # Make steep paths "longer"

                        self.edges[node_id].append((neighbor_id, dist))

            self.loaded = len(self.nodes) > 0
            log(f"Loaded {len(self.nodes)} nodes with climb penalty {self.CLIMB_PENALTY}x")

        except Exception as e:
            print(f"[NavGraph] Load error: {e}")

    @staticmethod
    def _distance(a, b):
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

    def find_nearest_node(self, pos):
        """Find closest navigation node to position"""
        if not self.nodes:
            return None

        best_id = 0
        best_dist = float('inf')

        for node in self.nodes:
            dist = self._distance(pos, node['position'])
            if dist < best_dist:
                best_dist = dist
                best_id = node['id']

        return best_id

    def find_path(self, start_pos, goal_pos):
        """A* pathfinding between two positions"""
        start_id = self.find_nearest_node(start_pos)
        goal_id = self.find_nearest_node(goal_pos)

        if start_id is None or goal_id is None:
            return []

        if start_id == goal_id:
            return [goal_pos]

        # A* algorithm
        open_set = {start_id}
        came_from = {}
        g_score = {start_id: 0}

        def heuristic(node_id):
            pos = self.nodes[node_id]['position']
            return self._distance(pos, self.nodes[goal_id]['position'])

        f_score = {start_id: heuristic(start_id)}

        while open_set:
            current = min(open_set, key=lambda n: f_score.get(n, float('inf')))

            if current == goal_id:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(self.nodes[current]['position'])
                    current = came_from[current]
                path.reverse()
                path.append(goal_pos)
                return path

            open_set.remove(current)

            for neighbor_id, edge_cost in self.edges.get(current, []):
                tentative_g = g_score[current] + edge_cost

                if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g
                    f_score[neighbor_id] = tentative_g + heuristic(neighbor_id)
                    open_set.add(neighbor_id)

        return []

class BotTests:
    def __init__(self, interval=8.0):
        self.interval = interval
        self.bots = []
        self.blue_marks = []
        self.red_marks = []
        self.is_running = False
        self.current_timer = None
        
        # Cods
        self.BASE_X = 10.799479484558105
        self.BASE_Y = 0.30053645372390747
        self.Z_POSITIONS = [
            -4.474666714668274, -3.474666714668274, -1.474666714668274,
            1.474666714668274, 3.474666714668274, 4.474666714668274
        ]
        
        # Create environment immediately upon instantiation
        self._setup_test_environment()
        print("[BotTests] Instance created - bots and bookmarks ready")
    
    def start(self):
        """Start the lateral movement test"""
        if self.is_running:
            print("[BotTests] The test is already running.")
            return
            
        self.is_running = True
        
        # Start movement cycle
        self._go_to_red()
        print("[BotTests] Test initiated - active lateral movement")
    
    def stop(self):
        """Stop all movements"""
        if not self.is_running:
            print("[BotTests] The test is not running")
            return
            
        self.is_running = False
        
        # Cancelar timer actual
        if self.current_timer is not None:
            self.current_timer = None
            
        # Stop all bots
        for i, bot in enumerate(self.bots):
            bot.stop()
            print(f"[BotTests] Bot #{i+1} detained in his current position")
            
        print("[BotTests] Test stopped - all bots stopped")
    
    def _setup_test_environment(self):
        """Configure markers and spawn bots (runs on instantiation)"""
        # Create blue positions (negative X)
        self.blue_marks = self._generate_side_positions(negative_x=True)
        self._create_marks(self.blue_marks, (0.2, 0.4, 1), "blue")
        
        # Create red positions (positive X)
        self.red_marks = self._generate_side_positions(negative_x=False)
        self._create_marks(self.red_marks, (1, 0.2, 0.2), "red")
        
        # Spawn bots in blue positions
        self.bots = self._spawn_bots_at_marks(self.blue_marks)
    
    def _generate_side_positions(self, negative_x=False):
        """Generate positions for one side (blue or red)"""
        x = -self.BASE_X if negative_x else self.BASE_X
        return [(x, self.BASE_Y, z) for z in self.Z_POSITIONS]
    
    def _create_marks(self, positions, color, label):
        """Create locator nodes for visualization"""
        for i, pos in enumerate(positions):
            bs.newnode('locator', attrs={
                'shape': 'circle', 'position': pos, 'color': color,
                'opacity': 0.6, 'draw_beauty': True, 'additive': True
            })
            print(f"[BotTests] Marker {label} #{i+1} in ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
    
    def _spawn_bots_at_marks(self, positions):
        """Spawn bots in the specified positions"""
        bots = []
        hm = NAME()
        for i, pos in enumerate(positions):
            random_character = choice(hm)
            bot = NaviBot(
                position=pos,
                color=(0.2, 0.5 + i * 0.05, 1),  # Blue with variation
                highlight=(1, 1, 1),
                character=random_character
            )
            bots.append(bot)
            print(f"[BotTests] Bot #{i+1} ({random_character}) spawned at ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
        return bots
    
    def _go_to_red(self):
        """Move all bots to red positions"""
        if not self.is_running:
            return
            
        print("[BotTests] Moving bots to RED positions")
        for i, bot in enumerate(self.bots):
            if i < len(self.red_marks):
                x, y, z = self.red_marks[i]
                bot.move_to_point(x, y, z)
        
        # Schedule next move
        self.current_timer = bs.apptimer(self.interval, self._go_to_blue)
    
    def _go_to_blue(self):
        """Mover todos los bots a posiciones azules"""
        if not self.is_running:
            return
            
        print("[BotTests] Moving bots to BLUE positions")
        for i, bot in enumerate(self.bots):
            if i < len(self.blue_marks):
                x, y, z = self.blue_marks[i]
                bot.move_to_point(x, y, z)
        
        # Schedule next move
        self.current_timer = bs.apptimer(self.interval, self._go_to_red)
        



class NaviBot:
    """Smart navigation bot for BombSquad"""

    MAX_VELOCITY = 5.0  # Max horizontal velocity before slowing down
    marks_created = False
    def __init__(self, position=(0,0,0), color=(0,0,0), highlight=(0.1,0.1,0.1), character='Pixel'):
        # Spawn bot
        self.bot = Spaz(color=color, highlight=highlight, character=character)
        self.bot.handlemessage(bs.StandMessage(position, 0))
        self.node = self.bot.node
        # Detect current map
        # Build JSON filename dynamically

        map_name, tex_name = self._get_current_map_name()
        print(f"[NaviBot] Current map: {map_name}, texture: {tex_name}")

        self.NAV_FILE = self._find_nav_file(tex_name)
        print(f"[NaviBot] Using navigation file: {self.NAV_FILE}")

        self.nav = NavGraph(self.NAV_FILE)

        if not self.nav.loaded:
            print(f"[NaviBot] Failed to load navigation data for {self.NAV_FILE}")
            return

        # Navigation state
        self.target = None
        self.path = []
        self.current_waypoint = 0

        # Timers
        self.update_apptimer = None
        self.abuse_apptimer = None

        # Movement state
        self.last_pos = None
        self.stuck_counter = 0

        # Height tracking for vertical movement
        self.vertical_progress_start = None
        self.last_height = None
        
        # Velocity control
        self.run_multiplier = 1.0  # Controls run intensity (0 to 1)

        self._speak("NaviBot online")
        log("Initialized")


    def generate_marks(self, x=12.7, y=0.3, z_start=-5.2, z_end=5.7, step=2.0):
        marks = []
        z = z_start
        while z <= z_end:
            marks.append((x, y, z))
            z += step
        return marks

    def _find_nav_file(self, tex_name: str) -> str:
        """Find nav file case-insensitively and with flexible suffix matching."""
        paths_dir = os.path.expanduser("~/.bombsquad/mods/Paths")
        if not os.path.isdir(paths_dir):
            # fallback to module-relative path if necessary
            paths_dir = os.path.join(os.path.dirname(__file__), "Paths")

        if not tex_name:
            return os.path.join(paths_dir, "cragCastleLevelCollide_navguide.json")

        want = tex_name.casefold()  # normalized search token

        candidates = []
        try:
            for fn in os.listdir(paths_dir):
                fn_lower = fn.casefold()
                # consider files that contain the token and end with _navguide.json
                if want in fn_lower and fn_lower.endswith("_navguide.json"):
                    candidates.append(fn)
            # if no strict _navguide match, accept files that contain token and 'collide' somewhere
            if not candidates:
                for fn in os.listdir(paths_dir):
                    fn_lower = fn.casefold()
                    if want in fn_lower and "collide" in fn_lower:
                        candidates.append(fn)
        except FileNotFoundError:
            candidates = []

        if not candidates:
            fallback = os.path.join(paths_dir, "cragCastleLevelCollide_navguide.json")
            print(f"[NaviBot] ⚠️ Nav file not found for {tex_name}, using fallback {fallback}")
            return fallback

        # Prefer exact-start matches (e.g. footballStadium...); otherwise pick shortest name (likely exact)
        def score(fn):
            fn_lower = fn.casefold()
            s = 0
            if fn_lower.startswith(want):
                s += 10
            if fn_lower.endswith("_navguide.json"):
                s += 5
            # prefer filenames that contain 'collide'
            if "collide" in fn_lower:
                s += 2
            # shorter is better
            s -= len(fn)
            return -s  # will sort ascending, we want highest score first -> negative

        candidates.sort(key=score)
        chosen = candidates[0]
        return os.path.join(paths_dir, chosen)
    
    def _get_current_map_name(self) -> tuple[str | None, str | None]:
        act = bs.get_foreground_host_activity()
        if isinstance(act, bs.GameActivity):
            texname = act.map.get_preview_texture_name()
            if texname:
                return act.map.name, texname.lower().removesuffix("preview")
        return None, None

    def _speak(self, text):
        """Display dialogue bubble if available"""
        if HAS_BUBBLE and self.node and self.node.exists():
            Bubble(node=self.node, text=text, time=2.0, color=self.node.color)

    def yay(self):
        """Yay"""
        self.node.handlemessage('celebrate',200)

    def move_to_point(self, x, y, z):
        """Command bot to navigate to target position"""
        self.target = (x, y, z)
        self.path = []
        self.current_waypoint = 0
        self.stuck_counter = 0
        self.vertical_progress_start = None
        self.last_height = None
        self.run_multiplier = 1.0

        log(f"New target: {self.target}")
        self._speak("Moving out!")

        # Start update loops
        if self.update_apptimer is None:
            self.update_apptimer = bs.Timer(0.05, self._update, repeat=True)
            self.abuse_apptimer = bs.Timer(0.15, self._abuse_movement, repeat=True)

    def stop(self):
        """Stop all movement"""
        self.target = None
        self.path = []
        self.update_apptimer = None
        self.abuse_apptimer = None

        if self.bot.exists():
            self.bot.on_move_left_right(0)
            self.bot.on_move_up_down(0)
            self.bot.on_run(0)

    def _abuse_movement(self):
        """Abuse apptimer for 90 degree breaks (mandatory) - uses run_multiplier"""
        if self.bot.exists():
            self.bot.on_run(0)
            bs.apptimer(0.02, lambda: self.bot.on_run(self.run_multiplier))

    def _check_velocity(self):
        """Monitor velocity and adjust run_multiplier to prevent falling"""
        if not self.node or not self.node.exists():
            return
        
        try:
            vx, vy, vz = self.node.velocity
            horizontal_speed = sqrt(vx**2 + vz**2)
            
            if horizontal_speed > self.MAX_VELOCITY:
                # Too fast! Stop running to slow down
                self.run_multiplier = 0.0
                log(f"Velocity too high: {horizontal_speed:.2f}, cooling down")
            else:
                # Safe speed, resume running
                if self.run_multiplier < 1.0:
                    self.run_multiplier = 1.0
                    log(f"Velocity safe: {horizontal_speed:.2f}, resuming")
        except:
            pass

    def _update(self):
        """Main navigation update loop"""
        # Safety checks
        if not self.target or not self.node or not self.node.exists():
            self.stop()
            return

        try:
            pos = tuple(self.node.position)
        except:
            self.stop()
            return
        
        # Check velocity to prevent falling from momentum
        self._check_velocity()

        # Check if we reached the target
        dist_to_target = sqrt(
            (pos[0] - self.target[0])**2 +
            (pos[1] - self.target[1])**2 +
            (pos[2] - self.target[2])**2
        )

        if dist_to_target < 0.5:
            log("Target reached!")
            self._speak("Target acquired")
            self.yay()
            self.stop()
            return

        # Generate path if needed
        if not self.path or self._should_replan(pos):
            self.path = self.nav.find_path(pos, self.target)
            self.current_waypoint = 0
            self.vertical_progress_start = None

            if not self.path:
                log("No path found")
                self._speak("Path blocked")
                self._move(0, 0)
                return

            log(f"Path calculated: {len(self.path)} waypoints")

        # Check for being stuck
        if self._is_stuck(pos):
            log("Stuck detected, replanning")
            self._speak("Recalculating")
            self.path = []
            self.stuck_counter = 0
            self.vertical_progress_start = None
            return

        # Navigate to current waypoint
        if self.current_waypoint >= len(self.path):
            self._move(0, 0)
            return

        waypoint = self.path[self.current_waypoint]

        # Calculate distances
        dist_2d = sqrt(
            (pos[0] - waypoint[0])**2 +
            (pos[2] - waypoint[2])**2
        )

        height_diff = waypoint[1] - pos[1]

        # CRITICAL: Handle vertical movement specially
        # If waypoint is significantly above us, we're climbing
        if height_diff > 0:
            # We're going uphill - TINY distance threshold

            if self.vertical_progress_start is None:
                self.vertical_progress_start = pos[1]
                self.last_height = pos[1]

            # Calculate FULL 3D distance to waypoint
            dist_3d = sqrt(
                (pos[0] - waypoint[0])**2 +
                (pos[1] - waypoint[1])**2 +
                (pos[2] - waypoint[2])**2
            )

            # TINY THRESHOLD - must be basically ON TOP of the waypoint
            can_advance = dist_3d < 0.1

            if can_advance:
                log(f"Climb complete: 3D distance {dist_3d:.3f}")
                self.current_waypoint += 1
                self.vertical_progress_start = None
                self.last_height = None
                if self.current_waypoint < len(self.path):
                    waypoint = self.path[self.current_waypoint]
                else:
                    return
        else:
            # Normal horizontal movement or downhill - standard distance check
            if dist_2d < 0.4:
                self.current_waypoint += 1
                self.vertical_progress_start = None
                self.last_height = None
                if self.current_waypoint < len(self.path):
                    waypoint = self.path[self.current_waypoint]
                else:
                    return

        # Move towards waypoint
        dx = waypoint[0] - pos[0]
        dz = waypoint[2] - pos[2]
        dist = sqrt(dx*dx + dz*dz)

        if dist > 0.01:
            move_x = dx / dist
            move_z = dz / dist
            self._move(move_x, move_z)
        else:
            self._move(0, 0)

        self.last_pos = pos
        self.last_height = pos[1]

    def _move(self, x, z):
        """Set bot movement direction"""
        if self.bot.exists():
            self.bot.on_move_left_right(x)
            self.bot.on_move_up_down(-z)
            # Always call on_run with run_multiplier (controlled by velocity check)
            self.bot.on_run(self.run_multiplier if (x != 0 or z != 0) else 0)

    def _should_replan(self, pos):
        """Check if path needs recalculation"""
        if not self.path:
            return True

        # Replan if bot has drifted far from path
        if self.current_waypoint < len(self.path):
            wp = self.path[self.current_waypoint]
            dist = sqrt((pos[0]-wp[0])**2 + (pos[2]-wp[2])**2)
            if dist > 5.0:
                return True

        return False

    def _is_stuck(self, pos):
        """Detect if bot is stuck"""
        if self.last_pos is None:
            return False

        movement = sqrt(
            (pos[0] - self.last_pos[0])**2 +
            (pos[2] - self.last_pos[2])**2
        )

        if movement < 0.02:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        return self.stuck_counter > 30  # ~1.5 seconds of no movement


# Test function
def spawn_test_bot():
    """Spawn a test bot for debugging"""
    bot = NaviBot(
        position=(0, 5, 0),
        color=(0, 0, 0),
        highlight=(0.1, 0.1, 0.1),
        character='Pixel'
    )

    # Command it to move somewhere
    bot.move_to_point(10, 5, -5)

    print("[Test] NaviBot spawned")
    return bot
