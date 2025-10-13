# WoWMon Roguelike: Quick Start Guide

## TL;DR - The Transformation

**FROM:** Linear Pokemon-style adventure with persistent world
**TO:** Roguelike dungeon crawler with procedural generation and permadeath

---

## Core Changes at a Glance

### What Stays ✅
- Battle system (turn-based combat)
- Creature types and stats
- Move system
- Evolution mechanics
- Type effectiveness
- Visual style and audio

### What Goes ❌
- Overworld map exploration
- Linear story progression
- Persistent trainer battles
- Badge collection
- Town/city locations
- NPC dialogue trees

### What's New 🆕
- Procedurally generated dungeon floors
- Branching room-based navigation
- Permadeath with run reset
- Soul shard meta-currency
- Unlock system for creatures/relics
- Permanent meta-upgrades
- Risk/reward banking system
- Daily challenges

---

## The New Game Loop

```
META HUB
    ↓
Select Starter → Choose Blessing → Enter Floor 1
    ↓
[FLOOR LOOP]
View Map → Choose Path → Enter Room → Face Encounter → Collect Rewards
    ↓
Clear Boss (every 5 floors) → CHOICE: Escape & Bank OR Continue Deeper
    ↓
DEATH (lose everything) → Convert gold to shards → Return to hub
    OR
VICTORY (floor 50) → Massive shard bonus → Return to hub
```

**Average run time:** 30 min - 4 hours depending on depth reached

---

## Key Systems Overview

### 1. Procedural Generation
- Each floor has 8-15 randomly generated rooms
- Room types: Combat (60%), Treasure (15%), Rest (10%), Shop (10%), Event (5%)
- Boss room every 5 floors
- Seeded generation (same seed = same dungeon for daily challenges)

### 2. Permadeath
- When all creatures faint: RUN ENDS
- Lose: All creatures, all items, all relics, all gold
- Keep: Soul shards (converted from gold), unlocks, achievements, stats
- Start fresh with new run, keep meta-progress

### 3. Meta-Progression
- **Soul Shards** = Permanent currency earned from runs
- Spend shards to:
  - Unlock new starter creatures
  - Unlock relics that can appear in runs
  - Buy permanent stat boosts
  - Upgrade run mechanics

### 4. Run Structure
- **Floors 1-10:** Tutorial difficulty, build team
- **Floors 11-20:** Real challenge begins
- **Floors 21-30:** Elite play required
- **Floors 31-40:** Expert territory
- **Floors 41-50:** Ultimate gauntlet
- **Floor 50:** Final boss, massive rewards

### 5. Risk/Reward
- After each boss (floors 5, 10, 15, etc.): ESCAPE OPTION
  - Escape = Bank current shards + bonus, start new run
  - Continue = Risk losing everything for greater rewards
- More risk = more reward (exponential shard scaling)

---

## Essential New Data Structures

### Meta Progress (Persistent)
```javascript
{
    soulShards: 12450,
    unlockedCreatures: ["murloc", "wisp", "imp", "kobold", "gnoll"],
    unlockedRelics: ["attack_shard", "speed_boots", "lifesteal_fang"],
    metaUpgrades: {
        healthBlessing1: true,
        merchantsFavor: true,
        fortunesFriend: false
    },
    stats: {
        totalRuns: 53,
        deepestFloor: 27,
        totalDeaths: 52,
        floor50Completions: 1
    }
}
```

### Active Run (Temporary, cleared on death)
```javascript
{
    seed: 1702834561234,
    currentFloor: 12,
    currentRoom: 3,
    team: [creature1, creature2, creature3],
    activeRelics: [relic1, relic2],
    gold: 4230,
    inventory: { healthPotion: 3, soulStone: 2 },
    runStats: {
        floorsCleared: 11,
        creaturesDefeated: 87,
        bossesKilled: 2
    }
}
```

---

## Implementation Priorities

### Phase 1: Foundation (MUST HAVE)
1. Seeded random number generator
2. Floor generation algorithm
3. Room-based navigation system
4. Meta/run dual save system
5. Death handler with shard conversion

### Phase 2: Core Content (MUST HAVE)
1. Combat encounters by floor depth
2. Treasure generation
3. Shop system
4. Boss encounters
5. Basic relic system

### Phase 3: Meta Progression (MUST HAVE)
1. Soul shard economy
2. Creature unlock tree
3. Relic unlock tree
4. 5-10 permanent upgrades
5. Meta hub UI

### Phase 4: Polish (SHOULD HAVE)
1. Run summary screen
2. Floor map visualization
3. Achievement system
4. Event rooms with choices
5. Floor modifiers

