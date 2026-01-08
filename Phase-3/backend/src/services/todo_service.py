from sqlmodel import Session, select
from typing import List, Optional
from models.task import Task, TaskCreate, TaskUpdate, TaskRead
from datetime import datetime
from ..utils.cache import cache, cache_result, cache_with_key


class TodoService:
    @staticmethod
    def create_todo_sync(session: Session, todo_create: TaskCreate, user_id: str) -> Task:
        """Create a new task item and clear related cache entries."""
        todo = Task(**todo_create.dict(), user_id=user_id)
        todo.created_at = datetime.utcnow()
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)

        # Clear cache patterns for this user
        from ..utils.cache import invalidate_cache_pattern
        invalidate_cache_pattern(f"todos_list:{user_id}:")

        return todo

    @staticmethod
    def get_todo_by_id_sync(session: Session, todo_id: int, user_id: str) -> Optional[Task]:
        """Get a task by its ID with caching and user filtering."""
        # Create cache key
        cache_key = f"todo:{user_id}:{todo_id}"

        # Try to get from cache first
        cached_todo = cache.get(cache_key)
        if cached_todo is not None:
            return cached_todo

        # If not in cache, fetch from database
        statement = select(Task).where(Task.id == todo_id, Task.user_id == user_id)
        result = session.execute(statement)
        todo = result.scalar_one_or_none()

        # Cache the result if found (for 5 minutes)
        if todo is not None:
            cache.set(cache_key, todo, ttl=300)

        return todo

    @staticmethod
    def get_todos_sync(session: Session, user_id: str, offset: int = 0, limit: int = 100, completed: Optional[bool] = None) -> List[Task]:
        """Get a list of tasks for a user with optional pagination and filtering."""
        # Create cache key based on parameters
        cache_key = f"todos_list:{user_id}:offset_{offset}:limit_{limit}:completed_{completed}"

        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        statement = select(Task).where(Task.user_id == user_id)

        # Apply completion status filter if provided (uses indexed column)
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Apply ordering by creation date (uses indexed column)
        statement = statement.order_by(Task.created_at.desc())

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        result = session.execute(statement)
        todos = result.scalars().all()

        # Cache the result for 2 minutes
        cache.set(cache_key, todos, ttl=120)

        return todos

    @staticmethod
    def get_todos_by_user_sync(session: Session, user_id: str) -> List[Task]:
        """Get all tasks for a specific user (placeholder - would need user relationship)."""
        # For now, return all tasks; in a real implementation, you'd filter by user
        statement = select(Task).order_by(Task.created_at.desc())
        result = session.execute(statement)
        return result.scalars().all()

    @staticmethod
    def search_todos_sync(session: Session, search_term: str, limit: int = 10) -> List[Task]:
        """Search tasks by title with optimized query and caching."""
        if not search_term:
            return []

        # Create cache key based on search parameters
        cache_key = f"search_todos:term_{search_term}:limit_{limit}"

        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Use the indexed title column for searching
        statement = select(Task).where(
            Task.title.icontains(search_term)  # Case-insensitive search using indexed column
        ).order_by(Task.created_at.desc()).limit(limit)

        result = session.execute(statement)
        todos = result.scalars().all()

        # Cache the result for 5 minutes (searches might be repeated)
        cache.set(cache_key, todos, ttl=300)

        return todos

    @staticmethod
    def get_todos_by_due_date_range_sync(session: Session, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[Task]:
        """Get tasks within a date range with caching (not implemented correctly for Tasks yet)."""
        # Tasks don't have a due_date in models/task.py presently, using created_at as fallback
        # Create cache key based on date range
        start_str = start_date.isoformat() if start_date else "none"
        end_str = end_date.isoformat() if end_date else "none"
        cache_key = f"todos_by_date_range:start_{start_str}:end_{end_str}"

        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        statement = select(Task)

        if start_date:
            statement = statement.where(Task.created_at >= start_date)
        if end_date:
            statement = statement.where(Task.created_at <= end_date)

        # Apply ordering by created_at
        statement = statement.order_by(Task.created_at.asc())

        result = session.execute(statement)
        todos = result.scalars().all()

        # Cache the result for 5 minutes
        cache.set(cache_key, todos, ttl=300)

        return todos

    @staticmethod
    def get_todos_by_completion_status_sync(session: Session, completed: bool) -> List[Task]:
        """Get tasks by completion status with optimized query and caching."""
        # Create cache key
        cache_key = f"todos_by_status:completed_{completed}"

        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        statement = select(Task).where(Task.completed == completed).order_by(Task.created_at.desc())
        result = session.execute(statement)
        todos = result.scalars().all()

        # Cache the result for 2 minutes
        cache.set(cache_key, todos, ttl=120)

        return todos

    @staticmethod
    def update_todo_sync(session: Session, todo_id: int, user_id: str, todo_update: TaskUpdate) -> Optional[Task]:
        """Update a task item if it belongs to the user."""
        statement = select(Task).where(Task.id == todo_id, Task.user_id == user_id)
        result = session.execute(statement)
        todo = result.scalar_one_or_none()

        if not todo:
            return None

        # Update fields that are provided
        update_data = todo_update.dict(exclude_unset=True)
        
        # Mapping for agent compatibility: if 'content' is provided in update but not 'title'
        if 'content' in update_data and 'title' not in update_data:
            update_data['title'] = update_data.pop('content')

        for field, value in update_data.items():
            if hasattr(todo, field):
                setattr(todo, field, value)

        todo.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(todo)

        # Invalidate the cache for this todo and related lists
        cache.delete(f"todo:{user_id}:{todo_id}")
        from ..utils.cache import invalidate_cache_pattern
        invalidate_cache_pattern(f"todos_list:{user_id}:")

        return todo

    @staticmethod
    def delete_todo_sync(session: Session, todo_id: int, user_id: str) -> bool:
        """Delete a task item if it belongs to the user."""
        statement = select(Task).where(Task.id == todo_id, Task.user_id == user_id)
        result = session.execute(statement)
        todo = result.scalar_one_or_none()

        if not todo:
            return False

        session.delete(todo)
        session.commit()

        # Invalidate the cache for this todo and related lists
        cache.delete(f"todo:{user_id}:{todo_id}")
        from ..utils.cache import invalidate_cache_pattern
        invalidate_cache_pattern(f"todos_list:{user_id}:")

        return True

    @staticmethod
    def complete_todo_sync(session: Session, todo_id: int, user_id: str) -> Optional[Task]:
        """Mark a task as completed if it belongs to the user."""
        statement = select(Task).where(Task.id == todo_id, Task.user_id == user_id)
        result = session.execute(statement)
        todo = result.scalar_one_or_none()

        if not todo:
            return None

        todo.completed = True
        todo.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(todo)

        # Invalidate the cache for this todo and related lists
        cache.delete(f"todo:{user_id}:{todo_id}")
        from ..utils.cache import invalidate_cache_pattern
        invalidate_cache_pattern(f"todos_list:{user_id}:")

        return todo