from typing import TypedDict, Annotated, List
from pydantic import BaseModel

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

class Queries(BaseModel):
    """Search query structure."""
    queries: List[str]