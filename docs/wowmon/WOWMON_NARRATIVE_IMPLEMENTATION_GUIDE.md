# WoWMon Narrative System - Implementation Quick Guide

## Overview
This is a practical implementation guide for integrating the story system into WoWMon. Use this alongside the full narrative design document.

---

## 1. Core Data Structures

### Story State Object
```javascript
gameState.story = {
  // Progression
  currentChapter: 1,
  completedChapters: [],

  // Karma and Relationships
  karmaScore: 0, // Range: -100 to +100
  relationships: {
    rival: 50,      // 0-100
    khadgar: 0,
    jaina: 0,
    thrall: 0,
    mother: 100
  },

  // Story Flags
  flags: {
    metRival: false,
    mentorDied: false,
    learnedMotherPast: false,
    rivalCorrupted: false,
    dragonEggReceived: false,
    dragonEggHatched: false,
    motherRevealed: false,
    motherSaved: false,
    factionsUnited: false,
    eliteFourDefeated: false
  },

  // Major Choices
  choices: {
    faction: null, // 'alliance' or 'horde'
    starter: null, // creature ID
    farmerChoice: null, // 'help' or 'ignore'
    forsakenChoice: null, // 'trust' or 'reject'
    rivalFate: null // 'saved', 'defeated', 'sacrificed'
  },

  // NPC States
  defeatedTrainers: new Set(),
  npcStates: {},

  // Side Quests
  sideQuests: {
    active: [],
    completed: []
  }
};
```

### Dialogue Data Structure
```javascript
const dialogueDatabase = {
  "khadgar_intro": {
    id: "khadgar_intro",
    speaker: "Professor Khadgar",
    text: "Welcome to the world of WoWmon! Choose your starter wisely!",
    portrait: "khadgar_happy",

    conditions: {
      chapter: 0,
      flags: [],
      notFlags: []
    },

    options: [
      {
        text: "Tell me about these creatures.",
        karma: 0,
        next: "khadgar_explanation"
      },
      {
        text: "I'm ready to choose!",
        karma: 0,
        next: "starter_selection"
      }
    ],

    onComplete: () => {
      gameState.story.flags.metKhadgar = true;
    }
  }
};
```

### Character Database
```javascript
const characters = {
  rival: {
    id: "rival",
    name: {
      alliance: "Aerin Sunstrider",
      horde: "Karg Hellscream"
    },

    dialogue: {
      chapter1: "I'll prove I'm better than you!",
      chapter7: "This power... it's everything I needed...",
      saved: "I was drowning in darkness. You pulled me out.",
      defeated: "You... you defeated me...",
      sacrifice: "Tell them... I wasn't a coward..."
    },

    team: {
      chapter1: ["kobold", "wisp"],
      chapter3: ["gnoll", "ancient_wisp", "treant"],
      chapter5: ["drake", "orc_grunt", "naga"],
      chapter7_corrupted: ["shadow_drake", "void_beast", "corrupt_naga"],
      chapter7_normal: ["dragon", "orc_warlord", "phoenix"]
    }
  }
};
```

---

## 2. Key Functions to Implement

### Story Progression
```javascript
function advanceToChapter(chapterNumber) {
  gameState.story.currentChapter = chapterNumber;
  gameState.story.completedChapters.push(chapterNumber - 1);

  // Trigger chapter start event
  triggerChapterCutscene(chapterNumber);

  // Unlock new areas
  unlockChapterAreas(chapterNumber);

  // Update NPC dialogues
  refreshNPCDialogues();

  // Save progress
  saveGame();
}

function checkChapterCompletion(chapterNumber) {
  const requirements = chapterRequirements[chapterNumber];

  // Check badges
  if (requirements.badges && gameState.badges.length < requirements.badges) {
    return false;
  }

  // Check story flags
  if (requirements.flags) {
    for (const flag of requirements.flags) {
      if (!gameState.story.flags[flag]) return false;
    }
  }

  // Check defeated trainers
  if (requirements.trainers) {
    for (const trainer of requirements.trainers) {
      if (!gameState.story.defeatedTrainers.has(trainer)) return false;
    }
  }

  return true;
}
```

