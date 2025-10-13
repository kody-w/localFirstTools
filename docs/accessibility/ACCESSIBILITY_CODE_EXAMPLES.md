# WoWmon Accessibility - Code Examples for Developers

## Quick Reference for Implementing Accessibility Features

This document provides code snippets and examples from the WoWmon accessibility implementation that can be reused in other projects.

---

## 1. ARIA Labels for Interactive Elements

### Buttons with Clear Purpose
```html
<!-- Game controls -->
<button class="btn" data-key="z"
        aria-label="Action button A - Confirm and interact">A</button>

<button class="btn" data-key="x"
        aria-label="Action button B - Cancel and go back">B</button>

<!-- File operations -->
<button onclick="game.exportSave()"
        aria-label="Export save game data to file">Export Save</button>

<button onclick="game.importSave()"
        aria-label="Import save game data from file">Import Save</button>
```

### Directional Controls
```html
<button class="dpad-btn" id="up" data-key="ArrowUp"
        aria-label="Move up">▲</button>
<button class="dpad-btn" id="down" data-key="ArrowDown"
        aria-label="Move down">▼</button>
<button class="dpad-btn" id="left" data-key="ArrowLeft"
        aria-label="Move left">◄</button>
<button class="dpad-btn" id="right" data-key="ArrowRight"
        aria-label="Move right">►</button>
```

**Key Principle:** Describe the action, not just the appearance.

---

## 2. Semantic Roles and Structure

### Application Container
```html
<div class="game-screen" id="game-screen"
     role="application"
     aria-label="WoWmon game screen">
    <canvas id="gameCanvas" width="160" height="144"
            aria-label="Game canvas - visual game display"
            role="img"></canvas>
</div>
```

### Menu System
```html
<div class="menu" id="mainMenu"
     role="menu"
     aria-label="Main game menu">

    <div class="menu-option selected"
         role="menuitem"
         tabindex="0"
         aria-label="View creatures">CREATURES</div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Open bag">BAG</div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Save game">SAVE</div>
</div>
```

### Dialog/Modal
```html
<div class="accessibility-panel"
     id="accessibilityPanel"
     role="dialog"
     aria-labelledby="a11y-panel-title"
     aria-hidden="true">

    <h2 id="a11y-panel-title">Accessibility Settings</h2>
    <!-- Content -->
</div>
```

---

## 3. Screen Reader Live Regions

### HTML Structure
```html
<!-- Polite announcements (don't interrupt) -->
<div class="live-region"
     role="status"
     aria-live="polite"
     aria-atomic="true"
     id="liveRegion"></div>

<!-- Assertive announcements (interrupt immediately) -->
<div class="live-region-urgent"
     role="alert"
     aria-live="assertive"
     aria-atomic="true"
     id="liveRegionUrgent"></div>
```

### CSS (Screen Reader Only)
```css
.live-region {
    position: absolute;
    left: -10000px;
    width: 1px;
    height: 1px;
    overflow: hidden;
}
```

### JavaScript Announcement System
```javascript
announce(message, priority = 'polite') {
    const liveRegion = document.getElementById('liveRegion');
    if (liveRegion) {
        liveRegion.setAttribute('aria-live', priority);
        liveRegion.textContent = message;

        // Clear after announcement for repeated messages
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 100);
    }
}

// Usage:
this.announce('Battle started');
this.announce('Critical health!', 'assertive');
this.announce('Menu opened');
```

---

## 4. Focus Management

### Visible Focus Indicators
```css
button:focus,
.menu-option:focus,
.interactive-element:focus {
    outline: 3px solid #ffcc00;
    outline-offset: 2px;
    z-index: 1000;
}

/* For elements with custom styling */
[tabindex]:focus {
    outline: 3px solid #ffcc00;
    outline-offset: 2px;
}

/* Focus within container */
.menu-option[tabindex]:focus {
    outline: 3px solid #ffcc00;
    outline-offset: -2px; /* Inset for tight containers */
}
```

### Skip Link
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

