# NeuAI Quick Start (localFirstTools)

This is a project-local NeuAI instance for the localFirstTools collection.

## Using NeuAI Here

From this directory, NeuAI will automatically use local memory:

```bash
# Chat (from localFirstTools directory)
python3 neuai-agent-bridge.py chat "What do you know about this project?"

# Store project-specific memory
python3 neuai-agent-bridge.py remember "Important project fact" --importance 4

# View memories
python3 neuai-agent-bridge.py memories

# Check status (shows local data_dir)
python3 neuai-agent-bridge.py status
```

## Directory Structure

```
.neuai/
├── QUICKSTART.md        # This file
├── identity.json        # Project GUID: localFirstTools-project-001
└── data/
    ├── memories.json    # Project memories
    ├── context.json     # Project context
    └── conversations.json
```

## Credentials

API credentials are loaded from `~/.neuai/config.json` (global).
Project data stays local and isolated.

## Full Documentation

See: `docs/neuai/README.md`
