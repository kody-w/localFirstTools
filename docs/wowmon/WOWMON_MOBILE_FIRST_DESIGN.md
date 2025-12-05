# WoWmon Mobile-First Feature Design

**Agent 5: Mobile-First Strategy**
**Date:** 2025-10-12
**Target File:** `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html`

---

## Executive Summary

This document provides comprehensive mobile-first design specifications for three major feature additions to wowMon.html:
1. **Team Builder System** - Touch-optimized creature management
2. **Battle System Enhancements** - Gesture-based combat improvements
3. **Mobile-Specific Features** - Offline, performance, and UX enhancements

All designs prioritize **mobile and touch devices first**, with progressive enhancement for desktop users.

---

## Current Mobile Support Analysis

### Existing Strengths
- Responsive layout with `@media (max-width: 768px)` breakpoints
- Touch-action CSS properties (`touch-action: manipulation`, `touch-action: none`)
- Safe area insets for notched devices (`env(safe-area-inset-*)`)
- Portrait and landscape orientation support
- Minimum touch target sizes (48x48px dpad, 56-64px buttons)
- Fullscreen mode toggle for immersive gameplay
- `-webkit-tap-highlight-color: transparent` to prevent flash on tap

### Identified Gaps
- No swipe gesture support
- Limited creature management interface (only basic menu navigation)
- No drag-and-drop for team organization
- Battle interface relies on button presses (no gesture shortcuts)
- No haptic feedback for touch interactions
- Limited quick-access controls for common actions

---

## 1. TEAM BUILDER SYSTEM (Mobile-First)

### Overview
A touch-optimized interface for managing creature parties, with drag-and-drop reordering, swipe actions, and large tap targets.

### Design Principles
- **Portrait-first layout** - Stack elements vertically for thumb reach
- **Bottom sheet pattern** - Critical actions within thumb zone (bottom 40% of screen)
- **Large touch targets** - Minimum 56px height for all interactive elements
- **Visual feedback** - Immediate haptic/visual response to all touches
- **Gesture support** - Swipe, long-press, drag-and-drop

---

### 1.1 Touch Interaction Patterns

#### Primary Gestures
```javascript
// Gesture types supported
const GESTURES = {
    TAP: 'Select creature or action',
    LONG_PRESS: 'Open quick actions menu (800ms)',
    SWIPE_LEFT: 'Quick swap with next party slot',
    SWIPE_RIGHT: 'Quick swap with previous party slot',
    SWIPE_DOWN: 'Remove from party',
    DRAG: 'Reorder party position',
    PINCH: 'Zoom creature sprite (detail view)'
};
```

#### Gesture Implementation
```javascript
class TouchGestureHandler {
    constructor(element) {
        this.element = element;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchStartTime = 0;
        this.longPressTimer = null;
        this.isDragging = false;

        this.element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        this.element.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
        this.element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
    }

    handleTouchStart(e) {
        const touch = e.touches[0];
        this.touchStartX = touch.clientX;
        this.touchStartY = touch.clientY;
        this.touchStartTime = Date.now();

        // Start long-press timer
        this.longPressTimer = setTimeout(() => {
            this.triggerLongPress(e);
        }, 800);

        // Add visual feedback
        this.element.classList.add('touch-active');
    }

    handleTouchMove(e) {
        if (!e.touches[0]) return;

        const touch = e.touches[0];
        const deltaX = touch.clientX - this.touchStartX;
        const deltaY = touch.clientY - this.touchStartY;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

        // Cancel long-press if moved
        if (distance > 10) {
            clearTimeout(this.longPressTimer);
        }

        // Start drag if moved enough
        if (distance > 15 && !this.isDragging) {
            this.isDragging = true;
            this.triggerDragStart(e);
        }

        if (this.isDragging) {
            this.triggerDrag(e, deltaX, deltaY);
        }
    }

    handleTouchEnd(e) {
        clearTimeout(this.longPressTimer);
        this.element.classList.remove('touch-active');

        if (this.isDragging) {
            this.triggerDragEnd(e);
            this.isDragging = false;
            return;
        }

        const touch = e.changedTouches[0];
        const deltaX = touch.clientX - this.touchStartX;
        const deltaY = touch.clientY - this.touchStartY;
        const deltaTime = Date.now() - this.touchStartTime;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

        // Detect swipes (fast, directional)
        if (deltaTime < 300 && distance > 50) {
            const angle = Math.atan2(deltaY, deltaX) * 180 / Math.PI;

            if (Math.abs(angle) < 45) {
                this.triggerSwipe('right', distance);
            } else if (Math.abs(angle) > 135) {
                this.triggerSwipe('left', distance);
            } else if (angle > 45 && angle < 135) {
                this.triggerSwipe('down', distance);
            } else {
                this.triggerSwipe('up', distance);
            }
        } else if (distance < 10 && deltaTime < 300) {
            // Regular tap
            this.triggerTap(e);
        }
    }

    triggerTap(e) {
        this.element.dispatchEvent(new CustomEvent('gesture-tap', { detail: { event: e } }));
        this.hapticFeedback('light');
    }

    triggerLongPress(e) {
        this.element.dispatchEvent(new CustomEvent('gesture-longpress', { detail: { event: e } }));
        this.hapticFeedback('medium');
    }

    triggerSwipe(direction, distance) {
        this.element.dispatchEvent(new CustomEvent('gesture-swipe', {
            detail: { direction, distance }
        }));
        this.hapticFeedback('light');
    }

    triggerDragStart(e) {
        this.element.dispatchEvent(new CustomEvent('gesture-dragstart', { detail: { event: e } }));
        this.hapticFeedback('medium');
    }

    triggerDrag(e, deltaX, deltaY) {
        this.element.dispatchEvent(new CustomEvent('gesture-drag', {
            detail: { event: e, deltaX, deltaY }
        }));
    }

    triggerDragEnd(e) {
        this.element.dispatchEvent(new CustomEvent('gesture-dragend', { detail: { event: e } }));
        this.hapticFeedback('light');
    }

    hapticFeedback(intensity = 'light') {
        if (navigator.vibrate) {
            const patterns = {
                light: 10,
                medium: 20,
                heavy: 30
            };
            navigator.vibrate(patterns[intensity]);
        }
    }
}
```

---

### 1.2 Team Builder UI Layout

#### Mobile Portrait Layout (Primary)
```
┌─────────────────────────────┐
│  TEAM BUILDER               │ ← Header (fixed top)
├─────────────────────────────┤
│                             │
│  ┌────────────────────────┐ │
│  │ Party Slot 1          ││ │ ← Active creature
│  │ [Sprite] GNOLL Lv.15  ││ │   (Large, detailed)
│  │ HP: 45/45  ⚡Beast    ││ │   88px min height
│  └────────────────────────┘ │
│                             │
│  ┌────────────────────────┐ │
│  │ Party Slot 2 [+ADD]   ││ │ ← Empty slots
│  └────────────────────────┘ │   (56px min height)
│                             │
│  ┌────────────────────────┐ │
│  │ Party Slot 3 [+ADD]   ││ │
│  └────────────────────────┘ │
│                             │
│  ... (slots 4-6)           │
│                             │
│  ─────────────────────────  │ ← Scrollable separator
│                             │
│  BOX CREATURES (12/100)     │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ │ ← Grid of owned
│  │🦊│ │🐺│ │🦅│ │🐉│ │🦇│ │   creatures
│  └──┘ └──┘ └──┘ └──┘ └──┘ │   48x48px tiles
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ │
│  │🦎│ │🐢│ │🦈│ │🦑│ │🕷│ │
│  └──┘ └──┘ └──┘ └──┘ └──┘ │
│                             │
└─────────────────────────────┘
│ [✓] [↻] [≡]               │ ← Bottom action bar
└─────────────────────────────┘   (64px min height)
```

#### Mobile Landscape Layout
```
┌───────────────────┬─────────────────────────────┐
│ PARTY (Left 40%) │ BOX CREATURES (Right 60%)  │
├───────────────────┼─────────────────────────────┤
│ ┌──────────────┐  │ ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐ │
│ │ Slot 1       │  │ │🦊││🐺││🦅││🐉││🦇││🦎│ │
│ │ GNOLL Lv.15  │  │ └──┘└──┘└──┘└──┘└──┘└──┘ │
│ └──────────────┘  │ ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐ │
│                   │ │🐢││🦈││🦑││🕷││🦂││🐍│ │
│ ┌──────────────┐  │ └──┘└──┘└──┘└──┘└──┘└──┘ │
│ │ Slot 2 [+]   │  │ ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐ │
│ └──────────────┘  │ │..││..││..││..││..││..│ │
│                   │ └──┘└──┘└──┘└──┘└──┘└──┘ │
│ ... (slots 3-6)   │                            │
│                   │ Filter: [All▼] Sort:[Lvl▼]│
│ [✓] [↻] [≡]      │                            │
└───────────────────┴─────────────────────────────┘
```

---

### 1.3 Responsive CSS for Team Builder

