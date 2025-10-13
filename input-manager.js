/**
 * InputManager - Comprehensive input handling system for multiple input methods
 * Supports: Keyboard, Mouse, Touch, and Gamepad with automatic detection and dynamic switching
 */

class InputManager {
    constructor(options = {}) {
        // Configuration
        this.navigationThrottle = options.navigationThrottle || 200;
        this.gamepadPollRate = options.gamepadPollRate || 100;
        this.deadzone = options.deadzone || 0.3;

        // State
        this.currentInputMode = 'keyboard'; // 'keyboard', 'mouse', 'touch', 'gamepad'
        this.lastNavigationTime = 0;
        this.gamepadIndex = null;
        this.gamepadConnected = false;
        this.gamepadPollInterval = null;
        this.lastGamepadState = {};

        // Callbacks
        this.onNavigate = options.onNavigate || null; // (direction) => {}
        this.onSelect = options.onSelect || null; // () => {}
        this.onBack = options.onBack || null; // () => {}
        this.onInputModeChange = options.onInputModeChange || null; // (mode) => {}

        // Initialize
        this.init();
    }

    init() {
        this.setupKeyboardListeners();
        this.setupMouseListeners();
        this.setupTouchListeners();
        this.setupGamepadListeners();

        // Check for initially connected gamepads
        this.checkInitialGamepads();
    }

    // ============================================
    // KEYBOARD HANDLING
    // ============================================

