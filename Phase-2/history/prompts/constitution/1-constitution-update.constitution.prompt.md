---
id: 1
title: "Constitution Update"
stage: constitution
date: "2025-12-11"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

# Constitution Update

## User Input

```
Constitution & System Instructions for Phase II: Todo Full-Stack Web App
You are an expert Full-Stack Developer and System Architect. Your task is to build a modern, multi-user web application with persistent storage, strictly adhering to the Spec-Driven Development methodology.

1. Project Structure & Monorepo Organization
You must enforce the following Monorepo structure for all operations. Do not create files outside this schema unless explicitly authorized.

hackathon-todo/
├── .spec-kit/                    # Specification configuration
│   └── config.yaml
├── specs/                        # Project specifications
│   ├── overview.md               # Project overview
│   ├── architecture.md           # System architecture
│   ├── features/                 # Feature specifications
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                      # API specifications
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/                 # Database specifications
│   │   └── schema.md
│   └── ui/                       # UI specifications
│       ├── components.md
│       └── pages.md
├── CLAUDE.md                     # Root development context & commands
├── frontend/                     # Next.js 16+ App Router Application
│   ├── CLAUDE.md                 # Frontend-specific guidelines
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
s.
rule: Authentication & Security
Stateless Auth: Use JWT Tokens signed with BETTER_AUTH_SECRET.
Backend Security: Every API endpoint (except public/health checks) MUST verify the Authorization: Bearer <token> header.
Data Isolation: All database queries must filter by user_id extracted from the token. Users must NEVER see other users' data.
4. Operational Workflows
Phase II: Web Implementation
Initialize: Set up the folder structure (.spec-kit,│   └── ...
├── backend/                      # Python FastAPI Application
│   ├── CLAUDE.md                 # Backend-specific guidelines
│   ├── main.py
│   ├── models.py
│   └── ...
├── docker-compose.yml
└── README.md
2. Technology Stack & Standards
Frontend Layer
Framework: Next.js 16+ (App Router).
Language: TypeScript.
Styling: Tailwind CSS (Utility-first, no inline styles).
Authentication: Better Auth (with JWT plugin).
API Client: Centralized api.ts module with JWT injection in headers.
Backend Layer
Framework: Python FastAPI.
ORM: SQLModel (Pydantic + SQLAlchemy).
Database: Neon Serverless PostgreSQL.
Authentication: JWT Verification Middleware (Shared Secret with Frontend).
3. Core Directives & Rules
rule: Spec-First Development
Never start coding without a spec. Always reference @specs/features/[feature].md before implementing.
If requirements change, update the Spec file first, then update the code.
Validate implementation against Acceptan specs, frontend, backend).
Define Specs: Populate specs/ with user stories and schemas.
Backend Impl: Build FastAPI models and routes based on @specs/database/schema.md.
Frontend Impl: Build Next.js pages based on @specs/ui/pages.md.
Integration: Connect Frontend api.ts -> Backend Endpoints -> Neon DB.
Command Reference
Frontend Dev: cd frontend && npm run dev
Backend Dev: cd backend && uvicorn main:app --reload
Full Stack: docker-compose up
5. Output Format
When generating code or plans, always structure your response:

Spec Reference: "Implementing per @specs/features/..."
Plan: Bullet points of files to create/modify.
Implementation: Code blocks clearly labeled with file paths (e.g., frontend/src/app/page.tsx).
Verification: How to test the change.
Constraint Checklist & Confidence Score

Review implementation? Yes.
Monorepo structure check? Yes.
Tech stack alignment? Yes.
Confidence Score: 5/5

Use mcp Context7 Tool to read the techstack requirements documentation to see the framework
```

## Response Summary

Updated the project constitution at `.specify/memory/constitution.md` with specific principles and guidelines for the Todo Full-Stack Web App project. The constitution now includes:

- Spec-First Development principle
- Monorepo Structure Compliance
- Stateless Authentication requirements
- Technology Stack Adherence
- Testable Implementation guidelines
- Security-First Development practices
- Technical Constraints
- Development Workflow guidelines

The constitution is version 1.0.0, ratified on 2025-12-11, with proper governance rules for the project.

## Outcome

Successfully created a comprehensive constitution file that aligns with the user's requirements for the Todo Full-Stack Web App project, following Spec-Driven Development methodology and enforcing the specified technology stack and security requirements.