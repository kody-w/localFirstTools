# WoWMon Endgame Implementation Guide
## Quick Reference for Developers

This is a practical implementation guide for adding endgame systems to WoWMon.

---

## I. DATA STRUCTURES

### Creature Structure (Enhanced)
```javascript
creature = {
    // Existing
    id: "murloc",
    name: "MURLOC",
    level: 50,
    hp: 140,
    maxHp: 140,
    attack: 95,
    defense: 88,
    specialAttack: 92,
    specialDefense: 85,
    speed: 105,
    exp: 5000,
    moves: ["tackle", "bubble", "water_gun", "bite"],
    pp: { "tackle": 35, "bubble": 30, "water_gun": 25, "bite": 25 },

    // NEW: Individual Values (0-31)
    ivs: {
        hp: 31,
        attack: 31,
        defense: 28,
        specialAttack: 31,
        specialDefense: 22,
        speed: 30
    },

    // NEW: Effort Values (0-252, max 510 total)
    evs: {
        hp: 200,
        attack: 252,
        defense: 0,
        specialAttack: 0,
        specialDefense: 0,
        speed: 58
    },

    // NEW: Nature (affects stats)
    nature: "adamant",  // +Attack -SpAttack

    // NEW: Ability
    ability: "swift_swim",
    hiddenAbility: false,

    // NEW: Breeding
    eggMoves: ["aqua_jet", "mirror_coat"],
    eggGroup: ["water"],

    // NEW: Shininess
    isShiny: false,
    shinyValue: 1234,  // For shiny determination

    // NEW: Origin
    origin: {
        trainer_id: 12345,
        trainer_name: "Player",
        region: "NA",
        caught_at: "Goldshire",
        caught_date: "2025-10-12"
    }
};
```

### Player Save Data (Enhanced)
```javascript
player = {
    // Existing
    name: "Red",
    position: { x: 5, y: 5 },
    direction: "down",
    team: {
        active: [/* 6 creatures max */],
        storage: [/* unlimited */]
    },
    badges: ["forge_badge", "nature_badge"],
    money: 50000,

    // NEW: Endgame progression
    battlePoints: 1247,
    achievementsUnlocked: {
        "first_steps": { unlocked: true, date: "2025-10-12" },
        "tower_master": { unlocked: true, date: "2025-10-15" }
    },
    battleTowerFloor: 73,
    battleTowerStreak: 21,
    battleTowerBestStreak: 47,

    // NEW: Breeding stats
    eggsHatched: 847,
    shiniesHatched: 3,
    breedingPerfectIVs: 8,

    // NEW: Shiny tracking
    shinyCharm: false,
    ovalCharm: false,
    shiniesEncountered: 12,
    chainCurrent: 0,
    chainSpecies: null,

    // NEW: Prestige
    prestigeLevel: 0,
    hardMode: false,

    // NEW: Playtime
    playtimeSeconds: 180000  // 50 hours
};
```

