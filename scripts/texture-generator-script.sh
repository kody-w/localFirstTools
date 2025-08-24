#!/bin/bash

# Create directory structure
echo "Creating directory structure..."
mkdir -p textures
mkdir -p textures/skybox
mkdir -p models
mkdir -p audio

# Function to create a procedural texture using ImageMagick
create_texture() {
    local filename=$1
    local pattern=$2
    local color1=$3
    local color2=$4
    local size=$5
    local extra_params=$6
    
    echo "Generating $filename..."
    
    case $pattern in
        "scales")
            # Snake scales pattern
            convert -size $size xc:$color1 \
                -fill $color2 \
                -draw "circle 32,32 32,48" \
                -draw "circle 96,32 96,48" \
                -draw "circle 160,32 160,48" \
                -draw "circle 224,32 224,48" \
                -draw "circle 64,96 64,112" \
                -draw "circle 128,96 128,112" \
                -draw "circle 192,96 192,112" \
                -draw "circle 32,160 32,176" \
                -draw "circle 96,160 96,176" \
                -draw "circle 160,160 160,176" \
                -draw "circle 224,160 224,176" \
                -draw "circle 64,224 64,240" \
                -draw "circle 128,224 128,240" \
                -draw "circle 192,224 192,240" \
                -tile ${size} \
                -blur 0x1 \
                -modulate 100,120,100 \
                -emboss 2 \
                $filename
            ;;
        "plasma")
            # Plasma pattern for organic textures
            convert -size $size plasma:$color1-$color2 \
                $extra_params \
                $filename
            ;;
        "granite")
            # Granite pattern for stone/wall textures
            convert -size $size granite:$color1 \
                -colorspace RGB \
                -modulate 100,50,100 \
                $extra_params \
                $filename
            ;;
        "checkerboard")
            # Checkerboard pattern for ground
            convert -size $size pattern:checkerboard \
                -colorspace RGB \
                -fill $color1 -opaque white \
                -fill $color2 -opaque black \
                $extra_params \
                $filename
            ;;
        "gradient")
            # Gradient pattern
            convert -size $size gradient:$color1-$color2 \
                $extra_params \
                $filename
            ;;
        "noise")
            # Noise pattern for rough surfaces
            convert -size $size xc:$color1 \
                +noise Random \
                -virtual-pixel tile \
                -blur 0x2 \
                -colorspace RGB \
                -modulate 100,80,100 \
                $extra_params \
                $filename
            ;;
        "brick")
            # Brick pattern for walls
            convert -size 128x64 xc:$color1 \
                -fill $color2 \
                -draw "rectangle 0,0 126,30" \
                -draw "rectangle 0,33 62,62" \
                -draw "rectangle 65,33 126,62" \
                -tile ${size} \
                -emboss 1 \
                $filename
            ;;
    esac
}

# Generate snake texture (green scales)
create_texture "textures/snake-scales.jpg" "scales" "#2d5016" "#4a7c2e" "512x512" "-quality 90"

# Generate alternative snake skins
create_texture "textures/snake-scales-blue.jpg" "scales" "#162550" "#2e4a7c" "512x512" "-quality 90"
create_texture "textures/snake-scales-red.jpg" "scales" "#501616" "#7c2e2e" "512x512" "-quality 90"
create_texture "textures/snake-scales-gold.jpg" "scales" "#504016" "#7c6a2e" "512x512" "-quality 90"

# Generate food textures (apple-like)
echo "Generating apple texture..."
convert -size 256x256 radial-gradient:"#ff6b6b"-"#cc2222" \
    -distort SRT 0 \
    -modulate 110,130,100 \
    -blur 0x1 \
    "textures/apple.png"

# Generate alternative food textures
convert -size 256x256 radial-gradient:"#6bff6b"-"#22cc22" \
    -distort SRT 0 \
    -modulate 110,130,100 \
    "textures/food-green.png"

convert -size 256x256 radial-gradient:"#ffeb3b"-"#ffc107" \
    -distort SRT 0 \
    -modulate 110,130,100 \
    "textures/food-gold.png"

# Generate ground/grid texture
create_texture "textures/grid.png" "checkerboard" "#1a1a1a" "#2d2d2d" "512x512" "-blur 0x0.5"

# Generate grass texture
create_texture "textures/grass.jpg" "noise" "#2d4a2d" "#4a7c4a" "512x512" "-quality 90"

# Generate stone floor texture
create_texture "textures/stone-floor.jpg" "granite" "#404040" "#606060" "512x512" "-quality 90 -emboss 1"

# Generate wall/brick texture
create_texture "textures/brick.jpg" "brick" "#8b4513" "#a0522d" "512x512" "-quality 90"

# Generate metal texture
create_texture "textures/metal.jpg" "granite" "#303030" "#505050" "512x512" "-quality 90 -blur 0x1 -modulate 100,0,100"

# Generate wood texture
echo "Generating wood texture..."
convert -size 512x128 gradient:"#654321"-"#8b6914" \
    -function Sinusoid 4,90 \
    -virtual-pixel tile \
    -distort SRT 0 \
    -resize 512x512! \
    -blur 0x0.5 \
    "textures/wood.jpg"

# Generate power-up textures
echo "Generating power-up textures..."
convert -size 256x256 radial-gradient:"#ffff00"-"#ff8800" \
    -modulate 110,150,100 \
    "textures/powerup-speed.png"

convert -size 256x256 radial-gradient:"#00ffff"-"#0088ff" \
    -modulate 110,150,100 \
    "textures/powerup-slow.png"

convert -size 256x256 radial-gradient:"#ff00ff"-"#8800ff" \
    -modulate 110,150,100 \
    "textures/powerup-invincible.png"

