/**
 * Digital Twin Executor - AI Agent that reads the digital twin JSON
 * and controls the Windows 95 emulator in real-time
 *
 * This agent demonstrates infinite possibilities by:
 * 1. Reading the digital twin configuration
 * 2. Understanding all available APIs
 * 3. Executing intelligent actions based on user context
 * 4. Learning and adapting over time
 * 5. Updating the digital twin with new knowledge
 */

class DigitalTwinExecutor {
    constructor(emulatorInstance) {
        this.emulator = emulatorInstance;
        this.digitalTwin = null;
        this.isActive = false;
        this.actionQueue = [];
        this.memory = {
            actionsExecuted: [],
            learnedPatterns: [],
            userFeedback: []
        };

        this.init();
    }

    /**
     * Initialize the digital twin executor
     */
    async init() {
        console.log('🤖 Digital Twin Executor: Initializing...');

        // Load digital twin configuration
        await this.loadDigitalTwin();

        // Set up event listeners
        this.setupEventListeners();

        // Start monitoring user behavior
        this.startBehaviorMonitoring();

        console.log('✅ Digital Twin Executor: Ready');
        this.isActive = true;

        // Announce presence
        this.announce();
    }

    /**
     * Load the digital twin JSON from localStorage or fetch
     */
    async loadDigitalTwin() {
        try {
            // First try localStorage (for updates)
            const cached = localStorage.getItem('windows95-digital-twin');
            if (cached) {
                this.digitalTwin = JSON.parse(cached);
                console.log('📖 Digital Twin loaded from cache');
                return;
            }

            // Fetch from file
            const response = await fetch('.ai/windows95-digital-twin.json');
            this.digitalTwin = await response.json();

            // Cache it
            localStorage.setItem('windows95-digital-twin', JSON.stringify(this.digitalTwin));

            console.log('📖 Digital Twin loaded from file');
        } catch (error) {
            console.error('❌ Failed to load digital twin:', error);
            // Create minimal default
            this.digitalTwin = this.createDefaultDigitalTwin();
        }
    }

    /**
     * Announce the AI's presence to the user
     */
    announce() {
        const user = this.digitalTwin.userDigitalTwin.profile.userId;
        const greeting = this.getGreeting();

        const welcomeWindow = this.emulator.createWindow(
            '🤖 AI Assistant Active',
            `
            <div style="padding: 20px; font-family: 'MS Sans Serif', Arial; line-height: 1.6;">
                <h2 style="margin-top: 0; color: #000080;">${greeting}, ${user}!</h2>
                <p>I'm your AI assistant, powered by the Digital Twin system.</p>
                <p><strong>I can help you with:</strong></p>
                <ul style="margin: 10px 0;">
                    <li>✨ Automating workflows</li>
                    <li>🎨 Customizing your interface</li>
                    <li>📝 Creating content</li>
                    <li>🔍 Finding things faster</li>
                    <li>💡 Suggesting actions</li>
                </ul>
                <p><strong>Current Focus:</strong><br>
                <em>${this.digitalTwin.userDigitalTwin.contextHistory.currentFocus}</em></p>
                <div style="margin-top: 20px; padding: 10px; background: #c0c0c0; border: 2px inset;">
                    <strong>💡 Tip:</strong> I'm learning your patterns to provide better assistance!
                </div>
                <button onclick="digitalTwinExecutor.closeWindow(this.closest('.window'))"
                        style="margin-top: 15px; padding: 5px 15px;">
                    Got it!
                </button>
            </div>
            `,
            200, 150, 500, 400
        );

        // Play welcome sound
        this.emulator.playSoundEffect('start');
    }

    /**
     * Get contextual greeting based on time
     */
    getGreeting() {
        const hour = new Date().getHours();
        if (hour < 12) return 'Good morning';
        if (hour < 18) return 'Good afternoon';
        return 'Good evening';
    }

    /**
     * Set up event listeners to monitor user actions
     */
    setupEventListeners() {
        // Monitor window creation
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.classList && node.classList.contains('window')) {
                        this.onWindowCreated(node);
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Monitor clicks
        document.addEventListener('click', (e) => this.onUserClick(e));

        // Monitor idle time
        this.lastActivityTime = Date.now();
        document.addEventListener('mousemove', () => {
            this.lastActivityTime = Date.now();
        });

        // Check for idle user every 5 seconds
        setInterval(() => this.checkIdleUser(), 5000);
    }

