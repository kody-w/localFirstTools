# WoWMon: Roguelike/Roguelite Redesign
## Complete Transformation into "WoWMon: Dungeon Crawl"

---

## Executive Summary

This redesign transforms the linear Pokemon-style WoWMon game into an endlessly replayable roguelike dungeon crawler. Instead of exploring a persistent overworld with trainers and gyms, players embark on procedurally generated dungeon runs where each decision matters, permadeath creates tension, and meta-progression ensures long-term engagement.

**Core Concept:** Descend through the corrupted depths of Azeroth, battling increasingly dangerous creatures, collecting powerful relics, and unlocking new starting creatures for future runs.

---

## 1. PROCEDURAL GENERATION

### Dungeon Structure
```javascript
const DUNGEON_SYSTEM = {
    floors: {
        depth: 1-50,  // Progressive difficulty
        layout: "procedural_rooms",
        rooms_per_floor: 8-15,
        connections: "branching_paths"
    },

    room_types: {
        combat: {
            weight: 50,
            encounter: "wild_creature",
            options: ["standard", "elite", "horde"]
        },
        elite: {
            weight: 15,
            encounter: "mini_boss",
            guaranteed_loot: "rare"
        },
        treasure: {
            weight: 20,
            contents: ["items", "relics", "gold", "creature_eggs"]
        },
        rest: {
            weight: 10,
            effect: "heal_team_50_percent",
            choice: "heal_or_upgrade"
        },
        shop: {
            weight: 15,
            vendor: "mysterious_goblin",
            currency: "soul_shards"
        },
        event: {
            weight: 10,
            types: ["blessing", "curse", "choice", "sacrifice"]
        },
        boss: {
            weight: 1,
            every: 5,  // Floor 5, 10, 15, etc.
            reward: "major_unlock"
        }
    }
}
```

### Encounter Pool System
- **Creature Tiers by Depth:**
  - Floors 1-10: Basic creatures (Murloc, Kobold, Imp, Wisp)
  - Floors 11-20: Mid-tier (Gnoll, Wolf, Ghoul, Spider)
  - Floors 21-30: Advanced (Naga, Treant, Orc Grunt, Whelp)
  - Floors 31-40: Elite (Drake, Abomination, Nerubian, Phoenix)
  - Floors 41-50: Legendary (Dragon, Ancient Wisp, Murloc King)

- **Dynamic Scaling:**
  - Creature level = Floor * 1.5 + variance(±2)
  - Elite creatures: +3 levels, +50% stats
  - Boss creatures: +5 levels, +100% stats, unique abilities

### Loot Generation
```javascript
const LOOT_TABLES = {
    common_items: {
        health_potion: { weight: 40, effect: "heal_50hp" },
        mana_potion: { weight: 30, effect: "restore_10pp" },
        soul_stone: { weight: 20, effect: "capture_creature" },
        revive_scroll: { weight: 10, effect: "revive_50hp" }
    },

    relics: {
        dragon_tooth: {
            rarity: "rare",
            effect: "+15% attack for dragon types",
            stackable: false
        },
        shadow_orb: {
            rarity: "epic",
            effect: "undead creatures gain lifesteal",
            stackable: false
        },
        prismatic_crystal: {
            rarity: "legendary",
            effect: "all elemental damage +25%",
            stackable: false
        }
    },

    creature_eggs: {
        generation: "floor_based",
        quality: {
            common: { weight: 60, iv_range: [0, 50] },
            uncommon: { weight: 25, iv_range: [40, 70] },
            rare: { weight: 12, iv_range: [60, 85] },
            perfect: { weight: 3, iv_range: [85, 100] }
        }
    }
}
```

### Map Hazards & Modifiers
- **Floor Modifiers (Randomly Applied):**
  - "Fog of War" - Limited visibility
  - "Fel Corruption" - Demon creatures +50% stats
  - "Undead Rising" - More undead encounters
  - "Treasure Hunt" - 2x treasure rooms
  - "Elite Zone" - All creatures are elite
  - "Blessed Halls" - 2x rest rooms
  - "Cursed Floor" - All creatures inflict debuffs

