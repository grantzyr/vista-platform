import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.games.turnbench.models.setup import GameSetup, GameSetupCreate, GameSetupUpdate
from app.models.game import Game


class SetupRepository:
    """game setup repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_setup(self, *, setup_create: GameSetupCreate) -> GameSetup:
        """create game setup"""
        db_obj = GameSetup.model_validate(setup_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def create_setups(self, *, setup_creates: List[GameSetupCreate]) -> List[GameSetup]:
        """create game setups"""
        db_objs = [GameSetup.model_validate(setup_create) for setup_create in setup_creates]
        self.session.add_all(db_objs)
        self.session.commit()
        return db_objs
    
    def get_setup_by_id(self, setup_id: uuid.UUID) -> GameSetup | None:
        """get game setup by id"""
        statement = select(GameSetup).where(GameSetup.id == setup_id)
        return self.session.exec(statement).first()
    
    def update_setup(self, *, setup_id: uuid.UUID, setup_update: GameSetupUpdate) -> GameSetup:
        """update game setup"""
        setup_data = setup_update.model_dump(exclude_unset=True)
        db_setup = self.get_setup_by_id(setup_id)
        db_setup.sqlmodel_update(setup_data)
        self.session.add(db_setup)
        self.session.commit()
        self.session.refresh(db_setup)
        return db_setup
    
    def delete_setup_by_id(self, setup_id: uuid.UUID) -> bool:
        """delete game setup by id"""
        db_setup = self.get_setup_by_id(setup_id)
        if db_setup:
            self.session.delete(db_setup)
            self.session.commit()
            return True
        return False
    
    def list_setups(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
    ) -> tuple[List[GameSetup], int]:
        """get setups list"""
        statement = select(GameSetup)
        
        count_statement = select(func.count(GameSetup.id))
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit)
        setups = list(self.session.exec(statement).all())
        
        return setups, total or 0