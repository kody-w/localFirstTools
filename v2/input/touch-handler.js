/**
 * Touch Handler - Touch and swipe gesture support
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';

class TouchHandler {
    /**
     * Create touch handler
     * @param {HTMLElement} container
     */
    constructor(container) {
        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();
        this.container = container;

        this.#touches = new Map();
        this.#gestures = {
            swipe: { enabled: true, threshold: 50 },
            pinch: { enabled: true, threshold: 0.1 },
            longPress: { enabled: true, duration: 500 },
            doubleTap: { enabled: true, interval: 300 }
        };

        this.#lastTap = 0;
        this.#longPressTimer = null;
        this.#initialPinchDistance = 0;

        this.#bindEvents();
    }

    #touches;
    #gestures;
    #lastTap;
    #longPressTimer;
    #initialPinchDistance;

    /**
     * Bind touch events
     */
    #bindEvents() {
        const options = { passive: false };

        this.container.addEventListener('touchstart', (e) => this.#onTouchStart(e), options);
        this.container.addEventListener('touchmove', (e) => this.#onTouchMove(e), options);
        this.container.addEventListener('touchend', (e) => this.#onTouchEnd(e), options);
        this.container.addEventListener('touchcancel', (e) => this.#onTouchCancel(e), options);
    }

    /**
     * Handle touch start
     * @param {TouchEvent} e
     */
    #onTouchStart(e) {
        this.events.emit('touch:start', { touches: e.touches.length });

        // Track touches
        for (const touch of e.changedTouches) {
            this.#touches.set(touch.identifier, {
                id: touch.identifier,
                startX: touch.clientX,
                startY: touch.clientY,
                currentX: touch.clientX,
                currentY: touch.clientY,
                startTime: Date.now(),
                target: touch.target
            });
        }

        // Single touch gestures
        if (e.touches.length === 1) {
            const touch = this.#touches.get(e.changedTouches[0].identifier);

            // Long press detection
            if (this.#gestures.longPress.enabled) {
                this.#startLongPressTimer(touch);
            }

            // Double tap detection
            if (this.#gestures.doubleTap.enabled) {
                const now = Date.now();
                if (now - this.#lastTap < this.#gestures.doubleTap.interval) {
                    this.#onDoubleTap(touch);
                    this.#lastTap = 0;
                } else {
                    this.#lastTap = now;
                }
            }
        }

        // Pinch gesture initialization
        if (e.touches.length === 2 && this.#gestures.pinch.enabled) {
            this.#initialPinchDistance = this.#getPinchDistance(e.touches[0], e.touches[1]);
        }
    }

    /**
     * Handle touch move
     * @param {TouchEvent} e
     */
    #onTouchMove(e) {
        // Cancel long press on move
        this.#cancelLongPressTimer();

        // Update touch positions
        for (const touch of e.changedTouches) {
            const tracked = this.#touches.get(touch.identifier);
            if (tracked) {
                tracked.currentX = touch.clientX;
                tracked.currentY = touch.clientY;
            }
        }

        // Handle pinch zoom
        if (e.touches.length === 2 && this.#gestures.pinch.enabled) {
            this.#handlePinch(e.touches[0], e.touches[1]);
            e.preventDefault();
        }

        // Handle swipe preview (for visual feedback)
        if (e.touches.length === 1) {
            const touch = this.#touches.get(e.changedTouches[0].identifier);
            if (touch) {
                const deltaX = touch.currentX - touch.startX;
                const deltaY = touch.currentY - touch.startY;

                this.events.emit('touch:move', {
                    deltaX,
                    deltaY,
                    target: touch.target
                });
            }
        }
    }

    /**
     * Handle touch end
     * @param {TouchEvent} e
     */
    #onTouchEnd(e) {
        this.#cancelLongPressTimer();

        for (const touch of e.changedTouches) {
            const tracked = this.#touches.get(touch.identifier);

            if (tracked) {
                // Check for swipe gesture
                if (this.#gestures.swipe.enabled) {
                    this.#detectSwipe(tracked);
                }

                // Check for tap
                const deltaX = Math.abs(tracked.currentX - tracked.startX);
                const deltaY = Math.abs(tracked.currentY - tracked.startY);
                const duration = Date.now() - tracked.startTime;

                if (deltaX < 10 && deltaY < 10 && duration < 200) {
                    this.events.emit('touch:tap', {
                        x: tracked.currentX,
                        y: tracked.currentY,
                        target: tracked.target
                    });
                }

                this.#touches.delete(touch.identifier);
            }
        }

        this.events.emit('touch:end', { remainingTouches: e.touches.length });
    }

    /**
     * Handle touch cancel
     * @param {TouchEvent} e
     */
    #onTouchCancel(e) {
        this.#cancelLongPressTimer();

        for (const touch of e.changedTouches) {
            this.#touches.delete(touch.identifier);
        }
    }

    /**
     * Detect swipe gesture
     * @param {Object} touch
     */
    #detectSwipe(touch) {
        const deltaX = touch.currentX - touch.startX;
        const deltaY = touch.currentY - touch.startY;
        const threshold = this.#gestures.swipe.threshold;
        const duration = Date.now() - touch.startTime;

        // Must be quick enough to be a swipe (under 300ms)
        if (duration > 300) return;

        const absX = Math.abs(deltaX);
        const absY = Math.abs(deltaY);

        // Determine swipe direction
        if (absX > threshold && absX > absY) {
            // Horizontal swipe
            const direction = deltaX > 0 ? 'right' : 'left';
            this.#onSwipe(direction, touch, { deltaX, deltaY, duration });
        } else if (absY > threshold && absY > absX) {
            // Vertical swipe
            const direction = deltaY > 0 ? 'down' : 'up';
            this.#onSwipe(direction, touch, { deltaX, deltaY, duration });
        }
    }

    /**
     * Handle swipe gesture
     * @param {string} direction
     * @param {Object} touch
     * @param {Object} details
     */
    #onSwipe(direction, touch, details) {
        const target = touch.target;
        const card = target.closest('.tool-card');

        this.events.emit('touch:swipe', {
            direction,
            ...details,
            target,
            card
        });

        // Handle card-specific swipes
        if (card) {
            const toolId = card.dataset.toolId;

            switch (direction) {
                case 'left':
                    // Swipe left to archive/dismiss
                    this.events.emit(EVENTS.TOOL_SWIPE_LEFT, { toolId });
                    break;

                case 'right':
                    // Swipe right to pin
                    this.events.emit(EVENTS.TOOL_PIN_TOGGLE, { toolId });
                    this.#showSwipeAction(card, 'Pinned!');
                    break;

                case 'up':
                    // Swipe up to add to collection
                    this.events.emit(EVENTS.TOOL_ADD_TO_COLLECTION, { toolId });
                    break;
            }
        }

        // Handle navigation swipes (on empty areas)
        if (!card && direction === 'right') {
            // Swipe right from edge to go back
            if (touch.startX < 50) {
                this.events.emit('navigate:back');
            }
        }
    }

    /**
     * Show swipe action feedback
     * @param {HTMLElement} card
     * @param {string} message
     */
    #showSwipeAction(card, message) {
        const feedback = document.createElement('div');
        feedback.className = 'swipe-feedback';
        feedback.textContent = message;
        feedback.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--color-accent);
            color: var(--color-bg-primary);
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            animation: swipe-feedback 0.5s ease-out forwards;
            pointer-events: none;
            z-index: 100;
        `;

        card.style.position = 'relative';
        card.appendChild(feedback);

        setTimeout(() => feedback.remove(), 500);
    }

    /**
     * Start long press timer
     * @param {Object} touch
     */
    #startLongPressTimer(touch) {
        this.#longPressTimer = setTimeout(() => {
            this.#onLongPress(touch);
        }, this.#gestures.longPress.duration);
    }

    /**
     * Cancel long press timer
     */
    #cancelLongPressTimer() {
        if (this.#longPressTimer) {
            clearTimeout(this.#longPressTimer);
            this.#longPressTimer = null;
        }
    }

    /**
     * Handle long press gesture
     * @param {Object} touch
     */
    #onLongPress(touch) {
        const target = touch.target;
        const card = target.closest('.tool-card');

        this.events.emit('touch:longpress', {
            x: touch.currentX,
            y: touch.currentY,
            target,
            card
        });

        if (card) {
            const toolId = card.dataset.toolId;
            // Long press opens context menu or preview
            this.events.emit(EVENTS.TOOL_CONTEXT_MENU, {
                toolId,
                x: touch.currentX,
                y: touch.currentY
            });

            // Haptic feedback (if available)
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }
        }
    }

    /**
     * Handle double tap
     * @param {Object} touch
     */
    #onDoubleTap(touch) {
        const target = touch.target;
        const card = target.closest('.tool-card');

        this.events.emit('touch:doubletap', {
            x: touch.currentX,
            y: touch.currentY,
            target,
            card
        });

        if (card) {
            const toolId = card.dataset.toolId;
            // Double tap to open tool
            this.events.emit(EVENTS.TOOL_OPEN, { toolId });
        }
    }

    /**
     * Get distance between two touches (for pinch)
     * @param {Touch} touch1
     * @param {Touch} touch2
     * @returns {number}
     */
    #getPinchDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    /**
     * Handle pinch gesture
     * @param {Touch} touch1
     * @param {Touch} touch2
     */
    #handlePinch(touch1, touch2) {
        const currentDistance = this.#getPinchDistance(touch1, touch2);
        const scale = currentDistance / this.#initialPinchDistance;
        const threshold = this.#gestures.pinch.threshold;

        if (Math.abs(scale - 1) > threshold) {
            this.events.emit('touch:pinch', {
                scale,
                centerX: (touch1.clientX + touch2.clientX) / 2,
                centerY: (touch1.clientY + touch2.clientY) / 2
            });

            // Pinch out to zoom/expand, pinch in to collapse
            if (scale > 1.3) {
                this.events.emit(EVENTS.VIEW_EXPAND);
            } else if (scale < 0.7) {
                this.events.emit(EVENTS.VIEW_COLLAPSE);
            }
        }
    }

    /**
     * Enable/disable gesture types
     * @param {string} gesture
     * @param {boolean} enabled
     */
    setGestureEnabled(gesture, enabled) {
        if (this.#gestures[gesture]) {
            this.#gestures[gesture].enabled = enabled;
        }
    }

    /**
     * Configure gesture thresholds
     * @param {string} gesture
     * @param {Object} config
     */
    configureGesture(gesture, config) {
        if (this.#gestures[gesture]) {
            Object.assign(this.#gestures[gesture], config);
        }
    }

    /**
     * Check if touch is supported
     * @returns {boolean}
     */
    static isSupported() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }

    /**
     * Destroy handler
     */
    destroy() {
        this.#cancelLongPressTimer();
        this.#touches.clear();
    }
}

export { TouchHandler };
