// LEVIATHAN World Browser - Content Script
// Injects imported worlds into the game

console.log('[LEVIATHAN World Browser] Content script loaded');

// Listen for messages from popup/background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'IMPORT_WORLD') {
        handleWorldImport(message.world, message.seed);
        sendResponse({ success: true });
    } else if (message.type === 'CHECK_GAME') {
        sendResponse({ isGame: isLeviathanGame() });
    }
    return true;
});

// Check for pending imports when page loads
checkPendingImports();

function isLeviathanGame() {
    // Check if we're on the LEVIATHAN game page
    return document.title.includes('LEVIATHAN') ||
           document.querySelector('[data-game="leviathan"]') !== null ||
           window.location.pathname.includes('levi.html');
}

async function checkPendingImports() {
    try {
        const result = await chrome.storage.local.get('pendingWorldImports');
        const pending = result.pendingWorldImports || [];

        if (pending.length > 0 && isLeviathanGame()) {
            // Wait for game to initialize
            setTimeout(() => {
                pending.forEach(item => {
                    handleWorldImport(item.world, item.seed);
                });
                // Clear pending imports
                chrome.storage.local.remove('pendingWorldImports');
            }, 2000);
        }
    } catch (error) {
        console.warn('[LEVIATHAN World Browser] Failed to check pending imports:', error);
    }
}

function handleWorldImport(world, seed) {
    console.log('[LEVIATHAN World Browser] Importing world:', world.name);

    try {
        // Store the world seed in localStorage for the game to access
        const STORAGE_KEY = 'leviathan-imported-worlds';
        let importedWorlds = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');

        importedWorlds[world.id] = {
            world: world,
            seed: seed,
            importedAt: Date.now()
        };

        localStorage.setItem(STORAGE_KEY, JSON.stringify(importedWorlds));

        // Try to notify the game directly if the WorldStore is available
        if (window.WorldStore && typeof window.WorldStore.onWorldImported === 'function') {
            window.WorldStore.onWorldImported(world, seed);
        }

        // Also try to trigger the public world manager
        if (window.PublicWorldManager && typeof window.PublicWorldManager.registerWorld === 'function') {
            window.PublicWorldManager.registerWorld(world, seed);
        }

        // Dispatch custom event for the game to listen to
        window.dispatchEvent(new CustomEvent('leviathan-world-imported', {
            detail: { world, seed }
        }));

        // Show in-game notification if available
        if (typeof window.showNotification === 'function') {
            window.showNotification(`World "${world.name}" imported successfully!`, 'success');
        }

        // Visual feedback
        showImportBanner(world);

    } catch (error) {
        console.error('[LEVIATHAN World Browser] Import failed:', error);

        if (typeof window.showNotification === 'function') {
            window.showNotification('Failed to import world: ' + error.message, 'error');
        }
    }
}

function showImportBanner(world) {
    // Create a temporary banner to show import success
    const banner = document.createElement('div');
    banner.id = 'world-import-banner';
    banner.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #0a0a2a 0%, #1a0a3a 100%);
            border: 2px solid #0ff;
            border-radius: 16px;
            padding: 16px 24px;
            z-index: 100000;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 10px 40px rgba(0,255,255,0.3);
            animation: slideDown 0.3s ease, fadeOut 0.3s ease 2.7s;
        ">
            <span style="font-size: 32px;">🌌</span>
            <div>
                <div style="color: #0ff; font-size: 14px; font-weight: 600;">World Imported</div>
                <div style="color: #fff; font-size: 16px;">${escapeHtml(world.name)}</div>
            </div>
        </div>
        <style>
            @keyframes slideDown {
                from { transform: translateX(-50%) translateY(-100px); opacity: 0; }
                to { transform: translateX(-50%) translateY(0); opacity: 1; }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
        </style>
    `;

    document.body.appendChild(banner);

    // Remove after 3 seconds
    setTimeout(() => {
        banner.remove();
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Also inject a helper into the page context for the game to use
function injectPageHelper() {
    const script = document.createElement('script');
    script.textContent = `
        // LEVIATHAN World Browser - Page Helper
        window.LeviathanWorldBrowser = {
            getImportedWorlds: function() {
                try {
                    return JSON.parse(localStorage.getItem('leviathan-imported-worlds') || '{}');
                } catch (e) {
                    return {};
                }
            },

            getWorld: function(worldId) {
                const worlds = this.getImportedWorlds();
                return worlds[worldId] || null;
            },

            clearImportedWorlds: function() {
                localStorage.removeItem('leviathan-imported-worlds');
            },

            listWorldIds: function() {
                return Object.keys(this.getImportedWorlds());
            }
        };

        // Listen for import events
        window.addEventListener('leviathan-world-imported', function(e) {
            console.log('[LEVIATHAN] World imported via browser extension:', e.detail.world.name);

            // Auto-add to registry if WorldStore is available
            if (window.WorldStore && !window.WorldStore._extensionWorlds) {
                window.WorldStore._extensionWorlds = [];
            }
            if (window.WorldStore) {
                window.WorldStore._extensionWorlds.push(e.detail);
            }
        });

        console.log('[LEVIATHAN World Browser] Page helper injected');
    `;

    document.documentElement.appendChild(script);
    script.remove();
}

// Inject helper when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectPageHelper);
} else {
    injectPageHelper();
}
