# Database Schema Specification

## Overview
This document defines the database schema for the task management application using SQLModel with Neon Serverless PostgreSQL.

## Entities

### User Entity
- **Table Name**: `user`
- **Fields**:
  - `id`: string (primary key, auto-generated)
  - `email`: string (unique, not null)
  - `name`: string (nullable)
  - `role`: string (default: "user")
  - `created_at`: timestamp (default: current timestamp)
  - `updated_at`: timestamp (default: current timestamp, updates on change)

### Task Entity
- **Table Name**: `task`
- **Fields**:
  - `id`: string (primary key, auto-generated)
  - `title`: string (not null)
  - `description`: string (nullable)
  - `completed`: boolean (default: false)
  - `user_id`: string (foreign key referencing `user.id`, not null)
  - `created_at`: timestamp (default: current timestamp)
  - `updated_at`: timestamp (default: current timestamp, updates on change)

## Relationships
- One User to Many Tasks (one-to-many)
- Foreign Key Constraint: `task.user_id` references `user.id`
- Cascade Delete: When a User is deleted, all their Tasks are also deleted

## Indexes
- `user.email`: Unique index for fast email lookups
- `task.user_id`: Index for fast user-based filtering
- `task.created_at`: Index for sorting tasks by creation date

## Constraints
- `user.email`: Must be unique and follow email format
- `task.title`: Must not be empty
- `task.status`: Must be either "pending" or "completed"
- `task.user_id`: Must reference an existing user (foreign key constraint)

## Example SQL
```sql
CREATE TABLE "user" (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "task" (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at);
CREATE UNIQUE INDEX idx_user_email ON "user"(email);
```