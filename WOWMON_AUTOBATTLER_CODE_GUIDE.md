# WoWmon Auto-Battler - Code Implementation Guide

## 🚀 Quick Start - Key Code Snippets

This guide provides ready-to-implement code snippets for the core auto-battler systems.

---

## 1. Auto-Battle Engine

### Battle Tick System (Core Loop)

```javascript
class AutoBattleEngine {
    constructor(game) {
        this.game = game;
        this.currentBattle = null;
        this.tickInterval = 500; // ms
        this.battleTimer = null;
    }

    startBattle(stage) {
        const enemy = this.generateEnemy(stage);

        this.currentBattle = {
            stage: stage,
            team: this.game.team.getActiveCopy(), // Clone to track battle state
            enemy: enemy,
            turn: 0,
            battleLog: []
        };

        // Start battle tick
        this.battleTimer = setInterval(() => this.battleTick(), this.tickInterval);
        this.game.ui.showBattleScreen(this.currentBattle);
    }

    battleTick() {
        if (!this.currentBattle) return;

        const { team, enemy } = this.currentBattle;

        // Get active creatures (first alive)
        const playerCreature = team.find(c => c.currentHp > 0);
        const enemyCreature = enemy;

        if (!playerCreature) {
            this.endBattle(false); // Player lost
            return;
        }

        if (enemyCreature.currentHp <= 0) {
            this.endBattle(true); // Player won
            return;
        }

        // Determine turn order (speed stat)
        const playerGoesFirst = playerCreature.speed >= enemyCreature.speed;

        if (playerGoesFirst) {
            this.executeTurn(playerCreature, enemyCreature, true);
            if (enemyCreature.currentHp > 0) {
                this.executeTurn(enemyCreature, playerCreature, false);
            }
        } else {
            this.executeTurn(enemyCreature, playerCreature, false);
            if (playerCreature.currentHp > 0) {
                this.executeTurn(playerCreature, enemyCreature, true);
            }
        }

        this.currentBattle.turn++;
        this.game.ui.updateBattleView(this.currentBattle);
    }

    executeTurn(attacker, defender, isPlayer) {
        // Select best move
        const move = this.selectMove(attacker, defender);

        if (!move) {
            this.log(`${attacker.name} has no moves!`);
            return;
        }

        // Reduce PP
        attacker.pp[move.id]--;

        this.log(`${attacker.name} used ${move.name}!`);

        // Check accuracy
        if (Math.random() * 100 > move.accuracy) {
            this.log(`${attacker.name}'s attack missed!`);
            return;
        }

        // Calculate damage
        if (move.power > 0) {
            const damage = this.calculateDamage(attacker, defender, move);
            defender.currentHp = Math.max(0, defender.currentHp - damage);
            this.log(`${defender.name} took ${damage} damage!`);

            // Check for knockout
            if (defender.currentHp === 0) {
                this.log(`${defender.name} fainted!`);
            }
        } else if (move.effect === 'heal') {
            const healAmount = Math.floor(attacker.maxHp * 0.5);
            attacker.currentHp = Math.min(attacker.maxHp, attacker.currentHp + healAmount);
            this.log(`${attacker.name} restored ${healAmount} HP!`);
        } else if (move.effect === 'raise_attack') {
            attacker.attackBoost = (attacker.attackBoost || 0) + 1;
            this.log(`${attacker.name}'s attack rose!`);
        }
    }

    selectMove(attacker, defender) {
        // Get available moves (PP > 0)
        const available = attacker.moves
            .map(moveId => this.game.cartridge.moves[moveId])
            .filter(move => attacker.pp[move.id] > 0);

        if (available.length === 0) {
            return attacker.moves.map(moveId => this.game.cartridge.moves[moveId])[0]; // Struggle
        }

        // Score each move
        let bestMove = available[0];
        let bestScore = 0;

        for (const move of available) {
            let score = move.power;

            // Type effectiveness bonus
            const effectiveness = this.getTypeEffectiveness(move.type, defender.type);
            score *= effectiveness;

            // STAB (Same Type Attack Bonus)
            if (attacker.type.includes(move.type)) {
                score *= 1.5;
            }

            // Healing priority when low HP
            if (move.effect === 'heal' && attacker.currentHp < attacker.maxHp * 0.3) {
                score += 1000;
            }

            // Buff priority early
            if ((move.effect === 'raise_attack' || move.effect === 'defense_up')
                && (!attacker.boosts || attacker.boosts < 2)) {
                score += 500;
            }

            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }

        return bestMove;
    }

    calculateDamage(attacker, defender, move) {
        // Pokemon-style damage formula
        const level = attacker.level;
        const power = move.power;
        const attack = attacker.attack * (1 + (attacker.attackBoost || 0) * 0.5);
        const defense = defender.defense * (1 + (defender.defenseBoost || 0) * 0.5);

        // Base damage
        const levelMod = ((2 * level / 5) + 2);
        const baseDamage = (levelMod * power * (attack / defense) / 50) + 2;

        // Type effectiveness
        const effectiveness = this.getTypeEffectiveness(move.type, defender.type);

        // STAB
        const stab = attacker.type.includes(move.type) ? 1.5 : 1;

        // Random variance (85-100%)
        const random = 0.85 + (Math.random() * 0.15);

        const totalDamage = Math.floor(baseDamage * effectiveness * stab * random);
        return Math.max(1, totalDamage);
    }

    getTypeEffectiveness(attackType, defenderTypes) {
        const chart = {
            water: { fire: 2, water: 0.5, nature: 0.5 },
            fire: { nature: 2, water: 0.5, fire: 0.5 },
            nature: { water: 2, fire: 0.5, nature: 0.5 },
            demon: { nature: 2, shadow: 0.5 },
            shadow: { nature: 2, demon: 0.5 },
            undead: { beast: 2, shadow: 0.5 },
            dragon: { dragon: 2 },
            // ... more type matchups
        };

        let effectiveness = 1;
        for (const defType of defenderTypes) {
            if (chart[attackType] && chart[attackType][defType]) {
                effectiveness *= chart[attackType][defType];
            }
        }
        return effectiveness;
    }

    endBattle(victory) {
        clearInterval(this.battleTimer);

        if (victory) {
            // Award XP
            const xp = this.calculateXP(this.currentBattle.enemy.level);
            this.game.team.awardXP(xp);

            // Award gold
            const gold = 50 + (this.currentBattle.stage * 5);
            this.game.economy.addGold(gold);

            // Attempt catch (5% base chance)
            if (Math.random() < this.game.getCatchRate()) {
                this.game.collection.catch(this.currentBattle.enemy.id);
                this.log(`Caught ${this.currentBattle.enemy.name}!`);
            }

            // Progress stage
            this.game.progression.recordVictory();
            this.log(`Victory! +${xp} XP, +${gold} Gold`);
        } else {
            this.log(`Defeat! Your team needs healing...`);
            this.game.team.healAll(); // Auto-heal on loss
        }

        this.currentBattle = null;
        this.game.ui.hideBattleScreen();

        // Start next battle automatically
        if (victory) {
            setTimeout(() => this.game.progression.nextBattle(), 1000);
        }
    }

    log(message) {
        if (this.currentBattle) {
            this.currentBattle.battleLog.push(message);
        }
        console.log(`[Battle] ${message}`);
    }

    generateEnemy(stage) {
        // Scale enemy to stage
        const baseHp = 100;
        const baseAttack = 50;
        const baseDefense = 50;
        const baseSpeed = 50;

        const scaleFactor = Math.pow(1.15, stage);

        return {
            id: 'murloc', // Random from encounter table
            name: 'Wild Murloc',
            level: Math.floor(stage / 2) + 1,
            currentHp: Math.floor(baseHp * scaleFactor),
            maxHp: Math.floor(baseHp * scaleFactor),
            attack: Math.floor(baseAttack * scaleFactor),
            defense: Math.floor(baseDefense * scaleFactor),
            speed: Math.floor(baseSpeed * scaleFactor),
            type: ['water', 'beast'],
            moves: ['tackle', 'bubble'],
            pp: { tackle: 35, bubble: 30 }
        };
    }
}
```

---

## 2. Team Synergy System

```javascript
class TeamManager {
    constructor(game) {
        this.game = game;
        this.activeTeam = []; // Array of creature IDs
        this.collection = {}; // All caught creatures
        this.maxTeamSize = 3; // Upgradeable to 6-9
    }

