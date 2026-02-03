# HydroToDo Phase 1: Implementation Plan

## Overview
This document outlines the step-by-step implementation plan for HydroToDo Phase 1, following the architectural separation between Data Layer (Task/TodoApp classes) and UI Layer (Curses implementation). The plan follows a progressive approach from core logic to polished UI.

## Architecture Verification
- **Data Layer**: Task and TaskManager classes with in-memory CRUD and JSON persistence
- **UI Layer**: Curses implementation with clean separation of concerns
- **Event System**: Keybindings connected to core logic through well-defined interfaces

## Step-by-Step Implementation

### Step 1: Core Logic Implementation
**Objective**: Implement Task and TaskManager classes with simple in-memory CRUD and JSON persistence

**Tasks**:
1. Implement the `Task` class with validation methods
   - Constructor with all required fields (id, title, description, category, completed, priority, created_at)
   - Validation methods for each field (validate_title, validate_description, validate_category, validate_priority)
   - Utility methods (to_dict, from_dict)
   - Field validation based on specification requirements (title: 1-50 chars, description: 0-200 chars, etc.)

2. Implement the `TaskManager` class
   - Constructor with data_file parameter defaulting to "todo_data.json"
   - CRUD operations: add_task, get_task, update_task, delete_task, toggle_completion
   - Query operations: get_all_tasks, get_tasks_by_category, search_tasks, filter_tasks
   - Persistence methods: save_to_file, load_from_file, backup_data
   - Initialize with sample data if file doesn't exist

3. Implement data persistence
   - JSON serialization/deserialization with proper format matching specification
   - Error handling for file operations
   - Backup mechanism for data safety

4. Unit tests for core logic
   - Test Task validation methods
   - Test TaskManager CRUD operations
   - Test data persistence functions

### Step 2: Curses Environment Setup
**Objective**: Create the safe wrapper for the curses environment (handling colors, key inputs, and clean exit)

**Tasks**:
1. Set up basic curses application structure
   - Initialize curses environment (curses.initscr(), curses.noecho(), curses.cbreak())
   - Enable keypad for special keys
   - Initialize color pairs based on specification color scheme
   - Set up signal handlers for graceful shutdown

2. Implement color pair definitions
   - HEADER: Bold white on blue background
   - NAV_ACTIVE: Blue background for active tab
   - NAV_INACTIVE: White background for inactive tab
   - TASK_NORMAL: White background for normal task rows
   - TASK_ALTERNATE: Light gray background for alternate task rows
   - TASK_COMPLETED: Green for completed task checkmark
   - SELECTION: Yellow highlight for active selection
   - FOOTER: White text on black background

3. Create safe wrapper functions
   - Safe initialization function that handles exceptions
   - Cleanup function that restores terminal to original state
   - Exception handling for various curses errors

4. Implement key input handling
   - Map special keys (arrow keys, function keys) to character representations
   - Handle Unicode characters safely
   - Implement input buffering if needed

### Step 3: UI Layout Engine
**Objective**: Implement the drawing logic for the 4-section layout (Header, Nav, Split-Pane, Footer)

**Tasks**:
1. Implement the `BaseUI` component
   - Constructor with stdscr, dimensions, and position parameters
   - Abstract render method
   - Input handling method
   - Resize method for dynamic layout adjustments

2. Implement the `Header` component
   - Render ASCII art "HYDROTODO" title centered in header area
   - Apply header color scheme (bold white on blue)
   - Handle different terminal widths gracefully

3. Implement the `Navigation` component
   - Render category tabs (GENERAL, WORK, PERSONAL) with borders
   - Highlight active tab with blue background
   - Render search bar on right side
   - Handle tab switching and search input

4. Implement the `TaskList` component
   - Render scrollable list of tasks with checkboxes ([x]/[ ])
   - Alternate row colors (white/light gray) for readability
   - Highlight selected task with yellow border
   - Implement pagination for large task lists
   - Show task status (completed with green checkmark and strikethrough)

5. Implement the `TaskDetail` component
   - Render detailed view of selected task
   - Display title, status, creation date, and description
   - Format content to fit within component bounds
   - Handle long text with proper wrapping

6. Implement the `Footer` component
   - Render key binding hints in footer area
   - Display status messages
   - Apply footer color scheme (white text on black background)

### Step 4: Event Loop & Interactivity
**Objective**: Connect keybindings (`j`, `k`, `a`, `d`, etc.) to the Core Logic

