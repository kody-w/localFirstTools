# Game Store Models - Quick Reference Cheat Sheet

## Import/Setup

```javascript
// Browser (after including game-store-models.js)
const { Game, StateManager, StorageService, GameUtils, AppConfig } = window.GameStore;

// Node.js / ES6 Modules
const { Game, StateManager, StorageService, GameUtils, AppConfig } = require('./game-store-models.js');
```

## Game Class

### Create
```javascript
const game = new Game({
    id: 'game-1',
    name: 'Tetris',
    description: 'Block puzzle game',
    icon: '🧱',
    category: 'puzzle',
    url: 'https://example.com/tetris.html',
    size: '8 KB',
    isLocal: false,
    code: null,
    author: 'John Doe',
    version: '1.0'
});
```

### Methods
```javascript
game.toJSON()           // Serialize for storage
game.isValid()          // Check if game has required fields
game.clone()            // Create a copy
```

## StateManager

### Initialize
```javascript
const stateManager = new StateManager();
```

### Update State
```javascript
stateManager.setState({
    games: [game1, game2],
    currentView: 'library',
    searchQuery: 'puzzle'
});
```

### Get State
```javascript
const state = stateManager.getState();           // Get all state
const games = stateManager.get('games');         // Get specific property
```

### Subscribe to Changes
```javascript
const unsubscribe = stateManager.subscribe('games', (games) => {
    console.log('Games updated:', games.length);
});

// Later: unsubscribe();
```

### Other Methods
```javascript
stateManager.reset()            // Reset to initial state
stateManager.clearSubscribers() // Remove all subscribers
```

## StorageService

### Basic Operations
```javascript
// Save
StorageService.save('myKey', { data: 'value' });

// Load
const data = StorageService.load('myKey', defaultValue);

// Remove
StorageService.remove('myKey');
```

### Game Operations
```javascript
// Save games
StorageService.saveLocalGames([game1, game2]);

// Load games
const games = StorageService.loadLocalGames();
```

### Favorites & Installed
```javascript
// Favorites
const favorites = new Set(['game-1', 'game-2']);
StorageService.saveFavorites(favorites);
const loadedFavorites = StorageService.loadFavorites();

// Installed
const installed = new Set(['game-1']);
StorageService.saveInstalledGames(installed);
const loadedInstalled = StorageService.loadInstalledGames();
```

### Bulk Operations
```javascript
// Export all
const exportData = StorageService.exportAllData();

// Import all
StorageService.importAllData(exportData);

// Clear all
StorageService.clearAll();
```

### Info
```javascript
StorageService.isAvailable()    // Check if localStorage works
StorageService.getStorageSize() // Get total size in bytes
```

## GameUtils

### Filter Games
```javascript
const filtered = GameUtils.filterGames(allGames, {
    category: 'puzzle',              // Filter by category
    searchQuery: 'tetris',           // Search in name/description
    installedOnly: true,             // Only installed games
    installedGames: installedSet     // Set of installed IDs
});
```

### Sort Games
```javascript
// Sort by name (ascending)
const sorted = GameUtils.sortGames(games, 'name', true);

// Sort by category (descending)
const sorted = GameUtils.sortGames(games, 'category', false);

// Sort options: 'name', 'category', 'size', 'author'
```

### Validation
```javascript
const result = GameUtils.validateGameData({
    id: 'game-1',
    name: 'Tetris',
    isLocal: true,
    code: '<html></html>'
});

if (result.valid) {
    console.log('Valid!');
} else {
    console.log('Errors:', result.errors);
}
```

### Helpers
```javascript
// Generate unique ID
const id = GameUtils.generateGameId('local');
// => 'local-1234567890-abc123def'

// Format file size
const size = GameUtils.formatFileSize(1024000);
// => '1000 KB'
```

## AppConfig

### Access Configuration
```javascript
// Repository info
AppConfig.repository.owner      // 'kody-w'
AppConfig.repository.name       // 'localFirstTools'
AppConfig.repository.branch     // 'main'

// Categories
AppConfig.categories            // ['all', 'action', 'puzzle', ...]

// Storage keys
AppConfig.storage.favorites     // 'steamDeck_favorites_v1'
AppConfig.storage.installed     // 'steamDeck_installed_v1'
AppConfig.storage.localGames    // 'steamDeck_localGames_v1'

// Animation timings
AppConfig.animation.short       // 200
AppConfig.animation.medium      // 300
AppConfig.animation.long        // 500
```

## Common Patterns

### Initialize App
```javascript
const stateManager = new StateManager();

// Load saved data
const games = StorageService.loadLocalGames();
const favorites = StorageService.loadFavorites();
const installed = StorageService.loadInstalledGames();

stateManager.setState({ games, favorites, installed });
```

### Add New Game
```javascript
const newGame = new Game({
    id: GameUtils.generateGameId('local'),
    name: 'My Game',
    description: 'Custom game',
    icon: '🎮',
    category: 'arcade',
    author: 'Me',
    version: '1.0',
    isLocal: true,
    code: '<!DOCTYPE html>...'
});

// Validate
const validation = GameUtils.validateGameData(newGame);
if (validation.valid) {
    const games = stateManager.get('games');
    stateManager.setState({ games: [...games, newGame] });
    StorageService.saveLocalGames(stateManager.get('games'));
}
```

