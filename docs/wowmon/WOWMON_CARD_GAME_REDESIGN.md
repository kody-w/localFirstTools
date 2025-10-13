# WowMon: Deck Builder Card Game Redesign
## Complete Strategic Card Battle System

---

## Executive Summary

This redesign transforms WowMon from a traditional Pokemon-style RPG into a **Slay the Spire-inspired deck-building card game**. Players build strategic decks from creature and spell cards, face challenging encounters, and refine their decks through smart choices. The system maintains the Warcraft creature theme while introducing deep card synergies, energy management, and roguelike progression.

---

## 1. CARD SYSTEM

### 1.1 Card Types

#### **CREATURE CARDS** (Summons)
- Play to summon a creature to your side of the battlefield
- Creatures persist between turns and can attack/defend
- Each creature has:
  - **Energy Cost**: 0-4 energy to play
  - **Attack Power**: Damage dealt when attacking
  - **Health Points**: Damage before destroyed
  - **Abilities**: Passive or triggered effects
  - **Type**: Water, Fire, Nature, Shadow, etc.

**Example Creature Cards:**

```
┌─────────────────────┐
│ MURLOC              │
│ [Water] [Beast]     │
│ Cost: 1 Energy      │
├─────────────────────┤
│    ╔═══╗            │
│   ║ @ @ ║           │
│   ║  ~  ║  Mrglglgl!│
│    ╚═══╝            │
├─────────────────────┤
│ ATK: 2   HP: 3      │
├─────────────────────┤
│ Battlecry: Draw a   │
│ card if you control │
│ another Water type. │
└─────────────────────┘

┌─────────────────────┐
│ DIRE WOLF           │
│ [Beast] [Shadow]    │
│ Cost: 3 Energy      │
├─────────────────────┤
│   ╔═══════╗         │
│  ║  Λ  Λ  ║         │
│  ║ (◉) (◉)║  HOWL! │
│   ╚═══════╝         │
├─────────────────────┤
│ ATK: 5   HP: 4      │
├─────────────────────┤
│ Quick: Can attack   │
│ immediately.        │
│ Bloodthirst: +2 ATK │
│ if enemy damaged.   │
└─────────────────────┘

┌─────────────────────┐
│ ANCIENT WISP        │
│ [Nature] [Spirit]   │
│ Cost: 4 Energy      │
├─────────────────────┤
│      ✧ ✦ ✧         │
│    ✦  ◉  ✦         │
│      ✧ ✦ ✧         │
├─────────────────────┤
│ ATK: 3   HP: 6      │
├─────────────────────┤
│ At end of turn:     │
│ Heal all friendly   │
│ creatures for 1 HP. │
│ Can't attack.       │
└─────────────────────┘
```

#### **SPELL CARDS** (Abilities)
- One-time effects that resolve immediately
- More powerful than creature abilities
- Include damage, healing, buffs, debuffs, card draw

**Example Spell Cards:**

```
┌─────────────────────┐
│ HYDRO PUMP          │
│ [Water]             │
│ Cost: 3 Energy      │
├─────────────────────┤
│     ═══════         │
│    ══≈≈≈≈═         │
│   ═≈≈≈≈≈≈═         │
│    ══≈≈≈═          │
│     ═══             │
├─────────────────────┤
│ Deal 8 damage to    │
│ any target.         │
│                     │
│ Drench: If target   │
│ survives, reduce    │
│ their ATK by 2.     │
└─────────────────────┘

┌─────────────────────┐
│ BATTLE SHOUT        │
│ [Warrior]           │
│ Cost: 1 Energy      │
├─────────────────────┤
│      !!!            │
│    ╔═══╗            │
│   ║▓▓▓▓▓║          │
│    ╚═══╝            │
│      !!!            │
├─────────────────────┤
│ Give all friendly   │
│ creatures +2 ATK    │
│ this turn.          │
│                     │
│ Draw a card.        │
└─────────────────────┘

┌─────────────────────┐
│ PLAGUE STRIKE       │
│ [Undead] [Shadow]   │
│ Cost: 2 Energy      │
├─────────────────────┤
│      ☠              │
│    ░▒▓█▓▒░         │
│   ░▒▓███▓▒░        │
│    ░▒▓█▓▒░         │
│      ☠              │
├─────────────────────┤
│ Deal 3 damage.      │
│ Apply Plague (2):   │
│ Take 2 damage at    │
│ start of each turn. │
└─────────────────────┘
```

#### **RELIC CARDS** (Permanent Upgrades)
- Passive effects that last the entire run
- Not part of your combat deck
- Acquired through special encounters and choices

```
┌─────────────────────┐
│ HEARTHSTONE         │
│ [Relic]             │
├─────────────────────┤
│    ╔═══════╗        │
│   ║ ◢█████◣ ║       │
│   ║  ◆─◆─◆  ║       │
│    ╚═══════╝        │
├─────────────────────┤
│ At start of combat: │
│ Heal 5 HP.          │
│                     │
│ Your healing effects│
│ are 50% stronger.   │
└─────────────────────┘

┌─────────────────────┐
│ DRAGON SCALE        │
│ [Relic]             │
├─────────────────────┤
│      ▓▓▓            │
│    ▓▓░░░▓▓          │
│   ▓░░░░░░░▓         │
│    ▓▓░░░▓▓          │
│      ▓▓▓            │
├─────────────────────┤
│ All Dragon-type     │
│ creatures cost 1    │
│ less energy.        │
│                     │
│ Start with +3 Block.│
└─────────────────────┘
```

### 1.2 Card Rarity System

**COMMON** (Gray) - 60% drop rate
- Basic creatures and spells
- Simple effects, low cost
- Examples: Murloc, Tackle, Howl

**UNCOMMON** (Green) - 30% drop rate
- Moderate complexity
- Good synergies
- Examples: Murloc Warrior, Water Gun, Battle Cry

**RARE** (Blue) - 8% drop rate
- Powerful effects
- Strong synergies
- Examples: Ancient Wisp, Hydro Pump, Dragon Breath

**EPIC** (Purple) - 1.8% drop rate
- Build-around cards
- Game-changing effects
- Examples: Dragon, Inferno, Bladestorm

**LEGENDARY** (Orange) - 0.2% drop rate
- Unique, powerful cards
- Only one in deck
- Examples: Phoenix (Rebirth ability), Infernal (massive stats)

### 1.3 Card Upgrade System

Cards can be **UPGRADED** at rest sites or through special events:

