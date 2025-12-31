/**
 * List View - Compact single-line tool list
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { SearchController } from '../search/search-controller.js';

class ListView {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
        this.searchController = SearchController.getInstance();

        this.#container = null;
        this.#tools = [];
    }

    #container;
    #tools;

    /**
     * Initialize the list view
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;
        this.#container.className = 'list-view-container';
    }

    /**
     * Render tools as a list
     * @param {Array} tools
     */
    render(tools) {
        this.#tools = tools;

        if (!this.#container) return;

        if (tools.length === 0) {
            this.#renderEmptyState();
            return;
        }

        const user = this.state.getSlice('user');
        const pinnedSet = new Set(user.pinnedTools);

        this.#container.innerHTML = `
            <div class="list-view">
                <table class="list-table" role="grid">
                    <thead>
                        <tr>
                            <th scope="col" class="list-col-pin" aria-label="Pinned"></th>
                            <th scope="col" class="list-col-title">Title</th>
                            <th scope="col" class="list-col-category">Category</th>
                            <th scope="col" class="list-col-complexity">Complexity</th>
                            <th scope="col" class="list-col-tags">Tags</th>
                            <th scope="col" class="list-col-actions">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tools.map(tool => this.#renderRow(tool, pinnedSet.has(tool.id))).join('')}
                    </tbody>
                </table>
            </div>
        `;

        this.#bindEvents();
        this.#injectStyles();
    }

    /**
     * Render a single row
     * @param {Object} tool
     * @param {boolean} isPinned
     * @returns {string}
     */
    #renderRow(tool, isPinned) {
        const category = this.toolRepo.getCategory(tool.category);
        const title = this.searchController.highlight(tool.title);

        return `
            <tr class="list-row ${isPinned ? 'pinned' : ''}" data-tool-id="${tool.id}">
                <td class="list-col-pin">
                    <button class="pin-btn-mini ${isPinned ? 'active' : ''}"
                            data-action="pin"
                            aria-label="${isPinned ? 'Unpin' : 'Pin'}"
                            aria-pressed="${isPinned}">
                        ${isPinned ? '★' : '☆'}
                    </button>
                </td>
                <td class="list-col-title">
                    <a href="../${tool.path}" target="_blank" class="list-title" data-action="open">
                        ${tool.featured ? '<span class="featured-dot" title="Featured">★</span>' : ''}
                        ${title}
                    </a>
                </td>
                <td class="list-col-category">
                    <span class="category-badge-mini" style="--cat-color: ${category?.color || '#888'}">
                        ${category?.icon || ''} ${category?.title || tool.category}
                    </span>
                </td>
                <td class="list-col-complexity">
                    <span class="complexity-badge complexity-${tool.complexity}">
                        ${tool.complexity}
                    </span>
                </td>
                <td class="list-col-tags">
                    ${tool.tags.slice(0, 2).map(tag => `
                        <span class="tag-mini">${tag}</span>
                    `).join('')}
                    ${tool.tags.length > 2 ? `<span class="tag-more">+${tool.tags.length - 2}</span>` : ''}
                </td>
                <td class="list-col-actions">
                    <button class="btn-mini" data-action="preview">Preview</button>
                </td>
            </tr>
        `;
    }

    /**
     * Render empty state
     */
    #renderEmptyState() {
        this.#container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
                        <rect x="9" y="3" width="6" height="4" rx="2"/>
                    </svg>
                </div>
                <h3 class="empty-title">No tools found</h3>
                <p class="empty-description">Try adjusting your filters</p>
            </div>
        `;
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.#container.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]')?.dataset.action;
            const row = e.target.closest('[data-tool-id]');
            const toolId = row?.dataset.toolId;

            if (!toolId) return;

            switch (action) {
                case 'pin':
                    e.preventDefault();
                    this.#handlePin(toolId);
                    break;
                case 'open':
                    this.#handleOpen(toolId);
                    break;
                case 'preview':
                    e.preventDefault();
                    this.#handlePreview(toolId);
                    break;
            }
        });
    }

    /**
     * Handle pin toggle
     * @param {string} toolId
     */
    #handlePin(toolId) {
        const user = this.state.getSlice('user');
        const pinnedTools = [...user.pinnedTools];
        const index = pinnedTools.indexOf(toolId);

        if (index === -1) {
            pinnedTools.push(toolId);
            this.events.emit(EVENTS.TOOL_PIN, { toolId });
        } else {
            pinnedTools.splice(index, 1);
            this.events.emit(EVENTS.TOOL_UNPIN, { toolId });
        }

        this.state.setSlice('user', { ...user, pinnedTools });

        // Update row state
        const row = this.#container.querySelector(`[data-tool-id="${toolId}"]`);
        const btn = row?.querySelector('.pin-btn-mini');
        if (row && btn) {
            const isPinned = index === -1;
            row.classList.toggle('pinned', isPinned);
            btn.classList.toggle('active', isPinned);
            btn.innerHTML = isPinned ? '★' : '☆';
            btn.setAttribute('aria-pressed', isPinned.toString());
        }
    }

    /**
     * Handle open
     * @param {string} toolId
     */
    #handleOpen(toolId) {
        const user = this.state.getSlice('user');
        const usage = { ...user.usage };
        usage[toolId] = (usage[toolId] || 0) + 1;

        const recentlyOpened = [
            toolId,
            ...user.recentlyOpened.filter(id => id !== toolId)
        ].slice(0, 10);

        this.state.setSlice('user', { ...user, usage, recentlyOpened });
        this.events.emit(EVENTS.TOOL_OPEN, { toolId });
    }

    /**
     * Handle preview
     * @param {string} toolId
     */
    #handlePreview(toolId) {
        const tool = this.toolRepo.getById(toolId);
        if (tool) {
            this.events.emit(EVENTS.TOOL_PREVIEW, { toolId, tool });
        }
    }

    /**
     * Inject list-specific styles
     */
    #injectStyles() {
        if (document.getElementById('list-view-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'list-view-styles';
        styles.textContent = `
            .list-view-container {
                padding: var(--space-4);
            }

            .list-view {
                background: var(--bg-elevated);
                border: 1px solid var(--border-primary);
                border-radius: var(--radius-xl);
                overflow: hidden;
            }

            .list-table {
                width: 100%;
                border-collapse: collapse;
            }

            .list-table th {
                text-align: left;
                padding: var(--space-3) var(--space-4);
                font-size: var(--text-xs);
                font-weight: var(--font-semibold);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--text-tertiary);
                background: var(--bg-tertiary);
                border-bottom: 1px solid var(--border-primary);
            }

            .list-row {
                transition: background var(--duration-150);
            }

            .list-row:hover {
                background: var(--bg-tertiary);
            }

            .list-row.pinned {
                background: rgba(6, 255, 165, 0.05);
            }

            .list-row td {
                padding: var(--space-3) var(--space-4);
                border-bottom: 1px solid var(--border-secondary);
                vertical-align: middle;
            }

            .list-col-pin {
                width: 40px;
                text-align: center;
            }

            .pin-btn-mini {
                background: none;
                border: none;
                font-size: 16px;
                cursor: pointer;
                color: var(--text-tertiary);
                padding: var(--space-1);
            }

            .pin-btn-mini.active {
                color: var(--color-accent);
            }

            .list-title {
                display: flex;
                align-items: center;
                gap: var(--space-2);
                color: var(--text-primary);
                text-decoration: none;
                font-weight: var(--font-medium);
            }

            .list-title:hover {
                color: var(--color-accent);
            }

            .featured-dot {
                color: var(--color-accent);
                font-size: 10px;
            }

            .category-badge-mini {
                display: inline-flex;
                align-items: center;
                gap: var(--space-1);
                font-size: var(--text-xs);
                color: var(--cat-color);
            }

            .tag-mini {
                display: inline-block;
                padding: 2px 6px;
                font-size: 10px;
                background: var(--bg-tertiary);
                border-radius: var(--radius-sm);
                color: var(--text-tertiary);
                margin-right: var(--space-1);
            }

            .tag-more {
                font-size: 10px;
                color: var(--text-muted);
            }

            .btn-mini {
                padding: var(--space-1) var(--space-2);
                font-size: var(--text-xs);
                background: var(--bg-tertiary);
                border: 1px solid var(--border-primary);
                border-radius: var(--radius-sm);
                color: var(--text-secondary);
                cursor: pointer;
                transition: all var(--duration-150);
            }

            .btn-mini:hover {
                border-color: var(--color-accent);
                color: var(--color-accent);
            }

            @media (max-width: 768px) {
                .list-col-tags,
                .list-col-complexity {
                    display: none;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    /**
     * Destroy the view
     */
    destroy() {
        this.#container = null;
        this.#tools = [];
    }
}

export { ListView };
