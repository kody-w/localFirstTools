# AGENT 3: FEATURE-RICH STRATEGY DESIGN
## WowMon Advanced Systems & Comprehensive Feature Set

**Agent Role:** Maximum Functionality & Advanced Features
**Focus:** Depth, Complexity, Power User Support, Completionist Features
**Date:** 2025-10-12

---

## EXECUTIVE SUMMARY

This document presents a comprehensive, feature-rich design for WowMon with THREE major system expansions:

1. **Advanced Team Builder System** - Deep strategy planning with 15+ analytics features
2. **Complex Battle System** - Multi-layered combat with 20+ mechanics
3. **Extended Features Suite** - 10+ additional game systems

**Philosophy:** Provide maximum depth and functionality for power users, completionists, and competitive players while maintaining the Game Boy aesthetic.

---

## PART 1: ADVANCED TEAM BUILDER SYSTEM

### 1.1 Core Team Management

#### Team Slots & Configurations
```javascript
teamBuilder: {
    mainTeam: [6 slots],           // Active battle team
    reserveTeams: [10 teams],       // Named saved teams
    boxStorage: [30 boxes * 30],    // 900 creature storage
    daycare: [2 slots],             // Breeding pairs

    teamPresets: {
        offensive: {},              // Pre-configured templates
        defensive: {},
        balanced: {},
        speedTier: {},
        typeMonoteam: {}
    }
}
```

#### Advanced Team Features
- **Team Templates:** 20+ pre-built team archetypes
- **Auto-Builder:** AI suggests teams based on:
  - Current opponent analysis
  - Gym leader counter-teams
  - Type coverage optimization
  - Stat distribution goals
- **Team Roles:** Assign roles (Sweeper, Tank, Support, Lead, Revenge Killer, Wall)
- **Formation System:** Battle order optimization with position-based bonuses
- **Team Nicknames:** Custom names with emoji support
- **Team Tags:** Categorize teams (PvE, PvP, Story, Farming, Elite Four, etc.)

### 1.2 Synergy Analysis Engine

#### Type Synergy Calculator
```javascript
synergyAnalysis: {
    offensiveCoverage: {
        superEffectiveCount: 0-12,      // How many types you hit for 2x+
        neutralCoverageGaps: [],         // Types with no good coverage
        immunityProblems: [],            // Types that can wall you
        moveTypeDistribution: {},        // Balance of move types
        coverageScore: 0-100             // Overall rating
    },

    defensiveSynergy: {
        sharedWeaknesses: [],            // Dangerous type overlaps (4x+ weak)
        resistanceChain: [],             // Overlapping resistances
        immunities: [],                  // Team immunities
        defensivePivots: [],             // Safe switch-in options
        wallBreakers: [],                // Can break through walls
        defensiveScore: 0-100
    },

    speedTiers: {
        fast: [],                        // 90+ speed creatures
        medium: [],                      // 50-89 speed
        slow: [],                        // <50 speed
        speedControl: bool,              // Do you control speed?
        priorityMoves: count,            // Quick Attack users
        speedTierScore: 0-100
    },

    roleBalance: {
        physicalAttackers: count,
        specialAttackers: count,
        tanks: count,
        supports: count,
        hybrids: count,
        roleScore: 0-100
    }
}
```

#### Combo Detection System
- **Baton Pass Chains:** Identify stat-passing opportunities
- **Weather Teams:** Detect rain/sun/sand/hail synergies
- **Entry Hazard Setup:** Stealth Rock + Spinblocker analysis
- **Volt-Turn Core:** U-turn/Volt Switch momentum teams
- **Trick Room:** Slow speed team viability
- **Dual Screens:** Light Screen + Reflect setups

### 1.3 EV/IV System (Effort Values / Individual Values)

#### Individual Values (IVs)
```javascript
ivSystem: {
    stats: {
        hp: 0-31,
        attack: 0-31,
        defense: 0-31,
        spAttack: 0-31,      // NEW: Split Attack into Physical/Special
        spDefense: 0-31,     // NEW: Split Defense into Physical/Special
        speed: 0-31
    },

    perfectIV: 31,
    inheritanceRates: {
        breeding: 0.5,       // 50% chance to inherit from parent
        withItem: 1.0        // 100% with Destiny Knot
    },

    hiddenPower: {
        type: 'calculated',  // Based on IV combination
        power: 30-70
    }
}
```

#### Effort Values (EVs)
```javascript
evSystem: {
    total: 510,              // Total EVs available
    maxPerStat: 252,         // Max in one stat

    presets: {
        offensive: { atk: 252, spd: 252, hp: 4 },
        defensive: { hp: 252, def: 252, spd: 4 },
        mixed: { hp: 252, atk: 128, def: 128 },
        speedster: { spd: 252, atk: 252, hp: 4 }
    },

    training: {
        wildBattles: { evGain: 1-3 },
        items: {
            proteinPlus: { stat: 'attack', evs: 10 },
            ironTablet: { stat: 'defense', evs: 10 },
            carbos: { stat: 'speed', evs: 10 }
        },
        virusBonus: 2.0      // Pokerus equivalent
    }
}
```

#### Stat Calculator
```javascript
calculateStat(base, level, iv, ev, nature) {
    // HP Formula
    if (stat === 'hp') {
        return Math.floor((2 * base + iv + Math.floor(ev / 4)) * level / 100) + level + 10;
    }

    // Other Stats Formula
    let stat = Math.floor((2 * base + iv + Math.floor(ev / 4)) * level / 100) + 5;
    stat = Math.floor(stat * natureMultiplier); // 0.9, 1.0, or 1.1
    return stat;
}
```

### 1.4 Nature System

