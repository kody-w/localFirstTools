#!/bin/bash

# setup_agent_app.sh
# This script sets up a local Azure Function + Ollama environment using Docker Compose.

PROJECT_ROOT="my-agent-app"

echo "🚀 Starting setup for $PROJECT_ROOT..."

# 1. Create Directory Structure
echo "📂 Creating directory structure..."
mkdir -p "$PROJECT_ROOT"
mkdir -p "$PROJECT_ROOT/azure_function_app/agents"
mkdir -p "$PROJECT_ROOT/azure_function_app/utils"
mkdir -p "$PROJECT_ROOT/local_data"

cd "$PROJECT_ROOT"

# 2. Create .env file
echo "📝 Creating .env file..."
cat << 'EOF' > .env
# Azure Function App Settings
AZURE_WEBJOBS_STORAGE="DefaultEndpointsProtocol=http;AccountName=[STORAGE_ACCOUNT];AccountKey=[YOUR_ACCOUNT_KEY];BlobEndpoint=http://azurite:10000/[STORAGE_ACCOUNT];QueueEndpoint=http://azurite:10001/[STORAGE_ACCOUNT];TableEndpoint=http://azurite:10002/[STORAGE_ACCOUNT];"
AZURE_OPENAI_API_KEY="[YOUR_API_KEY]"
AZURE_OPENAI_API_VERSION="2024-02-01"
AZURE_OPENAI_ENDPOINT="http://localhost:8000"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-deployment"

# Agent App Configuration
ASSISTANT_NAME="LocalInsightBot"
CHARACTERISTIC_DESCRIPTION="a helpful local AI assistant"

# Ollama Integration
USE_OLLAMA="true"
OLLAMA_API_BASE_URL="http://ollama:11434/v1"
OLLAMA_MODEL_NAME="llama2"

# Local Storage
USE_AZURE_STORAGE="false"
AZURE_FILES_SHARE_NAME="my-local-agent-share"
LOCAL_STORAGE_BASE_PATH="/home/site/wwwroot/local_storage"

# UI Port
FUNCTION_APP_PORT=7071
EOF

# 3. Create docker-compose.yml
echo "🐳 Creating docker-compose.yml..."
cat << 'EOF' > docker-compose.yml
version: '3.8'

services:
  agent_function:
    build:
      context: ./azure_function_app
      dockerfile: Dockerfile
    ports:
      - "${FUNCTION_APP_PORT}:80"
    environment:
      AzureWebJobsStorage: ${AZURE_WEBJOBS_STORAGE}
      FUNCTIONS_WORKER_RUNTIME: python
      AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY}
      AZURE_OPENAI_API_VERSION: ${AZURE_OPENAI_API_VERSION}
      AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT}
      AZURE_OPENAI_DEPLOYMENT_NAME: ${AZURE_OPENAI_DEPLOYMENT_NAME}
      ASSISTANT_NAME: ${ASSISTANT_NAME}
      CHARACTERISTIC_DESCRIPTION: ${CHARACTERISTIC_DESCRIPTION}
      USE_OLLAMA: ${USE_OLLAMA}
      OLLAMA_API_BASE_URL: ${OLLAMA_API_BASE_URL}
      OLLAMA_MODEL_NAME: ${OLLAMA_MODEL_NAME}
      USE_AZURE_STORAGE: ${USE_AZURE_STORAGE}
      AZURE_FILES_SHARE_NAME: ${AZURE_FILES_SHARE_NAME}
      LOCAL_STORAGE_BASE_PATH: ${LOCAL_STORAGE_BASE_PATH}
    volumes:
      - ./local_data:/home/site/wwwroot/local_storage
    depends_on:
      - ollama
    networks:
      - agent_network

  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    command: >
      bash -c "
      ollama serve &
      echo 'Waiting for Ollama server to be ready...'
      while ! curl -s http://localhost:11434/api/tags > /dev/null; do sleep 1; done
      echo 'Ollama server ready. Pulling model...'
      ollama pull ${OLLAMA_MODEL_NAME} || echo 'Model pull failed or model already exists.'
      wait -n
      exit $?
      "
    networks:
      - agent_network

volumes:
  ollama_models:

networks:
  agent_network:
    driver: bridge
EOF

# 4. Create Azure Function Files
echo "📦 Creating Azure Function configuration..."

