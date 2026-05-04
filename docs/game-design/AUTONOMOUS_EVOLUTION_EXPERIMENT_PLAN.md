# Infinite Game Jam - 24-Hour Autonomous Evolution Experiment Plan

## Experiment Design

### Objective
Autonomously evolve the Infinite Game Jam platformer to achieve 80%+ fun score through intelligent mutation strategies and adaptive optimization.

### Methodology
The experiment uses a sophisticated multi-phase evolution strategy with automatic adaptation based on progress detection.

## Execution Instructions

### Setup Phase
1. Open `/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/infinite-game-jam.html` in Chrome/Firefox
2. Open browser console (F12)
3. Click "Auto-Evolve" button to start autonomous evolution
4. Set speed slider to ~75 for faster evolution
5. Monitor console output for strategy changes and milestones

### Monitoring
The system will automatically:
- Log each generation's results to console
- Switch strategies based on progress
- Save milestone presets every 10 generations
- Detect stagnation and adapt
- Stop at 80% fun score or 100 generations
- Export complete evolution data as JSON

### Expected Timeline
- **Generations 1-10** (Conservative): ~15-20 minutes
- **Generations 11-25** (Aggressive): ~20-25 minutes
- **Generations 26-35** (Balanced): ~15 minutes
- **Generations 36-40** (Themed): ~7 minutes
- **Generations 41-50** (Aggressive): ~15 minutes
- **Generations 51-60** (Balanced): ~15 minutes
- **Total**: ~90-120 minutes for 60 generations

## Evolution Strategy Phases

### Phase 1: Baseline Establishment (Gen 1-10)
**Strategy**: Conservative
**Parameters**:
- Mutation Rate: 8%
- Mutation Strength: 10%

**Goals**:
- Establish baseline fun score
- Understand starting parameter space
- Identify major issues

**Expected Outcomes**:
- Small, incremental improvements
- Fun score: 30-50%
- Clear identification of difficulty issues

### Phase 2: Aggressive Exploration (Gen 11-25)
**Strategy**: Aggressive
**Parameters**:
- Mutation Rate: 25%
- Mutation Strength: 35%

**Goals**:
- Explore wide parameter space
- Try dramatic changes
- Find new local optima

**Expected Outcomes**:
- Large variance in fun scores
- Discovery of better parameter combinations
- Fun score: 40-65%
- Some generations may regress

### Phase 3: Refinement (Gen 26-35)
**Strategy**: Balanced
**Parameters**:
- Mutation Rate: 15%
- Mutation Strength: 20%

**Goals**:
- Refine discoveries from exploration
- Stabilize improvements
- Eliminate worst issues

**Expected Outcomes**:
- Steady improvement
- Fun score: 55-70%
- More balanced gameplay

### Phase 4: Themed Optimization (Gen 36-40)
**Strategy**: Themed (better-flow)
**Parameters**:
- Mutation Rate: 15%
- Mutation Strength: 25%
- Focus: scroll speed, platform gap, variance

**Goals**:
- Improve game flow and pacing
- Target specific gameplay feel
- Reduce idle time

**Expected Outcomes**:
- Better player engagement
- Smoother difficulty curve
- Fun score: 60-75%

### Phase 5: Second Exploration (Gen 41-50)
**Strategy**: Aggressive
**Parameters**:
- Mutation Rate: 25%
- Mutation Strength: 35%

**Goals**:
- Break out of any plateaus
- Find final optimizations
- Push toward 80% target

**Expected Outcomes**:
- Potential breakthrough improvements
- Fun score: 65-78%

### Phase 6: Final Refinement (Gen 51-60)
**Strategy**: Balanced
**Parameters**:
- Mutation Rate: 15%
- Mutation Strength: 20%

**Goals**:
- Polish final configuration
- Achieve 80%+ fun score
- Create stable, fun game

**Expected Outcomes**:
- Final optimization
- Fun score: 75-85%
- Achievement of target

## Adaptive Behaviors

### Stagnation Detection
If no improvement for 5+ generations:
- Auto-switch to aggressive exploration
- Try random themed evolution
- Increase mutation strength temporarily

### Success Triggers
- 80% fun score → Save "Target_Achieved" preset
- Automatic game mode generation
- Complete data export

## Data Collection

### Real-Time Metrics
Console logs track:
- Generation number
- Current strategy
- Fun score
- Survival rate
- Average distance
- Issues detected
- Mutations applied

