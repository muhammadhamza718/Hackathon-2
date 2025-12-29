# Admin API Contract

**Base URL**: `/api/admin`

## Endpoints

### DELETE /users/{user_id}

**Description**: Permanently delete a user account.
**Auth**: Admin required.
**Response**: 204 No Content.

### PATCH /users/{user_id}/role

**Description**: Update user role.
**Body**: `{ "role": "admin" | "user" }`
**Auth**: Admin required.
**Response**: 200 OK with User object.

### DELETE /users/{user_id}/tasks/{task_id}

**Description**: Delete a specific task.
**Auth**: Admin required.
**Response**: 204 No Content.