---

## 2. PERMADEATH SYSTEM

### Death Mechanics
```javascript
const PERMADEATH = {
    on_defeat: {
        action: "end_run",
        save_meta_progress: true,
        clear_run_data: true,

        consequences: {
            lose_all_creatures: true,
            lose_all_items: true,
            lose_all_relics: true,
            lose_current_gold: true
        },

        preserve: {
            soul_shards: "convert_gold_1_to_10_ratio",
            unlocked_creatures: true,
            unlocked_relics: true,
            achievements: true,
            highest_floor: true,
            total_runs: true
        }
    },

    revival_mechanics: {
        second_chance_relic: {
            effect: "revive_once_per_run",
            rarity: "legendary",
            restore: "50_percent_hp"
        },

        sacrifice_option: {
            trigger: "party_wipe",
            choice: "sacrifice_strongest_creature_to_revive_all",
            cost: "permanent_loss"
        }
    }
}
```

### Run Summary Screen
```
═══════════════════════════════════════
         RUN ENDED - FLOOR 23
═══════════════════════════════════════

PERFORMANCE:
• Floors Cleared: 23
• Creatures Defeated: 127
• Bosses Slain: 4
• Time Survived: 47 minutes
• Damage Dealt: 15,340
• Damage Taken: 8,920

REWARDS EARNED:
✓ Soul Shards: +2,340 (from 12,100 gold)
✓ New Record: Deepest Floor!
✓ Unlocked: Felguard (starter option)
✓ Achievement: "Depth Dweller" (+500 shards)

BEST RUN: Floor 23 (This run!)
TOTAL RUNS: 47
TOTAL SOUL SHARDS: 45,890
═══════════════════════════════════════
```

---

## 3. META-PROGRESSION

### Soul Shard Economy
```javascript
const META_CURRENCY = {
    soul_shards: {
        earned_from: [
            { source: "gold_conversion", rate: "10_gold_to_1_shard" },
            { source: "floor_completion", amount: "floor_number * 10" },
            { source: "boss_kills", amount: "floor_number * 50" },
            { source: "achievements", amount: "varies" }
        ],

        spent_on: [
            "unlock_creatures",
            "unlock_relics",
            "permanent_upgrades",
            "daily_blessings",
            "cosmetic_skins"
        ]
    }
}
```

### Permanent Upgrades (Meta Hub)
```javascript
const META_UPGRADES = {
    starter_upgrades: {
        "Health Blessing I": { cost: 500, effect: "All starters +10 max HP" },
        "Health Blessing II": { cost: 1500, effect: "All starters +20 max HP" },
        "Power Blessing I": { cost: 750, effect: "All starters +5 attack" },
        "Speed Blessing I": { cost: 650, effect: "All starters +5 speed" }
    },

    dungeon_upgrades: {
        "Merchant's Favor": { cost: 2000, effect: "Shops 20% cheaper" },
        "Fortune's Friend": { cost: 2500, effect: "+25% gold from all sources" },
        "Relic Seeker": { cost: 3000, effect: "+10% relic drop rate" },
        "Soul Collector": { cost: 5000, effect: "+50% soul shard gain" }
    },

    survival_upgrades: {
        "Second Wind": { cost: 4000, effect: "Extra rest room per 10 floors" },
        "Battle Hardened": { cost: 3500, effect: "Start runs with +1 HP potion" },
        "Lucky Charm": { cost: 6000, effect: "1 free revive per run" }
    }
}
```

