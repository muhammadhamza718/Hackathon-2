from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None