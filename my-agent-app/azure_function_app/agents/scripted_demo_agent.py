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
