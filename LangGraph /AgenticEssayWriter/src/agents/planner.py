from langchain_core.messages import SystemMessage, HumanMessage
from ..models.schema import AgentState

PLAN_PROMPT = """You are an expert writer tasked with writing a high level outline of an 3-paragraph essay..."""

def plan_node(state: AgentState):
    messages = [
        SystemMessage(content=PLAN_PROMPT), 
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    return {
        "plan": response.content,
        "lnode": "plan",
        "steps": 1,
    }