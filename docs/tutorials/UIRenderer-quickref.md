# UIRenderer Quick Reference

## Methods

### renderCategories(categories, activeCategory)
```javascript
UIRenderer.renderCategories(['all', 'action', 'puzzle'], 'all');
```
- Renders category filter tabs
- Highlights active category
- Adds ARIA attributes

### renderGames(games, favorites, installed)
```javascript
const games = [{ id, name, icon, description, size, category }];
const favorites = new Set(['game1']);
const installed = new Set(['game1', 'game2']);

UIRenderer.renderGames(games, favorites, installed);
```
- Renders game cards in grid
- Shows "No games found" if empty
- Play button shows "Play" if installed, "Install" otherwise
- Cards clickable for details

### renderGameDetail(game, isFavorite)
```javascript
UIRenderer.renderGameDetail(game, true);
```
- Renders game details in modal
- Shows Play Now and Favorite buttons
- Displays metadata (author, version, etc.)

### updateControlsFooter(inputMode)
```javascript
UIRenderer.updateControlsFooter('gamepad');  // or 'keyboard', 'mouse', 'touch'
```
- Updates control hints based on input mode

### showToast(message, duration = 3000)
```javascript
UIRenderer.showToast('Game installed!');
UIRenderer.showToast('Error occurred', 5000);
```
- Shows notification toast
- Auto-dismisses after duration

### hideToast()
```javascript
UIRenderer.hideToast();
```
- Manually hide toast

## HTML Requirements

```html
<!-- Categories -->
<div id="categoryTabs"></div>

<!-- Games Grid -->
<div id="gamesGrid"></div>

<!-- Game Detail Modal -->
<div id="gameDetailContent"></div>

<!-- Controls Footer -->
<div id="controlsFooter"></div>

<!-- Toast -->
<div id="toast"></div>
```

## CSS Classes

- `.category-tab` - Category button
- `.category-tab.active` - Active category
- `.game-card` - Game card container
- `.game-icon` - Game emoji icon
- `.game-title` - Game title
- `.game-description` - Game description
- `.game-meta` - Meta container (size + button)
- `.game-size` - Size text
- `.play-button` - Play/Install button
- `.no-games` - Empty state container
- `.no-games-icon` - Empty state icon
- `.no-games-text` - Empty state text
- `.control-hint` - Control hint container
- `.button-icon` - Control button icon
- `.toast` - Toast notification
- `.toast.show` - Visible toast

## Data Attributes

- `data-category="category-name"` - On category tabs
- `data-game-id="game-id"` - On game cards and buttons
- `data-action="launch"` - On play buttons
- `data-action="launch-detail"` - On modal play button
- `data-action="toggle-favorite"` - On favorite button
- `data-action="close-modal"` - On modal close button

## Features

✅ Modern DOM manipulation (createElement only)
✅ No innerHTML for dynamic content
✅ Performance optimized (DocumentFragment)
✅ Full accessibility (ARIA attributes)
✅ Empty state handling
✅ Dynamic button text (Play/Install)
✅ Multi-input mode support
✅ Toast notifications
✅ Modal integration
✅ Event delegation friendly

## Example Workflow

```javascript
// 1. Setup categories
UIRenderer.renderCategories(['all', 'action', 'puzzle'], 'all');

// 2. Load and render games
const games = await fetchGames();
const favorites = new Set(loadFavorites());
const installed = new Set(loadInstalled());
UIRenderer.renderGames(games, favorites, installed);

// 3. Update controls
UIRenderer.updateControlsFooter('mouse');

// 4. Show notification
UIRenderer.showToast('Welcome!');

// 5. When user clicks game card
// (handled by event delegation)
// UIRenderer.renderGameDetail(game, isFavorite);
```

## Files

1. **UIRenderer-clean.js** (377 lines)
   Clean implementation ready to use

2. **UIRenderer-documentation.js** (618 lines)
   Full documentation with 7 examples

3. **UIRenderer-summary.md** (252 lines)
   Complete implementation guide

4. **steamdeck-game-store.html** (lines 1267-1642)
   Integrated in main application
