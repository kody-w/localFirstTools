# ACCESSIBILITY-FIRST FEATURE DESIGN FOR WOWMON
## Comprehensive Design for Team Builder, Battle System, and Additional Features

**File Analyzed:** `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html`

**Design Philosophy:** Every feature must be fully accessible without visual or auditory cues, supporting keyboard-only navigation, screen readers, and customizable interaction modes.

---

## CURRENT ACCESSIBILITY BASELINE

### Existing Accessible Features
✅ **Keyboard Navigation:**
- Arrow keys for movement and menu navigation
- Z/A button for confirm/interact
- X/B button for cancel/back
- Enter for menu
- Shift for quick menu

✅ **ARIA Implementation:**
- Semantic HTML with `role` attributes
- `aria-label` on all interactive elements
- `aria-live` regions for dynamic content
- `aria-atomic` for complete announcements

✅ **Accessibility Settings Panel:**
- High Contrast Mode
- Reduced Motion
- Large Text (120%)
- Enhanced Screen Reader Mode
- Adjustable Text Speed

✅ **Screen Reader Support:**
- Live region announcements (`#liveRegion`)
- `announce()` function for state changes
- Focus management with `tabindex`

✅ **Visual Alternatives:**
- Skip to content link
- Focus indicators (3px solid #ffcc00 outline)
- Screen reader only (`.sr-only`) content

### Areas for Enhancement
⚠️ Creature switching in battle not implemented
⚠️ Team management limited to basic party
⚠️ No team builder interface
⚠️ Battle notifications could be more descriptive
⚠️ No audio descriptions for visual effects

---

## FEATURE 1: ACCESSIBLE TEAM BUILDER SYSTEM

### Overview
A fully accessible team management system allowing players to organize, customize, and optimize their creature party with complete keyboard and screen reader support.

### 1.1 Keyboard Navigation Pattern

#### Access Team Builder
- **Trigger:** `SELECT + START` (hold both for 1 second) or new menu option
- **Announcement:** "Team Builder opened. You have X creatures. Y are in your active party."

#### Navigation Structure
```
TEAM BUILDER LAYOUT (Grid-based with keyboard flow)

[Active Party Slots: 1-6]     [Available Creatures: 7+]
┌─────────┬─────────┐         ┌─────────────────────┐
│ Slot 1  │ Slot 2  │         │ Creature 1 (Lv. 5) │
├─────────┼─────────┤         ├─────────────────────┤
│ Slot 3  │ Slot 4  │         │ Creature 2 (Lv. 7) │
├─────────┼─────────┤         ├─────────────────────┤
│ Slot 5  │ Slot 6  │         │ Creature 3 (Lv. 4) │
└─────────┴─────────┘         └─────────────────────┘

[Quick Actions: Sort | Filter | Details]
```

#### Keyboard Controls
- **Arrow Keys:** Navigate between slots/creatures
- **Tab:** Switch between Active Party and Available Creatures sections
- **Shift + Tab:** Move backwards between sections
- **Enter/Z:** Select creature or slot
- **Space:** Toggle selection for batch operations
- **X/B:** Cancel selection or exit
- **Q:** Quick sort menu
- **F:** Filter creatures by type/level/HP
- **D:** View detailed stats of selected creature
- **S:** Swap selected creatures
- **1-6:** Jump directly to party slot
- **H:** Open help overlay with keyboard shortcuts

### 1.2 ARIA Labels and Semantic HTML

```html
<!-- Team Builder Container -->
<div class="team-builder-panel"
     id="teamBuilderPanel"
     role="application"
     aria-labelledby="team-builder-title"
     aria-describedby="team-builder-desc"
     aria-hidden="true">

  <h2 id="team-builder-title">Team Builder</h2>
  <p id="team-builder-desc" class="sr-only">
    Manage your active party and organize your creatures.
    Use arrow keys to navigate, Tab to switch sections,
    and Enter to select.
  </p>

  <!-- Active Party Section -->
  <section class="active-party-section"
           role="region"
           aria-label="Active Party - 6 slots"
           aria-describedby="active-party-help">

    <div id="active-party-help" class="sr-only">
      Your active party contains up to 6 creatures.
      These creatures will battle and earn experience.
    </div>

    <!-- Party Slot -->
    <div class="party-slot"
         role="button"
         tabindex="0"
         aria-label="Party slot 1: Kobold, Level 5, HP 20 of 20, healthy"
         aria-describedby="slot-1-details"
         data-slot-index="0">

      <span class="slot-number" aria-hidden="true">1</span>

      <div class="creature-preview" aria-hidden="true">
        <!-- Visual creature sprite -->
      </div>

      <div class="creature-info">
        <span class="creature-name">Kobold</span>
        <span class="creature-level">Lv. 5</span>
        <span class="creature-hp">HP: 20/20</span>
      </div>

      <div id="slot-1-details" class="sr-only">
        Kobold, Warrior type, knows Battle Cry, Slash, Stomp, and Rage.
        Attack: 12, Defense: 8, Speed: 10. Currently healthy.
      </div>
    </div>

    <!-- Empty Slot -->
    <div class="party-slot empty"
         role="button"
         tabindex="0"
         aria-label="Party slot 2: Empty"
         data-slot-index="1">
      <span class="slot-number" aria-hidden="true">2</span>
      <span class="empty-slot-text">Empty</span>
    </div>

    <!-- Repeat for slots 3-6 -->
  </section>

  <!-- Available Creatures Section -->
  <section class="available-creatures-section"
           role="region"
           aria-label="Available Creatures"
           aria-describedby="available-help">

    <div id="available-help" class="sr-only">
      Creatures in storage. Select to add to active party or view details.
    </div>

    <!-- Creature List -->
    <div class="creature-list"
         role="list"
         aria-label="Storage creatures">

      <div class="creature-item"
           role="listitem"
           tabindex="-1"
           aria-label="Wisp, Level 3, HP 15 of 18, slightly injured"
           aria-posinset="1"
           aria-setsize="15">

        <div class="creature-status-icon" aria-hidden="true">●</div>

        <div class="creature-info">
          <span class="creature-name">Wisp</span>
          <span class="creature-details">Lv. 3 • Spirit</span>
          <span class="creature-hp-bar" aria-hidden="true">
            <!-- Visual HP bar -->
          </span>
        </div>

        <span class="creature-hp-text">15/18 HP</span>
      </div>

      <!-- More creatures... -->
    </div>
  </section>

  <!-- Quick Actions Bar -->
  <div class="team-builder-actions"
       role="toolbar"
       aria-label="Team builder actions">

    <button class="action-btn"
            aria-label="Sort creatures by level, name, HP, or type. Press Q for quick access">
      <span aria-hidden="true">Sort</span>
    </button>

    <button class="action-btn"
            aria-label="Filter creatures by type, level range, or health status. Press F for quick access">
      <span aria-hidden="true">Filter</span>
    </button>

    <button class="action-btn"
            aria-label="View detailed stats and moves of selected creature. Press D for quick access">
      <span aria-hidden="true">Details</span>
    </button>

    <button class="action-btn"
            aria-label="Save team configuration and exit. Press Enter to confirm">
      <span aria-hidden="true">Save & Exit</span>
    </button>
  </div>

  <!-- Sort Menu (hidden by default) -->
  <div class="sort-menu"
       role="menu"
       aria-label="Sort options"
       aria-hidden="true">

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Sort by level, descending">
      By Level (High to Low)
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Sort by name, alphabetically">
      By Name (A-Z)
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Sort by current HP percentage">
      By HP (Injured First)
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         aria-label="Sort by creature type">
      By Type
    </div>
  </div>

  <!-- Filter Menu -->
  <div class="filter-menu"
       role="menu"
       aria-label="Filter options"
       aria-hidden="true">

    <fieldset>
      <legend>Filter by Type</legend>

      <label>
        <input type="checkbox" id="filter-warrior" value="warrior">
        Warrior
      </label>

      <label>
        <input type="checkbox" id="filter-spirit" value="spirit">
        Spirit
      </label>

      <!-- More types... -->
    </fieldset>

    <fieldset>
      <legend>Filter by Level Range</legend>

      <label for="level-min">Min Level:</label>
      <input type="number" id="level-min" min="1" max="100" value="1" aria-label="Minimum level filter">

      <label for="level-max">Max Level:</label>
      <input type="number" id="level-max" min="1" max="100" value="100" aria-label="Maximum level filter">
    </fieldset>

    <fieldset>
      <legend>Filter by Health Status</legend>

      <label>
        <input type="radio" name="health-filter" value="all" checked>
        All Creatures
      </label>

      <label>
        <input type="radio" name="health-filter" value="healthy">
        Healthy Only
      </label>

      <label>
        <input type="radio" name="health-filter" value="injured">
        Injured Only
      </label>

      <label>
        <input type="radio" name="health-filter" value="fainted">
        Fainted Only
      </label>
    </fieldset>

    <button aria-label="Apply filters and update creature list">Apply Filters</button>
    <button aria-label="Clear all filters and show all creatures">Clear Filters</button>
  </div>

</div>
```

### 1.3 Screen Reader Announcements

#### State Change Announcements
```javascript
// Team Builder specific announcements
teamBuilder: {
  open: () => {
    const partyCount = game.player.creatures.filter(c => c.inParty).length;
    const totalCount = game.player.creatures.length;
    game.announce(
      `Team Builder opened. ${partyCount} creatures in active party,
       ${totalCount - partyCount} in storage. Use Tab to switch sections,
       arrow keys to navigate.`,
      'polite'
    );
  },

  selectSlot: (slotIndex, creature) => {
    if (creature) {
      const hpPercent = Math.round((creature.hp / creature.maxHp) * 100);
      const status = creature.hp === 0 ? 'fainted' :
                     hpPercent < 30 ? 'critically injured' :
                     hpPercent < 70 ? 'injured' : 'healthy';

      game.announce(
        `Party slot ${slotIndex + 1} selected. ${creature.name},
         Level ${creature.level}, ${creature.hp} of ${creature.maxHp} HP, ${status}.
         Press Enter to view options, D for details, or arrow keys to move.`,
        'polite'
      );
    } else {
      game.announce(
        `Empty party slot ${slotIndex + 1} selected.
         Press Enter to add a creature from storage.`,
        'polite'
      );
    }
  },

  selectCreature: (creature, index, total) => {
    const types = creature.types ? creature.types.join(' and ') : 'Normal';
    const hpPercent = Math.round((creature.hp / creature.maxHp) * 100);

    game.announce(
      `Storage creature ${index + 1} of ${total}: ${creature.name},
       ${types} type, Level ${creature.level},
       ${hpPercent} percent HP. Press Enter to add to party.`,
      'polite'
    );
  },

  swap: (creature1, creature2) => {
    game.announce(
      `Swapped ${creature1.name} with ${creature2.name}.
       Press Enter to confirm or X to undo.`,
      'assertive'
    );
  },

  sortApplied: (sortType) => {
    const descriptions = {
      level: 'highest level first',
      name: 'alphabetically',
      hp: 'most injured first',
      type: 'by creature type'
    };
    game.announce(
      `Creatures sorted ${descriptions[sortType]}.
       List updated with ${game.player.creatures.length} creatures.`,
      'polite'
    );
  },

  filterApplied: (activeFilters) => {
    const filterCount = Object.keys(activeFilters).length;
    game.announce(
      `${filterCount} filters applied.
       Showing ${game.filteredCreatures.length} of ${game.player.creatures.length} creatures.`,
      'polite'
    );
  },

  partyUpdated: (action, creature) => {
    game.announce(
      `${creature.name} ${action} active party.
       Party now has ${game.player.creatures.filter(c => c.inParty).length} creatures.`,
      'assertive'
    );
  }
}
```

### 1.4 Visual Alternatives and Options

#### Text-Based Status Indicators
```css
/* Health status badges */
.health-status::before {
  content: attr(data-status);
  font-weight: bold;
  margin-right: 4px;
}

.health-status[data-status="Healthy"]::before { color: #0f0; }
.health-status[data-status="Injured"]::before { color: #ff0; }
.health-status[data-status="Critical"]::before { color: #f00; }
.health-status[data-status="Fainted"]::before { color: #888; }

/* Pattern-based backgrounds for colorblind support */
.type-warrior { background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0,0,0,0.1) 10px, rgba(0,0,0,0.1) 20px); }
.type-spirit { background-image: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px); }
.type-fire { background-image: url('data:image/svg+xml,...'); /* flame pattern */ }

/* Visual HP indicators with multiple cues */
.hp-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hp-bar {
  position: relative;
  background: #333;
  border: 2px solid #fff;
}

.hp-fill {
  position: relative;
}

/* Stripe pattern for low HP (not just color) */
.hp-fill.low {
  background-image: repeating-linear-gradient(
    -45deg,
    #f00,
    #f00 4px,
    #a00 4px,
    #a00 8px
  );
  animation: pulse 1s infinite;
}

.hp-text {
  font-weight: bold;
  font-family: monospace;
}
```

#### Audio Feedback (Optional)
```javascript
// Non-intrusive sound cues for visual state changes
audioFeedback: {
  slotFocus: () => game.audio.playSFX('menu_move', 0.3),
  slotSelect: () => game.audio.playSFX('menu_select'),
  creatureSwap: () => game.audio.playSFX('item', 0.5),
  filterApplied: () => game.audio.playSFX('menu_open', 0.4),
  partyFull: () => game.audio.playSFX('error', 0.6),

  // Optional: Creature type sounds (can be disabled in settings)
  creatureTypeSound: (type) => {
    if (game.accessibilitySettings.creatureTypeSounds) {
      game.audio.playSFX(`type_${type}`, 0.2);
    }
  }
}
```

### 1.5 Team Builder JavaScript Implementation

```javascript
class TeamBuilder {
  constructor(game) {
    this.game = game;
    this.activeSection = 'party'; // 'party' or 'storage'
    this.selectedIndex = 0;
    this.selectedCreatures = new Set();
    this.sortMode = 'level';
    this.filters = {
      types: [],
      levelMin: 1,
      levelMax: 100,
      healthStatus: 'all'
    };
  }

  open() {
    const panel = document.getElementById('teamBuilderPanel');
    panel.classList.add('active');
    panel.setAttribute('aria-hidden', 'false');

    this.render();
    this.focusFirstSlot();
    this.game.announce(this.getOpeningAnnouncement(), 'polite');
  }

  close() {
    const panel = document.getElementById('teamBuilderPanel');
    panel.classList.remove('active');
    panel.setAttribute('aria-hidden', 'true');

    this.game.announce('Team Builder closed. Returning to game.', 'polite');
  }

  handleInput(key) {
    switch(key) {
      case 'Tab':
        this.switchSection();
        break;
      case 'ArrowUp':
      case 'ArrowDown':
      case 'ArrowLeft':
      case 'ArrowRight':
        this.navigate(key);
        break;
      case 'Enter':
      case 'z':
        this.selectCurrent();
        break;
      case 'x':
        this.cancel();
        break;
      case 'Space':
        this.toggleSelection();
        break;
      case '1': case '2': case '3': case '4': case '5': case '6':
        this.jumpToSlot(parseInt(key) - 1);
        break;
      case 'q':
        this.openSortMenu();
        break;
      case 'f':
        this.openFilterMenu();
        break;
      case 'd':
        this.showDetails();
        break;
      case 's':
        this.swapSelected();
        break;
      case 'h':
        this.showHelp();
        break;
    }
  }

  navigate(direction) {
    const items = this.getCurrentItems();
    const columns = this.activeSection === 'party' ? 2 : 1;

    switch(direction) {
      case 'ArrowUp':
        this.selectedIndex = Math.max(0, this.selectedIndex - columns);
        break;
      case 'ArrowDown':
        this.selectedIndex = Math.min(items.length - 1, this.selectedIndex + columns);
        break;
      case 'ArrowLeft':
        if (this.selectedIndex % columns !== 0) {
          this.selectedIndex--;
        }
        break;
      case 'ArrowRight':
        if (this.selectedIndex % columns !== columns - 1 && this.selectedIndex < items.length - 1) {
          this.selectedIndex++;
        }
        break;
    }

    this.updateFocus();
    this.announceCurrentSelection();
  }

  switchSection() {
    this.activeSection = this.activeSection === 'party' ? 'storage' : 'party';
    this.selectedIndex = 0;
    this.updateFocus();

    const announcement = this.activeSection === 'party'
      ? 'Switched to Active Party section. Use arrow keys to navigate party slots.'
      : 'Switched to Storage section. Use arrow keys to navigate stored creatures.';

    this.game.announce(announcement, 'polite');
  }

  getCurrentItems() {
    if (this.activeSection === 'party') {
      return Array(6).fill(null).map((_, i) =>
        this.game.player.creatures.find(c => c.partySlot === i) || null
      );
    } else {
      return this.getFilteredCreatures();
    }
  }

  getFilteredCreatures() {
    let creatures = this.game.player.creatures.filter(c => !c.partySlot && c.partySlot !== 0);

    // Apply filters
    if (this.filters.types.length > 0) {
      creatures = creatures.filter(c =>
        c.types && c.types.some(t => this.filters.types.includes(t))
      );
    }

    creatures = creatures.filter(c =>
      c.level >= this.filters.levelMin && c.level <= this.filters.levelMax
    );

    switch(this.filters.healthStatus) {
      case 'healthy':
        creatures = creatures.filter(c => c.hp === c.maxHp);
        break;
      case 'injured':
        creatures = creatures.filter(c => c.hp > 0 && c.hp < c.maxHp);
        break;
      case 'fainted':
        creatures = creatures.filter(c => c.hp === 0);
        break;
    }

    // Apply sort
    this.sortCreatures(creatures);

    return creatures;
  }

  sortCreatures(creatures) {
    switch(this.sortMode) {
      case 'level':
        creatures.sort((a, b) => b.level - a.level);
        break;
      case 'name':
        creatures.sort((a, b) => a.name.localeCompare(b.name));
        break;
      case 'hp':
        creatures.sort((a, b) => (a.hp / a.maxHp) - (b.hp / b.maxHp));
        break;
      case 'type':
        creatures.sort((a, b) => {
          const typeA = a.types ? a.types[0] : 'normal';
          const typeB = b.types ? b.types[0] : 'normal';
          return typeA.localeCompare(typeB);
        });
        break;
    }
  }

  updateFocus() {
    const items = document.querySelectorAll(
      this.activeSection === 'party' ? '.party-slot' : '.creature-item'
    );

    items.forEach((item, index) => {
      item.setAttribute('tabindex', index === this.selectedIndex ? '0' : '-1');
      item.classList.toggle('focused', index === this.selectedIndex);
    });

    if (items[this.selectedIndex]) {
      items[this.selectedIndex].focus();
    }
  }

  announceCurrentSelection() {
    const items = this.getCurrentItems();
    const current = items[this.selectedIndex];

    if (this.activeSection === 'party') {
      this.announcePartySlot(this.selectedIndex, current);
    } else {
      this.announceStorageCreature(current, this.selectedIndex, items.length);
    }
  }

  announcePartySlot(slotIndex, creature) {
    if (creature) {
      const hpPercent = Math.round((creature.hp / creature.maxHp) * 100);
      const status = this.getHealthStatus(creature);
      const types = creature.types ? creature.types.join(' and ') : 'Normal';

      this.game.announce(
        `Party slot ${slotIndex + 1}: ${creature.name}, ${types} type,
         Level ${creature.level}, ${creature.hp} of ${creature.maxHp} HP, ${status}.
         Knows ${creature.moves.length} moves. Press Enter for options.`,
        'polite'
      );
    } else {
      this.game.announce(
        `Party slot ${slotIndex + 1}: Empty. Press Enter to add a creature.`,
        'polite'
      );
    }
  }

  announceStorageCreature(creature, index, total) {
    if (!creature) return;

    const types = creature.types ? creature.types.join(' and ') : 'Normal';
    const status = this.getHealthStatus(creature);

    this.game.announce(
      `Creature ${index + 1} of ${total}: ${creature.name}, ${types} type,
       Level ${creature.level}, ${status}. Press Enter to add to party.`,
      'polite'
    );
  }

  getHealthStatus(creature) {
    const hpPercent = (creature.hp / creature.maxHp) * 100;
    if (creature.hp === 0) return 'fainted';
    if (hpPercent < 25) return 'critically injured';
    if (hpPercent < 50) return 'heavily injured';
    if (hpPercent < 75) return 'moderately injured';
    if (hpPercent < 100) return 'slightly injured';
    return 'healthy';
  }

  showDetails() {
    const items = this.getCurrentItems();
    const creature = items[this.selectedIndex];

    if (!creature) {
      this.game.announce('No creature selected.', 'assertive');
      return;
    }

    // Open detailed stats view
    this.openDetailsPanel(creature);
  }

  openDetailsPanel(creature) {
    const types = creature.types ? creature.types.join(', ') : 'Normal';
    const moves = creature.moves.map((moveId, i) => {
      const move = this.game.cartridge.moves[moveId];
      return move ? `${i + 1}. ${move.name}, ${move.type} type,
                     ${move.power} power, ${creature.pp[moveId]} PP remaining` : '';
    }).join('. ');

    const details = `
      Detailed stats for ${creature.name}:
      Level ${creature.level}, ${types} type.
      HP: ${creature.hp} of ${creature.maxHp}.
      Attack: ${creature.attack}.
      Defense: ${creature.defense}.
      Speed: ${creature.speed}.
      Experience: ${creature.exp}.
      Moves: ${moves}.
      Press X to close details.
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(details, 'assertive');

    // Show visual details panel
    this.showVisualDetailsPanel(creature);
  }
}
```

---

## FEATURE 2: ACCESSIBLE BATTLE SYSTEM ENHANCEMENTS

### Overview
Enhanced battle system with in-battle creature switching, comprehensive status announcements, and strategic options accessible to all players.

### 2.1 Enhanced Battle Menu Structure

```
BATTLE MENU (Vertical Navigation)
┌─────────────────────┐
│ ► FIGHT             │  ← Arrow keys up/down
│   SWITCH            │
│   BAG               │
│   RUN               │
└─────────────────────┘

