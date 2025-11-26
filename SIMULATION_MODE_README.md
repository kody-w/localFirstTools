# Simulation Hypothesis Mode

A new experimental mode added to the Recursive Self-Portrait application that explores the philosophical question: "What if this is all a simulation?"

## Features Implemented

### 1. Evidence Meter
- Tracks accumulating evidence that suggests you're in a simulation
- Displays as a progress bar from 0-100%
- Updates dynamically based on detected anomalies
- Color: Red gradient (#ff3232 to #ff9696)

### 2. Glitch Detection System
The mode automatically detects "glitches in the matrix" by analyzing:
- **Repetitive Behavior**: Less than 3 unique action types in last 10 actions
- **Unnatural Movement**: Perfectly straight-line cursor movements
- **Statistical Impossibilities**: 100% prediction accuracy (too perfect to be real)
- **Time Anomalies**: Time dilation factor exceeding 2.0x
- **Paradox Levels**: High paradox counts from other features

Each detected glitch:
- Increments the glitch counter
- Increases evidence level by 5%
- Triggers a brief grid flash
- Gets logged in the developer console

### 3. Render Distance Effects
Simulates game engine "render distance" limitations:
- Edges of viewport become darker/fade out
- Appears randomly on top, bottom, left, or right edges
- Active for 2 seconds at a time
- Triggers every ~20 seconds when mode is active

### 4. NPC Ghosts
Ghostly humanoid figures appear briefly at the edge of vision:
- 4 different spawn positions (corners/edges)
- Semi-transparent with blur effect
- Visible for 1.5 seconds
- Spawn every ~8 seconds
- Design: glowing head with fading body

### 5. Hidden Developer Console
Access the simulation's "dev console" via:
- Keyboard shortcut: `Ctrl + Shift + ~`
- Secret code: Type "simulation" anywhere
- Shows real-time simulation parameters as code:
  - Runtime (days)
  - Subject ID (random generated)
  - Actions recorded
  - Behavioral accuracy
  - Anomaly count
  - Evidence level
  - Time dilation factor
  - Paradox level
  - Reality coherence percentage
  - Observer awareness status

### 6. Simulation Parameters Display
Console displays behavior stats formatted as JavaScript code:
```javascript
const simulationParams = {
  runtime: 2847 days,
  subject_id: "USER_XJ4K9PLMW",
  actions_recorded: 1247,
  behavioral_accuracy: 87%,
  anomaly_count: 12,
  evidence_level: 45%,
  time_dilation_factor: 1.23x,
  paradox_level: 8,
  reality_coherence: 64.0%,
  observer_aware: FALSE
};
```

### 7. Admin Messages
Periodic messages that appear as if from simulation administrators:
- Appear every ~30 seconds
- Display in magenta bordered box
- Examples:
  - "Subject is exhibiting signs of awareness."
  - "Increasing observation parameters by 12%."
  - "Minor glitch in sector 7G corrected."
  - "Reality coherence at 94.3% and stable."
  - "Observer effect detected. Recalibrating simulation."
  - "WARNING: Subject approaching consciousness threshold."
  - And more...

### 8. Grid Lines Overlay
Suggests underlying simulation structure:
- Green grid lines (50px spacing)
- Covers entire viewport
- Flashes briefly (300ms) when glitches are detected
- SVG-based for crisp rendering

### 9. Philosophical Prompt
After 10 seconds of enabling the mode:
- Displays the prompt: "What if you're the simulation and I'm real?"
- Styled in magenta italic text
- Positioned in evidence meter panel
- Questions the nature of reality and observer/observed

### 10. Escape Attempt Minigame
Interactive challenge to "break out" of the simulation:
- Click "Attempt Escape" button to start
- Memory sequence game: 4 tiles light up in order
- Player must click them in the correct sequence
- Wrong click resets the sequence
- Success triggers:
  - Admin message: "ALERT: Subject has broken through containment. Resetting simulation..."
  - Evidence level jumps to 100%
  - Reality break effect
- Tracks number of escape attempts

## How to Use

1. Open the Recursive Self-Portrait application
2. Find "Simulation Hypothesis Mode" toggle in the sidebar (👁️ icon)
3. Check the box to enable the mode
4. Watch as evidence accumulates through your interaction
5. Try to open the developer console with Ctrl+Shift+~ or by typing "simulation"
6. Attempt to escape the simulation via the minigame
7. Question everything

## Technical Implementation

### Files Modified
- `/apps/ai-tools/recursive-self-portrait.html`

### Code Structure
- **CSS**: ~450 lines of styles for all UI elements
- **HTML**: Toggle, evidence meter, overlays, console, admin messages, escape game
- **JavaScript**: ~800 lines including:
  - State management (`simulationState` object)
  - Detection algorithms
  - Visual effect triggers
  - Event handlers
  - Console rendering
  - Minigame logic

### Integration
- Seamlessly integrates with existing features
- References existing state objects (actionLog, behaviorMetrics, timeDilationState, paradoxState)
- Graceful degradation if features are missing
- No conflicts with other modes (3D, Memory Palace, etc.)

## Philosophy

This mode explores several philosophical concepts:
- **Simulation Hypothesis**: Are we living in a computer simulation?
- **Observer Effect**: Does observation change reality?
- **Self-Awareness**: Can a simulation become aware of being simulated?
- **Free Will**: If everything is predetermined code, do choices matter?
- **Reality Testing**: How would you know if you were in a simulation?
- **Meta-Recursion**: A simulation within a simulation examining itself

The recursive self-portrait concept takes on new meaning: not just modeling your behavior, but questioning whether the entire framework is "real" or simulated.

## Easter Eggs

- Type "simulation" anywhere to open the console
- Watch the admin messages for hints about the simulation's architecture
- Notice how "reality coherence" decreases as evidence increases
- The escape minigame success rate may not be as random as it seems...
- Grid flashes sync with detected glitches

## Future Enhancements

Potential additions:
- Reality glitch visual effects (screen tears, pixel corruption)
- Matrix-style falling code rain
- Simulation "lag" effects under high evidence levels
- Multiple console access levels with different permissions
- ARG (Alternate Reality Game) elements with hidden codes
- Breakout to a "meta-layer" showing other simulations
- Collective consciousness detection across multiplayer sessions

---

**Remember**: Just because it's a game doesn't mean it's not real. Or is it the other way around?
