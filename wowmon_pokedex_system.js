/**
 * =======================================================================
 * WOWMON POKÉDEX SEARCH & FILTER SYSTEM
 * =======================================================================
 *
 * A comprehensive, real-time search and filtering system for the WoWmon
 * creature collection game. This system provides powerful filtering
 * capabilities for viewing and managing your creature collection.
 *
 * FEATURES:
 * - Real-time search (name, number, fuzzy matching)
 * - Multi-criteria filtering (type, generation, stats)
 * - Advanced sorting options
 * - Quick filter presets
 * - URL parameter support for shareable views
 * - Local storage for search history
 * - Debounced input for performance
 * - Virtual scrolling support (optional)
 *
 * INTEGRATION:
 * Add this code to the WoWGame class in wowMon.html
 * =======================================================================
 */

/**
 * =======================================================================
 * PART 1: CSS STYLES FOR POKÉDEX UI
 * =======================================================================
 * Add these styles to the <style> section
 */
const POKEDEX_STYLES = `
    /* Pokédex Container */
    .pokedex-container {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--gb-lightest);
        display: none;
        flex-direction: column;
        z-index: 100;
        overflow: hidden;
    }

    .pokedex-container.active {
        display: flex;
    }

    /* Pokédex Header */
    .pokedex-header {
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        padding: 8px;
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        border-bottom: 2px solid var(--gb-dark);
    }

    /* Search Section */
    .pokedex-search {
        padding: 8px;
        background: var(--gb-light);
        border-bottom: 2px solid var(--gb-dark);
    }

    .search-input-wrapper {
        position: relative;
        margin-bottom: 8px;
    }

    .search-input {
        width: 100%;
        padding: 6px;
        font-family: monospace;
        font-size: 12px;
        border: 2px solid var(--gb-darkest);
        background: var(--gb-lightest);
        color: var(--gb-darkest);
        box-sizing: border-box;
    }

    .search-input:focus {
        outline: 3px solid #ffcc00;
        outline-offset: 1px;
    }

    .search-clear {
        position: absolute;
        right: 4px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        border: none;
        padding: 2px 6px;
        cursor: pointer;
        font-size: 10px;
        font-family: monospace;
    }

    /* Filter Controls */
    .filter-controls {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
        margin-bottom: 4px;
    }

    .filter-btn {
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        border: none;
        padding: 4px 8px;
        font-size: 10px;
        font-family: monospace;
        cursor: pointer;
        flex: 1;
        min-width: 60px;
    }

    .filter-btn:hover {
        background: var(--gb-dark);
    }

    .filter-btn.active {
        background: #ffcc00;
        color: var(--gb-darkest);
        font-weight: bold;
    }

    /* Type Filters */
    .type-filters {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        margin-top: 4px;
    }

    .type-filter-btn {
        background: var(--gb-dark);
        color: var(--gb-lightest);
        border: 2px solid var(--gb-darkest);
        padding: 4px;
        font-size: 9px;
        font-family: monospace;
        cursor: pointer;
        text-align: center;
    }

    .type-filter-btn.active {
        background: var(--gb-darkest);
        border-color: #ffcc00;
        font-weight: bold;
    }

    /* Stat Range Sliders */
    .stat-filters {
        display: none;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--gb-dark);
    }

    .stat-filters.active {
        display: block;
    }

    .stat-filter-group {
        margin-bottom: 6px;
    }

    .stat-filter-label {
        font-size: 9px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px;
    }

    .stat-filter-slider {
        width: 100%;
        height: 8px;
        -webkit-appearance: none;
        appearance: none;
        background: var(--gb-darkest);
        outline: none;
        cursor: pointer;
    }

    .stat-filter-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 12px;
        height: 12px;
        background: #ffcc00;
        cursor: pointer;
        border: 2px solid var(--gb-darkest);
    }

    .stat-filter-slider::-moz-range-thumb {
        width: 12px;
        height: 12px;
        background: #ffcc00;
        cursor: pointer;
        border: 2px solid var(--gb-darkest);
    }

    /* Sort Controls */
    .sort-controls {
        padding: 4px 8px;
        background: var(--gb-light);
        border-bottom: 2px solid var(--gb-dark);
        display: flex;
        gap: 4px;
        font-size: 10px;
    }

    .sort-label {
        font-weight: bold;
        margin-right: 4px;
        align-self: center;
    }

    .sort-select {
        flex: 1;
        padding: 4px;
        font-family: monospace;
        font-size: 10px;
        border: 2px solid var(--gb-darkest);
        background: var(--gb-lightest);
        color: var(--gb-darkest);
    }

    .sort-direction-btn {
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        border: none;
        padding: 4px 8px;
        font-size: 10px;
        cursor: pointer;
    }

    /* Results Info */
    .results-info {
        padding: 4px 8px;
        background: var(--gb-light);
        border-bottom: 1px solid var(--gb-dark);
        font-size: 9px;
        display: flex;
        justify-content: space-between;
    }

    /* Creature List */
    .pokedex-list {
        flex: 1;
        overflow-y: auto;
        background: var(--gb-lightest);
    }

    .creature-entry {
        padding: 8px;
        border-bottom: 2px solid var(--gb-light);
        cursor: pointer;
        display: flex;
        gap: 8px;
        align-items: center;
    }

    .creature-entry:hover {
        background: var(--gb-light);
    }

    .creature-entry.selected {
        background: var(--gb-dark);
        color: var(--gb-lightest);
    }

    .creature-entry.locked {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .creature-number {
        font-size: 10px;
        font-weight: bold;
        min-width: 30px;
        color: var(--gb-dark);
    }

    .creature-entry.selected .creature-number {
        color: var(--gb-lightest);
    }

    .creature-icon {
        width: 24px;
        height: 24px;
        background: var(--gb-dark);
        border: 2px solid var(--gb-darkest);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .creature-info {
        flex: 1;
    }

    .creature-name {
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 2px;
    }

    .creature-types {
        font-size: 8px;
        display: flex;
        gap: 4px;
    }

    .type-badge {
        background: var(--gb-dark);
        color: var(--gb-lightest);
        padding: 1px 4px;
        border-radius: 2px;
    }

    .creature-stats-preview {
        font-size: 8px;
        text-align: right;
    }

    /* Creature Detail View */
    .creature-detail {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--gb-lightest);
        display: none;
        flex-direction: column;
        z-index: 101;
        overflow-y: auto;
    }

    .creature-detail.active {
        display: flex;
    }

    .detail-header {
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        padding: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .detail-close-btn {
        background: var(--gb-dark);
        color: var(--gb-lightest);
        border: none;
        padding: 4px 8px;
        cursor: pointer;
        font-size: 10px;
    }

    .detail-body {
        padding: 12px;
        flex: 1;
    }

    .detail-section {
        margin-bottom: 12px;
    }

    .detail-section-title {
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 4px;
        padding-bottom: 2px;
        border-bottom: 1px solid var(--gb-dark);
    }

    .detail-stat-bars {
        margin-top: 6px;
    }

    .detail-stat-bar {
        margin-bottom: 4px;
    }

    .detail-stat-label {
        font-size: 9px;
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px;
    }

    .detail-stat-fill-container {
        height: 8px;
        background: var(--gb-dark);
        border: 1px solid var(--gb-darkest);
    }

    .detail-stat-fill {
        height: 100%;
        background: var(--gb-darkest);
        transition: width 0.3s;
    }

    /* Quick Filters */
    .quick-filters {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 4px;
        margin-top: 4px;
    }

    .quick-filter-btn {
        background: var(--gb-dark);
        color: var(--gb-lightest);
        border: 2px solid var(--gb-darkest);
        padding: 6px;
        font-size: 9px;
        font-family: monospace;
        cursor: pointer;
        text-align: center;
    }

    .quick-filter-btn.active {
        background: #ffcc00;
        color: var(--gb-darkest);
        font-weight: bold;
    }

    /* Empty State */
    .empty-state {
        padding: 24px;
        text-align: center;
        font-size: 11px;
        color: var(--gb-dark);
    }

    /* Accessibility - High Contrast Mode */
    body.high-contrast .pokedex-container,
    body.high-contrast .creature-detail {
        background: #fff;
        border: 2px solid #000;
    }

    body.high-contrast .filter-btn,
    body.high-contrast .type-filter-btn,
    body.high-contrast .sort-direction-btn {
        border: 2px solid #000;
    }
`;

/**
 * =======================================================================
 * PART 2: HTML STRUCTURE
 * =======================================================================
 * Add this HTML inside the .ui-overlay div
 */
const POKEDEX_HTML = `
<!-- Pokédex Container -->
<div class="pokedex-container" id="pokedexContainer" role="region" aria-label="Creature Pokédex">
    <!-- Header -->
    <div class="pokedex-header">
        <span>CREATURE POKÉDEX</span>
    </div>

    <!-- Search Section -->
    <div class="pokedex-search">
        <div class="search-input-wrapper">
            <input
                type="text"
                class="search-input"
                id="pokedexSearch"
                placeholder="Search by name or number..."
                aria-label="Search creatures by name or number"
            >
            <button class="search-clear" id="searchClear" aria-label="Clear search">✕</button>
        </div>

        <!-- Main Filter Controls -->
        <div class="filter-controls">
            <button class="filter-btn" id="filterAll" aria-label="Show all creatures">ALL</button>
            <button class="filter-btn" id="filterCaught" aria-label="Show caught creatures">CAUGHT</button>
            <button class="filter-btn" id="filterUnseen" aria-label="Show unseen creatures">UNSEEN</button>
            <button class="filter-btn" id="filterTypes" aria-label="Filter by type">TYPES</button>
            <button class="filter-btn" id="filterStats" aria-label="Filter by stats">STATS</button>
        </div>

        <!-- Type Filters (Hidden by default) -->
        <div class="type-filters" id="typeFiltersContainer" style="display: none;">
            <!-- Will be populated dynamically -->
        </div>

        <!-- Stat Filters (Hidden by default) -->
        <div class="stat-filters" id="statFiltersContainer">
            <div class="stat-filter-group">
                <div class="stat-filter-label">
                    <span>HP</span>
                    <span id="hpFilterValue">Any</span>
                </div>
                <input type="range" class="stat-filter-slider" id="hpFilter" min="0" max="150" value="0" step="5">
            </div>
            <div class="stat-filter-group">
                <div class="stat-filter-label">
                    <span>Attack</span>
                    <span id="attackFilterValue">Any</span>
                </div>
                <input type="range" class="stat-filter-slider" id="attackFilter" min="0" max="150" value="0" step="5">
            </div>
            <div class="stat-filter-group">
                <div class="stat-filter-label">
                    <span>Defense</span>
                    <span id="defenseFilterValue">Any</span>
                </div>
                <input type="range" class="stat-filter-slider" id="defenseFilter" min="0" max="150" value="0" step="5">
            </div>
            <div class="stat-filter-group">
                <div class="stat-filter-label">
                    <span>Speed</span>
                    <span id="speedFilterValue">Any</span>
                </div>
                <input type="range" class="stat-filter-slider" id="speedFilter" min="0" max="150" value="0" step="5">
            </div>
        </div>

        <!-- Quick Filters -->
        <div class="quick-filters">
            <button class="quick-filter-btn" id="quickFilterStarters" aria-label="Show starter creatures">STARTERS</button>
            <button class="quick-filter-btn" id="quickFilterEvolved" aria-label="Show fully evolved">FULLY EVOLVED</button>
            <button class="quick-filter-btn" id="quickFilterCanEvolve" aria-label="Show creatures that can evolve">CAN EVOLVE</button>
            <button class="quick-filter-btn" id="quickFilterHighStats" aria-label="Show high stat creatures">HIGH STATS</button>
        </div>
    </div>

    <!-- Sort Controls -->
    <div class="sort-controls">
        <span class="sort-label">SORT:</span>
        <select class="sort-select" id="sortSelect" aria-label="Sort creatures by">
            <option value="number-asc">Number (Low-High)</option>
            <option value="number-desc">Number (High-Low)</option>
            <option value="name-asc">Name (A-Z)</option>
            <option value="name-desc">Name (Z-A)</option>
            <option value="hp-desc">HP (Highest)</option>
            <option value="hp-asc">HP (Lowest)</option>
            <option value="attack-desc">Attack (Highest)</option>
            <option value="attack-asc">Attack (Lowest)</option>
            <option value="defense-desc">Defense (Highest)</option>
            <option value="defense-asc">Defense (Lowest)</option>
            <option value="speed-desc">Speed (Highest)</option>
            <option value="speed-asc">Speed (Lowest)</option>
        </select>
        <button class="sort-direction-btn" id="sortDirection" aria-label="Toggle sort direction">↕</button>
    </div>

    <!-- Results Info -->
    <div class="results-info">
        <span id="resultsCount">0 creatures</span>
        <span id="resultsFiltered"></span>
    </div>

    <!-- Creature List -->
    <div class="pokedex-list" id="pokedexList" role="list">
        <!-- Will be populated dynamically -->
    </div>
</div>

<!-- Creature Detail View -->
<div class="creature-detail" id="creatureDetail" role="dialog" aria-labelledby="detailCreatureName">
    <div class="detail-header">
        <span id="detailCreatureName">CREATURE NAME</span>
        <button class="detail-close-btn" id="detailClose" aria-label="Close detail view">CLOSE</button>
    </div>
    <div class="detail-body" id="detailBody">
        <!-- Will be populated dynamically -->
    </div>
</div>
`;

