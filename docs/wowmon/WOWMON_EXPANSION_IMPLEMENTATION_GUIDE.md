# WoWMon Expansion: Implementation Guide
## Quick Reference for Adding New Content

---

## 1. ADDING NEW CREATURES

### Basic Creature Template
```javascript
"creature_id": {
    "id": "creature_id",
    "name": "DISPLAYNAME",
    "type": ["type1", "type2"],
    "baseHp": 50,
    "baseAttack": 60,
    "baseDefense": 55,
    "baseSpecialAttack": 70,
    "baseSpecialDefense": 65,
    "baseSpeed": 75,
    "evolveLevel": 30,
    "evolveTo": "evolution_id",
    "moves": ["move1", "move2", "move3", "move4"],
    "ability": "ability_name",
    "description": "Creature description text"
}
```

### Evolution Chain Example (3-Stage)
```javascript
// Stage 1: Basic
"shadowling": {
    "id": "shadowling",
    "name": "SHADOWLING",
    "type": ["shadow"],
    "baseHp": 35,
    "baseAttack": 40,
    "baseDefense": 35,
    "baseSpecialAttack": 55,
    "baseSpecialDefense": 45,
    "baseSpeed": 60,
    "evolveLevel": 25,
    "evolveTo": "darkling",
    "moves": ["shadow_ball", "tackle", "confuse_ray", "dark_pulse"],
    "ability": "shadow_cloak",
    "description": "A small spirit born from pure darkness."
},

// Stage 2: Mid
"darkling": {
    "id": "darkling",
    "name": "DARKLING",
    "type": ["shadow", "spirit"],
    "baseHp": 55,
    "baseAttack": 60,
    "baseDefense": 55,
    "baseSpecialAttack": 85,
    "baseSpecialDefense": 70,
    "baseSpeed": 80,
    "evolveLevel": 50,
    "evolveTo": "void_lord",
    "moves": ["shadow_ball", "dark_pulse", "nightmare", "void_strike"],
    "ability": "shadow_cloak",
    "description": "Growing in power, it feeds on fear and darkness."
},

// Stage 3: Final
"void_lord": {
    "id": "void_lord",
    "name": "VOIDLORD",
    "type": ["shadow", "spirit", "magic"],
    "baseHp": 80,
    "baseAttack": 75,
    "baseDefense": 70,
    "baseSpecialAttack": 125,
    "baseSpecialDefense": 95,
    "baseSpeed": 105,
    "evolveLevel": null,
    "evolveTo": null,
    "moves": ["void_rift", "dark_pulse", "nightmare", "psychic"],
    "ability": "void_master",
    "description": "A master of the void with reality-bending powers."
}
```

### Legendary Creature Template
```javascript
"ragnaros": {
    "id": "ragnaros",
    "name": "RAGNAROS",
    "type": ["fire", "earth", "spirit"],
    "baseHp": 105,
    "baseAttack": 125,
    "baseDefense": 90,
    "baseSpecialAttack": 140,
    "baseSpecialDefense": 95,
    "baseSpeed": 85,
    "evolveLevel": null,
    "evolveTo": null,
    "moves": ["sulfuras_smash", "earthquake", "inferno", "eruption"],
    "ability": "flame_lord",
    "legendary": true,
    "catchRate": 0.01,
    "description": "The Firelord, an elemental of living flame and molten rage."
}
```

---

## 2. ADDING NEW MOVES

### Physical Move
```javascript
"shadow_strike": {
    "name": "Shadow Strike",
    "power": 80,
    "accuracy": 100,
    "pp": 15,
    "type": "shadow",
    "category": "physical",
    "effect": "high_crit_in_darkness",
    "description": "Always crits when used in darkness or at night."
}
```

### Special Move
```javascript
"void_rift": {
    "name": "Void Rift",
    "power": 120,
    "accuracy": 90,
    "pp": 5,
    "type": "shadow",
    "category": "special",
    "effect": "reality_tear",
    "description": "Tears reality itself, dealing massive shadow damage."
}
```

