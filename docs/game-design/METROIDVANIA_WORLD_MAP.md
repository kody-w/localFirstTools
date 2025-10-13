# WoWmon Metroidvania - World Map & Connections

## ASCII World Map

```
                    ╔═══════════════════╗
                    ║  FROZEN PEAKS     ║
                    ║  [ICE/DRAGON]     ║
                    ║  Lv 25-35         ║
                    ╚═════════╦═════════╝
                              ║
                    ┌─────────╨─────────┐
                    │   Mountain Pass   │
                    │   (Climbing Req)  │
                    └─────────┬─────────┘
                              │
          ╔═══════════════════╩═══════════════════╗
          ║        DARK FOREST                    ║
          ║        [NATURE/SPIRIT]                ║
          ║        Lv 5-15                        ║
          ╚═══════════════╦═══════════════════════╝
                          ║
    ╔═══════════╗         ║         ╔═══════════════╗
    ║ SUNKEN    ║         ║         ║ BURNING       ║
    ║ RUINS     ╠═════╗   ║   ╔═════╣ WASTES        ║
    ║ [WATER]   ║     ║   ║   ║     ║ [FIRE/DEMON]  ║
    ║ Lv 10-20  ║     ║   ║   ║     ║ Lv 20-30      ║
    ╚═══╦═══════╝     ║   ║   ║     ╚═══════╦═══════╝
        ║             ║   ║   ║             ║
        ║   ┌─────────┴───╨───┴─────────┐   ║
        ║   │                           │   ║
        ╚═══╣      GOLDSHIRE (HUB)      ╠═══╝
            │      Lv 5-10              │
            │   ┌───────────────────┐   │
            └───┤   Well of Worlds  ├───┘
                └──────────┬────────┘
                           │ (Underground)
                ╔══════════╩══════════╗
                ║  UNDERGROUND        ║
                ║  DEPTHS             ║
                ║  [EARTH/BEAST]      ║
                ║  Lv 15-25           ║
                ╚══════════╦══════════╝
                           ║
                           ║ (Shadow Walk Required)
                           ║
                ╔══════════╩══════════╗
                ║  SHADOW CRYPTS      ║
                ║  [UNDEAD/SHADOW]    ║
                ║  Lv 35-50           ║
                ╚═════════════════════╝
```

## Zone Connection Matrix

| From Zone          | To Zone            | Path Type      | Requirement      | Two-Way? |
|--------------------|--------------------|----------------|------------------|----------|
| Goldshire          | Dark Forest        | Surface        | None             | Yes      |
| Goldshire          | Sunken Ruins       | Surface        | None             | Yes      |
| Goldshire          | Burning Wastes     | Surface        | Tree Cut         | Yes      |
| Goldshire          | Underground Depths | Well/Stairs    | None (partial)   | Yes      |
| Goldshire          | Shadow Crypts      | Hidden Stairs  | Shadow Walk      | Yes      |
| Dark Forest        | Frozen Peaks       | Mountain Pass  | Climbing         | Yes      |
| Dark Forest        | Underground Depths | Hollow Tree    | Rock Smash       | Yes      |
| Dark Forest        | Burning Wastes     | Hidden Cave    | Tree Cut         | Yes      |
| Sunken Ruins       | Underground Depths | Underwater     | Swimming         | Yes      |
| Sunken Ruins       | Goldshire          | Well           | Swimming         | Yes      |
| Burning Wastes     | Frozen Peaks       | Cave System    | Lava Walking     | Yes      |
| Burning Wastes     | Underground Depths | Lava Tubes     | Lava Walking     | Yes      |
| Frozen Peaks       | Goldshire          | Avalanche Path | Ice Breaking     | One-way  |
| Underground Depths | All Surface Zones  | Hidden Tunnels | Various          | Yes      |
| Shadow Crypts      | Underground Depths | Stairway       | Shadow Walk      | Yes      |

## Ability-Gated Progression Tree

