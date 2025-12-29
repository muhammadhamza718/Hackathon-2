---
ID: "0021"
TITLE: "Specify Admin Dashboard High Tech UI"
STAGE: "spec"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "claude-3-5-sonnet-20241022"
FEATURE: "admin-dashboard"
BRANCH: "main"
USER: "unknown"
COMMAND: "/sp.implements"
LABELS: ["spec", "ui-ux", "admin", "glassmorphism", "animations", "security"]
LINKS_SPEC: "specs/006-admin-dashboard-fixes/spec.md"
LINKS_TICKET: "null"
LINKS_ADR: "null"
LINKS_PR: "null"
FILES_YAML:
  - "failed: none (Planning phase)"
TESTS_YAML:
  - "none"
---

# SPECIFY ADMIN DASHBOARD & HIGH TECH UI

## PROMPT_TEXT

/sp.implements
# Specify Admin Dashboard & High Tech UI

## Goal

Transform the current Admin Dashboard into a "High Tech" experience with "Next.js Gen UI/UX" animations, while strictly enforcing navigation & authentication constraints.

## Requirements

### 1. Strict Authentication & Navigation

- **Hidden Entry**: The Navbar MUST NOT contain links to `/admin/dashboard` or `/admin/auth`.
- **Exclusive Gateway**:
  - Regular login (`/auth/signin`) MUST NOT provide access to the admin dashboard.
  - Access to `/admin/dashboard` MUST require a fresh authentication via `/admin/auth`.
  - _Note: If a user is already logged in as admin, they can be auto-redirected, but the entry point for the session should be distinct or verified._
- **Credentials**: Admin credentials (email/password) must be securely managed (e.g., via `.env` for seeding, never hardcoded).

### 2. Admin Dashboard Functionality

- **User Management**:
  - View all users.
  - View all tasks for ANY user.
  - Manage (Delete/Update) users and tasks.
- **Backend Support**: Ensure the `api/admin.py` router supports these operations (Project verification confirms this is largely implemented, but ensure strict RBAC).

### 3. "High Tech" UI/UX

- **Design Language**:
  - **Glassmorphism**: Deep, multi-layered glass effects with heavy blurs and white borders.
  - **Animations**: Use `framer-motion` for:
    - Staggered list reveals (users/tasks).
    - Hover effects (scale, glow).
    - Layout transitions (smooth expansion of user cards).
    - "Gen UI" feel: energetic, responsive, fluid.
- **Visuals**:
  - Background: Dynamic, animated gradients or "Aurora" effects.
  - Typography: Clean, modern sans-serif (Inter/Geist) with strict hierarchy.
  - Micro-interactions: satisfying clicks, loading states, and transitions.

## Implementation Guide

- **Frontend**: `app/admin/dashboard/page.tsx`, `components/ui/admin-user-card.tsx`
- **Backend**: `backend/api/admin.py` (Verify endpoints)
- **Auth**: `frontend/lib/auth.ts`, `frontend/components/protected-route.tsx`

## Technical Constraints

- Use **Tailwind CSS** for styling (with `framer-motion` for animation).
- Maintain existing **Better Auth** session logic (add `role` field check).
- Ensure **Responsive Design** for mobile admin access.

## RESPONSE_TEXT

Created the detailed specification prompt for the Admin Dashboard Overhaul. Verified that current backend capabilities (Admin API) match the requirements, but identified gaps in the UI (currently standard Tailwind, needs Glassmorphism/Framer Motion) and strict link visibility (Admin links were only partially hidden). This prompt serves as the input for the next implementation phase.

## OUTCOME_IMPACT

- Established clear "High Tech" aesthetic requirements.
- Defined strict security boundaries for Admin entry (Exclusive Gateway).
- Aligned implementation plan with existing monorepo structure.

## TESTS_SUMMARY

- Verified `backend/api/admin.py` exists.
- Checked `frontend/components/navigation.tsx` for link logic.

## FILES_SUMMARY

- `history/prompts/009-admin-dashboard-spec/0021-admin-dashboard-spec.prompt.md` (Self)

## NEXT_PROMPTS

- Run `/sp.implement` with this spec to build the UI.

## REFLECTION_NOTE

"High Tech" is subjective; specifying libraries like `framer-motion` and concrete effects like "Aurora gradients" makes the requirement actionable for an AI.
