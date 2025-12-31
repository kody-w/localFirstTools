/**
 * Main View - Default grid gallery view
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { GridRenderer } from '../renderers/grid-renderer.js';
import { SectionRenderer } from '../renderers/section-renderer.js';
import { Skeleton } from '../renderers/skeleton-loader.js';

class MainView {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.gridRenderer = GridRenderer.getInstance();
        this.sectionRenderer = SectionRenderer.getInstance();

        this.#container = null;
        this.#options = {
            useSections: false,
            showPinnedSection: true,
            showFeaturedSection: true,
            groupByCategory: false
        };
    }

    #container;
    #options;

    /**
     * Initialize the main view
     * @param {HTMLElement} container
     * @param {Object} options
     */
    initialize(container, options = {}) {
        this.#container = container;
        this.#options = { ...this.#options, ...options };

        // Show loading skeleton
        Skeleton.showGrid(container, 6);

        // Initialize appropriate renderer
        if (this.#options.useSections) {
            this.sectionRenderer.initialize(container);
        } else {
            this.gridRenderer.initialize(container);
        }
    }

    /**
     * Render tools
     * @param {Array} tools
     * @param {boolean} animate
     */
    render(tools, animate = true) {
        if (!this.#container) return;

        if (this.#options.useSections) {
            this.sectionRenderer.render(tools, {
                showPinnedSection: this.#options.showPinnedSection,
                showFeaturedSection: this.#options.showFeaturedSection,
                groupByCategory: this.#options.groupByCategory
            });
        } else {
            this.gridRenderer.render(tools, animate);
        }
    }

    /**
     * Switch between grid and section modes
     * @param {boolean} useSections
     */
    setUseSections(useSections) {
        this.#options.useSections = useSections;

        // Re-initialize with current tools
        const tools = this.state.getSlice('filteredTools');
        this.render(tools, false);
    }

    /**
     * Toggle category grouping
     * @param {boolean} groupByCategory
     */
    setGroupByCategory(groupByCategory) {
        this.#options.groupByCategory = groupByCategory;

        if (this.#options.useSections) {
            const tools = this.state.getSlice('filteredTools');
            this.sectionRenderer.render(tools, {
                ...this.#options,
                groupByCategory
            });
        }
    }

    /**
     * Scroll to a tool
     * @param {string} toolId
     */
    scrollToTool(toolId) {
        this.gridRenderer.scrollToTool(toolId);
    }

    /**
     * Focus a tool
     * @param {string} toolId
     */
    focusTool(toolId) {
        this.gridRenderer.focusTool(toolId);
    }

    /**
     * Get current options
     * @returns {Object}
     */
    getOptions() {
        return { ...this.#options };
    }

    /**
     * Destroy the view
     */
    destroy() {
        this.gridRenderer.destroy();
        this.sectionRenderer.destroy();
        this.#container = null;
    }
}

export { MainView };