### Karma System
```javascript
function adjustKarma(amount, reason) {
  gameState.story.karmaScore = Math.max(-100, Math.min(100,
    gameState.story.karmaScore + amount
  ));

  // Show notification
  showNotification(`Karma ${amount > 0 ? '+' : ''}${amount}: ${reason}`);

  // Check for karma milestones
  checkKarmaMilestones();
}

function getKarmaLevel() {
  const score = gameState.story.karmaScore;
  if (score >= 75) return 'hero';
  if (score >= 25) return 'good';
  if (score >= -25) return 'neutral';
  if (score >= -75) return 'dark';
  return 'villain';
}

// Example karma actions
function helpNPC() {
  adjustKarma(5, "Helped someone in need");
  gameState.story.relationships.helped++;
}

function ignoreNPC() {
  adjustKarma(-5, "Ignored plea for help");
}

function showMercy() {
  adjustKarma(10, "Showed mercy to defeated foe");
}

function useCorruptedWowmon() {
  adjustKarma(-3, "Used corrupted creature");
}
```

### Relationship System
```javascript
function changeRelationship(character, amount) {
  if (!gameState.story.relationships[character]) {
    gameState.story.relationships[character] = 50;
  }

  gameState.story.relationships[character] = Math.max(0, Math.min(100,
    gameState.story.relationships[character] + amount
  ));

  // Check for relationship milestones
  checkRelationshipMilestone(character);
}

function getRelationshipLevel(character) {
  const value = gameState.story.relationships[character] || 50;
  if (value >= 80) return 'devoted';
  if (value >= 60) return 'friendly';
  if (value >= 40) return 'neutral';
  if (value >= 20) return 'distant';
  return 'hostile';
}

function checkRelationshipMilestone(character) {
  const level = gameState.story.relationships[character];

  // Unlock special quests at high relationship
  if (level >= 80 && !gameState.story.sideQuests.completed.includes(`${character}_personal`)) {
    unlockSideQuest(`${character}_personal_quest`);
    showNotification(`New quest available: ${character}'s story`);
  }
}
```

### Dialogue System
```javascript
function showDialogue(dialogueId, npcName = null) {
  const dialogue = dialogueDatabase[dialogueId];

  if (!dialogue) {
    console.error(`Dialogue not found: ${dialogueId}`);
    return;
  }

  // Check conditions
  if (!checkDialogueConditions(dialogue.conditions)) {
    return;
  }

  // Show dialogue UI
  const dialogueBox = document.getElementById('dialogueBox');
  dialogueBox.classList.add('active');

  // Set speaker and text
  document.getElementById('dialogueSpeaker').textContent = npcName || dialogue.speaker;
  document.getElementById('dialogueText').textContent = dialogue.text;

  // Set portrait if available
  if (dialogue.portrait) {
    document.getElementById('dialoguePortrait').src = `assets/portraits/${dialogue.portrait}.png`;
  }

  // Show options if present
  if (dialogue.options && dialogue.options.length > 0) {
    showDialogueOptions(dialogue.options);
  } else {
    // Single option: continue
    showDialogueOptions([{
      text: "...",
      next: dialogue.next || null
    }]);
  }

  // Execute completion callback
  if (dialogue.onComplete) {
    dialogue.onComplete();
  }
}

function checkDialogueConditions(conditions) {
  if (!conditions) return true;

  // Check chapter
  if (conditions.chapter !== undefined &&
      gameState.story.currentChapter < conditions.chapter) {
    return false;
  }

  // Check required flags
  if (conditions.flags) {
    for (const flag of conditions.flags) {
      if (!gameState.story.flags[flag]) return false;
    }
  }

  // Check prohibited flags
  if (conditions.notFlags) {
    for (const flag of conditions.notFlags) {
      if (gameState.story.flags[flag]) return false;
    }
  }

  // Check karma
  if (conditions.minKarma !== undefined &&
      gameState.story.karmaScore < conditions.minKarma) {
    return false;
  }

  if (conditions.maxKarma !== undefined &&
      gameState.story.karmaScore > conditions.maxKarma) {
    return false;
  }

  return true;
}

