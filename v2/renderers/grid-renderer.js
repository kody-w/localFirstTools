/**
 * Grid Renderer - Virtual scrolling grid layout
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { createToolCard } from './tool-card.js';
import { DEFAULT_CARD_HEIGHT, LIMITS, DEBOUNCE } from '../core/constants.js';

class GridRenderer {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {GridRenderer}
     */
    static getInstance() {
        if (!GridRenderer.#instance) {
            GridRenderer.#instance = new GridRenderer();
        }
        return GridRenderer.#instance;
    }

    constructor() {
        if (GridRenderer.#instance) {
            throw new Error('Use GridRenderer.getInstance() instead of new GridRenderer()');
        }

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();

        this.#container = null;
        this.#scrollContainer = null;
        this.#tools = [];
        this.#renderedCards = new Map();
        this.#cardHeights = new Map();
        this.#virtualScrollEnabled = false;
        this.#scrollDebounce = null;
        this.#resizeObserver = null;
        this.#intersectionObserver = null;
        this.#columnsCount = 4;
        this.#cardWidth = 300;
        this.#gap = 24;
    }

    #container;
    #scrollContainer;
    #tools;
    #renderedCards;
    #cardHeights;
    #virtualScrollEnabled;
    #scrollDebounce;
    #resizeObserver;
    #intersectionObserver;
    #columnsCount;
    #cardWidth;
    #gap;

    /**
     * Initialize the grid renderer
     * @param {HTMLElement} container
     * @param {HTMLElement} scrollContainer
     */
    initialize(container, scrollContainer = window) {
        this.#container = container;
        this.#scrollContainer = scrollContainer;

        this.#setupResizeObserver();
        this.#calculateColumns();
        this.#setupScrollListener();

        // Subscribe to state changes
        this.state.subscribeToSlice('filteredTools', (tools) => {
            this.render(tools);
        });
    }

    /**
     * Render tools in the grid
     * @param {Array} tools
     * @param {boolean} animate
     */
    render(tools, animate = true) {
        this.#tools = tools;

        if (!this.#container) return;

        // Clear existing cards
        this.#clearCards();

        if (tools.length === 0) {
            this.#renderEmptyState();
            return;
        }

        // Decide rendering strategy based on tool count
        if (tools.length > 100) {
            this.#virtualScrollEnabled = true;
            this.#renderVirtual();
        } else {
            this.#virtualScrollEnabled = false;
            this.#renderAll(animate);
        }

        this.events.emit(EVENTS.VIEW_RENDERED, {
            toolCount: tools.length,
            virtual: this.#virtualScrollEnabled
        });
    }

    /**
     * Render all tools (non-virtual)
     * @param {boolean} animate
     */
    #renderAll(animate) {
        const fragment = document.createDocumentFragment();

        this.#tools.forEach((tool, index) => {
            const card = createToolCard(tool);

            if (animate) {
                card.style.animationDelay = `${Math.min(index * 50, 300)}ms`;
            }

            fragment.appendChild(card);
            this.#renderedCards.set(tool.id, card);
        });

        this.#container.innerHTML = '';
        this.#container.appendChild(fragment);

        if (animate) {
            this.#container.classList.add('animate-in');
            setTimeout(() => {
                this.#container.classList.remove('animate-in');
            }, 500);
        }
    }

    /**
     * Render with virtual scrolling
     */
    #renderVirtual() {
        // Calculate total height
        const rowCount = Math.ceil(this.#tools.length / this.#columnsCount);
        const totalHeight = rowCount * (DEFAULT_CARD_HEIGHT + this.#gap);

        // Set container height for scrollbar
        this.#container.style.height = `${totalHeight}px`;
        this.#container.classList.add('virtual-scroll');

        // Render visible range
        this.#updateVisibleCards();
    }

    /**
     * Update visible cards for virtual scrolling
     */
    #updateVisibleCards() {
        if (!this.#virtualScrollEnabled) return;

        const scrollTop = this.#getScrollTop();
        const viewportHeight = this.#getViewportHeight();
        const buffer = LIMITS.VIRTUAL_SCROLL_BUFFER;

        // Calculate visible row range
        const rowHeight = DEFAULT_CARD_HEIGHT + this.#gap;
        const startRow = Math.max(0, Math.floor(scrollTop / rowHeight) - buffer);
        const endRow = Math.min(
            Math.ceil(this.#tools.length / this.#columnsCount),
            Math.ceil((scrollTop + viewportHeight) / rowHeight) + buffer
        );

        // Calculate visible tool indices
        const startIndex = startRow * this.#columnsCount;
        const endIndex = Math.min(this.#tools.length, endRow * this.#columnsCount);

        // Get currently visible tool IDs
        const visibleIds = new Set();
        for (let i = startIndex; i < endIndex; i++) {
            visibleIds.add(this.#tools[i].id);
        }

        // Remove cards no longer visible
        for (const [id, card] of this.#renderedCards) {
            if (!visibleIds.has(id)) {
                card.remove();
                this.#renderedCards.delete(id);
            }
        }

        // Add new visible cards
        const fragment = document.createDocumentFragment();

        for (let i = startIndex; i < endIndex; i++) {
            const tool = this.#tools[i];

            if (!this.#renderedCards.has(tool.id)) {
                const card = createToolCard(tool);
                const row = Math.floor(i / this.#columnsCount);
                const col = i % this.#columnsCount;

                // Position absolutely
                card.style.position = 'absolute';
                card.style.top = `${row * rowHeight}px`;
                card.style.left = `${col * (this.#cardWidth + this.#gap)}px`;
                card.style.width = `${this.#cardWidth}px`;

                fragment.appendChild(card);
                this.#renderedCards.set(tool.id, card);
            }
        }

        this.#container.appendChild(fragment);
    }

    /**
     * Render empty state
     */
    #renderEmptyState() {
        this.#container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="1.5">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                </div>
                <h2 class="empty-title">No tools found</h2>
                <p class="empty-description">Try adjusting your filters or search terms</p>
                <button class="btn btn-primary" id="reset-filters-btn">Clear Filters</button>
            </div>
        `;

        // Bind reset button
        const resetBtn = this.#container.querySelector('#reset-filters-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.events.emit(EVENTS.FILTERS_RESET);
            });
        }
    }

    /**
     * Clear all rendered cards
     */
    #clearCards() {
        this.#renderedCards.clear();
        this.#container.innerHTML = '';
        this.#container.style.height = '';
        this.#container.classList.remove('virtual-scroll');
    }

    /**
     * Setup scroll listener
     */
    #setupScrollListener() {
        const handleScroll = () => {
            if (!this.#virtualScrollEnabled) return;

            clearTimeout(this.#scrollDebounce);
            this.#scrollDebounce = setTimeout(() => {
                this.#updateVisibleCards();
            }, DEBOUNCE.SCROLL);
        };

        if (this.#scrollContainer === window) {
            window.addEventListener('scroll', handleScroll, { passive: true });
        } else {
            this.#scrollContainer.addEventListener('scroll', handleScroll, { passive: true });
        }
    }

    /**
     * Setup resize observer
     */
    #setupResizeObserver() {
        this.#resizeObserver = new ResizeObserver((entries) => {
            for (const entry of entries) {
                this.#calculateColumns();

                if (this.#virtualScrollEnabled) {
                    this.#updateVisibleCards();
                }
            }
        });

        if (this.#container) {
            this.#resizeObserver.observe(this.#container);
        }
    }

    /**
     * Calculate number of columns based on container width
     */
    #calculateColumns() {
        if (!this.#container) return;

        const containerWidth = this.#container.offsetWidth;
        const minCardWidth = 300;

        this.#columnsCount = Math.max(1, Math.floor((containerWidth + this.#gap) / (minCardWidth + this.#gap)));
        this.#cardWidth = (containerWidth - (this.#columnsCount - 1) * this.#gap) / this.#columnsCount;
    }

    /**
     * Get scroll top position
     * @returns {number}
     */
    #getScrollTop() {
        if (this.#scrollContainer === window) {
            return window.scrollY || document.documentElement.scrollTop;
        }
        return this.#scrollContainer.scrollTop;
    }

    /**
     * Get viewport height
     * @returns {number}
     */
    #getViewportHeight() {
        if (this.#scrollContainer === window) {
            return window.innerHeight;
        }
        return this.#scrollContainer.offsetHeight;
    }

    /**
     * Scroll to a specific tool
     * @param {string} toolId
     */
    scrollToTool(toolId) {
        const index = this.#tools.findIndex(t => t.id === toolId);
        if (index === -1) return;

        const row = Math.floor(index / this.#columnsCount);
        const rowHeight = DEFAULT_CARD_HEIGHT + this.#gap;
        const targetScroll = row * rowHeight;

        if (this.#scrollContainer === window) {
            window.scrollTo({ top: targetScroll, behavior: 'smooth' });
        } else {
            this.#scrollContainer.scrollTo({ top: targetScroll, behavior: 'smooth' });
        }

        // Highlight the card briefly
        setTimeout(() => {
            const card = this.#renderedCards.get(toolId);
            if (card) {
                card.classList.add('highlighted');
                setTimeout(() => card.classList.remove('highlighted'), 2000);
            }
        }, 300);
    }

    /**
     * Focus a specific tool card
     * @param {string} toolId
     */
    focusTool(toolId) {
        this.scrollToTool(toolId);

        setTimeout(() => {
            const card = this.#renderedCards.get(toolId);
            if (card) {
                card.focus();
            }
        }, 500);
    }

    /**
     * Get rendered card element
     * @param {string} toolId
     * @returns {HTMLElement|null}
     */
    getCard(toolId) {
        return this.#renderedCards.get(toolId) || null;
    }

    /**
     * Refresh a specific card
     * @param {string} toolId
     * @param {Object} tool
     */
    refreshCard(toolId, tool) {
        const existingCard = this.#renderedCards.get(toolId);
        if (existingCard) {
            const newCard = createToolCard(tool);
            existingCard.replaceWith(newCard);
            this.#renderedCards.set(toolId, newCard);
        }
    }

    /**
     * Get statistics about rendered cards
     * @returns {Object}
     */
    getStats() {
        return {
            totalTools: this.#tools.length,
            renderedCards: this.#renderedCards.size,
            columnsCount: this.#columnsCount,
            virtualScrollEnabled: this.#virtualScrollEnabled
        };
    }

    /**
     * Destroy the renderer and clean up
     */
    destroy() {
        if (this.#resizeObserver) {
            this.#resizeObserver.disconnect();
        }

        if (this.#intersectionObserver) {
            this.#intersectionObserver.disconnect();
        }

        this.#clearCards();
        this.#container = null;
        this.#scrollContainer = null;
    }
}

export { GridRenderer };
