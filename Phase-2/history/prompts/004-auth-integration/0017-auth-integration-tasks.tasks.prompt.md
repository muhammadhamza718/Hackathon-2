---
id: 3
title: auth-integration-tasks
stage: tasks
date: 2025-12-13
surface: agent
model: qwen3-coder-plus
feature: 004-auth-integration
branch: main
user: Claude Code
command: /sp.tasks
labels: ["authentication", "better-auth", "jwt", "tasks", "planning"]
links:
  spec: ../../specs/004-auth-integration/spec.md
  plan: ../../specs/004-auth-integration/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-auth-integration/tasks.md
tests:
 - null
---

## Prompt

**Feature**: Auth Integration with Better Auth
**Goal**: Break down the implementation plan into granular, executable tasks for implementing Better Auth JWT authentication in the Phase 2 Todo application.
**Context**:
- Implementation plan already created: @Phase-2/specs/004-auth-integration/plan.md
- Source specifications:
  - @Phase-2/specs/004-auth-integration/spec.md
  - @Phase-2/specs/005-fix-auth-flow/spec.md
- Monorepo structure: frontend/ (Next.js 16+) and backend/ (FastAPI)
- Database: Neon Serverless PostgreSQL (shared)
**Task Structure Requirements**:
Each task should include:
1. **Task ID**: Unique identifier (e.g., AUTH-001)
2. **Task Name**: Clear, action-oriented title
3. **Description**: What needs to be done and why
4. **Component**: Frontend, Backend, Database, or Docs
5. **Files to Create/Modify**: Exact file paths
6. **Dependencies**: Which tasks must l
- Implement token refresh logic if needed
- Add 401 error handling
- Test all CRUD operations with real auth
### Phase 6: Route Protection (Frontend)
- Create middleware.ts for route protection
- Protect dashboard, tasks, profile routes
- Redirect authenticated users away from auth pages
- Test route protection scenarios
### Phase 7: User ID Integration (Frontend)
- Update AuthContext to expose userId
- Update dashboard to use userId for API calls
- Update task pages to use userId
- Test multi-user task isolation
### Phase 8: Backend Verification (Backend)
- Verify JWT middleware exists and works
- Verify CORS configuration includes allow_credentials=True
- Test backend JWT verification with real tokens
- Test user_id extraction from JWT
### Phase 9: Integration Testing
- End-to-end sign-up flow
- End-to-end sign-in flow
- Session persistence across page refresh
- Token expiry and error handling
- Multi-user task isolation
- All API endpoints with authentication
### Phase 10: Documentation & Cleanup
- Update CLAUDE.md files if needed
- Document environment setup
- Create troubleshooting guide
- Remove any mock auth code
**Task Granularity**:
- Each task should take 15-45 minutes to implement
- If a task seems larger, break it into sub-tasks
- Tasks should be independently testable when possible
- Avoid tasks that modify too many files at once
**Dependency Rules**:
- Infrastructure tasks must come first
- Better Auth setup before authentication pages
- AuthContext before using useAuth() in pages
- API client updates before route protection
- All implementation before integration testing
**Acceptance Criteria Guidelines**:
Each task's acceptance criteria should be:
- **Specific**: Exact condition to verify (not "auth works")
- **Testable**: Can be checked programmatically or manually
- **Observable**: Clear pass/fail outcome
- **Measurable**: Quantifiable when possible
Good examples:
- ✅ "Running `npm run build` completes without errors"
- ✅ "POST /api/auth/signin returns 200 with valid credentials"
- ✅ "Unauthenticated user visiting /dashboard redirects to /auth/signin"
- ✅ "User table exists in database with 4 columns: id, email, name, password_hash"
Bad examples:
- ❌ "Auth is set up"
- ❌ "Everything works"
- ❌ "Users can log in"
**File Path Format**:
Use absolute paths from project root:
- Frontend: `frontend/lib/auth.ts`
- Backend: `backend/middleware/auth.py`
- Root: `.env`, `docker-compose.yml`
**Effort Estimation Key**:
- **XS** (5-15 min): Single file, simple config change
- **S** (15-30 min): Single file, moderate logic
- **M** (30-60 min): Multiple files, integration required
- **L** (1-2 hours): Complex logic, multiple integrations
- **XL** (2+ hours): Major refactor or system-wide change
**Special Considerations**:
1. **Environment Variables**:
   - BETTER_AUTH_SECRET must be IDENTICAL in frontend and backend
   - Generate secret using: `openssl rand -base64 32`
   - Task should include secret generation step