function selectDialogueOption(optionIndex) {
  const dialogue = currentDialogue;
  const option = dialogue.options[optionIndex];

  // Apply karma
  if (option.karma) {
    adjustKarma(option.karma, option.text);
  }

  // Set flags
  if (option.setFlags) {
    option.setFlags.forEach(flag => {
      gameState.story.flags[flag] = true;
    });
  }

  // Adjust relationships
  if (option.relationship) {
    Object.entries(option.relationship).forEach(([character, amount]) => {
      changeRelationship(character, amount);
    });
  }

  // Execute callback
  if (option.onSelect) {
    option.onSelect();
  }

  // Continue to next dialogue or close
  if (option.next) {
    showDialogue(option.next);
  } else {
    closeDialogue();
  }
}
```

### Choice System (Chapter 9 - The Defining Moment)
```javascript
function showRivalChoice() {
  // This is the big choice in Chapter 9
  const choiceUI = document.getElementById('majorChoiceUI');
  choiceUI.classList.add('active');

  const choices = [
    {
      id: 'save_rival',
      title: "Save Your Rival",
      description: "Use the Emerald Essence to purify them. They'll return as your ally.",
      requirements: "Requires: Emerald Essence",
      outcome: "Path of Redemption - True Hero Ending Available",
      karma: +20,
      action: () => saveRival()
    },
    {
      id: 'defeat_rival',
      title: "Defeat Them in Combat",
      description: "Your rival has fallen too far. Take their power for yourself.",
      outcome: "Path of Power - Dark Champion Ending",
      karma: -20,
      action: () => defeatRival()
    },
    {
      id: 'accept_sacrifice',
      title: "Let Them Sacrifice Themselves",
      description: "Your rival chooses to save you from the void trap.",
      outcome: "Path of Memory - Bittersweet Ending",
      karma: +10,
      action: () => rivalSacrifice()
    }
  ];

  renderChoices(choices);
}

function saveRival() {
  // Use Emerald Essence
  removeItem('emerald_essence');

  // Set story flags
  gameState.story.flags.rivalSaved = true;
  gameState.story.choices.rivalFate = 'saved';

  // Play cutscene
  playCutscene('rival_purification');

  // Rival becomes ally
  gameState.allies.push('rival');
  changeRelationship('rival', 50);

  // Unlock double battles
  gameState.features.doubleBattles = true;

  // Achievement
  unlockAchievement('true_friend');

  adjustKarma(20, "Saved your rival from corruption");

  showNotification("Rival rejoined your party!");
}

function defeatRival() {
  // Set story flags
  gameState.story.flags.rivalDefeated = true;
  gameState.story.choices.rivalFate = 'defeated';

  // Play cutscene
  playCutscene('rival_falls_to_void');

  // Gain corrupted legendary
  addWowmonToBox(createCorruptedLegendary());

  // Relationship destroyed
  changeRelationship('rival', -100);

  // Darker tone unlocked
  gameState.story.flags.darkPath = true;

  adjustKarma(-20, "Defeated corrupted rival");

  showNotification("You obtained Shadow Legendary...");
}

