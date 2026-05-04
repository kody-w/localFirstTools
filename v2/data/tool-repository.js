/**
 * Tool Repository - Data access layer for tools
 * Local First Tools v2
 */

import { CATEGORIES, COMPLEXITY } from '../core/constants.js';

/**
 * @typedef {Object} Tool
 * @property {string} id
 * @property {string} title
 * @property {string} description
 * @property {string} filename
 * @property {string} path
 * @property {string} category
 * @property {string[]} tags
 * @property {string} complexity
 * @property {string} interactionType
 * @property {boolean} featured
 * @property {boolean} polished
 * @property {boolean} archived
 * @property {string|null} dateAdded
 * @property {string|null} thumbnail
 * @property {Object} metadata
 */

class ToolRepository {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {ToolRepository}
     */
    static getInstance() {
        if (!ToolRepository.#instance) {
            ToolRepository.#instance = new ToolRepository();
        }
        return ToolRepository.#instance;
    }

    constructor() {
        if (ToolRepository.#instance) {
            throw new Error('Use ToolRepository.getInstance() instead of new ToolRepository()');
        }

        /** @type {Tool[]} */
        this.#tools = [];
        /** @type {Map<string, Tool>} */
        this.#toolsById = new Map();
        /** @type {Map<string, Tool[]>} */
        this.#toolsByCategory = new Map();
        /** @type {Map<string, Set<string>>} */
        this.#tagIndex = new Map();
        /** @type {Object} */
        this.#categories = {};
        /** @type {boolean} */
        this.#initialized = false;
    }

    #tools;
    #toolsById;
    #toolsByCategory;
    #tagIndex;
    #categories;
    #initialized;

    /**
     * Initialize repository with config data
     * @param {Object} config - Normalized config from DataLoader
     */
    initialize(config) {
        this.#tools = config.tools || [];
        this.#categories = { ...CATEGORIES, ...config.categories };
        this.#buildIndexes();
        this.#initialized = true;
    }

    /**
     * Build lookup indexes for fast queries
     */
    #buildIndexes() {
        this.#toolsById.clear();
        this.#toolsByCategory.clear();
        this.#tagIndex.clear();

