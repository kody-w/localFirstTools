# WowMon Card Game - Quick Start Implementation Guide

## TL;DR - The Elevator Pitch

**Transform WowMon from Pokemon-style RPG into Slay the Spire-style deck builder:**
- 🃏 **Cards instead of creatures** - Build strategic decks of 15-40 cards
- ⚡ **Energy system** - 3 energy per turn, cards cost 0-4
- 🎯 **Strategic combat** - Play creatures to board, cast spells, manage resources
- 🔄 **Roguelike runs** - 30-50 battles per run, randomized paths and rewards
- 📈 **Deck building** - Add/remove cards, upgrade them, discover synergies

---

## Core Game Loop (60 seconds)

```
1. Start with 15-card starter deck
   ↓
2. Battle enemy (play cards, attack with creatures)
   ↓
3. Win → Get rewards (gold + choose 1 of 3 cards)
   ↓
4. Navigate map (choose path: combat, shop, rest, event)
   ↓
5. Repeat 30-50 battles across 4 acts
   ↓
6. Defeat final boss → Victory!
   ↓
7. Unlock new cards/decks for next run
```

---

## Card Types (3 Core Types)

### 1. CREATURE CARDS
```javascript
{
  name: "Murloc",
  cost: 1,        // Energy to play
  attack: 2,      // Damage dealt
  health: 3,      // HP before destroyed
  type: ["water", "beast"],
  ability: "Battlecry: Draw card if you control another Water creature"
}
```

### 2. SPELL CARDS
```javascript
{
  name: "Hydro Pump",
  cost: 3,
  effect: "Deal 8 damage to any target",
  type: ["water"]
}
```

### 3. RELIC CARDS
```javascript
{
  name: "Hearthstone",
  effect: "At start of combat: Heal 5 HP. Healing effects +50%",
  permanent: true  // Lasts entire run
}
```

---

## Combat System (5 Key Mechanics)

### 1. ENERGY
- Start with 3 energy per turn
- Spend energy to play cards
- Resets to 3 each turn

### 2. CREATURES
- Play to board (max 5 creatures)
- Attack once per turn
- Persist between turns

### 3. BLOCK (Armor)
- Reduces damage before HP
- Resets at start of your turn

### 4. INTENT
- Enemies show what they'll do next
- ⚔️ = Attack (shows damage)
- 🛡️ = Defend (gaining block)
- 🔮 = Special ability

### 5. WIN CONDITIONS
- Reduce enemy HP to 0
- Don't let your HP reach 0

---

## Turn Structure (Simple)

```
START OF TURN
├─ Draw to 5 cards
├─ Gain 3 energy
└─ Process status effects (poison, regen, etc.)

MAIN PHASE
├─ Play cards (costs energy)
├─ Attack with creatures
└─ Can do in any order

END OF TURN
├─ Discard hand to 2 cards (choose which)
├─ Trigger end-of-turn effects
└─ Enemy takes their turn
```

---

## Starter Decks (Choose One)

### WATER DECK (Card Draw/Control)
```
3x Murloc (1 cost, 2/3, draw synergy)
3x Strike (1 cost, deal 5 damage)
2x Water Gun (1 cost, deal 4 damage)
2x Defend (1 cost, gain 5 block)
2x Bubble (0 cost, gain 3 block)
2x Tide Surge (1 cost, draw 1 card)
1x Hydro Pump (3 cost, deal 8 damage)
```

### FIRE DECK (Aggressive Burn)
```
3x Imp (1 cost, 3/2, deal 1 on play)
3x Strike (1 cost, deal 5 damage)
2x Ember (1 cost, deal 5 damage)
2x Firebolt (1 cost, deal 6 random)
2x Defend (1 cost, gain 5 block)
2x Rage (0 cost, gain 2 energy this turn)
1x Inferno (3 cost, deal 12, risky)
```

### NATURE DECK (Healing/Sustain)
```
3x Wisp (2 cost, 1/4, heal 2 per turn)
3x Strike (1 cost, deal 5 damage)
2x Defend (1 cost, gain 5 block)
2x Magical Leaf (1 cost, deal 4, never miss)
2x Nature's Blessing (1 cost, heal 5 HP)
2x Grow (1 cost, creature gets +2/+2)
1x Ancient Wisdom (2 cost, draw 3 cards)
```

---

## Keywords (Essential 10)

| Keyword | Meaning |
|---------|---------|
| **Quick** | Can attack the turn it's played |
| **Taunt** | Enemies must attack this first |
| **Flying** | Can only be blocked by Flying |
| **Battlecry** | Effect when played |
| **Deathrattle** | Effect when dies |
| **Poison X** | Deal X damage per turn |
| **Regen X** | Heal X per turn |
| **Exhaust** | Remove from deck after use |
| **Echo** | Can play multiple times in one turn |
| **Combo** | Bonus if not first card played |

