"""
Audit log model for the Todo application
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid


class AuditLogBase(SQLModel):
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    entity_type: str = Field(min_length=1)
    entity_id: uuid.UUID
    operation: str = Field(regex="^(create|update|delete|read)$")
    old_values: Optional[dict] = Field(default={})
    new_values: Optional[dict] = Field(default={})
    metadata: Optional[dict] = Field(default={})


class AuditLog(AuditLogBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: uuid.UUID
    timestamp: datetime