#### 25 Natures with Stat Modifications
```javascript
natures: {
    // Neutral Natures (no change)
    hardy: { plus: null, minus: null },
    docile: { plus: null, minus: null },
    serious: { plus: null, minus: null },
    bashful: { plus: null, minus: null },
    quirky: { plus: null, minus: null },

    // Offensive Natures
    lonely: { plus: 'attack', minus: 'defense' },      // +10% Atk, -10% Def
    adamant: { plus: 'attack', minus: 'spAttack' },
    naughty: { plus: 'attack', minus: 'spDefense' },
    brave: { plus: 'attack', minus: 'speed' },

    // Defensive Natures
    bold: { plus: 'defense', minus: 'attack' },
    impish: { plus: 'defense', minus: 'spAttack' },
    lax: { plus: 'defense', minus: 'spDefense' },
    relaxed: { plus: 'defense', minus: 'speed' },

    // Special Attack Natures
    modest: { plus: 'spAttack', minus: 'attack' },
    mild: { plus: 'spAttack', minus: 'defense' },
    rash: { plus: 'spAttack', minus: 'spDefense' },
    quiet: { plus: 'spAttack', minus: 'speed' },

    // Special Defense Natures
    calm: { plus: 'spDefense', minus: 'attack' },
    gentle: { plus: 'spDefense', minus: 'defense' },
    careful: { plus: 'spDefense', minus: 'spAttack' },
    sassy: { plus: 'spDefense', minus: 'speed' },

    // Speed Natures
    timid: { plus: 'speed', minus: 'attack' },
    hasty: { plus: 'speed', minus: 'defense' },
    jolly: { plus: 'speed', minus: 'spAttack' },
    naive: { plus: 'speed', minus: 'spDefense' }
}
```

### 1.5 Advanced Analytics Dashboard

#### Team Stats Display
```javascript
teamAnalytics: {
    // Basic Stats
    averageLevel: number,
    totalBST: number,            // Base Stat Total
    averageBST: number,

    // Coverage Analysis
    offensiveCoverage: {
        chart: [12x12 type effectiveness grid],
        superEffective: [list of types],
        notEffective: [list of types],
        immune: [list of types],
        coveragePercentage: 0-100
    },

    // Defensive Analysis
    defensiveProfile: {
        weaknesses: {
            '4x': [types],       // Stacked weaknesses
            '2x': [types],
            '1x': [types]
        },
        resistances: {
            '0.5x': [types],
            '0.25x': [types],
            '0x': [types]        // Immunities
        },
        neutralMatchups: [types]
    },

    // Speed Distribution
    speedChart: {
        histogram: [speed ranges],
        fastestCreature: {},
        slowestCreature: {},
        averageSpeed: number,
        speedTierBreakpoints: {
            '100+': count,
            '90-99': count,
            '70-89': count,
            '50-69': count,
            '<50': count
        }
    },

    // Move Analysis
    moveDistribution: {
        physical: count,
        special: count,
        status: count,
        sharedMoves: [],         // Moves multiple creatures have
        uniqueMoves: [],         // Rare/unique coverage
        moveTypes: {},           // Type distribution
        priorityMoves: [],
        multiHitMoves: [],
        chargeMoves: []
    },

    // Battle Readiness
    readinessScore: {
        overall: 0-100,
        breakdown: {
            coverage: 0-100,
            defense: 0-100,
            speed: 0-100,
            synergy: 0-100,
            movepool: 0-100
        }
    }
}
```

#### Weakness Calculator
```javascript
calculateTeamWeakness(team, targetType) {
    let weaknessMap = {};

    team.forEach(creature => {
        let multiplier = 1.0;

        creature.types.forEach(type => {
            multiplier *= getTypeEffectiveness(targetType, type);
        });

        if (multiplier > 1) {
            weaknessMap[targetType] = (weaknessMap[targetType] || 0) + multiplier;
        }
    });

    return weaknessMap;
}
```

### 1.6 Team Building Tools

#### Interactive Team Planner
- **Drag & Drop:** Reorder team members
- **Swap Moves:** In-planner moveset editor
- **Level Simulation:** Test team at different level ranges
- **Battle Simulator Preview:** Quick battle test vs preset teams
- **Copy/Paste:** Share team codes (compressed JSON)
- **Export Options:**
  - Text format (Reddit/Discord friendly)
  - Image (team card with stats)
  - CSV (spreadsheet import)
  - QR Code (mobile share)

#### Team Comparison
```javascript
compareTeams(team1, team2) {
    return {
        coverageComparison: {},
        statComparison: {},
        synergyComparison: {},
        matchupPrediction: {
            team1Advantages: [],
            team2Advantages: [],
            neutralMatchups: [],
            predictedWinner: team1 | team2,
            confidence: 0-100
        }
    };
}
```

#### Team Validation
- **Rule Compliance:** Check for duplicate species, banned creatures, etc.
- **Format Checker:** OU, UU, RU tier restrictions
- **Item Clause:** No duplicate held items
- **Mega Clause:** Only one mega evolution per team
- **Legends Clause:** Limit on legendary creatures

### 1.7 Saved Team System

#### Team Storage
```javascript
savedTeams: {
    maxSlots: 50,

    teamData: {
        name: string,
        description: string,
        format: 'singles' | 'doubles' | 'story',
        dateCreated: timestamp,
        lastModified: timestamp,
        wins: number,
        losses: number,
        winRate: percentage,

        creatures: [6],

        tags: [],
        favorite: boolean,

        notes: string,           // Strategy notes

        analytics: {
            typeSpread: {},
            mostUsed: creatureId,
            mvp: creatureId,
            speedDistribution: []
        }
    }
}
```

#### Team Management
- **Folders:** Organize teams by category
- **Search/Filter:** Find teams by type, stats, format
- **Version History:** Revert to previous team versions
- **Import/Export:** Share with community
- **Team Ratings:** Community upvotes/downvotes
- **Team Comments:** Notes and strategy guides

---

## PART 2: COMPLEX BATTLE SYSTEM

### 2.1 Advanced Battle Mechanics

#### Turn Structure
```javascript
battleTurn: {
    phases: [
        'startOfTurn',       // Weather, status effects
        'priorityPhase',     // Quick Attack, Protect
        'speedPhase',        // Normal speed ordering
        'endOfTurn'          // Poison damage, Leech Seed
    ],

    turnCount: number,
    maxTurns: 100,           // Timeout for infinite battles

    turnLog: []              // Full battle history
}
```

#### Speed Calculation & Priority
```javascript
calculateTurnOrder(creature1, creature2, move1, move2) {
    // Priority Bracket System
    let priority1 = move1.priority || 0;
    let priority2 = move2.priority || 0;

    if (priority1 !== priority2) {
        return priority1 > priority2 ? creature1 : creature2;
    }

    // Speed Tiebreaker
    let speed1 = calculateSpeed(creature1);
    let speed2 = calculateSpeed(creature2);

    if (speed1 === speed2) {
        return Math.random() < 0.5 ? creature1 : creature2;
    }

    return speed1 > speed2 ? creature1 : creature2;
}
```

