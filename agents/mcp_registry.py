"""Local-only MCP discovery for RAPP Brainstem; never connects to or executes servers."""

import json
from pathlib import Path

from agents.basic_agent import BasicAgent


class MCPRegistryAgent(BasicAgent):
    def __init__(self):
        self.name = "MCPRegistry"
        self.metadata = {
            "name": self.name,
            "description": "Discover public MCP servers in the local catalog, optionally by exact tool name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "description": "Exact MCP tool name. Omit to list all servers.",
                    }
                },
                "required": [],
                "additionalProperties": False,
            },
        }
        super().__init__()

    def perform(self, tool=None, **kwargs) -> str:
        if tool is not None and not isinstance(tool, str):
            raise TypeError("tool must be a string")
        endpoint = Path(__file__).resolve().parents[1] / "data/mcp-registry/api/v1/servers.json"
        servers = json.loads(endpoint.read_text(encoding="utf-8"))["servers"]
        if tool is not None:
            servers = [
                server for server in servers
                if any(
                    item["name"] == tool
                    for item in server["_meta"]["io.modelcontextprotocol.registry/publisher-provided"]["tools"]
                )
            ]
        return json.dumps({"servers": sorted(servers, key=lambda server: server["name"])}, ensure_ascii=False)