### Cartridge Data (Enhanced)
```javascript
cartridge = {
    // Existing
    name: "WoWmon",
    version: "2.0",
    creatures: { /* ... */ },
    moves: { /* ... */ },
    maps: { /* ... */ },

    // NEW: Natures
    natures: {
        "hardy": { neutral: true },
        "adamant": { up: "attack", down: "specialAttack" },
        "jolly": { up: "speed", down: "specialAttack" },
        "modest": { up: "specialAttack", down: "attack" },
        "timid": { up: "speed", down: "attack" },
        "bold": { up: "defense", down: "attack" },
        "calm": { up: "specialDefense", down: "attack" },
        "careful": { up: "specialDefense", down: "specialAttack" },
        "impish": { up: "defense", down: "specialAttack" },
        "relaxed": { up: "defense", down: "speed" },
        "brave": { up: "attack", down: "speed" },
        "quiet": { up: "specialAttack", down: "speed" },
        "sassy": { up: "specialDefense", down: "speed" },
        // ... 12 more
    },

    // NEW: Abilities
    abilities: {
        "swift_swim": {
            description: "Doubles Speed in rain",
            effect: "speed_weather_rain"
        },
        "storm_drain": {
            description: "Immune to Water moves, +1 SpA when hit",
            effect: "immune_water_boost_spa"
        },
        "intimidate": {
            description: "Lowers enemy Attack on entry",
            effect: "entry_lower_attack"
        },
        // ... more
    },

    // NEW: EV Yield
    evYields: {
        "murloc": { hp: 1 },
        "murloc_warrior": { hp: 2 },
        "murloc_king": { hp: 3 },
        "wisp": { specialAttack: 1 },
        "ancient_wisp": { specialAttack: 3 },
        "wolf": { speed: 1 },
        "dire_wolf": { attack: 2, speed: 1 },
        "dragon": { attack: 3 },
        // ... all creatures
    },

    // NEW: Egg Groups
    eggGroups: {
        "murloc": ["water"],
        "wolf": ["beast"],
        "wisp": ["nature"],
        "imp": ["demon"],
        "dragon": ["dragon"],
        "ditto": ["ditto"],  // Universal breeder
        // ... all creatures
    },

    // NEW: Egg Moves
    eggMoves: {
        "murloc": {
            "aqua_jet": {
                power: 40,
                type: "water",
                priority: 1,
                learn_from: ["wolf", "dire_wolf"]
            },
            "mirror_coat": {
                power: "special",
                type: "psychic",
                learn_from: ["ancient_wisp"]
            }
        },
        // ... more
    },

    // NEW: Battle Tower
    battleTower: {
        location: { map: "ironforge", x: 10, y: 15 },
        unlock_requirement: "badges_8",
        floors: 100,
        opponents: [
            // Floor 1-20
            { floor: 1, trainer: "rookie", level: 50, ivs: 0, evs: false },
            // Floor 21-40
            { floor: 21, trainer: "veteran", level: 50, ivs: 3, evs: true },
            // Floor 41-60
            { floor: 41, trainer: "ace", level: 75, ivs: 4, evs: "max" },
            // Floor 61-80
            { floor: 61, trainer: "master", level: 100, ivs: 5, evs: "max", items: true },
            // Floor 81-99
            { floor: 81, trainer: "legend", level: 100, ivs: 6, evs: "max", legendary: true },
            // Floor 100
            { floor: 100, boss: "tower_tycoon", level: 100, perfect: true }
        ]
    },

    // NEW: Achievements
    achievements: {
        "first_steps": {
            id: "first_steps",
            name: "First Steps",
            description: "Start your journey",
            condition: { type: "event", event: "game_start" },
            reward: { type: "none" }
        },
        "all_badges": {
            id: "all_badges",
            name: "Badge Master",
            description: "Collect all 8 badges",
            condition: { type: "badges", count: 8 },
            reward: { type: "bp", amount: 50 }
        },
        "tower_master": {
            id: "tower_master",
            name: "Tower Master",
            description: "Reach Battle Tower Floor 100",
            condition: { type: "tower_floor", floor: 100 },
            reward: { type: "item", item: "master_ball" }
        },
        "first_shiny": {
            id: "first_shiny",
            name: "Shiny Hunter",
            description: "Catch your first shiny",
            condition: { type: "shiny_caught", count: 1 },
            reward: { type: "bp", amount: 100 }
        },
        "perfect_iv": {
            id: "perfect_iv",
            name: "Perfect Specimen",
            description: "Obtain a 6IV creature",
            condition: { type: "perfect_ivs", count: 1 },
            reward: { type: "item", item: "destiny_knot" }
        },
        // ... 75+ more
    },

    // NEW: Items
    items: {
        // Breeding
        "destiny_knot": {
            name: "Destiny Knot",
            type: "held",
            effect: "breeding_5iv_inheritance",
            cost: 48,  // BP
            description: "Passes down 5 IVs from parents"
        },
        "everstone": {
            name: "Everstone",
            type: "held",
            effect: "breeding_nature_inheritance",
            description: "Passes down nature to offspring"
        },
        "power_bracer": {
            name: "Power Bracer",
            type: "held",
            effect: "breeding_attack_iv + ev_attack_boost",
            cost: 16,
            description: "Guarantees Attack IV inheritance, +8 Attack EVs"
        },

        // EV Training
        "hp_up": { name: "HP Up", type: "vitamin", ev: "hp", amount: 10, cost: 9800 },
        "protein": { name: "Protein", type: "vitamin", ev: "attack", amount: 10, cost: 9800 },
        "iron": { name: "Iron", type: "vitamin", ev: "defense", amount: 10, cost: 9800 },
        "calcium": { name: "Calcium", type: "vitamin", ev: "specialAttack", amount: 10, cost: 9800 },
        "zinc": { name: "Zinc", type: "vitamin", ev: "specialDefense", amount: 10, cost: 9800 },
        "carbos": { name: "Carbos", type: "vitamin", ev: "speed", amount: 10, cost: 9800 },

        // EV Reset
        "pomeg_berry": { name: "Pomeg Berry", type: "berry", ev: "hp", amount: -10 },
        "reset_bag": { name: "Reset Bag", type: "tool", effect: "reset_all_evs", cost: 50000 },

        // Hyper Training
        "bottle_cap": { name: "Bottle Cap", type: "tool", effect: "hyper_train_1iv", cost: 25 },
        "gold_bottle_cap": { name: "Gold Bottle Cap", type: "tool", effect: "hyper_train_all_ivs", cost: 200 },

        // Ability
        "ability_capsule": { name: "Ability Capsule", type: "tool", effect: "change_ability", cost: 100 },
        "ability_patch": { name: "Ability Patch", type: "tool", effect: "unlock_hidden_ability", cost: 200 },

        // Battle Items
        "choice_band": { name: "Choice Band", type: "held", effect: "1.5x_attack_lock_move", cost: 48 },
        "life_orb": { name: "Life Orb", type: "held", effect: "1.3x_damage_10%_recoil", cost: 48 },
        "focus_sash": { name: "Focus Sash", type: "held", effect: "survive_ohko_at_full_hp", cost: 32 },

        // Rare
        "master_ball": { name: "Master Ball", type: "pokeball", catch_rate: "100%", cost: "uncatchable" },
        "shiny_charm": { name: "Shiny Charm", type: "key", effect: "3x_shiny_odds" },
        "oval_charm": { name: "Oval Charm", type: "key", effect: "faster_egg_generation" }
    }
};
```

