---
id: 0002
title: Update Auth Integration Spec
stage: spec
date: 2025-12-12
surface: agent
model: qwen3-coder-plus
feature: 004-auth-integration
branch: main
user: unknown
command: /sp.phr
labels: ["auth", "better-auth", "spec", "integration", "jwt", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-auth-integration/spec.md
tests:
 - none
---

## Prompt

/sp.specify
**Feature Name**: `004-auth-integration` (REVISION)
**Goal**: Create a COMPLETE, UNAMBIGUOUS specification for integrating Better Auth JWT authentication in the frontend, with all prerequisites, environment setup, implementation details, and testing criteria clearly defined.
**Context**:
- Current spec has critical ambiguities about Better Auth architecture
- Missing assumptions about shared secrets, database setup, and CORS
- Incomplete requirements for environment variables, server-side auth, route protection
- Scope conflicts about where auth routes run (frontend vs backend)
- Detailed review completed: identified 4 ambiguous terms, 5 missing assumptions, 8 incomplete requirements, 4 scope conflicts
**Critical Fixes Required**:
## 1. ARCHITECTURE CLARIFICATION
**MUST SPECIFY**:
- Better Auth runs ON Next.js frontend, NOT on FastAPI backend
- Better Auth creates `/api/auth/*` routes as Next.js API routes
- Backend ONLY verifies JWT tokens, does NOT issue them
- Frontend issues tokens via Better Auth → Backend verifies via shared secret
**UPDATE Section**: Add "Architecture Overview" section with:
```markdown
## Architecture Overview
### Authentication Flow
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │         │   Next.js    │         │   FastAPI   │
│             │         │   Frontend   │         │   Backend   │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │ 1. POST /api/auth/signin │                        │
      │─────────────────────────→│                        │
      │                        │ 2. Create JWT & Session│
      │                        │────────────────────────→│
      │ 3. Redirect to /dashboard│                        │
      │←─────────────────────────│                        │
      │                        │                        │
      │ 4. GET /api/{user_id}/tasks │                    │
      │─────────────────────────────────────────────────→│
      │                        │                        │
      │                        │ 5. Verify JWT          │
      │                        │    signature           │
      │                        │←───────────────────────│
      │                        │                        │
      │ 6. Return user's tasks │                        │
      │←───────────────────────│                        │
      │                        │                        │
      │ 7. Display tasks       │                        │
      │←───────────────────────│                        │
### Component Responsibilities
| Component | Responsibility |
|-----------|----------------|
| Better Auth (Next.js) | Issue JWT tokens, manage sessions, store users in DB |
| Next.js Frontend | Provide auth UI, call auth endpoints, attach tokens to API calls |
| FastAPI Backend | VERIFY JWT tokens, filter data by authenticated user |
| Neon PostgreSQL | Store users, sessions (Better Auth), and tasks (Backend) |
**CRITICAL**: Backend does NOT have `/api/auth/*` routes. Those are Next.js routes.
2. PREREQUISITES SECTION
ADD NEW SECTION before "Requirements":

## Prerequisites
### Infrastructure Ready
- [ ] Neon PostgreSQL database created and accessible
- [ ] Database connection string available for both frontend and backend
- [ ] CORS configured on FastAPI backend to allow frontend origin
### Backend Completed (Feature 002)
- [ ] FastAPI JWT verification middleware implemented
- [ ] Middleware extracts `user_id` from JWT payload
- [ ] All `/api/{user_id}/*` endpoints filter by authenticated user
- [ ] Backend uses `BETTER_AUTH_SECRET` environment variable to verify tokens
### Frontend UI Completed (Feature 003)
- [ ] Sign-in page exists at `/auth/signin`
- [ ] Sign-up page exists at `/auth/signup`
- [ ] Dashboard page exists at `/dashboard`
- [ ] Mock authentication in place (to be replaced)
### Better Auth Installation
- [ ] Run: `cd frontend && npm install better-auth`
- [ ] Run: `npm install @better-auth/react` (for hooks)
- [ ] Database migrations: `npx better-auth migrate` (creates user/session tables)
3. ENVIRONMENT VARIABLES
ADD NEW SECTION after Prerequisites:

## Environment Configuration
### Frontend Environment Variables
Create `frontend/.env.local`:
```env
# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long-same-as-backend
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
# Database (for Better Auth session storage)
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
Environment Variable Details:

Variable    Purpose    Example
BETTER_AUTH_SECRET    JWT signing secret (server-side)    7f8a9b3c2d1e0f4a5b6c7d8e9f0a1b2c
BETTER_AUTH_URL    Server-side auth URL    http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL    Client-side auth URL    http://localhost:3000
DATABASE_URL    Neon PostgreSQL connection    postgresql://user:pass@host/db
NEXT_PUBLIC_API_URL    FastAPI backend base URL    http://localhost:8000
Backend Environment Variables
Verify backend/.env contains:

# JWT Verification (MUST MATCH FRONTEND)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long-same-as-backend
# Database
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
CRITICAL: BETTER_AUTH_SECRET MUST be IDENTICAL in both frontend and backend.

Generating BETTER_AUTH_SECRET
Run this command:

openssl rand -base64 32
Use the output in BOTH frontend and backend .env files.

---
## 4. EXPANDED REQUIREMENTS
**REPLACE Current "Requirements" Section** with:
```markdown
## Requirements
### 1. Better Auth Server-Side Setup
**File**: `frontend/lib/auth.ts` (NEW FILE - server-side only)
**Implementation**:
```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  jwt: {
    enabled: true,
    expiresIn: "7d", // 7 days
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days in seconds
    },
  },
});
Acceptance Criteria:

 Server-side auth instance created
 Connected to Neon PostgreSQL database
 Email/password provider enabled
 JWT plugin enabled with 7-day expiry
 Session stored in HTTP-only cookie
2. Better Auth API Routes
File: frontend/app/api/auth/[...all]/route.ts (NEW FILE)

Implementation:

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
export const { GET, POST } = toNextJsHandler(auth);
What This Does:

Creates /api/auth/signin, /api/auth/signup, /api/auth/signout endpoints
Handles JWT token issuance
Manages session cookies
Acceptance Criteria:

 Better Auth routes mounted at /api/auth/*
 Sign-in endpoint working at POST /api/auth/signin
 Sign-up endpoint working at POST /api/auth/signup
 Sign-out endpoint working at POST /api/auth/signout
3. Better Auth Client Setup
File: frontend/lib/auth-client.ts (NEW FILE - client-side)

Implementation:

import { createAuthClient } from "better-auth/react";
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
});
export const { useSession, signIn, signUp, signOut } = authClient;
Acceptance Criteria:

 Client-side auth client created
 Points to NEXT_PUBLIC_BETTER_AUTH_URL (Next.js frontend)
 Exports hooks: useSession, signIn, signUp, signOut
4. Authentication Context Provider
File: frontend/contexts/AuthContext.tsx (NEW FILE)

Implementation:

"use client";
import { createContext, useContext, ReactNode } from "react";
import { useSession } from "@/lib/auth-client";
interface AuthContextType {
  user: any | null;
  isLoading: boolean;
  error: Error | null;
}
const AuthContext = createContext<AuthContextType | undefined>(undefined);
export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, isPending, error } = useSession();
  return (
    <AuthContext.Provider
      value={{
        user: session?.user ?? null,
        isLoading: isPending,
        error: error ?? null,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
Root Layout Update: frontend/app/layout.tsx

import { AuthProvider } from "@/contexts/AuthContext";
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
Acceptance Criteria:

 AuthContext created with user, isLoading, error
 useAuth() hook available to all components
 AuthProvider wraps entire app in root layout
5. Update Sign-In Page
File: frontend/app/auth/signin/page.tsx (MODIFY)

Changes Required:

Remove: localStorage.setItem('token', 'mock-jwt-token')
Add: Import { signIn } from "@/lib/auth-client"
Replace: Form submission with Better Auth sign-in
Implementation:

"use client";
import { useState } from "react";
import { signIn } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await signIn.email({
        email,
        password,
      });
      if (result.error) {
        setError(result.error.message || "Invalid email or password");
        setLoading(false);
        return;
      }
      // Success - redirect to dashboard
      router.push("/dashboard");
    } catch (err) {
      setError("An unexpected error occurred");
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
Acceptance Criteria:

 Mock localStorage code removed
 Real Better Auth signIn.email() implemented
 Error handling displays user-friendly messages
 Loading state prevents double submissions
 Successful sign-in redirects to /dashboard
6. Update Sign-Up Page
File: frontend/app/auth/signup/page.tsx (MODIFY)

Changes Required:

Remove: Mock authentication logic
Add: Import { signUp } from "@/lib/auth-client"
Implement: Real sign-up with email/password/name
Implementation:

"use client";
import { useState } from "react";
import { signUp } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
export default function SignUpPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    // Validate password
    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      setLoading(false);
      return;
    }
    try {
      const result = await signUp.email({
        name,
        email,
        password,
      });
      if (result.error) {
        setError(result.error.message || "Sign up failed");
        setLoading(false);
        return;
      }
      // Success - redirect to dashboard (Better Auth auto-signs in)
      router.push("/dashboard");
    } catch (err) {
      setError("An unexpected error occurred");
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
        required
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password (min 8 characters)"
        required
        minLength={8}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Creating account..." : "Sign Up"}
      </button>
    </form>
  );
}
Sign-Up Requirements:

Name: Required, 1-100 characters
Email: Required, valid email format, must be unique
Password: Required, minimum 8 characters
Acceptance Criteria:

 Real Better Auth signUp.email() implemented
 Password validation (min 8 chars) enforced
 Error handling for duplicate email
 Successful sign-up auto-signs in and redirects to /dashboard
7. Update API Client for Token Handling
File: frontend/lib/api.ts (MODIFY)

Changes Required:

Remove: const token = localStorage.getItem('token')
Add: Get token from Better Auth session
Implementation:

import { authClient } from "./auth-client";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
async function getAuthToken(): Promise<string | null> {
  const session = await authClient.getSession();
  return session.data?.session?.token ?? null;
}
export const api = {
  async getTasks(userId: string) {
    const token = await getAuthToken();
    if (!token) {
      throw new Error("Not authenticated");
    }
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (response.status === 401) {
      throw new Error("Unauthorized - please sign in again");
    }
    if (!response.ok) {
      throw new Error("Failed to fetch tasks");
    }
    return response.json();
  },
  async createTask(userId: string, task: { title: string; description?: string }) {
    const token = await getAuthToken();
    if (!token) {
      throw new Error("Not authenticated");
    }
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(task),
    });
    if (response.status === 401) {
      throw new Error("Unauthorized - please sign in again");
    }
    if (!response.ok) {
      throw new Error("Failed to create task");
    }
    return response.json();
  },
  // Add similar updates for updateTask, deleteTask, toggleComplete...
};
Acceptance Criteria:

 localStorage token retrieval removed
 Real token fetched from authClient.getSession()
 Token attached to all API requests in Authorization header
 401 errors throw specific "Unauthorized" error
 All CRUD operations updated (GET, POST, PUT, DELETE, PATCH)
8. Route Protection Middleware
File: frontend/middleware.ts (NEW FILE)

Implementation:

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "@/lib/auth";
const protectedRoutes = ["/dashboard", "/tasks", "/profile"];
const authRoutes = ["/auth/signin", "/auth/signup"];
export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });
  const { pathname } = request.nextUrl;
  // Redirect authenticated users away from auth pages
  if (authRoutes.some((route) => pathname.startsWith(route))) {
    if (session) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }
  // Protect routes requiring authentication
  if (protectedRoutes.some((route) => pathname.startsWith(route))) {
    if (!session) {
      return NextResponse.redirect(new URL("/auth/signin", request.url));
    }
  }
  return NextResponse.next();
}
export const config = {
  matcher: ["/dashboard/:path*", "/tasks/:path*", "/profile/:path*", "/auth/:path*"],
};
Protected Routes:

/dashboard - Requires authentication
/tasks - Requires authentication
/profile - Requires authentication
Public Routes:

/ - Home page (accessible to all)
/auth/signin - Sign-in page
/auth/signup - Sign-up page
Acceptance Criteria:

 Middleware intercepts protected routes
 Unauthenticated users redirected to /auth/signin
 Authenticated users can't access /auth/signin (redirect to /dashboard)
 Session checked server-side for security
9. Session Persistence
Implementation: Handled automatically by Better Auth

How It Works:

Better Auth stores session in HTTP-only cookie
Cookie lifetime: 7 days (configurable)
On page refresh, useSession() hook automatically checks cookie
If valid, session restored; if expired, user is null
Acceptance Criteria:

 User remains signed in after page refresh
 Session expires after 7 days of inactivity
 Expired sessions automatically clear
 Sign-out clears session cookie
10. Error Handling
Required Error Scenarios:

Scenario    Error Message    Action
Invalid credentials    "Email or password incorrect"    Display error on form
Email already exists    "Email already registered"    Display error on sign-up form
Network failure    "Unable to connect to server"    Display error, retry option
Expired session    Silent redirect    Redirect to /auth/signin
Token verification failure (backend)    401 Unauthorized    Frontend catches, redirects to signin
Missing user_id in JWT    403 Forbidden    Backend error, should never happen
Password too short    "Password must be at least 8 characters"    Display on sign-up form
Acceptance Criteria:

 All error scenarios handled gracefully
 User-friendly error messages displayed
 Network errors show retry option
 401 errors trigger automatic sign-out and redirect
---
## 5. TESTING & VALIDATION
**ADD NEW SECTION**:
```markdown
## Testing & Validation
### Manual Testing Checklist
#### Sign-Up Flow
- [ ] Navigate to `/auth/signup`
- [ ] Enter valid name, email, password (8+ chars)
- [ ] Submit form → Should create user in database
- [ ] Should auto-sign in and redirect to `/dashboard`
- [ ] Check Neon database → User record exists in `user` table
#### Sign-In Flow
- [ ] Navigate to `/auth/signin`
- [ ] Enter valid credentials → Should sign in and redirect to `/dashboard`
- [ ] Enter invalid credentials → Should show "Email or password incorrect"
- [ ] Try duplicate email → Should show "Email already registered"
#### Session Persistence
- [ ] Sign in successfully
- [ ] Refresh page → Should remain signed in
- [ ] Close browser and reopen → Should remain signed in (within 7 days)
- [ ] Wait 7 days → Session should expire, redirect to signin
#### Route Protection
- [ ] While signed out, visit `/dashboard` → Should redirect to `/auth/signin`
- [ ] Sign in, visit `/dashboard` → Should display dashboard
- [ ] While signed in, visit `/auth/signin` → Should redirect to `/dashboard`
#### API Integration
- [ ] Sign in as user A
- [ ] Create a task → Should appear in task list
- [ ] Open browser dev tools → Check Network tab
- [ ] Verify request to `/api/{user_id}/tasks` has `Authorization: Bearer <token>` header
- [ ] Sign out
- [ ] Try to access `/api/{user_id}/tasks` → Should return 401 Unauthorized
#### Error Handling
- [ ] Disconnect network → Try to sign in → Should show network error
- [ ] Enter password < 8 chars → Should show validation error
- [ ] Sign up with existing email → Should show "Email already registered"
### Backend Verification
- [ ] Check FastAPI logs → JWT tokens are being verified
- [ ] Sign in as user A → Create task → Task has user_id = A
- [ ] Sign in as user B → Create task → Task has user_id = B
- [ ] User A cannot see User B's tasks (verified via API call)
### Database Verification
Run these SQL queries in Neon console:
```sql
-- Check users table
SELECT id, email, name, created_at FROM "user";
-- Check sessions table
SELECT user_id, expires_at FROM "session" WHERE expires_at > NOW();
-- Check tasks are properly associated with users
SELECT tasks.id, tasks.title, tasks.user_id, "user".email
FROM tasks
JOIN "user" ON tasks.user_id = "user".id;
Expected Results:

Users created via sign-up appear in user table
Active sessions appear in session table
Tasks are correctly linked to user_id
6. SCOPE CLARIFICATIONS
UPDATE "Out of Scope" Section:

## Out of Scope
- Backend authentication routes (Better Auth runs on Next.js, not FastAPI)
- Better Auth database migrations (run separately via CLI)
- UI/UX design changes to auth pages
- Password reset functionality
- Email verification
- Social authentication providers (Google, GitHub, etc.)
- Two-factor authentication (2FA)
- Remember me functionality (session is already persistent for 7 days)
- Custom JWT claims beyond user_id
7. DEPENDENCIES & ASSUMPTIONS
UPDATE "Dependencies" Section:

## Dependencies
### External Dependencies
- `better-auth` npm package (v1.0.0+)
- `@better-auth/react` npm package
- `pg` npm package (PostgreSQL client for Node.js)
- Neon PostgreSQL database with public access
### Internal Dependencies
- **Feature 002**: Backend JWT verification middleware ✅
  - Backend extracts user_id from JWT
  - Backend filters data by authenticated user
  - Backend uses BETTER_AUTH_SECRET to verify tokens
- **Feature 003**: Frontend UI pages ✅
  - Sign-in page at `/auth/signin`
  - Sign-up page at `/auth/signup`
  - Dashboard page at `/dashboard`
### Assumptions
- Neon PostgreSQL database is accessible from both frontend and backend
- `BETTER_AUTH_SECRET` is shared and identical in both services
- CORS is configured on FastAPI to allow requests from Next.js origin
- Better Auth database migrations have been run (`npx better-auth migrate`)
- Backend API endpoints follow the pattern: `/api/{user_id}/tasks`
Output: Update
Phase-2/specs/004-auth-integration/spec.md
 with ALL the above sections, replacing ambiguous language, adding missing details, and clarifying scope conflicts.

Then run /sp.phr to document this specification revision.

## Response snapshot

Updated the auth integration specification with complete and unambiguous requirements for Better Auth integration.

## Outcome

- ✅ Impact: Enhanced auth integration spec with clear architecture overview, prerequisites, environment config, detailed requirements, and testing criteria
- 🧪 Tests: none
- 📁 Files: 1 file modified (specs/004-auth-integration/spec.md)
- 🔁 Next prompts: none
- 🧠 Reflection: Specification now clearly defines the complete architecture for Better Auth integration with proper separation of concerns between frontend and backend

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
