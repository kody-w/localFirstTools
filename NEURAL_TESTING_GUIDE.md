# Neural Network Testing Guide

## Quick Start Testing

### 1. Open the Application
```bash
# From the localFirstTools directory
open apps/ai-tools/recursive-self-portrait.html
```

Or use a local server:
```bash
python3 -m http.server 8000
# Navigate to: http://localhost:8000/apps/ai-tools/recursive-self-portrait.html
```

### 2. Initial Setup
1. Click "Begin Observation" button
2. Move your cursor around the viewport
3. After 11+ movements, the neural network can begin training

### 3. Enable Neural Prediction
1. Check the "Use Neural Prediction" checkbox
2. Watch the "Neural Confidence" meter start at 0%
3. Continue moving your cursor
4. Observe the confidence increase as the network trains

### 4. Compare Prediction Modes

#### Test A: Smooth Linear Motion
- **Goal**: See how well neural network learns simple patterns
- **Action**: Move cursor in straight lines
- **Expected**: Neural confidence should reach 70%+ quickly (within 100 moves)
- **Observation**: Prediction trails should closely follow actual cursor

#### Test B: Circular Motion
- **Goal**: Test pattern recognition on curves
- **Action**: Move cursor in circles
- **Expected**: Neural adapts within 50-100 moves, confidence 60-80%
- **Observation**: Ghost cursors should predict circular trajectory

#### Test C: Erratic Movement
- **Goal**: Compare neural vs heuristic on unpredictable behavior
- **Action**: Move cursor randomly and chaotically
- **Expected**: Neural confidence stays lower (30-50%)
- **Observation**: Heuristic may perform better (toggle to compare)

#### Test D: Pattern Switch
- **Goal**: Test adaptation to behavioral changes
- **Action**:
  1. Move in circles (let neural train to 70%+)
  2. Suddenly switch to straight lines
- **Expected**: Confidence may drop temporarily, then recover
- **Observation**: See "Adjusting prediction model" in log

### 5. Visual Indicators to Check

#### Stats Panel
- [ ] "Neural Confidence" shows percentage (0-100%)
- [ ] "Prediction Mode" shows "Neural" when checkbox is checked
- [ ] "Prediction Mode" shows "Heuristic" when checkbox is unchecked
- [ ] Confidence updates in real-time as you move

#### Neural Network Visualization Canvas
- [ ] Canvas appears between fingerprint and behavior log
- [ ] Shows network architecture: Input → Hidden → Hidden → Hidden → Output
- [ ] Neurons light up as you move cursor
- [ ] Brighter neurons = higher activation
- [ ] Purple output neurons when in neural mode
- [ ] Connection lines visible between layers

#### Behavior Log
- [ ] Log entry when neural network initializes
- [ ] Log entries when switching prediction modes
- [ ] Existing log entries still work (movement style, predictions, etc.)

### 6. Performance Testing

#### Frame Rate Test
1. Open browser dev tools (F12)
2. Go to Performance tab
3. Start recording
4. Move cursor rapidly while in neural mode
5. Stop recording
6. Check frame rate stays near 60 FPS

**Expected**: Should maintain 55-60 FPS even with neural training active

#### Training Speed Test
1. Enable neural prediction
2. Note time when confidence is 0%
3. Move cursor in consistent pattern
4. Time until confidence reaches 70%

**Expected**: ~100-200 cursor movements (10-30 seconds of active movement)

### 7. Edge Cases to Test

#### Minimal Movement
- [ ] Enable neural mode
- [ ] Move very slowly (lazy movement style)
- [ ] Neural should still train (confidence increases slowly)

#### Rapid Toggle
- [ ] Toggle neural mode on/off rapidly
- [ ] Should not crash or freeze
- [ ] Mode indicator updates correctly

#### High Recursion Depth
- [ ] Set depth slider to 12 (maximum)
- [ ] Enable neural mode
- [ ] Both prediction methods should work at all depths

