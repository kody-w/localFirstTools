/**
 * Tool Card - Renders individual tool cards
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { SearchController } from '../search/search-controller.js';

class ToolCard {
    /**
     * Create a tool card
     * @param {Object} tool - Tool data
     * @param {Object} options - Rendering options
     */
    constructor(tool, options = {}) {
        this.tool = tool;
        this.options = {
            showPreview: true,
            showActions: true,
            showTags: true,
            maxTags: 3,
            highlighted: false,
            ...options
        };

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
        this.searchController = SearchController.getInstance();

        this.element = null;
    }

    /**
     * Render the tool card
     * @returns {HTMLElement}
     */
    render() {
        const element = document.createElement('article');
        element.className = this.#getCardClasses();
        element.dataset.toolId = this.tool.id;
        element.innerHTML = this.#getCardHTML();

        this.element = element;
        this.#bindEvents();

        return element;
    }

    /**
     * Get card CSS classes
     * @returns {string}
     */
    #getCardClasses() {
        const classes = ['tool-card'];

        if (this.#isPinned()) {
            classes.push('pinned');
        }

        if (this.tool.featured) {
            classes.push('featured');
        }

        if (this.options.highlighted) {
            classes.push('highlighted');
        }

        return classes.join(' ');
    }

    /**
     * Check if tool is pinned
     * @returns {boolean}
     */
    #isPinned() {
        const user = this.state.getSlice('user');
        return user.pinnedTools.includes(this.tool.id);
    }

    /**
     * Get card HTML
     * @returns {string}
     */
    #getCardHTML() {
        const category = this.toolRepo.getCategory(this.tool.category);
        const isPinned = this.#isPinned();
        const title = this.#highlightText(this.tool.title);
        const description = this.#highlightText(this.tool.description || 'No description available');

        return `
            <div class="tool-card-header">
                <span class="tool-category" style="--cat-color: ${category?.color || '#888'}">
                    ${category?.icon || '📦'} ${category?.title || this.tool.category}
                </span>
                <button class="pin-btn ${isPinned ? 'active' : ''}"
                        data-action="pin"
                        aria-label="${isPinned ? 'Unpin' : 'Pin'} ${this.tool.title}"
                        aria-pressed="${isPinned}">
                    ${this.#getPinIcon(isPinned)}
                </button>
            </div>

            <div class="tool-card-content">
                <h3 class="tool-title">${title}</h3>
                <p class="tool-description">${description}</p>
            </div>

            ${this.options.showTags ? this.#renderTags() : ''}

            <div class="tool-card-meta">
                ${this.#renderComplexityBadge()}
                ${this.tool.featured ? '<span class="featured-badge">Featured</span>' : ''}
            </div>

            ${this.options.showActions ? this.#renderActions() : ''}
        `;
    }

    /**
     * Highlight search terms in text
     * @param {string} text
     * @returns {string}
     */
    #highlightText(text) {
        if (!text) return '';
        return this.searchController.highlight(text);
    }

    /**
     * Get pin icon SVG
     * @param {boolean} isPinned
     * @returns {string}
     */
    #getPinIcon(isPinned) {
        return `
            <svg width="16" height="16" viewBox="0 0 24 24"
                 fill="${isPinned ? 'currentColor' : 'none'}"
                 stroke="currentColor" stroke-width="2">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
        `;
    }

    /**
     * Render tags
     * @returns {string}
     */
    #renderTags() {
        if (!this.tool.tags || this.tool.tags.length === 0) {
            return '';
        }

        const visibleTags = this.tool.tags.slice(0, this.options.maxTags);
        const remainingCount = this.tool.tags.length - visibleTags.length;

        const tagHTML = visibleTags.map(tag => `
            <button class="tag-badge clickable" data-action="filter-tag" data-tag="${tag}">
                ${tag}
            </button>
        `).join('');

        const moreHTML = remainingCount > 0
            ? `<span class="tag-badge">+${remainingCount}</span>`
            : '';

        return `
            <div class="tool-card-tags">
                ${tagHTML}${moreHTML}
            </div>
        `;
    }

    /**
     * Render complexity badge
     * @returns {string}
     */
    #renderComplexityBadge() {
        const complexity = this.tool.complexity || 'intermediate';
        return `
            <span class="complexity-badge complexity-${complexity}">
                ${this.#getComplexityDots(complexity)}
                ${complexity}
            </span>
        `;
    }

    /**
     * Get complexity dots
     * @param {string} complexity
     * @returns {string}
     */
    #getComplexityDots(complexity) {
        const levels = { simple: 1, intermediate: 2, advanced: 3 };
        const level = levels[complexity] || 2;
        let dots = '';

        for (let i = 1; i <= 3; i++) {
            dots += `<span class="complexity-dot ${i <= level ? 'filled' : ''}"></span>`;
        }

        return `<span class="complexity-dots">${dots}</span>`;
    }

    /**
     * Render action buttons
     * @returns {string}
     */
    #renderActions() {
        return `
            <div class="tool-card-actions">
                <a href="../${this.tool.path}"
                   class="btn btn-primary tool-open-btn"
                   data-action="open"
                   target="_blank"
                   rel="noopener">
                    Open Tool
                </a>
                ${this.options.showPreview ? `
                    <button class="btn btn-secondary tool-preview-btn"
                            data-action="preview"
                            aria-label="Preview ${this.tool.title}">
                        Preview
                    </button>
                ` : ''}
            </div>
        `;
    }

    /**
     * Bind event listeners
     */
    #bindEvents() {
        if (!this.element) return;

        // Use event delegation
        this.element.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]')?.dataset.action;

            switch (action) {
                case 'pin':
                    e.preventDefault();
                    this.#handlePin();
                    break;
                case 'preview':
                    e.preventDefault();
                    this.#handlePreview();
                    break;
                case 'open':
                    this.#handleOpen();
                    break;
                case 'filter-tag':
                    e.preventDefault();
                    const tag = e.target.dataset.tag;
                    this.#handleTagFilter(tag);
                    break;
            }
        });

        // Keyboard navigation
        this.element.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                if (e.target === this.element) {
                    e.preventDefault();
                    this.#handlePreview();
                }
            }
        });
    }

    /**
     * Handle pin toggle
     */
    #handlePin() {
        const user = this.state.getSlice('user');
        const pinnedTools = [...user.pinnedTools];
        const index = pinnedTools.indexOf(this.tool.id);

        if (index === -1) {
            pinnedTools.push(this.tool.id);
            this.events.emit(EVENTS.TOOL_PIN, { toolId: this.tool.id });
        } else {
            pinnedTools.splice(index, 1);
            this.events.emit(EVENTS.TOOL_UNPIN, { toolId: this.tool.id });
        }

        this.state.setSlice('user', { ...user, pinnedTools });
        this.#updatePinState();
    }

    /**
     * Update pin button state
     */
    #updatePinState() {
        if (!this.element) return;

        const isPinned = this.#isPinned();
        const pinBtn = this.element.querySelector('.pin-btn');

        if (pinBtn) {
            pinBtn.classList.toggle('active', isPinned);
            pinBtn.setAttribute('aria-pressed', isPinned.toString());
            pinBtn.setAttribute('aria-label', `${isPinned ? 'Unpin' : 'Pin'} ${this.tool.title}`);
            pinBtn.innerHTML = this.#getPinIcon(isPinned);
        }

        this.element.classList.toggle('pinned', isPinned);
    }

    /**
     * Handle preview
     */
    #handlePreview() {
        this.events.emit(EVENTS.TOOL_PREVIEW, {
            toolId: this.tool.id,
            tool: this.tool
        });
    }

    /**
     * Handle open
     */
    #handleOpen() {
        const user = this.state.getSlice('user');
        const usage = { ...user.usage };
        usage[this.tool.id] = (usage[this.tool.id] || 0) + 1;

        const recentlyOpened = [
            this.tool.id,
            ...user.recentlyOpened.filter(id => id !== this.tool.id)
        ].slice(0, 10);

        this.state.setSlice('user', { ...user, usage, recentlyOpened });
        this.events.emit(EVENTS.TOOL_OPEN, { toolId: this.tool.id });
    }

    /**
     * Handle tag filter
     * @param {string} tag
     */
    #handleTagFilter(tag) {
        this.searchController.search(`tag:${tag}`, true);
    }

    /**
     * Update the card with new tool data
     * @param {Object} tool
     */
    update(tool) {
        this.tool = tool;
        if (this.element) {
            this.element.className = this.#getCardClasses();
            this.element.innerHTML = this.#getCardHTML();
            this.#bindEvents();
        }
    }

    /**
     * Destroy the card and clean up
     */
    destroy() {
        if (this.element) {
            this.element.remove();
            this.element = null;
        }
    }
}

/**
 * Factory function to create tool cards
 * @param {Object} tool
 * @param {Object} options
 * @returns {HTMLElement}
 */
export function createToolCard(tool, options = {}) {
    const card = new ToolCard(tool, options);
    return card.render();
}

export { ToolCard };
