# WoWmon Metroidvania - Visual Design Guide

## World Map Visualization

```
                    ╔═══════════════════════════╗
                    ║   FROZEN PEAKS            ║
                    ║   ❄️ Ice/Dragon            ║
                    ║   Lv 25-35 | Ice Gym      ║
                    ║   🏔️ Summit Dragon Lair   ║
                    ╚═══════════╦═══════════════╝
                                ║ [Climbing]
                    ┌───────────╨──────────────┐
                    │   Mountain Pass          │
                    │   Vertical Climbing      │
                    └───────────┬──────────────┘
                                ║
        ╔═══════════════════════╩═══════════════════════╗
        ║            DARK FOREST                        ║
        ║            🌲 Nature/Spirit                    ║
        ║            Lv 5-15 | Nature Gym               ║
        ║   🌳 Twisted Grove  ✨ Moonwell  🌲 Hollow   ║
        ╚═══════════════╦═══════════════════════════════╝
                        ║
                        ║ [Always Open]
                        ║
    ╔═══════════════╗   ║   ╔═══════════════════════╗
    ║ SUNKEN RUINS  ╠═══╩═══╣    GOLDSHIRE (HUB)    ║
    ║ 🌊 Water      ║       ║    🏠 Central Hub      ║
    ║ Lv 10-20      ║       ║    Lv 5-10            ║
    ║ 🏛️ Temple      ║       ║    🏠 Inn  🌳 Oak      ║
    ╚═══╦═══════════╝       ╚═══╦═══════════════════╝
        ║ [Swimming]            ║
        ║                       ║ [Tree Cut]
        ║   ┌───────────────────╨───────────┐
        ║   │    Well of Worlds             │
        ╚═══╡    (Underground Connection)   ╞═══════╗
            └───────────┬───────────────────┘       ║
                        ║                           ║
                        ║ [Rock Smash]              ║
                        ║                           ║
            ╔═══════════╩═══════════════╗   ╔═══════╩═════════╗
            ║  UNDERGROUND DEPTHS       ║   ║ BURNING WASTES   ║
            ║  ⛏️ Earth/Beast            ║   ║ 🌋 Fire/Demon     ║
            ║  Lv 15-25 | Earth Gym    ║   ║ Lv 20-30         ║
            ║  💎 Crystal  ⚫ Abyss      ║   ║ 🔥 Volcano 🌋 Gate║
            ╚═══════════╦═══════════════╝   ╚═══════╦══════════╝
                        ║                           ║
                        ║ [Lava Walking]            ║
                        ╚═══════════════╦═══════════╝
                                        ║
                                        ║ [Shadow Walk]
                                        ║
                            ╔═══════════╩═══════════╗
                            ║   SHADOW CRYPTS       ║
                            ║   💀 Undead/Shadow     ║
                            ║   Lv 35-50            ║
                            ║   ⚔️ Elite Four        ║
                            ╚═══════════════════════╝

Legend:
═══ Major Connection (2-way)
─── Secondary Path
[Ability] Required ability
🎮 Landmark
```

## Ability Progression Tree

```
                        START
                          │
                    Choose Starter
                          │
            ┌─────────────┼─────────────┐
            │             │             │
        🌊 MURLOC     🌿 WISP       🔥 IMP
       (Water)      (Nature)      (Fire)
            │             │             │
            └─────────────┴─────────────┘
                          │
                    Early Exploration
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    🌿 TREE CUT      🪨 ROCK SMASH    💡 ILLUMINATE
   (Catch Nature)   (Catch Beast)   (Catch Fire/Spirit)
        │                 │                 │
   Dark Forest      Underground         Dark Caves
   Full Access      Partial Access      Visibility
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                    First Gym Victory
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   🏃 SPRINT         🌊 SWIMMING       🧗 CLIMBING
  (After Badge)   (Evolve Water)    (Catch Dragon)
        │                 │                 │
   Move Faster     Sunken Ruins      Frozen Peaks
                   Full Access         Access
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                    Mid-Game Expansion
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   🌋 LAVA WALK     ❄️ ICE BREAK      💪 STRENGTH
  (Fire Gym)      (Use Fire Move)  (High Level)
        │                 │                 │
  Burning Wastes    Frozen Peaks      Push Puzzles
  Interior Access   100% Access       Everywhere
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                    Late-Game Abilities
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   👻 SHADOW WALK    🧠 TELEKINESIS    🦅 FLIGHT
  (Shadow-type)     (Psychic-type)   (Dragon/Phoenix)
        │                 │                 │
  Shadow Crypts    Remote Puzzles    Sky Areas
   Endgame Zone    Advanced Secrets  Fast Travel
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                    100% World Access
                          │
                    Secret Hunting
```

