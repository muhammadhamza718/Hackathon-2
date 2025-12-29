# Data Model: Admin Dashboard Refinements

**Existing Models Used**:

## User (SQLModel)

- `id` (uuid, pk)
- `name` (str)
- `email` (str)
- `role` (str) - Used for Admin check
- `tasks` (Relationship)

## Task (SQLModel)

- `id` (uuid, pk)
- `title` (str)
- `description` (str)
- `completed` (bool)
- `user_id` (fk)