```
BEFORE UPGRADE:
┌─────────────────────┐
│ WATER GUN           │
│ Cost: 1             │
│ Deal 4 damage.      │
└─────────────────────┘

AFTER UPGRADE:
┌─────────────────────┐
│ WATER GUN+          │
│ Cost: 1             │
│ Deal 6 damage.      │
│ Draw a card if      │
│ target dies.        │
└─────────────────────┘
```

Upgrade benefits:
- **Spells**: More damage, lower cost, or added effects
- **Creatures**: +1/+1 stats, improved abilities, or lower cost
- **Each card can only be upgraded once**

---

## 2. DECK BUILDING SYSTEM

### 2.1 Starting Decks

Players choose one of three starter decks:

#### **WATER DECK** (Murloc Starter)
*Theme: Card draw and momentum*

**Starting Deck (15 cards):**
- 3x Murloc (1 cost, 2/3, draw synergy)
- 2x Bubble (0 cost, give 3 block)
- 3x Strike (1 cost, deal 5 damage)
- 2x Water Gun (1 cost, deal 4 damage)
- 2x Defend (1 cost, gain 5 block)
- 2x Tide Surge (1 cost, draw 1 card)
- 1x Hydro Pump (3 cost, deal 8 damage)

**Archetype**: Control/Draw
**Win Condition**: Maintain card advantage, outlast opponent

#### **FIRE DECK** (Imp Starter)
*Theme: Aggressive burst damage*

**Starting Deck (15 cards):**
- 3x Imp (1 cost, 3/2, deal 1 damage when played)
- 2x Ember (1 cost, deal 5 damage)
- 3x Strike (1 cost, deal 5 damage)
- 2x Firebolt (1 cost, deal 6 damage to random enemy)
- 2x Defend (1 cost, gain 5 block)
- 2x Rage (0 cost, gain 2 energy this turn)
- 1x Inferno (3 cost, deal 12 damage, 50% accuracy)

**Archetype**: Aggro/Burn
**Win Condition**: Fast damage, finish before resources run out

#### **NATURE DECK** (Wisp Starter)
*Theme: Healing and sustain*

**Starting Deck (15 cards):**
- 3x Wisp (2 cost, 1/4, heal 2 at end of turn)
- 2x Magical Leaf (1 cost, deal 4 damage, never miss)
- 3x Strike (1 cost, deal 5 damage)
- 2x Defend (1 cost, gain 5 block)
- 2x Nature's Blessing (1 cost, heal 5 HP)
- 2x Grow (1 cost, creature gains +2/+2)
- 1x Ancient Wisdom (2 cost, draw 3 cards)

**Archetype**: Midrange/Sustain
**Win Condition**: Survive early game, build powerful board

### 2.2 Deck Construction Rules

- **Minimum deck size**: 15 cards (starting)
- **Maximum deck size**: 40 cards (practical limit)
- **No card limit**: Can have multiple copies
- **Legendary limit**: Only 1 of each legendary in deck
- **Deck grows during run**: Add cards after victories
- **Deck refinement**: Remove cards at rest sites (costs gold)

### 2.3 Deck Archetypes

#### **AGGRO SWARM** (Beast/Demon)
**Strategy**: Play many low-cost creatures quickly
**Key Cards**:
- Wolf (2 cost, 3/3, Quick)
- Imp (1 cost, 3/2, ping damage)
- Battle Cry (1 cost, +2 ATK to all)
- Quick Strike (0 cost, deal 3 damage)

**Win Condition**: Overwhelm before opponent stabilizes

#### **CONTROL/STALL** (Water/Undead)
**Strategy**: Remove threats, survive to late game
**Key Cards**:
- Plague Strike (2 cost, apply poison)
- Curse (1 cost, weaken enemy)
- Hydro Pump (3 cost, big removal)
- Heal effects

**Win Condition**: Exhaust opponent's resources

#### **COMBO BURST** (Magic/Fire)
**Strategy**: Set up multi-card combos for huge turns
**Key Cards**:
- Mana Drain (gain energy)
- Card draw spells
- Cosmic Power (buff stats)
- Inferno/Explosion (huge damage)

**Win Condition**: Execute perfect combo turn

#### **SUSTAIN/ATTRITION** (Nature/Spirit)
**Strategy**: Heal and outlast everything
**Key Cards**:
- Ancient Wisp (heal each turn)
- Synthesis (heal 10 HP)
- Treant (5/8 tank)
- Nature synergies

**Win Condition**: Survive until opponent runs out

#### **TEMPO/MIDRANGE** (Warrior/Dragon)
**Strategy**: Efficient trades, strong board presence
**Key Cards**:
- Dire Wolf (3 cost, 5/4, Quick)
- Battle Shout (buff all)
- Execute (finish damaged enemies)
- Drake (4 cost, 6/5, flying)

**Win Condition**: Control board, pressure consistently

#### **SACRIFICE/UNDEAD** (Undead/Demon)
**Strategy**: Sacrifice own creatures for power
**Key Cards**:
- Ghoul (dies, deal 3 to all enemies)
- Drain Life (deal damage, heal self)
- Corpse Explosion (destroy ally, huge damage)
- Abomination (gets stronger as allies die)

**Win Condition**: Turn deaths into advantage

---

## 3. CARD MECHANICS & KEYWORDS

### 3.1 Core Keywords

**QUICK** - Creature can attack the turn it's played
```
Example: Dire Wolf (3 cost, 5/4, Quick)
```

**TAUNT** - Enemies must attack this creature first
```
Example: Treant (4 cost, 3/8, Taunt)
```

**FLYING** - Can only be blocked by Flying creatures
```
Example: Drake (4 cost, 6/5, Flying)
```

**BATTLECRY** - Effect triggers when card is played
```
Example: Imp (Battlecry: Deal 1 damage to random enemy)
```

**DEATHRATTLE** - Effect triggers when creature dies
```
Example: Ghoul (Deathrattle: Deal 3 damage to all enemies)
```

**STEALTH** - Cannot be targeted by enemies for 1 turn
```
Example: Banshee (3 cost, 4/3, Stealth)
```

**REGENERATE X** - Heals X HP at start of your turn
```
Example: Wisp (Regenerate 2)
```

**POISON X** - Deal X damage at start of defender's turn
```
Example: Spider Bite (Apply Poison 3 for 3 turns)
```

### 3.2 Advanced Mechanics

