from pydantic import BaseModel
from typing import List, Optional, Annotated
import operator

class AgentState(TypedDict):
    """Core state management."""
    task: str
    lnode: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    queries: List[str]
    revision_number: int
    max_revisions: int
    steps: Annotated[int, operator.add]

class AgentState(BaseModel):
    task: str
    plan: Optional[str] = None
    draft: Optional[str] = None
    critique: Optional[str] = None
    content: List[str] = []
    revision_number: int = 1
    max_revisions: int = 3
    lnode: str = ""
    count: Annotated[int, operator.add] = 0