---

## II. STAT CALCULATION FORMULAS

### Standard Stat Formula
```javascript
function calculateStat(baseStat, level, iv, ev, natureMultiplier) {
    // ((2 * Base + IV + (EV/4)) * Level / 100) + 5
    const statValue = Math.floor(((2 * baseStat + iv + Math.floor(ev / 4)) * level / 100) + 5);
    return Math.floor(statValue * natureMultiplier);
}

// Example: Attack at level 100
// Base: 100, IV: 31, EV: 252, Nature: Adamant (+10%)
// ((2 * 100 + 31 + 252/4) * 100 / 100) + 5 = 299
// 299 * 1.1 = 328
```

### HP Formula (Different)
```javascript
function calculateHP(baseHP, level, iv, ev) {
    // ((2 * Base + IV + (EV/4)) * Level / 100) + Level + 10
    return Math.floor(((2 * baseHP + iv + Math.floor(ev / 4)) * level / 100) + level + 10);
}

// Example: HP at level 100
// Base: 100, IV: 31, EV: 252
// ((2 * 100 + 31 + 252/4) * 100 / 100) + 100 + 10 = 404
```

### Nature Multipliers
```javascript
function getNatureMultiplier(nature, stat) {
    const natureData = cartridge.natures[nature];
    if (natureData.neutral) return 1.0;
    if (natureData.up === stat) return 1.1;
    if (natureData.down === stat) return 0.9;
    return 1.0;
}
```

