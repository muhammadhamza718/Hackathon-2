from typing import List
from src.models.task import Task


class DisplayFormatter:
    """
    Formatter for displaying tasks in various formats.
    Provides methods to format tasks for console output.
    """

    @staticmethod
    def format_task_table(tasks: List[Task]) -> str:
        """
        Format tasks in a table format with ID, Status, Title, and Description columns.

        Args:
            tasks: List of tasks to format

        Returns:
            Formatted table as a string
        """
        if not tasks:
            return "No tasks found."

        # Define column widths
        id_width = max(5, len("ID"))  # At least 5 characters for ID column
        status_width = 10  # Status column (e.g., "Complete", "Pending")
        title_width = min(30, max(15, len("TITLE")))  # Title column
        desc_width = min(40, max(20, len("DESCRIPTION")))  # Description column

        # Calculate actual max widths based on content
        for task in tasks:
            id_width = max(id_width, len(str(task.id)))
            title_width = max(title_width, len(task.title))
            desc_width = max(desc_width, len(task.description))

        # Limit maximum width for better readability
        title_width = min(title_width, 50)
        desc_width = min(desc_width, 70)

        # Create header
        header = (
            f"{'ID':<{id_width}} | "
            f"{'STATUS':<{status_width}} | "
            f"{'TITLE':<{title_width}} | "
            f"{'DESCRIPTION':<{desc_width}}"
        )
        separator = (
            f"{'-' * id_width}-+-"
            f"{'-' * status_width}-+-"
            f"{'-' * title_width}-+-"
            f"{'-' * desc_width}"
        )

        # Create rows
        rows = [header, separator]
        for task in tasks:
            status = "Complete" if task.completed else "Pending"
            # Truncate title and description if too long
            title = task.title if len(task.title) <= title_width else task.title[:title_width-3] + "..."
            desc = task.description if len(task.description) <= desc_width else task.description[:desc_width-3] + "..."

            row = (
                f"{task.id!s:>{id_width}} | "
                f"{status:<{status_width}} | "
                f"{title:<{title_width}} | "
                f"{desc:<{desc_width}}"
            )
            rows.append(row)

        return "\n".join(rows)

    @staticmethod
    def format_single_task(task: Task) -> str:
        """
        Format a single task for display.

        Args:
            task: The task to format

        Returns:
            Formatted task as a string
        """
        status = "Complete" if task.completed else "Pending"
        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")

        return (
            f"ID: {task.id}\n"
            f"Title: {task.title}\n"
            f"Description: {task.description}\n"
            f"Status: {status}\n"
            f"Created: {created_str}"
        )

    @staticmethod
    def format_task_list(tasks: List[Task]) -> str:
        """
        Format tasks as a simple list.

        Args:
            tasks: List of tasks to format

        Returns:
            Formatted list as a string
        """
        if not tasks:
            return "No tasks found."

        lines = []
        for task in tasks:
            status = "✓" if task.completed else "○"
            lines.append(f"{status} [{task.id}] {task.title}")

        return "\n".join(lines)

    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """
        Truncate text to a maximum length.

        Args:
            text: The text to truncate
            max_length: The maximum length

        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."