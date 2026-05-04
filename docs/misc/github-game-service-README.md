# GitHub Game Service

A comprehensive JavaScript service for fetching HTML games from GitHub repositories and managing local game collections. Designed for local-first applications with full offline support and JSON import/export capabilities.

## Features

- **GitHub Integration**: Fetch HTML game files from any GitHub repository
- **Game Metadata Database**: Pre-configured metadata for popular games (Snake, Tetris, Pong, etc.)
- **Built-in Games**: Includes a complete Tetris implementation
- **Import/Export**: Full JSON-based game import/export functionality
- **Local-First**: Works entirely offline with localStorage support
- **Error Handling**: Robust fallback mechanisms for API failures
- **Zero Dependencies**: Pure vanilla JavaScript, no external libraries

## Installation

Simply include the service in your HTML:

```html
<script src="github-game-service.js"></script>
```

Or import as a module:

```javascript
import { GitHubService, LocalGameService, Game } from './github-game-service.js';
```

## Usage

### Fetch Games from GitHub

```javascript
// Fetch all HTML games from the repository
const games = await GitHubService.fetchGames();
console.log(`Loaded ${games.length} games`);

// Each game object contains:
games.forEach(game => {
    console.log(game.name);        // "Snake Classic"
    console.log(game.icon);        // "🐍"
    console.log(game.category);    // "arcade"
    console.log(game.description); // "The classic snake game..."
    console.log(game.url);         // GitHub raw URL
    console.log(game.size);        // "42 KB"
});
```

### Get Built-in Tetris

```javascript
// Get the embedded Tetris game
const tetris = LocalGameService.getBuiltInTetris();

// Launch it in an iframe or new window
const iframe = document.createElement('iframe');
iframe.srcdoc = tetris.code;
document.body.appendChild(iframe);
```

### Import Games from JSON

```javascript
// Import from file input
document.getElementById('fileInput').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const text = await file.text();

    // Import can handle single game or multiple games
    const games = LocalGameService.importGamesFromJSON(text);
    console.log(`Imported ${games.length} games`);
});
```

### Export Games

```javascript
// Export a single game
const game = games[0];
LocalGameService.exportGame(game);

// Export all games to a single JSON file
LocalGameService.exportAllGames(games);
```

### Create Custom Games

```javascript
const myGame = new Game({
    id: 'my-custom-game',
    name: 'My Awesome Game',
    description: 'A fun game I created',
    icon: '🎮',
    category: 'arcade',
    author: 'Your Name',
    version: '1.0',
    code: '<html><!-- Your complete game HTML here --></html>',
    isLocal: true
});
```

## API Reference

### GitHubService

#### `GitHubService.fetchGames()`

Fetches HTML games from the repository.

- **Returns**: `Promise<Game[]>` - Array of Game objects
- **Filters**: Automatically excludes index, gallery, template, and steamdeck files
- **Error Handling**: Returns empty array on failure

#### `GitHubService.getGameInfo(filename)`

Gets metadata for known games from the built-in database.

- **Parameters**: `filename` (string) - Filename without extension
- **Returns**: Object with `{ icon, category, description, name }`
- **Database includes**: snake, tetris, breakout, pong, space-invaders, flappy, asteroids, pacman

#### `GitHubService.formatName(baseName)`

Converts filename to human-readable title.

- **Parameters**: `baseName` (string) - Filename without extension
- **Returns**: string - Formatted name (e.g., "snake-game" → "Snake Game")

#### `GitHubService.formatFileSize(bytes)`

Formats file size from bytes to readable format.

- **Parameters**: `bytes` (number) - File size in bytes
- **Returns**: string - Formatted size (e.g., "42 KB", "2 MB")

### LocalGameService

#### `LocalGameService.getBuiltInTetris()`

Returns a complete Tetris game as a Game object.

- **Returns**: `Game` - Fully playable Tetris implementation
- **Features**: Full controls, scoring, line clearing, game over

#### `LocalGameService.createGameFromJSON(json)`

Creates a Game object from JSON data.

- **Parameters**: `json` (string|Object) - JSON string or object
- **Returns**: `Game` - New game instance
- **Throws**: Error if JSON is invalid or missing required fields
- **Required fields**: `name`, `code`
- **Auto-generates**: `id` if not present

#### `LocalGameService.exportGame(game)`

Exports a single game to a JSON file.

- **Parameters**: `game` (Game) - Game object to export
- **Downloads**: JSON file named `{game-id}.json`

#### `LocalGameService.exportAllGames(games)`

Exports multiple games to a single JSON file.

- **Parameters**: `games` (Game[]) - Array of games to export
- **Returns**: `boolean` - Success status
- **Export format**:
  ```json
  {
    "version": "1.0",
    "exported": "2025-10-12T12:34:56.789Z",
    "timestamp": 1728734096789,
    "count": 5,
    "games": [...]
  }
  ```

#### `LocalGameService.importGamesFromJSON(json)`

Imports games from JSON file content.

- **Parameters**: `json` (string|Object) - JSON string or object
- **Returns**: `Game[]` - Array of imported games
- **Supports**: Single game or multiple game exports
- **Throws**: Error if import fails

### Game Class

The Game class represents a single game with all its metadata and code.

#### Constructor

```javascript
new Game({
    id: string,              // Unique identifier
    name: string,            // Display name
    description: string,     // Game description
    icon: string,            // Emoji icon
    category: string,        // Game category
    url: string,            // URL to game (for remote games)
    size: string,           // File size (formatted)
    code: string,           // Complete HTML code (for local games)
    author: string,         // Author name
    version: string,        // Version number
    isLocal: boolean,       // Whether game is stored locally
    isEmulated: boolean     // Whether game requires emulation
})
```

#### Methods

- `toJSON()` - Returns JSON-serializable object for export

#### Properties

All constructor parameters are available as instance properties.

## Game Categories

The service recognizes the following categories:

- **arcade** - Classic arcade games (Snake, Pong, Pac-Man)
- **puzzle** - Puzzle games (Tetris)
- **action** - Action games (Space Invaders, Asteroids)
- **strategy** - Strategy games
- **adventure** - Adventure games

## JSON Export Format

### Single Game Export

```json
{
    "id": "snake-game",
    "name": "Snake Classic",
    "description": "The classic snake game",
    "icon": "🐍",
    "category": "arcade",
    "author": "Unknown",
    "version": "1.0",
    "code": "<!DOCTYPE html>...",
    "isLocal": true
}
```

### Multiple Games Export

```json
{
    "version": "1.0",
    "exported": "2025-10-12T12:34:56.789Z",
    "timestamp": 1728734096789,
    "count": 3,
    "games": [
        { "id": "...", "name": "...", ... },
        { "id": "...", "name": "...", ... },
        { "id": "...", "name": "...", ... }
    ]
}
```

## Error Handling

The service includes comprehensive error handling:

- **GitHub API failures**: Returns empty array instead of throwing
- **Invalid JSON**: Throws descriptive errors for debugging
- **Missing fields**: Validates required fields on import
- **Network issues**: Graceful fallback to empty results

Example error handling:

```javascript
try {
    const games = await GitHubService.fetchGames();
    if (games.length === 0) {
        console.log('No games available or API error');
        // Fall back to local games
        const tetris = LocalGameService.getBuiltInTetris();
        games.push(tetris);
    }
} catch (error) {
    console.error('Failed to load games:', error);
}
```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires ES6+ support
- Uses Fetch API for GitHub integration
- Uses Blob API for file exports

## Demo

Open `github-game-service-demo.html` to see the service in action with:

- Live GitHub fetching
- Game display and metadata
- Import/Export functionality
- Tetris demo
- Usage examples

## Repository Configuration

The service is configured to fetch from:

- **Repository**: kody-w/localFirstTools
- **Branch**: main
- **Files**: All `.html` files (excluding index, gallery, template, steamdeck)

To use with a different repository, modify the constants in `GitHubService.fetchGames()`:

```javascript
const owner = 'your-username';
const name = 'your-repo';
const branch = 'main';
```

## License

Part of the localFirstTools project. See main repository for license details.

## Contributing

When adding games to the database, update the `gameDatabase` object in `GitHubService.getGameInfo()`:

```javascript
'your-game': {
    icon: '🎮',
    category: 'arcade',
    description: 'Your game description',
    name: 'Display Name'
}
```

## Built-in Games

### Tetris Classic

The service includes a complete, production-ready Tetris implementation:

- **Features**: Classic gameplay, scoring, line clearing, game over
- **Controls**: Arrow keys (left/right/down), up to rotate, space to pause
- **Size**: ~8 KB
- **Style**: Modern gradient design with smooth animations
- **Code**: Fully commented and maintainable

Access it with:

```javascript
const tetris = LocalGameService.getBuiltInTetris();
```

## Best Practices

1. **Always handle errors**: Use try-catch blocks for async operations
2. **Validate imports**: Check imported games before adding to your collection
3. **Cache locally**: Store fetched games in localStorage for offline use
4. **Provide fallbacks**: Always have built-in games as fallback
5. **Filter duplicates**: Check for existing game IDs before adding imports

## Example Integration

Complete example of integrating the service:

```javascript
class GameStore {
    constructor() {
        this.games = [];
        this.init();
    }

    async init() {
        // Load from localStorage
        const cached = localStorage.getItem('games');
        if (cached) {
            this.games = JSON.parse(cached).map(g => new Game(g));
        }

        // Add built-in games
        const tetris = LocalGameService.getBuiltInTetris();
        if (!this.games.some(g => g.id === tetris.id)) {
            this.games.push(tetris);
        }

        // Try to fetch from GitHub
        try {
            const githubGames = await GitHubService.fetchGames();
            githubGames.forEach(game => {
                if (!this.games.some(g => g.id === game.id)) {
                    this.games.push(game);
                }
            });
        } catch (error) {
            console.log('Offline mode - using cached games');
        }

        // Save to cache
        this.saveToCache();
    }

    saveToCache() {
        localStorage.setItem('games', JSON.stringify(this.games));
    }

    exportAll() {
        LocalGameService.exportAllGames(this.games);
    }

    async importFile(file) {
        const text = await file.text();
        const imported = LocalGameService.importGamesFromJSON(text);

        imported.forEach(game => {
            if (!this.games.some(g => g.id === game.id)) {
                this.games.push(game);
            }
        });

        this.saveToCache();
        return imported.length;
    }
}

// Usage
const store = new GameStore();
```

## Support

For issues or questions, check the main repository or open an issue.
