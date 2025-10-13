# AGENT 7: STORY-DRIVEN STRATEGY DESIGN
## WoWmon: Narrative-Focused Campaign System

**Document Version:** 1.0
**Date:** 2025-10-12
**Focus:** Story, Narrative, Campaign Mode, and Single-Player Experience

---

## EXECUTIVE SUMMARY

This design document outlines a comprehensive story-driven experience for WoWmon that transforms it from a creature collection game into an epic narrative journey through Azeroth. The focus is on creating memorable story moments, character development, meaningful choices, and engaging PvE encounters.

---

## 1. NARRATIVE FRAMEWORK

### 1.1 Core Story Structure

**Main Campaign: "The Shadow Rising"**

**Act 1: Awakening (Levels 1-15)**
- **Setting:** Goldshire and surrounding territories
- **Conflict:** Strange corruptions appearing in the forest
- **Character Development:** Player begins as a novice trainer, mentored by veteran trainers
- **Key NPCs:**
  - Professor Bronzebeard (mentor)
  - Captain Alara (alliance guard)
  - Mysterious Hooded Figure (recurring antagonist)
- **Story Beats:**
  1. Choose your starter creature and bond with it
  2. Investigate disappearing wildlife
  3. First encounter with corrupted creatures
  4. Discovery of ancient Shadow Stones
  5. Gym Leader Muradin reveals partial truth about the corruption

**Act 2: The Gathering Storm (Levels 15-30)**
- **Setting:** Expanded territories (Darkshire, Westfall, Duskwood)
- **Conflict:** Shadow corruption spreading, creatures becoming aggressive
- **Character Development:** Player becomes regional champion, trusted by Alliance
- **Key NPCs:**
  - Malfurion Stormrage (reveals ancient history)
  - Jaina Proudmoore (provides magical insight)
  - The Defias Brotherhood (morally gray faction)
- **Story Beats:**
  1. Multiple gym challenges with story integration
  2. Discovery of Shadow Lord's plan to corrupt all creatures
  3. Moral choices: save corrupted creatures or destroy them?
  4. Faction choice: Alliance-focused or neutral path
  5. First encounter with legendary Shadow Beast

**Act 3: Into Darkness (Levels 30-45)**
- **Setting:** Undercity, Plaguelands, forbidden territories
- **Conflict:** Direct confrontation with Shadow Lord's forces
- **Character Development:** Player becomes legendary trainer, makes world-altering choices
- **Key NPCs:**
  - Thrall (Horde perspective and alliance)
  - Lady Sylvanas (complex anti-hero)
  - Shadow Lord Mal'Ganis (primary antagonist)
- **Story Beats:**
  1. Journey into enemy territory
  2. Uncover truth about Shadow Stones (ancient Titan artifacts)
  3. Elite Four challenges tied to story progression
  4. Corruption of player's starter creature (temporary)
  5. Alliance between Alliance and Horde factions

**Act 4: The Final Stand (Levels 45-50+)**
- **Setting:** Mount Hyjal, World Tree, Shadow Realm
- **Conflict:** Final battle to prevent Azeroth's corruption
- **Character Development:** Player's choices throughout campaign affect ending
- **Story Beats:**
  1. Assembling legendary team for final battles
  2. Multi-stage boss battle against Shadow Lord
  3. Sacrifice choices: which NPCs survive?
  4. Multiple endings based on choices
  5. Post-game: rebuilding Azeroth

### 1.2 Branching Narrative System

**Major Choice Points:**

1. **Starter Choice Consequences** (Level 5)
   - Murloc path: Water-focused story, coastal territories
   - Wisp path: Nature-focused story, forest territories
   - Imp path: Fire/demon-focused story, darker territories

2. **The Corrupted Creature Dilemma** (Level 18)
   - **Choice A:** Purify corrupted creatures (peaceful route)
   - **Choice B:** Defeat corrupted creatures (combat route)
   - **Choice C:** Study corruption (research route)
   - **Impact:** Changes available abilities, NPCs react differently, different boss patterns

3. **Faction Allegiance** (Level 25)
   - **Alliance Path:** More structured progression, honor-based rewards
   - **Horde Path:** More freedom, power-based rewards
   - **Neutral Path:** Access to both, unique legendary encounters

4. **The Betrayal** (Level 35)
   - **Choice:** Trust the mysterious informant or follow your mentor's advice
   - **Impact:** One path leads to temporary loss of strongest creature, other leads to NPC death

5. **The Final Sacrifice** (Level 48)
   - **Choice:** Sacrifice your starter creature to purify Shadow Stones OR find alternative solution
   - **Impact:** Different final boss patterns, different endings

### 1.3 Character Relationship System

**Companion NPCs (Travel with player periodically):**

1. **Captain Alara** (Alliance Warrior)
   - **Bond Level 1-5:** Unlocks dialogue, special training sessions
   - **Max Bond Reward:** Legendary warrior-type creature, special team training ability
   - **Story Role:** Protector, represents duty and honor

2. **Lyra Dawnseeker** (Mage Researcher)
   - **Bond Level 1-5:** Unlocks lore entries, creature insights
   - **Max Bond Reward:** Rare magical-type creature, ability to identify creature weaknesses
   - **Story Role:** Scholar, represents knowledge and curiosity

3. **Grimtusk** (Horde Outcast)
   - **Bond Level 1-5:** Unlocks underground trading, rare items
   - **Max Bond Reward:** Powerful beast-type creature, survival skills
   - **Story Role:** Outcast, represents redemption and second chances

