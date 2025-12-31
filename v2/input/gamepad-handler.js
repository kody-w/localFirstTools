/**
 * Gamepad Handler - Xbox controller support
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';

// Xbox controller button mapping
const BUTTONS = {
    A: 0,
    B: 1,
    X: 2,
    Y: 3,
    LB: 4,
    RB: 5,
    LT: 6,
    RT: 7,
    BACK: 8,
    START: 9,
    L3: 10,
    R3: 11,
    DPAD_UP: 12,
    DPAD_DOWN: 13,
    DPAD_LEFT: 14,
    DPAD_RIGHT: 15,
    XBOX: 16
};

// Axis indices
const AXES = {
    LEFT_X: 0,
    LEFT_Y: 1,
    RIGHT_X: 2,
    RIGHT_Y: 3
};

class GamepadHandler {
    constructor() {
        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();

        this.#gamepadIndex = null;
        this.#isPolling = false;
        this.#pollId = null;
        this.#deadzone = 0.15;
        this.#buttonStates = {};
        this.#lastNavigateTime = 0;
        this.#navigateCooldown = 200; // ms between navigation events

        this.#bindEvents();
    }

    #gamepadIndex;
    #isPolling;
    #pollId;
    #deadzone;
    #buttonStates;
    #lastNavigateTime;
    #navigateCooldown;

    /**
     * Bind gamepad events
     */
    #bindEvents() {
        window.addEventListener('gamepadconnected', (e) => {
            this.#onGamepadConnected(e);
        });

        window.addEventListener('gamepaddisconnected', (e) => {
            this.#onGamepadDisconnected(e);
        });

        // Check for already connected gamepads
        const gamepads = navigator.getGamepads();
        for (const gp of gamepads) {
            if (gp) {
                this.#onGamepadConnected({ gamepad: gp });
                break;
            }
        }
    }

    /**
     * Handle gamepad connection
     * @param {GamepadEvent} e
     */
    #onGamepadConnected(e) {
        const gamepad = e.gamepad;

        // Prefer Xbox controllers
        if (gamepad.id.toLowerCase().includes('xbox') || this.#gamepadIndex === null) {
            this.#gamepadIndex = gamepad.index;
            this.#startPolling();

            this.events.emit(EVENTS.GAMEPAD_CONNECTED, {
                gamepad,
                name: this.#getControllerName(gamepad)
            });

            // Show notification
            this.events.emit(EVENTS.NOTIFICATION, {
                message: `Controller connected: ${this.#getControllerName(gamepad)}`,
                type: 'success'
            });
        }
    }

    /**
     * Handle gamepad disconnection
     * @param {GamepadEvent} e
     */
    #onGamepadDisconnected(e) {
        if (e.gamepad.index === this.#gamepadIndex) {
            this.#stopPolling();
            this.#gamepadIndex = null;
            this.#buttonStates = {};

            this.events.emit(EVENTS.GAMEPAD_DISCONNECTED);

            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Controller disconnected',
                type: 'info'
            });
        }
    }

    /**
     * Get friendly controller name
     * @param {Gamepad} gamepad
     * @returns {string}
     */
    #getControllerName(gamepad) {
        const id = gamepad.id.toLowerCase();

        if (id.includes('xbox')) return 'Xbox Controller';
        if (id.includes('playstation') || id.includes('dualshock') || id.includes('dualsense')) return 'PlayStation Controller';
        if (id.includes('nintendo') || id.includes('switch')) return 'Nintendo Controller';

        return 'Game Controller';
    }

    /**
     * Start polling gamepad state
     */
    #startPolling() {
        if (this.#isPolling) return;

        this.#isPolling = true;
        this.#poll();
    }

    /**
     * Stop polling
     */
    #stopPolling() {
        this.#isPolling = false;

        if (this.#pollId) {
            cancelAnimationFrame(this.#pollId);
            this.#pollId = null;
        }
    }

    /**
     * Poll gamepad state
     */
    #poll() {
        if (!this.#isPolling) return;

        this.#pollId = requestAnimationFrame(() => this.#poll());

        if (this.#gamepadIndex === null) return;

        const gamepads = navigator.getGamepads();
        const gamepad = gamepads[this.#gamepadIndex];

        if (!gamepad) return;

        this.#processButtons(gamepad);
        this.#processAxes(gamepad);
    }

    /**
     * Process button inputs
     * @param {Gamepad} gamepad
     */
    #processButtons(gamepad) {
        for (const [name, index] of Object.entries(BUTTONS)) {
            const button = gamepad.buttons[index];
            if (!button) continue;

            const wasPressed = this.#buttonStates[name];
            const isPressed = button.pressed;

            if (isPressed && !wasPressed) {
                this.#onButtonPress(name);
            } else if (!isPressed && wasPressed) {
                this.#onButtonRelease(name);
            }

            this.#buttonStates[name] = isPressed;
        }
    }

    /**
     * Handle button press
     * @param {string} button
     */
    #onButtonPress(button) {
        this.events.emit(EVENTS.GAMEPAD_BUTTON, { button, pressed: true });

        switch (button) {
            case 'A':
                // Select/Open
                this.#performAction('select');
                break;

            case 'B':
                // Back/Cancel
                this.events.emit(EVENTS.MODAL_CLOSE);
                this.events.emit('navigate:back');
                break;

            case 'X':
                // Preview
                this.#performAction('preview');
                break;

            case 'Y':
                // Pin
                this.#performAction('pin');
                break;

            case 'LB':
                // Previous page/category
                this.events.emit(EVENTS.CATEGORY_PREV);
                break;

            case 'RB':
                // Next page/category
                this.events.emit(EVENTS.CATEGORY_NEXT);
                break;

            case 'START':
                // Open menu
                this.events.emit(EVENTS.TOGGLE_MENU);
                break;

            case 'BACK':
                // Toggle view
                this.events.emit(EVENTS.VIEW_CYCLE);
                break;

            case 'DPAD_UP':
                this.#navigate('up');
                break;

            case 'DPAD_DOWN':
                this.#navigate('down');
                break;

            case 'DPAD_LEFT':
                this.#navigate('left');
                break;

            case 'DPAD_RIGHT':
                this.#navigate('right');
                break;
        }
    }

    /**
     * Handle button release
     * @param {string} button
     */
    #onButtonRelease(button) {
        this.events.emit(EVENTS.GAMEPAD_BUTTON, { button, pressed: false });
    }

    /**
     * Process analog stick axes
     * @param {Gamepad} gamepad
     */
    #processAxes(gamepad) {
        // Left stick for navigation
        const leftX = this.#applyDeadzone(gamepad.axes[AXES.LEFT_X]);
        const leftY = this.#applyDeadzone(gamepad.axes[AXES.LEFT_Y]);

        if (leftX !== 0 || leftY !== 0) {
            this.#handleStickNavigation(leftX, leftY);
        }

        // Right stick for scrolling
        const rightY = this.#applyDeadzone(gamepad.axes[AXES.RIGHT_Y]);

        if (rightY !== 0) {
            this.#handleScroll(rightY);
        }

        // Emit axis values for custom handling
        this.events.emit(EVENTS.GAMEPAD_AXIS, {
            leftX,
            leftY,
            rightX: this.#applyDeadzone(gamepad.axes[AXES.RIGHT_X]),
            rightY
        });
    }

    /**
     * Apply deadzone to axis value
     * @param {number} value
     * @returns {number}
     */
    #applyDeadzone(value) {
        return Math.abs(value) < this.#deadzone ? 0 : value;
    }

    /**
     * Handle stick navigation
     * @param {number} x
     * @param {number} y
     */
    #handleStickNavigation(x, y) {
        const now = Date.now();
        if (now - this.#lastNavigateTime < this.#navigateCooldown) return;

        // Determine direction based on strongest axis
        let direction = null;

        if (Math.abs(x) > Math.abs(y)) {
            direction = x > 0 ? 'right' : 'left';
        } else if (Math.abs(y) > 0.3) {
            direction = y > 0 ? 'down' : 'up';
        }

        if (direction) {
            this.#navigate(direction);
            this.#lastNavigateTime = now;
        }
    }

    /**
     * Handle scroll with right stick
     * @param {number} y
     */
    #handleScroll(y) {
        const scrollContainer = document.querySelector('.main-view-container, .scroll-container');
        if (scrollContainer) {
            scrollContainer.scrollTop += y * 20;
        }
    }

    /**
     * Navigate in direction
     * @param {string} direction
     */
    #navigate(direction) {
        this.events.emit(`navigate:${direction}`, { source: 'gamepad' });

        // Also handle grid navigation
        const grid = document.querySelector('.tool-grid, .grid-view');
        if (!grid) return;

        const cards = Array.from(grid.querySelectorAll('.tool-card'));
        if (cards.length === 0) return;

        const focused = document.activeElement;
        let currentIndex = cards.indexOf(focused);

        if (currentIndex === -1) currentIndex = 0;

        const gridStyle = window.getComputedStyle(grid);
        const columns = gridStyle.gridTemplateColumns?.split(' ').length || 4;

        let nextIndex = currentIndex;

        switch (direction) {
            case 'up':
                nextIndex = Math.max(0, currentIndex - columns);
                break;
            case 'down':
                nextIndex = Math.min(cards.length - 1, currentIndex + columns);
                break;
            case 'left':
                nextIndex = Math.max(0, currentIndex - 1);
                break;
            case 'right':
                nextIndex = Math.min(cards.length - 1, currentIndex + 1);
                break;
        }

        if (cards[nextIndex]) {
            cards[nextIndex].focus();
            cards[nextIndex].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    /**
     * Perform action on focused element
     * @param {string} action
     */
    #performAction(action) {
        const focused = document.activeElement;

        if (focused?.classList.contains('tool-card')) {
            const toolId = focused.dataset.toolId;
            if (toolId) {
                switch (action) {
                    case 'select':
                        this.events.emit(EVENTS.TOOL_OPEN, { toolId });
                        break;
                    case 'preview':
                        this.events.emit(EVENTS.TOOL_PREVIEW, { toolId });
                        break;
                    case 'pin':
                        this.events.emit(EVENTS.TOOL_PIN_TOGGLE, { toolId });
                        break;
                }
            }
        }
    }

    /**
     * Vibrate controller
     * @param {number} duration - Duration in ms
     * @param {number} intensity - 0 to 1
     */
    vibrate(duration = 100, intensity = 0.5) {
        if (this.#gamepadIndex === null) return;

        const gamepad = navigator.getGamepads()[this.#gamepadIndex];
        if (!gamepad?.vibrationActuator) return;

        gamepad.vibrationActuator.playEffect('dual-rumble', {
            duration,
            strongMagnitude: intensity,
            weakMagnitude: intensity * 0.5
        }).catch(() => {
            // Vibration not supported or failed
        });
    }

    /**
     * Check if gamepad is connected
     * @returns {boolean}
     */
    isConnected() {
        return this.#gamepadIndex !== null;
    }

    /**
     * Get connected gamepad
     * @returns {Gamepad|null}
     */
    getGamepad() {
        if (this.#gamepadIndex === null) return null;
        return navigator.getGamepads()[this.#gamepadIndex];
    }

    /**
     * Set deadzone
     * @param {number} value
     */
    setDeadzone(value) {
        this.#deadzone = Math.max(0, Math.min(1, value));
    }

    /**
     * Set navigation cooldown
     * @param {number} ms
     */
    setNavigateCooldown(ms) {
        this.#navigateCooldown = ms;
    }

    /**
     * Destroy handler
     */
    destroy() {
        this.#stopPolling();
        this.#gamepadIndex = null;
        this.#buttonStates = {};
    }
}

export { GamepadHandler, BUTTONS, AXES };
