from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlmodel import select
from models.user import User
from models.task import Task, TaskCreate, TaskUpdate, TaskRead
from schemas.task import TaskCreate as TaskCreateSchema, TaskRead as TaskReadSchema, TaskUpdate as TaskUpdateSchema
from db.session import get_async_session
from api.deps import get_current_user
from datetime import datetime
import uuid

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskReadSchema])
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    List all tasks for the authenticated user.
    Verified by matching the URL user_id with the JWT current_user.id.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    statement = select(Task).where(Task.user_id == current_user.id)
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return tasks


@router.post("/{user_id}/tasks", response_model=TaskReadSchema)
async def create_task(
    user_id: str,
    task_data: TaskCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=False,
        user_id=current_user.id
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskReadSchema)
async def get_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or permission denied"
        )

    return task[0]


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskReadSchema)
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or permission denied"
        )

    task = task[0]

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or permission denied"
        )

    task = task[0]

    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskReadSchema)
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Violation: URL ID does not match Session ID"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or permission denied"
        )

    task = task[0]

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task