/**
 * WoWmon Metroidvania - Code Implementation Examples
 * Agent 7: Exploration Strategy
 *
 * This file contains example code snippets for implementing the Metroidvania redesign.
 * These can be integrated into the existing wowMon.html file.
 */

// ===================================================================
// 1. ENHANCED MAP SYSTEM WITH INTERCONNECTIONS
// ===================================================================

class MetroidvaniaMapSystem {
    constructor() {
        this.zones = new Map();
        this.currentZone = 'goldshire';
        this.discoveredZones = new Set(['goldshire']);
        this.unlockedConnections = new Set();
        this.playerAbilities = new Set();

        this.initializeWorldData();
    }

    initializeWorldData() {
        // Goldshire - Central Hub
        this.addZone('goldshire', {
            name: 'Goldshire',
            size: { width: 40, height: 40 },
            tileData: [], // 40x40 tile array
            connections: [
                { to: 'dark_forest', x: 20, y: 0, requirement: null, direction: 'north' },
                { to: 'sunken_ruins', x: 0, y: 20, requirement: null, direction: 'west' },
                { to: 'burning_wastes', x: 39, y: 20, requirement: 'tree_cut', direction: 'east' },
                { to: 'underground_depths', x: 20, y: 39, requirement: 'rock_smash', direction: 'south' },
                { to: 'shadow_crypts', x: 15, y: 35, requirement: 'shadow_walk', hidden: true, direction: 'down' }
            ],
            landmarks: [
                { id: 'inn', name: "Lion's Pride Inn", x: 20, y: 20, icon: '🏠', type: 'healing' },
                { id: 'oak', name: 'Great Oak', x: 25, y: 15, icon: '🌳', type: 'landmark' },
                { id: 'well', name: 'Well of Worlds', x: 18, y: 25, icon: '⚪', type: 'warp', hidden: true }
            ],
            secrets: [
                {
                    id: 'goldshire_exp_share',
                    x: 18, y: 26,
                    requirement: 'swimming',
                    type: 'hidden_item',
                    reward: { item: 'exp_share', quantity: 1 }
                }
            ],
            encounters: {
                base: ['gnoll', 'kobold', 'wisp'],
                scaled: {
                    2: ['wolf', 'spider'],
                    4: ['dire_wolf', 'nerubian'],
                    8: ['legendary_beast']
                }
            },
            warpShrineLocation: { x: 20, y: 18 }
        });

        // Dark Forest - Nature Zone
        this.addZone('dark_forest', {
            name: 'Dark Forest',
            size: { width: 60, height: 60 },
            tileData: [],
            connections: [
                { to: 'goldshire', x: 30, y: 59, requirement: null, direction: 'south' },
                { to: 'frozen_peaks', x: 30, y: 0, requirement: 'climbing', direction: 'north' },
                { to: 'underground_depths', x: 35, y: 45, requirement: 'rock_smash', direction: 'down' },
                { to: 'burning_wastes', x: 59, y: 30, requirement: 'tree_cut', hidden: true, direction: 'east' }
            ],
            landmarks: [
                { id: 'twisted_grove', name: 'Twisted Grove', x: 30, y: 30, icon: '🌲', type: 'gym' },
                { id: 'moonwell', name: 'Moonwell Glade', x: 15, y: 20, icon: '✨', type: 'peaceful' }
            ],
            secrets: [
                {
                    id: 'secret_grove',
                    x: 5, y: 5,
                    requirement: 'tree_cut',
                    type: 'hidden_area',
                    reward: { creature: 'ancient_treant', level: 50 }
                }
            ],
            encounters: {
                base: ['wisp', 'wolf', 'spider'],
                scaled: {
                    3: ['ancient_wisp', 'dire_wolf'],
                    6: ['treant', 'nerubian']
                }
            },
            warpShrineLocation: { x: 5, y: 5 }
        });

        // More zones would be added similarly...
    }

    addZone(id, zoneData) {
        this.zones.set(id, zoneData);
    }

    canAccessConnection(connection) {
        // Check if player has required ability
        if (!connection.requirement) return true;
        return this.playerAbilities.has(connection.requirement);
    }

