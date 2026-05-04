/**
 * MEMBRANE CONNECTOR v1.0.0
 *
 * Drop this into any HTML app to connect it to The Membrane.
 *
 * Usage:
 *   <script src="membrane-connect.js"></script>
 *
 *   // Or configure before loading:
 *   window.MEMBRANE_CONFIG = {
 *       appId: 'my-app',
 *       appName: 'My Cool App',
 *       icon: '🎨',
 *       autoTrack: true,
 *       showWidget: true
 *   };
 *
 * API:
 *   membrane.track('event-name', { data });
 *   membrane.clipboard('color', '#ff0000');
 *   membrane.command('do-something', { params });
 */

(function() {
    'use strict';

    // ========================================
    // CONFIGURATION
    // ========================================

    const defaultConfig = {
        appId: window.location.pathname.split('/').pop().replace('.html', '') || 'unknown-app',
        appName: document.title || 'Unknown App',
        icon: '📱',
        autoTrack: true,
        showWidget: true,
        channelName: 'membrane-channel',
        widgetPosition: 'bottom-right', // bottom-right, bottom-left, top-right, top-left
        debug: false
    };

    const config = { ...defaultConfig, ...(window.MEMBRANE_CONFIG || {}) };

    // ========================================
    // MEMBRANE CONNECTOR CLASS
    // ========================================

    class MembraneConnector {
        constructor() {
            this.connected = false;
            this.channel = null;
            this.widget = null;
            this.eventQueue = [];
            this.commandHandlers = new Map();
            this.clipboardData = null;

            this.init();
        }

        // ========================================
        // INITIALIZATION
        // ========================================

        init() {
            this.log('Initializing Membrane Connector...');

            // Set up broadcast channel
            this.channel = new BroadcastChannel(config.channelName);
            this.channel.onmessage = (e) => this.handleMessage(e.data);

            // Register with Membrane
            this.register();

            // Set up auto-tracking if enabled
            if (config.autoTrack) {
                this.setupAutoTracking();
            }

            // Create widget if enabled
            if (config.showWidget) {
                this.createWidget();
            }

            // Set up clipboard interception
            this.setupClipboard();

            this.log('Membrane Connector initialized');
        }

        register() {
            this.channel.postMessage({
                type: 'app:register',
                appId: config.appId,
                name: config.appName,
                icon: config.icon,
                capabilities: this.getCapabilities(),
                timestamp: Date.now()
            });
        }

        getCapabilities() {
            const caps = [];

            // Detect common capabilities
            if (document.querySelector('canvas')) caps.push('canvas');
            if (document.querySelector('audio, video')) caps.push('media');
            if (document.querySelector('form')) caps.push('forms');
            if (window.THREE) caps.push('3d');
            if (localStorage.length > 0) caps.push('storage');

            return caps;
        }

        // ========================================
        // MESSAGE HANDLING
        // ========================================

        handleMessage(data) {
            this.log('Received:', data.type);

            switch (data.type) {
                case 'membrane:registered':
                    this.connected = true;
                    this.updateWidget('connected');
                    this.log('Connected to Membrane');
                    break;

                case 'membrane:announce':
                    // Membrane is alive, register again
                    this.register();
                    break;

                case 'membrane:discover':
                    // Membrane is looking for apps
                    this.register();
                    break;

                case 'membrane:command':
                    this.executeCommand(data.intent);
                    break;

                case 'membrane:queryResult':
                    // Handle query results if needed
                    break;

                case 'membrane:clipboard':
                    // Incoming clipboard data from another app
                    this.handleIncomingClipboard(data);
                    break;
            }
        }

        // ========================================
        // EVENT TRACKING
        // ========================================

        track(eventName, data = {}) {
            const event = {
                type: 'app:event',
                appId: config.appId,
                event: eventName,
                data: data,
                timestamp: Date.now()
            };

            if (this.connected) {
                this.channel.postMessage(event);
            } else {
                this.eventQueue.push(event);
            }

            this.log('Tracked:', eventName, data);
        }

        setupAutoTracking() {
            // Track page visibility
            document.addEventListener('visibilitychange', () => {
                this.track(document.hidden ? 'app:hidden' : 'app:visible');
            });

            // Track clicks on important elements
            document.addEventListener('click', (e) => {
                const target = e.target.closest('button, a, [data-track]');
                if (target) {
                    this.track('click', {
                        element: target.tagName.toLowerCase(),
                        text: target.textContent?.slice(0, 50),
                        id: target.id || undefined,
                        class: target.className || undefined
                    });
                }
            });

            // Track form submissions
            document.addEventListener('submit', (e) => {
                this.track('form:submit', {
                    formId: e.target.id || undefined
                });
            });

            // Track key shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey || e.metaKey) {
                    this.track('shortcut', {
                        key: e.key,
                        ctrl: e.ctrlKey,
                        meta: e.metaKey,
                        shift: e.shiftKey
                    });
                }
            });

            // Track localStorage changes
            const originalSetItem = localStorage.setItem.bind(localStorage);
            localStorage.setItem = (key, value) => {
                this.track('storage:set', { key, size: value.length });
                return originalSetItem(key, value);
            };

            // Track errors
            window.addEventListener('error', (e) => {
                this.track('error', {
                    message: e.message,
                    filename: e.filename?.split('/').pop()
                });
            });

            // Track app-specific events via custom event
            window.addEventListener('membrane:track', (e) => {
                this.track(e.detail.event, e.detail.data);
            });

            this.log('Auto-tracking enabled');
        }

        // ========================================
        // SEMANTIC CLIPBOARD
        // ========================================

        clipboard(dataType, data, metadata = {}) {
            this.clipboardData = {
                type: dataType,
                data: data,
                metadata: metadata,
                sourceApp: config.appId,
                timestamp: Date.now()
            };

            this.channel.postMessage({
                type: 'app:clipboard',
                appId: config.appId,
                dataType: dataType,
                data: data,
                metadata: metadata,
                timestamp: Date.now()
            });

            this.log('Clipboard set:', dataType);
        }

        setupClipboard() {
            // Intercept copy events
            document.addEventListener('copy', (e) => {
                const selection = window.getSelection().toString();
                if (selection) {
                    // Try to detect type
                    const type = this.detectDataType(selection);
                    this.clipboard(type, selection);
                }
            });

            // Listen for paste events
            document.addEventListener('paste', (e) => {
                if (this.clipboardData) {
                    // Dispatch custom event with semantic data
                    window.dispatchEvent(new CustomEvent('membrane:paste', {
                        detail: this.clipboardData
                    }));
                }
            });
        }

        detectDataType(text) {
            // Color
            if (/^#[0-9a-fA-F]{3,8}$/.test(text)) return 'color';
            if (/^rgb\(/.test(text)) return 'color';
            if (/^hsl\(/.test(text)) return 'color';

            // Date/Time
            if (/^\d{4}-\d{2}-\d{2}/.test(text)) return 'date';
            if (/^\d{1,2}:\d{2}/.test(text)) return 'time';

            // Number
            if (/^-?\d+(\.\d+)?$/.test(text)) return 'number';

            // URL
            if (/^https?:\/\//.test(text)) return 'url';

            // Email
            if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text)) return 'email';

            // JSON
            try {
                JSON.parse(text);
                return 'json';
            } catch {}

            // Default
            return 'text';
        }

        handleIncomingClipboard(data) {
            this.clipboardData = {
                type: data.dataType,
                data: data.data,
                metadata: data.metadata || {},
                sourceApp: data.appId,
                timestamp: data.timestamp
            };

            // Notify app of new clipboard data
            window.dispatchEvent(new CustomEvent('membrane:clipboard', {
                detail: this.clipboardData
            }));
        }

        // ========================================
        // COMMAND EXECUTION
        // ========================================

        onCommand(commandName, handler) {
            this.commandHandlers.set(commandName, handler);
        }

        executeCommand(intent) {
            // Parse intent from Membrane
            // Format: { action: 'setColor', target: 'background', value: '#ff0000' }

            const handler = this.commandHandlers.get(intent.action);
            if (handler) {
                try {
                    handler(intent);
                    this.track('command:executed', { action: intent.action });
                } catch (error) {
                    this.track('command:failed', { action: intent.action, error: error.message });
                }
            } else {
                // Try generic command execution
                this.tryGenericCommand(intent);
            }
        }

        tryGenericCommand(intent) {
            // Attempt common DOM manipulations
            switch (intent.action) {
                case 'setStyle':
                    const el = document.querySelector(intent.target);
                    if (el) {
                        Object.assign(el.style, intent.styles);
                        this.track('command:executed', { action: 'setStyle' });
                    }
                    break;

                case 'click':
                    const clickEl = document.querySelector(intent.target);
                    if (clickEl) {
                        clickEl.click();
                        this.track('command:executed', { action: 'click' });
                    }
                    break;

                case 'setValue':
                    const inputEl = document.querySelector(intent.target);
                    if (inputEl) {
                        inputEl.value = intent.value;
                        inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                        this.track('command:executed', { action: 'setValue' });
                    }
                    break;
            }
        }

        // ========================================
        // FLOATING WIDGET
        // ========================================

        createWidget() {
            // Inject styles
            const style = document.createElement('style');
            style.textContent = `
                .membrane-widget {
                    position: fixed;
                    ${config.widgetPosition.includes('bottom') ? 'bottom: 20px' : 'top: 20px'};
                    ${config.widgetPosition.includes('right') ? 'right: 20px' : 'left: 20px'};
                    z-index: 999999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                .membrane-widget-btn {
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    border: none;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
                    transition: transform 0.2s, box-shadow 0.2s;
                    position: relative;
                }

                .membrane-widget-btn:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 30px rgba(99, 102, 241, 0.6);
                }

                .membrane-widget-btn.connecting {
                    animation: membrane-pulse 1s ease-in-out infinite;
                }

                .membrane-widget-btn.connected::after {
                    content: '';
                    position: absolute;
                    bottom: 2px;
                    right: 2px;
                    width: 12px;
                    height: 12px;
                    background: #10b981;
                    border-radius: 50%;
                    border: 2px solid white;
                }

                @keyframes membrane-pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.6; }
                }

                .membrane-widget-panel {
                    position: absolute;
                    ${config.widgetPosition.includes('bottom') ? 'bottom: 60px' : 'top: 60px'};
                    ${config.widgetPosition.includes('right') ? 'right: 0' : 'left: 0'};
                    width: 280px;
                    background: #1a1a2e;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                    padding: 16px;
                    display: none;
                    color: #e2e8f0;
                }

                .membrane-widget-panel.open {
                    display: block;
                    animation: membrane-slideIn 0.2s ease;
                }

                @keyframes membrane-slideIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .membrane-widget-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 12px;
                    padding-bottom: 12px;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                }

                .membrane-widget-title {
                    font-weight: 600;
                    font-size: 14px;
                }

                .membrane-widget-status {
                    font-size: 12px;
                    color: #94a3b8;
                }

                .membrane-widget-status.connected {
                    color: #10b981;
                }

                .membrane-widget-stats {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                    margin-bottom: 12px;
                }

                .membrane-widget-stat {
                    background: rgba(255,255,255,0.05);
                    padding: 8px;
                    border-radius: 8px;
                    text-align: center;
                }

                .membrane-widget-stat-value {
                    font-size: 20px;
                    font-weight: 700;
                    color: #6366f1;
                }

                .membrane-widget-stat-label {
                    font-size: 11px;
                    color: #94a3b8;
                }

                .membrane-widget-actions {
                    display: flex;
                    gap: 8px;
                }

                .membrane-widget-action {
                    flex: 1;
                    padding: 8px;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    cursor: pointer;
                    transition: background 0.2s;
                }

                .membrane-widget-action.primary {
                    background: #6366f1;
                    color: white;
                }

                .membrane-widget-action.primary:hover {
                    background: #8b5cf6;
                }

                .membrane-widget-action.secondary {
                    background: rgba(255,255,255,0.1);
                    color: #e2e8f0;
                }

                .membrane-widget-action.secondary:hover {
                    background: rgba(255,255,255,0.2);
                }
            `;
            document.head.appendChild(style);

            // Create widget HTML
            this.widget = document.createElement('div');
            this.widget.className = 'membrane-widget';
            this.widget.innerHTML = `
                <button class="membrane-widget-btn connecting" id="membraneWidgetBtn">
                    🧠
                </button>
                <div class="membrane-widget-panel" id="membraneWidgetPanel">
                    <div class="membrane-widget-header">
                        <span class="membrane-widget-title">THE MEMBRANE</span>
                        <span class="membrane-widget-status" id="membraneWidgetStatus">Connecting...</span>
                    </div>
                    <div class="membrane-widget-stats">
                        <div class="membrane-widget-stat">
                            <div class="membrane-widget-stat-value" id="membraneEventCount">0</div>
                            <div class="membrane-widget-stat-label">Events</div>
                        </div>
                        <div class="membrane-widget-stat">
                            <div class="membrane-widget-stat-value" id="membraneSessionTime">0m</div>
                            <div class="membrane-widget-stat-label">Session</div>
                        </div>
                    </div>
                    <div class="membrane-widget-actions">
                        <button class="membrane-widget-action primary" onclick="window.open('membrane.html', '_blank')">
                            Open Membrane
                        </button>
                        <button class="membrane-widget-action secondary" onclick="membrane.track('manual:ping')">
                            Ping
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(this.widget);

            // Toggle panel on click
            const btn = this.widget.querySelector('#membraneWidgetBtn');
            const panel = this.widget.querySelector('#membraneWidgetPanel');

            btn.addEventListener('click', () => {
                panel.classList.toggle('open');
            });

            // Close panel when clicking outside
            document.addEventListener('click', (e) => {
                if (!this.widget.contains(e.target)) {
                    panel.classList.remove('open');
                }
            });

            // Start session timer
            this.startSessionTimer();
        }

        updateWidget(status) {
            if (!this.widget) return;

            const btn = this.widget.querySelector('#membraneWidgetBtn');
            const statusEl = this.widget.querySelector('#membraneWidgetStatus');

            btn.classList.remove('connecting');

            if (status === 'connected') {
                btn.classList.add('connected');
                statusEl.textContent = 'Connected';
                statusEl.classList.add('connected');
            } else if (status === 'disconnected') {
                btn.classList.remove('connected');
                statusEl.textContent = 'Disconnected';
                statusEl.classList.remove('connected');
            }
        }

        incrementEventCount() {
            if (!this.widget) return;
            const el = this.widget.querySelector('#membraneEventCount');
            if (el) {
                el.textContent = parseInt(el.textContent) + 1;
            }
        }

        startSessionTimer() {
            const startTime = Date.now();
            const el = this.widget.querySelector('#membraneSessionTime');

            setInterval(() => {
                const minutes = Math.floor((Date.now() - startTime) / 60000);
                el.textContent = `${minutes}m`;
            }, 60000);
        }

        // ========================================
        // UTILITIES
        // ========================================

        log(...args) {
            if (config.debug) {
                console.log('[Membrane]', ...args);
            }
        }
    }

    // ========================================
    // INITIALIZATION
    // ========================================

    // Create global instance
    const membrane = new MembraneConnector();

    // Expose to window
    window.membrane = membrane;

    // Also expose config for debugging
    window.MEMBRANE_CONFIG = config;

    // Convenience method for custom tracking
    window.trackToMembrane = (event, data) => membrane.track(event, data);

    // Fire ready event
    window.dispatchEvent(new CustomEvent('membrane:ready', {
        detail: { membrane, config }
    }));

})();
