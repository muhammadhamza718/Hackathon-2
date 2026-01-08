#!/usr/bin/env python3
"""
Premium Todo TUI Application

A premium Terminal User Interface for task management with Textual and Rich.
Supports both the legacy CLI menu and the new TUI interface.
"""

import sys
from typing import Optional

try:
    from textual.app import App
except ImportError:
    # Textual not available, only use CLI
    TextualApp = None
else:
    TextualApp = App

from src.ui.menu_system import MenuSystem
from src.services.task_service import TaskService
from src.storage.task_storage import TaskStorage


def main(tui: bool = True):
    """Main entry point for the application"""
    # Initialize the application components
    storage = TaskStorage()
    task_service = TaskService(storage)

    if tui and TextualApp is not None:
        # Try to run the TUI if requested and available
        try:
            from src.ui.premium_todo_app import PremiumTodoApp
            app = PremiumTodoApp(task_service)
            app.run()
        except ImportError as e:
            # Fallback to CLI if TUI is not implemented yet
            print(f"TUI not available: {e}")
            menu_system = MenuSystem(task_service)
            menu_system.run()
    else:
        # Run the legacy CLI menu system
        menu_system = MenuSystem(task_service)
        menu_system.run()


if __name__ == "__main__":
    # Check command line arguments
    use_tui = True
    for arg in sys.argv[1:]:
        if arg.lower() in ['--cli', '-c']:
            use_tui = False
        elif arg.lower() in ['--tui', '--premium', '-t']:
            use_tui = True

    main(tui=use_tui)