### Phase 5: Endgame (NICE TO HAVE)
1. Daily challenges
2. Prestige system
3. Endless mode
4. More relics and events
5. Leaderboards

---

## Balancing Quick Reference

### Soul Shard Economy
- Gold to shards conversion: **10:1** (1000 gold = 100 shards)
- Floor completion bonus: **floor number × 10** (floor 20 = 200 shards)
- Boss kill bonus: **floor number × 50** (floor 15 boss = 750 shards)

### Unlock Costs
- **Common creatures:** 500-1,000 shards (3-5 runs)
- **Rare creatures:** 2,000-4,000 shards (10-15 runs)
- **Legendary creatures:** 8,000-15,000 shards (30-50 runs)
- **Meta upgrades:** 500-6,000 shards each
- **Total to unlock everything:** ~150,000 shards (200-300 runs)

### Difficulty Scaling
- **Creature level formula:** `floor × 1.5 ± variance(2)`
- **Elite multiplier:** 1.5x stats
- **Boss multiplier:** 2.0x stats
- **Floor 1 creatures:** Level ~2-3
- **Floor 50 creatures:** Level ~75-80

### Loot Drop Rates
- **Common items:** 50% chance per treasure
- **Rare relics:** 15% chance per treasure
- **Epic relics:** 3% chance per treasure
- **Legendary relics:** Boss only (guaranteed on floor 40+)

---

## UI Screen Flowchart

```
[META HUB] ─────┐
    ↓           │
    │           │
[RUN SETUP]     │
    ↓           │
[STARTER SELECT]│
    ↓           │
[BLESSING SELECT]│
    ↓           │
[FLOOR MAP]     │
    ↓           │
[ROOM ENTER] ───┤
    ↓           │
[ENCOUNTER] ────┤ (Combat/Event/Shop/etc)
    ↓           │
[REWARD]        │
    ↓           │
[FLOOR MAP] ────┘
    ↓
[BOSS FIGHT]
    ↓
[ESCAPE CHOICE?] ── YES → [RUN SUMMARY] → [META HUB]
    ↓ NO                       ↑
[NEXT FLOOR]                   │
    ↓                          │
[Continue loop...]             │
    ↓                          │
[DEATH] ───────────────────────┘
```

---

## Code Migration Checklist

### Remove from wowMon.html
- [ ] Overworld tilemap rendering
- [ ] NPC interaction system
- [ ] Map transition logic
- [ ] Trainer defeat tracking
- [ ] Badge progression
- [ ] Linear quest flags

### Add to wowMon.html
- [ ] `class SeededRNG`
- [ ] `class FloorGenerator`
- [ ] `class SaveManager` (dual save)
- [ ] `class DeathHandler`
- [ ] `class MetaHubUI`
- [ ] `class FloorMapUI`
- [ ] `class RunSetupUI`
- [ ] `class RunSummaryUI`

### Modify in wowMon.html
- [ ] `GameEngine.constructor()` - add roguelike state
- [ ] `GameEngine.startGame()` → `GameEngine.startNewRun()`
- [ ] Battle system - add relic effect handlers
- [ ] Save system - implement meta/run split
- [ ] UI layer - add new screens

---

## Minimum Viable Roguelike (MVP)

To get a playable prototype quickly, implement this subset:

### MVP Features
1. **5 starter creatures** (Murloc, Wisp, Imp, Kobold, Gnoll)
2. **10 floors only** (floor 5 = boss, floor 10 = final boss)
3. **3 room types:** Combat, Treasure, Boss
4. **Basic shard system:** Gold → shards on death
5. **2 unlockable creatures:** Wolf (1000 shards), Ghoul (1500 shards)
6. **5 basic relics:** Health Ring, Attack Boost, Speed Boost, Lifesteal, Crit Chance
7. **Simple meta hub:** Start Run, Unlock Creatures, View Stats
8. **No events/shops** in MVP (add later)

### MVP Implementation Time
- **Procedural generation:** 1 week
- **Dual save system:** 3 days
- **Meta hub UI:** 1 week
- **Floor map UI:** 1 week
- **Death/summary screens:** 3 days
- **Testing & balance:** 1 week

**Total MVP: 4-5 weeks**

---

## Testing Checklist

### Core Mechanics
- [ ] Floor generation creates valid layouts
- [ ] All rooms are reachable
- [ ] Combat encounters scale properly
- [ ] Death triggers correctly
- [ ] Gold → shard conversion works
- [ ] Meta progress saves
- [ ] Active run saves/loads
- [ ] Active run clears on death

### Economy Balance
- [ ] Can unlock first creature in ~3-5 runs
- [ ] Can unlock rare creature in ~10-15 runs
- [ ] Reaching floor 10 feels achievable
- [ ] Reaching floor 25 feels challenging
- [ ] Reaching floor 50 feels epic

### Replayability
- [ ] Each run feels different
- [ ] Multiple viable strategies exist
- [ ] Players want to "try one more run"
- [ ] Meta-progression feels rewarding
- [ ] Not too grindy (skill matters more than grind)

---

## Common Pitfalls to Avoid

### ❌ DON'T
- Make unlock costs too high (frustrating grind)
- Make unlock costs too low (no long-term goals)
- Use true randomness (breaks daily challenges)
- Make permadeath feel punishing (it should feel fair)
- Ignore run variety (procedural ≠ automatically fun)
- Forget to telegraph danger (unfair deaths = rage quit)

### ✅ DO
- Use seeded randomness for reproducibility
- Balance shard economy so skilled play = faster progress
- Provide visual/audio feedback for all systems
- Make death feel like learning opportunity
- Ensure multiple viable builds/strategies
- Playtest obsessively with different player types

---

## FAQ for Implementation

**Q: Can I keep the current battle system?**
A: YES! The battle system works great. Just add relic effect hooks.

**Q: Do I need to rewrite everything?**
A: NO! ~60% of code (creatures, moves, battles, audio) stays. Replace exploration with procedural dungeons.

**Q: How do I handle daily challenges?**
A: Use a date-based seed (e.g., `YYYYMMDD` → seed). Everyone gets same dungeon that day.

**Q: What if players die on floor 49?**
A: That's the design! Near-misses create "one more run" addiction. Make sure they get significant shards even from partial runs.

**Q: Should I add PvP?**
A: Not initially. Focus on single-player loop first. Add asynchronous PvP later (ghost runs).

**Q: How many creatures should be unlockable?**
A: All 25 existing creatures. Start with 3, unlock rest through progression.

**Q: How do I prevent save scumming?**
A: Auto-save after every room. Make it transparent: "Auto-saved" indicator.

**Q: Should floors get bigger as you go deeper?**
A: No, keep 8-15 rooms per floor. Instead, increase enemy density and difficulty.

---

## Success Metrics

Your roguelike is working if:

1. **Players restart immediately after death** ("one more run")
2. **Average session = 30-60 minutes** (good for coffee break)
3. **Players reach floor 10 within 5 attempts** (not too hard)
4. **Floor 50 completion rate = 5-10%** (epic achievement)
5. **Multiple viable strategies exist** (not one meta build)
6. **Each run feels different** (procedural variety)
7. **Meta-progression feels meaningful** (unlocks impact gameplay)

---

## Final Checklist Before Launch

- [ ] Can start a run and reach floor 5
- [ ] Death converts gold to shards correctly
- [ ] Meta progress persists across runs
- [ ] Can unlock at least one new creature
- [ ] Boss fights are challenging but fair
- [ ] UI clearly shows current floor, team status, resources
- [ ] Auto-save works (no lost progress)
- [ ] Export/import save data works
- [ ] Audio/SFX work for all new actions
- [ ] Mobile controls function properly
- [ ] Game runs offline (no CDN dependencies)
- [ ] File size remains reasonable (<500kb)

---

## Post-Launch Content Roadmap

### Month 1-2
- Balance tweaks based on player feedback
- Add 10 more relics
- Add 5 event types
- Fix bugs

### Month 3-4
- Daily challenge system
- Leaderboards (local storage based)
- 5 new creatures
- Prestige system

### Month 5-6
- Endless mode (post-floor 50)
- Achievement system expansion
- Cosmetic unlocks
- PvP ghost runs

### Month 7+
- New game modes (speed run, no relics, etc.)
- Community events
- More creatures/relics
- Seasonal content

---

## Resources & References

### Roguelike Design
- Slay the Spire (card-based roguelike inspiration)
- Hades (meta-progression inspiration)
- Binding of Isaac (procedural generation)
- Dead Cells (risk/reward, permadeath)

### Technical References
- Procedural generation: Use seeded RNG
- Save system: LocalStorage with JSON
- UI: CSS Grid for room layouts
- Audio: Existing Web Audio API approach

---

## Contact & Support

For questions about implementation:
1. Check WOWMON_ROGUELIKE_REDESIGN.md for design details
2. Check WOWMON_ROGUELIKE_IMPLEMENTATION.md for code examples
3. Reference existing wowMon.html battle system
4. Playtest frequently and iterate

---

**Remember:** The goal is to transform a linear adventure into an endlessly replayable dungeon crawler. Focus on the core loop first, then add variety and depth. Good luck!

🎮 **"One more run..."**
