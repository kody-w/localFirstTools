import os
import math

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.faces = [] # (v_idx, uv_idx, n_idx) tuples
        self.vertex_offset = 1 # OBJ is 1-indexed

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))

    def add_normal(self, x, y, z):
        self.normals.append((x, y, z))
    
    def add_uv(self, u, v):
        self.uvs.append((u, v))

    def add_face(self, indices):
        # indices is list of (v_idx, uv_idx, n_idx) relative to current offset
        # We convert to absolute indices
        absolute_indices = []
        for v, uv, n in indices:
            absolute_indices.append((
                self.vertex_offset + v,
                self.vertex_offset + uv,
                self.vertex_offset + n
            ))
        self.faces.append(absolute_indices)

    def commit_geometry(self, num_new_vertices, num_new_uvs, num_new_normals):
        self.vertex_offset += num_new_vertices

    def add_cube(self, width, height, depth, px, py, pz, rx=0, ry=0, rz=0):
        w, h, d = width/2, height/2, depth/2
        
        # Local vertices
        local_verts = [
            (-w, -h, d), (w, -h, d), (w, h, d), (-w, h, d), # Front
            (-w, -h, -d), (-w, h, -d), (w, h, -d), (w, -h, -d), # Back
            (-w, h, -d), (-w, h, d), (w, h, d), (w, h, -d), # Top
            (-w, -h, -d), (w, -h, -d), (w, -h, d), (-w, -h, d), # Bottom
            (w, -h, -d), (w, h, -d), (w, h, d), (w, -h, d), # Right
            (-w, -h, -d), (-w, -h, d), (-w, h, d), (-w, h, -d) # Left
        ]

        # Transform and add vertices
        for x, y, z in local_verts:
            # Rotate
            # X-axis
            y1 = y * math.cos(rx) - z * math.sin(rx)
            z1 = y * math.sin(rx) + z * math.cos(rx)
            y, z = y1, z1
            # Y-axis
            x1 = x * math.cos(ry) + z * math.sin(ry)
            z1 = -x * math.sin(ry) + z * math.cos(ry)
            x, z = x1, z1
            # Z-axis
            x1 = x * math.cos(rz) - y * math.sin(rz)
            y1 = x * math.sin(rz) + y * math.cos(rz)
            x, y = x1, y1
            
            self.add_vertex(x + px, y + py, z + pz)

        # Normals (simplified, one per face type)
        normals = [
            (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)
        ]
        for n in normals:
            self.add_normal(*n)

        # UVs (dummy)
        self.add_uv(0, 0)
        self.add_uv(1, 0)
        self.add_uv(1, 1)
        self.add_uv(0, 1)

        # Faces (quads)
        # v_idx relative to start of this cube (0-23)
        # n_idx relative to start of this cube (0-5)
        # uv_idx relative to start of this cube (0-3)
        
        faces_indices = [
            [0, 1, 2, 3], # Front
            [7, 6, 5, 4], # Back
            [8, 9, 10, 11], # Top
            [12, 13, 14, 15], # Bottom
            [16, 17, 18, 19], # Right
            [20, 21, 22, 23]  # Left
        ]

        for i, face in enumerate(faces_indices):
            face_data = []
            for j, v_idx in enumerate(face):
                # Map to UV corners: 0->(0,0), 1->(1,0), 2->(1,1), 3->(0,1)
                face_data.append((v_idx, j, i)) 
            self.add_face(face_data)

        self.commit_geometry(24, 4, 6)

    def add_cone(self, radius, height, segments, px, py, pz, rx=0, ry=0, rz=0):
        # Base center at (0, -height/2, 0), Tip at (0, height/2, 0)
        
        # Tip vertex
        tip_idx = 0
        local_verts = [(0, height/2, 0)]
        
        # Base vertices
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius
            local_verts.append((x, -height/2, z))
            
        # Transform and add
        for x, y, z in local_verts:
            # Rotate
            y1 = y * math.cos(rx) - z * math.sin(rx)
            z1 = y * math.sin(rx) + z * math.cos(rx)
            y, z = y1, z1
            x1 = x * math.cos(ry) + z * math.sin(ry)
            z1 = -x * math.sin(ry) + z * math.cos(ry)
            x, z = x1, z1
            x1 = x * math.cos(rz) - y * math.sin(rz)
            y1 = x * math.sin(rz) + y * math.cos(rz)
            x, y = x1, y1
            self.add_vertex(x + px, y + py, z + pz)
            
        # Normals (simplified: up, down, side)
        self.add_normal(0, 1, 0)
        self.add_normal(0, -1, 0)
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            self.add_normal(math.cos(angle), 0, math.sin(angle))
            
        # UVs
        self.add_uv(0.5, 1) # Tip
        for i in range(segments):
            u = i / segments
            self.add_uv(u, 0)
            
        # Faces
        # Sides
        for i in range(segments):
            next_i = (i + 1) % segments
            # Triangle: Tip, Base[i], Base[next_i]
            # Normals: Tip(0), Side(2+i), Side(2+next_i)
            self.add_face([
                (0, 0, 2+i),
                (1+i, 1+i, 2+i),
                (1+next_i, 1+next_i, 2+next_i)
            ])
            
        # Base Cap
        base_center_idx = len(local_verts) # We didn't add a center vert, let's just fan it
        # Actually, let's just make a polygon for the base
        base_face = []
        for i in range(segments):
            # Reverse order for downward facing normal
            idx = segments - 1 - i
            base_face.append((1+idx, 1+idx, 1))
        self.add_face(base_face)
        
        self.commit_geometry(len(local_verts), len(local_verts), 2 + segments)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write("# Apex Protocol Model\n")
            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for vt in self.uvs:
                f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
            for vn in self.normals:
                f.write(f"vn {vn[0]:.4f} {vn[1]:.4f} {vn[2]:.4f}\n")
            
            for face in self.faces:
                f.write("f")
                for v, uv, n in face:
                    # OBJ indices are 1-based, which we handled in add_face
                    f.write(f" {v}/{uv}/{n}")
                f.write("\n")

