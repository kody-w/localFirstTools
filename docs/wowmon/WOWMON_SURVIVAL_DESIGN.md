# WoWmon Survival - Complete Design Document

## Executive Summary

WoWmon Survival transforms the creature collection game into a comprehensive survival/crafting experience where creatures become companions and tools for surviving in the wilderness of Azeroth. Players must manage resources, craft equipment, build shelter, and tame creatures to overcome environmental challenges.

---

## 1. SURVIVAL MECHANICS

### Core Survival Stats
Players must manage four critical survival statistics:

#### Health (❤️)
- **Range**: 0-100
- **Purpose**: Primary life force
- **Depletion Causes**:
  - Combat with wild creatures
  - Eating raw/poisoned food
  - Extreme weather exposure
  - Starvation/dehydration
- **Restoration Methods**:
  - Eating cooked food
  - Resting in shelter
  - Healing items
  - Companion abilities (Wisp healing)

#### Hunger (🍖)
- **Range**: 0-100
- **Depletion Rate**: ~0.5 per minute
- **Critical Threshold**: Below 20 triggers health damage
- **Restoration Methods**:
  - Eating berries (+10)
  - Cooked meat (+30)
  - Cooked fish (+25)
  - Mushrooms (+8)
- **Effects When Low**:
  - Energy regeneration stops
  - Movement speed reduced
  - Health slowly decreases

#### Thirst (💧)
- **Range**: 0-100
- **Depletion Rate**: ~0.7 per minute (faster than hunger)
- **Critical Threshold**: Below 20 causes rapid health loss
- **Restoration Methods**:
  - Dirty water (+10, -3 health)
  - Clean water (+30, safe)
  - Found in water biomes
- **Effects When Low**:
  - All stats regenerate slower
  - Vision slightly blurred (visual effect)
  - Severe penalties below 10

#### Energy (⚡)
- **Range**: 0-100
- **Depletion Causes**:
  - Movement (-0.1 per step)
  - Gathering resources (-2-5 per action)
  - Crafting (-5-10 per item)
  - Combat actions
- **Restoration Methods**:
  - Resting (+50, advances 2 hours)
  - Eating mushrooms (+5)
  - Sleeping in shelter (full restore)
- **Effects When Low**:
  - Cannot sprint
  - Cannot perform heavy tasks
  - Actions take longer

### Survival Degradation System
```javascript
// Continuous passive degradation
Every game tick (~1 second):
  hunger -= 0.008 (100 in ~12.5 minutes real time)
  thirst -= 0.012 (100 in ~8 minutes real time)

  if (energy < 30) {
    health -= 0.1
  }

  if (hunger < 20) {
    health -= 0.5
    energy regeneration stopped
  }

  if (thirst < 20) {
    health -= 0.8
    all stats regen halved
  }
```

---

## 2. CRAFTING SYSTEM

### Resource Tiers

#### Tier 1: Basic Resources (Immediately Available)
- **Wood** 🪵
  - Found in: Forest biomes
  - Gathering: Hand gathering (slow) or stone axe (fast)
  - Used for: Basic tools, structures, fuel
  - Stack size: 99

- **Stone** 🪨
  - Found in: Mountain biomes, beaches
  - Gathering: Hand gathering (slow) or stone pickaxe (fast)
  - Used for: Tools, buildings, campfire
  - Stack size: 99

- **Plant Fiber** 🌾
  - Found in: Grass, forest floor
  - Gathering: Hand gathering
  - Used for: Rope, bindings, crafting
  - Stack size: 99

#### Tier 2: Advanced Resources
- **Metal Ore** ⛏️
  - Found in: Deep mountain biomes
  - Requires: Stone pickaxe
  - Used for: Advanced tools, weapons
  - Stack size: 99

- **Animal Hide** 🦌
  - Found from: Hunting wild creatures
  - Requires: Hunting weapon
  - Used for: Clothing, leather armor, bags
  - Stack size: 50

- **Crystal** 💎
  - Found in: Rare mountain deposits
  - Requires: Metal pickaxe
  - Used for: Magic items, taming enhancements
  - Stack size: 20

### Crafting Recipes

#### Basic Tools
```
Stone Axe 🪓
  Materials: 3x Wood, 5x Stone, 2x Fiber
  Effect: +200% wood gathering speed
  Durability: 50 uses
  Unlocked: Start

Stone Pickaxe ⛏️
  Materials: 3x Wood, 6x Stone, 2x Fiber
  Effect: +200% stone/metal gathering speed
  Durability: 50 uses
  Unlocked: Start
```

#### Weapons
```
Wooden Spear 🗡️
  Materials: 5x Wood, 3x Fiber
  Damage: 10
  Durability: 30 uses
  Special: Can be thrown
  Unlocked: Start

Wooden Bow 🏹
  Materials: 8x Wood, 5x Fiber
  Damage: 8
  Range: 5 tiles
  Durability: 40 uses
  Requires: Arrows (crafted separately)
  Unlocked: Craft 5 items
```

