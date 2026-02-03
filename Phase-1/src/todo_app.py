"""
HydroToDo - Phase 1: In-Memory Curses TUI Application
Complete Implementation: Core Logic and Curses UI
"""

import json
import os
import curses
import signal
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Category(Enum):
    GENERAL = "GENERAL"
    WORK = "WORK"
    PERSONAL = "PERSONAL"


class Task:
    def __init__(self, id: int, title: str, description: str = "",
                 category: str = "GENERAL", completed: bool = False,
                 priority: str = "MEDIUM", created_at: datetime = None):
        """
        Represents a single todo item

        Args:
            id: Unique identifier (auto-generated)
            title: Required task title (max 50 chars)
            description: Optional task description (max 200 chars)
            category: Task category ("GENERAL", "WORK", "PERSONAL")
            completed: Completion status (default: False)
            priority: Task priority ("LOW", "MEDIUM", "HIGH")
            created_at: Creation timestamp (auto-generated if None)
        """
        self.id = id
        self.title = title
        self.description = description
        self.category = category if category in [cat.value for cat in Category] else Category.GENERAL.value
        self.completed = completed
        self.priority = priority if priority in [prio.value for prio in Priority] else Priority.MEDIUM.value
        self.created_at = created_at or datetime.now()

    def validate_title(self, title: str) -> bool:
        """Validate that title is between 1-50 characters"""
        return 1 <= len(title) <= 50

    def validate_description(self, description: str) -> bool:
        """Validate that description is between 0-200 characters"""
        return 0 <= len(description) <= 200

    def validate_category(self, category: str) -> bool:
        """Validate that category is one of the allowed values"""
        return category in [cat.value for cat in Category]

    def validate_priority(self, priority: str) -> bool:
        """Validate that priority is one of the allowed values"""
        return priority in [prio.value for prio in Priority]

    def to_dict(self) -> dict:
        """Convert Task object to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "completed": self.completed,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create Task object from dictionary representation"""
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            category=data.get('category', 'GENERAL'),
            completed=data.get('completed', False),
            priority=data.get('priority', 'MEDIUM'),
            created_at=created_at
        )


class TaskManager:
    def __init__(self, data_file: str = "todo_data.json"):
        """
        Manages all tasks in memory and handles persistence

        Args:
            data_file: Path to JSON file for data persistence
        """
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_from_file()

    def add_task(self, title: str, description: str = "",
                 category: str = "GENERAL", priority: str = "MEDIUM") -> Task:
        """
        Add a new task to the collection

        Args:
            title: Task title (max 50 chars)
            description: Task description (max 200 chars, optional)
            category: Task category ("GENERAL", "WORK", "PERSONAL")
            priority: Task priority ("LOW", "MEDIUM", "HIGH")

        Returns:
            Task: The newly created task object
        """
        # Validate inputs
        if not Task("", "").validate_title(title):
            raise ValueError(f"Title must be 1-50 characters, got {len(title)} characters")

        if not Task("", "").validate_description(description):
            raise ValueError(f"Description must be 0-200 characters, got {len(description)} characters")

        if not Task("", "").validate_category(category):
            raise ValueError(f"Category must be one of {', '.join([cat.value for cat in Category])}")

        if not Task("", "").validate_priority(priority):
            raise ValueError(f"Priority must be one of {', '.join([prio.value for prio in Priority])}")

        # Create new task with auto-generated ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            category=category,
            priority=priority
        )

        self.tasks.append(task)

        # Update next_id to be one more than the highest ID in the list
        self.next_id = max([t.id for t in self.tasks]) + 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None,
                   category: str = None, priority: str = None, completed: bool = None) -> Optional[Task]:
        """
        Update an existing task

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            category: New category (optional)
            priority: New priority (optional)
            completed: New completion status (optional)

        Returns:
            Task: The updated task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Validate and update fields if provided
        if title is not None:
            if not Task("", "").validate_title(title):
                raise ValueError(f"Title must be 1-50 characters, got {len(title)} characters")
            task.title = title

        if description is not None:
            if not Task("", "").validate_description(description):
                raise ValueError(f"Description must be 0-200 characters, got {len(description)} characters")
            task.description = description

        if category is not None:
            if not Task("", "").validate_category(category):
                raise ValueError(f"Category must be one of {', '.join([cat.value for cat in Category])}")
            task.category = category

        if priority is not None:
            if not Task("", "").validate_priority(priority):
                raise ValueError(f"Priority must be one of {', '.join([prio.value for prio in Priority])}")
            task.priority = priority

        if completed is not None:
            task.completed = completed

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Task: The updated task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks

        Returns:
            List[Task]: List of all tasks
        """
        return self.tasks.copy()

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """
        Get tasks filtered by category

        Args:
            category: The category to filter by

        Returns:
            List[Task]: List of tasks in the specified category
        """
        if not Task("", "").validate_category(category):
            raise ValueError(f"Category must be one of {', '.join([cat.value for cat in Category])}")

        return [task for task in self.tasks if task.category == category]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description

        Args:
            query: The search query string

        Returns:
            List[Task]: List of tasks that match the query
        """
        if not query:
            return self.get_all_tasks()

        query_lower = query.lower()
        matching_tasks = []

        for task in self.tasks:
            if (query_lower in task.title.lower() or
                query_lower in task.description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, completed: bool = None,
                     priority: str = None, category: str = None) -> List[Task]:
        """
        Filter tasks by various criteria

        Args:
            completed: Filter by completion status (optional)
            priority: Filter by priority (optional)
            category: Filter by category (optional)

        Returns:
            List[Task]: List of tasks that match all specified criteria
        """
        filtered_tasks = self.tasks[:]

        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == completed]

        if priority is not None:
            if not Task("", "").validate_priority(priority):
                raise ValueError(f"Priority must be one of {', '.join([prio.value for prio in Priority])}")
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        if category is not None:
            if not Task("", "").validate_category(category):
                raise ValueError(f"Category must be one of {', '.join([cat.value for cat in Category])}")
            filtered_tasks = [task for task in filtered_tasks if task.category == category]

        return filtered_tasks

    def save_to_file(self) -> None:
        """Save all tasks to the JSON file"""
        try:
            # Create data structure to save
            data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "tasks": [task.to_dict() for task in self.tasks]
            }

            # Write to file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save tasks to {self.data_file}: {str(e)}")

    def load_from_file(self) -> None:
        """Load tasks from the JSON file"""
        if not os.path.exists(self.data_file):
            # Initialize with empty list if file doesn't exist
            self.tasks = []
            self.next_id = 1
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Load tasks from the data
            self.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]

            # Set next_id to be one more than the highest ID in the list
            if self.tasks:
                self.next_id = max([task.id for task in self.tasks]) + 1
            else:
                self.next_id = 1

        except (IOError, json.JSONDecodeError, KeyError) as e:
            # If there's an error loading, start with empty list
            print(f"Warning: Could not load tasks from {self.data_file}: {str(e)}. Starting with empty task list.")
            self.tasks = []
            self.next_id = 1

    def backup_data(self) -> None:
        """Create a backup of the current data file"""
        if os.path.exists(self.data_file):
            backup_filename = f"{self.data_file}.backup"
            try:
                with open(self.data_file, 'r', encoding='utf-8') as src:
                    data = src.read()

                with open(backup_filename, 'w', encoding='utf-8') as dst:
                    dst.write(data)
            except IOError as e:
                raise IOError(f"Failed to create backup {backup_filename}: {str(e)}")


class BaseUI:
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Base class for all UI components

        Args:
            stdscr: Main curses screen object
            height, width: Dimensions of the component
            start_y, start_x: Position coordinates
        """
        self.stdscr = stdscr
        self.height = height
        self.width = width
        self.start_y = start_y
        self.start_x = start_x

        # Create a new window for this component
        self.win = curses.newwin(height, width, start_y, start_x)

    def render(self) -> None:
        """Render the component - to be overridden by subclasses"""
        pass

    def handle_input(self, key) -> str:
        """Handle input for the component - to be overridden by subclasses"""
        return ""

    def resize(self, height: int, width: int, start_y: int, start_x: int) -> None:
        """Resize the component"""
        self.height = height
        self.width = width
        self.start_y = start_y
        self.start_x = start_x
        self.win.resize(height, width)
        self.win.mvwin(start_y, start_x)


