# WoWMon Expansion - Quick Reference Card

## 📊 At a Glance

| Category | Count | Status |
|----------|-------|--------|
| **Total Creatures** | 156 | 110+ to add |
| **Evolution Lines** | 50+ | 38+ to add |
| **Legendary Creatures** | 25 | All new |
| **Regions** | 19 | 12 to add |
| **Gym Leaders** | 8 | 4 to add |
| **Post-Game Islands** | 5 | All new |
| **Types** | 17 | 4 new |
| **Moves** | 180+ | 50+ to add |

---

## 🎯 Top 10 New Creatures to Add First

1. **SHADOWLING → DARKLING → VOID LORD** (Shadow evolution chain)
2. **RAGNAROS** (Fire/Earth/Spirit legendary, Lv 70)
3. **LIGHTLING → RADIANCE → CELESTIAL** (NEW Light type)
4. **EMBERWOLF → HELLHOUND → CERBERUS** (Fire/Beast/Demon)
5. **COPPERBOT → IRONMECH → MITHRIL GOLEM** (NEW Tech type)
6. **TADPOLE → FROGKIN → FROGGERNAUT** (Water alternative)
7. **SNOWPUP → ARCTIC WOLF → WINTER'S HOWL** (Ice/Beast)
8. **PANDAREN CUB → MONK → BREWMASTER** (Warcraft favorite)
9. **DEATHWING** (Dragon/Fire/Earth legendary, roaming)
10. **ARTHAS** (Ultimate boss, Undead/Warrior/Shadow/Ice, Lv 80)

---

## 🗺️ Top 5 Regions to Add First

1. **DARNASSUS FOREST** - Nature/Light theme, Tyrande gym
2. **WINTERSPRING TUNDRA** - Ice/Water theme, Jaina gym (relocated)
3. **BLACKROCK MOUNTAIN** - Fire/Earth theme, Ragnaros legendary
4. **PANDARIA** - Balance theme, Chen Stormstout gym
5. **ICECROWN CITADEL** - Undead theme, Arthas final boss

---

## ⚡ Top 10 New Moves to Add

1. **Void Rift** - Shadow/Special, 120 power (Void Lord signature)
2. **Sulfuras Smash** - Fire/Physical, 110 power (Ragnaros signature)
3. **Holy Nova** - Light/Special, AoE heal + damage
4. **Time Warp** - Magic/Status, grants extra turn
5. **Frostmourne** - Ice/Physical, instant KO chance (Arthas)
6. **Shadow Strike** - Shadow/Physical, always crits in darkness
7. **Fel Storm** - Demon/Status, demon weather setter
8. **Metamorphosis** - Demon/Status, transform boost (Illidan)
9. **Blood Drain** - Undead/Special, lifesteal nuke
10. **Cataclysm** - Multi/Special, terrain destruction (Deathwing)

---

## 🏆 Legendary Priority List

### Must-Have First (Top 5):
1. **RAGNAROS** - Blackrock Mountain, Fire Elemental Lord
2. **DEATHWING** - Roaming, corrupted Dragon Aspect
3. **ARTHAS (LICH KING)** - Icecrown peak, ultimate boss
4. **C'THUN** - Ahn'Qiraj, Old God (quest-based)
5. **ILLIDAN** - Black Temple, Demon Hunter

### Add Second (Next 5):
6. **ALEXSTRASZA** - Wyrmrest Temple, Dragon Aspect
7. **AL'AKIR** - Skywall, Wind Elemental Lord
8. **NEPTULON** - Abyssal Depths, Water Elemental Lord
9. **YSERA** - Emerald Dream, Dream Dragon Aspect
10. **SARGERAS** - Dark Portal, final endgame boss (Lv 85)

---

## 🎮 Implementation Phases (8 Weeks)