When SWITCH selected:
┌─────────────────────┐
│ Your Party:         │
│ ► 1. Kobold (20/20) │  ← Number keys 1-6 or arrows
│   2. Wisp (15/18)   │
│   3. Drake (0/25)   │  ← Fainted creatures grayed
│   4. [Empty]        │  ← Empty slots skipped
└─────────────────────┘

When FIGHT selected:
┌───────────┬───────────┐
│ ► Move 1  │   Move 3  │  ← Arrow keys / WASD
│   10/10PP │   5/5PP   │
├───────────┼───────────┤
│   Move 2  │   Move 4  │
│   8/15PP  │   0/10PP  │  ← No PP = disabled
└───────────┴───────────┘
```

### 2.2 Battle ARIA Implementation

```html
<!-- Enhanced Battle UI -->
<div class="battle-container"
     role="application"
     aria-label="Battle mode"
     aria-describedby="battle-status">

  <!-- Battle Status Summary (always announced) -->
  <div id="battle-status" class="sr-only" aria-live="polite" aria-atomic="true">
    Turn 1. Your Kobold: 20 of 20 HP, healthy.
    Enemy Gnoll: 18 of 18 HP, healthy.
    Battle menu ready. Select an action.
  </div>

  <!-- Visual Battle Area -->
  <div class="battle-area" aria-hidden="true">
    <!-- Canvas rendering - purely visual -->
  </div>

  <!-- Enemy Info (accessible) -->
  <section class="battle-combatant enemy"
           role="region"
           aria-label="Enemy creature status">

    <div class="combatant-info">
      <h3 id="enemy-name">Gnoll</h3>
      <p id="enemy-level">Level 5</p>

      <div class="hp-display" role="status" aria-live="polite">
        <span class="hp-label sr-only">Enemy HP:</span>
        <div class="hp-bar" aria-hidden="true">
          <div class="hp-fill" id="enemy-hp-visual" style="width: 100%"></div>
        </div>
        <span class="hp-text" id="enemy-hp-text">18/18</span>
        <span class="hp-percent sr-only">100 percent</span>
      </div>

      <p id="enemy-status" class="status-condition" aria-live="polite">
        Normal condition
      </p>
    </div>
  </section>

  <!-- Player Info (accessible) -->
  <section class="battle-combatant player"
           role="region"
           aria-label="Your creature status">

    <div class="combatant-info">
      <h3 id="player-name">Kobold</h3>
      <p id="player-level">Level 5</p>

      <div class="hp-display" role="status" aria-live="polite">
        <span class="hp-label sr-only">Your HP:</span>
        <div class="hp-bar" aria-hidden="true">
          <div class="hp-fill" id="player-hp-visual" style="width: 100%"></div>
        </div>
        <span class="hp-text" id="player-hp-text">20/20</span>
        <span class="hp-percent sr-only">100 percent</span>
      </div>

      <p id="player-status" class="status-condition" aria-live="polite">
        Normal condition
      </p>
    </div>
  </section>

  <!-- Enhanced Battle Menu -->
  <nav class="battle-menu"
       role="menu"
       aria-label="Battle actions"
       aria-activedescendant="battle-option-0">

    <div class="menu-option selected"
         role="menuitem"
         tabindex="0"
         id="battle-option-0"
         aria-label="Fight: Choose a move to attack">
      <span class="option-icon" aria-hidden="true">⚔️</span>
      <span class="option-text">FIGHT</span>
      <span class="option-hint sr-only">
        Choose from 4 moves. Press Enter to select.
      </span>
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         id="battle-option-1"
         aria-label="Switch: Change to a different creature. You have 2 healthy creatures available.">
      <span class="option-icon" aria-hidden="true">🔄</span>
      <span class="option-text">SWITCH</span>
      <span class="option-hint sr-only">
        Your party: Kobold is active, Wisp is healthy, Drake has fainted.
      </span>
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         id="battle-option-2"
         aria-label="Bag: Use an item. You have 3 potions and 5 berries.">
      <span class="option-icon" aria-hidden="true">🎒</span>
      <span class="option-text">BAG</span>
      <span class="option-hint sr-only">
        Use healing items or capture tools.
      </span>
    </div>

    <div class="menu-option"
         role="menuitem"
         tabindex="-1"
         id="battle-option-3"
         aria-label="Run: Attempt to flee from battle. Not available against trainers.">
      <span class="option-icon" aria-hidden="true">🏃</span>
      <span class="option-text">RUN</span>
      <span class="option-hint sr-only">
        This is a wild battle. You can run away safely.
      </span>
    </div>
  </nav>

  <!-- Switch Menu (when SWITCH selected) -->
  <nav class="switch-menu"
       role="menu"
       aria-label="Choose creature to switch in"
       aria-hidden="true">

    <div class="menu-header">
      <h3>Your Party</h3>
      <p class="sr-only">Select a creature to switch in. Arrow keys to navigate, Enter to confirm.</p>
    </div>

    <div class="party-list" role="list">

      <!-- Active Creature (cannot switch to self) -->
      <div class="party-member active disabled"
           role="listitem"
           tabindex="-1"
           aria-label="Kobold, Level 5, 20 of 20 HP, currently active"
           aria-disabled="true">

        <span class="slot-number" aria-hidden="true">1</span>
        <div class="member-info">
          <span class="member-name">Kobold</span>
          <span class="member-level">Lv. 5</span>
          <span class="member-hp">20/20</span>
          <span class="member-status">[Active]</span>
        </div>
      </div>

      <!-- Healthy Creature (can switch) -->
      <div class="party-member healthy"
           role="listitem"
           tabindex="0"
           id="switch-option-1"
           aria-label="Wisp, Level 3, Spirit type, 15 of 18 HP, slightly injured but can battle">

        <span class="slot-number" aria-hidden="true">2</span>
        <div class="member-info">
          <span class="member-name">Wisp</span>
          <span class="member-level">Lv. 3</span>
          <span class="member-hp">15/18</span>
          <span class="member-types sr-only">Spirit type</span>
        </div>
      </div>

      <!-- Fainted Creature (cannot switch) -->
      <div class="party-member fainted disabled"
           role="listitem"
           tabindex="-1"
           aria-label="Drake, Level 7, 0 HP, fainted, cannot battle"
           aria-disabled="true">

        <span class="slot-number" aria-hidden="true">3</span>
        <div class="member-info">
          <span class="member-name">Drake</span>
          <span class="member-level">Lv. 7</span>
          <span class="member-hp">0/25</span>
          <span class="member-status">[Fainted]</span>
        </div>
      </div>

      <!-- Empty Slot -->
      <div class="party-member empty disabled"
           role="listitem"
           tabindex="-1"
           aria-label="Empty party slot"
           aria-disabled="true">

        <span class="slot-number" aria-hidden="true">4</span>
        <div class="member-info">
          <span class="member-name">Empty</span>
        </div>
      </div>

      <!-- Slots 5-6... -->
    </div>

    <div class="menu-footer">
      <button class="cancel-btn" aria-label="Cancel and return to battle menu">
        Back (Press X)
      </button>
    </div>
  </nav>

  <!-- Battle Log (Screen Reader Priority) -->
  <div class="battle-log"
       role="log"
       aria-live="assertive"
       aria-atomic="false"
       aria-relevant="additions">
    <!-- Recent battle actions announced here -->
  </div>

