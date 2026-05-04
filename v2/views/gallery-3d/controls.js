/**
 * Controls 3D - First-person camera controls
 * Local First Tools v2
 */

import { GALLERY_3D } from '../../core/constants.js';
import { EVENTS } from '../../core/event-bus.js';

class Controls3D {
    /**
     * Create 3D controls
     * @param {THREE.Camera} camera
     * @param {HTMLElement} domElement
     * @param {EventBus} events
     */
    constructor(camera, domElement, events) {
        this.camera = camera;
        this.domElement = domElement;
        this.events = events;

        // Movement state
        this.velocity = { x: 0, y: 0, z: 0 };
        this.rotation = { x: 0, y: 0 };
        this.keys = {};
        this.gamepadIndex = null;

        // Settings
        this.moveSpeed = GALLERY_3D.MOVEMENT_SPEED;
        this.lookSpeed = GALLERY_3D.LOOK_SPEED;
        this.deadzone = GALLERY_3D.CONTROLLER_DEADZONE;

        // Pointer lock
        this.isLocked = false;

        this.#bindEvents();
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Pointer lock
        this.domElement.addEventListener('click', () => this.lock());

        document.addEventListener('pointerlockchange', () => {
            this.isLocked = document.pointerLockElement === this.domElement;
        });

        // Mouse movement
        document.addEventListener('mousemove', (e) => this.#onMouseMove(e));

        // Keyboard
        document.addEventListener('keydown', (e) => this.#onKeyDown(e));
        document.addEventListener('keyup', (e) => this.#onKeyUp(e));

        // Gamepad
        window.addEventListener('gamepadconnected', (e) => {
            this.gamepadIndex = e.gamepad.index;
            this.events.emit(EVENTS.GAMEPAD_CONNECTED, { gamepad: e.gamepad });
        });

        window.addEventListener('gamepaddisconnected', (e) => {
            if (e.gamepad.index === this.gamepadIndex) {
                this.gamepadIndex = null;
            }
            this.events.emit(EVENTS.GAMEPAD_DISCONNECTED);
        });

        // Touch controls
        this.#setupTouchControls();
    }

    /**
     * Lock pointer
     */
    lock() {
        if (!this.isLocked) {
            this.domElement.requestPointerLock();
        }
    }

    /**
     * Unlock pointer
     */
    unlock() {
        if (this.isLocked) {
            document.exitPointerLock();
        }
    }

    /**
     * Handle mouse movement
     * @param {MouseEvent} e
     */
    #onMouseMove(e) {
        if (!this.isLocked) return;

        const movementX = e.movementX || 0;
        const movementY = e.movementY || 0;

        this.rotation.y -= movementX * this.lookSpeed;
        this.rotation.x -= movementY * this.lookSpeed;

        // Clamp vertical rotation
        this.rotation.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotation.x));
    }

    /**
     * Handle key down
     * @param {KeyboardEvent} e
     */
    #onKeyDown(e) {
        this.keys[e.code] = true;

