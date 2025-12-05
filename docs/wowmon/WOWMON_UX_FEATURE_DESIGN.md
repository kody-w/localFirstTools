# WoWmon UX-Centric Feature Design
## Agent 2: User Experience & Interface Design Strategy

**Document Version:** 2.0  
**Date:** 2025-10-12  
**Focus:** Team Builder, Battle System, and Quality-of-Life Features  
**Design Philosophy:** Intuitive interactions, Game Boy aesthetic, minimal cognitive load, delightful feedback

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current System Analysis](#current-system-analysis)
3. [Feature 1: Team Builder System](#feature-1-team-builder-system)
4. [Feature 2: Enhanced Battle System](#feature-2-enhanced-battle-system)
5. [Feature 3: Quality-of-Life Features](#feature-3-quality-of-life-features)
6. [Design System](#design-system)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

This document presents a comprehensive UX-focused design for three core WoWmon features:

### 1. Team Builder System
A complete creature management interface allowing players to:
- View and organize teams of 6 WoWmon
- Switch creatures during battles strategically
- Store excess creatures in PC boxes (30 creatures per box, 8 boxes)
- Quick-access team overview via SELECT button
- Compare creatures side-by-side

### 2. Enhanced Battle System
Improvements focusing on clarity and strategic depth:
- Visual type effectiveness indicators (▲▼)
- Enhanced move selection with power/accuracy display
- HP hearts system (more intuitive than bars)
- Damage number animations
- Turn order preview
- Improved catch mechanics UI

### 3. Quality-of-Life Features
Player-requested conveniences:
- Quick heal system (hold B button)
- Type chart quick reference
- Creature comparison tool
- Nickname system
- Adventure journal/log
- Auto-battle mode for grinding
- Battle speed options

**Design Constraints:**
- Game Boy Color aesthetic (320x288px screen)
- 4-button input (D-Pad, A, B, START, SELECT)
- Touch-friendly for mobile (48px minimum targets)
- Accessible (keyboard nav, screen reader, high contrast)

---

## Current System Analysis

### Existing Architecture

**File:** `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html`

**Game States:**
```javascript
'LOADING'   // Initial cartridge load
'OVERWORLD' // Exploration mode
'BATTLE'    // Turn-based combat
'MENU'      // Main menu (START button)
'TEXT'      // Dialog/messages
```

**Player Data Structure:**
```javascript
player: {
  name: 'PLAYER',
  x: 10, y: 10,
  facing: 'down',
  creatures: [],        // ❌ Currently unlimited, no organization
  bag: {                // Items inventory
    'health_potion': 5,
    'soul_stone': 10
  },
  money: 3000,
  badges: [],
  stats: {              // Tracking
    battlesWon: 0,
    creaturesCaught: 0,
    uniqueCreaturesCaught: [],
    evolutions: 0,
    // ... more stats
  },
  achievements: {},
  journal: { entries: [], discoveries: [] }
}
```

**Battle System:**
```javascript
battle: {
  type: 'wild',        // or 'trainer'
  playerCreature: {},
  enemyCreature: {},
  // Menu options: FIGHT, CREATURES (not implemented), RUN
}
```

### UX Pain Points Identified

#### Critical Issues
1. **No Team Management** - `creatures[]` array has no organization
   - Cannot view all captured creatures
   - No way to switch active creature
   - "CREATURES" button in battle shows "Not implemented yet!"

2. **Limited Battle Information**
   - No type effectiveness preview
   - Move power/accuracy hidden until attack
   - No indication of turn order (who attacks first)

3. **Poor Battle Visibility**
   - HP bars are small (4px height)
   - No numeric HP display for enemy
   - Status effects lack visual indicators

#### Secondary Issues
4. No quick-access menus (all requires START → navigate)
5. No creature comparison tools
6. No storage for excess creatures (unlimited array)
7. No nickname/customization system

---

## Feature 1: Team Builder System

### Design Philosophy

**Core Principles:**
- **Progressive Disclosure** - Show essentials first, details on demand
- **Visual Hierarchy** - Lead creature prominent, others supporting
- **Instant Feedback** - Every action has visual/audio response
- **Touch-Friendly** - 48px minimum touch targets on mobile
- **Consistent Navigation** - Same D-Pad patterns across all screens

---

### 1.1 Quick Team View (SELECT Button)

**Access Method:** Press SELECT button anywhere in overworld

**Purpose:** Rapid status check without interrupting gameplay

**Layout (320x288px Game Boy screen):**
```
┌─────────────────────────────────────────┐
│ TEAM                            1/6  HP │ ← Header
├─────────────────────────────────────────┤
│                                         │
│        [WHELP Sprite 48x48]             │ ← Lead creature (large)
│                                         │
│     WHELP           Lv.12      ♥♥♥      │ ← Name  Level  HP hearts
│     [Dragon][Fire]                      │ ← Type badges (colored)
│     HP: 45/52      EXP: 389/500         │ ← Numeric stats
│                                         │
├─────────────────────────────────────────┤
│ [24×24] [24×24] [24×24]                 │ ← Party slots 2-4
│ SPRITE  GHOUL   WHELP                   │    (clickable)
│ Lv.8♥♥♡ Lv.10♥♥♥ Lv.7♥♡♡                │
│                                         │
│ [24×24] [24×24] [EMPTY]                 │ ← Party slots 5-6
│ DRAKE   PHOENIX  +ADD                   │
│ Lv.5♥♥  Lv.9♥♥♥  [····]                 │
│                                         │
├─────────────────────────────────────────┤
│ ◄► SELECT  A:INFO  B:CLOSE  START:MANAGE│ ← Controls hint
└─────────────────────────────────────────┘
```

**Interaction Flow:**

1. **Press SELECT** → Screen slides up from bottom (200ms ease-out)
2. **D-Pad Left/Right** → Cycle through team members
   - Sprite scales (current: 1.0 → 1.1, others: 1.0 → 0.9)
   - Smooth 150ms transition
   - SFX: "whoosh" sound
   - Mobile: Haptic pulse (10ms)
3. **D-Pad Up/Down** → Navigate party thumbnails (highlight border)
4. **A Button** → View detailed stats (transitions to Creature Detail View)
5. **B Button** → Close (slide down, return to game)
6. **START Button** → Open full Team Manager

**Visual Feedback Elements:**

**HP Hearts System** (Game Boy authentic):
```
Full HP (80-100%):   ♥♥♥♥♥  (--gb-dark green)
Medium HP (40-79%):  ♥♥♡♡♡  (--gb-light yellow)
Low HP (1-39%):      ♥♡♡♡♡  (red #d04828, pulsing)
Fainted (0%):        ✕✕✕✕✕  (--gb-darkest gray)
```

**Type Badges** (color-coded rounded rectangles):
```css
[Fire]    background: #b85420 (dark orange-red)
[Water]   background: #2860a8 (dark blue)
[Nature]  background: #488830 (dark green)
[Dragon]  background: #6838b8 (dark purple)
[Shadow]  background: #483848 (dark gray-purple)
[Beast]   background: #906030 (brown)
[Spirit]  background: #a0a8c0 (light blue-gray)
```

**Animation Details:**
```css
@keyframes slideInFromBottom {
  0% { transform: translateY(100%); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

.quick-team-view {
  animation: slideInFromBottom 200ms ease-out;
}

/* Smooth sprite swap */
.creature-sprite.selected {
  transform: scale(1.1);
  filter: drop-shadow(0 0 8px var(--gb-highlight));
  transition: all 150ms cubic-bezier(0.68, -0.55, 0.265, 1.55); /* bounce easing */
}
```

---

### 1.2 Full Team Manager (START Menu → CREATURES)

**Access:** START → CREATURES (or START from Quick Team View)

**Purpose:** Comprehensive team organization and management

**Layout:**
```
┌─────────────────────────────────────────┐
│ ◄ TEAM MANAGER                        ►│ ← Header with arrows
├─────────────────────────────────────────┤
│ Active Team (1-6):                      │
│                                         │
│ 1▶[Sprite 32×32] WHELP      Lv.12  ♥♥♥  │ ← Lead (▶ indicator)
│   Dragon/Fire      HP: 45/52            │
│                                         │
│ 2 [Sprite 32×32] SPRITE     Lv.8   ♥♥♡  │
│   Water            HP: 28/35            │
│                                         │
│ 3 [Sprite 32×32] GHOUL      Lv.10  ♥♥♥  │
│   Undead/Shadow    HP: 40/40            │
│                                         │
│ 4 [Empty Slot]              [+ ADD]     │
│                                         │
│ 5 [Empty Slot]              [+ ADD]     │
│                                         │
│ 6 [Empty Slot]              [+ ADD]     │
│                                         │
├─────────────────────────────────────────┤
│ A:SELECT  Y:SWAP  X:STORAGE  B:BACK     │ ← Action hints
└─────────────────────────────────────────┘
```

**Interactions:**

**Swap Creatures (Reorder Team):**
1. Highlight creature → Press Y button
2. Creature icon bounces + "SWAP MODE" indicator
3. D-Pad Up/Down → Select destination slot
4. Press A to confirm → Smooth slide animation (300ms)
5. SFX: "swap_confirm" sound
6. Auto-save to localStorage

**Add Creature from Storage:**
1. Highlight empty slot → Press A
2. Transitions to Box Storage screen
3. Select creature → Returns to team with creature added
4. Celebration animation (sparkles) + SFX

**View Creature Details:**
1. Highlight creature → Press A (if not in swap mode)
2. Transitions to Creature Detail View (slide left transition)

---

### 1.3 Box Storage System (PC)

**Metaphor:** "PC Storage" (familiar to Pokemon players)

**Capacity:** 8 boxes × 30 creatures = 240 total storage

**Access:**
- From Team Manager → Press X button
- From Overworld → Interact with PC object

**Layout:**
```
┌─────────────────────────────────────────┐
│ ◄ BOX 1: GOLDSHIRE                    ►│ ← Box name (editable)
├─────────────────────────────────────────┤
│ [■][■][■][■][■][■]                      │ ← 5×6 grid (30 creatures)
│ [■][■][■][■][■][■]                      │   ■ = filled slot
│ [■][■][■][■][□][□]                      │   □ = empty slot
│ [□][□][□][□][□][□]                      │
│ [□][□][□][□][□][□]                      │
│                                         │
│ Creatures in box: 14/30                 │ ← Counter
│                                         │
├─────────────────────────────────────────┤
│ [Hover Preview]                         │ ← Bottom panel shows
│ WHELP  Lv.12  Dragon/Fire               │   creature on hover
│ HP: 45/52   ATK: 34                     │
│                                         │
├─────────────────────────────────────────┤
│ A:SELECT  Y:MOVE  SELECT:SORT  B:BACK   │
└─────────────────────────────────────────┘
```

**Features:**

**1. Quick Filter/Sort (SELECT button):**
```
SORT BY:
► Level (High→Low)
  Level (Low→High)
  Name (A→Z)
  Type
  Caught Date (Recent)
  Favorite First
```

**2. Move Creature:**
- Select creature → Press Y → "MOVE MODE"
- Navigate to destination (same box, other box, or team)
- Press A to confirm
- Drag-and-drop on touch devices

**3. Box Management:**
- D-Pad Left/Right on header → Switch boxes instantly
- Long-press on box name → Rename box (8 characters)
- Boxes auto-created when needed

**4. Batch Operations:**
- Hold A while navigating → Mark multiple creatures (checkboxes)
- Options: MOVE ALL, RELEASE ALL (with confirmation)

**Visual Enhancements:**
```css
/* Grid slot hover */
.box-slot:hover {
  background: var(--gb-highlight);
  transform: scale(1.1);
  box-shadow: 0 0 8px var(--gb-light);
  cursor: pointer;
}

/* Selected creature */
.box-slot.selected {
  border: 3px solid var(--gb-light);
  animation: bounce 500ms ease-in-out infinite;
}

/* Hover preview panel */
.hover-preview {
  background: var(--gb-lightest);
  border-top: 3px solid var(--gb-darkest);
  padding: 8px;
  animation: slideUp 150ms ease-out;
}
```

**Mobile Optimizations:**
- Grid slots: 48×48px minimum (touch-friendly)
- Long-press for details (no hover state)
- Swipe left/right to change boxes
- Pinch-to-zoom on grid (optional)

---

### 1.4 Creature Detail View

**Access:** Team view → Select creature → Press A

**Purpose:** View all stats, moves, and history for a creature

**Layout:**
```
┌─────────────────────────────────────────┐
│ ◄ WHELP                            INFO │
├─────────────────────────────────────────┤
│                                         │
│         [Large Sprite 64×64]            │ ← Animated (breathing)
│                                         │
│  WHELP              Lv.12  ♂            │ ← Name, Level, Gender
│  [Dragon][Fire]                         │ ← Type badges
│  OT: PLAYER        ID: #00412           │ ← Original Trainer, ID
│                                         │
├─────────────────────────────────────────┤
│  HP:  45/52   [████████░░░]             │ ← Stats with bars
│  ATK: 34      [██████░░░░]              │
│  DEF: 28      [█████░░░░░]              │
│  SPD: 31      [█████░░░░░]              │
│  EXP: 389/500 [███████░░░]              │
│                                         │
├─────────────────────────────────────────┤
│  MOVES:                      PP:        │
│  ► DRAGON BREATH            8/10        │ ← Selected move
│    Dragon | Power:60 | Acc:100%        │    (shows details)
│                                         │
│    TACKLE                  15/15        │
│    BITE                    12/15        │
│    WING ATTACK              5/10        │
│                                         │
├─────────────────────────────────────────┤
│  Evolves at Lv.25 → DRAKE               │ ← Evolution info
│                                         │
│  "A young dragon still learning to      │ ← Pokedex entry
│   control its power."                   │
│                                         │
├─────────────────────────────────────────┤
│  Caught: Day 3, Goldshire Forest        │ ← Capture info
│  Battles Won: 8   Friendship: ♥♥♥♥♡     │
│                                         │
├─────────────────────────────────────────┤
│ ↑↓:SCROLL  A:MOVES  START:RENAME  B:BACK│
└─────────────────────────────────────────┘
```

**Interactions:**

**1. Scroll Content (if too long):**
- D-Pad Up/Down scrolls smoothly
- Scrollbar indicator on right edge
- Content fades at edges (gradient mask)

**2. View Move Details:**
- Highlight move → Press A
- Shows move description, effect, accuracy
- Press B to return

**3. Rename Creature (Nickname):**
- Press START → Opens keyboard
- 8 character limit (Game Boy style)
- Capital letters + numbers only
- Saves to creature.name field

**4. Compare with Another:**
- Press Y → "Select creature to compare"
- Shows side-by-side stats (see section 3.4)

**Visual Polish:**

```css
/* Animated sprite */
.detail-sprite {
  animation: breathe 2s ease-in-out infinite,
             float 3s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.05); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* Stat bars with gradient */
.stat-bar-fill {
  background: linear-gradient(to right, 
    var(--gb-dark), var(--gb-light));
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.3);
}

/* Evolve info pulse */
.evolve-info {
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { text-shadow: 0 0 5px var(--gb-light); }
  50% { text-shadow: 0 0 10px var(--gb-highlight); }
}
```

---

### 1.5 Battle Creature Swap

**Use Case:** Switch creatures mid-battle (strategic retreat)

**Access:** Battle Menu → CREATURES

**Layout:**
```
┌─────────────────────────────────────────┐
│ SWITCH CREATURE                         │
├─────────────────────────────────────────┤
│ Current: WHELP (Cannot select)          │
│                                         │
│ ► [Sprite24] SPRITE   Lv.8   ♥♥♡    ▲  │ ← Type advantage ▲
│   [Sprite24] GHOUL    Lv.10  ♥♥♥    ▬  │    (vs enemy)
│   [Sprite24] DRAKE    Lv.7   ♥♡♡    ▼  │
│   [Sprite24] PHOENIX  Lv.9   ♥♥♥    ▲▲ │ ← Super effective
│   [Empty Slot]                          │
│   [Empty Slot]                          │
│                                         │
├─────────────────────────────────────────┤
│ PHOENIX has type advantage vs enemy!    │ ← Hint text
│                                         │
├─────────────────────────────────────────┤
│ A:SWITCH   B:CANCEL                     │
└─────────────────────────────────────────┘
```

**Type Advantage Indicators:**
- **▲▲** = 2× damage (super effective)
- **▲** = 1.5× damage (effective)
- **▬** = 1× damage (normal)
- **▼** = 0.5× damage (not very effective)
- **✕** = 0× damage (no effect)

**Smart Features:**
1. Current creature grayed out (cannot select)
2. Fainted creatures shown last with ✕ icon
3. Low HP creatures have yellow ⚠ warning
4. Best matchup automatically highlighted
5. Enemy type shown in corner for reference

**Interaction Flow:**
1. Select creature → Press A
2. Confirmation prompt: "Send out SPRITE?"
3. Press A again → Swap animation (300ms)
   - Current creature slides left (fades out)
   - New creature slides in from right (fades in)
4. Enemy gets free turn (penalty for switching)
5. Battle continues

**Animation:**
```css
@keyframes swapOut {
  0% { transform: translateX(0); opacity: 1; }
  100% { transform: translateX(-100%); opacity: 0; }
}

@keyframes swapIn {
  0% { transform: translateX(100%); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}
```

---

### 1.6 Auto-Team Suggestions

**Trigger:** Team Manager → Press SELECT button

**Purpose:** AI recommends optimal team composition

**Algorithm Factors:**
- Type coverage (all major types represented)
- Level balance (no creature >10 levels apart)
- Move diversity (physical + special + status)
- Synergy (complementary types)

**Layout:**
```
┌─────────────────────────────────────────┐
│ SUGGESTED TEAM                          │
├─────────────────────────────────────────┤
│ Strategy: Balanced Coverage             │
│                                         │
│ Lead: WHELP (Dragon/Fire)  Lv.12        │
│       High attack, intimidation         │
│                                         │
│ 2. SPRITE (Water)          Lv.8         │
│    Counters Fire enemies                │
│                                         │
│ 3. TREANT (Nature)         Lv.10        │
│    Healing + status control             │
│                                         │
│ 4. GRYPHON (Beast/Flying)  Lv.11        │
│    Speed advantage                      │
│                                         │
│ 5. GHOUL (Undead/Shadow)   Lv.10        │
│    Status ailments                      │
│                                         │
│ 6. PHOENIX (Fire/Spirit)   Lv.9         │
│    Resurrection ability                 │
│                                         │
│ Type Coverage: 10/12 types ✓            │
│ Avg Level: 10.0            ✓            │
│ Move Diversity: High       ✓            │
│                                         │
├─────────────────────────────────────────┤
│ A:APPLY  Y:OTHER STRATEGIES  B:CANCEL   │
└─────────────────────────────────────────┘
```

**Preset Strategies (Y button cycles):**
1. **Balanced** - All-around coverage
2. **Offensive** - High attack stats
3. **Defensive** - High HP/Defense
4. **Speedy** - Fast creatures
5. **Type Specialist** - Single type focus
6. **Status Master** - Ailment-focused

**Apply Flow:**
1. Press A on suggestion
2. Confirmation: "Replace current team?"
3. Shows before/after comparison
4. Press A again → Team swapped with animation
5. Previous team sent to Box 1 (safe)

---

## Feature 2: Enhanced Battle System

### Design Philosophy

**Goals:**
- **Clarity** - Player always knows what will happen
- **Feedback** - Every action has visual/audio response
- **Strategy** - Information enables better decisions
- **Excitement** - Animations create impact and drama

---

### 2.1 Improved Battle HUD

**Current Problems:**
- HP bars too small (4px height)
- No type indicators
- No status effect icons
- No numeric HP for enemy

**New Layout (320×288px):**
```
┌─────────────────────────────────────────┐
│ ╔═══════════════════╗                   │ ← Enemy area
│ ║  [Sprite 48×48]   ║                   │   (elevated)
│ ╚═══════════════════╝                   │
│  ORCGRUNT  Lv.15  ♂  [Beast][Warrior]   │ ← Name, Level, Gender, Types
│  HP: [██████████░░] 85%                  │ ← HP bar + percentage
│  ⚡Paralyze                              │ ← Status icon + name
│                                         │
│             ⚔ BATTLE ⚔                  │ ← Central divider
│                                         │
│                  ╔═══════════╗          │ ← Player area
│                  ║[Sprite48] ║          │   (elevated)
│                  ╚═══════════╝          │
│              WHELP  Lv.12  ♂            │
│         [Dragon][Fire]                  │ ← Types
│  HP: [██████░░░░] 45/52  60%            │ ← Numeric + bar + %
│  🔥Burned                                │ ← Status with icon
│                                         │
├─────────────────────────────────────────┤
│ ▶ FIGHT    BAG     CREATURES    RUN     │ ← Battle menu
└─────────────────────────────────────────┘
```

**Status Effect Icons:**
```
🔥 Burn      (red)    - Loses HP each turn
💀 Poison    (purple) - Loses HP each turn (increasing)
⚡ Paralyze  (yellow) - 25% chance to skip turn
❄ Freeze    (cyan)   - Cannot act (50% thaw chance)
💤 Sleep     (blue)   - Cannot act (1-3 turns)
```

**HP Bar Enhancements:**
```css
/* Larger, more visible HP bars */
.hp-bar {
  height: 8px; /* was 4px */
  border-radius: 4px;
  border: 2px solid var(--gb-darkest);
  background: var(--gb-shadow);
  position: relative;
  overflow: hidden;
}

/* Gradient fill */
.hp-fill {
  background: linear-gradient(to bottom,
    var(--gb-light), var(--gb-dark));
  height: 100%;
  transition: width 400ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.4);
}

/* HP state colors */
.hp-fill.high { /* 70-100% */
  background: linear-gradient(to bottom, #8bac0f, #306230);
}

.hp-fill.medium { /* 30-69% */
  background: linear-gradient(to bottom, #d0a010, #906010);
}

.hp-fill.low { /* 1-29% */
  background: linear-gradient(to bottom, #d94545, #8b0000);
  animation: hpPulse 800ms ease-in-out infinite;
}

@keyframes hpPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

---

### 2.2 Enhanced Move Selection

**Current Issues:**
- No type/power/accuracy shown
- Can't see effectiveness before attacking
- No visual move type differentiation

**New Layout:**
```
┌─────────────────────────────────────────┐
│ SELECT MOVE                             │
├─────────────────────────────────────────┤
│ ► DRAGON BREATH          PP: 8/10       │ ← Selected (highlighted)
│   [Dragon] 60 Power | 100% Acc         │    Type badge, stats
│   Super Effective!  ▲▲                  │    Damage preview
│   Expected: ~45 damage                  │    (calculated)
│                                         │
│   TACKLE               PP: 15/15        │
│   [Normal] 40 Power | 100% Acc         │
│   Normal damage  ▬                      │
│   Expected: ~28 damage                  │
│                                         │
│   BITE                 PP: 12/15        │
│   [Dark] 60 Power | 100% Acc           │
│   Super Effective!  ▲                   │
│   Expected: ~40 damage                  │
│                                         │
│   WING ATTACK          PP: 5/10  ⚠     │ ← Low PP warning
│   [Flying] 60 Power | 95% Acc          │
│   Not very effective... ▼               │
│   Expected: ~22 damage                  │
│                                         │
├─────────────────────────────────────────┤
│ ↑↓:SELECT  A:USE  SELECT:INFO  B:CANCEL │
└─────────────────────────────────────────┘
```

**Key Improvements:**

**1. Type Effectiveness Preview:**
- Calculates vs enemy types in real-time
- Shows damage multiplier (▲▲ = 2×, ▲ = 1.5×, ▬ = 1×, ▼ = 0.5×, ✕ = 0×)
- Estimates damage range (helps strategic planning)

**2. Visual Move Categories:**
```css
/* Color-code move options by type */
.move-option[data-type="fire"] {
  border-left: 4px solid #b85420;
}

.move-option[data-type="water"] {
  border-left: 4px solid #2860a8;
}

/* ... etc for all types */

/* Low PP warning */
.move-option.low-pp::after {
  content: '⚠';
  color: #d0a010;
  animation: blink 1s infinite;
}

/* Out of PP (disabled) */
.move-option.no-pp {
  opacity: 0.4;
  pointer-events: none;
}

.move-option.no-pp::after {
  content: 'NO PP';
  color: #8b0000;
}
```

**3. Move Details Panel (SELECT button):**
```
┌─────────────────────────────────────────┐
│ DRAGON BREATH - Details                 │
├─────────────────────────────────────────┤
│ Type: Dragon                            │
│ Category: Special                       │
│ Power: 60      Accuracy: 100%           │
│ PP: 8/10                                │
│                                         │
│ Effect: May burn the target             │
│ Burn Chance: 10%                        │
│                                         │
│ "The user exhales a mighty blast of     │
│  draconic energy that can scorch foes." │
│                                         │
│ STAB Bonus: YES (+50% damage)           │
│ Vs ORCGRUNT: Super Effective (×2)       │
│                                         │
├─────────────────────────────────────────┤
│ B:BACK                                  │
└─────────────────────────────────────────┘
```

---

### 2.3 Battle Animation System

**Goal:** Make battles visually exciting without slowing gameplay

**Animation Sequence (400ms total):**

1. **Charge (100ms):**
   - Attacker slides forward 8px
   - Sprite squashes slightly (anticipation)
   - SFX: "charge_up.wav"

2. **Impact (50ms):**
   - Screen flash (white/yellow/red based on effectiveness)
   - Defender sprite shakes (3-5px horizontal)
   - Impact particles spawn
   - SFX: "hit_[type].wav"

3. **Damage Number (150ms):**
   - Large number floats up from defender
   - Color-coded background:
     - Green: Super effective
     - White: Normal
     - Red: Not very effective
     - Yellow: Critical hit!
   - Fade out + scale up (1.0 → 1.5)

4. **HP Drain (200ms):**
   - HP bar smoothly decreases
   - Number count-down effect
   - SFX: "hp_drain.wav" (pitch = damage amount)

5. **Recoil (50ms):**
   - Attacker returns to position
   - Defender returns to idle

**Code Example:**
```javascript
async executeMoveAnimation(attacker, defender, move, damage) {
  // 1. Charge
  await this.playAnimation(attacker, 'charge', 100);
  this.playSFX('charge_up');

  // 2. Impact
  this.screenFlash(this.getEffectivenessColor(effectiveness));
  this.shakeSprite(defender, 5, 50);
  this.spawnImpactParticles(defender.x, defender.y, move.type);
  this.playSFX(`hit_${move.type}`);

  // 3. Damage number
  this.showDamageNumber(damage, defender.x, defender.y, {
    color: this.getDamageColor(effectiveness, isCritical),
    isCritical: isCritical
  });

  // 4. HP drain
  await this.animateHPChange(defender, -damage, 200);

  // 5. Recoil
  await this.playAnimation(attacker, 'recoil', 50);
}

getEffectivenessColor(effectiveness) {
  if (effectiveness >= 2.0) return '#8bac0f'; // Green (super effective)
  if (effectiveness <= 0.5) return '#d94545'; // Red (not very effective)
  return '#ffffff'; // White (normal)
}

showDamageNumber(damage, x, y, options) {
  const number = this.createText(damage, x, y);
  number.fontSize = options.isCritical ? 24 : 18;
  number.color = options.color;

  // Animate: float up + scale + fade
  gsap.to(number, {
    y: y - 40,
    scale: 1.5,
    alpha: 0,
    duration: 0.4,
    ease: 'power2.out',
    onComplete: () => number.destroy()
  });
}
```

**Critical Hit Effect:**
```
Special animation:
- Longer screen flash (100ms vs 50ms)
- More intense shake (8px vs 5px)
- "CRITICAL HIT!" banner flies across screen
- Unique SFX: "critical.wav" (high pitch "ding!")
- Damage number is yellow with exclamation mark
- Zoom effect on defender sprite (1.0 → 1.2 → 1.0)
```

**Status Effect Animations:**
```javascript
// Burn effect (rising flames)
spawnBurnParticles(x, y) {
  for (let i = 0; i < 5; i++) {
    this.createParticle({
      x: x + random(-8, 8),
      y: y + 16,
      color: '#FF6600',
      velocity: { x: random(-0.5, 0.5), y: -2 },
      lifetime: 600,
      size: random(2, 4),
      shape: 'circle'
    });
  }
}

// Poison effect (purple bubbles)
spawnPoisonParticles(x, y) {
  for (let i = 0; i < 3; i++) {
    this.createParticle({
      x: x + random(-12, 12),
      y: y + random(0, 16),
      color: '#905090',
      velocity: { x: 0, y: -1 },
      lifetime: 1000,
      size: random(3, 6),
      shape: 'circle',
      wobble: true
    });
  }
}

// Paralyze effect (electric sparks)
spawnParalyzeParticles(x, y) {
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    this.createParticle({
      x: x,
      y: y,
      color: '#d0a010',
      velocity: {
        x: Math.cos(angle) * 3,
        y: Math.sin(angle) * 3
      },
      lifetime: 300,
      size: 2,
      shape: 'square',
      flash: true
    });
  }
}
```

---

### 2.4 Turn Order Indicator

**Problem:** No way to know who attacks first (speed-based)

**Solution:** Show turn order during move selection

**Location:** Top of move selection menu

**Visual:**
```
┌─────────────────────────────────────────┐
│ TURN ORDER:  [👤 WHELP] → [💀 ORCGRUNT] │ ← Player faster
└─────────────────────────────────────────┘

OR

┌─────────────────────────────────────────┐
│ TURN ORDER:  [💀 ORCGRUNT] → [👤 WHELP] │ ← Enemy faster
└─────────────────────────────────────────┘
```

**Logic:**
```javascript
determineTurnOrder(playerCreature, enemyCreature, playerMove, enemyMove) {
  // Priority moves go first (Quick Attack, Extremespeed)
  const playerPriority = playerMove.priority || 0;
  const enemyPriority = enemyMove.priority || 0;

  if (playerPriority !== enemyPriority) {
    return playerPriority > enemyPriority ? 'player_first' : 'enemy_first';
  }

  // Speed stat comparison
  let playerSpeed = playerCreature.speed;
  let enemySpeed = enemyCreature.speed;

  // Apply status modifiers
  if (playerCreature.status === 'paralyze') playerSpeed *= 0.5;
  if (enemyCreature.status === 'paralyze') enemySpeed *= 0.5;

  // Random on tie
  if (playerSpeed === enemySpeed) {
    return Math.random() < 0.5 ? 'player_first' : 'enemy_first';
  }

  return playerSpeed > enemySpeed ? 'player_first' : 'enemy_first';
}
```

**Visual Indicators:**
- Green outline = Faster (attacks first)
- Red outline = Slower (attacks second)
- Arrow (→) shows sequence
- Icons: 👤 = Player, 💀 = Enemy

---

### 2.5 Catch Mechanics UI

**Use Case:** Throwing Soul Stone to catch wild creatures

**Access:** Battle → BAG → Soul Stone → Select enemy

**Animation Sequence (2000ms total):**

1. **Throw (400ms):**
   - Soul Stone flies in arc trajectory (bezier curve)
   - Rotating animation (360° per 200ms)
   - SFX: "throw_ball.wav"

2. **Capture (300ms):**
   - Stone hits enemy
   - Flash effect (white)
   - Enemy turns to red energy particles
   - Energy streams into stone
   - SFX: "capture_beam.wav"

3. **Shake (900ms = 3× 300ms):**
   - Stone falls to ground (bounces once)
   - Stone rocks left/right/left
   - Suspense music plays
   - SFX: "shake.wav" per rock

4. **Result (400ms):**
   - **Success:**
     - Stone locks (star burst effect)
     - "WHELP was caught!" text banner
     - Victory fanfare (4 bars)
     - Creature added to team/box
     - SFX: "catch_success.wav"
   - **Fail:**
     - Stone breaks open (explosion particles)
     - Enemy reappears (fade in)
     - "Oh no! WHELP broke free!" text
     - Battle continues
     - SFX: "catch_fail.wav"

**Catch Rate Assistance UI:**
```
┌─────────────────────────────────────────┐
│ Throw SOUL STONE?                       │
├─────────────────────────────────────────┤
│ Target: ORCGRUNT  Lv.15                 │
│ HP: 35%  Status: Paralyzed ⚡           │
│                                         │
│ Catch Rate: [████░░░░░░] 40%            │ ← Estimate
│                                         │
│ Tips:                                   │
│ • Lower HP = better chance              │
│ • Status effects help (+20%)            │
│ • Sleep/Freeze best (+50%)              │
│                                         │
├─────────────────────────────────────────┤
│ A:THROW   B:CANCEL                      │
└─────────────────────────────────────────┘
```

**Catch Formula (visible to player):**
```javascript
calculateCatchRate(enemy, ballType) {
  const base = enemy.catchRate; // Species-specific (e.g., 45/255)
  const hpFactor = (1 - (enemy.hp / enemy.maxHp)) * 100; // 0-100%

  let statusBonus = 0;
  if (enemy.status === 'sleep' || enemy.status === 'freeze') {
    statusBonus = 50;
  } else if (enemy.status) { // burn, poison, paralyze
    statusBonus = 20;
  }

  const ballMultiplier = {
    'soul_stone': 1.0,      // 1× (basic)
    'great_stone': 1.5,     // 1.5× (better)
    'ultra_stone': 2.0,     // 2× (best)
    'master_stone': 255     // 100% (legendary)
  }[ballType];

  const rate = Math.min(100, 
    (base + hpFactor + statusBonus) * ballMultiplier
  );

  return rate;
}
```

**Shake Calculation (authentic to Pokemon):**
```javascript
attemptCatch(rate) {
  const checks = 3; // Number of shakes
  const threshold = Math.floor(rate * 2.55); // Convert to 0-255

  for (let i = 0; i < checks; i++) {
    const roll = Math.floor(Math.random() * 256);
    if (roll > threshold) {
      return { success: false, shakes: i };
    }
  }

  return { success: true, shakes: 3 };
}
```

---

### 2.6 Victory & Rewards Screen

**Current:** Battle ends abruptly with minimal feedback

**Enhanced Flow:**

**Step 1: Victory Announcement (1000ms):**
```
┌─────────────────────────────────────────┐
│                                         │
│              ★ VICTORY! ★               │
│                                         │
│         [Winner Sprite 64×64]           │
│                                         │
│    You defeated TRAINER MARCUS!         │
│                                         │
└─────────────────────────────────────────┘
```
- Victory fanfare plays (4-bar melody)
- Confetti/sparkle particles fall
- Winner sprite bounces

**Step 2: Experience Gained (per creature):**
```
┌─────────────────────────────────────────┐
│ WHELP gained 145 EXP!                   │
│ [████████░░░░] 389 → 534 / 500          │ ← Bar fills with animation
│                                         │
│ Ding-ding-ding! (sound per tick)        │
└─────────────────────────────────────────┘
```
- EXP bar fills gradually (20 EXP per 50ms)
- SFX: "exp_tick.wav" (increases pitch near level-up)
- When bar reaches 500, overflow continues to next level

**Step 3: Level Up! (if applicable):**
```
┌─────────────────────────────────────────┐
│              LEVEL UP!                  │
│                                         │
│         [WHELP Sprite glowing]          │
│                                         │
│      WHELP grew to Lv.13!               │
│                                         │
│      HP  +3  (52 → 55)                  │
│      ATK +2  (34 → 36)                  │
│      DEF +2  (28 → 30)                  │
│      SPD +1  (31 → 32)                  │
│                                         │
└─────────────────────────────────────────┘
```
- Flash effect (white)
- Sprite scales up (1.0 → 1.3 → 1.0)
- Stats appear one by one (staggered 100ms)
- SFX: "level_up.wav"

**Step 4: New Move Learned (if applicable):**
```
┌─────────────────────────────────────────┐
│ WHELP is trying to learn FLAME BURST!   │
│                                         │
│ But WHELP already knows 4 moves.        │
│                                         │
│ Delete a move to make room?             │
│                                         │
│ Current Moves:                          │
│ ► DRAGON BREATH   [Dragon] 60 Power    │
│   TACKLE          [Normal] 40 Power    │
│   BITE            [Dark] 60 Power      │
│   WING ATTACK     [Flying] 60 Power    │
│                                         │
│ New Move:                               │
│   FLAME BURST     [Fire] 70 Power      │
│   May burn target (20% chance)         │
│                                         │
├─────────────────────────────────────────┤
│ A:REPLACE  B:CANCEL (keep old moves)    │
└─────────────────────────────────────────┘
```
- If no slot available, player chooses which to replace
- Shows move comparison (power, type, effect)
- Can cancel (keep old moveset)

**Step 5: Evolution Check (if applicable):**
```
┌─────────────────────────────────────────┐
│ What? WHELP is evolving!                │
│                                         │
│     [Sprite flashing between forms]     │
│                                         │
│ WHELP evolved into DRAKE!               │
│                                         │
│         [DRAKE Sprite 64×64]            │
│                                         │
└─────────────────────────────────────────┘
```
- Sprite alternates between old/new form (200ms intervals)
- Bright flashing (white/yellow)
- Evolution fanfare (12 bars)
- Can be cancelled by pressing B (optional)

**Step 6: Money & Items:**
```
┌─────────────────────────────────────────┐
│ TRAINER MARCUS paid out $500!           │
│                                         │
│ Money: $3000 → $3500                    │ ← Counting animation
│                                         │
│ Found:                                  │
│ • Health Potion ×2                      │
│ • Soul Stone ×1                         │
│                                         │
├─────────────────────────────────────────┤
│ Press A to continue...                  │
└─────────────────────────────────────────┘
```
- Money counter animates (increment by 10s)
- Items added to bag with icon pop-in
- SFX: "coin.wav" per increment

**Multiple Creatures EXP Distribution:**
```
┌─────────────────────────────────────────┐
│ EXP Distribution:                       │
│                                         │
│ WHELP gained 145 EXP! (active)          │
│ SPRITE gained 145 EXP! (participated)   │
│ GHOUL gained 72 EXP! (switched out)     │ ← 50% for non-active
│                                         │
│ Press A for details...                  │
└─────────────────────────────────────────┘
```

---

### 2.7 Battle Speed Options

**Setting:** Allow players to customize battle pace

**Access:** Settings → Battle Speed

**Options:**
1. **Normal** (default) - Full animations, 400ms per move
2. **Fast** - 1.5× speed, 270ms per move
3. **Instant** - No animations, immediate results

**Implementation:**
```javascript
class BattleSpeed {
  constructor() {
    this.speed = 'normal'; // 'normal', 'fast', 'instant'
    this.multipliers = {
      normal: 1.0,
      fast: 1.5,
      instant: 999 // Skip animations entirely
    };
  }

  getDuration(baseDuration) {
    if (this.speed === 'instant') return 0;
    return baseDuration / this.multipliers[this.speed];
  }

  shouldSkipAnimation() {
    return this.speed === 'instant';
  }
}

// Usage in battle
async executeTurn(playerMove, enemyMove) {
  if (this.battleSpeed.shouldSkipAnimation()) {
    // Instant: Just apply damage, no animations
    this.applyDamage(enemy, damage);
    this.updateBattleUI();
  } else {
    // Normal/Fast: Play animations at scaled speed
    const duration = this.battleSpeed.getDuration(400);
    await this.playMoveAnimation(playerMove, duration);
  }
}
```

**UI Toggle (in battle):**
```
Press START+SELECT during battle:

┌─────────────────────────────────────────┐
│ Battle Speed:                           │
│ ► Normal   (Full animations)            │
│   Fast     (1.5× speed)                 │
│   Instant  (Results only)               │
└─────────────────────────────────────────┘
```

---

## Feature 3: Quality-of-Life Features

### 3.1 Quick Heal System

**Use Case:** Heal party without menu navigation

**Trigger:** Hold B button for 1 second (overworld only)

**UI:**
```
┌─────────────────────────────────────────┐
│ QUICK HEAL                              │
├─────────────────────────────────────────┤
│ Heal Method:                            │
│                                         │
│ ► USE ITEM                              │
│   Health Potion ×5                      │
│   Restores 50 HP to one creature        │
│                                         │
│   HEAL ALL (at Pokemon Center)          │
│   Costs $100 (free at centers)          │
│                                         │
│   NEVERMIND                             │
│                                         │
├─────────────────────────────────────────┤
│ A:SELECT   B:CANCEL                     │
└─────────────────────────────────────────┘
```

**If "USE ITEM" selected:**
```
┌─────────────────────────────────────────┐
│ Select creature to heal:                │
│                                         │
│ ► WHELP     Lv.12  ♥♥♡  (45/52 HP)      │
│   SPRITE   Lv.8   ♥♡♡  (15/35 HP)  ⚠   │ ← Low HP warning
│   GHOUL    Lv.10  ♥♥♥  (40/40 HP)      │
│   (Empty slot)                          │
│                                         │
├─────────────────────────────────────────┤
│ Health Potion: Restores 50 HP           │
│ You have: 5                             │
│                                         │
├─────────────────────────────────────────┤
│ A:USE   B:BACK                          │
└─────────────────────────────────────────┘
```

**Mobile:** Dedicated "+" button in corner overlay

---

### 3.2 Type Chart Quick Reference

**Access:** Press START+SELECT simultaneously (chord input)

**Purpose:** Reference type matchups without interrupting play

**Layout (Interactive):**
```
┌─────────────────────────────────────────┐
│ TYPE EFFECTIVENESS                      │
├─────────────────────────────────────────┤
│ Select Type: ◄ [FIRE] ►                 │ ← Cycle with D-Pad
│                                         │
│ [FIRE] is STRONG against:               │
│   Nature  (×2)                          │
│   Ice     (×2)                          │
│                                         │
│ [FIRE] is WEAK against:                 │
│   Water   (×0.5)                        │
│   Earth   (×0.5)                        │
│   Fire    (×0.5)                        │
│                                         │
│ [FIRE] resists:                         │
│   Fire, Nature, Ice                     │
│                                         │
├─────────────────────────────────────────┤
│ ◄►:CHANGE TYPE  A:GRID VIEW  B:CLOSE    │
└─────────────────────────────────────────┘
```

**Alternative: Grid View (press A):**
```
┌─────────────────────────────────────────┐
│ TYPE CHART (Attacker → Defender)        │
├─────────────────────────────────────────┤
│      │Fir│Wat│Nat│Dra│Shd│Bst│Nor│     │
├──────┼───┼───┼───┼───┼───┼───┼───┤     │
│ Fire │ - │ ▼ │ ▲ │ - │ - │ - │ - │     │
│ Water│ ▲ │ - │ ▼ │ - │ - │ - │ - │     │
│Nature│ ▼ │ ▲ │ - │ - │ - │ ▼ │ - │     │
│Dragon│ - │ - │ - │ ▲ │ - │ - │ - │     │
│Shadow│ - │ - │ - │ - │ ▼ │ - │ ▲ │     │
│ Beast│ - │ - │ - │ - │ ▼ │ ▼ │ ▲ │     │
│Normal│ - │ - │ - │ - │ - │ - │ - │     │
│                                         │
│ ▲ = Super Effective (×2)                │
│ ▼ = Not Very Effective (×0.5)           │
│ - = Normal (×1)                         │
│ ✕ = No Effect (×0)                      │
└─────────────────────────────────────────┘
```

**Persistent Access:** Small "?" button in battle (top-right corner)

---

### 3.3 Creature Comparison Tool

**Use Case:** Compare stats before deciding which to keep/use

**Access:**
- Team Builder → Select creature → Press Y
- Detail View → Press Y

**Flow:**
1. Select first creature (highlighted)
2. Press Y → "Select creature to compare"
3. Select second creature
4. Side-by-side comparison appears

**Layout:**
```
┌─────────────────────────────────────────┐
│ COMPARE                                 │
├─────────────────────────────────────────┤
│   WHELP           vs        DRAKE       │
│   [Sprite32]                [Sprite32]  │
│   Lv.12                     Lv.25       │
│   Dragon/Fire               Dragon/Fire │
│                                         │
├─────────────────────────────────────────┤
│   HP:  52         <         75          │ ← Lower value in red
│   ATK: 34         <         85          │   Higher in green
│   DEF: 28         <         75          │
│   SPD: 31         <         75          │
│                                         │
├─────────────────────────────────────────┤
│   MOVES: 4/4                4/4         │
│   Dragon Breath             Dragon Claw │
│   Tackle                    Flame Burst │
│   Bite                      Dragon Breath│
│   Wing Attack               Aerial Ace  │
│                                         │
├─────────────────────────────────────────┤
│   ABILITIES:                            │
│   None                      Intimidate  │
│                                         │
├─────────────────────────────────────────┤
│   EVOLUTION:                            │
│   → DRAKE (Lv.25)           Final form  │
│                                         │
├─────────────────────────────────────────┤
│ Winner: DRAKE (4/4 stats higher)        │ ← Auto-analysis
│                                         │
├─────────────────────────────────────────┤
│ Y:SWAP COMPARE   B:BACK                 │
└─────────────────────────────────────────┘
```

**Color Coding:**
- Green text = Higher/better value
- Red text = Lower/worse value
- Yellow = Equal values

---

### 3.4 Nickname System (Name Rater)

**Access:** Creature Detail → Press START

**Purpose:** Give custom names to creatures (personalization)

**Keyboard Layout:**
```
┌─────────────────────────────────────────┐
│ NICKNAME WHELP                          │
├─────────────────────────────────────────┤
│ Current Name: WHELP                     │
│                                         │
│ New Name: [F][L][A][M][E][Y]_____       │ ← 8 char limit
│           ▲ Cursor                      │
│                                         │
│ ┌───────────────────────────────────┐   │
│ │ A B C D E F G H I J K L M         │   │
│ │ N O P Q R S T U V W X Y Z         │   │
│ │ 0 1 2 3 4 5 6 7 8 9               │   │
│ │ . , ! ? - ' ♂ ♀ ♥                │   │
│ │                                   │   │
│ │ [SPACE] [DEL] [CLEAR] [DONE]      │   │
│ └───────────────────────────────────┘   │
│                                         │
├─────────────────────────────────────────┤
│ D-Pad:Navigate  A:Select  B:Cancel      │
└─────────────────────────────────────────┘
```

**Features:**
- 8 character limit (Game Boy authentic)
- Capital letters only (retro style)
- Special symbols for flair (♂♀♥)
- DEL removes last character
- CLEAR resets to empty
- DONE saves nickname

**Restrictions:**
- Cannot name "CANCEL" (reserved)
- Cannot use offensive words (filter list)
- Must have at least 1 character

**Display Behavior:**
- Nickname shown everywhere instead of species name
- Pokedex still tracks by species ID
- Can revert to original name by clearing nickname

---

### 3.5 Adventure Journal

**Feature:** Automatic diary of significant events

**Access:** START menu → JOURNAL

**Events Automatically Logged:**
- Creatures caught (timestamp + location)
- Battles won/lost (vs trainers)
- Evolutions
- Badges earned
- Achievements unlocked
- Rare encounters
- First time seeing new species

**Layout:**
```
┌─────────────────────────────────────────┐
│ ◄ ADVENTURE LOG              PAGE 1/5 ►│
├─────────────────────────────────────────┤
│ DAY 3 - GOLDSHIRE                       │
│                                         │
│ 🕐 12:45 PM                              │
│ Caught WHELP (Lv.5) in Goldshire Forest!│
│                                         │
│ 🕐 1:32 PM                               │
│ ★ WHELP evolved into DRAKE!             │
│                                         │
│ 🕐 2:15 PM                               │
│ Defeated TRAINER MARCUS                 │
│ Earned $500                             │
│                                         │
│ 🕐 3:20 PM                               │
│ 🏆 Achievement: Catch 5 creatures       │
│                                         │
│ 🕐 4:10 PM                               │
│ ⚠ WHELP fainted in battle vs ORCGRUNT   │
│                                         │
├─────────────────────────────────────────┤
│ SELECT:FILTER  ◄►:PAGE  B:BACK          │
└─────────────────────────────────────────┘
```

**Filter Options (SELECT button):**
```
VIEW:
► All Events
  Catches Only
  Battles Only
  Evolutions Only
  Achievements Only
  Today
  This Week
```

**Entry Details (press A on entry):**
```
┌─────────────────────────────────────────┐
│ Entry Details                           │
├─────────────────────────────────────────┤
│ Event: Creature Caught                  │
│ Date: Day 3, 12:45 PM                   │
│ Location: Goldshire Forest (X:23 Y:45)  │
│                                         │
│ Creature: WHELP                         │
│ Level: 5                                │
│ Moves: Dragon Breath, Tackle            │
│                                         │
│ Capture:                                │
│ • HP: 3/20 (15%)                        │
│ • Status: Paralyzed                     │
│ • Ball Used: Soul Stone                 │
│ • Catch Rate: 67%                       │
│ • Shakes: 3 (success)                   │
│                                         │
├─────────────────────────────────────────┤
│ B:BACK                                  │
└─────────────────────────────────────────┘
```

**Export Feature:**
- Journal exportable as JSON
- Share with friends
- Import to another save file

---

### 3.6 Auto-Battle Mode

**Use Case:** AI controls player for grinding/farming

**Activation:** Battle Menu → Hold START for 2 seconds

**Behavior:**
- AI selects most effective move
- Auto-switches if creature faints (chooses type advantage)
- Auto-uses healing items if HP <20%
- Auto-catches creatures if HP <30% (wild battles)
- Player can cancel anytime (press any button)

**Visual Indicator:**
```
┌─────────────────────────────────────────┐
│ ⚡ AUTO-BATTLE ACTIVE                    │ ← Top banner (yellow bg)
│ (Press any button to resume control)    │
└─────────────────────────────────────────┘
```

**AI Logic:**
```javascript
class AutoBattleAI {
  selectBestMove(playerCreature, enemyCreature) {
    let bestMove = null;
    let highestScore = -1;

    for (const moveId of playerCreature.moves) {
      const move = this.cartridge.moves[moveId];
      if (playerCreature.pp[moveId] <= 0) continue; // No PP

      let score = move.power || 0;

      // Factor in type effectiveness
      const effectiveness = this.getTypeEffectiveness(
        move.type, enemyCreature.types
      );
      score *= effectiveness;

      // Prefer STAB (Same Type Attack Bonus)
      if (playerCreature.types.includes(move.type)) {
        score *= 1.5;
      }

      // Avoid low PP moves (save for later)
      if (playerCreature.pp[moveId] <= 2) {
        score *= 0.5;
      }

      if (score > highestScore) {
        highestScore = score;
        bestMove = moveId;
      }
    }

    return bestMove || playerCreature.moves[0]; // Fallback
  }

  shouldSwitch(playerCreature, enemyCreature) {
    // Switch if current creature has type disadvantage
    const playerTypes = playerCreature.types;
    const enemyTypes = enemyCreature.types;

    // Check if we're at disadvantage
    let isDisadvantaged = false;
    for (const enemyType of enemyTypes) {
      for (const playerType of playerTypes) {
        const eff = this.getTypeEffectiveness(enemyType, [playerType]);
        if (eff >= 2.0) isDisadvantaged = true;
      }
    }

    // If disadvantaged and HP <50%, consider switching
    if (isDisadvantaged && playerCreature.hp / playerCreature.maxHp < 0.5) {
      const betterCreature = this.findBetterMatchup(enemyCreature);
      if (betterCreature) return betterCreature;
    }

    return null; // Don't switch
  }

  shouldHeal(playerCreature) {
    // Heal if HP <20% and have potions
    const hpPercent = playerCreature.hp / playerCreature.maxHp;
    const hasPotion = this.player.bag['health_potion'] > 0;

    return hpPercent < 0.2 && hasPotion;
  }

  shouldCatch(enemyCreature) {
    // Try to catch if wild, HP <30%, and have balls
    const isCaught = this.player.creatures.some(c => c.id === enemyCreature.id);
    const hpPercent = enemyCreature.hp / enemyCreature.maxHp;
    const hasBall = this.player.bag['soul_stone'] > 0;

    return !isCaught && hpPercent < 0.3 && hasBall;
  }
}
```

**Safety Features:**
- Stops if bag is empty (no items)
- Stops if all creatures faint
- Stops if flee fails 3 times
- Never uses rare items (Ultra Stone, Master Stone)

---

### 3.7 Favorite Creatures

**Feature:** Mark up to 3 creatures as favorites

**Benefits:**
- Favorites appear first in all lists
- Special ★ icon in menus
- Cannot be accidentally released
- Auto-protected in box organization

**Interaction:**
- Team Builder → Select creature → Hold A for 2 seconds
- Heart fills up animation
- "★ WHELP marked as favorite!"
- SFX: "favorite.wav"

**Visual Indicator:**
```
In team list:
★ WHELP      Lv.12  ♥♥♥  (Dragon/Fire)

In box grid:
[■] ← Normal creature sprite
[■★] ← Favorited creature (star overlay)
```

**Unfavorite:**
- Same gesture (hold A for 2s)
- "★ removed from WHELP"

**Limit:**
- Maximum 3 favorites
- If trying to add 4th: "You can only have 3 favorites. Remove one first."

---

### 3.8 Mini-Map & Region Overview

**Feature:** World map showing visited areas

**Access:** START menu → MAP

**Layout:**
```
┌─────────────────────────────────────────┐
│ AZEROTH MAP                             │
├─────────────────────────────────────────┤
│                                         │
│   [🏠 Goldshire]────[🌲 Elwynn Forest]  │
│        │                    │           │
│        │                    │           │
│   [⛰️ Stonepeak]      [👤 You]          │ ← Player
│        │                    │           │
│        │                    │           │
│   [🏰 Stormwind]────[🌊 Crystal Lake]   │
│                            │           │
│                            │           │
│                     [🔥 Burning Steppes] │
│                      (not visited)      │
│                                         │
├─────────────────────────────────────────┤
│ Current: Elwynn Forest                  │
│ Creatures: 12 seen, 8 caught            │
│ Trainers: 3/5 defeated                  │
│                                         │
├─────────────────────────────────────────┤
│ D-Pad:SELECT  A:INFO  B:CLOSE           │
└─────────────────────────────────────────┘
```

**Icons:**
- 🏠 = Town/Village
- 🌲 = Forest
- ⛰️ = Mountain
- 🌊 = Lake/River
- 🔥 = Volcano/Lava
- 🏰 = Castle/City
- 👤 = Player current location
- Gray text = Not yet visited

**Region Details (press A):**
```
┌─────────────────────────────────────────┐
│ ELWYNN FOREST                           │
├─────────────────────────────────────────┤
│ Description: A peaceful woodland area   │
│ bordering Goldshire. Home to many       │
│ nature creatures.                       │
│                                         │
│ Wild Creatures:                         │
│ • Sprite (Water) - Common               │
│ • Whelp (Dragon/Fire) - Uncommon        │
│ • Treant (Nature) - Common              │
│ • Deer (Normal/Beast) - Common          │
│                                         │
│ Trainers: 3/5 defeated                  │
│ • TRAINER MARCUS ✓                      │
│ • TRAINER SARAH ✓                       │
│ • TRAINER TODD ✓                        │
│ • TRAINER ELENA (not battled)           │
│ • TRAINER BOSS (not battled)            │
│                                         │
│ Items Found: 8/12                       │
│ Secrets: 1/3                            │
│                                         │
├─────────────────────────────────────────┤
│ B:BACK                                  │
└─────────────────────────────────────────┘
```

**Interactive:**
- D-Pad to pan map
- A button to view region details
- Automatically updates as player explores

---

### 3.9 Color-Blind Modes

**Feature:** Alternative palettes for accessibility

**Access:** Settings → Accessibility → Color-Blind Mode

**Modes:**
1. **Default** - Standard Game Boy green
2. **Deuteranopia** (red-green) - Blue/yellow palette
3. **Protanopia** (red-green) - Blue/yellow palette
4. **Tritanopia** (blue-yellow) - Red/pink palette
5. **Monochrome** - Black/white/gray

**Type Badges with Patterns:**
```
In addition to colors, use patterns:
[Fire]    = Diagonal stripes
[Water]   = Horizontal waves
[Nature]  = Vertical lines
[Dragon]  = Scales pattern
[Shadow]  = Dots
[Beast]   = Cross-hatch
```

**Status Effects with Unique Icons:**
```
Not just color tints:
🔥 Burn      (flames icon)
💀 Poison    (skull icon)
⚡ Paralyze  (lightning icon)
❄ Freeze    (snowflake icon)
💤 Sleep     (Z's icon)
```

---

### 3.10 Difficulty Modes

**Feature:** Adjust game challenge level

**Access:** New Game → Select Difficulty

**Options:**

**1. Easy Mode:**
- Enemy levels -2 from normal
- Catch rate +20%
- Items cost 50% less
- Starting money: $5000 (vs $3000)
- Starting creatures: 2 (vs 1)

**2. Normal Mode:**
- Default experience
- Balanced gameplay

**3. Hard Mode:**
- Enemy levels +2 from normal
- Catch rate -10%
- Items cost 50% more
- Starting money: $1500
- Enemies have better AI

**4. Nuzlocke Mode:**
- Fainted creatures permanently dead (cannot revive)
- Can only catch first creature per route
- Must nickname all creatures (emotional attachment)
- Battle style: Set (no free switch on enemy faint)
- Permadeath warning on every battle

**Visual Indicator:**
```
Top-right corner shows difficulty icon:
😊 = Easy
😐 = Normal
😠 = Hard
💀 = Nuzlocke
```

---

## Design System

### Color Palette

**Core Game Boy Colors:**
```css
:root {
  /* Original 4 colors */
  --gb-darkest: #0f380f;   /* Shadows, text */
  --gb-dark: #306230;      /* UI elements */
  --gb-light: #8bac0f;     /* Highlights */
  --gb-lightest: #9bbc0f;  /* Backgrounds */

  /* Extended palette (8 total) */
  --gb-medium: #639b3f;    /* Mid-tone */
  --gb-highlight: #b8d868; /* Bright accent */
  --gb-shadow: #071a07;    /* Deep black */
  --gb-ui: #4a5a3a;        /* Button color */

  /* Type colors (adapted to GB palette) */
  --type-fire: #b85420;
  --type-water: #2860a8;
  --type-nature: #488830;
  --type-dragon: #6838b8;
  --type-shadow: #483848;
  --type-beast: #906030;
  --type-spirit: #a0a8c0;
  --type-normal: #787878;

  /* Status colors */
  --status-burn: #d04828;
  --status-poison: #905090;
  --status-paralyze: #d0a010;
  --status-freeze: #40b0d0;
  --status-sleep: #606870;
}
```

### Typography

```css
/* Font stack */
font-family: 'Press Start 2P', 'Courier New', monospace;

/* Sizes (scaled for readability) */
--text-xs: 8px;   /* Subscript, fine print */
--text-sm: 10px;  /* Body text, descriptions */
--text-md: 12px;  /* Menu options, stats */
--text-lg: 16px;  /* Headers, creature names */
--text-xl: 20px;  /* Titles, important messages */
```

### Spacing System

```css
/* Consistent spacing units (multiples of 2px) */
--space-1: 2px;
--space-2: 4px;
--space-3: 8px;
--space-4: 12px;
--space-5: 16px;
--space-6: 24px;
--space-7: 32px;
--space-8: 48px;
```

### Animation Timing

```css
/* Standard durations */
--anim-instant: 50ms;   /* Button press */
--anim-fast: 150ms;     /* Menu transitions */
--anim-normal: 300ms;   /* Screen slides, HP drain */
--anim-slow: 500ms;     /* Creature appearance */
--anim-dramatic: 1000ms; /* Level up, evolution */

/* Easing functions */
--ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-in-out: cubic-bezier(0.645, 0.045, 0.355, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Touch Targets (Mobile)

```css
/* Minimum sizes (iOS/Android HIG) */
--touch-min: 48px;       /* Minimum */
--touch-comfortable: 56px; /* Comfortable */
--touch-large: 64px;     /* Primary actions */
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Priority: Core Team Management**

1. **Data Structure Updates**
   - [ ] Add `player.team[]` (6 slots)
   - [ ] Add `player.boxes[]` (8 boxes × 30 creatures)
   - [ ] Add `creature.uid` (unique instance ID)
   - [ ] Add `creature.name` (nickname field)
   - [ ] Add `creature.metaData` (caught location, date, etc.)

2. **Quick Team View (SELECT button)**
   - [ ] Create overlay UI component
   - [ ] Implement D-Pad navigation (left/right between creatures)
   - [ ] Add HP hearts rendering
   - [ ] Add type badges
   - [ ] Slide-in/out animations
   - [ ] Sound effects

3. **Full Team Manager**
   - [ ] Create team list UI
   - [ ] Implement swap functionality (Y button)
   - [ ] Add to/from storage transitions
   - [ ] Save state to localStorage

4. **Battle Creature Swap**
   - [ ] Enable "CREATURES" button in battle
   - [ ] Show team roster with type advantage indicators
   - [ ] Implement swap animation
   - [ ] Handle enemy free turn

**Estimated Time:** 20-30 hours  
**Deliverable:** Players can view, organize, and switch creatures

---

### Phase 2: Storage & Detail Views (Week 3-4)

**Priority: Creature Management**

5. **Box Storage System**
   - [ ] Create box grid UI (5×6 layout)
   - [ ] Implement box navigation (8 boxes)
   - [ ] Add drag-and-drop (touch)
   - [ ] Filter/sort functionality
   - [ ] Box naming

6. **Creature Detail View**
   - [ ] Full stat display
   - [ ] Move list with details
   - [ ] Evolution info
   - [ ] Capture history
   - [ ] Scrollable content

7. **Nickname System**
   - [ ] Create keyboard UI
   - [ ] 8-character input
   - [ ] Save to creature.name
   - [ ] Display everywhere

**Estimated Time:** 15-20 hours  
**Deliverable:** Complete creature organization system

---

### Phase 3: Battle Enhancements (Week 5-6)

**Priority: Battle Clarity & Feedback**

8. **Improved Battle HUD**
   - [ ] Larger HP bars (8px height)
   - [ ] HP percentage display
   - [ ] Status effect icons
   - [ ] Type badges in battle

9. **Enhanced Move Selection**
   - [ ] Type effectiveness preview (▲▼)
   - [ ] Power/accuracy display
   - [ ] Expected damage calculation
   - [ ] Low PP warnings
   - [ ] Move details panel (SELECT)

10. **Battle Animations**
    - [ ] Damage number pop-ups
    - [ ] Impact flash effects
    - [ ] HP drain animation
    - [ ] Status effect particles
    - [ ] Critical hit effects

11. **Turn Order Indicator**
    - [ ] Speed-based calculation
    - [ ] Visual preview (top of move menu)
    - [ ] Priority move handling

**Estimated Time:** 25-35 hours  
**Deliverable:** Polished, informative battle system

---

### Phase 4: Quality-of-Life (Week 7-8)

**Priority: Player Convenience**

12. **Quick Heal System**
    - [ ] Hold B button trigger
    - [ ] Item selection UI
    - [ ] Creature selection
    - [ ] Mobile button overlay

13. **Type Chart Reference**
    - [ ] START+SELECT chord input
    - [ ] Interactive type selector
    - [ ] Grid view option
    - [ ] In-battle access

14. **Comparison Tool**
    - [ ] Side-by-side stats
    - [ ] Color-coded values
    - [ ] Auto-analysis

15. **Adventure Journal**
    - [ ] Auto-logging system
    - [ ] Event types (catch, battle, evolve)
    - [ ] Filter/sort options
    - [ ] Detail view

16. **Auto-Battle Mode**
    - [ ] AI move selection
    - [ ] Auto-switch logic
    - [ ] Auto-heal/catch
    - [ ] Cancel anytime

**Estimated Time:** 20-25 hours  
**Deliverable:** Comprehensive QoL features

---

### Phase 5: Polish & Accessibility (Week 9-10)

**Priority: Refinement**

17. **Visual Polish**
    - [ ] Victory/rewards screen
    - [ ] Catch mechanics UI
    - [ ] Level-up animations
    - [ ] Evolution sequence
    - [ ] Sprite idle animations

18. **Additional Features**
    - [ ] Favorite creatures (★)
    - [ ] Mini-map system
    - [ ] Battle speed options
    - [ ] Difficulty modes

19. **Accessibility**
    - [ ] Color-blind modes
    - [ ] Button remapping
    - [ ] Dyslexia-friendly font
    - [ ] One-handed mode

20. **Testing & Optimization**
    - [ ] Mobile device testing
    - [ ] Performance profiling
    - [ ] Battery usage optimization
    - [ ] LocalStorage compression
    - [ ] Cross-browser testing

**Estimated Time:** 15-20 hours  
**Deliverable:** Production-ready, accessible game

---

## Total Estimated Time

**Minimum:** 95 hours (12 weeks part-time, 6 weeks full-time)  
**Maximum:** 130 hours (16 weeks part-time, 8 weeks full-time)

---

## Success Metrics

### User Experience Goals

1. **Discoverability**
   - 90% of players find team builder without tutorial
   - 80% understand type effectiveness within 5 battles

2. **Efficiency**
   - Team swap in battle: <5 seconds
   - Creature organization: <2 minutes per 10 creatures
   - Quick heal: <3 seconds

3. **Satisfaction**
   - Post-play survey: 4.5/5 average rating
   - 80% completion rate for team building tutorial
   - <5% error rate in move selection

4. **Retention**
   - 70% return within 24 hours
   - 50% return within 1 week
   - Average session: 20+ minutes

---

## Testing Strategy

### User Testing Scenarios

**Scenario 1: First Time Team Building**
- Task: "Organize your team with strongest creature as lead"
- Success criteria: Completes without help in <60 seconds
- Measure: Time, help requests, errors

**Scenario 2: Battle Strategy**
- Task: "Switch to a creature with type advantage"
- Success criteria: Selects correct creature in <10 seconds
- Measure: Accuracy, time, confidence (self-report)

**Scenario 3: Storage Management**
- Task: "Move 5 creatures to Box 2"
- Success criteria: No errors, <2 minutes
- Measure: Time, navigation path, errors

### A/B Tests

**Test 1: HP Display**
- Version A: Hearts (♥♥♥)
- Version B: Numeric (45/52)
- Version C: Bar (████░░)
- Metric: Time to recognize low HP, preference

**Test 2: Type Effectiveness**
- Version A: Symbols (▲▼)
- Version B: Text ("Super Effective!")
- Version C: Colors only
- Metric: Move selection accuracy, speed

**Test 3: Menu Layout**
- Version A: Vertical list
- Version B: Grid (2×2)
- Version C: Radial menu
- Metric: Selection speed, error rate

---

## Future Enhancements (Post-v1.0)

### Advanced Features

1. **Breeding System**
   - Combine two creatures for offspring
   - Inherit moves from parents
   - Rare egg mechanics

2. **Shiny Variants**
   - 1/4096 chance for alternate colors
   - Sparkle animation on encounter
   - Trophy badge in detail view

3. **Held Items**
   - Equip items for battle bonuses
   - Leftovers: HP regen per turn
   - Focus Band: Survive fatal hit (10% chance)

4. **Abilities**
   - Passive effects (Intimidate, Lightning Rod)
   - Hidden abilities (rare)
   - Ability capsules to change

5. **Weather System**
   - Rain: Water moves +50%, Fire moves -50%
   - Sun: Fire moves +50%, Water moves -50%
   - Hail: Ice moves +25%, non-Ice lose HP

6. **Multi-Battles**
   - 2v2 battles with coordination
   - Double targeting
   - Combination moves

7. **Online Features**
   - Friend codes
   - Trading via JSON export/import
   - Battle replays
   - Leaderboards

8. **Competitive Mode**
   - EV/IV stats (hidden values)
   - Nature system (personality traits)
   - Ranked battles
   - Tournaments

---

## Conclusion

This UX-centric design document provides a comprehensive roadmap for implementing three core feature sets in WoWmon:

1. **Team Builder System** - Complete creature management with intuitive navigation
2. **Enhanced Battle System** - Clear information and satisfying feedback
3. **Quality-of-Life Features** - Player-requested conveniences

**Design Principles Applied:**
- ✅ Intuitive interactions (minimal learning curve)
- ✅ Game Boy aesthetic (authentic retro charm)
- ✅ Minimal cognitive load (progressive disclosure)
- ✅ Delightful feedback (animations, sounds, haptics)
- ✅ Mobile-friendly (touch targets, gestures)
- ✅ Accessible (keyboard, screen reader, color-blind modes)

**Key Innovations:**
- HP hearts system (more intuitive than bars)
- Type effectiveness preview in move menu (strategic advantage)
- Quick team view via SELECT button (instant access)
- Box storage with 240 creature capacity (long-term play)
- Auto-team suggestions (helps casual players)
- Adventure journal (narrative investment)

**Expected Outcomes:**
- Increased player retention (compelling progression)
- Higher satisfaction scores (quality-of-life features)
- Broader accessibility (multiple play styles supported)
- Viral potential (compelling enough to share)

---

**Document Status:** ✅ Complete and ready for implementation

**Next Steps:**
1. Review with development team
2. Prioritize Phase 1 features
3. Create technical specification document
4. Begin implementation with Quick Team View
5. User testing after each phase

---

**END OF DOCUMENT**
