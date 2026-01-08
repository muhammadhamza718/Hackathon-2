"""
Task event schemas for the Todo Backend
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
import uuid


class TaskEvent(BaseModel):
    """
    Base class for task events
    """
    event_id: uuid.UUID
    event_type: str
    timestamp: datetime
    task_id: uuid.UUID
    user_id: uuid.UUID
    payload: Dict[str, Any]


class TaskCreatedEvent(TaskEvent):
    """
    Event published when a task is created
    """
    event_type: str = "task.created"
    task_data: Dict[str, Any]


class TaskUpdatedEvent(TaskEvent):
    """
    Event published when a task is updated
    """
    event_type: str = "task.updated"
    old_values: Optional[Dict[str, Any]]
    new_values: Dict[str, Any]


class TaskDeletedEvent(TaskEvent):
    """
    Event published when a task is deleted
    """
    event_type: str = "task.deleted"
    task_data: Dict[str, Any]


class TaskCompletedEvent(TaskEvent):
    """
    Event published when a task is completed
    """
    event_type: str = "task.completed"


class RecurringTaskGeneratedEvent(TaskEvent):
    """
    Event published when a recurring task generates a new instance
    """
    event_type: str = "recurring_task.generated"
    parent_template_id: uuid.UUID