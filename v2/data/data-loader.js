/**
 * Data Loader - Config loading with fallbacks
 * Local First Tools v2
 */

import { CONFIG_PATH, MANIFEST_PATH } from '../core/constants.js';

/**
 * @typedef {Object} LoadResult
 * @property {boolean} success
 * @property {Object|null} data
 * @property {string|null} error
 * @property {string} source
 */

class DataLoader {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {DataLoader}
     */
    static getInstance() {
        if (!DataLoader.#instance) {
            DataLoader.#instance = new DataLoader();
        }
        return DataLoader.#instance;
    }

    constructor() {
        if (DataLoader.#instance) {
            throw new Error('Use DataLoader.getInstance() instead of new DataLoader()');
        }

        this.#cache = new Map();
        this.#loadPromises = new Map();
    }

    #cache;
    #loadPromises;

    /**
     * Load the gallery configuration
     * Tries primary config first, falls back to manifest
     * @returns {Promise<LoadResult>}
     */
    async loadConfig() {
        // Try primary config first
        const primaryResult = await this.#loadJSON(CONFIG_PATH);

        if (primaryResult.success) {
            return {
                success: true,
                data: this.#normalizeConfig(primaryResult.data),
                error: null,
                source: 'vibe_gallery_config.json'
            };
        }

        // Try fallback manifest
        const fallbackResult = await this.#loadJSON(MANIFEST_PATH);

        if (fallbackResult.success) {
            return {
                success: true,
                data: this.#normalizeManifest(fallbackResult.data),
                error: null,
                source: 'tools-manifest.json'
            };
        }

        return {
            success: false,
            data: null,
            error: `Failed to load config: ${primaryResult.error}`,
            source: 'none'
        };
    }

    /**
     * Load JSON file with caching
     * @param {string} path
     * @returns {Promise<{success: boolean, data: any, error: string|null}>}
     */
    async #loadJSON(path) {
        // Check cache first
        if (this.#cache.has(path)) {
            return { success: true, data: this.#cache.get(path), error: null };
        }

        // Deduplicate concurrent requests
        if (this.#loadPromises.has(path)) {
            return this.#loadPromises.get(path);
        }

        const loadPromise = this.#fetchJSON(path);
        this.#loadPromises.set(path, loadPromise);

        try {
            const result = await loadPromise;
            if (result.success) {
                this.#cache.set(path, result.data);
            }
            return result;
        } finally {
            this.#loadPromises.delete(path);
        }
    }

    /**
     * Fetch and parse JSON
     * @param {string} path
     * @returns {Promise<{success: boolean, data: any, error: string|null}>}
     */
    async #fetchJSON(path) {
        try {
            const response = await fetch(path);

            if (!response.ok) {
                return {
                    success: false,
                    data: null,
                    error: `HTTP ${response.status}: ${response.statusText}`
                };
            }

            const data = await response.json();
            return { success: true, data, error: null };
        } catch (error) {
            return {
                success: false,
                data: null,
                error: error.message
            };
        }
    }

    /**
     * Normalize vibe_gallery_config.json format
     * @param {Object} config
     * @returns {Object}
     */
    #normalizeConfig(config) {
        const tools = [];
        const categories = {};

        // Handle the category-based structure
        if (config.categories) {
            for (const [categoryKey, category] of Object.entries(config.categories)) {
                categories[categoryKey] = {
                    key: categoryKey,
                    title: category.title || categoryKey,
                    icon: category.icon || '',
                    color: category.color || '#888888'
                };

                if (Array.isArray(category.tools)) {
                    for (const tool of category.tools) {
                        tools.push(this.#normalizeTool(tool, categoryKey));
                    }
                }
            }
        }

        // Handle flat tools array if present
        if (Array.isArray(config.tools)) {
            for (const tool of config.tools) {
                tools.push(this.#normalizeTool(tool, tool.category || 'uncategorized'));
            }
        }

        return {
            version: config.version || '1.0.0',
            lastUpdated: config.lastUpdated || new Date().toISOString(),
            categories,
            tools,
            metadata: config.metadata || {}
        };
    }

    /**
     * Normalize tools-manifest.json format
     * @param {Object} manifest
     * @returns {Object}
     */
    #normalizeManifest(manifest) {
        const tools = [];

        if (Array.isArray(manifest.tools)) {
            for (const tool of manifest.tools) {
                tools.push(this.#normalizeTool(tool, 'uncategorized'));
            }
        }

        return {
            version: '1.0.0',
            lastUpdated: new Date().toISOString(),
            categories: {},
            tools,
            metadata: {}
        };
    }

    /**
     * Normalize individual tool data
     * @param {Object} tool
     * @param {string} category
     * @returns {Object}
     */
    #normalizeTool(tool, category) {
        return {
            id: tool.id || this.#generateId(tool.filename || tool.title),
            title: tool.title || tool.name || 'Untitled',
            description: tool.description || '',
            filename: tool.filename || tool.file || '',
            path: tool.path || tool.filename || '',
            category: tool.category || category,
            tags: Array.isArray(tool.tags) ? tool.tags : [],
            complexity: tool.complexity || 'intermediate',
            interactionType: tool.interactionType || tool.type || 'interactive',
            featured: Boolean(tool.featured),
            polished: Boolean(tool.polished),
            archived: Boolean(tool.archived),
            dateAdded: tool.dateAdded || tool.date || null,
            thumbnail: tool.thumbnail || null,
            metadata: tool.metadata || {}
        };
    }

    /**
     * Generate a unique ID from a string
     * @param {string} str
     * @returns {string}
     */
    #generateId(str) {
        return str
            .toLowerCase()
            .replace(/\.html?$/i, '')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '');
    }

    /**
     * Clear the cache
     */
    clearCache() {
        this.#cache.clear();
    }

    /**
     * Reload config (bypasses cache)
     * @returns {Promise<LoadResult>}
     */
    async reloadConfig() {
        this.clearCache();
        return this.loadConfig();
    }

    /**
     * Get cached data
     * @param {string} path
     * @returns {any|null}
     */
    getCached(path) {
        return this.#cache.get(path) || null;
    }
}

export { DataLoader };