#### Food Processing
```
Cooked Meat 🍖
  Materials: 1x Raw Meat
  Effect: +30 hunger, +5 health
  Requires: Campfire nearby
  Unlocked: Build campfire

Cooked Fish 🍣
  Materials: 1x Raw Fish
  Effect: +25 hunger, +3 health
  Requires: Campfire nearby
  Unlocked: Build campfire

Clean Water 💦
  Materials: 1x Dirty Water
  Effect: +30 thirst (safe)
  Requires: Campfire nearby
  Unlocked: Build campfire
```

#### Special Items
```
Taming Bait 🎣
  Materials: 3x Berries, 1x Raw Meat
  Effect: +30% taming progress
  Duration: Instant
  Unlocked: Tame first creature
```

### Crafting Mechanics
- **Discovery System**: Recipes unlock through gameplay milestones
- **Proximity Requirements**: Some recipes require nearby structures (campfire for cooking)
- **Material Consumption**: All materials consumed on craft, even if failed
- **Bulk Crafting**: Hold button to craft multiple (if materials available)
- **Quality Variation**: 10% chance for superior quality (+50% durability/effect)

---

## 3. RESOURCE GATHERING

### Gathering Mechanics

#### Manual Gathering (No Tools)
```
Wood from Trees:
  Base rate: 1-2 per attempt
  Energy cost: 5
  Success chance: 60%
  Time: 3 seconds

Stone from Rocks:
  Base rate: 1 per attempt
  Energy cost: 8
  Success chance: 50%
  Time: 4 seconds

Fiber from Grass:
  Base rate: 1-3 per attempt
  Energy cost: 2
  Success chance: 90%
  Time: 1 second
```

#### Tool-Enhanced Gathering
```
With Stone Axe:
  Wood: 3-5 per attempt (+200%)
  Energy cost: 3 (40% reduction)
  Success chance: 95%
  Time: 1.5 seconds
  Tool durability: -1 per use

With Stone Pickaxe:
  Stone: 2-4 per attempt (+200%)
  Metal: 1-2 per attempt (unavailable without tool)
  Energy cost: 4 (50% reduction)
  Success chance: 95%
  Time: 2 seconds
```

#### Companion-Assisted Gathering
Certain companions provide gathering bonuses:

```
Treant Companion 🌳:
  Wood gathering: +100% yield
  Auto-gather wood in range
  No energy cost reduction

Bear Companion 🐻:
  Berry gathering: +150% yield
  Honey gathering: Enabled
  Foraging radius: +3 tiles

Murloc Companion 🐸:
  Fish gathering: +200% yield
  Can fish in deep water
  Finds rare fish types
```

### Resource Node Distribution

#### Biome Resource Tables
```
Forest Biome:
  Wood: 70% spawn rate, 3-5 per node
  Berries: 40% spawn rate, 2-4 per node
  Fiber: 80% spawn rate, 1-3 per node
  Mushrooms: 15% spawn rate, 1-2 per node

Mountain Biome:
  Stone: 90% spawn rate, 4-6 per node
  Metal Ore: 30% spawn rate, 1-3 per node
  Crystal: 5% spawn rate, 1 per node
  Fiber: 20% spawn rate, 1-2 per node

Water Biome:
  Fish (Raw): 60% spawn rate, 1-2 per attempt
  Dirty Water: 100% availability
  Shellfish: 30% spawn rate, 1-3 per node

Plains/Grass Biome:
  Fiber: 90% spawn rate, 2-4 per node
  Berries: 30% spawn rate, 2-3 per node
  Wood: 20% spawn rate, 2-3 per node
```

#### Respawn Mechanics
- **Node Depletion**: Resources depleted after 3-5 harvests
- **Respawn Time**: 5-10 minutes real time
- **Respawn Rate**: Faster near water, slower in depleted areas
- **Seasonal Variation**: Berries more common in summer, mushrooms in fall

---

## 4. BASE BUILDING

### Structure Categories

#### Essential Structures

**Shelter ⛺**
```
Cost: 20x Wood, 15x Fiber
Size: 3x3 tiles
Functions:
  - Sleep (full energy/health restore)
  - Save game
  - Advance time
  - Weather protection
Upgrades: Can upgrade to wooden house, stone house
```

**Campfire 🔥**
```
Cost: 5x Wood, 3x Stone
Size: 1x1 tile
Functions:
  - Cook raw food
  - Boil water (purify)
  - Light source (night)
  - Warmth (+5°C in radius)
  - Scare away weak predators
Fuel: Requires 1 wood per 10 minutes
```

**Storage Box 📦**
```
Cost: 15x Wood, 10x Fiber
Size: 2x2 tiles
Functions:
  - Store 20 extra inventory slots
  - Preserve food (slower decay)
  - Organize items
Upgrades: Large storage, metal chest
```

#### Production Structures

**Workbench 🔨**
```
Cost: 25x Wood, 10x Stone
Size: 2x2 tiles
Functions:
  - Unlock advanced crafting recipes
  - Repair tools (costs materials)
  - Craft faster (-50% time)
Required for: Metal tools, advanced weapons, armor
```

**Farm Plot 🌱**
```
Cost: 10x Wood, 20x Fiber
Size: 2x2 tiles
Functions:
  - Plant seeds (berries, vegetables)
  - Grow food passively
  - Harvest every 2 days
Yield: 10-15 food items per harvest
Requires: Daily watering, companion maintenance optional
```

**Taming Pen 🚧**
```
Cost: 30x Wood, 15x Fiber, 10x Stone
Size: 5x5 tiles
Functions:
  - Safe area for taming
  - +50% taming speed inside
  - Prevents companion escape
  - Up to 3 companions can live here
```

#### Utility Structures

**Well 💧**
```
Cost: 20x Stone, 10x Wood, 5x Metal
Size: 2x2 tiles
Functions:
  - Infinite clean water source
  - No need to boil water
  - Irrigation for nearby farms
Game-changer: Eliminates thirst management
```

**Fence 🚧**
```
Cost: 5x Wood, 2x Fiber per segment
Size: 1x1 tile (connectable)
Functions:
  - Enclose areas
  - Protect from wild creatures
  - Keep tamed creatures contained
  - Decorative boundaries
```

**Beacon 💡**
```
Cost: 10x Crystal, 15x Metal, 20x Stone
Size: 1x1 tile
Functions:
  - Fast travel point
  - Large light radius
  - Map visibility
  - Attracts rare creatures
Endgame: Enables teleportation network
```

### Base Building Mechanics

#### Placement Rules
- **Proximity Check**: Structures cannot overlap
- **Terrain Requirements**: Some structures require flat ground
- **Foundation System**: Large structures need foundation blocks
- **Snap Grid**: Buildings snap to grid for organization
- **Blueprint Mode**: Preview placement before committing resources

#### Upgrade System
```
Shelter Progression:
  1. Tent (⛺) -> Basic shelter
  2. Wooden Hut (🏠) -> +inventory, +companion slots
  3. Stone House (🏛️) -> Weather-proof, +crafting speed
  4. Fortified Base (🏰) -> Defensive, multiple rooms

Materials scale with tier:
  Tier 2: +50% materials, +100% benefits
  Tier 3: +150% materials, +200% benefits
  Tier 4: +300% materials, +400% benefits
```

#### Base Defense
- **Predator Raids**: Random attacks at night (if no fence)
- **Weather Damage**: Structures take damage from storms
- **Durability System**: Buildings need periodic repair
- **Companion Guards**: Tamed creatures can defend base automatically

---

## 5. DAY/NIGHT CYCLE

### Time System

#### Time Scale
- **Real Time to Game Time**: 1 real minute = 1 game hour
- **Full Day Length**: 24 real minutes
- **Day Start**: 06:00 (sunrise)
- **Night Start**: 18:00 (sunset)

#### Time Periods and Effects

**Dawn (05:00 - 07:00)**
```
Light level: Increasing
Temperature: Cool (10-15°C)
Creature activity: Low
Resource gathering: Normal
Special: Dew provides +10% water from plants
```

**Morning (07:00 - 12:00)**
```
Light level: Bright
Temperature: Mild (15-22°C)
Creature activity: High
Resource gathering: +10% yield
Special: Best time for exploration
```

**Afternoon (12:00 - 18:00)**
```
Light level: Bright
Temperature: Warm (22-28°C)
Creature activity: Moderate
Resource gathering: Normal
Special: Increased thirst consumption
```

**Dusk (18:00 - 20:00)**
```
Light level: Decreasing
Temperature: Cool (15-20°C)
Creature activity: High
Resource gathering: -10% yield
Special: Predators become active
```

**Night (20:00 - 05:00)**
```
Light level: Dark (60% screen darkness)
Temperature: Cold (5-10°C)
Creature activity: Predators only
Resource gathering: -50% yield (visibility)
Special:
  - Dangerous predators spawn
  - Energy drains faster (-0.3 per tick)
  - Must have light source or risk getting lost
  - Taming impossible
```

### Day Advancement
- **Natural**: Time passes in real-time
- **Rest Action**: Skip 2 hours, restore energy
- **Sleep in Shelter**: Skip to next morning (06:00), full restore

---

## 6. ENVIRONMENTAL HAZARDS

### Weather System

#### Weather Types and Effects

