/**
 * LocalFirst Command Parser
 * Parses natural language text commands and maps them to emulator actions
 *
 * Features:
 * - Exact pattern matching
 * - Fuzzy matching for typos
 * - Alias support
 * - Filler word removal
 * - Command suggestions
 * - Learning from usage
 *
 * Usage:
 * const parser = new CommandParser(emulator);
 * await parser.init(); // Loads command mappings
 * const result = parser.parse("open notepad");
 * if (result.success) result.execute();
 */

class CommandParser {
    constructor(emulator) {
        this.emulator = emulator;
        this.mappings = null;
        this.commandIndex = new Map();
        this.usageStats = new Map();
        this.fillerWords = [];

        // Performance: Cache compiled patterns
        this.patternCache = new Map();
    }

    /**
     * Initialize parser by loading command mappings
     */
    async init() {
        try {
            // Load command mappings
            const response = await fetch('.ai/command-mappings.json');
            this.mappings = await response.json();

            // Build command index for fast lookup
            this.buildCommandIndex();

            // Extract filler words
            const rules = this.mappings.parsingRules.rules.find(r => r.name === 'Ignore filler words');
            this.fillerWords = rules?.fillerWords || [];

            console.log('[CommandParser] Initialized with', this.commandIndex.size, 'commands');

            return true;
        } catch (error) {
            console.error('[CommandParser] Failed to initialize:', error);
            return false;
        }
    }

    /**
     * Build index of all commands for fast lookup
     */
    buildCommandIndex() {
        if (!this.mappings) return;

        for (const [category, data] of Object.entries(this.mappings.commandCategories)) {
            for (const command of data.commands) {
                // Index by command ID
                this.commandIndex.set(command.id, {
                    ...command,
                    category
                });

                // Index each pattern
                for (const pattern of command.patterns) {
                    const normalizedPattern = this.normalize(pattern);
                    if (!this.patternCache.has(normalizedPattern)) {
                        this.patternCache.set(normalizedPattern, []);
                    }
                    this.patternCache.get(normalizedPattern).push(command);
                }
            }
        }

        // Index aliases
        for (const [alias, commandId] of Object.entries(this.mappings.commandAliases?.aliases || {})) {
            const command = this.commandIndex.get(commandId);
            if (command) {
                this.patternCache.set(alias, [command]);
            }
        }
    }

    /**
     * Parse a text command and return execution result
     */
    parse(text) {
        if (!text || typeof text !== 'string') {
            return { success: false, error: 'Invalid input' };
        }

        // Normalize input
        const normalized = this.normalize(text);

        // Try exact match first (fastest)
        let matches = this.exactMatch(normalized);

        // Try fuzzy match if no exact match
        if (matches.length === 0) {
            matches = this.fuzzyMatch(normalized);
        }

        // Try partial match if still no matches
        if (matches.length === 0) {
            matches = this.partialMatch(normalized);
        }

        if (matches.length === 0) {
            return {
                success: false,
                error: 'No matching command found',
                suggestions: this.getSuggestions(normalized),
                input: text
            };
        }

        // If multiple matches, pick the best one
        const bestMatch = this.selectBestMatch(matches, normalized);

        // Track usage
        this.trackUsage(bestMatch.id, text);

        // Return executable result
        return {
            success: true,
            command: bestMatch,
            input: text,
            execute: () => this.executeCommand(bestMatch)
        };
    }

    /**
     * Normalize text for matching
     */
    normalize(text) {
        let normalized = text.toLowerCase().trim();

        // Remove filler words
        for (const filler of this.fillerWords) {
            const regex = new RegExp(`\\b${filler}\\b`, 'gi');
            normalized = normalized.replace(regex, '');
        }

        // Remove extra whitespace
        normalized = normalized.replace(/\s+/g, ' ').trim();

        return normalized;
    }

    /**
     * Exact pattern match
     */
    exactMatch(normalized) {
        const matches = [];

        for (const [pattern, commands] of this.patternCache.entries()) {
            if (pattern === normalized) {
                matches.push(...commands);
            }
        }

        return matches;
    }