### Apply All Stats
```javascript
function recalculateStats(creature) {
    const data = cartridge.creatures[creature.id];
    const level = creature.level;

    // HP (special formula)
    creature.maxHp = calculateHP(data.baseHp, level, creature.ivs.hp, creature.evs.hp);

    // Attack
    const atkMulti = getNatureMultiplier(creature.nature, "attack");
    creature.attack = calculateStat(data.baseAttack, level, creature.ivs.attack, creature.evs.attack, atkMulti);

    // Defense
    const defMulti = getNatureMultiplier(creature.nature, "defense");
    creature.defense = calculateStat(data.baseDefense, level, creature.ivs.defense, creature.evs.defense, defMulti);

    // Special Attack
    const spaMulti = getNatureMultiplier(creature.nature, "specialAttack");
    creature.specialAttack = calculateStat(data.baseSpecialAttack, level, creature.ivs.specialAttack, creature.evs.specialAttack, spaMulti);

    // Special Defense
    const spdMulti = getNatureMultiplier(creature.nature, "specialDefense");
    creature.specialDefense = calculateStat(data.baseSpecialDefense, level, creature.ivs.specialDefense, creature.evs.specialDefense, spdMulti);

    // Speed
    const speMulti = getNatureMultiplier(creature.nature, "speed");
    creature.speed = calculateStat(data.baseSpeed, level, creature.ivs.speed, creature.evs.speed, speMulti);

    // Heal to full HP if leveling up
    if (creature.hp > 0) {
        creature.hp = creature.maxHp;
    }
}
```

---

## III. GENERATION FUNCTIONS

### Generate Wild Creature (with IVs)
```javascript
function generateWildCreature(creatureId, level, guaranteedIVs = 0) {
    const data = cartridge.creatures[creatureId];

    // Generate IVs
    const ivs = generateIVs(guaranteedIVs);

    // Random nature
    const natures = Object.keys(cartridge.natures);
    const nature = natures[Math.floor(Math.random() * natures.length)];

    // Determine shininess
    const isShiny = determineShiny();

    // Create creature
    const creature = {
        id: creatureId,
        name: data.name,
        level: level,
        ivs: ivs,
        evs: { hp: 0, attack: 0, defense: 0, specialAttack: 0, specialDefense: 0, speed: 0 },
        nature: nature,
        ability: data.ability,
        hiddenAbility: false,
        isShiny: isShiny,
        moves: [...data.moves].slice(0, 4),
        pp: {},
        origin: {
            trainer_id: 0,
            trainer_name: "Wild",
            region: "NA",
            caught_at: game.currentMap,
            caught_date: new Date().toISOString()
        }
    };

    // Initialize PP
    creature.moves.forEach(move => {
        const moveData = cartridge.moves[move];
        creature.pp[move] = moveData.pp;
    });

    // Calculate stats
    recalculateStats(creature);

    return creature;
}
```

### Generate IVs
```javascript
function generateIVs(guaranteedPerfect = 0) {
    const ivs = { hp: 0, attack: 0, defense: 0, specialAttack: 0, specialDefense: 0, speed: 0 };
    const stats = Object.keys(ivs);

    // Guaranteed perfect IVs (31)
    const perfectStats = [];
    while (perfectStats.length < guaranteedPerfect) {
        const stat = stats[Math.floor(Math.random() * stats.length)];
        if (!perfectStats.includes(stat)) {
            perfectStats.push(stat);
            ivs[stat] = 31;
        }
    }

    // Random IVs for remaining
    stats.forEach(stat => {
        if (ivs[stat] === 0) {
            ivs[stat] = Math.floor(Math.random() * 32);  // 0-31
        }
    });

    return ivs;
}
```

### Determine Shininess
```javascript
function determineShiny() {
    const shinyCharm = game.player.shinyCharm;
    const baseOdds = 4096;
    const roll = Math.floor(Math.random() * baseOdds);

    if (shinyCharm) {
        // 3x better odds
        return roll < 3;
    } else {
        return roll === 0;
    }
}
```

---

## IV. BREEDING SYSTEM

### Check Compatibility
```javascript
function canBreed(parent1, parent2) {
    // Same species or same egg group
    const group1 = cartridge.eggGroups[parent1.id];
    const group2 = cartridge.eggGroups[parent2.id];

    // Ditto breeds with anything
    if (group1.includes("ditto") || group2.includes("ditto")) {
        return true;
    }

    // Check shared egg group
    return group1.some(g => group2.includes(g));
}
```

