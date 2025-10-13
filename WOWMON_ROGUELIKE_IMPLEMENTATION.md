# WoWMon Roguelike: Technical Implementation Guide

## Code Architecture Changes

---

## 1. NEW DATA STRUCTURES

### Meta Progression State
```javascript
const metaProgress = {
    // Persistent currency
    soulShards: 0,
    totalShardsEarned: 0,

    // Unlocks
    unlockedCreatures: new Set(['murloc', 'wisp', 'imp']), // Starters unlocked by default
    unlockedRelics: new Set(),

    // Permanent upgrades purchased
    metaUpgrades: {
        healthBlessing1: false,
        healthBlessing2: false,
        powerBlessing1: false,
        speedBlessing1: false,
        merchantsFavor: false,
        fortunesFriend: false,
        relicSeeker: false,
        soulCollector: false,
        secondWind: false,
        battleHardened: false,
        luckyCharm: false
    },

    // Statistics
    stats: {
        totalRuns: 0,
        totalDeaths: 0,
        deepestFloor: 0,
        totalCreaturesDefeated: 0,
        totalBossesKilled: 0,
        totalGoldEarned: 0,
        totalPlayTime: 0,
        floor50Completions: 0
    },

    // Achievements
    achievements: {},

    // Prestige
    prestigeLevel: 0,
    prestigeRuns: 0
};
```

### Active Run State
```javascript
const activeRun = {
    // Run identification
    seed: 0,
    startTime: Date.now(),

    // Current progress
    currentFloor: 1,
    currentRoom: 0,

    // Team
    team: [],
    teamSlots: 6,

    // Inventory (items consumed during run only)
    inventory: {
        healthPotion: 0,
        manaPotion: 0,
        soulStone: 0,
        greaterSoulStone: 0,
        reviveScroll: 0,
        fullRestore: 0
    },

    // Relics (permanent buffs for this run)
    activeRelics: [],
    maxRelics: 8,

    // Currency (lost on death, converted to shards)
    gold: 0,

    // Run modifiers
    modifiers: [],
    blessings: [],
    curses: [],

    // Floor data
    currentFloorData: null,
    visitedRooms: new Set(),

    // Statistics for this run
    runStats: {
        floorsCleared: 0,
        creaturesDefeated: 0,
        bossesKilled: 0,
        damageDealt: 0,
        damageTaken: 0,
        goldEarned: 0,
        relicsFound: 0,
        creaturesCaptures: 0
    },

    // Used for banking decision
    hasEscapeAvailable: false,
    lastBossFloor: 0
};
```

### Procedural Floor Data
```javascript
const floorData = {
    floorNumber: 1,
    seed: 12345,
    modifier: null, // "fog_of_war", "fel_corruption", etc.

    rooms: [
        {
            id: 0,
            type: 'combat', // combat, elite, treasure, rest, shop, event, boss
            cleared: false,
            connections: [1, 2],

            // Type-specific data
            encounter: {
                creatureId: 'murloc',
                level: 7,
                isElite: false
            }
        },
        // ... more rooms
    ],

    startRoom: 0,
    bossRoom: null, // Set if floor % 5 === 0

    totalRooms: 12,
    roomsCleared: 0
};
```

---

## 2. PROCEDURAL GENERATION SYSTEM

### Seeded Random Number Generator
```javascript
class SeededRNG {
    constructor(seed) {
        this.seed = seed;
        this.state = seed;
    }

    next() {
        // LCG algorithm
        this.state = (this.state * 1103515245 + 12345) & 0x7fffffff;
        return this.state / 0x7fffffff;
    }

    range(min, max) {
        return Math.floor(this.next() * (max - min + 1)) + min;
    }

    choice(array) {
        return array[this.range(0, array.length - 1)];
    }

    shuffle(array) {
        const result = [...array];
        for (let i = result.length - 1; i > 0; i--) {
            const j = this.range(0, i);
            [result[i], result[j]] = [result[j], result[i]];
        }
        return result;
    }

    weighted(weights) {
        const total = weights.reduce((sum, w) => sum + w.weight, 0);
        let rand = this.next() * total;

        for (let i = 0; i < weights.length; i++) {
            rand -= weights[i].weight;
            if (rand <= 0) return weights[i];
        }

        return weights[weights.length - 1];
    }
}
```

