// WoWMon Endgame - Ready-to-Use Code Snippets
// Copy-paste these directly into wowMon.html

// ============================================
// SECTION 1: STAT CALCULATION SYSTEM
// ============================================

// Add to Game class
calculateStat(baseStat, level, iv, ev, natureMultiplier) {
    // Pokemon stat formula
    const statValue = Math.floor(((2 * baseStat + iv + Math.floor(ev / 4)) * level / 100) + 5);
    return Math.floor(statValue * natureMultiplier);
}

calculateHP(baseHP, level, iv, ev) {
    // HP has a different formula
    return Math.floor(((2 * baseHP + iv + Math.floor(ev / 4)) * level / 100) + level + 10);
}

getNatureMultiplier(nature, stat) {
    const natureData = this.cartridge.natures[nature];
    if (!natureData) return 1.0;
    if (natureData.neutral) return 1.0;
    if (natureData.up === stat) return 1.1;
    if (natureData.down === stat) return 0.9;
    return 1.0;
}

recalculateCreatureStats(creature) {
    const data = this.cartridge.creatures[creature.id];
    const level = creature.level;

    // HP (special formula)
    creature.maxHp = this.calculateHP(
        data.baseHp,
        level,
        creature.ivs.hp,
        creature.evs.hp
    );

    // Attack
    const atkMulti = this.getNatureMultiplier(creature.nature, "attack");
    creature.attack = this.calculateStat(
        data.baseAttack,
        level,
        creature.ivs.attack,
        creature.evs.attack,
        atkMulti
    );

    // Defense
    const defMulti = this.getNatureMultiplier(creature.nature, "defense");
    creature.defense = this.calculateStat(
        data.baseDefense,
        level,
        creature.ivs.defense,
        creature.evs.defense,
        defMulti
    );

    // Special Attack
    const spaMulti = this.getNatureMultiplier(creature.nature, "specialAttack");
    creature.specialAttack = this.calculateStat(
        data.baseSpecialAttack || data.baseAttack,
        level,
        creature.ivs.specialAttack,
        creature.evs.specialAttack,
        spaMulti
    );

    // Special Defense
    const spdMulti = this.getNatureMultiplier(creature.nature, "specialDefense");
    creature.specialDefense = this.calculateStat(
        data.baseSpecialDefense || data.baseDefense,
        level,
        creature.ivs.specialDefense,
        creature.evs.specialDefense,
        spdMulti
    );

    // Speed
    const speMulti = this.getNatureMultiplier(creature.nature, "speed");
    creature.speed = this.calculateStat(
        data.baseSpeed,
        level,
        creature.ivs.speed,
        creature.evs.speed,
        speMulti
    );

    // Heal if leveling up
    if (creature.hp > 0) {
        creature.hp = creature.maxHp;
    }
}

// ============================================
// SECTION 2: IV GENERATION
// ============================================

generateIVs(guaranteedPerfect = 0) {
    const ivs = {
        hp: 0,
        attack: 0,
        defense: 0,
        specialAttack: 0,
        specialDefense: 0,
        speed: 0
    };

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

    // Random IVs for remaining stats (0-31)
    stats.forEach(stat => {
        if (ivs[stat] === 0) {
            ivs[stat] = Math.floor(Math.random() * 32);
        }
    });

    return ivs;
}

// Generate random nature
generateNature() {
    const natures = Object.keys(this.cartridge.natures);
    return natures[Math.floor(Math.random() * natures.length)];
}

// Check if shiny
determineShiny() {
    const shinyCharm = this.player.shinyCharm || false;
    const baseOdds = 4096;
    const roll = Math.floor(Math.random() * baseOdds);

    if (shinyCharm) {
        return roll < 3; // 1/1365 with charm
    } else {
        return roll === 0; // 1/4096
    }
}

// ============================================
// SECTION 3: ENHANCED CREATURE CREATION
// ============================================

