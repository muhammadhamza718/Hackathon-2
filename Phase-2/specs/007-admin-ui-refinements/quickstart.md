# Quickstart: Admin Dashboard Testing

## Prerequisites

1. Backend running on localhost:8000
2. Frontend running on localhost:3000
3. One user with `role='admin'`
4. One user with `role='user'`

## Test Scenarios

### 1. Verify Admin Access

- Login as Admin.
- Check if "Admin" link appears in navbar.
- Navigate to `/admin/dashboard`.
- **Pass**: Dashboard loads with user list.

### 2. User Management

- Locate the test user account.
- Click "Change Role".
- Navigate to Database or Console log.
- **Pass**: User role changes in DB.

### 3. Task Deletion

- As test user, create 3 tasks.
- Login as Admin.
- View test user's task list.
- Click "Delete Task".
- Refresh page.
- **Pass**: Task is gone.