### Floor Generator
```javascript
class FloorGenerator {
    constructor(floorNumber, seed) {
        this.floorNumber = floorNumber;
        this.rng = new SeededRNG(seed + floorNumber);
    }

    generate() {
        const roomCount = this.rng.range(8, 15);
        const rooms = [];

        // Determine if this is a boss floor
        const isBossFloor = this.floorNumber % 5 === 0;

        // Generate room types
        const roomTypes = this.generateRoomTypes(roomCount, isBossFloor);

        // Create room objects
        for (let i = 0; i < roomCount; i++) {
            rooms.push({
                id: i,
                type: roomTypes[i],
                cleared: false,
                connections: [],
                data: this.generateRoomData(roomTypes[i])
            });
        }

        // Generate connections (branching paths)
        this.generateConnections(rooms);

        // Select floor modifier
        const modifier = this.selectFloorModifier();

        return {
            floorNumber: this.floorNumber,
            seed: this.rng.seed,
            modifier: modifier,
            rooms: rooms,
            startRoom: 0,
            bossRoom: isBossFloor ? roomCount - 1 : null,
            totalRooms: roomCount,
            roomsCleared: 0
        };
    }

    generateRoomTypes(count, isBossFloor) {
        const weights = this.getRoomWeights();
        const types = [];

        for (let i = 0; i < count; i++) {
            if (isBossFloor && i === count - 1) {
                types.push('boss');
            } else {
                const roomType = this.rng.weighted(weights);
                types.push(roomType.type);
            }
        }

        return types;
    }

    getRoomWeights() {
        // Adjust weights based on floor depth
        const baseCombat = 50;
        const combatIncrease = Math.min(this.floorNumber, 30); // Max +30% at floor 30

        return [
            { type: 'combat', weight: baseCombat + combatIncrease },
            { type: 'elite', weight: 15 },
            { type: 'treasure', weight: Math.max(20 - combatIncrease / 2, 5) },
            { type: 'rest', weight: Math.max(10 - combatIncrease / 3, 5) },
            { type: 'shop', weight: 15 },
            { type: 'event', weight: 10 }
        ];
    }

    generateRoomData(type) {
        switch(type) {
            case 'combat':
                return this.generateCombatEncounter(false);
            case 'elite':
                return this.generateCombatEncounter(true);
            case 'treasure':
                return this.generateTreasure();
            case 'rest':
                return this.generateRestSite();
            case 'shop':
                return this.generateShop();
            case 'event':
                return this.generateEvent();
            case 'boss':
                return this.generateBoss();
            default:
                return {};
        }
    }

    generateCombatEncounter(isElite) {
        const creaturePool = this.getCreaturePoolForFloor();
        const creatureId = this.rng.choice(creaturePool);

        const baseLevel = Math.floor(this.floorNumber * 1.5);
        const level = baseLevel + this.rng.range(-2, 2);

        return {
            type: 'combat',
            creatureId: creatureId,
            level: Math.max(1, level),
            isElite: isElite,
            quantity: isElite ? 1 : (this.rng.next() < 0.2 ? 2 : 1) // 20% chance of 2v1
        };
    }

    getCreaturePoolForFloor() {
        const floor = this.floorNumber;

        if (floor <= 10) {
            return ['murloc', 'kobold', 'imp', 'wisp', 'gnoll'];
        } else if (floor <= 20) {
            return ['murloc_warrior', 'gnoll', 'wolf', 'ghoul', 'spider', 'elemental'];
        } else if (floor <= 30) {
            return ['wolf', 'ghoul', 'spider', 'elemental', 'naga', 'treant', 'orc_grunt', 'whelp'];
        } else if (floor <= 40) {
            return ['dire_wolf', 'abomination', 'nerubian', 'drake', 'orc_warlord', 'banshee', 'phoenix'];
        } else {
            return ['dragon', 'ancient_wisp', 'murloc_king', 'phoenix', 'felhound', 'nerubian'];
        }
    }

    generateTreasure() {
        const treasureCount = this.rng.range(1, 3);
        const treasures = [];

        for (let i = 0; i < treasureCount; i++) {
            const roll = this.rng.next();

            if (roll < 0.5) {
                // Gold
                treasures.push({
                    type: 'gold',
                    amount: this.rng.range(300, 800) * this.floorNumber
                });
            } else if (roll < 0.8) {
                // Item
                treasures.push({
                    type: 'item',
                    itemId: this.rng.choice(['health_potion', 'mana_potion', 'soul_stone', 'revive_scroll'])
                });
            } else if (roll < 0.95) {
                // Relic
                treasures.push({
                    type: 'relic',
                    relicId: this.selectRandomRelic('rare')
                });
            } else {
                // Creature egg
                treasures.push({
                    type: 'creature_egg',
                    creatureId: this.rng.choice(this.getCreaturePoolForFloor()),
                    quality: this.rng.weighted([
                        { type: 'common', weight: 60 },
                        { type: 'uncommon', weight: 25 },
                        { type: 'rare', weight: 12 },
                        { type: 'perfect', weight: 3 }
                    ]).type
                });
            }
        }

        return { treasures };
    }

    generateRestSite() {
        return {
            type: 'rest',
            healAmount: 0.5, // Heal 50% HP
            options: [
                { id: 'heal', name: 'Rest and Heal', effect: 'heal_50_percent' },
                { id: 'upgrade', name: 'Train Creature', effect: 'random_stat_boost' }
            ]
        };
    }

    generateShop() {
        const items = [];
        const itemPool = [
            { id: 'health_potion', price: 300, stock: 3 },
            { id: 'mana_potion', price: 200, stock: 3 },
            { id: 'soul_stone', price: 500, stock: 5 },
            { id: 'greater_soul_stone', price: 1200, stock: 2 },
            { id: 'revive_scroll', price: 800, stock: 2 },
            { id: 'full_restore', price: 1500, stock: 1 }
        ];

        // Randomize shop inventory
        const shopItems = this.rng.shuffle(itemPool).slice(0, this.rng.range(3, 5));

        // Chance for relic
        if (this.rng.next() < 0.3) {
            shopItems.push({
                id: this.selectRandomRelic('uncommon'),
                price: this.rng.range(2000, 4000),
                stock: 1
            });
        }

        return { items: shopItems };
    }

    generateEvent() {
        const events = [
            'demon_altar',
            'mysterious_egg',
            'cursed_shrine',
            'soul_trade',
            'ancient_fountain',
            'wandering_merchant',
            'creature_trainer',
            'mysterious_portal'
        ];

        return {
            type: 'event',
            eventId: this.rng.choice(events)
        };
    }

    generateBoss() {
        const bossCreatures = {
            5: 'orc_grunt',
            10: 'drake',
            15: 'treant',
            20: 'abomination',
            25: 'phoenix',
            30: 'nerubian',
            35: 'ancient_wisp',
            40: 'orc_warlord',
            45: 'dragon',
            50: 'murloc_king' // Final boss
        };

        const bossCreature = bossCreatures[this.floorNumber] || 'dragon';
        const bossLevel = this.floorNumber * 2;

        return {
            type: 'boss',
            creatureId: bossCreature,
            level: bossLevel,
            isBoss: true,
            reward: {
                gold: this.floorNumber * 500,
                guaranteedRelic: true,
                relicRarity: this.floorNumber >= 40 ? 'legendary' :
                              this.floorNumber >= 25 ? 'epic' : 'rare'
            }
        };
    }

    generateConnections(rooms) {
        // Create branching path structure
        // Simple implementation: each room connects to 1-2 forward rooms

        for (let i = 0; i < rooms.length - 1; i++) {
            const connectionCount = this.rng.range(1, 2);

            for (let j = 0; j < connectionCount; j++) {
                const targetRoom = Math.min(i + this.rng.range(1, 3), rooms.length - 1);

                if (!rooms[i].connections.includes(targetRoom)) {
                    rooms[i].connections.push(targetRoom);
                }
            }
        }

        // Ensure last room is reachable
        if (rooms[rooms.length - 2].connections.length === 0) {
            rooms[rooms.length - 2].connections.push(rooms.length - 1);
        }
    }

    selectFloorModifier() {
        // 30% chance for floor modifier
        if (this.rng.next() < 0.3) {
            const modifiers = [
                { id: 'fog_of_war', name: 'Fog of War', effect: 'limited_visibility' },
                { id: 'fel_corruption', name: 'Fel Corruption', effect: 'demon_boost' },
                { id: 'undead_rising', name: 'Undead Rising', effect: 'more_undead' },
                { id: 'treasure_hunt', name: 'Treasure Hunt', effect: 'more_treasure' },
                { id: 'elite_zone', name: 'Elite Zone', effect: 'all_elite' },
                { id: 'blessed_halls', name: 'Blessed Halls', effect: 'more_rest' },
                { id: 'cursed_floor', name: 'Cursed Floor', effect: 'debuff_inflict' }
            ];

            return this.rng.choice(modifiers);
        }

        return null;
    }

    selectRandomRelic(minRarity) {
        // This would pull from your relic database
        // Placeholder implementation
        const relicsByRarity = {
            common: ['minor_health_ring', 'attack_shard', 'speed_boots'],
            uncommon: ['vampiric_fang', 'critical_eye', 'element_stone'],
            rare: ['lifesteal_fang', 'dragon_tooth', 'shadow_orb'],
            epic: ['phoenix_feather', 'dragons_hoard', 'evolution_catalyst'],
            legendary: ['crown_lich_king', 'heart_azeroth', 'infinity_stone']
        };

        let availableRelics = [];

        switch(minRarity) {
            case 'legendary':
                availableRelics = relicsByRarity.legendary;
                break;
            case 'epic':
                availableRelics = [...relicsByRarity.epic, ...relicsByRarity.legendary];
                break;
            case 'rare':
                availableRelics = [...relicsByRarity.rare, ...relicsByRarity.epic];
                break;
            default:
                availableRelics = [...relicsByRarity.common, ...relicsByRarity.uncommon];
        }

        return this.rng.choice(availableRelics);
    }
}
```