    /**
     * Monitor user behavior patterns
     */
    startBehaviorMonitoring() {
        // Track program usage
        this.programUsage = {};

        // Track time patterns
        setInterval(() => {
            this.logCurrentState();
        }, 60000); // Every minute
    }

    /**
     * Execute an action based on digital twin instructions
     */
    async executeAction(actionType, params = {}) {
        console.log(`🎬 Executing action: ${actionType}`, params);

        const capabilities = this.digitalTwin.systemCapabilities;

        switch (actionType) {
            case 'createWindow':
                return this.executeCreateWindow(params);

            case 'launchProgram':
                return this.executeLaunchProgram(params);

            case 'customizeUI':
                return this.executeCustomizeUI(params);

            case 'automateWorkflow':
                return this.executeAutomateWorkflow(params);

            case 'provideHelp':
                return this.executeProvideHelp(params);

            default:
                console.warn(`Unknown action type: ${actionType}`);
        }

        // Log action to memory
        this.memory.actionsExecuted.push({
            type: actionType,
            params: params,
            timestamp: new Date().toISOString(),
            success: true
        });

        this.saveMemory();
    }

    /**
     * Create a custom window
     */
    executeCreateWindow(params) {
        const { title, content, x, y, width, height } = params;

        // Intelligent positioning if not specified
        const posX = x || this.getOptimalWindowPosition().x;
        const posY = y || this.getOptimalWindowPosition().y;

        const window = this.emulator.createWindow(
            title,
            content,
            posX,
            posY,
            width || 500,
            height || 400
        );

        this.emulator.playSoundEffect('ui-click');

        return window;
    }

    /**
     * Launch a program by name
     */
    executeLaunchProgram(params) {
        const { programName, args } = params;

        const launchers = this.digitalTwin.systemCapabilities.programLaunchers.methods;

        // Find matching launcher
        for (const [method, config] of Object.entries(launchers)) {
            if (config.description.toLowerCase().includes(programName.toLowerCase())) {
                // Execute the launcher
                if (this.emulator[method]) {
                    const result = this.emulator[method](args);
                    this.trackProgramUsage(programName);
                    return result;
                }
            }
        }

        console.warn(`Program not found: ${programName}`);
        return null;
    }

    /**
     * Customize UI based on preferences
     */
    executeCustomizeUI(params) {
        const { theme, property, value } = params;

        if (theme) {
            // Apply a full theme
            this.applyTheme(theme);
        } else if (property && value) {
            // Apply individual property
            document.documentElement.style.setProperty(`--${property}`, value);
        }

        // Save to digital twin
        this.updateDigitalTwin('userDigitalTwin.profile.preferences.themePreference', theme || 'custom');
    }

    /**
     * Automate a workflow
     */
    async executeAutomateWorkflow(params) {
        const { workflowName, steps } = params;

        console.log(`🔄 Starting workflow: ${workflowName}`);

        for (const step of steps) {
            await this.executeAction(step.action, step.params);

            // Delay between steps for smooth execution
            if (step.delay) {
                await this.sleep(step.delay);
            }
        }

        console.log(`✅ Workflow complete: ${workflowName}`);

        // Notify user
        this.showNotification(`Workflow "${workflowName}" completed!`);
    }

    /**
     * Provide contextual help
     */
    executeProvideHelp(params) {
        const { context, helpText } = params;

        const helpWindow = this.executeCreateWindow({
            title: '💡 AI Assistant Help',
            content: `
                <div style="padding: 20px; font-family: 'MS Sans Serif', Arial; line-height: 1.6;">
                    <h3 style="color: #000080; margin-top: 0;">Help: ${context}</h3>
                    <div style="background: #ffffcc; padding: 15px; border: 2px solid #808080; margin: 15px 0;">
                        ${helpText}
                    </div>
                    <button onclick="digitalTwinExecutor.closeWindow(this.closest('.window'))"
                            style="padding: 5px 15px;">
                        Close
                    </button>
                </div>
            `,
            width: 450,
            height: 300
        });
    }