```css
/* Team Builder Container */
.team-builder {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gb-lightest);
    display: none;
    flex-direction: column;
    z-index: 5000;
    overflow: hidden;
}

.team-builder.active {
    display: flex;
}

/* Header */
.team-builder-header {
    background: var(--gb-darkest);
    color: var(--gb-lightest);
    padding: 16px;
    min-height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 18px;
    font-weight: bold;
    position: sticky;
    top: 0;
    z-index: 100;
    /* Safe area for notched devices */
    padding-top: max(16px, env(safe-area-inset-top));
}

.team-builder-header button {
    background: transparent;
    border: 2px solid var(--gb-lightest);
    color: var(--gb-lightest);
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    min-height: 40px;
    min-width: 40px;
    touch-action: manipulation;
}

/* Party Section */
.party-section {
    flex-shrink: 0;
    padding: 12px;
    border-bottom: 2px solid var(--gb-darkest);
}

.party-slot {
    background: var(--gb-light);
    border: 3px solid var(--gb-darkest);
    border-radius: 8px;
    margin-bottom: 12px;
    min-height: 88px;
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
    touch-action: none;
    -webkit-user-select: none;
    user-select: none;
}

/* Touch feedback */
.party-slot.touch-active {
    transform: scale(0.98);
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
}

.party-slot.dragging {
    opacity: 0.7;
    transform: scale(1.05) rotate(2deg);
    box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    z-index: 1000;
}

/* Empty slot state */
.party-slot.empty {
    min-height: 64px;
    justify-content: center;
    border-style: dashed;
    background: var(--gb-lightest);
}

.party-slot.empty .add-button {
    font-size: 24px;
    color: var(--gb-dark);
}

/* Creature info in slot */
.party-slot .creature-sprite {
    width: 64px;
    height: 64px;
    background: var(--gb-lightest);
    border: 2px solid var(--gb-darkest);
    border-radius: 4px;
    image-rendering: pixelated;
    flex-shrink: 0;
}

.party-slot .creature-info {
    flex: 1;
    min-width: 0;
}

.party-slot .creature-name {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.party-slot .creature-stats {
    font-size: 12px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.party-slot .creature-hp-bar {
    height: 6px;
    background: var(--gb-darkest);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 4px;
}

.party-slot .creature-hp-fill {
    height: 100%;
    background: var(--gb-dark);
    transition: width 0.3s;
}

/* Quick action button (appears on long-press) */
.party-slot .quick-actions {
    position: absolute;
    top: 8px;
    right: 8px;
    background: var(--gb-darkest);
    color: var(--gb-lightest);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    display: none;
    z-index: 10;
}

.party-slot.show-actions .quick-actions {
    display: block;
}

/* Box Creatures Section (scrollable) */
.box-section {
    flex: 1;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding: 12px;
    padding-bottom: 80px; /* Space for bottom bar */
}

.box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 14px;
    font-weight: bold;
}

.box-filters {
    display: flex;
    gap: 8px;
}

.box-filters select {
    background: var(--gb-light);
    border: 2px solid var(--gb-darkest);
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
    min-height: 40px;
    font-family: monospace;
}

.box-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 8px;
}

.box-creature-tile {
    aspect-ratio: 1;
    background: var(--gb-light);
    border: 2px solid var(--gb-darkest);
    border-radius: 4px;
    padding: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    touch-action: manipulation;
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s;
}

.box-creature-tile:active {
    transform: scale(0.95);
    border-color: var(--gb-dark);
}

.box-creature-tile.selected {
    border-color: #ffcc00;
    border-width: 3px;
    background: var(--gb-lightest);
}

.box-creature-tile .tile-sprite {
    width: 48px;
    height: 48px;
    image-rendering: pixelated;
}

.box-creature-tile .tile-name {
    font-size: 10px;
    text-align: center;
    margin-top: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.box-creature-tile .tile-level {
    position: absolute;
    top: 4px;
    right: 4px;
    background: var(--gb-darkest);
    color: var(--gb-lightest);
    font-size: 10px;
    padding: 2px 4px;
    border-radius: 2px;
}

.box-creature-tile .tile-hp-indicator {
    position: absolute;
    bottom: 4px;
    left: 4px;
    right: 4px;
    height: 3px;
    background: var(--gb-darkest);
    border-radius: 2px;
}

.box-creature-tile .tile-hp-fill {
    height: 100%;
    background: var(--gb-dark);
}

.box-creature-tile.fainted {
    opacity: 0.5;
    background: #999;
}

.box-creature-tile.fainted::after {
    content: '✗';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 32px;
    color: #8b0000;
}

/* Bottom Action Bar */
.team-builder-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--gb-darkest);
    padding: 12px;
    display: flex;
    gap: 12px;
    justify-content: space-around;
    box-shadow: 0 -4px 8px rgba(0,0,0,0.3);
    /* Safe area for devices with bottom gestures */
    padding-bottom: max(12px, env(safe-area-inset-bottom));
    min-height: 64px;
    z-index: 100;
}

.team-builder-actions button {
    flex: 1;
    background: var(--gb-light);
    border: 2px solid var(--gb-lightest);
    color: var(--gb-darkest);
    padding: 12px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    min-height: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    touch-action: manipulation;
    transition: transform 0.1s;
}

.team-builder-actions button:active {
    transform: scale(0.95);
}

.team-builder-actions button .button-icon {
    font-size: 20px;
}

.team-builder-actions button .button-label {
    font-size: 12px;
}

/* Landscape Mode Adjustments */
@media (max-width: 932px) and (orientation: landscape) {
    .team-builder {
        flex-direction: row;
    }

    .party-section {
        width: 40%;
        border-right: 2px solid var(--gb-darkest);
        border-bottom: none;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }

    .party-slot {
        min-height: 72px;
    }

    .party-slot .creature-sprite {
        width: 48px;
        height: 48px;
    }

    .box-section {
        width: 60%;
        padding-bottom: 12px;
    }

    .box-grid {
        grid-template-columns: repeat(auto-fill, minmax(64px, 1fr));
    }

    .team-builder-actions {
        position: absolute;
        bottom: 12px;
        left: 12px;
        width: calc(40% - 24px);
        flex-direction: column;
        background: transparent;
        box-shadow: none;
        padding: 0;
        gap: 8px;
    }

    .team-builder-actions button {
        min-height: 40px;
        font-size: 14px;
    }
}

/* Small phones (< 375px width) */
@media (max-width: 375px) {
    .party-slot {
        min-height: 72px;
        padding: 8px;
    }

    .party-slot .creature-sprite {
        width: 48px;
        height: 48px;
    }

    .party-slot .creature-name {
        font-size: 14px;
    }

    .box-grid {
        grid-template-columns: repeat(auto-fill, minmax(64px, 1fr));
    }

    .team-builder-actions button {
        font-size: 14px;
        padding: 8px;
    }
}

/* High contrast mode support */
body.high-contrast .party-slot,
body.high-contrast .box-creature-tile {
    border-width: 3px;
}

body.high-contrast .party-slot.selected,
body.high-contrast .box-creature-tile.selected {
    border-width: 4px;
    border-color: #ffff00;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .party-slot,
    .box-creature-tile,
    .team-builder-actions button {
        transition: none !important;
    }
}
```

---

### 1.4 Team Builder JavaScript Logic

