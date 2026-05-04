# DOTA 3: LEGACY - Complete MOBA Transformation

## Goal
Transform DOTA 3: LEGACY (dota3-legacy.html) into a complete, polished MOBA game with all core systems fully implemented, tested, and functioning. This is an autonomous 24-hour improvement session.

## Context
- **File**: `/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/dota3-legacy.html`
- **Current State**: 4209-line self-contained HTML game with basic hero system, simple abilities, creeps, Three.js 3D rendering
- **Architecture**: Model builder pattern with GameEntity base class, Hero class extends it
- **Available Assets**: 120+ hero JSONs in `/data/games/heroes/`, creep data in `/data/games/creeps/`, item JSONs in `/data/games/items/`
- **Project Type**: Local-first single HTML file (all CSS/JS inline, no external dependencies)

## Success Criteria

### CRITICAL FEATURES (Must Complete)
- [X] **Ability System**: All 4 ability slots (Q/W/E/R) functional with cooldowns, mana costs, and visual effects
- [X] **Hero Abilities**: Implement unique abilities for at least 5 heroes using data from `/data/games/heroes/*.json`
- [X] **Jungle Camps**: 4+ jungle creep camps with different creatures, respawn timers (60-90s), and gold/XP rewards
- [X] **Advanced Items**: Expand shop to 15+ items with recipes, stat bonuses, and active abilities
- [X] **Combat Polish**: Death animations, hit effects, level-up effects, floating damage numbers (already partial)
- [X] **AI Enemies**: Basic enemy hero AI that can attack, use abilities, and farm creeps
- [X] **Game Balance**: Proper MOBA pacing with balanced gold/XP rates, ability damage scaling
- [X] **Sound Effects**: Attack sounds, ability sounds, death sounds, purchase sounds (using Web Audio API)

### IMPORTANT FEATURES (High Priority)
- [X] **UI/UX Improvements**: Ability tooltips on hover, item descriptions, kill feed, team score display
- [X] **Visual Effects**: Particle effects for abilities, projectile trails, AoE indicators
- [X] **Minimap Enhancements**: Show jungle camps, enemy heroes, structure health
- [X] **AI Teammates**: Basic friendly AI for 5v5 experience
- [X] **Map Features**: Boss pit with powerful neutral, secret shop area, vision mechanics
- [X] **Leveling System**: XP curve properly tuned, stat gains per level working correctly

### NICE-TO-HAVE FEATURES (If Time Permits)
- [ ] **Advanced AI**: Enemy AI uses abilities strategically, retreats when low HP
- [ ] **Item Actives**: Active item abilities like Blink Dagger, Black King Bar
- [ ] **Ward System**: Observer wards for vision, sentry wards for detection
- [ ] **Quick Actions**: Minimap pings, quick-buy system, ability queue
- [ ] **Match Statistics**: Damage dealt, healing done, gold earned tracking
- [ ] **Spectator Features**: Free camera mode, replay system

## Verification Steps

After each significant change, verify success by:

1. **Browser Test**: Open in browser, check console for errors
```bash
python3 -m http.server 8000
# Open http://localhost:8000/dota3-legacy.html
# Check browser console (F12) for errors
```

2. **Functional Tests**: Test each new feature
   - Select a hero and verify abilities work (Q/W/E/R keys)
   - Check jungle camps spawn and give gold/XP on death
   - Purchase items from shop (B key) and verify stat bonuses
   - Verify sound effects play on actions
   - Check AI enemies attack and use abilities
   - Confirm damage numbers, death animations, and visual effects

3. **Code Quality**: Ensure no regressions
   - File remains self-contained (no external dependencies)
   - No JavaScript errors in console
   - Performance remains smooth (60 FPS target)
   - All existing features still work

4. **Git Commits**: Commit after each working feature
```bash
cd /Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools
git add dota3-legacy.html
git commit -m "feat(dota3): [description of feature]"
```

## Work Instructions

### Iteration Process
1. **Assess Current State**: Read dota3-legacy.html and identify next highest-priority incomplete feature
2. **Review Assets**: Check `/data/games/heroes/`, `/data/games/creeps/`, `/data/games/items/` for relevant data
3. **Implement Feature**: Add code following existing architecture patterns
4. **Test**: Verify feature works without breaking existing functionality
5. **Commit**: Git commit with clear message describing the change
6. **Update Progress**: Log the completion in `.claude/ralph-loop.local.md`
7. **Check Criteria**: If ALL critical + important features complete, output promise and exit

### Architecture Guidelines
- **Self-Contained**: All code inline, no CDN links or npm packages
- **Three.js Integration**: Use existing `THREE` global for 3D rendering
- **Model Builder Pattern**: Extend GameEntity/Hero classes, don't rewrite core
- **Web Audio API**: Use `AudioContext` for procedural sound generation (no external audio files)
- **Performance**: Keep file size reasonable, optimize render loop
- **Data Loading**: Load hero/item/creep data from `/data/games/` JSON files dynamically

### Feature Implementation Priority
Work in this order:
1. **Phase 1**: Ability system overhaul (cooldowns, mana, effects)
2. **Phase 2**: Jungle camps with respawn timers
3. **Phase 3**: Expanded item shop with recipes
4. **Phase 4**: Sound effects via Web Audio API
5. **Phase 5**: AI enemies (attack, abilities, farming)
6. **Phase 6**: Visual polish (particles, animations, effects)
7. **Phase 7**: AI teammates for 5v5
8. **Phase 8**: Game balance tuning
9. **Phase 9**: UI/UX improvements (tooltips, kill feed)
10. **Phase 10**: Map features (boss, secret shop, vision)

### Common Patterns to Use

#### Loading Hero Data
```javascript
async function loadHeroData(heroId) {
    const response = await fetch(`/data/games/heroes/${heroId}.json`);
    return await response.json();
}
```

#### Web Audio Sound Effect
```javascript
function playSound(type, frequency, duration) {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.value = frequency;
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);
    osc.start();
    osc.stop(ctx.currentTime + duration);
}
```

#### Particle Effect
```javascript
function createParticleEffect(x, y, z, color, count = 20) {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    // ... create particles using THREE.Points
    scene.add(particleSystem);
}
```

## Safety Measures
- **No External Dependencies**: Never add CDN links or require npm packages
- **Preserve Existing Code**: Don't delete working features
- **Incremental Changes**: Make small, testable changes
- **Git Checkpoints**: Commit after each working feature
- **Error Handling**: Gracefully handle missing assets or API failures
- **Performance Budget**: Keep file under 10,000 lines, maintain 60 FPS

## Escape Conditions
If you encounter blocking issues:
- **Missing Asset**: Note in commit message, continue with placeholder
- **Browser Compatibility**: Ensure Chrome/Firefox/Edge support
- **Performance Issue**: Profile and optimize before continuing
- **Stuck**: Skip feature, document in progress log, move to next priority

## Completion Promise
Only output this EXACT text when ALL critical features AND all important features are complete and verified:

<promise>DOTA3_LEGACY_COMPLETE_ALL_FEATURES_POLISHED</promise>

Do NOT output this promise if:
- Any critical feature is incomplete
- Browser console shows JavaScript errors
- Abilities don't work properly
- AI enemies are non-functional
- Sound effects are missing
- Visual effects are broken
- Game is unplayable or severely unbalanced

## Progress Tracking
After each iteration, update `/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/.claude/ralph-loop.local.md` with:
- Iteration number
- Features completed
- Current file size
- Issues encountered
- Next priorities

---

Remember: This is an autonomous loop. Work systematically through priorities, test thoroughly, commit frequently, and only output the promise when the game is truly complete and polished.
