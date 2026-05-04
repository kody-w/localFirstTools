#!/usr/bin/env python3
"""
NeuAI - Standalone CLI
======================
A self-contained AI assistant CLI with persistent memory and tool capabilities.
No external dependencies beyond Python standard library and Azure OpenAI.

Usage:
    python neuai-cli.py

Environment Variables Required:
    AZURE_OPENAI_ENDPOINT - Your Azure OpenAI endpoint URL
    AZURE_OPENAI_KEY - Your Azure OpenAI API key
    AZURE_OPENAI_DEPLOYMENT - Your deployment name (e.g., gpt-4)

Optional:
    AZURE_OPENAI_API_VERSION - API version (default: 2024-02-15-preview)
"""

import os
import sys
import json
import uuid
import time
import urllib.request
import urllib.error
import ssl
import getpass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from abc import ABC, abstractmethod


# =============================================================================
# Configuration
# =============================================================================

class Config:
    """Configuration management with environment variables and local storage.

    Supports both global (~/.neuai) and local project (.neuai) directories:
    - Credentials (API keys) are always stored globally in ~/.neuai/config.json
    - Data (memories, context) uses local .neuai if found, otherwise global
    """

    def __init__(self, use_local: bool = True):
        # Check for environment variables (these take highest priority)
        self._env_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        self._env_api_key = os.environ.get("AZURE_OPENAI_KEY", "")
        self._env_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
        self._env_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "")

        # Set defaults
        self.endpoint = self._env_endpoint
        self.api_key = self._env_api_key
        self.deployment = self._env_deployment or "gpt-4"
        self.api_version = self._env_api_version or "2024-02-15-preview"

        # Global directory (always exists, stores credentials)
        self.global_dir = Path.home() / ".neuai"
        self.config_file = self.global_dir / "config.json"

        # Find local project .neuai directory
        self.local_dir = self._find_local_neuai() if use_local else None
        self.is_local = self.local_dir is not None

        # Data directory: prefer local, fall back to global
        if self.is_local:
            self.base_dir = self.local_dir
            self.data_dir = self.local_dir / "data"
            self.identity_file = self.local_dir / "identity.json"
        else:
            self.base_dir = self.global_dir
            self.data_dir = self.global_dir / "data"
            self.identity_file = self.global_dir / "identity.json"

        self.memory_file = self.data_dir / "memories.json"
        self.context_file = self.data_dir / "context.json"

        # Create directories
        self.global_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Load or create persistent user identity
        self.user_guid = self._load_or_create_identity()

        # Load saved config (env vars take priority)
        self._load_saved_config()

    def _find_local_neuai(self) -> Optional[Path]:
        """Find .neuai directory in current or parent directories."""
        current = Path.cwd()
        # Check up to 10 parent directories
        for _ in range(10):
            local_neuai = current / ".neuai"
            if local_neuai.exists() and local_neuai.is_dir():
                return local_neuai
            parent = current.parent
            if parent == current:  # Reached root
                break
            current = parent
        return None

    def _load_or_create_identity(self) -> str:
        """Load existing user GUID or create a new persistent one."""
        if self.identity_file.exists():
            try:
                with open(self.identity_file, 'r') as f:
                    data = json.load(f)
                    return data.get("user_guid", str(uuid.uuid4()))
            except Exception:
                pass
        # Create new identity
        user_guid = str(uuid.uuid4())
        with open(self.identity_file, 'w') as f:
            json.dump({"user_guid": user_guid, "created": datetime.now().isoformat()}, f, indent=2)
        return user_guid

    def _load_saved_config(self):
        """Load configuration from saved file. Env vars take priority."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                    # Only use saved values if env vars weren't set
                    if not self._env_endpoint and saved.get("endpoint"):
                        self.endpoint = saved.get("endpoint")
                    if not self._env_api_key and saved.get("api_key"):
                        self.api_key = saved.get("api_key")
                    if not self._env_deployment and saved.get("deployment"):
                        self.deployment = saved.get("deployment")
                    if not self._env_api_version and saved.get("api_version"):
                        self.api_version = saved.get("api_version")
            except Exception:
                pass

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump({
                "endpoint": self.endpoint,
                "api_key": self.api_key,
                "deployment": self.deployment,
                "api_version": self.api_version
            }, f, indent=2)
        # Set restrictive permissions on config file (contains API key)
        try:
            os.chmod(self.config_file, 0o600)
        except Exception:
            pass

    def is_configured(self) -> bool:
        """Check if Azure OpenAI is properly configured."""
        return bool(self.endpoint and self.api_key and self.deployment)

    def test_connection(self) -> Tuple[bool, str]:
        """Test the Azure OpenAI connection with current credentials."""
        if not self.is_configured():
            return False, "Missing required credentials"

        url = (
            f"{self.endpoint.rstrip('/')}/openai/deployments/"
            f"{self.deployment}/chat/completions"
            f"?api-version={self.api_version}"
        )

        # Use max_completion_tokens for newer API versions (2024-10+ and 2025+)
        if "2025" in self.api_version or self.api_version >= "2024-10":
            payload = {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_completion_tokens": 5
            }
        else:
            payload = {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            }

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            ctx = ssl.create_default_context()
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')

            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                if response.status == 200:
                    return True, "Connection successful"
                return False, f"Unexpected status: {response.status}"

        except urllib.error.HTTPError as e:
            if e.code == 401:
                return False, "Authentication failed - check your API key"
            elif e.code == 404:
                return False, f"Deployment '{self.deployment}' not found"
            elif e.code == 429:
                return True, "Connection successful (rate limited but credentials valid)"
            else:
                error_body = ""
                try:
                    error_body = e.read().decode('utf-8')
                except:
                    pass
                return False, f"API Error {e.code}: {error_body[:100]}"

        except urllib.error.URLError as e:
            return False, f"Connection failed - check endpoint URL: {e.reason}"

        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def first_run_setup(self) -> bool:
        """Complete first-run setup experience. Returns True if successful."""
        self._print_welcome()

        while True:
            print("\n" + "─" * 60)
            print("STEP 1: Azure OpenAI Endpoint")
            print("─" * 60)
            print("This is your Azure OpenAI resource URL.")
            print("Example: https://your-resource-name.openai.azure.com")
            print()

            endpoint = input("Enter Endpoint URL: ").strip()
            if not endpoint:
                print("\n⚠️  Endpoint is required.")
                continue

            # Auto-add https if missing
            if not endpoint.startswith("http"):
                endpoint = "https://" + endpoint
            self.endpoint = endpoint

            print("\n" + "─" * 60)
            print("STEP 2: API Key")
            print("─" * 60)
            print("Your Azure OpenAI API key (input will be hidden).")
            print("Find this in Azure Portal → Your OpenAI Resource → Keys")
            print()

            try:
                api_key = getpass.getpass("Enter API Key: ").strip()
            except Exception:
                # Fallback if getpass doesn't work (some terminals)
                api_key = input("Enter API Key: ").strip()

            if not api_key:
                print("\n⚠️  API Key is required.")
                continue
            self.api_key = api_key

            print("\n" + "─" * 60)
            print("STEP 3: Deployment Name")
            print("─" * 60)
            print("The name of your deployed model in Azure OpenAI Studio.")
            print("Example: gpt-4, gpt-4o, gpt-35-turbo")
            print()

            deployment = input(f"Enter Deployment Name [{self.deployment}]: ").strip()
            if deployment:
                self.deployment = deployment

            # Test the connection
            print("\n" + "─" * 60)
            print("Testing connection...")
            print("─" * 60)

            success, message = self.test_connection()

            if success:
                print(f"\n✅ {message}")
                print("\nSaving credentials locally...")
                self.save_config()
                print(f"✅ Credentials saved to: {self.config_file}")
                print("\n🔒 Your API key is stored locally and never transmitted")
                print("   except to Azure OpenAI for API calls.")

                input("\nPress Enter to continue...")
                return True
            else:
                print(f"\n❌ {message}")
                print("\nWould you like to:")
                print("  1. Try again with different credentials")
                print("  2. Save anyway and continue (not recommended)")
                print("  3. Exit")

                choice = input("\nChoice [1/2/3]: ").strip()

                if choice == "2":
                    self.save_config()
                    print(f"\n⚠️  Credentials saved despite failed test.")
                    return True
                elif choice == "3":
                    return False
                # Otherwise loop and try again

    def _print_welcome(self):
        """Print first-run welcome message."""
        welcome = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███╗   ██╗███████╗██╗   ██╗ █████╗ ██╗                   ║
║    ████╗  ██║██╔════╝██║   ██║██╔══██╗██║                   ║
║    ██╔██╗ ██║█████╗  ██║   ██║███████║██║                   ║
║    ██║╚██╗██║██╔══╝  ██║   ██║██╔══██║██║                   ║
║    ██║ ╚████║███████╗╚██████╔╝██║  ██║██║                   ║
║    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝                   ║
║                                                              ║
║                    FIRST-TIME SETUP                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Welcome to NeuAI! 🧠

NeuAI is an intelligent assistant with persistent memory that
learns about you over time. It runs entirely on your machine
with no external dependencies beyond Azure OpenAI.

To get started, you'll need:

  📌 An Azure OpenAI resource (endpoint URL)
  🔑 An API key from that resource
  🚀 A deployed model name (e.g., gpt-4, gpt-4o)

Your credentials will be stored locally at:
  ~/.neuai/config.json

Need Azure OpenAI? Visit:
  https://azure.microsoft.com/en-us/products/ai-services/openai-service
"""
        print(welcome)

    def configure_interactive(self, reconfigure: bool = False):
        """Interactive configuration setup (for reconfiguring existing setup)."""
        print("\n" + "=" * 60)
        print("NEUAI - AZURE OPENAI CONFIGURATION")
        print("=" * 60)

        print("\nEnter your Azure OpenAI credentials:")
        print("(Press Enter to keep existing value shown in brackets)\n")

        # Endpoint
        current_endpoint = self.endpoint or 'not set'
        if len(current_endpoint) > 40:
            current_endpoint = current_endpoint[:37] + "..."
        endpoint = input(f"Endpoint URL [{current_endpoint}]: ").strip()
        if endpoint:
            if not endpoint.startswith("http"):
                endpoint = "https://" + endpoint
            self.endpoint = endpoint

        # API Key (use getpass for security)
        key_display = ('*' * 8 + self.api_key[-4:]) if self.api_key else 'not set'
        print(f"API Key [{key_display}]: ", end="", flush=True)
        try:
            api_key = getpass.getpass("").strip()
        except Exception:
            api_key = input("").strip()
        if api_key:
            self.api_key = api_key

        # Deployment
        deployment = input(f"Deployment Name [{self.deployment}]: ").strip()
        if deployment:
            self.deployment = deployment

        # Test connection
        print("\nTesting connection...")
        success, message = self.test_connection()

        if success:
            print(f"✅ {message}")
            self.save_config()
            print("✅ Configuration saved!")
        else:
            print(f"⚠️  {message}")
            save_anyway = input("Save anyway? (y/n): ").strip().lower()
            if save_anyway == 'y':
                self.save_config()
                print("✅ Configuration saved (with warnings)")