// Replace existing createEnemyCreature with this enhanced version
createEnemyCreature(creatureId, level, guaranteedIVs = 0) {
    const creatureData = this.cartridge.creatures[creatureId];
    if (!creatureData) return null;

    // Generate IVs
    const ivs = this.generateIVs(guaranteedIVs);

    // Generate EVs (0 for wild, can be set for trainers)
    const evs = {
        hp: 0,
        attack: 0,
        defense: 0,
        specialAttack: 0,
        specialDefense: 0,
        speed: 0
    };

    // Random nature
    const nature = this.generateNature();

    // Determine shininess
    const isShiny = this.determineShiny();

    // Create creature object
    const creature = {
        id: creatureId,
        name: creatureData.name,
        type: creatureData.type,
        level: level,
        exp: 0,
        moves: [...creatureData.moves].slice(0, 4),
        pp: {},

        // NEW: Endgame stats
        ivs: ivs,
        evs: evs,
        nature: nature,
        ability: creatureData.ability || "no_ability",
        hiddenAbility: false,
        isShiny: isShiny,

        // Origin tracking
        origin: {
            trainer_id: 0,
            trainer_name: "Wild",
            region: "NA",
            caught_at: this.currentMap,
            caught_date: new Date().toISOString()
        }
    };

    // Initialize PP
    creature.moves.forEach(moveId => {
        const move = this.cartridge.moves[moveId];
        if (move) {
            creature.pp[moveId] = move.pp;
        }
    });

    // Calculate stats using new formula
    this.recalculateCreatureStats(creature);

    return creature;
}

// ============================================
// SECTION 4: EV TRAINING SYSTEM
// ============================================

// Add to cartridge.evYields
/*
"evYields": {
    "murloc": { "hp": 1 },
    "murloc_warrior": { "hp": 2 },
    "murloc_king": { "hp": 3 },
    "wisp": { "specialAttack": 1 },
    "ancient_wisp": { "specialAttack": 3 },
    "imp": { "specialAttack": 1 },
    "felguard": { "attack": 2, "specialAttack": 1 },
    "wolf": { "speed": 1 },
    "dire_wolf": { "attack": 2, "speed": 1 },
    "gnoll": { "attack": 1 },
    "kobold": { "defense": 1 },
    "treant": { "hp": 2, "defense": 1 },
    "naga": { "specialAttack": 2 },
    "elemental": { "specialAttack": 1, "specialDefense": 1 },
    "whelp": { "speed": 1 },
    "drake": { "attack": 1, "specialAttack": 1, "speed": 1 },
    "dragon": { "attack": 3 },
    "ghoul": { "attack": 1 },
    "abomination": { "hp": 3 },
    "skeleton": { "attack": 1 },
    "orc_grunt": { "attack": 1 },
    "orc_warlord": { "attack": 3 },
    "banshee": { "specialAttack": 2 },
    "spider": { "attack": 1 },
    "nerubian": { "attack": 2, "speed": 1 },
    "phoenix": { "specialAttack": 3 },
    "quilboar": { "defense": 1 },
    "felhound": { "specialDefense": 2 },
    "infernal": { "attack": 1, "defense": 2 }
}
*/

// Award EVs after battle
awardEVs(winningCreature, defeatedId) {
    if (!this.cartridge.evYields || !this.cartridge.evYields[defeatedId]) {
        return;
    }

    const evYield = this.cartridge.evYields[defeatedId];
    const stats = Object.keys(evYield);

    stats.forEach(stat => {
        const amount = evYield[stat];

        // Apply Power Item bonus (+8 if held)
        let bonus = 0;
        const powerItems = {
            'power_weight': 'hp',
            'power_bracer': 'attack',
            'power_belt': 'defense',
            'power_lens': 'specialAttack',
            'power_band': 'specialDefense',
            'power_anklet': 'speed'
        };
        if (winningCreature.heldItem && powerItems[winningCreature.heldItem] === stat) {
            bonus = 8;
        }

        // Apply Pokerus (2x multiplier)
        const multiplier = winningCreature.hasPokerus ? 2 : 1;

        const total = (amount + bonus) * multiplier;

        // Add EVs (respect caps)
        const currentEVs = winningCreature.evs[stat] || 0;
        const totalEVs = Object.values(winningCreature.evs).reduce((a, b) => a + b, 0);

        // Cap at 252 per stat, 510 total
        if (totalEVs < 510 && currentEVs < 252) {
            const maxCanAdd = Math.min(252 - currentEVs, 510 - totalEVs);
            winningCreature.evs[stat] = currentEVs + Math.min(total, maxCanAdd);
        }
    });

    // Recalculate stats after EV gain
    this.recalculateCreatureStats(winningCreature);
}

