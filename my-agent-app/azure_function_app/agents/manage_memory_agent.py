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
