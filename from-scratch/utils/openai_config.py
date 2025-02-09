import os

class OpenAIConfig:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "your_default_api_key")
        # You can add other configuration parameters here
        self.cost_rate = 0.00002  # example cost per token
