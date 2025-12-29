# Backend Development Guidelines

## Python FastAPI with SQLModel

This project uses Python FastAPI with SQLModel for the backend. Follow these guidelines for backend development:

### Core Principles
- Use Async Session for SQLModel
- Require JWT Bearer Token for all non-public endpoints
- Use Pydantic v2 models for request/response validation

### Database Operations
- Use async sessions for all database operations
- Implement proper error handling for database connections
- Follow SQLModel best practices for model definitions

### Authentication & Security
- All API endpoints (except health checks) must verify JWT tokens
- Extract user_id from JWT token for data isolation
- Validate Authorization: Bearer <token> header format
- Return 401 Unauthorized for invalid/missing tokens

### API Development
- Use Pydantic v2 models for request/response validation
- Implement proper HTTP status codes
- Follow REST API best practices
- Include comprehensive error responses

### Performance & Scalability
- Use async/await for I/O operations
- Implement proper connection pooling for database
- Cache frequently accessed data when appropriate
- Optimize database queries with proper indexing