// ============================================
// SECTION 5: NATURE SYSTEM
// ============================================

// Add to cartridge.natures
/*
"natures": {
    "hardy": { "neutral": true },
    "lonely": { "up": "attack", "down": "defense" },
    "brave": { "up": "attack", "down": "speed" },
    "adamant": { "up": "attack", "down": "specialAttack" },
    "naughty": { "up": "attack", "down": "specialDefense" },
    "bold": { "up": "defense", "down": "attack" },
    "docile": { "neutral": true },
    "relaxed": { "up": "defense", "down": "speed" },
    "impish": { "up": "defense", "down": "specialAttack" },
    "lax": { "up": "defense", "down": "specialDefense" },
    "timid": { "up": "speed", "down": "attack" },
    "hasty": { "up": "speed", "down": "defense" },
    "jolly": { "up": "speed", "down": "specialAttack" },
    "naive": { "up": "speed", "down": "specialDefense" },
    "modest": { "up": "specialAttack", "down": "attack" },
    "mild": { "up": "specialAttack", "down": "defense" },
    "quiet": { "up": "specialAttack", "down": "speed" },
    "bashful": { "neutral": true },
    "rash": { "up": "specialAttack", "down": "specialDefense" },
    "calm": { "up": "specialDefense", "down": "attack" },
    "gentle": { "up": "specialDefense", "down": "defense" },
    "sassy": { "up": "specialDefense", "down": "speed" },
    "careful": { "up": "specialDefense", "down": "specialAttack" },
    "quirky": { "neutral": true },
    "serious": { "neutral": true }
}
*/

// ============================================
// SECTION 6: IV JUDGE SYSTEM
// ============================================

getIVDescription(iv) {
    if (iv === 31) return "Best";
    if (iv >= 30) return "Fantastic";
    if (iv >= 26) return "Very Good";
    if (iv >= 16) return "Pretty Good";
    if (iv >= 1) return "Decent";
    return "No Good";
}

getIVRating(totalIVs) {
    if (totalIVs >= 186) return "Perfect";
    if (totalIVs >= 170) return "Amazing";
    if (totalIVs >= 151) return "Great";
    if (totalIVs >= 121) return "Good";
    if (totalIVs >= 91) return "Decent";
    return "Mediocre";
}

displayCreatureIVs(creature) {
    const ivs = creature.ivs;
    const total = Object.values(ivs).reduce((a, b) => a + b, 0);
    const rating = this.getIVRating(total);

    let display = `IV JUDGE: ${rating}\n\n`;
    display += `HP:      ${ivs.hp}/31  [${this.getIVDescription(ivs.hp)}]\n`;
    display += `Attack:  ${ivs.attack}/31  [${this.getIVDescription(ivs.attack)}]\n`;
    display += `Defense: ${ivs.defense}/31  [${this.getIVDescription(ivs.defense)}]\n`;
    display += `Sp.Atk:  ${ivs.specialAttack}/31  [${this.getIVDescription(ivs.specialAttack)}]\n`;
    display += `Sp.Def:  ${ivs.specialDefense}/31  [${this.getIVDescription(ivs.specialDefense)}]\n`;
    display += `Speed:   ${ivs.speed}/31  [${this.getIVDescription(ivs.speed)}]\n\n`;
    display += `Total IVs: ${total}/186 (${((total / 186) * 100).toFixed(1)}%)`;

    return display;
}

displayCreatureEVs(creature) {
    const evs = creature.evs;
    const total = Object.values(evs).reduce((a, b) => a + b, 0);

    let display = `EFFORT VALUES: ${total}/510\n\n`;

    const statNames = {
        hp: "HP",
        attack: "Attack",
        defense: "Defense",
        specialAttack: "Sp.Atk",
        specialDefense: "Sp.Def",
        speed: "Speed"
    };

    Object.keys(evs).forEach(stat => {
        const ev = evs[stat];
        const statGain = Math.floor(ev / 4);
        display += `${statNames[stat]}: ${ev}/252 (+${statGain} at Lv100)\n`;
    });

    return display;
}

// ============================================
// SECTION 7: BREEDING SYSTEM
// ============================================

