# Admin Authentication & Dashboard Architecture

## Overview

This spec defines the architecture for the Admin Dashboard, including Role-Based Access Control (RBAC), Authentication flow, and API security.

## 1. Authentication & Session Management

Using **Better Auth** with a Hybrid approach (JWT + Database Session).

### Configuration (`frontend/lib/auth.ts`)

- **Session Strategy**: Database-backed sessions.
- **Custom Fields**: The `role` field MUST be explicitly configured in `user.additionalFields` to be exposed in the React `useSession` hook.
  ```typescript
  user: {
      additionalFields: {
          role: { type: "string", defaultValue: "user" }
      }
  }
  ```

## 2. Protected Routes & Navigation

The `ProtectedRoute` component manages access control.

### Logic Flow

1.  **Loading**: Show Loading Spinner.
2.  **Unauthenticated**: Redirect to `unauthorizedPath` (default `/auth/signin`).
3.  **Authenticated (Role Mismatch)**:
    - If `requireAdmin` is `true` AND `user.role !== 'admin'`:
    - **Redirect to `/admin/auth`** (NOT `/dashboard`). This allows the user to re-login with the correct account.
4.  **Authorized**: Render children.

### Admin Login Page (`/admin/auth`)

- **Auto-Redirect**: If user is already "admin", forward to `/admin/dashboard`.
- **Auto-Logout**: If user is logged in as "user", force `signOut()` immediately to clear the session and allow admin login.

## 3. Backend Security

FastAPI backend enforces role checks via dependencies.

### Dependency: `get_current_admin`

1.  Verifies Session/Token.
2.  Fetches `User` from Database.
3.  **Check**: `if user.role != "admin": raise HTTP_403_FORBIDDEN`.

### CORS Configuration

- **Origins**: Allow `http://localhost:3000`.
- **Credentials**: `Allow-Credentials: true` (Required for cookie-based auth).

## 4. Database Schema

- **User Table**:
  - `role`: String (default "user").
  - `createdAt`/`updatedAt`: Mapped to camelCase for JS compatibility.

## 5. Implementation Status

- [x] Backend Admin Dependency
- [x] Frontend Session Role Config
- [x] Redirect Logic Fixed
- [x] Admin Dashboard UI Implementation
