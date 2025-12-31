/**
 * Dashboard View - Category-focused overview
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { createToolCard } from '../renderers/tool-card.js';

class DashboardView {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#tools = [];
    }

    #container;
    #tools;

    /**
     * Initialize the dashboard view
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;
        this.#container.className = 'dashboard-view-container';
        this.#injectStyles();
    }

    /**
     * Render dashboard
     * @param {Array} tools
     */
    render(tools) {
        this.#tools = tools;

        if (!this.#container) return;

        const stats = this.toolRepo.getStats();
        const categories = this.toolRepo.getCategoriesWithCounts();
        const user = this.state.getSlice('user');

        this.#container.innerHTML = `
            <div class="dashboard">
                ${this.#renderStatsRow(stats)}
                ${this.#renderQuickActions(user)}
                ${this.#renderCategoryGrid(categories)}
                ${this.#renderRecentlyOpened(user)}
                ${this.#renderPopularTools(user)}
            </div>
        `;

        this.#bindEvents();
    }

    /**
     * Render stats row
     * @param {Object} stats
     * @returns {string}
     */
    #renderStatsRow(stats) {
        return `
            <div class="dashboard-stats">
                <div class="stat-card">
                    <div class="stat-value">${stats.total}</div>
                    <div class="stat-label">Total Tools</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.featured}</div>
                    <div class="stat-label">Featured</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.tags}</div>
                    <div class="stat-label">Tags</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${Object.keys(stats.categories).length}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
        `;
    }

    /**
     * Render quick actions
     * @param {Object} user
     * @returns {string}
     */
    #renderQuickActions(user) {
        const pinnedCount = user.pinnedTools?.length || 0;

        return `
            <div class="dashboard-section">
                <h2 class="dashboard-section-title">Quick Actions</h2>
                <div class="quick-actions">
                    <button class="quick-action" data-action="view-pinned">
                        <span class="quick-action-icon">📌</span>
                        <span class="quick-action-label">Pinned (${pinnedCount})</span>
                    </button>
                    <button class="quick-action" data-action="view-featured">
                        <span class="quick-action-icon">⭐</span>
                        <span class="quick-action-label">Featured</span>
                    </button>
                    <button class="quick-action" data-action="view-recent">
                        <span class="quick-action-icon">🕐</span>
                        <span class="quick-action-label">Recent</span>
                    </button>
                    <button class="quick-action" data-action="random-tool">
                        <span class="quick-action-icon">🎲</span>
                        <span class="quick-action-label">Random</span>
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Render category grid
     * @param {Array} categories
     * @returns {string}
     */
    #renderCategoryGrid(categories) {
        const categoryCards = categories.map(cat => `
            <button class="category-card" data-action="filter-category" data-category="${cat.key}"
                    style="--cat-color: ${cat.color}">
                <div class="category-icon">${cat.icon}</div>
                <div class="category-info">
                    <div class="category-name">${cat.title}</div>
                    <div class="category-count">${cat.count} tools</div>
                </div>
            </button>
        `).join('');

        return `
            <div class="dashboard-section">
                <h2 class="dashboard-section-title">Categories</h2>
                <div class="category-grid">
                    ${categoryCards}
                </div>
            </div>
        `;
    }

    /**
     * Render recently opened tools
     * @param {Object} user
     * @returns {string}
     */
    #renderRecentlyOpened(user) {
        const recentIds = user.recentlyOpened?.slice(0, 4) || [];

        if (recentIds.length === 0) {
            return '';
        }

        const recentTools = recentIds
            .map(id => this.toolRepo.getById(id))
            .filter(Boolean);

        if (recentTools.length === 0) {
            return '';
        }

        const toolsHTML = recentTools.map(tool => {
            const card = createToolCard(tool, { showPreview: false });
            return card.outerHTML;
        }).join('');

        return `
            <div class="dashboard-section">
                <h2 class="dashboard-section-title">Recently Opened</h2>
                <div class="dashboard-tools-grid">
                    ${toolsHTML}
                </div>
            </div>
        `;
    }

    /**
     * Render popular tools
     * @param {Object} user
     * @returns {string}
     */
    #renderPopularTools(user) {
        const usage = user.usage || {};

        // Get top 4 by usage
        const topIds = Object.entries(usage)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 4)
            .map(([id]) => id);

        if (topIds.length === 0) {
            return '';
        }

        const topTools = topIds
            .map(id => this.toolRepo.getById(id))
            .filter(Boolean);

        if (topTools.length === 0) {
            return '';
        }

        const toolsHTML = topTools.map(tool => {
            const card = createToolCard(tool, { showPreview: false });
            return card.outerHTML;
        }).join('');

        return `
            <div class="dashboard-section">
                <h2 class="dashboard-section-title">Most Used</h2>
                <div class="dashboard-tools-grid">
                    ${toolsHTML}
                </div>
            </div>
        `;
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.#container.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]')?.dataset.action;

            switch (action) {
                case 'filter-category':
                    const category = e.target.closest('[data-category]').dataset.category;
                    this.events.emit(EVENTS.FILTER_ADDED, { type: 'category', value: category });
                    this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
                    break;

                case 'view-pinned':
                    this.events.emit(EVENTS.FILTER_ADDED, { type: 'pinned', value: true });
                    this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
                    break;

                case 'view-featured':
                    this.events.emit(EVENTS.FILTER_ADDED, { type: 'featured', value: 'featured' });
                    this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
                    break;

                case 'view-recent':
                    this.events.emit(EVENTS.FILTER_ADDED, { type: 'recent', value: true });
                    this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
                    break;

                case 'random-tool':
                    this.#openRandomTool();
                    break;
            }
        });
    }

    /**
     * Open a random tool
     */
    #openRandomTool() {
        const tools = this.toolRepo.getAll();
        if (tools.length === 0) return;

        const randomTool = tools[Math.floor(Math.random() * tools.length)];
        window.open(`../${randomTool.path}`, '_blank');

        this.events.emit(EVENTS.TOOL_OPEN, { toolId: randomTool.id });
    }

    /**
     * Inject dashboard-specific styles
     */
    #injectStyles() {
        if (document.getElementById('dashboard-view-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'dashboard-view-styles';
        styles.textContent = `
            .dashboard-view-container {
                padding: var(--space-5);
            }

            .dashboard {
                max-width: 1400px;
                margin: 0 auto;
            }

            .dashboard-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: var(--space-4);
                margin-bottom: var(--space-6);
            }

            .stat-card {
                background: var(--bg-elevated);
                border: 1px solid var(--border-primary);
                border-radius: var(--radius-xl);
                padding: var(--space-5);
                text-align: center;
            }

            .stat-value {
                font-size: var(--text-4xl);
                font-weight: var(--font-bold);
                color: var(--color-accent);
                margin-bottom: var(--space-2);
            }

            .stat-label {
                font-size: var(--text-sm);
                color: var(--text-tertiary);
            }

            .dashboard-section {
                margin-bottom: var(--space-6);
            }

            .dashboard-section-title {
                font-size: var(--text-lg);
                font-weight: var(--font-semibold);
                margin-bottom: var(--space-4);
            }

            .quick-actions {
                display: flex;
                flex-wrap: wrap;
                gap: var(--space-3);
            }

            .quick-action {
                display: flex;
                align-items: center;
                gap: var(--space-2);
                padding: var(--space-3) var(--space-4);
                background: var(--bg-elevated);
                border: 1px solid var(--border-primary);
                border-radius: var(--radius-lg);
                cursor: pointer;
                transition: all var(--duration-150);
            }

            .quick-action:hover {
                border-color: var(--color-accent);
                background: var(--bg-tertiary);
            }

            .quick-action-icon {
                font-size: var(--text-xl);
            }

            .quick-action-label {
                font-size: var(--text-sm);
                color: var(--text-secondary);
            }

            .category-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: var(--space-3);
            }

            .category-card {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                padding: var(--space-4);
                background: var(--bg-elevated);
                border: 1px solid var(--border-primary);
                border-left: 4px solid var(--cat-color);
                border-radius: var(--radius-lg);
                cursor: pointer;
                transition: all var(--duration-150);
                text-align: left;
            }

            .category-card:hover {
                border-color: var(--cat-color);
                transform: translateX(4px);
            }

            .category-icon {
                font-size: var(--text-2xl);
            }

            .category-name {
                font-size: var(--text-sm);
                font-weight: var(--font-medium);
                color: var(--text-primary);
            }

            .category-count {
                font-size: var(--text-xs);
                color: var(--text-tertiary);
            }

            .dashboard-tools-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: var(--space-4);
            }

            @media (max-width: 768px) {
                .dashboard-stats {
                    grid-template-columns: repeat(2, 1fr);
                }

                .category-grid {
                    grid-template-columns: 1fr;
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

export { DashboardView };