        for (const tool of this.#tools) {
            // Index by ID
            this.#toolsById.set(tool.id, tool);

            // Index by category
            if (!this.#toolsByCategory.has(tool.category)) {
                this.#toolsByCategory.set(tool.category, []);
            }
            this.#toolsByCategory.get(tool.category).push(tool);

            // Index by tags
            for (const tag of tool.tags) {
                const normalizedTag = tag.toLowerCase();
                if (!this.#tagIndex.has(normalizedTag)) {
                    this.#tagIndex.set(normalizedTag, new Set());
                }
                this.#tagIndex.get(normalizedTag).add(tool.id);
            }
        }
    }

    /**
     * Get all tools
     * @param {boolean} includeArchived - Whether to include archived tools
     * @returns {Tool[]}
     */
    getAll(includeArchived = false) {
        if (includeArchived) {
            return [...this.#tools];
        }
        return this.#tools.filter(t => !t.archived);
    }

    /**
     * Get tool by ID
     * @param {string} id
     * @returns {Tool|null}
     */
    getById(id) {
        return this.#toolsById.get(id) || null;
    }

    /**
     * Get tools by category
     * @param {string} category
     * @param {boolean} includeArchived
     * @returns {Tool[]}
     */
    getByCategory(category, includeArchived = false) {
        const tools = this.#toolsByCategory.get(category) || [];
        if (includeArchived) {
            return [...tools];
        }
        return tools.filter(t => !t.archived);
    }

    /**
     * Get tools by tag
     * @param {string} tag
     * @returns {Tool[]}
     */
    getByTag(tag) {
        const normalizedTag = tag.toLowerCase();
        const toolIds = this.#tagIndex.get(normalizedTag);
        if (!toolIds) return [];

        return Array.from(toolIds)
            .map(id => this.#toolsById.get(id))
            .filter(Boolean);
    }

    /**
     * Get featured tools
     * @returns {Tool[]}
     */
    getFeatured() {
        return this.#tools.filter(t => t.featured && !t.archived);
    }

    /**
     * Get polished tools
     * @returns {Tool[]}
     */
    getPolished() {
        return this.#tools.filter(t => t.polished && !t.archived);
    }

    /**
     * Get archived tools
     * @returns {Tool[]}
     */
    getArchived() {
        return this.#tools.filter(t => t.archived);
    }

    /**
     * Get tools by complexity
     * @param {string} complexity
     * @returns {Tool[]}
     */
    getByComplexity(complexity) {
        return this.#tools.filter(t => t.complexity === complexity && !t.archived);
    }

    /**
     * Get tools by interaction type
     * @param {string} type
     * @returns {Tool[]}
     */
    getByInteractionType(type) {
        return this.#tools.filter(t => t.interactionType === type && !t.archived);
    }

    /**
     * Search tools by query
     * @param {string} query
     * @returns {Tool[]}
     */
    search(query) {
        if (!query || query.trim() === '') {
            return this.getAll();
        }

        const normalizedQuery = query.toLowerCase().trim();
        const terms = normalizedQuery.split(/\s+/);

        return this.#tools.filter(tool => {
            if (tool.archived) return false;

            const searchableText = [
                tool.title,
                tool.description,
                tool.filename,
                ...tool.tags
            ].join(' ').toLowerCase();

            return terms.every(term => searchableText.includes(term));
        });
    }

    /**
     * Get all unique tags
     * @returns {string[]}
     */
    getAllTags() {
        return Array.from(this.#tagIndex.keys()).sort();
    }

    /**
     * Get all categories with counts
     * @returns {Object[]}
     */
    getCategoriesWithCounts() {
        const counts = {};

        for (const tool of this.#tools) {
            if (tool.archived) continue;
            counts[tool.category] = (counts[tool.category] || 0) + 1;
        }

        return Object.entries(this.#categories).map(([key, category]) => ({
            ...category,
            count: counts[key] || 0
        }));
    }

    /**
     * Get category metadata
     * @param {string} categoryKey
     * @returns {Object|null}
     */
    getCategory(categoryKey) {
        return this.#categories[categoryKey] || null;
    }

    /**
     * Get all categories
     * @returns {Object}
     */
    getAllCategories() {
        return { ...this.#categories };
    }

    /**
     * Get unique folders from tool paths
     * @returns {string[]}
     */
    getUniqueFolders() {
        const folders = new Set();

        for (const tool of this.#tools) {
            if (tool.path && tool.path.includes('/')) {
                const folder = tool.path.substring(0, tool.path.lastIndexOf('/'));
                if (folder) {
                    folders.add(folder);
                }
            }
        }

        return Array.from(folders).sort();
    }

    /**
     * Get tools by folder path
     * @param {string} folder
     * @returns {Tool[]}
     */
    getByFolder(folder) {
        return this.#tools.filter(tool => {
            if (tool.archived) return false;
            return tool.path && tool.path.startsWith(folder + '/');
        });
    }

    /**
     * Get statistics about the tool collection
     * @returns {Object}
     */
    getStats() {
        const active = this.#tools.filter(t => !t.archived);
        const complexityCounts = {};
        const typeCounts = {};

        for (const tool of active) {
            complexityCounts[tool.complexity] = (complexityCounts[tool.complexity] || 0) + 1;
            typeCounts[tool.interactionType] = (typeCounts[tool.interactionType] || 0) + 1;
        }

        return {
            total: this.#tools.length,
            active: active.length,
            archived: this.#tools.length - active.length,
            featured: this.getFeatured().length,
            polished: this.getPolished().length,
            categories: this.getCategoriesWithCounts(),
            complexity: complexityCounts,
            types: typeCounts,
            tags: this.getAllTags().length
        };
    }

    /**
     * Check if repository is initialized
     * @returns {boolean}
     */
    isInitialized() {
        return this.#initialized;
    }

    /**
     * Get tool count
     * @param {boolean} includeArchived
     * @returns {number}
     */
    count(includeArchived = false) {
        if (includeArchived) {
            return this.#tools.length;
        }
        return this.#tools.filter(t => !t.archived).length;
    }

    /**
     * Reset repository
     */
    reset() {
        this.#tools = [];
        this.#toolsById.clear();
        this.#toolsByCategory.clear();
        this.#tagIndex.clear();
        this.#categories = { ...CATEGORIES };
        this.#initialized = false;
    }
}

export { ToolRepository };
