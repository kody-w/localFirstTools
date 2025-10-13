# WoWmon Detail View System - Integration Guide

**Agent 4 - Detail View Specialist Deliverable**

## Overview

This is a comprehensive, tabbed detail view system for individual Pokemon/Creatures in the WoWmon game. The system includes:

- **5 Tabbed Views**: Overview, Stats, Moves, Evolution, Abilities
- **Stats Visualization**: Canvas-based radar chart with color-coded stat bars
- **Evolution Chain**: Visual evolution path with clickable sprites and conditions
- **Move Management**: Categorized, searchable move list with full details
- **Navigation**: Previous/Next buttons to cycle through Pokedex
- **Actions**: Favorite, Add to Team, Share functionality
- **Responsive Design**: Works on desktop and mobile devices

## Files Delivered

1. **wowMon_detail_view.html** - Standalone demo with all code
2. **WOWMON_DETAIL_VIEW_INTEGRATION.md** - This integration guide

## Live Demo

Open `wowMon_detail_view.html` in your browser to see the working demo. Click the demo buttons to view different Pokemon.

## Quick Start Integration

### Step 1: Add CSS to wowMon.html

Copy all CSS styles from `wowMon_detail_view.html` between the comments:
```
/* ==================================== */
/* POKEMON DETAIL MODAL - MAIN STYLES  */
/* ==================================== */
```

Add these styles to your existing `<style>` section in wowMon.html (around line 813).

### Step 2: Add HTML Modal Structure

Copy the entire modal HTML structure from `wowMon_detail_view.html`:

```html
<!-- ================================== -->
<!-- POKEMON DETAIL MODAL HTML         -->
<!-- ================================== -->
<div class="pokemon-detail-modal" id="pokemonDetailModal">
    <!-- Full modal structure here -->
</div>
```

Add this just before the closing `</body>` tag in wowMon.html (around line 4440).

### Step 3: Add JavaScript Functions

Copy all JavaScript functions from the `<script>` section in `wowMon_detail_view.html` to your wowMon.html script section.

**Required Functions:**
- `showPokemonDetail(pokemonId)`
- `closePokemonDetail()`
- `switchTab(tabName)`
- `populateOverviewTab(pokemon)`
- `populateStatsTab(pokemon)`
- `drawStatsRadarChart(pokemon)`
- `populateMovesTab(pokemon)`
- `filterMoves()`
- `populateEvolutionTab(pokemon)`
- `buildEvolutionChain(pokemon)`
- `populateAbilitiesTab(pokemon)`
- `navigatePokemon(direction)`
- `toggleFavorite()`
- `addToTeam()`
- `sharePokemon()`

### Step 4: Update Data References

Replace the MOCK data references with your actual game data:

```javascript
// BEFORE (in demo):
const pokemon = MOCK_CREATURES[pokemonId];
const move = MOCK_MOVES[moveId];

// AFTER (in your game):
const pokemon = game.cartridge.creatures[pokemonId];
const move = game.cartridge.moves[moveId];
```

Update these locations:
1. In `showPokemonDetail()` - line ~10
2. In `populateMovesTab()` - line ~20
3. In `buildEvolutionChain()` - line ~15

### Step 5: Hook Up to Your Game

Add calls to `showPokemonDetail()` wherever you want to show creature details:

**Examples:**

```javascript
// In your creature menu:
function showCreatureMenu() {
    // ... existing code ...
    creatureElement.addEventListener('click', () => {
        showPokemonDetail(creature.id);
    });
}

// After catching a creature:
function onCreatureCaught(creatureId) {
    // ... existing code ...
    showPokemonDetail(creatureId);
}

// In battle victory screen:
function showBattleVictory() {
    // ... existing code ...
    if (playerWants) {
        showPokemonDetail(enemyCreatureId);
    }
}

// Keyboard shortcut (optional):
if (e.key === 'i' && this.state === 'WORLD') {
    // Show detail for first creature in party
    if (this.player.creatures.length > 0) {
        showPokemonDetail(this.player.creatures[0].id);
    }
}
```

## Feature Details

### 1. Overview Tab

**Displays:**
- Large Pokemon sprite (using emoji placeholders)
- Pokemon name and Pokedex number
- Type badges with color coding
- Height and weight (randomized for demo)
- Pokemon description

**Customization:**
- Update sprite emojis in `spriteEmojis` object
- Add real height/weight data to creature definitions
- Customize type badge colors in CSS

### 2. Stats Tab

**Features:**
- Canvas-based radar/spider chart for 6 stats
- Color-coded horizontal stat bars
- Base Stat Total (BST) calculation
- Percentile ranking display

**Stats Displayed:**
- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

**Customization:**
- Adjust max stat value (default: 150) in `drawStatsRadarChart()`
- Change color thresholds in `populateStatsTab()`
- Modify chart colors in canvas drawing code