### 2.2 Status Effects System

#### Volatile Status (Battle Only)
```javascript
volatileStatus: {
    confusion: {
        duration: 1-4,
        effect: 'May hit self (40% chance)',
        selfDamage: 'attack / 2'
    },

    flinch: {
        duration: 1,
        effect: 'Cannot move this turn'
    },

    trapped: {
        duration: 2-5,
        effect: 'Cannot switch out',
        damage: 'maxHP / 8 per turn'
    },

    cursed: {
        duration: permanent,
        effect: 'Lose HP each turn',
        damage: 'maxHP / 4'
    },

    seeded: {
        duration: permanent,
        effect: 'Drain HP, heal opponent',
        drain: 'maxHP / 8'
    },

    nightmare: {
        duration: permanent,
        effect: 'Lose HP while asleep',
        damage: 'maxHP / 4'
    },

    identified: {
        duration: permanent,
        effect: 'Cannot evade attacks',
        accuracy: '+∞'
    },

    embargo: {
        duration: 5,
        effect: 'Cannot use items'
    },

    healBlock: {
        duration: 5,
        effect: 'Cannot heal HP'
    }
}
```

#### Permanent Status (Persists)
```javascript
permanentStatus: {
    burn: {
        effect: 'Halve physical attack, lose HP/turn',
        attackMultiplier: 0.5,
        damage: 'maxHP / 16'
    },

    poison: {
        effect: 'Lose HP each turn',
        damage: 'maxHP / 8'
    },

    badlyPoisoned: {
        effect: 'Increasing poison damage',
        damage: 'maxHP / 16 * turnCount'
    },

    paralysis: {
        effect: '50% may not move, quarter speed',
        speedMultiplier: 0.25,
        cannotAct: 0.25
    },

    sleep: {
        duration: 1-3,
        effect: 'Cannot move',
        cannotAct: 1.0
    },

    freeze: {
        duration: permanent,
        effect: 'Cannot move until thawed',
        thawChance: 0.2,        // 20% per turn
        fireMoveThaws: true
    }
}
```

### 2.3 Stat Modification System

#### Stat Stages (-6 to +6)
```javascript
statStages: {
    attack: 0,
    defense: 0,
    spAttack: 0,
    spDefense: 0,
    speed: 0,
    accuracy: 0,
    evasion: 0,

    multipliers: {
        '-6': 2/8,
        '-5': 2/7,
        '-4': 2/6,
        '-3': 2/5,
        '-2': 2/4,
        '-1': 2/3,
        '0': 1.0,
        '+1': 3/2,
        '+2': 4/2,
        '+3': 5/2,
        '+4': 6/2,
        '+5': 7/2,
        '+6': 8/2
    }
}
```

#### Stat-Modifying Moves
```javascript
statMoves: {
    // Single Stat
    swordsDance: { attack: +2 },
    ironDefense: { defense: +2 },
    nastyPlot: { spAttack: +2 },
    amnesia: { spDefense: +2 },
    agility: { speed: +2 },

    // Multi-Stat
    dragonDance: { attack: +1, speed: +1 },
    bulkUp: { attack: +1, defense: +1 },
    calmMind: { spAttack: +1, spDefense: +1 },

    // Enemy Debuffs
    growl: { attack: -1, target: 'enemy' },
    leer: { defense: -1, target: 'enemy' },
    scaryFace: { speed: -2, target: 'enemy' },

    // Self-Debuffs (for power)
    shellSmash: {
        attack: +2,
        spAttack: +2,
        speed: +2,
        defense: -1,
        spDefense: -1
    }
}
```

### 2.4 Weather System

#### Weather Types
```javascript
weather: {
    none: {
        duration: permanent,
        effects: []
    },

    sun: {
        duration: 5,
        effects: [
            { type: 'fire', modifier: 1.5 },
            { type: 'water', modifier: 0.5 },
            { move: 'solarBeam', chargeTime: 0 },
            { move: 'synthesis', healing: 2/3 }
        ]
    },

    rain: {
        duration: 5,
        effects: [
            { type: 'water', modifier: 1.5 },
            { type: 'fire', modifier: 0.5 },
            { move: 'thunder', accuracy: 100 },
            { move: 'hurricane', accuracy: 100 }
        ]
    },

    sandstorm: {
        duration: 5,
        effects: [
            { types: ['earth', 'metal', 'rock'], spDefense: 1.5 },
            { damageNonImmune: 'maxHP / 16' },
            { move: 'shoreUp', healing: 2/3 }
        ]
    },

    hail: {
        duration: 5,
        effects: [
            { type: 'ice', immune: true },
            { damageNonImmune: 'maxHP / 16' },
            { move: 'blizzard', accuracy: 100 }
        ]
    },

    harshSunlight: {
        duration: permanent,
        effects: [
            { type: 'fire', modifier: 1.5 },
            { type: 'water', modifier: 0 },
            { weatherBall: 'fire' }
        ]
    },

    heavyRain: {
        duration: permanent,
        effects: [
            { type: 'water', modifier: 1.5 },
            { type: 'fire', modifier: 0 }
        ]
    }
}
```

### 2.5 Terrain System

#### Battle Terrains
```javascript
terrain: {
    none: {},

    grassyTerrain: {
        duration: 5,
        effects: [
            { type: 'nature', modifier: 1.3, groundedOnly: true },
            { healing: 'maxHP / 16', groundedOnly: true },
            { move: 'earthquake', modifier: 0.5 }
        ]
    },

    electricTerrain: {
        duration: 5,
        effects: [
            { type: 'electric', modifier: 1.3, groundedOnly: true },
            { status: 'sleep', immune: true, groundedOnly: true }
        ]
    },

    mistyTerrain: {
        duration: 5,
        effects: [
            { type: 'dragon', modifier: 0.5, groundedOnly: true },
            { status: 'any', immune: true, groundedOnly: true }
        ]
    },

    psychicTerrain: {
        duration: 5,
        effects: [
            { type: 'magic', modifier: 1.3, groundedOnly: true },
            { priorityMoves: 'blocked', groundedOnly: true }
        ]
    }
}
```

