# WoWMon Animation System - Quick Reference Guide

## Quick Start

### 1. Adding a New Move Animation

```javascript
// In Game class, add new animation method
animateYourMoveName(attacker, defender) {
    const anim = this.animEngine;

    // Step 1: Charge/windup
    attacker.playAnimation('attack');

    // Step 2: Create effect
    anim.createParticle({
        x: attacker.x,
        y: attacker.y,
        vx: 2, vy: -1,
        color: '#ff0000',
        size: 3,
        life: 1.0
    });

    // Step 3: Impact
    anim.shake(5, 200);
    defender.playAnimation('hurt');

    // Step 4: Return to idle
    return anim.wait(500);
}
```

### 2. Common Animation Patterns

#### Pattern A: Projectile Attack
```javascript
// Fire projectile from attacker to defender
await anim.queueAnimation({
    type: 'projectile',
    from: { x: attacker.x, y: attacker.y },
    to: { x: defender.x, y: defender.y },
    particle: { color: '#ff0000', size: 6 },
    duration: 400
});
```

#### Pattern B: Beam Attack
```javascript
// Sustained beam between attacker and defender
await anim.queueAnimation({
    type: 'beam',
    from: { x: attacker.x, y: attacker.y },
    to: { x: defender.x, y: defender.y },
    color: '#00ff00',
    width: 15,
    glow: true,
    duration: 600
});
```

#### Pattern C: Area Effect
```javascript
// Explosion/burst around target
for (let i = 0; i < 20; i++) {
    anim.createParticle({
        x: defender.x,
        y: defender.y,
        vx: Math.cos(i / 20 * Math.PI * 2) * 3,
        vy: Math.sin(i / 20 * Math.PI * 2) * 3,
        color: '#ffff00',
        size: 3,
        life: 0.8
    });
}
anim.shake(8, 400);
```

#### Pattern D: Status Effect
```javascript
// Apply lingering effect over time
for (let i = 0; i < 30; i++) {
    setTimeout(() => {
        anim.createParticle({
            x: defender.x + (Math.random() - 0.5) * 30,
            y: defender.y + (Math.random() - 0.5) * 30,
            vx: 0, vy: 0.5,
            color: '#800080',
            size: 2,
            life: 1.5,
            alpha: 0.6
        });
    }, i * 50);
}
```

---

## Animation Building Blocks

### Particles

```javascript
// Basic particle
anim.createParticle({
    x: 100,           // X position
    y: 100,           // Y position
    vx: 2,            // X velocity
    vy: -1,           // Y velocity
    ax: 0,            // X acceleration (default: 0)
    ay: 0.1,          // Y acceleration/gravity (default: 0.1)
    color: '#ff0000', // Color
    size: 3,          // Size in pixels
    life: 1.0,        // Lifespan (1.0 = full, 0 = dead)
    decay: 0.02,      // Life decay per frame
    alpha: 1.0,       // Opacity
    type: 'circle',   // circle, square, diamond, star, line, spark
    rotation: 0,      // Rotation in radians
    rotationSpeed: 0  // Rotation speed
});
```

### Screen Effects

```javascript
// Shake
anim.shake(intensity, duration);
// Examples:
anim.shake(5, 200);   // Light shake
anim.shake(10, 400);  // Medium shake
anim.shake(20, 800);  // Heavy shake

// Flash
anim.flash(color, opacity, duration);
// Examples:
anim.flash('#ffffff', 0.5, 200);  // White flash
anim.flash('#ff0000', 0.4, 300);  // Red tint
anim.flash('#000000', 0.6, 400);  // Darken

// Damage number
anim.showDamageNumber(x, y, damage, isCritical, effectiveness);
// Examples:
anim.showDamageNumber(defender.x, defender.y, 42, false, 1.0);
anim.showDamageNumber(defender.x, defender.y, 68, true, 2.0);
```

### Creature Animations

```javascript
// Play creature animation state
creature.playAnimation('idle');    // Breathing/bobbing
creature.playAnimation('attack');  // Lunge forward
creature.playAnimation('hurt');    // Recoil/shake
creature.playAnimation('faint');   // Collapse
creature.playAnimation('victory'); // Celebrate
```