### Milestone Snapshots
Every 10 generations, saves:
- Complete DNA parameters
- Analysis results
- Timestamp
- Generation number

### Final Export
JSON file containing:
- Full evolution history
- All milestone presets
- Best DNA configuration
- Fitness graph data
- Complete analytics

## Post-Experiment Analysis

### Step 1: Extract Data
```javascript
// In browser console after evolution completes
exportEvolutionData()
```
This downloads: `evolution-data-genN.json`

### Step 2: Create Game Modes
```javascript
createGameModes()
```
Generates:
- Hardcore Mode
- Casual Mode
- Speedrun Mode

### Step 3: Document Findings
Analyze exported JSON for:
- Which parameters changed most
- What correlates with fun score
- Surprising discoveries
- Optimal parameter ranges

### Step 4: Update Evolution Log
Transfer insights to:
`/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/docs/game-design/INFINITE_GAME_JAM_EVOLUTION_LOG.md`

## Expected Discoveries

### Critical Parameters
Based on the fun score formula, expect to find:
1. **Platform Gap** - Most important for survival rate
2. **Jump Force** - Affects player agency
3. **Obstacle Chance** - Primary difficulty tuner
4. **Scroll Speed** - Controls pacing
5. **Difficulty Ramp** - Affects late game

### Parameter Interactions
Likely to discover:
- Jump force vs gravity ratio for "jump feel"
- Platform gap vs jump force for reachability
- Obstacle chance vs obstacle speed for difficulty
- Scroll speed vs player speed for control feel
- Coin placement vs platform design

### Optimal Ranges
Predictions for evolved parameters:
- **platformGap**: 120-140 (from 150)
- **jumpForce**: 13-15 (from 12)
- **gravity**: 0.45-0.55 (from 0.5)
- **obstacleChance**: 0.2-0.28 (from 0.3)
- **scrollSpeed**: 3.5-4.5 (from 3)
- **coinChance**: 0.6-0.7 (from 0.5)

## Success Criteria

### Minimum Success
- ✓ 60%+ fun score achieved
- ✓ All phases completed
- ✓ Data exported
- ✓ Insights documented

### Target Success
- ✓ 80%+ fun score achieved
- ✓ 10+ documented insights
- ✓ 3 game modes created
- ✓ Pattern analysis complete

### Exceptional Success
- ✓ 85%+ fun score achieved
- ✓ Novel discoveries about game design
- ✓ Improved evolution algorithm based on findings
- ✓ Publishable insights

## Failure Modes & Recovery

### Stuck in Local Optimum
**Symptom**: No improvement for 10+ generations
**Recovery**: Aggressive + themed evolution

### Fun Score Regression
**Symptom**: Score decreasing over time
**Recovery**: Load best DNA, continue from there

### Browser Crash
**Symptom**: Page closes unexpectedly
**Recovery**: Presets saved in localStorage, reload page

### Time Limit Hit
**Symptom**: 100 generations reached
**Recovery**: Review best DNA, consider manual tuning

## Manual Intervention Points

### When to Stop Early
- Fun score > 80% (target achieved)
- Clear pattern emerges requiring algorithm change
- Infinite loop detected

### When to Restart
- Early generations show fundamental flaws
- Parameters drift to extreme values
- Fun score stuck below 30% for 20+ generations

### When to Adjust
- Evolution too slow: increase speed slider
- Missing visualization: decrease speed slider
- Stagnation: manually switch to aggressive

## Human Testing Phase

After autonomous evolution:
1. Test "Play Yourself" mode
2. Evaluate subjective fun
3. Compare human experience to AI metrics
4. Identify gaps in fun score formula
5. Document human vs AI differences

## Deliverables

1. **Evolution Data JSON** - Complete history
2. **Updated Evolution Log** - Insights and patterns
3. **Game Mode Presets** - Hardcore, Casual, Speedrun
4. **Analysis Report** - What makes this game fun
5. **Evolved Game HTML** - Committed to repo
6. **Recommendations** - For future evolution experiments

## Next Steps After Experiment

1. Validate findings with human players
2. Improve fun score formula based on discoveries
3. Add more sophisticated AI behaviors
4. Implement discovered patterns as recommendations
5. Create tutorial mode based on optimal parameters
6. Consider multi-objective optimization (fun + replayability + difficulty)