    calculateSynergies() {
        const team = this.getActiveCreatures();
        const synergies = [];

        // Count types
        const typeCounts = {};
        team.forEach(creature => {
            creature.type.forEach(type => {
                typeCounts[type] = (typeCounts[type] || 0) + 1;
            });
        });

        // Type synergies
        if (typeCounts.water >= 3) {
            synergies.push({
                id: 'water_pack',
                name: 'Water Pack',
                description: '+25% Water damage',
                bonus: { waterDamage: 1.25 }
            });
        }

        if (typeCounts.demon >= 2) {
            synergies.push({
                id: 'demonic_pact',
                name: 'Demonic Pact',
                description: '+20% attack on kill',
                bonus: { attackOnKill: 1.20 }
            });
        }

        if (typeCounts.nature >= 2) {
            synergies.push({
                id: 'druidic_circle',
                name: 'Druidic Circle',
                description: 'Heal 5% HP/second',
                bonus: { regenPerSecond: 0.05 }
            });
        }

        if (typeCounts.undead >= 3) {
            synergies.push({
                id: 'undead_army',
                name: 'Undead Army',
                description: 'Revive once at 50% HP',
                bonus: { revive: true }
            });
        }

        if (typeCounts.dragon >= 2) {
            synergies.push({
                id: 'dragon_dominance',
                name: 'Dragon Dominance',
                description: '+40% damage vs Dragons',
                bonus: { dragonSlayer: 1.40 }
            });
        }

        // Elemental Chaos - 4+ different types
        const uniqueTypes = Object.keys(typeCounts).length;
        if (uniqueTypes >= 4) {
            synergies.push({
                id: 'elemental_chaos',
                name: 'Elemental Chaos',
                description: '+15% all stats',
                bonus: { allStats: 1.15 }
            });
        }

        // Role synergies
        const roles = team.map(c => c.role || this.inferRole(c));
        if (roles.includes('tank') && roles.includes('healer')) {
            synergies.push({
                id: 'tank_healer',
                name: 'Tank + Healer',
                description: 'Tank takes 30% less damage',
                bonus: { tankDefense: 1.30 }
            });
        }

        if (roles.filter(r => r === 'dps').length >= 2) {
            synergies.push({
                id: 'double_dps',
                name: 'Double DPS',
                description: '+15% attack speed',
                bonus: { attackSpeed: 1.15 }
            });
        }

        return synergies;
    }

