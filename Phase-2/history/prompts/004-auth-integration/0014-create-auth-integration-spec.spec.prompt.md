---
id: 0001
title: Create Auth Integration Spec
stage: spec
date: 2025-12-12
surface: agent
model: qwen3-coder-plus
feature: 004-auth-integration
branch: main
user: unknown
command: /sp.phr
labels: ["auth", "better-auth", "spec", "integration", "jwt"]
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

**Feature Name**: `004-auth-integration`

**Goal**: Replace frontend mock authentication with REAL Better Auth (JWT) integration.

**Context**:
*   Backend has JWT verification (Completed in 002).
*   Frontend has UI pages (Completed in 003).
*   **Gap**: The Frontend `lib/auth.ts` client is missing, and Sign-in pages use `mock-jwt-token`.

**Requirements**:
1.  **Frontend Auth Client**:
    *   Create `frontend/lib/auth-client.ts`.
    *   Initialize `createAuthClient` from `better-auth/react`.
    *   Configure it to point to `NEXT_PUBLIC_BETTER_AUTH_URL` (usually the backend URL).
2.  **Sign In / Sign Up Logic**:
    *   Update [frontend/app/auth/signin/page.tsx] & `signup/page.tsx`.
    *   Replace `localStorage` mock logic with `authClient.signIn.email(...)`.
3.  **Token Management**:
    *   Ensure the session token is properly retrieved.
    *   Update [frontend/lib/api.ts] to get the *real* token from the auth client (or cookie), not just `localStorage`.
4.  **Backend Connection**:
    *   Ensure Frontend calls the Backend's `/api/auth/*` routes correctly.

**Output**:
Create `specs/004-auth-integration/spec.md`.
then run /sp.phr

## Response snapshot

Created the complete specification for the auth integration feature, defining requirements for implementing Better Auth in the frontend.

## Outcome

- ✅ Impact: Created complete feature specification for auth integration with Better Auth
- 🧪 Tests: none
- 📁 Files: 1 file created (specs/004-auth-integration/spec.md)
- 🔁 Next prompts: none
- 🧠 Reflection: Specification clearly defines the gap between frontend mock auth and backend JWT verification, with clear requirements for integration

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
