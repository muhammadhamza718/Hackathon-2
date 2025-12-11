#!/usr/bin/env python3
"""
Todo Console Application

A simple in-memory todo application that allows users to:
- Add new tasks
- View all tasks
- Update task details
- Delete tasks
- Mark tasks as complete/incomplete
"""

from src.ui.menu_system import MenuSystem
from src.services.task_service import TaskService
from src.storage.task_storage import TaskStorage


def main():
    """Main entry point for the application"""
    # Initialize the application components
    storage = TaskStorage()
    task_service = TaskService(storage)
    menu_system = MenuSystem(task_service)

    # Run the menu system
    menu_system.run()


if __name__ == "__main__":
    main()