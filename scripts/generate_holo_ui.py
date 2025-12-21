import os
import math
from PIL import Image, ImageDraw, ImageFilter

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_glow(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))

def draw_health_ring(draw, center, radius, width, color):
    # Draw background ring (dim)
    draw.arc(
        [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
        start=135, end=405, fill=(color[0], color[1], color[2], 50), width=width
    )
    # Draw active segment (bright) - representing full health initially
    draw.arc(
        [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
        start=135, end=405, fill=color, width=width
    )

def draw_ammo_counter(draw, center, radius, width, color):
    # Segmented ammo ring
    segments = 30
    angle_per_seg = 270 / segments
    start_angle = 135
    
    for i in range(segments):
        a1 = start_angle + (i * angle_per_seg)
        a2 = a1 + (angle_per_seg - 2) # 2 degree gap
        draw.arc(
            [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
            start=a1, end=a2, fill=color, width=width
        )

def draw_radar_grid(draw, center, radius, color):
    # Concentric circles
    for r in range(radius // 4, radius + 1, radius // 4):
        draw.ellipse(
            [center[0]-r, center[1]-r, center[0]+r, center[1]+r],
            outline=color, width=1
        )
    
    # Cross lines
    draw.line([center[0]-radius, center[1], center[0]+radius, center[1]], fill=color, width=1)
    draw.line([center[0], center[1]-radius, center[0], center[1]+radius], fill=color, width=1)
    
    # Scanning line (visual only)
    draw.line([center[0], center[1], center[0]+radius*0.7, center[1]-radius*0.7], fill=color, width=2)

def draw_crosshair(draw, center, size, color):
    # Tech crosshair
    l = size // 2
    draw.ellipse([center[0]-4, center[1]-4, center[0]+4, center[1]+4], outline=color, width=2)
    draw.line([center[0]-l, center[1], center[0]-8, center[1]], fill=color, width=2)
    draw.line([center[0]+8, center[1], center[0]+l, center[1]], fill=color, width=2)
    draw.line([center[0], center[1]-l, center[0], center[1]-8], fill=color, width=2)
    draw.line([center[0], center[1]+8, center[0], center[1]+l], fill=color, width=2)

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/textures/apex'))
    ensure_dir(output_dir)
    print(f"Generating holographic UI in {output_dir}...")

    # Atlas size: 1024x1024
    # We will divide it into quadrants for simplicity in UV mapping
    # Top-Left: Health/Status Ring
    # Top-Right: Ammo/Weapon Info
    # Bottom-Left: Radar
    # Bottom-Right: Crosshair/Misc
    
    width = 1024
    height = 1024
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cyan = (0, 255, 255, 255)
    orange = (255, 165, 0, 255)
    red = (255, 50, 50, 255)
    
    # 1. Health Ring (Top-Left)
    # Center at 256, 256
    print("Drawing Health Ring...")
    draw_health_ring(draw, (256, 256), 200, 20, cyan)
    # Add some tech text decoration
    draw.text((256-40, 256-10), "VITALS", fill=cyan)
    
    # 2. Ammo Counter (Top-Right)
    # Center at 768, 256
    print("Drawing Ammo Counter...")
    draw_ammo_counter(draw, (768, 256), 200, 15, orange)
    draw.text((768-30, 256-10), "AMMO", fill=orange)

    # 3. Radar (Bottom-Left)
    # Center at 256, 768
    print("Drawing Radar...")
    draw_radar_grid(draw, (256, 768), 200, (0, 255, 100, 200))
    
    # 4. Crosshair & Misc (Bottom-Right)
    # Center at 768, 768
    print("Drawing Crosshair...")
    draw_crosshair(draw, (768, 768), 100, red)
    
    # Apply a slight glow to everything
    # We do this by compositing a blurred version
    glow_layer = create_glow(img, radius=5)
    final_img = Image.alpha_composite(Image.new('RGBA', (width, height), (0,0,0,0)), glow_layer)
    final_img = Image.alpha_composite(final_img, img)
    
    final_img.save(os.path.join(output_dir, 'holo_atlas.png'))
    print("Done! Saved holo_atlas.png")

if __name__ == '__main__':
    main()
