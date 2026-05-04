# Infinite Game Jam - Autonomous Evolution System Guide

## Overview

The Infinite Game Jam is a self-evolving platformer game that uses AI playtesting and genetic algorithms to automatically improve its fun factor. This document explains the enhanced autonomous evolution system.

## Evolution System Components

### 1. AI Playtester
- Runs 50 simulations per generation with varying skill levels (0.5-0.9)
- Each AI player has different reaction times and decision-making quality
- Simulates realistic player behavior including mistakes

### 2. Analytics Engine
Tracks comprehensive metrics:
- **Survival Rate**: How many AI players survive
- **Average Score**: Points collected
- **Average Distance**: How far players progress
- **Close Calls**: Near-misses with obstacles (excitement factor)
- **Idle Time**: Time spent not making inputs
- **Death Reasons**: Fall, obstacle hit, left edge, survived
- **Coin Collection**: Efficiency of collectible placement

### 3. Fun Score Formula
```
funScore = 50
  + (survivalRate - 0.3) * 50    // Target ~30% survival
  + min(closeCalls, 10) * 3       // Reward excitement
  - idleRatio * 30                 // Penalize boredom
  + min(distance/100, 20)          // Reward progress
  - issues.length * 10             // Penalize problems
```

### 4. Mutation Strategies

#### Conservative Mode
- Mutation Rate: 8%
- Mutation Strength: 10%
- Use for: Initial baseline establishment

#### Balanced Mode (Default)
- Mutation Rate: 15%
- Mutation Strength: 20%
- Use for: Standard evolution

#### Aggressive Mode
- Mutation Rate: 25%
- Mutation Strength: 35%
- Use for: Breaking out of local optima

#### Themed Mode
- Mutation Rate: 15%
- Mutation Strength: 25%
- Focuses mutations on specific parameter groups

### 5. Themed Evolution
Target specific aspects of gameplay:
- **better-jumps**: Jump force, gravity, air control
- **better-flow**: Scroll speed, platform gap, variance
- **more-exciting**: Obstacle chance/speed, moving platforms
- **more-rewarding**: Coin chance/value, powerups
- **smoother-difficulty**: Difficulty ramp, max difficulty
- **speedrun-mode**: Speed, jump, gravity tuning
- **hardcore-mode**: Obstacles, gaps, difficulty
- **casual-mode**: Platform width, jumps, coins

## Autonomous Evolution Features

### Strategy Orchestration
The auto-evolve system automatically switches between strategies:

1. **Baseline (Conservative, 10 gens)**: Establish starting metrics
2. **Exploration (Aggressive, 15 gens)**: Find parameter space
3. **Refinement (Balanced, 10 gens)**: Optimize discoveries
4. **Themed (5 gens)**: Focus on flow
5. **Second Exploration (Aggressive, 10 gens)**: Break plateaus
6. **Final Refinement (Balanced, 10 gens)**: Polish

### Adaptive Behavior

**Stagnation Detection**:
- If no improvement for 5 generations → switch to aggressive
- If no improvement for 8 generations → try random theme
- Prevents getting stuck in local optima

**Target Achievement**:
- Stops automatically at 80% fun score
- Saves "Target_Achieved" preset
- Exports complete evolution data

**Generation Limit**:
- Maximum 100 generations
- Prevents infinite loops

### Milestone Presets
Automatically saved every 10 generations:
- Generation_10
- Generation_20
- Generation_30
- etc.

## Console API

Access these functions via browser console:

```javascript
// Export all evolution data
exportEvolutionData()

// Create specialized game modes
createGameModes()

// Manually set evolution strategy
setEvolutionStrategy('aggressive')
setEvolutionStrategy('themed', 'better-jumps')

// Access evolution engine
window.evolutionEngine

// Access current DNA
window.gameDNA

// Access evolution history
window.evolutionHistory
```

## Game Modes

### Standard Mode
Evolved through autonomous optimization

### Hardcore Mode
- 1.5x obstacle chance
- 1.3x obstacle speed
- 1.2x platform gap
- 1.5x difficulty ramp
- 1.4x moving platform chance

### Casual Mode
- 1.3x platform width
- 0.8x platform gap
- 1.2x jump force
- 1.5x coin chance
- 0.6x obstacle chance
- 0.8x scroll speed

### Speedrun Mode
- 1.5x scroll speed
- 1.4x player speed
- 1.2x jump force
- 1.1x gravity
- 1.1x platform gap
- 2x coin value

## Running the Experiment

### Quick Start
1. Open infinite-game-jam.html in browser
2. Click "Auto-Evolve"
3. Watch the evolution progress
4. Export data when complete

### Manual Control
1. Click "Evolve Once" to run single generation
2. Adjust speed slider for visualization
3. "Play Yourself" to test current DNA
4. "Load Best DNA" to restore highest score

### Console-Driven Evolution
```javascript
// Run specific number of generations
for(let i = 0; i < 20; i++) {
  await evolveOnce();
}

// Export and analyze
exportEvolutionData();

// Create game modes from result
createGameModes();
```

## Understanding the Results

### Good Fun Score Indicators
- 60-70%: Decent game
- 70-80%: Good game
- 80%+: Excellent game

### Balance Metrics
- **Survival Rate**: 30-50% is ideal
- **Close Calls**: 3-8 per run is exciting
- **Idle Ratio**: <0.2 means good pacing

### Common Issues
- "Too hard": Survival < 10%
- "Too easy": Survival > 80%
- "Frustrating start": Avg distance < 500
- "Too slow": Idle ratio > 0.3
- "Not exciting": Close calls < 2

## Data Export Format

```json
{
  "timestamp": "ISO timestamp",
  "totalGenerations": 50,
  "bestGeneration": 23,
  "bestFunScore": 78.5,
  "bestDNA": {...},
  "currentDNA": {...},
  "evolutionHistory": [
    {
      "generation": 1,
      "funScore": 45,
      "dna": {...},
      "analysis": {...}
    }
  ],
  "fitnessHistory": [45, 48, 52, ...],
  "presets": [...]
}
```

## Tips for Autonomous Evolution

1. **Let it run**: Don't stop early, evolution needs time
2. **Monitor console**: Look for strategy changes and insights
3. **Watch the graph**: Fitness should trend upward
4. **Check milestones**: Generation_10, _20, etc. show progress
5. **Export regularly**: Data is valuable for analysis
6. **Create modes**: Always run createGameModes() at the end

## What Makes a Game Fun?

Based on the evolution algorithm:
- **Balanced difficulty**: Not too hard, not too easy
- **Exciting moments**: Close calls and narrow escapes
- **Constant engagement**: Minimize idle time
- **Sense of progress**: Distance and score should increase
- **Clear feedback**: Players should understand why they died
- **Risk/reward**: Collectibles should be challenging to get
- **Smooth pacing**: Difficulty should ramp gradually

## Known Limitations

1. Fun score is algorithmic, not human-validated
2. AI player skill is simulated, may not match real players
3. Some parameters interact in complex ways
4. Local optima can trap evolution
5. 100 generations may not be enough for perfect balance

## Future Enhancements

Potential improvements to explore:
- Human player data integration
- Multi-objective optimization (fun + difficulty + replayability)
- More sophisticated AI behaviors
- Dynamic difficulty adjustment
- Procedural level generation evolution
- Music/sound evolution