# Dockerfile
cat << 'EOF' > azure_function_app/Dockerfile
FROM mcr.microsoft.com/azure-functions/python:3.10-appservice
WORKDIR /home/site/wwwroot
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN find . -type d -name "agents" -exec touch {}/__init__.py \;
RUN find . -type d -name "utils" -exec touch {}/__init__.py \;
RUN mkdir -p local_storage/my-local-agent-share/memory \
           local_storage/my-local-agent-share/agents \
           local_storage/my-local-agent-share/demos \
           local_storage/my-local-agent-share/multi_agents \
           local_storage/my-local-agent-share/agent_config/c0p110t0-aaaa-bbbb-cccc-123456789abc/
CMD ["func", "host", "start"]
EOF

# requirements.txt
cat << 'EOF' > azure_function_app/requirements.txt
azure-functions
azure-storage-file-share
openai
requests
pandas
tensorflow
numpy
EOF

# host.json
cat << 'EOF' > azure_function_app/host.json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[3.*, 4.0.0)"
  }
}
EOF

# 5. Create Python Utilities (Modified for Local Storage)
echo "🐍 Creating Python utilities (with local storage support)..."

# utils/__init__.py
touch azure_function_app/utils/__init__.py

# utils/azure_file_storage.py (MODIFIED)
cat << 'EOF' > azure_function_app/utils/azure_file_storage.py
import json
import os
import logging
import re
from datetime import datetime, timedelta, timezone

_USE_AZURE_STORAGE = os.environ.get('USE_AZURE_STORAGE', 'true').lower() == 'true'
if _USE_AZURE_STORAGE:
    try:
        from azure.storage.file import FileService
    except ImportError:
        logging.warning("Azure Storage File SDK not found.")
        _USE_AZURE_STORAGE = False
else:
    logging.info("USE_AZURE_STORAGE is false. Using local file system.")

def safe_json_loads(json_str):
    if not json_str: return {}
    try:
        if isinstance(json_str, (dict, list)): return json_str
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

