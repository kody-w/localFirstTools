/**
 * LocalFirst Service Worker
 * Caches HTML applications for offline use and enables seamless updates
 *
 * Strategy: Cache-first with background update detection
 * - Serves cached version immediately for fast loads
 * - Checks for updates in background
 * - Notifies user when update available
 */

const CACHE_VERSION = 'v1';
const HTML_CACHE = `localfirst-html-${CACHE_VERSION}`;
const ASSET_CACHE = `localfirst-assets-${CACHE_VERSION}`;
const UPDATE_CHECK_INTERVAL = 60000; // Check for updates every minute

// Files to cache (will be dynamically populated)
const CACHE_URLS = [];

/**
 * Install Event - Cache initial resources
 */
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Installing...');

    event.waitUntil(
        caches.open(HTML_CACHE).then((cache) => {
            console.log('[ServiceWorker] Caching app shell');
            return cache.addAll(CACHE_URLS);
        }).then(() => {
            return self.skipWaiting(); // Activate immediately
        })
    );
});

/**
 * Activate Event - Clean up old caches
 */
self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activating...');

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName.startsWith('localfirst-') && cacheName !== HTML_CACHE && cacheName !== ASSET_CACHE) {
                        console.log('[ServiceWorker] Removing old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            return self.clients.claim(); // Take control of all pages immediately
        })
    );
});

/**
 * Fetch Event - Cache-first strategy with background update
 */
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Only handle same-origin requests
    if (url.origin !== location.origin) {
        return;
    }

    // Determine cache based on file type
    const isHTML = url.pathname.endsWith('.html') || url.pathname === '/';
    const cacheName = isHTML ? HTML_CACHE : ASSET_CACHE;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // Return cached version immediately
            if (cachedResponse) {
                // Check for updates in background
                checkForUpdate(event.request, cacheName);
                return cachedResponse;
            }

            // Not in cache, fetch from network
            return fetch(event.request).then((response) => {
                // Cache the new response
                if (response.status === 200) {
                    const responseToCache = response.clone();
                    caches.open(cacheName).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return response;
            });
        }).catch(() => {
            // Network failed and no cache, return offline page
            return new Response(
                '<html><body><h1>Offline</h1><p>Please check your connection.</p></body></html>',
                { headers: { 'Content-Type': 'text/html' } }
            );
        })
    );
});

/**
 * Check for update in background
 */
function checkForUpdate(request, cacheName) {
    fetch(request, { cache: 'no-cache' }).then((response) => {
        if (response.status === 200) {
            caches.open(cacheName).then((cache) => {
                cache.match(request).then((cachedResponse) => {
                    // Compare response headers to detect changes
                    const cachedETag = cachedResponse?.headers.get('etag');
                    const newETag = response.headers.get('etag');

                    const cachedModified = cachedResponse?.headers.get('last-modified');
                    const newModified = response.headers.get('last-modified');

                    // Check if content has changed
                    const hasChanged = (cachedETag && newETag && cachedETag !== newETag) ||
                                      (cachedModified && newModified && cachedModified !== newModified);

                    if (hasChanged || !cachedResponse) {
                        console.log('[ServiceWorker] Update detected for:', request.url);

                        // Cache the new version
                        cache.put(request, response.clone());

                        // Notify all clients about update
                        self.clients.matchAll().then((clients) => {
                            clients.forEach((client) => {
                                client.postMessage({
                                    type: 'UPDATE_AVAILABLE',
                                    url: request.url,
                                    timestamp: Date.now()
                                });
                            });
                        });
                    }
                });
            });
        }
    }).catch((error) => {
        console.log('[ServiceWorker] Update check failed:', error);
    });
}

/**
 * Message Event - Handle messages from clients
 */
self.addEventListener('message', (event) => {
    if (event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName.startsWith('localfirst-')) {
                            return caches.delete(cacheName);
                        }
                    })
                );
            }).then(() => {
                event.ports[0].postMessage({ success: true });
            })
        );
    }

    if (event.data.type === 'GET_CACHED_URLS') {
        event.waitUntil(
            caches.open(HTML_CACHE).then((cache) => {
                return cache.keys();
            }).then((requests) => {
                const urls = requests.map(req => req.url);
                event.ports[0].postMessage({ urls });
            })
        );
    }
});

/**
 * Sync Event - Background sync for state (if needed)
 */
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-state') {
        event.waitUntil(syncState());
    }
});

async function syncState() {
    // Placeholder for state sync logic
    // Could be used to sync state to cloud when online
    console.log('[ServiceWorker] Syncing state...');
}

console.log('[ServiceWorker] Loaded');
