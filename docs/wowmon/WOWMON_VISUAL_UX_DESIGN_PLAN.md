# WoWMon Visual/UX Design & Battle Animation System
## Comprehensive Visual Enhancement Plan

---

## Executive Summary

This document outlines a complete visual overhaul for WoWMon, focusing on battle animations, particle effects, UI/UX polish, and visual feedback. The plan transforms static text-based battles into dynamic, visually exciting encounters with satisfying animations and effects.

**Current State:**
- Modern gradient UI with animated backgrounds
- Static text-based battle system
- Basic creature rendering (simple rectangles)
- Minimal visual feedback during attacks
- HP bars with smooth transitions

**Goal:**
- Cinema-quality battle animations
- 50+ unique move animation designs
- Particle effect library
- Creature idle/attack animation system
- Dynamic camera effects
- Rich visual feedback for all battle events

---

## 1. Battle Animation Framework

### 1.1 Core Animation System

```javascript
class BattleAnimationEngine {
    constructor(game) {
        this.game = game;
        this.ctx = game.ctx;
        this.activeAnimations = [];
        this.particles = [];
        this.screenShake = { x: 0, y: 0, intensity: 0, duration: 0 };
        this.flashEffect = { color: null, opacity: 0, duration: 0 };
        this.damageNumbers = [];
        this.statusIcons = [];
    }

    // Animation queue system for chaining effects
    queueAnimation(animation) {
        return new Promise((resolve) => {
            this.activeAnimations.push({
                ...animation,
                onComplete: resolve
            });
        });
    }

    // Main animation loop (called each frame)
    update(deltaTime) {
        this.updateParticles(deltaTime);
        this.updateAnimations(deltaTime);
        this.updateScreenShake(deltaTime);
        this.updateFlashEffects(deltaTime);
        this.updateDamageNumbers(deltaTime);
        this.render();
    }

    // Particle system
    createParticle(config) {
        this.particles.push({
            x: config.x,
            y: config.y,
            vx: config.vx || 0,
            vy: config.vy || 0,
            ax: config.ax || 0,
            ay: config.ay || 0.1, // gravity
            size: config.size || 2,
            color: config.color || '#fff',
            life: config.life || 1.0,
            decay: config.decay || 0.02,
            type: config.type || 'circle',
            rotation: config.rotation || 0,
            rotationSpeed: config.rotationSpeed || 0
        });
    }

    // Screen shake effect
    shake(intensity = 5, duration = 300) {
        this.screenShake = { x: 0, y: 0, intensity, duration };
    }

    // Flash effect (for super effective, critical hits, etc.)
    flash(color = '#ffffff', opacity = 0.5, duration = 200) {
        this.flashEffect = { color, opacity, duration, initialOpacity: opacity };
    }

    // Damage numbers
    showDamageNumber(x, y, damage, isCritical = false, effectiveness = 1.0) {
        let color = '#ffffff';
        let scale = 1.0;
        let text = damage.toString();

        if (isCritical) {
            color = '#ffff00'; // Yellow for critical
            scale = 1.5;
            text = `${damage}!`;
        } else if (effectiveness > 1.5) {
            color = '#4ade80'; // Green for super effective
            scale = 1.3;
        } else if (effectiveness < 0.75) {
            color = '#94a3b8'; // Gray for not very effective
            scale = 0.8;
        }

        this.damageNumbers.push({
            x, y,
            text,
            color,
            scale,
            life: 1.0,
            vy: -1, // Float upward
            decay: 0.02
        });
    }
}
```

### 1.2 Creature Animation States

```javascript
class CreatureAnimator {
    constructor(creature, position) {
        this.creature = creature;
        this.position = position; // {x, y}
        this.state = 'idle';
        this.frame = 0;
        this.timer = 0;

        // Animation states
        this.animations = {
            idle: { frames: 2, speed: 500, loop: true },
            attack: { frames: 4, speed: 100, loop: false },
            hurt: { frames: 2, speed: 100, loop: false },
            faint: { frames: 6, speed: 150, loop: false },
            victory: { frames: 4, speed: 200, loop: true }
        };
    }

    playAnimation(state) {
        this.state = state;
        this.frame = 0;
        this.timer = 0;
    }

    update(deltaTime) {
        const anim = this.animations[this.state];
        this.timer += deltaTime;

        if (this.timer >= anim.speed) {
            this.timer = 0;
            this.frame++;

            if (this.frame >= anim.frames) {
                if (anim.loop) {
                    this.frame = 0;
                } else {
                    this.frame = anim.frames - 1;
                    this.state = 'idle';
                }
            }
        }
    }

    render(ctx) {
        const offset = this.getAnimationOffset();
        const scale = this.getAnimationScale();

        // Apply transformations
        ctx.save();
        ctx.translate(this.position.x + offset.x, this.position.y + offset.y);
        ctx.scale(scale.x, scale.y);

        // Draw creature sprite (enhanced from simple rectangle)
        this.renderCreatureSprite(ctx);

        ctx.restore();
    }

    getAnimationOffset() {
        switch(this.state) {
            case 'idle':
                return { x: 0, y: Math.sin(this.frame * 0.5) * 2 }; // Bobbing
            case 'attack':
                return { x: Math.sin(this.frame * 2) * 10, y: 0 }; // Lunge
            case 'hurt':
                return { x: Math.sin(this.frame * 5) * 3, y: 0 }; // Recoil
            default:
                return { x: 0, y: 0 };
        }
    }

    getAnimationScale() {
        switch(this.state) {
            case 'attack':
                return { x: 1 + (this.frame / 10), y: 1 + (this.frame / 10) }; // Grow
            case 'hurt':
                return { x: 0.9, y: 0.9 }; // Shrink
            default:
                return { x: 1, y: 1 };
        }
    }
}
```

---

## 2. Move Animation Designs (50+ Moves)

### 2.1 Physical Attack Animations

#### TACKLE / QUICK ATTACK
```javascript
animateTackle(attacker, defender) {
    const anim = this.animEngine;

    // 1. Attacker rushes forward
    await anim.queueAnimation({
        type: 'slide',
        target: attacker,
        to: { x: defender.x - 20, y: defender.y },
        duration: 200,
        easing: 'easeOutQuad'
    });

    // 2. Impact effect
    anim.shake(4, 200);
    for (let i = 0; i < 8; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: (Math.random() - 0.5) * 3,
            vy: (Math.random() - 0.5) * 3,
            color: '#ffffff',
            size: 3,
            life: 0.5
        });
    }

    // 3. Defender recoils
    defender.playAnimation('hurt');

    // 4. Attacker returns
    await anim.queueAnimation({
        type: 'slide',
        target: attacker,
        to: { x: attacker.originalX, y: attacker.originalY },
        duration: 200,
        easing: 'easeInQuad'
    });
}
```

#### SLASH / CRUNCH
```javascript
animateSlash(attacker, defender) {
    const anim = this.animEngine;

    // 1. Wind-up
    attacker.playAnimation('attack');
    await anim.wait(100);

    // 2. Slash arc effect
    const slashPath = this.createArcPath(
        defender.x - 20,
        defender.y - 20,
        defender.x + 20,
        defender.y + 20,
        8 // segments
    );

    await anim.queueAnimation({
        type: 'slash',
        path: slashPath,
        color: '#e0e0e0',
        width: 4,
        duration: 150
    });

    // 3. Impact particles
    anim.shake(6, 200);
    for (let i = 0; i < 12; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: Math.cos(i / 12 * Math.PI * 2) * 4,
            vy: Math.sin(i / 12 * Math.PI * 2) * 4,
            color: i % 2 ? '#ffff00' : '#ff0000',
            size: 2,
            life: 0.6
        });
    }

    defender.playAnimation('hurt');
}
```

#### EARTHQUAKE
```javascript
animateEarthquake(attacker, defender) {
    const anim = this.animEngine;

    // 1. Charge up (ground glowing)
    await anim.queueAnimation({
        type: 'radialPulse',
        x: attacker.x,
        y: attacker.y + 20,
        maxRadius: 40,
        color: '#8b4513',
        duration: 500
    });

    // 2. Massive screen shake
    anim.shake(12, 1000);

    // 3. Ground cracks spreading
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: Math.random() * this.canvas.width,
                y: this.canvas.height * 0.7 + Math.random() * 40,
                vx: (Math.random() - 0.5) * 2,
                vy: -Math.random() * 3,
                color: '#654321',
                size: 4,
                type: 'square',
                life: 1.0
            });
        }, i * 50);
    }

    // 4. Both creatures shake
    defender.playAnimation('hurt');
}
```

### 2.2 Fire Type Animations

#### EMBER / FIREBOLT
```javascript
animateEmber(attacker, defender) {
    const anim = this.animEngine;

    // 1. Fire charging
    attacker.playAnimation('attack');
    for (let i = 0; i < 15; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 20,
            y: attacker.y + (Math.random() - 0.5) * 20,
            vx: 0,
            vy: -1,
            color: i % 2 ? '#ff4500' : '#ffa500',
            size: 2,
            life: 0.5
        });
    }

    await anim.wait(300);

    // 2. Fireball projectile
    await anim.queueAnimation({
        type: 'projectile',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        particle: {
            color: '#ff4500',
            size: 6,
            trail: true,
            trailLength: 10,
            trailColor: '#ffa500'
        },
        duration: 400
    });

    // 3. Explosion on impact
    anim.shake(5, 200);
    anim.flash('#ff4500', 0.4, 150);
    for (let i = 0; i < 20; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: Math.cos(i / 20 * Math.PI * 2) * 3,
            vy: Math.sin(i / 20 * Math.PI * 2) * 3,
            color: ['#ff0000', '#ff4500', '#ffa500', '#ffff00'][Math.floor(Math.random() * 4)],
            size: 3,
            life: 0.8
        });
    }

    defender.playAnimation('hurt');
}
```

#### INFERNO / METEOR STRIKE
```javascript
animateInferno(attacker, defender) {
    const anim = this.animEngine;

    // 1. Sky darkens
    anim.flash('#000000', 0.5, 500);
    await anim.wait(500);

    // 2. Multiple meteors fall
    for (let i = 0; i < 5; i++) {
        setTimeout(async () => {
            const startX = Math.random() * this.canvas.width;
            await anim.queueAnimation({
                type: 'projectile',
                from: { x: startX, y: -20 },
                to: { x: defender.x + (Math.random() - 0.5) * 40, y: defender.y },
                particle: {
                    color: '#ff0000',
                    size: 8,
                    trail: true,
                    trailColor: '#ff4500'
                },
                duration: 500
            });

            // Explosion per meteor
            anim.shake(8, 200);
            for (let j = 0; j < 15; j++) {
                anim.createParticle({
                    x: defender.x,
                    y: defender.y,
                    vx: (Math.random() - 0.5) * 5,
                    vy: -Math.random() * 4,
                    color: ['#ff0000', '#ffa500', '#ffff00'][Math.floor(Math.random() * 3)],
                    size: 4,
                    life: 1.0
                });
            }
        }, i * 200);
    }

    defender.playAnimation('hurt');
}
```

#### FLAME STRIKE / SACRED FIRE
```javascript
animateFlameStrike(attacker, defender) {
    const anim = this.animEngine;

    // 1. Pillar of light charges
    await anim.queueAnimation({
        type: 'beam',
        from: { x: defender.x, y: -20 },
        to: { x: defender.x, y: defender.y },
        color: '#ffff00',
        width: 3,
        glow: true,
        duration: 300
    });

    // 2. Fire erupts from ground
    for (let i = 0; i < 30; i++) {
        anim.createParticle({
            x: defender.x + (Math.random() - 0.5) * 30,
            y: defender.y + 20,
            vx: (Math.random() - 0.5) * 2,
            vy: -Math.random() * 6 - 4,
            color: ['#ff0000', '#ff4500', '#ffa500', '#ffff00'][Math.floor(Math.random() * 4)],
            size: 3,
            life: 1.2
        });
    }

    // 3. Sustained damage effect
    anim.shake(7, 800);
    anim.flash('#ff4500', 0.5, 600);
    defender.playAnimation('hurt');
}
```

### 2.3 Water Type Animations

#### BUBBLE / WATER GUN
```javascript
animateWaterGun(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // Stream of water bubbles
    for (let i = 0; i < 10; i++) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'projectile',
                from: { x: attacker.x, y: attacker.y },
                to: { x: defender.x + (Math.random() - 0.5) * 20, y: defender.y },
                particle: {
                    color: '#00bfff',
                    size: 4,
                    alpha: 0.7
                },
                duration: 300
            });

            // Splash on impact
            setTimeout(() => {
                for (let j = 0; j < 5; j++) {
                    anim.createParticle({
                        x: defender.x,
                        y: defender.y,
                        vx: (Math.random() - 0.5) * 3,
                        vy: (Math.random() - 0.5) * 3,
                        color: '#87ceeb',
                        size: 2,
                        life: 0.4
                    });
                }
            }, 300);
        }, i * 100);
    }

    anim.shake(3, 500);
    defender.playAnimation('hurt');
}
```

#### HYDRO PUMP / TIDAL WAVE
```javascript
animateHydroPump(attacker, defender) {
    const anim = this.animEngine;

    // 1. Water builds up
    for (let i = 0; i < 20; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 30,
            y: attacker.y + (Math.random() - 0.5) * 30,
            vx: (defender.x - attacker.x) * 0.01,
            vy: (defender.y - attacker.y) * 0.01,
            color: '#0080ff',
            size: 3,
            life: 0.8,
            alpha: 0.8
        });
    }

    await anim.wait(400);

    // 2. Massive water beam
    await anim.queueAnimation({
        type: 'beam',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        color: '#0080ff',
        width: 20,
        glow: true,
        duration: 600,
        particles: true
    });

    // 3. Crushing impact
    anim.shake(10, 400);
    anim.flash('#0080ff', 0.4, 300);

    for (let i = 0; i < 40; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6,
            color: '#87ceeb',
            size: 4,
            life: 1.0,
            alpha: 0.7
        });
    }

    defender.playAnimation('hurt');
}
```

#### WATER PULSE / SCALD
```javascript
animateWaterPulse(attacker, defender) {
    const anim = this.animEngine;

    // 1. Water sphere forms
    attacker.playAnimation('attack');
    await anim.queueAnimation({
        type: 'orbit',
        center: { x: attacker.x, y: attacker.y },
        radius: 20,
        particles: 12,
        color: '#00bfff',
        duration: 400
    });

    // 2. Sphere travels as rippling wave
    await anim.queueAnimation({
        type: 'projectile',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        particle: {
            color: '#0080ff',
            size: 10,
            ripple: true,
            alpha: 0.6
        },
        duration: 400
    });

    // 3. Concentric wave burst
    for (let r = 10; r <= 50; r += 10) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'ring',
                x: defender.x,
                y: defender.y,
                radius: r,
                color: '#00bfff',
                width: 2,
                duration: 200,
                fadeOut: true
            });
        }, (r - 10) * 20);
    }

    anim.shake(4, 300);
    defender.playAnimation('hurt');
}
```

### 2.4 Electric Type Animations

#### SPARK / THUNDER WAVE
```javascript
animateThunderWave(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Electric charge builds
    for (let i = 0; i < 15; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 25,
            y: attacker.y + (Math.random() - 0.5) * 25,
            vx: 0,
            vy: 0,
            color: '#ffff00',
            size: 2,
            life: 0.3
        });
    }

    await anim.wait(300);

    // 2. Lightning bolt strikes
    const lightningPoints = this.generateLightningPath(
        { x: attacker.x, y: attacker.y },
        { x: defender.x, y: defender.y },
        10 // segments
    );

    await anim.queueAnimation({
        type: 'lightning',
        points: lightningPoints,
        color: '#ffff00',
        width: 3,
        flicker: true,
        duration: 200
    });

    // 3. Electric sparks on impact
    anim.flash('#ffff00', 0.5, 150);
    for (let i = 0; i < 20; i++) {
        anim.createParticle({
            x: defender.x + (Math.random() - 0.5) * 30,
            y: defender.y + (Math.random() - 0.5) * 30,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            color: '#ffff00',
            size: 2,
            life: 0.5
        });
    }

    defender.playAnimation('hurt');
}
```

#### LIGHTNING BOLT / DISCHARGE
```javascript
animateLightningBolt(attacker, defender) {
    const anim = this.animEngine;

    // 1. Storm clouds gather
    anim.flash('#404040', 0.6, 300);

    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            // Multiple lightning strikes
            const startX = defender.x + (Math.random() - 0.5) * 40;
            const lightningPath = this.generateLightningPath(
                { x: startX, y: -10 },
                { x: defender.x, y: defender.y },
                15
            );

            anim.queueAnimation({
                type: 'lightning',
                points: lightningPath,
                color: '#ffff00',
                width: 4,
                glow: true,
                duration: 100
            });

            anim.flash('#ffffff', 0.8, 50);
            anim.shake(6, 100);

            // Electric sparks
            for (let j = 0; j < 15; j++) {
                anim.createParticle({
                    x: defender.x,
                    y: defender.y,
                    vx: (Math.random() - 0.5) * 5,
                    vy: (Math.random() - 0.5) * 5,
                    color: '#ffff00',
                    size: 3,
                    life: 0.6
                });
            }
        }, i * 150);
    }

    defender.playAnimation('hurt');
}
```

### 2.5 Nature/Grass Type Animations

#### VINE WHIP / MAGICAL LEAF
```javascript
animateVineWhip(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Vine grows and extends
    const vineSegments = 10;
    for (let i = 0; i < vineSegments; i++) {
        setTimeout(() => {
            const t = i / vineSegments;
            const x = attacker.x + (defender.x - attacker.x) * t;
            const y = attacker.y + (defender.y - attacker.y) * t + Math.sin(t * Math.PI * 2) * 10;

            anim.createParticle({
                x, y,
                vx: 0, vy: 0,
                color: '#228b22',
                size: 3,
                life: 0.8,
                type: 'square'
            });

            // Leaves along vine
            if (i % 2 === 0) {
                anim.createParticle({
                    x: x + (Math.random() - 0.5) * 5,
                    y: y + (Math.random() - 0.5) * 5,
                    vx: 0, vy: 0.5,
                    color: '#32cd32',
                    size: 2,
                    life: 0.6
                });
            }
        }, i * 40);
    }

    // 2. Whip snaps
    setTimeout(() => {
        anim.shake(5, 200);
        defender.playAnimation('hurt');

        for (let i = 0; i < 10; i++) {
            anim.createParticle({
                x: defender.x,
                y: defender.y,
                vx: (Math.random() - 0.5) * 3,
                vy: (Math.random() - 0.5) * 3,
                color: '#90ee90',
                size: 2,
                life: 0.5
            });
        }
    }, vineSegments * 40);
}
```

#### SOLAR BEAM / ENERGY BALL
```javascript
animateSolarBeam(attacker, defender) {
    const anim = this.animEngine;

    // 1. Charge phase - gathering solar energy
    attacker.playAnimation('attack');

    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            const angle = (i / 30) * Math.PI * 2;
            const radius = 50 + Math.random() * 20;
            anim.createParticle({
                x: attacker.x + Math.cos(angle) * radius,
                y: attacker.y + Math.sin(angle) * radius,
                vx: -Math.cos(angle) * 2,
                vy: -Math.sin(angle) * 2,
                color: '#ffff00',
                size: 3,
                life: 0.8
            });
        }, i * 30);
    }

    await anim.wait(1000); // Charge time

    // 2. Massive beam release
    await anim.queueAnimation({
        type: 'beam',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        color: '#ffff00',
        width: 25,
        glow: true,
        innerColor: '#ffffff',
        duration: 800,
        particles: true
    });

    // 3. Devastating impact
    anim.shake(12, 600);
    anim.flash('#ffff00', 0.6, 500);

    for (let i = 0; i < 50; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: Math.cos(i / 50 * Math.PI * 2) * 5,
            vy: Math.sin(i / 50 * Math.PI * 2) * 5,
            color: ['#ffff00', '#90ee90', '#ffffff'][Math.floor(Math.random() * 3)],
            size: 4,
            life: 1.2
        });
    }

    defender.playAnimation('hurt');
}
```

#### WOOD HAMMER / ROOT
```javascript
animateWoodHammer(attacker, defender) {
    const anim = this.animEngine;

    // 1. Roots burst from ground beneath attacker
    for (let i = 0; i < 10; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 20,
            y: attacker.y + 15,
            vx: 0,
            vy: -3,
            color: '#654321',
            size: 3,
            type: 'square',
            life: 0.6
        });
    }

    // 2. Attacker leaps high
    await anim.queueAnimation({
        type: 'jump',
        target: attacker,
        height: 40,
        to: { x: defender.x, y: defender.y - 40 },
        duration: 400
    });

    // 3. Massive downward slam
    await anim.queueAnimation({
        type: 'slide',
        target: attacker,
        to: { x: defender.x, y: defender.y },
        duration: 150,
        easing: 'easeInQuad'
    });

    // 4. Ground shattering impact
    anim.shake(15, 500);
    anim.flash('#8b4513', 0.5, 300);

    for (let i = 0; i < 30; i++) {
        anim.createParticle({
            x: defender.x + (Math.random() - 0.5) * 40,
            y: defender.y + 10,
            vx: (Math.random() - 0.5) * 6,
            vy: -Math.random() * 5,
            color: ['#8b4513', '#654321', '#32cd32'][Math.floor(Math.random() * 3)],
            size: 4,
            type: 'square',
            life: 1.0
        });
    }

    defender.playAnimation('hurt');

    // 5. Return
    await anim.queueAnimation({
        type: 'slide',
        target: attacker,
        to: { x: attacker.originalX, y: attacker.originalY },
        duration: 300
    });
}
```

### 2.6 Ice Type Animations

#### ICE SHARD / FROST SHOCK
```javascript
animateIceShard(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Ice crystals form
    for (let i = 0; i < 8; i++) {
        const angle = (i / 8) * Math.PI * 2;
        anim.createParticle({
            x: attacker.x + Math.cos(angle) * 20,
            y: attacker.y + Math.sin(angle) * 20,
            vx: 0, vy: 0,
            color: '#00ffff',
            size: 3,
            life: 0.5,
            type: 'diamond'
        });
    }

    await anim.wait(300);

    // 2. Shards shoot rapidly
    for (let i = 0; i < 8; i++) {
        setTimeout(() => {
            const angle = (i / 8) * Math.PI * 2;
            anim.queueAnimation({
                type: 'projectile',
                from: { x: attacker.x, y: attacker.y },
                to: { x: defender.x + Math.cos(angle) * 15, y: defender.y + Math.sin(angle) * 15 },
                particle: {
                    color: '#87ceeb',
                    size: 4,
                    rotation: angle,
                    type: 'diamond',
                    trail: true,
                    trailColor: '#e0ffff'
                },
                duration: 300
            });

            // Impact frost
            setTimeout(() => {
                for (let j = 0; j < 5; j++) {
                    anim.createParticle({
                        x: defender.x,
                        y: defender.y,
                        vx: (Math.random() - 0.5) * 2,
                        vy: (Math.random() - 0.5) * 2,
                        color: '#00ffff',
                        size: 2,
                        life: 0.6
                    });
                }
            }, 300);
        }, i * 80);
    }

    anim.shake(4, 600);
    anim.flash('#00ffff', 0.3, 400);
    defender.playAnimation('hurt');
}
```

#### ICE BEAM / BLIZZARD
```javascript
animateIceBeam(attacker, defender) {
    const anim = this.animEngine;

    // 1. Cold air gathers
    for (let i = 0; i < 20; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 30,
            y: attacker.y + (Math.random() - 0.5) * 30,
            vx: (defender.x - attacker.x) * 0.01,
            vy: (defender.y - attacker.y) * 0.01,
            color: '#e0ffff',
            size: 2,
            life: 0.6,
            alpha: 0.7
        });
    }

    await anim.wait(400);

    // 2. Freezing beam
    await anim.queueAnimation({
        type: 'beam',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        color: '#00ffff',
        width: 15,
        glow: true,
        innerColor: '#ffffff',
        duration: 600,
        spiral: true
    });

    // 3. Freeze effect on defender
    anim.flash('#00ffff', 0.4, 400);
    anim.shake(6, 400);

    // Ice crystals spread over defender
    for (let i = 0; i < 25; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: defender.x + (Math.random() - 0.5) * 35,
                y: defender.y + (Math.random() - 0.5) * 35,
                vx: 0, vy: 0,
                color: '#87ceeb',
                size: 2,
                life: 1.5,
                alpha: 0.8
            });
        }, i * 30);
    }

    defender.playAnimation('hurt');
}
```

### 2.7 Dragon Type Animations

#### DRAGON BREATH / DRAGON RAGE
```javascript
animateDragonBreath(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Energy builds in mouth
    for (let i = 0; i < 15; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 15,
            y: attacker.y - 5 + (Math.random() - 0.5) * 10,
            vx: 0, vy: 0,
            color: ['#ff00ff', '#9370db', '#4b0082'][Math.floor(Math.random() * 3)],
            size: 3,
            life: 0.4
        });
    }

    await anim.wait(300);

    // 2. Breath weapon stream
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            const spread = (Math.random() - 0.5) * 20;
            anim.queueAnimation({
                type: 'projectile',
                from: { x: attacker.x, y: attacker.y },
                to: { x: defender.x + spread, y: defender.y + spread },
                particle: {
                    color: ['#ff00ff', '#9370db', '#8a2be2'][Math.floor(Math.random() * 3)],
                    size: 5,
                    trail: true,
                    alpha: 0.8
                },
                duration: 400 + Math.random() * 200
            });
        }, i * 50);
    }

    // 3. Engulfed in dragon energy
    anim.shake(7, 800);
    anim.flash('#9370db', 0.5, 600);

    for (let i = 0; i < 30; i++) {
        anim.createParticle({
            x: defender.x + (Math.random() - 0.5) * 40,
            y: defender.y + (Math.random() - 0.5) * 40,
            vx: (Math.random() - 0.5) * 3,
            vy: -Math.random() * 2,
            color: ['#ff00ff', '#9370db', '#8a2be2'][Math.floor(Math.random() * 3)],
            size: 3,
            life: 1.0
        });
    }

    defender.playAnimation('hurt');
}
```

#### DRAGON CLAW / OUTRAGE
```javascript
animateDragonClaw(attacker, defender) {
    const anim = this.animEngine;

    // 1. Draconic aura emanates
    attacker.playAnimation('attack');
    for (let i = 0; i < 20; i++) {
        anim.createParticle({
            x: attacker.x,
            y: attacker.y,
            vx: (Math.random() - 0.5) * 3,
            vy: (Math.random() - 0.5) * 3,
            color: '#9370db',
            size: 2,
            life: 0.5,
            alpha: 0.6
        });
    }

    // 2. Rapid dash
    await anim.queueAnimation({
        type: 'slide',
        target: attacker,
        to: { x: defender.x - 15, y: defender.y },
        duration: 150,
        easing: 'easeOutQuad'
    });

    // 3. Multiple claw slashes
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const slashAngle = -45 + i * 45;
            anim.queueAnimation({
                type: 'slash',
                x: defender.x,
                y: defender.y,
                angle: slashAngle,
                length: 30,
                color: '#ff00ff',
                width: 5,
                duration: 120
            });

            anim.shake(5, 150);

            // Draconic energy particles
            for (let j = 0; j < 8; j++) {
                anim.createParticle({
                    x: defender.x,
                    y: defender.y,
                    vx: Math.cos((j / 8) * Math.PI * 2 + slashAngle) * 4,
                    vy: Math.sin((j / 8) * Math.PI * 2 + slashAngle) * 4,
                    color: ['#ff00ff', '#9370db'][j % 2],
                    size: 3,
                    life: 0.7
                });
            }
        }, i * 150);
    }

    defender.playAnimation('hurt');

    // 4. Return
    setTimeout(() => {
        anim.queueAnimation({
            type: 'slide',
            target: attacker,
            to: { x: attacker.originalX, y: attacker.originalY },
            duration: 200
        });
    }, 500);
}
```

### 2.8 Shadow/Dark Type Animations

#### SHADOW BALL / DARK PULSE
```javascript
animateShadowBall(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Dark energy coalesces
    for (let i = 0; i < 20; i++) {
        const angle = (i / 20) * Math.PI * 2;
        const radius = 30;
        anim.createParticle({
            x: attacker.x + Math.cos(angle) * radius,
            y: attacker.y + Math.sin(angle) * radius,
            vx: -Math.cos(angle) * 1.5,
            vy: -Math.sin(angle) * 1.5,
            color: '#4b0082',
            size: 2,
            life: 0.6,
            alpha: 0.8
        });
    }

    await anim.wait(400);

    // 2. Shadow orb travels
    await anim.queueAnimation({
        type: 'projectile',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        particle: {
            color: '#000000',
            size: 12,
            glow: true,
            glowColor: '#8b00ff',
            trail: true,
            trailColor: '#4b0082',
            alpha: 0.9
        },
        duration: 500
    });

    // 3. Dark explosion
    anim.shake(8, 400);
    anim.flash('#000000', 0.6, 300);

    // Shadowy tendrils burst outward
    for (let i = 0; i < 16; i++) {
        const angle = (i / 16) * Math.PI * 2;
        for (let j = 0; j < 5; j++) {
            setTimeout(() => {
                anim.createParticle({
                    x: defender.x,
                    y: defender.y,
                    vx: Math.cos(angle) * (2 + j * 0.5),
                    vy: Math.sin(angle) * (2 + j * 0.5),
                    color: ['#000000', '#4b0082', '#8b00ff'][j % 3],
                    size: 3 - j * 0.4,
                    life: 0.8,
                    alpha: 0.9 - j * 0.1
                });
            }, j * 40);
        }
    }

    defender.playAnimation('hurt');
}
```

