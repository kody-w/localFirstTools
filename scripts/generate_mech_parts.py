import os
import math
import random

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class OBJWriter:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.vertex_offset = 1

    def add_cube(self, x, y, z, w, h, d):
        # Simple cube vertices
        vs = [
            (x-w/2, y-h/2, z-d/2), (x+w/2, y-h/2, z-d/2), (x+w/2, y+h/2, z-d/2), (x-w/2, y+h/2, z-d/2), # Front
            (x-w/2, y-h/2, z+d/2), (x+w/2, y-h/2, z+d/2), (x+w/2, y+h/2, z+d/2), (x-w/2, y+h/2, z+d/2)  # Back
        ]
        start = len(self.vertices) + 1
        self.vertices.extend(vs)
        
        # Faces (1-based indexing)
        # Front, Back, Left, Right, Top, Bottom
        indices = [
            (0,1,2,3), (5,4,7,6), (4,0,3,7), (1,5,6,2), (3,2,6,7), (4,5,1,0)
        ]
        for i in indices:
            self.faces.append([start + idx for idx in i])

    def add_pyramid(self, x, y, z, w, h, d):
        # Base
        vs = [
            (x-w/2, y-h/2, z-d/2), (x+w/2, y-h/2, z-d/2), (x+w/2, y-h/2, z+d/2), (x-w/2, y-h/2, z+d/2), # Base
            (x, y+h/2, z) # Tip
        ]
        start = len(self.vertices) + 1
        self.vertices.extend(vs)
        
        # Base face
        self.faces.append([start, start+1, start+2, start+3])
        # Side faces
        self.faces.append([start, start+4, start+1])
        self.faces.append([start+1, start+4, start+2])
        self.faces.append([start+2, start+4, start+3])
        self.faces.append([start+3, start+4, start])

    def save(self, filepath):
        with open(filepath, 'w') as f:
            f.write(f"# Generated Mech Part\n")
            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for face in self.faces:
                f.write("f " + " ".join(map(str, face)) + "\n")

def generate_torso(type_name):
    writer = OBJWriter()
    if type_name == 'light':
        # Aerodynamic, sleek torso
        writer.add_cube(0, 0, 0, 0.4, 0.5, 0.3)
        writer.add_pyramid(0, 0.35, 0, 0.3, 0.3, 0.2) # Top cowl
        writer.add_cube(0, -0.1, -0.2, 0.2, 0.3, 0.1) # Jetpack
    elif type_name == 'heavy':
        # Bulky, armored torso
        writer.add_cube(0, 0, 0, 0.8, 0.7, 0.6)
        writer.add_cube(0.3, 0.1, 0, 0.3, 0.5, 0.4) # Shoulder pad L
        writer.add_cube(-0.3, 0.1, 0, 0.3, 0.5, 0.4) # Shoulder pad R
        writer.add_cube(0, 0, -0.35, 0.5, 0.5, 0.2) # Back armor
    else: # Standard
        writer.add_cube(0, 0, 0, 0.5, 0.6, 0.4)
        writer.add_cube(0, 0.2, -0.25, 0.3, 0.4, 0.1) # Backpack
    return writer

def generate_leg_upper(type_name):
    writer = OBJWriter()
    if type_name == 'light':
        writer.add_cube(0, -0.2, 0, 0.1, 0.4, 0.1) # Thigh
    elif type_name == 'heavy':
        writer.add_cube(0, -0.25, 0, 0.25, 0.5, 0.25) # Thigh
    else: # Standard
        writer.add_cube(0, -0.2, 0, 0.15, 0.4, 0.15)
    return writer

def generate_leg_lower(type_name):
    writer = OBJWriter()
    if type_name == 'light':
        writer.add_cube(0, -0.2, -0.1, 0.08, 0.4, 0.08) # Shin
        writer.add_cube(0, -0.4, 0.05, 0.12, 0.05, 0.2) # Foot
    elif type_name == 'heavy':
        writer.add_cube(0, -0.2, 0, 0.3, 0.4, 0.3) # Shin
        writer.add_cube(0, -0.45, 0, 0.4, 0.1, 0.5) # Foot
    else: # Standard
        writer.add_cube(0, -0.2, 0, 0.12, 0.4, 0.12)
        writer.add_cube(0, -0.4, 0.05, 0.15, 0.08, 0.25) # Foot
    return writer

def generate_head(type_name):
    writer = OBJWriter()
    if type_name == 'light':
        # Sensor array, single eye
        writer.add_cube(0, 0, 0, 0.2, 0.15, 0.2)
        writer.add_cube(0, 0, 0.12, 0.05, 0.05, 0.05) # Eye
        writer.add_cube(0, 0.1, -0.05, 0.02, 0.2, 0.02) # Antenna
    elif type_name == 'heavy':
        # Dome, armored
        writer.add_cube(0, 0, 0, 0.3, 0.25, 0.3)
        writer.add_cube(0, 0, 0.16, 0.2, 0.05, 0.02) # Visor slit
    else: # Standard
        writer.add_cube(0, 0, 0, 0.25, 0.25, 0.25)
        writer.add_cube(0.08, 0, 0.13, 0.05, 0.05, 0.02) # Eye L
        writer.add_cube(-0.08, 0, 0.13, 0.05, 0.05, 0.02) # Eye R
    return writer

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/models/apex/parts'))
    ensure_dir(output_dir)
    print(f"Generating mech parts in {output_dir}...")

    types = ['light', 'standard', 'heavy']
    
    for t in types:
        print(f"Generating {t} set...")
        generate_torso(t).save(os.path.join(output_dir, f'torso_{t}.obj'))
        generate_leg_upper(t).save(os.path.join(output_dir, f'leg_upper_{t}.obj'))
        generate_leg_lower(t).save(os.path.join(output_dir, f'leg_lower_{t}.obj'))
        generate_head(t).save(os.path.join(output_dir, f'head_{t}.obj'))

    print("Done!")

if __name__ == '__main__':
    main()