---

## Progression Path (Run Structure)

```
ACT 1: GOLDSHIRE (8-10 battles)
├─ Enemies: Gnolls, Kobolds, Wolves
├─ Boss: Muradin (80 HP, summons Elementals)
└─ Reward: Forge Badge + Rare card

ACT 2: ASHENVALE (10-12 battles)
├─ Enemies: Wisps, Treants, Naga
├─ Boss: Malfurion (100 HP, Nature master)
└─ Reward: Nature Badge + Epic card

ACT 3: FROZEN WASTES (12-15 battles)
├─ Enemies: Undead, Elementals
├─ Boss: Jaina (120 HP, Frost spells)
└─ Reward: Frost Badge + Epic card

ACT 4: ORGRIMMAR (15+ battles)
├─ Enemies: Orcs, Dragons, Demons
├─ Boss: Thrall (150 HP, Elemental fury)
└─ Reward: Storm Badge + Legendary

FINAL: ELITE FOUR (4 bosses)
└─ Victory = Complete run!
```

---

## Map Nodes (What You'll Encounter)

| Icon | Type | What Happens |
|------|------|--------------|
| ⚔️ | Combat | Fight normal enemy → Rewards |
| 💀 | Elite | Harder fight → Better rewards |
| 💰 | Shop | Buy cards, relics, upgrades |
| 🔥 | Rest | Heal OR upgrade card OR remove card |
| ❓ | Event | Random encounter (can be good or bad) |
| 🎁 | Treasure | Free reward (card/gold/relic) |
| 👑 | Boss | Act finale, must win |

---

## Rewards After Battle

**EVERY VICTORY:**
1. 💰 Gold (30-80g)
2. 🃏 Choose 1 of 3 cards to add (or skip)
3. 🧪 25% chance for potion

**ELITE VICTORIES:**
- More gold (80-150g)
- Better card choices (more rares)
- 50% chance for relic

**BOSS VICTORIES:**
- Lots of gold (200-400g)
- Epic/Legendary card choice
- Badge (permanent upgrade)

---

## Deck Building Strategy (3 Rules)

### RULE 1: Consistency > Power
- **Smaller deck** (15-25 cards) = Draw best cards more often
- **Remove weak starters** at rest sites (costs 75g)
- **Don't add every card** - only if it fits strategy

### RULE 2: Energy Curve Matters
```
Ideal distribution:
- 30% low cost (0-1 energy)
- 40% medium (2 energy)
- 20% high (3 energy)
- 10% finishers (4+ energy)
```

### RULE 3: Build Synergies
- **Water deck?** Add more Water creatures + water spells
- **Warrior deck?** Stack Warrior buffs and battle shouts
- **Poison deck?** Add poison appliers + poison payoffs

---

## Common Archetypes (7 Viable Strategies)

1. **Water Swarm** - Many small creatures + card draw
2. **Fire Burn** - Direct damage spells, ignore creatures
3. **Nature Tank** - High HP creatures + healing
4. **Shadow Poison** - Apply poison, stall with defense
5. **Warrior Tempo** - Efficient trades, board control
6. **Dragon Ramp** - Expensive dragons, energy generation
7. **Undead Sacrifice** - Kill own creatures for power

---

## Key Strategic Decisions

### AT REST SITES (Choose 1):
- 🛌 **Rest** - Heal 30 HP
- ⚒️ **Upgrade** - Make 1 card stronger (permanent)
- 🗑️ **Remove** - Delete 1 card from deck (costs 75g)

### IN SHOPS:
- Buy powerful cards (50-150g)
- Buy relics (250-300g permanent upgrades)
- Remove cards (75g)
- Upgrade cards (100g)

### ON MAP:
- **More combats** = more cards/gold but riskier
- **Elite path** = high risk, high reward
- **Safe path** = guaranteed rest sites and shops

---

## Example Turn (Visual)

```
TURN START
Energy: ⚡⚡⚡ (3/3)
Hand: [Murloc][Strike][Defend][Water Gun][Bubble]

ACTIONS:
1. Play Murloc (1⚡) → Summon 2/3 creature
2. Play Water Gun (1⚡) → Deal 4 damage to enemy
3. Play Bubble (0⚡) → Gain 3 block
4. Energy remaining: ⚡ (1/3)
5. Attack with Murloc → Deal 2 damage
6. End turn

RESULT:
- Enemy took 6 damage total (4 spell + 2 creature)
- You gained 3 block
- Have 1/3 Murloc on board for next turn
```

