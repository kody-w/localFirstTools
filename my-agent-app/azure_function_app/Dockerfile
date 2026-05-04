FROM python:3.11-slim

LABEL maintainer="kodywildfeuer"
LABEL description="Copilot Agent 365 - Enterprise AI Assistant with Ollama/Azure OpenAI support"
LABEL version="1.0.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask gunicorn

# Copy application code
COPY . .

# Create __init__.py files for Python modules
RUN find . -type d -name "agents" -exec touch {}/__init__.py \;
RUN find . -type d -name "utils" -exec touch {}/__init__.py \;

# Create local storage directories
RUN mkdir -p local_storage/my-local-agent-share/memory \
           local_storage/my-local-agent-share/agents \
           local_storage/my-local-agent-share/demos \
           local_storage/my-local-agent-share/multi_agents \
           local_storage/my-local-agent-share/agent_config/c0p110t0-aaaa-bbbb-cccc-123456789abc/

# Environment variables with defaults
ENV USE_OLLAMA=true
ENV OLLAMA_API_BASE_URL=http://ollama:11434/v1
ENV OLLAMA_MODEL_NAME=llama3.1
ENV ASSISTANT_NAME=CopilotAgent365
ENV CHARACTERISTIC_DESCRIPTION="a helpful enterprise AI assistant"
ENV USE_AZURE_STORAGE=false
ENV LOCAL_STORAGE_BASE_PATH=/app/local_storage

EXPOSE 7071

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7071/ || exit 1

# Run with gunicorn for production
CMD ["python", "-m", "azure.functions"]
