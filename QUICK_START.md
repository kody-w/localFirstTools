# Neural Network Quick Start Guide

## How to Use the Neural Prediction Feature

### 1. Open the App
```bash
open apps/ai-tools/recursive-self-portrait.html
```
or visit: http://localhost:8000/apps/ai-tools/recursive-self-portrait.html

### 2. Start Observation
Click **"Begin Observation"** button

### 3. Move Your Cursor
Move your cursor around for at least 10-15 movements to collect training data

### 4. Enable Neural Mode
Check the **"Use Neural Prediction"** checkbox

### 5. Watch It Learn!
- **Neural Confidence** meter will start at 0% and increase as you move
- Network visualization will show neurons activating
- After ~100-200 movements, confidence should reach 60-80%

---

## Quick Test Pattern

Move your cursor in a circle:
1. Start at the center
2. Move clockwise in a circle
3. Complete 2-3 full circles
4. Watch the neural confidence rise to 70%+
5. The ghost cursors should start predicting your circular motion!

---

## Toggle Comparison

Try this to compare neural vs heuristic:

1. Move in circles with neural mode **ON**
2. Note the prediction accuracy
3. Toggle neural mode **OFF**
4. Keep moving in circles
5. Compare which method predicts better!

---

## What to Look For

### Good Signs
- ✓ Neural confidence increasing (0% → 70%+)
- ✓ Prediction trails following your cursor
- ✓ Network visualization neurons lighting up
- ✓ Smooth 60 FPS performance

### If Something's Wrong
- Neural confidence stuck at 0%? → Make sure you moved at least 11 times
- Checkbox not working? → Check browser console for errors
- Canvas blank? → Scroll down in sidebar to see it
- Lagging? → Try reducing recursion depth

---

## Key Features

| Feature | Location | What It Shows |
|---------|----------|---------------|
| Neural Confidence | Stats Panel | 0-100% training quality |
| Prediction Mode | Stats Panel | "Neural" or "Heuristic" |
| Neural Toggle | Below Depth Slider | On/Off checkbox |
| Network Viz | Below Fingerprint | Live network activations |
| Prediction Trails | Main Viewport | Colored prediction paths |

---

## Pro Tips

1. **Smooth movements** → Higher confidence (70-90%)
2. **Erratic movements** → Lower confidence (30-50%)
3. **Patterns** → Neural learns them quickly
4. **Random motion** → Heuristic may work better
5. **Toggle during movement** → See real-time comparison

---

## Keyboard Shortcuts

- **Space** - Start/Stop observation
- **R** - Reset session
- **W** - Toggle webcam
- **(Tab to checkbox)** - Toggle neural mode

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Confidence not increasing | Move cursor more (need 11+ actions) |
| Can't find neural toggle | Scroll down sidebar, it's below depth slider |
| Canvas shows "Awaiting data" | Move cursor with observation started |
| Performance issues | Lower recursion depth to 3-5 |
| Toggle not working | Refresh page, try again |

---

## Performance Tips

For best performance:
- Keep recursion depth at 5-7
- Don't enable webcam and neural simultaneously (can, but more CPU)
- Close other browser tabs
- Use Chrome or Firefox for best performance

---

## Understanding the Visualization

### Network Canvas
- **Bright neurons** = High activity
- **Dim neurons** = Low activity
- **Purple neurons** = Output (when neural mode active)
- **Lines** = Connections between layers

### Confidence Meter
- **<30%** = Still learning
- **30-70%** = Getting better
- **70%+** = Good predictions
- **90%+** = Excellent (on regular patterns)

---

## What's Next?

Try these experiments:
1. Move in different shapes (circles, squares, zigzags)
2. Change speed (slow vs fast)
3. Mix patterns (circle then straight line)
4. Compare neural vs heuristic on each
5. See which patterns neural learns fastest

---

## Documentation

For more details:
- **IMPLEMENTATION_SUMMARY.md** - Feature overview
- **NEURAL_NETWORK_IMPLEMENTATION.md** - Technical details
- **NEURAL_TESTING_GUIDE.md** - Comprehensive testing

---

**Enjoy exploring how AI learns your movement patterns in real-time!**
