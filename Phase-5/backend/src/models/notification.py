"""
Notification model for the Todo application
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid


class NotificationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    task_id: Optional[uuid.UUID] = Field(default=None, foreign_key="task.id")
    type: str = Field(regex="^(email|push|in_app)$")
    title: str = Field(min_length=1)
    message: str = Field(min_length=1)
    scheduled_at: datetime
    sent_at: Optional[datetime] = None
    status: str = Field(default="pending", regex="^(pending|sent|failed)$")


class Notification(NotificationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="notifications")
    task: Optional["Task"] = Relationship(back_populates="notifications")


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(SQLModel):
    status: Optional[str] = None
    sent_at: Optional[datetime] = None


class NotificationRead(NotificationBase):
    id: uuid.UUID
    created_at: datetime