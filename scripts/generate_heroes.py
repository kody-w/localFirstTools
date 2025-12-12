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
    },
    "faceless_void": {
        "name": "Faceless Void",
        "title": "Darkterror",
        "attr": "agility",
        "icon": "time",
        "lore": "Darkterror the Faceless Void is a creature of another realm, bound by powerful magic to exist between dimensions.",
        "baseStats": {
            "maxHp": 95, "maxMana": 75, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "timeWalk": {
                "name": "Time Walk",
                "type": "active",
                "description": "Rushes to a location and reverses all damage taken in the last few seconds.",
                "reverseDuration": 2000, "range": 8,
                "cooldown": 10000, "manaCost": 20
            },
            "timeDilation": {
                "name": "Time Dilation",
                "type": "active",
                "description": "Slows enemies in an area and freezes their ability cooldowns.",
                "slowPercent": 20, "cooldownFreeze": 1000, "duration": 8000, "radius": 6,
                "cooldown": 20000, "manaCost": 25
            },
            "timelock": {
                "name": "Time Lock",
                "type": "passive",
                "description": "Gives a chance to lock an enemy in time, stunning and dealing bonus damage.",
                "procChance": 25, "stunDuration": 800, "bonusDamage": 30
            },
            "chronosphere": {
                "name": "Chronosphere",
                "type": "ultimate",
                "description": "Creates a sphere where time stands still. All units except Faceless Void are frozen.",
                "duration": 5000, "radius": 5,
                "cooldown": 140000, "manaCost": 60, "range": 8
            }
        },
        "talents": {
            "10": ["+8 Strength", "+10 Time Lock Damage"],
            "15": ["+40 Damage", "+100 Time Walk Range"],
            "20": ["+500 Timewalk Cast Range", "+100 Chronosphere AoE"],
            "25": ["+25% Backtrack", "-50s Chronosphere Cooldown"]
        }
    },
    "grimstroke": {
        "name": "Grimstroke",
        "title": "Artist of Death",
        "attr": "intelligence",
        "icon": "brush",
        "lore": "To Grimstroke, the beauty of the world lies in its potential for destruction. His art is pure devastation.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 21, "manaPerLevel": 26,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "strokeOfFate": {
                "name": "Stroke of Fate",
                "type": "active",
                "description": "Paints a path of destruction, damaging enemies. Damage increases per enemy hit.",
                "baseDamage": 30, "damagePerUnit": 10, "range": 12, "width": 3,
                "cooldown": 8000, "manaCost": 20
            },
            "phantomsEmbrace": {
                "name": "Phantom's Embrace",
                "type": "active",
                "description": "Summons a phantom that latches onto an enemy, silencing them and dealing damage over time.",
                "damage": 20, "silenceDuration": 4000, "latches": 4,
                "cooldown": 18000, "manaCost": 25, "range": 10
            },
            "inkSwell": {
                "name": "Ink Swell",
                "type": "active",
                "description": "Covers an ally with ink that damages nearby enemies. At the end, it stuns nearby enemies.",
                "damagePerSecond": 20, "stunDuration": 3000, "duration": 3000, "radius": 4,
                "cooldown": 20000, "manaCost": 30, "range": 8
            },
            "soulbind": {
                "name": "Soulbind",
                "type": "ultimate",
                "description": "Binds two enemy heroes together. Any targeted spell cast on one affects both.",
                "duration": 6000, "range": 10, "leashRange": 8,
                "cooldown": 70000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+30 Movement Speed", "+50 Phantom's Embrace Damage"],
            "15": ["+12% Spell Amplification", "-4s Ink Swell Cooldown"],
            "20": ["+50% Stroke of Fate Damage", "+2s Soulbind Duration"],
            "25": ["Ink Swell Deals Damage", "3 Phantom's Embrace Charges"]
        }
    },
    "gyrocopter": {
        "name": "Gyrocopter",
        "title": "Aurel Vlaicu",
        "attr": "agility",
        "icon": "copter",
        "lore": "After finding a crashed flying machine, Aurel Vlaicu spent years rebuilding it. Now he soars above battlefields.",
        "baseStats": {
            "maxHp": 90, "maxMana": 85, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.2
        },
        "abilities": {
            "rocketBarrage": {
                "name": "Rocket Barrage",
                "type": "active",
                "description": "Launches rockets at nearby enemies, dealing damage over time.",
                "damagePerRocket": 8, "rockets": 30, "duration": 3000, "radius": 4,
                "cooldown": 7000, "manaCost": 20
            },
            "homingMissile": {
                "name": "Homing Missile",
                "type": "active",
                "description": "Launches a missile that homes in on an enemy, stunning on impact.",
                "damage": 40, "stunDuration": 2000, "growthDamage": 30, "growthTime": 3000,
                "cooldown": 18000, "manaCost": 25, "range": 12
            },
            "flakCannon": {
                "name": "Flak Cannon",
                "type": "active",
                "description": "Gyrocopter's attacks hit all enemies in a range for a limited number of attacks.",
                "attacks": 6, "radius": 6, "cooldown": 20000, "manaCost": 20
            },
            "callDown": {
                "name": "Call Down",
                "type": "ultimate",
                "description": "Calls down two missiles that slow and damage enemies in the target area.",
                "firstStrikeDamage": 100, "secondStrikeDamage": 150, "slowPercent": 40, "radius": 5,
                "cooldown": 80000, "manaCost": 50, "range": 12
            }
        },
        "talents": {
            "10": ["+20 Damage", "+200 Health"],
            "15": ["+40 Movement Speed", "+3 Rocket Barrage Damage"],
            "20": ["+0.5s Homing Missile Stun Duration", "+25 Flak Cannon Damage"],
            "25": ["Global Call Down", "+50% Homing Missile Damage"]
        }
    },
    "hoodwink": {
        "name": "Hoodwink",
        "title": "Forest Rogue",
        "attr": "agility",
        "icon": "acorn",
        "lore": "Hoodwink grew up in the forest, learning to fight with cunning and trickery against much larger foes.",
        "baseStats": {
            "maxHp": 80, "maxMana": 90, "hpPerLevel": 20, "manaPerLevel": 20,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "acornShot": {
                "name": "Acorn Shot",
                "type": "active",
                "description": "Fires an acorn that bounces between enemies, slowing them. Plants a tree if it hits the ground.",
                "damage": 35, "bounces": 4, "slowPercent": 25, "slowDuration": 2000,
                "cooldown": 8000, "manaCost": 20, "range": 10
            },
            "bushwhack": {
                "name": "Bushwhack",
                "type": "active",
                "description": "Throws a net that stuns enemies if they're near a tree.",
                "damage": 40, "stunDuration": 2000, "radius": 4,
                "cooldown": 14000, "manaCost": 25, "range": 10
            },
            "scurry": {
                "name": "Scurry",
                "type": "passive",
                "description": "Hoodwink has a chance to evade attacks. Gains bonus movement speed near trees.",
                "evasionChance": 25, "moveSpeedNearTrees": 30, "treeRadius": 4
            },
            "sharpshooter": {
                "name": "Sharpshooter",
                "type": "ultimate",
                "description": "Charges up and fires a powerful bolt that deals massive damage based on charge time.",
                "maxDamage": 400, "maxChargeTime": 3000, "slowPercent": 50, "breakDuration": 5000,
                "cooldown": 45000, "manaCost": 50, "range": 25
            }
        },
        "talents": {
            "10": ["+25 Acorn Shot Damage", "+1 Acorn Shot Bounce"],
            "15": ["+1.5s Bushwhack Stun Duration", "+30 Movement Speed"],
            "20": ["+100% Acorn Shot Damage", "+150 Sharpshooter Max Damage"],
            "25": ["Scurry Camouflage", "2 Acorn Shot Charges"]
        }
    },
    "huskar": {
        "name": "Huskar",
        "title": "Sacred Warrior",
        "attr": "strength",
        "icon": "spear",
        "lore": "Huskar is a warrior of the Dezun Order, devoted to the goddess Dazzle. He grows stronger as death approaches.",
        "baseStats": {
            "maxHp": 130, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "innerFire": {
                "name": "Inner Fire",
                "type": "active",
                "description": "Releases an inner fire that knocks back enemies and disarms them.",
                "damage": 35, "disarmDuration": 3000, "knockback": 3, "radius": 5,
                "cooldown": 14000, "manaCost": 20
            },
            "burningSpear": {
                "name": "Burning Spear",
                "type": "toggle",
                "description": "Imbues spears with flames, dealing damage over time but costing HP per attack.",
                "dotDamage": 8, "dotDuration": 8000, "hpCost": 5
            },
            "berserkersBlood": {
                "name": "Berserker's Blood",
                "type": "passive",
                "description": "Huskar gains attack speed and magic resistance as his health drops.",
                "maxAttackSpeedBonus": 300, "maxMagicResist": 50, "healthThreshold": 0.1
            },
            "lifeBreak": {
                "name": "Life Break",
                "type": "ultimate",
                "description": "Huskar leaps at an enemy, dealing damage based on the target's current HP. Also damages himself.",
                "targetDamagePercent": 35, "selfDamagePercent": 35, "slowPercent": 60, "slowDuration": 4000,
                "cooldown": 12000, "manaCost": 0, "range": 8
            }
        },
        "talents": {
            "10": ["+15 Damage", "+15% Lifesteal"],
            "15": ["+300 Health", "+20 Burning Spear DPS"],
            "20": ["+15% Life Break Damage", "+30% Berserker's Blood Attack Speed"],
            "25": ["0 Inner Fire Cooldown", "+350 Life Break Cast Range"]
        }
    },
    "io": {
        "name": "Io",
        "title": "Wisp",
        "attr": "universal",
        "icon": "wisp",
        "lore": "Io is a fundamental force of the universe, an amalgam of pure energy. It seeks out other beings to bond with.",
        "baseStats": {
            "maxHp": 80, "maxMana": 100, "hpPerLevel": 20, "manaPerLevel": 22,
            "baseDamage": 12, "damagePerLevel": 2.5, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 12, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "tether": {
                "name": "Tether",
                "type": "active",
                "description": "Links Io to an allied unit, sharing regeneration and granting movement speed.",
                "hpRegenShare": 1.5, "manaRegenShare": 1.5, "moveSpeedBonus": 15, "breakDistance": 15,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "spirits": {
                "name": "Spirits",
                "type": "active",
                "description": "Summons spirits that rotate around Io, damaging enemies they pass through.",
                "damage": 30, "numSpirits": 5, "duration": 19000, "radius": 8,
                "cooldown": 20000, "manaCost": 25
            },
            "overcharge": {
                "name": "Overcharge",
                "type": "toggle",
                "description": "Io channels energy, draining HP and mana but granting attack speed and damage reduction.",
                "attackSpeedBonus": 60, "damageReduction": 15, "hpDrainPercent": 4, "manaDrainPercent": 4
            },
            "relocate": {
                "name": "Relocate",
                "type": "ultimate",
                "description": "Teleports Io and a tethered ally to any location on the map. Returns after a delay.",
                "returnDelay": 12000, "castTime": 3000, "cooldown": 80000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+6 Health Regen", "+45 Spirits Hero Damage"],
            "15": ["+75 Spirits Damage", "-25s Relocate Cooldown"],
            "20": ["-10s Spirits Cooldown", "+15% Overcharge Damage Reduction"],
            "25": ["+1.5x Tether Regen Share", "Relocate Grants Invisibility"]
        }
    },
    "jakiro": {
        "name": "Jakiro",
        "title": "Twin Head Dragon",
        "attr": "intelligence",
        "icon": "twinhead",
        "lore": "A freak of nature with two heads that fight each other almost as much as their enemies. One breathes fire, the other ice.",
        "baseStats": {
            "maxHp": 95, "maxMana": 110, "hpPerLevel": 24, "manaPerLevel": 24,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "dualBreath": {
                "name": "Dual Breath",
                "type": "active",
                "description": "Jakiro breathes fire and ice, damaging and slowing enemies in a line.",
                "fireDamage": 35, "iceDamage": 30, "slowPercent": 35, "slowDuration": 3000, "range": 10,
                "cooldown": 10000, "manaCost": 25
            },
            "iceBreath": {
                "name": "Ice Path",
                "type": "active",
                "description": "Creates a path of ice that stuns enemies who walk through it.",
                "stunDuration": 2000, "pathDuration": 3000, "length": 12,
                "cooldown": 12000, "manaCost": 25, "range": 12
            },
            "liquidFire": {
                "name": "Liquid Fire",
                "type": "passive",
                "description": "Jakiro's attacks burn the target, dealing damage over time and slowing attack speed.",
                "damagePerSecond": 15, "duration": 5000, "attackSlowPercent": 40, "cooldown": 4000
            },
            "macropyre": {
                "name": "Macropyre",
                "type": "ultimate",
                "description": "Creates a massive river of fire that burns enemies for massive damage over time.",
                "damagePerSecond": 80, "duration": 10000, "length": 18, "width": 4,
                "cooldown": 60000, "manaCost": 60, "range": 12
            }
        },
        "talents": {
            "10": ["+250 Health", "+8% Magic Resistance"],
            "15": ["+50 Dual Breath Damage", "+350 Attack Range"],
            "20": ["+100 Liquid Fire DPS", "+0.8s Ice Path Duration"],
            "25": ["+150 Macropyre DPS", "Macropyre Pure and Pierces Immunity"]
        }
    },
    "keeper_of_the_light": {
        "name": "Keeper of the Light",
        "title": "Ezalor",
        "attr": "universal",
        "icon": "light",
        "lore": "Ezalor is an ancient being, one of the Fundamentals. He is the keeper of light itself, wielding it against evil.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 20, "manaPerLevel": 28,
            "baseDamage": 12, "damagePerLevel": 2.4, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "illuminate": {
                "name": "Illuminate",
                "type": "active",
                "description": "Channels a wave of light that damages enemies. Longer channel = more damage.",
                "maxDamage": 150, "maxChannelTime": 5000, "range": 18, "width": 4,
                "cooldown": 14000, "manaCost": 30
            },
            "blindingLight": {
                "name": "Blinding Light",
                "type": "active",
                "description": "Creates a burst of light that knocks back enemies and causes them to miss attacks.",
                "missChance": 80, "knockback": 4, "duration": 4000, "radius": 5,
                "cooldown": 20000, "manaCost": 25, "range": 10
            },
            "chakraMagic": {
                "name": "Chakra Magic",
                "type": "active",
                "description": "Restores mana to a target ally and reduces their ability cooldowns.",
                "manaRestore": 150, "cooldownReduction": 4000,
                "cooldown": 16000, "manaCost": 0, "range": 10
            },
            "spiritForm": {
                "name": "Spirit Form",
                "type": "ultimate",
                "description": "Transforms into spirit form, gaining Will-O-Wisp which creates a hypnotizing light.",
                "wispDamage": 50, "wispStunInterval": 1500, "wispDuration": 5000, "wispRadius": 5,
                "cooldown": 80000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+200 Cast Range", "+25 Movement Speed"],
            "15": ["+300 Illuminate Damage", "+2s Blinding Light Miss Chance"],
            "20": ["+1.5s Will-O-Wisp Stun Interval", "+35% Magic Resistance"],
            "25": ["Illuminate Heals Allies for 50%", "+3 Will-O-Wisp Flicker"]
        }
    },
    "kunkka": {
        "name": "Kunkka",
        "title": "Admiral",
        "attr": "strength",
        "icon": "anchor",
        "lore": "As Admiral of the Claddish Navy, Kunkka commanded a fleet until a demon from the Cataract destroyed it all.",
        "baseStats": {
            "maxHp": 130, "maxMana": 80, "hpPerLevel": 30, "manaPerLevel": 18,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "torrent": {
                "name": "Torrent",
                "type": "active",
                "description": "Summons a rising torrent of water that stuns, lifts, and damages enemies.",
                "damage": 40, "stunDuration": 1500, "slowPercent": 35, "slowDuration": 3000, "radius": 4,
                "cooldown": 12000, "manaCost": 25, "range": 12
            },
            "tidebringer": {
                "name": "Tidebringer",
                "type": "passive",
                "description": "Kunkka's attacks cleave in a massive arc, dealing bonus damage to enemies.",
                "bonusDamage": 50, "cleaveRadius": 8, "cleavePercent": 100, "cooldown": 8000
            },
            "xMark": {
                "name": "X Marks the Spot",
                "type": "active",
                "description": "Marks a target's position. After a delay, they're returned to that spot.",
                "delay": 4000, "cooldown": 16000, "manaCost": 20, "range": 10
            },
            "ghostShip": {
                "name": "Ghostship",
                "type": "ultimate",
                "description": "Summons a ghostly ship that crashes into enemies, stunning and damaging them.",
                "damage": 80, "stunDuration": 1400, "delayDamagePercent": 40, "buffDuration": 8000,
                "cooldown": 60000, "manaCost": 50, "range": 15
            }
        },
        "talents": {
            "10": ["+30 Damage", "+40 Torrent Damage"],
            "15": ["+100 Tidebringer Cleave Damage", "+12 Health Regen"],
            "20": ["+50% Tidebringer Cleave", "+1s Torrent Slow Duration"],
            "25": ["Ghostship Fleet", "+100% Tidebringer Damage"]
        }
    },
    "legion_commander": {
        "name": "Legion Commander",
        "title": "Tresdin",
        "attr": "strength",
        "icon": "duel",
        "lore": "Tresdin, the Legion Commander, was the only survivor when demons destroyed the Bronze Legion. She rebuilt and leads again.",
        "baseStats": {
            "maxHp": 130, "maxMana": 75, "hpPerLevel": 30, "manaPerLevel": 16,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "overwhelmingOdds": {
                "name": "Overwhelming Odds",
                "type": "active",
                "description": "Deals damage based on the number of enemies in an area. Gains movement speed for each hero hit.",
                "baseDamage": 40, "damagePerUnit": 10, "damagePerHero": 30, "speedPerHero": 9, "radius": 5,
                "cooldown": 15000, "manaCost": 25, "range": 10
            },
            "pressTheAttack": {
                "name": "Press the Attack",
                "type": "active",
                "description": "Empowers an ally, granting attack speed and HP regeneration.",
                "attackSpeedBonus": 100, "hpRegen": 50, "duration": 5000, "cooldown": 13000, "manaCost": 20, "range": 8
            },
            "momentOfCourage": {
                "name": "Moment of Courage",
                "type": "passive",
                "description": "When attacked, Legion Commander has a chance to immediately counterattack with bonus lifesteal.",
                "procChance": 25, "lifestealPercent": 80
            },
            "duel": {
                "name": "Duel",
                "type": "ultimate",
                "description": "Forces a target to fight Legion Commander one-on-one. The winner gains permanent damage.",
                "bonusDamage": 20, "duration": 5500, "cooldown": 50000, "manaCost": 40, "range": 3
            }
        },
        "talents": {
            "10": ["+8 Strength", "+75 Overwhelming Odds Hero Damage"],
            "15": ["+75 Press the Attack HP Regen", "+30 Movement Speed"],
            "20": ["+30% Moment of Courage Lifesteal", "+30 Duel Damage Bonus"],
            "25": ["+1.5s Duel Duration", "Press the Attack Applies Strong Dispel"]
        }
    },
    "leshrac": {
        "name": "Leshrac",
        "title": "Tormented Soul",
        "attr": "intelligence",
        "icon": "torment",
        "lore": "Leshrac is a tormented spirit who saw the true nature of reality and was driven mad by its horror.",
        "baseStats": {
            "maxHp": 85, "maxMana": 130, "hpPerLevel": 21, "manaPerLevel": 28,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "splitEarth": {
                "name": "Split Earth",
                "type": "active",
                "description": "Splits the earth, stunning and damaging enemies in an area after a delay.",
                "damage": 50, "stunDuration": 2000, "delay": 350, "radius": 4,
                "cooldown": 9000, "manaCost": 25, "range": 10
            },
            "diabolicEdict": {
                "name": "Diabolic Edict",
                "type": "active",
                "description": "Summons explosions around Leshrac that damage enemies and structures.",
                "damage": 12, "explosions": 40, "duration": 10000, "radius": 5,
                "cooldown": 20000, "manaCost": 30
            },
            "lightningStorm": {
                "name": "Lightning Storm",
                "type": "active",
                "description": "Calls a lightning storm that jumps between enemies, slowing and damaging them.",
                "damage": 35, "jumps": 6, "slowPercent": 50, "slowDuration": 1000,
                "cooldown": 5000, "manaCost": 20, "range": 10
            },
            "pulseNova": {
                "name": "Pulse Nova",
                "type": "ultimate",
                "description": "Creates waves of damaging energy around Leshrac. Drains mana while active.",
                "damagePerPulse": 50, "pulseInterval": 1000, "radius": 5, "manaDrainPerSecond": 30
            }
        },
        "talents": {
            "10": ["+15 Movement Speed", "+15 Diabolic Edict Explosions"],
            "15": ["+100 Lightning Storm Damage", "+100 Split Earth Damage"],
            "20": ["+25 Pulse Nova Damage", "-2s Split Earth Cooldown"],
            "25": ["+60 Diabolic Edict Explosions", "0 Pulse Nova Mana Cost"]
        }
    },
    "lich": {
        "name": "Lich",
        "title": "Ethreain",
        "attr": "intelligence",
        "icon": "cold",
        "lore": "In life, Ethreain was a powerful mage who sacrificed his kingdom for immortality. Now he is the Lich.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 20, "manaPerLevel": 28,
            "baseDamage": 12, "damagePerLevel": 2.5, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 0.9
        },
        "abilities": {
            "frostBlast": {
                "name": "Frost Blast",
                "type": "active",
                "description": "Blasts an enemy with frost, damaging and slowing them and nearby enemies.",
                "damage": 40, "slowPercent": 30, "slowDuration": 4000, "radius": 4,
                "cooldown": 8000, "manaCost": 20, "range": 10
            },
            "frostShield": {
                "name": "Frost Shield",
                "type": "active",
                "description": "Surrounds an ally with frost, reducing incoming damage and damaging nearby enemies.",
                "damageReduction": 40, "damagePerSecond": 15, "duration": 6000, "radius": 4,
                "cooldown": 20000, "manaCost": 25, "range": 10
            },
            "sinisterGaze": {
                "name": "Sinister Gaze",
                "type": "active",
                "description": "Hypnotizes an enemy, causing them to walk toward Lich and draining their mana.",
                "duration": 2500, "manaDrainPercent": 20, "cooldown": 16000, "manaCost": 20, "range": 8
            },
            "chainFrost": {
                "name": "Chain Frost",
                "type": "ultimate",
                "description": "Releases an orb of frost that bounces between enemies, dealing massive damage and slowing.",
                "damage": 100, "bounces": 10, "slowPercent": 50, "slowDuration": 2500,
                "cooldown": 100000, "manaCost": 60, "range": 10
            }
        },
        "talents": {
            "10": ["+100 Frost Blast Radius/Damage", "+15 Movement Speed"],
            "15": ["+100 Cast Range", "+1s Sinister Gaze Duration"],
            "20": ["+1.5s Frost Shield Duration", "-3s Frost Blast Cooldown"],
            "25": ["Chain Frost Unlimited Bounces", "+4s Frost Shield Duration"]
        }
    },
    "lifestealer": {
        "name": "Lifestealer",
        "title": "N'aix",
        "attr": "strength",
        "icon": "feast",
        "lore": "N'aix was a wizard's experiment gone wrong. Now he escapes only through feeding on the life essence of others.",
        "baseStats": {
            "maxHp": 130, "maxMana": 60, "hpPerLevel": 30, "manaPerLevel": 14,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "rage": {
                "name": "Rage",
                "type": "active",
                "description": "Lifestealer becomes spell immune and gains bonus attack speed.",
                "attackSpeedBonus": 80, "duration": 6000, "cooldown": 16000, "manaCost": 20
            },
            "feast": {
                "name": "Feast",
                "type": "passive",
                "description": "Lifestealer's attacks deal bonus damage based on the target's current HP and heals him.",
                "lifestealPercent": 3, "damagePercent": 1.5
            },
            "ghoulFrenzy": {
                "name": "Ghoul Frenzy",
                "type": "passive",
                "description": "Passively grants Lifestealer bonus attack speed and slow on attacks.",
                "attackSpeedBonus": 30, "slowPercent": 15, "slowDuration": 1500
            },
            "infest": {
                "name": "Infest",
                "type": "ultimate",
                "description": "Lifestealer hides inside a target unit. When he emerges, he damages nearby enemies.",
                "damage": 200, "healPercent": 100, "radius": 5,
                "cooldown": 50000, "manaCost": 40, "range": 3
            }
        },
        "talents": {
            "10": ["+25 Movement Speed", "+30 Damage"],
            "15": ["+350 Health", "+25 Attack Speed"],
            "20": ["+1% Feast Lifesteal", "+1.5s Rage Duration"],
            "25": ["+1.5% Feast Damage", "Infest Increases Infested Unit MS"]
        }
    },
    "lina": {
        "name": "Lina",
        "title": "Slayer",
        "attr": "intelligence",
        "icon": "fire",
        "lore": "Lina was born with a fire within her that grew stronger each day. She learned to wield flames with deadly precision.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 20, "manaPerLevel": 28,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "dragonSlave": {
                "name": "Dragon Slave",
                "type": "active",
                "description": "Sends a wave of fire that damages all enemies in a line.",
                "damage": 50, "range": 12, "width": 4,
                "cooldown": 8000, "manaCost": 25
            },
            "lightStrikeArray": {
                "name": "Light Strike Array",
                "type": "active",
                "description": "Calls down a pillar of flame that stuns and damages enemies in an area.",
                "damage": 40, "stunDuration": 2000, "delay": 500, "radius": 4,
                "cooldown": 10000, "manaCost": 25, "range": 10
            },
            "fieryaoul": {
                "name": "Fiery Soul",
                "type": "passive",
                "description": "Each spell cast grants Lina bonus attack and movement speed for a duration.",
                "attackSpeedPerStack": 20, "moveSpeedPerStack": 4, "maxStacks": 7, "duration": 10000
            },
            "lagunaBlade": {
                "name": "Laguna Blade",
                "type": "ultimate",
                "description": "Fires a bolt of lightning that deals massive damage to a single target.",
                "damage": 150, "cooldown": 40000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+30 Damage", "+25 Movement Speed"],
            "15": ["+100 Light Strike Array Damage", "-1.5s Dragon Slave Cooldown"],
            "20": ["+150 Dragon Slave Damage", "+30/2% Fiery Soul AS/MS"],
            "25": ["+200 Laguna Blade Damage", "Laguna Blade Pure and Pierces Immunity"]
        }
    },
    "lone_druid": {
        "name": "Lone Druid",
        "title": "Sylla",
        "attr": "universal",
        "icon": "bear",
        "lore": "Sylla the Lone Druid is one with nature. His spirit bear fights alongside him as a powerful extension of his will.",
        "baseStats": {
            "maxHp": 90, "maxMana": 80, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "spiritBear": {
                "name": "Summon Spirit Bear",
                "type": "active",
                "description": "Summons a powerful spirit bear that can carry items and attack enemies.",
                "bearHP": 300, "bearDamage": 35, "bearArmor": 5, "duration": 0,
                "cooldown": 120000, "manaCost": 50
            },
            "spiritLink": {
                "name": "Spirit Link",
                "type": "passive",
                "description": "Lone Druid and his bear share a portion of damage and attack speed.",
                "sharedDamagePercent": 30, "sharedAttackSpeed": 30
            },
            "savageRoar": {
                "name": "Savage Roar",
                "type": "active",
                "description": "Both Lone Druid and his bear roar, causing nearby enemies to flee in fear.",
                "fearDuration": 2000, "radius": 5, "cooldown": 28000, "manaCost": 25
            },
            "trueForm": {
                "name": "True Form",
                "type": "ultimate",
                "description": "Transforms into a powerful bear form with bonus HP, armor, and melee attacks.",
                "bonusHP": 500, "bonusArmor": 8, "battleCryBonus": 40, "cooldown": 0
            }
        },
        "talents": {
            "10": ["+200 Spirit Bear HP", "+20 Spirit Bear Damage"],
            "15": ["+15% Savage Roar MS", "+10 Spirit Bear Armor"],
            "20": ["-30s True Form Cooldown", "+1000 True Form HP"],
            "25": ["+40 Battle Cry Bonus", "-0.15s Spirit Bear BAT"]
        }
    },
    "luna": {
        "name": "Luna",
        "title": "Moon Rider",
        "attr": "agility",
        "icon": "moon",
        "lore": "Luna rides her tiger mount, fighting for the goddess Selemene. Her glaives and moonbeams are deadly.",
        "baseStats": {
            "maxHp": 85, "maxMana": 80, "hpPerLevel": 21, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 12, "attackRange": 8, "attackSpeed": 1.3
        },
        "abilities": {
            "lucentBeam": {
                "name": "Lucent Beam",
                "type": "active",
                "description": "Calls a beam of lunar energy to damage and mini-stun a target.",
                "damage": 45, "ministun": 600, "cooldown": 6000, "manaCost": 20, "range": 10
            },
            "moonGlaives": {
                "name": "Moon Glaives",
                "type": "passive",
                "description": "Luna's glaives bounce between enemies, dealing reduced damage with each bounce.",
                "bounces": 6, "damageReductionPercent": 35
            },
            "lunarBlessing": {
                "name": "Lunar Blessing",
                "type": "passive",
                "description": "Grants bonus damage to Luna and nearby allies, plus extra night vision.",
                "bonusDamage": 30, "radius": 10, "nightVisionBonus": 8
            },
            "eclipse": {
                "name": "Eclipse",
                "type": "ultimate",
                "description": "Calls down a barrage of moon beams that strike nearby enemies randomly.",
                "beamDamage": 50, "beamCount": 10, "duration": 4000, "radius": 6,
                "cooldown": 100000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Damage", "+300 Cast Range"],
            "15": ["+100 Lucent Beam Damage", "+20 Movement Speed"],
            "20": ["-15s Eclipse Cooldown", "+30 Lunar Blessing Damage"],
            "25": ["+0.3s Eclipse Lucent Beam Stun", "+1 Moon Glaive Bounce"]
        }
    },
    "lycan": {
        "name": "Lycan",
        "title": "Banehallow",
        "attr": "universal",
        "icon": "wolf",
        "lore": "Banehallow was once a noble, but was cursed by the moon to become the Lycan. He embraced his wolf nature.",
        "baseStats": {
            "maxHp": 120, "maxMana": 70, "hpPerLevel": 28, "manaPerLevel": 15,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "summonWolves": {
                "name": "Summon Wolves",
                "type": "active",
                "description": "Summons two wolves to fight alongside Lycan. Wolves gain abilities at higher levels.",
                "wolfDamage": 25, "wolfHP": 150, "duration": 50000,
                "cooldown": 30000, "manaCost": 30
            },
            "howl": {
                "name": "Howl",
                "type": "active",
                "description": "Grants bonus damage to Lycan, his wolves, and nearby allies.",
                "bonusDamage": 30, "duration": 8000, "radius": 999,
                "cooldown": 24000, "manaCost": 20
            },
            "feralImpulse": {
                "name": "Feral Impulse",
                "type": "passive",
                "description": "Grants Lycan and his units bonus attack damage and health regeneration.",
                "damagePercent": 20, "hpRegen": 8, "radius": 10
            },
            "shapeshift": {
                "name": "Shapeshift",
                "type": "ultimate",
                "description": "Lycan transforms into a wolf with maximum movement speed, critical strike, and night vision.",
                "critChance": 40, "critMultiplier": 1.8, "duration": 25000,
                "cooldown": 110000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+15 Damage", "+8 Feral Impulse HP Regen"],
            "15": ["+10s Shapeshift Duration", "+14% Feral Impulse Damage"],
            "20": ["+400 Howl Hero Damage", "+2 Wolves Summoned"],
            "25": ["+30% Shapeshift Critical Strike", "+25s Summon Wolves Duration"]
        }
    },
    "magnus": {
        "name": "Magnus",
        "title": "Magnataur",
        "attr": "strength",
        "icon": "rhino",
        "lore": "Magnus is the last of the Magnataurs, an ancient race of centaur-like creatures with incredible strength.",
        "baseStats": {
            "maxHp": 125, "maxMana": 85, "hpPerLevel": 29, "manaPerLevel": 18,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "shockwave": {
                "name": "Shockwave",
                "type": "active",
                "description": "Sends a wave of force in a line, damaging enemies and pulling them toward Magnus.",
                "damage": 40, "pullDistance": 2, "range": 12, "width": 3,
                "cooldown": 9000, "manaCost": 20
            },
            "empower": {
                "name": "Empower",
                "type": "active",
                "description": "Grants an ally bonus damage and cleave on their attacks.",
                "bonusDamagePercent": 25, "cleavePercent": 50, "duration": 35000,
                "cooldown": 12000, "manaCost": 20, "range": 8
            },
            "skewer": {
                "name": "Skewer",
                "type": "active",
                "description": "Magnus charges forward, dragging enemies to his destination.",
                "damage": 35, "slowPercent": 40, "slowDuration": 3000, "range": 10,
                "cooldown": 18000, "manaCost": 25
            },
            "reversePolarity": {
                "name": "Reverse Polarity",
                "type": "ultimate",
                "description": "Pulls all enemies in front of Magnus toward him and stuns them.",
                "damage": 50, "stunDuration": 3000, "radius": 5,
                "cooldown": 120000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+15 Damage", "+12% Empower Damage/Cleave"],
            "15": ["+10 Strength", "+100 Shockwave Damage"],
            "20": ["+12% Empower Damage/Cleave", "+1s Reverse Polarity Stun Duration"],
            "25": ["+1000 Skewer Range", "Reverse Polarity Affects Buildings"]
        }
    },
    "marci": {
        "name": "Marci",
        "title": "Faithful Sidekick",
        "attr": "universal",
        "icon": "fist",
        "lore": "Marci communicates through actions rather than words. Her strength and loyalty are unmatched.",
        "baseStats": {
            "maxHp": 115, "maxMana": 75, "hpPerLevel": 27, "manaPerLevel": 16,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "dispose": {
                "name": "Dispose",
                "type": "active",
                "description": "Marci grabs an ally or enemy and throws them, damaging and stunning enemies in the landing area.",
                "damage": 50, "stunDuration": 2000, "radius": 4,
                "cooldown": 16000, "manaCost": 25, "range": 4
            },
            "rebound": {
                "name": "Rebound",
                "type": "active",
                "description": "Marci bounds toward a unit then leaps to a target location, damaging and slowing enemies.",
                "damage": 40, "slowPercent": 50, "slowDuration": 3000, "radius": 4,
                "cooldown": 14000, "manaCost": 20, "range": 8
            },
            "sidekick": {
                "name": "Sidekick",
                "type": "active",
                "description": "Marci buffs an ally with lifesteal and attack damage for a duration.",
                "lifestealPercent": 30, "bonusDamage": 20, "duration": 6000,
                "cooldown": 18000, "manaCost": 20, "range": 8
            },
            "unleash": {
                "name": "Unleash",
                "type": "ultimate",
                "description": "Marci gains pulse waves that deal damage around her and boost her movement speed.",
                "pulseDamage": 30, "pulseInterval": 1500, "moveSpeedBonus": 20, "duration": 16000,
                "cooldown": 80000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+50 Dispose Damage", "+0.5s Rebound Stun Duration"],
            "15": ["+1s Dispose Stun Duration", "+75 Rebound Damage"],
            "20": ["-7s Unleash Cooldown", "+1.5s Sidekick Duration"],
            "25": ["+35 Unleash Pulse Damage", "Sidekick Grants Spell Immunity"]
        }
    },
    "mars": {
        "name": "Mars",
        "title": "God of War",
        "attr": "strength",
        "icon": "shield",
        "lore": "Mars is the god of war, son of heaven. He fights not for glory, but for the love of battle itself.",
        "baseStats": {
            "maxHp": 135, "maxMana": 75, "hpPerLevel": 31, "manaPerLevel": 16,
            "baseDamage": 20, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "spearOfMars": {
                "name": "Spear of Mars",
                "type": "active",
                "description": "Mars throws his spear, damaging enemies. The first hero hit is knocked back and pinned to terrain.",
                "damage": 50, "stunDuration": 2000, "knockbackDistance": 5, "range": 12,
                "cooldown": 14000, "manaCost": 25
            },
            "godsRebuke": {
                "name": "God's Rebuke",
                "type": "active",
                "description": "Mars smashes enemies in front of him, dealing critical damage and knocking them back.",
                "critMultiplier": 2.0, "knockback": 3, "radius": 5,
                "cooldown": 10000, "manaCost": 20
            },
            "bulwark": {
                "name": "Bulwark",
                "type": "passive",
                "description": "Mars takes reduced damage from the front and sides. Can be activated to redirect attacks.",
                "frontReduction": 60, "sideReduction": 30, "activeDuration": 4000
            },
            "arenaOfBlood": {
                "name": "Arena of Blood",
                "type": "ultimate",
                "description": "Mars creates an arena where enemies can't leave. Soldiers attack anyone trying to escape.",
                "damage": 30, "duration": 6000, "radius": 8,
                "cooldown": 60000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+8 Strength", "+35 Spear Damage"],
            "15": ["+20 God's Rebuke Crit", "+120 God's Rebuke Damage"],
            "20": ["+2s Arena Of Blood Duration", "+0.8s Spear Stun Duration"],
            "25": ["God's Rebuke Applies Bulwark", "+1.5s Arena Of Blood Stun"]
        }
    },
    "medusa": {
        "name": "Medusa",
        "title": "Gorgon",
        "attr": "agility",
        "icon": "snake",
        "lore": "Medusa was once a beautiful woman, transformed by jealous gods into a monster. Her gaze turns enemies to stone.",
        "baseStats": {
            "maxHp": 90, "maxMana": 100, "hpPerLevel": 22, "manaPerLevel": 22,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "splitShot": {
                "name": "Split Shot",
                "type": "toggle",
                "description": "Medusa's arrows split to hit multiple targets at reduced damage.",
                "additionalTargets": 4, "damageReduction": 40
            },
            "mysticSnake": {
                "name": "Mystic Snake",
                "type": "active",
                "description": "A snake that bounces between enemies, stealing mana and dealing increasing damage.",
                "damage": 30, "manaSteal": 15, "bounces": 6, "damageIncrease": 20,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "manaShield": {
                "name": "Mana Shield",
                "type": "toggle",
                "description": "Creates a shield that uses mana to absorb damage.",
                "damageAbsorb": 60, "manaPerDamage": 1.6
            },
            "stoneGaze": {
                "name": "Stone Gaze",
                "type": "ultimate",
                "description": "Enemies facing Medusa slowly turn to stone, becoming stunned and taking bonus physical damage.",
                "stunDuration": 3000, "physicalDamageBonus": 50, "duration": 6000, "radius": 8,
                "cooldown": 80000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+15 Damage", "+15% Mystic Snake Mana Steal"],
            "15": ["+25 Attack Speed", "+1 Mystic Snake Bounce"],
            "20": ["+20% Mana Shield", "-3s Mystic Snake Cooldown"],
            "25": ["+1.5s Stone Gaze Duration", "Split Shot Uses Modifiers"]
        }
    },
    "meepo": {
        "name": "Meepo",
        "title": "Geomancer",
        "attr": "agility",
        "icon": "shovel",
        "lore": "Meepo is a scoundrel who discovered an artifact that split him into multiple selves. If one dies, all die.",
        "baseStats": {
            "maxHp": 95, "maxMana": 75, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "earthbind": {
                "name": "Earthbind",
                "type": "active",
                "description": "Throws a net that roots enemies in place.",
                "rootDuration": 2000, "radius": 3, "cooldown": 8000, "manaCost": 15, "range": 10
            },
            "poof": {
                "name": "Poof",
                "type": "active",
                "description": "Teleports Meepo to another Meepo, dealing damage at both locations.",
                "damage": 40, "radius": 4, "channelTime": 1500,
                "cooldown": 6000, "manaCost": 15
            },
            "ransack": {
                "name": "Ransack",
                "type": "passive",
                "description": "Each Meepo's attacks steal HP from enemies.",
                "hpSteal": 15
            },
            "dividedWeStand": {
                "name": "Divided We Stand",
                "type": "ultimate",
                "description": "Meepo summons additional clones of himself that share experience but not items.",
                "clones": 3, "cloneStatShare": 80
            }
        },
        "talents": {
            "10": ["+8 Strength", "+20 Poof Damage"],
            "15": ["+10% Lifesteal", "+5 Ransack Damage/Heal"],
            "20": ["+400 Health", "+30% Evasion"],
            "25": ["+5s Earthbind Duration", "+600 Poof Damage"]
        }
    },
    "mirana": {
        "name": "Mirana",
        "title": "Princess of the Moon",
        "attr": "universal",
        "icon": "arrow",
        "lore": "Mirana is the chosen servant of Selemene, goddess of the moon. She rides her tiger mount into battle.",
        "baseStats": {
            "maxHp": 90, "maxMana": 90, "hpPerLevel": 22, "manaPerLevel": 20,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "starstorm": {
                "name": "Starstorm",
                "type": "active",
                "description": "Calls down stars that damage nearby enemies. A second star hits the closest enemy.",
                "damage": 40, "secondHitDamage": 25, "radius": 6,
                "cooldown": 12000, "manaCost": 25
            },
            "sacredArrow": {
                "name": "Sacred Arrow",
                "type": "active",
                "description": "Fires a long-range arrow that stuns and damages. Stun duration increases with distance.",
                "maxDamage": 120, "maxStun": 5000, "maxDistance": 20,
                "cooldown": 18000, "manaCost": 30, "range": 25
            },
            "leap": {
                "name": "Leap",
                "type": "active",
                "description": "Mirana and her tiger leap forward, granting bonus attack and movement speed.",
                "distance": 10, "attackSpeedBonus": 80, "moveSpeedBonus": 20, "buffDuration": 4000,
                "cooldown": 22000, "manaCost": 20
            },
            "moonlightShadow": {
                "name": "Moonlight Shadow",
                "type": "ultimate",
                "description": "Makes all allied heroes invisible. Attacking breaks invisibility briefly.",
                "duration": 15000, "fadeDelay": 2500,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Damage", "+100 Leap Distance"],
            "15": ["+1 Sacred Arrow", "+30% Leap Bonus Attack Speed"],
            "20": ["+100 Starstorm Damage", "-50 Moonlight Shadow Cooldown"],
            "25": ["Starstorm Attacks Proc Modifiers", "+2 Multishot Sacred Arrows"]
        }
    },
    "monkey_king": {
        "name": "Monkey King",
        "title": "Sun Wukong",
        "attr": "agility",
        "icon": "monkey",
        "lore": "Sun Wukong, the Monkey King, is a trickster born from a stone. He wields an enchanted staff that can change size.",
        "baseStats": {
            "maxHp": 95, "maxMana": 75, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 3, "attackSpeed": 1.2
        },
        "abilities": {
            "boundlessStrike": {
                "name": "Boundless Strike",
                "type": "active",
                "description": "Monkey King slams his staff, stunning and dealing critical damage in a line.",
                "critMultiplier": 2.0, "stunDuration": 1200, "range": 10,
                "cooldown": 20000, "manaCost": 25
            },
            "treesDance": {
                "name": "Tree Dance",
                "type": "active",
                "description": "Jumps to a tree, gaining unobstructed vision. Attacks from trees deal bonus damage.",
                "bonusDamage": 60, "visionBonus": 8, "cooldown": 1000, "range": 10
            },
            "jinguMastery": {
                "name": "Jingu Mastery",
                "type": "passive",
                "description": "Attacks on the same target grant bonus damage and lifesteal on the next four attacks.",
                "requiredHits": 4, "bonusDamage": 80, "lifestealPercent": 30, "chargedAttacks": 4
            },
            "wukongsCommand": {
                "name": "Wukong's Command",
                "type": "ultimate",
                "description": "Creates a circular formation of soldiers that attack enemies within the ring.",
                "soldierDamagePercent": 90, "duration": 13000, "radius": 6,
                "cooldown": 100000, "manaCost": 60, "range": 10
            }
        },
        "talents": {
            "10": ["+300 Tree Dance Cast Range", "+75 Jingu Mastery Damage"],
            "15": ["+75 Boundless Strike Damage", "+30% Jingu Mastery Lifesteal"],
            "20": ["+0.5s Boundless Strike Stun", "+100 Wukong's Command Attack Range"],
            "25": ["Extra Wukong's Command Ring", "+350% Boundless Strike Crit"]
        }
    },
    "morphling": {
        "name": "Morphling",
        "title": "Water Elemental",
        "attr": "agility",
        "icon": "water",
        "lore": "Morphling is a water elemental who can shift his form between strength and agility at will.",
        "baseStats": {
            "maxHp": 90, "maxMana": 90, "hpPerLevel": 22, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.3
        },
        "abilities": {
            "waveform": {
                "name": "Waveform",
                "type": "active",
                "description": "Morphling becomes a wave of water, damaging enemies as he passes through them.",
                "damage": 50, "range": 12, "cooldown": 11000, "manaCost": 25
            },
            "adaptiveStrike": {
                "name": "Adaptive Strike",
                "type": "active",
                "description": "Damages and stuns or damages and knocks back based on Morphling's stats.",
                "damage": 40, "stunDuration": 2500, "knockbackDistance": 5,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "attributeShift": {
                "name": "Attribute Shift",
                "type": "toggle",
                "description": "Morphling can shift points between strength and agility.",
                "shiftRate": 5
            },
            "replicate": {
                "name": "Replicate",
                "type": "ultimate",
                "description": "Creates an illusion of a target hero. Morphling can morph into this illusion.",
                "illusionDamage": 50, "illusionDuration": 30000,
                "cooldown": 80000, "manaCost": 50, "range": 12
            }
        },
        "talents": {
            "10": ["+10 Agility", "+300 Waveform Range"],
            "15": ["+15s Morph Duration", "+15 Waveform Damage"],
            "20": ["Waveform Attacks", "-4s Adaptive Strike Cooldown"],
            "25": ["2 Waveform Charges", "+3 Multishot Adaptive Strike"]
        }
    },
    "muerta": {
        "name": "Muerta",
        "title": "Master of Death",
        "attr": "intelligence",
        "icon": "skull",
        "lore": "Muerta was a revolutionary who was executed and returned as the Master of Death, wielding spectral guns.",
        "baseStats": {
            "maxHp": 85, "maxMana": 110, "hpPerLevel": 21, "manaPerLevel": 24,
            "baseDamage": 15, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "deadShot": {
                "name": "Dead Shot",
                "type": "active",
                "description": "Fires a spectral bullet that bounces off terrain, fearing and damaging enemies.",
                "damage": 45, "fearDuration": 1500, "slowPercent": 30,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "theCallings": {
                "name": "The Calling",
                "type": "active",
                "description": "Summons spirits that slow enemies and damage them based on attack damage.",
                "damagePerSpirit": 25, "slowPercent": 25, "duration": 6000, "radius": 5,
                "cooldown": 20000, "manaCost": 30, "range": 10
            },
            "gunslinger": {
                "name": "Gunslinger",
                "type": "passive",
                "description": "Muerta's attacks have a chance to fire an extra bullet at a random visible enemy.",
                "procChance": 25, "bonusTargets": 1
            },
            "pierceTheVeil": {
                "name": "Pierce the Veil",
                "type": "ultimate",
                "description": "Muerta enters the spirit world, becoming ethereal. Her attacks become magical and can't miss.",
                "bonusDamage": 100, "duration": 8000,
                "cooldown": 75000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+15 Dead Shot Damage"],
            "15": ["+25 Attack Speed", "+8% The Calling Slow"],
            "20": ["+1 Gunslinger Target", "+60 Dead Shot Damage"],
            "25": ["+4s Pierce the Veil Duration", "The Calling Silences"]
        }
    },
    "naga_siren": {
        "name": "Naga Siren",
        "title": "Slithice",
        "attr": "agility",
        "icon": "siren",
        "lore": "Slithice is a warrior of the deep, fighting to restore her people's honor. Her voice and illusions are deadly.",
        "baseStats": {
            "maxHp": 90, "maxMana": 90, "hpPerLevel": 22, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "mirrorImage": {
                "name": "Mirror Image",
                "type": "active",
                "description": "Creates illusions of Naga Siren that deal damage and take increased damage.",
                "illusionCount": 3, "illusionDamage": 30, "illusionDamageTaken": 350, "duration": 26000,
                "cooldown": 40000, "manaCost": 30
            },
            "ensnare": {
                "name": "Ensnare",
                "type": "active",
                "description": "Interrupts and roots a target enemy, preventing movement and invisibility.",
                "rootDuration": 3500, "cooldown": 14000, "manaCost": 25, "range": 8
            },
            "riptide": {
                "name": "Rip Tide",
                "type": "active",
                "description": "Naga and her illusions create a wave that damages enemies and reduces their armor.",
                "damage": 35, "armorReduction": 4, "duration": 4000, "radius": 4,
                "cooldown": 10000, "manaCost": 20
            },
            "songOfTheSiren": {
                "name": "Song of the Siren",
                "type": "ultimate",
                "description": "Puts all enemies in range to sleep, making them invulnerable but unable to act.",
                "duration": 7000, "radius": 10, "healPercent": 0,
                "cooldown": 160000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+10 Strength", "+15 Damage"],
            "15": ["+10% Mirror Image Damage", "+1s Ensnare Duration"],
            "20": ["-5s Mirror Image Cooldown", "+2 Armor Corruption"],
            "25": ["-50s Song of the Siren Cooldown", "+1 Mirror Image Illusion"]
        }
    },
    "natures_prophet": {
        "name": "Nature's Prophet",
        "title": "Tequoia",
        "attr": "intelligence",
        "icon": "tree",
        "lore": "Nature's Prophet is a powerful druid who can teleport anywhere and summon armies of treants.",
        "baseStats": {
            "maxHp": 85, "maxMana": 110, "hpPerLevel": 21, "manaPerLevel": 24,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "sprout": {
                "name": "Sprout",
                "type": "active",
                "description": "Creates a ring of trees around a target, trapping them inside.",
                "duration": 4000, "cooldown": 8000, "manaCost": 20, "range": 10
            },
            "teleportation": {
                "name": "Teleportation",
                "type": "active",
                "description": "Teleports to any point on the map after a channeling delay.",
                "channelTime": 3000, "cooldown": 50000, "manaCost": 35, "range": 999
            },
            "naturesCall": {
                "name": "Nature's Call",
                "type": "active",
                "description": "Converts trees into treant warriors that attack enemies.",
                "treantCount": 5, "treantDamage": 25, "treantHP": 150, "duration": 50000,
                "cooldown": 30000, "manaCost": 30, "range": 8
            },
            "wrathOfNature": {
                "name": "Wrath of Nature",
                "type": "ultimate",
                "description": "Sends a bolt of energy bouncing between enemies, dealing increasing damage.",
                "baseDamage": 60, "damagePerBounce": 10, "bounces": 16,
                "cooldown": 60000, "manaCost": 50, "range": 999
            }
        },
        "talents": {
            "10": ["+30 Damage", "+3 Treants"],
            "15": ["-2.5s Sprout Cooldown", "+40 Treant Damage"],
            "20": ["+8 Treant Armor", "-25s Wrath of Nature Cooldown"],
            "25": ["Teleportation Creates Treants", "Removed Teleportation Cooldown"]
        }
    },
    "necrophos": {
        "name": "Necrophos",
        "title": "Rotund'jere",
        "attr": "intelligence",
        "icon": "plague",
        "lore": "Necrophos spreads disease and pestilence wherever he goes. His very presence saps the life from enemies.",
        "baseStats": {
            "maxHp": 95, "maxMana": 120, "hpPerLevel": 24, "manaPerLevel": 26,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "deathPulse": {
                "name": "Death Pulse",
                "type": "active",
                "description": "Releases a wave that damages enemies and heals allies.",
                "damage": 40, "heal": 40, "radius": 5,
                "cooldown": 8000, "manaCost": 20
            },
            "ghostShroud": {
                "name": "Ghost Shroud",
                "type": "active",
                "description": "Necrophos becomes ethereal, slowing himself but gaining increased healing and magic resistance.",
                "slowSelf": 15, "healAmpPercent": 75, "magicResist": 35, "duration": 4000,
                "cooldown": 20000, "manaCost": 25
            },
            "hearthstopper": {
                "name": "Heartstopper Aura",
                "type": "passive",
                "description": "Necrophos's aura damages enemies based on their max HP.",
                "damagePercent": 1.0, "radius": 8
            },
            "reapersScythe": {
                "name": "Reaper's Scythe",
                "type": "ultimate",
                "description": "Stuns a target and deals damage based on how much HP they're missing. Kills add to respawn time.",
                "damagePerMissingHP": 1.2, "stunDuration": 1500, "respawnPenalty": 20,
                "cooldown": 80000, "manaCost": 50, "range": 8
            }
        },
        "talents": {
            "10": ["+30 Damage", "+20% Ghost Shroud Slow/Heal"],
            "15": ["-2s Death Pulse Cooldown", "+0.8% Heartstopper Aura"],
            "20": ["+100 Death Pulse Heal", "+20 Reaper's Scythe Respawn Time"],
            "25": ["Death Pulse Spawns Ghost", "+0.8 Reaper's Scythe Damage/Missing HP"]
        }
    },
    "night_stalker": {
        "name": "Night Stalker",
        "title": "Balanar",
        "attr": "strength",
        "icon": "night",
        "lore": "Balanar hunts only at night, when his power is at its peak. During the day, he waits in darkness.",
        "baseStats": {
            "maxHp": 130, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 19, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "void_ns": {
                "name": "Void",
                "type": "active",
                "description": "Deals damage and slows. At night, ministuns and slows for longer.",
                "damage": 40, "daySlowPercent": 25, "nightSlowPercent": 50, "nightMinistun": 300, "duration": 3000,
                "cooldown": 8000, "manaCost": 20, "range": 8
            },
            "cripplingFear": {
                "name": "Crippling Fear",
                "type": "active",
                "description": "Silences enemies in an area. At night, the duration is longer.",
                "daySilence": 3000, "nightSilence": 6000, "radius": 4,
                "cooldown": 12000, "manaCost": 25, "range": 8
            },
            "hunterInTheNight": {
                "name": "Hunter in the Night",
                "type": "passive",
                "description": "Night Stalker gains bonus attack speed and movement speed at night.",
                "attackSpeedBonus": 60, "moveSpeedBonus": 30
            },
            "darkAscension": {
                "name": "Dark Ascension",
                "type": "ultimate",
                "description": "Night Stalker transforms, gaining flying movement and turning day into night.",
                "bonusDamage": 50, "duration": 30000, "flySpeed": 20,
                "cooldown": 120000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Damage", "+200 Health"],
            "15": ["+40 Hunter in the Night Attack Speed", "+25 Void Damage"],
            "20": ["+30% Lifesteal", "+1.5s Crippling Fear Duration"],
            "25": ["-50s Dark Ascension Cooldown", "+200 Void AoE"]
        }
    },
    "nyx_assassin": {
        "name": "Nyx Assassin",
        "title": "Anub'arak",
        "attr": "agility",
        "icon": "beetle",
        "lore": "Nyx Assassin serves Nyx, goddess of the night. He waits in shadows before striking with precision.",
        "baseStats": {
            "maxHp": 100, "maxMana": 90, "hpPerLevel": 25, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "impale": {
                "name": "Impale",
                "type": "active",
                "description": "Sends a row of spikes that stun and damage enemies.",
                "damage": 40, "stunDuration": 2000, "range": 10, "width": 3,
                "cooldown": 14000, "manaCost": 25
            },
            "manaBurn": {
                "name": "Mana Burn",
                "type": "active",
                "description": "Burns mana from an enemy based on their intelligence, dealing damage equal to mana burned.",
                "manaMultiplier": 5, "cooldown": 16000, "manaCost": 20, "range": 8
            },
            "spikedCarapace": {
                "name": "Spiked Carapace",
                "type": "active",
                "description": "Nyx's shell hardens, reflecting and stunning the next source of damage.",
                "stunDuration": 2000, "duration": 2000, "cooldown": 20000, "manaCost": 20
            },
            "vendetta": {
                "name": "Vendetta",
                "type": "ultimate",
                "description": "Nyx becomes invisible with bonus movement speed. His next attack deals massive bonus damage.",
                "bonusDamage": 250, "moveSpeedBonus": 25, "duration": 60000,
                "cooldown": 70000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+60 Impale Damage", "+8% Spell Amplification"],
            "15": ["+100 Vendetta Damage", "-30s Vendetta Cooldown"],
            "20": ["+100 Mana Burn Multiplier", "+1s Spiked Carapace Reflect Duration"],
            "25": ["+0.6s Impale Stun Duration", "Burrow"]
        }
    },
    "ogre_magi": {
        "name": "Ogre Magi",
        "title": "Aggron Stonebreak",
        "attr": "strength",
        "icon": "ogre",
        "lore": "Two-headed ogres are rare, but Aggron Stonebreak is rarer still - he's actually intelligent. Sometimes.",
        "baseStats": {
            "maxHp": 140, "maxMana": 80, "hpPerLevel": 32, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "fireblast": {
                "name": "Fireblast",
                "type": "active",
                "description": "Blasts a target with fire, stunning and damaging them.",
                "damage": 40, "stunDuration": 1500, "cooldown": 10000, "manaCost": 20, "range": 8
            },
            "ignite": {
                "name": "Ignite",
                "type": "active",
                "description": "Hurls an ignitable substance that slows and deals damage over time.",
                "damage": 10, "damagePerSecond": 15, "slowPercent": 25, "duration": 5000,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "bloodlust": {
                "name": "Bloodlust",
                "type": "active",
                "description": "Incites an ally into a frenzy, granting bonus attack and movement speed.",
                "attackSpeedBonus": 60, "moveSpeedBonus": 15, "duration": 20000,
                "cooldown": 15000, "manaCost": 20, "range": 8
            },
            "multicast": {
                "name": "Multicast",
                "type": "ultimate",
                "description": "Gives Ogre Magi's spells a chance to cast multiple times.",
                "x2Chance": 75, "x3Chance": 30, "x4Chance": 15
            }
        },
        "talents": {
            "10": ["+90 Fireblast Damage", "+20 Movement Speed"],
            "15": ["+350 Health", "+30 Bloodlust Attack Speed"],
            "20": ["+40 Ignite DPS", "+6% Multicast Chance"],
            "25": ["+275 Fireblast Damage", "Bloodlust Grants +50 Damage"]
        }
    },
    "omniknight": {
        "name": "Omniknight",
        "title": "Purist Thunderwrath",
        "attr": "strength",
        "icon": "knight",
        "lore": "Purist Thunderwrath serves the Omniscience, a deity of order. His protective magic shields allies.",
        "baseStats": {
            "maxHp": 130, "maxMana": 75, "hpPerLevel": 30, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "purification": {
                "name": "Purification",
                "type": "active",
                "description": "Heals an ally while damaging nearby enemies.",
                "heal": 80, "damage": 80, "radius": 4,
                "cooldown": 11000, "manaCost": 25, "range": 8
            },
            "heavenlyGrace": {
                "name": "Heavenly Grace",
                "type": "active",
                "description": "Grants an ally bonus strength and status resistance.",
                "bonusStrength": 20, "statusResist": 50, "duration": 8000,
                "cooldown": 16000, "manaCost": 20, "range": 8
            },
            "hammerOfPurity": {
                "name": "Hammer of Purity",
                "type": "passive",
                "description": "Omniknight's attacks heal him based on the damage dealt to non-hero units.",
                "healPercent": 50, "heroDamageCooldown": 6000
            },
            "guardianAngel": {
                "name": "Guardian Angel",
                "type": "ultimate",
                "description": "Grants physical damage immunity to all nearby allies.",
                "duration": 6000, "radius": 999,
                "cooldown": 140000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+50 Purification Damage/Heal", "+20 Movement Speed"],
            "15": ["+100 Hammer of Purity Damage", "+15% Heavenly Grace Status Resistance"],
            "20": ["-3s Purification Cooldown", "+15 Strength"],
            "25": ["+2s Guardian Angel Duration", "+200 Purification Damage/Heal"]
        }
    },
    "oracle": {
        "name": "Oracle",
        "title": "Nerif",
        "attr": "intelligence",
        "icon": "oracle",
        "lore": "Nerif the Oracle can see all possible futures. His magic can save allies from death or doom enemies.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 20, "manaPerLevel": 28,
            "baseDamage": 13, "damagePerLevel": 2.6, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "fortunesEnd": {
                "name": "Fortune's End",
                "type": "active",
                "description": "Channels and releases a bolt that damages and roots enemies in an area.",
                "damage": 30, "rootDuration": 2500, "maxChannelTime": 2500, "radius": 4,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "fatesEdict": {
                "name": "Fate's Edict",
                "type": "active",
                "description": "Disarms a target but grants them 100% magic resistance.",
                "duration": 4000, "cooldown": 14000, "manaCost": 20, "range": 8
            },
            "purifyingFlames": {
                "name": "Purifying Flames",
                "type": "active",
                "description": "Burns a target for heavy damage, then heals them for more over time.",
                "damage": 90, "healPerSecond": 15, "healDuration": 9000,
                "cooldown": 2500, "manaCost": 20, "range": 8
            },
            "falsesPromise": {
                "name": "False Promise",
                "type": "ultimate",
                "description": "Delays all damage and healing on an ally. At the end, doubles all healing received.",
                "duration": 9000, "healMultiplier": 2.0,
                "cooldown": 80000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+25 Movement Speed", "+0.5s Fortune's End Max Duration"],
            "15": ["+100 Purifying Flames Heal/Damage", "+1s Fate's Edict Duration"],
            "20": ["+100 Cast Range", "+2s False Promise Duration"],
            "25": ["False Promise Invisibility", "-1.5s Purifying Flames Cooldown"]
        }
    },
    "outworld_destroyer": {
        "name": "Outworld Destroyer",
        "title": "Harbinger",
        "attr": "intelligence",
        "icon": "outworld",
        "lore": "One of a race of fundamental forces, Harbinger's mission is to preserve existence by preventing minds from becoming too powerful.",
        "baseStats": {
            "maxHp": 85, "maxMana": 140, "hpPerLevel": 22, "manaPerLevel": 30,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "arcaneOrb": {
                "name": "Arcane Orb",
                "type": "active",
                "description": "Adds extra pure damage based on remaining mana to each attack.",
                "manaDamagePercent": 14, "cooldown": 0, "manaCost": 20
            },
            "astralImprisonment": {
                "name": "Astral Imprisonment",
                "type": "active",
                "description": "Banishes a target to an astral prison, dealing damage on release.",
                "damage": 40, "duration": 4000, "radius": 4,
                "cooldown": 18000, "manaCost": 25, "range": 8
            },
            "essenceFlux": {
                "name": "Essence Flux",
                "type": "passive",
                "description": "Grants a chance to restore a percentage of max mana when casting.",
                "restoreChance": 30, "manaRestorePercent": 25
            },
            "sanitysEclipse": {
                "name": "Sanity's Eclipse",
                "type": "ultimate",
                "description": "Damages enemies in an area based on the difference in intelligence.",
                "damageMultiplier": 10, "radius": 8,
                "cooldown": 140000, "manaCost": 60, "range": 12
            }
        },
        "talents": {
            "10": ["+200 Mana", "+20 Attack Speed"],
            "15": ["+2s Astral Imprisonment Duration", "+15% Essence Flux Mana Restore"],
            "20": ["+50 Arcane Orb Damage", "+0.1 Sanity's Eclipse Multiplier"],
            "25": ["+20% Spell Lifesteal", "Arcane Orb Pierces Spell Immunity"]
        }
    },
    "pangolier": {
        "name": "Pangolier",
        "title": "Donté Panlin",
        "attr": "universal",
        "icon": "pangolier",
        "lore": "The Pangolier is a swashbuckler who rolls into battle with style and panache.",
        "baseStats": {
            "maxHp": 100, "maxMana": 90, "hpPerLevel": 24, "manaPerLevel": 20,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "swashbuckle": {
                "name": "Swashbuckle",
                "type": "active",
                "description": "Pangolier dashes forward and slashes enemies in a line.",
                "damage": 20, "slashes": 4, "range": 10,
                "cooldown": 12000, "manaCost": 25
            },
            "shieldCrash": {
                "name": "Shield Crash",
                "type": "active",
                "description": "Jumps and crashes down, damaging enemies and gaining damage reduction.",
                "damage": 35, "damageReductionPerHero": 8, "duration": 8000, "radius": 5,
                "cooldown": 13000, "manaCost": 20
            },
            "luckyShot": {
                "name": "Lucky Shot",
                "type": "passive",
                "description": "Attacks have a chance to disarm and slow enemies.",
                "chance": 15, "slowPercent": 30, "disarmDuration": 2000
            },
            "rollingThunder": {
                "name": "Rolling Thunder",
                "type": "ultimate",
                "description": "Pangolier curls into a ball and rolls, stunning and knocking back enemies hit.",
                "damage": 50, "stunDuration": 1500, "duration": 10000,
                "cooldown": 70000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Swashbuckle Damage", "+3 Mana Regen"],
            "15": ["+2s Rolling Thunder Duration", "+15% Shield Crash Damage Reduction"],
            "20": ["+10% Lucky Shot Chance", "-3s Shield Crash Cooldown"],
            "25": ["Swashbuckle Applies Lucky Shot", "+15% Rolling Thunder Move Speed"]
        }
    },
    "phantom_lancer": {
        "name": "Phantom Lancer",
        "title": "Azwraith",
        "attr": "agility",
        "icon": "phantom_lancer",
        "lore": "The last of the Revenant Army, Azwraith fights with an army of illusions to confuse and overwhelm foes.",
        "baseStats": {
            "maxHp": 90, "maxMana": 80, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "spiritLance": {
                "name": "Spirit Lance",
                "type": "active",
                "description": "Throws a lance at a target, damaging and slowing them while creating an illusion.",
                "damage": 35, "slowPercent": 30, "slowDuration": 3500, "illusionDamage": 20,
                "cooldown": 9000, "manaCost": 20, "range": 10
            },
            "doppelganger": {
                "name": "Doppelganger",
                "type": "active",
                "description": "Phantom Lancer briefly vanishes, reappearing with illusions.",
                "illusionCount": 2, "illusionDamage": 20, "delay": 1000,
                "cooldown": 18000, "manaCost": 25, "range": 8
            },
            "phantomRush": {
                "name": "Phantom Rush",
                "type": "passive",
                "description": "When attacking from range, charges with bonus agility.",
                "bonusAgility": 20, "duration": 2000, "minRange": 4
            },
            "juxtapose": {
                "name": "Juxtapose",
                "type": "ultimate",
                "description": "Attacks have a chance to create an illusion. Illusions can also spawn more illusions.",
                "heroChance": 50, "illusionChance": 8, "maxIllusions": 8, "illusionDuration": 8000
            }
        },
        "talents": {
            "10": ["+15 Attack Speed", "+100 Spirit Lance Damage"],
            "15": ["+250 Phantom Rush Range", "-1s Spirit Lance Cooldown"],
            "20": ["+25% Critical Strike (150%)", "+5% Juxtapose Illusion Chance"],
            "25": ["+20% Juxtapose Illusion Damage", "+2 Max Juxtapose Illusions"]
        }
    },
    "phoenix": {
        "name": "Phoenix",
        "title": "Icarus",
        "attr": "universal",
        "icon": "phoenix",
        "lore": "A celestial bird of fire, Phoenix sacrifices its own life force to burn enemies and protect allies.",
        "baseStats": {
            "maxHp": 110, "maxMana": 100, "hpPerLevel": 26, "manaPerLevel": 22,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 0.9
        },
        "abilities": {
            "icarus_dive": {
                "name": "Icarus Dive",
                "type": "active",
                "description": "Phoenix dives forward, damaging and slowing enemies. Can be canceled early.",
                "damage": 30, "slowPercent": 25, "duration": 2000, "range": 12,
                "cooldown": 26000, "hpCost": 15
            },
            "fireSpirits": {
                "name": "Fire Spirits",
                "type": "active",
                "description": "Summons fire spirits that can be launched at enemies, burning and slowing their attack speed.",
                "spiritCount": 4, "damagePerSecond": 12, "attackSpeedSlow": 80, "duration": 4000,
                "cooldown": 30000, "hpCost": 20
            },
            "sunRay": {
                "name": "Sun Ray",
                "type": "toggle",
                "description": "Channels a beam of light that damages enemies and heals allies based on max HP.",
                "damagePercent": 2.5, "healPercent": 1.5, "maxDuration": 6000,
                "cooldown": 20000, "hpCostPerSecond": 6
            },
            "supernova": {
                "name": "Supernova",
                "type": "ultimate",
                "description": "Phoenix transforms into a burning sun. If the sun survives, Phoenix is reborn with full HP and abilities reset.",
                "damagePerSecond": 50, "radius": 8, "hitsRequired": 6, "duration": 6000,
                "cooldown": 110000
            }
        },
        "talents": {
            "10": ["+15% Sun Ray HP Cost Reduction", "+350 Icarus Dive Range"],
            "15": ["+1 Fire Spirit", "+800 Fire Spirits Attack Speed Slow"],
            "20": ["+1.5% Sun Ray Damage", "+2 Supernova Hit Count"],
            "25": ["Sun Ray Always Max Range", "Fire Spirits Pierce Spell Immunity"]
        }
    },
    "primal_beast": {
        "name": "Primal Beast",
        "title": "The Beast",
        "attr": "strength",
        "icon": "primal_beast",
        "lore": "An ancient creature of pure rage, the Primal Beast was imprisoned for eons before breaking free.",
        "baseStats": {
            "maxHp": 140, "maxMana": 70, "hpPerLevel": 32, "manaPerLevel": 15,
            "baseDamage": 20, "damagePerLevel": 3.5, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "onslaught": {
                "name": "Onslaught",
                "type": "active",
                "description": "Charges forward, damaging and stunning enemies. Damage increases with distance.",
                "baseDamage": 30, "bonusDamagePerDistance": 5, "stunDuration": 1500, "maxRange": 15,
                "cooldown": 16000, "manaCost": 25
            },
            "trample": {
                "name": "Trample",
                "type": "active",
                "description": "Runs in place, damaging nearby enemies and gaining magic immunity.",
                "damagePerStep": 15, "steps": 6, "radius": 4, "duration": 3000,
                "cooldown": 18000, "manaCost": 30
            },
            "uproar": {
                "name": "Uproar",
                "type": "passive",
                "description": "Gains stacks when attacked. Can activate to deal bonus damage and slow.",
                "maxStacks": 5, "bonusDamagePerStack": 10, "slowPercent": 20, "slowDuration": 2000
            },
            "pulverize": {
                "name": "Pulverize",
                "type": "ultimate",
                "description": "Grabs an enemy and slams them repeatedly, dealing massive damage.",
                "damagePerSlam": 60, "slamCount": 3, "stunDuration": 2500,
                "cooldown": 80000, "manaCost": 50, "range": 3
            }
        },
        "talents": {
            "10": ["+5 Uproar Stack Damage", "+15 Trample Damage"],
            "15": ["+300 Onslaught Distance", "+1 Uproar Max Stacks"],
            "20": ["+1 Pulverize Slam", "+50% Trample Magic Immunity Duration"],
            "25": ["Onslaught Stuns Through Spell Immunity", "+100 Pulverize Damage"]
        }
    },
    "puck": {
        "name": "Puck",
        "title": "Faerie Dragon",
        "attr": "intelligence",
        "icon": "puck",
        "lore": "A creature of mischief and magic, Puck delights in confusing and outmaneuvering enemies.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 20, "manaPerLevel": 26,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "illusoryOrb": {
                "name": "Illusory Orb",
                "type": "active",
                "description": "Launches an orb that damages enemies. Puck can teleport to the orb's location.",
                "damage": 40, "orbSpeed": 6, "range": 14,
                "cooldown": 11000, "manaCost": 20
            },
            "waning_rift": {
                "name": "Waning Rift",
                "type": "active",
                "description": "Teleports to a location, silencing and damaging nearby enemies.",
                "damage": 35, "silenceDuration": 3000, "radius": 5,
                "cooldown": 16000, "manaCost": 25, "range": 8
            },
            "phaseShift": {
                "name": "Phase Shift",
                "type": "active",
                "description": "Puck shifts out of existence, becoming invulnerable for a short time.",
                "duration": 3000, "cooldown": 8000, "manaCost": 0
            },
            "dreamCoil": {
                "name": "Dream Coil",
                "type": "ultimate",
                "description": "Creates a coil that latches to enemies. Breaking the leash stuns and damages them.",
                "latchDamage": 25, "breakDamage": 70, "breakStun": 2500, "radius": 6, "leashRange": 8, "duration": 6000,
                "cooldown": 70000, "manaCost": 50, "range": 12
            }
        },
        "talents": {
            "10": ["+10% Spell Amplification", "+40 Waning Rift Damage"],
            "15": ["+75 Illusory Orb Damage", "+1s Waning Rift Silence"],
            "20": ["+250 Dream Coil Leash Range", "-5s Waning Rift Cooldown"],
            "25": ["+250 Dream Coil Damage", "Dream Coil Rapid Fire"]
        }
    },
    "pugna": {
        "name": "Pugna",
        "title": "Grandmaster of Oblivion",
        "attr": "intelligence",
        "icon": "pugna",
        "lore": "A master of dark magic, Pugna's life force manipulation makes him deadly to magic users.",
        "baseStats": {
            "maxHp": 75, "maxMana": 140, "hpPerLevel": 18, "manaPerLevel": 30,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "netherBlast": {
                "name": "Nether Blast",
                "type": "active",
                "description": "Creates an explosion of nether energy that damages enemies and buildings.",
                "damage": 50, "buildingDamage": 25, "radius": 5, "delay": 1000,
                "cooldown": 5500, "manaCost": 20, "range": 10
            },
            "decrepify": {
                "name": "Decrepify",
                "type": "active",
                "description": "Target becomes ethereal, taking amplified magic damage but immune to physical attacks.",
                "magicAmpPercent": 30, "duration": 3500,
                "cooldown": 12000, "manaCost": 15, "range": 8
            },
            "netherWard": {
                "name": "Nether Ward",
                "type": "active",
                "description": "Summons a ward that damages enemies when they cast spells based on mana spent.",
                "damagePerMana": 1.5, "wardHp": 100, "duration": 25000, "radius": 10,
                "cooldown": 35000, "manaCost": 30
            },
            "lifeDrain": {
                "name": "Life Drain",
                "type": "ultimate",
                "description": "Drains health from an enemy, healing Pugna. Can target allies to heal them.",
                "drainPerSecond": 25, "allyHealPerSecond": 20, "duration": 10000,
                "cooldown": 7000, "manaCost": 30, "range": 10
            }
        },
        "talents": {
            "10": ["+200 Health", "+25 Nether Blast Damage"],
            "15": ["+1.5 Nether Ward Damage Per Mana", "-1.5s Nether Blast Cooldown"],
            "20": ["+200 Cast Range", "+15 Life Drain Heal"],
            "25": ["+1.5s Decrepify Duration", "Life Drain Grants +50% Speed"]
        }
    },
    "queen_of_pain": {
        "name": "Queen of Pain",
        "title": "Akasha",
        "attr": "intelligence",
        "icon": "queen_of_pain",
        "lore": "The Queen of Pain delights in the suffering of others, using her agility and magic to torment foes.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 21, "manaPerLevel": 26,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "shadowStrike": {
                "name": "Shadow Strike",
                "type": "active",
                "description": "Throws a dagger that damages and slows an enemy, dealing damage over time.",
                "initialDamage": 25, "damageOverTime": 8, "slowPercent": 40, "duration": 5000,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "blink_qop": {
                "name": "Blink",
                "type": "active",
                "description": "Queen of Pain teleports to a target location.",
                "range": 12, "cooldown": 10000, "manaCost": 20
            },
            "screamOfPain": {
                "name": "Scream of Pain",
                "type": "active",
                "description": "Releases a sonic wave that damages nearby enemies.",
                "damage": 45, "radius": 6,
                "cooldown": 7000, "manaCost": 25
            },
            "sonicWave": {
                "name": "Sonic Wave",
                "type": "ultimate",
                "description": "Creates a devastating wave of sound that damages all enemies in its path.",
                "damage": 100, "range": 15, "width": 6,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+10 Strength", "+15 Attack Speed"],
            "15": ["+30 Shadow Strike DPS", "+100 Scream of Pain Damage"],
            "20": ["+30% Spell Lifesteal", "-3s Blink Cooldown"],
            "25": ["+250 Sonic Wave Damage", "Scream of Pain 1.5s Fear"]
        }
    },
    "razor": {
        "name": "Razor",
        "title": "The Lightning Revenant",
        "attr": "agility",
        "icon": "razor",
        "lore": "A being of pure electricity, Razor guards the Underscape, punishing those who would escape death.",
        "baseStats": {
            "maxHp": 100, "maxMana": 90, "hpPerLevel": 24, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 2.9, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.2
        },
        "abilities": {
            "plasmaField": {
                "name": "Plasma Field",
                "type": "active",
                "description": "Releases a ring of plasma that expands outward, damaging enemies based on distance.",
                "minDamage": 15, "maxDamage": 50, "maxRadius": 10,
                "cooldown": 12000, "manaCost": 20
            },
            "staticLink": {
                "name": "Static Link",
                "type": "active",
                "description": "Creates a link that drains damage from an enemy and gives it to Razor.",
                "drainPerSecond": 10, "duration": 8000, "breakRange": 10,
                "cooldown": 25000, "manaCost": 25, "range": 6
            },
            "stormSurge": {
                "name": "Storm Surge",
                "type": "passive",
                "description": "Grants Razor bonus movement speed and a chance to release lightning.",
                "moveSpeedBonus": 15, "strikeChance": 18, "strikeDamage": 30, "strikeRadius": 6
            },
            "eyeOfTheStorm": {
                "name": "Eye of the Storm",
                "type": "ultimate",
                "description": "Summons a storm that strikes the lowest health enemy nearby, reducing their armor.",
                "damagePerStrike": 40, "armorReduction": 2, "strikeInterval": 700, "duration": 30000, "radius": 8,
                "cooldown": 70000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+15 Attack Speed", "+150 Plasma Field Damage"],
            "15": ["+8 Static Link Damage Steal", "+10% Storm Surge Move Speed"],
            "20": ["+100 Eye of the Storm Damage", "+8s Static Link Duration"],
            "25": ["Eye of the Storm Strikes Two Targets", "Static Link Steals Attack Speed"]
        }
    },
    "riki": {
        "name": "Riki",
        "title": "Stealth Assassin",
        "attr": "agility",
        "icon": "riki",
        "lore": "The last of his tribe, Riki uses stealth and cunning to strike from the shadows.",
        "baseStats": {
            "maxHp": 85, "maxMana": 75, "hpPerLevel": 20, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.4, "armor": 4, "armorPerLevel": 0.7,
            "moveSpeed": 12, "attackRange": 2.5, "attackSpeed": 1.4
        },
        "abilities": {
            "smokeScreen": {
                "name": "Smoke Screen",
                "type": "active",
                "description": "Creates a cloud of smoke that silences enemies and causes them to miss attacks.",
                "missChance": 50, "silenced": True, "radius": 5, "duration": 5000,
                "cooldown": 17000, "manaCost": 20, "range": 8
            },
            "blinkStrike": {
                "name": "Blink Strike",
                "type": "active",
                "description": "Teleports to a target and attacks them from behind with bonus damage.",
                "bonusDamage": 40, "charges": 2, "chargeRestoreTime": 15000,
                "cooldown": 4000, "manaCost": 15, "range": 10
            },
            "cloakAndDagger": {
                "name": "Cloak and Dagger",
                "type": "passive",
                "description": "Riki is permanently invisible and deals bonus backstab damage.",
                "backstabMultiplier": 1.5, "fadeDelay": 4000
            },
            "tricksOfTheTrade": {
                "name": "Tricks of the Trade",
                "type": "ultimate",
                "description": "Riki phases out and attacks all enemies in an area with backstab damage.",
                "attackCount": 5, "radius": 6, "duration": 3000,
                "cooldown": 40000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+10 Agility", "+0.4 Cloak and Dagger Backstab Multiplier"],
            "15": ["+20% Smoke Screen Miss Chance", "+1s Smoke Screen Duration"],
            "20": ["+50 Blink Strike Damage", "+1 Blink Strike Charges"],
            "25": ["+2 Tricks of the Trade Attacks", "Cloak and Dagger Doesn't Reveal on Attack"]
        }
    },
    "rubick": {
        "name": "Rubick",
        "title": "Grand Magus",
        "attr": "intelligence",
        "icon": "rubick",
        "lore": "The Grand Magus can steal any spell, turning his enemies' greatest weapons against them.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 19, "manaPerLevel": 28,
            "baseDamage": 14, "damagePerLevel": 2.7, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "telekinesis": {
                "name": "Telekinesis",
                "type": "active",
                "description": "Lifts an enemy into the air and slams them down, stunning them and nearby enemies.",
                "liftDuration": 2000, "stunDuration": 1200, "landingRadius": 4,
                "cooldown": 18000, "manaCost": 25, "range": 8
            },
            "fadeBolt": {
                "name": "Fade Bolt",
                "type": "active",
                "description": "Launches a bolt of energy that bounces between enemies, reducing their damage.",
                "damage": 35, "damageReduction": 20, "damageReductionDuration": 10000, "bounces": 5,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "arcaneSupremacy": {
                "name": "Arcane Supremacy",
                "type": "passive",
                "description": "Increases cast range and spell amplification for Rubick.",
                "castRangeBonus": 100, "spellAmpPercent": 14
            },
            "spellSteal": {
                "name": "Spell Steal",
                "type": "ultimate",
                "description": "Steals the last spell cast by an enemy hero to use as Rubick's own.",
                "stolenSpellDuration": 180000, "cooldown": 16000, "manaCost": 10, "range": 12
            }
        },
        "talents": {
            "10": ["+200 Health", "+50 Fade Bolt Damage"],
            "15": ["+100 Cast Range", "+0.5s Telekinesis Lift Duration"],
            "20": ["+250 Telekinesis Landing Damage", "+14% Spell Amplification"],
            "25": ["Can Steal Two Spells", "+50% Fade Bolt Damage Reduction"]
        }
    },
    "sand_king": {
        "name": "Sand King",
        "title": "Crixalis",
        "attr": "universal",
        "icon": "sand_king",
        "lore": "The king beneath the sand, Crixalis rules the desert and punishes those who disturb his domain.",
        "baseStats": {
            "maxHp": 110, "maxMana": 90, "hpPerLevel": 26, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "burrowstrike": {
                "name": "Burrowstrike",
                "type": "active",
                "description": "Sand King burrows forward, stunning all enemies in his path.",
                "damage": 40, "stunDuration": 1800, "range": 10,
                "cooldown": 11000, "manaCost": 25
            },
            "sandStorm": {
                "name": "Sand Storm",
                "type": "toggle",
                "description": "Sand King becomes invisible in a sandstorm that damages nearby enemies.",
                "damagePerSecond": 25, "radius": 6, "maxDuration": 40000,
                "cooldown": 28000, "manaCostPerSecond": 5
            },
            "causticFinale": {
                "name": "Caustic Finale",
                "type": "passive",
                "description": "Attacks inject a toxin that explodes on death, slowing and damaging nearby enemies.",
                "explosionDamage": 45, "slowPercent": 25, "slowDuration": 3000, "explosionRadius": 4
            },
            "epicenter": {
                "name": "Epicenter",
                "type": "ultimate",
                "description": "Channels to unleash pulses of destructive force that damage and slow enemies.",
                "damagePerPulse": 60, "pulseCount": 10, "slowPercent": 30, "radius": 8, "channelTime": 2000,
                "cooldown": 100000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+20 Burrowstrike Damage"],
            "15": ["+50 Sand Storm DPS", "+0.5s Burrowstrike Stun"],
            "20": ["+4 Epicenter Pulses", "+50 Caustic Finale Damage"],
            "25": ["+50 Health Regen During Sand Storm", "Burrowstrike +350 Range"]
        }
    },
    "shadow_demon": {
        "name": "Shadow Demon",
        "title": "The Shadow Demon",
        "attr": "intelligence",
        "icon": "shadow_demon",
        "lore": "A creature from the abyss, Shadow Demon manipulates souls and corrupts the minds of his enemies.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 19, "manaPerLevel": 28,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "disruption": {
                "name": "Disruption",
                "type": "active",
                "description": "Banishes an enemy, then creates illusions of them when they return.",
                "banishDuration": 2500, "illusionDamage": 50, "illusionDuration": 8000,
                "cooldown": 24000, "manaCost": 25, "range": 8
            },
            "soulCatcher": {
                "name": "Soul Catcher",
                "type": "active",
                "description": "Creates a region that amplifies all damage taken by enemies inside.",
                "damageAmpPercent": 30, "duration": 10000, "radius": 5,
                "cooldown": 18000, "manaCost": 20, "range": 10
            },
            "shadowPoison": {
                "name": "Shadow Poison",
                "type": "active",
                "description": "Launches poison that stacks on enemies. Releasing the poison deals damage per stack.",
                "stackDamage": 30, "maxStacks": 5, "stackDuration": 10000, "radius": 4,
                "cooldown": 2500, "manaCost": 10, "range": 10
            },
            "demonicPurge": {
                "name": "Demonic Purge",
                "type": "ultimate",
                "description": "Purges an enemy of buffs and continuously slows them. Deals damage at the end.",
                "slowPercent": 100, "slowDecay": True, "damage": 100, "duration": 7000,
                "cooldown": 40000, "manaCost": 40, "range": 10
            }
        },
        "talents": {
            "10": ["+25% XP Gain", "+15 Shadow Poison Damage"],
            "15": ["+1.5s Disruption Banish Duration", "-5s Soul Catcher Cooldown"],
            "20": ["+500 Demonic Purge Damage", "+30% Shadow Poison Damage"],
            "25": ["2 Charges of Disruption", "-1s Shadow Poison Cooldown"]
        }
    },
    "shadow_shaman": {
        "name": "Shadow Shaman",
        "title": "Rhasta",
        "attr": "intelligence",
        "icon": "shadow_shaman",
        "lore": "Rhasta channels spirits of the wild, using powerful disables and summoned serpents to control battles.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 21, "manaPerLevel": 26,
            "baseDamage": 17, "damagePerLevel": 2.9, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "etherShock": {
                "name": "Ether Shock",
                "type": "active",
                "description": "Releases a cone of lightning that damages multiple enemies.",
                "damage": 45, "targets": 5, "bounceRange": 6,
                "cooldown": 10000, "manaCost": 20, "range": 10
            },
            "hex": {
                "name": "Hex",
                "type": "active",
                "description": "Transforms an enemy into a harmless creature, disabling them completely.",
                "duration": 3000, "cooldown": 13000, "manaCost": 25, "range": 6
            },
            "shackles": {
                "name": "Shackles",
                "type": "active",
                "description": "Channels to bind an enemy in place, dealing damage over time.",
                "damagePerSecond": 25, "maxDuration": 5000,
                "cooldown": 16000, "manaCost": 25, "range": 6
            },
            "massSerpenWard": {
                "name": "Mass Serpent Ward",
                "type": "ultimate",
                "description": "Summons a group of serpent wards that attack enemies and buildings.",
                "wardCount": 10, "wardDamage": 15, "wardDuration": 30000, "radius": 4,
                "cooldown": 110000, "manaCost": 60, "range": 8
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+100 Ether Shock Damage"],
            "15": ["+1.5s Hex Duration", "+1.5s Shackles Duration"],
            "20": ["+300 Serpent Ward Damage", "+4 Serpent Wards"],
            "25": ["Shackles Hits Two Targets", "+2s Hex Duration"]
        }
    },
    "silencer": {
        "name": "Silencer",
        "title": "Nortrom",
        "attr": "intelligence",
        "icon": "silencer",
        "lore": "Nortrom drains intelligence from his victims, growing more powerful as he steals their knowledge.",
        "baseStats": {
            "maxHp": 80, "maxMana": 130, "hpPerLevel": 20, "manaPerLevel": 28,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "arcaneCurse": {
                "name": "Arcane Curse",
                "type": "active",
                "description": "Curses enemies in an area, dealing damage and slowing. Casting extends the curse.",
                "damage": 20, "slowPercent": 18, "duration": 6000, "radius": 6,
                "cooldown": 16000, "manaCost": 20, "range": 10
            },
            "glaivesOfWisdom": {
                "name": "Glaives of Wisdom",
                "type": "toggle",
                "description": "Silencer's attacks deal bonus pure damage based on intelligence.",
                "intDamagePercent": 60, "manaCostPerAttack": 8
            },
            "lastWord": {
                "name": "Last Word",
                "type": "active",
                "description": "Marks an enemy. If they cast a spell or the duration expires, they are silenced and damaged.",
                "damage": 40, "silenceDuration": 4000, "delay": 4000,
                "cooldown": 15000, "manaCost": 20, "range": 10
            },
            "globalSilence": {
                "name": "Global Silence",
                "type": "ultimate",
                "description": "Silences all enemy heroes on the map.",
                "duration": 6000, "cooldown": 130000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+20 Attack Speed", "+15 Arcane Curse Damage"],
            "15": ["+100 Glaives of Wisdom Damage", "+1.5s Last Word Silence"],
            "20": ["+2s Global Silence Duration", "-3s Arcane Curse Cooldown"],
            "25": ["+25% Glaives of Wisdom Intelligence as Damage", "Arcane Curse Undispellable"]
        }
    },
    "skywrath_mage": {
        "name": "Skywrath Mage",
        "title": "Dragonus",
        "attr": "intelligence",
        "icon": "skywrath",
        "lore": "A winged sorcerer devoted to his fallen queen, Dragonus rains magical fury upon his enemies.",
        "baseStats": {
            "maxHp": 75, "maxMana": 140, "hpPerLevel": 18, "manaPerLevel": 30,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "arcaneBolt": {
                "name": "Arcane Bolt",
                "type": "active",
                "description": "Fires a slow-moving bolt of arcane energy that deals damage based on intelligence.",
                "baseDamage": 20, "intMultiplier": 1.5,
                "cooldown": 5000, "manaCost": 15, "range": 12
            },
            "concussiveShot": {
                "name": "Concussive Shot",
                "type": "active",
                "description": "Automatically targets the closest enemy, damaging and slowing them.",
                "damage": 40, "slowPercent": 40, "slowDuration": 4000,
                "cooldown": 14000, "manaCost": 20
            },
            "ancientSeal": {
                "name": "Ancient Seal",
                "type": "active",
                "description": "Silences an enemy and amplifies all magic damage they take.",
                "magicAmpPercent": 35, "silenceDuration": 4000,
                "cooldown": 14000, "manaCost": 20, "range": 10
            },
            "mysticFlare": {
                "name": "Mystic Flare",
                "type": "ultimate",
                "description": "Rains down magical energy in an area, dealing massive damage split among enemies.",
                "totalDamage": 300, "radius": 4, "duration": 2000,
                "cooldown": 60000, "manaCost": 60, "range": 14
            }
        },
        "talents": {
            "10": ["+2 Mana Regen", "+50 Arcane Bolt Damage"],
            "15": ["+1s Ancient Seal Duration", "+100 Concussive Shot Damage"],
            "20": ["+15% Ancient Seal Magic Resistance Reduction", "Global Concussive Shot"],
            "25": ["Mystic Flare Hits Invisible Units", "+200 Mystic Flare Damage"]
        }
    },
    "slardar": {
        "name": "Slardar",
        "title": "Slithereen Guard",
        "attr": "strength",
        "icon": "slardar",
        "lore": "Guardian of the deep, Slardar crushes his enemies with raw strength and reveals hidden foes.",
        "baseStats": {
            "maxHp": 125, "maxMana": 75, "hpPerLevel": 28, "manaPerLevel": 16,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "guardianSprint": {
                "name": "Guardian Sprint",
                "type": "active",
                "description": "Slardar moves at maximum speed but takes bonus damage while active.",
                "moveSpeedBonus": 50, "bonusDamageTaken": 15, "duration": 10000,
                "cooldown": 17000, "manaCost": 0
            },
            "slithereenCrush": {
                "name": "Slithereen Crush",
                "type": "active",
                "description": "Slams the ground, stunning and damaging nearby enemies.",
                "damage": 45, "stunDuration": 1400, "slowPercent": 20, "slowDuration": 2000, "radius": 5,
                "cooldown": 8000, "manaCost": 25
            },
            "bashOfTheDeep": {
                "name": "Bash of the Deep",
                "type": "passive",
                "description": "Grants a chance to bash enemies, stunning and dealing bonus damage.",
                "chance": 25, "bonusDamage": 30, "stunDuration": 1000
            },
            "corrosiveHaze": {
                "name": "Corrosive Haze",
                "type": "ultimate",
                "description": "Reveals an enemy and reduces their armor significantly.",
                "armorReduction": 15, "duration": 18000,
                "cooldown": 5000, "manaCost": 15, "range": 10
            }
        },
        "talents": {
            "10": ["+20 Damage", "+8 Health Regen"],
            "15": ["+50 Slithereen Crush Damage", "+30% Guardian Sprint Movement Speed"],
            "20": ["+1s Bash of the Deep Stun", "+4 Corrosive Haze Armor Reduction"],
            "25": ["Corrosive Haze Undispellable", "+80 Bash Damage"]
        }
    },
    "slark": {
        "name": "Slark",
        "title": "Nightcrawler",
        "attr": "agility",
        "icon": "slark",
        "lore": "Escaped from Dark Reef prison, Slark is a cunning predator who grows stronger with each attack.",
        "baseStats": {
            "maxHp": 90, "maxMana": 80, "hpPerLevel": 22, "manaPerLevel": 18,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "darkPact": {
                "name": "Dark Pact",
                "type": "active",
                "description": "Slark sacrifices health to purge debuffs and deal AoE damage.",
                "damage": 35, "selfDamage": 15, "radius": 5, "pulses": 5, "totalDuration": 2000,
                "cooldown": 6000, "manaCost": 20
            },
            "pounce": {
                "name": "Pounce",
                "type": "active",
                "description": "Slark leaps forward, leashing the first enemy hit.",
                "leashDuration": 3000, "leashRange": 4, "leapRange": 8,
                "cooldown": 12000, "manaCost": 20
            },
            "essenceShift": {
                "name": "Essence Shift",
                "type": "passive",
                "description": "Each attack steals a stat point from the enemy, granting Slark agility.",
                "agilitySteal": 3, "statLoss": 1, "duration": 20000
            },
            "shadowDance": {
                "name": "Shadow Dance",
                "type": "ultimate",
                "description": "Slark becomes invisible and gains bonus health regen and movement speed.",
                "hpRegenPercent": 6, "moveSpeedBonus": 30, "duration": 4500,
                "cooldown": 60000, "manaCost": 40
            }
        },
        "talents": {
            "10": ["+10 Agility", "+1s Pounce Leash Duration"],
            "15": ["+75 Dark Pact Damage", "+30 Attack Speed"],
            "20": ["+2s Shadow Dance Duration", "+0.4s Shadow Dance Health Regen"],
            "25": ["+100 Essence Shift Max Stacks", "Pounce Leashes Two Targets"]
        }
    },
    "snapfire": {
        "name": "Snapfire",
        "title": "Beatrix Snapfire",
        "attr": "universal",
        "icon": "snapfire",
        "lore": "A feisty grandma who rides a dragon toad and bakes explosive cookies for her allies.",
        "baseStats": {
            "maxHp": 100, "maxMana": 100, "hpPerLevel": 24, "manaPerLevel": 22,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "scatterBlast": {
                "name": "Scatterblast",
                "type": "active",
                "description": "Fires a shotgun blast that damages and slows enemies in a cone.",
                "damage": 35, "slowPercent": 30, "slowDuration": 2500, "range": 8,
                "cooldown": 10000, "manaCost": 20
            },
            "fireSnapCookie": {
                "name": "Firesnap Cookie",
                "type": "active",
                "description": "Feeds a cookie to an ally, launching them forward to stun enemies on landing.",
                "damage": 40, "stunDuration": 2000, "stunRadius": 4, "launchRange": 6,
                "cooldown": 15000, "manaCost": 25, "range": 8
            },
            "lizHitit": {
                "name": "Lil' Shredder",
                "type": "active",
                "description": "Mortimer rapidly attacks enemies, slowing their attack speed.",
                "attacks": 6, "damagePerAttack": 20, "attackSpeedSlow": 20, "duration": 6000,
                "cooldown": 15000, "manaCost": 20
            },
            "mortimerKisses": {
                "name": "Mortimer Kisses",
                "type": "ultimate",
                "description": "Channels to launch fireballs at target areas, damaging and slowing enemies.",
                "fireballDamage": 80, "fireballCount": 8, "impactRadius": 4, "burnDuration": 3000,
                "cooldown": 110000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+20 Lil' Shredder Attack Speed Slow", "+20 Scatterblast Damage"],
            "15": ["+1s Firesnap Cookie Stun", "+1.5 Lil' Shredder Attacks"],
            "20": ["+100 Mortimer Kisses Impact Damage", "+75 Scatterblast Damage"],
            "25": ["Scatterblast Applies 40% Slow", "3 Firesnap Cookie Charges"]
        }
    },
    "spectre": {
        "name": "Spectre",
        "title": "Mercurial",
        "attr": "agility",
        "icon": "spectre",
        "lore": "A phantom born from a broken goddess, Spectre haunts all who witness her ghostly form.",
        "baseStats": {
            "maxHp": 100, "maxMana": 70, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 14, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "spectralDagger": {
                "name": "Spectral Dagger",
                "type": "active",
                "description": "Throws a dagger that damages enemies and leaves a shadow path. Spectre gains phased movement on the path.",
                "damage": 35, "slowPercent": 20, "pathDuration": 12000, "range": 14,
                "cooldown": 16000, "manaCost": 25
            },
            "desolate": {
                "name": "Desolate",
                "type": "passive",
                "description": "Deals bonus damage to enemies who are alone, without nearby allies.",
                "bonusDamage": 40, "aloneRadius": 5
            },
            "dispersion": {
                "name": "Dispersion",
                "type": "passive",
                "description": "Reflects a portion of damage taken back to nearby enemies.",
                "reflectPercent": 22, "radius": 8
            },
            "haunt": {
                "name": "Haunt",
                "type": "ultimate",
                "description": "Creates a spectral illusion to attack each enemy hero. Can teleport to any illusion.",
                "illusionDamage": 50, "illusionDuration": 7000,
                "cooldown": 150000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+5 Health Regen", "+80 Spectral Dagger Damage"],
            "15": ["+10% Dispersion", "+10 Desolate Damage"],
            "20": ["+350 Health", "+8% Dispersion Reflect"],
            "25": ["+20 Desolate Damage", "Haunt Creates 2 Illusions Per Hero"]
        }
    },
    "spirit_breaker": {
        "name": "Spirit Breaker",
        "title": "Barathrum",
        "attr": "strength",
        "icon": "spirit_breaker",
        "lore": "From the elemental plane, Barathrum charges across the battlefield to bash his enemies.",
        "baseStats": {
            "maxHp": 130, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "chargeOfDarkness": {
                "name": "Charge of Darkness",
                "type": "active",
                "description": "Spirit Breaker charges at a target, gaining speed and stunning on impact.",
                "stunDuration": 1600, "bonusSpeed": 25, "bashDamage": 50,
                "cooldown": 12000, "manaCost": 20
            },
            "bulldoze": {
                "name": "Bulldoze",
                "type": "active",
                "description": "Grants bonus movement speed and status resistance for a duration.",
                "moveSpeedBonus": 30, "statusResistPercent": 70, "duration": 8000,
                "cooldown": 22000, "manaCost": 25
            },
            "greaterBash": {
                "name": "Greater Bash",
                "type": "passive",
                "description": "Attacks have a chance to bash, dealing bonus damage and pushing enemies back.",
                "chance": 17, "damagePercent": 22, "pushDistance": 3, "stunDuration": 1200
            },
            "netherStrike": {
                "name": "Nether Strike",
                "type": "ultimate",
                "description": "Teleports to an enemy and delivers a devastating Greater Bash.",
                "damage": 100, "extraBashChance": 100, "stunDuration": 1000,
                "cooldown": 70000, "manaCost": 50, "range": 8
            }
        },
        "talents": {
            "10": ["+20 Movement Speed", "+400 Night Vision"],
            "15": ["+5% Greater Bash Damage", "+40 Charge of Darkness Damage"],
            "20": ["+20% Greater Bash Chance", "+500 Charge of Darkness Speed"],
            "25": ["+25% Bulldoze Status Resistance", "+1s Nether Strike Stun"]
        }
    },
    "storm_spirit": {
        "name": "Storm Spirit",
        "title": "Raijin Thunderkeg",
        "attr": "intelligence",
        "icon": "storm_spirit",
        "lore": "A jolly spirit of lightning, Storm zips across the battlefield with electric energy.",
        "baseStats": {
            "maxHp": 85, "maxMana": 130, "hpPerLevel": 21, "manaPerLevel": 28,
            "baseDamage": 16, "damagePerLevel": 3.0, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "staticRemnant": {
                "name": "Static Remnant",
                "type": "active",
                "description": "Creates an electric clone that explodes when enemies come near.",
                "damage": 40, "triggerRadius": 4, "duration": 12000,
                "cooldown": 3500, "manaCost": 20
            },
            "electricVortex": {
                "name": "Electric Vortex",
                "type": "active",
                "description": "Pulls an enemy towards Storm Spirit.",
                "pullDuration": 2000, "pullDistance": 6,
                "cooldown": 16000, "manaCost": 25, "range": 8
            },
            "overload": {
                "name": "Overload",
                "type": "passive",
                "description": "After casting a spell, Storm's next attack deals bonus damage and slows.",
                "damage": 35, "slowPercent": 40, "slowDuration": 800, "radius": 4
            },
            "ballLightning": {
                "name": "Ball Lightning",
                "type": "ultimate",
                "description": "Storm transforms into lightning, becoming invulnerable while traveling and dealing damage.",
                "damagePerUnit": 10, "travelSpeed": 20, "manaCostBase": 30, "manaCostPerUnit": 1.2
            }
        },
        "talents": {
            "10": ["+3 Mana Regen", "+30 Static Remnant Damage"],
            "15": ["+40 Overload Damage", "+0.5s Electric Vortex Pull Duration"],
            "20": ["+150 Static Remnant Damage", "+20% Overload Slow"],
            "25": ["Overload Pierces Spell Immunity", "Electric Vortex Pulls All Enemies in Range"]
        }
    },
    "sven": {
        "name": "Sven",
        "title": "Rogue Knight",
        "attr": "strength",
        "icon": "sven",
        "lore": "Cast out by his order, Sven wields his father's sword to dispense justice on his own terms.",
        "baseStats": {
            "maxHp": 130, "maxMana": 70, "hpPerLevel": 30, "manaPerLevel": 15,
            "baseDamage": 20, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "stormHammer": {
                "name": "Storm Hammer",
                "type": "active",
                "description": "Sven throws his hammer, stunning and damaging enemies in an area.",
                "damage": 50, "stunDuration": 1800, "radius": 4,
                "cooldown": 13000, "manaCost": 25, "range": 10
            },
            "greatCleave": {
                "name": "Great Cleave",
                "type": "passive",
                "description": "Sven's attacks cleave, dealing damage to enemies in a cone behind the target.",
                "cleavePercent": 66, "cleaveRadius": 5
            },
            "warcry": {
                "name": "Warcry",
                "type": "active",
                "description": "Sven rallies nearby allies, granting bonus armor and movement speed.",
                "bonusArmor": 12, "moveSpeedPercent": 20, "duration": 8000, "radius": 10,
                "cooldown": 28000, "manaCost": 30
            },
            "godsStrength": {
                "name": "God's Strength",
                "type": "ultimate",
                "description": "Sven channels his rogue energy, gaining massive bonus damage.",
                "damageBonus": 160, "duration": 35000,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+4 Mana Regen", "+10% Lifesteal"],
            "15": ["+15 Movement Speed", "+12 Strength"],
            "20": ["+20% Great Cleave Damage", "+0.8s Storm Hammer Stun"],
            "25": ["+50% God's Strength Damage", "+15 Warcry Armor"]
        }
    },
    "techies": {
        "name": "Techies",
        "title": "Squee, Spleen and Spoon",
        "attr": "universal",
        "icon": "techies",
        "lore": "Three maniacal goblins united by a love of explosions, Techies cover the battlefield with deadly mines.",
        "baseStats": {
            "maxHp": 90, "maxMana": 110, "hpPerLevel": 22, "manaPerLevel": 24,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "stickyBomb": {
                "name": "Sticky Bomb",
                "type": "active",
                "description": "Throws a bomb that sticks to enemies, detonating after a delay.",
                "damage": 40, "slowPercent": 30, "delay": 2000, "radius": 4,
                "cooldown": 9000, "manaCost": 20, "range": 10
            },
            "reactiveTagging": {
                "name": "Reactive Tagging",
                "type": "active",
                "description": "Places a sign that disarms enemies who walk through it.",
                "disarmDuration": 2000, "silenceDuration": 2000, "duration": 20000,
                "cooldown": 25000, "manaCost": 25, "range": 8
            },
            "blastOff": {
                "name": "Blast Off!",
                "type": "active",
                "description": "Techies leap to a target area, silencing enemies on landing while damaging themselves.",
                "damage": 50, "selfDamage": 35, "silenceDuration": 4000, "radius": 5, "range": 12,
                "cooldown": 18000, "manaCost": 25
            },
            "proximityMines": {
                "name": "Proximity Mines",
                "type": "ultimate",
                "description": "Places an invisible mine that detonates when enemies approach.",
                "damage": 120, "activationDelay": 1500, "detectionRadius": 3, "charges": 3,
                "cooldown": 8000, "manaCost": 30
            }
        },
        "talents": {
            "10": ["+200 Health", "+25 Sticky Bomb Damage"],
            "15": ["+200 Blast Off! Damage", "+1s Reactive Tagging Duration"],
            "20": ["+25% Magic Resistance", "+50 Proximity Mines Damage"],
            "25": ["-10s Blast Off! Cooldown", "+150 Proximity Mines Damage"]
        }
    },
    "templar_assassin": {
        "name": "Templar Assassin",
        "title": "Lanaya",
        "attr": "agility",
        "icon": "templar_assassin",
        "lore": "Lanaya guards the temple's secrets with deadly precision, striking from the shadows.",
        "baseStats": {
            "maxHp": 85, "maxMana": 90, "hpPerLevel": 21, "manaPerLevel": 20,
            "baseDamage": 20, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "refraction": {
                "name": "Refraction",
                "type": "active",
                "description": "Bends light around Lanaya, granting damage block instances and bonus damage.",
                "damageInstances": 4, "bonusDamageInstances": 4, "bonusDamage": 40, "duration": 17000,
                "cooldown": 15000, "manaCost": 20
            },
            "meld": {
                "name": "Meld",
                "type": "active",
                "description": "Lanaya becomes invisible and gains bonus damage and armor reduction on her next attack.",
                "bonusDamage": 60, "armorReduction": 8, "duration": 12000,
                "cooldown": 7000, "manaCost": 15
            },
            "psiBlades": {
                "name": "Psi Blades",
                "type": "passive",
                "description": "Attacks spill through the target, hitting enemies in a line behind.",
                "spillRange": 6, "spillWidth": 2, "bonusRange": 80
            },
            "psionicTraps": {
                "name": "Psionic Traps",
                "type": "ultimate",
                "description": "Places invisible traps that slow enemies when triggered.",
                "maxTraps": 11, "slowPercent": 50, "trapDuration": 120000, "triggerRadius": 4,
                "cooldown": 5000, "manaCost": 10, "range": 14
            }
        },
        "talents": {
            "10": ["+25 Attack Speed", "+3 Refraction Instances"],
            "15": ["+80 Meld Bonus Damage", "+100 Psi Blades Range"],
            "20": ["Meld Dispels", "+4 Refraction Instances"],
            "25": ["+200 Psionic Trap Damage", "-3 Meld Armor Reduction"]
        }
    },
    "terrorblade": {
        "name": "Terrorblade",
        "title": "Demon Marauder",
        "attr": "agility",
        "icon": "terrorblade",
        "lore": "A demon so twisted even his own kind imprisoned him, Terrorblade commands illusions and reflects damage.",
        "baseStats": {
            "maxHp": 85, "maxMana": 80, "hpPerLevel": 20, "manaPerLevel": 18,
            "baseDamage": 22, "damagePerLevel": 3.6, "armor": 5, "armorPerLevel": 0.7,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.4
        },
        "abilities": {
            "reflection": {
                "name": "Reflection",
                "type": "active",
                "description": "Creates invulnerable illusions of all nearby enemies that attack them.",
                "illusionDamage": 60, "slowPercent": 25, "duration": 5500, "radius": 8,
                "cooldown": 16000, "manaCost": 25
            },
            "conjureImage": {
                "name": "Conjure Image",
                "type": "active",
                "description": "Creates an illusion of Terrorblade that deals moderate damage.",
                "illusionDamage": 60, "illusionDuration": 34000,
                "cooldown": 16000, "manaCost": 20
            },
            "metamorphosis": {
                "name": "Metamorphosis",
                "type": "active",
                "description": "Terrorblade transforms into a ranged demon with bonus damage.",
                "bonusDamage": 40, "bonusRange": 8, "duration": 40000,
                "cooldown": 140000, "manaCost": 50
            },
            "sunder": {
                "name": "Sunder",
                "type": "ultimate",
                "description": "Swaps health percentages with a target enemy or ally.",
                "minHealthPercent": 25, "cooldown": 40000, "manaCost": 30, "range": 6
            }
        },
        "talents": {
            "10": ["+300 Health", "+8 Conjure Image Damage"],
            "15": ["+4s Metamorphosis Duration", "+4s Conjure Image Duration"],
            "20": ["-20s Metamorphosis Cooldown", "-8s Reflection Cooldown"],
            "25": ["+8s Sunder Cooldown per Hero Hit", "Metamorphosis Affects Illusions"]
        }
    },
    "tidehunter": {
        "name": "Tidehunter",
        "title": "Leviathan",
        "attr": "strength",
        "icon": "tidehunter",
        "lore": "Leviathan hunts the beasts of the deep, using the tide itself to crush his enemies.",
        "baseStats": {
            "maxHp": 140, "maxMana": 80, "hpPerLevel": 32, "manaPerLevel": 18,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 0.9
        },
        "abilities": {
            "gush": {
                "name": "Gush",
                "type": "active",
                "description": "Sprays water at a target, damaging them and reducing their armor and movement speed.",
                "damage": 40, "armorReduction": 5, "slowPercent": 40, "duration": 4500,
                "cooldown": 12000, "manaCost": 20, "range": 8
            },
            "kraken_shell": {
                "name": "Kraken Shell",
                "type": "passive",
                "description": "Tidehunter's thick skin blocks damage and removes debuffs after taking enough damage.",
                "damageBlock": 15, "debuffThreshold": 500
            },
            "anchor_smash": {
                "name": "Anchor Smash",
                "type": "active",
                "description": "Swings a massive anchor, damaging enemies and reducing their attack damage.",
                "damage": 35, "damageReductionPercent": 45, "duration": 6000, "radius": 5,
                "cooldown": 4000, "manaCost": 15
            },
            "ravage": {
                "name": "Ravage",
                "type": "ultimate",
                "description": "Slams the ground, causing tentacles to rise and stun all enemies in a huge area.",
                "damage": 100, "stunDuration": 2500, "radius": 12,
                "cooldown": 150000, "manaCost": 60
            }
        },
        "talents": {
            "10": ["+3 Mana Regen", "+20 Movement Speed"],
            "15": ["+100 Anchor Smash Damage", "-3 Gush Armor"],
            "20": ["+25% Anchor Smash Damage Reduction", "+0.8s Ravage Stun Duration"],
            "25": ["Kraken Shell Procs While Stunned", "-4s Anchor Smash Cooldown"]
        }
    },
    "timbersaw": {
        "name": "Timbersaw",
        "title": "Rizzrack",
        "attr": "universal",
        "icon": "timbersaw",
        "lore": "Paranoid of trees, Rizzrack built a suit of armor to destroy every forest that threatens him.",
        "baseStats": {
            "maxHp": 115, "maxMana": 100, "hpPerLevel": 26, "manaPerLevel": 22,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "whirlingDeath": {
                "name": "Whirling Death",
                "type": "active",
                "description": "Spins rapidly, dealing damage and reducing the primary stat of enemies hit.",
                "damage": 40, "statReductionPercent": 15, "radius": 5, "treeBonusDamage": 12,
                "cooldown": 6000, "manaCost": 20
            },
            "timberChain": {
                "name": "Timber Chain",
                "type": "active",
                "description": "Launches a chain that attaches to trees, pulling Timbersaw and damaging enemies in the path.",
                "damage": 40, "range": 14, "speed": 25,
                "cooldown": 4000, "manaCost": 15
            },
            "reactiveArmor": {
                "name": "Reactive Armor",
                "type": "passive",
                "description": "Each attack against Timbersaw grants bonus armor and health regen that stacks.",
                "armorPerStack": 1, "regenPerStack": 1, "maxStacks": 20, "stackDuration": 10000
            },
            "chakram": {
                "name": "Chakram",
                "type": "ultimate",
                "description": "Launches a spinning chakram that damages and slows enemies. Costs mana per second to maintain.",
                "damagePerSecond": 50, "slowPercent": 25, "manaCostPerSecond": 8,
                "cooldown": 6000, "manaCost": 40, "range": 14
            }
        },
        "talents": {
            "10": ["+200 Health", "+1 Reactive Armor Stack"],
            "15": ["+8% Whirling Death Stat Reduction", "+60 Timber Chain Damage"],
            "20": ["+10 Reactive Armor Regen per Stack", "+1200 Timber Chain Range"],
            "25": ["+2s Chakram Slow Duration", "Whirling Death Grants +10 Strength per Hero Hit"]
        }
    },
    "tinker": {
        "name": "Tinker",
        "title": "Boush",
        "attr": "intelligence",
        "icon": "tinker",
        "lore": "A brilliant inventor, Boush uses his gadgets to overwhelm enemies with relentless ability spam.",
        "baseStats": {
            "maxHp": 80, "maxMana": 140, "hpPerLevel": 19, "manaPerLevel": 30,
            "baseDamage": 16, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "laserTinker": {
                "name": "Laser",
                "type": "active",
                "description": "Fires a laser that damages and blinds enemies, causing them to miss attacks.",
                "damage": 50, "blindDuration": 3000, "missChance": 100,
                "cooldown": 14000, "manaCost": 25, "range": 8
            },
            "heatSeekingMissiles": {
                "name": "Heat-Seeking Missiles",
                "type": "active",
                "description": "Launches missiles at the nearest enemy heroes, dealing damage.",
                "damagePerMissile": 50, "missileCount": 2,
                "cooldown": 18000, "manaCost": 30
            },
            "defense_matrix": {
                "name": "Defense Matrix",
                "type": "active",
                "description": "Shields an ally, granting barrier and status resistance.",
                "barrierAmount": 80, "statusResistPercent": 50, "duration": 10000,
                "cooldown": 18000, "manaCost": 25, "range": 8
            },
            "rearm": {
                "name": "Rearm",
                "type": "ultimate",
                "description": "Channels to reset the cooldowns of all abilities and items.",
                "channelTime": 3000, "cooldown": 0, "manaCost": 80
            }
        },
        "talents": {
            "10": ["+4 Armor", "+100 Laser Damage"],
            "15": ["+8% Spell Amplification", "+1 Heat-Seeking Missiles Target"],
            "20": ["+100 Defense Matrix Barrier", "-0.5s Rearm Channel"],
            "25": ["+100 Heat-Seeking Missiles Damage", "Laser Has 100% Blind"]
        }
    },
    "tiny": {
        "name": "Tiny",
        "title": "Stone Giant",
        "attr": "strength",
        "icon": "tiny",
        "lore": "An elemental born from a single pebble, Tiny grows larger and stronger with each passing moment.",
        "baseStats": {
            "maxHp": 130, "maxMana": 80, "hpPerLevel": 30, "manaPerLevel": 18,
            "baseDamage": 20, "damagePerLevel": 3.6, "armor": 0, "armorPerLevel": 0.3,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 0.8
        },
        "abilities": {
            "avalanche": {
                "name": "Avalanche",
                "type": "active",
                "description": "Bombards an area with rocks, stunning and damaging enemies.",
                "damage": 45, "stunDuration": 1200, "radius": 4, "waveDuration": 1000,
                "cooldown": 17000, "manaCost": 25, "range": 10
            },
            "toss": {
                "name": "Toss",
                "type": "active",
                "description": "Grabs the nearest unit and throws it at a target, dealing damage on impact.",
                "damage": 60, "radius": 4, "range": 12,
                "cooldown": 8000, "manaCost": 20
            },
            "treeGrab": {
                "name": "Tree Grab",
                "type": "active",
                "description": "Tiny grabs a tree, gaining bonus attack damage and splash damage but losing attack speed.",
                "bonusDamage": 30, "splashPercent": 50, "attackSpeedReduction": 20, "charges": 5,
                "cooldown": 18000, "manaCost": 15
            },
            "grow": {
                "name": "Grow",
                "type": "ultimate",
                "description": "Tiny grows in size, gaining bonus damage and armor but losing attack speed.",
                "bonusDamage": 100, "bonusArmor": 15, "attackSpeedLoss": 30
            }
        },
        "talents": {
            "10": ["+15 Movement Speed", "+75 Avalanche Damage"],
            "15": ["-4s Tree Grab Cooldown", "+100 Toss Damage"],
            "20": ["+15% Status Resistance", "+20 Grow Attack Speed"],
            "25": ["+3 Tree Grab Attacks", "-8s Avalanche Cooldown"]
        }
    },
    "treant_protector": {
        "name": "Treant Protector",
        "title": "Rooftrellen",
        "attr": "strength",
        "icon": "treant",
        "lore": "An ancient guardian of the forest, Rooftrellen protects all living things with his immense power.",
        "baseStats": {
            "maxHp": 145, "maxMana": 90, "hpPerLevel": 34, "manaPerLevel": 20,
            "baseDamage": 22, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 9, "attackRange": 2.5, "attackSpeed": 0.8
        },
        "abilities": {
            "naturesGrasp": {
                "name": "Nature's Grasp",
                "type": "active",
                "description": "Creates vines that damage and slow enemies.",
                "damagePerSecond": 20, "slowPercent": 25, "duration": 8000, "range": 12,
                "cooldown": 18000, "manaCost": 25
            },
            "leechSeed": {
                "name": "Leech Seed",
                "type": "active",
                "description": "Plants a seed in an enemy that damages them and heals nearby allies.",
                "damagePerPulse": 12, "healPerPulse": 12, "pulses": 6, "radius": 6,
                "cooldown": 14000, "manaCost": 20, "range": 8
            },
            "livingArmor": {
                "name": "Living Armor",
                "type": "active",
                "description": "Wraps an ally or building in protective bark, granting bonus health regen and damage block.",
                "hpRegen": 8, "damageBlock": 40, "blockInstances": 6, "duration": 30000,
                "cooldown": 16000, "manaCost": 20
            },
            "overgrowth": {
                "name": "Overgrowth",
                "type": "ultimate",
                "description": "Summons roots to entangle all enemies in a large area, preventing movement and attacks.",
                "damage": 40, "duration": 4500, "radius": 10,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+25 Leech Seed Damage/Heal", "+2 Living Armor Block Instances"],
            "15": ["+25% Nature's Grasp Slow", "+60 Leech Seed Damage/Heal"],
            "20": ["+50 Nature's Grasp DPS", "+100 Living Armor Health Regen"],
            "25": ["+2.5s Overgrowth Duration", "Living Armor Provides +50 Attack Speed"]
        }
    },
    "troll_warlord": {
        "name": "Troll Warlord",
        "title": "Jah'rakal",
        "attr": "agility",
        "icon": "troll_warlord",
        "lore": "A savage troll chieftain whose battle frenzy makes him attack with unmatched speed.",
        "baseStats": {
            "maxHp": 100, "maxMana": 75, "hpPerLevel": 24, "manaPerLevel": 16,
            "baseDamage": 17, "damagePerLevel": 3.2, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.3
        },
        "abilities": {
            "berserkerRage": {
                "name": "Berserker's Rage",
                "type": "toggle",
                "description": "Switches between ranged and melee, gaining bonus stats in melee form.",
                "meleeBonus": {"armor": 6, "moveSpeed": 15, "bashChance": 10, "bashDamage": 30}
            },
            "whirlingAxes": {
                "name": "Whirling Axes",
                "type": "active",
                "description": "Throws or spins axes depending on form. Ranged slows, melee blinds.",
                "rangedDamage": 35, "rangedSlow": 35, "meleeDamage": 45, "meleeBlindChance": 60,
                "cooldown": 9000, "manaCost": 20
            },
            "fervor": {
                "name": "Fervor",
                "type": "passive",
                "description": "Each consecutive attack on the same target grants bonus attack speed.",
                "attackSpeedPerStack": 15, "maxStacks": 10
            },
            "battleTrance": {
                "name": "Battle Trance",
                "type": "ultimate",
                "description": "Enters a battle trance, granting lifesteal and attack speed to Troll and nearby allies.",
                "bonusAttackSpeed": 180, "lifestealPercent": 50, "duration": 6500,
                "cooldown": 90000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+10 Agility", "+5 Fervor Attack Speed"],
            "15": ["+3 Max Fervor Stacks", "+50 Whirling Axes Damage"],
            "20": ["+10% Berserker's Rage Status Resistance", "+1s Battle Trance Duration"],
            "25": ["+60 Battle Trance Attack Speed", "Battle Trance Strong Dispel"]
        }
    },
    "tusk": {
        "name": "Tusk",
        "title": "Ymir",
        "attr": "strength",
        "icon": "tusk",
        "lore": "A brawler from the frozen tundra, Tusk uses ice and his fists to punch enemies into submission.",
        "baseStats": {
            "maxHp": 120, "maxMana": 85, "hpPerLevel": 28, "manaPerLevel": 18,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.1
        },
        "abilities": {
            "iceShards": {
                "name": "Ice Shards",
                "type": "active",
                "description": "Launches shards of ice that damage enemies and create a barrier.",
                "damage": 40, "barrierDuration": 7000, "range": 14,
                "cooldown": 14000, "manaCost": 20
            },
            "snowball": {
                "name": "Snowball",
                "type": "active",
                "description": "Rolls towards an enemy in a snowball, gathering allies along the way. Stuns on impact.",
                "damage": 35, "stunDuration": 800, "range": 12,
                "cooldown": 18000, "manaCost": 20
            },
            "tagTeam": {
                "name": "Tag Team",
                "type": "active",
                "description": "Creates an aura that causes attacks on slowed enemies to deal bonus damage.",
                "bonusDamage": 50, "slowPercent": 75, "duration": 5000, "radius": 5,
                "cooldown": 15000, "manaCost": 25
            },
            "walrusPunch": {
                "name": "Walrus PUNCH!",
                "type": "ultimate",
                "description": "Tusk's next attack launches the target into the air, dealing critical damage.",
                "critMultiplier": 350, "airTime": 1000, "slowDuration": 4000, "slowPercent": 40,
                "cooldown": 12000, "manaCost": 25
            }
        },
        "talents": {
            "10": ["+25 Ice Shards Damage", "+350 Health"],
            "15": ["+100 Snowball Damage", "+40 Tag Team Bonus Damage"],
            "20": ["+100% Walrus PUNCH! Crit", "-6s Ice Shards Cooldown"],
            "25": ["Walrus PUNCH! Has No Cooldown", "+1.5s Snowball Stun"]
        }
    },
    "underlord": {
        "name": "Underlord",
        "title": "Vrogros",
        "attr": "strength",
        "icon": "underlord",
        "lore": "Commander of the Abyssal Horde, Vrogros opens rifts to bring his army to any battlefield.",
        "baseStats": {
            "maxHp": 135, "maxMana": 90, "hpPerLevel": 30, "manaPerLevel": 20,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 4, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "firestorm": {
                "name": "Firestorm",
                "type": "active",
                "description": "Rains fire over an area, dealing damage and burning enemies over time.",
                "damagePerWave": 20, "waveCount": 6, "burnPercent": 1, "radius": 6,
                "cooldown": 12000, "manaCost": 25, "range": 10
            },
            "pitOfMalice": {
                "name": "Pit of Malice",
                "type": "active",
                "description": "Creates a pit that roots enemies repeatedly.",
                "rootDuration": 1200, "pitDuration": 12000, "radius": 5,
                "cooldown": 18000, "manaCost": 20, "range": 10
            },
            "atrophy_aura": {
                "name": "Atrophy Aura",
                "type": "passive",
                "description": "Reduces enemy attack damage and permanently gains damage when enemies die nearby.",
                "damageReductionPercent": 25, "bonusDamagePerDeath": 5, "radius": 8
            },
            "darkRift": {
                "name": "Dark Rift",
                "type": "ultimate",
                "description": "Opens a rift to teleport Underlord and nearby allies to a friendly unit or building.",
                "castDelay": 6000, "radius": 6,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+15 Firestorm DPS", "+175 Health"],
            "15": ["+100 Pit of Malice AoE", "+3 Atrophy Permanent Bonus Damage"],
            "20": ["+50 Attack Speed", "+0.8s Pit of Malice Root Duration"],
            "25": ["-50s Dark Rift Cooldown", "+15% Atrophy Aura Damage Reduction"]
        }
    },
    "undying": {
        "name": "Undying",
        "title": "Almighty Dirge",
        "attr": "strength",
        "icon": "undying",
        "lore": "A creature of decay, Undying spreads plague and drains the life from his enemies.",
        "baseStats": {
            "maxHp": 125, "maxMana": 90, "hpPerLevel": 28, "manaPerLevel": 20,
            "baseDamage": 16, "damagePerLevel": 2.8, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.0
        },
        "abilities": {
            "decay": {
                "name": "Decay",
                "type": "active",
                "description": "Steals strength from enemies in an area, gaining it for himself.",
                "damage": 25, "strengthSteal": 4, "stealDuration": 40000, "radius": 5,
                "cooldown": 8000, "manaCost": 20, "range": 8
            },
            "soulRip": {
                "name": "Soul Rip",
                "type": "active",
                "description": "Redirects nearby souls to damage an enemy or heal an ally.",
                "damagePerUnit": 8, "healPerUnit": 8, "maxUnits": 10, "radius": 8,
                "cooldown": 6000, "manaCost": 15, "range": 10
            },
            "tombstone": {
                "name": "Tombstone",
                "type": "active",
                "description": "Summons a tombstone that spawns zombies to attack nearby enemies.",
                "tombstoneHp": 200, "zombieDamage": 10, "duration": 30000, "radius": 12,
                "cooldown": 60000, "manaCost": 40, "range": 8
            },
            "fleshGolem": {
                "name": "Flesh Golem",
                "type": "ultimate",
                "description": "Transforms into a flesh golem, gaining bonus health and slowing nearby enemies.",
                "bonusHealthPercent": 35, "slowPercent": 30, "damageAmp": 25, "radius": 8, "duration": 40000,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+100 Decay Radius", "+30 Tombstone Zombie Damage"],
            "15": ["+6 Soul Rip Damage/Heal Per Unit", "+30 Decay Duration"],
            "20": ["+5 Decay Strength Steal", "+500 Tombstone Health"],
            "25": ["Gains Charges on Tombstone", "+40% Flesh Golem Slow"]
        }
    },
    "ursa": {
        "name": "Ursa",
        "title": "Ulfsaar",
        "attr": "agility",
        "icon": "ursa",
        "lore": "A fierce warrior who fights to protect his cubs, Ursa's fury makes him stronger with each strike.",
        "baseStats": {
            "maxHp": 110, "maxMana": 70, "hpPerLevel": 26, "manaPerLevel": 15,
            "baseDamage": 19, "damagePerLevel": 3.4, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "earthshock": {
                "name": "Earthshock",
                "type": "active",
                "description": "Ursa slams the ground, damaging and slowing enemies in front of him.",
                "damage": 40, "slowPercent": 40, "slowDuration": 4000, "radius": 5,
                "cooldown": 7000, "manaCost": 20
            },
            "overpower": {
                "name": "Overpower",
                "type": "active",
                "description": "Ursa attacks with maximum attack speed for a number of attacks.",
                "maxAttackSpeed": True, "attacks": 6, "duration": 20000,
                "cooldown": 8000, "manaCost": 25
            },
            "furySwipes": {
                "name": "Fury Swipes",
                "type": "passive",
                "description": "Each consecutive attack on the same target deals increasing bonus damage.",
                "damagePerStack": 20, "stackDuration": 20000
            },
            "enrage": {
                "name": "Enrage",
                "type": "ultimate",
                "description": "Ursa goes into a rage, multiplying Fury Swipes damage and gaining status resistance.",
                "furySwipesMultiplier": 1.8, "statusResistPercent": 80, "duration": 5000,
                "cooldown": 50000, "manaCost": 0
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+15 Fury Swipes Damage"],
            "15": ["+12 Earthshock Damage", "+350 Health"],
            "20": ["+14% Enrage Status Resistance", "+2 Overpower Attacks"],
            "25": ["+1.5s Enrage Duration", "+15% Earthshock Slow"]
        }
    },
    "vengeful_spirit": {
        "name": "Vengeful Spirit",
        "title": "Shendelzare",
        "attr": "agility",
        "icon": "vengeful_spirit",
        "lore": "Betrayed by her own sister, Shendelzare returns as a spirit seeking vengeance.",
        "baseStats": {
            "maxHp": 90, "maxMana": 90, "hpPerLevel": 22, "manaPerLevel": 20,
            "baseDamage": 17, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "magicMissile": {
                "name": "Magic Missile",
                "type": "active",
                "description": "Fires a missile at a target, stunning and damaging them.",
                "damage": 40, "stunDuration": 1700,
                "cooldown": 9000, "manaCost": 20, "range": 10
            },
            "waveOfTerror": {
                "name": "Wave of Terror",
                "type": "active",
                "description": "Sends a wave that damages and reduces enemy armor while revealing them.",
                "damage": 20, "armorReduction": 5, "duration": 8000, "range": 14,
                "cooldown": 10000, "manaCost": 15
            },
            "vengeanceAura": {
                "name": "Vengeance Aura",
                "type": "passive",
                "description": "Increases attack damage of nearby allies. On death, creates a spirit illusion.",
                "damagePercent": 18, "radius": 10, "illusionDuration": 7000
            },
            "netherSwap": {
                "name": "Nether Swap",
                "type": "ultimate",
                "description": "Swaps positions with a target ally or enemy.",
                "cooldown": 45000, "manaCost": 40, "range": 10
            }
        },
        "talents": {
            "10": ["+175 Health", "+15 Magic Missile Damage"],
            "15": ["+100 Cast Range", "+12% Vengeance Aura Damage"],
            "20": ["+100 Magic Missile Damage", "-4s Wave of Terror Cooldown"],
            "25": ["+200 Magic Missile Stun Duration", "Nether Swap Dispels"]
        }
    },
    "venomancer": {
        "name": "Venomancer",
        "title": "Lesale Deathbringer",
        "attr": "universal",
        "icon": "venomancer",
        "lore": "Once a chemist, Lesale was transformed by his own experiments into a creature of pure venom.",
        "baseStats": {
            "maxHp": 90, "maxMana": 100, "hpPerLevel": 22, "manaPerLevel": 22,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "venomousGale": {
                "name": "Venomous Gale",
                "type": "active",
                "description": "Launches a wave of poison that damages and slows enemies over time.",
                "initialDamage": 20, "damageOverTime": 15, "slowPercent": 50, "duration": 15000, "range": 12,
                "cooldown": 18000, "manaCost": 25
            },
            "poisonSting": {
                "name": "Poison Sting",
                "type": "passive",
                "description": "Venomancer's attacks poison enemies, dealing damage over time and slowing.",
                "damagePerSecond": 6, "slowPercent": 14, "duration": 6000
            },
            "plagueWard": {
                "name": "Plague Ward",
                "type": "active",
                "description": "Summons a ward that attacks enemies and applies Poison Sting.",
                "wardHp": 75, "wardDamage": 20, "wardDuration": 40000,
                "cooldown": 5000, "manaCost": 10, "range": 8
            },
            "poisonNova": {
                "name": "Poison Nova",
                "type": "ultimate",
                "description": "Releases a ring of poison that damages all enemies over time. Cannot kill.",
                "damagePerSecond": 40, "duration": 16000, "radius": 10,
                "cooldown": 100000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+150 Health", "+100 Plague Ward Health"],
            "15": ["+8% Poison Sting Slow", "+10 Venomous Gale DPS"],
            "20": ["Gale Hero Impact Summons 2 Wards", "+10s Poison Nova Duration"],
            "25": ["+8 Plague Ward Damage", "3x Plague Ward HP/Damage"]
        }
    },
    "viper": {
        "name": "Viper",
        "title": "Netherdrake",
        "attr": "agility",
        "icon": "viper",
        "lore": "Born in the Nether Reaches, Viper is a venomous drake who corrupts all he touches.",
        "baseStats": {
            "maxHp": 95, "maxMana": 85, "hpPerLevel": 23, "manaPerLevel": 18,
            "baseDamage": 18, "damagePerLevel": 3.0, "armor": 3, "armorPerLevel": 0.6,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.1
        },
        "abilities": {
            "poisonAttack": {
                "name": "Poison Attack",
                "type": "toggle",
                "description": "Viper's attacks poison enemies, dealing damage over time and slowing.",
                "damagePerSecond": 10, "slowPercent": 20, "duration": 4000, "manaCostPerAttack": 8
            },
            "nethertoxin": {
                "name": "Nethertoxin",
                "type": "active",
                "description": "Covers an area with toxin that damages enemies and disables passive abilities.",
                "damagePerSecond": 25, "duration": 8000, "radius": 5,
                "cooldown": 14000, "manaCost": 20, "range": 10
            },
            "corrosiveSkin": {
                "name": "Corrosive Skin",
                "type": "passive",
                "description": "Viper's skin poisons attackers, dealing damage and slowing them. Also grants magic resistance.",
                "poisonDamage": 15, "slowPercent": 15, "duration": 4000, "magicResist": 15
            },
            "viperStrike": {
                "name": "Viper Strike",
                "type": "ultimate",
                "description": "Launches a venom blast that massively slows and damages an enemy over time.",
                "damage": 100, "slowPercent": 80, "duration": 5000,
                "cooldown": 30000, "manaCost": 40, "range": 8
            }
        },
        "talents": {
            "10": ["+6 Corrosive Skin Stats", "+80 Poison Attack DPS"],
            "15": ["+80 Viper Strike DPS", "+4% Poison Attack Slow"],
            "20": ["+120 Nethertoxin Min/Max Damage", "Nethertoxin Silences"],
            "25": ["+120 Viper Strike DPS", "Poison Attack Affects Buildings"]
        }
    },
    "visage": {
        "name": "Visage",
        "title": "Necro'lic",
        "attr": "universal",
        "icon": "visage",
        "lore": "A gargoyle bound to guard the Narrow Maze, Visage commands familiars and drains souls.",
        "baseStats": {
            "maxHp": 100, "maxMana": 110, "hpPerLevel": 24, "manaPerLevel": 24,
            "baseDamage": 16, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 10, "attackRange": 8, "attackSpeed": 1.0
        },
        "abilities": {
            "graveChillVisage": {
                "name": "Grave Chill",
                "type": "active",
                "description": "Steals movement and attack speed from an enemy.",
                "moveSpeedSteal": 32, "attackSpeedSteal": 64, "duration": 6000,
                "cooldown": 10000, "manaCost": 20, "range": 8
            },
            "soulAssumption": {
                "name": "Soul Assumption",
                "type": "active",
                "description": "Launches a soul blast that deals damage based on nearby damage dealt.",
                "baseDamage": 20, "damagePerCharge": 20, "maxCharges": 6,
                "cooldown": 4000, "manaCost": 15, "range": 10
            },
            "gravekeepersCloak": {
                "name": "Gravekeeper's Cloak",
                "type": "passive",
                "description": "Visage gains layers that reduce damage taken. Layers regenerate over time.",
                "damageReductionPerLayer": 20, "maxLayers": 4, "regenTime": 6000
            },
            "summonFamiliars": {
                "name": "Summon Familiars",
                "type": "ultimate",
                "description": "Summons stone gargoyles that can stun enemies by diving.",
                "familiarCount": 2, "familiarDamage": 30, "stunDuration": 1000, "familiarHp": 300,
                "cooldown": 120000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+25 Soul Assumption Damage per Charge", "+100 Familiar Attack Damage"],
            "15": ["+1 Gravekeeper's Cloak Layer", "+60 Grave Chill Attack/Move Speed Steal"],
            "20": ["+5 Soul Assumption Max Charges", "-3s Grave Chill Cooldown"],
            "25": ["+1 Familiar", "+200 Familiar HP"]
        }
    },
    "void_spirit": {
        "name": "Void Spirit",
        "title": "Inai",
        "attr": "universal",
        "icon": "void_spirit",
        "lore": "Inai guards the thin membrane between the mortal and spirit realms with void magic.",
        "baseStats": {
            "maxHp": 95, "maxMana": 110, "hpPerLevel": 23, "manaPerLevel": 24,
            "baseDamage": 16, "damagePerLevel": 2.9, "armor": 3, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 2.5, "attackSpeed": 1.2
        },
        "abilities": {
            "aetherRemnant": {
                "name": "Aether Remnant",
                "type": "active",
                "description": "Creates a remnant that watches an area, pulling and damaging the first enemy.",
                "damage": 40, "pullDuration": 1400, "watchDuration": 8000,
                "cooldown": 10000, "manaCost": 20, "range": 8
            },
            "dissimilate": {
                "name": "Dissimilate",
                "type": "active",
                "description": "Void Spirit fades into the void, reappearing at a chosen portal to damage enemies.",
                "damage": 60, "portalCount": 9, "duration": 1300, "radius": 4,
                "cooldown": 18000, "manaCost": 25
            },
            "resonantPulse": {
                "name": "Resonant Pulse",
                "type": "active",
                "description": "Emits a pulse that damages enemies and absorbs their damage into a shield.",
                "damage": 40, "shieldPerHero": 60, "shieldDuration": 10000, "radius": 6,
                "cooldown": 16000, "manaCost": 20
            },
            "astralStep": {
                "name": "Astral Step",
                "type": "ultimate",
                "description": "Tears through reality, damaging enemies in a line and applying a slow.",
                "damage": 80, "slowPercent": 40, "charges": 2, "chargeRestoreTime": 20000,
                "cooldown": 0, "manaCost": 30
            }
        },
        "talents": {
            "10": ["+80 Resonant Pulse Damage", "+50 Dissimilate Damage"],
            "15": ["+1 Aether Remnant Charge", "+40 Resonant Pulse Absorb Per Hero"],
            "20": ["+150 Astral Step Damage", "Resonant Pulse Silences"],
            "25": ["+100% Aether Remnant Damage & Duration", "Dissimilate Stuns"]
        }
    },
    "warlock": {
        "name": "Warlock",
        "title": "Demnok Lannik",
        "attr": "intelligence",
        "icon": "warlock",
        "lore": "A master of dark pacts, Warlock binds demons and links the fates of his enemies.",
        "baseStats": {
            "maxHp": 100, "maxMana": 130, "hpPerLevel": 24, "manaPerLevel": 28,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "fatalBonds": {
                "name": "Fatal Bonds",
                "type": "active",
                "description": "Links enemies together. Damage dealt to one is partially shared by all.",
                "damageSharePercent": 25, "maxTargets": 6, "duration": 25000, "radius": 6,
                "cooldown": 24000, "manaCost": 25, "range": 10
            },
            "shadowWord": {
                "name": "Shadow Word",
                "type": "active",
                "description": "Whispers a curse that heals allies or damages enemies over time.",
                "healDamagePerSecond": 15, "duration": 12000,
                "cooldown": 14000, "manaCost": 20, "range": 10
            },
            "upheaval": {
                "name": "Upheaval",
                "type": "active",
                "description": "Channels to slow enemies in an area, increasing over time.",
                "maxSlowPercent": 84, "slowBuildUp": 7, "radius": 8,
                "cooldown": 50000, "manaCostPerSecond": 10, "range": 12
            },
            "chaoticOffering": {
                "name": "Chaotic Offering",
                "type": "ultimate",
                "description": "Summons a Golem that stuns enemies on arrival and fights for Warlock.",
                "stunDamage": 100, "stunDuration": 1500, "golemDamage": 50, "golemDuration": 60000, "radius": 6,
                "cooldown": 170000, "manaCost": 60, "range": 10
            }
        },
        "talents": {
            "10": ["+150 Shadow Word Duration", "+2s Fatal Bonds Duration"],
            "15": ["+10 Shadow Word Heal/Damage", "+6 Upheaval Max Slow"],
            "20": ["+20% Magic Resistance", "+25% Golem Damage"],
            "25": ["Summons 2 Golems", "+20% Fatal Bonds Damage Share"]
        }
    },
    "weaver": {
        "name": "Weaver",
        "title": "Skitskurr",
        "attr": "agility",
        "icon": "weaver",
        "lore": "A creature that exists outside of time, Weaver can unravel and restore the fabric of reality.",
        "baseStats": {
            "maxHp": 80, "maxMana": 90, "hpPerLevel": 20, "manaPerLevel": 20,
            "baseDamage": 18, "damagePerLevel": 3.2, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 12, "attackRange": 8, "attackSpeed": 1.2
        },
        "abilities": {
            "theSwarm": {
                "name": "The Swarm",
                "type": "active",
                "description": "Releases a swarm of beetles that attach to enemies, damaging and reducing armor.",
                "beetleDamage": 8, "armorReduction": 1, "duration": 14000, "beetleCount": 12,
                "cooldown": 29000, "manaCost": 25, "range": 10
            },
            "shukuchi": {
                "name": "Shukuchi",
                "type": "active",
                "description": "Weaver turns invisible and moves at maximum speed, damaging enemies passed.",
                "damage": 30, "duration": 4000, "maxMoveSpeed": True,
                "cooldown": 6000, "manaCost": 15
            },
            "geminate_attack": {
                "name": "Geminate Attack",
                "type": "passive",
                "description": "Weaver's attacks occasionally launch a second attack.",
                "bonusDamage": 20, "cooldown": 6000
            },
            "timeLapse": {
                "name": "Time Lapse",
                "type": "ultimate",
                "description": "Weaver warps backward in time, returning to where he was 5 seconds ago with that HP and mana.",
                "timeRewind": 5000, "cooldown": 60000, "manaCost": 0
            }
        },
        "talents": {
            "10": ["+75 Shukuchi Damage", "+8 Strength"],
            "15": ["+25 Geminate Attack Damage", "+5 The Swarm Beetles"],
            "20": ["+0.5 Swarm Attacks Per Second", "+200 Shukuchi Movement Speed"],
            "25": ["+2 Swarm Armor Reduction", "-25s Time Lapse Cooldown"]
        }
    },
    "windranger": {
        "name": "Windranger",
        "title": "Lyralei",
        "attr": "universal",
        "icon": "windranger",
        "lore": "Orphaned by war, Lyralei found kinship with the wind and became its living embodiment.",
        "baseStats": {
            "maxHp": 90, "maxMana": 100, "hpPerLevel": 22, "manaPerLevel": 22,
            "baseDamage": 16, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.5,
            "moveSpeed": 11, "attackRange": 10, "attackSpeed": 1.1
        },
        "abilities": {
            "shackleshot": {
                "name": "Shackleshot",
                "type": "active",
                "description": "Fires a shackle that latches enemies to trees or each other, stunning them.",
                "stunDuration": 2600, "latchRadius": 4,
                "cooldown": 12000, "manaCost": 20, "range": 10
            },
            "powershot": {
                "name": "Powershot",
                "type": "active",
                "description": "Channels to charge an arrow that damages enemies in a line.",
                "maxDamage": 80, "channelTime": 1000, "range": 16,
                "cooldown": 9000, "manaCost": 20
            },
            "windrun": {
                "name": "Windrun",
                "type": "active",
                "description": "Windranger runs with the wind, gaining evasion and bonus movement speed.",
                "evasionPercent": 100, "moveSpeedBonus": 50, "duration": 6000,
                "cooldown": 12000, "manaCost": 20
            },
            "focusFire": {
                "name": "Focus Fire",
                "type": "ultimate",
                "description": "Windranger channels the wind to attack a single target with maximum attack speed.",
                "attackSpeedBonus": 500, "damageReductionPercent": 25, "duration": 20000,
                "cooldown": 30000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+1.5 Mana Regen", "+100 Powershot Damage"],
            "15": ["+30% Windrun Movement Speed", "+0.8s Shackleshot Duration"],
            "20": ["+15% Focus Fire Damage", "Windrun Grants Invisibility"],
            "25": ["+25% Ministun Powershot", "Focus Fire Kills Reset Focus Fire"]
        }
    },
    "winter_wyvern": {
        "name": "Winter Wyvern",
        "title": "Auroth",
        "attr": "universal",
        "icon": "winter_wyvern",
        "lore": "A wise dragon of the frozen wastes, Auroth uses ice magic to protect allies and confuse enemies.",
        "baseStats": {
            "maxHp": 95, "maxMana": 120, "hpPerLevel": 23, "manaPerLevel": 26,
            "baseDamage": 14, "damagePerLevel": 2.6, "armor": 1, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "arcticBurn": {
                "name": "Arctic Burn",
                "type": "active",
                "description": "Wyvern takes to the air, gaining attack range and burning enemies.",
                "burnDamagePercent": 8, "bonusRange": 4, "duration": 8000,
                "cooldown": 30000, "manaCost": 30
            },
            "splinterBlast": {
                "name": "Splinter Blast",
                "type": "active",
                "description": "Fires a projectile that splinters on impact, damaging and slowing nearby enemies.",
                "damage": 50, "slowPercent": 30, "slowDuration": 4000, "radius": 6,
                "cooldown": 7000, "manaCost": 20, "range": 12
            },
            "coldEmbrace": {
                "name": "Cold Embrace",
                "type": "active",
                "description": "Encases an ally in ice, making them immune to physical damage but frozen in place.",
                "healPerSecond": 20, "baseHeal": 15, "duration": 4000,
                "cooldown": 17000, "manaCost": 20, "range": 8
            },
            "wintersCurse": {
                "name": "Winter's Curse",
                "type": "ultimate",
                "description": "Freezes an enemy and forces nearby allies to attack them.",
                "curseDuration": 5500, "radius": 6,
                "cooldown": 80000, "manaCost": 50, "range": 10
            }
        },
        "talents": {
            "10": ["+300 Health", "+45 Splinter Blast Damage"],
            "15": ["+1.5s Cold Embrace Duration", "+90 Arctic Burn Attack Range"],
            "20": ["+15% Arctic Burn Damage", "Splinter Blast 2s Stun on Primary"],
            "25": ["+1.5s Winter's Curse Duration", "-4s Cold Embrace Cooldown"]
        }
    },
    "witch_doctor": {
        "name": "Witch Doctor",
        "title": "Zharvakko",
        "attr": "intelligence",
        "icon": "witch_doctor",
        "lore": "A healer with dark knowledge, Zharvakko uses voodoo magic to curse enemies and restore allies.",
        "baseStats": {
            "maxHp": 85, "maxMana": 120, "hpPerLevel": 21, "manaPerLevel": 26,
            "baseDamage": 15, "damagePerLevel": 2.8, "armor": 2, "armorPerLevel": 0.4,
            "moveSpeed": 10, "attackRange": 10, "attackSpeed": 1.0
        },
        "abilities": {
            "paralyzing_cask": {
                "name": "Paralyzing Cask",
                "type": "active",
                "description": "Throws a cask that bounces between enemies, stunning them briefly.",
                "damage": 15, "stunDuration": 1000, "bounces": 8, "bounceRange": 6,
                "cooldown": 14000, "manaCost": 20, "range": 10
            },
            "voodoo_restoration": {
                "name": "Voodoo Restoration",
                "type": "toggle",
                "description": "Channels voodoo magic to heal nearby allies over time.",
                "healPerSecond": 15, "radius": 8, "manaCostPerSecond": 8
            },
            "maledict": {
                "name": "Maledict",
                "type": "active",
                "description": "Curses enemies in an area, dealing damage based on how much health they've lost.",
                "burstDamage": 10, "healthLostDamagePercent": 16, "duration": 12000, "radius": 4,
                "cooldown": 20000, "manaCost": 25, "range": 8
            },
            "deathWard": {
                "name": "Death Ward",
                "type": "ultimate",
                "description": "Channels a voodoo ward that rapidly attacks enemies in range.",
                "damagePerBounce": 60, "bounces": 4, "attackInterval": 300, "maxDuration": 8000, "range": 10,
                "cooldown": 80000, "manaCost": 50
            }
        },
        "talents": {
            "10": ["+100 Maledict AoE", "+1 Cask Bounce"],
            "15": ["+120 Death Ward Attack Range", "+2 Maledict Tick Damage"],
            "20": ["+100 Death Ward Damage", "-5s Maledict Cooldown"],
            "25": ["Death Ward Bounces Twice", "Voodoo Restoration Dispels"]
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