**Relationship Mechanics:**
- Conversations at key story points
- Side quests tied to companion backstories
- Combat synergy bonuses when using creatures they gift
- Romance-lite elements (friendship-focused, age-appropriate)
- Companions can be called for help in difficult battles

---

## 2. CAMPAIGN PROGRESSION SYSTEM

### 2.1 Story Milestone Structure

**World State Tracking:**
```javascript
campaignState: {
    act: 1,                      // Current act (1-4)
    storyProgress: 0,            // 0-100 per act
    majorChoices: [],            // Array of choice IDs and selections
    npcRelationships: {},        // NPC ID -> bond level
    unlockedRegions: [],         // Map IDs
    worldEvents: [],             // Active world events
    corruption Level: 0,         // 0-100, affects world state
    factionReputation: {
        alliance: 0,
        horde: 0,
        neutral: 0
    },
    storyFlags: {
        starterChosen: false,
        firstGymDefeated: false,
        corruptionDiscovered: false,
        betrayalRevealed: false,
        finalBattleUnlocked: false
    }
}
```

### 2.2 Quest System Architecture

**Quest Types:**

1. **Main Story Quests** (Red marker)
   - Required for progression
   - Unlock new areas and features
   - Major story revelations
   - Cannot be declined

2. **Character Quests** (Blue marker)
   - Develop NPC relationships
   - Optional but provide major rewards
   - Affect story outcomes
   - Multiple solutions possible

3. **World Quests** (Yellow marker)
   - Environmental challenges
   - Help civilians, protect villages
   - Build reputation
   - Dynamic events based on world state

4. **Secret Quests** (No marker)
   - Hidden throughout the world
   - Require exploration and observation
   - Unlock legendary creatures/items
   - Provide lore insights

**Quest Structure Example:**

```javascript
questSystem: {
    "quest_shadow_investigation": {
        id: "quest_shadow_investigation",
        name: "Shadows in the Forest",
        type: "main_story",
        act: 1,
        level: 8,
        description: "Investigate the strange shadows appearing near Goldshire",

        objectives: [
            {
                type: "explore",
                target: "dark_grove",
                description: "Explore the Dark Grove",
                completed: false
            },
            {
                type: "battle",
                target: "corrupted_wolf",
                count: 3,
                description: "Defeat 3 Corrupted Wolves",
                completed: false,
                current: 0
            },
            {
                type: "collect",
                target: "shadow_essence",
                count: 5,
                description: "Collect Shadow Essence samples",
                completed: false,
                current: 0
            },
            {
                type: "dialogue",
                target: "npc_professor",
                description: "Report findings to Professor Bronzebeard",
                completed: false
            }
        ],

        rewards: {
            experience: 500,
            money: 750,
            items: ["shadow_detector", "health_potion:3"],
            unlocks: ["dark_grove_fast_travel"],
            storyProgress: 10
        },

        dialogue: {
            start: [
                "Professor Bronzebeard looks worried.",
                "Something dark stirs in the forest, young trainer.",
                "Creatures are behaving strangely near the old grove.",
                "Will you investigate? Be careful out there."
            ],
            progress: {
                "corrupted_wolf_1": [
                    "This creature... it's not normal!",
                    "Its eyes are filled with shadow!",
                    "We must find the source of this corruption."
                ]
            },
            complete: [
                "You've done well, young trainer.",
                "But I fear this is only the beginning...",
                "These Shadow Essences... I've seen them before.",
                "Long ago, before you were born.",
                "We must prepare. Darker days lie ahead."
            ]
        },

        nextQuest: "quest_shadow_temple",
        prerequisite: ["quest_first_steps", "gym_badge_1"]
    }
}
```

### 2.3 Dynamic World Events

**World State Changes Based on Progress:**

1. **Corruption Spread**
   - Visual changes to maps as corruption increases
   - More aggressive wild encounters
   - NPCs react differently based on world state
   - Timed events: "The village needs help NOW!"

2. **Seasonal Story Events**
   - Harvest Festival: Peaceful creature exhibition, bonding activities
   - Shadow Moon: Increased undead encounters, special rewards
   - Dragon Flight: Rare dragon sightings, legendary encounters
   - Winter Veil: Story interludes, character moments

3. **Consequence System**
   - Failed to save a village in time? It remains corrupted
   - Chose violence over peace? NPCs remember
   - Ignored side quests? Miss out on allies in final battle
   - World permanently changes based on your choices

---

## 3. TEAM BUILDER SYSTEM (Story-Integrated)

### 3.1 Story-Driven Team Building

**Team Composition Philosophy:**
- Teams reflect player's journey and choices
- Creatures gained through story have unique abilities
- Synergies unlock based on narrative bonds

**Team Builder Features:**

```javascript
storyTeamBuilder: {
    // Maximum 12 creatures (2 teams of 6)
    totalSlots: 12,
    activeTeam: 6,

    // Team roles based on story
    roles: [
        {
            name: "Starter's Legacy",
            slot: 1,
            locked: true,  // Always your starter or evolution
            storyBonus: "+20% all stats when in first slot",
            description: "Your first companion, forever bonded to you"
        },
        {
            name: "The Protector",
            slot: 2,
            requirement: "Complete Alara's Bond Quest",
            storyBonus: "Takes reduced damage from boss attacks",
            description: "A creature trained in defensive tactics"
        },
        {
            name: "The Striker",
            slot: 3,
            requirement: "Defeat 50 enemies",
            storyBonus: "+15% critical hit chance",
            description: "Your primary offensive force"
        },
        {
            name: "The Sage",
            slot: 4,
            requirement: "Complete Lyra's Research Quests",
            storyBonus: "Magical abilities cost less PP",
            description: "A creature attuned to magical energies"
        },
        {
            name: "The Wild Card",
            slot: 5,
            requirement: "Befriend Grimtusk",
            storyBonus: "Unpredictable bonus effects in battle",
            description: "A creature from the untamed lands"
        },
        {
            name: "The Legend",
            slot: 6,
            requirement: "Complete Act 3",
            storyBonus: "Can use ultimate abilities",
            description: "A legendary creature from myth"
        }
    ],

    // Team Synergies
    synergies: [
        {
            name: "Bond of Heroes",
            requirement: "All creatures obtained through story quests",
            effect: "+10% HP to all team members",
            description: "Your companions fight harder when together"
        },
        {
            name: "Alliance United",
            requirement: "All creatures from Alliance territories",
            effect: "Increased defense against shadow attacks",
            description: "United against the darkness"
        },
        {
            name: "Horde Strength",
            requirement: "All creatures from Horde territories",
            effect: "Increased attack against corrupted enemies",
            description: "Raw power overwhelms corruption"
        },
        {
            name: "Elemental Harmony",
            requirement: "Balance of all elemental types",
            effect: "Type advantages increased by 50%",
            description: "The elements work in perfect balance"
        },
        {
            name: "Legends Assembled",
            requirement: "Three or more legendary creatures",
            effect: "Once per battle, survive lethal damage",
            description: "Legends don't fall easily"
        }
    ],

    // Story-based Team Presets
    storyPresets: {
        "The Hero's Journey": {
            description: "Your canonical story team",
            creatures: ["starter", "alara_gift", "lyra_gift", "wild_dragon", "shadow_redemption", "legendary_phoenix"],
            unlockedBy: "Story progression"
        },
        "The Purifiers": {
            description: "Team specialized against corruption",
            creatures: ["ancient_wisp", "phoenix", "naga", "treant", "elemental", "dragon"],
            unlockedBy: "Choose peaceful path"
        },
        "The Shadow Hunters": {
            description: "Fight fire with fire",
            creatures: ["imp", "felhound", "banshee", "ghoul", "dire_wolf", "infernal"],
            unlockedBy: "Choose aggressive path"
        }
    },

    // Memorial System
    memorial: {
        description: "Creatures that fell in your journey",
        permadeath: false,  // Optional hardcore mode
        tributeEffects: "Fighting in memory of fallen grants +5% stats",
        canRevive: true,
        reviveCost: "Special story quest"
    }
}
```

### 3.2 Creature Development Through Story

**Story-Based Evolution:**

```javascript
storyEvolution: {
    "murloc": {
        normalEvolution: {
            level: 16,
            evolveTo: "murloc_warrior",
            trigger: "Standard level up"
        },
        storyEvolution: {
            level: 16,
            evolveTo: "murloc_tidehunter",  // Alternate evolution
            trigger: "Complete 'Tides of War' quest",
            bonuses: ["Water Mastery ability", "+10 Speed"],
            description: "Trained by the Tidehunters of Kul Tiras"
        }
    },

    "wisp": {
        normalEvolution: {
            level: 18,
            evolveTo: "ancient_wisp"
        },
        storyEvolution: {
            level: 18,
            evolveTo: "emerald_guardian",  // Alternate evolution
            trigger: "High bond with Malfurion + Complete Nature's Call",
            bonuses: ["Rejuvenation ability", "Nature's Blessing passive"],
            description: "Blessed by the Emerald Dream itself"
        }
    },

    // Redemption Evolution (corrupted creatures can be purified)
    "corrupted_wolf": {
        redemptionEvolution: {
            evolveTo: "dire_wolf_pure",
            trigger: "Complete purification ritual quest",
            bonuses: ["Shadow Resistance", "Purifying Aura"],
            description: "A creature saved from darkness becomes stronger"
        }
    }
}
```

### 3.3 Team Training & Bonding

**Training Montage System:**
```javascript
trainingSystem: {
    // Special training sessions with NPC mentors
    mentorTraining: {
        "captain_alara": {
            specialty: "Defense and Tactics",
            sessions: [
                {
                    name: "Shield Wall Basics",
                    duration: "1 story hour",
                    effect: "+5 Defense to trained creature",
                    unlocks: "Defensive Stance ability",
                    story: "Alara teaches you the importance of protection"
                },
                {
                    name: "Last Stand",
                    duration: "3 story hours",
                    effect: "Learn 'Guardian' ability",
                    requirement: "Bond Level 3",
                    story: "Face impossible odds in training simulation"
                }
            ]
        },

        "malfurion": {
            specialty: "Nature Magic",
            sessions: [
                {
                    name: "Commune with Nature",
                    duration: "2 story hours",
                    effect: "+10 Nature-type move power",
                    unlocks: "Natural Healing passive",
                    story: "Meditate beneath the World Tree"
                },
                {
                    name: "Emerald Dream Vision",
                    duration: "5 story hours",
                    effect: "Unlock hidden nature-type creature",
                    requirement: "Complete Act 2, Bond Level 4",
                    story: "Journey into the Emerald Dream"
                }
            ]
        }
    },

    // Team bonding activities (visual novel style)
    bondingActivities: {
        "camping": {
            description: "Set up camp and bond with your team",
            time: "Night only",
            effects: [
                "Random stat boost to party",
                "Unlock creature backstory dialogue",
                "Chance for wild legendary encounter",
                "Heal all creatures"
            ],
            dialogue: "Dynamic dialogue based on team composition"
        },

        "training_together": {
            description: "Intense training session for your team",
            effects: [
                "+EXP to all creatures",
                "Improve team synergy",
                "Unlock combination moves"
            ],
            story: "Montage cutscene based on team composition"
        },

        "heart_to_heart": {
            description: "Have a meaningful conversation with your starter",
            effects: [
                "Increase bond level",
                "Unlock unique ability",
                "Story revelation about starter's past"
            ],
            story: "Deep character moment, choices matter"
        }
    }
}
```

---

## 4. BATTLE SYSTEM (PvE Focus)

### 4.1 Boss Battle Design Philosophy

**Principles:**
1. Every boss tells a story
2. Mechanics reflect character/lore
3. Multiple solutions based on team composition
4. Memorable setpiece moments
5. Fair but challenging

### 4.2 Boss Battle Archetypes

**Type 1: The Corrupted Guardian**
```javascript
boss_corrupted_treant: {
    name: "Ancient Treant - Corrupted",
    level: 20,
    phase: 1,
    maxPhases: 3,

    story: "Once protector of the forest, now consumed by shadow",

    mechanics: {
        phase1: {
            description: "Aggressive but predictable",
            abilities: ["Vine Whip", "Root Trap", "Shadow Thorns"],
            pattern: "Standard rotation",
            weakness: "Fire moves deal double damage",
            healTrigger: {
                at: "50% HP",
                effect: "Roots emerge, heal 25% HP over time",
                counterplay: "Destroy roots (targetable sub-entities)"
            }
        },

        phase2: {
            hp: "60%",
            description: "Shadow corruption intensifies",
            transformation: "Visual change, darker color, red eyes",
            newAbilities: ["Shadow Beam", "Corrupted Seeds"],
            pattern: "More aggressive, less predictable",
            weakness: "Nature moves now only deal normal damage",
            mechanicAdded: "Corrupted Seeds spawn mini-enemies",
            story: "The treant fights against the corruption but fails"
        },

        phase3: {
            hp: "30%",
            description: "Desperation - full corruption",
            transformation: "Shadow form, intimidating",
            ultimateAbility: {
                name: "Shadow Apocalypse",
                warning: "The treant gathers dark energy!",
                counter Time: "2 turns",
                counterplay: "Deal enough damage OR use purification item",
                failure: "Massive damage to all creatures"
            },
            story: "Make choice: destroy it or purify it"
        }
    },

    rewards: {
        standard: {
            exp: 2000,
            money: 1500,
            items: ["shadow_essence:5", "treant_bark"]
        },
        purified: {
            exp: 2500,
            money: 1500,
            items: ["shadow_essence:5", "treant_bark", "purification_token"],
            special: "Treant survives and joins as ally NPC",
            storyImpact: "Village saved, NPCs grateful"
        },
        destroyed: {
            exp: 1800,
            money: 2000,
            items: ["shadow_essence:10", "corrupted_wood"],
            special: "Obtain Dark Seed (plant for shadow-type creature)",
            storyImpact: "Village mourns loss, player questioned"
        }
    },

    dialogue: {
        intro: [
            "The ancient treant stands before you, wreathed in shadow.",
            "Its eyes flicker between green and red.",
            "For a moment, you see pain and recognition.",
            "Then the shadow takes over...",
            "BATTLE START!"
        ],
        phase2: [
            "The shadows dig deeper!",
            "The treant's cry echoes with anguish!",
            "Is there anything left to save?"
        ],
        phase3_destroy: [
            "The treant falls to the ground.",
            "The shadow dissipates into the air.",
            "...but at what cost?",
            "The forest grows quiet."
        ],
        phase3_purify: [
            "Light breaks through the shadow!",
            "The treant's eyes return to green!",
            "It bows its massive head in gratitude.",
            "The forest sighs in relief."
        ]
    }
}
```