</div>
```

### 2.3 Battle Screen Reader Announcements

```javascript
// Enhanced battle announcements
battleAnnouncements: {

  // Turn start
  turnStart: (turnNumber, playerCreature, enemyCreature) => {
    const playerHP = Math.round((playerCreature.hp / playerCreature.maxHp) * 100);
    const enemyHP = Math.round((enemyCreature.hp / enemyCreature.maxHp) * 100);

    return `Turn ${turnNumber}. Your ${playerCreature.name}: ${playerCreature.hp} of ${playerCreature.maxHp} HP, ${playerHP} percent.
            Enemy ${enemyCreature.name}: ${enemyHP} percent HP. What will you do?`;
  },

  // Move selection
  moveHover: (move, creature) => {
    const ppRemaining = creature.pp[move.id];
    const ppMax = move.pp;
    const typeEffectiveness = game.getTypeMatchup(move.type, enemyCreature.types);

    let effectiveness = '';
    if (typeEffectiveness > 1.5) effectiveness = 'Super effective against enemy!';
    else if (typeEffectiveness < 0.75) effectiveness = 'Not very effective against enemy.';
    else if (typeEffectiveness === 0) effectiveness = 'No effect on enemy.';

    return `${move.name}, ${move.type} type, ${move.power} power,
            ${ppRemaining} of ${ppMax} PP remaining. ${effectiveness}
            ${move.accuracy < 100 ? `${move.accuracy} percent accuracy.` : ''}`;
  },

  // Attack execution
  attackUsed: (attacker, move, isPlayer) => {
    return `${attacker.name} used ${move.name}!`;
  },

  // Damage dealt
  damageDealt: (damage, defender, effectiveness) => {
    const hpRemaining = defender.hp;
    const hpPercent = Math.round((hpRemaining / defender.maxHp) * 100);

    let effectivenessMsg = '';
    if (effectiveness > 1.5) effectivenessMsg = 'Super effective! ';
    else if (effectiveness < 0.75) effectivenessMsg = 'Not very effective. ';
    else if (effectiveness === 0) effectivenessMsg = 'It had no effect!';

    let statusMsg = '';
    if (hpPercent <= 0) statusMsg = `${defender.name} fainted!`;
    else if (hpPercent < 20) statusMsg = `${defender.name} is in critical condition!`;
    else if (hpPercent < 50) statusMsg = `${defender.name} is badly hurt.`;

    return `${effectivenessMsg}${defender.name} took ${damage} damage.
            ${hpRemaining} HP remaining, ${hpPercent} percent. ${statusMsg}`;
  },

  // Miss
  attackMissed: (attacker) => {
    return `${attacker.name}'s attack missed!`;
  },

  // Critical hit
  criticalHit: () => {
    return `Critical hit!`;
  },

  // Switch menu opened
  switchMenuOpened: (availableCount, faintedCount) => {
    return `Switch menu opened. ${availableCount} creatures available,
            ${faintedCount} have fainted. Use arrow keys to select, Enter to switch in.`;
  },

  // Creature switched
  creatureSwitched: (newCreature, isPlayer) => {
    const types = newCreature.types ? newCreature.types.join(' and ') : 'Normal';
    const hpPercent = Math.round((newCreature.hp / newCreature.maxHp) * 100);

    return `${isPlayer ? 'You sent out' : 'Enemy sent out'} ${newCreature.name}!
            ${types} type, Level ${newCreature.level}, ${newCreature.hp} HP, ${hpPercent} percent.
            Knows ${newCreature.moves.length} moves.`;
  },

  // Battle end - Victory
  victory: (exp, money) => {
    return `You won the battle! Gained ${exp} experience and ${money} gold.
            Press Enter to continue.`;
  },

  // Battle end - Defeat
  defeat: () => {
    return `You lost the battle! All your creatures have fainted.
            You'll be returned to the last healing point.`;
  },

  // Status conditions
  statusInflicted: (creature, status) => {
    const statusDescriptions = {
      burn: 'burned and will take damage each turn',
      poison: 'poisoned and will lose HP over time',
      paralyze: 'paralyzed and may be unable to move',
      freeze: 'frozen solid and cannot move',
      sleep: 'fell asleep and cannot act for a few turns',
      confuse: 'confused and may hurt itself'
    };

    return `${creature.name} was ${statusDescriptions[status] || status}!`;
  },

  // Stat changes
  statChanged: (creature, stat, stages) => {
    const direction = stages > 0 ? 'rose' : 'fell';
    const amount = Math.abs(stages) === 1 ? '' :
                   Math.abs(stages) === 2 ? 'sharply ' :
                   'drastically ';

    return `${creature.name}'s ${stat} ${amount}${direction}!`;
  },

  // Type matchup tutorial (optional, first time seeing effectiveness)
  typeMatchupTutorial: (moveType, defenderType, effectiveness) => {
    if (!game.tutorialShown.typeMatchup) {
      game.tutorialShown.typeMatchup = true;

      if (effectiveness > 1.5) {
        return `Type advantage! ${moveType} moves are super effective against ${defenderType} types.
                They deal extra damage.`;
      } else if (effectiveness < 0.75) {
        return `Type disadvantage. ${moveType} moves are not very effective against ${defenderType} types.
                Consider switching moves or creatures.`;
      }
    }
    return '';
  }
}
```

### 2.4 Battle JavaScript Implementation

```javascript
class AccessibleBattleSystem {
  constructor(game) {
    this.game = game;
    this.currentMenu = 'main'; // 'main', 'fight', 'switch', 'bag'
    this.selectedIndex = 0;
    this.turnNumber = 1;
    this.battleLog = [];
    this.lastAnnouncement = '';
  }

