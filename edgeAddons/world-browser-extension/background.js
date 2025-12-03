// LEVIATHAN World Browser - Background Service Worker
// Handles communication between popup and content scripts

console.log('[LEVIATHAN World Browser] Background service worker started');

// Listen for installation
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('[LEVIATHAN World Browser] Extension installed');
    } else if (details.reason === 'update') {
        console.log('[LEVIATHAN World Browser] Extension updated');
    }
});

// Handle messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('[LEVIATHAN World Browser] Message received:', message.type);

    switch (message.type) {
        case 'FETCH_REGISTRY':
            fetchRegistry().then(sendResponse);
            return true; // Will respond asynchronously

        case 'FETCH_SEED':
            fetchWorldSeed(message.worldId).then(sendResponse);
            return true;

        case 'IMPORT_TO_TAB':
            importToActiveTab(message.world, message.seed).then(sendResponse);
            return true;

        default:
            sendResponse({ error: 'Unknown message type' });
    }
});

async function fetchRegistry() {
    const urls = [
        'https://kody-w.github.io/localFirstTools/data/public-worlds/registry.json',
        'https://raw.githubusercontent.com/kody-w/localFirstTools/main/data/public-worlds/registry.json'
    ];

    for (const url of urls) {
        try {
            const response = await fetch(url, { cache: 'no-cache' });
            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            }
        } catch (error) {
            console.warn('Fetch failed:', url, error);
        }
    }

    return { success: false, error: 'Could not fetch registry' };
}

async function fetchWorldSeed(worldId) {
    const urls = [
        `https://kody-w.github.io/localFirstTools/data/public-worlds/seeds/${worldId}.json`,
        `https://raw.githubusercontent.com/kody-w/localFirstTools/main/data/public-worlds/seeds/${worldId}.json`
    ];

    for (const url of urls) {
        try {
            const response = await fetch(url, { cache: 'no-cache' });
            if (response.ok) {
                const data = await response.json();
                return { success: true, data };
            }
        } catch (error) {
            console.warn('Seed fetch failed:', url, error);
        }
    }

    return { success: false, error: 'Could not fetch world seed' };
}

async function importToActiveTab(world, seed) {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (!tab) {
            return { success: false, error: 'No active tab' };
        }

        // Check if it's a LEVIATHAN game page
        const isGame = await chrome.tabs.sendMessage(tab.id, { type: 'CHECK_GAME' });

        if (!isGame || !isGame.isGame) {
            // Save for later
            await saveWorldForLater(world, seed);
            return { success: true, message: 'World saved. Open LEVIATHAN to load it.' };
        }

        // Send import message
        await chrome.tabs.sendMessage(tab.id, {
            type: 'IMPORT_WORLD',
            world,
            seed
        });

        return { success: true, message: 'World imported!' };

    } catch (error) {
        console.error('Import error:', error);
        // Save for later as fallback
        await saveWorldForLater(world, seed);
        return { success: true, message: 'World saved. Open LEVIATHAN to load it.' };
    }
}

async function saveWorldForLater(world, seed) {
    const result = await chrome.storage.local.get('pendingWorldImports');
    const pending = result.pendingWorldImports || [];

    // Avoid duplicates
    const existingIndex = pending.findIndex(p => p.world.id === world.id);
    if (existingIndex >= 0) {
        pending[existingIndex] = { world, seed, timestamp: Date.now() };
    } else {
        pending.push({ world, seed, timestamp: Date.now() });
    }

    await chrome.storage.local.set({ pendingWorldImports: pending });
}

// Badge to show number of pending worlds
async function updateBadge() {
    try {
        const result = await chrome.storage.local.get('pendingWorldImports');
        const pending = result.pendingWorldImports || [];

        if (pending.length > 0) {
            chrome.action.setBadgeText({ text: String(pending.length) });
            chrome.action.setBadgeBackgroundColor({ color: '#0ff' });
        } else {
            chrome.action.setBadgeText({ text: '' });
        }
    } catch (error) {
        // Ignore
    }
}

// Update badge periodically
setInterval(updateBadge, 5000);
updateBadge();