    applyTeamBonuses() {
        const synergies = this.calculateSynergies();
        const team = this.getActiveCreatures();

        // Apply bonuses to team stats
        team.forEach(creature => {
            let bonusMultiplier = 1;

            synergies.forEach(synergy => {
                if (synergy.bonus.allStats) {
                    bonusMultiplier *= synergy.bonus.allStats;
                }
                if (synergy.bonus.tankDefense && creature.role === 'tank') {
                    creature.effectiveDefense = creature.defense * synergy.bonus.tankDefense;
                }
                // ... apply other bonuses
            });

            creature.effectiveAttack = creature.attack * bonusMultiplier;
            creature.effectiveDefense = creature.defense * bonusMultiplier;
            creature.effectiveSpeed = creature.speed * bonusMultiplier;
        });

        return synergies;
    }

    inferRole(creature) {
        // Simple role inference based on stats
        const { hp, attack, defense, speed } = creature;
        const total = hp + attack + defense + speed;

        if (hp / total > 0.35 && defense / total > 0.3) return 'tank';
        if (attack / total > 0.35) return 'dps';
        if (defense / total > 0.3 || creature.moves.some(m => m.effect === 'heal')) return 'support';
        return 'dps';
    }

    getActiveCreatures() {
        return this.activeTeam.map(id => this.collection[id]).filter(Boolean);
    }
}
```

---

## 3. Offline Progress System

```javascript
class OfflineProgressCalculator {
    constructor(game) {
        this.game = game;
        this.maxOfflineHours = 8; // Upgradeable
        this.offlineEfficiency = 0.5; // 50% base, upgradeable to 100%
    }

