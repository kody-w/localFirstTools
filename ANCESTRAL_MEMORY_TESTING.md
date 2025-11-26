# Ancestral Memory System - Testing Guide

## Quick Start
1. Open `apps/ai-tools/recursive-self-portrait.html` in a browser
2. Click "Start Observation"
3. Move your mouse around to generate behavioral data
4. Watch the "Ancestral Memory" panel in the sidebar

## What to Test

### Session 1: Establish Baseline
1. Start observation
2. Move mouse in **circular patterns** for 30 seconds
3. Check sidebar - you should see:
   - Generation: 1
   - Dominant Genes: "circular-motion" should appear
   - Genome Sequence: Should show DNA-like codes (ATG-GCC-TTA...)
   - Unlocked Memory: "Your ancestors drew circles in the sand..."

### Session 2: Test Heritability
1. Refresh the page
2. Start observation again
3. Move mouse in **circular patterns** again
4. Check sidebar:
   - Generation: 2
   - Heritability: Should increase (green bar grows)
   - Dominant Genes: "circular-motion" should be marked as DOMINANT

### Session 3: Test Mutations
1. Refresh the page
2. Start observation
3. Move mouse in **straight lines** (left to right, up to down)
4. Check sidebar:
   - Recent Mutations: Should show "straight-lines (emergence)"
   - Heritability: May decrease as behavior differs
   - Unlocked Memory: "They moved with purpose, direct and unwavering..."

### Test Primal Instincts

#### Fight Response
- Move cursor **very fast** (>250 speed) while staying near predicted areas
- Watch "Primal Instincts" section - **Fight** box should highlight

#### Flight Response
- Move cursor **very fast** (>200 speed) while avoiding predicted areas
- Watch "Primal Instincts" section - **Flight** box should highlight

#### Freeze Response
- Move cursor **very slowly** or stop moving
- Watch "Primal Instincts" section - **Freeze** box should highlight

#### Curiosity Response
- Move at **moderate speed** (50-150), exploring different areas
- Watch "Primal Instincts" section - **Explore** box should highlight

### Test Pattern Detection

#### Circular Motion
- Draw circles with your cursor
- Should unlock: "Your ancestors drew circles in the sand..."

#### Hesitation
- Move, pause, move, pause repeatedly
- Should unlock: "They paused before the hunt, measuring risk..."

#### Rapid-Fire Clicks
- Click rapidly multiple times (< 300ms between clicks)
- Should unlock: "In moments of danger, they moved without thought..."

#### Territorial Behavior
- Keep cursor in center of screen (middle 50%)
- Should unlock: "They claimed this space, marking boundaries..."

#### Migratory Behavior
- Move cursor all over the screen, covering all areas
- Should unlock: "They were nomads, never settling in one place..."

### Test Export
1. After generating some behavioral data
2. Click **"Export Behavioral Genome"** button
3. A JSON file should download
4. Open the file - it should contain:
   - Generation number
   - Genome sequence (DNA codes)
   - Dominant/recessive genes
   - Family tree data
   - Primal instinct profile
   - Unlocked memories

## Expected Behaviors

### UI Updates
- **Generation Number**: Increments with each session
- **Heritability Meter**: Green bar shows 0-100%
- **Dominant Genes**: Green rounded tags
- **Mutations**: Red pulsing tags
- **Primal Instincts**: Active instinct gets highlighted border
- **Genome Sequence**: Updates as new genes are detected
- **Unlocked Memories**: Purple badges appear with poetic text

### Console Logs
Open browser console (F12) and look for:
- "Generation X begins..."
- "Mutation detected: [gene] emerging"
- "Ancestral memory unlocked: [memory text]"

### localStorage
Check browser devtools → Application → localStorage:
- Key: `recursive-self-portrait-ancestral`
- Should contain JSON with genes, stability, generations, etc.

## Troubleshooting

### Panel Not Showing
- Check browser console for errors
- Verify you clicked "Start Observation"
- Scroll down in sidebar to find "Ancestral Memory" panel

### No Genes Detected
- Make sure you've moved mouse for at least 20 actions
- Try more pronounced patterns (bigger circles, longer lines)
- Wait at least 30 seconds of movement

### Heritability Always 0%
- This is normal for first session (no ancestral data yet)
- Refresh and start another session with similar behavior

### No Mutations
- Mutations only check every 30 seconds
- Try completely different movement patterns
- Wait longer in the session

