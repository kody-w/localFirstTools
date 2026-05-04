// WoWMon Action RPG - Code Examples
// Complete implementation examples for core systems

// =============================================================================
// 1. CORE COMBAT SYSTEM
// =============================================================================

class ActionCombatSystem {
    constructor(game) {
        this.game = game;
        this.state = 'neutral'; // neutral, attacking, dodging, blocking, stunned
        this.stamina = 100;
        this.maxStamina = 100;
        this.staminaRegen = 25; // per second
        this.combo = 0;
        this.lastAttackTime = 0;
        this.iframes = 0;
        this.lockOn = null;

        // Attack frame data
        this.attackFrames = null;
        this.frameTimer = 0;

        // Input buffer for advanced players
        this.inputBuffer = [];
        this.bufferWindow = 200; // 200ms buffer
    }

    update(deltaTime) {
        // Update stamina
        this.updateStamina(deltaTime);

        // Update attack frames
        if (this.attackFrames) {
            this.frameTimer += deltaTime * 1000;
            if (this.frameTimer >= this.attackFrames.total) {
                this.state = 'neutral';
                this.attackFrames = null;
                this.frameTimer = 0;
            }
        }

        // Update I-frames
        if (this.iframes > 0) {
            this.iframes -= deltaTime * 1000;
        }

        // Update combo timer
        if (Date.now() - this.lastAttackTime > 500) {
            this.combo = 0;
        }

        // Process input buffer
        this.processInputBuffer();

        // Update lock-on
        if (this.lockOn) {
            this.updateLockOn();
        }
    }

    lightAttack() {
        if (this.state !== 'neutral' || this.stamina < 15) return false;

        this.state = 'attacking';
        this.stamina -= 15;
        this.combo = Math.min(4, this.combo + 1);

        // Get combo attack data
        const attack = this.getLightAttackData(this.combo);

        this.attackFrames = {
            startup: attack.startup,
            active: attack.active,
            recovery: attack.recovery,
            total: attack.startup + attack.active + attack.recovery
        };

        this.frameTimer = 0;

        // Create hitbox during active frames
        setTimeout(() => {
            if (this.state === 'attacking') {
                this.createAttackHitbox('light', this.combo, attack);
            }
        }, attack.startup);

        // Reset to neutral after total frames
        setTimeout(() => {
            if (this.state === 'attacking') {
                this.state = 'neutral';
            }
        }, this.attackFrames.total);

        this.lastAttackTime = Date.now();
        this.game.audio.playSFX('attack_light');

        return true;
    }

    heavyAttack() {
        if (this.state !== 'neutral' || this.stamina < 30) return false;

        this.state = 'attacking';
        this.stamina -= 30;
        this.combo = 0; // Heavy attack resets combo

        const attack = {
            startup: 250,
            active: 200,
            recovery: 300,
            damage: 2.0,
            guardBreak: true,
            poiseBreak: 30
        };

        this.attackFrames = {
            startup: attack.startup,
            active: attack.active,
            recovery: attack.recovery,
            total: 750
        };

        this.frameTimer = 0;

        setTimeout(() => {
            if (this.state === 'attacking') {
                this.createAttackHitbox('heavy', 1, attack);
            }
        }, attack.startup);

        setTimeout(() => {
            if (this.state === 'attacking') {
                this.state = 'neutral';
            }
        }, this.attackFrames.total);

        this.game.audio.playSFX('attack_heavy');

        return true;
    }

    dodge() {
        // Can cancel attack recovery into dodge (advanced technique)
        const canCancel = this.state === 'attacking' &&
                         this.frameTimer >= (this.attackFrames.startup + this.attackFrames.active);

        if (this.state !== 'neutral' && !canCancel) return false;
        if (this.stamina < 25) return false;

        this.state = 'dodging';
        this.stamina -= 25;
        this.combo = 0;

        // I-frames: 200ms of invincibility
        this.iframes = 200;

        // Get dodge direction
        const direction = this.game.input.getMovementVector() || { x: 0, y: -1 };

        // Dodge roll movement
        this.game.player.dodgeVelocity = {
            x: direction.x * 180, // 180 pixels in 600ms = fast roll
            y: direction.y * 180
        };

        setTimeout(() => {
            this.state = 'neutral';
            this.game.player.dodgeVelocity = null;
        }, 600);

        this.game.audio.playSFX('dodge');

        return true;
    }

    block(isHolding) {
        if (isHolding) {
            if (this.state !== 'neutral' && this.state !== 'blocking') return false;
            if (this.stamina <= 0) {
                this.staminaBreak();
                return false;
            }

            this.state = 'blocking';

            if (!this.blockStartTime) {
                this.blockStartTime = Date.now();
            }

            return true;
        } else {
            if (this.state === 'blocking') {
                this.state = 'neutral';
                this.blockStartTime = null;
            }
            return true;
        }
    }

