# UIRenderer - Modern UI Rendering System

## Overview

A production-ready UI rendering system for game stores and similar applications. Built with modern JavaScript, using pure DOM manipulation for security, performance, and maintainability.

## Key Features

- ✅ **Security**: No `innerHTML` for dynamic content - prevents XSS attacks
- ✅ **Performance**: Uses `DocumentFragment` for batch DOM updates
- ✅ **Accessibility**: Full ARIA support for screen readers
- ✅ **Empty States**: Graceful handling when no content available
- ✅ **Modern DOM**: Uses `createElement()` and modern APIs
- ✅ **Event Delegation**: Works seamlessly with delegated events
- ✅ **Type Safe**: JSDoc annotations for better IDE support
- ✅ **Zero Dependencies**: Pure vanilla JavaScript

## Quick Start

### Installation

Copy `UIRenderer-clean.js` (377 lines) into your project:

```javascript
// Include in your HTML
<script src="UIRenderer-clean.js"></script>

// Or import as module
import { UIRenderer } from './UIRenderer-clean.js';
```

### Basic Usage

```javascript
// 1. Render categories
UIRenderer.renderCategories(['all', 'action', 'puzzle'], 'all');

// 2. Render games
const games = [
    {
        id: 'tetris',
        name: 'Tetris',
        icon: '🧱',
        description: 'Classic puzzle game',
        size: '8 KB'
    }
];
UIRenderer.renderGames(games, new Set(['tetris']), new Set());

// 3. Show notification
UIRenderer.showToast('Welcome to Game Store!');
```

## API Reference

### renderCategories(categories, activeCategory)

Renders category filter tabs with active state management.

**Parameters:**
- `categories` (Array<string>): List of category names
- `activeCategory` (string): Currently active category

**Example:**
```javascript
UIRenderer.renderCategories(
    ['all', 'action', 'puzzle', 'arcade', 'strategy'],
    'all'
);
```

**Generated HTML:**
```html
<button class="category-tab active" data-category="all" role="tab" aria-selected="true">
    All
</button>
```

---

### renderGames(games, favorites, installed)

Renders game cards in a grid layout. Handles empty states automatically.

**Parameters:**
- `games` (Array<Game>): Array of game objects
- `favorites` (Set): Set of favorited game IDs
- `installed` (Set): Set of installed game IDs

**Game Object:**
```javascript
{
    id: string,
    name: string,
    icon: string,        // emoji or image
    description: string,
    size: string,        // e.g., "8 KB"
    category: string
}
```

**Example:**
```javascript
const games = [
    {
        id: 'snake',
        name: 'Snake Classic',
        icon: '🐍',
        description: 'Eat food and grow longer!',
        size: '5 KB',
        category: 'arcade'
    }
];

const favorites = new Set(['snake']);
const installed = new Set(['snake']);

UIRenderer.renderGames(games, favorites, installed);
```

**Empty State:**
When `games.length === 0`, displays:
```html
<div class="no-games">
    <div class="no-games-icon">🎮</div>
    <div class="no-games-text">No games found</div>
</div>
```

---

### renderGameDetail(game, isFavorite)

Renders detailed game view in a modal.

**Parameters:**
- `game` (Game): Game object
- `isFavorite` (boolean): Whether game is favorited

**Example:**
```javascript
const game = {
    id: 'tetris',
    name: 'Tetris',
    icon: '🧱',
    description: 'The classic block-stacking puzzle game',
    category: 'puzzle',
    size: '8 KB',
    author: 'Built-in',
    version: '1.0'
};

UIRenderer.renderGameDetail(game, true);
```

**Features:**
- Large game icon display
- Play Now button
- Favorite toggle (★/☆)
- Metadata display (author, version, category, size)
- Responsive layout

---

### updateControlsFooter(inputMode)

Updates control hints based on current input method.

**Parameters:**
- `inputMode` (string): One of 'gamepad', 'keyboard', 'mouse', 'touch'

**Example:**
```javascript
UIRenderer.updateControlsFooter('gamepad');
```

**Control Schemes:**