class Header(BaseUI):
    def __init__(self, stdscr, width: int, start_y: int = 0, start_x: int = 0):
        """
        Renders the ASCII art header with "HYDROTODO" title
        """
        super().__init__(stdscr, 3, width, start_y, start_x)

    def render(self) -> None:
        """Render the header with ASCII art title"""
        self.win.clear()

        # Draw the header box
        for x in range(self.width):
            self.win.addch(0, x, ord('-'))
            self.win.addch(2, x, ord('-'))

        for y in range(3):
            self.win.addch(y, 0, ord('|'))
            if self.width > 1:
                self.win.addch(y, self.width - 1, ord('|'))

        # Draw the ASCII art title
        title = "HYDROTODO"
        title_x = (self.width - len(title)) // 2
        self.win.addstr(1, title_x, title, curses.A_BOLD | curses.color_pair(1))  # HEADER color

        self.win.refresh()


class Navigation(BaseUI):
    def __init__(self, stdscr, width: int, start_y: int, start_x: int):
        """
        Renders category tabs and search bar

        Attributes:
            active_tab: Current selected tab ("GENERAL", "WORK", "PERSONAL")
            search_query: Current search input
        """
        super().__init__(stdscr, 3, width, start_y, start_x)
        self.active_tab = "GENERAL"
        self.search_query = ""
        self.tabs = ["GENERAL", "WORK", "PERSONAL"]

    def render(self) -> None:
        """Render the navigation bar with tabs and search bar"""
        self.win.clear()

        # Calculate positions for tabs and search bar
        tab_width = 12  # Width for each tab
        total_tabs_width = len(self.tabs) * tab_width
        spacing = (self.width - total_tabs_width - 20) // (len(self.tabs) + 1)  # Account for search bar

        # Draw tabs
        current_x = spacing
        for i, tab in enumerate(self.tabs):
            if tab == self.active_tab:
                # Active tab: blue background
                self.win.addstr(1, current_x, f" {tab} ", curses.color_pair(2))  # NAV_ACTIVE
            else:
                # Inactive tab: white background
                self.win.addstr(1, current_x, f" {tab} ", curses.color_pair(3))  # NAV_INACTIVE
            current_x += tab_width + spacing

        # Draw search bar
        search_label = "[SEARCH]"
        search_start = current_x
        self.win.addstr(1, search_start, search_label, curses.color_pair(3))  # NAV_INACTIVE

        # Show search query if there is one
        if self.search_query:
            self.win.addstr(1, search_start + 8, self.search_query, curses.color_pair(3))

        # Draw bottom border
        for x in range(self.width):
            self.win.addch(2, x, ord('-'))

        self.win.refresh()

    def handle_input(self, key) -> str:
        """Handle input for navigation - tabs and search"""
        if key == ord('/'):
            # Enter search mode
            return "FOCUS_SEARCH"
        elif key in [ord('h'), curses.KEY_LEFT]:
            # Switch to previous tab
            self.switch_tab(-1)
            return "TAB_CHANGED"
        elif key in [ord('l'), curses.KEY_RIGHT]:
            # Switch to next tab
            self.switch_tab(1)
            return "TAB_CHANGED"
        else:
            # Handle search input if it's a printable character
            if 32 <= key <= 126:  # Printable ASCII range
                self.search_query += chr(key)
                return "SEARCH_UPDATED"

        return ""

    def switch_tab(self, direction: int) -> None:
        """Switch between tabs (-1 for left, +1 for right)"""
        current_index = self.tabs.index(self.active_tab)
        new_index = (current_index + direction) % len(self.tabs)
        self.active_tab = self.tabs[new_index]


