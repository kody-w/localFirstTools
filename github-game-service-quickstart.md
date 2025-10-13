# GitHub Game Service - Quick Start Guide

## Installation

```html
<script src="github-game-service.js"></script>
```

## Basic Usage

### Fetch Games from GitHub

```javascript
// Fetch all games
const games = await GitHubService.fetchGames();
console.log(`Loaded ${games.length} games`);
```

### Get Built-in Tetris

```javascript
const tetris = LocalGameService.getBuiltInTetris();
// Launch in iframe or new window
iframe.srcdoc = tetris.code;
```

### Import Games

```javascript
// From file input
const file = fileInput.files[0];
const text = await file.text();
const games = LocalGameService.importGamesFromJSON(text);
```

### Export Games

```javascript
// Export single game
LocalGameService.exportGame(game);

// Export all games
LocalGameService.exportAllGames(games);
```

## Game Object Structure

```javascript
{
    id: "snake-game",
    name: "Snake Classic",
    description: "The classic snake game",
    icon: "🐍",
    category: "arcade",
    url: "https://...",
    size: "42 KB",
    code: "<html>...</html>",  // For local games
    author: "Unknown",
    version: "1.0",
    isLocal: false,
    isEmulated: false
}
```

## Categories

- `arcade` - Classic arcade games
- `puzzle` - Puzzle games
- `action` - Action games
- `strategy` - Strategy games
- `adventure` - Adventure games

## Known Games Database

The service includes metadata for:

- Snake (🐍)
- Tetris (🧱)
- Breakout (🎯)
- Pong (🏓)
- Space Invaders (👾)
- Flappy Bird (🐦)
- Asteroids (☄️)
- Pac-Man (👻)

## Helper Methods

```javascript
// Format filename to title
GitHubService.formatName("snake-game")
// Returns: "Snake Game"

// Format file size
GitHubService.formatFileSize(42000)
// Returns: "41 KB"

// Get game metadata
const info = GitHubService.getGameInfo("tetris")
// Returns: { icon, category, description, name }
```

## Error Handling

```javascript
try {
    const games = await GitHubService.fetchGames();
    if (games.length === 0) {
        // Fallback to local games
        const tetris = LocalGameService.getBuiltInTetris();
        games.push(tetris);
    }
} catch (error) {
    console.error('Failed to load:', error);
}
```

## Export Format

### Single Game

```json
{
    "id": "my-game",
    "name": "My Game",
    "code": "<!DOCTYPE html>...",
    "isLocal": true
}
```

### Multiple Games

```json
{
    "version": "1.0",
    "exported": "2025-10-12T12:34:56Z",
    "count": 3,
    "games": [...]
}
```

## Demo Files

- **github-game-service-demo.html** - Interactive demo
- **github-game-service-test.html** - Test suite
- **github-game-service-README.md** - Full documentation

## Quick Example

```javascript
class GameStore {
    async init() {
        // Get built-in games
        const tetris = LocalGameService.getBuiltInTetris();
        this.games = [tetris];

        // Fetch from GitHub
        const githubGames = await GitHubService.fetchGames();
        this.games.push(...githubGames);

        // Save to localStorage
        localStorage.setItem('games', JSON.stringify(this.games));
    }

    exportAll() {
        LocalGameService.exportAllGames(this.games);
    }
}
```

## License

Part of localFirstTools - see main repository for details.
