import uuid
from typing import Any, Optional, List

from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.models.provider import Provider, ProviderCreate, ProviderUpdate


class ProviderRepository:
    """Provider repository"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_provider(self, *, provider_create: ProviderCreate) -> Provider:
        """Create provider"""
        db_obj = Provider.model_validate(provider_create)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def get_provider_by_id(self, provider_id: uuid.UUID) -> Provider | None:
        """Get provider by id"""
        statement = select(Provider).where(Provider.id == provider_id)
        return self.session.exec(statement).first()
    
    def update_provider(self, *, provider_id: uuid.UUID, provider_update: ProviderUpdate) -> Provider:
        """Update provider"""
        provider_data = provider_update.model_dump(exclude_unset=True)
        db_provider = self.get_provider_by_id(provider_id)
        db_provider.sqlmodel_update(provider_data)
        self.session.add(db_provider)
        self.session.commit()
        self.session.refresh(db_provider)
        return db_provider
    
    def delete_provider_by_id(self, provider_id: uuid.UUID) -> bool:
        """Delete provider by id"""
        db_provider = self.get_provider_by_id(provider_id)
        if db_provider:
            self.session.delete(db_provider)
            self.session.commit()
            return True
        return False
    
    def list_providers(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[List[Provider], int]:
        """Get providers list"""
        statement = select(Provider)
        count_statement = select(func.count(Provider.id))
        
        total = self.session.exec(count_statement).first()
        
        statement = statement.offset(skip).limit(limit)
        providers = list(self.session.exec(statement).all())
        
        return providers, total or 0
    
    def get_provider_with_llms(self, provider_id: uuid.UUID) -> Provider | None:
        """Get provider with LLMs"""
        statement = (
            select(Provider)
            .where(Provider.id == provider_id)
            .options(selectinload(Provider.llms))
        )
        return self.session.exec(statement).first()
