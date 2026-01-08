from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .priority import Priority


@dataclass
class Task:
    """
    Represents a single todo item with the following attributes:
    - id: auto-generated sequential unique identifier for the task (starting from 1)
    - title: required text string describing the task (max 50 characters)
    - description: optional text string with additional details (max 200 characters)
    - priority: priority level (Low, Medium, High)
    - completed: boolean value indicating completion status
    - tags: list of tag strings
    - created_at: timestamp when the task was created
    """
    id: int
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the task data after initialization"""
        self.validate()

    def validate(self):
        """Validate the task fields according to the specification"""
        # Validate title length (1-50 characters)
        if not (1 <= len(self.title) <= 50):
            raise ValueError(f"Title must be between 1 and 50 characters, got {len(self.title)}")

        # Validate description length (0-200 characters)
        if not (0 <= len(self.description) <= 200):
            raise ValueError(f"Description must be between 0 and 200 characters, got {len(self.description)}")

        # Validate id is positive
        if self.id < 1:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        # Validate completed is boolean
        if not isinstance(self.completed, bool):
            raise ValueError(f"Completed must be a boolean, got {type(self.completed)}")

        # Validate priority is a Priority enum
        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be a Priority enum, got {type(self.priority)}")

        # Validate tags is a list of strings
        if not isinstance(self.tags, list):
            raise ValueError(f"Tags must be a list, got {type(self.tags)}")

        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError(f"Each tag must be a string, got {type(tag)} in tags list")
            if len(tag) == 0:
                raise ValueError("Tags cannot be empty strings")
            if len(tag) > 50:  # Reasonable limit for tag length
                raise ValueError(f"Tag '{tag}' is too long (max 50 chars)")


def validate_task_data(title: str, description: str = "", priority: Optional[Priority] = None, tags: Optional[List[str]] = None) -> None:
    """
    Validate task data without creating a Task instance.

    Args:
        title: Task title (required, 1-50 characters)
        description: Task description (optional, 0-200 characters)
        priority: Task priority (optional, defaults to MEDIUM)
        tags: Task tags (optional, list of strings)

    Raises:
        ValueError: If validation fails
    """
    # Validate title length (1-50 characters)
    if not isinstance(title, str):
        raise ValueError("Title must be a string")

    if not (1 <= len(title) <= 50):
        raise ValueError(f"Title must be between 1 and 50 characters, got {len(title)}")

    # Validate description length (0-200 characters)
    if not isinstance(description, str):
        raise ValueError("Description must be a string")

    if not (0 <= len(description) <= 200):
        raise ValueError(f"Description must be between 0 and 200 characters, got {len(description)}")

    # Validate priority if provided
    if priority is not None and not isinstance(priority, Priority):
        raise ValueError(f"Priority must be a Priority enum, got {type(priority)}")

    # Validate tags if provided
    if tags is not None:
        if not isinstance(tags, list):
            raise ValueError(f"Tags must be a list, got {type(tags)}")

        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError(f"Each tag must be a string, got {type(tag)} in tags list")
            if len(tag) == 0:
                raise ValueError("Tags cannot be empty strings")
            if len(tag) > 50:  # Reasonable limit for tag length
                raise ValueError(f"Tag '{tag}' is too long (max 50 chars)")