**EVOLVE** - Permanent upgrade at certain conditions
```
Murloc → Murloc Warrior (when you have 5+ Water cards in deck)
Upgrades stats and abilities permanently
```

**ECHO** - Can play this card multiple times in one turn
```
Example: Shadow Step (0 cost, deal 2, Echo)
Play up to 3 times per turn
```

**EXHAUST** - Card is removed from deck after use
```
Example: Execute (2 cost, deal 20 to damaged enemy, Exhaust)
```

**RETAIN** - Keep in hand at end of turn (normally discard)
```
Example: Guardian's Shield (1 cost, +8 block, Retain)
```

**X COST** - Spend all remaining energy for scaling effect
```
Example: Dragon Rage (X cost, deal X*3 damage)
```

**COMBO** - Bonus effect if not first card played this turn
```
Example: Backstab (1 cost, deal 4. Combo: Deal 8 instead)
```

**SYNERGY** - Bonus when combined with type/tribe
```
Example: Pack Leader (Battlecry: +1/+1 to all Beasts)
```

### 3.3 Status Effects

**BUFFS** (Positive)
- **Strength (+X ATK)**: Creature deals more damage
- **Fortify (+X HP)**: Creature has more health
- **Regen (X)**: Heal X at start of turn
- **Barrier**: Immune to damage once
- **Fury**: Double attack this turn

**DEBUFFS** (Negative)
- **Weak (-X ATK)**: Creature deals less damage
- **Poison (X)**: Take X damage per turn
- **Frozen**: Can't attack or use abilities
- **Silenced**: Loses all abilities
- **Cursed**: Takes double damage

---

## 4. COMBAT FLOW

### 4.1 Battle Structure

**TURN SEQUENCE:**

1. **START OF TURN**
   - Draw cards to hand size (5 cards)
   - Gain energy (3 base energy)
   - Trigger start-of-turn effects (Regen, Poison, etc.)

2. **MAIN PHASE**
   - Play cards from hand (costs energy)
   - Attack with creatures (each creature attacks once)
   - Use abilities
   - Can do these in any order

3. **END OF TURN**
   - Trigger end-of-turn effects
   - Discard hand to 2 cards (choose which to keep)
   - Enemy takes their turn
   - Repeat

**COMBAT LAYOUT:**
```
┌──────────────────────────────────────────────┐
│ ENEMY CREATURES                    HP: 45/60 │
│ ┌──────┐ ┌──────┐ ┌──────┐                  │
│ │Gnoll │ │Kobold│ │Wolf  │         Block: 8 │
│ │ 4/3  │ │ 2/2  │ │ 3/3  │                  │
│ └──────┘ └──────┘ └──────┘       Energy: 0/3│
├──────────────────────────────────────────────┤
│ BATTLEFIELD                                   │
│                                               │
│      ⚔ Combat Zone ⚔                         │
│                                               │
├──────────────────────────────────────────────┤
│ YOUR CREATURES                     HP: 52/60 │
│ ┌──────┐ ┌──────┐                           │
│ │Murloc│ │Wisp  │                Block: 12  │
│ │ 2/3  │ │ 1/4  │                           │
│ └──────┘ └──────┘              Energy: 3/3  │
├──────────────────────────────────────────────┤
│ YOUR HAND (5 cards)              Deck: 18    │
│ [Water Gun] [Strike] [Defend] [Murloc] [Heal]│
├──────────────────────────────────────────────┤
│ Discard: 8 cards  |  [END TURN] | Exile: 3   │
└──────────────────────────────────────────────┘
```

### 4.2 Combat Rules

**ENERGY SYSTEM:**
- Start with 3 energy per turn
- Cards cost 0-4 energy
- Unused energy doesn't carry over
- Some cards/relics can give bonus energy

**ATTACKING:**
- Each creature can attack once per turn
- Quick creatures can attack immediately when played
- Creatures with Taunt must be attacked first
- Flying creatures can only be blocked by Flying

**BLOCKING (ARMOR):**
- Block reduces damage taken
- Block persists between player turns
- Resets to 0 at start of player's turn
- Enemy attacks deplete block before HP

**DAMAGE PRIORITY:**
1. Block is reduced first
2. Then HP is reduced
3. At 0 HP, creatures die
4. Player loses at 0 HP

**CARD DRAW:**
- Draw to 5 cards at start of turn
- When deck runs out, shuffle discard into new deck
- If deck empty and discard empty, take 1 damage per card

### 4.3 Enemy AI Patterns

Enemies have predictable patterns shown by **intent icons**:

```
⚔️  Attack (shows damage amount)
🛡️  Defend (gaining block)
🔮  Ability (special effect)
❓  Unknown (boss special)
```

**Example Enemy Turn:**
```
┌──────────────────┐
│ ORC GRUNT        │
│ HP: 25/40   ⚔️ 12│
│                  │
│ [Intent: Attack  │
│  for 12 damage]  │
└──────────────────┘

Player sees enemy will attack for 12 next turn
Can prepare: Play defense, kill it, or debuff it
```

### 4.4 Victory & Rewards

**WIN CONDITIONS:**
- Reduce enemy HP to 0
- Special objectives (survive X turns, etc.)

**LOSS CONDITIONS:**
- Your HP reaches 0
- Special fail states (time limit, etc.)

**REWARDS AFTER VICTORY:**
- **Gold**: 30-80g per fight
- **Card Choice**: Pick 1 of 3 cards to add to deck
- **Potion Drop**: 25% chance for consumable
- **Rare Rewards**: Sometimes relics or card upgrades

---

## 5. CARD ACQUISITION

### 5.1 Card Reward System

After each combat victory:

```
┌────────────────────────────────────────┐
│          VICTORY!                       │
│                                         │
│  +65 Gold     +1 Random Potion         │
├────────────────────────────────────────┤
│  Choose a card to add to your deck:    │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ WATER GUN│  │  MURLOC  │  │HYDRO   ││
│  │ +1 Common│  │ +1 Common│  │PUMP    ││
│  │          │  │          │  │+1 Rare ││
│  │ Deal 4   │  │  2/3     │  │        ││
│  │ damage   │  │ Battlecry│  │Deal 8  ││
│  └──────────┘  └──────────┘  └────────┘│
│                                         │
│           [SKIP - No Card]              │
└────────────────────────────────────────┘
```

**Card Reward Rules:**
- Always get 3 choices (or skip)
- Rarity weighted by progress (more rares later)
- Cards match your deck's types more often
- Elites and Bosses give rarer cards

### 5.2 Shops & Merchants

