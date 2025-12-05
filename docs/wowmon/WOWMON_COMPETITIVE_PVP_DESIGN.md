# WoWmon Competitive PvP System - Complete Design Document

**Agent 6: COMPETITIVE STRATEGY**
**Focus: Player vs Player Competition, Balance, Ranking, and Tournament Play**

---

## Executive Summary

This document outlines a comprehensive competitive multiplayer system for WoWmon.html, designed with PvP battles as the primary focus. The system includes team building with meta analysis, balanced battle mechanics, ELO-based ranking, matchmaking algorithms, tournament infrastructure, and anti-cheat measures.

**Core Philosophy**: Create a skill-based competitive environment where team composition, move selection, prediction, and strategic switching determine victory—not luck or pay-to-win mechanics.

---

## 1. TEAM BUILDER SYSTEM (Competitive Focus)

### 1.1 Team Builder Core Features

#### A. Team Composition Interface
```javascript
const CompetitiveTeamBuilder = {
    maxTeamSize: 6,
    battleFormat: {
        singles: { active: 1, teamSize: 6 },
        doubles: { active: 2, teamSize: 6 },
        triples: { active: 3, teamSize: 6 }
    },

    teamData: {
        name: "Team Alpha",
        format: "singles",
        creatures: [], // Array of 6 creatures
        tier: "OU", // OverUsed tier
        totalStats: 0,
        typeChart: {},
        threatList: [],
        weaknessCoverage: {}
    }
}
```

**Features**:
- **Drag-and-drop** creature positioning for optimal switching strategies
- **Real-time stat calculator** showing total BST (Base Stat Total)
- **Type coverage analyzer** highlighting weaknesses and resistances
- **Role assignment** (Physical Sweeper, Special Wall, Pivot, Lead, etc.)
- **Speed tier checker** showing which threats you outspeed
- **Item slot management** (Life Orb, Choice Scarf, Leftovers, etc.)
- **EV/IV spread calculator** for competitive stat optimization

#### B. Tier System and Balance

**Competitive Tiers** (Based on usage and power level):
```javascript
const TierSystem = {
    UBER: {
        name: "Ubers",
        description: "Legendary and overpowered creatures",
        examples: ["dragon", "infernal", "phoenix"],
        banList: [], // Banned from lower tiers
        restrictions: "No duplicate species"
    },

    OU: {
        name: "OverUsed",
        description: "Standard competitive tier",
        examples: ["murloc_king", "dire_wolf", "ancient_wisp", "orc_warlord"],
        banList: ["dragon", "infernal", "phoenix"],
        restrictions: "No Uber creatures"
    },

    UU: {
        name: "UnderUsed",
        description: "Mid-tier competitive creatures",
        examples: ["murloc_warrior", "drake", "felguard", "nerubian"],
        banList: [...UBER, ...OU_TOP],
        restrictions: "Usage < 4.52% in OU"
    },

    RU: {
        name: "RarelyUsed",
        description: "Niche but viable creatures",
        examples: ["wolf", "gnoll", "spider", "ghoul"],
        banList: [...UU_AND_ABOVE]
    },

    NU: {
        name: "NeverUsed",
        description: "Entry-level competitive",
        examples: ["murloc", "wisp", "imp", "whelp"],
        banList: [...RU_AND_ABOVE]
    },

    LITTLE_CUP: {
        name: "Little Cup",
        description: "Level 5 unevolved creatures only",
        levelCap: 5,
        evolutionRestriction: "No evolved forms"
    }
}
```

#### C. Meta Analysis Dashboard

```javascript
const MetaAnalytics = {
    // Real-time usage statistics
    usageStats: {
        creature: {
            "murloc_king": {
                usage: 23.4, // Percentage
                rank: 1,
                tier: "OU",
                winRate: 52.3,
                avgKills: 1.8,
                avgTurnsAlive: 8.2
            }
        },

        moves: {
            "hydro_pump": { usage: 89.2, successRate: 78.5 },
            "ice_beam": { usage: 76.3, successRate: 92.1 }
        },

        items: {
            "choice_scarf": { usage: 31.2, winRateBonus: +3.2 },
            "leftovers": { usage: 28.7, winRateBonus: +2.1 }
        }
    },

    // Threat analysis
    commonThreats: [
        {
            creature: "orc_warlord",
            frequency: 42.1,
            counterOptions: ["naga", "phoenix", "ancient_wisp"],
            dangerLevel: "HIGH"
        }
    ],

    // Popular team archetypes
    teamArchetypes: {
        "Balance": { usage: 34.2, description: "Mix of offense and defense" },
        "Hyper Offense": { usage: 28.1, description: "Fast, hard-hitting sweepers" },
        "Stall": { usage: 12.3, description: "Defensive walls and recovery" },
        "Weather": { usage: 15.8, description: "Weather-based strategies" },
        "Trick Room": { usage: 9.6, description: "Speed reversal teams" }
    },

    // Live tournament meta updates
    recentTournamentTrends: []
}
```

#### D. Team Validation and Legality Check

```javascript
const TeamValidator = {
    validateTeam(team) {
        const errors = [];
        const warnings = [];

        // Check 1: Team size
        if (team.creatures.length < 3) {
            errors.push("Team must have at least 3 creatures");
        }
        if (team.creatures.length > 6) {
            errors.push("Team cannot exceed 6 creatures");
        }

        // Check 2: Tier legality
        team.creatures.forEach(c => {
            if (!this.isLegalForTier(c, team.tier)) {
                errors.push(`${c.name} is banned in ${team.tier}`);
            }
        });

        // Check 3: Species clause (no duplicates)
        const speciesCount = {};
        team.creatures.forEach(c => {
            speciesCount[c.id] = (speciesCount[c.id] || 0) + 1;
            if (speciesCount[c.id] > 1) {
                errors.push(`Duplicate species: ${c.name}`);
            }
        });

        // Check 4: Item clause (optional rule)
        if (team.format === "singles") {
            const itemCount = {};
            team.creatures.forEach(c => {
                if (c.item) {
                    itemCount[c.item] = (itemCount[c.item] || 0) + 1;
                    if (itemCount[c.item] > 1) {
                        warnings.push(`Duplicate item: ${c.item}`);
                    }
                }
            });
        }

        // Check 5: Type coverage analysis
        const weaknesses = this.analyzeTypeWeaknesses(team);
        if (weaknesses.critical.length > 0) {
            warnings.push(`Critical weakness to: ${weaknesses.critical.join(", ")}`);
        }

        // Check 6: Speed balance check
        const speedTiers = this.analyzeSpeedTiers(team);
        if (speedTiers.slow >= 5) {
            warnings.push("Team may struggle against fast threats");
        }

        return {
            isLegal: errors.length === 0,
            errors,
            warnings,
            score: this.calculateTeamScore(team)
        };
    },

    // Anti-cheese detection
    detectCheese(team) {
        const cheesy = [];

        // Check for "FEAR" strategy (Focus Sash + Endeavor + Quick Attack)
        const fearUser = team.creatures.find(c =>
            c.item === "focus_sash" &&
            c.moves.includes("endeavor") &&
            c.moves.includes("quick_attack")
        );
        if (fearUser) cheesy.push("FEAR strategy detected");

        // Check for infinite stall potential
        const stallers = team.creatures.filter(c =>
            c.moves.includes("recover") || c.moves.includes("synthesis")
        );
        if (stallers.length >= 4) {
            cheesy.push("Excessive stall potential");
        }

        return cheesy;
    }
}
```

#### E. Team Import/Export (Showdown Format)

```javascript
const TeamExporter = {
    // Export to Pokémon Showdown format for easy sharing
    exportToShowdown(team) {
        return team.creatures.map(c => `
${c.name} @ ${c.item || "No Item"}
Ability: ${c.ability || "None"}
Level: ${c.level}
EVs: ${c.evs.hp} HP / ${c.evs.attack} Atk / ${c.evs.defense} Def / ${c.evs.spAttack} SpA / ${c.evs.spDefense} SpD / ${c.evs.speed} Spe
${c.nature} Nature
- ${c.moves[0]}
- ${c.moves[1]}
- ${c.moves[2]}
- ${c.moves[3]}
        `.trim()).join("\n\n");
    },

    // Import from text format
    importFromShowdown(text) {
        // Parser for Showdown format
        // Returns team object
    },

    // Export to QR code for mobile sharing
    exportToQRCode(team) {
        const compressed = this.compressTeam(team);
        return this.generateQRCode(compressed);
    }
}
```