        // Handle action keys
        if (e.code === 'Enter' || e.code === 'Space') {
            this.#performAction();
        }
    }

    /**
     * Handle key up
     * @param {KeyboardEvent} e
     */
    #onKeyUp(e) {
        this.keys[e.code] = false;
    }

    /**
     * Setup touch controls
     */
    #setupTouchControls() {
        let touchStart = { x: 0, y: 0 };
        let isTouching = false;

        this.domElement.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                touchStart.x = e.touches[0].clientX;
                touchStart.y = e.touches[0].clientY;
                isTouching = true;
            }
        });

        this.domElement.addEventListener('touchmove', (e) => {
            if (!isTouching || e.touches.length !== 1) return;

            const touch = e.touches[0];
            const deltaX = touch.clientX - touchStart.x;
            const deltaY = touch.clientY - touchStart.y;

            // Look around with drag
            this.rotation.y -= deltaX * this.lookSpeed * 2;
            this.rotation.x -= deltaY * this.lookSpeed * 2;
            this.rotation.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotation.x));

            touchStart.x = touch.clientX;
            touchStart.y = touch.clientY;

            e.preventDefault();
        }, { passive: false });

        this.domElement.addEventListener('touchend', () => {
            isTouching = false;
        });

        // Double tap to move forward
        let lastTap = 0;
        this.domElement.addEventListener('touchend', (e) => {
            const currentTime = Date.now();
            if (currentTime - lastTap < 300) {
                // Double tap - move forward
                this.velocity.z = -this.moveSpeed * 10;
                setTimeout(() => {
                    this.velocity.z = 0;
                }, 500);
            }
            lastTap = currentTime;
        });
    }

    /**
     * Perform action on focused item
     */
    #performAction() {
        this.events.emit(EVENTS.GALLERY_3D_TOOL_SELECT);
    }

    /**
     * Update controls
     */
    update() {
        this.#updateFromKeyboard();
        this.#updateFromGamepad();
        this.#applyMovement();
    }

    /**
     * Update from keyboard input
     */
    #updateFromKeyboard() {
        // Forward/backward
        if (this.keys['KeyW'] || this.keys['ArrowUp']) {
            this.velocity.z = -this.moveSpeed;
        } else if (this.keys['KeyS'] || this.keys['ArrowDown']) {
            this.velocity.z = this.moveSpeed;
        } else {
            this.velocity.z *= 0.9; // Friction
        }

        // Left/right strafe
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) {
            this.velocity.x = -this.moveSpeed;
        } else if (this.keys['KeyD'] || this.keys['ArrowRight']) {
            this.velocity.x = this.moveSpeed;
        } else {
            this.velocity.x *= 0.9;
        }

        // Up/down (for floating camera)
        if (this.keys['Space']) {
            this.velocity.y = this.moveSpeed;
        } else if (this.keys['ShiftLeft']) {
            this.velocity.y = -this.moveSpeed;
        } else {
            this.velocity.y *= 0.9;
        }
    }

    /**
     * Update from gamepad input
     */
    #updateFromGamepad() {
        if (this.gamepadIndex === null) return;

        const gamepads = navigator.getGamepads();
        const gamepad = gamepads[this.gamepadIndex];

        if (!gamepad) return;

        // Left stick - movement
        const leftX = this.#applyDeadzone(gamepad.axes[0]);
        const leftY = this.#applyDeadzone(gamepad.axes[1]);

        if (leftX !== 0 || leftY !== 0) {
            this.velocity.x = leftX * this.moveSpeed;
            this.velocity.z = leftY * this.moveSpeed;
        }

        // Right stick - look
        const rightX = this.#applyDeadzone(gamepad.axes[2]);
        const rightY = this.#applyDeadzone(gamepad.axes[3]);

        if (rightX !== 0 || rightY !== 0) {
            this.rotation.y -= rightX * this.lookSpeed * 3;
            this.rotation.x -= rightY * this.lookSpeed * 3;
            this.rotation.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotation.x));
        }

        // A button - select
        if (gamepad.buttons[0].pressed) {
            this.#performAction();
        }

        // B button - exit
        if (gamepad.buttons[1].pressed) {
            this.events.emit(EVENTS.GALLERY_3D_EXIT);
        }
    }

    /**
     * Apply deadzone to axis value
     * @param {number} value
     * @returns {number}
     */
    #applyDeadzone(value) {
        return Math.abs(value) < this.deadzone ? 0 : value;
    }

    /**
     * Apply movement to camera
     */
    #applyMovement() {
        // Apply rotation
        this.camera.rotation.order = 'YXZ';
        this.camera.rotation.y = this.rotation.y;
        this.camera.rotation.x = this.rotation.x;

        // Calculate movement direction based on camera rotation
        const forward = { x: 0, z: 0 };
        const right = { x: 0, z: 0 };

        forward.x = Math.sin(this.rotation.y);
        forward.z = Math.cos(this.rotation.y);

        right.x = Math.cos(this.rotation.y);
        right.z = -Math.sin(this.rotation.y);

        // Apply velocity in world space
        this.camera.position.x += forward.x * -this.velocity.z + right.x * this.velocity.x;
        this.camera.position.z += forward.z * -this.velocity.z + right.z * this.velocity.x;
        this.camera.position.y += this.velocity.y;

        // Clamp height
        this.camera.position.y = Math.max(1, Math.min(4, this.camera.position.y));

        // Clamp to gallery bounds
        this.camera.position.x = Math.max(-9, Math.min(9, this.camera.position.x));
    }

    /**
     * Reset controls
     */
    reset() {
        this.velocity = { x: 0, y: 0, z: 0 };
        this.rotation = { x: 0, y: 0 };
        this.camera.position.set(0, 2, 5);
        this.camera.rotation.set(0, 0, 0);
    }

    /**
     * Get current position
     * @returns {{x: number, y: number, z: number}}
     */
    getPosition() {
        return {
            x: this.camera.position.x,
            y: this.camera.position.y,
            z: this.camera.position.z
        };
    }

    /**
     * Set position
     * @param {number} x
     * @param {number} y
     * @param {number} z
     */
    setPosition(x, y, z) {
        this.camera.position.set(x, y, z);
    }

    /**
     * Dispose controls
     */
    dispose() {
        this.unlock();
        this.keys = {};
        this.gamepadIndex = null;
    }
}

export { Controls3D };
