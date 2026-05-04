/**
 * Suggestion Engine - Autocomplete and search suggestions
 * Local First Tools v2
 */

import { ToolRepository } from '../data/tool-repository.js';
import { StateManager } from '../core/state-manager.js';
import { SearchParser } from '../filters/search-parser.js';
import { SEARCH_OPERATORS, SEARCH_FLAGS, LIMITS } from '../core/constants.js';

/**
 * @typedef {Object} Suggestion
 * @property {string} type - 'tool', 'tag', 'category', 'operator', 'history', 'recent'
 * @property {string} value - The suggestion value
 * @property {string} display - Display text
 * @property {string} [icon] - Optional icon
 * @property {number} [score] - Relevance score
 */

class SuggestionEngine {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SuggestionEngine}
     */
    static getInstance() {
        if (!SuggestionEngine.#instance) {
            SuggestionEngine.#instance = new SuggestionEngine();
        }
        return SuggestionEngine.#instance;
    }

    constructor() {
        if (SuggestionEngine.#instance) {
            throw new Error('Use SuggestionEngine.getInstance() instead of new SuggestionEngine()');
        }

        this.toolRepo = ToolRepository.getInstance();
        this.state = StateManager.getInstance();
        this.searchParser = SearchParser.getInstance();
    }

    /**
     * Get suggestions for a query
     * @param {string} query
     * @returns {Suggestion[]}
     */
    getSuggestions(query) {
        if (!query || query.trim() === '') {
            return this.#getEmptyQuerySuggestions();
        }

        const suggestions = [];
        const lastWord = query.split(/\s+/).pop() || '';

        // Operator suggestions
        suggestions.push(...this.#getOperatorSuggestions(lastWord));

        // Tool title suggestions
        suggestions.push(...this.#getToolSuggestions(query));

        // Tag suggestions
        suggestions.push(...this.#getTagSuggestions(lastWord));

        // Category suggestions
        suggestions.push(...this.#getCategorySuggestions(lastWord));

        // History suggestions
        suggestions.push(...this.#getHistorySuggestions(query));

        // Sort by score and dedupe
        return this.#processResults(suggestions);
    }

    /**
     * Get suggestions when query is empty
     * @returns {Suggestion[]}
     */
    #getEmptyQuerySuggestions() {
        const suggestions = [];
        const user = this.state.getSlice('user');

        // Recent searches
        const history = user.searchHistory || [];
        for (let i = 0; i < Math.min(3, history.length); i++) {
            suggestions.push({
                type: 'history',
                value: history[i],
                display: history[i],
                icon: '🕐',
                score: 100 - i
            });
        }

        // Recently opened tools
        const recentlyOpened = user.recentlyOpened || [];
        for (let i = 0; i < Math.min(3, recentlyOpened.length); i++) {
            const tool = this.toolRepo.getById(recentlyOpened[i]);
            if (tool) {
                suggestions.push({
                    type: 'recent',
                    value: tool.id,
                    display: tool.title,
                    icon: '📂',
                    score: 90 - i
                });
            }
        }

        // Popular operator hints
        suggestions.push({
            type: 'hint',
            value: 'tag:',
            display: 'tag: - Filter by tag',
            icon: '🏷️',
            score: 50
        });

        suggestions.push({
            type: 'hint',
            value: 'is:featured',
            display: 'is:featured - Show featured tools',
            icon: '⭐',
            score: 49
        });

        return this.#processResults(suggestions);
    }

    /**
     * Get operator suggestions
     * @param {string} prefix
     * @returns {Suggestion[]}
     */
    #getOperatorSuggestions(prefix) {
        const suggestions = [];

        for (const [operator, method] of Object.entries(SEARCH_OPERATORS)) {
            if (operator.startsWith(prefix.toLowerCase())) {
                suggestions.push({
                    type: 'operator',
                    value: operator,
                    display: `${operator} - ${this.#getOperatorLabel(method)}`,
                    icon: '🔍',
                    score: 80
                });
            }
        }

        // Flag value suggestions if typing is:
        if (prefix.toLowerCase().startsWith('is:')) {
            const flagPrefix = prefix.slice(3).toLowerCase();
            for (const flag of Object.values(SEARCH_FLAGS)) {
                if (flag.startsWith(flagPrefix)) {
                    suggestions.push({
                        type: 'flag',
                        value: `is:${flag}`,
                        display: `is:${flag}`,
                        icon: '🚩',
                        score: 85
                    });
                }
            }
        }

        return suggestions;
    }

    /**
     * Get tool title suggestions
     * @param {string} query
     * @returns {Suggestion[]}
     */
    #getToolSuggestions(query) {
        const suggestions = [];
        const normalizedQuery = query.toLowerCase();
        const tools = this.toolRepo.getAll();

        for (const tool of tools) {
            const titleLower = tool.title.toLowerCase();
            let score = 0;

            // Exact start match
            if (titleLower.startsWith(normalizedQuery)) {
                score = 100;
            }
            // Word start match
            else if (titleLower.split(/\s+/).some(w => w.startsWith(normalizedQuery))) {
                score = 80;
            }
            // Contains match
            else if (titleLower.includes(normalizedQuery)) {
                score = 60;
            }
            // Fuzzy match (initials)
            else if (this.#matchesInitials(tool.title, query)) {
                score = 40;
            }

            if (score > 0) {
                // Boost featured tools
                if (tool.featured) score += 10;

                suggestions.push({
                    type: 'tool',
                    value: tool.id,
                    display: tool.title,
                    icon: this.#getCategoryIcon(tool.category),
                    score,
                    metadata: {
                        category: tool.category,
                        featured: tool.featured
                    }
                });
            }
        }

        return suggestions;
    }

    /**
     * Get tag suggestions
     * @param {string} prefix
     * @returns {Suggestion[]}
     */
    #getTagSuggestions(prefix) {
        const suggestions = [];
        const normalizedPrefix = prefix.toLowerCase();
        const allTags = this.toolRepo.getAllTags();

        for (const tag of allTags) {
            if (tag.startsWith(normalizedPrefix)) {
                suggestions.push({
                    type: 'tag',
                    value: `tag:${tag}`,
                    display: `tag:${tag}`,
                    icon: '🏷️',
                    score: 70
                });
            }
        }

        return suggestions;
    }

    /**
     * Get category suggestions
     * @param {string} prefix
     * @returns {Suggestion[]}
     */
    #getCategorySuggestions(prefix) {
        const suggestions = [];
        const normalizedPrefix = prefix.toLowerCase();
        const categories = this.toolRepo.getCategoriesWithCounts();

        for (const category of categories) {
            if (category.title.toLowerCase().includes(normalizedPrefix) ||
                category.key.includes(normalizedPrefix)) {
                suggestions.push({
                    type: 'category',
                    value: `cat:${category.key}`,
                    display: `${category.icon} ${category.title} (${category.count})`,
                    icon: category.icon,
                    score: 65
                });
            }
        }

        return suggestions;
    }

    /**
     * Get history-based suggestions
     * @param {string} query
     * @returns {Suggestion[]}
     */
    #getHistorySuggestions(query) {
        const suggestions = [];
        const user = this.state.getSlice('user');
        const history = user.searchHistory || [];
        const normalizedQuery = query.toLowerCase();

        for (let i = 0; i < history.length; i++) {
            if (history[i].toLowerCase().includes(normalizedQuery)) {
                suggestions.push({
                    type: 'history',
                    value: history[i],
                    display: history[i],
                    icon: '🕐',
                    score: 50 - i
                });
            }
        }

        return suggestions;
    }

    /**
     * Check if query matches initials of title
     * @param {string} title
     * @param {string} query
     * @returns {boolean}
     */
    #matchesInitials(title, query) {
        const words = title.split(/\s+/);
        const initials = words.map(w => w[0]).join('').toLowerCase();
        return initials.startsWith(query.toLowerCase());
    }

    /**
     * Get operator label from method name
     * @param {string} method
     * @returns {string}
     */
    #getOperatorLabel(method) {
        const labels = {
            filterByTag: 'Filter by tag',
            filterByCategory: 'Filter by category',
            filterByComplexity: 'Filter by complexity',
            filterByType: 'Filter by type',
            filterByFilename: 'Search filename',
            filterByFolder: 'Filter by folder',
            filterByFlag: 'Filter by status',
            filterByDateBefore: 'Added before date',
            filterByDateAfter: 'Added after date'
        };
        return labels[method] || 'Filter';
    }

    /**
     * Get category icon
     * @param {string} categoryKey
     * @returns {string}
     */
    #getCategoryIcon(categoryKey) {
        const category = this.toolRepo.getCategory(categoryKey);
        return category?.icon || '📦';
    }

    /**
     * Process and sort suggestions
     * @param {Suggestion[]} suggestions
     * @returns {Suggestion[]}
     */
    #processResults(suggestions) {
        // Remove duplicates by value
        const seen = new Set();
        const unique = suggestions.filter(s => {
            if (seen.has(s.value)) return false;
            seen.add(s.value);
            return true;
        });

        // Sort by score descending
        unique.sort((a, b) => (b.score || 0) - (a.score || 0));

        // Limit results
        return unique.slice(0, LIMITS.SEARCH_SUGGESTIONS);
    }

    /**
     * Get quick action suggestions based on context
     * @returns {Suggestion[]}
     */
    getQuickActions() {
        return [
            {
                type: 'action',
                value: 'is:featured',
                display: 'Show Featured Tools',
                icon: '⭐'
            },
            {
                type: 'action',
                value: 'is:pinned',
                display: 'Show Pinned Tools',
                icon: '📌'
            },
            {
                type: 'action',
                value: 'is:new',
                display: 'Show New Tools',
                icon: '🆕'
            },
            {
                type: 'action',
                value: 'level:simple',
                display: 'Show Simple Tools',
                icon: '🟢'
            }
        ];
    }
}

export { SuggestionEngine };
