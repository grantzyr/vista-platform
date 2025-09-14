import uuid
from typing import List, Optional, Tuple

from sqlmodel import Session, select
from fastapi import HTTPException

from app.repository.history_repository import GameHistoryRepository
from app.models.history import GameHistory, GameHistoryCreate, GameHistoryUpdate, GameHistoryPublic


class GameHistoryService:
    """GameHistory service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.history_repository = GameHistoryRepository(session)
    
    def create_game_history(self, game_history_create: GameHistoryCreate) -> GameHistory:
        """Create game history"""
        # Check if session_id already exists
        existing_history = self.history_repository.get_game_history_by_session_id(game_history_create.session_id)
        if existing_history:
            raise HTTPException(status_code=400, detail=f"Game history with session_id {game_history_create.session_id} already exists")
        
        return self.history_repository.create_game_history(game_history_create=game_history_create)
    
    def get_game_history_by_id(self, history_id: uuid.UUID) -> GameHistory:
        """Get game history by id"""
        history = self.history_repository.get_game_history_by_id(history_id)
        if not history:
            raise HTTPException(status_code=404, detail=f"Game history with id {history_id} not found")
        return history
    
    def get_game_history_with_game_and_llm_info(self, history_id: uuid.UUID) -> GameHistory:
        """Get game history with game info"""
        history = self.history_repository.get_game_history_with_game_and_llm_info(history_id)
        if not history:
            raise HTTPException(status_code=404, detail=f"Game history with id {history_id} not found")
        return history
    
    def get_game_histories_by_game_id(self, game_id: uuid.UUID) -> List[GameHistory]:
        """Get all game histories by game id"""
        return self.history_repository.get_game_histories_by_game_id(game_id)
    
    def get_game_histories_by_llm_id(self, llm_id: uuid.UUID) -> List[GameHistory]:
        """Get all game histories by llm id"""
        return self.history_repository.get_game_histories_by_llm_id(llm_id)
    
    def get_recent_histories_by_game_id(self, game_id: uuid.UUID, limit: int = 10) -> List[GameHistory]:
        """Get recent game histories by game id"""
        if limit <= 0 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        return self.history_repository.get_recent_histories_by_game_id(game_id, limit)
    
    def update_game_history(self, history_id: uuid.UUID, game_history_update: GameHistoryUpdate) -> GameHistory:
        """Update game history"""
        return self.history_repository.update_game_history(
            history_id=history_id, 
            game_history_update=game_history_update
        )
    
    def delete_game_history(self, history_id: uuid.UUID) -> bool:
        """Delete game history"""
        self.get_game_history_by_id(history_id)
        return self.history_repository.delete_game_history_by_id(history_id)
    
    def list_game_histories(
        self,
        skip: int = 0,
        limit: int = 100,
        game_id: Optional[uuid.UUID] = None,
        llm_id: Optional[str] = None,
        result: Optional[bool] = None
    ) -> tuple[List[GameHistory], int]:
        """Get game histories list with filters"""
        # Validate pagination params
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip cannot be negative")
        if limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        return self.history_repository.list_game_histories(
            skip=skip,
            limit=limit,
            game_id=game_id,
            llm_id=llm_id,
            result=result
        )
    
    def get_game_histories_public_page(
        self, 
        page: int, 
        page_size: int,
        game_id: Optional[uuid.UUID] = None,
        llm_id: Optional[str] = None,
        result: Optional[bool] = None
    ) -> Tuple[List[GameHistoryPublic], int]:
        """Get public game histories page"""
        histories, total = self.list_game_histories(
            skip=(page - 1) * page_size, 
            limit=page_size,
            game_id=game_id,
            llm_id=llm_id,
            result=result
        )
        return [GameHistoryPublic(**history.model_dump()) for history in histories], total
    
    def get_game_history_public_by_id(self, history_id: uuid.UUID) -> GameHistoryPublic:
        """Get public game history by history id"""
        history = self.get_game_history_by_id(history_id)
        return GameHistoryPublic(**history.model_dump())
    
    def get_game_history_public_by_session_id(self, session_id: str) -> GameHistoryPublic:
        """Get public game history by session id"""
        history = self.get_game_history_by_session_id(session_id)
        return GameHistoryPublic(**history.model_dump())
    
    def complete_game_session(self, session_id: str, result: bool, total_turns: int = 0) -> GameHistory:
        """Complete a game session"""
        history = self.get_game_history_by_session_id(session_id)
        
        update_data = GameHistoryUpdate(
            result=result,
            total_turns=max(total_turns, history.total_turns)
        )
        
        return self.update_game_history(history.id, update_data)
    
    def abandon_game_session(self, session_id: str, error_message: Optional[str] = None) -> GameHistory:
        """Abandon a game session"""
        history = self.get_game_history_by_session_id(session_id)
        
        update_data = GameHistoryUpdate(
            error_message=error_message
        )
        
        return self.update_game_history(history.id, update_data)
