# Command Parser Integration Guide

Complete guide for integrating natural language text commands into the Windows 95 emulator.

## Quick Start

### 1. Add Files to Your HTML

```html
<!-- Add before </body> -->
<script src="localfirst-command-parser.js"></script>
```

### 2. Initialize Command Parser

```javascript
// After emulator is created
let commandParser;

document.addEventListener('DOMContentLoaded', async () => {
    // Create emulator
    emulator = new Windows95Emulator();

    // Create and initialize command parser
    commandParser = new CommandParser(emulator);
    await commandParser.init();

    // Make globally available
    window.commandParser = commandParser;

    console.log('Command parser ready!');
});
```

### 3. Use in Chat Interface (Clippy)

```javascript
// In Clippy chat message handler
function handleUserMessage(message) {
    // Try to parse as command first
    const result = commandParser.parse(message);

    if (result.success) {
        // Execute the command
        result.execute();

        // Show confirmation
        addMessage('Clippy', `${result.command.icon} ${result.command.response}`, true);

        return true; // Command handled
    } else {
        // Not a command, check for suggestions
        if (result.suggestions && result.suggestions.length > 0) {
            const suggestions = result.suggestions
                .map(s => `${s.icon} ${s.patterns[0]}`)
                .join(', ');

            addMessage('Clippy',
                `I didn't understand that. Did you mean: ${suggestions}?`,
                true
            );
        } else {
            // Fall back to AI or default response
            addMessage('Clippy',
                `I'm not sure what you mean. Type "help" to see available commands.`,
                true
            );
        }

        return false;
    }
}
```

### 4. Use in Text Input Field

```javascript
// General text input handler
function handleTextCommand(inputElement) {
    const text = inputElement.value.trim();

    if (!text) return;

    const result = commandParser.parse(text);

    if (result.success) {
        // Execute
        result.execute();

        // Clear input
        inputElement.value = '';

        // Show toast
        if (window.toastManager) {
            window.toastManager.show('✓', `Executed: ${result.command.patterns[0]}`);
        }
    } else {
        // Show error
        if (window.toastManager) {
            window.toastManager.show('❌', 'Command not recognized');
        }
    }
}
```

---

## Integration Patterns

### Pattern 1: Command Palette

Add a command palette that users can trigger with a keyboard shortcut:

```javascript
// Add keyboard shortcut (Ctrl+K or Cmd+K)
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        showCommandPalette();
    }
});

function showCommandPalette() {
    const content = `
        <div style="padding: 20px; font-family: 'MS Sans Serif';">
            <h2>Command Palette</h2>
            <p style="margin: 10px 0; color: #666;">Type a command and press Enter</p>
            <input
                type="text"
                id="command-input"
                placeholder="e.g., open notepad, mute, tile windows..."
                style="width: 100%; padding: 8px; font-size: 14px; border: 2px inset;"
                autofocus
            />
            <div id="command-suggestions" style="margin-top: 10px; font-size: 12px; color: #666;"></div>
        </div>
    `;

    const win = emulator.windowManager.createWindow('Command Palette', content, {
        width: 500,
        height: 200
    });

    // Handle input
    setTimeout(() => {
        const input = document.getElementById('command-input');
        const suggestions = document.getElementById('command-suggestions');

        // Live suggestions as user types
        input.addEventListener('input', () => {
            const text = input.value.trim();

            if (text.length >= 2) {
                const result = commandParser.parse(text);

                if (result.suggestions && result.suggestions.length > 0) {
                    suggestions.innerHTML = 'Suggestions: ' +
                        result.suggestions.map(s => s.patterns[0]).join(', ');
                } else {
                    suggestions.innerHTML = '';
                }
            }
        });

        // Execute on Enter
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const result = commandParser.parse(input.value);

                if (result.success) {
                    result.execute();
                    win.remove(); // Close palette
                } else {
                    suggestions.innerHTML = '❌ Command not recognized';
                    suggestions.style.color = 'red';
                }
            } else if (e.key === 'Escape') {
                win.remove(); // Close on Escape
            }
        });
    }, 100);
}
```

### Pattern 2: Voice Commands

Combine with Web Speech API for voice control:

```javascript
// Initialize speech recognition
let recognition;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Voice command:', transcript);

        // Parse and execute
        const result = commandParser.parse(transcript);

        if (result.success) {
            result.execute();

            if (window.toastManager) {
                window.toastManager.show('🎤', `Voice: ${result.command.patterns[0]}`);
            }
        } else {
            if (window.toastManager) {
                window.toastManager.show('🎤', 'Voice command not recognized');
            }
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };
}

