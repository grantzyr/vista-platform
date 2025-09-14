import uuid
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, JSON, Column, Relationship

from app.models.base import BaseModel
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.models.llm import Prompt
from app.games.turnbench.models.setup import GameSetupDetail

if TYPE_CHECKING:
    from app.models.llm import LLM
    from app.games.turnbench.models.setup import GameSetup

class PlayTurnData(SQLModel):
    turn_num: int
    round_num: int
    turn_name: str
    turn_prompt: str
    turn_reasoning: str
    turn_model_level_reasoning: Optional[str] = None
    turn_time_used: Optional[float] = None
    guess_code: Optional[str] = None
    verifier_choice: Optional[str] = None
    verifier_result: Optional[str] = None
    deduce_choice_skip: Optional[bool] = None
    deduce_choice_submit_code: Optional[str] = None
    is_game_over: bool = False
    game_over_reason: Optional[str] = None
    game_success: bool = False

class GameSessionBase(SQLModel):
    """session base model"""
    mode: str = Field(max_length=100)
    llm_id: uuid.UUID = Field(foreign_key="llms.id", index=True)
    setup_id: uuid.UUID = Field(foreign_key=f"{GAME_NAME}_setups.id", index=True)
    max_rounds: Optional[int] = Field(default=99)

    # game settings
    game_info: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    verifier_descriptions: Optional[str] = Field(default=None)

    # game stats
    total_time: Optional[float] = Field(default=0)
    total_turns: Optional[int] = Field(default=0)
    total_rounds: Optional[int] = Field(default=0)
    total_verifiers: Optional[int] = Field(default=0)
    total_input_tokens: Optional[int] = Field(default=0)
    total_output_tokens: Optional[int] = Field(default=0)
    longest_context_length: Optional[int] = Field(default=0)
    total_response_with_formatting_error: Optional[int] = Field(default=0)
    total_response_with_not_valid_error: Optional[int] = Field(default=0)
    submitted_code: Optional[str] = Field(default=None)
    num_of_verifier_passed: Optional[int] = Field(default=0)

    # game status
    game_over: bool = Field(default=False)
    game_over_reason: Optional[str] = Field(default=None)
    game_success: bool = Field(default=False)

    # prompts
    base_game_prompts: Optional[Dict[str, str]] = Field(default=None, sa_column=Column(JSON))

    # game stats
    turn_messages: Optional[List[Dict[str, Any]]] = Field(default=[], sa_column=Column(JSON))
    turn_time_used: Optional[float] = Field(default=0)
    turn_input_tokens: Optional[int] = Field(default=0)
    turn_output_tokens: Optional[int] = Field(default=0)
    turn_longest_context_length: Optional[int] = Field(default=0)

    # game data
    next_turn_name: Optional[str] = Field(default="proposal")
    messages: Optional[List[Dict[str, Any]]] = Field(default=[], sa_column=Column(JSON))
    turn_result_history: Optional[List[Dict[str, Any]]] = Field(default=[], sa_column=Column(JSON))
    turn_message_indexes: Optional[List[int]] = Field(default=[], sa_column=Column(JSON))
    turn_llm_response_indexes: Optional[List[int]] = Field(default=[], sa_column=Column(JSON))

class GameSessionCreate(GameSessionBase):
    """create session request model"""
    pass

class GameSessionUpdate(GameSessionBase):
    """update session request model"""
    mode: Optional[str] = Field(default=None, max_length=100)
    llm_id: Optional[uuid.UUID] = Field(default=None)
    setup_id: Optional[uuid.UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

class GameSession(GameSessionBase, BaseModel, table=True):
    """game session database model"""
    __tablename__ = f"{GAME_NAME}_sessions"

    # relations
    llm: "LLM" = Relationship(back_populates=f"{GAME_NAME}_sessions")
    turnbench_setup: "GameSetup" = Relationship(back_populates=f"{GAME_NAME}_sessions")
    
class GameSessionPublic(GameSessionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class GetSessionsResponse(SQLModel):
    data: List[GameSessionPublic]
    count: int
    page: int
    page_size: int

class GetSessionResponse(SQLModel):
    data: GameSessionPublic

class GetSessionTurnHistoryResponse(SQLModel):
    data: List[PlayTurnData]
    
class CreateSessionRequest(SQLModel):
    mode: str
    llm_id: uuid.UUID
    setup_id: uuid.UUID
    max_rounds: int

class CreateSessionResponse(SQLModel):
    data: GameSessionPublic

class UpdateSessionRequest(SQLModel):
    new_turn_data: Optional[PlayTurnData] = None

class UpdateSessionResponse(SQLModel):
    data: uuid.UUID

class CopySessionRequest(SQLModel):
    new_llm_id: Optional[uuid.UUID] = None
    new_turn_data: Optional[PlayTurnData] = None

class CopySessionResponse(SQLModel):
    data: uuid.UUID # session id

class PlayTurnRequest(SQLModel):
    turn_num: Optional[int] = None
    reasoning_effort: Optional[str] = None # None, low, medium, high

class PlayTurnResponse(SQLModel):
    data: PlayTurnData

class SaveSessionRequest(SQLModel):
    save_to_db: bool

class SaveSessionResponse(SQLModel):
    data: uuid.UUID # session id

class ReloadSessionResponse(SQLModel):
    data: GameSessionPublic