### Status Move
```javascript
"time_warp": {
    "name": "Time Warp",
    "power": 0,
    "accuracy": 100,
    "pp": 5,
    "type": "magic",
    "category": "status",
    "effect": "extra_turn",
    "description": "Bends time to grant the user an extra turn."
}
```

### Weather Move
```javascript
"fel_storm": {
    "name": "Fel Storm",
    "power": 0,
    "accuracy": 100,
    "pp": 5,
    "type": "demon",
    "category": "status",
    "effect": "weather_fel",
    "description": "Summons a fel storm that boosts demon-type moves."
}
```

### Move with Secondary Effect
```javascript
"shadow_bite": {
    "name": "Shadow Bite",
    "power": 70,
    "accuracy": 100,
    "pp": 20,
    "type": "shadow",
    "category": "physical",
    "secondaryEffect": {
        "chance": 30,
        "effect": "flinch"
    },
    "description": "A vicious bite that may make the foe flinch."
}
```

---

## 3. ADDING NEW REGIONS

### Basic Map Template
```javascript
"region_name": {
    "name": "Display Name",
    "width": 25,
    "height": 20,
    "tiles": [
        // 25x20 grid of tile IDs
        2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        2,1,1,1,1,1,1,9,9,9,1,1,1,1,9,9,9,1,1,1,1,1,1,1,2,
        // ... more rows
    ],
    "npcs": [
        {
            "id": "npc_id",
            "x": 10,
            "y": 10,
            "sprite": 1,
            "dialogue": "NPC dialogue text",
            "trainer": true, // Optional
            "team": ["creature1", "creature2"] // If trainer
        }
    ],
    "warps": [
        {
            "x": 12,
            "y": 19,
            "toMap": "other_map",
            "toX": 15,
            "toY": 1
        }
    ],
    "encounters": [
        { "id": "creature1", "rate": 40 },
        { "id": "creature2", "rate": 30 },
        { "id": "creature3", "rate": 20 },
        { "id": "creature4", "rate": 10 }
    ]
}
```

### Gym Map Template
```javascript
"darnassus_gym": {
    "name": "Moonwell Gym",
    "width": 15,
    "height": 15,
    "tiles": [
        // Nature-themed gym with obstacles
    ],
    "npcs": [
        {
            "id": "gym_trainer1",
            "x": 5,
            "y": 5,
            "sprite": 3,
            "dialogue": "Nature's power flows through me!",
            "trainer": true,
            "team": ["sprite", "dryad"]
        },
        {
            "id": "gym_trainer2",
            "x": 10,
            "y": 5,
            "sprite": 3,
            "dialogue": "The forest protects us!",
            "trainer": true,
            "team": ["ancient_guardian", "treant_lord"]
        },
        {
            "id": "gym_leader",
            "x": 7,
            "y": 7,
            "sprite": 8,
            "dialogue": "I am Tyrande! The moon guides my path!",
            "trainer": true,
            "gymLeader": "gym5"
        }
    ],
    "warps": [
        { "x": 7, "y": 14, "toMap": "darnassus", "toX": 15, "toY": 10 }
    ],
    "encounters": []
}
```

---

## 4. ADDING GYM LEADERS

### Gym Leader Definition
```javascript
"trainers": {
    "gym5": {
        "name": "TYRANDE",
        "title": "The High Priestess",
        "sprite": 5,
        "team": ["sprite", "dryad", "ancient_guardian", "celestial"],
        "reward": 5000,
        "badge": "Moonwell Badge",
        "dialogue": "The goddess Elune blesses my creatures with her light!"
    }
}
```

### Elite Four Member
```javascript
"elite_shadow": {
    "name": "SHADOW MASTER",
    "title": "Master of Darkness",
    "sprite": 11,
    "team": ["void_lord", "nightmare_weaver", "shadowfang", "darkling", "shade"],
    "reward": 10000,
    "eliteFour": true,
    "dialogue": "The shadows will consume you!"
}
```

