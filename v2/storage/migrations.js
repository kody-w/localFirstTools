/**
 * Migrations - v1 to v2 data migration
 * Local First Tools v2
 */

/**
 * Migration version
 */
const CURRENT_VERSION = 2;

/**
 * v1 storage keys to migrate
 */
const V1_KEYS = {
    pinnedTools: 'pinnedTools',
    votes: 'votes',
    toolUsage: 'toolUsage',
    collections: 'collections',
    theme: 'vibeGalleryTheme',
    gridSize: 'vibeGalleryGridSize',
    viewMode: 'vibeGalleryViewMode',
    searchHistory: 'searchHistory',
    favorites: 'favorites',
    lastVisit: 'lastVisit'
};

/**
 * v2 storage key prefix
 */
const V2_PREFIX = 'lft_v2_';

class MigrationManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {MigrationManager}
     */
    static getInstance() {
        if (!MigrationManager.#instance) {
            MigrationManager.#instance = new MigrationManager();
        }
        return MigrationManager.#instance;
    }

    constructor() {
        if (MigrationManager.#instance) {
            return MigrationManager.#instance;
        }

        this.#migrated = false;
        this.#migrationLog = [];
    }

    #migrated;
    #migrationLog;

    /**
     * Check if migration is needed
     * @returns {boolean}
     */
    needsMigration() {
        const version = this.#getStoredVersion();
        return version < CURRENT_VERSION;
    }

    /**
     * Get stored version
     * @returns {number}
     */
    #getStoredVersion() {
        try {
            const version = localStorage.getItem(`${V2_PREFIX}version`);
            return version ? parseInt(version, 10) : 0;
        } catch {
            return 0;
        }
    }

    /**
     * Run all pending migrations
     * @returns {Object}
     */
    async migrate() {
        const startVersion = this.#getStoredVersion();
        this.#migrationLog = [];

        if (startVersion >= CURRENT_VERSION) {
            return { success: true, message: 'Already up to date', log: [] };
        }

        try {
            // Run migrations in order
            if (startVersion < 1) {
                await this.#migrateToV1();
            }
            if (startVersion < 2) {
                await this.#migrateToV2();
            }

            // Update version
            localStorage.setItem(`${V2_PREFIX}version`, CURRENT_VERSION.toString());
            this.#migrated = true;

            return {
                success: true,
                message: `Migrated from v${startVersion} to v${CURRENT_VERSION}`,
                log: this.#migrationLog
            };
        } catch (error) {
            return {
                success: false,
                message: error.message,
                log: this.#migrationLog
            };
        }
    }

    /**
     * Migrate to v1 (initial structure)
     */
    async #migrateToV1() {
        this.#log('Starting v1 migration...');

        // Migrate pinned tools
        this.#migrateKey(V1_KEYS.pinnedTools, 'pins', (data) => {
            if (Array.isArray(data)) {
                return data.map(id => ({
                    id,
                    pinnedAt: Date.now()
                }));
            }
            return [];
        });

        // Migrate votes
        this.#migrateKey(V1_KEYS.votes, 'votes', (data) => {
            if (typeof data === 'object') {
                return Object.entries(data).map(([id, count]) => ({
                    toolId: id,
                    count,
                    lastVoted: Date.now()
                }));
            }
            return [];
        });

        // Migrate tool usage
        this.#migrateKey(V1_KEYS.toolUsage, 'usage', (data) => {
            if (typeof data === 'object') {
                return Object.entries(data).map(([id, usage]) => ({
                    toolId: id,
                    openCount: typeof usage === 'number' ? usage : usage.count || 0,
                    lastOpened: usage.lastOpened || Date.now()
                }));
            }
            return [];
        });

        // Migrate collections
        this.#migrateKey(V1_KEYS.collections, 'collections', (data) => {
            if (Array.isArray(data)) {
                return data.map(col => ({
                    ...col,
                    id: col.id || `col_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    createdAt: col.createdAt || Date.now(),
                    updatedAt: col.updatedAt || Date.now()
                }));
            }
            return [];
        });

        // Migrate theme
        this.#migrateKey(V1_KEYS.theme, 'theme', (data) => {
            // Map old theme names to new
            const themeMap = {
                'dark': 'dark',
                'light': 'light',
                'system': 'system',
                'high-contrast': 'highContrast'
            };
            return themeMap[data] || 'dark';
        });

        // Migrate view preferences
        this.#migrateKey(V1_KEYS.viewMode, 'viewMode');
        this.#migrateKey(V1_KEYS.gridSize, 'gridSize');

        // Migrate search history
        this.#migrateKey(V1_KEYS.searchHistory, 'searchHistory', (data) => {
            if (Array.isArray(data)) {
                return data.slice(0, 50).map(query => ({
                    query,
                    searchedAt: Date.now()
                }));
            }
            return [];
        });

        this.#log('v1 migration complete');
    }

    /**
     * Migrate to v2 (enhanced structure)
     */
    async #migrateToV2() {
        this.#log('Starting v2 migration...');

        // Add analytics tracking
        const usage = this.#getV2Data('usage') || [];
        if (usage.length > 0) {
            const analytics = {
                totalOpens: usage.reduce((sum, u) => sum + u.openCount, 0),
                uniqueTools: usage.length,
                firstTracked: Math.min(...usage.map(u => u.lastOpened)),
                lastActivity: Math.max(...usage.map(u => u.lastOpened))
            };
            this.#setV2Data('analytics_summary', analytics);
            this.#log('Created analytics summary');
        }

        // Add collection metadata
        const collections = this.#getV2Data('collections') || [];
        if (collections.length > 0) {
            const enhancedCollections = collections.map(col => ({
                ...col,
                color: col.color || this.#generateColor(),
                icon: col.icon || '📁',
                isDefault: col.name?.toLowerCase() === 'favorites'
            }));
            this.#setV2Data('collections', enhancedCollections);
            this.#log('Enhanced collections with metadata');
        }

        // Create default favorites collection if none exists
        const hasFavorites = collections.some(c => c.name?.toLowerCase() === 'favorites');
        if (!hasFavorites) {
            const pins = this.#getV2Data('pins') || [];
            const favoritesCollection = {
                id: 'col_favorites',
                name: 'Favorites',
                description: 'Your favorite tools',
                icon: '⭐',
                color: '#FBBF24',
                tools: pins.map(p => p.id),
                isDefault: true,
                createdAt: Date.now(),
                updatedAt: Date.now()
            };
            const updatedCollections = [...collections, favoritesCollection];
            this.#setV2Data('collections', updatedCollections);
            this.#log('Created default favorites collection');
        }

        // Set migration timestamp
        this.#setV2Data('migration_timestamp', Date.now());

        this.#log('v2 migration complete');
    }

    /**
     * Migrate a single key
     * @param {string} v1Key
     * @param {string} v2Key
     * @param {Function} transformer
     */
    #migrateKey(v1Key, v2Key, transformer = null) {
        try {
            const v1Data = localStorage.getItem(v1Key);
            if (v1Data === null) return;

            let data = JSON.parse(v1Data);

            if (transformer) {
                data = transformer(data);
            }

            this.#setV2Data(v2Key, data);
            this.#log(`Migrated ${v1Key} -> ${v2Key}`);
        } catch (error) {
            this.#log(`Failed to migrate ${v1Key}: ${error.message}`);
        }
    }

    /**
     * Get v2 data
     * @param {string} key
     * @returns {*}
     */
    #getV2Data(key) {
        try {
            const data = localStorage.getItem(`${V2_PREFIX}${key}`);
            return data ? JSON.parse(data) : null;
        } catch {
            return null;
        }
    }

    /**
     * Set v2 data
     * @param {string} key
     * @param {*} value
     */
    #setV2Data(key, value) {
        localStorage.setItem(`${V2_PREFIX}${key}`, JSON.stringify(value));
    }

    /**
     * Log migration step
     * @param {string} message
     */
    #log(message) {
        const entry = {
            timestamp: Date.now(),
            message
        };
        this.#migrationLog.push(entry);
        console.log(`[Migration] ${message}`);
    }

    /**
     * Generate random color
     * @returns {string}
     */
    #generateColor() {
        const colors = [
            '#FF6B6B', '#4ECDC4', '#A78BFA', '#F472B6',
            '#60A5FA', '#34D399', '#FBBF24', '#FB7185'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    /**
     * Get migration log
     * @returns {Array}
     */
    getMigrationLog() {
        return [...this.#migrationLog];
    }

    /**
     * Check if migrated
     * @returns {boolean}
     */
    isMigrated() {
        return this.#migrated;
    }

    /**
     * Get current version
     * @returns {number}
     */
    getCurrentVersion() {
        return CURRENT_VERSION;
    }

    /**
     * Reset migration (for testing)
     */
    reset() {
        localStorage.removeItem(`${V2_PREFIX}version`);
        this.#migrated = false;
        this.#migrationLog = [];
    }

    /**
     * Export v1 data for backup
     * @returns {Object}
     */
    exportV1Data() {
        const data = {};

        for (const [name, key] of Object.entries(V1_KEYS)) {
            try {
                const value = localStorage.getItem(key);
                if (value !== null) {
                    data[name] = JSON.parse(value);
                }
            } catch {
                // Skip invalid data
            }
        }

        return data;
    }
}

export { MigrationManager, CURRENT_VERSION, V1_KEYS, V2_PREFIX };
