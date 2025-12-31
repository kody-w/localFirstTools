/**
 * Sync Manager - Cross-tab synchronization
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StateManager } from '../core/state-manager.js';

class SyncManager {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {SyncManager}
     */
    static getInstance() {
        if (!SyncManager.#instance) {
            SyncManager.#instance = new SyncManager();
        }
        return SyncManager.#instance;
    }

    constructor() {
        if (SyncManager.#instance) {
            return SyncManager.#instance;
        }

        this.events = EventBus.getInstance();
        this.state = StateManager.getInstance();
        this.#channel = null;
        this.#tabId = this.#generateTabId();
        this.#isLeader = false;
        this.#syncKeys = new Set();
        this.#pendingSync = new Map();

        this.#initialize();
    }

    #channel;
    #tabId;
    #isLeader;
    #syncKeys;
    #pendingSync;

    /**
     * Initialize sync manager
     */
    #initialize() {
        // Setup BroadcastChannel if supported
        if (typeof BroadcastChannel !== 'undefined') {
            this.#channel = new BroadcastChannel('lft_v2_sync');
            this.#channel.onmessage = (e) => this.#handleMessage(e.data);
        }

        // Fallback to storage events
        window.addEventListener('storage', (e) => this.#handleStorageEvent(e));

        // Register default sync keys
        this.#registerDefaultSyncKeys();

        // Attempt leadership election
        this.#electLeader();

        // Announce presence
        this.#broadcast({ type: 'TAB_OPEN', tabId: this.#tabId });

        // Cleanup on unload
        window.addEventListener('beforeunload', () => {
            this.#broadcast({ type: 'TAB_CLOSE', tabId: this.#tabId });
        });
    }

    /**
     * Generate unique tab ID
     * @returns {string}
     */
    #generateTabId() {
        return `tab_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Register default sync keys
     */
    #registerDefaultSyncKeys() {
        this.registerSyncKey('pins');
        this.registerSyncKey('collections');
        this.registerSyncKey('theme');
        this.registerSyncKey('viewMode');
        this.registerSyncKey('votes');
    }

    /**
     * Register a key for synchronization
     * @param {string} key
     */
    registerSyncKey(key) {
        this.#syncKeys.add(key);
    }

    /**
     * Unregister a sync key
     * @param {string} key
     */
    unregisterSyncKey(key) {
        this.#syncKeys.delete(key);
    }

    /**
     * Broadcast a message to other tabs
     * @param {Object} message
     */
    #broadcast(message) {
        const payload = {
            ...message,
            senderId: this.#tabId,
            timestamp: Date.now()
        };

        if (this.#channel) {
            this.#channel.postMessage(payload);
        }

        // Also store for fallback
        try {
            localStorage.setItem('lft_v2_sync_message', JSON.stringify(payload));
            // Clear immediately (just for triggering storage event)
            setTimeout(() => {
                localStorage.removeItem('lft_v2_sync_message');
            }, 100);
        } catch {
            // Ignore storage errors
        }
    }

    /**
     * Handle incoming message
     * @param {Object} message
     */
    #handleMessage(message) {
        // Ignore own messages
        if (message.senderId === this.#tabId) return;

        switch (message.type) {
            case 'TAB_OPEN':
                this.#handleTabOpen(message);
                break;

            case 'TAB_CLOSE':
                this.#handleTabClose(message);
                break;

            case 'DATA_CHANGED':
                this.#handleDataChanged(message);
                break;

            case 'SYNC_REQUEST':
                this.#handleSyncRequest(message);
                break;

            case 'SYNC_RESPONSE':
                this.#handleSyncResponse(message);
                break;

            case 'LEADER_CLAIM':
                this.#handleLeaderClaim(message);
                break;
        }
    }

    /**
     * Handle storage event (fallback for browsers without BroadcastChannel)
     * @param {StorageEvent} e
     */
    #handleStorageEvent(e) {
        if (e.key === 'lft_v2_sync_message' && e.newValue) {
            try {
                const message = JSON.parse(e.newValue);
                this.#handleMessage(message);
            } catch {
                // Ignore invalid messages
            }
        }

        // Handle direct key changes
        if (e.key && e.key.startsWith('lft_v2_')) {
            const key = e.key.replace('lft_v2_', '');
            if (this.#syncKeys.has(key)) {
                this.#handleExternalChange(key, e.newValue);
            }
        }
    }

    /**
     * Handle tab open
     * @param {Object} message
     */
    #handleTabOpen(message) {
        // If we're leader, send current state
        if (this.#isLeader) {
            this.#sendSyncResponse(message.senderId);
        }
    }

    /**
     * Handle tab close
     * @param {Object} message
     */
    #handleTabClose(message) {
        // Re-elect leader if leader closed
        if (message.isLeader) {
            this.#electLeader();
        }
    }

    /**
     * Handle data change from another tab
     * @param {Object} message
     */
    #handleDataChanged(message) {
        const { key, value, version } = message;

        if (!this.#syncKeys.has(key)) return;

        // Apply change locally
        this.events.emit(EVENTS.SYNC_RECEIVED, { key, value, source: message.senderId });

        // Update state if needed
        this.state.set(`sync.${key}`, value);
    }

    /**
     * Handle external storage change
     * @param {string} key
     * @param {string} newValue
     */
    #handleExternalChange(key, newValue) {
        if (!this.#syncKeys.has(key)) return;

        try {
            const value = newValue ? JSON.parse(newValue) : null;
            this.events.emit(EVENTS.SYNC_RECEIVED, { key, value, source: 'storage' });
        } catch {
            // Ignore parse errors
        }
    }

    /**
     * Handle sync request
     * @param {Object} message
     */
    #handleSyncRequest(message) {
        if (this.#isLeader) {
            this.#sendSyncResponse(message.senderId);
        }
    }

    /**
     * Handle sync response
     * @param {Object} message
     */
    #handleSyncResponse(message) {
        if (message.targetId !== this.#tabId) return;

        const resolve = this.#pendingSync.get('initial');
        if (resolve) {
            resolve(message.data);
            this.#pendingSync.delete('initial');
        }
    }

    /**
     * Send sync response to requesting tab
     * @param {string} targetId
     */
    #sendSyncResponse(targetId) {
        const data = {};

        for (const key of this.#syncKeys) {
            try {
                const value = localStorage.getItem(`lft_v2_${key}`);
                if (value !== null) {
                    data[key] = JSON.parse(value);
                }
            } catch {
                // Skip invalid data
            }
        }

        this.#broadcast({
            type: 'SYNC_RESPONSE',
            targetId,
            data
        });
    }

    /**
     * Elect leader tab
     */
    #electLeader() {
        // Simple election: claim leadership with timestamp
        const claimTime = Date.now();

        this.#broadcast({
            type: 'LEADER_CLAIM',
            claimTime
        });

        // Wait for conflicts
        setTimeout(() => {
            // Check if we're still the earliest claimer
            const storedClaim = localStorage.getItem('lft_v2_leader_claim');
            if (!storedClaim || claimTime <= parseInt(storedClaim, 10)) {
                this.#isLeader = true;
                localStorage.setItem('lft_v2_leader_claim', claimTime.toString());
                localStorage.setItem('lft_v2_leader_tab', this.#tabId);
            }
        }, 100);
    }

    /**
     * Handle leader claim
     * @param {Object} message
     */
    #handleLeaderClaim(message) {
        const currentClaim = localStorage.getItem('lft_v2_leader_claim');

        if (!currentClaim || message.claimTime < parseInt(currentClaim, 10)) {
            // Another tab has earlier claim
            this.#isLeader = false;
        }
    }

    /**
     * Sync a key to other tabs
     * @param {string} key
     * @param {*} value
     */
    sync(key, value) {
        if (!this.#syncKeys.has(key)) return;

        this.#broadcast({
            type: 'DATA_CHANGED',
            key,
            value,
            version: Date.now()
        });
    }

    /**
     * Request initial sync from leader
     * @returns {Promise<Object>}
     */
    requestInitialSync() {
        return new Promise((resolve) => {
            this.#pendingSync.set('initial', resolve);

            this.#broadcast({
                type: 'SYNC_REQUEST'
            });

            // Timeout fallback
            setTimeout(() => {
                if (this.#pendingSync.has('initial')) {
                    this.#pendingSync.delete('initial');
                    resolve(null);
                }
            }, 1000);
        });
    }

    /**
     * Check if this tab is the leader
     * @returns {boolean}
     */
    isLeader() {
        return this.#isLeader;
    }

    /**
     * Get tab ID
     * @returns {string}
     */
    getTabId() {
        return this.#tabId;
    }

    /**
     * Force sync all keys
     */
    forceSync() {
        for (const key of this.#syncKeys) {
            try {
                const value = localStorage.getItem(`lft_v2_${key}`);
                if (value !== null) {
                    this.sync(key, JSON.parse(value));
                }
            } catch {
                // Skip invalid data
            }
        }
    }

    /**
     * Destroy sync manager
     */
    destroy() {
        if (this.#channel) {
            this.#channel.close();
        }
        this.#broadcast({ type: 'TAB_CLOSE', tabId: this.#tabId, isLeader: this.#isLeader });
    }
}

export { SyncManager };
