#!/usr/bin/env python3
"""
NeuAI Agent Bridge
==================
Programmatic interface to NeuAI for Claude agents and automation.
Provides non-interactive access to all NeuAI capabilities.

Usage:
    python neuai-agent-bridge.py <command> [args]

Commands:
    chat <message>      Send a message and get response
    memories            List all stored memories
    recall <keywords>   Search memories by keywords
    remember <content>  Store a new memory
    status              Get connection status
    new                 Start new conversation
    clear               Clear all memories
    history             Get conversation history
    test                Test connection

Output:
    All commands return JSON for easy parsing by agents.

Examples:
    python neuai-agent-bridge.py chat "What is 2+2?"
    python neuai-agent-bridge.py memories
    python neuai-agent-bridge.py remember "User prefers dark mode"
    python neuai-agent-bridge.py status
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import NeuAI components
try:
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    neuai_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neuai-cli.py")

    # Also check installed location
    if not os.path.exists(neuai_path):
        neuai_path = os.path.expanduser("~/.neuai/neuai-cli.py")

    spec = spec_from_loader("neuai_cli", SourceFileLoader("neuai_cli", neuai_path))
    neuai = module_from_spec(spec)
    spec.loader.exec_module(neuai)

    Config = neuai.Config
    NeuAIAssistant = neuai.NeuAIAssistant
    MemoryManager = neuai.MemoryManager
    ConversationManager = neuai.ConversationManager

except Exception as e:
    print(json.dumps({
        "success": False,
        "error": f"Failed to load NeuAI: {str(e)}",
        "hint": "Ensure neuai-cli.py is installed at ~/.neuai/"
    }))
    sys.exit(1)


class NeuAIBridge:
    """Bridge class for programmatic NeuAI access."""

    def __init__(self):
        self.config = Config()
        self._assistant = None

    @property
    def assistant(self) -> NeuAIAssistant:
        """Lazy-load assistant."""
        if self._assistant is None:
            if not self.config.is_configured():
                raise ValueError("NeuAI not configured. Run 'neuai --configure' first.")
            self._assistant = NeuAIAssistant(self.config)
        return self._assistant

    def chat(self, message: str) -> Dict[str, Any]:
        """Send a chat message and get response."""
        try:
            response = self.assistant.chat(message)
            return {
                "success": True,
                "command": "chat",
                "input": message,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "command": "chat",
                "input": message,
                "error": str(e)
            }

    def get_memories(
        self,
        keywords: Optional[List[str]] = None,
        subjects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get memories with optional keyword filter and multi-subject support.

        Args:
            keywords: Filter by keywords in content
            subjects: List of subject IDs to query (deduplicates automatically)
        """
        try:
            if keywords:
                memories = self.assistant.memory.recall_memories(
                    keywords=keywords,
                    subjects=subjects
                )
            else:
                memories = self.assistant.memory.get_all_memories(subjects=subjects)

            formatted = []
            for mem in memories:
                formatted.append({
                    "id": mem.get("id", ""),
                    "content": mem.get("content", ""),
                    "type": mem.get("type", "fact"),
                    "importance": mem.get("importance", 3),
                    "subjects": mem.get("subjects", []),
                    "shared_count": len(mem.get("subjects", [])),
                    "date": mem.get("date", ""),
                    "time": mem.get("time", "")
                })

            return {
                "success": True,
                "command": "memories",
                "count": len(formatted),
                "keywords": keywords,
                "queried_subjects": subjects or [self.assistant.memory.subject_id],
                "deduplicated": len(subjects) > 1 if subjects else False,
                "memories": formatted
            }
        except Exception as e:
            return {
                "success": False,
                "command": "memories",
                "error": str(e)
            }

    def store_memory(
        self,
        content: str,
        memory_type: str = "fact",
        importance: int = 3,
        subjects: Optional[List[str]] = None,
        smart: bool = False
    ) -> Dict[str, Any]:
        """Store a new memory, optionally linking to multiple subjects.

        Args:
            content: The memory content
            memory_type: Type (fact, preference, insight, task)
            importance: Importance level 1-5
            subjects: List of subject IDs to link to
            smart: If True, links to existing memory if content matches
        """
        try:
            if smart:
                memory_id, was_new = self.assistant.memory.store_or_link_memory(
                    content=content,
                    memory_type=memory_type,
                    importance=importance,
                    subjects=subjects
                )
                return {
                    "success": True,
                    "command": "remember",
                    "memory_id": memory_id,
                    "content": content,
                    "type": memory_type,
                    "importance": importance,
                    "subjects": subjects or [self.assistant.memory.subject_id],
                    "was_new": was_new,
                    "action": "created" if was_new else "linked_existing"
                }
            else:
                memory_id = self.assistant.memory.store_memory(
                    content=content,
                    memory_type=memory_type,
                    importance=importance,
                    subjects=subjects
                )
                return {
                    "success": True,
                    "command": "remember",
                    "memory_id": memory_id,
                    "content": content,
                    "type": memory_type,
                    "importance": importance,
                    "subjects": subjects or [self.assistant.memory.subject_id]
                }
        except Exception as e:
            return {
                "success": False,
                "command": "remember",
                "error": str(e)
            }

    def link_memory(self, memory_id: str, subject_id: str) -> Dict[str, Any]:
        """Link an existing memory to an additional subject."""
        try:
            success = self.assistant.memory.link_memory_to_subject(memory_id, subject_id)
            if success:
                mem = self.assistant.memory.get_memory_by_id(memory_id)
                return {
                    "success": True,
                    "command": "link",
                    "memory_id": memory_id,
                    "linked_to": subject_id,
                    "all_subjects": mem.get("subjects", []) if mem else []
                }
            else:
                return {
                    "success": False,
                    "command": "link",
                    "error": f"Memory {memory_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "command": "link",
                "error": str(e)
            }

    def unlink_memory(self, memory_id: str, subject_id: str) -> Dict[str, Any]:
        """Unlink a memory from a subject (deletes if no subjects remain)."""
        try:
            success = self.assistant.memory.unlink_memory_from_subject(memory_id, subject_id)
            mem = self.assistant.memory.get_memory_by_id(memory_id)
            return {
                "success": success,
                "command": "unlink",
                "memory_id": memory_id,
                "unlinked_from": subject_id,
                "remaining_subjects": mem.get("subjects", []) if mem else [],
                "deleted": mem is None
            }
        except Exception as e:
            return {
                "success": False,
                "command": "unlink",
                "error": str(e)
            }

    def get_subjects(self) -> Dict[str, Any]:
        """Get all subjects with their memory counts."""
        try:
            subjects = self.assistant.memory.get_subjects()
            return {
                "success": True,
                "command": "subjects",
                "count": len(subjects),
                "current_subject": self.assistant.memory.subject_id,
                "subjects": subjects
            }
        except Exception as e:
            return {
                "success": False,
                "command": "subjects",
                "error": str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Get NeuAI status and connection info."""
        try:
            success, message = self.config.test_connection()

            return {
                "success": True,
                "command": "status",
                "connection": {
                    "status": "connected" if success else "failed",
                    "message": message
                },
                "config": {
                    "endpoint": self.config.endpoint[:50] + "..." if len(self.config.endpoint) > 50 else self.config.endpoint,
                    "deployment": self.config.deployment,
                    "api_version": self.config.api_version
                },
                "data": {
                    "memories_count": len(self.assistant.memory.get_all_memories()) if self._assistant else 0,
                    "conversation_messages": len(self.assistant.conversation.messages) if self._assistant else 0,
                    "data_dir": str(self.config.data_dir)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "command": "status",
                "error": str(e)
            }

    def new_conversation(self) -> Dict[str, Any]:
        """Start a new conversation."""
        try:
            self.assistant.new_conversation()
            return {
                "success": True,
                "command": "new",
                "message": "New conversation started. Memory retained."
            }
        except Exception as e:
            return {
                "success": False,
                "command": "new",
                "error": str(e)
            }

    def clear_memories(self) -> Dict[str, Any]:
        """Clear all memories."""
        try:
            count = len(self.assistant.memory.get_all_memories())
            self.assistant.memory.clear_memories()
            return {
                "success": True,
                "command": "clear",
                "cleared_count": count,
                "message": f"Cleared {count} memories."
            }
        except Exception as e:
            return {
                "success": False,
                "command": "clear",
                "error": str(e)
            }

    def get_history(self, limit: int = 20) -> Dict[str, Any]:
        """Get conversation history."""
        try:
            messages = self.assistant.conversation.get_messages()

            # Format messages
            formatted = []
            for msg in messages[-limit:]:
                formatted.append({
                    "role": msg.get("role", "unknown"),
                    "content": msg.get("content", "")[:500]  # Truncate long messages
                })

            return {
                "success": True,
                "command": "history",
                "total_messages": len(messages),
                "returned": len(formatted),
                "messages": formatted
            }
        except Exception as e:
            return {
                "success": False,
                "command": "history",
                "error": str(e)
            }

    def test_connection(self) -> Dict[str, Any]:
        """Test the Azure OpenAI connection."""
        try:
            success, message = self.config.test_connection()
            return {
                "success": success,
                "command": "test",
                "connection_status": "ok" if success else "failed",
                "message": message,
                "endpoint": self.config.endpoint,
                "deployment": self.config.deployment
            }
        except Exception as e:
            return {
                "success": False,
                "command": "test",
                "error": str(e)
            }

    def multi_turn_chat(self, messages: List[str]) -> Dict[str, Any]:
        """Send multiple messages in sequence (for multi-turn conversations)."""
        try:
            responses = []
            for msg in messages:
                response = self.assistant.chat(msg)
                responses.append({
                    "input": msg,
                    "response": response
                })

            return {
                "success": True,
                "command": "multi_chat",
                "turns": len(responses),
                "conversation": responses
            }
        except Exception as e:
            return {
                "success": False,
                "command": "multi_chat",
                "error": str(e)
            }


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print(__doc__)
        return 0

    command = sys.argv[1].lower()
    bridge = NeuAIBridge()

    try:
        if command == "chat":
            if len(sys.argv) < 3:
                result = {"success": False, "error": "Usage: chat <message>"}
            else:
                message = " ".join(sys.argv[2:])
                result = bridge.chat(message)

        elif command == "memories":
            # Parse optional --subjects flag
            subjects = None
            if "--subjects" in sys.argv:
                idx = sys.argv.index("--subjects")
                if idx + 1 < len(sys.argv):
                    subjects = sys.argv[idx + 1].split(",")
            result = bridge.get_memories(subjects=subjects)

        elif command == "recall":
            if len(sys.argv) < 3:
                result = {"success": False, "error": "Usage: recall <keywords> [--subjects S1,S2]"}
            else:
                # Parse keywords and optional --subjects
                subjects = None
                keywords = []
                i = 2
                while i < len(sys.argv):
                    if sys.argv[i] == "--subjects" and i + 1 < len(sys.argv):
                        subjects = sys.argv[i + 1].split(",")
                        i += 2
                    else:
                        keywords.append(sys.argv[i])
                        i += 1
                result = bridge.get_memories(keywords=keywords, subjects=subjects)

        elif command == "remember":
            if len(sys.argv) < 3:
                result = {"success": False, "error": "Usage: remember <content> [--type TYPE] [--importance N] [--subjects S1,S2] [--smart]"}
            else:
                content = " ".join(sys.argv[2:])
                # Parse optional flags
                memory_type = "fact"
                importance = 3
                subjects = None
                smart = "--smart" in sys.argv

                if "--type" in sys.argv:
                    idx = sys.argv.index("--type")
                    if idx + 1 < len(sys.argv):
                        memory_type = sys.argv[idx + 1]
                        content = content.replace(f"--type {memory_type}", "").strip()
                if "--importance" in sys.argv:
                    idx = sys.argv.index("--importance")
                    if idx + 1 < len(sys.argv):
                        importance = int(sys.argv[idx + 1])
                        content = content.replace(f"--importance {importance}", "").strip()
                if "--subjects" in sys.argv:
                    idx = sys.argv.index("--subjects")
                    if idx + 1 < len(sys.argv):
                        subjects = sys.argv[idx + 1].split(",")
                        content = content.replace(f"--subjects {sys.argv[idx + 1]}", "").strip()
                if smart:
                    content = content.replace("--smart", "").strip()

                result = bridge.store_memory(content, memory_type, importance, subjects, smart)

        elif command == "link":
            if len(sys.argv) < 4:
                result = {"success": False, "error": "Usage: link <memory_id> <subject_id>"}
            else:
                result = bridge.link_memory(sys.argv[2], sys.argv[3])

        elif command == "unlink":
            if len(sys.argv) < 4:
                result = {"success": False, "error": "Usage: unlink <memory_id> <subject_id>"}
            else:
                result = bridge.unlink_memory(sys.argv[2], sys.argv[3])

        elif command == "subjects":
            result = bridge.get_subjects()

        elif command == "status":
            result = bridge.get_status()

        elif command == "new":
            result = bridge.new_conversation()

        elif command == "clear":
            result = bridge.clear_memories()

        elif command == "history":
            limit = 20
            if len(sys.argv) > 2:
                try:
                    limit = int(sys.argv[2])
                except ValueError:
                    pass
            result = bridge.get_history(limit)

        elif command == "test":
            result = bridge.test_connection()

        elif command == "multi":
            # Read messages from stdin (JSON array)
            if len(sys.argv) > 2:
                messages = sys.argv[2:]
            else:
                stdin_data = sys.stdin.read().strip()
                if stdin_data:
                    messages = json.loads(stdin_data)
                else:
                    result = {"success": False, "error": "Usage: multi <msg1> <msg2> ... or pipe JSON array"}
                    print(json.dumps(result, indent=2))
                    return 1
            result = bridge.multi_turn_chat(messages)

        else:
            result = {
                "success": False,
                "error": f"Unknown command: {command}",
                "available_commands": [
                    "chat", "memories", "recall", "remember",
                    "link", "unlink", "subjects",
                    "status", "new", "clear", "history", "test", "multi"
                ],
                "multi_subject_examples": {
                    "store_to_multiple": "remember 'fact' --subjects proj1,proj2",
                    "query_across": "memories --subjects proj1,proj2",
                    "smart_store": "remember 'fact' --smart",
                    "link_existing": "link <memory_id> <subject_id>",
                    "list_subjects": "subjects"
                }
            }

        print(json.dumps(result, indent=2))
        return 0 if result.get("success", False) else 1

    except Exception as e:
        result = {
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }
        print(json.dumps(result, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