// Check if two creatures can breed
canBreed(parent1, parent2) {
    if (!parent1 || !parent2) return false;

    // Get egg groups
    const groups1 = this.cartridge.eggGroups[parent1.id] || [];
    const groups2 = this.cartridge.eggGroups[parent2.id] || [];

    // Ditto breeds with everything
    if (groups1.includes("ditto") || groups2.includes("ditto")) {
        return true;
    }

    // Check for shared egg group
    return groups1.some(g => groups2.includes(g));
}

// Generate egg from two parents
generateEgg(parent1, parent2) {
    if (!this.canBreed(parent1, parent2)) {
        return null;
    }

    // Determine species (mother's species, or non-Ditto)
    let speciesId = parent1.id;
    const groups1 = this.cartridge.eggGroups[parent1.id] || [];
    const groups2 = this.cartridge.eggGroups[parent2.id] || [];

    if (groups1.includes("ditto")) {
        speciesId = parent2.id;
    }

    // Inherit IVs
    const ivs = this.inheritIVs(parent1, parent2);

    // Inherit nature
    const nature = this.inheritNature(parent1, parent2);

    // Determine shininess (Masuda Method)
    const isShiny = this.determineShinyBreeding(parent1, parent2);

    // Create egg creature at level 1
    const creatureData = this.cartridge.creatures[speciesId];
    const egg = {
        id: speciesId,
        name: creatureData.name,
        type: creatureData.type,
        level: 1,
        exp: 0,
        moves: [...creatureData.moves].slice(0, 4),
        pp: {},
        ivs: ivs,
        evs: {
            hp: 0,
            attack: 0,
            defense: 0,
            specialAttack: 0,
            specialDefense: 0,
            speed: 0
        },
        nature: nature,
        ability: creatureData.ability || "no_ability",
        hiddenAbility: false,
        isShiny: isShiny,
        origin: {
            trainer_id: this.player.id || 1,
            trainer_name: this.player.name,
            region: "NA",
            caught_at: "Daycare",
            caught_date: new Date().toISOString()
        }
    };

    // Initialize PP
    egg.moves.forEach(moveId => {
        const move = this.cartridge.moves[moveId];
        if (move) {
            egg.pp[moveId] = move.pp;
        }
    });

    // Calculate stats
    this.recalculateCreatureStats(egg);

    return egg;
}

// Inherit IVs from parents
inheritIVs(parent1, parent2) {
    const ivs = {};
    const stats = ['hp', 'attack', 'defense', 'specialAttack', 'specialDefense', 'speed'];

    // Check for Destiny Knot (5 IVs instead of 3)
    const destinyKnot = parent1.heldItem === "destiny_knot" || parent2.heldItem === "destiny_knot";
    const inheritCount = destinyKnot ? 5 : 3;

    // Inherit random stats
    const toInherit = [];
    while (toInherit.length < inheritCount) {
        const stat = stats[Math.floor(Math.random() * stats.length)];
        if (!toInherit.includes(stat)) {
            toInherit.push(stat);
            // 50% from each parent
            ivs[stat] = Math.random() < 0.5 ? parent1.ivs[stat] : parent2.ivs[stat];
        }
    }

    // Random for remaining stats
    stats.forEach(stat => {
        if (!ivs[stat]) {
            ivs[stat] = Math.floor(Math.random() * 32);
        }
    });

    return ivs;
}

// Inherit nature from parents
inheritNature(parent1, parent2) {
    // Everstone: 100% pass nature
    if (parent1.heldItem === "everstone") return parent1.nature;
    if (parent2.heldItem === "everstone") return parent2.nature;

    // Random nature
    return this.generateNature();
}

// Masuda Method shiny breeding
determineShinyBreeding(parent1, parent2) {
    const shinyCharm = this.player.shinyCharm || false;
    const masudaMethod = parent1.origin.region !== parent2.origin.region;

    let odds = 4096;
    if (masudaMethod) odds = 682;  // 6x better
    if (shinyCharm) odds = Math.floor(odds / 3);  // 3x better
    if (masudaMethod && shinyCharm) odds = 512;  // Best odds: 1/512

    const roll = Math.floor(Math.random() * odds);
    return roll === 0;
}

// ============================================
// SECTION 8: ACHIEVEMENT SYSTEM
// ============================================

// Add to player initialization
initializePlayer() {
    this.player = {
        // ... existing properties
        achievementsUnlocked: {},
        battlePoints: 0,
        battleTowerFloor: 1,
        battleTowerStreak: 0,
        battleTowerBestStreak: 0,
        eggsHatched: 0,
        shiniesEncountered: 0,
        shinyCharm: false
    };
}