  startBattle(type, enemyId) {
    // Existing battle start code...

    // Enhanced announcement
    this.announceBattleStart();

    // Set up keyboard focus
    this.focusBattleMenu();
  }

  announceBattleStart() {
    const enemy = this.game.battle.enemyCreature;
    const player = this.game.battle.playerCreature;
    const types = enemy.types ? enemy.types.join(' and ') : 'Normal';

    const announcement = `
      Battle started! Wild ${enemy.name} appeared!
      ${types} type, Level ${enemy.level}.
      You sent out ${player.name}, Level ${player.level}.
      Battle menu ready. Use arrow keys to select action, Enter to confirm.
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(announcement, 'assertive');
    this.addToBattleLog(announcement);
  }

  handleBattleInput(key) {
    if (!this.game.battle || !this.game.battle.waitingForInput) return;

    switch(this.currentMenu) {
      case 'main':
        this.handleMainMenuInput(key);
        break;
      case 'fight':
        this.handleFightMenuInput(key);
        break;
      case 'switch':
        this.handleSwitchMenuInput(key);
        break;
      case 'bag':
        this.handleBagMenuInput(key);
        break;
    }
  }

  handleMainMenuInput(key) {
    const options = ['FIGHT', 'SWITCH', 'BAG', 'RUN'];

    switch(key) {
      case 'ArrowUp':
      case 'w':
        this.selectedIndex = Math.max(0, this.selectedIndex - 1);
        this.updateBattleMenuFocus();
        this.announceBattleOption();
        break;

      case 'ArrowDown':
      case 's':
        this.selectedIndex = Math.min(options.length - 1, this.selectedIndex + 1);
        this.updateBattleMenuFocus();
        this.announceBattleOption();
        break;

      case 'Enter':
      case 'z':
        this.selectBattleOption(this.selectedIndex);
        break;

      case '1':
        this.selectedIndex = 0;
        this.selectBattleOption(0);
        break;
      case '2':
        this.selectedIndex = 1;
        this.selectBattleOption(1);
        break;
      case '3':
        this.selectedIndex = 2;
        this.selectBattleOption(2);
        break;
      case '4':
        this.selectedIndex = 3;
        this.selectBattleOption(3);
        break;
    }
  }

  announceBattleOption() {
    const player = this.game.battle.playerCreature;
    const enemy = this.game.battle.enemyCreature;

    const announcements = {
      0: `Fight: Choose a move to attack. ${player.name} knows ${player.moves.length} moves.`,
      1: () => {
        const availableCreatures = this.getAvailableCreatures();
        return `Switch: Change to a different creature. ${availableCreatures.length} creatures available.`;
      },
      2: () => {
        const items = this.game.player.bag || {};
        const itemCount = Object.values(items).reduce((sum, count) => sum + count, 0);
        return `Bag: Use an item. You have ${itemCount} items.`;
      },
      3: () => {
        if (this.game.battle.type === 'wild') {
          return `Run: Flee from battle. You can escape safely.`;
        } else {
          return `Run: Cannot run from trainer battles.`;
        }
      }
    };

    const announcement = typeof announcements[this.selectedIndex] === 'function'
      ? announcements[this.selectedIndex]()
      : announcements[this.selectedIndex];

    this.game.announce(announcement, 'polite');
  }

  selectBattleOption(index) {
    this.game.audio.playSFX('menu_select');

    switch(index) {
      case 0: // FIGHT
        this.openFightMenu();
        break;
      case 1: // SWITCH
        this.openSwitchMenu();
        break;
      case 2: // BAG
        this.openBagMenu();
        break;
      case 3: // RUN
        this.attemptRun();
        break;
    }
  }

  openSwitchMenu() {
    const availableCreatures = this.getAvailableCreatures();

    if (availableCreatures.length === 0) {
      this.game.announce(
        'No other creatures available to switch. All have fainted. Press X to go back.',
        'assertive'
      );
      return;
    }

    this.currentMenu = 'switch';
    this.selectedIndex = 0;

    // Show switch menu UI
    document.getElementById('battleMenu').classList.remove('active');
    document.getElementById('switchMenu').classList.add('active');
    document.getElementById('switchMenu').setAttribute('aria-hidden', 'false');

    // Announce
    const announcement = `
      Switch menu opened. ${availableCreatures.length} creatures available.
      Current creature: ${this.game.battle.playerCreature.name}.
      Use arrow keys to select, Enter to switch, X to cancel.
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(announcement, 'assertive');

    // Focus first available creature
    this.focusSwitchOption(0);
    this.announceSwitchOption(availableCreatures[0]);
  }