---

## 3. STATE MANAGEMENT SYSTEM

### Save Manager
```javascript
class SaveManager {
    constructor() {
        this.META_KEY = 'wowmon_roguelike_meta';
        this.RUN_KEY = 'wowmon_roguelike_run';
    }

    // Meta progress (persistent)
    saveMetaProgress(metaData) {
        try {
            localStorage.setItem(this.META_KEY, JSON.stringify(metaData));
            return true;
        } catch(e) {
            console.error('Failed to save meta progress:', e);
            return false;
        }
    }

    loadMetaProgress() {
        try {
            const saved = localStorage.getItem(this.META_KEY);
            return saved ? JSON.parse(saved) : this.getDefaultMetaProgress();
        } catch(e) {
            console.error('Failed to load meta progress:', e);
            return this.getDefaultMetaProgress();
        }
    }

    getDefaultMetaProgress() {
        return {
            soulShards: 0,
            totalShardsEarned: 0,
            unlockedCreatures: ['murloc', 'wisp', 'imp'],
            unlockedRelics: [],
            metaUpgrades: {},
            stats: {
                totalRuns: 0,
                totalDeaths: 0,
                deepestFloor: 0,
                totalCreaturesDefeated: 0,
                totalBossesKilled: 0,
                totalGoldEarned: 0,
                totalPlayTime: 0,
                floor50Completions: 0
            },
            achievements: {},
            prestigeLevel: 0
        };
    }

    // Active run (temporary)
    saveActiveRun(runData) {
        try {
            localStorage.setItem(this.RUN_KEY, JSON.stringify(runData));
            return true;
        } catch(e) {
            console.error('Failed to save active run:', e);
            return false;
        }
    }

    loadActiveRun() {
        try {
            const saved = localStorage.getItem(this.RUN_KEY);
            return saved ? JSON.parse(saved) : null;
        } catch(e) {
            console.error('Failed to load active run:', e);
            return null;
        }
    }

    clearActiveRun() {
        localStorage.removeItem(this.RUN_KEY);
    }

    // Auto-save functionality
    autoSave(metaData, runData) {
        this.saveMetaProgress(metaData);
        if (runData) {
            this.saveActiveRun(runData);
        }
    }

    // Export/Import for cross-device sync
    exportAllData() {
        return {
            meta: this.loadMetaProgress(),
            run: this.loadActiveRun(),
            version: '1.0.0',
            exportDate: Date.now()
        };
    }

    importAllData(data) {
        if (data.version !== '1.0.0') {
            throw new Error('Incompatible save version');
        }

        this.saveMetaProgress(data.meta);
        if (data.run) {
            this.saveActiveRun(data.run);
        }
    }
}
```

