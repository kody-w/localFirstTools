# Game Store Data Models and Storage Services

Clean, well-commented JavaScript code for managing game data, state, and local storage in a game store application.

## Overview

This module provides ES6 classes and utilities for building a local-first game store application with:
- Game data modeling
- Reactive state management
- LocalStorage persistence
- Utility functions for common operations

## Files

- `game-store-models.js` - Core data models and services

## Components

### 1. AppConfig

Configuration object containing:
- **Repository settings** - GitHub repository information
- **Categories** - Available game categories
- **Storage keys** - LocalStorage key names
- **Animation timings** - Standard animation durations

```javascript
const AppConfig = {
    repository: {
        owner: 'kody-w',
        name: 'localFirstTools',
        branch: 'main'
    },
    categories: ['all', 'action', 'puzzle', 'arcade', 'strategy', 'adventure'],
    storage: {
        favorites: 'steamDeck_favorites_v1',
        installed: 'steamDeck_installed_v1',
        localGames: 'steamDeck_localGames_v1'
    }
};
```

### 2. Game Class

Represents a single game with all metadata.

**Properties:**
- `id` (string) - Unique identifier
- `name` (string) - Display name
- `description` (string) - Brief description
- `icon` (string) - Emoji or icon
- `category` (string) - Game category
- `url` (string) - URL to game resource
- `size` (string) - File size
- `isLocal` (boolean) - Local vs remote flag
- `code` (string|null) - Complete HTML code for local games
- `author` (string) - Creator name
- `version` (string) - Version number

**Methods:**
- `toJSON()` - Serialize game for storage/export
- `isValid()` - Validate required fields
- `clone()` - Create a copy of the game

**Example:**
```javascript
const game = new Game({
    id: 'tetris-01',
    name: 'Tetris',
    description: 'Classic block puzzle game',
    icon: '🧱',
    category: 'puzzle',
    author: 'John Doe',
    version: '1.0',
    isLocal: true,
    code: '<!DOCTYPE html>...'
});

// Serialize for storage
const jsonData = game.toJSON();

// Validate
if (game.isValid()) {
    console.log('Game is valid');
}
```

### 3. StateManager Class

Manages application state with publish-subscribe pattern for reactive updates.

**State Properties:**
- `games` - Array of all Game instances
- `filteredGames` - Currently displayed games
- `currentView` - Active view ('store', 'library', 'create', 'settings')
- `currentCategory` - Selected category filter
- `searchQuery` - Search text
- `favorites` - Set of favorite game IDs
- `installedGames` - Set of installed game IDs
- `selectedIndex` - Current selection index
- `inputMode` - Input method ('mouse', 'keyboard', 'gamepad', 'touch')

**Methods:**
- `setState(updates)` - Update state and notify subscribers
- `getState()` - Get copy of current state
- `get(key)` - Get specific state property
- `subscribe(key, callback)` - Subscribe to property changes
- `notify(keys)` - Notify subscribers (internal)
- `reset()` - Reset to initial state
- `clearSubscribers()` - Remove all subscribers

**Example:**
```javascript
const stateManager = new StateManager();

// Subscribe to changes
const unsubscribe = stateManager.subscribe('games', (games) => {
    console.log('Games updated:', games.length);
});

// Update state
stateManager.setState({
    games: [game1, game2],
    currentView: 'library'
});

// Get state
const state = stateManager.getState();
console.log(state.currentView); // 'library'

// Unsubscribe when done
unsubscribe();
```

### 4. StorageService Class

Static methods for localStorage operations with error handling.

