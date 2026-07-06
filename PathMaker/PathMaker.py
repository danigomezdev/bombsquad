# ba_meta nomod

import struct
import json
import math
from collections import defaultdict
from typing import List, Tuple, Dict, Set

COB_FILE_ID = 13466

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Vector3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
    def to_tuple(self):
        return (self.x, self.y, self.z)
    
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

class Face:
    def __init__(self, v1_idx: int, v2_idx: int, v3_idx: int, normal: Vector3):
        self.indices = [v1_idx, v2_idx, v3_idx]
        self.normal = normal
        self.center = None
        self.is_walkable = False
        self.neighbors = []
    
    def compute_center(self, vertices: List[Vector3]):
        v1, v2, v3 = [vertices[i] for i in self.indices]
        self.center = (v1 + v2 + v3) / 3.0
    
    def check_walkable(self, max_slope: float = 0.7):
        self.is_walkable = self.normal.y > max_slope

class COBMesh:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.vertices: List[Vector3] = []
        self.faces: List[Face] = []
        self.load()
    
    def load(self):
        with open(self.filepath, 'rb') as f:
            magic = struct.unpack('I', f.read(4))[0]
            if magic != COB_FILE_ID:
                raise ValueError(f"Invalid COB file. Expected magic {COB_FILE_ID}, got {magic}")
            
            vertex_count = struct.unpack('I', f.read(4))[0]
            face_count = struct.unpack('I', f.read(4))[0]
            
            print(f"Loading COB: {vertex_count} vertices, {face_count} faces")
            
            for _ in range(vertex_count):
                x, y, z = struct.unpack('fff', f.read(12))
                self.vertices.append(Vector3(x, y, z))
            
            face_indices = []
            for _ in range(face_count):
                i1, i2, i3 = struct.unpack('III', f.read(12))
                face_indices.append((i1, i2, i3))
            
            for i in range(face_count):
                nx, ny, nz = struct.unpack('fff', f.read(12))
                normal = Vector3(nx, ny, nz)
                indices = face_indices[i]
                face = Face(indices[0], indices[1], indices[2], normal)
                face.compute_center(self.vertices)
                face.check_walkable()
                self.faces.append(face)