# Generate skybox textures (simple gradients for each face)
echo "Generating skybox textures..."
# Positive X (right)
create_texture "textures/skybox/px.jpg" "gradient" "#1e3c72" "#2a5298" "1024x1024" "-quality 90"
# Negative X (left)
create_texture "textures/skybox/nx.jpg" "gradient" "#2a5298" "#1e3c72" "1024x1024" "-quality 90"
# Positive Y (top)
create_texture "textures/skybox/py.jpg" "gradient" "#87ceeb" "#4682b4" "1024x1024" "-quality 90"
# Negative Y (bottom)
create_texture "textures/skybox/ny.jpg" "gradient" "#1a1a2e" "#16213e" "1024x1024" "-quality 90"
# Positive Z (front)
create_texture "textures/skybox/pz.jpg" "gradient" "#1e3c72" "#2a5298" "1024x1024" "-quality 90"
# Negative Z (back)
create_texture "textures/skybox/nz.jpg" "gradient" "#2a5298" "#1e3c72" "1024x1024" "-quality 90"

# Generate particle textures
echo "Generating particle textures..."
convert -size 64x64 radial-gradient:"white"-"transparent" \
    "textures/particle.png"

convert -size 64x64 radial-gradient:"#ffff00"-"transparent" \
    "textures/particle-star.png"

# Generate normal maps for some textures
echo "Generating normal maps..."
convert textures/snake-scales.jpg -colorspace Gray \
    -blur 0x1 \
    -emboss 2 \
    -normalize \
    -evaluate multiply 0.5 \
    -evaluate add 50% \
    "textures/snake-scales-normal.jpg"

convert textures/brick.jpg -colorspace Gray \
    -blur 0x1 \
    -emboss 2 \
    -normalize \
    -evaluate multiply 0.5 \
    -evaluate add 50% \
    "textures/brick-normal.jpg"

# Create a simple README for the textures
cat > textures/README.md << 'EOF'
# 3D Snake Game Textures

This directory contains procedurally generated textures for the 3D Snake Game.

## Texture List

### Snake Textures
- `snake-scales.jpg` - Default green snake skin
- `snake-scales-blue.jpg` - Blue snake skin variant
- `snake-scales-red.jpg` - Red snake skin variant
- `snake-scales-gold.jpg` - Gold snake skin variant
- `snake-scales-normal.jpg` - Normal map for snake scales

### Food Textures
- `apple.png` - Red apple food item
- `food-green.png` - Green food variant
- `food-gold.png` - Golden food variant

### Environment Textures
- `grid.png` - Grid pattern for game board
- `grass.jpg` - Grass texture
- `stone-floor.jpg` - Stone floor texture
- `brick.jpg` - Brick wall texture
- `brick-normal.jpg` - Normal map for bricks
- `metal.jpg` - Metal surface texture
- `wood.jpg` - Wood texture

### Power-up Textures
- `powerup-speed.png` - Speed boost power-up
- `powerup-slow.png` - Slow-down power-up
- `powerup-invincible.png` - Invincibility power-up

### Skybox Textures
- `skybox/px.jpg` - Positive X face
- `skybox/nx.jpg` - Negative X face
- `skybox/py.jpg` - Positive Y face
- `skybox/ny.jpg` - Negative Y face
- `skybox/pz.jpg` - Positive Z face
- `skybox/nz.jpg` - Negative Z face

### Particle Effects
- `particle.png` - Basic particle
- `particle-star.png` - Star particle

## Usage

These textures are designed to be loaded via Three.js TextureLoader:

```javascript
const textureLoader = new THREE.TextureLoader();
const snakeTexture = textureLoader.load('textures/snake-scales.jpg');
```

For GitHub hosting, use raw URLs:
```javascript
const ASSET_URL = 'https://raw.githubusercontent.com/USERNAME/REPO/main';
const texture = textureLoader.load(`${ASSET_URL}/textures/snake-scales.jpg`);
```

## Generation

These textures were procedurally generated using ImageMagick.
To regenerate, run: `bash generate-textures.sh`
EOF

# Create main README
cat > README.md << 'EOF'
# 3D Snake Game Assets

A collection of procedurally generated textures and assets for a Three.js-based 3D Snake Game.

## Repository Structure

```
.
├── textures/           # All game textures
│   ├── skybox/        # Skybox cube map textures
│   └── ...           # Various game textures
├── models/            # 3D models (placeholder)
├── audio/             # Sound effects (placeholder)
└── generate-textures.sh  # Script to regenerate textures
```

## Setup

1. Clone this repository
2. Ensure ImageMagick is installed: `sudo apt-get install imagemagick` (Linux) or `brew install imagemagick` (Mac)
3. Run `bash generate-textures.sh` to generate all textures
4. Push to GitHub to use as a CDN

## Using as a CDN

Once pushed to GitHub, access textures via:
```
https://raw.githubusercontent.com/[YOUR-USERNAME]/[REPO-NAME]/main/textures/[TEXTURE-NAME]
```

## Game Repository

The main game code is available at: [Your Game Repo URL]

## License

MIT License - Feel free to use these assets in your projects!
EOF

echo "✅ Texture generation complete!"
echo ""
echo "📁 Generated files:"
ls -la textures/
echo ""
echo "📝 Next steps:"
echo "1. Review the generated textures in the 'textures' directory"
echo "2. Initialize git: git init"
echo "3. Add files: git add ."
echo "4. Commit: git commit -m 'Add procedurally generated textures'"
echo "5. Create a GitHub repo and push"
echo "6. Update the game code with your GitHub username and repo name"
echo ""
echo "Note: Requires ImageMagick to be installed."
echo "Install with: sudo apt-get install imagemagick (Linux) or brew install imagemagick (Mac)"