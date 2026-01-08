# Data Model: Premium Visual Todo TUI (Phase-1)

## Task Entity

### Fields
- **id**: int (required) - Sequential unique identifier for the task (starting from 1)
- **title**: str (required, max 50 chars) - Text describing the task
- **description**: str (optional, max 200 chars) - Additional details about the task
- **completed**: bool (required) - Boolean indicating completion status
- **created_at**: datetime (required) - Timestamp when the task was created

### Validation Rules
- Title must be between 1 and 50 characters (inclusive)
- Description must be between 0 and 200 characters (inclusive)
- ID must be a positive integer
- Completed must be a boolean value
- Created_at must be a valid datetime object

### State Transitions
- **Pending → Completed**: When user toggles task completion status
- **Completed → Pending**: When user toggles task completion status

## TaskList Collection

### Fields
- **tasks**: List[Task] - Collection of Task entities
- **filtered_tasks**: List[Task] - Subset of tasks based on current filters
- **search_query**: str - Current search filter text

### Operations
- **Add Task**: Append new Task to the collection
- **Update Task**: Modify existing Task properties
- **Delete Task**: Remove Task from the collection
- **Filter Tasks**: Return subset matching status (All, Pending, Completed)
- **Search Tasks**: Return subset matching title/description query