/**
 * Windows 95 Static Instruction Executor
 *
 * ULTRA THINK: Autonomous task execution through pure data
 * - Reads JSON instruction files
 * - Executes tasks WITHOUT AI in the loop
 * - Self-generating: can create new instruction files
 * - Data sloshing: instructions → execution → state → new instructions
 *
 * Think of this like Minecraft command blocks or Docker Compose:
 * You define what you want in JSON, and it happens automatically.
 */

class InstructionExecutor {
    constructor(emulator, statePersistence) {
        this.emulator = emulator;
        this.statePersistence = statePersistence;
        this.instructionsPath = '.ai/static-instructions/';
        this.loadedInstructions = new Map();
        this.executionHistory = [];
        this.maxHistorySize = 100;

        this.init();
    }

    async init() {
        console.log('🤖 Instruction Executor: Initializing...');

        // Load available instruction files
        await this.discoverInstructions();

        // Set up triggers
        this.setupTriggers();

        // Expose API
        window.executeInstruction = (name) => this.execute(name);
        window.listInstructions = () => this.listAvailable();

        console.log('✅ Instruction Executor: Ready');
        console.log('💡 Type executeInstruction("name") to run a script');
    }

    /**
     * Discover all available instruction files
     */
    async discoverInstructions() {
        // In a real implementation, this would scan the directory
        // For now, we'll load known instruction files

        const knownInstructions = [
            'morning-routine.json',
            'focus-mode.json',
            'cleanup-workspace.json',
            'demo-showcase.json',
            'auto-organize.json'
        ];

        for (const filename of knownInstructions) {
            try {
                const response = await fetch(this.instructionsPath + filename);
                if (response.ok) {
                    const instruction = await response.json();
                    this.loadedInstructions.set(instruction.name, instruction);
                    console.log(`📜 Loaded instruction: ${instruction.name}`);
                }
            } catch (e) {
                // File doesn't exist yet, that's ok
            }
        }

        // Also check localStorage for dynamically generated instructions
        this.loadDynamicInstructions();
    }

    /**
     * Load dynamically generated instructions from localStorage
     */
    loadDynamicInstructions() {
        const dynamic = localStorage.getItem('windows95_dynamic_instructions');
        if (dynamic) {
            try {
                const instructions = JSON.parse(dynamic);
                Object.entries(instructions).forEach(([name, instruction]) => {
                    this.loadedInstructions.set(name, instruction);
                    console.log(`📜 Loaded dynamic instruction: ${name}`);
                });
            } catch (e) {
                console.warn('Failed to load dynamic instructions:', e);
            }
        }
    }

    /**
     * Execute an instruction by name
     */
    async execute(instructionName) {
        const instruction = this.loadedInstructions.get(instructionName);

        if (!instruction) {
            console.error(`Instruction not found: ${instructionName}`);
            return false;
        }

        console.log(`🚀 Executing instruction: ${instructionName}`);

        const startTime = Date.now();
        const result = {
            name: instructionName,
            startTime,
            steps: [],
            success: true,
            error: null
        };

        try {
            // Execute each step in sequence
            for (const step of instruction.steps) {
                const stepResult = await this.executeStep(step);
                result.steps.push(stepResult);

                if (!stepResult.success && step.required !== false) {
                    result.success = false;
                    result.error = stepResult.error;
                    break;
                }

                // Wait between steps if specified
                if (step.delay) {
                    await this.sleep(step.delay);
                }
            }

            result.endTime = Date.now();
            result.duration = result.endTime - result.startTime;

            console.log(`✅ Instruction completed: ${instructionName} (${result.duration}ms)`);
        } catch (error) {
            result.success = false;
            result.error = error.message;
            console.error(`❌ Instruction failed: ${instructionName}`, error);
        }

        // Record execution
        this.recordExecution(result);

        // Save state after execution
        if (instruction.saveStateAfter !== false) {
            await this.statePersistence.saveState();
        }

        return result;
    }

    /**
     * Execute a single step
     */
    async executeStep(step) {
        const result = {
            type: step.type,
            success: false,
            error: null,
            output: null
        };

        try {
            switch (step.type) {
                case 'openProgram':
                    result.output = await this.stepOpenProgram(step.params);
                    break;

                case 'createWindow':
                    result.output = await this.stepCreateWindow(step.params);
                    break;

                case 'closeWindow':
                    result.output = await this.stepCloseWindow(step.params);
                    break;

                case 'moveWindow':
                    result.output = await this.stepMoveWindow(step.params);
                    break;

                case 'resizeWindow':
                    result.output = await this.stepResizeWindow(step.params);
                    break;

                case 'minimizeAll':
                    result.output = await this.stepMinimizeAll(step.params);
                    break;

                case 'cascadeWindows':
                    result.output = await this.stepCascadeWindows(step.params);
                    break;

                case 'tileWindows':
                    result.output = await this.stepTileWindows(step.params);
                    break;

                case 'executeScript':
                    result.output = await this.stepExecuteScript(step.params);
                    break;

                case 'playSound':
                    result.output = await this.stepPlaySound(step.params);
                    break;

                case 'notification':
                    result.output = await this.stepNotification(step.params);
                    break;

                case 'setTheme':
                    result.output = await this.stepSetTheme(step.params);
                    break;

                case 'organizeIcons':
                    result.output = await this.stepOrganizeIcons(step.params);
                    break;

                case 'wait':
                    result.output = await this.stepWait(step.params);
                    break;

                default:
                    throw new Error(`Unknown step type: ${step.type}`);
            }

            result.success = true;
        } catch (error) {
            result.error = error.message;
            console.error(`Step failed (${step.type}):`, error);
        }

        return result;
    }

