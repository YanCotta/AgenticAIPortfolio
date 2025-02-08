from ..models.schema import AgentState

REFLECTION_PROMPT = """You are a teacher grading an 3-paragraph essay submission..."""

def reflection_node(state: AgentState):
    messages = [
        SystemMessage(content=REFLECTION_PROMPT),
        HumanMessage(content=state['draft'])
    ]
    response = model.invoke(messages)
    return {
        "critique": response.content,
        "lnode": "reflect",
        "steps": 1
    }