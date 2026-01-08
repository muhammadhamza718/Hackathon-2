from typing import List, Optional
import rich.repr
from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static, Input, Button, Label
from textual.binding import Binding
from textual.message import Message
from src.models.task import Task
from src.models.priority import Priority
from src.ui.components.add_task_modal import AddTaskModal
from src.ui.components.edit_task_modal import EditTaskModal


class TaskTable(DataTable):
    """A custom DataTable for displaying tasks with priority indicators."""

    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.show_cursor = True

        # Add columns for the task table
        self.add_columns("ID", "Title", "Description", "Priority", "Status", "Tags")

    def update_tasks(self, tasks: List[Task]) -> None:
        """Update the table with the given tasks."""
        # Clear existing rows
        self.clear()

        # Add each task as a row
        for task in tasks:
            # Format priority with visual indicators
            priority_text = f"{task.priority.value}"
            if task.priority == Priority.HIGH:
                priority_text = f"[red]{priority_text}[/red] 🔴"
            elif task.priority == Priority.MEDIUM:
                priority_text = f"[yellow]{priority_text}[/yellow] 🟡"
            elif task.priority == Priority.LOW:
                priority_text = f"[green]{priority_text}[/green] 🟢"

            # Format status
            status_text = "✅ Completed" if task.completed else "⏳ Pending"

            # Format tags
            tags_text = ", ".join(task.tags) if task.tags else ""

            # Add the row
            self.add_row(
                str(task.id),
                task.title,
                task.description[:50] + "..." if len(task.description) > 50 else task.description,  # Truncate long descriptions
                priority_text,
                status_text,
                tags_text,
                key=str(task.id)
            )