```
START (Goldshire)
│
├─→ [No Requirements]
│   ├─→ Dark Forest (partial)
│   ├─→ Sunken Ruins (30%)
│   └─→ Underground Depths (entrance only)
│
├─→ [Tree Cut] ← Catch Nature-type
│   ├─→ Dark Forest (full access)
│   ├─→ Burning Wastes (entrance)
│   └─→ Secret groves in Goldshire
│
├─→ [Rock Smash] ← Catch Beast/Warrior
│   ├─→ Underground Depths (50%)
│   ├─→ Dark Forest (secret areas)
│   └─→ Mountain pass foundations
│
├─→ [Swimming] ← Evolve Water-type
│   ├─→ Sunken Ruins (100%)
│   ├─→ Underground Lake access
│   ├─→ Goldshire Well descent
│   └─→ Underwater shortcuts
│
├─→ [Climbing] ← Catch Dragon/Flying
│   ├─→ Frozen Peaks (entrance)
│   ├─→ Vertical cave shafts
│   └─→ Cliffside secrets
│
├─→ [Lava Walking] ← Defeat Fire Gym
│   ├─→ Burning Wastes (100%)
│   ├─→ Volcano interior
│   ├─→ Lava caves in Underground
│   └─→ Cave to Frozen Peaks
│
├─→ [Ice Breaking] ← Use Fire moves
│   ├─→ Frozen Peaks (100%)
│   ├─→ Ice cave secrets
│   └─→ Avalanche shortcut
│
├─→ [Shadow Walk] ← Catch Shadow-type
│   ├─→ Shadow Crypts (entrance)
│   ├─→ Void realm passages
│   └─→ Hidden shadow doors everywhere
│
├─→ [Telekinesis] ← Catch Psychic/Magic
│   ├─→ Remote puzzle solutions
│   ├─→ Floating platforms
│   └─→ Secret chambers
│
└─→ [Flight] ← Catch Dragon/Phoenix
    ├─→ Sky Islands
    ├─→ Fast travel anywhere
    ├─→ Mountain peaks
    └─→ 100% world access
```

## Landmark Quick Reference

### Goldshire (Hub)
1. **Lion's Pride Inn** (20, 20) - Healing, save point
2. **Great Oak** (25, 15) - Visual landmark, wisdom NPCs
3. **Bone Vault Church** (15, 35) - Shadow Crypts entrance (late)
4. **Well of Worlds** (18, 25) - Swimming access to Underground Lake
5. **Monument Square** (20, 18) - Badge progress indicator

### Dark Forest
1. **Twisted Grove** (30, 30) - Nature Gym
2. **Moonwell Glade** (15, 20) - Wisp encounters, peaceful area
3. **The Hollow** (35, 45) - Giant tree to Underground
4. **Troll Bridge** (25, 10) - Optional boss, rare item
5. **Secret Grove** (5, 5) - Treant guardians, legendary seed

### Sunken Ruins
1. **Drowned Plaza** (30, 30) - Central area, half-submerged
2. **Coral Throne** (10, 50) - Murloc King (secret boss)
3. **Temple of Tides** (30, 45) - Water Gym
4. **Naga Lair** (5, 55) - Deep dive required
5. **Lighthouse** (55, 10) - Puzzle beacon, view entire zone

### Underground Depths
1. **Kobold Mines** (20, 15) - Twisting tunnels, minecart rails
2. **Crystal Caverns** (40, 30) - Beautiful, rare encounters
3. **The Abyss** (30, 40) - Bottomless pit, floating platforms
4. **Forge Chamber** (25, 25) - Earth Gym
5. **Underground Lake** (35, 50) - Hub to Sunken Ruins & Goldshire

### Burning Wastes
1. **Volcano's Maw** (30, 30) - Active lava flows
2. **Demon Gate** (25, 40) - Fire Gym
3. **Scorched Bridge** (40, 20) - Crumbling bridge puzzle
4. **Phoenix Nest** (30, 5) - Top of volcano, legendary
5. **Obsidian Cliffs** (50, 45) - Infernal spawn

### Frozen Peaks
1. **Summit of Kings** (30, 5) - Highest point, dragon lair
2. **Ice Palace** (30, 30) - Ice Gym, sliding puzzles
3. **Avalanche Pass** (40, 40) - Ice Breaking required
4. **Wyvern Roost** (15, 15) - Flying creature area
5. **Frozen Throne** (30, 50) - Secret boss arena

