# Implementation Plan: Auth Integration with Better Auth

**Feature**: 004-auth-integration
**Created**: 2025-12-13
**Status**: Draft
**Author**: Claude Code

## Overview

This plan outlines the implementation of Better Auth JWT authentication in the Phase 2 Todo Full-Stack Web Application, replacing mock authentication with production-ready user signup/signin using JWT tokens.

## Architecture Summary

- Better Auth runs ON Next.js frontend (creates JWT tokens)
- Backend ONLY verifies JWT tokens (never creates them)
- JWT tokens passed via HTTP-only cookies
- Shared secret (BETTER_AUTH_SECRET) between frontend and backend

## Critical Architecture Points (Updated)

1. **JWT Creation Location**: Better Auth creates JWT tokens on Next.js frontend (NOT backend)
2. **Backend Role**: Backend ONLY verifies tokens using shared secret
3. **API Flow**: Frontend calls /api/auth/* on Next.js (NOT backend /api/auth/*)
4. **Token Flow**: Backend receives tokens via Authorization: Bearer header from frontend API calls
5. **Secret Consistency**: BETTER_AUTH_SECRET must be IDENTICAL in both frontend and backend .env files

## Implementation Tasks

### Phase 1: Environment Setup and Dependencies

#### Task 1.1: Install Better Auth Dependencies
**Component**: Frontend
**Files**: package.json, frontend/requirements.txt (if exists)
**Effort**: Low
**Dependencies**: None

**Description**: Install Better Auth packages in the frontend

**Implementation Steps**:
1. Run: `cd frontend && npm install better-auth @better-auth/react`
2. Run: `npm install @types/node --save-dev` (for TypeScript types)
3. Verify packages are added to package.json

**Acceptance Criteria**:
- [ ] Better Auth packages installed successfully
- [ ] Package.json updated with better-auth and @better-auth/react
- [ ] TypeScript types available for development

#### Task 1.2: Generate and Configure Environment Variables
**Component**: Frontend & Backend
**Files**: frontend/.env.local, backend/.env
**Effort**: Low
**Dependencies**: None

**Description**: Set up shared secrets and database connections

**Implementation Steps**:
1. Generate BETTER_AUTH_SECRET: `openssl rand -base64 32`
2. Create frontend/.env.local with required variables
3. Update backend/.env to match BETTER_AUTH_SECRET
4. Ensure both services use same DATABASE_URL
5. Configure CORS on backend with allow_credentials=True for cookie support

**Acceptance Criteria**:
- [ ] BETTER_AUTH_SECRET is identical in both frontend and backend
- [ ] Frontend has NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
- [ ] Frontend has NEXT_PUBLIC_API_URL=http://localhost:8000
- [ ] Backend has CORS configured with allow_credentials=True to support HTTP-only cookies
- [ ] Both services can connect to Neon PostgreSQL database

#### Task 1.3: Run Better Auth Database Migrations
**Component**: Frontend
**Files**: N/A (database schema)
**Effort**: Low
**Dependencies**: Task 1.2

**Description**: Create Better Auth tables in the database

**Implementation Steps**:
1. Run: `cd frontend && npx better-auth migrate`
2. Verify user, session, and account tables are created
3. Confirm tables use the same database as backend
4. Verify that user table has id, email, name, password_hash columns
5. Verify that session table has id, user_id, expires_at columns

**Acceptance Criteria**:
- [ ] Better Auth user table created with id, email, name, password_hash
- [ ] Better Auth session table created with id, user_id, expires_at
- [ ] Account table created (for future OAuth support)
- [ ] Tables accessible by both frontend (Better Auth) and backend (for user_id reference)
- [ ] Backend can read user.id for task relationships but does not modify Better Auth tables

### Phase 2: Frontend Authentication Setup

#### Task 2.1: Create Better Auth Server Instance
**Component**: Frontend
**Files**: frontend/lib/auth.ts
**Effort**: Medium
**Dependencies**: Task 1.2

**Description**: Set up server-side Better Auth instance

**Implementation Steps**:
1. Create frontend/lib/auth.ts file
2. Configure Better Auth with database connection
3. Enable email/password authentication
4. Configure JWT with 7-day expiry
5. Set up HTTP-only session cookies
6. Ensure JWT tokens are created on frontend (not sent to backend)

**Acceptance Criteria**:
- [ ] Server-side auth instance created and exported
- [ ] Connected to Neon PostgreSQL database via DATABASE_URL
- [ ] Email/password provider enabled
- [ ] JWT tokens configured with 7-day expiry
- [ ] Session stored in HTTP-only cookie for security
- [ ] JWT creation happens on frontend only (not sent to backend)

#### Task 2.2: Create Better Auth API Routes
**Component**: Frontend
**Files**: frontend/app/api/auth/[...all]/route.ts
**Effort**: Low
**Dependencies**: Task 2.1

**Description**: Mount Better Auth API endpoints

**Implementation Steps**:
1. Create frontend/app/api/auth/[...all]/route.ts
2. Import auth instance from lib/auth
3. Use toNextJsHandler to create GET/POST handlers
4. Verify routes are accessible at /api/auth/*
5. Confirm these routes handle authentication on frontend, not backend

**Acceptance Criteria**:
- [ ] Better Auth routes mounted at /api/auth/* on frontend
- [ ] Sign-in endpoint available at POST /api/auth/signin on frontend
- [ ] Sign-up endpoint available at POST /api/auth/signup on frontend
- [ ] Sign-out endpoint available at POST /api/auth/signout on frontend
- [ ] JWT tokens created on frontend (not sent to backend)

#### Task 2.3: Create Better Auth Client
**Component**: Frontend
**Files**: frontend/lib/auth-client.ts
**Effort**: Low
**Dependencies**: Task 1.2

**Description**: Set up client-side Better Auth client

**Implementation Steps**:
1. Create frontend/lib/auth-client.ts file
2. Initialize createAuthClient with BASE_URL
3. Export useSession, signIn, signUp, signOut hooks
4. Ensure client communicates with frontend auth endpoints, not backend

**Acceptance Criteria**:
- [ ] Client-side auth client created
- [ ] Points to NEXT_PUBLIC_BETTER_AUTH_URL (frontend endpoint)
- [ ] Exports necessary hooks: useSession, signIn, signUp, signOut
- [ ] Client communicates with frontend, not backend

#### Task 2.4: Create Authentication Context
**Component**: Frontend
**Files**: frontend/contexts/AuthContext.tsx, frontend/app/layout.tsx
**Effort**: Medium
**Dependencies**: Task 2.3

**Description**: Create authentication context provider for global state

**Implementation Steps**:
1. Create frontend/contexts/AuthContext.tsx
2. Implement AuthProvider with user, isLoading, error state
3. Create useAuth hook to access context
4. Wrap entire app in AuthProvider in root layout
5. Ensure context only accesses frontend auth state, not backend

**Acceptance Criteria**:
- [ ] AuthContext created with user, isLoading, error
- [ ] useAuth() hook available to all components
- [ ] AuthProvider wraps entire app in root layout
- [ ] Context properly handles session loading states from frontend
- [ ] No direct communication with backend for auth state

### Phase 3: Frontend Authentication UI Integration

#### Task 3.1: Update Sign-In Page
**Component**: Frontend
**Files**: frontend/app/auth/signin/page.tsx
**Effort**: Medium
**Dependencies**: Task 2.3

**Description**: Replace mock authentication with Better Auth sign-in

**Implementation Steps**:
1. Remove localStorage mock authentication code
2. Import signIn from auth-client
3. Implement signIn.email() with proper error handling
4. Add loading states and form validation
5. Redirect to dashboard on successful sign-in
6. Verify JWT token is created on frontend and stored in HTTP-only cookie

**Acceptance Criteria**:
- [ ] Mock localStorage code removed
- [ ] Real Better Auth signIn.email() implemented
- [ ] Error handling displays user-friendly messages
- [ ] Loading state prevents double submissions
- [ ] Successful sign-in redirects to /dashboard
- [ ] JWT token created on frontend (not sent to backend)

#### Task 3.2: Update Sign-Up Page
**Component**: Frontend
**Files**: frontend/app/auth/signup/page.tsx
**Effort**: Medium
**Dependencies**: Task 2.3

**Description**: Replace mock authentication with Better Auth sign-up

**Implementation Steps**:
1. Remove mock authentication logic
2. Import signUp from auth-client
3. Implement signUp.email() with name, email, password
4. Add password validation (min 8 chars)
5. Implement proper error handling
6. Redirect to dashboard on successful sign-up
7. Verify JWT token is created on frontend and stored in HTTP-only cookie

**Acceptance Criteria**:
- [ ] Real Better Auth signUp.email() implemented
- [ ] Password validation (min 8 chars) enforced
- [ ] Error handling for duplicate email
- [ ] Successful sign-up auto-signs in and redirects to /dashboard
- [ ] JWT token created on frontend (not sent to backend)

#### Task 3.3: Update API Client for Token Handling
**Component**: Frontend
**Files**: frontend/lib/api.ts
**Effort**: Medium
**Dependencies**: Task 2.3

**Description**: Replace mock token with Better Auth session token

**Implementation Steps**:
1. Remove localStorage token retrieval
2. Implement getAuthToken() using authClient.getSession()
3. Update all API calls to use Authorization: Bearer token
4. Add 401 error handling for expired/invalid tokens
5. Update all CRUD operations (GET, POST, PUT, DELETE, PATCH)
6. Ensure tokens are retrieved from frontend auth and sent to backend for verification

**Acceptance Criteria**:
- [ ] localStorage token retrieval removed
- [ ] Real token fetched from authClient.getSession() (from frontend)
- [ ] Token attached to all API requests in Authorization header
- [ ] 401 errors throw specific "Unauthorized" error
- [ ] All CRUD operations updated with proper authentication
- [ ] JWT tokens created on frontend and sent to backend for verification only

### Phase 4: Security and Route Protection

#### Task 4.1: Implement Route Protection Middleware
**Component**: Frontend
**Files**: frontend/middleware.ts
**Effort**: Medium
**Dependencies**: Task 2.1

**Description**: Create middleware to protect authenticated routes

**Implementation Steps**:
1. Create frontend/middleware.ts
2. Implement session checking using auth.api.getSession() (frontend)
3. Define protected routes: /dashboard, /tasks, /profile
4. Define auth routes: /auth/signin, /auth/signup
5. Redirect logic for authenticated/unauthenticated users
6. Ensure middleware checks frontend session, not backend

**Acceptance Criteria**:
- [ ] Middleware intercepts protected routes
- [ ] Unauthenticated users redirected to /auth/signin
- [ ] Authenticated users can't access auth pages (redirect to /dashboard)
- [ ] Session checked server-side on frontend for security
- [ ] No communication with backend required for route protection

#### Task 4.2: Verify Backend JWT Verification
**Component**: Backend
**Files**: backend/middleware/auth.py, backend/main.py
**Effort**: Low
**Dependencies**: Task 1.2

**Description**: Confirm backend is properly verifying JWT tokens

**Implementation Steps**:
1. Verify JWT verification middleware exists in backend/middleware/auth.py
2. Confirm middleware extracts user_id from JWT payload
3. Verify all API endpoints filter data by authenticated user
4. Check BETTER_AUTH_SECRET matches frontend
5. Ensure backend only verifies tokens, never creates them

**Acceptance Criteria**:
- [ ] JWT verification middleware exists and functional
- [ ] Middleware properly extracts user_id from JWT (created by frontend)
- [ ] All /api/{user_id}/* endpoints filter by authenticated user
- [ ] BETTER_AUTH_SECRET matches frontend configuration
- [ ] Backend only verifies tokens (does not create new ones)

### Phase 5: Testing and Validation

#### Task 5.1: Manual Testing - Authentication Flows
**Component**: Frontend & Backend
**Files**: N/A (testing)
**Effort**: Medium
**Dependencies**: All previous tasks

**Description**: Test all authentication flows manually

**Implementation Steps**:
1. Test sign-up flow: valid inputs → user creation → auto-sign-in → redirect
2. Test sign-in flow: valid credentials → sign-in → redirect
3. Test error cases: invalid credentials, duplicate email, network failures
4. Test session persistence: refresh page, close/reopen browser
5. Test route protection: unauthenticated access, authenticated access
6. Verify JWT is created on frontend and used for backend API calls

**Acceptance Criteria**:
- [ ] Sign-up flow works: creates user, auto-signs in, redirects to dashboard
- [ ] Sign-in flow works: validates credentials, signs in, redirects
- [ ] Error cases handled gracefully with user-friendly messages
- [ ] Session persists across page refreshes and browser restarts
- [ ] Route protection works: unauthenticated users redirected to sign-in
- [ ] JWT tokens are created on frontend, not backend

#### Task 5.2: API Integration Testing
**Component**: Frontend & Backend
**Files**: N/A (testing)
**Effort**: Medium
**Dependencies**: Task 5.1

**Description**: Test API calls with authentication tokens

**Implementation Steps**:
1. Sign in as user A and create tasks
2. Verify Authorization header includes JWT token (from frontend)
3. Test multi-user isolation: User A can't see User B's tasks
4. Test 401 handling: expired/invalid tokens redirect to sign-in
5. Verify backend properly validates tokens (created by frontend) and filters by user_id
6. Confirm backend only verifies tokens, never creates new ones

**Acceptance Criteria**:
- [ ] API requests include Authorization: Bearer <token> header (token from frontend)
- [ ] Backend successfully verifies JWT tokens (created by frontend)
- [ ] Data is properly filtered by authenticated user_id
- [ ] 401 responses trigger proper error handling and redirects
- [ ] Multi-user isolation enforced (User A can't access User B's data)
- [ ] Backend only verifies tokens (does not create new ones)

#### Task 5.3: Database Verification
**Component**: Database
**Files**: N/A (database)
**Effort**: Low
**Dependencies**: Task 5.1

**Description**: Verify database records are created and linked correctly

**Implementation Steps**:
1. Check user table: verify users created via sign-up (via frontend Better Auth)
2. Check session table: verify active sessions (via frontend Better Auth)
3. Check tasks table: verify user_id foreign key relationships (via backend)
4. Verify data isolation: tasks properly linked to correct users
5. Confirm Better Auth tables are managed by frontend, task table by backend

**Acceptance Criteria**:
- [ ] Users created via sign-up appear in user table with correct fields (via frontend)
- [ ] Active sessions appear in session table with correct user_id (via frontend)
- [ ] Tasks are correctly linked to user_id foreign key (via backend)
- [ ] No cross-user data leakage in database
- [ ] Clear separation: Better Auth tables (user, session) managed by frontend, tasks by backend

## Risk Analysis

### High-Risk Items
1. **Secret Mismatch**: BETTER_AUTH_SECRET must be identical in frontend and backend
2. **Database Connection**: Both services must connect to the same Neon PostgreSQL instance
3. **CORS Configuration**: Backend must allow credentials from frontend origin for cookie support
4. **Architecture Violation**: Backend might accidentally try to create JWT tokens instead of verifying them

### Mitigation Strategies
1. Use the same environment configuration script for both services
2. Verify database connection before starting auth implementation
3. Test CORS configuration early in the process with allow_credentials=True
4. Review backend code to ensure it only verifies tokens, never creates them

## Success Criteria

### Functional Requirements
- [ ] Users can sign up with email/password → Creates user record in database via frontend
- [ ] Users can sign in with valid credentials → Receives JWT in cookie from frontend
- [ ] Invalid credentials show appropriate error messages
- [ ] Authenticated users can access /dashboard and see their tasks
- [ ] Unauthenticated users redirected to /auth/signin when accessing protected routes
- [ ] All API calls include JWT token (from frontend) in Authorization header
- [ ] Backend successfully verifies JWT (created by frontend) and filters data by user_id
- [ ] Session persists across page refreshes (7-day expiry)
- [ ] User A cannot access User B's tasks (enforced by backend)

### Non-Functional Requirements
- [ ] Authentication flow completes in under 2 seconds
- [ ] Session cookies are HTTP-only for XSS protection
- [ ] JWT tokens expire after 7 days of inactivity
- [ ] Error handling provides clear feedback to users
- [ ] No sensitive information stored in client-side storage
- [ ] Backend only verifies tokens (does not create new ones)

## Out of Scope
- Password reset functionality
- Email verification
- Social authentication (Google, GitHub)
- Two-factor authentication
- Remember me functionality (already implemented with 7-day session)
- Custom JWT claims beyond user_id