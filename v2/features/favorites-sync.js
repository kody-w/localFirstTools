/**
 * Favorites Sync - Export/import favorites and settings
 * Local First Tools v2
 */

import { EventBus, EVENTS } from '../core/event-bus.js';
import { StorageManager } from '../storage/storage-manager.js';
import { CollectionsManager } from './collections/collections-manager.js';

class FavoritesSync {
    static #instance = null;

    /**
     * Get singleton instance
     * @returns {FavoritesSync}
     */
    static getInstance() {
        if (!FavoritesSync.#instance) {
            FavoritesSync.#instance = new FavoritesSync();
        }
        return FavoritesSync.#instance;
    }

    constructor() {
        if (FavoritesSync.#instance) {
            return FavoritesSync.#instance;
        }

        this.events = EventBus.getInstance();
        this.storage = StorageManager.getInstance();
        this.collections = CollectionsManager.getInstance();
    }

    /**
     * Export all user data
     * @returns {Object}
     */
    exportAll() {
        return {
            version: 2,
            exportDate: new Date().toISOString(),
            data: {
                pinnedTools: this.storage.get('pinnedTools') || [],
                collections: this.collections.getAll(),
                votes: this.storage.get('votes') || {},
                theme: this.storage.get('theme') || 'dark',
                customTheme: this.storage.get('customTheme') || null,
                viewPreferences: this.storage.get('viewPreferences') || {},
                filterPresets: this.storage.get('filterPresets') || [],
                analytics: this.storage.get('analytics') || null
            }
        };
    }

    /**
     * Export only favorites (pins + collections)
     * @returns {Object}
     */
    exportFavorites() {
        return {
            version: 2,
            exportDate: new Date().toISOString(),
            type: 'favorites',
            data: {
                pinnedTools: this.storage.get('pinnedTools') || [],
                collections: this.collections.getAll()
            }
        };
    }

    /**
     * Export as JSON file
     * @param {string} type - 'all' or 'favorites'
     */
    downloadExport(type = 'all') {
        const data = type === 'all' ? this.exportAll() : this.exportFavorites();
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const filename = type === 'all'
            ? `localfirst-backup-${this.#formatDate()}.json`
            : `localfirst-favorites-${this.#formatDate()}.json`;

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();

        URL.revokeObjectURL(url);

        this.events.emit(EVENTS.NOTIFICATION, {
            message: `${type === 'all' ? 'Backup' : 'Favorites'} exported successfully`,
            type: 'success'
        });

        this.events.emit(EVENTS.DATA_EXPORTED, { type });
    }