---

## Color Palettes by Type

```javascript
const TYPE_COLORS = {
    fire: ['#ff0000', '#ff4500', '#ffa500', '#ffff00'],
    water: ['#0080ff', '#00bfff', '#87ceeb', '#e0ffff'],
    nature: ['#228b22', '#32cd32', '#90ee90', '#98fb98'],
    electric: ['#ffff00', '#ffd700', '#ffffe0', '#fffacd'],
    ice: ['#00ffff', '#87ceeb', '#add8e6', '#e0ffff'],
    dragon: ['#ff00ff', '#9370db', '#8a2be2', '#4b0082'],
    shadow: ['#000000', '#4b0082', '#8b00ff', '#9370db'],
    poison: ['#800080', '#9370db', '#8b008b', '#dda0dd'],
    psychic: ['#ff1493', '#ff69b4', '#da70d6', '#ee82ee'],
    normal: ['#ffffff', '#f0f0f0', '#d3d3d3', '#c0c0c0']
};
```

---

## Timing Guidelines

### Animation Durations

```javascript
// Fast attacks (Quick Attack, Scratch)
charge: 100ms
travel: 200ms
impact: 100ms
total: ~400ms

// Normal attacks (Tackle, Bite)
charge: 200ms
travel: 400ms
impact: 200ms
total: ~800ms

// Powerful attacks (Earthquake, Hydro Pump)
charge: 500ms
effect: 800ms
impact: 400ms
total: ~1700ms

// Ultimate moves (Hyper Beam, Explosion)
charge: 1000ms
effect: 1500ms
impact: 800ms
total: ~3300ms

// Status moves (Will-O-Wisp, Sleep Powder)
effect: 1000-1500ms
```

### Frame Timing

```javascript
// Standard timing
await anim.wait(100);  // Very short
await anim.wait(300);  // Short
await anim.wait(600);  // Medium
await anim.wait(1000); // Long
await anim.wait(2000); // Very long
```

---

## Effect Intensity Guidelines

### Particle Counts

```javascript
// Weak moves
particles: 8-12

// Normal moves
particles: 15-25

// Strong moves
particles: 30-50

// Ultimate moves
particles: 60-100+
```

### Shake Intensity

```javascript
// Light hit
anim.shake(3, 150);

// Normal hit
anim.shake(5, 250);

// Heavy hit
anim.shake(8, 400);

// Devastating hit
anim.shake(12, 600);

// Catastrophic
anim.shake(20, 1000);
```

### Flash Opacity

```javascript
// Subtle
anim.flash(color, 0.2, duration);

// Noticeable
anim.flash(color, 0.4, duration);

// Strong
anim.flash(color, 0.6, duration);

// Intense
anim.flash(color, 0.8, duration);

// Overwhelming
anim.flash(color, 1.0, duration);
```

---

## Move Animation Checklist

When creating a new move animation, ensure:

- [ ] Charge/windup phase (attacker animation)
- [ ] Visual effect (particles, beams, projectiles)
- [ ] Travel time (if applicable)
- [ ] Impact effect (shake, flash, particles)
- [ ] Defender reaction (hurt animation)
- [ ] Sound sync point (note when to play SFX)
- [ ] Return to idle
- [ ] Appropriate timing for move power
- [ ] Type-appropriate colors
- [ ] Accessibility consideration (reduced motion)

---

## Animation Patterns by Move Type

### Physical Contact Moves
1. Attacker slides toward defender
2. Impact particles at contact point
3. Shake camera
4. Defender recoils
5. Attacker returns to position

**Examples**: Tackle, Slash, Crunch, Body Slam

### Projectile Moves
1. Charging particles around attacker
2. Projectile travels to defender
3. Trail effect behind projectile
4. Explosion on impact
5. Defender hurt animation

**Examples**: Ember, Water Gun, Shadow Ball

### Beam Moves
1. Energy gathers at attacker
2. Sustained beam from attacker to defender
3. Particles along beam
4. Strong shake during beam
5. Flash on impact

