from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(SQLModel):
    user_id: str = Field(index=True)
    content: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Index for sorting by creation date
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Index for sorting by update date
    completed: bool = Field(default=False, index=True)  # Index for filtering by completion status
    content: str = Field(min_length=1, max_length=500, index=True)  # Index for searching content
    due_date: Optional[datetime] = Field(default=None, index=True)  # Index for sorting by due date


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime