/**
 * Game Store Data Models and Storage Services
 *
 * A comprehensive collection of ES6 classes for managing game data,
 * state management, and local storage in a game store application.
 *
 * @version 1.0.0
 * @author Steam Deck Game Store
 */

'use strict';

// ========================================
// CONFIGURATION
// ========================================

/**
 * Application configuration object
 * Contains repository information, categories, and storage keys
 */
const AppConfig = {
    // GitHub repository configuration
    repository: {
        owner: 'kody-w',
        name: 'localFirstTools',
        branch: 'main'
    },

    // Game categories for filtering and organization
    categories: [
        'all',
        'action',
        'puzzle',
        'arcade',
        'strategy',
        'adventure'
    ],

    // LocalStorage keys for persistent data
    storage: {
        favorites: 'steamDeck_favorites_v1',
        installed: 'steamDeck_installed_v1',
        localGames: 'steamDeck_localGames_v1',
        settings: 'steamDeck_settings_v1'
    },

    // Animation timing constants (in milliseconds)
    animation: {
        short: 200,
        medium: 300,
        long: 500
    }
};

// ========================================
// DATA MODELS
// ========================================

/**
 * Game class representing a single game in the store
 *
 * @class Game
 * @property {string} id - Unique identifier for the game
 * @property {string} name - Display name of the game
 * @property {string} description - Brief description of the game
 * @property {string} icon - Emoji or icon representing the game
 * @property {string} category - Game category (action, puzzle, etc.)
 * @property {string} url - URL to the game file or resource
 * @property {string} size - File size as formatted string (e.g., "2 MB")
 * @property {boolean} isLocal - Whether the game is stored locally
 * @property {string|null} code - Complete HTML/JS code for local games
 * @property {string} author - Author/creator of the game
 * @property {string} version - Version number of the game
 */
class Game {
    /**
     * Creates a new Game instance
     * @param {Object} data - Game data object
     * @param {string} data.id - Unique game identifier
     * @param {string} data.name - Game name
     * @param {string} data.description - Game description
     * @param {string} data.icon - Game icon/emoji
     * @param {string} data.category - Game category
     * @param {string} data.url - Game URL
     * @param {string} data.size - Game file size
     * @param {boolean} data.isLocal - Is local game flag
     * @param {string} data.code - Game code (for local games)
     * @param {string} data.author - Game author
     * @param {string} data.version - Game version
     */
    constructor(data) {
        this.id = data.id || '';
        this.name = data.name || 'Unknown Game';
        this.description = data.description || 'No description available';
        this.icon = data.icon || '🎮';
        this.category = data.category || 'arcade';
        this.url = data.url || '';
        this.size = data.size || '0 KB';
        this.isLocal = data.isLocal || false;
        this.code = data.code || null;
        this.author = data.author || 'Unknown';
        this.version = data.version || '1.0';
    }

    /**
     * Converts the Game instance to a JSON-serializable object
     * Primarily used for exporting local games
     *
     * @returns {Object} JSON representation of the game
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            icon: this.icon,
            category: this.category,
            url: this.url,
            size: this.size,
            author: this.author,
            version: this.version,
            code: this.code,
            isLocal: true
        };
    }

    /**
     * Validates that the game has all required fields
     *
     * @returns {boolean} True if valid, false otherwise
     */
    isValid() {
        return !!(this.id && this.name && (this.url || this.code));
    }

    /**
     * Creates a clone of the game instance
     *
     * @returns {Game} Cloned game instance
     */
    clone() {
        return new Game(this.toJSON());
    }
}

// ========================================
// STATE MANAGEMENT
// ========================================

/**
 * StateManager class for managing application state
 * Implements a publish-subscribe pattern for reactive state updates
 *
 * @class StateManager
 */
class StateManager {
    /**
     * Initializes the StateManager with default state
     */
    constructor() {
        // Application state object
        this.state = {
            games: [],                      // Array of all Game instances
            filteredGames: [],              // Currently filtered/displayed games
            currentView: 'store',           // Current view: 'store', 'library', 'create', 'settings'
            currentCategory: 'all',         // Currently selected category filter
            searchQuery: '',                // Current search query string
            favorites: new Set(),           // Set of favorite game IDs
            installedGames: new Set(),      // Set of installed game IDs
            selectedIndex: 0,               // Currently selected game index (for keyboard/gamepad navigation)
            inputMode: 'mouse'              // Current input mode: 'mouse', 'keyboard', 'gamepad', 'touch'
        };

        // Map of state keys to subscriber callbacks
        // Key: state property name
        // Value: Set of callback functions
        this.subscribers = new Map();
    }

