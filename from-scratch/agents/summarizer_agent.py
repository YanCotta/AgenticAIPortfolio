# agents/summarizer_agent.py
import openai
import asyncio
import time
import random
from .base_agent import BaseAgent
from utils.openai_config import OpenAIConfig

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummarizerAgent")
        self.config = OpenAIConfig()
        self.cache = {}
        self.client = openai.OpenAI(api_key=self.config.api_key)
    
    async def process(self, data):
        text = data["text"]
        # Caching mechanism
        if text in self.cache:
            return self.cache[text]

        # Define models - primary first, then fallback
        models = ["gpt-4", "gpt-3.5-turbo"]
        summary = None
        cost = None
        
        for model in models:
            retries = 3
            for attempt in range(retries):
                try:
                    response = await self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "Summarize the following document."},
                            {"role": "user", "content": text}
                        ]
                    )
                    summary = response.choices[0].message.content
                    # Token counting and cost tracking (if usage data available)
                    tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0
                    cost = tokens * self.config.cost_rate
                    # Simple summary quality validation: require more than 5 words
                    if len(summary.split()) < 5:
                        raise ValueError("Summary quality insufficient")
                    # Successful summary - break out
                    break
                except Exception as e:
                    if attempt < retries - 1:
                        wait_time = random.uniform(1, 3)
                        await asyncio.sleep(wait_time)
                    else:
                        self.logger.error(f"Model {model} summarization failed on attempt {attempt+1}: {str(e)}")
                        summary = None
            if summary:
                break

        result = {"summary": summary, "metadata": {**data.get("metadata", {}), "cost": cost}}
        # Add result to cache
        if summary:
            self.cache[text] = result
        return result