#### SHADOW CLAW / CURSE
```javascript
animateShadowClaw(attacker, defender) {
    const anim = this.animEngine;

    // 1. Attacker cloaked in shadow
    attacker.playAnimation('attack');
    await anim.queueAnimation({
        type: 'fade',
        target: attacker,
        to: 0.3,
        duration: 200
    });

    // 2. Teleport behind defender
    await anim.queueAnimation({
        type: 'teleport',
        target: attacker,
        to: { x: defender.x + 20, y: defender.y },
        particles: true,
        particleColor: '#4b0082'
    });

    // 3. Shadow claw strikes
    const clawPaths = [
        { angle: 45, length: 25 },
        { angle: -45, length: 25 },
        { angle: 0, length: 30 }
    ];

    for (let i = 0; i < clawPaths.length; i++) {
        setTimeout(() => {
            const claw = clawPaths[i];
            anim.queueAnimation({
                type: 'slash',
                x: defender.x,
                y: defender.y,
                angle: claw.angle,
                length: claw.length,
                color: '#8b00ff',
                width: 4,
                glow: true,
                duration: 150
            });

            anim.shake(6, 150);

            // Dark particles
            for (let j = 0; j < 10; j++) {
                anim.createParticle({
                    x: defender.x,
                    y: defender.y,
                    vx: (Math.random() - 0.5) * 4,
                    vy: (Math.random() - 0.5) * 4,
                    color: '#4b0082',
                    size: 2,
                    life: 0.6,
                    alpha: 0.8
                });
            }
        }, i * 150);
    }

    defender.playAnimation('hurt');

    // 4. Fade back and return
    await anim.wait(500);
    await anim.queueAnimation({
        type: 'fade',
        target: attacker,
        to: 1.0,
        duration: 200
    });

    await anim.queueAnimation({
        type: 'teleport',
        target: attacker,
        to: { x: attacker.originalX, y: attacker.originalY },
        particles: true,
        particleColor: '#4b0082'
    });
}
```

### 2.9 Poison Type Animations

#### POISON STING / TOXIC
```javascript
animateToxic(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Toxic droplets spray
    for (let i = 0; i < 12; i++) {
        setTimeout(() => {
            const spread = (Math.random() - 0.5) * 30;
            anim.queueAnimation({
                type: 'projectile',
                from: { x: attacker.x, y: attacker.y },
                to: { x: defender.x + spread, y: defender.y + spread },
                particle: {
                    color: '#800080',
                    size: 4,
                    trail: true,
                    trailColor: '#9370db',
                    alpha: 0.8
                },
                duration: 400,
                arc: true
            });

            // Poison splash on impact
            setTimeout(() => {
                for (let j = 0; j < 6; j++) {
                    anim.createParticle({
                        x: defender.x + spread,
                        y: defender.y + spread,
                        vx: (Math.random() - 0.5) * 2,
                        vy: -Math.random() * 2,
                        color: '#9370db',
                        size: 2,
                        life: 0.8,
                        alpha: 0.7
                    });
                }
            }, 400);
        }, i * 80);
    }

    // 2. Poison spreads over defender
    setTimeout(() => {
        anim.shake(4, 400);

        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                anim.createParticle({
                    x: defender.x + (Math.random() - 0.5) * 30,
                    y: defender.y + (Math.random() - 0.5) * 30,
                    vx: 0,
                    vy: 0.5,
                    color: ['#800080', '#9370db', '#8b008b'][Math.floor(Math.random() * 3)],
                    size: 2,
                    life: 1.5,
                    alpha: 0.6
                });
            }, i * 50);
        }

        defender.playAnimation('hurt');
    }, 1000);
}
```

#### SLUDGE BOMB / POISON JAB
```javascript
animateSludgeBomb(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Toxic sphere forms
    for (let i = 0; i < 15; i++) {
        anim.createParticle({
            x: attacker.x + (Math.random() - 0.5) * 20,
            y: attacker.y + (Math.random() - 0.5) * 20,
            vx: 0, vy: 0,
            color: '#8b008b',
            size: 3,
            life: 0.5,
            alpha: 0.7
        });
    }

    await anim.wait(300);

    // 2. Sludge ball arcs through air
    await anim.queueAnimation({
        type: 'projectile',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        particle: {
            color: '#800080',
            size: 10,
            glow: true,
            glowColor: '#9370db',
            trail: true,
            alpha: 0.8
        },
        duration: 600,
        arc: true,
        arcHeight: 30
    });

    // 3. Toxic explosion
    anim.shake(8, 500);
    anim.flash('#800080', 0.5, 300);

    for (let i = 0; i < 35; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: (Math.random() - 0.5) * 5,
            vy: (Math.random() - 0.5) * 5 - 1,
            color: ['#800080', '#9370db', '#8b008b'][Math.floor(Math.random() * 3)],
            size: 4,
            life: 1.2,
            alpha: 0.7
        });
    }

    // Lingering poison cloud
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: defender.x + (Math.random() - 0.5) * 40,
                y: defender.y + (Math.random() - 0.5) * 40,
                vx: (Math.random() - 0.5) * 0.5,
                vy: -Math.random() * 0.5,
                color: '#9370db',
                size: 3,
                life: 2.0,
                alpha: 0.4
            });
        }, i * 50);
    }

    defender.playAnimation('hurt');
}
```

### 2.10 Psychic/Magic Type Animations

#### PSYCHIC / CONFUSION
```javascript
animatePsychic(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Psychic energy radiates
    for (let i = 0; i < 25; i++) {
        const angle = (i / 25) * Math.PI * 2;
        const radius = 35;
        setTimeout(() => {
            anim.createParticle({
                x: attacker.x + Math.cos(angle) * radius,
                y: attacker.y + Math.sin(angle) * radius,
                vx: Math.cos(angle) * 0.5,
                vy: Math.sin(angle) * 0.5,
                color: ['#ff1493', '#ff69b4', '#da70d6'][Math.floor(Math.random() * 3)],
                size: 3,
                life: 0.8,
                alpha: 0.7
            });
        }, i * 30);
    }

    await anim.wait(500);

    // 2. Defender lifted by psychic force
    await anim.queueAnimation({
        type: 'float',
        target: defender,
        height: 20,
        duration: 400,
        oscillate: true
    });

    // 3. Psychic waves crush defender
    for (let i = 0; i < 8; i++) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'ring',
                x: defender.x,
                y: defender.y,
                radius: 15 + i * 5,
                color: '#ff1493',
                width: 3,
                duration: 200,
                pulse: true
            });

            anim.shake(4, 150);

            // Psychic sparkles
            for (let j = 0; j < 5; j++) {
                anim.createParticle({
                    x: defender.x + (Math.random() - 0.5) * 30,
                    y: defender.y + (Math.random() - 0.5) * 30,
                    vx: 0, vy: 0,
                    color: ['#ff1493', '#ff69b4'][j % 2],
                    size: 2,
                    life: 0.5
                });
            }
        }, i * 120);
    }

    defender.playAnimation('hurt');

    // 4. Drop defender
    await anim.wait(1000);
    await anim.queueAnimation({
        type: 'slide',
        target: defender,
        to: { x: defender.originalX, y: defender.originalY },
        duration: 200,
        easing: 'easeInQuad'
    });
}
```

#### COSMIC POWER / BARRIER
```javascript
animateBarrier(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Energy gathers around attacker
    for (let i = 0; i < 30; i++) {
        const angle = (i / 30) * Math.PI * 2;
        setTimeout(() => {
            for (let r = 20; r <= 40; r += 10) {
                anim.createParticle({
                    x: attacker.x + Math.cos(angle) * r,
                    y: attacker.y + Math.sin(angle) * r,
                    vx: 0, vy: 0,
                    color: ['#00f2fe', '#4facfe', '#f093fb'][Math.floor(r / 10) % 3],
                    size: 2,
                    life: 1.0,
                    alpha: 0.6
                });
            }
        }, i * 30);
    }

    // 2. Hexagonal barrier forms
    for (let i = 0; i < 6; i++) {
        setTimeout(() => {
            const angle = (i / 6) * Math.PI * 2;
            const x1 = attacker.x + Math.cos(angle) * 25;
            const y1 = attacker.y + Math.sin(angle) * 25;
            const x2 = attacker.x + Math.cos(angle + Math.PI / 3) * 25;
            const y2 = attacker.y + Math.sin(angle + Math.PI / 3) * 25;

            anim.queueAnimation({
                type: 'line',
                from: { x: x1, y: y1 },
                to: { x: x2, y: y2 },
                color: '#00f2fe',
                width: 2,
                glow: true,
                duration: 300,
                persist: true
            });
        }, i * 80);
    }

    // 3. Barrier pulses
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'ring',
                x: attacker.x,
                y: attacker.y,
                radius: 30,
                color: '#4facfe',
                width: 2,
                duration: 400,
                pulse: true
            });

            // Sparkles
            for (let j = 0; j < 10; j++) {
                const angle = (j / 10) * Math.PI * 2;
                anim.createParticle({
                    x: attacker.x + Math.cos(angle) * 25,
                    y: attacker.y + Math.sin(angle) * 25,
                    vx: 0, vy: 0,
                    color: '#ffffff',
                    size: 2,
                    life: 0.3
                });
            }
        }, i * 200);
    }
}
```