// Add button to trigger voice recognition
function startVoiceCommand() {
    if (recognition) {
        recognition.start();

        if (window.toastManager) {
            window.toastManager.show('🎤', 'Listening...');
        }
    }
}
```

### Pattern 3: Chat Integration (Full Example)

Complete integration with Clippy chat:

```javascript
// Enhance Clippy chat with command parsing
function enhanceClippyChat() {
    // Find Clippy chat window
    const chatWindow = document.querySelector('[data-program="clippy-chat"]');

    if (!chatWindow) {
        console.warn('Clippy chat not found');
        return;
    }

    // Find message input
    const messageInput = chatWindow.querySelector('textarea, input[type="text"]');
    const sendButton = chatWindow.querySelector('button');

    if (!messageInput || !sendButton) {
        console.warn('Chat UI elements not found');
        return;
    }

    // Replace send handler
    const originalHandler = sendButton.onclick;

    sendButton.onclick = async () => {
        const message = messageInput.value.trim();

        if (!message) return;

        // Add user message to chat
        addClippyMessage('You', message, false);

        // Clear input
        messageInput.value = '';

        // Try to parse as command
        const result = commandParser.parse(message);

        if (result.success) {
            // It's a command! Execute it
            result.execute();

            // Clippy confirms
            addClippyMessage('Clippy',
                `${result.command.icon} ${result.command.response}`,
                true
            );
        } else {
            // Not a command, check suggestions
            if (result.suggestions && result.suggestions.length > 0) {
                const suggestionList = result.suggestions
                    .map(s => `• ${s.patterns[0]}`)
                    .join('\\n');

                addClippyMessage('Clippy',
                    `I didn't recognize that command. Did you mean:\\n${suggestionList}`,
                    true
                );
            } else {
                // Fall back to AI or scripted response
                addClippyMessage('Clippy',
                    `Hmm, I'm not sure about that. Type "help" to see what I can do!`,
                    true
                );
            }
        }
    };
}

