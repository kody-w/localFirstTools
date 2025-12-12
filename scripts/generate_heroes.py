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