    calculateOfflineProgress() {
        const now = Date.now();
        const lastPlay = this.game.save.lastPlayTime || now;
        const msAway = now - lastPlay;
        const hoursAway = msAway / (1000 * 60 * 60);

        // Cap offline time
        const effectiveHours = Math.min(hoursAway, this.maxOfflineHours);

        if (effectiveHours < 0.1) {
            return null; // Less than 6 minutes, no offline progress
        }

        // Calculate battles per hour
        const avgBattleTime = this.estimateAverageBattleTime(); // seconds
        const battlesPerHour = 3600 / avgBattleTime;
        const totalBattles = Math.floor(battlesPerHour * effectiveHours);

        // Calculate resources
        const avgGoldPerBattle = 50 + (this.game.progression.stage * 5);
        const avgXPPerBattle = 100 * (this.game.progression.stage / 10);

        const offlineGold = Math.floor(totalBattles * avgGoldPerBattle * this.offlineEfficiency);
        const offlineXP = Math.floor(totalBattles * avgXPPerBattle * this.offlineEfficiency);

        // Calculate stage progression (conservative)
        const stageProgress = Math.floor(totalBattles / 10);

        return {
            hoursAway: Math.floor(hoursAway * 10) / 10,
            effectiveHours: Math.floor(effectiveHours * 10) / 10,
            battles: totalBattles,
            gold: offlineGold,
            xp: offlineXP,
            stageProgress: stageProgress,
            wasCaped: hoursAway > this.maxOfflineHours
        };
    }

    estimateAverageBattleTime() {
        // Estimate based on team power vs current stage
        const teamPower = this.game.team.getTotalPower();
        const stageDifficulty = Math.pow(1.15, this.game.progression.stage);

        const powerRatio = teamPower / stageDifficulty;

        // Strong team = fast battles (10s), weak team = slow battles (60s)
        if (powerRatio > 2) return 10;
        if (powerRatio > 1.5) return 20;
        if (powerRatio > 1.2) return 30;
        if (powerRatio > 1) return 40;
        return 60;
    }

    applyOfflineProgress(progress) {
        // Award resources
        this.game.economy.addGold(progress.gold);
        this.game.team.awardXP(progress.xp);

        // Advance stages
        this.game.progression.advanceStages(progress.stageProgress);

        // Apply welcome back bonus
        this.game.applyWelcomeBackBonus();

        return progress;
    }

    applyWelcomeBackBonus() {
        // +50% XP/Gold for next 10 battles
        this.game.buffs.add({
            id: 'welcome_back',
            name: 'Welcome Back!',
            xpMultiplier: 1.5,
            goldMultiplier: 1.5,
            battlesRemaining: 10
        });

        // Calculate rested XP (20% per hour, max 200%)
        const hoursAway = (Date.now() - this.game.save.lastPlayTime) / (1000 * 60 * 60);
        const restedBonus = Math.min(2.0, hoursAway * 0.2);

        if (restedBonus > 0) {
            this.game.buffs.add({
                id: 'rested',
                name: 'Rested',
                xpMultiplier: 1 + restedBonus,
                battlesRemaining: Math.floor(restedBonus * 50) // 50 battles per 100% bonus
            });
        }
    }
}
```

---

## 4. Prestige System

```javascript
class PrestigeSystem {
    constructor(game) {
        this.game = game;
        this.ascensionCount = 0;
        this.totalTokens = 0;
        this.availableTokens = 0;
        this.upgrades = {
            battleSpeed: 0,
            goldMultiplier: 0,
            xpBoost: 0,
            offlineEfficiency: 0,
            offlineCap: 0,
            startingResources: 0,
            teamSize: 0,
            autoEvolution: false,
            shinyChance: 0,
            prestigePower: 0
        };
    }

