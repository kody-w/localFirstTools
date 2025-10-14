# 🤖 Data Sloshing Agent Hierarchy

Complete guide to all agents and when to use them.

---

## 🌊 The Sloshing Steward (MASTER)

**File**: `.claude/agents/sloshing-steward.md`

**Role**: Master orchestrator of ALL data sloshing systems

**Invoke**: `"Run the sloshing steward"`

**What it does**:
- ✅ Coordinates all other agents
- ✅ Health checks across all systems
- ✅ Optimizes commands, scripts, state, APIs
- ✅ Commits all changes to git
- ✅ Generates comprehensive reports
- ✅ Weekly/monthly maintenance

**When to use**:
- Weekly optimization runs
- Monthly deep maintenance
- Emergency system fixes
- Comprehensive health checks
- When you want everything optimized

**Time**: 25-30 minutes (full run)

**Output**: Complete report + all optimizations + git commit

---

## 📊 Data Sloshing Steward (SPECIALIST)

**File**: `.claude/agents/data-sloshing-steward.md`

**Role**: Focused data optimization specialist

**Invoke**: `"Optimize the command system"`

**What it does**:
- ✅ Learns from usage patterns
- ✅ Adds command patterns based on failed searches
- ✅ Creates aliases for popular commands
- ✅ Optimizes automation scripts
- ✅ Updates changelog
- ✅ Commits to git

**When to use**:
- Focused command system optimization
- Script performance tuning
- After noticing failed searches
- When you want targeted optimization

**Time**: 15-20 minutes

**Output**: Command/script optimizations + git commit

**Invoked by**: Sloshing Steward (master) or direct

---

## 🎨 Windows 95 Adaptive Polisher (SPECIALIST)

**File**: `.claude/agents/windows95-adaptive-polisher.md`

**Role**: Feature enhancement and UX improvement

**Invoke**: `"Make Clippy more lively"` or `"Polish this feature"`

**What it does**:
- ✅ Morphs emulator based on feedback
- ✅ Extracts true intent from vague requests
- ✅ Enhances features while preserving Win95 authenticity
- ✅ Reads API manifest for capabilities
- ✅ Makes bold improvements

**When to use**:
- Improving existing features
- Making UX enhancements
- Adding polish and delight
- When you have feature feedback

**Time**: 10-30 minutes (varies by task)

**Output**: Code changes + feature improvements

**Invoked by**: Sloshing Steward (master) or direct

---

## 🏗️ Digital Twin Builder (SPECIALIST)

**File**: `.claude/agents/digital-twin-builder.md`

**Role**: Application creation from JSON

**Invoke**: `"Create a meditation timer app"`

**What it does**:
- ✅ Reads digital twin context
- ✅ Studies existing instruction files
- ✅ Generates new JSON applications
- ✅ Validates API usage
- ✅ Updates digital twin

**When to use**:
- Building new applications
- Creating automation workflows
- Generating instruction files
- When you need new functionality

**Time**: 15-30 minutes

**Output**: New JSON instruction files

**Invoked by**: Direct (not by master orchestrator)

---

## 🎮 Windows 95 AI Controller (SPECIALIST)

**File**: `.claude/agents/windows95-ai-controller.md`

**Role**: Real-time emulator control

**Invoke**: `"Control the Windows 95 emulator"`

**What it does**:
- ✅ Real-time window management
- ✅ Daily briefing generation
- ✅ Live program execution
- ✅ State manipulation
- ✅ Telemetry monitoring

**When to use**:
- Daily briefing creation
- Real-time automation
- Live system control
- Emulator demonstrations

**Time**: Continuous (real-time)

**Output**: Live actions + briefing state files

**Invoked by**: Direct (not by master orchestrator)

---

## 🎯 When to Use Which Agent

### For Weekly Maintenance
```
Use: Sloshing Steward (Master)
Command: "Run the sloshing steward"
Why: Comprehensive optimization of everything
```

### For Command Optimization
```
Use: Data Sloshing Steward (Specialist)
Command: "Optimize the command system"
Why: Focused on command/script improvements
```

### For Feature Enhancement
```
Use: Windows 95 Adaptive Polisher (Specialist)
Command: "Make Clippy more animated"
Why: Feature polish and UX improvements
```

### For Building New Apps
```
Use: Digital Twin Builder (Specialist)
Command: "Create a meditation timer"
Why: Generates new JSON applications
```

### For Real-Time Control
```
Use: Windows 95 AI Controller (Specialist)
Command: "Generate today's briefing"
Why: Live emulator control and briefings
```