    getAvailableConnections(zoneId) {
        const zone = this.zones.get(zoneId);
        return zone.connections.filter(conn => {
            if (conn.hidden && !this.hasDiscoveredSecret(zoneId, conn)) return false;
            return this.canAccessConnection(conn);
        });
    }

    checkConnectionAtPosition(x, y) {
        const zone = this.zones.get(this.currentZone);
        const connection = zone.connections.find(conn =>
            conn.x === x && conn.y === y
        );

        if (!connection) return null;

        if (!this.canAccessConnection(connection)) {
            return {
                blocked: true,
                requirement: connection.requirement,
                message: this.getBlockedMessage(connection.requirement)
            };
        }

        return { blocked: false, connection };
    }

    getBlockedMessage(requirement) {
        const messages = {
            'tree_cut': 'A thick tree blocks the path. Maybe a Nature creature could cut it?',
            'rock_smash': 'A large boulder is in the way. A strong creature might be able to smash it.',
            'swimming': 'Deep water ahead. You need a Water creature that can swim.',
            'climbing': 'The cliff is too steep to climb without help.',
            'lava_walking': 'The lava is too hot! You need protection from fire.',
            'shadow_walk': 'A shadowy barrier blocks the way. Only shadow creatures can pass.',
            'flight': 'The area is unreachable without flying.',
            'ice_breaking': 'Ice blocks the path. Fire might melt it...'
        };
        return messages[requirement] || 'Something is blocking the way.';
    }

    unlockAbility(abilityName) {
        this.playerAbilities.add(abilityName);
        this.triggerAbilityUnlockEvent(abilityName);
        return this.revealNewPaths(abilityName);
    }

    revealNewPaths(abilityName) {
        const newPaths = [];

        // Check all zones for newly accessible connections
        for (const [zoneId, zone] of this.zones) {
            for (const connection of zone.connections) {
                if (connection.requirement === abilityName) {
                    newPaths.push({
                        zone: zone.name,
                        destination: this.zones.get(connection.to).name,
                        direction: connection.direction
                    });
                }
            }
        }

        return newPaths;
    }

    triggerAbilityUnlockEvent(abilityName) {
        // Show cutscene/animation
        console.log(`🎉 New ability unlocked: ${abilityName}!`);
        console.log(`New areas are now accessible!`);

        // Update map UI to show new connections
        this.updateMapUI();
    }

    updateMapUI() {
        // Refresh minimap display with newly available connections
        // This would integrate with the game's rendering system
    }

    getScaledEncounters(zoneId, playerBadges) {
        const zone = this.zones.get(zoneId);
        let encounters = [...zone.encounters.base];

        // Add scaled encounters based on badge count
        for (const [badgeCount, creatures] of Object.entries(zone.encounters.scaled)) {
            if (playerBadges >= parseInt(badgeCount)) {
                encounters.push(...creatures);
            }
        }

        return encounters;
    }
}

// ===================================================================
// 2. ABILITY SYSTEM WITH WORLD INTERACTIONS
// ===================================================================

class AbilityManager {
    constructor() {
        this.abilities = this.initializeAbilities();
        this.unlockedAbilities = new Set();
    }

