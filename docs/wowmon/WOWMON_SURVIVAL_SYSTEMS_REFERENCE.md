# WoWmon Survival - Systems Quick Reference

## 🎮 Core Systems At-a-Glance

### 1. SURVIVAL STATS SYSTEM

```
┌─────────────────────────────────────────────┐
│  HEALTH ❤️                                   │
│  ████████████████████░░░░  85/100           │
│  • Depletion: Combat, starvation, poison    │
│  • Restore: Food, rest, healing             │
│  • Critical: <20 = death risk               │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  HUNGER 🍖                                   │
│  ██████████░░░░░░░░░░  50/100               │
│  • Depletion: 0.5/min passive               │
│  • Restore: Berries +10, Cooked meat +30    │
│  • Critical: <20 = health drain             │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  THIRST 💧                                   │
│  ███████████████░░░░░  75/100               │
│  • Depletion: 0.7/min (faster than hunger)  │
│  • Restore: Clean water +30                 │
│  • Critical: <20 = rapid health loss        │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  ENERGY ⚡                                   │
│  ████████████████████  100/100              │
│  • Depletion: Movement, actions             │
│  • Restore: Rest +50, Sleep +100            │
│  • Critical: <10 = can't perform actions    │
└─────────────────────────────────────────────┘
```

**Survival Tick** (every second):
```javascript
hunger -= 0.008   // 12.5 min to empty
thirst -= 0.012   // 8.3 min to empty

if (hunger < 20) health -= 0.5
if (thirst < 20) health -= 0.8
if (energy < 30) health -= 0.1
```

---

### 2. RESOURCE TIERS

```
TIER 1: BASIC (Everywhere)
┌─────────┬─────────┬─────────┐
│ Wood 🪵 │Stone 🪨 │Fiber 🌾 │
├─────────┼─────────┼─────────┤
│ 99 max  │ 99 max  │ 99 max  │
│ Forest  │Mountain │ Grass   │
│ Tool: ✊│ Tool: ✊│ Tool: ✊│
└─────────┴─────────┴─────────┘

TIER 2: ADVANCED (Specific biomes)
┌──────────┬─────────┬─────────┐
│ Metal ⛏️ │ Hide 🦌 │Berry 🫐 │
├──────────┼─────────┼─────────┤
│ 99 max   │ 50 max  │ 50 max  │
│ Mountain │ Hunting │ Forest  │
│ Tool: ⛏️ │ Tool: 🗡️│ Tool: ✊│
└──────────┴─────────┴─────────┘

TIER 3: RARE (Endgame)
┌──────────┬─────────┬─────────┐
│Crystal💎 │Honey 🍯 │Artifact │
├──────────┼─────────┼─────────┤
│ 20 max   │ 10 max  │ Unique  │
│ Deep Mtn │ W/Bear  │ Ruins   │
│ Tool: ⛏️ │ Tool: 🐻│ Tool: 🔍│
└──────────┴─────────┴─────────┘
```

---

### 3. CRAFTING RECIPE TREE

```
START: Hand Gathering
  │
  ├─> CAMPFIRE 🔥 (5 Wood, 3 Stone)
  │     │
  │     ├─> Cooked Meat 🍖 (1 Raw Meat)
  │     ├─> Cooked Fish 🍣 (1 Raw Fish)
  │     └─> Clean Water 💦 (1 Dirty Water)
  │
  ├─> STONE AXE 🪓 (3 Wood, 5 Stone, 2 Fiber)
  │     └─> +200% wood gathering
  │
  ├─> STONE PICKAXE ⛏️ (3 Wood, 6 Stone, 2 Fiber)
  │     └─> +200% stone/metal gathering
  │
  ├─> SHELTER ⛺ (20 Wood, 15 Fiber)
  │     └─> Sleep, Save, Fast travel
  │
  └─> WORKBENCH 🔨 (25 Wood, 10 Stone)
        │
        ├─> METAL TOOLS (Tier 2)
        │     ├─> Metal Axe ⚒️ (+400% wood)
        │     ├─> Metal Pickaxe ⛏️ (+400% stone)
        │     └─> Metal Sword 🗡️ (20 damage)
        │
        ├─> ADVANCED STRUCTURES (Tier 2)
        │     ├─> Stone House 🏠
        │     ├─> Large Storage 📦
        │     └─> Farm Plot 🌾
        │
        └─> SPECIAL ITEMS
              ├─> Taming Bait 🎣
              ├─> Healing Potion 💊
              └─> Compass 🧭
```

---

### 4. CREATURE COMPARISON MATRIX

