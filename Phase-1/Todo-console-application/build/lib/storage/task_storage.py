from typing import List, Optional
from src.models.task import Task


class TaskStorage:
    """
    In-memory storage for tasks using a simple list.
    This storage maintains tasks during the application runtime only.
    """
    def __init__(self):
        """Initialize an empty task list"""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, task: Task) -> Task:
        """
        Add a task to the storage.

        Args:
            task: The task to add

        Returns:
            The added task with assigned ID
        """
        # If the task ID is 0 or negative, assign the next available ID
        if task.id <= 0:
            task.id = self._next_id
            self._next_id += 1
        elif task.id >= self._next_id:
            # If a task is added with a higher ID, update the next ID
            self._next_id = task.id + 1

        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks from storage.

        Returns:
            List of all tasks
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, **updates) -> bool:
        """
        Update a task by its ID.

        Args:
            task_id: The ID of the task to update
            **updates: Fields to update (title, description, completed)

        Returns:
            True if the task was updated, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Update the allowed fields
        if 'title' in updates:
            task.title = updates['title']
        if 'description' in updates:
            task.description = updates['description']
        if 'completed' in updates:
            task.completed = updates['completed']

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def get_next_available_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            The next available ID
        """
        return self._next_id

    def clear_all(self) -> None:
        """Clear all tasks from storage"""
        self._tasks.clear()
        self._next_id = 1

    def count(self) -> int:
        """
        Get the number of tasks in storage.

        Returns:
            The number of tasks
        """
        return len(self._tasks)