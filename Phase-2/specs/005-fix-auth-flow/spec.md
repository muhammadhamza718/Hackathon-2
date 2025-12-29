# Feature Specification: Fix Authentication Flow Diagram

**Feature Branch**: `005-fix-auth-flow`
**Created**: 2025-12-13
**Status**: Draft
**Input**: User description: "Fix these 🔴 REMAINING CRITICAL ISSUES ISSUE 1: Architecture Flow Diagram is WRONG ❌ Location: Lines 14-17 Current Flow: 1. POST /api/auth/signin │─────────────────────────→ Next.js Frontend │ 2. Create JWT & Session │────────────────────────→ FastAPI Backend PROBLEM: Step 2 shows Next.js sending \"Create JWT & Session\" to FastAPI Backend THIS IS INCORRECT - Better Auth creates JWT on Next.js, NEVER sends to backend Backend only RECEIVES tokens from frontend API calls, doesn't create them CORRECT Flow Should Be: 1. POST /api/auth/signin │─────────────────────────→ Next.js Frontend │ 2. Verify credentials (Better - created_at: timestamp ### tasks - id: integer (primary key) - user_id: string (foreign key -> users.id) - title: string (not null) - description: text (nullable) - completed: boolean (default false) - created_at: timestamp - updated_at: timestamp Add After Line 67: ### Database Schema Created by Better Auth Migration When you run `npx better-auth migrate`, it creates these tables: **`user` table** (Better Auth managed): - `id`: VARCHAR (primary key, UUID) - `email`: VARCHAR(255) UNIQUE NOT NULL - `name`: VARCHAR(255) - `password_hash`: VARCHAR(255) - `created_at`: TIMESTAMP DEFAULT NOW() - `updated_at`: TIMESTAMP DEFAULT NOW() **`session` table** (Better Auth managed): - `id`: VARCHAR (primary key, session token) - `user_id`: VARCHAR (foreign key -> user.id) - `expires_at`: TIMESTAMP - `created_at`: TIMESTAMP **`account` table** (Better Auth managed - for OAuth, unused in this phase): - Skip for Phase 2 **`tasks` table** (Backend managed - MUST be created separately): - `id`: SERIAL PRIMARY KEY - `user_id`: VARCHAR NOT NULL (foreign key -> user.id) - `title`: VARCHAR(200) NOT NULL - `description`: TEXT - `completed`: BOOLEAN DEF[Pasted text #2 +230 lines]"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Correct Authentication Flow (Priority: P1)

As a developer working on the application, I need the architecture flow diagram to accurately represent how authentication works with Better Auth, so that I can properly understand and implement the authentication system.

**Why this priority**: This is critical for all team members to understand the correct flow of authentication between frontend and backend, preventing implementation errors and security issues.

**Independent Test**: The architecture documentation should clearly show that JWT creation happens on the frontend via Better Auth, and that the backend only receives and validates these tokens.

**Acceptance Scenarios**:

1. **Given** a user needs to authenticate, **When** they submit credentials to the Next.js frontend, **Then** Better Auth creates JWT and session tokens on the frontend without involving the backend
2. **Given** an authenticated user makes API calls, **When** they include JWT in request headers, **Then** the FastAPI backend validates these tokens without creating new ones

---

### User Story 2 - Database Schema Understanding (Priority: P2)

As a developer, I need to understand which database tables are managed by Better Auth vs. the custom backend, so I can properly implement data relationships and access patterns.

**Why this priority**: Understanding the separation of concerns between Better Auth's database management and custom backend tables is essential for proper data handling.

**Independent Test**: Documentation clearly identifies which tables (user, session, account) are managed by Better Auth and which (tasks) are managed by the backend.

**Acceptance Scenarios**:

1. **Given** a user registers or signs in, **When** the process completes, **Then** Better Auth creates records in user and session tables automatically
2. **Given** a user creates tasks, **When** they interact with the task API, **Then** the backend creates records in the tasks table with proper user_id foreign key relationships

---

### User Story 3 - Backend API Token Validation (Priority: P3)

As a developer, I need to ensure the backend properly validates JWT tokens from Better Auth, so that only authenticated users can access protected endpoints.

**Why this priority**: This ensures proper security implementation where the backend only accepts and validates tokens from Better Auth.

**Independent Test**: Backend endpoints properly validate JWT tokens sent from the frontend without attempting to create new tokens.

**Acceptance Scenarios**:

1. **Given** a user has valid JWT from Better Auth, **When** they make API requests with the token, **Then** the backend successfully validates and processes the request
2. **Given** a user has invalid or expired JWT, **When** they make API requests with the token, **Then** the backend properly rejects the request with appropriate error

---

### Edge Cases

