/**
 * Input Manager - Unified input coordination
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';
import { KeyboardHandler } from './keyboard-handler.js';
import { GamepadHandler } from './gamepad-handler.js';
import { TouchHandler } from './touch-handler.js';

class InputManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {InputManager}
     */
    static getInstance() {
        if (!InputManager.#instance) {
            InputManager.#instance = new InputManager();
        }
        return InputManager.#instance;
    }

    constructor() {
        if (InputManager.#instance) {
            return InputManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();

        this.keyboard = null;
        this.gamepad = null;
        this.touch = null;

        this.#activeInput = 'keyboard';
        this.#isInitialized = false;
    }

    #activeInput;
    #isInitialized;

    /**
     * Initialize all input handlers
     * @param {HTMLElement} container
     */
    initialize(container) {
        if (this.#isInitialized) return;

        // Initialize handlers
        this.keyboard = new KeyboardHandler();
        this.gamepad = new GamepadHandler();
        this.touch = new TouchHandler(container);

        // Setup cross-handler events
        this.#setupInputEvents();

        // Detect preferred input method
        this.#detectInputMethod();

        this.#isInitialized = true;
    }

    /**
     * Setup input event listeners
     */
    #setupInputEvents() {
        // Track last input method used
        this.events.on(EVENTS.KEYBOARD_INPUT, () => {
            this.#setActiveInput('keyboard');
        });

        this.events.on(EVENTS.GAMEPAD_CONNECTED, () => {
            this.#setActiveInput('gamepad');
        });

        this.events.on('touch:start', () => {
            this.#setActiveInput('touch');
        });

        // Unified navigation events
        this.#setupUnifiedNavigation();
    }

    /**
     * Setup unified navigation across input types
     */
    #setupUnifiedNavigation() {
        // Map various input methods to unified navigation events
        const navigationMap = {
            'ArrowUp': 'navigate:up',
            'ArrowDown': 'navigate:down',
            'ArrowLeft': 'navigate:left',
            'ArrowRight': 'navigate:right',
            'Enter': 'navigate:select',
            'Escape': 'navigate:back',
            'Tab': 'navigate:next'
        };

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            const navEvent = navigationMap[e.key];
            if (navEvent) {
                this.events.emit(navEvent, { source: 'keyboard', event: e });
            }
        });

        // Gamepad navigation is handled by GamepadHandler polling
    }

    /**
     * Detect initial input method
     */
    #detectInputMethod() {
        // Check for touch support
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            // Mobile device, but could still have keyboard
            if (window.matchMedia('(hover: none)').matches) {
                this.#setActiveInput('touch');
            }
        }

        // Check for connected gamepads
        const gamepads = navigator.getGamepads();
        for (const gp of gamepads) {
            if (gp) {
                this.#setActiveInput('gamepad');
                break;
            }
        }
    }

    /**
     * Set active input method
     * @param {string} method
     */
    #setActiveInput(method) {
        if (this.#activeInput !== method) {
            this.#activeInput = method;
            this.events.emit(EVENTS.INPUT_METHOD_CHANGE, { method });

            // Update body class for CSS targeting
            document.body.setAttribute('data-input', method);
        }
    }

    /**
     * Get active input method
     * @returns {string}
     */
    getActiveInput() {
        return this.#activeInput;
    }

    /**
     * Check if gamepad is connected
     * @returns {boolean}
     */
    isGamepadConnected() {
        return this.gamepad?.isConnected() || false;
    }

    /**
     * Check if touch is supported
     * @returns {boolean}
     */
    isTouchSupported() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }

    /**
     * Enable/disable keyboard shortcuts
     * @param {boolean} enabled
     */
    setKeyboardEnabled(enabled) {
        this.keyboard?.setEnabled(enabled);
    }

    /**
     * Register a custom keyboard shortcut
     * @param {string} key
     * @param {Function} handler
     * @param {Object} options
     */
    registerShortcut(key, handler, options = {}) {
        this.keyboard?.registerShortcut(key, handler, options);
    }

    /**
     * Unregister a keyboard shortcut
     * @param {string} key
     */
    unregisterShortcut(key) {
        this.keyboard?.unregisterShortcut(key);
    }

    /**
     * Get all registered shortcuts
     * @returns {Map}
     */
    getShortcuts() {
        return this.keyboard?.getShortcuts() || new Map();
    }

    /**
     * Vibrate gamepad (if supported)
     * @param {number} duration
     * @param {number} intensity
     */
    vibrateGamepad(duration = 100, intensity = 0.5) {
        this.gamepad?.vibrate(duration, intensity);
    }

    /**
     * Destroy all input handlers
     */
    destroy() {
        this.keyboard?.destroy();
        this.gamepad?.destroy();
        this.touch?.destroy();

        this.keyboard = null;
        this.gamepad = null;
        this.touch = null;
        this.#isInitialized = false;
    }
}

export { InputManager };