// Check and unlock achievements
checkAchievements() {
    if (!this.cartridge.achievements) return;

    Object.values(this.cartridge.achievements).forEach(achievement => {
        // Skip if already unlocked
        if (this.player.achievementsUnlocked[achievement.id]) return;

        let unlocked = false;
        const cond = achievement.condition;

        switch (cond.type) {
            case "badges":
                unlocked = this.player.badges.length >= cond.count;
                break;
            case "creatures_caught":
                unlocked = this.player.creatures.length >= cond.count;
                break;
            case "tower_floor":
                unlocked = this.player.battleTowerFloor >= cond.floor;
                break;
            case "shiny_caught":
                unlocked = this.player.shiniesEncountered >= cond.count;
                break;
            case "battles_won":
                unlocked = (this.player.battlesWon || 0) >= cond.count;
                break;
        }

        if (unlocked) {
            this.unlockAchievement(achievement.id);
        }
    });
}

unlockAchievement(achievementId) {
    const achievement = this.cartridge.achievements[achievementId];
    if (!achievement) return;

    this.player.achievementsUnlocked[achievementId] = {
        unlocked: true,
        date: new Date().toISOString()
    };

    // Award reward
    const reward = achievement.reward;
    if (reward.type === "bp") {
        this.player.battlePoints += reward.amount;
        this.showText(`Achievement Unlocked!\n${achievement.name}\n+${reward.amount} BP`);
    } else if (reward.type === "item") {
        this.showText(`Achievement Unlocked!\n${achievement.name}\nReceived ${reward.item}!`);
    } else {
        this.showText(`Achievement Unlocked!\n${achievement.name}`);
    }

    this.audio.playSFX("level_up");
    this.autoSave();
}

// ============================================
// SECTION 9: BATTLE TOWER
// ============================================

// Initialize Battle Tower
initializeBattleTower() {
    if (!this.player.battleTowerFloor) {
        this.player.battleTowerFloor = 1;
        this.player.battleTowerStreak = 0;
        this.player.battleTowerBestStreak = 0;
    }
}

// Generate Battle Tower opponent
generateTowerOpponent(floor) {
    let config = {
        level: 50,
        ivs: 0,
        evs: false,
        items: false
    };

    // Difficulty scaling
    if (floor >= 81) {
        config = { level: 100, ivs: 6, evs: "max", items: true, legendary: true };
    } else if (floor >= 61) {
        config = { level: 100, ivs: 5, evs: "max", items: true };
    } else if (floor >= 41) {
        config = { level: 75, ivs: 4, evs: "max" };
    } else if (floor >= 21) {
        config = { level: 50, ivs: 3, evs: true };
    }

    // Generate team of 3
    const team = [];
    const allCreatures = Object.keys(this.cartridge.creatures);

    for (let i = 0; i < 3; i++) {
        const randomId = allCreatures[Math.floor(Math.random() * allCreatures.length)];
        const creature = this.createEnemyCreature(randomId, config.level, config.ivs);

        // Apply max EVs if required
        if (config.evs === "max") {
            creature.evs = {
                hp: 252,
                attack: 252,
                defense: 0,
                specialAttack: 0,
                specialDefense: 0,
                speed: 6
            };
            this.recalculateCreatureStats(creature);
        }

        team.push(creature);
    }

    return {
        name: `Tower Trainer ${floor}`,
        team: team,
        floor: floor
    };
}

// Battle Tower victory
battleTowerVictory() {
    this.player.battleTowerStreak++;
    this.player.battleTowerFloor++;

    if (this.player.battleTowerStreak > this.player.battleTowerBestStreak) {
        this.player.battleTowerBestStreak = this.player.battleTowerStreak;
    }

    // Award BP
    const bpReward = 3 + Math.floor(this.player.battleTowerFloor / 10);
    this.player.battlePoints += bpReward;

    this.showText(`Victory! Floor ${this.player.battleTowerFloor}\n+${bpReward} BP`);

    // Milestones
    if (this.player.battleTowerFloor === 50) {
        this.showText("IV Judge unlocked!");
        this.player.ivJudgeUnlocked = true;
    }
    if (this.player.battleTowerFloor === 100) {
        this.unlockAchievement("tower_master");
        this.player.battlePoints += 200;
    }

    this.checkAchievements();
    this.autoSave();
}