    initializeAbilities() {
        return {
            tree_cut: {
                name: 'Tree Cut',
                displayName: 'Vine Whip',
                obtainMethod: 'creature_type',
                requiredType: ['nature'],
                description: 'Cut through trees and vines blocking paths',
                combatPower: 45,
                combatType: 'nature',
                worldInteractions: ['cut_tree', 'swing_vine', 'pull_lever'],
                unlockMessage: 'Your Nature creature can now cut trees!',
                visualEffect: 'leaf_particles'
            },
            rock_smash: {
                name: 'Rock Smash',
                displayName: 'Rock Smash',
                obtainMethod: 'creature_type',
                requiredType: ['beast', 'warrior', 'earth'],
                description: 'Break cracked rocks and boulders',
                combatPower: 40,
                combatType: 'fighting',
                worldInteractions: ['break_rock', 'break_wall', 'trigger_rockslide'],
                unlockMessage: 'Your creature can now smash rocks!',
                visualEffect: 'rock_debris'
            },
            swimming: {
                name: 'Swimming',
                displayName: 'Surf',
                obtainMethod: 'creature_evolution',
                requiredCreature: 'murloc_warrior',
                description: 'Cross water and explore underwater areas',
                combatPower: 90,
                combatType: 'water',
                worldInteractions: ['traverse_water', 'dive_underwater', 'water_current'],
                unlockMessage: 'You can now surf on water!',
                visualEffect: 'water_splash',
                upgrades: ['dive_deep', 'water_speed']
            },
            lava_walking: {
                name: 'Lava Walking',
                displayName: 'Heat Resistance',
                obtainMethod: 'gym_badge',
                requiredBadge: 'fire_badge',
                description: 'Walk safely on lava surfaces',
                combatPower: 0,
                worldInteractions: ['traverse_lava', 'resist_heat'],
                unlockMessage: 'You can now walk on lava!',
                visualEffect: 'fire_shield'
            },
            climbing: {
                name: 'Climbing',
                displayName: 'Scale',
                obtainMethod: 'creature_type',
                requiredType: ['dragon', 'flying', 'beast'],
                description: 'Climb walls and cliffs',
                combatPower: 0,
                worldInteractions: ['climb_wall', 'climb_cliff', 'rope_climb'],
                unlockMessage: 'Your creature can help you climb!',
                visualEffect: 'climbing_creature',
                stamina: 100
            },
            shadow_walk: {
                name: 'Shadow Walk',
                displayName: 'Shadow Phase',
                obtainMethod: 'creature_type',
                requiredType: ['shadow', 'undead', 'spirit'],
                requiredLevel: 30,
                description: 'Phase through shadow barriers',
                combatPower: 80,
                combatType: 'shadow',
                worldInteractions: ['phase_barrier', 'enter_void', 'shadow_realm'],
                unlockMessage: 'You can now walk through shadows!',
                visualEffect: 'ghost_translucent'
            },
            ice_breaking: {
                name: 'Ice Breaking',
                displayName: 'Melt Ice',
                obtainMethod: 'move_usage',
                requiredMove: 'flame_strike',
                description: 'Melt ice obstacles and frozen doors',
                combatPower: 0,
                worldInteractions: ['melt_ice', 'thaw_frozen', 'steam_puzzle'],
                unlockMessage: 'Fire can melt ice barriers!',
                visualEffect: 'steam_particles'
            },
            telekinesis: {
                name: 'Telekinesis',
                displayName: 'Psychic Move',
                obtainMethod: 'creature_type',
                requiredType: ['magic', 'psychic'],
                requiredLevel: 35,
                description: 'Move distant objects and activate remote switches',
                combatPower: 80,
                combatType: 'psychic',
                worldInteractions: ['move_object', 'remote_switch', 'float_platform'],
                unlockMessage: 'Your Psychic creature can move objects with its mind!',
                visualEffect: 'psychic_glow'
            },
            flight: {
                name: 'Flight',
                displayName: 'Fly',
                obtainMethod: 'creature_specific',
                requiredCreature: ['dragon', 'phoenix', 'wyvern'],
                requiredLevel: 40,
                description: 'Fly to any discovered location',
                combatPower: 90,
                combatType: 'flying',
                worldInteractions: ['fast_travel', 'sky_access', 'soar'],
                unlockMessage: 'You can now fly anywhere!',
                visualEffect: 'flying_creature',
                enablesFastTravel: true
            }
        };
    }

    checkAbilityUnlock(player) {
        // Check if player has unlocked any new abilities
        for (const [abilityId, ability] of Object.entries(this.abilities)) {
            if (this.unlockedAbilities.has(abilityId)) continue;

            if (this.canUnlockAbility(ability, player)) {
                this.unlockAbility(abilityId);
                return abilityId;
            }
        }
        return null;
    }

