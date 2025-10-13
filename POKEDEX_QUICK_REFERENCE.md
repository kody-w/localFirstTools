# WoWmon Pokédex System - Quick Reference Card

## Quick Integration Checklist

- [ ] Copy CSS from `wowmon_pokedex_system.js` → `<style>` section
- [ ] Copy HTML from `wowmon_pokedex_system.js` → `.ui-overlay` div
- [ ] Copy `PokedexManager` class → Before `WoWGame` class
- [ ] Add `this.pokedex = null;` to `WoWGame` constructor
- [ ] Add `initializePokedex()` after cartridge loads
- [ ] Add `setupPokedexEventListeners()` method
- [ ] Add helper methods: `openPokedex()`, `closePokedex()`, etc.
- [ ] Update `selectMenuOption()` to call `openPokedex()`
- [ ] Test: Press START → Select CREATURES

---

## Code Snippets

### 1. Initialize in Constructor
```javascript
constructor() {
    // ... existing code ...
    this.pokedex = null; // Initialize after cartridge loads
}
```

### 2. After Cartridge Loads
```javascript
autoLoadWoWmon() {
    this.cartridge = { /* ... */ };

    // ADD THIS:
    this.initializePokedex();
}

initializePokedex() {
    this.pokedex = new PokedexManager(this);
    this.setupPokedexEventListeners();
}
```

### 3. Update Menu Handler
```javascript
selectMenuOption(index) {
    switch (index) {
        case 0: // CREATURES
            this.openPokedex();  // CHANGE THIS LINE
            this.closeMenu();
            break;
        // ... rest of cases ...
    }
}
```

---

## API Reference

### PokedexManager Methods

#### Public Methods
```javascript
// Initialize/Refresh
pokedex.initializeCreatureData()    // Rebuild creature list from cartridge
pokedex.applyFilters()              // Apply current filters to list
pokedex.render()                    // Render current filtered list

// Search
pokedex.handleSearchInput(text)     // Debounced search handler
pokedex.addToSearchHistory(term)    // Add term to history

// Filtering
pokedex.toggleTypeFilter(type)      // Toggle type filter on/off
pokedex.clearAllFilters()           // Reset all filters
pokedex.getAllTypes()               // Get all unique types

// Sorting
pokedex.applySorting()              // Apply current sort method

// Display
pokedex.showCreatureDetail(creature) // Show detail view
pokedex.closeDetail()                // Close detail view

// Utility
pokedex.isCreatureCaught(id)        // Check if player caught creature
pokedex.isCreatureSeen(id)          // Check if player has seen creature
pokedex.getShareableURL()           // Get URL with current filters
pokedex.loadFromURL()               // Load filters from URL params
pokedex.announceToScreenReader(msg) // Announce to screen readers
```

#### Filter State
```javascript
pokedex.filters = {
    search: '',              // Search text
    caught: null,            // null=all, true=caught, false=unseen
    types: [],               // Array of type strings
    stats: {
        hp: 0,
        attack: 0,
        defense: 0,
        speed: 0
    },
    quickFilter: null        // 'starters' | 'evolved' | 'canEvolve' | 'highStats'
}
```

#### Sort Methods
```javascript
'number-asc'    // Pokédex number (ascending)
'number-desc'   // Pokédex number (descending)
'name-asc'      // Name A-Z
'name-desc'     // Name Z-A
'hp-asc'        // HP lowest first
'hp-desc'       // HP highest first
'attack-asc'    // Attack lowest first
'attack-desc'   // Attack highest first
'defense-asc'   // Defense lowest first
'defense-desc'  // Defense highest first
'speed-asc'     // Speed lowest first
'speed-desc'    // Speed highest first
```

### WoWGame Methods (Add These)

```javascript
// Core methods
game.initializePokedex()              // Initialize Pokédex system
game.setupPokedexEventListeners()     // Bind all event listeners
game.openPokedex()                    // Open Pokédex UI
game.closePokedex()                   // Close Pokédex UI

// Helper methods
game.initializeTypeFilters()          // Create type filter buttons
game.toggleQuickFilter(filterName)    // Toggle quick filter
game.updateFilterButtonStates()       // Update active filter buttons
game.handlePokedexInput(key)          // Handle keyboard input
```

---

## DOM Element IDs

### Containers
- `pokedexContainer` - Main Pokédex container
- `pokedexList` - Scrollable creature list
- `creatureDetail` - Detail view overlay
- `typeFiltersContainer` - Type filter button grid
- `statFiltersContainer` - Stat slider container

### Inputs
- `pokedexSearch` - Search text input
- `sortSelect` - Sort method dropdown
- `hpFilter`, `attackFilter`, `defenseFilter`, `speedFilter` - Stat sliders

### Buttons
- `searchClear` - Clear search button
- `filterAll`, `filterCaught`, `filterUnseen` - Status filters
- `filterTypes`, `filterStats` - Toggle filter sections
- `sortDirection` - Sort direction toggle
- `quickFilterStarters`, `quickFilterEvolved`, `quickFilterCanEvolve`, `quickFilterHighStats` - Quick filters
- `detailClose` - Close detail view

### Display Elements
- `resultsCount` - Number of filtered creatures
- `detailCreatureName` - Creature name in detail view
- `detailBody` - Detail view content

---

## CSS Classes

### States
- `.active` - Show/activate element
- `.selected` - Currently selected item
- `.locked` - Creature not yet seen

### Components
- `.pokedex-container` - Main container
- `.pokedex-search` - Search section
- `.filter-btn` - Main filter buttons
- `.type-filter-btn` - Type filter buttons
- `.quick-filter-btn` - Quick filter buttons
- `.creature-entry` - Individual creature in list
- `.creature-detail` - Detail view
- `.stat-filter-slider` - Stat range sliders

