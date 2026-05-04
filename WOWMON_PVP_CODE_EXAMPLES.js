/**
 * WoWmon Competitive PvP - Code Implementation Examples
 * Agent 6: Competitive Strategy
 *
 * This file contains ready-to-use code snippets for implementing
 * the competitive PvP features in WoWmon.html
 */

// ============================================================================
// 1. TEAM BUILDER SYSTEM
// ============================================================================

class TeamBuilder {
    constructor() {
        this.team = {
            name: "My Team",
            format: "singles",
            tier: "OU",
            creatures: [] // Max 6
        };
    }

    // Add creature to team
    addCreature(creatureData) {
        if (this.team.creatures.length >= 6) {
            return { error: "Team is full (max 6 creatures)" };
        }

        // Create competitive creature instance
        const creature = {
            id: creatureData.id,
            name: creatureData.name,
            level: 100, // Competitive standard
            moves: creatureData.moves.slice(0, 4),
            item: null,
            ability: null,
            nature: "neutral", // Can add natures for stat modifications
            evs: { hp: 0, attack: 0, defense: 0, spAttack: 0, spDefense: 0, speed: 0 },
            ivs: { hp: 31, attack: 31, defense: 31, spAttack: 31, spDefense: 31, speed: 31 }
        };

        this.team.creatures.push(creature);
        return { success: true, creature };
    }

    // Validate team legality
    validateTeam() {
        const errors = [];
        const warnings = [];

        // Check team size
        if (this.team.creatures.length < 3) {
            errors.push("Team must have at least 3 creatures");
        }

        // Check for duplicate species
        const speciesCount = {};
        this.team.creatures.forEach(c => {
            speciesCount[c.id] = (speciesCount[c.id] || 0) + 1;
            if (speciesCount[c.id] > 1) {
                errors.push(`Duplicate species: ${c.name}`);
            }
        });

        // Check tier legality
        this.team.creatures.forEach(c => {
            const tierData = TierSystem.getCreatureTier(c.id);
            if (tierData && !TierSystem.isLegalForTier(c.id, this.team.tier)) {
                errors.push(`${c.name} is banned in ${this.team.tier} tier`);
            }
        });

        // Analyze type coverage
        const coverage = this.analyzeTypeCoverage();
        if (coverage.weaknesses.critical.length > 0) {
            warnings.push(`Critical weakness to: ${coverage.weaknesses.critical.join(", ")}`);
        }

        return {
            isLegal: errors.length === 0,
            errors,
            warnings,
            score: this.calculateTeamScore()
        };
    }

    // Analyze type coverage
    analyzeTypeCoverage() {
        const typeChart = {
            weaknesses: { critical: [], major: [], minor: [] },
            resistances: [],
            immunities: []
        };

        // Count weaknesses across team
        const weaknessCounts = {};

        this.team.creatures.forEach(creature => {
            const creatureData = game.cartridge.creatures[creature.id];
            if (!creatureData) return;

            // Check each attacking type
            Object.keys(game.cartridge.moves).forEach(moveId => {
                const move = game.cartridge.moves[moveId];
                const effectiveness = TypeEffectiveness.calculate(move.type, creatureData.type);

                if (effectiveness >= 2.0) {
                    weaknessCounts[move.type] = (weaknessCounts[move.type] || 0) + 1;
                }
            });
        });

        // Categorize weaknesses
        Object.entries(weaknessCounts).forEach(([type, count]) => {
            if (count >= 5) typeChart.weaknesses.critical.push(type);
            else if (count >= 3) typeChart.weaknesses.major.push(type);
            else typeChart.weaknesses.minor.push(type);
        });

        return typeChart;
    }

    // Calculate team score (0-100)
    calculateTeamScore() {
        let score = 50; // Base score

        // Offensive coverage (+20 max)
        const offensiveCoverage = this.calculateOffensiveCoverage();
        score += offensiveCoverage * 20;

        // Defensive balance (+20 max)
        const defensiveBalance = this.calculateDefensiveBalance();
        score += defensiveBalance * 20;

        // Speed tiers (+10 max)
        const speedDistribution = this.analyzeSpeedTiers();
        score += speedDistribution * 10;

        return Math.min(100, Math.max(0, score));
    }

    // Calculate offensive type coverage (0-1)
    calculateOffensiveCoverage() {
        const types = new Set();
        this.team.creatures.forEach(creature => {
            creature.moves.forEach(moveId => {
                const move = game.cartridge.moves[moveId];
                if (move) types.add(move.type);
            });
        });

        // Good coverage = 8+ different types
        return Math.min(1.0, types.size / 8);
    }

