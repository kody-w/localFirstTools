/**
 * Section Renderer - Renders tool sections (Pinned, Featured, Regular)
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { createToolCard } from './tool-card.js';

/**
 * @typedef {Object} Section
 * @property {string} id - Section identifier
 * @property {string} title - Section title
 * @property {string} [icon] - Section icon
 * @property {Array} tools - Tools in this section
 * @property {boolean} [collapsible] - Can section be collapsed
 * @property {boolean} [collapsed] - Is section collapsed
 */

class SectionRenderer {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SectionRenderer}
     */
    static getInstance() {
        if (!SectionRenderer.#instance) {
            SectionRenderer.#instance = new SectionRenderer();
        }
        return SectionRenderer.#instance;
    }

    constructor() {
        if (SectionRenderer.#instance) {
            throw new Error('Use SectionRenderer.getInstance() instead of new SectionRenderer()');
        }

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();

        this.#container = null;
        this.#sections = [];
        this.#collapsedSections = new Set();
    }

    #container;
    #sections;
    #collapsedSections;

    /**
     * Initialize the section renderer
     * @param {HTMLElement} container
     */
    initialize(container) {
        this.#container = container;

        // Subscribe to state changes
        this.state.subscribeToSlice('filteredTools', (tools) => {
            this.render(tools);
        });
    }

    /**
     * Render tools in sections
     * @param {Array} tools
     * @param {Object} options
     */
    render(tools, options = {}) {
        const {
            groupByCategory = false,
            showPinnedSection = true,
            showFeaturedSection = true
        } = options;

        if (!this.#container) return;

        // Build sections
        this.#sections = this.#buildSections(tools, {
            groupByCategory,
            showPinnedSection,
            showFeaturedSection
        });

        // Render sections
        this.#container.innerHTML = '';

        if (this.#sections.length === 0) {
            this.#renderEmptyState();
            return;
        }

        const fragment = document.createDocumentFragment();

        for (const section of this.#sections) {
            const sectionEl = this.#renderSection(section);
            fragment.appendChild(sectionEl);
        }

        this.#container.appendChild(fragment);

        this.events.emit(EVENTS.VIEW_RENDERED, {
            sectionCount: this.#sections.length,
            toolCount: tools.length
        });
    }

    /**
     * Build sections from tools
     * @param {Array} tools
     * @param {Object} options
     * @returns {Section[]}
     */
    #buildSections(tools, options) {
        const sections = [];
        const user = this.state.getSlice('user');
        const pinnedSet = new Set(user.pinnedTools);

        // Separate pinned tools
        const pinnedTools = [];
        const unpinnedTools = [];

        for (const tool of tools) {
            if (pinnedSet.has(tool.id)) {
                pinnedTools.push(tool);
            } else {
                unpinnedTools.push(tool);
            }
        }

        // Pinned section
        if (options.showPinnedSection && pinnedTools.length > 0) {
            sections.push({
                id: 'pinned',
                title: 'Pinned',
                icon: '📌',
                tools: pinnedTools,
                collapsible: true,
                collapsed: this.#collapsedSections.has('pinned'),
                className: 'pinned-section'
            });
        }

        // Featured section
        if (options.showFeaturedSection) {
            const featuredTools = unpinnedTools.filter(t => t.featured);
            const regularTools = unpinnedTools.filter(t => !t.featured);

            if (featuredTools.length > 0) {
                sections.push({
                    id: 'featured',
                    title: 'Featured',
                    icon: '⭐',
                    tools: featuredTools,
                    collapsible: true,
                    collapsed: this.#collapsedSections.has('featured'),
                    className: 'featured-section'
                });
            }

            // Group remaining by category or as single section
            if (options.groupByCategory) {
                const byCategory = this.#groupByCategory(regularTools);
                sections.push(...byCategory);
            } else if (regularTools.length > 0) {
                sections.push({
                    id: 'all',
                    title: 'All Tools',
                    icon: '📦',
                    tools: regularTools,
                    collapsible: false,
                    collapsed: false
                });
            }
        } else {
            // No featured separation - group by category or show all
            if (options.groupByCategory) {
                const byCategory = this.#groupByCategory(unpinnedTools);
                sections.push(...byCategory);
            } else if (unpinnedTools.length > 0) {
                sections.push({
                    id: 'all',
                    title: 'All Tools',
                    icon: '📦',
                    tools: unpinnedTools,
                    collapsible: false,
                    collapsed: false
                });
            }
        }

        return sections;
    }

    /**
     * Group tools by category
     * @param {Array} tools
     * @returns {Section[]}
     */
    #groupByCategory(tools) {
        const groups = new Map();

        for (const tool of tools) {
            const category = tool.category || 'uncategorized';
            if (!groups.has(category)) {
                groups.set(category, []);
            }
            groups.get(category).push(tool);
        }

        const sections = [];

        for (const [categoryKey, categoryTools] of groups) {
            const category = this.toolRepo.getCategory(categoryKey);

            sections.push({
                id: `category-${categoryKey}`,
                title: category?.title || categoryKey,
                icon: category?.icon || '📁',
                tools: categoryTools,
                collapsible: true,
                collapsed: this.#collapsedSections.has(`category-${categoryKey}`),
                className: 'category-section',
                categoryKey
            });
        }

        // Sort by category title
        sections.sort((a, b) => a.title.localeCompare(b.title));

        return sections;
    }

    /**
     * Render a single section
     * @param {Section} section
     * @returns {HTMLElement}
     */
    #renderSection(section) {
        const sectionEl = document.createElement('section');
        sectionEl.className = `tools-section ${section.className || ''}`;
        sectionEl.dataset.sectionId = section.id;

        if (section.categoryKey) {
            sectionEl.dataset.category = section.categoryKey;
        }

        sectionEl.innerHTML = `
            <header class="section-header">
                <h2 class="section-title">
                    <span class="icon">${section.icon || ''}</span>
                    ${section.title}
                </h2>
                <div class="section-meta">
                    <span class="section-count">${section.tools.length}</span>
                    ${section.collapsible ? `
                        <button class="section-toggle"
                                aria-expanded="${!section.collapsed}"
                                aria-label="${section.collapsed ? 'Expand' : 'Collapse'} ${section.title}">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                 stroke="currentColor" stroke-width="2"
                                 class="${section.collapsed ? 'collapsed' : ''}">
                                <path d="M6 9l6 6 6-6"/>
                            </svg>
                        </button>
                    ` : ''}
                </div>
            </header>
            <div class="section-content ${section.collapsed ? 'collapsed' : ''}">
                <div class="tools-container">
                    <!-- Tools rendered here -->
                </div>
            </div>
        `;

        // Render tools
        const toolsContainer = sectionEl.querySelector('.tools-container');
        const fragment = document.createDocumentFragment();

        for (const tool of section.tools) {
            const card = createToolCard(tool);
            fragment.appendChild(card);
        }

        toolsContainer.appendChild(fragment);

        // Bind toggle
        if (section.collapsible) {
            const toggleBtn = sectionEl.querySelector('.section-toggle');
            toggleBtn?.addEventListener('click', () => {
                this.#toggleSection(section.id);
            });
        }

        return sectionEl;
    }

    /**
     * Toggle section collapsed state
     * @param {string} sectionId
     */
    #toggleSection(sectionId) {
        const isCollapsed = this.#collapsedSections.has(sectionId);

        if (isCollapsed) {
            this.#collapsedSections.delete(sectionId);
        } else {
            this.#collapsedSections.add(sectionId);
        }

        // Update DOM
        const sectionEl = this.#container.querySelector(`[data-section-id="${sectionId}"]`);
        if (sectionEl) {
            const content = sectionEl.querySelector('.section-content');
            const toggle = sectionEl.querySelector('.section-toggle');
            const svg = toggle?.querySelector('svg');

            content?.classList.toggle('collapsed', !isCollapsed);
            toggle?.setAttribute('aria-expanded', isCollapsed.toString());
            svg?.classList.toggle('collapsed', !isCollapsed);
        }
    }

    /**
     * Render empty state
     */
    #renderEmptyState() {
        this.#container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="1.5">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                </div>
                <h2 class="empty-title">No tools found</h2>
                <p class="empty-description">Try adjusting your filters or search terms</p>
                <button class="btn btn-primary" id="reset-filters-btn">Clear Filters</button>
            </div>
        `;

        const resetBtn = this.#container.querySelector('#reset-filters-btn');
        resetBtn?.addEventListener('click', () => {
            this.events.emit(EVENTS.FILTERS_RESET);
        });
    }

    /**
     * Expand all sections
     */
    expandAll() {
        this.#collapsedSections.clear();
        this.#updateAllSectionStates();
    }

    /**
     * Collapse all sections
     */
    collapseAll() {
        for (const section of this.#sections) {
            if (section.collapsible) {
                this.#collapsedSections.add(section.id);
            }
        }
        this.#updateAllSectionStates();
    }

    /**
     * Update all section collapsed states in DOM
     */
    #updateAllSectionStates() {
        for (const section of this.#sections) {
            const sectionEl = this.#container.querySelector(`[data-section-id="${section.id}"]`);
            if (sectionEl) {
                const isCollapsed = this.#collapsedSections.has(section.id);
                const content = sectionEl.querySelector('.section-content');
                const toggle = sectionEl.querySelector('.section-toggle');

                content?.classList.toggle('collapsed', isCollapsed);
                toggle?.setAttribute('aria-expanded', (!isCollapsed).toString());
            }
        }
    }

    /**
     * Get section by ID
     * @param {string} sectionId
     * @returns {Section|null}
     */
    getSection(sectionId) {
        return this.#sections.find(s => s.id === sectionId) || null;
    }

    /**
     * Get all sections
     * @returns {Section[]}
     */
    getAllSections() {
        return [...this.#sections];
    }

    /**
     * Destroy the renderer
     */
    destroy() {
        this.#container = null;
        this.#sections = [];
        this.#collapsedSections.clear();
    }
}

export { SectionRenderer };
