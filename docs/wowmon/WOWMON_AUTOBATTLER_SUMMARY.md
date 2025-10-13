# WoWmon Auto-Battler Design - Implementation Summary

## 🎯 Project Overview

**Objective**: Transform wowMon.html from an active Pokemon-style adventure into a strategic auto-battler with idle game mechanics.

**Target Audience**: Casual players who want strategic depth without time commitment

**Core Philosophy**: Respect player time, reward strategy over grinding, provide months of engaging progression

---

## 🔄 Core Game Loop

```
Build Team → Auto-Battle → Collect Loot → Optimize → Progress → Prestige → Repeat
```

### The 3-Minute Session
1. Check progress (30s)
2. Collect offline loot (10s)
3. Adjust team for next boss (2m)
4. Buy upgrades (30s)
5. Done! Come back later

### The 10-Minute Session
- Complete daily quests
- Attempt boss fight
- Reorganize collection
- Plan prestige strategy

---

## 🎮 Core Systems

### 1. Auto-Battle System

**How It Works:**
- Team fights automatically 24/7
- Battles take 5-60 seconds depending on strength
- Smart AI selects moves based on type advantage, HP, buffs
- Progress through 100 stages (10 enemies per stage)
- Boss every 10 stages requires optimization

**Battle Resolution:**
```javascript
Every 0.5 seconds:
1. Check turn order (speed stat)
2. Active creature uses best move
3. Calculate damage with type effectiveness
4. Check for deaths/switches
5. Award XP/loot on victory
```

