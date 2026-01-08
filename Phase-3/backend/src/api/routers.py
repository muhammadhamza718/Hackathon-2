from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..services.todo_service import TodoService
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..models.database import get_sync_session
from sqlmodel import Session

# Create routers
admin_router = APIRouter(prefix="/api/admin", tags=["admin"])
tasks_router = APIRouter(prefix="/api", tags=["tasks"])

# --- Mock User Models for Admin ---
class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    image: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

# --- Admin Routes ---

@admin_router.get("/users", response_model=List[User])
async def get_users():
    """Get all users (Mock implementation)"""
    # In a real app, this would query the User table or Auth provider
    return [
        User(
            id="user_123",
            name="Demo User",
            email="demo@example.com",
            role="user",
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        ),
        User(
            id="admin_456",
            name="Admin User",
            email="admin@example.com",
            role="admin",
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
    ]

@admin_router.get("/users/{user_id}/tasks", response_model=List[TodoRead])
async def get_user_tasks(user_id: str, session: Session = Depends(get_sync_session)):
    """Get tasks for a specific user"""
    # For now, we return all tasks as we don't strictly enforce user_id filtering in the simple service yet
    # In production, filter by user_id
    todos = TodoService.get_todos_by_user_sync(session, user_id)
    return [TodoRead.from_orm(t) for t in todos]

@admin_router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user (Mock)"""
    return {"success": True, "message": f"User {user_id} deleted"}

@admin_router.patch("/users/{user_id}/role")
async def update_user_role(user_id: str, role: str):
    """Update user role (Mock)"""
    return {"id": user_id, "role": role}

@admin_router.delete("/users/{user_id}/tasks/{task_id}")
async def delete_user_task(user_id: str, task_id: int, session: Session = Depends(get_sync_session)):
    """Delete a user's task"""
    success = TodoService.delete_todo_sync(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}


# --- Task Routes ---

@tasks_router.get("/{user_id}/tasks", response_model=List[TodoRead])
async def get_my_tasks(user_id: str, session: Session = Depends(get_sync_session)):
    """Get all tasks for the current user"""
    todos = TodoService.get_todos_by_user_sync(session, user_id)
    return [TodoRead.from_orm(t) for t in todos]

@tasks_router.post("/{user_id}/tasks", response_model=TodoRead)
async def create_task(user_id: str, task: TodoCreate, session: Session = Depends(get_sync_session)):
    """Create a new task"""
    # Ideally link task to user_id here
    return TodoService.create_todo_sync(session, task)

@tasks_router.put("/{user_id}/tasks/{task_id}", response_model=TodoRead)
async def update_task(user_id: str, task_id: int, task_update: TodoUpdate, session: Session = Depends(get_sync_session)):
    """Update a task"""
    updated_todo = TodoService.update_todo_sync(session, task_id, task_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_todo

@tasks_router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(user_id: str, task_id: int, session: Session = Depends(get_sync_session)):
    """Delete a task"""
    success = TodoService.delete_todo_sync(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}

@tasks_router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TodoRead)
async def toggle_task_complete(user_id: str, task_id: int, completed: bool, session: Session = Depends(get_sync_session)):
    """Toggle task completion"""
    # Note: completed param is currently unused in service logic explicitly for 'toggle', 
    # but service has 'complete_todo_sync'. 
    # Let's implement generic update for toggle
    mock_update = TodoUpdate(completed=completed)
    updated_todo = TodoService.update_todo_sync(session, task_id, mock_update)
    if not updated_todo:
         raise HTTPException(status_code=404, detail="Task not found")
    return updated_todo