### Creature Unlocking System
```javascript
const CREATURE_UNLOCKS = {
    starters: {
        // Initially only 3 available
        murloc: { unlocked: true, cost: 0 },
        wisp: { unlocked: true, cost: 0 },
        imp: { unlocked: true, cost: 0 },

        // Unlock through progression
        kobold: { cost: 800, requirement: "reach_floor_5" },
        gnoll: { cost: 1200, requirement: "reach_floor_10" },
        wolf: { cost: 1500, requirement: "defeat_20_beasts" },
        ghoul: { cost: 1800, requirement: "defeat_30_undead" },
        elemental: { cost: 2200, requirement: "reach_floor_15" },
        spider: { cost: 2500, requirement: "defeat_50_poison_types" },
        whelp: { cost: 3500, requirement: "defeat_floor_20_boss" },
        orc_grunt: { cost: 4000, requirement: "win_10_runs" },
        naga: { cost: 4500, requirement: "reach_floor_25" },
        phoenix: { cost: 8000, requirement: "reach_floor_35" },
        dragon: { cost: 15000, requirement: "reach_floor_50" }
    },

    evolution_unlocks: {
        // Evolved forms can also be starters once unlocked
        murloc_warrior: { cost: 5000, requirement: "evolve_murloc_10_times" },
        dire_wolf: { cost: 6000, requirement: "evolve_wolf_15_times" },
        abomination: { cost: 7000, requirement: "evolve_ghoul_20_times" }
    }
}
```

### Relic Unlocking
```javascript
const RELIC_UNLOCKS = {
    // Unlocked relics can appear in dungeon runs
    common_relics: [
        { name: "Minor Health Ring", cost: 300, effect: "+50 max HP" },
        { name: "Attack Shard", cost: 400, effect: "+10% attack" },
        { name: "Speed Boots", cost: 350, effect: "+10% speed" }
    ],

    rare_relics: [
        { name: "Lifesteal Fang", cost: 1500, effect: "Heal 10% damage dealt" },
        { name: "Critical Eye", cost: 1800, effect: "+15% crit chance" },
        { name: "Type Mastery Charm", cost: 2000, effect: "Pick type: +30% damage" }
    ],

    epic_relics: [
        { name: "Phoenix Feather", cost: 5000, effect: "Revive once at 50% HP" },
        { name: "Dragon's Hoard", cost: 4500, effect: "+100% gold gain" },
        { name: "Evolution Catalyst", cost: 6000, effect: "Creatures evolve 5 levels earlier" }
    ],

    legendary_relics: [
        { name: "Crown of the Lich King", cost: 15000, effect: "Undead creatures immortal for 1 turn when killed" },
        { name: "Heart of Azeroth", cost: 20000, effect: "All creatures +50% all stats" },
        { name: "Infinity Stone", cost: 25000, effect: "Unlimited PP for all moves" }
    ]
}
```

---

## 4. RUN STRUCTURE

### Run Flow
```
START RUN
    ↓
[1] Select Starter Creature (from unlocked pool)
    ↓
[2] Choose Starting Blessing (3 random options)
    - "Extra HP" / "Find Rare Creature" / "Start with Relic"
    ↓
[3] Enter Floor 1
    ↓
[FLOOR LOOP]
    - View procedural map (8-15 rooms)
    - Choose path through dungeon
    - Face encounters/events
    - Collect loot/creatures
    - Boss every 5 floors
    ↓
[CONTINUE OR ESCAPE]
    - After boss floors, option to "Escape with winnings"
    - Bank soul shards but end run
    - OR continue deeper for more rewards (risk/reward)
    ↓
[DEATH OR VICTORY]
    - Permadeath: Convert gold → soul shards
    - Victory (Floor 50): Massive shard bonus + cosmetic reward
```

### Time Investment
- **Single Floor:** 3-5 minutes
- **To Boss (5 floors):** 15-25 minutes
- **Full Run (Floor 50):** 2-4 hours
- **Quick Run (Floors 1-10):** 30-45 minutes

Perfect for:
- Quick coffee break runs (10 floors)
- Evening gaming session (20-30 floors)
- Weekend deep dive (full run attempt)

---

## 5. RISK/REWARD SYSTEMS

### Banking System
```javascript
const BANKING = {
    escape_points: [
        { floor: 5, bonus: "25% soul shard bonus" },
        { floor: 10, bonus: "50% soul shard bonus" },
        { floor: 15, bonus: "75% soul shard bonus" },
        { floor: 20, bonus: "100% soul shard bonus" },
        { floor: 25, bonus: "150% soul shard bonus" }
    ],

    risk_calculation: {
        continue: "Risk losing everything for greater rewards",
        escape: "Bank current progress and start fresh run"
    }
}
```