class PremiumTodoApp(App):
    """Premium Terminal User Interface for task management."""

    # Define keyboard shortcuts
    BINDINGS = [
        Binding("a", "add_task", "Add Task"),
        Binding("d", "delete_task", "Delete Task"),
        Binding("c", "toggle_completion", "Toggle Complete"),
        Binding("u", "update_task", "Update Task"),
        Binding("q", "quit", "Quit"),
        Binding("f", "focus_filter", "Filter Sidebar"),
        Binding("/", "focus_search", "Search"),
    ]

    CSS = """
    Screen {
        layout: vertical;
    }

    #main-container {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 30%;
        height: 1fr;
        dock: left;
    }

    #main-content {
        width: 70%;
        height: 1fr;
        dock: right;
    }

    #task-table-container {
        height: 1fr;
    }

    #search-container {
        height: auto;
        dock: top;
        margin: 1 0;
    }

    #status-bar {
        height: auto;
        dock: bottom;
        margin: 1 0;
    }

    .priority-high {
        color: red;
    }

    .priority-medium {
        color: yellow;
    }

    .priority-low {
        color: green;
    }
    """

    def __init__(self, task_service):
        super().__init__()
        self.task_service = task_service
        self.current_tasks = []
        self.filtered_tasks = []
        self.search_query = ""
        self.status_filter = "All"  # All, Pending, Completed
        self.priority_filter = "All"  # All, Low, Medium, High
        self.tag_filter = "All"  # All, or specific tag

    def compose(self) -> ComposeResult:
        """Create the app's UI."""
        yield Header()
        with Container(id="main-container"):
            with Vertical(id="sidebar"):
                yield Static("Filters", classes="section-title")

                # Status filter
                yield Label("Status:", id="status-filter-label")
                with Horizontal(id="status-filter-controls"):
                    yield Button("All", id="status-all", variant="default")
                    yield Button("Pending", id="status-pending", variant="default")
                    yield Button("Completed", id="status-completed", variant="default")

                # Priority filter
                yield Label("Priority:", id="priority-filter-label")
                with Horizontal(id="priority-filter-controls"):
                    yield Button("All", id="priority-all", variant="default")
                    yield Button("Low", id="priority-low", variant="default")
                    yield Button("Medium", id="priority-medium", variant="default")
                    yield Button("High", id="priority-high", variant="default")

                # Tags filter
                yield Label("Tags:", id="tags-filter-label")
                yield Static("All [Click to select]", id="tags-filter-value")

                yield Static("Quick Stats", classes="section-title")
                yield Static(id="stats")

            with Vertical(id="main-content"):
                # Search bar
                with Horizontal(id="search-container"):
                    yield Input(placeholder="Search tasks...", id="search-input")
                    yield Button("Clear", id="clear-search")

                # Task table
                with VerticalScroll(id="task-table-container"):
                    self.task_table = TaskTable()
                    yield self.task_table

                # Status bar
                with Horizontal(id="status-bar"):
                    yield Static("Press 'A' to add a task", id="status-message")

        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.load_tasks()
        self.update_stats()

    def load_tasks(self) -> None:
        """Load tasks from the service and update the display."""
        if self.search_query:
            self.current_tasks = self.task_service.search_tasks(self.search_query)
        else:
            self.current_tasks = self.task_service.get_all_tasks()

        # Apply filters
        self.filtered_tasks = self.apply_filters(self.current_tasks)

        # Update the task table
        self.task_table.update_tasks(self.filtered_tasks)

    def apply_filters(self, tasks: List[Task]) -> List[Task]:
        """Apply current filters to the list of tasks."""
        filtered = tasks

        # Apply status filter
        if self.status_filter and self.status_filter != "All":
            if self.status_filter == "Pending":
                filtered = [task for task in filtered if not task.completed]
            elif self.status_filter == "Completed":
                filtered = [task for task in filtered if task.completed]

        # Apply priority filter
        if self.priority_filter and self.priority_filter != "All":
            priority_map = {
                "Low": Priority.LOW,
                "Medium": Priority.MEDIUM,
                "High": Priority.HIGH
            }
            if self.priority_filter in priority_map:
                priority_enum = priority_map[self.priority_filter]
                filtered = [task for task in filtered if task.priority == priority_enum]

        return filtered

    def update_stats(self) -> None:
        """Update the statistics display."""
        all_tasks = self.task_service.get_all_tasks()
        total = len(all_tasks)
        completed = len([task for task in all_tasks if task.completed])
        pending = total - completed

        stats_widget = self.query_one("#stats", Static)
        stats_widget.update(f"Total: {total}\nCompleted: {completed}\nPending: {pending}")

    def action_add_task(self) -> None:
        """Add a new task."""
        def handle_task_creation(task):
            if task:
                self.load_tasks()
                self.update_stats()
                self.notify(f"Task '{task.title}' added successfully!")

        self.app.push_screen(AddTaskModal(self.task_service), callback=handle_task_creation)

    def action_delete_task(self) -> None:
        """Delete the currently selected task."""
        if not self.task_table.is_valid_row_index(self.task_table.cursor_row):
            self.notify("No task selected", severity="warning")
            return

        selected_task_id = int(self.task_table.get_row_at(self.task_table.cursor_row)[0])
        task = self.task_service.get_task_by_id(selected_task_id)

        if task:
            success = self.task_service.delete_task(selected_task_id)
            if success:
                self.load_tasks()
                self.update_stats()
                self.notify(f"Task '{task.title}' deleted successfully!")
            else:
                self.notify("Failed to delete task", severity="error")

    def action_toggle_completion(self) -> None:
        """Toggle the completion status of the currently selected task."""
        if not self.task_table.is_valid_row_index(self.task_table.cursor_row):
            self.notify("No task selected", severity="warning")
            return

        selected_task_id = int(self.task_table.get_row_at(self.task_table.cursor_row)[0])
        task = self.task_service.get_task_by_id(selected_task_id)

        if task:
            success = self.task_service.toggle_task_completion(selected_task_id)
            if success:
                self.load_tasks()
                self.update_stats()
                status = "completed" if task.completed else "pending"
                self.notify(f"Task '{task.title}' marked as {status}!")
            else:
                self.notify("Failed to update task", severity="error")

    def action_update_task(self) -> None:
        """Update the currently selected task."""
        if not self.task_table.is_valid_row_index(self.task_table.cursor_row):
            self.notify("No task selected", severity="warning")
            return

        selected_task_id = int(self.task_table.get_row_at(self.task_table.cursor_row)[0])
        task = self.task_service.get_task_by_id(selected_task_id)

        if task:
            def handle_task_update(updated_task):
                if updated_task:
                    self.load_tasks()
                    self.update_stats()
                    self.notify(f"Task '{updated_task.title}' updated successfully!")

            self.app.push_screen(EditTaskModal(self.task_service, task), callback=handle_task_update)
        else:
            self.notify("Task not found", severity="error")

    def on_input_changed(self, message: Input.Changed) -> None:
        """Handle search input changes."""
        if message.input.id == "search-input":
            self.search_query = message.value
            self.load_tasks()

    def action_focus_filter(self) -> None:
        """Focus the filter sidebar."""
        # For now, just show a notification - in a full implementation, we would focus the sidebar
        self.notify("Filter sidebar would be focused", timeout=2)

    def action_focus_search(self) -> None:
        """Focus the search bar."""
        self.query_one("#search-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        # Handle search clear
        if event.button.id == "clear-search":
            self.query_one("#search-input", Input).value = ""
            self.search_query = ""
            self.load_tasks()

        # Handle status filters
        elif event.button.id == "status-all":
            self.status_filter = "All"
            self.load_tasks()
        elif event.button.id == "status-pending":
            self.status_filter = "Pending"
            self.load_tasks()
        elif event.button.id == "status-completed":
            self.status_filter = "Completed"
            self.load_tasks()

        # Handle priority filters
        elif event.button.id == "priority-all":
            self.priority_filter = "All"
            self.load_tasks()
        elif event.button.id == "priority-low":
            self.priority_filter = "Low"
            self.load_tasks()
        elif event.button.id == "priority-medium":
            self.priority_filter = "Medium"
            self.load_tasks()
        elif event.button.id == "priority-high":
            self.priority_filter = "High"
            self.load_tasks()