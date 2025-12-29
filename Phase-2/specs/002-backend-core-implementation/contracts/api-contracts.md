# API Contracts: Backend Core Implementation and Admin Extension

## Overview
This document defines the API contracts for the backend implementation, mapping directly to the specifications in `specs/api/rest-endpoints.md`.

## Standard User Endpoints

### 1. List User's Tasks
- **Endpoint**: `GET /api/tasks`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User can only access their own tasks
- **Request**:
  - Headers: `Authorization: Bearer <token>`
- **Response**:
  - 200 OK: `[{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}]`
  - 401 Unauthorized: `{error: "Authentication required"}`
- **Validation**:
  - Token must be valid JWT
  - User must exist in database

### 2. Create Task
- **Endpoint**: `POST /api/tasks`
- **Authentication**: JWT Bearer Token required
- **Authorization**: Task is assigned to authenticated user
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Body: `{title: string, description?: string}`
- **Response**:
  - 201 Created: `{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}`
  - 400 Bad Request: `{error: "Invalid input", details: string}`
  - 401 Unauthorized: `{error: "Authentication required"}`
- **Validation**:
  - Title is required and 1-255 characters
  - Description is optional and max 1000 characters

### 3. Get Task Details
- **Endpoint**: `GET /api/tasks/{id}`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must own the task
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Path: `id` (task ID)
- **Response**:
  - 200 OK: `{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}`
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 404 Not Found: `{error: "Task not found"}`
- **Validation**:
  - Task ID must exist
  - Task must belong to authenticated user

### 4. Update Task
- **Endpoint**: `PUT /api/tasks/{id}`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must own the task
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Path: `id` (task ID)
  - Body: `{title?: string, description?: string, completed?: boolean}`
- **Response**:
  - 200 OK: `{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}`
  - 400 Bad Request: `{error: "Invalid input", details: string}`
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 404 Not Found: `{error: "Task not found"}`
- **Validation**:
  - Task ID must exist
  - Task must belong to authenticated user
  - Title is 1-255 characters if provided

### 5. Delete Task
- **Endpoint**: `DELETE /api/tasks/{id}`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must own the task
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Path: `id` (task ID)
- **Response**:
  - 204 No Content
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 404 Not Found: `{error: "Task not found"}`
- **Validation**:
  - Task ID must exist
  - Task must belong to authenticated user

### 6. Toggle Task Completion
- **Endpoint**: `PATCH /api/tasks/{id}/complete`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must own the task
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Path: `id` (task ID)
- **Response**:
  - 200 OK: `{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}`
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 404 Not Found: `{error: "Task not found"}`
- **Validation**:
  - Task ID must exist
  - Task must belong to authenticated user

## Admin Endpoints

### 1. List All Users
- **Endpoint**: `GET /api/admin/users`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must have `role=admin`
- **Request**:
  - Headers: `Authorization: Bearer <token>`
- **Response**:
  - 200 OK: `[{id: string, email: string, name: string, role: string, created_at: datetime}]`
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 403 Forbidden: `{error: "Access denied"}`
- **Validation**:
  - User must have admin role
  - Token must be valid JWT

### 2. Get User's Tasks
- **Endpoint**: `GET /api/admin/users/{id}/tasks`
- **Authentication**: JWT Bearer Token required
- **Authorization**: User must have `role=admin`
- **Request**:
  - Headers: `Authorization: Bearer <token>`
  - Path: `id` (user ID)
- **Response**:
  - 200 OK: `[{id: string, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime}]`
  - 401 Unauthorized: `{error: "Authentication required"}`
  - 403 Forbidden: `{error: "Access denied"}`
  - 404 Not Found: `{error: "User not found"}`
- **Validation**:
  - User must have admin role
  - Target user ID must exist
  - Token must be valid JWT

## Common Headers
- `Authorization: Bearer <token>` (for all protected endpoints)
- `Content-Type: application/json` (for POST/PUT/PATCH requests)

## Common Error Responses
- `400 Bad Request`: `{error: "Invalid input", details: string}`
- `401 Unauthorized`: `{error: "Authentication required"}`
- `403 Forbidden`: `{error: "Access denied"}`
- `404 Not Found`: `{error: "Resource not found"}`
- `500 Internal Server Error`: `{error: "Internal server error"}`

## Security Requirements
- All endpoints (except health checks) require JWT token verification
- Standard endpoints enforce user isolation (user can only access their own data)
- Admin endpoints require role=admin verification
- All sensitive data is filtered out of responses (e.g., passwords, tokens)