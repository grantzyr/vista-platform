import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.models.llm import LLM, LLMCreate, LLMUpdate


class LLMRepository:
    """LLM repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_llm(self, *, llm_create: LLMCreate) -> LLM:
        """Create LLM"""
        db_obj = LLM.model_validate(llm_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_llm_by_id(self, llm_id: uuid.UUID) -> LLM | None:
        """Get LLM by id"""
        statement = select(LLM).where(LLM.id == llm_id)
        return self.session.exec(statement).first()
    
    def get_llms_by_provider_id(self, provider_id: uuid.UUID) -> List[LLM]:
        """Get all LLMs by provider id"""
        statement = select(LLM).where(LLM.provider_id == provider_id)
        return list(self.session.exec(statement).all())
    
    def update_llm(self, *, llm_id: uuid.UUID, llm_update: LLMUpdate) -> LLM:
        """Update LLM"""
        llm_data = llm_update.model_dump(exclude_unset=True)
        db_llm = self.get_llm_by_id(llm_id)
        db_llm.sqlmodel_update(llm_data)
        self.session.add(db_llm)
        self.session.commit()
        self.session.refresh(db_llm)
        return db_llm
    
    def delete_llm_by_id(self, llm_id: uuid.UUID) -> bool:
        """Delete LLM by id"""
        db_llm = self.get_llm_by_id(llm_id)
        if db_llm:
            self.session.delete(db_llm)
            self.session.commit()
            return True
        return False
    
    def list_llms(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        provider_id: Optional[uuid.UUID] = None
    ) -> tuple[List[LLM], int]:
        """Get LLMs list"""
        statement = select(LLM)
        
        if provider_id:
            statement = statement.where(LLM.provider_id == provider_id)
        
        count_statement = select(func.count(LLM.id))
        if provider_id:
            count_statement = count_statement.where(LLM.provider_id == provider_id)
        
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit)
        llms = list(self.session.exec(statement).all())
        
        return llms, total or 0
    
    def get_llm_with_provider_info(self, llm_id: uuid.UUID) -> LLM | None:
        """Get LLM with provider info"""
        statement = (
            select(LLM)
            .where(LLM.id == llm_id)
            .options(selectinload(LLM.provider))
        )
        return self.session.exec(statement).first()