    /**
     * Fuzzy match using Levenshtein distance
     */
    fuzzyMatch(normalized) {
        const matches = [];
        const threshold = 0.8; // 80% similarity required

        for (const [pattern, commands] of this.patternCache.entries()) {
            const similarity = this.stringSimilarity(normalized, pattern);

            if (similarity >= threshold) {
                matches.push(...commands.map(cmd => ({
                    ...cmd,
                    similarity
                })));
            }
        }

        return matches;
    }

    /**
     * Partial match (substring matching)
     */
    partialMatch(normalized) {
        const matches = [];

        for (const [pattern, commands] of this.patternCache.entries()) {
            if (pattern.includes(normalized) || normalized.includes(pattern)) {
                matches.push(...commands);
            }
        }

        return matches;
    }

    /**
     * Calculate string similarity using Levenshtein distance
     */
    stringSimilarity(str1, str2) {
        const len1 = str1.length;
        const len2 = str2.length;

        if (len1 === 0) return len2 === 0 ? 1 : 0;
        if (len2 === 0) return 0;

        const matrix = Array(len2 + 1).fill(null).map(() => Array(len1 + 1).fill(null));

        for (let i = 0; i <= len1; i++) matrix[0][i] = i;
        for (let j = 0; j <= len2; j++) matrix[j][0] = j;

        for (let j = 1; j <= len2; j++) {
            for (let i = 1; i <= len1; i++) {
                const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
                matrix[j][i] = Math.min(
                    matrix[j][i - 1] + 1,
                    matrix[j - 1][i] + 1,
                    matrix[j - 1][i - 1] + cost
                );
            }
        }

        const distance = matrix[len2][len1];
        const maxLen = Math.max(len1, len2);

        return 1 - (distance / maxLen);
    }

    /**
     * Select best match from multiple candidates
     */
    selectBestMatch(matches, normalized) {
        if (matches.length === 1) return matches[0];

        // Prefer matches with higher similarity score
        matches.sort((a, b) => {
            const simA = a.similarity || 1;
            const simB = b.similarity || 1;
            return simB - simA;
        });

        // Also consider usage frequency
        const withUsage = matches.map(match => ({
            ...match,
            usageCount: this.usageStats.get(match.id) || 0
        }));

        withUsage.sort((a, b) => {
            // Weight: 70% similarity, 30% usage
            const scoreA = (a.similarity || 1) * 0.7 + (a.usageCount / 100) * 0.3;
            const scoreB = (b.similarity || 1) * 0.7 + (b.usageCount / 100) * 0.3;
            return scoreB - scoreA;
        });

        return withUsage[0];
    }

    /**
     * Get command suggestions based on input
     */
    getSuggestions(normalized) {
        const suggestions = [];
        const words = normalized.split(' ');

        // Find commands containing any of the words
        for (const [pattern, commands] of this.patternCache.entries()) {
            for (const word of words) {
                if (word.length >= 3 && pattern.includes(word)) {
                    suggestions.push(...commands);
                    break;
                }
            }
        }

        // Remove duplicates and limit to 5
        const unique = [...new Set(suggestions.map(s => s.id))]
            .map(id => this.commandIndex.get(id))
            .slice(0, 5);

        return unique;
    }

