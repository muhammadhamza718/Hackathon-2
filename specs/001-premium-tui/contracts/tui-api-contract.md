# API Contract: Premium Visual Todo TUI (Phase-1)

## Task Operations

### Add Task
- **Trigger**: User presses 'a' key
- **Input**: title (str, 1-50 chars), description (str, 0-200 chars)
- **Output**: Task object with id, title, description, completed=False, created_at
- **Error Cases**: Invalid input (title too long, etc.)

### List Tasks
- **Trigger**: Application loads or task operations complete
- **Input**: None
- **Output**: List of Task objects
- **Filters**: Status (All, Pending, Completed), Search query

### Update Task
- **Trigger**: User presses 'u' key on selected task
- **Input**: task_id, updated fields (title, description)
- **Output**: Boolean indicating success
- **Error Cases**: Task not found, invalid input

### Delete Task
- **Trigger**: User presses 'd' key on selected task
- **Input**: task_id
- **Output**: Boolean indicating success
- **Error Cases**: Task not found

### Toggle Task Completion
- **Trigger**: User presses 'c' key on selected task
- **Input**: task_id
- **Output**: Boolean indicating success
- **Error Cases**: Task not found

## UI Operations

### Search Tasks
- **Trigger**: User types in search field
- **Input**: search query string
- **Output**: Filtered list of Task objects
- **Behavior**: Real-time filtering as user types

### Focus Search
- **Trigger**: User presses '/' key
- **Input**: None
- **Output**: Search input field receives focus