# Data Model: Phase-5 Advanced Todo Features

## Entity: Task
**Description**: Core entity representing a user's task with advanced fields
**Fields**:
- id: UUID (Primary Key)
- title: String (required, max 255 chars)
- description: Text (optional)
- status: Enum (pending, completed, archived)
- due_date: DateTime (nullable)
- priority: Enum (low, medium, high, critical)
- tags: JSONB (array of strings)
- user_id: UUID (Foreign Key to User)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- recurrence_pattern: JSONB (nullable, structure for recurring tasks)

**Validation Rules**:
- Title must not be empty
- Due date must be in the future if provided
- Priority must be one of the defined values
- Tags array must not exceed 10 items
- Recurrence pattern must follow defined schema if provided

**Relationships**:
- Belongs to one User
- Can have many AuditLogs (one-to-many)

## Entity: RecurringTaskTemplate
**Description**: Template that defines the pattern for generating recurring tasks
**Fields**:
- id: UUID (Primary Key)
- name: String (required, max 255 chars)
- description: Text (optional)
- recurrence_pattern: JSONB (required, defines frequency, interval, end conditions)
- task_template: JSONB (template for creating new tasks)
- user_id: UUID (Foreign Key to User)
- active: Boolean (default true)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)

**Validation Rules**:
- Name must not be empty
- Recurrence pattern must follow defined schema
- Task template must contain valid task fields
- User must exist

**Relationships**:
- Belongs to one User
- Has many generated Tasks (one-to-many)

## Entity: User
**Description**: Person who creates and manages tasks, with preferences for notifications and reminders
**Fields**:
- id: UUID (Primary Key)
- email: String (required, unique)
- name: String (required)
- notification_preferences: JSONB (settings for email, push, in-app notifications)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)

**Validation Rules**:
- Email must be valid and unique
- Name must not be empty
- Notification preferences must follow defined schema

**Relationships**:
- Has many Tasks (one-to-many)
- Has many RecurringTaskTemplates (one-to-many)
- Has many AuditLogs (one-to-many)

## Entity: Notification
**Description**: Communication sent to users about tasks, due dates, and reminders
**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User)
- task_id: UUID (Foreign Key to Task, nullable for system notifications)
- type: Enum (email, push, in_app)
- title: String (required)
- message: Text (required)
- scheduled_at: DateTime (when to send)
- sent_at: DateTime (when sent, nullable)
- status: Enum (pending, sent, failed)
- created_at: DateTime (auto-generated)

**Validation Rules**:
- Type must be one of the defined values
- Title and message must not be empty
- Scheduled time must be in the future
- Status transitions must follow defined rules

**Relationships**:
- Belongs to one User
- Optionally belongs to one Task
- Belongs to one AuditLog (for tracking)

## Entity: AuditLog
**Description**: Record of all operations performed on tasks for compliance and debugging
**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User, nullable for system operations)
- entity_type: String (required, e.g., "Task", "RecurringTaskTemplate")
- entity_id: UUID (required, ID of the entity being audited)
- operation: Enum (create, update, delete, read)
- old_values: JSONB (previous state, nullable)
- new_values: JSONB (new state, nullable)
- timestamp: DateTime (auto-generated)
- metadata: JSONB (additional context)

**Validation Rules**:
- Entity type and ID must be provided
- Operation must be one of the defined values
- Timestamp is auto-generated

**Relationships**:
- Optionally belongs to one User
- Optionally belongs to one Notification (for notification audits)