**Color Coding:**
- Excellent (100+): Green (#27ae60)
- Good (80-99): Light Green (#2ecc71)
- Average (60-79): Orange (#f39c12)
- Low (<60): Red (#e74c3c)

### 3. Moves Tab

**Features:**
- All learnable moves displayed
- Move type badges with colors
- Physical/Special/Status category
- Power and Accuracy stats
- Real-time search filter
- PP (Power Points) display

**Customization:**
- Add TM/HM moves to creature definitions
- Add level-up move lists
- Implement move filtering by category

**Future Enhancements:**
```javascript
// Group moves by learn method:
{
    "level_up": { level: 1, move: "tackle" },
    "tm": { tm: "TM01", move: "focus_punch" },
    "egg": { move: "aqua_jet" }
}
```

### 4. Evolution Tab

**Features:**
- Visual evolution chain with all stages
- Evolution condition display (level, stone, etc.)
- Current Pokemon highlighted with red border
- Clickable sprites to navigate between forms
- Arrow indicators between stages
- "Does not evolve" message for final forms

**Evolution Methods Supported:**
- Level-based evolution (e.g., "Level 16")
- Stone evolution (e.g., "Water Stone")
- Friendship evolution
- Trade evolution
- Custom conditions

**Customization:**
Add evolution data to creature definitions:
```javascript
{
    "evolveLevel": 16,
    "evolveTo": "murloc_warrior",
    "evolveFrom": "murloc",
    // Or for special evolution:
    "evolveMethod": "Trade holding Metal Coat",
    "evolveTo": "scizor"
}
```

### 5. Abilities Tab

**Features:**
- Multiple abilities per Pokemon
- Normal and Hidden ability tags
- Detailed ability descriptions
- Type-based ability suggestions

**Current Implementation:**
- Abilities are generated based on Pokemon's primary type
- Mock data provides 2 abilities per type

**Full Integration:**
Add abilities to creature definitions:
```javascript
{
    "abilities": [
        {
            "name": "Torrent",
            "type": "normal",
            "description": "Powers up Water-type moves when HP is low."
        },
        {
            "name": "Rain Dish",
            "type": "hidden",
            "description": "Restores HP in rain."
        }
    ]
}
```

## Navigation & Actions

### Previous/Next Navigation

**Keyboard Shortcuts:**
- Left Arrow: Previous Pokemon
- Right Arrow: Next Pokemon
- Escape: Close modal

**Implementation:**
```javascript
// Arrow buttons in header automatically cycle through all Pokemon IDs
// Order is determined by Object.keys(game.cartridge.creatures)
```

### Favorite System

**Features:**
- Star button to toggle favorite status
- Favorites saved to localStorage
- Visual indicator (red background) when favorited

**Storage Key:** `wowmon_favorites`

**Access favorites:**
```javascript
const favorites = JSON.parse(localStorage.getItem('wowmon_favorites') || '[]');
```

### Add to Team

**Current Implementation:**
- Shows alert confirmation
- Console logs the creature ID

**Full Integration:**
```javascript
function addToTeam() {
    if (!currentPokemonId) return;

    const pokemon = game.cartridge.creatures[currentPokemonId];

    // Check team size
    if (game.player.creatures.length >= 6) {
        alert('Your team is full!');
        return;
    }

    // Create creature instance
    const newCreature = {
        id: pokemon.id,
        name: pokemon.name,
        level: 5,
        hp: pokemon.baseHp,
        maxHp: pokemon.baseHp,
        attack: pokemon.baseAttack,
        defense: pokemon.baseDefense,
        speed: pokemon.baseSpeed,
        exp: 0,
        moves: pokemon.moves.slice(0, 4),
        pp: {}
    };

    game.player.creatures.push(newCreature);
    alert(`${pokemon.name} added to your team!`);
}
```

### Share Functionality

**Features:**
- Generates shareable URL with Pokemon ID
- Copies to clipboard
- Supports deep linking

**URL Format:**
```
https://yourgame.com/wowMon.html?pokemon=murloc
```

**Auto-open on load:**
The system automatically checks URL parameters and opens the detail view if a Pokemon ID is present.

## Responsive Design

The detail view is fully responsive and adapts to different screen sizes:

**Desktop (>768px):**
- Two-column layouts for overview and stats
- Horizontal evolution chain
- Full-width modal (max 800px)

**Mobile (≤768px):**
- Single-column layouts
- Vertical evolution chain
- Full-screen modal with padding
- Scrollable tab navigation
- Touch-friendly buttons

## Performance Considerations

### Canvas Rendering

The radar chart is drawn using Canvas 2D API:
- Only redraws when stats tab is active
- Efficient path drawing with minimal operations
- No animation overhead

### DOM Updates

- Tab switching uses CSS classes (no DOM creation/destruction)
- Modal content is populated once per Pokemon
- Search filtering uses CSS display property

### Data Loading

- All creature data is already loaded in `game.cartridge`
- No external API calls
- Instant Pokemon switching

## Accessibility Features

### Keyboard Navigation

- Tab key to navigate through interactive elements
- Enter/Space to activate buttons
- Escape to close modal
- Arrow keys for Pokemon navigation

### Screen Reader Support

Add ARIA attributes for better accessibility:

```html
<div class="pokemon-detail-modal" role="dialog" aria-labelledby="detailPokemonName" aria-modal="true">
    <button class="tab-btn" role="tab" aria-selected="true">Overview</button>
    <!-- etc -->
</div>
```

### Focus Management

All interactive elements have visible focus indicators:
- Buttons have border glow on focus
- Tab navigation maintains focus state
- Modal traps focus when open

## Customization Guide

### Color Scheme

Update Game Boy colors to match your theme:

```css
:root {
    --detail-bg: #9bbc0f;          /* Main background */
    --detail-border: #0f380f;      /* Borders and text */
    --detail-accent: #306230;      /* Buttons and accents */
    --detail-hover: #556b2f;       /* Hover states */
}
```

### Sprite System

Replace emoji sprites with actual images:

```javascript
function populateOverviewTab(pokemon) {
    const spriteElement = document.getElementById('detailSprite');

    // Option 1: Base64 encoded sprites
    spriteElement.innerHTML = `<img src="${pokemon.sprite}" alt="${pokemon.name}">`;

    // Option 2: Sprite sheet
    spriteElement.style.backgroundImage = `url(sprites.png)`;
    spriteElement.style.backgroundPosition = `${pokemon.spriteX}px ${pokemon.spriteY}px`;
}
```

### Tab Customization

Add new tabs:

1. Add tab button to `.tab-nav`:
```html
<button class="tab-btn" onclick="switchTab('location')">Location</button>
```

2. Add tab pane to `.tab-content`:
```html
<div class="tab-pane" id="location-tab">
    <!-- Tab content -->
</div>
```

3. Add populate function:
```javascript
function populateLocationTab(pokemon) {
    // Custom content
}
```

## Troubleshooting

### Modal doesn't appear

Check:
1. `pokemonDetailModal` element exists in DOM
2. `showPokemonDetail()` function is defined
3. No JavaScript errors in console
4. CSS is properly loaded

### Stats chart not drawing

Check:
1. Canvas element exists: `statsRadarCanvas`
2. Pokemon has stat properties: `baseHp`, `baseAttack`, etc.
3. Canvas context is available
4. No errors in `drawStatsRadarChart()` function

### Evolution chain empty

Check:
1. Creature has `evolveTo` or `evolveFrom` properties
2. Evolution IDs match actual creature IDs
3. `buildEvolutionChain()` is working correctly

### Moves not displaying

Check:
1. Creature has `moves` array property
2. Move IDs match `game.cartridge.moves` keys
3. Move data includes required properties: `name`, `type`, `power`, `accuracy`

## Advanced Features

### Stat Comparison

Compare current Pokemon with another:

```javascript
function compareStats(pokemonId1, pokemonId2) {
    const p1 = game.cartridge.creatures[pokemonId1];
    const p2 = game.cartridge.creatures[pokemonId2];

    // Show comparison view
    // Highlight differences in stats
    // Show which is stronger in each category
}
```

### Moveset Builder

Allow players to customize movesets:

```javascript
function editMoveset(pokemon) {
    // Show all available moves
    // Allow drag-and-drop to reorder
    // Save custom moveset
}
```

### Shiny Variants

Add shiny Pokemon support:

```javascript
function populateOverviewTab(pokemon) {
    const isShiny = pokemon.isShiny || false;

    if (isShiny) {
        spriteElement.classList.add('shiny');
        // Use alternate sprite/colors
    }
}
```

### Battle Simulator

Preview battles from detail view:

```javascript
function simulateBattle(attackerId, defenderId) {
    // Calculate type effectiveness
    // Show predicted damage
    // Display win probability
}
```

## Testing Checklist

- [ ] Modal opens and closes properly
- [ ] All 5 tabs switch correctly
- [ ] Stats radar chart draws without errors
- [ ] Evolution chain displays correctly
- [ ] Moves filter works
- [ ] Previous/Next navigation cycles through all Pokemon
- [ ] Favorite button toggles and saves to localStorage
- [ ] Add to Team shows confirmation
- [ ] Share button copies URL to clipboard
- [ ] Keyboard shortcuts work (Escape, arrows)
- [ ] Responsive design works on mobile
- [ ] No console errors
- [ ] URL parameter loading works
- [ ] Background click closes modal

## Support & Questions

For issues or questions about this system:

1. Check the demo file: `wowMon_detail_view.html`
2. Review this integration guide
3. Inspect browser console for errors
4. Test with mock data first before integrating

## Version History

**v1.0** (2025-10-12)
- Initial release
- 5 tabbed views
- Canvas radar chart
- Evolution chain visualization
- Complete move system
- Navigation and actions
- Responsive design
- Accessibility features

---

**Created by Agent 4 - Detail View Specialist**
**For WoWmon - Pocket Creatures of Azeroth**
