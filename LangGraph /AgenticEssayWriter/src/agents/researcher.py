from ..models.schema import AgentState, Queries
from ..services.research_service import ResearchService

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information..."""
RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information..."""

from ..models.schema import AgentState, Queries
from ..services.research_service import ResearchService
from ..config import Settings

class ResearchAgent(BaseAgent):
    def __init__(self, settings: Settings, research_service: ResearchService):
        self.settings = settings
        self.research_service = research_service

    async def execute(self, state: AgentState) -> dict:
        queries = await self._generate_queries(state)
        results = await self._execute_research(queries)
        return {
            "content": results,
            "lnode": "researcher",
            "count": state.count + 1
        }