// LEVIATHAN World Browser - Popup Logic
// Fetches world seeds from GitHub and allows importing into the game

const REGISTRY_URLS = [
    // Try GitHub Pages first
    'https://kody-w.github.io/localFirstTools/data/public-worlds/registry.json',
    // Fallback to raw GitHub
    'https://raw.githubusercontent.com/kody-w/localFirstTools/main/data/public-worlds/registry.json'
];

const SEED_BASE_URLS = [
    'https://kody-w.github.io/localFirstTools/data/public-worlds/seeds/',
    'https://raw.githubusercontent.com/kody-w/localFirstTools/main/data/public-worlds/seeds/'
];

let registry = null;
let currentFilter = 'all';
let importingWorld = null;

// DOM Elements
const worldGrid = document.getElementById('worldGrid');
const loadingState = document.getElementById('loadingState');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const worldCount = document.getElementById('worldCount');
const refreshBtn = document.getElementById('refreshBtn');
const filterTabs = document.getElementById('filterTabs');
const toast = document.getElementById('toast');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadRegistry();
    setupEventListeners();
});

function setupEventListeners() {
    // Refresh button
    refreshBtn.addEventListener('click', () => {
        loadRegistry(true);
    });

    // Filter tabs
    filterTabs.addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-tab')) {
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderWorlds();
        }
    });
}

