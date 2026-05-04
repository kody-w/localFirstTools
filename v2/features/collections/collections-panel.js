/**
 * Collections Panel - Enhanced collections UI
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../../core/event-bus.js';
import { CollectionsManager } from './collections-manager.js';
import { ToolRepository } from '../../data/tool-repository.js';

class CollectionsPanel {
    constructor() {
        this.events = EventBus.getInstance();
        this.manager = CollectionsManager.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#isVisible = false;
        this.#selectedCollection = null;
    }

    #container;
    #isVisible;
    #selectedCollection;

    /**
     * Show collections panel
     * @param {HTMLElement} parentContainer
     */
    show(parentContainer) {
        if (this.#isVisible) return;

        this.#container = document.createElement('div');
        this.#container.className = 'collections-panel';
        this.#render();

        parentContainer.appendChild(this.#container);
        this.#isVisible = true;

        this.#injectStyles();
        this.#bindEvents();

        // Animate in
        requestAnimationFrame(() => {
            this.#container.classList.add('visible');
        });
    }

    /**
     * Hide panel
     */
    hide() {
        if (!this.#isVisible || !this.#container) return;

        this.#container.classList.remove('visible');

        setTimeout(() => {
            this.#container?.remove();
            this.#container = null;
            this.#isVisible = false;
        }, 300);
    }

    /**
     * Toggle panel visibility
     * @param {HTMLElement} parentContainer
     */
    toggle(parentContainer) {
        if (this.#isVisible) {
            this.hide();
        } else {
            this.show(parentContainer);
        }
    }

    /**
     * Render panel content
     */
    #render() {
        const collections = this.manager.getAll();

        this.#container.innerHTML = `
            <div class="panel-header">
                <h2>Collections</h2>
                <div class="panel-actions">
                    <button class="btn btn-icon" id="create-collection" title="Create collection">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 5v14M5 12h14"/>
                        </svg>
                    </button>
                    <button class="btn btn-icon panel-close" title="Close">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
            </div>

            <div class="collections-list">
                ${collections.map(col => this.#renderCollectionItem(col)).join('')}
            </div>

            <div class="collection-detail" id="collection-detail" style="display: none;">
                <!-- Filled when collection selected -->
            </div>

            <div class="panel-footer">
                <button class="btn btn-secondary btn-sm" id="export-collections">
                    Export All
                </button>
                <button class="btn btn-ghost btn-sm" id="import-collections">
                    Import
                </button>
            </div>
        `;
    }

    /**
     * Render collection item
     * @param {Object} collection
     * @returns {string}
     */
    #renderCollectionItem(collection) {
        return `
            <div class="collection-item" data-collection-id="${collection.id}">
                <div class="collection-icon" style="background: ${collection.color}20; color: ${collection.color}">
                    ${collection.icon}
                </div>
                <div class="collection-info">
                    <span class="collection-name">${collection.name}</span>
                    <span class="collection-count">${collection.toolCount} tools</span>
                </div>
                <button class="btn btn-icon btn-sm collection-menu" title="Menu">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="6" r="2"/>
                        <circle cx="12" cy="12" r="2"/>
                        <circle cx="12" cy="18" r="2"/>
                    </svg>
                </button>
            </div>
        `;
    }

    /**
     * Render collection detail
     * @param {Object} collection
     */
    #renderCollectionDetail(collection) {
        const toolIds = this.manager.getToolsInCollection(collection.id);
        const tools = toolIds.map(id => this.toolRepo.getById(id)).filter(Boolean);

        const detailEl = this.#container.querySelector('#collection-detail');
        if (!detailEl) return;

        detailEl.innerHTML = `
            <div class="detail-header">
                <button class="btn btn-icon btn-sm back-btn" title="Back">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 12H5M12 19l-7-7 7-7"/>
                    </svg>
                </button>
                <div class="detail-title">
                    <span class="detail-icon" style="color: ${collection.color}">${collection.icon}</span>
                    <h3>${collection.name}</h3>
                </div>
                <button class="btn btn-icon btn-sm edit-collection" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                </button>
            </div>

            ${collection.description ? `<p class="detail-description">${collection.description}</p>` : ''}

            <div class="detail-tools">
                ${tools.length === 0 ? `
                    <p class="empty-message">No tools in this collection yet</p>
                ` : tools.map(tool => `
                    <div class="detail-tool" data-tool-id="${tool.id}">
                        <span class="tool-title">${tool.title}</span>
                        <button class="btn btn-icon btn-sm remove-tool" title="Remove from collection">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M18 6L6 18M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>
                `).join('')}
            </div>

            <div class="detail-actions">
                <button class="btn btn-primary btn-sm" id="view-collection-tools">
                    View All Tools
                </button>
                ${!collection.isDefault ? `
                    <button class="btn btn-ghost btn-sm text-error" id="delete-collection">
                        Delete Collection
                    </button>
                ` : ''}
            </div>
        `;

        detailEl.style.display = 'block';
        this.#container.querySelector('.collections-list').style.display = 'none';

        // Bind detail events
        this.#bindDetailEvents(collection);
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Close panel
        this.#container.querySelector('.panel-close')?.addEventListener('click', () => this.hide());

        // Create collection
        this.#container.querySelector('#create-collection')?.addEventListener('click', () => {
            this.#showCreateDialog();
        });

        // Collection item clicks
        this.#container.querySelectorAll('.collection-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (e.target.closest('.collection-menu')) return;

                const collectionId = item.dataset.collectionId;
                const collection = this.manager.getCollection(collectionId);
                if (collection) {
                    this.#selectedCollection = collection;
                    this.#renderCollectionDetail(collection);
                }
            });
        });

        // Export
        this.#container.querySelector('#export-collections')?.addEventListener('click', () => {
            this.#exportCollections();
        });

        // Import
        this.#container.querySelector('#import-collections')?.addEventListener('click', () => {
            this.#importCollections();
        });

        // Listen for collection changes
        this.events.on(EVENTS.COLLECTIONS_CHANGE, () => {
            if (this.#isVisible) {
                this.#render();
                this.#bindEvents();
            }
        });
    }

    /**
     * Bind detail view events
     * @param {Object} collection
     */
    #bindDetailEvents(collection) {
        // Back button
        this.#container.querySelector('.back-btn')?.addEventListener('click', () => {
            this.#container.querySelector('#collection-detail').style.display = 'none';
            this.#container.querySelector('.collections-list').style.display = 'block';
            this.#selectedCollection = null;
        });

        // Edit collection
        this.#container.querySelector('.edit-collection')?.addEventListener('click', () => {
            this.#showEditDialog(collection);
        });

        // Remove tools
        this.#container.querySelectorAll('.remove-tool').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const toolEl = btn.closest('.detail-tool');
                const toolId = toolEl.dataset.toolId;

                this.manager.removeTool(collection.id, toolId);
                toolEl.remove();
            });
        });

        // View all tools
        this.#container.querySelector('#view-collection-tools')?.addEventListener('click', () => {
            this.events.emit(EVENTS.FILTER_CHANGE, {
                collection: collection.id
            });
            this.hide();
        });

        // Delete collection
        this.#container.querySelector('#delete-collection')?.addEventListener('click', () => {
            if (confirm(`Delete "${collection.name}"? This cannot be undone.`)) {
                this.manager.deleteCollection(collection.id);
                this.#render();
                this.#bindEvents();
            }
        });
    }

    /**
     * Show create collection dialog
     */
    #showCreateDialog() {
        const name = prompt('Collection name:');
        if (!name) return;

        const icons = ['📁', '⭐', '🔥', '💡', '🎮', '🎨', '🔧', '📌'];
        const icon = icons[Math.floor(Math.random() * icons.length)];

        this.manager.createCollection(name, { icon });
        this.#render();
        this.#bindEvents();

        this.events.emit(EVENTS.NOTIFICATION, {
            message: `Collection "${name}" created`,
            type: 'success'
        });
    }

    /**
     * Show edit collection dialog
     * @param {Object} collection
     */
    #showEditDialog(collection) {
        const name = prompt('Collection name:', collection.name);
        if (!name) return;

        this.manager.updateCollection(collection.id, { name });

        const updated = this.manager.getCollection(collection.id);
        this.#renderCollectionDetail(updated);

        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'Collection updated',
            type: 'success'
        });
    }

    /**
     * Export collections
     */
    #exportCollections() {
        const data = this.manager.exportCollections();
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `collections-${new Date().toISOString().split('T')[0]}.json`;
        a.click();

        URL.revokeObjectURL(url);

        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'Collections exported',
            type: 'success'
        });
    }

    /**
     * Import collections
     */
    #importCollections() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';

        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            try {
                const text = await file.text();
                const count = this.manager.importCollections(text);

                this.events.emit(EVENTS.NOTIFICATION, {
                    message: `Imported ${count} collections`,
                    type: 'success'
                });

                this.#render();
                this.#bindEvents();
            } catch (err) {
                this.events.emit(EVENTS.NOTIFICATION, {
                    message: 'Failed to import collections',
                    type: 'error'
                });
            }
        };

        input.click();
    }

    /**
     * Inject panel styles
     */
    #injectStyles() {
        if (document.getElementById('collections-panel-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'collections-panel-styles';
        styles.textContent = `
            .collections-panel {
                position: fixed;
                top: 0;
                right: -400px;
                width: 400px;
                height: 100vh;
                background: var(--color-bg-elevated);
                border-left: 1px solid var(--color-border);
                box-shadow: var(--shadow-lg);
                display: flex;
                flex-direction: column;
                transition: right var(--duration-300) var(--ease-out);
                z-index: 1000;
            }

            .collections-panel.visible {
                right: 0;
            }

            @media (max-width: 480px) {
                .collections-panel {
                    width: 100%;
                    right: -100%;
                }
            }

            .panel-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .panel-header h2 {
                margin: 0;
                font-size: var(--text-lg);
            }

            .panel-actions {
                display: flex;
                gap: var(--space-2);
            }

            .collections-list {
                flex: 1;
                overflow-y: auto;
                padding: var(--space-3);
            }

            .collection-item {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                padding: var(--space-3);
                border-radius: var(--radius-lg);
                cursor: pointer;
                transition: background var(--duration-150);
            }

            .collection-item:hover {
                background: var(--color-bg-tertiary);
            }

            .collection-icon {
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: var(--radius-md);
                font-size: 20px;
            }

            .collection-info {
                flex: 1;
                min-width: 0;
            }

            .collection-name {
                display: block;
                font-weight: 500;
                color: var(--color-text-primary);
            }

            .collection-count {
                display: block;
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            .collection-menu {
                opacity: 0;
                transition: opacity var(--duration-150);
            }

            .collection-item:hover .collection-menu {
                opacity: 1;
            }

            /* Detail View */
            .collection-detail {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .detail-header {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .detail-title {
                flex: 1;
                display: flex;
                align-items: center;
                gap: var(--space-2);
            }

            .detail-title h3 {
                margin: 0;
                font-size: var(--text-lg);
            }

            .detail-icon {
                font-size: 24px;
            }

            .detail-description {
                padding: var(--space-3) var(--space-4);
                margin: 0;
                color: var(--color-text-secondary);
                font-size: var(--text-sm);
                border-bottom: 1px solid var(--color-border-subtle);
            }

            .detail-tools {
                flex: 1;
                overflow-y: auto;
                padding: var(--space-3);
            }

            .detail-tool {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: var(--space-3);
                border-radius: var(--radius-md);
                transition: background var(--duration-150);
            }

            .detail-tool:hover {
                background: var(--color-bg-tertiary);
            }

            .detail-tool .tool-title {
                font-size: var(--text-sm);
            }

            .detail-tool .remove-tool {
                opacity: 0;
                color: var(--color-error);
            }

            .detail-tool:hover .remove-tool {
                opacity: 1;
            }

            .detail-actions {
                display: flex;
                gap: var(--space-3);
                padding: var(--space-4);
                border-top: 1px solid var(--color-border);
            }

            .panel-footer {
                display: flex;
                gap: var(--space-3);
                padding: var(--space-4);
                border-top: 1px solid var(--color-border);
                justify-content: flex-end;
            }

            .empty-message {
                text-align: center;
                color: var(--color-text-tertiary);
                padding: var(--space-6);
            }

            .text-error {
                color: var(--color-error);
            }
        `;

        document.head.appendChild(styles);
    }
}

export { CollectionsPanel };
