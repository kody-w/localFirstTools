# Local-First HTML Application Bootstrap Guide with GitHub Data

## 🎯 Overview

This guide provides a complete template for creating self-contained, offline-first HTML applications that leverage public GitHub repositories as a universal data source while avoiding API rate limits. Applications feature local data persistence with JSON import/export capabilities and can sync with GitHub-hosted content.

## 🏗️ Core Architecture Principles

### Design Philosophy
- **Single File Distribution**: Everything in one HTML file
- **Zero Dependencies**: No external libraries, CDNs, or build tools required
- **GitHub as CDN**: Use raw GitHub URLs to avoid API rate limits
- **Local-First with Cloud Sync**: Store data locally, sync with GitHub when needed
- **Offline-First**: Full functionality without internet after initial data load
- **Progressive Enhancement**: Cache GitHub data locally for offline use

### Technical Stack
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables and animations
- **Vanilla JavaScript**: No frameworks required
- **LocalStorage API**: Persistent data storage and caching
- **File API**: Import/export functionality
- **Raw GitHub URLs**: Direct file access without API limits
- **Service Worker (Optional)**: Advanced offline caching

## 📝 Complete Application Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>My Local-First App</title>
    <style>
        /* ============================================
           CSS VARIABLES & THEME
           ============================================ */
        :root {
            /* Color Palette */
            --primary-color: #0078d4;
            --secondary-color: #06ffa5;
            --accent-color: #ff006e;
            --bg-primary: #0a0a0a;
            --bg-secondary: rgba(255, 255, 255, 0.05);
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
            
            /* Spacing */
            --spacing-xs: 4px;
            --spacing-sm: 8px;
            --spacing-md: 16px;
            --spacing-lg: 24px;
            --spacing-xl: 32px;
            
            /* Transitions */
            --transition-fast: 0.2s ease;
            --transition-normal: 0.3s ease;
        }

        /* ============================================
           RESET & BASE STYLES
           ============================================ */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* ============================================
           LAYOUT COMPONENTS
           ============================================ */
        .app-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--spacing-lg);
        }

        .app-header {
            text-align: center;
            padding: var(--spacing-xl);
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            border-radius: 12px;
            margin-bottom: var(--spacing-xl);
        }

        .app-title {
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: var(--spacing-sm);
        }

        /* ============================================
           DATA SYNC STATUS
           ============================================ */
        .sync-status {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-secondary);
            padding: 10px 20px;
            border-radius: 25px;
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1000;
        }

        .sync-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4caf50;
        }

        .sync-indicator.syncing {
            background: #ff9800;
            animation: pulse 1s infinite;
        }

        .sync-indicator.offline {
            background: #666;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* ============================================
           BUTTONS & CONTROLS
           ============================================ */
        .btn {
            padding: 12px 24px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: var(--transition-normal);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 120, 212, 0.3);
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn-secondary {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
        }

        /* ============================================
           DATA GRID
           ============================================ */
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: var(--spacing-lg);
            margin-top: var(--spacing-xl);
        }

        .data-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: var(--spacing-lg);
            transition: var(--transition-normal);
            cursor: pointer;
        }

        .data-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary-color);
            box-shadow: 0 10px 30px rgba(0, 120, 212, 0.2);
        }

        /* ============================================
           LOADING & ERROR STATES
           ============================================ */
        .loading {
            text-align: center;
            padding: 60px;
            color: var(--text-secondary);
        }

        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid var(--border-color);
            border-top-color: var(--primary-color);
            border-radius: 50%;
            margin: 0 auto 20px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .error {
            background: rgba(255, 0, 110, 0.1);
            border: 1px solid var(--accent-color);
            color: var(--accent-color);
            padding: var(--spacing-lg);
            border-radius: 8px;
            margin: var(--spacing-lg) 0;
        }

        /* ============================================
           TOAST NOTIFICATIONS
           ============================================ */
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #333;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            opacity: 0;
            transition: var(--transition-normal);
            z-index: 2000;
        }

        .toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }

        .toast.success { background: #4caf50; }
        .toast.error { background: #f44336; }
        .toast.info { background: var(--primary-color); }
    </style>
</head>
<body>
    <!-- App Container -->
    <div class="app-container">
        <!-- Sync Status Indicator -->
        <div class="sync-status">
            <div class="sync-indicator" id="syncIndicator"></div>
            <span id="syncStatus">Connected</span>
        </div>

        <!-- Header -->
        <header class="app-header">
            <h1 class="app-title">My Local-First Application</h1>
            <p>Powered by GitHub Data • Works Offline</p>
        </header>

        <!-- Control Panel -->
        <div class="control-panel">
            <button class="btn" onclick="app.syncWithGitHub()">
                <span>🔄</span> Sync with GitHub
            </button>
            <button class="btn btn-secondary" onclick="app.exportData()">
                <span>💾</span> Export Data
            </button>
            <button class="btn btn-secondary" onclick="app.importData()">
                <span>📁</span> Import Data
            </button>
            <input type="file" id="importFile" style="display: none;" accept=".json" />
        </div>

        <!-- Main Content -->
        <main id="mainContent">
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Loading application data...</p>
            </div>
        </main>

        <!-- Data Grid (populated dynamically) -->
        <div class="data-grid" id="dataGrid"></div>
    </div>

    <!-- Toast Notification -->
    <div class="toast" id="toast"></div>

    <script>
        // ============================================
        // APPLICATION CONFIGURATION
        // ============================================
        const CONFIG = {
            // GitHub Repository Configuration
            GITHUB: {
                OWNER: 'your-github-username',
                REPO: 'your-repo-name',
                BRANCH: 'main',
                // Use raw URLs to avoid API rate limits
                RAW_BASE: 'https://raw.githubusercontent.com',
                // Optional: GitHub Pages URL if you're using it
                PAGES_BASE: null // e.g., 'https://username.github.io/repo/'
            },
            
            // Local Storage Keys
            STORAGE: {
                DATA: 'app_data',
                CACHE: 'github_cache',
                LAST_SYNC: 'last_sync',
                USER_DATA: 'user_data',
                SETTINGS: 'app_settings'
            },
            
            // Cache Configuration
            CACHE: {
                TTL: 3600000, // 1 hour in milliseconds
                VERSION: '1.0.0'
            },
            
            // Application Settings
            APP: {
                NAME: 'My Local-First App',
                VERSION: '1.0.0',
                DEBUG: true
            }
        };

        // ============================================
        // GITHUB DATA MANAGER
        // ============================================
        class GitHubDataManager {
            constructor() {
                this.cache = new Map();
                this.lastSync = null;
            }

            /**
             * Build raw GitHub URL (no API, no rate limits!)
             */
            getRawUrl(path) {
                const { OWNER, REPO, BRANCH, RAW_BASE } = CONFIG.GITHUB;
                return `${RAW_BASE}/${OWNER}/${REPO}/${BRANCH}/${path}`;
            }

            /**
             * Fetch file from GitHub using raw URL
             */
            async fetchFile(path, options = {}) {
                const url = this.getRawUrl(path);
                
                try {
                    const response = await fetch(url, {
                        ...options,
                        // Add cache headers for better performance
                        headers: {
                            'Cache-Control': 'max-age=3600',
                            ...options.headers
                        }
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Failed to fetch ${path}: ${response.status}`);
                    }
                    
                    const contentType = response.headers.get('content-type');
                    
                    // Auto-detect content type
                    if (path.endsWith('.json') || contentType?.includes('json')) {
                        return await response.json();
                    } else if (path.endsWith('.md') || path.endsWith('.txt')) {
                        return await response.text();
                    } else {
                        return await response.blob();
                    }
                } catch (error) {
                    console.error(`Error fetching ${path}:`, error);
                    
                    // Try to return cached version if available
                    const cached = this.getCached(path);
                    if (cached) {
                        console.log(`Using cached version of ${path}`);
                        return cached;
                    }
                    
                    throw error;
                }
            }

            /**
             * Fetch manifest or index file
             */
            async fetchManifest() {
                try {
                    // Try multiple possible manifest locations
                    const possiblePaths = [
                        'manifest.json',
                        'data/manifest.json',
                        'index.json',
                        'data/index.json'
                    ];
                    
                    for (const path of possiblePaths) {
                        try {
                            const manifest = await this.fetchFile(path);
                            this.cacheData(path, manifest);
                            return manifest;
                        } catch (error) {
                            // Continue to next path
                            if (CONFIG.APP.DEBUG) {
                                console.log(`Manifest not found at ${path}, trying next...`);
                            }
                        }
                    }
                    
                    // If no manifest found, return default structure
                    return this.getDefaultManifest();
                } catch (error) {
                    console.error('Error fetching manifest:', error);
                    return this.getDefaultManifest();
                }
            }

            /**
             * Cache data locally
             */
            cacheData(key, data) {
                const cacheEntry = {
                    data: data,
                    timestamp: Date.now(),
                    version: CONFIG.CACHE.VERSION
                };
                
                this.cache.set(key, cacheEntry);
                
                // Also save to localStorage
                try {
                    const allCache = this.loadCache();
                    allCache[key] = cacheEntry;
                    localStorage.setItem(CONFIG.STORAGE.CACHE, JSON.stringify(allCache));
                } catch (error) {
                    console.error('Error saving to cache:', error);
                }
            }

            /**
             * Get cached data
             */
            getCached(key) {
                // Check memory cache first
                if (this.cache.has(key)) {
                    const entry = this.cache.get(key);
                    if (this.isCacheValid(entry)) {
                        return entry.data;
                    }
                }
                
                // Check localStorage cache
                const allCache = this.loadCache();
                if (allCache[key] && this.isCacheValid(allCache[key])) {
                    this.cache.set(key, allCache[key]);
                    return allCache[key].data;
                }
                
                return null;
            }

            /**
             * Check if cache entry is still valid
             */
            isCacheValid(entry) {
                if (!entry) return false;
                
                const age = Date.now() - entry.timestamp;
                return age < CONFIG.CACHE.TTL && entry.version === CONFIG.CACHE.VERSION;
            }

            /**
             * Load cache from localStorage
             */
            loadCache() {
                try {
                    const cached = localStorage.getItem(CONFIG.STORAGE.CACHE);
                    return cached ? JSON.parse(cached) : {};
                } catch (error) {
                    console.error('Error loading cache:', error);
                    return {};
                }
            }

            /**
             * Clear all cached data
             */
            clearCache() {
                this.cache.clear();
                localStorage.removeItem(CONFIG.STORAGE.CACHE);
            }

            /**
             * Get default manifest structure
             */
            getDefaultManifest() {
                return {
                    version: '1.0.0',
                    generated: new Date().toISOString(),
                    items: [],
                    categories: [],
                    metadata: {
                        title: CONFIG.APP.NAME,
                        description: 'Local-first application with GitHub sync'
                    }
                };
            }
        }

        // ============================================
        // LOCAL DATA MANAGER
        // ============================================
        class LocalDataManager {
            constructor() {
                this.data = this.loadData();
                this.userData = this.loadUserData();
            }

            /**
             * Load application data from localStorage
             */
            loadData() {
                try {
                    const stored = localStorage.getItem(CONFIG.STORAGE.DATA);
                    return stored ? JSON.parse(stored) : {};
                } catch (error) {
                    console.error('Error loading data:', error);
                    return {};
                }
            }

            /**
             * Save application data to localStorage
             */
            saveData(data) {
                try {
                    this.data = { ...this.data, ...data };
                    localStorage.setItem(CONFIG.STORAGE.DATA, JSON.stringify(this.data));
                    return true;
                } catch (error) {
                    console.error('Error saving data:', error);
                    return false;
                }
            }

            /**
             * Load user-specific data
             */
            loadUserData() {
                try {
                    const stored = localStorage.getItem(CONFIG.STORAGE.USER_DATA);
                    return stored ? JSON.parse(stored) : {
                        favorites: [],
                        history: [],
                        settings: {}
                    };
                } catch (error) {
                    console.error('Error loading user data:', error);
                    return { favorites: [], history: [], settings: {} };
                }
            }

            /**
             * Save user-specific data
             */
            saveUserData(data) {
                try {
                    this.userData = { ...this.userData, ...data };
                    localStorage.setItem(CONFIG.STORAGE.USER_DATA, JSON.stringify(this.userData));
                    return true;
                } catch (error) {
                    console.error('Error saving user data:', error);
                    return false;
                }
            }

            /**
             * Export all data as JSON
             */
            exportData() {
                const exportData = {
                    version: CONFIG.APP.VERSION,
                    exported: new Date().toISOString(),
                    app_data: this.data,
                    user_data: this.userData,
                    cached_data: this.getCachedData()
                };
                
                return JSON.stringify(exportData, null, 2);
            }

            /**
             * Import data from JSON
             */
            importData(jsonString) {
                try {
                    const imported = JSON.parse(jsonString);
                    
                    // Validate import structure
                    if (!imported.version || !imported.app_data) {
                        throw new Error('Invalid import file structure');
                    }
                    
                    // Import app data
                    if (imported.app_data) {
                        this.saveData(imported.app_data);
                    }
                    
                    // Import user data
                    if (imported.user_data) {
                        this.saveUserData(imported.user_data);
                    }
                    
                    // Import cached data if present
                    if (imported.cached_data) {
                        localStorage.setItem(CONFIG.STORAGE.CACHE, JSON.stringify(imported.cached_data));
                    }
                    
                    return true;
                } catch (error) {
                    console.error('Error importing data:', error);
                    return false;
                }
            }

            /**
             * Get cached GitHub data
             */
            getCachedData() {
                try {
                    const cached = localStorage.getItem(CONFIG.STORAGE.CACHE);
                    return cached ? JSON.parse(cached) : {};
                } catch (error) {
                    return {};
                }
            }

            /**
             * Clear all local data
             */
            clearAllData() {
                const keys = Object.values(CONFIG.STORAGE);
                keys.forEach(key => localStorage.removeItem(key));
                this.data = {};
                this.userData = { favorites: [], history: [], settings: {} };
            }
        }

        // ============================================
        // UI MANAGER
        // ============================================
        class UIManager {
            constructor() {
                this.elements = {
                    mainContent: document.getElementById('mainContent'),
                    dataGrid: document.getElementById('dataGrid'),
                    syncIndicator: document.getElementById('syncIndicator'),
                    syncStatus: document.getElementById('syncStatus'),
                    toast: document.getElementById('toast')
                };
            }

            /**
             * Show loading state
             */
            showLoading(message = 'Loading...') {
                this.elements.mainContent.innerHTML = `
                    <div class="loading">
                        <div class="loading-spinner"></div>
                        <p>${message}</p>
                    </div>
                `;
            }

            /**
             * Show error state
             */
            showError(message, details = '') {
                this.elements.mainContent.innerHTML = `
                    <div class="error">
                        <h3>⚠️ ${message}</h3>
                        ${details ? `<p>${details}</p>` : ''}
                        <button class="btn" onclick="app.retry()">Retry</button>
                    </div>
                `;
            }

            /**
             * Update sync status indicator
             */
            updateSyncStatus(status) {
                const indicator = this.elements.syncIndicator;
                const statusText = this.elements.syncStatus;
                
                switch(status) {
                    case 'syncing':
                        indicator.className = 'sync-indicator syncing';
                        statusText.textContent = 'Syncing...';
                        break;
                    case 'online':
                        indicator.className = 'sync-indicator';
                        statusText.textContent = 'Connected';
                        break;
                    case 'offline':
                        indicator.className = 'sync-indicator offline';
                        statusText.textContent = 'Offline';
                        break;
                    case 'error':
                        indicator.className = 'sync-indicator offline';
                        statusText.textContent = 'Sync Error';
                        break;
                }
            }

            /**
             * Render data grid
             */
            renderDataGrid(items) {
                if (!items || items.length === 0) {
                    this.elements.dataGrid.innerHTML = `
                        <div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">
                            No items to display
                        </div>
                    `;
                    return;
                }
                
                this.elements.dataGrid.innerHTML = items.map(item => `
                    <div class="data-card" onclick="app.selectItem('${item.id}')">
                        <h3>${item.title || item.name}</h3>
                        <p>${item.description || ''}</p>
                        ${item.metadata ? `
                            <div style="margin-top: 10px; font-size: 0.9em; color: var(--text-secondary);">
                                ${Object.entries(item.metadata).map(([key, value]) => 
                                    `<div>${key}: ${value}</div>`
                                ).join('')}
                            </div>
                        ` : ''}
                    </div>
                `).join('');
            }

            /**
             * Show toast notification
             */
            showToast(message, type = 'info', duration = 3000) {
                const toast = this.elements.toast;
                toast.textContent = message;
                toast.className = `toast show ${type}`;
                
                setTimeout(() => {
                    toast.classList.remove('show');
                }, duration);
            }

            /**
             * Clear content
             */
            clearContent() {
                this.elements.mainContent.innerHTML = '';
                this.elements.dataGrid.innerHTML = '';
            }
        }

        // ============================================
        // MAIN APPLICATION
        // ============================================
        class LocalFirstApp {
            constructor() {
                this.github = new GitHubDataManager();
                this.local = new LocalDataManager();
                this.ui = new UIManager();
                this.isOnline = navigator.onLine;
                this.manifest = null;
                this.items = [];
                
                this.initialize();
            }

            /**
             * Initialize application
             */
            async initialize() {
                // Set up event listeners
                this.setupEventListeners();
                
                // Check online status
                this.updateOnlineStatus();
                
                // Load data
                await this.loadData();
                
                // Set up periodic sync if online
                if (this.isOnline) {
                    this.setupPeriodicSync();
                }
            }

            /**
             * Set up event listeners
             */
            setupEventListeners() {
                // Online/offline detection
                window.addEventListener('online', () => this.handleOnline());
                window.addEventListener('offline', () => this.handleOffline());
                
                // File import
                const importFile = document.getElementById('importFile');
                if (importFile) {
                    importFile.addEventListener('change', (e) => this.handleFileImport(e));
                }
                
                // Visibility change (tab focus)
                document.addEventListener('visibilitychange', () => {
                    if (!document.hidden && this.isOnline) {
                        this.checkForUpdates();
                    }
                });
            }

            /**
             * Load application data
             */
            async loadData() {
                this.ui.showLoading('Loading application data...');
                
                try {
                    // Try to load from cache first
                    const cachedManifest = this.github.getCached('manifest');
                    if (cachedManifest) {
                        this.manifest = cachedManifest;
                        this.items = cachedManifest.items || [];
                        this.renderContent();
                    }
                    
                    // If online, sync with GitHub
                    if (this.isOnline) {
                        await this.syncWithGitHub();
                    } else if (!cachedManifest) {
                        // No cache and offline
                        this.ui.showError(
                            'No cached data available',
                            'Please connect to the internet to load initial data.'
                        );
                    }
                } catch (error) {
                    console.error('Error loading data:', error);
                    this.ui.showError('Failed to load data', error.message);
                }
            }

            /**
             * Sync with GitHub
             */
            async syncWithGitHub() {
                if (!this.isOnline) {
                    this.ui.showToast('Cannot sync while offline', 'error');
                    return;
                }
                
                this.ui.updateSyncStatus('syncing');
                this.ui.showToast('Syncing with GitHub...', 'info');
                
                try {
                    // Fetch manifest
                    this.manifest = await this.github.fetchManifest();
                    
                    // Load additional data files if specified in manifest
                    if (this.manifest.dataFiles) {
                        for (const file of this.manifest.dataFiles) {
                            try {
                                const data = await this.github.fetchFile(file.path);
                                this.github.cacheData(file.path, data);
                                
                                // Process based on file type
                                if (file.type === 'items') {
                                    this.items = [...this.items, ...data];
                                }
                            } catch (error) {
                                console.error(`Error loading ${file.path}:`, error);
                            }
                        }
                    }
                    
                    // Update last sync time
                    localStorage.setItem(CONFIG.STORAGE.LAST_SYNC, new Date().toISOString());
                    
                    // Save to local storage
                    this.local.saveData({
                        manifest: this.manifest,
                        items: this.items,
                        lastSync: new Date().toISOString()
                    });
                    
                    // Update UI
                    this.renderContent();
                    this.ui.updateSyncStatus('online');
                    this.ui.showToast('Sync complete!', 'success');
                    
                } catch (error) {
                    console.error('Sync error:', error);
                    this.ui.updateSyncStatus('error');
                    this.ui.showToast('Sync failed', 'error');
                }
            }

            /**
             * Render main content
             */
            renderContent() {
                this.ui.clearContent();
                
                // Render main content area
                const mainContent = this.elements.mainContent;
                if (this.manifest) {
                    mainContent.innerHTML = `
                        <h2>${this.manifest.metadata?.title || 'Application Data'}</h2>
                        <p>${this.manifest.metadata?.description || ''}</p>
                        <div style="margin-top: 20px;">
                            <small>Version: ${this.manifest.version} | Items: ${this.items.length}</small>
                        </div>
                    `;
                }
                
                // Render data grid
                this.ui.renderDataGrid(this.items);
            }

            /**
             * Select an item
             */
            selectItem(id) {
                const item = this.items.find(i => i.id === id);
                if (item) {
                    // Add to history
                    const history = this.local.userData.history || [];
                    history.unshift({ id, timestamp: Date.now() });
                    this.local.saveUserData({ history: history.slice(0, 50) }); // Keep last 50
                    
                    // Show item details (customize as needed)
                    this.showItemDetails(item);
                }
            }

            /**
             * Show item details
             */
            showItemDetails(item) {
                // This is where you'd show a modal or navigate to a detail view
                console.log('Selected item:', item);
                this.ui.showToast(`Selected: ${item.title || item.name}`, 'info');
            }

            /**
             * Export application data
             */
            exportData() {
                const dataStr = this.local.exportData();
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = URL.createObjectURL(dataBlob);
                
                const link = document.createElement('a');
                link.href = url;
                link.download = `${CONFIG.APP.NAME.replace(/\s+/g, '_')}_backup_${Date.now()}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                this.ui.showToast('Data exported successfully', 'success');
            }

            /**
             * Import application data
             */
            importData() {
                document.getElementById('importFile').click();
            }

            /**
             * Handle file import
             */
            async handleFileImport(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                try {
                    const text = await file.text();
                    const success = this.local.importData(text);
                    
                    if (success) {
                        // Reload data from localStorage
                        this.local.data = this.local.loadData();
                        this.local.userData = this.local.loadUserData();
                        
                        // Re-render
                        this.renderContent();
                        this.ui.showToast('Data imported successfully', 'success');
                    } else {
                        this.ui.showToast('Import failed - invalid file format', 'error');
                    }
                } catch (error) {
                    console.error('Import error:', error);
                    this.ui.showToast('Import failed', 'error');
                }
                
                // Clear the input
                event.target.value = '';
            }

            /**
             * Update online status
             */
            updateOnlineStatus() {
                this.isOnline = navigator.onLine;
                this.ui.updateSyncStatus(this.isOnline ? 'online' : 'offline');
            }

            /**
             * Handle coming online
             */
            handleOnline() {
                this.updateOnlineStatus();
                this.ui.showToast('Connection restored', 'success');
                this.syncWithGitHub();
            }

            /**
             * Handle going offline
             */
            handleOffline() {
                this.updateOnlineStatus();
                this.ui.showToast('Working offline', 'info');
            }

            /**
             * Check for updates
             */
            async checkForUpdates() {
                const lastSync = localStorage.getItem(CONFIG.STORAGE.LAST_SYNC);
                if (lastSync) {
                    const timeSinceSync = Date.now() - new Date(lastSync).getTime();
                    // Only auto-sync if more than 5 minutes have passed
                    if (timeSinceSync > 300000) {
                        await this.syncWithGitHub();
                    }
                }
            }

            /**
             * Set up periodic sync
             */
            setupPeriodicSync() {
                // Sync every 30 minutes if online
                setInterval(() => {
                    if (this.isOnline) {
                        this.syncWithGitHub();
                    }
                }, 1800000);
            }

            /**
             * Retry loading
             */
            retry() {
                this.loadData();
            }
        }

        // ============================================
        // INITIALIZE APPLICATION
        // ============================================
        let app;

        document.addEventListener('DOMContentLoaded', () => {
            app = new LocalFirstApp();
            
            // Make app globally accessible for debugging
            if (CONFIG.APP.DEBUG) {
                window.app = app;
            }
        });

        // ============================================
        // SERVICE WORKER (Optional - for advanced offline)
        // ============================================
        if ('serviceWorker' in navigator) {
            // Uncomment to enable service worker
            // navigator.serviceWorker.register('/sw.js');
        }
    </script>
</body>
</html>
```

## 📁 GitHub Repository Structure

Set up your GitHub repository with this structure:

```
your-repo/
├── manifest.json           # Main application manifest
├── data/
│   ├── items.json         # Application data
│   ├── categories.json    # Category definitions
│   └── config.json        # App configuration
├── assets/
│   ├── icons/            # Icon files
│   └── images/           # Image assets
├── README.md             # Repository documentation
└── index.html            # Your application file
```

### Example manifest.json

```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:00:00Z",
  "metadata": {
    "title": "My Application",
    "description": "A local-first application with GitHub sync",
    "author": "Your Name",
    "license": "MIT"
  },
  "dataFiles": [
    {
      "path": "data/items.json",
      "type": "items",
      "description": "Main item database"
    },
    {
      "path": "data/categories.json",
      "type": "categories",
      "description": "Category definitions"
    }
  ],
  "assets": {
    "icons": "assets/icons/",
    "images": "assets/images/"
  },
  "config": {
    "syncInterval": 1800000,
    "cacheTimeout": 3600000,
    "maxItems": 1000
  }
}
```

## 🚀 Key Features & Implementation

### 1. Raw GitHub URLs (No API Limits!)

```javascript
// Always use raw.githubusercontent.com
const rawUrl = `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${path}`;

// This bypasses API rate limits completely!
fetch(rawUrl)
  .then(response => response.json())
  .then(data => console.log(data));
```

### 2. Intelligent Caching

```javascript
class CacheManager {
    constructor(ttl = 3600000) { // 1 hour default
        this.ttl = ttl;
    }
    
    set(key, data) {
        const entry = {
            data,
            timestamp: Date.now(),
            expires: Date.now() + this.ttl
        };
        localStorage.setItem(`cache_${key}`, JSON.stringify(entry));
    }
    
    get(key) {
        const stored = localStorage.getItem(`cache_${key}`);
        if (!stored) return null;
        
        const entry = JSON.parse(stored);
        if (Date.now() > entry.expires) {
            localStorage.removeItem(`cache_${key}`);
            return null;
        }
        
        return entry.data;
    }
}
```

### 3. Progressive Data Loading

```javascript
async function loadDataProgressive() {
    // 1. Check memory cache
    if (memoryCache.has(key)) return memoryCache.get(key);
    
    // 2. Check localStorage cache
    const cached = localStorage.getItem(key);
    if (cached && isCacheValid(cached)) return JSON.parse(cached);
    
    // 3. Fetch from GitHub (raw URL)
    try {
        const data = await fetchFromGitHub(key);
        cacheData(key, data);
        return data;
    } catch (error) {
        // 4. Fall back to stale cache if offline
        if (!navigator.onLine && cached) {
            return JSON.parse(cached);
        }
        throw error;
    }
}
```

### 4. Offline-First Architecture

```javascript
class OfflineFirst {
    constructor() {
        this.queue = [];
        this.setupListeners();
    }
    
    setupListeners() {
        window.addEventListener('online', () => this.processQueue());
        window.addEventListener('offline', () => this.notifyOffline());
    }
    
    async fetch(url, options = {}) {
        if (navigator.onLine) {
            return fetch(url, options);
        } else {
            // Return cached version or queue for later
            const cached = this.getCached(url);
            if (cached) return cached;
            
            this.queue.push({ url, options, timestamp: Date.now() });
            throw new Error('Offline - request queued');
        }
    }
    
    async processQueue() {
        while (this.queue.length > 0) {
            const request = this.queue.shift();
            try {
                await fetch(request.url, request.options);
            } catch (error) {
                console.error('Queue processing error:', error);
            }
        }
    }
}
```

## 🔧 Advanced Configuration

### Using GitHub Pages as CDN

```javascript
// If you have GitHub Pages enabled
const CONFIG = {
    GITHUB: {
        PAGES_URL: 'https://username.github.io/repo/',
        USE_PAGES: true, // Use GitHub Pages when available
        
        getAssetUrl(path) {
            if (this.USE_PAGES && this.PAGES_URL) {
                return `${this.PAGES_URL}${path}`;
            }
            return this.getRawUrl(path);
        }
    }
};
```

### Multiple Data Sources

```javascript
class DataSourceManager {
    constructor() {
        this.sources = [
            {
                name: 'primary',
                baseUrl: 'https://raw.githubusercontent.com/user/repo1/main/',
                priority: 1
            },
            {
                name: 'fallback',
                baseUrl: 'https://raw.githubusercontent.com/user/repo2/main/',
                priority: 2
            }
        ];
    }
    
    async fetchWithFallback(path) {
        for (const source of this.sources) {
            try {
                const response = await fetch(`${source.baseUrl}${path}`);
                if (response.ok) return response.json();
            } catch (error) {
                continue; // Try next source
            }
        }
        throw new Error('All sources failed');
    }
}
```

### Data Versioning

```javascript
class VersionManager {
    constructor() {
        this.currentVersion = '1.0.0';
    }
    
    async checkForUpdates() {
        const manifest = await fetch(this.getManifestUrl());
        const remote = await manifest.json();
        
        if (this.isNewer(remote.version, this.currentVersion)) {
            return {
                hasUpdate: true,
                currentVersion: this.currentVersion,
                newVersion: remote.version,
                changelog: remote.changelog
            };
        }
        
        return { hasUpdate: false };
    }
    
    isNewer(v1, v2) {
        const parts1 = v1.split('.').map(Number);
        const parts2 = v2.split('.').map(Number);
        
        for (let i = 0; i < 3; i++) {
            if (parts1[i] > parts2[i]) return true;
            if (parts1[i] < parts2[i]) return false;
        }
        
        return false;
    }
}
```

## 🎨 UI Components

### Data Card Component

```javascript
class DataCard {
    constructor(data) {
        this.data = data;
    }
    
    render() {
        return `
            <div class="data-card" data-id="${this.data.id}">
                <div class="card-header">
                    <h3>${this.data.title}</h3>
                    <span class="badge">${this.data.category}</span>
                </div>
                <div class="card-body">
                    <p>${this.data.description}</p>
                </div>
                <div class="card-footer">
                    <button onclick="app.viewDetails('${this.data.id}')">
                        View Details
                    </button>
                    <button onclick="app.toggleFavorite('${this.data.id}')">
                        ${this.isFavorite() ? '★' : '☆'}
                    </button>
                </div>
            </div>
        `;
    }
    
    isFavorite() {
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        return favorites.includes(this.data.id);
    }
}
```

### Search & Filter System

```javascript
class SearchFilter {
    constructor(items) {
        this.items = items;
        this.filtered = items;
    }
    
    search(query) {
        query = query.toLowerCase();
        this.filtered = this.items.filter(item => 
            item.title.toLowerCase().includes(query) ||
            item.description.toLowerCase().includes(query) ||
            item.tags?.some(tag => tag.toLowerCase().includes(query))
        );
        return this.filtered;
    }
    
    filter(criteria) {
        this.filtered = this.items.filter(item => {
            for (const [key, value] of Object.entries(criteria)) {
                if (item[key] !== value) return false;
            }
            return true;
        });
        return this.filtered;
    }
    
    sort(field, direction = 'asc') {
        this.filtered.sort((a, b) => {
            const aVal = a[field];
            const bVal = b[field];
            
            if (direction === 'asc') {
                return aVal > bVal ? 1 : -1;
            } else {
                return aVal < bVal ? 1 : -1;
            }
        });
        return this.filtered;
    }
}
```

## 🔐 Security Considerations

1. **Public Data Only**: Only use this pattern for PUBLIC repositories
2. **No Sensitive Data**: Never store API keys or sensitive data
3. **CORS Headers**: GitHub raw URLs include proper CORS headers
4. **Rate Limiting**: Raw URLs have much higher limits than API
5. **Validation**: Always validate data from external sources

## 📊 Performance Optimizations

### 1. Lazy Loading

```javascript
class LazyLoader {
    constructor() {
        this.loaded = new Set();
        this.loading = new Map();
    }
    
    async load(key, loader) {
        if (this.loaded.has(key)) {
            return this.getFromCache(key);
        }
        
        if (this.loading.has(key)) {
            return this.loading.get(key);
        }
        
        const promise = loader().then(data => {
            this.loaded.add(key);
            this.loading.delete(key);
            this.cache(key, data);
            return data;
        });
        
        this.loading.set(key, promise);
        return promise;
    }
}
```

### 2. Virtual Scrolling

```javascript
class VirtualScroller {
    constructor(container, items, itemHeight) {
        this.container = container;
        this.items = items;
        this.itemHeight = itemHeight;
        this.visibleItems = [];
        
        this.setup();
    }
    
    setup() {
        const scrollHandler = () => this.handleScroll();
        this.container.addEventListener('scroll', scrollHandler);
        
        // Set container height
        const totalHeight = this.items.length * this.itemHeight;
        this.container.style.height = `${totalHeight}px`;
        
        this.render();
    }
    
    handleScroll() {
        const scrollTop = this.container.scrollTop;
        const containerHeight = this.container.clientHeight;
        
        const startIndex = Math.floor(scrollTop / this.itemHeight);
        const endIndex = Math.ceil((scrollTop + containerHeight) / this.itemHeight);
        
        this.visibleItems = this.items.slice(startIndex, endIndex);
        this.render();
    }
    
    render() {
        // Render only visible items
        this.container.innerHTML = this.visibleItems.map(item => 
            `<div style="height: ${this.itemHeight}px">${item.content}</div>`
        ).join('');
    }
}
```

### 3. Web Workers for Heavy Processing

```javascript
// Create worker code as a blob
const workerCode = `
    self.addEventListener('message', function(e) {
        const { action, data } = e.data;
        
        switch(action) {
            case 'process':
                const result = heavyProcessing(data);
                self.postMessage({ action: 'complete', result });
                break;
        }
    });
    
    function heavyProcessing(data) {
        // CPU-intensive work here
        return processedData;
    }
`;

const blob = new Blob([workerCode], { type: 'application/javascript' });
const worker = new Worker(URL.createObjectURL(blob));

worker.postMessage({ action: 'process', data: largeDataset });
worker.onmessage = (e) => {
    if (e.data.action === 'complete') {
        console.log('Processed:', e.data.result);
    }
};
```

## 🚢 Deployment Options

### 1. GitHub Pages

1. Enable GitHub Pages in repository settings
2. Set source to main branch
3. Access at: `https://username.github.io/repository/`

### 2. Static Hosting

Deploy the single HTML file to any static host:
- Netlify (drag & drop)
- Vercel
- Surge.sh
- AWS S3
- Azure Static Web Apps

### 3. Local File

Simply open the HTML file directly in a browser:
- Works offline after first sync
- No server required
- Can be distributed via USB/email

## 🧪 Testing Strategy

```javascript
// Simple test framework
class TestRunner {
    constructor() {
        this.tests = [];
        this.results = [];
    }
    
    test(name, fn) {
        this.tests.push({ name, fn });
    }
    
    async run() {
        for (const test of this.tests) {
            try {
                await test.fn();
                this.results.push({ name: test.name, passed: true });
                console.log(`✓ ${test.name}`);
            } catch (error) {
                this.results.push({ name: test.name, passed: false, error });
                console.error(`✗ ${test.name}:`, error);
            }
        }
        
        this.report();
    }
    
    report() {
        const passed = this.results.filter(r => r.passed).length;
        const failed = this.results.filter(r => !r.passed).length;
        
        console.log(`\nTests: ${passed} passed, ${failed} failed, ${this.tests.length} total`);
    }
}

// Usage
const tests = new TestRunner();

tests.test('GitHub data fetching', async () => {
    const data = await app.github.fetchFile('manifest.json');
    assert(data.version, 'Version should exist');
});

tests.test('Local storage', () => {
    app.local.saveData({ test: 'value' });
    const data = app.local.loadData();
    assert(data.test === 'value', 'Data should persist');
});

tests.run();
```

## 📱 Mobile Optimizations

```css
/* Mobile-first responsive design */
@media (max-width: 768px) {
    .data-grid {
        grid-template-columns: 1fr;
    }
    
    .app-header {
        padding: var(--spacing-md);
    }
    
    .btn {
        width: 100%;
        margin-bottom: 10px;
    }
}

/* Touch-friendly interactions */
.touch-target {
    min-height: 44px;
    min-width: 44px;
}

/* Prevent zoom on input focus (iOS) */
input, select, textarea {
    font-size: 16px;
}

/* Safe area for notched devices */
.app-container {
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
}
```

## 🎯 Best Practices

1. **Always Use Raw URLs**: Never use GitHub API for public data
2. **Cache Aggressively**: Store everything locally
3. **Fail Gracefully**: Always have offline fallbacks
4. **Version Your Data**: Include version in manifest
5. **Validate Input**: Sanitize all external data
6. **Progressive Enhancement**: Core features work offline
7. **Optimize Assets**: Minimize file sizes
8. **Test Offline**: Regularly test offline scenarios
9. **Monitor Storage**: Check localStorage quotas
10. **Document Everything**: Keep README updated

## 🔗 Resources

- [GitHub Raw URLs Documentation](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file)
- [LocalStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Progressive Web Apps](https://web.dev/progressive-web-apps/)
- [Offline First](https://offlinefirst.org/)

## 📄 License

This template is provided as open source under the MIT License. Use it to build amazing local-first applications!