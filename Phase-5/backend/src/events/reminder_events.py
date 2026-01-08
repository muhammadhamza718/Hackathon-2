"""
Reminder event schemas for the Todo Backend
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
import uuid


class ReminderEvent(BaseModel):
    """
    Base class for reminder events
    """
    event_id: uuid.UUID
    event_type: str
    timestamp: datetime
    reminder_id: uuid.UUID
    user_id: uuid.UUID
    task_id: Optional[uuid.UUID] = None
    scheduled_time: datetime
    payload: dict


class ReminderScheduledEvent(ReminderEvent):
    """
    Event published when a reminder is scheduled
    """
    event_type: str = "reminder.scheduled"
    notification_preferences: dict


class ReminderTriggeredEvent(ReminderEvent):
    """
    Event published when a reminder is triggered
    """
    event_type: str = "reminder.triggered"
    delivery_status: str


class ReminderCancelledEvent(ReminderEvent):
    """
    Event published when a reminder is cancelled
    """
    event_type: str = "reminder.cancelled"
    reason: str


class ReminderDeliveredEvent(ReminderEvent):
    """
    Event published when a reminder is delivered
    """
    event_type: str = "reminder.delivered"
    delivery_method: str  # email, push, in_app