### Generate Egg
```javascript
function generateEgg(parent1, parent2) {
    if (!canBreed(parent1, parent2)) {
        return null;
    }

    // Determine species (mother's species or Ditto)
    const speciesId = parent1.gender === "female" ? parent1.id : parent2.id;

    // Inherit IVs
    const ivs = inheritIVs(parent1, parent2);

    // Inherit nature
    const nature = inheritNature(parent1, parent2);

    // Inherit ability
    const hiddenAbility = inheritAbility(parent1, parent2);

    // Inherit moves
    const moves = inheritMoves(parent1, parent2, speciesId);

    // Determine shininess (Masuda Method)
    const isShiny = determineShinyBreeding(parent1, parent2);

    return {
        id: speciesId,
        level: 1,
        ivs: ivs,
        evs: { hp: 0, attack: 0, defense: 0, specialAttack: 0, specialDefense: 0, speed: 0 },
        nature: nature,
        ability: cartridge.creatures[speciesId].ability,
        hiddenAbility: hiddenAbility,
        isShiny: isShiny,
        moves: moves,
        pp: {},
        origin: {
            trainer_id: game.player.id,
            trainer_name: game.player.name,
            region: "NA",
            caught_at: "Daycare",
            caught_date: new Date().toISOString()
        }
    };
}
```

### Inherit IVs
```javascript
function inheritIVs(parent1, parent2) {
    const ivs = {};
    const stats = ['hp', 'attack', 'defense', 'specialAttack', 'specialDefense', 'speed'];

    // Check for Destiny Knot (5 IVs) or normal (3 IVs)
    const destinyKnot = parent1.heldItem === "destiny_knot" || parent2.heldItem === "destiny_knot";
    const inheritCount = destinyKnot ? 5 : 3;

    // Check for Power Items (guarantee specific stat)
    const powerItems = {
        'power_weight': 'hp',
        'power_bracer': 'attack',
        'power_belt': 'defense',
        'power_lens': 'specialAttack',
        'power_band': 'specialDefense',
        'power_anklet': 'speed'
    };

    let guaranteedStat = null;
    if (powerItems[parent1.heldItem]) guaranteedStat = powerItems[parent1.heldItem];
    if (powerItems[parent2.heldItem]) guaranteedStat = powerItems[parent2.heldItem];

    if (guaranteedStat) {
        ivs[guaranteedStat] = Math.random() < 0.5 ? parent1.ivs[guaranteedStat] : parent2.ivs[guaranteedStat];
    }

    // Inherit random stats
    const toInherit = [];
    while (toInherit.length < inheritCount) {
        const stat = stats[Math.floor(Math.random() * stats.length)];
        if (!toInherit.includes(stat) && !ivs[stat]) {
            toInherit.push(stat);
            ivs[stat] = Math.random() < 0.5 ? parent1.ivs[stat] : parent2.ivs[stat];
        }
    }

    // Random for remaining
    stats.forEach(stat => {
        if (!ivs[stat]) {
            ivs[stat] = Math.floor(Math.random() * 32);
        }
    });

    return ivs;
}
```

### Inherit Nature
```javascript
function inheritNature(parent1, parent2) {
    // Everstone: 100% pass nature
    if (parent1.heldItem === "everstone") return parent1.nature;
    if (parent2.heldItem === "everstone") return parent2.nature;

    // Random nature
    const natures = Object.keys(cartridge.natures);
    return natures[Math.floor(Math.random() * natures.length)];
}
```

### Inherit Ability
```javascript
function inheritAbility(parent1, parent2) {
    // Mother has 60% chance to pass hidden ability
    const mother = parent1.gender === "female" ? parent1 : parent2;
    if (mother.hiddenAbility && Math.random() < 0.6) {
        return true;
    }
    return false;
}
```

### Masuda Method Shiny
```javascript
function determineShinyBreeding(parent1, parent2) {
    const shinyCharm = game.player.shinyCharm;
    const masudaMethod = parent1.origin.region !== parent2.origin.region;

    let odds = 4096;
    if (masudaMethod) odds = 682;  // 6x better
    if (shinyCharm) odds = Math.floor(odds / 3);  // 3x better
    if (masudaMethod && shinyCharm) odds = 512;  // Best odds

    const roll = Math.floor(Math.random() * odds);
    return roll === 0;
}
```

