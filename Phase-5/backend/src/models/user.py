"""
User model for the Todo application
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str
    notification_preferences: Optional[dict] = Field(default={})


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    recurring_tasks: List["RecurringTaskTemplate"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    notification_preferences: Optional[dict] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool