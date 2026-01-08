from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlmodel import select
from models.user import User
from models.task import Task
from schemas.user import UserRead
from db.session import get_async_session
from api.deps import get_current_admin
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class UserRoleUpdate(BaseModel):
    role: str

@router.get("/users", response_model=List[UserRead])
async def list_all_users(
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """
    List all users in the system.
    Admin only endpoint.
    """
    statement = select(User)
    result = await session.execute(statement)
    users = result.scalars().all()

    return users


@router.get("/users/{user_id}/tasks", response_model=List[dict])
async def get_user_tasks(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific user.
    Admin only endpoint.
    """
    # First verify the target user exists
    user_statement = select(User).where(User.id == user_id)
    user_result = await session.execute(user_statement)
    target_user = user_result.scalars().first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get tasks for the specified user
    task_statement = select(Task).where(Task.user_id == user_id)
    task_result = await session.execute(task_statement)
    tasks = task_result.scalars().all()

    # Convert tasks to dict format to match schema
    task_dicts = []
    for task in tasks:
        task_dicts.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": task.user_id,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        })

    return task_dicts

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a user by ID.
    Admin only endpoint.
    """
    user_statement = select(User).where(User.id == user_id)
    result = await session.execute(user_statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return None

@router.patch("/users/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: str,
    role_update: UserRoleUpdate,
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a user's role.
    Admin only endpoint.
    """
    user_statement = select(User).where(User.id == user_id)
    result = await session.execute(user_statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_task(
    user_id: str,
    task_id: str,
    current_admin: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for a user.
    Admin only endpoint.
    """
    # Verify task exists and belongs to user
    task_statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(task_statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return None