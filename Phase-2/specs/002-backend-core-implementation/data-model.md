# Data Model: Backend Core Implementation and Admin Extension

## Entity Definitions

### User Entity
**Table Name**: `user`

**Fields**:
- `id`: str (primary key, auto-generated)
- `email`: str (unique, not null)
- `name`: str (nullable)
- `role`: str (default: "user", values: "user", "admin")
- `created_at`: datetime (default: current timestamp)
- `updated_at`: datetime (default: current timestamp, updates on change)

**Relationships**:
- One-to-many: `tasks` (User.tasks → List[Task])

**Constraints**:
- `email` must be unique
- `role` must be either "user" or "admin"

**Indexes**:
- `email`: Unique index for fast user lookups
- `role`: Index for role-based queries

### Task Entity
**Table Name**: `task`

**Fields**:
- `id`: str (primary key, auto-generated)
- `title`: str (not null)
- `description`: str (nullable)
- `completed`: bool (default: false)
- `user_id`: str (foreign key referencing `user.id`, not null)
- `created_at`: datetime (default: current timestamp)
- `updated_at`: datetime (default: current timestamp, updates on change)

**Relationships**:
- Many-to-one: `user` (Task.user → User)

**Constraints**:
- `user_id` must reference an existing user (foreign key constraint)
- `title` must not be empty

**Indexes**:
- `user_id`: Index for user-based filtering
- `completed`: Index for completion status queries
- `created_at`: Index for chronological sorting

## Entity Relationships

### User-Task Relationship
- **Type**: One-to-Many (One User to Many Tasks)
- **Foreign Key**: `task.user_id` references `user.id`
- **Cascade Delete**: When a User is deleted, all their Tasks are also deleted
- **Access Pattern**: User.tasks provides access to all tasks belonging to a user

## Validation Rules

### User Validation
- Email format validation using standard email regex pattern
- Role field restricted to "user" or "admin" values
- Name field optional, max length 255 characters if provided

### Task Validation
- Title field required, minimum 1 character, maximum 255 characters
- Description field optional, maximum 1000 characters if provided
- Completed field defaults to false, boolean type only

## State Transitions

### Task State Transitions
- `pending` → `completed`: When task is marked as done via PATCH /api/tasks/{id}/complete
- `completed` → `pending`: When task is unmarked via PATCH /api/tasks/{id}/complete

## Query Patterns

### Common Queries
1. **User's Tasks**: `SELECT * FROM task WHERE user_id = :user_id`
2. **Task by ID for User**: `SELECT * FROM task WHERE id = :task_id AND user_id = :user_id`
3. **All Users (Admin)**: `SELECT * FROM user WHERE role = 'admin'`
4. **Tasks for Specific User (Admin)**: `SELECT * FROM task WHERE user_id = :user_id`

## Database Indexing Strategy
- Primary indexes on all ID fields for fast lookups
- Foreign key indexes for relationship queries
- Role index for admin access patterns
- Completion status index for filtering completed tasks