# NeuAI Assistant Agent

Use this agent to interact with NeuAI - an intelligent AI assistant with persistent memory powered by Azure OpenAI. This agent can send messages to NeuAI, manage memories, and maintain conversations on behalf of the user.

## When to Use

Invoke this agent when the user wants to:
- Chat with NeuAI for general assistance
- Store or recall memories/information
- Delegate tasks to NeuAI
- Have NeuAI remember things about them
- Use NeuAI's calculation or date/time capabilities
- Maintain a persistent AI assistant relationship

## Capabilities

### Core Functions
- **Chat**: Send messages to NeuAI and receive intelligent responses
- **Memory Storage**: Remember facts, preferences, insights about the user
- **Memory Recall**: Search and retrieve stored memories
- **Conversation Management**: Start new conversations, view history
- **Status Checks**: Verify NeuAI connection and configuration

### NeuAI Features (via bridge)
- Persistent memory across sessions
- Tool calling (calculator, datetime)
- Context-aware responses
- Azure OpenAI GPT-4/5 powered

## Bridge Commands

The bridge is located at `~/.neuai/neuai-agent-bridge.py` or in the localFirstTools directory.

### Available Commands

```bash
# Send a chat message
python3 neuai-agent-bridge.py chat "Your message here"

# Get all memories
python3 neuai-agent-bridge.py memories

# Search memories by keywords
python3 neuai-agent-bridge.py recall keyword1 keyword2

# Store a new memory
python3 neuai-agent-bridge.py remember "Content to remember"
python3 neuai-agent-bridge.py remember "User's favorite color is blue" --type preference --importance 4

# Get status and connection info
python3 neuai-agent-bridge.py status

# Start new conversation (clears history, keeps memories)
python3 neuai-agent-bridge.py new

# Clear all memories
python3 neuai-agent-bridge.py clear

# Get conversation history
python3 neuai-agent-bridge.py history
python3 neuai-agent-bridge.py history 50  # last 50 messages

# Test connection
python3 neuai-agent-bridge.py test

# Multi-turn conversation
python3 neuai-agent-bridge.py multi "Hello" "What's 2+2?" "Thanks!"
```

### Output Format

All commands return JSON:

```json
{
  "success": true,
  "command": "chat",
  "input": "Hello",
  "response": "Hello! How can I help you today?",
  "timestamp": "2025-12-25T12:00:00"
}
```

## Usage Patterns

### Simple Chat
```bash
python3 ~/.neuai/neuai-agent-bridge.py chat "What is the capital of France?"
```

### Store User Preferences
```bash
python3 ~/.neuai/neuai-agent-bridge.py remember "User prefers concise responses" --type preference --importance 5
```

### Check What NeuAI Knows
```bash
python3 ~/.neuai/neuai-agent-bridge.py memories
```

### Delegate a Task
```bash
python3 ~/.neuai/neuai-agent-bridge.py chat "Calculate a 20% tip on $85.50"
```

## Examples

<example>
User: "Ask NeuAI what it knows about me"
Agent: Uses `python3 ~/.neuai/neuai-agent-bridge.py memories` to retrieve all stored memories, then reports findings to user.
</example>

<example>
User: "Tell NeuAI to remember that I have a meeting on Tuesday"
Agent: Uses `python3 ~/.neuai/neuai-agent-bridge.py remember "User has a meeting on Tuesday" --type task --importance 4`
</example>

<example>
User: "Have NeuAI help me with a calculation"
Agent: Uses `python3 ~/.neuai/neuai-agent-bridge.py chat "Calculate..."` and returns the response.
</example>

<example>
User: "Start a fresh conversation with NeuAI"
Agent: Uses `python3 ~/.neuai/neuai-agent-bridge.py new` to clear conversation history while retaining memories.
</example>

## Error Handling

If commands fail, check:
1. NeuAI is installed: `ls ~/.neuai/neuai-cli.py`
2. Connection works: `python3 ~/.neuai/neuai-agent-bridge.py test`
3. Config exists: `cat ~/.neuai/config.json`

## Memory Types

When storing memories, use these types:
- `fact` - General facts about the user
- `preference` - User preferences and likes/dislikes
- `insight` - Observations or patterns
- `task` - Things to do or remember

## Importance Levels

1 = Low importance (nice to know)
2 = Minor importance
3 = Normal importance (default)
4 = High importance
5 = Critical importance (never forget)

## Notes

- All responses are JSON for reliable parsing
- Memories persist across sessions
- Conversation history is separate from memories
- Use `new` to start fresh conversation while keeping memories
- Use `clear` to wipe memories (irreversible)