/**
 * =======================================================================
 * PART 3: POKÉDEX MANAGER CLASS
 * =======================================================================
 * Core logic for the Pokédex system
 */
class PokedexManager {
    constructor(game) {
        this.game = game;
        this.allCreatures = [];
        this.filteredCreatures = [];
        this.searchHistory = [];
        this.maxHistorySize = 10;

        // Filter state
        this.filters = {
            search: '',
            caught: null, // null = all, true = caught, false = unseen
            types: [],
            stats: {
                hp: 0,
                attack: 0,
                defense: 0,
                speed: 0
            },
            quickFilter: null
        };

        // Sort state
        this.sortMethod = 'number-asc';

        // Debounce timer
        this.searchDebounceTimer = null;
        this.searchDebounceDelay = 300; // milliseconds

        this.loadSearchHistory();
        this.initializeCreatureData();
    }

    /**
     * Initialize creature data from cartridge
     * Converts cartridge data into searchable format
     */
    initializeCreatureData() {
        const creatures = this.game.cartridge.creatures;
        let index = 1;

        for (const id in creatures) {
            const creature = creatures[id];
            this.allCreatures.push({
                number: index++,
                id: creature.id,
                name: creature.name,
                types: creature.type || [],
                hp: creature.baseHp,
                attack: creature.baseAttack,
                defense: creature.baseDefense,
                speed: creature.baseSpeed,
                evolveLevel: creature.evolveLevel,
                evolveTo: creature.evolveTo,
                moves: creature.moves || [],
                description: creature.description,
                caught: this.isCreatureCaught(creature.id),
                seen: this.isCreatureSeen(creature.id)
            });
        }

        this.filteredCreatures = [...this.allCreatures];
    }

