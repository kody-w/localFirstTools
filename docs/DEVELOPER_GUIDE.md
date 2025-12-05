# Local First Tools - Developer Guide

Complete guide for contributing applications, understanding the architecture, and maintaining the project.

## Table of Contents

1. [Quick Start for Contributors](#quick-start-for-contributors)
2. [Development Environment](#development-environment)
3. [Creating Your First Application](#creating-your-first-application)
4. [Application Standards](#application-standards)
5. [Testing Your Application](#testing-your-application)
6. [Submitting Contributions](#submitting-contributions)
7. [Gallery System](#gallery-system)
8. [Advanced Topics](#advanced-topics)

## Quick Start for Contributors

### Prerequisites

```bash
# Required
- Modern web browser (Chrome, Firefox, Edge)
- Text editor (VS Code, Sublime, Vim, etc.)
- Git for version control

# Optional but helpful
- Python 3.7+ (for gallery updater scripts)
- Local web server (python -m http.server)
```

### Getting the Code

```bash
# Clone the repository
git clone https://github.com/your-repo/localFirstTools3.git
cd localFirstTools3

# View existing applications
ls *.html

# Run local server (optional)
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Your First Contribution

1. **Create** a new HTML file in the root directory
2. **Code** your application (see template below)
3. **Test** in multiple browsers
4. **Update** the gallery configuration
5. **Submit** a pull request

## Development Environment

### Recommended Setup

**VS Code Extensions:**
- HTML CSS Support
- JavaScript (ES6) code snippets
- Live Server
- Prettier - Code formatter

**Browser DevTools:**
- Chrome DevTools (F12)
- Firefox Developer Edition
- Safari Web Inspector

### Project Structure

```
localFirstTools3/
├── index.html                    # Main gallery launcher
├── vibe_gallery_config.json      # Auto-generated app registry
├── tools-manifest.json           # Simple tool listing
├── *.html                        # 100+ application files in root
├── CLAUDE.md                     # AI assistant instructions
├── README.md                     # Project overview
│
├── docs/                         # Documentation
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md        # This file
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION.md
│   ├── templates/                # Application templates
│   ├── schemas/                  # JSON schemas
│   └── examples/                 # Example applications
│
├── scripts/                      # Utility scripts
│   └── update-gallery.sh
│
├── archive/                      # Legacy code and versions
│   └── app-store-updater.py
│
├── data/                         # Data files
│   ├── config/
│   │   └── utility_apps_config.json
│   └── games/                    # Game data
│
├── edgeAddons/                   # Browser extensions
│   └── xbox-mkb-extension/
│
├── notes/                        # Dev notes and experiments
│
├── vibe_gallery_updater.py       # Main gallery updater
├── update-tools-manifest.py      # Manifest updater
└── *.py                          # Other utility scripts
```

### Development Workflow

```bash
# 1. Create a new branch
git checkout -b feature/my-awesome-app

# 2. Create your HTML file
touch my-awesome-app.html

# 3. Develop and test locally
python3 -m http.server 8000

# 4. Update gallery configuration
python3 vibe_gallery_updater.py

# 5. Test the gallery
# Open http://localhost:8000

# 6. Commit your changes
git add my-awesome-app.html
git add vibe_gallery_config.json
git commit -m "Add My Awesome App"

# 7. Push and create PR
git push origin feature/my-awesome-app
```

## Creating Your First Application

### Minimal Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Brief description of your app for SEO and gallery">
    <title>Your Application Name</title>
    <style>
        /* All CSS inline here */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Your custom styles */
    </style>
</head>
<body>
    <!-- Your HTML structure -->
    <div class="container">
        <h1>Your Application</h1>
        <!-- Application content -->
    </div>

    <script>
        // All JavaScript inline here

        // Local Storage helpers
        function saveData(key, data) {
            localStorage.setItem(key, JSON.stringify(data));
        }

        function loadData(key) {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        }

        // Export functionality
        function exportToJSON() {
            const data = {
                version: "1.0",
                timestamp: new Date().toISOString(),
                data: {
                    // Your application data
                }
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `your-app-data-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        // Import functionality
        function importFromJSON(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    // Process imported data
                    console.log('Data imported:', data);
                } catch (error) {
                    console.error('Import failed:', error);
                    alert('Failed to import file. Please check the file format.');
                }
            };
            reader.readAsText(file);
        }

        // Your application logic
        function init() {
            // Initialize your application
            console.log('Application initialized');
        }

        // Start the application
        init();
    </script>
</body>
</html>
```

### Advanced Template Features

See `/docs/templates/advanced-app-template.html` for:
- Responsive design patterns
- Touch and mouse event handling
- Canvas and SVG usage
- Audio synthesis
- Gamepad API integration
- Advanced state management
- Animation loops
- Error handling

## Application Standards

### Core Principles

1. **Self-Contained**: Everything in one HTML file
2. **No Dependencies**: No CDN links, no npm packages
3. **Offline First**: Must work without internet
4. **Local Storage**: Save state in browser
5. **Import/Export**: JSON data portability
6. **Responsive**: Works on desktop and mobile
7. **Accessible**: Keyboard navigation, ARIA labels

### File Naming

```bash
# Good
my-awesome-app.html
card-game-trainer.html
3d-cube-visualizer.html

# Bad
MyApp.html                    # No camelCase
app_v2.html                   # No version numbers
temp-test-file.html           # No temporary files
```

### Code Quality

**Required:**
- Valid HTML5 structure
- Clean, formatted code
- Comments for complex logic
- Error handling
- Browser console logging for debugging

**Recommended:**
- ES6+ JavaScript features
- CSS Grid/Flexbox for layout
- CSS Variables for theming
- Semantic HTML elements
- Progressive enhancement

### Metadata Requirements

```html
<head>
    <!-- Required -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clear, Descriptive Title</title>

    <!-- Highly Recommended -->
    <meta name="description" content="Detailed description for gallery">

    <!-- Optional but helpful for auto-categorization -->
    <!-- Include keywords in HTML comments -->
    <!-- Keywords: 3d, game, canvas, svg, audio, interactive -->
</head>
```

### Feature Detection

```javascript
// Check for required APIs
function checkSupport() {
    const features = {
        localStorage: typeof(Storage) !== "undefined",
        canvas: !!document.createElement('canvas').getContext,
        webgl: !!document.createElement('canvas').getContext('webgl'),
        audio: typeof(Audio) !== "undefined",
        gamepad: 'getGamepads' in navigator
    };

    // Warn user if critical features missing
    if (!features.localStorage) {
        console.warn('LocalStorage not supported');
    }

    return features;
}
```

### Performance Guidelines

1. **File Size**: Keep under 500KB when possible
2. **Assets**: Inline small images as data URIs
3. **Animations**: Use requestAnimationFrame
4. **Memory**: Clean up event listeners
5. **Mobile**: Test on real devices

## Testing Your Application

### Browser Testing Checklist

**Desktop:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (latest, Mac only)

**Mobile:**
- [ ] iOS Safari (iPhone)
- [ ] Chrome for Android
- [ ] Landscape and portrait modes

### Feature Testing

- [ ] Application loads without errors
- [ ] All interactive elements work
- [ ] LocalStorage saves/loads correctly
- [ ] Export function creates valid JSON
- [ ] Import function reads JSON correctly
- [ ] Offline functionality works
- [ ] Keyboard navigation works
- [ ] Touch gestures work on mobile
- [ ] Gamepad support (if applicable)
- [ ] No console errors
- [ ] Responsive at all screen sizes

### Performance Testing

```javascript
// Add performance monitoring
window.addEventListener('load', () => {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`Page load time: ${pageLoadTime}ms`);
});

// Monitor memory usage (Chrome only)
if (performance.memory) {
    console.log('Memory usage:', {
        used: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
        total: (performance.memory.totalJSHeapSize / 1048576).toFixed(2) + ' MB'
    });
}
```

### Accessibility Testing

- [ ] Semantic HTML elements used
- [ ] ARIA labels where needed
- [ ] Keyboard only navigation works
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader compatible
- [ ] No seizure-inducing animations

## Submitting Contributions

### Pre-Submission Checklist

- [ ] Application works in all major browsers
- [ ] Code is clean and commented
- [ ] File size is reasonable
- [ ] No external dependencies
- [ ] LocalStorage implemented
- [ ] Import/Export functions work
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Gallery updated (run updater script)
- [ ] Git commit message is descriptive

### Pull Request Guidelines

**Title Format:**
```
Add [Application Name] - [Brief Description]

Example:
Add Rainbow Path Designer - Interactive SVG drawing tool
```

**PR Description Template:**
```markdown
## Application Description
Brief description of what your application does.

## Category
Suggested category: [Visual Art / Games / Tools / etc.]

## Features
- Feature 1
- Feature 2
- Feature 3

## Testing
- [x] Tested in Chrome
- [x] Tested in Firefox
- [x] Tested on mobile
- [x] LocalStorage works
- [x] Import/Export works

## Screenshots
(Optional but helpful)

## Additional Notes
Any special considerations or known limitations.
```

### Code Review Process

Your PR will be reviewed for:

1. **Functionality**: Does it work as described?
2. **Code Quality**: Is it clean and maintainable?
3. **Standards**: Does it follow project guidelines?
4. **Performance**: Is it reasonably efficient?
5. **Documentation**: Is it well-commented?

### After Submission

- Respond to review feedback promptly
- Make requested changes in your branch
- Update your PR with new commits
- Once approved, your app will be merged!

## Gallery System

### How Auto-Discovery Works

```python
# The vibe_gallery_updater.py script:
1. Scans all HTML files in root directory
2. Extracts title from <title> tag
3. Extracts description from <meta name="description">
4. Analyzes code for technical features (3D, canvas, SVG, etc.)
5. Determines complexity based on file size and features
6. Auto-categorizes based on keywords and patterns
7. Generates vibe_gallery_config.json
```

### Manual Updates

```bash
# Run the gallery updater
python3 vibe_gallery_updater.py

# Update tools manifest
python3 update-tools-manifest.py

# Quick shell wrapper
./scripts/update-gallery.sh
```

### Gallery Configuration

Edit `vibe_gallery_config.json` manually if needed:

```json
{
  "vibeGallery": {
    "categories": {
      "visual_art": {
        "title": "Visual Art & Design",
        "description": "...",
        "color": "#ff6b9d",
        "apps": [
          {
            "title": "Your App",
            "filename": "your-app.html",
            "path": "your-app.html",
            "description": "...",
            "tags": ["canvas", "interactive"],
            "category": "visual_art",
            "featured": true,
            "complexity": "intermediate",
            "interactionType": "drawing"
          }
        ]
      }
    }
  }
}
```

### Adding Custom Categories

Modify `vibe_gallery_updater.py`:

```python
category_info = {
    "your_new_category": {
        "title": "Your Category Title",
        "description": "Description of category",
        "color": "#yourcolor"
    }
}
```

## Advanced Topics

### Canvas Applications

```javascript
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

// Make canvas responsive
function resizeCanvas() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Animation loop
function animate() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Your drawing code

    requestAnimationFrame(animate);
}
animate();
```

### WebGL/3D Applications

```javascript
// Basic Three.js pattern (inline, no CDN)
// Include Three.js code inline or use minimal WebGL

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
const renderer = new THREE.WebGLRenderer();

// Your 3D scene code
```

### Audio Applications

```javascript
// Web Audio API
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

function playTone(frequency, duration) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = frequency;
    gainNode.gain.value = 0.3;

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration);
}
```

### Gamepad Support

```javascript
// Xbox controller support
function updateGamepad() {
    const gamepads = navigator.getGamepads();
    const gamepad = gamepads[0];

    if (gamepad) {
        // Buttons
        if (gamepad.buttons[0].pressed) {
            console.log('A button pressed');
        }

        // Axes
        const leftStickX = gamepad.axes[0];
        const leftStickY = gamepad.axes[1];

        // Your game logic
    }

    requestAnimationFrame(updateGamepad);
}

window.addEventListener('gamepadconnected', (e) => {
    console.log('Gamepad connected:', e.gamepad);
    updateGamepad();
});
```

### State Management Pattern

```javascript
class AppState {
    constructor() {
        this.data = this.load() || this.getDefaultState();
        this.listeners = [];
    }

    getDefaultState() {
        return {
            // Your default state
        };
    }

    update(newData) {
        this.data = { ...this.data, ...newData };
        this.save();
        this.notify();
    }

    save() {
        localStorage.setItem('appState', JSON.stringify(this.data));
    }

    load() {
        const saved = localStorage.getItem('appState');
        return saved ? JSON.parse(saved) : null;
    }

    subscribe(callback) {
        this.listeners.push(callback);
    }

    notify() {
        this.listeners.forEach(callback => callback(this.data));
    }
}

const state = new AppState();
```

### Progressive Enhancement

```javascript
// Start with basic functionality
function basicFeature() {
    // Works everywhere
}

// Add enhanced features with detection
if ('IntersectionObserver' in window) {
    // Use modern API
}

// Provide fallbacks
const requestAnimFrame =
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    (callback => setTimeout(callback, 1000/60));
```

## Community and Support

### Getting Help

- **Documentation**: Read all docs thoroughly
- **Examples**: Study existing applications
- **GitHub Discussions**: Ask questions
- **Code Review**: Request early feedback

### Contributing Beyond Code

- **Documentation**: Improve guides and tutorials
- **Testing**: Test applications and report bugs
- **Design**: Create UI/UX improvements
- **Tutorials**: Write blog posts or videos
- **Community**: Help other developers

### Best Practices

1. **Start Small**: Begin with simple applications
2. **Study Examples**: Learn from existing apps
3. **Iterate**: Improve based on feedback
4. **Document**: Comment your code well
5. **Test**: Thoroughly test before submitting
6. **Share**: Help others learn from your work

---

**Happy coding! Build amazing local-first applications!**
