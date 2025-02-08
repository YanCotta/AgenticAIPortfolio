from ..agents.planner import PlannerAgent
from ..agents.researcher import ResearchAgent
from ..agents.writer import WriterAgent
from ..agents.critic import CriticAgent
from ..models.schema import AgentState

class EssayWorkflow:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: WriterAgent, critic: CriticAgent):
        self.planner = planner
        self.researcher = researcher
        self.writer = writer
        self.critic = critic

    async def generate_essay(self, task: str) -> AgentState:
        """
        Orchestrates the essay generation process.
        """
        state = AgentState(task=task)

        # Plan
        plan_result = await self.planner.execute(state)
        state.plan = plan_result["plan"]
        state.lnode = plan_result["lnode"]
        state.count = plan_result["count"]

        # Research
        research_result = await self.researcher.execute(state)
        state.content = research_result["content"]
        state.lnode = research_result["lnode"]
        state.count = research_result["count"]

        # Write
        write_result = await self.writer.execute(state)
        state.draft = write_result["draft"]
        state.revision_number = write_result["revision_number"]
        state.lnode = write_result["lnode"]
        state.count = write_result["count"]

        # Critique
        critique_result = await self.critic.execute(state)
        state.critique = critique_result["critique"]
        state.lnode = critique_result["lnode"]
        state.count = critique_result["count"]

        return state
