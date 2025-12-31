---
description: Interact with NeuAI - your AI assistant with persistent memory
argument-hint: <command> [args] - try: chat, remember, recall, status
---

# NeuAI Command

Interact with NeuAI, a zero-dependency AI assistant powered by Azure OpenAI with persistent memory capabilities.

## Available Subcommands

Based on the argument provided, execute the appropriate NeuAI bridge command:

### Chat (default)
If the argument is a message or no specific command is given:
```bash
python3 ~/.neuai/neuai-agent-bridge.py chat "$ARGUMENTS"
```

### Remember
If the argument starts with "remember":
```bash
python3 ~/.neuai/neuai-agent-bridge.py remember "<content>" --type <type> --importance <1-5>
```
Types: fact, preference, insight, task

### Recall
If the argument starts with "recall" or "search":
```bash
python3 ~/.neuai/neuai-agent-bridge.py recall <keywords>
```

### Memories
If the argument is "memories" or "list":
```bash
python3 ~/.neuai/neuai-agent-bridge.py memories
```

### Status
If the argument is "status" or "test":
```bash
python3 ~/.neuai/neuai-agent-bridge.py status
```

### History
If the argument is "history":
```bash
python3 ~/.neuai/neuai-agent-bridge.py history
```

### New Conversation
If the argument is "new" or "reset":
```bash
python3 ~/.neuai/neuai-agent-bridge.py new
```

### Multi-Subject Commands
- `link <memory_id> <subject_id>` - Link memory to additional subject
- `unlink <memory_id> <subject_id>` - Remove memory from subject
- `subjects` - List all subjects with memory counts

## Usage Examples

```
/neuai What is the weather like today?
/neuai remember User prefers dark mode --type preference --importance 4
/neuai recall project preferences
/neuai memories
/neuai status
/neuai new
```

## Response Handling

All NeuAI responses are JSON. Parse and present the response clearly to the user:

```json
{
  "success": true,
  "command": "chat",
  "response": "...",
  "timestamp": "..."
}
```

If `success` is false, check:
1. NeuAI is installed: `ls ~/.neuai/neuai-cli.py`
2. Config exists: `cat ~/.neuai/config.json`
3. Run setup if needed: `python3 ~/.neuai/neuai-cli.py --setup`

## Installation Check

Before executing, verify NeuAI is installed:
```bash
if [ ! -f ~/.neuai/neuai-agent-bridge.py ]; then
    echo "NeuAI not installed. Visit: https://kody-w.github.io/localFirstTools/docs/neuai/"
fi
```

## Local Project Context

If a local `.neuai/identity.json` exists in the current project, NeuAI will automatically use project-local memories. This enables project-specific context without affecting global memories.
