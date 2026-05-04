# WowMon Team Builder Guide

## Overview

The WowMon Team Builder is a comprehensive tool for planning and analyzing Pokemon-style teams in the WowMon universe. It provides advanced type coverage analysis, defensive weakness detection, and team management features.

## Features

### 1. Team Management System

#### Adding Creatures
- **Click on any empty slot** to select it (indicated by green outline)
- **Search and select** a creature from the creature list on the right
- Creatures are automatically added to the selected slot
- If no slot is selected, creatures are added to the first available slot

#### Removing Creatures
- Click the **× button** in the top-right corner of any filled slot
- The creature will be immediately removed from your team

#### Adjusting Levels
- Each creature has a **level input field**
- Set levels from 1-100
- Levels are saved automatically when changed

### 2. Type Coverage Analysis

#### Offensive Coverage
The **Offensive Coverage** section shows how well your team can hit each type:

- **Green (Super Effective)**: Your team has 2× or better coverage against this type
- **Light Green (Effective)**: Your team has moves that are effective (>1×)
- **Red (Not Effective)**: Your team struggles against this type
- **Gray (Immune)**: This type is completely immune to your attacks

#### Coverage Multipliers
- **×2.0**: Super effective damage
- **×1.5**: Moderately effective
- **×1.0**: Neutral damage
- **×0.5**: Not very effective
- **×0.0**: Immune (no damage)

### 3. Defensive Analysis

#### Weaknesses
Shows types your team is vulnerable to:
- **4× Weakness** (Pulsing Red): Multiple team members share a weakness to this type
- **2× Weakness** (Red): Standard weakness

#### Resistances
Types your team can resist effectively (shown in green)

#### Immunities
Types your team is completely immune to (shown in gray)
- Number in parentheses shows how many team members have the immunity

### 4. Team Statistics

The stats panel displays:
- **Average Level**: Mean level of all team members
- **Average BST**: Base Stat Total (HP + Attack + Defense + Speed)
- **Average HP**: Mean HP stat
- **Average Attack**: Mean Attack stat
- **Average Defense**: Mean Defense stat
- **Average Speed**: Mean Speed stat
- **Type Diversity**: How many different types are represented

### 5. Speed Tiers

Shows your team sorted by Speed stat (fastest first):
- Helps determine who moves first in battle
- Critical for planning strategies
- Speed ties are resolved randomly in actual battles

### 6. Saved Teams

#### Saving a Team
1. Build your team
2. Click **Save Team** button
3. Enter a team name
4. Team is saved to local storage

#### Loading a Team
- Click **Load** button on any saved team
- Current team will be replaced

#### Deleting a Team
- Click **Delete** button on any saved team
- Confirm deletion (cannot be undone)

### 7. Import/Export

#### Exporting Teams
1. Click **Export JSON** button
2. JSON data appears in modal
3. Click **Copy to Clipboard** to copy
4. Share with friends or save externally

#### Importing Teams
1. Click **Import JSON** button
2. Paste JSON data into text area
3. Click **Import** button
4. Team is loaded (current team is replaced)

#### Export Format
```json
{
  "version": "1.0",
  "team": [
    {
      "id": "murloc",
      "name": "MURLOC",
      "type": ["water", "beast"],
      "level": 25,
      "baseHp": 45,
      "baseAttack": 49,
      "baseDefense": 49,
      "baseSpeed": 45
    }
  ],
  "exported": "2025-10-12T..."
}
```

### 8. Quick Actions

#### Clear Team
- Removes all creatures from current team
- Confirmation required
- Cannot be undone (unless team was saved)

#### Random Team
- Generates a completely random team of 6 creatures
- Random levels between 5-50
- Great for testing coverage or trying new strategies

## Type Effectiveness Chart

### WowMon Type System

| Attacking Type | Super Effective Against | Not Effective Against | Immune To |
|---------------|------------------------|----------------------|-----------|
| **Water** | Fire, Earth | Water, Nature | - |
| **Fire** | Nature, Ice | Water, Fire, Earth | - |
| **Nature** | Water, Earth | Fire, Beast | - |
| **Earth** | Fire, Electric | Nature, Water | - |
| **Ice** | Nature, Beast | Fire, Water | - |
| **Electric** | Water, Beast | Electric | Earth |
| **Beast** | Normal (1.5×) | Beast, Shadow | - |
| **Shadow** | Spirit, Magic | Shadow, Normal | - |
| **Magic** | Shadow, Demon | Magic | - |
| **Demon** | Spirit, Nature (1.5×) | Demon, Magic | - |
| **Spirit** | Demon, Shadow (1.5×) | Spirit | - |
| **Normal** | - | Earth | - |