- What happens when Better Auth fails to create JWT on the frontend?
- How does the system handle expired JWT tokens sent to the backend?
- What occurs when there's a mismatch between Better Auth session and backend user records?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST accurately document the authentication flow showing JWT creation happens on Next.js frontend via Better Auth
- **FR-002**: System MUST document that FastAPI backend only receives and validates JWT tokens, never creates them
- **FR-003**: Users MUST be able to understand the correct flow: POST /api/auth/signin → Next.js Frontend → Verify credentials and create JWT → Use JWT for backend API calls
- **FR-004**: System MUST clearly identify which database tables are managed by Better Auth (user, session, account) versus custom backend (tasks)
- **FR-005**: System MUST specify that the tasks table has a foreign key relationship to Better Auth's user table via user_id

### Key Entities _(include if feature involves data)_

- **User**: Represents application users, managed by Better Auth with id, email, name, password_hash
- **Session**: Represents active user sessions, managed by Better Auth with session tokens and user associations
- **Task**: Represents user tasks, managed by backend with relationship to Better Auth user id

## Implementation _(mandatory)_

### Target Files

- **specs/004-auth-integration/spec.md** (MODIFY - documentation update only)

### Deliverable Type

This is a **DOCUMENTATION-ONLY** fix. No code implementation required.

**What This Spec Does**:

- Fix incorrect architecture diagram in spec 004
- Add missing database schema section to spec 004
- Add backend JWT verification code example to spec 004

**What This Spec Does NOT Do**:

- ❌ Implement actual authentication code
- ❌ Create Better Auth configuration
- ❌ Create backend JWT middleware
- ❌ Modify any frontend/backend application code

---

### Change 1: Fix Architecture Flow Diagram

**File**: `specs/004-auth-integration/spec.md`  
**Location**: Lines 8-33

**Current (INCORRECT)**:

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │         │   Next.js    │         │   FastAPI   │
│             │         │   Frontend   │         │   Backend   │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │ 1. POST /api/auth/signin │                     │
      │─────────────────────────→│                     │
      │                        │ 2. Create JWT & Session│
      │                        │────────────────────────→│  ❌ WRONG
```

**Replace With (CORRECT)**:

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │         │   Next.js    │         │   FastAPI   │
│             │         │   Frontend   │         │   Backend   │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │ 1. POST /api/auth/signin                       │
      ├───────────────────────→│                        │
      │                        │ 2. Verify credentials  │
      │                        │    (Better Auth)       │
      │                        │ 3. Create JWT          │
      │                        │    (Better Auth)       │
      │ 4. Return JWT cookie   │                        │
      │←───────────────────────┤                        │
      │                        │                        │
      │ 5. GET /api/{user_id}/tasks (with JWT cookie)  │
      ├────────────────────────┴───────────────────────→│
      │                                                 │ 6. Verify JWT
      │                                                 │    signature
      │                                                 │ 7. Extract
      │                                                 │    user_id
      │ 8. Return user's tasks                          │
      │←────────────────────────────────────────────────┤
```

**Key Changes**:

- ✅ Removed arrow from Next.js to Backend for JWT creation
- ✅ Added steps 2-3 showing JWT creation happens on Next.js
- ✅ Made it clear Backend only verifies tokens in step 6-7

---

### Change 2: Add Database Schema Section

**File**: `specs/004-auth-integration/spec.md`  
**Location**: After line 67 (after Better Auth Installation section)

**Add New Section**:

````markdown
## Database Schema

### Tables Created by Better Auth Migration

When you run `npx better-auth migrate`, Better Auth creates these tables in your Neon PostgreSQL database:

#### 1. `user` table (Better Auth Managed)

```sql
CREATE TABLE "user" (
  id VARCHAR PRIMARY KEY,           -- UUID generated by Better Auth
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```
````

**Purpose**: Stores user accounts and credentials  
**Managed By**: Better Auth  
**Access**: Backend can READ user.id for task relationships, but should NOT modify

---

#### 2. `session` table (Better Auth Managed)

```sql
CREATE TABLE "session" (
  id VARCHAR PRIMARY KEY,           -- Session token
  user_id VARCHAR NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);
```

**Purpose**: Stores active user sessions  
**Managed By**: Better Auth  
**Access**: Backend should NOT access this table directly

---

#### 3. `account` table (Better Auth Managed - Optional)

```sql
-- Better Auth creates this for OAuth providers
-- Not used in Phase 2 (email/password only)
-- Safe to ignore for now
```

---

### Tables You MUST Create for Your Application

#### 4. `tasks` table (Backend Managed)

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Purpose**: Stores user tasks  
**Managed By**: FastAPI Backend (SQLModel)  
**Relationship**: Each task belongs to a user via `user_id` foreign key

---

### Database Responsibility Matrix

