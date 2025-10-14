/**
 * Data Sloshing Pipeline
 *
 * ULTRA THINK: Pure data-driven computing
 *
 * This is the master coordinator that creates a bidirectional data flow:
 *
 *    Emulator State
 *         ↓
 *    JSON Export (current state)
 *         ↓
 *    AI Analysis (optional)
 *         ↓
 *    JSON Instructions (static or AI-generated)
 *         ↓
 *    Instruction Executor
 *         ↓
 *    Emulator State (updated)
 *         ↓
 *    [LOOP INFINITELY]
 *
 * The beautiful part: NO CODE CHANGES NEEDED.
 * Everything flows through JSON. The system self-modifies through data.
 */

class DataSloshPipeline {
    constructor(emulator) {
        this.emulator = emulator;
        this.statePersistence = null;
        this.instructionExecutor = null;
        this.isRunning = false;
        this.sloshInterval = null;
        this.config = this.loadConfig();

        this.init();
    }

    async init() {
        console.log('🌊 Data Slosh Pipeline: Initializing...');

        // Initialize components
        this.statePersistence = new StatePersistence(this.emulator);
        this.instructionExecutor = new InstructionExecutor(this.emulator, this.statePersistence);

        // Wait for components to be ready
        await this.sleep(1000);

        // Set up the data flow
        this.setupDataFlow();

        // Expose global API
        this.exposeAPI();

        console.log('✅ Data Slosh Pipeline: Active');
        console.log('💡 Data is flowing! State ↔️ Instructions ↔️ Execution');
    }

    /**
     * Load pipeline configuration
     */
    loadConfig() {
        const defaults = {
            autoSloshInterval: 60000, // Slosh every 60 seconds
            maxStateSize: 5 * 1024 * 1024, // 5MB
            enableAutoGeneration: true, // Auto-generate instructions from patterns
            enableTimeTriggers: true, // Execute scheduled instructions
            enableStateTriggers: true, // Execute instructions based on state conditions
            exportPath: '.ai/generated/',
            verbose: true
        };

        const saved = localStorage.getItem('data_slosh_config');
        return saved ? { ...defaults, ...JSON.parse(saved) } : defaults;
    }

    /**
     * Save configuration
     */
    saveConfig() {
        localStorage.setItem('data_slosh_config', JSON.stringify(this.config));
    }

    /**
     * Set up the data flow pipeline
     */
    setupDataFlow() {
        // Phase 1: State → JSON (capture)
        this.statePersistence.startAutoSave();

        // Phase 2: JSON → Analysis (detect patterns)
        if (this.config.enableAutoGeneration) {
            this.startPatternDetection();
        }

        // Phase 3: Analysis → Instructions (generate)
        if (this.config.enableAutoGeneration) {
            this.startInstructionGeneration();
        }

        // Phase 4: Instructions → Execution (run)
        if (this.config.enableTimeTriggers) {
            this.instructionExecutor.setupTriggers();
        }

        // Phase 5: State Triggers (reactive)
        if (this.config.enableStateTriggers) {
            this.startStateTriggers();
        }

        // Start the main slosh loop
        this.startSloshing();
    }

    /**
     * Start the main data sloshing loop
     */
    startSloshing() {
        if (this.isRunning) return;

        this.isRunning = true;

        this.sloshInterval = setInterval(async () => {
            await this.slosh();
        }, this.config.autoSloshInterval);

        console.log(`🌊 Sloshing started (every ${this.config.autoSloshInterval/1000}s)`);
    }

    /**
     * Stop sloshing
     */
    stopSloshing() {
        if (this.sloshInterval) {
            clearInterval(this.sloshInterval);
            this.sloshInterval = null;
        }
        this.isRunning = false;
        console.log('🛑 Sloshing stopped');
    }

    /**
     * One complete slosh cycle
     */
    async slosh() {
        if (this.config.verbose) {
            console.log('🌊 SLOSH: Starting cycle...');
        }

        // 1. Capture current state
        const state = this.statePersistence.captureState();

        // 2. Analyze state for patterns
        const patterns = this.analyzePatterns(state);

        // 3. Generate instructions if patterns detected
        if (patterns.length > 0 && this.config.enableAutoGeneration) {
            patterns.forEach(pattern => {
                this.generateInstructionFromPattern(pattern);
            });
        }

        // 4. Check for state-triggered instructions
        if (this.config.enableStateTriggers) {
            this.checkStateTriggers(state);
        }

        // 5. Export state for external consumption
        await this.exportStateData(state);

        if (this.config.verbose) {
            console.log('✅ SLOSH: Cycle complete');
            console.log(`   Windows: ${state.windows.length}`);
            console.log(`   Icons: ${state.icons.length}`);
            console.log(`   Patterns detected: ${patterns.length}`);
        }
    }