async function loadRegistry(forceRefresh = false) {
    setStatus('loading', 'Fetching worlds...');
    refreshBtn.classList.add('loading');
    worldGrid.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span>Fetching worlds from GitHub...</span>
        </div>
    `;

    // Try cache first unless force refresh
    if (!forceRefresh) {
        const cached = await getCachedRegistry();
        if (cached) {
            registry = cached;
            setStatus('connected', 'Connected (cached)');
            renderWorlds();
            refreshBtn.classList.remove('loading');
            // Still try to update in background
            fetchAndUpdateRegistry();
            return;
        }
    }

    await fetchAndUpdateRegistry();
    refreshBtn.classList.remove('loading');
}

async function fetchAndUpdateRegistry() {
    for (const url of REGISTRY_URLS) {
        try {
            const response = await fetch(url, {
                cache: 'no-cache',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (response.ok) {
                registry = await response.json();
                await cacheRegistry(registry);
                setStatus('connected', 'Connected to GitHub');
                renderWorlds();
                return;
            }
        } catch (error) {
            console.warn(`Failed to fetch from ${url}:`, error);
        }
    }

    // All URLs failed
    setStatus('error', 'Failed to connect');
    worldGrid.innerHTML = `
        <div class="error-container">
            <div class="error-icon">🌐</div>
            <div class="error-message">Could not connect to GitHub</div>
            <button class="retry-btn" onclick="loadRegistry(true)">Try Again</button>
        </div>
    `;
}

async function getCachedRegistry() {
    try {
        const result = await chrome.storage.local.get('worldRegistry');
        if (result.worldRegistry) {
            const cached = result.worldRegistry;
            // Check if cache is less than 1 hour old
            if (Date.now() - cached.timestamp < 3600000) {
                return cached.data;
            }
        }
    } catch (error) {
        console.warn('Cache read failed:', error);
    }
    return null;
}

async function cacheRegistry(data) {
    try {
        await chrome.storage.local.set({
            worldRegistry: {
                data: data,
                timestamp: Date.now()
            }
        });
    } catch (error) {
        console.warn('Cache write failed:', error);
    }
}

function setStatus(state, text) {
    statusDot.className = 'status-dot ' + state;
    statusText.textContent = text;
}

function renderWorlds() {
    if (!registry || !registry.worlds) {
        worldGrid.innerHTML = `
            <div class="empty-container">
                <div class="empty-icon">🌌</div>
                <div>No worlds available</div>
            </div>
        `;
        worldCount.textContent = '0 worlds';
        return;
    }

    let worlds = registry.worlds;

    // Apply filter
    if (currentFilter === 'featured') {
        worlds = worlds.filter(w => w.featured);
    } else if (currentFilter !== 'all') {
        worlds = worlds.filter(w => w.category === currentFilter);
    }

    worldCount.textContent = `${worlds.length} world${worlds.length !== 1 ? 's' : ''}`;

    if (worlds.length === 0) {
        worldGrid.innerHTML = `
            <div class="empty-container">
                <div class="empty-icon">🔍</div>
                <div>No worlds match this filter</div>
            </div>
        `;
        return;
    }

    worldGrid.innerHTML = worlds.map(world => renderWorldCard(world)).join('');

    // Add click handlers to import buttons
    document.querySelectorAll('.import-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const worldId = btn.dataset.worldId;
            importWorld(worldId);
        });
    });
}

function renderWorldCard(world) {
    const icon = getCategoryIcon(world.category);
    const isImporting = importingWorld === world.id;

    return `
        <div class="world-card ${world.featured ? 'featured' : ''}" data-world-id="${world.id}">
            <div class="world-header">
                <span class="world-icon">${icon}</span>
                <div class="world-info">
                    <div class="world-name">${escapeHtml(world.name)}</div>
                    <div class="world-author">by ${escapeHtml(world.author)}</div>
                </div>
                ${world.featured ? '<span class="featured-badge">Featured</span>' : ''}
            </div>
            <div class="world-description">${escapeHtml(world.description)}</div>
            <div class="world-meta">
                <div class="meta-item">
                    <span>👥</span>
                    <span>${world.totalVisitors || 0} visitors</span>
                </div>
                <div class="meta-item">
                    <span>⚡</span>
                    <span>${world.temporalContributions || 0} energy</span>
                </div>
            </div>
            <div class="world-tags">
                ${(world.tags || []).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
            </div>
            <button class="import-btn ${isImporting ? 'importing' : ''}"
                    data-world-id="${world.id}"
                    ${isImporting ? 'disabled' : ''}>
                ${isImporting ? '⏳ Importing...' : '📥 Import World'}
            </button>
        </div>
    `;
}

function getCategoryIcon(category) {
    const icons = {
        exploration: '🌋',
        social: '👥',
        creative: '🎨',
        challenge: '⚔️',
        story: '📖'
    };
    return icons[category] || '🌍';
}

async function importWorld(worldId) {
    const world = registry.worlds.find(w => w.id === worldId);
    if (!world) {
        showToast('World not found', 'error');
        return;
    }

    importingWorld = worldId;
    renderWorlds();

    try {
        // Fetch the world seed
        let seedData = null;

        for (const baseUrl of SEED_BASE_URLS) {
            try {
                const seedUrl = `${baseUrl}${worldId}.json`;
                const response = await fetch(seedUrl, {
                    cache: 'no-cache'
                });

                if (response.ok) {
                    seedData = await response.json();
                    break;
                }
            } catch (error) {
                console.warn('Seed fetch failed:', error);
            }
        }

        if (!seedData) {
            throw new Error('Could not fetch world seed');
        }

        // Send to content script via background
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (tab) {
            try {
                await chrome.tabs.sendMessage(tab.id, {
                    type: 'IMPORT_WORLD',
                    world: world,
                    seed: seedData
                });
                showToast(`Imported "${world.name}"!`, 'success');
            } catch (error) {
                // If content script isn't loaded, save to storage and show instructions
                await saveWorldToStorage(world, seedData);
                showToast('World saved! Open LEVIATHAN to load it.', 'success');
            }
        } else {
            // Save to storage
            await saveWorldToStorage(world, seedData);
            showToast('World saved! Open LEVIATHAN to load it.', 'success');
        }

    } catch (error) {
        console.error('Import failed:', error);
        showToast('Import failed: ' + error.message, 'error');
    }

    importingWorld = null;
    renderWorlds();
}

async function saveWorldToStorage(world, seed) {
    // Get existing pending imports
    const result = await chrome.storage.local.get('pendingWorldImports');
    const pending = result.pendingWorldImports || [];

    // Add new import (avoid duplicates)
    const existing = pending.findIndex(p => p.world.id === world.id);
    if (existing >= 0) {
        pending[existing] = { world, seed, timestamp: Date.now() };
    } else {
        pending.push({ world, seed, timestamp: Date.now() });
    }

    await chrome.storage.local.set({ pendingWorldImports: pending });
}

function showToast(message, type = 'info') {
    toast.textContent = type === 'success' ? '✓ ' + message : type === 'error' ? '✕ ' + message : message;
    toast.className = 'toast show ' + type;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
