/**
 * Recommendations - "You might also like" suggestions
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { ToolRepository } from '../data/tool-repository.js';
import { StorageManager } from '../storage/storage-manager.js';
import { AnalyticsTracker } from './analytics/tracker.js';

class Recommendations {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {Recommendations}
     */
    static getInstance() {
        if (!Recommendations.#instance) {
            Recommendations.#instance = new Recommendations();
        }
        return Recommendations.#instance;
    }

    constructor() {
        if (Recommendations.#instance) {
            return Recommendations.#instance;
        }

        this.events = EventBus.getInstance();
        this.toolRepo = ToolRepository.getInstance();
        this.storage = StorageManager.getInstance();
        this.analytics = AnalyticsTracker.getInstance();
    }

    /**
     * Get recommendations for a specific tool
     * @param {string} toolId
     * @param {number} limit
     * @returns {Array}
     */
    getForTool(toolId, limit = 5) {
        const tool = this.toolRepo.getById(toolId);
        if (!tool) return [];

        const allTools = this.toolRepo.getAll();
        const scored = [];

        for (const candidate of allTools) {
            if (candidate.id === toolId) continue;

            const score = this.#calculateSimilarity(tool, candidate);
            if (score > 0) {
                scored.push({ tool: candidate, score });
            }
        }

        // Sort by score descending and take top N
        return scored
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map(s => s.tool);
    }

    /**
     * Get personalized recommendations based on user behavior
     * @param {number} limit
     * @returns {Array}
     */
    getPersonalized(limit = 10) {
        const mostUsed = this.analytics.getMostUsedTools(5);
        const favoriteCategories = this.analytics.getFavoriteCategories();
        const pinnedTools = this.storage.get('pinnedTools') || [];

        const allTools = this.toolRepo.getAll();
        const usedToolIds = new Set(mostUsed.map(t => t.id));
        const pinnedSet = new Set(pinnedTools);

        const scored = [];

        for (const tool of allTools) {
            // Skip already used and pinned tools
            if (usedToolIds.has(tool.id) || pinnedSet.has(tool.id)) continue;

            let score = 0;

            // Boost if in favorite category
            if (favoriteCategories.includes(tool.category)) {
                const categoryIndex = favoriteCategories.indexOf(tool.category);
                score += (5 - categoryIndex) * 10;
            }

            // Boost featured and polished tools
            if (tool.featured) score += 15;
            if (tool.polished) score += 10;

            // Calculate similarity to used tools
            for (const usedTool of mostUsed) {
                const usedToolData = this.toolRepo.getById(usedTool.id);
                if (usedToolData) {
                    score += this.#calculateSimilarity(usedToolData, tool) * 0.5;
                }
            }

            if (score > 0) {
                scored.push({ tool, score });
            }
        }

        return scored
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map(s => s.tool);
    }

    /**
     * Get trending tools (most used recently)
     * @param {number} limit
     * @returns {Array}
     */
    getTrending(limit = 10) {
        const recentlyUsed = this.analytics.getRecentlyUsedTools(20);
        const toolIds = recentlyUsed.map(t => t.id);

        // Count occurrences and weight by recency
        const counts = new Map();

        toolIds.forEach((id, index) => {
            const weight = 1 + (20 - index) / 20; // Higher weight for more recent
            counts.set(id, (counts.get(id) || 0) + weight);
        });

        return Array.from(counts.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, limit)
            .map(([id]) => this.toolRepo.getById(id))
            .filter(Boolean);
    }

    /**
     * Get featured tools the user hasn't seen
     * @param {number} limit
     * @returns {Array}
     */
    getFeaturedUnseen(limit = 5) {
        const usedToolIds = new Set(
            this.analytics.getMostUsedTools(50).map(t => t.id)
        );

        return this.toolRepo.getAll()
            .filter(tool => tool.featured && !usedToolIds.has(tool.id))
            .slice(0, limit);
    }

    /**
     * Get tools similar to pinned tools
     * @param {number} limit
     * @returns {Array}
     */
    getBasedOnPins(limit = 10) {
        const pinnedTools = this.storage.get('pinnedTools') || [];
        if (pinnedTools.length === 0) return [];

        const recommendations = new Map();

        for (const pinnedId of pinnedTools) {
            const similar = this.getForTool(pinnedId, 5);

            for (const tool of similar) {
                if (pinnedTools.includes(tool.id)) continue;

                const existing = recommendations.get(tool.id) || { tool, score: 0 };
                existing.score += 1;
                recommendations.set(tool.id, existing);
            }
        }

        return Array.from(recommendations.values())
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map(r => r.tool);
    }

    /**
     * Get "discover something new" recommendations
     * Random tools from categories user hasn't explored
     * @param {number} limit
     * @returns {Array}
     */
    getDiscovery(limit = 5) {
        const favoriteCategories = new Set(this.analytics.getFavoriteCategories());
        const allCategories = this.toolRepo.getCategories();

        // Find unexplored categories
        const unexplored = allCategories.filter(cat => !favoriteCategories.has(cat.id));

        if (unexplored.length === 0) {
            // User has explored all categories, return random featured tools
            return this.#getRandomFeatured(limit);
        }

        const recommendations = [];

        for (const category of unexplored) {
            const categoryTools = this.toolRepo.getByCategory(category.id);
            const featured = categoryTools.filter(t => t.featured || t.polished);

            if (featured.length > 0) {
                recommendations.push(featured[Math.floor(Math.random() * featured.length)]);
            } else if (categoryTools.length > 0) {
                recommendations.push(categoryTools[Math.floor(Math.random() * categoryTools.length)]);
            }

            if (recommendations.length >= limit) break;
        }

        return recommendations;
    }

    /**
     * Get random featured tools
     * @param {number} limit
     * @returns {Array}
     */
    #getRandomFeatured(limit) {
        const featured = this.toolRepo.getAll().filter(t => t.featured);
        const shuffled = [...featured].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, limit);
    }

    /**
     * Calculate similarity between two tools
     * @param {Object} tool1
     * @param {Object} tool2
     * @returns {number}
     */
    #calculateSimilarity(tool1, tool2) {
        let score = 0;

        // Same category
        if (tool1.category === tool2.category) {
            score += 30;
        }

        // Same complexity
        if (tool1.complexity === tool2.complexity) {
            score += 10;
        }

        // Same interaction type
        if (tool1.interactionType === tool2.interactionType) {
            score += 15;
        }

        // Shared tags
        const tags1 = new Set(tool1.tags || []);
        const tags2 = new Set(tool2.tags || []);
        let sharedTags = 0;

        for (const tag of tags1) {
            if (tags2.has(tag)) sharedTags++;
        }

        score += sharedTags * 5;

        // Both featured
        if (tool1.featured && tool2.featured) {
            score += 5;
        }

        // Both polished
        if (tool1.polished && tool2.polished) {
            score += 5;
        }

        return score;
    }

    /**
     * Get all recommendation types as a combined list
     * @returns {Object}
     */
    getAllRecommendations() {
        return {
            personalized: this.getPersonalized(5),
            trending: this.getTrending(5),
            featuredUnseen: this.getFeaturedUnseen(3),
            basedOnPins: this.getBasedOnPins(5),
            discovery: this.getDiscovery(3)
        };
    }

    /**
     * Render recommendations widget
     * @param {HTMLElement} container
     * @param {string} type - Type of recommendations to show
     */
    render(container, type = 'personalized') {
        let tools = [];
        let title = '';

        switch (type) {
            case 'personalized':
                tools = this.getPersonalized(5);
                title = 'Recommended for You';
                break;
            case 'trending':
                tools = this.getTrending(5);
                title = 'Trending Now';
                break;
            case 'discovery':
                tools = this.getDiscovery(5);
                title = 'Discover Something New';
                break;
            case 'pins':
                tools = this.getBasedOnPins(5);
                title = 'Based on Your Pins';
                break;
            default:
                tools = this.getPersonalized(5);
                title = 'Recommended';
        }

        if (tools.length === 0) {
            container.innerHTML = '';
            return;
        }

        container.innerHTML = `
            <div class="recommendations-widget">
                <h3 class="recommendations-title">${title}</h3>
                <div class="recommendations-list">
                    ${tools.map(tool => `
                        <div class="recommendation-item" data-tool-id="${tool.id}">
                            <div class="recommendation-info">
                                <span class="recommendation-name">${tool.title}</span>
                                <span class="recommendation-category">${this.#formatCategory(tool.category)}</span>
                            </div>
                            <button class="btn btn-icon btn-sm" title="Preview">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M9 18l6-6-6-6"/>
                                </svg>
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        // Bind click events
        container.querySelectorAll('.recommendation-item').forEach(item => {
            item.addEventListener('click', () => {
                const toolId = item.dataset.toolId;
                this.events.emit(EVENTS.TOOL_PREVIEW, { toolId });
            });
        });
    }

    /**
     * Format category name
     * @param {string} category
     * @returns {string}
     */
    #formatCategory(category) {
        if (!category) return '';
        return category.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    }
}

export { Recommendations };