**Clear ☀️**
```
Probability: 50%
Duration: 30-60 minutes
Effects:
  - Ideal conditions
  - Normal stat consumption
  - +10% visibility
  - Optimal gathering
Temperature: Baseline (20-25°C)
```

**Rain 🌧️**
```
Probability: 25%
Duration: 15-30 minutes
Effects:
  - Movement speed -10%
  - Thirst consumption -50% (can drink rainwater)
  - Fire structures require shelter
  - -20% visibility
  - Muddy terrain (slip chance)
Temperature: -5°C from baseline
Benefits: Farms grow faster, water sources refill
```

**Storm ⛈️**
```
Probability: 10%
Duration: 10-20 minutes
Effects:
  - Movement speed -25%
  - Energy drain +50%
  - Lightning strikes (random damage)
  - Cannot light fires
  - -40% visibility
  - Structures take damage
Temperature: -10°C from baseline
Warning: Seek shelter immediately
```

**Fog 🌫️**
```
Probability: 10%
Duration: 20-40 minutes
Effects:
  - Visibility -60%
  - Easy to get lost
  - Creatures harder to detect
  - +20% rare creature spawns
Temperature: Normal
Strategy: Use landmarks or stay in place
```

**Snow ❄️**
```
Probability: 5% (increased in mountains)
Duration: 30-60 minutes
Effects:
  - Movement speed -30%
  - Health drain -0.5 per minute (without warm clothing)
  - Water freezes (no gathering)
  - Footprints leave trail
  - Beautiful aesthetics
Temperature: -15°C from baseline
Survival: Requires campfire or shelter nearby
```

### Temperature System

#### Temperature Ranges and Effects
```
Extreme Cold (<0°C):
  - Health: -1.0 per minute
  - Energy: -0.5 per minute
  - Hunger: +50% consumption (body heat)
  - Movement: -40% speed
  - Remedy: Campfire, warm clothing, shelter

Cold (0-10°C):
  - Health: -0.2 per minute
  - Energy: -0.2 per minute
  - Hunger: +20% consumption
  - Movement: -10% speed

Comfortable (10-30°C):
  - No penalties
  - Optimal performance

Hot (30-40°C):
  - Thirst: +100% consumption
  - Energy: -0.3 per minute
  - Movement: -15% speed
  - Remedy: Shade, water, light clothing

Extreme Heat (>40°C):
  - Thirst: +200% consumption
  - Health: -0.5 per minute
  - Energy: -0.8 per minute
  - Movement: -30% speed
  - Remedy: Shelter, constant water intake
```

### Terrain Hazards

**Cliffs and Falls**
```
Fall Damage:
  1 tile: 0 damage
  2 tiles: 10 damage
  3 tiles: 25 damage
  4+ tiles: 50 damage (likely fatal)
Prevention: Careful movement, ropes (crafted item)
```

**Deep Water**
```
Without Swimming:
  - Energy drain: 1.0 per second
  - Cannot gather
  - Risk of drowning at 0 energy
With Murloc Companion:
  - Energy drain: 0.2 per second
  - Can swim indefinitely
  - Fish gathering enabled
```

**Poison Plants**
```
Random Encounters: 5% in forest biomes
Effects:
  - Health: -20 over 60 seconds
  - Movement: -50% for duration
Cure: Antidote (crafted from mushrooms)
```

**Quicksand/Mud**
```
Found: Desert and rain-affected areas
Effects:
  - Movement: Locked for 5 seconds
  - Energy: -10 per struggle
  - Can sink if energy reaches 0
Escape: Stop moving, wait for timer, or companion rescue
```

---

## 7. CREATURE TAMING

### Taming Mechanics

#### Taming Process
```
1. Encounter Wild Creature
   - Approach slowly (no sudden movements)
   - Check taming difficulty (Easy/Medium/Hard/Expert)

2. Initiate Taming
   - Stand still within 3 tiles
   - Progress bar appears (0-100%)
   - Creature may flee if approached too fast

3. Building Trust
   - Feed appropriate food: +10-30% progress
     * Berries: +10% (herbivores)
     * Raw meat: +15% (carnivores)
     * Taming bait: +30% (all creatures)
   - Stay still: +1% per 5 seconds
   - Pet creature: +5% (close range only)

4. Taming Success
   - Reach 100% progress
   - Creature joins your party
   - Starts at level 1 with full loyalty
   - Can be renamed

5. Taming Failure (progress resets if:)
   - Player moves away (>5 tiles)
   - Player attacks creature
   - Another creature attacks
   - Player runs out of food
```

#### Taming Difficulty Levels

**Easy (30% base requirement)**
- Murloc 🐸
- Rabbit (not in base game yet)
- Small birds

**Medium (50% base requirement)**
- Wolf 🐺
- Raptor 🦖
- Wild boar

**Hard (70% base requirement)**
- Wisp ✨
- Bear 🐻
- Saber cat