### Type Colors
- **Water**: Blue (#4A90E2)
- **Fire**: Red (#E74C3C)
- **Nature**: Green (#27AE60)
- **Earth**: Brown (#8B7355)
- **Ice**: Light Blue (#5DADE2)
- **Electric**: Yellow (#F4D03F)
- **Beast**: Tan (#A0826D)
- **Shadow**: Purple (#5F4B8B)
- **Magic**: Violet (#9B59B6)
- **Demon**: Dark Purple (#7D3C98)
- **Spirit**: Sky Blue (#85C1E2)
- **Normal**: Gray (#A8A8A8)

## Team Building Tips

### 1. Coverage Goals
- Aim for **super effective coverage** against at least 8-10 types
- Prioritize coverage against common types (Water, Fire, Nature, Beast)
- Don't worry about covering every type - focus on threats

### 2. Defensive Balance
- **Avoid stacking weaknesses**: Multiple creatures with same weakness = 4× vulnerability
- **Seek resistances**: Having 2-3 types that resist common attacks is ideal
- **Immunities are powerful**: A single Electric immunity (via Earth type) can shut down Electric teams

### 3. Speed Tiers
- **Fast sweeper**: At least one creature with 80+ Speed
- **Slow tank**: At least one creature with high Defense/HP
- **Mixed speeds**: Balance across speed tiers for versatility

### 4. Type Diversity
- **5-8 types** is ideal for most teams
- Too few types = predictable and vulnerable
- Too many types = hard to find synergy

### 5. Role Balance
Consider having:
- **1-2 Physical attackers** (high Attack)
- **1-2 Tanks** (high HP/Defense)
- **1-2 Fast sweepers** (high Speed)
- **1-2 Utility creatures** (mixed stats)

### 6. Sample Team Compositions

#### Balanced Team
- Dragon (Fire/Magic): Special sweeper
- Dire Wolf (Beast/Shadow): Physical attacker
- Treant (Nature/Earth): Tank
- Naga (Water/Magic): Mixed attacker
- Ancient Wisp (Nature/Spirit): Support
- Thunder Lizard (Electric/Beast): Fast sweeper

**Coverage**: Excellent (9/12 types super effective)
**Weaknesses**: Fire (4×), Ice (2×)
**Strengths**: Great type diversity, good speed tiers

#### Offensive Rush Team
- Phoenix (Fire/Spirit): 95 Speed
- Thunder Lizard (Electric/Beast): 80 Speed
- Dire Wolf (Beast/Shadow): 85 Speed
- Drake (Fire/Beast): 80 Speed
- Ancient Wisp (Nature/Spirit): 90 Speed
- Naga (Water/Magic): 75 Speed

**Coverage**: Good offensive presence
**Weaknesses**: Low defense, vulnerable to slow tanks
**Strengths**: Outspeeds most opponents

#### Defensive Wall Team
- Rock Golem (Earth/Normal): 95 Defense
- Treant (Nature/Earth): 90 Defense
- Frost Elemental (Ice/Magic): 75 Defense
- Dragon (Fire/Magic): 85 Defense
- Murloc King (Water/Beast/Magic): 83 Defense
- Ghoul (Shadow/Beast): 60 Defense

**Coverage**: Moderate
**Weaknesses**: Low speed
**Strengths**: Can survive powerful hits

## Keyboard Shortcuts

- **Ctrl + S**: Save current team
- **Ctrl + T**: (In integrated version) Toggle team builder panel
- **Search bar**: Type to filter creatures instantly

## Local Storage

All data is saved in your browser's local storage:
- **Current team** is auto-saved on every change
- **Saved teams** persist across sessions
- **No server connection** required
- **Data is private** to your browser

### Clearing Data
To reset all data:
1. Open browser developer console (F12)
2. Run: `localStorage.clear()`
3. Refresh page

## Troubleshooting

### Team Won't Save
- Check if browser has local storage enabled
- Ensure you're not in private/incognito mode
- Try a different browser

### Import Fails
- Verify JSON format is correct
- Ensure all creature IDs are valid
- Check for syntax errors in JSON

### Creatures Not Showing
- Check search filter - clear it to see all creatures
- Scroll down in creature list
- Refresh page if list appears empty

### Stats Look Wrong
- Verify creature levels are set correctly
- Base stats are fixed per creature (cannot be changed)
- BST = HP + Attack + Defense + Speed

## Advanced Features

### Type Effectiveness Calculations

The tool uses multiplicative type effectiveness:
```javascript
// Example: Water/Beast defending against Fire
waterMultiplier = 0.5 (Fire vs Water)
beastMultiplier = 1.0 (Fire vs Beast, no relation)
totalMultiplier = 0.5 × 1.0 = 0.5 (Not very effective)

// Example: Nature/Earth defending against Water
natureMultiplier = 0.5 (Water vs Nature)
earthMultiplier = 2.0 (Water vs Earth)
totalMultiplier = 0.5 × 2.0 = 1.0 (Neutral!)
```

### Stacking Weaknesses
When multiple creatures share a weakness, the tool shows:
- Sum of multipliers (e.g., 4× = two creatures with 2× weakness)
- Pulsing animation to draw attention
- High priority for team improvement

### Coverage Optimization
The tool calculates:
- **Max multiplier**: Best effectiveness your team can achieve
- **Count**: How many creatures/moves can hit this type effectively
- Both are considered when color-coding coverage

## Integration with WowMon Game

To use teams in the actual WowMon game:
1. Export team as JSON
2. Open WowMon game
3. Use import feature (if available)
4. Or manually catch and train the creatures listed

Note: The team builder is a planning tool. Actual gameplay may require catching and training creatures first.

## Future Enhancements

Potential additions:
- Move set analysis
- Ability synergies
- Weather/terrain effects
- EV/IV calculations
- Battle simulator
- Team suggestions based on opponent
- Drag-and-drop reordering
- Team comparison tool

## Credits

Created as part of the localFirstTools project.
Based on the WowMon creature collection game.

## License

Part of localFirstTools - use freely for personal or educational purposes.