```css
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
```

### Keyboard Navigation in Menus
```javascript
setupMenuAccessibility() {
    const menu = document.getElementById('myMenu');
    const options = menu.querySelectorAll('.menu-option');

    options.forEach((option, index) => {
        // First item is focusable, others are not (but can receive focus programmatically)
        option.setAttribute('tabindex', index === 0 ? '0' : '-1');
        option.setAttribute('role', 'menuitem');

        option.addEventListener('keydown', (e) => {
            let newIndex = index;

            // Navigate with arrow keys
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                newIndex = (index + 1) % options.length;
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                newIndex = (index - 1 + options.length) % options.length;
            } else if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                option.click();
                return;
            } else if (e.key === 'Escape') {
                e.preventDefault();
                this.closeMenu();
                return;
            }

            // Move focus
            if (newIndex !== index) {
                options[newIndex].focus();
                options[newIndex].setAttribute('tabindex', '0');
                option.setAttribute('tabindex', '-1');

                // Announce to screen reader
                this.announce(options[newIndex].textContent.trim());
            }
        });
    });
}
```

---

## 5. Accessibility Settings Panel

### Complete Panel Implementation
```html
<div class="accessibility-panel" id="accessibilityPanel"
     role="dialog" aria-labelledby="a11y-panel-title" aria-hidden="true">

    <h2 id="a11y-panel-title">Accessibility Settings</h2>

    <!-- High Contrast -->
    <div class="accessibility-option">
        <input type="checkbox" id="highContrastToggle"
               aria-label="Enable high contrast mode">
        <label for="highContrastToggle">High Contrast Mode</label>
    </div>

    <!-- Reduced Motion -->
    <div class="accessibility-option">
        <input type="checkbox" id="reducedMotionToggle"
               aria-label="Enable reduced motion">
        <label for="reducedMotionToggle">Reduced Motion</label>
    </div>

    <!-- Large Text -->
    <div class="accessibility-option">
        <input type="checkbox" id="largeTextToggle"
               aria-label="Enable large text">
        <label for="largeTextToggle">Large Text (120%)</label>
    </div>

    <!-- Range Control -->
    <div class="accessibility-option">
        <label for="textSpeedRange">Text Speed:</label>
        <input type="range" id="textSpeedRange"
               min="1" max="5" value="3"
               aria-label="Adjust text display speed">
        <span id="textSpeedValue" aria-live="polite">3</span>
    </div>

    <button class="close-panel-btn"
            onclick="closeAccessibilityPanel()"
            aria-label="Close accessibility settings">Close</button>
</div>
```

### JavaScript Controller
```javascript
initializeAccessibility() {
    // Default settings
    this.accessibilitySettings = {
        highContrast: false,
        reducedMotion: false,
        largeText: false,
        textSpeed: 3
    };

    // Load saved preferences
    const saved = localStorage.getItem('app_accessibility');
    if (saved) {
        this.accessibilitySettings = JSON.parse(saved);
        this.applyAccessibilitySettings();
    }

    // High Contrast Toggle
    const highContrast = document.getElementById('highContrastToggle');
    highContrast.checked = this.accessibilitySettings.highContrast;
    highContrast.addEventListener('change', (e) => {
        this.accessibilitySettings.highContrast = e.target.checked;
        document.body.classList.toggle('high-contrast', e.target.checked);
        this.saveAccessibilitySettings();
        this.announce(e.target.checked ?
            'High contrast mode enabled' :
            'High contrast mode disabled');
    });

    // Reduced Motion Toggle
    const reducedMotion = document.getElementById('reducedMotionToggle');
    reducedMotion.checked = this.accessibilitySettings.reducedMotion;
    reducedMotion.addEventListener('change', (e) => {
        this.accessibilitySettings.reducedMotion = e.target.checked;
        document.body.classList.toggle('reduced-motion', e.target.checked);
        this.saveAccessibilitySettings();
        this.announce(e.target.checked ?
            'Reduced motion enabled' :
            'Reduced motion disabled');
    });

    // Text Speed Range
    const textSpeed = document.getElementById('textSpeedRange');
    const textSpeedValue = document.getElementById('textSpeedValue');
    textSpeed.value = this.accessibilitySettings.textSpeed;
    textSpeedValue.textContent = this.accessibilitySettings.textSpeed;
    textSpeed.addEventListener('input', (e) => {
        this.accessibilitySettings.textSpeed = parseInt(e.target.value);
        textSpeedValue.textContent = e.target.value;
        this.saveAccessibilitySettings();
        this.announce('Text speed set to ' + e.target.value);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key.toLowerCase() === 'a') {
            e.preventDefault();
            this.toggleAccessibilityPanel();
        }

        if (e.key === 'Escape') {
            const panel = document.getElementById('accessibilityPanel');
            if (panel && panel.classList.contains('active')) {
                this.toggleAccessibilityPanel();
            }
        }
    });
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
        // Focus first control
        document.getElementById('highContrastToggle').focus();
        this.announce('Accessibility settings opened');
    }
}

saveAccessibilitySettings() {
    localStorage.setItem('app_accessibility',
        JSON.stringify(this.accessibilitySettings));
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
```