---

## 4. GAME STATE TRANSITIONS

### Game State Machine
```javascript
class RoguelikeGameState {
    constructor() {
        this.state = 'META_HUB'; // Current state
        this.states = {
            META_HUB: 'meta_hub',
            RUN_SETUP: 'run_setup',
            FLOOR_MAP: 'floor_map',
            ROOM_ENTER: 'room_enter',
            COMBAT: 'combat',
            EVENT: 'event',
            REWARD: 'reward',
            DEATH: 'death',
            VICTORY: 'victory',
            RUN_SUMMARY: 'run_summary'
        };
    }

    transition(newState) {
        console.log(`State transition: ${this.state} → ${newState}`);
        this.state = newState;
        this.onStateChange(newState);
    }

    onStateChange(state) {
        // Update UI based on state
        switch(state) {
            case this.states.META_HUB:
                this.showMetaHub();
                break;
            case this.states.RUN_SETUP:
                this.showRunSetup();
                break;
            case this.states.FLOOR_MAP:
                this.showFloorMap();
                break;
            case this.states.COMBAT:
                this.startCombat();
                break;
            case this.states.DEATH:
                this.handleDeath();
                break;
            // ... etc
        }
    }

    showMetaHub() {
        // Hide game screens, show meta hub UI
        document.getElementById('metaHub').style.display = 'block';
        document.getElementById('dungeonView').style.display = 'none';
    }

    // ... more state handlers
}
```