---

## V. EV TRAINING

### Award EVs After Battle
```javascript
function awardEVs(creature, defeatedId) {
    const evYield = cartridge.evYields[defeatedId];
    if (!evYield) return;

    const stats = Object.keys(evYield);
    stats.forEach(stat => {
        const amount = evYield[stat];

        // Apply Power Item bonus (+8)
        let bonus = 0;
        if (creature.heldItem === `power_${stat}`) bonus = 8;

        // Apply Pokerus (2x)
        const multiplier = creature.hasPokerus ? 2 : 1;

        const total = (amount + bonus) * multiplier;

        // Add EVs (respect caps)
        const currentEVs = creature.evs[stat] || 0;
        const totalEVs = Object.values(creature.evs).reduce((a, b) => a + b, 0);

        if (totalEVs < 510 && currentEVs < 252) {
            creature.evs[stat] = Math.min(252, currentEVs + total);
        }
    });

    // Recalculate stats if EVs changed
    recalculateStats(creature);
}
```

### Use Vitamin
```javascript
function useVitamin(creature, vitamin) {
    const vitaminData = cartridge.items[vitamin];
    const stat = vitaminData.ev;
    const amount = vitaminData.amount;

    // Check if under 100 EVs (vitamin limit)
    if (creature.evs[stat] >= 100) {
        return { success: false, message: "Already at vitamin cap (100 EVs)" };
    }

    // Check total EV cap
    const totalEVs = Object.values(creature.evs).reduce((a, b) => a + b, 0);
    if (totalEVs >= 510) {
        return { success: false, message: "Total EVs maxed (510)" };
    }

    // Add EVs
    creature.evs[stat] = Math.min(100, creature.evs[stat] + amount);
    recalculateStats(creature);

    return { success: true, message: `+${amount} ${stat} EVs!` };
}
```

### Reset EVs
```javascript
function resetEVs(creature) {
    creature.evs = {
        hp: 0,
        attack: 0,
        defense: 0,
        specialAttack: 0,
        specialDefense: 0,
        speed: 0
    };
    recalculateStats(creature);
}
```

---

## VI. BATTLE TOWER IMPLEMENTATION

### Enter Battle Tower
```javascript
function enterBattleTower() {
    if (game.player.badges.length < 8) {
        game.showText("You need all 8 badges to enter!");
        return;
    }

    game.state = "BATTLE_TOWER";
    game.battleTowerFloor = game.player.battleTowerFloor || 1;
    game.showBattleTowerUI();
}
```

### Generate Tower Opponent
```javascript
function generateTowerOpponent(floor) {
    const towerData = cartridge.battleTower;
    let config = towerData.opponents.find(o => o.floor <= floor);

    // Find appropriate difficulty
    for (let i = towerData.opponents.length - 1; i >= 0; i--) {
        if (floor >= towerData.opponents[i].floor) {
            config = towerData.opponents[i];
            break;
        }
    }

    // Generate team
    const team = [];
    for (let i = 0; i < 3; i++) {
        const randomId = getRandomCreatureId();
        const creature = generateWildCreature(randomId, config.level, config.ivs);

        // Apply EVs if required
        if (config.evs === "max") {
            creature.evs = {
                hp: 252,
                attack: 252,
                defense: 0,
                specialAttack: 0,
                specialDefense: 0,
                speed: 6
            };
        } else if (config.evs === true) {
            // Random EV spread
            creature.evs = generateRandomEVSpread();
        }

        // Give held items if required
        if (config.items) {
            creature.heldItem = getRandomBattleItem();
        }

        recalculateStats(creature);
        team.push(creature);
    }

    return {
        name: `${config.trainer} ${Math.floor(Math.random() * 1000)}`,
        team: team,
        floor: floor
    };
}
```