### Week 1-2: Foundation
- [ ] 10 new evolution lines (30 creatures)
- [ ] Darnassus Forest region
- [ ] Winterspring Tundra region
- [ ] Tyrande gym leader
- [ ] 5 legendaries (Ragnaros, Al'akir, Neptulon, Therazane, Thunderaan)

### Week 3-4: Expansion
- [ ] 8 dual-type lines (24 creatures)
- [ ] Blackrock Mountain region
- [ ] Netherstorm region
- [ ] Kael'thas gym leader
- [ ] 5 Dragon Aspects

### Week 5-6: Endgame
- [ ] 8 specialty lines (24 creatures)
- [ ] Pandaria region
- [ ] Chen Stormstout gym leader
- [ ] Kezan island (Battle Tower)
- [ ] 5 Old Gods + Titan Watchers

### Week 7-8: Polish
- [ ] Remaining creatures
- [ ] Icecrown Citadel
- [ ] Argus island
- [ ] Lich King + Demon Lords
- [ ] Balance & achievements

---

## 📋 Code Template Quick Copy

### Creature Template:
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
    "description": "Description text"
}
```

### Move Template:
```javascript
"move_id": {
    "name": "Move Name",
    "power": 80,
    "accuracy": 100,
    "pp": 15,
    "type": "type",
    "category": "physical/special/status",
    "description": "Move description"
}
```

### Legendary Template:
```javascript
"legendary_id": {
    "id": "legendary_id",
    "name": "LEGENDARY",
    "type": ["type1", "type2", "type3"],
    "baseHp": 100,
    "baseAttack": 120,
    "baseDefense": 90,
    "baseSpecialAttack": 135,
    "baseSpecialDefense": 95,
    "baseSpeed": 85,
    "evolveLevel": null,
    "evolveTo": null,
    "moves": ["signature", "move2", "move3", "move4"],
    "legendary": true,
    "catchRate": 0.01,
    "description": "Legendary lore"
}
```

---

## 🌟 Type Matchups (NEW TYPES)

### Light Type:
- **Super Effective vs:** Shadow, Undead
- **Not Very Effective vs:** Fire, Nature
- **Weak To:** Shadow
- **Resistant To:** Light, Shadow

### Tech Type:
- **Super Effective vs:** Ice, Earth
- **Not Very Effective vs:** Fire, Electric
- **Weak To:** Electric, Fire
- **Resistant To:** Normal, Flying

### Flying Type:
- **Super Effective vs:** Beast, Nature
- **Not Very Effective vs:** Electric, Ice
- **Weak To:** Electric, Ice
- **Immune To:** Earth

---

## 💰 Stat Budget by Tier

| Tier | Total Stats | Example |
|------|-------------|---------|
| **Basic** | 250-320 | Shadowling (265) |
| **Mid** | 380-450 | Darkling (420) |
| **Final** | 500-580 | Void Lord (550) |
| **Legendary** | 600-720 | Ragnaros (640) |
| **Mythic** | 680-780 | Sargeras (750) |

---

## 🎯 Completion Checklist (Quick Goals)

### Main Story:
- [ ] Beat 8 Gym Leaders
- [ ] Defeat Elite Four
- [ ] Become Champion

### Collection:
- [ ] Catch 50 creatures
- [ ] Catch 100 creatures
- [ ] Catch all 156 creatures
- [ ] Catch 10 legendaries
- [ ] Catch all 25 legendaries

### Post-Game:
- [ ] Battle Tower Floor 50
- [ ] Battle Tower Floor 100
- [ ] Defeat 7 Legion Commanders
- [ ] Defeat Sargeras (Lv 100)
- [ ] Build perfect IV team

### Completion:
- [ ] 100+ achievements
- [ ] All contest ribbons
- [ ] All difficulty modes
- [ ] Living Pokédex
- [ ] All shinies (optional)

---

## 📁 Documentation Files

1. **WOWMON_MASSIVE_CONTENT_EXPANSION_PLAN.md**
   - Full creature list (104+ new)
   - All region designs
   - Complete legendary system
   - Post-game details

2. **WOWMON_EXPANSION_IMPLEMENTATION_GUIDE.md**
   - Code templates
   - Battle mechanics
   - System implementations
   - Quick checklists

3. **WOWMON_VISUAL_ROADMAP.md**
   - Flowcharts and maps
   - Evolution trees
   - Visual progression

4. **WOWMON_EXPANSION_SUMMARY.md**
   - Executive overview
   - Success metrics
   - Phase roadmap

5. **WOWMON_QUICK_REFERENCE.md** (this file)
   - At-a-glance info
   - Priority lists
   - Quick templates

---

## ⚡ Power Moves Cheat Sheet

| Move | Type | Power | Effect |
|------|------|-------|--------|
| Void Rift | Shadow | 120 | Reality tear |
| Sulfuras Smash | Fire | 110 | Burns ground |
| Cataclysm | Multi | 150 | Destroys terrain |
| Frostmourne | Ice | 120 | OHKO chance |
| Time Warp | Magic | 0 | Extra turn |
| Holy Nova | Light | 90 | AoE heal+dmg |
| Metamorphosis | Demon | 0 | Transform |
| Blood Drain | Undead | 100 | Lifesteal |
| Dragon Rage | Dragon | 120 | Fixed 40 dmg |

---

## 🗺️ World Map (ASCII)

```
        [WINTER]
            |
        [DARNASSUS]
            |
[BLACK]--[STORM]--[NETHER]
    |       |         |
[DRAGON]-[GOLD]--[QUELTHALAS]
    |
[PLAGUE]-[SILI]--[PANDARIA]
    |
[ICECROWN]

POST-GAME:
[KEZAN] [ZANDALAR] [BROKEN] [ARGUS] [DREAM]
```

---

## 🔥 Top Team Compositions

### Sweeper Team:
- Void Lord (Shadow/Spirit/Magic)
- Dragon (Dragon/Fire)
- Thunderbird (Electric/Flying/Spirit)
- Archmage (Magic)
- Cerberus (Fire/Demon/Beast)
- Flex slot

### Tank Team:
- Glacier Golem (Ice/Earth/Warrior)
- Celestial (Light/Magic/Spirit)
- Coralossus (Water/Earth/Magic)
- Ancient Guardian (Nature/Magic)
- Royal Griffon (Flying/Beast/Light)
- Flex slot

### Legendary Team:
- Ragnaros (Fire/Earth/Spirit)
- Deathwing (Dragon/Fire/Earth)
- Arthas (Undead/War/Shad/Ice)
- Sargeras (Demon/Fire/War/Mag)
- Alexstrasza (Dragon/Fire/Light)
- C'Thun (Shadow/Magic/Spirit)

---

## 💡 Quick Tips

### For Fast Implementation:
1. Start with 5-10 creatures at a time
2. Build one complete region before moving on
3. Test evolution chains immediately
4. Add legendaries after main content works
5. Balance stats in phases, not all at once

### For Best Results:
1. Prioritize creatures players will use most
2. Make each region feel unique
3. Give legendaries memorable encounters
4. Create diverse team building options
5. Test difficulty modes early

### For Maximum Impact:
1. Lead with popular Warcraft characters
2. Include fan-favorite creatures
3. Make legendaries feel epic
4. Design clear progression curve
5. Create rewarding post-game

---

**Files Location:** `/Users/kodyw/Documents/GitHub/localFirstTools3/`

**Ready to expand WoWMon!** 🎮🔥