**Tasks**:
1. Implement the main application class `HydroTodoApp`
   - Initialize all UI components with proper positioning
   - Store references to task manager and UI components
   - Track current state (selected task, active tab, search query)

2. Implement the main event loop
   - Continuously read key inputs
   - Dispatch events to appropriate handlers
   - Refresh display after each action
   - Handle terminal resize events

3. Connect keybindings to functionality
   - `j` / Down Arrow: Move down in task list (select_next)
   - `k` / Up Arrow: Move up in task list (select_prev)
   - `h` / Left Arrow: Switch to previous tab (switch_tab(-1))
   - `l` / Right Arrow: Switch to next tab (switch_tab(1))
   - `a`: Add new task (handle_add_task)
   - `d`: Delete selected task (handle_delete_task)
   - `e`: Edit selected task (handle_edit_task)
   - `c`: Toggle completion status (handle_toggle_completion)
   - `n`: View/edit task notes/description (handle_view_notes)
   - `Enter`: Select/activate focused element
   - `q`: Quit application (handle_quit)
   - `/`: Focus search bar (handle_search)
   - `Esc`: Cancel current operation or clear selection

4. Implement event handlers
   - Each handler should interact with TaskManager and refresh UI
   - Update status messages in footer
   - Handle edge cases and error conditions

5. Implement category filtering
   - Update task list when category tab is switched
   - Ensure task detail view shows appropriate task for current category

6. Implement search functionality
   - Filter tasks based on search query
   - Update UI to show search results
   - Clear search when category changes

### Step 5: Polish & Final Touches
**Objective**: Add the specific visual details (borders, reverse video for active tabs)

**Tasks**:
1. Enhance visual appearance
   - Add borders around each UI section
   - Implement reverse video for active tabs
   - Fine-tune color schemes for better contrast
   - Add subtle shadows or depth effects where appropriate

2. Optimize performance
   - Implement efficient rendering (only redraw changed components)
   - Optimize string operations during render cycles
   - Add lazy loading for task details
   - Profile application with large task lists (1000+ tasks)

3. Implement advanced features
   - Screen resize handling to prevent display corruption
   - Smooth scrolling for large task lists
   - Task sorting options (by date, priority, etc.)
   - Confirmation dialogs for destructive operations

4. Add error handling and user feedback
   - Display informative error messages in footer
   - Handle edge cases gracefully
   - Add visual feedback for user actions
   - Implement proper validation with clear error messages

5. Final testing and refinement
   - Test with various terminal sizes
   - Verify all key bindings work correctly
   - Test data persistence and recovery
   - Performance testing with large datasets
   - Cross-platform compatibility testing

6. Documentation and code cleanup
   - Add docstrings to all public methods
   - Comment complex algorithms
   - Clean up code formatting
   - Ensure consistent coding style

## Implementation Timeline

### Week 1: Core Logic & Curses Setup
- Complete Step 1: Core Logic Implementation
- Complete Step 2: Curses Environment Setup

### Week 2: UI Layout & Basic Interactivity
- Complete Step 3: UI Layout Engine
- Begin Step 4: Event Loop & Interactivity

### Week 3: Full Interactivity & Polish
- Complete Step 4: Event Loop & Interactivity
- Complete Step 5: Polish & Final Touches

## Success Criteria

### Functional Requirements Met
- [ ] Add Task: Create new items with title and optional description
- [ ] Delete Task: Remove items by ID or selection
- [ ] Update Task: Edit existing task details
- [ ] View List: Display all tasks with proper categorization
- [ ] Mark as Complete: Toggle completion status
- [ ] Data Persistence: Save/load from JSON file

### UI/UX Requirements Met
- [ ] Clean, intuitive curses-based interface
- [ ] Responsive keyboard navigation (j/k/h/l/a/d/c/n/q)
- [ ] Proper visual feedback for selections
- [ ] Clear key binding instructions in footer
- [ ] Attractive color scheme and formatting

### Performance Requirements Met
- [ ] Handle up to 1000 tasks efficiently
- [ ] Sub-100ms response times for operations
- [ ] Smooth scrolling for long task lists
- [ ] Proper handling of terminal resize events

### Quality Requirements Met
- [ ] Comprehensive error handling
- [ ] Data integrity maintained during operations
- [ ] Proper cleanup on exit
- [ ] Cross-platform compatibility