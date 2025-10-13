# WoWMon - Casual Player UI Mockups & Visual Guide

**Visual reference for implementing casual player features**

---

## 1. Tutorial System UI

### Welcome Screen
```
┌─────────────────────────────────────────────────┐
│                                                 │
│         🌟 Welcome to WoWMon! 🌟                │
│                                                 │
│   I'm Professor Thrall, and I'll guide you     │
│   on an amazing journey through Azeroth!       │
│                                                 │
│   Ready to start your adventure?               │
│                                                 │
│   [▶ START ADVENTURE]   [↻ SKIP TUTORIAL]      │
│                                                 │
│   (Tutorial takes ~10 minutes)                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Starter Selection Screen
```
┌─────────────────────────────────────────────────────────────────────────┐
│  CHOOSE YOUR FIRST COMPANION                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐              │
│  │   MURLOC      │  │     WISP      │  │      IMP      │              │
│  │   🐟 (Water)  │  │  🌿 (Nature)  │  │  🔥 (Fire)    │              │
│  │               │  │               │  │               │              │
│  │  ⭐⭐⭐☆☆      │  │  ⭐⭐⭐⭐☆      │  │  ⭐⭐☆☆☆      │              │
│  │  Beginner     │  │  Intermediate │  │  Advanced     │              │
│  │               │  │               │  │               │              │
│  │ Balanced stats│  │ Fast & can    │  │ High damage,  │              │
│  │ Easy to learn │  │ heal itself   │  │ fragile       │              │
│  │               │  │               │  │               │              │
│  │  [SELECT] →   │  │   [SELECT] →  │  │  [SELECT] →   │              │
│  └───────────────┘  └───────────────┘  └───────────────┘              │
│                                                                         │
│  ℹ Recommended for new players: MURLOC                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Tutorial Battle Tooltip
```
┌──────────────────────────────────────┐
│  💡 TUTORIAL TIP                     │
├──────────────────────────────────────┤
│                                      │
│  Your Murloc knows 4 moves!         │
│                                      │
│  Each move has different:           │
│  • Type (Water, Fire, etc.)         │
│  • Power (damage dealt)             │
│  • Uses (PP - Power Points)         │
│                                      │
│  Try WATER GUN - it's effective     │
│  against this creature!             │
│                                      │
│  [OK, GOT IT]  [TELL ME MORE]       │
└──────────────────────────────────────┘
```

---

## 2. Difficulty Selection UI

### Difficulty Selection Modal
```
┌──────────────────────────────────────────────────────────────────────┐
│  🎮 CHOOSE YOUR ADVENTURE STYLE                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🌱 EASY MODE - "Casual Adventure"                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Perfect for: Newcomers, casual play, relaxed fun           │   │
│  │                                                              │   │
│  │  ✓ +20% your creature stats                                 │   │
│  │  ✓ Enemies have -20% stats                                  │   │
│  │  ✓ +50% XP and Gold earned                                  │   │
│  │  ✓ Better catch rates                                       │   │
│  │  ✓ Auto-revive once per battle                              │   │
│  │                                                              │   │
│  │  [▶ SELECT EASY MODE]                                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ⚔ NORMAL MODE - "Classic Journey"                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Perfect for: Balanced experience, standard gameplay        │   │
│  │                                                              │   │
│  │  • Standard stats for all creatures                         │   │
│  │  • Fair challenge throughout                                │   │
│  │  • Classic progression curve                                │   │
│  │                                                              │   │
│  │  [▶ SELECT NORMAL MODE]  ⭐ RECOMMENDED                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  🔥 HARD MODE - "Champion's Challenge"                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Perfect for: Veterans, challenge seekers                   │   │
│  │                                                              │   │
│  │  ⚠ Enemies have +20% stats                                  │   │
│  │  ⚠ Smarter AI opponents                                     │   │
│  │  ⚠ Level caps for gym battles                               │   │
│  │  ✓ +50% Gold rewards                                        │   │
│  │                                                              │   │
│  │  [▶ SELECT HARD MODE]                                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ℹ You can change difficulty any time in Settings!                  │
│                                                                      │
│  [LEARN MORE]  [BACK]                                               │
└──────────────────────────────────────────────────────────────────────┘
```

