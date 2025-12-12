#!/usr/bin/env python3
"""
DOTA 2 Hero Generator for LEVIATHAN
Generates individual JSON files for each of the 124 DOTA 2 heroes
with abilities adapted for the game mechanics.
"""

import json
import os

# Base directory for hero files
HEROES_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'games', 'heroes')

# Hero definitions with abilities (adapted from DOTA 2)
HEROES = {
    "abaddon": {
        "name": "Abaddon",
        "title": "Lord of Avernus",
        "attr": "universal",
        "icon": "shield",
        "lore": "The Font of Avernus is the source of a family's strength, a well of dark power that infuses the blood of every noble in the House of Avernus.",
        "baseStats": {
            "maxHp": 120, "maxMana": 80, "hpPerLevel": 28, "manaPerLevel": 18,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "mistCoil": {
                "name": "Mist Coil",
                "type": "active",
                "description": "Abaddon releases a coil of deathly mist that damages an enemy or heals an ally at the cost of his own health.",
                "damage": 25, "heal": 30, "selfDamage": 10,
                "cooldown": 6000, "manaCost": 15, "range": 8
            },
            "aphotic_shield": {
                "name": "Aphotic Shield",
                "type": "active",
                "description": "Summons dark energies around an ally, creating a shield that absorbs damage. When the shield breaks, it explodes and damages nearby enemies.",
                "shieldAmount": 40, "burstDamage": 20, "duration": 5000,
                "cooldown": 10000, "manaCost": 20, "range": 6
            },
            "curse_of_avernus": {
                "name": "Curse of Avernus",
                "type": "passive",
                "description": "Abaddon strikes enemies with his cursed blade, slowing them and causing those nearby to receive increased damage.",
                "slowPercent": 20, "bonusDamagePercent": 15, "duration": 3000
            },
            "borrowedTime": {
                "name": "Borrowed Time",
                "type": "ultimate",
                "description": "When activated, all damage dealt to Abaddon heals instead of hurting him. Automatically triggers when his health drops too low.",
                "duration": 6000, "autoTriggerThreshold": 0.25,
                "cooldown": 60000, "manaCost": 0
            }
        },
        "talents": {
            "10": ["+5 Armor", "+15 Movement Speed"],
            "15": ["+20% XP Gain", "+30 Mist Coil Heal"],
            "20": ["+100 Aphotic Shield Health", "+25 Damage"],
            "25": ["300 AoE Mist Coil", "+1s Borrowed Time Duration"]
        }
    },
    "alchemist": {
        "name": "Alchemist",
        "title": "Razzil Darkbrew",
        "attr": "strength",
        "icon": "potion",
        "lore": "The sacred science of Chymistry was invented by a keen observer who noticed the crystalline powder at the bottom of the brewing pot.",
        "baseStats": {
            "maxHp": 130, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "acidSpray": {
                "name": "Acid Spray",
                "type": "active",
                "description": "Sprays acid in a target area, damaging enemies over time and reducing their armor.",
                "damagePerSecond": 8, "armorReduction": 4, "duration": 6000, "radius": 6,
                "cooldown": 16000, "manaCost": 25, "range": 12
            },
            "unstableConcoction": {
                "name": "Unstable Concoction",
                "type": "active",
                "description": "Alchemist brews a volatile concoction that he can throw at enemies. The longer it brews, the more damage and stun it deals.",
                "minDamage": 20, "maxDamage": 60, "minStun": 1000, "maxStun": 3000,
                "brewTime": 4000, "cooldown": 14000, "manaCost": 20, "range": 8
            },
            "greedyGain": {
                "name": "Greedy Gain",
                "type": "passive",
                "description": "Alchemist synthesizes gold from enemies, gaining bonus gold and collecting bounty runes from a distance.",
                "bonusGoldPercent": 25, "stackPerKill": 5, "maxStacks": 20
            },
            "chemicalRage": {
                "name": "Chemical Rage",
                "type": "ultimate",
                "description": "Alchemist drinks a potent brew, transforming him into a raging beast with increased health regeneration and attack speed.",
                "bonusHpRegen": 15, "bonusAttackSpeed": 50, "bonusMoveSpeed": 30, "duration": 10000,
                "cooldown": 55000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Damage", "+200 Health"],
            "15": ["+25% Cleave", "+10 Chemical Rage Regen"],
            "20": ["+30 Attack Speed", "+4s Chemical Rage"],
            "25": ["-0.2s Chemical Rage BAT", "+50% Greedy Gain Gold"]
        }
    },
    "ancient_apparition": {
        "name": "Ancient Apparition",
        "title": "Kaldr",
        "attr": "intelligence",
        "icon": "frost",
        "lore": "Kaldr, the Ancient Apparition, is an image projected from outside time. He springs from the cold, infinite void that both predates the universe and awaits its end.",
        "baseStats": {
            "maxHp": 80, "maxMana": 120, "hpPerLevel": 20, "manaPerLevel": 25,
            "baseDamage": 12, "damagePerLevel": 2.5, "armor": 1, "armorPerLevel": 0.3,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "coldFeet": {
                "name": "Cold Feet",
                "type": "active",
                "description": "Places a frozen hex on an enemy. Unless they move away, they become frozen and stunned.",
                "damage": 15, "stunDuration": 2500, "requiredDistance": 6, "duration": 4000,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "iceVortex": {
                "name": "Ice Vortex",
                "type": "active",
                "description": "Creates a vortex of icy energy that slows enemies and increases magic damage they take.",
                "slowPercent": 25, "magicAmpPercent": 15, "duration": 8000, "radius": 5,
                "cooldown": 6000, "manaCost": 15, "range": 12
            },
            "chillingTouch": {
                "name": "Chilling Touch",
                "type": "passive",
                "description": "Adds a chilling effect to attacks, dealing bonus magic damage and slowing attack speed.",
                "bonusDamage": 12, "attackSlowPercent": 20, "duration": 2000
            },
            "iceBless": {
                "name": "Ice Blast",
                "type": "ultimate",
                "description": "Launches a tracer that creates an expanding ice blast at its location. Enemies hit cannot heal and shatter if their health drops too low.",
                "damage": 50, "shatterThreshold": 0.12, "debuffDuration": 10000,
                "cooldown": 45000, "manaCost": 40, "range": 999
            }
        },
        "talents": {
            "10": ["+25 Damage", "+10% Magic Resistance"],
            "15": ["+100 Chilling Touch Damage", "-3s Ice Vortex Cooldown"],
            "20": ["+3s Cold Feet Stun", "+5% Ice Vortex Slow"],
            "25": ["Ice Blast Pierces Immunity", "+4% Ice Blast Kill Threshold"]
        }
    },
    "anti_mage": {
        "name": "Anti-Mage",
        "title": "Magina",
        "attr": "agility",
        "icon": "blade",
        "lore": "The monks of Turstarkuri watched the rugged valleys from their mountain temple, practicing meditation and martial arts.",
        "baseStats": {
            "maxHp": 90, "maxMana": 60, "hpPerLevel": 22, "manaPerLevel": 12,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 13, "attackRange": 2, "attackSpeed": 1.4
        },
        "abilities": {
            "manaBurn": {
                "name": "Mana Break",
                "type": "passive",
                "description": "Burns mana from enemies with each attack, dealing bonus damage equal to mana burned.",
                "manaBurnPercent": 8, "damagePerMana": 0.8
            },
            "blink": {
                "name": "Blink",
                "type": "active",
                "description": "Short distance teleportation that allows Anti-Mage to move instantly to a target point.",
                "range": 12, "cooldown": 6000, "manaCost": 10
            },
            "spellShield": {
                "name": "Counterspell",
                "type": "active",
                "description": "Creates a shield that blocks and reflects targeted spells back at the caster.",
                "passiveMagicResist": 25, "reflectDuration": 1500,
                "cooldown": 12000, "manaCost": 15
            },
            "manaVoid": {
                "name": "Mana Void",
                "type": "ultimate",
                "description": "Deals massive damage to a target based on how much mana they're missing. Stuns and damages nearby enemies.",
                "damagePerMissingMana": 1.0, "stunDuration": 1500, "radius": 5,
                "cooldown": 70000, "manaCost": 35, "range": 8
            }
        },
        "talents": {
            "10": ["+10 Strength", "+20 Attack Speed"],
            "15": ["-1s Blink Cooldown", "+15 Agility"],
            "20": ["+0.5% Max Mana Burn", "Blink Uncontrollable Illusion"],
            "25": ["+25% Counterspell Magic Resistance", "-50s Mana Void Cooldown"]
        }
    },
    "axe": {
        "name": "Axe",
        "title": "Mogul Khan",
        "attr": "strength",
        "icon": "axe",
        "lore": "As a grunt in the Turstarkuri army, Mogul Khan had no rival in combat, and no equal on the field of war.",
        "baseStats": {
            "maxHp": 150, "maxMana": 60, "hpPerLevel": 32, "manaPerLevel": 14,
            "baseDamage": 20, "damagePerLevel": 3.5, "armor": 4, "armorPerLevel": 0.7,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "berserkerCall": {
                "name": "Berserker's Call",
                "type": "active",
                "description": "Axe taunts all nearby enemies, forcing them to attack him while gaining bonus armor.",
                "radius": 5, "duration": 2500, "bonusArmor": 8,
                "cooldown": 14000, "manaCost": 20
            },
            "battleHunger": {
                "name": "Battle Hunger",
                "type": "active",
                "description": "Enrages an enemy, causing them to take damage over time until they kill a unit or the duration ends.",
                "damagePerSecond": 12, "slowPercent": 15, "duration": 6000,
                "cooldown": 10000, "manaCost": 18, "range": 8
            },
            "counterHelix": {
                "name": "Counter Helix",
                "type": "passive",
                "description": "When attacked, Axe has a chance to spin and deal damage to all nearby enemies.",
                "procChance": 20, "damage": 25, "radius": 4
            },
            "cullingBlade": {
                "name": "Culling Blade",
                "type": "ultimate",
                "description": "Axe spots weakness and strikes, instantly killing an enemy if their health is below a threshold. Kills grant bonus speed.",
                "killThreshold": 0.30, "speedBonus": 30, "speedDuration": 5000,
                "cooldown": 55000, "manaCost": 40, "range": 3
            }
        },
        "talents": {
            "10": ["+2 Mana Regen", "+8 Strength"],
            "15": ["+40 Counter Helix Damage", "+12% Movement Speed"],
            "20": ["+100 Berserker's Call AoE", "+25 Battle Hunger DPS"],
            "25": ["+2s Berserker's Call Duration", "+150 Culling Blade Threshold"]
        }
    },
    "bloodseeker": {
        "name": "Bloodseeker",
        "title": "Strygwyr",
        "attr": "agility",
        "icon": "blood",
        "lore": "Strygwyr the Bloodseeker is a ritually sanctioned hunter, Hound of the Flayed Twins, charged with finding the blood of the Ancients.",
        "baseStats": {
            "maxHp": 100, "maxMana": 70, "hpPerLevel": 25, "manaPerLevel": 16,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "bloodRite": {
                "name": "Blood Rite",
                "type": "active",
                "description": "Bloodseeker baptizes an area in sacred blood. After a delay, enemies in the area are silenced and take damage.",
                "damage": 35, "silenceDuration": 3000, "delay": 2500, "radius": 5,
                "cooldown": 12000, "manaCost": 25, "range": 12
            },
            "bloodrage": {
                "name": "Bloodrage",
                "type": "active",
                "description": "Drives a unit into a bloodthirsty rage, increasing attack damage but causing them to take increased damage.",
                "damageAmpPercent": 25, "duration": 6000,
                "cooldown": 8000, "manaCost": 15, "range": 6
            },
            "thirst": {
                "name": "Thirst",
                "type": "passive",
                "description": "Bloodseeker senses wounded heroes, gaining movement speed and attack damage for each enemy below half health.",
                "maxBonusDamage": 20, "maxBonusSpeed": 30, "healthThreshold": 0.5
            },
            "rupture": {
                "name": "Rupture",
                "type": "ultimate",
                "description": "Causes an enemy's skin to rupture. Moving while ruptured causes damage based on distance traveled.",
                "damagePerUnit": 5, "duration": 8000,
                "cooldown": 60000, "manaCost": 45, "range": 8
            }
        },
        "talents": {
            "10": ["+25 Damage", "+8% Spell Lifesteal"],
            "15": ["+75 Blood Rite Damage", "+15% Bloodrage Attack Speed"],
            "20": ["+18% Rupture Damage", "-6s Blood Rite Cooldown"],
            "25": ["Global Thirst", "+20% Bloodrage Damage"]
        }
    },
    "crystal_maiden": {
        "name": "Crystal Maiden",
        "title": "Rylai",
        "attr": "intelligence",
        "icon": "crystal",
        "lore": "Born in a temperate realm, Rylai was always fascinated by the cold. She learned to channel her love of winter into magical power.",
        "baseStats": {
            "maxHp": 70, "maxMana": 130, "hpPerLevel": 18, "manaPerLevel": 28,
            "baseDamage": 10, "damagePerLevel": 2.2, "armor": 1, "armorPerLevel": 0.3,
            "moveSpeed": 8, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "crystalNova": {
                "name": "Crystal Nova",
                "type": "active",
                "description": "A burst of frost that damages and slows enemies in a target area.",
                "damage": 30, "slowPercent": 30, "slowDuration": 3500, "radius": 5,
                "cooldown": 10000, "manaCost": 20, "range": 12
            },
            "frostbite": {
                "name": "Frostbite",
                "type": "active",
                "description": "Encases an enemy in ice, preventing movement and dealing damage over time.",
                "damage": 40, "duration": 3000,
                "cooldown": 9000, "manaCost": 18, "range": 8
            },
            "arcaneAura": {
                "name": "Arcane Aura",
                "type": "passive",
                "description": "Provides bonus mana regeneration to all allies globally.",
                "selfManaRegen": 4, "allyManaRegen": 2
            },
            "freezingField": {
                "name": "Freezing Field",
                "type": "ultimate",
                "description": "Surrounds Crystal Maiden with random icy explosions that slow and damage enemies. Channeled.",
                "explosionDamage": 25, "slowPercent": 40, "radius": 8, "duration": 8000,
                "cooldown": 90000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+200 Health", "+100 Crystal Nova Damage"],
            "15": ["+150 Cast Range", "+1.5s Frostbite Duration"],
            "20": ["+60 Freezing Field Damage", "+1.5 Arcane Aura Mana Regen"],
            "25": ["Frostbite Immunity", "-1.5s Crystal Nova Cooldown"]
        }
    },
    "drow_ranger": {
        "name": "Drow Ranger",
        "title": "Traxex",
        "attr": "agility",
        "icon": "bow",
        "lore": "Drow Ranger's given name is Traxex—a name which means 'fearful' in Elvish, owing to her crippling shyness.",
        "baseStats": {
            "maxHp": 85, "maxMana": 70, "hpPerLevel": 21, "manaPerLevel": 15,
            "baseDamage": 18, "damagePerLevel": 3.4, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 12, "attackSpeed": 1.4
        },
        "abilities": {
            "frostArrows": {
                "name": "Frost Arrows",
                "type": "toggle",
                "description": "Adds a frost effect to attacks that slows the target.",
                "slowPercent": 25, "slowDuration": 2000, "bonusDamage": 8,
                "manaCost": 5
            },
            "gust": {
                "name": "Gust",
                "type": "active",
                "description": "Releases a wave of silence that pushes back and silences enemies.",
                "knockback": 4, "silenceDuration": 3000, "range": 10, "width": 4,
                "cooldown": 14000, "manaCost": 20
            },
            "multishot": {
                "name": "Multishot",
                "type": "active",
                "description": "Drow fires a barrage of arrows at enemies in a cone.",
                "waves": 4, "damagePercent": 80, "cooldown": 20000, "manaCost": 25
            },
            "marksmanship": {
                "name": "Marksmanship",
                "type": "ultimate",
                "description": "Drow's focus allows her attacks to sometimes pierce through enemies. Disabled when enemies are too close.",
                "procChance": 40, "bonusAgility": 30, "disableRadius": 4
            }
        },
        "talents": {
            "10": ["+50% Gust Blind", "+15 Movement Speed"],
            "15": ["+4 Multishot Waves", "+12 All Stats"],
            "20": ["50% Cooldown Reduction on Gust", "+20% Multishot Damage"],
            "25": ["0 Marksmanship Disable Range", "+25% Frost Arrows Slow"]
        }
    },
    "earthshaker": {
        "name": "Earthshaker",
        "title": "Raigor Stonehoof",
        "attr": "strength",
        "icon": "earth",
        "lore": "Like a living mountain, Earthshaker was birthed of the earth, his massive form perfectly attuned to seismic forces.",
        "baseStats": {
            "maxHp": 110, "maxMana": 90, "hpPerLevel": 26, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "fissure": {
                "name": "Fissure",
                "type": "active",
                "description": "Slams the ground creating a fissure that stuns and damages enemies in a line.",
                "damage": 35, "stunDuration": 1500, "length": 10,
                "cooldown": 15000, "manaCost": 25, "range": 10
            },
            "enchantTotem": {
                "name": "Enchant Totem",
                "type": "active",
                "description": "Empowers Earthshaker's totem, causing his next attack to deal massive damage.",
                "damageMultiplier": 3.0, "duration": 8000,
                "cooldown": 8000, "manaCost": 15
            },
            "aftershock": {
                "name": "Aftershock",
                "type": "passive",
                "description": "Causes a mini-stun and damage whenever Earthshaker casts a spell.",
                "damage": 15, "stunDuration": 800, "radius": 4
            },
            "echoSlam": {
                "name": "Echo Slam",
                "type": "ultimate",
                "description": "Shockwaves travel through the ground, damaging enemies. Additional damage for each enemy hit.",
                "baseDamage": 30, "echoDamage": 20, "radius": 7,
                "cooldown": 100000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+30 Damage", "+200 Mana"],
            "15": ["+50 Aftershock Damage", "+7 Armor"],
            "20": ["+50% Magic Resistance", "+100 Fissure Range"],
            "25": ["+400 Fissure Stun Duration", "+1.5x Enchant Totem Damage"]
        }
    },
    "invoker": {
        "name": "Invoker",
        "title": "Kael",
        "attr": "universal",
        "icon": "orb",
        "lore": "In its earliest, and some would say most potent form, magic was primarily the art of memory.",
        "baseStats": {
            "maxHp": 90, "maxMana": 150, "hpPerLevel": 23, "manaPerLevel": 30,
            "baseDamage": 12, "damagePerLevel": 2.8, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "sunStrike": {
                "name": "Sun Strike",
                "type": "active",
                "description": "Sends a beam of solar energy crashing down, dealing massive damage split among enemies in the area.",
                "damage": 100, "radius": 3, "delay": 1500,
                "cooldown": 25000, "manaCost": 35, "range": 999
            },
            "coldSnap": {
                "name": "Cold Snap",
                "type": "active",
                "description": "Causes a target to freeze, receiving mini-stuns and damage whenever they take damage.",
                "damagePerProc": 10, "stunPerProc": 400, "duration": 5000,
                "cooldown": 16000, "manaCost": 20, "range": 10
            },
            "tornado": {
                "name": "Tornado",
                "type": "active",
                "description": "Conjures a fast-moving tornado that lifts enemies into the air, disabling them.",
                "damage": 40, "liftDuration": 2000, "range": 15, "travelSpeed": 15,
                "cooldown": 20000, "manaCost": 25
            },
            "chaosDefens": {
                "name": "Deafening Blast",
                "type": "ultimate",
                "description": "Unleashes a mighty blast that knocks back, disarms, and damages all enemies.",
                "damage": 60, "knockback": 5, "disarmDuration": 3000, "radius": 8,
                "cooldown": 40000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+40 Chaos Meteor Contact Damage", "+1 Forged Spirit Armor"],
            "15": ["+1s Cold Snap Duration", "+30 Alacrity Damage"],
            "20": ["+1.5s Tornado Lift Time", "Cataclysm"],
            "25": ["+2 Forge Spirits", "Radial Deafening Blast"]
        }
    },
    "juggernaut": {
        "name": "Juggernaut",
        "title": "Yurnero",
        "attr": "agility",
        "icon": "sword",
        "lore": "No one has ever seen the face hidden beneath the mask of Yurnero the Juggernaut.",
        "baseStats": {
            "maxHp": 95, "maxMana": 75, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 12, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "bladeFury": {
                "name": "Blade Fury",
                "type": "active",
                "description": "Juggernaut spins, becoming spell immune while dealing damage to nearby enemies.",
                "damagePerSecond": 25, "duration": 4000, "radius": 4,
                "cooldown": 20000, "manaCost": 25
            },
            "healingWard": {
                "name": "Healing Ward",
                "type": "active",
                "description": "Summons a ward that heals all nearby allies based on their max HP.",
                "healPercentPerSecond": 3, "duration": 20000, "radius": 6,
                "cooldown": 45000, "manaCost": 30
            },
            "bladeDance": {
                "name": "Blade Dance",
                "type": "passive",
                "description": "Gives Juggernaut a chance to deal critical damage on each attack.",
                "critChance": 35, "critMultiplier": 1.8
            },
            "omnislash": {
                "name": "Omnislash",
                "type": "ultimate",
                "description": "Juggernaut leaps between enemies, dealing devastating slashes. Invulnerable during Omnislash.",
                "slashes": 6, "damagePerSlash": 30, "bounceRadius": 6,
                "cooldown": 100000, "manaCost": 50, "range": 6
            }
        },
        "talents": {
            "10": ["+5 All Stats", "+20 Movement Speed"],
            "15": ["+100 Blade Fury DPS", "+20 Attack Speed"],
            "20": ["+1s Blade Fury Duration", "+1 Healing Ward HP%"],
            "25": ["+5 Omnislash Slashes", "+50% Blade Dance Crit"]
        }
    },
    "lion": {
        "name": "Lion",
        "title": "Demon Witch",
        "attr": "intelligence",
        "icon": "demon",
        "lore": "Once a master sorcerer who sought dark power, Lion traded his soul to demons multiple times.",
        "baseStats": {
            "maxHp": 75, "maxMana": 120, "hpPerLevel": 19, "manaPerLevel": 26,
            "baseDamage": 11, "damagePerLevel": 2.4, "armor": 1, "armorPerLevel": 0.3,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "earthSpike": {
                "name": "Earth Spike",
                "type": "active",
                "description": "Rock spikes burst from the earth, stunning and damaging enemies in a line.",
                "damage": 35, "stunDuration": 2000, "length": 8,
                "cooldown": 10000, "manaCost": 22, "range": 8
            },
            "hex": {
                "name": "Hex",
                "type": "active",
                "description": "Transforms an enemy into a harmless frog, disabling all abilities and reducing movement speed.",
                "duration": 3000, "slowPercent": 50,
                "cooldown": 16000, "manaCost": 20, "range": 8
            },
            "manaDrain": {
                "name": "Mana Drain",
                "type": "active",
                "description": "Channels to drain mana from an enemy, slowing them. Deals damage based on mana drained.",
                "manaPerSecond": 15, "damagePercent": 0.5, "duration": 5000,
                "cooldown": 10000, "manaCost": 0, "range": 8
            },
            "fingerOfDeath": {
                "name": "Finger of Death",
                "type": "ultimate",
                "description": "Rips at an enemy with pure magical energy, dealing massive damage. Damage increases per kill.",
                "baseDamage": 100, "damagePerKill": 20, "maxStacks": 30,
                "cooldown": 60000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+75 Earth Spike Damage"],
            "15": ["+100 Cast Range", "+2 Mana Drain Multi Target"],
            "20": ["+500 Health", "-2s Earth Spike Cooldown"],
            "25": ["1000 AoE Hex", "+150 Finger of Death Damage"]
        }
    },
    "phantom_assassin": {
        "name": "Phantom Assassin",
        "title": "Mortred",
        "attr": "agility",
        "icon": "dagger",
        "lore": "Through a pact made with the Veiled Oracle, Mortred became the Phantom Assassin, an unstoppable contract killer.",
        "baseStats": {
            "maxHp": 90, "maxMana": 65, "hpPerLevel": 23, "manaPerLevel": 14,
            "baseDamage": 18, "damagePerLevel": 3.4, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 12, "attackRange": 2.5, "attackSpeed": 1.4
        },
        "abilities": {
            "stiflingDagger": {
                "name": "Stifling Dagger",
                "type": "active",
                "description": "Throws a dagger that slows and deals attack-based damage to the target.",
                "damagePercent": 60, "slowPercent": 30, "slowDuration": 3000,
                "cooldown": 6000, "manaCost": 15, "range": 12
            },
            "phantomStrike": {
                "name": "Phantom Strike",
                "type": "active",
                "description": "Teleports to a target and gains bonus attack speed for several attacks.",
                "bonusAttackSpeed": 100, "attackCount": 4,
                "cooldown": 8000, "manaCost": 20, "range": 10
            },
            "blur": {
                "name": "Blur",
                "type": "passive",
                "description": "Gives PA a chance to evade attacks. Can activate to become invisible briefly.",
                "evasionPercent": 35, "invisDuration": 2500, "invisCooldown": 30000
            },
            "coupDeGrace": {
                "name": "Coup de Grace",
                "type": "ultimate",
                "description": "PA refines her assassination technique, gaining a chance to deal devastating critical strikes.",
                "critChance": 20, "critMultiplier": 4.5
            }
        },
        "talents": {
            "10": ["+15% Lifesteal", "+150 Phantom Strike Cast Range"],
            "15": ["+25% Evasion", "-3 Armor Corruption"],
            "20": ["+350 Stifling Dagger Range", "Triple Strike Stifling Dagger"],
            "25": ["+6% Coup de Grace Chance", "Double Strike"]
        }
    },
    "pudge": {
        "name": "Pudge",
        "title": "Butcher",
        "attr": "strength",
        "icon": "hook",
        "lore": "The Butcher haunts the shadows, his terrible meat hook searching for victims to drag to their doom.",
        "baseStats": {
            "maxHp": 140, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 19, "damagePerLevel": 3.3, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 9, "attackRange": 2.5, "attackSpeed": 0.9
        },
        "abilities": {
            "meatHook": {
                "name": "Meat Hook",
                "type": "active",
                "description": "Launches a hook that drags the first unit it hits back to Pudge, dealing damage.",
                "damage": 40, "hookRange": 15,
                "cooldown": 12000, "manaCost": 25
            },
            "rot": {
                "name": "Rot",
                "type": "toggle",
                "description": "Deals damage per second to nearby enemies and slows them, but also damages Pudge.",
                "damagePerSecond": 15, "selfDamagePerSecond": 8, "slowPercent": 25, "radius": 4
            },
            "fleshHeap": {
                "name": "Flesh Heap",
                "type": "passive",
                "description": "Grants magic resistance and strength for each nearby hero death.",
                "magicResist": 10, "strPerStack": 2
            },
            "dismember": {
                "name": "Dismember",
                "type": "ultimate",
                "description": "Pudge chews on an enemy for several seconds, dealing massive damage and healing himself.",
                "damagePerSecond": 40, "healPercent": 100, "duration": 3000,
                "cooldown": 25000, "manaCost": 40, "range": 2.5
            }
        },
        "talents": {
            "10": ["+25 Rot Damage", "+1.5 Mana Regen"],
            "15": ["+12% Rot Slow", "+100 Meat Hook Damage"],
            "20": ["+3s Dismember Duration", "+1.5 Flesh Heap Stack Strength"],
            "25": ["+7 Meat Hook Range", "Dismember Heals Allies"]
        }
    },
    "shadow_fiend": {
        "name": "Shadow Fiend",
        "title": "Nevermore",
        "attr": "agility",
        "icon": "shadow",
        "lore": "It is said that Nevermore the Shadow Fiend has the soul of a poet, but in truth, he has thousands of souls.",
        "baseStats": {
            "maxHp": 80, "maxMana": 85, "hpPerLevel": 20, "manaPerLevel": 18,
            "baseDamage": 8, "damagePerLevel": 3.6, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.2
        },
        "abilities": {
            "shadowraze": {
                "name": "Shadowraze",
                "type": "active",
                "description": "Shadow Fiend razes the ground at three distances, dealing damage and stacking debuffs.",
                "damage": 30, "stackDamage": 10, "maxStacks": 3, "razeDistances": [3, 6, 9],
                "cooldown": 6000, "manaCost": 15
            },
            "necromastery": {
                "name": "Necromastery",
                "type": "passive",
                "description": "Shadow Fiend steals the souls of enemies he kills, gaining bonus damage per soul.",
                "damagePerSoul": 2, "maxSouls": 25, "soulLossOnDeath": 0.5
            },
            "presenceOfDarkLord": {
                "name": "Presence of the Dark Lord",
                "type": "passive",
                "description": "Shadow Fiend's presence reduces the armor of nearby enemies.",
                "armorReduction": 5, "radius": 6
            },
            "requiem": {
                "name": "Requiem of Souls",
                "type": "ultimate",
                "description": "Captured souls explode outward, dealing damage and fearing enemies. More souls = more lines.",
                "damagePerLine": 25, "fearDuration": 2000, "radius": 10,
                "cooldown": 100000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Attack Speed", "+15 Movement Speed"],
            "15": ["+35 Damage", "-2 Presence of the Dark Lord Armor"],
            "20": ["+25% Evasion", "+2 Shadowraze Damage per Stack"],
            "25": ["Requiem Fear per Line", "+100 Shadowraze Damage"]
        }
    },
    "sniper": {
        "name": "Sniper",
        "title": "Kardel Sharpeye",
        "attr": "agility",
        "icon": "rifle",
        "lore": "Kardel Sharpeye was born deep in the mountains, where his people had built their empire on a mastery of gunpowder.",
        "baseStats": {
            "maxHp": 75, "maxMana": 70, "hpPerLevel": 18, "manaPerLevel": 15,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 14, "attackSpeed": 1.2
        },
        "abilities": {
            "shrapnel": {
                "name": "Shrapnel",
                "type": "active",
                "description": "Fires shrapnel at an area, dealing damage over time and slowing enemies.",
                "damagePerSecond": 12, "slowPercent": 25, "duration": 6000, "radius": 5,
                "charges": 3, "chargeRestoreTime": 20000, "manaCost": 20, "range": 18
            },
            "headshot": {
                "name": "Headshot",
                "type": "passive",
                "description": "Sniper's attacks have a chance to deal bonus damage and briefly slow.",
                "procChance": 40, "bonusDamage": 15, "slowDuration": 500
            },
            "takeAim": {
                "name": "Take Aim",
                "type": "passive",
                "description": "Extends Sniper's attack range. Can be activated for temporary additional range.",
                "bonusRange": 3, "activeBonusRange": 4, "activeDuration": 5000,
                "activeCooldown": 15000
            },
            "assassinate": {
                "name": "Assassinate",
                "type": "ultimate",
                "description": "Takes aim at a target and fires a devastating shot after a short delay.",
                "damage": 100, "aimTime": 2000, "range": 25,
                "cooldown": 15000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+25 Shrapnel DPS", "+20 Attack Speed"],
            "15": ["+30 Headshot Damage", "+30 Knockback Distance"],
            "20": ["+100 Attack Range", "+30% Shrapnel Slow"],
            "25": ["Headshot Applies Current Level of Shrapnel", "-1.5s Assassinate Cast Time"]
        }
    },
    "tidehunter": {
        "name": "Tidehunter",
        "title": "Leviathan",
        "attr": "strength",
        "icon": "anchor",
        "lore": "The Tidehunter known as Leviathan was once a major player in the politics of the Sunken Isles.",
        "baseStats": {
            "maxHp": 150, "maxMana": 80, "hpPerLevel": 32, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 0.9
        },
        "abilities": {
            "gush": {
                "name": "Gush",
                "type": "active",
                "description": "Sprays a wave of water that damages and slows an enemy while reducing their armor.",
                "damage": 25, "slowPercent": 35, "armorReduction": 5, "duration": 4000,
                "cooldown": 10000, "manaCost": 20, "range": 8
            },
            "krakenshell": {
                "name": "Kraken Shell",
                "type": "passive",
                "description": "Thickens Tidehunter's skin, reducing damage and removing debuffs after taking enough damage.",
                "damageBlock": 8, "purgeThreshold": 50
            },
            "anchorSmash": {
                "name": "Anchor Smash",
                "type": "active",
                "description": "Tidehunter swings his anchor, damaging nearby enemies and reducing their attack damage.",
                "damage": 30, "attackReduction": 35, "duration": 5000, "radius": 4,
                "cooldown": 6000, "manaCost": 15
            },
            "ravage": {
                "name": "Ravage",
                "type": "ultimate",
                "description": "Slams the ground, sending tentacles that stun and damage all enemies in a huge radius.",
                "damage": 50, "stunDuration": 2500, "radius": 10,
                "cooldown": 120000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+100 Gush Damage"],
            "15": ["+40% XP Gain", "-25% Anchor Smash Damage Reduction"],
            "20": ["+15 Kraken Shell Damage Block", "+25% Anchor Smash Damage"],
            "25": ["+1s Ravage Stun Duration", "Gush Hits in Area"]
        }
    },
    "wraith_king": {
        "name": "Wraith King",
        "title": "Ostarion",
        "attr": "strength",
        "icon": "crown",
        "lore": "For untold years, King Ostarion built his empire by battering his enemies with his massive mace.",
        "baseStats": {
            "maxHp": 130, "maxMana": 60, "hpPerLevel": 30, "manaPerLevel": 14,
            "baseDamage": 20, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "wraithfireBlast": {
                "name": "Wraithfire Blast",
                "type": "active",
                "description": "Hurls a spectral blast that stuns, then slows and damages the target over time.",
                "damage": 30, "stunDuration": 2000, "dotDamage": 20, "slowPercent": 30, "dotDuration": 3000,
                "cooldown": 10000, "manaCost": 25, "range": 8
            },
            "vampiricSpirit": {
                "name": "Vampiric Spirit",
                "type": "passive",
                "description": "Wraith King and nearby allies gain lifesteal. Summons skeletons on kills.",
                "lifestealPercent": 15, "skeletonsPerKill": 2, "maxSkeletons": 8
            },
            "mortalStrike": {
                "name": "Mortal Strike",
                "type": "passive",
                "description": "Wraith King has a chance to deal critical damage with each attack.",
                "critChance": 15, "critMultiplier": 2.5
            },
            "reincarnation": {
                "name": "Reincarnation",
                "type": "ultimate",
                "description": "Wraith King returns to life with full HP after dying, slowing nearby enemies.",
                "slowPercent": 50, "slowDuration": 5000, "slowRadius": 8,
                "cooldown": 180000, "manaCost": 80
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+15 Skeleton Damage"],
            "15": ["+25 Attack Speed", "+15% Vampiric Spirit Lifesteal"],
            "20": ["+10 Skeleton HP", "-25s Reincarnation Cooldown"],
            "25": ["Reincarnation Resurrects Allied Heroes", "+3 Skeleton Charges"]
        }
    },
    "zeus": {
        "name": "Zeus",
        "title": "Lord of Olympus",
        "attr": "intelligence",
        "icon": "lightning",
        "lore": "Lord of Heaven, father of gods, Zeus treats all the Heroes as if they were his rambunctious, rebellious children.",
        "baseStats": {
            "maxHp": 80, "maxMana": 140, "hpPerLevel": 20, "manaPerLevel": 30,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 1, "armorPerLevel": 0.3,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "arcLightning": {
                "name": "Arc Lightning",
                "type": "active",
                "description": "Hurls a bolt of lightning that bounces between enemies.",
                "damage": 20, "bounces": 8, "bounceDamageReduction": 0.15,
                "cooldown": 2500, "manaCost": 12, "range": 10
            },
            "lightningBolt": {
                "name": "Lightning Bolt",
                "type": "active",
                "description": "Calls down a bolt of lightning to strike a target, stunning briefly and revealing them.",
                "damage": 50, "ministun": 200, "trueVision": 6000,
                "cooldown": 6000, "manaCost": 25, "range": 12
            },
            "staticField": {
                "name": "Static Field",
                "type": "passive",
                "description": "Zeus's spells shock nearby enemies, dealing damage based on their current HP.",
                "currentHpPercent": 5, "radius": 6
            },
            "thundergodsWrath": {
                "name": "Thundergod's Wrath",
                "type": "ultimate",
                "description": "Strikes all enemy heroes with bolts from the sky, dealing damage and revealing them.",
                "damage": 80, "trueVision": 5000,
                "cooldown": 90000, "manaCost": 60, "range": 999
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+25 Arc Lightning Damage"],
            "15": ["+350 Health", "+100 Lightning Bolt Damage"],
            "20": ["+75 Thundergod's Wrath Damage", "+0.5s Lightning Bolt Ministun"],
            "25": ["+2.5% Static Field Damage", "Thundergod's Wrath Applies Debuff"]
        }
    },
    "arc_warden": {
        "name": "Arc Warden",
        "title": "Zet",
        "attr": "agility",
        "icon": "spark",
        "lore": "Before the battle of the Primordials, before the light of the world, before the First Day, there was Zet, the Self-Aware Fragment.",
        "baseStats": {
            "maxHp": 85, "maxMana": 100, "hpPerLevel": 22, "manaPerLevel": 22,
            "baseDamage": 15, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "flux": {
                "name": "Flux",
                "type": "active",
                "description": "Engulfs an enemy in a swirling, slowing field that deals damage over time. Effect is stronger when the enemy is alone.",
                "damage": 20, "damagePerSecond": 12, "slowPercent": 35, "duration": 6000,
                "cooldown": 14000, "manaCost": 25, "range": 10
            },
            "magneticField": {
                "name": "Magnetic Field",
                "type": "active",
                "description": "Creates a circular distortion field that grants evasion and attack speed to allies inside.",
                "evasionPercent": 60, "attackSpeedBonus": 60, "duration": 5000, "radius": 4,
                "cooldown": 18000, "manaCost": 30, "range": 10
            },
            "sparkWraith": {
                "name": "Spark Wraith",
                "type": "active",
                "description": "Summons a ghost-like spark that slowly materializes and seeks out enemies to damage and slow them.",
                "damage": 35, "slowPercent": 20, "activationDelay": 2000, "duration": 45000,
                "cooldown": 4000, "manaCost": 15, "range": 12
            },
            "tempestDouble": {
                "name": "Tempest Double",
                "type": "ultimate",
                "description": "Creates a perfect duplicate of Arc Warden that can use all of his abilities and items.",
                "doubleDuration": 20000, "cooldown": 50000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+175 Flux Cast Range", "+30 Attack Speed"],
            "15": ["+100 Spark Wraith Damage", "-1.5s Spark Wraith Cooldown"],
            "20": ["+30% Lifesteal", "+8s Tempest Double Duration"],
            "25": ["30% Cooldown Reduction", "+250 Magnetic Field AoE"]
        }
    },
    "bane": {
        "name": "Bane",
        "title": "Atropos",
        "attr": "universal",
        "icon": "nightmare",
        "lore": "When the gods have nightmares, it is Bane Elemental who brings them. From the Plane of Dreams, he serves Nyctasha.",
        "baseStats": {
            "maxHp": 100, "maxMana": 110, "hpPerLevel": 24, "manaPerLevel": 24,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "enfeeble": {
                "name": "Enfeeble",
                "type": "active",
                "description": "Weakens an enemy, reducing their status resistance and magic resistance.",
                "statusResistReduction": 30, "magicResistReduction": 25, "duration": 8000,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "brainSap": {
                "name": "Brain Sap",
                "type": "active",
                "description": "Feasts on the target's brain, dealing damage and healing Bane for the same amount.",
                "damage": 40, "heal": 40, "cooldown": 10000, "manaCost": 25, "range": 8
            },
            "nightmare": {
                "name": "Nightmare",
                "type": "active",
                "description": "Puts a target to sleep, making them invulnerable but unable to act. Damage wakes them.",
                "duration": 4000, "damagePerSecond": 10, "invulnDuration": 1000,
                "cooldown": 16000, "manaCost": 20, "range": 8
            },
            "fiendGrip": {
                "name": "Fiend's Grip",
                "type": "ultimate",
                "description": "Grips an enemy with nightmarish force, stunning and draining their mana while dealing damage.",
                "damagePerSecond": 50, "manaDrainPercent": 5, "duration": 5000,
                "cooldown": 80000, "manaCost": 50, "range": 6
            }
        },
        "talents": {
            "10": ["+7 Armor", "+100 Brain Sap Damage/Heal"],
            "15": ["-2s Brain Sap Cooldown", "+30 Movement Speed"],
            "20": ["+100 Enfeeble Damage Reduction", "+6% Fiend's Grip Max Mana Drain"],
            "25": ["Brain Sap Creates Nightmare Illusion", "+1.5s Fiend's Grip Duration"]
        }
    },
    "batrider": {
        "name": "Batrider",
        "title": "Jin'zakk",
        "attr": "universal",
        "icon": "bat",
        "lore": "There is no such thing as a fair fight. Jin'zakk, the Batrider, will tell you that while setting your tower on fire.",
        "baseStats": {
            "maxHp": 95, "maxMana": 90, "hpPerLevel": 24, "manaPerLevel": 20,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "stickyNapalm": {
                "name": "Sticky Napalm",
                "type": "active",
                "description": "Covers enemies with napalm that amplifies damage from Batrider's attacks and slows them.",
                "bonusDamage": 8, "slowPercent": 3, "maxStacks": 10, "duration": 8000,
                "cooldown": 3000, "manaCost": 10, "range": 10, "radius": 4
            },
            "flamebreak": {
                "name": "Flamebreak",
                "type": "active",
                "description": "Hurls an explosive that knocks back enemies and deals damage over time.",
                "damage": 35, "dotDamage": 20, "knockback": 3, "dotDuration": 3000,
                "cooldown": 14000, "manaCost": 25, "range": 12
            },
            "firefly": {
                "name": "Firefly",
                "type": "active",
                "description": "Batrider takes to the skies, flying over terrain and leaving a trail of fire that damages enemies.",
                "damagePerSecond": 15, "trailDuration": 2000, "duration": 12000,
                "cooldown": 34000, "manaCost": 30
            },
            "flamingLasso": {
                "name": "Flaming Lasso",
                "type": "ultimate",
                "description": "Lassoes an enemy and drags them behind Batrider. The victim is stunned for the duration.",
                "damage": 30, "duration": 3000, "cooldown": 70000, "manaCost": 50, "range": 3
            }
        },
        "talents": {
            "10": ["+5 Sticky Napalm Damage", "+25 Movement Speed"],
            "15": ["+4s Firefly Duration", "+2 Sticky Napalm Max Stacks"],
            "20": ["+150 Flamebreak Knockback", "+15% Firefly Movement Speed"],
            "25": ["0 Turn Rate in Firefly", "+150 Lasso Cast Range"]
        }
    },
    "beastmaster": {
        "name": "Beastmaster",
        "title": "Karroch",
        "attr": "universal",
        "icon": "boar",
        "lore": "Karroch was born a child of the stocks. Raised among the wild creatures of the forest, he learned their ways.",
        "baseStats": {
            "maxHp": 120, "maxMana": 80, "hpPerLevel": 28, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "wildAxes": {
                "name": "Wild Axes",
                "type": "active",
                "description": "Throws axes that travel outward then return. Enemies hit take damage and attack more slowly.",
                "damage": 35, "attackSlowPercent": 25, "slowDuration": 3000, "range": 12,
                "cooldown": 10000, "manaCost": 20
            },
            "callOfTheWild": {
                "name": "Call of the Wild",
                "type": "active",
                "description": "Summons a loyal boar and hawk to fight alongside Beastmaster.",
                "boarDamage": 15, "boarSlow": 15, "hawkVision": 10, "duration": 40000,
                "cooldown": 30000, "manaCost": 25
            },
            "innerBeast": {
                "name": "Inner Beast",
                "type": "passive",
                "description": "Unleashes the inner beast of allies, increasing their attack speed.",
                "attackSpeedBonus": 30, "radius": 10
            },
            "primalRoar": {
                "name": "Primal Roar",
                "type": "ultimate",
                "description": "Releases a powerful roar that stuns the target and pushes aside all enemies in its path.",
                "damage": 50, "stunDuration": 3500, "pushDamage": 25, "pushStun": 1000,
                "cooldown": 70000, "manaCost": 50, "range": 8
            }
        },
        "talents": {
            "10": ["+25 Boar Damage", "+20 Movement Speed"],
            "15": ["+100 Wild Axes Damage", "+400 Hawk HP"],
            "20": ["+100 Inner Beast Attack Speed", "-30s Call of the Wild Cooldown"],
            "25": ["+2 Boar/Hawk per Summon", "+1.5s Primal Roar Stun Duration"]
        }
    },
    "bounty_hunter": {
        "name": "Bounty Hunter",
        "title": "Gondar",
        "attr": "agility",
        "icon": "gold",
        "lore": "When the first sun rose, a clan of assassins watched its light chase away the night.",
        "baseStats": {
            "maxHp": 90, "maxMana": 70, "hpPerLevel": 22, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 12, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "shurikenToss": {
                "name": "Shuriken Toss",
                "type": "active",
                "description": "Hurls a shuriken at an enemy, damaging and mini-stunning them. Bounces to Tracked targets.",
                "damage": 40, "ministun": 400, "bounceRadius": 10,
                "cooldown": 8000, "manaCost": 20, "range": 10
            },
            "jinada": {
                "name": "Jinada",
                "type": "passive",
                "description": "Bounty Hunter's attacks periodically deal critical damage and steal gold from the target.",
                "critMultiplier": 1.8, "goldSteal": 20, "cooldown": 6000
            },
            "shadowWalk": {
                "name": "Shadow Walk",
                "type": "active",
                "description": "Bounty Hunter becomes invisible and moves faster. His next attack breaks invisibility with bonus damage.",
                "bonusDamage": 40, "moveSpeedBonus": 25, "duration": 25000, "fadeDuration": 1000,
                "cooldown": 15000, "manaCost": 15
            },
            "track": {
                "name": "Track",
                "type": "ultimate",
                "description": "Tracks an enemy hero, granting true sight and bonus gold when the target dies.",
                "bonusGold": 150, "allyGold": 75, "duration": 25000, "moveSpeedBonus": 20,
                "cooldown": 6000, "manaCost": 20, "range": 12
            }
        },
        "talents": {
            "10": ["+25 Jinada Gold Steal", "+25 Damage"],
            "15": ["+50% Jinada Critical Strike", "+30 Track Movement Speed"],
            "20": ["+100 Shuriken Toss Damage", "-30% Track Armor Corruption"],
            "25": ["No Cooldown on Jinada", "+300 Track Gold"]
        }
    },
    "brewmaster": {
        "name": "Brewmaster",
        "title": "Mangix",
        "attr": "universal",
        "icon": "brew",
        "lore": "Deep in the Wailing Mountains lived a monk master of the brewing arts. Mangix was his finest disciple.",
        "baseStats": {
            "maxHp": 130, "maxMana": 90, "hpPerLevel": 30, "manaPerLevel": 20,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "thunderClap": {
                "name": "Thunder Clap",
                "type": "active",
                "description": "Slams the ground, dealing damage and slowing enemies in an area.",
                "damage": 40, "slowPercent": 35, "attackSlowPercent": 35, "duration": 4000, "radius": 5,
                "cooldown": 12000, "manaCost": 25
            },
            "cinderBrew": {
                "name": "Cinder Brew",
                "type": "active",
                "description": "Drenches enemies in alcohol, slowing them and causing fire to ignite them for bonus damage.",
                "slowPercent": 25, "igniteDamage": 40, "duration": 5000, "radius": 5,
                "cooldown": 16000, "manaCost": 20, "range": 10
            },
            "drunkenBrawler": {
                "name": "Drunken Brawler",
                "type": "passive",
                "description": "Grants a chance to dodge attacks or deal critical damage. Cycles between offense and defense.",
                "dodgeChance": 70, "critChance": 80, "critMultiplier": 2.0, "cycleDuration": 3000
            },
            "primalSplit": {
                "name": "Primal Split",
                "type": "ultimate",
                "description": "Splits into three elemental warriors - Earth, Storm, and Fire - each with unique abilities.",
                "duration": 16000, "earthHP": 200, "stormHP": 120, "fireHP": 150,
                "cooldown": 120000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+200 Health", "+1.5 Mana Regen"],
            "15": ["+20% Magic Resistance", "+80 Thunder Clap Damage"],
            "20": ["+100 Attack Speed", "-40s Primal Split Cooldown"],
            "25": ["+100% Drunken Brawler Crit/Evasion", "+2 Primal Split Brewlings"]
        }
    },
    "bristleback": {
        "name": "Bristleback",
        "title": "Rigwarl",
        "attr": "strength",
        "icon": "quill",
        "lore": "Never one to turn tail in a fight, Rigwarl was known for blunt sarcasm and his legendary spine-covered back.",
        "baseStats": {
            "maxHp": 140, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "viscousNasalGoo": {
                "name": "Viscous Nasal Goo",
                "type": "active",
                "description": "Covers an enemy in goo, slowing them and reducing their armor. Stacks multiple times.",
                "armorReduction": 2, "slowPercent": 10, "maxStacks": 6, "duration": 5000,
                "cooldown": 1500, "manaCost": 10, "range": 8
            },
            "quillSpray": {
                "name": "Quill Spray",
                "type": "active",
                "description": "Sprays quills around Bristleback. Consecutive hits deal stacking damage.",
                "baseDamage": 15, "stackDamage": 10, "stackDuration": 10000, "radius": 5,
                "cooldown": 3000, "manaCost": 12
            },
            "bristleback": {
                "name": "Bristleback",
                "type": "passive",
                "description": "Takes reduced damage from behind and sides. Releases quill spray when enough damage is taken.",
                "backDamageReduction": 40, "sideDamageReduction": 20, "quillThreshold": 50
            },
            "warpath": {
                "name": "Warpath",
                "type": "ultimate",
                "description": "Each time Bristleback casts a spell, he gains bonus movement speed and damage.",
                "damagePerStack": 15, "moveSpeedPerStack": 4, "maxStacks": 10, "stackDuration": 10000
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+2 Mana Regen"],
            "15": ["+25 Quill Stack Damage", "+250 Health"],
            "20": ["+20 Warpath Damage per Stack", "+25% Goo Slow"],
            "25": ["+15% Bristleback Damage Reduction", "Quill Spray Applies Nasal Goo"]
        }
    },
    "broodmother": {
        "name": "Broodmother",
        "title": "Black Arachnia",
        "attr": "universal",
        "icon": "spider",
        "lore": "For thousands of years, Black Arachnia the Broodmother has dwelt in her silken palace among the ruins.",
        "baseStats": {
            "maxHp": 90, "maxMana": 80, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "insatiableHunger": {
                "name": "Insatiable Hunger",
                "type": "active",
                "description": "Broodmother enters a ravenous state, gaining bonus damage and lifesteal.",
                "bonusDamage": 60, "lifestealPercent": 50, "duration": 8000,
                "cooldown": 25000, "manaCost": 30
            },
            "silkenBola": {
                "name": "Silken Bola",
                "type": "active",
                "description": "Throws bolas at enemies, rooting and dealing damage over time.",
                "damage": 30, "rootDuration": 2000, "dotDamage": 20, "dotDuration": 4000,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "spinWeb": {
                "name": "Spin Web",
                "type": "active",
                "description": "Spins a web that grants invisibility, movement speed, and regeneration to Broodmother.",
                "moveSpeedBonus": 60, "hpRegen": 8, "radius": 8, "maxWebs": 8,
                "cooldown": 0, "manaCost": 10
            },
            "spawnSpiderlings": {
                "name": "Spawn Spiderlings",
                "type": "ultimate",
                "description": "Spits venom at a target. If the target dies while debuffed, spiderlings spawn.",
                "damage": 50, "spiderlingsOnKill": 4, "spiderlingDamage": 12, "duration": 6000,
                "cooldown": 8000, "manaCost": 25, "range": 10
            }
        },
        "talents": {
            "10": ["+100 Spawn Spiderlings Damage", "+10 Spiderling Damage"],
            "15": ["+25 Insatiable Hunger Damage", "+300 Health"],
            "20": ["+40 Attack Speed", "+20% Insatiable Hunger Lifesteal"],
            "25": ["+60% Magic Resistance for Spiderlings", "+500 Spiderling HP"]
        }
    },
    "centaur_warrunner": {
        "name": "Centaur Warrunner",
        "title": "Bradwarden",
        "attr": "strength",
        "icon": "horse",
        "lore": "It's said that a centaur's strength comes from the fury of the sun. Bradwarden proved this with every charge.",
        "baseStats": {
            "maxHp": 160, "maxMana": 70, "hpPerLevel": 35, "manaPerLevel": 15,
            "baseDamage": 19, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 0.9
        },
        "abilities": {
            "hoofstomp": {
                "name": "Hoof Stomp",
                "type": "active",
                "description": "Slams the ground, stunning and damaging nearby enemies.",
                "damage": 40, "stunDuration": 2000, "radius": 4,
                "cooldown": 13000, "manaCost": 25
            },
            "doubleEdge": {
                "name": "Double Edge",
                "type": "active",
                "description": "Centaur strikes a mighty blow, damaging both himself and the enemy.",
                "damage": 80, "selfDamagePercent": 30, "cooldown": 6000, "manaCost": 0, "range": 2.5
            },
            "retaliate": {
                "name": "Retaliate",
                "type": "passive",
                "description": "Centaur's skin returns damage to attackers based on his strength.",
                "returnDamage": 20, "strMultiplier": 0.5
            },
            "stampede": {
                "name": "Stampede",
                "type": "ultimate",
                "description": "All allied heroes gain maximum movement speed and trample enemies for damage based on Centaur's strength.",
                "strDamageMultiplier": 2.0, "duration": 4000, "slowPercent": 50, "slowDuration": 2000,
                "cooldown": 90000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+30 Movement Speed", "+10 Retaliate Damage"],
            "15": ["+300 Double Edge Damage", "+40 Damage"],
            "20": ["+1s Hoof Stomp Stun Duration", "+20% Stampede Slow"],
            "25": ["Gains Retaliate Aura", "+1.5s Stampede Duration"]
        }
    },
    "chaos_knight": {
        "name": "Chaos Knight",
        "title": "Nessaj",
        "attr": "strength",
        "icon": "chaos",
        "lore": "The oldest Fundamental, Chaos Knight rides forth to bring the ultimate discord across all planes of existence.",
        "baseStats": {
            "maxHp": 130, "maxMana": 60, "hpPerLevel": 30, "manaPerLevel": 14,
            "baseDamage": 22, "damagePerLevel": 3.6, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "chaosBolt": {
                "name": "Chaos Bolt",
                "type": "active",
                "description": "Throws a bolt of chaotic energy, dealing random damage and stunning for a random duration.",
                "minDamage": 30, "maxDamage": 60, "minStun": 1000, "maxStun": 3000,
                "cooldown": 10000, "manaCost": 25, "range": 8
            },
            "realityRift": {
                "name": "Reality Rift",
                "type": "active",
                "description": "Teleports Chaos Knight and his illusions to a target, reducing their armor.",
                "armorReduction": 5, "armorDuration": 6000, "bonusDamage": 30,
                "cooldown": 8000, "manaCost": 20, "range": 8
            },
            "chaosStrike": {
                "name": "Chaos Strike",
                "type": "passive",
                "description": "Each attack has a chance to deal critical damage and steal HP from the target.",
                "critChance": 33, "critMultiplier": 2.0, "lifestealPercent": 40
            },
            "phantasm": {
                "name": "Phantasm",
                "type": "ultimate",
                "description": "Creates illusions of Chaos Knight that deal significant damage.",
                "illusionCount": 3, "illusionDamage": 100, "illusionTaken": 260, "duration": 30000,
                "cooldown": 120000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+1s Chaos Bolt Duration"],
            "15": ["+150 Reality Rift Pull Distance", "+15 Strength"],
            "20": ["+1 Phantasm Illusion", "+10% Chaos Strike Lifesteal"],
            "25": ["Reality Rift Pierces Spell Immune", "-3 Reality Rift Armor Reduction"]
        }
    },
    "chen": {
        "name": "Chen",
        "title": "Holy Knight",
        "attr": "universal",
        "icon": "cross",
        "lore": "Born in the desert of Hazhadal Baab, Chen was called the Holy Knight for bringing warriors of the wild into the faith.",
        "baseStats": {
            "maxHp": 95, "maxMana": 110, "hpPerLevel": 24, "manaPerLevel": 24,
            "baseDamage": 12, "damagePerLevel": 2.4, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "penitence": {
                "name": "Penitence",
                "type": "active",
                "description": "Forces an enemy to feel remorse, slowing them and causing them to take more damage.",
                "slowPercent": 30, "damageAmpPercent": 25, "duration": 6000,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "holyPersuasion": {
                "name": "Holy Persuasion",
                "type": "active",
                "description": "Converts enemy creeps to fight for Chen, gaining their abilities.",
                "maxCreeps": 4, "bonusHP": 100, "bonusMoveSpeed": 10,
                "cooldown": 30000, "manaCost": 30, "range": 8
            },
            "divineFavor": {
                "name": "Divine Favor",
                "type": "passive",
                "description": "Chen and his converted creeps gain bonus HP regeneration and attack speed.",
                "hpRegen": 4, "attackSpeedBonus": 15
            },
            "handOfGod": {
                "name": "Hand of God",
                "type": "ultimate",
                "description": "Heals all allied heroes and controlled units globally.",
                "healAmount": 200, "cooldown": 120000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+30 Movement Speed", "+200 Holy Persuasion Minimum HP"],
            "15": ["+150 Hand of God Heal", "-25s Holy Persuasion Cooldown"],
            "20": ["+1 Max Holy Persuasion Creeps", "+40% XP Gain"],
            "25": ["Hand of God Grants 75% Magic Resistance", "+1200 Holy Persuasion HP Bonus"]
        }
    },
    "clinkz": {
        "name": "Clinkz",
        "title": "Bone Fletcher",
        "attr": "agility",
        "icon": "skeleton",
        "lore": "At the crossing of Bleeding Hills, a demon and a great wizard battled. Clinkz, an archer, slew the demon but was cursed to burn eternally.",
        "baseStats": {
            "maxHp": 80, "maxMana": 75, "hpPerLevel": 20, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.4, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 13, "attackRange": 10, "attackSpeed": 1.5
        },
        "abilities": {
            "strafeFire": {
                "name": "Strafe",
                "type": "active",
                "description": "Clinkz gains a rapid burst of attack speed and attack damage for a short duration.",
                "attackSpeedBonus": 200, "bonusDamage": 30, "duration": 4000,
                "cooldown": 20000, "manaCost": 25
            },
            "searingArrows": {
                "name": "Searing Arrows",
                "type": "toggle",
                "description": "Imbues arrows with fire, dealing bonus damage to targets.",
                "bonusDamage": 40, "manaCost": 8
            },
            "deathPact": {
                "name": "Death Pact",
                "type": "active",
                "description": "Clinkz consumes a target creep, gaining bonus HP and damage based on its health.",
                "hpPercent": 80, "damagePercent": 8, "duration": 35000,
                "cooldown": 60000, "manaCost": 20, "range": 4
            },
            "burningBarrage": {
                "name": "Burning Barrage",
                "type": "ultimate",
                "description": "Channels to fire a volley of arrows in a direction, dealing attack damage plus bonus.",
                "waves": 6, "bonusDamagePerWave": 20, "range": 12,
                "cooldown": 25000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+15 Searing Arrows Damage"],
            "15": ["+30 Attack Speed", "+100 Burning Barrage Range"],
            "20": ["+100% Strafe Attack Speed", "+20 Health Regen"],
            "25": ["Searing Arrows Multishot", "+2 Burning Barrage Waves"]
        }
    },
    "clockwerk": {
        "name": "Clockwerk",
        "title": "Rattletrap",
        "attr": "universal",
        "icon": "gear",
        "lore": "Rattletrap descends from a line of inventors. His clockwork exosuit bristles with traps, rockets, and blades.",
        "baseStats": {
            "maxHp": 120, "maxMana": 80, "hpPerLevel": 28, "manaPerLevel": 18,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "batterAssault": {
                "name": "Battery Assault",
                "type": "active",
                "description": "Releases mini-shrapnel at nearby enemies, dealing damage and mini-stunning them.",
                "damagePerShrapnel": 15, "interval": 500, "duration": 6000, "radius": 4,
                "cooldown": 18000, "manaCost": 25
            },
            "powerCogs": {
                "name": "Power Cogs",
                "type": "active",
                "description": "Creates a ring of cogs around Clockwerk that knock back and drain mana from enemies.",
                "manaDrain": 50, "damage": 30, "duration": 8000,
                "cooldown": 16000, "manaCost": 20
            },
            "rocketFlare": {
                "name": "Rocket Flare",
                "type": "active",
                "description": "Fires a global-range rocket that reveals the targeted area and damages enemies.",
                "damage": 35, "visionDuration": 6000, "radius": 5,
                "cooldown": 14000, "manaCost": 15, "range": 999
            },
            "hookshot": {
                "name": "Hookshot",
                "type": "ultimate",
                "description": "Fires a grappling hook that latches to the first enemy hero, pulling Clockwerk and stunning them.",
                "damage": 50, "stunDuration": 2000, "range": 20,
                "cooldown": 40000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+2 Battery Assault Attacks", "+5 Armor"],
            "15": ["+100 Rocket Flare Damage", "+125 Power Cogs Mana Drain"],
            "20": ["+150 Hookshot Damage", "+12 Battery Assault Damage"],
            "25": ["-0.15s Battery Assault Interval", "+1200 Hookshot Range"]
        }
    },
    "dark_seer": {
        "name": "Dark Seer",
        "title": "Ish'Kafel",
        "attr": "universal",
        "icon": "void",
        "lore": "Fast when he needs to be, and with a mind cunning and deadly, Ish'Kafel earned his title of Dark Seer.",
        "baseStats": {
            "maxHp": 110, "maxMana": 100, "hpPerLevel": 26, "manaPerLevel": 22,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "vacuum": {
                "name": "Vacuum",
                "type": "active",
                "description": "Drags all enemies in an area to a target point, dealing damage.",
                "damage": 35, "radius": 6, "pullRadius": 8,
                "cooldown": 28000, "manaCost": 30, "range": 10
            },
            "ionShell": {
                "name": "Ion Shell",
                "type": "active",
                "description": "Surrounds a unit with a rotating shield of ions that damages nearby enemies.",
                "damagePerSecond": 30, "radius": 3, "duration": 22000,
                "cooldown": 9000, "manaCost": 25, "range": 8
            },
            "surge": {
                "name": "Surge",
                "type": "active",
                "description": "Charges a target allied unit with energy, granting them maximum movement speed for a short time.",
                "duration": 5000, "cooldown": 12000, "manaCost": 20, "range": 8
            },
            "wallOfReplica": {
                "name": "Wall of Replica",
                "type": "ultimate",
                "description": "Creates a wall that slows enemies and creates illusions of enemy heroes who pass through.",
                "slowPercent": 50, "illusionDamagePercent": 80, "duration": 30000, "wallLength": 12,
                "cooldown": 80000, "manaCost": 60, "range": 10
            }
        },
        "talents": {
            "10": ["+100 Ion Shell Radius", "+8% Ion Shell Damage as Heal"],
            "15": ["+75 Vacuum AoE", "+1.5 Surge Duration"],
            "20": ["+100 Ion Shell Damage", "Parallel Wall"],
            "25": ["400 AoE Surge", "+30% Wall of Replica Illusion Damage"]
        }
    },
    "dark_willow": {
        "name": "Dark Willow",
        "title": "Mireska Sunbreeze",
        "attr": "universal",
        "icon": "fairy",
        "lore": "Children love telling scary stories, but Mireska Sunbreeze, the Dark Willow, is the scary story herself.",
        "baseStats": {
            "maxHp": 85, "maxMana": 110, "hpPerLevel": 21, "manaPerLevel": 24,
            "baseDamage": 13, "damagePerLevel": 2.7, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "brambleMaze": {
                "name": "Bramble Maze",
                "type": "active",
                "description": "Creates a maze of brambles that root and damage enemies who enter.",
                "damage": 40, "rootDuration": 2000, "duration": 11000, "radius": 6,
                "cooldown": 16000, "manaCost": 25, "range": 12
            },
            "shadowRealm": {
                "name": "Shadow Realm",
                "type": "active",
                "description": "Dark Willow recedes into the shadows, becoming untargetable. Her next attack deals bonus damage.",
                "maxBonusDamage": 100, "duration": 4000, "fadeTime": 0.5,
                "cooldown": 20000, "manaCost": 20
            },
            "cursedCrown": {
                "name": "Cursed Crown",
                "type": "active",
                "description": "Places a curse on a target that stuns them and enemies around them after a delay.",
                "stunDuration": 2500, "delay": 4000, "stunRadius": 4,
                "cooldown": 14000, "manaCost": 20, "range": 10
            },
            "bedlam": {
                "name": "Bedlam",
                "type": "ultimate",
                "description": "Dark Willow's companion Jex attacks nearby enemies rapidly.",
                "damagePerAttack": 50, "attacksPerSecond": 2, "duration": 4000, "radius": 5,
                "cooldown": 30000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+30 Damage"],
            "15": ["+100 Shadow Realm Max Damage", "+1s Cursed Crown Stun Duration"],
            "20": ["+300 Bedlam Damage", "+100 Attack Range"],
            "25": ["+2s Shadow Realm Duration", "Terrorize Pierces Spell Immune"]
        }
    },
    "dawnbreaker": {
        "name": "Dawnbreaker",
        "title": "Valora",
        "attr": "strength",
        "icon": "sun",
        "lore": "Valora, the Dawnbreaker, is the last of the Children of Light. She wields a massive hammer forged from the sun itself.",
        "baseStats": {
            "maxHp": 130, "maxMana": 80, "hpPerLevel": 30, "manaPerLevel": 18,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "starbreaker": {
                "name": "Starbreaker",
                "type": "active",
                "description": "Dawnbreaker whirls her hammer, damaging enemies and stunning those hit by the final strike.",
                "damage": 25, "slamDamage": 50, "stunDuration": 1200, "radius": 4,
                "cooldown": 11000, "manaCost": 20
            },
            "celestialHammer": {
                "name": "Celestial Hammer",
                "type": "active",
                "description": "Hurls her hammer, damaging enemies and leaving a trail of fire. Can recall to teleport.",
                "damage": 35, "trailDamage": 15, "range": 12, "recallDelay": 1500,
                "cooldown": 14000, "manaCost": 25
            },
            "luminosity": {
                "name": "Luminosity",
                "type": "passive",
                "description": "After a number of attacks, Dawnbreaker's next attack heals herself and nearby allies.",
                "attacksRequired": 3, "healPercent": 35, "healRadius": 5, "critMultiplier": 1.4
            },
            "solarGuardian": {
                "name": "Solar Guardian",
                "type": "ultimate",
                "description": "Dawnbreaker flies to an ally, creating a pulsing sun that heals allies and damages enemies.",
                "healPerPulse": 30, "damagePerPulse": 30, "pulses": 6, "landingDamage": 60, "stunDuration": 1500,
                "cooldown": 100000, "manaCost": 50, "range": 999
            }
        },
        "talents": {
            "10": ["+15 Luminosity Attack Damage", "+20 Movement Speed"],
            "15": ["+40 Starbreaker Swipe Damage", "+30% Luminosity Crit"],
            "20": ["-12s Solar Guardian Cooldown", "+2 Starbreaker Swipes"],
            "25": ["+3 Celestial Hammer Charges", "Solar Guardian Stuns"]
        }
    },
    "dazzle": {
        "name": "Dazzle",
        "title": "Shadow Priest",
        "attr": "universal",
        "icon": "purple",
        "lore": "Each morning, in the village of Dezun, Dazzle would watch the sun rise, knowing his power over life and death grew stronger.",
        "baseStats": {
            "maxHp": 90, "maxMana": 110, "hpPerLevel": 22, "manaPerLevel": 24,
            "baseDamage": 12, "damagePerLevel": 2.5, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "poisonTouch": {
                "name": "Poison Touch",
                "type": "active",
                "description": "Casts a poisonous hex on enemies, slowing them and dealing damage over time.",
                "damage": 8, "slowPercent": 25, "duration": 6000, "maxTargets": 4,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "shallowGrave": {
                "name": "Shallow Grave",
                "type": "active",
                "description": "Prevents an ally from dying for a short duration. They cannot drop below 1 HP.",
                "duration": 4000, "cooldown": 18000, "manaCost": 25, "range": 10
            },
            "shadowWave": {
                "name": "Shadow Wave",
                "type": "active",
                "description": "Sends a wave of healing that bounces between allies, damaging enemies near each target.",
                "healAmount": 40, "damage": 40, "bounces": 6, "bounceRadius": 6,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "badJuju": {
                "name": "Bad Juju",
                "type": "ultimate",
                "description": "Dazzle gains armor and reduces ability cooldowns whenever he casts a spell. Enemies near him lose armor.",
                "armorPerStack": 2, "armorReductionAura": 2, "cooldownReductionPercent": 35, "radius": 8
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+60 Damage"],
            "15": ["+30 Shadow Wave Heal/Damage", "-3s Shadow Wave Cooldown"],
            "20": ["+35 Poison Touch DPS", "+0.5s Shallow Grave Duration"],
            "25": ["+0.5s Hex on Poison Touch", "-4s Shallow Grave Cooldown"]
        }
    },
    "death_prophet": {
        "name": "Death Prophet",
        "title": "Krobelus",
        "attr": "intelligence",
        "icon": "ghost",
        "lore": "Krobelus was a Death Prophet, a seer who could speak with the spirits of the dead. She learned her own death was near.",
        "baseStats": {
            "maxHp": 95, "maxMana": 120, "hpPerLevel": 24, "manaPerLevel": 26,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "cryptSwarm": {
                "name": "Crypt Swarm",
                "type": "active",
                "description": "Sends a swarm of bats in a line, dealing damage to enemies they pass through.",
                "damage": 45, "width": 4, "range": 12,
                "cooldown": 7000, "manaCost": 20
            },
            "silence": {
                "name": "Silence",
                "type": "active",
                "description": "Silences all enemies in an area, preventing them from casting spells.",
                "duration": 5000, "radius": 5,
                "cooldown": 15000, "manaCost": 25, "range": 10
            },
            "spiritSiphon": {
                "name": "Spirit Siphon",
                "type": "active",
                "description": "Creates a link between Death Prophet and an enemy, draining their HP and slowing them.",
                "drainPercent": 6, "slowPercent": 15, "duration": 4000, "charges": 3,
                "chargeRestore": 35000, "manaCost": 15, "range": 8
            },
            "exorcism": {
                "name": "Exorcism",
                "type": "ultimate",
                "description": "Releases vengeful spirits that swarm enemies, dealing physical damage and healing Death Prophet.",
                "spirits": 20, "damagePerSpirit": 18, "healPercent": 25, "duration": 30000,
                "cooldown": 140000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+30 Damage", "+12% Magic Resistance"],
            "15": ["-2s Crypt Swarm Cooldown", "+1% Spirit Siphon Max HP Drain"],
            "20": ["+400 Health", "+8 Exorcism Spirits"],
            "25": ["Exorcism Grants Haste", "-25s Exorcism Cooldown"]
        }
    },
    "disruptor": {
        "name": "Disruptor",
        "title": "Thrall",
        "attr": "intelligence",
        "icon": "storm",
        "lore": "High on the wind plains of Druud, riders know the sky gods favor them. Thrall is the greatest stormcrafter of his tribe.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 21, "manaPerLevel": 26,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "thunderStrike": {
                "name": "Thunder Strike",
                "type": "active",
                "description": "Repeatedly strikes an enemy with lightning, dealing damage and revealing them.",
                "damagePerStrike": 20, "strikes": 4, "interval": 2000,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "glimpse": {
                "name": "Glimpse",
                "type": "active",
                "description": "Teleports an enemy hero back to where they were a few seconds ago.",
                "lookbackTime": 4000, "cooldown": 16000, "manaCost": 25, "range": 12
            },
            "kineticField": {
                "name": "Kinetic Field",
                "type": "active",
                "description": "Creates a circular field that prevents enemies from leaving.",
                "duration": 3000, "formationTime": 1200, "radius": 4,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "staticStorm": {
                "name": "Static Storm",
                "type": "ultimate",
                "description": "Creates a damaging storm that silences enemies within it. Damage increases over time.",
                "maxDamagePerSecond": 80, "duration": 5000, "radius": 5,
                "cooldown": 80000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+40 Thunder Strike Damage", "+150 Cast Range"],
            "15": ["+150 Glimpse Cast Range", "-2s Kinetic Field Cooldown"],
            "20": ["+1.5s Static Storm Duration", "+1.5s Kinetic Field Duration"],
            "25": ["3 Thunder Strike Hits Kinetic Field", "Static Storm Grants Disruptor True Sight"]
        }
    },
    "doom": {
        "name": "Doom",
        "title": "Lucifer",
        "attr": "strength",
        "icon": "fire",
        "lore": "He who was once the morning star, Lucifer, fell from grace and became the lord of all demons, Doom.",
        "baseStats": {
            "maxHp": 140, "maxMana": 70, "hpPerLevel": 32, "manaPerLevel": 15,
            "baseDamage": 21, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 0.9
        },
        "abilities": {
            "devour": {
                "name": "Devour",
                "type": "active",
                "description": "Consumes a creep, gaining bonus gold and the creep's abilities.",
                "bonusGold": 100, "digestTime": 70000, "cooldown": 60000, "manaCost": 30, "range": 3
            },
            "scorchedEarth": {
                "name": "Scorched Earth",
                "type": "active",
                "description": "Doom engulfs himself in flames, damaging nearby enemies and gaining bonus movement speed and regen.",
                "damagePerSecond": 30, "healPerSecond": 30, "moveSpeedBonus": 14, "duration": 12000, "radius": 5,
                "cooldown": 30000, "manaCost": 30
            },
            "infernalBlade": {
                "name": "Infernal Blade",
                "type": "passive",
                "description": "Doom's attacks deal bonus damage based on the enemy's max HP and stun briefly.",
                "hpBurnPercent": 2, "ministun": 400, "dotDuration": 4000, "cooldown": 14000
            },
            "doom_ability": {
                "name": "Doom",
                "type": "ultimate",
                "description": "Inflicts Doom on the target, dealing massive damage over time and muting all items and abilities.",
                "damagePerSecond": 40, "duration": 16000, "cooldown": 140000, "manaCost": 60, "range": 8
            }
        },
        "talents": {
            "10": ["+15 Scorched Earth Movement Speed", "+1.5% Infernal Blade Damage"],
            "15": ["+120 Devour Bonus Gold", "+15 Scorched Earth Damage"],
            "20": ["+50 Doom DPS", "Devour Can Target Ancients"],
            "25": ["+2% Infernal Blade Damage", "Doom Applies Break"]
        }
    },
    "dragon_knight": {
        "name": "Dragon Knight",
        "title": "Davion",
        "attr": "strength",
        "icon": "dragon",
        "lore": "After years of training, Davion the Dragon Knight joined the Dragonguard. In a final battle, he slew the dragon Slyrak but was transformed.",
        "baseStats": {
            "maxHp": 130, "maxMana": 75, "hpPerLevel": 30, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "breatheFire": {
                "name": "Breathe Fire",
                "type": "active",
                "description": "Breathes fire in a cone, damaging enemies and reducing their attack damage.",
                "damage": 45, "attackReduction": 30, "reductionDuration": 8000, "range": 8,
                "cooldown": 11000, "manaCost": 25
            },
            "dragonTail": {
                "name": "Dragon Tail",
                "type": "active",
                "description": "Strikes an enemy with his shield, stunning them and dealing damage.",
                "damage": 30, "stunDuration": 2500, "cooldown": 10000, "manaCost": 20, "range": 2.5
            },
            "dragonBlood": {
                "name": "Dragon Blood",
                "type": "passive",
                "description": "Grants increased health regeneration and armor from dragon heritage.",
                "hpRegen": 8, "bonusArmor": 8
            },
            "elderDragonForm": {
                "name": "Elder Dragon Form",
                "type": "ultimate",
                "description": "Transforms into a powerful dragon with ranged attacks and special abilities.",
                "bonusAttackRange": 8, "poisonDamage": 15, "splashPercent": 50, "slowPercent": 35, "duration": 50000,
                "cooldown": 100000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+2.5 Mana Regen", "+15 Damage"],
            "15": ["+30 Dragon Tail Damage", "+500 Night Vision"],
            "20": ["+25 Strength", "+150 Breathe Fire Damage"],
            "25": ["+1.8s Dragon Tail Stun Duration", "2x Dragon Blood HP Regen/Armor"]
        }
    },
    "earth_spirit": {
        "name": "Earth Spirit",
        "title": "Kaolin",
        "attr": "strength",
        "icon": "rock",
        "lore": "Deep in the barren hills of Narshen, Kaolin the Earth Spirit was one of the four spirits, guardians of elemental balance.",
        "baseStats": {
            "maxHp": 120, "maxMana": 90, "hpPerLevel": 28, "manaPerLevel": 20,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "boulderSmash": {
                "name": "Boulder Smash",
                "type": "active",
                "description": "Earth Spirit kicks a Stone Remnant or enemy unit, stunning and damaging units in its path.",
                "damage": 40, "stunDuration": 1500, "range": 12,
                "cooldown": 14000, "manaCost": 20
            },
            "rollingBoulder": {
                "name": "Rolling Boulder",
                "type": "active",
                "description": "Earth Spirit rolls as a boulder, stunning and damaging enemies. Travels faster if it passes through a Remnant.",
                "damage": 35, "stunDuration": 1200, "speed": 15, "remnantSpeed": 25,
                "cooldown": 12000, "manaCost": 25, "range": 10
            },
            "geomagneticGrip": {
                "name": "Geomagnetic Grip",
                "type": "active",
                "description": "Pulls a Stone Remnant toward Earth Spirit, silencing enemies it passes through.",
                "silenceDuration": 3000, "damage": 30,
                "cooldown": 13000, "manaCost": 20, "range": 12
            },
            "magnetize": {
                "name": "Magnetize",
                "type": "ultimate",
                "description": "Magnetizes nearby enemies, causing them to take damage over time. Remnants refresh and spread the debuff.",
                "damagePerSecond": 40, "duration": 6000, "radius": 5,
                "cooldown": 80000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+250 Rolling Boulder Damage", "+10 Strength"],
            "15": ["+2s Geomagnetic Grip Silence", "-50 Rolling Boulder Cooldown"],
            "20": ["+15% Spell Amplification", "+150 Boulder Smash Damage"],
            "25": ["Magnetize Undispellable", "+2s Magnetize Duration"]
        }
    },
    "elder_titan": {
        "name": "Elder Titan",
        "title": "Worldsmith",
        "attr": "strength",
        "icon": "titan",
        "lore": "The Elder Titan was the creator of worlds. Now, searching for a flaw in his design, he wanders alone.",
        "baseStats": {
            "maxHp": 130, "maxMana": 85, "hpPerLevel": 30, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "echoStomp": {
                "name": "Echo Stomp",
                "type": "active",
                "description": "Elder Titan and his Astral Spirit stomp together, sleeping all nearby enemies.",
                "damage": 40, "sleepDuration": 4000, "radius": 5, "channelTime": 1400,
                "cooldown": 11000, "manaCost": 25
            },
            "astralSpirit": {
                "name": "Astral Spirit",
                "type": "active",
                "description": "Sends out Elder Titan's spirit, damaging enemies and returning with bonus damage and speed for each hero hit.",
                "damage": 30, "bonusDamagePerHero": 20, "bonusSpeedPerHero": 5, "duration": 8000,
                "cooldown": 16000, "manaCost": 20, "range": 12
            },
            "naturalOrder": {
                "name": "Natural Order",
                "type": "passive",
                "description": "Elder Titan's presence strips enemies of their natural defenses, reducing armor and magic resistance.",
                "armorReductionPercent": 75, "magicResistReductionPercent": 75, "radius": 4
            },
            "earthSplitter": {
                "name": "Earth Splitter",
                "type": "ultimate",
                "description": "Cracks the earth, dealing a percentage of enemies' max HP and slowing them.",
                "maxHpDamagePercent": 35, "slowPercent": 50, "slowDuration": 4000, "delay": 3000, "length": 14,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+200 Health", "+20 Astral Spirit Hero Damage"],
            "15": ["+100% Cleave", "+100 Echo Stomp Damage"],
            "20": ["+30% Magic Resistance", "+100 Astral Spirit Damage"],
            "25": ["+50% Earth Splitter Damage", "0% Natural Order Armor"]
        }
    },
    "ember_spirit": {
        "name": "Ember Spirit",
        "title": "Xin",
        "attr": "agility",
        "icon": "flame",
        "lore": "Xin the Ember Spirit was one of four celestial spirits dedicated to maintaining universal balance.",
        "baseStats": {
            "maxHp": 90, "maxMana": 80, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 12, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "searingChains": {
                "name": "Searing Chains",
                "type": "active",
                "description": "Ember Spirit unleashes chains that bind and damage nearby enemies.",
                "damage": 25, "duration": 2500, "maxTargets": 2, "radius": 4,
                "cooldown": 10000, "manaCost": 20
            },
            "slightOfFist": {
                "name": "Sleight of Fist",
                "type": "active",
                "description": "Ember Spirit dashes around, attacking all enemies in an area and returning to his origin point.",
                "bonusDamage": 40, "radius": 6, "cooldown": 6000, "manaCost": 20, "range": 10
            },
            "flameguard": {
                "name": "Flame Guard",
                "type": "active",
                "description": "Ember Spirit surrounds himself with fire, absorbing magic damage and dealing damage to nearby enemies.",
                "damageAbsorb": 100, "damagePerSecond": 25, "duration": 10000, "radius": 4,
                "cooldown": 30000, "manaCost": 30
            },
            "fireRemnant": {
                "name": "Fire Remnant",
                "type": "ultimate",
                "description": "Places fire remnants that Ember Spirit can dash to, damaging enemies in his path.",
                "damageOnDash": 50, "maxRemnants": 3, "remnantDuration": 45000, "remnantCooldown": 35000,
                "dashCooldown": 0, "manaCostPerRemnant": 35, "range": 15
            }
        },
        "talents": {
            "10": ["+15 Damage", "+0.5s Searing Chains"],
            "15": ["+1s Fire Remnant Duration", "+50 Flame Guard Damage/Shield"],
            "20": ["+80 Sleight of Fist Damage", "True Strike"],
            "25": ["-12s Fire Remnant Charge Restore", "+2 Searing Chain Targets"]
        }
    },
    "enchantress": {
        "name": "Enchantress",
        "title": "Aiushtha",
        "attr": "universal",
        "icon": "deer",
        "lore": "Aiushtha appears to be a Dryad, but no mere forest sprite has her power. The Enchantress charms all who meet her.",
        "baseStats": {
            "maxHp": 85, "maxMana": 100, "hpPerLevel": 21, "manaPerLevel": 22,
            "baseDamage": 12, "damagePerLevel": 2.5, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "untouchable": {
                "name": "Untouchable",
                "type": "passive",
                "description": "Enchantress beguiles her enemies, slowing their attacks when they assault her.",
                "attackSlowPercent": 100
            },
            "enchant": {
                "name": "Enchant",
                "type": "active",
                "description": "Takes control of an enemy creep or slows an enemy hero.",
                "slowPercent": 55, "slowDuration": 5000, "controlDuration": 80000,
                "cooldown": 20000, "manaCost": 25, "range": 8
            },
            "naturesAttendants": {
                "name": "Nature's Attendants",
                "type": "active",
                "description": "Wisps surround Enchantress, healing her and nearby allies over time.",
                "healPerWisp": 2, "numWisps": 8, "duration": 10000, "radius": 5,
                "cooldown": 35000, "manaCost": 30
            },
            "impetus": {
                "name": "Impetus",
                "type": "ultimate",
                "description": "Places a magical charge on attacks that deals bonus damage based on distance traveled.",
                "damagePerDistance": 3, "maxDistance": 20, "manaCost": 15
            }
        },
        "talents": {
            "10": ["+15% Magic Resistance", "+8 Nature's Attendants Wisps"],
            "15": ["+8 Enchant Slow", "+35 Movement Speed"],
            "20": ["+100 Impetus Distance Damage", "+8% Untouchable Slow"],
            "25": ["+25 Nature's Attendants Heal", "+4% Impetus Distance Damage"]
        }
    },
    "enigma": {
        "name": "Enigma",
        "title": "Void Entity",
        "attr": "universal",
        "icon": "void",
        "lore": "Nothing is known of Enigma's past, save that he is a fundamental force of the universe, a being of pure malice.",
        "baseStats": {
            "maxHp": 105, "maxMana": 100, "hpPerLevel": 26, "manaPerLevel": 22,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "malefice": {
                "name": "Malefice",
                "type": "active",
                "description": "Repeatedly stuns and damages a target enemy over several seconds.",
                "damagePerStun": 20, "stunDuration": 600, "stuns": 4, "totalDuration": 4500,
                "cooldown": 14000, "manaCost": 25, "range": 8
            },
            "demonic_conversion": {
                "name": "Demonic Conversion",
                "type": "active",
                "description": "Transforms a creep into three Eidolons that multiply when attacking.",
                "eidolonDamage": 20, "eidolonHP": 150, "duration": 35000, "attacksToSplit": 6,
                "cooldown": 30000, "manaCost": 30, "range": 8
            },
            "midnightPulse": {
                "name": "Midnight Pulse",
                "type": "active",
                "description": "Creates a zone of pure void that deals damage based on enemies' max HP.",
                "damagePercent": 4, "duration": 10000, "radius": 5,
                "cooldown": 30000, "manaCost": 25, "range": 10
            },
            "blackHole": {
                "name": "Black Hole",
                "type": "ultimate",
                "description": "Creates a vortex that sucks in and disables all nearby enemies while dealing massive damage.",
                "damagePerSecond": 60, "duration": 4000, "radius": 5,
                "cooldown": 160000, "manaCost": 60, "range": 8
            }
        },
        "talents": {
            "10": ["+20 Eidolon Damage", "+15 Malefice Instance Damage"],
            "15": ["+150 Cast Range", "+15 Eidolon Health"],
            "20": ["+100 Black Hole DPS", "+3% Midnight Pulse Damage"],
            "25": ["+5 Demonic Conversion Eidolons", "Black Hole Undispellable"]
        }
    }
}

def generate_hero_file(hero_id, hero_data):
    """Generate a JSON file for a single hero"""
    filepath = os.path.join(HEROES_DIR, f"{hero_id}.json")

    output = {
        "id": hero_id,
        "version": "1.0.0",
        **hero_data
    }

    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Generated: {filepath}")

def main():
    """Generate all hero files"""
    os.makedirs(HEROES_DIR, exist_ok=True)

    for hero_id, hero_data in HEROES.items():
        generate_hero_file(hero_id, hero_data)

    print(f"\nGenerated {len(HEROES)} hero files in {HEROES_DIR}")

if __name__ == "__main__":
    main()