# =============================================================================
# Azure OpenAI Client (No External Dependencies)
# =============================================================================

class AzureOpenAIClient:
    """Minimal Azure OpenAI client using only standard library."""

    def __init__(self, config: Config):
        self.config = config
        self.max_retries = 3
        self.retry_delay = 1

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Make a chat completion request to Azure OpenAI."""

        if not self.config.is_configured():
            raise ValueError("Azure OpenAI not configured. Run with --configure first.")

        url = (
            f"{self.config.endpoint.rstrip('/')}/openai/deployments/"
            f"{self.config.deployment}/chat/completions"
            f"?api-version={self.config.api_version}"
        )

        payload = {
            "messages": messages
        }

        # Use max_completion_tokens for newer API versions (2024-10+ and 2025+)
        # Also skip temperature for newer models that only support default (1)
        if "2025" in self.config.api_version or self.config.api_version >= "2024-10":
            payload["max_completion_tokens"] = max_tokens
            # Only include temperature if it's not the default
            if temperature != 1.0:
                # Some newer models don't support custom temperature
                # Try without it first, the API will tell us if it's supported
                pass
        else:
            payload["max_tokens"] = max_tokens
            payload["temperature"] = temperature

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.config.api_key
        }

        data = json.dumps(payload).encode('utf-8')

        # Create SSL context
        ctx = ssl.create_default_context()

        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method='POST')
                with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result

            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8') if e.fp else str(e)
                if e.code == 429:  # Rate limited
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"\n⏳ Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif e.code == 401:
                    raise ValueError("Authentication failed. Check your API key.")
                elif e.code == 404:
                    raise ValueError(f"Deployment '{self.config.deployment}' not found.")
                else:
                    raise ValueError(f"API Error {e.code}: {error_body}")

            except urllib.error.URLError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise ValueError(f"Connection error: {e.reason}")

        raise ValueError("Max retries exceeded")


# =============================================================================
# Memory System (Normalized Multi-Subject Storage)
# =============================================================================

class MemoryManager:
    """Manages persistent memory storage with multi-subject support.

    Memories are stored in a normalized structure where each memory exists once
    but can be linked to multiple subjects. This enables:
    - Sharing memories across subjects without duplication
    - Efficient deduplication when querying multiple subjects
    - Lightweight data transfer (no redundant content)

    Data Structure:
    {
        "memories": {
            "mem-id": {content, type, importance, subjects: [...], ...}
        },
        "subjects": {
            "subject-id": {name, memory_ids: [...]}
        }
    }
    """

    def __init__(self, config: Config, subject_id: Optional[str] = None):
        self.config = config
        # Primary subject (formerly user_guid) - now called subject for universality
        self.subject_id = subject_id or config.user_guid
        self.data: Dict[str, Any] = {"memories": {}, "subjects": {}}
        self._load_memories()
        self._ensure_subject_exists(self.subject_id)

    # Backward compatibility alias
    @property
    def user_guid(self) -> str:
        return self.subject_id

    def _load_memories(self):
        """Load memories from file, handling legacy format migration."""
        if self.config.memory_file.exists():
            try:
                with open(self.config.memory_file, 'r') as f:
                    raw_data = json.load(f)

                # Check if this is the new normalized format
                if "memories" in raw_data and "subjects" in raw_data:
                    self.data = raw_data
                else:
                    # Migrate from legacy format (subject_id -> [memories])
                    self.data = self._migrate_legacy_format(raw_data)
                    self._save_memories()  # Save migrated data
            except Exception:
                self.data = {"memories": {}, "subjects": {}}

    def _migrate_legacy_format(self, legacy_data: Dict) -> Dict:
        """Migrate from legacy format to normalized structure."""
        new_data = {"memories": {}, "subjects": {}}

        for subject_id, memories in legacy_data.items():
            if not isinstance(memories, list):
                continue

            memory_ids = []
            for mem in memories:
                mem_id = mem.get("id", str(uuid.uuid4()))
                # Add subject tracking to memory
                mem["subjects"] = [subject_id]
                new_data["memories"][mem_id] = mem
                memory_ids.append(mem_id)

            new_data["subjects"][subject_id] = {
                "name": subject_id,
                "memory_ids": memory_ids,
                "created": datetime.now().isoformat()
            }

        return new_data

    def _ensure_subject_exists(self, subject_id: str, name: Optional[str] = None):
        """Ensure a subject entry exists in the data structure."""
        if subject_id not in self.data["subjects"]:
            self.data["subjects"][subject_id] = {
                "name": name or subject_id,
                "memory_ids": [],
                "created": datetime.now().isoformat()
            }

    def _save_memories(self):
        """Save memories to file."""
        with open(self.config.memory_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def store_memory(
        self,
        content: str,
        memory_type: str = "fact",
        importance: int = 3,
        tags: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None
    ) -> str:
        """Store a new memory entry, optionally linking to multiple subjects.

        Args:
            content: The memory content
            memory_type: Type of memory (fact, preference, insight, task)
            importance: Importance level 1-5
            tags: Optional tags for categorization
            subjects: List of subject IDs to link (defaults to current subject)

        Returns:
            The memory ID
        """
        memory_id = str(uuid.uuid4())
        now = datetime.now()

        # Determine which subjects to link
        target_subjects = subjects or [self.subject_id]

        # Ensure all target subjects exist
        for subj in target_subjects:
            self._ensure_subject_exists(subj)

        memory_entry = {
            "id": memory_id,
            "content": content,
            "type": memory_type,
            "importance": importance,
            "tags": tags or [],
            "subjects": target_subjects,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "timestamp": now.isoformat(),
            "created": now.isoformat(),
            "updated": now.isoformat()
        }

        # Store memory in normalized structure
        self.data["memories"][memory_id] = memory_entry

        # Link memory to each subject
        for subj in target_subjects:
            if memory_id not in self.data["subjects"][subj]["memory_ids"]:
                self.data["subjects"][subj]["memory_ids"].append(memory_id)

        self._save_memories()
        return memory_id

    def link_memory_to_subject(self, memory_id: str, subject_id: str) -> bool:
        """Link an existing memory to an additional subject.

        Args:
            memory_id: The memory to link
            subject_id: The subject to link it to

        Returns:
            True if successful, False if memory doesn't exist
        """
        if memory_id not in self.data["memories"]:
            return False

        self._ensure_subject_exists(subject_id)

        # Add subject to memory's subject list
        if subject_id not in self.data["memories"][memory_id]["subjects"]:
            self.data["memories"][memory_id]["subjects"].append(subject_id)
            self.data["memories"][memory_id]["updated"] = datetime.now().isoformat()

        # Add memory to subject's memory list
        if memory_id not in self.data["subjects"][subject_id]["memory_ids"]:
            self.data["subjects"][subject_id]["memory_ids"].append(memory_id)

        self._save_memories()
        return True

    def unlink_memory_from_subject(self, memory_id: str, subject_id: str) -> bool:
        """Remove a memory's link to a subject (doesn't delete the memory).

        If the memory has no remaining subjects, it will be deleted.
        """
        if memory_id not in self.data["memories"]:
            return False

        mem = self.data["memories"][memory_id]

        # Remove subject from memory
        if subject_id in mem["subjects"]:
            mem["subjects"].remove(subject_id)
            mem["updated"] = datetime.now().isoformat()

        # Remove memory from subject
        if subject_id in self.data["subjects"]:
            subj = self.data["subjects"][subject_id]
            if memory_id in subj["memory_ids"]:
                subj["memory_ids"].remove(memory_id)

        # Delete memory if no subjects remain
        if not mem["subjects"]:
            del self.data["memories"][memory_id]

        self._save_memories()
        return True

    def recall_memories(
        self,
        keywords: Optional[List[str]] = None,
        max_results: int = 10,
        memory_type: Optional[str] = None,
        subjects: Optional[List[str]] = None
    ) -> List[Dict]:
        """Recall memories with automatic deduplication across subjects.

        Args:
            keywords: Filter by keywords in content
            max_results: Maximum number of results
            memory_type: Filter by memory type
            subjects: List of subjects to search (defaults to current subject)

        Returns:
            Deduplicated list of memories sorted by timestamp
        """
        target_subjects = subjects or [self.subject_id]

        # Collect unique memory IDs from all target subjects
        memory_ids = set()
        for subj in target_subjects:
            if subj in self.data["subjects"]:
                memory_ids.update(self.data["subjects"][subj]["memory_ids"])

        # Fetch actual memories (automatic deduplication via set)
        memories = []
        for mem_id in memory_ids:
            if mem_id in self.data["memories"]:
                memories.append(self.data["memories"][mem_id].copy())

        # Filter by type
        if memory_type:
            memories = [m for m in memories if m.get("type") == memory_type]

        # Filter by keywords
        if keywords:
            filtered = []
            for mem in memories:
                content_lower = mem.get("content", "").lower()
                if any(kw.lower() in content_lower for kw in keywords):
                    filtered.append(mem)
            memories = filtered

        # Sort by timestamp (newest first)
        memories.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return memories[:max_results]

    def get_all_memories(self, subjects: Optional[List[str]] = None) -> List[Dict]:
        """Get all memories for specified subjects with deduplication.

        Args:
            subjects: List of subjects (defaults to current subject)

        Returns:
            Deduplicated list of all memories
        """
        return self.recall_memories(subjects=subjects, max_results=9999)

    def get_memory_by_id(self, memory_id: str) -> Optional[Dict]:
        """Get a specific memory by ID."""
        return self.data["memories"].get(memory_id)

    def get_subjects(self) -> List[Dict]:
        """Get all subjects with their metadata."""
        result = []
        for subj_id, subj_data in self.data["subjects"].items():
            result.append({
                "id": subj_id,
                "name": subj_data.get("name", subj_id),
                "memory_count": len(subj_data.get("memory_ids", [])),
                "created": subj_data.get("created", "")
            })
        return result

    def clear_memories(self, subject_id: Optional[str] = None):
        """Clear all memories for a subject (or current subject).

        Memories shared with other subjects are unlinked, not deleted.
        """
        target = subject_id or self.subject_id

        if target not in self.data["subjects"]:
            return

        # Get memory IDs for this subject
        memory_ids = self.data["subjects"][target]["memory_ids"].copy()

        # Unlink each memory from this subject
        for mem_id in memory_ids:
            self.unlink_memory_from_subject(mem_id, target)

        # Clear the subject's memory list
        self.data["subjects"][target]["memory_ids"] = []
        self._save_memories()

    def format_memories_for_context(self, subjects: Optional[List[str]] = None) -> str:
        """Format memories as context for the AI.

        Args:
            subjects: List of subjects to include (defaults to current subject)
        """
        memories = self.get_all_memories(subjects=subjects)
        if not memories:
            return "No stored memories."

        lines = ["Stored memories:"]
        for mem in memories[-20:]:  # Last 20 memories
            subj_count = len(mem.get("subjects", []))
            shared_indicator = f" [shared:{subj_count}]" if subj_count > 1 else ""
            lines.append(f"- [{mem.get('type', 'note')}]{shared_indicator} {mem.get('content', '')}")

        return "\n".join(lines)

    def find_duplicate_content(self, content: str) -> Optional[str]:
        """Find if identical content already exists, return memory_id if found."""
        content_lower = content.lower().strip()
        for mem_id, mem in self.data["memories"].items():
            if mem.get("content", "").lower().strip() == content_lower:
                return mem_id
        return None

    def store_or_link_memory(
        self,
        content: str,
        memory_type: str = "fact",
        importance: int = 3,
        tags: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None
    ) -> Tuple[str, bool]:
        """Store a memory or link existing one if content matches.

        Returns:
            Tuple of (memory_id, was_new) - was_new is False if linked to existing
        """
        existing_id = self.find_duplicate_content(content)

        if existing_id:
            # Link existing memory to new subjects
            target_subjects = subjects or [self.subject_id]
            for subj in target_subjects:
                self.link_memory_to_subject(existing_id, subj)
            return existing_id, False
        else:
            # Create new memory
            new_id = self.store_memory(content, memory_type, importance, tags, subjects)
            return new_id, True


# =============================================================================
# Agent System
# =============================================================================

class BasicAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters: Dict[str, Dict] = {}

    @abstractmethod
    def perform(self, **kwargs) -> str:
        """Execute the agent's task."""
        pass

    def get_tool_definition(self) -> Dict:
        """Get OpenAI function/tool definition for this agent."""
        properties = {}
        required = []

        for param_name, param_info in self.parameters.items():
            properties[param_name] = {
                "type": param_info.get("type", "string"),
                "description": param_info.get("description", "")
            }
            if param_info.get("enum"):
                properties[param_name]["enum"] = param_info["enum"]
            if param_info.get("required", False):
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


