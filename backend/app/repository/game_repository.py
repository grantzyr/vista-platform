import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.models.game import Game, GameCreate, GameUpdate


class GameRepository:
    """Game repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_game(self, *, game_create: GameCreate) -> Game:
        """Create game"""
        db_obj = Game.model_validate(game_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_game_by_id(self, game_id: uuid.UUID) -> Game | None:
        """Get game by id"""
        statement = select(Game).where(Game.id == game_id)
        return self.session.exec(statement).first()
    
    def get_game_by_name(self, game_name: str) -> Game | None:
        """Get game by name"""
        statement = select(Game).where(Game.game_name == game_name)
        return self.session.exec(statement).first()
    
    def update_game(self, *, game_id: uuid.UUID, game_update: GameUpdate) -> Game:
        """Update game"""
        game_data = game_update.model_dump(exclude_unset=True)
        db_game = self.get_game_by_id(game_id)
        db_game.sqlmodel_update(game_data)
        self.session.add(db_game)
        self.session.commit()
        self.session.refresh(db_game)
        return db_game
    
    def delete_game_by_id(self, game_id: uuid.UUID) -> bool:
        """Delete game by id"""
        db_game = self.get_game_by_id(game_id)
        if db_game:
            self.session.delete(db_game)
            self.session.commit()
            return True
        return False
    
    def list_games(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[List[Game], int]:
        """Get games list"""
        statement = select(Game)
        count_statement = select(func.count(Game.id))
        
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit)
        games = list(self.session.exec(statement).all())
        
        return games, total or 0
    
    def get_game_with_histories(self, game_id: uuid.UUID) -> Game | None:
        """Get game with histories"""
        statement = (
            select(Game)
            .where(Game.id == game_id)
            .options(selectinload(Game.histories))
        )
        return self.session.exec(statement).first()