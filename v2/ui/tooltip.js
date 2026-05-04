/**
 * Tooltip - Accessible tooltips
 * Local First Tools v2
 */

class Tooltip {
    static #instance = null;
    static #activeTooltip = null;

    /**
     * Get singleton instance
     * @returns {Tooltip}
     */
    static getInstance() {
        if (!Tooltip.#instance) {
            Tooltip.#instance = new Tooltip();
        }
        return Tooltip.#instance;
    }

    constructor() {
        if (Tooltip.#instance) {
            return Tooltip.#instance;
        }

        this.#tooltipEl = null;
        this.#showDelay = 500;
        this.#hideDelay = 100;
        this.#showTimeout = null;
        this.#hideTimeout = null;

        this.#initialize();
    }

    #tooltipEl;
    #showDelay;
    #hideDelay;
    #showTimeout;
    #hideTimeout;

    /**
     * Initialize tooltip system
     */
    #initialize() {
        this.#createTooltipElement();
        this.#bindGlobalEvents();
        this.#injectStyles();
    }

    /**
     * Create tooltip element
     */
    #createTooltipElement() {
        this.#tooltipEl = document.createElement('div');
        this.#tooltipEl.className = 'tooltip';
        this.#tooltipEl.setAttribute('role', 'tooltip');
        this.#tooltipEl.id = 'tooltip';

        document.body.appendChild(this.#tooltipEl);
    }

    /**
     * Bind global event listeners
     */
    #bindGlobalEvents() {
        // Use event delegation
        document.addEventListener('mouseenter', (e) => {
            const target = e.target.closest('[data-tooltip], [title]');
            if (target) {
                this.#handleMouseEnter(target);
            }
        }, true);

        document.addEventListener('mouseleave', (e) => {
            const target = e.target.closest('[data-tooltip], [title]');
            if (target) {
                this.#handleMouseLeave();
            }
        }, true);

        document.addEventListener('focusin', (e) => {
            const target = e.target.closest('[data-tooltip], [title]');
            if (target) {
                this.#handleFocusIn(target);
            }
        });

        document.addEventListener('focusout', (e) => {
            const target = e.target.closest('[data-tooltip], [title]');
            if (target) {
                this.#handleFocusOut();
            }
        });

        // Hide on scroll
        document.addEventListener('scroll', () => {
            this.hide();
        }, true);

        // Hide on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hide();
            }
        });
    }

    /**
     * Handle mouse enter
     * @param {HTMLElement} target
     */
    #handleMouseEnter(target) {
        this.#clearTimeouts();

        this.#showTimeout = setTimeout(() => {
            this.show(target);
        }, this.#showDelay);
    }

    /**
     * Handle mouse leave
     */
    #handleMouseLeave() {
        this.#clearTimeouts();

        this.#hideTimeout = setTimeout(() => {
            this.hide();
        }, this.#hideDelay);
    }

    /**
     * Handle focus in
     * @param {HTMLElement} target
     */
    #handleFocusIn(target) {
        this.#clearTimeouts();
        this.show(target);
    }

    /**
     * Handle focus out
     */
    #handleFocusOut() {
        this.#clearTimeouts();
        this.hide();
    }

    /**
     * Clear pending timeouts
     */
    #clearTimeouts() {
        if (this.#showTimeout) {
            clearTimeout(this.#showTimeout);
            this.#showTimeout = null;
        }
        if (this.#hideTimeout) {
            clearTimeout(this.#hideTimeout);
            this.#hideTimeout = null;
        }
    }

    /**
     * Show tooltip
     * @param {HTMLElement} target
     */
    show(target) {
        const text = target.dataset.tooltip || target.getAttribute('title');
        if (!text) return;

        // Remove native title to prevent double tooltip
        if (target.hasAttribute('title')) {
            target.dataset.originalTitle = target.getAttribute('title');
            target.removeAttribute('title');
        }

        // Set content
        this.#tooltipEl.textContent = text;

        // Get position
        const position = target.dataset.tooltipPosition || 'top';

        // Position tooltip
        this.#positionTooltip(target, position);

        // Show
        this.#tooltipEl.classList.add('visible');
        Tooltip.#activeTooltip = target;

        // Set ARIA
        target.setAttribute('aria-describedby', 'tooltip');
    }

    /**
     * Hide tooltip
     */
    hide() {
        this.#tooltipEl.classList.remove('visible');

        if (Tooltip.#activeTooltip) {
            Tooltip.#activeTooltip.removeAttribute('aria-describedby');

            // Restore title
            const originalTitle = Tooltip.#activeTooltip.dataset.originalTitle;
            if (originalTitle) {
                Tooltip.#activeTooltip.setAttribute('title', originalTitle);
                delete Tooltip.#activeTooltip.dataset.originalTitle;
            }

            Tooltip.#activeTooltip = null;
        }
    }

    /**
     * Position tooltip relative to target
     * @param {HTMLElement} target
     * @param {string} position
     */
    #positionTooltip(target, position) {
        const targetRect = target.getBoundingClientRect();
        const tooltipRect = this.#tooltipEl.getBoundingClientRect();
        const gap = 8;

        let top, left;

        // Remove position classes
        this.#tooltipEl.classList.remove('position-top', 'position-bottom', 'position-left', 'position-right');

        switch (position) {
            case 'top':
                top = targetRect.top - tooltipRect.height - gap;
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                this.#tooltipEl.classList.add('position-top');
                break;

            case 'bottom':
                top = targetRect.bottom + gap;
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                this.#tooltipEl.classList.add('position-bottom');
                break;

            case 'left':
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                left = targetRect.left - tooltipRect.width - gap;
                this.#tooltipEl.classList.add('position-left');
                break;

            case 'right':
                top = targetRect.top + (targetRect.height - tooltipRect.height) / 2;
                left = targetRect.right + gap;
                this.#tooltipEl.classList.add('position-right');
                break;

            default:
                top = targetRect.top - tooltipRect.height - gap;
                left = targetRect.left + (targetRect.width - tooltipRect.width) / 2;
                this.#tooltipEl.classList.add('position-top');
        }

        // Keep within viewport
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        // Flip if out of bounds
        if (top < 0 && position === 'top') {
            top = targetRect.bottom + gap;
            this.#tooltipEl.classList.remove('position-top');
            this.#tooltipEl.classList.add('position-bottom');
        }

        if (top + tooltipRect.height > vh && position === 'bottom') {
            top = targetRect.top - tooltipRect.height - gap;
            this.#tooltipEl.classList.remove('position-bottom');
            this.#tooltipEl.classList.add('position-top');
        }

        // Keep within horizontal bounds
        left = Math.max(gap, Math.min(vw - tooltipRect.width - gap, left));

        this.#tooltipEl.style.top = `${top}px`;
        this.#tooltipEl.style.left = `${left}px`;
    }

    /**
     * Set show delay
     * @param {number} ms
     */
    setShowDelay(ms) {
        this.#showDelay = ms;
    }

    /**
     * Set hide delay
     * @param {number} ms
     */
    setHideDelay(ms) {
        this.#hideDelay = ms;
    }

    /**
     * Inject tooltip styles
     */
    #injectStyles() {
        if (document.getElementById('tooltip-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'tooltip-styles';
        styles.textContent = `
            .tooltip {
                position: fixed;
                padding: var(--space-2) var(--space-3);
                background: var(--color-bg-elevated);
                color: var(--color-text-primary);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-md);
                font-size: var(--text-xs);
                max-width: 250px;
                white-space: normal;
                word-wrap: break-word;
                box-shadow: var(--shadow-md);
                opacity: 0;
                visibility: hidden;
                transition: opacity var(--duration-150), visibility var(--duration-150);
                z-index: 10001;
                pointer-events: none;
            }

            .tooltip.visible {
                opacity: 1;
                visibility: visible;
            }

            .tooltip::before {
                content: '';
                position: absolute;
                width: 8px;
                height: 8px;
                background: var(--color-bg-elevated);
                border: 1px solid var(--color-border);
                transform: rotate(45deg);
            }

            .tooltip.position-top::before {
                bottom: -5px;
                left: 50%;
                margin-left: -4px;
                border-top: none;
                border-left: none;
            }

            .tooltip.position-bottom::before {
                top: -5px;
                left: 50%;
                margin-left: -4px;
                border-bottom: none;
                border-right: none;
            }

            .tooltip.position-left::before {
                right: -5px;
                top: 50%;
                margin-top: -4px;
                border-bottom: none;
                border-left: none;
            }

            .tooltip.position-right::before {
                left: -5px;
                top: 50%;
                margin-top: -4px;
                border-top: none;
                border-right: none;
            }
        `;

        document.head.appendChild(styles);
    }
}

export { Tooltip };