    canUnlockAbility(ability, player) {
        switch (ability.obtainMethod) {
            case 'creature_type':
                return this.hasCreatureOfType(player.party, ability.requiredType);

            case 'creature_evolution':
                return this.hasCreature(player.party, ability.requiredCreature);

            case 'gym_badge':
                return player.badges.includes(ability.requiredBadge);

            case 'move_usage':
                return this.hasMove(player.party, ability.requiredMove);

            case 'creature_specific':
                return this.hasAnyCreature(player.party, ability.requiredCreature) &&
                       this.hasLevelRequirement(player.party, ability.requiredLevel);

            default:
                return false;
        }
    }

    hasCreatureOfType(party, types) {
        return party.some(creature =>
            creature.types.some(t => types.includes(t))
        );
    }

    hasCreature(party, creatureId) {
        return party.some(c => c.id === creatureId);
    }

    hasAnyCreature(party, creatureIds) {
        return party.some(c => creatureIds.includes(c.id));
    }

    hasLevelRequirement(party, minLevel) {
        return party.some(c => c.level >= minLevel);
    }

    hasMove(party, moveName) {
        return party.some(creature =>
            creature.moves.some(move => move.id === moveName)
        );
    }

    unlockAbility(abilityId) {
        this.unlockedAbilities.add(abilityId);
        const ability = this.abilities[abilityId];

        // Show unlock cutscene
        this.showUnlockCutscene(ability);

        // Trigger world state changes
        this.triggerWorldChanges(abilityId);

        return ability;
    }

    showUnlockCutscene(ability) {
        // Display ability unlock animation and message
        console.log(`✨ ${ability.unlockMessage}`);
        // This would integrate with the game's UI system
    }

    triggerWorldChanges(abilityId) {
        // Update game world to reflect new ability
        // e.g., show previously hidden paths, update NPC dialogue
        console.log(`World updated with ${abilityId} ability!`);
    }

    useAbilityOnWorldTile(abilityId, tileX, tileY, map) {
        const ability = this.abilities[abilityId];
        const tile = map.getTile(tileX, tileY);

        // Check if ability can interact with this tile
        if (!tile.interactable) return false;

        switch (tile.interactionType) {
            case 'cut_tree':
                if (ability.worldInteractions.includes('cut_tree')) {
                    this.cutTree(tileX, tileY, map);
                    return true;
                }
                break;

            case 'break_rock':
                if (ability.worldInteractions.includes('break_rock')) {
                    this.breakRock(tileX, tileY, map);
                    return true;
                }
                break;

            case 'melt_ice':
                if (ability.worldInteractions.includes('melt_ice')) {
                    this.meltIce(tileX, tileY, map);
                    return true;
                }
                break;

            // More interaction types...
        }

        return false;
    }

    cutTree(x, y, map) {
        map.removeTile(x, y);
        map.addEffect(x, y, 'leaf_particles');
        map.playSound('tree_cut');
    }

    breakRock(x, y, map) {
        map.removeTile(x, y);
        map.addEffect(x, y, 'rock_debris');
        map.playSound('rock_smash');
        // Check for hidden items under rock
        map.checkHiddenItem(x, y);
    }

    meltIce(x, y, map) {
        map.changeTile(x, y, 'water');
        map.addEffect(x, y, 'steam_particles');
        map.playSound('ice_melt');
    }
}

// ===================================================================
// 3. BACKTRACKING INCENTIVE SYSTEM
// ===================================================================

class BacktrackingManager {
    constructor(mapSystem) {
        this.mapSystem = mapSystem;
        this.revisitTriggers = new Map();
        this.environmentalChanges = [];
        this.npcDialogueUpdates = new Map();
        this.secretsRevealed = new Set();
    }

    checkZoneRevisit(zoneId, playerState) {
        const zone = this.mapSystem.zones.get(zoneId);
        const rewards = {
            newEncounters: [],
            newDialogue: [],
            newSecrets: [],
            shortcuts: []
        };

        // 1. Scaled Encounters
        rewards.newEncounters = this.getNewEncounters(zoneId, playerState.badges);

        // 2. Updated NPC Dialogue
        rewards.newDialogue = this.getUpdatedNPCDialogue(zoneId, playerState);

        // 3. Newly Accessible Secrets
        rewards.newSecrets = this.checkUnlockedSecrets(zoneId, playerState.abilities);

        // 4. Shortcuts Revealed
        rewards.shortcuts = this.checkNewShortcuts(zoneId, playerState.abilities);

        return rewards;
    }