    calculateTokenReward() {
        const base = 100;
        const stageBonus = this.game.progression.highestStage * 2;
        const achievementBonus = Object.values(this.game.achievements)
            .filter(a => a.unlocked).length * 10;

        // Time bonus - under 7 days
        const runTime = (Date.now() - this.game.save.runStartTime) / (1000 * 60 * 60 * 24);
        const timeBonus = runTime < 7 ? 50 : 0;

        // Collection bonus
        const uniqueCreatures = Object.keys(this.game.collection.caught).length;
        const collectionBonus = uniqueCreatures * 5;

        const total = base + stageBonus + achievementBonus + timeBonus + collectionBonus;

        return {
            base,
            stageBonus,
            achievementBonus,
            timeBonus,
            collectionBonus,
            total
        };
    }

    canAscend() {
        return this.game.progression.stage >= 100; // Beat champion
    }

    performAscension() {
        if (!this.canAscend()) {
            throw new Error('Cannot ascend yet!');
        }

        // Calculate reward
        const reward = this.calculateTokenReward();
        this.availableTokens += reward.total;
        this.totalTokens += reward.total;
        this.ascensionCount++;

        // Save what to keep
        const collectionToKeep = { ...this.game.collection.caught };
        const achievementsToKeep = { ...this.game.achievements };
        const upgradestoKeep = { ...this.upgrades };

        // Reset progression
        this.game.progression.reset();
        this.game.team.resetLevels();
        this.game.economy.reset();

        // Restore what we keep
        this.game.collection.caught = collectionToKeep;
        this.game.achievements = achievementsToKeep;
        this.upgrades = upgradestoKeep;

        // Reset all creatures to level 1
        Object.values(this.game.collection.caught).forEach(creature => {
            creature.level = 1;
            creature.xp = 0;
            creature.currentHp = creature.maxHp;
        });

        // Apply starting resources if upgraded
        if (this.upgrades.startingResources > 0) {
            const startingGold = [1000, 5000, 20000][this.upgrades.startingResources - 1] || 0;
            this.game.economy.addGold(startingGold);
        }

        // Save
        this.game.save.lastAscension = Date.now();
        this.game.save.runStartTime = Date.now();
        this.game.saveGame();

        return reward;
    }

    getUpgradeCost(upgradeId) {
        const costs = {
            battleSpeed: [50, 100, 200, 400, 800],
            goldMultiplier: [100, 200, 400, 800],
            xpBoost: [80, 160, 320, 640],
            offlineEfficiency: [150, 300, 600],
            offlineCap: [200, 400, 800],
            startingResources: [100, 250, 500],
            teamSize: [500, 1000, 2000],
            autoEvolution: [300],
            shinyChance: [500, 1000, 2000],
            prestigePower: [1000] // Infinite
        };

        const currentLevel = this.upgrades[upgradeId];

        if (upgradeId === 'prestigePower') {
            return 1000; // Always 1000
        }

        return costs[upgradeId][currentLevel] || null;
    }

    canAffordUpgrade(upgradeId) {
        const cost = this.getUpgradeCost(upgradeId);
        return cost !== null && this.availableTokens >= cost;
    }

    purchaseUpgrade(upgradeId) {
        if (!this.canAffordUpgrade(upgradeId)) {
            throw new Error('Cannot afford upgrade!');
        }

        const cost = this.getUpgradeCost(upgradeId);
        this.availableTokens -= cost;

        if (upgradeId === 'autoEvolution') {
            this.upgrades[upgradeId] = true;
        } else {
            this.upgrades[upgradeId]++;
        }

        this.game.saveGame();
        return this.upgrades[upgradeId];
    }

    getUpgradeEffect(upgradeId) {
        const level = this.upgrades[upgradeId];

        const effects = {
            battleSpeed: level * -10, // -10% per level
            goldMultiplier: level * 25, // +25% per level
            xpBoost: level * 20, // +20% per level
            offlineEfficiency: level * 25, // +25% per level (50% → 100%)
            offlineCap: level * 4, // +4 hours per level
            teamSize: level, // +1 slot per level
            shinyChance: Math.pow(2, level), // 2×/4×/8×
            prestigePower: level * 5 // +5% per ascension
        };

        return effects[upgradeId] || 0;
    }