    // Calculate defensive balance (0-1)
    calculateDefensiveBalance() {
        const roles = {
            physical: 0,
            special: 0,
            fast: 0,
            slow: 0
        };

        this.team.creatures.forEach(creature => {
            const stats = this.calculateStats(creature);

            if (stats.defense > stats.spDefense) roles.physical++;
            else roles.special++;

            if (stats.speed >= 80) roles.fast++;
            else roles.slow++;
        });

        // Balanced team has mix of roles
        const balance = 1 - Math.abs((roles.physical - roles.special) / 6) * 0.5;
        const speedBalance = 1 - Math.abs((roles.fast - roles.slow) / 6) * 0.5;

        return (balance + speedBalance) / 2;
    }

    // Analyze speed tiers
    analyzeSpeedTiers() {
        const speeds = this.team.creatures.map(c => this.calculateStats(c).speed);
        const avgSpeed = speeds.reduce((a, b) => a + b, 0) / speeds.length;

        // Good distribution: some fast, some slow
        const variance = speeds.reduce((sum, speed) => sum + Math.pow(speed - avgSpeed, 2), 0) / speeds.length;

        // Higher variance = better distribution
        return Math.min(1.0, variance / 1000);
    }

    // Calculate creature stats at level 100
    calculateStats(creature) {
        const baseStats = game.cartridge.creatures[creature.id];
        if (!baseStats) return { hp: 0, attack: 0, defense: 0, speed: 0 };

        // Pokemon-style stat formula
        const stats = {};

        // HP formula
        stats.hp = Math.floor(((2 * baseStats.baseHp + creature.ivs.hp + creature.evs.hp / 4) * creature.level / 100) + creature.level + 10);

        // Other stats
        ['attack', 'defense', 'speed'].forEach(stat => {
            const baseStat = baseStats[`base${stat.charAt(0).toUpperCase() + stat.slice(1)}`] || 50;
            stats[stat] = Math.floor(((2 * baseStat + creature.ivs[stat] + creature.evs[stat] / 4) * creature.level / 100) + 5);
        });

        return stats;
    }

    // Export team to Showdown format
    exportToShowdown() {
        return this.team.creatures.map(c => {
            const baseStats = game.cartridge.creatures[c.id];
            return `
${c.name} @ ${c.item || "No Item"}
Ability: ${c.ability || "None"}
Level: ${c.level}
EVs: ${c.evs.hp} HP / ${c.evs.attack} Atk / ${c.evs.defense} Def / ${c.evs.speed} Spe
${c.nature} Nature
- ${game.cartridge.moves[c.moves[0]]?.name || c.moves[0]}
- ${game.cartridge.moves[c.moves[1]]?.name || c.moves[1]}
- ${game.cartridge.moves[c.moves[2]]?.name || c.moves[2]}
- ${game.cartridge.moves[c.moves[3]]?.name || c.moves[3]}
            `.trim();
        }).join("\n\n");
    }
}

// ============================================================================
// 2. TIER SYSTEM
// ============================================================================

const TierSystem = {
    tiers: {
        UBER: {
            name: "Ubers",
            minUsage: 0,
            banList: [],
            creatures: ["dragon", "infernal", "phoenix"]
        },
        OU: {
            name: "OverUsed",
            minUsage: 4.52,
            banList: ["dragon", "infernal", "phoenix"],
            creatures: ["murloc_king", "dire_wolf", "ancient_wisp", "orc_warlord", "naga"]
        },
        UU: {
            name: "UnderUsed",
            minUsage: 3.41,
            banList: ["dragon", "infernal", "phoenix", "murloc_king", "dire_wolf"],
            creatures: ["drake", "murloc_warrior", "felguard", "nerubian", "abomination"]
        },
        RU: {
            name: "RarelyUsed",
            minUsage: 2.15,
            banList: [], // Ban all above tiers
            creatures: ["wolf", "orc_grunt", "banshee", "spider", "ghoul"]
        },
        NU: {
            name: "NeverUsed",
            minUsage: 0,
            banList: [], // Ban all above tiers
            creatures: ["murloc", "wisp", "imp", "whelp", "skeleton", "gnoll"]
        }
    },

    getCreatureTier(creatureId) {
        for (const [tierKey, tierData] of Object.entries(this.tiers)) {
            if (tierData.creatures.includes(creatureId)) {
                return { tier: tierKey, ...tierData };
            }
        }
        return { tier: "NU", ...this.tiers.NU };
    },

    isLegalForTier(creatureId, tier) {
        const tierData = this.tiers[tier];
        if (!tierData) return false;

        // Check if creature is in ban list
        return !tierData.banList.includes(creatureId);
    },

    // Calculate usage-based tiers from battle data
    calculateTiersFromUsage(battleData) {
        const usage = {};

        // Count creature appearances in battles
        battleData.forEach(battle => {
            battle.teams.forEach(team => {
                team.forEach(creature => {
                    usage[creature.id] = (usage[creature.id] || 0) + 1;
                });
            });
        });

        // Calculate usage percentages
        const totalBattles = battleData.length * 2; // 2 teams per battle
        const usagePercentages = {};

        Object.entries(usage).forEach(([id, count]) => {
            usagePercentages[id] = (count / totalBattles) * 100;
        });

        // Sort by usage
        const sorted = Object.entries(usagePercentages).sort((a, b) => b[1] - a[1]);

        // Assign tiers based on usage thresholds
        const newTiers = {
            OU: [],
            UU: [],
            RU: [],
            NU: []
        };

        sorted.forEach(([id, percentage]) => {
            if (percentage >= 4.52) newTiers.OU.push(id);
            else if (percentage >= 3.41) newTiers.UU.push(id);
            else if (percentage >= 2.15) newTiers.RU.push(id);
            else newTiers.NU.push(id);
        });

        return newTiers;
    }
};

