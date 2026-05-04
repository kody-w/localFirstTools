# NARRATIVE DESIGN PATTERNS - QUICK REFERENCE
## WoWmon Story-Driven Features

**Quick lookup for implementing story elements**

---

## STORY BEATS - PACING GUIDE

### Act Structure
```
Act 1 (Levels 1-15):  Hook + World Introduction
Act 2 (Levels 15-30): Rising Action + Major Choice
Act 3 (Levels 30-45): Climax Build + Dark Hour
Act 4 (Levels 45-50): Resolution + Multiple Endings
```

### Beat Frequency
- **Main Story Quest**: Every 5 levels
- **Character Development**: Every 3-4 levels
- **Major Choice**: Every act
- **Boss Battle**: End of each act + mid-act miniboss
- **Emotional Moment**: Every 7-8 levels

---

## DIALOGUE PATTERNS

### Three-Line Rule
Every important dialogue should follow: Setup → Reveal → Impact
```javascript
// Example
"I've been watching you, trainer.",           // Setup
"The shadow chose you... just like it chose me.", // Reveal
"We're the same, you and I."                   // Impact
```

### Choice Design
Always offer 3 choices representing:
1. **Compassionate** (bond +5-10)
2. **Pragmatic** (neutral, unlocks items/info)
3. **Aggressive** (bond -5, power/money reward)

### NPC Voice Guide
- **Professor Bronzebeard**: Wise mentor, speaks in metaphors
- **Captain Alara**: Direct, military, protective
- **Lyra Dawnseeker**: Curious, explains lore, asks questions
- **Grimtusk**: Gruff, suspicious, slowly warms up
- **Rival**: Mirrors player choices, becomes darker or lighter

---

## BOSS DESIGN FORMULA

### Phase Structure
```
Phase 1: Learn the patterns (100-60% HP)
Phase 2: Increased difficulty (60-30% HP)
Phase 3: Desperation + Ultimate (30-0% HP)
```

### Mechanics Per Phase
- **Phase 1**: 3-4 basic abilities, predictable
- **Phase 2**: +2 new abilities, one mechanic (adds/traps/etc)
- **Phase 3**: Ultimate ability + transformation

### Boss Dialogue Timing
```javascript
Intro: Before battle starts
Phase 2: At transition (dramatic moment)
Phase 3: When ultimate charges
Victory: Different based on how you won
```

---

## QUEST DESIGN TEMPLATES

### Investigation Quest
```
1. Talk to NPC (learn about problem)
2. Explore 2-3 locations (find clues)
3. Battle encounters (defend/clear area)
4. Collect evidence (items/samples)
5. Return to NPC (reveal truth)
```

### Rescue Quest
```
1. Urgent message/request
2. Race against time element
3. Clear path of enemies
4. Boss or miniboss encounter
5. Choice: save NPC or secure objective
```

### Character Development Quest
```
1. Personal conversation (bond requirement)
2. Flashback or story reveal
3. Confront NPC's past (symbolic battle)
4. Make choice that defines relationship
5. Reward: unique ability/creature/item
```

### Mystery Quest
```
1. Strange occurrence
2. Gather clues from multiple NPCs
3. Hidden area exploration
4. Revelation cutscene
5. Choice impacts world state
```

---

## MEMORY SYSTEM TRIGGERS

### When to Create Memories

**Minor Memories** (tracked but not announced):
- Defeat 10+ enemies of same type
- Visit location 3+ times
- Use same creature for 5+ battles

**Major Memories** (journal entries):
- Boss defeats
- NPC deaths or saves
- Major story choices
- Emotional cutscenes
- Legendary captures

**Critical Memories** (affect ending):
- Faction choices
- Sacrifice decisions
- Betrayals
- Redemptions

---

## CHOICE CONSEQUENCE MATRIX

### Immediate Consequences (Same session)
```
Choice Made → Dialogue change → Small reward/penalty
```

### Medium-Term (Next act)
```
Choice Made → NPC availability → Quest availability
```

### Long-Term (Ending)
```
Choice Made → World state → Ending variant → Post-game content
```