### Difficulty Indicator (In-Game)
```
Top-right corner of screen:

┌────────────────┐
│ 🌱 EASY MODE   │
│ Boosts: ON     │
└────────────────┘
```

---

## 3. Battle QoL Features

### Move Selection with Effectiveness Preview
```
┌───────────────────────────────────────────────────────────────────────┐
│  YOUR TURN - Select a move:                                          │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ⭐ WATER GUN (Recommended)                    PP: ████████░░ 8/10   │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Type: 💧 Water  |  Power: 40  |  Accuracy: 100%              │  │
│  │  🎯 SUPER EFFECTIVE against Fire! (2x damage)                 │  │
│  │  Estimated damage: ~45-55 HP                                  │  │
│  │                                                     [SELECT] → │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  TACKLE                                            PP: ██████░░░░ 6/10│
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Type: ⚪ Normal  |  Power: 35  |  Accuracy: 95%              │  │
│  │  → Normal damage (1x)                                         │  │
│  │  Estimated damage: ~30-40 HP                                  │  │
│  │                                                     [SELECT] → │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  BUBBLE                                            PP: ██████████ 10/10│
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Type: 💧 Water  |  Power: 20  |  Accuracy: 100%              │  │
│  │  🎯 SUPER EFFECTIVE! (2x) - Low power                         │  │
│  │  May lower enemy speed                                        │  │
│  │                                                     [SELECT] → │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  BITE                                              PP: ████████░░ 8/10│
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Type: ⚫ Shadow  |  Power: 60  |  Accuracy: 100%             │  │
│  │  → Normal damage                                              │  │
│  │  May cause flinching                                          │  │
│  │                                                     [SELECT] → │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  [BAG]  [SWITCH]  [RUN]                                              │
└───────────────────────────────────────────────────────────────────────┘
```

### Battle Status Tooltips
```
Enemy Creature HP Bar:
┌──────────────────────────────┐
│  ENEMY FLAMELING  Lv. 8      │
│  HP: ███████████░░░░ 70%     │  ← Hover/tap here
│  🔥 BURNED                   │
└──────────────────────────────┘
         ↓
┌───────────────────────────────────┐
│  💡 BURN STATUS                   │
├───────────────────────────────────┤
│  • Takes damage each turn        │
│  • Physical attacks reduced 50%  │
│  • Lasts until healed            │
│                                  │
│  Use: Burn Heal or Pokecenter   │
└───────────────────────────────────┘
```

### Battle Speed Controls
```
Top-left of battle screen:

┌─────────────────────────┐
│  BATTLE SPEED           │
│  ○ Normal  ● Fast       │
│  ○ Ultra   ○ Instant    │
│                         │
│  [⚙ Settings]           │
└─────────────────────────┘
```

### Battle History Log
```
Bottom-left corner (collapsible):

┌─────────────────────────────────────┐
│  📜 BATTLE LOG          [−] [✕]     │
├─────────────────────────────────────┤
│  Turn 3:                            │
│  → You: WATER GUN (Super effective!)│
│     Enemy took 52 damage!           │
│  → Enemy: EMBER (Not very effective)│
│     You took 18 damage!             │
│                                     │
│  Turn 2:                            │
│  → You: TACKLE                      │
│     Enemy took 35 damage!           │
│  → Enemy: SUNNY DAY                 │
│     Weather changed to sunny!       │
│                                     │
│  [Scroll for more ↓]                │
└─────────────────────────────────────┘
```

---

## 4. Auto-Battle UI

