/**
 * Tour - Onboarding experience
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StorageManager } from '../storage/storage-manager.js';

class Tour {
    constructor() {
        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();

        this.#container = null;
        this.#currentStep = 0;
        this.#steps = [];
        this.#isActive = false;
        this.#overlay = null;
        this.#spotlight = null;
    }

    #container;
    #currentStep;
    #steps;
    #isActive;
    #overlay;
    #spotlight;

    /**
     * Define tour steps
     * @returns {Array}
     */
    #getDefaultSteps() {
        return [
            {
                id: 'welcome',
                title: 'Welcome to Local First Tools!',
                content: 'A collection of self-contained HTML applications that work offline. Let me show you around!',
                target: null, // No target = centered modal
                position: 'center'
            },
            {
                id: 'search',
                title: 'Find Tools Quickly',
                content: 'Use the search bar to find tools by name, description, or tags. Try pressing "/" for quick access.',
                target: '.search-input, #search-input, [data-tour="search"]',
                position: 'bottom'
            },
            {
                id: 'filters',
                title: 'Filter by Category',
                content: 'Browse tools by category, complexity level, or type. Click the filter icon to see all options.',
                target: '.filter-btn, [data-tour="filters"]',
                position: 'bottom'
            },
            {
                id: 'pin',
                title: 'Pin Your Favorites',
                content: 'Hover over any tool card and click the star icon to pin it. Pinned tools appear at the top!',
                target: '.tool-card:first-child, [data-tour="tool-card"]',
                position: 'right'
            },
            {
                id: 'views',
                title: 'Multiple View Modes',
                content: 'Switch between Grid, List, Masonry, Timeline, and Dashboard views to find your preferred layout.',
                target: '.view-toggle, [data-tour="views"]',
                position: 'bottom'
            },
            {
                id: 'keyboard',
                title: 'Keyboard Shortcuts',
                content: 'Press "?" at any time to see all keyboard shortcuts. Power users love this!',
                target: null,
                position: 'center'
            },
            {
                id: 'gamepad',
                title: 'Controller Support',
                content: 'Connect an Xbox or PlayStation controller to navigate the gallery and even play games!',
                target: null,
                position: 'center'
            },
            {
                id: '3d-gallery',
                title: '3D Gallery Mode',
                content: 'Try the immersive 3D gallery experience! Walk through a virtual museum of tools.',
                target: '[data-tour="3d-gallery"], .view-3d-btn',
                position: 'bottom'
            },
            {
                id: 'done',
                title: "You're All Set!",
                content: "That's the basics! Explore and have fun. You can always restart this tour from the settings.",
                target: null,
                position: 'center'
            }
        ];
    }

    /**
     * Start the tour
     * @param {Array} customSteps - Optional custom steps
     */
    start(customSteps = null) {
        if (this.#isActive) return;

        this.#steps = customSteps || this.#getDefaultSteps();
        this.#currentStep = 0;
        this.#isActive = true;

        this.#injectStyles();
        this.#createOverlay();
        this.#showStep(0);

        this.events.emit(EVENTS.TOUR_START);
    }

    /**
     * Skip the tour
     */
    skip() {
        this.#complete(false);
    }

    /**
     * Complete the tour
     * @param {boolean} finished
     */
    #complete(finished = true) {
        this.#isActive = false;
        this.#cleanup();

        this.storage.set('tourCompleted', true);
        this.storage.set('tourCompletedAt', Date.now());

        this.events.emit(EVENTS.TOUR_COMPLETE, { finished });

        if (finished) {
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Tour complete! Enjoy exploring!',
                type: 'success'
            });
        }
    }

    /**
     * Go to next step
     */
    next() {
        if (this.#currentStep < this.#steps.length - 1) {
            this.#currentStep++;
            this.#showStep(this.#currentStep);
        } else {
            this.#complete(true);
        }
    }

    /**
     * Go to previous step
     */
    prev() {
        if (this.#currentStep > 0) {
            this.#currentStep--;
            this.#showStep(this.#currentStep);
        }
    }

    /**
     * Go to specific step
     * @param {number} index
     */
    goTo(index) {
        if (index >= 0 && index < this.#steps.length) {
            this.#currentStep = index;
            this.#showStep(index);
        }
    }

    /**
     * Show a specific step
     * @param {number} index
     */
    #showStep(index) {
        const step = this.#steps[index];
        if (!step) return;

        // Find target element
        let targetEl = null;
        if (step.target) {
            targetEl = document.querySelector(step.target);
        }

        // Update spotlight
        this.#updateSpotlight(targetEl);

        // Create/update tooltip
        this.#createTooltip(step, targetEl);

        this.events.emit(EVENTS.TOUR_STEP, { step: index, stepData: step });
    }

    /**
     * Create overlay
     */
    #createOverlay() {
        this.#overlay = document.createElement('div');
        this.#overlay.className = 'tour-overlay';

        this.#spotlight = document.createElement('div');
        this.#spotlight.className = 'tour-spotlight';

        document.body.appendChild(this.#overlay);
        document.body.appendChild(this.#spotlight);
    }

    /**
     * Update spotlight position
     * @param {HTMLElement} target
     */
    #updateSpotlight(target) {
        if (!this.#spotlight) return;

        if (target) {
            const rect = target.getBoundingClientRect();
            const padding = 8;

            this.#spotlight.style.display = 'block';
            this.#spotlight.style.top = `${rect.top - padding}px`;
            this.#spotlight.style.left = `${rect.left - padding}px`;
            this.#spotlight.style.width = `${rect.width + padding * 2}px`;
            this.#spotlight.style.height = `${rect.height + padding * 2}px`;

            // Scroll into view if needed
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            this.#spotlight.style.display = 'none';
        }
    }

    /**
     * Create tooltip
     * @param {Object} step
     * @param {HTMLElement} target
     */
    #createTooltip(step, target) {
        // Remove existing tooltip
        const existing = document.querySelector('.tour-tooltip');
        existing?.remove();

        const tooltip = document.createElement('div');
        tooltip.className = 'tour-tooltip';

        const progress = `${this.#currentStep + 1} / ${this.#steps.length}`;

        tooltip.innerHTML = `
            <div class="tour-tooltip-content">
                <div class="tour-header">
                    <h4>${step.title}</h4>
                    <span class="tour-progress">${progress}</span>
                </div>
                <p>${step.content}</p>
                <div class="tour-footer">
                    <button class="tour-skip">Skip Tour</button>
                    <div class="tour-nav">
                        ${this.#currentStep > 0 ? '<button class="tour-prev">Back</button>' : ''}
                        <button class="tour-next">
                            ${this.#currentStep === this.#steps.length - 1 ? 'Finish' : 'Next'}
                        </button>
                    </div>
                </div>
            </div>
            <div class="tour-arrow"></div>
        `;

        // Position tooltip
        this.#positionTooltip(tooltip, step, target);

        document.body.appendChild(tooltip);

        // Bind events
        tooltip.querySelector('.tour-skip')?.addEventListener('click', () => this.skip());
        tooltip.querySelector('.tour-prev')?.addEventListener('click', () => this.prev());
        tooltip.querySelector('.tour-next')?.addEventListener('click', () => this.next());

        // Animate in
        requestAnimationFrame(() => {
            tooltip.classList.add('visible');
        });
    }

    /**
     * Position tooltip relative to target
     * @param {HTMLElement} tooltip
     * @param {Object} step
     * @param {HTMLElement} target
     */
    #positionTooltip(tooltip, step, target) {
        if (!target || step.position === 'center') {
            // Center in viewport
            tooltip.classList.add('centered');
            return;
        }

        const rect = target.getBoundingClientRect();
        const tooltipWidth = 300;
        const tooltipHeight = 200; // Approximate
        const gap = 16;

        let top, left;
        const position = step.position || 'bottom';

        switch (position) {
            case 'top':
                top = rect.top - tooltipHeight - gap;
                left = rect.left + rect.width / 2 - tooltipWidth / 2;
                tooltip.classList.add('position-top');
                break;

            case 'bottom':
                top = rect.bottom + gap;
                left = rect.left + rect.width / 2 - tooltipWidth / 2;
                tooltip.classList.add('position-bottom');
                break;

            case 'left':
                top = rect.top + rect.height / 2 - tooltipHeight / 2;
                left = rect.left - tooltipWidth - gap;
                tooltip.classList.add('position-left');
                break;

            case 'right':
                top = rect.top + rect.height / 2 - tooltipHeight / 2;
                left = rect.right + gap;
                tooltip.classList.add('position-right');
                break;
        }

        // Keep within viewport
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        top = Math.max(gap, Math.min(vh - tooltipHeight - gap, top));
        left = Math.max(gap, Math.min(vw - tooltipWidth - gap, left));

        tooltip.style.top = `${top}px`;
        tooltip.style.left = `${left}px`;
    }

    /**
     * Cleanup tour elements
     */
    #cleanup() {
        this.#overlay?.remove();
        this.#spotlight?.remove();
        document.querySelector('.tour-tooltip')?.remove();

        this.#overlay = null;
        this.#spotlight = null;
        this.#container = null;
    }

    /**
     * Check if tour should auto-start
     * @returns {boolean}
     */
    shouldAutoStart() {
        return !this.storage.get('tourCompleted');
    }

    /**
     * Reset tour completion status
     */
    reset() {
        this.storage.remove('tourCompleted');
        this.storage.remove('tourCompletedAt');
    }

    /**
     * Inject tour styles
     */
    #injectStyles() {
        if (document.getElementById('tour-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'tour-styles';
        styles.textContent = `
            .tour-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.75);
                z-index: 9998;
                pointer-events: none;
            }

            .tour-spotlight {
                position: fixed;
                border-radius: var(--radius-lg);
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.75);
                z-index: 9999;
                pointer-events: none;
                transition: all var(--duration-300) var(--ease-out);
            }

            .tour-tooltip {
                position: fixed;
                width: 300px;
                background: var(--color-bg-elevated);
                border: 1px solid var(--color-border);
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-lg);
                z-index: 10000;
                opacity: 0;
                transform: translateY(10px);
                transition: all var(--duration-300) var(--ease-out);
            }

            .tour-tooltip.visible {
                opacity: 1;
                transform: translateY(0);
            }

            .tour-tooltip.centered {
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%);
            }

            .tour-tooltip.centered.visible {
                transform: translate(-50%, -50%);
            }

            .tour-tooltip-content {
                padding: var(--space-4);
            }

            .tour-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: var(--space-2);
            }

            .tour-header h4 {
                margin: 0;
                font-size: var(--text-lg);
                color: var(--color-accent);
            }

            .tour-progress {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            .tour-tooltip p {
                margin: 0 0 var(--space-4) 0;
                font-size: var(--text-sm);
                color: var(--color-text-secondary);
                line-height: 1.5;
            }

            .tour-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .tour-skip {
                background: none;
                border: none;
                color: var(--color-text-tertiary);
                font-size: var(--text-sm);
                cursor: pointer;
                padding: var(--space-2);
            }

            .tour-skip:hover {
                color: var(--color-text-secondary);
            }

            .tour-nav {
                display: flex;
                gap: var(--space-2);
            }

            .tour-prev, .tour-next {
                padding: var(--space-2) var(--space-3);
                border-radius: var(--radius-md);
                font-size: var(--text-sm);
                cursor: pointer;
                transition: all var(--duration-150);
            }

            .tour-prev {
                background: var(--color-bg-tertiary);
                border: 1px solid var(--color-border);
                color: var(--color-text-secondary);
            }

            .tour-prev:hover {
                background: var(--color-bg-secondary);
            }

            .tour-next {
                background: var(--color-accent);
                border: none;
                color: var(--color-bg-primary);
                font-weight: 500;
            }

            .tour-next:hover {
                background: var(--color-accent-hover);
            }

            .tour-arrow {
                position: absolute;
                width: 12px;
                height: 12px;
                background: var(--color-bg-elevated);
                border: 1px solid var(--color-border);
                transform: rotate(45deg);
            }

            .tour-tooltip.position-top .tour-arrow {
                bottom: -7px;
                left: 50%;
                margin-left: -6px;
                border-top: none;
                border-left: none;
            }

            .tour-tooltip.position-bottom .tour-arrow {
                top: -7px;
                left: 50%;
                margin-left: -6px;
                border-bottom: none;
                border-right: none;
            }

            .tour-tooltip.position-left .tour-arrow {
                right: -7px;
                top: 50%;
                margin-top: -6px;
                border-bottom: none;
                border-left: none;
            }

            .tour-tooltip.position-right .tour-arrow {
                left: -7px;
                top: 50%;
                margin-top: -6px;
                border-top: none;
                border-right: none;
            }

            .tour-tooltip.centered .tour-arrow {
                display: none;
            }
        `;

        document.head.appendChild(styles);
    }
}

export { Tour };