### Example Flow
```
Save corrupted creature (Act 1)
  ↓
NPC remembers your compassion (Act 2)
  ↓
They help you in critical moment (Act 3)
  ↓
Appear in your ending cutscene (Act 4)
  ↓
Available as post-game ally (Post-game)
```

---

## EMOTIONAL BEATS CHECKLIST

Every act should include:

✓ **Hope** - Victory, new ally, discovery
✓ **Fear** - Threat revealed, power displayed
✓ **Loss** - Something taken away (temporary)
✓ **Triumph** - Overcome obstacle, boss defeated
✓ **Wonder** - Explore beautiful area, lore reveal
✓ **Anger** - Injustice witnessed, villain action
✓ **Relief** - Danger passed, safe zone reached
✓ **Sacrifice** - Give something for greater good

---

## NPC RELATIONSHIP MILESTONES

### Bond Level Unlocks
```
Level 1 (0-20):   Basic dialogue, quest giver
Level 2 (21-40):  Personal questions, small favors
Level 3 (41-60):  Backstory revealed, unique quest
Level 4 (61-80):  Deep bond, combat assistance
Level 5 (81-100): Max bond, legendary reward, always available
```

### Bond Gain Sources
- Dialogue choices: ±5
- Complete their quest: +10
- Save their life: +20
- Betray their trust: -30
- Give them gift: +5
- Battle alongside: +3 per battle

---

## BOSS AI PERSONALITIES

### Aggressive
- Always attacks
- Highest power move
- No defensive moves
- High risk/reward

### Defensive
- Uses buffs and healing
- Waits for player mistakes
- Counter-attacks
- Long battle, tests patience

### Intelligent
- Adapts to player team
- Switches strategies
- Exploits weaknesses
- Pattern changes each phase

### Chaotic
- Random move selection
- Unpredictable patterns
- High variance damage
- Can't be learned easily

---

## CUTSCENE COMPOSITION

### Visual Novel Style
```
[Character Portrait Left] [Text Box] [Character Portrait Right]
           ↓                  ↓                ↓
        Emotion           Dialogue       Emotion Response
```

### Action Sequence
```
Wide shot (establish) →
Close up (emotion) →
Action shot (impact) →
Reaction shot (consequence)
```

### Dialogue Only (minimal)
```
Character name + emotion indicator
Dialogue line 1
Dialogue line 2
[Choice prompt if applicable]
```

---

## PACING RULES

### Combat to Story Ratio
- **Early game**: 60% combat, 40% story
- **Mid game**: 50% combat, 50% story
- **Late game**: 40% combat, 60% story
- **Post-game**: 70% combat, 30% story

### Intensity Curve
```
Tutorial → Ramp up → Boss → Cooldown → Repeat
  5min       10min     10min    5min
```

### Dialogue Length Limits
- **Overworld NPC**: 3-5 lines max
- **Quest giver**: 5-8 lines
- **Cutscene**: 10-15 lines
- **Boss intro**: 4-6 lines
- **Choices**: 1-2 lines per option

---

## WORLD STATE FLAGS

### Track These
```javascript
flags = {
    // Progress gates
    gymsDefeated: [],
    badgesOwned: [],
    regionsUnlocked: [],

    // Story milestones
    actComplete: [false, false, false, false],
    majorBossesDefeated: [],

    // World changes
    corruptionLevel: 0,
    villageSaved: {},
    npcAlive: {},

    // Relationships
    companionsMet: [],
    enemiesMade: [],
    alliedsGained: []
}
```

### Trigger World Changes
- Corruption 0-25%: Normal world
- Corruption 26-50%: Some areas affected
- Corruption 51-75%: Major changes, dark atmosphere
- Corruption 76-100%: World on brink of destruction

---

## ACHIEVEMENT DESIGN

### Types
**Progression**: Natural story completion
**Challenge**: Difficult optional objectives
**Collection**: Gather all of something
**Mastery**: Perfect execution required
**Secret**: Hidden, discovery-based

### Reward Structure
- **Bronze**: Common, participation
- **Silver**: Uncommon, skill required
- **Gold**: Rare, dedicated players
- **Platinum**: Ultra rare, completionists

---

## WRITING TIPS