def generate_grunt(output_dir):
    builder = MeshBuilder()
    s = 1.0
    body_height = s
    
    # Body
    builder.add_cube(s * 1.2, s * 2, s * 0.8, 0, body_height, 0)
    
    # Backpack (Methane Tank)
    # ConeGeometry(s * 0.6, s * 1.2, 4)
    # position.set(0, bodyHeight + s * 0.2, -s * 0.5)
    # rotation.x = -0.5, rotation.y = PI/4
    builder.add_cone(s * 0.6, s * 1.2, 4, 0, body_height + s * 0.2, -s * 0.5, -0.5, math.pi/4, 0)
    
    # Head (Sphere approximated as Cube for OBJ simplicity or low-poly style)
    # SphereGeometry(s * 0.4) -> Cube(s*0.7)
    builder.add_cube(s * 0.7, s * 0.7, s * 0.7, 0, body_height + s * 1.2, 0)
    
    builder.save(os.path.join(output_dir, 'grunt.obj'))

def generate_rusher(output_dir):
    builder = MeshBuilder()
    s = 1.0
    body_height = s * 0.9
    
    # Body (Cone)
    # ConeGeometry(s * 0.5, s * 1.8, 6)
    builder.add_cone(s * 0.5, s * 1.8, 6, 0, body_height, 0)
    
    # Head (Cone)
    # ConeGeometry(s * 0.3, s * 0.6, 4)
    # position.y = bodyHeight + s * 1.2
    # rotation.x = PI
    builder.add_cone(s * 0.3, s * 0.6, 4, 0, body_height + s * 1.2, 0, math.pi, 0, 0)
    
    # Blade Arms
    # BoxGeometry(s * 0.1, s * 1.2, s * 0.4)
    # position.set(side * s * 0.5, bodyHeight * 0.6, 0)
    # rotation.x = PI * 0.2
    for side in [-1, 1]:
        builder.add_cube(s * 0.1, s * 1.2, s * 0.4, side * s * 0.5, body_height * 0.6, 0, math.pi * 0.2, 0, 0)

    builder.save(os.path.join(output_dir, 'rusher.obj'))

def generate_tank(output_dir):
    builder = MeshBuilder()
    s = 1.0
    body_height = s * 0.9
    
    # Body (Box)
    # BoxGeometry(s * 1.6, s * 1.8, s * 1.2)
    builder.add_cube(s * 1.6, s * 1.8, s * 1.2, 0, body_height, 0)
    
    # Head (Box)
    # BoxGeometry(s * 0.6, s * 0.5, s * 0.6)
    builder.add_cube(s * 0.6, s * 0.5, s * 0.6, 0, body_height + s * 1.2, 0)
    
    # Shoulders
    # BoxGeometry(s * 0.8, s * 0.8, s * 0.8)
    for side in [-1, 1]:
        builder.add_cube(s * 0.8, s * 0.8, s * 0.8, side * s * 1.0, body_height * 0.5, 0)
        
    # Cannon
    # CylinderGeometry(s * 0.2, s * 0.25, s * 1.5, 8) -> Approximated as long box or cone
    # Let's use a Cone for the cannon barrel
    builder.add_cone(s * 0.25, s * 1.5, 8, 0, body_height + s * 0.8, -s * 0.4, math.pi * 0.2 + math.pi/2, 0, 0) # Rotated to point back/up

    builder.save(os.path.join(output_dir, 'tank.obj'))

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/models/apex'))
    ensure_dir(output_dir)
    print(f"Generating models in {output_dir}...")
    
    generate_grunt(output_dir)
    generate_rusher(output_dir)
    generate_tank(output_dir)
    
    print("Done!")

if __name__ == '__main__':
    main()