---

## 📊 Agent Comparison

| Agent | Scope | Time | Frequency | Commits | Output |
|-------|-------|------|-----------|---------|--------|
| **Sloshing Steward** | All systems | 30 min | Weekly | Yes | Full report + commits |
| **Data Steward** | Commands/scripts | 20 min | As needed | Yes | Optimizations + commit |
| **Adaptive Polisher** | Features/UX | 10-30 min | As needed | No* | Code changes |
| **Digital Twin** | New apps | 15-30 min | As needed | No* | JSON files |
| **AI Controller** | Real-time | Continuous | Daily | No | Live actions |

*May commit depending on changes

---

## 🔄 The Hierarchy

```
┌─────────────────────────────────────┐
│   🌊 Sloshing Steward (MASTER)      │
│   - Orchestrates everything         │
│   - Weekly/monthly maintenance      │
└────────────┬────────────────────────┘
             │
             ├──> 📊 Data Sloshing Steward
             │    (Commands & Scripts)
             │
             ├──> 🎨 Adaptive Polisher
             │    (Features & UX)
             │
             └──> Can invoke other agents
                  as needed


Standalone Specialists:
┌─────────────────────────────────────┐
│   🏗️ Digital Twin Builder           │
│   (New applications)                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   🎮 Windows 95 AI Controller       │
│   (Real-time control)               │
└─────────────────────────────────────┘
```

---

## 💡 Recommended Workflow

### Daily
```
Morning: Use emulator naturally
         Type commands, run scripts
         Don't worry about failures
```

### Weekly
```
Friday: "Run the sloshing steward"
        ↓
        Agent analyzes usage
        Optimizes all systems
        Commits changes
        ↓
        Review report
        ↓
        Next week: Enjoy improvements!
```

### Monthly
```
First Friday: "Steward monthly"
              ↓
              Deep system clean
              Performance benchmarking
              Archive old data
              ↓
              Review analytics
```

### As Needed
```
Feature idea: "Polish this feature" (Adaptive Polisher)
New app: "Create X app" (Digital Twin Builder)
Briefing: "Generate today's briefing" (AI Controller)
Emergency: "Steward emergency" (Sloshing Steward)
```

---

## 🎓 Learning Path

### Beginner: Use One Agent
```
Week 1: Learn the emulator
Week 2: "Run the sloshing steward"
Week 3: Review results
Week 4: Repeat weekly
```

### Intermediate: Use Multiple Agents
```
Weekly: "Run the sloshing steward"
As needed: "Optimize the command system"
As needed: "Polish this feature"
```

### Advanced: Full Ecosystem
```
Weekly: Sloshing Steward (master)
Daily: AI Controller (briefings)
As needed: Adaptive Polisher (features)
As needed: Digital Twin Builder (new apps)
As needed: Data Steward (focused optimization)
```

---

## 📝 Quick Reference

### Master Orchestrator
```bash
"Run the sloshing steward"        # Full run (30 min)
"Steward check"                   # Health check (5 min)
"Steward weekly"                  # Weekly run (20 min)
"Steward monthly"                 # Monthly run (30 min)
"Steward emergency"               # Emergency fix (10 min)
```

### Specialists
```bash
"Optimize the command system"     # Data Steward
"Make Clippy more lively"         # Adaptive Polisher
"Create a meditation timer"       # Digital Twin Builder
"Generate today's briefing"       # AI Controller
```

---

## 🏆 Success Metrics

### After Using Sloshing Steward (Weekly)
```
Health Score: 72 → 95 (+23)
Command Match: 82% → 94% (+12%)
Script Speed: 3.2s → 2.1s (-34%)
Failed Searches: 23 → 6 (-74%)
```

### After Using Data Steward
```
New Patterns: +7
New Aliases: +3
Match Rate: +8%
Failed Searches: -60%
```

### After Using Adaptive Polisher
```
Feature Polish: High
UX Improvements: Multiple
User Delight: Increased
Win95 Authenticity: Preserved
```

---

## 🎯 Bottom Line

**One Agent for Everything**:
```
"Run the sloshing steward" → Everything optimized
```

**Specialists When Needed**:
```
Commands: "Optimize the command system"
Features: "Polish this feature"
New apps: "Create X app"
Briefings: "Generate today's briefing"
```

**The Result**:
- Self-improving system
- Optimized weekly
- All changes committed
- Continuous evolution

---

**The Agent Hierarchy: From master orchestrator to focused specialists, all working together to keep your data sloshing system running perfectly.** 🌊✨