### Champion
```javascript
"champion": {
    "name": "ANDUIN WRYNN",
    "title": "Champion of Azeroth",
    "sprite": 13,
    "team": [
        "light_dragon",
        "celestial",
        "silver_hand",
        "royal_griffon",
        "magistrate",
        "ancient_guardian"
    ],
    "reward": 20000,
    "champion": true,
    "dialogue": "I fight for the Alliance and for all of Azeroth!"
}
```

---

## 5. LEGENDARY ENCOUNTER SYSTEMS

### Static Legendary (Fixed Location)
```javascript
// In map NPCs array
{
    "id": "ragnaros_encounter",
    "x": 15,
    "y": 10,
    "sprite": 20, // Special legendary sprite
    "dialogue": "TOO SOON, EXECUTUS!",
    "legendary": true,
    "creature": "ragnaros",
    "level": 70,
    "respawn": true, // Respawns if not caught
    "respawnDays": 7
}
```

### Roaming Legendary (Appears Randomly)
```javascript
// Add to game state
this.roamingLegendaries = {
    "deathwing": {
        "id": "deathwing",
        "level": 75,
        "active": false, // Activates after Elite Four
        "currentMap": null,
        "fleeRate": 0.5 // 50% chance to flee each turn
    },
    "thunderaan": {
        "id": "thunderaan",
        "level": 70,
        "active": false,
        "currentMap": null,
        "fleeRate": 0.3,
        "weatherRequired": "storm" // Only appears in storms
    }
}
```

### Quest-Based Legendary
```javascript
// Add to achievements/quests
"old_god_quest": {
    "id": "old_god_quest",
    "name": "Whispers in the Deep",
    "description": "Collect 4 Old God relics",
    "steps": [
        { "type": "item", "item": "eye_of_cthun", "found": false },
        { "type": "item", "item": "heart_of_yogg", "found": false },
        { "type": "item", "item": "tentacle_of_nzoth", "found": false },
        { "type": "item", "item": "skull_of_yshaarj", "found": false }
    ],
    "reward": {
        "type": "legendary_encounter",
        "creature": "nzoth",
        "level": 75
    }
}
```

---

## 6. EVOLUTION SYSTEMS

### Level-Based Evolution
```javascript
// Standard evolution (handled in existing code)
"evolveLevel": 30,
"evolveTo": "next_form"
```

### Stone Evolution
```javascript
// Add to items
"shadow_stone": {
    "name": "Shadow Stone",
    "type": "evolution",
    "price": 3000,
    "effect": "evolve_shadow",
    "description": "Evolves certain creatures into shadow forms.",
    "evolutionPaths": {
        "sprite": "dark_sprite",
        "wisp": "dark_wisp",
        "imp": "satyr"
    }
}
```

### Friendship Evolution
```javascript
// Add friendship tracking
"shadowling": {
    // ... other stats
    "evolveCondition": {
        "type": "friendship",
        "value": 200,
        "evolveTo": "loyal_shadow"
    }
}
```

### Location-Based Evolution
```javascript
"whelp": {
    // ... other stats
    "evolveCondition": {
        "type": "location",
        "map": "blackrock_mountain",
        "level": 35,
        "evolveTo": "chromatic_drake"
    }
}
```

### Time-Based Evolution
```javascript
"werewolf_pup": {
    // ... other stats
    "evolveCondition": {
        "type": "time",
        "timeOfDay": "night",
        "level": 25,
        "evolveTo": "werewolf"
    }
}
```

---

## 7. BATTLE MECHANICS EXTENSIONS

### Weather Effects
```javascript
"weatherEffects": {
    "fel_storm": {
        "name": "Fel Storm",
        "boosts": {
            "demon": 1.5,
            "fire": 1.5
        },
        "nerfs": {
            "light": 0.5,
            "nature": 0.5
        },
        "damagePerTurn": {
            "excludeTypes": ["demon", "fire", "shadow"],
            "damage": 0.0625 // 1/16 HP per turn
        }
    },
    "light_blessing": {
        "name": "Light's Blessing",
        "boosts": {
            "light": 1.5
        },
        "healPerTurn": {
            "includeTypes": ["light"],
            "amount": 0.0625 // 1/16 HP per turn
        }
    }
}
```

