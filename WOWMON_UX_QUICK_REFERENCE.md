# WoWmon UX Quick Reference Guide
**Agent 2: User Experience Design - Visual Cheatsheet**

---

## Input Controls Mapping

### Game Boy Button Layout
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   D-PAD                  A BUTTON (Confirm)         │
│    ▲                     B BUTTON (Cancel)          │
│  ◄ ► (Navigate)                                     │
│    ▼                                                │
│                                                     │
│   START BUTTON (Menu)    SELECT BUTTON (Quick View) │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Context-Specific Controls

**Overworld:**
- D-Pad: Move character
- A: Interact with objects/NPCs
- B: (unused normally) → **HOLD 1s = QUICK HEAL**
- START: Open main menu
- SELECT: **Open Quick Team View**

**Battle:**
- D-Pad: Navigate menus
- A: Confirm selection
- B: Cancel/back
- START: (unused) → **HOLD 2s = AUTO-BATTLE**
- SELECT: View move details
- **START+SELECT: Battle speed toggle**

**Team Builder:**
- D-Pad: Navigate/select
- A: Select creature / Info
- B: Back/close
- Y: Swap mode / Compare
- X: Open storage
- START: Rename creature
- SELECT: Auto-team suggestions

**Box Storage:**
- D-Pad: Navigate grid
- A: Select creature
- B: Back to team
- Y: Move mode
- SELECT: Filter/sort
- ◄►: Switch boxes (on header)

---

## Navigation Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                   OVERWORLD                         │
│         (Player exploring the world)                │
└─────────────────────────────────────────────────────┘
          │
          ├─ [Press SELECT] ───────────────────────────┐
          │                                            │
          │  ┌─────────────────────────────────────┐   │
          │  │   QUICK TEAM VIEW (Overlay)         │   │
          │  │   - See all 6 team members          │   │
          │  │   - HP status at glance             │   │
          │  │   - D-Pad ◄► to cycle               │   │
          │  │   - Press A for details             │   │
          │  │   - Press B to close                │   │
          │  │   - Press START for full manager    │   │
          │  └─────────────────────────────────────┘   │
          │                                            │
          ├─ [Press START] ────────────────────────────┤
          │                                            │
          │  ┌─────────────────────────────────────┐   │
          │  │      MAIN MENU                      │   │
          │  │  ► CREATURES                        │───┼── Full Team Manager
          │  │    BAG                              │   │
          │  │    SAVE                             │   │
          │  │    JOURNAL                          │   │
          │  │    MAP                              │   │
          │  │    SETTINGS                         │   │
          │  │    EXIT                             │   │
          │  └─────────────────────────────────────┘   │
          │                                            │
          └─ [Random Encounter] ───────────────────────┤
                                                       │
┌─────────────────────────────────────────────────────┐
│                    BATTLE                           │
│         (Turn-based combat system)                  │
└─────────────────────────────────────────────────────┘
          │
          ├─ [Battle Menu] ────────────────────────────┐
          │                                            │
          │  ┌─────────────────────────────────────┐   │
          │  │  ► FIGHT     (Select move)          │───┼── Move Selection
          │  │    BAG       (Use items)            │   │   - See effectiveness
          │  │    CREATURES (Switch creature)      │───┼── Switch Creature
          │  │    RUN       (Flee battle)          │   │   - Type advantages
          │  └─────────────────────────────────────┘   │   - HP status
          │                                            │
          └────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│              TEAM MANAGEMENT                        │
