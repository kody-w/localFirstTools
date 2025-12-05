#!/usr/bin/env python3
"""
Accessibility Enhancement Script for wowMon.html
This script adds comprehensive accessibility features to the WoWmon game.
"""

import re

def add_accessibility_features(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add meta description if not present
    if 'meta name="description"' not in content:
        content = content.replace(
            '<title>WoWmon - Pocket Creatures of Azeroth</title>',
            '<meta name="description" content="WoWmon - An accessible Warcraft-themed creature collection game inspired by Pokemon">\n    <title>WoWmon - Pocket Creatures of Azeroth</title>'
        )

    # 2. Add accessibility CSS before </style>
    accessibility_css = '''
        /* Accessibility Enhancements */

        /* Focus indicators for keyboard navigation */
        button:focus,
        .menu-option:focus,
        .move-option:focus,
        .dpad-btn:focus,
        .btn:focus,
        .cartridge-btn:focus {
            outline: 3px solid #ffcc00;
            outline-offset: 2px;
            z-index: 1000;
        }

        /* Skip to content link */
        .skip-link {
            position: absolute;
            top: -40px;
            left: 0;
            background: #000;
            color: #fff;
            padding: 8px;
            text-decoration: none;
            z-index: 10000;
        }

        .skip-link:focus {
            top: 0;
        }

        /* Screen reader only content */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }

        /* Live region for screen reader announcements */
        .live-region {
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        }

        /* Accessibility Settings Panel */
        .accessibility-panel {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #8b956d;
            border: 4px solid #2d3a1d;
            padding: 20px;
            border-radius: 10px;
            display: none;
            z-index: 10000;
            min-width: 300px;
            max-width: 90vw;
            color: #0f380f;
        }

        .accessibility-panel.active {
            display: block;
        }

        .accessibility-panel h2 {
            margin-bottom: 15px;
            font-size: 18px;
            color: #0f380f;
        }

        .accessibility-option {
            margin: 10px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .accessibility-option label {
            cursor: pointer;
            font-size: 14px;
        }

        .accessibility-option input[type="checkbox"],
        .accessibility-option input[type="range"] {
            cursor: pointer;
        }

        .accessibility-option input[type="range"] {
            flex: 1;
        }

        /* High contrast mode */
        body.high-contrast {
            background: #000;
        }

        body.high-contrast .game-container {
            background: #fff;
            border: 4px solid #000;
        }

        body.high-contrast .game-screen {
            border-color: #000;
        }

        body.high-contrast .btn,
        body.high-contrast .dpad-btn,
        body.high-contrast .cartridge-btn {
            background: #000;
            color: #fff;
            border: 2px solid #fff;
        }

        body.high-contrast .text-box,
        body.high-contrast .menu {
            background: #fff;
            border-color: #000;
            color: #000;
        }

        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        body.reduced-motion * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }

        /* Large text mode */
        body.large-text {
            font-size: 120%;
        }

        body.large-text .text-box,
        body.large-text .menu-option,
        body.large-text .move-option {
            font-size: 18px;
        }

        body.large-text .btn,
        body.large-text .cartridge-btn {
            font-size: 16px;
            padding: 18px 24px;
        }

        /* Button with proper tabindex styling */
        [tabindex]:focus {
            outline: 3px solid #ffcc00;
            outline-offset: 2px;
        }

        /* Better focus for menu options */
        .menu-option[tabindex]:focus,
        .move-option[tabindex]:focus {
            outline: 3px solid #ffcc00;
            outline-offset: -2px;
        }

        .close-panel-btn {
            background: #4a5a3a;
            border: none;
            color: #8b956d;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 15px;
            box-shadow: 0 2px 0 #2d3a1d;
            font-family: monospace;
        }

        .close-panel-btn:active {
            transform: translateY(1px);
            box-shadow: 0 1px 0 #2d3a1d;
        }
'''

    if '/* Accessibility Enhancements */' not in content:
        content = content.replace('    </style>', accessibility_css + '    </style>')

    # 3. Add accessibility HTML elements after <body>
    accessibility_html = '''    <!-- Accessibility Features -->
    <a href="#game-screen" class="skip-link">Skip to game content</a>

    <!-- Screen reader live region for announcements -->
    <div class="live-region" role="status" aria-live="polite" aria-atomic="true" id="liveRegion"></div>

    <!-- Accessibility Settings Panel -->
    <div class="accessibility-panel" id="accessibilityPanel" role="dialog" aria-labelledby="a11y-panel-title" aria-hidden="true">
        <h2 id="a11y-panel-title">Accessibility Settings</h2>
        <div class="accessibility-option">
            <input type="checkbox" id="highContrastToggle" aria-label="Enable high contrast mode">
            <label for="highContrastToggle">High Contrast Mode</label>
        </div>
        <div class="accessibility-option">
            <input type="checkbox" id="reducedMotionToggle" aria-label="Enable reduced motion">
            <label for="reducedMotionToggle">Reduced Motion</label>
        </div>
        <div class="accessibility-option">
            <input type="checkbox" id="largeTextToggle" aria-label="Enable large text">
            <label for="largeTextToggle">Large Text (120%)</label>
        </div>
        <div class="accessibility-option">
            <input type="checkbox" id="screenReaderMode" aria-label="Enable enhanced screen reader announcements">
            <label for="screenReaderMode">Enhanced Screen Reader</label>
        </div>
        <div class="accessibility-option">
            <label for="textSpeedRange">Text Speed:</label>
            <input type="range" id="textSpeedRange" min="1" max="5" value="3" aria-label="Adjust text display speed">
            <span id="textSpeedValue" aria-live="polite">3</span>
        </div>
        <button class="close-panel-btn" onclick="game.toggleAccessibilityPanel()" aria-label="Close accessibility settings">Close</button>
    </div>

'''

    if '<!-- Accessibility Features -->' not in content:
        content = content.replace('<body>', '<body>\n' + accessibility_html)

    # 4. Add ARIA labels to cartridge controls
    content = re.sub(
        r'<button class="cartridge-btn" onclick="game\.loadCartridge\(\)">Load Game</button>',
        '<button class="cartridge-btn" onclick="game.loadCartridge()" aria-label="Load game cartridge from file">Load Game</button>',
        content
    )

    content = re.sub(
        r'<button class="cartridge-btn" onclick="game\.autoLoadWoWmon\(\)">Load WoWmon</button>',
        '<button class="cartridge-btn" onclick="game.autoLoadWoWmon()" aria-label="Load WoWmon game automatically">Load WoWmon</button>',
        content
    )

    content = re.sub(
        r'<button class="cartridge-btn" onclick="game\.exportSave\(\)">Export Save</button>',
        '<button class="cartridge-btn" onclick="game.exportSave()" aria-label="Export save game data to file">Export Save</button>',
        content
    )

    content = re.sub(
        r'<button class="cartridge-btn" onclick="game\.importSave\(\)">Import Save</button>',
        '<button class="cartridge-btn" onclick="game.importSave()" aria-label="Import save game data from file">Import Save</button>',
        content
    )

    # 5. Add accessibility button to cartridge controls
    if 'Accessibility' not in content.split('cartridge-controls')[1].split('</div>')[0]:
        content = content.replace(
            '<input type="file" id="cartridgeInput"',
            '<button class="cartridge-btn" onclick="game.toggleAccessibilityPanel()" aria-label="Open accessibility settings panel">Accessibility</button>\n            <input type="file" id="cartridgeInput"'
        )

    # 6. Add ARIA label to game screen
    content = re.sub(
        r'<div class="game-screen">',
        '<div class="game-screen" id="game-screen" role="application" aria-label="WoWmon game screen">',
        content
    )

    # 7. Add ARIA labels to canvas
    content = re.sub(
        r'<canvas id="gameCanvas" width="160" height="144"></canvas>',
        '<canvas id="gameCanvas" width="160" height="144" aria-label="Game canvas - visual game display" role="img"></canvas>',
        content
    )

    # 8. Add ARIA to text box
    content = re.sub(
        r'<div class="text-box" id="textBox">',
        '<div class="text-box" id="textBox" role="dialog" aria-live="polite" aria-label="Game dialogue">',
        content
    )

    # 9. Add ARIA to menus
    content = re.sub(
        r'<div class="menu" id="mainMenu"',
        '<div class="menu" id="mainMenu" role="menu" aria-label="Main game menu"',
        content
    )

    content = re.sub(
        r'<div class="menu" id="battleMenu"',
        '<div class="menu" id="battleMenu" role="menu" aria-label="Battle menu"',
        content
    )

    # 10. Add ARIA to move menu
    content = re.sub(
        r'<div class="move-menu" id="moveMenu">',
        '<div class="move-menu" id="moveMenu" role="menu" aria-label="Move selection menu">',
        content
    )

    # 11. Add role and tabindex to menu options
    content = re.sub(
        r'<div class="menu-option selected">CREATURES</div>',
        '<div class="menu-option selected" role="menuitem" tabindex="0" aria-label="View creatures">CREATURES</div>',
        content
    )

    content = re.sub(
        r'<div class="menu-option">BAG</div>',
        '<div class="menu-option" role="menuitem" tabindex="-1" aria-label="Open bag">BAG</div>',
        content
    )

    content = re.sub(
        r'<div class="menu-option">SAVE</div>',
        '<div class="menu-option" role="menuitem" tabindex="-1" aria-label="Save game">SAVE</div>',
        content
    )

    content = re.sub(
        r'<div class="menu-option">EXIT</div>',
        '<div class="menu-option" role="menuitem" tabindex="-1" aria-label="Exit menu">EXIT</div>',
        content
    )

    # 12. Add role to battle menu options
    content = re.sub(
        r'<div class="menu-option selected">FIGHT</div>',
        '<div class="menu-option selected" role="menuitem" tabindex="0" aria-label="Choose fight action">FIGHT</div>',
        content, count=1
    )

    # 13. Add ARIA labels to D-pad buttons
    content = re.sub(
        r'<button class="dpad-btn" id="up" data-key="ArrowUp">▲</button>',
        '<button class="dpad-btn" id="up" data-key="ArrowUp" aria-label="Move up">▲</button>',
        content
    )

    content = re.sub(
        r'<button class="dpad-btn" id="left" data-key="ArrowLeft">◄</button>',
        '<button class="dpad-btn" id="left" data-key="ArrowLeft" aria-label="Move left">◄</button>',
        content
    )

    content = re.sub(
        r'<button class="dpad-btn" id="right" data-key="ArrowRight">►</button>',
        '<button class="dpad-btn" id="right" data-key="ArrowRight" aria-label="Move right">►</button>',
        content
    )

    content = re.sub(
        r'<button class="dpad-btn" id="down" data-key="ArrowDown">▼</button>',
        '<button class="dpad-btn" id="down" data-key="ArrowDown" aria-label="Move down">▼</button>',
        content
    )

    # 14. Add ARIA to action buttons
    content = re.sub(
        r'<button class="btn" data-key="z">A</button>',
        '<button class="btn" data-key="z" aria-label="Action button A - Confirm and interact">A</button>',
        content
    )

    content = re.sub(
        r'<button class="btn" data-key="x">B</button>',
        '<button class="btn" data-key="x" aria-label="Action button B - Cancel and go back">B</button>',
        content
    )

    content = re.sub(
        r'<button class="btn" data-key="Enter">START</button>',
        '<button class="btn" data-key="Enter" aria-label="Start button - Open main menu">START</button>',
        content
    )

    content = re.sub(
        r'<button class="btn" data-key="Shift">SELECT</button>',
        '<button class="btn" data-key="Shift" aria-label="Select button - Open creature quick menu">SELECT</button>',
        content
    )

    # 15. Add ARIA to battle UI elements
    content = re.sub(
        r'<div class="battle-ui" id="battleUI">',
        '<div class="battle-ui" id="battleUI" role="complementary" aria-label="Battle status information">',
        content
    )

    return content

def add_javascript_accessibility(content):
    """Add JavaScript accessibility functions before the closing GameEngine class"""

    js_accessibility = '''

            // Accessibility Features

            announce(message, priority = 'polite') {
                // Announce to screen readers
                const liveRegion = document.getElementById('liveRegion');
                if (liveRegion) {
                    liveRegion.setAttribute('aria-live', priority);
                    liveRegion.textContent = message;

                    // Clear after announcement
                    setTimeout(() => {
                        liveRegion.textContent = '';
                    }, 100);
                }

                // Also log for debugging
                if (this.accessibilitySettings && this.accessibilitySettings.screenReaderMode) {
                    console.log('[Screen Reader]:', message);
                }
            }

            toggleAccessibilityPanel() {
                const panel = document.getElementById('accessibilityPanel');
                const isActive = panel.classList.contains('active');

                if (isActive) {
                    panel.classList.remove('active');
                    panel.setAttribute('aria-hidden', 'true');
                    this.announce('Accessibility settings closed');
                } else {
                    panel.classList.add('active');
                    panel.setAttribute('aria-hidden', 'false');
                    document.getElementById('highContrastToggle').focus();
                    this.announce('Accessibility settings opened');
                }
            }

            initializeAccessibility() {
                // Initialize accessibility settings
                this.accessibilitySettings = {
                    highContrast: false,
                    reducedMotion: false,
                    largeText: false,
                    screenReaderMode: false,
                    textSpeed: 3
                };

                // Load saved accessibility preferences
                const saved = localStorage.getItem('wowmon_accessibility');
                if (saved) {
                    try {
                        this.accessibilitySettings = JSON.parse(saved);
                        this.applyAccessibilitySettings();
                    } catch (e) {
                        console.error('Failed to load accessibility settings:', e);
                    }
                }

                // High Contrast Toggle
                const highContrastToggle = document.getElementById('highContrastToggle');
                if (highContrastToggle) {
                    highContrastToggle.checked = this.accessibilitySettings.highContrast;
                    highContrastToggle.addEventListener('change', (e) => {
                        this.accessibilitySettings.highContrast = e.target.checked;
                        document.body.classList.toggle('high-contrast', e.target.checked);
                        this.saveAccessibilitySettings();
                        this.announce(e.target.checked ? 'High contrast mode enabled' : 'High contrast mode disabled');
                    });
                }

                // Reduced Motion Toggle
                const reducedMotionToggle = document.getElementById('reducedMotionToggle');
                if (reducedMotionToggle) {
                    reducedMotionToggle.checked = this.accessibilitySettings.reducedMotion;
                    reducedMotionToggle.addEventListener('change', (e) => {
                        this.accessibilitySettings.reducedMotion = e.target.checked;
                        document.body.classList.toggle('reduced-motion', e.target.checked);
                        this.saveAccessibilitySettings();
                        this.announce(e.target.checked ? 'Reduced motion enabled' : 'Reduced motion disabled');
                    });
                }

                // Large Text Toggle
                const largeTextToggle = document.getElementById('largeTextToggle');
                if (largeTextToggle) {
                    largeTextToggle.checked = this.accessibilitySettings.largeText;
                    largeTextToggle.addEventListener('change', (e) => {
                        this.accessibilitySettings.largeText = e.target.checked;
                        document.body.classList.toggle('large-text', e.target.checked);
                        this.saveAccessibilitySettings();
                        this.announce(e.target.checked ? 'Large text enabled' : 'Large text disabled');
                    });
                }

                // Screen Reader Mode Toggle
                const screenReaderMode = document.getElementById('screenReaderMode');
                if (screenReaderMode) {
                    screenReaderMode.checked = this.accessibilitySettings.screenReaderMode;
                    screenReaderMode.addEventListener('change', (e) => {
                        this.accessibilitySettings.screenReaderMode = e.target.checked;
                        this.saveAccessibilitySettings();
                        this.announce(e.target.checked ? 'Enhanced screen reader mode enabled' : 'Enhanced screen reader mode disabled');
                    });
                }

                // Text Speed Range
                const textSpeedRange = document.getElementById('textSpeedRange');
                const textSpeedValue = document.getElementById('textSpeedValue');
                if (textSpeedRange && textSpeedValue) {
                    textSpeedRange.value = this.accessibilitySettings.textSpeed;
                    textSpeedValue.textContent = this.accessibilitySettings.textSpeed;
                    textSpeedRange.addEventListener('input', (e) => {
                        this.accessibilitySettings.textSpeed = parseInt(e.target.value);
                        textSpeedValue.textContent = e.target.value;
                        this.saveAccessibilitySettings();
                        this.announce('Text speed set to ' + e.target.value);
                    });
                }

                // Keyboard shortcuts
                document.addEventListener('keydown', (e) => {
                    // Alt+A opens accessibility panel
                    if (e.altKey && e.key.toLowerCase() === 'a') {
                        e.preventDefault();
                        this.toggleAccessibilityPanel();
                    }

                    // Escape closes accessibility panel
                    if (e.key === 'Escape') {
                        const panel = document.getElementById('accessibilityPanel');
                        if (panel && panel.classList.contains('active')) {
                            this.toggleAccessibilityPanel();
                        }
                    }
                });

                // Add focus management for menus
                this.setupMenuAccessibility();

                // Announce game state changes
                this.announceGameState();
            }

            setupMenuAccessibility() {
                // Add keyboard navigation to menu options
                const addMenuNavigation = (menuId) => {
                    const menu = document.getElementById(menuId);
                    if (!menu) return;

                    const options = menu.querySelectorAll('.menu-option, .move-option');
                    options.forEach((option, index) => {
                        option.setAttribute('tabindex', index === 0 ? '0' : '-1');
                        option.setAttribute('role', 'menuitem');

                        option.addEventListener('keydown', (e) => {
                            let newIndex = index;

                            if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                                e.preventDefault();
                                newIndex = (index + 1) % options.length;
                            } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                                e.preventDefault();
                                newIndex = (index - 1 + options.length) % options.length;
                            } else if (e.key === 'Enter' || e.key === ' ') {
                                e.preventDefault();
                                option.click();
                                return;
                            }

                            if (newIndex !== index) {
                                options[newIndex].focus();
                                options[newIndex].setAttribute('tabindex', '0');
                                option.setAttribute('tabindex', '-1');

                                // Announce the focused option
                                this.announce(options[newIndex].textContent.trim());
                            }
                        });
                    });
                };

                addMenuNavigation('mainMenu');
                addMenuNavigation('battleMenu');
                addMenuNavigation('moveMenu');
            }

            announceGameState() {
                // Override state changes to announce them
                const originalState = this.state;
                Object.defineProperty(this, '_state', {
                    writable: true,
                    value: originalState
                });

                Object.defineProperty(this, 'state', {
                    get() {
                        return this._state;
                    },
                    set(newState) {
                        const oldState = this._state;
                        this._state = newState;

                        if (this.accessibilitySettings && this.accessibilitySettings.screenReaderMode && oldState !== newState) {
                            switch (newState) {
                                case 'WORLD':
                                    this.announce('Exploring the world');
                                    break;
                                case 'BATTLE':
                                    this.announce('Battle started');
                                    break;
                                case 'MENU':
                                    this.announce('Menu opened');
                                    break;
                                case 'TEXT':
                                    this.announce('Dialogue displayed');
                                    break;
                            }
                        }
                    }
                });
            }

            saveAccessibilitySettings() {
                localStorage.setItem('wowmon_accessibility', JSON.stringify(this.accessibilitySettings));
            }

            applyAccessibilitySettings() {
                if (this.accessibilitySettings.highContrast) {
                    document.body.classList.add('high-contrast');
                }
                if (this.accessibilitySettings.reducedMotion) {
                    document.body.classList.add('reduced-motion');
                }
                if (this.accessibilitySettings.largeText) {
                    document.body.classList.add('large-text');
                }
            }
'''

    # Find the init() method and add accessibility initialization
    init_pattern = r'(init\(\) {[^}]+this\.gameLoop\(\);[\s]*})'

    def replace_init(match):
        original = match.group(1)
        return original.replace(
            'this.gameLoop();',
            'this.initializeAccessibility();\n                this.gameLoop();'
        )

    content = re.sub(init_pattern, replace_init, content)

    # Add the accessibility methods before the final closing brace of GameEngine class
    # Find the location just before "// Initialize game engine"
    marker = '        // Initialize game engine'
    if marker in content:
        content = content.replace(marker, js_accessibility + '\n        ' + marker)

    return content

if __name__ == '__main__':
    file_path = '/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html'
    print("Adding accessibility features to wowMon.html...")

    content = add_accessibility_features(file_path)
    content = add_javascript_accessibility(content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Accessibility features added successfully!")
    print("\nKey improvements:")
    print("- Added ARIA labels and semantic HTML")
    print("- Implemented keyboard navigation")
    print("- Added screen reader announcements")
    print("- Created accessibility settings panel")
    print("- Added high contrast mode")
    print("- Added reduced motion support")
    print("- Added large text mode")
    print("- Improved focus indicators")
    print("- Added skip links")
    print("\nPress Alt+A to open the accessibility settings panel while playing!")