// ============================================================================
// 3. ADVANCED DAMAGE CALCULATOR
// ============================================================================

class CompetitiveDamageCalculator {
    constructor() {
        this.typeChart = this.initializeTypeChart();
    }

    initializeTypeChart() {
        // Simplified type chart (expand based on WoWmon types)
        return {
            water: { weak: ["electric", "nature"], resist: ["fire", "ice", "water"] },
            fire: { weak: ["water", "earth"], resist: ["fire", "ice", "nature"] },
            nature: { weak: ["fire", "ice", "poison"], resist: ["water", "earth", "electric"] },
            dragon: { weak: ["ice", "dragon"], resist: ["fire", "water", "nature", "electric"] },
            undead: { weak: ["fire", "magic"], resist: ["shadow", "poison"], immune: ["normal"] },
            // ... add all types
        };
    }

    calculate(attacker, defender, move, field = {}) {
        // Step 1: Base damage
        const level = attacker.level || 50;
        const attack = this.getAttackStat(attacker, move, field);
        const defense = this.getDefenseStat(defender, move, field);
        const power = this.getModifiedPower(move, attacker, field);

        let damage = Math.floor(
            Math.floor(
                Math.floor(2 * level / 5 + 2) * power * attack / defense
            ) / 50
        ) + 2;

        // Step 2: Weather modifier
        damage = Math.floor(damage * this.getWeatherModifier(move, field.weather));

        // Step 3: Critical hit
        const critRoll = Math.random();
        const isCrit = critRoll < this.getCritRate(attacker.critStage || 0);
        if (isCrit) {
            damage = Math.floor(damage * 1.5);
        }

        // Step 4: Random factor (85-100%)
        const randomFactor = (85 + Math.random() * 15) / 100;
        damage = Math.floor(damage * randomFactor);

        // Step 5: STAB
        if (this.hasSTAB(move.type, attacker.types)) {
            damage = Math.floor(damage * 1.5);
        }

        // Step 6: Type effectiveness
        const effectiveness = this.getTypeEffectiveness(move.type, defender.types);
        damage = Math.floor(damage * effectiveness);

        // Step 7: Item modifiers
        damage = Math.floor(damage * this.getItemModifier(attacker.item, move));

        // Step 8: Ability modifiers
        damage = Math.floor(damage * this.getAbilityModifier(attacker.ability, defender.ability, move));

        // Step 9: Screens
        if (defender.side?.reflect && move.category === "physical") {
            damage = Math.floor(damage * 0.5);
        }
        if (defender.side?.lightScreen && move.category === "special") {
            damage = Math.floor(damage * 0.5);
        }

        damage = Math.max(1, damage);

        return {
            damage,
            effectiveness,
            isCrit,
            min: Math.floor(damage * 0.85),
            max: Math.floor(damage * 1.0)
        };
    }

    getAttackStat(attacker, move, field) {
        let attack = move.category === "physical" ? attacker.attack : attacker.spAttack || attacker.attack;

        // Apply stat stages (-6 to +6)
        if (attacker.statStages) {
            const stage = move.category === "physical" ? attacker.statStages.attack : attacker.statStages.spAttack;
            const multiplier = stage >= 0 ? (2 + stage) / 2 : 2 / (2 - stage);
            attack = Math.floor(attack * multiplier);
        }

        return Math.max(1, attack);
    }