**Key Features:**
- Type-advantage detection
- Healing priority (< 30% HP)
- Buff timing (use early)
- PP conservation (don't overkill)

---

### 2. Team Synergies

**Why It Matters:**
Composition > Power Level. A well-synergized team of weak creatures beats a poorly composed team of strong ones.

**Type Synergies:**
- **Water Pack** (3+ Water): +25% Water damage
- **Demonic Pact** (2+ Demon): +20% attack on kill
- **Druidic Circle** (2+ Nature): Heal 5% HP/second
- **Undead Army** (3+ Undead): Revive once at 50% HP
- **Dragon Dominance** (2+ Dragon): +40% vs Dragons
- **Elemental Chaos** (4+ types): +15% all stats

**Role Synergies:**
- Tank + Healer: Tank -30% damage taken
- Double DPS: +15% attack speed
- Support + DPS: DPS +20% crit chance

**Evolution Synergies:**
- Full line (Murloc → Warrior → King): +30% XP
- All starters evolved: +50% gold

---

### 3. Offline Progression

**The Problem:** Players feel punished for not playing constantly

**Our Solution:**
```
Offline Time = Min(Time Away, 8 hours)
Offline Loot = (Battles Won × Resources) × 50%
Upgradeable to 100% offline efficiency
```

**Caps:**
- Base: 8 hours worth of loot
- Upgrades: 12h → 16h → 20h → 24h → 48h (prestige)

**Welcome Back Bonuses:**
- +50% XP/Gold for first 10 battles
- Rested XP: +20% per hour offline (max 200%)
- "Marathon Trainer" achievement (24h offline)

**Key Philosophy:**
- Never punish players for having a life
- Check-ins feel rewarding, not mandatory
- Long absences don't destroy progress

---

### 4. Prestige System (Ascension)

**Unlock:** Defeat Champion (Stage 100)

**What You Keep:**
- ✅ Ascension Tokens (spent on permanent upgrades)
- ✅ Collection (all creatures at level 1)
- ✅ Achievements
- ✅ Cosmetics

**What You Lose:**
- ❌ Levels (reset to 1)
- ❌ Stage progress (back to stage 1)
- ❌ Gold/consumables
- ❌ Team formation

**Token Calculation:**
```
Base = 100
Stage Bonus = Stage × 2
Achievement Bonus = Achievements × 10
Time Bonus = +50 if under 7 days
Collection Bonus = Unique Creatures × 5
```

**Permanent Upgrades:**

| Upgrade | Max Level | Effect | Total Cost |
|---------|-----------|--------|------------|
| Battle Speed | 5 | -10% battle time | 1,550 |
| Gold Mult | 4 | +25% gold | 1,500 |
| XP Boost | 4 | +20% XP | 1,200 |
| Offline Efficiency | 3 | +25% offline | 1,050 |
| Offline Cap | 3 | +4 hours | 1,400 |
| Starting Resources | 3 | Better start | 850 |
| Team Size | 3 | +1 slot (9 max) | 3,500 |
| Auto Evolution | 1 | Auto-evolve | 300 |
| Shiny Chance | 3 | 2×/4×/8× | 3,500 |
| Prestige Power | ∞ | +5% stats/ascension | 1,000 each |

**Strategy:**
- Ascension 1-3: Core upgrades (battle speed, gold, XP)
- Ascension 4-6: Optimization (offline, team size)
- Ascension 7+: Luxury (shiny hunting, challenge runs)

---

### 5. Collection System

**Catch Mechanics:**
- 5% base auto-catch rate
- Upgradeable: 5% → 10% → 20% → 35% → 50%
- Shiny chance: 1/500 (base)
- Unlimited storage

**Rarity System:**

| Rarity | Rate | Stat Bonus | Examples |
|--------|------|------------|----------|
| Common | 50% | +0% | Murloc, Imp, Wolf |
| Uncommon | 30% | +10% | Gnoll, Kobold, Skeleton |
| Rare | 15% | +25% | Naga, Treant, Whelp |
| Epic | 4% | +50% | Drake, Elemental, Dire Wolf |
| Legendary | 1% | +100% | Dragon, Phoenix, Infernal |

**Collection Bonuses:**
- Type Mastery: Catch all Water → +10% Water damage
- Evolution Master: Full line → +15% XP for that line
- Completionist: All 75 → Unlock Legendary Mode
- Shiny Hunter: 10 shinies → +50% shiny chance

---

### 6. Economy

**Resources:**
- **Gold** - Main currency (battles)
- **Essence** - Premium (bosses, 10% drop)
- **Fragments** - Evolution material (5% drop, type-specific)
- **Tokens** - Prestige currency (ascension)

**Income Rates:**
```
Gold Per Battle = 50 + (Stage × 5)
Early Game: ~2,000 gold/hour
Late Game: ~10,000 gold/hour

Essence: 1-3 per boss (10% drop rate)
Fragments: 5% per battle (type-specific)
```

**Gold Shop:**
- Health Potions: 100g (auto-heal)
- XP Boost (1h): 500g (2× XP)
- Gold Boost (1h): 500g (2× Gold)
- Catch Rate Upgrades: 1K/5K/25K/100K
- Team Slots: 10K/50K/250K (4→5→6)

**Essence Shop:**
- Instant Evolution: 10 Essence
- Shiny Charm: 25 Essence (guarantee next shiny)
- Boss Ticket: 5 Essence (retry immediately)
- Mega Evolution Stone: 100 Essence (power-up)

---

## 📊 Progression Timeline

| Milestone | Time | Unlock |
|-----------|------|--------|
| Stage 10 | 1-2 days | Synergies, Shop |
| First Evolution | 3-4 days | Fragments, Evolution bonuses |
| Stage 50 | 1-2 weeks | Rare creatures, New zones |
| Stage 100 (Champion) | 3-4 weeks | Prestige unlock |
| First Ascension | 1 month | Permanent bonuses |
| Complete Collection | 2-3 months | Master title |
| Ascension 10 | 3-4 months | Legendary creatures |
| 100% Completion | 6+ months | All achievements/shinies |

---

## 🎨 UI Design

### Main Screen
```
┌─────────────────────────────────────┐
│  [≡] WoWmon Auto-Battler    [💰12K]│
├─────────────────────────────────────┤
│  Stage 23 - Elwynn Forest      ⚔️   │
│  ┌─────────────────────────────┐   │
│  │  [Your Team] vs [Enemy]     │   │
│  │  🐸 🐺 🔥   vs   🕷️         │   │
│  │  HP █████░░  HP ███░░░       │   │
│  │  Murloc used Water Gun!     │   │
│  └─────────────────────────────┘   │
│  Progress: [████████░░] 8/10       │
│  ┌────────┐┌────────┐┌────────┐   │
│  │ Team  ││Collect││ Shop  │   │
│  └────────┘└────────┘└────────┘   │
│  Quick Stats:                      │
│  • Offline: 2h 34m (24,500g)       │
│  • Next Evo: Imp→Felguard (Lv18)   │
│  • Daily: 32/50 battles            │
└─────────────────────────────────────┘
```

### Team Builder
- Active team slots (3-6 creatures)
- Visual synergy indicators
- Collection browser with filters
- Quick stats comparison
- One-tap creature swap

### Prestige Screen
- Current run statistics
- Token calculation preview
- What you keep/lose
- Upgrade shop preview
- "Are you sure?" confirmation

---

## 💡 Implementation Priority

### Phase 1: MVP (Week 1-2)
**Goal:** Playable auto-battle loop

1. Auto-battle engine
   - Battle tick system (0.5s intervals)
   - Move selection AI
   - Damage calculation
   - Victory/defeat handling

2. Team management
   - Active team slots
   - Creature swapping
   - Basic stats display

3. Stage progression
   - 10 enemies per stage
   - Stage advancement
   - Difficulty scaling

4. Offline progress
   - Time calculation
   - Loot accumulation
   - Welcome back screen

**Success Metric:** Can leave game, come back, see progress

---

### Phase 2: Core Loop (Week 3-4)
**Goal:** Satisfying progression

1. Economy system
   - Gold earning/spending
   - Shop implementation
   - Upgrade purchases

2. Daily quests
   - 5 daily objectives
   - Completion tracking
   - Reward claiming

3. Collection tracking
   - Creature database
   - Catch mechanics
   - Storage system

4. Achievement system
   - Unlock tracking
   - Reward distribution
   - Progress display

**Success Metric:** Players want to come back tomorrow

---

### Phase 3: Depth (Week 5-6)
**Goal:** Strategic complexity

1. Team synergies
   - Type-based bonuses
   - Role combinations
   - Evolution chains
   - Visual indicators

2. Boss fights
   - Boss every 10 stages
   - Unique mechanics
   - Special rewards
   - Retry system

3. Prestige system
   - Ascension calculation
   - Token economy
   - Permanent upgrades
   - Reset mechanics

**Success Metric:** Team composition matters

---

### Phase 4: Polish (Week 7-8)
**Goal:** Professional feel

1. Balance tuning
   - Progression pacing
   - Resource rates
   - Boss difficulty

2. Visual polish
   - Animations
   - Particle effects
   - Sound effects
   - UI transitions

3. Mobile optimization
   - Touch controls
   - Responsive layout
   - Performance

4. Tutorial system
   - First-time experience
   - Tooltips
   - Help screens

**Success Metric:** Feels like a real game

---

### Phase 5: Endgame (Ongoing)
**Goal:** Long-term retention

1. Challenge modes
   - Boss Rush
   - Type restrictions
   - Speedrun mode

2. Weekly events
   - Shiny Weekend
   - Gold Rush Monday
   - XP Frenzy Wednesday
   - Boss Blitz Saturday

3. Leaderboards (optional)
   - Fastest ascension
   - Highest stage
   - Most shinies

4. Meta progression
   - Legendary Mode (post-100%)
   - Ultimate achievements
   - Prestige 20+ content

**Success Metric:** Players stay for months

---

## 🔧 Technical Architecture

### Core Classes

```javascript
class AutoBattleEngine {
    constructor()
    startBattle(stage)
    battleTick() // Every 500ms
    selectMove(creature, enemy)
    calculateDamage(attacker, defender, move)
    applyTypeEffectiveness(move, defender)
    checkVictory()
    awardLoot()
    checkBossUnlock()
}

class TeamManager {
    activeTeam // 3-6 creatures
    collection // All caught

    calculateSynergies()
    getActiveBonus(bonusType)
    swapCreature(slot, creatureId)
    validateTeam()
    getTeamPower()
}

class ProgressionSystem {
    currentStage
    defeatedCount
    offlineLastPlay

    calculateOfflineGains(timeAway)
    advanceStage()
    unlockBoss()
    checkMilestones()
}

class PrestigeSystem {
    ascensionCount
    tokens
    upgrades

    calculateTokens()
    performAscension()
    applyPrestigeBonuses()
    canAffordUpgrade(upgradeId)
    purchaseUpgrade(upgradeId)
}

class Economy {
    gold
    essence
    fragments

    awardResources(type, amount)
    spendResources(type, amount)
    purchaseItem(itemId)
    canAfford(itemId)
}

class CollectionManager {
    caught // All creatures

    attemptCatch(creatureId, isShiny)
    getCatchRate()
    getCollectionBonus(type)
    hasFullLine(evolutionLine)
}
```

### Data Structure

```javascript
localStorage.wowmon_autobattler = {
    version: "1.0",
    lastUpdate: timestamp,

    progression: {
        stage: 23,
        ascensionCount: 2,
        defeatedThisStage: 7,
        totalBattles: 1250,
        totalVictories: 1180
    },

    team: {
        active: ["murloc_1", "wisp_1", "imp_1"],
        collection: {
            murloc_1: {
                id: "murloc",
                uniqueId: "murloc_1",
                level: 15,
                xp: 2450,
                currentHp: 230,
                maxHp: 285,
                attack: 165,
                defense: 162,
                speed: 148,
                shiny: false,
                caughtAt: timestamp,
                moves: ["tackle", "bubble", "water_gun", "bite"],
                pp: { tackle: 35, bubble: 30, water_gun: 25, bite: 25 }
            },
            // ... more creatures
        }
    },

    resources: {
        gold: 12450,
        essence: 23,
        fragments: {
            water: 15,
            fire: 8,
            nature: 12,
            demon: 5,
            undead: 3,
            dragon: 1
        }
    },

    prestige: {
        tokens: 450,
        totalTokensEarned: 1230,
        upgrades: {
            battleSpeed: 3,
            goldMultiplier: 2,
            xpBoost: 2,
            offlineEfficiency: 1,
            offlineCap: 1,
            startingResources: 0,
            teamSize: 1,
            autoEvolution: true,
            shinyChance: 1,
            prestigePower: 2
        }
    },

    achievements: {
        firstWin: { unlocked: true, timestamp: timestamp },
        firstEvolution: { unlocked: true, timestamp: timestamp },
        // ... more achievements
    },

    dailyQuests: {
        lastReset: timestamp,
        battles: { progress: 32, target: 50, reward: 2000, claimed: false },
        boss: { progress: 0, target: 1, reward: { essence: 3 }, claimed: false },
        catches: { progress: 3, target: 5, reward: { fragments: 5 }, claimed: false },
        evolutions: { progress: 0, target: 1, reward: { gold: 500, xpBoost: 1 }, claimed: false }
    },

    settings: {
        autoHeal: true,
        autoEvolution: true,
        notifications: true,
        soundEnabled: true
    }
}
```

---

## 📈 Balance & Metrics

### Progression Formula

```javascript
// Enemy HP scaling
enemyHP = baseHP * (1.15 ^ stage)

// XP required per level
xpRequired = 100 * (level ^ 1.5)

// Gold rewards
goldReward = 50 + (stage * 5)

// Boss multipliers
bossHP = stageEnemyHP * 3
bossGold = stageGold * 5
bossEssence = 1-3 (guaranteed)

// Offline calculation
offlineTime = Math.min(hoursAway, offlineCapHours)
battlesWon = estimatedBattlesPerHour * offlineTime
offlineLoot = battlesWon * rewardsPerBattle * offlineMultiplier
```

### Retention Targets

| Metric | Target | How We Achieve It |
|--------|--------|-------------------|
| D1 Retention | 60% | Strong first session, clear goals |
| D7 Retention | 30% | Daily quests, steady unlocks |
| D30 Retention | 15% | First prestige, long-term visible |
| Avg Session | 5-10min | Quick sessions, no forced waits |
| Sessions/Day | 2-3 | Morning check, evening play, bedtime |

### Monetization (Optional - Not Recommended)

**If monetization is needed, keep it ethical:**
- ❌ NO pay-to-win
- ❌ NO forced ads
- ❌ NO energy systems
- ✅ Cosmetics only (skins, animations)
- ✅ Optional "support the dev" tip jar
- ✅ Offline cap extension (convenience, not power)

**Better approach:** Keep it free, build portfolio/community

---

## 🎯 Success Criteria

### Player Testimonials We Want:
- ✅ "Perfect game for my commute"
- ✅ "I can play for 5 minutes and feel progress"
- ✅ "Coming back after a day feels rewarding"
- ✅ "Team building is actually strategic"
- ✅ "Prestiging made me excited, not angry"
- ✅ "This respects my time"

### Anti-Patterns to Avoid:
- ❌ Forced check-ins or lose progress
- ❌ Meaningless number inflation (1e100 damage)
- ❌ One dominant strategy (all teams the same)
- ❌ Pay-to-progress systems
- ❌ Complexity without depth
- ❌ Punishing casual players

---

## 🌟 What Makes This Special

### vs Other Idle Games:
- **Strategic team building** (not just numbers going up)
- **Warcraft IP** (familiar creatures, established lore)
- **Ethical design** (no dark patterns, no ads)
- **Offline-first** (never punish players for living life)

### vs Original WoWmon:
- **Respects time** (auto-battle vs manual)
- **Strategic depth** (synergies > grinding)
- **Long-term goals** (months vs days)
- **Casual-friendly** (busy players can succeed)

---

## 📝 Next Steps

1. **Review this document** with stakeholders
2. **Prototype auto-battle** system (Week 1)
3. **Test offline progression** feels (Week 1)
4. **Implement Phase 1 MVP** (Week 1-2)
5. **Playtest with 5-10 users** (Week 3)
6. **Iterate based on feedback** (Week 3-4)
7. **Add depth systems** (Week 5-6)
8. **Polish and launch** (Week 7-8)

---

## 🔗 Related Files

- `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon.html` - Original game
- `/Users/kodyw/Documents/GitHub/localFirstTools3/wowMon-autobattler-design.html` - Full design doc
- This file - Implementation summary

---

## 📞 Questions?

**Design Philosophy:** "What would I want to play during my lunch break?"

**Target Player:** Busy adult who loves strategy games but doesn't have time to grind

**Core Promise:** Meaningful progress in 5-10 minute sessions, strategic depth for engaged players, months of content

---

**Last Updated:** 2025-10-12
**Version:** 1.0
**Status:** Design Complete - Ready for Implementation