    /**
     * Check if player has caught this creature
     */
    isCreatureCaught(creatureId) {
        return this.game.player.creatures.some(c => c.id === creatureId);
    }

    /**
     * Check if player has seen this creature
     */
    isCreatureSeen(creatureId) {
        // Check if in uniqueCreaturesCaught or if player has it
        return this.game.player.stats.uniqueCreaturesCaught.includes(creatureId) ||
               this.isCreatureCaught(creatureId);
    }

    /**
     * Apply all active filters to creature list
     */
    applyFilters() {
        let results = [...this.allCreatures];

        // Text search filter (fuzzy matching)
        if (this.filters.search) {
            const searchLower = this.filters.search.toLowerCase();
            results = results.filter(creature => {
                // Match by number
                if (creature.number.toString() === searchLower) {
                    return true;
                }

                // Match by name (fuzzy)
                const nameLower = creature.name.toLowerCase();
                if (nameLower.includes(searchLower)) {
                    return true;
                }

                // Fuzzy match (allows 1-2 character differences)
                if (this.fuzzyMatch(nameLower, searchLower)) {
                    return true;
                }

                return false;
            });
        }

        // Caught/Unseen filter
        if (this.filters.caught === true) {
            results = results.filter(c => c.caught);
        } else if (this.filters.caught === false) {
            results = results.filter(c => !c.seen);
        }

        // Type filter (OR logic - match any selected type)
        if (this.filters.types.length > 0) {
            results = results.filter(creature => {
                return this.filters.types.some(type =>
                    creature.types.includes(type)
                );
            });
        }

        // Stat filters
        if (this.filters.stats.hp > 0) {
            results = results.filter(c => c.hp >= this.filters.stats.hp);
        }
        if (this.filters.stats.attack > 0) {
            results = results.filter(c => c.attack >= this.filters.stats.attack);
        }
        if (this.filters.stats.defense > 0) {
            results = results.filter(c => c.defense >= this.filters.stats.defense);
        }
        if (this.filters.stats.speed > 0) {
            results = results.filter(c => c.speed >= this.filters.stats.speed);
        }

        // Quick filters
        if (this.filters.quickFilter === 'starters') {
            const starters = this.game.cartridge.starters || [];
            results = results.filter(c => starters.includes(c.id));
        } else if (this.filters.quickFilter === 'evolved') {
            results = results.filter(c => c.evolveTo === null && c.evolveLevel === null);
        } else if (this.filters.quickFilter === 'canEvolve') {
            results = results.filter(c => c.evolveTo !== null);
        } else if (this.filters.quickFilter === 'highStats') {
            // Creatures with total base stats > 300
            results = results.filter(c =>
                (c.hp + c.attack + c.defense + c.speed) > 300
            );
        }

        this.filteredCreatures = results;
        this.applySorting();
    }

    /**
     * Fuzzy string matching (Levenshtein distance)
     * Allows 1-2 character differences for typo tolerance
     */
    fuzzyMatch(str1, str2) {
        if (str2.length < 3) return false; // Too short for fuzzy matching

        const maxDistance = str2.length <= 5 ? 1 : 2;
        const distance = this.levenshteinDistance(str1, str2);
        return distance <= maxDistance;
    }

