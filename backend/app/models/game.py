import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, JSON, Column, Relationship
from sqlalchemy import Text

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.history import GameHistory

class GameBase(SQLModel):
    """game base model"""
    game_name: str = Field(unique=True, max_length=50, index=True)
    display_name: str = Field(max_length=100)
    description: str = Field(sa_column=Column(Text))

    # display info
    icon_url: Optional[str] = Field(default=None, max_length=255)

class GameCreate(GameBase):
    """create game request model"""
    pass

class GameUpdate(SQLModel):
    """update game request model"""
    display_name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    icon_url: Optional[str] = Field(default=None, max_length=255)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

# database model
class Game(GameBase, BaseModel, table=True):
    """game database model"""
    __tablename__ = "games"
    
    # relations
    histories: List["GameHistory"] = Relationship(back_populates="game")

# response model
class GamePublic(GameBase):
    """game public info model"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class GameListResponse(SQLModel):
    """game list response model"""
    data: List[GamePublic]
    count: int
    page: int
    page_size: int

class GameDeleteResponse(SQLModel):
    """game delete response model"""
    data: uuid.UUID