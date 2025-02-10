import os
from dotenv import load_dotenv

class OpenAIConfig:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.cost_rate = float(os.getenv('OPENAI_COST_RATE', '0.001'))  # Default cost per token
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
