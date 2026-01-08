from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    role: str = Field(default="user")


class User(UserBase, table=True):
    __tablename__ = "user"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"name": "createdAt"})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"name": "updatedAt"})

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str  # This would be handled by Better Auth, but included for completeness


class UserUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None