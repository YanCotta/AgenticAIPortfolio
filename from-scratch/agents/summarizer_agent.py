# agents/summarizer_agent.py
import openai
import time
import random
from .base_agent import BaseAgent
from utils.config import OPENAI_API_KEY

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummarizerAgent")

    def process(self, data):
        text = data["text"]
        retries = 3

        for attempt in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "Summarize the following document."},
                              {"role": "user", "content": text}],
                    api_key=OPENAI_API_KEY
                )
                summary = response["choices"][0]["message"]["content"]
                return {"summary": summary, "metadata": data["metadata"]}
            except Exception as e:
                if attempt < retries - 1:
                    wait_time = random.uniform(1, 3)
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Summarization failed: {str(e)}")
                    return None