| Creature | Icon | Difficulty | Primary Role | Gather Bonus | Combat | Special Ability |
|----------|------|-----------|--------------|--------------|---------|-----------------|
| **Murloc** | 🐸 | ⭐ Easy (30%) | Fisher | Fish +200% | 0.8x ❌ | Deep water swim |
| **Wolf** | 🐺 | ⭐⭐ Medium (50%) | Hunter | Hide +100% | 1.5x ✅ | Track creatures |
| **Raptor** | 🦖 | ⭐⭐ Medium (60%) | Mount | None | 1.3x ✅ | Rideable +50% speed |
| **Wisp** | ✨ | ⭐⭐⭐ Hard (70%) | Utility | None | 0.5x ❌ | Eternal light + heal |
| **Bear** | 🐻 | ⭐⭐⭐ Hard (80%) | Gatherer | Berries +150% | 2.0x ✅✅ | Honey gathering |
| **Treant** | 🌳 | ⭐⭐⭐⭐ Expert (90%) | Automation | Wood +300% | 2.5x ✅✅ | Auto-gather wood |

**Legend**:
- ✅ = Strong combat
- ❌ = Weak combat
- ⭐ = Taming difficulty

**Companion Synergies**:
```
🐸 Murloc + 🌳 Treant = Coastal base (fish + wood)
🐺 Wolf + 🐻 Bear = Hunting base (meat + berries)
✨ Wisp + 🦖 Raptor = Explorer build (light + speed)
🐻 Bear + 🌳 Treant = Resource automation (food + wood)
```

---

### 5. DAY/NIGHT CYCLE

```
24 HOUR CYCLE (24 real minutes)

06:00 ☀️ DAWN
├─ Light increasing
├─ Temperature rising
└─ Best time to start gathering

12:00 ☀️ NOON
├─ Full brightness
├─ Warmest period
└─ +10% gathering speed

18:00 🌙 DUSK
├─ Light decreasing
├─ Predators spawning
└─ Warning to seek shelter

00:00 🌙 MIDNIGHT
├─ 60% screen darkness
├─ Energy drain +100%
├─ Dangerous creatures
└─ Can't tame creatures

SURVIVAL TIPS:
├─ Sleep in shelter to skip night
├─ Campfire provides light (5 tile radius)
├─ Wisp companion = portable light
└─ Don't explore at night (early game)
```

---

### 6. WEATHER SYSTEM

```
WEATHER TYPE WHEEL

        CLEAR ☀️
         / | \
        /  |  \
      /    |    \
    /      |      \
RAIN 🌧️   |      SNOW ❄️
    \      |      /
     \     |     /
      \    |    /
       \   |   /
        \  |  /
       STORM ⛈️
          |
          |
        FOG 🌫️

EFFECTS TABLE:
╔═══════════╦════════════╦════════════╦═════════╗
║  Weather  ║   Speed    ║   Danger   ║  Bonus  ║
╠═══════════╬════════════╬════════════╬═════════╣
║ Clear ☀️  ║   100%     ║    Low     ║ +10% vis║
║ Rain 🌧️   ║    90%     ║   Medium   ║ Farms++║
║ Storm ⛈️  ║    75%     ║    High    ║  None  ║
║ Fog 🌫️    ║    90%     ║   Medium   ║ Rare++ ║
║ Snow ❄️   ║    70%     ║    High    ║ Pretty ║
╚═══════════╩════════════╩════════════╩═════════╝

TEMPERATURE HAZARDS:
  < 0°C: Extreme Cold (-1 HP/min)
0-10°C: Cold (-0.2 HP/min)
10-30°C: Comfortable (no effect)
30-40°C: Hot (+100% thirst drain)
  >40°C: Extreme Heat (-0.5 HP/min)
```

---

### 7. BASE BUILDING CHECKLIST

