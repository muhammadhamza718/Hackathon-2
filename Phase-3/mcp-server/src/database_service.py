"""Optimized database service for the MCP Todo Server"""
from sqlmodel import create_engine, Session, select
from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field as PydanticField
import os
import hashlib
import time
from threading import Lock


class SimpleCache:
    """A simple in-memory cache with TTL (Time To Live) for MCP server"""

    def __init__(self):
        self._cache = {}
        self._lock = Lock()

    def set(self, key: str, value, ttl: int = 300) -> None:  # Default 5 minutes TTL
        """Set a value in cache with TTL in seconds"""
        with self._lock:
            expiration_time = time.time() + ttl
            self._cache[key] = {
                'value': value,
                'expiration': expiration_time
            }

    def get(self, key: str):
        """Get a value from cache, return None if expired or not found"""
        with self._lock:
            if key not in self._cache:
                return None

            item = self._cache[key]
            if time.time() > item['expiration']:
                # Remove expired item
                del self._cache[key]
                return None

            return item['value']

    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all cache"""
        with self._lock:
            self._cache.clear()

    def invalidate_cache_pattern(self, pattern: str) -> int:
        """Remove all cache entries matching a pattern and return count of removed items"""
        with self._lock:
            keys_to_remove = [key for key in self._cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self._cache[key]
            return len(keys_to_remove)


# Global cache instance for MCP server
cache = SimpleCache()


# Define the Todo model for database operations (matching the backend)
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True, max_length=500)  # Indexed for searching
    completed: bool = Field(default=False, index=True)  # Indexed for filtering
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Indexed for sorting
    due_date: Optional[datetime] = Field(default=None, index=True)  # Indexed for date queries
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Indexed for updates


# Define the request/response models
class AddTodoRequest(BaseModel):
    content: str = PydanticField(
        ...,
        description="The content of the todo item",
        min_length=1,
        max_length=500,
        strip_whitespace=True
    )
    due_date: Optional[str] = PydanticField(
        None,
        description="Optional due date in ISO format",
        pattern=r'^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2}))?$'
    )


class AddTodoResponse(BaseModel):
    success: bool
    todo_id: Optional[int] = None
    message: str


class ListTodosRequest(BaseModel):
    completed: Optional[bool] = PydanticField(
        None,
        description="Filter by completion status (true for completed, false for pending, null for all)"
    )
    limit: Optional[int] = PydanticField(
        50,
        description="Maximum number of todos to return (pagination)",
        ge=1,
        le=100
    )
    offset: Optional[int] = PydanticField(
        0,
        description="Number of todos to skip (pagination)",
        ge=0
    )
    search: Optional[str] = PydanticField(
        None,
        description="Optional search term to filter todos by content"
    )


class TodoItem(BaseModel):
    id: int
    content: str
    completed: bool
    created_at: datetime
    due_date: Optional[datetime] = None
    updated_at: datetime


class ListTodosResponse(BaseModel):
    success: bool
    todos: List[TodoItem]
    total_count: int
    message: str


class CompleteTodoRequest(BaseModel):
    todo_id: int = PydanticField(
        ...,
        description="The ID of the todo to mark as completed",
        ge=1
    )


class CompleteTodoResponse(BaseModel):
    success: bool
    message: str
    todo: Optional[TodoItem] = None


class DeleteTodoRequest(BaseModel):
    todo_id: int = PydanticField(
        ...,
        description="The ID of the todo to delete",
        ge=1
    )


class DeleteTodoResponse(BaseModel):
    success: bool
    message: str


class UpdateTodoRequest(BaseModel):
    todo_id: int = PydanticField(
        ...,
        description="The ID of the todo to update",
        ge=1
    )
    content: Optional[str] = PydanticField(
        None,
        description="The new content of the todo item",
        min_length=1,
        max_length=500,
        strip_whitespace=True
    )
    completed: Optional[bool] = PydanticField(
        None,
        description="The new completion status of the todo"
    )
    due_date: Optional[str] = PydanticField(
        None,
        description="Optional new due date in ISO format",
        pattern=r'^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2}))?$'
    )


class UpdateTodoResponse(BaseModel):
    success: bool
    message: str
    todo: Optional[TodoItem] = None


class OptimizedTodoService:
    """Optimized service with indexed queries for todo operations"""

    def __init__(self):
        # Initialize database connection - using environment variable for database URL
        database_url = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
        self.engine = create_engine(database_url, echo=True)
        # Create tables with indexes
        SQLModel.metadata.create_all(self.engine)

    def add_todo(self, content: str, due_date: Optional[str] = None) -> AddTodoResponse:
        """Add a new todo item to the database with optimized indexing and cache clearing."""
        try:
            # Additional validation
            if not content or len(content.strip()) == 0:
                return AddTodoResponse(
                    success=False,
                    message="Todo content cannot be empty"
                )

            if len(content.strip()) > 500:
                return AddTodoResponse(
                    success=False,
                    message="Todo content cannot exceed 500 characters"
                )

            # Parse due date if provided
            parsed_due_date = None
            if due_date:
                try:
                    from datetime import datetime
                    # Validate ISO format date
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    # Ensure due date is not in the past
                    if parsed_due_date < datetime.utcnow():
                        return AddTodoResponse(
                            success=False,
                            message="Due date cannot be in the past"
                        )
                except ValueError:
                    return AddTodoResponse(
                        success=False,
                        message=f"Invalid date format: {due_date}. Expected ISO format."
                    )

            # Create new todo
            new_todo = Todo(
                content=content.strip(),
                due_date=parsed_due_date
            )

            # Save to database
            with Session(self.engine) as session:
                session.add(new_todo)
                session.commit()
                session.refresh(new_todo)

            # Clear any cached list queries that might be affected by the new todo
            # This ensures that any cached lists will be refreshed
            cache.invalidate_cache_pattern("list_todos:")

            return AddTodoResponse(
                success=True,
                todo_id=new_todo.id,
                message=f"Todo '{content}' added successfully"
            )
        except Exception as e:
            return AddTodoResponse(
                success=False,
                message=f"Error adding todo: {str(e)}"
            )

    def list_todos(self, completed: Optional[bool] = None, limit: int = 50, offset: int = 0, search: Optional[str] = None) -> ListTodosResponse:
        """List todos with optional filtering and pagination using optimized indexed queries and caching."""
        try:
            # Create cache key based on parameters
            cache_key = f"list_todos:completed_{completed}:limit_{limit}:offset_{offset}:search_{search}"

            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            with Session(self.engine) as session:
                # Build the query with optional filtering
                statement = select(Todo)

                # Apply completion status filter (uses indexed column)
                if completed is not None:
                    statement = statement.where(Todo.completed == completed)

                # Apply search filter if provided (uses indexed content column)
                if search:
                    statement = statement.where(Todo.content.icontains(search))

                # Apply ordering by creation date (uses indexed column)
                statement = statement.order_by(Todo.created_at.desc())

                # Apply pagination
                statement = statement.offset(offset).limit(limit)

                # Execute query to get todos
                todos = session.exec(statement).all()

                # Get total count for pagination info
                count_statement = select(Todo)
                if completed is not None:
                    count_statement = count_statement.where(Todo.completed == completed)
                if search:
                    count_statement = count_statement.where(Todo.content.icontains(search))
                total_count = session.exec(count_statement).count()

                # Convert to response format
                todo_items = [
                    TodoItem(
                        id=todo.id,
                        content=todo.content,
                        completed=todo.completed,
                        created_at=todo.created_at,
                        due_date=todo.due_date,
                        updated_at=todo.updated_at
                    )
                    for todo in todos
                ]

                result = ListTodosResponse(
                    success=True,
                    todos=todo_items,
                    total_count=total_count,
                    message=f"Retrieved {len(todo_items)} todos out of {total_count} total"
                )

                # Cache the result for 2 minutes
                cache.set(cache_key, result, ttl=120)

                return result
        except Exception as e:
            return ListTodosResponse(
                success=False,
                todos=[],
                total_count=0,
                message=f"Error listing todos: {str(e)}"
            )

    def get_todo_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """Get a todo by its ID with caching."""
        # Create cache key
        cache_key = f"todo:{todo_id}"

        # Try to get from cache first
        cached_todo = cache.get(cache_key)
        if cached_todo is not None:
            return cached_todo

        # If not in cache, fetch from database
        with Session(self.engine) as session:
            statement = select(Todo).where(Todo.id == todo_id)
            result = session.execute(statement)
            todo = result.scalar_one_or_none()

            if todo is not None:
                # Convert to TodoItem and cache the result
                todo_item = TodoItem(
                    id=todo.id,
                    content=todo.content,
                    completed=todo.completed,
                    created_at=todo.created_at,
                    due_date=todo.due_date,
                    updated_at=todo.updated_at
                )
                cache.set(cache_key, todo_item, ttl=300)  # Cache for 5 minutes
                return todo_item

        return None

    def complete_todo(self, todo_id: int) -> CompleteTodoResponse:
        """Mark a todo as completed with optimized lookup using indexed ID and cache invalidation."""
        try:
            # Validate that the todo exists
            with Session(self.engine) as session:
                # Get the todo by ID (uses indexed primary key)
                todo = session.get(Todo, todo_id)

                if todo is None:
                    return CompleteTodoResponse(
                        success=False,
                        message=f"Todo with ID {todo_id} not found"
                    )

                # Update the completion status
                todo.completed = True
                todo.updated_at = datetime.utcnow()
                session.add(todo)
                session.commit()
                session.refresh(todo)

                # Return the updated todo
                todo_item = TodoItem(
                    id=todo.id,
                    content=todo.content,
                    completed=todo.completed,
                    created_at=todo.created_at,
                    due_date=todo.due_date,
                    updated_at=todo.updated_at
                )

                # Invalidate the cache for this todo
                cache.delete(f"todo:{todo_id}")

                return CompleteTodoResponse(
                    success=True,
                    message=f"Todo '{todo.content}' marked as completed",
                    todo=todo_item
                )
        except Exception as e:
            return CompleteTodoResponse(
                success=False,
                message=f"Error completing todo: {str(e)}"
            )

    def delete_todo(self, todo_id: int) -> DeleteTodoResponse:
        """Delete a todo from the database with optimized lookup using indexed ID and cache invalidation."""
        try:
            # Validate that the todo exists
            with Session(self.engine) as session:
                # Get the todo by ID (uses indexed primary key)
                todo = session.get(Todo, todo_id)

                if todo is None:
                    return DeleteTodoResponse(
                        success=False,
                        message=f"Todo with ID {todo_id} not found"
                    )

                # Delete the todo
                session.delete(todo)
                session.commit()

                # Invalidate the cache for this todo
                cache.delete(f"todo:{todo_id}")

                return DeleteTodoResponse(
                    success=True,
                    message=f"Todo '{todo.content}' deleted successfully"
                )
        except Exception as e:
            return DeleteTodoResponse(
                success=False,
                message=f"Error deleting todo: {str(e)}"
            )

    def update_todo(self, todo_id: int, content: Optional[str] = None, completed: Optional[bool] = None, due_date: Optional[str] = None) -> UpdateTodoResponse:
        """Update a todo in the database with optimized lookup using indexed ID and cache invalidation."""
        try:
            # Validate that the todo exists
            with Session(self.engine) as session:
                # Get the todo by ID (uses indexed primary key)
                todo = session.get(Todo, todo_id)

                if todo is None:
                    return UpdateTodoResponse(
                        success=False,
                        message=f"Todo with ID {todo_id} not found"
                    )

                # Track original values for the response
                original_content = todo.content

                # Update fields if provided
                if content is not None:
                    if len(content.strip()) == 0:
                        return UpdateTodoResponse(
                            success=False,
                            message="Todo content cannot be empty"
                        )
                    if len(content.strip()) > 500:
                        return UpdateTodoResponse(
                            success=False,
                            message="Todo content cannot exceed 500 characters"
                        )
                    todo.content = content.strip()

                if completed is not None:
                    todo.completed = completed

                if due_date is not None:
                    try:
                        from datetime import datetime
                        # Validate ISO format date
                        parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        # Ensure due date is not in the past (only if changing to incomplete)
                        if not completed and parsed_due_date < datetime.utcnow():
                            return UpdateTodoResponse(
                                success=False,
                                message="Due date cannot be in the past"
                            )
                        todo.due_date = parsed_due_date
                    except ValueError:
                        return UpdateTodoResponse(
                            success=False,
                            message=f"Invalid date format: {due_date}. Expected ISO format."
                        )

                # Update the timestamp
                todo.updated_at = datetime.utcnow()

                # Save to database
                session.add(todo)
                session.commit()
                session.refresh(todo)

                # Return the updated todo
                todo_item = TodoItem(
                    id=todo.id,
                    content=todo.content,
                    completed=todo.completed,
                    created_at=todo.created_at,
                    due_date=todo.due_date,
                    updated_at=todo.updated_at
                )

                # Invalidate the cache for this todo
                cache.delete(f"todo:{todo_id}")

                return UpdateTodoResponse(
                    success=True,
                    message=f"Todo '{original_content}' updated successfully",
                    todo=todo_item
                )
        except Exception as e:
            return UpdateTodoResponse(
                success=False,
                message=f"Error updating todo: {str(e)}"
            )