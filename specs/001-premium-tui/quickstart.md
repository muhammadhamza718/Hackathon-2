# Quickstart Guide: Premium Visual Todo TUI (Phase-1)

## Prerequisites
- Python 3.13+
- UV package manager

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run python main.py
   ```

   Or to explicitly launch the premium TUI:
   ```bash
   uv run python main.py --premium
   ```

## Key Features

### Visual Elements
- Large gradient "TODO" logo in cyan-to-purple at the top
- Styled DataTable showing tasks with status indicators (✅ completed, ⏳ pending)
- Themed interface with deep background (#0f0f14) and bright accents

### Keyboard Shortcuts
- `a` - Add new task (opens modal dialog)
- `u` - Update selected task (opens modal dialog)
- `d` - Delete selected task (with confirmation)
- `c` - Toggle completion status of selected task
- `/` - Focus search input
- `q` - Quit the application

### Task Management
1. **Add Task**: Press 'a' to open modal, enter title and description, confirm
2. **Update Task**: Select task, press 'u', modify details in modal, confirm
3. **Delete Task**: Select task, press 'd', confirm deletion
4. **Toggle Complete**: Select task, press 'c' to toggle status
5. **Search**: Press '/' to focus search, type to filter tasks by title

## Development

### Running Tests
```bash
uv run pytest
```

### Code Structure
- `src/ui/premium_todo_app.py` - Main Textual application
- `src/ui/components/` - Modal dialogs and visual components
- `src/services/task_service.py` - Business logic layer
- `src/models/task.py` - Data model

### Customization
- Modify CSS in the `PremiumTodoApp` class for styling changes
- Update color palette in the styling section to match different themes