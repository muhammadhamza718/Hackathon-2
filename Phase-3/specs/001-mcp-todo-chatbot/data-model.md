# Data Model: AI-Powered Todo Chatbot

## Todo Entity

### Fields
- **id** (UUID/Integer): Unique identifier for the todo item
  - Type: UUID (primary key) or Auto-incrementing Integer
  - Required: Yes
  - Constraints: Unique, Not null

- **content** (String): The text content of the todo item
  - Type: String (VARCHAR)
  - Required: Yes
  - Constraints: Not null, Max length 1000 characters
  - Validation: Must not be empty or whitespace only

- **completed** (Boolean): Status indicating if the todo is completed
  - Type: Boolean
  - Required: No
  - Default: False
  - Constraints: Not null

- **created_at** (DateTime): Timestamp when the todo was created
  - Type: DateTime (with timezone)
  - Required: Yes
  - Default: Current timestamp
  - Constraints: Not null

- **completed_at** (DateTime): Timestamp when the todo was marked as completed
  - Type: DateTime (nullable, with timezone)
  - Required: No
  - Default: NULL
  - Constraints: Can be null if not completed

- **due_date** (DateTime): Optional due date for the todo
  - Type: DateTime (nullable, with timezone)
  - Required: No
  - Default: NULL
  - Constraints: Can be null

### Relationships
- No direct relationships needed for the basic Todo entity
- Future extension could include User relationship for multi-user support

### Validation Rules
- Content must be at least 1 character (after trimming whitespace)
- Due date must be in the future if provided
- Completed todos can be uncompleted (completed_at can be reset)

## User Session Entity (for conversation state)

### Fields
- **id** (UUID/Integer): Unique identifier for the session
  - Type: UUID (primary key) or Auto-incrementing Integer
  - Required: Yes
  - Constraints: Unique, Not null

- **user_id** (String/UUID): Identifier for the user
  - Type: String or UUID
  - Required: No (for now, could be extended for multi-user)
  - Default: NULL

- **session_data** (JSON): JSON blob containing conversation context
  - Type: JSON/JSONB
  - Required: No
  - Default: {}
  - Constraints: Valid JSON format

- **created_at** (DateTime): Timestamp when the session was created
  - Type: DateTime (with timezone)
  - Required: Yes
  - Default: Current timestamp
  - Constraints: Not null

- **updated_at** (DateTime): Timestamp when the session was last updated
  - Type: DateTime (with timezone)
  - Required: Yes
  - Default: Current timestamp
  - Constraints: Not null

## Chat Message Entity (for conversation history)

### Fields
- **id** (UUID/Integer): Unique identifier for the message
  - Type: UUID (primary key) or Auto-incrementing Integer
  - Required: Yes
  - Constraints: Unique, Not null

- **session_id** (UUID/Integer): Reference to the user session
  - Type: UUID or Integer (foreign key)
  - Required: Yes
  - Constraints: Not null, References session.id

- **role** (String): The role of the message sender
  - Type: String (ENUM: 'user', 'assistant', 'system')
  - Required: Yes
  - Constraints: Not null, Must be one of allowed values

- **content** (Text): The content of the message
  - Type: Text
  - Required: Yes
  - Constraints: Not null

- **timestamp** (DateTime): When the message was created
  - Type: DateTime (with timezone)
  - Required: Yes
  - Default: Current timestamp
  - Constraints: Not null

- **metadata** (JSON): Additional metadata about the message
  - Type: JSON/JSONB
  - Required: No
  - Default: {}
  - Constraints: Valid JSON format

## State Transitions

### Todo State Transitions
- **Active Todo**: Default state when created (completed = false)
- **Completed Todo**: When marked as completed (completed = true, completed_at set)
- **Reopened Todo**: When completed todo is marked as incomplete again (completed = false, completed_at reset to NULL)

### Validation for State Transitions
- Cannot complete an already completed todo (should be idempotent)
- Cannot reopen an already active todo
- Must maintain data integrity during state changes

## Database Indexes

### Todo Table
- Index on `user_id` (when implemented) for faster user queries
- Index on `completed` for filtering completed/active todos
- Index on `created_at` for chronological ordering
- Index on `due_date` for due date queries (when not null)

### Session Table
- Index on `user_id` for faster user session retrieval
- Index on `updated_at` for session activity tracking

### Message Table
- Index on `session_id` for session-based queries
- Index on `timestamp` for chronological message retrieval
- Composite index on (`session_id`, `timestamp`) for efficient session timeline queries

## Constraints

### Todo Constraints
- Content cannot be empty or only whitespace
- Due date cannot be in the past (optional validation)
- Prevent duplicate identical todos (optional, based on business requirement)

### Session Constraints
- One active session per user (optional, for session management)
- Session data size limits to prevent oversized records

### Message Constraints
- Session must exist before adding messages
- Role must be one of allowed values
- Message content cannot be empty (optional validation)