  getAvailableCreatures() {
    return this.game.player.creatures.filter(c =>
      c.hp > 0 && c !== this.game.battle.playerCreature
    );
  }

  handleSwitchMenuInput(key) {
    const availableCreatures = this.getAvailableCreatures();

    switch(key) {
      case 'ArrowUp':
      case 'w':
        this.selectedIndex = Math.max(0, this.selectedIndex - 1);
        this.focusSwitchOption(this.selectedIndex);
        this.announceSwitchOption(availableCreatures[this.selectedIndex]);
        break;

      case 'ArrowDown':
      case 's':
        this.selectedIndex = Math.min(availableCreatures.length - 1, this.selectedIndex + 1);
        this.focusSwitchOption(this.selectedIndex);
        this.announceSwitchOption(availableCreatures[this.selectedIndex]);
        break;

      case 'Enter':
      case 'z':
        this.switchToCreature(availableCreatures[this.selectedIndex]);
        break;

      case 'x':
      case 'Escape':
        this.closeSwitchMenu();
        break;

      case '1': case '2': case '3': case '4': case '5': case '6':
        const slotIndex = parseInt(key) - 1;
        if (slotIndex < availableCreatures.length) {
          this.switchToCreature(availableCreatures[slotIndex]);
        }
        break;
    }
  }

