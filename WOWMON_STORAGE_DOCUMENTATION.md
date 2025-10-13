# WoWmon Storage Manager Documentation
## Agent 8 - Storage & Export Specialist

This document provides comprehensive documentation for the WoWmon StorageManager class, which handles all localStorage persistence, import/export functionality, and data management for user data.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [Usage Examples](#usage-examples)
6. [Data Formats](#data-formats)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## Overview

The StorageManager class provides a complete solution for:
- **Data Persistence**: Save user favorites, teams, notes, preferences, and search history
- **Import/Export**: Export data as JSON and import from various formats
- **Team Management**: Create, update, and delete teams with up to 6 creatures
- **Pokedex Tracking**: Track which creatures have been seen and caught
- **Sharing Features**: Generate shareable URLs and copy data to clipboard
- **Auto-Backup**: Automatic backup and restore functionality
- **Data Management**: Clear specific data types or all data with confirmation

### Storage Keys

The manager uses the following localStorage keys:
- `wowmon_favorites` - Array of favorite creature IDs
- `wowmon_teams` - Array of saved team objects
- `wowmon_preferences` - User preferences object
- `wowmon_notes` - Object mapping creature IDs to notes
- `wowmon_search_history` - Array of recent search terms
- `wowmon_pokedex` - Object tracking seen/caught creatures
- `wowmon_achievements` - Achievement tracking (reserved)

### Limits

- **Max Storage Size**: 5MB (configurable)
- **Max Search History**: 50 entries
- **Max Teams**: 20 teams
- **Max Team Size**: 6 creatures per team

---

## Installation

### Option 1: Copy the StorageManager class into wowMon.html

Insert the StorageManager class before the GameEngine class definition in wowMon.html:

```javascript
// Around line 1379, before "class GameEngine {"
class StorageManager {
    // ... (copy entire class from wowmon_storage_manager.js)
}
```

### Option 2: Use as separate file (not recommended for this project)

Since this is a local-first project with self-contained HTML files, Option 1 is preferred.

---

## Quick Start

```javascript
// Initialize the storage manager
const storage = new StorageManager();

// Check if storage is available
if (storage.isStorageAvailable()) {
    console.log('Storage is ready!');
}

// Save a favorite
const result = storage.saveFavorite('kobold');
console.log(result.message); // "Added to favorites!"

// Get all favorites
const favorites = storage.getFavorites();
console.log(favorites); // ['kobold']

// Check storage size
console.log(storage.getStorageSizeFormatted()); // "15.2 KB"
```

---

## API Reference

### Initialization

#### `constructor()`
Creates a new StorageManager instance and initializes storage.

```javascript
const storage = new StorageManager();
```

#### `initializeStorage()`
Initializes all storage keys with default values if they don't exist.

**Returns**: `boolean` - true if successful, false otherwise

```javascript
const success = storage.initializeStorage();
```

---

### Storage Status

#### `isStorageAvailable()`
Checks if localStorage is available in the browser.

**Returns**: `boolean` - true if localStorage is available

```javascript
if (storage.isStorageAvailable()) {
    // Storage is available
}
```

#### `getStorageSize()`
Gets the current storage size in bytes.

**Returns**: `number` - Size in bytes

```javascript
const bytes = storage.getStorageSize();
```

#### `getStorageSizeFormatted()`
Gets the current storage size as a human-readable string.

**Returns**: `string` - Formatted size (e.g., "15.2 KB", "1.5 MB")

```javascript
console.log(storage.getStorageSizeFormatted()); // "15.2 KB"
```

#### `checkStorageQuota(additionalSize)`
Checks if adding more data would exceed the storage quota.

**Parameters**:
- `additionalSize` (number, optional) - Additional bytes to check

**Returns**: `boolean` - true if within quota

```javascript
if (storage.checkStorageQuota(1024)) {
    // Can add 1KB more data
}
```

---

### Favorites Management

#### `getFavorites()`
Gets all favorite creature IDs.

**Returns**: `string[]` - Array of creature IDs

```javascript
const favorites = storage.getFavorites();
// ['kobold', 'dragon', 'phoenix']
```

#### `saveFavorite(creatureId)`
Adds a creature to favorites.

**Parameters**:
- `creatureId` (string) - The creature ID to add

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.saveFavorite('dragon');
if (result.success) {
    console.log(result.message); // "Added to favorites!"
}
```

#### `removeFavorite(creatureId)`
Removes a creature from favorites.

**Parameters**:
- `creatureId` (string) - The creature ID to remove

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.removeFavorite('dragon');
```

#### `toggleFavorite(creatureId)`
Toggles a creature's favorite status.

**Parameters**:
- `creatureId` (string) - The creature ID to toggle

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.toggleFavorite('dragon');
```

#### `isFavorite(creatureId)`
Checks if a creature is in favorites.

**Parameters**:
- `creatureId` (string) - The creature ID to check

**Returns**: `boolean` - true if favorited

```javascript
if (storage.isFavorite('dragon')) {
    // Dragon is favorited
}
```

#### `getFavoritesCount()`
Gets the total number of favorites.

**Returns**: `number` - Count of favorites

```javascript
const count = storage.getFavoritesCount(); // 3
```

---

### Team Management

#### `getTeams()`
Gets all saved teams.

**Returns**: `Team[]` - Array of team objects

```javascript
const teams = storage.getTeams();
```

**Team Object Structure**:
```javascript
{
    id: "1699999999999",
    name: "My Team",
    creatures: [
        {
            id: "dragon",
            nickname: "Fluffy",
            level: 50,
            moves: ["fire_breath", "fly"]
        }
    ],
    createdAt: "2024-01-15T10:30:00.000Z",
    updatedAt: "2024-01-15T10:30:00.000Z"
}
```

#### `saveTeam(team, teamName)`
Saves a new team.

**Parameters**:
- `team` (object) - Team object with creatures array
- `teamName` (string, optional) - Name for the team

**Returns**: `{success: boolean, message: string, teamId?: string}`

```javascript
const team = {
    creatures: [
        { id: 'dragon', level: 50, moves: ['fire_breath'] },
        { id: 'phoenix', level: 45, moves: ['revive'] }
    ]
};

const result = storage.saveTeam(team, 'Fire Team');
if (result.success) {
    console.log('Team ID:', result.teamId);
}
```

#### `updateTeam(teamId, updatedTeam)`
Updates an existing team.

**Parameters**:
- `teamId` (string) - The team ID to update
- `updatedTeam` (object) - Updated team data

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.updateTeam('1699999999999', {
    name: 'Super Fire Team'
});
```

#### `deleteTeam(teamId)`
Deletes a team.

**Parameters**:
- `teamId` (string) - The team ID to delete

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.deleteTeam('1699999999999');
```

#### `getTeam(teamId)`
Gets a specific team by ID.

**Parameters**:
- `teamId` (string) - The team ID to retrieve

**Returns**: `Team | null` - Team object or null if not found

```javascript
const team = storage.getTeam('1699999999999');
if (team) {
    console.log(team.name);
}
```

---

### Notes Management

#### `getNotes()`
Gets all creature notes.

**Returns**: `{[creatureId: string]: string}` - Object mapping creature IDs to notes

```javascript
const notes = storage.getNotes();
// { "dragon": "Very powerful!", "kobold": "Good starter" }
```

#### `getNote(creatureId)`
Gets the note for a specific creature.

**Parameters**:
- `creatureId` (string) - The creature ID

**Returns**: `string` - Note text (empty string if no note)

```javascript
const note = storage.getNote('dragon');
console.log(note); // "Very powerful!"
```

#### `saveNote(creatureId, noteText)`
Saves a note for a creature.

**Parameters**:
- `creatureId` (string) - The creature ID
- `noteText` (string) - The note text (empty to delete)

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.saveNote('dragon', 'Found in mountain caves');
```

#### `deleteNote(creatureId)`
Deletes a creature's note.

**Parameters**:
- `creatureId` (string) - The creature ID

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.deleteNote('dragon');
```

---

### Search History

#### `getSearchHistory()`
Gets search history.

**Returns**: `string[]` - Array of search terms (most recent first)

```javascript
const history = storage.getSearchHistory();
// ["dragon", "fire", "kobold"]
```

#### `addSearchHistory(searchTerm)`
Adds a term to search history.

**Parameters**:
- `searchTerm` (string) - The search term to add

```javascript
storage.addSearchHistory('phoenix');
```

#### `clearSearchHistory()`
Clears all search history.

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearSearchHistory();
```

---

### Preferences

#### `getPreferences()`
Gets all user preferences.

**Returns**: `object` - Preferences object

```javascript
const prefs = storage.getPreferences();
```

**Default Preferences**:
```javascript
{
    viewMode: 'grid',
    theme: 'default',
    sortBy: 'id',
    showTypes: true,
    showStats: true,
    autoSave: true,
    soundEnabled: true
}
```

#### `savePreferences(preferences)`
Saves user preferences (merges with existing).

**Parameters**:
- `preferences` (object) - Preferences to save

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.savePreferences({
    theme: 'dark',
    soundEnabled: false
});
```

#### `getPreference(key, defaultValue)`
Gets a specific preference value.

**Parameters**:
- `key` (string) - Preference key
- `defaultValue` (any, optional) - Default if not found

**Returns**: `any` - Preference value

```javascript
const theme = storage.getPreference('theme', 'default');
```

#### `setPreference(key, value)`
Sets a specific preference value.

**Parameters**:
- `key` (string) - Preference key
- `value` (any) - Preference value

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.setPreference('theme', 'dark');
```

---

### Pokedex Tracking

#### `getPokedexEntries()`
Gets all Pokedex entries.

**Returns**: `{[creatureId: string]: PokedexEntry}` - Object mapping creature IDs to entries

```javascript
const pokedex = storage.getPokedexEntries();
```

**PokedexEntry Structure**:
```javascript
{
    seen: true,
    caught: false,
    firstSeenAt: "2024-01-15T10:30:00.000Z",
    firstCaughtAt: "2024-01-15T11:00:00.000Z"
}
```

#### `markCreatureSeen(creatureId)`
Marks a creature as seen in the Pokedex.

**Parameters**:
- `creatureId` (string) - The creature ID

```javascript
storage.markCreatureSeen('dragon');
```

#### `markCreatureCaught(creatureId)`
Marks a creature as caught in the Pokedex.

**Parameters**:
- `creatureId` (string) - The creature ID

```javascript
storage.markCreatureCaught('dragon');
```

#### `getPokedexEntry(creatureId)`
Gets the Pokedex entry for a specific creature.

**Parameters**:
- `creatureId` (string) - The creature ID

**Returns**: `PokedexEntry` - Entry object

```javascript
const entry = storage.getPokedexEntry('dragon');
if (entry.caught) {
    console.log('You caught this creature!');
}
```

#### `getPokedexStats()`
Gets overall Pokedex statistics.

**Returns**: `{totalSeen: number, totalCaught: number, total: number}`

```javascript
const stats = storage.getPokedexStats();
console.log(`Caught: ${stats.totalCaught}/${stats.total}`);
```

---

### Export Functionality

#### `exportFavorites()`
Exports favorites as JSON.

**Returns**: `{success: boolean, data?: object, json?: string, message?: string}`

```javascript
const result = storage.exportFavorites();
if (result.success) {
    console.log(result.json);
    // Download it
    storage.downloadJSON(result.data, 'wowmon-favorites.json');
}
```

#### `exportTeams()`
Exports all teams as JSON.

**Returns**: `{success: boolean, data?: object, json?: string, message?: string}`

```javascript
const result = storage.exportTeams();
if (result.success) {
    storage.downloadJSON(result.data, 'wowmon-teams.json');
}
```

#### `exportTeamShowdownFormat(teamId)`
Exports a team in Showdown format (text).

**Parameters**:
- `teamId` (string) - The team ID to export

**Returns**: `{success: boolean, text?: string, message?: string}`

```javascript
const result = storage.exportTeamShowdownFormat('1699999999999');
if (result.success) {
    console.log(result.text);
    storage.downloadText(result.text, 'team.txt');
}
```

#### `exportNotes()`
Exports all creature notes as JSON.

**Returns**: `{success: boolean, data?: object, json?: string, message?: string}`

```javascript
const result = storage.exportNotes();
if (result.success) {
    storage.downloadJSON(result.data, 'wowmon-notes.json');
}
```

#### `exportPokedex()`
Exports Pokedex data as JSON.

**Returns**: `{success: boolean, data?: object, json?: string, message?: string}`

```javascript
const result = storage.exportPokedex();
if (result.success) {
    storage.downloadJSON(result.data, 'wowmon-pokedex.json');
}
```

#### `exportAllData()`
Exports all user data as a single JSON file.

**Returns**: `{success: boolean, data?: object, json?: string, message?: string}`

```javascript
const result = storage.exportAllData();
if (result.success) {
    storage.downloadJSON(result.data, 'wowmon-backup.json');
}
```

---

### Import Functionality

#### `validateImportData(data, expectedType)`
Validates import data structure.

**Parameters**:
- `data` (object) - Parsed JSON data
- `expectedType` (string, optional) - Expected data type

**Returns**: `{valid: boolean, message?: string}`

```javascript
const validation = storage.validateImportData(parsedData, 'wowmon_favorites');
if (!validation.valid) {
    console.error(validation.message);
}
```

#### `importFavorites(jsonString, merge)`
Imports favorites from JSON.

**Parameters**:
- `jsonString` (string) - JSON string to import
- `merge` (boolean, optional) - Merge with existing data (default: true)

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.importFavorites(jsonString, true);
if (result.success) {
    console.log(result.message);
}
```

#### `importTeams(jsonString, merge)`
Imports teams from JSON.

**Parameters**:
- `jsonString` (string) - JSON string to import
- `merge` (boolean, optional) - Merge with existing data (default: true)

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.importTeams(jsonString, true);
```

#### `importNotes(jsonString, merge)`
Imports notes from JSON.

**Parameters**:
- `jsonString` (string) - JSON string to import
- `merge` (boolean, optional) - Merge with existing data (default: true)

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.importNotes(jsonString, true);
```

#### `importPokedex(jsonString, merge)`
Imports Pokedex data from JSON.

**Parameters**:
- `jsonString` (string) - JSON string to import
- `merge` (boolean, optional) - Merge with existing data (default: true)

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.importPokedex(jsonString, true);
```

#### `importAllData(jsonString)`
Imports all user data from a backup JSON file.

**Parameters**:
- `jsonString` (string) - JSON string to import

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.importAllData(jsonString);
console.log(result.message); // "Imported 6 data categories!"
```

---

### Sharing Features

#### `generateShareableURL(data)`
Generates a shareable URL with encoded data.

**Parameters**:
- `data` (object) - Data to encode in URL

**Returns**: `string | null` - Shareable URL or null if failed

```javascript
const team = storage.getTeam('1699999999999');
const url = storage.generateShareableURL(team);
console.log(url); // "https://example.com/wowMon.html?share=eyJ..."
```

#### `parseSharedURL()`
Parses shared data from the current URL.

**Returns**: `object | null` - Decoded data or null if not found

```javascript
const sharedData = storage.parseSharedURL();
if (sharedData) {
    console.log('Received shared data:', sharedData);
}
```

#### `copyToClipboard(text)`
Copies text to clipboard.

**Parameters**:
- `text` (string) - Text to copy

**Returns**: `Promise<{success: boolean, message: string}>`

```javascript
storage.copyToClipboard('Hello World').then(result => {
    console.log(result.message); // "Copied to clipboard!"
});
```

---

### Data Management

#### `clearAllData(confirm)`
Clears all stored data.

**Parameters**:
- `confirm` (boolean) - Must be true to proceed

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearAllData(true);
```

#### `clearFavorites(confirm)`
Clears all favorites.

**Parameters**:
- `confirm` (boolean) - Must be true to proceed

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearFavorites(true);
```

#### `clearTeams(confirm)`
Clears all teams.

**Parameters**:
- `confirm` (boolean) - Must be true to proceed

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearTeams(true);
```

#### `clearNotes(confirm)`
Clears all notes.

**Parameters**:
- `confirm` (boolean) - Must be true to proceed

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearNotes(true);
```

#### `clearPokedex(confirm)`
Clears all Pokedex data.

**Parameters**:
- `confirm` (boolean) - Must be true to proceed

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.clearPokedex(true);
```

---

### Download Helpers

#### `downloadJSON(data, filename)`
Downloads data as a JSON file.

**Parameters**:
- `data` (object) - Data to download
- `filename` (string) - Filename for download

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.downloadJSON({ foo: 'bar' }, 'data.json');
```

#### `downloadText(text, filename)`
Downloads text as a file.

**Parameters**:
- `text` (string) - Text to download
- `filename` (string) - Filename for download

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.downloadText('Hello World', 'hello.txt');
```

---

### Auto-Backup

#### `createAutoBackup()`
Creates an automatic backup of all data.

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.createAutoBackup();
```

#### `restoreAutoBackup()`
Restores data from the auto-backup.

**Returns**: `{success: boolean, message: string}`

```javascript
const result = storage.restoreAutoBackup();
```

#### `getAutoBackupInfo()`
Gets information about the auto-backup.

**Returns**: `{exists: boolean, timestamp?: string, date?: string}`

```javascript
const info = storage.getAutoBackupInfo();
if (info.exists) {
    console.log('Backup created:', info.date);
}
```

---

## Usage Examples

### Example 1: Complete Favorites Workflow

```javascript
const storage = new StorageManager();

// Add favorites
storage.saveFavorite('dragon');
storage.saveFavorite('phoenix');
storage.saveFavorite('kobold');

// Check if favorited
if (storage.isFavorite('dragon')) {
    console.log('Dragon is a favorite!');
}

// Get count
console.log(`You have ${storage.getFavoritesCount()} favorites`);

// Export favorites
const exportResult = storage.exportFavorites();
if (exportResult.success) {
    storage.downloadJSON(exportResult.data, 'my-favorites.json');
}

// Toggle favorite
storage.toggleFavorite('dragon'); // Removes it
storage.toggleFavorite('dragon'); // Adds it back
```

### Example 2: Team Management

```javascript
const storage = new StorageManager();

// Create a team
const myTeam = {
    creatures: [
        { id: 'dragon', level: 50, moves: ['fire_breath', 'fly'] },
        { id: 'phoenix', level: 45, moves: ['revive', 'fire_blast'] },
        { id: 'kobold', level: 30, moves: ['scratch', 'bite'] }
    ]
};

// Save the team
const saveResult = storage.saveTeam(myTeam, 'My First Team');
if (saveResult.success) {
    const teamId = saveResult.teamId;

    // Update team name
    storage.updateTeam(teamId, { name: 'Dragon Team' });

    // Export team in Showdown format
    const exportResult = storage.exportTeamShowdownFormat(teamId);
    if (exportResult.success) {
        console.log(exportResult.text);
    }

    // Delete team (with confirmation)
    // storage.deleteTeam(teamId);
}

// List all teams
const teams = storage.getTeams();
teams.forEach(team => {
    console.log(`${team.name}: ${team.creatures.length} creatures`);
});
```

### Example 3: Pokedex Tracking

```javascript
const storage = new StorageManager();

// Mark creatures as seen
storage.markCreatureSeen('kobold');
storage.markCreatureSeen('dragon');

// Mark creatures as caught
storage.markCreatureCaught('kobold');

// Check status
const dragonEntry = storage.getPokedexEntry('dragon');
console.log(`Dragon - Seen: ${dragonEntry.seen}, Caught: ${dragonEntry.caught}`);

// Get overall stats
const stats = storage.getPokedexStats();
console.log(`Pokedex: ${stats.totalCaught}/${stats.totalSeen} caught`);

// Export Pokedex
const exportResult = storage.exportPokedex();
if (exportResult.success) {
    console.log('Pokedex stats:', exportResult.data.stats);
    storage.downloadJSON(exportResult.data, 'pokedex.json');
}
```

### Example 4: Complete Import/Export Workflow

```javascript
const storage = new StorageManager();

// Export all data
const exportResult = storage.exportAllData();
if (exportResult.success) {
    // Save to file
    storage.downloadJSON(exportResult.data, 'wowmon-backup.json');

    // Or copy to clipboard
    storage.copyToClipboard(exportResult.json).then(result => {
        console.log(result.message);
    });

    // Or generate shareable URL
    const shareUrl = storage.generateShareableURL(exportResult.data);
    console.log('Share URL:', shareUrl);
}

// Import from file (user would select file)
function handleFileImport(fileContent) {
    const importResult = storage.importAllData(fileContent);
    if (importResult.success) {
        console.log(importResult.message);
    } else {
        console.error(importResult.message);
    }
}

// Parse shared URL on page load
window.addEventListener('load', () => {
    const sharedData = storage.parseSharedURL();
    if (sharedData) {
        // Handle shared data
        console.log('Received shared data:', sharedData);
    }
});
```

### Example 5: Auto-Backup Integration

```javascript
const storage = new StorageManager();

// Create backup periodically (e.g., every 5 minutes)
setInterval(() => {
    const result = storage.createAutoBackup();
    if (result.success) {
        console.log('Auto-backup created');
    }
}, 5 * 60 * 1000);

// Check for existing backup on startup
const backupInfo = storage.getAutoBackupInfo();
if (backupInfo.exists) {
    console.log('Last backup:', backupInfo.date);

    // Optionally restore if data is corrupted
    // const restoreResult = storage.restoreAutoBackup();
}

// Check storage size
const size = storage.getStorageSizeFormatted();
console.log('Current storage usage:', size);
```

---

## Data Formats

### Export Format Structure

All exports follow this structure:

```javascript
{
    "type": "wowmon_favorites", // Data type identifier
    "version": "1.0",            // Format version
    "timestamp": "2024-01-15T10:30:00.000Z", // Export timestamp
    "data": [ /* actual data */ ]
}
```

### Favorites Export

```json
{
    "type": "wowmon_favorites",
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "data": ["dragon", "phoenix", "kobold"]
}
```

### Teams Export

```json
{
    "type": "wowmon_teams",
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "data": [
        {
            "id": "1699999999999",
            "name": "Fire Team",
            "creatures": [
                {
                    "id": "dragon",
                    "nickname": "Fluffy",
                    "level": 50,
                    "moves": ["fire_breath", "fly"]
                }
            ],
            "createdAt": "2024-01-15T10:00:00.000Z",
            "updatedAt": "2024-01-15T10:30:00.000Z"
        }
    ]
}
```

### Team Showdown Format

```
=== Fire Team ===

Fluffy (dragon)
Level: 50
- fire_breath
- fly

Phoenix (phoenix)
Level: 45
- revive
- fire_blast
```

### Notes Export

```json
{
    "type": "wowmon_notes",
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "data": {
        "dragon": "Very powerful, found in mountains",
        "kobold": "Good for beginners"
    }
}
```

### Pokedex Export

```json
{
    "type": "wowmon_pokedex",
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "data": {
        "dragon": {
            "seen": true,
            "caught": true,
            "firstSeenAt": "2024-01-15T09:00:00.000Z",
            "firstCaughtAt": "2024-01-15T10:00:00.000Z"
        },
        "kobold": {
            "seen": true,
            "caught": false,
            "firstSeenAt": "2024-01-15T08:00:00.000Z"
        }
    },
    "stats": {
        "totalSeen": 2,
        "totalCaught": 1,
        "total": 2
    }
}
```

### All Data Export

```json
{
    "type": "wowmon_all_data",
    "version": "1.0",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "data": {
        "favorites": ["dragon", "phoenix"],
        "teams": [ /* team objects */ ],
        "notes": { /* notes object */ },
        "preferences": { /* preferences object */ },
        "searchHistory": ["dragon", "fire"],
        "pokedex": { /* pokedex object */ }
    }
}
```

---

## Error Handling

All methods that modify data return a result object with this structure:

```javascript
{
    success: boolean,
    message: string,
    // ... additional fields depending on method
}
```

### Example Error Handling

```javascript
const result = storage.saveFavorite('dragon');

if (result.success) {
    // Success
    console.log(result.message); // "Added to favorites!"
} else {
    // Error
    console.error(result.message); // "Already in favorites"
}
```

### Common Error Scenarios

1. **Storage Not Available**: Browser doesn't support localStorage
2. **Quota Exceeded**: Storage limit reached
3. **Invalid Data**: Import data is malformed or wrong type
4. **Not Found**: Trying to access non-existent item
5. **Limit Reached**: Maximum number of items (teams, search history) reached

### Handling Storage Quota Errors

```javascript
try {
    const result = storage.saveFavorite('dragon');
    if (!result.success) {
        if (result.message.includes('quota')) {
            // Storage is full
            alert('Storage is full! Please export and clear some data.');
        }
    }
} catch (error) {
    if (error.name === 'QuotaExceededError') {
        alert('Storage quota exceeded!');
    }
}
```

---

## Best Practices

### 1. Check Storage Availability

Always check if storage is available before using:

```javascript
if (!storage.isStorageAvailable()) {
    alert('Storage is not available. Data will not be saved.');
    return;
}
```

### 2. Handle Errors Gracefully

Always check result.success:

```javascript
const result = storage.saveTeam(team, 'My Team');
if (!result.success) {
    alert(result.message);
    return;
}
```

### 3. Validate Before Import

Validate data before importing:

```javascript
try {
    const data = JSON.parse(fileContent);
    const validation = storage.validateImportData(data);
    if (!validation.valid) {
        alert(validation.message);
        return;
    }
    storage.importAllData(fileContent);
} catch (error) {
    alert('Invalid JSON file');
}
```

### 4. Confirm Destructive Actions

Always require confirmation for destructive actions:

```javascript
if (confirm('Are you sure you want to clear all data?')) {
    const result = storage.clearAllData(true);
    console.log(result.message);
}
```

### 5. Monitor Storage Size

Regularly check storage size:

```javascript
const size = storage.getStorageSize();
const maxSize = storage.MAX_STORAGE_SIZE;
const percentUsed = (size / maxSize) * 100;

if (percentUsed > 80) {
    alert('Storage is 80% full! Consider exporting and clearing old data.');
}
```

### 6. Create Regular Backups

Implement auto-backup:

```javascript
// Create backup on major actions
function saveTeamWithBackup(team, name) {
    const result = storage.saveTeam(team, name);
    if (result.success) {
        storage.createAutoBackup();
    }
    return result;
}
```

### 7. Use Merge When Importing

When importing, use merge=true to preserve existing data:

```javascript
// Merge with existing favorites
storage.importFavorites(jsonString, true);

// Replace all favorites
storage.importFavorites(jsonString, false);
```

### 8. Provide Export Options

Give users multiple export options:

```javascript
function exportUserData() {
    const result = storage.exportAllData();
    if (!result.success) {
        alert('Export failed');
        return;
    }

    // Option 1: Download JSON file
    storage.downloadJSON(result.data, 'wowmon-backup.json');

    // Option 2: Copy to clipboard
    storage.copyToClipboard(result.json);

    // Option 3: Generate share URL
    const shareUrl = storage.generateShareableURL(result.data);
    console.log('Share URL:', shareUrl);
}
```

---

## Integration with GameEngine

To integrate with the existing GameEngine in wowMon.html:

```javascript
class GameEngine {
    constructor() {
        // ... existing code ...

        // Initialize storage manager
        this.storage = new StorageManager();

        // Load preferences
        const prefs = this.storage.getPreferences();
        if (prefs.autoSave) {
            this.enableAutoSave();
        }
    }

    // Hook into creature caught event
    onCreatureCaught(creatureId) {
        // Mark in Pokedex
        this.storage.markCreatureCaught(creatureId);

        // Show stats
        const stats = this.storage.getPokedexStats();
        this.showText(`Pokedex: ${stats.totalCaught}/${stats.totalSeen}`);
    }

    // Hook into creature seen event
    onCreatureSeen(creatureId) {
        this.storage.markCreatureSeen(creatureId);
    }

    // Auto-save integration
    enableAutoSave() {
        setInterval(() => {
            this.storage.createAutoBackup();
        }, 5 * 60 * 1000); // Every 5 minutes
    }
}
```

---

## Troubleshooting

### Issue: Storage Not Working

**Solution**: Check if localStorage is available and enabled in browser settings.

```javascript
if (!storage.isStorageAvailable()) {
    console.error('localStorage is not available');
    // Check browser settings or privacy mode
}
```

### Issue: Quota Exceeded

**Solution**: Clear old data or export and reset.

```javascript
const size = storage.getStorageSizeFormatted();
console.log('Current usage:', size);

// Export before clearing
const backup = storage.exportAllData();
storage.downloadJSON(backup.data, 'backup.json');

// Clear old data
storage.clearSearchHistory(true);
```

### Issue: Import Fails

**Solution**: Validate the import file format.

```javascript
try {
    const data = JSON.parse(fileContent);
    const validation = storage.validateImportData(data);
    if (!validation.valid) {
        console.error('Validation failed:', validation.message);
    }
} catch (error) {
    console.error('Invalid JSON:', error);
}
```

---

## Future Enhancements

Potential future improvements:

1. **Compression**: Compress data before storing to save space
2. **IndexedDB**: Use IndexedDB for larger storage limits
3. **Cloud Sync**: Optional cloud backup integration
4. **Versioning**: Track data version for migrations
5. **Encryption**: Encrypt sensitive data
6. **Undo/Redo**: Implement undo/redo for data changes
7. **Conflict Resolution**: Better handling of import conflicts
8. **Data Analytics**: Track usage patterns and statistics

---

## License

This StorageManager is part of the WoWmon project and follows the same license as the main project.

---

## Support

For issues or questions about the StorageManager, please refer to the main WoWmon project documentation or create an issue in the project repository.