### 2.6 Ability System

#### Hidden Abilities (120+ abilities)
```javascript
abilities: {
    // Stat Modifiers
    intimidate: {
        trigger: 'onSwitchIn',
        effect: 'Lower enemy Attack by 1 stage'
    },

    download: {
        trigger: 'onSwitchIn',
        effect: 'Raise Atk or SpA based on foe\'s lower defense'
    },

    // Type Interactions
    levitate: {
        trigger: 'passive',
        effect: 'Immune to Ground-type moves'
    },

    flashFire: {
        trigger: 'onHitByType',
        type: 'fire',
        effect: 'Absorb Fire moves, boost Fire damage by 1.5x'
    },

    waterAbsorb: {
        trigger: 'onHitByType',
        type: 'water',
        effect: 'Heal 25% HP when hit by Water'
    },

    // Weather Abilities
    drizzle: {
        trigger: 'onSwitchIn',
        effect: 'Summon rain for 5 turns'
    },

    drought: {
        trigger: 'onSwitchIn',
        effect: 'Summon sun for 5 turns'
    },

    sandStream: {
        trigger: 'onSwitchIn',
        effect: 'Summon sandstorm for 5 turns'
    },

    snowWarning: {
        trigger: 'onSwitchIn',
        effect: 'Summon hail for 5 turns'
    },

    // Status Abilities
    poisonHeal: {
        trigger: 'onTurnEnd',
        condition: 'poisoned',
        effect: 'Heal 12.5% HP instead of taking damage'
    },

    toxicBoost: {
        trigger: 'passive',
        condition: 'poisoned',
        effect: 'Attack increased by 1.5x'
    },

    guts: {
        trigger: 'passive',
        condition: 'anyStatus',
        effect: 'Attack increased by 1.5x'
    },

    // Speed Abilities
    speedBoost: {
        trigger: 'onTurnEnd',
        effect: 'Raise Speed by 1 stage'
    },

    swiftSwim: {
        trigger: 'passive',
        condition: 'rain',
        effect: 'Double Speed in rain'
    },

    chlorophyll: {
        trigger: 'passive',
        condition: 'sun',
        effect: 'Double Speed in sun'
    },

    // Defensive Abilities
    sturdy: {
        trigger: 'onDamage',
        condition: 'fullHP',
        effect: 'Survive with 1 HP from full health'
    },

    multiscale: {
        trigger: 'onDamage',
        condition: 'fullHP',
        effect: 'Take 0.5x damage at full HP'
    },

    wonderGuard: {
        trigger: 'passive',
        effect: 'Only super-effective moves can hit'
    },

    // Offensive Abilities
    hugepower: {
        trigger: 'passive',
        effect: 'Double Attack stat'
    },

    sheerForce: {
        trigger: 'onMoveUse',
        effect: '1.3x power, remove secondary effects'
    },

    technician: {
        trigger: 'onMoveUse',
        condition: 'movePower <= 60',
        effect: '1.5x power for weak moves'
    },

    // Entry Hazards
    magicGuard: {
        trigger: 'passive',
        effect: 'Immune to indirect damage'
    },

    // Item Abilities
    pickpocket: {
        trigger: 'onContact',
        effect: 'Steal opponent\'s held item'
    },

    unburden: {
        trigger: 'onItemLoss',
        effect: 'Double Speed after using item'
    }
}
```

### 2.7 Held Items System

#### Battle Items (80+ items)
```javascript
heldItems: {
    // Stat Boosters
    choiceBand: {
        effect: '1.5x Attack, locked into first move'
    },

    choiceScarf: {
        effect: '1.5x Speed, locked into first move'
    },

    choiceSpecs: {
        effect: '1.5x Sp. Attack, locked into first move'
    },

    lifeOrb: {
        effect: '1.3x damage, lose 10% HP on hit'
    },

    // Type Boosters
    charcoal: {
        effect: '1.2x Fire-type moves'
    },

    mysticWater: {
        effect: '1.2x Water-type moves'
    },

    // Berries
    sitrusBerry: {
        trigger: 'hp < 50%',
        effect: 'Restore 25% HP'
    },

    oranBerry: {
        trigger: 'hp < 50%',
        effect: 'Restore 10 HP'
    },

    lumBerry: {
        trigger: 'onStatus',
        effect: 'Cure any status condition'
    },

    // Defensive Items
    leftovers: {
        trigger: 'onTurnEnd',
        effect: 'Heal 6.25% HP'
    },

    rockyHelmet: {
        trigger: 'onContactReceived',
        effect: 'Deal 16.7% damage to attacker'
    },

    focusSash: {
        trigger: 'onFaint',
        condition: 'fullHP',
        effect: 'Survive with 1 HP (one-time use)'
    },

    // Utility Items
    expertBelt: {
        effect: '1.2x damage on super-effective hits'
    },

    wideLeens: {
        effect: '+10% accuracy'
    },

    brightPowder: {
        effect: '-10% accuracy for opponent'
    },

    // Terrain Extenders
    terrainExtender: {
        effect: 'Extend terrain duration to 8 turns'
    },

    // Mega Stones
    murlockingite: {
        effect: 'Mega evolve Murloc King'
    }
}
```

### 2.8 Move Categories & Effects

#### Physical, Special, Status Split
```javascript
moveCategories: {
    physical: {
        damageCalc: 'uses Attack vs Defense',
        examples: ['Tackle', 'Bite', 'Earthquake']
    },

    special: {
        damageCalc: 'uses Sp. Attack vs Sp. Defense',
        examples: ['Hydro Pump', 'Psychic', 'Shadow Ball']
    },

    status: {
        damageCalc: 'no damage',
        examples: ['Thunder Wave', 'Swords Dance', 'Recover']
    }
}
```

