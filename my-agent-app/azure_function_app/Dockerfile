FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask

COPY . .
RUN find . -type d -name "agents" -exec touch {}/__init__.py \;
RUN find . -type d -name "utils" -exec touch {}/__init__.py \;
RUN mkdir -p local_storage/my-local-agent-share/memory \
           local_storage/my-local-agent-share/agents \
           local_storage/my-local-agent-share/demos \
           local_storage/my-local-agent-share/multi_agents \
           local_storage/my-local-agent-share/agent_config/c0p110t0-aaaa-bbbb-cccc-123456789abc/

EXPOSE 7071
CMD ["python", "server.py"]
