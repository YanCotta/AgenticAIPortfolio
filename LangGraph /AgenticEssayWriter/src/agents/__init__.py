from abc import ABC, abstractmethod
from ..models.schema import AgentState
from ..utils.logging import get_logger

logger = get_logger(__name__)

class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, state: AgentState) -> AgentState:
        pass