import uuid
from typing import List, Optional, Tuple

from sqlmodel import Session
from fastapi import HTTPException

from app.games.turnbench.game_setup.setup_repository import SetupRepository
from app.games.turnbench.models.setup import GameSetup, GameSetupCreate, GameSetupUpdate, GameSetupPublic


class SetupService:
    """game setup service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.setup_repository = SetupRepository(session)
    
    def create_setup(self, setup_create: GameSetupCreate) -> GameSetup:
        """create game setup"""
        return self.setup_repository.create_setup(setup_create=setup_create)
    
    def create_setups(self, setup_creates: List[GameSetupCreate]) -> List[GameSetup]:
        """create game setups"""
        return self.setup_repository.create_setups(setup_creates=setup_creates)
    
    def get_setup_by_id(self, setup_id: uuid.UUID) -> GameSetup:
        """get setup by id"""
        setup = self.setup_repository.get_setup_by_id(setup_id)
        if not setup:
            raise HTTPException(status_code=404, detail=f"Setup with id {setup_id} not found")
        return setup
    
    def update_setup(self, setup_id: uuid.UUID, setup_update: GameSetupUpdate) -> GameSetup:
        """update setup"""
        return self.setup_repository.update_setup(
            setup_id=setup_id, 
            setup_update=setup_update
        )
    
    def delete_setup(self, setup_id: uuid.UUID) -> bool:
        """delete setup"""
        self.get_setup_by_id(setup_id)
        return self.setup_repository.delete_setup_by_id(setup_id)
    
    def list_setups(
        self,
        page: int,
        page_size: int,
    ) -> tuple[List[GameSetup], int]:
        """get setups list"""
        # validate pagination params
        if page < 1:
            raise HTTPException(status_code=400, detail="Page cannot be less than 1")
        if page_size <= 0:
            raise HTTPException(status_code=400, detail="Page size must be greater than 0")
        return self.setup_repository.list_setups(
            skip=(page - 1) * page_size,
            limit=page_size
        )
    
    def get_setup_public_by_setup_id(self, setup_id: uuid.UUID) -> GameSetupPublic:
        """get public setup by setup id"""
        setup = self.get_setup_by_id(setup_id)
        return GameSetupPublic(**setup.model_dump())