## Zone Layout Examples

### Goldshire (Central Hub) - 40x40 Tiles

```
    0         10        20        30        40
  0 ████████████████ NORTH ████████████████
    ██                  ↑                 ██
    ██  🌳              ║              🌳 ██
    ██     🌳    [To Dark Forest]   🌳    ██
 10 ██  🌳      🌳      ║      🌳      🌳  ██
    ██═════════════════╬═════════════════██
    ██                 ║                 ██
    ██  🏠  🏠         🌳         🏠  🏠  ██
    ██                 ║                 ██
 20 ══  [To Sunken]  🏠🌳🏠  [To Wastes] ══
    ═W     Ruins]      ║        (Cut)    E═
    ██                 ║                 ██
    ██  🏠            🏠            🏠   ██
    ██      🏠    ⚪(Well)    🏠         ██
 30 ██                 ║                 ██
    ██  ⛪            🏠            ⛪   ██
    ██  (Church)       ║        (Shop)  ██
    ██═════════════════╬═════════════════██
    ██                 ↓                 ██
 40 ████████████ [Underground] ███████████
                     (Smash)

Legend:
██ = Walls/Trees      ⚪ = Well (Swimming access)
🏠 = Buildings        ⛪ = Special buildings
🌳 = Decorative       ═ = Paths/Roads
↑↓ = Zone exits       (Text) = Requirements
```

### Underground Depths - Cross-Section View

```
   SURFACE LEVEL (Multiple Zone Connections)
         ↓         ↓         ↓         ↓
    Goldshire  Dark Forest  Ruins   Wastes
         ║         ║         ║         ║
   ══════╩═════════╩═════════╩═════════╩═══════
         │                              │
   UPPER CAVES (Easy, Lv 15-20)        │
         │   ⛏️ Kobold Mines            │
         │   💎 Crystal Caverns         │
         │                              │
   ══════╪══════════════════════════════╪═══════
         │                              │
   MIDDLE LAYER (Medium, Lv 20-25)     │
         │   🏛️ Earth Gym               │
         │   🌊 Underground Lake         │
         │                              │
   ══════╪══════════════════════════════╪═══════
         │                              │
   DEEP CAVES (Hard, Lv 25-30)         │
         │   ⚫ The Abyss                │
         │   🌋 Lava Tubes (to Wastes)  │
         │                              │
   ══════╧══════════════════════════════╧═══════
         ↓
   [Shadow Walk Required]
         ↓
   SHADOW CRYPTS ENTRANCE
```

## Ability Gate Visual Language

```
🌳 TREE GATE           🪨 ROCK GATE          🌊 WATER BARRIER
┌─────────┐            ┌─────────┐           ┌─────────┐
│ 🌳 🌳 🌳 │            │  ███    │           │ ≈≈≈≈≈≈≈ │
│🌳 🌳 🌳🌳│            │ █████   │           │≈≈≈≈≈≈≈≈ │
│ 🌳 🌳 🌳 │            │  ███    │           │ ≈≈≈≈≈≈≈ │
└─────────┘            └─────────┘           └─────────┘
 Tree Cut              Rock Smash             Swimming
 Required              Required               Required

🌋 LAVA FLOW          ❄️ ICE WALL            👻 SHADOW GATE
┌─────────┐            ┌─────────┐           ┌─────────┐
│ ▓▓▓▓▓▓▓ │            │ ▒▒▒▒▒▒▒ │           │░░░░░░░░ │
│▓▓▓▓▓▓▓▓ │            │▒▒▒▒▒▒▒▒ │           │░░░░░░░░░│
│ ▓▓▓▓▓▓▓ │            │ ▒▒▒▒▒▒▒ │           │░░░░░░░░ │
└─────────┘            └─────────┘           └─────────┘
Lava Walking           Ice Breaking          Shadow Walk
Required               Required              Required
```

## Secret Location Markers