**Expert (90% base requirement)**
- Treant 🌳
- Phoenix
- Rare legendary creatures

#### Creature Abilities and Roles

**Murloc 🐸 (Water/Beast)**
```
Taming Difficulty: Easy (30%)
Found: Water biomes, beaches
Primary Role: Fisher and swimmer

Abilities:
  - Fishing Expert: +200% fish yield
  - Deep Dive: Can gather underwater resources
  - Swimming: Player can swim with Murloc active

Gather Bonus: Fish (raw)
Combat: Weak (0.8x damage multiplier)
Utility: High for coastal survival

Loyalty Maintenance:
  - Feed fish: +5 loyalty per day
  - Let it swim daily: +3 loyalty
  - Loyalty decay: -1 per day
```

**Wolf 🐺 (Beast)**
```
Taming Difficulty: Medium (50%)
Found: Forest, plains biomes
Primary Role: Hunter and tracker

Abilities:
  - Tracking: Reveals nearby creatures on map
  - Hunting: +50% damage to wild creatures
  - Guard: Protects player at night
  - Pack Bonus: +10% stats per additional wolf

Gather Bonus: Hide from hunted creatures
Combat: Strong (1.5x damage multiplier)
Utility: Medium - excellent for hunting

Loyalty Maintenance:
  - Feed meat: +10 loyalty
  - Hunt together: +5 loyalty
  - Keep in combat: +3 loyalty
  - Loyalty decay: -2 per day
```

**Wisp ✨ (Magic)**
```
Taming Difficulty: Hard (70%)
Found: Forest, mountain biomes (rare)
Primary Role: Healer and light source

Abilities:
  - Eternal Light: Provides light radius at night (no fuel)
  - Healing Aura: Restores +0.5 health per second
  - Energy Regeneration: +50% energy regen rate
  - Magic Detection: Reveals crystal deposits

Gather Bonus: None
Combat: Weak (0.5x damage)
Utility: Extremely High - quality of life

Loyalty Maintenance:
  - Rest together: +8 loyalty
  - Use healing: +5 loyalty
  - Find crystals: +10 loyalty
  - Loyalty decay: -1 per day
```

**Bear 🐻 (Beast)**
```
Taming Difficulty: Hard (80%)
Found: Forest, mountain biomes
Primary Role: Gatherer and tank

Abilities:
  - Berry Forager: +150% berry yield
  - Honey Hunter: Can gather honey (unique resource)
  - Intimidation: Scares away small predators
  - Tank: +2.0x combat damage, high HP

Gather Bonus: Berries, honey
Combat: Very Strong (2.0x damage multiplier)
Utility: High - gathering and defense

Loyalty Maintenance:
  - Feed berries/honey: +12 loyalty
  - Gather together: +6 loyalty
  - Win combat: +4 loyalty
  - Loyalty decay: -3 per day
```

**Raptor 🦖 (Beast)**
```
Taming Difficulty: Medium (60%)
Found: Plains, desert biomes
Primary Role: Mount and hunter

Abilities:
  - Mounted Speed: +50% movement speed (rideable)
  - Sprint: Can sprint (costs energy)
  - Pursuit Hunter: +80% damage to fleeing creatures
  - Endurance: -50% energy cost for movement

Gather Bonus: None
Combat: Strong (1.3x damage multiplier)
Utility: High - travel and mobility

Loyalty Maintenance:
  - Ride daily: +8 loyalty
  - Feed meat: +10 loyalty
  - Sprint/run: +4 loyalty
  - Loyalty decay: -2 per day
```

**Treant 🌳 (Nature)**
```
Taming Difficulty: Expert (90%)
Found: Deep forest biomes (very rare)
Primary Role: Wood gatherer and guardian

Abilities:
  - Lumber Giant: +300% wood yield, auto-gather nearby
  - Plant Growth: Farms grow 2x faster in range
  - Forest Guardian: +3.0x damage in forest biome
  - Regeneration: Slowly heals over time

Gather Bonus: Wood (massive yield)
Combat: Very Strong (2.5x in forest, 1.5x elsewhere)
Utility: Extreme - resource generation

Loyalty Maintenance:
  - Plant trees: +15 loyalty
  - Gather wood: +8 loyalty
  - Stay in forest: +5 loyalty
  - Loyalty decay: -1 per day (very loyal)
```

### Companion Management

#### Loyalty System
```
Loyalty Range: 0-100
  - 100-80: Maximum benefits, obeys instantly
  - 79-50: Normal behavior
  - 49-20: Reduced effectiveness, may ignore commands
  - 19-0: May run away or become hostile

Loyalty Gains:
  - Feed preferred food: +5-15 per day
  - Use their abilities: +3-8 per use
  - Win battles: +2-5 per victory
  - Rest together: +5 per rest

Loyalty Losses:
  - Ignore/neglect: -1-3 per day
  - Let HP reach 0: -20
  - Abandon in combat: -30
  - Don't feed: -5 per day
```