### 2.11 Status Move Animations

#### WILL-O-WISP (Burn)
```javascript
animateWillOWisp(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Three ghostly flames appear
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const angle = (i / 3) * Math.PI * 2;
            const startX = attacker.x + Math.cos(angle) * 25;
            const startY = attacker.y + Math.sin(angle) * 25;

            // Flame floats eerily
            const flame = {
                x: startX,
                y: startY,
                targetX: defender.x + Math.cos(angle) * 20,
                targetY: defender.y + Math.sin(angle) * 20
            };

            // Animate flame movement
            anim.queueAnimation({
                type: 'custom',
                duration: 1000,
                update: (progress) => {
                    flame.x = startX + (flame.targetX - startX) * progress;
                    flame.y = startY + (flame.targetY - startY) * progress;
                    flame.y += Math.sin(progress * Math.PI * 4) * 5; // Wobble

                    // Emit flame particles
                    if (Math.random() < 0.3) {
                        anim.createParticle({
                            x: flame.x,
                            y: flame.y,
                            vx: (Math.random() - 0.5) * 0.5,
                            vy: -Math.random() * 1,
                            color: ['#ff4500', '#ffa500', '#ffff00'][Math.floor(Math.random() * 3)],
                            size: 2,
                            life: 0.5,
                            alpha: 0.8
                        });
                    }
                }
            });
        }, i * 300);
    }

    // 2. Flames circle defender
    await anim.wait(1200);

    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            const angle = (i / 20) * Math.PI * 2 + performance.now() * 0.001;
            anim.createParticle({
                x: defender.x + Math.cos(angle) * 25,
                y: defender.y + Math.sin(angle) * 25,
                vx: 0, vy: -0.5,
                color: ['#ff4500', '#ffa500'][i % 2],
                size: 2,
                life: 0.8,
                alpha: 0.7
            });
        }, i * 50);
    }

    defender.playAnimation('hurt');
    anim.showStatusIcon(defender, 'burn');
}
```

#### SLEEP POWDER (Sleep)
```javascript
animateSleepPowder(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Sparkling powder clouds emerge
    for (let i = 0; i < 40; i++) {
        setTimeout(() => {
            const spread = (Math.random() - 0.5) * 40;
            anim.createParticle({
                x: attacker.x + (Math.random() - 0.5) * 20,
                y: attacker.y + (Math.random() - 0.5) * 20,
                vx: (defender.x - attacker.x) * 0.005 + (Math.random() - 0.5) * 0.5,
                vy: (defender.y - attacker.y) * 0.005 - Math.random() * 0.3,
                color: ['#ffff99', '#ffffcc', '#f0f0ff'][Math.floor(Math.random() * 3)],
                size: 2,
                life: 2.0,
                alpha: 0.6,
                ay: 0.05 // Slow fall
            });
        }, i * 40);
    }

    // 2. Powder settles on defender
    await anim.wait(1200);

    // 3. Sleep effect
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            // "Z" particles float up
            const zPositions = [
                { x: defender.x + 10, y: defender.y - 10 },
                { x: defender.x + 15, y: defender.y - 20 },
                { x: defender.x + 20, y: defender.y - 30 }
            ];

            zPositions.forEach((pos, j) => {
                setTimeout(() => {
                    anim.queueAnimation({
                        type: 'text',
                        text: 'Z',
                        x: pos.x,
                        y: pos.y,
                        color: '#4169e1',
                        fontSize: 10,
                        vy: -1,
                        duration: 800,
                        fadeOut: true
                    });
                }, j * 200);
            });
        }, i * 1000);
    }

    defender.playAnimation('hurt');
    anim.showStatusIcon(defender, 'sleep');
}
```

### 2.12 Weather Move Animations

#### SUNNY DAY
```javascript
animateSunnyDay(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Sun symbol appears above attacker
    await anim.queueAnimation({
        type: 'custom',
        duration: 1000,
        render: (ctx, progress) => {
            const y = attacker.y - 40 - (1 - progress) * 30;
            const radius = 10 + Math.sin(progress * Math.PI) * 2;

            // Sun core
            ctx.fillStyle = '#ffff00';
            ctx.beginPath();
            ctx.arc(attacker.x, y, radius, 0, Math.PI * 2);
            ctx.fill();

            // Sun rays
            for (let i = 0; i < 8; i++) {
                const angle = (i / 8) * Math.PI * 2 + progress * Math.PI;
                ctx.strokeStyle = '#ffa500';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(attacker.x + Math.cos(angle) * radius, y + Math.sin(angle) * radius);
                ctx.lineTo(attacker.x + Math.cos(angle) * (radius + 8), y + Math.sin(angle) * (radius + 8));
                ctx.stroke();
            }
        }
    });

    // 2. Screen brightens
    anim.flash('#ffff00', 0.3, 500);

    // 3. Light particles cascade down
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: Math.random() * this.canvas.width,
                y: -10,
                vx: (Math.random() - 0.5) * 0.5,
                vy: Math.random() * 2 + 1,
                color: ['#ffff00', '#ffa500', '#ffffff'][Math.floor(Math.random() * 3)],
                size: 2,
                life: 2.0,
                alpha: 0.6
            });
        }, i * 30);
    }

    // 4. Show weather icon
    anim.showWeatherIcon('sun');
}
```

#### RAIN DANCE
```javascript
animateRainDance(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Dark clouds gather
    anim.flash('#404060', 0.5, 600);

    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: Math.random() * this.canvas.width,
                y: Math.random() * 30,
                vx: (Math.random() - 0.5) * 1,
                vy: 0.2,
                color: '#808080',
                size: 8,
                life: 3.0,
                alpha: 0.5,
                ay: 0
            });
        }, i * 50);
    }

    await anim.wait(800);

    // 2. Rain begins
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: Math.random() * this.canvas.width,
                y: -5,
                vx: -0.5 + Math.random() * 0.2,
                vy: 4 + Math.random() * 2,
                color: '#87ceeb',
                size: 1,
                type: 'line',
                lineLength: 6,
                life: 1.5,
                alpha: 0.7,
                ay: 0.1
            });
        }, i * 20);
    }

    // 3. Lightning flash
    setTimeout(() => {
        anim.flash('#ffffff', 0.8, 100);

        // Thunder sound effect trigger
        this.game.audio.playSFX('thunder');
    }, 1200);

    // 4. Show weather icon
    anim.showWeatherIcon('rain');
}
```

### 2.13 Ultimate/Signature Moves

#### HYPER BEAM
```javascript
animateHyperBeam(attacker, defender) {
    const anim = this.animEngine;

    // 1. Massive charge up
    attacker.playAnimation('attack');

    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const angle = Math.random() * Math.PI * 2;
            const distance = 50 + Math.random() * 30;
            anim.createParticle({
                x: attacker.x + Math.cos(angle) * distance,
                y: attacker.y + Math.sin(angle) * distance,
                vx: -Math.cos(angle) * 3,
                vy: -Math.sin(angle) * 3,
                color: ['#ff0000', '#ffa500', '#ffff00', '#ffffff'][Math.floor(Math.random() * 4)],
                size: 4,
                life: 0.6
            });
        }, i * 20);
    }

    await anim.wait(1000);

    // 2. Energy concentrates
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'ring',
                x: attacker.x,
                y: attacker.y,
                radius: 40 - i * 2,
                color: '#ffff00',
                width: 3,
                duration: 100
            });
        }, i * 30);
    }

    await anim.wait(600);

    // 3. UNLEASH THE BEAM
    anim.shake(20, 1500);
    anim.flash('#ffffff', 0.8, 200);

    await anim.queueAnimation({
        type: 'beam',
        from: { x: attacker.x, y: attacker.y },
        to: { x: defender.x, y: defender.y },
        color: '#ffff00',
        width: 35,
        glow: true,
        innerColor: '#ffffff',
        outerColor: '#ff0000',
        duration: 1200,
        particles: true,
        distortion: true
    });

    // 4. Catastrophic explosion
    for (let i = 0; i < 80; i++) {
        anim.createParticle({
            x: defender.x,
            y: defender.y,
            vx: (Math.random() - 0.5) * 8,
            vy: (Math.random() - 0.5) * 8,
            color: ['#ff0000', '#ffa500', '#ffff00', '#ffffff'][Math.floor(Math.random() * 4)],
            size: 5,
            life: 1.5
        });
    }

    // 5. Shockwave
    for (let r = 20; r <= 100; r += 20) {
        setTimeout(() => {
            anim.queueAnimation({
                type: 'ring',
                x: defender.x,
                y: defender.y,
                radius: r,
                color: '#ffa500',
                width: 4,
                duration: 300,
                fadeOut: true
            });
        }, (r - 20) * 40);
    }

    defender.playAnimation('hurt');

    // 6. Attacker recharge (exhausted animation)
    await anim.wait(1500);
    // Show "must recharge" indicator
}
```

