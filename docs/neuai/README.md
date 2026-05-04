# NeuAI

A zero-dependency AI assistant CLI powered by Azure OpenAI with persistent memory and project-aware context.

## Overview

NeuAI is a self-contained Python CLI that provides:

- **Persistent Memory**: Remember facts, preferences, and context across sessions
- **Project Isolation**: Each project can have its own memory and identity
- **Zero Dependencies**: Uses only Python standard library (no pip install required)
- **Claude Code Integration**: Programmatic bridge for AI agent automation
- **Secure Credentials**: API keys stored with restrictive permissions

## Quick Start

### 1. Install

```bash
# Copy files to ~/.neuai
mkdir -p ~/.neuai
cp neuai-cli.py ~/.neuai/
cp neuai-agent-bridge.py ~/.neuai/
chmod +x ~/.neuai/neuai-cli.py

# Optional: Add to PATH
mkdir -p ~/.local/bin
ln -sf ~/.neuai/neuai-cli.py ~/.local/bin/neuai
```

### 2. Configure

Run NeuAI for the first time to set up credentials:

```bash
python3 ~/.neuai/neuai-cli.py
```

You'll be prompted for:
- **Azure OpenAI Endpoint**: Your Azure OpenAI resource URL
- **API Key**: Your Azure OpenAI API key
- **Deployment Name**: Your model deployment (e.g., `gpt-4`, `gpt-5.2-chat`)
- **API Version**: API version (e.g., `2025-01-01-preview`)

### 3. Use

```bash
# Interactive mode
neuai

# Single message
neuai --message "What is the capital of France?"

# Test connection
neuai --test
```

## Commands

### Interactive Mode

Once in the interactive CLI, use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/new` | Start a new conversation (keeps memories) |
| `/memory` | View stored memories |
| `/remember <text>` | Store a new memory |
| `/forget` | Clear all memories |
| `/status` | Show connection and config info |
| `/export` | Export conversation to file |
| `/exit` or `/quit` | Exit NeuAI |

### CLI Flags

```bash
neuai --help              # Show help
neuai --test              # Test Azure OpenAI connection
neuai --configure         # Re-run setup wizard
neuai --reset             # Reset all configuration
neuai --message "text"    # Send single message and exit
neuai --global            # Force use of global ~/.neuai (ignore local)
```

## Project-Specific Usage

NeuAI supports project-local memory and context. When you run NeuAI from within a directory that contains a `.neuai` folder, it will use that folder for data storage while still loading credentials from your global `~/.neuai/config.json`.

### Setting Up a Project

```bash
# Navigate to your project
cd ~/my-project

# Create local .neuai directory
mkdir -p .neuai/data

# Create project identity
cat > .neuai/identity.json << 'EOF'
{
  "user_guid": "my-project-001",
  "project": "my-project",
  "created": "2025-12-25T00:00:00",
  "scope": "project"
}
EOF

# Initialize data files
echo '{"my-project-001": []}' > .neuai/data/memories.json
echo '[]' > .neuai/data/conversations.json
echo '{"project": "my-project"}' > .neuai/data/context.json

# Add to .gitignore (recommended)
echo '.neuai/' >> .gitignore
```

### How It Works

```
~/my-project/
├── .neuai/                    # Project-local data
│   ├── identity.json          # Project GUID
│   └── data/
│       ├── memories.json      # Project memories
│       ├── context.json       # Project context
│       └── conversations.json # Conversation history
├── src/
└── ...

~/.neuai/                      # Global (always exists)
├── config.json                # API credentials (shared)
├── neuai-cli.py               # Main CLI
├── neuai-agent-bridge.py      # Agent bridge
└── data/                      # Fallback global data
    ├── memories.json
    └── ...
```

**Priority Order:**
1. Local `.neuai/` in current or parent directory → used for data
2. Global `~/.neuai/config.json` → always used for credentials
3. Global `~/.neuai/data/` → used if no local `.neuai/` found

## Claude Code Integration

NeuAI includes a programmatic bridge (`neuai-agent-bridge.py`) that allows Claude Code to interact with NeuAI on your behalf.

### Bridge Commands

All commands return JSON for reliable parsing:

```bash
# Chat
python3 ~/.neuai/neuai-agent-bridge.py chat "Hello, what can you do?"

# Store memory
python3 ~/.neuai/neuai-agent-bridge.py remember "User prefers dark mode" --type preference --importance 5

# Retrieve memories
python3 ~/.neuai/neuai-agent-bridge.py memories

