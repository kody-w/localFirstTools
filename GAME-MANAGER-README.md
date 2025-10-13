# Game Manager System Documentation

A comprehensive game management system for launching, managing favorites, filtering, and organizing games in a local-first application environment.

## Features

- **StateManager Class**: Centralized state management with localStorage persistence
- **GameManager Class**: Complete game lifecycle management
- **Event Delegation**: Efficient event handling for all button clicks
- **Async Game Loading**: Proper async/await handling for game resources
- **Multiple Game Types**: Support for embedded, iframe, and local blob-based games
- **Favorites System**: Add/remove games from favorites with UI updates
- **Filtering**: Filter by view (store/library), category, and search query
- **Game Details Modal**: View detailed information before launching
- **Emulator Container**: Fullscreen game player with close functionality
- **localStorage Sync**: Automatic state persistence across sessions

## Architecture

### StateManager

Manages application state with automatic localStorage persistence.

```javascript
class StateManager {
    state = {
        installedGames: Set,      // Games marked as installed
        favorites: Set,            // Favorited games
        currentView: String,       // 'store' or 'library'
        currentCategory: String,   // Current category filter
        searchQuery: String,       // Current search query
        currentGame: String,       // Currently playing game ID
        gameHistory: Array         // Recently played games
    }
}
```

**Key Methods:**
- `loadState()` - Load state from localStorage
- `saveState()` - Save state to localStorage
- `subscribe(event, callback)` - Subscribe to state changes
- `emit(event, data)` - Emit state change events
- `updateState(updates)` - Update state and trigger saves
- `getState()` - Get current state snapshot

### GameManager

Manages game library, launching, filtering, and UI interactions.

```javascript
class GameManager {
    constructor(stateManager, gameLibrary)
}
```

**Key Methods:**

#### Game Launching
- `launchGame(gameId)` - Launch a game (marks as installed, creates blob URLs, shows emulator)
- `launchLocalGame(game)` - Launch game from local HTML content or blob
- `launchIframeGame(game)` - Launch game in iframe
- `launchEmbeddedGame(game)` - Launch embedded canvas/renderer game
- `closeEmulator()` - Close emulator, cleanup resources

#### Game Details
- `showGameDetails(gameId)` - Open modal with game information
- `closeModal()` - Close all modals

#### Favorites
- `toggleFavorite(gameId)` - Add/remove from favorites, update UI, save to storage
- `updateFavoriteButton(gameId, isFavorite)` - Update specific button UI

#### Filtering
- `filterGames()` - Filter games by view, category, and search query
- `updateViewCounts()` - Update visible game count display

#### Rendering
- `renderGameCard(game)` - Create DOM element for game card
- `renderAllGames()` - Render all games in library

#### Library Management
- `addGame(game)` - Add game to library
- `removeGame(gameId)` - Remove game from library
- `getGameById(gameId)` - Get single game
- `getAllGames()` - Get all games
- `getInstalledGames()` - Get only installed games
- `getFavoriteGames()` - Get only favorited games

## Usage

### Basic Setup

```javascript
// Initialize state manager
const stateManager = new StateManager();

// Initialize game manager with game library
const gameManager = new GameManager(stateManager, gameLibrary);

// Render all games
gameManager.renderAllGames();
```

### Game Object Structure

```javascript
const game = {
    id: 'unique-game-id',           // Required: unique identifier
    name: 'Game Name',              // Required: display name
    description: 'Description...',  // Optional: game description
    icon: '🎮',                     // Optional: emoji or image
    category: 'action',             // Optional: category for filtering
    rating: 4.5,                    // Optional: rating (0-5)
    plays: 100,                     // Optional: play count
    type: 'embedded',               // Required: 'embedded', 'iframe', or 'local'

    // For embedded games:
    initialize: function(display) { /* setup */ },
    update: function(deltaTime) { /* game loop */ },
    render: function() { /* rendering */ },
    handleInput: function(button, isPressed) { /* input */ },
    cleanup: function() { /* cleanup */ },

    // For iframe games:
    url: 'https://example.com/game.html',

    // For local games:
    htmlContent: '<html>...</html>',  // or use url with blob
};
```

### Event Delegation

All button clicks are handled through event delegation:

```javascript
setupEventDelegation() {
    this.gamesGrid.addEventListener('click', (e) => {
        const gameCard = e.target.closest('.game-card');
        const gameId = gameCard.dataset.gameId;

        // Handle different button types
        if (target.closest('.play-button')) {
            this.launchGame(gameId);
        }
        else if (target.closest('.favorite-button')) {
            this.toggleFavorite(gameId);
        }
        else {
            this.showGameDetails(gameId);
        }
    });
}
```

### State Management

```javascript
// Subscribe to state changes
stateManager.subscribe('stateChanged', (state) => {
    console.log('State updated:', state);
});

// Update state
stateManager.updateState({
    currentView: 'library',
    currentCategory: 'action'
});

// Get current state
const state = stateManager.getState();
console.log('Installed games:', state.installedGames);
console.log('Favorites:', state.favorites);
```

### Launching Games

```javascript
// Launch a game by ID
await gameManager.launchGame('snake-game');

// The game will:
// 1. Mark as installed in state
// 2. Create blob URL if needed (for local games)
// 3. Set iframe src or initialize embedded game
// 4. Show emulator container
// 5. Add to play history
```

### Filtering Games

```javascript
// Filter by view
stateManager.updateState({ currentView: 'library' }); // Only installed

// Filter by category
stateManager.updateState({ currentCategory: 'action' });

// Search
stateManager.updateState({ searchQuery: 'snake' });

// Favorites only
stateManager.updateState({ currentCategory: 'favorites' });

// Filtering is automatic - no manual call needed
```

### Managing Favorites

```javascript
// Toggle favorite
gameManager.toggleFavorite('snake-game');

// Get all favorites
const favorites = gameManager.getFavoriteGames();

// Check if favorited
const state = stateManager.getState();
const isFavorited = state.favorites.has('snake-game');
```

## HTML Structure Requirements

### Required DOM Elements

```html
<!-- Game grid container -->
<div id="games-grid"></div>

<!-- Emulator container -->
<div id="emulator-container">
    <button id="close-emulator">Close</button>
    <iframe id="game-iframe"></iframe>
    <div id="game-display"></div>
</div>

<!-- Modal overlay -->
<div id="modal-overlay">
    <div id="game-details-modal" class="modal">
        <button class="close-modal">&times;</button>
        <div id="modal-game-icon"></div>
        <div id="modal-game-title"></div>
        <div id="modal-game-description"></div>
        <div id="modal-game-category"></div>
        <div id="modal-game-rating"></div>
        <div id="modal-game-plays"></div>
        <button id="play-from-modal">Play</button>
    </div>
</div>

<!-- Filter controls -->
<select id="view-toggle">
    <option value="store">Store</option>
    <option value="library">Library</option>
</select>

<select id="category-filter">
    <option value="all">All</option>
    <option value="favorites">Favorites</option>
    <!-- Add more categories -->
</select>

<input type="text" id="search-input" placeholder="Search...">

<div id="visible-games-count"></div>
```

### Game Card Structure

```html
<div class="game-card" data-game-id="unique-id">
    <div class="game-icon">🎮</div>
    <div class="game-info">
        <h3 class="game-name">Game Name</h3>
        <p class="game-description">Description...</p>
        <div class="game-meta">
            <span class="game-category">Category</span>
            <span class="game-rating">⭐ 4.5</span>
        </div>
    </div>
    <div class="game-actions">
        <button class="play-button">▶️ Play</button>
        <button class="favorite-button">🤍</button>
    </div>
    <span class="installed-badge">Installed</span>
</div>
```

## Advanced Features

### Game History

```javascript
// Automatically tracked when launching games
addToHistory(gameId) {
    const history = state.gameHistory;
    history.unshift(gameId);
    if (history.length > 10) history.pop();
}

// Get recent games
const recent = stateManager.getState().gameHistory
    .map(id => gameManager.getGameById(id));
```

### Blob URL Management

```javascript
// Automatically creates and tracks blob URLs
launchLocalGame(game) {
    const blob = new Blob([game.htmlContent], { type: 'text/html' });
    const blobUrl = URL.createObjectURL(blob);
    this.blobUrls.set(game.id, blobUrl);
    this.gameIframe.src = blobUrl;
}

// Automatically cleaned up on close
closeEmulator() {
    this.blobUrls.forEach(url => URL.revokeObjectURL(url));
    this.blobUrls.clear();
}
```

