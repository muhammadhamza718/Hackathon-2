# Research: Admin Dashboard Refinements

**Feature**: `007-admin-ui-refinements`
**Status**: Completed

## Decisions

### Backend Framework

- **Decision**: Use FastAPI with SQLModel.
- **Rationale**: Consistent with existing project architecture. Provides async support and easy Type hints.

### Frontend UI Library

- **Decision**: Use Shadcn/UI + TailwindCSS.
- **Rationale**: Existing design system uses these tools. Ensures visual consistency.
- **Alternatives**: Material UI (rejected for inconsistent look).

### Authentication

- **Decision**: Verify `role='admin'` via Custom User field.
- **Rationale**: Simple RBAC implementation sufficient for current requirements.