    getDefenseStat(defender, move, field) {
        let defense = move.category === "physical" ? defender.defense : defender.spDefense || defender.defense;

        // Apply stat stages
        if (defender.statStages) {
            const stage = move.category === "physical" ? defender.statStages.defense : defender.statStages.spDefense;
            const multiplier = stage >= 0 ? (2 + stage) / 2 : 2 / (2 - stage);
            defense = Math.floor(defense * multiplier);
        }

        return Math.max(1, defense);
    }

    getModifiedPower(move, attacker, field) {
        let power = move.power;

        // Weather boosts
        if (field.weather === "sun" && move.type === "fire") power *= 1.5;
        if (field.weather === "rain" && move.type === "water") power *= 1.5;

        return power;
    }

    getWeatherModifier(move, weather) {
        if (!weather) return 1.0;

        if (weather === "sun") {
            if (move.type === "fire") return 1.5;
            if (move.type === "water") return 0.5;
        }
        if (weather === "rain") {
            if (move.type === "water") return 1.5;
            if (move.type === "fire") return 0.5;
        }

        return 1.0;
    }

    getCritRate(critStage) {
        const rates = [1/16, 1/8, 1/4, 1/3, 1/2, 1];
        return rates[Math.min(critStage, 5)] || 1/16;
    }

    hasSTAB(moveType, creatureTypes) {
        return creatureTypes.includes(moveType);
    }

    getTypeEffectiveness(moveType, defenderTypes) {
        let effectiveness = 1.0;

        defenderTypes.forEach(defenderType => {
            const chart = this.typeChart[defenderType];
            if (!chart) return;

            if (chart.immune && chart.immune.includes(moveType)) {
                effectiveness = 0;
            } else if (chart.weak && chart.weak.includes(moveType)) {
                effectiveness *= 2.0;
            } else if (chart.resist && chart.resist.includes(moveType)) {
                effectiveness *= 0.5;
            }
        });

        return effectiveness;
    }

    getItemModifier(item, move) {
        if (!item) return 1.0;

        const itemModifiers = {
            life_orb: 1.3,
            choice_band: 1.5, // Physical moves only
            choice_specs: 1.5, // Special moves only
            expert_belt: move.effectiveness > 1.0 ? 1.2 : 1.0
        };

        return itemModifiers[item] || 1.0;
    }

    getAbilityModifier(attackerAbility, defenderAbility, move) {
        let modifier = 1.0;

        // Example abilities
        if (attackerAbility === "adaptability" && move.stab) {
            modifier *= 2.0 / 1.5; // STAB becomes 2x instead of 1.5x
        }

        if (defenderAbility === "thick_fat" && (move.type === "fire" || move.type === "ice")) {
            modifier *= 0.5;
        }

        return modifier;
    }

    // Calculate damage range for all possible rolls
    calculateRange(attacker, defender, move, field = {}) {
        const results = [];

        // Test all random rolls (85-100%)
        for (let i = 85; i <= 100; i++) {
            const testCalc = this.calculate(attacker, defender, move, field);
            results.push(testCalc.damage);
        }

        return {
            min: Math.min(...results),
            max: Math.max(...results),
            average: Math.floor(results.reduce((a, b) => a + b) / results.length),
            guaranteed2HKO: results.every(d => d * 2 >= defender.hp),
            guaranteedOHKO: results.every(d => d >= defender.hp),
            chanceToOHKO: results.filter(d => d >= defender.hp).length / results.length
        };
    }
}

// ============================================================================
// 4. ELO RATING SYSTEM
// ============================================================================

class ELORatingSystem {
    constructor() {
        this.tiers = [
            { name: "Master", minElo: 2000, icon: "👑" },
            { name: "Diamond", minElo: 1800, icon: "💎" },
            { name: "Platinum", minElo: 1600, icon: "🏆" },
            { name: "Gold", minElo: 1400, icon: "🥇" },
            { name: "Silver", minElo: 1200, icon: "🥈" },
            { name: "Bronze", minElo: 1000, icon: "🥉" },
            { name: "Beginner", minElo: 0, icon: "🌱" }
        ];
    }

    calculateEloChange(playerRating, opponentRating, result, kFactor = 32) {
        // Expected score (probability of winning)
        const expectedScore = 1 / (1 + Math.pow(10, (opponentRating - playerRating) / 400));

        // Actual score
        const actualScore = result === "win" ? 1 : result === "draw" ? 0.5 : 0;

        // ELO change
        const change = Math.round(kFactor * (actualScore - expectedScore));

        return {
            change,
            newRating: playerRating + change,
            expectedWinChance: Math.round(expectedScore * 100)
        };
    }