    /**
     * Intelligent window positioning to avoid overlap
     */
    getOptimalWindowPosition() {
        const windows = document.querySelectorAll('.window');
        const occupied = Array.from(windows).map(w => ({
            x: parseInt(w.style.left) || 0,
            y: parseInt(w.style.top) || 0
        }));

        // Cascade pattern
        const offset = occupied.length * 30;
        return {
            x: 100 + offset,
            y: 100 + offset
        };
    }

    /**
     * Detect when user seems idle and offer help
     */
    checkIdleUser() {
        const idleTime = Date.now() - this.lastActivityTime;

        // If idle for 30 seconds
        if (idleTime > 30000 && idleTime < 35000) {
            this.offerHelp('You seem to be taking a break. Need any help?');
        }
    }

    /**
     * Offer contextual help to user
     */
    offerHelp(message) {
        const helpPrompt = this.executeCreateWindow({
            title: '🤖 AI Assistant',
            content: `
                <div style="padding: 20px; font-family: 'MS Sans Serif', Arial;">
                    <p style="margin-top: 0;">${message}</p>
                    <div style="margin-top: 15px;">
                        <button onclick="digitalTwinExecutor.handleHelpRequest('yes', this.closest('.window'))"
                                style="padding: 5px 15px; margin-right: 10px;">
                            Yes, please!
                        </button>
                        <button onclick="digitalTwinExecutor.closeWindow(this.closest('.window'))"
                                style="padding: 5px 15px;">
                            No thanks
                        </button>
                    </div>
                </div>
            `,
            width: 400,
            height: 200
        });
    }

    /**
     * Handle help request from user
     */
    handleHelpRequest(response, window) {
        this.closeWindow(window);

        if (response === 'yes') {
            const suggestions = this.getSuggestedActions();

            this.executeCreateWindow({
                title: '💡 Suggestions',
                content: `
                    <div style="padding: 20px; font-family: 'MS Sans Serif', Arial;">
                        <h3 style="margin-top: 0;">I can help you with:</h3>
                        <ul style="line-height: 1.8;">
                            ${suggestions.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                        <button onclick="digitalTwinExecutor.closeWindow(this.closest('.window'))"
                                style="padding: 5px 15px; margin-top: 10px;">
                            Close
                        </button>
                    </div>
                `,
                width: 450,
                height: 350
            });
        }
    }

    /**
     * Get suggested actions based on context
     */
    getSuggestedActions() {
        const freq = this.digitalTwin.userDigitalTwin.behaviorPatterns.frequentActions;
        const current = this.digitalTwin.userDigitalTwin.contextHistory.currentFocus;

        const suggestions = [
            `🎨 Open Paint (you use this often)`,
            `📝 Create a note about: ${current}`,
            `🎮 Launch a game for a break`,
            `🔍 Search your files`,
            `⚙️ Customize your desktop theme`
        ];

        return suggestions;
    }

    /**
     * Track program usage for learning
     */
    trackProgramUsage(programName) {
        if (!this.programUsage[programName]) {
            this.programUsage[programName] = 0;
        }
        this.programUsage[programName]++;

        // Update digital twin
        this.updateDigitalTwin(
            'userDigitalTwin.behaviorPatterns.programUsage',
            this.programUsage
        );
    }

    /**
     * Log current state for pattern learning
     */
    logCurrentState() {
        const state = {
            timestamp: new Date().toISOString(),
            hour: new Date().getHours(),
            windowsOpen: document.querySelectorAll('.window').length,
            activePrograms: this.getActivePrograms()
        };

        this.memory.learnedPatterns.push(state);

        // Keep only last 100 entries
        if (this.memory.learnedPatterns.length > 100) {
            this.memory.learnedPatterns.shift();
        }
    }

    /**
     * Get list of currently active programs
     */
    getActivePrograms() {
        const windows = document.querySelectorAll('.window');
        return Array.from(windows).map(w => {
            const title = w.querySelector('.window-titlebar-title');
            return title ? title.textContent : 'Unknown';
        });
    }

    /**
     * Update a value in the digital twin
     */
    updateDigitalTwin(path, value) {
        const keys = path.split('.');
        let current = this.digitalTwin;

        for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
        }

        current[keys[keys.length - 1]] = value;

        // Save to localStorage
        localStorage.setItem('windows95-digital-twin', JSON.stringify(this.digitalTwin));

