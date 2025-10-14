# State Persistence Integration Guide

Complete guide for adding state persistence to local HTML applications using the LocalFirst State Management system.

## Quick Start

### 1. Add Files to Your Project

```html
<!-- In your HTML <head> or before </body> -->
<script src="localfirst-state-manager.js"></script>
```

### 2. Register Service Worker

The StateManager automatically registers the service worker, but ensure `localfirst-sw.js` is in your project root.

### 3. Initialize State Manager

```javascript
// Define capture and restore functions
function captureState() {
    return {
        // Capture all app state here
        windows: getOpenWindows(),
        desktop: getDesktopState(),
        settings: getUserSettings(),
        // etc...
    };
}

function restoreState(state) {
    // Restore app state here
    restoreWindows(state.windows);
    restoreDesktop(state.desktop);
    restoreSettings(state.settings);
}

// Initialize StateManager
const stateManager = new StateManager(
    'windows95-emulator',  // App ID
    '1.0.0',               // Schema version
    captureState,          // State capture function
    restoreState           // State restore function
);

// Restore saved state on load
document.addEventListener('DOMContentLoaded', () => {
    stateManager.init();
    stateManager.enableAutoSave(5000); // Auto-save every 5 seconds
});
```

## Windows 95 Emulator Integration

### Step 1: Add State Capture

Add this to the `Windows95Emulator` class:

```javascript
class Windows95Emulator {
    // ... existing code ...

    captureCompleteState() {
        return {
            // Window state
            windows: this.captureWindowState(),

            // Desktop state
            desktop: {
                icons: this.desktop.icons.map(icon => ({
                    x: icon.x,
                    y: icon.y,
                    label: icon.label,
                    emoji: icon.emoji,
                    selected: icon.selected
                }))
            },

            // Settings
            settings: {
                soundMuted: this.soundMuted,
                soundVolume: this.soundVolume,
                ...this.settings
            },

            // Program-specific states
            programs: this.captureProgramStates(),

            // File system
            fileSystem: this.captureFileSystem(),

            // Recycle Bin
            recycleBin: this.captureRecycleBin(),

            // Clipboard
            clipboard: { ...this.clipboard },

            // System state
            system: {
                uptime: Date.now() - this.startTime,
                frameCount: this.frameCount
            }
        };
    }

    captureWindowState() {
        const windows = document.querySelectorAll('.window');
        return Array.from(windows).map(win => ({
            id: win.dataset.windowId || Math.random().toString(36),
            title: win.querySelector('.window-title')?.textContent || '',
            program: win.dataset.program || 'unknown',
            position: {
                x: parseInt(win.style.left) || 0,
                y: parseInt(win.style.top) || 0
            },
            size: {
                width: parseInt(win.style.width) || 400,
                height: parseInt(win.style.height) || 300
            },
            zIndex: parseInt(win.style.zIndex) || 1000,
            minimized: win.style.display === 'none',
            maximized: win.classList.contains('maximized'),
            content: this.captureWindowContent(win)
        }));
    }

    captureWindowContent(windowElement) {
        // Capture program-specific content
        const program = windowElement.dataset.program;

        switch(program) {
            case 'notepad':
                const textarea = windowElement.querySelector('textarea');
                return textarea ? textarea.value : '';

            case 'calculator':
                const display = windowElement.querySelector('.calc-display');
                return display ? display.textContent : '0';

            case 'paint':
                const canvas = windowElement.querySelector('canvas');
                return canvas ? canvas.toDataURL() : null;

            // Add more programs as needed

            default:
                return null;
        }
    }

    captureProgramStates() {
        // Capture states of specific programs
        return {
            notepad: this.captureNotepadState(),
            calculator: this.captureCalculatorState(),
            minesweeper: this.captureMinesweeperState(),
            solitaire: this.captureSolitaireState(),
            // Add more...
        };
    }

    captureFileSystem() {
        // Get file system from localStorage or internal state
        const fsData = SafeStorage.getItem('win95-file-system');
        return fsData ? JSON.parse(fsData) : {};
    }

    captureRecycleBin() {
        const binData = SafeStorage.getItem('win95-recycle-bin');
        return binData ? JSON.parse(binData) : [];
    }

    // Add more capture methods as needed...
}
```

### Step 2: Add State Restoration