class ContextMemoryAgent(BasicAgent):
    """Agent that recalls stored memories about the user."""

    def __init__(self, memory_manager: MemoryManager):
        super().__init__(
            name="recall_memory",
            description="Recalls and provides context based on stored memories of past interactions with the user. Use this to remember things about the user."
        )
        self.memory_manager = memory_manager
        self.parameters = {
            "keywords": {
                "type": "string",
                "description": "Optional comma-separated keywords to filter memories"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of memories to return (default 10)"
            }
        }

    def perform(self, keywords: str = "", max_results: int = 10) -> str:
        keyword_list = [k.strip() for k in keywords.split(",")] if keywords else None
        memories = self.memory_manager.recall_memories(
            keywords=keyword_list,
            max_results=max_results
        )

        if not memories:
            return "No relevant memories found."

        lines = [f"Found {len(memories)} relevant memories:"]
        for mem in memories:
            date = mem.get("date", "unknown date")
            content = mem.get("content", "")
            mem_type = mem.get("type", "note")
            lines.append(f"- [{date}] ({mem_type}) {content}")

        return "\n".join(lines)


class ManageMemoryAgent(BasicAgent):
    """Agent that stores new memories about the user."""

    def __init__(self, memory_manager: MemoryManager):
        super().__init__(
            name="store_memory",
            description="Stores important information about the user for future reference. Use this to remember facts, preferences, or insights about the user."
        )
        self.memory_manager = memory_manager
        self.parameters = {
            "content": {
                "type": "string",
                "description": "The information to remember about the user",
                "required": True
            },
            "memory_type": {
                "type": "string",
                "description": "Type of memory",
                "enum": ["fact", "preference", "insight", "task"]
            },
            "importance": {
                "type": "integer",
                "description": "Importance level from 1-5 (5 being most important)"
            }
        }

    def perform(
        self,
        content: str,
        memory_type: str = "fact",
        importance: int = 3
    ) -> str:
        memory_id = self.memory_manager.store_memory(
            content=content,
            memory_type=memory_type,
            importance=importance
        )
        return f"Memory stored successfully (ID: {memory_id[:8]}...)"