---

## 5. PERMADEATH HANDLER

### Death System
```javascript
class DeathHandler {
    constructor(game) {
        this.game = game;
        this.saveManager = new SaveManager();
    }

    handleDeath() {
        const runData = this.game.activeRun;
        const metaData = this.game.metaProgress;

        // Calculate soul shards earned
        const goldToShards = Math.floor(runData.gold / 10);
        const floorBonus = runData.currentFloor * 10;
        const bossBonus = runData.runStats.bossesKilled * 50;

        const totalShards = goldToShards + floorBonus + bossBonus;

        // Apply soul collector upgrade
        const soulCollectorBonus = metaData.metaUpgrades.soulCollector ? 1.5 : 1.0;
        const finalShards = Math.floor(totalShards * soulCollectorBonus);

        // Update meta progress
        metaData.soulShards += finalShards;
        metaData.totalShardsEarned += finalShards;
        metaData.stats.totalRuns++;
        metaData.stats.totalDeaths++;
        metaData.stats.deepestFloor = Math.max(metaData.stats.deepestFloor, runData.currentFloor);
        metaData.stats.totalCreaturesDefeated += runData.runStats.creaturesDefeated;
        metaData.stats.totalBossesKilled += runData.runStats.bossesKilled;
        metaData.stats.totalGoldEarned += runData.runStats.goldEarned;

        // Check for achievements
        this.checkAchievements(metaData, runData);

        // Save meta progress
        this.saveManager.saveMetaProgress(metaData);

        // Clear active run
        this.saveManager.clearActiveRun();

        // Show death summary
        this.showDeathSummary(runData, finalShards);
    }

    checkAchievements(metaData, runData) {
        // Floor milestones
        if (runData.currentFloor >= 5 && !metaData.achievements.floor_5) {
            this.unlockAchievement(metaData, 'floor_5', 'Surface Dweller', 500);
        }
        if (runData.currentFloor >= 10 && !metaData.achievements.floor_10) {
            this.unlockAchievement(metaData, 'floor_10', 'Into Darkness', 1000);
        }
        // ... more achievements
    }

    unlockAchievement(metaData, id, name, shardReward) {
        metaData.achievements[id] = {
            name: name,
            unlockedAt: Date.now()
        };
        metaData.soulShards += shardReward;

        console.log(`Achievement Unlocked: ${name} (+${shardReward} shards)`);
    }

    showDeathSummary(runData, shardsEarned) {
        const summary = `