#### Move Effects (50+ effect types)
```javascript
moveEffects: {
    // Damage Modifiers
    multiHit: {
        hits: 2-5,
        example: 'Fury Attack'
    },

    recoil: {
        selfDamage: 0.25-0.5,
        example: 'Brave Bird'
    },

    drain: {
        healing: 0.5,
        example: 'Giga Drain'
    },

    // Stat Changes
    statDown: {
        target: 'enemy',
        chance: 0.1-1.0,
        example: 'Psychic (10% SpD down)'
    },

    statUp: {
        target: 'self',
        chance: 1.0,
        example: 'Dragon Dance'
    },

    // Status Infliction
    burn: {
        chance: 0.1-0.3,
        example: 'Flamethrower (10%)'
    },

    paralyze: {
        chance: 0.1-1.0,
        example: 'Thunder Wave (100%)'
    },

    poison: {
        chance: 0.1-0.3,
        example: 'Sludge Bomb (30%)'
    },

    // Special Mechanics
    priority: {
        bracket: +1 to +5,
        example: 'Quick Attack (+1)'
    },

    flinch: {
        chance: 0.1-0.3,
        example: 'Rock Slide (30%)'
    },

    criticalHit: {
        baseRate: 0.0625,
        highCritRate: 0.125-0.5,
        example: 'Slash (high crit rate)'
    },

    ohko: {
        accuracy: '30 + user level - target level',
        example: 'Fissure'
    },

    // Field Effects
    entryHazard: {
        types: ['Stealth Rock', 'Spikes', 'Toxic Spikes'],
        effect: 'Damage on switch-in'
    },

    weatherSet: {
        duration: 5,
        example: 'Rain Dance'
    },

    terrainSet: {
        duration: 5,
        example: 'Electric Terrain'
    }
}
```

### 2.9 Damage Calculation Formula

#### Complete Damage Formula
```javascript
calculateDamage(attacker, defender, move) {
    // Base Damage
    let level = attacker.level;
    let power = move.power;

    let attack, defense;
    if (move.category === 'physical') {
        attack = calculateStat(attacker.attack, attacker.statStages.attack);
        defense = calculateStat(defender.defense, defender.statStages.defense);
    } else {
        attack = calculateStat(attacker.spAttack, attacker.statStages.spAttack);
        defense = calculateStat(defender.spDefense, defender.statStages.spDefense);
    }

    let baseDamage = Math.floor((2 * level / 5 + 2) * power * attack / defense / 50) + 2;

    // Modifiers
    let modifiers = 1.0;

    // Targets (multi-target moves deal 0.75x)
    if (move.targets === 'allAdjacent') modifiers *= 0.75;

    // Weather
    if (weather === 'sun' && move.type === 'fire') modifiers *= 1.5;
    if (weather === 'rain' && move.type === 'water') modifiers *= 1.5;
    if (weather === 'sun' && move.type === 'water') modifiers *= 0.5;
    if (weather === 'rain' && move.type === 'fire') modifiers *= 0.5;

    // Critical Hit (1.5x in Gen VI+)
    let critChance = move.critRate || 0.0625;
    if (Math.random() < critChance) {
        modifiers *= 1.5;
        console.log('Critical hit!');
    }

    // Random (0.85 - 1.00)
    modifiers *= (0.85 + Math.random() * 0.15);

    // STAB (Same Type Attack Bonus)
    if (attacker.types.includes(move.type)) {
        modifiers *= 1.5;
    }

    // Type Effectiveness
    let effectiveness = 1.0;
    defender.types.forEach(defType => {
        effectiveness *= getTypeEffectiveness(move.type, defType);
    });
    modifiers *= effectiveness;

    // Burn (halve physical attack)
    if (attacker.status === 'burn' && move.category === 'physical') {
        modifiers *= 0.5;
    }

    // Ability Modifiers
    modifiers *= getAbilityModifier(attacker, defender, move);

    // Item Modifiers
    modifiers *= getItemModifier(attacker, defender, move);

    // Final Damage
    let damage = Math.floor(baseDamage * modifiers);
    return Math.max(1, damage);
}
```

### 2.10 Battle Modes

#### Single Battles
```javascript
singleBattle: {
    format: '1v1',
    teamSize: 6,
    activeCreatures: 1,

    rules: {
        switches: 'unlimited',
        items: 'allowed',
        megaEvolution: '1 per battle',
        zMoves: '1 per battle'
    }
}
```

#### Double Battles
```javascript
doubleBattle: {
    format: '2v2',
    teamSize: 6,
    activeCreatures: 2,

    mechanics: {
        targeting: ['adjacent', 'any', 'allAdjacent', 'allFoes', 'allAllies'],
        spreadMoves: 'deal 0.75x damage',
        allySupport: 'can target allies with buffs',
        protectSharing: 'Wide Guard, Quick Guard'
    }
}
```

#### Rotation Battles
```javascript
rotationBattle: {
    format: '3-way rotation',
    teamSize: 6,
    activeCreatures: 3,

    mechanics: {
        rotation: 'free action before move',
        onlyFront: 'only front creature targeted',
        prediction: 'high skill ceiling'
    }
}
```

#### Triple Battles
```javascript
tripleBattle: {
    format: '3v3',
    teamSize: 6,
    activeCreatures: 3,

    mechanics: {
        targeting: 'position-dependent',
        spreadMoves: 'hit up to 3 targets',
        positionSwap: 'move left/center/right'
    }
}
```

---

## PART 3: EXTENDED FEATURES SUITE

### 3.1 Breeding System

#### Breeding Mechanics
```javascript
breeding: {
    daycare: {
        slots: 2,
        requirements: 'same egg group or Ditto',

        eggGroups: [
            'water1', 'water2', 'water3',
            'bug', 'flying', 'field',
            'fairy', 'grass', 'humanlike',
            'mineral', 'amorphous', 'monster',
            'dragon', 'undiscovered', 'ditto'
        ]
    },

    eggGeneration: {
        baseSteps: 2560-10240,
        flameBody: 'halve steps',

        inheritance: {
            species: 'from mother',
            moves: {
                levelUp: 'from father',
                eggMoves: 'from father',
                tmMoves: 'from either parent'
            },
            ability: {
                normal: '80% regular, 20% hidden',
                hidden: '60% hidden ability from mother'
            },
            ivs: {
                random: 3,          // 3 random perfect IVs
                destinyKnot: 5,     // 5 IVs from parents
                powerItem: 'guarantee 1 stat'
            },
            nature: {
                everstone: '100% pass nature'
            }
        }
    },

    eggMoves: {
        learnableOnly: 'through breeding',
        chainBreeding: 'multi-step breeding paths',
        examples: [
            { species: 'murloc', eggMove: 'aquaJet' },
            { species: 'wisp', eggMove: 'leechSeed' }
        ]
    }
}
```

