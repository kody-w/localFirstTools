/**
 * Notification - Toast notifications
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';

class NotificationManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {NotificationManager}
     */
    static getInstance() {
        if (!NotificationManager.#instance) {
            NotificationManager.#instance = new NotificationManager();
        }
        return NotificationManager.#instance;
    }

    constructor() {
        if (NotificationManager.#instance) {
            return NotificationManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.#container = null;
        this.#queue = [];
        this.#activeNotifications = new Map();
        this.#maxVisible = 5;

        this.#initialize();
    }

    #container;
    #queue;
    #activeNotifications;
    #maxVisible;

    /**
     * Initialize notification manager
     */
    #initialize() {
        this.#createContainer();
        this.#bindEvents();
        this.#injectStyles();
    }

    /**
     * Create notification container
     */
    #createContainer() {
        this.#container = document.createElement('div');
        this.#container.className = 'notification-container';
        this.#container.setAttribute('role', 'region');
        this.#container.setAttribute('aria-label', 'Notifications');
        this.#container.setAttribute('aria-live', 'polite');

        document.body.appendChild(this.#container);
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        this.events.on(EVENTS.NOTIFICATION, (data) => {
            this.show(data);
        });
    }

    /**
     * Show a notification
     * @param {Object} options
     * @returns {string} Notification ID
     */
    show(options = {}) {
        const notification = {
            id: `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            message: options.message || '',
            type: options.type || 'info', // info, success, warning, error
            duration: options.duration ?? 4000,
            closable: options.closable !== false,
            action: options.action || null,
            icon: options.icon || this.#getDefaultIcon(options.type)
        };

        // Check if we need to queue
        if (this.#activeNotifications.size >= this.#maxVisible) {
            this.#queue.push(notification);
            return notification.id;
        }

        this.#displayNotification(notification);
        return notification.id;
    }

    /**
     * Display notification
     * @param {Object} notification
     */
    #displayNotification(notification) {
        const element = document.createElement('div');
        element.className = `notification notification-${notification.type}`;
        element.id = notification.id;
        element.setAttribute('role', 'alert');

        element.innerHTML = `
            <div class="notification-content">
                ${notification.icon ? `<span class="notification-icon">${notification.icon}</span>` : ''}
                <span class="notification-message">${notification.message}</span>
            </div>
            <div class="notification-actions">
                ${notification.action ? `
                    <button class="notification-action-btn">${notification.action.label}</button>
                ` : ''}
                ${notification.closable ? `
                    <button class="notification-close" aria-label="Dismiss">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                ` : ''}
            </div>
            ${notification.duration > 0 ? '<div class="notification-progress"></div>' : ''}
        `;

        // Bind event handlers
        if (notification.closable) {
            element.querySelector('.notification-close')?.addEventListener('click', () => {
                this.dismiss(notification.id);
            });
        }

        if (notification.action) {
            element.querySelector('.notification-action-btn')?.addEventListener('click', () => {
                notification.action.handler?.();
                this.dismiss(notification.id);
            });
        }

        // Add to container
        this.#container.appendChild(element);
        this.#activeNotifications.set(notification.id, { element, notification });

        // Animate in
        requestAnimationFrame(() => {
            element.classList.add('visible');
        });

        // Start progress animation
        if (notification.duration > 0) {
            const progress = element.querySelector('.notification-progress');
            if (progress) {
                progress.style.animationDuration = `${notification.duration}ms`;
            }

            // Auto dismiss
            setTimeout(() => {
                this.dismiss(notification.id);
            }, notification.duration);
        }
    }

    /**
     * Dismiss a notification
     * @param {string} id
     */
    dismiss(id) {
        const data = this.#activeNotifications.get(id);
        if (!data) return;

        const { element } = data;

        // Animate out
        element.classList.remove('visible');
        element.classList.add('dismissing');

        setTimeout(() => {
            element.remove();
            this.#activeNotifications.delete(id);

            // Show next queued notification
            if (this.#queue.length > 0) {
                const next = this.#queue.shift();
                this.#displayNotification(next);
            }
        }, 300);
    }

    /**
     * Dismiss all notifications
     */
    dismissAll() {
        for (const id of this.#activeNotifications.keys()) {
            this.dismiss(id);
        }
        this.#queue = [];
    }

    /**
     * Get default icon for type
     * @param {string} type
     * @returns {string}
     */
    #getDefaultIcon(type) {
        const icons = {
            info: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>`,
            success: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>`,
            warning: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>`,
            error: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>`
        };

        return icons[type] || icons.info;
    }

    /**
     * Shorthand methods
     */
    info(message, options = {}) {
        return this.show({ ...options, message, type: 'info' });
    }

    success(message, options = {}) {
        return this.show({ ...options, message, type: 'success' });
    }

    warning(message, options = {}) {
        return this.show({ ...options, message, type: 'warning' });
    }

    error(message, options = {}) {
        return this.show({ ...options, message, type: 'error' });
    }

    /**
     * Inject notification styles
     */
    #injectStyles() {
        if (document.getElementById('notification-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification-container {
                position: fixed;
                top: var(--space-4);
                right: var(--space-4);
                display: flex;
                flex-direction: column;
                gap: var(--space-2);
                z-index: 10000;
                max-width: 400px;
                pointer-events: none;
            }

            @media (max-width: 480px) {
                .notification-container {
                    top: auto;
                    bottom: 80px;
                    left: var(--space-3);
                    right: var(--space-3);
                    max-width: none;
                }
            }

            .notification {
                display: flex;
                align-items: flex-start;
                gap: var(--space-3);
                padding: var(--space-3) var(--space-4);
                background: var(--color-bg-elevated);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-lg);
                box-shadow: var(--shadow-lg);
                pointer-events: auto;
                transform: translateX(100%);
                opacity: 0;
                transition: all var(--duration-300) var(--ease-out);
                overflow: hidden;
                position: relative;
            }

            .notification.visible {
                transform: translateX(0);
                opacity: 1;
            }

            .notification.dismissing {
                transform: translateX(100%);
                opacity: 0;
            }

            .notification-content {
                flex: 1;
                display: flex;
                align-items: flex-start;
                gap: var(--space-2);
            }

            .notification-icon {
                flex-shrink: 0;
            }

            .notification-message {
                font-size: var(--text-sm);
                line-height: 1.4;
            }

            .notification-actions {
                display: flex;
                align-items: center;
                gap: var(--space-2);
            }

            .notification-action-btn {
                padding: var(--space-1) var(--space-2);
                background: var(--color-accent);
                color: var(--color-bg-primary);
                border: none;
                border-radius: var(--radius-sm);
                font-size: var(--text-xs);
                font-weight: 500;
                cursor: pointer;
                transition: background var(--duration-150);
            }

            .notification-action-btn:hover {
                background: var(--color-accent-hover);
            }

            .notification-close {
                padding: var(--space-1);
                background: none;
                border: none;
                color: var(--color-text-tertiary);
                cursor: pointer;
                border-radius: var(--radius-sm);
                transition: all var(--duration-150);
            }

            .notification-close:hover {
                color: var(--color-text-primary);
                background: var(--color-bg-tertiary);
            }

            .notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: var(--color-accent);
                animation: notification-progress linear forwards;
            }

            @keyframes notification-progress {
                from { width: 100%; }
                to { width: 0%; }
            }

            /* Type variants */
            .notification-info .notification-icon { color: var(--color-info); }
            .notification-success .notification-icon { color: var(--color-success); }
            .notification-warning .notification-icon { color: var(--color-warning); }
            .notification-error .notification-icon { color: var(--color-error); }

            .notification-info { border-left: 3px solid var(--color-info); }
            .notification-success { border-left: 3px solid var(--color-success); }
            .notification-warning { border-left: 3px solid var(--color-warning); }
            .notification-error { border-left: 3px solid var(--color-error); }

            .notification-success .notification-progress { background: var(--color-success); }
            .notification-warning .notification-progress { background: var(--color-warning); }
            .notification-error .notification-progress { background: var(--color-error); }
        `;

        document.head.appendChild(styles);
    }
}

export { NotificationManager };
