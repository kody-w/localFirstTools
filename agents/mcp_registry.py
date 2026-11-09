"""Local, read-only discovery of MCP servers by exact tool name."""

import json
from pathlib import Path

from agents.basic_agent import BasicAgent


class MCPRegistryAgent(BasicAgent):
    def __init__(self):
        self.name = "MCPRegistry"
        self.metadata = {
            "name": self.name,
            "description": (
                "Discover public MCP servers from the local catalog. Supply an exact "
                "tool name to find its providers, or omit tool to list all servers. "
                "Does not contact or execute the servers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "description": "Exact MCP tool name, such as browser_navigate.",
                    }
                },
                "required": [],
            },
        }
        super().__init__()

    def perform(self, tool=None, **kwargs) -> str:
        if tool is not None and not isinstance(tool, str):
            return json.dumps({"status": "error", "message": "tool must be a string"})
        path = Path(__file__).resolve().parent.parent / "data/mcp-registry/api/v1/servers.json"
        try:
            servers = json.loads(path.read_text(encoding="utf-8"))["servers"]
            matches = []
            for server in servers:
                meta = server["_meta"]["io.modelcontextprotocol.registry/publisher-provided"]
                tools = [entry["name"] for entry in meta["tools"]]
                if tool is None or tool in tools:
                    matches.append({
                        "name": server["name"],
                        "description": server["description"],
                        "category": meta["category"],
                        "repository": server["repository"]["url"],
                        "tools": tools,
                    })
            return json.dumps({"status": "success", "servers": matches}, sort_keys=True)
        except (OSError, ValueError, KeyError, TypeError) as error:
            return json.dumps({"status": "error", "message": f"Local registry unreadable: {error}"})
