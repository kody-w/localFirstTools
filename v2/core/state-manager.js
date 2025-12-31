/**
 * State Manager - Central state with pub/sub pattern
 * Local First Tools v2
 */

/**
 * @typedef {Object} GalleryState
 * @property {Array} tools - All loaded tools
 * @property {Array} filteredTools - Currently filtered tools
 * @property {Object|null} config - Gallery configuration
 * @property {Object} filters - Current filter state
 * @property {Object} sort - Current sort state
 * @property {Object} view - Current view state
 * @property {Object} user - User preferences and data
 * @property {Object} ui - UI state
 */

const DEFAULT_STATE = {
    // Data
    tools: [],
    filteredTools: [],
    config: null,
    isLoading: true,
    error: null,

    // Filters
    filters: {
        category: 'all',
        complexity: '',
        type: '',
        featured: '',
        polished: '',
        folder: '',
        tags: new Set(),
        searchTerm: ''
    },

    // Sort
    sort: {
        field: 'name',
        direction: 'asc'
    },

    // View
    view: {
        mode: 'grid', // grid, list, masonry, timeline, dashboard, 3d
        focusedIndex: -1
    },

    // User
    user: {
        pinnedTools: [],
        votes: {},
        usage: {},
        recentlyOpened: [],
        collections: {},
        searchHistory: [],
        theme: 'dark'
    },

    // UI
    ui: {
        comparisonMode: false,
        comparisonTools: [],
        analyticsEnabled: true,
        tourCompleted: false,
        sidebarOpen: false
    }
};

class StateManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {StateManager}
     */
    static getInstance() {
        if (!StateManager.#instance) {
            StateManager.#instance = new StateManager();
        }
        return StateManager.#instance;
    }

    constructor() {
        if (StateManager.#instance) {
            throw new Error('Use StateManager.getInstance() instead of new StateManager()');
        }

        this.#state = this.#deepClone(DEFAULT_STATE);
        this.#listeners = new Map();
        this.#sliceListeners = new Map();
        this.#selectors = new Map();
        this.#selectorCache = new Map();
    }

    /** @type {GalleryState} */
    #state;
    /** @type {Map<Function, Function>} */
    #listeners;
    /** @type {Map<string, Set<Function>>} */
    #sliceListeners;
    /** @type {Map<string, Function>} */
    #selectors;
    /** @type {Map<string, any>} */
    #selectorCache;

    /**
     * Get the entire state (read-only copy)
     * @returns {GalleryState}
     */
    getState() {
        return this.#deepClone(this.#state);
    }

    /**
     * Get a specific slice of state
     * @template K
     * @param {K} key - State key
     * @returns {GalleryState[K]}
     */
    getSlice(key) {
        const value = this.#state[key];
        if (value instanceof Set) {
            return new Set(value);
        }
        if (typeof value === 'object' && value !== null) {
            return this.#deepClone(value);
        }
        return value;
    }

    /**
     * Update state using an updater function
     * @param {Function} updater - Function that receives current state and returns partial update
     */
    setState(updater) {
        const currentState = this.#state;
        const updates = updater(currentState);

        if (!updates || typeof updates !== 'object') {
            return;
        }

        const changedKeys = [];

        for (const [key, value] of Object.entries(updates)) {
            if (!this.#isEqual(currentState[key], value)) {
                this.#state[key] = value;
                changedKeys.push(key);
            }
        }

        if (changedKeys.length > 0) {
            this.#invalidateSelectorCache(changedKeys);
            this.#notifyListeners(changedKeys);
        }
    }

    /**
     * Set a specific slice of state
     * @template K
     * @param {K} key - State key
     * @param {GalleryState[K]} value - New value
     */
    setSlice(key, value) {
        if (!this.#isEqual(this.#state[key], value)) {
            this.#state[key] = value;
            this.#invalidateSelectorCache([key]);
            this.#notifyListeners([key]);
        }
    }

    /**
     * Subscribe to all state changes
     * @param {Function} listener - Callback function
     * @returns {Function} Unsubscribe function
     */
    subscribe(listener) {
        this.#listeners.set(listener, listener);
        return () => this.#listeners.delete(listener);
    }

    /**
     * Subscribe to specific state slice changes
     * @param {string} key - State key to watch
     * @param {Function} listener - Callback function
     * @returns {Function} Unsubscribe function
     */
    subscribeToSlice(key, listener) {
        if (!this.#sliceListeners.has(key)) {
            this.#sliceListeners.set(key, new Set());
        }
        this.#sliceListeners.get(key).add(listener);

        // Return unsubscribe function
        return () => {
            const listeners = this.#sliceListeners.get(key);
            if (listeners) {
                listeners.delete(listener);
                if (listeners.size === 0) {
                    this.#sliceListeners.delete(key);
                }
            }
        };
    }

    /**
     * Register a memoized selector
     * @param {string} name - Selector name
     * @param {Function} selector - Selector function
     */
    registerSelector(name, selector) {
        this.#selectors.set(name, selector);
    }

    /**
     * Get value from a registered selector (memoized)
     * @param {string} name - Selector name
     * @returns {any}
     */
    select(name) {
        if (!this.#selectors.has(name)) {
            throw new Error(`Selector "${name}" not found`);
        }

        if (this.#selectorCache.has(name)) {
            return this.#selectorCache.get(name);
        }

        const selector = this.#selectors.get(name);
        const result = selector(this.#state);
        this.#selectorCache.set(name, result);
        return result;
    }

    /**
     * Hydrate state from storage
     * @param {Object} storageManager - Storage manager instance
     */
    async hydrate(storageManager) {
        const userState = {
            pinnedTools: storageManager.get('v2:pinnedTools') || [],
            votes: storageManager.get('v2:votes') || {},
            usage: storageManager.get('v2:usage') || {},
            recentlyOpened: storageManager.get('v2:recentlyOpened') || [],
            collections: storageManager.get('v2:collections') || {},
            searchHistory: storageManager.get('v2:searchHistory') || [],
            theme: storageManager.get('v2:theme') || 'dark'
        };

        const uiState = {
            tourCompleted: storageManager.get('v2:tourCompleted') || false,
            analyticsEnabled: storageManager.get('v2:analyticsEnabled') !== false
        };

        this.setState(() => ({
            user: { ...this.#state.user, ...userState },
            ui: { ...this.#state.ui, ...uiState }
        }));
    }

    /**
     * Persist user state to storage
     * @param {Object} storageManager - Storage manager instance
     */
    persist(storageManager) {
        const { user, ui } = this.#state;

        storageManager.set('v2:pinnedTools', user.pinnedTools);
        storageManager.set('v2:votes', user.votes);
        storageManager.set('v2:usage', user.usage);
        storageManager.set('v2:recentlyOpened', user.recentlyOpened);
        storageManager.set('v2:collections', user.collections);
        storageManager.set('v2:searchHistory', user.searchHistory);
        storageManager.set('v2:theme', user.theme);
        storageManager.set('v2:tourCompleted', ui.tourCompleted);
        storageManager.set('v2:analyticsEnabled', ui.analyticsEnabled);
    }

    /**
     * Reset state to defaults
     */
    reset() {
        const previousUser = this.#state.user;
        this.#state = this.#deepClone(DEFAULT_STATE);
        // Preserve user data on reset
        this.#state.user = previousUser;
        this.#selectorCache.clear();
        this.#notifyListeners(Object.keys(this.#state));
    }

    /**
     * Reset filters to defaults
     */
    resetFilters() {
        this.setSlice('filters', this.#deepClone(DEFAULT_STATE.filters));
    }

    // Private methods

    #notifyListeners(changedKeys) {
        // Notify global listeners
        for (const listener of this.#listeners.values()) {
            try {
                listener(this.#state, changedKeys);
            } catch (error) {
                console.error('State listener error:', error);
            }
        }

        // Notify slice listeners
        for (const key of changedKeys) {
            const listeners = this.#sliceListeners.get(key);
            if (listeners) {
                const value = this.#state[key];
                for (const listener of listeners) {
                    try {
                        listener(value, key);
                    } catch (error) {
                        console.error(`Slice listener error for "${key}":`, error);
                    }
                }
            }
        }
    }

    #invalidateSelectorCache(changedKeys) {
        // Simple invalidation - clear all cached selectors
        // A more sophisticated approach would track dependencies
        this.#selectorCache.clear();
    }

    #deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }

        if (obj instanceof Set) {
            return new Set(obj);
        }

        if (obj instanceof Map) {
            return new Map(obj);
        }

        if (obj instanceof Date) {
            return new Date(obj);
        }

        if (Array.isArray(obj)) {
            return obj.map(item => this.#deepClone(item));
        }

        const cloned = {};
        for (const [key, value] of Object.entries(obj)) {
            cloned[key] = this.#deepClone(value);
        }
        return cloned;
    }

    #isEqual(a, b) {
        if (a === b) return true;
        if (a == null || b == null) return false;
        if (typeof a !== typeof b) return false;

        if (a instanceof Set && b instanceof Set) {
            if (a.size !== b.size) return false;
            for (const item of a) {
                if (!b.has(item)) return false;
            }
            return true;
        }

        if (Array.isArray(a) && Array.isArray(b)) {
            if (a.length !== b.length) return false;
            for (let i = 0; i < a.length; i++) {
                if (!this.#isEqual(a[i], b[i])) return false;
            }
            return true;
        }

        if (typeof a === 'object') {
            const keysA = Object.keys(a);
            const keysB = Object.keys(b);
            if (keysA.length !== keysB.length) return false;
            for (const key of keysA) {
                if (!this.#isEqual(a[key], b[key])) return false;
            }
            return true;
        }

        return false;
    }
}

export { StateManager, DEFAULT_STATE };
