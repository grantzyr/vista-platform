import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.models.history import GameHistory, GameHistoryCreate, GameHistoryUpdate


class GameHistoryRepository:
    """GameHistory repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_game_history(self, *, game_history_create: GameHistoryCreate) -> GameHistory:
        """Create game history"""
        db_obj = GameHistory.model_validate(game_history_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_game_history_by_id(self, history_id: uuid.UUID) -> GameHistory | None:
        """Get game history by id"""
        statement = select(GameHistory).where(GameHistory.id == history_id)
        return self.session.exec(statement).first()
    
    def get_game_histories_by_game_id(self, game_id: uuid.UUID) -> List[GameHistory]:
        """Get all game histories by game id"""
        statement = select(GameHistory).where(GameHistory.game_id == game_id)
        return list(self.session.exec(statement).all())
    
    def get_game_histories_by_llm_id(self, llm_id: uuid.UUID) -> List[GameHistory]:
        """Get all game histories by llm id"""
        statement = select(GameHistory).where(GameHistory.llm_id == llm_id)
        return list(self.session.exec(statement).all())
    
    def update_game_history(self, *, history_id: uuid.UUID, game_history_update: GameHistoryUpdate) -> GameHistory:
        """Update game history"""
        history_data = game_history_update.model_dump(exclude_unset=True)
        db_history = self.get_game_history_by_id(history_id)
        db_history.sqlmodel_update(history_data)
        self.session.add(db_history)
        self.session.commit()
        self.session.refresh(db_history)
        return db_history
    
    def delete_game_history_by_id(self, history_id: uuid.UUID) -> bool:
        """Delete game history by id"""
        db_history = self.get_game_history_by_id(history_id)
        if db_history:
            self.session.delete(db_history)
            self.session.commit()
            return True
        return False
    
    def list_game_histories(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        game_id: Optional[uuid.UUID] = None,
        llm_id: Optional[str] = None,
        result: Optional[bool] = None
    ) -> tuple[List[GameHistory], int]:
        """Get game histories list with filters"""
        statement = select(GameHistory)
        count_statement = select(func.count(GameHistory.id))
        
        # Apply filters
        if game_id:
            statement = statement.where(GameHistory.game_id == game_id)
            count_statement = count_statement.where(GameHistory.game_id == game_id)
        
        if llm_id:
            statement = statement.where(GameHistory.llm_id == llm_id)
            count_statement = count_statement.where(GameHistory.llm_id == llm_id)
        
        if result:
            statement = statement.where(GameHistory.result == result)
            count_statement = count_statement.where(GameHistory.result == result)
        
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit).order_by(GameHistory.created_at.desc())
        histories = list(self.session.exec(statement).all())
        
        return histories, total or 0
    
    def get_game_history_with_game_and_llm_info(self, history_id: uuid.UUID) -> GameHistory | None:
        """Get game history with game info"""
        statement = (
            select(GameHistory)
            .where(GameHistory.id == history_id)
            .options(selectinload(GameHistory.game))
            .options(selectinload(GameHistory.llm))
        )
        return self.session.exec(statement).first()
    
    def get_recent_histories_by_game_id(self, game_id: uuid.UUID, limit: int = 10) -> List[GameHistory]:
        """Get recent game histories by game id"""
        statement = (
            select(GameHistory)
            .where(GameHistory.game_id == game_id)
            .order_by(GameHistory.created_at.desc())
            .limit(limit)
        )
        return list(self.session.exec(statement).all())