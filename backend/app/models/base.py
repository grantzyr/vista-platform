import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class TimestampMixin(SQLModel):
    """timestamp mixin"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UUIDMixin(SQLModel):
    """UUID primary key mixin"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class BaseModel(UUIDMixin, TimestampMixin):
    """base model"""
    pass

class Message(SQLModel):
    """message model"""
    message: str