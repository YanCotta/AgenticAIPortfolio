from typing import List
from tavily import TavilyClient

class ResearchService:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)
    
    async def search(self, query: str, max_results: int = 2) -> List[str]:
        response = await self.client.search(query=query, max_results=max_results)
        return [r['content'] for r in response['results']]