### Terrain Effects
```javascript
"terrainEffects": {
    "lava_field": {
        "name": "Lava Field",
        "damagePerTurn": {
            "excludeTypes": ["fire", "earth"],
            "damage": 0.125 // 1/8 HP per turn
        },
        "boosts": {
            "fire": 1.3
        }
    },
    "hallowed_ground": {
        "name": "Hallowed Ground",
        "preventStatus": ["curse", "poison", "burn"],
        "boosts": {
            "light": 1.3
        }
    }
}
```

### Ability System
```javascript
"abilities": {
    "void_master": {
        "name": "Void Master",
        "effect": "shadow_boost",
        "description": "Boosts shadow moves by 50%",
        "onBattleStart": function(creature) {
            creature.shadowBoost = 1.5;
        }
    },
    "flame_lord": {
        "name": "Flame Lord",
        "effect": "fire_immunity",
        "description": "Immune to fire attacks and burns",
        "onReceiveAttack": function(move, creature) {
            if (move.type === 'fire') return 0; // No damage
        }
    },
    "regeneration": {
        "name": "Regeneration",
        "effect": "heal_per_turn",
        "description": "Heals 1/16 HP each turn",
        "onTurnEnd": function(creature) {
            creature.hp += Math.floor(creature.maxHp / 16);
            if (creature.hp > creature.maxHp) creature.hp = creature.maxHp;
        }
    }
}
```

---

## 8. POST-GAME CONTENT

### Battle Tower
```javascript
"battle_tower": {
    "name": "Battle Tower",
    "floors": 100,
    "floorTypes": ["single", "double", "rotation"],
    "rewards": {
        10: { "type": "item", "item": "rare_candy", "count": 3 },
        25: { "type": "item", "item": "master_soul_stone", "count": 1 },
        50: { "type": "creature", "creature": "special_reward", "level": 70 },
        75: { "type": "item", "item": "golden_ticket", "count": 1 },
        100: { "type": "title", "title": "Tower Master" }
    },
    "enemyScaling": {
        "baseLevel": 50,
        "levelPerFloor": 0.5,
        "maxLevel": 100
    }
}
```

### Safari Zone
```javascript
"safari_zone": {
    "name": "Creature Safari",
    "areas": [
        {
            "name": "Grassland",
            "creatures": ["rare1", "rare2", "rare3"],
            "rareRate": 0.1
        },
        {
            "name": "Water Edge",
            "creatures": ["water_rare1", "water_rare2"],
            "rareRate": 0.05
        },
        {
            "name": "Mountain Peak",
            "creatures": ["dragon_rare1", "flying_rare1"],
            "rareRate": 0.02
        }
    ],
    "mechanics": {
        "balls": 30,
        "steps": 500,
        "throwAccuracy": 1.5,
        "fleeRate": 0.3
    }
}
```

### Creature Contests
```javascript
"contests": {
    "beauty": {
        "name": "Beauty Contest",
        "stats": ["appearance", "grace", "charm"],
        "rewards": ["beauty_ribbon", "rare_candy"]
    },
    "strength": {
        "name": "Strength Contest",
        "stats": ["power", "defense", "endurance"],
        "rewards": ["strength_ribbon", "protein"]
    },
    "intelligence": {
        "name": "Intelligence Contest",
        "stats": ["special", "wisdom", "strategy"],
        "rewards": ["smart_ribbon", "calcium"]
    }
}
```

---

## 9. ACHIEVEMENT SYSTEM