    /**
     * Execute a matched command
     */
    executeCommand(command) {
        console.log('[CommandParser] Executing:', command.id);

        try {
            // Show response notification
            if (command.response && window.toastManager) {
                window.toastManager.show(command.icon || '✓', command.response);
            }

            // Execute the action
            switch (command.action) {
                case 'openProgram':
                    return this.openProgram(command.params.programName);

                case 'closeAllWindows':
                    return this.closeAllWindows();

                case 'tileWindows':
                    return this.tileWindows(command.params.layout);

                case 'showDesktop':
                    return this.showDesktop();

                case 'toggleMute':
                    return this.emulator.toggleMute();

                case 'adjustVolume':
                    const currentVolume = this.emulator.soundVolume || 50;
                    return this.emulator.setVolume(currentVolume + command.params.delta);

                case 'saveState':
                    if (window.stateManager) {
                        return window.stateManager.save('manual');
                    }
                    break;

                case 'showClippy':
                    if (window.clippyAssistant) {
                        window.clippyAssistant.show();
                    }
                    break;

                case 'hideClippy':
                    if (window.clippyAssistant) {
                        window.clippyAssistant.hide();
                    }
                    break;

                case 'showCommandList':
                    return this.showCommandList();

                case 'openStartMenu':
                    // Trigger start menu (implementation depends on emulator)
                    document.querySelector('.start-button')?.click();
                    break;

                case 'listPrograms':
                    return this.listPrograms();

                case 'listGames':
                    return this.listGames();

                case 'tellJoke':
                    return this.tellJoke();

                case 'openRandomProgram':
                    return this.openRandomProgram();

                case 'startDemo':
                    return this.startDemo();

                case 'quickNote':
                    return this.openProgram('notepad');

                case 'quickCalc':
                    return this.openProgram('calculator');

                default:
                    console.warn('[CommandParser] Unknown action:', command.action);
                    return false;
            }

            return true;
        } catch (error) {
            console.error('[CommandParser] Execution failed:', error);
            return false;
        }
    }

    /**
     * Open a program
     */
    openProgram(programName) {
        const methodMap = {
            notepad: 'openNotepad',
            calculator: 'openCalculator',
            paint: 'openPaint',
            minesweeper: 'openMinesweeper',
            solitaire: 'openSolitaire',
            internetExplorer: 'openInternetExplorer',
            fileExplorer: 'openFileExplorer',
            dosPrompt: 'openDOSPrompt',
            mediaPlayer: 'openMediaPlayer',
            taskManager: 'openTaskManager',
            controlPanel: 'openControlPanel',
            aboutWindows: 'openAboutDialog',
            recycleBin: 'openRecycleBin'
        };

        const method = methodMap[programName];
        if (method && typeof this.emulator[method] === 'function') {
            this.emulator[method]();
            return true;
        }

        console.warn('[CommandParser] Unknown program:', programName);
        return false;
    }

    /**
     * Close all windows
     */
    closeAllWindows() {
        const windows = document.querySelectorAll('.window');
        windows.forEach(win => {
            win.querySelector('.window-close')?.click();
        });
        return true;
    }

    /**
     * Tile windows
     */
    tileWindows(layout = 'grid') {
        const windows = document.querySelectorAll('.window');
        const count = windows.length;

        if (count === 0) return false;

        const cols = Math.ceil(Math.sqrt(count));
        const rows = Math.ceil(count / cols);
        const winWidth = Math.floor((window.innerWidth - 40) / cols);
        const winHeight = Math.floor((window.innerHeight - 80) / rows);

        windows.forEach((win, i) => {
            const col = i % cols;
            const row = Math.floor(i / cols);

            win.style.left = (20 + col * winWidth) + 'px';
            win.style.top = (20 + row * winHeight) + 'px';
            win.style.width = (winWidth - 10) + 'px';
            win.style.height = (winHeight - 10) + 'px';
        });

        return true;
    }

    /**
     * Show desktop (minimize all)
     */
    showDesktop() {
        const windows = document.querySelectorAll('.window');
        windows.forEach(win => {
            if (win.style.display !== 'none') {
                win.querySelector('.window-minimize')?.click();
            }
        });
        return true;
    }

    /**
     * Show command list
     */
    showCommandList() {
        const commands = [];

        for (const [category, data] of Object.entries(this.mappings.commandCategories)) {
            for (const cmd of data.commands) {
                commands.push(`${cmd.icon} ${cmd.patterns[0]}`);
            }
        }

        const content = `
            <div style="padding: 20px; font-family: 'MS Sans Serif';">
                <h2>Available Commands</h2>
                <p>Type any of these commands:</p>
                <div style="margin-top: 15px; max-height: 400px; overflow-y: auto;">
                    ${commands.map(cmd => `<div style="margin: 5px 0;">${cmd}</div>`).join('')}
                </div>
            </div>
        `;

        if (this.emulator.windowManager) {
            this.emulator.windowManager.createWindow('Command List', content, {
                width: 500,
                height: 600
            });
        }

        return true;
    }

