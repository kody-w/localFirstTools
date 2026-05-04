/**
 * Analytics Tracker - Usage tracking
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../../core/event-bus.js';
import { StorageManager } from '../../storage/storage-manager.js';

class AnalyticsTracker {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {AnalyticsTracker}
     */
    static getInstance() {
        if (!AnalyticsTracker.#instance) {
            AnalyticsTracker.#instance = new AnalyticsTracker();
        }
        return AnalyticsTracker.#instance;
    }

    constructor() {
        if (AnalyticsTracker.#instance) {
            return AnalyticsTracker.#instance;
        }

        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();

        this.#sessionId = this.#generateSessionId();
        this.#sessionStart = Date.now();
        this.#isTracking = true;

        this.#loadData();
        this.#bindEvents();
    }

    #sessionId;
    #sessionStart;
    #isTracking;
    #data;

    /**
     * Generate unique session ID
     * @returns {string}
     */
    #generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Load analytics data from storage
     */
    #loadData() {
        const stored = this.storage.get('analytics') || {};

        this.#data = {
            toolUsage: stored.toolUsage || {},
            categoryViews: stored.categoryViews || {},
            searchHistory: stored.searchHistory || [],
            sessions: stored.sessions || [],
            dailyUsage: stored.dailyUsage || {},
            totalOpens: stored.totalOpens || 0,
            totalPins: stored.totalPins || 0,
            favoriteCategories: stored.favoriteCategories || [],
            lastVisit: stored.lastVisit || null
        };
    }

    /**
     * Save analytics data to storage
     */
    #saveData() {
        this.storage.set('analytics', this.#data);
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Track tool opens
        this.events.on(EVENTS.TOOL_OPEN, ({ toolId, tool }) => {
            this.trackToolOpen(toolId, tool);
        });

        // Track pins
        this.events.on(EVENTS.TOOL_PIN, ({ toolId }) => {
            this.trackPin(toolId);
        });

        // Track searches
        this.events.on(EVENTS.SEARCH, ({ query }) => {
            this.trackSearch(query);
        });

        // Track view changes
        this.events.on(EVENTS.VIEW_CHANGE, ({ mode }) => {
            this.trackViewChange(mode);
        });

        // Track category views
        this.events.on(EVENTS.FILTER_CHANGE, ({ category }) => {
            if (category) {
                this.trackCategoryView(category);
            }
        });

        // End session on page unload
        window.addEventListener('beforeunload', () => {
            this.endSession();
        });

        // Track visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.#saveData();
            }
        });
    }

    /**
     * Track tool open
     * @param {string} toolId
     * @param {Object} tool
     */
    trackToolOpen(toolId, tool = {}) {
        if (!this.#isTracking) return;

        const now = Date.now();
        const today = new Date().toISOString().split('T')[0];

        // Update tool usage
        if (!this.#data.toolUsage[toolId]) {
            this.#data.toolUsage[toolId] = {
                opens: 0,
                lastOpened: null,
                firstOpened: now,
                category: tool.category || 'unknown',
                title: tool.title || toolId
            };
        }

        this.#data.toolUsage[toolId].opens++;
        this.#data.toolUsage[toolId].lastOpened = now;

        // Update daily usage
        if (!this.#data.dailyUsage[today]) {
            this.#data.dailyUsage[today] = { opens: 0, uniqueTools: [] };
        }

        this.#data.dailyUsage[today].opens++;

        if (!this.#data.dailyUsage[today].uniqueTools.includes(toolId)) {
            this.#data.dailyUsage[today].uniqueTools.push(toolId);
        }

        // Update totals
        this.#data.totalOpens++;

        this.#saveData();

        this.events.emit(EVENTS.ANALYTICS_UPDATE, {
            type: 'tool_open',
            toolId,
            data: this.#data.toolUsage[toolId]
        });
    }

    /**
     * Track pin action
     * @param {string} toolId
     */
    trackPin(toolId) {
        if (!this.#isTracking) return;

        this.#data.totalPins++;
        this.#saveData();
    }

    /**
     * Track search
     * @param {string} query
     */
    trackSearch(query) {
        if (!this.#isTracking || !query) return;

        const search = {
            query: query.toLowerCase().trim(),
            timestamp: Date.now()
        };

        // Add to history (limit to 100)
        this.#data.searchHistory.unshift(search);
        if (this.#data.searchHistory.length > 100) {
            this.#data.searchHistory.pop();
        }

        this.#saveData();
    }

    /**
     * Track category view
     * @param {string} category
     */
    trackCategoryView(category) {
        if (!this.#isTracking) return;

        if (!this.#data.categoryViews[category]) {
            this.#data.categoryViews[category] = 0;
        }

        this.#data.categoryViews[category]++;
        this.#updateFavoriteCategories();
        this.#saveData();
    }

    /**
     * Track view change
     * @param {string} mode
     */
    trackViewChange(mode) {
        if (!this.#isTracking) return;

        // Could track view preference patterns here
    }

    /**
     * Update favorite categories based on views
     */
    #updateFavoriteCategories() {
        const sorted = Object.entries(this.#data.categoryViews)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([category]) => category);

        this.#data.favoriteCategories = sorted;
    }

    /**
     * End current session
     */
    endSession() {
        const session = {
            id: this.#sessionId,
            start: this.#sessionStart,
            end: Date.now(),
            duration: Date.now() - this.#sessionStart
        };

        this.#data.sessions.push(session);

        // Keep only last 50 sessions
        if (this.#data.sessions.length > 50) {
            this.#data.sessions = this.#data.sessions.slice(-50);
        }

        this.#data.lastVisit = Date.now();
        this.#saveData();
    }

    /**
     * Get most used tools
     * @param {number} limit
     * @returns {Array}
     */
    getMostUsedTools(limit = 10) {
        return Object.entries(this.#data.toolUsage)
            .sort((a, b) => b[1].opens - a[1].opens)
            .slice(0, limit)
            .map(([id, data]) => ({
                id,
                ...data
            }));
    }

    /**
     * Get recently used tools
     * @param {number} limit
     * @returns {Array}
     */
    getRecentlyUsedTools(limit = 10) {
        return Object.entries(this.#data.toolUsage)
            .filter(([, data]) => data.lastOpened)
            .sort((a, b) => b[1].lastOpened - a[1].lastOpened)
            .slice(0, limit)
            .map(([id, data]) => ({
                id,
                ...data
            }));
    }

    /**
     * Get popular searches
     * @param {number} limit
     * @returns {Array}
     */
    getPopularSearches(limit = 10) {
        const searchCounts = {};

        for (const { query } of this.#data.searchHistory) {
            searchCounts[query] = (searchCounts[query] || 0) + 1;
        }

        return Object.entries(searchCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([query, count]) => ({ query, count }));
    }

    /**
     * Get favorite categories
     * @returns {Array}
     */
    getFavoriteCategories() {
        return [...this.#data.favoriteCategories];
    }

    /**
     * Get usage stats for a date range
     * @param {Date} startDate
     * @param {Date} endDate
     * @returns {Object}
     */
    getUsageStats(startDate, endDate) {
        const stats = {
            totalOpens: 0,
            uniqueTools: new Set(),
            byDay: {}
        };

        const start = startDate.toISOString().split('T')[0];
        const end = endDate.toISOString().split('T')[0];

        for (const [day, data] of Object.entries(this.#data.dailyUsage)) {
            if (day >= start && day <= end) {
                stats.totalOpens += data.opens;
                stats.byDay[day] = data;

                for (const toolId of data.uniqueTools) {
                    stats.uniqueTools.add(toolId);
                }
            }
        }

        stats.uniqueToolsCount = stats.uniqueTools.size;
        stats.uniqueTools = [...stats.uniqueTools];

        return stats;
    }

    /**
     * Get session stats
     * @returns {Object}
     */
    getSessionStats() {
        const sessions = this.#data.sessions;

        if (sessions.length === 0) {
            return { avgDuration: 0, totalSessions: 0 };
        }

        const totalDuration = sessions.reduce((sum, s) => sum + s.duration, 0);

        return {
            totalSessions: sessions.length,
            avgDuration: totalDuration / sessions.length,
            totalTime: totalDuration,
            lastSession: sessions[sessions.length - 1]
        };
    }

    /**
     * Get all analytics data
     * @returns {Object}
     */
    getAllData() {
        return {
            ...this.#data,
            currentSession: {
                id: this.#sessionId,
                start: this.#sessionStart,
                duration: Date.now() - this.#sessionStart
            }
        };
    }

    /**
     * Export analytics data
     * @returns {string}
     */
    exportData() {
        return JSON.stringify(this.getAllData(), null, 2);
    }

    /**
     * Clear all analytics data
     */
    clearData() {
        this.#data = {
            toolUsage: {},
            categoryViews: {},
            searchHistory: [],
            sessions: [],
            dailyUsage: {},
            totalOpens: 0,
            totalPins: 0,
            favoriteCategories: [],
            lastVisit: null
        };

        this.#saveData();

        this.events.emit(EVENTS.ANALYTICS_CLEARED);
    }

    /**
     * Enable/disable tracking
     * @param {boolean} enabled
     */
    setTrackingEnabled(enabled) {
        this.#isTracking = enabled;
        this.storage.set('analyticsEnabled', enabled);
    }

    /**
     * Check if tracking is enabled
     * @returns {boolean}
     */
    isTrackingEnabled() {
        return this.#isTracking;
    }
}

export { AnalyticsTracker };