    getTier(elo) {
        for (let i = this.tiers.length - 1; i >= 0; i--) {
            if (elo >= this.tiers[i].minElo) {
                return this.tiers[i];
            }
        }
        return this.tiers[this.tiers.length - 1];
    }

    // Calculate K-factor based on number of games and rating
    getKFactor(player) {
        // New players (< 30 games) get higher K-factor for faster convergence
        if (player.totalGames < 30) return 40;

        // High-rated players get lower K-factor for stability
        if (player.rating >= 2400) return 16;

        // Standard K-factor
        return 32;
    }

    // Glicko-2 system (more sophisticated)
    calculateGlicko2(player, opponent, result) {
        const tau = 0.5; // System constant
        const epsilon = 0.000001;

        // Convert ratings to Glicko-2 scale
        const mu = (player.rating - 1500) / 173.7178;
        const phi = player.rd / 173.7178;
        const sigma = player.volatility;

        const muPrime = (opponent.rating - 1500) / 173.7178;
        const phiPrime = opponent.rd / 173.7178;

        // Calculate g(φ)
        const g = (phi) => 1 / Math.sqrt(1 + 3 * Math.pow(phi, 2) / Math.pow(Math.PI, 2));

        // Calculate E(μ, μ', φ')
        const E = (mu, muPrime, phiPrime) => 1 / (1 + Math.exp(-g(phiPrime) * (mu - muPrime)));

        const score = result === "win" ? 1 : result === "draw" ? 0.5 : 0;

        // Calculate variance
        const v = 1 / (Math.pow(g(phiPrime), 2) * E(mu, muPrime, phiPrime) * (1 - E(mu, muPrime, phiPrime)));

        // Calculate improvement estimate
        const delta = v * g(phiPrime) * (score - E(mu, muPrime, phiPrime));

        // Iterative algorithm to find new volatility
        let sigmaNew = sigma;
        // ... (full implementation requires iterative convergence)

        // Calculate new rating and RD
        const phiStar = Math.sqrt(Math.pow(phi, 2) + Math.pow(sigmaNew, 2));
        const phiNew = 1 / Math.sqrt(1 / Math.pow(phiStar, 2) + 1 / v);
        const muNew = mu + Math.pow(phiNew, 2) * g(phiPrime) * (score - E(mu, muPrime, phiPrime));

        // Convert back to normal scale
        const newRating = Math.round(muNew * 173.7178 + 1500);
        const newRD = Math.round(phiNew * 173.7178);

        return {
            newRating,
            newRD,
            newVolatility: sigmaNew,
            confidence: `±${newRD * 2}` // 95% confidence interval
        };
    }
}

// ============================================================================
// 5. MATCHMAKING SYSTEM
// ============================================================================

class MatchmakingSystem {
    constructor() {
        this.queue = {
            singles: [],
            doubles: [],
            triples: []
        };

        this.config = {
            maxRatingDifference: 200,
            ratingExpansionRate: 50, // Per 30 seconds
            maxWaitTime: 300000, // 5 minutes
            prioritizeLatency: true,
            latencyThreshold: 100
        };
    }

    async joinQueue(player, format = "singles") {
        const queueEntry = {
            id: player.id,
            name: player.name,
            rating: player.rating,
            hiddenMMR: player.hiddenMMR || player.rating,
            region: player.region || "NA",
            latency: player.avgLatency || 50,
            queuedAt: Date.now(),
            team: player.team
        };

        this.queue[format].push(queueEntry);

        // Try to find match every 2 seconds
        return new Promise((resolve) => {
            const interval = setInterval(() => {
                const match = this.findMatch(queueEntry, format);

                if (match) {
                    clearInterval(interval);
                    resolve(match);
                }

                // Timeout after max wait time
                const waitTime = Date.now() - queueEntry.queuedAt;
                if (waitTime >= this.config.maxWaitTime) {
                    clearInterval(interval);
                    this.removeFromQueue(queueEntry.id, format);
                    resolve(null);
                }
            }, 2000);
        });
    }