#### Long Session
- [ ] Run for 500+ actions
- [ ] Neural confidence should stabilize
- [ ] Performance should remain consistent

### 8. Integration Testing

#### Works With Existing Features
- [ ] Webcam integration still works
- [ ] Sound effects still work
- [ ] Heat map still works
- [ ] Glitch effects still work
- [ ] Meta-commentary still appears
- [ ] Export/import still works
- [ ] Behavioral fingerprint still updates

### 9. Browser Compatibility

Test in each browser:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

Expected: All features work in all modern browsers

### 10. Debugging Tips

If neural network isn't working:

1. **Check console for errors**
   - Open dev tools (F12) → Console tab
   - Look for JavaScript errors

2. **Verify initialization**
   - Check behavior log for "Neural network initialized: 40→20→15→10→2"
   - If missing, neural toggle may not be triggering init

3. **Check data collection**
   - Move cursor at least 11 times before expecting training
   - Verify "Actions Recorded" counter in stats panel

4. **Canvas not showing**
   - Scroll sidebar if neural canvas is off-screen
   - Check if canvas element exists in dev tools → Elements tab

5. **Confidence not increasing**
   - Ensure neural toggle is checked
   - Move cursor more (need consistent movement pattern)
   - Check if training function is being called (console.log)

### 11. Expected Console Logs

When working correctly, you should see (open dev tools):

```
// No errors
// Optional: Can add console.logs to verify:
// - trainNeuralNetwork called every 3 mousemoves
// - visualizeNeuralNetwork called every 20 mousemoves
// - Neural confidence value updating
```

### 12. Screenshot Checklist

Take screenshots of:
- [ ] Stats panel showing neural confidence at 0%
- [ ] Stats panel showing neural confidence at 70%+
- [ ] Neural network visualization with neurons lit up
- [ ] Prediction trails in neural mode
- [ ] Prediction trails in heuristic mode (for comparison)
- [ ] Behavior log entries about neural network

### 13. Known Limitations

- Network trains incrementally (no batch training)
- Only output layer weights update (for performance)
- Maximum 60 FPS during training
- Confidence based on MSE (may not reflect true accuracy)
- No weight persistence (resets on page reload)

### 14. Success Criteria

The implementation is successful if:
- ✓ Neural toggle switches between modes
- ✓ Confidence meter updates in real-time
- ✓ Network visualization shows active neurons
- ✓ Predictions work in both modes
- ✓ Performance stays at ~60 FPS
- ✓ All existing features still work
- ✓ No JavaScript errors in console

## Quick Test Script

Copy and paste into browser console for automated test:

```javascript
// Automated neural network test
(async function testNeural() {
    console.log('Starting neural network test...');

    // Start observation
    document.getElementById('startBtn').click();
    await new Promise(r => setTimeout(r, 100));

    // Simulate cursor movements
    const viewport = document.getElementById('viewport');
    const rect = viewport.getBoundingClientRect();

    for (let i = 0; i < 50; i++) {
        const x = rect.left + rect.width/2 + Math.cos(i/5) * 100;
        const y = rect.top + rect.height/2 + Math.sin(i/5) * 100;

        const event = new MouseEvent('mousemove', {
            clientX: x,
            clientY: y,
            bubbles: true
        });
        viewport.dispatchEvent(event);

        await new Promise(r => setTimeout(r, 50));
    }

    // Enable neural mode
    document.getElementById('neuralToggle').checked = true;
    document.getElementById('neuralToggle').dispatchEvent(new Event('change'));

    console.log('Test complete. Check:');
    console.log('- Neural Confidence should be > 0%');
    console.log('- Prediction Mode should show "Neural"');
    console.log('- Canvas should show network visualization');
})();
```

## Reporting Issues

If you find bugs or issues, report:
1. Browser and version
2. Steps to reproduce
3. Console errors (if any)
4. Screenshot of the issue
5. Expected vs actual behavior

---

**Happy testing!** The neural network should demonstrate real-time learning of your cursor movement patterns while maintaining smooth 60 FPS performance.
