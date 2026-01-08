from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging


class TodoError(Exception):
    """Base exception for todo-related errors."""
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None, user_friendly_message: Optional[str] = None):
        self.message = message
        self.error_code = error_code or "TODO_ERROR"
        self.details = details or {}
        self.user_friendly_message = user_friendly_message or message
        super().__init__(self.message)


class TodoNotFoundError(TodoError):
    """Raised when a todo item is not found."""
    def __init__(self, todo_id: int):
        super().__init__(
            f"Todo with ID {todo_id} not found",
            error_code="TODO_NOT_FOUND",
            details={"todo_id": todo_id},
            user_friendly_message=f"I couldn't find a todo with ID {todo_id}. It may have been deleted already."
        )


class TodoValidationError(TodoError):
    """Raised when todo validation fails."""
    def __init__(self, message: str, field: Optional[str] = None, user_friendly_message: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(
            message,
            error_code="TODO_VALIDATION_ERROR",
            details=details,
            user_friendly_message=user_friendly_message or "There was an issue with the information provided."
        )


class DatabaseError(TodoError):
    """Raised when database operations fail."""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            details=details,
            user_friendly_message="I'm having trouble accessing the database. Please try again later."
        )


class MCPServerError(TodoError):
    """Raised when MCP server operations fail."""
    def __init__(self, message: str, operation: Optional[str] = None):
        details = {"operation": operation} if operation else {}
        super().__init__(
            message,
            error_code="MCP_SERVER_ERROR",
            details=details,
            user_friendly_message="I'm having trouble connecting to the todo service. Please try again later."
        )


class TodoErrorResponse(BaseModel):
    """Standard error response model."""
    success: bool = False
    error_code: str
    message: str
    user_friendly_message: str
    details: Optional[Dict[str, Any]] = None


def handle_todo_error(error: TodoError) -> TodoErrorResponse:
    """Convert a TodoError to a standardized error response."""
    return TodoErrorResponse(
        error_code=error.error_code,
        message=error.message,
        user_friendly_message=error.user_friendly_message,
        details=error.details
    )


def handle_generic_error(error: Exception) -> TodoErrorResponse:
    """Convert any exception to a standardized error response."""
    if isinstance(error, TodoError):
        return handle_todo_error(error)

    # Handle other types of exceptions
    error_code = "INTERNAL_ERROR"
    message = str(error)
    user_friendly_message = "An unexpected error occurred. Please try again later."

    # Provide more specific user feedback for common errors
    if "timeout" in message.lower():
        user_friendly_message = "The request took too long to process. Please try again."
    elif "connection" in message.lower() or "connect" in message.lower():
        user_friendly_message = "I'm having trouble connecting to the service. Please try again later."
    elif "validation" in message.lower() or "invalid" in message.lower():
        user_friendly_message = "The information provided seems to be invalid. Please check and try again."

    return TodoErrorResponse(
        error_code=error_code,
        message=message,
        user_friendly_message=user_friendly_message,
        details={"original_error_type": type(error).__name__}
    )


def log_error(error: Exception, logger: Optional[logging.Logger] = None, context: Optional[Dict[str, Any]] = None) -> None:
    """Log an error with optional context."""
    if logger is None:
        logger = logging.getLogger(__name__)

    log_message = f"Error: {str(error)}"
    if context:
        log_message += f" | Context: {context}"

    logger.error(log_message, exc_info=True)