```javascript
class TeamBuilder {
    constructor(game) {
        this.game = game;
        this.maxPartySize = 6;
        this.party = []; // Array of creature objects
        this.box = []; // Array of all owned creatures not in party
        this.selectedCreature = null;
        this.draggedSlot = null;
        this.gestureHandlers = new Map();

        this.init();
    }

    init() {
        // Create team builder UI
        this.createUI();

        // Load party from game state
        this.loadParty();

        // Setup gesture handlers
        this.setupGestureHandlers();
    }

    createUI() {
        const teamBuilder = document.createElement('div');
        teamBuilder.className = 'team-builder';
        teamBuilder.id = 'teamBuilder';
        teamBuilder.innerHTML = `
            <div class="team-builder-header">
                <button id="teamBuilderClose" aria-label="Close team builder">✕</button>
                <span>TEAM BUILDER</span>
                <button id="teamBuilderSort" aria-label="Sort creatures">↕</button>
            </div>

            <div class="party-section">
                <div id="partySlots"></div>
            </div>

            <div class="box-section">
                <div class="box-header">
                    <span id="boxCount">BOX CREATURES (0/100)</span>
                    <div class="box-filters">
                        <select id="filterType" aria-label="Filter by type">
                            <option value="all">All Types</option>
                            <option value="beast">Beast</option>
                            <option value="dragon">Dragon</option>
                            <option value="elemental">Elemental</option>
                            <option value="magic">Magic</option>
                            <option value="shadow">Shadow</option>
                            <option value="water">Water</option>
                            <option value="fire">Fire</option>
                        </select>
                        <select id="sortOrder" aria-label="Sort creatures">
                            <option value="level">Level</option>
                            <option value="name">Name</option>
                            <option value="hp">HP</option>
                            <option value="recent">Recent</option>
                        </select>
                    </div>
                </div>
                <div class="box-grid" id="boxGrid"></div>
            </div>

            <div class="team-builder-actions">
                <button id="confirmTeam" aria-label="Confirm team changes">
                    <span class="button-icon">✓</span>
                    <span class="button-label">Confirm</span>
                </button>
                <button id="autoFill" aria-label="Auto-fill team with strongest creatures">
                    <span class="button-icon">↻</span>
                    <span class="button-label">Auto-fill</span>
                </button>
                <button id="healAll" aria-label="Heal all party creatures">
                    <span class="button-icon">❤</span>
                    <span class="button-label">Heal All</span>
                </button>
            </div>
        `;

        document.body.appendChild(teamBuilder);

        // Event listeners for buttons
        document.getElementById('teamBuilderClose').addEventListener('click', () => this.close());
        document.getElementById('confirmTeam').addEventListener('click', () => this.confirmChanges());
        document.getElementById('autoFill').addEventListener('click', () => this.autoFillParty());
        document.getElementById('healAll').addEventListener('click', () => this.healAllParty());
        document.getElementById('filterType').addEventListener('change', () => this.refreshBox());
        document.getElementById('sortOrder').addEventListener('change', () => this.refreshBox());
    }

    setupGestureHandlers() {
        // Will be added to each party slot dynamically
    }

    open() {
        document.getElementById('teamBuilder').classList.add('active');
        this.refreshParty();
        this.refreshBox();

        // Announce to screen readers
        this.game.announceToScreenReader('Team builder opened');

        // Haptic feedback
        if (navigator.vibrate) navigator.vibrate(10);
    }

    close() {
        document.getElementById('teamBuilder').classList.remove('active');
        this.game.announceToScreenReader('Team builder closed');
        if (navigator.vibrate) navigator.vibrate(10);
    }

    loadParty() {
        // Load current party from game state
        this.party = this.game.player.creatures.slice(0, this.maxPartySize);
        this.box = this.game.player.creatures.slice(this.maxPartySize);
    }

    refreshParty() {
        const partySlots = document.getElementById('partySlots');
        partySlots.innerHTML = '';

        for (let i = 0; i < this.maxPartySize; i++) {
            const creature = this.party[i];
            const slot = this.createPartySlot(i, creature);
            partySlots.appendChild(slot);
        }
    }

    createPartySlot(index, creature) {
        const slot = document.createElement('div');
        slot.className = creature ? 'party-slot' : 'party-slot empty';
        slot.dataset.slotIndex = index;

        if (creature) {
            const hpPercent = (creature.hp / creature.maxHp) * 100;
            const creatureData = this.game.cartridge.creatures[creature.id];

            slot.innerHTML = `
                <div class="creature-sprite">
                    <!-- Render sprite here -->
                </div>
                <div class="creature-info">
                    <div class="creature-name">${creature.name}</div>
                    <div class="creature-stats">
                        <span>Lv.${creature.level}</span>
                        <span>HP: ${creature.hp}/${creature.maxHp}</span>
                        <span>${creatureData.type.join('/')}</span>
                    </div>
                    <div class="creature-hp-bar">
                        <div class="creature-hp-fill" style="width: ${hpPercent}%"></div>
                    </div>
                </div>
                <div class="quick-actions">⋮</div>
            `;

            // Setup gesture handler
            const gestureHandler = new TouchGestureHandler(slot);
            this.gestureHandlers.set(slot, gestureHandler);

            // Gesture event listeners
            slot.addEventListener('gesture-tap', (e) => {
                this.handleSlotTap(index);
            });

            slot.addEventListener('gesture-longpress', (e) => {
                this.handleSlotLongPress(index);
            });

            slot.addEventListener('gesture-swipe', (e) => {
                this.handleSlotSwipe(index, e.detail.direction);
            });

            slot.addEventListener('gesture-dragstart', (e) => {
                this.handleDragStart(index);
            });

            slot.addEventListener('gesture-drag', (e) => {
                this.handleDrag(index, e.detail.deltaX, e.detail.deltaY);
            });

            slot.addEventListener('gesture-dragend', (e) => {
                this.handleDragEnd(index);
            });
        } else {
            slot.innerHTML = `
                <div class="add-button">+ Add Creature</div>
            `;

            slot.addEventListener('click', () => {
                this.handleEmptySlotTap(index);
            });
        }

        return slot;
    }

    handleSlotTap(index) {
        // Show quick info or toggle selection
        const creature = this.party[index];
        if (!creature) return;

        this.selectedCreature = creature;
        this.game.announceToScreenReader(`Selected ${creature.name}, level ${creature.level}`);

        // Visual feedback
        document.querySelectorAll('.party-slot').forEach(s => s.classList.remove('selected'));
        document.querySelector(`[data-slot-index="${index}"]`).classList.add('selected');
    }

    handleSlotLongPress(index) {
        // Show quick actions menu
        const slot = document.querySelector(`[data-slot-index="${index}"]`);
        slot.classList.toggle('show-actions');

        // Create context menu
        this.showQuickActionsMenu(index);
    }

    handleSlotSwipe(index, direction) {
        const creature = this.party[index];
        if (!creature) return;

        switch(direction) {
            case 'left':
                // Swap with next slot
                if (index < this.maxPartySize - 1) {
                    this.swapPartySlots(index, index + 1);
                }
                break;
            case 'right':
                // Swap with previous slot
                if (index > 0) {
                    this.swapPartySlots(index, index - 1);
                }
                break;
            case 'down':
                // Remove from party
                this.removeFromParty(index);
                break;
        }
    }

    handleDragStart(index) {
        this.draggedSlot = index;
        const slot = document.querySelector(`[data-slot-index="${index}"]`);
        slot.classList.add('dragging');

        this.game.announceToScreenReader(`Dragging ${this.party[index].name}`);
    }

    handleDrag(index, deltaX, deltaY) {
        // Update visual position during drag
        const slot = document.querySelector(`[data-slot-index="${index}"]`);
        slot.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.05)`;
    }

    handleDragEnd(index) {
        const slot = document.querySelector(`[data-slot-index="${index}"]`);
        slot.classList.remove('dragging');
        slot.style.transform = '';

        // Determine drop target
        const dropTarget = this.getDropTarget(slot);
        if (dropTarget && dropTarget !== index) {
            this.swapPartySlots(index, dropTarget);
        }

        this.draggedSlot = null;
    }

    getDropTarget(draggedElement) {
        // Get all party slots
        const slots = Array.from(document.querySelectorAll('.party-slot'));
        const draggedRect = draggedElement.getBoundingClientRect();
        const draggedCenter = {
            x: draggedRect.left + draggedRect.width / 2,
            y: draggedRect.top + draggedRect.height / 2
        };

        // Find closest slot
        let closestSlot = null;
        let closestDistance = Infinity;

        slots.forEach((slot, index) => {
            if (slot === draggedElement) return;

            const rect = slot.getBoundingClientRect();
            const center = {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };

            const distance = Math.sqrt(
                Math.pow(center.x - draggedCenter.x, 2) +
                Math.pow(center.y - draggedCenter.y, 2)
            );

            if (distance < closestDistance) {
                closestDistance = distance;
                closestSlot = index;
            }
        });

        return closestDistance < 100 ? closestSlot : null;
    }

    handleEmptySlotTap(index) {
        // Open box selection mode
        this.game.announceToScreenReader('Select a creature from your box');

        // Highlight available creatures
        document.querySelectorAll('.box-creature-tile').forEach(tile => {
            tile.classList.add('selectable');
        });
    }

    swapPartySlots(fromIndex, toIndex) {
        const temp = this.party[fromIndex];
        this.party[fromIndex] = this.party[toIndex];
        this.party[toIndex] = temp;

        this.refreshParty();

        if (navigator.vibrate) navigator.vibrate(20);
        this.game.announceToScreenReader('Party order updated');
    }

    removeFromParty(index) {
        const creature = this.party[index];
        if (!creature) return;

        // Move to box
        this.box.push(creature);
        this.party.splice(index, 1);

        this.refreshParty();
        this.refreshBox();

        if (navigator.vibrate) navigator.vibrate([10, 50, 10]);
        this.game.announceToScreenReader(`${creature.name} removed from party`);
    }

    addToParty(creature) {
        if (this.party.length >= this.maxPartySize) {
            this.game.announceToScreenReader('Party is full');
            return;
        }

        // Remove from box
        const boxIndex = this.box.indexOf(creature);
        if (boxIndex !== -1) {
            this.box.splice(boxIndex, 1);
        }

        this.party.push(creature);

        this.refreshParty();
        this.refreshBox();

        if (navigator.vibrate) navigator.vibrate(20);
        this.game.announceToScreenReader(`${creature.name} added to party`);
    }

    refreshBox() {
        const grid = document.getElementById('boxGrid');
        const filterType = document.getElementById('filterType').value;
        const sortOrder = document.getElementById('sortOrder').value;

        // Filter creatures
        let creatures = [...this.box];

        if (filterType !== 'all') {
            creatures = creatures.filter(c => {
                const data = this.game.cartridge.creatures[c.id];
                return data.type.includes(filterType);
            });
        }

        // Sort creatures
        creatures.sort((a, b) => {
            switch(sortOrder) {
                case 'level':
                    return b.level - a.level;
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'hp':
                    return b.hp - a.hp;
                case 'recent':
                    return b.caughtTimestamp - a.caughtTimestamp;
                default:
                    return 0;
            }
        });

        // Render tiles
        grid.innerHTML = '';
        creatures.forEach((creature, index) => {
            const tile = this.createBoxTile(creature);
            grid.appendChild(tile);
        });

        // Update count
        document.getElementById('boxCount').textContent =
            `BOX CREATURES (${this.box.length}/100)`;
    }

    createBoxTile(creature) {
        const tile = document.createElement('div');
        tile.className = 'box-creature-tile';
        tile.dataset.creatureId = creature.id;

        const hpPercent = (creature.hp / creature.maxHp) * 100;
        const isFainted = creature.hp <= 0;

        if (isFainted) {
            tile.classList.add('fainted');
        }

        tile.innerHTML = `
            <div class="tile-sprite">
                <!-- Render sprite here -->
            </div>
            <div class="tile-name">${creature.name}</div>
            <div class="tile-level">Lv.${creature.level}</div>
            <div class="tile-hp-indicator">
                <div class="tile-hp-fill" style="width: ${hpPercent}%"></div>
            </div>
        `;

        tile.addEventListener('click', () => {
            if (!isFainted) {
                this.addToParty(creature);
            } else {
                this.game.announceToScreenReader(`${creature.name} has fainted and cannot battle`);
            }
        });

        return tile;
    }

    showQuickActionsMenu(slotIndex) {
        const creature = this.party[slotIndex];
        if (!creature) return;

        // Create modal menu
        const menu = document.createElement('div');
        menu.className = 'quick-actions-menu';
        menu.innerHTML = `
            <div class="quick-actions-backdrop"></div>
            <div class="quick-actions-content">
                <h3>${creature.name}</h3>
                <button class="quick-action-btn" data-action="view">View Details</button>
                <button class="quick-action-btn" data-action="moves">Change Moves</button>
                <button class="quick-action-btn" data-action="heal">Heal</button>
                <button class="quick-action-btn" data-action="remove">Remove from Party</button>
                <button class="quick-action-btn" data-action="cancel">Cancel</button>
            </div>
        `;

        document.body.appendChild(menu);

        // Add event listeners
        menu.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleQuickAction(slotIndex, action);
                menu.remove();
            });
        });

        // Close on backdrop click
        menu.querySelector('.quick-actions-backdrop').addEventListener('click', () => {
            menu.remove();
        });
    }

    handleQuickAction(slotIndex, action) {
        const creature = this.party[slotIndex];

        switch(action) {
            case 'view':
                this.showCreatureDetails(creature);
                break;
            case 'moves':
                this.showMoveManager(creature);
                break;
            case 'heal':
                this.healCreature(creature);
                break;
            case 'remove':
                this.removeFromParty(slotIndex);
                break;
        }
    }

    healCreature(creature) {
        creature.hp = creature.maxHp;
        this.refreshParty();
        if (navigator.vibrate) navigator.vibrate(20);
        this.game.announceToScreenReader(`${creature.name} fully healed`);
    }

    healAllParty() {
        this.party.forEach(creature => {
            if (creature) {
                creature.hp = creature.maxHp;
            }
        });
        this.refreshParty();
        if (navigator.vibrate) navigator.vibrate([20, 50, 20]);
        this.game.announceToScreenReader('All party creatures healed');
    }

    autoFillParty() {
        // Fill party with strongest available creatures
        const available = [...this.box].sort((a, b) => {
            // Sort by: 1) Not fainted, 2) Level, 3) HP
            if (a.hp > 0 && b.hp <= 0) return -1;
            if (a.hp <= 0 && b.hp > 0) return 1;
            if (a.level !== b.level) return b.level - a.level;
            return b.hp - a.hp;
        });

        // Fill empty slots
        while (this.party.length < this.maxPartySize && available.length > 0) {
            const creature = available.shift();
            if (creature.hp > 0) {
                this.addToParty(creature);
            }
        }

        if (navigator.vibrate) navigator.vibrate([20, 30, 20]);
        this.game.announceToScreenReader('Party auto-filled with strongest creatures');
    }

    confirmChanges() {
        // Save party to game state
        this.game.player.creatures = [...this.party, ...this.box];

        // Close team builder
        this.close();

        if (navigator.vibrate) navigator.vibrate([20, 50, 20, 50, 20]);
        this.game.announceToScreenReader('Team changes saved');
    }

    showCreatureDetails(creature) {
        // Implementation for detailed view (see next section)
    }

    showMoveManager(creature) {
        // Implementation for move management
    }
}
```

---

### 1.5 Integration with Main Game

```javascript
// In GameEngine class, add team builder initialization
class GameEngine {
    constructor() {
        // ... existing code ...
        this.teamBuilder = new TeamBuilder(this);
    }