**Type 2: The Rival Trainer**
```javascript
boss_rival_trainer: {
    name: "Shadow Blade - Rival Trainer",
    type: "trainer_battle",
    level: 25,

    story: "Your rival, corrupted by ambition and shadow power",

    team: [
        {
            species: "dire_wolf",
            level: 24,
            moves: ["Shadow Claw", "Crunch", "Ice Fang", "Howl"],
            ai: "aggressive",
            strategy: "Setup sweeper - uses Howl then attacks"
        },
        {
            species: "corrupted_elemental",
            level: 25,
            moves: ["Shadow Blast", "Barrier", "Explosion", "Toxic"],
            ai: "defensive",
            strategy: "Stall tank - sets up barriers and poisons"
        },
        {
            species: "shadow_dragon",
            level: 26,
            moves: ["Shadow Rage", "Dragon Claw", "Aerial Ace", "Dark Pulse"],
            held Item: "shadow_stone",  // Powers up shadow moves
            ai: "intelligent",
            strategy: "Adapts to player's team, switches intelligently"
        }
    ],

    mechanics: {
        // Rival makes strategic switches
        switching: true,

        // Rival uses items
        items: [
            "greater_health_potion:2",
            "full_restore:1"
        ],

        // Special mechanics
        shadowForm: {
            trigger: "When down to last creature at 25% HP",
            effect: "Dragon enters Shadow Form - +50% all stats, new moveset",
            counter: "Use purification abilities or overwhelm with type advantage",
            story: "Your rival loses control, shadow takes over"
        }
    },

    dialogue: {
        pre_battle: [
            "So we meet again, old friend.",
            "...Or should I say, former friend?",
            "The shadow has shown me true power.",
            "Power you're too weak to grasp!",
            "Let me show you the difference between us!"
        ],

        mid_battle: {
            "losing": [
                "No... this can't be!",
                "I have the shadow's power!",
                "I won't lose to you!"
            ],
            "winning": [
                "Is that all you've got?",
                "I expected more from my rival.",
                "The shadow chose wisely when it chose me!"
            ]
        },

        shadow_form: [
            "ENOUGH!",
            "The Shadow Blade screams in pain!",
            "Dark energy surrounds his dragon!",
            "You watch in horror as your rival is consumed...",
            "This is no longer just a battle!"
        ],

        post_battle_defeat_rival: [
            "...I... lost?",
            "The shadow... promised me power...",
            "Why... why did I trust it?",
            "The dark energy fades from his eyes.",
            "*Your old friend collapses.*",
            "I'm... sorry. I was so focused on being strong...",
            "...that I forgot what truly matters.",
            "Thank you... for saving me from myself."
        ],

        post_battle_alternate: [
            "*If you chose to purify rather than defeat*",
            "The light... it burns!",
            "But it's... warm...",
            "I can see clearly now.",
            "What have I done?",
            "Can you... ever forgive me?"
        ]
    },

    rewards: {
        victory: {
            exp: 3000,
            money: 2500,
            items: ["shadow_stone", "rival's_badge"],
            story: "Rival becomes ally"
        }
    },

    consequences: {
        victory: {
            story: "Rival joins you for final battles",
            unlocks: ["double_battles", "rival_summon_ability"],
            relationship: "max_bond_with_rival"
        },
        defeat: {
            story: "Rival must be saved later through side quest",
            changes: "More difficult final boss (rival fights against you)",
            canRetry: true
        }
    }
}
```

**Type 3: The Raid Boss**
```javascript
boss_raid_shadow_lord: {
    name: "Mal'Ganis, The Shadow Lord",
    type: "raid_boss",
    phases: 5,
    recommended Team: "Full team of level 45+",

    story: "The architect of Azeroth's corruption, ancient and powerful",

    unique Mechanic: "FULL TEAM BATTLE",
    description: "All 6 creatures fight simultaneously in 3v1 format",

    phase1: {
        name: "The Demon Awakens",
        hp: "100-80%",
        creatures: 3,  // Player uses 3 at once
        abilities: [
            {
                name: "Shadow Blast",
                target: "single",
                power: 80,
                effect: "Random target"
            },
            {
                name: "Dark Command",
                target: "all",
                power: 40,
                effect: "Forces random creature to skip turn"
            },
            {
                name: "Corruption Aura",
                target: "field",
                power: 0,
                effect: "All creatures take 5% max HP per turn"
            }
        ],
        mechanic: "Must rotate creatures to avoid corruption buildup",
        story: [
            "The Shadow Lord emerges from the portal.",
            "His presence alone makes your creatures hesitate.",
            "This is the final battle. Everything depends on you!"
        ]
    },

    phase2: {
        name: "Army of Shadows",
        hp: "80-60%",
        adds: true,
        summons: [
            {type: "shadow_minion", count: 4},
            {type: "corrupted_beast", count: 2}
        ],
        mechanic: "Must defeat adds or they empower boss",
        abilities: [
            "Previous abilities",
            {
                name: "Summon Shadows",
                trigger: "Every 3 turns",
                effect: "Summon 2 shadow minions"
            }
        ],
        story: [
            "Mal'Ganis laughs mockingly.",
            "'You think you can defeat me alone?'",
            "'Let me show you true power!'",
            "Shadows pour from the portal!"
        ]
    },

    phase3: {
        name: "The Shadow Revealed",
        hp: "60-40%",
        transformation: "Shadow form - increased stats",
        creatures: 6,  // Now player uses full team
        mechanic: "Boss targets based on creature types - strategic positioning",
        abilities: [
            "Enhanced versions of previous abilities",
            {
                name: "Shadow Nova",
                target: "all",
                power: 60,
                charge Time: 2,
                warning: "Dark energy gathers around Mal'Ganis!",
                counter: "Use defensive abilities or deal massive damage"
            },
            {
                name: "Corrupt",
                target: "strongest creature",
                effect: "Temporarily control player's strongest creature",
                duration: "2 turns",
                counter: "Damage your own creature or use purification"
            }
        ],
        story: [
            "The Shadow Lord's true form emerges!",
            "Reality itself seems to bend around him!",
            "Your companions stand with you - all of them!",
            "This is where legends are born!"
        ]
    },

    phase4: {
        name: "Desperation",
        hp: "40-20%",
        mechanic: "CHOICE MOMENT",
        choice: {
            description: "Your starter creature offers to sacrifice itself to weaken the boss",
            option1: {
                choice: "Accept the sacrifice",
                effect: "Starter faints but boss loses 30% HP and defense down",
                story: "Your first friend gives everything for you",
                emotional: "HIGH"
            },
            option2: {
                choice: "Refuse - find another way",
                effect: "Harder fight but starter survives",
                requirement: "High bond with all creatures",
                story: "Together, you find strength you didn't know you had",
                emotional: "HIGH"
            }
        },
        abilities: "All previous abilities, increased frequency",
        story: "Dynamic based on player choice"
    },

    phase5: {
        name: "The Final Stand",
        hp: "20-0%",
        mechanic: "LEGENDARY MOMENT",
        specialAbility: {
            name: "Bond of Legends",
            trigger: "Automatically activates",
            effect: "All your creatures gain +50% stats, team attacks available",
            description: "Your journey, your bonds, your determination - all culminate here"
        },
        bossUltimate: {
            name: "Apocalypse",
            trigger: "At 5% HP",
            description: "Mal'Ganis attempts to destroy everything",
            mechanic: "DPS check - must deal 10,000 damage in 3 turns",
            failure: "Boss fully heals to 50%",
            success: "Boss defeated, epic victory"
        },
        story: [
            "The Shadow Lord trembles with rage!",
            "'Impossible! I AM ETERNAL!'",
            "Your creatures glow with light!",
            "The bonds you've forged... they're your true power!",
            "Together, you unleash your final attack!"
        ]
    },

    rewards: {
        exp: 10000,
        money: 10000,
        items: [
            "shadow_lord_essence",
            "legendary_soul_stone",
            "champion's_crown",
            "master_trainer_badge"
        ],
        unlocks: [
            "postgame_content",
            "legendary_creature_encounters",
            "new_game_plus",
            "ultimate_team_builder"
        ],
        title: "Shadow Slayer",
        achievement: "Legend of Azeroth"
    },

    ending: {
        cutscene: "Epic conclusion based on all your choices",
        impacts: [
            "NPCs you helped appear in victory celebration",
            "Creatures you saved stand beside you",
            "Rivals you redeemed fight alongside you",
            "Choices throughout journey affect ending scene"
        ],
        epilogue: "Where are they now?" style for all major characters
    }
}
```