---

## Event Flow

### Opening Pokédex
1. User presses START → Opens menu
2. User selects "CREATURES"
3. `selectMenuOption(0)` called
4. Calls `openPokedex()`
5. Refreshes creature data
6. Applies filters
7. Renders list
8. Shows container
9. Focuses search input

### Searching
1. User types in search box
2. Input event fires
3. Calls `handleSearchInput(text)`
4. Debounce timer starts (300ms)
5. Timer expires → applies filters
6. Calls `applyFilters()`
7. Calls `render()`
8. Updates creature list
9. Adds to search history

### Filtering
1. User clicks filter button
2. Click event fires
3. Updates filter state
4. Calls `applyFilters()`
5. Calls `render()`
6. Updates UI to show results

### Viewing Details
1. User clicks creature
2. Click event fires
3. Calls `showCreatureDetail(creature)`
4. Builds detail HTML
5. Shows detail overlay
6. Announces to screen reader

---

## Common Patterns

### Add New Filter Type
```javascript
// 1. Add to filters object
this.filters.myFilter = false;

// 2. Add HTML button
<button id="myFilterBtn">MY FILTER</button>

// 3. Add event listener
document.getElementById('myFilterBtn')?.addEventListener('click', () => {
    this.pokedex.filters.myFilter = !this.pokedex.filters.myFilter;
    this.pokedex.applyFilters();
    this.pokedex.render();
});

// 4. Add filter logic
if (this.filters.myFilter) {
    results = results.filter(c => /* your logic */);
}
```

### Add New Sort Method
```javascript
// 1. Add option to select
<option value="total-desc">Total Stats (Highest)</option>

// 2. Add case to applySorting()
case 'total':
    comparison = (a.hp + a.attack + a.defense + a.speed) -
                 (b.hp + b.attack + b.defense + b.speed);
    break;
```

### Refresh After Catching Creature
```javascript
// After catching creature
game.pokedex.initializeCreatureData(); // Refresh caught status
game.pokedex.applyFilters();
game.pokedex.render();
```

---

## Debug Commands

### Console Commands
```javascript
// View filter state
game.pokedex.filters

// View all creatures
game.pokedex.allCreatures

// View filtered creatures
game.pokedex.filteredCreatures

// Test search
game.pokedex.handleSearchInput('murloc')

// Clear all filters
game.pokedex.clearAllFilters()

// Get shareable URL
game.pokedex.getShareableURL()

// Check if creature caught
game.pokedex.isCreatureCaught('murloc')
```

---

## Performance Tips

1. **Debounce Search**: Already implemented (300ms)
2. **Lazy Initialize**: Type filters created on first view
3. **Minimal Re-renders**: Only render when data changes
4. **Efficient Filtering**: Use array methods efficiently
5. **Event Delegation**: Use on parent containers when possible

---

## Accessibility Checklist

- [ ] All buttons have `aria-label` attributes
- [ ] Containers have appropriate `role` attributes
- [ ] Search input has `aria-label`
- [ ] Focus visible on all interactive elements
- [ ] Keyboard navigation works (Tab, Enter, ESC)
- [ ] Screen reader announcements for state changes
- [ ] High contrast mode supported
- [ ] Text readable at 200% zoom

---

## Testing Checklist

### Functionality
- [ ] Search finds creatures by name
- [ ] Search finds creatures by number
- [ ] Fuzzy search handles typos
- [ ] Status filters work (All, Caught, Unseen)
- [ ] Type filters work (single and multiple)
- [ ] Stat filters work (all four stats)
- [ ] Quick filters work (all four presets)
- [ ] Sort dropdown changes order
- [ ] Detail view shows correct info
- [ ] Close buttons work
- [ ] ESC key closes views

### Data
- [ ] All creatures appear in list
- [ ] Caught status accurate
- [ ] Seen status accurate
- [ ] Stats display correctly
- [ ] Types display correctly
- [ ] Evolution info correct
- [ ] Moves list correct

### UI
- [ ] Game Boy aesthetic maintained
- [ ] Colors match game style
- [ ] Layout responsive
- [ ] Buttons have hover states
- [ ] Active states visible
- [ ] Scrolling smooth
- [ ] Empty state shows when no results

### Performance
- [ ] No lag when typing
- [ ] Filters apply instantly
- [ ] List scrolls smoothly
- [ ] No memory leaks
- [ ] Works with 100+ creatures

---

## File Locations in wowMon.html

| Content | Approximate Line | Section |
|---------|-----------------|---------|
| CSS Styles | 500-800 | `<style>` |
| HTML Structure | 850-960 | `.ui-overlay` |
| PokedexManager Class | 1400-2000 | `<script>` |
| WoWGame Constructor | 1380-1400 | class WoWGame |
| autoLoadWoWmon() | 1600-2400 | WoWGame methods |
| selectMenuOption() | 3876-3895 | WoWGame methods |
| handleInput() | 4200-4300 | WoWGame methods |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Pokédex won't open | Check `initializePokedex()` called after cartridge loads |
| Search not working | Verify `pokedexSearch` element exists with correct ID |
| No creatures showing | Check `allCreatures` array populated |
| Filters not working | Console log `game.pokedex.filters` to debug state |
| Styling broken | Verify CSS variables defined in `:root` |
| Detail won't close | Check ESC handler added to input system |

---

## Support Resources

1. Full Integration Guide: `POKEDEX_INTEGRATION_GUIDE.md`
2. Complete Code: `wowmon_pokedex_system.js`
3. Browser Console: Use debug commands above
4. Test in Multiple Browsers: Chrome, Firefox, Safari

---

**Quick Reference Card v1.0.0**
