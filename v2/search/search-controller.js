/**
 * Search Controller - Orchestrates search functionality
 * Local First Tools v2
 */

import { StateManager } from '../core/state-manager.js';
import { EventBus, EVENTS } from '../core/event-bus.js';
import { FilterEngine } from '../filters/filter-engine.js';
import { SearchParser } from '../filters/search-parser.js';
import { SortEngine } from '../filters/sort-engine.js';
import { SuggestionEngine } from './suggestion-engine.js';
import { DEBOUNCE, LIMITS } from '../core/constants.js';

class SearchController {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SearchController}
     */
    static getInstance() {
        if (!SearchController.#instance) {
            SearchController.#instance = new SearchController();
        }
        return SearchController.#instance;
    }

    constructor() {
        if (SearchController.#instance) {
            throw new Error('Use SearchController.getInstance() instead of new SearchController()');
        }

        this.state = StateManager.getInstance();
        this.events = EventBus.getInstance();
        this.filterEngine = FilterEngine.getInstance();
        this.searchParser = SearchParser.getInstance();
        this.sortEngine = SortEngine.getInstance();
        this.suggestionEngine = SuggestionEngine.getInstance();

        this.#debounceTimer = null;
        this.#lastQuery = '';
        this.#searchHistory = [];
    }

    #debounceTimer;
    #lastQuery;
    #searchHistory;

    /**
     * Initialize the search controller
     */
    initialize() {
        // Load search history from state
        const user = this.state.getSlice('user');
        this.#searchHistory = user.searchHistory || [];
    }

    /**
     * Handle search input (debounced)
     * @param {string} query
     * @param {boolean} immediate - Skip debounce
     */
    search(query, immediate = false) {
        if (immediate) {
            clearTimeout(this.#debounceTimer);
            this.#executeSearch(query);
            return;
        }

        clearTimeout(this.#debounceTimer);
        this.#debounceTimer = setTimeout(() => {
            this.#executeSearch(query);
        }, DEBOUNCE.SEARCH);
    }

    /**
     * Execute the search
     * @param {string} query
     */
    #executeSearch(query) {
        this.#lastQuery = query;

        // Parse the query
        const parsed = this.searchParser.parse(query);

        // Convert to filter criteria
        const searchCriteria = this.searchParser.toFilterCriteria(parsed);

        // Get current filter state
        const currentFilters = this.state.getSlice('filters');

        // Merge search criteria with current filters
        const mergedCriteria = {
            ...currentFilters,
            ...searchCriteria,
            tags: new Set([...currentFilters.tags, ...searchCriteria.tags])
        };

        // Apply filters
        const filteredTools = this.filterEngine.apply(mergedCriteria);

        // Get sort config and user data
        const sortConfig = this.state.getSlice('sort');
        const userData = this.state.getSlice('user');

        // Sort results
        const sortedTools = this.sortEngine.sortWithPinned(
            filteredTools,
            userData.pinnedTools,
            sortConfig,
            userData
        );

        // Update state
        this.state.setState(() => ({
            filteredTools: sortedTools,
            filters: { ...currentFilters, searchTerm: query }
        }));

        // Emit search complete event
        this.events.emit(EVENTS.SEARCH_COMPLETE, {
            query,
            parsed,
            resultCount: sortedTools.length
        });
    }

    /**
     * Get search suggestions
     * @param {string} query
     * @returns {Array}
     */
    getSuggestions(query) {
        return this.suggestionEngine.getSuggestions(query);
    }

    /**
     * Add query to search history
     * @param {string} query
     */
    addToHistory(query) {
        if (!query || query.trim() === '') return;

        // Remove duplicates and add to front
        this.#searchHistory = [
            query,
            ...this.#searchHistory.filter(q => q !== query)
        ].slice(0, LIMITS.SEARCH_HISTORY);

        // Update state
        const user = this.state.getSlice('user');
        this.state.setSlice('user', {
            ...user,
            searchHistory: this.#searchHistory
        });
    }

    /**
     * Get search history
     * @param {number} limit
     * @returns {string[]}
     */
    getHistory(limit = 10) {
        return this.#searchHistory.slice(0, limit);
    }

    /**
     * Clear search history
     */
    clearHistory() {
        this.#searchHistory = [];
        const user = this.state.getSlice('user');
        this.state.setSlice('user', {
            ...user,
            searchHistory: []
        });
    }

    /**
     * Clear current search
     */
    clear() {
        this.#lastQuery = '';

        const currentFilters = this.state.getSlice('filters');
        this.state.setSlice('filters', {
            ...currentFilters,
            searchTerm: ''
        });

        // Re-apply filters without search
        this.#executeSearch('');

        this.events.emit(EVENTS.SEARCH_CLEAR);
    }

    /**
     * Get the last search query
     * @returns {string}
     */
    getLastQuery() {
        return this.#lastQuery;
    }

    /**
     * Highlight search terms in text
     * @param {string} text
     * @param {string} query
     * @returns {string} HTML with highlighted terms
     */
    highlight(text, query = null) {
        const searchQuery = query || this.#lastQuery;
        if (!searchQuery || !text) return text;

        const parsed = this.searchParser.parse(searchQuery);
        if (!parsed.text) return text;

        const terms = parsed.text.split(/\s+/).filter(Boolean);
        let result = text;

        for (const term of terms) {
            const regex = new RegExp(`(${this.#escapeRegex(term)})`, 'gi');
            result = result.replace(regex, '<mark class="search-highlight">$1</mark>');
        }

        return result;
    }

    /**
     * Escape special regex characters
     * @param {string} str
     * @returns {string}
     */
    #escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Get search statistics
     * @returns {Object}
     */
    getStats() {
        const filteredTools = this.state.getSlice('filteredTools');
        const tools = this.state.getSlice('tools');

        return {
            totalTools: tools.length,
            matchingTools: filteredTools.length,
            hasQuery: this.#lastQuery.length > 0,
            historyCount: this.#searchHistory.length
        };
    }

    /**
     * Focus search input
     */
    focus() {
        const input = document.getElementById('search-input');
        if (input) {
            input.focus();
            input.select();
        }
    }

    /**
     * Apply a suggestion
     * @param {Object} suggestion
     */
    applySuggestion(suggestion) {
        if (suggestion.type === 'history') {
            this.search(suggestion.value, true);
        } else if (suggestion.type === 'tool') {
            // Navigate to tool
            this.events.emit(EVENTS.TOOL_FOCUS, { toolId: suggestion.value });
        } else {
            // Append operator or value to current query
            const currentQuery = this.#lastQuery;
            const newQuery = currentQuery
                ? `${currentQuery} ${suggestion.value}`
                : suggestion.value;
            this.search(newQuery, true);
        }

        this.events.emit(EVENTS.SEARCH_SUGGESTION_SELECT, suggestion);
    }
}

export { SearchController };