  announceSwitchOption(creature) {
    if (!creature) return;

    const types = creature.types ? creature.types.join(' and ') : 'Normal';
    const hpPercent = Math.round((creature.hp / creature.maxHp) * 100);
    const status = this.getHealthStatus(creature);

    const announcement = `
      ${creature.name}, ${types} type, Level ${creature.level},
      ${creature.hp} of ${creature.maxHp} HP, ${hpPercent} percent, ${status}.
      Knows ${creature.moves.length} moves. Press Enter to switch in.
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(announcement, 'polite');
  }

  switchToCreature(newCreature) {
    const oldCreature = this.game.battle.playerCreature;

    this.game.audio.playSFX('menu_select');

    // Announce switch
    this.game.announce(
      `Switching ${oldCreature.name} for ${newCreature.name}. Stand by.`,
      'assertive'
    );

    // Perform switch
    this.game.battle.playerCreature = newCreature;
    this.game.battle.waitingForInput = false;

    // Close switch menu
    this.closeSwitchMenu();

    // Update battle UI
    this.updateBattleUI();

    // Announce new creature is in
    setTimeout(() => {
      const types = newCreature.types ? newCreature.types.join(' and ') : 'Normal';
      this.game.announce(
        `${newCreature.name} is now in battle! ${types} type, Level ${newCreature.level},
         ${newCreature.hp} HP. Enemy ${this.game.battle.enemyCreature.name} prepares to attack.`,
        'assertive'
      );

      // Enemy turn
      this.executeEnemyTurn();
    }, 1500);
  }

  closeSwitchMenu() {
    this.currentMenu = 'main';
    this.selectedIndex = 0;

    document.getElementById('switchMenu').classList.remove('active');
    document.getElementById('switchMenu').setAttribute('aria-hidden', 'true');
    document.getElementById('battleMenu').classList.add('active');

    this.updateBattleMenuFocus();

    this.game.announce('Switch menu closed. Back to battle menu.', 'polite');
  }

  executeMove(attacker, defender, moveId, isPlayer) {
    const move = this.game.cartridge.moves[moveId];
    if (!move) return;

    // Announce move usage
    this.game.announce(`${attacker.name} used ${move.name}!`, 'assertive');
    this.addToBattleLog(`${attacker.name} used ${move.name}!`);

    // Deduct PP
    attacker.pp[moveId]--;

    setTimeout(() => {
      // Check accuracy
      const accuracyRoll = Math.random() * 100;
      if (accuracyRoll > move.accuracy) {
        this.game.announce(`${attacker.name}'s attack missed!`, 'assertive');
        this.addToBattleLog(`${attacker.name}'s attack missed!`);

        setTimeout(() => {
          this.endTurn();
        }, 1000);
        return;
      }