### 4.3 Regular Encounter Design

**Dynamic Encounters Based on Story:**

```javascript
encounterSystem: {
    // Encounters change based on story progress
    storyBasedEncounters: {
        "route1_early": {
            condition: "Act 1, before gym 1",
            creatures: ["gnoll:60%", "kobold:30%", "wolf:10%"],
            levels: "3-6",
            behavior: "passive",
            story: "Wild creatures, curious but cautious"
        },

        "route1_corrupted": {
            condition: "Act 2, corruption spreading",
            creatures: ["corrupted_gnoll:40%", "corrupted_kobold:30%", "shadow_beast:20%", "gnoll:10%"],
            levels: "15-20",
            behavior: "aggressive",
            story: "Corruption spreads, creatures attack on sight"
        },

        "route1_restored": {
            condition: "Act 4, after purification",
            creatures: ["gnoll:40%", "wolf:30%", "wisp:20%", "rare_legendary:1%"],
            levels: "40-45",
            behavior: "peaceful",
            story: "Nature restored, rare creatures return"
        }
    },

    // Special encounters triggered by story
    specialEncounters: {
        "legendary_phoenix_sighting": {
            trigger: "Random 1% after completing 'Rebirth' quest",
            location: "Mount Hyjal",
            description: "A flash of fire streaks across the sky!",
            oneTime: true,
            difficulty: "very_hard",
            rewards: "Chance to capture Phoenix"
        },

        "ghost_of_past": {
            trigger: "Return to starting area after Act 3",
            description: "You encounter a familiar face...",
            encounter: "Ghost of NPC who died in your playthrough",
            purpose: "Closure, emotional moment, special item",
            battle: false
        },

        "mirror_match": {
            trigger: "Secret location, post-game",
            description: "You face a shadowy version of yourself",
            encounter: "Your own team but corrupted",
            difficulty: "nightmare",
            reward: "Ultimate soul stone"
        }
    }
}
```

### 4.4 Environmental Battle Mechanics

**Battles Affected by Story and Location:**

```javascript
environmentalBattles: {
    "corrupted_forest": {
        effect: "Shadow-type moves +20% power",
        visualEffect: "Dark fog, ominous atmosphere",
        story: "The corruption empowers dark creatures"
    },

    "world_tree": {
        effect: "Nature-type moves +30% power, healing increased",
        visualEffect: "Beautiful glowing leaves, peaceful",
        story: "Nature's power is strongest here"
    },

    "storm_peaks": {
        effect: "Weather changes randomly, affects battle",
        mechanics: {
            "rain": "Water moves +50%, Fire moves -50%",
            "snow": "Ice moves +50%, Speed reduced",
            "lightning": "Electric moves +50%, random paralyze chance"
        },
        story: "The elements are wild and unpredictable"
    },

    "shadow_realm": {
        effect: "All creatures take corruption damage each turn",
        mechanic: "Must finish battle quickly or lose",
        visual: "Nightmarish twisted landscape",
        story: "This realm is hostile to all life"
    }
}
```

---

## 5. ADDITIONAL STORY FEATURES

### 5.1 Dialogue System

**Rich Dialogue Tree Structure:**