class NavigationGuide:
    def __init__(self, mesh: COBMesh):
        self.mesh = mesh
        self.nav_nodes: List[Dict] = []
        self.edges: List[Tuple[int, int, float]] = []
        self.grid_size = 1.0
        self.spatial_grid: Dict[Tuple[int, int, int], List[int]] = defaultdict(list)
    
    def generate(self):
        print("Generating navigation guide...")
        
        walkable_faces = [i for i, face in enumerate(self.mesh.faces) if face.is_walkable]
        print(f"Found {len(walkable_faces)} walkable faces out of {len(self.mesh.faces)} total")
        
        for face_idx in walkable_faces:
            face = self.mesh.faces[face_idx]
            node = {
                'id': len(self.nav_nodes),
                'position': face.center.to_tuple(),
                'normal': face.normal.to_tuple(),
                'face_idx': face_idx,
                'neighbors': []
            }
            self.nav_nodes.append(node)
            
            grid_key = self._get_grid_key(face.center)
            self.spatial_grid[grid_key].append(node['id'])
        
        self._connect_neighbors()
        
        for node in self.nav_nodes:
            node_pos = Vector3(*node['position'])
            for neighbor_id in node['neighbors']:
                neighbor_pos = Vector3(*self.nav_nodes[neighbor_id]['position'])
                distance = node_pos.distance_to(neighbor_pos)
                self.edges.append((node['id'], neighbor_id, distance))
        
        print(f"Generated {len(self.nav_nodes)} navigation nodes with {len(self.edges)} edges")
    
    def _get_grid_key(self, pos: Vector3) -> Tuple[int, int, int]:
        return (
            int(pos.x / self.grid_size),
            int(pos.y / self.grid_size),
            int(pos.z / self.grid_size)
        )
    
    def _connect_neighbors(self):
        print("Connecting navigation nodes...")
        
        vertex_to_faces: Dict[int, List[int]] = defaultdict(list)
        for node in self.nav_nodes:
            face_idx = node['face_idx']
            face = self.mesh.faces[face_idx]
            for vertex_idx in face.indices:
                vertex_to_faces[vertex_idx].append(node['id'])
        
        for node in self.nav_nodes:
            face = self.mesh.faces[node['face_idx']]
            connected = set()
            
            for vertex_idx in face.indices:
                for neighbor_node_id in vertex_to_faces[vertex_idx]:
                    if neighbor_node_id != node['id'] and neighbor_node_id not in connected:
                        node_pos = Vector3(*node['position'])
                        neighbor_pos = Vector3(*self.nav_nodes[neighbor_node_id]['position'])
                        distance = node_pos.distance_to(neighbor_pos)
                        
                        if distance < 5.0:
                            node['neighbors'].append(neighbor_node_id)
                            connected.add(neighbor_node_id)
    
    def compute_bounds(self) -> Dict:
        if not self.mesh.vertices:
            return {'min': (0, 0, 0), 'max': (0, 0, 0)}
        
        min_x = min(v.x for v in self.mesh.vertices)
        max_x = max(v.x for v in self.mesh.vertices)
        min_y = min(v.y for v in self.mesh.vertices)
        max_y = max(v.y for v in self.mesh.vertices)
        min_z = min(v.z for v in self.mesh.vertices)
        max_z = max(v.z for v in self.mesh.vertices)
        
        return {
            'min': (min_x, min_y, min_z),
            'max': (max_x, max_y, max_z),
            'center': ((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2),
            'size': (max_x - min_x, max_y - min_y, max_z - min_z)
        }
    
    def save_json(self, output_path: str):
        bounds = self.compute_bounds()
        
        data = {
            'version': '1.0',
            'source_file': self.mesh.filepath,
            'bounds': bounds,
            'node_count': len(self.nav_nodes),
            'edge_count': len(self.edges),
            'nodes': self.nav_nodes,
            'edges': [[e[0], e[1], round(e[2], 3)] for e in self.edges],
            'metadata': {
                'total_faces': len(self.mesh.faces),
                'walkable_faces': len(self.nav_nodes),
                'grid_size': self.grid_size
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Navigation guide saved to {output_path}")
    
    def save_simplified_json(self, output_path: str, max_nodes: int = 500):
        if len(self.nav_nodes) <= max_nodes:
            self.save_json(output_path)
            return
        
        print(f"Simplifying navigation mesh from {len(self.nav_nodes)} to ~{max_nodes} nodes...")
        
        step = len(self.nav_nodes) // max_nodes
        simplified_nodes = self.nav_nodes[::step][:max_nodes]
        
        node_id_map = {node['id']: i for i, node in enumerate(simplified_nodes)}
        simplified_edges = []
        
        for i, node in enumerate(simplified_nodes):
            node['id'] = i
            new_neighbors = []
            for neighbor_id in node['neighbors']:
                if neighbor_id in node_id_map:
                    new_neighbors.append(node_id_map[neighbor_id])
            node['neighbors'] = new_neighbors
            
            for neighbor_id in new_neighbors:
                pos1 = Vector3(*node['position'])
                pos2 = Vector3(*simplified_nodes[neighbor_id]['position'])
                distance = pos1.distance_to(pos2)
                simplified_edges.append((i, neighbor_id, distance))
        
        bounds = self.compute_bounds()
        data = {
            'version': '1.0-simplified',
            'source_file': self.mesh.filepath,
            'bounds': bounds,
            'node_count': len(simplified_nodes),
            'edge_count': len(simplified_edges),
            'nodes': simplified_nodes,
            'edges': [[e[0], e[1], round(e[2], 3)] for e in simplified_edges],
            'metadata': {
                'original_node_count': len(self.nav_nodes),
                'simplification_ratio': len(simplified_nodes) / len(self.nav_nodes)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Simplified navigation guide saved to {output_path}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pathmaker.py <input.cob> [output.json]")
        print("Example: python pathmaker.py cragCastleLevelCollide.cob cragCastle_navguide.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.cob', '_navguide.json')
    
    try:
        mesh = COBMesh(input_file)
        
        nav_guide = NavigationGuide(mesh)
        nav_guide.generate()
        
        nav_guide.save_json(output_file)
        
        if len(nav_guide.nav_nodes) > 500:
            simplified_output = output_file.replace('.json', '_simplified.json')
            nav_guide.save_simplified_json(simplified_output, max_nodes=500)
        
        print("\n=== Navigation Guide Summary ===")
        print(f"Input: {input_file}")
        print(f"Output: {output_file}")
        print(f"Nodes: {len(nav_guide.nav_nodes)}")
        print(f"Edges: {len(nav_guide.edges)}")
        bounds = nav_guide.compute_bounds()
        print(f"Bounds: {bounds['size']}")
        print("\nNavigation guide generation complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
