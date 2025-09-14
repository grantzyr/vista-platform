import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.games.turnbench.models.session import GameSession, GameSessionCreate, GameSessionUpdate


class SessionRepository:
    """Session repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_game_session(self, *, game_session_create: GameSessionCreate) -> GameSession:
        """Create game session"""
        db_obj = GameSession.model_validate(game_session_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_game_session_by_id(self, session_id: uuid.UUID) -> GameSession | None:
        """Get game session by id"""
        statement = (
            select(GameSession)
            .where(GameSession.id == session_id)
            .execution_options(populate_existing=True)
        )
        return self.session.exec(statement).first()
    
    def get_game_session_by_id_with_llm_info_and_setup_info(self, session_id: uuid.UUID) -> GameSession | None:
        """Get game session by id with llm info"""
        statement = (
            select(GameSession)
            .where(GameSession.id == session_id)
            .options(selectinload(GameSession.llm))
            .options(selectinload(GameSession.turnbench_setup))
        )
        return self.session.exec(statement).first()

    def update_game_session(self, session_id: uuid.UUID, game_session_update: GameSessionUpdate) -> GameSession:
        """Update game session"""
        session_data = game_session_update.model_dump(exclude_unset=True)
        db_session = self.get_game_session_by_id(session_id)
        db_session.sqlmodel_update(session_data)
        self.session.add(db_session)
        self.session.commit()
        # self.session.refresh(db_session)
        return db_session
    
    def delete_game_session_by_id(self, session_id: uuid.UUID) -> bool:
        """Delete game session by id"""
        db_session = self.get_game_session_by_id(session_id)
        if db_session:
            self.session.delete(db_session)
            self.session.commit()
            return True
        return False
    
    def list_game_sessions(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        llm_id: Optional[str] = None,
        setup_id: Optional[str] = None,
    ) -> tuple[List[GameSession], int]:
        """Get game sessions list with filters"""
        statement = select(GameSession)
        count_statement = select(func.count(GameSession.id))
        
        # Apply filters
        if llm_id:
            statement = statement.where(GameSession.llm_id == llm_id)
            count_statement = count_statement.where(GameSession.llm_id == llm_id)
        
        if setup_id:
            statement = statement.where(GameSession.setup_id == setup_id)
            count_statement = count_statement.where(GameSession.setup_id == setup_id)
        
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit).order_by(GameSession.created_at.desc())
        sessions = list(self.session.exec(statement).all())
        
        return sessions, total or 0
    
    def get_game_session_with_game_and_llm_info(self, session_id: uuid.UUID) -> GameSession | None:
        """Get game session with game info"""
        statement = (
            select(GameSession)
            .where(GameSession.id == session_id)
            .options(selectinload(GameSession.llm))
            .options(selectinload(GameSession.setup))
        )
        return self.session.exec(statement).first()