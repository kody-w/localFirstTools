# WoWMon: Action RPG / Souls-Like Redesign
## Complete Real-Time Combat System Overhaul

---

## Executive Summary

Transform WoWMon from a turn-based Pokemon clone into a skill-based action RPG with Souls-like combat mechanics. This redesign focuses on real-time combat, stamina management, challenging boss encounters, and rewarding player skill over grinding.

**Core Philosophy:** Challenging but fair, skill-based over stat-based, memorable encounters over random battles.

---

## 1. Real-Time Combat System

### Current System (Turn-Based)
```javascript
// OLD: Menu-driven turn selection
executeTurn(playerMoveId) {
    this.battle.waitingForInput = false;
    const playerFirst = this.battle.playerCreature.speed >= this.battle.enemyCreature.speed;
    // Wait for animations, then enemy attacks
}
```

### New System (Real-Time Action)
```javascript
// NEW: Real-time combat state machine
class ActionCombatSystem {
    constructor(game) {
        this.game = game;
        this.state = 'neutral'; // neutral, attacking, dodging, blocking, stunned
        this.stamina = 100;
        this.maxStamina = 100;
        this.staminaRegen = 25; // per second
        this.lockOn = null;
        this.combo = 0;
        this.iframes = 0; // Invincibility frames after dodge
    }

    // Core combat actions with stamina costs
    lightAttack() {
        if (this.state !== 'neutral' || this.stamina < 15) return false;

        this.state = 'attacking';
        this.stamina -= 15;
        this.combo++;

        const damage = this.calculateDamage('light', this.combo);
        const hitbox = this.createAttackHitbox('light', this.combo);

        // Attack animation: 400ms with active frames 100-250ms
        this.attackFrames = {
            startup: 100,  // Cannot cancel
            active: 150,   // Hitbox active
            recovery: 150  // Can roll-cancel after 100ms
        };

        // Combo window: 500ms to chain next attack
        this.comboWindow = 500;

        setTimeout(() => {
            if (this.state === 'attacking') {
                this.state = 'neutral';
                if (Date.now() - this.lastAttackTime > this.comboWindow) {
                    this.combo = 0;
                }
            }
        }, 400);

        this.lastAttackTime = Date.now();
        return true;
    }

    heavyAttack() {
        if (this.state !== 'neutral' || this.stamina < 30) return false;

        this.state = 'attacking';
        this.stamina -= 30;

        const damage = this.calculateDamage('heavy', 1);
        const hitbox = this.createAttackHitbox('heavy', 1);

        // Heavy attack: slower but more damage, can break guards
        this.attackFrames = {
            startup: 250,   // Long wind-up, vulnerable
            active: 200,    // Hitbox active
            recovery: 300   // Long recovery
        };

        setTimeout(() => {
            if (this.state === 'attacking') {
                this.state = 'neutral';
                this.combo = 0;
            }
        }, 750);

        return true;
    }

    dodge() {
        // THE SOULS DODGE: Timing is everything
        if (this.state !== 'neutral' && this.state !== 'attacking') return false;
        if (this.stamina < 25) return false;

        this.state = 'dodging';
        this.stamina -= 25;

        // I-frames: 12 frames at 60fps = 200ms of invincibility
        this.iframes = 200;

        // Dodge roll duration: 600ms
        const dodgeDirection = this.getInputDirection() || this.facing;
        this.dodgeVelocity = {
            x: dodgeDirection.x * 3,
            y: dodgeDirection.y * 3
        };

        setTimeout(() => {
            this.state = 'neutral';
        }, 600);

        return true;
    }

    block() {
        // Hold to block, drains stamina while active
        if (this.stamina <= 0) {
            this.state = 'stunned';
            this.staminaBroken = true;
            return false;
        }

        this.state = 'blocking';
        this.blockStaminaDrain = 5; // per second while holding

        return true;
    }

    releaseBlock() {
        if (this.state === 'blocking') {
            this.state = 'neutral';
        }
    }

    parry() {
        // Advanced technique: Block at exact moment of enemy attack
        if (this.state !== 'blocking') return false;

        const parryWindow = 150; // 150ms window
        const timeSinceBlockStart = Date.now() - this.blockStartTime;

        if (timeSinceBlockStart <= parryWindow) {
            // PERFECT PARRY!
            this.state = 'parry_success';
            this.stamina = Math.min(this.maxStamina, this.stamina + 30);

            // Enemy is riposte-vulnerable for 2 seconds
            if (this.lockOn) {
                this.lockOn.riposteVulnerable = true;
                this.lockOn.riposteWindow = 2000;
            }

            // Play parry sound and visual effect
            this.game.audio.playSFX('parry');
            this.createParryEffect();

            setTimeout(() => {
                this.state = 'neutral';
            }, 300);

            return true;
        }

        return false;
    }

    riposte() {
        // Critical attack after successful parry
        if (!this.lockOn || !this.lockOn.riposteVulnerable) return false;
        if (this.state !== 'neutral') return false;

        this.state = 'riposting';

        // Riposte deals massive damage (3x normal)
        const damage = this.calculateDamage('riposte', 1);
        this.dealDamage(this.lockOn, damage * 3);

        // Lock both entities in critical animation
        this.lockOn.state = 'riposted';

        this.game.audio.playSFX('critical_hit');
        this.createCriticalEffect();

        setTimeout(() => {
            this.state = 'neutral';
            if (this.lockOn) this.lockOn.state = 'neutral';
        }, 1500);

        return true;
    }

    // Stamina management
    updateStamina(deltaTime) {
        if (this.state === 'blocking') {
            this.stamina -= this.blockStaminaDrain * deltaTime;
            if (this.stamina <= 0) {
                this.stamina = 0;
                this.state = 'stunned';
                this.staminaBroken = true;
                setTimeout(() => {
                    this.state = 'neutral';
                    this.staminaBroken = false;
                }, 2000);
            }
        } else if (this.state === 'neutral' && this.stamina < this.maxStamina) {
            // Stamina regenerates when not attacking/dodging/blocking
            this.stamina = Math.min(this.maxStamina, this.stamina + this.staminaRegen * deltaTime);
        }

        // Update I-frames
        if (this.iframes > 0) {
            this.iframes -= deltaTime * 1000;
        }
    }

    // Hit detection with precise hitboxes
    createAttackHitbox(type, comboStep) {
        const player = this.game.player;
        const range = type === 'light' ? 20 : 30;
        const arc = type === 'light' ? 90 : 120;

        // Different hitboxes for combo steps
        const hitbox = {
            x: player.x,
            y: player.y,
            range: range,
            arc: arc,
            direction: player.facing,
            comboStep: comboStep,
            type: type
        };

        // Check all enemies in range
        this.game.enemies.forEach(enemy => {
            if (this.checkHitboxCollision(hitbox, enemy)) {
                if (enemy.iframes <= 0) {
                    this.onHit(enemy, hitbox);
                }
            }
        });

        return hitbox;
    }

    checkHitboxCollision(hitbox, enemy) {
        const dx = enemy.x - hitbox.x;
        const dy = enemy.y - hitbox.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > hitbox.range) return false;

        // Check if enemy is within arc
        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
        const facingAngle = this.directionToAngle(hitbox.direction);
        const angleDiff = Math.abs(angle - facingAngle);

        return angleDiff <= hitbox.arc / 2;
    }

    onHit(enemy, hitbox) {
        const damage = this.calculateDamage(hitbox.type, hitbox.comboStep);

        // Apply damage
        enemy.hp -= damage;

        // Apply hitstun based on attack type
        if (hitbox.type === 'heavy') {
            enemy.state = 'stunned';
            enemy.stunDuration = 800;
        } else {
            enemy.state = 'hitstun';
            enemy.stunDuration = 200;
        }

        // Knockback
        const knockback = hitbox.type === 'heavy' ? 40 : 15;
        enemy.velocity = {
            x: Math.cos(this.directionToAngle(hitbox.direction) * Math.PI / 180) * knockback,
            y: Math.sin(this.directionToAngle(hitbox.direction) * Math.PI / 180) * knockback
        };

        // Visual feedback
        this.createHitEffect(enemy.x, enemy.y);
        this.game.audio.playSFX('hit');

        // Combo counter increases
        if (this.combo > 1) {
            this.showComboText(this.combo);
        }
    }

    calculateDamage(type, comboStep) {
        const baseDamage = {
            'light': 10,
            'heavy': 35,
            'riposte': 50
        };

        let damage = baseDamage[type] || 10;

        // Combo multiplier: 1.0x -> 1.2x -> 1.4x -> 1.6x
        if (comboStep > 1) {
            damage *= (1 + (comboStep - 1) * 0.2);
        }

        // Add weapon scaling
        damage *= this.game.player.weapon.damageModifier;

        // Add stat scaling
        damage *= (1 + this.game.player.strength / 50);

        return Math.floor(damage);
    }

    // Lock-on system (Z-targeting)
    toggleLockOn() {
        if (!this.lockOn) {
            // Find nearest enemy
            const nearestEnemy = this.findNearestEnemy();
            if (nearestEnemy && this.distanceToEnemy(nearestEnemy) < 150) {
                this.lockOn = nearestEnemy;
                this.lockOn.isLockedOn = true;
            }
        } else {
            this.lockOn.isLockedOn = false;
            this.lockOn = null;
        }
    }

    cycleLockOn(direction) {
        if (!this.lockOn) {
            this.toggleLockOn();
            return;
        }

        // Cycle through nearby enemies
        const enemies = this.getEnemiesInRange(150);
        const currentIndex = enemies.indexOf(this.lockOn);
        const nextIndex = direction > 0
            ? (currentIndex + 1) % enemies.length
            : (currentIndex - 1 + enemies.length) % enemies.length;

        this.lockOn.isLockedOn = false;
        this.lockOn = enemies[nextIndex];
        this.lockOn.isLockedOn = true;
    }

    update(deltaTime) {
        this.updateStamina(deltaTime);

        // Update dodge movement
        if (this.state === 'dodging' && this.dodgeVelocity) {
            this.game.player.x += this.dodgeVelocity.x;
            this.game.player.y += this.dodgeVelocity.y;
            // Decay velocity
            this.dodgeVelocity.x *= 0.9;
            this.dodgeVelocity.y *= 0.9;
        }

        // Auto-face locked enemy
        if (this.lockOn && this.state === 'neutral') {
            const dx = this.lockOn.x - this.game.player.x;
            const dy = this.lockOn.y - this.game.player.y;
            this.game.player.facing = this.vectorToDirection(dx, dy);
        }
    }

    // Input mapping
    handleInput(input, pressed) {
        switch(input) {
            case 'light_attack': // X button
                if (pressed) this.lightAttack();
                break;
            case 'heavy_attack': // Y button
                if (pressed) this.heavyAttack();
                break;
            case 'dodge': // B button
                if (pressed) this.dodge();
                break;
            case 'block': // LT/L2
                if (pressed) {
                    this.blockStartTime = Date.now();
                    this.block();
                } else {
                    this.releaseBlock();
                }
                break;
            case 'lock_on': // RT/R2
                if (pressed) this.toggleLockOn();
                break;
            case 'riposte': // A button when available
                if (pressed) this.riposte();
                break;
        }
    }
}
```