    /**
     * Import data from JSON
     * @param {string} json
     * @param {Object} options
     * @returns {Object} - Import result
     */
    importData(json, options = {}) {
        try {
            const data = JSON.parse(json);

            // Validate structure
            if (!data.version || !data.data) {
                throw new Error('Invalid backup format');
            }

            const result = {
                imported: [],
                skipped: [],
                errors: []
            };

            const importData = data.data;
            const merge = options.merge !== false; // Default to merge

            // Import pinned tools
            if (importData.pinnedTools) {
                const existing = this.storage.get('pinnedTools') || [];
                const toImport = merge
                    ? [...new Set([...existing, ...importData.pinnedTools])]
                    : importData.pinnedTools;

                this.storage.set('pinnedTools', toImport);
                result.imported.push(`${importData.pinnedTools.length} pinned tools`);
            }

            // Import collections
            if (importData.collections && Array.isArray(importData.collections)) {
                const collectionsJson = JSON.stringify(importData.collections);
                const count = this.collections.importCollections(collectionsJson);
                result.imported.push(`${count} collections`);
            }

            // Import votes
            if (importData.votes) {
                const existing = this.storage.get('votes') || {};
                const merged = merge ? { ...existing, ...importData.votes } : importData.votes;
                this.storage.set('votes', merged);
                result.imported.push('votes');
            }

            // Import theme (only if specified)
            if (options.includeTheme && importData.theme) {
                this.storage.set('theme', importData.theme);
                if (importData.customTheme) {
                    this.storage.set('customTheme', importData.customTheme);
                }
                result.imported.push('theme settings');
            }

            // Import view preferences
            if (options.includePreferences && importData.viewPreferences) {
                this.storage.set('viewPreferences', importData.viewPreferences);
                result.imported.push('view preferences');
            }

            // Import filter presets
            if (importData.filterPresets) {
                const existing = this.storage.get('filterPresets') || [];
                const merged = merge ? [...existing, ...importData.filterPresets] : importData.filterPresets;
                // Remove duplicates by name
                const unique = merged.filter((preset, index, self) =>
                    index === self.findIndex(p => p.name === preset.name)
                );
                this.storage.set('filterPresets', unique);
                result.imported.push('filter presets');
            }

            this.events.emit(EVENTS.DATA_IMPORTED, result);
            this.events.emit(EVENTS.NOTIFICATION, {
                message: `Import complete: ${result.imported.join(', ')}`,
                type: 'success'
            });

            return result;

        } catch (e) {
            console.error('Import failed:', e);
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Import failed: Invalid file format',
                type: 'error'
            });
            throw e;
        }
    }

    /**
     * Import from file input
     * @param {Object} options
     * @returns {Promise<Object>}
     */
    importFromFile(options = {}) {
        return new Promise((resolve, reject) => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';

            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (!file) {
                    reject(new Error('No file selected'));
                    return;
                }

                try {
                    const text = await file.text();
                    const result = this.importData(text, options);
                    resolve(result);
                } catch (err) {
                    reject(err);
                }
            };

            input.click();
        });
    }

    /**
     * Sync to cloud storage (placeholder for future implementation)
     * @param {string} provider - 'google', 'dropbox', etc.
     * @returns {Promise<void>}
     */
    async syncToCloud(provider) {
        // Placeholder for cloud sync functionality
        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'Cloud sync coming soon!',
            type: 'info'
        });
    }

    /**
     * Generate shareable link with encoded favorites
     * @returns {string}
     */
    generateShareLink() {
        const favorites = {
            pins: this.storage.get('pinnedTools') || []
        };

        // Encode as base64
        const encoded = btoa(JSON.stringify(favorites));

        const url = new URL(window.location.origin + window.location.pathname);
        url.searchParams.set('import', encoded);

        return url.toString();
    }

    /**
     * Import from URL parameter
     * @returns {boolean} - Whether import was performed
     */
    importFromUrl() {
        const params = new URLSearchParams(window.location.search);
        const encoded = params.get('import');

        if (!encoded) return false;

        try {
            const decoded = JSON.parse(atob(encoded));

            if (decoded.pins && Array.isArray(decoded.pins)) {
                const existing = this.storage.get('pinnedTools') || [];
                const merged = [...new Set([...existing, ...decoded.pins])];
                this.storage.set('pinnedTools', merged);

                this.events.emit(EVENTS.NOTIFICATION, {
                    message: `Imported ${decoded.pins.length} favorites`,
                    type: 'success'
                });

                // Clean URL
                window.history.replaceState({}, '', window.location.pathname);

                return true;
            }
        } catch (e) {
            console.error('Failed to import from URL:', e);
        }

        return false;
    }

    /**
     * Reset all user data
     * @param {boolean} confirm
     */
    resetAllData(confirm = false) {
        if (!confirm) {
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Reset cancelled - confirmation required',
                type: 'warning'
            });
            return;
        }

        // Create backup first
        const backup = this.exportAll();
        console.log('Created backup before reset:', backup);

        // Clear storage
        this.storage.clear();

        // Reset collections
        this.collections.clearAll();

        this.events.emit(EVENTS.DATA_RESET);
        this.events.emit(EVENTS.NOTIFICATION, {
            message: 'All data has been reset',
            type: 'info'
        });
    }

    /**
     * Get sync status summary
     * @returns {Object}
     */
    getStatus() {
        const pinnedTools = this.storage.get('pinnedTools') || [];
        const collections = this.collections.getAll();
        const votes = this.storage.get('votes') || {};

        return {
            pinnedCount: pinnedTools.length,
            collectionsCount: collections.length,
            votesCount: Object.keys(votes).length,
            lastExport: this.storage.get('lastExport') || null,
            lastImport: this.storage.get('lastImport') || null
        };
    }

    /**
     * Format date for filename
     * @returns {string}
     */
    #formatDate() {
        return new Date().toISOString().split('T')[0];
    }

    /**
     * Show sync panel UI
     * @param {HTMLElement} parentContainer
     */
    showSyncPanel(parentContainer) {
        const status = this.getStatus();

        const panel = document.createElement('div');
        panel.className = 'sync-panel';
        panel.innerHTML = `
            <div class="sync-backdrop"></div>
            <div class="sync-content">
                <div class="sync-header">
                    <h3>Backup & Sync</h3>
                    <button class="btn btn-icon sync-close">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 6L6 18M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <div class="sync-body">
                    <div class="sync-status">
                        <div class="status-item">
                            <span class="status-label">Pinned Tools</span>
                            <span class="status-value">${status.pinnedCount}</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Collections</span>
                            <span class="status-value">${status.collectionsCount}</span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Votes</span>
                            <span class="status-value">${status.votesCount}</span>
                        </div>
                    </div>

                    <div class="sync-actions">
                        <button class="btn btn-primary btn-block" id="export-all">
                            Export Full Backup
                        </button>
                        <button class="btn btn-secondary btn-block" id="export-favorites">
                            Export Favorites Only
                        </button>
                        <button class="btn btn-secondary btn-block" id="import-data">
                            Import Backup
                        </button>
                        <button class="btn btn-ghost btn-block" id="share-link">
                            Generate Share Link
                        </button>
                    </div>

                    <div class="sync-danger">
                        <button class="btn btn-ghost text-error btn-sm" id="reset-data">
                            Reset All Data
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.#injectSyncStyles();
        parentContainer.appendChild(panel);

        // Animate in
        requestAnimationFrame(() => panel.classList.add('visible'));

        // Bind events
        const close = () => {
            panel.classList.remove('visible');
            setTimeout(() => panel.remove(), 300);
        };

        panel.querySelector('.sync-backdrop')?.addEventListener('click', close);
        panel.querySelector('.sync-close')?.addEventListener('click', close);

        panel.querySelector('#export-all')?.addEventListener('click', () => {
            this.downloadExport('all');
        });

        panel.querySelector('#export-favorites')?.addEventListener('click', () => {
            this.downloadExport('favorites');
        });

        panel.querySelector('#import-data')?.addEventListener('click', async () => {
            try {
                await this.importFromFile();
                close();
            } catch (e) {
                // Error handled in importFromFile
            }
        });

        panel.querySelector('#share-link')?.addEventListener('click', () => {
            const link = this.generateShareLink();
            navigator.clipboard.writeText(link);
            this.events.emit(EVENTS.NOTIFICATION, {
                message: 'Share link copied to clipboard!',
                type: 'success'
            });
        });

        panel.querySelector('#reset-data')?.addEventListener('click', () => {
            if (confirm('Are you sure you want to reset all data? This cannot be undone.')) {
                this.resetAllData(true);
                close();
            }
        });
    }

    /**
     * Inject sync panel styles
     */
    #injectSyncStyles() {
        if (document.getElementById('sync-panel-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'sync-panel-styles';
        styles.textContent = `
            .sync-panel {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1000;
                opacity: 0;
                transition: opacity var(--duration-300);
            }

            .sync-panel.visible {
                opacity: 1;
            }

            .sync-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
            }

            .sync-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 90%;
                max-width: 400px;
                background: var(--color-bg-elevated);
                border-radius: var(--radius-xl);
                overflow: hidden;
            }

            .sync-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-4);
                border-bottom: 1px solid var(--color-border);
            }

            .sync-header h3 {
                margin: 0;
            }

            .sync-body {
                padding: var(--space-4);
            }

            .sync-status {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: var(--space-3);
                margin-bottom: var(--space-4);
                padding: var(--space-3);
                background: var(--color-bg-secondary);
                border-radius: var(--radius-lg);
            }

            .status-item {
                text-align: center;
            }

            .status-value {
                display: block;
                font-size: var(--text-xl);
                font-weight: 700;
                color: var(--color-accent);
            }

            .status-label {
                font-size: var(--text-xs);
                color: var(--color-text-tertiary);
            }

            .sync-actions {
                display: flex;
                flex-direction: column;
                gap: var(--space-2);
            }

            .sync-danger {
                margin-top: var(--space-4);
                padding-top: var(--space-4);
                border-top: 1px solid var(--color-border);
                text-align: center;
            }

            .text-error {
                color: var(--color-error);
            }
        `;

        document.head.appendChild(styles);
    }
}

export { FavoritesSync };