    // Add keyboard shortcut to open team builder
    handleInput(key) {
        // ... existing code ...

        if (key === 'Enter') {
            // Open main menu
            if (!this.menuOpen) {
                this.openMainMenu();
            }
        }

        // ... existing code ...
    }

    openMainMenu() {
        // ... existing menu code ...

        // Add "TEAM" option to main menu
        const menuOptions = [
            'CREATURES', // Opens team builder
            'BAG',
            'SAVE',
            'EXIT'
        ];
    }

    handleMenuSelection(option) {
        switch(option) {
            case 'CREATURES':
                this.teamBuilder.open();
                break;
            // ... other cases ...
        }
    }
}
```

---

## 2. BATTLE SYSTEM ENHANCEMENTS (Mobile-First)

### Overview
Transform the battle interface with gesture-based controls, swipe-to-attack, quick action buttons, and mobile-optimized UI.

### Design Principles
- **Gesture-first combat** - Swipe directions for different move types
- **Large tap zones** - 64px minimum for all battle buttons
- **Visual clarity** - Clear HP bars, type advantages, status effects
- **Quick actions** - Single-tap access to common moves
- **Battle flow** - Minimize taps between actions

---

### 2.1 Battle UI Redesign (Mobile)

#### Portrait Battle Layout
```
┌─────────────────────────────┐
│ ENEMY                       │ ← Enemy info (top)
│ GNOLL Lv.12  HP: ████░░ 75%│   Fixed position
├─────────────────────────────┤
│                             │
│         [ENEMY]             │ ← Battle sprites
│           ☻                │   (scaled for mobile)
│                             │
│                             │
│           ◉                │ ← Player sprite
│         [YOURS]             │   (larger, prominent)
│                             │
├─────────────────────────────┤
│ YOUR GNOLL Lv.10            │ ← Player info
│ HP: ████████░░░ 80% (24/30)│   (detailed)
├─────────────────────────────┤
│ ┌─────────┐ ┌─────────┐   │ ← Move buttons
│ │  BITE   │ │  HOWL   │   │   (2x2 grid)
│ │ PP 10/15│ │ PP 5/10 │   │   64px min height
│ └─────────┘ └─────────┘   │
│ ┌─────────┐ ┌─────────┐   │
│ │ SLASH   │ │ CRUNCH  │   │
│ │ PP 8/20 │ │ PP 3/5  │   │
│ └─────────┘ └─────────┘   │
└─────────────────────────────┘
│ [⚔] [👥] [🎒] [🏃]        │ ← Quick actions
└─────────────────────────────┘   (bottom bar)
```

#### Landscape Battle Layout
```
┌────────────┬──────────────────────────────┐
│  ENEMY     │                              │
│  GNOLL 12  │         [ENEMY]              │
│  HP: ███   │           ☻                 │
│            │                              │
│            │                              │
│  YOURS     │           ◉                 │
│  GNOLL 10  │         [YOURS]              │
│  HP: ████  │                              │
│  24/30 80% │                              │
├────────────┼──────────────────────────────┤
│ BITE 10/15 │ HOWL  5/10                   │
│ SLASH 8/20 │ CRUNCH 3/5                   │
└────────────┴──────────────────────────────┘
```

---

### 2.2 Gesture-Based Battle Controls

```javascript
class BattleGestureController {
    constructor(battleSystem) {
        this.battle = battleSystem;
        this.canvas = document.getElementById('gameCanvas');
        this.gestureZone = null;
        this.init();
    }

    init() {
        // Create gesture zone overlay
        this.gestureZone = document.createElement('div');
        this.gestureZone.id = 'battleGestureZone';
        this.gestureZone.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 200px;
            pointer-events: auto;
            z-index: 100;
        `;

        const gameScreen = document.querySelector('.game-screen');
        gameScreen.appendChild(this.gestureZone);

        // Setup gesture handler
        this.gestureHandler = new TouchGestureHandler(this.gestureZone);

        // Listen for gestures
        this.gestureZone.addEventListener('gesture-swipe', (e) => {
            this.handleBattleSwipe(e.detail.direction);
        });

        this.gestureZone.addEventListener('gesture-tap', (e) => {
            this.handleBattleTap(e);
        });
    }

    handleBattleSwipe(direction) {
        if (!this.battle.isPlayerTurn) return;

        const moves = this.battle.playerCreature.moves;

        // Map swipe directions to move slots
        const moveMap = {
            'up': 0,    // Slot 1 (usually primary attack)
            'right': 1, // Slot 2 (usually secondary attack)
            'down': 2,  // Slot 3 (usually buff/status)
            'left': 3   // Slot 4 (usually special/ultimate)
        };

        const moveIndex = moveMap[direction];
        if (moves[moveIndex]) {
            this.battle.selectMove(moveIndex);

            // Visual feedback
            this.showSwipeEffect(direction);

            // Haptic feedback
            if (navigator.vibrate) navigator.vibrate(30);

            // Announce to screen reader
            const move = this.battle.game.cartridge.moves[moves[moveIndex]];
            this.battle.game.announceToScreenReader(
                `Used ${move.name} - swipe ${direction}`
            );
        }
    }

    handleBattleTap(e) {
        // Double-tap to use first move (quick attack)
        if (this.lastTapTime && Date.now() - this.lastTapTime < 300) {
            this.battle.selectMove(0);
            if (navigator.vibrate) navigator.vibrate([10, 20, 10]);
        }
        this.lastTapTime = Date.now();
    }

    showSwipeEffect(direction) {
        // Create visual swipe indicator
        const effect = document.createElement('div');
        effect.className = `swipe-effect swipe-${direction}`;
        effect.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            color: var(--gb-darkest);
            pointer-events: none;
            z-index: 1000;
            animation: swipe-fade 0.5s ease-out;
        `;

        const arrows = {
            'up': '⬆',
            'down': '⬇',
            'left': '⬅',
            'right': '➡'
        };

        effect.textContent = arrows[direction];
        this.gestureZone.appendChild(effect);

        setTimeout(() => effect.remove(), 500);
    }