    applyPrestigeBonuses() {
        // Called when calculating stats
        const bonuses = {
            battleSpeedMult: 1 + (this.getUpgradeEffect('battleSpeed') / 100),
            goldMult: 1 + (this.getUpgradeEffect('goldMultiplier') / 100),
            xpMult: 1 + (this.getUpgradeEffect('xpBoost') / 100),
            offlineEfficiency: 0.5 + (this.getUpgradeEffect('offlineEfficiency') / 100),
            offlineCapHours: 8 + this.getUpgradeEffect('offlineCap'),
            maxTeamSize: 3 + this.getUpgradeEffect('teamSize'),
            shinyMult: this.getUpgradeEffect('shinyChance') || 1,
            prestigePowerBonus: 1 + (this.getUpgradeEffect('prestigePower') / 100)
        };

        return bonuses;
    }
}
```

---

## 5. UI Manager

```javascript
class UIManager {
    constructor(game) {
        this.game = game;
        this.elements = {};
        this.init();
    }

    init() {
        // Cache DOM elements
        this.elements = {
            battleScreen: document.getElementById('battleScreen'),
            teamView: document.getElementById('teamView'),
            collectionBtn: document.getElementById('collectionBtn'),
            shopBtn: document.getElementById('shopBtn'),
            prestigeBtn: document.getElementById('prestigeBtn'),
            goldDisplay: document.getElementById('goldDisplay'),
            stageDisplay: document.getElementById('stageDisplay'),
            progressBar: document.getElementById('progressBar')
        };

        this.bindEvents();
        this.updateMainView();
    }

    bindEvents() {
        this.elements.collectionBtn?.addEventListener('click', () => this.showCollection());
        this.elements.shopBtn?.addEventListener('click', () => this.showShop());
        this.elements.prestigeBtn?.addEventListener('click', () => this.showPrestigeScreen());
    }

    updateMainView() {
        // Update gold display
        if (this.elements.goldDisplay) {
            this.elements.goldDisplay.textContent = this.formatNumber(this.game.economy.gold);
        }

        // Update stage
        if (this.elements.stageDisplay) {
            this.elements.stageDisplay.textContent = `Stage ${this.game.progression.stage}`;
        }

        // Update progress bar
        if (this.elements.progressBar) {
            const progress = (this.game.progression.defeatedThisStage / 10) * 100;
            this.elements.progressBar.style.width = `${progress}%`;
        }

        // Update team display
        this.updateTeamDisplay();

        // Update synergies
        this.updateSynergiesDisplay();
    }

    updateBattleView(battle) {
        const battleLog = this.elements.battleScreen.querySelector('.battle-log');
        const latestLog = battle.battleLog[battle.battleLog.length - 1];

        if (latestLog && battleLog) {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.textContent = latestLog;
            battleLog.appendChild(logEntry);

            // Auto-scroll
            battleLog.scrollTop = battleLog.scrollHeight;
        }

        // Update HP bars
        this.updateHPBar('player', battle.team[0]);
        this.updateHPBar('enemy', battle.enemy);
    }