### Key Features
- **Frame-perfect timing**: Attack startups, active frames, recovery
- **I-frames on dodge**: 200ms invincibility window
- **Stamina management**: Every action costs stamina
- **Combo system**: Chain light attacks with proper timing
- **Parry/Riposte**: High-risk, high-reward defensive technique
- **Lock-on targeting**: Z-targeting like Souls games
- **Hitbox precision**: Arc-based melee detection

---

## 2. Stamina System

### Visual UI Design
```javascript
class StaminaUI {
    render(ctx, combat) {
        const x = 20;
        const y = 100;
        const width = 120;
        const height = 8;

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(x - 2, y - 2, width + 4, height + 4);

        // Stamina bar
        const staminaPercent = combat.stamina / combat.maxStamina;

        // Color based on stamina level
        if (staminaPercent > 0.5) {
            ctx.fillStyle = '#4ade80'; // Green
        } else if (staminaPercent > 0.25) {
            ctx.fillStyle = '#fbbf24'; // Yellow
        } else {
            ctx.fillStyle = '#ef4444'; // Red - danger!
        }

        // Flash red when stamina broken
        if (combat.staminaBroken) {
            ctx.fillStyle = '#ef4444';
            ctx.globalAlpha = 0.3 + Math.sin(Date.now() / 100) * 0.3;
        }

        ctx.fillRect(x, y, width * staminaPercent, height);
        ctx.globalAlpha = 1;

        // Stamina segments (each 25 stamina)
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.lineWidth = 1;
        for (let i = 1; i < 4; i++) {
            const segX = x + (width / 4) * i;
            ctx.beginPath();
            ctx.moveTo(segX, y);
            ctx.lineTo(segX, y + height);
            ctx.stroke();
        }

        // Stamina cost preview
        if (combat.hoveredAction) {
            const cost = this.getActionCost(combat.hoveredAction);
            const costWidth = (cost / combat.maxStamina) * width;
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.fillRect(x + width * staminaPercent - costWidth, y, costWidth, height);
        }
    }

    getActionCost(action) {
        const costs = {
            'light_attack': 15,
            'heavy_attack': 30,
            'dodge': 25,
            'block_per_sec': 5
        };
        return costs[action] || 0;
    }
}
```

### Stamina Management Strategy
```javascript
// Player must manage stamina carefully
class StaminaStrategy {
    // Bad play: Button mashing depletes stamina
    buttonMasher() {
        // Attack, attack, attack, attack... STAMINA BROKEN!
        this.lightAttack(); // 15 stamina
        this.lightAttack(); // 15 stamina
        this.lightAttack(); // 15 stamina
        this.lightAttack(); // 15 stamina
        this.lightAttack(); // 15 stamina
        this.dodge(); // 25 stamina - CAN'T! Stamina at 0
        // NOW VULNERABLE! Enemy attacks during stamina break
    }

    // Good play: Measured aggression
    skilledPlayer() {
        // 2-hit combo, back off to regen
        this.lightAttack(); // 85 stamina left
        this.lightAttack(); // 70 stamina left
        this.dodge(); // 45 stamina left - still safe!
        // Back away, stamina regenerates to 70 in 1 second
        // Re-engage with full options
    }

    // Advanced play: Resource manipulation
    expertPlayer() {
        // Bait attack, perfect parry
        this.block(); // -5 stamina per second
        this.parry(); // +30 stamina on success!
        this.riposte(); // Massive damage, no stamina cost
        // Net stamina gain from perfect parry!
    }
}
```

### Equipment Scaling
```javascript
class Equipment {
    constructor() {
        this.weapons = {
            'starter_sword': {
                name: 'Rusty Sword',
                lightCost: 15,
                heavyCost: 30,
                dodgeCost: 25,
                damageModifier: 1.0,
                description: 'A balanced weapon for beginners'
            },
            'heavy_hammer': {
                name: 'Orcish Warhammer',
                lightCost: 20, // More stamina per swing
                heavyCost: 40,
                dodgeCost: 35, // Heavier = slower dodge
                damageModifier: 1.5, // But much more damage!
                description: 'Slow but devastating. High risk, high reward.'
            },
            'light_dagger': {
                name: 'Rogue\'s Knife',
                lightCost: 10, // Very fast attacks
                heavyCost: 20,
                dodgeCost: 15, // Quick dodges
                damageModifier: 0.7, // Lower damage
                staminaRegen: 1.5, // 50% faster stamina regen!
                description: 'Fast and agile. Perfect for combo builds.'
            },
            'enchanted_staff': {
                name: 'Archmage Staff',
                lightCost: 18,
                heavyCost: 35,
                dodgeCost: 25,
                damageModifier: 1.2,
                maxStamina: 150, // +50% stamina pool!
                description: 'Increased stamina pool for mages'
            }
        };

        this.armor = {
            'light_armor': {
                name: 'Leather Armor',
                staminaRegen: 1.3,
                dodgeCost: 0.8, // 20% cheaper dodges
                defense: 1.0
            },
            'medium_armor': {
                name: 'Chain Mail',
                staminaRegen: 1.0,
                dodgeCost: 1.0,
                defense: 1.3
            },
            'heavy_armor': {
                name: 'Plate Armor',
                staminaRegen: 0.7, // Slower stamina regen
                dodgeCost: 1.4, // Expensive dodges
                defense: 1.6, // But great defense
                blockEfficiency: 1.5 // Blocks cost less stamina
            }
        };
    }
}
```

---

## 3. Boss Design

