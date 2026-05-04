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