**SHOP ENCOUNTERS** (appear every 3-4 battles):

```
┌────────────────────────────────────────┐
│      GOLDSHIRE MERCHANT                 │
│         "Welcome, hero!"                │
├────────────────────────────────────────┤
│  CARDS FOR SALE:                        │
│  • Dire Wolf (Rare) ........... 150g   │
│  • Battle Shout (Uncommon) ..... 80g   │
│  • Strike+ (Common) ............ 50g   │
│  • Hydro Pump (Rare) .......... 150g   │
│                                         │
│  RELICS:                                │
│  • Dragon Scale (Uncommon) .... 250g   │
│  • Hearthstone (Rare) ......... 300g   │
│                                         │
│  SERVICES:                              │
│  • Remove Card from Deck ....... 75g   │
│  • Upgrade a Card ............. 100g   │
│  • Heal 30 HP .................. 50g   │
│                                         │
│  Your Gold: 485g                        │
└────────────────────────────────────────┘
```

**SHOP STRATEGY:**
- Removing weak cards strengthens deck consistency
- Upgrading key cards increases power ceiling
- Buying relics provides permanent advantages
- Card purchases fill gaps in strategy

### 5.3 Special Encounters

**MYSTERY EVENTS** (random encounters):

#### Event Types:

**1. SHRINE OF FORTUNE**
```
Options:
A) Pray: Gain random relic (50% good, 50% cursed)
B) Donate 100g: Gain rare card
C) Leave: Nothing happens
```

**2. WILD TRAINER**
```
Challenge them to battle:
- Win: Get 3 rare cards to choose from
- Lose: Lose 50g and all potions
```

**3. ANCIENT LIBRARY**
```
Study tomes:
A) Upgrade 2 random cards
B) Transform 1 card into random card of higher rarity
C) Gain 3 copies of a common spell
```

**4. SOUL FORGE**
```
Sacrifice mechanic:
- Remove 5 cards from deck
- Gain 1 legendary card
```

**5. CURSED TREASURE**
```
Risk/reward:
A) Take cursed relic + 500g (relic has drawback)
B) Take normal relic
C) Leave
```

### 5.4 Rest Sites

**REST STOPS** (every 5-6 battles):

```
┌────────────────────────────────────────┐
│        CAMPFIRE REST                    │
│          🔥 Safe Zone 🔥                │
├────────────────────────────────────────┤
│  Choose ONE:                            │
│                                         │
│  🛌 REST                                │
│     Heal 30 HP                          │
│                                         │
│  ⚒️  SMITH                              │
│     Upgrade 1 card in your deck         │
│                                         │
│  💰 MERCHANT                            │
│     Access shop (costs 50g to enter)    │
│                                         │
│  🗑️  PURGE                              │
│     Remove 1 card from deck (free)      │
└────────────────────────────────────────┘
```

**Strategic Choices:**
- **Early game**: Upgrade key cards
- **Mid game**: Remove weak starters
- **Late game**: Heal if needed
- **Always**: Consider deck balance

### 5.5 Evolution System

Some creatures **EVOLVE** during the run:

**Evolution Triggers:**
- Reach X battles with creature in deck
- Play creature X times
- Win with creature on board
- Specific achievements

**Example Evolution Chain:**
```
MURLOC (1 cost, 2/3)
  ↓ (Win 5 battles)
MURLOC WARRIOR (2 cost, 4/5, Taunt)
  ↓ (Win 10 battles)
MURLOC KING (4 cost, 6/7, Taunt + Regen 2)
```

**Evolution Benefits:**
- Automatically upgrades all copies in deck
- Improves stats significantly
- Adds powerful abilities
- Permanent for rest of run

---

## 6. DECK ARCHETYPES (Detailed)

### 6.1 WATER SWARM
**Theme**: Many small water creatures + card draw

**Core Cards:**
- 6-8x Murloc/Water creatures (1-2 cost)
- 4x Bubble/Water Gun (cheap spells)
- 3x Tidal Surge (card draw)
- 2x Hydro Pump (finisher)

**Win Condition**: Flood board with creatures, overwhelm with numbers

**Key Synergies:**
- Murloc Synergy (draw cards when multiple on board)
- Water Resonance (+1/+1 to Water creatures per spell cast)
- Tide Caller (all Water creatures cost 1 less)

**Ideal Relics:**
- **Coral Crown**: Water creatures cost 1 less
- **Ocean's Blessing**: Draw extra card each turn
- **Tidal Talisman**: Start combat with 2 Murklocs

### 6.2 FIRE BURN
**Theme**: Direct damage, ignore creatures

**Core Cards:**
- 6x Burn spells (Ember, Firebolt, Flame Strike)
- 3x Imp (chip damage)
- 2x Inferno (high damage, risky)
- 2x Rage (energy boost)

**Win Condition**: Deal 60 damage directly to enemy HP

**Key Synergies:**
- Pyromania (spells deal +2 damage)
- Immolate (enemies burn for 2 per turn)
- Combustion (spells cost 1 less if enemy burning)

**Ideal Relics:**
- **Flameheart Crystal**: Spells deal +3 damage
- **Demon's Bargain**: Start with 1 extra energy, take 1 damage per turn
- **Molten Core**: Deal 2 damage to all enemies at start of turn

### 6.3 NATURE TANK
**Theme**: High HP creatures, healing, sustain

**Core Cards:**
- 4x Treant/Ancient Wisp (high HP)
- 6x Healing spells (Synthesis, Heal Pulse)
- 3x Grow/Nature's Blessing (buffs)
- 2x Defend

**Win Condition**: Outlast opponent, win through attrition

**Key Synergies:**
- Life Bloom (healing also grants +1/+1)
- Ironbark (Nature creatures have +2 HP)
- Regrowth (shuffle heals back into deck)

**Ideal Relics:**
- **Ancient Seed**: Heal 3 HP per turn
- **Nature's Guardian**: Start with 5 extra max HP
- **Eternal Grove**: Healing is 50% more effective

### 6.4 SHADOW POISON
**Theme**: Damage over time, debuffs

**Core Cards:**
- 6x Poison effects (Plague Strike, Toxic Bite)
- 4x Shadow Bolt/Shadow Claw
- 3x Curse/Weaken
- 2x Abomination (synergizes with poison)

**Win Condition**: Stack poison, stall with defense

**Key Synergies:**
- Virulence (Poison deals +1 damage)
- Contagion (Poison spreads to adjacent enemies)
- Necrotic Strike (deal damage equal to poison stacks)