```
HIDDEN WALL                BREAKABLE FLOOR         SECRET SWITCH
┌───────────┐             ┌───────────┐            ┌───────────┐
│ ████████  │             │           │            │     ·     │
│ ████████  │   ← Looks  │   ····    │  ← Tiny   │           │
│ ███████   │     normal │   ····    │    cracks │     □     │
│ ████████  │     but... │           │            │           │
└───────────┘             └───────────┘            └───────────┘
Walk through!             Rock Smash below        Push to reveal

INVISIBLE PLATFORM        HIDDEN LEVER            WARP SHRINE
┌───────────┐             ┌───────────┐            ┌───────────┐
│           │             │           │            │           │
│     ?     │  ← Only    │  🌿│🌿    │  ← Behind │     ✨    │
│           │    visible │  🌿│🌿    │    vines  │    ╱│╲    │
│           │    with    │    │      │            │   ╱ │ ╲   │
└───────────┘    light   └───────────┘            └───────────┘
Illuminate needed         Tree Cut needed          Activated!
```

## Platforming Elements

```
JUMPING GAPS              CLIMBING WALLS          MOVING PLATFORMS
     ┌──┐                      │││                  ┌───┐
→ → →│  │                      │││                  │   │ ↓
     └──┘                      │││                  └───┘
 ░░       ░░                   │P│                 ░░   ░░
Press A   Land                 │││                Platform
                               │││                Moving

ICE SLIDING               CRUMBLING PLATFORMS      VINE SWINGING
┌────────────┐           ┌─────────────┐          ~~~│~~~
│  ≈≈≈≈≈≈≈≈  │           │    [▓▓▓]    │           ~~│~~
│ P → → → ■  │           │  2 seconds  │            ~│~
│  ≈≈≈≈≈≈≈≈  │           │  then fall  │             P
└────────────┘           └─────────────┘         Swing across!
Slide until hit          Move quickly!
```

## Environmental Hazards

```
LAVA FLOOR                POISON PLANTS           SHADOW DAMAGE
▓▓▓▓▓▓▓▓▓▓▓              🍃🍃🍃🍃🍃                ░░░░░░░░░░░
▓▓ 🔥 ▓▓ 🔥 ▓             🍃💀🍃💀🍃               ░░ 💀 ░░ 💀 ░
▓▓▓▓▓▓▓▓▓▓▓              🍃🍃🍃🍃🍃                ░░░░░░░░░░░
15 HP/sec                 5 HP/sec                20 HP/sec
Need Lava Walk            Need Nature-type        Need Shadow-type

FALLING ROCKS             ICE SLIPPERY            DROWNING
    ▼ ▼ ▼                ▒▒▒▒▒▒▒▒▒                ≈≈≈≈≈≈≈≈≈
   ▼ ▼ ▼                 ▒▒▒▒▒▒▒▒▒                ≈≈≈💀≈≈≈
  ▼ ▼ ▼                  ▒▒ P →→→                 ≈≈≈≈≈≈≈≈≈
10 HP damage              Can't stop!              Need Swimming
Move quickly!             Ice puzzles              or instant death
```

## Landmark Icons

```
GYMS                  HEALING                SHOPS
┌─────────┐          ┌─────────┐            ┌─────────┐
│   ⚔️    │          │    +    │            │    💰    │
│  GYM    │          │  ❤️ ❤️   │            │  SHOP   │
└─────────┘          └─────────┘            └─────────┘

WARP SHRINES          LEGENDARY SITES        SECRETS
┌─────────┐          ┌─────────┐            ┌─────────┐
│    ✨   │          │   👑    │            │    ?    │
│   ╱│╲   │          │ LEGEND  │            │  HIDDEN │
└─────────┘          └─────────┘            └─────────┘
```

## Connection Types

```
SURFACE PATH              UNDERGROUND TUNNEL      WARP CONNECTION
Zone A                    Zone A                  Zone A
  │                         │                       │
  ║ Road                    ║ Tunnel                ║
  ║ Always                  ║ Requires              ║
  ║ Open                    ║ Ability               ✨ Instant
  │                         │                       ✨ Teleport
Zone B                    Zone B                  Zone B

ONE-WAY JUMP              HIDDEN PATH             SHORTCUT
Zone A                    Zone A                  Zone A
  │                         │                       │
  ↓ Jump                    ┊ Secret               ═══ After
  ↓ Down                    ┊ Wall                 ═══ Unlock
  X Can't                   ┊ Phase                ═══ Fast!
    return                  │                       │
Zone B                    Zone B                  Zone B
```

## Creature Ability Indicators

```
TREE CUT                  ROCK SMASH              SWIMMING
🌿 Wisp                   🐺 Wolf                 🐸 Murloc
   ↓                         ↓                       ↓
  Can cut                  Can smash                Can swim
  trees                    rocks                    & dive

CLIMBING                  LAVA WALK               SHADOW WALK
🐉 Drake                  🔥 Felguard             👻 Banshee
   ↓                         ↓                       ↓
  Can climb                Protected               Can phase
  walls                    from heat               through shadow

TELEKINESIS               FLIGHT                  ILLUMINATE
🧠 Elemental              🦅 Phoenix              💡 Imp
   ↓                         ↓                       ↓
  Move objects             Fly anywhere            Light up
  remotely                 fast travel             dark areas
```

