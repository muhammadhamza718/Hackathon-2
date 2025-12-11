from typing import Tuple
from src.models.task import validate_task_data


class TaskValidator:
    """
    Validator for task-related inputs.
    Provides validation functions for task data.
    """

    @staticmethod
    def validate_task_title(title: str) -> Tuple[bool, str]:
        """
        Validate a task title.

        Args:
            title: The title to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            validate_task_data(title)
            return True, ""
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def validate_task_description(description: str) -> Tuple[bool, str]:
        """
        Validate a task description.

        Args:
            description: The description to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate with an empty title since we're only checking description
            validate_task_data("temp", description)
            return True, ""
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def validate_task_data(title: str, description: str = "") -> Tuple[bool, str]:
        """
        Validate both title and description.

        Args:
            title: The title to validate
            description: The description to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            validate_task_data(title, description)
            return True, ""
        except ValueError as e:
            return False, str(e)

    @staticmethod
    def validate_task_id(task_id: int) -> Tuple[bool, str]:
        """
        Validate a task ID.

        Args:
            task_id: The ID to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(task_id, int):
            return False, "Task ID must be an integer"

        if task_id < 1:
            return False, "Task ID must be a positive integer"

        return True, ""