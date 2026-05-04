/**
 * Category Service - Category metadata and operations
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';

/**
 * Category definitions with metadata
 */
const CATEGORY_DEFINITIONS = {
    visual_art: {
        id: 'visual_art',
        name: 'Visual Art',
        description: 'Interactive visual experiences and design tools',
        icon: '🎨',
        color: '#FF6B6B',
        gradient: 'linear-gradient(135deg, #FF6B6B, #FF8E53)',
        order: 1
    },
    '3d_immersive': {
        id: '3d_immersive',
        name: '3D & Immersive',
        description: 'Three-dimensional and WebGL experiences',
        icon: '🌐',
        color: '#4ECDC4',
        gradient: 'linear-gradient(135deg, #4ECDC4, #44A08D)',
        order: 2
    },
    audio_music: {
        id: 'audio_music',
        name: 'Audio & Music',
        description: 'Sound synthesis and music creation tools',
        icon: '🎵',
        color: '#A78BFA',
        gradient: 'linear-gradient(135deg, #A78BFA, #8B5CF6)',
        order: 3
    },
    games_puzzles: {
        id: 'games_puzzles',
        name: 'Games & Puzzles',
        description: 'Interactive games and playful experiences',
        icon: '🎮',
        color: '#F472B6',
        gradient: 'linear-gradient(135deg, #F472B6, #EC4899)',
        order: 4
    },
    experimental_ai: {
        id: 'experimental_ai',
        name: 'Experimental AI',
        description: 'AI-powered interfaces and cutting-edge demos',
        icon: '🤖',
        color: '#60A5FA',
        gradient: 'linear-gradient(135deg, #60A5FA, #3B82F6)',
        order: 5
    },
    creative_tools: {
        id: 'creative_tools',
        name: 'Creative Tools',
        description: 'Productivity and creative utilities',
        icon: '🛠️',
        color: '#34D399',
        gradient: 'linear-gradient(135deg, #34D399, #10B981)',
        order: 6
    },
    generative_art: {
        id: 'generative_art',
        name: 'Generative Art',
        description: 'Algorithmic art generation systems',
        icon: '✨',
        color: '#FBBF24',
        gradient: 'linear-gradient(135deg, #FBBF24, #F59E0B)',
        order: 7
    },
    particle_physics: {
        id: 'particle_physics',
        name: 'Particle & Physics',
        description: 'Physics simulations and particle systems',
        icon: '⚛️',
        color: '#FB7185',
        gradient: 'linear-gradient(135deg, #FB7185, #F43F5E)',
        order: 8
    },
    educational_tools: {
        id: 'educational_tools',
        name: 'Educational',
        description: 'Learning resources and tutorials',
        icon: '📚',
        color: '#38BDF8',
        gradient: 'linear-gradient(135deg, #38BDF8, #0EA5E9)',
        order: 9
    },
    uncategorized: {
        id: 'uncategorized',
        name: 'Uncategorized',
        description: 'Tools awaiting categorization',
        icon: '📦',
        color: '#94A3B8',
        gradient: 'linear-gradient(135deg, #94A3B8, #64748B)',
        order: 99
    }
};

class CategoryService {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {CategoryService}
     */
    static getInstance() {
        if (!CategoryService.#instance) {
            CategoryService.#instance = new CategoryService();
        }
        return CategoryService.#instance;
    }

    constructor() {
        if (CategoryService.#instance) {
            return CategoryService.#instance;
        }

        this.events = EventBus.getInstance();
        this.#categories = new Map();
        this.#toolCounts = new Map();

        this.#initialize();
    }

    #categories;
    #toolCounts;