│       (From Quick View or Main Menu)                │
└─────────────────────────────────────────────────────┘
          │
          ├─ [Full Team Manager] ──────────────────────┐
          │  - List of 6 team slots                    │
          │  - Press Y to swap positions               │
          │  - Press A for details                     │
          │  - Press X for storage                     │
          │                                            │
          ├─ [Press X or interact with PC] ────────────┤
          │                                            │
          │  ┌─────────────────────────────────────┐   │
          │  │      BOX STORAGE                    │   │
          │  │   [■][■][■][■][■][■]  (5×6 grid)    │   │
          │  │   [■][■][■][■][■][■]                │   │
          │  │   [■][■][□][□][□][□]                │   │
          │  │   [□][□][□][□][□][□]                │   │
          │  │   [□][□][□][□][□][□]                │   │
          │  │   14/30 creatures in Box 1          │   │
          │  │   ◄► to switch boxes (8 total)      │   │
          │  └─────────────────────────────────────┘   │
          │                                            │
          ├─ [Press A on creature] ────────────────────┤
          │                                            │
          │  ┌─────────────────────────────────────┐   │
          │  │    CREATURE DETAIL VIEW             │   │
          │  │    [Large Sprite 64×64]             │   │
          │  │    - Full stats                     │   │
          │  │    - Move list                      │   │
          │  │    - Evolution info                 │   │
          │  │    - Capture history                │   │
          │  │    Press START to rename            │   │
          │  │    Press Y to compare               │   │
          │  └─────────────────────────────────────┘   │
          │                                            │
          └────────────────────────────────────────────┘
```

---

## Feature Access Quick Reference

| Feature | Access Method | Context |
|---------|--------------|---------|
| **Quick Team View** | Press SELECT | Overworld (anytime) |
| **Full Team Manager** | START → CREATURES | Main menu |
| **Box Storage** | Team Manager → Press X | Team management |
| **Creature Details** | Select creature → Press A | Any creature list |
| **Rename Creature** | Detail view → Press START | Creature detail |
| **Compare Creatures** | Detail view → Press Y | Creature detail |
| **Switch in Battle** | Battle → CREATURES | Battle menu |
| **Quick Heal** | Hold B for 1 second | Overworld only |
| **Type Chart** | START+SELECT (chord) | Anytime |
| **Auto-Battle** | Hold START for 2 seconds | During battle |
| **Battle Speed** | START+SELECT | During battle |
| **Adventure Journal** | START → JOURNAL | Main menu |
| **Mini-Map** | START → MAP | Main menu |
| **Auto-Team Suggest** | Team Manager → SELECT | Team management |
| **Filter/Sort Box** | Box Storage → SELECT | Box storage |

---

## Visual Language Guide

### HP Display Systems

**Hearts (Recommended):**
```
Full HP (80-100%):   ♥♥♥♥♥  (green)
Medium HP (40-79%):  ♥♥♡♡♡  (yellow)
Low HP (1-39%):      ♥♡♡♡♡  (red, pulsing)
Fainted (0%):        ✕✕✕✕✕  (gray)
```

**Bars (Alternative):**
```
High HP:   [████████░░] 80%
Medium HP: [████░░░░░░] 40%
Low HP:    [█░░░░░░░░░] 10% (pulsing)
```

**Numeric (Most Precise):**
```
45/52 HP (87%)
```

### Type Effectiveness Indicators

```
▲▲  = Super Effective (2× damage)
▲   = Effective (1.5× damage)
▬   = Normal (1× damage)
▼   = Not Very Effective (0.5× damage)
✕   = No Effect (0× damage)
```

**Example in Move Selection:**
```
┌─────────────────────────────────────────┐
│ ► DRAGON BREATH          PP: 8/10       │
│   [Dragon] 60 Power | 100% Acc         │
│   Super Effective!  ▲▲                  │
│   Expected: ~45 damage                  │
└─────────────────────────────────────────┘
```

### Status Effect Icons

```
🔥 Burn      - Loses HP each turn (red)
💀 Poison    - Loses HP each turn, increasing (purple)
⚡ Paralyze  - 25% chance can't act (yellow)
❄ Freeze    - Can't act, 50% thaw chance (cyan)
💤 Sleep     - Can't act for 1-3 turns (blue)
```

### Type Badges (Color-Coded)

```
[Fire]    #b85420  (dark orange-red)  | Diagonal stripes
[Water]   #2860a8  (dark blue)        | Horizontal waves
[Nature]  #488830  (dark green)       | Vertical lines
[Dragon]  #6838b8  (dark purple)      | Scales pattern
[Shadow]  #483848  (dark gray-purple) | Dots
[Beast]   #906030  (brown)            | Cross-hatch
[Spirit]  #a0a8c0  (light blue-gray)  | Swirls
[Normal]  #787878  (gray)             | Plain
```

---

## Common User Flows

### Flow 1: Organizing Your Team

```
1. Press SELECT → Quick Team View opens
2. D-Pad ◄► → Cycle through your 6 creatures
3. Press A on creature → View full details
4. Press Y → Compare with another creature
5. Press B → Return to Quick View
6. Press START → Open Full Team Manager
7. Highlight creature → Press Y → "SWAP MODE"
8. D-Pad ↑↓ → Select destination slot
9. Press A → Creature moves to new position
10. Press B → Return to overworld
```

**Time:** <60 seconds

### Flow 2: Switching Creatures in Battle

```
1. Battle Menu → Navigate to CREATURES
2. Press A → Team roster appears
3. D-Pad ↑↓ → Select replacement creature
   - See type advantages: ▲▲ = Super Effective
   - See HP status: ♥♥♡ = Medium HP
