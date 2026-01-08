from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TodoInput(BaseModel):
    """Input model for creating a todo."""
    content: str
    due_date: Optional[datetime] = None


class TodoOutput(BaseModel):
    """Output model for a todo."""
    id: int
    content: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None


class TodoUpdateInput(BaseModel):
    """Input model for updating a todo."""
    id: int
    content: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TodoListInput(BaseModel):
    """Input model for listing todos."""
    limit: int = 100
    offset: int = 0
    completed: Optional[bool] = None


class TodoCompleteInput(BaseModel):
    """Input model for completing a todo."""
    id: int


class TodoDeleteInput(BaseModel):
    """Input model for deleting a todo."""
    id: int


class TodoOperationResponse(BaseModel):
    """Response model for todo operations."""
    success: bool
    message: str
    data: Optional[TodoOutput] = None
    data_list: Optional[List[TodoOutput]] = None