class AzureFileStorageManager:
    def __init__(self):
        self.share_name = os.environ.get('AZURE_FILES_SHARE_NAME', 'local-share')
        self.shared_memory_path = "shared_memories"
        self.default_file_name = 'memory.json'
        self.current_guid = None
        self.local_base_path = os.environ.get('LOCAL_STORAGE_BASE_PATH', '/app/local_storage')

        if _USE_AZURE_STORAGE:
            storage_connection = os.environ.get('AzureWebJobsStorage', '')
            connection_parts = dict(part.split('=', 1) for part in storage_connection.split(';'))
            self.account_name = connection_parts.get('AccountName')
            self.account_key = connection_parts.get('AccountKey')
            self.file_service = FileService(account_name=self.account_name, account_key=self.account_key)
            self._ensure_azure_share_exists()
        else:
            self._ensure_local_share_exists()
        
        self.current_memory_path = os.path.join(self.share_name, self.shared_memory_path)

    def _ensure_azure_share_exists(self):
        try:
            self.file_service.create_share(self.share_name, fail_on_exist=False)
            self._ensure_directory_exists_azure(self.shared_memory_path)
            try:
                self.file_service.get_file_properties(self.share_name, self.shared_memory_path, self.default_file_name)
            except Exception:
                self.file_service.create_file_from_text(self.share_name, self.shared_memory_path, self.default_file_name, '{}')
        except Exception as e:
            logging.error(f"Error ensuring Azure share: {str(e)}")

    def _ensure_local_share_exists(self):
        try:
            os.makedirs(os.path.join(self.local_base_path, self.share_name, self.shared_memory_path), exist_ok=True)
            local_file = os.path.join(self.local_base_path, self.share_name, self.shared_memory_path, self.default_file_name)
            if not os.path.exists(local_file):
                with open(local_file, 'w') as f: f.write('{}')
        except Exception as e:
            logging.error(f"Error ensuring local share: {str(e)}")

    def set_memory_context(self, guid=None):
        if _USE_AZURE_STORAGE: return self._set_memory_context_azure(guid)
        else: return self._set_memory_context_local(guid)

    def _set_memory_context_azure(self, guid):
        if not guid:
            self.current_guid = None
            self.current_memory_path = self.shared_memory_path
            return True
        guid_dir = f"memory/{guid}"
        try:
            self.file_service.get_file_properties(self.share_name, guid_dir, "user_memory.json")
            self.current_guid = guid
            self.current_memory_path = guid_dir
            return True
        except Exception:
            self._ensure_directory_exists_azure(guid_dir)
            self.file_service.create_file_from_text(self.share_name, guid_dir, "user_memory.json", '{}')
            self.current_guid = guid
            self.current_memory_path = guid_dir
            return True

    def _set_memory_context_local(self, guid):
        if not guid:
            self.current_guid = None
            self.current_memory_path = os.path.join(self.share_name, self.shared_memory_path)
            return True
        guid_dir = f"memory/{guid}"
        local_dir = os.path.join(self.local_base_path, self.share_name, guid_dir)
        os.makedirs(local_dir, exist_ok=True)
        local_file = os.path.join(local_dir, "user_memory.json")
        if not os.path.exists(local_file):
            with open(local_file, 'w') as f: f.write('{}')
        self.current_guid = guid
        self.current_memory_path = os.path.join(self.share_name, guid_dir)
        return True

    def read_json(self):
        if _USE_AZURE_STORAGE: return self._read_json_azure()
        else: return self._read_json_local()

    def _read_json_azure(self):
        path = self.current_memory_path if self.current_guid else self.shared_memory_path
        file = "user_memory.json" if self.current_guid else self.default_file_name
        try:
            content = self.file_service.get_file_to_text(self.share_name, path, file)
            return safe_json_loads(content.content)
        except Exception: return {}

    def _read_json_local(self):
        local_path = os.path.join(self.local_base_path, self.current_memory_path, "user_memory.json" if self.current_guid else self.default_file_name)
        try:
            with open(local_path, 'r') as f: return safe_json_loads(f.read())
        except Exception: return {}

    def write_json(self, data):
        if _USE_AZURE_STORAGE: self._write_json_azure(data)
        else: self._write_json_local(data)

    def _write_json_azure(self, data):
        path = self.current_memory_path if self.current_guid else self.shared_memory_path
        file = "user_memory.json" if self.current_guid else self.default_file_name
        self.file_service.create_file_from_text(self.share_name, path, file, json.dumps(data, indent=4))

    def _write_json_local(self, data):
        local_path = os.path.join(self.local_base_path, self.current_memory_path, "user_memory.json" if self.current_guid else self.default_file_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w') as f: f.write(json.dumps(data, indent=4))

    def ensure_directory_exists(self, directory_name):
        if _USE_AZURE_STORAGE: return self._ensure_directory_exists_azure(directory_name)
        else:
             local_dir = os.path.join(self.local_base_path, self.share_name, directory_name)
             os.makedirs(local_dir, exist_ok=True)
             return True

    def _ensure_directory_exists_azure(self, directory_name):
        if not directory_name: return False
        self.file_service.create_share(self.share_name, fail_on_exist=False)
        parts = directory_name.split('/')
        current = ""
        for part in parts:
            if part:
                current = f"{current}/{part}" if current else part
                self.file_service.create_directory(self.share_name, current, fail_on_exist=False)
        return True

    def write_file(self, directory, filename, content):
        if _USE_AZURE_STORAGE:
            self._ensure_directory_exists_azure(directory)
            self.file_service.create_file_from_text(self.share_name, directory, filename, str(content))
            return True
        else:
            path = os.path.join(self.local_base_path, self.share_name, directory, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f: f.write(str(content))
            return True

    def read_file(self, directory, filename):
        if _USE_AZURE_STORAGE:
            try: return self.file_service.get_file_to_text(self.share_name, directory, filename).content
            except: return None
        else:
            path = os.path.join(self.local_base_path, self.share_name, directory, filename)
            try:
                with open(path, 'r') as f: return f.read()
            except: return None
    
    def list_files(self, directory_name):
        # Simplified list_files for local
        if not _USE_AZURE_STORAGE:
            local_dir = os.path.join(self.local_base_path, self.share_name, directory_name)
            files = []
            if os.path.exists(local_dir):
                for item in os.listdir(local_dir):
                    if os.path.isfile(os.path.join(local_dir, item)):
                         # Mock object to match Azure SDK structure
                        files.append(type('obj', (object,), {'name': item})())
            return files
        else:
             return list(self.file_service.list_directories_and_files(self.share_name, directory_name))
EOF

# utils/agent_manager.py
cat << 'EOF' > azure_function_app/utils/agent_manager.py
import logging
import os
import sys
import importlib.util
from threading import Lock
from typing import Dict, Optional, List, Any

class AgentManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self._agents = {}
        self._initialized = True

    def register_agent(self, name, agent_instance):
        self._agents[name] = agent_instance

    def get_agent(self, name):
        return self._agents.get(name)

    def discover_agents(self, agents_directory="agents"):
        # Basic auto-discovery implementation
        pass
EOF

# 6. Create Agents
echo "🤖 Creating Agent classes..."
touch azure_function_app/agents/__init__.py

# agents/basic_agent.py
cat << 'EOF' > azure_function_app/agents/basic_agent.py
class BasicAgent:
    def __init__(self, name, metadata):
        self.name = name
        self.metadata = metadata

    def perform(self, **kwargs):
        pass
EOF

# agents/context_memory_agent.py
cat << 'EOF' > azure_function_app/agents/context_memory_agent.py
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager

class ContextMemoryAgent(BasicAgent):
    def __init__(self):
        self.name = 'ContextMemory'
        self.metadata = {
            "name": self.name,
            "description": "Recalls memories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_guid": {"type": "string"},
                    "full_recall": {"type": "boolean"}
                }
            }
        }
        self.storage_manager = AzureFileStorageManager()
        super().__init__(name=self.name, metadata=self.metadata)
        
    def perform(self, **kwargs):
        user_guid = kwargs.get('user_guid')
        self.storage_manager.set_memory_context(user_guid)
        return self._recall_context(kwargs.get('full_recall', False))

    def _recall_context(self, full_recall):
        data = self.storage_manager.read_json()
        if not data: return "No memories found."
        
        memories = []
        for k, v in data.items():
            if isinstance(v, dict) and 'message' in v:
                memories.append(f"• {v['message']} (Theme: {v.get('theme','Unknown')})")
        
        if not memories: return "No memories found."
        return "\n".join(memories)