    /**
     * Analyze state for patterns
     */
    analyzePatterns(state) {
        const patterns = [];

        // Pattern: Too many windows open
        if (state.windows.length > 8) {
            patterns.push({
                type: 'too_many_windows',
                description: 'User has too many windows open',
                suggestedAction: 'cleanup-workspace'
            });
        }

        // Pattern: Windows overlapping significantly
        const overlapping = this.detectOverlappingWindows(state.windows);
        if (overlapping > 5) {
            patterns.push({
                type: 'overlapping_windows',
                description: 'Many windows are overlapping',
                suggestedAction: 'cascade-windows'
            });
        }

        // Pattern: All windows minimized (user might be lost)
        if (state.windows.every(w => w.minimized)) {
            patterns.push({
                type: 'all_minimized',
                description: 'All windows are minimized',
                suggestedAction: 'restore-workspace'
            });
        }

        // Pattern: Desktop icons disorganized
        if (this.detectDisorganizedIcons(state.icons)) {
            patterns.push({
                type: 'disorganized_icons',
                description: 'Desktop icons are scattered',
                suggestedAction: 'organize-icons'
            });
        }

        return patterns;
    }

    /**
     * Detect overlapping windows
     */
    detectOverlappingWindows(windows) {
        let overlappingCount = 0;

        for (let i = 0; i < windows.length; i++) {
            for (let j = i + 1; j < windows.length; j++) {
                if (this.windowsOverlap(windows[i], windows[j])) {
                    overlappingCount++;
                }
            }
        }

        return overlappingCount;
    }