═══════════════════════════════════════
         RUN ENDED - FLOOR ${runData.currentFloor}
═══════════════════════════════════════

PERFORMANCE:
• Floors Cleared: ${runData.runStats.floorsCleared}
• Creatures Defeated: ${runData.runStats.creaturesDefeated}
• Bosses Slain: ${runData.runStats.bossesKilled}
• Damage Dealt: ${runData.runStats.damageDealt}
• Damage Taken: ${runData.runStats.damageTaken}

REWARDS EARNED:
✓ Soul Shards: +${shardsEarned}
${runData.currentFloor > this.game.metaProgress.stats.deepestFloor ? '✓ New Record: Deepest Floor!' : ''}

TOTAL SOUL SHARDS: ${this.game.metaProgress.soulShards}
═══════════════════════════════════════
        `;

        console.log(summary);
        // Display in UI
    }
}
```

---

## 6. INTEGRATION WITH EXISTING BATTLE SYSTEM

The existing battle system can be largely preserved with modifications:

### Battle System Modifications
```javascript
class RoguelikeBattleSystem extends BattleSystem {
    constructor() {
        super();
        this.activeRelics = [];
    }

    // Override damage calculation to include relic effects
    calculateDamage(attacker, defender, move) {
        let baseDamage = super.calculateDamage(attacker, defender, move);

        // Apply relic modifiers
        for (const relic of this.activeRelics) {
            baseDamage = this.applyRelicEffect(relic, baseDamage, attacker, defender, move);
        }

        return baseDamage;
    }

    applyRelicEffect(relic, damage, attacker, defender, move) {
        switch(relic.id) {
            case 'attack_shard':
                return damage * 1.1; // +10% damage

            case 'dragon_tooth':
                if (attacker.type.includes('dragon')) {
                    return damage * 1.15; // +15% for dragons
                }
                return damage;

            case 'critical_eye':
                if (Math.random() < 0.15) {
                    console.log('Critical hit!');
                    return damage * 2;
                }
                return damage;

            case 'lifesteal_fang':
                const healAmount = Math.floor(damage * 0.1);
                attacker.hp = Math.min(attacker.maxHp, attacker.hp + healAmount);
                console.log(`Lifesteal: ${healAmount} HP`);
                return damage;

            // ... more relic effects

            default:
                return damage;
        }
    }

    // Add end-of-battle rewards
    endBattle(won) {
        super.endBattle(won);

        if (won) {
            this.distributeRewards();
        }
    }

    distributeRewards() {
        // Calculate gold earned
        const goldReward = this.calculateGoldReward();

        // Apply fortune's friend upgrade
        if (this.game.metaProgress.metaUpgrades.fortunesFriend) {
            goldReward *= 1.25;
        }

        this.game.activeRun.gold += goldReward;

        // Update run stats
        this.game.activeRun.runStats.creaturesDefeated++;

        console.log(`Victory! +${goldReward} gold`);
    }
}
```