    /**
     * Updates one or more state properties and notifies subscribers
     *
     * @param {Object} updates - Object containing state properties to update
     * @example
     * stateManager.setState({ currentView: 'library', searchQuery: 'puzzle' });
     */
    setState(updates) {
        // Merge updates into current state
        Object.assign(this.state, updates);

        // Notify subscribers for each updated property
        this.notify(Object.keys(updates));
    }

    /**
     * Gets the current state object (returns a shallow copy)
     *
     * @returns {Object} Copy of the current state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Gets a specific state property value
     *
     * @param {string} key - State property key
     * @returns {*} Value of the state property
     */
    get(key) {
        return this.state[key];
    }

    /**
     * Subscribes to state changes for a specific property
     * Returns an unsubscribe function
     *
     * @param {string} key - State property to watch
     * @param {Function} callback - Function to call when property changes
     * @returns {Function} Unsubscribe function
     * @example
     * const unsubscribe = stateManager.subscribe('games', (games) => {
     *   console.log('Games updated:', games);
     * });
     * // Later: unsubscribe();
     */
    subscribe(key, callback) {
        // Create Set for this key if it doesn't exist
        if (!this.subscribers.has(key)) {
            this.subscribers.set(key, new Set());
        }

        // Add callback to subscribers
        this.subscribers.get(key).add(callback);

        // Return unsubscribe function
        return () => this.subscribers.get(key).delete(callback);
    }

    /**
     * Notifies all subscribers for the given state keys
     * Internal method called by setState
     *
     * @private
     * @param {string[]} keys - Array of state property keys that changed
     */
    notify(keys) {
        keys.forEach(key => {
            const callbacks = this.subscribers.get(key);
            if (callbacks) {
                // Call each subscriber callback with the new value
                callbacks.forEach(callback => {
                    try {
                        callback(this.state[key]);
                    } catch (error) {
                        console.error(`Error in subscriber callback for ${key}:`, error);
                    }
                });
            }
        });
    }

    /**
     * Resets the state to initial values
     */
    reset() {
        this.state = {
            games: [],
            filteredGames: [],
            currentView: 'store',
            currentCategory: 'all',
            searchQuery: '',
            favorites: new Set(),
            installedGames: new Set(),
            selectedIndex: 0,
            inputMode: 'mouse'
        };

        // Notify all subscribers of the reset
        this.notify(Object.keys(this.state));
    }

    /**
     * Removes all subscribers
     */
    clearSubscribers() {
        this.subscribers.clear();
    }
}

// ========================================
// STORAGE SERVICE
// ========================================

/**
 * StorageService provides static methods for localStorage operations
 * Handles saving, loading, and removing data with error handling
 *
 * @class StorageService
 */
class StorageService {
    /**
     * Saves data to localStorage with JSON serialization
     *
     * @static
     * @param {string} key - Storage key
     * @param {*} data - Data to save (will be JSON stringified)
     * @returns {boolean} True if successful, false otherwise
     * @example
     * StorageService.save('myKey', { name: 'Game', score: 100 });
     */
    static save(key, data) {
        try {
            const jsonString = JSON.stringify(data);
            localStorage.setItem(key, jsonString);
            return true;
        } catch (error) {
            console.error('Storage save error:', error);

            // Handle QuotaExceededError
            if (error.name === 'QuotaExceededError') {
                console.error('LocalStorage quota exceeded');
            }

            return false;
        }
    }

    /**
     * Loads data from localStorage with JSON parsing
     *
     * @static
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if key doesn't exist or parsing fails
     * @returns {*} Parsed data or default value
     * @example
     * const data = StorageService.load('myKey', { name: 'Default' });
     */
    static load(key, defaultValue = null) {
        try {
            const jsonString = localStorage.getItem(key);

            // Return default if key doesn't exist
            if (jsonString === null) {
                return defaultValue;
            }

            return JSON.parse(jsonString);
        } catch (error) {
            console.error('Storage load error:', error);
            return defaultValue;
        }
    }