### Auto-Battle Control Panel
```
┌──────────────────────────────────────────────────────────────────────┐
│  🤖 AUTO-BATTLE CONTROLS                                  [ACTIVE ▶]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Status: ⚡ RUNNING                                                  │
│  Speed:  ⚡⚡⚡□□  [Fast]                                              │
│          └─────────┘                                                │
│           1  2  3  4  5                                             │
│                                                                      │
│  STRATEGY: ● Smart AI                                               │
│            ○ Aggressive                                             │
│            ○ Defensive                                              │
│            ○ Custom                                                 │
│                                                                      │
│  OPTIONS:                                                           │
│  ☑ Auto-switch for type advantage                                  │
│  ☑ Use healing items when low HP                                   │
│  ☐ Try to catch wild creatures                                     │
│  ☑ Skip battle animations                                          │
│                                                                      │
│  STOP CONDITIONS:                                                   │
│  ☑ Team member faints                                              │
│  ☑ HP drops below 30%                                              │
│  ☑ Rare/shiny creature found                                       │
│  ☑ Evolution available                                             │
│  ☐ Status effect applied                                           │
│                                                                      │
│  STATISTICS:                                                        │
│  Battles: 15  |  Wins: 14  |  XP: 1,250  |  Gold: 450              │
│                                                                      │
│  [⏸ PAUSE]  [⏹ STOP]  [⚙ CONFIGURE]  [❓ HELP]                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Auto-Battle In-Progress Indicator
```
Small floating indicator during auto-battle:

┌─────────────────────┐
│  🤖 AUTO-BATTLE     │
│  Battle #7          │
│  XP: 850            │
│  [⏸] [⏹]           │
└─────────────────────┘
```

### Training Grounds Interface
```
┌──────────────────────────────────────────────────────────────────────┐
│  🏋 TRAINING GROUNDS                                   [Unlocked ✓]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Quick level-up your team with intense training!                   │
│                                                                      │
│  SELECT TRAINING MODE:                                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  ⚡ QUICK TRAINING (10 battles)                             │    │
│  │  Duration: ~5 minutes  |  Cost: 100 gold                   │    │
│  │  Expected: ~500 XP per creature, ~200 gold reward          │    │
│  │                                            [START TRAINING]  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  💪 EXTENDED TRAINING (30 battles)                          │    │
│  │  Duration: ~15 minutes  |  Cost: 250 gold                  │    │
│  │  Expected: ~1,500 XP per creature, ~600 gold reward        │    │
│  │                                            [START TRAINING]  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  🌙 OVERNIGHT TRAINING (while you're away)                  │    │
│  │  Duration: Up to 4 hours  |  Cost: FREE                    │    │
│  │  Simulated training - safe, no creatures can faint         │    │
│  │  Returns: XP, gold, items                                  │    │
│  │                                            [SCHEDULE]        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  CUSTOM SETTINGS:                                                   │
│  Target Level: [20▼]  |  Focus: [All Party ▼]  |  Safety: [ON]    │
│                                                                      │
│  [BACK]  [VIEW TRAINING HISTORY]                                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Team Management UI

### Team Builder Assistant
```
┌──────────────────────────────────────────────────────────────────────┐
│  👥 TEAM BUILDER ASSISTANT                                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CURRENT TEAM ANALYSIS:                                             │
│                                                                      │
│  1. MURLOC (Water)      Lv.18  HP: 85/95   [⭐ FAVORITE]            │
│  2. FLAMELING (Fire)    Lv.15  HP: 62/68                            │
│  3. WISP (Nature)       Lv.17  HP: 70/75                            │
│  4. (Empty)                                                         │
│  5. (Empty)                                                         │
│  6. (Empty)                                                         │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  TYPE COVERAGE:                                                     │
│  ✓ Water (2 moves)      Strong vs: Fire, Earth                     │
│  ✓ Fire (3 moves)       Strong vs: Nature, Ice                     │
│  ✓ Nature (2 moves)     Strong vs: Water, Earth                    │
│  ⚠ Missing: Shadow, Dragon, Beast types                            │
│                                                                      │
│  WEAKNESSES:                                                        │
│  ⚠ Vulnerable to: Earth attacks (2 creatures weak)                 │
│  ⚠ Vulnerable to: Dragon attacks (entire team)                     │
│                                                                      │
│  RECOMMENDATIONS:                                                   │
│  → Add GNOLL (Beast) for physical power                            │
│  → Add GHOUL (Undead/Shadow) for type coverage                     │
│  → Consider evolving FLAMELING (ready at Lv.20)                    │
│                                                                      │
│  SUGGESTED TEAM CHANGES:                                            │
│  [View Suggestions]  [Auto-Optimize]  [Keep Current]               │
│                                                                      │
│  [SAVE AS PRESET]  [LOAD PRESET]  [CLOSE]                          │
└──────────────────────────────────────────────────────────────────────┘
```

### Team Presets UI
```
┌──────────────────────────────────────────────┐
│  📋 TEAM PRESETS                             │
├──────────────────────────────────────────────┤
│                                              │
│  SLOT 1: "Balanced Squad" ✓ ACTIVE          │
│  ├─ Murloc (Water) Lv.18                    │
│  ├─ Flameling (Fire) Lv.15                  │
│  ├─ Wisp (Nature) Lv.17                     │
│  └─ (3 empty slots)                         │
│  [LOAD] [EDIT] [RENAME]                     │
│                                              │
│  SLOT 2: "Dragon Team"                      │
│  ├─ Whelp (Dragon) Lv.12                    │
│  ├─ Drake (Dragon/Fire) Lv.25               │
│  └─ (4 empty slots)                         │
│  [LOAD] [EDIT] [RENAME] [DELETE]            │
│                                              │
│  SLOT 3: [EMPTY]                            │
│  [SAVE CURRENT TEAM]                        │
│                                              │
│  [QUICK SWAP] [BACK]                        │
└──────────────────────────────────────────────┘
```

---

## 6. Accessibility UI

### Accessibility Settings Panel
```
┌──────────────────────────────────────────────────────────────────────┐
│  ♿ ACCESSIBILITY SETTINGS                                [SAVE] [✕]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  VISION                                                             │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Colorblind Mode:    [Normal ▼]                            │    │
│  │                      • Normal (standard colors)             │    │
│  │                      • Red-blind (Protanopia)               │    │
│  │                      • Green-blind (Deuteranopia)           │    │
│  │                      • Blue-blind (Tritanopia)              │    │
│  │                      • Grayscale (Achromatopsia)            │    │
│  │                                                             │    │
│  │  Text Size:          [● 100%] [○ 120%] [○ 140%] [○ 160%]   │    │
│  │  Font:               [☐ Dyslexic-Friendly Font]             │    │
│  │  Contrast:           [● Normal] [○ High] [○ Maximum]        │    │
│  │  Effects:            [☐ Reduce visual effects]              │    │
│  │                      [☐ Solid backgrounds]                  │    │
│  │                      [☐ Remove screen shake]                │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  MOTOR                                                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  [☐ One-handed mode]                                        │    │
│  │  [☐ Sticky keys]                                            │    │
│  │  [☐ Toggle sprint (instead of hold)]                       │    │
│  │  Button hold time: [0.5s ━━━━━━━━━━ 2.0s]                  │    │
│  │  [☐ Auto-confirm after delay (2s)]                         │    │
│  │  [☐ Skip button mashing]                                   │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  COGNITIVE                                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  [☐ Simplified text mode]                                  │    │
│  │  Reading speed: [● Normal] [○ Slow] [○ Very Slow]          │    │
│  │  [☑ Show recommended actions]                              │    │
│  │  [☑ Double-confirm important choices]                      │    │
│  │  [☐ Focus mode (reduce UI clutter)]                        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  AUDIO                                                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  [☑ Audio cues for events]                                 │    │
│  │  [☑ Critical HP warning sound]                             │    │
│  │  [☑ Battle phase sounds]                                   │    │
│  │  [☐ Extended audio descriptions]                           │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  [RESTORE DEFAULTS]  [TEST SETTINGS]  [SAVE & CLOSE]               │
└──────────────────────────────────────────────────────────────────────┘
```

### Colorblind Mode Preview
```
NORMAL MODE:
  🔥 Fire (Red)     💧 Water (Blue)    🌿 Nature (Green)

PROTANOPIA (Red-blind):
  🟧 Fire (Orange+Bold)  💧 Water (Dark Blue+Stripe)  🟨 Nature (Yellow)

DEUTERANOPIA (Green-blind):
  🟧 Fire (Orange)  💧 Water (Blue)  🟫 Nature (Brown)

TRITANOPIA (Blue-blind):
  🟥 Fire (Red-Pink)  🔷 Water (Cyan)  💚 Nature (Teal)

ACHROMATOPSIA (Full colorblind):
  ▓ Fire (Dense)  ≈ Water (Waves)  ░ Nature (Dots)
```

---

## 7. Catching & Collection UI

### Catch Probability Display
```
┌───────────────────────────────────────────────┐
│  WILD MURLOC (Level 8)                        │
│  HP: ████████░░ 80%  [⚠ Too high!]           │
│  Status: None                                │
│                                              │
│  SELECT CAPTURE ITEM:                        │
│                                              │
│  ○ CAPTURE STONE (x12)                       │
│    Catch Rate: 35% ⚠ FAIR                   │
│    └─ 💡 Lower HP first! Aim for <50%       │
│                                              │
│  ● SUPER STONE (x5)                          │
│    Catch Rate: 65% ✓ GOOD                   │
│    └─ ⭐ Recommended!                        │
│                                              │
│  ○ ULTRA STONE (x1)                          │
│    Catch Rate: 90% ✓✓ EXCELLENT             │
│    └─ Save for rare creatures                │
│                                              │
│  TIPS:                                       │
│  • Red HP bar = best chance                 │
│  • Status effects help (sleep, paralyze)    │
│  • Better balls = better odds               │
│                                              │
│  [THROW]  [CANCEL]  [MORE INFO]             │
└───────────────────────────────────────────────┘
```

### Quick Catch Mode Toggle
```
┌────────────────────────────────────────┐
│  ⚡ QUICK CATCH MODE                   │
├────────────────────────────────────────┤
│  Status: [ON ✓]  [OFF]                │
│                                        │
│  When enabled:                         │
│  • Press Q to auto-throw best ball    │
│  • Repeats until caught or fled       │
│  • Great for common creatures          │
│                                        │
│  Settings:                             │
│  Auto-ball: [Best Available ▼]        │
│  Stop if HP >: [50% ▼]                │
│  Max attempts: [5 ▼]                  │
│                                        │
│  [CONFIGURE]  [CLOSE]                 │
└────────────────────────────────────────┘
```

### Living Dex Progress Tracker
```
┌──────────────────────────────────────────────────────────────────────┐
│  📚 LIVING DEX TRACKER                             [28/46 = 61%] ✓   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PROGRESS BY TYPE:                                                  │
│  💧 Water:  ████████░░ 6/8    (75%)                                 │
│  🔥 Fire:   ██████████ 5/5    (100%) ✓ COMPLETE                     │
│  🌿 Nature: ██████░░░░ 4/7    (57%)                                 │
│  🐉 Dragon: ████░░░░░░ 2/5    (40%)                                 │
│  ⚫ Shadow: ██████░░░░ 3/6    (50%)                                 │
│  🏔 Earth:  ████████░░ 4/5    (80%)                                 │
│  ☠ Undead: ██████░░░░ 3/6    (50%)                                 │
│  ⚪ Normal: ████░░░░░░ 1/4    (25%)                                 │
│                                                                      │
│  MISSING CREATURES (18):                                            │
│                                                                      │
│  🔥 Fire Line: [All caught! ✓]                                      │
│                                                                      │
│  💧 Water Line:                                                      │
│  → Murloc King (Evolve Murloc Warrior to Lv.32)                    │
│  → Naga (Rare spawn: Darkshore Beach, 10% rate)                    │
│                                                                      │
│  🐉 Dragon Line:                                                     │
│  → Drake (Evolve Whelp to Lv.25)                                    │
│  → Dragon (Evolve Drake to Lv.45)                                   │
│  → Ancient Dragon (Post-game legendary)                             │
│                                                                      │
│  [VIEW ALL]  [FILTER]  [SORT]  [WHERE TO FIND]  [CLOSE]            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 8. Progression & Guidance UI

### Level Recommendation Badge
```
Before entering gym:

┌─────────────────────────────────────────┐
│  ⚠ IRONFORGE GYM AHEAD                  │
├─────────────────────────────────────────┤
│                                         │
│  Recommended Level: 20-25              │
│  Your Team Average:  18                │
│                                         │
│  Status: ⚠ SLIGHTLY UNDERLEVELED       │
│                                         │
│  Suggestions:                          │
│  • Train in nearby caves (+2 levels)  │
│  • Battle area trainers (3 available) │
│  • Use Training Grounds (Quick!)       │
│                                         │
│  [CONTINUE ANYWAY]  [VIEW TRAINING]    │
└─────────────────────────────────────────┘
```

### Achievement Progress Notifications
```
Bottom-right popup:

┌────────────────────────────────────┐
│  🏆 ACHIEVEMENT PROGRESS           │
├────────────────────────────────────┤
│  "Catch 10 Creatures"              │
│  Progress: ████████░░ 8/10 (80%)  │
│                                    │
│  Reward: Pokédex Scan Feature      │
│  (See catch rates in battle!)      │
│                                    │
│  [VIEW ALL]  [✕]                   │
└────────────────────────────────────┘
```

### Evolution Reminder
```
Persistent notification:

┌──────────────────────────────────────────┐
│  🌟 EVOLUTION READY!                     │
├──────────────────────────────────────────┤
│  Your MURLOC can evolve!                │
│                                          │
│  MURLOC → MURLOCWARRIOR                 │
│                                          │
│  Stats Preview:                         │
│  HP:      60 → 70  (+10)               │
│  Attack:  49 → 65  (+16)               │
│  Defense: 49 → 58  (+9)                │
│  Speed:   45 → 60  (+15)               │
│                                          │
│  New Moves: Water Pulse, Scald         │
│                                          │
│  [EVOLVE NOW]  [REMIND LATER]  [NEVER]  │
└──────────────────────────────────────────┘
```

---

## 9. Family Mode UI

### Family Mode Setup
```
┌──────────────────────────────────────────────────────────────────────┐
│  👨‍👩‍👧‍👦 FAMILY MODE SETTINGS                       [🔒 LOCK SETTINGS]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PLAYER PROFILE:                                                    │
│  Name: [Alex]                Age: [8] years old                     │
│  Account Type: ● Child  ○ Teen  ○ Adult                             │
│                                                                      │
│  TIME LIMITS:                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Play Session Limit:     [30 minutes ▼]                    │    │
│  │  Daily Limit:            [1 hour ▼]                        │    │
│  │  Weekly Limit:           [7 hours ▼]                       │    │
│  │                                                             │    │
│  │  [☑] Show 5-minute warning before limit                    │    │
│  │  [☑] Auto-pause when time limit reached                    │    │
│  │  [☑] Require parent permission to extend                   │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  CONTENT SETTINGS:                                                  │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  [☑] Kid-friendly difficulty (can't lose battles)          │    │
│  │  [☑] Simplified menus (picture-based)                      │    │
│  │  [☑] No complex mechanics (status effects off)             │    │
│  │  [☑] Auto-best move suggestions                            │    │
│  │  [☐] Text narration (read aloud)                           │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  PARENT MONITORING:                                                 │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  [☑] View child's achievements and progress                │    │
│  │  [☑] Receive weekly play report                            │    │
│  │  Email: [parent@email.com]                                 │    │
│  │                                                             │    │
│  │  [VIEW PROGRESS REPORT]  [VIEW PLAY HISTORY]               │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  PARENTAL LOCK:                                                     │
│  Password: [••••]  (Required to change settings or disable)         │
│                                                                      │
│  [SAVE & LOCK]  [CANCEL]  [DISABLE FAMILY MODE]                    │
└──────────────────────────────────────────────────────────────────────┘
```

### Time Limit Warning
```
┌────────────────────────────────┐
│  ⏰ TIME LIMIT WARNING          │
├────────────────────────────────┤
│                                │
│  5 minutes remaining!          │
│                                │
│  Time played today: 55 min     │
│  Daily limit: 1 hour           │
│                                │
│  Please save your game soon.   │
│                                │
│  [OK]  [REQUEST MORE TIME]     │
└────────────────────────────────┘
```

---

## 10. Wellness Features UI

### Break Reminder
```
Full-screen dimmed overlay:

┌──────────────────────────────────────────────┐
│                                              │
│            🧘 TIME FOR A BREAK!              │
│                                              │
│      You've been playing for 45 minutes     │
│                                              │
│      Take a moment to:                      │
│      • Stretch your arms and legs           │
│      • Look away from the screen            │
│      • Get some water                       │
│      • Rest your eyes                       │
│                                              │
│      Game auto-paused.                      │
│                                              │
│      [CONTINUE PLAYING]  [SNOOZE 15 MIN]    │
│                                              │
└──────────────────────────────────────────────┘
```

### Play Time Tracker
```
┌──────────────────────────────────────────────────────────────────────┐
│  📊 PLAY TIME STATISTICS                                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TODAY:                         ████████░░░░░░░░░░  1h 23m / 2h    │
│  THIS WEEK:                     ████████████░░░░░░  8h 45m / 12h   │
│  TOTAL PLAYTIME:                                     45h 12m        │
│                                                                      │
│  AVERAGE SESSION:  35 minutes                                       │
│  SESSIONS TODAY:   3                                                │
│  LONGEST SESSION:  1h 15m                                           │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  PROGRESS THIS WEEK:                                                │
│  ✓ Caught first Dragon-type creature                               │
│  ✓ Defeated 3rd Gym Leader                                         │
│  ✓ Evolved 5 creatures                                              │
│  ✓ Completed 10 trainer battles                                    │
│                                                                      │
│  WELLNESS GOALS:                                                    │
│  ✓ Took 3 breaks (Goal: 2+)                                        │
│  ✓ Avg session < 60 min (Goal: < 90 min)                           │
│  ⚠ Played after bedtime 1x (Goal: 0)                               │
│                                                                      │
│  [SET GOALS]  [VIEW DETAILED STATS]  [EXPORT DATA]  [CLOSE]        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### CSS Classes for Quick Styling

```css
/* Tutorial highlights */
.tutorial-highlight {
    outline: 3px solid #FFD700;
    animation: pulse 2s infinite;
}

/* Effectiveness indicators */
.super-effective { color: #00FF00; }
.not-effective { color: #FF6666; }
.neutral { color: #CCCCCC; }

/* Difficulty badges */
.difficulty-easy { background: #4CAF50; }
.difficulty-normal { background: #2196F3; }
.difficulty-hard { background: #F44336; }

/* Status icons */
.status-burn { color: #FF6B35; }
.status-poison { color: #9B4DCA; }
.status-paralyze { color: #FFD93D; }
.status-sleep { color: #6C7A89; }
.status-freeze { color: #00D4FF; }

/* Colorblind patterns */
.type-fire-pattern { background: repeating-linear-gradient(45deg, #000, #000 2px, transparent 2px, transparent 4px); }
.type-water-pattern { background: repeating-linear-gradient(0deg, #000, #000 1px, transparent 1px, transparent 3px); }
.type-nature-pattern { background: radial-gradient(circle, #000 10%, transparent 10%); }
```

### Keyboard Shortcuts Reference

```
GLOBAL SHORTCUTS:
A / Z / Enter    - Confirm/Interact
B / X / Escape   - Cancel/Back
Arrow Keys       - Navigate/Move
Q                - Quick Catch (when enabled)
Tab              - Cycle UI elements
Shift + A        - Auto-Battle Toggle
Ctrl + S         - Quick Save
Ctrl + M         - Toggle Map

BATTLE SHORTCUTS:
1-4              - Quick move select
F                - Fast forward battle
Space            - Skip animation
S                - Switch creature
B                - Open bag
```

---

**Visual Design Philosophy:**
- Clean, readable typography
- High contrast text and backgrounds
- Clear visual hierarchy
- Consistent iconography
- Accessible color schemes
- Generous spacing and padding
- Helpful tooltips everywhere
- Visual feedback for all actions
- Progress bars for everything
- Always show next steps

**Mobile Considerations:**
- All UI elements tappable (min 44x44px)
- Swipe gestures for common actions
- Collapsible panels to save space
- Bottom navigation for thumbs
- Haptic feedback on actions
- Portrait and landscape support

---

**File:** WOWMON_CASUAL_UI_MOCKUPS.md
**Created:** 2025-10-12
**Purpose:** Visual reference for casual player features
**Status:** Ready for implementation