function addClippyMessage(sender, text, isClippy) {
    const chatMessages = document.querySelector('.chat-messages');

    if (!chatMessages) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = isClippy ? 'clippy-message' : 'user-message';
    msgDiv.innerHTML = `
        <strong>${sender}:</strong> ${text}
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
```

---

## Example Commands

Once integrated, users can type:

### Program Commands
- "open notepad"
- "launch calculator"
- "start paint"
- "calc" (alias)
- "np" (alias)

### Window Commands
- "close all windows"
- "tile windows"
- "show desktop"

### System Commands
- "mute"
- "volume up"
- "save state"
- "about"

### Clippy Commands
- "show clippy"
- "hide clippy"
- "help"

### Fun Commands
- "tell me a joke"
- "surprise me"
- "demo mode"

---

## Customization

### Add Custom Commands

Create `.ai/user-commands.json`:

```json
{
  "customCommands": [
    {
      "id": "custom-hello",
      "patterns": [
        "hello",
        "hi",
        "hey"
      ],
      "action": "customAction",
      "response": "Hello! How can I help?",
      "icon": "👋",
      "handler": "showGreeting"
    }
  ]
}
```

Load and merge with default commands:

```javascript
async function loadCustomCommands() {
    try {
        const response = await fetch('.ai/user-commands.json');
        const custom = await response.json();

        // Merge with default mappings
        for (const cmd of custom.customCommands) {
            commandParser.commandIndex.set(cmd.id, cmd);

            // Add patterns to cache
            for (const pattern of cmd.patterns) {
                const normalized = commandParser.normalize(pattern);
                if (!commandParser.patternCache.has(normalized)) {
                    commandParser.patternCache.set(normalized, []);
                }
                commandParser.patternCache.get(normalized).push(cmd);
            }
        }

        console.log('Custom commands loaded');
    } catch (error) {
        console.warn('No custom commands found');
    }
}

// Call after parser initialization
await commandParser.init();
await loadCustomCommands();
```

### Add Custom Action Handlers

Extend CommandParser with custom actions:

```javascript
// Add custom handler method
CommandParser.prototype.showGreeting = function() {
    const greetings = [
        "Hello! Ready to explore Windows 95?",
        "Hi there! What would you like to do?",
        "Hey! Need help with anything?"
    ];

    const greeting = greetings[Math.floor(Math.random() * greetings.length)];

    if (window.toastManager) {
        window.toastManager.show('👋', greeting);
    }

    return true;
};
```

---

## Usage Analytics

### Track Popular Commands

```javascript
// Get usage statistics
function showCommandStats() {
    const stats = commandParser.getUsageStats();

    // Sort by usage count
    const sorted = Object.entries(stats.persistent)
        .filter(([key]) => !key.startsWith('_input_'))
        .sort(([, a], [, b]) => b - a)
        .slice(0, 10);

    const content = `
        <div style="padding: 20px; font-family: 'MS Sans Serif';">
            <h2>Top Commands</h2>
            <div style="margin-top: 15px;">
                ${sorted.map(([id, count], i) => {
                    const cmd = commandParser.commandIndex.get(id);
                    return `
                        <div style="margin: 8px 0;">
                            ${i + 1}. ${cmd?.icon || '•'} ${cmd?.patterns[0] || id}
                            <span style="float: right; color: #666;">${count} uses</span>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;

    emulator.windowManager.createWindow('Command Stats', content, {
        width: 400,
        height: 400
    });
}
```

---

## Performance

The CommandParser is optimized for speed:

- **O(1) lookup** for exact matches and aliases
- **Pattern cache** for instant matching
- **Lazy evaluation** - only fuzzy match if exact fails
- **~10KB** compressed command mappings
- **<5ms** average parse time

## Testing

Test the command parser:

```javascript
// Test suite
function testCommandParser() {
    const tests = [
        { input: "open notepad", expected: "open-notepad" },
        { input: "can you please open calculator", expected: "open-calculator" },
        { input: "np", expected: "open-notepad" },
        { input: "calc", expected: "open-calculator" },
        { input: "opn notpad", expected: "open-notepad" }, // typo
        { input: "tile", expected: "tile-windows" }, // partial
    ];

    let passed = 0;
    let failed = 0;

    for (const test of tests) {
        const result = commandParser.parse(test.input);

        if (result.success && result.command.id === test.expected) {
            console.log(`✓ PASS: "${test.input}" -> ${test.expected}`);
            passed++;
        } else {
            console.log(`✗ FAIL: "${test.input}" expected ${test.expected}, got ${result.command?.id || 'no match'}`);
            failed++;
        }
    }

    console.log(`\nResults: ${passed} passed, ${failed} failed`);
}

// Run tests
testCommandParser();
```

---

## Complete Integration Example

Here's the complete code to add to `windows95-emulator.html`:

```html
<!-- Add before </body> -->
<script src="localfirst-command-parser.js"></script>
<script>
// Initialize command parser after emulator loads
let commandParser;

document.addEventListener('DOMContentLoaded', async () => {
    // Wait for emulator to be ready
    if (typeof emulator === 'undefined') {
        console.error('Emulator not found');
        return;
    }

    // Create command parser
    commandParser = new CommandParser(emulator);
    await commandParser.init();

    // Make globally available
    window.commandParser = commandParser;

    console.log('✓ Command parser ready with', commandParser.commandIndex.size, 'commands');

    // Add command palette shortcut (Ctrl+K)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            showCommandPalette();
        }
    });

    // Enhance Clippy chat with command parsing
    enhanceClippyChat();
});

function showCommandPalette() {
    // ... (code from Pattern 1 above)
}

function enhanceClippyChat() {
    // ... (code from Pattern 3 above)
}
</script>
```

Now users can:
- Type "open notepad" in Clippy chat → Notepad opens
- Press Ctrl+K → Command palette appears
- Type "np" → Notepad opens (alias)
- Say "open calculator" → Calculator opens (voice)

**Pure data-driven, cached by default, instant execution!** 🚀
