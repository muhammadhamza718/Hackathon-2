from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging


class TodoError(Exception):
    """Base exception for todo-related errors."""
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code or "TODO_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class TodoNotFoundError(TodoError):
    """Raised when a todo item is not found."""
    def __init__(self, todo_id: int):
        super().__init__(
            f"Todo with ID {todo_id} not found",
            error_code="TODO_NOT_FOUND",
            details={"todo_id": todo_id}
        )


class TodoValidationError(TodoError):
    """Raised when todo validation fails."""
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(
            message,
            error_code="TODO_VALIDATION_ERROR",
            details=details
        )


class DatabaseError(TodoError):
    """Raised when database operations fail."""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            details=details
        )


class TodoErrorResponse(BaseModel):
    """Standard error response model."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


def handle_todo_error(error: TodoError) -> TodoErrorResponse:
    """Convert a TodoError to a standardized error response."""
    return TodoErrorResponse(
        error_code=error.error_code,
        message=error.message,
        details=error.details
    )


def log_error(error: Exception, logger: Optional[logging.Logger] = None, context: Optional[Dict[str, Any]] = None) -> None:
    """Log an error with optional context."""
    if logger is None:
        logger = logging.getLogger(__name__)

    log_message = f"Error: {str(error)}"
    if context:
        log_message += f" | Context: {context}"

    logger.error(log_message, exc_info=True)