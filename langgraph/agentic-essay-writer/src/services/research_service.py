import logging
from typing import List
from tavily import TavilyClient
from ..config import Settings
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ResearchService:
    def __init__(self, settings: Settings):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(self, query: str, max_results: int = 5):
        try:
            return self.tavily.search(query=query, max_results=max_results)
        except Exception as e:
            logger.exception(f"Error during Tavily search: {e}")
            return {"results": []}