### Battle Tower Victory
```javascript
function battleTowerVictory() {
    game.player.battleTowerStreak++;
    game.player.battleTowerFloor++;

    // Award BP
    const bpReward = Math.floor(game.player.battleTowerFloor / 7) * 3;
    game.player.battlePoints += bpReward;

    game.showText(`Victory! +${bpReward} BP`);

    // Check for milestones
    if (game.player.battleTowerFloor === 50) {
        unlockIVJudge();
    }
    if (game.player.battleTowerFloor === 100) {
        unlockAchievement("tower_master");
        game.player.battlePoints += 200;
    }

    game.saveSave();
}
```

---

## VII. ACHIEVEMENT TRACKING

### Check Achievements
```javascript
function checkAchievements() {
    const achievements = cartridge.achievements;

    Object.values(achievements).forEach(achievement => {
        // Skip if already unlocked
        if (game.player.achievementsUnlocked[achievement.id]) return;

        let unlocked = false;
        const cond = achievement.condition;

        switch (cond.type) {
            case "event":
                // Triggered manually
                break;
            case "badges":
                unlocked = game.player.badges.length >= cond.count;
                break;
            case "creatures_caught":
                unlocked = game.player.team.storage.length >= cond.count;
                break;
            case "tower_floor":
                unlocked = game.player.battleTowerFloor >= cond.floor;
                break;
            case "shiny_caught":
                unlocked = game.player.shiniesEncountered >= cond.count;
                break;
            case "perfect_ivs":
                unlocked = countPerfectIVCreatures() >= cond.count;
                break;
            case "battles_won":
                unlocked = game.player.battlesWon >= cond.count;
                break;
        }

        if (unlocked) {
            unlockAchievement(achievement.id);
        }
    });
}
```

### Unlock Achievement
```javascript
function unlockAchievement(achievementId) {
    const achievement = cartridge.achievements[achievementId];

    game.player.achievementsUnlocked[achievementId] = {
        unlocked: true,
        date: new Date().toISOString()
    };

    // Award reward
    const reward = achievement.reward;
    if (reward.type === "bp") {
        game.player.battlePoints += reward.amount;
        game.showText(`Achievement Unlocked: ${achievement.name}! +${reward.amount} BP`);
    } else if (reward.type === "item") {
        game.player.items.push(reward.item);
        game.showText(`Achievement Unlocked: ${achievement.name}! Received ${reward.item}!`);
    } else {
        game.showText(`Achievement Unlocked: ${achievement.name}!`);
    }

    game.audio.playSFX("achievement");
    game.saveSave();
}
```

---

## VIII. UI COMPONENTS

### IV Display
```javascript
function displayIVs(creature) {
    const ivs = creature.ivs;
    const total = Object.values(ivs).reduce((a, b) => a + b, 0);
    const rating = getIVRating(total);

    let display = `IV Judge: ${rating}\n\n`;
    display += `HP:      ${ivs.hp}/31  [${getIVDescription(ivs.hp)}]\n`;
    display += `Attack:  ${ivs.attack}/31  [${getIVDescription(ivs.attack)}]\n`;
    display += `Defense: ${ivs.defense}/31  [${getIVDescription(ivs.defense)}]\n`;
    display += `Sp. Atk: ${ivs.specialAttack}/31  [${getIVDescription(ivs.specialAttack)}]\n`;
    display += `Sp. Def: ${ivs.specialDefense}/31  [${getIVDescription(ivs.specialDefense)}]\n`;
    display += `Speed:   ${ivs.speed}/31  [${getIVDescription(ivs.speed)}]\n\n`;
    display += `Total: ${total}/186 (${((total / 186) * 100).toFixed(1)}%)`;

    return display;
}

function getIVDescription(iv) {
    if (iv === 31) return "Best";
    if (iv >= 30) return "Fantastic";
    if (iv >= 26) return "Very Good";
    if (iv >= 16) return "Pretty Good";
    if (iv >= 1) return "Decent";
    return "No Good";
}

function getIVRating(total) {
    if (total >= 186) return "Perfect";
    if (total >= 170) return "Amazing";
    if (total >= 151) return "Great";
    if (total >= 121) return "Good";
    if (total >= 91) return "Decent";
    return "Mediocre";
}
```