```javascript
dialogueSystem: {
    npcConversations: {
        "captain_alara": {
            greetings: {
                "first_meeting": [
                    "You must be the new trainer.",
                    "Professor Bronzebeard has told me about you.",
                    "Welcome to Goldshire. I'm Captain Alara.",
                    {
                        choice: true,
                        options: [
                            {
                                text: "Nice to meet you!",
                                response: "alara_friendly",
                                bond: +5
                            },
                            {
                                text: "I don't need a babysitter.",
                                response: "alara_cold",
                                bond: -5
                            },
                            {
                                text: "What's your story?",
                                response: "alara_curious",
                                bond: +3,
                                unlocks: "alara_backstory_quest"
                            }
                        ]
                    }
                ],

                "act2_meeting": [
                    "*Alara looks exhausted, her armor dented*",
                    "Thank the Light you're here.",
                    "The corruption is spreading faster than we can contain.",
                    "I've lost three good soldiers this week.",
                    {
                        choice: true,
                        options: [
                            {
                                text: "We'll stop this together.",
                                response: "alara_encouraged",
                                effect: "Alara joins you for next quest",
                                bond: +10
                            },
                            {
                                text: "Sounds like you need better soldiers.",
                                response: "alara_hurt",
                                bond: -15,
                                consequence: "Alara unavailable for rest of act"
                            },
                            {
                                text: "Tell me about the soldiers you lost.",
                                response: "alara_memorial",
                                bond: +8,
                                unlocks: "memorial_side_quest",
                                emotional: "HIGH"
                            }
                        ]
                    }
                ]
            },

            bondDialogue: {
                level1: "Basic conversations, quest-related",
                level2: "Personal questions available",
                level3: "Backstory revealed",
                level4: "Deep personal conversations",
                level5: "Lifetime friendship, always available as ally"
            },

            specialDialogue: {
                "after_death_scene": [
                    "*If you witnessed an NPC death*",
                    "I heard what happened to Marcus.",
                    "...",
                    "He was a good man.",
                    {
                        choice: true,
                        options: [
                            {
                                text: "I'm sorry I couldn't save him.",
                                response: "alara_grief",
                                emotional: "HIGH"
                            },
                            {
                                text: "He died a hero.",
                                response: "alara_honor"
                            },
                            {
                                text: "*Say nothing, just nod*",
                                response: "alara_understood"
                            }
                        ]
                    }
                ]
            }
        }
    },

    // Creature dialogue (yes, your creatures can "talk")
    creatureDialogue: {
        "starter_creature": {
            bond_level_5: [
                "*Your starter looks at you with understanding*",
                "You sense deep gratitude and loyalty.",
                "It's ready to give everything for you.",
                "Because you've given everything for it.",
                "*Your bond is unbreakable.*"
            ],

            pre_sacrifice: [
                "*Your starter steps forward*",
                "You sense its determination.",
                "It knows what must be done.",
                "It looks back at you one last time...",
                {
                    choice: true,
                    options: [
                        {
                            text: "No! I won't let you!",
                            response: "find_another_way",
                            requirement: "All NPC bonds maxed",
                            emotional: "CRITICAL"
                        },
                        {
                            text: "Thank you... for everything.",
                            response: "accept_sacrifice",
                            emotional: "CRITICAL"
                        }
                    ]
                }
            ]
        }
    }
}
```

### 5.2 Memory System

**The Game Remembers Everything:**

```javascript
memorySystem: {
    // NPCs remember your actions
    npcMemory: {
        "saved_village": {
            npcs: ["village_elder", "villagers"],
            permanentEffect: "Villagers always friendly, discount in shops",
            dialogue: "You're the one who saved us!",
            longTerm: "Mentioned in ending"
        },

        "let_village_burn": {
            npcs: ["village_elder", "survivor"],
            permanentEffect: "NPCs distrustful, some shops closed",
            dialogue: "Where were you when we needed you?",
            longTerm: "Haunts you in Act 4",
            redemption: "Special very difficult quest can redeem"
        }
    },

    // Creatures remember battles
    creatureMemory: {
        "rival_battles": [
            "First battle: Starter remembers",
            "Rematch: Special dialogue if you use same starter",
            "Final battle: Callback to first battle"
        ],

        "legendary_encounters": [
            "If you caught a legendary peacefully vs forcefully",
            "Affects its loyalty and power in battle",
            "Some legendaries can refuse to fight for cruel trainers"
        ]
    },

    // World remembers your choices
    worldMemory: {
        "corruption_path": {
            "purification": "World slowly heals, nature returns",
            "destruction": "Corruption gone but land scarred",
            "mixed": "Some areas beautiful, others damaged"
        },

        "faction_choices": {
            "alliance": "Horde territories less friendly",
            "horde": "Alliance territories less friendly",
            "neutral": "Both sides respect you, unique dialogues"
        }
    }
}
```

### 5.3 Journal & Lore System

**Extensive Lore Collection:**

```javascript
journalSystem: {
    // Automatic journal entries
    storyJournal: {
        autoRecord: true,
        entries: [
            {
                title: "Day 1 - The Journey Begins",
                content: "Today I received my first creature from Professor Bronzebeard...",
                autoGenerated: true,
                includesPlayerChoices: true
            },
            {
                title: "The Shadow in the Forest",
                content: "I saw something terrible today. The creatures... they were corrupted...",
                triggers: "After first corrupted encounter"
            }
        ],

        illustrations: "ASCII art or simple drawings for major moments"
    },

    // Creature encyclopedia
    creatureDex: {
        entries: [
            {
                species: "murloc",
                discovered: true,
                caught: true,
                evolved: false,
                lore: [
                    "The Murloc is an amphibious humanoid...",
                    "Known for their distinctive gurgling speech...",
                    "Often underestimated despite their numbers..."
                ],
                locations: ["Goldshire Pond", "Westfall Coast", "Any water"],
                variants: ["Normal", "Corrupted", "Tidehunter"],
                behaviorNotes: "Player can add their own notes"
            }
        ],

        completion Rewards: {
            "10_creatures": "Research Grant - 1000 gold",
            "25_creatures": "Master Researcher title",
            "all_creatures": "Legendary creature egg"
        }
    },

    // Lore collectibles
    loreFragments: {
        "shadow_stones_origin": {
            fragments: 8,
            foundLocations: "Hidden throughout world",
            readsLike: "Dark Souls item descriptions",
            reward: "Complete lore unlocks secret boss",
            content: [
                "Fragment 1: '...in the beginning, the Titans forged...'",
                "Fragment 2: '...but one stone was corrupted...'",
                "Fragment 8: '...and so the Shadow Lord was born.'"
            ]
        }
    },

    // NPC backstories
    npcBiographies: {
        unlockCondition: "Max bond",
        replayable: "Can replay any story you've unlocked",
        examples: {
            "captain_alara": {
                title: "The Knight's Oath",
                story: "Told through flashback sequences",
                reveals: "Why she's so dedicated to protecting others",
                emotional: "Very high",
                rewards: "Unique shield item for your creatures"
            }
        }
    }
}
```

