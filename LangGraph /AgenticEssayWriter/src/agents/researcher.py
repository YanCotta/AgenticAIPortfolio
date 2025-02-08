from ..models.schema import AgentState, Queries
from ..services.research_service import ResearchService

RESEARCH_PLAN_PROMPT = """You are a researcher charged with providing information..."""
RESEARCH_CRITIQUE_PROMPT = """You are a researcher charged with providing information..."""

class ResearchAgent:
    def __init__(self, model, research_service: ResearchService):
        self.model = model
        self.research_service = research_service

    def research_plan_node(self, state: AgentState):
        queries = self.model.with_structured_output(Queries).invoke([
            SystemMessage(content=RESEARCH_PLAN_PROMPT),
            HumanMessage(content=state['task'])
        ])
        return self._execute_research(queries, state, "research_plan")

    def research_critique_node(self, state: AgentState):
        # Similar implementation...