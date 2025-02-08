from abc import ABC, abstractmethod
from ..models.schema import AgentState

class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        pass