### Event Choices
```javascript
const RISKY_EVENTS = {
    demon_altar: {
        choice_1: {
            option: "Sacrifice 30% HP from all creatures",
            reward: "Gain powerful relic"
        },
        choice_2: {
            option: "Decline",
            reward: "Nothing"
        }
    },

    mysterious_egg: {
        choice_1: {
            option: "Hatch immediately",
            reward: "Random creature (50% weak, 40% strong, 10% legendary)"
        },
        choice_2: {
            option: "Save for later",
            reward: "Egg becomes perfect IV creature after 10 floors"
        }
    },

    cursed_shrine: {
        choice_1: {
            option: "Take curse for gold",
            reward: "5000 gold but -20% stats for 5 floors"
        },
        choice_2: {
            option: "Destroy shrine",
            reward: "Remove all curses, gain blessing"
        }
    },

    soul_trade: {
        choice_1: {
            option: "Trade strongest creature",
            reward: "3x legendary relics"
        },
        choice_2: {
            option: "Keep team intact",
            reward: "Nothing"
        }
    }
}
```

### Daily Challenges
```javascript
const DAILY_RUNS = {
    seed: "daily_seed",
    leaderboard: "global_rankings",
    modifiers: [
        "Start at floor 10",
        "All creatures are shiny variants",
        "Triple gold rewards",
        "Relic bonanza (2x relic drops)"
    ],

    rewards: {
        top_10_percent: "1000 bonus soul shards",
        top_1_percent: "5000 bonus soul shards + exclusive relic unlock"
    }
}
```

---

## 6. VARIETY & REPLAYABILITY

### Build Diversity
```javascript
const BUILD_ARCHETYPES = {
    glass_cannon: {
        strategy: "Max attack, ignore defense",
        relics: ["Critical Eye", "Berserker's Rage", "Glass Sword"],
        creatures: ["Imp → Felguard", "Phoenix", "Drake"]
    },

    tank_sustain: {
        strategy: "High HP, healing, outlast enemies",
        relics: ["Lifesteal Fang", "Regeneration Band", "Shield of Azeroth"],
        creatures: ["Treant", "Abomination", "Orc Warlord"]
    },

    speed_blitz: {
        strategy: "Strike first, win fast",
        relics: ["Speed Boots", "First Strike Medal", "Swift Talon"],
        creatures: ["Wisp → Ancient Wisp", "Wolf → Dire Wolf", "Phoenix"]
    },

    type_specialist: {
        strategy: "Focus single type, maximize synergy",
        relics: ["Dragon Tooth", "Undead Mastery", "Elemental Core"],
        creatures: ["All dragon type" or "All undead" or "All elemental"]
    },

    evolution_rush: {
        strategy: "Evolve fast, snowball power",
        relics: ["Evolution Catalyst", "XP Multiplier", "Growth Stone"],
        creatures: ["Murloc → King", "Whelp → Dragon", "Ghoul → Abomination"]
    },

    capture_master: {
        strategy: "Catch everything, build massive roster",
        relics: ["Master Ball Amulet", "Creature Charm", "Vast Storage"],
        creatures: ["Mix of all types for coverage"]
    }
}
```

### Creature Synergies
```javascript
const SYNERGY_SYSTEM = {
    type_bonuses: {
        all_water: "+20% damage in water-based floors",
        all_undead: "Revive once per battle at 1 HP",
        all_dragon: "Shared damage resistance",
        all_demon: "Lifesteal on all attacks"
    },

    evolution_chains: {
        same_family: {
            bonus: "Each evolved form on team +15% stats",
            example: "Murloc + Murloc Warrior + Murloc King"
        }
    },

    creature_combos: {
        phoenix_dragon: "Fire damage +50%",
        ghoul_abomination: "Poison immune, inflict plague",
        wisp_treant: "Nature healing doubled"
    }
}
```