**Methods:**
- `save(key, data)` - Save data to localStorage
- `load(key, defaultValue)` - Load data from localStorage
- `remove(key)` - Remove item from localStorage
- `saveLocalGames(games)` - Save array of Game instances
- `loadLocalGames()` - Load array of Game instances
- `saveFavorites(favorites)` - Save favorites Set
- `loadFavorites()` - Load favorites Set
- `saveInstalledGames(installedGames)` - Save installed Set
- `loadInstalledGames()` - Load installed Set
- `clearAll()` - Remove all game store data
- `getStorageSize()` - Get total storage size in bytes
- `isAvailable()` - Check if localStorage is available
- `exportAllData()` - Export all data as JSON object
- `importAllData(data)` - Import data from JSON object

**Example:**
```javascript
// Save a game
const game = new Game({ name: 'Tetris', ... });
const games = [game];
StorageService.saveLocalGames(games);

// Load games
const loadedGames = StorageService.loadLocalGames();

// Save favorites
const favorites = new Set(['game-1', 'game-2']);
StorageService.saveFavorites(favorites);

// Load favorites
const loadedFavorites = StorageService.loadFavorites();

// Check storage availability
if (StorageService.isAvailable()) {
    console.log('LocalStorage is available');
}

// Export all data
const exportData = StorageService.exportAllData();
console.log(exportData);

// Clear all data
StorageService.clearAll();
```

### 5. GameUtils Class

Utility functions for game operations.

**Methods:**
- `filterGames(games, filters)` - Filter games by criteria
- `sortGames(games, sortBy, ascending)` - Sort games
- `validateGameData(data)` - Validate game data structure
- `generateGameId(prefix)` - Generate unique ID
- `formatFileSize(bytes)` - Format bytes to readable size

**Example:**
```javascript
// Filter games
const filtered = GameUtils.filterGames(allGames, {
    category: 'puzzle',
    searchQuery: 'tetris',
    installedOnly: true,
    installedGames: installedSet
});

// Sort games
const sorted = GameUtils.sortGames(allGames, 'name', true);

// Validate game data
const validation = GameUtils.validateGameData({
    name: 'Tetris',
    id: 'tetris-01',
    isLocal: true,
    code: '<!DOCTYPE html>...'
});

if (validation.valid) {
    console.log('Valid game data');
} else {
    console.log('Errors:', validation.errors);
}

// Generate unique ID
const newId = GameUtils.generateGameId('local');
console.log(newId); // 'local-1234567890-abc123def'

// Format file size
const size = GameUtils.formatFileSize(1024000);
console.log(size); // '1000 KB'
```

## Complete Usage Example

```javascript
// Initialize the system
const stateManager = new StateManager();

// Load saved data
const savedFavorites = StorageService.loadFavorites();
const savedInstalled = StorageService.loadInstalledGames();
const savedGames = StorageService.loadLocalGames();

stateManager.setState({
    games: savedGames,
    favorites: savedFavorites,
    installedGames: savedInstalled
});

// Subscribe to state changes
stateManager.subscribe('games', (games) => {
    console.log(`Games updated: ${games.length} total`);

    // Filter and display games
    const filtered = GameUtils.filterGames(games, {
        category: stateManager.get('currentCategory'),
        searchQuery: stateManager.get('searchQuery')
    });

    // Update UI here
    renderGames(filtered);
});

// Create a new game
const newGame = new Game({
    id: GameUtils.generateGameId('local'),
    name: 'My Custom Game',
    description: 'A fun game I created',
    icon: '🎮',
    category: 'arcade',
    author: 'Me',
    version: '1.0',
    isLocal: true,
    code: '<!DOCTYPE html>...'
});

// Validate before adding
const validation = GameUtils.validateGameData(newGame);
if (validation.valid) {
    // Add to state
    const currentGames = stateManager.get('games');
    stateManager.setState({
        games: [...currentGames, newGame]
    });

    // Save to storage
    StorageService.saveLocalGames(stateManager.get('games'));
}

// Toggle favorite
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

// Search games
function searchGames(query) {
    stateManager.setState({ searchQuery: query });

    const filtered = GameUtils.filterGames(
        stateManager.get('games'),
        { searchQuery: query }
    );

    stateManager.setState({ filteredGames: filtered });
}

// Filter by category
function filterByCategory(category) {
    stateManager.setState({ currentCategory: category });

    const filtered = GameUtils.filterGames(
        stateManager.get('games'),
        { category: category }
    );

    stateManager.setState({ filteredGames: filtered });
}

// Export all games
function exportGames() {
    const data = StorageService.exportAllData();
    const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'game-store-backup.json';
    a.click();

    URL.revokeObjectURL(url);
}

// Import games
async function importGames(file) {
    const text = await file.text();
    const data = JSON.parse(text);

    if (StorageService.importAllData(data)) {
        // Reload state
        const games = StorageService.loadLocalGames();
        stateManager.setState({ games });
        console.log('Import successful');
    } else {
        console.error('Import failed');
    }
}
```