---

## 2. BATTLE SYSTEM (PvP Balanced)

### 2.1 Enhanced Battle Mechanics

#### A. Turn-Based Battle Flow
```javascript
const PvPBattleEngine = {
    battleState: {
        turn: 0,
        player1: { activeCreature: null, team: [], switches: 0 },
        player2: { activeCreature: null, team: [], switches: 0 },
        field: {
            weather: null, // sun, rain, sandstorm, hail
            terrain: null, // electric, grassy, psychic, misty
            hazards: {
                player1Side: [], // stealth_rock, spikes, toxic_spikes
                player2Side: []
            },
            screens: {
                player1: { reflect: 0, lightScreen: 0 },
                player2: { reflect: 0, lightScreen: 0 }
            }
        },
        turnHistory: []
    },

    async processTurn(player1Action, player2Action) {
        // 1. Determine move priority and speed
        const actionOrder = this.determineActionOrder(player1Action, player2Action);

        // 2. Execute switches first (switches always go first)
        for (const action of actionOrder) {
            if (action.type === "switch") {
                await this.executeSwitch(action);
            }
        }

        // 3. Execute moves in priority/speed order
        for (const action of actionOrder) {
            if (action.type === "move") {
                await this.executeMove(action);

                // Check for KO
                if (this.checkKO()) {
                    const forcedSwitch = await this.handleKO();
                    if (forcedSwitch) continue;
                }
            }
        }

        // 4. End of turn effects
        this.processEndOfTurn();

        // 5. Check for battle end
        if (this.checkBattleEnd()) {
            return this.endBattle();
        }

        this.battleState.turn++;
        return { status: "ongoing", turn: this.battleState.turn };
    },

    determineActionOrder(action1, action2) {
        const actions = [action1, action2];

        // Sort by:
        // 1. Switches first
        // 2. Move priority (Quick Attack = +1)
        // 3. Speed stat
        // 4. Random if speed tie

        return actions.sort((a, b) => {
            if (a.type === "switch" && b.type !== "switch") return -1;
            if (b.type === "switch" && a.type !== "switch") return 1;

            if (a.type === "move" && b.type === "move") {
                const priorityDiff = (a.move.priority || 0) - (b.move.priority || 0);
                if (priorityDiff !== 0) return -priorityDiff;

                const speedDiff = a.creature.speed - b.creature.speed;
                if (speedDiff !== 0) return -speedDiff;

                return Math.random() - 0.5; // Speed tie
            }

            return 0;
        });
    }
}
```

#### B. Advanced Damage Calculation (Competitive Formula)

```javascript
const DamageCalculator = {
    calculate(attacker, defender, move, field) {
        // Use Generation 5+ damage formula for competitive accuracy

        // Base damage
        const level = attacker.level;
        const basePower = this.getModifiedPower(move, attacker, defender, field);
        const attack = this.getAttackStat(attacker, move, field);
        const defense = this.getDefenseStat(defender, move, field);

        const baseDamage = Math.floor(
            Math.floor(
                Math.floor(2 * level / 5 + 2) * basePower * attack / defense
            ) / 50
        ) + 2;

        // Apply modifiers
        let damage = baseDamage;

        // 1. Weather modifier
        damage *= this.getWeatherModifier(move, field.weather);

        // 2. Critical hit (12.5% chance with +0 crit stage)
        const critRoll = Math.random();
        const critRate = this.getCritRate(attacker.critStage || 0);
        if (critRoll < critRate) {
            damage *= 1.5;
            move.wasCrit = true;
        }

        // 3. Random factor (85-100%)
        damage *= (85 + Math.random() * 15) / 100;
        damage = Math.floor(damage);

        // 4. STAB (Same Type Attack Bonus)
        if (attacker.types.includes(move.type)) {
            damage = Math.floor(damage * 1.5);
        }

        // 5. Type effectiveness
        const effectiveness = this.getTypeEffectiveness(move.type, defender.types);
        damage = Math.floor(damage * effectiveness);

        // 6. Held item modifiers
        damage *= this.getItemModifier(attacker.item, move);

        // 7. Ability modifiers
        damage *= this.getAbilityModifier(attacker.ability, defender.ability, move);

        // 8. Screen modifiers (Reflect/Light Screen)
        if (defender.side.reflect && move.category === "physical") {
            damage = Math.floor(damage * 0.5);
        }
        if (defender.side.lightScreen && move.category === "special") {
            damage = Math.floor(damage * 0.5);
        }

        damage = Math.max(1, Math.floor(damage));

        return {
            damage,
            effectiveness,
            isCrit: move.wasCrit || false,
            roll: "exact" // Can show min/max/avg for damage calc tools
        };
    },

    // Damage roll ranges for competitive analysis
    calculateDamageRange(attacker, defender, move, field) {
        const ranges = [];
        for (let i = 85; i <= 100; i++) {
            const modifiedCalc = { ...this.calculate };
            // Calculate with fixed random value
            ranges.push(modifiedCalc(attacker, defender, move, field));
        }

        return {
            min: Math.min(...ranges.map(r => r.damage)),
            max: Math.max(...ranges.map(r => r.damage)),
            average: ranges.reduce((a, b) => a + b.damage, 0) / ranges.length,
            guaranteed2HKO: ranges.every(r => r.damage * 2 >= defender.hp),
            guaranteedOHKO: ranges.every(r => r.damage >= defender.hp),
            chanceToOHKO: ranges.filter(r => r.damage >= defender.hp).length / ranges.length
        };
    }
}
```

#### C. Status Conditions and Weather