### Show Don't Tell
❌ "The creature is angry"
✓ "The creature's eyes glow red. It snarls."

### Active Voice
❌ "The village was destroyed by the shadow"
✓ "The shadow destroyed the village"

### Emotional Words
Use sparingly for impact:
- Love, hate, terror, hope, despair
- Save for critical moments

### Player Agency
❌ "You decide to help"
✓ "Will you help? [Choice]"

### Brevity
- Cut unnecessary words
- Every line should advance story or character
- When in doubt, shorter is better

---

## TESTING CHECKLIST

### Story Flow
- [ ] Can complete without getting stuck
- [ ] All choices lead somewhere
- [ ] Consequences make sense
- [ ] NPCs remember player actions

### Emotional Impact
- [ ] At least 3 emotional moments per act
- [ ] Earned, not manipulative
- [ ] Player choices matter
- [ ] Satisfying resolution

### Balance
- [ ] Story doesn't interrupt gameplay too much
- [ ] Gameplay supports story themes
- [ ] Optional content feels rewarding
- [ ] Mandatory content is paced well

### Accessibility
- [ ] Can skip cutscenes (after first viewing)
- [ ] Text speed adjustable
- [ ] Difficult choices clearly explained
- [ ] Screen reader compatible

---

## COMMON PITFALLS TO AVOID

### ❌ Don't Do This
1. **Fake choices** - All options lead to same outcome
2. **Cutscene spam** - Too much story, not enough play
3. **Unclear objectives** - Player doesn't know what to do
4. **Inconsistent characters** - NPCs act randomly
5. **Deus ex machina** - Problems solved by coincidence
6. **Forced emotion** - Trying too hard to be sad/epic
7. **Info dumps** - Walls of exposition text
8. **Forgotten consequences** - Choices don't matter

### ✓ Do This Instead
1. **Real choices** - Different outcomes, consequences
2. **Story chunks** - Short, digestible story moments
3. **Clear goals** - Always know what's next
4. **Character consistency** - NPCs stay true to themselves
5. **Earned victories** - Player agency solves problems
6. **Natural emotion** - Build up to emotional moments
7. **Show lore** - Environmental storytelling
8. **Memory system** - Game remembers everything

---

## QUICK IMPLEMENTATION PRIORITIES

### Week 1: Foundation
1. Story state tracking
2. Quest system basics
3. Dialogue with choices
4. Save/load story data

### Week 2: Content Creation
1. Write Act 1 main quest
2. Create 3-4 side quests
3. Design first boss
4. Add 5 key NPCs

### Week 3: Systems
1. Memory system
2. Consequence engine
3. Bond system
4. Journal

### Week 4: Polish
1. Test all story paths
2. Balance boss encounters
3. Proofread all dialogue
4. Add accessibility features

---

## NARRATIVE RESOURCES

### Inspiration Sources
- **Pokemon**: Mystery Dungeon series (story)
- **Undertale**: Consequence system
- **Fire Emblem**: Support conversations
- **Persona**: Social links/bonds
- **Final Fantasy**: Epic moments
- **Dark Souls**: Environmental storytelling
- **Mass Effect**: Choice consequences

### Writing Exercise
Before implementing, write:
1. One-paragraph story summary
2. Three key emotional moments
3. Five major choice points
4. Beginning and ending scenes
5. Main antagonist motivation

---

## FINAL CHECKLIST BEFORE LAUNCH

Story:
- [ ] Beginning hooks player
- [ ] Middle maintains interest
- [ ] Ending feels satisfying
- [ ] Choices matter
- [ ] Characters memorable

Technical:
- [ ] All quests completable
- [ ] No soft locks
- [ ] Saves preserve story state
- [ ] Bugs fixed
- [ ] Accessible

Polish:
- [ ] Dialogue proofread
- [ ] Pacing feels good
- [ ] Boss battles balanced
- [ ] Rewards satisfying
- [ ] Post-game content

---

**Remember**: Story serves gameplay, gameplay serves story. They should enhance each other, never fight for attention.

**Core Rule**: If a story element doesn't make the game more fun or meaningful, cut it.

**Golden Ratio**: 70% player agency, 30% authored narrative.

---

END OF QUICK REFERENCE