    enable() {
        this.gestureZone.style.display = 'block';
    }

    disable() {
        this.gestureZone.style.display = 'none';
    }
}

// Add animation to CSS
const swipeEffectCSS = `
@keyframes swipe-fade {
    0% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }
    100% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(2);
    }
}

.swipe-effect.swipe-up {
    animation: swipe-fade 0.5s ease-out, swipe-move-up 0.5s ease-out;
}

@keyframes swipe-move-up {
    from { transform: translate(-50%, -50%); }
    to { transform: translate(-50%, -150%); }
}

.swipe-effect.swipe-down {
    animation: swipe-fade 0.5s ease-out, swipe-move-down 0.5s ease-out;
}

@keyframes swipe-move-down {
    from { transform: translate(-50%, -50%); }
    to { transform: translate(-50%, 50%); }
}

.swipe-effect.swipe-left {
    animation: swipe-fade 0.5s ease-out, swipe-move-left 0.5s ease-out;
}

@keyframes swipe-move-left {
    from { transform: translate(-50%, -50%); }
    to { transform: translate(-150%, -50%); }
}

.swipe-effect.swipe-right {
    animation: swipe-fade 0.5s ease-out, swipe-move-right 0.5s ease-out;
}

@keyframes swipe-move-right {
    from { transform: translate(-50%, -50%); }
    to { transform: translate(50%, -50%); }
}
`;
```

---

### 2.3 Enhanced Battle UI (CSS)

```css
/* Mobile Battle Interface Enhancements */

/* Battle container adjustments for mobile */
@media (max-width: 768px) {
    .battle-ui {
        pointer-events: all; /* Enable touch on entire battle area */
    }

    /* Larger creature info panels */
    .creature-info {
        font-size: 14px;
        padding: 8px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .enemy-info {
        top: 16px;
        left: 16px;
        right: 16px;
        max-width: none;
    }

    .player-info {
        bottom: 240px; /* Above move menu */
        right: 16px;
        left: 16px;
        max-width: none;
    }

    /* Larger HP bars */
    .hp-bar {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        margin: 4px 0;
    }

    /* Type indicators */
    .creature-type {
        display: inline-block;
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10px;
        margin-top: 4px;
    }

    /* Move Menu - Larger touch targets */
    .move-menu {
        bottom: 16px;
        left: 16px;
        right: 16px;
        padding: 12px;
        gap: 12px;
        border-radius: 12px;
        box-shadow: 0 -4px 16px rgba(0,0,0,0.4);
    }

    .move-option {
        min-height: 72px;
        padding: 12px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 4px;
        font-size: 14px;
        font-weight: bold;
        position: relative;
        transition: transform 0.1s, background 0.2s;
    }

    .move-option:active {
        transform: scale(0.95);
    }

    .move-option.selected {
        border-width: 3px;
        transform: scale(1.05);
    }

    /* Move type indicator */
    .move-option::before {
        content: attr(data-type);
        position: absolute;
        top: 4px;
        right: 4px;
        font-size: 10px;
        background: var(--gb-darkest);
        color: var(--gb-lightest);
        padding: 2px 4px;
        border-radius: 2px;
    }

    /* Low PP warning */
    .move-option.low-pp {
        border-color: #ff6b6b;
        background: #ffe5e5;
    }

    .move-option.no-pp {
        opacity: 0.4;
        pointer-events: none;
    }

    /* Swipe hint overlay */
    .battle-swipe-hints {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        opacity: 0.3;
        font-size: 12px;
        color: var(--gb-darkest);
        text-align: center;
        width: 200px;
        height: 200px;
        display: none;
    }

    .battle-swipe-hints.show-hints {
        display: block;
    }

    .battle-swipe-hints .hint {
        position: absolute;
    }

    .battle-swipe-hints .hint-up {
        top: 0;
        left: 50%;
        transform: translateX(-50%);
    }

    .battle-swipe-hints .hint-down {
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
    }

    .battle-swipe-hints .hint-left {
        left: 0;
        top: 50%;
        transform: translateY(-50%);
    }

    .battle-swipe-hints .hint-right {
        right: 0;
        top: 50%;
        transform: translateY(-50%);
    }
}

/* Landscape battle layout */
@media (max-width: 932px) and (orientation: landscape) {
    .battle-ui {
        display: grid;
        grid-template-areas:
            "enemy-info battle-area"
            "player-info battle-area"
            "moves moves";
        grid-template-columns: 200px 1fr;
        grid-template-rows: auto auto 1fr;
    }

    .enemy-info {
        grid-area: enemy-info;
        position: relative;
        top: auto;
        left: auto;
        margin: 8px;
    }

    .player-info {
        grid-area: player-info;
        position: relative;
        bottom: auto;
        right: auto;
        margin: 8px;
    }

    .move-menu {
        grid-area: moves;
        bottom: 8px;
        left: 8px;
        right: 8px;
        display: flex;
        gap: 8px;
    }

    .move-option {
        flex: 1;
        min-height: 60px;
    }
}

/* Quick action bar for battles */
.battle-quick-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--gb-darkest);
    display: flex;
    gap: 4px;
    padding: 8px;
    padding-bottom: max(8px, env(safe-area-inset-bottom));
    z-index: 200;
    opacity: 0;
    transform: translateY(100%);
    transition: opacity 0.3s, transform 0.3s;
}

.battle-quick-actions.active {
    opacity: 1;
    transform: translateY(0);
}

.battle-quick-actions button {
    flex: 1;
    background: var(--gb-light);
    border: none;
    color: var(--gb-darkest);
    padding: 12px;
    border-radius: 8px;
    font-size: 20px;
    min-height: 56px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    touch-action: manipulation;
    transition: transform 0.1s;
}

.battle-quick-actions button:active {
    transform: scale(0.9);
}

.battle-quick-actions button .action-label {
    font-size: 10px;
    margin-top: 4px;
}

/* Type effectiveness indicators */
.type-effectiveness {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 36px;
    font-weight: bold;
    pointer-events: none;
    z-index: 1000;
    animation: effectiveness-pop 0.6s ease-out;
}

.type-effectiveness.super-effective {
    color: #4caf50;
}

.type-effectiveness.not-very-effective {
    color: #f44336;
}

.type-effectiveness.no-effect {
    color: #666;
}

@keyframes effectiveness-pop {
    0% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.5);
    }
    50% {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.2);
    }
    100% {
        opacity: 0;
        transform: translate(-50%, -70%) scale(1);
    }
}

/* Battle animations for mobile */
.battle-sprite {
    transition: transform 0.3s, filter 0.3s;
}

.battle-sprite.attacking {
    animation: attack-pulse 0.5s ease-out;
}

.battle-sprite.damaged {
    animation: damage-shake 0.5s ease-out;
}

@keyframes attack-pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.15);
    }
}

@keyframes damage-shake {
    0%, 100% {
        transform: translateX(0);
    }
    25% {
        transform: translateX(-8px);
    }
    75% {
        transform: translateX(8px);
    }
}

/* Status effect indicators */
.status-effect {
    position: absolute;
    top: 4px;
    left: 4px;
    background: var(--gb-darkest);
    color: var(--gb-lightest);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
}

.status-effect.poison {
    background: #9c27b0;
}

.status-effect.burn {
    background: #ff5722;
}

.status-effect.freeze {
    background: #2196f3;
}

.status-effect.sleep {
    background: #607d8b;
}

.status-effect.paralysis {
    background: #ffc107;
}
```

---

### 2.4 Battle Quick Actions Bar

```javascript
class BattleQuickActions {
    constructor(battleSystem) {
        this.battle = battleSystem;
        this.createUI();
    }

    createUI() {
        const quickActions = document.createElement('div');
        quickActions.className = 'battle-quick-actions';
        quickActions.id = 'battleQuickActions';
        quickActions.innerHTML = `
            <button id="quickAttack" aria-label="Quick attack with first move">
                <span>⚔</span>
                <span class="action-label">Attack</span>
            </button>
            <button id="quickSwitch" aria-label="Switch creature">
                <span>👥</span>
                <span class="action-label">Switch</span>
            </button>
            <button id="quickItem" aria-label="Use item">
                <span>🎒</span>
                <span class="action-label">Item</span>
            </button>
            <button id="quickRun" aria-label="Run from battle">
                <span>🏃</span>
                <span class="action-label">Run</span>
            </button>
        `;

        document.body.appendChild(quickActions);

        // Event listeners
        document.getElementById('quickAttack').addEventListener('click', () => {
            this.quickAttack();
        });

        document.getElementById('quickSwitch').addEventListener('click', () => {
            this.quickSwitch();
        });

        document.getElementById('quickItem').addEventListener('click', () => {
            this.quickItem();
        });

        document.getElementById('quickRun').addEventListener('click', () => {
            this.quickRun();
        });
    }

    show() {
        document.getElementById('battleQuickActions').classList.add('active');
    }

    hide() {
        document.getElementById('battleQuickActions').classList.remove('active');
    }

    quickAttack() {
        // Use first available move
        if (this.battle.isPlayerTurn) {
            this.battle.selectMove(0);
            if (navigator.vibrate) navigator.vibrate(20);
        }
    }