    getNewEncounters(zoneId, badgeCount) {
        const zone = this.mapSystem.zones.get(zoneId);
        const newEncounters = [];

        for (const [requiredBadges, creatures] of Object.entries(zone.encounters.scaled)) {
            if (badgeCount >= parseInt(requiredBadges)) {
                creatures.forEach(creature => {
                    if (!this.hasEncountered(zoneId, creature)) {
                        newEncounters.push(creature);
                        this.markEncountered(zoneId, creature);
                    }
                });
            }
        }

        return newEncounters;
    }

    getUpdatedNPCDialogue(zoneId, playerState) {
        const updates = [];
        const npcs = this.mapSystem.zones.get(zoneId).npcs || [];

        npcs.forEach(npc => {
            const newDialogue = this.getNPCDialogueForState(npc, playerState);
            if (newDialogue !== npc.lastDialogue) {
                updates.push({ npc: npc.id, dialogue: newDialogue });
                npc.lastDialogue = newDialogue;
            }
        });

        return updates;
    }

    getNPCDialogueForState(npc, playerState) {
        // NPCs give different hints based on player progression
        const badgeCount = playerState.badges.length;

        if (badgeCount === 0) {
            return npc.dialogue.start || npc.dialogue.default;
        } else if (badgeCount < 3) {
            return npc.dialogue.early || npc.dialogue.default;
        } else if (badgeCount < 6) {
            return npc.dialogue.mid || npc.dialogue.default;
        } else if (badgeCount < 8) {
            return npc.dialogue.late || npc.dialogue.default;
        } else {
            return npc.dialogue.postgame || npc.dialogue.default;
        }
    }

    checkUnlockedSecrets(zoneId, playerAbilities) {
        const zone = this.mapSystem.zones.get(zoneId);
        const newSecrets = [];

        zone.secrets.forEach(secret => {
            const secretKey = `${zoneId}_${secret.id}`;

            if (!this.secretsRevealed.has(secretKey)) {
                if (!secret.requirement || playerAbilities.has(secret.requirement)) {
                    newSecrets.push(secret);
                    this.secretsRevealed.add(secretKey);
                }
            }
        });

        return newSecrets;
    }

    checkNewShortcuts(zoneId, playerAbilities) {
        // Check if any one-way shortcuts can now be activated
        const shortcuts = [];
        const zone = this.mapSystem.zones.get(zoneId);

        zone.shortcuts?.forEach(shortcut => {
            if (!shortcut.activated && playerAbilities.has(shortcut.requirement)) {
                shortcuts.push(shortcut);
                this.activateShortcut(zoneId, shortcut);
            }
        });

        return shortcuts;
    }

    activateShortcut(zoneId, shortcut) {
        shortcut.activated = true;
        console.log(`🚀 New shortcut discovered: ${shortcut.name}`);
        // Update map to show new connection
    }

    triggerEnvironmentalChange(eventId, affectedZones) {
        // Major world events that change zones
        const event = {
            id: eventId,
            timestamp: Date.now(),
            zones: affectedZones
        };

        this.environmentalChanges.push(event);

        // Apply changes to affected zones
        affectedZones.forEach(zone => {
            this.applyEnvironmentalChange(zone, eventId);
        });
    }

    applyEnvironmentalChange(zoneId, eventId) {
        // Examples:
        // - Volcano erupts: Burning Wastes gets new lava flows
        // - Forest grows: Dark Forest becomes denser, new areas
        // - Ruins flood: Sunken Ruins water level rises

        console.log(`🌍 Environmental change in ${zoneId}: ${eventId}`);
        // Update zone tiles and encounters
    }

    hasEncountered(zoneId, creatureId) {
        const key = `${zoneId}_${creatureId}`;
        return this.revisitTriggers.has(key);
    }

