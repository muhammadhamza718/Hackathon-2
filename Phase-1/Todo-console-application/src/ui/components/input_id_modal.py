from typing import Optional
import rich.repr
from textual import events
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

@rich.repr.auto
class InputIdModal(ModalScreen):
    """A modal dialog for inputting a Task ID."""

    def __init__(self, title: str, action_label: str) -> None:
        super().__init__()
        self.modal_title = title
        self.action_label = action_label
        self.id_input = Input(placeholder="Enter Task ID", id="id-input", type="integer")

    def compose(self) -> ComposeResult:
        """Create the modal dialog."""
        with Container(id="input-id-modal", classes="modal-container"):
            yield Static(self.modal_title, classes="title")
            with Vertical():
                yield Label("Task ID:", id="id-label")
                yield self.id_input
                with Horizontal(id="buttons"):
                    yield Button(self.action_label, variant="primary", id="submit")
                    yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        """Called when the modal is mounted."""
        self.id_input.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "submit":
            self.submit_id()
        elif event.button.id == "cancel":
            self.dismiss(None)

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        if event.key == "escape":
            self.dismiss(None)
        elif event.key == "enter":
            self.submit_id()

    def submit_id(self) -> None:
        """Submit the input ID."""
        value = self.id_input.value.strip()
        if not value:
            self.notify("ID is required", severity="error", timeout=3)
            return
            
        try:
            task_id = int(value)
            if task_id < 1:
                self.notify("ID must be positive", severity="error", timeout=3)
                return
            self.dismiss(task_id)
        except ValueError:
            self.notify("ID must be a number", severity="error", timeout=3)