    /**
     * Removes an item from localStorage
     *
     * @static
     * @param {string} key - Storage key to remove
     * @returns {boolean} True if successful, false otherwise
     */
    static remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Storage remove error:', error);
            return false;
        }
    }

    /**
     * Saves local games to localStorage
     * Filters for local games only and serializes them
     *
     * @static
     * @param {Game[]} games - Array of Game instances
     * @returns {boolean} True if successful, false otherwise
     */
    static saveLocalGames(games) {
        // Filter for local games and convert to JSON
        const localGames = games
            .filter(game => game.isLocal)
            .map(game => game.toJSON());

        return StorageService.save(AppConfig.storage.localGames, localGames);
    }

    /**
     * Loads local games from localStorage
     * Returns array of Game instances
     *
     * @static
     * @returns {Game[]} Array of Game instances
     */
    static loadLocalGames() {
        const savedData = StorageService.load(AppConfig.storage.localGames, []);

        // Convert JSON data back to Game instances
        return savedData.map(data => new Game(data));
    }

    /**
     * Saves favorites to localStorage
     *
     * @static
     * @param {Set<string>} favorites - Set of favorite game IDs
     * @returns {boolean} True if successful
     */
    static saveFavorites(favorites) {
        const favoritesArray = Array.from(favorites);
        return StorageService.save(AppConfig.storage.favorites, favoritesArray);
    }

    /**
     * Loads favorites from localStorage
     *
     * @static
     * @returns {Set<string>} Set of favorite game IDs
     */
    static loadFavorites() {
        const favoritesArray = StorageService.load(AppConfig.storage.favorites, []);
        return new Set(favoritesArray);
    }

    /**
     * Saves installed games to localStorage
     *
     * @static
     * @param {Set<string>} installedGames - Set of installed game IDs
     * @returns {boolean} True if successful
     */
    static saveInstalledGames(installedGames) {
        const installedArray = Array.from(installedGames);
        return StorageService.save(AppConfig.storage.installed, installedArray);
    }

    /**
     * Loads installed games from localStorage
     *
     * @static
     * @returns {Set<string>} Set of installed game IDs
     */
    static loadInstalledGames() {
        const installedArray = StorageService.load(AppConfig.storage.installed, []);
        return new Set(installedArray);
    }

    /**
     * Clears all game store data from localStorage
     * Removes favorites, installed games, and local games
     *
     * @static
     * @returns {boolean} True if successful
     */
    static clearAll() {
        try {
            StorageService.remove(AppConfig.storage.favorites);
            StorageService.remove(AppConfig.storage.installed);
            StorageService.remove(AppConfig.storage.localGames);
            StorageService.remove(AppConfig.storage.settings);
            return true;
        } catch (error) {
            console.error('Error clearing storage:', error);
            return false;
        }
    }

    /**
     * Gets the total size of stored data in bytes (approximate)
     *
     * @static
     * @returns {number} Total size in bytes
     */
    static getStorageSize() {
        let totalSize = 0;

        try {
            for (let key in localStorage) {
                if (localStorage.hasOwnProperty(key)) {
                    totalSize += localStorage[key].length + key.length;
                }
            }
        } catch (error) {
            console.error('Error calculating storage size:', error);
        }

        return totalSize;
    }

    /**
     * Checks if localStorage is available
     *
     * @static
     * @returns {boolean} True if localStorage is available
     */
    static isAvailable() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Exports all game store data as a JSON object
     *
     * @static
     * @returns {Object} All stored data
     */
    static exportAllData() {
        return {
            version: '1.0',
            exported: new Date().toISOString(),
            favorites: StorageService.load(AppConfig.storage.favorites, []),
            installed: StorageService.load(AppConfig.storage.installed, []),
            localGames: StorageService.load(AppConfig.storage.localGames, []),
            settings: StorageService.load(AppConfig.storage.settings, {})
        };
    }

    /**
     * Imports game store data from an exported object
     *
     * @static
     * @param {Object} data - Exported data object
     * @returns {boolean} True if successful
     */
    static importAllData(data) {
        try {
            if (data.favorites) {
                StorageService.save(AppConfig.storage.favorites, data.favorites);
            }
            if (data.installed) {
                StorageService.save(AppConfig.storage.installed, data.installed);
            }
            if (data.localGames) {
                StorageService.save(AppConfig.storage.localGames, data.localGames);
            }
            if (data.settings) {
                StorageService.save(AppConfig.storage.settings, data.settings);
            }
            return true;
        } catch (error) {
            console.error('Error importing data:', error);
            return false;
        }
    }
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * GameUtils provides utility functions for game operations
 *
 * @class GameUtils
 */