    markEncountered(zoneId, creatureId) {
        const key = `${zoneId}_${creatureId}`;
        this.revisitTriggers.set(key, true);
    }
}

// ===================================================================
// 4. PLATFORMING & TRAVERSAL MECHANICS
// ===================================================================

class PlatformingController {
    constructor() {
        this.isJumping = false;
        this.jumpProgress = 0;
        this.jumpHeight = 1; // tiles

        this.isClimbing = false;
        this.climbingStamina = 100;
        this.maxClimbingStamina = 100;

        this.isSwimming = false;
        this.underwaterAir = 100;
        this.maxUnderwaterAir = 100;

        this.onMovingPlatform = null;
        this.movingPlatformOffset = { x: 0, y: 0 };
    }

    update(deltaTime, player, map) {
        // Update jumping
        if (this.isJumping) {
            this.updateJump(deltaTime, player);
        }

        // Update climbing
        if (this.isClimbing) {
            this.updateClimbing(deltaTime, player);
        }

        // Update swimming/diving
        if (this.isSwimming) {
            this.updateSwimming(deltaTime, player);
        }

        // Update moving platforms
        if (this.onMovingPlatform) {
            this.updateMovingPlatform(deltaTime, player);
        }

        // Check hazards
        this.checkHazards(player, map);
    }

    jump(player, direction) {
        if (this.isJumping || this.isClimbing) return false;

        const targetX = player.x + (direction === 'right' ? 1 : direction === 'left' ? -1 : 0);
        const targetY = player.y + (direction === 'down' ? 1 : direction === 'up' ? -1 : 0);

        // Check if jump is valid
        if (!this.canJumpTo(targetX, targetY, player.map)) {
            return false;
        }

        this.isJumping = true;
        this.jumpProgress = 0;
        this.jumpStart = { x: player.x, y: player.y };
        this.jumpTarget = { x: targetX, y: targetY };
        this.jumpDirection = direction;

        return true;
    }

    canJumpTo(x, y, map) {
        const targetTile = map.getTile(x, y);

        // Can jump to walkable tiles or certain special tiles
        return targetTile.walkable ||
               targetTile.type === 'ledge' ||
               targetTile.type === 'platform';
    }

    updateJump(deltaTime, player) {
        this.jumpProgress += deltaTime * 0.01; // Jump speed

        if (this.jumpProgress >= 1) {
            // Jump complete
            player.x = this.jumpTarget.x;
            player.y = this.jumpTarget.y;
            this.isJumping = false;
            this.jumpProgress = 0;

            // Check for landing effects
            this.handleLanding(player);
        } else {
            // Interpolate position
            player.renderX = this.jumpStart.x + (this.jumpTarget.x - this.jumpStart.x) * this.jumpProgress;
            player.renderY = this.jumpStart.y + (this.jumpTarget.y - this.jumpStart.y) * this.jumpProgress;

            // Add jump arc (parabolic motion)
            player.renderOffsetY = -Math.sin(this.jumpProgress * Math.PI) * this.jumpHeight * 8; // pixels
        }
    }

    startClimbing(player, wall) {
        if (!player.abilities.has('climbing')) {
            return false;
        }

        this.isClimbing = true;
        this.climbingWall = wall;
        player.onClimbable = true;

        return true;
    }

    updateClimbing(deltaTime, player) {
        // Drain stamina while climbing
        this.climbingStamina -= deltaTime * 0.1;

        if (this.climbingStamina <= 0) {
            // Fall if stamina depleted
            this.stopClimbing(player);
            this.handleFall(player);
        }
    }

    stopClimbing(player) {
        this.isClimbing = false;
        this.climbingWall = null;
        player.onClimbable = false;
    }

    startSwimming(player) {
        if (!player.abilities.has('swimming')) {
            return false;
        }

        this.isSwimming = true;
        player.inWater = true;
        return true;
    }

    dive(player) {
        if (!this.isSwimming || !player.abilities.has('dive_deep')) {
            return false;
        }

        player.isUnderwater = true;
        return true;
    }

