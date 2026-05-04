/**
 * Tool Comparison - Compare tools side by side
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { StorageManager } from '../storage/storage-manager.js';

class ToolComparison {
    constructor() {
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
        this.storage = StorageManager.getInstance();

        this.#container = null;
        this.#selectedTools = [];
        this.#maxTools = 4;
        this.#isVisible = false;
    }

    #container;
    #selectedTools;
    #maxTools;
    #isVisible;

    /**
     * Add tool to comparison
     * @param {string} toolId
     * @returns {boolean}
     */
    addTool(toolId) {
        if (this.#selectedTools.includes(toolId)) return false;
        if (this.#selectedTools.length >= this.#maxTools) {
            this.events.emit(EVENTS.NOTIFICATION, {
                message: `Maximum ${this.#maxTools} tools can be compared`,
                type: 'warning'
            });
            return false;
        }

        this.#selectedTools.push(toolId);
        this.events.emit(EVENTS.COMPARISON_CHANGE, { tools: this.#selectedTools });

        if (this.#isVisible) {
            this.#render();
        }

        return true;
    }

    /**
     * Remove tool from comparison
     * @param {string} toolId
     */
    removeTool(toolId) {
        const index = this.#selectedTools.indexOf(toolId);
        if (index > -1) {
            this.#selectedTools.splice(index, 1);
            this.events.emit(EVENTS.COMPARISON_CHANGE, { tools: this.#selectedTools });

            if (this.#isVisible) {
                this.#render();
            }
        }
    }

    /**
     * Clear all selected tools
     */
    clear() {
        this.#selectedTools = [];
        this.events.emit(EVENTS.COMPARISON_CHANGE, { tools: [] });

        if (this.#isVisible) {
            this.#render();
        }
    }

    /**
     * Get selected tools
     * @returns {Array}
     */
    getSelectedTools() {
        return [...this.#selectedTools];
    }

    /**
     * Show comparison modal
     * @param {HTMLElement} parentContainer
     */
    show(parentContainer) {
        if (this.#selectedTools.length < 2) {
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Select at least 2 tools to compare',
                type: 'info'
            });
            return;
        }

        this.#container = document.createElement('div');
        this.#container.className = 'comparison-modal';
        this.#render();

        parentContainer.appendChild(this.#container);
        this.#isVisible = true;

        this.#injectStyles();

        requestAnimationFrame(() => {
            this.#container.classList.add('visible');
        });
    }

    /**
     * Hide comparison modal
     */
    hide() {
        if (!this.#isVisible || !this.#container) return;

        this.#container.classList.remove('visible');

        setTimeout(() => {
            this.#container?.remove();
            this.#container = null;
            this.#isVisible = false;
        }, 300);
    }

    /**
     * Toggle comparison visibility
     * @param {HTMLElement} parentContainer
     */
    toggle(parentContainer) {
        if (this.#isVisible) {
            this.hide();
        } else {
            this.show(parentContainer);
        }
    }

    /**
     * Render comparison view
     */
    #render() {
        const tools = this.#selectedTools
            .map(id => this.toolRepo.getById(id))
            .filter(Boolean);

        if (tools.length === 0) {
            this.#container.innerHTML = `
                <div class="comparison-empty">
                    <p>No tools selected for comparison</p>
                    <button class="btn btn-secondary" id="close-comparison">Close</button>
                </div>
            `;
            this.#container.querySelector('#close-comparison')?.addEventListener('click', () => this.hide());
            return;
        }

        const attributes = this.#getComparisonAttributes();

        this.#container.innerHTML = `
            <div class="comparison-content">
                <div class="comparison-header">
                    <h2>Compare Tools</h2>
                    <button class="btn btn-icon comparison-close" aria-label="Close">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <div class="comparison-table-wrapper">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th class="attribute-column">Attribute</th>
                                ${tools.map(tool => `
                                    <th class="tool-column">
                                        <div class="tool-header">
                                            <span class="tool-name">${tool.title}</span>
                                            <button class="btn btn-icon btn-sm remove-tool" data-tool-id="${tool.id}" title="Remove">
                                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                                    <path d="M18 6L6 18M6 6l12 12"/>
                                                </svg>
                                            </button>
                                        </div>
                                    </th>
                                `).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${attributes.map(attr => `
                                <tr>
                                    <td class="attribute-name">${attr.label}</td>
                                    ${tools.map(tool => `
                                        <td class="attribute-value ${this.#getValueClass(attr.key, tool)}">
                                            ${this.#formatValue(attr.key, tool)}
                                        </td>
                                    `).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>

                <div class="comparison-actions">
                    <button class="btn btn-secondary" id="clear-comparison">
                        Clear All
                    </button>
                </div>
            </div>
        `;

        // Bind events
        this.#container.querySelector('.comparison-close')?.addEventListener('click', () => this.hide());

        this.#container.querySelector('#clear-comparison')?.addEventListener('click', () => {
            this.clear();
            this.hide();
        });

        this.#container.querySelectorAll('.remove-tool').forEach(btn => {
            btn.addEventListener('click', () => {
                const toolId = btn.dataset.toolId;
                this.removeTool(toolId);
            });
        });
    }

    /**
     * Get attributes for comparison
     * @returns {Array}
     */
    #getComparisonAttributes() {
        return [
            { key: 'category', label: 'Category' },
            { key: 'complexity', label: 'Complexity' },
            { key: 'interactionType', label: 'Type' },
            { key: 'featured', label: 'Featured' },
            { key: 'polished', label: 'Polished' },
            { key: 'tags', label: 'Tags' },
            { key: 'file', label: 'File Path' },
            { key: 'dateAdded', label: 'Date Added' }
        ];
    }

    /**
     * Format value for display
     * @param {string} key
     * @param {Object} tool
     * @returns {string}
     */
    #formatValue(key, tool) {
        const value = tool[key];

        switch (key) {
            case 'category':
                return this.#formatCategory(value);

            case 'complexity':
                return this.#formatComplexity(value);

            case 'interactionType':
                return this.#formatInteractionType(value);

            case 'featured':
            case 'polished':
                return value ? '✓ Yes' : '✗ No';

            case 'tags':
                if (!value || value.length === 0) return '-';
                return value.slice(0, 3).map(t => `<span class="tag">${t}</span>`).join('');

            case 'file':
                return value || '-';

            case 'dateAdded':
                return value ? new Date(value).toLocaleDateString() : 'Unknown';

            default:
                return value || '-';
        }
    }

    /**
     * Format category name
     * @param {string} category
     * @returns {string}
     */
    #formatCategory(category) {
        if (!category) return '-';
        return category
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase());
    }

    /**
     * Format complexity level
     * @param {string} complexity
     * @returns {string}
     */
    #formatComplexity(complexity) {
        const icons = {
            simple: '🟢 Simple',
            intermediate: '🟡 Intermediate',
            advanced: '🔴 Advanced'
        };
        return icons[complexity] || complexity || '-';
    }

    /**
     * Format interaction type
     * @param {string} type
     * @returns {string}
     */
    #formatInteractionType(type) {
        if (!type) return '-';
        return type.charAt(0).toUpperCase() + type.slice(1);
    }

    /**
     * Get CSS class for value
     * @param {string} key
     * @param {Object} tool
     * @returns {string}
     */
    #getValueClass(key, tool) {
        const value = tool[key];

        switch (key) {
            case 'featured':
            case 'polished':
                return value ? 'value-positive' : 'value-neutral';

            case 'complexity':
                if (value === 'simple') return 'value-positive';
                if (value === 'advanced') return 'value-warning';
                return 'value-neutral';

            default:
                return '';
        }
    }

    /**
     * Inject comparison styles
     */
    #injectStyles() {
        if (document.getElementById('comparison-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'comparison-styles';
        styles.textContent = `
            .comparison-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity var(--duration-300);
                z-index: 1000;
            }

            .comparison-modal.visible {
                opacity: 1;
            }

            .comparison-content {
                background: var(--color-bg-elevated);
                border-radius: var(--radius-xl);
                width: 90%;
                max-width: 1000px;
                max-height: 85vh;
                display: flex;
                flex-direction: column;
                transform: scale(0.95);
                transition: transform var(--duration-300);
            }

            .comparison-modal.visible .comparison-content {
                transform: scale(1);
            }

            .comparison-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4) var(--space-5);
                border-bottom: 1px solid var(--color-border);
            }

            .comparison-header h2 {
                margin: 0;
                font-size: var(--text-xl);
            }

            .comparison-table-wrapper {
                flex: 1;
                overflow: auto;
                padding: var(--space-4);
            }

            .comparison-table {
                width: 100%;
                border-collapse: collapse;
                font-size: var(--text-sm);
            }

            .comparison-table th,
            .comparison-table td {
                padding: var(--space-3);
                text-align: left;
                border-bottom: 1px solid var(--color-border-subtle);
            }

            .comparison-table th {
                background: var(--color-bg-tertiary);
                font-weight: 600;
                position: sticky;
                top: 0;
            }

            .attribute-column {
                width: 120px;
                min-width: 120px;
            }

            .tool-column {
                min-width: 150px;
            }

            .tool-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: var(--space-2);
            }

            .tool-name {
                font-weight: 600;
                color: var(--color-text-primary);
            }

            .attribute-name {
                color: var(--color-text-secondary);
                font-weight: 500;
            }

            .attribute-value {
                color: var(--color-text-primary);
            }

            .value-positive {
                color: var(--color-success);
            }

            .value-warning {
                color: var(--color-warning);
            }

            .value-neutral {
                color: var(--color-text-tertiary);
            }

            .attribute-value .tag {
                display: inline-block;
                padding: 2px 6px;
                background: var(--color-bg-tertiary);
                border-radius: var(--radius-sm);
                font-size: var(--text-xs);
                margin-right: 4px;
            }

            .comparison-actions {
                display: flex;
                justify-content: flex-end;
                gap: var(--space-3);
                padding: var(--space-4) var(--space-5);
                border-top: 1px solid var(--color-border);
            }

            .comparison-empty {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: var(--space-8);
                text-align: center;
            }

            .comparison-empty p {
                color: var(--color-text-secondary);
                margin-bottom: var(--space-4);
            }

            @media (max-width: 640px) {
                .comparison-content {
                    width: 100%;
                    height: 100%;
                    max-height: 100%;
                    border-radius: 0;
                }

                .attribute-column {
                    width: 80px;
                    min-width: 80px;
                }
            }
        `;

        document.head.appendChild(styles);
    }
}

export { ToolComparison };
