from ..models.schema import AgentState, Queries
from ..services.research_service import ResearchService
from langchain_core.messages import SystemMessage, HumanMessage
from ..utils.logging import get_logger

logger = get_logger(__name__)

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information..."""
RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information..."""

from ..models.schema import AgentState, Queries
from ..services.research_service import ResearchService
from ..config import Settings

class ResearchAgent(BaseAgent):
    def __init__(self, settings: Settings, research_service: ResearchService, model):
        self.settings = settings
        self.research_service = research_service
        self.model = model
        self.RESEARCH_PLAN_PROMPT = ("You are a researcher charged with providing information that can "
                                     "be used when writing the following essay. Generate a list of search "
                                     "queries that will gather "
                                     "any relevant information. Only generate 3 queries max.")
        self.RESEARCH_CRITIQUE_PROMPT = ("You are a researcher charged with providing information that can "
                                         "be used when making any requested revisions (as outlined below). "
                                         "Generate a list of search queries that will gather any relevant information. "
                                         "Only generate 2 queries max.")

    async def execute(self, state: AgentState) -> dict:
        try:
            queries = await self._generate_queries(state)
            results = await self._execute_research(queries)
            return {
                "content": results,
                "lnode": "researcher",
                "count": state.count + 1
            }
        except Exception as e:
            logger.exception(f"Error during researcher execution: {e}")
            return {
                "content": ["Error occurred. Check logs."],
                "lnode": "researcher",
                "count": state.count + 1
            }

    async def generate_queries(self, state: AgentState, critique=False) -> Queries:
        prompt = self.RESEARCH_PLAN_PROMPT if not critique else self.RESEARCH_CRITIQUE_PROMPT
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=state['task'])
        ]
        return await self.model.with_structured_output(Queries).ainvoke(messages)

    async def _generate_queries(self, state: AgentState) -> Queries:
        return await self.generate_queries(state)

    async def _execute_research(self, queries: Queries) -> list:
        content = state['content'] or []
        for q in queries.queries:
            try:
                response = self.research_service.search(query=q, max_results=2)
                for r in response['results']:
                    content.append(r['content'])
            except Exception as e:
                logger.exception(f"Error during research service call: {e}")
                content.append(f"Error occurred during research: {e}")
        return content