function rivalSacrifice() {
  // Set story flags
  gameState.story.flags.rivalSacrificed = true;
  gameState.story.choices.rivalFate = 'sacrificed';

  // Play cutscene (emotional)
  playCutscene('rival_final_sacrifice');

  // Receive rival's signature creature and journal
  const rivalSignature = getRivalSignatureWowmon();
  rivalSignature.bond = 100;
  rivalSignature.note = "From my best friend...";
  addWowmonToParty(rivalSignature);

  addItem('rival_journal');

  // Memorial unlocked
  gameState.story.flags.rivalMemorial = true;

  adjustKarma(10, "Honored rival's sacrifice");

  showNotification("Received rival's partner and journal...");
}
```

### Cutscene System
```javascript
const cutscenes = {
  chapter1_intro: {
    id: "chapter1_intro",
    scenes: [
      {
        type: "dialogue",
        speaker: "Mother (Memory)",
        text: "Always remember - strength isn't just about winning. It's about protecting those you love.",
        portrait: "mother_warm"
      },
      {
        type: "fade",
        duration: 1000
      },
      {
        type: "narration",
        text: "Five years later..."
      },
      {
        type: "dialogue",
        speaker: "Professor Khadgar",
        text: "Welcome to the world of WoWmon! Today, you begin your journey.",
        portrait: "khadgar_excited"
      }
    ]
  },

  mentor_death: {
    id: "mentor_death",
    scenes: [
      {
        type: "battle_pause",
        text: "Garrick steps in front of you!"
      },
      {
        type: "animation",
        animation: "void_blast_hits_garrick"
      },
      {
        type: "dialogue",
        speaker: "Garrick",
        text: "Tell her story... don't let them forget... the heroes...",
        portrait: "garrick_dying",
        voice: "strained"
      },
      {
        type: "fade",
        duration: 2000,
        color: "black"
      },
      {
        type: "set_flag",
        flag: "mentorDied"
      }
    ]
  }
};

function playCutscene(cutsceneId) {
  const cutscene = cutscenes[cutsceneId];
  if (!cutscene) return;

  gameState.inCutscene = true;
  let sceneIndex = 0;

  function playNextScene() {
    if (sceneIndex >= cutscene.scenes.length) {
      endCutscene();
      return;
    }

    const scene = cutscene.scenes[sceneIndex];
    sceneIndex++;

    switch(scene.type) {
      case 'dialogue':
        showDialogue(scene.speaker, scene.text, scene.portrait);
        break;
      case 'narration':
        showNarration(scene.text);
        break;
      case 'fade':
        fadeScreen(scene.duration, scene.color || 'black');
        setTimeout(playNextScene, scene.duration);
        return;
      case 'animation':
        playAnimation(scene.animation);
        break;
      case 'set_flag':
        gameState.story.flags[scene.flag] = true;
        playNextScene();
        return;
      case 'battle_pause':
        showBattleText(scene.text);
        break;
    }

    // Wait for user input to continue (except for auto-continue scenes)
    if (!scene.autoContinue) {
      waitForInput(playNextScene);
    }
  }

  playNextScene();
}