---

## 6. High Contrast Mode

### CSS Implementation
```css
/* High Contrast Mode */
body.high-contrast {
    background: #000;
}

body.high-contrast .container {
    background: #fff;
    border: 4px solid #000;
}

body.high-contrast .button {
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

body.high-contrast .text-box:focus {
    outline: 3px solid #ffcc00;
}
```

---

## 7. Reduced Motion Support

### CSS Implementation
```css
/* Respect user's motion preference */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Manual toggle */
body.reduced-motion * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
}

/* Alternative: disable specific animations */
body.reduced-motion .animated-element {
    animation: none;
    transition: none;
}
```

---

## 8. Large Text Mode

### CSS Implementation
```css
body.large-text {
    font-size: 120%;
}

body.large-text .text-content,
body.large-text .menu-option {
    font-size: 18px;
}

body.large-text .button {
    font-size: 16px;
    padding: 18px 24px;
}

body.large-text .small-text {
    font-size: 14px;
}
```

---

## 9. Screen Reader Only Content

### CSS Class for Hidden Context
```css
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
```

### Usage
```html
<button>
    <span aria-hidden="true">⚙️</span>
    <span class="sr-only">Settings</span>
</button>

<div class="progress-bar" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
    <div class="progress-fill" style="width: 75%"></div>
    <span class="sr-only">Loading: 75% complete</span>
</div>
```

---

## 10. Game State Announcements

### Property Observer Pattern
```javascript
announceGameState() {
    // Store original state internally
    Object.defineProperty(this, '_state', {
        writable: true,
        value: this.state
    });

    // Create getter/setter to intercept changes
    Object.defineProperty(this, 'state', {
        get() {
            return this._state;
        },
        set(newState) {
            const oldState = this._state;
            this._state = newState;

            // Announce state change
            if (this.accessibilitySettings.enhancedAnnouncements &&
                oldState !== newState) {
                switch (newState) {
                    case 'MENU':
                        this.announce('Menu opened');
                        break;
                    case 'BATTLE':
                        this.announce('Battle started');
                        break;
                    case 'VICTORY':
                        this.announce('Victory! You won the battle!');
                        break;
                    case 'GAME_OVER':
                        this.announce('Game over', 'assertive');
                        break;
                }
            }
        }
    });
}
```

---

## 11. Color Contrast Validation

