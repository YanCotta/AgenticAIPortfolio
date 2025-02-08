import logging
from typing import List
from tavily import TavilyClient
from ..config import Settings

class ResearchService:
    def __init__(self, settings: Settings):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.max_results = settings.MAX_RESEARCH_RESULTS

    async def search(self, query: str) -> List[str]:
        try:
            response = await self.client.search(query=query, max_results=self.max_results)
            return [r['content'] for r in response['results']]
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []