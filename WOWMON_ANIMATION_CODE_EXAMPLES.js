/**
 * WoWMon Battle Animation System - Code Examples
 * Ready-to-use animation implementations
 *
 * Usage: Copy these into your wowMon.html Game class
 */

// ============================================================================
// CORE ANIMATION ENGINE
// ============================================================================

class BattleAnimationEngine {
    constructor(game) {
        this.game = game;
        this.ctx = game.ctx;
        this.canvas = game.canvas;
        this.activeAnimations = [];
        this.particles = [];
        this.screenShake = { x: 0, y: 0, intensity: 0, duration: 0, elapsed: 0 };
        this.flashEffect = { color: null, opacity: 0, duration: 0, elapsed: 0 };
        this.damageNumbers = [];
        this.banners = [];
        this.statusIcons = [];
    }

    update(deltaTime) {
        this.updateParticles(deltaTime);
        this.updateAnimations(deltaTime);
        this.updateScreenShake(deltaTime);
        this.updateFlashEffects(deltaTime);
        this.updateDamageNumbers(deltaTime);
        this.updateBanners(deltaTime);
    }

    updateParticles(deltaTime) {
        this.particles = this.particles.filter(particle => {
            // Apply physics
            particle.vx += particle.ax || 0;
            particle.vy += particle.ay || 0.1; // gravity
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Update life
            particle.life -= particle.decay || 0.02;

            // Update rotation
            if (particle.rotationSpeed) {
                particle.rotation = (particle.rotation || 0) + particle.rotationSpeed;
            }

            return particle.life > 0;
        });
    }

    updateAnimations(deltaTime) {
        this.activeAnimations = this.activeAnimations.filter(anim => {
            anim.elapsed = (anim.elapsed || 0) + deltaTime;
            const progress = Math.min(anim.elapsed / anim.duration, 1);

            if (anim.update) {
                anim.update(progress);
            }

            if (progress >= 1) {
                if (anim.onComplete) anim.onComplete();
                return false;
            }
            return true;
        });
    }

    updateScreenShake(deltaTime) {
        if (this.screenShake.duration > 0) {
            this.screenShake.elapsed += deltaTime;
            const progress = this.screenShake.elapsed / this.screenShake.duration;

            if (progress >= 1) {
                this.screenShake = { x: 0, y: 0, intensity: 0, duration: 0, elapsed: 0 };
            } else {
                const intensity = this.screenShake.intensity * (1 - progress);
                this.screenShake.x = (Math.random() - 0.5) * intensity;
                this.screenShake.y = (Math.random() - 0.5) * intensity;
            }
        }
    }

    updateFlashEffects(deltaTime) {
        if (this.flashEffect.duration > 0) {
            this.flashEffect.elapsed += deltaTime;
            const progress = this.flashEffect.elapsed / this.flashEffect.duration;

            if (progress >= 1) {
                this.flashEffect = { color: null, opacity: 0, duration: 0, elapsed: 0 };
            }
        }
    }

    updateDamageNumbers(deltaTime) {
        this.damageNumbers = this.damageNumbers.filter(dmg => {
            dmg.y += dmg.vy;
            dmg.vy += 0.05; // gravity
            dmg.life -= 0.02;
            return dmg.life > 0;
        });
    }

    updateBanners(deltaTime) {
        this.banners = this.banners.filter(banner => {
            banner.life -= 0.02;
            banner.scale = Math.min(banner.scale + 0.1, 1.0);
            banner.y -= 0.5;
            return banner.life > 0;
        });
    }

    render() {
        this.ctx.save();

        // Apply screen shake
        if (this.screenShake.intensity > 0) {
            this.ctx.translate(this.screenShake.x, this.screenShake.y);
        }

        // Render particles
        this.particles.forEach(p => this.renderParticle(p));

        // Render damage numbers
        this.damageNumbers.forEach(dmg => this.renderDamageNumber(dmg));

        // Render banners
        this.banners.forEach(b => this.renderBanner(b));

        this.ctx.restore();

        // Render flash (on top of everything)
        if (this.flashEffect.opacity > 0) {
            const progress = this.flashEffect.elapsed / this.flashEffect.duration;
            this.ctx.fillStyle = this.flashEffect.color;
            this.ctx.globalAlpha = this.flashEffect.opacity * (1 - progress);
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.globalAlpha = 1;
        }
    }

