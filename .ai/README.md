# AI Daily Intelligence Briefing System

This directory contains the **daily briefing brain** for the Windows 95 emulator - your AI-powered morning agenda and success guide.

## Overview

The Windows 95 emulator has been transformed into an **AI-guided productivity system** that receives daily intelligence briefings through a local JSON file. The system is **time-gap aware** - it knows how long it's been since your last session and calibrates the briefing accordingly.

### What Makes This Special: Time-Gap Calibration

**The AI treats you completely differently based on how long you've been away:**

- **3 hours ago?** → "Welcome back! Let's continue your day."
- **Yesterday?** → "Good morning! Here's today's agenda."
- **1 week ago?** → "Welcome back! Let's ease back in and catch up."
- **5 years ago?** → "🎉 Welcome back! It's been a while. No pressure, just explore."

Every briefing includes:

- 📋 **Contextual Agenda** - Priorities adjusted for time gap (productive if recent, gentle if long)
- ⏰ **Time Blocks** - Schedule based on gap (full day if recent, exploration if long)
- 📊 **Insights** - Yesterday's stats if recent, "what happened since" if long
- 💡 **AI Guidance** - Tone calibrated to gap (energetic if recent, patient if long)
- ⚡ **Quick Actions** - Programs recommended based on where you are

This creates a unique architecture where:

1. **Static HTML remains static** - No server required, works completely offline
2. **AI publishes time-aware briefings** - Updated with full awareness of time context
3. **HTML displays contextually** - The emulator shows exactly the right message for the gap
4. **User success focused** - Meets you where you are, not where you "should" be

## Architecture

```
        ┌──────────────────────────────────────┐
        │  Daily Briefing (Updated @ 8:00 AM)  │
        │  - Today's agenda and priorities     │
        │  - Time-blocked schedule             │
        │  - Yesterday's achievements          │
        │  - AI guidance for success           │
        └──────────────┬───────────────────────┘
                       │ Written by AI Agent or Human
                       ▼
        ┌──────────────────────────────────────┐
        │  .ai/windows95-agent-state.json      │  ◄─── DAILY BRIEFING FILE
        │  (Published daily at 8:00 AM)        │
        │  - todaysAgenda                      │
        │  - insights (yesterday's stats)      │
        │  - commands (windows to create)      │
        └──────────────┬───────────────────────┘
                       │ Polls every 5 seconds
                       ▼
        ┌──────────────────────────────────────┐
        │  windows95-emulator.html             │
        │  (User's Workspace)                  │
        │                                      │
        │  On Login, Shows:                    │
        │  → Daily Intelligence Briefing       │
        │  → Quick Actions Panel               │
        │  → Green AI Status Indicator         │
        └──────────────────────────────────────┘
                       ↓
               User works guided by
               AI recommendations
```

## Daily Briefing Structure

The state file now serves as a **daily intelligence briefing** that guides the user through their day.

## Daily Briefing File Format

The `windows95-agent-state.json` file is structured as a daily intelligence briefing:

### Core Structure

```json
{
  "timestamp": 1736928000000,           // Unix timestamp - changes trigger UI updates
  "publishedDate": "2025-01-15",        // Human-readable date
  "publishedTime": "08:00 AM",          // Time briefing was published
  "version": "1.0.0",
  "agentId": "windows95-ai-controller",
  "briefingTitle": "Daily Intelligence Briefing - Tuesday, January 15th, 2025",

  "todaysAgenda": {                     // ⭐ THE MAIN AGENDA
    "greeting": "Good morning! Welcome back...",
    "primaryFocus": "Productivity and Organization",
    "keyPriorities": [                  // Today's main tasks
      "📋 Review and organize open projects",
      "✅ Complete 3 high-priority tasks",
      "🧹 Clean up desktop and file structure"
    ],
    "aiGuidance": "Today's focus is on clearing clutter...",
    "recommendedPrograms": ["Notepad", "Paint", "FileManager"],
    "timeBlocks": [                     // Suggested schedule
      {
        "time": "8:00 AM - 10:00 AM",
        "activity": "Deep work - Focus on high-priority tasks",
        "suggestion": "Minimize distractions, use Notepad"
      }
    ]
  },

  "insights": {                         // 📊 YESTERDAY'S FEEDBACK
    "yesterdayStats": {
      "windowsOpened": 12,
      "mostUsedProgram": "Notepad",
      "productiveHours": 4.5,
      "completedTasks": 7
    },
    "suggestions": [                    // AI insights from yesterday
      "You opened Notepad 8 times - consider keeping it open",
      "Your most productive time was 9-11 AM"
    ],
    "achievements": [                   // What you accomplished
      "🏆 Completed 7 tasks yesterday",
      "⚡ 4.5 hours of focused work"
    ]
  },

  "commands": [                         // 🎯 UI COMMANDS TO EXECUTE
    {
      "id": "daily-briefing-main",
      "type": "createWindow",
      "params": {
        "title": "☀️ Daily Intelligence Briefing",
        "content": "<html with briefing>",
        "x": 50, "y": 50, "width": 600, "height": 650
      },
      "priority": "critical"            // Shows immediately on login
    },
    {
      "id": "quick-actions-panel",
      "type": "createWindow",
      "params": {
        "title": "⚡ Quick Actions",
        "content": "<buttons for recommended programs>"
      },
      "priority": "high"
    }
  ],

  "metadata": {
    "lastUpdate": 1736928000000,
    "nextUpdate": "2025-01-16T08:00:00Z",  // When next briefing publishes
    "briefingType": "daily_agenda"
  }
}
```