| Table     | Created By            | Managed By         | Backend Access             |
| --------- | --------------------- | ------------------ | -------------------------- |
| `user`    | Better Auth migration | Better Auth        | READ-ONLY (for user_id FK) |
| `session` | Better Auth migration | Better Auth        | NO ACCESS                  |
| `account` | Better Auth migration | Better Auth        | NO ACCESS                  |
| `tasks`   | Backend migration     | Backend (SQLModel) | FULL ACCESS (CRUD)         |

**CRITICAL**:

- Better Auth tables (`user`, `session`) are created when you run `npx better-auth migrate`
- Backend tables (`tasks`) must be created separately via backend migrations (e.g., Alembic)
- Both use the SAME Neon PostgreSQL database

````

---

### Change 3: Add Backend JWT Verification Code Example

**File**: `specs/004-auth-integration/spec.md`
**Location**: After Prerequisites section (after line 67)

**Add New Section**:

```markdown
## Backend JWT Verification (Feature 002 Reference)

**IMPORTANT**: This section shows the backend implementation that MUST be completed BEFORE starting this feature.

### Required Backend Code

**File**: `backend/middleware/auth.py`

```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

security = HTTPBearer()

async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Verify JWT token from Better Auth and extract user_id.

    Returns:
        user_id (str): The authenticated user's ID

    Raises:
        HTTPException: 401 if token is invalid/expired
        HTTPException: 403 if user_id is missing
    """
    token = credentials.credentials
    secret = os.getenv("BETTER_AUTH_SECRET")

    if not secret:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: BETTER_AUTH_SECRET not set"
        )

    try:
        # Verify JWT signature and decode payload
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        # Better Auth uses 'sub' claim for user ID
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=403,
                detail="Invalid token: missing user_id"
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
````

### Backend Route Example

**File**: `backend/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from middleware.auth import verify_jwt
from models import Task
from database import get_session

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Security:
    - Verifies user_id in URL matches authenticated user from JWT
    - Only returns tasks belonging to the authenticated user
    """

    # Verify user_id in URL matches authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot access other user's tasks"
        )

    # Fetch tasks for this user only
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    return tasks
```

### Required Dependencies

**File**: `backend/requirements.txt`

```txt
PyJWT==2.8.0  # For JWT verification
```

**Installation**:

```bash
cd backend
pip install PyJWT
```

### Environment Variable

**File**: `backend/.env`

```env
BETTER_AUTH_SECRET=<same-secret-as-frontend>
```

**CRITICAL**: The `BETTER_AUTH_SECRET` MUST be identical to the one in `frontend/.env.local`

````

---

### Change 4: Add CORS Configuration Section

**File**: `specs/004-auth-integration/spec.md`
**Location**: After Prerequisites section (line 50)

**Add**:

```markdown
### Backend CORS Configuration (Required)

**File**: `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration for Better Auth cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",              # Next.js dev server
        "https://your-frontend-domain.com",    # Production frontend
    ],
    allow_credentials=True,  # CRITICAL: Required for cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
````

**Why `allow_credentials=True` is CRITICAL**:

- Enables browsers to send HTTP-only cookies cross-origin
- Without this, authentication cookies will be blocked
- Required for Better Auth session cookies to work

```

---

## Validation *(mandatory)*

### Documentation Review Checklist

**After making changes to spec 004, verify**:

- [ ] Architecture diagram no longer shows Backend creating JWT
- [ ] Architecture diagram shows JWT creation happens on Next.js (steps 2-3)
- [ ] Architecture diagram shows Backend only verifies JWT (steps 6-7)
- [ ] Database schema section exists with all 4 tables documented
- [ ] `user`, `session`, `account` tables marked as "Better Auth Managed"
- [ ] `tasks` table marked as "Backend Managed"
- [ ] Foreign key relationship between `tasks.user_id` and `user.id` documented
- [ ] Backend JWT verification code example included
- [ ] CORS configuration section included with `allow_credentials=True`

### Peer Review

Have another developer review the updated spec 004 and confirm:

- [ ] They understand JWT creation happens on Next.js frontend
- [ ] They understand Backend only validates tokens, never creates them
- [ ] They can identify which tables are managed by Better Auth vs Backend
- [ ] They understand the `tasks` table must be created separately from Better Auth migrations
- [ ] They know backend needs PyJWT library for token verification

### Success Validation

**Before**: Developer might implement auth incorrectly with backend creating JWTs
**After**: Developer clearly understands frontend creates JWTs, backend validates them

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Architecture diagram in spec 004 accurately shows JWT creation on Next.js frontend only
- **SC-002**: Database schema section in spec 004 documents all 4 tables with clear ownership
- **SC-003**: All team members can correctly explain which component creates vs validates JWTs after reading updated spec
- **SC-004**: Zero implementation attempts where backend tries to create JWT tokens
- **SC-005**: Backend JWT verification code example is included in spec 004 for reference
```
