# Authentication Feature Specification

## Overview
This document defines the authentication flows for the task management application using Better Auth with JWT Plugin.

## Authentication Flows

### Sign Up Flow
1. **Frontend**: User provides email and password on sign-up form
2. **Frontend**: Sends credentials to Better Auth `/api/auth/signup` endpoint
3. **Better Auth**: Creates new user in database with hashed password
4. **Better Auth**: Generates JWT token with user information (user_id, email)
5. **Better Auth**: Returns JWT token to frontend
6. **Frontend**: Stores JWT token securely (in memory or secure cookie)
7. **Frontend**: Redirects user to dashboard/home page

### Sign In Flow
1. **Frontend**: User provides email and password on sign-in form
2. **Frontend**: Sends credentials to Better Auth `/api/auth/signin` endpoint
3. **Better Auth**: Validates credentials against stored hash
4. **Better Auth**: Generates JWT token with user information (user_id, email)
5. **Better Auth**: Returns JWT token to frontend
6. **Frontend**: Stores JWT token securely (in memory or secure cookie)
7. **Frontend**: Redirects user to dashboard/home page

### Token Verification Middleware
1. **Backend**: All API endpoints (except health checks) require JWT verification
2. **Backend**: Extracts `Authorization: Bearer <token>` header from request
3. **Backend**: Verifies JWT signature using `BETTER_AUTH_SECRET`
4. **Backend**: Decodes JWT to extract `user_id` claim
5. **Backend**: Attaches `user_id` to request context for data filtering
6. **Backend**: If verification fails, returns `401 Unauthorized`
7. **Backend**: All database queries filter by `user_id` to ensure data isolation

## JWT Token Structure
- **Header**:
  - `alg`: "HS256" (algorithm)
  - `typ`: "JWT" (token type)
- **Payload**:
  - `user_id`: string (unique identifier for the user)
  - `email`: string (user's email address)
  - `exp`: number (expiration timestamp)
  - `iat`: number (issued at timestamp)
- **Secret**: `BETTER_AUTH_SECRET` environment variable

## Security Considerations
- JWT tokens must be signed with a strong secret (`BETTER_AUTH_SECRET`)
- Tokens should have a reasonable expiration time (e.g., 24 hours)
- All API requests must include the JWT in the `Authorization: Bearer <token>` header
- Backend must validate JWT signature before processing any request
- User data must be isolated by filtering all queries with the `user_id` from the token
- Frontend must securely store JWT tokens and include them in all API requests

## Error Handling
- `401 Unauthorized`: Invalid or missing JWT token
- `401 Unauthorized`: Expired JWT token
- `401 Unauthorized`: Invalid JWT signature