# Data Sloshing Steward - Agent Guide

## What Is This Agent?

The **Data Sloshing Steward** is an autonomous agent that manages, optimizes, and evolves the static JSON files that power your Windows 95 emulator. While you use the emulator, this agent learns from your behavior and improves the system.

Think of it as the **groundskeeper** of your data sloshing system.

---

## What Does It Do?

### 1. 📊 Learns From Your Usage

The agent monitors:
- Which commands you type
- Which commands fail to match
- How often you use each command
- What automation scripts you run
- Your typing patterns and shortcuts

### 2. 🎯 Optimizes Command Mappings

**Automatically adds patterns based on what you type**:

```
You type: "text editor" (fails 5 times)
         ↓
Agent adds: "text editor" → notepad mapping
         ↓
Next time: "text editor" works instantly! ✓
```

**Creates smart aliases**:

```
You type: "vol up" (frequently)
         ↓
Agent creates: "vol" → volume-up alias
         ↓
Now you can type: "vol" (ultra-short!)
```

### 3. ⚡ Optimizes Automation Scripts

**Removes unnecessary delays**:
```json
// Before
{"action": "openProgram", "delay": 800}
{"action": "wait", "params": {"duration": 500}}

// After (optimized)
{"action": "openProgram", "delay": 300}
// Wait removed - redundant!
```

**Combines redundant steps**:
```json
// Before
{"action": "showToast", "params": {"message": "A"}}
{"action": "wait", "params": {"duration": 100}}
{"action": "showToast", "params": {"message": "B"}}

// After (optimized)
{"action": "showToast", "params": {"message": "A"}, "delay": 100}
{"action": "showToast", "params": {"message": "B"}}
```

### 4. 💾 Commits Changes Locally

All optimizations are saved to your local JSON files:
- `.ai/command-mappings.json` - Command patterns and aliases
- `.ai/automation-scripts/*.json` - Automation scripts
- `.ai/data-sloshing-changelog.json` - Change history

**These changes persist!** Next time you run Windows 95, the improvements are already there.

---

## How to Use

### Option 1: Automatic Optimization

Just say:
```
"Optimize the command system"
"Update command mappings based on usage"
"Improve automation scripts"
```

The agent will:
1. Analyze your usage data
2. Identify improvements
3. Update JSON files
4. Commit changes locally
5. Report what it did

### Option 2: Targeted Optimization

Be specific:
```
"Add new command patterns for failed searches"
"Optimize the demo-cascade script"
"Create aliases for frequently used commands"
```

### Option 3: Scheduled Maintenance

Run weekly or monthly:
```
"Run weekly data optimization"
"Do monthly system cleanup"
```

---

## What Gets Optimized?

### Command Mappings

**Patterns Added**:
- Failed searches with clear intent
- Common variations of existing commands
- Typos that fuzzy matching misses

**Aliases Created**:
- Ultra-short versions of popular commands
- Common abbreviations
- Power user shortcuts

**Example**:
```json
{
  "id": "open-notepad",
  "patterns": [
    "open notepad",      // Original
    "text editor",       // NEW - learned from usage
    "edit text",         // NEW - learned from usage
    "open text"          // NEW - learned from usage
  ]
}
```

### Automation Scripts

**Delays Optimized**:
- Reduced from 500ms → 300ms (if safe)
- Removed redundant waits
- Adjusted based on actual performance

**Steps Combined**:
- Merged sequential actions
- Eliminated no-ops
- Parallelized independent actions

**Error Handling Added**:
- Retry logic for flaky operations
- Graceful degradation
- Better error messages

---

## Usage Data Sources

The agent reads:

### 1. Command Usage Stats (localStorage)
```javascript
{
  "open-notepad": 45,           // Used 45 times
  "open-calculator": 12,        // Used 12 times
  "_input_failed_1": "text editor",  // Failed search
  "_input_failed_2": "vol up"        // Failed search
}
```

### 2. Failed Command Attempts
- Searches that didn't match
- Typos and variations
- Common patterns

### 3. Script Execution Logs
- How long scripts take
- Which steps fail
- Error patterns

---

## Example Session

### You:
> "I've been using the emulator for a week. Optimize the command system."

### Agent Process:

**Step 1: Analyze**
```javascript
Reading localStorage command stats...
Found 127 command executions
Found 23 failed searches

Top failed searches:
1. "text editor" - 8 times
2. "vol" - 5 times
3. "open files" - 4 times
4. "calc app" - 3 times
```

**Step 2: Identify Improvements**
```
Can map:
✓ "text editor" → notepad (high confidence)
✓ "vol" → volume-up (alias)
✓ "open files" → fileExplorer (high confidence)
✓ "calc app" → calculator (high confidence)

Total: 20 failed searches can be resolved
```

**Step 3: Update Files**
```json
// .ai/command-mappings.json
{
  "commandCategories": {
    "programs": {
      "commands": [{
        "id": "open-notepad",
        "patterns": [
          "open notepad",
          "text editor"    // NEW
        ]
      }]
    }
  },
  "commandAliases": {
    "aliases": {
      "vol": "volume-up"  // NEW
    }
  }
}
```

