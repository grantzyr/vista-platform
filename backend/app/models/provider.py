import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, JSON, Column, Relationship
from sqlalchemy import Text
from enum import Enum

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.llm import LLM

class ProviderBase(SQLModel):
    """provider base model"""
    # name: str = Field(max_length=100, unique=True, index=True)
    display_name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # connection config
    base_url: Optional[str] = Field(default=None, max_length=255)
    api_key: Optional[str] = Field(default=None, max_length=255)
    
    # limit settings
    max_concurrent: Optional[int] = Field(default=None)

class ProviderCreate(ProviderBase):
    """create provider request model"""
    pass

class ProviderUpdate(SQLModel):
    """update provider request model"""
    display_name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None)
    base_url: Optional[str] = Field(default=None, max_length=255)
    api_key: Optional[str] = Field(default=None, max_length=255)
    max_concurrent: Optional[int] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))

# database model
class Provider(ProviderBase, BaseModel, table=True):
    """provider database model"""
    __tablename__ = "providers"
    
    # relations
    llms: List["LLM"] = Relationship(back_populates="provider")

# response model
class ProviderPublic(SQLModel):
    """provider public info model"""
    id: uuid.UUID
    display_name: str
    description: Optional[str]
    base_url: Optional[str]
    max_concurrent: Optional[int]
    created_at: datetime
    updated_at: datetime

class ProviderListResponse(SQLModel):
    """provider list response model"""
    data: List[ProviderPublic]
    count: int
    page: int
    page_size: int

class ProviderDeleteResponse(SQLModel):
    """provider delete response model"""
    data: uuid.UUID