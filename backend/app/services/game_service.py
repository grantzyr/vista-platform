import uuid
from typing import List, Optional, Tuple

from sqlmodel import Session, select
from fastapi import HTTPException

from app.repository.game_repository import GameRepository
from app.models.game import Game, GameCreate, GameUpdate, GamePublic


class GameService:
    """Game service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.game_repository = GameRepository(session)
    
    def create_game(self, game_create: GameCreate) -> Game:
        """Create game"""
        # Check if game name already exists
        existing_game = self.game_repository.get_game_by_name(game_create.game_name)
        if existing_game:
            raise HTTPException(status_code=400, detail=f"Game with name {game_create.game_name} already exists")
        
        return self.game_repository.create_game(game_create=game_create)
    
    def get_game_by_id(self, game_id: uuid.UUID) -> Game:
        """Get game by id"""
        game = self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with id {game_id} not found")
        return game
    
    def get_game_by_name(self, game_name: str) -> Optional[Game]:
        """Get game by name"""
        game = self.game_repository.get_game_by_name(game_name)
        if not game:
            return None
            # raise HTTPException(status_code=404, detail=f"Game with name {game_name} not found")
        return game
    
    def get_game_with_histories(self, game_id: uuid.UUID) -> Game:
        """Get game with histories"""
        game = self.game_repository.get_game_with_histories(game_id)
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with id {game_id} not found")
        return game
    
    def update_game(self, game_id: uuid.UUID, game_update: GameUpdate) -> Game:
        """Update game"""
        # Check if game exists
        self.get_game_by_id(game_id)
        
        return self.game_repository.update_game(
            game_id=game_id, 
            game_update=game_update
        )
    
    def delete_game(self, game_id: uuid.UUID) -> bool:
        """Delete game"""
        self.get_game_by_id(game_id)
        return self.game_repository.delete_game_by_id(game_id)
    
    def list_games(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Game], int]:
        """Get games list"""
        # Validate pagination params
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip cannot be negative")
        if limit <= 0:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        return self.game_repository.list_games(
            skip=skip,
            limit=limit
        )
    
    def get_games_public_page(self, page: int, page_size: int) -> Tuple[List[GamePublic], int]:
        """Get public games page"""
        games, total = self.list_games(skip=(page - 1) * page_size, limit=page_size)
        return [GamePublic(**game.model_dump()) for game in games], total
    
    def get_game_public_by_id(self, game_id: uuid.UUID) -> GamePublic:
        """Get public game by game id"""
        game = self.get_game_by_id(game_id)
        return GamePublic(**game.model_dump())
    
    def get_game_public_by_name(self, game_name: str) -> GamePublic:
        """Get public game by game name"""
        game = self.get_game_by_name(game_name)
        return GamePublic(**game.model_dump())