class WebSearchAgent(BasicAgent):
    """Agent that simulates web search capability."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for current information. Use when you need up-to-date information that may not be in your training data."
        )
        self.parameters = {
            "query": {
                "type": "string",
                "description": "The search query",
                "required": True
            }
        }

    def perform(self, query: str) -> str:
        # In a full implementation, this would call a search API
        return (
            f"[Web search for '{query}' - This is a simulated result. "
            f"In production, integrate with Bing Search API or similar. "
            f"For now, I'll use my training knowledge to help with your query.]"
        )


class CalculatorAgent(BasicAgent):
    """Agent that performs mathematical calculations."""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs mathematical calculations. Use for arithmetic, unit conversions, or mathematical operations."
        )
        self.parameters = {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate (e.g., '2 + 2', '15 * 7', 'sqrt(144)')",
                "required": True
            }
        }

    def perform(self, expression: str) -> str:
        try:
            # Safe math evaluation with limited builtins
            import math
            safe_dict = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e
            }
            result = eval(expression, safe_dict)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"


class DateTimeAgent(BasicAgent):
    """Agent that provides date and time information."""

    def __init__(self):
        super().__init__(
            name="datetime",
            description="Gets current date, time, or performs date calculations."
        )
        self.parameters = {
            "operation": {
                "type": "string",
                "description": "The operation to perform",
                "enum": ["current", "format", "difference"],
                "required": True
            },
            "format_string": {
                "type": "string",
                "description": "Optional format string for date output"
            }
        }

    def perform(self, operation: str = "current", format_string: str = "") -> str:
        now = datetime.now()

        if operation == "current":
            return f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"
        elif operation == "format" and format_string:
            try:
                return now.strftime(format_string)
            except Exception as e:
                return f"Format error: {e}"
        else:
            return f"Date: {now.strftime('%Y-%m-%d')}, Time: {now.strftime('%H:%M:%S')}"


# =============================================================================
# Conversation Manager
# =============================================================================

class ConversationManager:
    """Manages conversation history and context."""

    def __init__(self, config: Config):
        self.config = config
        self.messages: List[Dict[str, str]] = []
        self.max_history = 50
        self._load_context()

    def _load_context(self):
        """Load conversation context from file."""
        if self.config.context_file.exists():
            try:
                with open(self.config.context_file, 'r') as f:
                    data = json.load(f)
                    self.messages = data.get("messages", [])[-self.max_history:]
            except Exception:
                self.messages = []

    def _save_context(self):
        """Save conversation context to file."""
        with open(self.config.context_file, 'w') as f:
            json.dump({"messages": self.messages[-self.max_history:]}, f, indent=2)

    def add_message(self, role: str, content: str):
        """Add a message to the conversation."""
        self.messages.append({"role": role, "content": content})
        self._save_context()

    def add_tool_result(self, tool_call_id: str, result: str):
        """Add a tool result to the conversation."""
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result
        })

    def add_assistant_with_tools(self, content: Optional[str], tool_calls: List[Dict]):
        """Add an assistant message with tool calls."""
        msg = {"role": "assistant", "content": content or ""}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)

    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages."""
        return self.messages.copy()

    def clear(self):
        """Clear conversation history."""
        self.messages = []
        self._save_context()


