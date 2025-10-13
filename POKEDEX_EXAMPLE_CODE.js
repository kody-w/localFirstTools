/**
 * ============================================================================
 * WOWMON POKÉDEX SYSTEM - EXAMPLE IMPLEMENTATION
 * ============================================================================
 *
 * This file shows example code snippets demonstrating how the Pokédex system
 * works in practice. Use these examples as reference during integration.
 *
 * NOTE: This is NOT a complete file. It shows key code sections only.
 * ============================================================================
 */

// ============================================================================
// EXAMPLE 1: Initializing the Pokédex
// ============================================================================

class WoWGame {
    constructor() {
        // Existing game initialization
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.state = 'LOADING';

        // Pokédex initialization (will be set after cartridge loads)
        this.pokedex = null;

        // Load cartridge
        this.autoLoadWoWmon();
    }

    autoLoadWoWmon() {
        // Cartridge data with creatures
        this.cartridge = {
            "name": "WoWmon",
            "creatures": {
                "murloc": {
                    "id": "murloc",
                    "name": "MURLOC",
                    "type": ["water", "beast"],
                    "baseHp": 45,
                    "baseAttack": 49,
                    "baseDefense": 49,
                    "baseSpeed": 45,
                    "moves": ["tackle", "bubble", "water_gun", "bite"],
                    "description": "The amphibious Murloc makes strange gurgling sounds."
                },
                // ... more creatures ...
            },
            "moves": { /* ... */ },
            "starters": ["murloc", "wisp", "imp"]
        };

        // Initialize Pokédex AFTER cartridge is loaded
        this.initializePokedex();
    }

    initializePokedex() {
        // Create Pokédex manager
        this.pokedex = new PokedexManager(this);

        // Setup all event listeners
        this.setupPokedexEventListeners();

        console.log('Pokédex initialized with', this.pokedex.allCreatures.length, 'creatures');
    }
}

// ============================================================================
// EXAMPLE 2: Setting Up Event Listeners
// ============================================================================

setupPokedexEventListeners() {
    // 1. SEARCH INPUT - Real-time search with debouncing
    const searchInput = document.getElementById('pokedexSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            // This will debounce automatically (300ms delay)
            this.pokedex.handleSearchInput(e.target.value);
        });
    }

    // 2. CLEAR SEARCH BUTTON
    const searchClear = document.getElementById('searchClear');
    if (searchClear) {
        searchClear.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            this.pokedex.filters.search = '';
            this.pokedex.applyFilters();
            this.pokedex.render();
        });
    }

    // 3. STATUS FILTER BUTTONS
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

    // 4. TYPE FILTER TOGGLE
    document.getElementById('filterTypes')?.addEventListener('click', () => {
        const typeContainer = document.getElementById('typeFiltersContainer');
        if (typeContainer) {
            const isHidden = typeContainer.style.display === 'none';
            typeContainer.style.display = isHidden ? 'grid' : 'none';

            // Create type filter buttons on first show
            if (isHidden && typeContainer.children.length === 0) {
                this.initializeTypeFilters();
            }
        }
    });

    // 5. STAT FILTER SLIDERS
    ['hp', 'attack', 'defense', 'speed'].forEach(stat => {
        const slider = document.getElementById(`${stat}Filter`);
        const valueDisplay = document.getElementById(`${stat}FilterValue`);

        if (slider && valueDisplay) {
            slider.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                valueDisplay.textContent = value === 0 ? 'Any' : `${value}+`;
                this.pokedex.filters.stats[stat] = value;

                // Real-time filtering
                this.pokedex.applyFilters();
                this.pokedex.render();
            });
        }
    });

    // 6. QUICK FILTERS
    document.getElementById('quickFilterStarters')?.addEventListener('click', () => {
        this.toggleQuickFilter('starters');
    });

    document.getElementById('quickFilterEvolved')?.addEventListener('click', () => {
        this.toggleQuickFilter('evolved');
    });

    // 7. SORT CONTROLS
    document.getElementById('sortSelect')?.addEventListener('change', (e) => {
        this.pokedex.sortMethod = e.target.value;
        this.pokedex.applySorting();
        this.pokedex.render();
    });

    // 8. DETAIL VIEW CLOSE
    document.getElementById('detailClose')?.addEventListener('click', () => {
        this.pokedex.closeDetail();
    });
}

// ============================================================================
// EXAMPLE 3: Opening and Closing Pokédex
// ============================================================================