```
ESSENTIAL STRUCTURES (Priority Order):

[✓] 1. CAMPFIRE 🔥
    Cost: 5 Wood, 3 Stone
    Purpose: Cook food, boil water
    Location: Central base area

[✓] 2. SHELTER ⛺
    Cost: 20 Wood, 15 Fiber
    Purpose: Sleep, save, restore
    Location: Protected area

[✓] 3. STORAGE BOX 📦
    Cost: 15 Wood, 10 Fiber
    Purpose: +20 inventory slots
    Location: Near shelter

[✓] 4. WORKBENCH 🔨
    Cost: 25 Wood, 10 Stone
    Purpose: Advanced crafting
    Location: Near storage

[ ] 5. FARM PLOT 🌱
    Cost: 10 Wood, 20 Fiber
    Purpose: Grow food
    Location: Open area, near water

[ ] 6. FENCE 🚧
    Cost: 5 Wood, 2 Fiber per segment
    Purpose: Base perimeter
    Location: Surrounding base

[ ] 7. WELL 💧
    Cost: 20 Stone, 10 Wood, 5 Metal
    Purpose: Infinite clean water
    Location: Central, accessible

[ ] 8. TAMING PEN 🐾
    Cost: 30 Wood, 15 Fiber, 10 Stone
    Purpose: House companions
    Location: Near shelter

OPTIMAL BASE LAYOUT:

┌─────────────────────────┐
│  🚧🚧🚧🚧🚧🚧🚧🚧🚧  │  🚧 = Fence
│  🚧           🌱🌱🚧  │  🌱 = Farm
│  🚧  ⛺ 📦    🌱🌱🚧  │  ⛺ = Shelter
│  🚧     🔨       🚧  │  📦 = Storage
│  🚧  🔥 💧    🐾🚧  │  🔥 = Campfire
│  🚧           🐾🚧  │  💧 = Well
│  🚧🚧🚧🚧🚧🚧🚧🚧🚧  │  🔨 = Workbench
└─────────────────────────┘  🐾 = Taming Pen
```

---

### 8. TAMING PROCESS FLOWCHART

```
START: Wild Creature Encountered
    ↓
┌───────────────────┐
│ Is creature rare? │
└────────┬──────────┘
         │
    YES ← → NO (easier)
         │
         ↓
┌────────────────────┐
│ Approach Slowly    │←─────┐
│ (Don't run)        │      │
└─────────┬──────────┘      │
          ↓                 │
┌────────────────────┐      │
│ Press E to Start   │      │
│ Taming             │      │
└─────────┬──────────┘      │
          ↓                 │
┌────────────────────┐      │
│ Progress Bar: 0%   │      │
└─────────┬──────────┘      │
          ↓                 │
┌────────────────────┐      │
│ STAY STILL         │      │
│ (+1% per 5 sec)    │      │
└─────────┬──────────┘      │
          ↓                 │
┌────────────────────┐      │
│ Feed Creature:     │      │
│ • Berries: +10%    │      │
│ • Meat: +15%       │      │
│ • Taming Bait: +30%│      │
└─────────┬──────────┘      │
          ↓                 │
┌────────────────────┐      │
│ Progress >= 100%?  │      │
└────────┬───────────┘      │
         │                  │
    YES  │  NO             │
         │   └──────────────┘
         ↓   (Keep feeding)
┌────────────────────┐
│ SUCCESS!           │
│ Creature Tamed     │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ • Name creature    │
│ • Add to party     │
│ • Loyalty: 100     │
│ • Level: 1         │
└────────────────────┘

FAILURE CONDITIONS:
❌ Move >5 tiles away
❌ Attack creature
❌ Other creature attacks
❌ Run out of food
❌ Progress resets to 0%
```

---

### 9. EXPLORATION MAP ZONES

```
WORLD MAP (100x100 tiles)

                NORTH
                  ↑
    ┌─────────────┴─────────────┐
    │                           │
    │  ❄️❄️❄️❄️❄️❄️❄️❄️❄️   │ EXTREME
    │  ❄️⛰️⛰️⛰️⛰️⛰️❄️   │ (Danger: ★★★★)
    │  ❄️⛰️🌲🌲🌲⛰️❄️   │
    │  🌊🌊🌲🏠🌲🌊🌊   │ MID RANGE
W ←─┤  🌊🌲🌲⛺🌲🌲🌊   ├─→ E
E   │  🌊🌲🌲🌲🌲🌊🌊   │ (Danger: ★★)
S   │  🏜️🏜️🌲🌲🌲🏜️🏜️  │
T   │  🏜️🏜️🏜️🏜️🏜️🏜️🏜️  │ OUTER RIM
    │                           │ (Danger: ★★★★★)
    └─────────────┬─────────────┘
                  ↓
                SOUTH

BIOME LEGEND:
⛺ = Starting Area (Safe, tutorial)
🏠 = Ideal Base Locations
🌲 = Forest (Wood, Berries, Wolf)
⛰️ = Mountain (Stone, Metal, Bear)
🌊 = Water (Fish, Murloc)
❄️ = Snow (Crystal, Danger)
🏜️ = Desert (Raptor, Hot)

LOOT QUALITY BY DISTANCE:
0-10 tiles: Common resources
11-30 tiles: Uncommon resources + recipes
31-60 tiles: Rare resources + creatures
61-100 tiles: Legendary + extreme danger
```

---

### 10. PROGRESSION MILESTONES

