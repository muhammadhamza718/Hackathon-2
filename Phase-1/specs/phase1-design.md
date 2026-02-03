# HydroToDo - Phase 1: In-Memory Curses TUI Specification

## Overview
HydroToDo is a clean, high-performance, in-memory console application built with Python's curses library. This document outlines the architecture, class structure, and UI design for Phase 1 of the "Evolution of Todo" Hackathon project.

## Functional Requirements

### 1. Task Management Operations
- **Add Task**: Create new items with title and optional description
- **Delete Task**: Remove items by ID or selection
- **Update Task**: Edit existing task details
- **View List**: Display all tasks
- **Mark as Complete**: Toggle completion status

### 2. Data Persistence
- In-memory storage using Python standard data structures (Lists/Dicts)
- Data persisted to `todo_data.json` on exit only
- No external database allowed

### 3. Performance Requirements
- Responsive UI with sub-100ms response times for user interactions
- Efficient rendering for up to 1000 tasks
- Smooth navigation between UI elements

## UI/UX Design System

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                        HYDROTODO                            │  <- Header with ASCII art
├─────────────────────────────────────────────────────────────┤
│  GENERAL  │  WORK  │  PERSONAL  │ [SEARCH]                  │  <- Navigation Bar
├────────────┬────────────────────────────────────────────────┤
│ [x] Task 1 │                                                │
│ [ ] Task 2 │  Task Detail View                              │
│ [x] Task 3 │  ┌──────────────────────────────────────────┐  │
│ [ ] Task 4 │  │ Title: Sample Task                       │  │
│ [ ] Task 5 │  │ Status: Pending                          │  │
│ ...        │  │ Created: 2026-01-06                      │  │
│            │  │ Description: Detailed description here   │  │
│            │  │ ...                                      │  │
│            │  └──────────────────────────────────────────┘  │
│            │                                                │
│            │                                                │
│            │                                                │
│            │                                                │
│            │                                                │
│            │                                                │
├─────────────────────────────────────────────────────────────┤
│ Keys: [a]dd [d]elete [e]dit [c]omplete [n]otes [q]uit      │  <- Footer
└─────────────────────────────────────────────────────────────┘
```

### Color Scheme
- **Header**: Bold white on blue background
- **Navigation Tabs**: Blue background for active, white background for inactive
- **Task List**: Alternating row colors (white/light gray)
- **Completed Tasks**: Green checkmark, strike-through text
- **Active Selection**: Yellow highlight
- **Footer**: White text on black background

### Key Bindings
- `j` / `Down Arrow`: Move down in task list
- `k` / `Up Arrow`: Move up in task list
- `h` / `Left Arrow`: Switch to previous tab (GENERAL ← WORK ← PERSONAL)
- `l` / `Right Arrow`: Switch to next tab (GENERAL → WORK → PERSONAL)
- `a`: Add new task
- `d`: Delete selected task
- `e`: Edit selected task
- `c`: Toggle completion status
- `n`: View/edit task notes/description
- `Enter`: Select/activate focused element
- `q`: Quit application
- `/`: Focus search bar
- `Esc`: Cancel current operation or clear selection

## Technology Stack
- **Python**: 3.13+
- **Standard Libraries Only**:
  - `curses`: Primary UI framework
  - `json`: Data serialization/deserialization
  - `textwrap`: Text formatting and wrapping
  - `datetime`: Timestamp management
- **External Packages**: None (Rich, Textual, and other packages are prohibited)

## Class Structure

### Task Class
```python
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

    # Validation methods
    def validate_title(self, title: str) -> bool
    def validate_description(self, description: str) -> bool
    def validate_category(self, category: str) -> bool
    def validate_priority(self, priority: str) -> bool

    # Utility methods
    def to_dict(self) -> dict
    @classmethod
    def from_dict(cls, data: dict) -> Task
```

### TaskManager Class
```python
class TaskManager:
    def __init__(self, data_file: str = "todo_data.json"):
        """
        Manages all tasks in memory and handles persistence

        Args:
            data_file: Path to JSON file for data persistence
        """

    # CRUD operations
    def add_task(self, title: str, description: str = "",
                 category: str = "GENERAL", priority: str = "MEDIUM") -> Task
    def get_task(self, task_id: int) -> Task
    def update_task(self, task_id: int, title: str = None, description: str = None,
                   category: str = None, priority: str = None) -> Task
    def delete_task(self, task_id: int) -> bool
    def toggle_completion(self, task_id: int) -> Task

    # Query operations
    def get_all_tasks(self) -> List[Task]
    def get_tasks_by_category(self, category: str) -> List[Task]
    def search_tasks(self, query: str) -> List[Task]
    def filter_tasks(self, completed: bool = None,
                     priority: str = None, category: str = None) -> List[Task]

    # Persistence
    def save_to_file(self) -> None
    def load_from_file(self) -> None
    def backup_data(self) -> None
