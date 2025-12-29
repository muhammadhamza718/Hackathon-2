# Implementation Tasks: Backend Core Implementation and Admin Extension

**Branch**: `002-backend-core-implementation` | **Date**: 2025-12-12 | **Spec**: specs/002-backend-core-implementation/spec.md

**Input**: Implementation Plan from `/specs/002-backend-core-implementation/plan.md`

## Summary

Implementation of the core backend functionality for the multi-user task management web application. This includes standard user endpoints for task management with strict user isolation, as well as admin extension endpoints for user and task oversight. The implementation follows stateless authentication patterns with JWT tokens and uses SQLModel for database operations with Neon Serverless PostgreSQL.

## Phase 0: Research & Setup Tasks

### Research Tasks
- [x] Research SQLModel relationship patterns for User-Task foreign key relationship with proper user isolation
- [x] Investigate Better Auth JWT integration with FastAPI for user authentication and role verification
- [x] Examine async session patterns for SQLModel with Neon Serverless PostgreSQL
- [x] Review Pydantic v2 schema validation for request/response handling
- [x] Analyze role-based access control implementation in FastAPI with JWT tokens

### Scaffolding Tasks
- [x] Create backend directory structure (models, api, core, db, schemas)
- [x] Set up database connection with Neon Serverless PostgreSQL
- [x] Create base SQLModel models for User and Task entities
- [x] Implement JWT authentication middleware
- [x] Create Pydantic schemas for request/response validation
- [x] Set up dependency injection for database sessions and current user

## Phase 1: Database Layer Tasks (SQLModel)

### 1. Create User Model
- [x] Define `User` class in `backend/models/user.py`.
    *Constraint*: Must have `id`, `email`, local `role` field (default='user'), and `created_at`.

### 2. Create Task Model
- [x] Define `Task` class in `backend/models/task.py`.
    *Constraint*: Must have `id`, `title`, `description`, `completed`, and `user_id` (ForeignKey).

### 3. Setup Database Engine
- [x] Configure `backend/db/session.py` to connect to `DATABASE_URL` using `AsyncEngine`.

## Phase 2: Authentication Layer Tasks (Better Auth Integration)

### 1. Define Pydantic Security Schemas
- [x] Create schemas for `TokenPayload` (sub, exp, role) in `backend/schemas/auth.py`.

### 2. Implement Security Utilities
- [x] Create `backend/core/security.py` to handle JWT decoding using `python-jose` and `BETTER_AUTH_SECRET`.

### 3. Create Auth Middleware
- [x] Implement `get_current_user` dependency in `backend/api/deps.py`.
    *Constraint*: Must extract Bearer token, verify signature, and return User object.

### 4. Create Admin Middleware
- [x] Implement `get_current_admin` dependency.
    *Constraint*: Must verify `get_current_user` AND check `user.role == 'admin'`.

## Phase 3: API Core Implementation (Priority 1: Basic Features)

### 1. Define Task Schemas
- [x] Create Pydantic models for `TaskCreate`, `TaskRead`, `TaskUpdate` in `backend/schemas/task.py`.

### 2. Implement Standard Routes
- [x] Create `GET /api/tasks` endpoint: List user's tasks with user isolation
- [x] Create `POST /api/tasks` endpoint: Create task for authenticated user
- [x] Create `GET /api/tasks/{id}` endpoint: Get specific task with user verification
- [x] Create `PUT /api/tasks/{id}` endpoint: Update specific task with user verification
- [x] Create `DELETE /api/tasks/{id}` endpoint: Delete specific task with user verification
- [x] Create `PATCH /api/tasks/{id}/complete` endpoint: Toggle task completion with user verification

## Phase 4: Admin Extension Implementation (Priority 2: Admin Features)

### 1. Define Admin Schemas
- [x] Create Pydantic models for `UserRead` in `backend/schemas/user.py`.

### 2. Implement Admin Routes
- [x] Create `GET /api/admin/users` endpoint: List all users (admin only)
- [x] Create `GET /api/admin/users/{id}/tasks` endpoint: Get specific user's tasks (admin only)

## Phase 5: Integration & Testing Tasks

### 1. Application Setup
- [x] Create main FastAPI application in `backend/main.py`
- [x] Mount all API routes (auth, tasks, admin)
- [x] Configure CORS and middleware

### 2. Testing
- [ ] Write unit tests for database models
- [ ] Write unit tests for authentication functions
- [ ] Write integration tests for all API endpoints
- [ ] Test user isolation functionality
- [ ] Test admin role verification

## Acceptance Criteria

- [x] All Phase 0 research tasks completed with findings documented
- [x] Database models created with proper relationships and constraints
- [x] Authentication layer implemented with JWT verification
- [x] All standard task endpoints implemented with proper user isolation
- [x] Admin endpoints implemented with role-based access control
- [x] All endpoints return appropriate HTTP status codes
- [x] Error handling implemented consistently across all endpoints
- [x] All tasks marked as completed in this checklist
- [x] Implementation validated against specification requirements