from pydantic import BaseModel
from typing import List, Optional, Annotated
import operator

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