# Feature Specification: Backend Core Implementation (002-backend-core-implementation)

## Overview
This feature implements the core backend functionality for the multi-user task management web application. The implementation follows the Phase II Basic Level Requirements with an extension for Admin support. The system will provide a secure, multi-user environment with stateless authentication and user data isolation.

## Feature Requirements

### Priority 1: Core Project Requirements (MUST HAVE)

#### Context
Transform console app into multi-user web app with stateless authentication. The system must support multiple concurrent users with proper data isolation.

#### Database Schema
- **User Table** (Managed by Better Auth):
  - `id`: string (primary key, auto-generated)
  - `email`: string (unique, not null)
  - `name`: string (nullable)
  - `created_at`: timestamp (default: current timestamp)
  - `role`: string (default: 'user', for admin extension)

- **Task Table**:
  - `id`: string (primary key, auto-generated)
  - `title`: string (not null)
  - `description`: string (nullable)
  - `completed`: boolean (default: false)
  - `user_id`: string (foreign key referencing `user.id`, not null)
  - `created_at`: timestamp (default: current timestamp)
  - `updated_at`: timestamp (default: current timestamp, updates on change)

#### Security Requirements (User Isolation)
- **Strict Rule**: Users can ONLY see/edit their own tasks
- **Implementation**: Verify JWT matches `user_id` in route handler or implicitly filter queries by `current_user.id`
- **JWT Verification**: All protected endpoints must validate the `Authorization: Bearer <token>` header
- **Data Filtering**: Database queries must filter by the authenticated user's ID to ensure data isolation

#### Standard Endpoints (The 5 Basic Features)
1. **List Tasks** (`GET /api/tasks`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Return all tasks belonging to the authenticated user
   - Response: Array of user's tasks

2. **Create Task** (`POST /api/tasks`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Create a new task for the authenticated user
   - Response: Created task object with user_id set to authenticated user

3. **Get Task Details** (`GET /api/tasks/{id}`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Retrieve details of a specific task if it belongs to the authenticated user
   - Response: Task object if user owns the task, 404 otherwise

4. **Update Task** (`PUT /api/tasks/{id}`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Update a specific task if it belongs to the authenticated user
   - Response: Updated task object if user owns the task, 404 otherwise

5. **Delete Task** (`DELETE /api/tasks/{id}`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Delete a specific task if it belongs to the authenticated user
   - Response: 204 No Content if successful, 404 if task doesn't exist or belong to user

6. **Toggle Task Completion** (`PATCH /api/tasks/{id}/complete`)
   - Authentication: Required (JWT Bearer Token)
   - Function: Toggle the completion status of a specific task if it belongs to the authenticated user
   - Response: Updated task object with toggled completion status

### Priority 2: Admin Extension (NICE TO HAVE)

#### Context
Support a future "Admin Dashboard" in Next.js with minimal administrative capabilities.

#### Admin Extension Requirements
- **Role Field**: Add `role` field to User table with default value 'user'
- **Admin Protection**: All admin endpoints require `role=admin` check
- **Minimal Implementation**: Only implement essential admin functionality for dashboard

#### Admin Endpoints
1. **List All Users** (`GET /api/admin/users`)
   - Authentication: Required (JWT Bearer Token)
   - Authorization: Must have `role=admin`
   - Function: Return list of all users in the system
   - Response: Array of all users (excluding sensitive information)

2. **View User's Tasks** (`GET /api/admin/users/{id}/tasks`)
   - Authentication: Required (JWT Bearer Token)
   - Authorization: Must have `role=admin`
   - Function: Return all tasks for a specific user
   - Response: Array of tasks belonging to the specified user

## Success Criteria
- [ ] All standard endpoints implement proper user isolation
- [ ] JWT authentication is validated on all protected endpoints
- [ ] Admin endpoints are protected by role-based access control
- [ ] Database schema includes the role field for users
- [ ] All endpoints return appropriate HTTP status codes
- [ ] Error handling is consistent across all endpoints
- [ ] Tasks can only be accessed by their owner (except by admins)

## Out of Scope
- Advanced admin features beyond the specified endpoints
- User management capabilities (create, delete, modify users)
- Complex reporting or analytics
- Real-time notifications
- File attachments or complex task relationships

## Dependencies
- Better Auth for user management and JWT generation
- SQLModel for database modeling and ORM
- Neon Serverless PostgreSQL for data storage
- FastAPI for API framework and automatic documentation

## Performance Requirements
- API endpoints should respond within 200ms under normal load
- Database queries should be optimized with proper indexing
- JWT verification should be efficient and secure

## Security Requirements
- All user data must be properly isolated
- JWT tokens must be validated with proper secret
- Admin endpoints must have role-based access control
- Input validation must be implemented on all endpoints