    quickSwitch() {
        // Open creature switch menu
        this.battle.showSwitchMenu();
        if (navigator.vibrate) navigator.vibrate(20);
    }

    quickItem() {
        // Open item menu
        this.battle.showItemMenu();
        if (navigator.vibrate) navigator.vibrate(20);
    }

    quickRun() {
        // Attempt to run
        if (this.battle.type === 'wild') {
            this.battle.attemptRun();
            if (navigator.vibrate) navigator.vibrate([20, 50, 20]);
        } else {
            this.battle.game.announceToScreenReader("Can't run from trainer battles!");
            if (navigator.vibrate) navigator.vibrate([50, 100]);
        }
    }
}
```

---

### 2.5 Battle System Integration

```javascript
// In GameEngine class, integrate battle enhancements
class GameEngine {
    startBattle(battleConfig) {
        // ... existing battle setup ...

        // Add gesture controller for mobile
        if ('ontouchstart' in window) {
            this.battleGestureController = new BattleGestureController(this);
            this.battleGestureController.enable();
        }

        // Add quick actions bar for mobile
        if (window.innerWidth <= 768) {
            this.battleQuickActions = new BattleQuickActions(this);
            this.battleQuickActions.show();
        }

        // Show swipe hints for first-time users
        if (!localStorage.getItem('wowmon_swipe_hints_shown')) {
            this.showSwipeHints();
            localStorage.setItem('wowmon_swipe_hints_shown', 'true');
        }
    }

    endBattle() {
        // ... existing battle end logic ...

        // Cleanup mobile battle enhancements
        if (this.battleGestureController) {
            this.battleGestureController.disable();
        }

        if (this.battleQuickActions) {
            this.battleQuickActions.hide();
        }
    }

    showSwipeHints() {
        const hints = document.createElement('div');
        hints.className = 'battle-swipe-hints show-hints';
        hints.innerHTML = `
            <div class="hint hint-up">↑ Move 1</div>
            <div class="hint hint-right">→ Move 2</div>
            <div class="hint hint-down">↓ Move 3</div>
            <div class="hint hint-left">← Move 4</div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold;">
                Swipe to Attack!
            </div>
        `;

        const battleUI = document.getElementById('battleUI');
        battleUI.appendChild(hints);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            hints.classList.remove('show-hints');
            setTimeout(() => hints.remove(), 300);
        }, 5000);
    }
}
```

---

## 3. MOBILE-SPECIFIC FEATURES & ENHANCEMENTS

### Overview
Additional mobile optimizations focusing on offline play, performance, bandwidth, and mobile-specific UX patterns.

---

### 3.1 Offline Mode & Progressive Web App (PWA)

```javascript
// Service Worker for offline support
// File: wowmon-sw.js (to be embedded inline in HTML)

const CACHE_NAME = 'wowmon-v1';
const ASSETS_TO_CACHE = [
    // Since everything is inline, just cache the main HTML
    './wowMon.html',
    // Add any external assets if needed
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
```

```javascript
// PWA initialization in main game code
class PWAManager {
    constructor() {
        this.init();
    }

    init() {
        if ('serviceWorker' in navigator) {
            this.registerServiceWorker();
        }

        this.handleInstallPrompt();
        this.checkOnlineStatus();
    }

    registerServiceWorker() {
        // Since everything is inline, embed service worker as blob
        const swCode = `
            ${/* Service worker code here */}
        `;

        const blob = new Blob([swCode], { type: 'application/javascript' });
        const swURL = URL.createObjectURL(blob);

        navigator.serviceWorker.register(swURL)
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }

    handleInstallPrompt() {
        let deferredPrompt;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;

            // Show install button/banner
            this.showInstallPrompt(deferredPrompt);
        });
    }

    showInstallPrompt(prompt) {
        // Create install banner
        const banner = document.createElement('div');
        banner.id = 'installBanner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--gb-darkest);
            color: var(--gb-lightest);
            padding: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 10000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        `;

        banner.innerHTML = `
            <span>📱 Install WoWmon for offline play!</span>
            <div>
                <button id="installBtn" style="background: var(--gb-light); border: none; padding: 8px 16px; border-radius: 4px; margin-right: 8px; font-family: monospace;">Install</button>
                <button id="dismissInstall" style="background: transparent; border: 2px solid var(--gb-lightest); color: var(--gb-lightest); padding: 8px 16px; border-radius: 4px; font-family: monospace;">Later</button>
            </div>
        `;

        document.body.appendChild(banner);

        document.getElementById('installBtn').addEventListener('click', async () => {
            banner.remove();
            prompt.prompt();
            const { outcome } = await prompt.userChoice;
            console.log('Install outcome:', outcome);
        });

        document.getElementById('dismissInstall').addEventListener('click', () => {
            banner.remove();
        });
    }

    checkOnlineStatus() {
        const updateOnlineStatus = () => {
            const status = navigator.onLine ? 'online' : 'offline';
            document.body.classList.toggle('offline-mode', !navigator.onLine);

            if (!navigator.onLine) {
                this.showOfflineBanner();
            } else {
                this.hideOfflineBanner();
            }
        };

        window.addEventListener('online', updateOnlineStatus);
        window.addEventListener('offline', updateOnlineStatus);
        updateOnlineStatus();
    }

    showOfflineBanner() {
        if (document.getElementById('offlineBanner')) return;

        const banner = document.createElement('div');
        banner.id = 'offlineBanner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff9800;
            color: #000;
            padding: 8px;
            text-align: center;
            z-index: 9999;
            font-size: 14px;
            font-weight: bold;
        `;
        banner.textContent = '📡 Offline Mode - Playing from cache';

        document.body.appendChild(banner);
    }

    hideOfflineBanner() {
        const banner = document.getElementById('offlineBanner');
        if (banner) banner.remove();
    }
}
```

---

### 3.2 Performance Optimizations for Mobile

```javascript
class MobilePerformanceOptimizer {
    constructor(game) {
        this.game = game;
        this.isLowPowerMode = false;
        this.init();
    }

    init() {
        this.detectLowPowerMode();
        this.optimizeCanvasRendering();
        this.implementLazyLoading();
        this.reduceBatteryDrain();
    }

    detectLowPowerMode() {
        // Check battery status
        if ('getBattery' in navigator) {
            navigator.getBattery().then((battery) => {
                this.updatePowerMode(battery);

                battery.addEventListener('levelchange', () => {
                    this.updatePowerMode(battery);
                });

                battery.addEventListener('chargingchange', () => {
                    this.updatePowerMode(battery);
                });
            });
        }
    }

    updatePowerMode(battery) {
        // Enable low power mode if battery < 20% and not charging
        this.isLowPowerMode = battery.level < 0.2 && !battery.charging;

        if (this.isLowPowerMode) {
            this.enableLowPowerMode();
        } else {
            this.disableLowPowerMode();
        }
    }

    enableLowPowerMode() {
        // Reduce frame rate
        this.game.targetFPS = 30;

        // Disable animations
        document.body.classList.add('low-power-mode');

        // Reduce particle effects
        this.game.particleLimit = 10;

        // Show notification
        this.game.showText('Low power mode enabled');
    }

    disableLowPowerMode() {
        this.game.targetFPS = 60;
        document.body.classList.remove('low-power-mode');
        this.game.particleLimit = 50;
    }

    optimizeCanvasRendering() {
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // Use lower resolution on mobile
        if (window.innerWidth <= 768) {
            canvas.width = 160;
            canvas.height = 144;
        }

        // Disable image smoothing for pixelated graphics
        ctx.imageSmoothingEnabled = false;
        ctx.mozImageSmoothingEnabled = false;
        ctx.webkitImageSmoothingEnabled = false;
        ctx.msImageSmoothingEnabled = false;

        // Use hardware acceleration hints
        canvas.style.willChange = 'transform';
    }

    implementLazyLoading() {
        // Only load creature sprites when needed
        this.game.spriteCache = new Map();
        this.game.maxCachedSprites = 20;
    }

    reduceBatteryDrain() {
        // Pause game when tab is hidden
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.game.pause();
            } else {
                this.game.resume();
            }
        });

        // Reduce audio quality on mobile
        if (this.game.audio && window.innerWidth <= 768) {
            this.game.audio.settings.masterVolume *= 0.7;
        }
    }
}

// CSS for low power mode
const lowPowerModeCSS = `
body.low-power-mode * {
    animation-duration: 0s !important;
    transition-duration: 0s !important;
}

body.low-power-mode .particle-effect {
    display: none;
}
`;
```

---

### 3.3 Mobile-Specific UI Patterns

```javascript
class MobileUIEnhancements {
    constructor(game) {
        this.game = game;
        this.init();
    }

    init() {
        this.implementPullToRefresh();
        this.addSwipeNavigation();
        this.improveKeyboardHandling();
        this.addQuickAccessMenu();
    }

    implementPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let isPulling = false;

        const gameContainer = document.querySelector('.game-container');