**Examples**: Hyper Beam, Solar Beam, Ice Beam

### Area Effect Moves
1. Warning indicators
2. Effect spreads across area
3. Multiple hit points
4. Sustained shake
5. Lingering particles

**Examples**: Earthquake, Explosion, Sandstorm

### Status Moves
1. Mystical particle formation
2. Particles travel to target
3. Effect settles on target
4. Status icon appears
5. Lingering status particles

**Examples**: Will-O-Wisp, Sleep Powder, Thunder Wave

### Buff/Debuff Moves
1. Aura emanates from user
2. Geometric shapes form
3. Pulsing rings expand
4. Stat change indicator
5. Persistent glow effect

**Examples**: Barrier, Battle Cry, Howl

---

## Performance Tips

### Optimize Particle Count
```javascript
// Instead of:
for (let i = 0; i < 100; i++) {
    createParticle(...);
}

// Use quality settings:
const count = this.optimizer.qualityLevel === 'high' ? 100 :
              this.optimizer.qualityLevel === 'medium' ? 50 : 25;
for (let i = 0; i < count; i++) {
    createParticle(...);
}
```

### Batch Similar Operations
```javascript
// Instead of many setTimeout calls:
for (let i = 0; i < 50; i++) {
    setTimeout(() => createParticle(...), i * 20);
}

// Batch in animation queue:
const animation = {
    duration: 1000,
    update: (progress) => {
        if (progress * 50 > lastSpawned) {
            createParticle(...);
            lastSpawned++;
        }
    }
};
```

### Reuse Particle Objects
```javascript
// Use object pooling
const particle = this.optimizer.getParticle();
Object.assign(particle, {
    x: 100, y: 100,
    // ... other properties
});

// Later, when particle dies:
this.optimizer.releaseParticle(particle);
```

---

## Debugging

### Log Animation Events
```javascript
animateMove(attacker, defender) {
    console.log('[ANIM START]', move.name);

    // ... animation code ...

    console.log('[ANIM END]', move.name);
}
```

### Visualize Hit Boxes
```javascript
// In render function
if (DEBUG_MODE) {
    ctx.strokeStyle = '#00ff00';
    ctx.strokeRect(creature.x - 20, creature.y - 20, 40, 40);
}
```

### Slow Motion Mode
```javascript
// For testing animations
const DEBUG_SLOW_MOTION = false;
const deltaTime = DEBUG_SLOW_MOTION ? 16 * 0.5 : 16;
```

---

## Common Issues & Solutions

### Issue: Particles Not Appearing
**Solution**: Check particle lifecycle
```javascript
// Ensure life > 0
particle.life = 1.0;
particle.decay = 0.02; // Decays over time

// Check render is being called
if (particle.life > 0) {
    renderParticle(particle);
}
```

### Issue: Animation Too Fast/Slow
**Solution**: Adjust timing
```javascript
// Too fast? Increase duration
await anim.wait(600); // instead of 200

// Too slow? Decrease duration or parallelize
Promise.all([
    animation1(),
    animation2()
]); // Run simultaneously
```

### Issue: Screen Shake Too Intense
**Solution**: Scale by power level
```javascript
const baseShake = 5;
const shakeIntensity = baseShake * (move.power / 100);
anim.shake(shakeIntensity, 300);
```

### Issue: Memory Leak
**Solution**: Clean up animations
```javascript
// Remove completed animations
this.activeAnimations = this.activeAnimations.filter(a => !a.complete);

// Limit particle count
if (this.particles.length > MAX_PARTICLES) {
    this.particles = this.particles.slice(-MAX_PARTICLES);
}
```

---

## Code Snippets

### Lightning Path Generator
```javascript
generateLightningPath(start, end, segments) {
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
```

### Arc Path Generator (for thrown projectiles)
```javascript
createArcPath(start, end, height, segments = 20) {
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
```