```javascript
const BattleConditions = {
    statusConditions: {
        BURN: {
            name: "Burn",
            effect: (creature) => {
                creature.attack = Math.floor(creature.attack * 0.5); // Halve physical attack
            },
            endOfTurn: (creature) => {
                const damage = Math.floor(creature.maxHp / 16);
                creature.hp = Math.max(0, creature.hp - damage);
                return `${creature.name} is hurt by its burn!`;
            }
        },

        POISON: {
            name: "Poison",
            endOfTurn: (creature) => {
                const damage = Math.floor(creature.maxHp / 8);
                creature.hp = Math.max(0, creature.hp - damage);
                return `${creature.name} is hurt by poison!`;
            }
        },

        TOXIC: {
            name: "Badly Poisoned",
            turns: 0,
            endOfTurn: (creature, state) => {
                state.turns++;
                const damage = Math.floor(creature.maxHp * state.turns / 16);
                creature.hp = Math.max(0, creature.hp - damage);
                return `${creature.name} is hurt by poison!`;
            }
        },

        PARALYSIS: {
            name: "Paralysis",
            effect: (creature) => {
                creature.speed = Math.floor(creature.speed * 0.5); // Halve speed
            },
            beforeMove: (creature) => {
                if (Math.random() < 0.25) { // 25% chance to be fully paralyzed
                    return { canMove: false, message: `${creature.name} is paralyzed! It can't move!` };
                }
                return { canMove: true };
            }
        },

        SLEEP: {
            name: "Sleep",
            turns: 0,
            maxTurns: 3, // Sleeps for 1-3 turns
            beforeMove: (creature, state) => {
                state.turns++;
                if (state.turns >= state.maxTurns) {
                    creature.status = null;
                    return { canMove: true, message: `${creature.name} woke up!` };
                }
                return { canMove: false, message: `${creature.name} is fast asleep!` };
            }
        },

        FREEZE: {
            name: "Freeze",
            beforeMove: (creature) => {
                if (Math.random() < 0.2) { // 20% chance to thaw
                    creature.status = null;
                    return { canMove: true, message: `${creature.name} thawed out!` };
                }
                return { canMove: false, message: `${creature.name} is frozen solid!` };
            }
        }
    },

    weather: {
        SUN: {
            name: "Harsh Sunlight",
            turns: 5,
            modifyDamage: (move) => {
                if (move.type === "fire") return 1.5;
                if (move.type === "water") return 0.5;
                return 1.0;
            },
            endOfTurn: () => "The sunlight is strong!"
        },

        RAIN: {
            name: "Rain",
            turns: 5,
            modifyDamage: (move) => {
                if (move.type === "water") return 1.5;
                if (move.type === "fire") return 0.5;
                return 1.0;
            },
            modifyAccuracy: (move) => {
                if (move.name === "Thunder") return 999; // Never miss
                return move.accuracy;
            },
            endOfTurn: () => "Rain continues to fall!"
        },

        SANDSTORM: {
            name: "Sandstorm",
            turns: 5,
            endOfTurn: (creature) => {
                if (!["earth", "beast", "warrior"].includes(creature.types[0])) {
                    const damage = Math.floor(creature.maxHp / 16);
                    creature.hp = Math.max(0, creature.hp - damage);
                    return `${creature.name} is buffeted by the sandstorm!`;
                }
                return "The sandstorm rages!";
            },
            modifyDefense: (creature) => {
                if (creature.types.includes("earth")) {
                    return creature.spDefense * 1.5;
                }
                return creature.spDefense;
            }
        },

        HAIL: {
            name: "Hail",
            turns: 5,
            endOfTurn: (creature) => {
                if (!creature.types.includes("ice")) {
                    const damage = Math.floor(creature.maxHp / 16);
                    creature.hp = Math.max(0, creature.hp - damage);
                    return `${creature.name} is buffeted by the hail!`;
                }
                return "Hail continues to fall!";
            },
            modifyAccuracy: (move) => {
                if (move.name === "Blizzard") return 999; // Never miss
                return move.accuracy;
            }
        }
    },

    terrain: {
        ELECTRIC: {
            name: "Electric Terrain",
            turns: 5,
            effect: (creature, move) => {
                // Grounded creatures: Electric moves get 1.5x boost
                if (!creature.flying && move.type === "electric") {
                    return 1.5;
                }
                return 1.0;
            },
            preventStatus: ["SLEEP"] // Prevents sleep while grounded
        },

        GRASSY: {
            name: "Grassy Terrain",
            turns: 5,
            effect: (creature, move) => {
                if (!creature.flying && move.type === "nature") {
                    return 1.3;
                }
                return 1.0;
            },
            endOfTurn: (creature) => {
                if (!creature.flying) {
                    const heal = Math.floor(creature.maxHp / 16);
                    creature.hp = Math.min(creature.maxHp, creature.hp + heal);
                    return `${creature.name} was healed by the grassy terrain!`;
                }
            }
        },

        PSYCHIC: {
            name: "Psychic Terrain",
            turns: 5,
            effect: (creature, move) => {
                if (!creature.flying && move.type === "magic") {
                    return 1.3;
                }
                return 1.0;
            },
            preventMoves: ["quick_attack"] // Blocks priority moves
        },

        MISTY: {
            name: "Misty Terrain",
            turns: 5,
            effect: (creature, move) => {
                if (!creature.flying && move.type === "dragon") {
                    return 0.5; // Halve dragon damage
                }
                return 1.0;
            },
            preventStatus: true // Prevents all status conditions
        }
    }
}
```

#### D. Entry Hazards and Field Effects

```javascript
const FieldHazards = {
    STEALTH_ROCK: {
        name: "Stealth Rock",
        onSwitch: (creature) => {
            // Damage based on rock-type effectiveness
            const effectiveness = TypeChart.getEffectiveness("earth", creature.types);
            const damage = Math.floor(creature.maxHp * effectiveness / 8);
            creature.hp = Math.max(0, creature.hp - damage);
            return `Pointed stones dug into ${creature.name}!`;
        }
    },

    SPIKES: {
        name: "Spikes",
        layers: 0, // Can stack up to 3 layers
        maxLayers: 3,
        onSwitch: (creature) => {
            if (creature.types.includes("flying") || creature.ability === "levitate") {
                return null; // Flying types immune
            }
            const damage = Math.floor(creature.maxHp * this.layers / 8);
            creature.hp = Math.max(0, creature.hp - damage);
            return `${creature.name} is hurt by spikes!`;
        }
    },

    TOXIC_SPIKES: {
        name: "Toxic Spikes",
        layers: 0,
        maxLayers: 2,
        onSwitch: (creature) => {
            if (creature.types.includes("flying") || creature.ability === "levitate") {
                return null;
            }
            if (creature.types.includes("poison")) {
                // Poison types absorb toxic spikes
                this.layers = 0;
                return `${creature.name} absorbed the toxic spikes!`;
            }
            if (this.layers === 1) {
                creature.status = "POISON";
                return `${creature.name} was poisoned!`;
            } else {
                creature.status = "TOXIC";
                return `${creature.name} was badly poisoned!`;
            }
        }
    },

    STICKY_WEB: {
        name: "Sticky Web",
        onSwitch: (creature) => {
            if (!creature.types.includes("flying") && creature.ability !== "levitate") {
                creature.speed = Math.floor(creature.speed * 0.75);
                return `${creature.name} was caught in a sticky web!`;
            }
        }
    }
}
```

---

## 3. RANKING & MATCHMAKING SYSTEM

### 3.1 ELO Rating System

```javascript
const RankingSystem = {
    tiers: [
        { name: "Master", minElo: 2000, icon: "👑" },
        { name: "Diamond", minElo: 1800, icon: "💎" },
        { name: "Platinum", minElo: 1600, icon: "🏆" },
        { name: "Gold", minElo: 1400, icon: "🥇" },
        { name: "Silver", minElo: 1200, icon: "🥈" },
        { name: "Bronze", minElo: 1000, icon: "🥉" },
        { name: "Beginner", minElo: 0, icon: "🌱" }
    ],

    calculateEloChange(playerRating, opponentRating, result, kFactor = 32) {
        // Expected score
        const expectedScore = 1 / (1 + Math.pow(10, (opponentRating - playerRating) / 400));

        // Actual score (1 = win, 0.5 = draw, 0 = loss)
        const actualScore = result === "win" ? 1 : result === "draw" ? 0.5 : 0;

        // ELO change
        const change = Math.round(kFactor * (actualScore - expectedScore));

        return {
            change,
            newRating: playerRating + change,
            expectedWinChance: expectedScore * 100
        };
    },

    // Glicko-2 system (more accurate for competitive)
    calculateGlicko2(player, opponent, result) {
        // More sophisticated rating system that accounts for:
        // - Rating deviation (uncertainty)
        // - Volatility (consistency)
        // - Time decay (activity)

        const g = (rd) => 1 / Math.sqrt(1 + 3 * Math.pow(rd, 2) / Math.pow(Math.PI, 2));
        const E = (rating, opRating, opRD) => {
            return 1 / (1 + Math.exp(-g(opRD) * (rating - opRating)));
        };

        // Calculate new rating, RD, and volatility
        // (Full Glicko-2 implementation)

        return {
            newRating: player.rating,
            newRD: player.rd,
            newVolatility: player.volatility,
            confidence: this.getConfidenceInterval(player.rating, player.rd)
        };
    },

    getPlayerTier(elo) {
        for (let i = this.tiers.length - 1; i >= 0; i--) {
            if (elo >= this.tiers[i].minElo) {
                return this.tiers[i];
            }
        }
        return this.tiers[this.tiers.length - 1];
    },

    // Leaderboard system
    leaderboard: {
        global: [],
        regional: {},
        seasonal: [],

        updateLeaderboard(player) {
            // Update all leaderboards
            this.global = this.sortAndLimit(this.global, player, 1000);

            const region = player.region || "NA";
            if (!this.regional[region]) this.regional[region] = [];
            this.regional[region] = this.sortAndLimit(this.regional[region], player, 500);

            // Seasonal leaderboard resets every 3 months
            const season = this.getCurrentSeason();
            if (!this.seasonal[season]) this.seasonal[season] = [];
            this.seasonal[season] = this.sortAndLimit(this.seasonal[season], player, 1000);
        },

        sortAndLimit(board, player, limit) {
            // Remove old entry
            board = board.filter(p => p.id !== player.id);
            // Add new entry
            board.push(player);
            // Sort by rating
            board.sort((a, b) => b.rating - a.rating);
            // Limit size
            return board.slice(0, limit);
        }
    }
}
```

### 3.2 Matchmaking Algorithm

```javascript
const MatchmakingSystem = {
    queue: {
        singles: [],
        doubles: [],
        triples: []
    },

    matchmakingConfig: {
        maxRatingDifference: 200, // Initial max ELO diff
        ratingExpansionRate: 50, // Increase by 50 every 30 seconds
        maxWaitTime: 300, // 5 minutes max
        minRatingDifference: 0,
        prioritizeLatency: true,
        latencyThreshold: 100 // ms
    },

    async findMatch(player, format = "singles") {
        const queuedAt = Date.now();
        const playerData = {
            id: player.id,
            rating: player.rating,
            tier: player.tier,
            region: player.region,
            latency: player.avgLatency || 50,
            queuedAt,
            preferences: player.matchPreferences
        };

        this.queue[format].push(playerData);

        // Try to find match
        return new Promise((resolve) => {
            const matchInterval = setInterval(() => {
                const match = this.attemptMatch(playerData, format);

                if (match) {
                    clearInterval(matchInterval);
                    resolve(match);
                } else {
                    // Expand search range over time
                    const waitTime = (Date.now() - queuedAt) / 1000;
                    const currentMaxDiff = this.matchmakingConfig.maxRatingDifference +
                        (Math.floor(waitTime / 30) * this.matchmakingConfig.ratingExpansionRate);

                    if (waitTime >= this.matchmakingConfig.maxWaitTime) {
                        clearInterval(matchInterval);
                        resolve(null); // No match found
                    }
                }
            }, 2000); // Check every 2 seconds
        });
    },

    attemptMatch(player, format) {
        const candidates = this.queue[format].filter(p => p.id !== player.id);

        if (candidates.length === 0) return null;

        // Calculate match quality scores
        const matchScores = candidates.map(opponent => {
            const ratingDiff = Math.abs(player.rating - opponent.rating);
            const waitTime = (Date.now() - player.queuedAt) / 1000;
            const maxAllowedDiff = this.matchmakingConfig.maxRatingDifference +
                (Math.floor(waitTime / 30) * this.matchmakingConfig.ratingExpansionRate);

            // Check if within acceptable range
            if (ratingDiff > maxAllowedDiff) {
                return { opponent, score: -1 }; // Not eligible
            }

            // Calculate match quality
            let score = 1000 - ratingDiff; // Prefer closer ratings

            // Latency bonus (prioritize low-latency matches)
            if (this.matchmakingConfig.prioritizeLatency) {
                const avgLatency = (player.latency + opponent.latency) / 2;
                if (avgLatency < this.matchmakingConfig.latencyThreshold) {
                    score += 200;
                }
            }

            // Same region bonus
            if (player.region === opponent.region) {
                score += 100;
            }

            // Similar wait time bonus (fair queue system)
            const waitDiff = Math.abs(player.queuedAt - opponent.queuedAt);
            score -= waitDiff / 1000; // Penalize large wait time differences

            return { opponent, score };
        });

        // Find best match
        const bestMatch = matchScores
            .filter(m => m.score > 0)
            .sort((a, b) => b.score - a.score)[0];

        if (bestMatch) {
            // Remove both players from queue
            this.queue[format] = this.queue[format].filter(
                p => p.id !== player.id && p.id !== bestMatch.opponent.id
            );

            return {
                player1: player,
                player2: bestMatch.opponent,
                format,
                matchQuality: bestMatch.score,
                expectedDuration: this.estimateBattleDuration(player, bestMatch.opponent)
            };
        }

        return null;
    },

    // Skill-based matchmaking with hidden MMR
    hiddenMMR: {
        // Separate hidden rating for more accurate matchmaking
        // Prevents rank manipulation and smurfing

        calculateHiddenMMR(player) {
            // Factors:
            // 1. Win rate
            // 2. Opponent strength
            // 3. Performance metrics (avg damage, turns per battle, etc.)
            // 4. Consistency over time

            const baseMMR = player.rating;
            const winRateAdjustment = (player.winRate - 0.5) * 200;
            const opponentStrengthBonus = player.avgOpponentRating - player.rating;
            const consistencyBonus = this.calculateConsistency(player.recentMatches) * 50;

            return baseMMR + winRateAdjustment + opponentStrengthBonus + consistencyBonus;
        }
    }
}
```

### 3.3 Anti-Smurf Detection

```javascript
const AntiSmurfSystem = {
    detectSmurf(player) {
        const suspicionScore = 0;
        const flags = [];

        // 1. New account with high win rate
        if (player.totalBattles < 20 && player.winRate > 0.8) {
            suspicionScore += 30;
            flags.push("High win rate on new account");
        }

        // 2. Consistently beating higher-rated opponents
        const avgOpponentRating = this.getAverageOpponentRating(player);
        if (avgOpponentRating > player.rating + 300) {
            suspicionScore += 40;
            flags.push("Consistently beating stronger opponents");
        }

        // 3. Advanced team compositions for low rating
        if (player.rating < 1200 && this.hasAdvancedTeamStrategy(player.team)) {
            suspicionScore += 20;
            flags.push("Advanced team strategy for rating");
        }

        // 4. Unusual play patterns (perfect predictions, optimal switches)
        const predictionAccuracy = this.calculatePredictionAccuracy(player.recentBattles);
        if (predictionAccuracy > 0.85) {
            suspicionScore += 30;
            flags.push("Unusually high prediction accuracy");
        }

        // 5. Rapid rating gain
        if (player.ratingGainLast10 > 200) {
            suspicionScore += 20;
            flags.push("Rapid rating increase");
        }

        if (suspicionScore >= 70) {
            return {
                isSmurf: true,
                confidence: suspicionScore,
                flags,
                action: "boost_mmr" // Place in higher skill bracket
            };
        }

        return { isSmurf: false };
    },

    // Dynamic MMR boost for suspected smurfs
    applySmurfProtection(player) {
        if (this.detectSmurf(player).isSmurf) {
            // Accelerate rating gains
            player.kFactor = 64; // Double K-factor for faster climb
            player.hiddenMMR += 300; // Boost hidden MMR

            // Match with higher-rated opponents
            player.matchmakingMMR = player.hiddenMMR;
        }
    }
}
```

---

## 4. TOURNAMENT SYSTEM

### 4.1 Tournament Structure

```javascript
const TournamentSystem = {
    formats: {
        SINGLE_ELIMINATION: {
            name: "Single Elimination",
            description: "Lose once and you're out",
            rounds: (players) => Math.ceil(Math.log2(players))
        },

        DOUBLE_ELIMINATION: {
            name: "Double Elimination",
            description: "Two chances - winners and losers brackets",
            brackets: ["winners", "losers"],
            grandfinals: true
        },

        SWISS: {
            name: "Swiss System",
            description: "Round-robin style, no elimination",
            rounds: (players) => Math.ceil(Math.log2(players)),
            pairing: "swiss" // Pair by similar records
        },

        ROUND_ROBIN: {
            name: "Round Robin",
            description: "Everyone plays everyone",
            rounds: (players) => players - 1,
            matches: (players) => players * (players - 1) / 2
        },

        BATTLE_ROYALE: {
            name: "Battle Royale",
            description: "100 players, last team standing",
            players: 100,
            format: "simultaneous",
            zones: true // Shrinking safe zone
        }
    },

    createTournament(config) {
        return {
            id: this.generateTournamentId(),
            name: config.name,
            format: config.format,
            tierRestriction: config.tier, // OU, UU, etc.
            entryFee: config.entryFee || 0,
            prizePool: 0,
            maxPlayers: config.maxPlayers,
            startTime: config.startTime,
            status: "registration",

            rules: {
                teamLock: true, // Can't change team after registration
                speciesClause: true,
                itemClause: config.itemClause || false,
                sleepClause: true, // Can't put 2+ opponent creatures to sleep
                evasionClause: config.evasionClause || true,
                ohkoClause: true, // Ban OHKO moves
                moodyClause: true, // Ban Moody ability
                endlessClause: true // Prevent infinite battles
            },

            bracket: null,
            participants: [],
            matches: [],
            results: {},

            stream: {
                enabled: config.streaming,
                url: null,
                spectators: []
            }
        };
    },

    // Tournament bracket generation
    generateBracket(tournament) {
        const players = tournament.participants;

        switch (tournament.format) {
            case "SINGLE_ELIMINATION":
                return this.generateSingleElimBracket(players);

            case "DOUBLE_ELIMINATION":
                return this.generateDoubleElimBracket(players);

            case "SWISS":
                return this.generateSwissBracket(players, tournament.rounds);

            case "ROUND_ROBIN":
                return this.generateRoundRobinBracket(players);
        }
    },

    generateSingleElimBracket(players) {
        // Power of 2 bracket with byes if needed
        const bracketSize = Math.pow(2, Math.ceil(Math.log2(players.length)));
        const byes = bracketSize - players.length;

        const bracket = {
            rounds: [],
            matches: []
        };

        // Seed players (1 vs 16, 2 vs 15, etc.)
        const seededPlayers = this.seedPlayers(players);

        // Generate first round
        let round = 1;
        let matchId = 1;
        for (let i = 0; i < seededPlayers.length; i += 2) {
            const match = {
                id: `R${round}M${matchId}`,
                round,
                player1: seededPlayers[i],
                player2: seededPlayers[i + 1] || null, // Bye if null
                winner: seededPlayers[i + 1] ? null : seededPlayers[i],
                status: seededPlayers[i + 1] ? "pending" : "bye"
            };
            bracket.matches.push(match);
            matchId++;
        }

        // Generate subsequent rounds
        const totalRounds = Math.log2(bracketSize);
        for (let r = 2; r <= totalRounds; r++) {
            const prevRoundMatches = bracket.matches.filter(m => m.round === r - 1);
            matchId = 1;
            for (let i = 0; i < prevRoundMatches.length; i += 2) {
                bracket.matches.push({
                    id: `R${r}M${matchId}`,
                    round: r,
                    player1: null, // Winner of prevRoundMatches[i]
                    player2: null, // Winner of prevRoundMatches[i+1]
                    advanceFrom: [prevRoundMatches[i].id, prevRoundMatches[i + 1].id],
                    winner: null,
                    status: "pending"
                });
                matchId++;
            }
        }

        return bracket;
    },

    seedPlayers(players) {
        // Seed based on rating
        const sorted = [...players].sort((a, b) => b.rating - a.rating);

        // Standard tournament seeding
        const seeded = [];
        const bracketSize = Math.pow(2, Math.ceil(Math.log2(players.length)));

        // 1 vs 16, 8 vs 9, 5 vs 12, 4 vs 13, etc.
        const seedOrder = this.generateSeedOrder(bracketSize);

        for (const seed of seedOrder) {
            if (seed <= sorted.length) {
                seeded.push(sorted[seed - 1]);
            }
        }

        return seeded;
    },

    // Swiss pairing algorithm
    swissPairing(players, round) {
        // Group players by record
        const groups = {};
        players.forEach(p => {
            const record = `${p.wins}-${p.losses}`;
            if (!groups[record]) groups[record] = [];
            groups[record].push(p);
        });

        const pairings = [];

        // Pair within each group
        Object.values(groups).forEach(group => {
            // Sort by rating
            group.sort((a, b) => b.rating - a.rating);

            // Pair sequentially, avoiding rematches
            while (group.length >= 2) {
                const p1 = group.shift();

                // Find opponent who hasn't played p1 yet
                let opponentIndex = 0;
                while (opponentIndex < group.length &&
                       p1.opponents.includes(group[opponentIndex].id)) {
                    opponentIndex++;
                }

                if (opponentIndex < group.length) {
                    const p2 = group.splice(opponentIndex, 1)[0];
                    pairings.push({ player1: p1, player2: p2 });
                } else {
                    // Can't find valid pairing, move to next group
                    // (Handle odd player count)
                }
            }
        });

        return pairings;
    },

    // Prize distribution
    distributePrizes(tournament) {
        const pool = tournament.prizePool;
        const distribution = {
            1: 0.50, // 50% to winner
            2: 0.25, // 25% to runner-up
            3: 0.125, // 12.5% to 3rd-4th
            4: 0.125
        };

        const finalStandings = this.getFinalStandings(tournament);

        finalStandings.forEach((player, index) => {
            const placement = index + 1;
            const percentage = distribution[placement] || 0;
            const prize = Math.floor(pool * percentage);

            if (prize > 0) {
                this.awardPrize(player, prize, placement, tournament);
            }
        });
    }
}
```

### 4.2 Tournament Spectator Mode

```javascript
const SpectatorSystem = {
    spectateMatch(matchId) {
        const match = this.getMatch(matchId);

        return {
            // Full battle state visible to spectators
            battleState: match.battle,

            // Advanced statistics
            stats: {
                damageDealt: { player1: 0, player2: 0 },
                damageTaken: { player1: 0, player2: 0 },
                effectiveSwitches: { player1: 0, player2: 0 },
                predictionAccuracy: { player1: 0, player2: 0 },
                hazardDamage: { player1: 0, player2: 0 }
            },

            // Replay data for later viewing
            replay: {
                turns: [],
                teamPreview: {
                    player1: match.player1.team,
                    player2: match.player2.team
                },
                seed: match.randomSeed // For deterministic replay
            },

            // Live commentary (optional AI commentator)
            commentary: this.generateCommentary(match),

            // Spectator chat
            chat: match.spectatorChat || []
        };
    },

    // AI Commentary system
    generateCommentary(match) {
        const events = [];
        const lastTurn = match.battle.turnHistory[match.battle.turn - 1];

        if (!lastTurn) return events;

        // Analyze significant events
        if (lastTurn.ko) {
            events.push({
                type: "ko",
                message: `Big knockout! ${lastTurn.ko.attacker} takes down ${lastTurn.ko.defender}!`,
                importance: "high"
            });
        }

        if (lastTurn.crit) {
            events.push({
                type: "crit",
                message: "Critical hit! That could be a game-changer!",
                importance: "medium"
            });
        }

        if (lastTurn.effectiveness > 1.5) {
            events.push({
                type: "effective",
                message: "Super effective hit! Great type matchup!",
                importance: "medium"
            });
        }

        // Strategic commentary
        if (lastTurn.switch) {
            const prediction = this.evaluateSwitch(lastTurn);
            if (prediction.good) {
                events.push({
                    type: "strategy",
                    message: `Excellent switch! ${prediction.reason}`,
                    importance: "high"
                });
            }
        }

        return events;
    }
}
```

---

## 5. REPLAY & ANALYSIS SYSTEM

### 5.1 Battle Replay System

```javascript
const ReplaySystem = {
    saveReplay(battle) {
        const replay = {
            id: this.generateReplayId(),
            date: Date.now(),
            format: battle.format,
            tier: battle.tier,

            players: {
                player1: {
                    name: battle.player1.name,
                    rating: battle.player1.rating,
                    team: battle.player1.team
                },
                player2: {
                    name: battle.player2.name,
                    rating: battle.player2.rating,
                    team: battle.player2.team
                }
            },

            winner: battle.winner,
            turns: battle.turnHistory.length,
            duration: battle.duration,

            // Compressed turn-by-turn data
            data: this.compressReplayData(battle.turnHistory),

            // Random seed for deterministic replay
            seed: battle.randomSeed,

            // Metadata
            tags: this.generateReplayTags(battle),
            views: 0,
            rating: 0,
            featured: false
        };

        this.database.saveReplay(replay);
        return replay.id;
    },

    compressReplayData(turnHistory) {
        // Compress using delta encoding
        // Only store changes from previous turn

        const compressed = [];
        let prevState = null;

        turnHistory.forEach(turn => {
            if (!prevState) {
                compressed.push(turn); // First turn - store full state
            } else {
                compressed.push(this.getDelta(prevState, turn));
            }
            prevState = turn;
        });

        return compressed;
    },

    playReplay(replayId, options = {}) {
        const replay = this.database.getReplay(replayId);

        return {
            // Reconstructed battle state
            battleState: this.reconstructBattle(replay),

            // Playback controls
            controls: {
                speed: options.speed || 1.0, // 0.5x to 2x
                autoPlay: options.autoPlay || false,
                currentTurn: 0,

                pause: () => {},
                resume: () => {},
                seek: (turn) => {},
                skipTo: (event) => {} // Skip to specific event (KO, switch, etc.)
            },

            // Analysis overlay
            analysis: options.showAnalysis ? this.analyzeReplay(replay) : null
        };
    },

    analyzeReplay(replay) {
        return {
            // Turn-by-turn analysis
            criticalMoments: this.findCriticalMoments(replay),

            // Player performance
            playerStats: {
                player1: this.calculatePlayerPerformance(replay, 1),
                player2: this.calculatePlayerPerformance(replay, 2)
            },

            // Mistakes and missed opportunities
            mistakes: this.identifyMistakes(replay),

            // Optimal plays
            optimalPlays: this.suggestOptimalPlays(replay),

            // Damage chart
            damageChart: this.generateDamageChart(replay),

            // Switch timeline
            switchTimeline: this.generateSwitchTimeline(replay)
        };
    },

    findCriticalMoments(replay) {
        const moments = [];

        replay.data.forEach((turn, index) => {
            let importance = 0;
            let description = "";

            // KO moments
            if (turn.ko) {
                importance = 8;
                description = `${turn.ko.attacker} KO'd ${turn.ko.defender}`;
            }

            // Critical hits at crucial times
            if (turn.crit && turn.damage > turn.defender.hp * 0.5) {
                importance = 7;
                description = `Critical hit changed the game!`;
            }

            // Successful predictions
            if (turn.switch && turn.prediction) {
                importance = 6;
                description = `Perfect prediction switch to ${turn.switch.to}`;
            }

            // Clutch plays (surviving at 1 HP, etc.)
            if (turn.survivor && turn.survivor.hp <= 3) {
                importance = 7;
                description = `${turn.survivor.name} survives with ${turn.survivor.hp} HP!`;
            }

            // Momentum shifts
            const momentumShift = this.detectMomentumShift(replay, index);
            if (momentumShift > 0.3) {
                importance = 6;
                description = "Major momentum shift!";
            }

            if (importance >= 6) {
                moments.push({
                    turn: index + 1,
                    importance,
                    description,
                    timestamp: turn.timestamp
                });
            }
        });

        return moments.sort((a, b) => b.importance - a.importance);
    },

    identifyMistakes(replay) {
        const mistakes = [];

        replay.data.forEach((turn, index) => {
            // Check if player stayed in when they should have switched
            if (turn.stayed && turn.tookDamage > turn.creature.hp * 0.7) {
                const betterSwitch = this.findBetterSwitch(turn, replay.players[turn.player]);
                if (betterSwitch) {
                    mistakes.push({
                        turn: index + 1,
                        player: turn.player,
                        type: "bad_stay",
                        description: `Should have switched to ${betterSwitch.name}`,
                        severity: "high"
                    });
                }
            }

            // Check for suboptimal move choices
            if (turn.move) {
                const optimalMove = this.calculateOptimalMove(turn, replay);
                if (optimalMove.id !== turn.move && optimalMove.advantage > 20) {
                    mistakes.push({
                        turn: index + 1,
                        player: turn.player,
                        type: "suboptimal_move",
                        description: `${optimalMove.name} would have been ${optimalMove.advantage}% better`,
                        severity: optimalMove.advantage > 40 ? "high" : "medium"
                    });
                }
            }

            // Check for wasted turns (status move when damage would KO)
            if (turn.move && turn.movePower === 0 && turn.opponentHp < turn.maxDamageAvailable) {
                mistakes.push({
                    turn: index + 1,
                    player: turn.player,
                    type: "wasted_turn",
                    description: `Could have secured KO instead of using ${turn.moveName}`,
                    severity: "high"
                });
            }
        });

        return mistakes;
    },

    // Share replay
    shareReplay(replayId) {
        const replay = this.database.getReplay(replayId);

        return {
            url: `https://wowmon.com/replay/${replayId}`,
            embedCode: `<iframe src="https://wowmon.com/embed/${replayId}" width="800" height="600"></iframe>`,
            qrCode: this.generateQRCode(`https://wowmon.com/replay/${replayId}`),

            // Export formats
            exportFormats: {
                json: () => JSON.stringify(replay),
                video: () => this.renderReplayToVideo(replay), // Generate MP4
                gif: () => this.renderReplayToGIF(replay, { turns: [/* critical moments */] })
            }
        };
    }
}
```

### 5.2 Post-Battle Statistics

```javascript
const BattleStatistics = {
    generateStats(battle) {
        return {
            // Basic stats
            turns: battle.turnHistory.length,
            duration: battle.duration,
            winner: battle.winner,

            // Damage statistics
            damage: {
                player1: {
                    dealt: this.calculateTotalDamage(battle, 1, "dealt"),
                    taken: this.calculateTotalDamage(battle, 1, "taken"),
                    ratio: 0
                },
                player2: {
                    dealt: this.calculateTotalDamage(battle, 2, "dealt"),
                    taken: this.calculateTotalDamage(battle, 2, "taken"),
                    ratio: 0
                }
            },

            // Creature performance
            creatureStats: this.getCreaturePerformance(battle),

            // Move usage
            moveUsage: this.getMoveUsageStats(battle),

            // Strategic metrics
            metrics: {
                player1: {
                    switches: this.countSwitches(battle, 1),
                    effectiveSwitches: this.countEffectiveSwitches(battle, 1),
                    predictionAccuracy: this.calculatePredictionAccuracy(battle, 1),
                    avgDamagePerTurn: 0,
                    timeToKO: []
                },
                player2: {
                    switches: this.countSwitches(battle, 2),
                    effectiveSwitches: this.countEffectiveSwitches(battle, 2),
                    predictionAccuracy: this.calculatePredictionAccuracy(battle, 2),
                    avgDamagePerTurn: 0,
                    timeToKO: []
                }
            },

            // MVP creature (most damage, most KOs, most important KOs)
            mvp: this.calculateMVP(battle),

            // Momentum chart (who was winning at each turn)
            momentumChart: this.generateMomentumChart(battle)
        };
    },

    getCreaturePerformance(battle) {
        const stats = {};

        battle.turnHistory.forEach(turn => {
            const creature = turn.activeCreature;
            const id = `${turn.player}_${creature.id}_${creature.uniqueId}`;

            if (!stats[id]) {
                stats[id] = {
                    name: creature.name,
                    player: turn.player,
                    damageDealt: 0,
                    damageTaken: 0,
                    turnsActive: 0,
                    kos: 0,
                    timesKOd: 0,
                    switchIns: 0,
                    movesUsed: {}
                };
            }

            stats[id].turnsActive++;

            if (turn.damage) stats[id].damageDealt += turn.damage.dealt;
            if (turn.tookDamage) stats[id].damageTaken += turn.tookDamage;
            if (turn.ko && turn.ko.attacker === creature.name) stats[id].kos++;
            if (turn.ko && turn.ko.defender === creature.name) stats[id].timesKOd++;
            if (turn.switchIn) stats[id].switchIns++;

            if (turn.move) {
                stats[id].movesUsed[turn.move] = (stats[id].movesUsed[turn.move] || 0) + 1;
            }
        });

        return Object.values(stats).sort((a, b) => b.damageDealt - a.damageDealt);
    },

    calculateMVP(battle) {
        const creatures = this.getCreaturePerformance(battle);

        // Score based on:
        // - Damage dealt (40%)
        // - KOs (30%)
        // - Damage taken (10% - survivability)
        // - Critical moments (20%)

        const scored = creatures.map(c => {
            let score = 0;

            score += c.damageDealt * 0.4;
            score += c.kos * 100 * 0.3;
            score += (c.turnsActive / battle.turnHistory.length) * 50 * 0.1;

            // Check if creature got critical KOs
            const criticalKOs = this.getCriticalKOs(battle, c);
            score += criticalKOs * 50 * 0.2;

            return { ...c, mvpScore: score };
        });

        return scored.sort((a, b) => b.mvpScore - a.mvpScore)[0];
    }
}
```

---

## 6. ANTI-CHEAT & FAIR PLAY

### 6.1 Anti-Cheat System

```javascript
const AntiCheatSystem = {
    // Server-side validation
    validateBattle(battle) {
        const violations = [];

        // Check 1: Damage calculation validation
        battle.turnHistory.forEach((turn, index) => {
            if (turn.damage) {
                const calculatedDamage = DamageCalculator.calculate(
                    turn.attacker,
                    turn.defender,
                    turn.move,
                    turn.field
                );

                const range = DamageCalculator.calculateDamageRange(
                    turn.attacker,
                    turn.defender,
                    turn.move,
                    turn.field
                );

                // Allow for rounding errors
                if (turn.damage < range.min - 1 || turn.damage > range.max + 1) {
                    violations.push({
                        turn: index,
                        type: "invalid_damage",
                        severity: "critical",
                        expected: range,
                        actual: turn.damage
                    });
                }
            }
        });

        // Check 2: Impossible move usage
        battle.turnHistory.forEach((turn, index) => {
            if (turn.move) {
                const creature = turn.activeCreature;

                // Check if creature knows the move
                if (!creature.moves.includes(turn.move)) {
                    violations.push({
                        turn: index,
                        type: "impossible_move",
                        severity: "critical",
                        move: turn.move,
                        creature: creature.name
                    });
                }

                // Check PP
                if (creature.pp[turn.move] < 0) {
                    violations.push({
                        turn: index,
                        type: "negative_pp",
                        severity: "critical"
                    });
                }
            }
        });

        // Check 3: Stat modification validation
        battle.turnHistory.forEach((turn, index) => {
            if (turn.statChange) {
                // Verify stat changes are within legal limits (-6 to +6)
                const stages = turn.creature.statStages;
                Object.values(stages).forEach(stage => {
                    if (stage < -6 || stage > 6) {
                        violations.push({
                            turn: index,
                            type: "invalid_stat_stage",
                            severity: "high"
                        });
                    }
                });
            }
        });

        // Check 4: Timing anomalies
        const timings = battle.turnHistory.map(t => t.submitTime);
        const avgTurnTime = timings.reduce((a, b) => a + b, 0) / timings.length;

        timings.forEach((time, index) => {
            // Suspiciously fast turns (under 100ms)
            if (time < 100) {
                violations.push({
                    turn: index,
                    type: "suspicious_timing",
                    severity: "medium",
                    time
                });
            }
        });

        // Check 5: Pattern detection (always perfect predictions)
        const predictions = this.analyzePredictions(battle);
        if (predictions.accuracy > 0.9 && predictions.count > 10) {
            violations.push({
                type: "perfect_predictions",
                severity: "high",
                accuracy: predictions.accuracy
            });
        }

        return {
            isValid: violations.filter(v => v.severity === "critical").length === 0,
            violations,
            confidence: this.calculateConfidence(violations)
        };
    },

    // Heuristic-based cheat detection
    detectCheating(player) {
        const suspicion = {
            score: 0,
            flags: [],
            evidence: []
        };

        // 1. Win rate anomaly
        if (player.winRate > 0.85 && player.totalBattles > 50) {
            suspicion.score += 20;
            suspicion.flags.push("abnormal_win_rate");
        }

        // 2. Perfect damage predictions
        const damageCalcAccuracy = this.calculateDamageCalcAccuracy(player.recentBattles);
        if (damageCalcAccuracy > 0.95) {
            suspicion.score += 30;
            suspicion.flags.push("perfect_damage_knowledge");
            suspicion.evidence.push("Always makes optimal plays based on exact damage ranges");
        }

        // 3. Input pattern analysis
        const inputPatterns = this.analyzeInputPatterns(player.recentBattles);
        if (inputPatterns.automated > 0.7) {
            suspicion.score += 40;
            suspicion.flags.push("automated_inputs");
            suspicion.evidence.push("Input patterns suggest bot usage");
        }

        // 4. Team builder patterns
        const teamCopying = this.detectTeamCopying(player.teams);
        if (teamCopying.score > 0.9) {
            suspicion.score += 10; // Not cheating, but suspicious
            suspicion.flags.push("copied_team");
        }

        // 5. Multiple accounts from same IP
        const accounts = this.findRelatedAccounts(player.ip);
        if (accounts.length > 3) {
            suspicion.score += 25;
            suspicion.flags.push("multiple_accounts");
        }

        if (suspicion.score >= 60) {
            return {
                cheating: true,
                confidence: suspicion.score / 100,
                flags: suspicion.flags,
                evidence: suspicion.evidence,
                action: suspicion.score >= 80 ? "ban" : "flag_for_review"
            };
        }

        return { cheating: false };
    },

    // Real-time battle monitoring
    monitorBattle(battle) {
        const anomalies = [];

        // Monitor turn times
        const turnTimes = [];
        battle.on("turn", (turn) => {
            turnTimes.push(turn.duration);

            // Check for instant decisions (bot-like)
            if (turn.duration < 50 && turn.decision !== "forced") {
                anomalies.push({
                    type: "instant_decision",
                    turn: turn.number
                });
            }
        });

        // Monitor packet manipulation
        battle.on("action", (action) => {
            if (!this.validateActionPacket(action)) {
                anomalies.push({
                    type: "invalid_packet",
                    action
                });

                // Immediately end battle and flag player
                this.flagPlayer(action.player, "packet_manipulation");
                battle.forfeit(action.player);
            }
        });

        return anomalies;
    },

    // Fairness system
    fairPlayScore: {
        calculate(player) {
            let score = 100;

            // Deduct for violations
            score -= player.warnings * 5;
            score -= player.tempBans * 15;

            // Deduct for rage quits
            score -= player.forfeitRate * 20;

            // Deduct for toxic chat
            score -= player.chatViolations * 10;

            // Bonus for sportsmanship
            score += player.sportsmanshipAwards * 5;

            // Bonus for reporting cheaters
            score += player.validReports * 2;

            return Math.max(0, Math.min(100, score));
        },

        getBadge(score) {
            if (score >= 95) return { name: "Exemplary", icon: "🏆", color: "gold" };
            if (score >= 80) return { name: "Honorable", icon: "🎖️", color: "silver" };
            if (score >= 60) return { name: "Fair", icon: "✓", color: "green" };
            if (score >= 40) return { name: "Warning", icon: "⚠️", color: "yellow" };
            return { name: "Restricted", icon: "🚫", color: "red" };
        }
    }
}
```

### 6.2 Replay Validation

```javascript
const ReplayValidator = {
    validateReplay(replay) {
        // Reconstruct battle from replay data
        const reconstructed = this.reconstructBattle(replay);

        // Re-calculate all damage, stat changes, etc.
        const validation = {
            valid: true,
            errors: []
        };

        replay.data.forEach((turn, index) => {
            const reconstructedTurn = reconstructed.turns[index];

            // Compare original vs reconstructed
            if (turn.damage !== reconstructedTurn.damage) {
                validation.valid = false;
                validation.errors.push({
                    turn: index,
                    type: "damage_mismatch",
                    expected: reconstructedTurn.damage,
                    actual: turn.damage
                });
            }

            // Validate RNG (using seed)
            const rng = new SeededRNG(replay.seed);
            const expectedRoll = rng.nextInRange(85, 100);
            if (Math.abs(turn.randomRoll - expectedRoll) > 1) {
                validation.valid = false;
                validation.errors.push({
                    turn: index,
                    type: "rng_manipulation"
                });
            }
        });

        return validation;
    },

    // Seeded RNG for deterministic replay
    SeededRNG: class {
        constructor(seed) {
            this.seed = seed;
            this.state = seed;
        }

        next() {
            // Linear congruential generator
            this.state = (this.state * 1103515245 + 12345) & 0x7fffffff;
            return this.state / 0x7fffffff;
        }

        nextInRange(min, max) {
            return min + (this.next() * (max - min));
        }
    }
}
```

---

## 7. ADDITIONAL COMPETITIVE FEATURES

### 7.1 Draft Mode

```javascript
const DraftMode = {
    // Pokemon-style draft pick
    startDraft(players, config) {
        const draft = {
            players,
            pool: config.creaturePool || "all",
            bans: config.bansPerPlayer || 2,
            picks: config.picksPerPlayer || 6,
            format: config.format || "snake", // snake or linear

            state: {
                phase: "ban",
                currentPlayer: 0,
                banList: [],
                pickedCreatures: { player1: [], player2: [] },
                availablePool: this.getCreaturePool(config.pool)
            }
        };

        return draft;
    },

    processDraftPick(draft, player, creatureId) {
        // Validate pick
        if (!draft.state.availablePool.includes(creatureId)) {
            return { error: "Creature not available" };
        }

        // Ban phase
        if (draft.state.phase === "ban") {
            draft.state.banList.push(creatureId);
            draft.state.availablePool = draft.state.availablePool.filter(c => c !== creatureId);

            if (draft.state.banList.length >= draft.bans * 2) {
                draft.state.phase = "pick";
            }
        }
        // Pick phase
        else {
            const playerKey = `player${player}`;
            draft.state.pickedCreatures[playerKey].push(creatureId);
            draft.state.availablePool = draft.state.availablePool.filter(c => c !== creatureId);

            if (draft.state.pickedCreatures[playerKey].length >= draft.picks) {
                // Draft complete
                return { complete: true, teams: draft.state.pickedCreatures };
            }
        }

        // Determine next player (snake draft alternates)
        if (draft.format === "snake") {
            const totalPicks = Object.values(draft.state.pickedCreatures).flat().length;
            const round = Math.floor(totalPicks / 2);
            draft.state.currentPlayer = round % 2 === 0 ? (totalPicks % 2) : (1 - (totalPicks % 2));
        }

        return { success: true, draft };
    }
}
```

### 7.2 Seasonal Rewards

```javascript
const SeasonalSystem = {
    season: {
        number: 1,
        startDate: Date.now(),
        endDate: Date.now() + (90 * 24 * 60 * 60 * 1000), // 3 months
        theme: "Dragon's Ascent",
        rewards: {}
    },

    calculateSeasonRewards(player) {
        const tier = RankingSystem.getPlayerTier(player.rating);
        const rank = player.seasonalRank;

        const rewards = {
            title: null,
            cosmetics: [],
            currency: 0,
            exclusive: null
        };

        // Rank-based rewards
        if (rank <= 10) {
            rewards.title = "Seasonal Champion";
            rewards.cosmetics.push("golden_avatar_border");
            rewards.currency = 5000;
            rewards.exclusive = "legendary_skin_choice";
        } else if (rank <= 100) {
            rewards.title = "Seasonal Master";
            rewards.cosmetics.push("platinum_avatar_border");
            rewards.currency = 2000;
            rewards.exclusive = "epic_skin_choice";
        } else if (tier.name === "Master") {
            rewards.title = `Season ${this.season.number} Master`;
            rewards.cosmetics.push("master_tier_badge");
            rewards.currency = 1000;
        } else if (tier.name === "Diamond") {
            rewards.cosmetics.push("diamond_tier_badge");
            rewards.currency = 500;
        }

        // Achievement rewards
        if (player.seasonWins >= 100) {
            rewards.cosmetics.push("century_warrior_badge");
        }

        return rewards;
    },

    endSeason() {
        // Distribute rewards to all players
        const allPlayers = this.database.getAllPlayers();

        allPlayers.forEach(player => {
            const rewards = this.calculateSeasonRewards(player);
            this.awardSeasonRewards(player, rewards);
        });

        // Reset seasonal stats
        this.resetSeasonalStats();

        // Start new season
        this.season.number++;
        this.season.startDate = Date.now();
        this.season.endDate = Date.now() + (90 * 24 * 60 * 60 * 1000);

        // Soft MMR reset (move toward 1500)
        allPlayers.forEach(player => {
            player.rating = Math.floor((player.rating + 1500) / 2);
        });
    }
}
```

---

## 8. IMPLEMENTATION ROADMAP

### Phase 1: Core PvP Infrastructure (Weeks 1-4)
1. **Week 1**: Enhanced battle mechanics
   - Advanced damage calculation
   - Status conditions and weather
   - Field effects and hazards

2. **Week 2**: Team builder system
   - Drag-and-drop interface
   - Type coverage analyzer
   - Team validation

3. **Week 3**: Multiplayer networking
   - WebSocket server setup
   - P2P battle protocol
   - Latency compensation

4. **Week 4**: Basic matchmaking
   - ELO system implementation
   - Simple matchmaking queue
   - Battle result tracking

### Phase 2: Competitive Features (Weeks 5-8)
1. **Week 5**: Tier system
   - Usage-based tier calculation
   - Tier restrictions
   - Meta analytics dashboard

2. **Week 6**: Ranking system
   - Leaderboards (global, regional, seasonal)
   - Rank decay system
   - Seasonal rewards

3. **Week 7**: Replay system
   - Save/load replays
   - Replay viewer with controls
   - Basic analysis tools

4. **Week 8**: Tournament infrastructure
   - Single elimination brackets
   - Swiss system
   - Tournament registration

### Phase 3: Advanced Features (Weeks 9-12)
1. **Week 9**: Anti-cheat system
   - Server-side validation
   - Pattern detection
   - Fair play scoring

2. **Week 10**: Advanced analytics
   - Post-battle statistics
   - MVP calculation
   - Mistake identification

3. **Week 11**: Draft mode
   - Pick/ban interface
   - Snake draft logic
   - Draft analytics

4. **Week 12**: Polish and balance
   - Creature balance adjustments
   - Move pool optimization
   - Meta testing

### Phase 4: Launch Preparation (Weeks 13-16)
1. **Week 13**: Beta testing
   - Invite competitive players
   - Balance feedback
   - Bug fixes

2. **Week 14**: Tournament hosting
   - First official tournament
   - Spectator features
   - Prize system

3. **Week 15**: Community features
   - Team sharing
   - Replay highlights
   - Social features

4. **Week 16**: Official launch
   - Season 1 begins
   - Marketing push
   - Ladder reset

---

## 9. BALANCE CONSIDERATIONS

### 9.1 Competitive Balance Philosophy

**Core Principles**:
1. **No creature should be completely unviable** - Even low-tier creatures should have niche uses
2. **Counterplay exists for everything** - No unbeatable strategies
3. **Skill > Team composition** - Prediction and strategy matter more than raw stats
4. **Diversity encouraged** - Multiple viable team archetypes
5. **Regular balance patches** - Monthly meta adjustments based on data

### 9.2 Balance Metrics to Monitor

```javascript
const BalanceMetrics = {
    // Creature usage rates
    trackUsage(tier) {
        // Creatures with >50% usage need nerfs
        // Creatures with <1% usage need buffs
    },

    // Win rates when present
    trackWinRates(creature) {
        // 55%+ win rate = too strong
        // <45% win rate = too weak
    },

    // Move usage rates
    trackMoveUsage(move) {
        // Identify must-have moves (need nerfs)
        // Identify never-used moves (need buffs)
    },

    // Team archetype success
    trackArchetypes() {
        // Ensure multiple viable playstyles
        // No single archetype should dominate
    },

    // Type balance
    trackTypeDistribution() {
        // Ensure all types are represented
        // Identify type chart imbalances
    }
}
```

### 9.3 Suggested Balance Changes for Current WoWmon

Based on the current creature data:

**Over-Powered** (Needs Nerfs):
- **Dragon**: Base stat total too high (400+), reduce by 10-15%
- **Infernal**: Explosion move (250 power) is too strong, reduce to 200 or add drawback
- **Phoenix**: Speed 100 + Fire/Spirit typing is too good, reduce speed to 90

**Under-Powered** (Needs Buffs):
- **Murloc**: Too weak early game, increase base HP from 45 to 50
- **Skeleton**: No evolution and weak stats, add evolution or increase stats
- **Kobold**: Very limited use, buff base attack from 35 to 45

**Move Balance**:
- **Hyper Beam** (150 power): Should require recharge turn
- **Explosion** (250 power): Should cause user to faint
- **Quick Attack**: Priority +1 is fine but damage may be too high at 40

---

## 10. CONCLUSION

This comprehensive competitive PvP system transforms WoWmon from a single-player game into a deep, strategic multiplayer experience. The design prioritizes:

✅ **Competitive Integrity**: Anti-cheat, server validation, fair play
✅ **Skill Expression**: Prediction, team building, strategic depth
✅ **Balanced Gameplay**: Regular patches, usage-based tiers, counterplay
✅ **Player Engagement**: Rankings, tournaments, replays, seasons
✅ **Community Features**: Spectating, sharing, social competition

**Next Steps**:
1. Begin with Phase 1 implementation (core battle mechanics)
2. Set up WebSocket server for multiplayer
3. Implement basic matchmaking queue
4. Test with small group of competitive players
5. Iterate based on feedback

The system is designed to scale from casual play to high-level competitive tournaments, with infrastructure that supports millions of battles and comprehensive anti-cheat measures to ensure fair play.

**Estimated Development Time**: 16 weeks (4 months) for full implementation
**Team Size**: 2-3 developers + 1 game balance designer
**Technology Stack**: WebSocket (multiplayer), IndexedDB (local storage), Node.js backend (validation)

---

**Document Version**: 1.0
**Date**: 2025-10-12
**Author**: Agent 6 - Competitive Strategy Specialist
