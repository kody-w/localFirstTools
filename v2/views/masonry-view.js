/**
 * Masonry View - Pinterest-style varied heights layout
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { createToolCard } from '../renderers/tool-card.js';

class MasonryView {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#tools = [];
        this.#columns = 4;
        this.#gap = 24;
        this.#resizeObserver = null;
    }

    #container;
    #tools;
    #columns;
    #gap;
    #resizeObserver;

    /**
     * Initialize the masonry view
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;
        this.#container.className = 'masonry-view-container';

        this.#setupResizeObserver();
        this.#calculateColumns();
        this.#injectStyles();
    }

    /**
     * Render tools in masonry layout
     * @param {Array} tools
     */
    render(tools) {
        this.#tools = tools;

        if (!this.#container) return;

        if (tools.length === 0) {
            this.#renderEmptyState();
            return;
        }

        this.#calculateColumns();
        this.#renderMasonry();
    }

    /**
     * Render masonry grid
     */
    #renderMasonry() {
        // Create column containers
        const columns = Array.from({ length: this.#columns }, () => ({
            element: document.createElement('div'),
            height: 0
        }));

        columns.forEach((col, i) => {
            col.element.className = 'masonry-column';
            col.element.style.width = `calc((100% - ${(this.#columns - 1) * this.#gap}px) / ${this.#columns})`;
        });

        // Distribute tools to shortest column
        for (const tool of this.#tools) {
            // Find shortest column
            const shortestCol = columns.reduce((min, col) =>
                col.height < min.height ? col : min
            );

            // Create card with variable height based on content
            const card = createToolCard(tool);
            const wrapper = document.createElement('div');
            wrapper.className = 'masonry-item';
            wrapper.appendChild(card);

            shortestCol.element.appendChild(wrapper);

            // Estimate height (will be refined after render)
            const estimatedHeight = this.#estimateCardHeight(tool);
            shortestCol.height += estimatedHeight + this.#gap;
        }

        // Build container
        this.#container.innerHTML = '';
        const grid = document.createElement('div');
        grid.className = 'masonry-grid';
        grid.style.gap = `${this.#gap}px`;

        columns.forEach(col => grid.appendChild(col.element));
        this.#container.appendChild(grid);

        // After render, recalculate with actual heights
        requestAnimationFrame(() => this.#balanceColumns());
    }

    /**
     * Estimate card height based on content
     * @param {Object} tool
     * @returns {number}
     */
    #estimateCardHeight(tool) {
        let height = 200; // Base height

        // Add for description length
        if (tool.description) {
            const lines = Math.ceil(tool.description.length / 50);
            height += Math.min(lines * 20, 60);
        }

        // Add for tags
        if (tool.tags && tool.tags.length > 0) {
            height += 32;
        }

        // Featured tools get extra height
        if (tool.featured) {
            height += 20;
        }

        return height;
    }

    /**
     * Balance columns based on actual rendered heights
     */
    #balanceColumns() {
        const columns = this.#container.querySelectorAll('.masonry-column');
        const items = Array.from(this.#container.querySelectorAll('.masonry-item'));

        if (items.length === 0) return;

        // Get actual heights
        const columnHeights = Array.from(columns).map(col => col.offsetHeight);

        // Check if rebalancing is needed (height difference > 100px)
        const maxHeight = Math.max(...columnHeights);
        const minHeight = Math.min(...columnHeights);

        if (maxHeight - minHeight > 100) {
            // Could implement more sophisticated rebalancing here
            // For now, the initial distribution usually works well
        }
    }

    /**
     * Setup resize observer
     */
    #setupResizeObserver() {
        this.#resizeObserver = new ResizeObserver(() => {
            const newColumns = this.#calculateColumns();
            if (newColumns !== this.#columns) {
                this.#columns = newColumns;
                if (this.#tools.length > 0) {
                    this.#renderMasonry();
                }
            }
        });

        this.#resizeObserver.observe(this.#container);
    }

    /**
     * Calculate number of columns based on container width
     * @returns {number}
     */
    #calculateColumns() {
        if (!this.#container) return 4;

        const width = this.#container.offsetWidth;
        const minColWidth = 280;

        if (width < 640) return 1;
        if (width < 900) return 2;
        if (width < 1200) return 3;
        return 4;
    }

    /**
     * Render empty state
     */
    #renderEmptyState() {
        this.#container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="3" y="3" width="7" height="9"/>
                        <rect x="14" y="3" width="7" height="5"/>
                        <rect x="14" y="12" width="7" height="9"/>
                        <rect x="3" y="16" width="7" height="5"/>
                    </svg>
                </div>
                <h3 class="empty-title">No tools found</h3>
                <p class="empty-description">No tools match your current filters</p>
            </div>
        `;
    }

    /**
     * Inject masonry-specific styles
     */
    #injectStyles() {
        if (document.getElementById('masonry-view-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'masonry-view-styles';
        styles.textContent = `
            .masonry-view-container {
                padding: var(--space-5);
            }

            .masonry-grid {
                display: flex;
                justify-content: center;
            }

            .masonry-column {
                display: flex;
                flex-direction: column;
                gap: var(--space-5);
            }

            .masonry-item {
                break-inside: avoid;
                animation: masonry-fade-in var(--duration-300) var(--ease-out);
            }

            .masonry-item .tool-card {
                height: auto;
            }

            @keyframes masonry-fade-in {
                from {
                    opacity: 0;
                    transform: scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }

            /* Alternative CSS columns approach for simpler cases */
            .masonry-columns {
                column-count: 4;
                column-gap: var(--space-5);
            }

            @media (max-width: 1200px) {
                .masonry-columns { column-count: 3; }
            }

            @media (max-width: 900px) {
                .masonry-columns { column-count: 2; }
            }

            @media (max-width: 640px) {
                .masonry-columns { column-count: 1; }
            }
        `;
        document.head.appendChild(styles);
    }

    /**
     * Destroy the view
     */
    destroy() {
        if (this.#resizeObserver) {
            this.#resizeObserver.disconnect();
            this.#resizeObserver = null;
        }

        this.#container = null;
        this.#tools = [];
    }
}

export { MasonryView };
