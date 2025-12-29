from typing import Optional
from src.services.task_service import TaskService
from src.ui.display_formatters import DisplayFormatter
from src.ui.task_prompts import TaskPrompts


class MenuSystem:
    """
    Menu system for the todo console application.
    Handles user navigation and routing to appropriate functions.
    """
    def __init__(self, task_service: TaskService):
        """
        Initialize the menu system with a task service.

        Args:
            task_service: The task service to use for operations
        """
        self.task_service = task_service

    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*50)
        print("TODO CONSOLE APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Completion")
        print("6. Exit")
        print("="*50)

    def handle_add_task(self):
        """Handle the add task menu option"""
        print("\n--- Add New Task ---")
        result = TaskPrompts.prompt_for_task_details()

        if result is None:  # User canceled
            print("Task creation canceled.")
            return

        title, description = result

        try:
            task = self.task_service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def handle_view_tasks(self):
        """Handle the view tasks menu option"""
        print("\n--- View All Tasks ---")
        tasks = self.task_service.get_tasks_sorted_by_id()

        if not tasks:
            print("No tasks found.")
            return

        formatted_tasks = DisplayFormatter.format_task_table(tasks)
        print(formatted_tasks)

    def handle_update_task(self):
        """Handle the update task menu option"""
        print("\n--- Update Task ---")
        tasks = self.task_service.get_tasks_sorted_by_id()

        if not tasks:
            print("No tasks found to update.")
            return

        # Show current tasks
        print("Current tasks:")
        print(DisplayFormatter.format_task_table(tasks))

        # Get task ID to update
        task_ids = [task.id for task in tasks]
        task_id = TaskPrompts.prompt_for_task_id(task_ids)

        if task_id is None:  # User canceled
            print("Task update canceled.")
            return

        # Get updates from user
        updates = TaskPrompts.prompt_for_task_update()

        if not updates:  # No updates provided or error
            print("No updates made.")
            return

        # Apply updates
        success = self.task_service.update_task(task_id, **updates)

        if success:
            print(f"Task {task_id} updated successfully!")
        else:
            print(f"Failed to update task {task_id}.")

    def handle_delete_task(self):
        """Handle the delete task menu option"""
        print("\n--- Delete Task ---")
        tasks = self.task_service.get_tasks_sorted_by_id()

        if not tasks:
            print("No tasks found to delete.")
            return

        # Show current tasks
        print("Current tasks:")
        print(DisplayFormatter.format_task_table(tasks))

        # Get task ID to delete
        task_ids = [task.id for task in tasks]
        task_id = TaskPrompts.prompt_for_task_id(task_ids)

        if task_id is None:  # User canceled
            print("Task deletion canceled.")
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()

        if confirm in ['y', 'yes']:
            success = self.task_service.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully!")
            else:
                print(f"Failed to delete task {task_id}.")
        else:
            print("Task deletion canceled.")

    def handle_toggle_task_completion(self):
        """Handle the toggle task completion menu option"""
        print("\n--- Toggle Task Completion ---")
        tasks = self.task_service.get_tasks_sorted_by_id()

        if not tasks:
            print("No tasks found to toggle.")
            return

        # Show current tasks
        print("Current tasks:")
        print(DisplayFormatter.format_task_table(tasks))

        # Get task ID to toggle
        task_ids = [task.id for task in tasks]
        task_id = TaskPrompts.prompt_for_task_id(task_ids)

        if task_id is None:  # User canceled
            print("Task toggle canceled.")
            return

        # Toggle completion
        success = self.task_service.toggle_task_completion(task_id)

        if success:
            task = self.task_service.get_task_by_id(task_id)
            status = "completed" if task.completed else "pending"
            print(f"Task {task_id} marked as {status}!")
        else:
            print(f"Failed to toggle task {task_id}.")

    def run(self):
        """Run the main menu loop"""
        print("Welcome to the Todo Console Application!")
        print("Use the menu below to manage your tasks.")

        while True:
            self.display_menu()

            try:
                choice = input("Select an option (1-6): ").strip()

                if choice == '1':
                    self.handle_add_task()
                elif choice == '2':
                    self.handle_view_tasks()
                elif choice == '3':
                    self.handle_update_task()
                elif choice == '4':
                    self.handle_delete_task()
                elif choice == '5':
                    self.handle_toggle_task_completion()
                elif choice == '6' or choice.lower() in ['exit', 'quit']:
                    print("Thank you for using the Todo Console Application. Goodbye!")
                    break
                else:
                    print("Invalid option. Please select 1-6.")
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")