2. **Database Migrations**:
   - Better Auth migration creates: user, session, account tables
   - Backend must create: tasks table separately
   - Verify foreign key: tasks.user_id → user.id
3. **CORS Configuration**:
   - Must have `allow_credentials=True` for cookies
   - Must include frontend origin (http://localhost:3000)
   - Critical for auth to work
4. **JWT Token Handling**:
   - Frontend gets token from Better Auth session
   - Token passed in Authorization: Bearer header
   - Backend verifies using PyJWT and BETTER_AUTH_SECRET
5. **Architecture Clarity**:
   - Better Auth creates tokens (frontend)
   - Backend ONLY verifies tokens
   - No backend /api/auth/* routes (those are on Next.js)
**Testing Requirements**:
Each implementation task should include basic validation:
- "Build succeeds without errors"
- "Type checking passes"
- "No runtime errors in console"
Integration testing tasks should include:
- Manual test steps
- Expected vs actual outcomes
- Error scenario handling
**Output Format**:
Generate tasks.md with this structure:
```markdown
# Auth Integration Tasks
## Phase 1: Infrastructure Setup
### AUTH-001: Install Frontend Dependencies
**Component**: Frontend
**Effort**: XS
**Dependencies**: None
**Description**:
Install Better Auth packages in the frontend application.
**Files**:
- `frontend/package.json`
**Steps**:
1. Navigate to frontend directory
2. Run npm install better-auth @better-auth/react
3. Verify packages in package.json
**Acceptance Criteria**:
- [ ] better-auth appears in package.json dependencies
- [ ] @better-auth/react appears in package.json dependencies
- [ ] npm install completes without errors
**Implementation Notes**:
- pg is required for Better Auth database connection
- Version should be latest stable
---
### AUTH-002: Configure Frontend Environment Variables
...
[Continue for all tasks]
Critical Tasks to Include:

Environment setup (frontend and backend)
Install dependencies (better-auth, PyJWT)
Generate BETTER_AUTH_SECRET
Configure DATABASE_URL (same in both)
Run Better Auth migration
Create lib/auth.ts (server-side)
Create /api/auth/[...all]/route.ts
Create lib/auth-client.ts (client-side)
Create AuthContext.tsx
Update app/layout.tsx (wrap in AuthProvider)
Update signin page (remove mock)
Update signup page (remove mock)
Update api.ts (use real tokens)
Create middleware.ts (route protection)
Update AuthContext (add userId)
Verify backend JWT middleware
Verify backend CORS config
Test sign-up flow
Test sign-in flow
Test session persistence
Test route protection
Test API authentication
Test multi-user isolation
Output Deliverable:

Create Phase-2/specs/004-auth-integration/tasks.md with:

All tasks organized by phase
Each task following the format above
Clear dependency chain
Estimated total effort
Risk callouts for complex tasks
Total Task Count: Aim for 20-30 granular tasks

Priority Markers:

🔴 P0: Blocking (must complete before anything else)
🟡 P1: High priority (core functionality)
🟢 P2: Medium priority (important but not blocking)
⚪ P3: Low priority (nice to have, documentation)
Generate the tasks now.


## Response snapshot

Created comprehensive task breakdown for Better Auth integration with 30 granular tasks organized by phase. Each task includes unique ID, component, effort estimation, priority, dependencies, description, files to modify, steps, acceptance criteria, and implementation notes. Tasks follow proper format with specific, testable, observable, and measurable acceptance criteria. Critical architecture points are emphasized: JWT creation on frontend, backend only verifying tokens, shared secrets, and proper CORS configuration.

## Outcome

- ✅ Impact: Created comprehensive task breakdown with 30 granular tasks for Better Auth integration
- 🧪 Tests: Each task includes specific, testable acceptance criteria
- 📁 Files: Created tasks.md file with proper structure and format
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks follow Spec-Kit Plus conventions with proper dependencies and granular scope

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of P0 tasks