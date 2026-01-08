from typing import Optional
import rich.repr
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Checkbox, Static
from src.models.task import Task


@rich.repr.auto
class EditTaskModal(ModalScreen):
    """A modal dialog for editing existing tasks."""

    def __init__(self, task_service, task: Task) -> None:
        super().__init__()
        self.task_service = task_service
        self.todo_task = task
        self.title_input = Input(value=task.title, placeholder="Task title (max 50 chars)", id="title")
        self.description_input = Input(value=task.description, placeholder="Task description (optional, max 200 chars)", id="description")

    def compose(self) -> ComposeResult:
        """Create the modal dialog."""
        with Container(id="edit-task-modal"):
            yield Static("Edit Task", classes="title")
            with Vertical():
                yield Label("Title:", id="title-label")
                yield self.title_input
                yield Label("Description:", id="description-label")
                yield self.description_input
                with Horizontal(id="buttons"):
                    yield Button("Update Task", variant="primary", id="update")
                    yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        """Called when the modal is mounted."""
        self.title_input.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "update":
            self.update_task()
        elif event.button.id == "cancel":
            self.dismiss(None)

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        if event.key == "escape":
            self.dismiss(None)
        elif event.key == "enter":
            # Only process enter if we're not in a multi-line input
            if self.title_input.has_focus or self.description_input.has_focus:
                # Focus on the update button instead of submitting directly
                self.query_one("#update", Button).focus()
            else:
                self.update_task()

    def update_task(self) -> None:
        """Update the task using the input values."""
        title = self.title_input.value.strip()
        description = self.description_input.value.strip()

        # Validate title (required, max 50 chars)
        if not title:
            self.notify("Title is required", severity="error", timeout=3)
            self.title_input.focus()
            return

        if len(title) > 50:
            self.notify("Title must be 50 characters or less", severity="error", timeout=3)
            self.title_input.focus()
            return

        # Validate description (max 200 chars)
        if len(description) > 200:
            self.notify("Description must be 200 characters or less", severity="error", timeout=3)
            self.description_input.focus()
            return

        try:
            # Update the task via the service
            success = self.task_service.update_task(
                task_id=self.todo_task.id,
                title=title,
                description=description
            )
            if success:
                # Get the updated task to return
                updated_task = self.task_service.get_task_by_id(self.todo_task.id)
                # Return the updated task to the parent screen
                self.dismiss(updated_task)
            else:
                self.notify("Failed to update task", severity="error", timeout=3)
        except ValueError as e:
            self.notify(str(e), severity="error", timeout=5)