    parry() {
        if (this.state !== 'blocking') return false;

        const parryWindow = 150; // 150ms perfect parry window
        const timeSinceBlock = Date.now() - this.blockStartTime;

        if (timeSinceBlock <= parryWindow) {
            // PERFECT PARRY!
            this.state = 'parry_success';
            this.stamina = Math.min(this.maxStamina, this.stamina + 30);

            // Enemy becomes riposte-vulnerable
            if (this.lockOn) {
                this.lockOn.state = 'riposte_vulnerable';
                this.lockOn.riposteWindow = 2000;

                setTimeout(() => {
                    if (this.lockOn && this.lockOn.state === 'riposte_vulnerable') {
                        this.lockOn.state = 'neutral';
                    }
                }, 2000);
            }

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
        if (!this.lockOn || this.lockOn.state !== 'riposte_vulnerable') return false;
        if (this.state !== 'neutral') return false;

        this.state = 'riposting';

        // Riposte deals massive damage
        const damage = this.game.player.getAttackDamage() * 3;

        // Lock both entities in critical animation
        this.lockOn.takeDamage(damage, 0, true);
        this.lockOn.state = 'riposted';

        this.game.audio.playSFX('critical_hit');
        this.createCriticalEffect();

        setTimeout(() => {
            this.state = 'neutral';
            if (this.lockOn && this.lockOn.state === 'riposted') {
                this.lockOn.state = 'neutral';
            }
        }, 1500);

        return true;
    }

    updateStamina(deltaTime) {
        if (this.state === 'blocking') {
            this.stamina -= 5 * deltaTime;
            if (this.stamina <= 0) {
                this.stamina = 0;
                this.staminaBreak();
            }
        } else if (this.state === 'neutral' && this.stamina < this.maxStamina) {
            // Apply armor modifier to stamina regen
            const armorMod = this.game.player.equipment.armor?.staminaRegen || 1.0;
            this.stamina = Math.min(
                this.maxStamina,
                this.stamina + this.staminaRegen * deltaTime * armorMod
            );
        }
    }

    staminaBreak() {
        this.state = 'stunned';
        this.staminaBroken = true;

        this.game.showText('Stamina Broken!');
        this.game.audio.playSFX('stamina_break');

        setTimeout(() => {
            this.state = 'neutral';
            this.staminaBroken = false;
            this.stamina = this.maxStamina * 0.3; // Recover 30% stamina
        }, 2000);
    }

    createAttackHitbox(type, comboStep, attackData) {
        const player = this.game.player;
        const weapon = player.equipment.weapon;

        const range = weapon.range || 20;
        const arc = weapon.arc || 90;

        const hitbox = {
            x: player.x,
            y: player.y,
            range: range,
            arc: arc,
            direction: player.facing,
            damage: attackData.damage || 1.0,
            guardBreak: attackData.guardBreak || false,
            poiseBreak: attackData.poiseBreak || 10
        };

        // Check all enemies in range
        this.game.enemies.forEach(enemy => {
            if (this.checkHitboxCollision(hitbox, enemy)) {
                if (enemy.iframes <= 0) {
                    this.onHit(enemy, hitbox);
                }
            }
        });

        // Visual effect
        this.createAttackEffect(hitbox);
    }

    checkHitboxCollision(hitbox, enemy) {
        const dx = enemy.x - hitbox.x;
        const dy = enemy.y - hitbox.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > hitbox.range) return false;

        // Check if enemy is within arc
        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
        const facingAngle = this.directionToAngle(hitbox.direction);
        let angleDiff = Math.abs(angle - facingAngle);

        // Normalize angle difference
        if (angleDiff > 180) angleDiff = 360 - angleDiff;

        return angleDiff <= hitbox.arc / 2;
    }

    onHit(enemy, hitbox) {
        const player = this.game.player;
        const weapon = player.equipment.weapon;

        // Calculate damage
        let damage = player.getAttackDamage() * hitbox.damage;

        // Combo multiplier
        if (this.combo > 1) {
            damage *= (1 + (this.combo - 1) * 0.2);
        }

        // Backstab check
        const isBackstab = this.checkBackstab(player, enemy);
        if (isBackstab) {
            damage *= 2.5;
            this.game.audio.playSFX('backstab');
            this.createBackstabEffect(enemy);
        }

        // Apply damage
        const killed = enemy.takeDamage(damage, hitbox.poiseBreak, hitbox.guardBreak);

        // Visual feedback
        this.createHitEffect(enemy.x, enemy.y);
        this.game.audio.playSFX(isBackstab ? 'critical_hit' : 'hit');

        // Camera shake
        this.game.camera.shake(hitbox.damage * 2);

        // Show damage number
        this.showDamageNumber(enemy.x, enemy.y, Math.floor(damage));

        // Combo counter
        if (this.combo > 2) {
            this.showComboText(this.combo);
        }
    }

