# Quickstart Guide: Premium Todo TUI (Phase-1)

## Prerequisites

- Python 3.13 or higher
- UV package manager
- Terminal with support for color and mouse interaction

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Install the required packages**:
   ```bash
   uv add textual rich
   ```

## Running the Application

1. **Launch the Premium TUI**:
   ```bash
   uv run python main.py --premium
   ```

2. **Or make it the default**:
   ```bash
   uv run python main.py
   ```

## Key Features

### Navigation
- Use arrow keys to navigate through tasks
- Press `Tab` to move between UI components
- Mouse support available for all interactive elements

### Keyboard Shortcuts
- `A` - Add new task
- `U` - Update selected task
- `D` - Delete selected task
- `C` - Toggle completion status
- `/` - Focus search bar
- `Q` - Quit application
- `F` - Focus filter sidebar

### Task Management
1. **Adding Tasks**: Press `A` to open the add task modal
2. **Editing Tasks**: Select a task and press `U` to edit
3. **Deleting Tasks**: Select a task and press `D` to delete
4. **Completing Tasks**: Select a task and press `C` to toggle completion

### Filtering and Searching
- Use the sidebar to filter by status and priority
- Type in the search bar at the top to filter tasks in real-time
- Combine filters and search for precise results

## Visual Indicators

- **High Priority**: Red color with 🔴 icon
- **Medium Priority**: Yellow color with 🟡 icon
- **Low Priority**: Green color with 🟢 icon
- **Completed Tasks**: Strikethrough text with ✅ icon
- **Pending Tasks**: Normal text with ⏳ icon

## Troubleshooting

- If colors don't display properly, ensure your terminal supports ANSI colors
- If mouse doesn't work, try using keyboard shortcuts instead
- For performance issues with large task lists, consider reducing the number of tasks