    renderParticle(particle) {
        this.ctx.save();
        this.ctx.globalAlpha = particle.life * (particle.alpha || 1);

        switch(particle.type || 'circle') {
            case 'circle':
                this.ctx.fillStyle = particle.color;
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.ctx.fill();
                break;

            case 'square':
                this.ctx.translate(particle.x, particle.y);
                this.ctx.rotate(particle.rotation || 0);
                this.ctx.fillStyle = particle.color;
                this.ctx.fillRect(-particle.size/2, -particle.size/2, particle.size, particle.size);
                break;

            case 'diamond':
                this.ctx.translate(particle.x, particle.y);
                this.ctx.rotate(particle.rotation || 0);
                this.ctx.beginPath();
                this.ctx.moveTo(0, -particle.size);
                this.ctx.lineTo(particle.size, 0);
                this.ctx.lineTo(0, particle.size);
                this.ctx.lineTo(-particle.size, 0);
                this.ctx.closePath();
                this.ctx.fillStyle = particle.color;
                this.ctx.fill();
                break;

            case 'line':
                this.ctx.translate(particle.x, particle.y);
                this.ctx.rotate(Math.atan2(particle.vy, particle.vx));
                this.ctx.strokeStyle = particle.color;
                this.ctx.lineWidth = particle.size;
                this.ctx.beginPath();
                this.ctx.moveTo(0, 0);
                this.ctx.lineTo(particle.lineLength || 6, 0);
                this.ctx.stroke();
                break;
        }

        this.ctx.restore();
    }

    renderDamageNumber(dmg) {
        this.ctx.save();
        this.ctx.globalAlpha = dmg.life;
        this.ctx.font = `${12 * dmg.scale}px monospace`;
        this.ctx.fillStyle = dmg.color;
        this.ctx.strokeStyle = '#000000';
        this.ctx.lineWidth = 3;
        this.ctx.textAlign = 'center';
        this.ctx.strokeText(dmg.text, dmg.x, dmg.y);
        this.ctx.fillText(dmg.text, dmg.x, dmg.y);
        this.ctx.restore();
    }

    renderBanner(banner) {
        this.ctx.save();
        this.ctx.globalAlpha = banner.life;
        this.ctx.translate(banner.x, banner.y);
        this.ctx.scale(banner.scale, banner.scale);

        // Background
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(-60, -12, 120, 24);

        // Border
        this.ctx.strokeStyle = banner.color;
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(-60, -12, 120, 24);

        // Text
        this.ctx.font = '10px monospace';
        this.ctx.fillStyle = banner.color;
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`${banner.icon} ${banner.text} ${banner.icon}`, 0, 4);

        this.ctx.restore();
    }

    // Public API methods
    createParticle(config) {
        this.particles.push({
            x: config.x,
            y: config.y,
            vx: config.vx || 0,
            vy: config.vy || 0,
            ax: config.ax || 0,
            ay: config.ay !== undefined ? config.ay : 0.1,
            size: config.size || 2,
            color: config.color || '#fff',
            life: config.life || 1.0,
            decay: config.decay || 0.02,
            type: config.type || 'circle',
            rotation: config.rotation || 0,
            rotationSpeed: config.rotationSpeed || 0,
            alpha: config.alpha || 1,
            lineLength: config.lineLength
        });
    }

    shake(intensity = 5, duration = 300) {
        this.screenShake = {
            x: 0, y: 0,
            intensity,
            duration,
            elapsed: 0
        };
    }

    flash(color = '#ffffff', opacity = 0.5, duration = 200) {
        this.flashEffect = {
            color,
            opacity,
            duration,
            elapsed: 0
        };
    }

    showDamageNumber(x, y, damage, isCritical = false, effectiveness = 1.0) {
        let color = '#ffffff';
        let scale = 1.0;
        let text = damage.toString();

        if (isCritical) {
            color = '#ffff00';
            scale = 1.5;
            text = `${damage}!`;
        } else if (effectiveness > 1.5) {
            color = '#4ade80';
            scale = 1.3;
        } else if (effectiveness < 0.75 && effectiveness > 0) {
            color = '#94a3b8';
            scale = 0.8;
        }

        this.damageNumbers.push({
            x, y,
            text,
            color,
            scale,
            life: 1.0,
            vy: -2,
            decay: 0.02
        });
    }

    showEffectivenessIndicator(x, y, effectiveness) {
        const messages = {
            0: { text: "NO EFFECT", color: '#6b7280', icon: '✕' },
            0.5: { text: "NOT VERY EFFECTIVE", color: '#cbd5e1', icon: '▼' },
            2.0: { text: "SUPER EFFECTIVE", color: '#4ade80', icon: '▲' }
        };

        const msg = messages[effectiveness];
        if (!msg) return;

        this.banners.push({
            x: this.canvas.width / 2,
            y: y - 30,
            text: msg.text,
            color: msg.color,
            icon: msg.icon,
            life: 1.0,
            scale: 0
        });
    }

    queueAnimation(config) {
        return new Promise(resolve => {
            this.activeAnimations.push({
                ...config,
                elapsed: 0,
                onComplete: resolve
            });
        });
    }

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ============================================================================
// EXAMPLE MOVE ANIMATIONS
// ============================================================================

// TACKLE - Simple physical attack
function animateTackle(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // 1. Dash forward
        const originalX = attacker.x;
        const targetX = defender.x - 20;

        await anim.queueAnimation({
            duration: 200,
            update: (progress) => {
                attacker.x = originalX + (targetX - originalX) * progress;
            }
        });

        // 2. Impact
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

        // 3. Return
        await anim.queueAnimation({
            duration: 200,
            update: (progress) => {
                attacker.x = targetX + (originalX - targetX) * progress;
            }
        });
    })();
}

// EMBER - Fire projectile
function animateEmber(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // 1. Charge up
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

        // 2. Fire projectile
        let projectileX = attacker.x;
        let projectileY = attacker.y;
        const trail = [];

        await anim.queueAnimation({
            duration: 400,
            update: (progress) => {
                projectileX = attacker.x + (defender.x - attacker.x) * progress;
                projectileY = attacker.y + (defender.y - attacker.y) * progress;

                // Create trail
                if (Math.random() < 0.5) {
                    anim.createParticle({
                        x: projectileX,
                        y: projectileY,
                        vx: (Math.random() - 0.5),
                        vy: (Math.random() - 0.5),
                        color: '#ffa500',
                        size: 3,
                        life: 0.3
                    });
                }
            }
        });

        // 3. Explosion
        anim.shake(5, 200);
        anim.flash('#ff4500', 0.4, 150);

        for (let i = 0; i < 20; i++) {
            const angle = (i / 20) * Math.PI * 2;
            anim.createParticle({
                x: defender.x,
                y: defender.y,
                vx: Math.cos(angle) * 3,
                vy: Math.sin(angle) * 3,
                color: ['#ff0000', '#ff4500', '#ffa500', '#ffff00'][Math.floor(Math.random() * 4)],
                size: 3,
                life: 0.8
            });
        }
    })();
}

// WATER GUN - Rapid water projectiles
function animateWaterGun(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // Stream of water bubbles
        for (let i = 0; i < 10; i++) {
            setTimeout(() => {
                let bubbleX = attacker.x;
                let bubbleY = attacker.y;

                anim.queueAnimation({
                    duration: 300,
                    update: (progress) => {
                        bubbleX = attacker.x + (defender.x - attacker.x) * progress;
                        bubbleY = attacker.y + (defender.y - attacker.y) * progress;
                    }
                }).then(() => {
                    // Splash on impact
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
                });
            }, i * 100);
        }

        anim.shake(3, 500);
        await anim.wait(1200);
    })();
}

// THUNDER WAVE - Electric paralysis
function animateThunderWave(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // 1. Charge
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

        // 2. Lightning bolt
        const segments = 10;
        const path = [];
        for (let i = 0; i <= segments; i++) {
            const t = i / segments;
            const x = attacker.x + (defender.x - attacker.x) * t + (Math.random() - 0.5) * 15;
            const y = attacker.y + (defender.y - attacker.y) * t + (Math.random() - 0.5) * 15;
            path.push({ x, y });
        }

        // Draw lightning
        for (let flash = 0; flash < 3; flash++) {
            setTimeout(() => {
                anim.flash('#ffff00', 0.5, 100);

                for (let i = 0; i < path.length - 1; i++) {
                    const p1 = path[i];
                    const p2 = path[i + 1];

                    // Create line particles
                    const steps = 5;
                    for (let j = 0; j < steps; j++) {
                        const t = j / steps;
                        anim.createParticle({
                            x: p1.x + (p2.x - p1.x) * t,
                            y: p1.y + (p2.y - p1.y) * t,
                            vx: 0,
                            vy: 0,
                            color: '#ffff00',
                            size: 2,
                            life: 0.2
                        });
                    }
                }
            }, flash * 150);
        }

        // 3. Electric sparks
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

        await anim.wait(500);
    })();
}

// EARTHQUAKE - Ground shaking attack
function animateEarthquake(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // 1. Charge
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const angle = (i / 20) * Math.PI * 2;
                anim.createParticle({
                    x: attacker.x + Math.cos(angle) * 20,
                    y: attacker.y + 20,
                    vx: 0,
                    vy: -1,
                    color: '#8b4513',
                    size: 3,
                    life: 0.5
                });
            }, i * 30);
        }

        await anim.wait(600);

        // 2. MASSIVE SHAKE
        anim.shake(12, 1000);

        // 3. Ground cracks
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

        await anim.wait(1200);
    })();
}