### Export Button Not Working
- Check browser console for errors
- Verify you have some behavioral data
- Try a different browser if download fails

## Expected File Growth
- Original file: ~15,784 lines, ~642KB
- With Ancestral Memory: ~19,074 lines, ~716KB
- Added: ~3,290 lines, ~74KB

## Performance
Should have minimal performance impact:
- Gene extraction: Only when 20+ actions exist
- Mutation detection: Throttled to every 30 seconds
- Commentary: Throttled to every 20 seconds
- UI updates: Once per frame (integrated with existing loop)

## Browser Compatibility
Tested with:
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

Requires:
- localStorage support
- ES6 support (Map, arrow functions)
- Modern CSS (flexbox, grid)

## Success Criteria
After 3 sessions of varied movement:
- [x] Generation number is 3
- [x] At least 5 genes detected
- [x] At least 2 dominant genes
- [x] At least 1 mutation recorded
- [x] Heritability shows a percentage > 0
- [x] At least 2 memories unlocked
- [x] All 4 primal instincts triggered at some point
- [x] Genome sequence is visible
- [x] Export produces valid JSON

## Advanced Testing

### Long-Term Evolution (10+ Sessions)
1. Run 10 sessions with consistent behavior
2. Check if genes reach max stability (100%)
3. Verify family tree grows
4. Test if extinct traits are tracked

### Behavioral Diversity
1. Session 1: Circles only
2. Session 2: Lines only
3. Session 3: Random chaos
4. Session 4: Slow deliberate movements
5. Session 5: Fast erratic movements
6. Verify that mutations and heritability reflect this

### Data Persistence
1. Generate significant ancestral data
2. Close browser completely
3. Reopen and start observation
4. Verify all ancestral data loads correctly

### Export/Import Cycle
1. Export genome
2. Clear localStorage
3. Manually construct import (future feature)
4. Verify data restoration

## Visual Indicators to Watch

### Gene Tags
- **Green tags with bold**: Dominant genes (>70% stability)
- **Orange tags with italic**: Recessive genes (<30% stability)
- **Red pulsing tags**: Recent mutations

### Heritability Bar
- **Purple → Blue → Green gradient**: Visual appeal
- **0%**: No similarity to ancestors
- **50%**: Moderate similarity
- **100%**: Identical to ancestral average

### Primal Instinct Grid
- **Normal**: Dark background
- **Active**: Gold background with glowing border

### Genome Sequence
- **Format**: Triplet codes separated by hyphens
- **Example**: ATG-GCC-TTA-CAG-GGT
- **Scrollable**: For long genomes

## Known Behaviors

### First Session
- Generation: 1
- Heritability: Will be 0% or undefined (no ancestors yet)
- Family Tree: Empty
- This is expected!

### Second Session
- Heritability calculation activates
- Genetic comparison begins
- Mutations can be detected

### Tenth+ Session
- Rich family tree
- Clear dominant genes
- Stable heritability
- Extinct traits may appear
- Complex genome sequence

## Commentary System
Every ~20 seconds during observation, you may see/hear:
- Log entry with ancestral commentary
- Voice synthesis (if enabled)
- Contextual messages about genes, mutations, heritability

Example messages:
- "Your ancestors moved this way..."
- "The genetic line is strong in you..."
- "Mutation rate increasing..."
- "Fight or flight? Your ancestors chose..."

## Data Export Format
```json
{
  "version": "1.0",
  "generationNumber": 3,
  "genome": "ATG-GCC-TTA-CAG-GGT",
  "genes": ["circular-motion", "fast-mover", "territorial"],
  "dominantGenes": ["circular-motion"],
  "recessiveGenes": ["hesitation"],
  "familyTree": {
    "totalGenerations": 3,
    "recentGenerations": [...]
  },
  "ancestralTraits": {
    "heritability": "67.5%",
    "mutationRate": "15.2%",
    "adaptationScore": "82.3"
  },
  "primalInstinctProfile": {
    "fight": 5,
    "flight": 2,
    "freeze": 8,
    "curiosity": 12
  },
  "unlockedMemories": [...],
  "exportedAt": "2025-11-26T..."
}
```

## Report Issues
If you encounter problems:
1. Check browser console (F12)
2. Verify localStorage is enabled
3. Note your browser version
4. Describe the behavioral pattern you were trying
5. Check if genes/mutations/memories are being detected at all