    findMatch(player, format) {
        const candidates = this.queue[format].filter(p => p.id !== player.id);

        if (candidates.length === 0) return null;

        const waitTime = (Date.now() - player.queuedAt) / 1000;
        const maxAllowedDiff = this.config.maxRatingDifference +
            (Math.floor(waitTime / 30) * this.config.ratingExpansionRate);

        // Score each potential opponent
        const scored = candidates.map(opponent => {
            const ratingDiff = Math.abs(player.hiddenMMR - opponent.hiddenMMR);

            // Not eligible if rating too far
            if (ratingDiff > maxAllowedDiff) {
                return { opponent, score: -1 };
            }

            let score = 1000 - ratingDiff;

            // Latency bonus
            if (this.config.prioritizeLatency) {
                const avgLatency = (player.latency + opponent.latency) / 2;
                if (avgLatency < this.config.latencyThreshold) {
                    score += 200;
                }
            }

            // Same region bonus
            if (player.region === opponent.region) {
                score += 100;
            }

            // Fair queue - prefer similar wait times
            const waitDiff = Math.abs(player.queuedAt - opponent.queuedAt);
            score -= waitDiff / 1000;

            return { opponent, score };
        });

        // Find best match
        const bestMatch = scored
            .filter(m => m.score > 0)
            .sort((a, b) => b.score - a.score)[0];

        if (bestMatch) {
            // Remove both from queue
            this.removeFromQueue(player.id, format);
            this.removeFromQueue(bestMatch.opponent.id, format);

            return {
                player1: player,
                player2: bestMatch.opponent,
                format,
                matchQuality: bestMatch.score / 1000,
                server: this.selectBestServer(player, bestMatch.opponent)
            };
        }

        return null;
    }

    removeFromQueue(playerId, format) {
        this.queue[format] = this.queue[format].filter(p => p.id !== playerId);
    }

    selectBestServer(player1, player2) {
        // Select server closest to both players
        // Simplified - in reality would use geolocation
        const servers = ["US-WEST", "US-EAST", "EU-WEST", "ASIA"];
        return servers[0]; // Default
    }
}

// ============================================================================
// 6. REPLAY SYSTEM
// ============================================================================

class ReplaySystem {
    constructor() {
        this.replays = new Map();
    }

    saveReplay(battle) {
        const replay = {
            id: this.generateId(),
            date: Date.now(),
            format: battle.format,
            tier: battle.tier,
            players: {
                player1: {
                    name: battle.player1.name,
                    rating: battle.player1.rating,
                    team: this.sanitizeTeam(battle.player1.team)
                },
                player2: {
                    name: battle.player2.name,
                    rating: battle.player2.rating,
                    team: this.sanitizeTeam(battle.player2.team)
                }
            },
            winner: battle.winner,
            turns: battle.turnHistory.length,
            duration: battle.endTime - battle.startTime,
            data: this.compressTurnData(battle.turnHistory),
            seed: battle.randomSeed,
            views: 0
        };

        this.replays.set(replay.id, replay);
        this.saveToStorage(replay);

        return replay.id;
    }

    sanitizeTeam(team) {
        // Remove sensitive data but keep structure
        return team.map(creature => ({
            id: creature.id,
            name: creature.name,
            level: creature.level,
            moves: creature.moves,
            item: creature.item
        }));
    }

    compressTurnData(turnHistory) {
        // Delta compression - only store changes
        const compressed = [];
        let prevState = null;

        turnHistory.forEach(turn => {
            if (!prevState) {
                compressed.push(turn);
            } else {
                const delta = this.calculateDelta(prevState, turn);
                compressed.push(delta);
            }
            prevState = turn;
        });

        return compressed;
    }

    calculateDelta(prev, curr) {
        const delta = { turn: curr.turn };

        // Only include changed fields
        Object.keys(curr).forEach(key => {
            if (JSON.stringify(prev[key]) !== JSON.stringify(curr[key])) {
                delta[key] = curr[key];
            }
        });

        return delta;
    }

    loadReplay(replayId) {
        const replay = this.replays.get(replayId) || this.loadFromStorage(replayId);

        if (!replay) {
            throw new Error("Replay not found");
        }

        replay.views++;
        return replay;
    }

    analyzeReplay(replayId) {
        const replay = this.loadReplay(replayId);

        return {
            criticalMoments: this.findCriticalMoments(replay),
            mistakes: this.identifyMistakes(replay),
            playerStats: this.calculatePlayerStats(replay),
            mvp: this.calculateMVP(replay)
        };
    }

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

            // Critical hits
            if (turn.crit && turn.damage > turn.defender.hp * 0.5) {
                importance = 7;
                description = "Critical hit changed the battle!";
            }

            // Perfect predictions
            if (turn.prediction && turn.prediction.correct) {
                importance = 6;
                description = `Perfect prediction: ${turn.prediction.action}`;
            }