        gameContainer.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
            }
        });

        gameContainer.addEventListener('touchmove', (e) => {
            if (window.scrollY === 0) {
                currentY = e.touches[0].clientY;
                const pullDistance = currentY - startY;

                if (pullDistance > 0 && pullDistance < 100) {
                    isPulling = true;
                    // Show pull indicator
                    this.showPullIndicator(pullDistance);
                }
            }
        });

        gameContainer.addEventListener('touchend', () => {
            if (isPulling && (currentY - startY) > 80) {
                this.refreshGame();
            }
            this.hidePullIndicator();
            isPulling = false;
        });
    }

    showPullIndicator(distance) {
        let indicator = document.getElementById('pullIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'pullIndicator';
            indicator.style.cssText = `
                position: fixed;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                background: var(--gb-darkest);
                color: var(--gb-lightest);
                padding: 8px 16px;
                border-radius: 0 0 8px 8px;
                font-size: 12px;
                z-index: 10000;
                transition: transform 0.2s;
            `;
            indicator.textContent = '↓ Pull to refresh';
            document.body.appendChild(indicator);
        }

        indicator.style.transform = `translateX(-50%) translateY(${Math.min(distance, 80)}px)`;

        if (distance > 80) {
            indicator.textContent = '↻ Release to refresh';
        } else {
            indicator.textContent = '↓ Pull to refresh';
        }
    }

    hidePullIndicator() {
        const indicator = document.getElementById('pullIndicator');
        if (indicator) {
            indicator.style.transform = 'translateX(-50%) translateY(-100%)';
            setTimeout(() => indicator.remove(), 300);
        }
    }

    refreshGame() {
        // Sync game state
        this.game.saveGame();

        // Show refresh animation
        if (navigator.vibrate) navigator.vibrate([20, 50, 20]);

        // Reload certain elements
        this.game.announceToScreenReader('Game refreshed');
    }

    addSwipeNavigation() {
        // Swipe left/right on main screen to quickly access features
        const gameScreen = document.querySelector('.game-screen');
        const gestureHandler = new TouchGestureHandler(gameScreen);

        gameScreen.addEventListener('gesture-swipe', (e) => {
            if (this.game.currentState === 'overworld') {
                switch(e.detail.direction) {
                    case 'up':
                        // Quick access to team builder
                        if (this.game.teamBuilder) {
                            this.game.teamBuilder.open();
                        }
                        break;
                    case 'down':
                        // Quick access to bag
                        this.game.openBag();
                        break;
                }
            }
        });
    }

    improveKeyboardHandling() {
        // Handle on-screen keyboard appearing
        if ('visualViewport' in window) {
            window.visualViewport.addEventListener('resize', () => {
                const viewportHeight = window.visualViewport.height;
                const windowHeight = window.innerHeight;

                if (viewportHeight < windowHeight) {
                    // Keyboard is showing
                    document.body.classList.add('keyboard-visible');
                } else {
                    document.body.classList.remove('keyboard-visible');
                }
            });
        }
    }

    addQuickAccessMenu() {
        // Floating action button for quick access
        const fab = document.createElement('button');
        fab.id = 'mobileFAB';
        fab.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--gb-darkest);
            color: var(--gb-lightest);
            border: none;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            z-index: 9000;
            display: none;
            touch-action: manipulation;
            transition: transform 0.2s;
        `;
        fab.textContent = '⚡';
        fab.setAttribute('aria-label', 'Quick actions menu');

        document.body.appendChild(fab);

        // Show on mobile only
        if (window.innerWidth <= 768) {
            fab.style.display = 'block';
        }

        fab.addEventListener('click', () => {
            this.showQuickActionsMenu();
            if (navigator.vibrate) navigator.vibrate(20);
        });

        fab.addEventListener('touchstart', () => {
            fab.style.transform = 'scale(0.9)';
        });

        fab.addEventListener('touchend', () => {
            fab.style.transform = 'scale(1)';
        });
    }

    showQuickActionsMenu() {
        const menu = document.createElement('div');
        menu.className = 'quick-actions-modal';
        menu.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content">
                <h3>Quick Actions</h3>
                <button class="quick-action-item" data-action="team">
                    <span>👥</span> Team Builder
                </button>
                <button class="quick-action-item" data-action="pokedex">
                    <span>📖</span> Pokedex
                </button>
                <button class="quick-action-item" data-action="map">
                    <span>🗺</span> Map
                </button>
                <button class="quick-action-item" data-action="settings">
                    <span>⚙</span> Settings
                </button>
                <button class="quick-action-item" data-action="save">
                    <span>💾</span> Save Game
                </button>
                <button class="quick-action-item" data-action="cancel">
                    <span>✕</span> Close
                </button>
            </div>
        `;

        document.body.appendChild(menu);

        // Animate in
        requestAnimationFrame(() => {
            menu.classList.add('active');
        });

        // Handle actions
        menu.querySelectorAll('.quick-action-item').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleQuickAction(action);
                menu.remove();
            });
        });

        // Close on backdrop click
        menu.querySelector('.modal-backdrop').addEventListener('click', () => {
            menu.remove();
        });
    }

    handleQuickAction(action) {
        switch(action) {
            case 'team':
                this.game.teamBuilder.open();
                break;
            case 'pokedex':
                this.game.openPokedex();
                break;
            case 'map':
                this.game.showMap();
                break;
            case 'settings':
                this.game.toggleAccessibilityPanel();
                break;
            case 'save':
                this.game.saveGame();
                this.game.showText('Game saved!');
                break;
        }
    }
}

// Additional CSS for mobile UI enhancements
const mobileUICSS = `
/* Quick Actions Modal */
.quick-actions-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10000;
    display: flex;
    align-items: flex-end;
    opacity: 0;
    transition: opacity 0.3s;
}

.quick-actions-modal.active {
    opacity: 1;
}

.quick-actions-modal .modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
}

.quick-actions-modal .modal-content {
    position: relative;
    background: var(--gb-lightest);
    border-radius: 16px 16px 0 0;
    padding: 20px;
    padding-bottom: max(20px, env(safe-area-inset-bottom));
    width: 100%;
    transform: translateY(100%);
    transition: transform 0.3s;
}

.quick-actions-modal.active .modal-content {
    transform: translateY(0);
}

.quick-actions-modal h3 {
    font-size: 18px;
    margin-bottom: 16px;
    color: var(--gb-darkest);
}

.quick-action-item {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    background: var(--gb-light);
    border: 2px solid var(--gb-darkest);
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 8px;
    font-size: 16px;
    font-family: monospace;
    color: var(--gb-darkest);
    text-align: left;
    touch-action: manipulation;
    transition: transform 0.1s;
}

.quick-action-item:active {
    transform: scale(0.98);
}

.quick-action-item span:first-child {
    font-size: 24px;
}

/* Keyboard visible adjustments */
body.keyboard-visible .game-container {
    padding-bottom: 0;
}

body.keyboard-visible #mobileFAB {
    bottom: 20px;
}

/* Floating Action Button pulse animation */
@keyframes fab-pulse {
    0%, 100% {
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    50% {
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
}

#mobileFAB:not(:active) {
    animation: fab-pulse 2s infinite;
}
`;
```

---

### 3.4 Mobile Data Persistence & Sync

```javascript
class MobileDataManager {
    constructor(game) {
        this.game = game;
        this.autoSaveInterval = 60000; // 1 minute
        this.lastSaveTime = Date.now();
        this.init();
    }

    init() {
        this.setupAutoSave();
        this.implementCloudSync();
        this.handleAppLifecycle();
    }

    setupAutoSave() {
        // Auto-save on mobile to prevent data loss
        setInterval(() => {
            this.autoSave();
        }, this.autoSaveInterval);
    }

    autoSave() {
        if (this.game.currentState !== 'battle') {
            this.game.saveGame();
            this.lastSaveTime = Date.now();

            // Show subtle notification
            this.showSaveIndicator();
        }
    }

    showSaveIndicator() {
        let indicator = document.getElementById('saveIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'saveIndicator';
            indicator.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--gb-darkest);
                color: var(--gb-lightest);
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s;
            `;
            indicator.textContent = '💾 Saved';
            document.body.appendChild(indicator);
        }

        indicator.style.opacity = '1';
        setTimeout(() => {
            indicator.style.opacity = '0';
        }, 2000);
    }

    implementCloudSync() {
        // Simple cloud sync using localStorage + future backend
        // For now, just ensure data is backed up to localStorage

        window.addEventListener('beforeunload', () => {
            // Force save before leaving
            this.game.saveGame();
        });
    }

    handleAppLifecycle() {
        // Handle app going to background (mobile browsers)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // App going to background - save immediately
                this.game.saveGame();
                console.log('App backgrounded - game saved');
            } else {
                // App returning to foreground
                console.log('App foregrounded');
                this.checkForUpdates();
            }
        });

        // Handle page unload (closing tab/app)
        window.addEventListener('pagehide', () => {
            this.game.saveGame();
        });
    }

    checkForUpdates() {
        // Check if there's a newer version of the game
        const currentVersion = '1.0.0';
        const storedVersion = localStorage.getItem('wowmon_version');

        if (storedVersion && storedVersion !== currentVersion) {
            this.showUpdateNotification();
        }

        localStorage.setItem('wowmon_version', currentVersion);
    }

    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--gb-lightest);
            border: 4px solid var(--gb-darkest);
            padding: 20px;
            border-radius: 8px;
            z-index: 10000;
            text-align: center;
            max-width: 300px;
        `;

        notification.innerHTML = `
            <h3 style="margin-bottom: 12px;">Update Available!</h3>
            <p style="margin-bottom: 16px;">A new version of WoWmon is available.</p>
            <button onclick="location.reload()" style="background: var(--gb-darkest); color: var(--gb-lightest); border: none; padding: 12px 24px; border-radius: 4px; font-family: monospace; font-size: 14px;">Reload Now</button>
        `;

        document.body.appendChild(notification);
    }

    exportSaveToClipboard() {
        const saveData = this.game.exportSave();

        if (navigator.clipboard) {
            navigator.clipboard.writeText(saveData).then(() => {
                this.game.showText('Save data copied to clipboard!');
                if (navigator.vibrate) navigator.vibrate(20);
            });
        }
    }

    importSaveFromClipboard() {
        if (navigator.clipboard) {
            navigator.clipboard.readText().then(text => {
                try {
                    const saveData = JSON.parse(text);
                    this.game.importSave(saveData);
                    this.game.showText('Save data imported!');
                    if (navigator.vibrate) navigator.vibrate([20, 50, 20]);
                } catch (e) {
                    this.game.showText('Invalid save data!');
                    if (navigator.vibrate) navigator.vibrate([50, 100]);
                }
            });
        }
    }
}
```

---

## 4. IMPLEMENTATION SUMMARY & INTEGRATION GUIDE

### 4.1 Feature Priority (Mobile-First)

**Phase 1 - Essential Mobile Features (Week 1)**
1. Touch gesture system (TouchGestureHandler class)
2. Team Builder UI with drag-and-drop
3. Basic battle gestures (swipe to attack)
4. Mobile-optimized CSS (responsive breakpoints)

**Phase 2 - Enhanced Battle System (Week 2)**
5. Battle quick actions bar
6. Swipe indicators and hints
7. Type effectiveness animations
8. Creature switching during battle

**Phase 3 - Performance & Polish (Week 3)**
9. PWA support and offline mode
10. Performance optimizations
11. Auto-save and data persistence
12. Quick actions menu (FAB)

### 4.2 Code Integration Points

Add to existing wowMon.html structure:

```javascript
// At the end of existing GameEngine class
class GameEngine {
    constructor() {
        // ... existing code ...

        // Add mobile-first features
        this.initMobileFeatures();
    }

    initMobileFeatures() {
        // Check if mobile
        this.isMobile = /Android|webOS|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
                        window.innerWidth <= 768;

        if (this.isMobile || 'ontouchstart' in window) {
            // Initialize mobile features
            this.teamBuilder = new TeamBuilder(this);
            this.mobileUI = new MobileUIEnhancements(this);
            this.performanceOptimizer = new MobilePerformanceOptimizer(this);
            this.dataManager = new MobileDataManager(this);
            this.pwaManager = new PWAManager();

            // Add mobile-specific event listeners
            this.setupMobileControls();
        }
    }

    setupMobileControls() {
        // Add touch event handlers to existing buttons
        document.querySelectorAll('.btn, .dpad-btn, .menu-option').forEach(btn => {
            btn.addEventListener('touchstart', () => {
                btn.classList.add('touch-active');
                if (navigator.vibrate) navigator.vibrate(10);
            });

            btn.addEventListener('touchend', () => {
                btn.classList.remove('touch-active');
            });
        });
    }
}
```

### 4.3 CSS Addition Summary

Add these CSS blocks to the `<style>` section:

1. Team Builder styles (section 1.3)
2. Battle gesture enhancements (section 2.3)
3. Mobile UI patterns (section 3.3)
4. Quick actions modal (section 3.3)
5. Low power mode styles (section 3.2)

### 4.4 HTML Additions

Add these elements to the `<body>`:

```html
<!-- Team Builder (dynamically created by JS) -->

<!-- Battle Gesture Zone (dynamically created by JS) -->

<!-- Mobile FAB Button (dynamically created by JS) -->

<!-- PWA Install Banner (dynamically created by JS) -->

<!-- Offline Mode Banner (dynamically created by JS) -->
```

### 4.5 Performance Metrics (Mobile Target)

**Target Performance on Mid-Range Mobile (2023)**
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Frame Rate: 60 FPS (30 FPS in low power mode)
- Memory Usage: < 100MB
- Bundle Size: N/A (single HTML file, currently ~200KB)

**Touch Response Times**
- Tap feedback: < 100ms
- Gesture recognition: < 150ms
- Battle move execution: < 200ms
- UI transitions: < 300ms

### 4.6 Mobile-Specific Testing Checklist

**Devices to Test**
- [ ] iPhone SE (small screen, 375px width)
- [ ] iPhone 14 Pro (notch, safe areas)
- [ ] Samsung Galaxy S21 (Android)
- [ ] iPad Mini (tablet portrait)
- [ ] iPad Pro (tablet landscape)

**Orientation Testing**
- [ ] Portrait mode - all features functional
- [ ] Landscape mode - layouts adjust properly
- [ ] Rotation transitions smooth

**Touch Testing**
- [ ] All buttons have 48px+ touch targets
- [ ] Swipe gestures work consistently
- [ ] Drag-and-drop feels responsive
- [ ] Long-press actions trigger correctly
- [ ] No accidental double-taps

**Performance Testing**
- [ ] 60 FPS during normal gameplay
- [ ] No dropped frames during battles
- [ ] Smooth scrolling in team builder
- [ ] Quick app resume from background
- [ ] Low battery mode reduces power usage

**Offline Testing**
- [ ] Game works completely offline
- [ ] Save/load functions without network
- [ ] PWA install prompt appears
- [ ] Offline indicator shows when disconnected

---

## 5. MOBILE-SPECIFIC EDGE CASES & SOLUTIONS

### 5.1 On-Screen Keyboard Issues

**Problem:** Keyboard covers game UI
**Solution:**
```javascript
// Adjust viewport when keyboard appears
if ('visualViewport' in window) {
    window.visualViewport.addEventListener('resize', () => {
        const offset = window.innerHeight - window.visualViewport.height;
        document.querySelector('.game-container').style.paddingBottom = offset + 'px';
    });
}
```

### 5.2 Notched Displays (iPhone X+)

**Problem:** Content hidden behind notch/camera cutout
**Solution:** Already implemented with `env(safe-area-inset-*)` in CSS

### 5.3 Accidental Touch Rejection

**Problem:** Palm rejection during gameplay
**Solution:**
```javascript
// Ignore touches outside main game area during battles
canvas.addEventListener('touchstart', (e) => {
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();

    // Only process touches within canvas
    if (touch.clientX >= rect.left && touch.clientX <= rect.right &&
        touch.clientY >= rect.top && touch.clientY <= rect.bottom) {
        // Process touch
    } else {
        e.preventDefault();
    }
});
```

### 5.4 Battery Drain During Long Sessions

**Problem:** Extended gameplay drains battery quickly
**Solution:** Implemented in MobilePerformanceOptimizer with:
- Reduced frame rate when battery low
- Audio volume reduction
- Particle effect limits
- Pause when tab hidden

### 5.5 Save Data Loss on App Kill

**Problem:** iOS/Android can kill app without warning
**Solution:** Implemented in MobileDataManager with:
- Auto-save every 60 seconds
- Save on visibility change
- Save on page unload/hide events
- localStorage persistence

---

## 6. ACCESSIBILITY ON MOBILE

### 6.1 Screen Reader Support

All mobile features include ARIA labels and announcements:
- Team builder actions announced
- Battle move selections announced
- Gesture hints for screen reader users
- Alternative button controls always available

### 6.2 Large Text Mode

Respects system text size settings:
```css
@media (prefers-reduced-motion: reduce) {
    /* Reduce animations */
}

body.large-text {
    font-size: 120%;
}
```

### 6.3 Touch Target Sizes

All interactive elements meet WCAG 2.1 Level AAA:
- Minimum 44x44px (iOS guideline)
- Recommended 48x48px (Material Design)
- Actual implementation: 56-64px for primary actions

---

## 7. FUTURE MOBILE ENHANCEMENTS (Post-MVP)

### 7.1 Multiplayer Trading (Local)
- Bluetooth LE for nearby device trading
- QR code creature sharing
- WebRTC peer-to-peer battles

### 7.2 Augmented Reality (AR)
- Web AR for creature catching in real world
- Camera-based wild encounters
- Location-based gym battles

### 7.3 Push Notifications (PWA)
- Daily creature catch reminders
- Event notifications
- Battle challenge alerts

### 7.4 Social Features
- Screenshot sharing
- Team composition sharing via URL
- Battle replay videos

---

## CONCLUSION

This mobile-first design document provides comprehensive specifications for implementing:

1. **Team Builder System** - Fully touch-optimized with drag-and-drop, swipe actions, and large tap targets
2. **Battle System Enhancements** - Gesture-based combat with swipe-to-attack and quick action buttons
3. **Mobile-Specific Features** - PWA support, offline mode, performance optimizations, and battery management

All features prioritize mobile experience first, with progressive enhancement for desktop users. The design adheres to mobile best practices including:
- Touch targets ≥ 48px
- Safe area insets for notched devices
- Portrait and landscape support
- Haptic feedback for all interactions
- Offline-first architecture
- Battery-conscious performance optimization

**Implementation can be done in 3 phases over 3 weeks**, with each phase building on the previous while maintaining backward compatibility with the existing Game Boy-style wowMon.html game.

---

**File Location:** `/Users/kodyw/Documents/GitHub/localFirstTools3/WOWMON_MOBILE_FIRST_DESIGN.md`
**Total Features:** 15+ mobile-specific enhancements
**Code Snippets:** 20+ ready-to-integrate examples
**CSS Additions:** 800+ lines of mobile-optimized styles
**JavaScript Classes:** 8 new mobile-first classes
