# Replay Feature Testing Checklist

## How to Test the Session Replay Feature

### Setup
1. Open `apps/ai-tools/recursive-self-portrait.html` in a browser
2. You should see two tabs at the top: "Observe" and "Replay"

### Test 1: Record a Session
- [ ] Click "Begin Observation"
- [ ] Move mouse around the viewport
- [ ] Click a few times in different locations
- [ ] Observe the recursive layers following your movements
- [ ] Click "Stop Observation"
- [ ] Verify actions were recorded (check stats panel)

### Test 2: Save a Replay
- [ ] Switch to "Replay" tab
- [ ] Click "Save Current Session" button
- [ ] Enter a name (e.g., "Test Session 1")
- [ ] Click OK
- [ ] Verify replay appears in the "Saved Replays" list with:
  - Your custom name
  - Action count
  - Duration
  - Divergence %
  - Accuracy %

### Test 3: Load and Play a Replay
- [ ] Click on the saved replay in the list
- [ ] Verify timeline appears at bottom of screen
- [ ] Verify "Replay Mode" badge appears at top
- [ ] Click the "Play" (▶) button
- [ ] Watch the red ghost cursor follow recorded path
- [ ] Observe prediction layers updating
- [ ] See click ripple effects at click points
- [ ] Hear layered sound effects (if sound enabled)

### Test 4: Playback Controls
- [ ] Click "Pause" (⏸) during playback
- [ ] Verify playback stops
- [ ] Click "Play" again
- [ ] Verify playback resumes from pause point
- [ ] Click "Rewind" (⏮)
- [ ] Verify timeline resets to start

### Test 5: Timeline Scrubbing
- [ ] Load a replay
- [ ] Click at different points on the timeline bar
- [ ] Verify playhead jumps to clicked position
- [ ] Verify time display updates correctly
- [ ] Start playback from scrubbed position
- [ ] Verify replay continues from that point

### Test 6: Playback Speed
- [ ] Start a replay
- [ ] Click "0.5x" speed button
- [ ] Verify slow-motion playback
- [ ] Verify badge shows "(0.5x)"
- [ ] Click "2x" speed button
- [ ] Verify faster playback
- [ ] Click "4x" speed button
- [ ] Verify very fast playback
- [ ] Return to "1x"

### Test 7: Comparison Mode
- [ ] Load a replay
- [ ] Check "Comparison Mode" checkbox
- [ ] Start replay playback
- [ ] Move your mouse in the viewport
- [ ] Verify two cursors visible:
  - Red cursor with "REPLAY" label (playback)
  - Green cursor with "LIVE" label (your movements)
- [ ] Try to follow the replay cursor
- [ ] Observe differences between replay and live

### Test 8: Prediction Layers During Replay
- [ ] Load a replay
- [ ] Play the replay
- [ ] Watch the colored ghost cursors in each layer
- [ ] Observe layers turning:
  - Green (converged) when predictions match
  - Red (diverged) when predictions differ
- [ ] Notice how deeper layers diverge more

### Test 9: Multiple Replays
- [ ] Record another session (switch to Observe tab)
- [ ] Save with a different name
- [ ] Switch to Replay tab
- [ ] Verify both replays in list
- [ ] Load first replay
- [ ] Load second replay
- [ ] Verify correct replay loads each time

### Test 10: Export Replay
- [ ] Go to Observe tab
- [ ] Click "Export Session" button
- [ ] Save JSON file
- [ ] Note: This exports full session including replay data

### Test 11: Import Replay
- [ ] Switch to Replay tab
- [ ] Click "Import Replay" button
- [ ] Select a previously exported JSON file
- [ ] Verify replay appears in list
- [ ] Load and play imported replay

### Test 12: Persistence
- [ ] Record and save a replay
- [ ] Close the browser
- [ ] Reopen the page
- [ ] Switch to Replay tab
- [ ] Verify saved replays still present
- [ ] Load and play to confirm data intact

### Test 13: Tab Switching
- [ ] Switch between Observe and Replay tabs
- [ ] Verify:
  - Timeline shows/hides appropriately
  - Replay Mode badge shows/hides
  - Ghost cursors show/hide
  - No console errors
  - Smooth transitions

### Test 14: Edge Cases
- [ ] Try to play when no replay loaded
- [ ] Try to save when no session recorded
- [ ] Import invalid JSON file
- [ ] Scrub timeline while paused
- [ ] Change speed while paused
- [ ] Enable comparison mode while not playing

### Test 15: Visual Elements
- [ ] Verify timeline markers for clicks (orange bars)
- [ ] Verify progress bar animates smoothly
- [ ] Verify playhead moves with progress
- [ ] Verify time display format (M:SS / M:SS)
- [ ] Verify replay item highlighting when active

### Test 16: Mobile/Responsive
- [ ] Test on mobile device or narrow window
- [ ] Verify timeline is usable
- [ ] Verify tabs are clickable
- [ ] Verify replay list is scrollable
- [ ] Verify controls don't overlap

## Expected Behaviors

### When Recording
- Actions counter increases
- Predictions counter increases
- Divergence meter updates
- Behavioral fingerprint updates
- Layers follow cursor with delays

### When Playing Replay
- Red ghost cursor visible
- Layers show predictions
- Timeline progresses
- Time display updates
- Click effects appear
- Sounds play (if enabled)

### When in Comparison Mode
- Green cursor follows your mouse
- Red cursor follows replay
- Both visible simultaneously
- Can see divergence between them

## Common Issues to Check

### Replay Won't Play
- Ensure a replay is loaded (click one from list)
- Check if already playing (press pause first)
- Verify replay has actions data

### Timeline Not Showing
- Ensure you're on Replay tab
- Ensure a replay is loaded
- Try reloading the page

### Ghost Cursor Not Visible
- Ensure replay is actually playing
- Check if hidden behind layers
- Verify replay has movement data

### No Sound
- Click sound toggle (top right)
- Check browser sound permissions
- Verify not muted

### Comparison Mode Not Working
- Ensure checkbox is checked
- Ensure replay is playing
- Move mouse over viewport
- Check if green cursor appears

## Success Criteria

✅ All 16 test sections pass
✅ No console errors during operation
✅ Replays persist across page reloads
✅ Import/Export works correctly
✅ All UI elements visible and functional
✅ Performance is smooth (no lag/stuttering)
✅ Original observation features still work

---

**Note**: This is a single-file HTML application with no server required. All data is stored in localStorage.
