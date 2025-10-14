# 🚀 Data Sloshing System - Quickstart Guide

Complete autonomous data management for the Windows 95 emulator.

---

## 🎯 What You Get

### 1. **Natural Language Commands** (Ready Now!)
Type "open notepad" → Notepad opens instantly

**50+ built-in commands**:
- `"open notepad"` / `"np"` → Notepad
- `"calc"` → Calculator  
- `"tile windows"` → Organizes all windows
- `"mute"` → Mutes sound
- `"help"` → Shows all commands

### 2. **Self-Improving System** (Ready Now!)
Agent learns from your usage and optimizes itself

**Say**: `"Optimize the command system"`

**Agent does**:
1. Analyzes your usage data
2. Adds patterns for failed searches
3. Creates aliases for popular commands
4. Optimizes automation scripts
5. Commits changes locally
6. Next session → Improved!

### 3. **Automation Scripts** (Examples Included)
JSON-powered autonomous workflows

**Try**: Press `Ctrl+Shift+D` → Demo cascade runs

**Files**: `.ai/automation-scripts/`
- `demo-cascade.json` - Window cascade demo
- `organize-workspace.json` - Opens & tiles common programs

### 4. **State Persistence** (Code Ready)
Never lose work on page refresh

**Files**: 
- `localfirst-sw.js` - Service worker
- `localfirst-state-manager.js` - State management
- `localfirst-command-parser.js` - Command parser

---

## ⚡ Quick Commands

### Use the System
```
"open notepad"          # Opens Notepad
"calc"                  # Opens Calculator (alias)
"tile windows"          # Tiles all windows
"help"                  # Shows command list
"tell me a joke"        # Clippy tells joke
```

### Optimize the System
```
"Optimize the command system"
"Add patterns for failed searches"
"Create aliases for common commands"
"Run weekly optimization"
```

### View What's Happening
```
"Show me the changelog"
"What optimizations have been made?"
"Show command stats"
```

---

## 📁 Key Files

### For Users
- **QUICKSTART.md** (this file) - Start here
- **DATA-SLOSHING-STEWARD-GUIDE.md** - How to use the steward agent
- **command-mappings.json** - All 50+ text commands

### For Developers
- **DATA-SLOSHING-ARCHITECTURE.md** - Complete system design
- **command-parser-integration.md** - Integration guide
- **state-persistence-integration-guide.md** - State system guide

### For AI Agents
- **windows95-api-manifest.json** - Complete API documentation
- **automation-script-schema.json** - Script format spec
- **data-sloshing-changelog.json** - Change history

---

## 🤖 The Agents

### 1. Data Sloshing Steward
**Autonomous data manager** - learns from usage and optimizes

**Invoke**: Say "Optimize the command system"

**Does**:
- Analyzes usage patterns
- Adds command patterns
- Creates aliases
- Optimizes scripts
- Commits changes

### 2. Windows 95 Adaptive Polisher  
**Feature enhancer** - morphs app based on feedback

**Invoke**: Say "Make Clippy more lively"

**Does**:
- Reads API manifest
- Extracts true intent
- Makes improvements
- Preserves Win95 authenticity

---

## 🌊 How It Works

### The Self-Improving Loop
```
Week 1: Use emulator → Data collected
Week 2: Say "optimize" → Agent learns patterns
Week 3: New commands added → Better UX
Week 4: Use more → More data → Better insights
... ∞: System gets smarter forever
```

### Example Evolution
```
Day 1:  Type "text editor" → ❌ Not found
Day 2:  Agent sees failed search 5x
Day 3:  Agent adds "text editor" → notepad mapping
Day 4:  Type "text editor" → ✅ Notepad opens!
```

---

## 📊 What Gets Optimized

### Commands
- New patterns based on what you type
- Aliases for frequently used commands  
- Reordering by popularity for speed

### Scripts
- Reduced delays (500ms → 300ms)
- Removed redundant steps
- Better error handling

### State
- Optimized save size
- Faster restore
- Better migrations

---

## 🎨 Try It Now

### 1. Type a Natural Language Command
Open Clippy chat, type:
```
"open calculator"
```

Calculator opens! ✅

### 2. Use an Alias
Type:
```
"calc"
```

Still works! Ultra-short! ✅

### 3. Try a Fuzzy Match (Typo)
Type:
```
"opn notpad"
```

Notepad opens anyway! Fuzzy matching! ✅

### 4. Trigger Automation
Press: **Ctrl+Shift+D**

Demo windows cascade! ✅

### 5. Let the Agent Optimize
After using for a week, say:
```
"Optimize the command system based on usage"
```

Agent analyzes and improves! ✅

---

## 📚 Learn More

- **QUICKSTART.md** (this file) - You are here
- **DATA-SLOSHING-STEWARD-GUIDE.md** - Complete agent guide
- **DATA-SLOSHING-ARCHITECTURE.md** - Full technical design
- **README.md** - Daily briefing system (different feature)

---

## 🔥 Power User Tips

### Ultra-Short Aliases
```
np      → open notepad
calc    → calculator
ie      → internet explorer
fe      → file explorer
cmd     → terminal
tm      → task manager
cp      → control panel
vol     → volume up
```

### Command Palette
Press **Ctrl+K** → Command palette appears
Type command → Execute instantly

### Voice Control
Enable Web Speech API:
```javascript
recognition.start();
// Then say: "open notepad"
```

### Custom Commands
Create `.ai/user-commands.json`:
```json
{
  "customCommands": [{
    "id": "my-command",
    "patterns": ["do cool thing"],
    "action": "openProgram",
    "params": {"programName": "notepad"}
  }]
}
```

---

## ✨ The Magic

All of this works:
- ✅ **Offline** (no network needed)
- ✅ **Instantly** (<5ms command execution)
- ✅ **Autonomously** (scripts run without AI)
- ✅ **Locally** (everything cached)
- ✅ **Persistently** (optimizations commit to JSON)

**Pure data sloshing.** 🌊

---

**Ready to use?** Just start typing commands in Clippy chat!

**Ready to optimize?** Say "Optimize the command system" after a week of use!

**Ready to build?** Read DATA-SLOSHING-ARCHITECTURE.md!
