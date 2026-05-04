"""
TextAnalyzer - Auto-generated agent

Analyzes text and returns word count, character count, and reading time
"""

from basic_agent import BasicAgent


class TextAnalyzer(BasicAgent):
    """
    Analyzes text and returns word count, character count, and reading time
    """

    def __init__(self):
        self.name = "TextAnalyzer"
        self.metadata = {
            "name": self.name,
            "description": "Analyzes text and returns word count, character count, and reading time",
            "parameters": {
            "type": "object",
            "properties": {
                        "text": {
                                    "type": "string",
                                    "description": "The text to analyze"
                        }
            },
            "required": [
                        "text"
            ]
}
        }
        super().__init__()

    def perform(self, **kwargs):
        text = kwargs.get('text', '')
        words = len(text.split())
        chars = len(text)
        reading_time = max(1, words // 200)
        return {
            'words': words,
            'characters': chars,
            'reading_time_minutes': reading_time
        }
