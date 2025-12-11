from typing import List, Optional
from src.models.task import Task, validate_task_data
from src.storage.task_storage import TaskStorage


class TaskService:
    """
    Service layer for task operations.
    Handles business logic for task management.
    """
    def __init__(self, storage: TaskStorage):
        """
        Initialize the task service with a storage instance.

        Args:
            storage: The task storage to use
        """
        self.storage = storage

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and description.

        Args:
            title: The task title (required, max 50 chars)
            description: The task description (optional, max 200 chars)

        Returns:
            The newly created task

        Raises:
            ValueError: If title or description validation fails
        """
        # Validate the input data
        validate_task_data(title, description)

        # Create a new task with the next available ID
        next_id = self.storage.get_next_available_id()
        task = Task(id=next_id, title=title, description=description, completed=False)

        # Add the task to storage
        return self.storage.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self.storage.get_all_tasks()

    def get_tasks_sorted_by_id(self) -> List[Task]:
        """
        Get all tasks sorted by ID.

        Returns:
            List of all tasks sorted by ID
        """
        tasks = self.storage.get_all_tasks()
        return sorted(tasks, key=lambda task: task.id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self.storage.get_task_by_id(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """
        Update a task by its ID.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided)
            description: New description (if provided)
            completed: New completion status (if provided)

        Returns:
            True if the task was updated, False if not found
        """
        updates = {}
        if title is not None:
            validate_task_data(title, description or "")
            updates['title'] = title
        if description is not None:
            # Get the current task to preserve the title if not updating
            current_task = self.storage.get_task_by_id(task_id)
            if current_task:
                validate_task_data(current_task.title, description)
            updates['description'] = description
        if completed is not None:
            updates['completed'] = completed

        return self.storage.update_task(task_id, **updates)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        return self.storage.delete_task(task_id)

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if not found
        """
        task = self.storage.get_task_by_id(task_id)
        if task is None:
            return False

        # Update the completion status
        return self.storage.update_task(task_id, completed=not task.completed)