4. Press A → Confirmation prompt appears
5. Press A again → Swap animation plays
6. New creature enters battle
7. Enemy gets free attack (penalty)
8. Battle continues with new creature
```

**Time:** <10 seconds

### Flow 3: Catching a Wild Creature

```
1. Battle → Navigate to BAG
2. Select Soul Stone → Press A
3. Catch rate screen appears:
   - Target: ORCGRUNT Lv.15
   - HP: 35%  Status: Paralyzed
   - Catch Rate: [████░░░░░░] 40%
   - Tip: Lower HP = better chance
4. Press A → Throw animation
5. Stone captures creature (energy particles)
6. Stone falls and shakes 1-3 times
7. Result:
   - SUCCESS: "ORCGRUNT was caught!" + fanfare
   - FAIL: "Oh no! Broke free!" + battle continues
```

**Time:** 2-3 seconds

### Flow 4: Using Quick Heal

```
1. Overworld → Hold B button for 1 second
2. Quick Heal menu appears
3. Select "USE ITEM" → Press A
4. Item selection appears (Health Potion x5)
5. Press A → Creature selection
6. Highlight WHELP (45/52 HP) → Press A
7. Healing animation plays (sparkles)
8. "WHELP restored 50 HP!" (now 52/52 HP)
9. Return to overworld
```

**Time:** <5 seconds

### Flow 5: Checking Type Chart

```
1. Anytime → Press START+SELECT (chord)
2. Type Chart appears
3. Default: [FIRE] selected
4. Shows:
   - Strong against: Nature (×2), Ice (×2)
   - Weak against: Water (×0.5), Earth (×0.5)
5. D-Pad ◄► → Cycle through types
6. Press A → Switch to grid view (all matchups)
7. Press B → Close chart
```

**Time:** <3 seconds

---

## Battle System Flowchart

```
┌─────────────────────────────────────────┐
│       ENCOUNTER STARTS                  │
│   (Wild creature or trainer battle)     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│    BATTLE MENU APPEARS                  │
│  ► FIGHT    BAG    CREATURES    RUN     │
└─────────────────────────────────────────┘
              ↓
         Select FIGHT
              ↓
┌─────────────────────────────────────────┐
│      MOVE SELECTION                     │
│  ► DRAGON BREATH      PP: 8/10          │
│    [Dragon] 60 Power | 100% Acc        │
│    Super Effective!  ▲▲                 │
│    Expected: ~45 damage                 │
│                                         │
│  • See type effectiveness BEFORE attack │
│  • See power/accuracy                   │
│  • See expected damage                  │
│  • SELECT for move details              │
└─────────────────────────────────────────┘
              ↓
         Press A (confirm)
              ↓
┌─────────────────────────────────────────┐
│    TURN ORDER CALCULATED                │
│  [👤 WHELP] → [💀 ORCGRUNT]             │
│  (Player faster, attacks first)         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      ATTACK ANIMATION (400ms)           │
│  1. Charge (100ms): Slide forward       │
│  2. Impact (50ms): Flash + shake        │
│  3. Damage Number (150ms): "45" floats  │
│  4. HP Drain (200ms): Bar decreases     │
│  5. Recoil (50ms): Return to position   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     CHECK BATTLE STATUS                 │
└─────────────────────────────────────────┘
    ↓              ↓              ↓
