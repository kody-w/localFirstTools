"""
AgentGenerator - Meta-agent that creates new agent Python files locally.

This agent can generate new agents from structured descriptions,
validate Python syntax, and maintain a JSON registry of all agents.
"""

import json
import os
import ast
from datetime import datetime
from typing import Dict, Any, Optional

from basic_agent import BasicAgent


AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(AGENTS_DIR, "registry.json")


class AgentGenerator(BasicAgent):
    """
    Agent responsible for creating new agent Python files locally.

    This is the "meta-agent" that can spawn new agents from descriptions.
    """

    def __init__(self):
        self.name = "AgentGenerator"
        self.metadata = {
            "name": self.name,
            "description": "Generates new Python agents from structured descriptions. Use this to create new specialized agents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Class name of the new agent (PascalCase, no spaces)",
                    },
                    "description": {
                        "type": "string",
                        "description": "What the agent does and when it should be used",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Input parameters for perform() method",
                        "additionalProperties": True,
                    },
                    "implementation": {
                        "type": "string",
                        "description": "Python code inside perform() method body",
                    },
                    "imports": {
                        "type": "array",
                        "description": "Additional Python imports needed",
                        "items": {"type": "string"}
                    }
                },
                "required": ["agent_name", "description"],
            },
        }

        os.makedirs(AGENTS_DIR, exist_ok=True)
        self._ensure_registry_exists()
        super().__init__()

    # ---------------------------
    # Public API
    # ---------------------------

    def perform(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a new agent from the provided specification.

        Args:
            agent_name: Class name of the new agent
            description: What the agent does
            parameters: Optional dict of input parameters
            implementation: Optional code for perform() body
            imports: Optional list of additional imports

        Returns:
            Dict with status, agent_name, and file path
        """
        agent_name = kwargs["agent_name"]
        description = kwargs["description"]
        parameters = kwargs.get("parameters", {})
        implementation = kwargs.get("implementation", "return 'Agent executed successfully'")
        imports = kwargs.get("imports", [])

        # Sanitize agent name
        agent_name = self._sanitize_name(agent_name)

        filename = self._agent_filename(agent_name)
        file_path = os.path.join(AGENTS_DIR, filename)

        if os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"Agent '{agent_name}' already exists at {file_path}",
                "agent_name": agent_name,
            }

        # Generate source code
        source_code = self._generate_agent_source(
            agent_name, description, parameters, implementation, imports
        )

        # Validate Python syntax
        validation_result = self._validate_python(source_code)
        if not validation_result["valid"]:
            return {
                "status": "error",
                "message": f"Generated code has syntax errors: {validation_result['error']}",
                "agent_name": agent_name,
            }

        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        # Update registry
        self._update_registry(agent_name, filename, description, parameters, imports)

        return {
            "status": "success",
            "agent_name": agent_name,
            "file": file_path,
            "message": f"Successfully created agent: {agent_name}",
        }

    def list_agents(self) -> Dict[str, Any]:
        """List all registered agents."""
        return self._load_registry()

    def delete_agent(self, agent_name: str) -> Dict[str, Any]:
        """Delete an agent from the filesystem and registry."""
        agent_name = self._sanitize_name(agent_name)
        filename = self._agent_filename(agent_name)
        file_path = os.path.join(AGENTS_DIR, filename)

        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"Agent '{agent_name}' not found",
            }

        os.remove(file_path)
        self._remove_from_registry(agent_name)

        return {
            "status": "success",
            "message": f"Deleted agent: {agent_name}",
        }

    def export_registry(self) -> str:
        """Export the registry as a JSON string."""
        return json.dumps(self._load_registry(), indent=2)

    def import_registry(self, registry_json: str) -> Dict[str, Any]:
        """Import agents from a JSON registry export."""
        try:
            imported = json.loads(registry_json)
            current = self._load_registry()
            current.update(imported)
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(current, f, indent=2)
            return {
                "status": "success",
                "message": f"Imported {len(imported)} agents",
            }
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Invalid JSON: {e}",
            }

    # ---------------------------
    # Internal Helpers
    # ---------------------------

    def _generate_agent_source(
        self,
        agent_name: str,
        description: str,
        parameters: dict,
        implementation: str,
        imports: list,
    ) -> str:
        """Generate Python source code for a new agent."""

        # Build imports section
        import_lines = ["from basic_agent import BasicAgent"]
        for imp in imports:
            if not imp.startswith("from") and not imp.startswith("import"):
                imp = f"import {imp}"
            import_lines.append(imp)
        imports_str = "\n".join(import_lines)

        # Build parameters dict
        params_json = json.dumps(parameters, indent=12) if parameters else "{}"

        # Clean implementation
        implementation = self._clean_template_markers(implementation)

        return f'''"""
{agent_name} - Auto-generated agent

{description}
"""

{imports_str}


class {agent_name}(BasicAgent):
    """
    {description}
    """

    def __init__(self):
        self.name = "{agent_name}"
        self.metadata = {{
            "name": self.name,
            "description": "{self._escape(description)}",
            "parameters": {params_json}
        }}
        super().__init__()

    def perform(self, **kwargs):
{self._indent_code(implementation)}
'''

    def _validate_python(self, source_code: str) -> Dict[str, Any]:
        """Validate Python syntax."""
        try:
            ast.parse(source_code)
            return {"valid": True}
        except SyntaxError as e:
            return {"valid": False, "error": str(e)}

    def _clean_template_markers(self, content: str) -> str:
        """Remove template markers from the content."""
        cleaned = content.replace('[[[', '').replace(']]]', '')
        cleaned = cleaned.replace('```python', '').replace('```', '')
        return cleaned.strip()

    def _update_registry(
        self,
        agent_name: str,
        filename: str,
        description: str,
        parameters: dict,
        imports: list,
    ):
        """Add agent to the registry."""
        registry = self._load_registry()

        registry[agent_name] = {
            "file": filename,
            "description": description,
            "parameters": parameters,
            "imports": imports,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

    def _remove_from_registry(self, agent_name: str):
        """Remove agent from the registry."""
        registry = self._load_registry()
        if agent_name in registry:
            del registry[agent_name]
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)

    def _load_registry(self) -> dict:
        """Load the agent registry."""
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _ensure_registry_exists(self):
        """Create registry file if it doesn't exist."""
        if not os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    def _agent_filename(self, agent_name: str) -> str:
        """Convert agent name to filename."""
        # Convert PascalCase to snake_case
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', agent_name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        return f"{name}_agent.py"

    def _sanitize_name(self, name: str) -> str:
        """Sanitize agent name to valid Python identifier."""
        # Remove non-alphanumeric characters except underscores
        sanitized = ''.join(c for c in name if c.isalnum() or c == '_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'Agent' + sanitized
        # Convert to PascalCase if needed
        if '_' in sanitized:
            parts = sanitized.split('_')
            sanitized = ''.join(p.capitalize() for p in parts)
        return sanitized or 'UnnamedAgent'

    @staticmethod
    def _indent_code(code: str, spaces: int = 8) -> str:
        """Indent code block."""
        indent = " " * spaces
        lines = code.splitlines() or ["return 'Agent executed successfully'"]
        return "\n".join(indent + line for line in lines)

    @staticmethod
    def _escape(text: str) -> str:
        """Escape special characters for Python strings."""
        return text.replace('\\', '\\\\').replace('"', '\\"').replace("\n", "\\n")


# Allow running as standalone script for testing
if __name__ == "__main__":
    generator = AgentGenerator()

    # Example: Create a simple agent
    result = generator.perform(
        agent_name="HelloWorld",
        description="A simple agent that greets the user",
        parameters={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name to greet"
                }
            },
            "required": ["name"]
        },
        implementation="name = kwargs.get('name', 'World')\nreturn f'Hello, {name}!'"
    )

    print(json.dumps(result, indent=2))
