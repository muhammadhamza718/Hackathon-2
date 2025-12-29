# ADR-0002: Stateless Authentication Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-11
- **Feature:** 001-init-project-arch
- **Context:** Integrating Better Auth (Frontend) with FastAPI (Backend) for a full-stack application that requires user authentication and authorization with proper data isolation.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Use JWT (JSON Web Tokens) with a shared `BETTER_AUTH_SECRET` for stateless authentication between frontend and backend services. The authentication flow will be:
- Frontend handles user login via Better Auth
- JWT tokens are generated and stored client-side
- Tokens are transmitted to backend via `Authorization: Bearer <token>` header
- Backend verifies tokens and extracts user information for authorization and user isolation

- Token Standard: JWT with HS256 algorithm
- Secret Management: Shared BETTER_AUTH_SECRET environment variable
- Token Validation: Backend verifies JWT signature and extracts user claims
- User Isolation: All API endpoints filter data by user_id extracted from token

## Consequences

### Positive

- Backend remains stateless with no session lookup needed
- Enables independent scaling of frontend and backend services
- Strong user isolation with data filtered by user_id from token
- Supports cross-service authentication without shared session stores
- Reduces backend memory requirements for session storage
- Allows for token-based authorization checks across services

### Negative

- Tokens cannot be easily invalidated before expiration (require additional mechanisms like token blacklisting)
- Slightly larger request sizes due to token transmission
- Client-side token storage requires security considerations (XSS protection)
- Token expiration handling requires refresh token mechanisms
- Complexity in managing token security (secure transmission, storage)

## Alternatives Considered

Alternative A: Server-side sessions with shared session store
- Store session data in Redis or database
- Why rejected: Would require backend to maintain state, complicating scaling and adding dependency on shared session store

Alternative B: OAuth 2.0 with external provider only
- Rely on external providers like Google, GitHub for authentication
- Why rejected: Would limit user registration options and create vendor lock-in to specific providers

## References

- Feature Spec: F:/Courses/Hamza/Hackathon-2-Phase-1/Phase-2/specs/001-init-project-arch/spec.md
- Implementation Plan: F:/Courses/Hamza/Hackathon-2-Phase-1/Phase-2/specs/001-init-project-arch/plan.md
- Related ADRs: ADR-0001 (Monorepo Structure Strategy), ADR-0003 (Technology Stack Selection Phase 2)
- Evaluator Evidence: Project constitution requires stateless authentication approach