EOF

# agents/manage_memory_agent.py
cat << 'EOF' > azure_function_app/agents/manage_memory_agent.py
import uuid
from datetime import datetime
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager

class ManageMemoryAgent(BasicAgent):
    def __init__(self):
        self.name = 'ManageMemory'
        self.metadata = {
            "name": self.name,
            "description": "Saves information to memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "memory_type": {"type": "string", "enum": ["fact", "preference", "insight", "task"]},
                    "content": {"type": "string"},
                    "user_guid": {"type": "string"}
                },
                "required": ["memory_type", "content"]
            }
        }
        self.storage_manager = AzureFileStorageManager()
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        content = kwargs.get('content')
        user_guid = kwargs.get('user_guid')
        if not content: return "Error: No content."
        
        self.storage_manager.set_memory_context(user_guid)
        memory_data = self.storage_manager.read_json() or {}
        
        memory_id = str(uuid.uuid4())
        memory_data[memory_id] = {
            "message": content,
            "theme": kwargs.get('memory_type', 'fact'),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.storage_manager.write_json(memory_data)
        return f"Stored memory: {content}"
EOF

# agents/scripted_demo_agent.py
cat << 'EOF' > azure_function_app/agents/scripted_demo_agent.py
import json
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager

class ScriptedDemoAgent(BasicAgent):
    def __init__(self):
        self.name = 'ScriptedDemo'
        self.metadata = {
            "name": self.name,
            "description": "Executes scripted demonstrations.",
            "parameters": {"type": "object", "properties": {"action": {"type": "string"}}}
        }
        self.storage_manager = AzureFileStorageManager()
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        action = kwargs.get('action')
        if action == 'respond':
            return "Demo response placeholder."
        return "Unknown action."
EOF

# agents/agent_uploader_agent.py
cat << 'EOF' > azure_function_app/agents/agent_uploader_agent.py
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager

class AgentUploaderAgent(BasicAgent):
    def __init__(self):
        self.name = "AgentUploader"
        self.metadata = {
            "name": self.name,
            "description": "Uploads custom agents.",
            "parameters": {"type": "object", "properties": {"action": {"type": "string"}}}
        }
        super().__init__(name=self.name, metadata=self.metadata)
        self.storage_manager = AzureFileStorageManager()

    def perform(self, **kwargs):
        return "Agent uploader placeholder."
EOF

# agents/github_agent_library_manager.py
cat << 'EOF' > azure_function_app/agents/github_agent_library_manager.py
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager

class GitHubAgentLibraryManager(BasicAgent):
    def __init__(self):
        self.name = 'GitHubAgentLibrary'
        self.metadata = {
            "name": self.name,
            "description": "Manages GitHub agents.",
            "parameters": {"type": "object", "properties": {"action": {"type": "string"}}}
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        return "GitHub Library placeholder."
EOF

# 7. Create Main Application Logic (Modified for Ollama)
echo "🧠 Creating function_app.py (with Ollama support)..."

# function_app.py (MODIFIED)
cat << 'EOF' > azure_function_app/function_app.py
import azure.functions as func
import logging
import json
import os
import importlib
import inspect
import sys
import re
from agents.basic_agent import BasicAgent
import uuid
from openai import AzureOpenAI, OpenAI
from datetime import datetime
import time
from utils.azure_file_storage import AzureFileStorageManager

DEFAULT_USER_GUID = "c0p110t0-aaaa-bbbb-cccc-123456789abc"

def safe_json_loads(json_str):
    if not json_str: return {}
    try: return json.loads(json_str)
    except: return {}

def load_agents_from_folder(user_guid=None):
    declared_agents = {}
    
    # Load built-in agents
    agents_dir = os.path.join(os.path.dirname(__file__), "agents")
    for file in os.listdir(agents_dir):
        if file.endswith(".py") and file not in ["__init__.py", "basic_agent.py"]:
            try:
                module_name = file[:-3]
                module = importlib.import_module(f'agents.{module_name}')
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BasicAgent) and obj is not BasicAgent:
                        instance = obj()
                        declared_agents[instance.name] = instance
            except Exception as e:
                logging.error(f"Error loading {file}: {e}")

    # Load local storage agents (simplified)
    storage = AzureFileStorageManager()
    agent_files = storage.list_files('agents')
    # Logic to load dynamic agents would go here
    
    return declared_agents

class Assistant:
    def __init__(self, declared_agents):
        self.config = {'assistant_name': 'LocalInsightBot'}
        
        if os.environ.get('USE_OLLAMA', 'false').lower() == 'true':
            logging.info("Initializing OpenAI client for Ollama.")
            self.client = OpenAI(
                base_url=os.environ.get('OLLAMA_API_BASE_URL', 'http://ollama:11434/v1'),
                api_key='ollama'
            )
            self.ollama_model_name = os.environ.get('OLLAMA_MODEL_NAME', 'llama2')
        else:
            self.client = AzureOpenAI(
                api_key=os.environ['AZURE_OPENAI_API_KEY'],
                api_version=os.environ['AZURE_OPENAI_API_VERSION'],
                azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
            )

        self.known_agents = declared_agents
        self.user_guid = DEFAULT_USER_GUID
        self.storage_manager = AzureFileStorageManager()
        self._initialize_context_memory(DEFAULT_USER_GUID)

    def _initialize_context_memory(self, user_guid):
        self.shared_memory = "Shared memory loaded."
        self.user_memory = "User memory loaded."
        if 'ContextMemory' in self.known_agents:
            self.storage_manager.set_memory_context(user_guid)
            # Simple init
            pass

    def get_agent_metadata(self):
        return [agent.metadata for agent in self.known_agents.values() if hasattr(agent, 'metadata')]

    def get_openai_api_call(self, messages):
        if os.environ.get('USE_OLLAMA', 'false').lower() == 'true':
            return self.client.chat.completions.create(
                model=self.ollama_model_name,
                messages=messages,
                functions=self.get_agent_metadata(),
                function_call="auto"
            )
        else:
            return self.client.chat.completions.create(
                model=os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-deployment'),
                messages=messages,
                functions=self.get_agent_metadata(),
                function_call="auto"
            )

    def get_response(self, prompt, conversation_history):
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        for msg in conversation_history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                messages.append(msg)
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.get_openai_api_call(messages)
            msg = response.choices[0].message
            content = msg.content or ""
            
            if msg.function_call:
                agent_name = msg.function_call.name
                agent = self.known_agents.get(agent_name)
                if agent:
                    args = safe_json_loads(msg.function_call.arguments)
                    if agent_name in ['ManageMemory', 'ContextMemory']:
                        args['user_guid'] = self.user_guid
                    
                    result = str(agent.perform(**args))
                    messages.append({"role": "function", "name": agent_name, "content": result})
                    
                    final_response = self.get_openai_api_call(messages)
                    content = final_response.choices[0].message.content or ""
                    return content, "Function executed.", f"Executed {agent_name}: {result}"
            
            # Simple voice extraction
            parts = content.split('.')
            voice = parts[0] if parts else "Done."
            return content, voice, ""
            
        except Exception as e:
            logging.error(f"Error: {e}")
            return f"Error: {str(e)}", "I encountered an error.", ""

app = func.FunctionApp()

@app.route(route="businessinsightbot_function", auth_level=func.AuthLevel.FUNCTION)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request.')
    
    # CORS
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*"
    }
    
    if req.method == 'OPTIONS':
        return func.HttpResponse(status_code=200, headers=headers)

    try:
        req_body = req.get_json()
        user_input = str(req_body.get('user_input', ''))
        history = req_body.get('conversation_history', [])
        user_guid = req_body.get('user_guid')
        
        agents = load_agents_from_folder(user_guid)
        assistant = Assistant(agents)
        if user_guid: assistant.user_guid = user_guid
        
        response_text, voice, logs = assistant.get_response(user_input, history)
        
        return func.HttpResponse(
            json.dumps({
                "assistant_response": response_text,
                "voice_response": voice,
                "agent_logs": logs,
                "user_guid": assistant.user_guid
            }),
            mimetype="application/json",
            headers=headers
        )
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, headers=headers)
EOF

