import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel, Field

class ReasoningHistoryItem(BaseModel):
    turn_num: int
    reasoning: str
    
class ParseDependencyRequest(BaseModel):
    llm_id: uuid.UUID
    reasoning_history: List[ReasoningHistoryItem]

class DependencyItem(BaseModel):
    current_turn: int
    dependency_turns: List[int]
    reason: str

class ParseDependencyResponse(BaseModel):
    data: List[DependencyItem]
