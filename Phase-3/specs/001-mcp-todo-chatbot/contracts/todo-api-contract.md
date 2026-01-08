# API Contract: Todo Operations for MCP Server

## Overview
This document defines the API contract for todo operations that will be exposed via the MCP (Model Context Protocol) server. These operations will be accessible to the AI agent for performing todo management tasks.

## Todo Operations

### 1. Add Todo
- **Operation**: `todo.add`
- **Description**: Creates a new todo item
- **Input**:
  ```json
  {
    "content": "string (required) - The content of the todo item)",
    "due_date": "string (optional) - ISO 8601 formatted date string"
  }
  ```
- **Output**:
  ```json
  {
    "success": "boolean - Whether the operation was successful",
    "todo": {
      "id": "string - The unique ID of the created todo",
      "content": "string - The content of the todo item",
      "completed": "boolean - Whether the todo is completed (default: false)",
      "created_at": "string - ISO 8601 timestamp",
      "completed_at": "string - ISO 8601 timestamp (null if not completed)",
      "due_date": "string - ISO 8601 timestamp (null if not set)"
    },
    "error": "string (optional) - Error message if operation failed"
  }
  ```
- **Error Cases**:
  - Content is empty or only whitespace
  - Invalid date format for due_date
  - Database connection issues

### 2. List Todos
- **Operation**: `todo.list`
- **Description**: Retrieves all todo items for the user
- **Input**:
  ```json
  {
    "filter": {
      "status": "string (optional) - 'all', 'completed', or 'active' (default: 'all')",
      "limit": "integer (optional) - Maximum number of todos to return",
      "offset": "integer (optional) - Number of todos to skip"
    }
  }
  ```
- **Output**:
  ```json
  {
    "success": "boolean - Whether the operation was successful",
    "todos": [
      {
        "id": "string - The unique ID of the todo",
        "content": "string - The content of the todo item",
        "completed": "boolean - Whether the todo is completed",
        "created_at": "string - ISO 8601 timestamp",
        "completed_at": "string - ISO 8601 timestamp (null if not completed)",
        "due_date": "string - ISO 8601 timestamp (null if not set)"
      }
    ],
    "total_count": "integer - Total number of todos matching the filter",
    "error": "string (optional) - Error message if operation failed"
  }
  ```
- **Error Cases**:
  - Database connection issues

### 3. Complete Todo
- **Operation**: `todo.complete`
- **Description**: Marks a todo item as completed
- **Input**:
  ```json
  {
    "id": "string (required) - The ID of the todo to complete"
  }
  ```
- **Output**:
  ```json
  {
    "success": "boolean - Whether the operation was successful",
    "todo": {
      "id": "string - The unique ID of the todo",
      "content": "string - The content of the todo item",
      "completed": "boolean - Whether the todo is completed (true)",
      "created_at": "string - ISO 8601 timestamp",
      "completed_at": "string - ISO 8601 timestamp (current time)",
      "due_date": "string - ISO 8601 timestamp (null if not set)"
    },
    "error": "string (optional) - Error message if operation failed"
  }
  ```
- **Error Cases**:
  - Todo with given ID does not exist
  - Database connection issues

### 4. Delete Todo
- **Operation**: `todo.delete`
- **Description**: Removes a todo item
- **Input**:
  ```json
  {
    "id": "string (required) - The ID of the todo to delete"
  }
  ```
- **Output**:
  ```json
  {
    "success": "boolean - Whether the operation was successful",
    "deleted_id": "string - The ID of the deleted todo",
    "error": "string (optional) - Error message if operation failed"
  }
  ```
- **Error Cases**:
  - Todo with given ID does not exist
  - Database connection issues

### 5. Update Todo
- **Operation**: `todo.update`
- **Description**: Modifies the content of an existing todo item
- **Input**:
  ```json
  {
    "id": "string (required) - The ID of the todo to update",
    "content": "string (optional) - The new content of the todo item",
    "due_date": "string (optional) - New ISO 8601 formatted date string"
  }
  ```
- **Output**:
  ```json
  {
    "success": "boolean - Whether the operation was successful",
    "todo": {
      "id": "string - The unique ID of the todo",
      "content": "string - The updated content of the todo item",
      "completed": "boolean - Whether the todo is completed",
      "created_at": "string - ISO 8601 timestamp",
      "completed_at": "string - ISO 8601 timestamp (null if not completed)",
      "due_date": "string - Updated ISO 8601 timestamp (null if not set)"
    },
    "error": "string (optional) - Error message if operation failed"
  }
  ```
- **Error Cases**:
  - Todo with given ID does not exist
  - Content is empty or only whitespace (if provided)
  - Invalid date format for due_date (if provided)
  - Database connection issues

## Error Response Format
All operations follow this error response pattern:
```json
{
  "success": false,
  "error": "Descriptive error message",
  "error_code": "string - Standardized error code"
}
```

## Common Error Codes
- `TODO_NOT_FOUND`: The specified todo ID does not exist
- `INVALID_INPUT`: The input data is invalid
- `DATABASE_ERROR`: A database-related error occurred
- `VALIDATION_ERROR`: Input validation failed

## Implementation Notes
- All datetime fields should be in ISO 8601 format (e.g., "2023-12-30T10:00:00Z")
- The MCP server should handle authentication and authorization if needed in future extensions
- Operations should be idempotent where possible (e.g., completing an already completed todo should be safe)
- All operations should handle database connection issues gracefully