### 5.4 Post-Game Content

**Story Continues:**

```javascript
postGameContent: {
    // New Game Plus
    newGamePlus: {
        unlocks: "After beating main story",
        carries Over: ["Creature dex", "Key items", "One creature of choice"],
        changes: [
            "Harder difficulty",
            "New story branches",
            "Hidden scenes available from start",
            "Secret third starter option",
            "Ability to make different major choices"
        ],
        goal: "See all possible outcomes"
    },

    // Battle Tower
    battleTower: {
        name: "Champions' Gauntlet",
        story: "Prove yourself against legends",
        challenges: [
            {
                floor: "1-10",
                difficulty: "normal",
                opponents: "Random trainers"
            },
            {
                floor: "11-20",
                difficulty: "hard",
                opponents: "Gym leaders rematches"
            },
            {
                floor: "21-50",
                difficulty: "nightmare",
                opponents: "Legendary trainers",
                special: "Some are previous player characters from different timelines"
            },
            {
                floor: "100",
                boss: "Your rival from another timeline where they won",
                story: "Epic confrontation with what you could have become",
                reward: "True ending unlock"
            }
        ]
    },

    // Epilogue quests
    epilogueQuests: {
        "rebuilding_azeroth": {
            description: "Help rebuild what was destroyed",
            quests: [
                "Restore corrupted areas",
                "Reunite separated creature families",
                "Help NPCs find peace"
            ],
            emotional: "Closure and healing",
            rewards: "Peaceful ending variants"
        },

        "the_last_legend": {
            description: "One final challenge awaits",
            requirement: "100% completion",
            encounter: "Shadow Lord from the future",
            story: "He warns you of an even greater threat",
            sequel_hook: "Sets up potential sequel",
            reward: "Ultimate legendary creature"
        }
    }
}
```

---

## 6. IMPLEMENTATION PRIORITIES

### Phase 1: Core Narrative Framework (Weeks 1-3)
1. Implement basic quest system with tracking
2. Create story progression flags and world state
3. Build dialogue system with choice tracking
4. Add journal and memory systems

### Phase 2: Campaign Act 1 (Weeks 4-6)
1. Complete Act 1 story with all quests
2. Implement first 2 gym leaders with story integration
3. Add NPC relationship system basics
4. Create first boss battle (Corrupted Treant)

### Phase 3: Battle System Enhancement (Weeks 7-9)
1. Implement boss battle mechanics (phases, special abilities)
2. Add environmental battle effects
3. Create team synergy system
4. Build trainer AI with strategy

### Phase 4: Team Builder & Bonding (Weeks 10-12)
1. Story-integrated team builder interface
2. Mentor training system
3. Bonding activities and events
4. Story evolution paths

### Phase 5: Acts 2-3 Content (Weeks 13-18)
1. Complete Act 2 and 3 stories
2. All gym leaders and elite four
3. Major boss battles
4. Branch ing narrative choices

### Phase 6: Final Content & Polish (Weeks 19-24)
1. Act 4 and final boss battle
2. Multiple endings implementation
3. Post-game content
4. New Game Plus
5. Extensive playtesting and balance

---

## 7. DESIGN NOTES & PHILOSOPHY

### Narrative Design Principles

1. **Player Agency Matters**
   - Choices have real consequences
   - No "fake choices" - everything affects something
   - Multiple solutions to most problems

2. **Emotional Investment**
   - Make players care about NPCs and creatures
   - Earned emotional moments, not manipulation
   - Balance levity and darkness

3. **Respect Player Time**
   - Main story: 15-20 hours
   - 100% completion: 40-50 hours
   - Replayable with different outcomes

4. **Show, Don't Tell**
   - Environmental storytelling
   - Character actions over exposition
   - Let players discover lore

5. **Memorable Moments**
   - Set pieces that players remember
   - "Water cooler" moments to discuss
   - Screenshot-worthy scenes

### Story-Gameplay Integration

- Never separate story from gameplay
- Cutscenes are short and impactful
- Gameplay mechanics reinforce narrative themes
- Story choices affect battle mechanics

### Accessibility

- Story difficulty separate from battle difficulty
- Options to skip battles but not story
- Journal recap for returning players
- Clear quest markers and objectives

---

## 8. CONCLUSION

This design transforms WoWmon from a creature collection game into a narrative-driven RPG adventure. Every system - team building, battles, progression - is integrated with story and character development.

The focus on PvE content, boss battles, and single-player experience creates a cohesive campaign where players feel like the hero of their own epic tale. Multiple branching paths and consequences ensure replayability while maintaining a strong central narrative.

The combination of Warcraft lore, Pokemon-style mechanics, and choice-driven storytelling creates a unique experience that respects the player's time and investment while delivering memorable, emotional moments.

---

**END OF DESIGN DOCUMENT**

*"Your journey awaits, Champion of Azeroth."*
