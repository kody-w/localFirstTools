/**
 * Storage Manager - localStorage abstraction with migrations
 * Local First Tools v2
 */

import { STORAGE_KEYS, STORAGE_PREFIX } from '../core/constants.js';

/**
 * @typedef {Object} StorageOptions
 * @property {string} prefix - Key prefix for namespacing
 * @property {number} version - Storage schema version
 */

class StorageManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {StorageManager}
     */
    static getInstance() {
        if (!StorageManager.#instance) {
            StorageManager.#instance = new StorageManager();
        }
        return StorageManager.#instance;
    }

    constructor() {
        if (StorageManager.#instance) {
            throw new Error('Use StorageManager.getInstance() instead of new StorageManager()');
        }

        this.#prefix = STORAGE_PREFIX;
        this.#version = 1;
        this.#isAvailable = this.#checkAvailability();

        if (this.#isAvailable) {
            this.#runMigrations();
        }
    }

    #prefix;
    #version;
    #isAvailable;

    /**
     * Check if localStorage is available
     * @returns {boolean}
     */
    #checkAvailability() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return false;
        }
    }

    /**
     * Run migrations from v1 to v2 storage format
     */
    #runMigrations() {
        const migrationKey = `${this.#prefix}migration_version`;
        const currentVersion = this.get(migrationKey) || 0;

        if (currentVersion < this.#version) {
            this.#migrateFromV1();
            this.set(migrationKey, this.#version);
        }
    }

    /**
     * Migrate v1 localStorage data to v2 format
     */
    #migrateFromV1() {
        const v1Keys = {
            'pinnedTools': STORAGE_KEYS.PINNED_TOOLS,
            'votes': STORAGE_KEYS.VOTES,
            'toolUsage': STORAGE_KEYS.USAGE,
            'recentlyOpened': STORAGE_KEYS.RECENTLY_OPENED,
            'collections': STORAGE_KEYS.COLLECTIONS,
            'searchHistory': STORAGE_KEYS.SEARCH_HISTORY,
            'theme': STORAGE_KEYS.THEME,
            'tourCompleted': STORAGE_KEYS.TOUR_COMPLETED,
            'analyticsEnabled': STORAGE_KEYS.ANALYTICS_ENABLED
        };

        for (const [v1Key, v2Key] of Object.entries(v1Keys)) {
            // Check if v1 data exists and v2 doesn't
            const v1Data = this.#getRaw(v1Key);
            const v2Data = this.#getRaw(v2Key);

            if (v1Data !== null && v2Data === null) {
                try {
                    const parsed = JSON.parse(v1Data);
                    this.set(v2Key, parsed);
                    console.log(`Migrated ${v1Key} to ${v2Key}`);
                } catch (e) {
                    // If not JSON, store as-is
                    this.#setRaw(v2Key, v1Data);
                }
            }
        }
    }

    /**
     * Get raw value from localStorage
     * @param {string} key
     * @returns {string|null}
     */
    #getRaw(key) {
        if (!this.#isAvailable) return null;
        return localStorage.getItem(key);
    }

    /**
     * Set raw value in localStorage
     * @param {string} key
     * @param {string} value
     */
    #setRaw(key, value) {
        if (!this.#isAvailable) return;
        localStorage.setItem(key, value);
    }

    /**
     * Get value from storage
     * @template T
     * @param {string} key - Storage key
     * @param {T} [defaultValue] - Default value if key doesn't exist
     * @returns {T|null}
     */
    get(key, defaultValue = null) {
        if (!this.#isAvailable) return defaultValue;

        try {
            const item = localStorage.getItem(key);
            if (item === null) return defaultValue;
            return JSON.parse(item);
        } catch (e) {
            console.warn(`Error reading ${key} from storage:`, e);
            return defaultValue;
        }
    }

    /**
     * Set value in storage
     * @param {string} key - Storage key
     * @param {any} value - Value to store
     * @returns {boolean} Success status
     */
    set(key, value) {
        if (!this.#isAvailable) return false;

        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            if (e.name === 'QuotaExceededError') {
                console.error('Storage quota exceeded');
                this.#handleQuotaExceeded();
            } else {
                console.error(`Error writing ${key} to storage:`, e);
            }
            return false;
        }
    }

    /**
     * Remove item from storage
     * @param {string} key - Storage key
     */
    remove(key) {
        if (!this.#isAvailable) return;
        localStorage.removeItem(key);
    }

    /**
     * Check if key exists in storage
     * @param {string} key - Storage key
     * @returns {boolean}
     */
    has(key) {
        if (!this.#isAvailable) return false;
        return localStorage.getItem(key) !== null;
    }

    /**
     * Get all keys with the v2 prefix
     * @returns {string[]}
     */
    keys() {
        if (!this.#isAvailable) return [];

        const keys = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.#prefix)) {
                keys.push(key);
            }
        }
        return keys;
    }

    /**
     * Clear all v2 storage (preserves v1 data)
     */
    clear() {
        if (!this.#isAvailable) return;

        const keysToRemove = this.keys();
        for (const key of keysToRemove) {
            localStorage.removeItem(key);
        }
    }

    /**
     * Get storage usage statistics
     * @returns {Object}
     */
    getStats() {
        if (!this.#isAvailable) {
            return { used: 0, available: 0, items: 0 };
        }

        let used = 0;
        let items = 0;

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.#prefix)) {
                const value = localStorage.getItem(key);
                used += key.length + (value?.length || 0);
                items++;
            }
        }

        return {
            used,
            usedKB: Math.round(used / 1024 * 100) / 100,
            items,
            // Most browsers have 5MB limit
            estimatedAvailable: 5 * 1024 * 1024 - used
        };
    }

    /**
     * Handle storage quota exceeded
     */
    #handleQuotaExceeded() {
        // Try to free up space by clearing old data
        const keysToConsider = [
            STORAGE_KEYS.SEARCH_HISTORY,
            STORAGE_KEYS.RECENTLY_OPENED
        ];

        for (const key of keysToConsider) {
            const data = this.get(key);
            if (Array.isArray(data) && data.length > 10) {
                // Keep only last 10 items
                this.set(key, data.slice(-10));
            }
        }
    }

    /**
     * Export all v2 data
     * @returns {Object}
     */
    export() {
        const data = {};
        for (const key of this.keys()) {
            data[key] = this.get(key);
        }
        return {
            version: this.#version,
            exportedAt: new Date().toISOString(),
            data
        };
    }

    /**
     * Import data from export
     * @param {Object} exportData
     * @returns {boolean}
     */
    import(exportData) {
        if (!exportData?.data) {
            console.error('Invalid export data');
            return false;
        }

        try {
            for (const [key, value] of Object.entries(exportData.data)) {
                this.set(key, value);
            }
            return true;
        } catch (e) {
            console.error('Error importing data:', e);
            return false;
        }
    }

    /**
     * Check if storage is available
     * @returns {boolean}
     */
    isAvailable() {
        return this.#isAvailable;
    }
}

export { StorageManager };