### Toggle Favorite
```javascript
function toggleFavorite(gameId) {
    const favorites = new Set(stateManager.get('favorites'));

    if (favorites.has(gameId)) {
        favorites.delete(gameId);
    } else {
        favorites.add(gameId);
    }

    stateManager.setState({ favorites });
    StorageService.saveFavorites(favorites);
}
```

### Search & Filter
```javascript
function searchGames(query) {
    const state = stateManager.getState();

    const filtered = GameUtils.filterGames(state.games, {
        searchQuery: query,
        category: state.currentCategory !== 'all' ? state.currentCategory : null
    });

    stateManager.setState({ filteredGames: filtered });
}
```

### Export/Import Games
```javascript
// Export
function exportGames() {
    const data = StorageService.exportAllData();
    const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'games-backup.json';
    a.click();

    URL.revokeObjectURL(url);
}

// Import
async function importGames(file) {
    const text = await file.text();
    const data = JSON.parse(text);

    StorageService.importAllData(data);

    // Reload state
    const games = StorageService.loadLocalGames();
    stateManager.setState({ games });
}
```

## State Properties

```javascript
{
    games: [],                    // All games (Game instances)
    filteredGames: [],           // Currently filtered games
    currentView: 'store',        // 'store', 'library', 'create', 'settings'
    currentCategory: 'all',      // Category filter
    searchQuery: '',             // Search string
    favorites: new Set(),        // Favorite game IDs
    installedGames: new Set(),   // Installed game IDs
    selectedIndex: 0,            // Navigation index
    inputMode: 'mouse'           // 'mouse', 'keyboard', 'gamepad', 'touch'
}
```

## Storage Format

### Favorites (Array)
```json
["game-id-1", "game-id-2"]
```

### Installed (Array)
```json
["game-id-1", "game-id-2"]
```

### Local Games (Array of Objects)
```json
[
  {
    "id": "game-1",
    "name": "Tetris",
    "description": "Puzzle game",
    "icon": "🧱",
    "category": "puzzle",
    "url": "",
    "size": "8 KB",
    "author": "John",
    "version": "1.0",
    "code": "<!DOCTYPE html>...",
    "isLocal": true
  }
]
```

## Error Handling

All storage operations return success indicators:

```javascript
// Returns true/false
const success = StorageService.save('key', data);
if (!success) {
    console.error('Save failed');
}

// Returns data or default value
const data = StorageService.load('key', []);
// data is always defined

// Try-catch for complex operations
try {
    const game = LocalGameService.createGameFromJSON(json);
    // use game
} catch (error) {
    console.error('Invalid game data:', error);
}
```

## Performance Tips

1. Batch state updates:
```javascript
// Good - single update
stateManager.setState({
    games: newGames,
    currentView: 'library',
    searchQuery: query
});

// Bad - multiple updates
stateManager.setState({ games: newGames });
stateManager.setState({ currentView: 'library' });
stateManager.setState({ searchQuery: query });
```

2. Subscribe selectively:
```javascript
// Only subscribe to properties you need
stateManager.subscribe('games', handleGamesChange);
// Don't subscribe to everything
```

3. Unsubscribe when done:
```javascript
const unsubscribe = stateManager.subscribe('games', handler);
// Later...
unsubscribe();
```

4. Filter before rendering:
```javascript
// Good - filter first
const filtered = GameUtils.filterGames(games, filters);
renderGames(filtered);

// Bad - filter during render
renderGames(games); // filters inside render function
```

## File Locations

- **Core Module**: `/game-store-models.js`
- **Documentation**: `/game-store-models-README.md`
- **Example**: `/game-store-models-example.html`
- **Cheat Sheet**: `/game-store-models-cheatsheet.md` (this file)

## Testing

```javascript
// Quick test
const game = new Game({ id: '1', name: 'Test', isLocal: true, code: '<html></html>' });
console.assert(game.isValid(), 'Game should be valid');

StorageService.clearAll();
StorageService.saveLocalGames([game]);
const loaded = StorageService.loadLocalGames();
console.assert(loaded.length === 1, 'Should load 1 game');
console.assert(loaded[0].name === 'Test', 'Name should match');
```

## Integration Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Game Store</title>
</head>
<body>
    <div id="app"></div>

    <script src="game-store-models.js"></script>
    <script>
        const { Game, StateManager, StorageService, GameUtils } = window.GameStore;

        // Initialize
        const stateManager = new StateManager();
        const games = StorageService.loadLocalGames();
        stateManager.setState({ games });

        // Subscribe to changes
        stateManager.subscribe('games', renderGames);

        // Your app logic here
    </script>
</body>
</html>
```

## Keyboard Shortcuts (for reference)

Based on typical game store implementations:
- **Arrow Keys**: Navigate
- **Enter/Space**: Select
- **Escape**: Back/Close
- **F**: Toggle favorite
- **Tab**: Switch focus

## Browser Compatibility

- **ES6 Classes**: Chrome 49+, Firefox 45+, Safari 9+, Edge 13+
- **Set**: Chrome 38+, Firefox 13+, Safari 8+, Edge 12+
- **LocalStorage**: All modern browsers (IE8+)

For older browsers, use Babel transpilation.