Enemy HP    Enemy HP > 0    Enemy Caught
reaches 0   Continue battle  (if throwing ball)
    ↓              ↓              ↓
┌─────────┐  ┌─────────┐  ┌─────────────┐
│ VICTORY │  │  ENEMY  │  │   CAUGHT!   │
│  SCREEN │  │  TURN   │  │ Add to team │
└─────────┘  └─────────┘  └─────────────┘
```

---

## Victory Sequence Flowchart

```
┌─────────────────────────────────────────┐
│      ENEMY HP REACHES 0                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   VICTORY ANNOUNCEMENT (1000ms)         │
│            ★ VICTORY! ★                 │
│    [Winner sprite bouncing]             │
│    Confetti particles falling           │
│    Victory fanfare (4 bars)             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   EXP GAINED (per creature)             │
│   WHELP gained 145 EXP!                 │
│   [████████░░░░] 389 → 534 / 500        │
│   Bar fills gradually (ding-ding-ding)  │
└─────────────────────────────────────────┘
              ↓
        EXP > Level Threshold?
              ↓
          YES │ NO → Skip to money
              ↓
┌─────────────────────────────────────────┐
│       LEVEL UP! (1000ms)                │
│     [Sprite glowing, flash effect]      │
│      WHELP grew to Lv.13!               │
│       HP  +3  (52 → 55)                 │
│       ATK +2  (34 → 36)                 │
│       DEF +2  (28 → 30)                 │
│       SPD +1  (31 → 32)                 │
└─────────────────────────────────────────┘
              ↓
      New move to learn?
              ↓
          YES │ NO → Skip to evolution
              ↓
┌─────────────────────────────────────────┐
│    MOVE LEARNING PROMPT                 │
│   WHELP wants to learn FLAME BURST!     │
│   But WHELP already knows 4 moves.      │
│   Delete a move to make room?           │
│   Current: [Dragon Breath, Tackle...]   │
│   New: [Flame Burst - 70 Power]         │
│   A: Replace  B: Cancel                 │
└─────────────────────────────────────────┘
              ↓
     Level >= Evolution Level?
              ↓
          YES │ NO → Skip to money
              ↓