    // ===== STEP IMPLEMENTATIONS =====

    async stepOpenProgram(params) {
        const { program } = params;
        const methodName = `open${program}`;

        if (this.emulator[methodName]) {
            const window = this.emulator[methodName]();
            return { windowId: window?.dataset?.windowId || window?.id };
        } else {
            throw new Error(`Program not found: ${program}`);
        }
    }

    async stepCreateWindow(params) {
        const { title, content, width, height, x, y } = params;
        const window = this.emulator.createWindow(title, content, width, height, x, y);
        return { windowId: window?.dataset?.windowId || window?.id };
    }

    async stepCloseWindow(params) {
        const { windowId, selector } = params;

        if (windowId) {
            const window = document.querySelector(`[data-window-id="${windowId}"]`);
            if (window) {
                this.emulator.closeWindow(window);
                return { closed: true };
            }
        } else if (selector) {
            const window = document.querySelector(selector);
            if (window) {
                this.emulator.closeWindow(window);
                return { closed: true };
            }
        }

        throw new Error('Window not found');
    }

    async stepMoveWindow(params) {
        const { windowId, x, y } = params;
        const window = document.querySelector(`[data-window-id="${windowId}"]`);

        if (window) {
            window.style.left = x + 'px';
            window.style.top = y + 'px';
            window.style.transition = 'left 0.3s ease, top 0.3s ease';
            return { moved: true, position: { x, y } };
        }

        throw new Error('Window not found');
    }

    async stepResizeWindow(params) {
        const { windowId, width, height } = params;
        const window = document.querySelector(`[data-window-id="${windowId}"]`);

        if (window) {
            window.style.width = width + 'px';
            window.style.height = height + 'px';
            window.style.transition = 'width 0.3s ease, height 0.3s ease';
            return { resized: true, size: { width, height } };
        }

        throw new Error('Window not found');
    }

    async stepMinimizeAll(params) {
        const windows = document.querySelectorAll('.window');
        windows.forEach(w => {
            if (this.emulator.minimizeWindow) {
                this.emulator.minimizeWindow(w);
            } else {
                w.classList.add('minimized');
                w.style.display = 'none';
            }
        });

        return { minimized: windows.length };
    }

    async stepCascadeWindows(params) {
        const windows = Array.from(document.querySelectorAll('.window'));
        const { startX = 50, startY = 50, offsetX = 30, offsetY = 30 } = params;

        windows.forEach((window, i) => {
            window.style.left = (startX + i * offsetX) + 'px';
            window.style.top = (startY + i * offsetY) + 'px';
            window.style.transition = 'left 0.5s ease, top 0.5s ease';
        });

        return { cascaded: windows.length };
    }

    async stepTileWindows(params) {
        const windows = Array.from(document.querySelectorAll('.window'));
        const { padding = 10 } = params;

        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight - 60; // Account for taskbar

        const cols = Math.ceil(Math.sqrt(windows.length));
        const rows = Math.ceil(windows.length / cols);

        const windowWidth = (screenWidth / cols) - (padding * 2);
        const windowHeight = (screenHeight / rows) - (padding * 2);

        windows.forEach((window, i) => {
            const col = i % cols;
            const row = Math.floor(i / cols);

            window.style.left = (col * (windowWidth + padding * 2) + padding) + 'px';
            window.style.top = (row * (windowHeight + padding * 2) + padding) + 'px';
            window.style.width = windowWidth + 'px';
            window.style.height = windowHeight + 'px';
            window.style.transition = 'all 0.5s ease';
        });

        return { tiled: windows.length, grid: `${cols}x${rows}` };
    }

    async stepExecuteScript(params) {
        const { code } = params;
        const result = eval(code);
        return { result };
    }

    async stepPlaySound(params) {
        const { sound } = params;
        if (this.emulator.playSoundEffect) {
            this.emulator.playSoundEffect(sound);
            return { played: sound };
        }
        throw new Error('Sound system not available');
    }

    async stepNotification(params) {
        const { message, title = 'Notification', x, y } = params;

        const notification = this.emulator.createWindow(
            title,
            `<div style="padding: 20px;">${message}</div>`,
            300,
            150,
            x || window.innerWidth - 350,
            y || 50
        );

        // Auto-close after 3 seconds
        setTimeout(() => {
            if (notification) {
                this.emulator.closeWindow(notification);
            }
        }, 3000);

        return { shown: true };
    }

    async stepSetTheme(params) {
        const { theme } = params;
        document.documentElement.dataset.theme = theme;
        return { theme };
    }

    async stepOrganizeIcons(params) {
        const icons = Array.from(document.querySelectorAll('.desktop-icon'));
        const { startX = 20, startY = 20, spacing = 80, columns = 4 } = params;

        icons.forEach((icon, i) => {
            const col = i % columns;
            const row = Math.floor(i / columns);

            icon.style.left = (startX + col * spacing) + 'px';
            icon.style.top = (startY + row * spacing) + 'px';
            icon.style.transition = 'all 0.5s ease';
        });

        return { organized: icons.length };
    }

    async stepWait(params) {
        const { duration } = params;
        await this.sleep(duration);
        return { waited: duration };
    }

    // ===== HELPERS =====

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Set up event-based triggers
     */
    setupTriggers() {
        // Trigger instructions on specific events
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+F = Focus mode
            if (e.ctrlKey && e.shiftKey && e.key === 'F') {
                e.preventDefault();
                this.execute('focus-mode');
            }

            // Ctrl+Shift+C = Cleanup workspace
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                this.execute('cleanup-workspace');
            }

            // Ctrl+Shift+M = Morning routine
            if (e.ctrlKey && e.shiftKey && e.key === 'M') {
                e.preventDefault();
                this.execute('morning-routine');
            }
        });

        // Time-based triggers
        this.checkScheduledInstructions();
        setInterval(() => this.checkScheduledInstructions(), 60000); // Check every minute
    }

    /**
     * Check if any instructions should run based on schedule
     */
    checkScheduledInstructions() {
        const now = new Date();
        const hour = now.getHours();
        const minute = now.getMinutes();
        const timeString = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;

        this.loadedInstructions.forEach((instruction, name) => {
            if (instruction.schedule === timeString) {
                console.log(`⏰ Scheduled execution: ${name}`);
                this.execute(name);
            }
        });
    }

    /**
     * Record execution in history
     */
    recordExecution(result) {
        this.executionHistory.push(result);

        // Prune history
        if (this.executionHistory.length > this.maxHistorySize) {
            this.executionHistory.shift();
        }

        // Save to localStorage
        localStorage.setItem('windows95_execution_history', JSON.stringify(this.executionHistory));
    }

    /**
     * List all available instructions
     */
    listAvailable() {
        const instructions = Array.from(this.loadedInstructions.values()).map(inst => ({
            name: inst.name,
            description: inst.description,
            steps: inst.steps.length,
            schedule: inst.schedule || 'manual'
        }));

        console.table(instructions);
        return instructions;
    }

    /**
     * Generate a new instruction file (self-generating)
     */
    generateInstruction(config) {
        const instruction = {
            name: config.name,
            description: config.description || `Generated instruction: ${config.name}`,
            version: '1.0.0',
            author: 'auto-generated',
            createdAt: new Date().toISOString(),
            schedule: config.schedule || null,
            saveStateAfter: config.saveStateAfter !== false,
            steps: config.steps || []
        };

        // Save to localStorage (dynamic instructions)
        const dynamic = JSON.parse(localStorage.getItem('windows95_dynamic_instructions') || '{}');
        dynamic[instruction.name] = instruction;
        localStorage.setItem('windows95_dynamic_instructions', JSON.stringify(dynamic));

        // Add to loaded instructions
        this.loadedInstructions.set(instruction.name, instruction);

        console.log(`✨ Generated new instruction: ${instruction.name}`);

        // Also export as downloadable JSON
        this.exportInstruction(instruction);

        return instruction;
    }

    /**
     * Export instruction as JSON file
     */
    exportInstruction(instruction) {
        const json = JSON.stringify(instruction, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `${instruction.name}.json`;
        a.style.display = 'none';
        document.body.appendChild(a);

        console.log(`📥 Instruction available for download: ${instruction.name}.json`);
        console.log('💡 Call a.click() to download');

        // Store reference for manual download
        window.__generatedInstructionDownload = a;
    }

    /**
     * Get execution statistics
     */
    getStats() {
        const stats = {
            totalExecutions: this.executionHistory.length,
            successRate: (this.executionHistory.filter(r => r.success).length / this.executionHistory.length * 100).toFixed(2) + '%',
            avgDuration: (this.executionHistory.reduce((sum, r) => sum + (r.duration || 0), 0) / this.executionHistory.length).toFixed(0) + 'ms',
            mostUsed: null
        };

        // Find most used instruction
        const usage = {};
        this.executionHistory.forEach(r => {
            usage[r.name] = (usage[r.name] || 0) + 1;
        });

        const mostUsed = Object.entries(usage).sort((a, b) => b[1] - a[1])[0];
        stats.mostUsed = mostUsed ? `${mostUsed[0]} (${mostUsed[1]}x)` : 'none';

        return stats;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InstructionExecutor;
}

if (typeof window !== 'undefined') {
    window.InstructionExecutor = InstructionExecutor;
}
