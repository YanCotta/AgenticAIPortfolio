from typing import Dict
from ..models.schema import AgentState

class StateManager:
    def __init__(self):
        self._states: Dict[str, AgentState] = {}
        
    async def get_state(self, thread_id: str) -> AgentState:
        return self._states.get(thread_id, AgentState())
        
    async def update_state(self, thread_id: str, updates: dict):
        current = await self.get_state(thread_id)
        self._states[thread_id] = AgentState(**{
            **current.dict(),
            **updates
        })