### Random Modifiers
Each run gets 1-3 random modifiers:

```javascript
const RUN_MODIFIERS = {
    positive: [
        "Abundant Loot: 2x item drops",
        "Evolution Surge: Creatures evolve 3 levels earlier",
        "Fortune's Blessing: Start with 5000 gold",
        "Relic Hunter: Guaranteed relic every 3 floors",
        "Mega Evolution: All creatures +1 evolution stage"
    ],

    negative: [
        "Cursed Run: All creatures -10% stats",
        "Scarce Resources: No shops",
        "Permacurse: Dead creatures deleted forever",
        "Boss Rush: Boss every 3 floors instead of 5",
        "Fog of Fate: Can't see room types before entering"
    ],

    chaos: [
        "Random Types: All creatures random type each floor",
        "Level Roulette: Creatures gain/lose random levels each floor",
        "Reverse Scaling: Enemies weaker in later floors",
        "Loot Explosion: Random items appear mid-battle"
    ]
}
```

---

## 7. UNLOCKS & PROGRESSION TIERS

### Achievement System
```javascript
const ACHIEVEMENTS = {
    floor_milestones: [
        { id: "floor_5", name: "Surface Dweller", reward: 500 },
        { id: "floor_10", name: "Into Darkness", reward: 1000 },
        { id: "floor_25", name: "Abyss Walker", reward: 2500 },
        { id: "floor_50", name: "Depth Master", reward: 10000 }
    ],

    combat: [
        { id: "defeat_100", name: "Slayer", reward: 800 },
        { id: "defeat_500", name: "Executioner", reward: 2000 },
        { id: "perfect_boss", name: "Flawless Victory", reward: 1500 }
    ],

    collection: [
        { id: "catch_all_common", name: "Novice Collector", reward: 1000 },
        { id: "catch_all_rare", name: "Expert Collector", reward: 3000 },
        { id: "perfect_iv_creature", name: "Perfectionist", reward: 5000 }
    ],

    special: [
        { id: "no_damage_floor", name: "Untouchable", reward: 2000 },
        { id: "solo_boss", name: "Solo Legend", reward: 3500 },
        { id: "no_relics_run", name: "Purist", reward: 4000 },
        { id: "speed_run_20_floors", name: "Speedrunner", reward: 2500 }
    ]
}
```

### Prestige System (After Floor 50)
```javascript
const PRESTIGE = {
    unlock_condition: "Complete Floor 50",

    benefits: {
        prestige_1: {
            icon: "Bronze Crown",
            bonus: "All runs start at Floor 5 with bonus loot"
        },
        prestige_2: {
            icon: "Silver Crown",
            bonus: "Unlock 'Nightmare Mode' - 2x difficulty, 3x rewards"
        },
        prestige_3: {
            icon: "Gold Crown",
            bonus: "Start with random legendary relic"
        },
        prestige_5: {
            icon: "Diamond Crown",
            bonus: "Unlock 'Endless Mode' - infinite floors with scaling"
        }
    }
}
```

---

## 8. CHALLENGE SCALING

### Difficulty Curve
```javascript
const SCALING = {
    creature_stats: {
        formula: "base_stat * (1 + floor * 0.15)",
        boss_multiplier: 2.0,
        elite_multiplier: 1.5
    },

    encounter_density: {
        floors_1_10: "60% combat, 20% treasure, 20% rest/shop",
        floors_11_25: "70% combat, 15% treasure, 15% rest/shop",
        floors_26_40: "80% combat, 10% treasure, 10% rest/shop",
        floors_41_50: "85% combat, 5% treasure, 10% boss/elite"
    },

    boss_mechanics: {
        floor_5: "Simple tank with high HP",
        floor_10: "Multi-stage fight, changes type mid-battle",
        floor_15: "Summons minions, must defeat adds first",
        floor_20: "Enrage timer, must defeat quickly",
        floor_25: "Environmental hazards, dodge mechanics",
        floor_30: "Clone fight, defeat 3 versions",
        floor_35: "Transformation, becomes stronger when low HP",
        floor_40: "Team battle, 3v3 simultaneous",
        floor_45: "Gauntlet, fight 5 elites in a row",
        floor_50: "FINAL BOSS - Multi-phase nightmare"
    }
}
```

