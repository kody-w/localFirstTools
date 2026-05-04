/**
 * History Manager - Search history tracking
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StorageManager } from '../storage/storage-manager.js';

class HistoryManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {HistoryManager}
     */
    static getInstance() {
        if (!HistoryManager.#instance) {
            HistoryManager.#instance = new HistoryManager();
        }
        return HistoryManager.#instance;
    }

    constructor() {
        if (HistoryManager.#instance) {
            return HistoryManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();
        this.#history = [];
        this.#maxHistory = 100;
        this.#sessionHistory = [];

        this.#initialize();
    }

    #history;
    #maxHistory;
    #sessionHistory;

    /**
     * Initialize history manager
     */
    #initialize() {
        this.#loadHistory();
        this.#bindEvents();
    }

    /**
     * Load history from storage
     */
    #loadHistory() {
        this.#history = this.storage.get('searchHistory', []);
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Track successful searches
        this.events.on(EVENTS.SEARCH_RESULTS, ({ query, count }) => {
            if (query && query.trim().length > 1 && count > 0) {
                this.add(query.trim());
            }
        });
    }

    /**
     * Add search query to history
     * @param {string} query
     */
    add(query) {
        if (!query || query.trim().length < 2) return;

        const normalizedQuery = query.trim().toLowerCase();

        // Create entry
        const entry = {
            query: query.trim(),
            normalizedQuery,
            timestamp: Date.now(),
            sessionId: this.#getSessionId()
        };

        // Remove duplicates
        this.#history = this.#history.filter(h => h.normalizedQuery !== normalizedQuery);

        // Add to beginning
        this.#history.unshift(entry);

        // Trim to max
        if (this.#history.length > this.#maxHistory) {
            this.#history = this.#history.slice(0, this.#maxHistory);
        }

        // Also track in session
        this.#sessionHistory.unshift(entry);

        // Save
        this.#save();

        this.events.emit(EVENTS.SEARCH_HISTORY_UPDATED, {
            entry,
            history: this.#history
        });
    }

    /**
     * Get session ID
     * @returns {string}
     */
    #getSessionId() {
        if (!this._sessionId) {
            this._sessionId = `session_${Date.now()}`;
        }
        return this._sessionId;
    }

    /**
     * Save history to storage
     */
    #save() {
        this.storage.set('searchHistory', this.#history);
    }

    /**
     * Get recent searches
     * @param {number} limit
     * @returns {Array}
     */
    getRecent(limit = 10) {
        return this.#history.slice(0, limit);
    }

    /**
     * Get all history
     * @returns {Array}
     */
    getAll() {
        return [...this.#history];
    }

    /**
     * Get session history
     * @returns {Array}
     */
    getSessionHistory() {
        return [...this.#sessionHistory];
    }

    /**
     * Search history
     * @param {string} query
     * @returns {Array}
     */
    search(query) {
        if (!query) return this.getRecent();

        const queryLower = query.toLowerCase();
        return this.#history.filter(h =>
            h.normalizedQuery.includes(queryLower)
        );
    }

    /**
     * Get popular searches
     * @param {number} limit
     * @returns {Array}
     */
    getPopular(limit = 10) {
        // Count query occurrences
        const counts = new Map();

        for (const entry of this.#history) {
            const count = counts.get(entry.normalizedQuery) || 0;
            counts.set(entry.normalizedQuery, count + 1);
        }

        // Sort by count
        return Array.from(counts.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([query, count]) => ({
                query: this.#history.find(h => h.normalizedQuery === query)?.query || query,
                count
            }));
    }

    /**
     * Get history by date
     * @param {Date} date
     * @returns {Array}
     */
    getByDate(date) {
        const startOfDay = new Date(date);
        startOfDay.setHours(0, 0, 0, 0);

        const endOfDay = new Date(date);
        endOfDay.setHours(23, 59, 59, 999);

        return this.#history.filter(h =>
            h.timestamp >= startOfDay.getTime() &&
            h.timestamp <= endOfDay.getTime()
        );
    }

    /**
     * Get history grouped by date
     * @returns {Object}
     */
    getGroupedByDate() {
        const groups = {};

        for (const entry of this.#history) {
            const date = new Date(entry.timestamp).toDateString();
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(entry);
        }

        return groups;
    }

    /**
     * Remove entry from history
     * @param {string} query
     */
    remove(query) {
        const normalizedQuery = query.trim().toLowerCase();
        this.#history = this.#history.filter(h => h.normalizedQuery !== normalizedQuery);
        this.#save();

        this.events.emit(EVENTS.SEARCH_HISTORY_UPDATED, {
            removed: query,
            history: this.#history
        });
    }

    /**
     * Clear all history
     */
    clear() {
        this.#history = [];
        this.#sessionHistory = [];
        this.#save();

        this.events.emit(EVENTS.SEARCH_HISTORY_UPDATED, {
            cleared: true,
            history: []
        });
    }

    /**
     * Clear old history
     * @param {number} daysToKeep
     */
    clearOld(daysToKeep = 30) {
        const cutoff = Date.now() - (daysToKeep * 24 * 60 * 60 * 1000);
        const oldCount = this.#history.length;

        this.#history = this.#history.filter(h => h.timestamp > cutoff);
        this.#save();

        const removedCount = oldCount - this.#history.length;
        if (removedCount > 0) {
            this.events.emit(EVENTS.SEARCH_HISTORY_UPDATED, {
                clearedOld: removedCount,
                history: this.#history
            });
        }
    }

    /**
     * Export history
     * @returns {Object}
     */
    export() {
        return {
            version: 1,
            exportedAt: Date.now(),
            history: this.#history
        };
    }

    /**
     * Import history
     * @param {Object} data
     */
    import(data) {
        if (!data || !Array.isArray(data.history)) {
            throw new Error('Invalid history data');
        }

        // Merge with existing
        const existingQueries = new Set(this.#history.map(h => h.normalizedQuery));

        for (const entry of data.history) {
            if (!existingQueries.has(entry.normalizedQuery)) {
                this.#history.push(entry);
            }
        }

        // Sort by timestamp
        this.#history.sort((a, b) => b.timestamp - a.timestamp);

        // Trim
        if (this.#history.length > this.#maxHistory) {
            this.#history = this.#history.slice(0, this.#maxHistory);
        }

        this.#save();

        this.events.emit(EVENTS.SEARCH_HISTORY_UPDATED, {
            imported: data.history.length,
            history: this.#history
        });
    }

    /**
     * Get statistics
     * @returns {Object}
     */
    getStatistics() {
        const today = new Date().toDateString();
        const todaySearches = this.#history.filter(h =>
            new Date(h.timestamp).toDateString() === today
        );

        const uniqueQueries = new Set(this.#history.map(h => h.normalizedQuery));

        return {
            totalSearches: this.#history.length,
            uniqueQueries: uniqueQueries.size,
            todaySearches: todaySearches.length,
            sessionSearches: this.#sessionHistory.length,
            oldestSearch: this.#history.length > 0
                ? new Date(this.#history[this.#history.length - 1].timestamp)
                : null,
            newestSearch: this.#history.length > 0
                ? new Date(this.#history[0].timestamp)
                : null
        };
    }

    /**
     * Get autocomplete suggestions
     * @param {string} partial
     * @param {number} limit
     * @returns {Array}
     */
    getAutocompleteSuggestions(partial, limit = 5) {
        if (!partial || partial.length < 1) {
            return this.getRecent(limit).map(h => h.query);
        }

        const partialLower = partial.toLowerCase();

        // Prioritize starts-with matches
        const startsWithMatches = [];
        const containsMatches = [];

        for (const entry of this.#history) {
            if (entry.normalizedQuery.startsWith(partialLower)) {
                startsWithMatches.push(entry.query);
            } else if (entry.normalizedQuery.includes(partialLower)) {
                containsMatches.push(entry.query);
            }

            if (startsWithMatches.length >= limit) break;
        }

        return [...startsWithMatches, ...containsMatches].slice(0, limit);
    }
}

export { HistoryManager };