**Ideal Relics:**
- **Plagued Vial**: Enemies start with Poison 2
- **Shadow Essence**: Poison lasts 1 extra turn
- **Death's Touch**: Poisoned enemies deal -2 damage

### 6.5 WARRIOR TEMPO
**Theme**: Efficient trades, board control

**Core Cards:**
- 5x Mid-cost creatures (Orc Grunt, Dire Wolf)
- 4x Battle Shout/Cleave (board buffs)
- 3x Execute/Cleave (removal)
- 3x Defend

**Win Condition**: Control board, pressure with efficient creatures

**Key Synergies:**
- Battle Rage (damaged creatures gain +2 ATK)
- Bloodthirst (deal 5 damage, gain 5 HP if enemy damaged)
- Warchief's Call (Warrior creatures cost 1 less)

**Ideal Relics:**
- **Banner of the Horde**: Warriors have +1/+1
- **Warlord's Axe**: Deal 3 damage at start of turn
- **Battle Standard**: Creatures attack twice if above half HP

### 6.6 DRAGON RAMP
**Theme**: Expensive dragons, ramp energy

**Core Cards:**
- 4x Dragon creatures (Whelp, Drake, Dragon)
- 4x Energy generation (Mana Crystal, Rage)
- 3x Stall cards (Defend, Barrier)
- 2x Dragon Rage/Outrage (finishers)

**Win Condition**: Survive to late game, play huge dragons

**Key Synergies:**
- Dragon Hoard (dragons give +1 max energy)
- Draconic Power (dragons have +2/+2)
- Ancient Wyrm (reduce dragon costs by 1)

**Ideal Relics:**
- **Dragon Scale**: Dragons cost 1 less
- **Wyrm's Hoard**: Start with 1 extra max energy
- **Ancient Egg**: Start combat with Whelp in play

### 6.7 UNDEAD SACRIFICE
**Theme**: Sacrifice creatures for powerful effects

**Core Cards:**
- 6x Cheap undead (Ghoul, Skeleton)
- 4x Sacrifice spells (Corpse Explosion, Dark Pact)
- 3x Abomination (gets stronger from deaths)
- 2x Resurrection effects

**Win Condition**: Sacrifice weak creatures for explosive turns

**Key Synergies:**
- Death Pact (when ally dies, draw 2 cards)
- Corpse Field (dead creatures become +1/+1 buffs)
- Lich's Bargain (sacrifice creature: gain 3 energy)

**Ideal Relics:**
- **Phylactery**: First creature death each turn summons Skeleton
- **Death Coil**: Whenever ally dies, deal 3 damage
- **Lich King's Crown**: Undead have +1/+1

---

## 7. VISUAL DESIGN

### 7.1 Card Layout

**CREATURE CARD ANATOMY:**
```
┌─────────────────────────────────────┐
│ NAME                    [RARITY]    │ ← Name + Rarity gem
│ [Type Icons]                        │ ← Type symbols
│ Cost: X Energy          [Set Icon]  │ ← Cost + Set
├─────────────────────────────────────┤
│                                     │
│        [CREATURE ARTWORK]           │ ← Art (ASCII/pixel)
│         (pixelated/ASCII)           │
│                                     │
├─────────────────────────────────────┤
│ ATK: X    HP: X         [Keywords]  │ ← Stats
├─────────────────────────────────────┤
│ [ABILITY TEXT]                      │ ← Full ability
│ Description of special ability or   │
│ effect triggers. Can be multiple    │
│ lines for complex cards.            │
├─────────────────────────────────────┤
│ "Flavor text quote"                 │ ← Optional flavor
└─────────────────────────────────────┘
```

**SPELL CARD ANATOMY:**
```
┌─────────────────────────────────────┐
│ NAME                    [RARITY]    │
│ [Type Icons]                        │
│ Cost: X Energy                      │
├─────────────────────────────────────┤
│                                     │
│        [SPELL EFFECT ART]           │
│     (VFX visualization)             │
│                                     │
├─────────────────────────────────────┤
│ [EFFECT TEXT]                       │
│ Clear description of immediate      │
│ effect when cast.                   │
│                                     │
│ [SECONDARY EFFECT]                  │
│ Additional conditions or upgrades.  │
└─────────────────────────────────────┘
```

### 7.2 Color Schemes by Type

**WATER** - Blues and Teals
```
Primary: #4169E1 (Royal Blue)
Secondary: #00CED1 (Dark Turquoise)
Accent: #87CEEB (Sky Blue)
```

**FIRE** - Reds and Oranges
```
Primary: #DC143C (Crimson)
Secondary: #FF4500 (Orange Red)
Accent: #FFD700 (Gold)
```

**NATURE** - Greens and Browns
```
Primary: #228B22 (Forest Green)
Secondary: #8B4513 (Saddle Brown)
Accent: #90EE90 (Light Green)
```

**SHADOW** - Purples and Blacks
```
Primary: #4B0082 (Indigo)
Secondary: #2F2F2F (Dark Gray)
Accent: #9370DB (Medium Purple)
```

**DRAGON** - Golds and Reds
```
Primary: #FFD700 (Gold)
Secondary: #B8860B (Dark Goldenrod)
Accent: #8B0000 (Dark Red)
```

**UNDEAD** - Grays and Greens
```
Primary: #696969 (Dim Gray)
Secondary: #556B2F (Dark Olive Green)
Accent: #98FB98 (Pale Green)
```

