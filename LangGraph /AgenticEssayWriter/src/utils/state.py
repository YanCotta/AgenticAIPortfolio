from typing import Dict, Any
from langgraph.graph import StateGraph
from ..models.schema import AgentState

class StateManager:
    def __init__(self):
        self.graph = None
        self.current_thread = None
        
    def initialize_graph(self, builder: StateGraph):
        self.graph = builder.compile()

    def get_state(self, thread_id: str) -> Dict[str, Any]:
        return self.graph.get_state({"thread_id": thread_id})