# 8. Create Frontend
echo "🎨 Creating Frontend (index.html)..."
# We'll use a simplified placeholder to keep the script size manageable, 
# but pointing to the correct localhost API endpoint.
cat << 'EOF' > azure_function_app/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Agent Chat</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f0f2f5; }
        .chat-container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px; height: 60vh; overflow-y: auto; display: flex; flex-direction: column; }
        .message { padding: 10px 15px; border-radius: 15px; margin-bottom: 10px; max-width: 70%; word-wrap: break-word; }
        .user { align-self: flex-end; background: #0084ff; color: white; }
        .assistant { align-self: flex-start; background: #e4e6eb; color: black; }
        .input-area { display: flex; margin-top: 20px; gap: 10px; }
        input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid #ddd; outline: none; }
        button { padding: 10px 20px; border-radius: 20px; border: none; background: #0084ff; color: white; cursor: pointer; }
        button:disabled { background: #ccc; }
        .logs { margin-top: 20px; font-size: 0.8em; color: #666; background: #eee; padding: 10px; border-radius: 5px; display: none; }
    </style>
</head>
<body>
    <h1>Local Insight Bot (Ollama)</h1>
    <div class="chat-container" id="chat"></div>
    <div class="input-area">
        <input type="text" id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()" id="sendBtn">Send</button>
    </div>
    <button onclick="document.querySelector('.logs').style.display = 'block'" style="margin-top:10px; background:#666; font-size:0.8em">Show Logs</button>
    <div class="logs" id="logs"></div>

    <script>
        const API_URL = 'http://localhost:7071/api/businessinsightbot_function';
        const chatHistory = [];
        const userGuid = "c0p110t0-aaaa-bbbb-cccc-123456789abc";

        async function sendMessage() {
            const input = document.getElementById('input');
            const btn = document.getElementById('sendBtn');
            const text = input.value.trim();
            if (!text) return;

            addMessage('user', text);
            input.value = '';
            btn.disabled = true;

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_input: text,
                        conversation_history: chatHistory,
                        user_guid: userGuid
                    })
                });

                const data = await response.json();
                
                if (data.assistant_response) {
                    addMessage('assistant', data.assistant_response);
                    chatHistory.push({role: 'user', content: text});
                    chatHistory.push({role: 'assistant', content: data.assistant_response});
                    if (data.agent_logs) {
                        const logDiv = document.getElementById('logs');
                        logDiv.innerHTML += `<div><strong>${new Date().toLocaleTimeString()}:</strong> ${data.agent_logs}</div>`;
                    }
                } else {
                    addMessage('assistant', 'Error: ' + (data.error || 'Unknown error'));
                }
            } catch (e) {
                addMessage('assistant', 'Network Error: ' + e.message);
            } finally {
                btn.disabled = false;
            }
        }

        function addMessage(role, text) {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.textContent = text;
            const container = document.getElementById('chat');
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
EOF

echo "✅ Setup complete! Project is in '$PROJECT_ROOT'"
echo "----------------------------------------------------"
echo "🚀 To start the application:"
echo "1. cd $PROJECT_ROOT"
echo "2. docker compose up --build -d"
echo ""
echo "⏳ Note: The first run will take time as it downloads the 'llama2' model (approx 4GB)."
echo "🌐 Once started, access the UI at: http://localhost:7071"
echo "----------------------------------------------------"

chmod +x setup_agent_app.sh