```
ACHIEVEMENT LADDER

BEGINNER TIER (Days 1-3)
├─ [✓] Light first campfire
├─ [✓] Cook first meal
├─ [✓] Build first shelter
├─ [✓] Craft first tool
├─ [✓] Survive first night
└─ [✓] Tame first companion

APPRENTICE TIER (Days 4-7)
├─ [ ] Build workbench
├─ [ ] Craft metal tools
├─ [ ] Tame 3 companions
├─ [ ] Establish farm
├─ [ ] Build storage system
└─ [ ] Explore 3 biomes

JOURNEYMAN TIER (Days 8-15)
├─ [ ] Tame rare creature (Bear/Wisp)
├─ [ ] Build fortified base
├─ [ ] Unlock all tier 2 recipes
├─ [ ] Discover 5 POIs
├─ [ ] Max level 1 companion
└─ [ ] Survive storm

EXPERT TIER (Days 16-30)
├─ [ ] Tame Treant (hardest)
├─ [ ] Build beacon network
├─ [ ] Craft all items
├─ [ ] Explore entire map
├─ [ ] Self-sustaining base
└─ [ ] 100% recipe discovery

MASTER TIER (Days 30+)
├─ [ ] Perfect base design
├─ [ ] All companions max level
├─ [ ] All achievements unlocked
├─ [ ] All secrets discovered
├─ [ ] Speedrun challenges
└─ [ ] Community showcase

SPEEDRUN CATEGORIES:
⏱️ First Shelter (target: <10 min)
⏱️ First Tame (target: <15 min)
⏱️ All Biomes (target: <2 hours)
⏱️ All Creatures (target: <10 hours)
⏱️ 100% Completion (target: <40 hours)
```

---

### 11. INVENTORY MANAGEMENT

```
STARTING INVENTORY: 20 slots
UPGRADED INVENTORY: 40 slots (with storage)

ORGANIZATION STRATEGY:

QUICK SLOTS (1-5): Most Used
┌─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │
├─────┼─────┼─────┼─────┼─────┤
│ 🍖  │ 💦  │ 🪓  │ ⛏️  │ 🗡️  │
│Food │Water│ Axe │Pick │Weapon│
└─────┴─────┴─────┴─────┴─────┘

MAIN INVENTORY: Categories
┌────────────────────────────────┐
│ RESOURCES (Stack 99):          │
│ [Wood x45] [Stone x32] [Fiber x23]│
│ [Metal x12] [Crystal x3]       │
├────────────────────────────────┤
│ FOOD (Stack 20-50):            │
│ [Berries x15] [Meat x8] [Fish x5]│
│ [Water x10]                    │
├────────────────────────────────┤
│ TOOLS (No stack):              │
│ [Stone Axe 45/50] [Pickaxe 38/50]│
│ [Spear 20/30] [Bow 35/40]     │
├────────────────────────────────┤
│ SPECIAL (Limited):             │
│ [Taming Bait x3] [Potion x1]  │
│ [Compass] [Map]                │
└────────────────────────────────┘

STORAGE BOX: +20 slots
└─ Store overflow resources
└─ Keep spare tools
└─ Food preservation

WEIGHT SYSTEM:
❌ No weight limit (slot-based only)
✅ Stack sizes vary by item type
✅ Tools don't stack (durability tracked)
```

---

### 12. COMPANION LOYALTY SYSTEM

```
LOYALTY SCALE (0-100)

100-80: DEVOTED ❤️❤️❤️
├─ Maximum effectiveness
├─ Instant obedience
├─ Bonus: +10% all stats
└─ Will defend you

79-50: LOYAL ❤️❤️
├─ Normal behavior
├─ Reliable companion
├─ No bonuses/penalties
└─ Stable relationship

49-20: UNCERTAIN ❤️
├─ -25% effectiveness
├─ May ignore commands
├─ Slower responses
└─ Warning signs

19-0: HOSTILE 💔
├─ Will run away
├─ Or become aggressive
├─ Relationship broken
└─ Cannot be recovered

LOYALTY GAINS (+):
┌────────────────────┬────────┐
│ Action             │ Loyalty│
├────────────────────┼────────┤
│ Feed (preferred)   │   +10  │
│ Feed (acceptable)  │    +5  │
│ Use ability        │  +3-8  │
│ Win combat         │  +2-5  │
│ Rest together      │    +5  │
│ Pet/interact       │    +3  │
│ Level up           │   +15  │
└────────────────────┴────────┘

LOYALTY LOSSES (-):
┌────────────────────┬────────┐
│ Action             │ Loyalty│
├────────────────────┼────────┤
│ Daily decay        │  -1-3  │
│ Don't feed         │    -5  │
│ HP reaches 0       │   -20  │
│ Abandon in combat  │   -30  │
│ Ignore for 3 days  │   -10  │
└────────────────────┴────────┘

MAINTENANCE SCHEDULE:
Daily:
  ✓ Feed once (preferred food)
  ✓ Use ability 2-3 times
  ✓ Keep HP above 50%

Weekly:
  ✓ Level up through use
  ✓ Win 5+ encounters
  ✓ Rest together nightly

Result: Maintain 80+ loyalty
```