#### EXPLOSION
```javascript
animateExplosion(attacker, defender) {
    const anim = this.animEngine;

    attacker.playAnimation('attack');

    // 1. Critical mass buildup
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: attacker.x + (Math.random() - 0.5) * 30,
                y: attacker.y + (Math.random() - 0.5) * 30,
                vx: 0, vy: 0,
                color: '#ff0000',
                size: 3 + Math.random() * 2,
                life: 0.3,
                alpha: 0.8
            });

            // Pulsing glow
            if (i % 5 === 0) {
                anim.queueAnimation({
                    type: 'ring',
                    x: attacker.x,
                    y: attacker.y,
                    radius: 20 + i,
                    color: '#ff0000',
                    width: 2,
                    duration: 200
                });
            }
        }, i * 40);
    }

    await anim.wait(1200);

    // 2. WARNING FLASH
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            anim.flash('#ff0000', 0.6, 100);
        }, i * 100);
    }

    await anim.wait(500);

    // 3. MASSIVE EXPLOSION
    anim.shake(25, 2000);
    anim.flash('#ffffff', 1.0, 300);

    // Nuclear explosion effect
    for (let ring = 0; ring < 10; ring++) {
        setTimeout(() => {
            const radius = ring * 15;

            // Explosive ring
            anim.queueAnimation({
                type: 'ring',
                x: attacker.x,
                y: attacker.y,
                radius: radius,
                color: ['#ff0000', '#ffa500', '#ffff00'][ring % 3],
                width: 6,
                duration: 400,
                expand: true,
                maxRadius: radius + 30
            });

            // Particles at ring edge
            for (let i = 0; i < 20; i++) {
                const angle = (i / 20) * Math.PI * 2;
                anim.createParticle({
                    x: attacker.x + Math.cos(angle) * radius,
                    y: attacker.y + Math.sin(angle) * radius,
                    vx: Math.cos(angle) * 6,
                    vy: Math.sin(angle) * 6,
                    color: ['#ff0000', '#ffa500', '#ffff00'][Math.floor(Math.random() * 3)],
                    size: 6,
                    life: 1.5
                });
            }
        }, ring * 80);
    }

    // 4. Fire everywhere
    for (let i = 0; i < 150; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: attacker.x + (Math.random() - 0.5) * 120,
                y: attacker.y + (Math.random() - 0.5) * 120,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.5) * 8 - 2,
                color: ['#ff0000', '#ffa500', '#ffff00', '#000000'][Math.floor(Math.random() * 4)],
                size: 4,
                life: 2.0
            });
        }, Math.random() * 1000);
    }

    // 5. Both creatures take damage
    defender.playAnimation('hurt');
    attacker.playAnimation('faint'); // Attacker faints from using explosion
}
```

---

## 3. UI/UX Enhancement List

### 3.1 Battle UI Improvements

#### Enhanced HP Bars
```css
.hp-bar {
    position: relative;
    width: 100px;
    height: 8px;
    background: linear-gradient(90deg, #1a1a2e 0%, #0f172a 100%);
    border: 2px solid rgba(79, 172, 254, 0.4);
    border-radius: 4px;
    overflow: visible;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
}

.hp-fill {
    height: 100%;
    background: linear-gradient(90deg, #4ade80 0%, #22c55e 100%);
    border-radius: 2px;
    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

/* Animated shine effect */
.hp-fill::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(255, 255, 255, 0.4) 50%,
        transparent 100%
    );
    animation: hpShine 2s infinite;
}

@keyframes hpShine {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* HP color stages */
.hp-fill.hp-high {
    background: linear-gradient(90deg, #4ade80 0%, #22c55e 100%);
}

.hp-fill.hp-medium {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
}

.hp-fill.hp-low {
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
    animation: hpLowPulse 0.5s infinite alternate;
}

@keyframes hpLowPulse {
    from { filter: brightness(1); }
    to { filter: brightness(1.3); }
}

/* HP depletion effect */
.hp-fill.depleting {
    background: linear-gradient(90deg,
        #ef4444 0%,
        #fbbf24 50%,
        transparent 100%
    );
    animation: hpDepleting 0.3s;
}

@keyframes hpDepleting {
    0%, 100% { transform: scaleX(1); }
    50% { transform: scaleX(1.05); }
}
```

#### Floating Damage Numbers
```javascript
class DamageNumber {
    constructor(x, y, damage, type = 'normal') {
        this.x = x;
        this.y = y;
        this.damage = damage;
        this.type = type;
        this.life = 1.0;
        this.vy = -2;
        this.scale = this.getScale();
        this.color = this.getColor();
    }

    getScale() {
        switch(this.type) {
            case 'critical': return 1.8;
            case 'super_effective': return 1.4;
            case 'not_effective': return 0.8;
            case 'miss': return 1.2;
            case 'heal': return 1.3;
            default: return 1.0;
        }
    }

    getColor() {
        switch(this.type) {
            case 'critical': return '#ffff00';
            case 'super_effective': return '#4ade80';
            case 'not_effective': return '#94a3b8';
            case 'miss': return '#6b7280';
            case 'heal': return '#10b981';
            default: return '#ffffff';
        }
    }

    update(deltaTime) {
        this.y += this.vy;
        this.vy += 0.05; // Gravity
        this.life -= 0.02;
        return this.life > 0;
    }

    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.life;
        ctx.font = `${12 * this.scale}px monospace`;
        ctx.fillStyle = this.color;
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.textAlign = 'center';

        const text = this.type === 'miss' ? 'MISS' :
                     this.type === 'heal' ? `+${this.damage}` :
                     this.damage.toString();

        ctx.strokeText(text, this.x, this.y);
        ctx.fillText(text, this.x, this.y);
        ctx.restore();
    }
}
```

#### Type Effectiveness Indicators
```javascript
showEffectivenessIndicator(x, y, effectiveness) {
    const messages = {
        0: { text: "NO EFFECT", color: '#6b7280', icon: '✕' },
        0.25: { text: "BARELY EFFECTIVE", color: '#94a3b8', icon: '▼▼' },
        0.5: { text: "NOT VERY EFFECTIVE", color: '#cbd5e1', icon: '▼' },
        1.0: null,
        2.0: { text: "SUPER EFFECTIVE", color: '#4ade80', icon: '▲' },
        4.0: { text: "DEVASTATINGLY EFFECTIVE", color: '#22c55e', icon: '▲▲' }
    };

    const msg = messages[effectiveness];
    if (!msg) return;

    // Create banner
    const banner = {
        x: this.canvas.width / 2,
        y: y - 30,
        text: msg.text,
        color: msg.color,
        icon: msg.icon,
        life: 1.0,
        scale: 0
    };

    // Animate banner
    const animation = setInterval(() => {
        banner.life -= 0.02;
        banner.scale = Math.min(banner.scale + 0.1, 1.0);
        banner.y -= 0.5;

        if (banner.life <= 0) {
            clearInterval(animation);
        }
    }, 16);

    this.banners.push(banner);
}

renderBanners(ctx) {
    this.banners.forEach(banner => {
        ctx.save();
        ctx.globalAlpha = banner.life;
        ctx.translate(banner.x, banner.y);
        ctx.scale(banner.scale, banner.scale);

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(-60, -12, 120, 24);

        // Border
        ctx.strokeStyle = banner.color;
        ctx.lineWidth = 2;
        ctx.strokeRect(-60, -12, 120, 24);

        // Text
        ctx.font = '10px monospace';
        ctx.fillStyle = banner.color;
        ctx.textAlign = 'center';
        ctx.fillText(`${banner.icon} ${banner.text} ${banner.icon}`, 0, 4);

        ctx.restore();
    });

    // Remove dead banners
    this.banners = this.banners.filter(b => b.life > 0);
}
```

### 3.2 Status Condition Visual Indicators

```javascript
class StatusIconSystem {
    constructor() {
        this.icons = {
            burn: {
                emoji: '🔥',
                color: '#ff4500',
                particles: () => ({
                    color: '#ffa500',
                    vy: -1,
                    life: 0.5
                })
            },
            poison: {
                emoji: '☠️',
                color: '#800080',
                particles: () => ({
                    color: '#9370db',
                    vy: 0.5,
                    life: 0.8
                })
            },
            paralyze: {
                emoji: '⚡',
                color: '#ffff00',
                particles: () => ({
                    color: '#ffff00',
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    life: 0.3
                })
            },
            sleep: {
                emoji: '💤',
                color: '#4169e1',
                particles: () => ({
                    color: '#87ceeb',
                    vy: -0.8,
                    life: 1.0
                })
            },
            freeze: {
                emoji: '❄️',
                color: '#00ffff',
                particles: () => ({
                    color: '#87ceeb',
                    vy: 0,
                    life: 1.5
                })
            }
        };
    }

    renderStatus(ctx, creature, status) {
        const icon = this.icons[status];
        if (!icon) return;

        // Draw status icon
        ctx.save();
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(icon.emoji, creature.x, creature.y - 35);
        ctx.restore();

        // Emit status particles
        if (Math.random() < 0.2) {
            const particleConfig = icon.particles();
            this.game.animEngine.createParticle({
                x: creature.x + (Math.random() - 0.5) * 20,
                y: creature.y + (Math.random() - 0.5) * 20,
                vx: particleConfig.vx || 0,
                vy: particleConfig.vy || 0,
                color: particleConfig.color,
                size: 2,
                life: particleConfig.life,
                alpha: 0.6
            });
        }
    }
}
```

### 3.3 Battle Transitions

#### Battle Start Transition
```javascript
async startBattleTransition() {
    const anim = this.animEngine;

    // 1. Screen flash
    anim.flash('#ffffff', 1.0, 200);
    await anim.wait(200);

    // 2. Wipe transition
    await anim.queueAnimation({
        type: 'wipe',
        direction: 'vertical',
        color: '#000000',
        duration: 400
    });

    // 3. Battle zoom in
    await anim.queueAnimation({
        type: 'zoom',
        from: 2.0,
        to: 1.0,
        duration: 600,
        easing: 'easeOutQuad'
    });

    // 4. Creatures slide in
    await Promise.all([
        anim.queueAnimation({
            type: 'slide',
            target: this.battle.enemyCreature,
            from: { x: this.canvas.width + 50, y: this.canvas.height * 0.35 },
            to: { x: this.canvas.width * 0.75, y: this.canvas.height * 0.35 },
            duration: 400,
            easing: 'easeOutBack'
        }),
        anim.queueAnimation({
            type: 'slide',
            target: this.battle.playerCreature,
            from: { x: -50, y: this.canvas.height * 0.7 },
            to: { x: this.canvas.width * 0.25, y: this.canvas.height * 0.7 },
            duration: 400,
            easing: 'easeOutBack'
        })
    ]);

    // 5. Battle ready flash
    anim.flash('#00f2fe', 0.3, 200);
    this.showBattleMessage("BATTLE START!");
}
```

