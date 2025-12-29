# API REST Endpoints Specification

## Overview
This document defines the REST API endpoints for the task management application. All endpoints (except health checks) require JWT authentication via the `Authorization: Bearer <token>` header.

## Standard Routes

### 1. List Tasks
- **Method**: `GET`
- **Path**: `/api/tasks`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `200 OK`
    - Body: `[{id: string, title: string, description: string, completed: boolean, user_id: string}]`
  - Error: `401 Unauthorized` (invalid/missing token)
- **Description**: Returns all tasks for the authenticated user, filtered by user_id from JWT token.

### 2. Create Task
- **Method**: `POST`
- **Path**: `/api/tasks`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
  - `title: string`
  - `description: string` (optional)
- **Response**:
  - Success: `201 Created`
    - Body: `{id: string, title: string, description: string, completed: boolean, user_id: string}`
  - Error: `400 Bad Request` (invalid input)
  - Error: `401 Unauthorized` (invalid/missing token)
- **Description**: Creates a new task for the authenticated user.

### 3. Get Task
- **Method**: `GET`
- **Path**: `/api/tasks/{id}`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `200 OK`
    - Body: `{id: string, title: string, description: string, completed: boolean, user_id: string}`
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `404 Not Found` (task doesn't exist or doesn't belong to user)
- **Description**: Returns a specific task by ID if it belongs to the authenticated user.

### 4. Update Task
- **Method**: `PUT`
- **Path**: `/api/tasks/{id}`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
  - `title: string` (optional)
  - `description: string` (optional)
  - `completed: boolean` (optional)
- **Response**:
  - Success: `200 OK`
    - Body: `{id: string, title: string, description: string, completed: boolean, user_id: string}`
  - Error: `400 Bad Request` (invalid input)
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `404 Not Found` (task doesn't exist or doesn't belong to user)
- **Description**: Updates a specific task by ID if it belongs to the authenticated user.

### 5. Delete Task
- **Method**: `DELETE`
- **Path**: `/api/tasks/{id}`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `204 No Content`
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `404 Not Found` (task doesn't exist or doesn't belong to user)
- **Description**: Deletes a specific task by ID if it belongs to the authenticated user.

### 6. Toggle Task Completion
- **Method**: `PATCH`
- **Path**: `/api/tasks/{id}/complete`
- **Authentication**: Required (JWT Bearer Token)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `200 OK`
    - Body: `{id: string, title: string, description: string, completed: boolean, user_id: string}`
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `404 Not Found` (task doesn't exist or doesn't belong to user)
- **Description**: Toggles the completion status of a specific task if it belongs to the authenticated user.

## Admin Routes

### 1. List All Users
- **Method**: `GET`
- **Path**: `/api/admin/users`
- **Authentication**: Required (JWT Bearer Token)
- **Authorization**: Must have `role=admin`
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `200 OK`
    - Body: `[{id: string, email: string, name: string, role: string, created_at: timestamp}]`
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `403 Forbidden` (user does not have admin role)
- **Description**: Returns all users in the system (excluding sensitive information).

### 2. Get User's Tasks
- **Method**: `GET`
- **Path**: `/api/admin/users/{id}/tasks`
- **Authentication**: Required (JWT Bearer Token)
- **Authorization**: Must have `role=admin`
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Response**:
  - Success: `200 OK`
    - Body: `[{id: string, title: string, description: string, completed: boolean, user_id: string}]`
  - Error: `401 Unauthorized` (invalid/missing token)
  - Error: `403 Forbidden` (user does not have admin role)
  - Error: `404 Not Found` (user doesn't exist)
- **Description**: Returns all tasks for a specific user (admin only).

## Authentication
All endpoints (except health checks) require a valid JWT token in the `Authorization: Bearer <token>` header. The token must contain a `user_id` and `role` claim that will be used to filter data appropriately and enforce authorization.

For admin endpoints, the `role` claim must equal "admin".

## Error Handling
All endpoints should return appropriate HTTP status codes and JSON error responses:
- `400 Bad Request`: `{error: "Invalid input", details: string}`
- `401 Unauthorized`: `{error: "Authentication required"}`
- `403 Forbidden`: `{error: "Access denied"}`
- `404 Not Found`: `{error: "Resource not found"}`
- `500 Internal Server Error`: `{error: "Internal server error"}`