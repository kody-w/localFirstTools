/**
 * Collections Manager - Tool collections management
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../../core/event-bus.js';
import { StorageManager } from '../../storage/storage-manager.js';

class CollectionsManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {CollectionsManager}
     */
    static getInstance() {
        if (!CollectionsManager.#instance) {
            CollectionsManager.#instance = new CollectionsManager();
        }
        return CollectionsManager.#instance;
    }

    constructor() {
        if (CollectionsManager.#instance) {
            return CollectionsManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();

        this.#collections = new Map();
        this.#loadCollections();
        this.#bindEvents();
    }

    #collections;

    /**
     * Load collections from storage
     */
    #loadCollections() {
        const stored = this.storage.get('collections') || [];

        for (const collection of stored) {
            this.#collections.set(collection.id, {
                ...collection,
                tools: new Set(collection.tools || [])
            });
        }

        // Create default collection if none exist
        if (this.#collections.size === 0) {
            this.createCollection('Favorites', {
                icon: '⭐',
                color: '#ffd700',
                isDefault: true
            });
        }
    }

    /**
     * Save collections to storage
     */
    #saveCollections() {
        const data = Array.from(this.#collections.values()).map(col => ({
            ...col,
            tools: [...col.tools]
        }));

        this.storage.set('collections', data);
        this.events.emit(EVENTS.COLLECTIONS_CHANGE, { collections: this.getAll() });
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.events.on(EVENTS.TOOL_ADD_TO_COLLECTION, ({ toolId, collectionId }) => {
            if (collectionId) {
                this.addTool(collectionId, toolId);
            }
        });
    }

    /**
     * Create a new collection
     * @param {string} name
     * @param {Object} options
     * @returns {Object}
     */
    createCollection(name, options = {}) {
        const id = `col_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        const collection = {
            id,
            name,
            description: options.description || '',
            icon: options.icon || '📁',
            color: options.color || '#06ffa5',
            tools: new Set(),
            isDefault: options.isDefault || false,
            createdAt: Date.now(),
            updatedAt: Date.now()
        };

        this.#collections.set(id, collection);
        this.#saveCollections();

        this.events.emit(EVENTS.COLLECTION_CREATED, { collection: this.#serializeCollection(collection) });

        return this.#serializeCollection(collection);
    }

    /**
     * Update a collection
     * @param {string} collectionId
     * @param {Object} updates
     * @returns {Object|null}
     */
    updateCollection(collectionId, updates) {
        const collection = this.#collections.get(collectionId);
        if (!collection) return null;

        // Apply updates
        if (updates.name !== undefined) collection.name = updates.name;
        if (updates.description !== undefined) collection.description = updates.description;
        if (updates.icon !== undefined) collection.icon = updates.icon;
        if (updates.color !== undefined) collection.color = updates.color;

        collection.updatedAt = Date.now();

        this.#saveCollections();

        this.events.emit(EVENTS.COLLECTION_UPDATED, { collection: this.#serializeCollection(collection) });

        return this.#serializeCollection(collection);
    }

    /**
     * Delete a collection
     * @param {string} collectionId
     * @returns {boolean}
     */
    deleteCollection(collectionId) {
        const collection = this.#collections.get(collectionId);
        if (!collection || collection.isDefault) return false;

        this.#collections.delete(collectionId);
        this.#saveCollections();

        this.events.emit(EVENTS.COLLECTION_DELETED, { collectionId });

        return true;
    }

    /**
     * Add tool to collection
     * @param {string} collectionId
     * @param {string} toolId
     * @returns {boolean}
     */
    addTool(collectionId, toolId) {
        const collection = this.#collections.get(collectionId);
        if (!collection) return false;

        collection.tools.add(toolId);
        collection.updatedAt = Date.now();

        this.#saveCollections();

        this.events.emit(EVENTS.TOOL_ADDED_TO_COLLECTION, {
            collectionId,
            toolId,
            collection: this.#serializeCollection(collection)
        });

        return true;
    }

    /**
     * Remove tool from collection
     * @param {string} collectionId
     * @param {string} toolId
     * @returns {boolean}
     */
    removeTool(collectionId, toolId) {
        const collection = this.#collections.get(collectionId);
        if (!collection) return false;

        const removed = collection.tools.delete(toolId);

        if (removed) {
            collection.updatedAt = Date.now();
            this.#saveCollections();

            this.events.emit(EVENTS.TOOL_REMOVED_FROM_COLLECTION, {
                collectionId,
                toolId,
                collection: this.#serializeCollection(collection)
            });
        }

        return removed;
    }

    /**
     * Toggle tool in collection
     * @param {string} collectionId
     * @param {string} toolId
     * @returns {boolean} - New state (true if added, false if removed)
     */
    toggleTool(collectionId, toolId) {
        const collection = this.#collections.get(collectionId);
        if (!collection) return false;

        if (collection.tools.has(toolId)) {
            this.removeTool(collectionId, toolId);
            return false;
        } else {
            this.addTool(collectionId, toolId);
            return true;
        }
    }

    /**
     * Move tool between collections
     * @param {string} fromCollectionId
     * @param {string} toCollectionId
     * @param {string} toolId
     * @returns {boolean}
     */
    moveTool(fromCollectionId, toCollectionId, toolId) {
        const removed = this.removeTool(fromCollectionId, toolId);
        if (removed) {
            return this.addTool(toCollectionId, toolId);
        }
        return false;
    }

    /**
     * Get collection by ID
     * @param {string} collectionId
     * @returns {Object|null}
     */
    getCollection(collectionId) {
        const collection = this.#collections.get(collectionId);
        return collection ? this.#serializeCollection(collection) : null;
    }

    /**
     * Get all collections
     * @returns {Array}
     */
    getAll() {
        return Array.from(this.#collections.values()).map(col => this.#serializeCollection(col));
    }

    /**
     * Get default collection
     * @returns {Object|null}
     */
    getDefaultCollection() {
        for (const collection of this.#collections.values()) {
            if (collection.isDefault) {
                return this.#serializeCollection(collection);
            }
        }
        return null;
    }

    /**
     * Get collections containing a tool
     * @param {string} toolId
     * @returns {Array}
     */
    getCollectionsForTool(toolId) {
        return Array.from(this.#collections.values())
            .filter(col => col.tools.has(toolId))
            .map(col => this.#serializeCollection(col));
    }

    /**
     * Check if tool is in collection
     * @param {string} collectionId
     * @param {string} toolId
     * @returns {boolean}
     */
    hasToolInCollection(collectionId, toolId) {
        const collection = this.#collections.get(collectionId);
        return collection ? collection.tools.has(toolId) : false;
    }

    /**
     * Get tools in collection
     * @param {string} collectionId
     * @returns {Array}
     */
    getToolsInCollection(collectionId) {
        const collection = this.#collections.get(collectionId);
        return collection ? [...collection.tools] : [];
    }

    /**
     * Search collections
     * @param {string} query
     * @returns {Array}
     */
    search(query) {
        const lowerQuery = query.toLowerCase();

        return this.getAll().filter(col =>
            col.name.toLowerCase().includes(lowerQuery) ||
            col.description.toLowerCase().includes(lowerQuery)
        );
    }

    /**
     * Get collection stats
     * @returns {Object}
     */
    getStats() {
        let totalTools = 0;
        let totalUniqueTools = new Set();

        for (const collection of this.#collections.values()) {
            totalTools += collection.tools.size;
            for (const toolId of collection.tools) {
                totalUniqueTools.add(toolId);
            }
        }

        return {
            totalCollections: this.#collections.size,
            totalTools,
            uniqueTools: totalUniqueTools.size
        };
    }

    /**
     * Export collections as JSON
     * @returns {string}
     */
    exportCollections() {
        return JSON.stringify(this.getAll(), null, 2);
    }

    /**
     * Import collections from JSON
     * @param {string} json
     * @returns {number} - Number of collections imported
     */
    importCollections(json) {
        try {
            const collections = JSON.parse(json);
            let imported = 0;

            for (const col of collections) {
                // Don't overwrite existing collections with same name
                const existing = Array.from(this.#collections.values())
                    .find(c => c.name === col.name);

                if (!existing) {
                    this.createCollection(col.name, {
                        description: col.description,
                        icon: col.icon,
                        color: col.color
                    });

                    // Add tools to newly created collection
                    const newCol = Array.from(this.#collections.values())
                        .find(c => c.name === col.name);

                    if (newCol && col.tools) {
                        for (const toolId of col.tools) {
                            this.addTool(newCol.id, toolId);
                        }
                    }

                    imported++;
                }
            }

            return imported;
        } catch (e) {
            console.error('Failed to import collections:', e);
            throw new Error('Invalid collections format');
        }
    }

    /**
     * Serialize collection for external use
     * @param {Object} collection
     * @returns {Object}
     */
    #serializeCollection(collection) {
        return {
            ...collection,
            tools: [...collection.tools],
            toolCount: collection.tools.size
        };
    }

    /**
     * Clear all collections
     */
    clearAll() {
        this.#collections.clear();
        this.storage.remove('collections');

        // Recreate default collection
        this.createCollection('Favorites', {
            icon: '⭐',
            color: '#ffd700',
            isDefault: true
        });

        this.events.emit(EVENTS.COLLECTIONS_CLEARED);
    }
}

export { CollectionsManager };