┌─────────────────────────────────────────┐
│      EVOLUTION! (3000ms)                │
│   What? WHELP is evolving!              │
│   [Sprite flashing between old/new]     │
│   Bright white/yellow flashing          │
│   Evolution fanfare (12 bars)           │
│   WHELP evolved into DRAKE!             │
│   [New sprite appears]                  │
│   (Press B to cancel - optional)        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     MONEY & ITEMS                       │
│   TRAINER MARCUS paid out $500!         │
│   Money: $3000 → $3500 (counting)       │
│   Found: Health Potion ×2               │
│          Soul Stone ×1                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      RETURN TO OVERWORLD                │
│      (Press A to continue...)           │
└─────────────────────────────────────────┘
```

---

## Data Structure Reference

### Player Object
```javascript
player: {
  name: 'PLAYER',
  x: 10, y: 10,
  facing: 'down',
  
  // NEW: Team roster (6 slots)
  team: [
    { slot: 0, creatureId: 'whelp_001', active: true },  // Lead
    { slot: 1, creatureId: 'sprite_002', active: false },
    { slot: 2, creatureId: 'ghoul_003', active: false },
    { slot: 3, null, active: false },  // Empty slots
    { slot: 4, null, active: false },
    { slot: 5, null, active: false }
  ],
  
  // NEW: Box storage (8 boxes × 30 creatures = 240 total)
  boxes: [
    { id: 1, name: "Box 1: Goldshire", creatures: [...] },
    { id: 2, name: "Box 2: Favorites", creatures: [...] },
    // ... up to 8 boxes
  ],
  
  // NEW: Favorites (max 3)
  favorites: ['whelp_001', 'phoenix_042'],
  
  // Existing inventory
  bag: {
    'health_potion': 5,
    'soul_stone': 10
  },
  
  money: 3000,
  badges: [],
  
  // Stats tracking
  stats: {
    battlesWon: 0,
    creaturesCaught: 0,
    uniqueCreaturesCaught: [],
    evolutions: 0,
    stepsWalked: 0,
    playTime: 0,
    // ... more stats
  },
  
  achievements: {},
  
  // NEW: Adventure journal
  journal: {
    entries: [
      {
        type: 'catch',
        creature: 'WHELP',
        level: 5,
        location: 'Goldshire Forest',
        timestamp: 1699564800000
      },
      // ... more entries
    ]
  }
}
```

### Creature Instance Object
```javascript
{
  uid: 'whelp_001',        // Unique instance ID
  id: 'whelp',             // Species ID (references cartridge)
  name: 'FLAMEY',          // Nickname (default: species name)
  level: 12,
  exp: 389,
  hp: 45,
  maxHp: 52,
  attack: 34,
  defense: 28,
  speed: 31,
  types: ['dragon', 'fire'],
  
  moves: ['dragon_breath', 'tackle', 'bite', 'wing_attack'],
  pp: {
    'dragon_breath': 8,
    'tackle': 15,
    'bite': 12,
    'wing_attack': 5
  },
  
  status: null,            // 'burn', 'poison', 'paralyze', 'sleep', 'freeze'
  friendship: 150,         // 0-255
  
  // NEW: Capture metadata
  metaData: {
    caughtAt: 'goldshire_forest',
    caughtDate: 1699564800000,
    caughtLevel: 5,
    originalTrainer: 'PLAYER',
    ballType: 'soul_stone',
    catchRate: 67  // Percentage when caught
  }
}
```

### Battle State Object
```javascript
battle: {
  type: 'wild',            // 'wild' or 'trainer'
  trainerId: null,         // ID if trainer battle
  
  playerCreature: {...},   // Active creature
  enemyCreature: {...},    // Enemy creature
  
  turnCount: 5,            // Turns elapsed
  
  // NEW: Turn order
  turnOrder: ['player', 'enemy'],  // Determined by speed
  
  // NEW: Battle speed setting
  speed: 'normal',         // 'normal', 'fast', 'instant'
  
  // NEW: Auto-battle flag
  autoBattle: false,       // AI controls if true
  
  weather: null,           // Future: 'rain', 'sun', 'hail'
  terrain: null            // Future: 'grass', 'water', 'cave'
}
```

---

## Animation Reference

### CSS Animation Durations

```css
/* Button press feedback */
--anim-instant: 50ms;

/* Menu transitions */
--anim-fast: 150ms;

/* Screen slides, HP drain */
--anim-normal: 300ms;

/* Creature appearance */
--anim-slow: 500ms;

/* Level up, evolution */
--anim-dramatic: 1000ms;
```

### Battle Animation Sequence

```
Total: 400ms

1. Charge    (100ms): Attacker slides forward 8px
2. Impact    ( 50ms): Screen flash + defender shakes
3. Damage    (150ms): Number floats up + fades
4. HP Drain  (200ms): Bar smoothly decreases
5. Recoil    ( 50ms): Attacker returns to position

