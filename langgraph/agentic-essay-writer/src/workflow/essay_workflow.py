from ..agents.planner import PlannerAgent
from ..agents.researcher import ResearchAgent
from ..agents.writer import WriterAgent
from ..agents.critic import CriticAgent
from ..models.schema import AgentState
from ..utils.logging import get_logger
import asyncio

logger = get_logger(__name__)

class EssayWorkflow:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: WriterAgent, critic: CriticAgent):
        self.planner = planner
        self.researcher = researcher
        self.writer = writer
        self.critic = critic

    async def generate_essay(self, task: str) -> AgentState:
        """
        Orchestrates the essay generation process with improved error handling and retry mechanisms.
        """
        state = AgentState(task=task)
        max_retries = 2  # Maximum number of retries for plan and research stages

        try:
            # Plan stage with retry
            for attempt in range(max_retries + 1):
                try:
                    plan_result = await self.planner.execute(state)
                    if "plan" in plan_result and plan_result["plan"]:
                        state.plan = plan_result["plan"]
                        state.lnode = plan_result["lnode"]
                        state.count = plan_result["count"]
                        break  # Exit retry loop if successful
                    else:
                        raise ValueError("Planner returned incomplete content.")
                except Exception as e:
                    logger.exception(f"Attempt {attempt + 1} failed during plan execution: {e}")
                    if attempt == max_retries:
                        state.plan = "Failed to generate a plan after multiple retries."
                        state.lnode = "planner"
                        return state  # Exit if max retries reached
                    await asyncio.sleep(1)  # Wait before retrying

            # Research stage with retry
            for attempt in range(max_retries + 1):
                try:
                    research_result = await self.researcher.execute(state)
                    if "content" in research_result and research_result["content"]:
                        state.content = research_result["content"]
                        state.lnode = research_result["lnode"]
                        state.count = research_result["count"]
                        break  # Exit retry loop if successful
                    else:
                        raise ValueError("Researcher returned incomplete content.")
                except Exception as e:
                    logger.exception(f"Attempt {attempt + 1} failed during research execution: {e}")
                    if attempt == max_retries:
                        state.content = ["Failed to gather research after multiple retries."]
                        state.lnode = "researcher"
                        break  # Exit if max retries reached
                    await asyncio.sleep(1)  # Wait before retrying

            # Write stage
            try:
                write_result = await self.writer.execute(state)
                if "draft" in write_result and write_result["draft"]:
                    state.draft = write_result["draft"]
                    state.revision_number = write_result["revision_number"]
                    state.lnode = write_result["lnode"]
                    state.count = write_result["count"]
                else:
                    raise ValueError("Writer returned incomplete content.")
            except Exception as e:
                logger.exception(f"Error during write execution: {e}")
                state.draft = "Failed to generate a draft."
                state.lnode = "generate"

            # Critique stage
            try:
                critique_result = await self.critic.execute(state)
                if "critique" in critique_result and critique_result["critique"]:
                    state.critique = critique_result["critique"]
                    state.lnode = critique_result["lnode"]
                    state.count = critique_result["count"]
                else:
                    raise ValueError("Critic returned incomplete content.")
            except Exception as e:
                logger.exception(f"Error during critic execution: {e}")
                state.critique = "Failed to generate critique."
                state.lnode = "reflect"

            return state

        except Exception as e:
            logger.exception(f"Error during essay workflow: {e}")
            state.draft = "An error occurred during essay generation. Please check the logs."
            return state
