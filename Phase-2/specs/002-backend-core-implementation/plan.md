# Implementation Plan: Backend Core Implementation and Admin Extension

**Branch**: `002-backend-core-implementation` | **Date**: 2025-12-12 | **Spec**: specs/002-backend-core-implementation/spec.md
**Input**: Feature specification from `/specs/002-backend-core-implementation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of the core backend functionality for the multi-user task management web application. This includes standard user endpoints for task management with strict user isolation, as well as admin extension endpoints for user and task oversight. The implementation follows stateless authentication patterns with JWT tokens and uses SQLModel for database operations with Neon Serverless PostgreSQL.

## Technical Context

**Language/Version**: Python 3.11+ (FastAPI)
**Primary Dependencies**: FastAPI, SQLModel, Better Auth with JWT Plugin, Neon Serverless PostgreSQL, python-jose[cryptography], passlib[bcrypt]
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend
**Target Platform**: Web application (API server with FastAPI backend)
**Project Type**: Web application (backend component with admin extension)
**Performance Goals**: <200ms API response time for standard operations
**Constraints**: Stateless authentication using JWT tokens, user data isolation, JWT token validation on all protected endpoints, role-based access for admin endpoints
**Scale/Scope**: Support for multiple concurrent users with proper data isolation and admin oversight capabilities

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Development Compliance
✅ **PASSED**: Following spec-driven development methodology by creating implementation plan based on feature specification in `specs/002-backend-core-implementation/spec.md`

### Monorepo Structure Compliance
✅ **PASSED**: Plan operates within existing monorepo structure with `backend/` directory as defined in constitution

### Stateless Authentication
✅ **PASSED**: Plan includes JWT token implementation using Better Auth with JWT Plugin, ensuring all API endpoints verify `Authorization: Bearer <token>` header and filter data by user_id

### Technology Stack Adherence
✅ **PASSED**: Plan uses Python FastAPI with SQLModel and Neon Serverless PostgreSQL as required by constitution

### Testable Implementation
✅ **PASSED**: Plan includes testing framework (pytest) and focuses on smallest viable diff approach

### Security-First Development
✅ **PASSED**: Plan includes stateless authentication, user data isolation, role-based admin access, and proper token validation to ensure security at every layer

### Architecture Validation
✅ **PASSED**: All architectural decisions align with the defined principles in the constitution

## Project Structure

### Documentation (this feature)
```text
specs/002-backend-core-implementation/
├── spec.md              # Feature requirements (/sp.specify command output)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (backend/)
```text
backend/
├── main.py              # FastAPI application entry point
├── core/
│   ├── auth.py          # JWT verification and middleware
│   ├── config.py        # Configuration settings
│   └── security.py      # Security utilities
├── models/
│   ├── user.py          # User model with role field
│   └── task.py          # Task model with user relationship
├── api/
│   ├── deps.py          # Dependency injection
│   ├── auth.py          # Auth endpoints
│   ├── tasks.py         # Standard task endpoints
│   └── admin.py         # Admin endpoints
├── db/
│   └── session.py       # Database session management
└── schemas/             # Pydantic schemas for request/response validation
    ├── user.py
    ├── task.py
    └── auth.py
```

**Structure Decision**: Backend follows FastAPI recommended project structure with clear separation of concerns. Models use SQLModel, API routes are separated by functionality, and schemas handle request/response validation using Pydantic v2.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phase 0: Research & Setup

### Research Tasks
- [ ] Research SQLModel relationship patterns for User-Task foreign key relationship with proper user isolation
- [ ] Investigate Better Auth JWT integration with FastAPI for user authentication and role verification
- [ ] Examine async session patterns for SQLModel with Neon Serverless PostgreSQL
- [ ] Review Pydantic v2 schema validation for request/response handling
- [ ] Analyze role-based access control implementation in FastAPI with JWT tokens

### Scaffolding Tasks
- [ ] Create backend directory structure (models, api, core, db, schemas)
- [ ] Set up database connection with Neon Serverless PostgreSQL
- [ ] Create base SQLModel models for User and Task entities
- [ ] Implement JWT authentication middleware
- [ ] Create Pydantic schemas for request/response validation
- [ ] Set up dependency injection for database sessions and current user

## Phase 1: Design & Contracts

### Data Model Tasks
- [ ] Create User model matching `specs/database/schema.md` with role field
- [ ] Create Task model matching `specs/database/schema.md` with user relationship
- [ ] Define User-Task relationship with proper foreign key constraint
- [ ] Implement user isolation at the model level with query helpers
- [ ] Add proper indexing for efficient queries

### API Contracts Tasks
- [ ] Create standard task endpoints matching `specs/api/rest-endpoints.md`
- [ ] Implement user isolation in all standard endpoints
- [ ] Create admin endpoints with role-based access control
- [ ] Define request/response schemas for all endpoints
- [ ] Implement proper error handling and status codes

### Design Tasks
- [ ] Generate `data-model.md` with User and Task entities, fields, and relationships
- [ ] Create API contracts in `/contracts/` directory based on functional requirements
- [ ] Generate `quickstart.md` with setup and run instructions
- [ ] Update agent context by running `.specify/scripts/bash/update-agent-context.sh claude`