# Data Model: Todo Console App

## Task Entity

### Schema
```python
@dataclass
class Task:
    id: int
    title: str  # max 50 characters
    description: str  # max 200 characters
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

### Fields
- **id**: Sequential integer identifier (auto-generated)
- **title**: Required string (1-50 characters)
- **description**: Optional string (0-200 characters)
- **completed**: Boolean indicating completion status (default False)
- **created_at**: Timestamp of task creation (auto-generated)

### Validation Rules
- Title must be 1-50 characters (inclusive)
- Description must be 0-200 characters (inclusive)
- ID must be unique within the system
- ID must be positive integer

### State Transitions
- New task: `completed = False` by default
- Toggle operation: `completed = not completed`

## Storage Model
- **Type**: In-memory Python list of Task objects
- **Access**: Direct list operations (append, remove, index)
- **Concurrency**: Single-threaded access (no concurrent modifications)
- **Lifetime**: Exists only during application runtime