class GameUtils {
    /**
     * Filters games based on criteria
     *
     * @static
     * @param {Game[]} games - Array of games to filter
     * @param {Object} filters - Filter criteria
     * @param {string} filters.category - Category to filter by
     * @param {string} filters.searchQuery - Search query string
     * @param {Set<string>} filters.installedOnly - Only show installed games
     * @returns {Game[]} Filtered games array
     */
    static filterGames(games, filters = {}) {
        let filtered = [...games];

        // Filter by category
        if (filters.category && filters.category !== 'all') {
            filtered = filtered.filter(game => game.category === filters.category);
        }

        // Filter by search query
        if (filters.searchQuery) {
            const query = filters.searchQuery.toLowerCase();
            filtered = filtered.filter(game =>
                game.name.toLowerCase().includes(query) ||
                game.description.toLowerCase().includes(query) ||
                game.category.toLowerCase().includes(query)
            );
        }

        // Filter installed only
        if (filters.installedOnly && filters.installedGames) {
            filtered = filtered.filter(game =>
                filters.installedGames.has(game.id)
            );
        }

        return filtered;
    }

    /**
     * Sorts games by various criteria
     *
     * @static
     * @param {Game[]} games - Array of games to sort
     * @param {string} sortBy - Sort criteria: 'name', 'category', 'size', 'author'
     * @param {boolean} ascending - Sort direction
     * @returns {Game[]} Sorted games array
     */
    static sortGames(games, sortBy = 'name', ascending = true) {
        const sorted = [...games];

        sorted.sort((a, b) => {
            let comparison = 0;

            switch (sortBy) {
                case 'name':
                    comparison = a.name.localeCompare(b.name);
                    break;
                case 'category':
                    comparison = a.category.localeCompare(b.category);
                    break;
                case 'author':
                    comparison = a.author.localeCompare(b.author);
                    break;
                case 'size':
                    // Simple size comparison (would need more sophisticated parsing)
                    comparison = a.size.localeCompare(b.size);
                    break;
                default:
                    comparison = 0;
            }

            return ascending ? comparison : -comparison;
        });

        return sorted;
    }

    /**
     * Validates game data structure
     *
     * @static
     * @param {Object} data - Game data to validate
     * @returns {Object} Validation result { valid: boolean, errors: string[] }
     */
    static validateGameData(data) {
        const errors = [];

        if (!data.name || typeof data.name !== 'string') {
            errors.push('Game name is required and must be a string');
        }

        if (!data.id || typeof data.id !== 'string') {
            errors.push('Game ID is required and must be a string');
        }

        if (data.isLocal && !data.code) {
            errors.push('Local games must have code property');
        }

        if (!data.isLocal && !data.url) {
            errors.push('Remote games must have a URL');
        }

        if (data.category && !AppConfig.categories.includes(data.category)) {
            errors.push(`Invalid category. Must be one of: ${AppConfig.categories.join(', ')}`);
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }

    /**
     * Generates a unique game ID
     *
     * @static
     * @param {string} prefix - ID prefix (default: 'game')
     * @returns {string} Unique game ID
     */
    static generateGameId(prefix = 'game') {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `${prefix}-${timestamp}-${random}`;
    }

    /**
     * Formats file size from bytes
     *
     * @static
     * @param {number} bytes - Size in bytes
     * @returns {string} Formatted size string
     */
    static formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + ' KB';
        return Math.round(bytes / (1024 * 1024)) + ' MB';
    }
}

// ========================================
// EXPORTS (for module usage)
// ========================================

// For ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AppConfig,
        Game,
        StateManager,
        StorageService,
        GameUtils
    };
}

// For browser global usage
if (typeof window !== 'undefined') {
    window.GameStore = {
        AppConfig,
        Game,
        StateManager,
        StorageService,
        GameUtils
    };
}
