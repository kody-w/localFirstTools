/**
 * Keyboard Handler - Keyboard shortcuts and navigation
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';

class KeyboardHandler {
    constructor() {
        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();

        this.#shortcuts = new Map();
        this.#enabled = true;
        this.#focusableSelector = 'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])';

        this.#registerDefaultShortcuts();
        this.#bindEvents();
    }

    #shortcuts;
    #enabled;
    #focusableSelector;

    /**
     * Register default keyboard shortcuts
     */
    #registerDefaultShortcuts() {
        // Search
        this.registerShortcut('/', () => {
            const searchInput = document.querySelector('.search-input, #search-input');
            if (searchInput) {
                searchInput.focus();
                return true; // Prevent default
            }
        }, { description: 'Focus search' });

        this.registerShortcut('Escape', () => {
            // Close any open modals or panels
            this.events.emit(EVENTS.MODAL_CLOSE);

            // Blur search input
            const searchInput = document.querySelector('.search-input, #search-input');
            if (document.activeElement === searchInput) {
                searchInput.blur();
            }
        }, { description: 'Close/Cancel' });

        // Navigation shortcuts
        this.registerShortcut('g h', () => {
            this.events.emit(EVENTS.NAVIGATE, { to: 'home' });
        }, { description: 'Go to home' });

        this.registerShortcut('g a', () => {
            this.events.emit(EVENTS.NAVIGATE, { to: 'archive' });
        }, { description: 'Go to archive' });

        this.registerShortcut('g 3', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: '3d' });
        }, { description: 'Go to 3D gallery' });

        // View mode shortcuts
        this.registerShortcut('v g', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'grid' });
        }, { description: 'Grid view' });

        this.registerShortcut('v l', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'list' });
        }, { description: 'List view' });

        this.registerShortcut('v m', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'masonry' });
        }, { description: 'Masonry view' });

        this.registerShortcut('v t', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'timeline' });
        }, { description: 'Timeline view' });

        this.registerShortcut('v d', () => {
            this.events.emit(EVENTS.VIEW_CHANGE, { mode: 'dashboard' });
        }, { description: 'Dashboard view' });

        // Action shortcuts
        this.registerShortcut('?', () => {
            this.events.emit(EVENTS.SHOW_SHORTCUTS);
        }, { shift: true, description: 'Show keyboard shortcuts' });

        this.registerShortcut('t', () => {
            this.events.emit(EVENTS.THEME_TOGGLE);
        }, { description: 'Toggle theme' });

        this.registerShortcut('f', () => {
            this.events.emit(EVENTS.TOGGLE_FILTERS);
        }, { description: 'Toggle filters panel' });

        this.registerShortcut('c', () => {
            this.events.emit(EVENTS.TOGGLE_COLLECTIONS);
        }, { description: 'Toggle collections panel' });

        // Grid navigation with arrow keys
        this.registerShortcut('ArrowUp', () => {
            this.#navigateGrid('up');
        }, { description: 'Navigate up' });

        this.registerShortcut('ArrowDown', () => {
            this.#navigateGrid('down');
        }, { description: 'Navigate down' });

        this.registerShortcut('ArrowLeft', () => {
            this.#navigateGrid('left');
        }, { description: 'Navigate left' });

        this.registerShortcut('ArrowRight', () => {
            this.#navigateGrid('right');
        }, { description: 'Navigate right' });

        // Quick actions on focused item
        this.registerShortcut('p', () => {
            this.#performActionOnFocused('pin');
        }, { description: 'Pin/unpin focused tool' });

        this.registerShortcut('Enter', () => {
            this.#performActionOnFocused('open');
        }, { description: 'Open focused tool' });

        this.registerShortcut('o', () => {
            this.#performActionOnFocused('preview');
        }, { description: 'Preview focused tool' });
    }

    /**
     * Bind keyboard event listeners
     */
    #bindEvents() {
        this.#pendingKeys = [];
        this.#keyTimeout = null;

        document.addEventListener('keydown', (e) => this.#handleKeyDown(e));
    }

    #pendingKeys;
    #keyTimeout;

    /**
     * Handle keydown event
     * @param {KeyboardEvent} e
     */
    #handleKeyDown(e) {
        if (!this.#enabled) return;

        // Ignore if typing in an input
        if (this.#isTyping(e)) return;

        // Build key string
        const keyString = this.#buildKeyString(e);

        // Check for multi-key shortcuts (e.g., "g h")
        this.#pendingKeys.push(keyString);

        // Clear timeout
        if (this.#keyTimeout) {
            clearTimeout(this.#keyTimeout);
        }

        // Try to match shortcut
        const combo = this.#pendingKeys.join(' ');
        const shortcut = this.#shortcuts.get(combo);

        if (shortcut) {
            e.preventDefault();
            shortcut.handler(e);
            this.#pendingKeys = [];
            this.events.emit(EVENTS.KEYBOARD_INPUT, { key: combo });
            return;
        }

        // Check if this could be start of a multi-key combo
        const couldBeMultiKey = Array.from(this.#shortcuts.keys()).some(k => k.startsWith(combo + ' '));

        if (couldBeMultiKey) {
            // Wait for more keys
            this.#keyTimeout = setTimeout(() => {
                this.#pendingKeys = [];
            }, 500);
        } else {
            // No match, check single key
            const singleShortcut = this.#shortcuts.get(keyString);
            if (singleShortcut) {
                e.preventDefault();
                singleShortcut.handler(e);
                this.events.emit(EVENTS.KEYBOARD_INPUT, { key: keyString });
            }
            this.#pendingKeys = [];
        }
    }

    /**
     * Check if user is typing in an input
     * @param {KeyboardEvent} e
     * @returns {boolean}
     */
    #isTyping(e) {
        const target = e.target;
        const tagName = target.tagName.toLowerCase();

        if (tagName === 'input' || tagName === 'textarea' || tagName === 'select') {
            return true;
        }

        if (target.isContentEditable) {
            return true;
        }

        return false;
    }

    /**
     * Build key string from event
     * @param {KeyboardEvent} e
     * @returns {string}
     */
    #buildKeyString(e) {
        const parts = [];

        if (e.ctrlKey || e.metaKey) parts.push('Ctrl');
        if (e.altKey) parts.push('Alt');
        if (e.shiftKey && e.key.length > 1) parts.push('Shift');

        // Normalize key
        let key = e.key;
        if (key === ' ') key = 'Space';
        if (key.length === 1) key = key.toLowerCase();

        parts.push(key);

        return parts.join('+');
    }

    /**
     * Navigate in grid
     * @param {string} direction
     */
    #navigateGrid(direction) {
        const grid = document.querySelector('.tool-grid, .grid-view, .main-view-container');
        if (!grid) return;

        const cards = Array.from(grid.querySelectorAll('.tool-card'));
        if (cards.length === 0) return;

        const focused = document.activeElement;
        const currentIndex = cards.indexOf(focused);

        // Calculate columns based on grid
        const gridStyle = window.getComputedStyle(grid);
        const columns = gridStyle.gridTemplateColumns?.split(' ').length || 4;

        let nextIndex = -1;

        switch (direction) {
            case 'up':
                nextIndex = currentIndex >= columns ? currentIndex - columns : currentIndex;
                break;
            case 'down':
                nextIndex = currentIndex + columns < cards.length ? currentIndex + columns : currentIndex;
                break;
            case 'left':
                nextIndex = currentIndex > 0 ? currentIndex - 1 : currentIndex;
                break;
            case 'right':
                nextIndex = currentIndex < cards.length - 1 ? currentIndex + 1 : currentIndex;
                break;
        }

        if (nextIndex >= 0 && nextIndex < cards.length) {
            cards[nextIndex].focus();
        } else if (currentIndex === -1 && cards.length > 0) {
            // No card focused, focus first one
            cards[0].focus();
        }
    }

    /**
     * Perform action on focused tool
     * @param {string} action
     */
    #performActionOnFocused(action) {
        const focused = document.activeElement;

        if (!focused?.classList.contains('tool-card')) return;

        const toolId = focused.dataset.toolId;
        if (!toolId) return;

        switch (action) {
            case 'pin':
                this.events.emit(EVENTS.TOOL_PIN_TOGGLE, { toolId });
                break;
            case 'open':
                this.events.emit(EVENTS.TOOL_OPEN, { toolId });
                break;
            case 'preview':
                this.events.emit(EVENTS.TOOL_PREVIEW, { toolId });
                break;
        }
    }

    /**
     * Register a keyboard shortcut
     * @param {string} key - Key or key combo (e.g., "g h", "Ctrl+s")
     * @param {Function} handler
     * @param {Object} options
     */
    registerShortcut(key, handler, options = {}) {
        this.#shortcuts.set(key, {
            handler,
            description: options.description || '',
            category: options.category || 'general'
        });
    }

    /**
     * Unregister a keyboard shortcut
     * @param {string} key
     */
    unregisterShortcut(key) {
        this.#shortcuts.delete(key);
    }

    /**
     * Get all registered shortcuts
     * @returns {Map}
     */
    getShortcuts() {
        return new Map(this.#shortcuts);
    }

    /**
     * Enable/disable keyboard handler
     * @param {boolean} enabled
     */
    setEnabled(enabled) {
        this.#enabled = enabled;
    }

    /**
     * Check if enabled
     * @returns {boolean}
     */
    isEnabled() {
        return this.#enabled;
    }

    /**
     * Destroy handler
     */
    destroy() {
        this.#shortcuts.clear();
        this.#enabled = false;
    }
}

export { KeyboardHandler };