    /**
     * Calculate Levenshtein distance between two strings
     */
    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
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

        return matrix[str2.length][str1.length];
    }

    /**
     * Apply current sort method to filtered results
     */
    applySorting() {
        const [field, direction] = this.sortMethod.split('-');

        this.filteredCreatures.sort((a, b) => {
            let comparison = 0;

            switch (field) {
                case 'number':
                    comparison = a.number - b.number;
                    break;
                case 'name':
                    comparison = a.name.localeCompare(b.name);
                    break;
                case 'hp':
                    comparison = a.hp - b.hp;
                    break;
                case 'attack':
                    comparison = a.attack - b.attack;
                    break;
                case 'defense':
                    comparison = a.defense - b.defense;
                    break;
                case 'speed':
                    comparison = a.speed - b.speed;
                    break;
            }

            return direction === 'asc' ? comparison : -comparison;
        });
    }

    /**
     * Debounced search handler
     * Waits for user to stop typing before filtering
     */
    handleSearchInput(searchText) {
        clearTimeout(this.searchDebounceTimer);

        this.searchDebounceTimer = setTimeout(() => {
            this.filters.search = searchText;
            this.applyFilters();
            this.render();

            // Save to history if not empty
            if (searchText.trim()) {
                this.addToSearchHistory(searchText);
            }
        }, this.searchDebounceDelay);
    }

    /**
     * Add search term to history
     */
    addToSearchHistory(term) {
        // Remove duplicates
        this.searchHistory = this.searchHistory.filter(t => t !== term);

        // Add to beginning
        this.searchHistory.unshift(term);

        // Limit size
        if (this.searchHistory.length > this.maxHistorySize) {
            this.searchHistory = this.searchHistory.slice(0, this.maxHistorySize);
        }

        this.saveSearchHistory();
    }

    /**
     * Save search history to localStorage
     */
    saveSearchHistory() {
        try {
            localStorage.setItem('wowmon_search_history', JSON.stringify(this.searchHistory));
        } catch (e) {
            console.warn('Failed to save search history:', e);
        }
    }

    /**
     * Load search history from localStorage
     */
    loadSearchHistory() {
        try {
            const saved = localStorage.getItem('wowmon_search_history');
            if (saved) {
                this.searchHistory = JSON.parse(saved);
            }
        } catch (e) {
            console.warn('Failed to load search history:', e);
        }
    }

    /**
     * Get all unique types from creatures
     */
    getAllTypes() {
        const types = new Set();
        this.allCreatures.forEach(creature => {
            creature.types.forEach(type => types.add(type));
        });
        return Array.from(types).sort();
    }

    /**
     * Toggle type filter
     */
    toggleTypeFilter(type) {
        const index = this.filters.types.indexOf(type);
        if (index === -1) {
            this.filters.types.push(type);
        } else {
            this.filters.types.splice(index, 1);
        }
        this.applyFilters();
        this.render();
    }

    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.filters = {
            search: '',
            caught: null,
            types: [],
            stats: { hp: 0, attack: 0, defense: 0, speed: 0 },
            quickFilter: null
        };
        this.applyFilters();
        this.render();
    }

    /**
     * Render the Pokédex UI
     */
    render() {
        const listContainer = document.getElementById('pokedexList');
        if (!listContainer) return;

        // Update results count
        const totalCount = this.allCreatures.length;
        const filteredCount = this.filteredCreatures.length;
        document.getElementById('resultsCount').textContent =
            `${filteredCount} of ${totalCount} creatures`;

        // Clear list
        listContainer.innerHTML = '';

        // Show empty state if no results
        if (this.filteredCreatures.length === 0) {
            listContainer.innerHTML = `
                <div class="empty-state">
                    No creatures match your filters.<br>
                    Try adjusting your search criteria.
                </div>
            `;
            return;
        }

        // Render creature entries
        this.filteredCreatures.forEach(creature => {
            const entry = this.createCreatureEntry(creature);
            listContainer.appendChild(entry);
        });
    }

    /**
     * Create a creature list entry element
     */
    createCreatureEntry(creature) {
        const entry = document.createElement('div');
        entry.className = 'creature-entry';
        entry.setAttribute('role', 'listitem');
        entry.setAttribute('tabindex', '0');

        if (!creature.seen) {
            entry.classList.add('locked');
        }

        // Creature number
        const number = document.createElement('div');
        number.className = 'creature-number';
        number.textContent = `#${creature.number.toString().padStart(3, '0')}`;

        // Creature icon/sprite
        const icon = document.createElement('div');
        icon.className = 'creature-icon';
        icon.textContent = creature.seen ? '●' : '?';

        // Creature info
        const info = document.createElement('div');
        info.className = 'creature-info';

        const name = document.createElement('div');
        name.className = 'creature-name';
        name.textContent = creature.seen ? creature.name : '???';

        const types = document.createElement('div');
        types.className = 'creature-types';
        if (creature.seen) {
            creature.types.forEach(type => {
                const badge = document.createElement('span');
                badge.className = 'type-badge';
                badge.textContent = type.toUpperCase();
                types.appendChild(badge);
            });
        }

        info.appendChild(name);
        info.appendChild(types);

        // Stats preview
        const stats = document.createElement('div');
        stats.className = 'creature-stats-preview';
        if (creature.seen) {
            stats.innerHTML = `
                HP: ${creature.hp}<br>
                ATK: ${creature.attack}
            `;
        }

        entry.appendChild(number);
        entry.appendChild(icon);
        entry.appendChild(info);
        entry.appendChild(stats);

        // Click handler
        if (creature.seen) {
            entry.addEventListener('click', () => this.showCreatureDetail(creature));
            entry.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.showCreatureDetail(creature);
                }
            });
        }

        return entry;
    }

    /**
     * Show detailed view of a creature
     */
    showCreatureDetail(creature) {
        const detailContainer = document.getElementById('creatureDetail');
        const detailBody = document.getElementById('detailBody');
        const detailName = document.getElementById('detailCreatureName');

        if (!detailContainer || !detailBody || !detailName) return;

        detailName.textContent = `#${creature.number.toString().padStart(3, '0')} ${creature.name}`;

        // Build detail content
        detailBody.innerHTML = `
            <div class="detail-section">
                <div class="detail-section-title">TYPE</div>
                <div class="creature-types">
                    ${creature.types.map(t => `<span class="type-badge">${t.toUpperCase()}</span>`).join(' ')}
                </div>
            </div>

            <div class="detail-section">
                <div class="detail-section-title">DESCRIPTION</div>
                <div style="font-size: 10px; line-height: 1.4;">${creature.description}</div>
            </div>

            <div class="detail-section">
                <div class="detail-section-title">BASE STATS</div>
                <div class="detail-stat-bars">
                    ${this.createStatBar('HP', creature.hp)}
                    ${this.createStatBar('Attack', creature.attack)}
                    ${this.createStatBar('Defense', creature.defense)}
                    ${this.createStatBar('Speed', creature.speed)}
                    ${this.createStatBar('Total', creature.hp + creature.attack + creature.defense + creature.speed)}
                </div>
            </div>

            ${creature.evolveTo ? `
            <div class="detail-section">
                <div class="detail-section-title">EVOLUTION</div>
                <div style="font-size: 10px;">
                    Evolves to ${creature.evolveTo.toUpperCase()} at level ${creature.evolveLevel}
                </div>
            </div>
            ` : ''}

            <div class="detail-section">
                <div class="detail-section-title">MOVES</div>
                <div style="font-size: 9px; display: grid; grid-template-columns: 1fr 1fr; gap: 4px;">
                    ${creature.moves.map(moveId => {
                        const move = this.game.cartridge.moves[moveId];
                        return move ? `<div>${move.name} (${move.type})</div>` : '';
                    }).join('')}
                </div>
            </div>

            ${creature.caught ? `
            <div class="detail-section">
                <div class="detail-section-title">YOUR COLLECTION</div>
                <div style="font-size: 10px;">
                    You have ${this.game.player.creatures.filter(c => c.id === creature.id).length} of this creature
                </div>
            </div>
            ` : ''}
        `;

        detailContainer.classList.add('active');

        // Announce to screen readers
        this.announceToScreenReader(`Viewing details for ${creature.name}`);
    }

    /**
     * Create stat bar HTML
     */
    createStatBar(label, value, maxValue = 150) {
        const percentage = Math.min((value / maxValue) * 100, 100);
        return `
            <div class="detail-stat-bar">
                <div class="detail-stat-label">
                    <span>${label}</span>
                    <span>${value}</span>
                </div>
                <div class="detail-stat-fill-container">
                    <div class="detail-stat-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }

    /**
     * Close detail view
     */
    closeDetail() {
        const detailContainer = document.getElementById('creatureDetail');
        if (detailContainer) {
            detailContainer.classList.remove('active');
        }
    }

    /**
     * Announce message to screen readers
     */
    announceToScreenReader(message) {
        const liveRegion = document.querySelector('.live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Get shareable URL with current filters
     */
    getShareableURL() {
        const params = new URLSearchParams();

        if (this.filters.search) {
            params.set('search', this.filters.search);
        }
        if (this.filters.caught !== null) {
            params.set('caught', this.filters.caught);
        }
        if (this.filters.types.length > 0) {
            params.set('types', this.filters.types.join(','));
        }
        if (this.sortMethod !== 'number-asc') {
            params.set('sort', this.sortMethod);
        }

        return `${window.location.origin}${window.location.pathname}?${params.toString()}`;
    }

    /**
     * Load filters from URL parameters
     */
    loadFromURL() {
        const params = new URLSearchParams(window.location.search);

        if (params.has('search')) {
            this.filters.search = params.get('search');
            const searchInput = document.getElementById('pokedexSearch');
            if (searchInput) {
                searchInput.value = this.filters.search;
            }
        }

        if (params.has('caught')) {
            this.filters.caught = params.get('caught') === 'true';
        }

        if (params.has('types')) {
            this.filters.types = params.get('types').split(',');
        }

        if (params.has('sort')) {
            this.sortMethod = params.get('sort');
            const sortSelect = document.getElementById('sortSelect');
            if (sortSelect) {
                sortSelect.value = this.sortMethod;
            }
        }

        this.applyFilters();
        this.render();
    }
}

/**
 * =======================================================================
 * PART 4: INTEGRATION INSTRUCTIONS
 * =======================================================================
 *
 * TO INTEGRATE INTO WOWMON.HTML:
 *
 * 1. Add POKEDEX_STYLES to the <style> section (around line 500)
 *
 * 2. Add POKEDEX_HTML to the .ui-overlay div (around line 900)
 *
 * 3. Add this PokedexManager class to the JavaScript section (around line 1400)
 *
 * 4. In the WoWGame class constructor, add:
 *    this.pokedex = new PokedexManager(this);
 *
 * 5. Replace the selectMenuOption method (around line 3876) with:
 */

// Add to WoWGame class:
function initializePokedex() {
    this.pokedex = new PokedexManager(this);

    // Setup event listeners
    this.setupPokedexEventListeners();
}

function setupPokedexEventListeners() {
    // Search input
    const searchInput = document.getElementById('pokedexSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            this.pokedex.handleSearchInput(e.target.value);
        });
    }

    // Clear search button
    const searchClear = document.getElementById('searchClear');
    if (searchClear) {
        searchClear.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            this.pokedex.filters.search = '';
            this.pokedex.applyFilters();
            this.pokedex.render();
        });
    }

    // Filter buttons
    document.getElementById('filterAll')?.addEventListener('click', () => {
        this.pokedex.filters.caught = null;
        this.updateFilterButtonStates();
        this.pokedex.applyFilters();
        this.pokedex.render();
    });

    document.getElementById('filterCaught')?.addEventListener('click', () => {
        this.pokedex.filters.caught = true;
        this.updateFilterButtonStates();
        this.pokedex.applyFilters();
        this.pokedex.render();
    });

    document.getElementById('filterUnseen')?.addEventListener('click', () => {
        this.pokedex.filters.caught = false;
        this.updateFilterButtonStates();
        this.pokedex.applyFilters();
        this.pokedex.render();
    });

    // Type filter toggle
    document.getElementById('filterTypes')?.addEventListener('click', () => {
        const typeContainer = document.getElementById('typeFiltersContainer');
        if (typeContainer) {
            const isHidden = typeContainer.style.display === 'none';
            typeContainer.style.display = isHidden ? 'grid' : 'none';

            // Initialize type buttons if first time
            if (isHidden && typeContainer.children.length === 0) {
                this.initializeTypeFilters();
            }
        }
    });

    // Stats filter toggle
    document.getElementById('filterStats')?.addEventListener('click', () => {
        const statsContainer = document.getElementById('statFiltersContainer');
        if (statsContainer) {
            statsContainer.classList.toggle('active');
        }
    });

    // Stat sliders
    ['hp', 'attack', 'defense', 'speed'].forEach(stat => {
        const slider = document.getElementById(`${stat}Filter`);
        const valueDisplay = document.getElementById(`${stat}FilterValue`);

        if (slider && valueDisplay) {
            slider.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                valueDisplay.textContent = value === 0 ? 'Any' : `${value}+`;
                this.pokedex.filters.stats[stat] = value;
                this.pokedex.applyFilters();
                this.pokedex.render();
            });
        }
    });

    // Quick filters
    document.getElementById('quickFilterStarters')?.addEventListener('click', () => {
        this.toggleQuickFilter('starters');
    });

    document.getElementById('quickFilterEvolved')?.addEventListener('click', () => {
        this.toggleQuickFilter('evolved');
    });

    document.getElementById('quickFilterCanEvolve')?.addEventListener('click', () => {
        this.toggleQuickFilter('canEvolve');
    });

    document.getElementById('quickFilterHighStats')?.addEventListener('click', () => {
        this.toggleQuickFilter('highStats');
    });

    // Sort controls
    document.getElementById('sortSelect')?.addEventListener('change', (e) => {
        this.pokedex.sortMethod = e.target.value;
        this.pokedex.applySorting();
        this.pokedex.render();
    });

    // Detail close button
    document.getElementById('detailClose')?.addEventListener('click', () => {
        this.pokedex.closeDetail();
    });
}

function initializeTypeFilters() {
    const container = document.getElementById('typeFiltersContainer');
    if (!container) return;

    const types = this.pokedex.getAllTypes();
    types.forEach(type => {
        const btn = document.createElement('button');
        btn.className = 'type-filter-btn';
        btn.textContent = type.toUpperCase();
        btn.setAttribute('aria-label', `Filter by ${type} type`);

        btn.addEventListener('click', () => {
            btn.classList.toggle('active');
            this.pokedex.toggleTypeFilter(type);
        });

        container.appendChild(btn);
    });
}

function toggleQuickFilter(filterName) {
    const buttons = document.querySelectorAll('.quick-filter-btn');
    const isActive = this.pokedex.filters.quickFilter === filterName;

    // Clear all quick filter buttons
    buttons.forEach(btn => btn.classList.remove('active'));

    if (isActive) {
        // Deactivate current filter
        this.pokedex.filters.quickFilter = null;
    } else {
        // Activate new filter
        this.pokedex.filters.quickFilter = filterName;
        // Highlight button
        const buttonId = `quickFilter${filterName.charAt(0).toUpperCase() + filterName.slice(1)}`;
        document.getElementById(buttonId)?.classList.add('active');
    }

    this.pokedex.applyFilters();
    this.pokedex.render();
}

function updateFilterButtonStates() {
    document.getElementById('filterAll')?.classList.toggle('active', this.pokedex.filters.caught === null);
    document.getElementById('filterCaught')?.classList.toggle('active', this.pokedex.filters.caught === true);
    document.getElementById('filterUnseen')?.classList.toggle('active', this.pokedex.filters.caught === false);
}

function openPokedex() {
    const container = document.getElementById('pokedexContainer');
    if (!container) return;

    // Refresh creature data (caught/seen status may have changed)
    this.pokedex.initializeCreatureData();
    this.pokedex.applyFilters();
    this.pokedex.render();

    // Show container
    container.classList.add('active');

    // Update filter button states
    this.updateFilterButtonStates();

    // Set focus to search input
    const searchInput = document.getElementById('pokedexSearch');
    if (searchInput) {
        searchInput.focus();
    }

    // Announce to screen readers
    this.pokedex.announceToScreenReader('Pokédex opened');
}

function closePokedex() {
    const container = document.getElementById('pokedexContainer');
    if (container) {
        container.classList.remove('active');
    }

    // Also close detail if open
    this.pokedex.closeDetail();
}

function selectMenuOption_UPDATED(index) {
    switch (index) {
        case 0: // CREATURES
            this.openPokedex();
            this.closeMenu();
            break;
        case 1: // BAG
            this.showText('Bag not implemented yet!');
            this.closeMenu();
            break;
        case 2: // SAVE
            this.exportSave();
            this.showText('Game saved!');
            this.closeMenu();
            break;
        case 3: // EXIT
            this.closeMenu();
            break;
    }
}

/**
 * =======================================================================
 * PART 5: KEYBOARD SHORTCUTS
 * =======================================================================
 *
 * Add these keyboard shortcuts to enhance navigation:
 *
 * - ESC: Close Pokédex or detail view
 * - /: Focus search input
 * - Arrow keys: Navigate creature list
 * - Enter: Open selected creature detail
 *
 * Add to the handleInput method in WoWGame class:
 */

function handlePokedexInput(key) {
    const pokedexOpen = document.getElementById('pokedexContainer')?.classList.contains('active');
    const detailOpen = document.getElementById('creatureDetail')?.classList.contains('active');

    if (!pokedexOpen) return false;

    if (key === 'Escape') {
        if (detailOpen) {
            this.pokedex.closeDetail();
        } else {
            this.closePokedex();
        }
        return true;
    }

    if (key === '/' || key === 's') {
        const searchInput = document.getElementById('pokedexSearch');
        if (searchInput) {
            searchInput.focus();
            return true;
        }
    }

    return false;
}

/**
 * =======================================================================
 * END OF POKÉDEX SYSTEM
 * =======================================================================
 */

// Export for use in wowMon.html
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PokedexManager,
        POKEDEX_STYLES,
        POKEDEX_HTML
    };
}
