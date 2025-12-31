/**
 * View Manager - Coordinates between different view modes
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { StorageManager } from '../storage/storage-manager.js';
import { VIEW_MODES, STORAGE_KEYS } from '../core/constants.js';

/**
 * @typedef {Object} ViewConfig
 * @property {string} key - View mode key
 * @property {string} label - Display label
 * @property {string} icon - Icon identifier
 * @property {Function} renderer - View renderer class/function
 */

class ViewManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {ViewManager}
     */
    static getInstance() {
        if (!ViewManager.#instance) {
            ViewManager.#instance = new ViewManager();
        }
        return ViewManager.#instance;
    }

    constructor() {
        if (ViewManager.#instance) {
            throw new Error('Use ViewManager.getInstance() instead of new ViewManager()');
        }

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();

        this.#container = null;
        this.#currentView = null;
        this.#currentMode = 'grid';
        this.#views = new Map();
        this.#initialized = false;
    }

    #container;
    #currentView;
    #currentMode;
    #views;
    #initialized;

    /**
     * Initialize the view manager
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;

        // Restore saved view mode
        const savedMode = this.storage.get(STORAGE_KEYS.VIEW_MODE);
        if (savedMode && VIEW_MODES[savedMode]) {
            this.#currentMode = savedMode;
        }

        // Set initial view state
        const view = this.state.getSlice('view');
        this.state.setSlice('view', { ...view, mode: this.#currentMode });

        // Listen for view change requests
        this.events.on(EVENTS.VIEW_CHANGE, ({ mode }) => {
            this.switchTo(mode);
        });

        this.#initialized = true;
    }

    /**
     * Register a view renderer
     * @param {string} mode - View mode key
     * @param {Object} view - View instance with render() method
     */
    register(mode, view) {
        this.#views.set(mode, view);
    }

    /**
     * Switch to a different view mode
     * @param {string} mode
     * @returns {boolean} Success
     */
    switchTo(mode) {
        if (!VIEW_MODES[mode]) {
            console.warn(`Unknown view mode: ${mode}`);
            return false;
        }

        if (mode === this.#currentMode) {
            return true;
        }

        // Cleanup current view
        if (this.#currentView && typeof this.#currentView.destroy === 'function') {
            this.#currentView.destroy();
        }

        // Get new view
        const view = this.#views.get(mode);

        if (!view) {
            console.warn(`View not registered: ${mode}`);
            return false;
        }

        this.#currentMode = mode;
        this.#currentView = view;

        // Update state
        const viewState = this.state.getSlice('view');
        this.state.setSlice('view', { ...viewState, mode });

        // Save preference
        this.storage.set(STORAGE_KEYS.VIEW_MODE, mode);

        // Initialize and render the view
        if (typeof view.initialize === 'function') {
            view.initialize(this.#container);
        }

        const tools = this.state.getSlice('filteredTools');
        if (typeof view.render === 'function') {
            view.render(tools);
        }

        this.events.emit(EVENTS.VIEW_RENDERED, { mode });

        return true;
    }

    /**
     * Get current view mode
     * @returns {string}
     */
    getCurrentMode() {
        return this.#currentMode;
    }

    /**
     * Get current view instance
     * @returns {Object|null}
     */
    getCurrentView() {
        return this.#currentView;
    }

    /**
     * Get available view modes
     * @returns {Array<{key: string, label: string, icon: string}>}
     */
    getAvailableModes() {
        return Object.values(VIEW_MODES).map(mode => ({
            ...mode,
            active: mode.key === this.#currentMode,
            available: this.#views.has(mode.key)
        }));
    }

    /**
     * Cycle to next view mode
     */
    cycleNext() {
        const modes = Object.keys(VIEW_MODES);
        const currentIndex = modes.indexOf(this.#currentMode);
        const nextIndex = (currentIndex + 1) % modes.length;
        this.switchTo(modes[nextIndex]);
    }

    /**
     * Cycle to previous view mode
     */
    cyclePrevious() {
        const modes = Object.keys(VIEW_MODES);
        const currentIndex = modes.indexOf(this.#currentMode);
        const prevIndex = (currentIndex - 1 + modes.length) % modes.length;
        this.switchTo(modes[prevIndex]);
    }

    /**
     * Refresh current view
     */
    refresh() {
        const tools = this.state.getSlice('filteredTools');

        if (this.#currentView && typeof this.#currentView.render === 'function') {
            this.#currentView.render(tools);
        }
    }

    /**
     * Get view mode configuration
     * @param {string} mode
     * @returns {Object|null}
     */
    getModeConfig(mode) {
        return VIEW_MODES[mode] || null;
    }

    /**
     * Check if a mode is available
     * @param {string} mode
     * @returns {boolean}
     */
    isModeAvailable(mode) {
        return this.#views.has(mode);
    }

    /**
     * Destroy the view manager
     */
    destroy() {
        if (this.#currentView && typeof this.#currentView.destroy === 'function') {
            this.#currentView.destroy();
        }

        this.#views.clear();
        this.#container = null;
        this.#currentView = null;
        this.#initialized = false;
    }
}

export { ViewManager };
