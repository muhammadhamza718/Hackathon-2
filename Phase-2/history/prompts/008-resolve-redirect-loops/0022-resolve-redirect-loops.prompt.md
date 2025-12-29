---
ID: "0020"
TITLE: "Resolve Redirect Loops Admin Dashboard"
STAGE: "refactor"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "claude-3-5-sonnet-20241022"
FEATURE: "admin-dashboard"
BRANCH: "main"
USER: "unknown"
COMMAND: "/sp.implements"
LABELS: ["routing", "nextjs", "ux", "redirects", "protected-route"]
LINKS_SPEC: "null"
LINKS_TICKET: "null"
LINKS_ADR: "null"
LINKS_PR: "null"
FILES_YAML:
  - "frontend/components/protected-route.tsx"
  - "frontend/app/admin/auth/page.tsx"
TESTS_YAML:
  - "manual navigation flow test"
---

# RESOLVE REDIRECT LOOPS & ADMIN DASHBOARD UI

## PROMPT_TEXT

/sp.implements
# Resolve Redirect Loops & Admin Dashboard UI

## Context

Now that the session correctly contains the `role`, I need to fix the frontend routing logic to prevent redirect loops.

## Problem Description

1.  **Redirect Loop**:
    - If a user is logged in as "user" but tries to access `/admin/dashboard`, `ProtectedRoute` redirects them to `/dashboard`.
    - But they _want_ to be on the admin page.
    - If they are an admin but have a stale session, they get stuck in a loop.
2.  **Admin Auth Page**:
    - Needs to automatically redirect _authorized_ admins to the dashboard.
    - Needs to automatically _sign out_ unauthorized users so they can switch accounts.

## Request

1.  Refactor `ProtectedRoute`: If `requireAdmin` is true and the user is NOT admin, redirect to `/admin/auth` (the admin login page), NOT `/dashboard`.
2.  Update `/admin/auth/page.tsx`:
    - Auto-redirect to `/admin/dashboard` if `session.user.role === 'admin'`.
    - Auto-logout if `session.user` exists but role is NOT `'admin'`.
3.  Ensure the "Admin" link in the Navbar is only visible to admins.

## RESPONSE_TEXT

Refactored `ProtectedRoute` to redirect non-admin users attempting to access admin routes to `/admin/auth` instead of the generic `/dashboard`, breaking the loop. Updated `app/admin/auth/page.tsx` to include an auto-logout effect for non-admin users (clearing stale sessions) and an auto-redirect for existing admins. This created a smooth "Exclusive Gateway" flow for the admin section.

## OUTCOME_IMPACT

- Eliminated the infinite redirect loop.
- Enabled seamless account switching for admins.
- Polished the admin login experience.

## TESTS_SUMMARY

- Verified flow: Login as User -> Go to /admin/dashboard -> Redirected to /admin/auth -> Auto Logout -> Login as Admin -> Redirected to /admin/dashboard.

## FILES_SUMMARY

- `frontend/components/protected-route.tsx`
- `frontend/app/admin/auth/page.tsx`
- `frontend/components/navigation.tsx`

## NEXT_PROMPTS

- Formalize the Admin Dashboard Specification.

## REFLECTION_NOTE

Authentication flows involving multiple roles require distinct entry points and aggressive session clearing to prevent "sticky" wrong-user states.
