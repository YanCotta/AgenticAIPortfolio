from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..models.schema import AgentState
from ..config import Settings

PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline..."""

class PlannerAgent(BaseAgent):
    def __init__(self, settings: Settings):
        self.model = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0
        )

    async def execute(self, state: AgentState) -> dict:
        messages = [
            SystemMessage(content=PLAN_PROMPT),
            HumanMessage(content=state.task)
        ]
        response = await self.model.ainvoke(messages)
        return {
            "plan": response.content,
            "lnode": "planner",
            "count": state.count + 1
        }