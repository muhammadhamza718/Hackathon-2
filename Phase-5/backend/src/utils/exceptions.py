"""
Custom exceptions for the Todo Backend
"""
from fastapi import HTTPException, status
from typing import Optional


class TodoException(HTTPException):
    """
    Custom exception for Todo application errors
    """
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class TaskNotFoundException(TodoException):
    """
    Exception raised when a task is not found
    """
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class RecurringTaskTemplateNotFoundException(TodoException):
    """
    Exception raised when a recurring task template is not found
    """
    def __init__(self, template_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recurring task template with id {template_id} not found"
        )


class UserNotFoundException(TodoException):
    """
    Exception raised when a user is not found
    """
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


class InvalidRecurrencePatternException(TodoException):
    """
    Exception raised when an invalid recurrence pattern is provided
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recurrence pattern provided"
        )


def handle_exception(exc: Exception, logger):
    """
    Handle exceptions and log them appropriately
    """
    logger.error(f"Exception occurred: {exc}")
    raise exc