# =============================================================================
# Main Assistant
# =============================================================================

class NeuAIAssistant:
    """Main NeuAI assistant class that orchestrates everything."""

    SYSTEM_PROMPT = """You are NeuAI, an advanced intelligent assistant designed to help users with a wide range of tasks.

You have access to the following capabilities through tools:
- **Memory**: You can remember facts, preferences, and insights about the user across conversations
- **Recall**: You can retrieve previously stored memories to provide personalized responses
- **Calculations**: You can perform mathematical operations
- **Date/Time**: You can provide current date/time information

Guidelines:
1. Be helpful, accurate, and concise
2. Use your memory tools to personalize interactions - remember important things about the user
3. If the user shares personal information or preferences, store them for future reference
4. When uncertain, ask clarifying questions
5. Provide structured responses when appropriate (lists, steps, etc.)
6. Be proactive in offering relevant follow-up suggestions

Your personality: Intelligent, intuitive, and genuinely helpful. You adapt to each user's communication style."""

    def __init__(self, config: Config):
        self.config = config
        self.client = AzureOpenAIClient(config)
        self.memory = MemoryManager(config)
        self.conversation = ConversationManager(config)
        self.agents: Dict[str, BasicAgent] = {}
        self._register_agents()

    def _register_agents(self):
        """Register all available agents."""
        self.agents["recall_memory"] = ContextMemoryAgent(self.memory)
        self.agents["store_memory"] = ManageMemoryAgent(self.memory)
        self.agents["calculator"] = CalculatorAgent()
        self.agents["datetime"] = DateTimeAgent()
        self.agents["web_search"] = WebSearchAgent()

    def _get_tools(self) -> List[Dict]:
        """Get tool definitions for all agents."""
        return [agent.get_tool_definition() for agent in self.agents.values()]

    def _build_messages(self, user_input: str) -> List[Dict]:
        """Build the message list for the API call."""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        # Add memory context
        memory_context = self.memory.format_memories_for_context()
        if memory_context and memory_context != "No stored memories.":
            messages.append({
                "role": "system",
                "content": f"[Context from memory system]\n{memory_context}"
            })

        # Add conversation history
        messages.extend(self.conversation.get_messages())

        # Add current user message
        messages.append({"role": "user", "content": user_input})

        return messages

    def _handle_tool_calls(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute tool calls and return results."""
        results = []

        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            tool_call_id = tool_call["id"]

            try:
                arguments = json.loads(tool_call["function"]["arguments"])
            except json.JSONDecodeError:
                arguments = {}

            if function_name in self.agents:
                agent = self.agents[function_name]
                try:
                    result = agent.perform(**arguments)
                except Exception as e:
                    result = f"Error executing {function_name}: {str(e)}"
            else:
                result = f"Unknown tool: {function_name}"

            results.append({
                "tool_call_id": tool_call_id,
                "result": result
            })

        return results

    def chat(self, user_input: str) -> str:
        """Process user input and return assistant response."""

        # Build messages
        messages = self._build_messages(user_input)

        # Add user message to conversation
        self.conversation.add_message("user", user_input)

        # Get initial response
        response = self.client.chat_completion(
            messages=messages,
            tools=self._get_tools()
        )

        choice = response["choices"][0]
        message = choice["message"]

        # Handle tool calls if present
        tool_calls = message.get("tool_calls", [])
        if tool_calls:
            # Execute tools
            tool_results = self._handle_tool_calls(tool_calls)

            # Add assistant message with tool calls
            self.conversation.add_assistant_with_tools(
                message.get("content"),
                tool_calls
            )

            # Add tool results
            for result in tool_results:
                self.conversation.add_tool_result(
                    result["tool_call_id"],
                    result["result"]
                )

            # Get final response after tool execution
            final_messages = self._build_messages("")
            # Remove the duplicate user message
            final_messages.pop()
            # Use conversation history which now includes tool results
            final_messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT}
            ] + self.conversation.get_messages()

            final_response = self.client.chat_completion(
                messages=final_messages,
                tools=self._get_tools()
            )

            assistant_content = final_response["choices"][0]["message"]["content"]
        else:
            assistant_content = message.get("content", "")

        # Save assistant response
        self.conversation.add_message("assistant", assistant_content)

        return assistant_content

    def new_conversation(self):
        """Start a new conversation."""
        self.conversation.clear()

    def show_memories(self) -> str:
        """Display all stored memories."""
        memories = self.memory.get_all_memories()
        if not memories:
            return "No memories stored yet."

        lines = [f"\n{'='*50}", "STORED MEMORIES", '='*50]
        for i, mem in enumerate(memories, 1):
            lines.append(
                f"\n{i}. [{mem.get('type', 'note')}] {mem.get('content', '')}\n"
                f"   Date: {mem.get('date', 'N/A')} | "
                f"Importance: {mem.get('importance', 'N/A')}"
            )
        return "\n".join(lines)


# =============================================================================
# CLI Interface
# =============================================================================

def print_banner():
    """Print the application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███╗   ██╗███████╗██╗   ██╗ █████╗ ██╗                   ║
║    ████╗  ██║██╔════╝██║   ██║██╔══██╗██║                   ║
║    ██╔██╗ ██║█████╗  ██║   ██║███████║██║                   ║
║    ██║╚██╗██║██╔══╝  ██║   ██║██╔══██║██║                   ║
║    ██║ ╚████║███████╗╚██████╔╝██║  ██║██║                   ║
║    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝                   ║
║                                                              ║
║         Intelligent Assistant | Persistent Memory            ║
║            Powered by Azure OpenAI | Zero Dependencies       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information."""
    help_text = """
COMMANDS:
  /help       - Show this help message
  /new        - Start a new conversation
  /memories   - Show all stored memories
  /clear      - Clear all memories
  /config     - Reconfigure Azure OpenAI settings
  /status     - Show connection status and statistics
  /export     - Export memories to JSON file
  /import     - Import memories from JSON file
  /quit       - Exit the application

FEATURES:
  • NeuAI automatically remembers important information about you
  • Conversation history persists between sessions
  • Use natural language - NeuAI understands context
  • Your data is stored locally in ~/.neuai/

EXAMPLES:
  "Remember that my favorite color is blue"
  "What do you remember about me?"
  "Calculate 15% tip on $47.50"
  "What's today's date?"
    """
    print(help_text)


def main():
    """Main CLI entry point."""

    # Check for command line arguments
    if "--help" in sys.argv or "-h" in sys.argv:
        print("NeuAI - Intelligent Assistant CLI")
        print("\nUsage: python neuai-cli.py [options]")
        print("\nOptions:")
        print("  --configure    Run configuration setup")
        print("  --test         Test current credentials")
        print("  --reset        Delete saved credentials and start fresh")
        print("  --help, -h     Show this help message")
        print("\nEnvironment Variables (optional, overrides saved config):")
        print("  AZURE_OPENAI_ENDPOINT    Your Azure OpenAI endpoint URL")
        print("  AZURE_OPENAI_KEY         Your Azure OpenAI API key")
        print("  AZURE_OPENAI_DEPLOYMENT  Your deployment name (e.g., gpt-4)")
        print("\nData Location:")
        print("  ~/.neuai/config.json     Saved credentials")
        print("  ~/.neuai/memories.json   Persistent memory")
        print("  ~/.neuai/context.json    Conversation history")
        return

    # Initialize configuration
    config = Config()

    # Handle --reset flag
    if "--reset" in sys.argv:
        if config.config_file.exists():
            confirm = input("Delete saved credentials? This cannot be undone. (yes/no): ").strip().lower()
            if confirm == "yes":
                config.config_file.unlink()
                config.endpoint = ""
                config.api_key = ""
                config.deployment = "gpt-4"
                print("✅ Credentials deleted. Run again to set up fresh credentials.")
            else:
                print("❌ Cancelled.")
        else:
            print("No saved credentials found.")
        return

    # Handle --test flag
    if "--test" in sys.argv:
        if config.is_configured():
            print("Testing Azure OpenAI connection...")
            success, message = config.test_connection()
            if success:
                print(f"✅ {message}")
                print(f"\nEndpoint: {config.endpoint}")
                print(f"Deployment: {config.deployment}")
            else:
                print(f"❌ {message}")
        else:
            print("❌ No credentials configured. Run without flags to set up.")
        return

    # Handle --configure flag (for existing users to reconfigure)
    if "--configure" in sys.argv:
        config.configure_interactive()
        return

    # Check if this is a first-time user (no saved credentials)
    if not config.is_configured():
        # First-time setup experience
        if not config.first_run_setup():
            print("\n👋 Setup cancelled. Run again when you're ready.")
            return

    # Double-check we're configured now
    if not config.is_configured():
        print("\n❌ Azure OpenAI is not configured.")
        print("Run 'python neuai-cli.py' to start the setup wizard.")
        return

    # Initialize assistant
    try:
        assistant = NeuAIAssistant(config)
    except Exception as e:
        print(f"\n❌ Failed to initialize: {e}")
        return

    # Print banner
    print_banner()
    print("Type /help for commands or just start chatting!\n")

    # Main loop
    while True:
        try:
            user_input = input("\n You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                cmd = user_input.lower()

                if cmd == "/quit" or cmd == "/exit":
                    print("\n👋 Goodbye! Your memories are saved.")
                    break

                elif cmd == "/help":
                    print_help()

                elif cmd == "/new":
                    assistant.new_conversation()
                    print("\n🔄 Started new conversation. Memory retained.")

                elif cmd == "/memories":
                    print(assistant.show_memories())

                elif cmd == "/clear":
                    confirm = input("Clear all memories? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        assistant.memory.clear_memories()
                        print("\n🗑️  Memories cleared.")
                    else:
                        print("\n❌ Cancelled.")

                elif cmd == "/config":
                    config.configure_interactive()
                    assistant = NeuAIAssistant(config)

                elif cmd == "/status":
                    print("\n" + "=" * 50)
                    print("NEUAI STATUS")
                    print("=" * 50)
                    print(f"\nEndpoint: {config.endpoint[:50]}..." if len(config.endpoint) > 50 else f"\nEndpoint: {config.endpoint}")
                    print(f"Deployment: {config.deployment}")
                    print(f"API Key: {'*' * 8}{config.api_key[-4:]}" if config.api_key else "API Key: Not set")
                    print(f"\nData Directory: {config.data_dir}")
                    print(f"Memories: {len(assistant.memory.get_all_memories())} stored")
                    print(f"Conversation: {len(assistant.conversation.messages)} messages")
                    print("\nTesting connection...")
                    success, message = config.test_connection()
                    print(f"Connection: {'✅ ' + message if success else '❌ ' + message}")

                elif cmd == "/export":
                    export_path = Path.home() / f"neuai-memories-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
                    with open(export_path, 'w') as f:
                        json.dump(assistant.memory.memories, f, indent=2)
                    print(f"\n📤 Exported to: {export_path}")

                elif cmd == "/import":
                    import_path = input("Enter file path: ").strip()
                    try:
                        with open(import_path, 'r') as f:
                            imported = json.load(f)
                        assistant.memory.memories.update(imported)
                        assistant.memory._save_memories()
                        print("\n📥 Memories imported successfully.")
                    except Exception as e:
                        print(f"\n❌ Import failed: {e}")

                else:
                    print(f"\n❓ Unknown command: {user_input}")
                    print("Type /help for available commands.")

                continue

            # Regular chat
            print("\n🧠 NeuAI: ", end="", flush=True)

            try:
                response = assistant.chat(user_input)
                print(response)
            except ValueError as e:
                print(f"\n❌ Error: {e}")
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Your memories are saved.")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
