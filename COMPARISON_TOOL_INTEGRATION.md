# WowMon Comparison Tool - Integration Guide

## Overview

The WowMon Comparison Tool is a comprehensive side-by-side creature comparison system that allows players to analyze multiple creatures simultaneously with visual statistics, type effectiveness, and battle predictions.

## Features

### 1. Comparison Interface
- **Compare 2-4 creatures** at once
- **Side-by-side card layout** with individual creature details
- **Add/remove creatures** dynamically to the comparison
- **Clear all** button to reset comparisons
- **Persistent panel** that slides in from the right side

### 2. Visual Comparisons
- **Side-by-side stat bars** with overlays highlighting the best stats
- **Comparative radar chart** showing all creatures on a single chart
- **Color-coded visualizations** for easy identification
- **Height/weight comparison** (extensible for future data)

### 3. Feature Comparisons
- **Base stat totals (BST)** with ranking
- **Evolution stage** comparison
- **Move pool overlap** analysis showing shared moves
- **Unique moves** for each creature
- **Level-normalized stats** (all creatures compared at level 50)

### 4. Battle Simulation
- **"Who would win"** calculations based on stats, types, and speed
- **Type advantage** analysis between all creatures
- **Key difference** highlighting (speed, attack, defense advantages)
- **Battle score** calculations considering damage output and survivability

### 5. UI/UX Features
- **Quick add** from creature details
- **Persistent comparison** panel with slide animation
- **Shareable comparison URL** that encodes compared creatures
- **Keyboard navigation** support
- **Screen reader** announcements
- **Responsive design** for mobile and desktop

## Installation

### Step 1: Add the JavaScript

Add this script tag before the closing `</body>` tag in wowMon.html:

```html
<script src="wowmon-comparison-tool.js"></script>
```

### Step 2: Initialize the Tool

Add this code in your GameEngine initialization (after the game engine is created):

```javascript
// In the GameEngine constructor or init method
this.comparisonTool = null;

// After cartridge is loaded and game is ready
initComparisonTool() {
    if (!this.comparisonTool) {
        this.comparisonTool = new WowMonComparisonTool(this);
        window.comparisonTool = this.comparisonTool; // Make globally accessible
    }
}

// Call this after autoLoadWoWmon() completes
this.initComparisonTool();
```

### Step 3: Add Compare Buttons to UI

Add "Add to Compare" buttons in your creature detail views:

```javascript
// In your creature detail/info rendering code
function renderCreatureInfo(creature) {
    // ... existing code ...

    html += `
        <button class="comparison-add-btn"
                onclick="comparisonTool.addToComparison('${creature.id}')"
                aria-label="Add ${creature.name} to comparison">
            Add to Compare
        </button>
    `;

    // ... rest of the code ...
}
```

### Step 4: Add Menu Integration

Add a comparison menu option to your main menu:

```javascript
// In your menu rendering code
const menuOptions = [
    { text: 'CREATURES', action: () => this.showCreatures() },
    { text: 'BAG', action: () => this.showBag() },
    { text: 'COMPARE', action: () => this.openComparison() }, // NEW
    // ... other options ...
];

// Add method to open comparison
openComparison() {
    if (window.comparisonTool) {
        window.comparisonTool.togglePanel();
    }
}
```

## Usage Examples

### Basic Usage

```javascript
// Add a creature to comparison
comparisonTool.addToComparison('murloc');
comparisonTool.addToComparison('wisp');
comparisonTool.addToComparison('imp');

// Remove a creature
comparisonTool.removeFromComparison('murloc');

// Clear all comparisons
comparisonTool.clearAll();

// Toggle panel visibility
comparisonTool.togglePanel();
```

### Compare Stats Between Two Creatures