### Key Sections Explained

#### 📋 `todaysAgenda`
The heart of the daily briefing - contains:
- **keyPriorities**: 3-5 prioritized tasks for the day
- **timeBlocks**: Suggested schedule with time-based activities
- **aiGuidance**: Contextual advice based on user patterns
- **recommendedPrograms**: Which Windows 95 programs to use today

#### 📊 `insights`
Feedback loop from previous sessions:
- **yesterdayStats**: Quantified productivity metrics
- **suggestions**: AI observations about work patterns
- **achievements**: Positive reinforcement for completed work

#### 🎯 `commands`
Windows to create on login - the daily briefing shows up as actual UI:
- **Priority "critical"**: Daily briefing window (large, front-and-center)
- **Priority "high"**: Quick actions panel with recommended programs
- All windows appear within 5 seconds of opening the emulator

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

## Digital Twin Builder Framework

The system has evolved beyond daily briefings into a complete **data-driven application framework**. This framework enables building applications using pure JSON instead of code.

### 🧠 Core Components

#### 1. Digital Twin Context (`windows95-digital-twin-context.json`)
Machine-readable API documentation that teaches AI agents about the emulator instantly:
- Complete API surface documentation
- Real-time control patterns
- Example code snippets
- DOM selectors and event handlers
- Canvas rendering methods

**Key Innovation**: AI cannot distinguish between trained knowledge and injected JSON context. Reading this file gives agents **instant expertise**.

#### 2. Data Slosh Pipeline (`data-slosh-pipeline.js`)
Bidirectional data flow system that creates a continuous cycle:
```
State → JSON → Pattern Detection → Instructions → Execution → New State → [LOOP]
```

Features:
- Captures emulator state every 60 seconds
- Detects patterns (too many windows, disorganized icons, etc.)
- Auto-generates instruction files based on patterns
- Executes time-based and state-based triggers
- Updates digital twin with discoveries

#### 3. State Persistence (`windows95-state-persistence.js`)
Complete state capture and restore system:
- localStorage for quick restore
- IndexedDB for state history (last 50 states)
- Time-travel debugging to any timestamp
- JSON export/import for portability
- Auto-save every 30 seconds

#### 4. Instruction Executor (`windows95-instruction-executor.js`)
Autonomous execution engine for JSON-defined workflows:
- 15+ supported step types (createWindow, cascadeWindows, notification, etc.)
- Time-based triggers (execute at specific times)
- State-based triggers (execute when conditions met)
- Self-generating (can create new instruction files)
- No AI required - runs autonomously!

#### 5. Digital Twin Builder Agent (`.claude/agents/digital-twin-builder.md`)
AI agent that builds applications using pure data:
- Reads digital twin context for instant expertise
- Studies existing instruction files to learn patterns
- Generates new JSON instruction files
- Validates API usage and structure
- Updates digital twin with discoveries

### 📦 Static Instruction Files

JSON files in `static-instructions/` define autonomous behaviors:

- **`morning-routine.json`** - Daily startup workflow (triggers at 8 AM)
- **`focus-mode.json`** - Deep work environment with Pomodoro timer
- **`cleanup-workspace.json`** - Auto-organize desktop and windows
- **`presentation-mode.json`** - Professional demo setup (built by agent)
- **`learning-assistant-tutorial.json`** - Interactive tutorial system (built by agent)
- **`workspace-templates-manager.json`** - Smart workspace management (built by agent)

