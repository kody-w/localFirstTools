import os
import random
import math

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Pillow not installed. Please install it to generate textures: pip install Pillow")
    exit(1)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_noise_texture(width, height, color1, color2, scale=1):
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    # Parse hex colors
    c1 = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    c2 = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if random.random() < 0.5:
                # Blend based on random alpha
                alpha = random.random() * 0.5
                r = int(c2[0] * alpha + c1[0] * (1 - alpha))
                g = int(c2[1] * alpha + c1[1] * (1 - alpha))
                b = int(c2[2] * alpha + c1[2] * (1 - alpha))
                pixels[x, y] = (r, g, b)
                
    return img

def create_grid_texture(width, height, color, line_color, grid_size=32):
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Draw grid
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=2)
    
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=2)
        
    # Add tech details
    for i in range(20):
        gx = random.randint(0, (width // grid_size) - 1) * grid_size
        gy = random.randint(0, (height // grid_size) - 1) * grid_size
        
        # Draw a filled rect inside the grid cell
        draw.rectangle([gx + 4, gy + 4, gx + grid_size - 4, gy + grid_size - 4], fill=line_color)
        
    return img

def create_hex_texture(width, height, color, hex_color, scale=20):
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    r = scale
    h = r * math.sqrt(3)
    
    def draw_hex(cx, cy, radius):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            px = cx + radius * math.cos(angle_rad)
            py = cy + radius * math.sin(angle_rad)
            points.append((px, py))
        draw.line(points + [points[0]], fill=hex_color, width=1)

    # Draw hex grid
    for y in range(int(-h), int(height + h), int(h)):
        for x in range(int(-r), int(width + r), int(3 * r)):
            draw_hex(x, y, r)
            draw_hex(x + 1.5 * r, y + h / 2, r)
            
    return img

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/textures/apex'))
    ensure_dir(output_dir)
    print(f"Generating textures in {output_dir}...")

    # Metal Plate (Noise)
    print("Generating metal_plate.png...")
    metal = create_noise_texture(512, 512, '#444444', '#666666', 0.5)
    metal.save(os.path.join(output_dir, 'metal_plate.png'))

    # Floor (Grid)
    print("Generating floor_grid.png...")
    floor = create_grid_texture(512, 512, '#111111', '#00ffff', 64)
    floor.save(os.path.join(output_dir, 'floor_grid.png'))

    # Wall (Hex)
    print("Generating wall_hex.png...")
    wall = create_hex_texture(512, 512, '#0a0a1a', '#0044ff', 30)
    wall.save(os.path.join(output_dir, 'wall_hex.png'))
    
    # Enemy Hex (White/Grey for tinting)
    print("Generating enemy_hex.png...")
    enemy_hex = create_hex_texture(256, 256, '#ffffff', '#aaaaaa', 40)
    enemy_hex.save(os.path.join(output_dir, 'enemy_hex.png'))

    print("Done!")

if __name__ == '__main__':
    main()