### Shadow Crypts
1. **Necropolis Gate** (30, 5) - Skull entrance
2. **Bone Cathedral** (30, 20) - Shadow Gym
3. **Shadowfell Portal** (15, 30) - Void realm access
4. **Elite Four Chamber** (30, 40) - Four rooms
5. **Throne of Shadows** (30, 55) - Champion battle

## Shortcut Network

### Early Shortcuts (0-2 Badges)
- **Goldshire ↔ Dark Forest**: Main road (always open)
- **Goldshire ↔ Sunken Ruins**: Western path (always open)
- **Dark Forest → Goldshire**: Cut through grove (Tree Cut)

### Mid Shortcuts (2-4 Badges)
- **Underground Lake → Goldshire Well**: Swim up (Swimming)
- **Underground Lake → Sunken Ruins**: Underwater tunnel (Swimming)
- **Burning Wastes → Frozen Peaks**: Lava cave (Lava Walking)
- **Frozen Peaks → Goldshire**: Avalanche slide (Ice Breaking, one-way)

### Late Shortcuts (4+ Badges)
- **Any Warp Shrine → Any Other Shrine**: Fast travel network (Flight)
- **Shadow Crypts → Goldshire Church**: Hidden portal (Shadow Walk)
- **Underground Tunnels**: Connect to all surface zones (Rock Smash + various)

### Warp Shrine Locations
1. Goldshire - Monument Square
2. Dark Forest - Secret Grove
3. Sunken Ruins - Lighthouse
4. Underground Depths - Crystal Caverns
5. Burning Wastes - Obsidian Cliffs
6. Frozen Peaks - Summit of Kings
7. Shadow Crypts - Throne Room
8. Sky Island - Secret 8th shrine (Flight required)

## Exploration Milestones

| Hour | Milestone | Zones Accessible | Abilities | Completion |
|------|-----------|------------------|-----------|------------|
| 0-1  | Tutorial, Starter | Goldshire, Dark Forest (partial) | None | 10% |
| 1-2  | First abilities | +Sunken Ruins, +Underground (partial) | Tree Cut, Rock Smash | 20% |
| 2-3  | First Gym | Dark Forest full, OR Underground full | +Illuminate | 30% |
| 3-5  | Swimming unlocked | Sunken Ruins full, Underground Lake | +Swimming | 50% |
| 5-8  | Mid-game expansion | +Burning Wastes, +Frozen Peaks | +Climbing, +Lava Walk | 70% |
| 8-10 | Late game | +Shadow Crypts, +Sky Islands | +Shadow Walk, +Flight | 85% |
| 10+  | Post-game secrets | All zones, all secrets | All abilities | 100% |

## Secret Locations Guide

### Master-Level Secrets (Require Multiple Abilities)

**Master Soul Stone Location**:
```
Zone: Shadow Crypts
Path: Goldshire Church → Shadow Walk through basement →
      Navigate to Throne Room → Rock Smash hidden wall →
      Flight to upper chamber → Telekinesis to activate switches →
      Master Soul Stone chest revealed
Required: Shadow Walk, Rock Smash, Flight, Telekinesis
```

**Phoenix Encounter**:
```
Zone: Burning Wastes
Path: Enter volcano → Lava Walk to inner sanctum →
      Climb lava walls to summit → Phoenix appears
Required: Lava Walking, Climbing
Reward: Catch Phoenix (enables Flight ability)
```

**Ancient Dragon Lair**:
```
Zone: Frozen Peaks
Path: Ice Palace → Ice Breaking on frozen gate →
      Climb to summit → Enter dragon cave →
      Defeat guardian drakes → Ancient Dragon appears
Required: Ice Breaking, Climbing
Reward: Legendary Dragon (Lv 60)
```

**Murloc King Boss**:
```
Zone: Sunken Ruins
Path: Swim to deepest point → Dive to ocean floor →
      Find Coral Throne → Defeat Murloc Royal Guard →
      Battle Murloc King
Required: Swimming (Dive upgrade)
Reward: King's Crown (boost to Water-types)
```

**Infernal Titan**:
```
Zone: Burning Wastes
Path: Volcano core → Lava Walk to center platform →
      Trigger awakening ritual → Boss battle
Required: Lava Walking, Fire-type in party
Reward: Infernal Heart (mega evolution item)
```

