from ..models.schema import AgentState
from langchain_core.messages import SystemMessage, HumanMessage

REFLECTION_PROMPT = """You are a teacher grading an 3-paragraph essay submission..."""

class CriticAgent(BaseAgent):
    def __init__(self, settings, model):
        self.model = model
        self.REFLECTION_PROMPT = ("You are a teacher grading an 3-paragraph essay submission. "
                                  "Generate critique and recommendations for the user's submission. "
                                  "Provide detailed recommendations, including requests for length, depth, style, etc.")

    async def execute(self, state: AgentState) -> dict:
        messages = [
            SystemMessage(content=self.REFLECTION_PROMPT),
            HumanMessage(content=state['draft'])
        ]
        response = await self.model.ainvoke(messages)
        return {
            "critique": response.content,
            "lnode": "reflect",
            "count": state.count + 1,
        }

    async def reflection_node(self, state: AgentState):
        messages = [
            SystemMessage(content=self.REFLECTION_PROMPT), 
            HumanMessage(content=state['draft'])
        ]
        response = await self.model.ainvoke(messages)
        return {"critique": response.content,
               "lnode": "reflect",
                "count": state.count + 1,
        }