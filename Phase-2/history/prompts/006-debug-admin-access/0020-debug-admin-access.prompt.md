---
ID: "0018"
TITLE: "Debug Admin Access 403 Error"
STAGE: "red"
DATE_ISO: "2025-12-14"
SURFACE: "agent"
MODEL: "claude-3-5-sonnet-20241022"
FEATURE: "admin-dashboard"
BRANCH: "main"
USER: "unknown"
COMMAND: "/sp.implement"
LABELS: ["debugging", "auth", "backend", "403-forbidden", "rbac"]
LINKS_SPEC: "null"
LINKS_TICKET: "null"
LINKS_ADR: "null"
LINKS_PR: "null"
FILES_YAML:
 - "failed: backend/promote_admin.py"
 - "failed: backend/fix_role_final.py"
TESTS_YAML:
 - "manual verification of /api/admin/users"
---

# DEBUG ADMIN ACCESS (403 FORBIDDEN)

## PROMPT_TEXT

/sp.implement
# Debug Admin Access (403 Forbidden)

## Context
I am trying to access the `/api/admin/users` endpoint using a user that I believe I have promoted to admin, but I am consistently receiving a `403 Forbidden` error.

## Problem Description
1.  **User ID**: `lNKmaiMTiGexTDFFBbjx0pGqxtw2W78K`
2.  **Expected Role**: "admin"
3.  **Actual Behavior**: Returns `403 Forbidden`. The backend logs show that the user is authenticated, but the permission check fails.

## Attempts
- I tried running scripts to update the role in the database, but they seemed to fail silently or crash.
- I need a way to **force** the admin role update to guarantee it's applied.

## Request
Please debug why the backend does not recognize my admin role.
1.  Verify the database schema (does the `role` column exist?).
2.  Create a robust method to force-update the user's role to "admin" on server startup if necessary.
3.  Ensure the `get_current_admin` dependency correctly checks the role.

## RESPONSE_TEXT

Investigated the backend 403 error. Initial attempts to run standalone scripts failed due to import errors. Verified that the `user` table has a `role` column. Implemented a direct SQL UPDATE injection in `main.py` lifespan to force the role update on startup, which successfully updated the role in the database to 'admin'. However, frontend access issues persisted, pointing to a separate session issue.

## OUTCOME_IMPACT

- Confirmed User DB schema has `role`.
- Successfully forced user `lNKmaiMT...` to 'admin' role via backend startup hook.
- Identified that while backend role is correct, the issue has layers (Backend OK -> Frontend Session bad).

## TESTS_SUMMARY

- Manual API check: backend logs showed 403 then eventually 200 for API calls.

## FILES_SUMMARY

- `backend/main.py` (Temporary injection)
- `backend/api/deps.py` (Verified logic)

## NEXT_PROMPTS

- Debug why frontend still redirects despite backend 200 OK.

## REFLECTION_NOTE

Direct database access via scripts in a complex async environment can be fragile; sometimes hooking into the running app's lifecycle is more reliable for ad-hoc fixes.