### 7.3 Battlefield Layout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ENEMY STATUS                     ⚔️ HP: 45/60┃
┃ Energy: 0/3  Block: 8  Intent: Attack for 12┃
┠──────────────────────────────────────────────┨
┃ ENEMY CREATURES (MAX 5)                      ┃
┃ ┌────────┐ ┌────────┐ ┌────────┐            ┃
┃ │ Gnoll  │ │ Kobold │ │  Wolf  │    [Empty] ┃
┃ │ ⚔️ 4 🛡️ 3│ │ ⚔️ 2 🛡️ 2│ │ ⚔️ 3 🛡️ 3│    slots┃
┃ │  [🌟]  │ │        │ │ [Quick]│            ┃
┃ └────────┘ └────────┘ └────────┘            ┃
┠──────────────────────────────────────────────┨
┃         ≈≈≈ BATTLEFIELD ≈≈≈                  ┃
┃    [Combat animations happen here]           ┃
┠──────────────────────────────────────────────┨
┃ YOUR CREATURES (MAX 5)                       ┃
┃ ┌────────┐ ┌────────┐                       ┃
┃ │ Murloc │ │  Wisp  │      [Empty slots]    ┃
┃ │ ⚔️ 2 🛡️ 3│ │ ⚔️ 1 🛡️ 4│                      ┃
┃ │Battlecry│ │ Regen 2│                      ┃
┃ └────────┘ └────────┘                       ┃
┠──────────────────────────────────────────────┨
┃ YOUR STATUS                      🛡️ HP: 52/60┃
┃ Energy: 3/3  Block: 12  Potions: 2           ┃
┠══════════════════════════════════════════════┨
┃ HAND (5 cards)                 Deck: 18/25  ┃
┃ ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐        ┃
┃ │Water││Strike││Defend││Murloc││Heal│        ┃
┃ │ Gun ││  5  ││  +5 ││ 2/3 ││ +5 │        ┃
┃ │  1⚡││  1⚡││  1⚡││  1⚡ ││ 1⚡│        ┃
┃ └─────┘└─────┘└─────┘└─────┘└─────┘        ┃
┠──────────────────────────────────────────────┨
┃ Discard: 8      [END TURN]      Exhaust: 2  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### 7.4 UI Polish & Effects

**CARD HOVER EFFECTS:**
- Glow matching card type color
- Slight lift/scale animation
- Show full description tooltip
- Preview targeting reticle

**PLAY ANIMATIONS:**
- Card slides to board position
- Flash of type-colored energy
- Sound effect matches card type
- Particle burst on impact

**DAMAGE NUMBERS:**
- Pop up from damaged target
- Red for damage, green for healing
- Critical hits larger and golden
- Overkill shows skull icon

**STATUS EFFECTS:**
- Floating icons above creatures
- Poison: green bubbles
- Regen: green sparkles
- Strength: red aura
- Weak: gray cloud

**ENERGY ORB DISPLAY:**
```
Energy: ⚡⚡⚡ (3/3 available)
Spent:  ◯◯◯ (0/3 spent)
```

---

## 8. PROGRESSION SYSTEM

### 8.1 Run Structure

**ACT 1: GOLDSHIRE FOREST** (8-10 battles)
- Enemies: Gnolls, Kobolds, Wolves, Spiders
- Boss: **MURADIN** (Forge Master)
  - 80 HP, summons Elementals
  - Reward: Forge Badge + Rare card choice

**ACT 2: ASHENVALE WILDS** (10-12 battles)
- Enemies: Wisps, Treants, Naga, Felhounds
- Boss: **MALFURION** (Archdruid)
  - 100 HP, heals and buffs Nature creatures
  - Reward: Nature Badge + Epic card choice

**ACT 3: FROZEN WASTES** (12-15 battles)
- Enemies: Undead, Elementals, Abominations
- Boss: **JAINA** (Frost Mage)
  - 120 HP, powerful frost spells
  - Reward: Frost Badge + Epic card choice

**ACT 4: ORGRIMMAR ARENA** (15+ battles)
- Enemies: Orcs, Dragons, Demons, Infernals
- Boss: **THRALL** (Warchief)
  - 150 HP, elemental mastery
  - Reward: Storm Badge + Legendary choice

**FINAL ACT: ELITE FOUR** (4 boss fights)
- No healing between fights
- Ultimate challenge
- Victory = Win run, unlock new cards

### 8.2 Map & Path Choices

**MAP NODE TYPES:**
```
⚔️  = Combat (Normal enemy)
💀 = Elite Combat (Harder, better rewards)
💰 = Shop
🔥 = Rest Site
❓ = Mystery Event
👑 = Boss
🎁 = Treasure (free reward)
```

**SAMPLE ACT MAP:**
```
                    👑 BOSS
                   / | \
                 💀 🔥  💰
                / | X | \
              ⚔️  ❓ 💰 💀
             / | X | X | \
           ⚔️  ⚔️  ⚔️  ⚔️  ⚔️
            \ | X | X | /
              ⚔️  🎁  ⚔️
               \ | /
                START
```

**PATH STRATEGY:**
- More combats = more cards/gold
- Elite fights = risky but rewarding
- Rest sites = essential for upgrades
- Mystery events = random, can be huge

### 8.3 Meta Progression (Between Runs)

**UNLOCKABLES:**
- New starter decks (unlock at Act 2, 3, 4)
- New cards added to card pool
- New relics become available
- Harder difficulty modes
- Challenge runs with modifiers

**ACHIEVEMENTS:**
```
🏆 First Victory - Complete Act 1
🏆 Dragon Slayer - Defeat a Dragon boss
🏆 Collector - Collect 50 unique cards
🏆 Minimalist - Win with 15-card deck
🏆 Maximalist - Win with 40-card deck
🏆 Speed Runner - Win in under 30 minutes
🏆 Perfectionist - Win without losing HP
🏆 Master Duelist - Complete Elite Four
```

**CARD UNLOCKS:**
```
Win with Water deck → Unlock "Tidal Wave" card
Win with Fire deck → Unlock "Inferno Blast" card
Defeat 10 Dragons → Unlock "Dragon Aspect" relic
Complete 5 runs → Unlock "Legendary Starter" deck
```

### 8.4 Difficulty Modes (Ascension)

**ASCENSION LEVELS** (1-20, unlock after first win):

**A1**: Elites have +10% HP
**A2**: Start with 1 curse card in deck
**A3**: Bosses have new abilities
**A5**: Enemies gain 1 Strength each turn
**A7**: Card removal costs 100g (up from 75g)
**A10**: Start with 50 HP (down from 60)
**A12**: Elites appear more frequently
**A15**: Final boss has 200 HP (up from 150)
**A18**: Shop prices increased 25%
**A20**: All enemies +50% HP/damage

Higher ascension = bragging rights + exclusive unlocks

### 8.5 Daily Challenges

**DAILY RUN:**
- Fixed seed for all players
- Compete on leaderboard
- Special modifiers active
- Unique rewards

**EXAMPLE MODIFIERS:**
```
"Spell Power": All spells deal double damage
"Big Deck Energy": Start with 30 cards
"Speed Run": 5 minute time limit per act
"Legendary Draft": All card rewards are legendary
"Chaos Mode": Random effect each turn
```

---

## 9. TECHNICAL IMPLEMENTATION

### 9.1 Data Structures

