/**
 * Sort Engine - Multi-field sorting
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { SORT_OPTIONS } from '../core/constants.js';

/**
 * @typedef {Object} SortConfig
 * @property {string} field - Field to sort by
 * @property {string} direction - 'asc' or 'desc'
 */

class SortEngine {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SortEngine}
     */
    static getInstance() {
        if (!SortEngine.#instance) {
            SortEngine.#instance = new SortEngine();
        }
        return SortEngine.#instance;
    }

    constructor() {
        if (SortEngine.#instance) {
            throw new Error('Use SortEngine.getInstance() instead of new SortEngine()');
        }

        this.state = StateManager.getInstance();

        // Complexity order for sorting
        this.complexityOrder = {
            'simple': 1,
            'intermediate': 2,
            'advanced': 3
        };
    }

    /**
     * Sort tools by the given configuration
     * @param {Array} tools - Tools to sort
     * @param {SortConfig} config - Sort configuration
     * @param {Object} [userData] - User data for usage/votes sorting
     * @returns {Array} Sorted tools
     */
    sort(tools, config, userData = null) {
        const { field, direction } = config;
        const modifier = direction === 'desc' ? -1 : 1;

        // Create a copy to avoid mutating original
        const sorted = [...tools];

        switch (field) {
            case 'name':
                return this.sortByName(sorted, modifier);

            case 'date':
                return this.sortByDate(sorted, modifier);

            case 'usage':
                return this.sortByUsage(sorted, modifier, userData?.usage || {});

            case 'votes':
                return this.sortByVotes(sorted, modifier, userData?.votes || {});

            case 'complexity':
                return this.sortByComplexity(sorted, modifier);

            case 'random':
                return this.shuffle(sorted);

            case 'category':
                return this.sortByCategory(sorted, modifier);

            default:
                return sorted;
        }
    }

    /**
     * Sort by name alphabetically
     * @param {Array} tools
     * @param {number} modifier
     * @returns {Array}
     */
    sortByName(tools, modifier = 1) {
        return tools.sort((a, b) => {
            return modifier * a.title.localeCompare(b.title, undefined, {
                sensitivity: 'base',
                numeric: true
            });
        });
    }

    /**
     * Sort by date added
     * @param {Array} tools
     * @param {number} modifier
     * @returns {Array}
     */
    sortByDate(tools, modifier = -1) {
        return tools.sort((a, b) => {
            const dateA = a.dateAdded ? new Date(a.dateAdded).getTime() : 0;
            const dateB = b.dateAdded ? new Date(b.dateAdded).getTime() : 0;
            return modifier * (dateA - dateB);
        });
    }

    /**
     * Sort by usage count
     * @param {Array} tools
     * @param {number} modifier
     * @param {Object} usage - Usage data {toolId: count}
     * @returns {Array}
     */
    sortByUsage(tools, modifier = -1, usage = {}) {
        return tools.sort((a, b) => {
            const usageA = usage[a.id] || 0;
            const usageB = usage[b.id] || 0;
            return modifier * (usageA - usageB);
        });
    }

    /**
     * Sort by vote count
     * @param {Array} tools
     * @param {number} modifier
     * @param {Object} votes - Votes data {toolId: count}
     * @returns {Array}
     */
    sortByVotes(tools, modifier = -1, votes = {}) {
        return tools.sort((a, b) => {
            const votesA = votes[a.id] || 0;
            const votesB = votes[b.id] || 0;
            return modifier * (votesA - votesB);
        });
    }

    /**
     * Sort by complexity level
     * @param {Array} tools
     * @param {number} modifier
     * @returns {Array}
     */
    sortByComplexity(tools, modifier = 1) {
        return tools.sort((a, b) => {
            const orderA = this.complexityOrder[a.complexity] || 2;
            const orderB = this.complexityOrder[b.complexity] || 2;
            return modifier * (orderA - orderB);
        });
    }

    /**
     * Sort by category
     * @param {Array} tools
     * @param {number} modifier
     * @returns {Array}
     */
    sortByCategory(tools, modifier = 1) {
        return tools.sort((a, b) => {
            const result = a.category.localeCompare(b.category);
            if (result !== 0) return modifier * result;
            // Secondary sort by name within category
            return a.title.localeCompare(b.title);
        });
    }

    /**
     * Shuffle array randomly (Fisher-Yates)
     * @param {Array} tools
     * @returns {Array}
     */
    shuffle(tools) {
        const shuffled = [...tools];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    /**
     * Sort with pinned items at top
     * @param {Array} tools
     * @param {string[]} pinnedIds
     * @param {SortConfig} config
     * @param {Object} userData
     * @returns {Array}
     */
    sortWithPinned(tools, pinnedIds = [], config, userData = null) {
        const pinnedSet = new Set(pinnedIds);
        const pinned = [];
        const unpinned = [];

        for (const tool of tools) {
            if (pinnedSet.has(tool.id)) {
                pinned.push(tool);
            } else {
                unpinned.push(tool);
            }
        }

        // Sort each group
        const sortedPinned = this.sort(pinned, config, userData);
        const sortedUnpinned = this.sort(unpinned, config, userData);

        // Combine with pinned first
        return [...sortedPinned, ...sortedUnpinned];
    }

    /**
     * Sort with featured items prioritized
     * @param {Array} tools
     * @param {SortConfig} config
     * @param {Object} userData
     * @returns {Array}
     */
    sortWithFeatured(tools, config, userData = null) {
        const featured = tools.filter(t => t.featured);
        const regular = tools.filter(t => !t.featured);

        const sortedFeatured = this.sort(featured, config, userData);
        const sortedRegular = this.sort(regular, config, userData);

        return [...sortedFeatured, ...sortedRegular];
    }

    /**
     * Multi-field sort
     * @param {Array} tools
     * @param {SortConfig[]} configs - Array of sort configurations (priority order)
     * @param {Object} userData
     * @returns {Array}
     */
    multiSort(tools, configs, userData = null) {
        return [...tools].sort((a, b) => {
            for (const config of configs) {
                const result = this.#compareByField(a, b, config, userData);
                if (result !== 0) return result;
            }
            return 0;
        });
    }

    /**
     * Compare two tools by a single field
     * @param {Object} a
     * @param {Object} b
     * @param {SortConfig} config
     * @param {Object} userData
     * @returns {number}
     */
    #compareByField(a, b, config, userData) {
        const { field, direction } = config;
        const modifier = direction === 'desc' ? -1 : 1;

        switch (field) {
            case 'name':
                return modifier * a.title.localeCompare(b.title);

            case 'date':
                const dateA = a.dateAdded ? new Date(a.dateAdded).getTime() : 0;
                const dateB = b.dateAdded ? new Date(b.dateAdded).getTime() : 0;
                return modifier * (dateA - dateB);

            case 'usage':
                const usageA = userData?.usage?.[a.id] || 0;
                const usageB = userData?.usage?.[b.id] || 0;
                return modifier * (usageA - usageB);

            case 'votes':
                const votesA = userData?.votes?.[a.id] || 0;
                const votesB = userData?.votes?.[b.id] || 0;
                return modifier * (votesA - votesB);

            case 'complexity':
                const orderA = this.complexityOrder[a.complexity] || 2;
                const orderB = this.complexityOrder[b.complexity] || 2;
                return modifier * (orderA - orderB);

            case 'category':
                return modifier * a.category.localeCompare(b.category);

            default:
                return 0;
        }
    }

    /**
     * Get available sort options
     * @returns {Array<{key: string, label: string, direction: string}>}
     */
    getOptions() {
        return Object.values(SORT_OPTIONS);
    }

    /**
     * Get default sort configuration
     * @returns {SortConfig}
     */
    getDefault() {
        return {
            field: 'name',
            direction: 'asc'
        };
    }
}

export { SortEngine };