    updateHPBar(side, creature) {
        const hpBar = document.getElementById(`${side}HpBar`);
        if (!hpBar || !creature) return;

        const percent = (creature.currentHp / creature.maxHp) * 100;
        hpBar.style.width = `${percent}%`;

        // Color based on HP
        if (percent > 50) {
            hpBar.style.background = 'linear-gradient(90deg, #10b981, #3b82f6)';
        } else if (percent > 25) {
            hpBar.style.background = 'linear-gradient(90deg, #fbbf24, #f59e0b)';
        } else {
            hpBar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
    }

    updateTeamDisplay() {
        const container = this.elements.teamView;
        if (!container) return;

        container.innerHTML = '';

        const team = this.game.team.getActiveCreatures();
        team.forEach((creature, index) => {
            const slot = document.createElement('div');
            slot.className = 'team-slot';
            slot.innerHTML = `
                <div class="creature-icon">${this.getCreatureIcon(creature.id)}</div>
                <div class="creature-level">Lv${creature.level}</div>
                <div class="hp-mini-bar">
                    <div class="hp-mini-fill" style="width: ${(creature.currentHp/creature.maxHp)*100}%"></div>
                </div>
            `;
            container.appendChild(slot);
        });
    }

    updateSynergiesDisplay() {
        const synergies = this.game.team.calculateSynergies();
        const container = document.getElementById('synergiesDisplay');

        if (!container) return;

        container.innerHTML = '<h3>Active Synergies</h3>';

        if (synergies.length === 0) {
            container.innerHTML += '<p class="no-synergies">No active synergies</p>';
            return;
        }

        synergies.forEach(synergy => {
            const synergyEl = document.createElement('div');
            synergyEl.className = 'synergy-item';
            synergyEl.innerHTML = `
                <span class="synergy-icon">✅</span>
                <span class="synergy-name">${synergy.name}</span>
                <span class="synergy-desc">${synergy.description}</span>
            `;
            container.appendChild(synergyEl);
        });
    }

    showOfflineProgress(progress) {
        const modal = document.createElement('div');
        modal.className = 'offline-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h2>Welcome Back!</h2>
                <p>You were away for ${progress.hoursAway} hours</p>
                <div class="offline-rewards">
                    <div class="reward">
                        <span class="reward-icon">💰</span>
                        <span class="reward-amount">+${this.formatNumber(progress.gold)} Gold</span>
                    </div>
                    <div class="reward">
                        <span class="reward-icon">⭐</span>
                        <span class="reward-amount">+${this.formatNumber(progress.xp)} XP</span>
                    </div>
                    <div class="reward">
                        <span class="reward-icon">🎯</span>
                        <span class="reward-amount">+${progress.stageProgress} Stages</span>
                    </div>
                </div>
                ${progress.wasCapped ? '<p class="cap-warning">⚠️ Offline progress was capped. Upgrade offline cap!</p>' : ''}
                <button onclick="this.closest('.offline-modal').remove()">Collect!</button>
            </div>
        `;
        document.body.appendChild(modal);
    }

    formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return Math.floor(num).toString();
    }

    getCreatureIcon(creatureId) {
        const icons = {
            murloc: '🐸',
            wisp: '✨',
            imp: '🔥',
            wolf: '🐺',
            dragon: '🐉',
            // ... more
        };
        return icons[creatureId] || '❓';
    }
}
```

---

## 6. Save/Load System

```javascript
class SaveManager {
    constructor(game) {
        this.game = game;
        this.saveKey = 'wowmon_autobattler';
        this.version = '1.0';
    }

    saveGame() {
        const saveData = {
            version: this.version,
            lastUpdate: Date.now(),
            lastPlayTime: Date.now(),
            runStartTime: this.game.save.runStartTime || Date.now(),

            progression: {
                stage: this.game.progression.stage,
                highestStage: this.game.progression.highestStage,
                defeatedThisStage: this.game.progression.defeatedThisStage,
                totalBattles: this.game.progression.totalBattles,
                totalVictories: this.game.progression.totalVictories
            },

            team: {
                active: this.game.team.activeTeam,
                collection: this.game.team.collection
            },

            resources: {
                gold: this.game.economy.gold,
                essence: this.game.economy.essence,
                fragments: this.game.economy.fragments
            },

            prestige: {
                ascensionCount: this.game.prestige.ascensionCount,
                totalTokens: this.game.prestige.totalTokens,
                availableTokens: this.game.prestige.availableTokens,
                upgrades: this.game.prestige.upgrades
            },

            achievements: this.game.achievements,
            dailyQuests: this.game.dailyQuests,
            settings: this.game.settings
        };

        try {
            localStorage.setItem(this.saveKey, JSON.stringify(saveData));
            return true;
        } catch (e) {
            console.error('Save failed:', e);
            return false;
        }
    }

    loadGame() {
        try {
            const saveData = localStorage.getItem(this.saveKey);
            if (!saveData) return null;

            const data = JSON.parse(saveData);

            // Version check
            if (data.version !== this.version) {
                console.warn('Save version mismatch, attempting migration...');
                // Implement migration logic if needed
            }

            return data;
        } catch (e) {
            console.error('Load failed:', e);
            return null;
        }
    }

    exportSave() {
        const saveData = this.saveGame();
        const blob = new Blob([JSON.stringify(saveData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `wowmon-autobattler-save-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    importSave(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                localStorage.setItem(this.saveKey, JSON.stringify(data));
                location.reload();
            } catch (err) {
                alert('Invalid save file!');
            }
        };
        reader.readAsText(file);
    }

