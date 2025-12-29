# Research: Backend Core Implementation and Admin Extension

## Research Findings Summary

### SQLModel Relationship Patterns
**Decision**: Use SQLModel's relationship() function to establish User-Task foreign key relationship
**Rationale**: Provides automatic type hints, proper foreign key constraints, and efficient querying
**Implementation**:
- User model will have `tasks: List[Task] = Relationship(back_populates="user")`
- Task model will have `user: User = Relationship(back_populates="tasks")`
- Foreign key in Task: `user_id: str = Field(foreign_key="user.id")`

### Better Auth JWT Integration
**Decision**: Use Better Auth JWT Plugin with custom middleware for FastAPI
**Rationale**: Provides secure token generation and verification, integrates well with FastAPI's dependency injection
**Implementation**:
- Create `get_current_user` dependency that verifies JWT and extracts user info
- Create `get_current_admin` dependency that verifies JWT and checks role='admin'
- Use python-jose for JWT verification

### Async Session Patterns for Neon Serverless
**Decision**: Implement async session management with proper connection pooling
**Rationale**: Neon Serverless PostgreSQL works best with async patterns to handle connection scaling
**Implementation**:
- Create async database session factory
- Use FastAPI's dependency system to inject sessions into endpoints
- Implement proper session cleanup with context managers

### Pydantic v2 Schema Validation
**Decision**: Use Pydantic v2 for all request/response validation
**Rationale**: Better performance, more features, and consistency with FastAPI's native support
**Implementation**:
- Create separate schemas for Create, Read, Update operations
- Use Field validation for input constraints
- Implement proper serialization for database models

### Role-Based Access Control
**Decision**: Implement role-based access through JWT claims and middleware
**Rationale**: Stateless authentication with role information in token prevents database lookups
**Implementation**:
- Add role field to JWT token during authentication
- Create dependency functions to verify roles
- Use FastAPI's Security dependency with custom roles

## Alternatives Considered

### Alternative Relationship Implementation
- **Alternative**: Manual foreign key handling without SQLModel relationships
- **Rejected**: Would lose automatic type hints and query optimization benefits

### Alternative Authentication Approach
- **Alternative**: Server-side session storage with Redis
- **Rejected**: Violates stateless authentication requirement from constitution

### Alternative Role Handling
- **Alternative**: Database lookup for role verification on each request
- **Rejected**: Would create additional database queries and reduce performance
- **Chosen**: Include role in JWT token to keep verification stateless