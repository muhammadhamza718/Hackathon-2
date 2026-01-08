from typing import List, Optional
from src.models.task import Task, validate_task_data
from src.models.priority import Priority
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

    def add_task(self, title: str, description: str = "", priority: Optional[Priority] = None, tags: Optional[List[str]] = None) -> Task:
        """
        Add a new task with the given title, description, priority, and tags.

        Args:
            title: The task title (required, max 50 chars)
            description: The task description (optional, max 200 chars)
            priority: The task priority (optional, defaults to MEDIUM)
            tags: List of tags for the task (optional)

        Returns:
            The newly created task

        Raises:
            ValueError: If validation fails
        """
        # Use default priority if not provided
        if priority is None:
            priority = Priority.MEDIUM

        # Use empty list if tags not provided
        if tags is None:
            tags = []

        # Validate the input data
        validate_task_data(title, description, priority, tags)

        # Create a new task with the next available ID
        next_id = self.storage.get_next_available_id()
        task = Task(
            id=next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            completed=False
        )

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
                    description: Optional[str] = None, completed: Optional[bool] = None,
                    priority: Optional[Priority] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Update a task by its ID.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided)
            description: New description (if provided)
            completed: New completion status (if provided)
            priority: New priority (if provided)
            tags: New tags (if provided)

        Returns:
            True if the task was updated, False if not found
        """
        updates = {}
        if title is not None:
            # Get the current task to preserve other fields if not updating
            current_task = self.storage.get_task_by_id(task_id)
            if current_task:
                validate_task_data(title, current_task.description, current_task.priority, current_task.tags)
            else:
                validate_task_data(title, description or "")
            updates['title'] = title
        if description is not None:
            # Get the current task to preserve other fields
            current_task = self.storage.get_task_by_id(task_id)
            if current_task:
                validate_task_data(current_task.title, description, current_task.priority, current_task.tags)
            else:
                validate_task_data(title or "", description)
            updates['description'] = description
        if completed is not None:
            updates['completed'] = completed
        if priority is not None:
            # Validate the priority value
            if not isinstance(priority, Priority):
                raise ValueError(f"Priority must be a Priority enum, got {type(priority)}")
            updates['priority'] = priority
        if tags is not None:
            # Get the current task to preserve other fields
            current_task = self.storage.get_task_by_id(task_id)
            if current_task:
                validate_task_data(current_task.title, current_task.description, priority, tags)
            else:
                validate_task_data(title or "", description or "", priority, tags)
            updates['tags'] = tags

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

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title and description.

        Args:
            query: The search query string

        Returns:
            List of tasks that match the search query
        """
        if not query:
            return self.get_all_tasks()

        query_lower = query.lower()
        matching_tasks = []

        for task in self.storage.get_all_tasks():
            # Check if query matches in title or description (case-insensitive)
            if (query_lower in task.title.lower() or
                query_lower in task.description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[Priority] = None, tags: Optional[List[str]] = None) -> List[Task]:
        """
        Filter tasks by status, priority, and/or tags.

        Args:
            status: Filter by status ("All", "Pending", "Completed") - defaults to "All"
            priority: Filter by priority enum
            tags: Filter by list of tags (task must have at least one of these tags)

        Returns:
            List of tasks that match the filter criteria
        """
        tasks = self.storage.get_all_tasks()

        # Apply status filter
        if status and status.lower() != "all":
            if status.lower() == "pending":
                tasks = [task for task in tasks if not task.completed]
            elif status.lower() == "completed":
                tasks = [task for task in tasks if task.completed]

        # Apply priority filter
        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]

        # Apply tags filter
        if tags:
            # Filter tasks that have at least one of the specified tags
            tasks = [task for task in tasks if any(tag in task.tags for tag in tags)]

        return tasks