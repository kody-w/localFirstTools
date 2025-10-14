/**
 * LocalFirst State Manager
 * Handles state persistence, restoration, and migration for local HTML applications
 *
 * Usage:
 * const stateManager = new StateManager('my-app', '1.0.0', captureStateFn, restoreStateFn);
 * stateManager.init(); // Restores saved state
 * stateManager.enableAutoSave(); // Auto-saves on changes
 */

class StateManager {
    constructor(appId, schemaVersion, captureStateFn, restoreStateFn) {
        this.appId = appId;
        this.schemaVersion = schemaVersion;
        this.captureState = captureStateFn;
        this.restoreStateImpl = restoreStateFn;

        this.storageKey = `${appId}-state-current`;
        this.previousKey = `${appId}-state-previous`;
        this.historyKey = `${appId}-state-history`;

        this.autoSaveEnabled = false;
        this.autoSaveInterval = null;
        this.savePending = false;

        // Migration registry
        this.migrations = {};

        // Bind methods
        this.save = this.save.bind(this);
        this.restore = this.restore.bind(this);
        this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
    }

    /**
     * Initialize state manager and restore saved state
     */
    init() {
        console.log(`[StateManager] Initializing for ${this.appId}...`);

        // Register service worker if available
        this.registerServiceWorker();

        // Listen for updates from service worker
        this.listenForUpdates();

        // Restore saved state
        const restored = this.restore();

        // Set up beforeunload save
        window.addEventListener('beforeunload', this.handleBeforeUnload);

        return restored;
    }