# Search memories
python3 ~/.neuai/neuai-agent-bridge.py recall "dark mode" "preferences"

# Get status
python3 ~/.neuai/neuai-agent-bridge.py status

# Start new conversation
python3 ~/.neuai/neuai-agent-bridge.py new

# Get conversation history
python3 ~/.neuai/neuai-agent-bridge.py history 20

# Test connection
python3 ~/.neuai/neuai-agent-bridge.py test

# Multi-turn conversation
python3 ~/.neuai/neuai-agent-bridge.py multi "Hello" "What's 2+2?" "Thanks!"
```

### Example Output

```json
{
  "success": true,
  "command": "chat",
  "input": "Hello",
  "response": "Hello! How can I help you today?",
  "timestamp": "2025-12-25T12:00:00"
}
```

### Memory Types

When storing memories, use these types:

| Type | Description |
|------|-------------|
| `fact` | General facts about the user or project |
| `preference` | User preferences and settings |
| `insight` | Observations or learned patterns |
| `task` | Things to do or remember |

### Importance Levels

| Level | Description |
|-------|-------------|
| 1 | Low importance (nice to know) |
| 2 | Minor importance |
| 3 | Normal importance (default) |
| 4 | High importance |
| 5 | Critical importance (never forget) |

## Directory Structure

```
~/.neuai/
├── config.json              # API credentials (chmod 600)
├── identity.json            # Global user GUID
├── neuai-cli.py             # Main CLI application
├── neuai-agent-bridge.py    # Programmatic interface
├── neuai-test-suite.py      # Test suite
└── data/
    ├── memories.json        # Persistent memories
    ├── context.json         # Session context
    └── conversations.json   # Conversation history
```

## Configuration File

The `config.json` file stores your Azure OpenAI credentials:

```json
{
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_key": "your-api-key",
  "deployment": "gpt-4",
  "api_version": "2025-01-01-preview"
}
```

**Security**: This file is created with `chmod 600` permissions (owner read/write only).

## Environment Variables

You can override configuration with environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_KEY="your-api-key"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"
export AZURE_OPENAI_API_VERSION="2025-01-01-preview"
```

Environment variables take priority over saved configuration.

## API Compatibility

NeuAI automatically handles Azure OpenAI API differences:

| API Version | Notes |
|-------------|-------|
| `2024-02-15-preview` | Uses `max_tokens`, supports `temperature` |
| `2024-10-*` and later | Uses `max_completion_tokens` |
| `2025-*` | Uses `max_completion_tokens`, temperature fixed at 1.0 |

## Troubleshooting

### Connection Failed

```bash
# Test connection
neuai --test

# Check config
cat ~/.neuai/config.json

# Verify endpoint format
# Should be: https://YOUR-RESOURCE.openai.azure.com/
```

### Wrong Deployment

If you see errors about model capabilities:

```bash
# Reconfigure
neuai --configure
```

### Permission Denied

```bash
# Fix permissions
chmod 600 ~/.neuai/config.json
chmod 700 ~/.neuai
```

### Memories Not Persisting

Check which directory is being used:

```bash
python3 ~/.neuai/neuai-agent-bridge.py status
```

Look at `data_dir` in the output to see where data is stored.

### Local vs Global Confusion

Force global mode to bypass local `.neuai`:

```bash
neuai --global
```

## Testing

Run the test suite to verify everything works:

```bash
python3 ~/.neuai/neuai-test-suite.py
```

This runs 17 tests covering:
- Configuration loading
- Connection testing
- Chat functionality
- Memory operations
- Conversation management
- Agent tools

## Requirements

- **Python 3.7+** (uses standard library only)
- **Azure OpenAI Resource** with a deployed model
- **Network Access** to Azure OpenAI endpoint

## License

MIT License - Use freely in your projects.

---

## Quick Reference Card

```bash
# Setup
neuai --configure          # Configure credentials
neuai --test               # Test connection

# Interactive
neuai                      # Start interactive mode
/help                      # Show commands
/memory                    # View memories
/remember <text>           # Store memory
/new                       # New conversation
/exit                      # Exit

# Programmatic (for scripts/agents)
python3 ~/.neuai/neuai-agent-bridge.py chat "message"
python3 ~/.neuai/neuai-agent-bridge.py remember "fact"
python3 ~/.neuai/neuai-agent-bridge.py memories
python3 ~/.neuai/neuai-agent-bridge.py status
```