#### Shiny Breeding
```javascript
shinyOdds: {
    baseOdds: 1/4096,
    masudaMethod: 1/683,        // Foreign parent
    shinyCharm: 1/512,          // With charm + Masuda

    shinyProperties: {
        colorVariant: true,
        sparkleAnimation: true,
        rarity: 'extremely rare',
        tradingValue: 'very high'
    }
}
```

### 3.2 Trading System

#### Trade Mechanics
```javascript
trading: {
    localTrade: {
        method: 'bluetooth/LAN',
        requirements: 'both players online',

        tradeOptions: {
            normal: {},
            withItem: {},
            evolutionTrigger: ['haunter', 'kadabra', 'graveler']
        }
    },

    globalTrade: {
        gts: {
            name: 'Global Trade System',
            list: 'post creature for desired creature',
            search: 'filter by species/level/gender',
            duration: '7 days max'
        },

        wonderTrade: {
            random: 'trade for random creature',
            surprise: 'element of chance',
            eventDistribution: 'rare event creatures'
        }
    },

    tradeEvolutions: {
        triggers: [
            { species: 'haunter', evolves: 'gengar' },
            { species: 'kadabra', evolves: 'alakazam' },
            { species: 'machoke', evolves: 'machamp' },
            { species: 'graveler', evolves: 'golem' }
        ],

        itemEvolutions: [
            { species: 'poliwhirl', item: 'kingRock', evolves: 'politoed' },
            { species: 'scyther', item: 'metalCoat', evolves: 'scizor' }
        ]
    }
}
```

### 3.3 Contest System

#### Beauty Contests
```javascript
contests: {
    categories: ['cool', 'beauty', 'cute', 'smart', 'tough'],

    ranks: ['normal', 'great', 'ultra', 'master'],

    judging: {
        appeal: {
            points: 0-10,
            moveCombo: 'bonus points',
            timing: 'excite crowd'
        },

        condition: {
            stats: ['coolness', 'beauty', 'cuteness', 'smartness', 'toughness'],
            pokeblocks: 'raise condition stats',
            grooming: 'improve appearance'
        }
    },

    prizes: {
        ribbons: 'decorative awards',
        items: 'rare berries',
        titles: 'contest champion'
    }
}
```

### 3.4 Battle Frontier

#### Facility Types
```javascript
battleFrontier: {
    battleTower: {
        format: 'singles',
        rules: 'standard 3v3',
        streak: 'win streaks unlock prizes',
        rewards: 'BP (Battle Points)'
    },

    battleFactory: {
        format: 'rental creatures',
        challenge: 'random teams each round',
        skill: 'team building on fly'
    },

    battlePalace: {
        format: 'AI-controlled creatures',
        gimmick: 'creatures act on personality',
        strategy: 'raise correctly'
    },

    battlePyramid: {
        format: 'dungeon crawl',
        challenge: 'limited items + trainers',
        rewards: 'unique items'
    },

    battleArena: {
        format: '3-turn KO contest',
        judging: 'mind, skill, body',
        strategy: 'fast-paced'
    }
}
```

### 3.5 Achievement System (Extended)

#### 200+ Achievements
```javascript
achievements: {
    // Collection Achievements
    catchFirst: { reward: 500 },
    catch10Species: { reward: 'greatBall x5' },
    catch25Species: { reward: 'ultraBall x5' },
    catchAll: { reward: 'masterBall' },
    catch100Total: { reward: 'quickBall x10' },
    catch500Total: { reward: 'shinyCharm' },

    // Battle Achievements
    win1Battle: { reward: 300 },
    win50Battles: { reward: 'powerBand' },
    win100Battles: { reward: 'luckyEgg' },
    win500Battles: { reward: 'championRibbon' },

    // Streak Achievements
    winStreak10: { reward: 1000 },
    winStreak50: { reward: 'focusSash' },
    winStreak100: { reward: 'choiceScarf' },

    // Evolution Achievements
    evolve1: { reward: 750 },
    evolve10: { reward: 'eviolite' },
    evolveAll: { reward: 'exp. share' },

    // Level Achievements
    reach50: { reward: 'rareCandy x3' },
    reach100: { reward: 'abilityPatch' },
    maxOut6Creatures: { reward: 'goldBottleCap' },

    // Type Achievements
    defeatAllTypes: { reward: 'typeMedallion' },
    monotype50Wins: { reward: 'typeGem' },

    // Legendary Achievements
    catchLegendary: { reward: 'masterBall' },
    catchAllLegendaries: { reward: 'arceusMedal' },

    // Shiny Achievements
    catchShiny: { reward: 'shinyCharm' },
    catch10Shinies: { reward: 'shinyCrown' },

    // Competitive Achievements
    winTournament: { reward: 'trophyRoom' },
    rank1Online: { reward: 'legendTitle' },

    // Time Achievements
    playTime100hrs: { reward: 'veteranRibbon' },
    playTime500hrs: { reward: 'timeMaster' },

    // Money Achievements
    earn100k: { reward: 'amuletCoin' },
    earn1million: { reward: 'tycoonTitle' },

    // Challenge Achievements
    nuzlockeRun: { reward: 'spiritSash' },
    soloRun: { reward: 'loneWolf' },
    noItemsRun: { reward: 'purist' }
}
```

### 3.6 Leaderboards & Rankings

#### Online Rankings
```javascript
leaderboards: {
    global: {
        ranked: {
            tiers: ['master', 'ultra', 'great', 'pokeball'],
            elo: 1000-3000,
            seasons: '3 months',
            rewards: 'seasonal exclusive creatures'
        },

        tournaments: {
            daily: 'single elimination',
            weekly: 'double elimination',
            monthly: 'swiss rounds'
        }
    },

    local: {
        friendsList: 'compare with friends',
        rival: 'track rival battles',
        records: {
            winStreak: 'longest win streak',
            fastestVictory: 'turns to win',
            highestLevel: 'max creature level',
            mostCaught: 'creature count'
        }
    },

    statistics: {
        globalStats: {
            mostUsedCreature: {},
            mostUsedMove: {},
            highestWinRate: {},
            rarest: {}
        }
    }
}
```

### 3.7 Pokedex Systems