    /**
     * Register service worker for HTML caching
     */
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/localfirst-sw.js')
                .then((registration) => {
                    console.log('[StateManager] Service Worker registered:', registration);
                })
                .catch((error) => {
                    console.warn('[StateManager] Service Worker registration failed:', error);
                });
        }
    }

    /**
     * Listen for update notifications from service worker
     */
    listenForUpdates() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.addEventListener('message', (event) => {
                if (event.data.type === 'UPDATE_AVAILABLE') {
                    this.handleUpdateAvailable(event.data);
                }
            });
        }
    }

    /**
     * Handle update notification
     */
    handleUpdateAvailable(data) {
        console.log('[StateManager] Update available for:', data.url);

        // Show notification to user
        const shouldReload = confirm(
            '🔄 A new version is available!\n\n' +
            'Your work will be saved and the page will reload.\n\n' +
            'Reload now?'
        );

        if (shouldReload) {
            // Save current state before reload
            this.save('beforeUpdate');

            // Reload page
            window.location.reload();
        }
    }

    /**
     * Enable auto-save with debouncing
     */
    enableAutoSave(intervalMs = 5000) {
        if (this.autoSaveEnabled) return;

        this.autoSaveEnabled = true;

        // Debounced save
        this.autoSaveInterval = setInterval(() => {
            if (this.savePending) {
                this.save('auto');
                this.savePending = false;
            }
        }, intervalMs);

        console.log(`[StateManager] Auto-save enabled (${intervalMs}ms)`);
    }

    /**
     * Disable auto-save
     */
    disableAutoSave() {
        if (this.autoSaveInterval) {
            clearInterval(this.autoSaveInterval);
            this.autoSaveInterval = null;
        }
        this.autoSaveEnabled = false;
        console.log('[StateManager] Auto-save disabled');
    }

    /**
     * Mark that state has changed (triggers auto-save)
     */
    markDirty() {
        this.savePending = true;
    }

    /**
     * Save current state to localStorage
     */
    save(reason = 'manual') {
        try {
            const appState = this.captureState();

            const state = {
                metadata: {
                    version: this.schemaVersion,
                    schemaVersion: this.schemaVersion,
                    timestamp: Date.now(),
                    appId: this.appId,
                    sessionId: this.getSessionId(),
                    saveReason: reason
                },
                state: appState
            };

            // Move current to previous
            const current = localStorage.getItem(this.storageKey);
            if (current) {
                localStorage.setItem(this.previousKey, current);
            }

            // Save new state
            const serialized = JSON.stringify(state);
            localStorage.setItem(this.storageKey, serialized);

            // Add to history (keep last 10)
            this.addToHistory(state);

            console.log(`[StateManager] State saved (${reason}):`, Math.round(serialized.length / 1024), 'KB');

            return true;
        } catch (error) {
            console.error('[StateManager] Failed to save state:', error);

            // If quota exceeded, try to clear history and retry
            if (error.name === 'QuotaExceededError') {
                localStorage.removeItem(this.historyKey);
                try {
                    const state = {
                        metadata: {
                            version: this.schemaVersion,
                            timestamp: Date.now(),
                            appId: this.appId
                        },
                        state: this.captureState()
                    };
                    localStorage.setItem(this.storageKey, JSON.stringify(state));
                    console.log('[StateManager] State saved after clearing history');
                    return true;
                } catch (retryError) {
                    console.error('[StateManager] Failed to save even after cleanup:', retryError);
                }
            }

            return false;
        }
    }

    /**
     * Restore state from localStorage
     */
    restore() {
        try {
            const saved = localStorage.getItem(this.storageKey);

            if (!saved) {
                console.log('[StateManager] No saved state found');
                return null;
            }

            const data = JSON.parse(saved);

            // Migrate if needed
            const migrated = this.migrate(data);

            // Restore state using app-provided function
            if (this.restoreStateImpl) {
                this.restoreStateImpl(migrated.state);
            }

            console.log('[StateManager] State restored from:', new Date(data.metadata.timestamp));

            return migrated.state;
        } catch (error) {
            console.error('[StateManager] Failed to restore state:', error);

            // Try to restore previous state
            return this.restorePrevious();
        }
    }

    /**
     * Restore previous state (fallback)
     */
    restorePrevious() {
        try {
            const saved = localStorage.getItem(this.previousKey);
            if (!saved) return null;

            const data = JSON.parse(saved);
            const migrated = this.migrate(data);

            if (this.restoreStateImpl) {
                this.restoreStateImpl(migrated.state);
            }

            console.log('[StateManager] Restored previous state');
            return migrated.state;
        } catch (error) {
            console.error('[StateManager] Failed to restore previous state:', error);
            return null;
        }
    }

    /**
     * Migrate state to current schema version
     */
    migrate(data) {
        const savedVersion = data.metadata.schemaVersion || data.metadata.version;

        if (savedVersion === this.schemaVersion) {
            return data;
        }

        console.log(`[StateManager] Migrating state from ${savedVersion} to ${this.schemaVersion}`);

        // Run migration functions
        let migrated = data;
        for (const [key, migrationFn] of Object.entries(this.migrations)) {
            const [from, to] = key.split('->');
            if (savedVersion === from) {
                migrated = migrationFn(migrated);
                console.log(`[StateManager] Migrated ${from} -> ${to}`);
            }
        }

        // Update metadata
        migrated.metadata.schemaVersion = this.schemaVersion;

        return migrated;
    }

    /**
     * Register a migration function
     */
    registerMigration(fromVersion, toVersion, migrationFn) {
        const key = `${fromVersion}->${toVersion}`;
        this.migrations[key] = migrationFn;
        console.log(`[StateManager] Registered migration: ${key}`);
    }

    /**
     * Clear all saved state
     */
    clear() {
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.previousKey);
        localStorage.removeItem(this.historyKey);
        console.log('[StateManager] All saved state cleared');
    }

    /**
     * Export state as JSON
     */
    exportState() {
        const saved = localStorage.getItem(this.storageKey);
        if (!saved) return null;

        const blob = new Blob([saved], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.appId}-state-${Date.now()}.json`;
        a.click();

        URL.revokeObjectURL(url);

        console.log('[StateManager] State exported');
    }

    /**
     * Import state from JSON
     */
    importState(jsonString) {
        try {
            const data = JSON.parse(jsonString);

            // Validate
            if (data.metadata.appId !== this.appId) {
                throw new Error('State is for a different application');
            }

            // Save as current state
            localStorage.setItem(this.storageKey, jsonString);

            // Restore
            this.restore();

            console.log('[StateManager] State imported successfully');
            return true;
        } catch (error) {
            console.error('[StateManager] Failed to import state:', error);
            return false;
        }
    }

    /**
     * Get state history
     */
    getHistory() {
        try {
            const history = localStorage.getItem(this.historyKey);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('[StateManager] Failed to get history:', error);
            return [];
        }
    }

    /**
     * Add state to history
     */
    addToHistory(state) {
        try {
            let history = this.getHistory();

            // Add new state
            history.push({
                timestamp: state.metadata.timestamp,
                reason: state.metadata.saveReason,
                size: JSON.stringify(state).length
            });

            // Keep last 10
            if (history.length > 10) {
                history = history.slice(-10);
            }

            localStorage.setItem(this.historyKey, JSON.stringify(history));
        } catch (error) {
            console.error('[StateManager] Failed to add to history:', error);
        }
    }

    /**
     * Get or create session ID
     */
    getSessionId() {
        let sessionId = sessionStorage.getItem('session-id');
        if (!sessionId) {
            sessionId = `${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
            sessionStorage.setItem('session-id', sessionId);
        }
        return sessionId;
    }

    /**
     * Handle beforeunload event
     */
    handleBeforeUnload() {
        this.save('beforeUnload');
    }

    /**
     * Get state size
     */
    getStateSize() {
        const saved = localStorage.getItem(this.storageKey);
        return saved ? saved.length : 0;
    }

    /**
     * Get storage info
     */
    getStorageInfo() {
        const current = localStorage.getItem(this.storageKey);
        const previous = localStorage.getItem(this.previousKey);
        const history = localStorage.getItem(this.historyKey);

        return {
            current: current ? Math.round(current.length / 1024) : 0,
            previous: previous ? Math.round(previous.length / 1024) : 0,
            history: history ? Math.round(history.length / 1024) : 0,
            total: Math.round((
                (current?.length || 0) +
                (previous?.length || 0) +
                (history?.length || 0)
            ) / 1024)
        };
    }
}

// Export for use in modules or make available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StateManager;
} else {
    window.StateManager = StateManager;
}