class TaskList(BaseUI):
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Renders scrollable list of tasks with checkboxes

        Attributes:
            tasks: List of tasks to display
            selected_idx: Index of currently selected task
            offset: Scroll offset for viewing tasks beyond viewport
        """
        super().__init__(stdscr, height, width, start_y, start_x)
        self.tasks = []
        self.selected_idx = 0
        self.offset = 0
        self.max_visible = height - 2  # Account for borders

    def set_tasks(self, tasks: List[Task]) -> None:
        """Set the tasks to display"""
        self.tasks = tasks
        # Reset selection if tasks list changed
        if self.selected_idx >= len(tasks) and len(tasks) > 0:
            self.selected_idx = len(tasks) - 1
        elif len(tasks) == 0:
            self.selected_idx = 0

    def render(self) -> None:
        """Render the task list with checkboxes and selection highlighting"""
        self.win.clear()

        # Draw borders
        for x in range(self.width):
            self.win.addch(0, x, ord('-'))
            if self.height > 1:
                self.win.addch(self.height - 1, x, ord('-'))

        for y in range(self.height):
            self.win.addch(y, 0, ord('|'))
            if self.width > 1:
                self.win.addch(y, self.width - 1, ord('|'))

        # Draw tasks
        visible_tasks = min(len(self.tasks), self.max_visible - 2)
        for i in range(visible_tasks):
            task_idx = i + self.offset
            if task_idx >= len(self.tasks):
                break

            task = self.tasks[task_idx]

            # Determine display row (account for top border)
            display_row = i + 1

            # Alternate row colors
            if i % 2 == 0:
                attr = curses.color_pair(4)  # TASK_NORMAL
            else:
                attr = curses.color_pair(5)  # TASK_ALTERNATE

            # Highlight selected task
            if task_idx == self.selected_idx:
                attr = curses.color_pair(6)  # SELECTION

            # Format task display
            checkbox = "[x]" if task.completed else "[ ]"
            task_text = f"{checkbox} {task.title}"

            # Truncate if too long
            max_text_length = self.width - 6  # Account for checkbox and padding
            if len(task_text) > max_text_length:
                task_text = task_text[:max_text_length-3] + "..."

            # Apply color for completed tasks
            if task.completed:
                attr = attr | curses.color_pair(7)  # TASK_COMPLETED

            self.win.addstr(display_row, 2, task_text, attr)

        self.win.refresh()

    def handle_input(self, key) -> str:
        """Handle input for task selection and navigation"""
        if key in [ord('j'), curses.KEY_DOWN]:
            if self.selected_idx < len(self.tasks) - 1:
                self.selected_idx += 1
                # Adjust offset if needed
                if self.selected_idx - self.offset >= self.max_visible - 2:
                    self.offset += 1
            return "TASK_SELECTED"
        elif key in [ord('k'), curses.KEY_UP]:
            if self.selected_idx > 0:
                self.selected_idx -= 1
                # Adjust offset if needed
                if self.selected_idx < self.offset:
                    self.offset -= 1
            return "TASK_SELECTED"
        elif key == ord('c'):
            if self.selected_idx < len(self.tasks):
                return "TOGGLE_TASK"
        elif key == ord('d'):
            if self.selected_idx < len(self.tasks):
                return "DELETE_TASK"
        elif key == ord('e'):
            if self.selected_idx < len(self.tasks):
                return "EDIT_TASK"

        return ""

    def scroll_up(self) -> None:
        """Scroll up in the task list"""
        if self.offset > 0:
            self.offset -= 1

    def scroll_down(self) -> None:
        """Scroll down in the task list"""
        max_offset = max(0, len(self.tasks) - self.max_visible + 2)
        if self.offset < max_offset:
            self.offset += 1

    def select_next(self) -> None:
        """Select the next task"""
        if self.selected_idx < len(self.tasks) - 1:
            self.selected_idx += 1
            # Adjust offset if needed
            if self.selected_idx - self.offset >= self.max_visible - 2:
                self.offset += 1

    def select_prev(self) -> None:
        """Select the previous task"""
        if self.selected_idx > 0:
            self.selected_idx -= 1
            # Adjust offset if needed
            if self.selected_idx < self.offset:
                self.offset -= 1


class TaskDetail(BaseUI):
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Renders detailed view of selected task

        Attributes:
            current_task: Task object currently being displayed
        """
        super().__init__(stdscr, height, width, start_y, start_x)
        self.current_task = None

    def set_task(self, task: Task) -> None:
        """Set the task to display in detail view"""
        self.current_task = task

    def render(self) -> None:
        """Render the detailed view of the selected task"""
        self.win.clear()

        # Draw borders
        for x in range(self.width):
            self.win.addch(0, x, ord('-'))
            if self.height > 1:
                self.win.addch(self.height - 1, x, ord('-'))

        for y in range(self.height):
            self.win.addch(y, 0, ord('|'))
            if self.width > 1:
                self.win.addch(y, self.width - 1, ord('|'))

        if self.current_task:
            # Display task details
            row = 1
            self.win.addstr(row, 2, f"Title: {self.current_task.title}")
            row += 1
            status = "Completed" if self.current_task.completed else "Pending"
            self.win.addstr(row, 2, f"Status: {status}")
            row += 1
            self.win.addstr(row, 2, f"Category: {self.current_task.category}")
            row += 1
            self.win.addstr(row, 2, f"Priority: {self.current_task.priority}")
            row += 1
            if self.current_task.created_at:
                self.win.addstr(row, 2, f"Created: {self.current_task.created_at.strftime('%Y-%m-%d %H:%M')}")
            row += 2

            # Display description
            if self.current_task.description:
                self.win.addstr(row, 2, "Description:", curses.A_BOLD)
                row += 1

                # Wrap description text
                desc_lines = self.current_task.description.split('\n')
                for line in desc_lines:
                    # Break long lines
                    wrapped_lines = [line[i:i+self.width-4] for i in range(0, len(line), self.width-4)]
                    for wrapped_line in wrapped_lines:
                        if row < self.height - 1:
                            self.win.addstr(row, 2, wrapped_line)
                            row += 1
                        if row >= self.height - 1:
                            break
                    if row >= self.height - 1:
                        break
        else:
            self.win.addstr(1, 2, "No task selected", curses.A_DIM)

        self.win.refresh()