---

## 7. UI COMPONENTS

### Meta Hub Component
```javascript
class MetaHubUI {
    constructor(game) {
        this.game = game;
    }

    render() {
        const meta = this.game.metaProgress;

        return `
            <div class="meta-hub">
                <h1>CHAMBER OF CHAMPIONS</h1>

                <div class="meta-stats">
                    <p>Soul Shards: ${meta.soulShards}</p>
                    <p>Best Run: Floor ${meta.stats.deepestFloor}</p>
                    <p>Total Runs: ${meta.stats.totalRuns}</p>
                </div>

                <div class="meta-actions">
                    <button onclick="game.startNewRun()">START NEW RUN</button>
                    <button onclick="game.showUnlocks()">UNLOCK CREATURES (${meta.unlockedCreatures.length}/25)</button>
                    <button onclick="game.showRelicUnlocks()">UNLOCK RELICS (${meta.unlockedRelics.length}/80)</button>
                    <button onclick="game.showUpgrades()">PERMANENT UPGRADES</button>
                    <button onclick="game.showAchievements()">ACHIEVEMENTS (${Object.keys(meta.achievements).length}/100)</button>
                </div>
            </div>
        `;
    }
}
```

### Floor Map Component
```javascript
class FloorMapUI {
    constructor(game) {
        this.game = game;
    }

    render() {
        const floor = this.game.activeRun.currentFloorData;
        const currentRoom = floor.rooms[this.game.activeRun.currentRoom];

        let mapHTML = '<div class="floor-map">';
        mapHTML += `<h2>FLOOR ${floor.floorNumber}`;

        if (floor.modifier) {
            mapHTML += ` - "${floor.modifier.name}"`;
        }

        mapHTML += '</h2>';

        // Render room grid
        mapHTML += '<div class="room-grid">';

        for (const room of floor.rooms) {
            const isCurrentRoom = room.id === this.game.activeRun.currentRoom;
            const isCleared = room.cleared;
            const isConnected = currentRoom.connections.includes(room.id);
            const isVisited = this.game.activeRun.visitedRooms.has(room.id);

            const roomClass = `room ${room.type} ${isCurrentRoom ? 'current' : ''} ${isCleared ? 'cleared' : ''} ${isConnected ? 'available' : ''} ${isVisited ? 'visited' : ''}`;

            const roomSymbol = this.getRoomSymbol(room.type, isVisited);

            mapHTML += `<div class="${roomClass}" onclick="game.selectRoom(${room.id})">${roomSymbol}</div>`;
        }

        mapHTML += '</div>';

        // Legend
        mapHTML += '<div class="legend">';
        mapHTML += '<p>[?] = Unknown</p>';
        mapHTML += '<p>[C] = Combat</p>';
        mapHTML += '<p>[E] = Elite</p>';
        mapHTML += '<p>[T] = Treasure</p>';
        mapHTML += '<p>[R] = Rest</p>';
        mapHTML += '<p>[S] = Shop</p>';
        mapHTML += '<p>[!] = Event</p>';
        mapHTML += '<p>[B] = Boss</p>';
        mapHTML += '</div>';

        mapHTML += '</div>';

        return mapHTML;
    }

    getRoomSymbol(type, isVisited) {
        if (!isVisited) return '?';

        switch(type) {
            case 'combat': return 'C';
            case 'elite': return 'E';
            case 'treasure': return 'T';
            case 'rest': return 'R';
            case 'shop': return 'S';
            case 'event': return '!';
            case 'boss': return 'B';
            default: return '?';
        }
    }
}
```

---

## 8. CONVERSION ROADMAP

### Phase 1: Core Systems (Week 1-2)
- [ ] Implement SeededRNG class
- [ ] Implement FloorGenerator class
- [ ] Create meta progression data structure
- [ ] Create active run data structure
- [ ] Implement SaveManager
- [ ] Add state machine