```javascript
const creature1 = comparisonTool.createComparisonCreature(
    gameEngine.cartridge.creatures['murloc'],
    50
);
const creature2 = comparisonTool.createComparisonCreature(
    gameEngine.cartridge.creatures['wisp'],
    50
);

const comparison = comparisonTool.compareStats(creature1, creature2);
console.log(comparison);
// Output:
// {
//   hp: { c1: 95, c2: 85, winner: "MURLOC", difference: 10 },
//   attack: { c1: 98, c2: 80, winner: "MURLOC", difference: 18 },
//   ...
// }
```

### Battle Simulation

```javascript
const creature1 = comparisonTool.createComparisonCreature(
    gameEngine.cartridge.creatures['murloc'],
    50
);
const creature2 = comparisonTool.createComparisonCreature(
    gameEngine.cartridge.creatures['imp'],
    50
);

const battleResult = comparisonTool.simulateBattle(creature1, creature2);
console.log(battleResult.winnerName); // "MURLOC"
console.log(battleResult.reason); // "Higher overall battle score"
console.log(battleResult.typeAdvantage); // "MURLOC has type advantage"
```

### Draw Comparative Radar Chart

```javascript
const creatures = [
    comparisonTool.createComparisonCreature(gameEngine.cartridge.creatures['murloc'], 50),
    comparisonTool.createComparisonCreature(gameEngine.cartridge.creatures['wisp'], 50),
    comparisonTool.createComparisonCreature(gameEngine.cartridge.creatures['imp'], 50)
];

comparisonTool.drawComparativeRadarChart(creatures);
```

### Share Comparison

```javascript
// Get shareable URL
const url = comparisonTool.getComparisonURL();
console.log(url); // http://example.com/wowMon.html?compare=murloc,wisp,imp

// Share via clipboard
comparisonTool.shareComparison();
```

### Load Comparison from URL

When someone visits a URL like:
```
http://example.com/wowMon.html?compare=murloc,wisp,imp
```

The comparison tool automatically:
1. Parses the URL parameters
2. Adds the creatures to comparison
3. Opens the comparison panel

## API Reference

### Class: WowMonComparisonTool

#### Constructor
```javascript
new WowMonComparisonTool(gameEngine)
```
- `gameEngine`: Reference to the main GameEngine instance

#### Methods

##### addToComparison(creatureIdOrInstance)
Adds a creature to the comparison list.
- **Parameters:**
  - `creatureIdOrInstance` (string | object): Creature ID or instance
- **Returns:** boolean - Success status

##### removeFromComparison(creatureId)
Removes a creature from comparison.
- **Parameters:**
  - `creatureId` (string): Creature ID to remove

##### clearAll()
Clears all creatures from comparison.

##### togglePanel()
Toggles the comparison panel visibility.

##### renderComparisonView()
Renders the complete comparison view with all visualizations.

##### compareStats(creature1, creature2)
Compares stats between two creatures.
- **Parameters:**
  - `creature1` (object): First creature instance
  - `creature2` (object): Second creature instance
- **Returns:** object - Detailed comparison results

##### drawComparativeRadarChart(creatures)
Draws a radar chart comparing multiple creatures.
- **Parameters:**
  - `creatures` (array): Array of creature instances

##### simulateBattle(creature1, creature2)
Simulates a battle between two creatures.
- **Parameters:**
  - `creature1` (object): First creature
  - `creature2` (object): Second creature
- **Returns:** object - Battle prediction results

##### shareComparison()
Generates and shares a URL with current comparison.

##### exportAsImage()
Exports the comparison as an image (placeholder).

##### createComparisonCreature(baseCreature, level)
Creates a normalized creature instance for comparison.
- **Parameters:**
  - `baseCreature` (object): Base creature data
  - `level` (number): Level to normalize to (default: 50)
- **Returns:** object - Normalized creature instance

## Styling

The comparison tool uses CSS variables that match the WowMon Game Boy aesthetic:

```css
--gb-darkest: #0f380f
--gb-dark: #306230
--gb-light: #8bac0f
--gb-lightest: #9bbc0f
```

### Custom Styling

