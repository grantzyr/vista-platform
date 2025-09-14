import uuid
from typing import List, Optional, Tuple

from sqlmodel import Session, select
from fastapi import HTTPException

from app.repository.provider_repository import ProviderRepository
from app.models.provider import Provider, ProviderCreate, ProviderUpdate, ProviderPublic


class ProviderService:
    """Provider service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.provider_repository = ProviderRepository(session)
    
    def create_provider(self, provider_create: ProviderCreate) -> Provider:
        """Create provider"""
        return self.provider_repository.create_provider(provider_create=provider_create)
    
    def get_provider_by_id(self, provider_id: uuid.UUID) -> Provider:
        """Get provider by id"""
        provider = self.provider_repository.get_provider_by_id(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail=f"Provider with id {provider_id} not found")
        return provider
    
    def get_provider_with_llms(self, provider_id: uuid.UUID) -> Provider:
        """Get provider with LLMs"""
        provider = self.provider_repository.get_provider_with_llms(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail=f"Provider with id {provider_id} not found")
        return provider
    
    def update_provider(self, provider_id: uuid.UUID, provider_update: ProviderUpdate) -> Provider:
        """Update provider"""
        return self.provider_repository.update_provider(
            provider_id=provider_id, 
            provider_update=provider_update
        )
    
    def delete_provider(self, provider_id: uuid.UUID) -> bool:
        """Delete provider"""
        self.get_provider_by_id(provider_id)
        return self.provider_repository.delete_provider_by_id(provider_id)
    
    def list_providers(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Provider], int]:
        """Get providers list"""
        # Validate pagination params
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip cannot be negative")
        if limit <= 0:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        return self.provider_repository.list_providers(
            skip=skip,
            limit=limit
        )
    
    def get_providers_public_page(self, page: int, page_size: int) -> Tuple[List[ProviderPublic], int]:
        """Get public providers page"""
        providers, total = self.list_providers(skip=(page - 1) * page_size, limit=page_size)
        return [ProviderPublic(**provider.model_dump()) for provider in providers], total
    
    def get_provider_public_by_id(self, provider_id: uuid.UUID) -> ProviderPublic:
        """Get public provider by provider id"""
        provider = self.get_provider_by_id(provider_id)
        return ProviderPublic(**provider.model_dump())