### 🎯 How It Works

#### Traditional Development
```
Write code → Deploy → Users interact → Write more code
```

#### Data-Driven Framework
```
Define behavior as JSON → System executes autonomously → Patterns detected →
System generates new JSON → Knowledge compounds → [Infinite improvement loop]
```

### 🚀 Building Applications

Use the Digital Twin Builder agent to create new applications:

```bash
# Invoke the agent
claude -a digital-twin-builder "Create a meditation timer with breathing exercises"

# The agent will:
# 1. Read windows95-digital-twin-context.json
# 2. Study existing instruction files
# 3. Generate new JSON instruction file
# 4. Validate structure and APIs
# 5. Save to static-instructions/

# Execute the new instruction
# In browser console:
executeInstruction('meditation-timer')
```

### 🌊 Data Sloshing in Action

Every 60 seconds, the system:
1. **Captures** complete emulator state as JSON
2. **Analyzes** patterns (window count, organization, etc.)
3. **Generates** instruction files when patterns detected
4. **Executes** scheduled or triggered instructions
5. **Updates** digital twin with new discoveries
6. **Loops** infinitely, improving over time

### 💡 Philosophy: Ultra Think

**Key Insight**: AI cannot distinguish between trained knowledge and injected JSON context.

This enables:
- **Instant Expertise** - Inject API docs, AI becomes expert immediately
- **Knowledge Compounding** - Each agent updates JSON, benefiting all future agents
- **Self-Evolution** - System writes its own behavior files
- **Zero Code Changes** - Everything flows through JSON

### 📚 Documentation

- **`DIGITAL-TWIN-BUILDER-GUIDE.md`** - Complete guide to the framework
- **`briefing-examples.md`** - Example briefing configurations
- **`clippy-system.md`** - Multi-agent Clippy coordination
- **`SYSTEM-OVERVIEW.md`** - High-level architecture overview

### 🎨 Global APIs

Available in browser console:

```javascript
// State Management
getLatestState()              // Get current emulator state
exportState()                 // Download state as JSON
importState(json)             // Restore state from JSON

// Instruction Control
executeInstruction(name)      // Run an instruction
listInstructions()            // See all available instructions
generateInstruction(config)   // Create new instruction

// Data Sloshing
slosh()                       // Run one slosh cycle
startSloshing()               // Auto-slosh every 60s
stopSloshing()                // Stop auto-sloshing
```

### 🔧 Creating Custom Instructions

Create a JSON file in `static-instructions/`:

```json
{
  "name": "my-workflow",
  "description": "What this does",
  "version": "1.0.0",
  "author": "you",
  "saveStateAfter": true,
  "schedule": "09:00",  // Optional: time-based trigger
  "steps": [
    {
      "type": "createWindow",
      "params": {
        "title": "My Window",
        "content": "<div>Content</div>",
        "width": 400,
        "height": 300
      },
      "delay": 500
    },
    {
      "type": "notification",
      "params": {
        "title": "Done!",
        "message": "Window created"
      }
    }
  ]
}
```

Then execute: `executeInstruction('my-workflow')`

## Files in this Directory

### Core Framework
- `windows95-digital-twin-context.json` - Machine-readable API documentation (15KB)
- `data-slosh-pipeline.js` - Bidirectional data flow coordinator
- `windows95-state-persistence.js` - State capture and restore system
- `windows95-instruction-executor.js` - Autonomous JSON execution engine

### Configuration & State
- `windows95-agent-state.json` - Daily briefing state file (emulator reads this)
- `README.md` - This documentation file

### Documentation
- `DIGITAL-TWIN-BUILDER-GUIDE.md` - Complete framework guide
- `SYSTEM-OVERVIEW.md` - Architecture overview
- `briefing-examples.md` - Example configurations
- `clippy-system.md` - Multi-agent coordination

### Static Instructions (Autonomous Behaviors)
- `static-instructions/morning-routine.json` - Daily startup workflow
- `static-instructions/focus-mode.json` - Deep work environment
- `static-instructions/cleanup-workspace.json` - Auto-organize workspace
- `static-instructions/presentation-mode.json` - Demo setup
- `static-instructions/learning-assistant-tutorial.json` - Interactive tutorial
- `static-instructions/workspace-templates-manager.json` - Template management

### Future
- (Future) `telemetry-history.json` - Historical telemetry data
- (Future) `agent-logs.json` - Agent decision logs

