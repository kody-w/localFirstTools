/**
 * Event Bus - Application-wide event system
 * Local First Tools v2
 */

/**
 * Event types for the application
 */
export const EVENTS = {
    // Data events
    DATA_LOADED: 'data:loaded',
    DATA_ERROR: 'data:error',
    DATA_REFRESH: 'data:refresh',

    // Filter events
    FILTERS_CHANGED: 'filters:changed',
    FILTERS_RESET: 'filters:reset',
    FILTER_ADDED: 'filter:added',
    FILTER_REMOVED: 'filter:removed',

    // Search events
    SEARCH_QUERY: 'search:query',
    SEARCH_COMPLETE: 'search:complete',
    SEARCH_CLEAR: 'search:clear',
    SEARCH_SUGGESTION_SELECT: 'search:suggestion:select',

    // View events
    VIEW_CHANGE: 'view:change',
    VIEW_RENDERED: 'view:rendered',
    VIEW_SCROLL: 'view:scroll',

    // Tool events
    TOOL_OPEN: 'tool:open',
    TOOL_PREVIEW: 'tool:preview',
    TOOL_PREVIEW_CLOSE: 'tool:preview:close',
    TOOL_PIN: 'tool:pin',
    TOOL_UNPIN: 'tool:unpin',
    TOOL_VOTE: 'tool:vote',
    TOOL_FOCUS: 'tool:focus',
    TOOL_BLUR: 'tool:blur',

    // Collection events
    COLLECTION_CREATE: 'collection:create',
    COLLECTION_DELETE: 'collection:delete',
    COLLECTION_ADD_TOOL: 'collection:add:tool',
    COLLECTION_REMOVE_TOOL: 'collection:remove:tool',

    // UI events
    MODAL_OPEN: 'modal:open',
    MODAL_CLOSE: 'modal:close',
    SIDEBAR_TOGGLE: 'sidebar:toggle',
    NOTIFICATION_SHOW: 'notification:show',
    NOTIFICATION_HIDE: 'notification:hide',

    // Theme events
    THEME_CHANGE: 'theme:change',

    // Input events
    KEYBOARD_SHORTCUT: 'input:keyboard',
    GAMEPAD_BUTTON: 'input:gamepad:button',
    GAMEPAD_AXIS: 'input:gamepad:axis',
    GAMEPAD_CONNECTED: 'input:gamepad:connected',
    GAMEPAD_DISCONNECTED: 'input:gamepad:disconnected',
    TOUCH_GESTURE: 'input:touch:gesture',

    // Analytics events
    ANALYTICS_TRACK: 'analytics:track',
    ANALYTICS_EXPORT: 'analytics:export',

    // 3D Gallery events
    GALLERY_3D_ENTER: 'gallery3d:enter',
    GALLERY_3D_EXIT: 'gallery3d:exit',
    GALLERY_3D_TOOL_HOVER: 'gallery3d:tool:hover',
    GALLERY_3D_TOOL_SELECT: 'gallery3d:tool:select',

    // Tour events
    TOUR_START: 'tour:start',
    TOUR_STEP: 'tour:step',
    TOUR_COMPLETE: 'tour:complete',
    TOUR_SKIP: 'tour:skip',

    // Comparison events
    COMPARISON_ADD: 'comparison:add',
    COMPARISON_REMOVE: 'comparison:remove',
    COMPARISON_CLEAR: 'comparison:clear',
    COMPARISON_OPEN: 'comparison:open'
};

class EventBus {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {EventBus}
     */
    static getInstance() {
        if (!EventBus.#instance) {
            EventBus.#instance = new EventBus();
        }
        return EventBus.#instance;
    }

    constructor() {
        if (EventBus.#instance) {
            throw new Error('Use EventBus.getInstance() instead of new EventBus()');
        }

        /** @type {Map<string, Set<Function>>} */
        this.#listeners = new Map();

        /** @type {Map<string, Set<Function>>} */
        this.#onceListeners = new Map();

        /** @type {Array<{event: string, data: any, timestamp: number}>} */
        this.#history = [];

        /** @type {number} */
        this.#maxHistorySize = 100;

        /** @type {boolean} */
        this.#debug = false;
    }

    #listeners;
    #onceListeners;
    #history;
    #maxHistorySize;
    #debug;

    /**
     * Enable/disable debug mode
     * @param {boolean} enabled
     */
    setDebug(enabled) {
        this.#debug = enabled;
    }

    /**
     * Subscribe to an event
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     * @returns {Function} Unsubscribe function
     */
    on(event, callback) {
        if (!this.#listeners.has(event)) {
            this.#listeners.set(event, new Set());
        }
        this.#listeners.get(event).add(callback);

        // Return unsubscribe function
        return () => this.off(event, callback);
    }

