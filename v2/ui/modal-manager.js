/**
 * Modal Manager - Modal coordination and stacking
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';

class ModalManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {ModalManager}
     */
    static getInstance() {
        if (!ModalManager.#instance) {
            ModalManager.#instance = new ModalManager();
        }
        return ModalManager.#instance;
    }

    constructor() {
        if (ModalManager.#instance) {
            return ModalManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.#modals = new Map();
        this.#stack = [];
        this.#baseZIndex = 1000;

        this.#bindEvents();
        this.#injectStyles();
    }

    #modals;
    #stack;
    #baseZIndex;

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Close modal on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.#stack.length > 0) {
                e.preventDefault();
                this.closeTop();
            }
        });

        // Listen for modal events
        this.events.on(EVENTS.MODAL_OPEN, ({ id, type }) => {
            // Track external modal opens
            if (id && !this.#modals.has(id)) {
                this.#stack.push(id);
            }
        });

        this.events.on(EVENTS.MODAL_CLOSE, ({ id }) => {
            if (id) {
                this.close(id);
            } else {
                this.closeTop();
            }
        });
    }

    /**
     * Open a modal
     * @param {Object} options
     * @returns {string} Modal ID
     */
    open(options = {}) {
        const id = options.id || `modal_${Date.now()}`;

        // Create modal container
        const modal = document.createElement('div');
        modal.className = `modal ${options.className || ''}`;
        modal.id = id;
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');

        if (options.ariaLabel) {
            modal.setAttribute('aria-label', options.ariaLabel);
        }

        // Calculate z-index
        const zIndex = this.#baseZIndex + (this.#stack.length * 10);
        modal.style.zIndex = zIndex;

        // Build modal structure
        modal.innerHTML = `
            <div class="modal-backdrop" data-dismiss="modal"></div>
            <div class="modal-dialog ${options.size ? `modal-${options.size}` : ''}">
                ${options.header !== false ? `
                    <div class="modal-header">
                        ${options.title ? `<h2 class="modal-title">${options.title}</h2>` : ''}
                        ${options.closable !== false ? `
                            <button class="btn btn-icon modal-close" data-dismiss="modal" aria-label="Close">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M18 6L6 18M6 6l12 12"/>
                                </svg>
                            </button>
                        ` : ''}
                    </div>
                ` : ''}
                <div class="modal-body">
                    ${options.content || ''}
                </div>
                ${options.footer ? `
                    <div class="modal-footer">
                        ${options.footer}
                    </div>
                ` : ''}
            </div>
        `;

        // Add to DOM
        document.body.appendChild(modal);

        // Store modal info
        this.#modals.set(id, {
            element: modal,
            options,
            onClose: options.onClose
        });

        this.#stack.push(id);

        // Bind dismiss handlers
        modal.querySelectorAll('[data-dismiss="modal"]').forEach(el => {
            el.addEventListener('click', () => this.close(id));
        });

        // Prevent scroll on body
        if (this.#stack.length === 1) {
            document.body.style.overflow = 'hidden';
        }

        // Animate in
        requestAnimationFrame(() => {
            modal.classList.add('visible');
        });

        // Focus first focusable element
        this.#trapFocus(modal);

        this.events.emit(EVENTS.MODAL_OPEN, { id, type: options.type });

        return id;
    }

    /**
     * Close a specific modal
     * @param {string} id
     */
    close(id) {
        const modalInfo = this.#modals.get(id);
        if (!modalInfo) return;

        const { element, onClose } = modalInfo;

        // Animate out
        element.classList.remove('visible');

        setTimeout(() => {
            element.remove();
            this.#modals.delete(id);

            // Remove from stack
            const index = this.#stack.indexOf(id);
            if (index > -1) {
                this.#stack.splice(index, 1);
            }

            // Restore scroll if no more modals
            if (this.#stack.length === 0) {
                document.body.style.overflow = '';
            }

            // Call onClose callback
            if (typeof onClose === 'function') {
                onClose();
            }

            this.events.emit(EVENTS.MODAL_CLOSE, { id });
        }, 300);
    }

    /**
     * Close the topmost modal
     */
    closeTop() {
        if (this.#stack.length > 0) {
            const topId = this.#stack[this.#stack.length - 1];
            this.close(topId);
        }
    }

    /**
     * Close all modals
     */
    closeAll() {
        const ids = [...this.#stack];
        ids.forEach(id => this.close(id));
    }

    /**
     * Check if any modals are open
     * @returns {boolean}
     */
    hasOpenModals() {
        return this.#stack.length > 0;
    }

    /**
     * Get open modal count
     * @returns {number}
     */
    getOpenCount() {
        return this.#stack.length;
    }

    /**
     * Update modal content
     * @param {string} id
     * @param {string} content
     */
    updateContent(id, content) {
        const modalInfo = this.#modals.get(id);
        if (!modalInfo) return;

        const body = modalInfo.element.querySelector('.modal-body');
        if (body) {
            body.innerHTML = content;
        }
    }

    /**
     * Trap focus within modal
     * @param {HTMLElement} modal
     */
    #trapFocus(modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        // Focus first element
        firstFocusable?.focus();

        // Trap focus
        modal.addEventListener('keydown', (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable?.focus();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable?.focus();
                }
            }
        });
    }

    /**
     * Show confirmation dialog
     * @param {Object} options
     * @returns {Promise<boolean>}
     */
    confirm(options = {}) {
        return new Promise((resolve) => {
            const id = this.open({
                title: options.title || 'Confirm',
                content: `<p>${options.message || 'Are you sure?'}</p>`,
                size: 'sm',
                footer: `
                    <button class="btn btn-secondary" data-action="cancel">
                        ${options.cancelText || 'Cancel'}
                    </button>
                    <button class="btn btn-primary" data-action="confirm">
                        ${options.confirmText || 'Confirm'}
                    </button>
                `,
                onClose: () => resolve(false)
            });

            const modal = this.#modals.get(id)?.element;
            if (!modal) return;

            modal.querySelector('[data-action="cancel"]')?.addEventListener('click', () => {
                this.close(id);
                resolve(false);
            });

            modal.querySelector('[data-action="confirm"]')?.addEventListener('click', () => {
                this.close(id);
                resolve(true);
            });
        });
    }

    /**
     * Show alert dialog
     * @param {Object} options
     * @returns {Promise<void>}
     */
    alert(options = {}) {
        return new Promise((resolve) => {
            const id = this.open({
                title: options.title || 'Alert',
                content: `<p>${options.message || ''}</p>`,
                size: 'sm',
                footer: `
                    <button class="btn btn-primary" data-action="ok">
                        ${options.okText || 'OK'}
                    </button>
                `,
                onClose: () => resolve()
            });

            const modal = this.#modals.get(id)?.element;
            if (!modal) return;

            modal.querySelector('[data-action="ok"]')?.addEventListener('click', () => {
                this.close(id);
                resolve();
            });
        });
    }

    /**
     * Inject modal styles
     */
    #injectStyles() {
        if (document.getElementById('modal-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'modal-styles';
        styles.textContent = `
            .modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity var(--duration-300);
            }

            .modal.visible {
                opacity: 1;
            }

            .modal-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
            }

            .modal-dialog {
                position: relative;
                width: 90%;
                max-width: 500px;
                max-height: 90vh;
                background: var(--color-bg-elevated);
                border-radius: var(--radius-xl);
                display: flex;
                flex-direction: column;
                transform: scale(0.95) translateY(20px);
                transition: transform var(--duration-300) var(--ease-out);
            }

            .modal.visible .modal-dialog {
                transform: scale(1) translateY(0);
            }

            .modal-sm .modal-dialog { max-width: 400px; }
            .modal-lg .modal-dialog { max-width: 800px; }
            .modal-xl .modal-dialog { max-width: 1140px; }
            .modal-fullscreen .modal-dialog {
                width: 100%;
                height: 100%;
                max-width: none;
                max-height: none;
                border-radius: 0;
            }

            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .modal-title {
                margin: 0;
                font-size: var(--text-lg);
            }

            .modal-body {
                flex: 1;
                padding: var(--space-4);
                overflow-y: auto;
            }

            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: var(--space-3);
                padding: var(--space-4);
                border-top: 1px solid var(--color-border);
            }

            @media (max-width: 640px) {
                .modal-dialog {
                    width: 100%;
                    height: 100%;
                    max-width: none;
                    max-height: none;
                    border-radius: 0;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

export { ModalManager };