---

## Winning Strategy (4-Step Process)

### 1. EARLY GAME (Acts 1-2)
- **Pick synergistic cards** - build around your type
- **Upgrade key cards** - at rest sites
- **Don't overfill deck** - quality > quantity

### 2. MID GAME (Act 3)
- **Remove weak cards** - trim the fat
- **Buy key relics** - permanent power spikes
- **Solidify win condition** - how will you close games?

### 3. LATE GAME (Act 4)
- **Maximize consistency** - deck should be tuned
- **Save potions** - for boss fights
- **Heal when needed** - don't greed

### 4. BOSS FIGHTS
- **Study intent** - plan around big attacks
- **Manage resources** - don't blow everything turn 1
- **Use potions** - they reset after boss

---

## Technical Implementation (For Devs)

### Minimum Data Structures

```javascript
// Game State
const gameState = {
  player: {
    hp: 60,
    maxHp: 60,
    energy: 3,
    maxEnergy: 3,
    deck: [],
    hand: [],
    discard: [],
    creatures: [],
    relics: [],
    gold: 0
  },
  enemy: {
    hp: 40,
    maxHp: 40,
    creatures: [],
    intent: { type: "attack", value: 10 }
  }
};

// Card Template
const card = {
  id: "murloc",
  name: "Murloc",
  cost: 1,
  type: "creature",
  attack: 2,
  health: 3,
  keywords: ["battlecry"],
  description: "Battlecry: Draw card if you control Water creature"
};
```

### Core Game Loop

```javascript
// 1. Start turn
function startTurn() {
  drawCards(5 - hand.length);
  player.energy = player.maxEnergy;
  processStartEffects();
}

// 2. Play card
function playCard(card) {
  if (player.energy >= card.cost) {
    player.energy -= card.cost;
    executeCardEffect(card);
    discard.push(card);
  }
}

// 3. End turn
function endTurn() {
  discardHand();
  processEndEffects();
  enemyTurn();
}

// 4. Enemy turn
function enemyTurn() {
  executeIntent(enemy.intent);
  enemyCreaturesAttack();
  checkWinCondition();
}
```

---

## Balancing Formula

### Creature Stats Formula
```
Total Stats = Cost × 5
Example: 2-cost creature = 10 total stats (could be 4/6, 5/5, 3/7, etc.)
```

### Spell Damage Formula
```
Damage = Cost × 5
1-cost = 5 damage
2-cost = 10 damage
3-cost = 15 damage
```

### Energy Costs by Power
```
0 cost: Utility only (block, draw)
1 cost: Basic effects (5 damage, 2/3 creature)
2 cost: Good value (8-10 damage, 4/4 creature)
3 cost: Strong (12-15 damage, 6/5 creature)
4 cost: Game-enders (18-20 damage, 8/8 creature)
```

---

## Files to Reference

1. **WOWMON_CARD_GAME_REDESIGN.md** - Complete detailed design (14+ sections)
2. **wowmon-card-game-demo.html** - Visual card showcase (interactive)
3. **This file** - Quick implementation guide

---

## Next Steps for Implementation

### PHASE 1: Prototype Core
- [ ] Implement energy system
- [ ] Create 20 basic cards (10 creatures, 10 spells)
- [ ] Build combat system (play cards, attack, take damage)
- [ ] Test single battle

### PHASE 2: Deck Building
- [ ] Add 3 starter decks (Water, Fire, Nature)
- [ ] Implement deck shuffling and drawing
- [ ] Add card rewards after battle
- [ ] Create shop system

### PHASE 3: Progression
- [ ] Design map with node types
- [ ] Implement rest sites (heal/upgrade/remove)
- [ ] Add 4 boss fights
- [ ] Create run win/loss screens

### PHASE 4: Polish
- [ ] Add 100+ more cards
- [ ] Balance testing
- [ ] Visual polish (animations, VFX)
- [ ] Save/load system

---

## Key Success Metrics

✅ **Easy to learn** - New players understand basics in 2 minutes
✅ **Hard to master** - Skilled players win more consistently
✅ **Replayable** - Want to do "one more run"
✅ **Strategic** - Decisions matter, not just luck
✅ **Satisfying** - Big plays feel amazing

---

## Common Pitfalls to Avoid

❌ **Too complex** - Don't add 50 mechanics at once
❌ **Unbalanced** - Playtest early and often
❌ **Luck-dependent** - Skill should matter more than RNG
❌ **Grindy** - Runs should be 45-90 min, not 5 hours
❌ **Pay-to-win** - Keep it fair, cosmetics only

---

**Ready to build? Start with Phase 1 and iterate!** 🚀