    checkBackstab(player, enemy) {
        const dx = enemy.x - player.x;
        const dy = enemy.y - player.y;
        const angleToEnemy = Math.atan2(dy, dx) * 180 / Math.PI;
        const enemyFacing = this.directionToAngle(enemy.facing);

        // Player must be behind enemy
        let angleDiff = Math.abs(angleToEnemy - (enemyFacing + 180) % 360);
        if (angleDiff > 180) angleDiff = 360 - angleDiff;

        return angleDiff < 45 && enemy.state !== 'attacking';
    }

    getLightAttackData(comboStep) {
        const weapon = this.game.player.equipment.weapon;

        // Different weapons have different combo patterns
        const comboData = {
            1: { startup: 100, active: 150, recovery: 150, damage: 1.0 },
            2: { startup: 100, active: 150, recovery: 150, damage: 1.0 },
            3: { startup: 150, active: 200, recovery: 150, damage: 1.2 },
            4: { startup: 200, active: 250, recovery: 200, damage: 1.5 } // Finisher
        };

        return comboData[comboStep] || comboData[1];
    }

    directionToAngle(direction) {
        const angles = { up: -90, down: 90, left: 180, right: 0 };
        return angles[direction] || 0;
    }

    processInputBuffer() {
        // Advanced: Allow buffering inputs during attack animations
        const now = Date.now();
        this.inputBuffer = this.inputBuffer.filter(input =>
            now - input.time < this.bufferWindow
        );

        if (this.state === 'neutral' && this.inputBuffer.length > 0) {
            const input = this.inputBuffer.shift();
            this[input.action]();
        }
    }

    bufferInput(action) {
        this.inputBuffer.push({
            action: action,
            time: Date.now()
        });
    }

    // Lock-on system
    toggleLockOn() {
        if (!this.lockOn) {
            const nearestEnemy = this.findNearestEnemy(150);
            if (nearestEnemy) {
                this.lockOn = nearestEnemy;
                this.lockOn.isLockedOn = true;
                this.game.audio.playSFX('lock_on');
            }
        } else {
            this.lockOn.isLockedOn = false;
            this.lockOn = null;
        }
    }

    findNearestEnemy(maxDistance) {
        const player = this.game.player;
        let nearest = null;
        let minDist = maxDistance;

        this.game.enemies.forEach(enemy => {
            const dx = enemy.x - player.x;
            const dy = enemy.y - player.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < minDist) {
                minDist = dist;
                nearest = enemy;
            }
        });

        return nearest;
    }

    updateLockOn() {
        if (!this.lockOn || this.lockOn.isDead) {
            this.lockOn = null;
            return;
        }

        // Auto-face locked enemy
        const player = this.game.player;
        const dx = this.lockOn.x - player.x;
        const dy = this.lockOn.y - player.y;

        if (Math.abs(dx) > Math.abs(dy)) {
            player.facing = dx > 0 ? 'right' : 'left';
        } else {
            player.facing = dy > 0 ? 'down' : 'up';
        }

        // Draw lock-on indicator
        this.renderLockOnIndicator();
    }

    renderLockOnIndicator() {
        if (!this.lockOn) return;

        const ctx = this.game.ctx;
        const camera = this.game.camera;

        const screenX = this.lockOn.x - camera.x;
        const screenY = this.lockOn.y - camera.y;

        ctx.save();
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 2;

        // Rotating brackets
        const angle = Date.now() / 500;
        const size = 16;

        ctx.translate(screenX, screenY);
        ctx.rotate(angle);

        // Four corner brackets
        for (let i = 0; i < 4; i++) {
            ctx.save();
            ctx.rotate((Math.PI / 2) * i);
            ctx.translate(size, size);

            ctx.beginPath();
            ctx.moveTo(-4, -4);
            ctx.lineTo(4, -4);
            ctx.lineTo(4, 4);
            ctx.stroke();

            ctx.restore();
        }

        ctx.restore();
    }

    createHitEffect(x, y) {
        // Spawn hit particles
        for (let i = 0; i < 10; i++) {
            this.game.particles.spawn({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 100,
                vy: (Math.random() - 0.5) * 100,
                life: 0.5,
                size: 2,
                color: '#ff8800'
            });
        }
    }

    createParryEffect() {
        const player = this.game.player;

        // Ring of particles
        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2;
            this.game.particles.spawn({
                x: player.x,
                y: player.y,
                vx: Math.cos(angle) * 80,
                vy: Math.sin(angle) * 80,
                life: 0.8,
                size: 3,
                color: '#00f2fe'
            });
        }
    }

    createCriticalEffect(x, y) {
        // Explosion of particles
        for (let i = 0; i < 30; i++) {
            this.game.particles.spawn({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 150,
                vy: (Math.random() - 0.5) * 150,
                life: 1.0,
                size: 4,
                color: '#ff0000'
            });
        }
    }

    showDamageNumber(x, y, damage) {
        this.game.floatingText.add({
            x: x,
            y: y,
            text: Math.floor(damage).toString(),
            color: '#ff0000',
            life: 1.0,
            vy: -50
        });
    }

    showComboText(combo) {
        const player = this.game.player;
        this.game.floatingText.add({
            x: player.x,
            y: player.y - 20,
            text: `${combo} HIT COMBO!`,
            color: '#00f2fe',
            life: 1.5,
            vy: -30,
            scale: 1.5
        });
    }
}