      // Calculate damage
      if (move.power > 0) {
        this.game.audio.playSFX('attack');

        const damage = this.calculateDamage(attacker, defender, move);
        const effectiveness = this.getEffectiveness(move, defender);

        // Apply damage
        defender.hp = Math.max(0, defender.hp - damage);

        // Update UI
        this.updateBattleUI();

        // Announce damage
        this.announceDamage(damage, defender, effectiveness);

        // Check if defender fainted
        if (defender.hp === 0) {
          setTimeout(() => {
            this.handleFainted(defender, isPlayer);
          }, 1500);
        } else {
          setTimeout(() => {
            this.endTurn();
          }, 1500);
        }
      } else {
        // Status move or other effect
        this.handleMoveEffect(move, attacker, defender);

        setTimeout(() => {
          this.endTurn();
        }, 1500);
      }
    }, 1000);
  }

  announceDamage(damage, defender, effectiveness) {
    const hpPercent = Math.round((defender.hp / defender.maxHp) * 100);

    let effectMsg = '';
    if (effectiveness > 1.5) effectMsg = 'Super effective! ';
    else if (effectiveness < 0.75) effectMsg = 'Not very effective. ';
    else if (effectiveness === 0) effectMsg = 'It had no effect! ';

    let statusMsg = '';
    if (defender.hp === 0) {
      statusMsg = `${defender.name} fainted!`;
    } else if (hpPercent < 20) {
      statusMsg = `${defender.name} is in critical condition!`;
    } else if (hpPercent < 50) {
      statusMsg = `${defender.name} is badly hurt.`;
    }

    const announcement = `
      ${effectMsg}${defender.name} took ${damage} damage.
      ${defender.hp} HP remaining, ${hpPercent} percent. ${statusMsg}
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(announcement, 'assertive');
    this.addToBattleLog(announcement);
  }

  addToBattleLog(message) {
    this.battleLog.push({
      message: message,
      timestamp: Date.now()
    });

    // Keep only last 10 messages
    if (this.battleLog.length > 10) {
      this.battleLog.shift();
    }

    // Update visual battle log
    const logElement = document.querySelector('.battle-log');
    if (logElement) {
      const entry = document.createElement('div');
      entry.className = 'log-entry';
      entry.textContent = message;
      logElement.appendChild(entry);

      // Auto-scroll
      logElement.scrollTop = logElement.scrollHeight;
    }
  }

  getHealthStatus(creature) {
    const hpPercent = (creature.hp / creature.maxHp) * 100;
    if (creature.hp === 0) return 'fainted';
    if (hpPercent < 25) return 'critically injured';
    if (hpPercent < 50) return 'heavily injured';
    if (hpPercent < 75) return 'moderately injured';
    if (hpPercent < 100) return 'slightly injured';
    return 'healthy';
  }

  // Accessibility helper: Read full battle status
  readBattleStatus() {
    const player = this.game.battle.playerCreature;
    const enemy = this.game.battle.enemyCreature;

    const playerHP = Math.round((player.hp / player.maxHp) * 100);
    const enemyHP = Math.round((enemy.hp / enemy.maxHp) * 100);

    const status = `
      Battle status, Turn ${this.turnNumber}.
      Your ${player.name}: Level ${player.level}, ${player.hp} of ${player.maxHp} HP, ${playerHP} percent.
      Enemy ${enemy.name}: Level ${enemy.level}, ${enemyHP} percent HP.
      Your turn. What will you do?
    `.trim().replace(/\s+/g, ' ');

    this.game.announce(status, 'assertive');
  }
}
```

---

## FEATURE 3: ACCESSIBILITY SETTINGS AND CUSTOMIZATION

### 3.1 Expanded Accessibility Panel

```html
<div class="accessibility-panel enhanced"
     id="accessibilityPanel"
     role="dialog"
     aria-labelledby="a11y-title"
     aria-modal="true">

  <h2 id="a11y-title">Accessibility & Control Settings</h2>

  <!-- Visual Settings -->
  <fieldset class="settings-section">
    <legend>Visual Settings</legend>

    <div class="setting-item">
      <input type="checkbox" id="highContrast" aria-describedby="high-contrast-desc">
      <label for="highContrast">High Contrast Mode</label>
      <p id="high-contrast-desc" class="setting-description">
        Increases contrast between UI elements for better visibility
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="colorblindMode" aria-describedby="colorblind-desc">
      <label for="colorblindMode">Colorblind-Friendly Mode</label>
      <p id="colorblind-desc" class="setting-description">
        Adds patterns and shapes to distinguish creature types and HP status
      </p>
      <select id="colorblindType" aria-label="Colorblind mode type">
        <option value="deuteranopia">Deuteranopia (Red-Green)</option>
        <option value="protanopia">Protanopia (Red)</option>
        <option value="tritanopia">Tritanopia (Blue-Yellow)</option>
      </select>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="largeText" aria-describedby="large-text-desc">
      <label for="largeText">Large Text</label>
      <p id="large-text-desc" class="setting-description">
        Increases text size by 20-50% for better readability
      </p>
      <label for="textSizeScale">Text Size: <span id="textSizeValue">120%</span></label>
      <input type="range" id="textSizeScale" min="100" max="200" step="10" value="120"
             aria-label="Text size percentage">
    </div>

    <div class="setting-item">
      <label for="uiScale">UI Scale: <span id="uiScaleValue">100%</span></label>
      <input type="range" id="uiScale" min="75" max="150" step="5" value="100"
             aria-label="Overall UI scale percentage">
      <p class="setting-description">
        Scale the entire interface up or down
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="showPatterns" aria-describedby="patterns-desc">
      <label for="showPatterns">Show Background Patterns</label>
      <p id="patterns-desc" class="setting-description">
        Add visual patterns to distinguish creature types (helps with color blindness)
      </p>
    </div>
  </fieldset>

  <!-- Motion & Animation Settings -->
  <fieldset class="settings-section">
    <legend>Motion & Animation Settings</legend>

    <div class="setting-item">
      <input type="checkbox" id="reducedMotion" aria-describedby="reduced-motion-desc">
      <label for="reducedMotion">Reduce Motion</label>
      <p id="reduced-motion-desc" class="setting-description">
        Minimizes animations and transitions
      </p>
    </div>

    <div class="setting-item">
      <label for="animationSpeed">Animation Speed: <span id="animSpeedValue">Normal</span></label>
      <input type="range" id="animationSpeed" min="50" max="200" step="25" value="100"
             aria-label="Animation speed percentage"
             aria-valuetext="Normal speed">
      <p class="setting-description">
        Adjust speed of battle animations and transitions
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="pauseOnFocusLoss" checked>
      <label for="pauseOnFocusLoss">Auto-Pause When Window Loses Focus</label>
    </div>
  </fieldset>

  <!-- Audio Settings -->
  <fieldset class="settings-section">
    <legend>Audio Settings</legend>

    <div class="setting-item">
      <input type="checkbox" id="audioDescriptions" aria-describedby="audio-desc-desc">
      <label for="audioDescriptions">Audio Descriptions</label>
      <p id="audio-desc-desc" class="setting-description">
        Spoken descriptions of visual-only events
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="soundEffectCues" checked aria-describedby="sfx-cues-desc">
      <label for="soundEffectCues">Sound Effect Cues</label>
      <p id="sfx-cues-desc" class="setting-description">
        Play sounds for menu navigation and actions
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="creatureTypeSounds" aria-describedby="type-sounds-desc">
      <label for="creatureTypeSounds">Creature Type Sounds</label>
      <p id="type-sounds-desc" class="setting-description">
        Unique sounds for each creature type when selected
      </p>
    </div>

    <div class="setting-item">
      <label for="masterVolume">Master Volume: <span id="masterVolValue">70%</span></label>
      <input type="range" id="masterVolume" min="0" max="100" step="5" value="70"
             aria-label="Master volume percentage">
    </div>

    <div class="setting-item">
      <label for="musicVolume">Music Volume: <span id="musicVolValue">50%</span></label>
      <input type="range" id="musicVolume" min="0" max="100" step="5" value="50"
             aria-label="Music volume percentage">
    </div>

    <div class="setting-item">
      <label for="sfxVolume">Sound Effects Volume: <span id="sfxVolValue">80%</span></label>
      <input type="range" id="sfxVolume" min="0" max="100" step="5" value="80"
             aria-label="Sound effects volume percentage">
    </div>
  </fieldset>

  <!-- Screen Reader Settings -->
  <fieldset class="settings-section">
    <legend>Screen Reader Settings</legend>

    <div class="setting-item">
      <input type="checkbox" id="enhancedScreenReader" aria-describedby="esr-desc">
      <label for="enhancedScreenReader">Enhanced Screen Reader Mode</label>
      <p id="esr-desc" class="setting-description">
        Provides detailed descriptions and additional context
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="verboseMode" aria-describedby="verbose-desc">
      <label for="verboseMode">Verbose Mode</label>
      <p id="verbose-desc" class="setting-description">
        Includes extra details like exact HP values, stat changes, and type matchups
      </p>
    </div>

    <div class="setting-item">
      <label for="textSpeed">Text Display Speed: <span id="textSpeedValue">Medium</span></label>
      <input type="range" id="textSpeed" min="1" max="5" step="1" value="3"
             aria-label="Text display speed"
             aria-valuetext="Medium speed">
      <p class="setting-description">
        How fast dialogue and messages appear
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="autoAdvanceText" aria-describedby="auto-advance-desc">
      <label for="autoAdvanceText">Auto-Advance Text</label>
      <p id="auto-advance-desc" class="setting-description">
        Text advances automatically after reading (no need to press A)
      </p>
      <label for="autoAdvanceDelay">Delay: <span id="autoDelayValue">3s</span></label>
      <input type="range" id="autoAdvanceDelay" min="1" max="10" step="1" value="3"
             aria-label="Auto advance delay in seconds">
    </div>

    <div class="setting-item">
      <input type="checkbox" id="announceMenuPosition" checked>
      <label for="announceMenuPosition">Announce Menu Position</label>
      <p class="setting-description">
        Announces "Item 3 of 5" when navigating menus
      </p>
    </div>
  </fieldset>

  <!-- Input & Control Settings -->
  <fieldset class="settings-section">
    <legend>Input & Control Settings</legend>

    <div class="setting-item">
      <input type="checkbox" id="stickyKeys" aria-describedby="sticky-keys-desc">
      <label for="stickyKeys">Sticky Keys</label>
      <p id="sticky-keys-desc" class="setting-description">
        Press modifier keys sequentially instead of holding
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="slowKeys" aria-describedby="slow-keys-desc">
      <label for="slowKeys">Slow Keys</label>
      <p id="slow-keys-desc" class="setting-description">
        Requires holding keys briefly before they register (reduces accidental presses)
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="keyRepeatDelay" checked>
      <label for="keyRepeatDelay">Increase Key Repeat Delay</label>
      <p class="setting-description">
        Prevents accidental rapid inputs
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="confirmActions" aria-describedby="confirm-desc">
      <label for="confirmActions">Confirm Important Actions</label>
      <p id="confirm-desc" class="setting-description">
        Asks for confirmation before using items or running from battle
      </p>
    </div>

    <div class="setting-item">
      <label for="controlScheme">Control Scheme:</label>
      <select id="controlScheme" aria-label="Choose control scheme">
        <option value="default">Default (Arrow Keys + Z/X)</option>
        <option value="wasd">WASD + J/K</option>
        <option value="vim">Vim (H/J/K/L)</option>
        <option value="custom">Custom...</option>
      </select>
    </div>

    <button class="secondary-btn" onclick="game.openKeyRemapping()">
      Remap Controls
    </button>
  </fieldset>

  <!-- Gameplay Assistance -->
  <fieldset class="settings-section">
    <legend>Gameplay Assistance</legend>

    <div class="setting-item">
      <input type="checkbox" id="showTypeEffectiveness" checked aria-describedby="type-eff-desc">
      <label for="showTypeEffectiveness">Show Type Effectiveness</label>
      <p id="type-eff-desc" class="setting-description">
        Displays which moves are super effective before you use them
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="battletutorials" checked aria-describedby="tutorials-desc">
      <label for="battletutorials">Battle Tutorials</label>
      <p id="tutorials-desc" class="setting-description">
        Helpful tips when encountering new mechanics
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="autoSwitchFainted" aria-describedby="auto-switch-desc">
      <label for="autoSwitchFainted">Auto-Switch Fainted Creatures</label>
      <p id="auto-switch-desc" class="setting-description">
        Automatically prompts to switch when a creature faints
      </p>
    </div>

    <div class="setting-item">
      <input type="checkbox" id="lowHPWarning" checked>
      <label for="lowHPWarning">Low HP Warnings</label>
      <p class="setting-description">
        Alerts you when your creature is below 25% HP
      </p>
    </div>
  </fieldset>

  <!-- Buttons -->
  <div class="settings-actions">
    <button class="primary-btn" onclick="game.saveAccessibilitySettings()">
      Save Settings
    </button>
    <button class="secondary-btn" onclick="game.resetAccessibilitySettings()">
      Reset to Defaults
    </button>
    <button class="secondary-btn" onclick="game.closeAccessibilityPanel()">
      Close
    </button>
  </div>

</div>
```

### 3.2 Additional Accessibility Features

#### Keyboard Shortcut Reference
```html
<!-- Keyboard Help Overlay (Press H anywhere) -->
<div class="keyboard-help-overlay" id="keyboardHelp" role="dialog" aria-hidden="true">
  <h2>Keyboard Shortcuts</h2>

  <section>
    <h3>Navigation</h3>
    <dl>
      <dt>Arrow Keys / WASD</dt>
      <dd>Move character / Navigate menus</dd>

      <dt>Tab</dt>
      <dd>Switch between menu sections</dd>

      <dt>Shift + Tab</dt>
      <dd>Move backwards between sections</dd>
    </dl>
  </section>

  <section>
    <h3>Actions</h3>
    <dl>
      <dt>Z / Enter / Space</dt>
      <dd>Confirm / Interact / Select</dd>

      <dt>X / Escape / Backspace</dt>
      <dd>Cancel / Go Back / Close</dd>

      <dt>Enter</dt>
      <dd>Open main menu (from overworld)</dd>

      <dt>Shift</dt>
      <dd>Open creature quick menu</dd>
    </dl>
  </section>

  <section>
    <h3>Battle Shortcuts</h3>
    <dl>
      <dt>1-4</dt>
      <dd>Quick select battle options or moves</dd>

      <dt>F</dt>
      <dd>Quick select Fight</dd>

      <dt>S</dt>
      <dd>Quick select Switch</dd>

      <dt>R</dt>
      <dd>Quick select Run</dd>
    </dl>
  </section>

  <section>
    <h3>Team Builder</h3>
    <dl>
      <dt>1-6</dt>
      <dd>Jump directly to party slot</dd>

      <dt>Q</dt>
      <dd>Open sort menu</dd>

      <dt>F</dt>
      <dd>Open filter menu</dd>

      <dt>D</dt>
      <dd>View creature details</dd>
    </dl>
  </section>

  <section>
    <h3>Accessibility</h3>
    <dl>
      <dt>Alt + A</dt>
      <dd>Open accessibility settings</dd>

      <dt>Ctrl + R</dt>
      <dd>Re-read last announcement</dd>

      <dt>Ctrl + S</dt>
      <dd>Read current game status</dd>

      <dt>H</dt>
      <dd>Show/hide this help</dd>
    </dl>
  </section>

  <button onclick="game.closeKeyboardHelp()">Close Help (Press H or X)</button>
</div>
```

#### Status Read-Out Function
```javascript
// Global shortcut: Ctrl + S reads full game state
readGameStatus() {
  let status = '';

  switch(this.state) {
    case 'OVERWORLD':
      status = `Exploring ${this.map.name}.
                Position: ${this.player.x}, ${this.player.y}.
                Facing ${this.player.facing}.
                Party: ${this.player.creatures.filter(c => c.hp > 0).length} creatures healthy.
                Press Enter for menu.`;
      break;

    case 'BATTLE':
      const player = this.battle.playerCreature;
      const enemy = this.battle.enemyCreature;
      status = `In battle, turn ${this.battleSystem.turnNumber}.
                Your ${player.name}: ${player.hp} of ${player.maxHp} HP.
                Enemy ${enemy.name}: ${Math.round((enemy.hp/enemy.maxHp)*100)} percent HP.
                ${this.battle.waitingForInput ? 'Your turn. Battle menu is open.' : 'Battle in progress.'}`;
      break;

    case 'MENU':
      status = `Main menu open. ${this.getMenuName()} selected.
                Party: ${this.player.creatures.length} creatures.
                Money: ${this.player.money} gold.`;
      break;

    case 'TEXT':
      status = `Dialogue box open. Press A to continue.`;
      break;
  }

  this.announce(status, 'assertive');
}

// Global shortcut: Ctrl + R repeats last announcement
repeatLastAnnouncement() {
  if (this.lastAnnouncement) {
    this.announce(this.lastAnnouncement, 'assertive');
  } else {
    this.announce('No recent announcement to repeat.', 'polite');
  }
}
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Team Builder Foundation
- [ ] Create `TeamBuilder` class with keyboard navigation
- [ ] Implement party slot management (6 slots max)
- [ ] Add storage creature list with filtering
- [ ] Implement swap and rearrange functionality
- [ ] Add sort options (level, name, HP, type)
- [ ] Add filter options (type, level range, health status)
- [ ] Create detailed stats view
- [ ] Add ARIA labels and semantic HTML
- [ ] Implement screen reader announcements
- [ ] Test with keyboard-only navigation

### Phase 2: Battle System Enhancements
- [ ] Add SWITCH option to battle menu
- [ ] Implement in-battle creature switching
- [ ] Create accessible switch menu with keyboard navigation
- [ ] Add comprehensive battle announcements
- [ ] Implement turn-by-turn status updates
- [ ] Add damage and effectiveness announcements
- [ ] Create battle log for review
- [ ] Add type matchup indicators (optional visual + always announced)
- [ ] Implement auto-switch prompt when creature faints
- [ ] Test screen reader battle flow

### Phase 3: Accessibility Settings
- [ ] Expand accessibility settings panel
- [ ] Add colorblind mode with patterns
- [ ] Implement UI scaling options
- [ ] Add animation speed controls
- [ ] Create audio description system
- [ ] Add verbose mode for detailed info
- [ ] Implement auto-advance text option
- [ ] Add control remapping interface
- [ ] Create gameplay assistance options
- [ ] Save/load accessibility preferences

### Phase 4: Global Accessibility Features
- [ ] Implement keyboard shortcut system
- [ ] Create help overlay (press H)
- [ ] Add status readout function (Ctrl + S)
- [ ] Add repeat announcement function (Ctrl + R)
- [ ] Implement focus management system
- [ ] Add skip links for major sections
- [ ] Create visual focus indicators
- [ ] Add high contrast mode styles
- [ ] Implement reduced motion mode
- [ ] Test with screen readers (NVDA, JAWS, VoiceOver)

### Phase 5: Testing & Refinement
- [ ] Keyboard-only playthrough (no mouse)
- [ ] Screen reader playthrough (NVDA)
- [ ] Screen reader playthrough (JAWS)
- [ ] Screen reader playthrough (VoiceOver)
- [ ] Colorblind mode testing (multiple types)
- [ ] Reduced motion testing
- [ ] High contrast testing
- [ ] Large text testing
- [ ] Touch controls testing (mobile)
- [ ] Gamepad support testing (if applicable)

---

## DESIGN PRINCIPLES SUMMARY

### 1. **Keyboard First**
Every feature must be fully accessible via keyboard alone. Mouse/touch are enhancements, not requirements.

### 2. **Semantic HTML + ARIA**
Use proper HTML elements (`<button>`, `<nav>`, `<section>`) and enhance with ARIA when needed.

### 3. **Announce Everything**
State changes, selections, results - all announced to screen readers via live regions.

### 4. **Multiple Cues**
Never rely on color alone. Use text, patterns, shapes, sounds, and position.

### 5. **Customizable Experience**
Provide settings for text size, contrast, motion, speed, verbosity, and controls.

### 6. **Graceful Degradation**
Features work with minimal settings, enhanced features are optional.

### 7. **Focus Management**
Always maintain clear focus, never trap users, provide escape routes.

### 8. **Consistent Patterns**
Same keys do same things across different contexts. Predictable navigation.

### 9. **Help & Documentation**
Built-in help (H key), tooltips, and descriptions available everywhere.

### 10. **Test With Real Users**
Design is validated by testing with screen reader users and keyboard-only users.

---

## CONCLUSION

This accessibility-first design ensures that **all players** can enjoy WoWmon regardless of visual, auditory, motor, or cognitive abilities. The Team Builder and Battle System enhancements are built from the ground up with accessibility as the primary concern, not an afterthought.

**Key Innovations:**
- Complete keyboard navigation with logical flow
- Comprehensive screen reader support with context-aware announcements
- Visual alternatives (patterns, text, multiple indicators)
- Customizable interface and controls
- Gameplay assistance options without removing challenge
- Detailed help and status readouts

**Next Steps:**
1. Implement Team Builder with Phase 1 checklist
2. Enhance Battle System with Phase 2 checklist
3. Expand Accessibility Settings with Phase 3 checklist
4. Add global features with Phase 4 checklist
5. Test thoroughly with Phase 5 checklist

This design can serve as a **model for accessible game design** in the local-first tools ecosystem.