openPokedex() {
    const container = document.getElementById('pokedexContainer');
    if (!container) {
        console.error('Pokédex container not found!');
        return;
    }

    console.log('Opening Pokédex...');

    // Refresh creature data (caught/seen status may have changed)
    this.pokedex.initializeCreatureData();

    // Apply current filters
    this.pokedex.applyFilters();

    // Render the list
    this.pokedex.render();

    // Show the container
    container.classList.add('active');

    // Update button visual states
    this.updateFilterButtonStates();

    // Focus the search input for immediate use
    const searchInput = document.getElementById('pokedexSearch');
    if (searchInput) {
        setTimeout(() => searchInput.focus(), 100);
    }

    // Announce to screen readers
    this.pokedex.announceToScreenReader('Pokédex opened');
}

closePokedex() {
    const container = document.getElementById('pokedexContainer');
    if (container) {
        container.classList.remove('active');
    }

    // Also close detail view if open
    this.pokedex.closeDetail();

    console.log('Pokédex closed');
}

// ============================================================================
// EXAMPLE 4: Menu Integration
// ============================================================================

selectMenuOption(index) {
    switch (index) {
        case 0: // CREATURES
            console.log('Opening Pokédex from menu...');
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

// ============================================================================
// EXAMPLE 5: Filtering Examples
// ============================================================================

// Example: Search for "mur"
function exampleSearch() {
    // User types "mur" in search box
    game.pokedex.handleSearchInput('mur');

    // After 300ms debounce:
    // Filters creatures matching "mur"
    // Results: Murloc, Murloc Warrior, Murloc King
}

// Example: Filter by type
function exampleTypeFilter() {
    // User selects "water" and "beast" types
    game.pokedex.filters.types = ['water', 'beast'];
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: All creatures with water OR beast type
    // (Murloc, Wolf, Gnoll, Naga, etc.)
}

// Example: Filter by stats
function exampleStatFilter() {
    // User sets Attack slider to 70
    game.pokedex.filters.stats.attack = 70;
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: Only creatures with baseAttack >= 70
    // (Murloc King, Felguard, Dire Wolf, etc.)
}

// Example: Combine filters
function exampleCombinedFilters() {
    // Search + Type + Stats
    game.pokedex.filters.search = 'wolf';
    game.pokedex.filters.types = ['beast'];
    game.pokedex.filters.stats.attack = 60;
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: Creatures matching ALL conditions:
    // - Name contains "wolf" AND
    // - Type is "beast" AND
    // - Attack >= 60
    // Result: Wolf, Dire Wolf
}

// ============================================================================
// EXAMPLE 6: Sorting Examples
// ============================================================================

// Sort by HP (highest first)
function exampleSortByHP() {
    game.pokedex.sortMethod = 'hp-desc';
    game.pokedex.applySorting();
    game.pokedex.render();

    // Results sorted: Murloc King (80 HP), Dire Wolf (75 HP), etc.
}

// Sort by name A-Z
function exampleSortByName() {
    game.pokedex.sortMethod = 'name-asc';
    game.pokedex.applySorting();
    game.pokedex.render();

    // Results sorted: Ancient Wisp, Dire Wolf, Elemental, etc.
}

// ============================================================================
// EXAMPLE 7: Quick Filters
// ============================================================================

// Show only starter creatures
function exampleStarterFilter() {
    game.pokedex.filters.quickFilter = 'starters';
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: Murloc, Wisp, Imp
}

// Show fully evolved creatures
function exampleFullyEvolvedFilter() {
    game.pokedex.filters.quickFilter = 'evolved';
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: Creatures where evolveTo === null
    // (Murloc King, Ancient Wisp, Felguard, etc.)
}

// Show high stat creatures
function exampleHighStatsFilter() {
    game.pokedex.filters.quickFilter = 'highStats';
    game.pokedex.applyFilters();
    game.pokedex.render();

    // Results: Creatures with total base stats > 300
}

// ============================================================================
// EXAMPLE 8: Viewing Creature Details
// ============================================================================

function exampleShowDetail() {
    // Get a creature
    const murloc = game.pokedex.allCreatures.find(c => c.id === 'murloc');

    // Show detail view
    game.pokedex.showCreatureDetail(murloc);

    // Detail view displays:
    // - Name: MURLOC
    // - Number: #001
    // - Types: WATER, BEAST
    // - Description
    // - Base stats with visual bars
    // - Evolution info (→ Murloc Warrior at level 16)
    // - Move list
    // - Collection status
}

// ============================================================================
// EXAMPLE 9: Keyboard Navigation
// ============================================================================

handlePokedexInput(key) {
    const pokedexOpen = document.getElementById('pokedexContainer')?.classList.contains('active');
    const detailOpen = document.getElementById('creatureDetail')?.classList.contains('active');

    if (!pokedexOpen) return false;

    // ESC - Close detail or Pokédex
    if (key === 'Escape') {
        if (detailOpen) {
            this.pokedex.closeDetail();
        } else {
            this.closePokedex();
        }
        return true;
    }

    // / or S - Focus search
    if (key === '/' || key === 's') {
        const searchInput = document.getElementById('pokedexSearch');
        if (searchInput) {
            searchInput.focus();
            return true;
        }
    }

    return false;
}

// Add to main input handler
handleInput(key) {
    // Let Pokédex handle input first
    const pokedexHandled = this.handlePokedexInput(key);
    if (pokedexHandled) return;

    // ... existing input handling ...
}

// ============================================================================
// EXAMPLE 10: Helper Methods
// ============================================================================

initializeTypeFilters() {
    const container = document.getElementById('typeFiltersContainer');
    if (!container) return;

    // Get all unique types from creatures
    const types = this.pokedex.getAllTypes();
    // Result: ['water', 'beast', 'fire', 'demon', 'nature', 'spirit', ...]

    types.forEach(type => {
        const btn = document.createElement('button');
        btn.className = 'type-filter-btn';
        btn.textContent = type.toUpperCase();
        btn.setAttribute('aria-label', `Filter by ${type} type`);

        btn.addEventListener('click', () => {
            // Toggle active state
            btn.classList.toggle('active');

            // Toggle filter
            this.pokedex.toggleTypeFilter(type);
        });

        container.appendChild(btn);
    });
}

toggleQuickFilter(filterName) {
    const buttons = document.querySelectorAll('.quick-filter-btn');
    const isActive = this.pokedex.filters.quickFilter === filterName;

    // Clear all button active states
    buttons.forEach(btn => btn.classList.remove('active'));

    if (isActive) {
        // Deactivate filter
        this.pokedex.filters.quickFilter = null;
    } else {
        // Activate filter
        this.pokedex.filters.quickFilter = filterName;

        // Highlight button
        const buttonId = `quickFilter${filterName.charAt(0).toUpperCase() + filterName.slice(1)}`;
        document.getElementById(buttonId)?.classList.add('active');
    }

    this.pokedex.applyFilters();
    this.pokedex.render();
}

updateFilterButtonStates() {
    // Update visual state of filter buttons
    document.getElementById('filterAll')?.classList.toggle('active',
        this.pokedex.filters.caught === null);

    document.getElementById('filterCaught')?.classList.toggle('active',
        this.pokedex.filters.caught === true);

    document.getElementById('filterUnseen')?.classList.toggle('active',
        this.pokedex.filters.caught === false);
}

// ============================================================================
// EXAMPLE 11: Fuzzy Search in Action
// ============================================================================

function demonstrateFuzzySearch() {
    const pokedex = game.pokedex;

    // Exact match
    console.log(pokedex.fuzzyMatch('murloc', 'murloc')); // true

    // Typo with 1 character off
    console.log(pokedex.fuzzyMatch('murloc', 'murlic')); // true (one char different)

    // Typo with 2 characters off
    console.log(pokedex.fuzzyMatch('murloc', 'murlic')); // true (two chars different)

    // Too many differences
    console.log(pokedex.fuzzyMatch('murloc', 'mxrxlx')); // false (three chars different)

    // Substring match (always works)
    console.log('murloc'.includes('mur')); // true

    // Real search examples:
    // "mur" finds: Murloc, Murloc Warrior, Murloc King
    // "wlf" finds: Wolf (fuzzy match), Dire Wolf
    // "ancent" finds: Ancient Wisp (fuzzy match for "ancient")
}

// ============================================================================
// EXAMPLE 12: URL Parameters
// ============================================================================

function exampleShareableURL() {
    // Setup some filters
    game.pokedex.filters.search = 'murloc';
    game.pokedex.filters.types = ['water', 'beast'];
    game.pokedex.sortMethod = 'hp-desc';

    // Get shareable URL
    const url = game.pokedex.getShareableURL();
    console.log(url);
    // Result: "https://example.com/wowmon.html?search=murloc&types=water,beast&sort=hp-desc"

    // Copy to clipboard
    navigator.clipboard.writeText(url);
}

function exampleLoadFromURL() {
    // If URL has parameters:
    // https://example.com/wowmon.html?search=wolf&caught=true&sort=attack-desc

    // Load filters from URL
    game.pokedex.loadFromURL();

    // Filters will be set:
    // - search: "wolf"
    // - caught: true
    // - sortMethod: "attack-desc"

    // And Pokédex will render with these filters applied
}

// ============================================================================
// EXAMPLE 13: Search History
// ============================================================================

function exampleSearchHistory() {
    // User searches for various terms
    game.pokedex.handleSearchInput('murloc');
    game.pokedex.handleSearchInput('wolf');
    game.pokedex.handleSearchInput('elemental');

    // History is saved
    console.log(game.pokedex.searchHistory);
    // Result: ['elemental', 'wolf', 'murloc']

    // History is persisted to localStorage
    // Key: 'wowmon_search_history'
    // Max size: 10 entries

    // On next visit, history is loaded automatically
    game.pokedex.loadSearchHistory();
}

// ============================================================================
// EXAMPLE 14: After Catching a Creature
// ============================================================================

function onCreatureCaught(creatureId) {
    console.log('Caught creature:', creatureId);

    // Update player data
    this.player.creatures.push(newCreature);
    this.player.stats.creaturesCaught++;

    if (!this.player.stats.uniqueCreaturesCaught.includes(creatureId)) {
        this.player.stats.uniqueCreaturesCaught.push(creatureId);
    }

    // If Pokédex is open, refresh it
    if (document.getElementById('pokedexContainer')?.classList.contains('active')) {
        this.pokedex.initializeCreatureData(); // Refresh caught status
        this.pokedex.applyFilters();
        this.pokedex.render();
    }
}

// ============================================================================
// EXAMPLE 15: Debugging
// ============================================================================

function debugPokedex() {
    const game = window.game; // Assuming game is global

    // View all creatures
    console.table(game.pokedex.allCreatures);

    // View filtered creatures
    console.table(game.pokedex.filteredCreatures);

    // View filter state
    console.log('Current filters:', game.pokedex.filters);

    // View sort method
    console.log('Sort method:', game.pokedex.sortMethod);

    // Test search
    game.pokedex.handleSearchInput('test');

    // Check caught status
    const caught = game.pokedex.allCreatures.filter(c => c.caught);
    console.log('Caught creatures:', caught);

    // Check unseen
    const unseen = game.pokedex.allCreatures.filter(c => !c.seen);
    console.log('Unseen creatures:', unseen);

    // Get types
    console.log('All types:', game.pokedex.getAllTypes());

    // Test filter
    game.pokedex.filters.stats.hp = 60;
    game.pokedex.applyFilters();
    console.log('Creatures with HP >= 60:', game.pokedex.filteredCreatures);
}

// ============================================================================
// EXAMPLE 16: Performance Monitoring
// ============================================================================

function monitorPerformance() {
    // Time search operation
    console.time('Search');
    game.pokedex.handleSearchInput('murloc');
    console.timeEnd('Search');

    // Time filtering
    console.time('Filter');
    game.pokedex.applyFilters();
    console.timeEnd('Filter');

    // Time rendering
    console.time('Render');
    game.pokedex.render();
    console.timeEnd('Render');

    // Check number of event listeners
    console.log('Search history size:', game.pokedex.searchHistory.length);
}

// ============================================================================
// EXAMPLE 17: Custom Extensions
// ============================================================================

// Add custom filter for legendary creatures
function addLegendaryFilter() {
    // 1. Add to filters
    game.pokedex.filters.legendary = false;

    // 2. Add HTML button (do this in the HTML)
    // <button id="filterLegendary">LEGENDARY</button>

    // 3. Add event listener
    document.getElementById('filterLegendary')?.addEventListener('click', () => {
        game.pokedex.filters.legendary = !game.pokedex.filters.legendary;
        game.pokedex.applyFilters();
        game.pokedex.render();
    });

    // 4. Add filter logic to PokedexManager.applyFilters()
    // if (this.filters.legendary) {
    //     results = results.filter(c => c.legendary === true);
    // }
}

// Add custom sort for total stats
function addTotalStatsSort() {
    // 1. Add option to HTML
    // <option value="total-desc">Total Stats</option>

    // 2. Add case to PokedexManager.applySorting()
    // case 'total':
    //     comparison = (a.hp + a.attack + a.defense + a.speed) -
    //                  (b.hp + b.attack + b.defense + b.speed);
    //     break;
}

// ============================================================================
// EXAMPLE 18: Accessibility Features
// ============================================================================

function demonstrateAccessibility() {
    // Announce to screen readers
    game.pokedex.announceToScreenReader('Found 5 creatures');

    // Focus management
    const searchInput = document.getElementById('pokedexSearch');
    searchInput.focus(); // Focus on search when opening

    // Keyboard navigation
    // Tab - Move through interactive elements
    // Enter - Activate buttons/open detail
    // ESC - Close detail or Pokédex
    // / or S - Focus search

    // ARIA labels
    // All buttons have aria-label
    // Containers have role attributes
    // Live region for announcements

    // High contrast mode
    // body.high-contrast class changes colors
    document.body.classList.toggle('high-contrast');
}

// ============================================================================
// END OF EXAMPLES
// ============================================================================

/**
 * These examples demonstrate the key functionality of the Pokédex system.
 * Use them as reference when implementing or debugging the system.
 *
 * For full implementation details, see:
 * - wowmon_pokedex_system.js (complete code)
 * - POKEDEX_INTEGRATION_GUIDE.md (step-by-step guide)
 * - POKEDEX_QUICK_REFERENCE.md (quick lookup)
 */