#### Companion Slots
```
Starting Slots: 2
Unlocks:
  - Build Taming Pen: +1 slot (total: 3)
  - Upgrade to Large Pen: +2 slots (total: 5)
  - Upgrade to Ranch: +3 slots (total: 8)

Active Companion: Only 1 can be active at a time
Switching: Can switch at any time (no cooldown)
Inactive Companions: Remain at base, slow loyalty decay
```

#### Companion Leveling
```
Experience Sources:
  - Using abilities: 10 XP per use
  - Combat: 50 XP per victory
  - Gathering: 5 XP per resource
  - Time together: 1 XP per minute

Level Benefits (per level):
  - +10% effectiveness
  - +5 HP
  - +2% gather speed
  - Unlock new abilities (levels 5, 10, 15, 20)

Max Level: 20
```

---

## 8. EXPLORATION

### World Generation

#### Biome Distribution (100x100 tile world)
```
Starting Area (Center 6x6):
  - Safe zone
  - Grass biome
  - Basic resources
  - No predators

Inner Ring (radius 15 tiles):
  - 30% Forest
  - 30% Plains
  - 20% Water
  - 20% Grass
  - Low danger

Mid Ring (radius 30 tiles):
  - 20% Forest
  - 15% Mountain
  - 15% Desert
  - 20% Water
  - 30% Mixed
  - Medium danger

Outer Ring (radius 45+):
  - 25% Mountain
  - 20% Snow
  - 15% Deep Forest
  - 15% Swamp
  - 25% Extreme terrain
  - High danger
```

### Discovery System

#### Points of Interest
```
Abandoned Camp:
  - Loot: Random tools, food, materials
  - Structure: Can be claimed/rebuilt
  - Frequency: 5-8 per world
  - Loot quality: Scales with distance from spawn

Ancient Ruins:
  - Loot: Rare recipes, crystals, artifacts
  - Danger: Usually guarded by strong creatures
  - Frequency: 2-3 per world
  - Rewards: Unique items and blueprints

Resource Veins:
  - Rich deposits of specific resource
  - 5x normal yield
  - Finite (50-100 harvests)
  - Frequency: 10-15 per world

Creature Nests:
  - High concentration of specific creature type
  - Easier taming (inside nest)
  - Gather unique resources (eggs, feathers)
  - Respawns: Creatures respawn here

Water Springs:
  - Infinite clean water
  - No boiling needed
  - Ideal base location
  - Frequency: 3-5 per world
```

### Exploration Rewards

#### Distance-Based Loot Scaling
```
0-10 tiles from spawn:
  - Common resources
  - Basic recipes
  - Tier 1 materials

11-30 tiles:
  - Uncommon resources
  - Advanced recipes
  - Tier 2 materials
  - Easy-Medium creatures

31-60 tiles:
  - Rare resources
  - Expert recipes
  - Tier 3 materials
  - Hard creatures
  - Better loot quality

61+ tiles:
  - Legendary resources
  - Unique recipes
  - Tier 4 materials (endgame)
  - Expert creatures
  - Massive loot quantities
```

#### Map Markers
```
Player can mark locations:
  - Custom icons
  - Color coding
  - Notes
  - Shared with companions

Auto-marked:
  - Discovered POIs
  - Resource veins
  - Your structures
  - Deaths (waypoint to recover items)
```

### Navigation Tools

**Compass** (Craftable)
```
Materials: 5x Metal, 1x Crystal
Effect: Shows cardinal directions
Display: Always visible in HUD
Unlocks: Map orientation
```

**Map** (Craftable)
```
Materials: 10x Fiber, 5x Hide, 1x Crystal
Effect: Reveals explored areas
Display: Opens full-screen map
Updates: Automatically as you explore
```

**Beacon Network** (Endgame)
```
Build multiple beacons
Creates fast-travel network
Cost per beacon: 10x Crystal, 15x Metal, 20x Stone
Cooldown: 5 minutes between teleports
```

---

## 9. PROGRESSION SYSTEMS

### Early Game (Days 1-5)
```
Goals:
  ✓ Gather basic resources (wood, stone, fiber)
  ✓ Craft stone tools
  ✓ Build campfire
  ✓ Find food and water
  ✓ Build basic shelter
  ✓ Survive first few nights

Challenges:
  - Learning resource locations
  - Managing survival stats
  - Avoiding predators at night
  - Limited inventory space

Key Milestones:
  - First campfire: Unlocks cooking
  - First shelter: Unlocks saving
  - First tool: Faster gathering
  - First tamed creature: Companion bonuses
```