### Boss Framework
```javascript
class BossEnemy {
    constructor(id, data) {
        this.id = id;
        this.name = data.name;
        this.hp = data.hp;
        this.maxHp = data.hp;
        this.phases = data.phases || 1;
        this.currentPhase = 1;

        // Boss-specific stats
        this.poise = data.poise || 100; // Resistance to stagger
        this.aggressiveness = data.aggressiveness || 1.0;

        // AI state machine
        this.aiState = 'idle';
        this.attackPattern = data.attackPatterns;
        this.movePool = data.moves;
        this.nextAttack = null;
        this.telegraph = null;

        // Boss unique mechanics
        this.uniqueMechanic = data.uniqueMechanic;

        this.position = { x: 0, y: 0 };
        this.facing = 0;
    }

    update(deltaTime) {
        // Check for phase transition
        const hpPercent = this.hp / this.maxHp;
        if (hpPercent <= 0.5 && this.currentPhase === 1 && this.phases >= 2) {
            this.enterPhase2();
        } else if (hpPercent <= 0.25 && this.currentPhase === 2 && this.phases >= 3) {
            this.enterPhase3();
        }

        // Update AI
        this.updateAI(deltaTime);

        // Update unique mechanic
        if (this.uniqueMechanic) {
            this.uniqueMechanic.update(deltaTime);
        }
    }

    updateAI(deltaTime) {
        const player = this.game.player;
        const distance = this.distanceTo(player);

        switch(this.aiState) {
            case 'idle':
                // Boss observes player, then attacks
                this.idleTimer = (this.idleTimer || 0) + deltaTime;
                if (this.idleTimer > 1.0) {
                    this.chooseNextAttack(player, distance);
                    this.aiState = 'telegraph';
                    this.idleTimer = 0;
                }
                break;

            case 'telegraph':
                // Show attack telegraph
                this.telegraphTimer = (this.telegraphTimer || 0) + deltaTime;

                // Visual telegraph based on attack type
                this.showTelegraph(this.nextAttack);

                if (this.telegraphTimer >= this.nextAttack.telegraphDuration) {
                    this.aiState = 'attacking';
                    this.telegraphTimer = 0;
                }
                break;

            case 'attacking':
                // Execute attack
                this.executeAttack(this.nextAttack);
                this.aiState = 'recovery';
                break;

            case 'recovery':
                // Recovery period after attack
                this.recoveryTimer = (this.recoveryTimer || 0) + deltaTime;
                if (this.recoveryTimer >= this.nextAttack.recovery) {
                    this.aiState = 'idle';
                    this.recoveryTimer = 0;
                }
                break;

            case 'stunned':
                // Poise broken, temporarily vulnerable
                this.stunTimer = (this.stunTimer || 0) + deltaTime;
                if (this.stunTimer >= 3.0) {
                    this.aiState = 'idle';
                    this.stunTimer = 0;
                    this.poise = this.maxPoise; // Reset poise
                }
                break;
        }
    }

    chooseNextAttack(player, distance) {
        // Select attack based on distance and current phase
        const phase = this.currentPhase;
        const availableAttacks = this.movePool.filter(move =>
            move.phase <= phase &&
            distance >= move.minRange &&
            distance <= move.maxRange
        );

        // Weight attacks by player behavior
        const weights = availableAttacks.map(move => {
            let weight = move.baseWeight;

            // Punish player patterns
            if (player.isBlocking && move.guardBreak) weight *= 3;
            if (player.recentDodges > 2 && move.rollCatch) weight *= 2;
            if (distance < 30 && move.type === 'aoe') weight *= 2;

            return weight;
        });

        // Weighted random selection
        this.nextAttack = this.weightedRandom(availableAttacks, weights);
    }

    showTelegraph(attack) {
        // Visual telegraph for player to react
        if (attack.type === 'melee') {
            // Show weapon glowing
            this.weaponGlow = {
                intensity: Math.sin(Date.now() / 100) * 0.5 + 0.5,
                color: attack.element || '#ff0000'
            };
        } else if (attack.type === 'charge') {
            // Show charge direction
            this.chargeLine = {
                from: this.position,
                to: this.game.player.position,
                color: '#ff0000'
            };
        } else if (attack.type === 'aoe') {
            // Show AoE circle
            this.aoeCircle = {
                x: this.position.x,
                y: this.position.y,
                radius: attack.range,
                color: 'rgba(255, 0, 0, 0.3)'
            };
        }
    }

    executeAttack(attack) {
        switch(attack.type) {
            case 'melee':
                this.meleeAttack(attack);
                break;
            case 'charge':
                this.chargeAttack(attack);
                break;
            case 'aoe':
                this.aoeAttack(attack);
                break;
            case 'combo':
                this.comboAttack(attack);
                break;
        }

        this.game.audio.playSFX(attack.sound || 'boss_attack');
    }

    takeDamage(amount, poiseBreak = 10) {
        this.hp -= amount;
        this.poise -= poiseBreak;

        if (this.poise <= 0 && this.aiState !== 'stunned') {
            // Poise broken! Boss is stunned
            this.aiState = 'stunned';
            this.stunTimer = 0;
            this.game.showText(`${this.name}'s poise broken!`);
            this.game.audio.playSFX('poise_break');
        }

        if (this.hp <= 0) {
            this.onDeath();
        }
    }

    enterPhase2() {
        this.currentPhase = 2;
        this.poise = this.maxPoise; // Reset poise
        this.aggressiveness *= 1.3; // More aggressive

        // Play phase transition cutscene
        this.game.showText(`${this.name} enters phase 2!`);
        this.game.audio.playSFX('phase_transition');

        // Heal 25% HP
        this.hp = Math.min(this.maxHp, this.hp + this.maxHp * 0.25);

        // Unlock new moves
        this.movePool = this.movePool.concat(this.attackPattern.phase2Moves);
    }

    enterPhase3() {
        this.currentPhase = 3;
        this.poise = this.maxPoise * 1.5; // More poise in final phase
        this.aggressiveness *= 1.5;

        this.game.showText(`${this.name} unleashes true power!`);
        this.game.audio.playSFX('phase_transition_final');

        // Activate unique mechanic
        if (this.uniqueMechanic) {
            this.uniqueMechanic.activate();
        }

        this.movePool = this.movePool.concat(this.attackPattern.phase3Moves);
    }
}
```

### Example Boss: Hogger (Early Game)
```javascript
const BOSS_HOGGER = {
    name: 'Hogger the Ravager',
    title: 'Gnoll Chieftain',
    hp: 500,
    poise: 80,
    phases: 2,
    aggressiveness: 0.8,

    attackPatterns: {
        phase1Moves: [
            {
                id: 'claw_swipe',
                name: 'Claw Swipe',
                type: 'melee',
                damage: 25,
                minRange: 0,
                maxRange: 30,
                telegraphDuration: 0.4,
                recovery: 0.8,
                baseWeight: 10,
                description: 'Basic melee swipe'
            },
            {
                id: 'leap',
                name: 'Gnoll Leap',
                type: 'charge',
                damage: 35,
                minRange: 40,
                maxRange: 100,
                telegraphDuration: 0.6,
                recovery: 1.2,
                baseWeight: 7,
                rollCatch: true, // Catches panic rolls
                description: 'Leaps at distant targets'
            },
            {
                id: 'howl',
                name: 'Savage Howl',
                type: 'buff',
                minRange: 0,
                maxRange: 999,
                telegraphDuration: 1.0,
                recovery: 0.5,
                baseWeight: 3,
                effect: { aggressiveness: 1.5, duration: 10 },
                description: 'Enrages, increasing attack speed'
            }
        ],

        phase2Moves: [
            {
                id: 'ground_slam',
                name: 'Ground Slam',
                type: 'aoe',
                damage: 40,
                range: 60,
                minRange: 0,
                maxRange: 999,
                telegraphDuration: 0.8,
                recovery: 1.5,
                baseWeight: 8,
                description: 'AoE attack that must be dodged'
            },
            {
                id: 'triple_swipe',
                name: 'Triple Swipe',
                type: 'combo',
                damage: [20, 20, 35],
                minRange: 0,
                maxRange: 30,
                telegraphDuration: 0.3,
                recovery: 2.0,
                baseWeight: 6,
                guardBreak: true, // Third hit breaks guard
                description: '3-hit combo, final hit breaks guard'
            }
        ]
    },

    uniqueMechanic: {
        type: 'summon_adds',
        description: 'At 50% HP, summons 2 gnoll minions',
        trigger: 0.5,
        execute: function() {
            this.game.spawnEnemy('gnoll_minion', this.position.x - 50, this.position.y);
            this.game.spawnEnemy('gnoll_minion', this.position.x + 50, this.position.y);
        }
    }
};
```

### Example Boss: Onyxia (Late Game)
```javascript
const BOSS_ONYXIA = {
    name: 'Onyxia',
    title: 'Broodmother of the Black Dragonflight',
    hp: 2000,
    poise: 150,
    phases: 3,
    aggressiveness: 1.2,

    attackPatterns: {
        // Phase 1: Ground combat
        phase1Moves: [
            {
                id: 'tail_swipe',
                name: 'Tail Swipe',
                type: 'melee',
                damage: 45,
                arc: 180,
                minRange: 0,
                maxRange: 40,
                telegraphDuration: 0.5,
                recovery: 1.0,
                baseWeight: 8,
                knockback: 50,
                description: 'Wide tail sweep behind her'
            },
            {
                id: 'flame_breath',
                name: 'Flame Breath',
                type: 'cone',
                damage: 60,
                range: 80,
                arc: 60,
                minRange: 0,
                maxRange: 80,
                telegraphDuration: 1.0,
                recovery: 2.0,
                baseWeight: 6,
                dot: { damage: 5, duration: 5 },
                description: 'Cone of fire in front'
            },
            {
                id: 'wing_buffet',
                name: 'Wing Buffet',
                type: 'aoe',
                damage: 30,
                range: 50,
                minRange: 0,
                maxRange: 999,
                telegraphDuration: 0.6,
                recovery: 1.5,
                baseWeight: 7,
                knockback: 70,
                description: 'Knocks back all nearby targets'
            }
        ],

        // Phase 2: Takes flight!
        phase2Moves: [
            {
                id: 'deep_breath',
                name: 'Deep Breath',
                type: 'line',
                damage: 100,
                width: 40,
                length: 200,
                telegraphDuration: 2.0,
                recovery: 0,
                baseWeight: 10,
                description: 'Fly across arena in straight line, devastating damage'
            },
            {
                id: 'fireball_barrage',
                name: 'Fireball Barrage',
                type: 'projectile',
                damage: 35,
                count: 6,
                spread: 30,
                telegraphDuration: 0.8,
                recovery: 1.5,
                baseWeight: 8,
                description: 'Rains fireballs from above'
            }
        ],

        // Phase 3: Lands enraged
        phase3Moves: [
            {
                id: 'cataclysm',
                name: 'Cataclysm',
                type: 'ultimate',
                damage: 80,
                stages: 3,
                telegraphDuration: 3.0,
                recovery: 3.0,
                baseWeight: 5,
                description: 'Arena-wide destruction in waves'
            }
        ]
    },

    uniqueMechanic: {
        type: 'phase_2_flight',
        description: 'Takes flight at 65% HP, player must dodge aerial attacks',
        trigger: 0.65,
        execute: function() {
            this.isFlying = true;
            this.invulnerable = true;
            this.position.z = 100; // Fly up

            // Spawn whelps on ground
            for (let i = 0; i < 4; i++) {
                this.game.spawnEnemy('dragon_whelp');
            }

            // After 60 seconds or all whelps dead, land
            this.flightTimer = 60;
            this.watchForWhelpsDead = true;
        },
        update: function(deltaTime) {
            if (!this.isFlying) return;

            this.flightTimer -= deltaTime;

            const whelpsAlive = this.game.enemies.filter(e => e.id === 'dragon_whelp').length;

            if (this.flightTimer <= 0 || whelpsAlive === 0) {
                // Land!
                this.isFlying = false;
                this.invulnerable = false;
                this.position.z = 0;
                this.enterPhase3();
            }
        }
    }
};
```

### Boss Tells & Telegraph System
```javascript
class BossTelegraph {
    render(ctx, boss) {
        if (boss.aiState !== 'telegraph') return;

        const attack = boss.nextAttack;
        const progress = boss.telegraphTimer / attack.telegraphDuration;

        // Color changes from yellow -> orange -> red
        const color = this.getTelegraphColor(progress);

        switch(attack.type) {
            case 'melee':
                this.renderMeleeTelegraph(ctx, boss, attack, color, progress);
                break;
            case 'aoe':
                this.renderAoETelegraph(ctx, boss, attack, color, progress);
                break;
            case 'cone':
                this.renderConeTelegraph(ctx, boss, attack, color, progress);
                break;
            case 'line':
                this.renderLineTelegraph(ctx, boss, attack, color, progress);
                break;
            case 'charge':
                this.renderChargeTelegraph(ctx, boss, attack, color, progress);
                break;
        }

        // Flash warning at end of telegraph
        if (progress > 0.8) {
            const flash = Math.sin(Date.now() / 50) * 0.5 + 0.5;
            ctx.globalAlpha = flash;
            this.renderDangerIcon(ctx, boss);
            ctx.globalAlpha = 1;
        }
    }

    getTelegraphColor(progress) {
        if (progress < 0.5) {
            return `rgba(255, 255, 0, ${0.3 + progress * 0.4})`; // Yellow
        } else if (progress < 0.8) {
            return `rgba(255, 165, 0, ${0.3 + progress * 0.4})`; // Orange
        } else {
            return `rgba(255, 0, 0, ${0.3 + progress * 0.4})`; // Red
        }
    }

    renderAoETelegraph(ctx, boss, attack, color, progress) {
        ctx.save();
        ctx.fillStyle = color;
        ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        ctx.lineWidth = 2;

        // Expanding circle
        const radius = attack.range * progress;

        ctx.beginPath();
        ctx.arc(boss.position.x, boss.position.y, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Inner warning ring
        if (progress > 0.5) {
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(boss.position.x, boss.position.y, attack.range * 0.8, 0, Math.PI * 2);
            ctx.stroke();
        }

        ctx.restore();
    }

    renderConeTelegraph(ctx, boss, attack, color, progress) {
        ctx.save();
        ctx.fillStyle = color;

        const angle = boss.facing;
        const arc = attack.arc * Math.PI / 180;

        ctx.beginPath();
        ctx.moveTo(boss.position.x, boss.position.y);
        ctx.arc(
            boss.position.x,
            boss.position.y,
            attack.range,
            angle - arc / 2,
            angle + arc / 2
        );
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }

    renderLineTelegraph(ctx, boss, attack, color, progress) {
        ctx.save();
        ctx.fillStyle = color;

        // Direction to player
        const dx = this.game.player.position.x - boss.position.x;
        const dy = this.game.player.position.y - boss.position.y;
        const angle = Math.atan2(dy, dx);

        // Rectangle for line attack
        ctx.translate(boss.position.x, boss.position.y);
        ctx.rotate(angle);
        ctx.fillRect(0, -attack.width / 2, attack.length, attack.width);

        // Pulsing edge
        if (progress > 0.6) {
            ctx.strokeStyle = 'rgba(255, 0, 0, ' + (Math.sin(Date.now() / 100) * 0.5 + 0.5) + ')';
            ctx.lineWidth = 4;
            ctx.strokeRect(0, -attack.width / 2, attack.length, attack.width);
        }

        ctx.restore();
    }
}
```

---

## 4. Death Mechanics

### Death & Respawn System
```javascript
class DeathSystem {
    constructor(game) {
        this.game = game;
        this.deathCount = 0;
        this.lastDeathPosition = null;
        this.soulStash = {
            experience: 0,
            gold: 0,
            position: null
        };
    }

    onPlayerDeath() {
        this.deathCount++;

        // Store death position
        this.lastDeathPosition = {
            x: this.game.player.x,
            y: this.game.player.y,
            area: this.game.currentArea
        };

        // Calculate soul loss
        const expLoss = Math.floor(this.game.player.experience * 0.5);
        const goldLoss = Math.floor(this.game.player.gold * 0.3);

        // Create blood stain at death location
        this.soulStash = {
            experience: expLoss,
            gold: goldLoss,
            position: { ...this.lastDeathPosition },
            timestamp: Date.now(),
            active: true
        };

        // Reduce player resources
        this.game.player.experience -= expLoss;
        this.game.player.gold -= goldLoss;

        // Show death screen
        this.showDeathScreen();

        // Respawn at last bonfire
        setTimeout(() => {
            this.respawnPlayer();
        }, 3000);

        // Play death sound
        this.game.audio.playSFX('death');
        this.game.audio.stopMusic();
    }

    respawnPlayer() {
        const lastBonfire = this.game.lastBonfireUsed || this.game.startingBonfire;

        // Full heal on respawn
        this.game.player.hp = this.game.player.maxHp;
        this.game.player.stamina = this.game.player.maxStamina;

        // Restore consumables
        this.game.player.estusCharges = this.game.player.maxEstusCharges;

        // Teleport to bonfire
        this.game.player.x = lastBonfire.x;
        this.game.player.y = lastBonfire.y;
        this.game.currentArea = lastBonfire.area;

        // Reset world state
        this.respawnEnemies();

        // Hide death screen
        this.hideDeathScreen();

        // Resume music
        this.game.audio.playMusic('overworld');

        // Show respawn message
        this.game.showText(`You respawn at ${lastBonfire.name}`);
    }

    respawnEnemies() {
        // All non-boss enemies respawn
        this.game.enemies = this.game.enemies.filter(e => e.isBoss);

        // Respawn regular enemies
        this.game.spawnAreaEnemies(this.game.currentArea);
    }

    recoverSouls() {
        if (!this.soulStash.active) return false;

        // Check if player is near their blood stain
        const dx = this.game.player.x - this.soulStash.position.x;
        const dy = this.game.player.y - this.soulStash.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 20) {
            // Recover souls!
            this.game.player.experience += this.soulStash.experience;
            this.game.player.gold += this.soulStash.gold;

            this.soulStash.active = false;

            // Visual effect
            this.createSoulRecoveryEffect();

            // Play sound
            this.game.audio.playSFX('soul_recovery');

            // Show message
            this.game.showText(`Souls recovered! +${this.soulStash.experience} EXP, +${this.soulStash.gold} Gold`);

            return true;
        }

        return false;
    }

    onDeathBeforeRecovery() {
        // Died before recovering souls - they're lost forever!
        if (this.soulStash.active) {
            this.game.showText(`Your souls are lost forever...`);
            this.soulStash.active = false;
            this.soulStash.experience = 0;
            this.soulStash.gold = 0;
        }
    }

    showDeathScreen() {
        const deathScreen = document.getElementById('deathScreen');
        deathScreen.style.display = 'block';

        // Update death message
        const messages = [
            'YOU DIED',
            'DEFEATED',
            'SLAIN',
            'DEATH',
            'GAME OVER'
        ];

        const message = messages[Math.floor(Math.random() * messages.length)];
        document.getElementById('deathMessage').textContent = message;

        // Show death count
        document.getElementById('deathCount').textContent = `Deaths: ${this.deathCount}`;

        // Fade in effect
        deathScreen.style.opacity = 0;
        let opacity = 0;
        const fadeIn = setInterval(() => {
            opacity += 0.05;
            deathScreen.style.opacity = opacity;
            if (opacity >= 1) clearInterval(fadeIn);
        }, 50);
    }

    createSoulRecoveryEffect() {
        // Particle effect when recovering souls
        for (let i = 0; i < 20; i++) {
            this.game.particles.push({
                x: this.soulStash.position.x,
                y: this.soulStash.position.y,
                vx: (Math.random() - 0.5) * 5,
                vy: (Math.random() - 0.5) * 5,
                life: 1.0,
                decay: 0.02,
                size: Math.random() * 4 + 2,
                color: '#00f2fe'
            });
        }
    }

    renderBloodStain(ctx) {
        if (!this.soulStash.active) return;

        const stain = this.soulStash.position;

        // Draw blood stain at death location
        ctx.save();

        // Pulsing glow
        const pulse = Math.sin(Date.now() / 500) * 0.3 + 0.7;
        ctx.globalAlpha = pulse;

        // Outer glow
        ctx.fillStyle = 'rgba(139, 0, 0, 0.5)';
        ctx.beginPath();
        ctx.arc(stain.x, stain.y, 12, 0, Math.PI * 2);
        ctx.fill();

        // Inner stain
        ctx.fillStyle = '#8b0000';
        ctx.beginPath();
        ctx.arc(stain.x, stain.y, 8, 0, Math.PI * 2);
        ctx.fill();

        // Soul count indicator
        ctx.globalAlpha = 1;
        ctx.fillStyle = '#fff';
        ctx.font = '8px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(`${this.soulStash.experience}`, stain.x, stain.y - 15);

        ctx.restore();
    }
}
```

### Bonfire System
```javascript
class Bonfire {
    constructor(id, x, y, area, name) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.area = area;
        this.name = name;
        this.discovered = false;
        this.lit = false;
    }

    interact(player) {
        if (!this.lit) {
            this.light();
            player.game.showText(`Bonfire lit: ${this.name}`);
            player.game.audio.playSFX('bonfire_lit');
        }

        // Rest at bonfire
        this.rest(player);
    }

    light() {
        this.lit = true;
        this.discovered = true;
    }

    rest(player) {
        // Full heal
        player.hp = player.maxHp;
        player.stamina = player.maxStamina;
        player.estusCharges = player.maxEstusCharges;

        // Set as respawn point
        player.game.lastBonfireUsed = this;

        // Respawn all enemies (except bosses)
        player.game.deathSystem.respawnEnemies();

        // Save game
        player.game.saveGame();

        // Show rest menu
        this.showBonfireMenu(player);

        player.game.showText(`Rested at ${this.name}. Enemies respawned.`);
    }

    showBonfireMenu(player) {
        // Menu options:
        // - Level Up (spend souls)
        // - Attune Equipment
        // - Upgrade Estus Flask
        // - Fast Travel (to other lit bonfires)
        // - Leave
    }

    render(ctx) {
        ctx.save();

        if (this.lit) {
            // Animated flames
            const flameHeight = 15 + Math.sin(Date.now() / 100) * 3;
            const flameWidth = 8 + Math.sin(Date.now() / 80) * 2;

            // Glow
            ctx.fillStyle = 'rgba(255, 165, 0, 0.3)';
            ctx.beginPath();
            ctx.arc(this.x, this.y, 20, 0, Math.PI * 2);
            ctx.fill();

            // Flame gradient
            const gradient = ctx.createRadialGradient(
                this.x, this.y, 0,
                this.x, this.y, flameWidth
            );
            gradient.addColorStop(0, '#fff');
            gradient.addColorStop(0.3, '#ff0');
            gradient.addColorStop(0.7, '#f80');
            gradient.addColorStop(1, '#f00');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.ellipse(this.x, this.y - 5, flameWidth, flameHeight, 0, 0, Math.PI * 2);
            ctx.fill();

            // Embers
            if (Math.random() > 0.9) {
                this.spawnEmber();
            }
        } else {
            // Unlit bonfire
            ctx.fillStyle = '#555';
            ctx.beginPath();
            ctx.arc(this.x, this.y, 8, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }

    spawnEmber() {
        this.game.particles.push({
            x: this.x + (Math.random() - 0.5) * 10,
            y: this.y,
            vx: (Math.random() - 0.5) * 0.5,
            vy: -1 - Math.random(),
            life: 1.0,
            decay: 0.02,
            size: 2,
            color: '#ff8800'
        });
    }
}
```

### Risk/Reward System
```javascript
class RiskRewardSystem {
    // High risk areas have better rewards
    calculateDropQuality(area) {
        const riskLevel = area.dangerLevel; // 1-10
        const baseDropRate = 0.05;
        const rareDropRate = baseDropRate * (1 + riskLevel * 0.2);

        return {
            commonChance: 1 - rareDropRate,
            rareChance: rareDropRate * 0.7,
            epicChance: rareDropRate * 0.25,
            legendaryChance: rareDropRate * 0.05
        };
    }

    // Risk vs Reward decision: Push forward or go back to bonfire?
    evaluateRiskDecision(player) {
        const distanceToBonfire = this.calculatePathDistance(
            player.position,
            player.game.lastBonfireUsed.position
        );

        const hpPercent = player.hp / player.maxHp;
        const estusLeft = player.estusCharges;
        const soulsHeld = player.experience; // Unspent souls

        // Risk score: High = very dangerous to continue
        let riskScore = 0;

        if (hpPercent < 0.3) riskScore += 40;
        else if (hpPercent < 0.5) riskScore += 20;

        if (estusLeft === 0) riskScore += 50;
        else if (estusLeft === 1) riskScore += 30;

        if (soulsHeld > 1000) riskScore += 30;
        else if (soulsHeld > 500) riskScore += 15;

        if (distanceToBonfire > 200) riskScore += 20;

        // Decision tension: "Do I risk it for one more room?"
        return {
            risk: riskScore,
            recommendation: riskScore > 60 ? 'Turn back!' : 'Press forward'
        };
    }
}
```

---

## 5. Build Variety

### Character Stats & Scaling
```javascript
class CharacterStats {
    constructor() {
        // Base stats (Souls-like stat system)
        this.vigor = 10;      // HP scaling
        this.endurance = 10;  // Stamina scaling
        this.strength = 10;   // Physical damage, heavy weapon req
        this.dexterity = 10;  // Attack speed, light weapon scaling
        this.intelligence = 10; // Magic damage
        this.faith = 10;      // Healing, holy damage
        this.arcane = 10;     // Item discovery, status effects

        // Derived stats
        this.level = 1;
        this.soulsForNextLevel = 100;
    }

    // Calculate HP from vigor
    calculateMaxHP() {
        // Soft cap at 40, hard cap at 60
        let hp = 300;

        for (let i = 1; i <= this.vigor; i++) {
            if (i <= 40) {
                hp += 20; // 20 HP per point
            } else if (i <= 60) {
                hp += 10; // Diminishing returns
            } else {
                hp += 5; // Hard cap
            }
        }

        return hp;
    }

    // Calculate stamina from endurance
    calculateMaxStamina() {
        let stamina = 80;

        for (let i = 1; i <= this.endurance; i++) {
            if (i <= 40) {
                stamina += 2;
            } else if (i <= 60) {
                stamina += 1;
            } else {
                stamina += 0.5;
            }
        }

        return Math.floor(stamina);
    }

    // Weapon damage scaling
    calculateWeaponDamage(weapon) {
        let damage = weapon.baseDamage;

        // Apply stat scaling
        if (weapon.strScaling) {
            const strBonus = this.getScalingBonus(this.strength, weapon.strScaling);
            damage += strBonus;
        }

        if (weapon.dexScaling) {
            const dexBonus = this.getScalingBonus(this.dexterity, weapon.dexScaling);
            damage += dexBonus;
        }

        if (weapon.intScaling) {
            const intBonus = this.getScalingBonus(this.intelligence, weapon.intScaling);
            damage += intBonus;
        }

        if (weapon.faiScaling) {
            const faiBonus = this.getScalingBonus(this.faith, weapon.faiScaling);
            damage += faiBonus;
        }

        return Math.floor(damage);
    }

    // Scaling grades: S (2.0) > A (1.5) > B (1.2) > C (1.0) > D (0.7) > E (0.4)
    getScalingBonus(statValue, scalingGrade) {
        const scalingMult = {
            'S': 2.0,
            'A': 1.5,
            'B': 1.2,
            'C': 1.0,
            'D': 0.7,
            'E': 0.4
        };

        const mult = scalingMult[scalingGrade] || 0;
        return statValue * mult;
    }

    // Level up cost increases exponentially
    levelUp(stat) {
        if (this.souls < this.soulsForNextLevel) return false;

        this.souls -= this.soulsForNextLevel;
        this[stat]++;
        this.level++;

        // Recalculate cost for next level
        this.soulsForNextLevel = Math.floor(100 * Math.pow(1.15, this.level));

        // Recalculate derived stats
        this.maxHp = this.calculateMaxHP();
        this.maxStamina = this.calculateMaxStamina();

        return true;
    }
}
```

### Build Archetypes
```javascript
const BUILD_ARCHETYPES = {
    knight: {
        name: 'Knight',
        description: 'Balanced STR build with heavy armor and shield',
        startingStats: {
            vigor: 14,
            endurance: 12,
            strength: 14,
            dexterity: 10,
            intelligence: 8,
            faith: 10,
            arcane: 8
        },
        startingEquipment: {
            weapon: 'longsword',
            shield: 'knight_shield',
            armor: 'chainmail_set'
        },
        playstyle: 'Tank with shield, punish with heavy attacks',
        difficulty: 'Easy'
    },

    rogue: {
        name: 'Rogue',
        description: 'DEX build focused on fast attacks and dodging',
        startingStats: {
            vigor: 10,
            endurance: 14,
            strength: 8,
            dexterity: 16,
            intelligence: 10,
            faith: 8,
            arcane: 10
        },
        startingEquipment: {
            weapon: 'dual_daggers',
            shield: null,
            armor: 'leather_set'
        },
        playstyle: 'Fast combos, dodge everything, high skill ceiling',
        difficulty: 'Hard'
    },

    mage: {
        name: 'Mage',
        description: 'INT build using magic spells and enchanted weapons',
        startingStats: {
            vigor: 8,
            endurance: 10,
            strength: 8,
            dexterity: 10,
            intelligence: 16,
            faith: 10,
            arcane: 14
        },
        startingEquipment: {
            weapon: 'enchanted_staff',
            shield: null,
            armor: 'robe_set',
            spells: ['magic_missile', 'frost_bolt', 'mana_shield']
        },
        playstyle: 'Ranged magic, fragile but powerful',
        difficulty: 'Medium'
    },

    paladin: {
        name: 'Paladin',
        description: 'FAI build with holy magic and healing',
        startingStats: {
            vigor: 12,
            endurance: 10,
            strength: 12,
            dexterity: 8,
            intelligence: 8,
            faith: 16,
            arcane: 10
        },
        startingEquipment: {
            weapon: 'holy_mace',
            shield: 'knight_shield',
            armor: 'plate_set',
            spells: ['heal', 'divine_smite', 'blessing']
        },
        playstyle: 'Hybrid melee/support, self-healing tank',
        difficulty: 'Easy'
    },

    berserker: {
        name: 'Berserker',
        description: 'Pure STR build with massive two-handed weapons',
        startingStats: {
            vigor: 16,
            endurance: 16,
            strength: 18,
            dexterity: 8,
            intelligence: 8,
            faith: 8,
            arcane: 8
        },
        startingEquipment: {
            weapon: 'great_axe',
            shield: null,
            armor: 'barbarian_furs'
        },
        playstyle: 'Massive damage, slow attacks, high risk/reward',
        difficulty: 'Hard'
    },

    spellblade: {
        name: 'Spellblade',
        description: 'Hybrid DEX/INT build with fast weapons and spells',
        startingStats: {
            vigor: 10,
            endurance: 12,
            strength: 8,
            dexterity: 14,
            intelligence: 14,
            faith: 8,
            arcane: 10
        },
        startingEquipment: {
            weapon: 'enchanted_rapier',
            shield: null,
            armor: 'battle_mage_set',
            spells: ['weapon_buff', 'frost_step', 'arcane_blade']
        },
        playstyle: 'Combo melee with spell buffs, very versatile',
        difficulty: 'Medium'
    }
};
```

### Weapon Types & Movesets
```javascript
const WEAPON_TYPES = {
    longsword: {
        name: 'Longsword',
        type: 'straight_sword',
        baseDamage: 80,
        strScaling: 'C',
        dexScaling: 'C',
        requirements: { str: 10, dex: 10 },
        weight: 6,
        moveset: {
            light: {
                combo: [
                    { damage: 1.0, frames: 400, startup: 100, active: 150, recovery: 150 },
                    { damage: 1.0, frames: 400, startup: 100, active: 150, recovery: 150 },
                    { damage: 1.2, frames: 500, startup: 150, active: 200, recovery: 150 } // Finisher
                ],
                staminaCost: 15
            },
            heavy: {
                damage: 1.8,
                frames: 750,
                startup: 250,
                active: 200,
                recovery: 300,
                staminaCost: 30,
                poiseBreak: 20
            }
        },
        description: 'Versatile and balanced for all situations'
    },

    great_axe: {
        name: 'Orcish Great Axe',
        type: 'great_weapon',
        baseDamage: 150,
        strScaling: 'A',
        dexScaling: 'E',
        requirements: { str: 24, dex: 8 },
        weight: 14,
        moveset: {
            light: {
                damage: 1.5,
                frames: 600,
                startup: 200,
                active: 250,
                recovery: 150,
                staminaCost: 25,
                arc: 180 // Wide swing
            },
            heavy: {
                damage: 2.5,
                frames: 1100,
                startup: 400,
                active: 300,
                recovery: 400,
                staminaCost: 45,
                guardBreak: true, // Breaks blocks!
                poiseBreak: 50,
                shockwave: 30 // AoE damage
            }
        },
        description: 'Devastating power but extremely slow. For STR builds only.'
    },

    dual_daggers: {
        name: 'Assassin\'s Daggers',
        type: 'dual_wield',
        baseDamage: 45,
        strScaling: 'E',
        dexScaling: 'A',
        requirements: { str: 6, dex: 16 },
        weight: 3,
        moveset: {
            light: {
                combo: [
                    { damage: 0.6, frames: 250 },
                    { damage: 0.6, frames: 250 },
                    { damage: 0.6, frames: 250 },
                    { damage: 0.6, frames: 250 },
                    { damage: 1.0, frames: 400 } // 5-hit combo!
                ],
                staminaCost: 12
            },
            heavy: {
                damage: 1.4,
                frames: 600,
                startup: 150,
                active: 250,
                recovery: 200,
                staminaCost: 20,
                backstabMultiplier: 3.0 // Huge backstab damage!
            }
        },
        passive: {
            extraDodges: 1, // Can dodge twice in a row
            backstabBonus: 2.0 // 2x backstab damage
        },
        description: 'Lightning fast combos. Highest skill ceiling.'
    },

    enchanted_staff: {
        name: 'Archmage Staff',
        type: 'catalyst',
        baseDamage: 60,
        intScaling: 'S',
        requirements: { int: 14 },
        weight: 5,
        moveset: {
            light: {
                spell: 'magic_missile',
                damage: 1.0,
                frames: 500,
                staminaCost: 20,
                fpCost: 15 // Focus Points for spells
            },
            heavy: {
                spell: 'soul_spear',
                damage: 3.0,
                frames: 1200,
                startup: 600,
                staminaCost: 30,
                fpCost: 40
            }
        },
        passive: {
            maxFP: 150,
            spellPower: 1.2
        },
        description: 'Channel devastating spells at range'
    }
};
```

### Armor Sets & Trade-offs
```javascript
const ARMOR_SETS = {
    heavy_plate: {
        name: 'Knight\'s Plate Armor',
        weight: 35,
        defense: {
            physical: 80,
            magic: 40,
            fire: 60,
            lightning: 50
        },
        poise: 40, // Resist stagger
        effects: {
            staminaRegen: 0.7, // -30% stamina regen
            rollSpeed: 0.8, // Slower rolls
            dodgeCost: 1.4 // +40% dodge cost
        },
        description: 'Maximum defense but heavy. Requires high endurance.'
    },

    medium_chain: {
        name: 'Chainmail Armor',
        weight: 20,
        defense: {
            physical: 50,
            magic: 30,
            fire: 40,
            lightning: 35
        },
        poise: 20,
        effects: {
            staminaRegen: 1.0,
            rollSpeed: 1.0,
            dodgeCost: 1.0
        },
        description: 'Balanced protection and mobility'
    },

    light_leather: {
        name: 'Rogue\'s Leathers',
        weight: 8,
        defense: {
            physical: 20,
            magic: 15,
            fire: 20,
            lightning: 20
        },
        poise: 5,
        effects: {
            staminaRegen: 1.3, // +30% stamina regen!
            rollSpeed: 1.2, // Faster rolls
            dodgeCost: 0.8, // -20% dodge cost
            backstabDamage: 1.5 // +50% backstab damage
        },
        description: 'Minimal defense but maximum mobility. For dodge masters.'
    }
};
```

---

## 6. World Structure

### Interconnected World Design
```javascript
class WorldMap {
    constructor() {
        this.areas = {
            // Starting area
            elwynn_forest: {
                id: 'elwynn_forest',
                name: 'Elwynn Forest',
                dangerLevel: 1,
                enemies: ['wolf', 'kobold', 'spider'],
                boss: null,
                bonfires: [
                    { id: 'elwynn_start', name: 'Northshire Abbey', x: 100, y: 100 }
                ],
                connections: [
                    { to: 'westfall', type: 'path', locked: false },
                    { to: 'redridge', type: 'path', locked: false },
                    { to: 'stormwind', type: 'gate', locked: true, key: 'stormwind_key' }
                ],
                shortcuts: [
                    {
                        from: { x: 200, y: 150 },
                        to: 'elwynn_start',
                        type: 'elevator',
                        unlocked: false,
                        description: 'Elevator shortcut back to start'
                    }
                ]
            },

            // Mid-game area
            westfall: {
                id: 'westfall',
                name: 'Westfall',
                dangerLevel: 3,
                enemies: ['gnoll', 'bandit', 'harpy'],
                boss: 'hogger',
                bonfires: [
                    { id: 'sentinel_hill', name: 'Sentinel Hill', x: 300, y: 200 }
                ],
                connections: [
                    { to: 'elwynn_forest', type: 'path', locked: false },
                    { to: 'deadmines', type: 'dungeon_entrance', locked: false },
                    { to: 'duskwood', type: 'path', locked: false }
                ],
                shortcuts: [
                    {
                        from: { x: 350, y: 250 },
                        to: 'elwynn_forest',
                        type: 'hidden_tunnel',
                        unlocked: false,
                        description: 'Secret tunnel back to Elwynn'
                    }
                ]
            },

            // Late game area
            burning_steppes: {
                id: 'burning_steppes',
                name: 'Burning Steppes',
                dangerLevel: 8,
                enemies: ['fire_elemental', 'black_dragonkin', 'demon'],
                boss: 'onyxia',
                bonfires: [
                    { id: 'morgan_vigil', name: 'Morgan\'s Vigil', x: 500, y: 400 }
                ],
                connections: [
                    { to: 'redridge', type: 'mountain_pass', locked: false },
                    { to: 'blackrock_depths', type: 'dungeon_entrance', locked: true, key: 'blackrock_key' },
                    { to: 'onyxia_lair', type: 'boss_gate', locked: true, key: 'onyxia_seal' }
                ],
                shortcuts: []
            }
        };

        // World layout positions
        this.areaPositions = {
            'elwynn_forest': { worldX: 0, worldY: 0 },
            'westfall': { worldX: -1, worldY: 0 },
            'redridge': { worldX: 1, worldY: 0 },
            'duskwood': { worldX: -1, worldY: 1 },
            'stormwind': { worldX: 0, worldY: -1 },
            'burning_steppes': { worldX: 2, worldY: 0 }
        };
    }

    // Check if area is accessible
    canAccessArea(from, to, player) {
        const fromArea = this.areas[from];
        const connection = fromArea.connections.find(c => c.to === to);

        if (!connection) return false;

        // Check if locked
        if (connection.locked) {
            // Check if player has key
            if (connection.key && !player.hasItem(connection.key)) {
                return false;
            }
        }

        return true;
    }

    // Unlock shortcut
    unlockShortcut(area, shortcutIndex, player) {
        const areaData = this.areas[area];
        const shortcut = areaData.shortcuts[shortcutIndex];

        if (!shortcut || shortcut.unlocked) return false;

        shortcut.unlocked = true;

        // Save to player data
        if (!player.unlockedShortcuts) player.unlockedShortcuts = [];
        player.unlockedShortcuts.push({
            area: area,
            index: shortcutIndex
        });

        this.game.showText(`Shortcut unlocked: ${shortcut.description}`);
        this.game.audio.playSFX('shortcut_unlock');

        return true;
    }
}
```

### Metroidvania-style Progression
```javascript
class WorldProgression {
    // Areas unlock as player gains abilities/items
    checkAreaAccess(player) {
        const unlocks = {
            // Early game
            'westfall': true, // Always accessible

            // Need to defeat Hogger to get key
            'deadmines': player.hasDefeatedBoss('hogger'),

            // Need double jump ability
            'duskwood_upper': player.hasAbility('double_jump'),

            // Need fire resistance gear
            'burning_steppes': player.fireResistance >= 50,

            // Need to collect 3 dragon seals
            'onyxia_lair': player.dragonSeals >= 3,

            // Secret area: Find hidden path in Westfall
            'defias_hideout': player.hasDiscovered('secret_tunnel')
        };

        return unlocks;
    }

    // Shortcuts dramatically improve world traversal
    demonstrateShortcutValue() {
        // Without shortcut:
        // Elwynn Start -> Walk 5 minutes -> Westfall Boss -> Walk 5 minutes back

        // With shortcut:
        // Elwynn Start -> Walk 5 minutes -> Unlock elevator
        // Now: Elwynn Start <-> Westfall Boss in 30 seconds!

        // This is the Souls formula: shortcuts are more valuable than fast travel
    }
}
```

### Example World Layout
```
                    [Stormwind Keep]
                           |
                      (locked gate)
                           |
    [Westfall] -------- [Elwynn Forest] -------- [Redridge Mountains]
        |                   |                            |
    (shortcut)          (elevator)                       |
        |                   |                            |
    [Deadmines]         [Goldshire]              [Burning Steppes]
                            |                            |
                        [Duskwood]                  (boss gate)
                            |                            |
                      [Darkshire]                 [Onyxia's Lair]
                            |
                    [Karazhan Tower]

Legend:
------- Path (always open)
(locked) Requires key/item/boss defeat
[Area] Major area with bonfire
```

---

## 7. Difficulty Curve

### Difficulty Design Philosophy
```javascript
class DifficultySystem {
    constructor() {
        // Souls-like difficulty principles:
        // 1. Fair but challenging
        // 2. Consistent rules
        // 3. Telegraphed attacks
        // 4. Punish mistakes
        // 5. Reward mastery

        this.principles = {
            noRubberBanding: true, // Enemies don't scale with player
            consistentRules: true, // Same rules for player and enemies
            telegraphedAttacks: true, // All attacks have tells
            learnablePatterns: true, // Enemies have patterns to learn
            noUnfairDeaths: true // Player should always see death coming
        };
    }

    // Enemy difficulty scaling by area
    getEnemyStats(enemy, area) {
        const baseDifficulty = area.dangerLevel; // 1-10

        return {
            hp: enemy.baseHP * baseDifficulty,
            attack: enemy.baseAttack * (1 + baseDifficulty * 0.15),
            defense: enemy.baseDefense * (1 + baseDifficulty * 0.1),
            aggressiveness: Math.min(2.0, 0.5 + baseDifficulty * 0.15),
            intelligence: Math.min(1.0, baseDifficulty * 0.1) // Better AI in late areas
        };
    }

    // Fair challenge: Player always has tools to succeed
    ensureFairness(encounter) {
        // Check 1: Can player realistically dodge attacks?
        for (const attack of encounter.boss.attacks) {
            if (attack.telegraphDuration < 0.2) {
                console.warn('Attack telegraph too short!', attack);
            }
        }

        // Check 2: Is stamina management reasonable?
        const dodgesNeeded = encounter.attacksPerPhase;
        const staminaForDodges = dodgesNeeded * 25;
        if (staminaForDodges > 100) {
            console.warn('Encounter requires too many dodges!');
        }

        // Check 3: Are there safe moments to heal?
        const recoveryWindows = encounter.boss.attacks.filter(a => a.recovery > 2.0);
        if (recoveryWindows.length === 0) {
            console.warn('Boss has no recovery windows!');
        }

        return {
            fair: true,
            warnings: []
        };
    }

    // Learning curve: Each area teaches new skills
    createLearningPath() {
        return {
            'elwynn_forest': {
                teaches: ['basic combat', 'dodge timing', 'stamina management'],
                threats: ['slow melee enemies', 'basic patterns']
            },
            'westfall': {
                teaches: ['guard breaks', 'combo interrupts', 'positioning'],
                threats: ['ranged enemies', 'aggressive enemies']
            },
            'redridge': {
                teaches: ['parrying', 'ripostes', 'multi-enemy combat'],
                threats: ['groups of enemies', 'ambushes']
            },
            'duskwood': {
                teaches: ['status effects', 'buff management', 'area hazards'],
                threats: ['poison enemies', 'environmental damage']
            },
            'burning_steppes': {
                teaches: ['advanced combos', 'phase management', 'DPS checks'],
                threats: ['mini-bosses', 'time-limited encounters']
            },
            'onyxia_lair': {
                teaches: ['all skills combined', 'perfect execution'],
                threats: ['ultimate boss', '3-phase fight']
            }
        };
    }
}
```

### Player Power Curve
```javascript
class PowerProgression {
    // Souls-like power curve: NOT exponential
    calculatePlayerPower(level, equipment, skills) {
        // Starting power: 100
        // Max power: ~300 (only 3x stronger at max level!)

        let power = 100;

        // Levels give linear scaling (Souls style)
        power += level * 2; // +2 per level

        // Equipment gives 20-30% boost
        const equipmentBonus = this.calculateEquipmentPower(equipment);
        power *= (1 + equipmentBonus);

        // Skill gives the biggest boost (player skill > stats)
        const skillMultiplier = this.calculateSkillBonus(skills);
        power *= skillMultiplier;

        return power;
    }

    calculateSkillBonus(skills) {
        // Mastering mechanics doubles effective power
        let multiplier = 1.0;

        if (skills.parrySuccess > 50) multiplier += 0.3; // 30% boost for parry mastery
        if (skills.dodgePerfection > 0.8) multiplier += 0.4; // 40% boost for dodge mastery
        if (skills.comboCompletion > 0.7) multiplier += 0.3; // 30% boost for combos

        // Master player: 2x effective power even at same level!
        return multiplier;
    }

    // Example power comparison
    demonstratePowerCurve() {
        // New player at level 1: 100 power
        const newbie = {
            level: 1,
            equipment: 0.1,
            skill: 1.0
        };
        // Power: 100 * 1.1 * 1.0 = 110

        // Average player at level 50: 200 power
        const average = {
            level: 50,
            equipment: 0.3,
            skill: 1.2
        };
        // Power: (100 + 50*2) * 1.3 * 1.2 = 312

        // Skilled player at level 1: 200 power (can beat level 50 areas!)
        const skilled = {
            level: 1,
            equipment: 0.1,
            skill: 2.0
        };
        // Power: 100 * 1.1 * 2.0 = 220

        // This demonstrates: SKILL > STATS
    }
}
```

### Boss Difficulty Tiers
```javascript
const BOSS_DIFFICULTY_TIERS = {
    tutorial: {
        name: 'Tutorial Boss',
        examples: ['Kobold Chief'],
        difficulty: 1,
        characteristics: {
            hp: 300,
            attacks: 2,
            phases: 1,
            telegraphTime: 1.0, // Long telegraphs
            attackSpeed: 1.5, // Slow
            comboLength: 1, // Single hits
            tricks: [] // No gimmicks
        },
        purpose: 'Teach boss combat basics'
    },

    miniBoss: {
        name: 'Mini-Boss',
        examples: ['Hogger', 'Gnoll Chieftain'],
        difficulty: 3,
        characteristics: {
            hp: 500,
            attacks: 4,
            phases: 2,
            telegraphTime: 0.6,
            attackSpeed: 1.2,
            comboLength: 2,
            tricks: ['summon adds']
        },
        purpose: 'Test basic skill mastery'
    },

    mainBoss: {
        name: 'Main Boss',
        examples: ['Edwin VanCleef', 'Deadmines Captain'],
        difficulty: 5,
        characteristics: {
            hp: 1000,
            attacks: 6,
            phases: 2,
            telegraphTime: 0.4,
            attackSpeed: 1.0,
            comboLength: 3,
            tricks: ['summon adds', 'phase transition heal', 'environmental hazards']
        },
        purpose: 'Major challenge, requires mastery'
    },

    legendaryBoss: {
        name: 'Legendary Boss',
        examples: ['Onyxia', 'Ragnaros'],
        difficulty: 8,
        characteristics: {
            hp: 2000,
            attacks: 10,
            phases: 3,
            telegraphTime: 0.3,
            attackSpeed: 0.8,
            comboLength: 4,
            tricks: ['flight phase', 'one-shot attacks', 'arena changes', 'rage timer']
        },
        purpose: 'Ultimate skill check'
    },

    secretBoss: {
        name: 'Secret Boss',
        examples: ['Deathwing', 'Ancient Lich'],
        difficulty: 10,
        characteristics: {
            hp: 3000,
            attacks: 15,
            phases: 4,
            telegraphTime: 0.2,
            attackSpeed: 0.6,
            comboLength: 5,
            tricks: ['all mechanics', 'instant kills', 'perfect execution required']
        },
        purpose: 'For masochists only'
    }
};
```

---

## 8. Combat Depth

### Advanced Combat Techniques
```javascript
class AdvancedCombat {
    // Technique 1: Roll Canceling
    rollCancel() {
        // During attack recovery (last 100ms), can cancel into dodge
        if (this.attackState === 'recovery' &&
            this.attackTimer > this.currentAttack.recovery - 100) {
            if (this.dodge()) {
                this.attackState = 'neutral';
                return true;
            }
        }
        return false;
    }

    // Technique 2: Backstab
    backstab(target) {
        // Must be directly behind enemy
        const angle = this.angleTo(target);
        const targetFacing = target.facing;
        const angleDiff = Math.abs(angle - (targetFacing + 180) % 360);

        if (angleDiff < 45 && target.state !== 'attacking') {
            // BACKSTAB!
            const damage = this.weaponDamage * 2.5;
            this.dealCriticalDamage(target, damage);
            this.createBackstabAnimation(target);
            return true;
        }
        return false;
    }

    // Technique 3: Guard Counter
    guardCounter() {
        // Immediately after blocking an attack, quick counter
        if (this.justBlocked && Date.now() - this.blockTime < 500) {
            this.lightAttack();
            this.combat.stamina += 15; // Refund stamina!
            this.attackDamageMultiplier = 1.3; // 30% bonus damage
            return true;
        }
        return false;
    }

    // Technique 4: Jumping Attack
    jumpAttack() {
        // Attack during jump for extra damage
        if (this.isJumping && this.attack()) {
            this.attackDamageMultiplier = 1.5;
            this.attackStagger = 2.0; // Extra stagger
            return true;
        }
        return false;
    }

    // Technique 5: Charged Attack
    chargedAttack() {
        // Hold heavy attack to charge
        if (this.heavyAttackHeld) {
            this.chargeTime = Math.min(2.0, this.chargeTime + deltaTime);

            // Visual charging effect
            this.showChargingEffect(this.chargeTime / 2.0);

            if (this.chargeTime >= 2.0) {
                // Fully charged!
                this.heavyAttackDamage *= 2.0;
                this.heavyAttackPoiseBreak *= 2.0;
                this.showFullChargeEffect();
            }
        }

        // Release to attack
        if (this.heavyAttackReleased) {
            const mult = 1 + this.chargeTime;
            this.heavyAttack(mult);
            this.chargeTime = 0;
        }
    }

    // Technique 6: Weapon Arts
    weaponArt() {
        // Special move unique to each weapon (like Ashes of War)
        const weapon = this.player.weapon;

        if (!weapon.art || this.stamina < weapon.art.cost) return false;

        this.stamina -= weapon.art.cost;

        switch(weapon.art.type) {
            case 'spin_slash':
                // 360° attack
                this.executeSpinAttack();
                break;
            case 'charge':
                // Rush forward
                this.executeChargeAttack();
                break;
            case 'parry':
                // Enhanced parry window
                this.executeEnhancedParry();
                break;
            case 'magic_buff':
                // Temporarily buff weapon
                this.applyWeaponBuff();
                break;
        }

        return true;
    }
}
```

### Combo System
```javascript
class ComboSystem {
    constructor() {
        this.currentCombo = [];
        this.comboTimer = 0;
        this.comboWindow = 500; // 500ms to continue combo
    }

    // Light attack combos
    executeLightCombo(step) {
        const combos = {
            1: {
                animation: 'slash_right',
                damage: 1.0,
                hitbox: { arc: 90, range: 20 },
                nextInputWindow: 300 // Can input next attack in last 300ms
            },
            2: {
                animation: 'slash_left',
                damage: 1.0,
                hitbox: { arc: 90, range: 20 },
                nextInputWindow: 300
            },
            3: {
                animation: 'thrust',
                damage: 1.2,
                hitbox: { arc: 60, range: 25 },
                nextInputWindow: 400
            },
            4: {
                animation: 'overhead_slam',
                damage: 1.5,
                hitbox: { arc: 120, range: 22 },
                knockdown: true,
                finisher: true // Ends combo
            }
        };

        return combos[step];
    }

    // Mix light and heavy attacks
    mixCombo(sequence) {
        // Example sequences:
        // L -> L -> H : Standard 3-hit
        // L -> H : Quick 2-hit heavy
        // L -> L -> L -> H : Full 4-hit finisher

        const comboString = sequence.join('-');

        const specialCombos = {
            'L-L-H': {
                name: 'Quick Finisher',
                damage: [1.0, 1.0, 2.0],
                effect: 'Launches enemy'
            },
            'L-L-L-H': {
                name: 'Berserker Combo',
                damage: [1.0, 1.0, 1.2, 2.5],
                effect: 'Massive damage finisher'
            },
            'H-L-L': {
                name: 'Power Jab',
                damage: [1.5, 0.8, 1.5],
                effect: 'Breaks guard on finisher'
            }
        };

        return specialCombos[comboString] || null;
    }

    // Cancel combo into special move
    comboCancel() {
        // At any point in combo, can spend stamina to cancel into:
        // - Dodge roll (25 stamina)
        // - Parry (15 stamina)
        // - Weapon Art (40 stamina)

        // Example: L -> L -> Dodge -> L -> L
        // This allows for fluid, creative combat
    }
}
```

### Positioning & Spacing
```javascript
class CombatPositioning {
    // Different positions have different risks/rewards
    analyzePosition(player, enemy) {
        const distance = this.distanceBetween(player, enemy);
        const relativeAngle = this.angleRelativeTo(player, enemy);

        return {
            // Front: Most dangerous
            front: relativeAngle < 45 ? {
                risk: 'high',
                reward: 'Can parry/block',
                danger: 'Enemy attacks hit here'
            } : null,

            // Side: Medium risk
            side: relativeAngle >= 45 && relativeAngle < 135 ? {
                risk: 'medium',
                reward: 'Avoid some attacks',
                danger: 'Some AoE still hits'
            } : null,

            // Back: Low risk, high reward
            back: relativeAngle >= 135 ? {
                risk: 'low',
                reward: 'Backstab opportunity!',
                danger: 'Hard to maintain'
            } : null,

            // Distance considerations
            close: distance < 30 ? {
                advantage: 'Fast attacks, enemy can\'t escape',
                disadvantage: 'Hard to see attacks coming'
            } : null,

            medium: distance >= 30 && distance < 60 ? {
                advantage: 'Can react to most attacks',
                disadvantage: 'Enemy can close gap'
            } : null,

            far: distance >= 60 ? {
                advantage: 'Safe, can see everything',
                disadvantage: 'Can\'t punish enemy attacks'
            } : null
        };
    }

    // AI uses same positioning logic
    enemyPositioningAI(enemy, player) {
        const position = this.analyzePosition(enemy, player);

        // If player is behind enemy, turn around!
        if (position.back) {
            enemy.turnToward(player);
        }

        // Aggressive enemies close distance
        if (enemy.aggressive && position.far) {
            enemy.moveToward(player);
        }

        // Defensive enemies maintain spacing
        if (enemy.defensive && position.close) {
            enemy.moveAway(player);
        }
    }
}
```

### Enemy AI Patterns
```javascript
class EnemyAI {
    // Different enemy types have different AI behaviors

    // Aggressive: Constant pressure
    aggressiveAI(enemy, player) {
        if (this.distance > 50) {
            // Close gap quickly
            enemy.moveToward(player, 2.0);
        } else {
            // Chain attacks
            if (enemy.canAttack()) {
                enemy.attack();
            }
        }

        // Rarely backs off
        enemy.retreatChance = 0.1;
    }

    // Defensive: Wait and punish
    defensiveAI(enemy, player) {
        // Keep medium distance
        if (this.distance < 40) {
            enemy.moveAway(player, 1.0);
        }

        // Block player attacks
        if (player.isAttacking) {
            enemy.block();
        }

        // Counter after player misses
        if (player.whiffedAttack) {
            enemy.attack();
        }
    }

    // Tricky: Bait and punish
    trickyAI(enemy, player) {
        // Fake attacks to bait dodges
        if (Math.random() < 0.3) {
            enemy.fakeAttack();

            // If player dodged, punish
            setTimeout(() => {
                if (player.justDodged) {
                    enemy.attack(); // Catches roll!
                }
            }, 400);
        }

        // Unpredictable timing
        enemy.attackDelayVariance = 0.5; // ±50% timing
    }

    // Adaptive: Learns player patterns
    adaptiveAI(enemy, player) {
        // Track player behavior
        enemy.memory = enemy.memory || {
            playerDodgeCount: 0,
            playerBlockCount: 0,
            playerAttackAfterDodge: 0
        };

        // If player always dodges, use roll-catch attacks
        if (enemy.memory.playerDodgeCount > enemy.memory.playerBlockCount * 2) {
            enemy.preferRollCatchAttacks = true;
        }

        // If player always attacks after dodge, bait and parry
        if (enemy.memory.playerAttackAfterDodge > 5) {
            enemy.baitAndParry = true;
        }

        // This creates dynamic difficulty that responds to player skill!
    }
}
```

---

## Implementation Summary

### File Structure Changes
```javascript
// Current: Single giant update loop
update(deltaTime) {
    // Everything in one place
}

// New: Modular systems
class WowMonActionRPG {
    constructor() {
        this.combat = new ActionCombatSystem(this);
        this.death = new DeathSystem(this);
        this.world = new WorldMap();
        this.difficulty = new DifficultySystem();
        this.bosses = new BossManager();
    }

    update(deltaTime) {
        this.combat.update(deltaTime);
        this.death.update(deltaTime);
        this.world.update(deltaTime);

        // Update enemies with AI
        this.enemies.forEach(enemy => enemy.update(deltaTime));

        // Update player
        this.player.update(deltaTime);
    }

    render(ctx) {
        // Render world
        this.world.render(ctx);

        // Render entities
        this.enemies.forEach(enemy => enemy.render(ctx));
        this.player.render(ctx);

        // Render UI
        this.renderUI(ctx);
    }
}
```

### Key Input Mappings
```
Keyboard/Controller Layout:

Movement: WASD / Left Stick
Camera: Mouse / Right Stick

X / □ - Light Attack
Y / △ - Heavy Attack
B / ○ - Dodge Roll
A / ✕ - Interact / Riposte

LT / L2 - Block (hold)
RT / R2 - Lock On (toggle)
LB / L1 - Use Item
RB / R1 - Weapon Art

D-Pad Up - Cycle Items
D-Pad Down - Quick Heal
D-Pad Left/Right - Cycle Lock-On Targets

Start - Menu
Select - Map
```

### Performance Considerations
```javascript
// Limit entities for performance
const MAX_ENEMIES = 10;
const MAX_PARTICLES = 100;
const MAX_PROJECTILES = 20;

// Use object pooling for particles
class ParticlePool {
    constructor(size) {
        this.pool = Array(size).fill(null).map(() => new Particle());
        this.active = [];
    }

    spawn(x, y, config) {
        const particle = this.pool.find(p => !p.active);
        if (particle) {
            particle.reset(x, y, config);
            this.active.push(particle);
        }
    }
}

// Spatial partitioning for collision detection
class SpatialGrid {
    // Only check collisions for nearby entities
    getNearbyEntities(x, y, radius) {
        const cellX = Math.floor(x / this.cellSize);
        const cellY = Math.floor(y / this.cellSize);

        const nearby = [];
        for (let dx = -1; dx <= 1; dx++) {
            for (let dy = -1; dy <= 1; dy++) {
                const cell = this.getCell(cellX + dx, cellY + dy);
                nearby.push(...cell);
            }
        }

        return nearby.filter(e => this.distance(e, {x, y}) < radius);
    }
}
```

---

## Conclusion

This redesign transforms WoWMon from a passive, menu-driven experience into an engaging, skill-based action RPG. Every system is designed around the core Souls-like principles:

1. **Player skill matters more than stats**
2. **Fair but challenging combat**
3. **Meaningful death penalties with recovery mechanics**
4. **Interconnected world with shortcuts**
5. **Diverse builds with real trade-offs**
6. **Memorable boss encounters**
7. **Deep combat system that rewards mastery**

The result is a game where every encounter is tense, every victory feels earned, and every death is a learning opportunity. Players will master dodge timings, memorize boss patterns, and feel genuine accomplishment when they finally overcome a challenging boss.

This is the antithesis of grinding—this is pure, skill-based action RPG gameplay.