| Mode | Hints |
|------|-------|
| `gamepad` | A (Select), B (Back), X (Details), Y (Favorite) |
| `keyboard` | ↵ (Select), ESC (Back), ↑↓ (Navigate), F (Favorite) |
| `mouse` | 🖱️ (Click to Select), ↻ (Scroll to Browse) |
| `touch` | 👆 (Tap to Select), 📱 (Swipe to Scroll) |

---

### showToast(message, duration = 3000)

Shows a toast notification with auto-dismiss.

**Parameters:**
- `message` (string): Message to display
- `duration` (number): Duration in milliseconds (default: 3000)

**Examples:**
```javascript
// Success message
UIRenderer.showToast('Game installed successfully!');

// Error with longer duration
UIRenderer.showToast('Failed to load game', 5000);

// Info message
UIRenderer.showToast('Added to favorites');
```

**Features:**
- Auto-dismiss after duration
- ARIA live region for accessibility
- Smooth CSS animations
- Multiple toasts handled gracefully

---

### hideToast()

Manually hide the current toast notification.

**Example:**
```javascript
UIRenderer.hideToast();
```

---

## HTML Requirements

Your HTML must include these elements:

```html
<!-- Category Tabs Container -->
<div id="categoryTabs"></div>

<!-- Games Grid Container -->
<div id="gamesGrid"></div>

<!-- Game Detail Modal Content -->
<div class="modal" id="gameDetailModal">
    <div class="modal-content">
        <button class="close-modal" data-action="close-modal">✕</button>
        <div id="gameDetailContent"></div>
    </div>
</div>

<!-- Controls Footer -->
<footer id="controlsFooter"></footer>

<!-- Toast Notification -->
<div id="toast"></div>
```

## CSS Classes

You need to define these CSS classes:

### Category Tabs
- `.category-tab` - Base category button style
- `.category-tab.active` - Active category highlight

### Game Cards
- `.game-card` - Card container
- `.game-icon` - Icon/emoji display
- `.game-title` - Game title (h3)
- `.game-description` - Description text
- `.game-meta` - Metadata container
- `.game-size` - Size display
- `.play-button` - Play/Install button

### Empty State
- `.no-games` - Empty state container
- `.no-games-icon` - Empty state icon
- `.no-games-text` - Empty state text

### Controls
- `.control-hint` - Control hint container
- `.button-icon` - Button icon display

### Toast
- `.toast` - Toast container
- `.toast.show` - Visible state

### Modal
- `.modal` - Modal overlay
- `.modal.show` - Visible state
- `.modal-content` - Modal content
- `.close-modal` - Close button
- `.nav-button` - Secondary button style

## Integration Example

### Complete Workflow

```javascript
class GameStore {
    constructor() {
        this.games = [];
        this.favorites = new Set();
        this.installed = new Set();
        this.currentCategory = 'all';
        this.inputMode = 'mouse';

        this.init();
    }

    async init() {
        // Load data
        await this.loadGames();
        this.favorites = new Set(this.loadFromStorage('favorites'));
        this.installed = new Set(this.loadFromStorage('installed'));

        // Render UI
        this.renderUI();

        // Setup event listeners
        this.setupEventListeners();
    }

    renderUI() {
        // Categories
        const categories = ['all', 'action', 'puzzle', 'arcade', 'strategy'];
        UIRenderer.renderCategories(categories, this.currentCategory);

        // Games
        const filteredGames = this.filterGames();
        UIRenderer.renderGames(filteredGames, this.favorites, this.installed);

        // Controls
        UIRenderer.updateControlsFooter(this.inputMode);

        // Welcome message
        UIRenderer.showToast('Welcome to Game Store!');
    }

    setupEventListeners() {
        // Category clicks
        document.getElementById('categoryTabs').addEventListener('click', (e) => {
            if (e.target.classList.contains('category-tab')) {
                this.currentCategory = e.target.dataset.category;
                this.renderUI();
            }
        });

        // Game card clicks
        document.getElementById('gamesGrid').addEventListener('click', (e) => {
            const card = e.target.closest('.game-card');
            if (card && !e.target.closest('.play-button')) {
                const gameId = card.dataset.gameId;
                this.showGameDetail(gameId);
            }
        });

        // Play button clicks
        document.addEventListener('click', (e) => {
            if (e.target.dataset.action === 'launch') {
                this.launchGame(e.target.dataset.gameId);
            }
        });

        // Input mode detection
        document.addEventListener('mousemove', () => {
            if (this.inputMode !== 'mouse') {
                this.inputMode = 'mouse';
                UIRenderer.updateControlsFooter('mouse');
            }
        });
    }

    showGameDetail(gameId) {
        const game = this.games.find(g => g.id === gameId);
        const isFavorite = this.favorites.has(gameId);
        UIRenderer.renderGameDetail(game, isFavorite);
        document.getElementById('gameDetailModal').classList.add('show');
    }

    launchGame(gameId) {
        this.installed.add(gameId);
        this.saveToStorage('installed', Array.from(this.installed));
        UIRenderer.showToast('Launching game...');
        this.renderUI();
    }

    filterGames() {
        let filtered = this.games;
        if (this.currentCategory !== 'all') {
            filtered = filtered.filter(g => g.category === this.currentCategory);
        }
        return filtered;
    }
}

// Initialize
new GameStore();
```

