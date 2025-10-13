# AGENT 7: STORY-DRIVEN IMPLEMENTATION GUIDE
## WoWmon Narrative System - Code Examples & Integration

**Document Version:** 1.0
**Date:** 2025-10-12
**Companion to:** AGENT7_STORY_DRIVEN_STRATEGY_DESIGN.md

---

## TABLE OF CONTENTS

1. [Core Story Engine](#1-core-story-engine)
2. [Quest System Implementation](#2-quest-system-implementation)
3. [Dialogue System](#3-dialogue-system)
4. [Boss Battle Framework](#4-boss-battle-framework)
5. [Team Builder Integration](#5-team-builder-integration)
6. [Memory & Consequence System](#6-memory--consequence-system)
7. [Integration with Existing Code](#7-integration-with-existing-code)

---

## 1. CORE STORY ENGINE

### 1.1 Story State Manager

Add to the existing GameEngine class:

```javascript
// Add to GameEngine initialization
initStoryEngine() {
    this.story = {
        // Current progress
        currentAct: 1,
        actProgress: 0,
        currentQuest: null,
        activeQuests: [],
        completedQuests: [],

        // Player choices and flags
        majorChoices: new Map(),
        storyFlags: {
            starterChosen: false,
            firstGymDefeated: false,
            corruptionDiscovered: false,
            betrayalRevealed: false,
            finalBattleUnlocked: false
        },

        // World state
        worldState: {
            corruptionLevel: 0,
            regionsUnlocked: ['goldshire'],
            gymsDefeated: [],
            npcsMetCount: 0
        },

        // NPC relationships
        npcRelationships: new Map(),

        // Faction reputation
        factionRep: {
            alliance: 0,
            horde: 0,
            neutral: 100
        },

        // Memory system
        memories: []
    };

    // Story event handlers
    this.storyEvents = new Map();
    this.registerStoryEvents();
}

// Story progression method
progressStory(questId, progress) {
    const quest = this.getQuest(questId);
    if (!quest) return;

    quest.progress = progress;
    this.story.actProgress += progress;

    // Check for act completion
    if (this.story.actProgress >= 100) {
        this.completeAct(this.story.currentAct);
    }

    // Trigger story events
    this.checkStoryTriggers();

    // Update world state
    this.updateWorldState();

    // Save story progress
    this.saveStoryProgress();
}

// Check for story triggers
checkStoryTriggers() {
    this.storyEvents.forEach((event, eventId) => {
        if (event.condition(this.story)) {
            this.triggerStoryEvent(eventId);
        }
    });
}

// Update world based on story
updateWorldState() {
    // Example: Update corruption level affects map visuals
    const corruption = this.story.worldState.corruptionLevel;

    if (corruption > 50) {
        // Change map tiles to corrupted versions
        this.map.tiles = this.map.tiles.map(tile => {
            if (tile.type === 'grass' && Math.random() < corruption / 100) {
                return {
                    ...tile,
                    type: 'corrupted_grass',
                    color: '#4a3a2a',
                    encounter: 'corrupted'
                };
            }
            return tile;
        });
    }

    // Update NPC dialogues based on world state
    this.updateNPCDialogues();
}

// Register story event listeners
registerStoryEvents() {
    // Example: Corruption discovery event
    this.storyEvents.set('corruption_discovery', {
        condition: (story) => {
            return story.worldState.corruptionLevel >= 20 &&
                   !story.storyFlags.corruptionDiscovered;
        },
        trigger: () => {
            this.storyFlags.corruptionDiscovered = true;
            this.showCutscene('corruption_revealed');
            this.addQuest('quest_investigate_corruption');
        }
    });

    // Example: Rival transformation event
    this.storyEvents.set('rival_corrupted', {
        condition: (story) => {
            return story.currentAct >= 2 &&
                   story.majorChoices.get('trust_rival') === 'yes';
        },
        trigger: () => {
            this.showCutscene('rival_betrayal');
            this.addMemory({
                type: 'betrayal',
                npc: 'rival',
                description: 'Your rival was corrupted by the shadow',
                emotional: 'high',
                impact: 'major'
            });
        }
    });
}
```

### 1.2 Cutscene System

```javascript
// Add to GameEngine
showCutscene(cutsceneId) {
    const cutscene = this.cartridge.cutscenes[cutsceneId];
    if (!cutscene) return;

    this.setState('cutscene');
    this.currentCutscene = {
        id: cutsceneId,
        frames: cutscene.frames,
        currentFrame: 0,
        choices: cutscene.choices || null
    };

    this.playCutsceneFrame(0);
}

playCutsceneFrame(frameIndex) {
    const frame = this.currentCutscene.frames[frameIndex];

    // Display text
    this.showTextBox(frame.text, () => {
        // After text completes
        if (frame.visual) {
            this.renderCutsceneVisual(frame.visual);
        }

        // Auto-advance or wait for input
        if (frame.autoAdvance) {
            setTimeout(() => {
                this.nextCutsceneFrame();
            }, frame.delay || 2000);
        }
    });

    // Play audio if specified
    if (frame.music) {
        this.audio.playMusic(frame.music);
    }

    // Announce to screen readers
    this.announce(`Cutscene: ${frame.text.join(' ')}`);
}

nextCutsceneFrame() {
    this.currentCutscene.currentFrame++;

    if (this.currentCutscene.currentFrame >= this.currentCutscene.frames.length) {
        // Cutscene complete
        if (this.currentCutscene.choices) {
            this.showChoiceMenu(this.currentCutscene.choices);
        } else {
            this.endCutscene();
        }
    } else {
        this.playCutsceneFrame(this.currentCutscene.currentFrame);
    }
}

renderCutsceneVisual(visual) {
    // Simple visual representation using canvas
    switch(visual.type) {
        case 'character':
            this.drawCharacter(visual.character, visual.position, visual.emotion);
            break;
        case 'background':
            this.drawBackground(visual.background);
            break;
        case 'effect':
            this.drawEffect(visual.effect);
            break;
    }
}

drawCharacter(characterId, position, emotion) {
    // Draw character sprite with emotion
    const char = this.cartridge.characters[characterId];
    const sprite = char.sprites[emotion] || char.sprites.neutral;

    const x = position === 'left' ? 40 : 120;
    const y = 80;

    // Simple representation - expand with actual sprites
    this.ctx.fillStyle = char.color;
    this.ctx.fillRect(x, y, 30, 50);

    // Name label
    this.ctx.fillStyle = '#0f380f';
    this.ctx.font = '8px monospace';
    this.ctx.textAlign = 'center';
    this.ctx.fillText(char.name, x + 15, y + 60);
}
```

---

## 2. QUEST SYSTEM IMPLEMENTATION

### 2.1 Quest Manager

```javascript
// Add to GameEngine
initQuestSystem() {
    this.quests = {
        active: [],
        completed: [],
        available: []
    };

    this.questObjectives = new Map();
}

addQuest(questId) {
    const quest = this.cartridge.quests[questId];
    if (!quest) return;

    // Check prerequisites
    if (quest.prerequisite && !this.hasCompletedQuests(quest.prerequisite)) {
        return;
    }

    // Initialize quest state
    const activeQuest = {
        ...quest,
        started: Date.now(),
        objectives: quest.objectives.map(obj => ({
            ...obj,
            completed: false,
            current: 0
        }))
    };

    this.quests.active.push(activeQuest);

    // Show quest start dialogue
    if (quest.dialogue && quest.dialogue.start) {
        this.showTextBox(quest.dialogue.start);
    }

    // Announce to player
    this.announce(`New quest: ${quest.name}`);

    // Add to journal
    this.addJournalEntry({
        type: 'quest_start',
        quest: quest.name,
        timestamp: Date.now()
    });
}

updateQuestObjective(questId, objectiveIndex, progress) {
    const quest = this.quests.active.find(q => q.id === questId);
    if (!quest) return;

    const objective = quest.objectives[objectiveIndex];
    objective.current = Math.min(objective.current + progress, objective.count || 1);

    // Check if objective complete
    if (objective.current >= (objective.count || 1)) {
        objective.completed = true;
        this.announce(`Objective complete: ${objective.description}`);

        // Show progress dialogue if exists
        if (quest.dialogue.progress && quest.dialogue.progress[objective.type]) {
            this.showTextBox(quest.dialogue.progress[objective.type]);
        }
    }

    // Check if all objectives complete
    if (quest.objectives.every(obj => obj.completed)) {
        this.completeQuest(questId);
    }

    // Update UI
    this.updateQuestUI();
}

completeQuest(questId) {
    const questIndex = this.quests.active.findIndex(q => q.id === questId);
    if (questIndex === -1) return;

    const quest = this.quests.active[questIndex];

    // Remove from active
    this.quests.active.splice(questIndex, 1);

    // Add to completed
    quest.completedAt = Date.now();
    this.quests.completed.push(quest);

    // Show completion dialogue
    if (quest.dialogue && quest.dialogue.complete) {
        this.showTextBox(quest.dialogue.complete, () => {
            this.giveQuestRewards(quest);
        });
    } else {
        this.giveQuestRewards(quest);
    }

    // Progress story
    if (quest.type === 'main_story') {
        this.progressStory(questId, quest.rewards.storyProgress || 10);
    }

    // Add journal entry
    this.addJournalEntry({
        type: 'quest_complete',
        quest: quest.name,
        timestamp: Date.now()
    });

    // Unlock next quest if specified
    if (quest.nextQuest) {
        this.addQuest(quest.nextQuest);
    }
}

giveQuestRewards(quest) {
    const rewards = quest.rewards;

    // Experience
    if (rewards.experience) {
        this.player.exp += rewards.experience;
        this.announce(`Gained ${rewards.experience} experience`);
    }

    // Money
    if (rewards.money) {
        this.player.money += rewards.money;
        this.announce(`Received ${rewards.money} gold`);
    }

    // Items
    if (rewards.items) {
        rewards.items.forEach(itemStr => {
            const [itemId, count] = itemStr.split(':');
            const amount = parseInt(count) || 1;
            this.giveItem(itemId, amount);
        });
    }

    // Unlocks
    if (rewards.unlocks) {
        rewards.unlocks.forEach(unlock => {
            this.unlock(unlock);
        });
    }

    // Show rewards screen
    this.showRewardsScreen(rewards);
}

// Quest tracking helper
trackQuestProgress(eventType, data) {
    // Automatically track quest progress based on game events
    this.quests.active.forEach(quest => {
        quest.objectives.forEach((obj, index) => {
            if (obj.type === eventType && !obj.completed) {
                switch(eventType) {
                    case 'battle':
                        if (obj.target === data.enemyId) {
                            this.updateQuestObjective(quest.id, index, 1);
                        }
                        break;
                    case 'collect':
                        if (obj.target === data.itemId) {
                            this.updateQuestObjective(quest.id, index, data.amount);
                        }
                        break;
                    case 'explore':
                        if (obj.target === data.locationId) {
                            this.updateQuestObjective(quest.id, index, 1);
                        }
                        break;
                    case 'dialogue':
                        if (obj.target === data.npcId) {
                            this.updateQuestObjective(quest.id, index, 1);
                        }
                        break;
                }
            }
        });
    });
}
```

### 2.2 Quest UI

```javascript
// Add to HTML
<div class="quest-tracker" id="questTracker" style="display: none;">
    <div class="quest-header">Active Quests</div>
    <div id="questList"></div>
</div>

// CSS for quest tracker (add to existing styles)
.quest-tracker {
    position: absolute;
    top: 30px;
    left: 10px;
    background: rgba(15, 56, 15, 0.9);
    border: 2px solid #9bbc0f;
    padding: 8px;
    max-width: 200px;
    font-size: 10px;
    color: #9bbc0f;
    font-family: monospace;
}

.quest-header {
    font-weight: bold;
    margin-bottom: 5px;
    border-bottom: 1px solid #9bbc0f;
    padding-bottom: 3px;
}

.quest-item {
    margin: 5px 0;
    padding: 3px;
}

.quest-main {
    color: #ff6b6b;
}

.quest-side {
    color: #4ecdc4;
}

.objective {
    font-size: 9px;
    margin-left: 5px;
}

.objective-complete {
    text-decoration: line-through;
    opacity: 0.6;
}

// JavaScript for quest UI
updateQuestUI() {
    const questList = document.getElementById('questList');
    if (!questList) return;

    questList.innerHTML = '';

    this.quests.active.forEach(quest => {
        const questDiv = document.createElement('div');
        questDiv.className = `quest-item quest-${quest.type === 'main_story' ? 'main' : 'side'}`;

        const questTitle = document.createElement('div');
        questTitle.className = 'quest-title';
        questTitle.textContent = quest.name;
        questDiv.appendChild(questTitle);

        quest.objectives.forEach(obj => {
            const objDiv = document.createElement('div');
            objDiv.className = `objective ${obj.completed ? 'objective-complete' : ''}`;

            if (obj.count && obj.count > 1) {
                objDiv.textContent = `${obj.description} (${obj.current}/${obj.count})`;
            } else {
                objDiv.textContent = obj.completed ? '✓ ' + obj.description : '○ ' + obj.description;
            }

            questDiv.appendChild(objDiv);
        });

        questList.appendChild(questDiv);
    });

    // Show/hide tracker
    const tracker = document.getElementById('questTracker');
    if (this.quests.active.length > 0) {
        tracker.style.display = 'block';
    } else {
        tracker.style.display = 'none';
    }
}
```

---

## 3. DIALOGUE SYSTEM

### 3.1 Dialogue Manager

```javascript
// Add to GameEngine
initDialogueSystem() {
    this.dialogue = {
        current: null,
        history: [],
        choices: []
    };
}

startDialogue(npcId, dialogueKey = 'greeting') {
    const npc = this.cartridge.npcs[npcId];
    if (!npc || !npc.dialogues) return;

    const dialogue = this.getAppropriateDialogue(npc, dialogueKey);
    if (!dialogue) return;

    this.setState('dialogue');
    this.dialogue.current = {
        npcId,
        dialogue,
        index: 0,
        npcName: npc.name
    };

    this.showNextDialogueLine();
}

getAppropriateDialogue(npc, key) {
    // Get dialogue based on story state, relationships, etc.
    const dialogues = npc.dialogues;

    // Check for special conditions
    if (this.story.worldState.corruptionLevel > 50 && dialogues.corrupted) {
        return dialogues.corrupted;
    }

    // Check bond level
    const bond = this.story.npcRelationships.get(npc.id) || 0;
    if (bond >= 80 && dialogues.highBond) {
        return dialogues.highBond;
    }

    // Check story flags
    for (const [flag, value] of Object.entries(this.story.storyFlags)) {
        if (value && dialogues[flag]) {
            return dialogues[flag];
        }
    }

    // Default to requested key
    return dialogues[key] || dialogues.greeting;
}

showNextDialogueLine() {
    const currentDialogue = this.dialogue.current;
    if (!currentDialogue) return;

    const line = currentDialogue.dialogue[currentDialogue.index];

    if (typeof line === 'string') {
        // Simple text line
        this.showTextBox([line], () => {
            currentDialogue.index++;

            if (currentDialogue.index < currentDialogue.dialogue.length) {
                this.showNextDialogueLine();
            } else {
                this.endDialogue();
            }
        });
    } else if (line.choice) {
        // Choice point
        this.showDialogueChoice(line);
    } else if (line.action) {
        // Trigger action
        this.executeDialogueAction(line.action);
        currentDialogue.index++;
        this.showNextDialogueLine();
    }
}

showDialogueChoice(choiceData) {
    const choices = choiceData.options;

    // Create choice menu
    const menu = document.getElementById('dialogueChoiceMenu') || this.createDialogueChoiceMenu();
    menu.innerHTML = '';
    menu.className = 'menu active dialogue-choice-menu';

    choices.forEach((choice, index) => {
        const option = document.createElement('div');
        option.className = `menu-option ${index === 0 ? 'selected' : ''}`;
        option.textContent = choice.text;
        option.setAttribute('data-choice-index', index);
        option.setAttribute('tabindex', index === 0 ? '0' : '-1');
        option.setAttribute('role', 'menuitem');

        option.addEventListener('click', () => {
            this.selectDialogueChoice(choice);
        });

        menu.appendChild(option);
    });

    // Set up keyboard navigation
    this.setupDialogueChoiceNav(menu);

    // Announce choices to screen reader
    this.announce(`Choose your response: ${choices.map(c => c.text).join(', ')}`);
}

selectDialogueChoice(choice) {
    // Record choice
    this.recordChoice(choice);

    // Apply bond changes
    if (choice.bond) {
        this.modifyNPCRelationship(this.dialogue.current.npcId, choice.bond);
    }

    // Apply consequences
    if (choice.consequence) {
        this.applyChoiceConsequence(choice.consequence);
    }

    // Unlock content
    if (choice.unlocks) {
        this.unlock(choice.unlocks);
    }

    // Continue to response dialogue
    if (choice.response) {
        const npc = this.cartridge.npcs[this.dialogue.current.npcId];
        const response = npc.dialogues[choice.response];

        if (response) {
            this.dialogue.current.dialogue = response;
            this.dialogue.current.index = 0;
            this.showNextDialogueLine();
        }
    } else {
        this.endDialogue();
    }

    // Hide choice menu
    const menu = document.getElementById('dialogueChoiceMenu');
    if (menu) menu.classList.remove('active');
}

recordChoice(choice) {
    this.dialogue.history.push({
        npcId: this.dialogue.current.npcId,
        choice: choice.text,
        timestamp: Date.now()
    });

    // Add to memory system
    if (choice.emotional === 'HIGH') {
        this.addMemory({
            type: 'choice',
            npc: this.dialogue.current.npcId,
            choice: choice.text,
            impact: 'major'
        });
    }
}

endDialogue() {
    this.dialogue.current = null;
    this.setState('overworld');

    // Track quest progress if dialogue was quest objective
    this.trackQuestProgress('dialogue', {
        npcId: this.dialogue.current?.npcId
    });
}
```

### 3.2 NPC Relationship System

```javascript
// Add to GameEngine
modifyNPCRelationship(npcId, amount) {
    const current = this.story.npcRelationships.get(npcId) || 0;
    const newValue = Math.max(0, Math.min(100, current + amount));

    this.story.npcRelationships.set(npcId, newValue);

    // Check for bond level ups
    const oldLevel = this.getBondLevel(current);
    const newLevel = this.getBondLevel(newValue);

    if (newLevel > oldLevel) {
        this.onBondLevelUp(npcId, newLevel);
    }

    // Save relationship change
    this.saveStoryProgress();
}

getBondLevel(bondValue) {
    if (bondValue >= 80) return 5;
    if (bondValue >= 60) return 4;
    if (bondValue >= 40) return 3;
    if (bondValue >= 20) return 2;
    return 1;
}

onBondLevelUp(npcId, level) {
    const npc = this.cartridge.npcs[npcId];

    this.announce(`Your bond with ${npc.name} has grown!`);

    // Show bond level up cutscene
    if (npc.bondCutscenes && npc.bondCutscenes[level]) {
        this.showCutscene(npc.bondCutscenes[level]);
    }

    // Unlock bond rewards
    if (npc.bondRewards && npc.bondRewards[level]) {
        this.giveQuestRewards(npc.bondRewards[level]);
    }

    // Unlock new quests
    if (npc.bondQuests && npc.bondQuests[level]) {
        this.addQuest(npc.bondQuests[level]);
    }
}
```

---

## 4. BOSS BATTLE FRAMEWORK

### 4.1 Boss Battle System

```javascript
// Extend existing battle system
initBossBattle(bossId) {
    const boss = this.cartridge.bosses[bossId];
    if (!boss) return;

    this.battle = {
        type: 'boss',
        boss: boss,
        currentPhase: 1,
        phaseTransitioned: false,
        playerCreature: this.player.creatures[0],
        enemyCreature: this.createBossCreature(boss, 1),
        turn: 'player',
        bossAI: this.createBossAI(boss)
    };

    // Show boss intro
    if (boss.dialogue && boss.dialogue.intro) {
        this.showTextBox(boss.dialogue.intro, () => {
            this.setState('battle');
            this.startBattle();
        });
    } else {
        this.setState('battle');
        this.startBattle();
    }
}

createBossCreature(boss, phase) {
    const phaseData = boss.mechanics[`phase${phase}`];

    return {
        name: boss.name,
        level: boss.level,
        hp: phaseData.hp || boss.baseHp,
        maxHp: phaseData.maxHp || boss.baseHp,
        attack: boss.baseAttack,
        defense: boss.baseDefense,
        speed: boss.baseSpeed,
        moves: phaseData.abilities.map(abilityName =>
            this.cartridge.moves[abilityName] || { name: abilityName, power: 50 }
        ),
        phase: phase,
        mechanics: phaseData
    };
}

createBossAI(boss) {
    return {
        strategy: boss.mechanics.phase1.pattern || 'aggressive',
        moveHistory: [],
        turnCount: 0,

        selectMove: function(playerCreature, bossCreature) {
            this.turnCount++;

            // Check for special mechanics
            if (bossCreature.mechanics.healTrigger) {
                const hpPercent = (bossCreature.hp / bossCreature.maxHp) * 100;
                if (hpPercent <= bossCreature.mechanics.healTrigger.at &&
                    !bossCreature.mechanics.healTrigger.triggered) {
                    bossCreature.mechanics.healTrigger.triggered = true;
                    return this.executeSpecialMechanic(bossCreature.mechanics.healTrigger);
                }
            }

            // Ultimate ability check
            if (bossCreature.mechanics.ultimateAbility) {
                const ultimate = bossCreature.mechanics.ultimateAbility;
                if (ultimate.counterTime && this.turnCount % 5 === 0) {
                    return { special: 'ultimate', ability: ultimate };
                }
            }

            // Select move based on strategy
            switch(this.strategy) {
                case 'aggressive':
                    return this.selectAggressiveMove(bossCreature, playerCreature);
                case 'defensive':
                    return this.selectDefensiveMove(bossCreature, playerCreature);
                case 'intelligent':
                    return this.selectIntelligentMove(bossCreature, playerCreature);
                default:
                    return this.selectRandomMove(bossCreature);
            }
        },

        selectAggressiveMove: function(boss, player) {
            // Always use highest power move
            return boss.moves.reduce((strongest, move) =>
                move.power > strongest.power ? move : strongest
            );
        },

        selectIntelligentMove: function(boss, player) {
            // Check type advantages, player HP, etc.
            const lowHpMoves = boss.moves.filter(m =>
                m.effect && m.effect.includes('execute')
            );

            if (player.hp < player.maxHp * 0.3 && lowHpMoves.length > 0) {
                return lowHpMoves[0];
            }

            // Otherwise use type advantage
            return this.selectAggressiveMove(boss, player);
        }
    };
}

// Boss battle turn processing
processBossTurn() {
    const boss = this.battle.enemyCreature;
    const ai = this.battle.bossAI;

    const selectedMove = ai.selectMove(this.battle.playerCreature, boss);

    if (selectedMove.special === 'ultimate') {
        this.executeUltimateAbility(selectedMove.ability);
    } else {
        this.executeMove(boss, this.battle.playerCreature, selectedMove);
    }

    // Check for phase transition
    this.checkBossPhaseTransition();
}

checkBossPhaseTransition() {
    const boss = this.battle.boss;
    const creature = this.battle.enemyCreature;
    const currentPhase = creature.phase;
    const nextPhase = currentPhase + 1;

    if (!boss.mechanics[`phase${nextPhase}`]) return;

    const nextPhaseData = boss.mechanics[`phase${nextPhase}`];
    const hpPercent = (creature.hp / creature.maxHp) * 100;

    // Check if HP threshold reached
    const threshold = parseInt(nextPhaseData.hp);
    if (hpPercent <= threshold && !this.battle.phaseTransitioned) {
        this.transitionBossPhase(nextPhase);
    }
}

transitionBossPhase(newPhase) {
    this.battle.phaseTransitioned = true;

    const boss = this.battle.boss;
    const phaseData = boss.mechanics[`phase${newPhase}`];

    // Show phase transition
    if (phaseData.transformation) {
        this.showTextBox([phaseData.transformation], () => {
            this.applyPhaseTransition(newPhase, phaseData);
        });
    } else {
        this.applyPhaseTransition(newPhase, phaseData);
    }

    // Show phase dialogue
    if (boss.dialogue && boss.dialogue[`phase${newPhase}`]) {
        setTimeout(() => {
            this.showTextBox(boss.dialogue[`phase${newPhase}`]);
        }, 1000);
    }
}

applyPhaseTransition(newPhase, phaseData) {
    const creature = this.battle.enemyCreature;

    // Update phase
    creature.phase = newPhase;
    creature.mechanics = phaseData;

    // Add new abilities
    if (phaseData.newAbilities) {
        phaseData.newAbilities.forEach(abilityName => {
            const ability = this.cartridge.moves[abilityName];
            if (ability && !creature.moves.find(m => m.name === ability.name)) {
                creature.moves.push(ability);
            }
        });
    }

    // Update AI strategy
    if (phaseData.pattern) {
        this.battle.bossAI.strategy = phaseData.pattern;
    }

    // Visual transformation
    if (phaseData.transformation) {
        this.animateBossTransformation();
    }

    this.battle.phaseTransitioned = false;
}

animateBossTransformation() {
    // Visual effect for boss transformation
    let flashes = 0;
    const flashInterval = setInterval(() => {
        this.ctx.fillStyle = flashes % 2 === 0 ? '#ffffff' : '#000000';
        this.ctx.globalAlpha = 0.5;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.globalAlpha = 1;

        flashes++;
        if (flashes >= 6) {
            clearInterval(flashInterval);
            this.render();
        }
    }, 100);
}

executeUltimateAbility(ultimate) {
    // Show warning
    this.showTextBox([ultimate.warning], () => {
        // Give player time to counter
        this.battle.ultimateCounter = {
            active: true,
            turnsRemaining: ultimate.counterTime,
            ability: ultimate,
            onSuccess: () => {
                this.announce('You countered the ultimate attack!');
            },
            onFailure: () => {
                this.applyUltimateEffect(ultimate.failure);
                if (ultimate.failureDialogue) {
                    this.showTextBox([ultimate.failureDialogue]);
                }
            }
        };
    });
}
```

### 4.2 Boss Rewards & Consequences

```javascript
// Add to battle end handler
endBossBattle(result) {
    const boss = this.battle.boss;

    if (result === 'victory') {
        // Check for special victory conditions
        const usedPurification = this.battle.itemsUsed &&
            this.battle.itemsUsed.includes('purification_token');

        const rewards = usedPurification ?
            boss.rewards.purified :
            boss.rewards.standard;

        // Show victory dialogue
        const dialogueKey = usedPurification ? 'phase3_purify' : 'phase3_destroy';
        if (boss.dialogue[dialogueKey]) {
            this.showTextBox(boss.dialogue[dialogueKey], () => {
                this.giveBossRewards(rewards);
            });
        } else {
            this.giveBossRewards(rewards);
        }

        // Apply story impact
        if (rewards.storyImpact) {
            this.applyStoryImpact(rewards.storyImpact);
        }
    } else {
        // Defeat handling for bosses
        if (boss.consequences && boss.consequences.defeat) {
            this.applyBossDefeatConsequences(boss.consequences.defeat);
        }
    }
}

giveBossRewards(rewards) {
    // Standard reward handling
    this.giveQuestRewards(rewards);

    // Special rewards
    if (rewards.special) {
        this.handleSpecialReward(rewards.special);
    }
}

applyStoryImpact(impact) {
    // Modify world state based on boss outcome
    if (impact.includes('saved')) {
        this.story.worldState.corruptionLevel -= 10;
        this.addMemory({
            type: 'victory',
            description: 'You saved the corrupted creature',
            impact: 'major',
            emotional: 'high'
        });
    } else if (impact.includes('mourns')) {
        this.story.worldState.corruptionLevel += 5;
        this.addMemory({
            type: 'loss',
            description: 'The creature could not be saved',
            impact: 'major',
            emotional: 'high'
        });
    }
}
```

---

## 5. TEAM BUILDER INTEGRATION

### 5.1 Story Team Builder

```javascript
// Add to GameEngine
initStoryTeamBuilder() {
    this.teamBuilder = {
        slots: 6,
        activeTeam: [],
        reserve: [],
        roles: [
            {
                name: "Starter's Legacy",
                slot: 0,
                locked: true,
                requirement: null,
                bonus: { statsMultiplier: 1.2 }
            },
            {
                name: "The Protector",
                slot: 1,
                requirement: 'alara_bond_3',
                bonus: { damageReduction: 0.15 }
            },
            // ... more roles
        ],
        synergies: [],
        activeSynergies: []
    };

    this.calculateTeamSynergies();
}

calculateTeamSynergies() {
    const team = this.teamBuilder.activeTeam;
    const synergies = this.cartridge.teamSynergies || [];

    this.teamBuilder.activeSynergies = [];

    synergies.forEach(synergy => {
        if (this.checkSynergyRequirement(synergy, team)) {
            this.teamBuilder.activeSynergies.push(synergy);
            this.applySynergyBonus(synergy);
        }
    });
}

checkSynergyRequirement(synergy, team) {
    switch(synergy.requirement.type) {
        case 'all_story':
            return team.every(creature => creature.obtainedFrom === 'story');

        case 'faction':
            return team.every(creature =>
                creature.faction === synergy.requirement.faction
            );

        case 'type_balance':
            const types = new Set(team.map(c => c.type[0]));
            return types.size >= 5;

        case 'legendary_count':
            const legendaryCount = team.filter(c => c.legendary).length;
            return legendaryCount >= synergy.requirement.count;

        default:
            return false;
    }
}

applySynergyBonus(synergy) {
    this.teamBuilder.activeTeam.forEach(creature => {
        switch(synergy.effect.type) {
            case 'hp_boost':
                creature.maxHp = Math.floor(creature.maxHp * (1 + synergy.effect.value));
                creature.hp = creature.maxHp;
                break;

            case 'attack_boost':
                creature.attack = Math.floor(creature.attack * (1 + synergy.effect.value));
                break;

            case 'type_advantage':
                creature.typeAdvantageMultiplier = (creature.typeAdvantageMultiplier || 1) * synergy.effect.value;
                break;
        }
    });
}

// Story-based team slot unlocking
unlockTeamSlot(slotIndex) {
    const slot = this.teamBuilder.roles[slotIndex];

    if (slot.requirement && !this.hasMetRequirement(slot.requirement)) {
        return false;
    }

    slot.unlocked = true;

    this.announce(`New team role unlocked: ${slot.name}`);
    this.showTextBox([
        `Team Role Unlocked!`,
        slot.name,
        slot.description,
        `Bonus: ${this.describeBo nus(slot.bonus)}`
    ]);

    return true;
}
```

### 5.2 Story Evolution System

```javascript
// Add to evolution check
checkStoryEvolution(creature) {
    const species = this.cartridge.creatures[creature.id];

    if (!species.storyEvolution) {
        return this.checkNormalEvolution(creature);
    }

    const storyEvo = species.storyEvolution;

    // Check if story evolution conditions met
    if (creature.level >= storyEvo.level) {
        const triggerMet = this.checkEvolutionTrigger(storyEvo.trigger);

        if (triggerMet) {
            this.triggerStoryEvolution(creature, storyEvo);
            return true;
        }
    }

    // Fall back to normal evolution
    return this.checkNormalEvolution(creature);
}

checkEvolutionTrigger(trigger) {
    // Example triggers
    if (trigger.includes('quest:')) {
        const questId = trigger.split(':')[1];
        return this.quests.completed.some(q => q.id === questId);
    }

    if (trigger.includes('bond:')) {
        const [_, npcId, level] = trigger.split(':');
        const bondLevel = this.story.npcRelationships.get(npcId) || 0;
        return this.getBondLevel(bondLevel) >= parseInt(level);
    }

    return false;
}

triggerStoryEvolution(creature, storyEvo) {
    // Show special evolution cutscene
    this.showCutscene('evolution_' + storyEvo.evolveTo);

    // Evolve creature
    const evolvedCreature = this.evolveCreature(creature, storyEvo.evolveTo);

    // Apply story bonuses
    if (storyEvo.bonuses) {
        storyEvo.bonuses.forEach(bonus => {
            this.applyEvolutionBonus(evolvedCreature, bonus);
        });
    }

    // Update team
    const teamIndex = this.teamBuilder.activeTeam.findIndex(c => c.id === creature.id);
    if (teamIndex !== -1) {
        this.teamBuilder.activeTeam[teamIndex] = evolvedCreature;
    }

    // Add memory
    this.addMemory({
        type: 'evolution',
        creature: evolvedCreature.name,
        description: storyEvo.description,
        special: true
    });
}
```

---

## 6. MEMORY & CONSEQUENCE SYSTEM

### 6.1 Memory System

```javascript
// Add to GameEngine
addMemory(memory) {
    memory.timestamp = Date.now();
    memory.act = this.story.currentAct;

    this.story.memories.push(memory);

    // Add to journal if significant
    if (memory.impact === 'major') {
        this.addJournalEntry({
            type: 'memory',
            title: memory.type.toUpperCase(),
            content: memory.description,
            emotional: memory.emotional
        });
    }

    // Some memories trigger events later
    if (memory.triggerLater) {
        this.scheduleMemoryCallback(memory);
    }
}

getRelevantMemories(context) {
    // Get memories relevant to current context
    return this.story.memories.filter(memory => {
        if (context.npc && memory.npc === context.npc) return true;
        if (context.location && memory.location === context.location) return true;
        if (context.type && memory.type === context.type) return true;
        return false;
    });
}

// Memories affect NPC dialogues
getMemoryInfluencedDialogue(npcId) {
    const relevantMemories = this.getRelevantMemories({ npc: npcId });

    if (relevantMemories.length === 0) {
        return null;
    }

    // Check for specific memory types
    const betrayal = relevantMemories.find(m => m.type === 'betrayal');
    if (betrayal) {
        return this.cartridge.npcs[npcId].dialogues.after_betrayal;
    }

    const heroicAct = relevantMemories.find(m => m.type === 'saved');
    if (heroicAct) {
        return this.cartridge.npcs[npcId].dialogues.grateful;
    }

    return null;
}
```

### 6.2 Consequence System

```javascript
applyChoiceConsequence(consequence) {
    switch(consequence.type) {
        case 'npc_unavailable':
            this.story.worldState.unavailableNPCs =
                this.story.worldState.unavailableNPCs || [];
            this.story.worldState.unavailableNPCs.push(consequence.npcId);

            this.addMemory({
                type: 'consequence',
                description: `${consequence.npcId} is no longer available`,
                impact: 'major'
            });
            break;

        case 'quest_failed':
            const quest = this.quests.active.find(q => q.id === consequence.questId);
            if (quest) {
                quest.failed = true;
                this.quests.active = this.quests.active.filter(q => q.id !== consequence.questId);
            }
            break;

        case 'world_change':
            this.story.worldState.corruptionLevel += consequence.corruptionChange || 0;
            this.updateWorldState();
            break;

        case 'faction_change':
            this.story.factionRep[consequence.faction] += consequence.amount;
            this.checkFactionThresholds();
            break;

        case 'permanent_loss':
            // Remove creature permanently (hardcore mode)
            const creatureIndex = this.player.creatures.findIndex(
                c => c.id === consequence.creatureId
            );
            if (creatureIndex !== -1) {
                const creature = this.player.creatures[creatureIndex];
                this.player.creatures.splice(creatureIndex, 1);

                this.addMemory({
                    type: 'loss',
                    creature: creature.name,
                    description: `${creature.name} was lost forever`,
                    emotional: 'CRITICAL',
                    impact: 'major'
                });
            }
            break;
    }
}

// Consequences can be reversed through redemption quests
checkRedemptionAvailable() {
    const negativeMemories = this.story.memories.filter(m =>
        m.type === 'consequence' && m.redemptionPossible
    );

    negativeMemories.forEach(memory => {
        if (!memory.redemptionOffered && this.story.currentAct >= 3) {
            // Offer redemption quest
            this.addQuest(`redemption_${memory.type}_${memory.id}`);
            memory.redemptionOffered = true;
        }
    });
}
```

---

## 7. INTEGRATION WITH EXISTING CODE

### 7.1 Modifications to Existing Battle System

```javascript
// Modify existing startBattle to check for boss battles
startBattle(enemyData) {
    // Check if this is a boss battle
    if (enemyData.isBoss) {
        return this.initBossBattle(enemyData.bossId);
    }

    // ... existing battle code ...

    // Track quest progress
    this.trackQuestProgress('battle', {
        enemyId: enemyData.id,
        enemyType: enemyData.type
    });
}

// Modify battle end to add memories
endBattle(result) {
    // ... existing code ...

    if (result === 'victory' && this.battle.enemyCreature.corrupted) {
        this.addMemory({
            type: 'battle',
            description: `Defeated corrupted ${this.battle.enemyCreature.name}`,
            impact: 'minor'
        });
    }
}
```

### 7.2 Modifications to Save System

```javascript
// Extend existing exportSave to include story data
exportSave() {
    const saveData = {
        version: this.cartridge.version,
        timestamp: Date.now(),
        player: this.player,
        map: {
            current: this.map.name,
            position: { x: this.player.x, y: this.player.y }
        },

        // ADD STORY DATA
        story: {
            act: this.story.currentAct,
            progress: this.story.actProgress,
            choices: Array.from(this.story.majorChoices),
            flags: this.story.storyFlags,
            worldState: this.story.worldState,
            relationships: Array.from(this.story.npcRelationships),
            faction: this.story.factionRep,
            memories: this.story.memories
        },

        quests: {
            active: this.quests.active,
            completed: this.quests.completed
        },

        journal: this.journal,

        // Existing data
        statistics: this.statistics,
        achievements: this.achievements
    };

    const json = JSON.stringify(saveData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `wowmon-story-save-${Date.now()}.json`;
    link.click();

    this.announce('Game saved successfully');
}

// Extend import to load story data
handleSaveLoad(event) {
    // ... existing code ...

    if (saveData.story) {
        this.story = saveData.story;
        this.story.majorChoices = new Map(saveData.story.choices);
        this.story.npcRelationships = new Map(saveData.story.relationships);

        // Restore world state
        this.updateWorldState();
    }

    if (saveData.quests) {
        this.quests = saveData.quests;
        this.updateQuestUI();
    }
}
```

### 7.3 New Keyboard Shortcuts

```javascript
// Add to existing keydown handler
document.addEventListener('keydown', (e) => {
    // ... existing controls ...

    // J key - Open Journal
    if (e.key.toLowerCase() === 'j') {
        e.preventDefault();
        this.toggleJournal();
    }

    // Q key - Open Quest Log
    if (e.key.toLowerCase() === 'q') {
        e.preventDefault();
        this.toggleQuestLog();
    }

    // R key - View Relationships
    if (e.key.toLowerCase() === 'r') {
        e.preventDefault();
        this.showRelationshipScreen();
    }

    // M key - View Memories
    if (e.key.toLowerCase() === 'm') {
        e.preventDefault();
        this.showMemoryScreen();
    }
});
```

---

## 8. DATA STRUCTURE ADDITIONS TO CARTRIDGE

### 8.1 Add to autoLoadWoWmon() cartridge data

```javascript
// Add to existing cartridge object in autoLoadWoWmon()
"quests": {
    "quest_shadow_investigation": {
        // ... as shown in section 2
    },
    // ... more quests
},

"bosses": {
    "boss_corrupted_treant": {
        // ... as shown in section 4
    },
    // ... more bosses
},

"cutscenes": {
    "corruption_revealed": {
        frames: [
            {
                text: ["A dark shadow passes over the forest..."],
                visual: { type: "background", background: "dark_forest" },
                music: "ominous"
            },
            // ... more frames
        ]
    }
},

"npcs": {
    // Extend existing NPCs with dialogue trees
    "captain_alara": {
        id: "captain_alara",
        name: "Captain Alara",
        dialogues: {
            greeting: [
                "Welcome, trainer.",
                "The corruption spreads..."
            ],
            // ... more dialogues
        },
        bondRewards: {
            3: {
                items: ["warrior_emblem"],
                creature: "trained_wolf"
            }
        }
    }
},

"teamSynergies": [
    {
        name: "Bond of Heroes",
        requirement: {
            type: "all_story"
        },
        effect: {
            type: "hp_boost",
            value: 0.1
        },
        description: "Your companions fight harder when together"
    }
],

"storyEvolutions": {
    // Add to creature definitions
}
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Core Systems
- [ ] Story state manager
- [ ] Quest system (add, update, complete)
- [ ] Dialogue system with choices
- [ ] Memory system
- [ ] Save/load story data

### Phase 2: UI Components
- [ ] Quest tracker overlay
- [ ] Journal interface
- [ ] Relationship screen
- [ ] Memory viewer
- [ ] Choice menu styling

### Phase 3: Battle Enhancements
- [ ] Boss battle framework
- [ ] Phase transitions
- [ ] Special mechanics
- [ ] Boss AI
- [ ] Consequence integration

### Phase 4: Team Builder
- [ ] Story-based slots
- [ ] Synergy calculation
- [ ] Story evolutions
- [ ] Bond system

### Phase 5: Content
- [ ] Write Act 1 quests
- [ ] Create first boss battles
- [ ] Add NPC dialogues
- [ ] Design cutscenes
- [ ] Implement consequences

### Phase 6: Polish
- [ ] Playtest story flow
- [ ] Balance boss encounters
- [ ] Accessibility for story UI
- [ ] Screen reader support
- [ ] Mobile touch optimizations

---

## CONCLUSION

This implementation guide provides the code framework to transform WoWmon into a story-driven RPG. The modular design allows gradual implementation - start with the core story engine, then add quest systems, then bosses, etc.

All systems integrate cleanly with the existing game architecture while maintaining the self-contained HTML structure. The memory and consequence systems create a living world that responds to player choices.

The focus remains on narrative, character development, and memorable single-player moments.

---

**Happy coding, and may your stories be epic!**
