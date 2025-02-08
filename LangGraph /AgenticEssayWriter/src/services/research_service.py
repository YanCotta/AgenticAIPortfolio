import logging
from typing import List
from tavily import TavilyClient
from ..config import Settings

class ResearchService:
    def __init__(self, settings: Settings):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(self, query: str, max_results: int = 5):
        return self.tavily.search(query=query, max_results=max_results)