#### Victory Transition
```javascript
async victoryTransition() {
    const anim = this.animEngine;

    // 1. Enemy creature faints
    this.battle.enemyCreature.playAnimation('faint');

    await anim.queueAnimation({
        type: 'fade',
        target: this.battle.enemyCreature,
        to: 0,
        duration: 600
    });

    // 2. Victory fanfare particles
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            anim.createParticle({
                x: this.battle.playerCreature.x,
                y: this.battle.playerCreature.y,
                vx: (Math.random() - 0.5) * 5,
                vy: -Math.random() * 5 - 2,
                color: ['#ffff00', '#ffa500', '#ffffff'][Math.floor(Math.random() * 3)],
                size: 4,
                life: 1.5
            });
        }, i * 30);
    }

    // 3. Victory message
    await anim.wait(800);
    this.showBattleMessage("VICTORY!", { color: '#4ade80', scale: 2.0 });

    // 4. Player creature victory animation
    this.battle.playerCreature.playAnimation('victory');

    // 5. Sparkles around player creature
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            const angle = (i / 30) * Math.PI * 2;
            const radius = 30;
            anim.createParticle({
                x: this.battle.playerCreature.x + Math.cos(angle) * radius,
                y: this.battle.playerCreature.y + Math.sin(angle) * radius,
                vx: Math.cos(angle) * 2,
                vy: Math.sin(angle) * 2 - 1,
                color: '#ffffff',
                size: 3,
                life: 1.0
            });
        }, i * 40);
    }
}
```

### 3.4 Menu Transitions & Polish

```css
/* Smooth menu animations */
.menu {
    transform: translateY(20px);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
}

.menu.active {
    transform: translateY(0);
    opacity: 1;
    pointer-events: all;
    animation: menuSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes menuSlideIn {
    0% {
        transform: translateY(20px) scale(0.95);
        opacity: 0;
    }
    100% {
        transform: translateY(0) scale(1);
        opacity: 1;
    }
}

/* Menu option hover effects */
.menu-option, .move-option {
    position: relative;
    transition: all 0.2s;
    overflow: hidden;
}

.menu-option::before, .move-option::before {
    content: '';
    position: absolute;
    left: -100%;
    top: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(79, 172, 254, 0.2) 50%,
        transparent 100%
    );
    transition: left 0.4s;
}

.menu-option:hover::before, .move-option:hover::before {
    left: 100%;
}

.menu-option.selected {
    background: linear-gradient(90deg,
        rgba(79, 172, 254, 0.3) 0%,
        rgba(240, 147, 251, 0.3) 100%
    );
    transform: translateX(8px);
    box-shadow: -4px 0 0 var(--primary);
}

/* Move selection with type colors */
.move-option {
    border-left: 4px solid transparent;
    transition: all 0.2s;
}

.move-option.selected {
    border-left-color: var(--primary);
    background: rgba(79, 172, 254, 0.2);
    transform: translateX(4px);
}

.move-option[data-type="fire"] { border-left-color: #ff4500; }
.move-option[data-type="water"] { border-left-color: #0080ff; }
.move-option[data-type="nature"] { border-left-color: #22c55e; }
.move-option[data-type="electric"] { border-left-color: #ffff00; }
.move-option[data-type="ice"] { border-left-color: #00ffff; }
.move-option[data-type="dragon"] { border-left-color: #9370db; }
.move-option[data-type="shadow"] { border-left-color: #4b0082; }
.move-option[data-type="poison"] { border-left-color: #800080; }
```

### 3.5 Creature Sprite Enhancements

```javascript
class EnhancedCreatureRenderer {
    constructor(creature, isPlayer) {
        this.creature = creature;
        this.isPlayer = isPlayer;
        this.size = isPlayer ? 35 : 30;
        this.hue = this.getTypeHue(creature.type);
        this.breathePhase = 0;
    }

    getTypeHue(type) {
        const hues = {
            fire: 0,      // Red
            water: 200,   // Blue
            nature: 120,  // Green
            electric: 60, // Yellow
            ice: 180,     // Cyan
            dragon: 270,  // Purple
            shadow: 280,  // Dark purple
            poison: 300,  // Magenta
            normal: 0     // Neutral
        };
        return hues[type] || 0;
    }

    render(ctx, x, y, animState = 'idle') {
        ctx.save();

        // Breathing animation
        this.breathePhase += 0.05;
        const breatheScale = 1 + Math.sin(this.breathePhase) * 0.05;

        ctx.translate(x, y);
        ctx.scale(breatheScale, breatheScale);

        // Shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.beginPath();
        ctx.ellipse(0, this.size/2 + 2, this.size/2, this.size/4, 0, 0, Math.PI * 2);
        ctx.fill();

        // Main body with gradient
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, this.size/2);
        gradient.addColorStop(0, `hsl(${this.hue}, 70%, 60%)`);
        gradient.addColorStop(0.7, `hsl(${this.hue}, 60%, 40%)`);
        gradient.addColorStop(1, `hsl(${this.hue}, 50%, 20%)`);

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(0, 0, this.size/2, 0, Math.PI * 2);
        ctx.fill();

        // Outline
        ctx.strokeStyle = `hsl(${this.hue}, 40%, 20%)`;
        ctx.lineWidth = 2;
        ctx.stroke();

        // Shine/highlight
        const highlight = ctx.createRadialGradient(
            -this.size/6, -this.size/6, 0,
            -this.size/6, -this.size/6, this.size/4
        );
        highlight.addColorStop(0, 'rgba(255, 255, 255, 0.6)');
        highlight.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = highlight;
        ctx.beginPath();
        ctx.arc(0, 0, this.size/2, 0, Math.PI * 2);
        ctx.fill();

        // Eyes
        const eyeY = -this.size/6;
        const eyeSpacing = this.size/4;

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(-eyeSpacing, eyeY, 3, 0, Math.PI * 2);
        ctx.arc(eyeSpacing, eyeY, 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#000000';
        ctx.beginPath();
        ctx.arc(-eyeSpacing, eyeY, 2, 0, Math.PI * 2);
        ctx.arc(eyeSpacing, eyeY, 2, 0, Math.PI * 2);
        ctx.fill();

        // Name label
        ctx.font = '6px monospace';
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.textAlign = 'center';
        const name = this.creature.name.substring(0, 8).toUpperCase();
        ctx.strokeText(name, 0, this.size/2 + 15);
        ctx.fillText(name, 0, this.size/2 + 15);

        ctx.restore();
    }
}
```

---

## 4. Visual Effect Library

### 4.1 Particle Types

```javascript
const PARTICLE_TYPES = {
    CIRCLE: (ctx, particle) => {
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.fill();
    },

    SQUARE: (ctx, particle) => {
        ctx.save();
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.fillRect(-particle.size/2, -particle.size/2, particle.size, particle.size);
        ctx.restore();
    },

    DIAMOND: (ctx, particle) => {
        ctx.save();
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.beginPath();
        ctx.moveTo(0, -particle.size);
        ctx.lineTo(particle.size, 0);
        ctx.lineTo(0, particle.size);
        ctx.lineTo(-particle.size, 0);
        ctx.closePath();
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.fill();
        ctx.restore();
    },

    STAR: (ctx, particle) => {
        ctx.save();
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
            const x = Math.cos(angle) * particle.size;
            const y = Math.sin(angle) * particle.size;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.fill();
        ctx.restore();
    },

    LINE: (ctx, particle) => {
        ctx.save();
        ctx.translate(particle.x, particle.y);
        ctx.rotate(Math.atan2(particle.vy, particle.vx));
        ctx.strokeStyle = particle.color;
        ctx.lineWidth = particle.size;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(particle.lineLength || 6, 0);
        ctx.stroke();
        ctx.restore();
    },

    SPARK: (ctx, particle) => {
        // Electric spark effect
        ctx.strokeStyle = particle.color;
        ctx.lineWidth = particle.size;
        ctx.globalAlpha = particle.life * particle.alpha;
        ctx.beginPath();
        ctx.moveTo(particle.x, particle.y);
        for (let i = 0; i < 3; i++) {
            const angle = Math.random() * Math.PI * 2;
            const length = Math.random() * particle.size * 2;
            ctx.lineTo(
                particle.x + Math.cos(angle) * length,
                particle.y + Math.sin(angle) * length
            );
        }
        ctx.stroke();
    }
};
```

### 4.2 Screen Effects

```javascript
class ScreenEffects {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.effects = [];
    }

    // Screen shake
    shake(intensity, duration) {
        this.effects.push({
            type: 'shake',
            intensity,
            duration,
            elapsed: 0
        });
    }

    // Flash effect
    flash(color, opacity, duration) {
        this.effects.push({
            type: 'flash',
            color,
            opacity,
            duration,
            elapsed: 0
        });
    }

    // Vignette effect
    vignette(intensity = 0.7, duration = 1000) {
        this.effects.push({
            type: 'vignette',
            intensity,
            duration,
            elapsed: 0
        });
    }

    // Zoom effect
    zoom(from, to, duration) {
        this.effects.push({
            type: 'zoom',
            from,
            to,
            duration,
            elapsed: 0
        });
    }

    // Blur effect
    blur(amount, duration) {
        this.effects.push({
            type: 'blur',
            amount,
            duration,
            elapsed: 0
        });
    }

    update(deltaTime) {
        this.effects = this.effects.filter(effect => {
            effect.elapsed += deltaTime;
            return effect.elapsed < effect.duration;
        });
    }

    render() {
        this.ctx.save();

        // Apply all active effects
        this.effects.forEach(effect => {
            const progress = effect.elapsed / effect.duration;
            const eased = this.easeOutQuad(progress);

            switch(effect.type) {
                case 'shake':
                    const x = (Math.random() - 0.5) * effect.intensity * (1 - eased);
                    const y = (Math.random() - 0.5) * effect.intensity * (1 - eased);
                    this.ctx.translate(x, y);
                    break;

                case 'flash':
                    this.ctx.fillStyle = effect.color;
                    this.ctx.globalAlpha = effect.opacity * (1 - eased);
                    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                    break;

                case 'vignette':
                    const gradient = this.ctx.createRadialGradient(
                        this.canvas.width / 2,
                        this.canvas.height / 2,
                        0,
                        this.canvas.width / 2,
                        this.canvas.height / 2,
                        this.canvas.width / 2
                    );
                    gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
                    gradient.addColorStop(1, `rgba(0, 0, 0, ${effect.intensity * (1 - eased)})`);
                    this.ctx.fillStyle = gradient;
                    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                    break;

                case 'zoom':
                    const scale = effect.from + (effect.to - effect.from) * eased;
                    this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
                    this.ctx.scale(scale, scale);
                    this.ctx.translate(-this.canvas.width / 2, -this.canvas.height / 2);
                    break;

                case 'blur':
                    this.ctx.filter = `blur(${effect.amount * (1 - eased)}px)`;
                    break;
            }
        });

        this.ctx.restore();
    }

    easeOutQuad(t) {
        return t * (2 - t);
    }
}
```