## Progression Flowchart

```
START
  │
  ▼
Choose Starter ──────────────────┐
  │                              │
  ▼                              ▼
Goldshire                    Tutorial
  │                          Battles
  │                              │
  ├─→ Dark Forest ──→ Tree Cut ──┤
  │                              │
  ├─→ Sunken Ruins (30%) ────────┤
  │                              │
  ├─→ Catch Creatures ───────────┤
  │                              │
  ▼                              ▼
Rock Smash ←──────────────── Exploration
  │
  ▼
Underground Depths ──→ First Gym ──→ Badge 1
  │                                      │
  ▼                                      ▼
Swimming ←────────── Evolve Water-type ──┘
  │
  ▼
Sunken Ruins (100%) ──→ Second Gym ──→ Badge 2
  │
  ▼
Climbing ←────────── Catch Dragon-type
  │
  ▼
Frozen Peaks ──→ Ice Gym ──→ Badge 3
  │                              │
  ├─→ Burning Wastes ─────────────┤
  │                              │
  ▼                              ▼
Lava Walking ←──── Fire Gym ─── Badge 4
  │
  ▼
Volcano Interior ──→ Phoenix ──→ Flight
  │                              │
  ▼                              ▼
Shadow Walk ←───── Shadow-type ──┘
  │
  ▼
Shadow Crypts ──→ Elite Four ──→ Champion
  │
  ▼
Post-Game Secrets ──→ 100% Completion
```

## Backtracking Diagram

```
                    GOLDSHIRE
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    VISIT 1         VISIT 2         VISIT 3
   0 Badges        2 Badges        4 Badges
        │               │               │
   Explore 50%     +Swimming       +Flight
   Basic areas     More zones      Sky access
   Tutorial        Shortcuts       All secrets
        │               │               │
        └───────────────┴───────────────┘
                        │
                 Each visit reveals
                   NEW CONTENT!
```

## Secret Discovery Flow

```
   Walk near secret
         │
         ▼
   Visual/Audio hint?
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
Investigate   Continue
    │        exploring
    ▼
Has required
  ability?
    │
┌───┴───┐
│       │
YES     NO
│       │
▼       ▼
Unlock  Get hint
secret  about
│       requirement
▼       │
Reward! └─→ Remember
           location
```

## Zone Color Coding

```
🟢 GOLDSHIRE        🟣 DARK FOREST      🔵 SUNKEN RUINS
Warm greens         Deep purples        Blues/teals
Peaceful            Mystical            Ancient
Tutorial            Nature focus        Underwater

🟤 UNDERGROUND      🔴 BURNING WASTES   ⚪ FROZEN PEAKS
Browns/grays        Reds/oranges        Whites/blues
Rocky               Volcanic            Icy
Labyrinth           Dangerous           Vertical

⚫ SHADOW CRYPTS
Blacks/purples
Undead
Endgame
```

---

## Quick Visual Reference

### What to Look For While Exploring

✓ **Suspicious walls** - May be hidden passages
✓ **Cracked rocks** - Can be smashed
✓ **Dark trees with X** - Can be cut
✓ **Tiny cracks in floor** - Breakable floor below
✓ **Water reflections** - May lead underwater
✓ **Shadow barriers** - Need Shadow Walk
✓ **Glowing objects** - Interactable
✓ **NPCs facing walls** - Hint at secret there
✓ **Dead ends** - Often hide secrets
✓ **Unusual tile patterns** - Mark hidden switches

### Visual Cues for Abilities Needed

| Visual Cue | Ability Needed |
|------------|---------------|
| 🌳 Dense trees | Tree Cut |
| 🪨 Cracked boulders | Rock Smash |
| 🌊 Deep water | Swimming |
| 🌋 Lava flows | Lava Walking |
| 🧗 Cliff faces | Climbing |
| ❄️ Ice walls | Ice Breaking |
| 👻 Purple barriers | Shadow Walk |
| 💡 Pitch black | Illuminate |
| 🧠 Distant objects | Telekinesis |
| 🦅 Sky platforms | Flight |

---

**File Location**: `/Users/kodyw/Documents/GitHub/localFirstTools3/METROIDVANIA_VISUAL_GUIDE.md`