### Dynamic Difficulty
```javascript
const ADAPTIVE_DIFFICULTY = {
    losing_streak: {
        3_losses: "Floors 1-5 slightly easier",
        5_losses: "Extra rest rooms, better shop prices",
        10_losses: "Start with bonus relic"
    },

    winning_streak: {
        3_wins: "Better loot quality",
        5_wins: "Chance for double rewards",
        10_wins: "Unlock 'Legend Mode' - hardcore difficulty"
    }
}
```

---

## 9. TECHNICAL IMPLEMENTATION NOTES

### State Management
```javascript
const RUN_STATE = {
    persistent: {
        soul_shards: 0,
        unlocked_creatures: [],
        unlocked_relics: [],
        meta_upgrades: [],
        achievements: {},
        statistics: {}
    },

    run_specific: {
        current_floor: 1,
        active_team: [],
        inventory: [],
        active_relics: [],
        gold: 0,
        run_modifiers: [],
        seed: "random_or_daily"
    }
}
```

### Procedural Generation Algorithm
```javascript
function generateFloor(floorNumber, seed) {
    const rng = new SeededRandom(seed + floorNumber);

    // Generate room count
    const roomCount = rng.range(8, 15);

    // Determine room types
    const rooms = [];
    for (let i = 0; i < roomCount; i++) {
        rooms.push(selectRoomType(rng, floorNumber));
    }

    // Boss room every 5 floors
    if (floorNumber % 5 === 0) {
        rooms[rooms.length - 1] = { type: 'boss', ...generateBoss(floorNumber) };
    }

    // Create connections (branching paths)
    const connections = generatePaths(rooms, rng);

    return {
        floor: floorNumber,
        rooms,
        connections,
        modifier: selectFloorModifier(rng, floorNumber)
    };
}
```

### Save System
```javascript
const SAVE_STRUCTURE = {
    meta_progress: {
        location: "localStorage.wowmon_meta",
        persist: "always",
        data: "soul_shards, unlocks, upgrades, achievements"
    },

    active_run: {
        location: "localStorage.wowmon_run",
        persist: "until_death",
        data: "floor, team, inventory, relics, seed",
        autosave: "after_each_room"
    },

    cloud_sync: {
        optional: true,
        method: "export_json",
        allows: "cross_device_progression"
    }
}
```

---

## 10. UI/UX CHANGES

### New Screens

#### Meta Hub (Between Runs)
```
╔══════════════════════════════════════════╗
║         CHAMBER OF CHAMPIONS             ║
╠══════════════════════════════════════════╣
║  Soul Shards: 12,450                     ║
║  Best Run: Floor 27                      ║
║  Total Runs: 53                          ║
║                                          ║
║  [START NEW RUN]                         ║
║  [UNLOCK CREATURES]    (15/25 unlocked)  ║
║  [UNLOCK RELICS]       (32/80 unlocked)  ║
║  [PERMANENT UPGRADES]  (8/30 purchased)  ║
║  [DAILY CHALLENGE]     (Rank: #423)      ║
║  [ACHIEVEMENTS]        (47/100)          ║
║  [STATISTICS]                            ║
╚══════════════════════════════════════════╝
```

#### Dungeon Map View
```
        FLOOR 12 - "Fel Corruption"

    [?] ─── [T] ─── [C]
     │               │
    [C] ─── [E] ─── [C] ─── [S]
     │               │
    [C] ─── [R] ─── [?]

    Legend:
    [?] = Unknown    [C] = Combat
    [T] = Treasure   [E] = Elite
    [R] = Rest       [S] = Shop
    [@] = You are here

    Team HP: ████░░ 75%
    Gold: 4,230
```