### Phase 2: Procedural Content (Week 3-4)
- [ ] Generate combat encounters
- [ ] Generate treasure rooms
- [ ] Generate shops
- [ ] Generate events
- [ ] Generate boss fights
- [ ] Implement room connections

### Phase 3: Meta Progression (Week 5-6)
- [ ] Implement soul shard economy
- [ ] Create unlock system for creatures
- [ ] Create unlock system for relics
- [ ] Implement permanent upgrades
- [ ] Add achievement system

### Phase 4: UI/UX (Week 7-8)
- [ ] Design and implement Meta Hub screen
- [ ] Design and implement Floor Map screen
- [ ] Design and implement Run Setup screen
- [ ] Design and implement Death Summary screen
- [ ] Update existing battle UI for relics

### Phase 5: Balance & Polish (Week 9-10)
- [ ] Balance soul shard earn rates
- [ ] Balance unlock costs
- [ ] Balance creature stats by floor
- [ ] Balance relic effects
- [ ] Playtest and iterate

### Phase 6: Advanced Features (Week 11-12)
- [ ] Daily challenges
- [ ] Prestige system
- [ ] More events and room types
- [ ] Additional relics
- [ ] Achievement rewards

---

## 9. QUICK START CONVERSION SNIPPET

Here's a minimal example of how to start converting the existing game:

```javascript
// In your existing GameEngine class, add:

class GameEngine {
    constructor() {
        // ... existing code

        // NEW: Roguelike additions
        this.roguelikeMode = true;
        this.saveManager = new SaveManager();
        this.metaProgress = this.saveManager.loadMetaProgress();
        this.activeRun = null;
        this.floorGenerator = null;
    }

    startNewRun(starterCreatureId) {
        // Create new run
        const seed = Date.now();
        this.activeRun = {
            seed: seed,
            startTime: Date.now(),
            currentFloor: 1,
            currentRoom: 0,
            team: [this.createStarterCreature(starterCreatureId)],
            inventory: {},
            activeRelics: [],
            gold: 0,
            runStats: {
                floorsCleared: 0,
                creaturesDefeated: 0,
                bossesKilled: 0,
                damageDealt: 0,
                damageTaken: 0
            }
        };

        // Generate first floor
        this.generateNewFloor(1);

        // Transition to floor map
        this.state = 'FLOOR_MAP';
    }

    generateNewFloor(floorNumber) {
        this.floorGenerator = new FloorGenerator(floorNumber, this.activeRun.seed);
        this.activeRun.currentFloorData = this.floorGenerator.generate();
        this.activeRun.currentRoom = 0;
        this.activeRun.visitedRooms = new Set([0]);
    }

    enterRoom(roomId) {
        const room = this.activeRun.currentFloorData.rooms[roomId];
        this.activeRun.currentRoom = roomId;
        this.activeRun.visitedRooms.add(roomId);

        switch(room.type) {
            case 'combat':
            case 'elite':
                this.startCombatEncounter(room.data);
                break;
            case 'treasure':
                this.openTreasure(room.data);
                break;
            case 'rest':
                this.enterRestSite(room.data);
                break;
            case 'shop':
                this.enterShop(room.data);
                break;
            case 'event':
                this.triggerEvent(room.data);
                break;
            case 'boss':
                this.startBossEncounter(room.data);
                break;
        }

        room.cleared = true;

        // Auto-save after each room
        this.saveManager.autoSave(this.metaProgress, this.activeRun);
    }
}
```

---

## CONCLUSION

This implementation guide provides the technical foundation for converting WoWMon into a roguelike. The key is to:

1. **Preserve** the existing battle system (it's solid)
2. **Replace** the overworld exploration with procedural dungeons
3. **Add** meta-progression and permadeath systems
4. **Refactor** save system for dual-state (meta + run)
5. **Extend** UI for new screens (hub, map, summary)

The conversion can be done incrementally—start with core procedural generation, then add meta-progression, then polish UI. The existing creature/move/battle code can remain largely untouched.

**Estimated total development time:** 8-12 weeks for full conversion with all features.