    deleteSave() {
        if (confirm('Delete all save data? This cannot be undone!')) {
            localStorage.removeItem(this.saveKey);
            location.reload();
        }
    }

    // Auto-save every 30 seconds
    startAutoSave() {
        setInterval(() => this.saveGame(), 30000);
    }
}
```

---

## 7. Main Game Class

```javascript
class WoWmonAutoBattler {
    constructor() {
        this.cartridge = null; // Creature/move data
        this.save = null;

        // Systems
        this.battle = new AutoBattleEngine(this);
        this.team = new TeamManager(this);
        this.progression = new ProgressionSystem(this);
        this.prestige = new PrestigeSystem(this);
        this.economy = new Economy(this);
        this.collection = new CollectionManager(this);
        this.offline = new OfflineProgressCalculator(this);
        this.ui = new UIManager(this);
        this.saveManager = new SaveManager(this);

        this.init();
    }

    async init() {
        // Load cartridge (creature data)
        await this.loadCartridge();

        // Load save or start new game
        const saveData = this.saveManager.loadGame();
        if (saveData) {
            this.loadSaveData(saveData);

            // Calculate offline progress
            const offlineProgress = this.offline.calculateOfflineProgress();
            if (offlineProgress) {
                this.offline.applyOfflineProgress(offlineProgress);
                this.ui.showOfflineProgress(offlineProgress);
            }
        } else {
            this.startNewGame();
        }

        // Start auto-save
        this.saveManager.startAutoSave();

        // Start game loop
        this.startGameLoop();
    }

    startGameLoop() {
        // Main game loop - check if we should start next battle
        setInterval(() => {
            if (!this.battle.currentBattle) {
                this.progression.startNextBattle();
            }
        }, 1000);

        // UI update loop
        setInterval(() => {
            this.ui.updateMainView();
        }, 100);
    }

    startNewGame() {
        this.save = {
            runStartTime: Date.now(),
            lastPlayTime: Date.now()
        };

        // Give starter creatures
        const starters = ['murloc', 'wisp', 'imp'];
        starters.forEach(id => {
            this.collection.catch(id);
        });

        // Set active team
        this.team.activeTeam = Object.keys(this.collection.caught).slice(0, 3);
    }
}

// Start game
window.addEventListener('DOMContentLoaded', () => {
    window.game = new WoWmonAutoBattler();
});
```

---

## 🎯 Integration Checklist

- [ ] Copy auto-battle engine into wowMon.html
- [ ] Replace manual battle system with auto-battle
- [ ] Implement team synergy calculations
- [ ] Add offline progress on game load
- [ ] Create prestige UI and mechanics
- [ ] Update save/load to include new systems
- [ ] Add UI for synergies display
- [ ] Implement welcome back bonuses
- [ ] Test offline calculations
- [ ] Balance progression rates
- [ ] Add daily quests
- [ ] Polish UI/UX

---

## 📝 Next Steps

1. **Test auto-battle** - Ensure battles run smoothly without player input
2. **Tune balance** - Adjust damage, XP, gold rates
3. **Test offline** - Leave game for various times, check calculations
4. **Add synergies** - Implement type/role bonuses
5. **Polish UI** - Make it clear what's happening
6. **Playtest** - Get 5-10 people to try it

---

**Last Updated:** 2025-10-12
**Version:** 1.0
**Status:** Ready for Implementation
