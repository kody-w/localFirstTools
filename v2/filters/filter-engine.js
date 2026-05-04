/**
 * Filter Engine - Multi-dimensional filtering
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { STORAGE_KEYS } from '../core/constants.js';

/**
 * @typedef {Object} FilterCriteria
 * @property {string} category - Category filter
 * @property {string} complexity - Complexity filter (simple, intermediate, advanced)
 * @property {string} type - Interaction type filter
 * @property {string} featured - Featured filter ('featured', 'regular', '')
 * @property {string} polished - Polished filter
 * @property {string} folder - Folder path filter
 * @property {Set<string>} tags - Tag filters
 * @property {string} searchTerm - Search query
 */

class FilterEngine {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {FilterEngine}
     */
    static getInstance() {
        if (!FilterEngine.#instance) {
            FilterEngine.#instance = new FilterEngine();
        }
        return FilterEngine.#instance;
    }

    constructor() {
        if (FilterEngine.#instance) {
            throw new Error('Use FilterEngine.getInstance() instead of new FilterEngine()');
        }

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
    }

    /**
     * Apply all filters and return filtered tools
     * @param {FilterCriteria} criteria - Filter criteria
     * @param {Array} [tools] - Tools to filter (defaults to all tools)
     * @returns {Array} Filtered tools
     */
    apply(criteria, tools = null) {
        let result = tools || this.toolRepo.getAll();

        // Apply each filter in sequence
        result = this.filterByCategory(result, criteria.category);
        result = this.filterByComplexity(result, criteria.complexity);
        result = this.filterByType(result, criteria.type);
        result = this.filterByFeatured(result, criteria.featured);
        result = this.filterByPolished(result, criteria.polished);
        result = this.filterByFolder(result, criteria.folder);
        result = this.filterByTags(result, criteria.tags);
        result = this.filterBySearch(result, criteria.searchTerm);

        return result;
    }

    /**
     * Filter by category
     * @param {Array} tools
     * @param {string} category
     * @returns {Array}
     */
    filterByCategory(tools, category) {
        if (!category || category === 'all') {
            return tools;
        }
        return tools.filter(tool => tool.category === category);
    }

    /**
     * Filter by complexity level
     * @param {Array} tools
     * @param {string} complexity
     * @returns {Array}
     */
    filterByComplexity(tools, complexity) {
        if (!complexity) {
            return tools;
        }
        return tools.filter(tool => tool.complexity === complexity);
    }

    /**
     * Filter by interaction type
     * @param {Array} tools
     * @param {string} type
     * @returns {Array}
     */
    filterByType(tools, type) {
        if (!type) {
            return tools;
        }
        return tools.filter(tool => tool.interactionType === type);
    }

    /**
     * Filter by featured status
     * @param {Array} tools
     * @param {string} featured - 'featured', 'regular', or ''
     * @returns {Array}
     */
    filterByFeatured(tools, featured) {
        if (!featured) {
            return tools;
        }
        if (featured === 'featured') {
            return tools.filter(tool => tool.featured);
        }
        if (featured === 'regular') {
            return tools.filter(tool => !tool.featured);
        }
        return tools;
    }

    /**
     * Filter by polished status
     * @param {Array} tools
     * @param {string} polished
     * @returns {Array}
     */
    filterByPolished(tools, polished) {
        if (!polished) {
            return tools;
        }
        if (polished === 'polished') {
            return tools.filter(tool => tool.polished);
        }
        return tools;
    }

    /**
     * Filter by folder path
     * @param {Array} tools
     * @param {string} folder
     * @returns {Array}
     */
    filterByFolder(tools, folder) {
        if (!folder) {
            return tools;
        }
        return tools.filter(tool => {
            if (!tool.path) return false;
            return tool.path.startsWith(folder + '/') || tool.path === folder;
        });
    }

    /**
     * Filter by tags (AND logic - must have all tags)
     * @param {Array} tools
     * @param {Set<string>} tags
     * @returns {Array}
     */
    filterByTags(tools, tags) {
        if (!tags || tags.size === 0) {
            return tools;
        }

        const tagArray = Array.from(tags).map(t => t.toLowerCase());

        return tools.filter(tool => {
            const toolTags = tool.tags.map(t => t.toLowerCase());
            return tagArray.every(tag => toolTags.includes(tag));
        });
    }