// HYPER BEAM - Ultimate attack
function animateHyperBeam(attacker, defender) {
    const anim = this.animEngine;

    return (async () => {
        // 1. Massive charge
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
                const angle = (i / 20) * Math.PI * 2;
                anim.createParticle({
                    x: attacker.x + Math.cos(angle) * (40 - i * 2),
                    y: attacker.y + Math.sin(angle) * (40 - i * 2),
                    vx: 0,
                    vy: 0,
                    color: '#ffff00',
                    size: 3,
                    life: 0.1
                });
            }, i * 30);
        }

        await anim.wait(600);

        // 3. BEAM!
        anim.shake(20, 1500);
        anim.flash('#ffffff', 0.8, 200);

        // Create beam effect
        for (let frame = 0; frame < 60; frame++) {
            setTimeout(() => {
                // Beam particles
                const steps = 20;
                for (let i = 0; i < steps; i++) {
                    const t = i / steps;
                    const x = attacker.x + (defender.x - attacker.x) * t;
                    const y = attacker.y + (defender.y - attacker.y) * t;

                    anim.createParticle({
                        x: x + (Math.random() - 0.5) * 15,
                        y: y + (Math.random() - 0.5) * 15,
                        vx: (Math.random() - 0.5) * 2,
                        vy: (Math.random() - 0.5) * 2,
                        color: ['#ffff00', '#ffffff'][Math.floor(Math.random() * 2)],
                        size: 4,
                        life: 0.3
                    });
                }
            }, frame * 20);
        }

        // 4. Explosion
        await anim.wait(800);

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

        // Shockwave rings
        for (let r = 20; r <= 100; r += 20) {
            setTimeout(() => {
                const angle = 0;
                for (let i = 0; i < 24; i++) {
                    const a = (i / 24) * Math.PI * 2;
                    anim.createParticle({
                        x: defender.x + Math.cos(a) * r,
                        y: defender.y + Math.sin(a) * r,
                        vx: Math.cos(a) * 2,
                        vy: Math.sin(a) * 2,
                        color: '#ffa500',
                        size: 3,
                        life: 0.5
                    });
                }
            }, (r - 20) * 40);
        }

        await anim.wait(2000);
    })();
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function generateLightningPath(start, end, segments) {
    const points = [start];
    for (let i = 1; i < segments; i++) {
        const t = i / segments;
        const x = start.x + (end.x - start.x) * t + (Math.random() - 0.5) * 15;
        const y = start.y + (end.y - start.y) * t + (Math.random() - 0.5) * 15;
        points.push({ x, y });
    }
    points.push(end);
    return points;
}

function createArcPath(start, end, height, segments = 20) {
    const points = [];
    for (let i = 0; i <= segments; i++) {
        const t = i / segments;
        const x = start.x + (end.x - start.x) * t;
        const parabola = 4 * height * t * (1 - t);
        const y = start.y + (end.y - start.y) * t - parabola;
        points.push({ x, y });
    }
    return points;
}

// ============================================================================
// INTEGRATION EXAMPLE
// ============================================================================

/*
// In Game class constructor:
this.animEngine = new BattleAnimationEngine(this);

// In Game update loop:
if (this.animEngine) {
    this.animEngine.update(deltaTime);
}

// In Game render loop (after drawing everything else):
if (this.animEngine) {
    this.animEngine.render();
}

// In executeMove function:
async executeMove(attacker, defender, moveId, isPlayer) {
    const move = this.cartridge.moves[moveId];
    if (!move) return;

    attacker.pp[moveId]--;
    this.showText(`${attacker.name} used ${move.name}!`);

    // Play animation
    const animName = `animate${this.toPascalCase(moveId)}`;
    if (typeof this[animName] === 'function') {
        await this[animName].call(this, attacker, defender);
    }

    // Calculate damage...
    if (move.power > 0) {
        const damage = this.calculateDamage(attacker, defender, move);
        defender.hp = Math.max(0, defender.hp - damage);

        // Show damage number
        this.animEngine.showDamageNumber(
            defender.x,
            defender.y,
            damage,
            this.wasCritical,
            this.effectiveness
        );

        // Show effectiveness
        if (this.effectiveness !== 1.0) {
            this.animEngine.showEffectivenessIndicator(
                defender.x,
                defender.y,
                this.effectiveness
            );
        }
    }

    this.updateBattleUI();
}

// Helper to convert move IDs to function names
toPascalCase(str) {
    return str.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join('');
}
*/

// ============================================================================
// EXPORT (for module systems)
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        BattleAnimationEngine,
        animateTackle,
        animateEmber,
        animateWaterGun,
        animateThunderWave,
        animateEarthquake,
        animateHyperBeam
    };
}
