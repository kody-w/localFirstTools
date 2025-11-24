#!/bin/bash

# =====================================
# GitHub Artifacts System Setup Script
# =====================================
# This script creates the complete file structure and files
# for the GitHub artifacts gallery system
# 
# Usage: bash setup-artifacts-system.sh [repository-name]
# =====================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
REPO_NAME="${1:-localFirstTools}"
GITHUB_USERNAME="${GITHUB_USERNAME:-kody-w}"
AUTHOR_NAME="${AUTHOR_NAME:-Kody Wildfeuer}"

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Create directory structure
create_directory_structure() {
    print_info "Creating directory structure for $REPO_NAME..."
    
    # Create main directories
    mkdir -p "$REPO_NAME"
    cd "$REPO_NAME"
    
    # Create subdirectories
    mkdir -p artifacts
    mkdir -p artifacts/metadata
    mkdir -p assets/images
    mkdir -p assets/styles
    mkdir -p assets/scripts
    mkdir -p docs
    
    print_success "Directory structure created!"
}

# Create README.md
create_readme() {
    print_info "Creating README.md..."
    
    cat > README.md << 'EOF'
# Local First Tools - Claude Artifacts Gallery

A collection of experimental web tools, creative coding projects, and Claude artifacts.

## 🚀 Features

- **Dynamic Gallery**: Automatically discovers and displays all HTML artifacts
- **3D Experience**: Immersive Minecraft-style 3D gallery mode
- **App Store Interface**: Browse artifacts like apps with ratings and metadata
- **GitHub Integration**: Direct integration with GitHub for artifact storage
- **Import/Export**: Full settings and data portability

## 📁 Directory Structure

```
localFirstTools/
├── index.html                      # Main gallery interface
├── artifacts/                      # All HTML artifacts
│   ├── metadata/                   # Artifact metadata JSON files
│   └── *.html                      # Individual artifacts
├── assets/                         # Shared resources
│   ├── images/
│   ├── styles/
│   └── scripts/
└── docs/                          # Documentation
```

## 🛠️ Setup

1. Clone this repository
2. Add your HTML artifacts to the `artifacts/` directory
3. Open `index.html` in a web browser
4. Or deploy to GitHub Pages for online access

## 📱 Tools Included

- **Vibe Coding Gallery**: Main gallery with classic and 3D viewing modes
- **App Store**: iOS-style interface for browsing artifacts
- **Artifact Manager**: Tool for organizing and managing artifacts
- **Sync Manager**: Import/export settings and discover artifacts from any GitHub repo

## 🔧 Adding New Artifacts

1. Save your Claude artifact HTML to the `artifacts/` directory
2. Optionally create a metadata JSON file in `artifacts/metadata/`
3. The gallery will automatically discover and display it

## 📄 Metadata Format

Create a JSON file with the same name as your artifact in `artifacts/metadata/`:

```json
{
    "id": "artifact-name",
    "name": "Artifact Display Name",
    "description": "Brief description",
    "category": "tools|games|creative|productivity|education|experimental",
    "version": "1.0.0",
    "author": "Your Name",
    "created": "2024-01-15",
    "tags": ["tag1", "tag2"],
    "claudeUrl": "https://claude.ai/chat/[conversation-id]"
}
```

## 🌐 GitHub Pages

This gallery is designed to work perfectly with GitHub Pages. Simply enable Pages in your repository settings and your gallery will be available at:

```
https://[username].github.io/[repository-name]/
```

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created by [Your Name]

---

**Note**: This is a personal creative project. All opinions and content are my own.
EOF
    
    print_success "README.md created!"
}