### Hidden Gym Locations

**Sky Gym** (Secret Badge 9):
```
Location: Floating Island above Frozen Peaks
Access: Flight required
Type: Flying/Dragon
Level: 45
Reward: Sky Badge, TM: Aerial Ace
```

**Shadow Gym** (Secret Badge 10):
```
Location: Void Realm (portal in Shadow Crypts)
Access: Shadow Walk + Beat Elite Four
Type: Pure Shadow
Level: 55
Reward: Void Badge, TM: Shadow Realm
```

**Time Gym** (Secret Badge 11):
```
Location: Temporal Pocket (random eclipse event)
Access: All 8 badges + be in right place during eclipse
Type: Psychic/Time
Level: 60
Reward: Time Badge, TM: Temporal Shift
```

## Recommended Progression Routes

### Route A: Nature Path (Balanced)
1. Start → Goldshire → Dark Forest
2. Catch Wisp → Tree Cut unlocked
3. Dark Forest Gym (Badge 1)
4. Cut trees to Burning Wastes → Catch Imp
5. Return → Rock Smash from Gnoll
6. Underground Depths → Earth Gym (Badge 2)
7. Sunken Ruins → Evolve Murloc → Swimming
8. Sunken Ruins Gym (Badge 3)
9. Climbing from Drake → Frozen Peaks
10. Ice Gym (Badge 4) → etc.

### Route B: Water Path (Exploration Focus)
1. Start → Goldshire → Sunken Ruins (30%)
2. Catch Murloc → Train to evolve → Swimming early
3. Full Sunken Ruins access → Water Gym (Badge 1)
4. Underground Lake → Rock Smash from encounter
5. Underground Depths Gym (Badge 2)
6. Dark Forest → Tree Cut → Nature Gym (Badge 3)
7. Burning Wastes → Fire Gym (Badge 4) → etc.

### Route C: Strength Path (Combat Focus)
1. Start → Goldshire → Catch Gnoll → Rock Smash
2. Underground Depths → Earth Gym (Badge 1)
3. Explore dark caves → Catch Shadow creature
4. Return to surface → Dark Forest
5. Catch Wisp → Tree Cut → Nature Gym (Badge 2)
6. Burning Wastes → Fire Gym (Badge 3)
7. Evolve creatures → Swimming/Climbing
8. Sunken Ruins/Frozen Peaks → Badges 4-5 → etc.

### Speedrun Route (Any%)
1. Goldshire → Rock Smash → Underground → Badge 1
2. Underground Lake → Swimming
3. Sunken Ruins → Badge 2
4. Dark Forest → Tree Cut → Badge 3
5. Burning Wastes → Badge 4
6. Sequence break to Shadow Crypts early
7. Elite Four rush

## Environmental Hazards by Zone

| Zone | Hazards | Safe With | Damage |
|------|---------|-----------|--------|
| Dark Forest | Poison plants, thorns | Nature-type in party | 5 HP/sec |
| Sunken Ruins | Drowning (without Swim) | Swimming ability | Instant |
| Underground | Darkness, falling rocks | Illuminate, fast movement | 10 HP |
| Burning Wastes | Lava floors | Lava Walking | 15 HP/sec |
| Frozen Peaks | Slippery ice, falling | Ice Breaking, careful movement | 10 HP |
| Shadow Crypts | Shadow damage, curses | Shadow-type in party | 20 HP/sec |

## NPC Hint System

NPCs give progressively more detailed hints based on badge count:

**0 Badges**:
- "I hear strange noises from the well..."
- "The forest is lovely, but some paths are blocked."

**1-2 Badges**:
- "Swimming opens up the western ruins completely!"
- "Miners say the underground connects to everywhere..."

**3-4 Badges**:
- "Dragons nest at the frozen summit. Be prepared."
- "They say a Phoenix lives in the volcano's heart."

**5-8 Badges**:
- "The church has a dark secret in its basement..."
- "Shrines light up when you've found all of them..."

**Post-Game**:
- "A master stone lies in the deepest shadow..."
- "Time itself bends during celestial events..."

---

**File Location**: `/Users/kodyw/Documents/GitHub/localFirstTools3/METROIDVANIA_WORLD_MAP.md`