### Mid Game (Days 6-15)
```
Goals:
  ✓ Tame 2-3 creatures
  ✓ Build workbench
  ✓ Craft advanced tools (metal)
  ✓ Establish farm
  ✓ Build storage
  ✓ Explore nearby biomes

Challenges:
  - Resource management
  - Companion loyalty upkeep
  - Weather survival
  - Creature combat

Key Milestones:
  - Workbench: Advanced crafting
  - Farm: Sustainable food
  - Metal tools: High-tier gathering
  - Storage: Inventory management
```

### Late Game (Days 16-30)
```
Goals:
  ✓ Tame rare creatures (Wisp, Treant, Bear)
  ✓ Build fortified base
  ✓ Establish beacon network
  ✓ Explore outer biomes
  ✓ Craft legendary items
  ✓ Complete all recipes

Challenges:
  - Extreme weather
  - Dangerous creatures
  - Resource scarcity in distant biomes
  - Base defense

Key Milestones:
  - Full companion roster
  - Beacon network
  - Self-sustaining base
  - All biomes explored
```

### Endgame (Days 30+)
```
Goals:
  ✓ Perfect base design
  ✓ Max level all companions
  ✓ Collect all rare items
  ✓ Discover all POIs
  ✓ Master all crafting
  ✓ Create efficient farming systems

Challenges:
  - Optimization
  - Rare resource hunting
  - Perfect companion synergies
  - Base aesthetics

Activities:
  - Breeding creatures (future feature)
  - Trading with NPCs (future feature)
  - Boss encounters (future feature)
  - Seasonal events (future feature)
```

---

## 10. DESIGN PHILOSOPHY

### Core Principles

#### 1. Resource Management is Key
Every action has a cost. Players must constantly balance:
- Survival stats (health, hunger, thirst, energy)
- Inventory space (limited slots)
- Tool durability (finite uses)
- Companion loyalty (daily maintenance)
- Time management (day/night cycle)

**Design Intent**: Create meaningful decisions where players must prioritize actions. No autopilot gameplay.

#### 2. Creatures as Tools and Companions
Unlike traditional Pokemon games where creatures are primarily for combat, WoWmon Survival treats creatures as:
- **Gathering assistants**: Increase resource yield
- **Utility providers**: Light, healing, speed, protection
- **Combat support**: But not the primary focus
- **Emotional bonds**: Loyalty system creates attachment

**Design Intent**: Creatures solve problems and enable strategies rather than being collectibles.

#### 3. Building and Progression
The base is the player's home and represents progress:
- **Visual progression**: Small tent → fortified compound
- **Functional upgrades**: Each structure unlocks capabilities
- **Personal expression**: Player-designed layouts
- **Safe haven**: Protection from hazards

**Design Intent**: Create a sense of ownership and permanence. The base is earned, not given.

#### 4. Survival Challenge
The wilderness is hostile but fair:
- **Clear feedback**: Players always know why they're taking damage
- **Multiple solutions**: Various strategies for same problem
- **Learning curve**: Starts accessible, becomes challenging
- **Death is meaningful**: Lose items but can recover

**Design Intent**: Tension without frustration. Players should feel accomplished when surviving, not relieved.

#### 5. Exploration Rewarded
The world encourages curiosity:
- **Distance = reward**: Better loot further from spawn
- **Hidden secrets**: POIs, rare creatures, Easter eggs
- **Biome diversity**: Each area has unique resources
- **Navigation tools**: Players aren't forced to memorize

**Design Intent**: Reward brave explorers without punishing cautious players.

### Player Retention Strategies

#### Short-Term Engagement (Session Goals)
```
0-15 minutes:
  - Gather immediate resources
  - Manage survival stats
  - Small crafting objectives
  - Companion interaction

15-30 minutes:
  - Build one structure
  - Tame one creature
  - Explore new biome
  - Complete crafting project

30-60 minutes:
  - Major base expansion
  - Multi-step crafting chains
  - Companion leveling
  - POI discovery

60+ minutes:
  - Long expeditions
  - Resource stockpiling
  - Base optimization
  - Achievement hunting
```

#### Long-Term Engagement (Multi-Session Goals)
```
Week 1:
  - Establish base
  - Tame first companions
  - Unlock core recipes
  - Survive first week

Week 2:
  - Expand to multiple biomes
  - Build advanced structures
  - Tame rare creatures
  - Master crafting system

Week 3+:
  - Perfect base design
  - Complete creature roster
  - Discover all secrets
  - Optimize systems
  - Create personal challenges
```

### Balance Considerations

#### Difficulty Curve
```
Tutorial Zone (First 30 minutes):
  - Abundant resources nearby
  - No predators
  - Forgiving survival stats
  - Clear objectives

Early Game (Hours 1-3):
  - Resources require travel
  - Weak predators at night
  - Survival stats matter
  - Player-driven goals

Mid Game (Hours 3-10):
  - Resources gated by tools
  - Dangerous creatures
  - Weather challenges
  - Complex crafting chains

Late Game (Hours 10+):
  - Rare resources far away
  - Extreme hazards
  - Min-maxing required
  - Player-created challenges
```

