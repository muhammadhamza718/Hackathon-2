"""
Audit event schemas for the Todo Backend
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid


class AuditEvent(BaseModel):
    """
    Base class for audit events
    """
    event_id: uuid.UUID
    event_type: str
    timestamp: datetime
    user_id: Optional[uuid.UUID] = None
    entity_type: str
    entity_id: uuid.UUID
    operation: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    metadata: Optional[dict] = None


class AuditCreatedEvent(AuditEvent):
    """
    Event published when an entity is created
    """
    event_type: str = "audit.created"


class AuditUpdatedEvent(AuditEvent):
    """
    Event published when an entity is updated
    """
    event_type: str = "audit.updated"


class AuditDeletedEvent(AuditEvent):
    """
    Event published when an entity is deleted
    """
    event_type: str = "audit.deleted"


class AuditReadEvent(AuditEvent):
    """
    Event published when an entity is read
    """
    event_type: str = "audit.read"