#### Run Start Selection
```
╔══════════════════════════════════════════╗
║        SELECT YOUR CHAMPION              ║
╠══════════════════════════════════════════╣
║                                          ║
║  [MURLOC]        Water/Beast  Lv.5      ║
║   "Balanced starter with evolution"     ║
║   HP: 45  ATK: 49  DEF: 49  SPD: 45     ║
║                                          ║
║  [DRAGON WHELP]  Dragon      Lv.5 🔒    ║
║   "Ultimate power, late game monster"   ║
║   Unlock: 3,500 shards                  ║
║                                          ║
║  [PHOENIX]       Fire/Spirit Lv.5 🔒    ║
║   "Immortal firebird, revive passive"   ║
║   Unlock: 8,000 shards                  ║
║                                          ║
╚══════════════════════════════════════════╝
```

### In-Run UI Elements

**Top Bar:**
```
Floor: 12    Gold: 4,230    Shards (run): 890    [ESCAPE?]
```

**Team Quick View:**
```
[MURLOC] ████████░░ 80% Lv.18
[GHOUL]  ██████████ 100% Lv.15
[WISP]   ████░░░░░░ 40% Lv.12
```

**Relic Bar:**
```
Active Relics:
[Dragon Tooth] [Lifesteal Fang] [Speed Boots]
```

---

## 11. "ONE MORE RUN" HOOKS

### Psychological Triggers

1. **"Almost There" Syndrome**
   - "You died on Floor 19... Floor 20 has a guaranteed legendary relic!"
   - "Only 500 shards from unlocking Phoenix!"

2. **Variable Rewards**
   - Random starting blessings each run
   - Unpredictable loot quality
   - Procedural surprises

3. **Short & Long Goals**
   - Short: "Reach next boss for big reward"
   - Medium: "Unlock next creature"
   - Long: "Complete Floor 50"

4. **Daily Engagement**
   - Daily challenge with leaderboard
   - Daily free blessing (must log in)
   - Weekly special runs

5. **Near-Miss Design**
   - "Boss had 5% HP left!"
   - "Found legendary relic right before death"
   - "One more floor to escape point"

6. **Mastery Progression**
   - Early runs: Learn mechanics
   - Mid runs: Test strategies
   - Late runs: Perfect execution
   - Endless: True mastery

---

## 12. BALANCE CONSIDERATIONS

### Economy Tuning
```javascript
const ECONOMY_BALANCE = {
    soul_shard_rates: {
        floor_1_10: "~300 shards per run",
        floor_11_20: "~1,500 shards per run",
        floor_21_30: "~4,000 shards per run",
        floor_31_40: "~10,000 shards per run",
        floor_41_50: "~25,000 shards per run"
    },

    unlock_costs: {
        early_creatures: "500-1,500 (2-5 runs)",
        mid_creatures: "2,000-5,000 (5-10 runs)",
        late_creatures: "8,000-15,000 (15-30 runs)",

        meta_upgrades: "500-6,000 per upgrade",
        total_meta_cost: "~150,000 shards for everything"
    },

    grind_prevention: {
        escalating_returns: "Later floors give exponentially more shards",
        skill_rewards: "Better play = more efficiency",
        achievement_bonuses: "One-time shard injections"
    }
}
```

### Power Curve
- **Floors 1-10:** Learn mechanics, build team
- **Floors 11-20:** First real challenges, strategy required
- **Floors 21-30:** Elite optimization needed
- **Floors 31-40:** Master-level play
- **Floors 41-50:** Near-perfect execution required

---

## 13. CONTENT ROADMAP

### Launch Content
- 25 creatures (current roster)
- 50 floors
- 60 relics
- 15 meta upgrades
- 50 achievements
- Daily challenges

### Post-Launch Additions

**Update 1: "New Horizons"**
- +10 new creatures
- +20 new relics
- Endless Mode (post-floor 50)
- Prestige system

**Update 2: "Fel Invasion"**
- Demon-themed expansion
- +8 demon creatures
- Demon-specific relics
- Special demon floors (51-60)

**Update 3: "Undead Scourge"**
- Undead expansion
- +8 undead creatures
- Necromancy mechanics
- Lich King final boss (Floor 100)

