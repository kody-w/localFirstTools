/**
 * Timeline View - Tools organized by date
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { createToolCard } from '../renderers/tool-card.js';

class TimelineView {
    constructor() {
        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#tools = [];
    }

    #container;
    #tools;

    /**
     * Initialize the timeline view
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;
        this.#container.className = 'timeline-view-container';
        this.#injectStyles();
    }

    /**
     * Render tools as a timeline
     * @param {Array} tools
     */
    render(tools) {
        this.#tools = tools;

        if (!this.#container) return;

        if (tools.length === 0) {
            this.#renderEmptyState();
            return;
        }

        // Group tools by date
        const groups = this.#groupByDate(tools);

        this.#container.innerHTML = `
            <div class="timeline">
                ${groups.map(group => this.#renderGroup(group)).join('')}
            </div>
        `;

        this.#bindEvents();
    }

    /**
     * Group tools by date periods
     * @param {Array} tools
     * @returns {Array}
     */
    #groupByDate(tools) {
        const now = new Date();
        const groups = {
            today: { label: 'Today', tools: [] },
            yesterday: { label: 'Yesterday', tools: [] },
            thisWeek: { label: 'This Week', tools: [] },
            thisMonth: { label: 'This Month', tools: [] },
            older: { label: 'Older', tools: [] },
            noDate: { label: 'No Date', tools: [] }
        };

        for (const tool of tools) {
            if (!tool.dateAdded) {
                groups.noDate.tools.push(tool);
                continue;
            }

            const date = new Date(tool.dateAdded);
            const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

            if (diffDays === 0) {
                groups.today.tools.push(tool);
            } else if (diffDays === 1) {
                groups.yesterday.tools.push(tool);
            } else if (diffDays < 7) {
                groups.thisWeek.tools.push(tool);
            } else if (diffDays < 30) {
                groups.thisMonth.tools.push(tool);
            } else {
                groups.older.tools.push(tool);
            }
        }

        // Return only non-empty groups
        return Object.values(groups).filter(g => g.tools.length > 0);
    }

    /**
     * Render a timeline group
     * @param {Object} group
     * @returns {string}
     */
    #renderGroup(group) {
        const toolsHTML = group.tools.map(tool => {
            const card = createToolCard(tool, { showPreview: false });
            return `<div class="timeline-item">${card.outerHTML}</div>`;
        }).join('');

        return `
            <div class="timeline-group">
                <div class="timeline-header">
                    <div class="timeline-dot"></div>
                    <h3 class="timeline-label">${group.label}</h3>
                    <span class="timeline-count">${group.tools.length} tools</span>
                </div>
                <div class="timeline-content">
                    <div class="timeline-tools">
                        ${toolsHTML}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render empty state
     */
    #renderEmptyState() {
        this.#container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                </div>
                <h3 class="empty-title">No tools found</h3>
                <p class="empty-description">No tools match your current filters</p>
            </div>
        `;
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        // Event delegation for tool cards is handled by the cards themselves
    }

    /**
     * Inject timeline-specific styles
     */
    #injectStyles() {
        if (document.getElementById('timeline-view-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'timeline-view-styles';
        styles.textContent = `
            .timeline-view-container {
                padding: var(--space-5);
            }

            .timeline {
                position: relative;
                max-width: 1200px;
                margin: 0 auto;
            }

            .timeline::before {
                content: '';
                position: absolute;
                left: 24px;
                top: 0;
                bottom: 0;
                width: 2px;
                background: var(--border-primary);
            }

            .timeline-group {
                position: relative;
                margin-bottom: var(--space-6);
            }

            .timeline-header {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                margin-bottom: var(--space-4);
                padding-left: 50px;
            }

            .timeline-dot {
                position: absolute;
                left: 17px;
                width: 16px;
                height: 16px;
                background: var(--color-accent);
                border: 3px solid var(--bg-primary);
                border-radius: 50%;
                box-shadow: 0 0 0 3px var(--color-accent);
            }

            .timeline-label {
                font-size: var(--text-lg);
                font-weight: var(--font-semibold);
                color: var(--text-primary);
            }

            .timeline-count {
                font-size: var(--text-sm);
                color: var(--text-tertiary);
                padding: var(--space-1) var(--space-3);
                background: var(--bg-tertiary);
                border-radius: var(--radius-full);
            }

            .timeline-content {
                padding-left: 50px;
            }

            .timeline-tools {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: var(--space-4);
            }

            .timeline-item {
                animation: timeline-fade-in var(--duration-300) var(--ease-out);
            }

            @keyframes timeline-fade-in {
                from {
                    opacity: 0;
                    transform: translateX(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            @media (max-width: 768px) {
                .timeline::before {
                    left: 12px;
                }

                .timeline-dot {
                    left: 5px;
                    width: 14px;
                    height: 14px;
                }

                .timeline-header,
                .timeline-content {
                    padding-left: 36px;
                }

                .timeline-tools {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    /**
     * Destroy the view
     */
    destroy() {
        this.#container = null;
        this.#tools = [];
    }
}

export { TimelineView };