```javascript
class Windows95Emulator {
    // ... existing code ...

    restoreCompleteState(state) {
        if (!state) return;

        console.log('[Emulator] Restoring state...');

        // Restore settings
        if (state.settings) {
            this.soundMuted = state.settings.soundMuted;
            this.soundVolume = state.settings.soundVolume;
            Object.assign(this.settings, state.settings);
        }

        // Restore desktop icons
        if (state.desktop?.icons) {
            this.desktop.icons = state.desktop.icons;
            this.drawDesktop();
            state.desktop.icons.forEach(icon => {
                this.drawIcon(icon.x, icon.y, icon.label, icon.emoji, icon.selected);
            });
        }

        // Restore clipboard
        if (state.clipboard) {
            this.clipboard = state.clipboard;
        }

        // Restore file system
        if (state.fileSystem) {
            SafeStorage.setItem('win95-file-system', JSON.stringify(state.fileSystem));
        }

        // Restore recycle bin
        if (state.recycleBin) {
            SafeStorage.setItem('win95-recycle-bin', JSON.stringify(state.recycleBin));
        }

        // Restore program states
        if (state.programs) {
            this.restoreProgramStates(state.programs);
        }

        // Restore windows (with delay to ensure DOM is ready)
        if (state.windows && state.windows.length > 0) {
            setTimeout(() => {
                this.restoreWindows(state.windows);
            }, 100);
        }

        console.log('[Emulator] State restored successfully');
    }

    restoreWindows(windows) {
        windows.forEach((winState, index) => {
            setTimeout(() => {
                this.restoreWindow(winState);
            }, index * 100); // Stagger window restoration
        });
    }

    restoreWindow(winState) {
        // Launch the program
        const programMap = {
            notepad: () => this.openNotepad(),
            calculator: () => this.openCalculator(),
            paint: () => this.openPaint(),
            minesweeper: () => this.openMinesweeper(),
            // Add more...
        };

        if (programMap[winState.program]) {
            programMap[winState.program]();

            // Wait for window to be created, then restore its state
            setTimeout(() => {
                const windows = document.querySelectorAll('.window');
                const targetWin = windows[windows.length - 1]; // Last created window

                if (targetWin) {
                    // Restore position and size
                    targetWin.style.left = winState.position.x + 'px';
                    targetWin.style.top = winState.position.y + 'px';
                    targetWin.style.width = winState.size.width + 'px';
                    targetWin.style.height = winState.size.height + 'px';
                    targetWin.style.zIndex = winState.zIndex;

                    // Restore minimized/maximized state
                    if (winState.minimized) {
                        this.windowManager.minimizeWindow(targetWin);
                    } else if (winState.maximized) {
                        this.windowManager.maximizeWindow(targetWin);
                    }

                    // Restore content
                    this.restoreWindowContent(targetWin, winState);
                }
            }, 50);
        }
    }

    restoreWindowContent(windowElement, winState) {
        const program = winState.program;

        switch(program) {
            case 'notepad':
                const textarea = windowElement.querySelector('textarea');
                if (textarea && winState.content) {
                    textarea.value = winState.content;
                }
                break;

            case 'calculator':
                const display = windowElement.querySelector('.calc-display');
                if (display && winState.content) {
                    display.textContent = winState.content;
                }
                break;

            case 'paint':
                const canvas = windowElement.querySelector('canvas');
                if (canvas && winState.content) {
                    const ctx = canvas.getContext('2d');
                    const img = new Image();
                    img.onload = () => ctx.drawImage(img, 0, 0);
                    img.src = winState.content;
                }
                break;

            // Add more programs...
        }
    }

    restoreProgramStates(programs) {
        // Restore program-specific states
        // This might set up internal state before windows are created
    }
}
```

### Step 3: Wire Up StateManager

```javascript
// After Windows95Emulator is defined, create and initialize StateManager
let emulator;
let stateManager;

document.addEventListener('DOMContentLoaded', () => {
    // Create emulator
    emulator = new Windows95Emulator();

    // Create state manager
    stateManager = new StateManager(
        'windows95-emulator',
        '1.0.0',
        () => emulator.captureCompleteState(),
        (state) => emulator.restoreCompleteState(state)
    );

    // Initialize and restore state
    stateManager.init();

    // Enable auto-save
    stateManager.enableAutoSave(5000);

    // Mark state as dirty when things change
    // Add listeners for state changes
    document.addEventListener('window-created', () => stateManager.markDirty());
    document.addEventListener('window-closed', () => stateManager.markDirty());
    document.addEventListener('icon-moved', () => stateManager.markDirty());
    // etc...

    // Make available globally
    window.emulator = emulator;
    window.stateManager = stateManager;
});
```

## Version Migration

### Define Migration Functions

```javascript
// Migration from 1.0.0 to 1.1.0
stateManager.registerMigration('1.0.0', '1.1.0', (data) => {
    console.log('Migrating 1.0.0 -> 1.1.0');

    // Example: Add new property to windows
    if (data.state.windows) {
        data.state.windows.forEach(win => {
            win.newProperty = 'defaultValue';
        });
    }

    return data;
});

// Migration from 1.1.0 to 2.0.0
stateManager.registerMigration('1.1.0', '2.0.0', (data) => {
    console.log('Migrating 1.1.0 -> 2.0.0');

    // Example: Restructure desktop icons
    if (data.state.desktop?.icons) {
        data.state.desktop.icons = data.state.desktop.icons.map(icon => ({
            ...icon,
            id: Math.random().toString(36)
        }));
    }

    return data;
});
```