function endCutscene() {
  gameState.inCutscene = false;
  // Resume gameplay
}
```

---

## 3. Implementation Checklist

### Phase 1: Core Story Framework (Week 1-2)
- [ ] Implement story state object in game save data
- [ ] Create dialogue system (show dialogue, parse text, display portraits)
- [ ] Implement karma tracking
- [ ] Create relationship system
- [ ] Build flag system for story progression
- [ ] Implement basic cutscene player

### Phase 2: Chapter Structure (Week 3-4)
- [ ] Write Prologue and Chapter 1 dialogue
- [ ] Implement chapter progression gates
- [ ] Create rival character with multiple battle instances
- [ ] Implement first gym leader with story integration
- [ ] Test basic story flow

### Phase 3: Character Development (Week 5-6)
- [ ] Write all 12 main chapters
- [ ] Implement relationship tracking with key NPCs
- [ ] Create character-specific side quests
- [ ] Add NPC reaction system based on karma/relationships
- [ ] Implement rival corruption arc

### Phase 4: Choice System (Week 7-8)
- [ ] Implement Chapter 9 major choice system
- [ ] Create branching cutscenes for each choice
- [ ] Implement consequence tracking
- [ ] Build different dialogue paths for each choice
- [ ] Test all three rival fate outcomes

### Phase 5: Endgame Content (Week 9-10)
- [ ] Implement Elite Four with story integration
- [ ] Create Champion corruption battle
- [ ] Implement mother confrontation scene
- [ ] Build N'Zoth final boss battle
- [ ] Create all three main endings

### Phase 6: Side Content (Week 11-12)
- [ ] Implement 10 core side quests
- [ ] Create Dragon Egg system
- [ ] Build corruption mechanic for WoWmons
- [ ] Add flashback/memory scenes
- [ ] Implement post-game content for each path

### Phase 7: Polish (Week 13-14)
- [ ] Add all character portraits
- [ ] Implement background music system with themes
- [ ] Create emotional scene effects (tears, screen shake, etc.)
- [ ] Add achievement tracking
- [ ] Balance karma and relationship thresholds
- [ ] Playtest entire story multiple times

---

## 4. Quick Reference: Story Milestones

### Chapter Unlocks
- **Chapter 1**: First rival battle, Route 1 access
- **Chapter 2**: Stormwind/Orgrimmar unlocked, First Badge
- **Chapter 3**: Darkshire unlocked, Mentor dies, First cult encounter
- **Chapter 4**: Wetlands unlocked, Second Badge, Earthen Ring intro
- **Chapter 5**: Dragonblight unlocked, Dragon Aspects met, Dragon Egg received
- **Chapter 6**: Icecrown unlocked, Third Badge, Rival shows darkness
- **Chapter 7**: Deepholm unlocked, Fourth Badge, Rival corrupted
- **Chapter 8**: Emerald Dream unlocked, Purification power obtained
- **Chapter 9**: THE CHOICE - Rival's fate decided
- **Chapter 10**: Elite Four unlocked, Champion battle
- **Chapter 11**: Ny'alotha unlocked, Mother confrontation
- **Chapter 12**: N'Zoth battle, Game completion, Epilogue

### Key Flag Checks
```javascript
// Example: NPC dialogue changes based on story progress
if (gameState.story.flags.mentorDied) {
  dialogue = "I heard about Garrick. I'm so sorry...";
} else {
  dialogue = "How's your training with Garrick going?";
}

// Example: Area access
if (gameState.story.currentChapter >= 5 && gameState.story.flags.dragonEggReceived) {
  allowAccessTo('wyrmrest_temple_inner_sanctum');
}

// Example: Rival dialogue
if (gameState.story.choices.rivalFate === 'saved') {
  rivalDialogue = "Thanks for not giving up on me.";
} else if (gameState.story.choices.rivalFate === 'defeated') {
  // Rival is gone
  rivalDialogue = null;
} else {
  // Sacrifice path
  showMemorial('rival_memorial');
}
```

---

## 5. Testing Scenarios

### Test Case 1: Hero Path
1. Choose Alliance, Water starter
2. Help all NPCs (karma +50)
3. Show mercy in all battles
4. Build relationships with all major characters
5. Chapter 9: Save rival
6. Defeat Champion without killing
7. Save mother
8. Verify True Hero ending

### Test Case 2: Dark Champion Path
1. Choose Horde, Fire starter
2. Ignore NPC requests (karma -30)
3. Aggressive battle choices
4. Chapter 9: Defeat rival
5. Use corrupted WoWmons
6. Verify Dark Champion ending

### Test Case 3: Bittersweet Path
1. Choose Alliance, Nature starter
2. High karma throughout (+40)
3. Strong rival relationship
4. Chapter 9: Rival sacrifices
5. Complete rival's side quests posthumously
6. Verify Bittersweet ending

---

## 6. Common Issues and Solutions

### Issue: Story flag not setting
**Solution**: Check conditions are met, verify flag name matches exactly

### Issue: Dialogue not showing
**Solution**: Check dialogue conditions, verify chapter progression

### Issue: Cutscene getting stuck
**Solution**: Ensure each scene has proper continuation logic

### Issue: Choice not registering
**Solution**: Verify choice callback is executing, check save data persistence

### Issue: Karma not affecting ending
**Solution**: Check ending determination logic includes karma thresholds

---

## File Paths
- Main Story Data: `/game/data/story/`
- Dialogue Database: `/game/data/dialogues/`
- Cutscene Definitions: `/game/data/cutscenes/`
- Character Profiles: `/game/data/characters/`

---

**Last Updated**: 2025-10-12
**Version**: 1.0
**Status**: Ready for Implementation
