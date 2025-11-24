/**
 * LOCAL FIRST TOOLS - Chrome Extension Background Service Worker
 */

// Installation handler
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('🎉 Local First Tools installed!');

        // Open welcome page
        chrome.tabs.create({
            url: chrome.runtime.getURL('index.html')
        });

        // Set default settings
        chrome.storage.local.set({
            version: '1.0.0',
            installedAt: new Date().toISOString(),
            usage: {}
        });
    } else if (details.reason === 'update') {
        console.log('✨ Local First Tools updated!');
    }
});

// Track app usage
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'trackUsage') {
        chrome.storage.local.get(['usage'], (result) => {
            const usage = result.usage || {};
            const appId = message.appId;

            if (!usage[appId]) {
                usage[appId] = { count: 0, lastUsed: null };
            }

            usage[appId].count++;
            usage[appId].lastUsed = new Date().toISOString();

            chrome.storage.local.set({ usage });
        });
    }

    sendResponse({ success: true });
    return true;
});

// Context menu for quick access
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: 'openGallery',
        title: 'Open Local First Tools',
        contexts: ['page', 'selection']
    });

    chrome.contextMenus.create({
        id: 'openMetaDashboard',
        title: 'Open Meta Dashboard',
        contexts: ['page']
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'openGallery') {
        chrome.tabs.create({
            url: chrome.runtime.getURL('index.html')
        });
    } else if (info.menuItemId === 'openMetaDashboard') {
        chrome.tabs.create({
            url: chrome.runtime.getURL('apps/development/meta-dashboard.html')
        });
    }
});

console.log('🚀 Local First Tools background service worker ready!');
