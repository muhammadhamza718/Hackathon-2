"""
Task model for the Todo application
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="pending", regex="^(pending|completed|archived)$")
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    tags: Optional[List[str]] = Field(default=[])
    recurrence_pattern: Optional[dict] = Field(default={})
    user_id: uuid.UUID = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    notifications: List["Notification"] = Relationship(back_populates="task")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    recurrence_pattern: Optional[dict] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class RecurringTaskTemplateBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    recurrence_pattern: dict = Field(default={})
    task_template: dict = Field(default={})
    user_id: uuid.UUID = Field(foreign_key="user.id")
    active: bool = Field(default=True)


class RecurringTaskTemplate(RecurringTaskTemplateBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="recurring_tasks")


class RecurringTaskTemplateCreate(RecurringTaskTemplateBase):
    pass


class RecurringTaskTemplateUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    recurrence_pattern: Optional[dict] = None
    task_template: Optional[dict] = None
    active: Optional[bool] = None


class RecurringTaskTemplateRead(RecurringTaskTemplateBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime