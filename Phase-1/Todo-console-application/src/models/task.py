from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with the following attributes:
    - id: auto-generated sequential unique identifier for the task (starting from 1)
    - title: required text string describing the task (max 50 characters)
    - description: optional text string with additional details (max 200 characters)
    - completed: boolean value indicating completion status
    - created_at: timestamp when the task was created
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
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


def validate_task_data(title: str, description: str = "") -> None:
    """
    Validate task data without creating a Task instance.

    Args:
        title: Task title (required, 1-50 characters)
        description: Task description (optional, 0-200 characters)

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