(Times overlap for smooth flow)
```

### Particle Effects

**Burn (🔥):**
- 5 flame particles
- Rise from sprite base
- Color: #FF6600
- Lifetime: 600ms
- Velocity: y=-2, x=random(-0.5, 0.5)

**Poison (💀):**
- 3 bubble particles
- Float around sprite
- Color: #905090
- Lifetime: 1000ms
- Wobble effect

**Paralyze (⚡):**
- 8 spark particles
- Radial burst pattern
- Color: #d0a010
- Lifetime: 300ms
- Flash effect

---

## Accessibility Features

### Keyboard Navigation

- **Tab**: Cycle through interactive elements
- **Arrow Keys**: Menu navigation
- **Enter/Space**: Confirm selection
- **Escape**: Cancel/back
- **Focus indicators**: Always visible (yellow outline)

### Screen Reader Support

- All interactive elements have aria-labels
- Live regions announce battle events
- Descriptive alt text for sprites
- Semantic HTML structure

### Color-Blind Modes

- **Deuteranopia** (red-green): Blue/yellow palette
- **Protanopia** (red-green): Blue/yellow palette
- **Tritanopia** (blue-yellow): Red/pink palette
- **Monochrome**: Black/white/gray

### Additional Options

- **High Contrast Mode**: Increased contrast ratios
- **Large Text Mode**: 120% font size
- **Reduced Motion**: Animations minimized
- **Button Remapping**: Custom key bindings
- **One-Handed Mode** (mobile): Larger buttons, side-aligned

---

## Performance Targets

### Frame Rates
- **60 FPS**: Menu navigation, overworld
- **30 FPS**: Battle animations (acceptable)
- **Instant (<16ms)**: Input response

### Loading Times
- **Initial Load**: <2 seconds
- **Screen Transition**: <300ms
- **Battle Start**: <500ms
- **Save/Load**: <100ms

### Memory Usage
- **Sprite Cache**: ~500KB (50 sprites × 48×48px)
- **Save Data**: <100KB (compressed JSON)
- **Audio Buffers**: <5MB total
- **Total Memory**: <10MB (mobile-friendly)

---

## Common Issues & Solutions

### Issue 1: "Can't find team builder"
**Solution:** Press SELECT button (not START)

### Issue 2: "CREATURES button says 'Not implemented'"
**Old bug - Will be fixed in Phase 1**

### Issue 3: "HP bars too small to read"
**Solution:** New HP hearts system (♥♥♥) coming in Phase 3

### Issue 4: "Don't know which move to use"
**Solution:** New type effectiveness preview (▲▼) in Phase 3

### Issue 5: "Running out of space for creatures"
**Solution:** Box storage system (240 capacity) in Phase 2

---

## Quick Tips

1. **Always check type advantages** before attacking (▲▼ indicators)
2. **Use Quick Heal** (Hold B) instead of navigating menus
3. **Favorite your best 3 creatures** (Hold A on creature) for quick access
4. **Check Adventure Journal** for narrative context and history
5. **Use Auto-Battle** (Hold START in battle) for grinding levels
6. **Compare creatures** (Press Y in detail view) before deciding which to keep
7. **Type Chart** (START+SELECT) is always accessible, even in battle
8. **Quick Team View** (SELECT) lets you check status without interrupting gameplay
9. **Box storage is automatic** - creatures go to next available slot
10. **Nickname creatures** (START in detail view) for emotional attachment

---

## Mobile-Specific Tips

- **Tap**: A button (confirm)
- **Swipe**: Movement direction
- **Long-press**: Hold actions (heal, favorite, rename)
- **Pinch-to-zoom**: Enlarge sprites in detail view
- **Two-finger tap**: B button (back/cancel)
- **Use fullscreen mode** for better immersion
- **Enable haptic feedback** for tactile response

---

## Future Features (Coming Soon)

- **Breeding System**: Combine creatures for offspring
- **Shiny Variants**: Rare alternate colors (1/4096 chance)
- **Held Items**: Equip items for battle bonuses
- **Abilities**: Passive effects (Intimidate, Lightning Rod)
- **Weather System**: Rain/Sun affects battle (Water/Fire boosts)
- **Multi-Battles**: 2v2 with coordinated attacks
- **Online Trading**: Export/import creature codes
- **Gym Leaders**: Boss battles with unique strategies
- **Elite Four**: Post-game challenge
- **Pokedex**: Encyclopedia tracking seen/caught

---

## Additional Resources

**Full Documentation:**
- `/Users/kodyw/Documents/GitHub/localFirstTools3/WOWMON_UX_FEATURE_DESIGN.md` (80KB, comprehensive)

**Summary:**
- `/Users/kodyw/Documents/GitHub/localFirstTools3/WOWMON_UX_SUMMARY.txt` (13KB, text overview)

**Original Game:**
- `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html` (current implementation)

**Related Guides:**
- `/Users/kodyw/Documents/GitHub/localFirstTools3/TEAM_BUILDER_GUIDE.md` (existing guide)

---

**Last Updated:** 2025-10-12  
**Version:** 2.0  
**Status:** Ready for Implementation

---

**END OF QUICK REFERENCE**
