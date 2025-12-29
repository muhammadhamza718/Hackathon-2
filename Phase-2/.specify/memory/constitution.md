<!--
SYNC IMPACT REPORT:
Version change: N/A → 1.0.0
List of modified principles: None (new constitution)
Added sections: Spec-First Development, Monorepo Structure Compliance, Stateless Authentication, Technology Stack Adherence, Testable Implementation, Security-First Development, Technical Constraints, Development Workflow
Removed sections: None
Templates requiring updates: ✅ .specify/templates/plan-template.md (Constitution Check section exists and will be validated with new principles)
Templates requiring updates: ✅ .specify/templates/spec-template.md (requirements alignment checked)
Templates requiring updates: ✅ .specify/templates/tasks-template.md (task categorization reflects new principles)
Templates requiring updates: ✅ CLAUDE.md (references constitution properly)
Follow-up TODOs: None
-->
# Todo Full-Stack Web App Constitution

## Core Principles

### Spec-First Development
Never start coding without a spec. Always reference @specs/features/[feature].md before implementing. If requirements change, update the Spec file first, then update the code. Validate implementation against specs.

### Monorepo Structure Compliance
Enforce the defined monorepo structure for all operations. Do not create files outside the schema unless explicitly authorized. Maintain proper folder organization with specs/, frontend/, backend/, and other designated directories.

### Stateless Authentication
Use JWT Tokens signed with BETTER_AUTH_SECRET. Every API endpoint (except public/health checks) MUST verify the Authorization: Bearer <token> header. All database queries must filter by user_id extracted from the token. Users must NEVER see other users' data.

### Technology Stack Adherence
Use Next.js 16+ (App Router) with TypeScript and Tailwind CSS for frontend. Use Python FastAPI with SQLModel and Neon Serverless PostgreSQL for backend. Follow all specified technology standards.

### Testable Implementation
Every feature must be testable. Implement with smallest viable diff; do not refactor unrelated code. Cite existing code with references and propose new code in fenced blocks.

### Security-First Development
Implement security measures at every layer. Never hardcode secrets or tokens; use .env and docs. Prefer the smallest viable diff; do not refactor unrelated code.

## Technical Constraints
Frontend: Next.js 16+, TypeScript, Tailwind CSS, Better Auth with JWT. Backend: Python FastAPI, SQLModel, Neon Serverless PostgreSQL, JWT Verification Middleware. All API endpoints must verify authorization tokens and filter data by user_id.

## Development Workflow
Initialize folder structure with specs, frontend, backend. Define specs with user stories and schemas. Build FastAPI models and routes based on database schema. Build Next.js pages based on UI specs. Connect frontend api.ts -> backend endpoints -> Neon DB.

## Governance
All development must follow Spec-Driven Development methodology. Every implementation must reference specifications. Code reviews must verify compliance with architectural decisions. Changes to core architecture require explicit approval.

**Version**: 1.0.0 | **Ratified**: 2025-12-11 | **Last Amended**: 2025-12-11