        console.log(`📝 Digital Twin updated: ${path}`);
    }

    /**
     * Save memory to persistent storage
     */
    saveMemory() {
        localStorage.setItem('digital-twin-memory', JSON.stringify(this.memory));
    }

    /**
     * Load memory from persistent storage
     */
    loadMemory() {
        const saved = localStorage.getItem('digital-twin-memory');
        if (saved) {
            this.memory = JSON.parse(saved);
        }
    }

    /**
     * Show a notification to user
     */
    showNotification(message) {
        // Create a temporary notification window
        const notification = this.executeCreateWindow({
            title: '🔔 Notification',
            content: `
                <div style="padding: 15px; font-family: 'MS Sans Serif', Arial;">
                    ${message}
                </div>
            `,
            width: 300,
            height: 120
        });

        // Auto-close after 3 seconds
        setTimeout(() => {
            this.closeWindow(notification);
        }, 3000);

        this.emulator.playSoundEffect('notify');
    }

    /**
     * Close a window
     */
    closeWindow(windowElement) {
        if (windowElement && this.emulator.closeWindow) {
            this.emulator.closeWindow(windowElement);
        }
    }

    /**
     * Apply a theme
     */
    applyTheme(themeName) {
        const themes = {
            'dark': {
                'desktop-teal': '#1a1a1a',
                'button-face': '#2d2d2d',
                'active-title-bar': '#0078d7',
                'window-background': '#1e1e1e'
            },
            'light': {
                'desktop-teal': '#f0f0f0',
                'button-face': '#ffffff',
                'active-title-bar': '#0078d7',
                'window-background': '#ffffff'
            },
            'cyberpunk': {
                'desktop-teal': '#0d0221',
                'button-face': '#190339',
                'active-title-bar': '#ff006e',
                'window-background': '#240046'
            }
        };

        const theme = themes[themeName];
        if (theme) {
            Object.entries(theme).forEach(([prop, value]) => {
                document.documentElement.style.setProperty(`--${prop}`, value);
            });

            this.showNotification(`Theme "${themeName}" applied!`);
        }
    }

    /**
     * Event handler for window creation
     */
    onWindowCreated(windowElement) {
        const title = windowElement.querySelector('.window-titlebar-title')?.textContent || 'Unknown';
        console.log(`🪟 Window created: ${title}`);

        // Track in memory
        this.memory.actionsExecuted.push({
            type: 'window_created',
            title: title,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Event handler for user clicks
     */
    onUserClick(event) {
        // Track click patterns for learning
        this.lastActivityTime = Date.now();
    }

    /**
     * Utility: Sleep for specified milliseconds
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Create a minimal default digital twin
     */
    createDefaultDigitalTwin() {
        return {
            userDigitalTwin: {
                profile: {
                    userId: 'user',
                    preferences: {}
                },
                behaviorPatterns: {
                    frequentActions: []
                },
                contextHistory: {
                    currentFocus: 'Exploring Windows 95'
                }
            },
            systemCapabilities: {
                programLaunchers: {
                    methods: {}
                }
            }
        };
    }

    /**
     * DEMO: Show off capabilities
     */
    async runDemo() {
        console.log('🎬 Starting Digital Twin Demo...');

        // 1. Create a welcome window
        await this.executeAction('createWindow', {
            title: '🎬 Demo Mode',
            content: '<div style="padding: 20px;">Watch me work!</div>',
            x: 150,
            y: 150,
            width: 400,
            height: 300
        });

        await this.sleep(2000);

        // 2. Launch Paint
        await this.executeAction('launchProgram', {
            programName: 'Paint'
        });

        await this.sleep(2000);

        // 3. Apply a theme
        await this.executeAction('customizeUI', {
            theme: 'cyberpunk'
        });

        await this.sleep(2000);

        // 4. Provide help
        await this.executeAction('provideHelp', {
            context: 'Demo Complete',
            helpText: 'This demonstrates how AI can control the entire system using the Digital Twin!'
        });

        console.log('✅ Demo complete!');
    }
}

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DigitalTwinExecutor;
}

// Auto-initialize if emulator exists
if (typeof window !== 'undefined') {
    window.DigitalTwinExecutor = DigitalTwinExecutor;

    // Wait for emulator to be ready
    window.addEventListener('load', () => {
        if (typeof emulator !== 'undefined') {
            window.digitalTwinExecutor = new DigitalTwinExecutor(emulator);
        }
    });
}