### EV Display
```javascript
function displayEVs(creature) {
    const evs = creature.evs;
    const total = Object.values(evs).reduce((a, b) => a + b, 0);

    let display = `Effort Values: ${total}/510\n\n`;

    const stats = ['hp', 'attack', 'defense', 'specialAttack', 'specialDefense', 'speed'];
    stats.forEach(stat => {
        const ev = evs[stat];
        const percent = (ev / 252) * 100;
        const bars = Math.floor(percent / 10);
        const barDisplay = '█'.repeat(bars) + '░'.repeat(10 - bars);
        const statGain = Math.floor(ev / 4);  // At level 100

        display += `${stat}: ${ev}/252 [${barDisplay}] (+${statGain})\n`;
    });

    return display;
}
```

---

## IX. SAVE/LOAD ENHANCEMENTS

### Save with Endgame Data
```javascript
function saveSave() {
    const saveData = {
        version: "2.0",
        player: game.player,
        team: {
            active: game.player.team.active.map(c => serializeCreature(c)),
            storage: game.player.team.storage.map(c => serializeCreature(c))
        },
        battlePoints: game.player.battlePoints,
        achievements: game.player.achievementsUnlocked,
        battleTower: {
            floor: game.player.battleTowerFloor,
            streak: game.player.battleTowerStreak,
            bestStreak: game.player.battleTowerBestStreak
        },
        breedingStats: {
            eggsHatched: game.player.eggsHatched,
            shiniesHatched: game.player.shiniesHatched
        },
        prestigeLevel: game.player.prestigeLevel,
        playtime: game.player.playtimeSeconds
    };

    localStorage.setItem("wowmon_save", JSON.stringify(saveData));
}

function serializeCreature(creature) {
    return {
        id: creature.id,
        level: creature.level,
        hp: creature.hp,
        exp: creature.exp,
        ivs: creature.ivs,
        evs: creature.evs,
        nature: creature.nature,
        ability: creature.ability,
        hiddenAbility: creature.hiddenAbility,
        isShiny: creature.isShiny,
        moves: creature.moves,
        pp: creature.pp,
        origin: creature.origin
    };
}
```

---

## X. PRIORITY CHECKLIST

### Phase 1: Core (Must Have)
- [ ] Add IV system to creature generation
- [ ] Add EV system to creature generation
- [ ] Implement stat calculation with IVs/EVs
- [ ] Add nature system (25 natures)
- [ ] Apply nature stat modifiers
- [ ] Award EVs after battle
- [ ] Create EV reset function

### Phase 2: Breeding (Must Have)
- [ ] Create Daycare location
- [ ] Implement egg generation
- [ ] Add IV inheritance (Destiny Knot, Power Items)
- [ ] Add nature inheritance (Everstone)
- [ ] Add Masuda Method shiny breeding
- [ ] Create egg groups for all creatures
- [ ] Track breeding stats

### Phase 3: Battle Tower (Must Have)
- [ ] Create Battle Tower building
- [ ] Implement 100-floor system
- [ ] Add difficulty scaling per floor
- [ ] Generate competitive AI teams
- [ ] Add Battle Point currency
- [ ] Create BP shop with items
- [ ] Track streaks and milestones

### Phase 4: UI (Must Have)
- [ ] IV Judge display
- [ ] EV training display
- [ ] Battle Tower UI
- [ ] Achievement tracker
- [ ] Breeding center UI

### Phase 5: Achievements (Should Have)
- [ ] Define 80+ achievements
- [ ] Implement tracking system
- [ ] Add achievement rewards
- [ ] Create achievement UI

### Phase 6: Shiny Hunting (Should Have)
- [ ] Add shiny variants (color palette)
- [ ] Implement shiny odds
- [ ] Add Shiny Charm unlock
- [ ] Create chain hunting methods
- [ ] Track shiny encounters

### Phase 7: Meta (Nice to Have)
- [ ] Prestige system
- [ ] Hard mode
- [ ] Endless mode
- [ ] Battle Frontier facilities
- [ ] Raid battles

---

**Ready to implement!** Start with Phase 1 and build incrementally.