---

## 5. Implementation Priority

### Phase 1: Core Animation System (Week 1)
1. ✅ Battle animation engine framework
2. ✅ Particle system
3. ✅ Screen shake/flash effects
4. ✅ Damage number system
5. ✅ Basic creature animations (idle, attack, hurt)

### Phase 2: Physical & Elemental Moves (Week 2)
1. ✅ 15 Physical attack animations (Tackle, Slash, Earthquake, etc.)
2. ✅ Fire type moves (5+ animations)
3. ✅ Water type moves (5+ animations)
4. ✅ Electric type moves (4+ animations)
5. ✅ Type effectiveness indicators

### Phase 3: Special Types & Status (Week 3)
1. ✅ Nature/Grass moves (6+ animations)
2. ✅ Ice moves (4+ animations)
3. ✅ Dragon moves (4+ animations)
4. ✅ Shadow/Dark moves (4+ animations)
5. ✅ Poison moves (4+ animations)
6. ✅ Psychic/Magic moves (4+ animations)
7. ✅ Status condition animations
8. ✅ Weather effects

### Phase 4: UI/UX Polish (Week 4)
1. ✅ Enhanced HP bars with animations
2. ✅ Battle transition effects
3. ✅ Menu animations and transitions
4. ✅ Enhanced creature sprites
5. ✅ Status icons and particles
6. ✅ Victory/defeat animations

### Phase 5: Ultimate Moves & Final Polish (Week 5)
1. ✅ Ultimate move animations (Hyper Beam, Explosion, etc.)
2. ✅ Battle intro cinematics
3. ✅ Comprehensive particle library
4. ✅ Screen effect library
5. ✅ Performance optimization
6. ✅ Animation settings for reduced motion

---

## 6. Performance Considerations

### Optimization Strategies

```javascript
class AnimationOptimizer {
    constructor() {
        this.maxParticles = 200;
        this.particlePool = [];
        this.renderBudget = 16; // ms per frame
        this.qualityLevel = 'high'; // high, medium, low
    }

    // Object pooling for particles
    getParticle() {
        return this.particlePool.pop() || {};
    }

    releaseParticle(particle) {
        if (this.particlePool.length < this.maxParticles) {
            Object.keys(particle).forEach(key => delete particle[key]);
            this.particlePool.push(particle);
        }
    }

    // Adjust quality based on performance
    adjustQuality(fps) {
        if (fps < 30) {
            this.qualityLevel = 'low';
            this.maxParticles = 50;
        } else if (fps < 45) {
            this.qualityLevel = 'medium';
            this.maxParticles = 100;
        } else {
            this.qualityLevel = 'high';
            this.maxParticles = 200;
        }
    }

    // Quality-based particle spawning
    shouldSpawnParticle(importance = 'normal') {
        if (this.qualityLevel === 'low') {
            return importance === 'high' && Math.random() < 0.3;
        } else if (this.qualityLevel === 'medium') {
            return importance === 'high' || Math.random() < 0.5;
        }
        return true;
    }
}
```

### Accessibility: Reduced Motion Support

```javascript
// Respect user's motion preferences
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

class AccessibleAnimations {
    constructor(reducedMotion = prefersReducedMotion) {
        this.reducedMotion = reducedMotion;
    }

    adaptAnimation(animation) {
        if (!this.reducedMotion) return animation;

        // Simplified animations for reduced motion
        return {
            ...animation,
            duration: animation.duration * 0.5, // Faster
            particles: Math.floor((animation.particles || 0) * 0.3), // Fewer particles
            shake: Math.min(animation.shake || 0, 2), // Less shake
            flash: false // No flashing
        };
    }

    shouldAnimate(type) {
        if (!this.reducedMotion) return true;

        // Only allow essential animations
        const essentialTypes = ['damage', 'hp', 'status'];
        return essentialTypes.includes(type);
    }
}
```

---

## 7. Code Integration Guide

### Step 1: Add Animation Engine to Game Class

```javascript
class Game {
    constructor() {
        // ... existing code ...

        // Add animation systems
        this.animEngine = new BattleAnimationEngine(this);
        this.screenEffects = new ScreenEffects(this.canvas, this.ctx);
        this.optimizer = new AnimationOptimizer();
        this.accessibleAnims = new AccessibleAnimations();

        // Animation state
        this.animating = false;
        this.animationQueue = [];
    }

    // Modified update loop
    update() {
        const deltaTime = 16; // ~60fps

        // Update animations
        if (this.animEngine) {
            this.animEngine.update(deltaTime);
        }

        // Update screen effects
        if (this.screenEffects) {
            this.screenEffects.update(deltaTime);
        }

        // ... existing game logic ...
    }

    // Modified render loop
    render() {
        // ... existing rendering ...

        // Render animations
        if (this.animEngine) {
            this.animEngine.render();
        }

        // Apply screen effects
        if (this.screenEffects) {
            this.screenEffects.render();
        }
    }
}
```

### Step 2: Integrate with Battle System

```javascript
// In executeMove function
executeMove(attacker, defender, moveId, isPlayer) {
    const move = this.cartridge.moves[moveId];
    if (!move) return;

    // Deduct PP
    attacker.pp[moveId]--;

    // Show move text
    this.showText(`${attacker.name} used ${move.name}!`);

    // NEW: Play move animation
    this.playMoveAnimation(move, attacker, defender).then(() => {
        // Calculate damage (existing code)
        if (move.power > 0) {
            const damage = this.calculateDamage(attacker, defender, move);
            defender.hp = Math.max(0, defender.hp - damage);

            // NEW: Show damage number
            this.animEngine.showDamageNumber(
                defender.x,
                defender.y,
                damage,
                this.wasCritical,
                this.effectiveness
            );

            // NEW: Show effectiveness indicator
            if (this.effectiveness !== 1.0) {
                this.animEngine.showEffectivenessIndicator(
                    defender.x,
                    defender.y,
                    this.effectiveness
                );
            }

            this.updateBattleUI();
        }

        // Continue battle logic...
    });
}

// NEW: Move animation dispatcher
playMoveAnimation(move, attacker, defender) {
    const animName = `animate${this.toPascalCase(move.id)}`;

    if (typeof this[animName] === 'function') {
        return this[animName](attacker, defender);
    } else {
        // Default animation
        return this.animateDefaultAttack(attacker, defender);
    }
}

toPascalCase(str) {
    return str.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join('');
}
```

---

## 8. Testing Checklist

- [ ] All 50+ move animations working correctly
- [ ] Particle system performs well (60fps)
- [ ] Screen shake intensity feels appropriate
- [ ] Damage numbers are readable
- [ ] Type effectiveness indicators are clear
- [ ] HP bars animate smoothly
- [ ] Status effects have clear visual indicators
- [ ] Battle transitions are smooth
- [ ] Reduced motion mode works correctly
- [ ] No memory leaks in particle system
- [ ] Animations work on mobile devices
- [ ] Sound effects sync with animations
- [ ] Critical hits feel impactful
- [ ] Miss animations are clear
- [ ] Weather effects persist properly

---

## 9. Future Enhancements

### Advanced Features
1. **Combo Animations**: Chain moves with unique combination effects
2. **Terrain-Based Effects**: Different animations based on battle location
3. **Z-Moves/Mega Evolution**: Special transformation animations
4. **Camera Angles**: Dynamic camera movement during special moves
5. **Slow Motion**: Dramatic slow-mo for critical moments
6. **Replay System**: Record and replay epic battles
7. **Custom Animation Editor**: Let players create move animations
8. **Animated Backgrounds**: Dynamic battle backgrounds
9. **Weather Particle Systems**: Environmental effects
10. **Achievement Unlocks**: Special animations for milestones

---

## Summary

This comprehensive visual/UX design plan transforms WoWMon from a functional game into a visually stunning experience. The animation system provides:

- **50+ unique move animations** across all types
- **Rich particle effects** for every move
- **Dynamic camera effects** (shake, flash, zoom)
- **Floating damage numbers** with type indicators
- **Smooth UI transitions** and menu animations
- **Enhanced creature sprites** with idle animations
- **Status effect visualizations** with particles
- **Performance optimization** for mobile devices
- **Accessibility support** with reduced motion mode

The modular architecture allows easy addition of new moves and effects, while the optimization systems ensure smooth performance even with complex particle effects.

**Total Development Time Estimate**: 5 weeks
**Lines of Code Added**: ~3,000-4,000 lines
**Visual Impact**: Transforms static battles into cinema-quality experiences

File locations for integration:
- **/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html** - Main integration point
- All code is designed to work inline within the existing HTML structure
- No external dependencies required (stays true to local-first philosophy)