# Create main gallery index.html
create_main_gallery() {
    print_info "Creating main gallery (index.html)..."
    
    cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vibe Coding Gallery</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #000;
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(120, 30, 255, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 30, 120, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 10%, rgba(30, 255, 120, 0.3) 0%, transparent 50%);
            animation: drift 20s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes drift {
            0%, 100% { transform: scale(1) rotate(0deg); }
            33% { transform: scale(1.1) rotate(120deg); }
            66% { transform: scale(0.95) rotate(240deg); }
        }
        
        .header {
            padding: 60px 20px;
            text-align: center;
            position: relative;
            background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%);
        }

        .gallery-title {
            font-size: 5em;
            font-weight: 100;
            letter-spacing: 0.2em;
            margin-bottom: 20px;
            text-transform: uppercase;
            position: relative;
            display: inline-block;
        }

        @media (max-width: 768px) {
            .gallery-title {
                font-size: 3em;
                letter-spacing: 0.1em;
            }
        }

        .gallery-title::before {
            content: 'VIBE CODING';
            position: absolute;
            left: 0;
            top: 0;
            background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
            background-size: 400% 100%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 8s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .content {
            padding: 40px 20px 80px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .loading {
            text-align: center;
            padding: 100px;
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.4);
            font-weight: 200;
            letter-spacing: 0.1em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 class="gallery-title">VIBE CODING</h1>
        <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.2em;">Loading gallery system...</p>
    </div>
    
    <div class="content" id="main-content">
        <div class="loading">Initializing...</div>
    </div>

    <script>
        // This is a placeholder that will be replaced with the full gallery code
        // For now, redirect to the vibe coding gallery
        setTimeout(() => {
            window.location.href = './vibe-coding-gallery.html';
        }, 2000);
    </script>
</body>
</html>
EOF
    
    print_success "Main gallery created!"
}

# Create settings.json
create_settings_json() {
    print_info "Creating settings.json..."
    
    cat > artifacts/settings.json << EOF
{
    "version": "1.0",
    "gallery": {
        "title": "Vibe Coding Gallery",
        "description": "A collection of experimental web art, creative coding projects, and digital explorations",
        "author": "$AUTHOR_NAME"
    },
    "repository": {
        "owner": "$GITHUB_USERNAME",
        "name": "$REPO_NAME",
        "path": "artifacts",
        "branch": "main"
    },
    "features": {
        "autoDiscover": true,
        "showMetadata": true,
        "enableSearch": true,
        "enableCategories": true,
        "enable3D": true,
        "enableAppStore": true
    },
    "categories": [
        "games",
        "creative",
        "tools",
        "productivity",
        "education",
        "experimental"
    ],
    "theme": {
        "primaryColor": "#8338ec",
        "secondaryColor": "#ff006e",
        "darkMode": "auto"
    }
}
EOF
    
    print_success "settings.json created!"
}

# Create sample artifact
create_sample_artifact() {
    print_info "Creating sample artifact..."
    
    cat > artifacts/sample-artifact.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample Artifact - Claude Artifact</title>
    <meta name="description" content="A sample artifact demonstrating the template structure">
    <meta name="author" content="Your Name">
    <meta name="claude-artifact-id" content="sample-artifact">
    <meta name="claude-conversation-url" content="https://claude.ai/chat/[conversation-id]">
    <meta name="created-date" content="2024-01-15">
    <meta name="version" content="1.0.0">
    
    <style>
        /* Artifact Header Styles */
        .artifact-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .artifact-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .artifact-title {
            font-size: 1.2em;
            font-weight: 600;
        }
        
        .artifact-links {
            display: flex;
            gap: 10px;
        }
        
        .artifact-link {
            padding: 5px 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
            transition: background 0.3s;
        }
        
        .artifact-link:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .artifact-content {
            margin-top: 80px;
            padding: 40px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Sample artifact styles */
        .demo-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .demo-title {
            font-size: 2.5em;
            margin-bottom: 20px;
            font-weight: 300;
        }
        
        .demo-description {
            font-size: 1.2em;
            opacity: 0.9;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .demo-button {
            margin-top: 30px;
            padding: 15px 40px;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 30px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .demo-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <!-- Artifact Header Bar -->
    <div class="artifact-header">
        <div class="artifact-info">
            <span class="artifact-title">🎨 Sample Artifact</span>
            <span style="opacity: 0.8; font-size: 0.9em;">Claude Artifact</span>
        </div>
        <div class="artifact-links">
            <a href="https://claude.ai/chat/[conversation-id]" class="artifact-link" target="_blank">
                View on Claude
            </a>
            <a href="../index.html" class="artifact-link">
                Back to Gallery
            </a>
        </div>
    </div>
    
    <!-- Artifact Content -->
    <div class="artifact-content">
        <div class="demo-container">
            <h1 class="demo-title">Welcome to Your First Artifact!</h1>
            <p class="demo-description">
                This is a sample artifact demonstrating the template structure. 
                Replace this content with your actual Claude artifact HTML.
                The header bar above provides navigation back to the gallery 
                and a link to the original Claude conversation.
            </p>
            <button class="demo-button" onclick="alert('Hello from your artifact!')">
                Try Me!
            </button>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #f5f5f5; border-radius: 10px; color: #333;">
            <h2>How to Use This Template</h2>
            <ol style="line-height: 1.8; margin-left: 20px;">
                <li>Copy your Claude artifact HTML content</li>
                <li>Replace everything inside the artifact-content div</li>
                <li>Update the meta tags in the head section</li>
                <li>Update the Claude conversation URL</li>
                <li>Save with a descriptive filename</li>
            </ol>
        </div>
    </div>
    
    <script>
        // Artifact metadata for gallery integration
        window.artifactMetadata = {
            id: 'sample-artifact',
            name: 'Sample Artifact',
            description: 'A sample artifact demonstrating the template structure',
            claudeUrl: 'https://claude.ai/chat/[conversation-id]',
            created: '2024-01-15',
            version: '1.0.0',
            tags: ['sample', 'template', 'demo']
        };
        
        console.log('Loaded Claude Artifact:', window.artifactMetadata.name);
    </script>
</body>
</html>
EOF
    
    # Create metadata for sample artifact
    cat > artifacts/metadata/sample-artifact.json << 'EOF'
{
    "id": "sample-artifact",
    "name": "Sample Artifact",
    "description": "A sample artifact demonstrating the template structure",
    "claudeUrl": "https://claude.ai/chat/[conversation-id]",
    "githubUrl": "https://github.com/[username]/[repo]/blob/main/artifacts/sample-artifact.html",
    "created": "2024-01-15",
    "updated": "2024-01-15",
    "version": "1.0.0",
    "author": "Your Name",
    "tags": ["sample", "template", "demo"],
    "category": "experimental",
    "icon": "🎯",
    "features": [
        "Template demonstration",
        "Header navigation",
        "Metadata integration"
    ]
}
EOF
    
    print_success "Sample artifact created!"
}

# Create .gitignore
create_gitignore() {
    print_info "Creating .gitignore..."
    
    cat > .gitignore << 'EOF'
# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Node modules (if any)
node_modules/

# Build files
dist/
build/

# Logs
*.log

# Environment variables
.env
.env.local

# Temporary files
tmp/
temp/
EOF
    
    print_success ".gitignore created!"
}

# Create artifact template
create_artifact_template() {
    print_info "Creating artifact template..."
    
    cat > docs/artifact-template.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Artifact Name] - Claude Artifact</title>
    <meta name="description" content="[Brief description of your artifact]">
    <meta name="author" content="[Your Name]">
    <meta name="claude-artifact-id" content="[artifact-id-from-claude]">
    <meta name="claude-conversation-url" content="https://claude.ai/chat/[conversation-id]">
    <meta name="created-date" content="[YYYY-MM-DD]">
    <meta name="version" content="1.0.0">
    
    <!-- Artifact Metadata -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "[Artifact Name]",
        "description": "[Description]",
        "author": {
            "@type": "Person",
            "name": "[Your Name]"
        },
        "dateCreated": "[YYYY-MM-DD]",
        "softwareVersion": "1.0.0",
        "keywords": "[tag1, tag2, tag3]"
    }
    </script>
    
    <style>
        /* Artifact Header Styles */
        .artifact-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .artifact-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .artifact-title {
            font-size: 1.2em;
            font-weight: 600;
        }
        
        .artifact-links {
            display: flex;
            gap: 10px;
        }
        
        .artifact-link {
            padding: 5px 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
            transition: background 0.3s;
        }
        
        .artifact-link:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .artifact-content {
            margin-top: 60px; /* Space for header */
        }
        
        /* Your artifact styles go here */
    </style>
</head>
<body>
    <!-- Artifact Header Bar -->
    <div class="artifact-header">
        <div class="artifact-info">
            <span class="artifact-title">🎨 [Artifact Name]</span>
            <span style="opacity: 0.8; font-size: 0.9em;">Claude Artifact</span>
        </div>
        <div class="artifact-links">
            <a href="https://claude.ai/chat/[conversation-id]" class="artifact-link" target="_blank">
                View on Claude
            </a>
            <a href="../index.html" class="artifact-link">
                Back to Gallery
            </a>
        </div>
    </div>
    
    <!-- Artifact Content -->
    <div class="artifact-content">
        <!-- YOUR ARTIFACT HTML CONTENT GOES HERE -->
        <!-- Copy everything from the Claude artifact -->
        
    </div>
    
    <!-- Optional: Artifact Footer -->
    <script>
        // Artifact metadata for gallery integration
        window.artifactMetadata = {
            id: '[artifact-id]',
            name: '[Artifact Name]',
            description: '[Description]',
            claudeUrl: 'https://claude.ai/chat/[conversation-id]',
            created: '[YYYY-MM-DD]',
            version: '1.0.0',
            tags: ['tag1', 'tag2', 'tag3']
        };
        
        // Log artifact load
        console.log('Loaded Claude Artifact:', window.artifactMetadata.name);
    </script>
</body>
</html>
EOF
    
    print_success "Artifact template created!"
}

# Create metadata template
create_metadata_template() {
    print_info "Creating metadata template..."
    
    cat > docs/metadata-template.json << 'EOF'
{
    "id": "artifact-unique-id",
    "name": "Artifact Display Name",
    "description": "Brief description of what this artifact does",
    "claudeUrl": "https://claude.ai/chat/[conversation-id]",
    "githubUrl": "https://github.com/[username]/[repo]/blob/main/artifacts/[filename].html",
    "created": "2024-01-15",
    "updated": "2024-01-15",
    "version": "1.0.0",
    "author": "Your Name",
    "tags": ["tool", "utility", "creative"],
    "category": "productivity",
    "icon": "🛠️",
    "features": [
        "Feature 1",
        "Feature 2",
        "Feature 3"
    ],
    "requirements": {
        "browser": "Modern browser with ES6 support",
        "dependencies": []
    },
    "screenshots": [
        {
            "url": "assets/images/screenshot1.png",
            "description": "Main interface"
        }
    ]
}
EOF
    
    print_success "Metadata template created!"
}

# Initialize git repository
initialize_git() {
    print_info "Initializing git repository..."
    
    git init
    git add .
    git commit -m "Initial commit: GitHub Artifacts Gallery System"
    
    print_success "Git repository initialized!"
}

# Create quick start script
create_quickstart_script() {
    print_info "Creating quick start script..."
    
    cat > quickstart.sh << 'EOF'
#!/bin/bash

# Quick start script for the artifacts gallery

echo "🚀 Starting Artifacts Gallery..."

# Check if Python is installed
if command -v python3 &> /dev/null; then
    echo "Starting Python HTTP server..."
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "Starting Python HTTP server..."
    python -m SimpleHTTPServer 8000
else
    echo "Python not found. Please install Python or use another HTTP server."
    echo "You can also open index.html directly in your browser."
fi
EOF
    
    chmod +x quickstart.sh
    print_success "Quick start script created!"
}

# Main setup function
main() {
    echo -e "${BLUE}=================================${NC}"
    echo -e "${BLUE}GitHub Artifacts System Setup${NC}"
    echo -e "${BLUE}=================================${NC}"
    echo ""
    
    # Check if directory already exists
    if [ -d "$REPO_NAME" ]; then
        print_warning "Directory $REPO_NAME already exists!"
        read -p "Do you want to continue and overwrite files? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Setup cancelled."
            exit 1
        fi
    fi
    
    # Create all components
    create_directory_structure
    create_readme
    create_main_gallery
    create_settings_json
    create_sample_artifact
    create_gitignore
    create_artifact_template
    create_metadata_template
    create_quickstart_script
    
    # Placeholder for the actual gallery files
    print_info "Creating placeholder files for gallery components..."
    
    # Create placeholders for the main components
    touch vibe-coding-gallery.html
    touch claude-artifact-app-store.html
    touch claude-artifact-manager.html
    touch github-sync-settings-manager.html
    
    # Add a note to these files
    for file in vibe-coding-gallery.html claude-artifact-app-store.html claude-artifact-manager.html github-sync-settings-manager.html; do
        echo "<!-- Replace this file with the actual content from Claude artifacts -->" > "$file"
        echo "<!-- This is a placeholder file -->" >> "$file"
    done
    
    # Initialize git
    read -p "Initialize git repository? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        initialize_git
    fi
    
    # Final instructions
    echo ""
    echo -e "${GREEN}=================================${NC}"
    echo -e "${GREEN}✨ Setup Complete!${NC}"
    echo -e "${GREEN}=================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Copy the actual HTML content from Claude artifacts into:"
    echo "   - vibe-coding-gallery.html"
    echo "   - claude-artifact-app-store.html"
    echo "   - claude-artifact-manager.html"
    echo "   - github-sync-settings-manager.html"
    echo ""
    echo "2. Add your artifacts to the artifacts/ directory"
    echo ""
    echo "3. Run the gallery locally:"
    echo "   cd $REPO_NAME"
    echo "   ./quickstart.sh"
    echo ""
    echo "4. Push to GitHub:"
    echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "   git push -u origin main"
    echo ""
    echo "5. Enable GitHub Pages in repository settings"
    echo ""
    print_success "Happy coding! 🎨"
}

# Run main function
main