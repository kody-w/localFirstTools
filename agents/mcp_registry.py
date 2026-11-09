"""Local, response-driven MCP server discovery without network access."""

import json
from pathlib import Path

from agents.basic_agent import BasicAgent


class MCPRegistryAgent(BasicAgent):
    name = "mcp_registry"
    metadata = {
        "name": name,
        "description": "Find public MCP servers in the local catalog by exact offered tool name.",
        "parameters": {
            "type": "object",
            "properties": {
                "tool": {
                    "type": "string",
                    "description": "Exact tool name; omit to list all catalog servers.",
                }
            },
            "required": [],
        },
    }

    def perform(self, tool=None, **kwargs) -> str:
        path = Path(__file__).resolve().parents[1] / "data/mcp-registry/api/v1/servers.json"
        servers = json.loads(path.read_text(encoding="utf-8"))["servers"]
        meta_key = "io.modelcontextprotocol.registry/publisher-provided"
        matches = sorted(
            server["name"]
            for server in servers
            if tool is None or any(
                offered["name"] == tool for offered in server["_meta"][meta_key]["tools"]
            )
        )
        return "\n".join(matches) if matches else "No matching servers."