### Achievement Template
```javascript
"achievements": {
    "legendary_master": {
        "id": "legendary_master",
        "name": "Legendary Master",
        "description": "Capture all 25 legendary creatures",
        "reward": {
            "type": "title",
            "title": "Legend Hunter"
        },
        "condition": {
            "type": "legendary_count",
            "count": 25
        },
        "hidden": false,
        "points": 100
    },
    "shiny_hunter": {
        "id": "shiny_hunter",
        "name": "Shiny Hunter",
        "description": "Capture 50 shiny creatures",
        "reward": {
            "type": "item",
            "item": "shiny_charm",
            "count": 1
        },
        "condition": {
            "type": "shiny_count",
            "count": 50
        },
        "hidden": false,
        "points": 150
    },
    "perfect_team": {
        "id": "perfect_team",
        "name": "Perfect Team",
        "description": "Build a team of 6 perfect IV creatures",
        "reward": {
            "type": "money",
            "amount": 100000
        },
        "condition": {
            "type": "perfect_ivs",
            "count": 6
        },
        "hidden": true,
        "points": 200
    }
}
```

---

## 10. QUICK ADDITION CHECKLIST

### Adding a New Creature:
- [ ] Create creature object in `creatures` section
- [ ] Add base stats (HP, Attack, Defense, Sp.Atk, Sp.Def, Speed)
- [ ] Set type(s)
- [ ] Define evolution (level/stone/special)
- [ ] Assign 4 moves
- [ ] Write description
- [ ] Add to encounter tables (wild areas)
- [ ] Test evolution chain

### Adding a New Region:
- [ ] Design map layout (width x height)
- [ ] Create tile array
- [ ] Add NPCs (trainers, story, shops)
- [ ] Set up warps (connections to other maps)
- [ ] Define wild encounters
- [ ] Add gym/special building if needed
- [ ] Connect to existing world map

### Adding a New Legendary:
- [ ] Create legendary creature (high stats)
- [ ] Set `legendary: true` flag
- [ ] Design encounter method (static/roaming/quest)
- [ ] Create special location/event
- [ ] Add to legendary tracker
- [ ] Design signature move
- [ ] Set catch rate (very low)

### Adding a New Move:
- [ ] Define move object
- [ ] Set power, accuracy, PP
- [ ] Set type and category (physical/special/status)
- [ ] Add special effects if any
- [ ] Write description
- [ ] Add to creature move pools

---

## STAT CALCULATION FORMULAS

### Base Stat Totals by Tier:
- **Basic (Stage 1):** 250-320 total
- **Mid (Stage 2):** 380-450 total
- **Final (Stage 3):** 500-580 total
- **Legendary:** 600-720 total
- **Mythic:** 680-780 total

### Damage Formula:
```javascript
damage = ((2 * level / 5 + 2) * power * attack / defense / 50 + 2) * modifier

modifier = STAB * typeEffectiveness * critical * random(0.85, 1.0) * weather * ability
```

### Catch Rate Formula:
```javascript
catchRate = ((3 * maxHP - 2 * currentHP) * catchRateModifier * ballModifier) / (3 * maxHP)

// For legendaries:
baseCatchRate = 0.01 (1%)
masterBallRate = 1.0 (100%)
```

---

## TYPE EFFECTIVENESS CHART

### Super Effective (2x):
- Fire > Nature, Ice
- Water > Fire, Earth
- Nature > Water, Earth
- Electric > Water, Flying
- Ice > Nature, Dragon, Flying
- Shadow > Magic, Spirit
- Light > Shadow, Undead
- Dragon > Dragon

### Not Very Effective (0.5x):
- Fire < Water, Earth
- Water < Nature, Electric
- Nature < Fire, Ice
- Electric < Earth
- Shadow < Light
- Light < Shadow

### Immune (0x):
- Earth < Electric (ground immune)
- Flying < Earth (flying immune)
- Spirit < Normal (ghost immune)
- Normal < Spirit (normal immune)

---

## NEXT STEPS FOR IMPLEMENTATION

1. **Start with Wave 1** - Add 30 core evolutions
2. **Build out 3 regions** - Darnassus, Winterspring, Blackrock
3. **Add 2 gym leaders** - Tyrande and update Jaina's location
4. **Implement 5 legendaries** - Ragnaros, Al'akir, Neptulon, Therazane, Thunderaan
5. **Test and balance** - Ensure gameplay feels good
6. **Iterate** - Add more waves gradually

---

This guide provides all the templates and formulas needed to massively expand WoWMon. Each section can be copy-pasted and modified to add new content quickly!