    setupKeyboardListeners() {
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    handleKeyboard(e) {
        // Don't interfere with typing in input fields
        const activeElement = document.activeElement;
        const isInputField = activeElement && (
            activeElement.tagName === 'INPUT' ||
            activeElement.tagName === 'TEXTAREA' ||
            activeElement.isContentEditable
        );

        if (isInputField && !['Escape'].includes(e.key)) {
            return;
        }

        // Switch to keyboard mode
        this.setInputMode('keyboard');

        // Navigation keys
        const navigationKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
        const selectKeys = ['Enter', ' ', 'Space'];
        const backKeys = ['Escape', 'Backspace'];

        if (navigationKeys.includes(e.key)) {
            e.preventDefault();
            this.navigate(e.key.replace('Arrow', '').toLowerCase());
        } else if (selectKeys.includes(e.key)) {
            e.preventDefault();
            this.selectCurrent();
        } else if (backKeys.includes(e.key)) {
            e.preventDefault();
            this.goBack();
        }
    }

    // ============================================
    // MOUSE HANDLING
    // ============================================

    setupMouseListeners() {
        let mouseMoveTimeout;

        document.addEventListener('mousemove', (e) => {
            // Debounce to avoid triggering on tiny movements
            clearTimeout(mouseMoveTimeout);
            mouseMoveTimeout = setTimeout(() => {
                // Only switch to mouse if there's actual movement
                if (this.currentInputMode !== 'mouse') {
                    this.setInputMode('mouse');
                }
            }, 50);
        });

        document.addEventListener('mousedown', () => {
            this.setInputMode('mouse');
        });
    }

    // ============================================
    // TOUCH HANDLING
    // ============================================

    setupTouchListeners() {
        document.addEventListener('touchstart', (e) => {
            this.setInputMode('touch');
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            this.setInputMode('touch');
        }, { passive: true });
    }

    // ============================================
    // GAMEPAD HANDLING
    // ============================================

    setupGamepadListeners() {
        window.addEventListener('gamepadconnected', (e) => {
            this.handleGamepadConnected(e.gamepad);
        });

        window.addEventListener('gamepaddisconnected', (e) => {
            this.handleGamepadDisconnected(e.gamepad);
        });
    }

    checkInitialGamepads() {
        const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
        for (let i = 0; i < gamepads.length; i++) {
            if (gamepads[i]) {
                this.handleGamepadConnected(gamepads[i]);
                break;
            }
        }
    }

    handleGamepadConnected(gamepad) {
        console.log(`Gamepad connected: ${gamepad.id}`);
        this.gamepadIndex = gamepad.index;
        this.gamepadConnected = true;
        this.setInputMode('gamepad');

        // Show toast notification
        this.showToast(`🎮 Gamepad Connected: ${gamepad.id}`, 'success');

        // Start polling
        this.startGamepadPolling();
    }

    handleGamepadDisconnected(gamepad) {
        console.log(`Gamepad disconnected: ${gamepad.id}`);

        if (this.gamepadIndex === gamepad.index) {
            this.gamepadConnected = false;
            this.gamepadIndex = null;
            this.stopGamepadPolling();

            // Show toast notification
            this.showToast('🎮 Gamepad Disconnected', 'warning');

            // Switch back to keyboard mode
            this.setInputMode('keyboard');
        }
    }

    startGamepadPolling() {
        if (this.gamepadPollInterval) {
            clearInterval(this.gamepadPollInterval);
        }

        this.gamepadPollInterval = setInterval(() => {
            this.pollGamepad();
        }, this.gamepadPollRate);
    }

    stopGamepadPolling() {
        if (this.gamepadPollInterval) {
            clearInterval(this.gamepadPollInterval);
            this.gamepadPollInterval = null;
        }
    }

    pollGamepad() {
        if (!this.gamepadConnected || this.gamepadIndex === null) {
            return;
        }

        const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
        const gamepad = gamepads[this.gamepadIndex];

        if (!gamepad) {
            return;
        }

        // D-pad / Left stick navigation
        const axes = gamepad.axes;
        const buttons = gamepad.buttons;

        // Left stick (axes 0 and 1)
        const leftStickX = Math.abs(axes[0]) > this.deadzone ? axes[0] : 0;
        const leftStickY = Math.abs(axes[1]) > this.deadzone ? axes[1] : 0;

        // D-pad buttons (standard mapping)
        const dpadUp = buttons[12]?.pressed;
        const dpadDown = buttons[13]?.pressed;
        const dpadLeft = buttons[14]?.pressed;
        const dpadRight = buttons[15]?.pressed;

        // Face buttons
        const buttonA = buttons[0]?.pressed; // Select
        const buttonB = buttons[1]?.pressed; // Back
        const start = buttons[9]?.pressed;
        const back = buttons[8]?.pressed;

        // Navigation with throttling
        if (leftStickY < -this.deadzone || dpadUp) {
            this.navigate('up');
        } else if (leftStickY > this.deadzone || dpadDown) {
            this.navigate('down');
        } else if (leftStickX < -this.deadzone || dpadLeft) {
            this.navigate('left');
        } else if (leftStickX > this.deadzone || dpadRight) {
            this.navigate('right');
        }

        // Select action
        if (buttonA && !this.lastGamepadState.buttonA) {
            this.selectCurrent();
        }

        // Back action
        if ((buttonB && !this.lastGamepadState.buttonB) ||
            (back && !this.lastGamepadState.back)) {
            this.goBack();
        }

        // Store state for edge detection
        this.lastGamepadState = {
            buttonA,
            buttonB,
            back,
            start
        };
    }

    // ============================================
    // INPUT MODE MANAGEMENT
    // ============================================

    setInputMode(mode) {
        if (this.currentInputMode !== mode) {
            this.currentInputMode = mode;
            console.log(`Input mode changed to: ${mode}`);

            // Update UI hints
            this.updateControlFooter();

            // Trigger callback
            if (this.onInputModeChange) {
                this.onInputModeChange(mode);
            }
        }
    }

    updateControlFooter() {
        const footer = document.getElementById('control-footer');
        if (!footer) return;

        const hints = this.getControlHints();
        footer.innerHTML = hints;
    }

    getControlHints() {
        switch (this.currentInputMode) {
            case 'keyboard':
                return `
                    <span>⬆️⬇️⬅️➡️ Navigate</span>
                    <span>Enter/Space Select</span>
                    <span>Esc Back</span>
                `;

            case 'mouse':
                return `
                    <span>🖱️ Mouse Controls</span>
                    <span>Click to Select</span>
                `;

            case 'touch':
                return `
                    <span>👆 Touch Controls</span>
                    <span>Tap to Select</span>
                `;

            case 'gamepad':
                return `
                    <span>🎮 D-Pad/Stick Navigate</span>
                    <span>Ⓐ Select</span>
                    <span>Ⓑ Back</span>
                `;

            default:
                return '';
        }
    }

    // ============================================
    // NAVIGATION METHODS
    // ============================================

    navigate(direction) {
        // Throttle navigation to prevent too rapid movement
        const now = Date.now();
        if (now - this.lastNavigationTime < this.navigationThrottle) {
            return;
        }
        this.lastNavigationTime = now;

        console.log(`Navigate: ${direction}`);

        if (this.onNavigate) {
            this.onNavigate(direction);
        }
    }

    selectCurrent() {
        console.log('Select current');

        if (this.onSelect) {
            this.onSelect();
        }
    }

    goBack() {
        console.log('Go back');

        if (this.onBack) {
            this.onBack();
        }
    }

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================

    showToast(message, type = 'info') {
        const existingToast = document.getElementById('input-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const toast = document.createElement('div');
        toast.id = 'input-toast';
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        // Add styles if not already present
        if (!document.getElementById('toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                .toast {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 25px;
                    background: rgba(0, 0, 0, 0.9);
                    color: white;
                    border-radius: 8px;
                    font-family: system-ui, -apple-system, sans-serif;
                    font-size: 14px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    z-index: 10000;
                    animation: slideIn 0.3s ease-out, slideOut 0.3s ease-in 2.7s;
                    pointer-events: none;
                }

                .toast-success {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }

                .toast-warning {
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                }

                .toast-info {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                }

                @keyframes slideIn {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes slideOut {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(toast);

        // Remove after animation
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // ============================================
    // CLEANUP
    // ============================================

    destroy() {
        this.stopGamepadPolling();
        // Event listeners will be garbage collected when the instance is destroyed
    }
}

// ============================================
// USAGE EXAMPLE
// ============================================

/*
const inputManager = new InputManager({
    navigationThrottle: 200,
    gamepadPollRate: 100,
    deadzone: 0.3,

    onNavigate: (direction) => {
        console.log(`User navigated: ${direction}`);
        // Implement your navigation logic here
        // e.g., move selection highlight, scroll, etc.
    },

    onSelect: () => {
        console.log('User selected current item');
        // Implement your selection logic here
        // e.g., click current item, open menu, etc.
    },

    onBack: () => {
        console.log('User pressed back');
        // Implement your back navigation logic here
        // e.g., close modal, go to previous screen, etc.
    },

    onInputModeChange: (mode) => {
        console.log(`Input mode changed to: ${mode}`);
        // Implement any mode-specific UI changes
        // e.g., show/hide cursor, update help text, etc.
    }
});

// To manually change input mode
inputManager.setInputMode('gamepad');

// To clean up
inputManager.destroy();
*/