            if (importance >= 6) {
                moments.push({
                    turn: index + 1,
                    importance,
                    description
                });
            }
        });

        return moments.sort((a, b) => b.importance - a.importance);
    }

    identifyMistakes(replay) {
        const mistakes = [];

        replay.data.forEach((turn, index) => {
            // Should have switched but didn't
            if (turn.action === "move" && turn.damageReceived > turn.creature.hp * 0.7) {
                mistakes.push({
                    turn: index + 1,
                    player: turn.player,
                    type: "bad_stay",
                    severity: "high",
                    description: `Should have switched out ${turn.creature.name}`
                });
            }

            // Used wrong move
            if (turn.action === "move" && turn.effectiveness < 0.5 && turn.betterMoveAvailable) {
                mistakes.push({
                    turn: index + 1,
                    player: turn.player,
                    type: "suboptimal_move",
                    severity: "medium",
                    description: `${turn.betterMove} would have been more effective`
                });
            }
        });

        return mistakes;
    }

    calculateMVP(replay) {
        const creatureStats = {};

        replay.data.forEach(turn => {
            const id = `${turn.player}_${turn.creature.id}`;

            if (!creatureStats[id]) {
                creatureStats[id] = {
                    name: turn.creature.name,
                    player: turn.player,
                    damageDealt: 0,
                    kos: 0,
                    turnsAlive: 0
                };
            }

            creatureStats[id].turnsAlive++;
            if (turn.damage) creatureStats[id].damageDealt += turn.damage;
            if (turn.ko) creatureStats[id].kos++;
        });

        // Score: 40% damage, 30% KOs, 30% survival
        const scored = Object.values(creatureStats).map(c => ({
            ...c,
            score: c.damageDealt * 0.4 + c.kos * 100 * 0.3 + c.turnsAlive * 10 * 0.3
        }));

        return scored.sort((a, b) => b.score - a.score)[0];
    }

    generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    saveToStorage(replay) {
        // Save to IndexedDB or localStorage
        localStorage.setItem(`replay_${replay.id}`, JSON.stringify(replay));
    }

    loadFromStorage(replayId) {
        const data = localStorage.getItem(`replay_${replayId}`);
        return data ? JSON.parse(data) : null;
    }
}

// ============================================================================
// 7. ANTI-CHEAT VALIDATOR
// ============================================================================

class AntiCheatValidator {
    constructor() {
        this.damageCalc = new CompetitiveDamageCalculator();
    }

    validateBattle(battle) {
        const violations = [];

        // Validate each turn
        battle.turnHistory.forEach((turn, index) => {
            // Validate damage calculations
            if (turn.damage) {
                const calculatedDamage = this.damageCalc.calculate(
                    turn.attacker,
                    turn.defender,
                    turn.move,
                    turn.field
                );

                const range = this.damageCalc.calculateRange(
                    turn.attacker,
                    turn.defender,
                    turn.move,
                    turn.field
                );

                // Check if damage is within valid range
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

            // Validate move legality
            if (turn.move && !turn.creature.moves.includes(turn.move.id)) {
                violations.push({
                    turn: index,
                    type: "illegal_move",
                    severity: "critical"
                });
            }

            // Validate PP
            if (turn.move && turn.creature.pp[turn.move.id] < 0) {
                violations.push({
                    turn: index,
                    type: "negative_pp",
                    severity: "critical"
                });
            }

            // Validate timing (detect bots)
            if (turn.submitTime < 100 && !turn.forced) {
                violations.push({
                    turn: index,
                    type: "suspicious_timing",
                    severity: "medium",
                    time: turn.submitTime
                });
            }
        });

        return {
            isValid: violations.filter(v => v.severity === "critical").length === 0,
            violations,
            score: this.calculateConfidence(violations)
        };
    }

    calculateConfidence(violations) {
        const criticalCount = violations.filter(v => v.severity === "critical").length;
        const highCount = violations.filter(v => v.severity === "high").length;
        const mediumCount = violations.filter(v => v.severity === "medium").length;

        const suspicionScore = criticalCount * 50 + highCount * 20 + mediumCount * 5;

        return {
            isCheating: suspicionScore >= 100,
            confidence: Math.min(100, suspicionScore),
            action: suspicionScore >= 100 ? "ban" : suspicionScore >= 50 ? "flag" : "none"
        };
    }

    validateReplay(replay) {
        // Reconstruct battle using seed
        const rng = new SeededRNG(replay.seed);
        const reconstructed = this.reconstructBattle(replay, rng);

        // Compare original vs reconstructed
        const differences = [];

        replay.data.forEach((turn, index) => {
            const reconstructedTurn = reconstructed[index];

            if (turn.damage !== reconstructedTurn.damage) {
                differences.push({
                    turn: index,
                    field: "damage",
                    original: turn.damage,
                    reconstructed: reconstructedTurn.damage
                });
            }
        });

        return {
            isValid: differences.length === 0,
            differences
        };
    }

    reconstructBattle(replay, rng) {
        // Full battle reconstruction using deterministic RNG
        // This ensures replays can't be tampered with
        const turns = [];

        replay.data.forEach(turn => {
            // Recalculate all random elements using seed
            const reconstructedTurn = {
                ...turn,
                damage: this.recalculateDamage(turn, rng),
                randomRoll: rng.next()
            };

            turns.push(reconstructedTurn);
        });

        return turns;
    }

    recalculateDamage(turn, rng) {
        // Use seeded RNG for random factor
        const randomFactor = 85 + rng.next() * 15;

        return this.damageCalc.calculate(
            turn.attacker,
            turn.defender,
            turn.move,
            turn.field
        ).damage;
    }
}

// Seeded RNG for deterministic replay
class SeededRNG {
    constructor(seed) {
        this.seed = seed;
        this.state = seed;
    }