    updateSwimming(deltaTime, player) {
        if (player.isUnderwater) {
            // Drain air while underwater
            this.underwaterAir -= deltaTime * 0.5;

            if (this.underwaterAir <= 0) {
                // Take damage from drowning
                player.takeDamage(5);
                this.surfaceFromDive(player);
            }
        }
    }

    surfaceFromDive(player) {
        player.isUnderwater = false;
        this.underwaterAir = this.maxUnderwaterAir;
    }

    checkHazards(player, map) {
        const currentTile = map.getTile(player.x, player.y);

        switch (currentTile.hazardType) {
            case 'lava':
                if (!player.abilities.has('lava_walking')) {
                    player.takeDamage(15);
                    this.playHazardEffect('lava_burn');
                }
                break;

            case 'ice':
                // Sliding on ice
                if (!player.keys.moving) {
                    this.slideOnIce(player, map);
                }
                break;

            case 'crumbling':
                // Platform crumbles after 2 seconds
                this.startCrumbleTimer(player, currentTile);
                break;

            case 'poison':
                if (!this.hasProtection(player, 'poison')) {
                    player.takeDamage(5);
                    this.playHazardEffect('poison');
                }
                break;
        }
    }

    slideOnIce(player, map) {
        // Continue moving in last direction until hitting obstacle
        const direction = player.lastMoveDirection;
        const nextX = player.x + (direction === 'right' ? 1 : direction === 'left' ? -1 : 0);
        const nextY = player.y + (direction === 'down' ? 1 : direction === 'up' ? -1 : 0);

        const nextTile = map.getTile(nextX, nextY);

        if (nextTile.walkable) {
            // Continue sliding
            player.x = nextX;
            player.y = nextY;
            setTimeout(() => this.slideOnIce(player, map), 200);
        }
        // Stop sliding when hit obstacle
    }

    handleLanding(player) {
        const tile = player.map.getTile(player.x, player.y);

        if (tile.type === 'crumbling') {
            // Start crumble timer
            this.startCrumbleTimer(player, tile);
        }
    }

    startCrumbleTimer(player, tile) {
        if (tile.crumbleTimer) return; // Already crumbling

        tile.crumbleTimer = setTimeout(() => {
            tile.crumbled = true;
            player.handleFall();
        }, 2000);
    }

    handleFall(player) {
        // Player falls to tile below or takes damage
        player.y += 1;
        player.takeDamage(10);
    }

    updateMovingPlatform(deltaTime, player) {
        // Move player with platform
        const platform = this.onMovingPlatform;
        const movement = platform.getMovement(deltaTime);

        player.x += movement.x;
        player.y += movement.y;
    }

    playHazardEffect(effectType) {
        // Visual and audio feedback for hazards
        console.log(`⚠️ Hazard: ${effectType}`);
    }

    hasProtection(player, hazardType) {
        // Check if player has creature with immunity
        return player.party.some(creature =>
            creature.types.includes(hazardType + '_immunity')
        );
    }
}

// ===================================================================
// 5. SECRET DISCOVERY SYSTEM
// ===================================================================

class SecretManager {
    constructor() {
        this.discoveredSecrets = new Set();
        this.secretHints = new Map();
        this.secretRewards = new Map();
    }

    checkSecretAtPosition(x, y, zoneId, playerAbilities) {
        const secretKey = `${zoneId}_${x}_${y}`;

        // Check if already discovered
        if (this.discoveredSecrets.has(secretKey)) {
            return null;
        }

        // Check for secret at this location
        const secret = this.getSecretAtPosition(x, y, zoneId);
        if (!secret) return null;

        // Check if player has required ability
        if (secret.requirement && !playerAbilities.has(secret.requirement)) {
            // Show hint about what's needed
            return {
                found: false,
                hint: `You sense something here... ${this.getRequirementHint(secret.requirement)}`
            };
        }

        // Secret discovered!
        return this.discoverSecret(secret, secretKey);
    }

    getSecretAtPosition(x, y, zoneId) {
        // Check zone data for secrets at this position
        // This would integrate with the map system
        return null; // Placeholder
    }

