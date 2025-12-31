/**
 * Archive View - Display archived/deprecated tools
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';
import { ToolRepository } from '../data/tool-repository.js';

class ArchiveView {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {ArchiveView}
     */
    static getInstance() {
        if (!ArchiveView.#instance) {
            ArchiveView.#instance = new ArchiveView();
        }
        return ArchiveView.#instance;
    }

    constructor() {
        if (ArchiveView.#instance) {
            return ArchiveView.#instance;
        }

        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();
        this.repository = ToolRepository.getInstance();
        this.#container = null;
        this.#isActive = false;
        this.#sortBy = 'archivedDate';
        this.#sortOrder = 'desc';

        this.#bindEvents();
    }

    #container;
    #isActive;
    #sortBy;
    #sortOrder;

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.events.on(EVENTS.VIEW_CHANGE, ({ mode }) => {
            if (mode === 'archive') {
                this.activate();
            } else if (this.#isActive) {
                this.deactivate();
            }
        });

        this.events.on(EVENTS.TOOL_ARCHIVED, () => {
            if (this.#isActive) {
                this.render();
            }
        });

        this.events.on(EVENTS.TOOL_RESTORED, () => {
            if (this.#isActive) {
                this.render();
            }
        });
    }

    /**
     * Activate archive view
     */
    activate() {
        this.#isActive = true;
        this.render();
    }

    /**
     * Deactivate archive view
     */
    deactivate() {
        this.#isActive = false;
        if (this.#container) {
            this.#container.innerHTML = '';
        }
    }

    /**
     * Render archive view
     */
    render() {
        this.#container = document.getElementById('main-content') ||
            document.querySelector('.gallery-container');

        if (!this.#container) return;

        const archivedTools = this.#getArchivedTools();

        this.#container.innerHTML = `
            <div class="archive-view">
                <header class="archive-header">
                    <div class="archive-title-row">
                        <h1 class="archive-title">
                            <span class="archive-icon">📦</span>
                            Archive
                        </h1>
                        <span class="archive-count">${archivedTools.length} tool${archivedTools.length !== 1 ? 's' : ''}</span>
                    </div>
                    <p class="archive-description">
                        Tools that have been archived or deprecated. These tools are still accessible but are no longer actively maintained.
                    </p>
                    ${this.#renderControls()}
                </header>

                <div class="archive-content">
                    ${archivedTools.length === 0
                        ? this.#renderEmptyState()
                        : this.#renderToolList(archivedTools)
                    }
                </div>
            </div>
        `;

        this.#bindViewEvents();
        this.#injectStyles();
    }

    /**
     * Get archived tools
     * @returns {Array}
     */
    #getArchivedTools() {
        const tools = this.repository.getAll();
        let archived = tools.filter(t => t.archived || t.deprecated || t.status === 'archived');

        // Sort
        archived.sort((a, b) => {
            let aVal, bVal;

            switch (this.#sortBy) {
                case 'archivedDate':
                    aVal = a.archivedAt || a.updatedAt || 0;
                    bVal = b.archivedAt || b.updatedAt || 0;
                    break;
                case 'name':
                    aVal = a.title?.toLowerCase() || '';
                    bVal = b.title?.toLowerCase() || '';
                    break;
                case 'category':
                    aVal = a.category || '';
                    bVal = b.category || '';
                    break;
                default:
                    aVal = 0;
                    bVal = 0;
            }

            if (aVal < bVal) return this.#sortOrder === 'asc' ? -1 : 1;
            if (aVal > bVal) return this.#sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        return archived;
    }

    /**
     * Render controls
     * @returns {string}
     */
    #renderControls() {
        return `
            <div class="archive-controls">
                <div class="archive-sort">
                    <label for="archive-sort-select">Sort by:</label>
                    <select id="archive-sort-select" class="archive-sort-select">
                        <option value="archivedDate" ${this.#sortBy === 'archivedDate' ? 'selected' : ''}>
                            Archive Date
                        </option>
                        <option value="name" ${this.#sortBy === 'name' ? 'selected' : ''}>
                            Name
                        </option>
                        <option value="category" ${this.#sortBy === 'category' ? 'selected' : ''}>
                            Category
                        </option>
                    </select>
                    <button class="archive-sort-order btn btn-icon"
                            aria-label="Toggle sort order"
                            title="${this.#sortOrder === 'asc' ? 'Ascending' : 'Descending'}">
                        ${this.#sortOrder === 'asc' ? '↑' : '↓'}
                    </button>
                </div>

                <div class="archive-actions">
                    <button class="btn btn-secondary" id="archive-export-btn">
                        Export Archive List
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Render empty state
     * @returns {string}
     */
    #renderEmptyState() {
        return `
            <div class="archive-empty">
                <div class="archive-empty-icon">🎉</div>
                <h2>No Archived Tools</h2>
                <p>All tools are currently active. When tools are archived or deprecated, they'll appear here.</p>
                <button class="btn btn-primary" id="back-to-gallery-btn">
                    Back to Gallery
                </button>
            </div>
        `;
    }

    /**
     * Render tool list
     * @param {Array} tools
     * @returns {string}
     */
    #renderToolList(tools) {
        return `
            <div class="archive-list">
                ${tools.map(tool => this.#renderToolCard(tool)).join('')}
            </div>
        `;
    }

    /**
     * Render tool card
     * @param {Object} tool
     * @returns {string}
     */
    #renderToolCard(tool) {
        const archivedDate = tool.archivedAt
            ? new Date(tool.archivedAt).toLocaleDateString()
            : 'Unknown';

        return `
            <article class="archive-card" data-tool-id="${tool.id}">
                <div class="archive-card-header">
                    <h3 class="archive-card-title">${tool.title || tool.file}</h3>
                    <span class="archive-card-status ${tool.deprecated ? 'deprecated' : 'archived'}">
                        ${tool.deprecated ? 'Deprecated' : 'Archived'}
                    </span>
                </div>

                <p class="archive-card-description">
                    ${tool.description || 'No description available.'}
                </p>

                <div class="archive-card-meta">
                    <span class="archive-card-category">${tool.category || 'Uncategorized'}</span>
                    <span class="archive-card-date">Archived: ${archivedDate}</span>
                </div>

                ${tool.archiveReason ? `
                    <div class="archive-card-reason">
                        <strong>Reason:</strong> ${tool.archiveReason}
                    </div>
                ` : ''}

                ${tool.replacedBy ? `
                    <div class="archive-card-replacement">
                        <strong>Replaced by:</strong>
                        <a href="${tool.replacedBy}" class="archive-replacement-link">
                            ${tool.replacedByTitle || tool.replacedBy}
                        </a>
                    </div>
                ` : ''}

                <div class="archive-card-actions">
                    <button class="btn btn-secondary btn-sm archive-open-btn"
                            data-file="${tool.file}">
                        Open Anyway
                    </button>
                    <button class="btn btn-secondary btn-sm archive-restore-btn"
                            data-tool-id="${tool.id}">
                        Restore
                    </button>
                    <button class="btn btn-ghost btn-sm archive-delete-btn"
                            data-tool-id="${tool.id}">
                        Delete Permanently
                    </button>
                </div>
            </article>
        `;
    }

    /**
     * Bind view events
     */
    #bindViewEvents() {
        // Sort select
        const sortSelect = this.#container.querySelector('#archive-sort-select');
        sortSelect?.addEventListener('change', (e) => {
            this.#sortBy = e.target.value;
            this.render();
        });

        // Sort order toggle
        const sortOrderBtn = this.#container.querySelector('.archive-sort-order');
        sortOrderBtn?.addEventListener('click', () => {
            this.#sortOrder = this.#sortOrder === 'asc' ? 'desc' : 'asc';
            this.render();
        });

        // Export button
        const exportBtn = this.#container.querySelector('#archive-export-btn');
        exportBtn?.addEventListener('click', () => this.#exportArchiveList());

        // Back to gallery button
        const backBtn = this.#container.querySelector('#back-to-gallery-btn');
        backBtn?.addEventListener('click', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
        });

        // Open buttons
        this.#container.querySelectorAll('.archive-open-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const file = e.target.dataset.file;
                window.open(file, '_blank');
            });
        });

        // Restore buttons
        this.#container.querySelectorAll('.archive-restore-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const toolId = e.target.dataset.toolId;
                this.#restoreTool(toolId);
            });
        });

        // Delete buttons
        this.#container.querySelectorAll('.archive-delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const toolId = e.target.dataset.toolId;
                this.#confirmDelete(toolId);
            });
        });
    }

    /**
     * Export archive list
     */
    #exportArchiveList() {
        const tools = this.#getArchivedTools();
        const data = {
            exportedAt: new Date().toISOString(),
            count: tools.length,
            tools: tools.map(t => ({
                id: t.id,
                title: t.title,
                file: t.file,
                category: t.category,
                archivedAt: t.archivedAt,
                reason: t.archiveReason,
                replacedBy: t.replacedBy
            }))
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `archive-list-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Restore tool from archive
     * @param {string} toolId
     */
    #restoreTool(toolId) {
        // This would need to update the tool repository
        // For now, emit an event
        this.events.emit(EVENTS.TOOL_RESTORED, { toolId });

        // Show notification
        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'Tool restored from archive',
            type: 'success'
        });
    }

    /**
     * Confirm delete
     * @param {string} toolId
     */
    #confirmDelete(toolId) {
        const tool = this.repository.getById(toolId);
        if (!tool) return;

        // Use modal manager for confirmation
        this.events.emit(EVENTS.MODAL_CONFIRM, {
            title: 'Delete Tool',
            message: `Are you sure you want to permanently delete "${tool.title}"? This cannot be undone.`,
            confirmText: 'Delete',
            confirmClass: 'btn-danger',
            onConfirm: () => {
                this.events.emit(EVENTS.TOOL_DELETED, { toolId });
                this.render();
            }
        });
    }

    /**
     * Inject styles
     */
    #injectStyles() {
        if (document.getElementById('archive-view-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'archive-view-styles';
        styles.textContent = `
            .archive-view {
                padding: var(--space-6);
                max-width: 1200px;
                margin: 0 auto;
            }

            .archive-header {
                margin-bottom: var(--space-6);
            }

            .archive-title-row {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                margin-bottom: var(--space-2);
            }

            .archive-title {
                display: flex;
                align-items: center;
                gap: var(--space-2);
                font-size: var(--text-2xl);
                margin: 0;
            }

            .archive-icon {
                font-size: var(--text-3xl);
            }

            .archive-count {
                padding: var(--space-1) var(--space-3);
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-full);
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
            }

            .archive-description {
                color: var(--color-text-secondary);
                margin-bottom: var(--space-4);
            }

            .archive-controls {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: var(--space-3);
            }

            .archive-sort {
                display: flex;
                align-items: center;
                gap: var(--space-2);
            }

            .archive-sort label {
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
            }

            .archive-sort-select {
                padding: var(--space-2) var(--space-3);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-md);
                background: var(--color-bg-secondary);
                color: var(--color-text-primary);
            }

            .archive-empty {
                text-align: center;
                padding: var(--space-12);
            }

            .archive-empty-icon {
                font-size: 4rem;
                margin-bottom: var(--space-4);
            }

            .archive-empty h2 {
                margin: 0 0 var(--space-2);
            }

            .archive-empty p {
                color: var(--color-text-secondary);
                margin-bottom: var(--space-6);
            }

            .archive-list {
                display: grid;
                gap: var(--space-4);
            }

            .archive-card {
                background: var(--color-bg-secondary);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-lg);
                padding: var(--space-4);
            }

            .archive-card-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: var(--space-3);
                margin-bottom: var(--space-2);
            }

            .archive-card-title {
                font-size: var(--text-lg);
                margin: 0;
            }

            .archive-card-status {
                padding: var(--space-1) var(--space-2);
                border-radius: var(--radius-sm);
                font-size: var(--text-xs);
                font-weight: 500;
                text-transform: uppercase;
            }

            .archive-card-status.archived {
                background: var(--color-bg-tertiary);
                color: var(--color-text-secondary);
            }

            .archive-card-status.deprecated {
                background: rgba(var(--color-warning-rgb, 251, 191, 36), 0.2);
                color: var(--color-warning, #FBBF24);
            }

            .archive-card-description {
                color: var(--color-text-secondary);
                margin-bottom: var(--space-3);
            }

            .archive-card-meta {
                display: flex;
                gap: var(--space-4);
                font-size: var(--text-sm);
                color: var(--color-text-tertiary);
                margin-bottom: var(--space-3);
            }

            .archive-card-reason,
            .archive-card-replacement {
                font-size: var(--text-sm);
                padding: var(--space-2);
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-md);
                margin-bottom: var(--space-3);
            }

            .archive-replacement-link {
                color: var(--color-accent);
            }

            .archive-card-actions {
                display: flex;
                gap: var(--space-2);
                flex-wrap: wrap;
            }

            @media (max-width: 640px) {
                .archive-view {
                    padding: var(--space-4);
                }

                .archive-controls {
                    flex-direction: column;
                    align-items: stretch;
                }

                .archive-card-header {
                    flex-direction: column;
                }

                .archive-card-actions {
                    flex-direction: column;
                }

                .archive-card-actions .btn {
                    width: 100%;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

export { ArchiveView };
