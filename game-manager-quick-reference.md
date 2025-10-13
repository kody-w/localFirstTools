# Game Manager System - Quick Reference

## Quick Start

```javascript
// 1. Initialize
const stateManager = new StateManager();
const gameManager = new GameManager(stateManager, gameLibrary);

// 2. Render games
gameManager.renderAllGames();

// 3. Done!
```

## Common Operations

### Add a Game
```javascript
gameManager.addGame({
    id: 'my-game',
    name: 'My Game',
    description: 'A fun game',
    icon: '🎮',
    category: 'action',
    type: 'embedded'
});
```

### Launch a Game
```javascript
await gameManager.launchGame('my-game');
```

### Toggle Favorite
```javascript
gameManager.toggleFavorite('my-game');
```

### Filter Games
```javascript
stateManager.updateState({
    currentView: 'library',      // 'store' or 'library'
    currentCategory: 'action',   // any category or 'all'
    searchQuery: 'search term'
});
```

### Get Games
```javascript
const all = gameManager.getAllGames();
const installed = gameManager.getInstalledGames();
const favorites = gameManager.getFavoriteGames();
const single = gameManager.getGameById('my-game');
```

## Game Types

### Embedded Game
```javascript
{
    id: 'game-id',
    type: 'embedded',
    initialize: function(display) { /* setup */ },
    update: function(deltaTime) { /* loop */ },
    render: function() { /* draw */ }
}
```

### Iframe Game
```javascript
{
    id: 'game-id',
    type: 'iframe',
    url: 'https://example.com/game.html'
}
```

### Local Game
```javascript
{
    id: 'game-id',
    type: 'local',
    htmlContent: '<html>...</html>'  // or use url
}
```

## State Subscription

```javascript
stateManager.subscribe('stateChanged', (state) => {
    console.log('State updated:', state);
});
```

## Event Delegation

All clicks handled automatically:
- Click card → Show details
- Click play button → Launch game
- Click favorite → Toggle favorite

No manual event listeners needed!

## Filtering Logic

Games shown when ALL conditions are true:

1. **View Filter**
   - Store: All games
   - Library: Only installed games

2. **Category Filter**
   - All: All categories
   - Favorites: Only favorites
   - Specific: Only that category

3. **Search Filter**
   - Matches name, description, or category

## localStorage Structure

```javascript
{
    "retroplay_state": {
        "installedGames": ["id1", "id2"],
        "favorites": ["id1"],
        "currentView": "store",
        "currentCategory": "all",
        "gameHistory": ["id1", "id2"]
    }
}
```

## Required HTML Elements

```html
<!-- Minimum required -->
<div id="games-grid"></div>
<div id="emulator-container">
    <button id="close-emulator"></button>
    <iframe id="game-iframe"></iframe>
    <div id="game-display"></div>
</div>
<div id="modal-overlay">
    <div id="game-details-modal" class="modal">
        <button class="close-modal"></button>
        <div id="modal-game-icon"></div>
        <div id="modal-game-title"></div>
        <div id="modal-game-description"></div>
        <button id="play-from-modal"></button>
    </div>
</div>
<select id="view-toggle"></select>
<select id="category-filter"></select>
<input id="search-input">
```

## Game Card CSS Classes

```css
.game-card { /* Card container */ }
.game-icon { /* Icon/emoji */ }
.game-name { /* Title */ }
.game-description { /* Description */ }
.game-category { /* Category badge */ }
.play-button { /* Play button */ }
.favorite-button { /* Favorite button */ }
.favorite-button.favorited { /* Favorited state */ }
.installed-badge { /* Installed badge */ }
```

## Cleanup

```javascript
// Clean up when done
gameManager.destroy();
```

## Error Handling

All methods include try/catch:
```javascript
try {
    await gameManager.launchGame(gameId);
} catch (error) {
    console.error('Error:', error);
    alert(`Failed: ${error.message}`);
}
```

## Performance Tips

1. Use `renderAllGames()` once at start
2. Filter updates are automatic
3. Blob URLs cleaned up automatically
4. Event delegation = single listener
5. State changes batched and saved

## Common Patterns

### Add and Launch
```javascript
gameManager.addGame(game);
await gameManager.launchGame(game.id);
```

### Favorite and Filter
```javascript
gameManager.toggleFavorite(gameId);
stateManager.updateState({ currentCategory: 'favorites' });
```

### Search and View
```javascript
stateManager.updateState({
    searchQuery: 'puzzle',
    currentView: 'store'
});
```

### Install and History
```javascript
// Automatically happens when launching
await gameManager.launchGame(gameId);
// Now in installedGames and gameHistory
```

## Debug Commands

```javascript
// In browser console:
console.log(stateManager.getState());
console.log(gameManager.getAllGames());
console.log(gameManager.getInstalledGames());
console.log(gameManager.getFavoriteGames());
localStorage.getItem('retroplay_state');
```

## Keyboard Shortcuts (Example)

```javascript
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        gameManager.closeEmulator();
        gameManager.closeModal();
    }
});
```

## Testing

See `game-manager-test.html` for complete test suite including:
- Basic operations
- State management
- Favorites
- Filtering
- Game launching
- Performance tests
- Stress tests
- Full integration

## Files

- `game-manager-system.js` - Core system
- `game-manager-demo.html` - Interactive demo
- `game-manager-test.html` - Test suite
- `GAME-MANAGER-README.md` - Full docs
- `game-manager-quick-reference.md` - This file

## Support

See full documentation in `GAME-MANAGER-README.md` for:
- Complete API reference
- Architecture details
- Advanced features
- Troubleshooting
- Security considerations
- Browser compatibility

## License

Part of localFirstTools project. See main repository for license.