    /**
     * List available programs
     */
    listPrograms() {
        const programs = [
            '📝 Notepad', '🔢 Calculator', '🎨 Paint', '💣 Minesweeper',
            '🃏 Solitaire', '🌐 Internet Explorer', '📁 File Explorer',
            '⬛ Terminal', '🎵 Media Player', '📊 Task Manager',
            '🎛️ Control Panel', '🗑️ Recycle Bin'
        ];

        const content = `
            <div style="padding: 20px; font-family: 'MS Sans Serif';">
                <h2>Available Programs</h2>
                <div style="margin-top: 15px;">
                    ${programs.map(p => `<div style="margin: 8px 0; font-size: 14px;">${p}</div>`).join('')}
                </div>
                <p style="margin-top: 20px; color: #666;">
                    Type "open [program name]" to launch any program
                </p>
            </div>
        `;

        if (this.emulator.windowManager) {
            this.emulator.windowManager.createWindow('Programs', content, {
                width: 400,
                height: 500
            });
        }

        return true;
    }

    /**
     * List games
     */
    listGames() {
        const games = ['💣 Minesweeper', '🃏 Solitaire', '🎴 FreeCell', '🐍 Snake', '🚀 Galactic Defender'];

        if (window.toastManager) {
            window.toastManager.show('🎮', `Games: ${games.join(', ')}`);
        }

        return true;
    }

    /**
     * Tell a random joke
     */
    tellJoke() {
        const jokes = [
            "Why did the computer go to the doctor? Because it had a virus! 😄",
            "Why was the computer cold? It left its Windows open! ❄️",
            "What do you call a computer that sings? A-Dell! 🎵",
            "Why did the PowerPoint presentation cross the road? To get to the other slide! 📊"
        ];

        const joke = jokes[Math.floor(Math.random() * jokes.length)];

        if (window.toastManager) {
            window.toastManager.show('😄', joke, 5000);
        }

        return true;
    }

    /**
     * Open a random program
     */
    openRandomProgram() {
        const programs = ['notepad', 'calculator', 'paint', 'minesweeper', 'solitaire'];
        const random = programs[Math.floor(Math.random() * programs.length)];
        return this.openProgram(random);
    }

    /**
     * Start demo mode (open several programs)
     */
    async startDemo() {
        const sequence = ['notepad', 'calculator', 'paint'];

        for (let i = 0; i < sequence.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 800));
            this.openProgram(sequence[i]);
        }

        await new Promise(resolve => setTimeout(resolve, 1000));
        this.tileWindows();

        return true;
    }

    /**
     * Track command usage
     */
    trackUsage(commandId, input) {
        const count = this.usageStats.get(commandId) || 0;
        this.usageStats.set(commandId, count + 1);

        // Store in localStorage for persistence
        try {
            const stats = JSON.parse(localStorage.getItem('command-usage-stats') || '{}');
            stats[commandId] = (stats[commandId] || 0) + 1;
            stats[`_input_${commandId}`] = input; // Store last input
            localStorage.setItem('command-usage-stats', JSON.stringify(stats));
        } catch (error) {
            console.warn('[CommandParser] Failed to persist usage stats:', error);
        }
    }

    /**
     * Get usage statistics
     */
    getUsageStats() {
        return {
            inMemory: Object.fromEntries(this.usageStats),
            persistent: JSON.parse(localStorage.getItem('command-usage-stats') || '{}')
        };
    }

    /**
     * Clear usage statistics
     */
    clearUsageStats() {
        this.usageStats.clear();
        localStorage.removeItem('command-usage-stats');
    }
}

// Export for use in modules or make available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommandParser;
} else {
    window.CommandParser = CommandParser;
}
