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
