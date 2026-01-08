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

# Import Model and Service
from src.models.task import Task
# Priority element removed

# Import UI Components and Assets
from src.ui.components.add_task_modal import AddTaskModal
from src.ui.components.edit_task_modal import EditTaskModal
from src.ui.components.input_id_modal import InputIdModal
from src.ui.assets import create_gradient_todo_logo, HeaderWidget
from src.ui.theme import THEME_CSS


class TaskTable(DataTable):
    """A custom DataTable for displaying tasks with status indicators."""

    def __init__(self):
        super().__init__()
        self.cursor_type = "row"
        self.show_cursor = True

        # Phase 1 Basic Level: Status, ID, Title. No Priority/Tags/Dates.
        self.add_columns("ID", "Status", "Title")

    def update_tasks(self, tasks: List[Task]) -> None:
        """Update the table with the given tasks."""
        self.clear()

        for task in tasks:
            # Status styling
            if task.completed:
                status_text = "COMPLETE"
                status_class = "status-completed"
            else:
                status_text = "PENDING"
                status_class = "status-pending"
            
            # Simple bold ID and Title styling using theme colors
            self.add_row(
                Text(str(task.id), style="bold white"),
                Text.from_markup(f"[{status_class}]{status_text}[/]"),
                Text(task.title, style="bold white"),
                key=str(task.id)
            )


class PremiumTodoApp(App):
    """Premium Terminal User Interface for task management (Phase 1 Basic)."""

    BINDINGS = [
        Binding("a", "add_task", "Add Task"),
        Binding("d", "delete_task", "Delete Task"),
        Binding("c", "toggle_completion", "Toggle Complete"),
        Binding("u", "update_task", "Update Task"),
        Binding("q", "quit", "Quit"),
    ]

    CSS = THEME_CSS

    def __init__(self, task_service):
        super().__init__()
        self.task_service = task_service
        self.current_tasks = []

    def compose(self) -> ComposeResult:
        """Create the app's UI."""
        header = Header(show_clock=True)
        header.sub_title = "PHASE 1 - BASIC EDITION"
        yield header

        with Container(id="main-container"):
            # Sidebar "Command Panel"
            with Vertical(id="sidebar"):
                yield Static(create_gradient_todo_logo(), id="sidebar-logo")
                
                yield Static("QUICK ACTIONS", classes="section-title")
                
                # Removed Filters as they are Intermediate Level
                yield Label("Press 'A' to Add Task", classes="help-text")
                yield Label("Press 'D' to Delete", classes="help-text")
                yield Label("Press 'C' to Complete", classes="help-text")
                yield Label("Press 'U' to Update", classes="help-text")
                

                yield Static("SYSTEM METRICS", classes="section-title")
                yield Static(id="stats")

            # Main Content Area
            with Vertical(id="main-content"):
                
                # Removed Search Bar (Intermediate Level)

                # Data Grid
                with VerticalScroll(id="task-table-container"):
                    self.task_table = TaskTable()
                    yield self.task_table

                # Status/Action Bar
                with Horizontal(id="status-bar"):
                    yield Static("► READY - AWAITING COMMAND ACQUISITION", id="status-message")

        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.load_tasks()
        self.update_stats()

    def load_tasks(self) -> None:
        """Load tasks from the service and update the display."""
        # Just simple get_all_tasks - basic View List requirement
        self.current_tasks = self.task_service.get_all_tasks()
        self.task_table.update_tasks(self.current_tasks)

    def update_stats(self) -> None:
        """Update statistics."""
        all_tasks = self.task_service.get_all_tasks()
        total = len(all_tasks)
        completed = len([t for t in all_tasks if t.completed])
        pending = total - completed

        stats_widget = self.query_one("#stats", Static)
        stats_widget.update(f"[bold cyan]TOTAL:[/]\t{total}\n[bold green]DONE:[/]\t{completed}\n[bold yellow]PEND:[/]\t{pending}")

    def action_add_task(self) -> None:
        def handle_task_creation(task):
            if task:
                self.load_tasks()
                self.update_stats()
                self.notify(f"Task '{task.title}' initialized.")
        self.app.push_screen(AddTaskModal(self.task_service), callback=handle_task_creation)

    def action_delete_task(self) -> None:
        def handle_delete(task_id):
            if task_id:
                if self.task_service.delete_task(task_id):
                    self.load_tasks()
                    self.update_stats()
                    self.notify(f"Task {task_id} neutralized.")
                else:
                    self.notify(f"Task {task_id} not found.", severity="error")
        
        self.app.push_screen(InputIdModal("Delete Task", "Delete"), callback=handle_delete)

    def action_toggle_completion(self) -> None:
        def handle_toggle(task_id):
            if task_id:
                if self.task_service.toggle_task_completion(task_id):
                    self.load_tasks()
                    self.update_stats()
                    self.notify(f"Task {task_id} status updated.")
                else:
                    self.notify(f"Task {task_id} not found.", severity="error")

        self.app.push_screen(InputIdModal("Toggle Status", "Toggle"), callback=handle_toggle)

    def action_update_task(self) -> None:
        def handle_id_input(task_id):
            if not task_id: return
            
            task = self.task_service.get_task_by_id(task_id)
            if task:
                def handle_update(updated):
                    if updated:
                        self.load_tasks()
                        self.update_stats()
                        self.notify("Task reconfigured.")
                self.app.push_screen(EditTaskModal(self.task_service, task), callback=handle_update)
            else:
                self.notify(f"Task {task_id} not found.", severity="error")

        self.app.push_screen(InputIdModal("Update Task", "Edit"), callback=handle_id_input)