## User Controls

### Add UI for State Management

```javascript
// Add to Control Panel or Settings

function createStateManagerUI() {
    const content = `
        <div style="padding: 20px;">
            <h2>State Management</h2>

            <div style="margin: 20px 0;">
                <h3>Storage Info</h3>
                <div id="storage-info"></div>
            </div>

            <div style="margin: 20px 0;">
                <button class="btn" onclick="stateManager.save('manual')">
                    💾 Save State Now
                </button>

                <button class="btn" onclick="stateManager.exportState()">
                    📤 Export State
                </button>

                <button class="btn" onclick="importStateDialog()">
                    📥 Import State
                </button>

                <button class="btn" onclick="confirmClearState()">
                    🗑️ Clear State
                </button>
            </div>

            <div style="margin: 20px 0;">
                <h3>State History</h3>
                <div id="state-history"></div>
            </div>
        </div>
    `;

    emulator.windowManager.createWindow('State Manager', content, {
        width: 500,
        height: 600
    });

    updateStorageInfo();
    updateStateHistory();
}

function updateStorageInfo() {
    const info = stateManager.getStorageInfo();
    const infoDiv = document.getElementById('storage-info');
    if (infoDiv) {
        infoDiv.innerHTML = `
            <div>Current: ${info.current} KB</div>
            <div>Previous: ${info.previous} KB</div>
            <div>History: ${info.history} KB</div>
            <div><strong>Total: ${info.total} KB</strong></div>
        `;
    }
}

function updateStateHistory() {
    const history = stateManager.getHistory();
    const historyDiv = document.getElementById('state-history');
    if (historyDiv) {
        historyDiv.innerHTML = history.map(entry => `
            <div style="margin: 5px 0; padding: 5px; border: 1px solid #ccc;">
                ${new Date(entry.timestamp).toLocaleString()} -
                ${entry.reason} -
                ${Math.round(entry.size / 1024)} KB
            </div>
        `).join('');
    }
}

function confirmClearState() {
    if (confirm('Clear all saved state? This cannot be undone.')) {
        stateManager.clear();
        alert('State cleared!');
        location.reload();
    }
}

function importStateDialog() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                if (stateManager.importState(event.target.result)) {
                    alert('State imported successfully!');
                    location.reload();
                } else {
                    alert('Failed to import state.');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}
```

## Testing

### Test Save/Restore Cycle

```javascript
// 1. Use the app (create windows, move icons, etc.)
// 2. Check state saved: console.log(localStorage.getItem('windows95-emulator-state-current'))
// 3. Refresh the page
// 4. Verify everything restored correctly

// Manual test
function testStateManagement() {
    console.log('=== Testing State Management ===');

    // Save current state
    console.log('Saving state...');
    stateManager.save('test');

    // Check state size
    console.log('State size:', stateManager.getStateSize(), 'bytes');

    // Get storage info
    console.log('Storage info:', stateManager.getStorageInfo());

    // Export state for inspection
    const state = localStorage.getItem('windows95-emulator-state-current');
    console.log('Current state:', JSON.parse(state));

    console.log('=== Test Complete ===');
}
```

## Best Practices

1. **Capture Minimal State**: Only save what's necessary to restore the experience
2. **Debounce Auto-Save**: Don't save on every keystroke, use 3-5 second intervals
3. **Test Migrations**: Always test version migrations with real data
4. **Handle Errors**: Gracefully handle corrupted or missing state
5. **User Control**: Give users clear controls to manage their state
6. **Monitor Size**: Watch state size and warn if approaching storage limits
7. **Document Schema**: Keep schema version docs up to date

## Troubleshooting

### State Not Saving
- Check browser console for errors
- Verify localStorage is available (not private browsing)
- Check storage quota (5-10MB typical limit)

### State Not Restoring
- Verify state exists: `localStorage.getItem('windows95-emulator-state-current')`
- Check for JSON parsing errors
- Verify schema version compatibility

### Large State Size
- Remove unnecessary data from capture
- Compress large strings (canvas data, etc.)
- Clean up old history entries

## Next Steps

Once integrated:
1. Test thoroughly with different scenarios
2. Add migration functions for schema changes
3. Monitor state size in production
4. Add user feedback for save/restore events
5. Consider adding cloud sync (optional)

## Complete Example

See `windows95-emulator.html` for full implementation example with all features integrated.