To customize the appearance, override these classes:

```css
.comparison-panel {
    /* Custom panel styles */
}

.creature-card {
    /* Custom creature card styles */
}

.radar-chart-container {
    /* Custom chart container styles */
}
```

## Type Effectiveness Chart

The tool uses this simplified type effectiveness chart:

| Attacker → Defender | Water | Fire | Nature | Earth | Electric | Ice | Beast | Shadow | Magic | Demon | Spirit |
|---------------------|-------|------|--------|-------|----------|-----|-------|--------|-------|-------|--------|
| Water               | 0.5x  | 2x   | 0.5x   | 2x    | -        | -   | -     | -      | -     | -     | -      |
| Fire                | 0.5x  | 0.5x | 2x     | 0.5x  | -        | 2x  | -     | -      | -     | -     | -      |
| Nature              | 2x    | 0.5x | -      | 2x    | -        | -   | 0.5x  | -      | -     | -     | -      |
| Earth               | 0.5x  | 2x   | 0.5x   | -     | 2x       | -   | -     | -      | -     | -     | -      |
| Electric            | 2x    | -    | -      | 0x    | -        | -   | -     | 0.5x   | -     | -     | -      |
| Ice                 | 0.5x  | 0.5x | 2x     | -     | -        | -   | 2x    | -      | -     | -     | -      |
| Beast               | -     | -    | 0.5x   | -     | -        | -   | -     | -      | 0.5x  | 0.5x  | -      |
| Shadow              | -     | -    | -      | -     | -        | -   | -     | -      | 2x    | -     | 2x     |
| Magic               | -     | -    | -      | -     | -        | -   | 2x    | 0.5x   | 0.5x  | 2x    | -      |
| Demon               | -     | -    | 2x     | -     | -        | -   | -     | -      | 0.5x  | -     | 2x     |

- **2x** = Super effective
- **0.5x** = Not very effective
- **0x** = No effect
- **-** = Neutral (1x)

## Accessibility

The comparison tool includes:

- **ARIA labels** on all interactive elements
- **Keyboard navigation** support
- **Screen reader announcements** for state changes
- **Focus indicators** for keyboard users
- **High contrast mode** compatibility
- **Reduced motion** support

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Mobile 90+)

## Performance Considerations

- Comparisons are limited to **4 creatures maximum** to maintain performance
- Radar charts use HTML5 Canvas for efficient rendering
- Stats are calculated on-demand, not stored
- URL updates use `replaceState` to avoid polluting browser history

## Future Enhancements

Potential features for future versions:

1. **Export as Image** - Full implementation using html2canvas
2. **Save Comparison Sets** - Save favorite comparisons to localStorage
3. **Advanced Filters** - Filter creatures by type, evolution stage, BST range
4. **Team Builder Mode** - Build and compare full teams of 6 creatures
5. **Move Coverage Analysis** - Analyze type coverage across move pools
6. **Damage Calculator** - Detailed damage calculations for specific moves
7. **Speed Tiers** - Show speed tier breakpoints
8. **EV/IV Simulation** - Include effort values and individual values (if added to game)

## Troubleshooting

### Comparison panel won't open
- Ensure `comparisonTool` is initialized after cartridge loads
- Check browser console for errors
- Verify `window.comparisonTool` exists

### Creatures not appearing in comparison
- Verify creature IDs are correct
- Check that cartridge data is loaded
- Ensure creatures exist in `gameEngine.cartridge.creatures`

### Radar chart not rendering
- Verify canvas element exists in DOM
- Check that container has non-zero dimensions
- Ensure chart is drawn after DOM updates (use setTimeout if needed)

### URL sharing not working
- Verify browser supports `URLSearchParams`
- Check that clipboard API is available (requires HTTPS or localhost)
- Try the manual share dialog fallback

## Support

For issues or feature requests, please refer to the main WowMon repository or documentation.

## License

This comparison tool is part of the WowMon project and follows the same license.