## How to Update the Daily Briefing

### Automatic Updates (Morning Publishing)

The daily briefing is designed to be updated every morning at 8:00 AM. You can:

1. **Use the AI Agent**: Ask the `windows95-ai-controller` agent to generate a new briefing
2. **Manual Update**: Edit the JSON file directly with today's priorities
3. **Automated Script**: Create a cron job or scheduled task to update the file

### Publishing a New Briefing

To publish a new daily briefing:

1. **Update Core Fields**:
```json
{
  "timestamp": 1736928000000,  // ⚠️ MUST CHANGE to trigger update
  "publishedDate": "2025-01-15",
  "publishedTime": "08:00 AM",
  "briefingTitle": "Daily Intelligence Briefing - Tuesday, January 15th, 2025"
}
```

2. **Set Today's Agenda**:
```json
"todaysAgenda": {
  "primaryFocus": "What should the user focus on today?",
  "keyPriorities": [
    "Priority 1",
    "Priority 2",
    "Priority 3"
  ],
  "aiGuidance": "Contextual advice...",
  "timeBlocks": [
    {
      "time": "8:00 AM - 10:00 AM",
      "activity": "Deep work",
      "suggestion": "What to do during this time"
    }
  ]
}
```

3. **Include Yesterday's Insights** (optional but powerful):
```json
"insights": {
  "yesterdayStats": {
    "completedTasks": 7,
    "productiveHours": 4.5
  },
  "achievements": [
    "What they accomplished"
  ]
}
```

4. **Change the Timestamp** (this triggers the UI to reload the briefing):
```javascript
state.timestamp = Date.now();  // New timestamp = new briefing!
```

### Example: Publishing Today's Briefing

```javascript
const briefing = {
  timestamp: Date.now(),  // ⭐ This makes it update!
  publishedDate: "2025-01-15",
  publishedTime: "08:00 AM",
  briefingTitle: "Daily Intelligence Briefing - Tuesday, January 15th, 2025",

  todaysAgenda: {
    greeting: "Good morning! Ready for a productive day?",
    primaryFocus: "Project completion and creative work",
    keyPriorities: [
      "📝 Finish project proposal by 11 AM",
      "🎨 Design mockups for new feature",
      "📞 Schedule follow-up meeting",
      "🧹 Organize digital workspace"
    ],
    aiGuidance: "Focus on completion today. You're 80% done with the proposal - finish strong!",
    recommendedPrograms: ["Notepad", "Paint"],
    timeBlocks: [
      {
        time: "8:00 AM - 11:00 AM",
        activity: "Deep work - Finish proposal",
        suggestion: "Use Notepad, silence notifications"
      },
      {
        time: "11:00 AM - 1:00 PM",
        activity: "Creative work - Design mockups",
        suggestion: "Open Paint, sketch ideas freely"
      }
    ]
  },

  insights: {
    yesterdayStats: {
      completedTasks: 5,
      productiveHours: 3.5,
      mostUsedProgram: "Notepad"
    },
    achievements: [
      "🏆 Completed 5 tasks",
      "📝 Drafted 3 proposals"
    ]
  },

  commands: [
    {
      id: "daily-briefing-" + Date.now(),
      type: "createWindow",
      params: {
        title: "☀️ Daily Intelligence Briefing - Jan 15",
        content: "...",  // HTML content
        x: 50, y: 50, width: 600, height: 650
      },
      priority: "critical"
    }
  ],

  metadata: {
    nextUpdate: "2025-01-16T08:00:00Z"
  }
};

// Write to file
fs.writeFileSync('.ai/windows95-agent-state.json',
  JSON.stringify(briefing, null, 2));
```

## Usage

### For Users

Just open `windows95-emulator.html` in a browser. Within 5 seconds:
- ☀️ **Daily briefing window** appears with today's agenda
- ⚡ **Quick actions panel** shows recommended programs
- 🟢 **Green LED** indicates AI system is active
- 📋 **Priorities and schedule** guide your day

The system automatically checks for updates every 5 seconds, so any changes to the briefing file appear immediately.

### For AI Agents

The `windows95-ai-controller` agent can generate personalized briefings:

```bash
# Ask the agent to create today's briefing
"Create a daily intelligence briefing for the Windows 95 emulator focused on
productivity and code review tasks"
```

The agent will:
1. Analyze your typical work patterns
2. Generate prioritized tasks
3. Create time-blocked schedule
4. Write the briefing to the state file
5. User sees it on next login!

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