    /**
     * Subscribe to an event (fires only once)
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     * @returns {Function} Unsubscribe function
     */
    once(event, callback) {
        if (!this.#onceListeners.has(event)) {
            this.#onceListeners.set(event, new Set());
        }
        this.#onceListeners.get(event).add(callback);

        return () => {
            const listeners = this.#onceListeners.get(event);
            if (listeners) {
                listeners.delete(callback);
            }
        };
    }

    /**
     * Unsubscribe from an event
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    off(event, callback) {
        const listeners = this.#listeners.get(event);
        if (listeners) {
            listeners.delete(callback);
            if (listeners.size === 0) {
                this.#listeners.delete(event);
            }
        }
    }

    /**
     * Emit an event
     * @param {string} event - Event name
     * @param {any} data - Event data
     */
    emit(event, data = null) {
        if (this.#debug) {
            console.log(`[EventBus] ${event}`, data);
        }

        // Store in history
        this.#history.push({
            event,
            data,
            timestamp: Date.now()
        });

        // Trim history if needed
        if (this.#history.length > this.#maxHistorySize) {
            this.#history.shift();
        }

        // Notify regular listeners
        const listeners = this.#listeners.get(event);
        if (listeners) {
            for (const callback of listeners) {
                try {
                    callback(data, event);
                } catch (error) {
                    console.error(`[EventBus] Error in listener for "${event}":`, error);
                }
            }
        }

        // Notify once listeners
        const onceListeners = this.#onceListeners.get(event);
        if (onceListeners) {
            for (const callback of onceListeners) {
                try {
                    callback(data, event);
                } catch (error) {
                    console.error(`[EventBus] Error in once listener for "${event}":`, error);
                }
            }
            this.#onceListeners.delete(event);
        }

        // Also notify wildcard listeners
        const wildcardListeners = this.#listeners.get('*');
        if (wildcardListeners) {
            for (const callback of wildcardListeners) {
                try {
                    callback(data, event);
                } catch (error) {
                    console.error(`[EventBus] Error in wildcard listener:`, error);
                }
            }
        }
    }

    /**
     * Emit an event asynchronously (next tick)
     * @param {string} event - Event name
     * @param {any} data - Event data
     * @returns {Promise<void>}
     */
    async emitAsync(event, data = null) {
        return new Promise(resolve => {
            queueMicrotask(() => {
                this.emit(event, data);
                resolve();
            });
        });
    }

    /**
     * Wait for an event to occur
     * @param {string} event - Event name
     * @param {number} timeout - Timeout in ms (0 = no timeout)
     * @returns {Promise<any>}
     */
    waitFor(event, timeout = 0) {
        return new Promise((resolve, reject) => {
            let timeoutId;

            const unsubscribe = this.once(event, (data) => {
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                resolve(data);
            });

            if (timeout > 0) {
                timeoutId = setTimeout(() => {
                    unsubscribe();
                    reject(new Error(`Timeout waiting for event "${event}"`));
                }, timeout);
            }
        });
    }

    /**
     * Check if there are any listeners for an event
     * @param {string} event - Event name
     * @returns {boolean}
     */
    hasListeners(event) {
        const regular = this.#listeners.get(event)?.size || 0;
        const once = this.#onceListeners.get(event)?.size || 0;
        return regular + once > 0;
    }

    /**
     * Get number of listeners for an event
     * @param {string} event - Event name
     * @returns {number}
     */
    listenerCount(event) {
        const regular = this.#listeners.get(event)?.size || 0;
        const once = this.#onceListeners.get(event)?.size || 0;
        return regular + once;
    }

    /**
     * Get all event names that have listeners
     * @returns {string[]}
     */
    eventNames() {
        const names = new Set([
            ...this.#listeners.keys(),
            ...this.#onceListeners.keys()
        ]);
        return Array.from(names);
    }

    /**
     * Get event history
     * @param {number} limit - Number of events to return
     * @returns {Array}
     */
    getHistory(limit = 10) {
        return this.#history.slice(-limit);
    }

    /**
     * Clear event history
     */
    clearHistory() {
        this.#history = [];
    }

    /**
     * Remove all listeners
     */
    removeAllListeners() {
        this.#listeners.clear();
        this.#onceListeners.clear();
    }

    /**
     * Remove all listeners for a specific event
     * @param {string} event - Event name
     */
    removeAllListenersFor(event) {
        this.#listeners.delete(event);
        this.#onceListeners.delete(event);
    }
}

export { EventBus, EVENTS };
