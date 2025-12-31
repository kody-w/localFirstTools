/**
 * Search Parser - Advanced search query parsing with operators
 * Local First Tools v2
 */

import { SEARCH_OPERATORS, SEARCH_FLAGS } from '../core/constants.js';

/**
 * @typedef {Object} ParsedQuery
 * @property {string} text - Plain text search terms
 * @property {Object} operators - Parsed operators and their values
 * @property {Array} tokens - All parsed tokens
 */

class SearchParser {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SearchParser}
     */
    static getInstance() {
        if (!SearchParser.#instance) {
            SearchParser.#instance = new SearchParser();
        }
        return SearchParser.#instance;
    }

    constructor() {
        if (SearchParser.#instance) {
            throw new Error('Use SearchParser.getInstance() instead of new SearchParser()');
        }

        // Build operator regex
        const operators = Object.keys(SEARCH_OPERATORS).map(op => op.replace(':', '\\:'));
        this.operatorRegex = new RegExp(`(${operators.join('|')})(\\S+)`, 'gi');
    }

    /**
     * Parse a search query into structured components
     * @param {string} query - Raw search query
     * @returns {ParsedQuery}
     */
    parse(query) {
        if (!query || typeof query !== 'string') {
            return {
                text: '',
                operators: {},
                tokens: []
            };
        }

        const tokens = [];
        const operators = {
            tags: [],
            categories: [],
            complexity: [],
            types: [],
            filenames: [],
            folders: [],
            flags: [],
            dateBefore: null,
            dateAfter: null
        };

        // Extract quoted strings first
        const quotedParts = [];
        let processedQuery = query.replace(/"([^"]+)"/g, (match, content) => {
            quotedParts.push(content);
            return `__QUOTED_${quotedParts.length - 1}__`;
        });

        // Extract operators
        processedQuery = processedQuery.replace(this.operatorRegex, (match, operator, value) => {
            const op = operator.toLowerCase();
            const method = SEARCH_OPERATORS[op];

            if (method) {
                tokens.push({ type: 'operator', operator: op, value, method });
                this.#addOperatorValue(operators, method, value);
            }

            return ''; // Remove from text
        });

        // Restore quoted strings and build remaining text
        let textParts = processedQuery
            .split(/\s+/)
            .filter(Boolean)
            .map(part => {
                const match = part.match(/__QUOTED_(\d+)__/);
                if (match) {
                    const index = parseInt(match[1], 10);
                    return quotedParts[index];
                }
                return part;
            });

        // Add plain text tokens
        for (const text of textParts) {
            if (text.trim()) {
                tokens.push({ type: 'text', value: text });
            }
        }

        return {
            text: textParts.join(' ').trim(),
            operators,
            tokens
        };
    }

    /**
     * Add a value to the appropriate operator array
     * @param {Object} operators
     * @param {string} method
     * @param {string} value
     */
    #addOperatorValue(operators, method, value) {
        switch (method) {
            case 'filterByTag':
                operators.tags.push(value.toLowerCase());
                break;
            case 'filterByCategory':
                operators.categories.push(value.toLowerCase());
                break;
            case 'filterByComplexity':
                operators.complexity.push(value.toLowerCase());
                break;
            case 'filterByType':
                operators.types.push(value.toLowerCase());
                break;
            case 'filterByFilename':
                operators.filenames.push(value.toLowerCase());
                break;
            case 'filterByFolder':
                operators.folders.push(value);
                break;
            case 'filterByFlag':
                operators.flags.push(value.toLowerCase());
                break;
            case 'filterByDateBefore':
                operators.dateBefore = this.#parseDate(value);
                break;
            case 'filterByDateAfter':
                operators.dateAfter = this.#parseDate(value);
                break;
        }
    }

    /**
     * Parse a date string
     * @param {string} value
     * @returns {Date|null}
     */
    #parseDate(value) {
        try {
            const date = new Date(value);
            return isNaN(date.getTime()) ? null : date;
        } catch {
            return null;
        }
    }

    /**
     * Build filter criteria from parsed query
     * @param {ParsedQuery} parsed
     * @returns {Object}
     */
    toFilterCriteria(parsed) {
        const criteria = {
            searchTerm: parsed.text,
            tags: new Set(parsed.operators.tags)
        };

        if (parsed.operators.categories.length > 0) {
            criteria.category = parsed.operators.categories[0];
        }

        if (parsed.operators.complexity.length > 0) {
            criteria.complexity = parsed.operators.complexity[0];
        }

        if (parsed.operators.types.length > 0) {
            criteria.type = parsed.operators.types[0];
        }

        if (parsed.operators.folders.length > 0) {
            criteria.folder = parsed.operators.folders[0];
        }

        // Handle flags
        for (const flag of parsed.operators.flags) {
            switch (flag) {
                case 'featured':
                    criteria.featured = 'featured';
                    break;
                case 'pinned':
                    criteria.isPinned = true;
                    break;
                case 'polished':
                    criteria.polished = 'polished';
                    break;
                case 'new':
                    // Tools added in the last 7 days
                    criteria.dateAfter = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    break;
                case 'recent':
                    criteria.isRecent = true;
                    break;
                case 'popular':
                    criteria.isPopular = true;
                    break;
            }
        }

        if (parsed.operators.dateBefore) {
            criteria.dateBefore = parsed.operators.dateBefore;
        }

        if (parsed.operators.dateAfter) {
            criteria.dateAfter = parsed.operators.dateAfter;
        }

        return criteria;
    }

    /**
     * Get autocomplete suggestions for a partial query
     * @param {string} partial
     * @returns {Array<{type: string, value: string, display: string}>}
     */
    getSuggestions(partial) {
        const suggestions = [];

        // Check if we're in the middle of typing an operator
        const lastPart = partial.split(/\s+/).pop() || '';

        // Suggest operators
        for (const [operator, method] of Object.entries(SEARCH_OPERATORS)) {
            if (operator.startsWith(lastPart.toLowerCase())) {
                suggestions.push({
                    type: 'operator',
                    value: operator,
                    display: `${operator} - ${this.#getOperatorDescription(method)}`
                });
            }
        }

        // If we have an operator prefix, suggest values
        for (const [operator] of Object.entries(SEARCH_OPERATORS)) {
            if (lastPart.toLowerCase().startsWith(operator)) {
                const valuePrefix = lastPart.slice(operator.length);
                const valueSuggestions = this.#getValueSuggestions(operator, valuePrefix);
                suggestions.push(...valueSuggestions);
            }
        }

        return suggestions.slice(0, 8); // Limit suggestions
    }

    /**
     * Get description for an operator method
     * @param {string} method
     * @returns {string}
     */
    #getOperatorDescription(method) {
        const descriptions = {
            filterByTag: 'Filter by tag',
            filterByCategory: 'Filter by category',
            filterByComplexity: 'Filter by complexity',
            filterByType: 'Filter by type',
            filterByFilename: 'Filter by filename',
            filterByFolder: 'Filter by folder',
            filterByFlag: 'Filter by status flag',
            filterByDateBefore: 'Added before date',
            filterByDateAfter: 'Added after date'
        };
        return descriptions[method] || 'Filter';
    }

    /**
     * Get value suggestions for an operator
     * @param {string} operator
     * @param {string} prefix
     * @returns {Array}
     */
    #getValueSuggestions(operator, prefix) {
        const suggestions = [];

        if (operator === 'is:') {
            for (const [key, value] of Object.entries(SEARCH_FLAGS)) {
                if (value.startsWith(prefix.toLowerCase())) {
                    suggestions.push({
                        type: 'flag',
                        value: `is:${value}`,
                        display: `is:${value} - Show ${value} tools`
                    });
                }
            }
        }

        if (operator === 'level:' || operator === 'complexity:') {
            const levels = ['simple', 'intermediate', 'advanced'];
            for (const level of levels) {
                if (level.startsWith(prefix.toLowerCase())) {
                    suggestions.push({
                        type: 'complexity',
                        value: `${operator}${level}`,
                        display: `${operator}${level}`
                    });
                }
            }
        }

        return suggestions;
    }

    /**
     * Highlight operators in a query string for display
     * @param {string} query
     * @returns {string} HTML with highlighted operators
     */
    highlight(query) {
        return query.replace(this.operatorRegex, '<span class="search-operator">$1$2</span>');
    }

    /**
     * Validate a search query
     * @param {string} query
     * @returns {{valid: boolean, errors: string[]}}
     */
    validate(query) {
        const errors = [];
        const parsed = this.parse(query);

        // Check for invalid operators
        for (const token of parsed.tokens) {
            if (token.type === 'operator' && !token.method) {
                errors.push(`Unknown operator: ${token.operator}`);
            }
        }

        // Check for conflicting filters
        if (parsed.operators.dateBefore && parsed.operators.dateAfter) {
            if (parsed.operators.dateBefore < parsed.operators.dateAfter) {
                errors.push('Invalid date range: before date is earlier than after date');
            }
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }
}

export { SearchParser };
