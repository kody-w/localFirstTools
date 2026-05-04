# Copilot Agent 365

🤖 **Your Local AI Assistant** - Enterprise-grade AI powered by Llama 3.1, running entirely on your machine.

[![Docker Hub](https://img.shields.io/docker/pulls/kodywf/copilot-agent-365)](https://hub.docker.com/r/kodywf/copilot-agent-365)
[![GitHub](https://img.shields.io/github/stars/kody-w/copilot-agent-365-docker)](https://github.com/kody-w/copilot-agent-365-docker)

---

## 🚀 Quick Install (Claude Code)

**The easiest way to install** - Just have [Claude Code](https://claude.ai/code) and say:

```
"Install Copilot Agent 365"
```

That's it! Claude Code handles everything:
- ✅ Checks system requirements
- ✅ Installs Docker if needed
- ✅ Downloads all components
- ✅ Configures everything
- ✅ Starts the AI assistant
- ✅ Opens the web UI

### First Time Setup

1. **Install Claude Code** (if you haven't): https://claude.ai/code

2. **Download the operator agent:**
   ```bash
   mkdir -p ~/.claude/agents
   curl -o ~/.claude/agents/copilot-agent-365-operator.md \
     https://raw.githubusercontent.com/kody-w/copilot-agent-365-docker/main/.claude/agents/copilot-agent-365-operator.md
   ```

3. **In Claude Code, just say:**
   ```
   "Install Copilot Agent 365"
   ```

4. **Done!** Open http://localhost:7071 and start chatting.

---

## 📋 What Claude Code Can Do For You

Once the agent is installed, you can ask Claude Code to:

| Say This | What Happens |
|----------|--------------|
| `"Install Copilot Agent 365"` | Full installation from scratch |
| `"Start the agent"` | Starts all services |
| `"Stop the agent"` | Stops all services |
| `"Status"` | Shows health and resource usage |
| `"Logs"` | Shows recent activity |
| `"Update"` | Updates to latest version |
| `"Change model to mistral"` | Switches AI model |
| `"Use GPU"` | Enables NVIDIA acceleration |
| `"Reset"` | Complete fresh start |
| `"It's not working"` | Full diagnostics |

---

## 🔧 Manual Install (Alternative)

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/kody-w/copilot-agent-365-docker.git
cd copilot-agent-365-docker

# Start with Docker Compose (CPU)
docker compose -f docker-compose.cpu.yml up -d

# Watch for "Model ready!" message
docker logs -f ollama

# Open the UI
open http://localhost:7071
```

---

## 🐳 Docker Hub

Pull directly from Docker Hub:

```bash
docker pull kodywf/copilot-agent-365:latest
```

**Tags:**
- `latest` - Most recent stable release
- `1.0.0` - Initial release with Llama 3.1

---

## ⚙️ Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL_NAME` | `llama3.1` | AI model to use |
| `FUNCTION_APP_PORT` | `7071` | Web UI port |
| `USE_OLLAMA` | `true` | Use local Ollama |
| `ASSISTANT_NAME` | `CopilotAgent365` | Bot display name |

### Available Models

- `llama3.1` - Default, balanced (4.7GB)
- `llama3.1:8b` - Smaller, faster (4.7GB)
- `llama3.1:70b` - Larger, smarter (40GB)
- `codellama` - Code-focused
- `mistral` - Fast and capable
- `phi3` - Microsoft's compact model

---

## 🖥️ System Requirements

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **8GB+ RAM** - For running Llama 3.1
- **10GB+ Disk** - For Docker images and model
- **Optional: NVIDIA GPU** - For faster responses

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Your Browser                   │
│         http://localhost:7071            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Docker Compose                   │
├─────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────┐ │
│  │   Agent     │◄──►│     Ollama      │ │
│  │  (Python)   │    │  (Llama 3.1)    │ │
│  │  Port 7071  │    │  Port 11434     │ │
│  └─────────────┘    └─────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 🔒 Privacy

- **100% Local** - No data leaves your machine
- **No API Keys** - Uses local Ollama
- **No Telemetry** - We don't track anything
- **Your Data** - Stored only in `./local_data/`

---

## 🆘 Troubleshooting

**Slow responses?**
- CPU mode takes 30-60 seconds per response
- Use GPU mode if you have NVIDIA: `docker compose up -d`
- Or use smaller model: `llama3.1:8b`

**Port conflict?**
```bash
lsof -ti:7071 | xargs kill -9
docker compose -f docker-compose.cpu.yml up -d
```

**Out of memory?**
- Increase Docker Desktop memory limit
- Or use smaller model in `.env`

**Need help?**
- In Claude Code: `"Diagnose Copilot Agent 365"`
- Or [open an issue](https://github.com/kody-w/copilot-agent-365-docker/issues)

---

## 📜 License

MIT License - Use it however you want.

---

## 🙏 Credits

- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Llama 3.1](https://llama.meta.com/) - Meta's open source LLM
- [Claude Code](https://claude.ai/code) - AI-powered development

---

**Made with ❤️ by [Kody Wildfeuer](https://github.com/kody-w)**