### Orbit Pattern
```javascript
createOrbitParticles(center, radius, count, color) {
    for (let i = 0; i < count; i++) {
        const angle = (i / count) * Math.PI * 2;
        anim.createParticle({
            x: center.x + Math.cos(angle) * radius,
            y: center.y + Math.sin(angle) * radius,
            vx: -Math.sin(angle) * 2,
            vy: Math.cos(angle) * 2,
            color: color,
            size: 2,
            life: 1.0
        });
    }
}
```

### Spiral Pattern
```javascript
createSpiralParticles(center, maxRadius, rotations, count, color) {
    for (let i = 0; i < count; i++) {
        const t = i / count;
        const angle = t * rotations * Math.PI * 2;
        const radius = t * maxRadius;
        anim.createParticle({
            x: center.x + Math.cos(angle) * radius,
            y: center.y + Math.sin(angle) * radius,
            color: color,
            size: 2,
            life: 1.0
        });
    }
}
```

---

## Testing Your Animation

1. **Visual Test**: Does it look good?
   - Clear impact moment
   - Appropriate particle count
   - Good color choice for type
   - Readable damage numbers

2. **Timing Test**: Does it feel right?
   - Not too fast (< 200ms total)
   - Not too slow (> 5s total)
   - Matches move power level
   - Syncs with audio

3. **Performance Test**: Does it run smoothly?
   - 60 FPS on target device
   - No memory leaks
   - Particle count reasonable
   - Object pooling working

4. **Accessibility Test**: Is it accessible?
   - Works with reduced motion
   - No seizure-inducing flashing
   - Clear without relying on color alone
   - Sound alternatives available

---

## Reference: All 50+ Moves Covered

### Physical (15)
- Tackle, Quick Attack, Slash, Crunch, Body Slam
- Earthquake, Dig, Wing Attack, Aerial Ace
- Dragon Claw, Shadow Claw, Ice Fang, Poison Jab
- Wood Hammer, Stomp

### Fire (8)
- Ember, Firebolt, Flame Burst, Flame Strike
- Inferno, Meteor Strike, Immolate, Sacred Fire

### Water (7)
- Bubble, Water Gun, Water Pulse, Scald
- Hydro Pump, Tidal Wave, Ice Beam

### Electric (5)
- Spark, Thunder Wave, Lightning Bolt
- Discharge, Thunderbolt

### Nature/Grass (6)
- Vine Whip, Magical Leaf, Energy Ball
- Solar Beam, Wood Hammer, Synthesis

### Ice (5)
- Ice Shard, Frost Shock, Ice Fang
- Ice Beam, Blizzard

### Dragon (4)
- Dragon Breath, Dragon Rage, Dragon Claw, Outrage

### Shadow/Dark (5)
- Shadow Ball, Dark Pulse, Shadow Claw
- Curse, Possession

### Poison (5)
- Poison Sting, Toxic, Poison Jab
- Sludge Bomb, Toxic Bite

### Psychic/Magic (5)
- Psychic, Confusion, Barrier
- Cosmic Power, Teleport

### Status Moves (8)
- Will-O-Wisp, Sleep Powder, Thunder Wave
- Toxic, Spore, Ice Shard (freeze)
- Howl, Battle Cry

### Weather (4)
- Sunny Day, Rain Dance, Sandstorm, Hail

### Ultimate (3)
- Hyper Beam, Explosion, Outrage

---

## Quick Command Reference

```javascript
// Particle
anim.createParticle({ x, y, vx, vy, color, size, life });

// Shake
anim.shake(intensity, duration);

// Flash
anim.flash(color, opacity, duration);

// Damage
anim.showDamageNumber(x, y, damage, critical, effectiveness);

// Wait
await anim.wait(milliseconds);

// Queue
await anim.queueAnimation({ type, ...config });

// Creature
creature.playAnimation('idle' | 'attack' | 'hurt' | 'faint' | 'victory');
```

---

## Additional Resources

- Main Plan: `/WOWMON_VISUAL_UX_DESIGN_PLAN.md`
- Integration File: `/wowMon.html`
- Type Effectiveness: See cartridge data
- Sound Effects: See audio manager

**Happy Animating!** 🎨✨