    /**
     * Check if two windows overlap
     */
    windowsOverlap(win1, win2) {
        const x1 = win1.position.x;
        const y1 = win1.position.y;
        const w1 = win1.size.width;
        const h1 = win1.size.height;

        const x2 = win2.position.x;
        const y2 = win2.position.y;
        const w2 = win2.size.width;
        const h2 = win2.size.height;

        return !(x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
    }

    /**
     * Detect if icons are disorganized
     */
    detectDisorganizedIcons(icons) {
        if (icons.length < 3) return false;

        // Check if icons follow a grid pattern
        const gridSize = 80;
        const alignedIcons = icons.filter(icon => {
            const xAligned = icon.position.x % gridSize < 10;
            const yAligned = icon.position.y % gridSize < 10;
            return xAligned && yAligned;
        });

        return alignedIcons.length / icons.length < 0.5; // Less than 50% aligned
    }

    /**
     * Generate instruction from detected pattern
     */
    generateInstructionFromPattern(pattern) {
        const instructionName = `auto-${pattern.type}-${Date.now()}`;

        const instruction = {
            name: instructionName,
            description: `Auto-generated: ${pattern.description}`,
            version: '1.0.0',
            author: 'data-slosh-pipeline',
            createdAt: new Date().toISOString(),
            pattern: pattern.type,
            steps: this.getStepsForPattern(pattern)
        };

        // Save the generated instruction
        this.instructionExecutor.generateInstruction(instruction);

        console.log(`✨ Auto-generated instruction: ${instructionName}`);

        // Optionally execute immediately
        if (this.config.autoExecuteGenerated) {
            this.instructionExecutor.execute(instructionName);
        }
    }

    /**
     * Get steps for a specific pattern
     */
    getStepsForPattern(pattern) {
        switch (pattern.type) {
            case 'too_many_windows':
                return [
                    {
                        type: 'notification',
                        params: {
                            title: '🧹 Too Many Windows',
                            message: 'You have many windows open. Would you like to organize them?'
                        }
                    },
                    {
                        type: 'wait',
                        params: { duration: 2000 }
                    },
                    {
                        type: 'cascadeWindows',
                        params: { startX: 50, startY: 50, offsetX: 30, offsetY: 30 }
                    }
                ];

            case 'overlapping_windows':
                return [
                    {
                        type: 'tileWindows',
                        params: { padding: 10 }
                    },
                    {
                        type: 'notification',
                        params: {
                            title: '✨ Windows Tiled',
                            message: 'Your windows have been arranged for better visibility'
                        }
                    }
                ];

            case 'disorganized_icons':
                return [
                    {
                        type: 'organizeIcons',
                        params: { startX: 20, startY: 20, spacing: 80, columns: 4 }
                    },
                    {
                        type: 'notification',
                        params: {
                            title: '📐 Icons Organized',
                            message: 'Desktop icons have been arranged in a grid'
                        }
                    }
                ];

            default:
                return [];
        }
    }

    /**
     * Check for state-triggered instructions
     */
    checkStateTriggers(state) {
        // Example: If user opens Notepad at 9am, suggest morning routine
        const hour = new Date().getHours();
        const hasNotepad = state.windows.some(w => w.title.includes('Notepad'));

        if (hour === 9 && hasNotepad && !this.hasExecutedToday('morning-routine')) {
            this.instructionExecutor.execute('morning-routine');
        }

        // Example: If more than 10 windows, suggest cleanup
        if (state.windows.length > 10) {
            const lastCleanup = localStorage.getItem('last_cleanup_timestamp');
            const hoursSinceCleanup = (Date.now() - (parseInt(lastCleanup) || 0)) / 3600000;

            if (hoursSinceCleanup > 1) {
                this.instructionExecutor.execute('cleanup-workspace');
                localStorage.setItem('last_cleanup_timestamp', Date.now());
            }
        }
    }

    /**
     * Check if instruction has been executed today
     */
    hasExecutedToday(instructionName) {
        const key = `executed_today_${instructionName}`;
        const lastExecuted = localStorage.getItem(key);

        if (!lastExecuted) return false;

        const lastDate = new Date(parseInt(lastExecuted));
        const today = new Date();

        return lastDate.toDateString() === today.toDateString();
    }

    /**
     * Start pattern detection
     */
    startPatternDetection() {
        // Patterns are detected during each slosh cycle
        console.log('🔍 Pattern detection enabled');
    }

    /**
     * Start instruction generation
     */
    startInstructionGeneration() {
        // Instructions are generated when patterns are detected
        console.log('✨ Auto-generation enabled');
    }

    /**
     * Start state triggers
     */
    startStateTriggers() {
        // State triggers are checked during each slosh cycle
        console.log('⚡ State triggers enabled');
    }

    /**
     * Export state data for external consumption
     */
    async exportStateData(state) {
        // Export to localStorage for easy access
        localStorage.setItem('windows95_latest_state', JSON.stringify(state));

        // Generate downloadable JSON (optional)
        if (this.config.exportToFile) {
            await this.statePersistence.generateStateJSON(state);
        }
    }

    /**
     * Expose global API
     */
    exposeAPI() {
        window.dataSloshPipeline = this;

        // Convenience methods
        window.slosh = () => this.slosh();
        window.startSloshing = () => this.startSloshing();
        window.stopSloshing = () => this.stopSloshing();
        window.getLatestState = () => JSON.parse(localStorage.getItem('windows95_latest_state') || '{}');
        window.exportState = () => this.statePersistence.exportState();
        window.importState = (json) => this.statePersistence.importState(json);
        window.executeInstruction = (name) => this.instructionExecutor.execute(name);
        window.listInstructions = () => this.instructionExecutor.listAvailable();
        window.generateInstruction = (config) => this.instructionExecutor.generateInstruction(config);

        console.log('🌐 Global API exposed:');
        console.log('   slosh() - Run one slosh cycle');
        console.log('   startSloshing() - Start auto-sloshing');
        console.log('   stopSloshing() - Stop auto-sloshing');
        console.log('   getLatestState() - Get current state');
        console.log('   exportState() - Download state JSON');
        console.log('   importState(json) - Import state from JSON');
        console.log('   executeInstruction(name) - Run an instruction');
        console.log('   listInstructions() - See all instructions');
        console.log('   generateInstruction(config) - Create new instruction');
    }

    /**
     * Get pipeline status
     */
    getStatus() {
        return {
            isRunning: this.isRunning,
            config: this.config,
            components: {
                statePersistence: !!this.statePersistence,
                instructionExecutor: !!this.instructionExecutor
            },
            stats: {
                stateHistory: this.statePersistence?.getStateHistory?.length || 0,
                executionHistory: this.instructionExecutor?.executionHistory?.length || 0
            }
        };
    }

    /**
     * Utility: Sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Auto-initialize when loaded
if (typeof window !== 'undefined') {
    window.DataSloshPipeline = DataSloshPipeline;

    // Auto-start when emulator is ready
    window.addEventListener('load', () => {
        if (typeof emulator !== 'undefined') {
            window.dataSloshPipeline = new DataSloshPipeline(emulator);
        }
    });
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataSloshPipeline;
}