**CARD OBJECT:**
```javascript
{
  id: "murloc_warrior",
  name: "Murloc Warrior",
  type: ["water", "beast"],
  cardType: "creature", // or "spell" or "relic"
  rarity: "uncommon",
  cost: 2,
  attack: 4,
  health: 5,
  keywords: ["taunt", "battlecry"],
  abilities: [
    {
      trigger: "battlecry",
      effect: "draw_card",
      condition: "has_water_ally"
    }
  ],
  description: "Taunt. Battlecry: Draw a card if you control another Water creature.",
  flavorText: "Mrglglglgl!",
  upgraded: false,
  upgradeChanges: {
    attack: +1,
    health: +1,
    cost: -1
  }
}
```

**GAME STATE:**
```javascript
{
  player: {
    hp: 52,
    maxHp: 60,
    block: 12,
    energy: 3,
    maxEnergy: 3,
    deck: [...cardObjects],
    hand: [...cardObjects],
    discard: [...cardObjects],
    exile: [...cardObjects],
    creatures: [...activeCreatures],
    relics: [...relicObjects],
    gold: 485,
    potions: [...potionObjects]
  },
  enemy: {
    hp: 45,
    maxHp: 60,
    block: 8,
    energy: 3,
    creatures: [...activeCreatures],
    intent: { type: "attack", value: 12 },
    ai: "aggressive" // or "defensive", "random"
  },
  battlefield: {
    turn: 5,
    effects: [...globalEffects]
  },
  run: {
    act: 2,
    floor: 12,
    path: [...mapNodes],
    seed: 12345
  }
}
```

### 9.2 Core Systems

**COMBAT SYSTEM:**
1. Initialize combat (shuffle deck, draw hand, set energy)
2. Start turn (draw cards, gain energy, process start effects)
3. Player phase (play cards, attack, end turn)
4. Enemy phase (AI plays cards, attacks)
5. Check win/loss conditions
6. Repeat until combat ends

**CARD PLAY SYSTEM:**
```javascript
function playCard(card, targets) {
  // Check if can afford
  if (player.energy < card.cost) return false;

  // Spend energy
  player.energy -= card.cost;

  // Execute card effect
  if (card.cardType === "creature") {
    summonCreature(card);
  } else if (card.cardType === "spell") {
    castSpell(card, targets);
  }

  // Trigger effects
  triggerEffects("on_card_played", card);

  // Move to discard (unless Exhaust)
  if (!card.hasKeyword("exhaust")) {
    player.discard.push(card);
  } else {
    player.exile.push(card);
  }

  return true;
}
```

**AI SYSTEM:**
```javascript
function enemyTurn() {
  // Decide intent based on AI type
  const intent = decideIntent(enemy.ai, gameState);

  // Show intent to player
  displayIntent(intent);

  // Execute intent next turn
  executeIntent(intent);

  // Attack with creatures
  enemy.creatures.forEach(creature => {
    attackTarget(creature, chooseTarget());
  });
}

function decideIntent(aiType, state) {
  switch(aiType) {
    case "aggressive":
      return { type: "attack", value: calculateDamage() };
    case "defensive":
      return state.player.damage > 10
        ? { type: "attack" }
        : { type: "defend", value: 10 };
    case "adaptive":
      return analyzeThreats(state);
  }
}
```

### 9.3 Performance Optimizations

**CARD RENDERING:**
- Cache rendered card images
- Use sprite sheets for card art
- Only render visible cards
- Virtualize large lists (deck view)

**ANIMATION SYSTEM:**
- Queue animations, don't block
- Skip animations option
- Fast mode for speedrunners
- Batch similar animations

**SAVE SYSTEM:**
```javascript
// Auto-save after each action
function saveGameState() {
  const saveData = {
    timestamp: Date.now(),
    version: "1.0",
    player: serializePlayer(),
    run: serializeRun(),
    settings: userSettings
  };

  localStorage.setItem("wowmon_save", JSON.stringify(saveData));
}

// Load on startup
function loadGameState() {
  const saved = localStorage.getItem("wowmon_save");
  if (saved) {
    const data = JSON.parse(saved);
    restoreGameState(data);
  }
}
```

### 9.4 Responsive Design

**MOBILE LAYOUT:**
```
┌──────────────────┐
│ Enemy: 45/60 HP  │
│ Intent: ⚔️ 12    │
├──────────────────┤
│ ┌───┐ ┌───┐     │
│ │Gnoll│Wolf│     │  ← Swipeable
│ └───┘ └───┘     │
├──────────────────┤
│  Battlefield     │
├──────────────────┤
│ ┌───┐            │
│ │Murloc│         │  ← Tap to select
│ └───┘            │
├──────────────────┤
│ You: 52/60 HP    │
│ Energy: ⚡⚡⚡    │
├══════════════════┤
│ ┌──┐┌──┐┌──┐   │
│ │1⚡││1⚡││2⚡│   │  ← Swipe left/right
│ └──┘└──┘└──┘   │
│ [End Turn]       │
└──────────────────┘
```

**TOUCH CONTROLS:**
- Drag cards to play
- Tap creatures to attack
- Swipe hand to scroll
- Long-press for card details
- Pinch to zoom battlefield

---

## 10. BALANCE & DESIGN PHILOSOPHY

### 10.1 Core Principles

**1. EASY TO LEARN, HARD TO MASTER**
- Simple mechanics (energy, creatures, spells)
- Deep interactions (synergies, combos)
- Clear feedback (intent system, damage preview)
- Skill expression through deck building

**2. MEANINGFUL CHOICES**
- Every card pick matters
- Deck size vs consistency tradeoff
- Risk/reward in path selection
- Build flexibility (can pivot strategies)

**3. EXCITING MOMENTS**
- Big combo turns feel satisfying
- Lucky card draws can turn fights
- Clutch victories at low HP
- Discovering new synergies

**4. REPLAYABILITY**
- Randomized runs (different enemies, cards)
- Multiple viable archetypes
- Daily challenges
- Ascension difficulty scaling

**5. NO PAY-TO-WIN**
- All cards unlockable through play
- No paid power, only cosmetics
- Fair progression curve
- Skill determines success

### 10.2 Balance Guidelines

**ENERGY CURVE:**
```
0 cost: Weak utility (Defend, simple effects)
1 cost: Basic creatures (2/3, 3/2) and spells (5 damage)
2 cost: Good creatures (3/4, 4/3) and removal
3 cost: Strong effects (6/5 creatures, 8 damage)
4+ cost: Game-enders (legendary creatures, board clears)
```