**Step 4: Commit**
```bash
git add .ai/command-mappings.json
git add .ai/data-sloshing-changelog.json

git commit -m "data: optimize command mappings

- Added 'text editor' pattern (8 failed searches)
- Added 'vol' alias (5 failed searches)
- Added 'open files' pattern (4 failed searches)
- Added 'calc app' pattern (3 failed searches)

Impact: Resolves 20/23 (87%) recent failed searches

🤖 Data Sloshing Steward
Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Step 5: Report**
```
✅ Optimization Complete!

Added:
• 4 new command patterns
• 1 new alias

Files updated:
• .ai/command-mappings.json (v1.0.0 → v1.1.0)

Impact:
• Resolves 87% of recent failed searches
• Estimated 20 commands now work that didn't before

Changes committed locally and ready for next session!
```

---

## Validation Rules

The agent follows strict rules:

### ✅ Safe Operations (Automatic)
- Adding new command patterns
- Creating aliases for popular commands
- Optimizing script delays
- Reordering patterns by frequency

### ⚠️ Requires Confirmation
- Removing existing patterns
- Breaking changes to schemas
- Major script restructuring
- Deleting automation scripts

### ❌ Never Allowed
- Breaking backward compatibility
- Removing user-created commands
- Changing action signatures
- Corrupting JSON syntax

---

## Changelog Tracking

Every change is logged in `.ai/data-sloshing-changelog.json`:

```json
{
  "changes": [{
    "timestamp": "2025-10-14T12:00:00Z",
    "version": "1.1.0",
    "agent": "data-sloshing-steward",
    "type": "command-mapping-update",
    "changes": [
      "Added 'text editor' pattern to open-notepad",
      "Created 'vol' alias for volume-up"
    ],
    "impact": "Resolves 20 failed searches",
    "files": [".ai/command-mappings.json"]
  }]
}
```

You can review the full history at any time!

---

## Performance Impact

### Before Optimization:
```
Command: "text editor"
Result: ❌ No match found
```

### After Optimization:
```
Command: "text editor"
Result: ✅ Opens Notepad (0.3ms)
```

### Typical Results:
- **50-90%** reduction in failed searches
- **20-40%** faster script execution
- **100%** of changes persist across sessions

---

## Files Managed

```
.ai/
├── command-mappings.json          ← Patterns & aliases
├── automation-scripts/*.json      ← User automation
├── data-sloshing-changelog.json   ← Change history
├── state-persistence-schema.json  ← State definitions
└── windows95-api-manifest.json    ← API docs

All files are:
✓ Valid JSON
✓ Version controlled
✓ Backward compatible
✓ Locally committed
```

---

## Best Practices

### For Best Results:

1. **Use the emulator naturally** - The more you use it, the better the data
2. **Run optimization weekly** - Fresh data = better insights
3. **Review changelog** - See what's being learned
4. **Report issues** - Tell the agent if something's wrong
5. **Let it learn** - Don't worry about typos, the agent learns from them!

### Commands to Try:

```bash
# Weekly maintenance
"Run weekly optimization"

# After heavy usage
"Optimize based on recent usage"

# Specific improvements
"Add patterns for failed searches"
"Create aliases for common commands"
"Speed up automation scripts"

# Review changes
"Show me the changelog"
"What optimizations have been made?"
```

---

## Advanced: Manual Review

You can manually review the agent's work:

### 1. Check Command Mappings
```bash
cat .ai/command-mappings.json | jq '.commandCategories.programs.commands[] | select(.id == "open-notepad")'
```

### 2. Review Changelog
```bash
cat .ai/data-sloshing-changelog.json | jq '.changes | last'
```

### 3. View Usage Stats
Open browser console:
```javascript
JSON.parse(localStorage.getItem('command-usage-stats'))
```

---

## Troubleshooting

### Issue: Agent added wrong pattern

**Solution**: Tell the agent
```
"Remove the 'xyz' pattern from notepad command"
```

### Issue: Script running slower after optimization

**Solution**: Rollback
```
"Revert the last optimization to demo-cascade script"
```

### Issue: Want to prevent certain optimizations

**Solution**: Configure rules
```
"Don't optimize delays in animation scripts"
"Never remove patterns from calculator command"
```

---

## The Self-Improving Loop

```
Week 1: You use emulator → Data collected
Week 2: Agent optimizes → Commands added
Week 3: Better UX → Use it more
Week 4: More data → Better optimizations
...
∞: System gets smarter forever
```

**The system learns FROM you and FOR you.** 🌊✨

---

## Summary

The Data Sloshing Steward is your personal data scientist:

- ✅ **Learns** from your usage patterns
- ✅ **Optimizes** command mappings automatically
- ✅ **Improves** automation scripts
- ✅ **Commits** changes locally
- ✅ **Tracks** all modifications
- ✅ **Persists** across sessions

**You use it. It learns. It improves. You benefit.**

That's data sloshing at its finest. 🚀
