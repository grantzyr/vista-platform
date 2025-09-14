import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy import Text
from enum import Enum

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.provider import Provider
    from app.models.history import GameHistory
    from app.games.turnbench.models.session import GameSession

class ReasoningEffort(str, Enum):
    """reasoning effort"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class LLMBase(SQLModel):
    """LLM base model"""
    name: str = Field(max_length=100, index=True)
    display_name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # params
    frequency_penalty: Optional[float] = Field(default=None, le=2.0, ge=-2.0)
    presence_penalty: Optional[float] = Field(default=None, le=2.0, ge=-2.0)
    max_tokens: Optional[int] = Field(default=None)
    max_completion_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None)
    reasoning_effort: Optional[ReasoningEffort] = Field(default=None)

    # relations
    provider_id: uuid.UUID = Field(foreign_key="providers.id", index=True)
    
class LLMCreate(LLMBase):
    """create LLM request model"""
    pass

class LLMUpdate(SQLModel):
    """update LLM request model"""
    name: Optional[str] = Field(default=None, max_length=100)
    display_name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    frequency_penalty: Optional[float] = Field(default=None, le=2.0, ge=-2.0)
    presence_penalty: Optional[float] = Field(default=None, le=2.0, ge=-2.0)
    max_tokens: Optional[int] = Field(default=None)
    max_completion_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None)
    reasoning_effort: Optional[ReasoningEffort] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

# database model
class LLM(LLMBase, BaseModel, table=True):
    """LLM database model"""
    __tablename__ = "llms"
    
    # relations
    provider: "Provider" = Relationship(back_populates="llms")
    histories: List["GameHistory"] = Relationship(back_populates="llm")
    turnbench_sessions: List["GameSession"] = Relationship(back_populates="llm")

# response model
class LLMPublic(LLMBase):
    """LLM public info model"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class LLMListResponse(SQLModel):
    """LLM list response model"""
    data: List[LLMPublic]
    count: int
    page: int
    page_size: int

class LLMInfoResponse(SQLModel):
    """LLM info response model"""
    data: LLMPublic

class LLMDeleteResponse(SQLModel):
    """LLM delete response model"""
    data: uuid.UUID

class LLMCompleteResponse(BaseModel):
    provider_id: uuid.UUID
    provider_name: str
    llm_id: uuid.UUID
    llm_name: str
    time_used: float
    content: str
    model_level_reasoning_content: Optional[str] = None
    input_tokens: int
    output_tokens: int