    /**
     * Filter by search term
     * @param {Array} tools
     * @param {string} searchTerm
     * @returns {Array}
     */
    filterBySearch(tools, searchTerm) {
        if (!searchTerm || searchTerm.trim() === '') {
            return tools;
        }

        const query = searchTerm.toLowerCase().trim();
        const terms = query.split(/\s+/);

        return tools.filter(tool => {
            const searchableText = [
                tool.title,
                tool.description,
                tool.filename,
                ...tool.tags
            ].join(' ').toLowerCase();

            // All terms must match (AND logic)
            return terms.every(term => searchableText.includes(term));
        });
    }

    /**
     * Filter by pinned status
     * @param {Array} tools
     * @param {string[]} pinnedIds
     * @returns {Array}
     */
    filterByPinned(tools, pinnedIds) {
        const pinnedSet = new Set(pinnedIds);
        return tools.filter(tool => pinnedSet.has(tool.id));
    }

    /**
     * Filter by date range
     * @param {Array} tools
     * @param {Date} after
     * @param {Date} before
     * @returns {Array}
     */
    filterByDateRange(tools, after = null, before = null) {
        return tools.filter(tool => {
            if (!tool.dateAdded) return true;

            const date = new Date(tool.dateAdded);

            if (after && date < after) return false;
            if (before && date > before) return false;

            return true;
        });
    }

    /**
     * Get active filter count
     * @param {FilterCriteria} criteria
     * @returns {number}
     */
    getActiveFilterCount(criteria) {
        let count = 0;

        if (criteria.category && criteria.category !== 'all') count++;
        if (criteria.complexity) count++;
        if (criteria.type) count++;
        if (criteria.featured) count++;
        if (criteria.polished) count++;
        if (criteria.folder) count++;
        if (criteria.tags && criteria.tags.size > 0) count += criteria.tags.size;
        if (criteria.searchTerm) count++;

        return count;
    }

    /**
     * Get active filters as array of objects for display
     * @param {FilterCriteria} criteria
     * @returns {Array<{type: string, value: string, label: string}>}
     */
    getActiveFiltersDisplay(criteria) {
        const filters = [];

        if (criteria.category && criteria.category !== 'all') {
            filters.push({
                type: 'category',
                value: criteria.category,
                label: `Category: ${criteria.category}`
            });
        }

        if (criteria.complexity) {
            filters.push({
                type: 'complexity',
                value: criteria.complexity,
                label: `Complexity: ${criteria.complexity}`
            });
        }

        if (criteria.type) {
            filters.push({
                type: 'type',
                value: criteria.type,
                label: `Type: ${criteria.type}`
            });
        }

        if (criteria.featured) {
            filters.push({
                type: 'featured',
                value: criteria.featured,
                label: `Featured: ${criteria.featured}`
            });
        }

        if (criteria.polished) {
            filters.push({
                type: 'polished',
                value: criteria.polished,
                label: 'Polished'
            });
        }

        if (criteria.folder) {
            filters.push({
                type: 'folder',
                value: criteria.folder,
                label: `Folder: ${criteria.folder}`
            });
        }

        if (criteria.tags && criteria.tags.size > 0) {
            for (const tag of criteria.tags) {
                filters.push({
                    type: 'tag',
                    value: tag,
                    label: `Tag: ${tag}`
                });
            }
        }

        if (criteria.searchTerm) {
            filters.push({
                type: 'search',
                value: criteria.searchTerm,
                label: `Search: "${criteria.searchTerm}"`
            });
        }

        return filters;
    }

    /**
     * Check if any filters are active
     * @param {FilterCriteria} criteria
     * @returns {boolean}
     */
    hasActiveFilters(criteria) {
        return this.getActiveFilterCount(criteria) > 0;
    }

    /**
     * Create empty filter criteria
     * @returns {FilterCriteria}
     */
    createEmptyCriteria() {
        return {
            category: 'all',
            complexity: '',
            type: '',
            featured: '',
            polished: '',
            folder: '',
            tags: new Set(),
            searchTerm: ''
        };
    }
}

export { FilterEngine };