### Custom Event Handlers

```javascript
// Subscribe to specific events
stateManager.subscribe('gameInstalled', (gameId) => {
    console.log('Game installed:', gameId);
});

// Emit custom events
stateManager.emit('gameInstalled', gameId);
```

### Cleanup

```javascript
// Proper cleanup when destroying
gameManager.destroy();
// - Closes emulator
// - Cleans up blob URLs
// - Removes event listeners
// - Clears state listeners
```

## Error Handling

All methods include proper error handling:

```javascript
async launchGame(gameId) {
    try {
        const game = this.gameLibrary[gameId];
        if (!game) throw new Error(`Game ${gameId} not found`);

        // Launch logic...

    } catch (error) {
        console.error('Error launching game:', error);
        alert(`Failed to launch game: ${error.message}`);
    }
}
```

## localStorage Schema

```javascript
{
    "retroplay_state": {
        "installedGames": ["game-id-1", "game-id-2"],
        "favorites": ["game-id-1"],
        "currentView": "store",
        "currentCategory": "all",
        "gameHistory": ["game-id-1", "game-id-2"]
    }
}
```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires ES6+ support (classes, async/await, Set, Map)
- localStorage API
- Blob API for local game loading
- iframe sandbox support

## Performance Considerations

- **Event Delegation**: Single listener for all game cards
- **Lazy Loading**: Games only initialized when launched
- **Blob URLs**: Properly cleaned up to prevent memory leaks
- **Filtered Rendering**: Only visible cards are shown (display: none)
- **State Caching**: State changes batched and saved efficiently

## Security

- **iframe Sandbox**: Restricts iframe capabilities
- **Blob URLs**: Temporary, revoked after use
- **localStorage**: All data stored locally, no server calls
- **XSS Protection**: Game content isolated in iframes

## Example Integration

See `game-manager-demo.html` for a complete working example with:
- Sample game library
- Full UI implementation
- Styled components
- Keyboard shortcuts
- Debug logging

## Troubleshooting

### Games not appearing
- Check that `renderAllGames()` is called after initialization
- Verify game objects have required `id` and `name` properties
- Check browser console for errors

### Favorites not persisting
- Ensure `stateManager.saveState()` is being called
- Check localStorage quota (may be full)
- Verify localStorage is enabled in browser

### Filtering not working
- Ensure filter elements have correct IDs
- Check that `setupEventDelegation()` is called
- Verify `filterGames()` is triggered on state changes

### Games won't launch
- Check game `type` property is set correctly
- For iframe games, verify `url` is accessible
- For local games, verify `htmlContent` or blob creation
- Check browser console for security/CORS errors

## API Reference

### StateManager API

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `loadState()` | - | void | Load from localStorage |
| `saveState()` | - | void | Save to localStorage |
| `subscribe(event, callback)` | event: string, callback: function | void | Subscribe to events |
| `emit(event, data)` | event: string, data: any | void | Emit event |
| `updateState(updates)` | updates: object | void | Update state |
| `getState()` | - | object | Get state copy |

### GameManager API

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `launchGame(gameId)` | gameId: string | Promise<void> | Launch game |
| `closeEmulator()` | - | void | Close emulator |
| `showGameDetails(gameId)` | gameId: string | void | Show modal |
| `closeModal()` | - | void | Close modal |
| `toggleFavorite(gameId)` | gameId: string | void | Toggle favorite |
| `filterGames()` | - | void | Apply filters |
| `renderGameCard(game)` | game: object | HTMLElement | Create card |
| `renderAllGames()` | - | void | Render library |
| `addGame(game)` | game: object | void | Add to library |
| `removeGame(gameId)` | gameId: string | void | Remove from library |
| `getGameById(gameId)` | gameId: string | object | Get game |
| `getAllGames()` | - | array | Get all games |
| `getInstalledGames()` | - | array | Get installed |
| `getFavoriteGames()` | - | array | Get favorites |
| `destroy()` | - | void | Cleanup |

## License

This is part of the localFirstTools project. See main repository for license information.