// =============================================================================
// 2. BOSS ENEMY SYSTEM
// =============================================================================

class BossEnemy {
    constructor(game, id, data) {
        this.game = game;
        this.id = id;
        this.name = data.name;
        this.hp = data.hp;
        this.maxHp = data.hp;
        this.poise = data.poise || 100;
        this.maxPoise = data.poise || 100;

        this.x = data.x || 0;
        this.y = data.y || 0;
        this.facing = data.facing || 'down';

        this.phases = data.phases || 1;
        this.currentPhase = 1;

        this.aiState = 'idle';
        this.stateTimer = 0;
        this.attackPattern = data.attackPattern;
        this.nextAttack = null;

        this.isBoss = true;
        this.isDead = false;
        this.isLockedOn = false;

        this.uniqueMechanic = data.uniqueMechanic;
    }

    update(deltaTime) {
        if (this.isDead) return;

        // Check phase transitions
        const hpPercent = this.hp / this.maxHp;
        if (hpPercent <= 0.5 && this.currentPhase === 1 && this.phases >= 2) {
            this.enterPhase2();
        } else if (hpPercent <= 0.25 && this.currentPhase === 2 && this.phases >= 3) {
            this.enterPhase3();
        }

        // Update AI state machine
        this.updateAI(deltaTime);

        // Update unique mechanic
        if (this.uniqueMechanic && this.uniqueMechanic.update) {
            this.uniqueMechanic.update(deltaTime);
        }

        this.stateTimer += deltaTime;
    }

    updateAI(deltaTime) {
        const player = this.game.player;
        const distance = this.distanceTo(player);

        switch(this.aiState) {
            case 'idle':
                // Observe player, then choose attack
                if (this.stateTimer > 1.0) {
                    this.chooseNextAttack(player, distance);
                    this.aiState = 'telegraph';
                    this.stateTimer = 0;
                }

                // Face player
                this.faceTarget(player);
                break;

            case 'telegraph':
                // Show attack warning
                this.showTelegraph(this.nextAttack);

                if (this.stateTimer >= this.nextAttack.telegraphDuration) {
                    this.aiState = 'attacking';
                    this.stateTimer = 0;
                }
                break;

            case 'attacking':
                // Execute attack
                this.executeAttack(this.nextAttack);
                this.aiState = 'recovery';
                this.stateTimer = 0;
                break;

            case 'recovery':
                // Recovery period after attack
                if (this.stateTimer >= this.nextAttack.recovery) {
                    this.aiState = 'idle';
                    this.stateTimer = 0;
                }
                break;

            case 'stunned':
                // Poise broken, vulnerable
                if (this.stateTimer >= 3.0) {
                    this.aiState = 'idle';
                    this.stateTimer = 0;
                    this.poise = this.maxPoise;
                }
                break;

            case 'riposte_vulnerable':
                // Waiting for riposte or timeout
                if (this.stateTimer >= 2.0) {
                    this.aiState = 'idle';
                    this.stateTimer = 0;
                }
                break;

            case 'riposted':
                // Being riposted, locked in animation
                // Will be reset by combat system
                break;
        }
    }

    chooseNextAttack(player, distance) {
        const availableAttacks = this.getAvailableAttacks(distance);

        if (availableAttacks.length === 0) {
            // No attacks in range, move closer
            this.moveToward(player);
            return;
        }

        // Weight attacks based on player behavior
        const weights = availableAttacks.map(attack => {
            let weight = attack.baseWeight || 1;

            // Punish player patterns
            if (player.combat.state === 'blocking' && attack.guardBreak) {
                weight *= 3;
            }

            if (player.recentDodges > 2 && attack.rollCatch) {
                weight *= 2;
            }

            if (distance < 30 && attack.type === 'aoe') {
                weight *= 2;
            }

            return weight;
        });

        // Weighted random selection
        this.nextAttack = this.weightedRandom(availableAttacks, weights);
    }

    getAvailableAttacks(distance) {
        const phase = this.currentPhase;
        const moves = this.attackPattern[`phase${phase}Moves`] || [];

        return moves.filter(move =>
            distance >= (move.minRange || 0) &&
            distance <= (move.maxRange || 999)
        );
    }

    weightedRandom(items, weights) {
        const totalWeight = weights.reduce((a, b) => a + b, 0);
        let random = Math.random() * totalWeight;

        for (let i = 0; i < items.length; i++) {
            random -= weights[i];
            if (random <= 0) {
                return items[i];
            }
        }

        return items[0];
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
            case 'cone':
                this.coneAttack(attack);
                break;
            case 'projectile':
                this.projectileAttack(attack);
                break;
        }

