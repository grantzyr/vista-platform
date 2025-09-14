import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, JSON, Column, Relationship

from app.models.base import BaseModel
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.verifier.models import VerifierPublic

if TYPE_CHECKING:
    from app.games.turnbench.models.session import GameSession

# base model
class GameSetupBase(SQLModel):
    """game setup base model"""
    number_of_verifiers: Optional[int] = Field(default=None)
    answer: Optional[str] = Field(default=None)
    difficulty: Optional[str] = Field(default=None)
    verifier_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    active_criteria_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    nightmare_verifier_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    nightmare_active_criteria_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))


class GameSetupCreate(GameSetupBase):
    """creater game setup request model"""
    pass

class GameSetupUpdate(SQLModel):
    """update game setup request model"""
    number_of_verifiers: Optional[int] = Field(default=None)
    answer: Optional[str] = Field(default=None)
    difficulty: Optional[str] = Field(default=None)
    verifier_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    active_criteria_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    nightmare_verifier_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    nightmare_active_criteria_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

# database model
class GameSetup(GameSetupBase, BaseModel, table=True):
    """game setup database model"""
    __tablename__ = f"{GAME_NAME}_setups"

    # relations
    turnbench_sessions: List["GameSession"] = Relationship(back_populates=f"{GAME_NAME}_setup")

# response model
class GameSetupPublic(GameSetupBase):
    """game setup public info model"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class GameSetupDetail(GameSetupPublic):
    verifier_details: List[VerifierPublic]
    
class GameSetupDetailResponse(SQLModel):
    data: GameSetupDetail
    
class GameSetupListResponse(SQLModel):
    """game setup list response model"""
    data: List[GameSetupPublic]
    count: int
    page: int
    page_size: int

class GameSetupDeleteResponse(SQLModel):
    """game setup delete response model"""
    data: uuid.UUID