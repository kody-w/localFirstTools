/**
 * Announcer - Screen reader live regions
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';

class Announcer {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {Announcer}
     */
    static getInstance() {
        if (!Announcer.#instance) {
            Announcer.#instance = new Announcer();
        }
        return Announcer.#instance;
    }

    constructor() {
        if (Announcer.#instance) {
            return Announcer.#instance;
        }

        this.events = EventBus.getInstance();
        this.#politeRegion = null;
        this.#assertiveRegion = null;
        this.#statusRegion = null;

        this.#initialize();
    }

    #politeRegion;
    #assertiveRegion;
    #statusRegion;

    /**
     * Initialize announcer regions
     */
    #initialize() {
        this.#createRegions();
        this.#bindEvents();
    }

    /**
     * Create live regions
     */
    #createRegions() {
        // Polite region - for non-critical updates
        this.#politeRegion = document.createElement('div');
        this.#politeRegion.className = 'sr-only';
        this.#politeRegion.setAttribute('role', 'status');
        this.#politeRegion.setAttribute('aria-live', 'polite');
        this.#politeRegion.setAttribute('aria-atomic', 'true');
        this.#politeRegion.id = 'announcer-polite';

        // Assertive region - for critical updates
        this.#assertiveRegion = document.createElement('div');
        this.#assertiveRegion.className = 'sr-only';
        this.#assertiveRegion.setAttribute('role', 'alert');
        this.#assertiveRegion.setAttribute('aria-live', 'assertive');
        this.#assertiveRegion.setAttribute('aria-atomic', 'true');
        this.#assertiveRegion.id = 'announcer-assertive';

        // Status region - for ongoing status
        this.#statusRegion = document.createElement('div');
        this.#statusRegion.className = 'sr-only';
        this.#statusRegion.setAttribute('role', 'status');
        this.#statusRegion.setAttribute('aria-live', 'polite');
        this.#statusRegion.id = 'announcer-status';

        // Add to DOM
        document.body.appendChild(this.#politeRegion);
        document.body.appendChild(this.#assertiveRegion);
        document.body.appendChild(this.#statusRegion);
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Announce notifications
        this.events.on(EVENTS.NOTIFICATION, ({ message, type }) => {
            if (type === 'error') {
                this.assertive(message);
            } else {
                this.polite(message);
            }
        });

        // Announce search results
        this.events.on(EVENTS.SEARCH_RESULTS, ({ count }) => {
            this.polite(`${count} tool${count !== 1 ? 's' : ''} found`);
        });

        // Announce filter changes
        this.events.on(EVENTS.FILTER_APPLIED, ({ count }) => {
            this.polite(`Filter applied. Showing ${count} tool${count !== 1 ? 's' : ''}`);
        });

        // Announce view changes
        this.events.on(EVENTS.VIEW_CHANGE, ({ mode }) => {
            this.polite(`View changed to ${mode}`);
        });

        // Announce pin actions
        this.events.on(EVENTS.TOOL_PIN, ({ tool, pinned }) => {
            const action = pinned ? 'pinned' : 'unpinned';
            this.polite(`${tool?.title || 'Tool'} ${action}`);
        });

        // Announce theme changes
        this.events.on(EVENTS.THEME_CHANGE, ({ theme }) => {
            this.polite(`Theme changed to ${theme}`);
        });

        // Announce loading states
        this.events.on(EVENTS.LOADING_START, () => {
            this.status('Loading...');
        });

        this.events.on(EVENTS.LOADING_END, () => {
            this.clearStatus();
        });

        // Announce modal states
        this.events.on(EVENTS.MODAL_OPEN, ({ type }) => {
            if (type) {
                this.polite(`${type} dialog opened`);
            }
        });

        this.events.on(EVENTS.MODAL_CLOSE, () => {
            this.polite('Dialog closed');
        });

        // Announce navigation
        this.events.on(EVENTS.NAVIGATE, ({ to }) => {
            this.polite(`Navigated to ${to}`);
        });

        // Announce collection changes
        this.events.on(EVENTS.TOOL_ADDED_TO_COLLECTION, ({ collection }) => {
            this.polite(`Added to ${collection?.name || 'collection'}`);
        });

        this.events.on(EVENTS.TOOL_REMOVED_FROM_COLLECTION, ({ collection }) => {
            this.polite(`Removed from ${collection?.name || 'collection'}`);
        });
    }

    /**
     * Make polite announcement (waits for pause in speech)
     * @param {string} message
     */
    polite(message) {
        this.#announce(this.#politeRegion, message);
    }

    /**
     * Make assertive announcement (interrupts current speech)
     * @param {string} message
     */
    assertive(message) {
        this.#announce(this.#assertiveRegion, message);
    }

    /**
     * Set ongoing status
     * @param {string} message
     */
    status(message) {
        this.#statusRegion.textContent = message;
    }

    /**
     * Clear status
     */
    clearStatus() {
        this.#statusRegion.textContent = '';
    }

    /**
     * Internal announce method
     * @param {HTMLElement} region
     * @param {string} message
     */
    #announce(region, message) {
        // Clear first to ensure re-announcement
        region.textContent = '';

        // Use requestAnimationFrame to ensure the clear is processed
        requestAnimationFrame(() => {
            region.textContent = message;

            // Clear after announcement (for next announcement)
            setTimeout(() => {
                region.textContent = '';
            }, 1000);
        });
    }

    /**
     * Announce list of items
     * @param {Array} items
     * @param {string} prefix
     */
    announceList(items, prefix = '') {
        if (items.length === 0) {
            this.polite(`${prefix}No items`);
        } else if (items.length <= 3) {
            this.polite(`${prefix}${items.join(', ')}`);
        } else {
            this.polite(`${prefix}${items.length} items. First: ${items[0]}`);
        }
    }

    /**
     * Announce progress
     * @param {number} current
     * @param {number} total
     * @param {string} label
     */
    announceProgress(current, total, label = 'Progress') {
        const percentage = Math.round((current / total) * 100);
        this.polite(`${label}: ${percentage}%`);
    }

    /**
     * Announce error
     * @param {string} error
     */
    announceError(error) {
        this.assertive(`Error: ${error}`);
    }

    /**
     * Announce success
     * @param {string} message
     */
    announceSuccess(message) {
        this.polite(`Success: ${message}`);
    }

    /**
     * Announce navigation position
     * @param {number} current
     * @param {number} total
     * @param {string} itemName
     */
    announcePosition(current, total, itemName = 'Item') {
        this.polite(`${itemName} ${current} of ${total}`);
    }
}

export { Announcer };
