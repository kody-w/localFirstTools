/**
 * Search Worker - Web Worker for non-blocking search
 * Local First Tools v2
 */

// Tool data cache
let toolsIndex = null;
let toolsMap = new Map();

/**
 * Initialize search index
 * @param {Array} tools
 */
function initializeIndex(tools) {
    toolsMap.clear();

    // Create search index
    toolsIndex = tools.map(tool => {
        toolsMap.set(tool.id, tool);

        // Pre-compute search text
        const searchText = [
            tool.title,
            tool.description,
            tool.category,
            ...(tool.tags || []),
            tool.file
        ].join(' ').toLowerCase();

        return {
            id: tool.id,
            searchText,
            titleLower: (tool.title || '').toLowerCase(),
            category: tool.category,
            tags: (tool.tags || []).map(t => t.toLowerCase()),
            featured: tool.featured,
            polished: tool.polished,
            complexity: tool.complexity
        };
    });

    self.postMessage({
        type: 'INDEX_READY',
        count: tools.length
    });
}

/**
 * Search tools
 * @param {string} query
 * @param {Object} options
 * @returns {Array}
 */
function search(query, options = {}) {
    if (!toolsIndex || !query) {
        return [];
    }

    const queryLower = query.toLowerCase().trim();
    const terms = queryLower.split(/\s+/).filter(t => t.length > 0);

    if (terms.length === 0) {
        return [];
    }

    const results = [];
    const limit = options.limit || 50;

    for (const indexed of toolsIndex) {
        let score = 0;
        let matches = 0;

        for (const term of terms) {
            // Check title (highest weight)
            if (indexed.titleLower.includes(term)) {
                score += 100;
                if (indexed.titleLower.startsWith(term)) {
                    score += 50; // Bonus for prefix match
                }
                if (indexed.titleLower === term) {
                    score += 100; // Exact match bonus
                }
                matches++;
            }

            // Check tags (high weight)
            if (indexed.tags.some(t => t.includes(term))) {
                score += 50;
                matches++;
            }

            // Check category
            if (indexed.category?.toLowerCase().includes(term)) {
                score += 30;
                matches++;
            }

            // Check full text (lower weight)
            if (indexed.searchText.includes(term)) {
                score += 10;
                matches++;
            }
        }

        // Only include if all terms match
        if (matches >= terms.length) {
            // Boost featured and polished
            if (indexed.featured) score += 20;
            if (indexed.polished) score += 10;

            results.push({
                id: indexed.id,
                score
            });
        }
    }

    // Sort by score
    results.sort((a, b) => b.score - a.score);

    // Return limited results with full tool data
    return results.slice(0, limit).map(r => ({
        ...toolsMap.get(r.id),
        _searchScore: r.score
    }));
}

/**
 * Fuzzy search for suggestions
 * @param {string} query
 * @param {number} limit
 * @returns {Array}
 */
function fuzzySearch(query, limit = 10) {
    if (!toolsIndex || !query || query.length < 2) {
        return [];
    }

    const queryLower = query.toLowerCase();
    const results = [];

    for (const indexed of toolsIndex) {
        const distance = levenshteinDistance(queryLower, indexed.titleLower.slice(0, query.length + 5));

        if (distance <= 3) {
            results.push({
                id: indexed.id,
                title: toolsMap.get(indexed.id).title,
                distance
            });
        }
    }

    results.sort((a, b) => a.distance - b.distance);
    return results.slice(0, limit);
}

/**
 * Calculate Levenshtein distance
 * @param {string} a
 * @param {string} b
 * @returns {number}
 */
function levenshteinDistance(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;

    const matrix = [];

    for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }

    for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }

    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }

    return matrix[b.length][a.length];
}

/**
 * Filter tools
 * @param {Object} filters
 * @returns {Array}
 */
function filter(filters) {
    if (!toolsIndex) {
        return [];
    }

    let results = [...toolsIndex];

    // Category filter
    if (filters.category) {
        results = results.filter(t => t.category === filters.category);
    }

    // Complexity filter
    if (filters.complexity) {
        results = results.filter(t => t.complexity === filters.complexity);
    }

    // Featured filter
    if (filters.featured) {
        results = results.filter(t => t.featured);
    }

    // Polished filter
    if (filters.polished) {
        results = results.filter(t => t.polished);
    }

    // Tags filter
    if (filters.tags && filters.tags.length > 0) {
        const filterTags = filters.tags.map(t => t.toLowerCase());
        results = results.filter(t =>
            filterTags.some(ft => t.tags.includes(ft))
        );
    }

    return results.map(r => toolsMap.get(r.id));
}

/**
 * Get suggestions based on partial input
 * @param {string} partial
 * @returns {Object}
 */
function getSuggestions(partial) {
    if (!toolsIndex || !partial || partial.length < 1) {
        return { tools: [], tags: [], categories: [] };
    }

    const partialLower = partial.toLowerCase();

    // Tool suggestions
    const tools = [];
    const seenTitles = new Set();

    for (const indexed of toolsIndex) {
        if (indexed.titleLower.includes(partialLower) && !seenTitles.has(indexed.titleLower)) {
            tools.push({
                id: indexed.id,
                title: toolsMap.get(indexed.id).title
            });
            seenTitles.add(indexed.titleLower);

            if (tools.length >= 5) break;
        }
    }

    // Tag suggestions
    const tagCounts = new Map();

    for (const indexed of toolsIndex) {
        for (const tag of indexed.tags) {
            if (tag.includes(partialLower)) {
                tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
            }
        }
    }

    const tags = Array.from(tagCounts.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([tag]) => tag);

    // Category suggestions
    const categories = new Set();

    for (const indexed of toolsIndex) {
        if (indexed.category?.toLowerCase().includes(partialLower)) {
            categories.add(indexed.category);
        }
    }

    return {
        tools,
        tags,
        categories: Array.from(categories).slice(0, 5)
    };
}

// Message handler
self.onmessage = function(e) {
    const { type, data } = e.data;

    switch (type) {
        case 'INIT':
            initializeIndex(data.tools);
            break;

        case 'SEARCH':
            const searchResults = search(data.query, data.options);
            self.postMessage({
                type: 'SEARCH_RESULTS',
                requestId: data.requestId,
                results: searchResults
            });
            break;

        case 'FUZZY_SEARCH':
            const fuzzyResults = fuzzySearch(data.query, data.limit);
            self.postMessage({
                type: 'FUZZY_RESULTS',
                requestId: data.requestId,
                results: fuzzyResults
            });
            break;

        case 'FILTER':
            const filterResults = filter(data.filters);
            self.postMessage({
                type: 'FILTER_RESULTS',
                requestId: data.requestId,
                results: filterResults
            });
            break;

        case 'SUGGESTIONS':
            const suggestions = getSuggestions(data.partial);
            self.postMessage({
                type: 'SUGGESTION_RESULTS',
                requestId: data.requestId,
                results: suggestions
            });
            break;

        case 'CLEAR':
            toolsIndex = null;
            toolsMap.clear();
            self.postMessage({ type: 'CLEARED' });
            break;
    }
};

// Log that worker is ready
self.postMessage({ type: 'WORKER_READY' });
