# AI Intelligence Injection System

This directory contains the "brain" file for the Windows 95 emulator AI agent system.

## Overview

The Windows 95 emulator has been enhanced with an intelligence injection system that allows a static HTML page to receive and execute commands from an AI agent through a local JSON file. This creates a unique architecture where:

1. **Static HTML remains static** - No server required, works offline
2. **AI agent writes state frames** - The `windows95-ai-controller` agent writes its decisions to a JSON file
3. **HTML polls and executes** - The emulator reads the JSON file every 5 seconds and executes commands

## Architecture

```
┌─────────────────────────────────┐
│  windows95-ai-controller Agent  │
│  (Claude Code Sub-Agent)        │
│                                 │
│  - Analyzes emulator state      │
│  - Makes decisions              │
│  - Writes commands              │
└────────────┬────────────────────┘
             │
             ▼ Writes state frames
┌─────────────────────────────────┐
│  .ai/windows95-agent-state.json │  ◄─── THIS FILE
│  (AI Brain / State Frame)       │
└────────────┬────────────────────┘
             │
             ▼ Polls every 5 seconds
┌─────────────────────────────────┐
│  windows95-emulator.html        │
│  (Static HTML + JavaScript)     │
│                                 │
│  - AIStateController class      │
│  - Reads state file             │
│  - Executes commands            │
│  - Shows visual feedback        │
└─────────────────────────────────┘
```

## State File Format

The `windows95-agent-state.json` file contains:

### Structure

```json
{
  "timestamp": 1234567890000,          // Unix timestamp - changes trigger updates
  "version": "1.0.0",                  // State file version
  "agentId": "windows95-ai-controller", // Which agent wrote this

  "goals": [                            // Current AI goals
    "Monitor window activity",
    "Optimize workspace layout"
  ],

  "observations": {                     // What the AI has observed
    "windowCount": 3,
    "activePrograms": ["Notepad", "Paint"],
    "userActivity": "high"
  },

  "actions": [                          // History of actions taken
    {
      "timestamp": 1234567890000,
      "type": "window_created",
      "result": "success"
    }
  ],

  "commands": [                         // Commands to execute (THIS IS THE KEY PART!)
    {
      "id": "unique-cmd-id",           // Unique ID (prevents duplicate execution)
      "type": "createWindow",          // Command type
      "params": {                      // Command parameters
        "title": "AI Window",
        "content": "<p>Hello!</p>",
        "x": 100,
        "y": 100
      },
      "priority": "normal",            // Priority level
      "expiry": 1234567900000          // Optional expiration timestamp
    }
  ],

  "telemetrySnapshot": {               // Telemetry data
    "windows": [],
    "events": []
  },

  "metadata": {                        // Metadata about the state
    "lastUpdate": 1234567890000,
    "autonomousMode": true
  }
}
```

## Supported Commands

The `AIStateController` class in the emulator supports these command types:

### 1. `createWindow`
Creates a new window in the emulator.

```json
{
  "type": "createWindow",
  "params": {
    "title": "Window Title",
    "content": "<html content>",
    "x": 100,
    "y": 100,
    "width": 400,
    "height": 300
  }
}
```

### 2. `closeWindow`
Closes an existing window.

```json
{
  "type": "closeWindow",
  "params": {
    "windowId": "window-5"
  }
}
```

### 3. `moveWindow`
Moves a window to a new position.

```json
{
  "type": "moveWindow",
  "params": {
    "windowId": "window-5",
    "x": 200,
    "y": 150
  }
}
```

### 4. `openProgram`
Opens a built-in program (Notepad, Paint, Calculator, etc.).

```json
{
  "type": "openProgram",
  "params": {
    "program": "Notepad"  // Calls emulator.openNotepad()
  }
}
```

### 5. `notification`
Shows a notification dialog.

```json
{
  "type": "notification",
  "params": {
    "message": "Hello from AI!",
    "x": 100,
    "y": 100
  }
}
```

### 6. `executeScript`
Executes arbitrary JavaScript (use with caution!).

```json
{
  "type": "executeScript",
  "params": {
    "code": "console.log('AI says hello!');"
  }
}
```

## How the AI Agent Uses This

When you ask Claude Code to enhance the Windows 95 emulator, the `windows95-ai-controller` agent:

1. **Reads** the emulator HTML file to understand current state
2. **Analyzes** what enhancements to make
3. **Decides** what commands to send
4. **Writes** a new state frame to this JSON file with updated `timestamp` and `commands`
5. **Waits** for the emulator to execute the commands
6. **Repeats** with new observations and goals

## Visual Feedback

When the AI is active:

- **Green pulsing LED** appears in the status bar
- **AI-controlled windows** have a green glow and green title bar
- **Console logs** show `[AI Controller]` messages

## Extending the System

To add new command types:

1. Add a new case in `AIStateController.executeCommand()`
2. Implement the command handler method (e.g., `cmdYourNewCommand()`)
3. Update this documentation

Example:

```javascript
case 'yourNewCommand':
    this.cmdYourNewCommand(command.params);
    break;
```

## Files in this Directory

- `windows95-agent-state.json` - The AI brain state file (this is what the emulator reads)
- `README.md` - This documentation file
- (Future) `telemetry-history.json` - Historical telemetry data
- (Future) `agent-logs.json` - Agent decision logs

## Usage

### For Users

Just open `windows95-emulator.html` in a browser. The AI system will:
- Automatically start monitoring
- Read this state file every 5 seconds
- Execute any commands found in the `commands` array

### For Developers / AI Agent

To send commands to the emulator:

1. Read the current state file
2. Add your commands to the `commands` array
3. Update the `timestamp` to trigger a reload
4. Write the file back

Example workflow:

```javascript
// Read current state
const state = JSON.parse(fs.readFileSync('.ai/windows95-agent-state.json'));

// Add a new command
state.commands.push({
  id: `cmd-${Date.now()}`,
  type: 'notification',
  params: {
    message: 'Hello from AI!'
  }
});

// Update timestamp to trigger reload
state.timestamp = Date.now();

// Write back
fs.writeFileSync('.ai/windows95-agent-state.json', JSON.stringify(state, null, 2));
```

## Benefits of This Architecture

1. **Local-First** - No server required, works completely offline
2. **Stateless HTML** - The HTML file remains a static file
3. **Autonomous AI** - The AI can continuously update the state file
4. **Inspectable** - You can see exactly what the AI is doing by reading the JSON
5. **Safe** - Commands are declarative and sandboxed
6. **Extensible** - Easy to add new command types
7. **Persistent** - State survives page reloads (if you save the file)

## Security Notes

- The `executeScript` command allows arbitrary JavaScript execution
- Only use state files from trusted sources
- The emulator validates command structure before execution
- Commands have optional expiry timestamps to prevent stale actions

## Future Enhancements

Potential future additions:

- Two-way communication (emulator writes telemetry back to a separate file)
- Command acknowledgment system
- Error reporting back to state file
- Multiple agent coordination
- Conditional command execution
- Command queuing and scheduling

---

Created by: windows95-ai-controller agent
Last Updated: 2025-01-14
Version: 1.0.0