---

## 🎓 QUICK REFERENCE CHEAT SHEET

```
╔═══════════════════════════════════════════════╗
║          WOWMON SURVIVAL ESSENTIALS           ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  CONTROLS:                                    ║
║    Arrow Keys = Move                          ║
║    I = Inventory  |  C = Craft  |  B = Build ║
║    E = Interact   |  R = Rest   |  S = Save  ║
║    1-5 = Quick slots                          ║
║                                               ║
║  SURVIVAL PRIORITIES:                         ║
║    1. Don't starve (eat every ~10 min)       ║
║    2. Don't dehydrate (drink every ~7 min)   ║
║    3. Maintain energy (rest often)           ║
║    4. Build shelter (save progress)          ║
║    5. Tame companions (easier survival)      ║
║                                               ║
║  FIRST 30 MINUTES:                           ║
║    → Gather: 10 wood, 6 stone, 5 fiber      ║
║    → Craft: Campfire, Stone Axe, Pickaxe    ║
║    → Cook: All food and water                ║
║    → Build: Shelter (20 wood, 15 fiber)     ║
║    → Tame: Murloc (easiest, very useful)    ║
║                                               ║
║  DANGER WARNINGS:                            ║
║    ⚠️ Night = predators (sleep to skip)     ║
║    ⚠️ Storm = seek shelter immediately       ║
║    ⚠️ Low stats = critical health risk       ║
║    ⚠️ Extreme temp = find campfire/shelter   ║
║                                               ║
║  BEST EARLY COMPANIONS:                      ║
║    🐸 Murloc = Fish gathering + swimming    ║
║    🐺 Wolf = Hunting + protection           ║
║    🦖 Raptor = Fast travel + hunting        ║
║                                               ║
║  ESSENTIAL STRUCTURES:                       ║
║    🔥 Campfire (5 wood, 3 stone)            ║
║    ⛺ Shelter (20 wood, 15 fiber)           ║
║    📦 Storage (15 wood, 10 fiber)           ║
║    🔨 Workbench (25 wood, 10 stone)         ║
║                                               ║
║  REMEMBER:                                   ║
║    • Always cook food before eating          ║
║    • Always boil water before drinking       ║
║    • Save often (sleep in shelter)           ║
║    • Feed companions daily                   ║
║    • Stay near base at night (early game)    ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## 📱 Mobile-Specific Tips

```
TOUCH CONTROLS:
├─ Swipe = Move direction
├─ Tap = Interact/Use item
├─ Two-finger tap = Menu
└─ Long press = Context actions

BATTERY OPTIMIZATION:
├─ Lower particle effects (auto)
├─ Reduce animation (auto)
├─ Dim screen slightly
└─ Enable power-saving mode

SCREEN LAYOUT:
├─ Portrait: Compact HUD
├─ Landscape: Full HUD
├─ Virtual buttons: Large targets
└─ Auto-pause on minimize

MOBILE ADVANTAGES:
✓ Play anywhere
✓ Touch-friendly UI
✓ Auto-save on exit
✓ Resume instantly
```

---

## 🏆 FINAL TIPS FOR SUCCESS

1. **Start Small**: Master basic survival before exploring
2. **Plan Ahead**: Always have 2+ days of food/water
3. **Use Companions**: They multiply your capabilities
4. **Build Smart**: Centralized base near resources
5. **Save Often**: Don't lose hours of progress
6. **Experiment**: Try different companion combos
7. **Optimize**: There's always a better way
8. **Have Fun**: Survival is the journey, not the destination

**Most Important**: Don't be afraid to die and learn!

---

## 📚 Documentation Index

- **Full Design Document**: `WOWMON_SURVIVAL_DESIGN.md`
- **Quick Start Guide**: `WOWMON_SURVIVAL_QUICKSTART.md`
- **Comparison to Original**: `WOWMON_SURVIVAL_COMPARISON.md`
- **This Reference**: `WOWMON_SURVIVAL_SYSTEMS_REFERENCE.md`

**Play the Game**: `wowMon-survival.html`