    discoverSecret(secret, secretKey) {
        this.discoveredSecrets.add(secretKey);

        const result = {
            found: true,
            type: secret.type,
            reward: secret.reward,
            message: this.getDiscoveryMessage(secret)
        };

        // Grant reward
        this.grantReward(secret.reward);

        // Trigger discovery effects
        this.playDiscoveryEffect(secret);

        return result;
    }

    getRequirementHint(requirement) {
        const hints = {
            'rock_smash': 'Maybe a strong creature could break through?',
            'tree_cut': 'A Nature creature might be able to clear the way.',
            'swimming': 'The path continues underwater...',
            'shadow_walk': 'Only shadows can pass through here.',
            'flight': 'If only you could fly...',
            'illuminate': 'It\'s too dark to see...'
        };
        return hints[requirement] || 'You need something special...';
    }

    getDiscoveryMessage(secret) {
        switch (secret.type) {
            case 'hidden_item':
                return `Found hidden item: ${secret.reward.item}!`;
            case 'secret_passage':
                return 'A secret passage has opened!';
            case 'legendary_encounter':
                return `A legendary ${secret.reward.creature} appeared!`;
            case 'warp_shrine':
                return 'Ancient shrine activated! Fast travel unlocked.';
            default:
                return 'You discovered a secret!';
        }
    }

    grantReward(reward) {
        // Grant rewards to player
        // This would integrate with player inventory system
        console.log('Reward granted:', reward);
    }

    playDiscoveryEffect(secret) {
        // Visual and audio effects for secret discovery
        console.log('✨ Secret discovered!');
    }

    checkForHiddenWalls(playerX, playerY, playerDirection, zoneId) {
        // Check if player is facing a hidden wall
        const facingX = playerX + (playerDirection === 'right' ? 1 : playerDirection === 'left' ? -1 : 0);
        const facingY = playerY + (playerDirection === 'down' ? 1 : playerDirection === 'up' ? -1 : 0);

        const secret = this.checkSecretAtPosition(facingX, facingY, zoneId, ['walk_through']);

        if (secret && secret.type === 'hidden_wall') {
            return true; // Player can walk through
        }

        return false;
    }
}

// ===================================================================
// 6. INTEGRATION WITH EXISTING GAME ENGINE
// ===================================================================

/*
To integrate these systems into wowMon.html:

1. Replace the existing map system with MetroidvaniaMapSystem
2. Add AbilityManager to track and unlock abilities
3. Integrate BacktrackingManager to handle zone revisits
4. Add PlatformingController for movement mechanics
5. Integrate SecretManager for discovery mechanics

Example integration in GameEngine class:

class GameEngine {
    constructor() {
        // ... existing code ...

        // Add new systems
        this.metroidvaniaMap = new MetroidvaniaMapSystem();
        this.abilityManager = new AbilityManager();
        this.backtrackingManager = new BacktrackingManager(this.metroidvaniaMap);
        this.platformingController = new PlatformingController();
        this.secretManager = new SecretManager();
    }

    update(deltaTime) {
        // ... existing update code ...

        // Update platforming
        this.platformingController.update(deltaTime, this.player, this.currentMap);

        // Check for ability unlocks
        const newAbility = this.abilityManager.checkAbilityUnlock(this.player);
        if (newAbility) {
            const newPaths = this.metroidvaniaMap.unlockAbility(newAbility);
            this.showNewPathsNotification(newPaths);
        }
    }

    handleMovement(direction) {
        // Check for connection at new position
        const connection = this.metroidvaniaMap.checkConnectionAtPosition(
            this.player.x,
            this.player.y
        );

        if (connection) {
            if (connection.blocked) {
                this.showMessage(connection.message);
                return;
            }

            // Transition to new zone
            this.transitionToZone(connection.connection.to);
        }

        // ... existing movement code ...
    }
}
*/

// ===================================================================
// EXPORT FOR USE IN WOWMON.HTML
// ===================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MetroidvaniaMapSystem,
        AbilityManager,
        BacktrackingManager,
        PlatformingController,
        SecretManager
    };
}