**Update 4: "PvP Abyss"**
- Asynchronous PvP
- Ghost run replays
- Tournaments
- Exclusive PvP rewards

---

## 14. CORE LOOP DIAGRAM

```
       ┌─────────────────────┐
       │    META HUB         │
       │  - Spend Shards     │
       │  - Unlock Content   │
       │  - Choose Starter   │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │   START RUN         │
       │  - Select Blessing  │
       │  - Generate Seed    │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │  EXPLORE FLOOR      │
       │  - Choose Path      │
       │  - Face Encounters  │
       │  - Collect Loot     │
       └──────────┬──────────┘
                  │
            ┌─────┴─────┐
            │           │
            ▼           ▼
       ┌────────┐  ┌────────┐
       │ COMBAT │  │ EVENT  │
       │        │  │ CHOICE │
       └───┬────┘  └───┬────┘
           │           │
           └─────┬─────┘
                 │
                 ▼
       ┌─────────────────────┐
       │   REWARD/PROGRESS   │
       │  - Gain Loot        │
       │  - Level Up         │
       │  - Get Creatures    │
       └──────────┬──────────┘
                  │
            ┌─────┴─────┐
            │           │
            ▼           ▼
       ┌─────────┐  ┌──────────┐
       │ VICTORY │  │  DEATH   │
       │ ESCAPE  │  │ PERMADEATH│
       └────┬────┘  └────┬─────┘
            │            │
            └─────┬──────┘
                  │
                  ▼
       ┌─────────────────────┐
       │   RUN SUMMARY       │
       │  - Stats            │
       │  - Convert Gold     │
       │  - Gain Shards      │
       │  - Unlock Progress  │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │  BACK TO META HUB   │
       │  "One more run..."  │
       └─────────────────────┘
```

---

## 15. CONVERSION CHECKLIST

### Code Refactoring Required

**Remove:**
- ❌ Overworld map system
- ❌ Linear trainer progression
- ❌ Badge system (replace with floor milestones)
- ❌ Persistent world state
- ❌ NPC dialogue system
- ❌ Town/city locations

**Add:**
- ✅ Procedural floor generation
- ✅ Room-based navigation
- ✅ Seeded randomness
- ✅ Meta-progression save system
- ✅ Soul shard economy
- ✅ Unlock tree UI
- ✅ Run summary screen
- ✅ Permadeath handler
- ✅ Banking/escape system
- ✅ Event choice system
- ✅ Relic inventory system
- ✅ Daily challenge system

**Modify:**
- 🔄 Battle system (keep core, add relic effects)
- 🔄 Creature system (add IV/quality tiers)
- 🔄 Evolution (keep but add catalyst relics)
- 🔄 Items (consumables for single run only)
- 🔄 Save system (dual save: meta + run)

---

## CONCLUSION

This roguelike redesign transforms WoWMon from a linear Pokemon clone into an endlessly replayable dungeon crawler with:

✅ **Infinite Replayability** - Procedural generation ensures no two runs are the same
✅ **Meaningful Choices** - Risk/reward decisions at every turn
✅ **Meta-Progression** - Soul shards provide long-term goals
✅ **Build Diversity** - Dozens of viable strategies and team compositions
✅ **"One More Run"** - Perfectly tuned hooks for addictive gameplay
✅ **Scalable Content** - Easy to add creatures, relics, floors post-launch
✅ **Local-First** - Everything works offline with optional cloud sync
✅ **Respectful Grind** - Skill-based, not time-gated

**Estimated playtime to "complete":** 100-200 hours (unlock everything)
**Estimated playtime for mastery:** Endless (prestige, daily challenges, PvP)

The core Pokemon-style battle system remains intact, but the context shifts from world exploration to dungeon diving. Players will experience the thrill of building powerful teams, discovering broken relic combos, and pushing deeper into the abyss—knowing that death is permanent but progress is eternal.

**The question changes from "Can I beat the Elite Four?" to "How deep can I go before the darkness claims me?"**

---

*End of Roguelike Redesign Document*