#### Advanced Pokedex
```javascript
pokedex: {
    entries: {
        seen: boolean,
        caught: boolean,
        shiny: boolean,

        data: {
            name: string,
            number: number,
            types: [],
            height: number,
            weight: number,
            description: string,
            habitat: string,
            rarity: string,

            baseStats: {},
            abilities: [],
            hiddenAbility: {},

            evolutions: [],

            learnset: {
                levelUp: [],
                tm: [],
                egg: [],
                tutor: []
            },

            locations: [],
            encounterRate: percentage
        }
    },

    filters: {
        type: [],
        habitat: [],
        evolutionStage: [],
        legendary: boolean,
        catchable: boolean,

        search: string,
        sort: 'number' | 'name' | 'type' | 'bst'
    },

    completion: {
        percentage: 0-100,
        seenCount: number,
        caughtCount: number,
        shinyCount: number,

        rewards: {
            50: 'exp. share',
            100: 'shinyCharm',
            150: 'oval charm',
            all: 'diploma'
        }
    }
}
```

### 3.8 Minigames

#### Side Activities
```javascript
minigames: {
    pokeathalon: {
        events: ['speed', 'skill', 'stamina'],
        medals: 'gold/silver/bronze',
        rewards: 'evolution stones'
    },

    safariZone: {
        entrance: 500,
        balls: 30,
        steps: 600,
        mechanics: 'bait or throw rock',
        rewards: 'rare creatures'
    },

    slotMachine: {
        cost: 10,
        prizes: 'TMs, items, creatures',
        jackpot: 'legendary encounters'
    },

    fishing: {
        rods: ['old', 'good', 'super'],
        spots: 'water tiles',
        chain: 'consecutive catches',
        rewards: 'water-type creatures'
    },

    bugCatching: {
        duration: '20 minutes',
        judging: 'rarity + level + stats',
        prizes: 'stones, TMs, rare creatures'
    }
}
```

### 3.9 Customization System

#### Trainer Customization
```javascript
customization: {
    avatar: {
        gender: ['male', 'female', 'nonbinary'],
        skin: 6,
        hair: 20,
        eyes: 15,
        clothing: 100+
    },

    trainerCard: {
        background: 20+,
        frame: 15+,
        stamps: 50+,
        signature: string,
        motto: string
    },

    teamCustomization: {
        nicknames: string,
        markings: 'symbols for organization',
        ribbons: 'display achievements'
    },

    baseCustomization: {
        furniture: 50+,
        decorations: 100+,
        theme: 10+,
        music: 20+
    }
}
```

### 3.10 Post-Game Content

#### Endgame Activities
```javascript
postGame: {
    eliteFour: {
        rematch: 'level 75-80 teams',
        champion: 'level 85 ace',
        rewards: 'rare items, legendaries'
    },

    battleTower: {
        infinite: 'endless battles',
        bosses: 'every 50 battles',
        leaderboard: 'global rankings'
    },

    legendaryHunts: {
        roaming: 'chase across regions',
        stationary: 'puzzle access',
        eventExclusive: 'limited time'
    },

    perfectIVHunting: {
        bottleCaps: 'max IVs',
        hyperTraining: 'level 100 requirement',
        breeding: 'optimize genetics'
    },

    shinyHunting: {
        methods: ['masuda', 'chain', 'sosChain', 'raid'],
        odds: '1/4096 to 1/512',
        tracking: 'shiny log'
    }
}
```

---

## PART 4: DATA STRUCTURES

### 4.1 Creature Data Structure
```javascript
creature: {
    // Identity
    id: string,
    species: string,
    nickname: string,
    gender: 'male' | 'female' | 'genderless',
    isShiny: boolean,
    personalityValue: number,

    // Stats
    level: 1-100,
    exp: number,

    baseStats: {
        hp: number,
        attack: number,
        defense: number,
        spAttack: number,
        spDefense: number,
        speed: number
    },

    ivs: {
        hp: 0-31,
        attack: 0-31,
        defense: 0-31,
        spAttack: 0-31,
        spDefense: 0-31,
        speed: 0-31
    },

    evs: {
        hp: 0-252,
        attack: 0-252,
        defense: 0-252,
        spAttack: 0-252,
        spDefense: 0-252,
        speed: 0-252,
        total: 0-510
    },

    nature: string,

    currentStats: {
        hp: number,
        attack: number,
        defense: number,
        spAttack: number,
        spDefense: number,
        speed: number
    },

    // Battle
    currentHP: number,
    maxHP: number,

    status: 'healthy' | 'burn' | 'freeze' | 'paralysis' | 'poison' | 'sleep',
    statusTurns: number,

    statStages: {
        attack: -6 to +6,
        defense: -6 to +6,
        spAttack: -6 to +6,
        spDefense: -6 to +6,
        speed: -6 to +6,
        accuracy: -6 to +6,
        evasion: -6 to +6
    },

    volatileStatus: [],

    // Moves
    moves: [
        {
            id: string,
            name: string,
            type: string,
            category: 'physical' | 'special' | 'status',
            power: number,
            accuracy: number,
            currentPP: number,
            maxPP: number,
            priority: number,
            effects: []
        }
    ],

    // Ability & Items
    ability: {
        id: string,
        name: string,
        description: string
    },

    hiddenAbility: boolean,

    heldItem: {
        id: string,
        name: string,
        effect: string
    },

    // Evolution
    evolutionStage: 1-3,
    canEvolve: boolean,
    evolveLevel: number,
    evolveTo: string,
    evolveMethod: 'level' | 'stone' | 'trade' | 'friendship',

    // Origin
    originalTrainer: {
        id: string,
        name: string,
        trainerID: number
    },

    caughtDate: timestamp,
    caughtLocation: string,
    caughtLevel: number,
    caughtBall: string,

    // Ribbons & Achievements
    ribbons: [],
    markings: [],

    // Meta
    friendship: 0-255,
    pokerus: boolean,

    // Contest Stats
    contestStats: {
        cool: 0-255,
        beauty: 0-255,
        cute: 0-255,
        smart: 0-255,
        tough: 0-255
    }
}
```

