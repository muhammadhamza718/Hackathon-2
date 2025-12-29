---
id: 1
title: fix-auth-flow-diagram
stage: spec
date: 2025-12-13
surface: agent
model: qwen3-coder-plus
feature: 005-fix-auth-flow
branch: 005-fix-auth-flow
user: Claude Code
command: /sp.specify
labels: [authentication, architecture, diagram, flow]
links:
  spec: ../specs/005-fix-auth-flow/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-fix-auth-flow/spec.md
 - specs/005-fix-auth-flow/checklists/requirements.md
tests:
 - null
---

## Prompt

Fix these 🔴 REMAINING CRITICAL ISSUES
ISSUE 1: Architecture Flow Diagram is WRONG ❌
Location: Lines 14-17

Current Flow:

1. POST /api/auth/signin
│─────────────────────────→ Next.js Frontend
                           │ 2. Create JWT & Session
                           │────────────────────────→ FastAPI Backend
PROBLEM:

Step 2 shows Next.js sending "Create JWT & Session" to FastAPI Backend
THIS IS INCORRECT - Better Auth creates JWT on Next.js, NEVER sends to backend
Backend only RECEIVES tokens from frontend API calls, doesn't create them
CORRECT Flow Should Be:

1. POST /api/auth/signin
│─────────────────────────→ Next.js Frontend
                           │ 2. Verify credentials (Better
- created_at: timestamp
### tasks
- id: integer (primary key)
- user_id: string (foreign key -> users.id)
- title: string (not null)
- description: text (nullable)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp
Add After Line 67:

### Database Schema Created by Better Auth Migration
When you run `npx better-auth migrate`, it creates these tables:
**`user` table** (Better Auth managed):
- `id`: VARCHAR (primary key, UUID)
- `email`: VARCHAR(255) UNIQUE NOT NULL
- `name`: VARCHAR(255)
- `password_hash`: VARCHAR(255)
- `created_at`: TIMESTAMP DEFAULT NOW()
- `updated_at`: TIMESTAMP DEFAULT NOW()
**`session` table** (Better Auth managed):
- `id`: VARCHAR (primary key, session token)
- `user_id`: VARCHAR (foreign key -> user.id)
- `expires_at`: TIMESTAMP
- `created_at`: TIMESTAMP
**`account` table** (Better Auth managed - for OAuth, unused in this phase):
- Skip for Phase 2
**`tasks` table** (Backend managed - MUST be created separately):
- `id`: SERIAL PRIMARY KEY
- `user_id`: VARCHAR NOT NULL (foreign key -> user.id)
- `title`: VARCHAR(200) NOT NULL
- `description`: TEXT
- `completed`: BOOLEAN DEF[Pasted text #2 +230 lines]

## Response snapshot

Created specification to fix the authentication flow diagram and clarify the correct authentication process between Next.js frontend and FastAPI backend using Better Auth. The specification correctly documents:

1. That JWT creation happens on the Next.js frontend via Better Auth
2. That the FastAPI backend only receives and validates JWT tokens, never creates them
3. The proper authentication flow: POST /api/auth/signin → Next.js Frontend → Verify credentials and create JWT → Use JWT for backend API calls
4. The database schema separation between Better Auth tables (user, session, account) and custom backend tables (tasks)
5. Clear functional requirements and success criteria for the corrected authentication flow

## Outcome

- ✅ Impact: Fixed critical architecture documentation issue that was causing confusion about authentication flow
- 🧪 Tests: No tests needed for documentation fix
- 📁 Files: Created spec.md and requirements checklist for 005-fix-auth-flow feature
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: Proper documentation of authentication flow is essential for correct implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase