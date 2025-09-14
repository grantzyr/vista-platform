import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, JSON, Column, Relationship
from sqlalchemy import Text
from enum import Enum

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.llm import LLM

# base model
class GameHistoryBase(SQLModel):
    """game history base model"""
    game_id: uuid.UUID = Field(foreign_key="games.id", index=True)
    game_name: str = Field(max_length=100)
    llm_id: uuid.UUID = Field(foreign_key="llms.id", index=True)
    session_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    
    # session info
    result: Optional[bool] = Field(default=False)
    
class GameHistoryCreate(GameHistoryBase):
    """creater game history request model"""
    pass

class GameHistoryUpdate(SQLModel):
    """update game history request model"""
    result: Optional[bool] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

# database model
class GameHistory(GameHistoryBase, BaseModel, table=True):
    """game history database model"""
    __tablename__ = "game_histories"
    
    # relations
    game: "Game" = Relationship(back_populates="histories")
    llm: "LLM" = Relationship(back_populates="histories")

# response model
class GameHistoryPublic(GameHistoryBase):
    """game history public info model"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class GameHistoryListResponse(SQLModel):
    """game history list response model"""
    data: List[GameHistoryPublic]
    count: int
    page: int
    page_size: int

class GameHistoryDeleteResponse(SQLModel):
    """game history delete response model"""
    data: uuid.UUID