// ============================================
// SECTION 10: INTEGRATION HELPERS
// ============================================

// Update existing handleBattleEnd to award EVs
handleBattleEnd(won) {
    if (won && this.battle && this.battle.enemyCreature) {
        // Award EVs to all participating creatures
        this.player.team.active.forEach(creature => {
            if (creature && creature.hp > 0) {
                this.awardEVs(creature, this.battle.enemyCreature.id);
            }
        });

        // Track shinies
        if (this.battle.enemyCreature.isShiny) {
            this.player.shiniesEncountered = (this.player.shiniesEncountered || 0) + 1;
        }

        // Track battles won
        this.player.battlesWon = (this.player.battlesWon || 0) + 1;
    }

    // Check achievements
    this.checkAchievements();
}

// Update existing starter selection to include IVs/EVs/Nature
giveStarterCreature(creatureId) {
    // Generate with 3 guaranteed perfect IVs (like starters)
    const starter = this.createEnemyCreature(creatureId, 5, 3);

    // Give player-specific origin
    starter.origin = {
        trainer_id: this.player.id || 1,
        trainer_name: this.player.name,
        region: "NA",
        caught_at: "Starter Selection",
        caught_date: new Date().toISOString()
    };

    this.player.creatures.push(starter);
    this.player.team.active.push(starter);

    this.showText(`You received ${starter.name}!`);
}

// ============================================
// SAMPLE CARTRIDGE DATA ADDITIONS
// ============================================

/*
Add these to your cartridge object in autoLoadWoWmon():

"natures": {
    "hardy": { "neutral": true },
    "adamant": { "up": "attack", "down": "specialAttack" },
    "jolly": { "up": "speed", "down": "specialAttack" },
    "modest": { "up": "specialAttack", "down": "attack" },
    "timid": { "up": "speed", "down": "attack" },
    "bold": { "up": "defense", "down": "attack" },
    "calm": { "up": "specialDefense", "down": "attack" },
    // ... rest of 25 natures
},

"evYields": {
    "murloc": { "hp": 1 },
    "murloc_warrior": { "hp": 2 },
    "wolf": { "speed": 1 },
    "dragon": { "attack": 3 },
    // ... rest of creatures
},

"eggGroups": {
    "murloc": ["water"],
    "wolf": ["beast"],
    "wisp": ["nature"],
    "imp": ["demon"],
    "dragon": ["dragon"],
    // ... rest of creatures
},

"achievements": {
    "all_badges": {
        "id": "all_badges",
        "name": "Badge Master",
        "description": "Collect all 8 badges",
        "condition": { "type": "badges", "count": 8 },
        "reward": { "type": "bp", "amount": 50 }
    },
    "tower_master": {
        "id": "tower_master",
        "name": "Tower Master",
        "description": "Reach Battle Tower Floor 100",
        "condition": { "type": "tower_floor", "floor": 100 },
        "reward": { "type": "item", "item": "master_ball" }
    },
    "first_shiny": {
        "id": "first_shiny",
        "name": "Shiny Hunter",
        "description": "Catch your first shiny",
        "condition": { "type": "shiny_caught", "count": 1 },
        "reward": { "type": "bp", "amount": 100 }
    }
    // ... rest of 80+ achievements
}
*/

// ============================================
// READY TO INTEGRATE!
// ============================================

/*
INTEGRATION STEPS:
1. Copy Section 1 (Stat Calculation) into Game class
2. Copy Section 2 (IV Generation) into Game class
3. Replace createEnemyCreature with Section 3
4. Copy Section 4 (EV System) into Game class
5. Add cartridge data from Section 5 (Natures)
6. Copy Section 6 (IV Judge) into Game class
7. Copy Section 7 (Breeding) into Game class
8. Copy Section 8 (Achievements) into Game class
9. Copy Section 9 (Battle Tower) into Game class
10. Update existing functions with Section 10 integrations

TESTING:
- Create a wild creature and check IVs/EVs
- Battle and verify EV gain
- Level up and verify stat recalculation
- Check IV Judge display
- Test breeding system
- Test achievement unlocking

You now have 100+ hours of endgame content!
*/