## Best Practices

### 1. Performance
```javascript
// Good: Uses DocumentFragment
const fragment = document.createDocumentFragment();
items.forEach(item => {
    const el = createElement(item);
    fragment.appendChild(el);
});
container.appendChild(fragment);  // Single reflow

// Bad: Multiple reflows
items.forEach(item => {
    const el = createElement(item);
    container.appendChild(el);  // Reflow each time
});
```

### 2. Security
```javascript
// Good: Uses textContent
element.textContent = userInput;  // Safe

// Bad: Uses innerHTML
element.innerHTML = userInput;  // XSS vulnerability
```

### 3. Accessibility
```javascript
// Good: ARIA attributes
button.setAttribute('aria-label', 'Play Tetris');
button.setAttribute('role', 'button');

// Bad: No accessibility
button.textContent = 'Play';
```

### 4. Event Delegation
```javascript
// Good: Delegate on parent
document.getElementById('gamesGrid').addEventListener('click', (e) => {
    const card = e.target.closest('.game-card');
    if (card) handleCardClick(card);
});

// Bad: Listener on each card
cards.forEach(card => {
    card.addEventListener('click', handleCardClick);
});
```

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Full support

Requires ES6+ support (2015+).

## Files in This Package

1. **UIRenderer-clean.js** (377 lines)
   - Production-ready implementation
   - Minimal comments, clean code
   - Copy this into your project

2. **UIRenderer-documentation.js** (618 lines)
   - Full documentation with examples
   - 7 complete usage examples
   - Development reference

3. **UIRenderer-summary.md** (252 lines)
   - Implementation guide
   - Feature descriptions
   - Integration notes

4. **UIRenderer-quickref.md** (103 lines)
   - Quick reference card
   - Method signatures
   - Common patterns

5. **UIRenderer-README.md** (this file)
   - Complete documentation
   - API reference
   - Best practices

## Live Example

See the complete implementation in action:
- **File**: `/Users/kodyw/Documents/GitHub/localFirstTools3/steamdeck-game-store.html`
- **Lines**: 1267-1642

Open in a browser to test all features.

## License

Free to use for any purpose. No attribution required.

## Contributing

This is a self-contained implementation. To modify:

1. Edit the UIRenderer class
2. Maintain the public API
3. Keep using createElement() (no innerHTML)
4. Add JSDoc comments
5. Update examples

## Support

For issues or questions, refer to:
- API Reference (above)
- Usage Examples (UIRenderer-documentation.js)
- Quick Reference (UIRenderer-quickref.md)

## Version

**v1.0.0** - Initial release
- All core features implemented
- Production ready
- Fully tested

## Changelog

### v1.0.0 (2025-10-12)
- Initial release
- renderCategories() method
- renderGames() method with empty state
- renderGameDetail() method
- updateControlsFooter() method
- showToast() method
- hideToast() method
- Full accessibility support
- DocumentFragment optimization
- Event delegation support