    /**
     * Initialize category service
     */
    #initialize() {
        // Load category definitions
        for (const [id, definition] of Object.entries(CATEGORY_DEFINITIONS)) {
            this.#categories.set(id, { ...definition });
        }
    }

    /**
     * Get all categories
     * @returns {Array}
     */
    getAll() {
        return Array.from(this.#categories.values())
            .sort((a, b) => a.order - b.order);
    }

    /**
     * Get category by ID
     * @param {string} id
     * @returns {Object|null}
     */
    get(id) {
        return this.#categories.get(id) || this.#categories.get('uncategorized');
    }

    /**
     * Get category name
     * @param {string} id
     * @returns {string}
     */
    getName(id) {
        return this.get(id)?.name || 'Uncategorized';
    }

    /**
     * Get category icon
     * @param {string} id
     * @returns {string}
     */
    getIcon(id) {
        return this.get(id)?.icon || '📦';
    }

    /**
     * Get category color
     * @param {string} id
     * @returns {string}
     */
    getColor(id) {
        return this.get(id)?.color || '#94A3B8';
    }

    /**
     * Get category gradient
     * @param {string} id
     * @returns {string}
     */
    getGradient(id) {
        return this.get(id)?.gradient || 'linear-gradient(135deg, #94A3B8, #64748B)';
    }

    /**
     * Update tool counts for categories
     * @param {Array} tools
     */
    updateCounts(tools) {
        this.#toolCounts.clear();

        for (const tool of tools) {
            const category = tool.category || 'uncategorized';
            const current = this.#toolCounts.get(category) || 0;
            this.#toolCounts.set(category, current + 1);
        }

        this.events.emit(EVENTS.CATEGORY_COUNTS_UPDATED, {
            counts: Object.fromEntries(this.#toolCounts)
        });
    }

    /**
     * Get tool count for category
     * @param {string} id
     * @returns {number}
     */
    getCount(id) {
        return this.#toolCounts.get(id) || 0;
    }

    /**
     * Get all counts
     * @returns {Object}
     */
    getAllCounts() {
        return Object.fromEntries(this.#toolCounts);
    }

    /**
     * Get categories with tools
     * @returns {Array}
     */
    getCategoriesWithTools() {
        return this.getAll().filter(cat => this.getCount(cat.id) > 0);
    }

    /**
     * Get category statistics
     * @returns {Object}
     */
    getStatistics() {
        const total = Array.from(this.#toolCounts.values()).reduce((a, b) => a + b, 0);
        const categorized = total - (this.#toolCounts.get('uncategorized') || 0);

        return {
            totalCategories: this.#categories.size,
            activeCategories: this.getCategoriesWithTools().length,
            totalTools: total,
            categorizedTools: categorized,
            categorizationRate: total > 0 ? (categorized / total * 100).toFixed(1) : 0
        };
    }

    /**
     * Search categories
     * @param {string} query
     * @returns {Array}
     */
    search(query) {
        if (!query) return this.getAll();

        const queryLower = query.toLowerCase();
        return this.getAll().filter(cat =>
            cat.name.toLowerCase().includes(queryLower) ||
            cat.description.toLowerCase().includes(queryLower)
        );
    }

    /**
     * Get category CSS variables
     * @param {string} id
     * @returns {Object}
     */
    getCSSVariables(id) {
        const cat = this.get(id);
        return {
            '--category-color': cat.color,
            '--category-gradient': cat.gradient,
            '--category-icon': `"${cat.icon}"`
        };
    }

    /**
     * Render category badge
     * @param {string} id
     * @returns {string}
     */
    renderBadge(id) {
        const cat = this.get(id);
        return `
            <span class="category-badge" style="background: ${cat.gradient}">
                <span class="category-icon">${cat.icon}</span>
                <span class="category-name">${cat.name}</span>
            </span>
        `;
    }

    /**
     * Render category card
     * @param {string} id
     * @param {Object} options
     * @returns {string}
     */
    renderCard(id, options = {}) {
        const cat = this.get(id);
        const count = this.getCount(id);

        return `
            <div class="category-card" data-category="${id}" style="background: ${cat.gradient}">
                <div class="category-card-icon">${cat.icon}</div>
                <div class="category-card-content">
                    <h3 class="category-card-title">${cat.name}</h3>
                    <p class="category-card-description">${cat.description}</p>
                    ${options.showCount !== false ? `<span class="category-card-count">${count} tool${count !== 1 ? 's' : ''}</span>` : ''}
                </div>
            </div>
        `;
    }
}

export { CategoryService, CATEGORY_DEFINITIONS };