#### Economy Balance
```
Resource Abundance:
  Tier 1 (Wood, Stone, Fiber): Common - 70% spawn
  Tier 2 (Metal, Hide): Uncommon - 30% spawn
  Tier 3 (Crystal, Rare): Rare - 5% spawn

Crafting Costs:
  Basic tools: Affordable (3-6 materials)
  Structures: Significant (15-30 materials)
  Advanced items: Expensive (20-50 materials)
  Endgame: Very expensive (50-100+ materials)

Gathering Rates (per minute):
  Manual: 5-10 resources
  With tools: 15-25 resources
  With companions: 30-50 resources
  Optimal setup: 60-100 resources
```

---

## 11. TECHNICAL IMPLEMENTATION

### Save System
```javascript
Save Data Includes:
  - Player position and stats
  - Inventory and quick slots
  - Companion data (stats, loyalty, levels)
  - Structure positions
  - World state (resource nodes)
  - Time and weather
  - Discovered recipes
  - Explored map areas

Save Triggers:
  - Manual save (button)
  - Sleep in shelter (auto-save)
  - Every 5 minutes (auto-save)
  - Before closing game (if supported)

Storage Method:
  - localStorage (browser)
  - Exportable JSON (backup)
  - Future: Cloud sync
```

### Performance Optimization
```javascript
Rendering:
  - Only render visible tiles (viewport culling)
  - Canvas-based rendering (fast pixel art)
  - Minimal DOM manipulation
  - Batch updates

World Generation:
  - Generate once, store in memory
  - Chunk-based loading (future)
  - Procedural but deterministic
  - Efficient biome algorithms

Resource Management:
  - Object pooling for entities
  - Efficient inventory lookups
  - Minimal array operations
  - Event-driven updates
```

### Mobile Optimization
```
Touch Controls:
  - Swipe for movement
  - Tap for interaction
  - Two-finger for menu
  - Virtual buttons for actions

UI Scaling:
  - Responsive design
  - Larger touch targets
  - Simplified layouts on small screens
  - Portrait/landscape support

Performance:
  - Lower particle effects
  - Reduced animation complexity
  - Efficient rendering pipeline
  - Battery-conscious updates
```

---

## 12. FUTURE EXPANSION IDEAS

### Potential Features (Not Yet Implemented)

#### Advanced Taming
- **Creature Breeding**: Combine companion traits
- **Genetics System**: Pass down stats and abilities
- **Rare Variants**: Shiny/legendary versions
- **Training Minigames**: Improve stats through activities

#### Multiplayer Elements
- **Co-op Mode**: Play with friends
- **Trading System**: Exchange items and companions
- **Shared Bases**: Build together
- **Competitive Events**: Leaderboards and challenges

#### Story Elements
- **NPC Settlements**: Trade, quests, lore
- **Boss Encounters**: Epic creature battles
- **Quest System**: Structured objectives
- **Lore Discoveries**: World history and secrets

#### Seasonal Content
- **Seasonal Events**: Limited-time resources and creatures
- **Holiday Themes**: Special decorations and items
- **Seasonal Weather**: Unique environmental challenges
- **Event Rewards**: Exclusive recipes and companions

#### Advanced Building
- **Multi-Level Structures**: Basements, upper floors
- **Automation Systems**: Auto-crafting, resource collection
- **Decorative Items**: Furniture, banners, trophies
- **Base Sharing**: Export/import base designs

---

## CONCLUSION

WoWmon Survival successfully transforms the creature collection genre into a comprehensive survival/crafting experience. By making creatures functional companions rather than combat tools, and by emphasizing resource management and base building, the game creates a unique niche.

### Key Success Factors:
1. **Balanced survival stats** create constant engagement
2. **Meaningful crafting** with clear progression
3. **Diverse creatures** with unique utility roles
4. **Dynamic environment** with weather and time challenges
5. **Rewarding exploration** through distance-scaled loot
6. **Personal bases** that represent player progress
7. **Accessible early game** with growing complexity
8. **Long-term goals** without forced grinding

### Target Audience:
- Survival game enthusiasts
- Crafting/building fans
- Pokemon/creature collection players
- Casual and hardcore gamers
- Mobile and desktop players

### Estimated Playtime:
- **First shelter**: 15-30 minutes
- **Comfortable survival**: 2-3 hours
- **First rare tame**: 3-5 hours
- **Advanced base**: 8-12 hours
- **Endgame mastery**: 20-40 hours
- **100% completion**: 40-60 hours

**The game provides depth without overwhelming complexity, creating a satisfying loop of gather → craft → build → explore → tame that keeps players engaged for dozens of hours.**