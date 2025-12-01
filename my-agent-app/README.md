# Copilot Agent 365

Enterprise AI Assistant powered by Ollama (Llama 3.1) or Azure OpenAI.

## Quick Start

```bash
# Pull the image
docker pull kodywf/copilot-agent-365:latest

# Run with docker-compose (includes Ollama)
curl -O https://raw.githubusercontent.com/kody-w/m365-agents-for-python/main/localFirstTools/my-agent-app/docker-compose.cpu.yml
docker compose -f docker-compose.cpu.yml up -d
```

Access the UI at: **http://localhost:7071**

## Features

- Local-first AI assistant using Llama 3.1 via Ollama
- Optional Azure OpenAI integration
- Modular agent architecture
- Persistent memory across sessions
- Web-based chat interface
- JSON import/export for data portability

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_OLLAMA` | `true` | Use Ollama instead of Azure OpenAI |
| `OLLAMA_MODEL_NAME` | `llama3.1` | Ollama model to use |
| `OLLAMA_API_BASE_URL` | `http://ollama:11434/v1` | Ollama API endpoint |
| `ASSISTANT_NAME` | `CopilotAgent365` | Display name for the assistant |
| `FUNCTION_APP_PORT` | `7071` | Port for the web interface |

## Docker Compose

### With GPU (NVIDIA)
```yaml
version: '3.8'
services:
  agent_function:
    image: kodywf/copilot-agent-365:latest
    ports:
      - "7071:7071"
    environment:
      USE_OLLAMA: "true"
      OLLAMA_API_BASE_URL: "http://ollama:11434/v1"
      OLLAMA_MODEL_NAME: "llama3.1"
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  ollama_models:
```

### CPU Only
```yaml
version: '3.8'
services:
  agent_function:
    image: kodywf/copilot-agent-365:latest
    ports:
      - "7071:7071"
    environment:
      USE_OLLAMA: "true"
      OLLAMA_API_BASE_URL: "http://ollama:11434/v1"
      OLLAMA_MODEL_NAME: "llama3.1"
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama

volumes:
  ollama_models:
```

## Azure OpenAI Mode

To use Azure OpenAI instead of Ollama:

```bash
docker run -p 7071:7071 \
  -e USE_OLLAMA=false \
  -e AZURE_OPENAI_API_KEY=your-key \
  -e AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/ \
  -e AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o \
  kodywf/copilot-agent-365:latest
```

## Tags

- `latest` - Most recent build
- `1.0.0` - Initial release with Llama 3.1 support

## Source

GitHub: [m365-agents-for-python](https://github.com/kody-w/m365-agents-for-python)

## License

MIT