## Storage Schema

### LocalStorage Keys

1. **steamDeck_favorites_v1**
   ```json
   ["game-id-1", "game-id-2", "game-id-3"]
   ```

2. **steamDeck_installed_v1**
   ```json
   ["game-id-1", "game-id-2"]
   ```

3. **steamDeck_localGames_v1**
   ```json
   [
     {
       "id": "game-1",
       "name": "Tetris",
       "description": "Classic puzzle game",
       "icon": "🧱",
       "category": "puzzle",
       "url": "",
       "size": "8 KB",
       "author": "John Doe",
       "version": "1.0",
       "code": "<!DOCTYPE html>...",
       "isLocal": true
     }
   ]
   ```

## Browser Compatibility

- **LocalStorage**: All modern browsers (IE8+)
- **ES6 Classes**: Modern browsers (ES6+)
- **Set**: Modern browsers (ES6+)

For older browser support, transpile with Babel.

## Error Handling

All storage operations include try-catch blocks and return boolean success indicators or default values:

```javascript
// Save returns true/false
const success = StorageService.save('key', data);
if (!success) {
    console.error('Save failed - storage quota exceeded?');
}

// Load returns default value on error
const data = StorageService.load('key', []);
// data is always defined (either loaded data or [])
```

## Performance Considerations

1. **Batch Updates**: Use `setState()` once with multiple properties instead of multiple calls
2. **Subscribe Wisely**: Only subscribe to properties you need to watch
3. **Filter Before Render**: Filter games before passing to render functions
4. **Unsubscribe**: Always unsubscribe when components unmount

## Testing

```javascript
// Example test cases

// Test Game creation
const game = new Game({
    id: 'test-1',
    name: 'Test Game',
    isLocal: true,
    code: '<html></html>'
});
console.assert(game.isValid(), 'Game should be valid');

// Test StateManager
const sm = new StateManager();
let callCount = 0;
sm.subscribe('games', () => callCount++);
sm.setState({ games: [game] });
console.assert(callCount === 1, 'Subscriber should be called once');

// Test StorageService
StorageService.clearAll();
StorageService.saveLocalGames([game]);
const loaded = StorageService.loadLocalGames();
console.assert(loaded.length === 1, 'Should load one game');
console.assert(loaded[0].name === 'Test Game', 'Game name should match');
```

## Integration with Existing Code

To use in an HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Game Store</title>
</head>
<body>
    <!-- Your HTML here -->

    <script src="game-store-models.js"></script>
    <script>
        // Access via window.GameStore
        const { Game, StateManager, StorageService, GameUtils, AppConfig } = window.GameStore;

        // Initialize your app
        const stateManager = new StateManager();
        // ... rest of your code
    </script>
</body>
</html>
```

## License

This code is part of the localFirstTools project and follows the same license.

## Contributing

When modifying these models:
1. Maintain backward compatibility with storage format
2. Update version numbers in storage keys if breaking changes
3. Add JSDoc comments for new methods
4. Test with actual localStorage operations
5. Consider storage quota limits

## Support

For issues or questions, refer to the main localFirstTools repository.