**CREATURE STAT FORMULA:**
```
Total stats (ATK + HP) ≈ Cost * 5
Examples:
- 1 cost: 2/3 = 5 total
- 2 cost: 3/4 = 7 total (less than 10 due to ability)
- 3 cost: 5/4 = 9 total
- 4 cost: 6/7 = 13 total
```

**SPELL DAMAGE FORMULA:**
```
Damage ≈ Cost * 5 (for pure damage)
- 1 cost: 5-6 damage
- 2 cost: 8-10 damage
- 3 cost: 12-15 damage
- 4 cost: 18-20 damage
```

**RARITY POWER LEVELS:**
- **Common**: Slightly below curve, simple
- **Uncommon**: On curve, moderate synergy
- **Rare**: Above curve, strong synergy
- **Epic**: Build-around, unique mechanics
- **Legendary**: Powerful but balanced, flashy

### 10.3 Counterplay & Interaction

**EVERY DECK HAS WEAKNESSES:**
- Aggro weak to: Taunt creatures, healing, board clears
- Control weak to: Burn damage, fast pressure, exile effects
- Combo weak to: Disruption, aggression, hand attack

**SIDEBOARD SYSTEM** (Advanced):
- After Act 1, unlock sideboard (5 cards)
- Between fights, swap cards in/out
- Adapt to upcoming boss
- Rewards strategic planning

**COUNTERPLAY CARDS:**
```
- Silence: Removes abilities from creature
- Dispel: Removes all buffs from target
- Counter Spell: Negate enemy spell
- Discard: Force enemy to discard cards
- Energy Drain: Enemy loses energy
```

### 10.4 Power Creep Prevention

**DESIGN RULES:**
1. New cards fill niches, don't outclass old cards
2. Legendaries are flashy, not strictly better
3. Commons remain viable in all decks
4. Archetypes stay balanced relative to each other
5. Regular balance patches based on win rates

**PATCH PROCESS:**
```
1. Collect data (win rates, card pick rates)
2. Identify overperforming cards (>60% win rate)
3. Identify underperforming (<35% win rate)
4. Nerf overperformers (cost +1, stats -1)
5. Buff underperformers (add keyword, lower cost)
6. Test changes in beta branch
7. Deploy to live with patch notes
```

---

## 11. MONETIZATION (Optional, Fair)

### 11.1 Cosmetic Only

**WHAT CAN BE SOLD:**
- Card backs (visual themes)
- Battlefield skins (different arenas)
- Creature skins (alternate art)
- Emotes and voice lines
- Profile icons and borders

**WHAT CANNOT BE SOLD:**
- Cards (all unlockable)
- Relics (all earnable)
- Deck slots (unlimited)
- Power boosts (never)

### 11.2 Battle Pass (Seasonal)

**FREE TRACK:**
- Common/uncommon cosmetics
- Profile rewards
- Card back variants

**PREMIUM TRACK ($10/season):**
- Exclusive legendary card back
- Animated creature skins
- Voice line pack
- Profile border with effects
- Does NOT include gameplay advantages

### 11.3 One-Time Purchases

**SUPPORTER PACK ($20):**
- Exclusive "Supporter" title
- Unique profile border
- Thanks in credits
- Support development

**COSMETIC BUNDLES ($5-15):**
- Themed card back + battlefield
- Complete creature skin set
- Voice line collection

---

## 12. FUTURE EXPANSIONS

### 12.1 New Card Sets

**EXPANSION 1: "Burning Legion"**
- 50 new cards
- New mechanic: **Infernal** (power grows each turn)
- New tribe: Demons
- New legendary: **Archimonde**

**EXPANSION 2: "Wrath of the Lich King"**
- 50 new cards
- New mechanic: **Frostbite** (freeze effects)
- New tribe: Death Knights
- New legendary: **Arthas**

**EXPANSION 3: "Cataclysm"**
- 50 new cards
- New mechanic: **Shatter** (destroy damaged creatures)
- New tribe: Elementals
- New legendary: **Deathwing**

### 12.2 New Game Modes

**ARENA MODE:**
- Draft deck from random cards
- Play until 3 losses or 12 wins
- Rewards based on wins
- Leaderboards

**CO-OP MODE:**
- 2 players vs strong boss
- Shared HP pool
- Complementary decks
- Exclusive rewards

**PVP MODE:**
- Direct player vs player
- Ranked ladder
- Seasonal rewards
- Tournament support

**ROGUELIKE+ MODE:**
- Infinite runs with branching paths
- Unlock new cards as you progress
- Permadeath with meta progression
- Leaderboards for longest runs

### 12.3 Advanced Features

**DECK SHARING:**
```
Share deck code: WOWMON-AAECAa0G...
Players can import/export decks
Community deck building
Streamer showcase decks
```

**REPLAY SYSTEM:**
- Save epic runs
- Share with friends
- Learn from mistakes
- Watch top players

**STAT TRACKING:**
- Win rate by deck
- Card performance analytics
- Personal records
- Achievement progress

---

## 13. MARKETING TAGLINES

**"Collect. Combine. Conquer."**

**"Every run is a new adventure in Azeroth."**

**"Build your legend, one card at a time."**

**"Strategic deck building meets Warcraft creatures."**

---

## 14. CONCLUSION

This redesign transforms **WowMon** into a strategic deck-building card game that combines:

✅ **Deep Strategy** - Meaningful choices in deck construction and card play
✅ **Easy Learning Curve** - Simple core mechanics, complex interactions
✅ **High Replayability** - Randomized runs, multiple archetypes, daily challenges
✅ **Satisfying Combos** - Exciting synergies and powerful turns
✅ **Fair Progression** - Skill-based, no pay-to-win
✅ **Warcraft Theme** - Maintains beloved creatures and lore

**Target Audience:**
- Slay the Spire fans
- Warcraft enthusiasts
- Card game players
- Roguelike lovers
- Strategic thinkers

**Estimated Playtime:**
- Single run: 45-90 minutes
- Full meta progression: 50+ hours
- Mastery (Ascension 20): 200+ hours

**Platform:**
- Web-based (HTML5)
- Mobile-friendly
- Offline playable
- Cross-platform saves

This design creates a **compelling, strategic, and endlessly replayable** card game that honors the WowMon creature collection while innovating with deck-building mechanics. It's accessible to newcomers but offers deep mastery for dedicated players.

---

**Ready to build your deck and conquer Azeroth? The cards await!** 🃏⚔️🔥
