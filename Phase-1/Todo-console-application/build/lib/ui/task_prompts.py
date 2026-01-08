from typing import Optional
from src.validators.task_validator import TaskValidator


class TaskPrompts:
    """
    User interface prompts for task-related operations.
    Handles user input collection and validation.
    """

    @staticmethod
    def prompt_for_task_title() -> Optional[str]:
        """
        Prompt the user for a task title.

        Returns:
            The title if valid, None if user cancels
        """
        while True:
            title = input("Enter task title (1-50 characters, 'cancel' to abort): ").strip()

            if title.lower() == 'cancel':
                return None

            is_valid, error_msg = TaskValidator.validate_task_title(title)
            if is_valid:
                return title
            else:
                print(f"Error: {error_msg}")
                print("Please try again.")

    @staticmethod
    def prompt_for_task_description() -> str:
        """
        Prompt the user for a task description.

        Returns:
            The description (can be empty)
        """
        while True:
            description = input("Enter task description (optional, max 200 characters, 'skip' to leave empty): ").strip()

            if description.lower() == 'skip':
                description = ""

            is_valid, error_msg = TaskValidator.validate_task_description(description)
            if is_valid:
                return description
            else:
                print(f"Error: {error_msg}")
                print("Please try again.")

    @staticmethod
    def prompt_for_task_details() -> Optional[tuple]:
        """
        Prompt the user for both title and description.

        Returns:
            Tuple of (title, description) if valid, None if user cancels
        """
        print("\nAdding a new task:")
        title = TaskPrompts.prompt_for_task_title()

        if title is None:  # User canceled
            return None

        description = TaskPrompts.prompt_for_task_description()
        return title, description

    @staticmethod
    def prompt_for_task_id(task_ids: list = None) -> Optional[int]:
        """
        Prompt the user for a task ID.

        Args:
            task_ids: Optional list of valid task IDs to validate against

        Returns:
            The ID if valid, None if user cancels
        """
        while True:
            id_input = input("Enter task ID ('cancel' to abort): ").strip()

            if id_input.lower() == 'cancel':
                return None

            try:
                task_id = int(id_input)
            except ValueError:
                print("Error: Task ID must be a number")
                continue

            is_valid, error_msg = TaskValidator.validate_task_id(task_id)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            if task_ids is not None and task_id not in task_ids:
                print(f"Error: Task ID {task_id} does not exist")
                continue

            return task_id

    @staticmethod
    def prompt_for_task_update() -> dict:
        """
        Prompt the user for task update details.

        Returns:
            Dictionary with fields to update (title, description)
        """
        updates = {}

        title_input = input("Enter new title (leave empty to keep current, 'cancel' to abort): ").strip()
        if title_input.lower() == 'cancel':
            return {}
        elif title_input:  # Only update if not empty
            is_valid, error_msg = TaskValidator.validate_task_title(title_input)
            if is_valid:
                updates['title'] = title_input
            else:
                print(f"Error: {error_msg}")
                return {}

        description_input = input("Enter new description (leave empty to keep current, 'skip' to clear): ").strip()
        if description_input.lower() == 'skip':
            updates['description'] = ""
        elif description_input:  # Only update if not empty
            is_valid, error_msg = TaskValidator.validate_task_description(description_input)
            if is_valid:
                updates['description'] = description_input
            else:
                print(f"Error: {error_msg}")
                return {}

        return updates