        this.game.audio.playSFX(attack.sound || 'boss_attack');
    }

    meleeAttack(attack) {
        const hitbox = {
            x: this.x,
            y: this.y,
            range: attack.range || 30,
            arc: attack.arc || 90,
            direction: this.facing,
            damage: attack.damage
        };

        if (this.checkPlayerInHitbox(hitbox)) {
            this.hitPlayer(attack.damage);
        }
    }

    aoeAttack(attack) {
        const player = this.game.player;
        const distance = this.distanceTo(player);

        if (distance <= attack.range) {
            // Player in AoE
            this.hitPlayer(attack.damage);
        }

        // Visual effect
        this.createAoEEffect(attack.range);
    }

    chargeAttack(attack) {
        // Charge toward player
        const player = this.game.player;
        const dx = player.x - this.x;
        const dy = player.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        const speed = attack.speed || 300;
        const duration = attack.duration || 1.0;

        this.chargeVelocity = {
            x: (dx / dist) * speed,
            y: (dy / dist) * speed
        };

        // Move during charge
        const chargeInterval = setInterval(() => {
            this.x += this.chargeVelocity.x * 0.016;
            this.y += this.chargeVelocity.y * 0.016;

            // Check collision with player
            if (this.distanceTo(player) < 20) {
                this.hitPlayer(attack.damage);
                clearInterval(chargeInterval);
                this.chargeVelocity = null;
            }
        }, 16);

        setTimeout(() => {
            clearInterval(chargeInterval);
            this.chargeVelocity = null;
        }, duration * 1000);
    }

    checkPlayerInHitbox(hitbox) {
        const player = this.game.player;
        const dx = player.x - hitbox.x;
        const dy = player.y - hitbox.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance > hitbox.range) return false;

        const angle = Math.atan2(dy, dx) * 180 / Math.PI;
        const facingAngle = this.directionToAngle(hitbox.direction);
        let angleDiff = Math.abs(angle - facingAngle);

        if (angleDiff > 180) angleDiff = 360 - angleDiff;

        return angleDiff <= hitbox.arc / 2;
    }

    hitPlayer(damage) {
        const player = this.game.player;

        // Check I-frames
        if (player.combat.iframes > 0) {
            this.game.showText('DODGED!');
            return;
        }

        // Check block
        if (player.combat.state === 'blocking') {
            const blockedDamage = damage * 0.3; // Block reduces damage by 70%
            player.takeDamage(blockedDamage);

            // Drain stamina
            player.combat.stamina -= damage * 0.5;
            if (player.combat.stamina <= 0) {
                player.combat.staminaBreak();
            }

            this.game.audio.playSFX('block');
            return;
        }

        // Full damage
        player.takeDamage(damage);
        this.game.audio.playSFX('player_hit');
        this.game.camera.shake(5);
    }

    takeDamage(amount, poiseBreak = 10, isCritical = false) {
        this.hp -= amount;
        this.poise -= poiseBreak;

        // Create damage effect
        this.createDamageEffect();

        // Check poise break
        if (this.poise <= 0 && this.aiState !== 'stunned') {
            this.aiState = 'stunned';
            this.stateTimer = 0;
            this.game.showText(`${this.name}'s poise broken!`);
            this.game.audio.playSFX('poise_break');
        }

        // Check death
        if (this.hp <= 0) {
            this.onDeath();
            return true;
        }

        return false;
    }

    enterPhase2() {
        this.currentPhase = 2;
        this.poise = this.maxPoise;

        // Heal 25%
        this.hp = Math.min(this.maxHp, this.hp + this.maxHp * 0.25);

        // Play transition
        this.game.showText(`${this.name} enters phase 2!`);
        this.game.audio.playSFX('phase_transition');

        // Invulnerable during transition
        this.aiState = 'transition';
        setTimeout(() => {
            this.aiState = 'idle';
        }, 2000);
    }

    enterPhase3() {
        this.currentPhase = 3;
        this.poise = this.maxPoise * 1.5;

        this.game.showText(`${this.name} unleashes true power!`);
        this.game.audio.playSFX('phase_transition_final');

        // Activate unique mechanic
        if (this.uniqueMechanic && this.uniqueMechanic.activate) {
            this.uniqueMechanic.activate.call(this);
        }

        this.aiState = 'transition';
        setTimeout(() => {
            this.aiState = 'idle';
        }, 3000);
    }

    onDeath() {
        this.isDead = true;
        this.game.audio.playSFX('boss_death');
        this.game.audio.stopMusic();

        // Victory screen
        this.game.showVictoryScreen(this.name);

        // Award souls
        const souls = this.maxHp * 5;
        this.game.player.gainSouls(souls);

        // Drop loot
        this.dropLoot();
    }

    dropLoot() {
        // Boss-specific drops
        const loot = {
            gold: Math.floor(this.maxHp * 2),
            items: ['boss_soul_' + this.id],
            equipment: this.rollEquipmentDrop()
        };

        this.game.showLootScreen(loot);
    }

    showTelegraph(attack) {
        // Store telegraph data for renderer
        this.currentTelegraph = {
            type: attack.type,
            progress: this.stateTimer / attack.telegraphDuration,
            attack: attack
        };
    }

    render(ctx, camera) {
        if (this.isDead) return;

        const screenX = this.x - camera.x;
        const screenY = this.y - camera.y;

        // Render telegraph
        if (this.currentTelegraph) {
            this.renderTelegraph(ctx, screenX, screenY);
        }

        // Render boss sprite
        ctx.save();

        // Flash when hit
        if (this.hitFlash) {
            ctx.globalAlpha = 0.5;
        }

        // Boss sprite (placeholder)
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(screenX - 20, screenY - 40, 40, 40);

        ctx.restore();

        // Render HP bar
        this.renderHealthBar(ctx, screenX, screenY);

        // Render lock-on indicator
        if (this.isLockedOn) {
            this.renderLockOnIndicator(ctx, screenX, screenY);
        }
    }

    renderTelegraph(ctx, x, y) {
        const telegraph = this.currentTelegraph;
        const progress = telegraph.progress;

        // Color progression: yellow -> orange -> red
        let color;
        if (progress < 0.5) {
            color = `rgba(255, 255, 0, ${0.3 + progress * 0.4})`;
        } else if (progress < 0.8) {
            color = `rgba(255, 165, 0, ${0.3 + progress * 0.4})`;
        } else {
            color = `rgba(255, 0, 0, ${0.3 + progress * 0.4})`;
        }

        ctx.save();
        ctx.fillStyle = color;
        ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        ctx.lineWidth = 2;

        switch(telegraph.type) {
            case 'aoe':
                const radius = telegraph.attack.range * progress;
                ctx.beginPath();
                ctx.arc(x, y, radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                break;

            case 'cone':
                const arc = telegraph.attack.arc * Math.PI / 180;
                const angle = this.directionToAngle(this.facing) * Math.PI / 180;

                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.arc(x, y, telegraph.attack.range, angle - arc/2, angle + arc/2);
                ctx.closePath();
                ctx.fill();
                break;

            case 'melee':
                // Show weapon glow
                ctx.fillStyle = color;
                ctx.fillRect(x - 10, y - 50, 20, 10);
                break;
        }

        ctx.restore();
    }

    renderHealthBar(ctx, x, y) {
        const barWidth = 80;
        const barHeight = 8;
        const hpPercent = this.hp / this.maxHp;

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(x - barWidth/2 - 2, y - 60, barWidth + 4, barHeight + 4);

        // HP bar
        ctx.fillStyle = hpPercent > 0.5 ? '#4ade80' : hpPercent > 0.25 ? '#fbbf24' : '#ef4444';
        ctx.fillRect(x - barWidth/2, y - 58, barWidth * hpPercent, barHeight);

        // Border
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.strokeRect(x - barWidth/2, y - 58, barWidth, barHeight);

        // Boss name
        ctx.fillStyle = '#fff';
        ctx.font = '8px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(this.name, x, y - 65);
    }

    distanceTo(target) {
        const dx = target.x - this.x;
        const dy = target.y - this.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    faceTarget(target) {
        const dx = target.x - this.x;
        const dy = target.y - this.y;

        if (Math.abs(dx) > Math.abs(dy)) {
            this.facing = dx > 0 ? 'right' : 'left';
        } else {
            this.facing = dy > 0 ? 'down' : 'up';
        }
    }

    directionToAngle(direction) {
        const angles = { up: -90, down: 90, left: 180, right: 0 };
        return angles[direction] || 0;
    }
}

// Example Boss Data: Hogger
const BOSS_HOGGER = {
    name: 'Hogger the Ravager',
    hp: 500,
    poise: 80,
    phases: 2,
    x: 200,
    y: 200,

    attackPattern: {
        phase1Moves: [
            {
                id: 'claw_swipe',
                type: 'melee',
                damage: 25,
                range: 30,
                arc: 90,
                minRange: 0,
                maxRange: 35,
                telegraphDuration: 0.4,
                recovery: 0.8,
                baseWeight: 10
            },
            {
                id: 'leap',
                type: 'charge',
                damage: 35,
                speed: 200,
                duration: 0.8,
                minRange: 40,
                maxRange: 100,
                telegraphDuration: 0.6,
                recovery: 1.2,
                baseWeight: 7,
                rollCatch: true
            },
            {
                id: 'howl',
                type: 'buff',
                minRange: 0,
                maxRange: 999,
                telegraphDuration: 1.0,
                recovery: 0.5,
                baseWeight: 3
            }
        ],

        phase2Moves: [
            {
                id: 'ground_slam',
                type: 'aoe',
                damage: 40,
                range: 60,
                minRange: 0,
                maxRange: 999,
                telegraphDuration: 0.8,
                recovery: 1.5,
                baseWeight: 8
            },
            {
                id: 'triple_swipe',
                type: 'combo',
                damage: [20, 20, 35],
                range: 30,
                arc: 90,
                minRange: 0,
                maxRange: 35,
                telegraphDuration: 0.3,
                recovery: 2.0,
                baseWeight: 6,
                guardBreak: true
            }
        ]
    },

    uniqueMechanic: {
        type: 'summon_adds',
        trigger: 0.5,
        activate: function() {
            // Spawn minions at 50% HP
            this.game.spawnEnemy('gnoll_minion', this.x - 50, this.y);
            this.game.spawnEnemy('gnoll_minion', this.x + 50, this.y);
        }
    }
};

// =============================================================================
// 3. DEATH & SOUL SYSTEM
// =============================================================================

class DeathSystem {
    constructor(game) {
        this.game = game;
        this.deathCount = 0;
        this.soulStash = {
            experience: 0,
            gold: 0,
            position: null,
            active: false
        };
    }

    onPlayerDeath() {
        this.deathCount++;

        // Calculate soul loss
        const expLoss = Math.floor(this.game.player.experience * 0.5);
        const goldLoss = Math.floor(this.game.player.gold * 0.3);

        // Check if player already has active souls
        if (this.soulStash.active) {
            // Lost previous souls!
            this.game.showText('Your previous souls are lost forever...');
        }

        // Create new soul stash
        this.soulStash = {
            experience: expLoss,
            gold: goldLoss,
            position: {
                x: this.game.player.x,
                y: this.game.player.y,
                area: this.game.currentArea
            },
            active: true
        };

        // Deduct from player
        this.game.player.experience -= expLoss;
        this.game.player.gold -= goldLoss;

        // Show death screen
        this.showDeathScreen();

        // Respawn after delay
        setTimeout(() => {
            this.respawnPlayer();
        }, 3000);

        this.game.audio.playSFX('death');
        this.game.audio.stopMusic();
    }

    respawnPlayer() {
        const bonfire = this.game.lastBonfireUsed || this.game.startingBonfire;

        // Full heal
        this.game.player.hp = this.game.player.maxHp;
        this.game.player.combat.stamina = this.game.player.combat.maxStamina;
        this.game.player.estusCharges = this.game.player.maxEstusCharges;

        // Teleport to bonfire
        this.game.player.x = bonfire.x;
        this.game.player.y = bonfire.y;
        this.game.currentArea = bonfire.area;

        // Respawn enemies
        this.respawnEnemies();

        // Hide death screen
        this.hideDeathScreen();

        // Resume music
        this.game.audio.playMusic('overworld');
    }

    respawnEnemies() {
        // Remove all non-boss enemies
        this.game.enemies = this.game.enemies.filter(e => e.isBoss && !e.isDead);

        // Respawn area enemies
        this.game.spawnAreaEnemies(this.game.currentArea);
    }

    checkSoulRecovery() {
        if (!this.soulStash.active) return;

        const player = this.game.player;
        const dx = player.x - this.soulStash.position.x;
        const dy = player.y - this.soulStash.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 20 && this.game.currentArea === this.soulStash.position.area) {
            // RECOVER SOULS!
            player.experience += this.soulStash.experience;
            player.gold += this.soulStash.gold;

            this.game.showText(`Souls recovered! +${this.soulStash.experience} EXP`);
            this.game.audio.playSFX('soul_recovery');

            // Particle effect
            this.createSoulRecoveryEffect();

            this.soulStash.active = false;
        }
    }

    render(ctx, camera) {
        if (!this.soulStash.active) return;
        if (this.game.currentArea !== this.soulStash.position.area) return;

        const screenX = this.soulStash.position.x - camera.x;
        const screenY = this.soulStash.position.y - camera.y;

        // Pulsing blood stain
        const pulse = Math.sin(Date.now() / 500) * 0.3 + 0.7;

        ctx.save();
        ctx.globalAlpha = pulse;

        // Outer glow
        ctx.fillStyle = 'rgba(139, 0, 0, 0.5)';
        ctx.beginPath();
        ctx.arc(screenX, screenY, 12, 0, Math.PI * 2);
        ctx.fill();

        // Inner stain
        ctx.fillStyle = '#8b0000';
        ctx.beginPath();
        ctx.arc(screenX, screenY, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        // Soul count
        ctx.fillStyle = '#fff';
        ctx.font = '8px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(this.soulStash.experience.toString(), screenX, screenY - 15);
    }

    showDeathScreen() {
        const overlay = document.createElement('div');
        overlay.id = 'deathOverlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 1s;
        `;

        const deathText = document.createElement('div');
        deathText.textContent = 'YOU DIED';
        deathText.style.cssText = `
            color: #8b0000;
            font-size: 72px;
            font-family: 'Press Start 2P', monospace;
            text-shadow: 0 0 20px rgba(139, 0, 0, 0.8);
        `;

        const deathCount = document.createElement('div');
        deathCount.textContent = `Deaths: ${this.deathCount}`;
        deathCount.style.cssText = `
            color: #fff;
            font-size: 16px;
            font-family: monospace;
            margin-top: 20px;
        `;

        overlay.appendChild(deathText);
        overlay.appendChild(deathCount);
        document.body.appendChild(overlay);

        // Fade in
        setTimeout(() => overlay.style.opacity = '1', 100);
    }

    hideDeathScreen() {
        const overlay = document.getElementById('deathOverlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 1000);
        }
    }

    createSoulRecoveryEffect() {
        for (let i = 0; i < 20; i++) {
            this.game.particles.spawn({
                x: this.soulStash.position.x,
                y: this.soulStash.position.y,
                vx: (Math.random() - 0.5) * 5,
                vy: (Math.random() - 0.5) * 5 - 3,
                life: 1.0,
                decay: 0.02,
                size: Math.random() * 4 + 2,
                color: '#00f2fe'
            });
        }
    }
}

// =============================================================================
// 4. INPUT SYSTEM
// =============================================================================

class InputManager {
    constructor(game) {
        this.game = game;
        this.keys = {};
        this.gamepad = null;

        this.setupKeyboard();
        this.setupGamepad();
    }

    setupKeyboard() {
        window.addEventListener('keydown', (e) => {
            this.keys[e.key.toLowerCase()] = true;
            this.handleInput(e.key.toLowerCase(), true);
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.key.toLowerCase()] = false;
            this.handleInput(e.key.toLowerCase(), false);
        });
    }

    setupGamepad() {
        window.addEventListener('gamepadconnected', (e) => {
            this.gamepad = e.gamepad;
            console.log('Gamepad connected:', e.gamepad.id);
        });

        window.addEventListener('gamepaddisconnected', () => {
            this.gamepad = null;
        });
    }

    update() {
        // Update gamepad state
        if (this.gamepad) {
            const gamepads = navigator.getGamepads();
            this.gamepad = gamepads[this.gamepad.index];

            if (this.gamepad) {
                this.handleGamepadInput();
            }
        }
    }

    handleInput(key, pressed) {
        const combat = this.game.player.combat;

        switch(key) {
            case 'x':
            case 'j':
                if (pressed) combat.lightAttack();
                break;
            case 'c':
            case 'k':
                if (pressed) combat.heavyAttack();
                break;
            case 'space':
            case 'l':
                if (pressed) combat.dodge();
                break;
            case 'shift':
                combat.block(pressed);
                break;
            case 'q':
                if (pressed) combat.toggleLockOn();
                break;
            case 'e':
                if (pressed && combat.lockOn && combat.lockOn.state === 'riposte_vulnerable') {
                    combat.riposte();
                }
                break;
        }
    }

    handleGamepadInput() {
        const gp = this.gamepad;
        const combat = this.game.player.combat;

        // Buttons
        if (gp.buttons[0].pressed) { // A/X - Light Attack
            combat.lightAttack();
        }
        if (gp.buttons[1].pressed) { // B/Circle - Dodge
            combat.dodge();
        }
        if (gp.buttons[2].pressed) { // X/Square - Heavy Attack
            combat.heavyAttack();
        }
        if (gp.buttons[3].pressed) { // Y/Triangle - Riposte
            if (combat.lockOn && combat.lockOn.state === 'riposte_vulnerable') {
                combat.riposte();
            }
        }

        // Triggers
        if (gp.buttons[6].pressed) { // LT - Block
            combat.block(true);
        } else {
            combat.block(false);
        }

        if (gp.buttons[7].pressed) { // RT - Lock On
            combat.toggleLockOn();
        }

        // Left stick for movement
        const moveX = gp.axes[0];
        const moveY = gp.axes[1];

        if (Math.abs(moveX) > 0.2 || Math.abs(moveY) > 0.2) {
            this.game.player.move(moveX, moveY);
        }
    }

    getMovementVector() {
        let x = 0;
        let y = 0;

        // Keyboard
        if (this.keys['w'] || this.keys['arrowup']) y -= 1;
        if (this.keys['s'] || this.keys['arrowdown']) y += 1;
        if (this.keys['a'] || this.keys['arrowleft']) x -= 1;
        if (this.keys['d'] || this.keys['arrowright']) x += 1;

        // Gamepad
        if (this.gamepad) {
            const gpX = this.gamepad.axes[0];
            const gpY = this.gamepad.axes[1];

            if (Math.abs(gpX) > 0.2) x = gpX;
            if (Math.abs(gpY) > 0.2) y = gpY;
        }

        // Normalize
        const length = Math.sqrt(x * x + y * y);
        if (length > 0) {
            return { x: x / length, y: y / length };
        }

        return null;
    }
}

// =============================================================================
// Export for use in wowMon.html
// =============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ActionCombatSystem,
        BossEnemy,
        DeathSystem,
        InputManager,
        BOSS_HOGGER
    };
}