### 4.2 Player Save Data Structure
```javascript
saveData: {
    // Player Info
    player: {
        name: string,
        id: number,
        gender: string,
        avatar: {},
        money: number,

        location: {
            map: string,
            x: number,
            y: number,
            facing: string
        },

        playtime: {
            hours: number,
            minutes: number,
            seconds: number
        },

        badges: [],

        // Teams
        party: [creature],           // Active team (max 6)
        boxes: [[creature]],          // PC storage (30 boxes)
        daycare: [creature],          // Breeding

        // Inventory
        bag: {
            items: {},
            keyItems: {},
            tms: {},
            berries: {}
        },

        // Pokedex
        pokedex: {
            seen: [],
            caught: [],
            shiny: []
        },

        // Stats
        stats: {
            battlesWon: number,
            battlesLost: number,
            creaturesCaught: number,
            eggsHatched: number,
            evolutions: number,

            winStreak: number,
            maxWinStreak: number,

            stepsWalked: number,

            typesDefeated: {},

            fishCaught: number,
            biggestFish: {},

            contestsWon: {},
            ribbonsEarned: []
        },

        // Achievements
        achievements: {
            unlocked: [],
            progress: {}
        },

        // Journal
        journal: {
            entries: [
                {
                    date: timestamp,
                    event: string,
                    location: string,
                    creatures: []
                }
            ]
        },

        // Trading
        tradingData: {
            tradesCompleted: number,
            wonderTradesCompleted: number,
            tradeHistory: []
        },

        // Online
        online: {
            rank: string,
            elo: number,
            seasonWins: number,
            seasonLosses: number
        }
    },

    // Game State
    gameState: {
        currentMap: string,
        position: { x, y },

        flags: {},
        defeatedTrainers: [],

        weather: string,
        terrain: string,

        savedTeams: [],

        options: {
            textSpeed: number,
            battleAnimations: boolean,
            sound: boolean,
            music: boolean,
            difficulty: string
        }
    },

    // Meta
    version: string,
    saveTime: timestamp
}
```

---

## PART 5: IMPLEMENTATION PRIORITIES

### Phase 1: Core Battle Enhancement (2-3 weeks)
1. Implement Ability System (20 abilities)
2. Add Held Items (15 items)
3. Implement Status Effects (6 statuses + volatiles)
4. Add Stat Stages system
5. Weather system (5 weathers)

### Phase 2: Team Builder (2 weeks)
1. Team management UI
2. Synergy analysis engine
3. Type coverage calculator
4. Saved teams system
5. Import/Export functionality

### Phase 3: Stats & Training (1-2 weeks)
1. Nature system
2. EV/IV system
3. Stat calculator
4. Training mechanics
5. Vitamins and items

### Phase 4: Extended Features (3-4 weeks)
1. Breeding system
2. Trading framework
3. Achievement expansion
4. Leaderboards
5. Post-game content

### Phase 5: Polish & Balance (1 week)
1. Battle AI improvements
2. Difficulty tuning
3. Performance optimization
4. Bug fixes
5. Testing

---

## PART 6: TECHNICAL SPECIFICATIONS

### 6.1 Storage Requirements
```javascript
localStorage: {
    saveData: ~50-100 KB,
    teams: ~10-20 KB,
    achievements: ~5 KB,
    settings: ~2 KB,

    total: ~70-130 KB (well under 5MB limit)
}
```

### 6.2 Performance Targets
- Battle calculation: <16ms (60 FPS)
- Team analysis: <100ms
- UI updates: <33ms (30 FPS)
- Save/Load: <200ms

### 6.3 Compatibility
- Desktop: Chrome, Firefox, Safari, Edge
- Mobile: iOS Safari, Chrome Mobile
- Offline: Full functionality
- No external dependencies

---

## PART 7: MONETIZATION (Optional)

### Free-to-Play Model (If Desired)
```javascript
monetization: {
    freemium: {
        free: {
            fullGame: true,
            allCreatures: true,
            allFeatures: true
        },

        optional: {
            cosmetics: {
                avatarSkins: 1-5,
                trainerCardThemes: 1-5,
                particleEffects: 1-5
            },

            convenience: {
                instantEggHatch: 'skip steps',
                fastTravel: 'teleport',
                autoSort: 'organize boxes'
            },

            premium: {
                extraBoxes: '10 additional',
                teamSlots: '5 extra saved teams',
                journal: 'unlimited entries'
            }
        }
    },

    pricing: {
        cosmetics: 0.99-2.99,
        convenience: 1.99-4.99,
        premium: 4.99 (one-time)
    }
}
```

---

## PART 8: ACCESSIBILITY FEATURES

### Enhanced Accessibility
```javascript
accessibility: {
    visual: {
        colorBlindModes: ['deuteranopia', 'protanopia', 'tritanopia'],
        highContrast: true,
        fontSize: 'adjustable 80-150%',
        animations: 'reducible/disable'
    },

    audio: {
        sfx: 'adjustable volume',
        music: 'adjustable volume',
        subtitles: 'all dialogue',
        soundEffectLabels: 'visual indicators'
    },

    motor: {
        singleButtonMode: 'cycle through options',
        touchTargetSize: '44x44px minimum',
        autoAdvanceText: 'timed or manual',
        autoSave: 'every 5 minutes'
    },

    cognitive: {
        simplifiedUI: 'reduce visual clutter',
        tutorialMode: 'always available',
        hintSystem: 'contextual help',
        pauseAnytime: true
    }
}
```

---

## CONCLUSION

This feature-rich design provides **maximum depth and functionality** across three major systems:

### Team Builder Highlights
- 15+ analytics features
- EV/IV system with 510 EVs
- 25 natures with stat modifications
- Advanced synergy analysis
- Comprehensive stat calculators

### Battle System Highlights
- 120+ abilities
- 80+ held items
- Complex damage calculation
- Weather + terrain systems
- 50+ move effect types
- Stat stages (-6 to +6)

### Extended Features Highlights
- Breeding with IV inheritance
- Trading system (local + global)
- 200+ achievements
- Contest system
- Battle Frontier (5 facilities)
- Extensive post-game content

**Total Feature Count: 300+ individual features**

This design prioritizes **power users, completionists, and competitive players** while maintaining the charming Game Boy aesthetic of WowMon.

---

**Estimated Development Time:** 10-14 weeks full-time
**Code Size:** ~15,000-20,000 lines
**Storage:** ~100 KB save files
**Performance:** 60 FPS target

**Status:** Ready for implementation approval
