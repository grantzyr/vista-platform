import uuid
from typing import List, Optional, Tuple

from sqlmodel import Session, select
from fastapi import HTTPException

from app.repository.llm_repository import LLMRepository
from app.models.llm import LLM, LLMCreate, LLMUpdate, LLMPublic
from app.models.provider import Provider


class LLMService:
    """LLM service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.llm_repository = LLMRepository(session)
    
    def create_llm(self, llm_create: LLMCreate) -> LLM:
        """Create LLM"""
        return self.llm_repository.create_llm(llm_create=llm_create)
    
    def get_llm_by_id(self, llm_id: uuid.UUID) -> LLM:
        """Get LLM by id"""
        llm = self.llm_repository.get_llm_by_id(llm_id)
        if not llm:
            raise HTTPException(status_code=404, detail=f"LLM with id {llm_id} not found")
        return llm
    
    def get_llm_with_provider_info(self, llm_id: uuid.UUID) -> LLM:
        """Get LLM with provider info"""
        llm = self.llm_repository.get_llm_with_provider_info(llm_id)
        if not llm:
            raise HTTPException(status_code=404, detail=f"LLM with id {llm_id} not found")
        return llm
    
    def get_llms_by_provider_id(self, provider_id: uuid.UUID) -> List[LLM]:
        """Get all LLMs by provider id"""
        return self.llm_repository.get_llms_by_provider_id(provider_id)
    
    def update_llm(self, llm_id: uuid.UUID, llm_update: LLMUpdate) -> LLM:
        """Update LLM"""
        return self.llm_repository.update_llm(
            llm_id=llm_id, 
            llm_update=llm_update
        )
    
    def delete_llm(self, llm_id: uuid.UUID) -> bool:
        """Delete LLM"""
        self.get_llm_by_id(llm_id)
        return self.llm_repository.delete_llm_by_id(llm_id)
    
    def list_llms(
        self,
        skip: int = 0,
        limit: int = 100,
        provider_id: Optional[uuid.UUID] = None
    ) -> tuple[List[LLM], int]:
        """Get LLMs list"""
        # Validate pagination params
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip cannot be negative")
        if limit <= 0:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        return self.llm_repository.list_llms(
            skip=skip,
            limit=limit,
            provider_id=provider_id
        )
    
    def get_llms_public_page(self, page: int, page_size: int) -> Tuple[List[LLMPublic], int]:
        """Get public LLMs page"""
        llms, total = self.list_llms(skip=(page - 1) * page_size, limit=page_size)
        return [LLMPublic(**llm.model_dump()) for llm in llms], total
    
    def get_llms_public_by_provider_id_page(self, provider_id: uuid.UUID, page: int, page_size: int) -> Tuple[List[LLMPublic], int]:
        """Get public LLMs by provider id page"""
        llms, total = self.list_llms(provider_id=provider_id, skip=(page - 1) * page_size, limit=page_size)
        return [LLMPublic(**llm.model_dump()) for llm in llms], total

    def get_llms_public_by_provider_id(self, provider_id: uuid.UUID) -> List[LLMPublic]:
        """Get public LLMs by provider id"""
        # Get LLMs list
        llms = self.llm_repository.get_llms_by_provider_id(provider_id)
        # Convert to public format
        public_llms = [LLMPublic(**llm.model_dump()) for llm in llms]
        return public_llms
    
    def get_llm_public_by_llm_id(self, llm_id: uuid.UUID) -> LLMPublic:
        """Get public LLM by LLM id"""
        llm = self.get_llm_by_id(llm_id)
        return LLMPublic(**llm.model_dump())