```

### UI Components

#### BaseUI Component
```python
class BaseUI:
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Base class for all UI components

        Args:
            stdscr: Main curses screen object
            height, width: Dimensions of the component
            start_y, start_x: Position coordinates
        """
    def render(self) -> None
    def handle_input(self, key) -> str  # Returns action string
    def resize(self, height: int, width: int, start_y: int, start_x: int) -> None
```

#### Header Component
```python
class Header(BaseUI):
    def __init__(self, stdscr, width: int):
        """
        Renders the ASCII art header with "HYDROTODO" title
        """
    def render(self) -> None
```

#### Navigation Component
```python
class Navigation(BaseUI):
    def __init__(self, stdscr, width: int, start_y: int, start_x: int):
        """
        Renders category tabs and search bar

        Attributes:
            active_tab: Current selected tab ("GENERAL", "WORK", "PERSONAL")
            search_query: Current search input
        """
    def render(self) -> None
    def handle_input(self, key) -> str
    def switch_tab(self, direction: int) -> None  # -1 for left, +1 for right
    def update_search(self, char: str) -> None
```

#### TaskList Component
```python
class TaskList(BaseUI):
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Renders scrollable list of tasks with checkboxes

        Attributes:
            tasks: List of tasks to display
            selected_idx: Index of currently selected task
            offset: Scroll offset for viewing tasks beyond viewport
        """
    def render(self) -> None
    def handle_input(self, key) -> str
    def scroll_up(self) -> None
    def scroll_down(self) -> None
    def select_next(self) -> None
    def select_prev(self) -> None
```

#### TaskDetail Component
```python
class TaskDetail(BaseUI):
    def __init__(self, stdscr, height: int, width: int, start_y: int, start_x: int):
        """
        Renders detailed view of selected task

        Attributes:
            current_task: Task object currently being displayed
        """
    def render(self) -> None
    def set_task(self, task: Task) -> None
```

#### Footer Component
```python
class Footer(BaseUI):
    def __init__(self, stdscr, width: int, start_y: int):
        """
        Renders key binding hints and status information
        """
    def render(self) -> None
    def set_status(self, message: str) -> None
```

### Main Application Class
```python
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

    def initialize_ui(self) -> None
        """Initialize curses and all UI components"""

    def run(self) -> None
        """Main application loop"""

    def cleanup(self) -> None
        """Cleanup curses and save data"""

    def refresh_display(self) -> None
        """Refresh all UI components"""

    # Event handlers
    def handle_add_task(self) -> None
    def handle_delete_task(self) -> None
    def handle_edit_task(self) -> None
    def handle_toggle_completion(self) -> None
    def handle_view_notes(self) -> None
    def handle_search(self) -> None
    def handle_quit(self) -> None
```

## Data Model

### Task Entity
- **id**: int (unique identifier, auto-incremented)
- **title**: str (required, 1-50 characters)
- **description**: str (optional, 0-200 characters)
- **category**: str (enum: "GENERAL", "WORK", "PERSONAL")
- **completed**: bool (default: False)
- **priority**: str (enum: "LOW", "MEDIUM", "HIGH", default: "MEDIUM")
- **created_at**: datetime (ISO format string)

### Validation Rules
- Title must be 1-50 characters
- Description must be 0-200 characters if provided
- Category must be one of "GENERAL", "WORK", "PERSONAL"
- Priority must be one of "LOW", "MEDIUM", "HIGH"
- Completed must be boolean
- ID must be unique within the application

### JSON File Format
```json
{
  "version": "1.0",
  "last_updated": "2026-01-06T10:00:00Z",
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Detailed description",
      "category": "GENERAL",
      "completed": false,
      "priority": "MEDIUM",
      "created_at": "2026-01-06T10:00:00Z"
    }
  ]
}
```

## Error Handling

### Input Validation
- Invalid task titles/descriptions will show error messages in footer
- Duplicate task IDs will be prevented
- Invalid category/priority values will be rejected

### File Operations
- Data loading errors will show notification and continue with empty task list
- Data saving errors will show notification but application continues
- Backup mechanism will be implemented for data safety

### UI Errors
- Screen resize handling to prevent display corruption
- Graceful handling of unexpected input
- Proper cleanup on application exit

## Performance Considerations

### Memory Management
- Efficient data structures for task storage
- Lazy loading for task details when needed
- Cleanup of unused objects during long sessions

### Rendering Optimization
- Only redraw changed UI components
- Efficient scrolling for large task lists
- Minimal string operations during render cycles

### Responsiveness
- Non-blocking input handling
- Efficient search algorithm with indexing if needed
- Background saving to prevent UI freezes

## Security Considerations

### Input Sanitization
- All user inputs validated before processing
- Prevent injection attacks through input fields
- Safe file operations with proper path validation

### Data Protection
- Local-only data storage
- No network transmission
- Secure temporary file handling

## Testing Strategy

### Unit Tests
- Task model validation
- TaskManager CRUD operations
- Data serialization/deserialization

### Integration Tests
- UI component interactions
- End-to-end task workflows
- File persistence operations

### UI Tests
- Keyboard navigation
- Screen resizing
- Different terminal sizes

## Acceptance Criteria

### Functional
- [ ] Add new tasks with title and optional description
- [ ] Delete tasks by selection
- [ ] Update existing task details
- [ ] View all tasks in categorized list
- [ ] Mark tasks as complete/incomplete
- [ ] Persist data to JSON file on exit
- [ ] Load data from JSON file on startup

### UI/UX
- [ ] Clean, intuitive curses-based interface
- [ ] Responsive keyboard navigation
- [ ] Proper visual feedback for selections
- [ ] Clear key binding instructions
- [ ] Attractive color scheme and formatting

### Performance
- [ ] Handle up to 1000 tasks efficiently
- [ ] Sub-100ms response times for operations
- [ ] Smooth scrolling for long task lists
- [ ] Proper handling of terminal resize events

### Quality
- [ ] Comprehensive error handling
- [ ] Data integrity maintained during operations
- [ ] Proper cleanup on exit
- [ ] Cross-platform compatibility