class Footer(BaseUI):
    def __init__(self, stdscr, width: int, start_y: int, start_x: int = 0):
        """
        Renders key binding hints and status information
        """
        super().__init__(stdscr, 3, width, start_y, start_x)
        self.status_message = ""

    def render(self) -> None:
        """Render the footer with key bindings and status"""
        self.win.clear()

        # Draw top border
        for x in range(self.width):
            self.win.addch(0, x, ord('-'))

        # Draw key bindings
        key_hints = "Keys: [a]dd [d]elete [e]dit [c]omplete [n]otes [q]uit"
        self.win.addstr(1, 2, key_hints, curses.color_pair(8))  # FOOTER color

        # Draw status message if available
        if self.status_message:
            # Clear the rest of the line first
            self.win.clrtoeol()
            # Add status message at the right side
            msg_len = len(self.status_message)
            if self.width > msg_len + 2:
                self.win.addstr(1, self.width - msg_len - 2, self.status_message, curses.color_pair(8))

        self.win.refresh()

    def set_status(self, message: str) -> None:
        """Set the status message to display in the footer"""
        self.status_message = message


class HydroTodoApp:
    def __init__(self):
        """
        Main application class that orchestrates all components
        """
        self.stdscr = None
        self.task_manager = TaskManager()
        self.current_category = "GENERAL"
        self.search_query = ""

        # UI Components
        self.header = None
        self.navigation = None
        self.task_list = None
        self.task_detail = None
        self.footer = None

    def initialize_ui(self) -> None:
        """Initialize curses and all UI components"""
        # Initialize curses
        self.stdscr = curses.initscr()
        curses.noecho()  # Turn off automatic echoing of keys
        curses.cbreak()  # React to keys instantly without waiting for enter
        self.stdscr.keypad(True)  # Enable keypad mode for special keys
        curses.curs_set(0)  # Hide cursor

        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # HEADER: white on blue
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # NAV_ACTIVE: black on cyan
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)   # NAV_INACTIVE: black on white
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # TASK_NORMAL: black on white
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA) # TASK_ALTERNATE: black on magenta as alternative to gray
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # SELECTION: black on yellow
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)   # TASK_COMPLETED: green text
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)   # FOOTER: white on black

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle signals for graceful shutdown"""
        self.cleanup()
        exit(0)

        # Calculate screen dimensions
        height, width = self.stdscr.getmaxyx()

        # Initialize UI components with calculated positions
        self.header = Header(self.stdscr, width, 0, 0)

        nav_height = 3
        self.navigation = Navigation(self.stdscr, width, 3, 0)

        footer_height = 3
        main_height = height - nav_height - footer_height - 6  # Account for borders

        # Split remaining space between task list and detail (50/50)
        list_width = width // 2 - 2  # Leave space for border
        detail_width = width - list_width - 4  # Account for borders between panes

        self.task_list = TaskList(self.stdscr, main_height, list_width, 6, 0)
        self.task_detail = TaskDetail(self.stdscr, main_height, detail_width, 6, list_width + 2)

        self.footer = Footer(self.stdscr, width, height - 3, 0)

        # Set initial tasks for the current category
        self._update_task_list()

    def _update_task_list(self) -> None:
        """Update the task list based on current category and search query"""
        if self.search_query:
            tasks = self.task_manager.search_tasks(self.search_query)
            # Filter by current category after search
            tasks = [t for t in tasks if t.category == self.current_category]
        else:
            tasks = self.task_manager.get_tasks_by_category(self.current_category)

        self.task_list.set_tasks(tasks)

        # Update task detail if a task is selected
        if self.task_list.selected_idx < len(tasks):
            selected_task = tasks[self.task_list.selected_idx]
            self.task_detail.set_task(selected_task)
        else:
            self.task_detail.set_task(None)

    def run(self) -> None:
        """Main application loop"""
        # Initial render
        self.header.render()
        self.navigation.render()
        self.task_list.render()
        self.task_detail.render()
        self.footer.render()

        # Main event loop
        while True:
            try:
                # Get user input
                key = self.stdscr.getch()

                # Handle global key bindings
                if key == ord('q'):
                    break  # Quit application
                elif key == ord('a'):
                    # Add new task
                    self.handle_add_task()
                    self._update_task_list()
                    self.refresh_display()
                elif key == ord('n'):
                    # View/edit notes
                    self.handle_view_notes()
                    self.refresh_display()
                elif key == 27:  # ESC key
                    self.footer.set_status("Cancelled")
                    self.footer.render()

                # Handle navigation input
                nav_result = self.navigation.handle_input(key)
                if nav_result == "TAB_CHANGED":
                    self.current_category = self.navigation.active_tab
                    self.search_query = ""  # Clear search when changing categories
                    self._update_task_list()
                    self.refresh_display()
                elif nav_result == "SEARCH_UPDATED":
                    self.search_query = self.navigation.search_query
                    self._update_task_list()
                    self.refresh_display()

                # Handle task list input
                list_result = self.task_list.handle_input(key)
                if list_result == "TASK_SELECTED":
                    # Update task detail view when task selection changes
                    tasks = self.task_list.tasks
                    if self.task_list.selected_idx < len(tasks):
                        selected_task = tasks[self.task_list.selected_idx]
                        self.task_detail.set_task(selected_task)
                    else:
                        self.task_detail.set_task(None)
                    self.task_list.render()
                    self.task_detail.render()
                elif list_result == "TOGGLE_TASK":
                    # Toggle the selected task's completion status
                    tasks = self.task_list.tasks
                    if self.task_list.selected_idx < len(tasks):
                        task_id = tasks[self.task_list.selected_idx].id
                        self.task_manager.toggle_completion(task_id)
                        self._update_task_list()  # Refresh the list
                        self.refresh_display()
                        self.footer.set_status(f"Toggled task {task_id}")
                elif list_result == "DELETE_TASK":
                    # Delete the selected task
                    tasks = self.task_list.tasks
                    if self.task_list.selected_idx < len(tasks):
                        task_id = tasks[self.task_list.selected_idx].id
                        task_title = tasks[self.task_list.selected_idx].title
                        if self.task_manager.delete_task(task_id):
                            self._update_task_list()
                            self.refresh_display()
                            self.footer.set_status(f"Deleted task: {task_title}")
                        else:
                            self.footer.set_status(f"Could not delete task {task_id}")
                elif list_result == "EDIT_TASK":
                    # Edit the selected task
                    self.handle_edit_task()
                    self._update_task_list()
                    self.refresh_display()

            except KeyboardInterrupt:
                break

        # Cleanup before exit
        self.cleanup()

    def cleanup(self) -> None:
        """Cleanup curses and save data"""
        # Restore terminal settings
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        # Save data before exiting
        try:
            self.task_manager.save_to_file()
        except Exception as e:
            print(f"Warning: Could not save tasks before exit: {str(e)}")

    def refresh_display(self) -> None:
        """Refresh all UI components"""
        self.header.render()
        self.navigation.render()
        self.task_list.render()
        self.task_detail.render()
        self.footer.render()

    # Event handlers
    def handle_add_task(self) -> None:
        """Placeholder for adding a task - in a full implementation, this would show an input dialog"""
        # For now, we'll add a placeholder task
        try:
            self.task_manager.add_task(
                f"New task {len(self.task_manager.get_all_tasks()) + 1}",
                "Added via UI",
                self.current_category
            )
            self.footer.set_status("Added new task")
        except ValueError as e:
            self.footer.set_status(f"Error: {str(e)}")

    def handle_delete_task(self) -> None:
        """Placeholder for deleting a task"""
        # This is now handled directly in the main loop
        pass

    def handle_edit_task(self) -> None:
        """Placeholder for editing a task - in a full implementation, this would show an edit dialog"""
        # For now, we'll just show a status message
        tasks = self.task_list.tasks
        if self.task_list.selected_idx < len(tasks):
            self.footer.set_status(f"Editing task: {tasks[self.task_list.selected_idx].title}")
        else:
            self.footer.set_status("No task selected to edit")

    def handle_toggle_completion(self) -> None:
        """Placeholder for toggling task completion"""
        # This is now handled directly in the main loop
        pass

    def handle_view_notes(self) -> None:
        """Placeholder for viewing/editing task notes"""
        tasks = self.task_list.tasks
        if self.task_list.selected_idx < len(tasks):
            task = tasks[self.task_list.selected_idx]
            self.footer.set_status(f"Viewing notes for: {task.title}")
        else:
            self.footer.set_status("No task selected")

    def handle_search(self) -> None:
        """Placeholder for search functionality"""
        # This is now handled in the navigation component
        pass

    def handle_quit(self) -> None:
        """Placeholder for quit functionality"""
        # This is now handled directly in the main loop
        pass


def main(stdscr):
    """Main entry point for the curses application"""
    app = HydroTodoApp()

    # Set the stdscr in the app
    app.stdscr = stdscr

    # Initialize UI components
    height, width = stdscr.getmaxyx()

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # HEADER
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # NAV_ACTIVE
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)   # NAV_INACTIVE
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # TASK_NORMAL
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA) # TASK_ALTERNATE (using magenta as gray alternative)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # SELECTION
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)   # TASK_COMPLETED
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)   # FOOTER

    # Initialize components
    app.header = Header(stdscr, width, 0, 0)

    nav_height = 3
    app.navigation = Navigation(stdscr, width, 3, 0)

    footer_height = 3
    main_height = height - nav_height - footer_height - 6

    list_width = width // 2 - 2
    detail_width = width - list_width - 4

    app.task_list = TaskList(stdscr, main_height, list_width, 6, 0)
    app.task_detail = TaskDetail(stdscr, main_height, detail_width, 6, list_width + 2)
    app.footer = Footer(stdscr, width, height - 3, 0)

    # Set initial tasks
    app._update_task_list()

    # Initial render
    app.header.render()
    app.navigation.render()
    app.task_list.render()
    app.task_detail.render()
    app.footer.render()

    # Main loop
    app.run()


# Example usage and testing
if __name__ == "__main__":
    # For now, run the curses app
    try:
        # Initialize with curses wrapper to handle setup/cleanup automatically
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        # Try to restore terminal settings if something went wrong
        try:
            curses.endwin()
        except:
            pass