### JavaScript Function to Check Contrast
```javascript
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function relativeLuminance(rgb) {
    const adjust = (val) => {
        val = val / 255.0;
        return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    };

    return 0.2126 * adjust(rgb.r) +
           0.7152 * adjust(rgb.g) +
           0.0722 * adjust(rgb.b);
}

function contrastRatio(color1, color2) {
    const lum1 = relativeLuminance(hexToRgb(color1));
    const lum2 = relativeLuminance(hexToRgb(color2));

    const lighter = Math.max(lum1, lum2);
    const darker = Math.min(lum1, lum2);

    return (lighter + 0.05) / (darker + 0.05);
}

function meetsWCAG(foreground, background, level = 'AA', size = 'normal') {
    const ratio = contrastRatio(foreground, background);

    if (level === 'AAA') {
        return size === 'large' ? ratio >= 4.5 : ratio >= 7.0;
    }
    // AA level
    return size === 'large' ? ratio >= 3.0 : ratio >= 4.5;
}

// Usage:
console.log(meetsWCAG('#ffffff', '#4a5a3a')); // true
console.log(contrastRatio('#ffffff', '#4a5a3a')); // 9.51
```

---

## 12. Accessible Form Controls

### Text Input
```html
<label for="playerName">Player Name:</label>
<input type="text"
       id="playerName"
       name="playerName"
       aria-required="true"
       aria-describedby="nameHelp">
<span id="nameHelp" class="help-text">
    Enter your character name (3-12 characters)
</span>
```

### Checkbox
```html
<input type="checkbox"
       id="agreeTerms"
       aria-describedby="termsText">
<label for="agreeTerms">I agree to the terms and conditions</label>
<span id="termsText" class="sr-only">
    You must agree to continue
</span>
```

### Radio Buttons
```html
<fieldset>
    <legend>Choose difficulty:</legend>
    <div>
        <input type="radio" id="easy" name="difficulty" value="easy">
        <label for="easy">Easy - For beginners</label>
    </div>
    <div>
        <input type="radio" id="normal" name="difficulty" value="normal" checked>
        <label for="normal">Normal - Balanced experience</label>
    </div>
    <div>
        <input type="radio" id="hard" name="difficulty" value="hard">
        <label for="hard">Hard - For veterans</label>
    </div>
</fieldset>
```

---

## 13. Testing Checklist

### Manual Testing Steps
```javascript
// 1. Keyboard Navigation Test
document.addEventListener('keydown', (e) => {
    console.log('Key pressed:', e.key);
    console.log('Active element:', document.activeElement);
});

// 2. Focus Indicator Test
const focusable = document.querySelectorAll('button, [tabindex], a, input, select');
focusable.forEach(el => {
    el.addEventListener('focus', () => {
        console.log('Focused:', el.tagName, el.className, el.getAttribute('aria-label'));
    });
});

// 3. ARIA Validation
const validateARIA = () => {
    const interactive = document.querySelectorAll('button, [role="button"], [role="menuitem"]');
    interactive.forEach(el => {
        if (!el.getAttribute('aria-label') && !el.textContent.trim()) {
            console.warn('Missing label:', el);
        }
    });
};

// 4. Contrast Check
const checkContrast = (fg, bg) => {
    const ratio = contrastRatio(fg, bg);
    console.log(`Contrast ratio: ${ratio.toFixed(2)}:1`,
                ratio >= 4.5 ? '✓ PASS' : '✗ FAIL');
};
```

---

## Best Practices Summary

1. **Always provide ARIA labels** for interactive elements
2. **Use semantic HTML** first, ARIA roles second
3. **Make everything keyboard accessible** (Tab, Enter, Space, Arrow keys, Escape)
4. **Provide visible focus indicators** (3px outline minimum)
5. **Announce state changes** to screen readers
6. **Meet WCAG contrast ratios** (4.5:1 for normal text, 3:1 for large text)
7. **Respect user preferences** (prefers-reduced-motion, prefers-color-scheme)
8. **Test with actual assistive technologies**
9. **Persist accessibility settings** in localStorage
10. **Document all keyboard shortcuts**

---

## Resources

- **WCAG Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices:** https://www.w3.org/WAI/ARIA/apg/
- **Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Screen Reader Testing:** https://www.nvaccess.org/ (NVDA)

---

**Remember:** Accessibility is not a feature, it's a requirement. Start with semantic HTML, add ARIA where needed, and always test with real users and assistive technologies.