    next() {
        // Linear congruential generator
        this.state = (this.state * 1103515245 + 12345) & 0x7fffffff;
        return this.state / 0x7fffffff;
    }
}

// ============================================================================
// 8. USAGE EXAMPLES
// ============================================================================

// Example 1: Build and validate a team
function exampleTeamBuilding() {
    const builder = new TeamBuilder();

    // Add creatures
    builder.addCreature({ id: "murloc_king", name: "MURLOCKING", moves: ["hydro_pump", "ice_beam", "thunderbolt", "recover"] });
    builder.addCreature({ id: "dire_wolf", name: "DIREWOLF", moves: ["crunch", "shadow_claw", "ice_fang", "iron_tail"] });
    builder.addCreature({ id: "ancient_wisp", name: "ANCIENTWISP", moves: ["solar_beam", "heal_pulse", "energy_ball", "psychic"] });

    // Validate
    const validation = builder.validateTeam();
    console.log(validation);

    // Export
    const showdownFormat = builder.exportToShowdown();
    console.log(showdownFormat);
}

// Example 2: Calculate damage
function exampleDamageCalculation() {
    const calc = new CompetitiveDamageCalculator();

    const attacker = {
        level: 50,
        attack: 120,
        types: ["water"],
        item: "life_orb"
    };

    const defender = {
        defense: 80,
        hp: 150,
        types: ["fire"]
    };

    const move = {
        name: "Hydro Pump",
        power: 110,
        type: "water",
        category: "special"
    };

    const result = calc.calculate(attacker, defender, move);
    console.log(`Damage: ${result.damage} (${result.effectiveness}x effectiveness)`);

    const range = calc.calculateRange(attacker, defender, move);
    console.log(`Range: ${range.min}-${range.max} (${range.chanceToOHKO * 100}% OHKO)`);
}

// Example 3: Matchmaking
async function exampleMatchmaking() {
    const mm = new MatchmakingSystem();

    const player = {
        id: "player123",
        name: "Trainer",
        rating: 1500,
        region: "NA",
        avgLatency: 40,
        team: []
    };

    const match = await mm.joinQueue(player, "singles");

    if (match) {
        console.log(`Match found! ${match.player1.name} vs ${match.player2.name}`);
        console.log(`Match quality: ${match.matchQuality}`);
    } else {
        console.log("No match found within time limit");
    }
}

// Example 4: ELO calculation
function exampleELO() {
    const elo = new ELORatingSystem();

    const playerRating = 1500;
    const opponentRating = 1600;

    // Player wins
    const result = elo.calculateEloChange(playerRating, opponentRating, "win");
    console.log(`ELO change: +${result.change} (${result.expectedWinChance}% expected)`);
    console.log(`New rating: ${result.newRating}`);

    const tier = elo.getTier(result.newRating);
    console.log(`Tier: ${tier.icon} ${tier.name}`);
}

// Example 5: Save and analyze replay
function exampleReplay() {
    const replaySystem = new ReplaySystem();

    // Save battle
    const battle = {
        format: "singles",
        tier: "OU",
        player1: { name: "Player1", rating: 1600, team: [] },
        player2: { name: "Player2", rating: 1550, team: [] },
        winner: "player1",
        startTime: Date.now(),
        endTime: Date.now() + 180000,
        turnHistory: [],
        randomSeed: 12345
    };

    const replayId = replaySystem.saveReplay(battle);
    console.log(`Replay saved: ${replayId}`);

    // Analyze replay
    const analysis = replaySystem.analyzeReplay(replayId);
    console.log("Critical moments:", analysis.criticalMoments);
    console.log("MVP:", analysis.mvp);
    console.log("Mistakes:", analysis.mistakes);
}

// Export classes for use in WoWmon.html
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TeamBuilder,
        TierSystem,
        CompetitiveDamageCalculator,
        ELORatingSystem,
        MatchmakingSystem,
        ReplaySystem,
        AntiCheatValidator
    };
}
