# Implementation Plan: Public Planets via GitHub for LEVIATHAN: OMNIVERSE

## 8-Strategy Consensus Analysis

### Unanimous Agreement (8/8 strategies):

1. **GitHub Public Planets is THE core feature** - All strategies identify this as the primary value proposition that enables "worldwide planet sharing via QR code"

2. **Existing infrastructure must be reused** - levi.html already has:
   - P2P spectator streaming via PeerJS (lines 52780-53213)
   - QR code generation with QRious library (line 53165)
   - URL parameter handling: `?spectate=`, `?join=`, `?planet=`, `?seed=` (line 56198)
   - `applyFullState()` for world state application
   - Show Mode modal with share functionality

3. **Holographic Companion Manager is LOWEST priority** - 4/5 complexity, medium user value, memory-intensive video textures

4. **Feature flags/toggles are essential** - All strategies recommend graceful degradation patterns

### Strong Agreement (6-7/8 strategies):

5. **Settings Manager should come early** - Foundation for voice/AI features
6. **Use existing object-literal pattern** - Match `SteamDeckManager` style (line 15170)
7. **MVP requires ~50-100 lines** - Not thousands
8. **SKIP THREE.js extensions** - FontLoader, Font, TextGeometry already exist (lines 12018-12155)

### Majority Agreement (5/8 strategies):

9. **Integration order**: GitHub Planets → Settings → Voice → AI → Holographic
10. **Use EventBus pattern** for decoupled communication
11. **Mobile optimizations**: Disable video textures, reduce text complexity

---

## Recommended Implementation: Phased Approach

### Phase 1: GitHub Public Planets (MVP)
**Estimated Lines: ~55-70**
**Complexity: 2/5**
**User Impact: HIGH**

This phase delivers the core value proposition with minimal code changes.

#### 1.1 New URL Parameter
Add support for `?github=username/repo/planetId` format.

**Location**: Modify `checkMultiplayerMode()` at line ~56198

```javascript
// Add after existing URL parameter checks
const githubPlanet = params.get('github');
if (githubPlanet) {
    console.log('[PUBLIC PLANET] Loading from GitHub:', githubPlanet);
    loadPublicPlanetFromGitHub(githubPlanet);
    return;
}
```

#### 1.2 GitHub Fetch Function
**Location**: Add near line ~52780 (after P2P section)

```javascript
async function loadPublicPlanetFromGitHub(githubPath) {
    // Parse: username/repo/planetId
    const parts = githubPath.split('/');
    if (parts.length < 3) {
        showNotification('Invalid planet URL format', 'error');
        return;
    }

    const [username, repo, ...planetPath] = parts;
    const planetId = planetPath.join('/');
    const url = `https://raw.githubusercontent.com/${username}/${repo}/main/planets/${planetId}.json`;

    // Show loading UI
    document.getElementById('loading').style.display = 'block';
    document.getElementById('loading').innerHTML = `
        <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 20px;">🌍</div>
            <div style="font-size: 24px; color: #0ff;">Loading Public Planet...</div>
            <div style="font-size: 14px; color: #888; margin-top: 10px;">${planetId}</div>
        </div>
    `;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Planet not found (HTTP ${response.status})`);

        const planetState = await response.json();

        // Validate required fields
        if (!planetState.worldSeed || !planetState.civilization) {
            throw new Error('Invalid planet configuration');
        }

        // Apply using existing infrastructure
        applyFullState(planetState);

        showNotification(`Welcome to ${planetState.civilization?.name || planetId}!`, 'success');
        document.getElementById('loading').style.display = 'none';

    } catch (error) {
        console.error('[PUBLIC PLANET] Load failed:', error);
        showNotification(`Failed to load planet: ${error.message}`, 'error');
        document.getElementById('loading').style.display = 'none';

        // Fallback: start normal game
        init();
    }
}
```

#### 1.3 Generate Public Planet URL
**Location**: Extend existing `setShareMode()` function at line ~54538

Add new share mode option:

```javascript
// In setShareMode() switch statement, add:
case 'public':
    // Generate GitHub-compatible URL
    const githubPath = prompt('Enter GitHub path (username/repo/planetId):');
    if (githubPath) {
        shareUrl = `${window.location.origin}${window.location.pathname}?github=${encodeURIComponent(githubPath)}`;
    }
    break;
```

#### 1.4 UI Addition (Optional)
Add "Public Planet" tab to existing Show Mode modal.

**Location**: Modify `openShowModeModal()` at line ~54522

```javascript
// Add new tab button in share mode selection
<button onclick="setShareMode('public')" class="share-mode-btn">
    🌐 Public Planet
</button>
```

#### 1.5 Planet Config JSON Schema
Document the expected format for GitHub-hosted planet configs:

```json
{
    "type": "fullState",
    "worldSeed": "volcano-world-2024",
    "civilization": {
        "id": 42,
        "name": "Volcano Prime",
        "biome": "Volcanic"
    },
    "world": {
        "timeOfDay": 0.5,
        "player": { "position": {"x": 0, "y": 0, "z": 0} },
        "mobs": [],
        "structures": [],
        "interactables": []
    },
    "agents": [],
    "customProps": {}
}
```

---

### Phase 2: Foundation Infrastructure (Optional)
**Estimated Lines: ~150**
**Complexity: 2/5**

Only implement if Phase 1 is successful and more features are needed.

#### 2.1 Feature Flags System
```javascript
const FeatureFlags = {
    STORAGE_KEY: 'leviathan-feature-flags',
    defaults: {
        'github-planets': true,
        'settings-manager': false,
        'voice-manager': false,
        'ai-manager': false,
        'holographic-companion': false
    },
    // ... init, isEnabled, setEnabled methods
};
```

#### 2.2 EventBus (Decoupled Communication)
```javascript
const EventBus = {
    listeners: {},
    on(event, callback) { /* ... */ },
    emit(event, data) { /* ... */ },
    off(event, callback) { /* ... */ }
};
```

#### 2.3 Settings Manager
- Consolidate existing scattered settings
- Import/export JSON functionality
- localStorage persistence with `leviathan_enhanced_settings` key

---

### Phase 3-8: Progressive Additions (Deferred)

These phases should ONLY be implemented after Phase 1 is validated:

| Phase | Feature | Complexity | Priority |
|-------|---------|------------|----------|
| 3 | Voice Manager (TTS) | 3/5 | Medium |
| 4 | Voice Input Manager | 2/5 | Medium |
| 5 | Perspective Manager | 2/5 | Low |
| 6 | Task Manager | 2/5 | Low |
| 7 | AI Manager | 4/5 | Medium |
| 8 | Holographic Companion | 4/5 | Low |

---

## Critical Implementation Rules

### DO:
- Use existing `applyFullState()` for world initialization
- Reuse QR code generation infrastructure
- Follow object-literal manager pattern (like `SteamDeckManager`)
- Gate features behind `FeatureFlags.isEnabled()` checks
- Use CSS variables for z-index (not hardcoded values)
- Use `leviathan_*` prefix for new localStorage keys

### DO NOT:
- Redefine `THREE.FontLoader`, `THREE.Font`, `THREE.TextGeometry` (already exist)
- Redefine `p2pStreaming` object (extend it instead)
- Add new animation keyframes without `showmode-` prefix
- Add HolographicCompanionManager on mobile devices
- Block the render loop with synchronous API calls

---

## Conflict Resolutions

| Conflict | Resolution |
|----------|------------|
| `ShowModeManager` class vs existing `openShowModeModal()` | SKIP class, enhance existing functions |
| THREE.js extensions | SKIP - already implemented at lines 12018-12155 |
| Animation keyframes (fadeIn, pulse) | Rename to `showmode-fadeIn`, `showmode-pulse` |
| z-index collisions | Use `var(--z-modal-content)` (9500) from design tokens |
| localStorage keys | Use `leviathan_showmode_*` namespace |

---

## Testing Checkpoints

### Phase 1 Validation:
- [ ] Game loads normally when `?github=` param is missing
- [ ] Valid GitHub planet URL loads world correctly
- [ ] Invalid GitHub URL shows error, falls back to normal game
- [ ] QR code generates correct `?github=` URL
- [ ] Mobile responsiveness unaffected
- [ ] Existing P2P spectator mode still works

### Performance Targets:
- No FPS drop from GitHub fetch (async operation)
- Loading indicator shows during fetch
- Graceful timeout after 10 seconds

---

## File Locations

**Primary file**: `/Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/apps/games/levi.html`

**Key line references**:
- URL parameter parsing: ~56198 (`checkMultiplayerMode()`)
- P2P streaming: ~26786 (`p2pStreaming` object)
- QR code generation: ~53165 (`generateSpectatorQRCode()`)
- Show Mode modal: ~54522 (`openShowModeModal()`)
- Main init: ~47206 (`init()` function)
- THREE.js extensions: ~12018-12155 (FontLoader, TextGeometry)

---

## Summary

**MVP (Phase 1)**: ~55-70 lines of code to enable worldwide public planet sharing via GitHub raw URLs and QR codes.

**Full Integration (All Phases)**: ~3000-5000 lines if all 8 managers are added.

**Recommendation**: Implement Phase 1 only. It delivers the core "public planets via QR code" functionality with minimal risk. Additional phases can be added incrementally based on user feedback.
