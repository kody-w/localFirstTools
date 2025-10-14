/**
 * Windows 95 State Persistence System
 *
 * ULTRA THINK: Data sloshing pattern for local state caching
 * - Captures emulator state to localStorage/IndexedDB
 * - Restores state on page reload
 * - Generates JSON snapshots for AI analysis
 * - Enables time-travel (undo/redo through state history)
 */

class StatePersistence {
    constructor(emulator) {
        this.emulator = emulator;
        this.dbName = 'windows95_state_db';
        this.storeName = 'state_history';
        this.db = null;
        this.maxHistorySize = 50; // Keep last 50 states

        this.init();
    }

    async init() {
        console.log('🔄 State Persistence: Initializing...');

        // Open IndexedDB for large state storage
        await this.openDB();

        // Try to restore previous state
        await this.restoreState();

        // Start auto-save
        this.startAutoSave();

        // Save state before page unload
        window.addEventListener('beforeunload', () => this.saveState());

        console.log('✅ State Persistence: Ready');
    }

    /**
     * Open IndexedDB connection
     */
    async openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, 1);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(this.storeName)) {
                    db.createObjectStore(this.storeName, { keyPath: 'timestamp' });
                }
            };
        });
    }

    /**
     * Capture complete emulator state
     */
    captureState() {
        const state = {
            timestamp: Date.now(),

            // Windows state
            windows: Array.from(document.querySelectorAll('.window')).map(w => ({
                id: w.dataset.windowId || w.id,
                title: w.querySelector('.window-titlebar-text')?.textContent || 'Unknown',
                position: {
                    x: parseInt(w.style.left) || 0,
                    y: parseInt(w.style.top) || 0
                },
                size: {
                    width: parseInt(w.style.width) || w.offsetWidth,
                    height: parseInt(w.style.height) || w.offsetHeight
                },
                zIndex: w.style.zIndex || 10,
                minimized: w.classList.contains('minimized'),
                maximized: w.classList.contains('maximized'),
                active: w.classList.contains('active'),
                content: w.querySelector('.window-content')?.innerHTML || ''
            })),

            // Desktop icons
            icons: Array.from(document.querySelectorAll('.desktop-icon')).map(icon => ({
                id: icon.dataset.iconId || icon.id,
                name: icon.querySelector('.icon-text')?.textContent || 'Unknown',
                position: {
                    x: parseInt(icon.style.left) || 0,
                    y: parseInt(icon.style.top) || 0
                },
                selected: icon.classList.contains('selected')
            })),

            // Start menu state
            startMenu: {
                open: document.getElementById('start-menu')?.classList.contains('active') || false,
                searchValue: document.getElementById('start-menu-search')?.value || ''
            },

            // Taskbar buttons
            taskbar: Array.from(document.querySelectorAll('.taskbar-button')).map(btn => ({
                windowId: btn.dataset.windowId,
                active: btn.classList.contains('active'),
                text: btn.textContent
            })),

            // Canvas state (for custom drawings/overlays)
            canvasState: this.captureCanvasState(),

            // User preferences
            preferences: this.loadPreferences(),

            // Metadata
            metadata: {
                userAgent: navigator.userAgent,
                screenResolution: `${window.screen.width}x${window.screen.height}`,
                timestamp: new Date().toISOString()
            }
        };

        return state;
    }

    /**
     * Capture canvas state (if there are overlays)
     */
    captureCanvasState() {
        const canvas = document.getElementById('screen');
        if (!canvas) return null;

        try {
            return {
                dataURL: canvas.toDataURL('image/png'),
                width: canvas.width,
                height: canvas.height
            };
        } catch (e) {
            // Canvas might be tainted by cross-origin content
            console.warn('Cannot capture canvas state:', e);
            return null;
        }
    }

    /**
     * Save current state to localStorage (quick access) and IndexedDB (history)
     */
    async saveState() {
        const state = this.captureState();

        // Save to localStorage for quick restore
        try {
            localStorage.setItem('windows95_current_state', JSON.stringify(state));
            console.log('💾 State saved to localStorage');
        } catch (e) {
            console.warn('localStorage full, saving to IndexedDB only');
        }

        // Save to IndexedDB for history
        await this.saveToHistory(state);

        // Generate JSON file for AI/external tools
        await this.generateStateJSON(state);

        return state;
    }

    /**
     * Save state to IndexedDB history
     */
    async saveToHistory(state) {
        if (!this.db) return;

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readwrite');
            const store = transaction.objectStore(this.storeName);

            store.add(state);

            transaction.oncomplete = () => {
                console.log('💾 State saved to history');
                this.pruneHistory(); // Keep history size manageable
                resolve();
            };
            transaction.onerror = () => reject(transaction.error);
        });
    }

    /**
     * Restore state from localStorage or IndexedDB
     */
    async restoreState() {
        console.log('🔄 Attempting to restore previous state...');

        // Try localStorage first (fastest)
        const cached = localStorage.getItem('windows95_current_state');
        if (cached) {
            try {
                const state = JSON.parse(cached);
                await this.applyState(state);
                console.log('✅ State restored from localStorage');
                return state;
            } catch (e) {
                console.warn('Failed to restore from localStorage:', e);
            }
        }

        // Try IndexedDB (get most recent)
        const state = await this.getMostRecentState();
        if (state) {
            await this.applyState(state);
            console.log('✅ State restored from IndexedDB');
            return state;
        }

        console.log('ℹ️ No previous state found, starting fresh');
        return null;
    }

    /**
     * Apply saved state to emulator
     */
    async applyState(state) {
        if (!state) return;

        console.log('🔄 Applying saved state...');

        // Close all existing windows
        document.querySelectorAll('.window').forEach(w => {
            if (this.emulator.closeWindow) {
                this.emulator.closeWindow(w);
            } else {
                w.remove();
            }
        });

        // Recreate windows
        for (const windowState of state.windows) {
            const win = this.emulator.createWindow(
                windowState.title,
                windowState.content,
                windowState.size.width,
                windowState.size.height,
                windowState.position.x,
                windowState.position.y
            );

            if (win) {
                win.dataset.windowId = windowState.id;
                win.style.zIndex = windowState.zIndex;

                if (windowState.minimized) {
                    win.classList.add('minimized');
                    win.style.display = 'none';
                }
                if (windowState.maximized) {
                    win.classList.add('maximized');
                }
                if (windowState.active) {
                    win.classList.add('active');
                }
            }
        }

        // Restore desktop icons
        state.icons.forEach(iconState => {
            const icon = document.querySelector(`[data-icon-id="${iconState.id}"]`);
            if (icon) {
                icon.style.left = iconState.position.x + 'px';
                icon.style.top = iconState.position.y + 'px';
                if (iconState.selected) {
                    icon.classList.add('selected');
                }
            }
        });

        // Restore start menu
        if (state.startMenu.open && this.emulator.toggleStartMenu) {
            this.emulator.toggleStartMenu();
        }

        // Restore preferences
        if (state.preferences) {
            this.applyPreferences(state.preferences);
        }

        console.log('✅ State applied successfully');
    }

    /**
     * Get most recent state from IndexedDB
     */
    async getMostRecentState() {
        if (!this.db) return null;

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readonly');
            const store = transaction.objectStore(this.storeName);
            const request = store.openCursor(null, 'prev'); // Get newest first

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                resolve(cursor ? cursor.value : null);
            };
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Get all states from history
     */
    async getAllStates() {
        if (!this.db) return [];

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readonly');
            const store = transaction.objectStore(this.storeName);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Prune history to keep size manageable
     */
    async pruneHistory() {
        const states = await this.getAllStates();

        if (states.length > this.maxHistorySize) {
            const toDelete = states
                .sort((a, b) => a.timestamp - b.timestamp)
                .slice(0, states.length - this.maxHistorySize);

            const transaction = this.db.transaction([this.storeName], 'readwrite');
            const store = transaction.objectStore(this.storeName);

            toDelete.forEach(state => {
                store.delete(state.timestamp);
            });
        }
    }

    /**
     * Generate JSON file that can be read by AI or external tools
     */
    async generateStateJSON(state) {
        // Create a downloadable JSON file
        const json = JSON.stringify(state, null, 2);

        // Save to a virtual file system (using localStorage as proxy)
        localStorage.setItem('windows95_state_export', json);

        // Also trigger a download if requested
        if (window.downloadStateJSON) {
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `windows95-state-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        return json;
    }

    /**
     * Load user preferences
     */
    loadPreferences() {
        const prefs = localStorage.getItem('windows95_preferences');
        return prefs ? JSON.parse(prefs) : this.getDefaultPreferences();
    }

    /**
     * Get default preferences
     */
    getDefaultPreferences() {
        return {
            theme: 'classic',
            soundEnabled: true,
            animationsEnabled: true,
            autoSaveInterval: 30000, // 30 seconds
            fontSize: 11,
            iconSpacing: 80
        };
    }

    /**
     * Apply preferences to emulator
     */
    applyPreferences(prefs) {
        // Apply theme
        if (prefs.theme && prefs.theme !== 'classic') {
            document.documentElement.dataset.theme = prefs.theme;
        }

        // Apply font size
        if (prefs.fontSize) {
            document.documentElement.style.fontSize = prefs.fontSize + 'px';
        }

        // Store for future use
        localStorage.setItem('windows95_preferences', JSON.stringify(prefs));
    }

    /**
     * Start auto-save timer
     */
    startAutoSave() {
        const prefs = this.loadPreferences();
        const interval = prefs.autoSaveInterval || 30000;

        setInterval(() => {
            this.saveState();
        }, interval);

        console.log(`🔄 Auto-save enabled (every ${interval/1000}s)`);
    }

    /**
     * Export state as JSON file for download
     */
    exportState() {
        const state = this.captureState();
        const json = JSON.stringify(state, null, 2);

        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `windows95-state-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        console.log('📥 State exported');
    }

    /**
     * Import state from JSON file
     */
    async importState(jsonString) {
        try {
            const state = JSON.parse(jsonString);
            await this.applyState(state);
            await this.saveState(); // Save imported state
            console.log('📤 State imported successfully');
            return true;
        } catch (e) {
            console.error('Failed to import state:', e);
            return false;
        }
    }

    /**
     * Time travel: go back to a specific timestamp
     */
    async timeTravel(timestamp) {
        if (!this.db) return false;

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readonly');
            const store = transaction.objectStore(this.storeName);
            const request = store.get(timestamp);

            request.onsuccess = async () => {
                if (request.result) {
                    await this.applyState(request.result);
                    console.log('⏰ Time traveled to', new Date(timestamp).toISOString());
                    resolve(true);
                } else {
                    console.warn('No state found for timestamp', timestamp);
                    resolve(false);
                }
            };
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Get state history for UI display
     */
    async getStateHistory() {
        const states = await this.getAllStates();
        return states
            .sort((a, b) => b.timestamp - a.timestamp)
            .map(state => ({
                timestamp: state.timestamp,
                date: new Date(state.timestamp).toISOString(),
                windowCount: state.windows.length,
                iconCount: state.icons.length
            }));
    }

    /**
     * Clear all state data
     */
    async clearAllStates() {
        // Clear localStorage
        localStorage.removeItem('windows95_current_state');
        localStorage.removeItem('windows95_state_export');

        // Clear IndexedDB
        if (this.db) {
            const transaction = this.db.transaction([this.storeName], 'readwrite');
            const store = transaction.objectStore(this.storeName);
            store.clear();
        }

        console.log('🗑️ All states cleared');
    }
}

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatePersistence;
}

// Browser global
if (typeof window !== 'undefined') {
    window.StatePersistence = StatePersistence;
}
